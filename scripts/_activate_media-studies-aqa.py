"""Phase 2 — Subject activation for Media Studies (AQA 8572), free tier.

Inserts a brand-new subjects row (slug media-studies-aqa), 5 units and
23 lesson shells. Aborts if the subjects row already exists (idempotent
guard per memory/feedback_dont_wipe_existing_supabase_rows.md).

Reads scripts/_plan_media-studies-aqa.json.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads((scripts / "_plan_media-studies-aqa.json").read_text(encoding="utf-8"))
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]  # media-studies-aqa
SCHOOL_ID = None  # free tier


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"['‘’′]", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


# ============================================================ guard
print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = (
    sb.table("subjects")
    .select("id, slug")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .execute()
    .data
)
if existing:
    print(
        f"ERROR: subjects row with slug '{SUBJECT_SLUG}' already exists "
        f"(id={existing[0]['id']}). Aborting to avoid overwriting existing data."
    )
    sys.exit(1)

# ============================================================ quote ticker HTML
unit_accents = [u["accent"] for u in plan["article_units"]]
quote_items_html = []
for i, q in enumerate(plan.get("quote_ticker_quotes", [])):
    color = unit_accents[i % len(unit_accents)]
    quote_items_html.append(
        f'<span class="quote-item" style="--q-color: {color};">{q["quote"]} '
        f'<em>&mdash; {q["author"]}</em></span>'
    )
# Duplicate the sequence once for seamless scroll animation
quote_items_html_doubled = quote_items_html + quote_items_html
quote_ticker_html = (
    '<div class="quote-ticker"><div class="quote-ticker-track">'
    + "".join(quote_items_html_doubled)
    + "</div></div>"
)

# ============================================================ subject row
settings = {
    "has_exam_guides": False,
    "practice_units": [],
    "question_type_names": plan.get("question_type_names", []),
    "quote_ticker_html": quote_ticker_html,
    "unit_image_positions": {u["slug"]: "center center" for u in plan["article_units"]},
}

subject_payload = {
    "name": plan["subject"]["name"],
    "slug": SUBJECT_SLUG,
    "exam_board": plan["subject"]["exam_board"],
    "spec_code": plan["subject"]["spec_code"],
    "school_id": SCHOOL_ID,
    "color": plan["subject"]["target_hero_colour"],
    "is_active": True,
    "status": "live",
    "sort_order": 0,
    "settings": settings,
}

res = sb.table("subjects").insert(subject_payload).execute()
SUBJECT_ID = res.data[0]["id"]
print(f"  subject row INSERTED: {SUBJECT_ID}")

# ============================================================ units
print(f"\n--- Inserting {len(plan['article_units'])} units ---")

unit_rows = {}  # slug -> row
for pu in plan["article_units"]:
    payload = {
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
        "image_url": None,  # auto-syncs from L1 hero via Postgres trigger in Phase 4
    }
    res = sb.table("units").insert(payload).execute()
    unit_rows[pu["slug"]] = res.data[0]
    print(f"  INSERTED unit sort={pu['sort_order']}: {pu['slug']}")

# ============================================================ lesson shells
print(f"\n--- Inserting lesson shells ---")

total_inserted = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    used_slugs: set[str] = set()
    inserted_in_unit = 0

    for L in pu["lessons"]:
        n = L["number"]
        title = L["title"].strip()
        description = (L.get("description") or "").strip()[:300]

        base_slug = slugify(title) or f"lesson-{n}"
        slug = base_slug
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
                "content_html": None,
                "youtube_video_id": None,
            }
        ).execute()
        inserted_in_unit += 1
        total_inserted += 1

    print(f"  [{pu['slug']}] inserted {inserted_in_unit} lessons")

# ============================================================ verify
print("\n--- Verification ---")
db_total = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", unit_id)
        .execute()
        .count
    )
    db_total += cnt
    status = "OK" if cnt == pu["lesson_count"] else f"MISMATCH (expected {pu['lesson_count']})"
    print(f"  {pu['slug']}: {cnt} lessons — {status}")

expected = sum(u["lesson_count"] for u in plan["article_units"])
print(f"\n  Total lessons: {db_total}  /  Expected: {expected}")

subj_row = sb.table("subjects").select("id, status, school_id").eq("id", SUBJECT_ID).execute().data[0]
print(f"  subjects.status = {subj_row['status']}")
print(f"  subjects.school_id = {subj_row['school_id']}")

if db_total == expected and subj_row["status"] == "live" and subj_row["school_id"] is None:
    print(f"\n=== DB activation COMPLETE for {SUBJECT_SLUG} ===")
    print(f"  Subject UUID : {SUBJECT_ID}")
    print(f"  Units        : {len(unit_rows)}")
    print(f"  Lessons      : {db_total}")
else:
    print(f"\n  WARN: verification failed — check rows above")
    sys.exit(1)
