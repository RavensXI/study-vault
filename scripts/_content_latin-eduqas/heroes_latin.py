# -*- coding: utf-8 -*-
"""Phase 4 hero images for GCSE Latin (latin-eduqas), free tier — 33 lessons.

Goes through `lib.hero_pipeline.HeroFinder`, which is the only sanctioned path:
every candidate is downloaded and graded by a vision model before it is used,
the caption describes the image that actually shipped, one image is never used
twice, and the file lands under this subject's own R2 folder.

Classical Civilisation (OCR) is the one legitimate same-family reuse pool for
this subject — Roman photographs of the Forum, temples, mosaics and inscriptions
serve both — so its heroes are offered as candidates, still vision-gated.

Usage:
    python scripts/_content_latin-eduqas/heroes_latin.py [--unit slug] [--dry-run]
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402
from lib.hero_pipeline import HeroFinder  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")
SUBJECT_SLUG = "latin-eduqas"
SUBJECT_NAME = "Latin"
FAMILY_POOL_SLUG = "classical-civilisation-ocr"


def reuse_pool(cfg):
    subs = D.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id"
                  % FAMILY_POOL_SLUG)
    if not subs:
        return []
    units = D.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id"
                   % subs[0]["id"])
    pool = []
    for u in units:
        rows = D.supa(cfg, "GET",
                      "/rest/v1/lessons?unit_id=eq.%s&select=title,hero_image_url,"
                      "hero_image_caption&hero_image_url=not.is.null" % u["id"])
        for r in rows:
            pool.append({"url": r["hero_image_url"], "title": r["title"],
                         "caption": r.get("hero_image_caption") or ""})
    return pool


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unit")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = D.load_config(CFG_PATH)
    st = D.load_state(cfg)
    subject_id = st["subject_id"]
    units = D.supa(cfg, "GET",
                   "/rest/v1/units?subject_id=eq.%s&select=id,slug,name,sort_order"
                   "&order=sort_order" % subject_id)
    pool = reuse_pool(cfg)
    print("same-family reuse pool: %d Classical Civilisation heroes" % len(pool))

    finder = HeroFinder()
    # never hand the same image to two subjects' lessons in this run
    done = fail = 0
    for u in units:
        if args.unit and u["slug"] != args.unit:
            continue
        lessons = D.supa(cfg, "GET",
                         "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,"
                         "title,description,hero_image_url&order=lesson_number" % u["id"])
        for l in lessons:
            if (l.get("hero_image_url") or "").strip():
                print("  SKIP %s L%02d — already has a hero" % (u["slug"], l["lesson_number"]))
                finder.used.add(l["hero_image_url"])
                continue
            print("\n  %s L%02d  %s" % (u["slug"], l["lesson_number"], l["title"]))
            if args.dry_run:
                continue
            res = finder.find(
                subject_slug=SUBJECT_SLUG, subject_name=SUBJECT_NAME,
                unit_slug=u["slug"], unit_name=u["name"],
                lesson_number=l["lesson_number"], title=l["title"],
                description=l.get("description") or "", reuse_pool=pool)
            if not res:
                print("      NO HERO FOUND")
                fail += 1
                continue
            D.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["id"], {
                "hero_image_url": res["url"],
                "hero_image_alt": res["shows"],
                "hero_image_caption": res["caption"],
                "hero_image_position": "center",
            })
            print("      -> %s" % res["caption"])
            done += 1

    print("\nheroes: %d assigned, %d failed, %d vision calls"
          % (done, fail, finder.vision_calls))


if __name__ == "__main__":
    main()
