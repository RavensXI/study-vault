"""Insert Edexcel French practice_data into Supabase. One lesson per JSON file."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

LESSON_DIR = Path(__file__).parent / "_content_spanish-edexcel" / "lessons"

sb = get_client()

inserted = 0
skipped = 0
for f in sorted(LESSON_DIR.glob("*.json")):
    data = json.loads(f.read_text(encoding="utf-8"))
    lesson_id = data.get("_lesson_id")
    practice_data = data.get("practice_data")
    if not lesson_id or not practice_data:
        print(f"  SKIP (no lesson_id or practice_data): {f.name}")
        skipped += 1
        continue

    res = sb.table("lessons").update({"practice_data": practice_data}).eq("id", lesson_id).execute()
    if res.data:
        print(f"  updated: L{data.get('_lesson_number')} {f.name[:60]:60s}")
        inserted += 1
    else:
        print(f"  FAIL: {f.name} — no row matched id {lesson_id}")
        skipped += 1

print(f"\n  Updated: {inserted}, skipped: {skipped}")
