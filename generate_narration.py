"""Generate per-paragraph narration audio for a StudyVault lesson.

Usage:
    python generate_narration.py conflict-tension/lesson-01.html

Reads every element with data-narration-id from the lesson HTML,
generates a WAV clip for each via Qwen3-TTS voice cloning, and
writes the updated manifest back into the HTML.

Output files go into the lesson's directory as narration_lesson-NN_nX.wav.
"""

import sys
import os
import re
import html
import time
import threading

# Force UTF-8 output on Windows (avoids cp1252 crashes when logging to file)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VOICEBOX_DIR = os.path.join(SCRIPT_DIR, "voicebox-test")
REF_AUDIO = os.path.join(VOICEBOX_DIR, "new test clone.m4a")
REF_AUDIO_WAV = os.path.join(VOICEBOX_DIR, "voice_sample_30s.wav")  # 30s clip — best accent quality on CPU

# Transcript of the 30s reference clip (corrected from Whisper output)
REF_TEXT = ("The Treaty of Versailles was shaped by three leaders with very different goals. "
            "Understanding their clashing aims is key to explaining why the treaty ended up the way it did. "
            "The Big Three were David Lloyd George of Britain, Georges Clemenceau of France, "
            "and Woodrow Wilson of the USA. Germany was not invited. Although 32 nations attended "
            "the Paris Peace Conference from January 1919, and Italy made it a Big Four, "
            "Italy was virtually ignored, so in reality it was")

# Labels to skip — these are visual-only and shouldn't be narrated
SKIP_LABELS = {"Key Fact", "Exam Tip"}

# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def strip_html(s):
    """Remove HTML tags, decode entities, normalise whitespace."""
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    # Normalise whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalise_for_speech(s):
    """Clean up text for more natural TTS output."""
    s = s.replace('\u2014', ' \u2014 ')   # em dash
    s = s.replace('\u2013', ' to ')        # en dash → "to"
    s = s.replace('&', ' and ')
    s = s.replace('vs.', 'versus')
    # Rate slashes like "km/h" → "per"
    s = re.sub(r'(\d)\s*/\s*([a-zA-Z])', r'\1 per \2', s)
    # Collapse multiple spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def find_inner_html(content, start_pos, tag):
    """Find the inner HTML of an element starting at start_pos (the '<' of the opening tag).

    Uses a nesting counter to handle nested tags of the same type.
    Returns (inner_html, end_pos) or (None, -1) if not found.
    """
    # Find end of opening tag
    gt_pos = content.index('>', start_pos)
    inner_start = gt_pos + 1

    # Count nesting to find matching close tag
    depth = 1
    pos = inner_start
    open_re = re.compile(r'<' + tag + r'[\s>/]')
    close_re = re.compile(r'</' + tag + r'>')

    while depth > 0 and pos < len(content):
        next_open = open_re.search(content, pos)
        next_close = close_re.search(content, pos)

        if next_close is None:
            break

        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            if depth == 0:
                return content[inner_start:next_close.start()], next_close.end()
            pos = next_close.end()

    return None, -1


def extract_chunks(html_path):
    """Extract narration chunks from lesson HTML.

    Returns list of { id: "n1", text: "..." } in document order.

    For container elements (key-fact, exam-tip, conclusion), excludes:
    - Visual labels (.key-fact-label, .exam-tip-label)
    - Text belonging to child elements with their own data-narration-id
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = []

    # Find every element with data-narration-id
    for m in re.finditer(r'<(\w+)\s([^>]*data-narration-id="(n\d+)"[^>]*)>', content):
        tag = m.group(1)
        nid = m.group(3)
        start_pos = m.start()

        inner, _ = find_inner_html(content, start_pos, tag)
        if inner is None:
            continue

        # Remove child elements that have their own data-narration-id
        cleaned = inner
        for child_m in re.finditer(
            r'<(\w+)\s[^>]*data-narration-id="n\d+"[^>]*>',
            inner
        ):
            child_tag = child_m.group(1)
            child_inner, child_end = find_inner_html(inner, child_m.start(), child_tag)
            if child_inner is not None:
                # Remove the entire child element from cleaned
                full_child = inner[child_m.start():child_end]
                cleaned = cleaned.replace(full_child, '', 1)

        # Remove label divs (key-fact-label, exam-tip-label)
        cleaned = re.sub(
            r'<div\s+class="(?:key-fact|exam-tip)-label"[^>]*>.*?</div>',
            '', cleaned, flags=re.DOTALL
        )

        text = strip_html(cleaned)

        # Skip empty chunks
        if not text:
            continue

        text = normalise_for_speech(text)
        if text:
            chunks.append({"id": nid, "text": text})

    return chunks


# ---------------------------------------------------------------------------
# Audio generation (Qwen3-TTS)
# ---------------------------------------------------------------------------

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
CHUNK_TIMEOUT = 600  # 10 minutes max per chunk (CPU generation is slow)


def load_model():
    """Load Qwen3-TTS model."""
    import torch
    from qwen_tts import Qwen3TTSModel

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Loading Qwen3-TTS on {device}...")

    kwargs = {}
    if device != "cpu":
        kwargs["device_map"] = device
    else:
        kwargs["device_map"] = "cpu"

    model = Qwen3TTSModel.from_pretrained(MODEL_ID, **kwargs)
    print(f"Model loaded on {device}")
    return model


def create_voice_prompt(model):
    """Build a reusable voice clone prompt from the reference audio (ICL mode for accent)."""
    print(f"Building voice clone prompt from {REF_AUDIO_WAV}...")
    prompts = model.create_voice_clone_prompt(
        ref_audio=REF_AUDIO_WAV,
        ref_text=REF_TEXT,
        x_vector_only_mode=False
    )
    print("Voice clone prompt ready.")
    return prompts


def generate_clip(model, text, voice_prompt, output_path):
    """Generate a single narration clip. Returns duration in seconds, or None on timeout."""
    import soundfile as sf
    import numpy as np

    result = [None]
    error = [None]

    def _run():
        try:
            wavs, sr = model.generate_voice_clone(
                text=text,
                language="english",
                voice_clone_prompt=voice_prompt,
            )
            audio = wavs[0]  # single text input → single output
            sf.write(output_path, audio, sr)
            duration = len(audio) / sr
            result[0] = round(duration, 2)
        except Exception as e:
            error[0] = e

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout=CHUNK_TIMEOUT)

    if t.is_alive():
        print(f"  TIMEOUT after {CHUNK_TIMEOUT}s — skipping this chunk")
        if os.path.exists(output_path):
            os.remove(output_path)
        return None

    if error[0]:
        print(f"  ERROR: {error[0]}")
        return None

    return result[0]


# ---------------------------------------------------------------------------
# HTML manifest update
# ---------------------------------------------------------------------------

def update_manifest(html_path, manifest_entries):
    """Write the new narrationManifest into the lesson HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build JS manifest array
    items = []
    for entry in manifest_entries:
        items.append(
            '      { id: "%s", src: "%s", duration: %s }'
            % (entry["id"], entry["src"], entry["duration"])
        )
    manifest_js = "[\n" + ",\n".join(items) + "\n    ]"

    # Replace the existing narrationManifest line
    content = re.sub(
        r'window\.narrationManifest\s*=\s*\[.*?\];',
        'window.narrationManifest = ' + manifest_js + ';',
        content,
        flags=re.DOTALL
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated manifest in {html_path} ({len(manifest_entries)} clips)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_lesson(html_path, rel_path, model, voice_prompt):
    """Generate narration for a single lesson. Returns (success_count, skip_count, fail_count)."""
    import soundfile as sf

    lesson_dir = os.path.dirname(html_path)

    # Derive lesson prefix from filename: "lesson-02.html" → "lesson-02"
    lesson_prefix = os.path.splitext(os.path.basename(html_path))[0]

    chunks = extract_chunks(html_path)
    print(f"Found {len(chunks)} narration chunks in {rel_path}")
    for c in chunks:
        words = len(c["text"].split())
        print(f"  {c['id']}: {words} words — {c['text'][:60]}...")

    total_words = sum(len(c["text"].split()) for c in chunks)
    print(f"\nTotal: {total_words} words")
    print()

    manifest = []
    successes = skips = fails = 0
    total_start = time.time()

    for i, chunk in enumerate(chunks):
        clip_filename = f"narration_{lesson_prefix}_{chunk['id']}.wav"
        clip_path = os.path.join(lesson_dir, clip_filename)

        # Skip if already generated
        if os.path.exists(clip_path):
            data, sr = sf.read(clip_path)
            duration = round(len(data) / sr, 2)
            print(f"[{i+1}/{len(chunks)}] {chunk['id']}: SKIPPED (exists, {duration}s)")
            manifest.append({"id": chunk["id"], "src": clip_filename, "duration": duration})
            skips += 1
            continue

        print(f"[{i+1}/{len(chunks)}] {chunk['id']}: Generating ({len(chunk['text'].split())} words)...")
        clip_start = time.time()

        duration = generate_clip(model, chunk["text"], voice_prompt, clip_path)

        elapsed = time.time() - clip_start

        if duration is None:
            print(f"  FAILED after {elapsed:.1f}s — chunk skipped")
            fails += 1
            continue

        print(f"  Done in {elapsed:.1f}s — clip duration: {duration}s")
        manifest.append({"id": chunk["id"], "src": clip_filename, "duration": duration})
        successes += 1

    total_elapsed = time.time() - total_start
    total_audio = sum(m["duration"] for m in manifest)
    print(f"\nLesson complete in {total_elapsed/60:.1f} minutes")
    print(f"Total audio duration: {total_audio:.1f}s ({total_audio/60:.1f} min)")
    print(f"Generated: {successes}  Skipped: {skips}  Failed: {fails}")

    # Write manifest back into HTML (only includes successful + skipped clips)
    update_manifest(html_path, manifest)
    return successes, skips, fails


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_narration.py <lesson.html> [lesson2.html ...]")
        print("Example: python generate_narration.py conflict-tension/lesson-01.html")
        print("Batch:   python generate_narration.py conflict-tension/lesson-*.html")
        sys.exit(1)

    # Resolve all lesson paths
    lessons = []
    for arg in sys.argv[1:]:
        path = os.path.join(SCRIPT_DIR, arg)
        if os.path.exists(path):
            lessons.append((path, arg))
        else:
            print(f"WARNING: File not found, skipping: {arg}")

    if not lessons:
        print("ERROR: No valid lesson files found.")
        sys.exit(1)

    print(f"{'='*60}")
    print(f"BATCH RUN: {len(lessons)} lesson(s)")
    print(f"{'='*60}\n")

    # Load model and build voice prompt once for all lessons
    model = load_model()
    voice_prompt = create_voice_prompt(model)
    print("Starting generation...\n")

    batch_start = time.time()
    results = []

    for idx, (html_path, rel_path) in enumerate(lessons):
        print(f"\n{'='*60}")
        print(f"LESSON {idx+1}/{len(lessons)}: {rel_path}")
        print(f"{'='*60}\n")

        successes, skips, fails = process_lesson(html_path, rel_path, model, voice_prompt)
        results.append((rel_path, successes, skips, fails))

    # Final summary
    batch_elapsed = time.time() - batch_start
    print(f"\n{'='*60}")
    print(f"BATCH COMPLETE — {len(lessons)} lessons in {batch_elapsed/60:.1f} minutes")
    print(f"{'='*60}")
    for rel_path, s, sk, f in results:
        status = "OK" if f == 0 else f"WARN ({f} failed)"
        print(f"  {rel_path}: {s} generated, {sk} skipped — {status}")
    total_fails = sum(r[3] for r in results)
    if total_fails:
        print(f"\n{total_fails} chunk(s) failed (timeout/error) — re-run those lessons to retry.")
    print()


if __name__ == "__main__":
    main()
