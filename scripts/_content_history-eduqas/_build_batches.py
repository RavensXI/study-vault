"""Build 16 batch files — one per Eduqas History pathway."""
import json, re
from pathlib import Path

here = Path(__file__).resolve().parent
plan = json.loads((here.parent / "_plan_history-eduqas.json").read_text(encoding="utf-8"))

subject_meta = {
    "name": plan["subject"]["name"],
    "slug": plan["subject"]["slug"],
    "exam_board": plan["subject"]["exam_board"],
    "target_audience": "free-tier",
}
teaching_brief = plan.get("teaching_brief", {})
question_type_names = plan.get("question_type_names", [])
reference_lesson_path = "scripts/_content_business-edexcel/_reference_lesson.json"

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]

for i, unit in enumerate(plan["article_units"], start=1):
    batch_id = f"b{i:02d}"
    unit_meta = {
        "name": unit["name"],
        "slug": unit["slug"],
        "subtitle": unit["subtitle"],
        "accent": unit["accent"],
        "accent_light": unit["accent_light"],
        "accent_badge": unit["accent_badge"],
        "body_class": unit["body_class"],
        "lesson_count": unit["lesson_count"],
        "pathway_category": unit.get("pathway_category", "?"),
        "option_letter": unit.get("option_letter", "?"),
        "component": unit.get("component", 0),
    }
    lessons_in_batch = []
    for L in unit["lessons"]:
        ct = L.get("content_transfer") or {}
        lessons_in_batch.append({
            "number": L["number"],
            "title": L["title"],
            "slug": slugify(L["title"]),
            "description": L["description"],
            "spec_references": L.get("spec_references", []),
            "section_markers": L.get("section_markers", []),
            "transfer_score": ct.get("transfer_score", "fresh"),
            "adaptation_notes": ct.get("adaptation_notes", ""),
            "source_subject_slug": ct.get("source_subject_slug"),
            "source_unit_slug": ct.get("source_unit_slug"),
            "source_lesson_number": ct.get("source_lesson_number"),
        })
    batch = {
        "batch_id": batch_id,
        "subject": subject_meta,
        "unit": unit_meta,
        "reference_lesson_path": reference_lesson_path,
        "subject_level_teaching_brief": teaching_brief,
        "registered_question_type_names": question_type_names,
        "allowed_question_types_for_this_unit": question_type_names,
        "lessons_in_batch": lessons_in_batch,
    }
    out = here / f"_batch_{batch_id}.json"
    out.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  wrote {out.name}  [{unit_meta['option_letter']}] {unit['name'][:50]:50s} ({len(unit['lessons'])} lessons)")
