# -*- coding: utf-8 -*-
"""Heroes for every music-edexcel lesson missing one, via the
vision-gated lib/hero_pipeline. Copied practice lessons seed the reuse
pool from their music-aqa counterparts (per-lesson source map — the
unfamiliar-listening unit draws from two AQA units). Articles get fresh
finds. Resumable.

Run: python edexcel_heroes.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from lib.hero_pipeline import HeroFinder

# edexcel unit -> {edexcel lesson_number: (aqa unit, aqa lesson_number)}
REUSE_MAP = {
    "listening-skills": {n: ("listening-skills", n) for n in (1, 2, 3)},
    "score-reading": {n: ("score-reading", n) for n in (1, 2, 3, 4)},
    "unfamiliar-listening": {1: ("western-classical-1650-1910", 3),
                             2: ("western-classical-1650-1910", 1),
                             3: ("aos-listening", 1),
                             4: ("aos-listening", 3)},
}


def main():
    sb = get_client()
    subs = {s["slug"]: s for s in sb.table("subjects")
            .select("id,slug,name").execute().data}
    units = sb.table("units").select("id,slug,name,subject_id").execute().data
    edx = subs["music-edexcel"]["id"]
    aqa = subs["music-aqa"]["id"]
    aqa_units = {u["slug"]: u["id"] for u in units if u["subject_id"] == aqa}

    finder = HeroFinder()
    for u in [x for x in units if x["subject_id"] == edx]:
        for l in sb.table("lessons").select("hero_image_url") \
                .eq("unit_id", u["id"]).execute().data:
            if l.get("hero_image_url"):
                finder.used.add(l["hero_image_url"])

    done = failed = 0
    for u in [x for x in units if x["subject_id"] == edx]:
        rows = sb.table("lessons").select(
            "id,lesson_number,title,description,hero_image_url") \
            .eq("unit_id", u["id"]).order("lesson_number").execute().data
        for l in rows:
            if l.get("hero_image_url"):
                continue
            reuse = None
            hit = REUSE_MAP.get(u["slug"], {}).get(l["lesson_number"])
            if hit:
                src_slug, src_n = hit
                src = sb.table("lessons") \
                    .select("hero_image_url,hero_image_caption") \
                    .eq("unit_id", aqa_units[src_slug]) \
                    .eq("lesson_number", src_n).execute().data
                if src and src[0].get("hero_image_url"):
                    reuse = [{"url": src[0]["hero_image_url"],
                              "caption": src[0].get("hero_image_caption")}]
            print("\n%s L%d: %s" % (u["slug"], l["lesson_number"],
                                    l["title"][:55]))
            r = finder.find("music-edexcel", "Music", u["slug"], u["name"],
                            l["lesson_number"], l["title"],
                            l.get("description"), reuse_pool=reuse)
            if not r:
                failed += 1
                print("   NO HERO FOUND")
                continue
            sb.table("lessons").update({
                "hero_image_url": r["url"],
                "hero_image_alt": r.get("shows") or r.get("caption"),
                "hero_image_caption": r.get("caption"),
            }).eq("id", l["id"]).execute()
            done += 1
            print("   set: %s" % r["url"][:80])
    print("\nheroes set: %d | failed: %d | vision calls: %d"
          % (done, failed, finder.vision_calls))


if __name__ == "__main__":
    main()
