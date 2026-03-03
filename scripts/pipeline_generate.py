"""
Pipeline Generate — Helper for Claude Code content generation sessions.

Reads an upload_job from Supabase (PPT extracted text + lesson plan),
provides functions to write generated lessons back to the database,
and orchestrates asset generation scripts.

Usage (from Claude Code):
    python scripts/pipeline_generate.py info <job_id>
    python scripts/pipeline_generate.py text <job_id>
    python scripts/pipeline_generate.py write <job_id> <unit_slug> <lesson_number> <json_file>
    python scripts/pipeline_generate.py status <job_id>
    python scripts/pipeline_generate.py assets <job_id>
    python scripts/pipeline_generate.py run-all-assets <job_id>
    python scripts/pipeline_generate.py review <job_id>
"""

import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.pipeline import get_progress_summary, get_job_subject_slug


def cmd_info(job_id):
    """Show job info and extracted text stats."""
    sb = get_client()
    result = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute()
    job = result.data

    config = job.get("subject_config") or {}
    text = job.get("extracted_text") or ""
    plan = job.get("lesson_plan")

    print(f"Job ID:        {job['id']}")
    print(f"File:          {job['filename']}")
    print(f"Subject:       {config.get('subject_name', '—')}")
    print(f"Exam Board:    {config.get('exam_board', '—')} {config.get('spec_code', '')}")
    print(f"Phase:         {job['current_phase']}")
    print(f"Text Length:   {len(text):,} chars")
    print(f"Plan:          {'Yes' if plan else 'No'}")

    if plan:
        print(f"\nLesson Plan:")
        for unit in plan.get("units", []):
            print(f"\n  {unit['name']} ({unit['slug']}):")
            for lesson in unit.get("lessons", []):
                print(f"    L{lesson['number']}: {lesson['title']}")

    # Show pipeline steps status
    steps = sb.table("pipeline_steps").select("*").eq("job_id", job_id).order("unit_slug").order("lesson_number").execute()
    if steps.data:
        print(f"\nPipeline Steps ({len(steps.data)} lessons):")
        for s in steps.data:
            status = "DONE" if s["content_done"] else ("ERROR" if s.get("last_error") else "pending")
            print(f"  L{s['lesson_number']} [{s['unit_slug']}] {s['lesson_title']}: {status}")


def cmd_text(job_id):
    """Print the full extracted PPT text."""
    sb = get_client()
    result = sb.table("upload_jobs").select("extracted_text").eq("id", job_id).single().execute()
    print(result.data.get("extracted_text") or "(no text)")


def cmd_write(job_id, unit_slug, lesson_number, json_file):
    """Write a generated lesson to Supabase from a JSON file."""
    sb = get_client()
    lesson_number = int(lesson_number)

    # Read lesson data from JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        lesson_data = json.load(f)

    # Fetch the job for plan info
    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    plan = job.get("lesson_plan") or {}
    config = job.get("subject_config") or {}
    school_id = job.get("school_id")

    # Find unit and lesson in plan
    unit_plan = None
    lesson_plan = None
    unit_index = 0
    for i, u in enumerate(plan.get("units", [])):
        if u["slug"] == unit_slug:
            unit_plan = u
            unit_index = i
            for l in u.get("lessons", []):
                if l["number"] == lesson_number:
                    lesson_plan = l
                    break
            break

    if not unit_plan or not lesson_plan:
        print(f"ERROR: Unit '{unit_slug}' lesson {lesson_number} not found in plan")
        sys.exit(1)

    # Upsert subject
    subject_slug = plan.get("subject_slug", job.get("subject_slug"))
    subject_data = {
        "slug": subject_slug,
        "name": plan.get("subject_name", config.get("subject_name", "Unknown")),
        "exam_board": plan.get("exam_board", config.get("exam_board", "Unknown")),
        "spec_code": plan.get("spec_code", config.get("spec_code")) or None,
        "status": "live",
        "is_active": True,
    }
    if school_id:
        subject_data["school_id"] = school_id
    else:
        schools = sb.table("schools").select("id").limit(1).execute()
        subject_data["school_id"] = schools.data[0]["id"] if schools.data else None

    result = sb.table("subjects").upsert(subject_data, on_conflict="school_id,slug").execute()
    subject_id = result.data[0]["id"]

    # Upsert unit
    # Check if unit already exists (don't overwrite accent set by activation agent)
    existing_unit = sb.table("units").select("id").eq("subject_id", subject_id).eq("slug", unit_slug).execute()
    if existing_unit.data:
        # Unit exists — only update name and lesson_count, preserve accent/body_class
        unit_id = existing_unit.data[0]["id"]
        sb.table("units").update({
            "name": unit_plan["name"],
            "lesson_count": len(unit_plan.get("lessons", [])),
        }).eq("id", unit_id).execute()
    else:
        # New unit — set accent from config
        colors = config.get("colors", {})
        accent = colors.get(f"color{unit_index + 1}", colors.get("color1", "#6b7280"))
        unit_data = {
            "subject_id": subject_id,
            "slug": unit_slug,
            "name": unit_plan["name"],
            "body_class": f"unit-{plan.get('subject_slug', 'unknown')}-{unit_index + 1}",
            "accent": accent,
            "accent_light": accent + "22",
            "accent_badge": accent + "33",
            "lesson_count": len(unit_plan.get("lessons", [])),
        }
        result = sb.table("units").upsert(unit_data, on_conflict="subject_id,slug").execute()
        unit_id = result.data[0]["id"]
    unit_id = result.data[0]["id"]

    # Upsert lesson
    lesson_record = {
        "unit_id": unit_id,
        "lesson_number": lesson_number,
        "slug": f"lesson-{lesson_number:02d}",
        "title": lesson_plan["title"],
        "content_html": lesson_data.get("content_html", ""),
        "exam_tip_html": lesson_data.get("exam_tip_html"),
        "conclusion_html": lesson_data.get("conclusion_html"),
        "practice_questions": lesson_data.get("practice_questions", []),
        "knowledge_checks": lesson_data.get("knowledge_checks", []),
        "glossary_terms": lesson_data.get("glossary_terms", []),
        "status": "live",
    }
    if lesson_data.get("description"):
        lesson_record["description"] = lesson_data["description"]
    result = sb.table("lessons").upsert(lesson_record, on_conflict="unit_id,lesson_number").execute()
    lesson_id = result.data[0]["id"]

    # Update pipeline step — include asset metadata if present in lesson JSON
    step_data = {
        "job_id": job_id,
        "unit_slug": unit_slug,
        "lesson_number": lesson_number,
        "lesson_title": lesson_plan["title"],
        "lesson_id": lesson_id,
        "content_done": True,
        "questions_done": True,
        "glossary_done": True,
        "subject_slug": subject_slug,
    }

    # Store diagram prompt if provided in lesson JSON
    if lesson_data.get("diagram_prompt"):
        step_data["diagram_prompt"] = lesson_data["diagram_prompt"]

    # Store hero keywords if provided in lesson JSON
    if lesson_data.get("hero_keywords"):
        step_data["hero_keywords"] = lesson_data["hero_keywords"]

    # Store diagram style if provided
    if lesson_data.get("diagram_style"):
        step_data["diagram_style"] = lesson_data["diagram_style"]

    sb.table("pipeline_steps").upsert(
        step_data, on_conflict="job_id,unit_slug,lesson_number"
    ).execute()

    # Update lessons_created count
    completed = sb.table("pipeline_steps").select("id").eq("job_id", job_id).eq("content_done", True).execute()
    sb.table("upload_jobs").update({
        "lessons_created": len(completed.data),
        "current_phase": "generating",
    }).eq("id", job_id).execute()

    print(f"OK: Lesson {lesson_number} '{lesson_plan['title']}' written to Supabase (id: {lesson_id})")
    if lesson_data.get("diagram_prompt"):
        print(f"    diagram_prompt stored ({len(lesson_data['diagram_prompt'])} chars)")
    if lesson_data.get("hero_keywords"):
        print(f"    hero_keywords stored: {lesson_data['hero_keywords']}")


def cmd_status(job_id):
    """Show pipeline progress summary with all asset flags."""
    sb = get_client()
    summary = get_progress_summary(sb, job_id)
    total = summary["total"]

    print(f"Pipeline Progress ({total} lessons):")
    print(f"  Content:   {summary['content']}/{total}")
    print(f"  Diagrams:  {summary['diagrams']}/{total}")
    print(f"  Heroes:    {summary['heroes']}/{total}")
    print(f"  Narration: {summary['narration']}/{total}")
    print(f"  Media:     {summary['media']}/{total}")
    if summary["errors"]:
        print(f"  Errors:    {summary['errors']}")

    # Per-lesson detail
    steps = sb.table("pipeline_steps").select("*").eq("job_id", job_id).order("unit_slug").order("lesson_number").execute()
    print()
    for s in (steps.data or []):
        flags = ""
        flags += "C" if s["content_done"] else "."
        flags += "D" if s["diagrams_done"] else "."
        flags += "H" if s["hero_done"] else "."
        flags += "N" if s["narration_done"] else "."
        flags += "M" if s["media_done"] else "."
        err = f" ERR: {s['last_error'][:40]}" if s.get("last_error") else ""
        print(f"  [{flags}] L{s['lesson_number']:02d} {s['lesson_title']}{err}")

    print(f"\n  Legend: C=Content D=Diagrams H=Hero N=Narration M=Media")


def cmd_assets(job_id):
    """Show detailed per-lesson asset completion table."""
    sb = get_client()
    steps = sb.table("pipeline_steps").select("*").eq("job_id", job_id).order("unit_slug").order("lesson_number").execute()

    if not steps.data:
        print("No pipeline steps found for this job.")
        return

    # Header
    print(f"{'Lesson':<8} {'Unit':<20} {'Content':>7} {'Diag':>6} {'Hero':>6} {'Narr':>6} {'Media':>6} {'Prompt':>7} {'Keywords':>8}")
    print("-" * 85)

    for s in steps.data:
        yes_no = lambda v: "yes" if v else " - "
        has_prompt = "yes" if s.get("diagram_prompt") else " - "
        has_kw = "yes" if s.get("hero_keywords") else " - "
        print(
            f"L{s['lesson_number']:02d}      "
            f"{s['unit_slug']:<20} "
            f"{yes_no(s['content_done']):>7} "
            f"{yes_no(s['diagrams_done']):>6} "
            f"{yes_no(s['hero_done']):>6} "
            f"{yes_no(s['narration_done']):>6} "
            f"{yes_no(s['media_done']):>6} "
            f"{has_prompt:>7} "
            f"{has_kw:>8}"
        )

    summary = get_progress_summary(sb, job_id)
    total = summary["total"]
    print(f"\nTotals: C={summary['content']}/{total} D={summary['diagrams']}/{total} "
          f"H={summary['heroes']}/{total} N={summary['narration']}/{total} M={summary['media']}/{total}")


def cmd_run_all_assets(job_id):
    """Orchestrate: diagrams + heroes in parallel, then narration."""
    sb = get_client()

    # Verify all content is done
    summary = get_progress_summary(sb, job_id)
    if summary["content"] < summary["total"]:
        print(f"ERROR: Not all content is done ({summary['content']}/{summary['total']}). "
              f"Complete content generation first.")
        sys.exit(1)

    print(f"Running asset generation for job {job_id}")
    print(f"  {summary['total']} lessons, subject: {get_job_subject_slug(sb, job_id)}")
    print()

    python = sys.executable

    # Step 1: Run diagrams and heroes in parallel
    print("Step 1: Diagrams + Heroes (parallel)")
    print("=" * 50)

    procs = []

    if summary["diagrams"] < summary["total"]:
        print("  Starting diagram generation...")
        p_diag = subprocess.Popen(
            [python, os.path.join(SCRIPT_DIR, "generate_diagrams.py"), "--job-id", job_id],
            stdout=sys.stdout, stderr=sys.stderr,
        )
        procs.append(("diagrams", p_diag))
    else:
        print("  Diagrams: all done, skipping")

    if summary["heroes"] < summary["total"]:
        print("  Starting hero image download...")
        p_hero = subprocess.Popen(
            [python, os.path.join(SCRIPT_DIR, "download_heroes.py"), "--job-id", job_id],
            stdout=sys.stdout, stderr=sys.stderr,
        )
        procs.append(("heroes", p_hero))
    else:
        print("  Heroes: all done, skipping")

    # Wait for parallel processes
    for name, proc in procs:
        rc = proc.wait()
        status = "OK" if rc == 0 else f"FAILED (exit {rc})"
        print(f"\n  {name}: {status}")

    # Step 2: Run narration (after diagrams — placement can shift narration IDs)
    print(f"\nStep 2: Narration (sequential)")
    print("=" * 50)

    # Re-check progress after parallel step
    summary = get_progress_summary(sb, job_id)
    if summary["narration"] < summary["total"]:
        print("  Starting narration generation...")
        rc = subprocess.call(
            [python, os.path.join(SCRIPT_DIR, "generate_narration.py"), "--job-id", job_id],
            stdout=sys.stdout, stderr=sys.stderr,
        )
        status = "OK" if rc == 0 else f"FAILED (exit {rc})"
        print(f"\n  narration: {status}")
    else:
        print("  Narration: all done, skipping")

    # Final summary
    summary = get_progress_summary(sb, job_id)
    total = summary["total"]
    print(f"\n{'=' * 50}")
    print(f"ASSET GENERATION COMPLETE")
    print(f"{'=' * 50}")
    print(f"  Content:   {summary['content']}/{total}")
    print(f"  Diagrams:  {summary['diagrams']}/{total}")
    print(f"  Heroes:    {summary['heroes']}/{total}")
    print(f"  Narration: {summary['narration']}/{total}")
    print(f"  Media:     {summary['media']}/{total} (curated separately)")

    all_done = all(summary[k] >= total for k in ("content", "diagrams", "heroes", "narration"))
    if all_done:
        print(f"\nAll automated assets complete! Next: curate related media, then review.")
    else:
        print(f"\nSome assets still pending — check errors above.")


def cmd_review(job_id):
    """Send all completed lessons to review status."""
    sb = get_client()
    steps = sb.table("pipeline_steps").select("lesson_id, content_done").eq("job_id", job_id).execute()

    count = 0
    for s in (steps.data or []):
        if s["content_done"] and s.get("lesson_id"):
            sb.table("lessons").update({"status": "review"}).eq("id", s["lesson_id"]).execute()
            count += 1

    sb.table("upload_jobs").update({"current_phase": "complete"}).eq("id", job_id).execute()
    print(f"Sent {count} lessons to review.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__.strip())
        sys.exit(1)

    cmd = sys.argv[1]
    job_id = sys.argv[2]

    if cmd == "info":
        cmd_info(job_id)
    elif cmd == "text":
        cmd_text(job_id)
    elif cmd == "write":
        if len(sys.argv) < 6:
            print("Usage: pipeline_generate.py write <job_id> <unit_slug> <lesson_number> <json_file>")
            sys.exit(1)
        cmd_write(job_id, sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "status":
        cmd_status(job_id)
    elif cmd == "assets":
        cmd_assets(job_id)
    elif cmd == "run-all-assets":
        cmd_run_all_assets(job_id)
    elif cmd == "review":
        cmd_review(job_id)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
