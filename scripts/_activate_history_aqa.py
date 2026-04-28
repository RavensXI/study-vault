"""Phase 2 — Subject activation for History (AQA 8145), free tier.

Reads scripts/_plan_history-aqa.json and creates the subject + 16 units + 210
empty lesson shells in Supabase. Updates subjects.settings with quote ticker,
practice_units (empty), and unit_image_positions. Idempotent: if rows already
exist for this subject they are reused, not duplicated.

Does NOT touch index.html, css/style.css, vercel.json, or the Edexcel slug rename.
Those file edits run separately (they need careful pattern matching, not Supabase).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
master = json.loads((scripts / "_plan_history-aqa.json").read_text(encoding="utf-8"))
sb = get_client()

SUBJECT_SLUG = master["subject"]["slug"]  # history-aqa
SCHOOL_ID = None  # free tier


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


def lesson_num(L):
    return L.get("number") or L.get("lesson_number")


# ---------------------------------------------------------------- subject row

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
    print(f"  subject already exists: {subject['id']}")
else:
    quote_ticker_html = (
        '<div class="quote-ticker"><div class="quote-ticker-track">\n'
        + "\n".join(
            f'  <span class="quote-item" style="--q-color: {c};">'
            f'{q["quote"]} <em>&mdash; {q["author"]}</em></span>'
            for q, c in zip(
                master["quote_ticker_quotes"],
                ["#7f1d1d", "#1e3a8a", "#4d7c0f", "#9d174d", "#581c87", "#374151"],
            )
        )
        + "\n"
        + "\n".join(
            f'  <span class="quote-item" style="--q-color: {c};">'
            f'{q["quote"]} <em>&mdash; {q["author"]}</em></span>'
            for q, c in zip(
                master["quote_ticker_quotes"],
                ["#7f1d1d", "#1e3a8a", "#4d7c0f", "#9d174d", "#581c87", "#374151"],
            )
        )
        + "\n</div></div>"
    )

    settings = {
        "quote_ticker_html": quote_ticker_html,
        "practice_units": [],
        "unit_image_positions": {u["slug"]: "center" for u in master["article_units"]},
        "has_exam_guides": False,
        "options_picker": {
            "enabled": True,
            "sections": [
                {
                    "key": k,
                    "label": v["label"] if isinstance(v, dict) and "label" in v else "",
                    "pick": master["section_structure"][k]["pick"],
                    "options": master["section_structure"][k]["unit_slugs"],
                }
                for k, v in {
                    "paper_1_section_a_period_studies": {"label": "Period Study"},
                    "paper_1_section_b_wider_world_depth": {"label": "Wider World Depth"},
                    "paper_2_section_a_thematic": {"label": "Thematic Study"},
                    "paper_2_section_b_british_depth": {"label": "British Depth Study"},
                }.items()
            ],
        },
    }

    payload = {
        "school_id": SCHOOL_ID,
        "slug": SUBJECT_SLUG,
        "name": master["subject"]["name"],
        "exam_board": master["subject"]["exam_board"],
        "spec_code": master["subject"]["spec_code"],
        "color": master["subject"]["target_hero_colour"],
        "image_url": None,  # set after Unsplash hero pulled
        "status": "live",
        "is_active": True,
        "sort_order": 1,  # high priority — History is core for many students
        "settings": settings,
    }
    res = sb.table("subjects").insert(payload).execute()
    subject = res.data[0]
    print(f"  subject inserted: {subject['id']}")

SUBJECT_ID = subject["id"]


# ---------------------------------------------------------------- units

print(f"\n--- Inserting {len(master['article_units'])} units ---")

# Map slug -> existing unit row
existing_units = (
    sb.table("units").select("*").eq("subject_id", SUBJECT_ID).execute().data
)
units_by_slug = {u["slug"]: u for u in existing_units}

for unit in master["article_units"]:
    slug = unit["slug"]
    if slug in units_by_slug:
        print(f"  unit exists: {slug}")
        continue

    payload = {
        "subject_id": SUBJECT_ID,
        "slug": slug,
        "name": unit["name"],
        "subtitle": unit["subtitle"],
        "body_class": unit["body_class"],
        "accent": unit["accent"],
        "accent_light": unit["accent_light"],
        "accent_badge": unit["accent_badge"],
        "lesson_count": unit["lesson_count"],
        "sort_order": unit["sort_order"],
        "image_url": None,  # set after lesson 1 hero pulled
    }
    res = sb.table("units").insert(payload).execute()
    units_by_slug[slug] = res.data[0]
    print(f"  unit inserted: {slug:40s} ({unit['lesson_count']} lessons)")


# ---------------------------------------------------------------- lesson shells

print(f"\n--- Inserting empty lesson shells ---")

inserted = 0
skipped = 0
for unit in master["article_units"]:
    unit_row = units_by_slug[unit["slug"]]
    unit_id = unit_row["id"]

    # Existing lessons in this unit
    existing_lessons = (
        sb.table("lessons")
        .select("id, lesson_number, slug")
        .eq("unit_id", unit_id)
        .execute()
        .data
    )
    nums_present = {L["lesson_number"] for L in existing_lessons}

    for L in unit["lessons"]:
        n = lesson_num(L)
        if n in nums_present:
            skipped += 1
            continue

        title = L.get("title") or "Untitled"
        slug = slugify(title)
        description = (L.get("description") or "")[:300]

        payload = {
            "unit_id": unit_id,
            "lesson_number": n,
            "slug": slug,
            "title": title,
            "description": description,
            "status": "pending_review",
        }
        sb.table("lessons").insert(payload).execute()
        inserted += 1

    print(
        f"  {unit['slug']:40s} {unit['lesson_count']:>2} planned, "
        f"{inserted - sum((u['lesson_count'] if u['slug'] != unit['slug'] else 0) for u in master['article_units']):>3} new (skipped existing)"
    )

print(f"\n  Inserted {inserted} lesson shells; skipped {skipped} (already present)")


# ---------------------------------------------------------------- final check

actual_total = 0
for unit in master["article_units"]:
    unit_id = units_by_slug[unit["slug"]]["id"]
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", unit_id)
        .execute()
        .count
    )
    actual_total += cnt
print(f"\n  Final count in DB: {actual_total} lessons across 16 units")
print(f"  Expected from plan: {sum(u['lesson_count'] for u in master['article_units'])} lessons")

if actual_total != sum(u["lesson_count"] for u in master["article_units"]):
    print("  ⚠  MISMATCH — investigate before Phase 3")
else:
    print(f"\n=== DB activation complete for {SUBJECT_SLUG} ===")
    print(f"\nNext steps:")
    print("  1. Edit css/style.css to add 16 dark-mode unit accent rules")
    print("  2. Append history-aqa to SUBJECT_ORDER in scripts/generate_cinematic_videos.py")
    print("  3. Pull Unsplash subject hero to images/subject-history-aqa.jpg")
    print("  4. (Deferred) Edexcel slug rename + homepage card / wizard picker — task #9")
