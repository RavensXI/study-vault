"""Compress all project images to reduce page load times.

Hero images → max 1200px wide, JPEG quality 82
Diagrams → max 1000px wide, JPEG quality 82
Other images → max 1200px wide, JPEG quality 82

Skips images already under 150KB.
Overwrites originals in-place.
"""

import os
import sys
from pathlib import Path
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

SKIP_DIRS = {'.git', '.claude', 'node_modules', 'scripts'}
MIN_SIZE_KB = 150  # Don't bother with files already under this
QUALITY = 82

def get_max_width(filepath: str) -> int:
    """Determine max width based on image type."""
    name = os.path.basename(filepath).lower()
    if 'diagram' in name:
        return 1000
    return 1200  # hero images, subject images, etc.

def compress_image(filepath: str) -> tuple[int, int]:
    """Compress a single image. Returns (old_size, new_size) in bytes."""
    old_size = os.path.getsize(filepath)

    if old_size < MIN_SIZE_KB * 1024:
        return old_size, old_size  # Skip small files

    max_width = get_max_width(filepath)

    try:
        with Image.open(filepath) as img:
            # Convert RGBA to RGB if needed (for JPEG)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Resize if wider than max
            w, h = img.size
            if w > max_width:
                ratio = max_width / w
                new_h = int(h * ratio)
                img = img.resize((max_width, new_h), Image.LANCZOS)

            # Save with compression
            img.save(filepath, 'JPEG', quality=QUALITY, optimize=True)

        new_size = os.path.getsize(filepath)
        return old_size, new_size
    except Exception as e:
        print(f"  ERROR: {filepath}: {e}")
        return old_size, old_size

def main():
    total_old = 0
    total_new = 0
    compressed_count = 0
    skipped_count = 0

    # Collect all image files
    images = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append(os.path.join(root, f))

    images.sort(key=lambda p: os.path.getsize(p), reverse=True)

    print(f"Found {len(images)} images to process\n")

    for filepath in images:
        old_size, new_size = compress_image(filepath)
        total_old += old_size
        total_new += new_size

        if old_size == new_size and old_size < MIN_SIZE_KB * 1024:
            skipped_count += 1
            continue

        saved = old_size - new_size
        rel = os.path.relpath(filepath, PROJECT_ROOT)

        if saved > 1024:  # Only report if we saved more than 1KB
            pct = (saved / old_size) * 100
            compressed_count += 1
            print(f"  {old_size//1024:>6} KB -> {new_size//1024:>6} KB  ({pct:4.0f}% saved)  {rel}")

    print(f"\n{'='*60}")
    print(f"Images processed: {compressed_count}")
    print(f"Images skipped (under {MIN_SIZE_KB}KB): {skipped_count}")
    print(f"Total before: {total_old // (1024*1024)} MB")
    print(f"Total after:  {total_new // (1024*1024)} MB")
    print(f"Saved:        {(total_old - total_new) // (1024*1024)} MB ({((total_old - total_new) / total_old) * 100:.0f}%)")

if __name__ == '__main__':
    main()
