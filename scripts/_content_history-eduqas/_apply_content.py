"""Apply generated lesson content to Supabase.

Reads scripts/_content_cambridge-nationals-enterprise-and-marketing/lessons/*.json
(written by the Phase 3 content agents) and PATCHes the matching lesson rows
in Supabase.

Agents write `_lesson_number`, `_unit_slug`, `_lesson_slug` as routing keys —
we look up the lesson_id from (subject_slug + unit_slug + lesson_number),
validate fields, and patch. Idempotent.
"""
import argparse
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

SUBJECT_SLUG = "history-eduqas"

ARTICLE_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]


def load_json(path: Path) -> dict:
    raw = path.read_bytes()
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    return json.loads(raw.decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sb = get_client()
    here = Path(__file__).resolve().parent
    lessons_dir = here / "lessons"
    if not lessons_dir.exists():
        print(f"ERROR: {lessons_dir} not found")
        sys.exit(1)

    # Resolve subject + all units + all lesson shells once.
    subj_rows = (
        sb.table("subjects")
        .select("id, slug")
        .eq("slug", SUBJECT_SLUG)
        .is_("school_id", "null")
        .execute()
        .data
    )
    if not subj_rows:
        print(f"ERROR: subject '{SUBJECT_SLUG}' not found")
        sys.exit(1)
    subject_id = subj_rows[0]["id"]

    units = (
        sb.table("units")
        .select("id, slug")
        .eq("subject_id", subject_id)
        .execute()
        .data
    )
    unit_id_by_slug = {u["slug"]: u["id"] for u in units}

    lessons = (
        sb.table("lessons")
        .select("id, slug, lesson_number, unit_id")
        .in_("unit_id", list(unit_id_by_slug.values()))
        .execute()
        .data
    )
    # Index by (unit_slug, lesson_number)
    unit_slug_by_id = {v: k for k, v in unit_id_by_slug.items()}
    lesson_id_by_pair = {
        (unit_slug_by_id[L["unit_id"]], L["lesson_number"]): L["id"]
        for L in lessons
    }
    print(f"Subject id: {subject_id}")
    print(f"Units: {len(unit_id_by_slug)}  /  Lesson shells: {len(lessons)}\n")

    paths = sorted(glob.glob(str(lessons_dir / "*.json")))
    print(f"Found {len(paths)} content JSON files\n")

    ok = 0
    fail = 0
    skip = 0
    for p in paths:
        pname = Path(p).name
        try:
            data = load_json(Path(p))
        except Exception as e:
            print(f"  [PARSE-FAIL] {pname}: {e}")
            fail += 1
            continue

        unit_slug = data.get("_unit_slug")
        lesson_number = data.get("_lesson_number")
        if not unit_slug or lesson_number is None:
            print(f"  [SKIP] {pname} - missing _unit_slug / _lesson_number")
            skip += 1
            continue

        lid = lesson_id_by_pair.get((unit_slug, lesson_number))
        if not lid:
            print(f"  [SKIP] {pname} - no shell at {unit_slug}/L{lesson_number}")
            skip += 1
            continue

        payload = {k: data[k] for k in ARTICLE_KEYS if k in data}
        if not payload:
            print(f"  [SKIP] {pname} - no content fields")
            skip += 1
            continue

        if args.dry_run:
            print(f"  [DRY] L{lesson_number:02d} {pname:55s} -> {lid[:8]}  ({len(payload)} fields)")
            ok += 1
        else:
            try:
                sb.table("lessons").update(payload).eq("id", lid).execute()
                print(f"  [OK]  L{lesson_number:02d} {pname[:55]:55s} -> {lid[:8]}")
                ok += 1
            except Exception as e:
                print(f"  [FAIL] {pname}: {e}")
                fail += 1

    print()
    print(f"=== Insert summary for {SUBJECT_SLUG} ===")
    print(f"  OK   : {ok}")
    print(f"  FAIL : {fail}")
    print(f"  SKIP : {skip}")


if __name__ == "__main__":
    main()
