"""
Upload all narration MP3 files to Cloudflare R2.
Organises files by subject/unit path to match lesson manifest src paths.

Usage:
    python scripts/upload_to_r2.py                # Upload all MP3s
    python scripts/upload_to_r2.py --dry-run      # Show what would be uploaded

Env vars required:
    R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID
"""

import io
import os
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

BUCKET_NAME = "studyvault-audio"
R2_PUBLIC_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev"

# Directories containing narration MP3s — key is the R2 prefix
UNIT_DIRS = {
    "history/conflict-tension": "history/conflict-tension",
    "history/health-people": "history/health-people",
    "history/elizabethan": "history/elizabethan",
    "history/america": "history/america",
    "business/theme-1": "business/theme-1",
    "business/theme-2": "business/theme-2",
    "geography/paper-1": "geography/paper-1",
    "geography/paper-2": "geography/paper-2",
    "sport-science/r180": "sport-science/r180",
}


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
    """List all existing object keys in the bucket with given prefix."""
    keys = set()
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.add(obj["Key"])
    return keys


def upload_unit(client, unit_dir, r2_prefix, existing_keys, dry_run=False):
    """Upload all MP3 files from a unit directory. Returns (uploaded, skipped, bytes)."""
    full_dir = os.path.join(PROJECT_ROOT, unit_dir)
    if not os.path.isdir(full_dir):
        return 0, 0, 0

    mp3_files = sorted(
        f for f in os.listdir(full_dir)
        if f.startswith("narration_") and f.endswith(".mp3")
    )

    if not mp3_files:
        return 0, 0, 0

    uploaded = 0
    skipped = 0
    total_bytes = 0

    for mp3_name in mp3_files:
        r2_key = f"{r2_prefix}/{mp3_name}"
        local_path = os.path.join(full_dir, mp3_name)
        file_size = os.path.getsize(local_path)

        if r2_key in existing_keys:
            skipped += 1
            continue

        if dry_run:
            print(f"    [DRY RUN] {r2_key} ({file_size / 1024:.0f} KB)")
            uploaded += 1
            total_bytes += file_size
            continue

        client.upload_file(
            local_path,
            BUCKET_NAME,
            r2_key,
            ExtraArgs={"ContentType": "audio/mpeg"},
        )
        uploaded += 1
        total_bytes += file_size

    return uploaded, skipped, total_bytes


def main():
    dry_run = "--dry-run" in sys.argv

    print(f"Upload Narration MP3s to Cloudflare R2")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Public URL: {R2_PUBLIC_URL}")
    if dry_run:
        print("MODE: DRY RUN (no uploads)")
    print()

    client = get_r2_client()

    # List existing objects to skip re-uploads
    print("Checking existing files in R2...")
    existing_keys = list_existing_keys(client)
    print(f"Found {len(existing_keys)} existing files\n")

    total_start = time.time()
    grand_uploaded = 0
    grand_skipped = 0
    grand_bytes = 0

    for r2_prefix, unit_dir in UNIT_DIRS.items():
        full_dir = os.path.join(PROJECT_ROOT, unit_dir)
        if not os.path.isdir(full_dir):
            continue

        mp3_count = len([
            f for f in os.listdir(full_dir)
            if f.startswith("narration_") and f.endswith(".mp3")
        ])

        if mp3_count == 0:
            continue

        print(f"  {unit_dir}: {mp3_count} MP3s")
        uploaded, skipped, nbytes = upload_unit(
            client, unit_dir, r2_prefix, existing_keys, dry_run
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
    print(f"Total size: {grand_bytes / 1024 / 1024:.0f} MB")
    print(f"Time:       {elapsed:.1f}s")
    print(f"\nPublic URL: {R2_PUBLIC_URL}")
    print(f"Example:    {R2_PUBLIC_URL}/history/conflict-tension/narration_lesson-01_n1.mp3")
    print(f"\nDone!")


if __name__ == "__main__":
    main()
