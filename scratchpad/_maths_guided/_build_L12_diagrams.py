# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_diag_L12_live.json", encoding="utf-8"))

# ---------- SVG parabola sketch builder ----------
def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")

def parabola_svg(a, b, c, r1, r2, region, eqlabel, aria, shade="#60a5fa"):
    r1, r2 = min(r1, r2), max(r1, r2)
    span = r2 - r1
    xmin = r1 - 0.45 * span - 0.4
    xmax = r2 + 0.45 * span + 0.4
    W, H = 240, 172
    ML, MR, MT, MB = 20, 14, 16, 22
    PW = W - ML - MR
    PH = H - MT - MB
    N = 64
    xs = [xmin + (xmax - xmin) * i / N for i in range(N + 1)]
    ys = [a * x * x + b * x + c for x in xs]
    ylo = min(ys + [0.0]); yhi = max(ys + [0.0])
    pad = (yhi - ylo) * 0.10 or 1.0
    Ymin = ylo - pad; Ymax = yhi + pad
    def sx(x): return ML + (x - xmin) / (xmax - xmin) * PW
    def sy(y): return MT + (Ymax - y) / (Ymax - Ymin) * PH
    axisY = sy(0)
    curve = " ".join("%s,%s" % (fmt(sx(x)), fmt(sy(a * x * x + b * x + c))) for x in xs)

    def arc(x0, x1):
        pts = [x for x in xs if x0 - 1e-9 <= x <= x1 + 1e-9]
        if not pts or pts[0] > x0: pts = [x0] + pts
        if pts[-1] < x1: pts = pts + [x1]
        return pts

    shapes = []
    if region == "between":
        pts = arc(r1, r2)
        poly = ["%s,%s" % (fmt(sx(r1)), fmt(axisY))]
        poly += ["%s,%s" % (fmt(sx(x)), fmt(sy(a * x * x + b * x + c))) for x in pts]
        poly += ["%s,%s" % (fmt(sx(r2)), fmt(axisY))]
        shapes.append('<polygon points="%s" fill="%s" fill-opacity="0.3" stroke="none"/>' % (" ".join(poly), shade))
    else:  # outside: two arms above axis
        for (x0, x1) in [(xmin, r1), (r2, xmax)]:
            pts = arc(x0, x1)
            poly = ["%s,%s" % (fmt(sx(x0)), fmt(axisY))]
            poly += ["%s,%s" % (fmt(sx(x)), fmt(sy(a * x * x + b * x + c))) for x in pts]
            poly += ["%s,%s" % (fmt(sx(x1)), fmt(axisY))]
            shapes.append('<polygon points="%s" fill="%s" fill-opacity="0.3" stroke="none"/>' % (" ".join(poly), shade))

    yaxis = ""
    if xmin < 0 < xmax:
        yaxis = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>' % (
            fmt(sx(0)), fmt(MT), fmt(sx(0)), fmt(MT + PH))
    dots = "".join('<circle cx="%s" cy="%s" r="2.6" fill="currentColor"/>' % (fmt(sx(r)), fmt(axisY)) for r in (r1, r2))

    svg = (
        '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
        'style="max-width:240px;font-family:Inter,sans-serif">' % (W, H, aria)
        + '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>' % (
            fmt(ML), fmt(axisY), fmt(ML + PW), fmt(axisY))
        + yaxis
        + "".join(shapes)
        + '<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (curve, shade)
        + dots
        + '<text x="%s" y="%s" font-size="9" fill="currentColor" text-anchor="end" opacity="0.7">x</text>' % (
            fmt(ML + PW), fmt(axisY - 3))
        + '<text x="%s" y="12" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (
            fmt(W / 2), eqlabel)
        + '</svg>'
    )
    return svg

CAP = '<span class="figure-caption">Sketch, not drawn to scale</span>'

# ---------- teach walk sketches ----------
teach = pd["guided"]["teach"]

svg_b = parabola_svg(1, -7, 12, 3, 4, "between",
                     "y = x squared minus 7x plus 12",
                     "U-shaped parabola y = x squared minus 7x plus 12 crossing the x-axis at two points, with the region below the x-axis between the roots shaded")
teach["bronze"]["display"] = svg_b + CAP + "Solve \\(x^2 - 7x + 12 < 0\\)"

svg_s = parabola_svg(1, -2, -15, -3, 5, "outside",
                     "y = x squared minus 2x minus 15",
                     "U-shaped parabola y = x squared minus 2x minus 15 with the regions above the x-axis outside the two roots shaded")
teach["silver"]["display"] = svg_s + CAP + "Solve \\(x^2 - 2x - 15 \\geq 0\\)"

svg_g = parabola_svg(2, 5, -3, -3, 0.5, "between",
                     "y = 2x squared plus 5x minus 3",
                     "U-shaped parabola y = 2x squared plus 5x minus 3 crossing the x-axis at two points, with the region below the x-axis between the roots shaded")
teach["gold"]["display"] = svg_g + CAP + "Solve \\(2x^2 + 5x - 3 < 0\\)"

# ---------- silver[0] bank: Chart.js parabola (roots -2, 3 are GIVEN in the text) ----------
s0 = pd["problem_bank"]["silver"][0]
def q(x): return x * x - x - 6
xsC = [-3, -2, -1, 0, 0.5, 1, 2, 3, 4]
s0["chart"] = {
    "type": "scatter",
    "data": {"datasets": [{
        "type": "line",
        "data": [{"x": x, "y": q(x)} for x in xsC],
        "tension": 0.35, "fill": False,
        "borderColor": "#3b82f6", "pointRadius": 3, "pointBackgroundColor": "#3b82f6"
    }]},
    "options": {"scales": {
        "x": {"min": -4, "max": 5, "grid": {"color": "rgba(128,128,128,0.18)"},
              "ticks": {"stepSize": 1}, "title": {"text": "x", "display": True}},
        "y": {"min": -8, "max": 8, "grid": {"color": "rgba(128,128,128,0.18)"},
              "ticks": {"stepSize": 2}, "title": {"text": "y", "display": True}}
    }}
}

with io.open("lesson_algebra-L12_diagrams.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)

# preview
with io.open("_L12_diag_preview.html", "w", encoding="utf-8") as f:
    f.write('<body style="background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif">')
    for lbl, s in [("bronze", svg_b), ("silver", svg_s), ("gold", svg_g)]:
        f.write('<div style="display:inline-block;margin:10px;padding:8px;border:1px solid #ccc">'
                '<b>%s</b><br>%s</div>' % (lbl, s))
    f.write('</body>')
print("wrote lesson_algebra-L12_diagrams.json")
print("silver[0] chart points q(x):", [(x, q(x)) for x in xsC])
print("bronze svg len", len(svg_b), "silver", len(svg_s), "gold", len(svg_g))
