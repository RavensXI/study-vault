"""Insert Statistics AQA content into Supabase.

Handles both article-format (Units 1 + 5) and practice-format (Units 2-4)
lessons. Each lesson JSON has `_lesson_id` embedded so the inserter maps
straight to the right Supabase row. Status stays at `pending_review`.
"""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

ARTICLE_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]
PRACTICE_KEYS = ["description", "practice_data"]


def load_json(path):
    raw = open(path, "rb").read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    return json.loads(raw.decode('utf-8'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sb = get_client()
    paths = sorted(glob.glob("scripts/_content_statistics-aqa/lessons/*.json"))
    print(f"Found {len(paths)} lesson JSONs")
    inserted = missing = 0
    for p in paths:
        try:
            data = load_json(p)
        except Exception as e:
            print(f"  [PARSE-FAIL] {p}: {e}")
            missing += 1
            continue
        lid = data.get("_lesson_id")
        slug = os.path.splitext(os.path.basename(p))[0]
        if not lid:
            print(f"  [MISS] {slug} -- no _lesson_id")
            missing += 1
            continue
        if "practice_data" in data:
            payload = {k: data[k] for k in PRACTICE_KEYS if k in data}
            kind = "PRAC"
        else:
            payload = {k: data[k] for k in ARTICLE_KEYS if k in data}
            kind = "ART "
        if args.dry_run:
            print(f"  [DRY {kind}] {lid[:8]} {slug[:60]:60s} {len(payload)} fields")
        else:
            sb.table("lessons").update(payload).eq("id", lid).execute()
            inserted += 1
            print(f"  [OK  {kind}] {lid[:8]} {slug[:60]}")
    print()
    print(f"Inserted: {inserted}.  Missing: {missing}.")


if __name__ == "__main__":
    main()
