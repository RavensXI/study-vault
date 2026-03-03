"""
Subject-agnostic TTS narration generator.

Queries pipeline_steps for lessons needing narration, generates MP3s via
Azure Speech, uploads to R2, and updates Supabase manifests.

Usage:
    python scripts/generate_narration.py --job-id <uuid>
    python scripts/generate_narration.py --job-id <uuid> --lessons 1,2,3
    python scripts/generate_narration.py --job-id <uuid> --dry-run
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

# Add scripts/ to path for lib imports
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
from lib.pipeline import (
    get_pending_lessons,
    mark_asset_done,
    mark_asset_error,
    get_job_subject_slug,
    get_progress_summary,
)


def process_lesson(sb, r2_client, step, subject_slug):
    """Process a single lesson: fetch HTML, extract chunks, generate TTS, upload, update manifest.

    Args:
        sb: Supabase client.
        r2_client: R2 S3 client.
        step: pipeline_step dict (with joined lessons data).
        subject_slug: Subject slug for R2 key paths.

    Returns:
        (clips_generated, total_chars, elapsed_seconds)
    """
    lesson = step.get("lessons") or {}
    lesson_id = step["lesson_id"]
    unit_slug = step["unit_slug"]
    lesson_number = step["lesson_number"]

    voice_name, voice_label = get_voice_for_lesson(lesson_number)

    print(f"\n  {unit_slug} / Lesson {lesson_number:02d} ({voice_label})")
    print(f"  {'=' * 50}")

    lesson_start = time.time()

    # Combine HTML parts for parsing
    combined_html = ""
    for field in ("content_html", "exam_tip_html", "conclusion_html"):
        html_part = lesson.get(field)
        if html_part:
            combined_html += html_part

    if not combined_html:
        # Fallback: fetch directly from lessons table
        direct = sb.table("lessons").select("content_html, exam_tip_html, conclusion_html").eq("id", lesson_id).single().execute()
        if direct.data:
            for field in ("content_html", "exam_tip_html", "conclusion_html"):
                html_part = direct.data.get(field)
                if html_part:
                    combined_html += html_part

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
        r2_key = f"{subject_slug}/{unit_slug}/narration_lesson-{lesson_number:02d}_{narration_id}.mp3"
        public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"

        total_chars += len(text)

        # Display truncated text
        display = text[:70] + "..." if len(text) > 70 else text
        display = display.encode("ascii", errors="replace").decode("ascii")
        print(f"    {narration_id}: {display}")

        # Generate MP3
        mp3_bytes = generate_audio_rest(text, voice_name)
        if mp3_bytes is None:
            print(f"    FAILED to generate audio for {narration_id}")
            continue

        # Calculate duration
        duration = get_mp3_duration(mp3_bytes)
        total_duration += duration

        # Upload to R2
        upload_bytes_to_r2(r2_client, AUDIO_BUCKET, r2_key, mp3_bytes, "audio/mpeg")

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
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson_id).execute()

    elapsed = time.time() - lesson_start
    print(f"  Manifest updated ({len(manifest)} entries)")
    print(f"  Total: {generated_count} clips, {total_chars:,} chars, {total_duration:.1f}s audio, {elapsed:.1f}s elapsed")

    return generated_count, total_chars, elapsed


def main():
    parser = argparse.ArgumentParser(description="Generate TTS narration for pipeline lessons")
    parser.add_argument("--job-id", required=True, help="Upload job UUID")
    parser.add_argument("--lessons", help="Comma-separated lesson numbers to process (default: all pending)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without generating")
    args = parser.parse_args()

    # Validate Azure key
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY environment variable not set")
        sys.exit(1)

    sb = get_client()

    # Resolve subject slug
    subject_slug = get_job_subject_slug(sb, args.job_id)
    print(f"Subject: {subject_slug}")

    # Parse lesson filter
    specific_lessons = None
    if args.lessons:
        specific_lessons = [int(x.strip()) for x in args.lessons.split(",")]
        print(f"Filtering to lessons: {specific_lessons}")

    # Get pending lessons
    pending = get_pending_lessons(sb, args.job_id, "narration_done", specific_lessons)
    if not pending:
        print("No lessons pending narration. All done!")
        return

    print(f"\nFound {len(pending)} lessons needing narration")
    print("=" * 55)

    if args.dry_run:
        for step in pending:
            print(f"  [DRY RUN] L{step['lesson_number']:02d} ({step['unit_slug']}): {step['lesson_title']}")
        return

    # Create R2 client
    r2_client = get_r2_client()

    # Process each lesson
    total_start = time.time()
    total_clips = 0
    total_chars = 0
    lesson_results = []

    for step in pending:
        try:
            clips, chars, elapsed = process_lesson(sb, r2_client, step, subject_slug)
            total_clips += clips
            total_chars += chars
            lesson_results.append((step["unit_slug"], step["lesson_number"], clips, chars, elapsed))

            if clips > 0:
                mark_asset_done(sb, step["id"], "narration_done")
            else:
                mark_asset_error(sb, step["id"], "No audio clips generated")
        except Exception as e:
            print(f"  ERROR: {e}")
            mark_asset_error(sb, step["id"], str(e))
            lesson_results.append((step["unit_slug"], step["lesson_number"], 0, 0, 0.0))

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

    # Show overall progress
    summary = get_progress_summary(sb, args.job_id)
    print(f"\nJob progress: {summary['narration']}/{summary['total']} narration done")
    print(f"Done!")


if __name__ == "__main__":
    main()
