"""
Phase 4 hero images for OCR Information Technology (it-ocr).
14 lessons across 3 units:
  - it-in-the-digital-world  (L1-L8)
  - augmented-reality-design (L1-L3)
  - data-manipulation-with-spreadsheets (L1-L3)

Workflow per lesson:
  1. Load hero_keywords from scripts/_content_it-ocr/{unit_slug}/L{N}.json
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

SUBJECT_ID = "ccb8b884-4c48-41cc-a356-fe95e60b396d"
SUBJECT_SLUG = "it-ocr"
CONTENT_DIR = os.path.join(SCRIPT_DIR, "_content_it-ocr")
R2_PUBLIC = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"
HERO_REUSE_MIN_SCORE = 4


# ── Lesson manifest in display order ────────────────────────────────────────
LESSONS = [
    # (unit_slug, lesson_number)
    ("it-in-the-digital-world", 1),
    ("it-in-the-digital-world", 2),
    ("it-in-the-digital-world", 3),
    ("it-in-the-digital-world", 4),
    ("it-in-the-digital-world", 5),
    ("it-in-the-digital-world", 6),
    ("it-in-the-digital-world", 7),
    ("it-in-the-digital-world", 8),
    ("augmented-reality-design", 1),
    ("augmented-reality-design", 2),
    ("augmented-reality-design", 3),
    ("data-manipulation-with-spreadsheets", 1),
    ("data-manipulation-with-spreadsheets", 2),
    ("data-manipulation-with-spreadsheets", 3),
]


def load_json(unit_slug, lesson_number):
    path = os.path.join(CONTENT_DIR, unit_slug, f"L{lesson_number}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def download_and_upload(url, r2_key, r2_client, source_hint=""):
    """Download url, compress, upload to R2. Returns (r2_url, file_size)."""
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
    """
    Returns dict with keys: url, alt, caption, source
    source is one of: 'reused', 'unsplash', 'wikimedia'
    Returns None if nothing found.
    """
    # 1. Hero index check
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

    # 2. Unsplash
    r2_key = f"it-ocr/{unit_slug}/lesson-{lesson_number:02d}.jpg"
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
        caption = f"Photo: {photographer} / Unsplash"

        r2_url, fsize = download_and_upload(img_url, r2_key, r2_client, source_hint="unsplash")
        if r2_url:
            # Trigger Unsplash download tracking
            try:
                trigger_unsplash_download(top.get("_download_location", ""))
            except Exception:
                pass
            return {
                "url": r2_url,
                "alt": alt_text,
                "caption": caption,
                "source": "unsplash",
                "_photographer": photographer,
                "_query": query,
            }
        time.sleep(1)

    # 3. Wikimedia fallback
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

    # Build unit slug -> unit_id map
    units_resp = sb.table("units").select("id,slug,name").eq("subject_id", SUBJECT_ID).execute()
    unit_map = {u["slug"]: u for u in units_resp.data}
    print(f"Units found: {[u['slug'] for u in units_resp.data]}")

    stats = {"reused": 0, "downloaded": 0, "failed": 0, "wikimedia_fallbacks": []}

    for unit_slug, lesson_number in LESSONS:
        print(f"\n--- {unit_slug} / L{lesson_number:02d} ---")

        # Load JSON
        try:
            data = load_json(unit_slug, lesson_number)
        except FileNotFoundError:
            print(f"  [MISS] No JSON at {unit_slug}/L{lesson_number}.json")
            stats["failed"] += 1
            continue

        keywords = data.get("hero_keywords") or []
        json_caption = data.get("hero_image_caption", "")

        # Get lesson from Supabase
        if unit_slug not in unit_map:
            print(f"  [ERR] Unit {unit_slug} not found in Supabase")
            stats["failed"] += 1
            continue

        unit_id = unit_map[unit_slug]["id"]
        lesson_resp = sb.table("lessons").select("id,title,hero_image_url").eq("unit_id", unit_id).eq("lesson_number", lesson_number).execute()

        if not lesson_resp.data:
            print(f"  [ERR] Lesson L{lesson_number} not found in unit {unit_slug}")
            stats["failed"] += 1
            continue

        lesson = lesson_resp.data[0]
        lesson_id = lesson["id"]
        lesson_title = lesson.get("title", "")

        print(f"  Title: {lesson_title}")
        print(f"  Keywords: {keywords}")

        result = find_hero(keywords, unit_slug, lesson_number, r2)

        if not result:
            print(f"  [FAIL] No image found for L{lesson_number} {lesson_title}")
            stats["failed"] += 1
            continue

        # Use JSON caption if content author wrote a good one, else use download caption
        # For fresh downloads, the JSON caption is more specific/editorial than "Photo: X / Unsplash"
        # Use JSON caption as-is, but append attribution in parentheses
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
        else:  # wikimedia
            wiki_attr = result["caption"]
            if json_caption:
                final_caption = f"{json_caption.rstrip('.')} ({wiki_attr})"
            else:
                final_caption = wiki_attr

        # Build alt text: use lesson title as base for clarity
        alt_text = f"{lesson_title} — {unit_slug.replace('-', ' ')} lesson for OCR Information Technology"

        # Update Supabase
        sb.table("lessons").update({
            "hero_image_url": result["url"],
            "hero_image_alt": alt_text,
            "hero_image_caption": final_caption,
            "hero_image_position": "center center",
        }).eq("id", lesson_id).execute()

        print(f"  [OK] source={source}  caption={final_caption[:80]}")

        # Add to hero index for fresh downloads
        if source in ("unsplash", "wikimedia"):
            try:
                add_to_index(
                    title=lesson_title,
                    description=f"Photo: {result.get('_photographer', '')} / Unsplash" if source == "unsplash" else result["caption"],
                    subject_slug=SUBJECT_SLUG,
                    subject_name="Information Technology (OCR)",
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

        # Brief pause to be rate-limit friendly
        time.sleep(0.5)

    # ── Summary ──────────────────────────────────────────────────────────────
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
