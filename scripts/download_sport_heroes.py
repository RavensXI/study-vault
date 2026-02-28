"""
download_sport_heroes.py
Download hero images from Wikimedia Commons for Sport Science R180 (10 lessons).

Usage:  python download_sport_heroes.py

Images saved as lesson-NN-hero.jpg in sport-science/r180/.
Attribution info saved to sport-science/hero_attributions.json.
Skips existing files.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(PROJECT_ROOT, "sport-science", "r180")
ATTRIB_FILE = os.path.join(PROJECT_ROOT, "sport-science", "hero_attributions.json")

USER_AGENT = "StudyVault/1.0 (educational)"
MIN_FILE_SIZE = 50 * 1024  # 50 KB
THUMB_WIDTH = 1280

# ---------------------------------------------------------------------------
# Search terms per lesson (multiple fallbacks)
# ---------------------------------------------------------------------------
SEARCHES = {
    1:  ["football pitch waterlogged", "rugby training rain", "muddy sports field"],
    2:  ["athlete hamstring stretch", "runner stretching muscles", "sports flexibility exercise"],
    3:  ["football team warm up pitch", "rugby warm up exercises", "athletes jogging warm up"],
    4:  ["athlete cooling down after race", "runner resting after marathon", "sports recovery water"],
    5:  ["football ankle injury stretcher", "rugby player injured tackle", "sports fracture ambulance pitch"],
    6:  ["tennis player elbow injury", "runner holding shin pain", "athlete physiotherapy treatment"],
    7:  ["sports pitch safety inspection", "sports ground first aid post", "sports event medical tent"],
    8:  ["sports physiotherapy rehabilitation", "athlete knee rehabilitation exercise", "sports medicine clinic"],
    9:  ["asthma inhaler exercise", "athlete using inhaler", "exercise induced asthma sport"],
    10: ["defibrillator sports centre wall", "AED automated external defibrillator", "heart defibrillator public access"],
}


def search_commons(query, limit=5):
    """Search Wikimedia Commons for images matching query."""
    params = urllib.parse.urlencode({
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrnamespace': '6',
        'gsrsearch': query,
        'gsrlimit': str(limit),
        'prop': 'imageinfo',
        'iiprop': 'url|extmetadata|size|mime',
        'iiurlwidth': str(THUMB_WIDTH),
    })
    url = f"https://commons.wikimedia.org/w/api.php?{params}"
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    pages = data.get('query', {}).get('pages', {})
    results = []
    for page in pages.values():
        ii = page.get('imageinfo', [{}])[0]
        if not ii:
            continue
        mime = ii.get('mime', '')
        if mime not in ('image/jpeg', 'image/png', 'image/webp'):
            continue
        width = ii.get('width', 0)
        if width < 800:
            continue
        thumb = ii.get('thumburl', '')
        if not thumb:
            continue
        ext = ii.get('extmetadata', {})
        author = ext.get('Artist', {}).get('value', 'Unknown')
        license_name = ext.get('LicenseShortName', {}).get('value', '')
        desc = ext.get('ImageDescription', {}).get('value', '')
        results.append({
            'thumb_url': thumb,
            'author': author,
            'license': license_name,
            'description': desc,
            'title': page.get('title', ''),
        })
    return results


def download_image(url, filepath):
    """Download image from URL to filepath."""
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if len(data) < MIN_FILE_SIZE:
        return False
    with open(filepath, 'wb') as f:
        f.write(data)
    return True


def strip_html(text):
    """Simple HTML tag stripper."""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Load existing attributions
    if os.path.exists(ATTRIB_FILE):
        with open(ATTRIB_FILE, 'r', encoding='utf-8') as f:
            attributions = json.load(f)
    else:
        attributions = {}

    total = 0
    for lesson_num, search_terms in sorted(SEARCHES.items()):
        filename = f"lesson-{lesson_num:02d}-hero.jpg"
        filepath = os.path.join(OUT_DIR, filename)
        attr_key = f"r180/{filename}"

        if os.path.exists(filepath):
            print(f"  SKIP (exists): {filename}")
            continue

        print(f"\nLesson {lesson_num}: searching...")
        downloaded = False

        for query in search_terms:
            print(f"  Trying: '{query}'")
            try:
                results = search_commons(query)
            except Exception as e:
                print(f"    Search failed: {e}")
                time.sleep(2)
                continue

            for r in results:
                try:
                    ok = download_image(r['thumb_url'], filepath)
                    if ok:
                        author = strip_html(r.get('author', 'Unknown'))
                        if len(author) > 100:
                            author = author[:80].strip()
                        attributions[attr_key] = {
                            'author': author,
                            'license': r.get('license', ''),
                            'source': r.get('title', ''),
                        }
                        print(f"  SAVED: {filename} ({r.get('license', '')})")
                        downloaded = True
                        total += 1
                        break
                except Exception as e:
                    print(f"    Download failed: {e}")
                    continue

            if downloaded:
                break
            time.sleep(1)

        if not downloaded:
            print(f"  [WARN] No suitable image found for lesson {lesson_num}")

        time.sleep(3)

    # Save attributions
    with open(ATTRIB_FILE, 'w', encoding='utf-8') as f:
        json.dump(attributions, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Downloaded {total} new hero image(s).")
    print(f"Attributions saved to {ATTRIB_FILE}")


if __name__ == "__main__":
    main()
