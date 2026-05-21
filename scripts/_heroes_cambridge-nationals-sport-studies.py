"""
Phase 4 hero images for Cambridge Nationals Enterprise & Marketing
(cambridge-nationals-sport-studies).

12 lessons across 1 unit:
  - contemporary-issues-in-sport (L1-L12)

Workflow per lesson:
  1. Load hero_keywords from scripts/_content_cambridge-nationals-sport-studies/lessons/{slug}.json
  2. Check hero index for reuse (min_score=4)
  3. Otherwise: Unsplash -> Wikimedia fallback
  4. Download -> resize_and_compress -> R2 upload
  5. Update Supabase lesson row
  6. add_to_index for fresh downloads
"""
import io
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
from lib.wikimedia import search_wikimedia, download_image, resize_and_compress, MIN_FILE_SIZE
from lib.hero_index import search_heroes, add_to_index
from lib.r2 import get_r2_client, IMAGES_BUCKET

SUBJECT_SLUG = "cambridge-nationals-sport-studies"
CONTENT_DIR = Path(SCRIPT_DIR) / f"_content_{SUBJECT_SLUG}"
LESSONS_DIR = CONTENT_DIR / "lessons"
R2_PUBLIC = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"
HERO_REUSE_MIN_SCORE = 4


def build_lesson_index():
    """Index every lessons/*.json by (_unit_slug, _lesson_number)."""
    idx = {}
    for p in LESSONS_DIR.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        key = (d.get("_unit_slug"), d.get("_lesson_number"))
        idx[key] = d
    return idx


def download_and_upload(url, r2_key, r2_client, source_hint=""):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_src:
        tmp_src_path = tmp_src.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_dest:
        tmp_dest_path = tmp_dest.name
    try:
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
            try:
                os.unlink(p)
            except OSError:
                pass


def find_hero(keywords, unit_slug, lesson_number, r2_client):
    query_str = " ".join(keywords)
    matches = search_heroes(query_str, min_score=HERO_REUSE_MIN_SCORE)
    if matches:
        top = matches[0]
        print(f"      [REUSE] score={top['score']} {top['hero_url'][:70]}")
        return {
            "url": top["hero_url"],
            "alt": top.get("title", query_str),
            "caption": top.get("description") or "Photo via Unsplash",
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
            r2_url, fsize = download_and_upload(img_url, r2_key, r2_client, source_hint="wikimedia")
            if r2_url:
                return {
                    "url": r2_url,
                    "alt": alt_text,
                    "caption": f"Wikimedia Commons — {alt_text[:80]}",
                    "source": "wikimedia",
                    "_query": query,
                }
            time.sleep(2)
        time.sleep(4)

    return None


def main():
    sb = get_client()
    r2 = get_r2_client()

    subj = (
        sb.table("subjects")
        .select("id, slug, name")
        .eq("slug", SUBJECT_SLUG)
        .is_("school_id", "null")
        .execute()
        .data
    )
    if not subj:
        print(f"ERROR: subject '{SUBJECT_SLUG}' not found")
        sys.exit(1)
    subject_id = subj[0]["id"]
    subject_name = subj[0]["name"]

    units_resp = sb.table("units").select("id,slug,name").eq("subject_id", subject_id).execute()
    unit_map = {u["slug"]: u for u in units_resp.data}
    print(f"Units: {list(unit_map.keys())}")

    LESSONS = [("contemporary-issues-in-sport", n) for n in range(1, 11)]
    lesson_idx = build_lesson_index()

    stats = {"reused": 0, "downloaded": 0, "failed": 0, "wikimedia_fallbacks": []}

    for unit_slug, lesson_number in LESSONS:
        print(f"\n--- {unit_slug} / L{lesson_number:02d} ---")
        data = lesson_idx.get((unit_slug, lesson_number))
        if not data:
            print(f"  [MISS] no JSON at ({unit_slug}, L{lesson_number})")
            stats["failed"] += 1
            continue
        keywords = data.get("hero_keywords") or []
        json_caption = data.get("hero_image_caption", "")

        unit_id = unit_map[unit_slug]["id"]
        lesson_resp = (
            sb.table("lessons")
            .select("id,title,hero_image_url")
            .eq("unit_id", unit_id)
            .eq("lesson_number", lesson_number)
            .execute()
        )
        if not lesson_resp.data:
            print(f"  [ERR] no Supabase row for L{lesson_number} in {unit_slug}")
            stats["failed"] += 1
            continue
        lesson = lesson_resp.data[0]
        lesson_id = lesson["id"]
        lesson_title = lesson.get("title", "")
        print(f"  Title: {lesson_title}")
        print(f"  Keywords: {keywords}")

        result = find_hero(keywords, unit_slug, lesson_number, r2)
        if not result:
            print(f"  [FAIL] no image for L{lesson_number} {lesson_title}")
            stats["failed"] += 1
            continue

        source = result["source"]
        if source == "reused":
            final_caption = result["caption"]
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

        alt_text = f"{lesson_title} — Sport Studies"

        sb.table("lessons").update({
            "hero_image_url": result["url"],
            "hero_image_alt": alt_text,
            "hero_image_caption": final_caption,
            "hero_image_position": "center center",
        }).eq("id", lesson_id).execute()
        print(f"  [OK] source={source}  caption={final_caption[:80]}")

        if source in ("unsplash", "wikimedia"):
            try:
                add_to_index(
                    title=lesson_title,
                    description=f"Photo: {result.get('_photographer', '')} / Unsplash" if source == "unsplash" else result["caption"],
                    subject_slug=SUBJECT_SLUG,
                    subject_name=subject_name,
                    unit_slug=unit_slug,
                    unit_name=unit_map[unit_slug].get("name", unit_slug),
                    lesson_slug=f"{unit_slug}-l{lesson_number:02d}",
                    hero_url=result["url"],
                )
            except Exception as e:
                print(f"      [WARN] hero index add failed: {e}")

        if source == "reused":
            stats["reused"] += 1
        else:
            stats["downloaded"] += 1
            if source == "wikimedia":
                stats["wikimedia_fallbacks"].append(f"{unit_slug}/L{lesson_number}")
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total = len(LESSONS)
    print(f"Total lessons:      {total}")
    print(f"Heroes reused:      {stats['reused']}")
    print(f"Heroes downloaded:  {stats['downloaded']}")
    print(f"Failures:           {stats['failed']}")
    if stats["wikimedia_fallbacks"]:
        print(f"Wikimedia fallbacks (check manually): {stats['wikimedia_fallbacks']}")
    else:
        print("Wikimedia fallbacks: none")
    print(f"Total updated:      {stats['reused'] + stats['downloaded']}/{total}")


if __name__ == "__main__":
    main()
