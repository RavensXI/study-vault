"""Generic Phase 2 activation script — takes a subject slug as argument.

Reads scripts/_plan_{slug}.json and creates:
  - 1 subjects row (status=live, school_id=null)
  - N units rows (article_units only for now; practice units handled separately)
  - All lesson shells (status=pending_review)
  - Activation report at scripts/_activation_report_{slug}.json

Idempotent guard: aborts if a subjects row with this slug already exists (school_id NULL).

Usage: python scripts/_activate_generic.py <subject-slug>
"""

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python scripts/_activate_generic.py <subject-slug>")
    sys.exit(1)

slug = sys.argv[1]
scripts_dir = Path(__file__).resolve().parent

sys.path.insert(0, str(scripts_dir))
from lib.supabase_client import get_client

plan = json.loads((scripts_dir / f"_plan_{slug}.json").read_text(encoding="utf-8"))
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]
assert SUBJECT_SLUG == slug, f"Slug mismatch: arg={slug} vs plan={SUBJECT_SLUG}"
SCHOOL_ID = None


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[''′']", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = sb.table("subjects").select("id, slug, status").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data
if existing:
    print(f"ERROR: subjects row with slug '{SUBJECT_SLUG}' already exists (id={existing[0]['id']}). Aborting.")
    sys.exit(1)
print("  Clean slate — proceeding with INSERT.")

unit_accents = [u["accent"] for u in plan["article_units"]]
quotes = plan.get("quote_ticker_quotes", [])
quote_items = []
for i, q in enumerate(quotes):
    color = unit_accents[i % len(unit_accents)] if unit_accents else "#1e40af"
    quote_items.append(
        f'<span class="quote-item" style="--q-color: {color};">{q["quote"]} '
        f'<em>&mdash; {q["author"]}</em></span>'
    )
quote_items_doubled = quote_items + quote_items
quote_ticker_html = (
    '<div class="quote-ticker"><div class="quote-ticker-track">'
    + "".join(quote_items_doubled)
    + "</div></div>"
)

practice_unit_slugs = [u["slug"] for u in plan.get("practice_units", [])]
settings = {
    "has_exam_guides": False,
    "practice_units": practice_unit_slugs,
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
    "image_url": None,
    "settings": settings,
}
res = sb.table("subjects").insert(subject_payload).execute()
SUBJECT_ID = res.data[0]["id"]
print(f"\n  Subject row INSERTED: {SUBJECT_ID}")

print(f"\n--- Inserting {len(plan['article_units'])} article units ---")
unit_rows = {}
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
        "image_url": None,
    }
    res = sb.table("units").insert(payload).execute()
    unit_rows[pu["slug"]] = res.data[0]
    print(f"  INSERTED unit {pu['sort_order']:2d}  [{pu['slug'][:55]}]  id={res.data[0]['id']}")

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
        s = base_slug
        i = 2
        while s in used_slugs:
            s = f"{base_slug}-{i}"
            i += 1
        used_slugs.add(s)
        sb.table("lessons").insert({
            "unit_id": unit_id,
            "lesson_number": n,
            "slug": s,
            "title": title,
            "description": description,
            "status": "pending_review",
            "tier": "both",
            "content_html": None,
            "youtube_video_id": None,
        }).execute()
        inserted_in_unit += 1
        total_inserted += 1
    print(f"  [{pu['slug'][:55]}] {inserted_in_unit} lessons")

# Verification
print("\n--- Verification ---")
db_total = 0
all_ok = True
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    cnt = sb.table("lessons").select("id", count="exact").eq("unit_id", unit_id).execute().count
    db_total += cnt
    ok = cnt == pu["lesson_count"]
    if not ok:
        all_ok = False
    status_str = "OK" if ok else f"MISMATCH (expected {pu['lesson_count']})"
    print(f"  {pu['slug'][:55]:55s}  {cnt:3d} lessons  [{status_str}]")

expected = sum(u["lesson_count"] for u in plan["article_units"])
print(f"\n  Total lessons : {db_total}  /  Expected : {expected}")

# UUID report
uuid_report = {"subject_id": SUBJECT_ID, "units": {}}
for pu in plan["article_units"]:
    u_row = unit_rows[pu["slug"]]
    lessons = sb.table("lessons").select("id, lesson_number, slug, title").eq("unit_id", u_row["id"]).order("lesson_number").execute().data
    uuid_report["units"][pu["slug"]] = {
        "unit_id": u_row["id"],
        "lessons": [{"id": L["id"], "number": L["lesson_number"], "slug": L["slug"], "title": L["title"]} for L in lessons]
    }

report_path = scripts_dir / f"_activation_report_{SUBJECT_SLUG}.json"
report_path.write_text(json.dumps(uuid_report, indent=2), encoding="utf-8")
print(f"\n  UUID report saved to {report_path.relative_to(scripts_dir.parent)}")

if all_ok and db_total == expected:
    print(f"\n=== DB activation COMPLETE for {SUBJECT_SLUG} ===")
    print(f"  Subject UUID : {SUBJECT_ID}")
    print(f"  Units        : {len(unit_rows)}")
    print(f"  Lessons      : {db_total}")
else:
    print(f"\n  WARN: verification failed — review output above")
    sys.exit(1)
