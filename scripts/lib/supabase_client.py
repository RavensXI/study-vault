"""Supabase client factory — single source of truth for all pipeline scripts."""

import os
import sys

from supabase import create_client


def get_client():
    """Create a Supabase client using service key from environment variables.

    Required env vars: SUPABASE_URL, SUPABASE_SERVICE_KEY
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        sys.exit(1)
    return create_client(url, key)
