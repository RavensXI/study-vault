"""
Pipeline API Media — Generate related media sidebar content via the Anthropic API.

Usage:
    # By job ID (original mode — all lessons for that job's subject):
    python scripts/pipeline_api_media.py <job_id>

    # By subject/unit (direct mode — no job required):
    python scripts/pipeline_api_media.py --subject english-literature --unit macbeth
    python scripts/pipeline_api_media.py --subject english-literature --unit animal-farm --lessons 4,5,10

    # Skip lessons that already have related_media:
    python scripts/pipeline_api_media.py --subject english-literature --unit macbeth --skip-existing
"""

import argparse
import json
import os
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import anthropic
from lib.supabase_client import get_client

MODEL = "claude-sonnet-4-20250514"
INPUT_PRICE = 3.0
OUTPUT_PRICE = 15.0


def load_doc(filename):
    path = os.path.join(PROJECT_ROOT, "docs", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(subject_name, exam_board, spec_code, unit_name, lesson_title, media_doc):
    """Build the user message for the API call."""
    return f"""You are generating related media sidebar content for a GCSE {subject_name} lesson.

SUBJECT: {subject_name} ({exam_board} {spec_code})
UNIT: {unit_name}
LESSON: {lesson_title}

{media_doc}

IMPORTANT GUIDELINES:
- YouTube is excellent — find subject-specific educational channels and video essays
- Movies/TV/Documentaries: use JustWatch UK URLs (justwatch.com/uk/movie/slug or justwatch.com/uk/tv-series/slug)
- Podcasts: link to specific episodes on Spotify, Apple Podcasts, or BBC Sounds
- Study Tools should include the exam board spec page and BBC Bitesize where relevant
- Target 4-8 items across all categories
- Skip categories where nothing genuinely good exists

Return ONLY a JSON array (no markdown fences, no explanation). Each element is a category object:
[
  {{
    "category": "Videos & Channels",
    "emoji": "🎬",
    "items": [
      {{ "title": "Item Title", "url": "https://...", "description": "One-line description" }}
    ]
  }}
]

Category order: Podcasts, Videos & Channels, Movies, TV Shows, Documentaries, Study Tools.
Emojis: Podcasts 🎧, Videos & Channels 🎬, Movies 🎥, TV Shows 📺, Documentaries 🎬, Study Tools 📚.
Omit any category with no good items. Max 3 items per category."""


def run_media(lessons, subject_name, exam_board, spec_code, sb, client, media_doc, job_id=None):
    """Generate and save related media for a list of lessons."""
    total_cost = 0.0
    total_input = 0
    total_output = 0
    done = 0

    print(f"Generating related media for {len(lessons)} {subject_name} lessons")
    print(f"Model: {MODEL}")
    print()

    for idx, lesson in enumerate(lessons):
        print(f"[{idx+1}/{len(lessons)}] {lesson['unit_slug']} L{lesson['lesson_number']:02d}: {lesson['title']}")

        user_msg = build_prompt(
            subject_name, exam_board, spec_code,
            lesson["unit_name"], lesson["title"], media_doc
        )

        start = time.time()
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": user_msg}],
        )
        elapsed = time.time() - start
        usage = response.usage
        cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE + (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
        total_cost += cost
        total_input += usage.input_tokens
        total_output += usage.output_tokens

        media_text = response.content[0].text.strip()
        if media_text.startswith("```"):
            media_text = re.sub(r"^```(?:json)?\s*\n?", "", media_text)
            media_text = re.sub(r"\n?```\s*$", "", media_text)

        try:
            media_json = json.loads(media_text)
        except json.JSONDecodeError as e:
            print(f"  WARNING: Invalid JSON, skipping: {e}")
            continue

        # Write to lesson
        sb.table("lessons").update({"related_media": media_json}).eq("id", lesson["lesson_id"]).execute()

        # Update pipeline step if job_id provided
        if job_id:
            sb.table("pipeline_steps").update({"media_done": True}).eq(
                "job_id", job_id
            ).eq("unit_slug", lesson["unit_slug"]).eq("lesson_number", lesson["lesson_number"]).execute()

        done += 1
        print(f"  {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${cost:.4f}")

    print(f"\nMedia complete: {done}/{len(lessons)} lessons")
    print(f"  Tokens: {total_input:,} in / {total_output:,} out")
    print(f"  Cost: ${total_cost:.4f}")
    return total_cost


def cmd_media_by_job(job_id):
    """Original mode: generate media for all lessons in a job's subject."""
    sb = get_client()
    client = anthropic.Anthropic()

    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    plan = job.get("lesson_plan")
    if isinstance(plan, str):
        plan = json.loads(plan)

    subject_name = plan.get("subject_name", "GCSE Music")
    subject_slug = plan.get("subject_slug", "gcse-music")
    exam_board = plan.get("exam_board", "Eduqas")
    spec_code = plan.get("spec_code", "C660U")

    subj = sb.table("subjects").select("id").eq("slug", subject_slug).single().execute().data
    subject_id = subj["id"]

    media_doc = load_doc("RELATED_MEDIA_PIPELINE.md")

    units = sb.table("units").select("id,slug,name").eq("subject_id", subject_id).execute()
    all_lessons = []
    for u in units.data:
        lessons = sb.table("lessons").select("id,lesson_number,title").eq("unit_id", u["id"]).order("lesson_number").execute()
        for l in lessons.data:
            all_lessons.append({
                "lesson_id": l["id"],
                "lesson_number": l["lesson_number"],
                "title": l["title"],
                "unit_slug": u["slug"],
                "unit_name": u["name"],
            })

    return run_media(all_lessons, subject_name, exam_board, spec_code, sb, client, media_doc, job_id=job_id)


def cmd_media_by_subject(subject_slug, unit_slug=None, lesson_numbers=None, skip_existing=False):
    """Direct mode: generate media by subject/unit/lesson filtering."""
    sb = get_client()
    client = anthropic.Anthropic()

    # Look up subject
    subj = sb.table("subjects").select("id,name,settings").eq("slug", subject_slug).single().execute().data
    subject_id = subj["id"]
    subject_name = subj["name"]

    # Try to get exam board and spec code from settings
    settings = subj.get("settings") or {}
    if isinstance(settings, str):
        settings = json.loads(settings)
    exam_board = settings.get("exam_board", "")
    spec_code = settings.get("spec_code", "")

    media_doc = load_doc("RELATED_MEDIA_PIPELINE.md")

    # Get units
    units_q = sb.table("units").select("id,slug,name").eq("subject_id", subject_id)
    if unit_slug:
        units_q = units_q.eq("slug", unit_slug)
    units = units_q.execute()

    if not units.data:
        print(f"ERROR: No units found for subject={subject_slug}" + (f", unit={unit_slug}" if unit_slug else ""))
        sys.exit(1)

    all_lessons = []
    for u in units.data:
        lessons_q = sb.table("lessons").select("id,lesson_number,title,related_media").eq("unit_id", u["id"]).order("lesson_number")
        lessons = lessons_q.execute()
        for l in lessons.data:
            # Filter by lesson numbers if specified
            if lesson_numbers and l["lesson_number"] not in lesson_numbers:
                continue
            # Skip if already has media and flag is set
            if skip_existing and l.get("related_media"):
                print(f"  Skipping {u['slug']} L{l['lesson_number']:02d} — already has related_media")
                continue
            all_lessons.append({
                "lesson_id": l["id"],
                "lesson_number": l["lesson_number"],
                "title": l["title"],
                "unit_slug": u["slug"],
                "unit_name": u["name"],
            })

    if not all_lessons:
        print("No lessons to process (all may already have related_media).")
        return 0.0

    return run_media(all_lessons, subject_name, exam_board, spec_code, sb, client, media_doc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate related media sidebar content via the Anthropic API.")
    parser.add_argument("job_id", nargs="?", help="Job ID from upload_jobs table (original mode)")
    parser.add_argument("--subject", help="Subject slug (e.g. english-literature)")
    parser.add_argument("--unit", help="Unit slug (e.g. macbeth). If omitted, all units for the subject.")
    parser.add_argument("--lessons", help="Comma-separated lesson numbers (e.g. 4,5,10). If omitted, all lessons in the unit.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip lessons that already have related_media")

    args = parser.parse_args()

    if args.subject:
        # Direct mode
        lesson_numbers = None
        if args.lessons:
            lesson_numbers = [int(x.strip()) for x in args.lessons.split(",")]
        cmd_media_by_subject(args.subject, args.unit, lesson_numbers, args.skip_existing)
    elif args.job_id:
        # Original mode
        cmd_media_by_job(args.job_id)
    else:
        parser.print_help()
        sys.exit(1)
