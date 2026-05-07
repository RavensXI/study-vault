"""Hero image fetch for Sociology Eduqas/WJEC.

Each JSON in scripts/_content_sociology-eduqas/lessons/ uses flat _lesson_id;
this script reads hero_keywords + caption, finds/downloads via Unsplash,
uploads to R2, and updates the matching lesson row.
"""
import argparse
import glob
import json
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.hero_index import search_heroes, add_to_index
from lib.r2 import get_r2_client, IMAGES_BUCKET
from lib.wikimedia import resize_and_compress

REUSE_MIN_SCORE = 6
SUBJECT_SLUG = "sociology-eduqas"
LESSON_DIR = Path(__file__).parent / "_content_sociology-eduqas" / "lessons"


def find_or_download(keywords, unit_slug, lesson_number, no_reuse=False):
    if not no_reuse and keywords:
        for query in keywords:
            matches = search_heroes(query)
            if matches:
                top = matches[0]
                if top.get("score", 0) >= REUSE_MIN_SCORE:
                    print(f"      reuse: ...{top['hero_url'][-50:]}  (score {top['score']})")
                    desc = top.get("description") or ""
                    caption = desc if desc.startswith("Photo: ") else "Photo via Unsplash"
                    return {"url": top["hero_url"], "alt": top.get("title", query),
                            "caption": caption, "reused": True}

    for query in keywords:
        try:
            results = search_unsplash(query, per_page=5)
        except Exception as e:
            print(f"      Unsplash error '{query}': {e}")
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
        photographer = top.get("photographer") or ""
        caption = f"Photo: {photographer} / Unsplash" if photographer else "Photo via Unsplash"

        try:
            tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            tmp_dest = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            urllib.request.urlretrieve(image_url, tmp_src)
            resize_and_compress(tmp_src, tmp_dest, max_width=1200, quality=82)
            r2_key = f"{SUBJECT_SLUG}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
            r2 = get_r2_client()
            with open(tmp_dest, "rb") as f:
                r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=f.read(), ContentType="image/jpeg")
            os.unlink(tmp_src); os.unlink(tmp_dest)
            r2_url = f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"
            try:
                add_to_index(
                    title=alt_text,
                    description=f"Photo: {photographer} / Unsplash",
                    subject_slug=SUBJECT_SLUG,
                    subject_name="Sociology",
                    unit_slug=unit_slug,
                    unit_name=unit_slug,
                    lesson_slug=f"{unit_slug}-l{lesson_number:02d}",
                    hero_url=r2_url,
                )
            except Exception as e:
                print(f"      index add error: {e}")
            return {"url": r2_url, "alt": alt_text, "caption": caption, "reused": False}
        except Exception as e:
            print(f"      download/upload error '{query}': {e}")
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-reuse", action="store_true")
    args = ap.parse_args()

    sb = get_client()
    files = sorted(LESSON_DIR.glob("*.json"))
    print(f"Found {len(files)} lessons")

    ok = skip = fail = 0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        lid = data["_lesson_id"]
        unit_slug = data["_unit_slug"]
        ln = data["_lesson_number"]
        keywords = data.get("hero_keywords") or []
        caption_override = data.get("hero_image_caption") or ""

        row = sb.table("lessons").select("id, title, hero_image_url").eq("id", lid).execute().data
        if not row:
            print(f"[ERR] lesson {lid} not in DB")
            fail += 1; continue
        title = row[0]["title"]
        if row[0].get("hero_image_url"):
            print(f"[SKIP] L{ln:02d} {title[:50]}  (already has hero)")
            skip += 1; continue

        print(f"[GET]  L{ln:02d} {title[:50]}  keywords={keywords[:3]}")
        result = find_or_download(keywords, unit_slug, ln, args.no_reuse)
        if not result:
            print(f"       FAIL no image found")
            fail += 1; continue
        # Prefer attribution caption from result (honest); fall back to agent caption
        sb.table("lessons").update({
            "hero_image_url": result["url"],
            "hero_image_alt": result["alt"],
            "hero_image_caption": result["caption"] or caption_override,
        }).eq("id", lid).execute()
        ok += 1

    print(f"\n  ok={ok} skip={skip} fail={fail}")


if __name__ == "__main__":
    main()
