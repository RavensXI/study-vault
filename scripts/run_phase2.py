"""
Phase 2 Polling Script — Enrichment of newly-published lessons.

Polls Supabase for lessons in `publishing` status and generates their
assets (diagrams, narration) via the existing pipeline scripts.

Usage:
    python scripts/run_phase2.py              # Poll mode (60s interval)
    python scripts/run_phase2.py --once       # Single pass, exit
    python scripts/run_phase2.py --interval 30  # Custom interval
    python scripts/run_phase2.py --dry-run    # Show what would be processed
"""

import argparse
import io
import os
import subprocess
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone

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
from lib.pipeline import get_progress_summary


def log(msg):
    """Print a timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def fetch_publishing_lessons(sb):
    """Fetch all lessons with status='publishing', joined with unit and subject info.

    Returns a list of dicts with lesson, unit, and subject data.
    """
    result = (
        sb.table("lessons")
        .select("id, lesson_number, title, slug, content_html, unit_id, units(id, slug, name, accent, subject_id, subjects(id, slug, name, school_id))")
        .eq("status", "publishing")
        .order("lesson_number")
        .execute()
    )
    return result.data or []


def group_by_subject(lessons):
    """Group lesson rows by (subject_slug, school_id).

    Returns a dict mapping (subject_slug, school_id) -> list of lesson dicts.
    Each lesson dict is enriched with flattened subject/unit fields.
    """
    groups = defaultdict(list)

    for lesson in lessons:
        unit = lesson.get("units") or {}
        subject = unit.get("subjects") or {}

        subject_slug = subject.get("slug", "unknown")
        school_id = subject.get("school_id")
        subject_name = subject.get("name", subject_slug)
        unit_slug = unit.get("slug", "unknown")
        unit_name = unit.get("name", unit_slug)
        accent = unit.get("accent", "#666666")

        enriched = {
            "lesson_id": lesson["id"],
            "lesson_number": lesson["lesson_number"],
            "lesson_title": lesson["title"],
            "lesson_slug": lesson.get("slug"),
            "content_html": lesson.get("content_html", ""),
            "unit_id": lesson["unit_id"],
            "unit_slug": unit_slug,
            "unit_name": unit_name,
            "accent": accent,
            "subject_id": subject.get("id"),
            "subject_slug": subject_slug,
            "subject_name": subject_name,
            "school_id": school_id,
        }
        groups[(subject_slug, school_id)].append(enriched)

    return groups


def find_existing_diagram_prompt(sb, lesson_id):
    """Check if a previous pipeline_steps row has a diagram_prompt for this lesson.

    Returns the prompt string or None.
    """
    result = (
        sb.table("pipeline_steps")
        .select("diagram_prompt")
        .eq("lesson_id", lesson_id)
        .not_.is_("diagram_prompt", "null")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if result.data and result.data[0].get("diagram_prompt"):
        return result.data[0]["diagram_prompt"]
    return None


def generate_default_diagram_prompt(title, accent):
    """Generate a basic diagram prompt from the lesson title and accent colour."""
    return (
        f"Create a diagram illustrating the key concept of '{title}'. "
        f"Use {accent} as the primary colour. "
        f"Style: pictorial isotype, clean, educational, white background."
    )


def create_synthetic_job(sb, subject_slug, school_id):
    """Create a synthetic upload_jobs row for the asset scripts to use.

    Returns the job UUID string.
    """
    job_id = str(uuid.uuid4())

    job_data = {
        "id": job_id,
        "subject_slug": subject_slug,
        "status": "enriching",
        "current_phase": "enriching",
        "filename": f"phase2-auto-{subject_slug}",
    }
    if school_id:
        job_data["school_id"] = school_id

    sb.table("upload_jobs").insert(job_data).execute()
    return job_id


def create_pipeline_steps(sb, job_id, lessons, subject_slug):
    """Create pipeline_steps rows for each lesson in the group.

    Args:
        sb: Supabase client.
        job_id: Synthetic job UUID.
        lessons: List of enriched lesson dicts.
        subject_slug: Subject slug string.

    Returns:
        Number of steps created.
    """
    created = 0

    for lesson in lessons:
        lesson_id = lesson["lesson_id"]

        # Check for existing diagram prompt from previous pipeline runs
        diagram_prompt = find_existing_diagram_prompt(sb, lesson_id)
        if not diagram_prompt:
            diagram_prompt = generate_default_diagram_prompt(
                lesson["lesson_title"], lesson["accent"]
            )

        step_data = {
            "job_id": job_id,
            "lesson_id": lesson_id,
            "unit_slug": lesson["unit_slug"],
            "lesson_number": lesson["lesson_number"],
            "lesson_title": lesson["lesson_title"],
            "subject_slug": subject_slug,
            "content_done": True,
            "hero_done": True,
            "questions_done": True,
            "glossary_done": True,
            "diagrams_done": False,
            "narration_done": False,
            "media_done": False,
            "diagram_prompt": diagram_prompt,
            "diagram_style": "gemini_only",
            "hero_keywords": [],
        }

        sb.table("pipeline_steps").upsert(
            step_data, on_conflict="job_id,unit_slug,lesson_number"
        ).execute()
        created += 1

    return created


def mark_enrichment_started(sb, lesson_ids):
    """Set enrichment_started_at on all lessons being processed."""
    now = datetime.now(timezone.utc).isoformat()
    for lid in lesson_ids:
        sb.table("lessons").update({
            "enrichment_started_at": now,
        }).eq("id", lid).execute()


def run_asset_scripts(job_id, dry_run=False):
    """Run diagram and narration generation scripts for a job.

    Returns (diagrams_ok, narration_ok) booleans.
    """
    python = sys.executable

    if dry_run:
        log(f"  [DRY RUN] Would run: generate_diagrams.py --job-id {job_id}")
        log(f"  [DRY RUN] Would run: generate_narration.py --job-id {job_id}")
        return True, True

    # Run diagrams and narration in parallel
    log("  Starting diagram generation...")
    p_diag = subprocess.Popen(
        [python, os.path.join(SCRIPT_DIR, "generate_diagrams.py"), "--job-id", job_id, "--skip-qa"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    log("  Starting narration generation...")
    p_narr = subprocess.Popen(
        [python, os.path.join(SCRIPT_DIR, "generate_narration.py"), "--job-id", job_id],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    # Wait for both
    diag_rc = p_diag.wait()
    narr_rc = p_narr.wait()

    diag_ok = diag_rc == 0
    narr_ok = narr_rc == 0

    log(f"  Diagrams: {'OK' if diag_ok else f'FAILED (exit {diag_rc})'}")
    log(f"  Narration: {'OK' if narr_ok else f'FAILED (exit {narr_rc})'}")

    return diag_ok, narr_ok


def check_and_finalise(sb, job_id, lessons, subject_slug, dry_run=False):
    """Check pipeline_steps completion and update lesson statuses.

    If all diagrams_done AND narration_done: set status='awaiting_qa'.
    If any failed: set enrichment_error on affected lessons, leave as 'publishing'.

    Returns (completed_count, error_count).
    """
    summary = get_progress_summary(sb, job_id)
    total = summary["total"]
    all_diagrams = summary["diagrams"] >= total
    all_narration = summary["narration"] >= total

    lesson_ids = [l["lesson_id"] for l in lessons]
    now = datetime.now(timezone.utc).isoformat()

    if all_diagrams and all_narration:
        if dry_run:
            log(f"  [DRY RUN] Would set {total} lessons to awaiting_qa")
            return total, 0

        for lid in lesson_ids:
            sb.table("lessons").update({
                "status": "awaiting_qa",
                "enrichment_completed_at": now,
                "enrichment_error": None,
            }).eq("id", lid).execute()

        log(f"  Phase 2 complete for {subject_slug}: {total} lessons ready for QA")
        return total, 0
    else:
        # Check per-lesson failures
        steps = (
            sb.table("pipeline_steps")
            .select("lesson_id, diagrams_done, narration_done, last_error")
            .eq("job_id", job_id)
            .execute()
        )

        completed = 0
        errors = 0

        for step in (steps.data or []):
            lid = step.get("lesson_id")
            if not lid:
                continue

            step_ok = step.get("diagrams_done", False) and step.get("narration_done", False)

            if step_ok:
                if not dry_run:
                    sb.table("lessons").update({
                        "status": "awaiting_qa",
                        "enrichment_completed_at": now,
                        "enrichment_error": None,
                    }).eq("id", lid).execute()
                completed += 1
            elif step.get("last_error"):
                error_msg = step["last_error"]
                log(f"  ERROR on lesson {lid}: {error_msg[:100]}")
                if not dry_run:
                    sb.table("lessons").update({
                        "enrichment_error": error_msg[:500],
                    }).eq("id", lid).execute()
                errors += 1
                # Leave status as 'publishing' for retry on next poll

        if errors:
            log(f"  {subject_slug}: {completed} completed, {errors} with errors (will retry)")
        else:
            log(f"  {subject_slug}: {completed}/{total} completed, rest pending")

        return completed, errors


def process_group(sb, subject_slug, school_id, lessons, dry_run=False):
    """Process a single subject group through the Phase 2 enrichment pipeline.

    Args:
        sb: Supabase client.
        subject_slug: Subject slug.
        school_id: School UUID or None (generic).
        lessons: List of enriched lesson dicts.
        dry_run: If True, only log what would happen.

    Returns:
        (completed_count, error_count).
    """
    scope = f"school={school_id[:8]}..." if school_id else "generic"
    log(f"Processing {subject_slug} ({scope}): {len(lessons)} lessons")

    if dry_run:
        for l in lessons:
            log(f"  L{l['lesson_number']:02d} [{l['unit_slug']}]: {l['lesson_title']}")
        return len(lessons), 0

    # 1. Create synthetic job
    job_id = create_synthetic_job(sb, subject_slug, school_id)
    log(f"  Created job {job_id}")

    # 2. Create pipeline steps
    step_count = create_pipeline_steps(sb, job_id, lessons, subject_slug)
    log(f"  Created {step_count} pipeline steps")

    # 3. Mark enrichment started
    lesson_ids = [l["lesson_id"] for l in lessons]
    mark_enrichment_started(sb, lesson_ids)

    # 4. Run asset scripts
    diag_ok, narr_ok = run_asset_scripts(job_id)

    # 5. Check results and finalise
    completed, errors = check_and_finalise(sb, job_id, lessons, subject_slug)

    # 6. Update synthetic job status
    if completed == len(lessons) and errors == 0:
        sb.table("upload_jobs").update({
            "status": "complete",
            "current_phase": "complete",
        }).eq("id", job_id).execute()
    elif errors > 0:
        sb.table("upload_jobs").update({
            "status": "error",
            "current_phase": "enriching",
        }).eq("id", job_id).execute()

    return completed, errors


def single_pass(sb, dry_run=False):
    """Run a single polling pass. Returns total lessons processed."""
    # 1. Fetch publishing lessons
    lessons = fetch_publishing_lessons(sb)
    if not lessons:
        log("No lessons in 'publishing' status.")
        return 0

    log(f"Found {len(lessons)} lessons in 'publishing' status")

    # 2. Group by subject
    groups = group_by_subject(lessons)
    log(f"Grouped into {len(groups)} subject(s)")

    # 3. Process each group
    total_completed = 0
    total_errors = 0

    for (subject_slug, school_id), group_lessons in groups.items():
        try:
            completed, errors = process_group(
                sb, subject_slug, school_id, group_lessons, dry_run=dry_run
            )
            total_completed += completed
            total_errors += errors
        except Exception as e:
            log(f"ERROR processing {subject_slug}: {e}")
            total_errors += len(group_lessons)

    log(f"Pass complete: {total_completed} enriched, {total_errors} errors")
    return total_completed + total_errors


def main():
    parser = argparse.ArgumentParser(
        description="Phase 2 polling — enrich lessons in 'publishing' status"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Single pass then exit (no polling loop)"
    )
    parser.add_argument(
        "--interval", type=int, default=60,
        help="Polling interval in seconds (default: 60)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be processed without running asset scripts"
    )
    args = parser.parse_args()

    log("Phase 2 Enrichment Pipeline")
    log(f"  Mode: {'single pass' if args.once else f'polling (every {args.interval}s)'}")
    if args.dry_run:
        log("  DRY RUN — no changes will be made")
    log("")

    sb = get_client()

    if args.once:
        single_pass(sb, dry_run=args.dry_run)
        return

    # Polling loop
    log(f"Starting polling loop (interval: {args.interval}s). Ctrl+C to stop.\n")
    try:
        while True:
            try:
                single_pass(sb, dry_run=args.dry_run)
            except Exception as e:
                log(f"ERROR in polling pass: {e}")

            log(f"Sleeping {args.interval}s...\n")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        log("\nStopped by user.")


if __name__ == "__main__":
    main()
