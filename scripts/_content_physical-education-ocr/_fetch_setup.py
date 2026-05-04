"""One-shot Phase 3 setup script for PE OCR.

Pulls:
  1. Reference lesson (RE L01 Worship & Prayer) -> _reference_lesson.json
  2. AQA source-lesson rows for every transferable OCR lesson -> _source/aqa_<slug>.json
  3. OCR lesson IDs from Supabase (subjects.slug='physical-education-ocr')
     -> Returns mapping for batch JSON construction.

Reads from:
  - Plan: scripts/_plan_physical-education-ocr.json
  - AQA reference dir: scripts/_content_physical-education-aqa/

Writes to:
  - scripts/_content_physical-education-ocr/_reference_lesson.json
  - scripts/_content_physical-education-ocr/_source/aqa_<slug>.json
  - Prints lesson_id-by-(unit_slug, lesson_number) map (used by batch writer).
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.supabase_client import get_client  # noqa: E402

PLAN_PATH = ROOT / "scripts" / "_plan_physical-education-ocr.json"
OUT_DIR = ROOT / "scripts" / "_content_physical-education-ocr"
SOURCE_DIR = OUT_DIR / "_source"
REF_LESSON_ID = "21447890-d512-42c6-85f9-90b4133c06e3"

CONTENT_FIELDS = [
    "id",
    "slug",
    "title",
    "lesson_number",
    "description",
    "content_html",
    "exam_tip_html",
    "conclusion_html",
    "practice_questions",
    "knowledge_checks",
    "flashcard_questions",
    "glossary_terms",
]


def main():
    sb = get_client()

    # 1. Reference lesson
    print("Fetching reference lesson...")
    ref = sb.table("lessons").select("*").eq("id", REF_LESSON_ID).single().execute()
    (OUT_DIR / "_reference_lesson.json").write_text(
        json.dumps(ref.data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  wrote _reference_lesson.json")

    # 2. AQA source lessons
    aqa_subj = (
        sb.table("subjects").select("id").eq("slug", "physical-education-aqa").single().execute()
    )
    aqa_units = (
        sb.table("units")
        .select("id,slug")
        .eq("subject_id", aqa_subj.data["id"])
        .execute()
    )
    aqa_unit_by_slug = {u["slug"]: u["id"] for u in aqa_units.data}

    aqa_lessons = (
        sb.table("lessons")
        .select(",".join(CONTENT_FIELDS) + ",unit_id")
        .in_("unit_id", list(aqa_unit_by_slug.values()))
        .execute()
    )
    # key: (unit_slug, lesson_number) -> lesson row
    aqa_by_unit_num = {}
    aqa_unit_id_to_slug = {v: k for k, v in aqa_unit_by_slug.items()}
    for l in aqa_lessons.data:
        u_slug = aqa_unit_id_to_slug[l["unit_id"]]
        aqa_by_unit_num[(u_slug, l["lesson_number"])] = l

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    fetched = 0
    skipped_fresh = 0
    failed = []

    for unit in plan["article_units"]:
        for lesson in unit["lessons"]:
            ct = lesson.get("content_transfer", {})
            score = ct.get("transfer_score")
            if score == "fresh":
                skipped_fresh += 1
                continue
            src_unit = ct.get("source_unit_slug")
            src_num = ct.get("source_lesson_number")
            if not src_unit or src_num is None:
                failed.append(f"L{lesson['number']} ({lesson['slug']}): missing source ref")
                continue
            row = aqa_by_unit_num.get((src_unit, src_num))
            if not row:
                failed.append(
                    f"L{lesson['number']} ({lesson['slug']}): no AQA match for {src_unit} L{src_num}"
                )
                continue
            slim = {k: row.get(k) for k in CONTENT_FIELDS}
            out_path = SOURCE_DIR / f"aqa_{row['slug']}.json"
            out_path.write_text(
                json.dumps(slim, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            fetched += 1

    print(f"  AQA source lessons fetched: {fetched}")
    print(f"  fresh lessons skipped:      {skipped_fresh}")
    print(f"  failures:                   {len(failed)}")
    for f in failed:
        print(f"    - {f}")

    # 3. OCR lesson IDs
    ocr_subj = (
        sb.table("subjects").select("id").eq("slug", "physical-education-ocr").single().execute()
    )
    ocr_units = (
        sb.table("units")
        .select("id,slug")
        .eq("subject_id", ocr_subj.data["id"])
        .execute()
    )
    ocr_unit_by_slug = {u["slug"]: u["id"] for u in ocr_units.data}
    ocr_lessons = (
        sb.table("lessons")
        .select("id,slug,lesson_number,unit_id,title,description")
        .in_("unit_id", list(ocr_unit_by_slug.values()))
        .execute()
    )
    ocr_unit_id_to_slug = {v: k for k, v in ocr_unit_by_slug.items()}

    ocr_id_map = {}
    for l in ocr_lessons.data:
        u_slug = ocr_unit_id_to_slug[l["unit_id"]]
        ocr_id_map[(u_slug, l["lesson_number"])] = {
            "id": l["id"],
            "slug": l["slug"],
            "title": l["title"],
            "description": l["description"],
        }

    out = {
        "ocr_lesson_id_map": {
            f"{k[0]}::{k[1]}": v for k, v in ocr_id_map.items()
        },
        "fetched": fetched,
        "skipped_fresh": skipped_fresh,
        "failed": failed,
    }
    (OUT_DIR / "_fetch_setup_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  wrote _fetch_setup_result.json with {len(ocr_id_map)} OCR lesson IDs")


if __name__ == "__main__":
    main()
