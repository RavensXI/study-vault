"""Insert curated related_media into Supabase lessons for psychology-aqa.

Reads every JSON in scripts/_related_media_psychology-aqa/ and updates the
matching lesson row. Preserves any existing real Lesson Podcast URL.
"""
import argparse, json, sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

JSON_DIR = "scripts/_related_media_psychology-aqa"


def find_lesson_podcast(related_media):
    if not isinstance(related_media, list):
        return None
    for cat in related_media:
        if not isinstance(cat, dict):
            continue
        if (cat.get("category") or "").lower() == "podcasts":
            for it in (cat.get("items") or []):
                if isinstance(it, dict) and it.get("title") == "Lesson Podcast":
                    url = it.get("url")
                    if url and url not in (None, "", "#"):
                        return it
    return None


def merge_lesson_podcast(curated, existing):
    """If the existing row has a real Lesson Podcast URL, keep it."""
    real = find_lesson_podcast(existing)
    if not real:
        return curated
    for cat in curated:
        if (cat.get("category") or "").lower() == "podcasts":
            items = cat.get("items") or []
            items = [i for i in items if not (isinstance(i, dict) and i.get("title") == "Lesson Podcast")]
            items.insert(0, real)
            cat["items"] = items
            return curated
    curated.insert(0, {"category": "Podcasts", "items": [real]})
    return curated


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    sb = get_client()
    paths = sorted(glob.glob(os.path.join(JSON_DIR, "*.json")))
    print(f"Files: {len(paths)}")

    ok, errs = 0, 0
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        lesson_id = data.get("lesson_id")
        curated = data.get("related_media")
        title = data.get("lesson_title", "")
        if not lesson_id or not curated:
            print(f"  [SKIP] {os.path.basename(path)}: missing lesson_id or related_media")
            errs += 1
            continue
        existing_row = sb.table("lessons").select("related_media").eq("id", lesson_id).execute().data
        existing = existing_row[0]["related_media"] if existing_row else None
        merged = merge_lesson_podcast(curated, existing)
        if args.dry_run:
            cats = ", ".join((c.get("category") or "?") for c in merged)
            print(f"  [DRY] {os.path.basename(path):50s} -> [{cats}]")
        else:
            sb.table("lessons").update({"related_media": merged}).eq("id", lesson_id).execute()
            print(f"  [OK]  {os.path.basename(path):50s} {title[:50]}")
            ok += 1
    print(f"\n{ok} inserted, {errs} skipped/failed")


if __name__ == "__main__":
    main()
