"""Compress images on Cloudflare R2 to reduce page load times.

Queries Supabase for all hero_image_url and diagram_url values,
downloads each from R2, compresses with Pillow, and re-uploads.

Hero images → max 1200px wide, JPEG quality 82
Diagrams → max 1000px wide, JPEG quality 82
Skips images already under 150KB.
"""

import io
import os
import sys
from urllib.parse import urlparse

import requests
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, IMAGES_BUCKET, IMAGES_PUBLIC_URL

MIN_SIZE_KB = 150
QUALITY = 82


def get_r2_key(url):
    """Extract R2 object key from public URL."""
    parsed = urlparse(url)
    return parsed.path.lstrip("/")


def compress_image(data, is_diagram):
    """Compress image bytes. Returns compressed bytes or None if no saving."""
    max_width = 1000 if is_diagram else 1200

    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=QUALITY, optimize=True)
    return buf.getvalue()


def main():
    sb = get_client()
    r2 = get_r2_client()

    # Fetch all image URLs from lessons
    print("Fetching image URLs from Supabase...")
    result = sb.table("lessons").select("hero_image_url, diagrams").execute()
    lessons = result.data

    # Build list of (url, is_diagram) pairs
    images = []
    for lesson in lessons:
        if lesson.get("hero_image_url"):
            images.append((lesson["hero_image_url"], False))
        if lesson.get("diagrams"):
            for diag in lesson["diagrams"]:
                if diag.get("url"):
                    images.append((diag["url"], True))

    # Filter to only R2-hosted images
    images = [(url, is_diag) for url, is_diag in images if url.startswith(IMAGES_PUBLIC_URL)]
    print(f"Found {len(images)} images on R2\n")

    total_old = 0
    total_new = 0
    compressed_count = 0
    skipped_count = 0
    error_count = 0

    for url, is_diagram in images:
        r2_key = get_r2_key(url)
        label = "diagram" if is_diagram else "hero"

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            print(f"  ERROR downloading {r2_key}: {e}")
            error_count += 1
            continue

        old_size = len(resp.content)
        total_old += old_size

        if old_size < MIN_SIZE_KB * 1024:
            total_new += old_size
            skipped_count += 1
            continue

        try:
            compressed = compress_image(resp.content, is_diagram)
        except Exception as e:
            print(f"  ERROR compressing {r2_key}: {e}")
            total_new += old_size
            error_count += 1
            continue

        new_size = len(compressed)
        saved = old_size - new_size

        if saved < 1024:
            # Not worth re-uploading
            total_new += old_size
            skipped_count += 1
            continue

        # Upload compressed version
        r2.put_object(
            Bucket=IMAGES_BUCKET,
            Key=r2_key,
            Body=compressed,
            ContentType="image/jpeg",
        )

        total_new += new_size
        compressed_count += 1
        pct = (saved / old_size) * 100
        print(f"  {old_size // 1024:>6} KB -> {new_size // 1024:>6} KB  ({pct:4.0f}% saved)  [{label}] {r2_key}")

    print(f"\n{'=' * 60}")
    print(f"Images compressed: {compressed_count}")
    print(f"Images skipped (small or no saving): {skipped_count}")
    if error_count:
        print(f"Errors: {error_count}")
    print(f"Total before: {total_old // (1024 * 1024)} MB")
    print(f"Total after:  {total_new // (1024 * 1024)} MB")
    if total_old > 0:
        print(f"Saved:        {(total_old - total_new) // (1024 * 1024)} MB ({((total_old - total_new) / total_old) * 100:.0f}%)")


if __name__ == "__main__":
    main()
