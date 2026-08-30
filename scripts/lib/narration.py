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
VOICE_EVEN = "en-GB-AdaMultilingualNeural"     # Even lessons

# Language codes for multilingual SSML <lang> tags
SUBJECT_LANG_CODES = {
    "french": "fr-FR",
    "german": "de-DE",
    "spanish": "es-ES",
}


# ── LaTeX to spoken English ────────────────────────────────────────────

def _repair_latex_escapes(text):
    """Repair damaged LaTeX escape sequences in text.

    When content was stored via Python/JSON without raw strings, sequences
    like \\frac became form-feed+'rac', \\neq became newline+'eq', etc.
    This restores the original LaTeX commands.
    """
    # Direct character replacements (safe — these chars don't belong in HTML text)
    text = text.replace("\x0c", "\\f")   # form feed → \f (\frac, \forall)
    text = text.replace("\x08", "\\b")   # backspace → \b (\beta, \bar, \binom)

    # Tab and newline are trickier — they exist as real whitespace in HTML.
    # Only repair inside LaTeX delimiters where they indicate damaged commands.
    def _repair_region(m):
        region = m.group(0)
        region = region.replace("\t", "\\t")  # \times, \theta, \tan, \text, \to
        region = region.replace("\n", "\\n")  # \neq, \ne, \nu, \nabla, \not
        region = region.replace("\r", "\\r")  # \rightarrow, \rho
        return region

    # Repair inside inline math \(...\)
    text = re.sub(r"\\\(.*?\\\)", _repair_region, text, flags=re.DOTALL)
    # Repair inside display math $$...$$
    text = re.sub(r"\$\$.*?\$\$", _repair_region, text, flags=re.DOTALL)
    # Repair inside display math \[...\]
    text = re.sub(r"\\\[.*?\\\]", _repair_region, text, flags=re.DOTALL)

    return text


def latex_to_spoken(text):
    """Convert LaTeX math notation embedded in text to spoken English.

    Handles inline \\(...\\), display $$...$$ and \\[...\\] regions.
    Converts common GCSE-level LaTeX to natural spoken maths.
    First repairs damaged escape sequences from storage.
    """
    text = _repair_latex_escapes(text)

    def _convert_math(latex):
        s = latex.strip()

        # Strip \left / \right (keep the bracket)
        s = re.sub(r"\\left\s*([(\[{|.])", r"\1", s)
        s = re.sub(r"\\right\s*([)\]}|.])", r"\1", s)

        # \text{...}, \textbf{...}, \mathrm{...} → plain text
        s = re.sub(r"\\(?:text|textbf|mathrm|mathbf)\{([^{}]*)\}", r"\1", s)

        # Iteratively resolve nested structures (innermost braces first)
        for _ in range(12):
            prev = s

            # \frac{a}{b} → (a over b)
            s = re.sub(
                r"\\frac\{([^{}]*)\}\{([^{}]*)\}",
                lambda m: f"({m.group(1).strip()} over {m.group(2).strip()})",
                s,
            )

            # \sqrt[n]{x} → nth root of x
            s = re.sub(
                r"\\sqrt\[([^\]]*)\]\{([^{}]*)\}",
                lambda m: f"{m.group(1)}th root of {m.group(2).strip()}",
                s,
            )

            # \sqrt{x} → square root of x
            s = re.sub(
                r"\\sqrt\{([^{}]*)\}",
                lambda m: f"square root of {m.group(1).strip()}",
                s,
            )

            # Superscripts: x^{2} → x squared, x^{3} → x cubed
            s = re.sub(r"\^\{2\}", " squared", s)
            s = re.sub(r"\^2(?![0-9])", " squared", s)
            s = re.sub(r"\^\{3\}", " cubed", s)
            s = re.sub(r"\^3(?![0-9])", " cubed", s)
            s = re.sub(r"\^\{([^{}]*)\}", r" to the power of \1", s)

            # Subscripts: x_{n} → x sub n
            s = re.sub(r"_\{([^{}]*)\}", r" sub \1", s)

            if s == prev:
                break

        # Single-char subscripts: x_n → x sub n (after braces removed)
        s = re.sub(r"_([a-zA-Z0-9])", r" sub \1", s)

        # Symbol replacements (order matters — longer commands first)
        _SYMBOLS = [
            (r"\rightarrow", "gives"),
            (r"\therefore", "therefore"),
            (r"\overline", ""),
            (r"\approx", "approximately equals"),
            (r"\propto", "is proportional to"),
            (r"\equiv", "is equivalent to"),
            (r"\infty", "infinity"),
            (r"\times", " times "),
            (r"\cdot", " times "),
            (r"\qquad", " "),
            (r"\theta", "theta"),
            (r"\alpha", "alpha"),
            (r"\gamma", "gamma"),
            (r"\delta", "delta"),
            (r"\sigma", "sigma"),
            (r"\omega", "omega"),
            (r"\lambda", "lambda"),
            (r"\prime", " prime"),
            (r"\angle", "angle "),
            (r"\quad", " "),
            (r"\beta", "beta"),
            (r"\neq", " is not equal to "),
            (r"\leq", " is less than or equal to "),
            (r"\geq", " is greater than or equal to "),
            (r"\div", " divided by "),
            (r"\cos", "cosine"),
            (r"\sin", "sine"),
            (r"\tan", "tangent"),
            (r"\log", "log"),
            (r"\vec", "vector "),
            (r"\hat", ""),
            (r"\bar", ""),
            (r"\pm", " plus or minus "),
            (r"\mp", " minus or plus "),
            (r"\ne", " is not equal to "),
            (r"\le", " is less than or equal to "),
            (r"\ge", " is greater than or equal to "),
            (r"\pi", "pi"),
            (r"\mu", "mu"),
            (r"\ln", "natural log"),
            (r"\to", " to "),
            (r"\,", " "),
            (r"\;", " "),
            (r"\!", ""),
            (r"\ ", " "),
        ]
        for cmd, spoken in _SYMBOLS:
            s = s.replace(cmd, spoken)

        # Remove any remaining backslash commands
        s = re.sub(r"\\[a-zA-Z]+", "", s)

        # Strip braces
        s = s.replace("{", "").replace("}", "")

        # Equals sign → "equals"
        s = s.replace("=", " equals ")

        # Clean up whitespace and stray punctuation
        s = re.sub(r"\s+", " ", s).strip()
        return s

    # Replace display math $$...$$ (greedy-safe with DOTALL)
    text = re.sub(
        r"\$\$(.*?)\$\$",
        lambda m: _convert_math(m.group(1)),
        text,
        flags=re.DOTALL,
    )
    # Replace display math \[...\]
    text = re.sub(
        r"\\\[(.*?)\\\]",
        lambda m: _convert_math(m.group(1)),
        text,
        flags=re.DOTALL,
    )
    # Replace inline math \(...\)
    text = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: _convert_math(m.group(1)),
        text,
        flags=re.DOTALL,
    )
    # Clean up double spaces
    text = re.sub(r"\s+", " ", text)
    return text


# ── HTML Parser ─────────────────────────────────────────────────────────

class NarrationExtractor(HTMLParser):
    """Extract text from elements with data-narration-id attributes.

    When lang_code is set (e.g. 'fr-FR'), <em> content is wrapped in
    {{LANG_START}} / {{LANG_END}} markers so SSML can insert <lang> tags.
    """

    def __init__(self, lang_code=None):
        super().__init__()
        self.chunks = []
        self._current_id = None
        self._current_tag = None
        self._current_text = []
        self._skip_depth = 0
        self._tag_depth = 0
        self._lang_code = lang_code
        self._in_foreign = False
        self._foreign_depth = 0

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
        # Track <em> and <strong> for foreign language marking
        if tag in ("em", "strong") and self._lang_code and self._current_id:
            if not self._in_foreign:
                self._in_foreign = True
                self._foreign_depth = 1
                self._current_text.append("{{LANG_START}}")
            else:
                self._foreign_depth += 1

    def handle_endtag(self, tag):
        if tag in ("svg", "button", "script", "style"):
            self._skip_depth = max(0, self._skip_depth - 1)
        # Close foreign language marker
        if tag in ("em", "strong") and self._in_foreign:
            self._foreign_depth -= 1
            if self._foreign_depth <= 0:
                self._current_text.append("{{LANG_END}}")
                self._in_foreign = False
                self._foreign_depth = 0
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
            text = latex_to_spoken(text)
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


def extract_narration_chunks(html_content, lang_code=None):
    """Parse HTML and return list of (narration_id, text) tuples.

    If lang_code is set (e.g. 'fr-FR'), <em> content is marked with
    {{LANG_START}}/{{LANG_END}} for SSML language switching.
    """
    # Repair damaged LaTeX escapes BEFORE the HTML parser sees the content,
    # because handle_data().strip() removes form feed / tab / newline chars.
    html_content = _repair_latex_escapes(html_content)
    parser = NarrationExtractor(lang_code=lang_code)
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

def _build_ssml_body(text, lang_code=None):
    """Build SSML body text, converting {{LANG_START}}/{{LANG_END}} markers
    to proper <lang> + <break> + <prosody> SSML tags.

    If no markers present or lang_code is None, returns plain xml-escaped text.
    """
    if not lang_code or "{{LANG_START}}" not in text:
        return xml_escape(text)

    # Split on markers and build SSML with language switches
    parts = []
    remaining = text
    while "{{LANG_START}}" in remaining:
        before, _, rest = remaining.partition("{{LANG_START}}")
        foreign, _, remaining = rest.partition("{{LANG_END}}")
        if before.strip():
            parts.append(xml_escape(before.strip()))
        parts.append(
            f'<break time="500ms"/>'
            f'<lang xml:lang="{lang_code}">'
            f'<prosody rate="-8%">{xml_escape(foreign.strip())}</prosody>'
            f'</lang>'
            f'<break time="300ms"/>'
        )
    if remaining.strip():
        parts.append(xml_escape(remaining.strip()))

    return " ".join(parts)


def generate_audio_rest(text, voice_name, lang_code=None):
    """Generate MP3 bytes from text using Azure Speech REST API.

    If lang_code is set, {{LANG_START}}/{{LANG_END}} markers in text
    are converted to SSML <lang> tags with a 500ms pause and -15% speed.

    Returns MP3 bytes on success, None on failure.
    """
    body = _build_ssml_body(text, lang_code)
    ssml = (
        f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
        f"xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-GB'>"
        f"<voice name='{voice_name}'>{body}</voice>"
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
    """Return duration of MP3 in seconds by reading MPEG frame headers.

    Handles MPEG-1 AND MPEG-2/2.5 Layer III. Azure's house format
    (96kbps 24kHz mono) is MPEG-2, which the old version of this
    function rejected - it then byte-scanned to a false-positive header
    and produced durations up to 3.4x off (the "manifest durations
    unreliable" bug, root-caused 30 Aug 2026).
    """
    SAMPLE_RATES = {0: [11025, 12000, 8000], 1: [0, 0, 0],
                    2: [22050, 24000, 16000], 3: [44100, 48000, 32000]}
    # Layer III bitrate tables (kbps): MPEG-1 vs MPEG-2/2.5
    BITRATES_V1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    BITRATES_V2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]

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
            version = (header >> 19) & 3     # 0=MPEG2.5, 2=MPEG2, 3=MPEG1
            layer = (header >> 17) & 3       # 1 = Layer III
            bitrate_idx = (header >> 12) & 0xF
            sr_idx = (header >> 10) & 3

            if (version in (0, 2, 3) and layer == 1
                    and bitrate_idx not in (0, 15) and sr_idx != 3):
                table = BITRATES_V1 if version == 3 else BITRATES_V2
                samples_per_frame = 1152 if version == 3 else 576
                bitrate = table[bitrate_idx] * 1000
                sample_rate = SAMPLE_RATES[version][sr_idx]
                if version == 0:
                    sample_rate //= 2  # MPEG2.5 halves the MPEG2 rates
                if bitrate > 0 and sample_rate > 0:
                    audio_bytes = file_size - offset
                    total_frames = audio_bytes * sample_rate / (samples_per_frame * (bitrate / 8))
                    return round(total_frames * samples_per_frame / sample_rate, 2)
        offset += 1

    # Fallback: estimate from file size and known bitrate (96kbps)
    return round(file_size * 8 / 96000, 2)


# ── Voice assignment ────────────────────────────────────────────────────

def get_voice_for_lesson(lesson_number):
    """Return (voice_name, label) for a lesson number. Odd=Ollie, Even=Ada."""
    if lesson_number % 2 == 1:
        return VOICE_ODD, "Ollie"
    return VOICE_EVEN, "Ada"
