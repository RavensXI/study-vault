"""
TTS Generation Script for StudyVault
Extracts narrable text from a lesson HTML, generates TTS via ElevenLabs API,
concatenates into a single WAV, and outputs a timestamp manifest.
"""

import urllib.request, json, struct, time, re, sys, os
from html.parser import HTMLParser

ELEVENLABS_API_KEY = "sk_37afa4e9f19765f44dd63e4827a22946de57096e9f3b7f14"
VOICE_ID = "Nd6wm0mR1AWfjae7WcRB"
MODEL_ID = "eleven_turbo_v2_5"
SAMPLE_RATE = 24000
SILENCE_PADDING = 0.4  # seconds between chunks


class NarrationExtractor(HTMLParser):
    """Extract text from elements with data-narration-id attributes."""

    # CSS classes whose text content should be skipped (visual labels only)
    SKIP_CLASSES = {'key-fact-label', 'exam-tip-label'}

    def __init__(self):
        super().__init__()
        self.chunks = []  # list of (id, text)
        self._current_id = None
        self._current_text = []
        self._depth = 0
        self._skip = False
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Track skip depth for nested elements inside skipped containers
        if self._skip:
            self._skip_depth += 1
            if self._current_id:
                self._depth += 1
            return

        # Skip script, style, and visual-only label elements
        classes = set(attrs_dict.get('class', '').split())
        if tag in ('script', 'style') or (classes & self.SKIP_CLASSES):
            self._skip = True
            self._skip_depth = 1
            if self._current_id:
                self._depth += 1
            return

        narration_id = attrs_dict.get('data-narration-id')
        if narration_id:
            # If we were already collecting, save the previous chunk
            if self._current_id:
                text = ' '.join(self._current_text).strip()
                if text:
                    self.chunks.append((self._current_id, text))
            self._current_id = narration_id
            self._current_text = []
            self._depth = 1
        elif self._current_id:
            self._depth += 1

    def handle_endtag(self, tag):
        if self._skip:
            self._skip_depth -= 1
            if self._skip_depth <= 0:
                self._skip = False
            if self._current_id:
                self._depth -= 1
                if self._depth <= 0:
                    text = ' '.join(self._current_text).strip()
                    if text:
                        self.chunks.append((self._current_id, text))
                    self._current_id = None
                    self._current_text = []
            return

        if self._current_id:
            self._depth -= 1
            if self._depth <= 0:
                text = ' '.join(self._current_text).strip()
                if text:
                    self.chunks.append((self._current_id, text))
                self._current_id = None
                self._current_text = []

    def handle_data(self, data):
        if self._skip:
            return
        if self._current_id:
            cleaned = data.strip()
            if cleaned:
                self._current_text.append(cleaned)

    def handle_entityref(self, name):
        if self._skip:
            return
        if self._current_id:
            entities = {
                'mdash': '\u2014', 'ndash': '\u2013',
                'rsquo': '\u2019', 'lsquo': '\u2018',
                'rdquo': '\u201d', 'ldquo': '\u201c',
                'amp': '&', 'lt': '<', 'gt': '>',
                'nbsp': ' '
            }
            self._current_text.append(entities.get(name, f'&{name};'))


def normalise_for_tts(text):
    """Normalise text for cleaner TTS output."""
    # Smart quotes → straight quotes, then strip double quotes entirely
    text = text.replace('\u201c', '').replace('\u201d', '')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('"', '')
    # Em/en dashes → spoken pauses
    text = text.replace('\u2014', ' - ').replace('\u2013', '-')
    # Parenthetical asides → comma-wrapped for natural speech
    # e.g. "David Lloyd George (Britain)" → "David Lloyd George, Britain,"
    text = re.sub(r'\(([^)]+)\)', r', \1,', text)
    # Ampersands → "and"
    text = text.replace(' & ', ' and ')
    # Numbered list items: "1. Text" → "1, Text" (avoids "one period")
    text = re.sub(r'(\d+)\. ', r'\1, ', text)
    # Clean up punctuation artefacts from above transformations
    text = re.sub(r',\s*,', ',', text)       # double commas
    text = re.sub(r',\.', '.', text)          # comma before period
    text = re.sub(r',;', ';', text)           # comma before semicolon
    text = re.sub(r'\s,', ',', text)          # space before comma
    # Collapse any double spaces
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text.strip()


def extract_narration_chunks(html_path):
    """Parse HTML and extract narration chunks in order."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    parser = NarrationExtractor()
    parser.feed(html)

    # Flush any remaining chunk
    if parser._current_id and parser._current_text:
        text = ' '.join(parser._current_text).strip()
        if text:
            parser.chunks.append((parser._current_id, text))

    # Normalise text for TTS
    return [(cid, normalise_for_tts(text)) for cid, text in parser.chunks]


def generate_tts_chunk(text, chunk_id, retries=5):
    """Generate TTS audio for a single text chunk via ElevenLabs API."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=pcm_24000"

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/pcm"
    }

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, json.dumps(payload).encode(), headers)
            resp = urllib.request.urlopen(req, timeout=120)
            pcm = resp.read()
            duration = len(pcm) / (SAMPLE_RATE * 2)
            print(f"  {chunk_id}: {duration:.1f}s ({len(text)} chars)")
            return pcm
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            wait = 2 * (attempt + 1)
            print(f"  {chunk_id} attempt {attempt+1} failed: HTTP {e.code} {body[:200]} \u2014 retrying in {wait}s...")
            time.sleep(wait)
        except Exception as e:
            wait = 2 * (attempt + 1)
            print(f"  {chunk_id} attempt {attempt+1} failed: {e} \u2014 retrying in {wait}s...")
            time.sleep(wait)

    raise Exception(f"All retries failed for chunk {chunk_id}")


def write_wav(filename, pcm_data):
    """Write raw PCM data as a WAV file."""
    data_size = len(pcm_data)
    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))           # chunk size
        f.write(struct.pack('<H', 1))            # PCM format
        f.write(struct.pack('<H', 1))            # mono
        f.write(struct.pack('<I', SAMPLE_RATE))  # sample rate
        f.write(struct.pack('<I', SAMPLE_RATE * 2))  # byte rate
        f.write(struct.pack('<H', 2))            # block align
        f.write(struct.pack('<H', 16))           # bits per sample
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        f.write(pcm_data)


def inline_manifest(html_path, manifest):
    """Update the narration manifest in the lesson HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new manifest JS
    lines = []
    for entry in manifest:
        lines.append(f'      {{ id: "{entry["id"]}", start: {entry["start"]}, end: {entry["end"]} }}')
    new_manifest = "    window.narrationManifest = [\n" + ",\n".join(lines) + "\n    ];"

    # Replace existing manifest or insert before practiceQuestions
    if 'window.narrationManifest' in content:
        content = re.sub(
            r'    window\.narrationManifest = \[.*?\];',
            new_manifest,
            content,
            flags=re.DOTALL
        )
    else:
        # Insert before practiceQuestions
        content = content.replace(
            '    window.practiceQuestions',
            new_manifest + '\n\n    window.practiceQuestions'
        )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_tts.py <lesson-html-path>")
        sys.exit(1)

    html_path = sys.argv[1]
    base_dir = os.path.dirname(html_path)
    lesson_name = os.path.splitext(os.path.basename(html_path))[0]
    wav_path = os.path.join(base_dir, f"{lesson_name}-narration.wav")
    json_path = os.path.join(base_dir, f"{lesson_name}-narration.json")

    print(f"Extracting narration chunks from {html_path}...")
    chunks = extract_narration_chunks(html_path)
    print(f"Found {len(chunks)} chunks\n")

    if not chunks:
        print("No narration chunks found!")
        sys.exit(1)

    # Generate silence padding (0.4s of zeros)
    silence = b'\x00' * int(SILENCE_PADDING * SAMPLE_RATE * 2)

    # Generate TTS for each chunk and build manifest
    all_pcm = b''
    manifest = []
    current_time = 0.0
    total_chars = sum(len(text) for _, text in chunks)
    print(f"Generating TTS ({total_chars:,} chars, ~{total_chars // 2:,} credits)...")

    for i, (chunk_id, text) in enumerate(chunks):
        pcm = generate_tts_chunk(text, chunk_id)
        duration = len(pcm) / (SAMPLE_RATE * 2)

        manifest.append({
            "id": chunk_id,
            "start": round(current_time, 2),
            "end": round(current_time + duration, 2)
        })

        all_pcm += pcm
        current_time += duration

        # Add silence padding between chunks (not after the last one)
        if i < len(chunks) - 1:
            all_pcm += silence
            current_time += SILENCE_PADDING

    # Write WAV
    print(f"\nWriting WAV to {wav_path}...")
    write_wav(wav_path, all_pcm)
    total_duration = current_time
    print(f"Total duration: {total_duration:.1f}s ({total_duration/60:.1f} min)")

    # Write manifest JSON
    print(f"Writing manifest to {json_path}...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    # Inline manifest into HTML
    print(f"Inlining manifest into {html_path}...")
    inline_manifest(html_path, manifest)

    print(f"\nDone! Credits used: ~{total_chars // 2:,}")


if __name__ == "__main__":
    main()
