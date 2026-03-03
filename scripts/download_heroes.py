"""
Subject-agnostic hero image downloader.

Queries pipeline_steps for lessons needing hero images, searches Wikimedia
Commons using hero_keywords, downloads + compresses, uploads to R2, and
updates Supabase lesson records.

Usage:
    python scripts/download_heroes.py --job-id <uuid>
    python scripts/download_heroes.py --job-id <uuid> --lessons 1,2,3
    python scripts/download_heroes.py --job-id <uuid> --dry-run
"""

import argparse
import io
import os
import sys
import tempfile
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
from lib.r2 import get_r2_client, upload_file_to_r2, IMAGES_BUCKET
from lib.wikimedia import (
    search_wikimedia,
    download_image,
    resize_and_compress,
    MIN_FILE_SIZE,
    API_DELAY,
)
from lib.pipeline import (
    get_pending_lessons,
    mark_asset_done,
    mark_asset_error,
    get_job_subject_slug,
    get_progress_summary,
)


def process_lesson(sb, r2_client, step, subject_slug, dry_run=False):
    """Process a single lesson: search Wikimedia, download, compress, upload, update DB.

    Returns True on success, False on failure.
    """
    lesson_id = step["lesson_id"]
    unit_slug = step["unit_slug"]
    lesson_number = step["lesson_number"]
    lesson_title = step["lesson_title"]
    label = f"{subject_slug}/{unit_slug}/lesson-{lesson_number:02d}"

    print(f"\n{'=' * 60}")
    print(f"  {label}: {lesson_title}")
    print(f"{'=' * 60}")

    # Get search keywords from pipeline_step or derive from title
    hero_keywords = step.get("hero_keywords") or []
    if not hero_keywords:
        # Derive from lesson title as fallback
        hero_keywords = [lesson_title]
        print(f"  No hero_keywords stored — using lesson title as search query")

    # Search Wikimedia with keywords (primary + fallbacks)
    chosen = None
    for i, query in enumerate(hero_keywords):
        if i > 0:
            print(f"  Trying fallback search: {query}")
            time.sleep(API_DELAY)
        else:
            print(f"  Searching: {query}")

        results = search_wikimedia(query)
        print(f"  Found {len(results)} landscape JPEG candidates")

        for r in results[:5]:
            print(f"    - {r['title'][:60]}  ({r['width']}x{r['height']}, {r['size']/1024:.0f}KB)")

        # Pick the best candidate (first landscape result with decent size)
        for r in results:
            if r["size"] >= MIN_FILE_SIZE:
                chosen = r
                break

        if chosen:
            break

    if not chosen:
        print(f"  WARNING: No suitable image found for {label}")
        return False

    print(f"  Selected: {chosen['title'][:70]}")

    if dry_run:
        print(f"  [DRY RUN] Would download, resize, upload to {label}-hero.jpg")
        return True

    # Download to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_path = os.path.join(tmpdir, "raw.jpg")
        final_path = os.path.join(tmpdir, f"lesson-{lesson_number:02d}-hero.jpg")

        # Use thumburl (pre-scaled to 1200px) if available, else original
        dl_url = chosen["url"] if chosen["url"] else chosen["original_url"]
        print(f"  Downloading from: {dl_url[:80]}...")
        raw_size = download_image(dl_url, raw_path)
        print(f"  Downloaded: {raw_size / 1024:.0f} KB")

        if raw_size < MIN_FILE_SIZE:
            print(f"  Too small ({raw_size/1024:.0f}KB), trying original URL...")
            dl_url = chosen["original_url"]
            raw_size = download_image(dl_url, raw_path)
            print(f"  Downloaded original: {raw_size / 1024:.0f} KB")

        if raw_size < MIN_FILE_SIZE:
            print(f"  WARNING: Image still too small ({raw_size/1024:.0f}KB), skipping")
            return False

        # Resize and compress
        final_size = resize_and_compress(raw_path, final_path)
        print(f"  Resized/compressed: {final_size / 1024:.0f} KB")

        if final_size < 10 * 1024:
            print(f"  WARNING: Compressed image too small ({final_size/1024:.0f}KB), skipping")
            return False

        # Upload to R2
        r2_key = f"{subject_slug}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
        print(f"  Uploading to R2: {r2_key}")
        r2_url = upload_file_to_r2(r2_client, IMAGES_BUCKET, final_path, r2_key, "image/jpeg")
        print(f"  R2 URL: {r2_url}")

        # Update Supabase lesson
        alt_text = lesson_title
        print(f"  Updating Supabase lesson {lesson_id[:8]}...")
        sb.table("lessons").update({
            "hero_image_url": r2_url,
            "hero_image_alt": alt_text,
        }).eq("id", lesson_id).execute()
        print(f"  Done!")

    return True


def main():
    parser = argparse.ArgumentParser(description="Download hero images for pipeline lessons")
    parser.add_argument("--job-id", required=True, help="Upload job UUID")
    parser.add_argument("--lessons", help="Comma-separated lesson numbers to process (default: all pending)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without downloading")
    args = parser.parse_args()

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
    pending = get_pending_lessons(sb, args.job_id, "hero_done", specific_lessons)
    if not pending:
        print("No lessons pending hero images. All done!")
        return

    print(f"\nFound {len(pending)} lessons needing hero images")
    print("=" * 60)

    # Create R2 client
    r2_client = get_r2_client()

    success = 0
    failed = 0

    for step in pending:
        try:
            ok = process_lesson(sb, r2_client, step, subject_slug, args.dry_run)
            if ok:
                success += 1
                if not args.dry_run:
                    mark_asset_done(sb, step["id"], "hero_done")
            else:
                failed += 1
                if not args.dry_run:
                    mark_asset_error(sb, step["id"], "No suitable Wikimedia image found")
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
            if not args.dry_run:
                mark_asset_error(sb, step["id"], str(e))

        # Rate-limit between lessons
        time.sleep(API_DELAY)

    total = success + failed
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Success: {success}/{total}")
    print(f"Failed:  {failed}/{total}")

    # Show overall progress
    if not args.dry_run:
        summary = get_progress_summary(sb, args.job_id)
        print(f"\nJob progress: {summary['heroes']}/{summary['total']} hero images done")

    print(f"\nDone!")


if __name__ == "__main__":
    main()
