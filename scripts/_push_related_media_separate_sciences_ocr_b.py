"""
Push upgraded related_media to Supabase for separate-sciences-ocr-b (54 lessons).
Updates only the related_media column using the lesson_id from each JSON file.

Run: python scripts/_push_related_media_separate_sciences_ocr_b.py
"""

import json
import os
import glob
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

LESSON_DIR = os.path.join(os.path.dirname(__file__), "_content_separate-sciences-ocr-b", "lessons")
sb = get_client()

files = sorted(glob.glob(os.path.join(LESSON_DIR, "*.json")))
print(f"Processing {len(files)} lesson files...\n")

ok = 0
skipped = 0
errors = 0

for filepath in files:
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    lesson_id = data.get("_lesson_id")
    slug = data.get("_lesson_slug", os.path.basename(filepath))
    related_media = data.get("related_media", [])

    if not lesson_id:
        print(f"  SKIP (no _lesson_id): {slug}")
        skipped += 1
        continue

    if not related_media:
        # Practice-format lessons have no related_media — skip silently
        skipped += 1
        continue

    try:
        result = (
            sb.table("lessons")
            .update({"related_media": related_media})
            .eq("id", lesson_id)
            .execute()
        )
        if result.data:
            print(f"  OK [{lesson_id[:8]}] {slug}")
            ok += 1
        else:
            print(f"  WARN no rows matched [{lesson_id[:8]}] {slug}")
            errors += 1
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        errors += 1

print(f"\nDone. {ok} updated, {skipped} skipped (no media/id), {errors} errors.")
