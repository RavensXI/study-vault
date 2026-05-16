"""
Fetch RS Edexcel lesson UUIDs from Supabase and patch them into all batch files.

Run once before starting content generation (after _fetch_aqa_sources.py):
    python scripts/_content_religious-studies-edexcel/_fetch_lesson_ids.py

Updates every _batch_bNN.json file in this workspace, replacing "LOOKUP_BY_SLUG"
lesson_id values with the real UUIDs from Supabase.

Requires SUPABASE_SERVICE_KEY environment variable.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.supabase_client import get_client

sb = get_client()
workspace = Path(__file__).resolve().parent

print("Fetching RS Edexcel lesson UUIDs from Supabase...")

# Fetch all lessons for religious-studies-edexcel
units_res = (
    sb.table("units")
    .select("id, slug")
    .eq("subject_slug", "religious-studies-edexcel")
    .execute()
)

if not units_res.data:
    print("ERROR: No RS Edexcel units found.")
    sys.exit(1)

unit_ids = [u["id"] for u in units_res.data]

lessons_res = (
    sb.table("lessons")
    .select("id, slug, lesson_number, unit_id")
    .in_("unit_id", unit_ids)
    .execute()
)

# Build slug -> uuid map (unit_id -> {lesson_number: uuid})
unit_slug_map = {u["id"]: u["slug"] for u in units_res.data}
lessons_by_slug: dict[str, str] = {}
for L in lessons_res.data:
    lessons_by_slug[L["slug"]] = L["id"]

print(f"  Found {len(lessons_by_slug)} lessons")

# Patch all batch files
batch_files = sorted(workspace.glob("_batch_b*.json"))
for bf in batch_files:
    data = json.loads(bf.read_text(encoding="utf-8"))
    changed = 0
    for lesson in data.get("lessons_in_batch", []):
        if lesson.get("lesson_id") == "LOOKUP_BY_SLUG":
            slug = lesson.get("lesson_slug", "")
            if slug in lessons_by_slug:
                lesson["lesson_id"] = lessons_by_slug[slug]
                changed += 1
            else:
                print(f"  WARN: slug '{slug}' not found in Supabase")
    if changed:
        bf.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  Patched {changed} lesson_ids in {bf.name}")
    else:
        print(f"  {bf.name}: nothing to patch")

print("\nDone. Run content agents next.")
