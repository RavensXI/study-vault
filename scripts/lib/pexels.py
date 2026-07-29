"""Pexels API helper for hero image search.

Free tier: 200 requests/hour, 20,000/month. Licence permits storing and
self-hosting; attribution not required but we credit anyway:
"Photo: {photographer} / Pexels".
"""
import json
import os
import time
import urllib.parse
import urllib.request

_last = 0.0
_DELAY = 0.4


def _get_key():
    key = os.environ.get("PEXELS_API_KEY", "")
    if not key:
        raise RuntimeError("PEXELS_API_KEY env var not set")
    return key


def search_pexels(query, per_page=6, orientation="landscape"):
    """Returns list of {url, title, photographer, width, height, source}."""
    global _last
    wait = _DELAY - (time.time() - _last)
    if wait > 0:
        time.sleep(wait)
    params = urllib.parse.urlencode({
        "query": query, "per_page": per_page, "orientation": orientation,
    })
    req = urllib.request.Request(
        f"https://api.pexels.com/v1/search?{params}",
        headers={"Authorization": _get_key(),
                 # Cloudflare fronts api.pexels.com and 403s python's default UA
                 "User-Agent": "StudyVaultHeroBot/1.0 (https://www.studyvault.co.uk)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        _last = time.time()
        data = json.loads(resp.read())

    results = []
    for photo in data.get("photos", []):
        src = photo.get("src", {})
        img_url = src.get("large2x") or src.get("large") or src.get("original", "")
        if not img_url:
            continue
        results.append({
            "url": img_url,
            "title": photo.get("alt") or query,
            "photographer": photo.get("photographer") or "",
            "width": photo.get("width", 0),
            "height": photo.get("height", 0),
            "source": "pexels",
        })
    return results
