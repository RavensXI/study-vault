# -*- coding: utf-8 -*-
"""Audit and prune the related-media links on every Latin lesson.

Self-contained: HEAD-checks every non-YouTube URL, oembed-checks every YouTube
id (which is the same check the pre-ship verifier runs), then removes the dead
items from Supabase. The "Lesson Podcast" placeholder carries a null url and is
never touched. Empty categories are dropped.

Reports any lesson left with fewer than the verifier's minimum so it can be
back-filled rather than silently shipped thin.

Usage:
    python scripts/_content_latin-eduqas/prune_media_latin.py            # audit only
    python scripts/_content_latin-eduqas/prune_media_latin.py --apply    # prune
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import re  # noqa: E402
import requests  # noqa: E402
import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")
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
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    cfg = D.load_config(CFG_PATH)
    st = D.load_state(cfg)
    units = D.supa(cfg, "GET",
                   "/rest/v1/units?subject_id=eq.%s&select=id,slug&order=sort_order"
                   % st["subject_id"])
    lessons = []
    for u in units:
        rows = D.supa(cfg, "GET",
                      "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,"
                      "related_media&order=lesson_number" % u["id"])
        for r in rows:
            r["unit_slug"] = u["slug"]
            lessons.append(r)

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
        for i, f in enumerate(as_completed(futs), 1):
            url, status, detail = f.result()
            results[url] = (status, detail)
            if i % 40 == 0:
                bad = sum(1 for s, _ in results.values() if s != "ok")
                print("  ... %d/%d (%d bad)" % (i, len(urls), bad))

    dead = {u for u, (s, _) in results.items() if s != "ok"}
    print("\ndead or unreachable: %d of %d" % (len(dead), len(urls)))
    for u in sorted(dead)[:40]:
        print("  [%s/%s] %s" % (results[u][0], results[u][1], u[:100]))

    thin = []
    for l in lessons:
        rm = l.get("related_media") or []
        out, removed = [], 0
        for cat in rm:
            items = [i for i in (cat.get("items") or [])
                     if not i.get("url") or i["url"] not in dead]
            removed += len(cat.get("items") or []) - len(items)
            if items:
                out.append({"category": cat.get("category"), "items": items})
        total = sum(len(c["items"]) for c in out)
        real = sum(1 for c in out for i in c["items"] if i.get("url"))
        if removed and args.apply:
            D.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["id"],
                   {"related_media": out})
        if total < MIN_ITEMS or real < MIN_ITEMS - 1:
            thin.append((l["unit_slug"], l["lesson_number"], l["title"], total, real))
        if removed:
            print("  %s L%02d: -%d dead, %d items left"
                  % (l["unit_slug"], l["lesson_number"], removed, total))

    print("\n%s" % ("pruned" if args.apply else "DRY RUN — nothing written"))
    if thin:
        print("lessons below the minimum (%d items) — back-fill these:" % MIN_ITEMS)
        for t in thin:
            print("  %s L%02d %s — %d items (%d with a url)" % t)
    else:
        print("every lesson still carries at least %d items" % MIN_ITEMS)


if __name__ == "__main__":
    main()
