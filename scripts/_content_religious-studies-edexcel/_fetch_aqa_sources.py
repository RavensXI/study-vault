"""
Fetch AQA RS source lessons from Supabase and populate _aqa_source_lessons.json.

Run once before starting content generation:
    python scripts/_content_religious-studies-edexcel/_fetch_aqa_sources.py

Requires SUPABASE_SERVICE_KEY environment variable.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.supabase_client import get_client

sb = get_client()
workspace = Path(__file__).resolve().parent
output_path = workspace / "_aqa_source_lessons.json"

UNITS_TO_FETCH = [
    "catholic-christianity-beliefs",
    "catholic-christianity-practices",
    "christianity-beliefs",
    "christianity-practices",
    "islam-beliefs",
    "islam-practices",
    "buddhism-beliefs",
    "buddhism-practices",
    "hinduism-beliefs",
    "hinduism-practices",
    "judaism-beliefs",
    "judaism-practices",
    "sikhism-beliefs",
    "sikhism-practices",
    "theme-a-relationships",
    "theme-c-existence-of-god",
]

print("Fetching AQA RS source lessons from Supabase...")

# Get AQA RS units
units_res = (
    sb.table("units")
    .select("id, slug, name")
    .eq("subject_slug", "religious-studies-aqa")
    .is_("school_id", "null")
    .in_("slug", UNITS_TO_FETCH)
    .execute()
)

if not units_res.data:
    print("ERROR: No AQA RS units found. Check that religious-studies-aqa is activated.")
    sys.exit(1)

unit_map = {u["slug"]: u["id"] for u in units_res.data}
print(f"  Found {len(unit_map)} AQA RS units")

result = {
    "_note": "AQA RS source lessons indexed by unit_slug. Fetched from Supabase.",
    "_fetched_units": len(unit_map),
}

for slug in UNITS_TO_FETCH:
    if slug not in unit_map:
        print(f"  WARN: unit '{slug}' not found in Supabase — leaving empty array")
        result[slug] = []
        continue

    unit_id = unit_map[slug]
    lessons_res = (
        sb.table("lessons")
        .select(
            "id, lesson_number, slug, title, description, "
            "content_html, practice_questions, knowledge_checks, "
            "flashcard_questions, glossary_terms"
        )
        .eq("unit_id", unit_id)
        .order("lesson_number")
        .execute()
    )

    lessons = lessons_res.data or []
    print(f"  {slug}: {len(lessons)} lessons")

    result[slug] = [
        {
            "id": L["id"],
            "lesson_number": L["lesson_number"],
            "slug": L["slug"],
            "title": L["title"],
            "description": L.get("description") or "",
            "content_html": L.get("content_html") or "",
            "practice_questions": L.get("practice_questions") or [],
            "knowledge_checks": L.get("knowledge_checks") or [],
            "flashcard_questions": L.get("flashcard_questions") or [],
            "glossary_terms": L.get("glossary_terms") or [],
        }
        for L in lessons
    ]

output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nWritten to {output_path}")
total = sum(len(v) for k, v in result.items() if k not in ("_note", "_fetched_units"))
print(f"Total source lessons: {total}")
