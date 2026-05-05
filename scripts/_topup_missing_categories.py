"""Top up lessons that pass the min-items check but are missing a required
category (Podcasts, Videos & Channels, one of {Movies/TV/Docs}, Study Tools).
Uses the same whitelist as _refill_related_media_from_whitelist.py.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client
# Reuse the WHITELIST from the refill module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib.machinery import SourceFileLoader
_refill = SourceFileLoader("refill", str(Path(__file__).resolve().parent / "_refill_related_media_from_whitelist.py")).load_module()
WHITELIST = _refill.WHITELIST
REQUIRED_GROUPS = _refill.REQUIRED_GROUPS

import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject_slug")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    sb = get_client()
    pool = WHITELIST.get(args.subject_slug)
    if not pool:
        print(f"No whitelist for {args.subject_slug}")
        return

    sid = sb.table("subjects").select("id").eq("slug", args.subject_slug).is_("school_id", "null").execute().data[0]["id"]
    units = sb.table("units").select("id").eq("subject_id", sid).execute().data

    DRY = not args.apply
    fixed = 0
    for u in units:
        rows = sb.table("lessons").select("id, slug, related_media").eq("unit_id", u["id"]).neq("status", "archived").execute().data
        for r in rows:
            rm = r.get("related_media") or []
            if not isinstance(rm, list):
                continue
            cat_set = set(c.get("category") for c in rm if isinstance(c, dict) and (c.get("items") or []))
            existing_urls = {it.get("url") for c in rm if isinstance(c, dict)
                             for it in (c.get("items") or []) if isinstance(it, dict)}

            additions = []
            for group in REQUIRED_GROUPS:
                if any(c in cat_set for c in group):
                    continue
                # Find a whitelist entry in this group not already present
                for cand in pool:
                    if cand["category"] in group and cand["url"] not in existing_urls:
                        additions.append(cand)
                        existing_urls.add(cand["url"])
                        break

            if not additions:
                continue

            # Merge into existing rm
            new_rm = [dict(c) for c in rm if isinstance(c, dict)]
            for cand in additions:
                # Find or create category
                target = next((c for c in new_rm if c.get("category") == cand["category"]), None)
                if target:
                    target.setdefault("items", []).append(
                        {"title": cand["title"], "url": cand["url"], "description": cand["description"]}
                    )
                else:
                    new_rm.append({
                        "category": cand["category"],
                        "emoji": cand.get("emoji", "🔗"),
                        "items": [{"title": cand["title"], "url": cand["url"], "description": cand["description"]}],
                    })

            print(f"  {r['slug'][:55]:55s}  +{len(additions)} (categories: {[c['category'] for c in additions]})")
            if not DRY:
                sb.table("lessons").update({"related_media": new_rm}).eq("id", r["id"]).execute()
            fixed += 1

    print(f"\n  Lessons fixed: {fixed}")
    if DRY:
        print(f"  DRY RUN — pass --apply to commit")


if __name__ == "__main__":
    main()
