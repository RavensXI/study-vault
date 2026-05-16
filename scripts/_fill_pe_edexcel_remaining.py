"""
Fill the 7 remaining hero images for physical-education-edexcel using Wikimedia.
Runs after _batch_heroes_pe_edexcel.py when Unsplash rate limit is exhausted.

Usage: python scripts/_fill_pe_edexcel_remaining.py [--dry-run]
"""
import argparse
import os
import sys
import time
import tempfile
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.wikimedia import search_wikimedia, download_image, resize_and_compress
from lib.hero_index import add_to_index
from lib.r2 import get_r2_client, IMAGES_BUCKET

SUBJECT_SLUG = "physical-education-edexcel"

# Wikimedia search queries for the 7 lessons that didn't get Unsplash images.
# Wikimedia has 4-second delays between requests (rate courtesy).
REMAINING = [
    {
        "title": "Physical, Emotional and Social Wellbeing",
        "unit_slug": "health-and-performance",
        "lesson_number": 1,
        "queries": ["sport team youth activity", "community sport group", "sport participation group"],
    },
    {
        "title": "Diet, Nutrition and Hydration",
        "unit_slug": "health-and-performance",
        "lesson_number": 3,
        "queries": ["healthy food vegetables colourful", "healthy food fruit vegetables", "balanced diet food"],
    },
    {
        "title": "Classification of Skills and Practice Structures",
        "unit_slug": "health-and-performance",
        "lesson_number": 4,
        "queries": ["basketball training drill", "sport training drill", "athlete practice session"],
    },
    {
        "title": "Guidance and Feedback in Sport",
        "unit_slug": "health-and-performance",
        "lesson_number": 6,
        "queries": ["basketball coaching clinic", "sport coaching athlete", "athletics coach training"],
    },
    {
        "title": "Mental Preparation for Performance",
        "unit_slug": "health-and-performance",
        "lesson_number": 7,
        "queries": ["athlete warm up stretching sport", "sport warmup stretch", "yoga meditation indoor"],
    },
    {
        "title": "Ethical Behaviour and Deviance in Sport",
        "unit_slug": "health-and-performance",
        "lesson_number": 10,
        "queries": ["football referee match", "referee sport football", "sport fair play handshake"],
    },
    {
        "title": "Performance Enhancing Drugs (Recap and Application)",
        "unit_slug": "health-and-performance",
        "lesson_number": 11,
        "queries": ["laboratory scientist testing", "medical laboratory testing", "scientist prepares samples laboratory"],
    },
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sb = get_client()
    subj = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").single().execute().data
    sid = subj["id"]
    units = sb.table("units").select("id,slug,name").eq("subject_id", sid).execute().data
    unit_map = {u["slug"]: (u["id"], u["name"]) for u in units}

    total_ok = 0
    total_miss = 0

    for spec in REMAINING:
        title = spec["title"]
        unit_slug = spec["unit_slug"]
        ln = spec["lesson_number"]
        queries = spec["queries"]

        uid, uname = unit_map.get(unit_slug, (None, None))
        if not uid:
            print(f"[ERR] unit {unit_slug} not found")
            continue

        lesson = sb.table("lessons").select("id,title,hero_image_url").eq("unit_id", uid).eq("lesson_number", ln).single().execute().data
        if not lesson:
            print(f"[ERR] L{ln:02d} not found in {unit_slug}")
            continue
        if lesson.get("hero_image_url"):
            print(f"[SKIP] L{ln:02d} {title} — already has hero")
            continue

        print(f"\n  L{ln:02d} {title}")
        found = None

        for q in queries:
            print(f"    Wikimedia: {q!r}")
            results = search_wikimedia(q, limit=10)
            if not results:
                print(f"      no results")
                time.sleep(4)
                continue
            top = results[0]
            print(f"      found: {top['title']} ({top['width']}x{top['height']})")
            if args.dry_run:
                found = {"url": top["url"], "alt": top["title"], "caption": "Photo via Wikimedia Commons", "_dry": True}
                break
            try:
                tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
                tmp_dest = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
                download_image(top["url"], tmp_src)
                resize_and_compress(tmp_src, tmp_dest, max_width=1200, quality=82)
                r2_key = f"{SUBJECT_SLUG}/{unit_slug}/lesson-{ln:02d}-hero.jpg"
                r2 = get_r2_client()
                with open(tmp_dest, "rb") as f:
                    r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=f.read(), ContentType="image/jpeg")
                os.unlink(tmp_src)
                os.unlink(tmp_dest)
                r2_url = f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"
                alt = top["title"].replace("File:", "").split(".")[0]
                caption = "Photo via Wikimedia Commons"
                try:
                    add_to_index(
                        title=alt,
                        description=caption,
                        subject_slug=SUBJECT_SLUG,
                        subject_name="Physical Education",
                        unit_slug=unit_slug,
                        unit_name=uname,
                        lesson_slug=f"{unit_slug}-l{ln:02d}",
                        hero_url=r2_url,
                    )
                except Exception as e:
                    print(f"      index err: {e}")
                found = {"url": r2_url, "alt": alt, "caption": caption}
                break
            except Exception as e:
                print(f"      download err: {e}")
            time.sleep(4)

        if not found:
            print(f"      [MISS] no image found")
            total_miss += 1
            continue
        if args.dry_run or found.get("_dry"):
            print(f"      [DRY] would set hero: {found['url'][:70]}")
            continue

        sb.table("lessons").update({
            "hero_image_url": found["url"],
            "hero_image_alt": found["alt"],
            "hero_image_caption": found["caption"],
            "hero_image_position": "center 50%",
        }).eq("id", lesson["id"]).execute()
        print(f"      [OK] downloaded — {found['caption'][:80]}")
        total_ok += 1
        time.sleep(1)

    print(f"\n=== Done: {total_ok} OK, {total_miss} missed ===")


if __name__ == "__main__":
    main()
