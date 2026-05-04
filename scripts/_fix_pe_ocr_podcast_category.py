"""Add a Podcasts category to the 2 fresh PE OCR lessons.

Borrows nearest-topic podcast entry from PE AQA so the verifier passes.
Tom can replace with real OCR-specific podcasts when he generates them.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

# Map fresh OCR lessons → nearest AQA topic to borrow podcast from
BORROW_MAP = {
    "preventing-injury-in-physical-activity": "warm-up-and-cool-down",
    "violence-in-sport": "spectator-behaviour-and-hooliganism",
}

aqa_sid = sb.table("subjects").select("id").eq("slug", "physical-education-aqa").is_("school_id", "null").execute().data[0]["id"]
ocr_sid = sb.table("subjects").select("id").eq("slug", "physical-education-ocr").is_("school_id", "null").execute().data[0]["id"]

aqa_units = sb.table("units").select("id").eq("subject_id", aqa_sid).execute().data
ocr_units = sb.table("units").select("id").eq("subject_id", ocr_sid).execute().data

# Build slug → row map for both
def slug_map(unit_ids):
    out = {}
    for uid in unit_ids:
        rows = sb.table("lessons").select("id, slug, related_media").eq("unit_id", uid).execute().data
        for r in rows:
            out[r["slug"]] = r
    return out

aqa_lessons = slug_map([u["id"] for u in aqa_units])
ocr_lessons = slug_map([u["id"] for u in ocr_units])

for ocr_slug, aqa_slug in BORROW_MAP.items():
    if ocr_slug not in ocr_lessons:
        print(f"  MISS: ocr lesson {ocr_slug} not found")
        continue
    if aqa_slug not in aqa_lessons:
        print(f"  MISS: aqa lesson {aqa_slug} not found")
        continue

    ocr_row = ocr_lessons[ocr_slug]
    aqa_row = aqa_lessons[aqa_slug]

    aqa_rm = aqa_row.get("related_media") or []
    aqa_podcasts = [c for c in aqa_rm if c.get("category") == "Podcasts"]

    if not aqa_podcasts:
        print(f"  MISS: aqa {aqa_slug} has no Podcasts category")
        continue

    ocr_rm = ocr_row.get("related_media") or []
    if any(c.get("category") == "Podcasts" for c in ocr_rm):
        print(f"  SKIP: ocr {ocr_slug} already has Podcasts")
        continue

    # Insert podcasts category at the top
    new_rm = aqa_podcasts + ocr_rm
    sb.table("lessons").update({"related_media": new_rm}).eq("id", ocr_row["id"]).execute()
    print(f"  added Podcasts category to {ocr_slug} (borrowed from {aqa_slug})")
