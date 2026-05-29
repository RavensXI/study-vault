"""Phase 3 prep — build per-unit content batch files for Food Preparation and
Nutrition (AQA 8585), free tier.

Reads the plan JSON + the live Supabase lesson rows (for lesson_id + the slug
that activation generated) and writes one self-contained batch file per unit to
scripts/_content_food-preparation-and-nutrition-aqa/_batch_u{N}.json.

Each unit has <=5 lessons, comfortably under the 10-lesson-per-agent cap, so one
batch == one unit == one content agent.

Content agents have NO DB access — everything they need is embedded in the batch
file (subject/unit metadata, teaching brief, registered question types, and the
per-lesson briefs with lesson_id + verbatim slug).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

SCRIPTS = Path(__file__).resolve().parent
CONTENT_DIR = SCRIPTS / "_content_food-preparation-and-nutrition-aqa"
PLAN = json.loads((SCRIPTS / "_plan_food-preparation-and-nutrition-aqa.json").read_text(encoding="utf-8"))

SUBJECT_SLUG = PLAN["subject"]["slug"]
QTYPES = PLAN["question_type_names"]

sb = get_client()

subj = (
    sb.table("subjects").select("id, name, slug, exam_board, spec_code")
    .eq("slug", SUBJECT_SLUG).is_("school_id", "null").single().execute().data
)
SUBJECT_ID = subj["id"]

# Build quote-ticker html the same way activation did (so the agent can echo it
# into per-unit context if needed) — pull it back from settings to stay in sync.
settings = (
    sb.table("subjects").select("settings").eq("id", SUBJECT_ID).single().execute().data["settings"]
)
quote_ticker_html = settings.get("quote_ticker_html", "")

units = (
    sb.table("units").select("id, slug, name, subtitle, accent, accent_light, accent_badge, body_class, lesson_count, sort_order")
    .eq("subject_id", SUBJECT_ID).order("sort_order").execute().data
)

plan_units_by_slug = {u["slug"]: u for u in PLAN["article_units"]}

written = []
for u in units:
    plan_u = plan_units_by_slug[u["slug"]]
    lessons = (
        sb.table("lessons").select("id, lesson_number, slug, title, description")
        .eq("unit_id", u["id"]).order("lesson_number").execute().data
    )
    # Map plan lesson briefs (section_markers, spec_references) by number
    plan_lessons_by_num = {pl["number"]: pl for pl in plan_u["lessons"]}

    lessons_in_batch = []
    for L in lessons:
        pl = plan_lessons_by_num.get(L["lesson_number"], {})
        lessons_in_batch.append({
            "lesson_id": L["id"],
            "lesson_number": L["lesson_number"],
            "slug": L["slug"],
            "title": L["title"],
            "description": L["description"],
            "spec_references": pl.get("spec_references", []),
            "section_markers": pl.get("section_markers", []),
            "suggested_question_types": QTYPES,
        })

    batch_id = f"u{u['sort_order']}"
    batch = {
        "batch_id": batch_id,
        "subject": {
            "name": subj["name"],
            "slug": SUBJECT_SLUG,
            "exam_board": subj["exam_board"],
            "spec_code": subj["spec_code"],
            "target_audience": "free-tier",
        },
        "unit": {
            "name": u["name"],
            "slug": u["slug"],
            "subtitle": u["subtitle"],
            "accent": u["accent"],
            "accent_light": u["accent_light"],
            "accent_badge": u["accent_badge"],
            "body_class": u["body_class"],
            "lesson_count": u["lesson_count"],
        },
        "spec_slice_path": "scripts/_content_food-preparation-and-nutrition-aqa/_spec_food-preparation-and-nutrition.txt",
        "reference_lesson_path": "scripts/_content_food-preparation-and-nutrition-aqa/_reference_lesson.json",
        "subject_level_teaching_brief": PLAN["teaching_brief"],
        "unit_level_teaching_brief": {},
        "quote_ticker_html_for_unit": quote_ticker_html,
        "registered_question_type_names": QTYPES,
        "allowed_question_types_for_this_unit": QTYPES,
        "lessons_in_batch": lessons_in_batch,
        "output_dir": "scripts/_content_food-preparation-and-nutrition-aqa/lessons",
    }

    out = CONTENT_DIR / f"_batch_{batch_id}.json"
    out.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
    written.append((batch_id, u["slug"], len(lessons_in_batch)))
    print(f"  wrote {out.name}: unit={u['slug']} lessons={len(lessons_in_batch)}")

print(f"\n  {len(written)} batch files written. Total lessons: {sum(w[2] for w in written)}")
