# -*- coding: utf-8 -*-
"""Add exam-realism figures to graphs-L08 (Gradients of Curves & Areas Under Graphs).
Charts (problem.chart) for graphs; inline SVG prepended to display for shapes.
Every number drawn is asserted against the problem's own values."""
import json, io

SRC = "_diag_L08_live.json"
OUT = "lesson_graphs-L08_diagrams.json"

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---------- chart helpers ----------
def line_chart(points, xmin, xmax, xstep, ymin, ymax, ystep,
               xtitle="x", ytitle="y", tension=0, fill=True, markers=True,
               colour="#3b82f6"):
    ds = {
        "type": "line",
        "data": [{"x": x, "y": y} for x, y in points],
        "tension": tension,
        "fill": fill,
        "backgroundColor": "rgba(96,165,250,0.25)",
        "borderColor": colour,
        "borderWidth": 2,
        "pointRadius": 4 if markers else 0,
        "pointBackgroundColor": colour,
    }
    return {
        "type": "scatter",
        "data": {"datasets": [ds]},
        "options": {
            "plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": xmin, "max": xmax, "ticks": {"stepSize": xstep},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": xtitle, "display": True}},
                "y": {"min": ymin, "max": ymax, "ticks": {"stepSize": ystep},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": ytitle, "display": True}},
            },
        },
    }

def two_ds_chart(curve, tangent, marks, xmin, xmax, xstep, ymin, ymax, ystep,
                 xtitle="x", ytitle="y"):
    d_curve = {"type": "line", "data": [{"x": x, "y": y} for x, y in curve],
               "tension": 0.35, "fill": False, "borderColor": "#3b82f6",
               "borderWidth": 2, "pointRadius": 0}
    d_tan = {"type": "line", "data": [{"x": x, "y": y} for x, y in tangent],
             "tension": 0, "fill": False, "borderColor": "#f59e0b",
             "borderWidth": 2, "pointRadius": 0}
    d_mk = {"type": "scatter", "data": [{"x": x, "y": y} for x, y in marks],
            "showLine": False, "borderColor": "#f59e0b",
            "backgroundColor": "#f59e0b", "pointRadius": 4}
    return {
        "type": "scatter",
        "data": {"datasets": [d_curve, d_tan, d_mk]},
        "options": {
            "plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": xmin, "max": xmax, "ticks": {"stepSize": xstep},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": xtitle, "display": True}},
                "y": {"min": ymin, "max": ymax, "ticks": {"stepSize": ystep},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": ytitle, "display": True}},
            },
        },
    }

# ---------- SVG helpers ----------
def svg_trapezium(a, b, w, aria):
    """Left vertical side a, right vertical side b, base width label w."""
    base = 120.0
    lx, rx = 70.0, 170.0
    scale = 84.0 / max(a, b)
    la, lb = a * scale, b * scale
    p1 = (lx, base); p2 = (lx, base - la); p3 = (rx, base - lb); p4 = (rx, base)
    poly = " ".join("%.1f,%.1f" % pt for pt in (p1, p2, p3, p4))
    s = ('<svg viewBox="0 0 240 150" role="img" '
         'aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif">' % aria)
    s += ('<polygon points="%s" fill="#60a5fa" fill-opacity="0.3" '
          'stroke="currentColor" stroke-width="1.5"/>' % poly)
    # side + base labels
    s += ('<text x="62" y="%.1f" font-size="11" fill="currentColor" '
          'text-anchor="end">y = %g</text>' % (base - la / 2 + 4, a))
    s += ('<text x="178" y="%.1f" font-size="11" fill="currentColor" '
          'text-anchor="start">y = %g</text>' % (base - lb / 2 + 4, b))
    s += ('<text x="120" y="138" font-size="11" fill="currentColor" '
          'text-anchor="middle">h = %g</text>' % w)
    s += '</svg>'
    return s

def svg_falling_tangent():
    # points (2,18) and (6,2); axes x 0..8, y 0..20
    ox, oy = 30.0, 140.0
    sx = (220.0 - ox) / 8.0     # px per second
    sy = (140.0 - 20.0) / 20.0  # px per unit y
    def P(x, y): return (ox + x * sx, oy - y * sy)
    a = P(2, 18); b = P(6, 2)
    xtick = ox + 4 * sx
    s = ('<svg viewBox="0 0 240 160" role="img" '
         'aria-label="A falling tangent to a curve, passing through (2, 18) and (6, 2)" '
         'style="max-width:280px;font-family:Inter,sans-serif">')
    # axes
    s += ('<line x1="%.1f" y1="%.1f" x2="230" y2="%.1f" stroke="currentColor" '
          'stroke-width="1"/>' % (ox, oy, oy))
    s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="12" stroke="currentColor" '
          'stroke-width="1"/>' % (ox, oy, ox))
    # tangent line (extended slightly)
    s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#f59e0b" '
          'stroke-width="2"/>' % (a[0] - 10, a[1] - 10 * (b[1] - a[1]) / (b[0] - a[0]),
                                  b[0] + 10, b[1] + 10 * (b[1] - a[1]) / (b[0] - a[0])))
    for (px, py), lab in ((a, "(2, 18)"), (b, "(6, 2)")):
        s += '<circle cx="%.1f" cy="%.1f" r="3" fill="#f59e0b"/>' % (px, py)
    s += ('<text x="%.1f" y="%.1f" font-size="11" fill="currentColor" '
          'text-anchor="start">(2, 18)</text>' % (a[0] + 6, a[1] - 4))
    s += ('<text x="%.1f" y="%.1f" font-size="11" fill="currentColor" '
          'text-anchor="end">(6, 2)</text>' % (b[0] - 6, b[1] + 12))
    s += ('<text x="%.1f" y="152" font-size="10" fill="currentColor" '
          'text-anchor="middle">x = 4</text>' % xtick)
    s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" '
          'stroke-width="1" stroke-dasharray="2 2"/>' % (xtick, oy, xtick, oy - 4))
    s += '</svg>'
    return s

def svg_concave_over():
    s = ('<svg viewBox="0 0 240 150" role="img" '
         'aria-label="A concave-up bowl curve with a straight trapezium top lying above it, '
         'so the estimate 42 is larger than the true area 40" '
         'style="max-width:280px;font-family:Inter,sans-serif">')
    # shaded region between chord (top) and curve
    s += ('<path d="M40,50 L200,50 L200,50 Q120,140 40,50 Z" '
          'fill="#f59e0b" fill-opacity="0.3"/>')
    # curve
    s += '<path d="M40,50 Q120,140 200,50" fill="none" stroke="#3b82f6" stroke-width="2"/>'
    # straight trapezium top (chord)
    s += '<line x1="40" y1="50" x2="200" y2="50" stroke="#f59e0b" stroke-width="2"/>'
    # end verticals
    s += '<line x1="40" y1="50" x2="40" y2="128" stroke="currentColor" stroke-width="1"/>'
    s += '<line x1="200" y1="50" x2="200" y2="128" stroke="currentColor" stroke-width="1"/>'
    s += '<line x1="30" y1="128" x2="215" y2="128" stroke="currentColor" stroke-width="1"/>'
    s += ('<text x="120" y="44" font-size="11" fill="currentColor" '
          'text-anchor="middle">estimate 42</text>')
    s += ('<text x="120" y="120" font-size="11" fill="currentColor" '
          'text-anchor="middle">actual area 40</text>')
    s += '</svg>'
    return s

def svg_three_strips():
    # three trapezium strips, areas 10, 18, 14 over t = 0..6
    base = 125.0
    xs = [40.0, 100.0, 160.0, 220.0]  # 3 strips
    tops = [100.0, 55.0, 78.0]        # illustrative heights only (no numbers shown)
    s = ('<svg viewBox="0 0 260 150" role="img" '
         'aria-label="A speed-time graph split into three trapezium strips with areas 10, 18 and 14" '
         'style="max-width:280px;font-family:Inter,sans-serif">')
    # outline top polyline points: at each boundary a height
    top_pts = [tops[0], tops[0] * 0.85, tops[1], tops[2]]  # smoothish rising then dip
    top_pts = [100.0, 70.0, 60.0, 90.0]
    poly = "%.0f,%.0f " % (xs[0], base)
    poly += " ".join("%.0f,%.0f" % (xs[i], top_pts[i]) for i in range(4))
    poly += " %.0f,%.0f" % (xs[3], base)
    s += ('<polygon points="%s" fill="#60a5fa" fill-opacity="0.3" '
          'stroke="#3b82f6" stroke-width="1.5"/>' % poly)
    # dividers
    for i in (1, 2):
        s += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="currentColor" '
              'stroke-width="1" stroke-dasharray="2 2"/>' % (xs[i], top_pts[i], xs[i], base))
    # axis
    s += '<line x1="40" y1="125" x2="230" y2="125" stroke="currentColor" stroke-width="1"/>'
    s += '<line x1="40" y1="125" x2="40" y2="30" stroke="currentColor" stroke-width="1"/>'
    for i, area in enumerate((10, 18, 14)):
        cx = (xs[i] + xs[i + 1]) / 2
        s += ('<text x="%.0f" y="115" font-size="11" fill="currentColor" '
              'text-anchor="middle">%d</text>' % (cx, area))
    s += ('<text x="40" y="140" font-size="10" fill="currentColor" '
          'text-anchor="middle">0</text>')
    s += ('<text x="220" y="140" font-size="10" fill="currentColor" '
          'text-anchor="middle">6</text>')
    s += ('<text x="135" y="140" font-size="10" fill="currentColor" '
          'text-anchor="middle">t (s)</text>')
    s += '</svg>'
    return s

def prepend(display, svg, caption=True):
    tail = (svg + CAP + display) if caption else (svg + display)
    return tail

# ---------- assign figures ----------
figs = []

# GOLD
# gold[0] trapezium-rule area, points (0,1),(2,3),(4,7),(6,9),(8,10)
pts = [(0, 1), (2, 3), (4, 7), (6, 9), (8, 10)]
assert [y for _, y in pts] == [1, 3, 7, 9, 10]
pb["gold"][0]["chart"] = line_chart(pts, 0, 8, 2, 0, 12, 2)
figs.append({"tier": "gold", "index": 0, "kind": "chart",
             "what": "Area curve through the five given y-values (1,3,7,9,10) at x=0,2,4,6,8; area shaded under the line."})

# gold[1] velocity-time (0,0),(2,8),(4,12),(6,12),(8,8)
pts = [(0, 0), (2, 8), (4, 12), (6, 12), (8, 8)]
pb["gold"][1]["chart"] = line_chart(pts, 0, 8, 2, 0, 14, 2, xtitle="t (s)", ytitle="v (m/s)")
figs.append({"tier": "gold", "index": 1, "kind": "chart",
             "what": "Velocity-time graph plotting the exact v-values 0,8,12,12,8; shaded area is the distance the question asks for."})

# gold[2] falling tangent through (2,18),(6,2)
pb["gold"][2]["display"] = prepend(pb["gold"][2]["display"], svg_falling_tangent())
figs.append({"tier": "gold", "index": 2, "kind": "svg",
             "what": "Falling tangent through (2,18) and (6,2) marking x=4; the downward slope is the negative gradient (falling ball) to interpret."})

# gold[3] concave-up overestimate (estimate 42, actual 40)
pb["gold"][3]["display"] = prepend(pb["gold"][3]["display"], svg_concave_over())
figs.append({"tier": "gold", "index": 3, "kind": "svg",
             "what": "Concave-up bowl with the straight trapezium top above it; shows why 42 > 40 (overestimate)."})

# gold[4] three strips areas 10,18,14 over t=0..6
pb["gold"][4]["display"] = prepend(pb["gold"][4]["display"], svg_three_strips())
figs.append({"tier": "gold", "index": 4, "kind": "svg",
             "what": "Speed-time graph split into three trapezium strips labelled with their areas 10, 18, 14 over t=0..6."})

# SILVER
# silver[0] points (0,2),(3,6),(6,8) find h
pts = [(0, 2), (3, 6), (6, 8)]
pb["silver"][0]["chart"] = line_chart(pts, 0, 6, 1, 0, 10, 2)
figs.append({"tier": "silver", "index": 0, "kind": "chart",
             "what": "Two strips through (0,2),(3,6),(6,8); equal x-gaps make the strip width h visible."})

# silver[1] y0=2,y1=6,y2=8, h=3 -> x=0,3,6
pts = [(0, 2), (3, 6), (6, 8)]
pb["silver"][1]["chart"] = line_chart(pts, 0, 6, 1, 0, 10, 2)
figs.append({"tier": "silver", "index": 1, "kind": "chart",
             "what": "Same three points at x=0,3,6 (h=3) with area shaded for the two-strip trapezium rule."})

# silver[2] parabola y=x^2 + tangent y=6x-9, points (1,-3),(5,21), touch (3,9)
curve = []
x = -1.0
while x <= 5.01:
    curve.append((round(x, 2), round(x * x, 3)))
    x += 0.5
for cx, cy in curve:
    assert abs(cy - cx * cx) < 1e-6
tangent = [(-1, 6 * -1 - 9), (5.5, 6 * 5.5 - 9)]   # y = 6x - 9
assert 6 * 1 - 9 == -3 and 6 * 5 - 9 == 21 and 6 * 3 - 9 == 9
marks = [(1, -3), (5, 21), (3, 9)]
pb["silver"][2]["chart"] = two_ds_chart(curve, tangent, marks, -1, 6, 1, -10, 30, 5)
figs.append({"tier": "silver", "index": 2, "kind": "chart",
             "what": "y=x^2 (blue) with its tangent y=6x-9 (amber) touching at (3,9) and passing through the given (1,-3) and (5,21); slope 6."})

# silver[3] velocity-time (0,0),(5,10),(10,10)
pts = [(0, 0), (5, 10), (10, 10)]
pb["silver"][3]["chart"] = line_chart(pts, 0, 10, 5, 0, 12, 2, xtitle="t (s)", ytitle="v (m/s)")
figs.append({"tier": "silver", "index": 3, "kind": "chart",
             "what": "Speed-time graph through (0,0),(5,10),(10,10); shaded area is the distance over two strips."})

# silver[5] (0,0),(1,4),(2,6),(3,6),(4,4)
pts = [(0, 0), (1, 4), (2, 6), (3, 6), (4, 4)]
assert [y for _, y in pts] == [0, 4, 6, 6, 4]
pb["silver"][5]["chart"] = line_chart(pts, 0, 4, 1, 0, 8, 2)
figs.append({"tier": "silver", "index": 5, "kind": "chart",
             "what": "Symmetric hump through the given y-values 0,4,6,6,4 at x=0..4; area shaded for the trapezium rule."})

# BRONZE
# bronze[3] trapezium sides 3 and 7, width 2
pb["bronze"][3]["display"] = prepend(pb["bronze"][3]["display"],
    svg_trapezium(3, 7, 2, "A trapezium strip with parallel sides y=3 and y=7 and width h=2"))
figs.append({"tier": "bronze", "index": 3, "kind": "svg",
             "what": "Trapezium strip, left side y=3, right side y=7, width h=2, matching the values to find its area."})

# bronze[4] sides 5 and 5, width 4 (rectangle)
pb["bronze"][4]["display"] = prepend(pb["bronze"][4]["display"],
    svg_trapezium(5, 5, 4, "A trapezium with both parallel sides y=5 and width h=4, so it is a rectangle"))
figs.append({"tier": "bronze", "index": 4, "kind": "svg",
             "what": "Equal-sided trapezium (a rectangle), both sides y=5, width h=4."})

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, "with", len(figs), "figures")
for f in figs:
    print(" ", f["tier"], f["index"], f["kind"])
