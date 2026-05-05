"""Strip placeholder Podcasts category from the 46 NEW lessons added in the
RE gap-fill session.

CRITICAL: only touch the 12 NEW units (sort_order 9-20). The original 8 units
(Christianity / Islam / Themes A/B/D/E) have legitimate, generated podcasts
that must NOT be touched.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

# Explicit allow-list. Refuse to act on any unit not in this list.
NEW_UNIT_SLUGS = {
    "buddhism-beliefs",
    "buddhism-practices",
    "catholic-christianity-beliefs",
    "catholic-christianity-practices",
    "hinduism-beliefs",
    "hinduism-practices",
    "judaism-beliefs",
    "judaism-practices",
    "sikhism-beliefs",
    "sikhism-practices",
    "theme-c-existence-of-god",
    "theme-f-human-rights-social-justice",
}

sid = sb.table("subjects").select("id").eq("slug", "religious-education").is_("school_id", "null").execute().data[0]["id"]
units = sb.table("units").select("id, slug, sort_order").eq("subject_id", sid).order("sort_order").execute().data

# Sanity check before any writes — confirm the new units exist and the old ones aren't in our target set
seen_new = set()
old_in_target = set()
for u in units:
    if u["slug"] in NEW_UNIT_SLUGS:
        seen_new.add(u["slug"])
    elif u["sort_order"] <= 8:
        if u["slug"] in NEW_UNIT_SLUGS:
            old_in_target.add(u["slug"])

if old_in_target:
    print(f"ABORT: original-8 unit found in target set: {old_in_target}")
    sys.exit(1)

missing = NEW_UNIT_SLUGS - seen_new
if missing:
    print(f"ABORT: expected NEW unit slugs not found in subject: {missing}")
    sys.exit(1)

print(f"Sanity check OK — {len(seen_new)}/{len(NEW_UNIT_SLUGS)} target units exist; original-8 untouched.\n")

stripped = 0
already_clean = 0
skipped_old = 0
for u in units:
    if u["slug"] not in NEW_UNIT_SLUGS:
        skipped_old += 1
        continue
    rows = (
        sb.table("lessons")
        .select("id, lesson_number, slug, related_media")
        .eq("unit_id", u["id"])
        .order("lesson_number")
        .execute()
        .data
    )
    for r in rows:
        rm = r.get("related_media") or []
        had_podcasts = any(c.get("category") == "Podcasts" for c in rm)
        if not had_podcasts:
            already_clean += 1
            continue
        new_rm = [c for c in rm if c.get("category") != "Podcasts"]
        sb.table("lessons").update({"related_media": new_rm}).eq("id", r["id"]).execute()
        print(f"  cleared {u['slug']:38s} L{r['lesson_number']:2d} {r['slug']}")
        stripped += 1

print(f"\n  Stripped: {stripped}")
print(f"  Already clean: {already_clean}")
print(f"  Original-8 units skipped: {skipped_old}")
