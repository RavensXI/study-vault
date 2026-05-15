"""
Unsplash API helpers for hero image search.

Usage:
    from lib.unsplash import search_unsplash, trigger_unsplash_download
"""
import os
import time
import urllib.parse
import urllib.request
import json

UNSPLASH_API_BASE = "https://api.unsplash.com"
# Respect Unsplash API rate limit: 50 requests/hour for demo, 5000/hour for production
_last_request_time = 0.0
_REQUEST_DELAY = 0.3  # seconds between requests


def _get_key():
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        raise RuntimeError("UNSPLASH_ACCESS_KEY env var not set")
    return key


def _make_request(url):
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _REQUEST_DELAY:
        time.sleep(_REQUEST_DELAY - elapsed)
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Client-ID {_get_key()}",
            "Accept-Version": "v1",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        _last_request_time = time.time()
        return json.loads(resp.read())


def search_unsplash(query, per_page=5, orientation="landscape"):
    """Search Unsplash for images matching the query.

    Returns a list of dicts with keys:
        url, title, photographer, width, height, _download_location, source
    """
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
        "orientation": orientation,
    })
    url = f"{UNSPLASH_API_BASE}/search/photos?{params}"
    try:
        data = _make_request(url)
    except Exception as e:
        raise RuntimeError(f"Unsplash search failed for '{query}': {e}") from e

    results = []
    for photo in data.get("results", []):
        urls = photo.get("urls", {})
        # Prefer the 'regular' size (1080px), fall back to 'full'
        img_url = urls.get("regular") or urls.get("full") or ""
        if not img_url:
            continue
        user = photo.get("user", {})
        results.append({
            "url": img_url,
            "original_url": urls.get("full") or img_url,
            "title": photo.get("alt_description") or query,
            "photographer": user.get("name") or "",
            "width": photo.get("width", 0),
            "height": photo.get("height", 0),
            "_download_location": photo.get("links", {}).get("download_location", ""),
            "source": "unsplash",
        })
    return results


def trigger_unsplash_download(download_location):
    """Hit the Unsplash download tracking endpoint (required by API guidelines)."""
    if not download_location:
        return
    try:
        params = urllib.parse.urlencode({"client_id": _get_key()})
        url = f"{download_location}?{params}"
        _make_request(url)
    except Exception:
        pass  # Non-fatal — tracking only
