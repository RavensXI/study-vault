# -*- coding: utf-8 -*-
"""Vision-gated heroes for a rebuilt OCR poetry cluster.

Runs the standard HeroFinder (photographs only, vision-gated, two-part caption)
over the fifteen lessons of one cluster and patches hero_image_url,
hero_image_caption, hero_image_alt and hero_image_position.

Every hero already in use across english-literature-ocr is pre-seeded into the
finder's used-set, so a rebuilt lesson can never duplicate an image the subject
already shows. Resumable: a lesson that already has a hero is skipped unless
--force is passed.

Usage: python scripts/api_build/heroes_ocr_cluster.py conflict
"""
import io
import json
import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

REPO = r"C:\Users\tshau\Documents\Study Vault"
sys.path.insert(0, os.path.join(REPO, "scripts"))

from lib.supabase_client import get_client
from lib.hero_pipeline import HeroFinder

SUBJECT_SLUG = "english-literature-ocr"
SUBJECT_NAME = "English Literature"


def norm(url):
    return (url or "").split("?")[0]


def main(cluster, force=False):
    cfg = json.load(io.open(os.path.join(REPO, "scripts", "api_build",
                                         "config_englit-ocr-%s.json" % cluster), encoding="utf-8"))
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    unit = plan["article_units"][0]

    sb = get_client()
    subj = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG) \
        .is_("school_id", "null").execute().data[0]
    urow = sb.table("units").select("id,name,slug").eq("subject_id", subj["id"]) \
        .eq("slug", unit["slug"]).execute().data[0]
    lessons = sb.table("lessons").select("id,lesson_number,title,description,hero_image_url") \
        .eq("unit_id", urow["id"]).order("lesson_number").execute().data
    print("unit %s: %d lessons" % (urow["slug"], len(lessons)))

    finder = HeroFinder()
    mine = {l["id"] for l in lessons}
    for u in sb.table("units").select("id").eq("subject_id", subj["id"]).execute().data:
        for l in sb.table("lessons").select("id,hero_image_url").eq("unit_id", u["id"]).execute().data:
            if l["id"] not in mine and l.get("hero_image_url"):
                finder.used.add(norm(l["hero_image_url"]))
    print("pre-seeded %d kept hero images" % len(finder.used))

    done = failed = 0
    for l in lessons:
        if l.get("hero_image_url") and not force:
            print("L%02d skip (hero present)" % l["lesson_number"])
            continue
        print("\n--- L%02d %s" % (l["lesson_number"], (l["title"] or "")[:60]))
        result = finder.find(
            subject_slug=SUBJECT_SLUG, subject_name=SUBJECT_NAME,
            unit_slug=urow["slug"], unit_name=urow["name"],
            lesson_number=l["lesson_number"], title=l["title"] or "",
            description=l.get("description") or "")
        if not result:
            print("    [FAIL] no acceptable image")
            failed += 1
            continue
        sb.table("lessons").update({
            "hero_image_url": result["url"],
            "hero_image_caption": result["caption"],
            "hero_image_position": "center center",
            "hero_image_alt": "%s — %s, %s" % (l["title"], urow["name"], SUBJECT_NAME),
        }).eq("id", l["id"]).execute()
        done += 1
        print("    [OK] %s: %s" % (result["source"], result["caption"][:90]))
    print("\nheroes: %d set, %d failed" % (done, failed))


if __name__ == "__main__":
    main(sys.argv[1], force="--force" in sys.argv)
