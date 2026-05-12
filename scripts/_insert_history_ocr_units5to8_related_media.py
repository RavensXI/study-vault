"""Insert related_media from JSON files into history-ocr lessons for Units 5-8.

Merge logic:
  - If the existing related_media has a "Podcasts" category with a "Lesson Podcast"
    item with a non-placeholder url, preserve that item at the start of the curated
    Podcasts category.
  - All other categories: replace with the agent's curation.
  - If the agent's JSON has no related_media key, skip the lesson.

Usage:
    python scripts/_insert_history_ocr_units5to8_related_media.py
    python scripts/_insert_history_ocr_units5to8_related_media.py --dry-run
    python scripts/_insert_history_ocr_units5to8_related_media.py --unit usa-people-state-1919-1948
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

BASE_DIR = Path("scripts/_related_media_history-ocr")

UNITS = [
    "usa-people-state-1919-1948",
    "usa-people-state-1945-1974",
    "migration-to-britain-1000-2010",
    "power-monarchy-democracy-1000-2014",
]


def find_lesson_podcast(related_media):
    """Return the Lesson Podcast item dict or None."""
    if not isinstance(related_media, list):
        return None
    for cat in related_media:
        if not isinstance(cat, dict):
            continue
        if (cat.get("category", "") or "").lower() == "podcasts":
            for it in (cat.get("items") or []):
                if isinstance(it, dict) and it.get("title") == "Lesson Podcast":
                    url = it.get("url")
                    if url and url != "#":
                        return it
    return None


def merge(curated, existing):
    """Inject the existing 'Lesson Podcast' item into the curated array's
    Podcasts category (or prepend a new Podcasts category if missing)."""
    lesson_pod = find_lesson_podcast(existing)
    if not lesson_pod:
        return curated

    for cat in curated:
        if (cat.get("category", "") or "").lower() == "podcasts":
            items = cat.get("items") or []
            # Don't double-insert
            if not any(i.get("title") == "Lesson Podcast" for i in items if isinstance(i, dict)):
                cat["items"] = [lesson_pod] + items
            return curated

    # No Podcasts category found — prepend one
    curated.insert(0, {"category": "Podcasts", "items": [lesson_pod]})
    return curated


def process_unit(unit_slug, dry_run, sb):
    unit_dir = BASE_DIR / unit_slug
    if not unit_dir.exists():
        print(f"  [SKIP] No directory: {unit_dir}")
        return 0, 0

    json_files = sorted(unit_dir.glob("L*.json"))
    ok_count = 0
    skip_count = 0

    for jf in json_files:
        with open(jf) as fh:
            data = json.load(fh)

        lesson_id = data.get("lesson_id")
        lesson_num = data.get("lesson_number")
        title = data.get("title", "?")
        curated = data.get("related_media")

        if not lesson_id or not curated:
            print(f"  [SKIP] {jf.name} — no lesson_id or related_media")
            skip_count += 1
            continue

        # Fetch existing to preserve real Lesson Podcast
        existing_row = sb.table("lessons").select("id,related_media").eq("id", lesson_id).single().execute()
        existing_rm = existing_row.data.get("related_media") if existing_row.data else None

        merged = merge(curated, existing_rm)

        if dry_run:
            print(f"  [DRY-RUN] L{lesson_num} {title[:60]} — {len(merged)} categories, {sum(len(c.get('items') or []) for c in merged)} items")
            ok_count += 1
            continue

        result = sb.table("lessons").update({"related_media": merged}).eq("id", lesson_id).execute()
        if result.data:
            print(f"  [OK] L{lesson_num} {title[:60]} — {sum(len(c.get('items') or []) for c in merged)} items written")
            ok_count += 1
        else:
            print(f"  [ERROR] L{lesson_num} {title[:60]} — update returned no data: {result}")
            skip_count += 1

    return ok_count, skip_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--unit", default=None)
    args = parser.parse_args()

    sb = get_client()
    units = [args.unit] if args.unit else UNITS

    total_ok = 0
    total_skip = 0
    for unit_slug in units:
        print(f"\n=== {unit_slug} ===")
        ok, skip = process_unit(unit_slug, args.dry_run, sb)
        total_ok += ok
        total_skip += skip

    print(f"\nDone: {total_ok} updated, {total_skip} skipped.")
    if args.dry_run:
        print("(dry run — no changes written)")


if __name__ == "__main__":
    main()
