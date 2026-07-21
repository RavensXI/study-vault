# -*- coding: utf-8 -*-
"""Where on each sheet do the contours actually exist?

    python scratchpad/_geo_guided/_map_contour_map.py

The first audit counted brown-ish pixels over the whole sheet and called it a
score. That was wrong twice over. Orange A-roads sit in the same hue band, so
Dorset scored 16.7 "sparse" while having no contours at all -- the score was
measuring the A351. And a single total cannot see Tom's actual complaint, which
is contours that stop part way across a sheet.

So: reject thick features, then report coverage per cell of a 6x6 grid.

Thickness is the discriminator that hue alone cannot give. An OS contour is a
1-2 px hairline; an A-road casing is 5+ px of solid fill. Eroding the brown mask
by a 3x3 kernel deletes hairlines entirely and leaves roads behind, so
(mask - eroded) isolates the thin ink. No third-party CV needed.

Verdicts:
  none     -- no usable contour ink anywhere
  cut off  -- present in some cells, absent in others (Tom's complaint)
  ok       -- present across the sheet
"""
import io, os, sys, urllib.request

R2 = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_mapcache")
GRID = 6

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("Pillow needed: python -m pip install pillow")


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        req = urllib.request.Request(R2 + name, headers={"User-Agent": "Mozilla/5.0 StudyVault-audit"})
        with urllib.request.urlopen(req, timeout=180) as r, io.open(p, "wb") as f:
            f.write(r.read())
    return p


def thin_brown_mask(im):
    """1 where a thin brown line sits, 0 elsewhere (roads removed)."""
    w, h = im.size
    px = im.load()
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            # OS contour ink: brown, red clearly ahead of blue, mid tone.
            # Deliberately wider than the final answer -- erosion does the
            # discriminating, this only has to not miss real contours.
            if r > 110 and r - b > 30 and 15 < r - g < 95 and g >= b and r < 240:
                mp[x, y] = 255
    # MinFilter(3) = erosion. A 1-2 px line has a non-brown neighbour in every
    # 3x3 window, so it erodes to nothing; a thick road core survives.
    eroded = mask.filter(ImageFilter.MinFilter(3))
    thin = Image.new("L", (w, h), 0)
    tp, ep = thin.load(), eroded.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y] and not ep[x, y]:
                tp[x, y] = 255
    return thin


def analyse(path):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    # downsample enough for speed, not so far that hairlines vanish
    scale = 900.0 / W
    im = im.resize((900, max(1, int(H * scale))))
    # drop the attribution strip so its text is not counted
    w, h = im.size
    im = im.crop((0, 0, w, int(h * 0.975)))
    thin = thin_brown_mask(im)
    w, h = thin.size
    tp = thin.load()
    cells, cw, ch = [], w // GRID, h // GRID
    for cy in range(GRID):
        row = []
        for cx in range(GRID):
            n = 0
            for y in range(cy * ch, (cy + 1) * ch):
                for x in range(cx * cw, (cx + 1) * cw):
                    if tp[x, y]:
                        n += 1
            row.append(round(10000.0 * n / (cw * ch), 1))
        cells.append(row)
    return W, H, cells


def verdict(cells):
    flat = [v for row in cells for v in row]
    live = [v for v in flat if v >= 8]           # a cell with real contour ink
    if len(live) <= 2:
        return "none", 0
    empty = sum(1 for v in flat if v < 3)        # a cell with essentially none
    pct = 100.0 * len(live) / len(flat)
    if empty >= len(flat) * 0.25:
        return "CUT OFF", pct
    return "ok", pct


def main():
    names = sorted(n for n in os.listdir(CACHE) if n.endswith((".jpg", ".png"))) if os.path.isdir(CACHE) else []
    if not names:
        sys.exit("no cached maps; run _audit_map_contours.py first to populate the cache")
    rows = []
    for n in names:
        W, H, cells = analyse(fetch(n))
        v, pct = verdict(cells)
        rows.append((n, W, H, cells, v, pct))
    order = {"none": 0, "CUT OFF": 1, "ok": 2}
    for n, W, H, cells, v, pct in sorted(rows, key=lambda r: (order[r[4]], -r[5])):
        print("%-34s %-9s cells-with-contours=%3d%%" % (n, v, round(pct)))
        if v != "ok":
            for row in cells:
                print("      " + " ".join(("%6.1f" % c) if c >= 3 else "     ." for c in row))
    print()
    for v in ("none", "CUT OFF", "ok"):
        got = [r[0] for r in rows if r[4] == v]
        print("%-8s %d" % (v, len(got)))


if __name__ == "__main__":
    main()
