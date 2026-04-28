"""Phase 3 prep — build per-batch input JSONs for content agents.

Reads:  scripts/_plan_history-aqa.json
Writes: scripts/_content_history-aqa/_reference_lesson.json
        scripts/_content_history-aqa/_spec_{unit-slug}.txt (16 unit spec slices)
        scripts/_content_history-aqa/_batch_{batch-id}.json (32 per-batch agent inputs)

Batch sizing follows pipeline-doc max of 10 lessons per agent. Tom asked to be
conservative — we use 6-7 per agent, splitting each unit into 2 batches.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

ROOT = Path(__file__).resolve().parent.parent
scripts = Path(__file__).resolve().parent
out_dir = scripts / "_content_history-aqa"
out_dir.mkdir(exist_ok=True)
(out_dir / "lessons").mkdir(exist_ok=True)

master = json.loads((scripts / "_plan_history-aqa.json").read_text(encoding="utf-8"))
spec_path = ROOT / "specs" / "aqa" / "history-8145-8145.md"
spec_lines = spec_path.read_text(encoding="utf-8").splitlines()


# ─────────────────────────────────────── reference lesson

REFERENCE_ID = "21447890-d512-42c6-85f9-90b4133c06e3"
ref_path = out_dir / "_reference_lesson.json"
if not ref_path.exists():
    sb = get_client()
    ref = (
        sb.table("lessons")
        .select(
            "id, title, description, content_html, exam_tip_html, conclusion_html, "
            "practice_questions, knowledge_checks, flashcard_questions, glossary_terms, "
            "hero_image_caption"
        )
        .eq("id", REFERENCE_ID)
        .single()
        .execute()
        .data
    )
    ref_path.write_text(json.dumps(ref, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Reference lesson saved: {ref_path}")
else:
    print(f"Reference lesson cached: {ref_path}")


# ─────────────────────────────────────── per-unit spec slices

shell = json.loads((scripts / "_plan_history-aqa-shell.json").read_text(encoding="utf-8"))
for unit in shell["unit_shells"]:
    rng = unit["spec_line_range"]
    start, end = (int(x) for x in rng.split("-"))
    slice_lines = spec_lines[start - 1 : end]
    slice_text = "\n".join(slice_lines)
    p = out_dir / f"_spec_{unit['slug']}.txt"
    p.write_text(slice_text, encoding="utf-8")
print(f"Wrote 16 per-unit spec slices to {out_dir}")


# ─────────────────────────────────────── batches

def split_batches(n_lessons: int) -> list[tuple[int, int]]:
    """Split a unit into 2 batches of roughly equal size, max 7 per batch."""
    if n_lessons <= 7:
        return [(1, n_lessons)]
    half = (n_lessons + 1) // 2
    return [(1, half), (half + 1, n_lessons)]


batches = []
for unit in master["article_units"]:
    n = unit["lesson_count"]
    splits = split_batches(n)
    for batch_idx, (lo, hi) in enumerate(splits, start=1):
        batch_id = f"{unit['slug']}_b{batch_idx}"
        lessons_in_batch = [
            L
            for L in unit["lessons"]
            if (L.get("number") or L.get("lesson_number")) in range(lo, hi + 1)
        ]
        batch_input = {
            "batch_id": batch_id,
            "subject": {
                "name": master["subject"]["name"],
                "slug": master["subject"]["slug"],
                "exam_board": master["subject"]["exam_board"],
                "spec_code": master["subject"]["spec_code"],
                "target_audience": "free-tier",
            },
            "unit": {
                "name": unit["name"],
                "slug": unit["slug"],
                "subtitle": unit["subtitle"],
                "accent": unit["accent"],
                "body_class": unit["body_class"],
                "section_key": unit["section_key"],
                "spec_section_focus": unit["spec_section_focus"],
                "lesson_count": unit["lesson_count"],
            },
            "spec_slice_path": f"scripts/_content_history-aqa/_spec_{unit['slug']}.txt",
            "reference_lesson_path": "scripts/_content_history-aqa/_reference_lesson.json",
            "subject_level_teaching_brief": master["subject_level_teaching_brief"],
            "option_teaching_brief": unit.get("teaching_brief", {}),
            "key_individuals_and_groups": unit.get("key_individuals_and_groups", []),
            "registered_question_type_names": master["question_type_names"],
            "content_agent_banlist_aqa_specific": master[
                "content_agent_banlist_aqa_specific"
            ],
            "content_agent_guardrails_for_he": unit.get(
                "content_agent_guardrails_for_he"
            ),
            "lessons_in_batch": lessons_in_batch,
            "output_dir": "scripts/_content_history-aqa/lessons",
        }
        p = out_dir / f"_batch_{batch_id}.json"
        p.write_text(json.dumps(batch_input, indent=2, ensure_ascii=False), encoding="utf-8")
        batches.append(batch_id)

print(f"\nWrote {len(batches)} batch input JSONs to {out_dir}")
print(f"Batch sizes: {sorted({len(json.loads((out_dir / f'_batch_{b}.json').read_text(encoding='utf-8'))['lessons_in_batch']) for b in batches})}")
print(f"Total lessons across batches: {sum(len(json.loads((out_dir / f'_batch_{b}.json').read_text(encoding='utf-8'))['lessons_in_batch']) for b in batches)}")

# Also write the manifest
(out_dir / "_batch_manifest.json").write_text(
    json.dumps({"batches": batches, "total_lessons": sum(u['lesson_count'] for u in master['article_units'])}, indent=2),
    encoding="utf-8",
)
print(f"Manifest: {out_dir / '_batch_manifest.json'}")
