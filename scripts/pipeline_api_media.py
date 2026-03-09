"""
Pipeline API Media — Generate related media sidebar content via the Anthropic API.

Usage:
    python scripts/pipeline_api_media.py <job_id>
"""

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

MODEL = "claude-opus-4-6"
INPUT_PRICE = 15.0
OUTPUT_PRICE = 75.0


def load_doc(filename):
    path = os.path.join(PROJECT_ROOT, "docs", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def cmd_media(job_id):
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

    # Get all units and lessons
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

    total_cost = 0.0
    total_input = 0
    total_output = 0
    done = 0

    print(f"Generating related media for {len(all_lessons)} {subject_name} lessons")
    print(f"Model: {MODEL}")
    print()

    for idx, lesson in enumerate(all_lessons):
        print(f"[{idx+1}/{len(all_lessons)}] {lesson['unit_slug']} L{lesson['lesson_number']:02d}: {lesson['title']}")

        user_msg = f"""You are generating related media sidebar content for a GCSE {subject_name} lesson.

SUBJECT: {subject_name} ({exam_board} {spec_code})
UNIT: {lesson['unit_name']}
LESSON: {lesson['title']}

{media_doc}

IMPORTANT GUIDELINES FOR MUSIC:
- YouTube is excellent for music — channels like Adam Neely, 12tone, David Bennett Piano, Rick Beato, Listening In, Classic FM
- For set work lessons (Bach Badinerie, Toto Africa), include specific analysis/performance videos
- For Film Music, link to actual film score analysis or memorable scenes
- For Jazz/Blues/Pop/Rock, link to iconic performances or explainer videos
- Study Tools should include: Eduqas GCSE Music spec page, BBC Bitesize GCSE Music
- Movies/TV/Documentaries: use JustWatch UK URLs (justwatch.com/uk/movie/slug or justwatch.com/uk/tv-series/slug)
- Podcasts: link to specific episodes on Spotify, Apple Podcasts, or BBC Sounds
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

        # Update pipeline step
        sb.table("pipeline_steps").update({"media_done": True}).eq(
            "job_id", job_id
        ).eq("unit_slug", lesson["unit_slug"]).eq("lesson_number", lesson["lesson_number"]).execute()

        done += 1
        print(f"  {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${cost:.4f}")

    print(f"\nMedia complete: {done}/{len(all_lessons)} lessons")
    print(f"  Tokens: {total_input:,} in / {total_output:,} out")
    print(f"  Cost: ${total_cost:.4f}")
    return total_cost


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    job_id = sys.argv[1]
    cmd_media(job_id)
