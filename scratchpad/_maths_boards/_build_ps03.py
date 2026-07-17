# -*- coding: utf-8 -*-
import json, math, copy

live = json.load(open("_live_ps03.json", encoding="utf-8"))
pd = copy.deepcopy(live)

# ---------- SVG helpers (theme-safe: currentColor strokes/text, soft fills) ----------
SOFT = ["#60a5fa", "#f59e0b", "#34d399", "#f472b6", "#a78bfa", "#94a3b8"]

def _pt(cx, cy, R, ang):
    r = math.radians(ang)
    return (cx + R * math.sin(r), cy - R * math.cos(r))

def pie(sectors, label, cx=70, cy=70, R=52, vbw=150, vbh=150):
    # sectors: list of (angle_degrees, fill_color, text)
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:180px">' % (vbw, vbh, label)]
    a = 0.0
    for ang, col, txt in sectors:
        a1 = a + ang
        x0, y0 = _pt(cx, cy, R, a)
        x1, y1 = _pt(cx, cy, R, a1)
        large = 1 if ang > 180 else 0
        out.append('<path d="M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" fill="%s" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"/>'
                    % (cx, cy, x0, y0, R, R, large, x1, y1, col))
        if txt:
            lx, ly = _pt(cx, cy, R * 0.60, (a + a1) / 2)
            out.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>' % (lx, ly, txt))
        a = a1
    out.append('</svg>')
    return "".join(out)

def two_pies(secA, labA, secB, labB, aria):
    left = pie(secA, aria, cx=70, cy=78, R=48, vbw=300, vbh=170)
    # inline second pie into same svg
    parts = ['<svg viewBox="0 0 300 170" role="img" aria-label="%s" style="max-width:280px">' % aria]
    def blk(sectors, cx, title):
        s = []
        a = 0.0
        for ang, col, txt in sectors:
            a1 = a + ang
            x0, y0 = _pt(cx, 78, 48, a)
            x1, y1 = _pt(cx, 78, 48, a1)
            large = 1 if ang > 180 else 0
            s.append('<path d="M%.1f %.1f L%.1f %.1f A48 48 0 %d 1 %.1f %.1f Z" fill="%s" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"/>'
                     % (cx, 78, x0, y0, large, x1, y1, col))
            if txt:
                lx, ly = _pt(cx, 78, 30, (a + a1) / 2)
                s.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>' % (lx, ly, txt))
            a = a1
        s.append('<text x="%d" y="150" font-family="Inter,sans-serif" font-size="12" fill="currentColor" text-anchor="middle">%s</text>' % (cx, title))
        return "".join(s)
    parts.append(blk(secA, 78, labA))
    parts.append(blk(secB, 222, labB))
    parts.append('</svg>')
    return "".join(parts)

def barchart(cats, vals, ymax, step, ylabel, aria, colors=None):
    # vertical bars with y-axis, gridlines, value labels
    W, H = 250, 160
    x0, y0 = 38, 122   # axis origin
    plotw, ploth = 200, 100
    n = len(cats)
    bw = plotw / n * 0.6
    gap = plotw / n
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:280px">' % (W, H, aria)]
    # gridlines + y ticks
    g = 0
    while g <= ymax:
        yy = y0 - (g / ymax) * ploth
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (x0, yy, x0 + plotw, yy))
        out.append('<text x="%d" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="end" dominant-baseline="middle">%d</text>' % (x0 - 4, yy, g))
        g += step
    # axes
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (x0, y0 - ploth, x0, y0))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (x0, y0, x0 + plotw, y0))
    for i, (c, v) in enumerate(zip(cats, vals)):
        bx = x0 + i * gap + (gap - bw) / 2
        bh = (v / ymax) * ploth
        col = (colors[i] if colors else SOFT[i % len(SOFT)])
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>' % (bx, y0 - bh, bw, bh, col))
        out.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (bx + bw / 2, y0 - bh - 3, v))
        out.append('<text x="%.1f" y="%d" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (bx + bw / 2, y0 + 11, c))
    out.append('<text x="10" y="70" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 10 70)">%s</text>' % ylabel)
    out.append('</svg>')
    return "".join(out)

def stacked_bar(parts, total, ymax, aria):
    # single stacked vertical bar, parts=list of (label,value,color)
    W, H = 190, 160
    x0, y0 = 44, 128
    ploth = 104
    bw = 54
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:200px">' % (W, H, aria)]
    g = 0
    while g <= ymax:
        yy = y0 - (g / ymax) * ploth
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (x0, yy, x0 + 100, yy))
        out.append('<text x="%d" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="end" dominant-baseline="middle">%d</text>' % (x0 - 4, yy, g))
        g += 10
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (x0, y0 - ploth, x0, y0))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (x0, y0, x0 + 100, y0))
    cum = 0
    for i, (lab, val, col) in enumerate(parts):
        h = (val / ymax) * ploth
        yy = y0 - (cum / ymax) * ploth - h
        out.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>' % (x0 + 12, yy, bw, h, col))
        out.append('<text x="%d" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s (%d)</text>' % (x0 + 12 + bw / 2, yy + h / 2, lab, val))
        cum += val
    out.append('</svg>')
    return "".join(out)

def semicircle_opener():
    # circle split in half: Football | Other
    return pie([(180, "#60a5fa", "Football"), (180, "#94a3b8", "Other")],
               "A circle split into two equal halves, one labelled Football, one labelled Other",
               cx=75, cy=70, R=52, vbw=160, vbh=150)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---------- 1. FIX the duplicate: bronze B3 shoe total 30 -> 32 ----------
b = pd["problem_bank"]["bronze"]
# B3 is index 3 (shoe sizes)
b3 = b[3]
assert "shoe" in b3["display"].lower(), b3["display"]
b3["chart"]["data"]["datasets"][0]["data"] = [3, 9, 10, 6, 4]  # was [3,7,10,6,4]=30 -> 32
b3["solutions"] = [32]

# ---------- descriptions ----------
pb = pd["problem_bank"]
pb["bronze_description"] = "Read a single value straight off a bar chart, or find a simple fraction from a pie chart."
pb["silver_description"] = "Compare two data sets, or convert between pie chart angles and frequencies."
pb["gold_description"] = "Combine steps: composite charts, comparing two pie charts, and estimating from a line of best fit."

print("build stage 1 ok")
json.dump(pd, open("_stage1.json", "w", encoding="utf-8"), ensure_ascii=False)
