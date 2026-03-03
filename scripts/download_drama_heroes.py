"""
Download hero images from Wikimedia Commons for Drama GCSE lessons,
upload to Cloudflare R2, and update Supabase lesson records.

Usage:
    python scripts/download_drama_heroes.py              # Full run
    python scripts/download_drama_heroes.py --dry-run    # Preview only

Env vars required:
    R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID
    SUPABASE_URL, SUPABASE_SERVICE_KEY
"""

import io
import os
import sys
import time
import json
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import boto3
import requests
from botocore.config import Config
from supabase import create_client
from PIL import Image

# ─── Config ──────────────────────────────────────────────────────────────────

BUCKET_NAME = "studyvault-images"
R2_PUBLIC_URL = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "StudyVault/1.0 (educational; contact: t.shaun@unity.lancs.sch.uk)"
HEADERS = {"User-Agent": USER_AGENT}

MIN_FILE_SIZE = 50 * 1024  # 50 KB minimum
MAX_WIDTH = 1200  # Resize to this max width
JPEG_QUALITY = 82
API_DELAY = 4  # seconds between Wikimedia requests

# ─── Lesson definitions ─────────────────────────────────────────────────────

LESSONS = [
    # Blood Brothers
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 1,
        "search": "musical theatre performance stage",
        "alt": "Blood Brothers musical theatre production",
        "fallback_searches": ["theatre musical production stage", "West End musical theatre", "Broadway musical stage"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 2,
        "search": "actors performing theatre stage",
        "alt": "Theatre actors performing on stage",
        "fallback_searches": ["theatre performance actors", "drama performance stage", "stage play actors performing"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 3,
        "search": "Liverpool terraced houses street",
        "alt": "Liverpool in the 1980s, working-class community",
        "fallback_searches": ["Liverpool street urban", "terraced houses England", "working class housing England"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 4,
        "search": "theatrical costume design stage",
        "alt": "Theatrical costume design for a stage production",
        "fallback_searches": ["theatre costume wardrobe backstage", "stage costume fitting theatre production"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 5,
        "search": "proscenium arch theatre stage set",
        "alt": "Proscenium arch theatre with stage set",
        "fallback_searches": ["proscenium theatre interior", "theatre auditorium stage", "opera house interior stage"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 6,
        "search": "theatre stage lighting colorful",
        "alt": "Colourful stage lighting in a theatre",
        "fallback_searches": ["stage lighting theatre spotlights", "theatre lighting design colored", "concert stage lights dramatic"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 7,
        "search": "actor performing stage drama",
        "alt": "Actor performing in a dramatic stage production",
        "fallback_searches": ["dramatic performance stage actor spotlight", "theatre actor monologue stage", "stage performance drama actor"],
    },
    {
        "unit_slug": "blood-brothers",
        "lesson_number": 8,
        "search": "theatre director rehearsal stage",
        "alt": "Theatre director leading a rehearsal on stage",
        "fallback_searches": ["theatre rehearsal director actors", "stage rehearsal directing drama", "director theatre production rehearsal"],
    },
    # Rise Up
    {
        "unit_slug": "rise-up",
        "lesson_number": 1,
        "search": "Freedom Riders 1960s civil rights bus",
        "alt": "Freedom Riders during the 1960s civil rights movement",
        "fallback_searches": ["Freedom Riders bus 1961", "civil rights movement bus", "civil rights march 1960s"],
    },
    {
        "unit_slug": "rise-up",
        "lesson_number": 2,
        "search": "1960s segregation protest America",
        "alt": "Civil rights protest against segregation in 1960s America",
        "fallback_searches": ["segregation protest 1960s United States", "civil rights march 1960s America", "1960s American civil rights demonstration"],
    },
    {
        "unit_slug": "rise-up",
        "lesson_number": 3,
        "search": "civil rights movement sit-in 1960s",
        "alt": "Civil rights sit-in protest in the 1960s",
        "fallback_searches": ["lunch counter sit-in 1960s civil rights", "sit-in protest 1960s segregation", "Nashville sit-ins 1960s civil rights"],
    },
    {
        "unit_slug": "rise-up",
        "lesson_number": 4,
        "search": "small theatre stage performance",
        "alt": "Small theatre stage during a performance",
        "fallback_searches": ["fringe theatre stage performance", "black box theatre performance", "studio theatre stage drama"],
    },
]


# ─── Wikimedia search ────────────────────────────────────────────────────────

def search_wikimedia(query, limit=20):
    """Search Wikimedia Commons for images matching a query. Returns list of file titles."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",  # File namespace
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": "1200",
    }

    # Retry up to 3 times on timeout
    for attempt in range(3):
        try:
            resp = requests.get(WIKIMEDIA_API, params=params, headers=HEADERS, timeout=60)
            resp.raise_for_status()
            break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt < 2:
                print(f"    Timeout (attempt {attempt + 1}/3), retrying in 5s...")
                time.sleep(5)
            else:
                print(f"    Failed after 3 attempts: {e}")
                return []

    data = resp.json()

    pages = data.get("query", {}).get("pages", {})
    results = []
    for page_id, page in pages.items():
        ii = page.get("imageinfo", [{}])[0]
        width = ii.get("width", 0)
        height = ii.get("height", 0)

        # Skip non-landscape or too-small images
        if width < 800 or height < 400:
            continue
        if height > width:
            continue  # portrait

        # Check MIME is photo (JPEG)
        mime = ii.get("mime", "")
        if "jpeg" not in mime and "jpg" not in mime:
            continue

        # Prefer actual photographs — skip SVGs/diagrams that got through
        title = page.get("title", "")
        if any(skip in title.lower() for skip in ["icon", "logo", "flag", "map", "diagram", "chart"]):
            continue

        url = ii.get("thumburl") or ii.get("url", "")
        original_url = ii.get("url", "")
        size = ii.get("size", 0)

        results.append({
            "title": title,
            "url": url,
            "original_url": original_url,
            "width": width,
            "height": height,
            "size": size,
            "mime": mime,
        })

    # Sort by size (prefer larger/higher quality)
    results.sort(key=lambda x: x["width"], reverse=True)
    return results


def download_image(url, dest_path):
    """Download an image from URL to dest_path. Returns file size in bytes."""
    resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
    resp.raise_for_status()

    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    return os.path.getsize(dest_path)


def resize_and_compress(src_path, dest_path, max_width=MAX_WIDTH, quality=JPEG_QUALITY):
    """Resize image to max_width and save as compressed JPEG."""
    img = Image.open(src_path)
    img = img.convert("RGB")  # Ensure RGB for JPEG

    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        new_h = int(h * ratio)
        img = img.resize((max_width, new_h), Image.LANCZOS)

    img.save(dest_path, "JPEG", quality=quality, optimize=True)
    return os.path.getsize(dest_path)


# ─── R2 upload ───────────────────────────────────────────────────────────────

def get_r2_client():
    """Create an S3-compatible client for Cloudflare R2."""
    account_id = os.environ.get("R2_ACCOUNT_ID")
    access_key = os.environ.get("R2_ACCESS_KEY_ID")
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")

    if not all([account_id, access_key, secret_key]):
        print("ERROR: Missing R2 environment variables.")
        sys.exit(1)

    return boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(
            region_name="auto",
            retries={"max_attempts": 3, "mode": "adaptive"},
        ),
    )


def upload_to_r2(client, local_path, r2_key):
    """Upload a file to R2 and return the public URL."""
    client.upload_file(
        local_path,
        BUCKET_NAME,
        r2_key,
        ExtraArgs={"ContentType": "image/jpeg"},
    )
    return f"{R2_PUBLIC_URL}/{r2_key}"


# ─── Supabase ────────────────────────────────────────────────────────────────

def get_supabase():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
        sys.exit(1)
    return create_client(url, key)


def get_lesson_id(sb, unit_slug, lesson_number):
    """Look up a lesson ID by unit slug and lesson number."""
    units = sb.table("units").select("id").eq("slug", unit_slug).execute()
    if not units.data:
        print(f"  ERROR: Unit '{unit_slug}' not found in Supabase")
        return None

    unit_id = units.data[0]["id"]
    lesson = (
        sb.table("lessons")
        .select("id")
        .eq("unit_id", unit_id)
        .eq("lesson_number", lesson_number)
        .single()
        .execute()
    )
    if not lesson.data:
        print(f"  ERROR: Lesson {lesson_number} not found in unit '{unit_slug}'")
        return None

    return lesson.data["id"]


def update_lesson_hero(sb, lesson_id, r2_url, alt_text):
    """Update a lesson's hero image URL and alt text in Supabase."""
    sb.table("lessons").update({
        "hero_image_url": r2_url,
        "hero_image_alt": alt_text,
    }).eq("id", lesson_id).execute()


# ─── Main ────────────────────────────────────────────────────────────────────

def process_lesson(lesson_def, r2_client, sb, dry_run=False):
    """Process a single lesson: search, download, resize, upload, update DB."""
    unit = lesson_def["unit_slug"]
    num = lesson_def["lesson_number"]
    label = f"drama/{unit}/lesson-{num:02d}"
    print(f"\n{'='*60}")
    print(f"  {label}: {lesson_def['alt']}")
    print(f"{'='*60}")

    # Look up lesson ID
    lesson_id = get_lesson_id(sb, unit, num)
    if not lesson_id:
        return False

    # Search Wikimedia
    all_searches = [lesson_def["search"]] + lesson_def.get("fallback_searches", [])
    chosen = None

    for i, query in enumerate(all_searches):
        if i > 0:
            print(f"  Trying fallback search: {query}")
            time.sleep(API_DELAY)
        else:
            print(f"  Searching: {query}")

        results = search_wikimedia(query)
        print(f"  Found {len(results)} landscape JPEG candidates")

        for r in results:
            print(f"    - {r['title'][:60]}  ({r['width']}x{r['height']}, {r['size']/1024:.0f}KB)")

        # Pick the best candidate (first landscape result with decent size)
        for r in results:
            if r["size"] >= MIN_FILE_SIZE:
                chosen = r
                break

        if chosen:
            break

    if not chosen:
        print(f"  WARNING: No suitable image found for {label}")
        return False

    print(f"  Selected: {chosen['title'][:70]}")

    if dry_run:
        print(f"  [DRY RUN] Would download, resize, upload to drama/{unit}/lesson-{num:02d}-hero.jpg")
        return True

    # Download to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_path = os.path.join(tmpdir, "raw.jpg")
        final_path = os.path.join(tmpdir, f"lesson-{num:02d}-hero.jpg")

        # Use thumburl (pre-scaled to 1200px) if available, else original
        dl_url = chosen["url"] if chosen["url"] else chosen["original_url"]
        print(f"  Downloading from: {dl_url[:80]}...")
        raw_size = download_image(dl_url, raw_path)
        print(f"  Downloaded: {raw_size / 1024:.0f} KB")

        if raw_size < MIN_FILE_SIZE:
            # Try original URL if thumb was too small
            print(f"  Too small ({raw_size/1024:.0f}KB), trying original URL...")
            dl_url = chosen["original_url"]
            raw_size = download_image(dl_url, raw_path)
            print(f"  Downloaded original: {raw_size / 1024:.0f} KB")

        if raw_size < MIN_FILE_SIZE:
            print(f"  WARNING: Image still too small ({raw_size/1024:.0f}KB), skipping")
            return False

        # Resize and compress
        final_size = resize_and_compress(raw_path, final_path)
        print(f"  Resized/compressed: {final_size / 1024:.0f} KB")

        if final_size < 10 * 1024:
            print(f"  WARNING: Compressed image too small ({final_size/1024:.0f}KB), skipping")
            return False

        # Upload to R2
        r2_key = f"drama/{unit}/lesson-{num:02d}-hero.jpg"
        print(f"  Uploading to R2: {r2_key}")
        r2_url = upload_to_r2(r2_client, final_path, r2_key)
        print(f"  R2 URL: {r2_url}")

        # Update Supabase
        print(f"  Updating Supabase lesson {lesson_id[:8]}...")
        update_lesson_hero(sb, lesson_id, r2_url, lesson_def["alt"])
        print(f"  Done!")

    return True


def main():
    dry_run = "--dry-run" in sys.argv

    print("Download Drama Hero Images from Wikimedia Commons")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Public URL: {R2_PUBLIC_URL}")
    if dry_run:
        print("MODE: DRY RUN")
    print()

    r2_client = get_r2_client()
    sb = get_supabase()

    success = 0
    failed = 0

    for lesson_def in LESSONS:
        try:
            ok = process_lesson(lesson_def, r2_client, sb, dry_run)
            if ok:
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

        # Rate-limit between lessons
        time.sleep(API_DELAY)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Success: {success}/12")
    print(f"Failed:  {failed}/12")
    print(f"\nDone!")


if __name__ == "__main__":
    main()
