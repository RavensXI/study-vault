# -*- coding: utf-8 -*-
"""Tile-clipping or genuinely flat ground? And if clipped, what survives a crop?

    python scratchpad/_geo_guided/_map_tile_edge.py

"Some cells have no contours" is not evidence of a bug. The Norfolk Broads are
the flattest place in England; a bare sheet there is correct. Cropping one would
be vandalism. So the test has to be the shape of the boundary, not the amount of
ink.

A contour layer that failed to render stops at a tile edge: a straight vertical
or horizontal line, spanning the sheet, with dense ink on one side and near-zero
on the other. Real lowland fades out in organic, ragged patches and never lines
up with a column of pixels.

So: score every candidate column and row as a splitter. A cut is called only if
one side is dense, the other is essentially bare, and the drop happens over a
narrow band. Then report the crop that keeps the good side.

Prints CROP lines as x0,y0,x1,y1 in original pixel coordinates.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_mapcache")

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from PIL import Image, ImageFilter

SUSPECT = [
    "yorkshire-dales-z15-final.jpg", "northumberland-z16-final.jpg",
    "norfolk-broads-z16-final.jpg", "south-downs-z15-final.jpg",
    "dartmoor-z15-final.jpg", "clitheroe-z15-final.jpg",
    "dorset-coast-z15-final.jpg", "south-downs-z16-final.jpg",
    "dorset-coast-z16-final.jpg", "dartmoor-z16-final.jpg",
]


def thin_mask(im):
    w, h = im.size
    px = im.load()
    m = Image.new("L", (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 110 and r - b > 30 and 15 < r - g < 95 and g >= b and r < 240:
                mp[x, y] = 255
    er = m.filter(ImageFilter.MinFilter(3)).load()
    t = Image.new("L", (w, h), 0)
    tp = t.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y] and not er[x, y]:
                tp[x, y] = 255
    return t


def profiles(t):
    w, h = t.size
    tp = t.load()
    col = [0] * w
    row = [0] * h
    for y in range(h):
        for x in range(w):
            if tp[x, y]:
                col[x] += 1
                row[y] += 1
    return col, row


def best_split(prof, span):
    """Return (pos, side, dense, bare, sharpness) for the strongest edge."""
    n = len(prof)
    lo, hi = int(n * 0.12), int(n * 0.88)          # ignore sheet margins
    best = None
    for i in range(lo, hi):
        left = sum(prof[:i]) / float(i * span)
        right = sum(prof[i:]) / float((n - i) * span)
        for dense, bare, side in ((left, right, "keep-left"), (right, left, "keep-right")):
            if dense < 0.004:                       # nothing worth keeping
                continue
            ratio = bare / dense if dense else 1.0
            if ratio > 0.10:                        # not a clean disappearance
                continue
            # sharpness: the drop must happen in a narrow band, not gradually.
            k = max(6, n // 60)
            a = sum(prof[max(0, i - k):i]) / float(k * span)
            b = sum(prof[i:i + k]) / float(k * span)
            near, far = (a, b) if side == "keep-left" else (b, a)
            sharp = (near - far) / near if near > 0 else 0
            if sharp < 0.75:
                continue
            score = dense * (1 - ratio) * sharp
            if not best or score > best[-1]:
                best = (i, side, dense, bare, sharp, score)
    return best


def main():
    print("%-34s %s" % ("map", "verdict"))
    crops = {}
    for name in SUSPECT:
        p = os.path.join(CACHE, name)
        if not os.path.exists(p):
            print("%-34s (not cached)" % name)
            continue
        im0 = Image.open(p).convert("RGB")
        W, H = im0.size
        im = im0.resize((900, int(H * 900.0 / W)))
        im = im.crop((0, 0, im.size[0], int(im.size[1] * 0.975)))   # drop attribution
        t = thin_mask(im)
        w, h = t.size
        col, row = profiles(t)
        v = best_split(col, h)
        z = best_split(row, w)
        pick = None
        if v and (not z or v[-1] >= z[-1]):
            pick = ("vertical", v)
        elif z:
            pick = ("horizontal", z)

        if not pick:
            print("%-34s flat ground (no straight edge) - LEAVE ALONE" % name)
            continue
        axis, (i, side, dense, bare, sharp, score) = pick
        sx = W / float(w)
        sy = H / float(im.size[1])
        if axis == "vertical":
            x = int(i * sx)
            box = (0, 0, x, H) if side == "keep-left" else (x, 0, W, H)
        else:
            y = int(i * sy)
            box = (0, 0, W, y) if side == "keep-left" else (0, y, W, H)
        keep = 100.0 * ((box[2] - box[0]) * (box[3] - box[1])) / (W * H)
        print("%-34s CLIPPED %s at %s, %s, keeps %d%% (drop %.0f%%)"
              % (name, axis, i, side, round(keep), sharp * 100))
        crops[name] = box

    print()
    for n, b in crops.items():
        print("CROP %s %d,%d,%d,%d" % (n, b[0], b[1], b[2], b[3]))
    if not crops:
        print("no clipped sheets")


if __name__ == "__main__":
    main()
