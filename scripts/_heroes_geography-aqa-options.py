"""
Phase 4 hero images for the 9 Geography AQA optional-topic lessons.

  paper-1 L21-L25  (Cold Environments x2, Glacial x3)
  paper-2 L21-L24  (Food x2, Water x2)

Reads hero_keywords from scripts/_content_geography-aqa/_hero_keywords.json.
Per lesson: reuse from hero index (min_score>=4) -> Unsplash -> Wikimedia.
R2 key convention matches existing geography heroes: geography/{unit}/lesson-NN-hero.jpg
"""
import json
import os
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

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
from lib.wikimedia import search_wikimedia, resize_and_compress, MIN_FILE_SIZE
from lib.hero_index import search_heroes, add_to_index
from lib.r2 import get_r2_client, IMAGES_BUCKET

SUBJECT_SLUG = "geography-aqa"
R2_PREFIX = "geography"  # existing geography heroes live under geography/ on R2
R2_PUBLIC = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"
HERO_REUSE_MIN_SCORE = 4
SIDECAR = Path(SCRIPT_DIR) / "_content_geography-aqa" / "_hero_keywords.json"

LESSONS = [("paper-1", n) for n in range(21, 26)] + [("paper-2", n) for n in range(21, 25)]


def download_and_upload(url, r2_key, r2_client, source_hint=""):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t1:
        src = t1.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t2:
        dest = t2.name
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "StudyVault/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(src, "wb") as f:
                f.write(resp.read())
        if os.path.getsize(src) < MIN_FILE_SIZE:
            print(f"      [SKIP] too small from {source_hint}")
            return None
        resize_and_compress(src, dest, max_width=1200, quality=82)
        with open(dest, "rb") as f:
            r2_client.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=f.read(),
                                 ContentType="image/jpeg")
        print(f"      uploaded: {r2_key} ({os.path.getsize(dest)//1024}KB)")
        return f"{R2_PUBLIC}/{r2_key}"
    except Exception as e:
        print(f"      [ERROR] {source_hint} {url[:70]}: {e}")
        return None
    finally:
        for p in (src, dest):
            try:
                os.unlink(p)
            except OSError:
                pass


def find_hero(keywords, unit_slug, lesson_number, r2_client):
    query_str = " ".join(keywords)
    matches = search_heroes(query_str, min_score=HERO_REUSE_MIN_SCORE,
                            exclude_subjects=None)
    if matches:
        top = matches[0]
        print(f"      [REUSE] score={top['score']} {top['hero_url'][:66]}")
        return {"url": top["hero_url"], "source": "reused",
                "caption": top.get("description") or "Photo via Unsplash"}

    r2_key = f"{R2_PREFIX}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
    for query in keywords:
        print(f"      Unsplash: '{query}'")
        try:
            results = search_unsplash(query, per_page=10)
        except Exception as e:
            print(f"      Unsplash error: {e}")
            continue
        if not results:
            continue
        top = results[0]
        url = download_and_upload(top["url"], r2_key, r2_client, "unsplash")
        if url:
            try:
                trigger_unsplash_download(top.get("_download_location", ""))
            except Exception:
                pass
            return {"url": url, "source": "unsplash",
                    "_photographer": top.get("photographer", ""), "_query": query}
        time.sleep(1)

    for query in keywords:
        print(f"      Wikimedia: '{query}'")
        try:
            results = search_wikimedia(query, limit=20)
        except Exception as e:
            print(f"      Wikimedia error: {e}")
            continue
        for cand in results or []:
            img_url = cand.get("url") or cand.get("original_url", "")
            if not img_url:
                continue
            url = download_and_upload(img_url, r2_key, r2_client, "wikimedia")
            if url:
                title = cand.get("title", query).replace("File:", "").strip()
                return {"url": url, "source": "wikimedia",
                        "caption": f"Wikimedia Commons — {title[:80]}"}
            time.sleep(2)
        time.sleep(4)
    return None


def main():
    sb = get_client()
    r2 = get_r2_client()
    sidecar = json.loads(SIDECAR.read_text(encoding="utf-8"))

    subj = (sb.table("subjects").select("id,name").eq("slug", SUBJECT_SLUG)
            .is_("school_id", "null").single().execute().data)
    sid, subject_name = subj["id"], subj["name"]
    units = {u["slug"]: u for u in
             sb.table("units").select("id,slug,name").eq("subject_id", sid).execute().data}

    stats = {"reused": 0, "downloaded": 0, "failed": 0, "wikimedia": []}
    for unit_slug, ln in LESSONS:
        key = f"{unit_slug}/lesson-{ln:02d}"
        meta = sidecar.get(key, {})
        keywords = meta.get("hero_keywords") or []
        json_caption = meta.get("hero_image_caption", "")
        uid = units[unit_slug]["id"]
        lrow = (sb.table("lessons").select("id,title,hero_image_url")
                .eq("unit_id", uid).eq("lesson_number", ln).execute().data)
        if not lrow:
            print(f"\n--- {key} --- [ERR] no Supabase row")
            stats["failed"] += 1
            continue
        lesson = lrow[0]
        print(f"\n--- {key}  {lesson['title']} ---")
        print(f"  keywords: {keywords}")
        res = find_hero(keywords, unit_slug, ln, r2)
        if not res:
            print("  [FAIL] no image")
            stats["failed"] += 1
            continue

        src = res["source"]
        if src == "unsplash":
            ph = res.get("_photographer", "")
            caption = (f"{json_caption.rstrip('.')} (Photo: {ph} / Unsplash)"
                       if json_caption and ph else (f"Photo: {ph} / Unsplash" if ph
                       else json_caption or "Photo via Unsplash"))
        elif src == "wikimedia":
            caption = (f"{json_caption.rstrip('.')} ({res['caption']})"
                       if json_caption else res["caption"])
        else:
            caption = json_caption or res.get("caption", "Photo via Unsplash")

        sb.table("lessons").update({
            "hero_image_url": res["url"],
            "hero_image_alt": f"{lesson['title']} — Geography",
            "hero_image_caption": caption,
            "hero_image_position": "center center",
        }).eq("id", lesson["id"]).execute()
        print(f"  [OK] source={src}  {caption[:70]}")

        if src in ("unsplash", "wikimedia"):
            try:
                add_to_index(lesson["title"], caption, SUBJECT_SLUG, subject_name,
                             unit_slug, units[unit_slug].get("name", unit_slug),
                             f"{unit_slug}-l{ln:02d}", res["url"])
            except Exception as e:
                print(f"      [WARN] index add failed: {e}")
            stats["downloaded"] += 1
            if src == "wikimedia":
                stats["wikimedia"].append(key)
        else:
            stats["reused"] += 1
        time.sleep(0.5)

    print("\n" + "=" * 50)
    print(f"reused={stats['reused']} downloaded={stats['downloaded']} failed={stats['failed']}")
    if stats["wikimedia"]:
        print(f"wikimedia fallbacks (eyeball these): {stats['wikimedia']}")


if __name__ == "__main__":
    main()
