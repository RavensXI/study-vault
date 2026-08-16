# -*- coding: utf-8 -*-
"""Heroes for every music-ocr lesson missing one, via the vision-gated
lib/hero_pipeline. Copied practice lessons seed the finder's reuse pool
with their music-aqa counterpart's hero — through the RENUMBERING map the
copier used (aos2-concerto-listening is chronological, not source order).
Film L1-L3 arrived with heroes from the eduqas copy and are skipped by
the has-hero guard. Articles get fresh finds.

Run: python ocr_heroes.py     (resumable — skips lessons with a hero)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from lib.hero_pipeline import HeroFinder

# ocr unit -> (aqa unit, {ocr lesson_number: aqa lesson_number})
REUSE_MAP = {
    "listening-skills": ("listening-skills", {1: 1, 2: 2, 3: 3}),
    "score-reading": ("score-reading", {1: 1, 2: 2, 3: 3, 4: 4}),
    "aos2-concerto-listening": ("western-classical-1650-1910",
                                {1: 5, 2: 3, 3: 1, 4: 2, 5: 4, 6: 6, 7: 8}),
    "aos45-unfamiliar-listening": ("aos-listening", {1: 1, 2: 2, 3: 3}),
}


def main():
    sb = get_client()
    subs = {s["slug"]: s for s in sb.table("subjects")
            .select("id,slug,name").execute().data}
    units = sb.table("units").select("id,slug,name,subject_id").execute().data
    ocr = subs["music-ocr"]["id"]
    aqa = subs["music-aqa"]["id"]
    aqa_units = {u["slug"]: u["id"] for u in units if u["subject_id"] == aqa}

    finder = HeroFinder()
    for u in [x for x in units if x["subject_id"] == ocr]:
        for l in sb.table("lessons").select("hero_image_url") \
                .eq("unit_id", u["id"]).execute().data:
            if l.get("hero_image_url"):
                finder.used.add(l["hero_image_url"])

    done = failed = 0
    for u in [x for x in units if x["subject_id"] == ocr]:
        rows = sb.table("lessons").select(
            "id,lesson_number,title,description,hero_image_url") \
            .eq("unit_id", u["id"]).order("lesson_number").execute().data
        for l in rows:
            if l.get("hero_image_url"):
                continue
            reuse = None
            if u["slug"] in REUSE_MAP:
                src_slug, num_map = REUSE_MAP[u["slug"]]
                src_n = num_map.get(l["lesson_number"])
                if src_n:
                    src = sb.table("lessons") \
                        .select("hero_image_url,hero_image_caption") \
                        .eq("unit_id", aqa_units[src_slug]) \
                        .eq("lesson_number", src_n).execute().data
                    if src and src[0].get("hero_image_url"):
                        reuse = [{"url": src[0]["hero_image_url"],
                                  "caption": src[0].get("hero_image_caption")}]
            print("\n%s L%d: %s" % (u["slug"], l["lesson_number"],
                                    l["title"][:55]))
            r = finder.find("music-ocr", "Music", u["slug"], u["name"],
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
