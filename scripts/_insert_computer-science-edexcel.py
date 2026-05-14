"""Insert Computer Science Edexcel content into Supabase.

Reads JSON files from scripts/_content_computer-science-edexcel/lessons/.
Each file has _lesson_id embedded. Status stays at `pending_review`
(free-tier convention — Tom approves to live).
"""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

CONTENT_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sb = get_client()
    paths = sorted(glob.glob("scripts/_content_computer-science-edexcel/lessons/*.json"))
    print(f"Found {len(paths)} content JSONs")

    inserted = missing = 0
    for p in paths:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        lid = data.get("_lesson_id")
        slug = os.path.splitext(os.path.basename(p))[0]
        if not lid:
            print(f"  [MISS] {slug} -- no _lesson_id")
            missing += 1
            continue
        payload = {k: data[k] for k in CONTENT_KEYS if k in data}
        if args.dry_run:
            print(f"  [DRY] {lid[:8]} {slug[:55]:55s}  {len(payload)} fields")
        else:
            sb.table("lessons").update(payload).eq("id", lid).execute()
            inserted += 1
            print(f"  [OK]  {lid[:8]} {slug[:55]}")

    print()
    if args.dry_run:
        print(f"DRY RUN -- would update {len(paths)-missing}, missing {missing}.")
    else:
        print(f"Inserted: {inserted}.  Missing: {missing}.")


if __name__ == "__main__":
    main()
