# -*- coding: utf-8 -*-
"""Phase 4 hero images for Edexcel Psychology (psychology-edexcel) free-tier.
38 lessons across 11 units. Lesson JSONs live in the API-build run dir
(driver.py output): {unit_slug}-L{NN}.json with hero_keywords + caption.

Per lesson: hero index reuse (psychology-aqa images score well here) ->
Unsplash -> Wikimedia fallback.
"""
import io
import json
import os
import re
import sys
import tempfile
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
from lib.wikimedia import search_wikimedia, download_image, resize_and_compress, MIN_FILE_SIZE
from lib.hero_index import search_heroes, add_to_index
from lib.r2 import get_r2_client, IMAGES_BUCKET

SUBJECT_SLUG = "psychology-edexcel"
SUBJECT_NAME = "Psychology (Edexcel)"
CONTENT_DIR = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad\_psych_build\run_edexcel\lessons")
R2_PUBLIC = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"
HERO_REUSE_MIN_SCORE = 4

LESSON_FILE_PATTERN = re.compile(r"^(?P<unit>[a-z0-9-]+)-L(?P<n>\d{2})\.json$")


def discover_lessons():
    pairs = []
    for name in sorted(os.listdir(CONTENT_DIR)):
        m = LESSON_FILE_PATTERN.match(name)
        if m:
            pairs.append((m.group("unit"), int(m.group("n")), name))
    return pairs


def load_json(filename):
    with open(os.path.join(CONTENT_DIR, filename), encoding="utf-8") as f:
        return json.load(f)


def download_and_upload(url, r2_key, r2_client, source_hint=""):
    tmp_src_path = None
    tmp_dest_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_src:
            tmp_src_path = tmp_src.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_dest:
            tmp_dest_path = tmp_dest.name

        req = urllib.request.Request(url, headers={"User-Agent": "StudyVault/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(tmp_src_path, "wb") as f:
                f.write(resp.read())

        file_size = os.path.getsize(tmp_src_path)
        if file_size < MIN_FILE_SIZE:
            print(f"      [SKIP] too small ({file_size} bytes) from {source_hint}")
            return None, 0

        resize_and_compress(tmp_src_path, tmp_dest_path, max_width=1200, quality=82)
        final_size = os.path.getsize(tmp_dest_path)

        with open(tmp_dest_path, "rb") as f:
            r2_client.put_object(
                Bucket=IMAGES_BUCKET,
                Key=r2_key,
                Body=f.read(),
                ContentType="image/jpeg",
            )

        r2_url = f"{R2_PUBLIC}/{r2_key}"
        print(f"      uploaded: {r2_key} ({final_size // 1024}KB)")
        return r2_url, final_size

    except Exception as e:
        print(f"      [ERROR] download/upload failed for {url[:80]}: {e}")
        return None, 0
    finally:
        for p in (tmp_src_path, tmp_dest_path):
            if p:
                try:
                    os.unlink(p)
                except OSError:
                    pass


def find_hero(keywords, unit_slug, lesson_number, r2_client):
    query_str = " ".join(keywords)
    matches = search_heroes(query_str, min_score=HERO_REUSE_MIN_SCORE,
                            exclude_subjects=[SUBJECT_SLUG])
    if matches:
        top = matches[0]
        print(f"      [REUSE] score={top['score']} {top['hero_url'][:70]}")
        return {
            "url": top["hero_url"],
            "alt": top.get("title", query_str),
            "caption": top.get("description") or "",
            "source": "reused",
        }

    r2_key = f"{SUBJECT_SLUG}/{unit_slug}/lesson-{lesson_number:02d}.jpg"

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
        img_url = top["url"]
        photographer = top.get("photographer", "Unknown")
        alt_text = top.get("title") or query

        r2_url, fsize = download_and_upload(img_url, r2_key, r2_client, source_hint="unsplash")
        if r2_url:
            try:
                trigger_unsplash_download(top.get("_download_location", ""))
            except Exception:
                pass
            return {
                "url": r2_url,
                "alt": alt_text,
                "caption": f"Photo: {photographer} / Unsplash",
                "source": "unsplash",
                "_photographer": photographer,
                "_query": query,
            }
        time.sleep(1)

    for query in keywords:
        print(f"      Wikimedia: '{query}'")
        try:
            results = search_wikimedia(query, limit=20)
        except Exception as e:
            print(f"      Wikimedia error: {e}")
            continue
        if not results:
            time.sleep(4)
            continue
        for candidate in results:
            if candidate.get("size", 0) < MIN_FILE_SIZE and candidate.get("size", 0) != 0:
                continue
            img_url = candidate.get("url") or candidate.get("original_url", "")
            if not img_url:
                continue
            alt_text = candidate.get("title", query).replace("File:", "").strip()
            caption = f"Wikimedia Commons — {alt_text[:80]}"

            r2_url, fsize = download_and_upload(img_url, r2_key, r2_client, source_hint="wikimedia")
            if r2_url:
                return {
                    "url": r2_url,
                    "alt": alt_text,
                    "caption": caption,
                    "source": "wikimedia",
                    "_query": query,
                }
            time.sleep(2)
        time.sleep(4)

    return None


def main():
    sb = get_client()
    r2 = get_r2_client()

    subj = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).execute()
    subject_id = subj.data[0]["id"]
    units_resp = sb.table("units").select("id,slug,name").eq("subject_id", subject_id).execute()
    unit_map = {u["slug"]: u for u in units_resp.data}
    print(f"Units in Supabase: {sorted(unit_map.keys())}")

    pairs = discover_lessons()
    print(f"Lesson files discovered: {len(pairs)}")

    stats = {"reused": 0, "unsplash": 0, "wikimedia": 0, "failed": 0}

    for unit_slug, lesson_number, filename in pairs:
        print(f"\n--- {unit_slug} / L{lesson_number:02d} ---")
        data = load_json(filename)
        keywords = data.get("hero_keywords") or []
        json_caption = data.get("hero_image_caption", "")
        print(f"  Keywords: {keywords}")

        if unit_slug not in unit_map:
            print(f"  [ERR] Unit '{unit_slug}' not in Supabase")
            stats["failed"] += 1
            continue

        unit_id = unit_map[unit_slug]["id"]
        lesson_resp = (
            sb.table("lessons")
            .select("id,title,lesson_number,hero_image_url")
            .eq("unit_id", unit_id)
            .eq("lesson_number", lesson_number)
            .execute()
        )
        if not lesson_resp.data:
            print(f"  [ERR] Lesson L{lesson_number} not found in {unit_slug}")
            stats["failed"] += 1
            continue

        lesson = lesson_resp.data[0]
        if lesson.get("hero_image_url"):
            print("  [SKIP] hero already set")
            continue
        lesson_id = lesson["id"]
        lesson_title = lesson.get("title", "")

        result = find_hero(keywords, unit_slug, lesson_number, r2)
        if not result:
            print(f"  [FAIL] No image found")
            stats["failed"] += 1
            continue

        source = result["source"]
        if source == "reused":
            final_caption = json_caption or result["caption"]
        elif source == "unsplash":
            photographer = result.get("_photographer", "")
            if json_caption and photographer:
                final_caption = f"{json_caption.rstrip('.')} (Photo: {photographer} / Unsplash)"
            elif photographer:
                final_caption = f"Photo: {photographer} / Unsplash"
            else:
                final_caption = json_caption or "Photo via Unsplash"
        else:
            wiki_attr = result["caption"]
            final_caption = f"{json_caption.rstrip('.')} ({wiki_attr})" if json_caption else wiki_attr

        unit_display = unit_slug.replace("-", " ").title()
        alt_text = f"{lesson_title} — {unit_display} for Edexcel GCSE Psychology"

        sb.table("lessons").update({
            "hero_image_url": result["url"],
            "hero_image_alt": alt_text,
            "hero_image_caption": final_caption,
            "hero_image_position": "center center",
        }).eq("id", lesson_id).execute()

        print(f"  [OK] source={source}  caption={final_caption[:90]}")
        stats[source] += 1

        if source in ("unsplash", "wikimedia"):
            try:
                add_to_index(
                    title=lesson_title,
                    description=json_caption or "",
                    subject_slug=SUBJECT_SLUG,
                    unit_slug=unit_slug,
                    lesson_number=lesson_number,
                    hero_url=result["url"],
                    keywords=keywords,
                )
            except Exception as e:
                print(f"      index add failed: {e}")

    print(f"\nDone: {stats}")
    # unit card images from L1 heroes (browse grid needs image_url on every unit)
    for u_slug, u in unit_map.items():
        l1 = (sb.table("lessons").select("hero_image_url")
              .eq("unit_id", u["id"]).eq("lesson_number", 1).execute())
        if l1.data and l1.data[0].get("hero_image_url"):
            sb.table("units").update({"image_url": l1.data[0]["hero_image_url"]}) \
                .eq("id", u["id"]).execute()
            print(f"unit image set: {u_slug}")


if __name__ == "__main__":
    main()
