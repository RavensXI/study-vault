"""
Subject-agnostic diagram generator.

Queries pipeline_steps for lessons needing diagrams, reads the stored
diagram_prompt, calls Gemini to generate a pictorial isotype diagram,
uploads to R2, and updates the lesson record in Supabase.

Usage:
    python scripts/generate_diagrams.py --job-id <uuid>
    python scripts/generate_diagrams.py --job-id <uuid> --lessons 1,2,3
    python scripts/generate_diagrams.py --job-id <uuid> --dry-run
"""

import argparse
import io
import os
import re
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
from lib.r2 import get_r2_client, upload_bytes_to_r2, IMAGES_BUCKET, IMAGES_PUBLIC_URL
from lib.gemini import call_gemini_image
from lib.pipeline import (
    get_pending_lessons,
    mark_asset_done,
    mark_asset_error,
    get_job_subject_slug,
    get_progress_summary,
)


def slugify(text):
    """Convert text to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')
    return text[:60]


def inject_diagram_into_html(content_html, diagram_url, diagram_alt, diagram_caption=None):
    """Insert a <figure class="diagram"> into the content HTML.

    Places the diagram after the first few paragraphs (15+ lines from top),
    or at the end if content is short.
    """
    figure_html = f'<figure class="diagram"><img src="{diagram_url}" alt="{diagram_alt}" loading="lazy">'
    if diagram_caption:
        figure_html += f'<figcaption>{diagram_caption}</figcaption>'
    figure_html += '</figure>'

    # Find a good insertion point: after 3rd paragraph or section heading
    paragraphs = list(re.finditer(r'</p>', content_html))
    if len(paragraphs) >= 3:
        insert_pos = paragraphs[2].end()
        return content_html[:insert_pos] + '\n\n' + figure_html + '\n\n' + content_html[insert_pos:]

    # Fallback: insert before conclusion or at end
    conclusion_match = re.search(r'<div class="conclusion"', content_html)
    if conclusion_match:
        return content_html[:conclusion_match.start()] + figure_html + '\n\n' + content_html[conclusion_match.start():]

    return content_html + '\n\n' + figure_html


def process_lesson(sb, r2_client, step, subject_slug, dry_run=False):
    """Process a single lesson: read prompt, call Gemini, upload, update DB.

    Returns True on success, False on failure.
    """
    lesson_id = step["lesson_id"]
    unit_slug = step["unit_slug"]
    lesson_number = step["lesson_number"]
    lesson_title = step["lesson_title"]
    diagram_prompt = step.get("diagram_prompt")
    label = f"{subject_slug}/{unit_slug}/L{lesson_number:02d}"

    print(f"\n{'=' * 60}")
    print(f"  {label}: {lesson_title}")
    print(f"{'=' * 60}")

    if not diagram_prompt:
        print(f"  SKIP: No diagram_prompt stored for this lesson")
        return False

    print(f"  Prompt: {diagram_prompt[:100]}...")

    if dry_run:
        print(f"  [DRY RUN] Would call Gemini and upload diagram")
        return True

    # Call Gemini
    print(f"  Calling Gemini...")
    start = time.time()
    image_bytes, gemini_text = call_gemini_image(diagram_prompt)
    elapsed = time.time() - start

    if gemini_text:
        print(f"  Gemini note: {gemini_text[:200]}")

    if not image_bytes:
        print(f"  FAILED: No image returned from Gemini ({elapsed:.1f}s)")
        return False

    print(f"  Generated: {len(image_bytes)/1024:.0f} KB in {elapsed:.1f}s")

    # Upload to R2
    title_slug = slugify(lesson_title)
    r2_key = f"{subject_slug}/{unit_slug}/diagram_{title_slug}.jpg"
    print(f"  Uploading to R2: {r2_key}")
    r2_url = upload_bytes_to_r2(r2_client, IMAGES_BUCKET, r2_key, image_bytes, "image/jpeg")
    print(f"  R2 URL: {r2_url}")

    # Update lesson: add to diagrams array and inject into content_html
    lesson = sb.table("lessons").select("diagrams, content_html").eq("id", lesson_id).single().execute()
    if not lesson.data:
        print(f"  ERROR: Lesson {lesson_id} not found")
        return False

    diagrams = lesson.data.get("diagrams") or []
    diagram_entry = {
        "url": r2_url,
        "alt": f"Diagram: {lesson_title}",
        "caption": lesson_title,
    }
    diagrams.append(diagram_entry)

    # Inject figure into content HTML
    content_html = lesson.data.get("content_html") or ""
    if content_html and r2_url not in content_html:
        content_html = inject_diagram_into_html(
            content_html, r2_url, diagram_entry["alt"], diagram_entry["caption"]
        )

    sb.table("lessons").update({
        "diagrams": diagrams,
        "content_html": content_html,
    }).eq("id", lesson_id).execute()

    print(f"  Updated lesson (diagrams: {len(diagrams)}, HTML injected)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate diagrams for pipeline lessons")
    parser.add_argument("--job-id", required=True, help="Upload job UUID")
    parser.add_argument("--lessons", help="Comma-separated lesson numbers to process (default: all pending)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without generating")
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
    pending = get_pending_lessons(sb, args.job_id, "diagrams_done", specific_lessons)
    if not pending:
        print("No lessons pending diagrams. All done!")
        return

    print(f"\nFound {len(pending)} lessons needing diagrams")
    print("=" * 60)

    # Create R2 client (only needed if not dry-run, but check env vars early)
    r2_client = get_r2_client() if not args.dry_run else None

    success = 0
    failed = 0

    for step in pending:
        try:
            ok = process_lesson(sb, r2_client, step, subject_slug, args.dry_run)
            if ok:
                success += 1
                if not args.dry_run:
                    mark_asset_done(sb, step["id"], "diagrams_done")
            else:
                failed += 1
                if not args.dry_run and step.get("diagram_prompt"):
                    mark_asset_error(sb, step["id"], "Gemini returned no image")
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
            if not args.dry_run:
                mark_asset_error(sb, step["id"], str(e))

        # Brief pause between Gemini calls
        time.sleep(2)

    total = success + failed
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Success: {success}/{total}")
    print(f"Failed:  {failed}/{total}")

    # Show overall progress
    if not args.dry_run:
        summary = get_progress_summary(sb, args.job_id)
        print(f"\nJob progress: {summary['diagrams']}/{summary['total']} diagrams done")

    print(f"\nDone!")


if __name__ == "__main__":
    main()
