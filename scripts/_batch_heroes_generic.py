"""
Generic batch hero downloader for new-pipeline subjects.

Reads content JSON files that include `hero_keywords` and `hero_image_caption`,
matches them to Supabase lessons by (subject_slug, unit_slug, lesson_number),
and downloads + uploads hero images.

Usage:
  python scripts/_batch_heroes_generic.py scripts/_gen_business/
  python scripts/_batch_heroes_generic.py scripts/_gen_business/ --dry-run
  python scripts/_batch_heroes_generic.py scripts/_gen_business/ --no-reuse

Each JSON file must have:
  _meta: { subject_slug, exam_board, school_id, unit_slug, lesson_number }
  hero_keywords: [...]
  hero_image_caption: "..."
"""
import argparse
import io
import os
import sys
import glob
import json
import time
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.hero_index import search_heroes, add_to_index
from lib.r2 import get_r2_client, upload_file_to_r2, IMAGES_BUCKET
from lib.wikimedia import resize_and_compress

REUSE_MIN_SCORE = 6


def find_or_download(keywords, subject_slug, unit_slug, lesson_number, no_reuse=False, dry_run=False):
    """Check the hero index for reuse; if no match, search Unsplash and download."""
    if not no_reuse and keywords:
        for query in keywords:
            matches = search_heroes(query)
            if matches:
                top = matches[0]
                if top.get("score", 0) >= REUSE_MIN_SCORE:
                    print(f"      reuse: {top['hero_url'][:70]}...  (score {top['score']}, query '{query}')")
                    return {"url": top["hero_url"], "alt": top.get("title", query), "reused": True}

    if dry_run:
        return None

    # Search Unsplash
    for query in keywords:
        try:
            results = search_unsplash(query, per_page=5)
        except Exception as e:
            print(f"      Unsplash search error for '{query}': {e}")
            continue
        if not results:
            continue
        top = results[0]
        try:
            trigger_unsplash_download(top.get("_download_location", ""))
        except Exception:
            pass
        image_url = top["url"]
        alt_text = top.get("title") or query
        # Download + compress + upload to R2
        try:
            import tempfile
            tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            tmp_dest = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            urllib.request.urlretrieve(image_url, tmp_src)
            resize_and_compress(tmp_src, tmp_dest, max_width=1200, quality=82)
            r2_key = f"{subject_slug}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
            r2 = get_r2_client()
            with open(tmp_dest, "rb") as f:
                r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=f.read(), ContentType="image/jpeg")
            os.unlink(tmp_src); os.unlink(tmp_dest)
            r2_url = f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"
            # Add to index
            try:
                add_to_index(
                    title=alt_text,
                    description=alt_text,
                    subject_slug=subject_slug,
                    subject_name=subject_slug,
                    unit_slug=unit_slug,
                    unit_name=unit_slug,
                    lesson_slug=f"{unit_slug}-l{lesson_number:02d}",
                    hero_url=r2_url,
                )
            except Exception as e:
                print(f"      index add error: {e}")
            return {"url": r2_url, "alt": alt_text, "reused": False}
        except Exception as e:
            print(f"      download/upload error for '{query}': {e}")
            continue
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-reuse", action="store_true")
    args = parser.parse_args()

    sb = get_client()
    paths = sorted(glob.glob(os.path.join(args.directory, "*.json")))
    print(f"Found {len(paths)} JSON files")

    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        meta = data.get("_meta") or {}
        if not meta:
            continue

        subject_slug = meta["subject_slug"]
        unit_slug = meta["unit_slug"]
        lesson_number = meta["lesson_number"]
        exam_board = meta.get("exam_board")
        school_id = meta.get("school_id")
        keywords = data.get("hero_keywords", []) or []
        caption = data.get("hero_image_caption", "") or ""

        # Find lesson id
        q = sb.table("subjects").select("id").eq("slug", subject_slug)
        if exam_board:
            q = q.eq("exam_board", exam_board)
        if school_id is None:
            q = q.is_("school_id", "null")
        else:
            q = q.eq("school_id", school_id)
        subj = q.execute().data
        if not subj:
            print(f"[ERR] subject {subject_slug} not found for {p}")
            continue
        subject_id = subj[0]["id"]
        unit = sb.table("units").select("id").eq("subject_id", subject_id).eq("slug", unit_slug).execute().data
        if not unit:
            print(f"[ERR] unit {unit_slug} not found")
            continue
        lesson = sb.table("lessons").select("id,title,hero_image_url").eq("unit_id", unit[0]["id"]).eq("lesson_number", lesson_number).execute().data
        if not lesson:
            print(f"[ERR] lesson {lesson_number} not found in {unit_slug}")
            continue
        lid = lesson[0]["id"]
        title = lesson[0]["title"]
        existing_hero = lesson[0].get("hero_image_url")

        if existing_hero:
            print(f"[SKIP] L{lesson_number:02d} {title[:45]}  (already has hero)")
            continue

        print(f"\n  L{lesson_number:02d} {title[:60]}")
        print(f"      keywords: {keywords[:3]}")

        result = find_or_download(keywords, subject_slug, unit_slug, lesson_number,
                                  no_reuse=args.no_reuse, dry_run=args.dry_run)
        if not result:
            print(f"      [MISS] no image found")
            continue

        if args.dry_run:
            print(f"      [DRY] would set hero_image_url={result['url']}")
            continue

        sb.table("lessons").update({
            "hero_image_url": result["url"],
            "hero_image_alt": result["alt"],
            "hero_image_caption": caption,
            "hero_image_position": "center 50%",
        }).eq("id", lid).execute()
        tag = "reused" if result["reused"] else "downloaded"
        print(f"      [OK] {tag}  caption={caption[:50] if caption else '(none)'}")
        time.sleep(1.0)  # rate-limit friendliness


if __name__ == "__main__":
    main()
