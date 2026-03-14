"""
Subject-agnostic diagram generator with automated QA.

Queries pipeline_steps for lessons needing diagrams, reads the stored
diagram_prompt, calls Gemini to generate a pictorial isotype diagram,
then sends to Claude Sonnet for automated QA. Regenerates with guardrails
if QA fails (up to 3 attempts). Only uploads to R2 when QA passes.

Usage:
    python scripts/generate_diagrams.py --job-id <uuid>
    python scripts/generate_diagrams.py --job-id <uuid> --lessons 1,2,3
    python scripts/generate_diagrams.py --job-id <uuid> --dry-run
    python scripts/generate_diagrams.py --job-id <uuid> --skip-qa
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
from lib.claude_qa import qa_diagram


MAX_QA_ATTEMPTS = 3

GUARDRAIL_PREFIX = """CRITICAL RULES — follow these exactly:
1. DO NOT render any meta-instructions, hex colour codes, age references, or prompt text as visible text in the image. No "GCSE", "aged 15-16", "pictorial isotype", "educational", or colour hex codes should appear anywhere in the final image.
2. Every word of text in the image must be a REAL English word, correctly spelled. Double-check every label before finalising. No garbled, truncated, or nonsensical text.
3. Do NOT duplicate labels. Each text label should appear exactly once unless it genuinely labels different things.
4. If drawing a flow diagram, use the minimum number of arrows needed. Each arrow must point in a clear, logical direction.
5. Use a clean white or very light warm cream background. Landscape orientation, roughly 1800x1050 pixels.
6. Use clean, modern sans-serif typography. All text must be large enough to read easily.
7. No watermarks, no UI elements, no toolbars, no borders.

COLOUR SCHEME: Use {accent_color} as the primary accent colour. Do NOT render this hex code as visible text.

---

"""


def slugify(text):
    """Convert text to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')
    return text[:60]


def inject_diagram_into_html(content_html, diagram_url, diagram_alt, diagram_caption=None):
    """Insert a <figure class="diagram"> into the content HTML.

    Looks for a <!-- DIAGRAM --> placeholder in the HTML (placed by content
    generation to mark the most relevant location). Falls back to midpoint
    h2 if no placeholder exists.
    """
    figure_html = f'<figure class="diagram"><img src="{diagram_url}" alt="{diagram_alt}" loading="lazy">'
    if diagram_caption:
        figure_html += f'<figcaption>{diagram_caption}</figcaption>'
    figure_html += '</figure>'

    # Primary: replace <!-- DIAGRAM --> placeholder from content generation
    if '<!-- DIAGRAM -->' in content_html:
        return content_html.replace('<!-- DIAGRAM -->', figure_html, 1)

    # Fallback: h2 nearest to midpoint
    h2_matches = list(re.finditer(r'<h2[^>]*>', content_html))
    if len(h2_matches) >= 2:
        target_pos = len(content_html) // 2
        best = min(h2_matches, key=lambda m: abs(m.start() - target_pos))
        return content_html[:best.start()] + figure_html + '\n\n' + content_html[best.start():]

    # Last resort: before conclusion or at end
    conclusion_match = re.search(r'<div class="conclusion"', content_html)
    if conclusion_match:
        return content_html[:conclusion_match.start()] + figure_html + '\n\n' + content_html[conclusion_match.start():]

    return content_html + '\n\n' + figure_html


def process_lesson(sb, r2_client, step, subject_slug, dry_run=False, skip_qa=False):
    """Process a single lesson: generate diagram, QA it, upload when passing.

    Generates via Gemini, sends to Claude Sonnet for automated QA.
    If QA fails, regenerates with guardrails (up to MAX_QA_ATTEMPTS total).
    Only uploads to R2 and updates Supabase when QA passes.

    Returns True on success, False on failure.
    """
    lesson_id = step["lesson_id"]
    unit_slug = step["unit_slug"]
    lesson_number = step["lesson_number"]
    lesson_title = step["lesson_title"]
    diagram_prompt = step.get("diagram_prompt")
    label = f"{subject_slug}/{unit_slug}/L{lesson_number:02d}"

    # Get unit info for QA context
    subject_name = step.get("subject_name", subject_slug)
    unit_name = step.get("unit_name", unit_slug)
    accent_color = step.get("accent_color", "#666666")

    print(f"\n{'=' * 60}")
    print(f"  {label}: {lesson_title}")
    print(f"{'=' * 60}")

    if not diagram_prompt:
        print(f"  SKIP: No diagram_prompt stored for this lesson")
        return False

    print(f"  Prompt: {diagram_prompt[:100]}...")

    if dry_run:
        print(f"  [DRY RUN] Would call Gemini, QA with Claude, and upload")
        return True

    # Generate + QA loop
    image_bytes = None
    prompt_to_use = diagram_prompt

    for attempt in range(1, MAX_QA_ATTEMPTS + 1):
        # Call Gemini
        attempt_label = f"attempt {attempt}/{MAX_QA_ATTEMPTS}"
        print(f"  [{attempt_label}] Calling Gemini...")
        start = time.time()
        image_bytes, gemini_text = call_gemini_image(prompt_to_use)
        elapsed = time.time() - start

        if gemini_text:
            print(f"  Gemini note: {gemini_text[:150]}")

        if not image_bytes:
            print(f"  [{attempt_label}] FAILED: No image returned ({elapsed:.1f}s)")
            time.sleep(2)
            continue

        print(f"  [{attempt_label}] Generated: {len(image_bytes)/1024:.0f} KB in {elapsed:.1f}s")

        # QA check
        if skip_qa:
            print(f"  [QA skipped]")
            break

        print(f"  [{attempt_label}] QA checking with Claude...")
        try:
            passed, issues = qa_diagram(
                image_bytes, lesson_title, subject_name, unit_name, accent_color
            )
        except Exception as e:
            print(f"  [{attempt_label}] QA error (proceeding anyway): {e}")
            break

        if passed:
            print(f"  [{attempt_label}] QA PASSED")
            break
        else:
            print(f"  [{attempt_label}] QA FAILED:")
            for issue in issues:
                print(f"    - {issue}")

            if attempt < MAX_QA_ATTEMPTS:
                # Add guardrails for next attempt
                prompt_to_use = GUARDRAIL_PREFIX.format(accent_color=accent_color) + diagram_prompt
                print(f"  Regenerating with guardrails...")
                time.sleep(2)
            else:
                print(f"  Max attempts reached — using last generated image")

        time.sleep(2)

    if not image_bytes:
        print(f"  FAILED: No image after {MAX_QA_ATTEMPTS} attempts")
        return False

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
    }
    diagrams.append(diagram_entry)

    # Inject figure into content HTML (no caption on diagrams — alt text is sufficient)
    content_html = lesson.data.get("content_html") or ""
    if content_html and r2_url not in content_html:
        content_html = inject_diagram_into_html(
            content_html, r2_url, diagram_entry["alt"]
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
    parser.add_argument("--skip-qa", action="store_true", help="Skip Claude QA step (generate and upload directly)")
    args = parser.parse_args()

    sb = get_client()

    # Resolve subject slug
    subject_slug = get_job_subject_slug(sb, args.job_id)
    print(f"Subject: {subject_slug}")

    if not args.skip_qa:
        print(f"QA: enabled (Claude Sonnet, up to {MAX_QA_ATTEMPTS} attempts per diagram)")
    else:
        print(f"QA: disabled (--skip-qa)")

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

    # Fetch subject + unit metadata for QA context
    job = sb.table("upload_jobs").select("subject_id").eq("id", args.job_id).single().execute()
    subject_id = job.data["subject_id"] if job.data else None
    subject_name = subject_slug
    unit_map = {}
    if subject_id:
        subject_row = sb.table("subjects").select("name").eq("id", subject_id).single().execute()
        if subject_row and subject_row.data:
            subject_name = subject_row.data["name"]
        units = sb.table("units").select("name, slug, accent").eq("subject_id", subject_id).execute()
        unit_map = {u["slug"]: u for u in (units.data or [])}

    # Enrich each step with subject/unit metadata for QA
    for step in pending:
        unit = unit_map.get(step.get("unit_slug"), {})
        step["subject_name"] = subject_name
        step["unit_name"] = unit.get("name", step.get("unit_slug", ""))
        step["accent_color"] = unit.get("accent", "#666666")

    print(f"\nFound {len(pending)} lessons needing diagrams")
    print("=" * 60)

    # Create R2 client (only needed if not dry-run, but check env vars early)
    r2_client = get_r2_client() if not args.dry_run else None

    success = 0
    failed = 0

    for step in pending:
        try:
            ok = process_lesson(sb, r2_client, step, subject_slug, args.dry_run, args.skip_qa)
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

        # Brief pause between lessons
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
