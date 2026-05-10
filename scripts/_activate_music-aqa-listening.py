"""Phase 2 — Restructure music-aqa for v1 listening content.

Subject row already exists (id=505cc121-7381-458c-aa5b-5bb5f1152786).
Existing 'listening' unit is renamed to 'western-classical-1650-1910'.
Existing PoC Mozart lesson is kept as lesson_number=2.
New lesson shells inserted for all missing lessons.
Unit 'score-reading' inserted with sort_order=2.
Subject settings.practice_units updated to include both units.

Idempotent: checks for existing unit slugs and lesson_numbers before
inserting. If content_html or practice_data is found on any existing
lesson, the script aborts rather than overwriting.

Does NOT touch index.html, css/style.css, or any other subject's data.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads(
    (scripts / "_plan_music-aqa-listening.json").read_text(encoding="utf-8")
)
sb = get_client()

SUBJECT_ID = plan["subject_id"]  # 505cc121-7381-458c-aa5b-5bb5f1152786
SUBJECT_SLUG = plan["subject_slug"]  # music-aqa
SCHOOL_ID = None  # free tier
PLAN_UNITS = plan["units"]  # list of unit dicts from the plan

# ---- convenience --------------------------------------------------------

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[''′‘’]", "", s)
    s = re.sub(r"[–—–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


print(f"=== Phase 2: music-aqa listening restructure ===\n")

# ---- confirm subject row exists ----------------------------------------

subj_row = (
    sb.table("subjects")
    .select("*")
    .eq("id", SUBJECT_ID)
    .execute()
    .data
)
if not subj_row:
    print(f"ERROR: subject row {SUBJECT_ID} not found. Aborting.")
    sys.exit(1)
subj = subj_row[0]
print(f"  Found subjects row: {subj['slug']} (id={SUBJECT_ID[:8]}...)")

# ---- existing units under this subject ---------------------------------

existing_units = (
    sb.table("units")
    .select("*")
    .eq("subject_id", SUBJECT_ID)
    .order("sort_order")
    .execute()
    .data
)
print(f"  Existing units: {[u['slug'] for u in existing_units]}")

# Build maps for idempotency
units_by_slug = {u["slug"]: u for u in existing_units}

# ---- safety check: abort if any existing lesson has content populated --

all_existing_units = existing_units  # includes any old/renamed slugs
populated_lessons = []
poc_lesson = None  # The known PoC (Mozart Sym 40) — allowed to have practice_data
for eu in all_existing_units:
    lrows = (
        sb.table("lessons")
        .select("id, lesson_number, slug, title, content_html, practice_data")
        .eq("unit_id", eu["id"])
        .execute()
        .data
    )
    for L in lrows:
        if L.get("content_html") or L.get("practice_data"):
            # Identify the known PoC — Mozart Sym 40 in the 'listening' unit
            title_lower = (L.get("title") or "").lower()
            is_poc = (
                eu["slug"] in ("listening", "western-classical-1650-1910")
                and ("mozart" in title_lower or "symphony" in title_lower or "40" in title_lower)
            )
            if is_poc:
                poc_lesson = L
                poc_lesson["_unit_slug"] = eu["slug"]
                t_safe = (L.get("title") or "").encode("ascii", errors="replace").decode("ascii")
                print(
                    f"  Known PoC lesson found: L{L['lesson_number']} '{t_safe}' "
                    f"(id={L['id'][:8]}...) -- will be preserved at lesson_number=2"
                )
            else:
                populated_lessons.append(
                    {
                        "unit": eu["slug"],
                        "lesson_number": L["lesson_number"],
                        "slug": L["slug"],
                    }
                )

if populated_lessons:
    print(
        f"\n  STOP: {len(populated_lessons)} unexpected lesson(s) have populated "
        f"content_html or practice_data (not the known PoC):"
    )
    for p in populated_lessons[:5]:
        print(f"    unit={p['unit']} L{p['lesson_number']} slug={p['slug']}")
    print("  Refusing to modify. Aborting.")
    sys.exit(2)

print("  No populated content found — safe to proceed.\n")

# ====================================================================
# STEP 1 — Rename / update unit rows
# ====================================================================

print("--- Step 1: Reconcile units ---")

unit_rows = {}  # slug -> row dict with 'id'

RENAME_MAP = {
    "listening": "western-classical-1650-1910",
}

for pu in PLAN_UNITS:
    slug = pu["slug"]
    plan_payload = {
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
    }

    if slug in units_by_slug:
        # Already exists with the right slug — just UPDATE metadata
        uid = units_by_slug[slug]["id"]
        sb.table("units").update(plan_payload).eq("id", uid).execute()
        unit_rows[slug] = {**units_by_slug[slug], **plan_payload}
        print(f"  UPDATED: {slug} (id={uid[:8]}...)")

    else:
        # Check if the old slug 'listening' exists and should be renamed
        old_slug = None
        for old, new in RENAME_MAP.items():
            if new == slug and old in units_by_slug:
                old_slug = old
                break

        if old_slug:
            uid = units_by_slug[old_slug]["id"]
            sb.table("units").update(plan_payload).eq("id", uid).execute()
            unit_rows[slug] = {**units_by_slug[old_slug], **plan_payload}
            print(f"  RENAMED + UPDATED: {old_slug} -> {slug} (id={uid[:8]}...)")
        else:
            # Insert fresh
            res = sb.table("units").insert({**plan_payload, "image_url": None}).execute()
            unit_rows[slug] = res.data[0]
            print(f"  INSERTED: {slug} (id={unit_rows[slug]['id'][:8]}...)")

# ====================================================================
# STEP 2 — Update the existing Mozart PoC lesson to lesson_number=2
# ====================================================================

print("\n--- Step 2: Re-number existing PoC Mozart lesson to lesson 2 ---")

unit_wc = unit_rows["western-classical-1650-1910"]
unit_wc_id = unit_wc["id"]

existing_lessons_wc = (
    sb.table("lessons")
    .select("id, lesson_number, slug, title")
    .eq("unit_id", unit_wc_id)
    .order("lesson_number")
    .execute()
    .data
)

print(f"  Existing lessons in {unit_wc_id[:8]}...: {len(existing_lessons_wc)}")
for el in existing_lessons_wc:
    t_safe = (el.get("title") or "").encode("ascii", errors="replace").decode("ascii")
    print(f"    L{el['lesson_number']} -- {t_safe} (id={el['id'][:8]}...)")

mozart_poc = None
# First check if the safety-check above already identified the PoC
if poc_lesson and poc_lesson.get("id"):
    # Confirm it's in the WC unit (after rename)
    for el in existing_lessons_wc:
        if el["id"] == poc_lesson["id"]:
            mozart_poc = el
            break
if not mozart_poc:
    # Fallback: scan by title
    for el in existing_lessons_wc:
        t = el["title"].lower()
        if "mozart" in t and ("40" in t or "symphony" in t):
            mozart_poc = el
            break
    if not mozart_poc and len(existing_lessons_wc) == 1:
        mozart_poc = existing_lessons_wc[0]

MOZART_LESSON_NUMBER = 2  # plan assigns Mozart Sym 40 as lesson 2

if mozart_poc:
    if mozart_poc["lesson_number"] != MOZART_LESSON_NUMBER:
        sb.table("lessons").update(
            {"lesson_number": MOZART_LESSON_NUMBER}
        ).eq("id", mozart_poc["id"]).execute()
        print(
            f"  Re-numbered Mozart PoC: L{mozart_poc['lesson_number']} -> L{MOZART_LESSON_NUMBER} "
            f"(id={mozart_poc['id'][:8]}...)"
        )
    else:
        print(
            f"  Mozart PoC already at L{MOZART_LESSON_NUMBER} — no change."
        )
    preserved_lesson_numbers_wc = {MOZART_LESSON_NUMBER}
else:
    print("  WARN: No Mozart PoC lesson found — will insert all WC shells fresh.")
    preserved_lesson_numbers_wc = set()

# ====================================================================
# STEP 3 — Insert missing lesson shells
# ====================================================================

print("\n--- Step 3: Insert missing lesson shells ---")

total_inserted = 0
total_skipped = 0
all_lesson_ids = {}  # (unit_slug, lesson_number) -> id

for pu in PLAN_UNITS:
    slug = pu["slug"]
    unit_id = unit_rows[slug]["id"]

    # Fetch current lessons after any re-numbering
    current_lessons = (
        sb.table("lessons")
        .select("id, lesson_number, slug, title")
        .eq("unit_id", unit_id)
        .execute()
        .data
    )
    nums_present = {L["lesson_number"]: L for L in current_lessons}
    used_slugs = {L["slug"] for L in current_lessons}

    # Record existing lessons in the master map
    for L in current_lessons:
        all_lesson_ids[(slug, L["lesson_number"])] = L["id"]

    new_in_unit = 0

    for L in pu["lessons"]:
        n = L["lesson_number"]

        if n in nums_present:
            # Already exists — skip but record its ID
            total_skipped += 1
            all_lesson_ids[(slug, n)] = nums_present[n]["id"]
            continue

        title = L["title"].strip()
        description = (L.get("description") or "").strip()[:300]

        base_slug = slugify(title) or f"lesson-{n}"
        lslug = base_slug
        i = 2
        while lslug in used_slugs:
            lslug = f"{base_slug}-{i}"
            i += 1
        used_slugs.add(lslug)

        res = sb.table("lessons").insert(
            {
                "unit_id": unit_id,
                "lesson_number": n,
                "slug": lslug,
                "title": title,
                "description": description,
                "status": "pending_review",
                "tier": "both",
                "content_html": None,
                "practice_data": None,
                "youtube_video_id": None,
            }
        ).execute()
        inserted_id = res.data[0]["id"]
        all_lesson_ids[(slug, n)] = inserted_id
        used_slugs.add(lslug)
        new_in_unit += 1
        total_inserted += 1

    print(
        f"  [{slug}] planned={len(pu['lessons'])} "
        f"inserted={new_in_unit} "
        f"skipped(present)={len(pu['lessons']) - new_in_unit}"
    )

print(f"\n  Total inserted: {total_inserted}  |  Skipped (already present): {total_skipped}")

# ====================================================================
# STEP 4 — Update subjects.settings (practice_units, lesson_count)
# ====================================================================

print("\n--- Step 4: Update subjects.settings ---")

existing_settings = dict(subj.get("settings") or {})

# Both units are practice format
practice_units = [pu["slug"] for pu in PLAN_UNITS]

# Preserve existing quote_ticker_html if it's already set
existing_settings["practice_units"] = practice_units

# Update unit_image_positions to include both units
uip = existing_settings.get("unit_image_positions") or {}
for pu in PLAN_UNITS:
    if pu["slug"] not in uip:
        uip[pu["slug"]] = "center center"
existing_settings["unit_image_positions"] = uip

sb.table("subjects").update({"settings": existing_settings}).eq("id", SUBJECT_ID).execute()
print(f"  settings.practice_units set to: {practice_units}")
print(f"  settings.unit_image_positions updated for all units")

# ====================================================================
# STEP 5 — Verify
# ====================================================================

print("\n--- Verification ---")

all_ok = True
total_in_db = 0
for pu in PLAN_UNITS:
    unit_id = unit_rows[pu["slug"]]["id"]
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", unit_id)
        .execute()
        .count
    )
    total_in_db += cnt
    status_str = "OK" if cnt == pu["lesson_count"] else f"MISMATCH (expected {pu['lesson_count']})"
    if cnt != pu["lesson_count"]:
        all_ok = False
    print(f"  {pu['slug']}: {cnt} lessons [{status_str}]")

print(f"\n  Total lessons: {total_in_db}  /  Expected: {sum(u['lesson_count'] for u in PLAN_UNITS)}")

# Print all lesson IDs for Phase 3 agent
print("\n--- Lesson UUIDs (for Phase 3) ---")
for pu in PLAN_UNITS:
    print(f"\n  Unit: {pu['slug']}")
    for L in pu["lessons"]:
        n = L["lesson_number"]
        key = (pu["slug"], n)
        lid = all_lesson_ids.get(key, "NOT FOUND")
        title_safe = L["title"][:60].encode("ascii", errors="replace").decode("ascii")
        print(f"    L{n:02d} {title_safe:<60} {lid}")

print()
final_settings = (
    sb.table("subjects")
    .select("settings")
    .eq("id", SUBJECT_ID)
    .execute()
    .data[0]["settings"]
)
print(f"  Final settings.practice_units: {final_settings.get('practice_units')}")

if all_ok:
    print(f"\n=== Phase 2 COMPLETE for {SUBJECT_SLUG} ===")
    print(f"  Subject UUID : {SUBJECT_ID}")
    print(f"  Units        : {len(unit_rows)}")
    print(f"  Lessons      : {total_in_db}")
else:
    print(f"\n  WARN: lesson count mismatch — check rows above")
    sys.exit(3)
