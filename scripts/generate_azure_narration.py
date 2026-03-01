"""
Generate TTS narration for Study Vault lessons using Azure Speech.
Alternates voices: odd lessons = Ollie (male), even lessons = Bella (female).

Usage:
    python scripts/generate_azure_narration.py --dir history/conflict-tension
    python scripts/generate_azure_narration.py --dir geography/paper-1 1 5 10
    python scripts/generate_azure_narration.py --dir sport-science/r180
"""

import glob
import io
import os
import re
import sys
import time
import wave
from html.parser import HTMLParser

# Fix Windows console encoding — allow Unicode chars to print without crashing
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    # Force UTF-8 mode for the whole process
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

# Azure Speech SDK
import azure.cognitiveservices.speech as speechsdk


def get_wav_duration(wav_path):
    """Return duration of a WAV file in seconds."""
    with wave.open(wav_path, "rb") as wf:
        return wf.getnframes() / wf.getframerate()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

AZURE_KEY = os.environ.get("AZURE_SPEECH_KEY")
AZURE_REGION = "uksouth"

VOICE_ODD = "en-GB-OllieMultilingualNeural"   # Lessons 1, 3, 5, 7, 9...
VOICE_EVEN = "en-GB-BellaNeural"               # Lessons 2, 4, 6, 8, 10...


class NarrationExtractor(HTMLParser):
    """Extract text content from elements with data-narration-id attributes."""

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
            # Save any previous chunk
            self._flush_chunk()
            self._current_id = attrs_dict["data-narration-id"]
            self._current_tag = tag
            self._current_text = []
            self._skip_depth = 0
            self._tag_depth = 1
        elif self._current_id:
            # Track nested depth of the same tag type
            if tag == self._current_tag:
                self._tag_depth += 1
        # Skip content inside these tags
        if tag in ("svg", "button", "script"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("svg", "button", "script"):
            self._skip_depth = max(0, self._skip_depth - 1)
        if not self._current_id:
            return
        # Track depth for matching container tag
        if tag == self._current_tag:
            self._tag_depth -= 1
            if self._tag_depth <= 0:
                self._flush_chunk()
                return
        # Insert a pause after any block-level element inside a container
        if tag in ("h2", "h3", "p", "div", "li"):
            if self._current_text and not self._current_text[-1].endswith("."):
                self._current_text.append(".")

    def _flush_chunk(self):
        if self._current_id:
            text = " ".join(self._current_text).strip()
            # Clean up multiple spaces
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
        entities = {"mdash": "-", "rsquo": "'", "lsquo": "'",
                    "rdquo": '"', "ldquo": '"', "amp": "&",
                    "ndash": "-", "hellip": "...", "nbsp": " ",
                    "rarr": " to ", "larr": " to ", "bull": ", ",
                    "pound": "pounds", "euro": "euros"}
        if self._current_id:
            self._current_text.append(entities.get(name, ""))


def extract_narration_chunks(html_path):
    """Parse lesson HTML and return list of (narration_id, text) tuples."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    parser = NarrationExtractor()
    parser.feed(html)
    return parser.chunks


def generate_audio(text, voice_name, output_path):
    """Generate a WAV file from text using Azure TTS."""
    config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
    config.speech_synthesis_voice_name = voice_name
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
    )
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    synth = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio_config)
    result = synth.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return True
    else:
        details = ""
        if result.cancellation_details:
            details = result.cancellation_details.error_details
        print(f"    ERROR: {details}")
        return False


def update_manifest(html_path, manifest_entries):
    """Update the narrationManifest in the lesson HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    manifest_js = "window.narrationManifest = [\n"
    for entry in manifest_entries:
        manifest_js += f'      {{ id: "{entry["id"]}", src: "{entry["src"]}", duration: {entry["duration"]} }},\n'
    manifest_js += "    ];"

    content = re.sub(
        r"window\.narrationManifest\s*=\s*\[.*?\];",
        manifest_js,
        content,
        flags=re.DOTALL,
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)


def process_lesson(lesson_dir, lesson_num):
    """Generate narration for a single lesson. Returns (clips, chars, seconds)."""
    filename = f"lesson-{lesson_num:02d}.html"
    html_path = os.path.join(lesson_dir, filename)

    if not os.path.exists(html_path):
        print(f"  Skipping {filename} - file not found")
        return 0, 0, 0.0

    voice = VOICE_ODD if lesson_num % 2 == 1 else VOICE_EVEN
    voice_label = "Ollie" if lesson_num % 2 == 1 else "Bella"
    print(f"\n  Lesson {lesson_num:02d} ({voice_label})")
    print(f"  {'=' * 40}")

    lesson_start = time.time()

    chunks = extract_narration_chunks(html_path)
    if not chunks:
        print("  No narration chunks found")
        return 0, 0, 0.0

    print(f"  Found {len(chunks)} chunks")

    manifest_entries = []
    total_chars = 0
    generated_count = 0
    for narration_id, text in chunks:
        wav_filename = f"narration_lesson-{lesson_num:02d}_{narration_id}.wav"
        wav_path = os.path.join(lesson_dir, wav_filename)

        # Skip if already generated
        if os.path.exists(wav_path):
            dur = get_wav_duration(wav_path)
            print(f"    {narration_id}: already exists ({dur:.1f}s), skipping")
            manifest_entries.append({"id": narration_id, "src": wav_filename, "duration": round(dur, 2)})
            continue

        total_chars += len(text)
        # Truncate display text — also encode-safe for Windows consoles
        display = text[:60] + "..." if len(text) > 60 else text
        display = display.encode("ascii", errors="replace").decode("ascii")
        print(f"    {narration_id}: {display}")

        if generate_audio(text, voice, wav_path):
            dur = get_wav_duration(wav_path)
            manifest_entries.append({"id": narration_id, "src": wav_filename, "duration": round(dur, 2)})
            generated_count += 1
        else:
            print(f"    FAILED: {narration_id}")

    # Update manifest in HTML
    update_manifest(html_path, manifest_entries)
    elapsed = time.time() - lesson_start
    print(f"  Manifest updated ({len(manifest_entries)} entries)")
    print(f"  Lesson {lesson_num:02d}: {generated_count} clips, {total_chars:,} chars, {elapsed:.1f}s")

    return generated_count, total_chars, elapsed


def auto_detect_lessons(lesson_dir):
    """Find all lesson-NN.html files and return sorted lesson numbers."""
    pattern = os.path.join(lesson_dir, "lesson-*.html")
    files = glob.glob(pattern)
    nums = []
    for f in files:
        m = re.search(r"lesson-(\d+)\.html$", f)
        if m:
            nums.append(int(m.group(1)))
    return sorted(nums)


def main():
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY environment variable not set")
        sys.exit(1)

    # Parse --dir argument
    args = sys.argv[1:]
    lesson_dir = None
    lesson_nums = []

    i = 0
    while i < len(args):
        if args[i] == "--dir" and i + 1 < len(args):
            lesson_dir = os.path.join(PROJECT_ROOT, args[i + 1])
            i += 2
        else:
            lesson_nums.append(int(args[i]))
            i += 1

    if not lesson_dir:
        print("ERROR: --dir argument required")
        print("Usage: python generate_azure_narration.py --dir history/conflict-tension [1 2 3...]")
        sys.exit(1)

    if not os.path.isdir(lesson_dir):
        print(f"ERROR: Directory not found: {lesson_dir}")
        sys.exit(1)

    # Auto-detect lessons if none specified
    if not lesson_nums:
        lesson_nums = auto_detect_lessons(lesson_dir)

    if not lesson_nums:
        print(f"ERROR: No lesson files found in {lesson_dir}")
        sys.exit(1)

    unit_name = os.path.relpath(lesson_dir, PROJECT_ROOT)
    print(f"Azure TTS Narration Generator")
    print(f"Unit: {unit_name}")
    print(f"Lessons: {lesson_nums}")
    print(f"Odd lessons -> {VOICE_ODD}")
    print(f"Even lessons -> {VOICE_EVEN}")

    total_start = time.time()
    total_clips = 0
    total_chars = 0
    lesson_timings = []

    for lesson_num in lesson_nums:
        clips, chars, elapsed = process_lesson(lesson_dir, lesson_num)
        total_clips += clips
        total_chars += chars
        lesson_timings.append((lesson_num, clips, chars, elapsed))

    total_elapsed = time.time() - total_start

    # Summary
    print(f"\n{'=' * 50}")
    print(f"SUMMARY: {unit_name}")
    print(f"{'=' * 50}")
    print(f"{'Lesson':<10} {'Clips':<8} {'Chars':<10} {'Time':<10}")
    print(f"{'-' * 38}")
    for num, clips, chars, elapsed in lesson_timings:
        print(f"L{num:02d}       {clips:<8} {chars:<10,} {elapsed:.1f}s")
    print(f"{'-' * 38}")
    print(f"{'TOTAL':<10} {total_clips:<8} {total_chars:<10,} {total_elapsed:.1f}s")
    cost_estimate = total_chars * 16 / 1_000_000  # $16 per 1M chars
    print(f"\nEstimated cost: ${cost_estimate:.2f} (at $16/1M chars)")
    print(f"Clips/min: {total_clips / (total_elapsed / 60):.0f}" if total_elapsed > 0 else "")
    print(f"\nDone!")


if __name__ == "__main__":
    main()
