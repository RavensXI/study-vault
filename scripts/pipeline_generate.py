"""
Pipeline Generate — Helper for Claude Code content generation sessions.

Reads an upload_job from Supabase (PPT extracted text + lesson plan),
provides functions to write generated lessons back to the database.
Designed to be used within a Claude Code session where Claude generates
the content and this script handles all DB operations.

Usage (from Claude Code):
    python scripts/pipeline_generate.py info <job_id>
    python scripts/pipeline_generate.py text <job_id>
    python scripts/pipeline_generate.py write <job_id> <unit_slug> <lesson_number> <json_file>
    python scripts/pipeline_generate.py status <job_id>
    python scripts/pipeline_generate.py review <job_id>
"""

import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from supabase import create_client


def get_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        sys.exit(1)
    return create_client(url, key)


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
    subject_data = {
        "school_id": school_id,
        "slug": plan.get("subject_slug", job.get("subject_slug")),
        "name": plan.get("subject_name", config.get("subject_name", "Unknown")),
        "exam_board": plan.get("exam_board", config.get("exam_board", "Unknown")),
        "spec_code": plan.get("spec_code", config.get("spec_code")) or None,
        "status": "draft",
        "is_active": False,
    }
    subject = sb.table("subjects").upsert(subject_data, on_conflict="school_id,slug").select("id").single().execute().data

    # Upsert unit
    colors = config.get("colors", {})
    accent = colors.get(f"color{unit_index + 1}", colors.get("color1", "#6b7280"))
    unit_data = {
        "subject_id": subject["id"],
        "slug": unit_slug,
        "name": unit_plan["name"],
        "body_class": f"unit-{plan.get('subject_slug', 'unknown')}-{unit_index + 1}",
        "accent": accent,
        "accent_light": accent + "22",
        "accent_badge": accent + "33",
        "lesson_count": len(unit_plan.get("lessons", [])),
    }
    unit = sb.table("units").upsert(unit_data, on_conflict="subject_id,slug").select("id").single().execute().data

    # Upsert lesson
    lesson_record = {
        "unit_id": unit["id"],
        "lesson_number": lesson_number,
        "slug": f"lesson-{lesson_number:02d}",
        "title": lesson_plan["title"],
        "content_html": lesson_data.get("content_html", ""),
        "exam_tip_html": lesson_data.get("exam_tip_html"),
        "conclusion_html": lesson_data.get("conclusion_html"),
        "practice_questions": lesson_data.get("practice_questions", []),
        "knowledge_checks": lesson_data.get("knowledge_checks", []),
        "glossary_terms": lesson_data.get("glossary_terms", []),
        "status": "draft",
    }
    lesson = sb.table("lessons").upsert(lesson_record, on_conflict="unit_id,lesson_number").select("id").single().execute().data

    # Update pipeline step
    sb.table("pipeline_steps").upsert({
        "job_id": job_id,
        "unit_slug": unit_slug,
        "lesson_number": lesson_number,
        "lesson_title": lesson_plan["title"],
        "lesson_id": lesson["id"],
        "content_done": True,
        "questions_done": True,
        "glossary_done": True,
    }, on_conflict="job_id,unit_slug,lesson_number").execute()

    # Update lessons_created count
    completed = sb.table("pipeline_steps").select("id").eq("job_id", job_id).eq("content_done", True).execute()
    sb.table("upload_jobs").update({
        "lessons_created": len(completed.data),
        "current_phase": "generating",
    }).eq("id", job_id).execute()

    print(f"OK: Lesson {lesson_number} '{lesson_plan['title']}' written to Supabase (id: {lesson['id']})")


def cmd_status(job_id):
    """Show pipeline progress summary."""
    sb = get_client()
    steps = sb.table("pipeline_steps").select("*").eq("job_id", job_id).order("unit_slug").order("lesson_number").execute()

    total = len(steps.data) if steps.data else 0
    done = sum(1 for s in (steps.data or []) if s["content_done"])
    errors = sum(1 for s in (steps.data or []) if s.get("last_error"))

    print(f"Progress: {done}/{total} lessons generated ({errors} errors)")
    for s in (steps.data or []):
        icon = "[OK]" if s["content_done"] else ("[ERR]" if s.get("last_error") else "[  ]")
        print(f"  {icon} L{s['lesson_number']} {s['lesson_title']}")


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
        print(__doc__)
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
    elif cmd == "review":
        cmd_review(job_id)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
