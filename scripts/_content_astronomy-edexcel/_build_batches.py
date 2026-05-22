"""Build 2 batch files (5 lessons each) for the Phase 3 content agents.

Sport Studies has LOW transfer baseline — 7 of 10 lessons are fresh from
spec, 3 are medium-transfer from PE-AQA but with no specific source lesson
to port from. All 10 will generate from the plan's adaptation_notes +
spec_references + section_markers; no source lesson exports needed.
"""
import json
import re
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
plan = json.loads(
    (here.parent / "_plan_astronomy-edexcel.json").read_text(encoding="utf-8")
)

subject_meta = {
    "name": plan["subject"]["name"],
    "slug": plan["subject"]["slug"],
    "exam_board": plan["subject"]["exam_board"],
    "target_audience": "free-tier",
    "qualification_type": "cambridge-national-l1-l2",
}


teaching_brief = plan.get("teaching_brief", {})
question_type_names = plan.get("question_type_names", [])

reference_lesson_path = "scripts/_content_business-edexcel/_reference_lesson.json"

# Astronomy: split each unit into 2 batches (4 batches total)
batches_data = []
for unit in plan['article_units']:
    um = {
        'name': unit['name'],
        'slug': unit['slug'],
        'subtitle': unit['subtitle'],
        'accent': unit['accent'],
        'accent_light': unit['accent_light'],
        'accent_badge': unit['accent_badge'],
        'body_class': unit['body_class'],
        'lesson_count': unit['lesson_count'],
    }
    lessons = unit['lessons']
    half = (len(lessons) + 1) // 2
    batches_data.append({'unit_meta': um, 'lessons': lessons[:half]})
    batches_data.append({'unit_meta': um, 'lessons': lessons[half:]})


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


for i, bd in enumerate(batches_data, start=1):
    unit_meta = bd["unit_meta"]
    batch_lessons = bd["lessons"]
    batch_id = f"b{i}"
    lessons_in_batch = []
    for L in batch_lessons:
        ct = L.get("content_transfer") or {}
        lessons_in_batch.append({
            "number": L["number"],
            "title": L["title"],
            "slug": slugify(L["title"]),
            "description": L["description"],
            "spec_references": L["spec_references"],
            "section_markers": L["section_markers"],
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
