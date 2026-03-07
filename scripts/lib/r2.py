"""Cloudflare R2 upload helpers — shared by narration, hero, and diagram scripts."""

import io
import os
import sys

import boto3
from botocore.config import Config
from PIL import Image


# ── Bucket constants ────────────────────────────────────────────────────

AUDIO_BUCKET = "studyvault-audio"
AUDIO_PUBLIC_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev"

IMAGES_BUCKET = "studyvault-images"
IMAGES_PUBLIC_URL = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"


# ── Client ──────────────────────────────────────────────────────────────

def get_r2_client():
    """Create an S3-compatible client for Cloudflare R2.

    Required env vars: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY
    """
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


# ── Image compression ──────────────────────────────────────────────────

COMPRESS_QUALITY = 82
HERO_MAX_WIDTH = 1200
DIAGRAM_MAX_WIDTH = 1000


def compress_image_bytes(data, max_width=HERO_MAX_WIDTH):
    """Compress image bytes: resize to max_width, JPEG quality 82.

    Returns compressed bytes. Skips compression if result would be larger.
    """
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=COMPRESS_QUALITY, optimize=True)
    compressed = buf.getvalue()

    # Only use compressed version if it's actually smaller
    return compressed if len(compressed) < len(data) else data


# ── Upload helpers ──────────────────────────────────────────────────────

def upload_bytes_to_r2(r2_client, bucket, r2_key, data, content_type="application/octet-stream"):
    """Upload bytes to R2. Compresses images automatically. Returns the public URL."""
    if bucket == IMAGES_BUCKET and content_type.startswith("image/"):
        max_w = DIAGRAM_MAX_WIDTH if "diagram" in r2_key else HERO_MAX_WIDTH
        old_size = len(data)
        data = compress_image_bytes(data, max_width=max_w)
        new_size = len(data)
        if new_size < old_size:
            print(f"  Compressed: {old_size // 1024}KB -> {new_size // 1024}KB ({(old_size - new_size) * 100 // old_size}% saved)")
        content_type = "image/jpeg"

    r2_client.put_object(
        Bucket=bucket,
        Key=r2_key,
        Body=data,
        ContentType=content_type,
    )
    public_url = AUDIO_PUBLIC_URL if bucket == AUDIO_BUCKET else IMAGES_PUBLIC_URL
    return f"{public_url}/{r2_key}"


def upload_file_to_r2(r2_client, bucket, local_path, r2_key, content_type="application/octet-stream"):
    """Upload a local file to R2. Compresses images automatically. Returns the public URL."""
    if bucket == IMAGES_BUCKET and content_type.startswith("image/"):
        with open(local_path, "rb") as f:
            data = f.read()
        max_w = DIAGRAM_MAX_WIDTH if "diagram" in r2_key else HERO_MAX_WIDTH
        old_size = len(data)
        data = compress_image_bytes(data, max_width=max_w)
        new_size = len(data)
        if new_size < old_size:
            print(f"  Compressed: {old_size // 1024}KB -> {new_size // 1024}KB ({(old_size - new_size) * 100 // old_size}% saved)")
        r2_client.put_object(
            Bucket=bucket,
            Key=r2_key,
            Body=data,
            ContentType="image/jpeg",
        )
        public_url = IMAGES_PUBLIC_URL
        return f"{public_url}/{r2_key}"

    r2_client.upload_file(
        local_path,
        bucket,
        r2_key,
        ExtraArgs={"ContentType": content_type},
    )
    public_url = AUDIO_PUBLIC_URL if bucket == AUDIO_BUCKET else IMAGES_PUBLIC_URL
    return f"{public_url}/{r2_key}"
