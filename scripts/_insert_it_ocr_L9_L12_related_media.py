"""Insert related_media for it-ocr L9-L12 (R050 expansion) using lesson_id.

Reads L9.json through L12.json from scripts/_related_media_it-ocr/,
fetches the current related_media from Supabase, preserves any real
Lesson Podcast URL, then writes the curated content back.

Usage:
    python scripts/_insert_it_ocr_L9_L12_related_media.py
    python scripts/_insert_it_ocr_L9_L12_related_media.py --dry-run
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

JSON_DIR = Path("scripts/_related_media_it-ocr")
LESSON_FILES = ["L9.json", "L10.json", "L11.json", "L12.json"]


def find_lesson_podcast(related_media):
    """Return the Lesson Podcast item if it has a real URL, else None."""
    if not isinstance(related_media, list):
        return None
    for cat in related_media:
        if not isinstance(cat, dict):
            continue
        if (cat.get("category", "") or "").lower() == "podcasts":
            for it in cat.get("items") or []:
                if isinstance(it, dict) and it.get("title") == "Lesson Podcast":
                    url = it.get("url")
                    if url and url not in (None, "", "#"):
                        return it
    return None


def merge(curated, existing):
    """Inject a real Lesson Podcast from existing into the curated list."""
    lesson_pod = find_lesson_podcast(existing)
    if not lesson_pod:
        return curated
    for cat in curated:
        if (cat.get("category", "") or "").lower() == "podcasts":
            items = cat.get("items") or []
            if any(i.get("title") == "Lesson Podcast" for i in items):
                return curated
            cat["items"] = [lesson_pod] + items
            return curated
    curated.insert(0, {"category": "Podcasts", "items": [lesson_pod]})
    return curated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sb = get_client()
    ok = 0
    failed = 0

    for fname in LESSON_FILES:
        fpath = JSON_DIR / fname
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [PARSE-ERR] {fname}: {e}")
            failed += 1
            continue

        lesson_id = data.get("lesson_id")
        title = data.get("title", "")
        curated = data.get("related_media")

        if not lesson_id or not curated:
            print(f"  [SKIP] {fname}: missing lesson_id or related_media")
            failed += 1
            continue

        # Fetch existing row
        rows = sb.table("lessons").select("id, related_media").eq("id", lesson_id).execute().data
        if not rows:
            print(f"  [NOT-FOUND] {fname}: lesson_id {lesson_id} not in Supabase")
            failed += 1
            continue

        existing = rows[0].get("related_media") or []
        merged = merge(curated, existing)

        n_cats = len(merged)
        n_items = sum(len(c.get("items") or []) for c in merged if isinstance(c, dict))

        if args.dry_run:
            print(f"  [DRY] {fname} ({title}): {n_cats} categories, {n_items} items")
        else:
            sb.table("lessons").update({"related_media": merged}).eq("id", lesson_id).execute()
            print(f"  [OK]  {fname} ({title}): {n_cats} categories, {n_items} items")
        ok += 1

    print()
    print(f"=== Summary: {ok} updated, {failed} failed ===")


if __name__ == "__main__":
    main()
