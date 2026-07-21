# -*- coding: utf-8 -*-
"""Which OS extracts actually carry contour lines, and at what size?

    python scratchpad/_geo_guided/_audit_map_contours.py

Tom: "some of the maps lose their contours for some reason". This measures it
instead of guessing. OS contour lines print in a brown/orange ink distinct from
the greens, greys and blues around them, so counting pixels in that hue band
gives an objective per-sheet score. Also reports pixel size and the ground area
each sheet covers, which is what decides whether it is legible on a phone.
"""
import io, os, sys, urllib.request

R2 = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_mapcache")

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow needed: python -m pip install pillow")

import boto3


def list_maps():
    s3 = boto3.client(
        "s3",
        endpoint_url="https://%s.r2.cloudflarestorage.com" % os.environ["R2_ACCOUNT_ID"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(
            Bucket="studyvault-images", Prefix="geography/os-maps/"):
        keys += [o["Key"].split("/")[-1] for o in page.get("Contents", [])]
    return sorted(k for k in keys if k.lower().endswith((".jpg", ".png")))


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        # R2 rejects urllib's default user agent with a 403
        req = urllib.request.Request(R2 + name, headers={"User-Agent": "Mozilla/5.0 StudyVault-audit"})
        with urllib.request.urlopen(req, timeout=120) as r, io.open(p, "wb") as f:
            f.write(r.read())
    return p


def contour_score(path):
    """Fraction of pixels in the OS contour ink band (brown/orange), per 10k px."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # downsample for speed; contour lines survive a modest reduction
    small = im.resize((min(w, 900), max(1, int(h * min(w, 900) / w))))
    sw, sh = small.size
    px = small.load()
    hits = 0
    for y in range(sh):
        for x in range(sw):
            r, g, b = px[x, y]
            # brown/orange ink: red clearly ahead of blue, green between, mid tone
            if r > 120 and r - b > 38 and 18 < r - g < 85 and g > b and 90 < r < 235:
                hits += 1
    return w, h, hits, round(10000.0 * hits / (sw * sh), 1)


def main():
    maps = list_maps()
    print("%-34s %-12s %-9s %s" % ("map", "pixels", "contour", "verdict"))
    rows = []
    for m in maps:
        try:
            w, h, hits, score = contour_score(fetch(m))
        except Exception as e:
            print("%-34s  ERROR %s" % (m, e))
            continue
        rows.append((m, w, h, score))
    if not rows:
        return
    scores = sorted(r[3] for r in rows)
    med = scores[len(scores) // 2]
    for m, w, h, score in rows:
        if score < 12:
            verdict = "NO CONTOURS"
        elif score < med * 0.45:
            verdict = "sparse"
        else:
            verdict = "ok"
        print("%-34s %-12s %-9s %s" % (m, "%dx%d" % (w, h), score, verdict))
    print()
    print("median contour score: %s" % med)
    print("sheets with no usable contours: %d of %d"
          % (sum(1 for r in rows if r[3] < 12), len(rows)))


if __name__ == "__main__":
    main()
