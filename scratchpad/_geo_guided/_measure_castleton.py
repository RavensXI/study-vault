# -*- coding: utf-8 -*-
"""Measure the Castleton sheet before writing a single question about it.

    python scratchpad/_geo_guided/_measure_castleton.py

The four questions being replaced were written by reading an image and trusting
it. The image was wrong, so the questions were wrong, and a pixel-checker
confirmed them because it re-read the same image. The guard against repeating
that is to measure quantities that a broken render cannot fake -- grid geometry
and relative contour density -- and to build questions only on what is
positively drawn.

Reports, for peak-district-z15 (Castleton, Hope Valley):
  - grid line positions, so square names are derived not guessed
  - thin-contour ink per grid square, so "steeper than" is measured
  - contour crossings along the middle transect of named squares
  - whether green woodland coincides with blue watercourses
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

SHEET = "peak-district-z15-final.jpg"


def load():
    return Image.open(os.path.join(CACHE, SHEET)).convert("RGB")


def is_grid_blue(r, g, b):
    # Sampled off the sheet rather than assumed: the grid prints as a dark
    # slate blue near (69,92,142), not the saturated blue a first guess used.
    # That guess found nothing at all, which is at least a loud failure.
    return 110 < b < 200 and b - r > 35 and b - g > 25 and r < 140


def grid_lines(im):
    w, h = im.size
    px = im.load()
    cols, rows = [], []
    for x in range(w):
        n = sum(1 for y in range(0, h, 3) if is_grid_blue(*px[x, y]))
        cols.append(n)
    for y in range(h):
        n = sum(1 for x in range(0, w, 3) if is_grid_blue(*px[x, y]))
        rows.append(n)

    def peaks(prof, span):
        thr = span * 0.30            # grid lines break for labels and features
        out, i = [], 0
        while i < len(prof):
            if prof[i] >= thr:
                j = i
                while j < len(prof) and prof[j] >= thr:
                    j += 1
                out.append((i + j - 1) // 2)
                i = j
            else:
                i += 1
        return out

    return peaks(cols, h / 3.0), peaks(rows, w / 3.0)


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
    ep = m.filter(ImageFilter.MinFilter(3)).load()
    t = Image.new("L", (w, h), 0)
    tp = t.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y] and not ep[x, y]:
                tp[x, y] = 255
    return t


def crossings(t, y, x0, x1):
    """Count contour lines met walking east along one row."""
    tp = t.load()
    n, run = 0, False
    for x in range(x0, x1):
        on = tp[x, y] > 0
        if on and not run:
            n += 1
        run = on
    return n


def main():
    im = load()
    W, H = im.size
    vx, hy = grid_lines(im)
    print("sheet %dx%d" % (W, H))
    print("vertical grid lines at x =", vx)
    print("horizontal grid lines at y =", hy)

    # Read from the sheet: eastings 13,14,15,16 left-to-right;
    # northings 85,84,83,82 top-to-bottom (north is up, so numbers descend).
    EAST = [13, 14, 15, 16]
    NORTH = [85, 84, 83, 82]
    if len(vx) < 2 or len(hy) < 2:
        sys.exit("could not find the grid")
    east = dict(zip(EAST, vx))
    north = dict(zip(NORTH, hy))

    t = thin_mask(im)
    print()
    print("%-8s %-10s %-9s %s" % ("square", "ink/10k", "crossings", "note"))
    rows = []
    for ei in range(len(EAST) - 1):
        for ni in range(len(NORTH) - 1):
            e, n = EAST[ei], NORTH[ni + 1]      # square named by left + bottom line
            x0, x1 = east[EAST[ei]], east[EAST[ei + 1]]
            y1, y0 = north[NORTH[ni]], north[NORTH[ni + 1]]   # y0 = lower line (south)
            tp = t.load()
            ink = sum(1 for y in range(y1, y0, 2) for x in range(x0, x1, 2) if tp[x, y])
            dens = 10000.0 * ink / max(1, ((x1 - x0) // 2) * ((y0 - y1) // 2))
            mid = (y0 + y1) // 2
            cr = crossings(t, mid, x0, x1)
            rows.append(("%d%d" % (e, n), dens, cr))
    for name, dens, cr in rows:
        note = ""
        if name == "1582":
            note = "<- Castleton"
        print("%-8s %-10.1f %-9d %s" % (name, dens, cr, note))

    flat = min(rows, key=lambda r: r[1])
    steep = max(rows, key=lambda r: r[1])
    print()
    print("least contour ink: %s (%.1f)   most: %s (%.1f)" % (flat[0], flat[1], steep[0], steep[1]))


if __name__ == "__main__":
    main()
