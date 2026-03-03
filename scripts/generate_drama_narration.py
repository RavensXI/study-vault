"""
Generate TTS narration for Drama GCSE lessons using Azure Speech REST API.
Fetches lesson content from Supabase, generates MP3s, uploads to R2, updates manifests.

Processes 6 lessons:
  - blood-brothers lesson 1 (Ollie)
  - blood-brothers lesson 2 (Bella)
  - blood-brothers lesson 3 (Ollie)
  - blood-brothers lesson 4 (Bella)
  - blood-brothers lesson 5 (Ollie)
  - blood-brothers lesson 6 (Bella)

Usage:
    python scripts/generate_drama_narration.py
"""

import io
import json
import os
import re
import struct
import sys
import time
from html.parser import HTMLParser

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

import boto3
import requests
from botocore.config import Config
from supabase import create_client

# ── Config ──────────────────────────────────────────────────────────────

AZURE_KEY = os.environ.get("AZURE_SPEECH_KEY")
AZURE_REGION = "uksouth"
AZURE_TTS_URL = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

VOICE_ODD = "en-GB-OllieMultilingualNeural"   # Odd lessons
VOICE_EVEN = "en-GB-BellaNeural"               # Even lessons

R2_BUCKET = "studyvault-audio"
R2_PUBLIC_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev"

SUBJECT_SLUG = "drama"

# Lessons to process: (unit_slug, lesson_number)
LESSONS_TO_PROCESS = [
    ("blood-brothers", 1),
    ("blood-brothers", 2),
    ("blood-brothers", 3),
    ("blood-brothers", 4),
    ("blood-brothers", 5),
    ("blood-brothers", 6),
]


# ── HTML Parser ─────────────────────────────────────────────────────────

class NarrationExtractor(HTMLParser):
    """Extract text from elements with data-narration-id attributes."""

    def __init__(self):
        super().__init__()
        self.chunks = []
        self._current_id = None
        self._current_tag = None
        self._current_text = []
        self._skip_depth = 0
        self._tag_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if "data-narration-id" in attrs_dict:
            self._flush_chunk()
            self._current_id = attrs_dict["data-narration-id"]
            self._current_tag = tag
            self._current_text = []
            self._skip_depth = 0
            self._tag_depth = 1
        elif self._current_id:
            if tag == self._current_tag:
                self._tag_depth += 1
        # Skip content inside these tags
        if tag in ("svg", "button", "script", "style"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("svg", "button", "script", "style"):
            self._skip_depth = max(0, self._skip_depth - 1)
        if not self._current_id:
            return
        if tag == self._current_tag:
            self._tag_depth -= 1
            if self._tag_depth <= 0:
                self._flush_chunk()
                return
        # Insert a pause after block-level elements inside a container
        if tag in ("h2", "h3", "p", "div", "li"):
            if self._current_text and not self._current_text[-1].endswith("."):
                self._current_text.append(".")

    def _flush_chunk(self):
        if self._current_id:
            text = " ".join(self._current_text).strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                self.chunks.append((self._current_id, text))
        self._current_id = None
        self._current_tag = None
        self._current_text = []
        self._tag_depth = 0

    def handle_data(self, data):
        if self._current_id and self._skip_depth == 0:
            self._current_text.append(data.strip())

    def handle_entityref(self, name):
        entities = {
            "mdash": "-", "rsquo": "'", "lsquo": "'",
            "rdquo": '"', "ldquo": '"', "amp": "&",
            "ndash": "-", "hellip": "...", "nbsp": " ",
            "rarr": " to ", "larr": " to ", "bull": ", ",
            "pound": "pounds", "euro": "euros",
        }
        if self._current_id:
            self._current_text.append(entities.get(name, ""))

    def handle_charref(self, name):
        """Handle numeric character references like &#8217; (right single quote)."""
        if self._current_id:
            try:
                if name.startswith("x"):
                    char = chr(int(name[1:], 16))
                else:
                    char = chr(int(name))
                self._current_text.append(char)
            except (ValueError, OverflowError):
                pass


def extract_narration_chunks(html_content):
    """Parse HTML and return list of (narration_id, text) tuples."""
    parser = NarrationExtractor()
    parser.feed(html_content)
    # Flush any remaining chunk
    parser._flush_chunk()
    return parser.chunks


# ── XML Escaping for SSML ───────────────────────────────────────────────

def xml_escape(text):
    """Escape text for SSML XML body."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


# ── Azure Speech REST API ───────────────────────────────────────────────

def generate_audio_rest(text, voice_name):
    """Generate MP3 bytes from text using Azure Speech REST API.
    Returns MP3 bytes on success, None on failure.
    """
    ssml = (
        f"<speak version='1.0' xml:lang='en-GB'>"
        f"<voice name='{voice_name}'>{xml_escape(text)}</voice>"
        f"</speak>"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
    }

    for attempt in range(3):
        try:
            resp = requests.post(AZURE_TTS_URL, headers=headers, data=ssml.encode("utf-8"), timeout=60)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 5))
                print(f"      Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"      HTTP {resp.status_code}: {resp.text[:200]}")
                if attempt < 2:
                    time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"      Request error: {e}")
            if attempt < 2:
                time.sleep(2)

    return None


# ── MP3 Duration ────────────────────────────────────────────────────────

def get_mp3_duration(mp3_bytes):
    """Return duration of MP3 in seconds by reading MPEG frame headers."""
    SAMPLE_RATES = {0: [11025, 12000, 8000], 1: [0, 0, 0],
                    2: [22050, 24000, 16000], 3: [44100, 48000, 32000]}
    BITRATES_V1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    SAMPLES_PER_FRAME = 1152  # MPEG1 Layer III

    file_size = len(mp3_bytes)
    data = mp3_bytes[:16384]  # Read enough to find a frame

    # Skip ID3v2 tag if present
    offset = 0
    if data[:3] == b"ID3":
        tag_size = ((data[6] & 0x7f) << 21 | (data[7] & 0x7f) << 14 |
                    (data[8] & 0x7f) << 7 | (data[9] & 0x7f))
        offset = tag_size + 10

    # Find first valid MPEG frame header
    while offset < len(data) - 4:
        if data[offset] == 0xFF and (data[offset + 1] & 0xE0) == 0xE0:
            header = struct.unpack(">I", data[offset:offset + 4])[0]
            version = (header >> 19) & 3
            bitrate_idx = (header >> 12) & 0xF
            sr_idx = (header >> 10) & 3

            if version == 3 and bitrate_idx not in (0, 15) and sr_idx != 3:
                bitrate = BITRATES_V1[bitrate_idx] * 1000
                sample_rate = SAMPLE_RATES[version][sr_idx]
                if bitrate > 0 and sample_rate > 0:
                    audio_bytes = file_size - offset
                    total_frames = audio_bytes * sample_rate / (SAMPLES_PER_FRAME * (bitrate / 8))
                    return round(total_frames * SAMPLES_PER_FRAME / sample_rate, 2)
        offset += 1

    # Fallback: estimate from file size and known bitrate (96kbps)
    return round(file_size * 8 / 96000, 2)


# ── R2 Upload ───────────────────────────────────────────────────────────

def get_r2_client():
    """Create an S3-compatible client for Cloudflare R2."""
    account_id = os.environ.get("R2_ACCOUNT_ID")
    access_key = os.environ.get("R2_ACCESS_KEY_ID")
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")

    if not all([account_id, access_key, secret_key]):
        print("ERROR: Missing R2 environment variables.")
        print("Required: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY")
        sys.exit(1)

    return boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(
            region_name="auto",
            retries={"max_attempts": 3, "mode": "adaptive"},
        ),
    )


def upload_to_r2(r2_client, r2_key, mp3_bytes):
    """Upload MP3 bytes to R2. Returns public URL."""
    r2_client.put_object(
        Bucket=R2_BUCKET,
        Key=r2_key,
        Body=mp3_bytes,
        ContentType="audio/mpeg",
    )
    return f"{R2_PUBLIC_URL}/{r2_key}"


# ── Main Processing ─────────────────────────────────────────────────────

def process_lesson(sb, r2_client, unit_slug, unit_id, lesson_number):
    """Process a single lesson: fetch, parse, generate TTS, upload, update manifest."""

    voice = VOICE_ODD if lesson_number % 2 == 1 else VOICE_EVEN
    voice_label = "Ollie" if lesson_number % 2 == 1 else "Bella"

    print(f"\n  {unit_slug} / Lesson {lesson_number:02d} ({voice_label})")
    print(f"  {'=' * 50}")

    lesson_start = time.time()

    # Fetch lesson from Supabase
    lesson = (
        sb.table("lessons")
        .select("id, lesson_number, title, content_html, exam_tip_html, conclusion_html")
        .eq("unit_id", unit_id)
        .eq("lesson_number", lesson_number)
        .single()
        .execute()
    )
    lesson_data = lesson.data
    lesson_id = lesson_data["id"]

    print(f"  Title: {lesson_data['title']}")
    print(f"  Lesson ID: {lesson_id}")

    # Combine HTML parts for parsing
    combined_html = ""
    if lesson_data.get("content_html"):
        combined_html += lesson_data["content_html"]
    if lesson_data.get("exam_tip_html"):
        combined_html += lesson_data["exam_tip_html"]
    if lesson_data.get("conclusion_html"):
        combined_html += lesson_data["conclusion_html"]

    if not combined_html:
        print("  ERROR: No HTML content found")
        return 0, 0, 0.0

    # Extract narration chunks
    chunks = extract_narration_chunks(combined_html)
    if not chunks:
        print("  ERROR: No narration chunks found (no data-narration-id elements)")
        return 0, 0, 0.0

    print(f"  Found {len(chunks)} narration chunks")

    # Generate audio, upload, build manifest
    manifest = []
    total_chars = 0
    generated_count = 0
    total_duration = 0.0

    for narration_id, text in chunks:
        r2_key = f"drama/{unit_slug}/narration_lesson-{lesson_number:02d}_{narration_id}.mp3"
        public_url = f"{R2_PUBLIC_URL}/{r2_key}"

        total_chars += len(text)

        # Display truncated text
        display = text[:70] + "..." if len(text) > 70 else text
        display = display.encode("ascii", errors="replace").decode("ascii")
        print(f"    {narration_id}: {display}")

        # Generate MP3
        mp3_bytes = generate_audio_rest(text, voice)
        if mp3_bytes is None:
            print(f"    FAILED to generate audio for {narration_id}")
            continue

        # Calculate duration
        duration = get_mp3_duration(mp3_bytes)
        total_duration += duration

        # Upload to R2
        upload_to_r2(r2_client, r2_key, mp3_bytes)

        manifest.append({
            "id": narration_id,
            "src": public_url,
            "duration": duration,
        })
        generated_count += 1
        print(f"           -> {len(mp3_bytes)/1024:.0f} KB, {duration:.1f}s, uploaded")

    if not manifest:
        print("  ERROR: No audio generated")
        return 0, 0, 0.0

    # Update narration manifest in Supabase
    sb.table("lessons").update(
        {"narration_manifest": manifest}
    ).eq("id", lesson_id).execute()

    elapsed = time.time() - lesson_start
    print(f"  Manifest updated in Supabase ({len(manifest)} entries)")
    print(f"  Total: {generated_count} clips, {total_chars:,} chars, {total_duration:.1f}s audio, {elapsed:.1f}s elapsed")

    return generated_count, total_chars, elapsed


def main():
    # Validate env vars
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY environment variable not set")
        sys.exit(1)

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not supabase_url or not supabase_key:
        print("ERROR: SUPABASE_URL or SUPABASE_SERVICE_KEY not set")
        sys.exit(1)

    print("Drama GCSE TTS Narration Generator")
    print("=" * 55)
    print(f"Azure Speech API: {AZURE_REGION}")
    print(f"R2 bucket: {R2_BUCKET}")
    print(f"Odd lessons -> {VOICE_ODD}")
    print(f"Even lessons -> {VOICE_EVEN}")
    print(f"Lessons to process: {len(LESSONS_TO_PROCESS)}")
    print()

    # Connect to Supabase
    sb = create_client(supabase_url, supabase_key)

    # Look up drama subject and units
    subjects = sb.table("subjects").select("id, slug").eq("slug", SUBJECT_SLUG).execute()
    if not subjects.data:
        print(f"ERROR: Subject '{SUBJECT_SLUG}' not found in Supabase")
        sys.exit(1)
    subject_id = subjects.data[0]["id"]
    print(f"Drama subject ID: {subject_id}")

    # Get all drama units
    units = sb.table("units").select("id, slug").eq("subject_id", subject_id).execute()
    unit_map = {u["slug"]: u["id"] for u in units.data}
    print(f"Units: {list(unit_map.keys())}")
    print()

    # Create R2 client
    r2_client = get_r2_client()

    # Process each lesson
    total_start = time.time()
    total_clips = 0
    total_chars = 0
    lesson_results = []

    for unit_slug, lesson_num in LESSONS_TO_PROCESS:
        if unit_slug not in unit_map:
            print(f"\n  ERROR: Unit '{unit_slug}' not found. Available: {list(unit_map.keys())}")
            continue

        unit_id = unit_map[unit_slug]
        clips, chars, elapsed = process_lesson(sb, r2_client, unit_slug, unit_id, lesson_num)
        total_clips += clips
        total_chars += chars
        lesson_results.append((unit_slug, lesson_num, clips, chars, elapsed))

    total_elapsed = time.time() - total_start

    # Summary
    print(f"\n{'=' * 55}")
    print(f"SUMMARY")
    print(f"{'=' * 55}")
    print(f"{'Unit':<20} {'Lesson':<10} {'Clips':<8} {'Chars':<10} {'Time':<10}")
    print(f"{'-' * 55}")
    for unit_slug, lesson_num, clips, chars, elapsed in lesson_results:
        print(f"{unit_slug:<20} L{lesson_num:02d}       {clips:<8} {chars:<10,} {elapsed:.1f}s")
    print(f"{'-' * 55}")
    print(f"{'TOTAL':<31} {total_clips:<8} {total_chars:<10,} {total_elapsed:.1f}s")

    cost_estimate = total_chars * 16 / 1_000_000
    print(f"\nEstimated cost: ${cost_estimate:.2f} (at $16/1M chars)")
    if total_elapsed > 0:
        print(f"Clips/min: {total_clips / (total_elapsed / 60):.0f}")
    print(f"\nDone! All manifests updated in Supabase.")


if __name__ == "__main__":
    main()
