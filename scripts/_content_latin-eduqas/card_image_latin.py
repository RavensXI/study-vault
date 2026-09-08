# -*- coding: utf-8 -*-
"""Pick and upload the homepage card image for GCSE Latin.

Same rule as the hero pipeline: no image is used unseen. Candidates are
downloaded, graded by a vision model against a brief, and only an A ships. The
winner lands on R2 at homepage-cards/latin-eduqas.jpg, which is what index.html
and freeSubjectMeta point at.

Usage: python scripts/_content_latin-eduqas/card_image_latin.py
"""
import base64
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import anthropic  # noqa: E402
from lib.unsplash import search_unsplash, trigger_unsplash_download  # noqa: E402
from lib.wikimedia import resize_and_compress  # noqa: E402
from lib.r2 import get_r2_client, IMAGES_BUCKET, IMAGES_PUBLIC_URL  # noqa: E402

KEY = "homepage-cards/latin-eduqas.jpg"
QUERIES = [
    "roman forum ruins",
    "latin inscription stone",
    "roman columns temple",
    "roman mosaic floor",
    "ancient roman amphitheatre",
]
BRIEF = """You are choosing the homepage card image for a GCSE Latin revision course.

The card is a small landscape photograph students see on a grid of subject cards. It must read instantly as ancient Rome and the Latin language: carved Latin inscriptions, Roman temples and columns, the Forum, Roman mosaics or statuary.

Look at the image. Reply in EXACTLY this format:

GRADE: A or B or C
SHOWS: one factual sentence (max 18 words) describing what the image actually shows.

Grading:
A = unmistakably ancient Roman, photographic, clean composition, reads well small.
B = plausibly classical but generic, or a cluttered composition.
C = wrong: not Roman, a modern scene, an illustration, text-heavy, a watermark, a logo, or a person's face dominating the frame.
"""


def fetch(url):
    src = dst = None
    try:
        import urllib.request
        with tempfile.NamedTemporaryFile(delete=False, suffix=".img") as f:
            src = f.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            dst = f.name
        req = urllib.request.Request(url, headers={"User-Agent": "StudyVaultHeroBot/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        open(src, "wb").write(data)
        resize_and_compress(src, dst, max_width=1200, quality=82)
        return open(dst, "rb").read()
    except Exception as e:
        print("   fetch fail:", e)
        return None
    finally:
        for p in (src, dst):
            if p:
                try:
                    os.unlink(p)
                except OSError:
                    pass


def main():
    cl = anthropic.Anthropic()
    best = None
    for q in QUERIES:
        print("unsplash:", q)
        try:
            results = search_unsplash(q, per_page=4)
        except Exception as e:
            print("  search failed:", e)
            continue
        for photo in results[:3]:
            jpeg = fetch(photo["url"])
            if not jpeg:
                continue
            msg = cl.messages.create(
                model="claude-haiku-4-5-20251001", max_tokens=200,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {
                        "type": "base64", "media_type": "image/jpeg",
                        "data": base64.b64encode(jpeg).decode()}},
                    {"type": "text", "text": BRIEF}]}])
            text = msg.content[0].text
            grade = "C"
            for g in ("A", "B", "C"):
                if ("GRADE: " + g) in text:
                    grade = g
                    break
            shows = text.split("SHOWS:")[-1].strip() if "SHOWS:" in text else ""
            print("  [%s] %s — %s" % (grade, photo.get("photographer", "?"), shows[:70]))
            if grade == "A":
                best = (jpeg, photo, shows)
                break
            if grade == "B" and best is None:
                best = (jpeg, photo, shows)
        if best and best[0] and "A" == grade:
            break
    if not best:
        print("no candidate found")
        sys.exit(1)
    jpeg, photo, shows = best
    r2 = get_r2_client()
    r2.put_object(Bucket=IMAGES_BUCKET, Key=KEY, Body=jpeg, ContentType="image/jpeg")
    print("uploaded: %s/%s (%d KB)" % (IMAGES_PUBLIC_URL, KEY, len(jpeg) // 1024))
    print("shows:", shows)
    print("credit: Photo:", photo.get("photographer"), "/ Unsplash")
    try:
        trigger_unsplash_download(photo.get("_download_location", ""))
    except Exception:
        pass


if __name__ == "__main__":
    main()
