"""
Generate Azure TTS narration for Statistics AQA (statistics-aqa) article-format lessons.

Narrates ONLY the 9 article-format lessons across two units:
  - planning-designing-enquiry  (Unit 1, lessons 1-5)
  - interpreting-results-sec    (Unit 5, lessons 1-4)

Practice-format units (representing-data, numerical-measures,
probability-comparing-distributions) are intentionally skipped —
they have no content_html to narrate.

Voice assignment (CLAUDE.md convention):
  Odd lesson_number  → Ollie (en-GB-OllieMultilingualNeural)
  Even lesson_number → Ada   (en-GB-AdaMultilingualNeural)

R2 audio key pattern:
  statistics-aqa/{unit_slug}/narration_lesson-{NN}_{nid}.mp3

Usage:
    python scripts/_narrate_statistics-aqa.py
    python scripts/_narrate_statistics-aqa.py --dry-run
    python scripts/_narrate_statistics-aqa.py --unit planning-designing-enquiry
    python scripts/_narrate_statistics-aqa.py --lesson 3
"""

import argparse
import io
import os
import sys
import time

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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import (
    extract_narration_chunks,
    generate_audio_rest,
    get_mp3_duration,
    get_voice_for_lesson,
    AZURE_KEY,
)


# ── Constants ────────────────────────────────────────────────────────────

SUBJECT_SLUG = "statistics-aqa"

# Only the article-format units — practice units have no content_html
ARTICLE_UNITS = [
    "planning-designing-enquiry",   # Unit 1, 5 lessons
    "interpreting-results-sec",     # Unit 5, 4 lessons
]


# ── Core processing ──────────────────────────────────────────────────────

def process_lesson(sb, r2_client, unit_slug, unit_id, lesson_number, dry_run=False):
    """Fetch lesson HTML, generate TTS, upload to R2, update Supabase manifest.

    Returns (clips_generated, total_chars, elapsed_seconds).
    """
    voice_name, voice_label = get_voice_for_lesson(lesson_number)

    print(f"\n  {unit_slug} / Lesson {lesson_number:02d} ({voice_label})")
    print(f"  {'=' * 54}")

    lesson_start = time.time()

    # Fetch lesson from Supabase
    result = (
        sb.table("lessons")
        .select("id, lesson_number, title, content_html, exam_tip_html, conclusion_html")
        .eq("unit_id", unit_id)
        .eq("lesson_number", lesson_number)
        .single()
        .execute()
    )
    lesson = result.data
    lesson_id = lesson["id"]

    print(f"  Title: {lesson['title']}")
    print(f"  ID:    {lesson_id}")

    # Combine HTML parts
    combined_html = (
        (lesson.get("content_html") or "")
        + (lesson.get("exam_tip_html") or "")
        + (lesson.get("conclusion_html") or "")
    )

    if not combined_html.strip():
        print("  SKIP: no content_html (practice-format lesson?)")
        return 0, 0, 0.0

    # Extract narration chunks
    chunks = extract_narration_chunks(combined_html)
    if not chunks:
        print("  ERROR: no data-narration-id elements found in HTML")
        return 0, 0, 0.0

    print(f"  Found {len(chunks)} narration chunks")

    if dry_run:
        total_chars = sum(len(text) for _, text in chunks)
        print(f"  [DRY RUN] Would generate {len(chunks)} clips, ~{total_chars:,} chars")
        return 0, total_chars, 0.0

    # Generate audio, upload, build manifest
    manifest = []
    total_chars = 0
    generated_count = 0
    total_duration = 0.0

    for nid, text in chunks:
        r2_key = f"{SUBJECT_SLUG}/{unit_slug}/narration_lesson-{lesson_number:02d}_{nid}.mp3"
        public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"

        total_chars += len(text)
        display = (text[:70] + "...") if len(text) > 70 else text
        display = display.encode("ascii", errors="replace").decode("ascii")
        print(f"    {nid}: {display}")

        mp3_bytes = generate_audio_rest(text, voice_name)
        if mp3_bytes is None:
            print(f"    FAILED to generate audio for {nid}")
            continue

        duration = get_mp3_duration(mp3_bytes)
        total_duration += duration

        upload_bytes_to_r2(r2_client, AUDIO_BUCKET, r2_key, mp3_bytes, "audio/mpeg")

        manifest.append({"id": nid, "src": public_url, "duration": duration})
        generated_count += 1
        print(f"           -> {len(mp3_bytes)/1024:.0f} KB, {duration:.1f}s, uploaded")

    if not manifest:
        print("  ERROR: no audio clips generated")
        return 0, 0, 0.0

    # Update Supabase
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson_id).execute()

    elapsed = time.time() - lesson_start
    print(f"  Manifest updated ({len(manifest)} entries, {total_duration:.1f}s audio, {elapsed:.1f}s elapsed)")

    return generated_count, total_chars, elapsed


# ── Entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate TTS narration for Statistics AQA article lessons"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be processed without generating audio"
    )
    parser.add_argument(
        "--unit", choices=ARTICLE_UNITS, default=None,
        help="Process only this unit slug (default: both article units)"
    )
    parser.add_argument(
        "--lesson", type=int, default=None,
        help="Process only this lesson_number within the unit"
    )
    args = parser.parse_args()

    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY environment variable not set")
        sys.exit(1)

    print("Statistics AQA — TTS Narration Generator")
    print("=" * 55)
    print(f"Subject slug:  {SUBJECT_SLUG}")
    print(f"Article units: {ARTICLE_UNITS}")
    print(f"Azure region:  uksouth")
    print(f"Odd lessons  → Ollie (en-GB-OllieMultilingualNeural)")
    print(f"Even lessons → Ada   (en-GB-AdaMultilingualNeural)")
    if args.dry_run:
        print("Mode: DRY RUN")
    print()

    sb = get_client()

    # Resolve subject
    subjects = (
        sb.table("subjects")
        .select("id, slug")
        .eq("slug", SUBJECT_SLUG)
        .is_("school_id", "null")
        .execute()
    )
    if not subjects.data:
        print(f"ERROR: subject '{SUBJECT_SLUG}' (school_id NULL) not found in Supabase")
        sys.exit(1)
    subject_id = subjects.data[0]["id"]
    print(f"Subject ID: {subject_id}")

    # Resolve article units
    units_result = (
        sb.table("units")
        .select("id, slug, sort_order")
        .eq("subject_id", subject_id)
        .in_("slug", ARTICLE_UNITS)
        .execute()
    )
    unit_map = {u["slug"]: u["id"] for u in units_result.data}
    print(f"Units found: {list(unit_map.keys())}")

    missing_units = [s for s in ARTICLE_UNITS if s not in unit_map]
    if missing_units:
        print(f"ERROR: units not found in Supabase: {missing_units}")
        sys.exit(1)
    print()

    # Determine which units to process
    units_to_process = [args.unit] if args.unit else ARTICLE_UNITS

    # Collect all lessons to process
    work_items = []  # (unit_slug, unit_id, lesson_number)
    for unit_slug in units_to_process:
        unit_id = unit_map[unit_slug]
        query = (
            sb.table("lessons")
            .select("lesson_number")
            .eq("unit_id", unit_id)
            .order("lesson_number")
        )
        if args.lesson:
            query = query.eq("lesson_number", args.lesson)
        lessons = query.execute()
        for row in lessons.data:
            work_items.append((unit_slug, unit_id, row["lesson_number"]))

    print(f"Lessons to narrate: {len(work_items)}")
    for unit_slug, _, lesson_num in work_items:
        _, label = get_voice_for_lesson(lesson_num)
        print(f"  {unit_slug} / L{lesson_num:02d} ({label})")
    print()

    if not work_items:
        print("Nothing to do.")
        return

    r2_client = None if args.dry_run else get_r2_client()

    # Process
    total_start = time.time()
    total_clips = 0
    total_chars = 0
    results = []

    for unit_slug, unit_id, lesson_num in work_items:
        try:
            clips, chars, elapsed = process_lesson(
                sb, r2_client, unit_slug, unit_id, lesson_num, dry_run=args.dry_run
            )
            total_clips += clips
            total_chars += chars
            results.append((unit_slug, lesson_num, clips, chars, elapsed, None))
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append((unit_slug, lesson_num, 0, 0, 0.0, str(e)))

    total_elapsed = time.time() - total_start

    # Summary
    print(f"\n{'=' * 55}")
    print("SUMMARY")
    print(f"{'=' * 55}")
    print(f"{'Unit':<34} {'L':<5} {'Clips':<7} {'Chars':<10} {'Time'}")
    print(f"{'-' * 55}")
    for unit_slug, lesson_num, clips, chars, elapsed, err in results:
        status = f"ERROR: {err}" if err else f"{clips} clips, {elapsed:.1f}s"
        print(f"{unit_slug:<34} L{lesson_num:02d}   {clips:<7} {chars:<10,} {elapsed:.1f}s")
    print(f"{'-' * 55}")
    print(f"TOTAL: {total_clips} clips, {total_chars:,} chars, {total_elapsed:.1f}s elapsed")

    if total_chars > 0:
        cost = total_chars * 16 / 1_000_000
        print(f"Estimated Azure cost: ${cost:.2f} (at $16/1M chars)")

    print("\nDone.")


if __name__ == "__main__":
    main()
