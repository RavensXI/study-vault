"""Mirror Unsplash homepage-card images to R2 + return the R2 URLs.

Bare Unsplash URLs can go dead (Geology entry in freeSubjectMeta did, May 2026).
Mirror them to studyvault-images bucket at homepage-cards/{slug}.jpg so the
homepage doesn't break when Unsplash deletes/expires.

Usage: edit IMAGES dict below, run once, copy URLs back into index.html.
"""
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.r2 import get_r2_client, IMAGES_BUCKET
from lib.wikimedia import resize_and_compress, MIN_FILE_SIZE
from lib.unsplash import trigger_unsplash_download

R2_PUBLIC = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"

# (slug, unsplash photo id, download_location for tracking ping)
IMAGES = [
    {
        "slug": "electronics-eduqas",
        "src_url": "https://images.unsplash.com/photo-1524234107056-1c1f48f64ab8?w=1200&q=82&fit=max&fm=jpg",
        "photographer": "Tim Käbel",
    },
    {
        "slug": "geology-eduqas",
        "src_url": "https://images.unsplash.com/photo-1748521694073-31f26e704b75?w=1200&q=82&fit=max&fm=jpg",
        "photographer": "Theo",
    },
    {
        "slug": "engineering-aqa",
        "src_url": "https://images.unsplash.com/photo-1666634157070-6fd830fb5672?w=1200&q=82&fit=max&fm=jpg",
        "photographer": "Unsplash",
    },
    {
        "slug": "astronomy-edexcel",
        "src_url": "https://images.unsplash.com/photo-1515705576963-95cad62945b6?w=1200&q=82&fit=max&fm=jpg",
        "photographer": "Unsplash",
    },
]


def main():
    r2 = get_r2_client()
    for spec in IMAGES:
        slug = spec["slug"]
        src_url = spec["src_url"]
        r2_key = f"homepage-cards/{slug}.jpg"
        print(f"=== {slug} ===")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as src_tmp:
            src_path = src_tmp.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as dest_tmp:
            dest_path = dest_tmp.name
        try:
            req = urllib.request.Request(src_url, headers={"User-Agent": "StudyVault/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            with open(src_path, "wb") as f:
                f.write(data)
            size_in = os.path.getsize(src_path)
            print(f"  downloaded: {size_in // 1024} KB from Unsplash")
            if size_in < MIN_FILE_SIZE:
                print(f"  SKIP: too small ({size_in} bytes)")
                continue
            resize_and_compress(src_path, dest_path, max_width=1200, quality=82)
            size_out = os.path.getsize(dest_path)
            with open(dest_path, "rb") as f:
                r2.put_object(
                    Bucket=IMAGES_BUCKET,
                    Key=r2_key,
                    Body=f.read(),
                    ContentType="image/jpeg",
                )
            r2_url = f"{R2_PUBLIC}/{r2_key}"
            print(f"  uploaded: {r2_key} ({size_out // 1024} KB)")
            print(f"  R2 URL: {r2_url}")
            print(f"  Photographer credit: {spec['photographer']} / Unsplash")
        except Exception as e:
            print(f"  ERROR: {e}")
        finally:
            for p in (src_path, dest_path):
                try:
                    os.unlink(p)
                except OSError:
                    pass


if __name__ == "__main__":
    main()
