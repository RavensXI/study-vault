"""Audit related_media URLs across a free-tier subject.

For each lesson, extracts every URL from `related_media[*].items[*].url`,
skips YouTube (already validated via oembed), HEAD-checks the rest in
parallel, and reports counts + a list of broken URLs.

Usage:
  python scripts/_audit_related_media_urls.py <subject-slug> [--unit-sort-min N]

The --unit-sort-min lets you scope to "new" units in a gap-fill build
(e.g. RE gap-fill = sort_order >= 9).
"""
import argparse
import json
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

UA = "Mozilla/5.0 (compatible; StudyVault-LinkAudit/1.0; +https://studyvault.co.uk)"
TIMEOUT = 8
PARALLEL = 16


def is_youtube(url):
    return "youtube.com" in url or "youtu.be" in url


def check_url(url):
    """Return (url, status) where status is 'ok', 'broken', 'maybe' (3xx no resolution), or 'error'."""
    try:
        r = requests.head(
            url, allow_redirects=True, timeout=TIMEOUT,
            headers={"User-Agent": UA, "Accept": "*/*"}
        )
        if r.status_code < 400:
            return (url, "ok", r.status_code)
        # Some servers (Substack, certain CDNs) return 405 to HEAD — try GET with stream
        if r.status_code in (403, 405, 429):
            try:
                r2 = requests.get(url, allow_redirects=True, timeout=TIMEOUT, stream=True,
                                  headers={"User-Agent": UA, "Accept": "*/*"})
                r2.close()
                if r2.status_code < 400:
                    return (url, "ok", r2.status_code)
                return (url, "broken", r2.status_code)
            except Exception as e:
                return (url, "error", str(e)[:60])
        return (url, "broken", r.status_code)
    except requests.exceptions.Timeout:
        return (url, "error", "timeout")
    except Exception as e:
        return (url, "error", str(e)[:60])


def collect_urls(subject_slug, unit_sort_min=None):
    """Return list of (lesson_id, lesson_slug, unit_slug, category, item_index, url)."""
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", subject_slug).is_("school_id", "null").execute().data
    if not sub:
        print(f"  Subject not found: {subject_slug}")
        return []
    sid = sub[0]["id"]

    units_q = sb.table("units").select("id, slug, sort_order").eq("subject_id", sid)
    if unit_sort_min is not None:
        units_q = units_q.gte("sort_order", unit_sort_min)
    units = units_q.order("sort_order").execute().data

    out = []
    for u in units:
        rows = (
            sb.table("lessons")
            .select("id, slug, related_media")
            .eq("unit_id", u["id"])
            .neq("status", "archived")
            .execute()
            .data
        )
        for r in rows:
            rm = r.get("related_media") or []
            if not isinstance(rm, list):
                continue
            for cat in rm:
                if not isinstance(cat, dict):
                    continue
                items = cat.get("items") or []
                if not isinstance(items, list):
                    continue
                for ii, item in enumerate(items):
                    if not isinstance(item, dict):
                        continue
                    url = item.get("url")
                    if not url or not isinstance(url, str):
                        continue
                    if not url.startswith(("http://", "https://")):
                        continue
                    if is_youtube(url):
                        continue  # validated separately via oembed
                    out.append({
                        "lesson_id": r["id"],
                        "lesson_slug": r["slug"],
                        "unit_slug": u["slug"],
                        "category": cat.get("category"),
                        "item_index": ii,
                        "title": item.get("title"),
                        "url": url,
                    })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject_slug")
    ap.add_argument("--unit-sort-min", type=int, default=None)
    ap.add_argument("--report-out", type=str, default=None,
                    help="Write JSON report to this path")
    args = ap.parse_args()

    print(f"=== URL audit: {args.subject_slug} ===")
    if args.unit_sort_min is not None:
        print(f"  scoped to units with sort_order >= {args.unit_sort_min}")

    targets = collect_urls(args.subject_slug, args.unit_sort_min)
    print(f"  Total non-YouTube URLs to check: {len(targets)}")

    if not targets:
        return

    # Dedupe so we don't HEAD the same URL multiple times if it appears in many lessons
    unique_urls = list({t["url"] for t in targets})
    print(f"  Unique URLs: {len(unique_urls)}")

    results = {}
    with ThreadPoolExecutor(max_workers=PARALLEL) as ex:
        futs = {ex.submit(check_url, u): u for u in unique_urls}
        for i, fut in enumerate(as_completed(futs), 1):
            url, status, detail = fut.result()
            results[url] = (status, detail)
            if i % 25 == 0:
                ok = sum(1 for s, _ in results.values() if s == "ok")
                bad = sum(1 for s, _ in results.values() if s in ("broken", "error"))
                print(f"  ... {i}/{len(unique_urls)} (ok={ok} broken={bad})")

    # Map back to lesson context
    broken = []
    ok_count = 0
    for t in targets:
        status, detail = results[t["url"]]
        if status == "ok":
            ok_count += 1
        else:
            broken.append({**t, "status": status, "detail": detail})

    pct = (len(broken) / len(targets) * 100) if targets else 0
    print(f"\n  RESULT: {ok_count}/{len(targets)} OK, {len(broken)} broken ({pct:.1f}%)")

    if broken:
        print(f"\n  Broken URLs:")
        for b in broken[:30]:
            print(f"    [{b['status']}/{b['detail']}] {b['unit_slug']}/L{b['lesson_slug'][:30]:30s}  {b['url'][:80]}")
        if len(broken) > 30:
            print(f"    ... +{len(broken) - 30} more")

    if args.report_out:
        with open(args.report_out, "w", encoding="utf-8") as f:
            json.dump({
                "subject_slug": args.subject_slug,
                "unit_sort_min": args.unit_sort_min,
                "total": len(targets),
                "ok": ok_count,
                "broken_count": len(broken),
                "broken_pct": round(pct, 2),
                "broken": broken,
            }, f, indent=2)
        print(f"\n  Report written to: {args.report_out}")


if __name__ == "__main__":
    main()
