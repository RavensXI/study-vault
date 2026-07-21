# -*- coding: utf-8 -*-
"""Grid geometry for any OS sheet: references, distances and bearings from pixels.

    python scratchpad/_geo_guided/_grid_ref.py <sheet> <firstEasting> <firstNorthing>
    python scratchpad/_geo_guided/_grid_ref.py clitheroe-z16-final.jpg 68 42

Prints the detected grid, the px/km needed for ruler calibration, and then reads
any "x,y" pairs from stdin, reporting the four- and six-figure reference of each
and the distance and bearing between consecutive pairs.

The point is to stop answers being estimated by eye. A feature's position comes
from looking at the map; everything derived from it -- which square it is in,
how far it is from another feature, what direction -- is arithmetic, and
arithmetic is what got skipped when questions were written around a broken
render. Grid references are properties of the ground, not of the sheet, so a
reference verified here stays true on any map covering the same area.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_mapcache")
CROP = os.path.join(HERE, "_cropped")

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from PIL import Image

POINTS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def is_grid_blue(r, g, b):
    return 110 < b < 200 and b - r > 35 and b - g > 25 and r < 140


def find_grid(im):
    w, h = im.size
    px = im.load()
    def peaks(prof, span):
        thr = span * 0.30
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
    cols = [sum(1 for y in range(0, h, 3) if is_grid_blue(*px[x, y])) for x in range(w)]
    rows = [sum(1 for x in range(0, w, 3) if is_grid_blue(*px[x, y])) for y in range(h)]
    return peaks(cols, h / 3.0), peaks(rows, w / 3.0)


def load(name):
    for d in (CACHE, CROP):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    sys.exit("sheet not found: %s" % name)


class Sheet(object):
    def __init__(self, name, e0, n0):
        im = load(name)
        self.name = name
        self.W, self.H = im.size
        vx, hy = find_grid(im)
        if len(vx) < 2 or len(hy) < 2:
            sys.exit("grid not found on %s" % name)
        self.vx, self.hy = vx, hy
        self.e0, self.n0 = e0, n0
        self.pxkm_x = (vx[-1] - vx[0]) / float(len(vx) - 1)
        self.pxkm_y = (hy[-1] - hy[0]) / float(len(hy) - 1)

    def easting(self, x):
        """Fractional easting at pixel x (increases to the right)."""
        return self.e0 + (x - self.vx[0]) / self.pxkm_x

    def northing(self, y):
        """Fractional northing at pixel y (increases upwards, so y falls)."""
        return self.n0 - (y - self.hy[0]) / self.pxkm_y

    def ref4(self, x, y):
        return "%02d%02d" % (int(math.floor(self.easting(x))) % 100,
                             int(math.floor(self.northing(y))) % 100)

    def ref6(self, x, y):
        e, n = self.easting(x), self.northing(y)
        return "%02d%d%02d%d" % (int(math.floor(e)) % 100, int((e % 1) * 10),
                                 int(math.floor(n)) % 100, int((n % 1) * 10))

    def between(self, a, b):
        dx = (self.easting(b[0]) - self.easting(a[0]))
        dy = (self.northing(b[1]) - self.northing(a[1]))
        dist = math.hypot(dx, dy)
        brg = (math.degrees(math.atan2(dx, dy)) + 360) % 360
        idx = int((brg + 22.5) // 45) % 8
        edge = min(abs((brg + 22.5) % 45 - 0), 45 - ((brg + 22.5) % 45))
        return dist, brg, POINTS[idx], edge

    def describe(self):
        print("%s  %dx%d" % (self.name, self.W, self.H))
        print("  vertical lines x=%s   -> eastings %s" %
              (self.vx, [self.e0 + i for i in range(len(self.vx))]))
        print("  horizontal lines y=%s -> northings %s" %
              (self.hy, [self.n0 - i for i in range(len(self.hy))]))
        print("  px per km: x=%.1f y=%.1f  (ruler pxPerKm -> %d)"
              % (self.pxkm_x, self.pxkm_y, round((self.pxkm_x + self.pxkm_y) / 2)))


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    s = Sheet(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    s.describe()
    pts = []
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", " ").split()
        x, y = int(parts[0]), int(parts[1])
        label = " ".join(parts[2:]) or "?"
        print("  %-26s (%4d,%4d)  4fig=%s  6fig=%s"
              % (label, x, y, s.ref4(x, y), s.ref6(x, y)))
        pts.append(((x, y), label))
    for i in range(len(pts) - 1):
        (a, la), (b, lb) = pts[i], pts[i + 1]
        d, brg, pt, edge = s.between(a, b)
        flag = "  <-- near sector edge, avoid" if edge < 8 else ""
        print("  %s -> %s: %.2f km, bearing %.0f deg, %s%s" % (la, lb, d, brg, pt, flag))


if __name__ == "__main__":
    main()
