"""Insert PE OCR lesson content into Supabase.

Each JSON in scripts/_content_food-preparation-and-nutrition-eduqas/lessons/ uses flat
`_lesson_id` field (set by the prep agent during batch creation).
Updates the matching lessons row with content fields.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

LESSON_DIR = Path(__file__).parent / "_content_food-preparation-and-nutrition-eduqas" / "lessons"

CONTENT_FIELDS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]

sb = get_client()

inserted = 0
skipped = 0
for f in sorted(LESSON_DIR.glob("*.json")):
    data = json.loads(f.read_text(encoding="utf-8"))
    lesson_id = data.get("_lesson_id")
    if not lesson_id:
        print(f"  SKIP (no lesson_id): {f.name}")
        skipped += 1
        continue

    payload = {k: data[k] for k in CONTENT_FIELDS if k in data}
    res = sb.table("lessons").update(payload).eq("id", lesson_id).execute()
    if res.data:
        print(f"  updated: {f.name[:60]:60s}  L{data.get('_lesson_number')}  ({len(payload)} fields)")
        inserted += 1
    else:
        print(f"  FAIL: {f.name} — no row matched id {lesson_id}")
        skipped += 1

print(f"\n  Updated: {inserted}, skipped: {skipped}")
