"""Build 3 batch files (4 lessons each) for the Phase 3 content agents.

Each batch JSON contains:
  - Subject + unit metadata (from plan)
  - subject_level_teaching_brief copied verbatim from plan
  - registered_question_type_names (must match getGuideUrl mappings)
  - lessons_in_batch: per-lesson port_source path + adaptation_notes from plan
  - reference_lesson_path (pinned RE L01 from REFERENCE_LESSONS.md)
"""
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
plan = json.loads(
    (here.parent / "_plan_cambridge-nationals-enterprise-and-marketing.json").read_text(encoding="utf-8")
)

unit = plan["article_units"][0]
subject_meta = {
    "name": plan["subject"]["name"],
    "slug": plan["subject"]["slug"],
    "exam_board": plan["subject"]["exam_board"],
    "target_audience": "free-tier",
    "qualification_type": "cambridge-national-l1-l2",
}
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

teaching_brief = plan.get("teaching_brief", {})
question_type_names = plan.get("question_type_names", [])

reference_lesson_path = "scripts/_content_business-edexcel/_reference_lesson.json"
# Re-using business-edexcel's reference lesson as the structural shape — it's
# the most similar in tone/content already on disk. RE L01 "Worship & Prayer"
# remains the canonical pin but doesn't add value here over business-edexcel.

# Split 12 lessons into 3 batches of 4
all_lessons = unit["lessons"]
batches = [all_lessons[0:4], all_lessons[4:8], all_lessons[8:12]]

def slugify(s):
    import re
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]

for i, batch_lessons in enumerate(batches, start=1):
    batch_id = f"b{i}"
    lessons_in_batch = []
    for L in batch_lessons:
        ct = L.get("content_transfer") or {}
        port_source = None
        if ct.get("source_subject_slug"):
            port_source = f"scripts/_content_cambridge-nationals-enterprise-and-marketing/_source_lessons/{L['number']:02d}.json"
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
            "suggested_question_types": [],
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
    print(f"  wrote {out.name}  lessons {[L['number'] for L in batch_lessons]}")
