# -*- coding: utf-8 -*-
"""Phase 6 finishing pass for GCSE Latin.

Sets every unit's `image_url` from its first lesson that has a hero (naked units
render as empty grey cards in the browse grid, and the verifier fails on them),
then prints the coverage table the pre-ship check wants to see.

Usage: python scripts/_content_latin-eduqas/finish_latin.py [--apply]
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    cfg = D.load_config(CFG_PATH)
    st = D.load_state(cfg)
    sub = D.supa(cfg, "GET", "/rest/v1/subjects?id=eq.%s&select=slug,status,settings"
                 % st["subject_id"])[0]
    units = D.supa(cfg, "GET",
                   "/rest/v1/units?subject_id=eq.%s&select=id,slug,name,image_url,"
                   "lesson_count,sort_order&order=sort_order" % st["subject_id"])
    practice = set((sub.get("settings") or {}).get("practice_units") or [])

    print("%-28s %-8s %5s %5s %5s %5s %5s %5s"
          % ("unit", "format", "less", "desc", "hero", "media", "narr", "body"))
    for u in units:
        rows = D.supa(cfg, "GET",
                      "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,"
                      "description,hero_image_url,related_media,narration_manifest,"
                      "content_html,practice_data&order=lesson_number" % u["id"])
        heroes = [r for r in rows if (r.get("hero_image_url") or "").strip()]
        if heroes and not (u.get("image_url") or "").strip():
            img = heroes[0]["hero_image_url"]
            if args.apply:
                D.supa(cfg, "PATCH", "/rest/v1/units?id=eq.%s" % u["id"],
                       {"image_url": img})
            print("  unit image %s <- %s" % (u["slug"], img.split("/")[-1]))
        fmt = "practice" if u["slug"] in practice else "article"
        body = sum(1 for r in rows
                   if (r.get("practice_data") if fmt == "practice"
                       else (r.get("content_html") or "").strip()))
        print("%-28s %-8s %5d %5d %5d %5d %5d %5d"
              % (u["slug"], fmt, len(rows),
                 sum(1 for r in rows if (r.get("description") or "").strip()),
                 len(heroes),
                 sum(1 for r in rows if r.get("related_media")),
                 sum(1 for r in rows if r.get("narration_manifest")),
                 body))
    if not args.apply:
        print("\nDRY RUN — pass --apply to write unit image_url values")


if __name__ == "__main__":
    main()
