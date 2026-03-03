"""Wikimedia Commons image search, download, and compression.

Extracted from download_drama_heroes.py — search API, download, resize/compress.
"""

import os
import time

import requests
from PIL import Image


# ── Config ──────────────────────────────────────────────────────────────

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "StudyVault/1.0 (educational; contact: t.shaun@unity.lancs.sch.uk)"
HEADERS = {"User-Agent": USER_AGENT}

MIN_FILE_SIZE = 50 * 1024  # 50 KB minimum
MAX_WIDTH = 1200
JPEG_QUALITY = 82
API_DELAY = 4  # seconds between Wikimedia requests


# ── Search ──────────────────────────────────────────────────────────────

def search_wikimedia(query, limit=20):
    """Search Wikimedia Commons for landscape JPEG images matching a query.

    Returns list of dicts with keys: title, url, original_url, width, height, size, mime.
    Sorted by width descending (prefer larger/higher quality).
    """
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

        # Skip SVGs/diagrams that got through
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

    results.sort(key=lambda x: x["width"], reverse=True)
    return results


# ── Download ────────────────────────────────────────────────────────────

def download_image(url, dest_path):
    """Download an image from URL to dest_path. Returns file size in bytes."""
    resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
    resp.raise_for_status()

    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    return os.path.getsize(dest_path)


# ── Resize / Compress ──────────────────────────────────────────────────

def resize_and_compress(src_path, dest_path, max_width=MAX_WIDTH, quality=JPEG_QUALITY):
    """Resize image to max_width and save as compressed JPEG. Returns file size."""
    img = Image.open(src_path)
    img = img.convert("RGB")

    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        new_h = int(h * ratio)
        img = img.resize((max_width, new_h), Image.LANCZOS)

    img.save(dest_path, "JPEG", quality=quality, optimize=True)
    return os.path.getsize(dest_path)
