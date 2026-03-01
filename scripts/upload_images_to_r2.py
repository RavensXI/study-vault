"""
Upload all hero images and diagrams to Cloudflare R2, then optionally update
image URLs in the Supabase lessons table.

Usage:
    python scripts/upload_images_to_r2.py                  # Upload images
    python scripts/upload_images_to_r2.py --dry-run        # Show what would upload
    python scripts/upload_images_to_r2.py --update-db      # Upload + rewrite DB URLs

Env vars required:
    R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID
    SUPABASE_URL, SUPABASE_SERVICE_KEY   (only with --update-db)
"""

import io
import mimetypes
import os
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import boto3
from botocore.config import Config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

BUCKET_NAME = "studyvault-images"
R2_PUBLIC_URL = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"

# Image extensions to upload
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}

# Directories containing lesson images
UNIT_DIRS = [
    "history/conflict-tension",
    "history/health-people",
    "history/elizabethan",
    "history/america",
    "business/theme-1",
    "business/theme-2",
    "geography/paper-1",
    "geography/paper-2",
    "sport-science/r180",
]

# Also upload root-level subject images
ROOT_IMAGE_DIRS = [
    "images",
]


def get_r2_client():
    """Create an S3-compatible client for Cloudflare R2."""
    account_id = os.environ.get("R2_ACCOUNT_ID")
    access_key = os.environ.get("R2_ACCESS_KEY_ID")
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")

    if not all([account_id, access_key, secret_key]):
        print("ERROR: Missing R2 environment variables.")
        print("Required: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY")
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


def list_existing_keys(client, prefix=""):
    """List all existing object keys in the bucket."""
    keys = set()
    paginator = client.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
            for obj in page.get("Contents", []):
                keys.add(obj["Key"])
    except client.exceptions.NoSuchBucket:
        print(f"NOTE: Bucket '{BUCKET_NAME}' does not exist yet. Will create on first upload.")
    return keys


def is_lesson_image(filename):
    """Check if a file is a lesson-related image (hero or diagram)."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in IMAGE_EXTS:
        return False
    # Skip narration files, thumbnails, etc.
    if filename.startswith("narration_"):
        return False
    return True


def get_content_type(filename):
    """Get MIME type for a file."""
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"


def upload_directory(client, local_dir, r2_prefix, existing_keys, dry_run=False):
    """Upload all image files from a directory. Returns (uploaded, skipped, bytes)."""
    full_dir = os.path.join(PROJECT_ROOT, local_dir)
    if not os.path.isdir(full_dir):
        return 0, 0, 0

    image_files = sorted(f for f in os.listdir(full_dir) if is_lesson_image(f))
    if not image_files:
        return 0, 0, 0

    uploaded = 0
    skipped = 0
    total_bytes = 0

    for img_name in image_files:
        r2_key = f"{r2_prefix}/{img_name}"
        local_path = os.path.join(full_dir, img_name)
        file_size = os.path.getsize(local_path)

        if r2_key in existing_keys:
            skipped += 1
            continue

        if dry_run:
            print(f"    [DRY RUN] {r2_key} ({file_size / 1024:.0f} KB)")
            uploaded += 1
            total_bytes += file_size
            continue

        content_type = get_content_type(img_name)
        client.upload_file(
            local_path,
            BUCKET_NAME,
            r2_key,
            ExtraArgs={"ContentType": content_type},
        )
        uploaded += 1
        total_bytes += file_size

    return uploaded, skipped, total_bytes


def update_supabase_urls():
    """Update image URLs in Supabase lessons to point to R2."""
    from supabase import create_client

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
        sys.exit(1)

    sb = create_client(url, key)

    # Fetch all lessons
    lessons = sb.table("lessons").select("id, hero_image_url, content_html, diagrams").execute()
    updated = 0

    for lesson in lessons.data:
        changes = {}

        # Rewrite hero image URL
        if lesson["hero_image_url"] and not lesson["hero_image_url"].startswith("http"):
            # Relative path like "Versailles_1919.jpg" or "lesson-01-hero.jpg"
            # We need the unit path context — get it from the content or DB
            new_url = f"{R2_PUBLIC_URL}/{lesson['hero_image_url']}"
            changes["hero_image_url"] = new_url

        # Rewrite image src in content_html
        if lesson["content_html"]:
            content = lesson["content_html"]
            # Find relative image srcs and rewrite to R2
            new_content = re.sub(
                r'src="(?!http)([^"]+\.(jpg|jpeg|png|gif|webp|svg))"',
                lambda m: f'src="{R2_PUBLIC_URL}/{m.group(1)}"',
                content,
            )
            if new_content != content:
                changes["content_html"] = new_content

        # Rewrite diagram URLs
        if lesson["diagrams"]:
            new_diagrams = []
            changed = False
            for d in lesson["diagrams"]:
                if d.get("url") and not d["url"].startswith("http"):
                    new_diagrams.append({**d, "url": f"{R2_PUBLIC_URL}/{d['url']}"})
                    changed = True
                else:
                    new_diagrams.append(d)
            if changed:
                changes["diagrams"] = new_diagrams

        if changes:
            sb.table("lessons").update(changes).eq("id", lesson["id"]).execute()
            updated += 1

    print(f"\nUpdated {updated} lesson records with R2 image URLs")


def main():
    dry_run = "--dry-run" in sys.argv
    update_db = "--update-db" in sys.argv

    print("Upload Images to Cloudflare R2")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Public URL: {R2_PUBLIC_URL}")
    if dry_run:
        print("MODE: DRY RUN (no uploads)")
    print()

    client = get_r2_client()

    print("Checking existing files in R2...")
    existing_keys = list_existing_keys(client)
    print(f"Found {len(existing_keys)} existing files\n")

    total_start = time.time()
    grand_uploaded = 0
    grand_skipped = 0
    grand_bytes = 0

    # Upload unit images
    for unit_dir in UNIT_DIRS:
        full_dir = os.path.join(PROJECT_ROOT, unit_dir)
        if not os.path.isdir(full_dir):
            continue

        img_count = len([f for f in os.listdir(full_dir) if is_lesson_image(f)])
        if img_count == 0:
            continue

        print(f"  {unit_dir}: {img_count} images")
        uploaded, skipped, nbytes = upload_directory(
            client, unit_dir, unit_dir, existing_keys, dry_run
        )
        grand_uploaded += uploaded
        grand_skipped += skipped
        grand_bytes += nbytes
        print(f"    -> {uploaded} uploaded, {skipped} skipped")

    # Upload root images
    for img_dir in ROOT_IMAGE_DIRS:
        full_dir = os.path.join(PROJECT_ROOT, img_dir)
        if not os.path.isdir(full_dir):
            continue

        img_count = len([f for f in os.listdir(full_dir) if is_lesson_image(f)])
        if img_count == 0:
            continue

        print(f"  {img_dir}: {img_count} images")
        uploaded, skipped, nbytes = upload_directory(
            client, img_dir, img_dir, existing_keys, dry_run
        )
        grand_uploaded += uploaded
        grand_skipped += skipped
        grand_bytes += nbytes
        print(f"    -> {uploaded} uploaded, {skipped} skipped")

    elapsed = time.time() - total_start

    print(f"\n{'=' * 45}")
    print(f"SUMMARY")
    print(f"{'=' * 45}")
    print(f"Uploaded:   {grand_uploaded}")
    print(f"Skipped:    {grand_skipped} (already in R2)")
    print(f"Total size: {grand_bytes / 1024 / 1024:.1f} MB")
    print(f"Time:       {elapsed:.1f}s")
    print(f"\nPublic URL: {R2_PUBLIC_URL}")

    if update_db and not dry_run:
        print("\nUpdating Supabase image URLs...")
        update_supabase_urls()

    print("\nDone!")


if __name__ == "__main__":
    main()
