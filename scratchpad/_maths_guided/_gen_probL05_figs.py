# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for probability-statistics-L05 and splice
them into the fresh live practice_data. Figures are built from each problem's
own numbers. Only display strings that already CLAIM a figure but lack one get
an SVG prepended; nothing else is touched."""
import json, io

LEFT, RIGHT, TOP, BOTTOM = 40, 244, 20, 145
VB = 'viewBox="0 0 260 175" role="img"'
SVGOPEN = '<svg %s aria-label="%s" style="max-width:100%%;height:auto">'

def fmtnum(v):
    return ("%g" % v)

def hist_svg(bars, xmin, xmax, fdtop, yticks, xlabels, aria, colors, slice_x=None):
    """bars: list of (lo, hi, fd). xlabels: list of boundary values to print."""
    def X(v): return LEFT + (v - xmin) / (xmax - xmin) * (RIGHT - LEFT)
    def Y(fd): return BOTTOM - fd / fdtop * (BOTTOM - TOP)
    s = ['<svg %s aria-label="%s" style="max-width:100%%;height:auto">' % (VB, aria)]
    s.append('<style>text{font-family:Inter,system-ui,sans-serif;fill:currentColor}</style>')
    # bars
    for i, (lo, hi, fd) in enumerate(bars):
        c = colors[i % len(colors)]
        x, w, y = X(lo), X(hi) - X(lo), Y(fd)
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>' % (x, y, w, BOTTOM - y, c))
    # optional slice divider (dashed)
    if slice_x is not None:
        sx = X(slice_x)
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>' % (sx, TOP, sx, BOTTOM))
        s.append('<text x="%.1f" y="%.0f" font-size="9" text-anchor="middle">%s</text>' % (sx, BOTTOM + 13, fmtnum(slice_x)))
    # axes
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (LEFT, BOTTOM, RIGHT, BOTTOM))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (LEFT, TOP, LEFT, BOTTOM))
    # y ticks
    for t in yticks:
        y = Y(t)
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (LEFT - 4, y, LEFT, y))
        s.append('<text x="%d" y="%.1f" font-size="9" text-anchor="end">%s</text>' % (LEFT - 6, y + 3, fmtnum(t)))
    # x boundary labels
    for b in xlabels:
        x = X(b)
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x, BOTTOM, x, BOTTOM + 4))
        s.append('<text x="%.1f" y="%d" font-size="9" text-anchor="middle">%s</text>' % (x, BOTTOM + 13, fmtnum(b)))
    # titles
    s.append('<text x="12" y="%d" font-size="9" text-anchor="middle" transform="rotate(-90 12 %d)">Frequency density</text>' % ((TOP + BOTTOM) // 2, (TOP + BOTTOM) // 2))
    s.append('<text x="%d" y="172" font-size="9" text-anchor="middle">%s</text>' % ((LEFT + RIGHT) // 2, aria_xtitle[0]))
    s.append('</svg>')
    return "".join(s)

def cf_svg(points, xmin, xmax, nmax, xticks, yticks, marks, aria, xtitle, color):
    """points: list of (mark, cf). marks: read-off dots (mark,cf)."""
    def X(v): return LEFT + (v - xmin) / (xmax - xmin) * (RIGHT - LEFT)
    def Y(cf): return BOTTOM - cf / nmax * (BOTTOM - TOP)
    s = ['<svg %s aria-label="%s" style="max-width:100%%;height:auto">' % (VB, aria)]
    s.append('<style>text{font-family:Inter,system-ui,sans-serif;fill:currentColor}</style>')
    # curve
    pts = " ".join("%.1f,%.1f" % (X(m), Y(c)) for m, c in points)
    s.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (pts, color))
    # read-off dots
    for m, c in marks:
        s.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (X(m), Y(c), color))
    # axes
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (LEFT, BOTTOM, RIGHT, BOTTOM))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (LEFT, TOP, LEFT, BOTTOM))
    for t in yticks:
        y = Y(t)
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (LEFT - 4, y, LEFT, y))
        s.append('<text x="%d" y="%.1f" font-size="9" text-anchor="end">%s</text>' % (LEFT - 6, y + 3, fmtnum(t)))
    for t in xticks:
        x = X(t)
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x, BOTTOM, x, BOTTOM + 4))
        s.append('<text x="%.1f" y="%d" font-size="9" text-anchor="middle">%s</text>' % (x, BOTTOM + 13, fmtnum(t)))
    s.append('<text x="12" y="%d" font-size="9" text-anchor="middle" transform="rotate(-90 12 %d)">Cumulative frequency</text>' % ((TOP + BOTTOM) // 2, (TOP + BOTTOM) // 2))
    s.append('<text x="%d" y="172" font-size="9" text-anchor="middle">%s</text>' % ((LEFT + RIGHT) // 2, xtitle))
    s.append('</svg>')
    return "".join(s)

COL = ["#3b82f6", "#8b5cf6", "#f59e0b", "#34d399", "#ef4444"]

# ---- Build the figures ----
aria_xtitle = ["Waiting time (minutes)"]
silver1 = hist_svg([(0, 10, 2), (10, 20, 5), (20, 50, 3)], 0, 50, 6,
                   [0, 2, 4, 6], [0, 10, 20, 50],
                   "Histogram: bars 0 to 10 frequency density 2, 10 to 20 frequency density 5, 20 to 50 frequency density 3",
                   COL)

aria_xtitle = ["Value"]
silver1 = silver1  # xtitle set via aria_xtitle at build time; fix below

# rebuild with proper x titles per figure using a wrapper
def hist(bars, xmin, xmax, fdtop, yticks, xlabels, aria, xtitle, colors, slice_x=None):
    global aria_xtitle
    aria_xtitle = [xtitle]
    return hist_svg(bars, xmin, xmax, fdtop, yticks, xlabels, aria, colors, slice_x)

svg_silver1 = hist([(0, 10, 2), (10, 20, 5), (20, 50, 3)], 0, 50, 6,
                   [0, 2, 4, 6], [0, 10, 20, 50],
                   "Histogram with bars 0 to 10 at frequency density 2, 10 to 20 at frequency density 5, and 20 to 50 at frequency density 3",
                   "Value", COL)

svg_teach_silver = hist([(0, 10, 3), (10, 30, 4), (30, 40, 2)], 0, 40, 5,
                        [0, 2, 4], [0, 10, 30, 40],
                        "Histogram with bars 0 to 10 at frequency density 3, 10 to 30 at frequency density 4, and 30 to 40 at frequency density 2",
                        "Waiting time (minutes)", COL)

svg_teach_gold = hist([(200, 300, 0.6)], 200, 300, 0.8,
                      [0, 0.2, 0.4, 0.6, 0.8], [200, 300],
                      "Histogram with one bar from 200 to 300 thousand pounds at frequency density 0.6, dashed line marking 250",
                      "House price (thousand pounds)", ["#3b82f6"], slice_x=250)

svg_teach_bronze = cf_svg([(20, 0), (30, 5), (40, 15), (52, 30), (64, 45), (72, 55), (80, 60)],
                          20, 80, 60, [20, 40, 60, 80], [0, 15, 30, 45, 60],
                          [(40, 15), (52, 30), (64, 45)],
                          "Cumulative frequency curve for 60 students passing through mark 40 at 15, mark 52 at 30, and mark 64 at 45",
                          "Mark", "#3b82f6")

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---- Splice into fresh data ----
pd = json.load(io.open("_probL05_fresh_live.json", encoding="utf-8"))

# silver[1] bank problem
sp = pd["problem_bank"]["silver"][1]
assert "0-10 (fd=2), 10-20 (fd=5), 20-50 (fd=3)" in sp["display"], sp["display"]
sp["display"] = svg_silver1 + CAP + sp["display"]

# teach walks
tb = pd["guided"]["teach"]["bronze"]
assert tb["display"].startswith("A cumulative frequency graph shows the marks of 60"), tb["display"][:40]
tb["display"] = svg_teach_bronze + tb["display"]

ts = pd["guided"]["teach"]["silver"]
assert ts["display"].startswith("A histogram of waiting times"), ts["display"][:40]
ts["display"] = svg_teach_silver + ts["display"]

tg = pd["guided"]["teach"]["gold"]
assert tg["display"].startswith("A histogram shows house prices"), tg["display"][:40]
tg["display"] = svg_teach_gold + CAP + tg["display"]

json.dump(pd, io.open("lesson_probability-statistics-L05_diagrams.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# quick size report
for name, s in [("silver1", svg_silver1), ("teach_bronze", svg_teach_bronze),
                ("teach_silver", svg_teach_silver), ("teach_gold", svg_teach_gold)]:
    print(name, len(s), "chars")
print("written.")
