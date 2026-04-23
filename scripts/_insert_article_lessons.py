"""
Generic insert script for article-format lessons generated per CONTENT_PROMPT.md.

Reads JSON files from a directory (one per lesson) and updates matching lesson
rows in Supabase. Expects each JSON to include a `_meta` block with subject/unit/lesson_number.

Usage:
  python scripts/_insert_article_lessons.py scripts/_gen_business/
  python scripts/_insert_article_lessons.py scripts/_gen_business/ --dry-run

Each JSON file must contain:
  _meta: {
    "subject_slug": "business",
    "exam_board": "AQA",
    "school_id": null,          # null for free-tier, UUID for bespoke
    "unit_slug": "theme-1-business-in-the-real-world",
    "lesson_number": 1
  },
  description, content_html, exam_tip_html, conclusion_html,
  practice_questions, knowledge_checks, flashcard_questions, glossary_terms,
  hero_keywords, hero_image_caption
"""
import sys, os, json, argparse, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

# Reuse validator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _validate_content_json import validate_file


CONTENT_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory containing per-lesson content JSONs")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-partial", action="store_true",
                        help="Continue even if some lessons fail validation")
    args = parser.parse_args()

    sb = get_client()
    paths = sorted(glob.glob(os.path.join(args.directory, "*.json")))
    if not paths:
        print(f"No JSONs in {args.directory}")
        sys.exit(1)

    print(f"Found {len(paths)} JSON files to process")

    # Validate every file first
    failures = {}
    for p in paths:
        v = validate_file(p)
        if v:
            failures[p] = v
    if failures:
        print(f"\n{len(failures)} files failed validation:")
        for p, vs in failures.items():
            print(f"  {os.path.basename(p)}:")
            for v in vs:
                print(f"    - {v}")
        if not args.allow_partial:
            print("\nExiting. Pass --allow-partial to proceed anyway.")
            sys.exit(1)

    # Now insert (only files that passed, unless --allow-partial)
    clean_paths = [p for p in paths if p not in failures] if not args.allow_partial else paths

    inserted = 0
    for p in clean_paths:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        meta = data.get("_meta") or {}
        if not meta:
            print(f"  [SKIP] {os.path.basename(p)}: no _meta block")
            continue

        subject_slug = meta["subject_slug"]
        unit_slug = meta["unit_slug"]
        lesson_number = meta["lesson_number"]
        school_id = meta.get("school_id")
        exam_board = meta.get("exam_board")

        # Find subject
        q = sb.table("subjects").select("id").eq("slug", subject_slug)
        if exam_board:
            q = q.eq("exam_board", exam_board)
        if school_id is None:
            q = q.is_("school_id", "null")
        else:
            q = q.eq("school_id", school_id)
        subj = q.execute().data
        if not subj:
            print(f"  [ERROR] {os.path.basename(p)}: subject {subject_slug} not found")
            continue
        subject_id = subj[0]["id"]

        # Find unit
        unit = sb.table("units").select("id").eq("subject_id", subject_id).eq("slug", unit_slug).execute().data
        if not unit:
            print(f"  [ERROR] {os.path.basename(p)}: unit {unit_slug} not found")
            continue
        unit_id = unit[0]["id"]

        # Find lesson
        lesson = sb.table("lessons").select("id,title").eq("unit_id", unit_id).eq("lesson_number", lesson_number).execute().data
        if not lesson:
            print(f"  [ERROR] {os.path.basename(p)}: lesson number {lesson_number} not found in unit {unit_slug}")
            continue
        lid = lesson[0]["id"]
        title = lesson[0]["title"]

        update_payload = {k: data[k] for k in CONTENT_KEYS if k in data}

        if args.dry_run:
            print(f"  [DRY] L{lesson_number:02d} {title[:50]:50s} → update {len(update_payload)} fields")
        else:
            sb.table("lessons").update(update_payload).eq("id", lid).execute()
            inserted += 1
            print(f"  [OK] L{lesson_number:02d} {title[:50]:50s}")

    if not args.dry_run:
        print(f"\n[DONE] Updated {inserted} lessons.")


if __name__ == "__main__":
    main()
