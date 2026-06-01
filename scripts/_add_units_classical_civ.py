"""Additively add the 6 new option-units (sort_order >= 5) to the existing
classical-civilisation-ocr subject. Purely additive: inserts unit rows and
empty lesson shells only where they don't already exist. Never deletes or
overwrites populated lessons (the existing 21 are untouched).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

plan = json.loads(Path("scripts/_plan_classical-civilisation-ocr.json").read_text(encoding="utf-8"))
sb = get_client()
SLUG = "classical-civilisation-ocr"


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[‘’′]", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:80]


subj = sb.table("subjects").select("id").eq("slug", SLUG).is_("school_id", "null").single().execute().data
SID = subj["id"]
existing_units = {u["slug"]: u for u in sb.table("units").select("id, slug").eq("subject_id", SID).execute().data}

new_units = [u for u in plan["article_units"] if u["sort_order"] >= 5]
print(f"Adding {len(new_units)} new units to {SLUG} ({SID[:8]})")

units_added = lessons_added = 0
for pu in new_units:
    slug = pu["slug"]
    if slug in existing_units:
        unit_id = existing_units[slug]["id"]
        print(f"  unit exists: {slug}")
    else:
        payload = {
            "subject_id": SID, "slug": slug, "name": pu["name"], "subtitle": pu["subtitle"],
            "body_class": pu["body_class"], "accent": pu["accent"], "accent_light": pu["accent_light"],
            "accent_badge": pu["accent_badge"], "lesson_count": pu["lesson_count"],
            "sort_order": pu["sort_order"], "image_url": None,
        }
        unit_id = sb.table("units").insert(payload).execute().data[0]["id"]
        units_added += 1
        print(f"  INSERTED unit: {slug} ({pu['lesson_count']} lessons)")

    present = {L["lesson_number"] for L in sb.table("lessons").select("lesson_number").eq("unit_id", unit_id).execute().data}
    used_slugs = {L["slug"] for L in sb.table("lessons").select("slug").eq("unit_id", unit_id).execute().data}
    for L in pu["lessons"]:
        if L["number"] in present:
            continue
        base = slugify(L["title"]) or f"lesson-{L['number']}"
        s = base; i = 2
        while s in used_slugs:
            s = f"{base}-{i}"; i += 1
        used_slugs.add(s)
        sb.table("lessons").insert({
            "unit_id": unit_id, "lesson_number": L["number"], "slug": s,
            "title": L["title"].strip(), "description": (L.get("description") or "").strip()[:300],
            "status": "pending_review", "tier": "both",
        }).execute()
        lessons_added += 1

print(f"\n  Units added: {units_added}, lesson shells added: {lessons_added}")
total = sb.table("units").select("id", count="exact").eq("subject_id", SID).execute().count
print(f"  Subject now has {total} units total.")
