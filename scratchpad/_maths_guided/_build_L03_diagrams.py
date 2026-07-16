# -*- coding: utf-8 -*-
import json, io, math

SRC = "_L03_live_fresh.json"
OUT = "lesson_L03_diagrams.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

def r2(x):
    return round(x, 1)

# ---------- PIE (single) ----------
def pie_single(total_label, angle, name, colour):
    cx, cy, r = 110, 100, 68
    th = math.radians(angle)
    ex = cx + r * math.sin(th)
    ey = cy - r * math.cos(th)
    large = 1 if angle > 180 else 0
    # sector path from top, clockwise
    path = "M%d %d L%d %d A%d %d 0 %d 1 %s %s Z" % (
        cx, cy, cx, cy - r, r, r, large, r2(ex), r2(ey))
    mid = math.radians(angle / 2.0)
    lx = cx + 0.55 * r * math.sin(mid)
    ly = cy - 0.55 * r * math.cos(mid)
    remid = math.radians(angle + (360 - angle) / 2.0)
    qx = cx + 0.5 * r * math.sin(remid)
    qy = cy - 0.5 * r * math.cos(remid)
    aria = "Pie chart of %s, the %s sector is %d degrees" % (total_label, name, angle)
    svg = (
        '<svg viewBox="0 0 220 200" role="img" aria-label="%s" '
        'style="max-width:220px;font-family:Inter,sans-serif">'
        '<text x="110" y="16" text-anchor="middle" font-size="12" fill="currentColor">%s</text>'
        '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
        '<text x="%s" y="%s" text-anchor="middle" font-size="12" fill="currentColor">%d°</text>'
        '<text x="%s" y="%s" text-anchor="middle" font-size="13" fill="currentColor">?</text>'
        '<text x="110" y="192" text-anchor="middle" font-size="11" fill="currentColor">Shaded sector = %s</text>'
        '</svg>'
    ) % (aria, total_label, cx, cy, r, path, colour,
         r2(lx), r2(ly + 4), angle, r2(qx), r2(qy + 4), name)
    return svg

# ---------- PIE (two side by side) ----------
def pie_two(title_a, ang_a, title_b, ang_b, name, colour):
    def one(cx, cy, r, angle, title):
        th = math.radians(angle)
        ex = cx + r * math.sin(th); ey = cy - r * math.cos(th)
        large = 1 if angle > 180 else 0
        path = "M%s %s L%s %s A%d %d 0 %d 1 %s %s Z" % (
            cx, cy, cx, cy - r, r, r, large, r2(ex), r2(ey))
        mid = math.radians(angle / 2.0)
        lx = cx + 0.55 * r * math.sin(mid); ly = cy - 0.55 * r * math.cos(mid)
        remid = math.radians(angle + (360 - angle) / 2.0)
        qx = cx + 0.5 * r * math.sin(remid); qy = cy - 0.5 * r * math.cos(remid)
        return (
            '<text x="%d" y="16" text-anchor="middle" font-size="11" fill="currentColor">%s</text>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            '<path d="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<text x="%s" y="%s" text-anchor="middle" font-size="11" fill="currentColor">%d°</text>'
            '<text x="%s" y="%s" text-anchor="middle" font-size="12" fill="currentColor">?</text>'
        ) % (cx, title, cx, cy, r, path, colour, r2(lx), r2(ly + 4), angle, r2(qx), r2(qy + 4))
    r = 46; cy = 100
    aria = "Two pie charts. %s with %s sector %d degrees, %s with %s sector %d degrees" % (
        title_a, name, ang_a, title_b, name, ang_b)
    svg = (
        '<svg viewBox="0 0 260 185" role="img" aria-label="%s" '
        'style="max-width:260px;font-family:Inter,sans-serif">'
        '%s%s'
        '<text x="130" y="178" text-anchor="middle" font-size="11" fill="currentColor">Shaded sector = %s</text>'
        '</svg>'
    ) % (aria, one(68, cy, r, ang_a, title_a), one(192, cy, r, ang_b, title_b), name)
    return svg

# ---------- HISTOGRAM ----------
def histogram(bars, xmin, xmax, ymax, aria):
    # bars: list of (x_lo, x_hi, fd)
    x0, xr = 44, 214           # y-axis px, right edge px
    base, top = 155, 30        # fd=0 px, fd=ymax px
    def px(v): return x0 + (v - xmin) / (xmax - xmin) * (xr - x0)
    def py(f): return base - (f / ymax) * (base - top)
    parts = []
    # axes
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (x0, top, x0, base))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (x0, base, xr, base))
    # y ticks
    f = 0
    while f <= ymax + 0.001:
        y = py(f)
        parts.append('<text x="%d" y="%s" text-anchor="end" font-size="9" fill="currentColor">%d</text>' % (x0 - 5, r2(y + 3), f))
        f += 1
    # bars
    xset = set()
    for (lo, hi, fd) in bars:
        xl, xh, yt = px(lo), px(hi), py(fd)
        parts.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.3"/>' % (
            r2(xl), r2(yt), r2(xh - xl), r2(base - yt)))
        parts.append('<text x="%s" y="%s" text-anchor="middle" font-size="10" fill="currentColor">%s</text>' % (
            r2((xl + xh) / 2), r2(yt - 4), fd))
        xset.add(lo); xset.add(hi)
    for v in sorted(xset):
        parts.append('<text x="%s" y="%s" text-anchor="middle" font-size="9" fill="currentColor">%d</text>' % (r2(px(v)), base + 13, v))
    parts.append('<text x="12" y="95" text-anchor="middle" font-size="9" fill="currentColor" transform="rotate(-90 12 95)">Frequency density</text>')
    parts.append('<text x="%d" y="188" text-anchor="middle" font-size="9" fill="currentColor">x</text>' % int((x0 + xr) / 2))
    return ('<svg viewBox="0 0 250 195" role="img" aria-label="%s" '
            'style="max-width:250px;font-family:Inter,sans-serif">%s</svg>') % (aria, "".join(parts))

# ---------- FREQUENCY TABLE ----------
def freq_table(rows, aria):
    # rows: list of (label, value); plus header
    x0, x1, xd = 20, 180, 112
    ry = 20; rh = 28
    parts = []
    n = len(rows) + 1
    parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.3"/>' % (x0, ry, x1 - x0, rh * n))
    parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.15"/>' % (x0, ry, x1 - x0, rh))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (xd, ry, xd, ry + rh * n))
    for i in range(1, n):
        y = ry + rh * i
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x0, y, x1, y))
    cells = [("Colour", "Frequency")] + rows
    for i, (a, b) in enumerate(cells):
        cy = ry + rh * i + rh / 2 + 4
        parts.append('<text x="%d" y="%s" text-anchor="middle" font-size="11" fill="currentColor">%s</text>' % (int((x0 + xd) / 2), r2(cy), a))
        parts.append('<text x="%d" y="%s" text-anchor="middle" font-size="11" fill="currentColor">%s</text>' % (int((xd + x1) / 2), r2(cy), b))
    h = ry + rh * n + 20
    return ('<svg viewBox="0 0 200 %d" role="img" aria-label="%s" '
            'style="max-width:200px;font-family:Inter,sans-serif">%s</svg>') % (h, aria, "".join(parts))

pb = pd["problem_bank"]

# gold[1]: two pies, sport 100/360, 120/240
pb["gold"][1]["display"] = pie_two("School A: 360", 100, "School B: 240", 120, "sport", "#60a5fa") + pb["gold"][1]["display"]
# gold[3]: histogram fd 3.2 (5-15), 4.8 (15-20)
pb["gold"][3]["display"] = histogram([(5, 15, 3.2), (15, 20, 4.8)], 5, 20, 5,
    "Histogram: class 5 to 15 frequency density 3.2, class 15 to 20 frequency density 4.8") + pb["gold"][3]["display"]
# gold[4]: two pies, car 144/200, 108/300
pb["gold"][4]["display"] = pie_two("Chart A: 200", 144, "Chart B: 300", 108, "car", "#34d399") + pb["gold"][4]["display"]

# bronze[4]: pie football 90/200
pb["bronze"][4]["display"] = pie_single("200 students", 90, "football", "#f59e0b") + pb["bronze"][4]["display"]
# bronze[5] and [6]: frequency table Red12 Blue8 Green10
ftbl = freq_table([("Red", "12"), ("Blue", "8"), ("Green", "10")],
    "Frequency table: Red 12, Blue 8, Green 10")
pb["bronze"][5]["display"] = ftbl + pb["bronze"][5]["display"]
pb["bronze"][6]["display"] = ftbl + pb["bronze"][6]["display"]
# bronze[7]: scatter positive (Chart.js)
pb["bronze"][7]["chart"] = {
    "type": "scatter",
    "data": {"datasets": [{"data": [
        {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 3}, {"x": 4, "y": 5},
        {"x": 5, "y": 6}, {"x": 6, "y": 6}, {"x": 7, "y": 8}, {"x": 8, "y": 9}],
        "pointRadius": 5, "backgroundColor": "#8b5cf6"}]},
    "options": {"scales": {
        "x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
        "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "y", "display": True}, "beginAtZero": True}}}
}

# silver[3]: pie grade A 54/100
pb["silver"][3]["display"] = pie_single("100 students", 54, "grade A", "#a78bfa") + pb["silver"][3]["display"]
# silver[4]: line of best fit y=2x+5 with marked point (8,21)
pb["silver"][4]["chart"] = {
    "type": "scatter",
    "data": {"datasets": [
        {"type": "line", "data": [{"x": 0, "y": 5}, {"x": 10, "y": 25}],
         "fill": False, "borderColor": "#3b82f6", "pointRadius": 0, "tension": 0},
        {"data": [{"x": 8, "y": 21}], "pointRadius": 6, "backgroundColor": "#ef4444"}]},
    "options": {"scales": {
        "x": {"min": 0, "max": 10, "grid": {"color": "rgba(0,0,0,0.05)"}, "ticks": {"stepSize": 2}, "title": {"text": "x", "display": True}},
        "y": {"min": 0, "max": 30, "grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 5}, "title": {"text": "y", "display": True}, "beginAtZero": True}}}
}
# silver[5]: histogram single bar fd 4 over 15-25
pb["silver"][5]["display"] = histogram([(15, 25, 4)], 15, 25, 5,
    "Histogram: class 15 to 25 frequency density 4") + pb["silver"][5]["display"]

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", OUT)
print("SVG lengths:")
for t in ("gold", "bronze", "silver"):
    for i, p in enumerate(pb[t]):
        d = p.get("display", "")
        if "<svg" in d:
            print(" ", t, i, len(d))
