"""Narration extraction and Azure Speech TTS generation.

Extracted from generate_drama_narration.py — HTML parsing, SSML generation,
MP3 duration calculation, and voice assignment.
"""

import os
import re
import struct
import time
from html.parser import HTMLParser

import requests


# ── Config ──────────────────────────────────────────────────────────────

AZURE_KEY = os.environ.get("AZURE_SPEECH_KEY")
AZURE_REGION = "uksouth"
AZURE_TTS_URL = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

VOICE_ODD = "en-GB-OllieMultilingualNeural"   # Odd lessons
VOICE_EVEN = "en-GB-BellaNeural"               # Even lessons


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
    data = mp3_bytes[:16384]

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


# ── Voice assignment ────────────────────────────────────────────────────

def get_voice_for_lesson(lesson_number):
    """Return (voice_name, label) for a lesson number. Odd=Ollie, Even=Bella."""
    if lesson_number % 2 == 1:
        return VOICE_ODD, "Ollie"
    return VOICE_EVEN, "Bella"
