"""Pixabay API helper for hero image search.

Free tier: ~100 requests/minute. Licence permits storing and self-hosting;
attribution not required but we credit anyway: "Image: {user} / Pixabay".
safesearch is always on — these images front lessons for 15-16 year olds.
"""
import json
import os
import time
import urllib.parse
import urllib.request

_last = 0.0
_DELAY = 0.7


def _get_key():
    key = os.environ.get("PIXABAY_API_KEY", "")
    if not key:
        raise RuntimeError("PIXABAY_API_KEY env var not set")
    return key


def search_pixabay(query, per_page=6):
    """Returns list of {url, title, photographer, width, height, source}."""
    global _last
    wait = _DELAY - (time.time() - _last)
    if wait > 0:
        time.sleep(wait)
    params = urllib.parse.urlencode({
        "key": _get_key(), "q": query, "image_type": "photo",
        "orientation": "horizontal", "per_page": max(per_page, 3),
        "safesearch": "true",
    })
    req = urllib.request.Request(f"https://pixabay.com/api/?{params}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        _last = time.time()
        data = json.loads(resp.read())

    results = []
    for hit in data.get("hits", []):
        img_url = hit.get("largeImageURL") or hit.get("webformatURL", "")
        if not img_url:
            continue
        results.append({
            "url": img_url,
            "title": (hit.get("tags") or query).replace(",", " —", 1),
            "photographer": hit.get("user") or "",
            "width": hit.get("imageWidth", 0),
            "height": hit.get("imageHeight", 0),
            "source": "pixabay",
        })
    return results
