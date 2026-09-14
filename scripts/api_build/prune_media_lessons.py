# -*- coding: utf-8 -*-
"""Audit and prune the related-media links on the lessons named by id.

Generalised from the Latin build's pruner (13-14 Sep 2026) for unit add-on builds.

Self-contained: HEAD-checks every non-YouTube URL, oembed-checks every YouTube
id (which is the same check the pre-ship verifier runs), then removes the dead
items from Supabase. The "Lesson Podcast" placeholder carries a null url and is
never touched. Empty categories are dropped.

Reports any lesson left with fewer than the verifier's minimum so it can be
back-filled rather than silently shipped thin.

Usage:
    python scripts/api_build/prune_media_lessons.py --ids <id,id,...>            # audit only
    python scripts/api_build/prune_media_lessons.py --ids <id,id,...> --apply    # prune
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))  # scripts/api_build -> repo
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import re  # noqa: E402
import requests  # noqa: E402
import driver as D  # noqa: E402

UA = ("Mozilla/5.0 (compatible; StudyVault-LinkAudit/1.0; "
      "+https://studyvault.co.uk)")
YT_RE = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w\-]{11})")
MIN_ITEMS = 8


def check(url):
    m = YT_RE.search(url)
    if m:
        try:
            r = requests.get("https://www.youtube.com/oembed",
                             params={"url": "https://www.youtube.com/watch?v=" + m.group(1),
                                     "format": "json"},
                             timeout=10, headers={"User-Agent": UA})
            return (url, "ok" if r.status_code == 200 else "dead", r.status_code)
        except Exception as e:
            return (url, "error", str(e)[:50])
    try:
        r = requests.head(url, allow_redirects=True, timeout=10,
                          headers={"User-Agent": UA, "Accept": "*/*"})
        if r.status_code < 400:
            return (url, "ok", r.status_code)
        if r.status_code in (403, 405, 429):
            r2 = requests.get(url, allow_redirects=True, timeout=12, stream=True,
                              headers={"User-Agent": UA, "Accept": "*/*"})
            code = r2.status_code
            r2.close()
            return (url, "ok" if code < 400 else "dead", code)
        return (url, "dead", r.status_code)
    except Exception as e:
        return (url, "error", str(e)[:50])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="comma-separated lesson ids")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    cfg = {"run_dir": os.path.join(os.environ.get("TEMP", "."), "prune_media_lessons")}
    lessons = D.supa(cfg, "GET", "/rest/v1/lessons?id=in.(%s)&select=id,lesson_number,title,related_media"
                     % args.ids)

    urls = set()
    for l in lessons:
        for cat in l.get("related_media") or []:
            for item in cat.get("items") or []:
                if item.get("url"):
                    urls.add(item["url"])
    print("checking %d unique URLs across %d lessons" % (len(urls), len(lessons)))

    results = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(check, u): u for u in urls}
        for f in as_completed(futs):
            url, status, detail = f.result()
            results[url] = (status, detail)

    dead = {u for u, (s, _) in results.items() if s != "ok"}
    print("dead or unreachable: %d of %d" % (len(dead), len(urls)))
    for u in sorted(dead):
        print("  [%s/%s] %s" % (results[u][0], results[u][1], u[:100]))

    for l in lessons:
        rm = l.get("related_media") or []
        out, removed = [], 0
        for cat in rm:
            items = [i for i in (cat.get("items") or []) if not i.get("url") or i["url"] not in dead]
            removed += len(cat.get("items") or []) - len(items)
            if items:
                out.append({"category": cat.get("category"), "items": items} | {k: v for k, v in cat.items() if k not in ("category", "items")})
        kept = sum(len(c["items"]) for c in out)
        flag = "  THIN (<%d)" % MIN_ITEMS if kept < MIN_ITEMS else ""
        print("L%s %s: kept %d, removed %d%s" % (l["lesson_number"], (l["title"] or "")[:50], kept, removed, flag))
        if args.apply and removed:
            D.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["id"], {"related_media": out})
    print("applied" if args.apply else "audit only (add --apply to prune)")


if __name__ == "__main__":
    main()
