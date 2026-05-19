"""Prep batch JSONs for a free-tier Phase 3 content build.

Usage: python scripts/_prep_content_batches.py <subject-slug>

Reads:
  scripts/_plan_{slug}.json
  scripts/_activation_report_{slug}.json

Writes:
  scripts/_content_{slug}/_batch_NN.json — one batch per unit
                                          (splits any unit > 7 lessons into halves)

Each batch contains:
  - subject metadata
  - unit metadata (slug, name, subtitle, accent palette, body_class)
  - subject_level_teaching_brief (from plan)
  - question_type_names (plan global)
  - allowed_question_types_for_this_unit (plan global by default — content agents
    can subset per-lesson via suggested_question_types)
  - lessons_in_batch — each with lesson_id (from activation), title, description,
    spec_references, section_markers, content_transfer
"""

import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python scripts/_prep_content_batches.py <subject-slug>")
    sys.exit(1)

slug = sys.argv[1]
scripts_dir = Path(__file__).resolve().parent

plan = json.loads((scripts_dir / f"_plan_{slug}.json").read_text(encoding="utf-8"))
activation = json.loads((scripts_dir / f"_activation_report_{slug}.json").read_text(encoding="utf-8"))

content_dir = scripts_dir / f"_content_{slug}"
content_dir.mkdir(exist_ok=True)
lessons_dir = content_dir / "lessons"
lessons_dir.mkdir(exist_ok=True)

subject_meta = {
    "name": plan["subject"]["name"],
    "slug": plan["subject"]["slug"],
    "exam_board": plan["subject"]["exam_board"],
    "spec_code": plan["subject"]["spec_code"],
    "target_audience": "free-tier",
}

teaching_brief = plan.get("teaching_brief", {})
all_question_types = plan.get("question_type_names", [])

batch_num = 0
batches_made = []

for pu in plan.get("article_units", []):
    unit_slug = pu["slug"]
    unit_activation = activation["units"][unit_slug]
    unit_lessons_meta = {L["number"]: L for L in unit_activation["lessons"]}

    plan_lessons = pu["lessons"]
    # Split into chunks of <=7
    chunks = [plan_lessons[i:i+7] for i in range(0, len(plan_lessons), 7)]

    for chunk_idx, chunk in enumerate(chunks):
        batch_num += 1
        batch_id = f"b{batch_num:02d}"
        lessons_in_batch = []
        for plan_lesson in chunk:
            n = plan_lesson["number"]
            act_lesson = unit_lessons_meta[n]
            lessons_in_batch.append({
                "lesson_id": act_lesson["id"],
                "number": n,
                "title": act_lesson["title"],
                "slug": act_lesson["slug"],
                "description": plan_lesson.get("description", ""),
                "spec_references": plan_lesson.get("spec_references", []),
                "section_markers": plan_lesson.get("section_markers", []),
                "content_transfer": plan_lesson.get("content_transfer"),
                "suggested_question_types": plan_lesson.get("suggested_question_types", []),
            })

        batch = {
            "batch_id": batch_id,
            "subject": subject_meta,
            "unit": {
                "name": pu["name"],
                "slug": pu["slug"],
                "subtitle": pu.get("subtitle", ""),
                "accent": pu["accent"],
                "accent_light": pu["accent_light"],
                "accent_badge": pu["accent_badge"],
                "body_class": pu["body_class"],
                "lesson_count": pu["lesson_count"],
            },
            "subject_level_teaching_brief": teaching_brief,
            "question_type_names": all_question_types,
            "allowed_question_types_for_this_unit": all_question_types,
            "lessons_in_batch": lessons_in_batch,
        }
        batch_path = content_dir / f"_batch_{batch_id}.json"
        batch_path.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
        batches_made.append({
            "batch_id": batch_id,
            "unit_slug": unit_slug,
            "lessons": len(lessons_in_batch),
            "path": str(batch_path.relative_to(scripts_dir.parent)),
        })

print(f"\n=== Batch prep for {slug} ===")
print(f"Generated {len(batches_made)} batches:\n")
for b in batches_made:
    print(f"  {b['batch_id']}  [{b['unit_slug'][:45]:45s}]  {b['lessons']} lessons  -> {b['path']}")

# Summary file for the orchestrator
summary = {
    "subject_slug": slug,
    "batches": batches_made,
    "total_lessons": sum(b["lessons"] for b in batches_made),
}
(content_dir / "_batches_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"\nSummary written to {content_dir / '_batches_summary.json'}")
