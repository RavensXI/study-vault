"""Cloudflare R2 upload helpers — shared by narration, hero, and diagram scripts."""

import os
import sys

import boto3
from botocore.config import Config


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


# ── Upload helpers ──────────────────────────────────────────────────────

def upload_bytes_to_r2(r2_client, bucket, r2_key, data, content_type="application/octet-stream"):
    """Upload bytes to R2. Returns the public URL."""
    r2_client.put_object(
        Bucket=bucket,
        Key=r2_key,
        Body=data,
        ContentType=content_type,
    )
    public_url = AUDIO_PUBLIC_URL if bucket == AUDIO_BUCKET else IMAGES_PUBLIC_URL
    return f"{public_url}/{r2_key}"


def upload_file_to_r2(r2_client, bucket, local_path, r2_key, content_type="application/octet-stream"):
    """Upload a local file to R2. Returns the public URL."""
    r2_client.upload_file(
        local_path,
        bucket,
        r2_key,
        ExtraArgs={"ContentType": content_type},
    )
    public_url = AUDIO_PUBLIC_URL if bucket == AUDIO_BUCKET else IMAGES_PUBLIC_URL
    return f"{public_url}/{r2_key}"
