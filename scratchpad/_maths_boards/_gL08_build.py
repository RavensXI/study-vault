# -*- coding: utf-8 -*-
import json, math

MINUS = "−"  # unicode minus for plain-text display

def s(n):
    """format a number for plain-text display using a unicode minus."""
    if isinstance(n, float) and n.is_integer():
        n = int(n)
    if n < 0:
        return MINUS + str(abs(n))
    return str(n)

def numify(n):
    if isinstance(n, float) and n.is_integer():
        return int(n)
    return n

# ---------------------------------------------------------------- figures
def tangent_svg(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    xlo, xhi = min(x1, x2), max(x1, x2)
    ylo, yhi = min(y1, y2, 0), max(y1, y2, 0)
    padx = (xhi - xlo) * 0.25 or 1
    pady = (yhi - ylo) * 0.20 or 1
    Xmin, Xmax = xlo - padx, xhi + padx
    Ymin, Ymax = ylo - pady * 0.6, yhi + pady
    PX0, PX1, PY0, PY1 = 42, 244, 18, 150
    def sx(x): return PX0 + (x - Xmin) / (Xmax - Xmin) * (PX1 - PX0)
    def sy(y): return PY1 - (y - Ymin) / (Ymax - Ymin) * (PY1 - PY0)
    Px1, Py1 = sx(x1), sy(y1)
    Px2, Py2 = sx(x2), sy(y2)
    Pmx, Pmy = (Px1 + Px2) / 2, (Py1 + Py2) / 2
    dx, dy = Px2 - Px1, Py2 - Py1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    if ny > 0:
        nx, ny = -nx, -ny
    Ls = min(L * 0.75, 62)
    R = (Ls * Ls) / 34.0
    pts = []
    steps = 14
    for i in range(steps + 1):
        ss = -Ls + (2 * Ls) * i / steps
        off = (ss * ss) / (2 * R)
        px = Pmx + ss * ux + off * nx
        py = Pmy + ss * uy + off * ny
        pts.append("%.1f,%.1f" % (px, py))
    curve = "M " + " L ".join(pts)
    # tangent line extended
    Ax, Ay = Px1 - 0.18 * dx, Py1 - 0.18 * dy
    Bx, By = Px2 + 0.18 * dx, Py2 + 0.18 * dy
    parts = []
    parts.append('<svg viewBox="0 0 260 176" role="img" aria-label="A curve with a tangent line through the two marked points and a gradient triangle" style="max-width:280px;width:100%;height:auto">')
    # frame axes
    parts.append('<line x1="42" y1="150" x2="248" y2="150" stroke="currentColor" stroke-width="1" opacity="0.55"/>')
    parts.append('<line x1="42" y1="12" x2="42" y2="150" stroke="currentColor" stroke-width="1" opacity="0.55"/>')
    parts.append('<text x="250" y="154" font-family="Inter,sans-serif" font-size="10" fill="currentColor">x</text>')
    parts.append('<text x="34" y="14" font-family="Inter,sans-serif" font-size="10" fill="currentColor">y</text>')
    # curve
    parts.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.45"/>' % curve)
    # gradient triangle
    Cx, Cy = Px2, Py1
    if rise != 0:
        parts.append('<path d="M %.1f,%.1f L %.1f,%.1f L %.1f,%.1f Z" fill="#60a5fa" fill-opacity="0.22" stroke="none"/>' % (Px1, Py1, Cx, Cy, Px2, Py2))
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" opacity="0.7"/>' % (Px1, Py1, Cx, Cy))
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" opacity="0.7"/>' % (Cx, Cy, Px2, Py2))
        # run label (under horizontal leg)
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">run %s</text>' % ((Px1 + Cx) / 2, Py1 + 13, s(run)))
        # rise label (beside vertical leg)
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor">rise %s</text>' % (Cx + 4, (Cy + Py2) / 2, s(rise)))
    else:
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">rise 0</text>' % (Pmx, Py1 - 6))
    # tangent line
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.6"/>' % (Ax, Ay, Bx, By))
    # points
    for (px, py, lx, ly, la) in ((Px1, Py1, x1, y1, "start"), (Px2, Py2, x2, y2, "end")):
        parts.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="currentColor"/>' % (px, py))
        tx = px + 5
        ty = py - 6 if la == "start" else py - 6
        anchor = "start"
        if px > 210:
            tx = px - 5; anchor = "end"
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="%s">(%s, %s)</text>' % (tx, ty, anchor, s(lx), s(ly)))
    parts.append('</svg>')
    return "".join(parts)

def trap_svg(heights, h):
    n = len(heights) - 1
    xs = [i * h for i in range(len(heights))]
    xmax = xs[-1]
    ymax = max(heights)
    Xmin, Xmax = 0, xmax
    Ymin, Ymax = 0, ymax * 1.12 or 1
    PX0, PX1, PY0, PY1 = 36, 246, 16, 148
    def sx(x): return PX0 + (x - Xmin) / (Xmax - Xmin) * (PX1 - PX0)
    def sy(y): return PY1 - (y - Ymin) / (Ymax - Ymin) * (PY1 - PY0)
    parts = []
    parts.append('<svg viewBox="0 0 260 174" role="img" aria-label="Area under a curve split into equal strips for the trapezium rule" style="max-width:280px;width:100%;height:auto">')
    # filled area (trapezoid tops)
    d = "M %.1f,%.1f" % (sx(xs[0]), sy(0))
    for x, y in zip(xs, heights):
        d += " L %.1f,%.1f" % (sx(x), sy(y))
    d += " L %.1f,%.1f Z" % (sx(xs[-1]), sy(0))
    parts.append('<path d="%s" fill="#60a5fa" fill-opacity="0.20" stroke="none"/>' % d)
    # strip dividers
    for x in xs:
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2" opacity="0.4"/>' % (sx(x), sy(0), sx(x), sy(0) - 3))
    # top polyline
    top = "M " + " L ".join("%.1f,%.1f" % (sx(x), sy(y)) for x, y in zip(xs, heights))
    parts.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.6"/>' % top)
    # axes
    parts.append('<line x1="36" y1="148" x2="248" y2="148" stroke="currentColor" stroke-width="1" opacity="0.6"/>')
    parts.append('<line x1="36" y1="10" x2="36" y2="148" stroke="currentColor" stroke-width="1" opacity="0.6"/>')
    parts.append('<text x="250" y="152" font-family="Inter,sans-serif" font-size="10" fill="currentColor">x</text>')
    parts.append('<text x="28" y="14" font-family="Inter,sans-serif" font-size="10" fill="currentColor">y</text>')
    # point dots + height labels
    for x, y in zip(xs, heights):
        parts.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="currentColor"/>' % (sx(x), sy(y)))
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (sx(x), sy(y) - 5, s(y)))
    # x tick labels
    for x in xs:
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle" opacity="0.8">%s</text>' % (sx(x), 160, s(x)))
    parts.append('</svg>')
    return "".join(parts)

def ramp_svg():
    # two right-triangle ramps: rise6/run3 and rise6/run2
    u = 11.0
    base = 104
    def tri(x0, run, rise, label):
        rx = run * u
        ry = rise * u
        p = []
        p.append('<path d="M %.1f,%.1f L %.1f,%.1f L %.1f,%.1f Z" fill="#60a5fa" fill-opacity="0.20" stroke="currentColor" stroke-width="1.4"/>' % (x0, base, x0 + rx, base, x0 + rx, base - ry))
        # right-angle square
        p.append('<path d="M %.1f,%.1f L %.1f,%.1f L %.1f,%.1f" fill="none" stroke="currentColor" stroke-width="1" opacity="0.7"/>' % (x0 + rx - 6, base, x0 + rx - 6, base - 6, x0 + rx, base - 6))
        p.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">run %d</text>' % (x0 + rx / 2, base + 14, run))
        p.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor">rise %d</text>' % (x0 + rx + 4, base - ry / 2, rise))
        p.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.85">%s</text>' % (x0 + rx / 2, base - ry - 6, label))
        return "".join(p)
    parts = ['<svg viewBox="0 0 260 132" role="img" aria-label="Two skateboard ramps, one gentle and one steeper, showing rise over run" style="max-width:280px;width:100%;height:auto">']
    parts.append(tri(18, 3, 6, "gentle"))
    parts.append(tri(150, 2, 6, "steeper"))
    parts.append('</svg>')
    return "".join(parts)

def trap_chart(heights, h):
    xs = [i * h for i in range(len(heights))]
    pts = [{"x": numify(x), "y": numify(y)} for x, y in zip(xs, heights)]
    ymax = max(heights)
    ytop = int(math.ceil(ymax * 1.15))
    return {
        "type": "line",
        "data": {"datasets": [{
            "data": pts, "fill": True,
            "backgroundColor": "rgba(96,165,250,0.25)",
            "borderColor": "#3b82f6", "tension": 0,
            "pointRadius": 4, "pointBackgroundColor": "#3b82f6"
        }]},
        "options": {
            "plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": 0, "max": numify(xs[-1]), "title": {"display": True, "text": "x"},
                      "ticks": {"stepSize": numify(h)}, "grid": {"color": "rgba(0,0,0,0.05)"}},
                "y": {"min": 0, "max": ytop, "title": {"display": True, "text": "y"},
                      "grid": {"color": "rgba(0,0,0,0.05)"}}
            }
        }
    }

# ---------------------------------------------------------------- walks
def tangent_steps(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    m = numify(rise / run)
    return [
        {"say": "Gradient of a tangent is rise ÷ run. Rise is the change in y, run is the change in x.",
         "pre": "rise = %s %s %s = " % (s(y2), MINUS, s(y1)), "post": "", "answer": numify(rise),
         "hint": "Take the first y from the second y."},
        {"pre": "run = %s %s %s = " % (s(x2), MINUS, s(x1)), "post": "", "answer": numify(run),
         "hint": "Take the first x from the second x."},
        {"say": "Now divide rise by run to get the gradient.", "phase": "substitute",
         "pre": "gradient = %s ÷ %s = " % (s(rise), s(run)), "post": "", "answer": m,
         "hint": "Rise divided by run."},
        {"pre": "check: run × gradient = %s × %s = " % (s(run), s(m)), "post": "", "answer": numify(rise),
         "done": "That matches the rise we found, so the gradient is correct.",
         "hint": "Multiply the run by your gradient; it should give the rise."}
    ]

def trap_steps(heights, h):
    y0, yn = heights[0], heights[-1]
    mids = heights[1:-1]
    ends = y0 + yn
    midsum = sum(mids)
    doubled = 2 * midsum
    bracket = ends + doubled
    area = numify((h / 2) * bracket)
    midexpr = " + ".join(s(v) for v in mids)
    hstr = s(numify(h))
    return [
        {"say": "Trapezium rule: A ≈ (h ÷ 2) × [first height + last height + 2 × (all the middle heights)].",
         "pre": "first + last = %s + %s = " % (s(y0), s(yn)), "post": "", "answer": numify(ends),
         "hint": "Add the two end heights."},
        {"pre": "middle heights: %s = " % midexpr, "post": "", "answer": numify(midsum),
         "hint": "Add all the in-between heights."},
        {"pre": "double the middles: 2 × %s = " % s(midsum), "post": "", "answer": numify(doubled),
         "hint": "Multiply the middle total by 2."},
        {"say": "Now add the ends total to the doubled middles, then multiply by h ÷ 2.", "phase": "substitute",
         "pre": "brackets: %s + %s = " % (s(ends), s(doubled)), "post": "", "answer": numify(bracket),
         "hint": "Add the ends total to the doubled middles."},
        {"pre": "area ≈ (%s ÷ 2) × %s = " % (hstr, s(bracket)), "post": "", "answer": area,
         "done": "That is the estimated area under the curve.",
         "hint": "Multiply the bracket by h ÷ 2."}
    ]

# sanity: final boxes land on solutions
def assert_tangent(x1, y1, x2, y2, sol):
    st = tangent_steps(x1, y1, x2, y2)
    assert st[2]["answer"] == sol, (x1, y1, x2, y2, st[2]["answer"], sol)

def assert_trap(heights, h, sol):
    st = trap_steps(heights, h)
    assert abs(st[-1]["answer"] - sol) < 1e-9, (heights, h, st[-1]["answer"], sol)

print("builder module loaded")
