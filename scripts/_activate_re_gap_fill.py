"""Phase 2 — gap-fill activator for AQA RE.

Reads scripts/_plan_religious-education-gap-fill.json and adds 12 new units
+ ~46 lesson shells to the existing free-tier `religious-education` subject.
Does NOT recreate the subject row, does NOT touch the existing 8 units.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads(
    (scripts / "_plan_religious-education-gap-fill.json").read_text(encoding="utf-8")
)
sb = get_client()

if not plan.get("is_gap_fill"):
    print("Plan is missing is_gap_fill flag. Aborting.")
    sys.exit(1)

SUBJECT_SLUG = plan["subject_slug"]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[‘’′]", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


print(f"=== Gap-filling {SUBJECT_SLUG} ===\n")

existing_subj = sb.table("subjects").select("*").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data
if not existing_subj:
    print(f"  ABORT: subject '{SUBJECT_SLUG}' does not exist as free-tier. Use the regular activator instead.")
    sys.exit(2)

SUBJECT_ID = existing_subj[0]["id"]
print(f"  Subject row: {SUBJECT_ID}")

existing_units = sb.table("units").select("*").eq("subject_id", SUBJECT_ID).order("sort_order").execute().data
existing_unit_slugs = {u["slug"] for u in existing_units}
print(f"  Existing units ({len(existing_units)}): {[u['slug'] for u in existing_units]}\n")

# === Reconcile units ===
print(f"--- Adding {len(plan['article_units'])} new units ---")

unit_rows = {}
for pu in plan["article_units"]:
    slug = pu["slug"]
    if slug in existing_unit_slugs:
        existing = next(u for u in existing_units if u["slug"] == slug)
        unit_rows[slug] = existing
        print(f"  SKIP existing: {slug}")
        continue

    payload = {
        "subject_id": SUBJECT_ID,
        "slug": slug,
        "name": pu["name"],
        "subtitle": pu["subtitle"],
        "body_class": pu["body_class"],
        "accent": pu["accent"],
        "accent_light": pu["accent_light"],
        "accent_badge": pu["accent_badge"],
        "lesson_count": pu["lesson_count"],
        "sort_order": pu["sort_order"],
        "image_url": None,
    }
    res = sb.table("units").insert(payload).execute()
    unit_rows[slug] = res.data[0]
    print(f"  INSERTED: {slug:48s} sort={pu['sort_order']:2d} ({pu['lesson_count']} lessons)")


# === Insert lesson shells ===
print(f"\n--- Inserting lesson shells ---")

total_inserted = 0
total_skipped = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    existing_lessons = sb.table("lessons").select("id, lesson_number, slug").eq("unit_id", unit_id).execute().data
    nums_present = {L["lesson_number"] for L in existing_lessons}
    used_slugs = {L["slug"] for L in existing_lessons}

    new_in_unit = 0
    for L in pu["lessons"]:
        n = L["number"]
        if n in nums_present:
            total_skipped += 1
            continue

        title = L["title"].strip()
        description = (L.get("description") or "").strip()[:300]

        base_slug = slugify(title) or f"lesson-{n}"
        slug = base_slug
        i = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{i}"
            i += 1
        used_slugs.add(slug)

        sb.table("lessons").insert({
            "unit_id": unit_id,
            "lesson_number": n,
            "slug": slug,
            "title": title,
            "description": description,
            "status": "pending_review",
            "tier": "both",
        }).execute()
        new_in_unit += 1
        total_inserted += 1

    print(f"  [{pu['slug']:40s}] new={new_in_unit}/{len(pu['lessons'])}")

print(f"\n  Lessons inserted: {total_inserted}, skipped (already present): {total_skipped}")


# === Verify ===
print("\n--- Verification ---")
all_units = sb.table("units").select("slug, lesson_count").eq("subject_id", SUBJECT_ID).order("sort_order").execute().data
total_in_db = 0
for u in all_units:
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", sb.table("units").select("id").eq("subject_id", SUBJECT_ID).eq("slug", u["slug"]).execute().data[0]["id"])
        .execute()
        .count
    )
    total_in_db += cnt
print(f"  Subject total: {len(all_units)} units, {total_in_db} lessons")
print(f"\n=== Gap-fill activation complete ===")
