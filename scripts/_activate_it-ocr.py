"""Phase 2 — Subject activation for Information Technology (OCR J836), free tier.

Reads scripts/_plan_it-ocr.json and creates:
  - 1 subjects row (status=live, school_id=null)
  - 3 units rows (sort_order 1..3)
  - 14 empty lesson shells (status=pending_review)

Idempotent: if the subject row already exists AND any lesson has
content_html or practice_questions populated, the script aborts WITHOUT
modifying anything.

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
    (scripts / "_plan_it-ocr.json").read_text(encoding="utf-8")
)
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]  # it-ocr
SCHOOL_ID = None  # free tier


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[''′]", "", s)        # smart quotes
    s = re.sub(r"[–—]", "-", s)        # en/em dashes
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


# ============================================================ stop-condition

print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = (
    sb.table("subjects")
    .select("*")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .execute()
    .data
)

if existing:
    subject = existing[0]
    SUBJECT_ID = subject["id"]
    units_check = (
        sb.table("units").select("id, slug").eq("subject_id", SUBJECT_ID).execute().data
    )
    populated = []
    total_lessons = 0
    for u in units_check:
        lrows = (
            sb.table("lessons")
            .select("id, lesson_number, slug, content_html, practice_questions")
            .eq("unit_id", u["id"])
            .execute()
            .data
        )
        total_lessons += len(lrows)
        for L in lrows:
            if L.get("content_html") or L.get("practice_questions"):
                populated.append(
                    {
                        "unit": u["slug"],
                        "lesson_number": L["lesson_number"],
                        "slug": L["slug"],
                        "has_content_html": bool(L.get("content_html")),
                        "has_practice_questions": bool(L.get("practice_questions")),
                    }
                )

    if populated:
        print(f"  STOP: subject row {SUBJECT_ID[:8]}... already exists AND")
        print(f"  {len(populated)} of {total_lessons} lessons have populated content.")
        print("  Refusing to modify. Sample:")
        for p in populated[:5]:
            print(f"    {p}")
        sys.exit(2)

    print(f"  Subject row exists ({SUBJECT_ID[:8]}...) with {total_lessons} empty")
    print("  lesson shells. Safe to UPDATE metadata + INSERT missing shells.")
else:
    SUBJECT_ID = None
    print(f"  Clean slate — no existing {SUBJECT_SLUG} row. Will INSERT.")


# ============================================================ build settings

# 3 unit accent colours — cycle across them for the 6 quotes, then duplicate
# the full sequence once for a seamless scroll loop.
unit_accents = [
    plan["article_units"][0]["accent"],   # #1e40af  (IT in the Digital World)
    plan["article_units"][1]["accent"],   # #0f766e  (Data Manipulation with Spreadsheets)
    plan["article_units"][2]["accent"],   # #7c3aed  (Augmented Reality Design)
]
quotes = plan.get("quote_ticker_quotes", [])
quote_items = []
for i, q in enumerate(quotes):
    color = unit_accents[i % len(unit_accents)]
    quote_items.append(
        f'<span class="quote-item" style="--q-color: {color};">{q["quote"]} '
        f'<em>&mdash; {q["author"]}</em></span>'
    )
# duplicate full sequence once for seamless loop
quote_items_doubled = quote_items + quote_items
quote_ticker_html = (
    '<div class="quote-ticker"><div class="quote-ticker-track">'
    + "".join(quote_items_doubled)
    + "</div></div>"
)

new_settings = {
    "has_exam_guides": False,
    "practice_units": [],
    "question_type_names": plan.get("question_type_names", []),
    "quote_ticker_html": quote_ticker_html,
    "unit_image_positions": {
        u["slug"]: "center center" for u in plan["article_units"]
    },
}


# ============================================================ subject row

subject_payload = {
    "name": plan["subject"]["name"],
    "slug": SUBJECT_SLUG,
    "exam_board": plan["subject"]["exam_board"],
    "spec_code": plan["subject"]["spec_code"],
    "school_id": SCHOOL_ID,
    "color": plan["subject"]["target_hero_colour"],
    "is_active": True,
    "status": "live",
    "sort_order": 1,
    "settings": new_settings,
    "image_url": None,
}

if SUBJECT_ID:
    merged_settings = dict(subject.get("settings") or {})
    merged_settings.update(new_settings)
    subject_payload["settings"] = merged_settings
    sb.table("subjects").update(subject_payload).eq("id", SUBJECT_ID).execute()
    print(f"\n  subject row UPDATED: {SUBJECT_ID}")
else:
    res = sb.table("subjects").insert(subject_payload).execute()
    SUBJECT_ID = res.data[0]["id"]
    print(f"\n  subject row INSERTED: {SUBJECT_ID}")


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
units_by_slug = {u["slug"]: u for u in existing_units}

unit_rows = {}
for pu in plan["article_units"]:
    slug = pu["slug"]
    payload_unit = {
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
        sb.table("units").update(payload_unit).eq(
            "id", units_by_slug[slug]["id"]
        ).execute()
        unit_rows[slug] = {**units_by_slug[slug], **payload_unit}
        print(f"  UPDATED: {slug:52s} ({pu['lesson_count']} lessons)")
    else:
        res = sb.table("units").insert({**payload_unit, "image_url": None}).execute()
        unit_rows[slug] = res.data[0]
        print(f"  INSERTED: {slug:52s} ({pu['lesson_count']} lessons)")


# ============================================================ lesson shells

print("\n--- Inserting lesson shells ---")

total_inserted = 0
total_skipped = 0
for pu in plan["article_units"]:
    unit_row = unit_rows[pu["slug"]]
    unit_id = unit_row["id"]

    existing_lessons = (
        sb.table("lessons")
        .select("id, lesson_number, slug")
        .eq("unit_id", unit_id)
        .execute()
        .data
    )
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

        sb.table("lessons").insert(
            {
                "unit_id": unit_id,
                "lesson_number": n,
                "slug": slug,
                "title": title,
                "description": description,
                "status": "pending_review",
                "tier": "both",
                "youtube_video_id": None,
            }
        ).execute()
        new_in_unit += 1
        total_inserted += 1

    print(
        f"  [{pu['slug']}] planned={len(pu['lessons'])} "
        f"new={new_in_unit} "
        f"skipped(already present)={len(pu['lessons']) - new_in_unit}"
    )

print(f"\n  Lessons inserted: {total_inserted}, skipped: {total_skipped}")


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
    status = "OK" if cnt == pu["lesson_count"] else "MISMATCH"
    print(f"  {pu['slug']}: {cnt} lessons (planned {pu['lesson_count']}) [{status}]")

expected = sum(u["lesson_count"] for u in plan["article_units"])
print(f"\n  Lessons total: {total_in_db}  /  Expected: {expected}")

if total_in_db == expected:
    print(f"\n=== DB activation complete for {SUBJECT_SLUG} ===")
    print(f"  Subject id : {SUBJECT_ID}")
    print(f"  Units      : {len(unit_rows)}")
    print(f"  Lessons    : {total_in_db}")
else:
    print(f"\n  WARN: row count mismatch ({total_in_db} vs {expected})")
    sys.exit(3)
