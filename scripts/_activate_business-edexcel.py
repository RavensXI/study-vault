"""Phase 2 - Subject activation for Business Studies (Pearson Edexcel 1BS0), free tier.

A placeholder business-edexcel subject row already exists from an earlier prototype
(2 placeholder units, 30 stub lessons). This script:

  1. UPDATES the subjects row to refresh metadata (name, color, spec_code,
     status='pending_review', is_active=true, settings = plan-derived dict).
     If the row does not exist (fresh install), inserts it.
  2. Reconciles the two units: existing units are updated in place to match
     the plan's slugs, body_classes and accents (rather than orphaning them).
     Lesson rows under the existing units are deleted before re-inserting
     fresh shells per the plan, because the prior lesson titles/groupings
     do not match the new plan and there are zero downstream references
     (lesson_visits, knowledge_check_scores both empty).
  3. INSERTS lesson shells (status pending_review, tier 'both') from the plan.

Idempotent: re-runs detect existing rows by slug and skip duplication.

Reads scripts/_plan_business-edexcel.json. Does NOT touch CSS / index.html /
wizard JS - those are separate Phase 2 steps.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads((scripts / "_plan_business-edexcel.json").read_text(encoding="utf-8"))
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]  # business-edexcel
SCHOOL_ID = None  # free tier


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[‘’′]", "", s)  # smart quotes
    s = re.sub(r"[–—]", "-", s)       # em/en dashes
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


# ============================================================ subject row

print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = (
    sb.table("subjects")
    .select("*")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .execute()
    .data
)

# Build settings: preserve quote_ticker_html if present, refresh question_type_names + flags.
quote_items = []
default_palette = [
    "#1d4ed8", "#be185d", "#0369a1", "#7c3aed",
    "#059669", "#be123c",
]
for i, q in enumerate(plan.get("quote_ticker_quotes", [])):
    color = default_palette[i % len(default_palette)]
    quote_items.append(
        f'<span class="quote-item" style="--q-color: {color};">{q["quote"]} '
        f'<em>— {q["author"]}</em></span>'
    )
# Duplicate first two to keep ticker animation seamless
if len(quote_items) >= 2:
    quote_items.extend(quote_items[:2])
quote_ticker_html = (
    '<div class="quote-ticker"><div class="quote-ticker-track">'
    + "".join(quote_items)
    + "</div></div>"
)

new_settings = {
    "has_exam_guides": False,
    "practice_units": [],
    "question_type_names": plan.get("question_type_names", []),
    "quote_ticker_html": quote_ticker_html,
    "unit_image_positions": {u["slug"]: "center" for u in plan["article_units"]},
}

subject_payload = {
    "name": plan["subject"]["name"],          # "Business"
    "slug": SUBJECT_SLUG,
    "exam_board": plan["subject"]["exam_board"],
    "spec_code": plan["subject"]["spec_code"],
    "school_id": SCHOOL_ID,
    "color": plan["subject"]["target_hero_colour"],  # #b45309
    "is_active": True,
    "status": "pending_review",
    "sort_order": 0,
    "settings": new_settings,
}

if existing:
    subject = existing[0]
    SUBJECT_ID = subject["id"]
    # Preserve any existing keys we did not explicitly redefine
    merged_settings = dict(subject.get("settings") or {})
    merged_settings.update(new_settings)
    subject_payload["settings"] = merged_settings
    sb.table("subjects").update(subject_payload).eq("id", SUBJECT_ID).execute()
    print(f"  subject row UPDATED in place: {SUBJECT_ID}")
else:
    res = sb.table("subjects").insert(subject_payload).execute()
    SUBJECT_ID = res.data[0]["id"]
    print(f"  subject row INSERTED: {SUBJECT_ID}")


# ============================================================ units

print(f"\n--- Reconciling {len(plan['article_units'])} units ---")

existing_units = (
    sb.table("units")
    .select("*")
    .eq("subject_id", SUBJECT_ID)
    .order("sort_order")
    .execute()
    .data
)

# Map plan units onto existing units by sort_order (placeholder convention used 1, 2)
plan_units_by_sort = {u["sort_order"]: u for u in plan["article_units"]}
existing_units_by_sort = {u["sort_order"]: u for u in existing_units}

unit_rows = {}  # slug -> row (after reconcile)
units_inserted = 0
units_updated = 0

for sort_order, pu in plan_units_by_sort.items():
    payload_unit = {
        "subject_id": SUBJECT_ID,
        "slug": pu["slug"],
        "name": pu["name"],
        "subtitle": pu["subtitle"],
        "body_class": pu["body_class"],
        "accent": pu["accent"],
        "accent_light": pu["accent_light"],
        "accent_badge": pu["accent_badge"],
        "lesson_count": pu["lesson_count"],
        "sort_order": pu["sort_order"],
    }

    # Try to match by slug first (fully idempotent re-run)
    by_slug = next(
        (u for u in existing_units if u["slug"] == pu["slug"]),
        None,
    )
    if by_slug:
        sb.table("units").update(payload_unit).eq("id", by_slug["id"]).execute()
        unit_rows[pu["slug"]] = {**by_slug, **payload_unit}
        units_updated += 1
        print(f"  UPDATED (by slug): sort={sort_order}  {pu['slug']}")
        continue

    # Otherwise, repurpose the placeholder unit at the same sort_order
    placeholder = existing_units_by_sort.get(sort_order)
    if placeholder:
        sb.table("units").update(payload_unit).eq("id", placeholder["id"]).execute()
        unit_rows[pu["slug"]] = {**placeholder, **payload_unit}
        units_updated += 1
        print(
            f"  UPDATED (repurposed placeholder): sort={sort_order}  "
            f"{placeholder['slug']} -> {pu['slug']}"
        )
    else:
        # Fresh insert
        # image_url left null - the auto-sync trigger fills it from L1 hero in Phase 4
        res = sb.table("units").insert({**payload_unit, "image_url": None}).execute()
        unit_rows[pu["slug"]] = res.data[0]
        units_inserted += 1
        print(f"  INSERTED: sort={sort_order}  {pu['slug']}")

print(f"\n  Units updated: {units_updated}, inserted: {units_inserted}")


# ============================================================ lesson shells

print(f"\n--- Reconciling lesson shells ---")

total_inserted = 0
total_deleted = 0
total_updated = 0

for pu in plan["article_units"]:
    unit_row = unit_rows[pu["slug"]]
    unit_id = unit_row["id"]

    existing_lessons = (
        sb.table("lessons")
        .select("id, lesson_number, slug, status, content_html")
        .eq("unit_id", unit_id)
        .execute()
        .data
    )

    plan_numbers = {L["number"] for L in pu["lessons"]}
    existing_numbers = {L["lesson_number"] for L in existing_lessons}

    # Delete any existing lessons whose lesson_number is not in the plan
    # (e.g. legacy stubs that don't align with the new plan)
    extras = [L for L in existing_lessons if L["lesson_number"] not in plan_numbers]
    for L in extras:
        sb.table("lessons").delete().eq("id", L["id"]).execute()
        total_deleted += 1
        print(f"  [{pu['slug']}] DELETED extra lesson L{L['lesson_number']} {L['slug']}")

    # Re-fetch after deletes for clean disambiguation
    existing_lessons = (
        sb.table("lessons")
        .select("id, lesson_number, slug, content_html")
        .eq("unit_id", unit_id)
        .execute()
        .data
    )
    by_number = {L["lesson_number"]: L for L in existing_lessons}
    used_slugs = {L["slug"] for L in existing_lessons}

    new_in_unit = 0
    refreshed_in_unit = 0
    for L in pu["lessons"]:
        n = L["number"]
        title = L["title"].strip()
        description = (L.get("description") or "").strip()[:300]

        base_slug = slugify(title) or f"lesson-{n}"
        slug = base_slug

        existing_lesson = by_number.get(n)
        if existing_lesson:
            # The plan is authoritative. If the existing slug does not match
            # the new title, assign a fresh slug (with collision-safe suffix).
            current_slug = existing_lesson.get("slug") or ""
            if current_slug == base_slug:
                slug = current_slug
            else:
                # New plan title -> new slug. Disambiguate against sibling slugs.
                slug = base_slug
                i = 2
                # Exclude this row's own slug from the collision set (we are renaming it)
                sibling_slugs = used_slugs - {current_slug}
                while slug in sibling_slugs:
                    slug = f"{base_slug}-{i}"
                    i += 1
                used_slugs.discard(current_slug)
                used_slugs.add(slug)

            update_payload = {
                "title": title,
                "description": description,
                "slug": slug,
                "status": "pending_review",
                "tier": "both",
                # Wipe stale content fields - the legacy rows had content for
                # different topics. Phase 3 will regenerate from the new plan.
                "content_html": None,
                "exam_tip_html": None,
                "conclusion_html": None,
                "hero_image_url": None,
                "hero_image_alt": None,
                "hero_image_position": None,
                "hero_image_caption": None,
                "narration_manifest": None,
                "practice_questions": None,
                "knowledge_checks": None,
                "glossary_terms": None,
                "diagrams": None,
                "related_media": None,
                "youtube_video_id": None,
                "flashcard_questions": None,
                "practice_data": None,
            }
            sb.table("lessons").update(update_payload).eq(
                "id", existing_lesson["id"]
            ).execute()
            refreshed_in_unit += 1
            total_updated += 1
            continue

        # Fresh insert: disambiguate slug if collision
        i = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{i}"
            i += 1
        used_slugs.add(slug)

        sb.table("lessons").insert(
            {
                "unit_id": unit_id,
                "lesson_number": n,
                "slug": slug,
                "title": title,
                "description": description,
                "status": "pending_review",
                "tier": "both",
            }
        ).execute()
        new_in_unit += 1
        total_inserted += 1

    print(
        f"  [{pu['slug']}] planned={len(pu['lessons'])} "
        f"new={new_in_unit} updated={refreshed_in_unit}"
    )

print(
    f"\n  Lessons inserted: {total_inserted}, "
    f"updated: {total_updated}, "
    f"deleted: {total_deleted}"
)


# ============================================================ verify

print("\n--- Verification ---")
total_in_db = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", unit_id)
        .execute()
        .count
    )
    total_in_db += cnt
    print(f"  {pu['slug']}: {cnt} lessons (planned {pu['lesson_count']})")

expected = sum(u["lesson_count"] for u in plan["article_units"])
print(f"\n  Lessons across new units: {total_in_db}  /  Expected: {expected}")

if total_in_db == expected:
    print(f"\n=== DB activation complete for {SUBJECT_SLUG} ===")
    print(f"  Subject id: {SUBJECT_ID}")
    print(f"  Units: {len(unit_rows)}")
    print(f"  Lessons: {total_in_db}")
else:
    print(f"\n  WARN: row count mismatch ({total_in_db} vs {expected})")
