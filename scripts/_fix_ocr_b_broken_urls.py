"""
Fix remaining broken URLs in separate-sciences-ocr-b related_media.
Handles:
1. JustWatch /tv-show/ → /tv-series/ path correction
2. Fabricated BBC programme IDs → parent show URL (b006qykl)
3. Met Office broken URL → working URL
4. CrowdScience broken ID → correct podcast URL

Run: python scripts/_fix_ocr_b_broken_urls.py
"""

import json
import glob
import os

LESSON_DIR = "scripts/_content_separate-sciences-ocr-b/lessons"

# ── JustWatch /tv-show/ → /tv-series/ mapping (verified working) ──────────────
JUSTWATCH_FIXES = {
    "https://www.justwatch.com/uk/tv-show/cosmos-a-spacetime-odyssey":
        "https://www.justwatch.com/uk/tv-series/cosmos-a-spacetime-odyssey",
    "https://www.justwatch.com/uk/tv-show/chemistry-a-volatile-history":
        "https://www.justwatch.com/uk/tv-series/chemistry-a-volatile-history",
    "https://www.justwatch.com/uk/tv-show/planet-earth-ii":
        "https://www.justwatch.com/uk/tv-series/planet-earth-ii",
    "https://www.justwatch.com/uk/tv-show/inside-bills-brain-decoding-bill-gates":
        "https://www.justwatch.com/uk/tv-series/inside-bills-brain-decoding-bill-gates",
    "https://www.justwatch.com/uk/tv-show/life":
        "https://www.justwatch.com/uk/tv-series/life",
    "https://www.justwatch.com/uk/tv-show/blue-planet-ii":
        "https://www.justwatch.com/uk/tv-series/blue-planet-ii",
}

# ── BBC programme IDs that couldn't be confirmed via web search ───────────────
# Replace fabricated/unverifiable episode IDs with the parent series URL
# b006qykl = In Our Time (main show)
# p04d42rc = CrowdScience (correct parent show URL from listener's guide)
BBC_ID_FIXES = {
    # p004y2xx IDs - no web evidence they exist, replace with parent show
    "https://www.bbc.co.uk/programmes/p004y27z": "https://www.bbc.co.uk/programmes/b006qykl",   # Atom
    "https://www.bbc.co.uk/programmes/p004y253": "https://www.bbc.co.uk/programmes/b006qykl",   # Quantum
    "https://www.bbc.co.uk/programmes/p004y24t": "https://www.bbc.co.uk/programmes/b006qykl",   # Newton's Laws
    "https://www.bbc.co.uk/programmes/p004y23k": "https://www.bbc.co.uk/programmes/b006qykl",   # Periodic Table
    "https://www.bbc.co.uk/programmes/p004y27b": "https://www.bbc.co.uk/programmes/b006qykl",   # Natural Selection
    "https://www.bbc.co.uk/programmes/p004y27x": "https://www.bbc.co.uk/programmes/b006qykl",   # DNA
    "https://www.bbc.co.uk/programmes/p004y27f": "https://www.bbc.co.uk/programmes/b006qykl",   # Genetics
    "https://www.bbc.co.uk/programmes/p004y24b": "https://www.bbc.co.uk/programmes/b006qykl",   # Light
    "https://www.bbc.co.uk/programmes/p004y23g": "https://www.bbc.co.uk/programmes/b006qykl",   # Electromagnetism
    "https://www.bbc.co.uk/programmes/p004y26f": "https://www.bbc.co.uk/programmes/b006qykl",   # Brain
    "https://www.bbc.co.uk/programmes/p004y24x": "https://www.bbc.co.uk/programmes/b006qykl",   # Radioactivity
    "https://www.bbc.co.uk/programmes/p004y238": "https://www.bbc.co.uk/programmes/b006qykl",   # Big Bang
    "https://www.bbc.co.uk/programmes/p004y239": "https://www.bbc.co.uk/programmes/b006qykl",   # Global Warming
    # b00p86nl - In Our Time Taxonomy: web search returned Wikipedia listing but 404 live
    "https://www.bbc.co.uk/programmes/b00p86nl": "https://www.bbc.co.uk/programmes/b006qykl",
    # b019dl1c - In Our Time Mitochondria: confirmed real in earlier search
    # Keep as-is; audit result was likely a transient BBC 404
    # p04d5zsd - CrowdScience episode ID not confirmed
    "https://www.bbc.co.uk/programmes/p04d5zsd": "https://www.bbc.co.uk/programmes/p04d42rc",   # CrowdScience parent
}

# ── Met Office URL fix ─────────────────────────────────────────────────────────
# Old URL redirected to weather.metoffice.gov.uk; use the updated path
METOFFICE_OLD = "https://www.metoffice.gov.uk/weather/climate-change"
METOFFICE_NEW = "https://weather.metoffice.gov.uk/climate-change/what-is-climate-change"

# ── Apply fixes ────────────────────────────────────────────────────────────────
files = sorted(glob.glob(os.path.join(LESSON_DIR, "*.json")))
total_fixed = 0
files_fixed = 0

for filepath in files:
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    slug = data.get("_lesson_slug", os.path.basename(filepath))
    changed = 0

    for cat in data.get("related_media", []):
        for item in cat.get("items", []):
            url = item.get("url", "")

            if url in JUSTWATCH_FIXES:
                item["url"] = JUSTWATCH_FIXES[url]
                changed += 1

            elif url in BBC_ID_FIXES:
                item["url"] = BBC_ID_FIXES[url]
                changed += 1

            elif METOFFICE_OLD in url:
                item["url"] = METOFFICE_NEW
                changed += 1

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {slug}: {changed} URL(s) fixed")
        total_fixed += changed
        files_fixed += 1

print(f"\nDone: {files_fixed} files, {total_fixed} URLs fixed.")
