"""Build batch JSONs for the PE OCR Phase 3 fan-out.

Unit 1 (14 lessons) -> 3 batches: u1_b1 (1-5), u1_b2 (6-10), u1_b3 (11-14)
Unit 2 (13 lessons) -> 3 batches: u2_b1 (1-5), u2_b2 (6-9), u2_b3 (10-13)

Each batch entry contains the lesson metadata, content_transfer block, and pointer
to the AQA source-content file (or null for fresh lessons).

Each batch JSON also embeds: subject + unit metadata, spec_slice_path, reference_lesson_path,
subject_level_teaching_brief, registered_question_type_names, allowed_question_types,
and the lessons_in_batch array.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = ROOT / "scripts" / "_plan_physical-education-ocr.json"
OUT_DIR = ROOT / "scripts" / "_content_physical-education-ocr"
RESULT_PATH = OUT_DIR / "_fetch_setup_result.json"

UNIT_BATCH_GROUPS = {
    "physical-factors-affecting-performance": [
        ("u1_b1", [1, 2, 3, 4, 5]),
        ("u1_b2", [6, 7, 8, 9, 10]),
        ("u1_b3", [11, 12, 13, 14]),
    ],
    "socio-cultural-issues-and-sports-psychology": [
        ("u2_b1", [1, 2, 3, 4, 5]),
        ("u2_b2", [6, 7, 8, 9]),
        ("u2_b3", [10, 11, 12, 13]),
    ],
}

UNIT_SPEC_SLICE = {
    "physical-factors-affecting-performance": "scripts/_content_physical-education-ocr/_spec_physical-factors-affecting-performance.txt",
    "socio-cultural-issues-and-sports-psychology": "scripts/_content_physical-education-ocr/_spec_socio-cultural-issues-and-sports-psychology.txt",
}

UNIT_NAMES = {
    "physical-factors-affecting-performance": "Physical Factors Affecting Performance",
    "socio-cultural-issues-and-sports-psychology": "Socio-Cultural Issues and Sports Psychology",
}


def build_quote_block(quotes):
    out = []
    for q in quotes:
        out.append(
            f"<blockquote>&ldquo;{q['quote']}&rdquo; <cite>&mdash; {q['author']}</cite></blockquote>"
        )
    return "\n".join(out)


def question_types_for_lesson(lesson):
    """Pick suggested question types from the registered 11.

    OCR is recall-heavy (AO1 ~42%). Bias toward 1/2/3/4-mark questions.
    Always include one extended response (6 OR 8 marks).
    Lessons amenable to data get a Calculate-from-Data or Interpret-Data slot.
    """
    title_lower = (lesson.get("title") or "").lower()
    description_lower = (lesson.get("description") or "").lower()
    haystack = title_lower + " " + description_lower

    data_amenable_keywords = [
        "cardiovascular",
        "effects of exercise",
        "components of fitness",
        "fitness test",
        "engagement patterns",
        "wellbeing",
        "well-being",
        "diet",
        "nutrition",
        "sedentary",
        "drugs",
        "commercialisation",
    ]
    is_data_lesson = any(k in haystack for k in data_amenable_keywords)

    extended = "8 marks — Evaluate" if lesson.get("number") in (4, 6, 8, 9, 10, 11, 13, 14) else "6 marks — Analyse"

    if is_data_lesson:
        return [
            "1 mark — Identify",
            "2 marks — Define",
            "3 marks — Calculate from Data",
            "4 marks — Interpret Data",
            "4 marks — Explain",
            extended,
        ]
    return [
        "1 mark — Identify",
        "2 marks — Define",
        "2 marks — State Two",
        "3 marks — Describe",
        "4 marks — Explain",
        extended,
    ]


def main():
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    fetch = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    id_map = fetch["ocr_lesson_id_map"]

    subject_meta = plan["subject"]
    subject_block = {
        "name": subject_meta["name"],
        "slug": subject_meta["slug"],
        "exam_board": subject_meta["exam_board"],
        "spec_code": subject_meta["spec_code"],
        "target_audience": "free-tier",
    }

    quote_html = build_quote_block(plan["quote_ticker_quotes"])

    teaching_brief = plan["teaching_brief"]

    registered_types = plan["question_type_names"]

    units_by_slug = {u["slug"]: u for u in plan["article_units"]}

    written = []

    for unit_slug, batch_groups in UNIT_BATCH_GROUPS.items():
        unit = units_by_slug[unit_slug]
        for batch_id, lesson_numbers in batch_groups:
            lessons_in_batch = []
            for ln in lesson_numbers:
                # find lesson in plan
                plan_lesson = next(
                    (l for l in unit["lessons"] if l["number"] == ln), None
                )
                assert plan_lesson, f"missing plan entry for {unit_slug} L{ln}"

                key = f"{unit_slug}::{ln}"
                ocr_row = id_map[key]

                ct = plan_lesson["content_transfer"]
                source_file = None
                if ct.get("transfer_score") != "fresh":
                    # build slug -> need AQA lesson slug from source_unit + source_lesson_number
                    # we already saved as aqa_<aqa-slug>.json. We don't have the AQA slug
                    # in plan; resolve via fetch_setup_result by re-reading the AQA source files.
                    # Easiest: reverse-look from the source files dir.
                    pass

                lessons_in_batch.append(
                    {
                        "lesson_id": ocr_row["id"],
                        "lesson_number": ln,
                        "slug": ocr_row["slug"],
                        "title": ocr_row["title"],
                        "description": ocr_row["description"],
                        "spec_references": plan_lesson["spec_references"],
                        "section_markers": plan_lesson["section_markers"],
                        "suggested_question_types": question_types_for_lesson(plan_lesson),
                        "content_transfer": ct,
                        "source_aqa_file": None,  # resolved below
                    }
                )

            batch_out = {
                "batch_id": batch_id,
                "subject": subject_block,
                "unit": {
                    "name": UNIT_NAMES[unit_slug],
                    "slug": unit_slug,
                    "subtitle": unit["subtitle"],
                    "accent": unit["accent"],
                    "accent_light": unit["accent_light"],
                    "accent_badge": unit["accent_badge"],
                    "body_class": unit["body_class"],
                    "lesson_count": unit["lesson_count"],
                },
                "spec_slice_path": UNIT_SPEC_SLICE[unit_slug],
                "reference_lesson_path": "scripts/_content_physical-education-ocr/_reference_lesson.json",
                "subject_level_teaching_brief": teaching_brief,
                "unit_level_teaching_brief": {},
                "quote_ticker_html_for_unit": quote_html,
                "registered_question_type_names": registered_types,
                "allowed_question_types_for_this_unit": registered_types,
                "lessons_in_batch": lessons_in_batch,
                "output_dir": "scripts/_content_physical-education-ocr/lessons",
            }

            out_path = OUT_DIR / f"_batch_{batch_id}.json"
            out_path.write_text(
                json.dumps(batch_out, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            written.append((batch_id, unit_slug, lesson_numbers, out_path))
            print(f"  wrote _batch_{batch_id}.json — {unit_slug} lessons {lesson_numbers}")

    # Resolve source_aqa_file for each batch entry by mapping AQA source slug.
    # We have the AQA source-lesson rows saved; map (source_unit_slug, source_lesson_number) -> file.
    source_dir = OUT_DIR / "_source"
    aqa_files = {p.name for p in source_dir.glob("aqa_*.json")}

    # Build (unit_slug, lesson_number) -> aqa_<slug>.json map by reading each file
    src_map = {}
    for f in source_dir.glob("aqa_*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        # We don't store unit_slug in the file content; lesson_number is enough only with unit context.
        # Instead we look up via the plan's adaptation_notes -> source_lesson_number + source_unit_slug.
        src_map[data["slug"]] = f.name

    # Now patch the batch files
    for unit in plan["article_units"]:
        for lesson in unit["lessons"]:
            ct = lesson["content_transfer"]
            if ct.get("transfer_score") == "fresh":
                continue
            # Get the AQA lesson slug. We need to look it up from the AQA Supabase data.
            # The simplest: read the AQA source file we saved. But we keyed by AQA slug.
            # Resolve by scanning source files for matching lesson_number.
            target_num = ct["source_lesson_number"]
            target_unit = ct["source_unit_slug"]
            # Look at every saved AQA source file and find one whose lesson_number matches
            # AND whose slug appears under the right AQA unit.
            # Easier: re-read the fetched files with their unit hint.
            # We need to disambiguate: the AQA L1 in unit-1 (skeleton) vs unit-2 (skill/ability).
            # So load each file and check its slug against the plan's expected source unit.
            matched = None
            for f in source_dir.glob("aqa_*.json"):
                d = json.loads(f.read_text(encoding="utf-8"))
                if d["lesson_number"] == target_num:
                    # We don't have unit_slug in the file; disambiguate via known mapping.
                    # AQA unit-1 slugs (skeleton, muscles, joints, cv, respiratory etc)
                    # AQA unit-2 slugs (skill, goal-setting, info-processing etc)
                    aqa_u1_slugs = {
                        "the-skeleton-structure-and-functions",
                        "muscles-and-antagonistic-pairs",
                        "synovial-joints-and-types-of-movement",
                        "the-cardiovascular-system-and-exercise",
                        "the-respiratory-system-and-gas-exchange",
                        "aerobic-and-anaerobic-exercise",
                        "short-and-long-term-effects-of-exercise",
                        "lever-systems-and-mechanical-advantage",
                        "planes-and-axes-of-movement",
                        "health-fitness-and-the-components-of-fitness",
                        "fitness-testing-procedures-and-validity",
                        "principles-of-training-sport-and-fitt",
                        "methods-of-training",
                        "optimising-training-and-preventing-injury",
                        "warm-up-and-cool-down",
                        "using-data-in-physical-activity-and-sport",
                    }
                    is_u1 = d["slug"] in aqa_u1_slugs
                    if target_unit == "human-body-and-movement" and is_u1:
                        matched = f.name
                        break
                    if target_unit == "socio-cultural-influences-and-wellbeing" and not is_u1:
                        matched = f.name
                        break
            if not matched:
                print(f"  WARN: no source file matched for OCR L{lesson['number']} (target {target_unit} L{target_num})")
                continue
            # Patch into corresponding batch file
            for unit_slug, batch_groups in UNIT_BATCH_GROUPS.items():
                if unit_slug != unit["slug"]:
                    continue
                for batch_id, nums in batch_groups:
                    if lesson["number"] not in nums:
                        continue
                    batch_path = OUT_DIR / f"_batch_{batch_id}.json"
                    bdata = json.loads(batch_path.read_text(encoding="utf-8"))
                    for lib in bdata["lessons_in_batch"]:
                        if lib["lesson_number"] == lesson["number"]:
                            lib["source_aqa_file"] = f"_source/{matched}"
                    batch_path.write_text(
                        json.dumps(bdata, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )

    # Verification print
    for unit_slug, batch_groups in UNIT_BATCH_GROUPS.items():
        for batch_id, nums in batch_groups:
            bp = OUT_DIR / f"_batch_{batch_id}.json"
            d = json.loads(bp.read_text(encoding="utf-8"))
            for lib in d["lessons_in_batch"]:
                tag = lib.get("source_aqa_file") or "FRESH"
                print(f"    {batch_id}  L{lib['lesson_number']}  {lib['slug']}  -> {tag}")


if __name__ == "__main__":
    main()
