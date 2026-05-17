"""Phase 2 — Subject activation for Edexcel GCSE Religious Studies A (1RA0), free tier.

Reads scripts/_plan_religious-studies-edexcel.json and creates:
  - 1 subjects row (status=live, school_id=null)
  - 15 units rows (sort_order 1..15)
  - 71 empty lesson shells (status=pending_review)

Idempotent guard: if a subject row with slug 'religious-studies-edexcel' already
exists (school_id NULL) the script ABORTS without modifying anything
(per memory/feedback_dont_wipe_existing_supabase_rows.md).

Does NOT touch index.html, css/style.css, or any other subject's data.
Those are handled separately in this activation run.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads(
    (scripts / "_plan_religious-studies-edexcel.json").read_text(encoding="utf-8")
)
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]   # religious-studies-edexcel
SCHOOL_ID = None                          # free tier


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[''′']", "", s)        # smart/curly quotes
    s = re.sub(r"[–—]", "-", s)        # en/em dashes
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


# ============================================================ abort guard
print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = (
    sb.table("subjects")
    .select("id, slug, status")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .execute()
    .data
)

if existing:
    print(
        f"ERROR: subjects row with slug '{SUBJECT_SLUG}' already exists "
        f"(id={existing[0]['id']}, status={existing[0]['status']}). "
        "Aborting to avoid overwriting existing data."
    )
    sys.exit(1)

print(f"  Clean slate — no existing '{SUBJECT_SLUG}' row. Proceeding with INSERT.")


# ============================================================ quote ticker HTML
# 6 quotes from plan, cycling across the 15 unit accents, doubled for seamless scroll.
unit_accents = [u["accent"] for u in plan["article_units"]]
quotes = plan.get("quote_ticker_quotes", [])
quote_items = []
for i, q in enumerate(quotes):
    color = unit_accents[i % len(unit_accents)]
    quote_items.append(
        f'<span class="quote-item" style="--q-color: {color};">{q["quote"]} '
        f'<em>&mdash; {q["author"]}</em></span>'
    )
# Duplicate for seamless loop
quote_items_doubled = quote_items + quote_items
quote_ticker_html = (
    '<div class="quote-ticker"><div class="quote-ticker-track">'
    + "".join(quote_items_doubled)
    + "</div></div>"
)


# ============================================================ subject row
# Edexcel RS option structure:
#   paper1: one of catholic-christianity, christianity, islam
#   paper2: one of catholic-christianity, christianity, islam, buddhism,
#           hinduism, judaism, sikhism
#   paper3/4 derive from paper1 choice (auto-derive, not user-pickable in wizard)
settings = {
    "has_exam_guides": False,
    "practice_units": [],
    "question_type_names": plan.get("question_type_names", []),
    "quote_ticker_html": quote_ticker_html,
    "unit_image_positions": {
        u["slug"]: "center center" for u in plan["article_units"]
    },
    "options": {
        "paper1": {
            "label": "Paper 1 religion",
            "helper": "The religion studied in depth for Paper 1 (includes Sources of Wisdom and Forms of Expression)",
            "required": True,
            "choices": [
                {"slug": "paper-1-catholic-christianity", "name": "Catholic Christianity"},
                {"slug": "paper-1-christianity", "name": "Christianity"},
                {"slug": "paper-1-islam", "name": "Islam"},
            ],
        },
        "paper2": {
            "label": "Paper 2 religion",
            "helper": "A second religion studied for Paper 2 (must be different from Paper 1 — Catholic and general Christianity cannot be combined)",
            "required": True,
            "choices": [
                {"slug": "paper-2-catholic-christianity", "name": "Catholic Christianity"},
                {"slug": "paper-2-christianity", "name": "Christianity"},
                {"slug": "paper-2-islam", "name": "Islam"},
                {"slug": "paper-2-buddhism", "name": "Buddhism"},
                {"slug": "paper-2-hinduism", "name": "Hinduism"},
                {"slug": "paper-2-judaism", "name": "Judaism"},
                {"slug": "paper-2-sikhism", "name": "Sikhism"},
            ],
        },
        # Paper 3 / Paper 4 derive from the Paper 1 choice:
        #   Catholic → paper-3-philosophy-ethics-catholic (+ paper-4-marks-gospel available)
        #   Christianity → paper-3-philosophy-ethics-christianity (+ paper-4-marks-gospel available)
        #   Islam → paper-3-philosophy-ethics-islam (+ paper-4-quran available)
        # The browse-loader filters these using the paper1 saved pref.
        "paper3_map": {
            "paper-1-catholic-christianity": "paper-3-philosophy-ethics-catholic",
            "paper-1-christianity": "paper-3-philosophy-ethics-christianity",
            "paper-1-islam": "paper-3-philosophy-ethics-islam",
        },
        "paper4_map": {
            "paper-1-catholic-christianity": "paper-4-marks-gospel",
            "paper-1-christianity": "paper-4-marks-gospel",
            "paper-1-islam": "paper-4-quran",
        },
    },
}

subject_payload = {
    "name": plan["subject"]["name"],           # Religious Studies
    "slug": SUBJECT_SLUG,                       # religious-studies-edexcel
    "exam_board": plan["subject"]["exam_board"],# Edexcel
    "spec_code": plan["subject"]["spec_code"],  # 1RA0
    "school_id": SCHOOL_ID,                     # NULL
    "color": plan["subject"]["target_hero_colour"],  # #7c2d12
    "is_active": True,
    "status": "live",
    "sort_order": 0,
    "image_url": None,
    "settings": settings,
}

res = sb.table("subjects").insert(subject_payload).execute()
SUBJECT_ID = res.data[0]["id"]
print(f"\n  Subject row INSERTED: {SUBJECT_ID}")


# ============================================================ units
print(f"\n--- Inserting {len(plan['article_units'])} units ---")

unit_rows = {}  # slug -> inserted row

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
        "image_url": None,   # auto-syncs from L1 hero via Postgres trigger in Phase 4
    }
    res = sb.table("units").insert(payload).execute()
    unit_rows[pu["slug"]] = res.data[0]
    print(
        f"  INSERTED unit {pu['sort_order']:2d}  [{pu['slug'][:55]}]  "
        f"id={res.data[0]['id']}"
    )


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

    print(f"  [{pu['slug'][:55]}] {inserted_in_unit} lessons")


# ============================================================ verification
print("\n--- Verification ---")
db_total = 0
all_ok = True

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
    ok = cnt == pu["lesson_count"]
    if not ok:
        all_ok = False
    status_str = "OK" if ok else f"MISMATCH (expected {pu['lesson_count']})"
    print(f"  {pu['slug'][:55]:55s}  {cnt:3d} lessons  [{status_str}]")

expected = sum(u["lesson_count"] for u in plan["article_units"])
print(f"\n  Total lessons : {db_total}  /  Expected : {expected}")

subj_row = (
    sb.table("subjects")
    .select("id, status, school_id")
    .eq("id", SUBJECT_ID)
    .execute()
    .data[0]
)
print(f"  subjects.status    = {subj_row['status']}")
print(f"  subjects.school_id = {subj_row['school_id']}")


# ============================================================ UUID report
print("\n--- Unit + Lesson UUIDs ---")
for pu in plan["article_units"]:
    u_row = unit_rows[pu["slug"]]
    print(f"\n  Unit {pu['sort_order']:2d}: {pu['name']}")
    print(f"    slug    : {pu['slug']}")
    print(f"    unit_id : {u_row['id']}")

    lessons = (
        sb.table("lessons")
        .select("id, lesson_number, slug, title")
        .eq("unit_id", u_row["id"])
        .order("lesson_number")
        .execute()
        .data
    )
    for L in lessons:
        print(f"      L{L['lesson_number']:02d}  {L['id']}  {L['slug']}")


# ============================================================ final status
if all_ok and db_total == expected and subj_row["status"] == "live" and subj_row["school_id"] is None:
    print(f"\n=== DB activation COMPLETE for {SUBJECT_SLUG} ===")
    print(f"  Subject UUID : {SUBJECT_ID}")
    print(f"  Units        : {len(unit_rows)}")
    print(f"  Lessons      : {db_total}")
else:
    print(f"\n  WARN: verification failed — review output above")
    sys.exit(1)
