# -*- coding: utf-8 -*-
"""Generate coordinate-grid SVG figures for geometry-L04 (Transformations)
programmatically from each problem's own numbers, then inject at the start of
the relevant display fields. THE FIGURE MUST MATCH THE NUMBERS: we only ever
plot points/lines/centres that are GIVEN in the problem text, never the answer.
"""
import json, io

CELL = 18
ML, MB, MT, MR = 16, 14, 9, 9

def fmt(n):
    return str(int(n)) if float(n) == int(n) else str(n)

def build(points=None, segment=None, polygon=None, poly_label=None,
          mirror=None, centre=None, mark_origin=False, aria=""):
    points = points or []
    # bounds from every GIVEN element (never the answer)
    xs, ys = [0.0], [0.0]
    for (x, y, *_r) in points:
        xs.append(x); ys.append(y)
    if segment:
        for (x, y) in segment:
            xs.append(x); ys.append(y)
    if polygon:
        for (x, y) in polygon:
            xs.append(x); ys.append(y)
    if centre:
        xs.append(centre[0]); ys.append(centre[1])
    if mirror and mirror["type"] == "vert":
        xs.append(mirror["k"])
    xmin = int(min(xs)) - 1
    xmax = int(max(xs)) + 1
    ymin = int(min(ys)) - 1
    ymax = int(max(ys)) + 1
    if mirror and mirror["type"] == "vert":
        xmax = max(xmax, int(mirror["k"]) + 2)
    W = ML + (xmax - xmin) * CELL + MR
    H = MT + (ymax - ymin) * CELL + MB

    def sx(x):
        return round(ML + (x - xmin) * CELL, 1)
    def sy(y):
        return round(H - MB - (y - ymin) * CELL, 1)

    out = []
    out.append(
        '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
        'style="max-width:280px;width:100%%;height:auto;font-family:Inter,sans-serif">'
        % (W, H, aria))
    # gridlines
    g = []
    for x in range(xmin, xmax + 1):
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(x), sy(ymin), sx(x), sy(ymax)))
    for y in range(ymin, ymax + 1):
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(xmin), sy(y), sx(xmax), sy(y)))
    out.append('<g stroke="currentColor" stroke-opacity="0.15" stroke-width="0.5">' + "".join(g) + '</g>')
    # axes
    ax = []
    if ymin <= 0 <= ymax:
        ax.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(xmin), sy(0), sx(xmax), sy(0)))
    if xmin <= 0 <= xmax:
        ax.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(0), sy(ymin), sx(0), sy(ymax)))
    out.append('<g stroke="currentColor" stroke-opacity="0.5" stroke-width="1">' + "".join(ax) + '</g>')
    # axis tick numbers (small)
    tn = []
    for x in range(xmin, xmax + 1):
        if x == 0:
            continue
        tn.append('<text x="%s" y="%s" text-anchor="middle">%d</text>' % (sx(x), sy(0) + 7, x))
    for y in range(ymin, ymax + 1):
        if y == 0:
            continue
        tn.append('<text x="%s" y="%s" text-anchor="end">%d</text>' % (sx(0) - 2.5, sy(y) + 2.5, y))
    tn.append('<text x="%s" y="%s" text-anchor="end">O</text>' % (sx(0) - 2.5, sy(0) + 7.5))
    out.append('<g fill="currentColor" fill-opacity="0.6" font-size="6.5">' + "".join(tn) + '</g>')

    # mirror line (amber, exam mirror convention)
    if mirror:
        t = mirror["type"]
        if t == "xaxis":
            ln = '<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(xmin), sy(0), sx(xmax), sy(0))
            lx, ly, anc = sx(xmax) - 2, sy(0) - 3, "end"
        elif t == "yaxis":
            ln = '<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(0), sy(ymin), sx(0), sy(ymax))
            lx, ly, anc = sx(0) + 3, sy(ymax) + 8, "start"
        elif t == "yeqx":
            lo = max(xmin, ymin); hi = min(xmax, ymax)
            ln = '<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(lo), sy(lo), sx(hi), sy(hi))
            lx, ly, anc = sx(hi) - 1, sy(hi) - 3, "end"
        elif t == "vert":
            k = mirror["k"]
            ln = '<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (sx(k), sy(ymin), sx(k), sy(ymax))
            lx, ly, anc = sx(k) + 3, sy(ymax) + 8, "start"
        out.append('<g stroke="#f59e0b" stroke-width="1.6" stroke-dasharray="4 2">' + ln + '</g>')
        out.append('<text x="%s" y="%s" text-anchor="%s" fill="currentColor" font-size="9" font-style="italic">%s</text>'
                   % (lx, ly, anc, mirror["label"]))

    # polygon (triangle etc.)
    if polygon:
        pts = " ".join("%s,%s" % (sx(x), sy(y)) for (x, y) in polygon)
        out.append('<polygon points="%s" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>' % pts)
        if poly_label:
            cx = sum(sx(x) for (x, y) in polygon) / len(polygon)
            cy = sum(sy(y) for (x, y) in polygon) / len(polygon)
            out.append('<text x="%s" y="%s" text-anchor="middle" fill="currentColor" font-size="8.5">%s</text>'
                       % (round(cx, 1), round(cy, 1), poly_label))

    # segment
    if segment:
        (x1, y1), (x2, y2) = segment
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#3b82f6" stroke-width="1.6"/>'
                   % (sx(x1), sy(y1), sx(x2), sy(y2)))

    # centre of enlargement (amber cross)
    if centre:
        cx, cy, clab = centre
        px, py = sx(cx), sy(cy)
        out.append('<g stroke="#f59e0b" stroke-width="1.6">'
                   '<line x1="%s" y1="%s" x2="%s" y2="%s"/>'
                   '<line x1="%s" y1="%s" x2="%s" y2="%s"/></g>'
                   % (px - 3.5, py - 3.5, px + 3.5, py + 3.5, px - 3.5, py + 3.5, px + 3.5, py - 3.5))
        out.append('<text x="%s" y="%s" text-anchor="middle" fill="currentColor" font-size="8.5">%s</text>'
                   % (px, py + 13, clab))

    # points
    for (x, y, *rest) in points:
        lab = rest[0] if rest else "(%s, %s)" % (fmt(x), fmt(y))
        px, py = sx(x), sy(y)
        out.append('<circle cx="%s" cy="%s" r="3.4" fill="#3b82f6"/>' % (px, py))
        if lab == "":
            continue
        # label placement: default upper-right; flip if near an edge
        dx, dy, anc = 6, -5, "start"
        if x >= xmax - 1:
            dx, anc = -6, "end"
        if y >= ymax - 1:
            dy = 12
        out.append('<text x="%s" y="%s" text-anchor="%s" fill="currentColor" font-size="10">%s</text>'
                   % (round(px + dx, 1), round(py + dy, 1), anc, lab))

    out.append('</svg>')
    return "".join(out)


# --- figure specifications: only GIVEN quantities plotted ---
FIGS = {}

# Opener: counter on games board at (2,1)
FIGS[("opener",)] = build(
    points=[(2, 1, "counter")],
    aria="Coordinate grid, a counter on square (2, 1) ready to slide 3 right and 2 up.")

# Teach walks
FIGS[("teach", "bronze")] = build(
    points=[(1, 2, "A"), (3, 2, "B")], segment=[(1, 2), (3, 2)],
    aria="Coordinate grid with segment from A(1, 2) to B(3, 2) to be translated by vector 2 right 4 up.")
FIGS[("teach", "silver")] = build(
    points=[(4, 1, "P"), (4, 3, "Q")], mark_origin=True,
    aria="Coordinate grid with points P(4, 1) and Q(4, 3), to be rotated 90 degrees clockwise about the origin.")
FIGS[("teach", "gold")] = build(
    points=[(5, 4)], centre=(1, 1, "centre (1, 1)"),
    aria="Coordinate grid with point (5, 4) and centre of enlargement (1, 1), scale factor 2.")

# Bronze bank
FIGS[("bank", "bronze", 0)] = build(
    points=[(4, 2)],
    aria="Coordinate grid with point (4, 2) to be translated by vector 3 right, 1 down.")
FIGS[("bank", "bronze", 1)] = build(
    points=[(5, 3)], mirror={"type": "xaxis", "label": "mirror"},
    aria="Coordinate grid with point (5, 3), to be reflected in the x-axis.")
FIGS[("bank", "bronze", 2)] = build(
    points=[(3, 7)], mirror={"type": "yaxis", "label": "mirror"},
    aria="Coordinate grid with point (3, 7), to be reflected in the y-axis.")
FIGS[("bank", "bronze", 3)] = build(
    points=[(2, 5)], mark_origin=True,
    aria="Coordinate grid with point (2, 5), to be rotated 180 degrees about the origin.")
FIGS[("bank", "bronze", 4)] = build(
    points=[(2, 4)], centre=(0, 0, ""),
    aria="Coordinate grid with point (2, 4), to be enlarged by scale factor 3 from the origin.")
FIGS[("bank", "bronze", 7)] = build(
    points=[(1, 6)],
    aria="Coordinate grid with point (1, 6) to be translated by vector 5 right, 3 down.")

# Silver bank
FIGS[("bank", "silver", 0)] = build(
    points=[(4, 1)], mirror={"type": "yeqx", "label": "y = x"},
    aria="Coordinate grid with point (4, 1) and the mirror line y = x.")
FIGS[("bank", "silver", 1)] = build(
    points=[(3, 2)], mark_origin=True,
    aria="Coordinate grid with point (3, 2), to be rotated 90 degrees clockwise about the origin.")
FIGS[("bank", "silver", 2)] = build(
    points=[(8, 6)], centre=(0, 0, ""),
    aria="Coordinate grid with point (8, 6), to be enlarged by scale factor one half from the origin.")
FIGS[("bank", "silver", 3)] = build(
    points=[(1, 3, "A"), (5, 1, "A′")],
    aria="Coordinate grid showing A(1, 3) mapping to A prime (5, 1); find the translation vector.")
FIGS[("bank", "silver", 4)] = build(
    polygon=[(2, 1), (4, 1), (2, 4)], poly_label="area 3",
    points=[(2, 1, ""), (4, 1, ""), (2, 4, "")],
    aria="Coordinate grid with triangle at (2,1), (4,1), (2,4) of area 3, to be enlarged by scale factor 2.")
FIGS[("bank", "silver", 5)] = build(
    points=[(5, 2)], mark_origin=True,
    aria="Coordinate grid with point (5, 2), to be rotated 90 degrees anticlockwise about the origin.")
FIGS[("bank", "silver", 6)] = build(
    points=[(-3, 4)], mirror={"type": "vert", "k": 1, "label": "x = 1"},
    aria="Coordinate grid with point (minus 3, 4) and the mirror line x = 1.")

# Gold bank
FIGS[("bank", "gold", 0)] = build(
    points=[(3, 2)], centre=(1, 1, "centre (1, 1)"),
    aria="Coordinate grid with point (3, 2) and centre of enlargement (1, 1), scale factor minus 2.")
FIGS[("bank", "gold", 1)] = build(
    points=[(2, 5, "(2, 5)"), (5, 2, "(5, 2)")],
    aria="Coordinate grid showing (2, 5) and (5, 2); describe the single transformation between them.")
FIGS[("bank", "gold", 4)] = build(
    points=[(5, 7)], centre=(2, 3, "centre (2, 3)"),
    aria="Coordinate grid with point (5, 7) and centre of enlargement (2, 3), scale factor minus 1.")

# --- inject ---
pd = json.load(io.open("_gL04_live_diag.json", encoding="utf-8"))

def prepend(display, svg):
    return svg + display

count = 0
sizes = []
for loc, svg in FIGS.items():
    sizes.append((loc, len(svg)))
    if loc[0] == "opener":
        pd["guided"]["opener"]["display"] = prepend(pd["guided"]["opener"]["display"], svg)
    elif loc[0] == "teach":
        t = loc[1]
        pd["guided"]["teach"][t]["display"] = prepend(pd["guided"]["teach"][t]["display"], svg)
    elif loc[0] == "bank":
        _, tier, idx = loc
        pd["problem_bank"][tier][idx]["display"] = prepend(pd["problem_bank"][tier][idx]["display"], svg)
    count += 1

json.dump(pd, io.open("lesson_geometry-L04_diagrams.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("figures injected:", count)
print("max svg bytes:", max(s for _, s in sizes))
for loc, s in sizes:
    if s > 3000:
        print("  LARGE", loc, s)
