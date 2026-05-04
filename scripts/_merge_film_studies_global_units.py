"""Merge 4 Film Studies units (global-film foundations + 3 case-study units)
into one 'Global Film and UK Film' unit.

Before: 8 units, 44 lessons. The 4 affected units host 5+5+5+5=20 lessons.
After:  5 units, 44 lessons. Single unit holds all 20 lessons (foundations
        L1-5, EN-language case studies L6-10, non-EN-language L11-15, UK L16-20).

The browse-loader's FILM_SELECTABLE filter is keyed on lesson slug, so
moving lessons between units doesn't affect the per-film picker behaviour.

Idempotent: re-runs detect that the merge has already happened (slug
'global-and-uk-film' exists, 3 sub-units gone) and become a no-op.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

SUBJECT_SLUG = "film-studies-eduqas"

DEST_SLUG_OLD = "global-film"
DEST_SLUG_NEW = "global-and-uk-film"
DEST_NAME_NEW = "Global Film and UK Film"
DEST_SUBTITLE_NEW = "Foundations of narrative, representation and aesthetic, plus case studies of the global English-language, global non-English-language and UK films you study."

# Order of merging matters: foundations (existing global-film) keeps L1-5.
# Then the 3 case-study units feed into L6-10, L11-15, L16-20.
SOURCE_UNIT_ORDER = [
    ("global-english-language-films", 6),
    ("global-non-english-language-films", 11),
    ("contemporary-uk-films", 16),
]

print(f"=== Merging Film Studies global/UK units ===\n")

sid = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data[0]["id"]
units = sb.table("units").select("*").eq("subject_id", sid).order("sort_order").execute().data
units_by_slug = {u["slug"]: u for u in units}

if DEST_SLUG_NEW in units_by_slug and DEST_SLUG_OLD not in units_by_slug:
    print(f"  Already merged. No-op.")
    sys.exit(0)

dest = units_by_slug.get(DEST_SLUG_OLD)
if not dest:
    print(f"  Cannot find destination unit '{DEST_SLUG_OLD}'. Aborting.")
    sys.exit(1)

# 1. Rename the destination unit
print(f"--- Renaming destination unit ---")
sb.table("units").update({
    "slug": DEST_SLUG_NEW,
    "name": DEST_NAME_NEW,
    "subtitle": DEST_SUBTITLE_NEW,
    "lesson_count": 20,
}).eq("id", dest["id"]).execute()
print(f"  {DEST_SLUG_OLD} -> {DEST_SLUG_NEW} ('{DEST_NAME_NEW}')")
print(f"  lesson_count: 5 -> 20")

# 2. Move lessons from the 3 source units into dest, renumbering as we go
print(f"\n--- Moving lessons ---")
for src_slug, dest_start_num in SOURCE_UNIT_ORDER:
    src = units_by_slug.get(src_slug)
    if not src:
        print(f"  SKIP '{src_slug}' (not found — may already be merged)")
        continue
    rows = sb.table("lessons").select("id, lesson_number, slug, title").eq("unit_id", src["id"]).order("lesson_number").execute().data
    for i, r in enumerate(rows):
        new_num = dest_start_num + i
        sb.table("lessons").update({
            "unit_id": dest["id"],
            "lesson_number": new_num,
        }).eq("id", r["id"]).execute()
        print(f"  L{r['lesson_number']:2d} {r['slug'][:50]:50s}  ->  L{new_num:2d} (in {DEST_SLUG_NEW})")

# 3. Delete the 3 emptied source units
print(f"\n--- Deleting emptied source units ---")
for src_slug, _ in SOURCE_UNIT_ORDER:
    src = units_by_slug.get(src_slug)
    if not src:
        continue
    cnt = sb.table("lessons").select("id", count="exact").eq("unit_id", src["id"]).execute().count
    if cnt > 0:
        print(f"  REFUSE delete '{src_slug}' — still has {cnt} lessons")
        continue
    sb.table("units").delete().eq("id", src["id"]).execute()
    print(f"  deleted: {src_slug}")

# 4. Compress sort_order: developments-in-film-technology was sort_order 8, now should be 5
print(f"\n--- Compressing sort_order ---")
remaining = sb.table("units").select("id, slug, sort_order").eq("subject_id", sid).order("sort_order").execute().data
for new_order, u in enumerate(remaining, start=1):
    if u["sort_order"] != new_order:
        sb.table("units").update({"sort_order": new_order}).eq("id", u["id"]).execute()
        print(f"  {u['slug']:35s}  sort_order {u['sort_order']} -> {new_order}")

# 5. Verify
print(f"\n--- Verification ---")
final = sb.table("units").select("slug, sort_order, lesson_count").eq("subject_id", sid).order("sort_order").execute().data
total_lessons = 0
for u in final:
    cnt = sb.table("lessons").select("id", count="exact").eq("unit_id", sb.table("units").select("id").eq("subject_id", sid).eq("slug", u["slug"]).execute().data[0]["id"]).execute().count
    total_lessons += cnt
    print(f"  [{u['sort_order']}] {u['slug']:35s}  declared={u['lesson_count']}  actual={cnt}")
print(f"\n  Total lessons across {len(final)} units: {total_lessons}")
