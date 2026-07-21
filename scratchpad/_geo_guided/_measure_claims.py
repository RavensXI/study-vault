# -*- coding: utf-8 -*-
"""Test the two remaining claims before they become questions.

    python scratchpad/_geo_guided/_measure_claims.py

Claim A (peak-district-z15): every patch of woodland lies beside a watercourse.
  Tested by dilating the blue-water mask and asking what fraction of green
  woodland pixels fall inside it. If the answer is not near-total the claim is
  false and no question gets written on it.

Claim B (yorkshire-dales-z15-w90): contours are packed on the western flank of
  Cow Close Fell and widely spaced over its top.
  Tested by comparing thin-contour ink in the two regions.

Both are claims about what is positively drawn, which is the sort a failed
render cannot invent. Absence is never the evidence.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_mapcache")
CROP = os.path.join(HERE, "_cropped")

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from PIL import Image, ImageFilter


def thin_ink(im, box):
    """Thin-contour pixels per 10k in a box (x0,y0,x1,y1)."""
    sub = im.crop(box)
    w, h = sub.size
    px = sub.load()
    m = Image.new("L", (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 110 and r - b > 30 and 15 < r - g < 95 and g >= b and r < 240:
                mp[x, y] = 255
    ep = m.filter(ImageFilter.MinFilter(3)).load()
    n = sum(1 for y in range(h) for x in range(w) if mp[x, y] and not ep[x, y])
    return 10000.0 * n / (w * h)


def claim_a():
    im = Image.open(os.path.join(CACHE, "peak-district-z15-final.jpg")).convert("RGB")
    w, h = im.size
    px = im.load()
    water = Image.new("L", (w, h), 0)
    wood = Image.new("L", (w, h), 0)
    wp, dp = water.load(), wood.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            # OS water: pale-to-mid blue, blue clearly ahead of red
            if b > 150 and b - r > 25 and b >= g:
                wp[x, y] = 255
            # OS woodland: green fill, green ahead of both others
            if g > 150 and g - r > 18 and g - b > 18:
                dp[x, y] = 255
    # "beside" = within roughly 60 m on the ground (~20 px at this scale)
    near = water.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.MaxFilter(21))
    np_, dpx = near.load(), wood.load()
    tot = inside = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if dpx[x, y]:
                tot += 1
                if np_[x, y]:
                    inside += 1
    pct = 100.0 * inside / tot if tot else 0
    print("CLAIM A  woodland beside water, peak-district-z15")
    print("         woodland samples=%d  within reach of water=%.0f%%" % (tot, pct))
    print("         verdict: %s" % ("SUPPORTED" if pct >= 85 else "NOT SUPPORTED - do not write it"))
    return pct


def claim_b():
    p = os.path.join(CROP, "yorkshire-dales-z15-w90-final.jpg")
    im = Image.open(p).convert("RGB")
    W, H = im.size
    # Read off the sheet: the summit rings sit around x 250-560, y 640-880;
    # the packed western/northern flank runs above them, y 300-560.
    top = thin_ink(im, (250, 640, 560, 880))
    flank = thin_ink(im, (250, 300, 560, 560))
    print()
    print("CLAIM B  contour spacing, yorkshire-dales-z15-w90 (%dx%d)" % (W, H))
    print("         summit area ink/10k = %.1f" % top)
    print("         flank  area ink/10k = %.1f" % flank)
    print("         flank is %.1fx the summit" % (flank / top if top else 0))
    print("         verdict: %s" % ("SUPPORTED" if flank > top * 1.8 else "NOT SUPPORTED - do not write it"))


if __name__ == "__main__":
    claim_a()
    claim_b()
