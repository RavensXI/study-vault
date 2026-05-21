"""Build 2 batches for HSC Eduqas/WJEC (one per unit).

Unit 1 (Growth, Development & Influences) — 7 lessons → batch b1
Unit 2 (Self-Concept, Measuring Health & Promoting Wellbeing) — 6 lessons → batch b2
"""
import json, re, sys
from pathlib import Path

here = Path(__file__).resolve().parent
plan = json.loads((here.parent / "_plan_health-social-care-eduqas.json").read_text(encoding="utf-8"))

subject_meta = {
    "name": plan["subject"]["name"],
    "slug": plan["subject"]["slug"],
    "exam_board": plan["subject"]["exam_board"],
    "target_audience": "free-tier",
    "qualification_type": "level-1-2-vocational-award",
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

global_idx = 0
for batch_i, unit in enumerate(plan["article_units"], start=1):
    batch_id = f"b{batch_i}"
    unit_meta = {
        "name": unit["name"],
        "slug": unit["slug"],
        "subtitle": unit["subtitle"],
        "accent": unit["accent"],
        "accent_light": unit["accent_light"],
        "accent_badge": unit["accent_badge"],
        "body_class": unit["body_class"],
        "lesson_count": unit["lesson_count"],
    }
    lessons_in_batch = []
    for L in unit["lessons"]:
        global_idx += 1
        ct = L.get("content_transfer") or {}
        port_source = None
        if ct.get("source_subject_slug") and ct.get("source_lesson_number") is not None:
            port_source = f"scripts/_content_health-social-care-eduqas/_source_lessons/{global_idx:02d}.json"
        lessons_in_batch.append({
            "number": L["number"],
            "title": L["title"],
            "slug": slugify(L["title"]),
            "description": L["description"],
            "spec_references": L["spec_references"],
            "section_markers": L["section_markers"],
            "port_source_path": port_source,
            "transfer_score": ct.get("transfer_score", "fresh"),
            "adaptation_notes": ct.get("adaptation_notes", ""),
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
    print(f"  wrote {out.name}  unit={unit['slug']}  lessons={[L['number'] for L in unit['lessons']]}")
