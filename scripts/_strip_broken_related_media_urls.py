"""Strip broken URLs from related_media for a given subject.

Reads an audit report (the JSON output of _audit_related_media_urls.py),
identifies broken URLs by lesson_id + url + item_index, and removes those
items from related_media. Empty categories get removed. Lessons that fall
below 6 total items get flagged in the output for re-curation.

Conservative deletion: only deletes URLs explicitly flagged as 'broken'
(4xx/5xx). Treats 'error' (timeout/connection) as broken too since those
are likely dead. 403/429 not deleted (might be bot-blocking, not 404).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report_path", help="Path to audit JSON")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out-needs-recurate", default=None,
                    help="Optional: write list of (lesson_id, slug, current_count) for lessons below min after strip")
    args = ap.parse_args()

    with open(args.report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    sb = get_client()
    DRY = not args.apply

    # Group broken entries by lesson_id
    by_lesson = {}
    for b in report.get("broken", []):
        # Skip 403/429 — might be bot-blocking, not actually broken
        if b["status"] == "broken" and isinstance(b.get("detail"), int) and b["detail"] in (403, 429):
            continue
        # Skip if status is 'error' AND detail mentions timeout — could be transient.
        # Actually we'll include errors since most are real. The audit already retried
        # GET on 405/403, so anything left is likely dead.
        by_lesson.setdefault(b["lesson_id"], []).append(b["url"])

    print(f"Lessons with broken URLs to strip: {len(by_lesson)}")
    if not by_lesson:
        return

    needs_recurate = []
    total_stripped = 0
    for lesson_id, broken_urls in by_lesson.items():
        broken_set = set(broken_urls)
        row = sb.table("lessons").select("id, slug, related_media").eq("id", lesson_id).execute().data
        if not row:
            print(f"  MISS: {lesson_id} not found")
            continue
        rm = row[0].get("related_media") or []
        if not isinstance(rm, list):
            continue

        # Filter
        new_rm = []
        stripped_in_lesson = 0
        for cat in rm:
            if not isinstance(cat, dict):
                new_rm.append(cat)
                continue
            items = cat.get("items") or []
            kept = [it for it in items if not (isinstance(it, dict) and it.get("url") in broken_set)]
            stripped_in_lesson += (len(items) - len(kept))
            if kept:
                new_cat = dict(cat)
                new_cat["items"] = kept
                new_rm.append(new_cat)
            # If category becomes empty, drop it entirely

        # Count visible items after strip
        total_items = sum(len(c.get("items") or []) for c in new_rm if isinstance(c, dict))
        below_min = total_items < 6

        if not DRY:
            sb.table("lessons").update({"related_media": new_rm}).eq("id", lesson_id).execute()
        print(f"  {row[0]['slug'][:55]:55s}  -{stripped_in_lesson} broken, {total_items} remain{' [< 6]' if below_min else ''}")
        total_stripped += stripped_in_lesson
        if below_min:
            needs_recurate.append({
                "lesson_id": lesson_id,
                "lesson_slug": row[0]["slug"],
                "remaining_count": total_items,
                "remaining_categories": [c.get("category") for c in new_rm if isinstance(c, dict)],
            })

    print(f"\nTotal URLs stripped: {total_stripped}")
    print(f"Lessons needing re-curate (below 6 items): {len(needs_recurate)}")

    if args.out_needs_recurate and needs_recurate:
        with open(args.out_needs_recurate, "w", encoding="utf-8") as f:
            json.dump(needs_recurate, f, indent=2)
        print(f"  needs-recurate list written to: {args.out_needs_recurate}")

    if DRY:
        print(f"\n  DRY RUN — pass --apply to commit changes")


if __name__ == "__main__":
    main()
