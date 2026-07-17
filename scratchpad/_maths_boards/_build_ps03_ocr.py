# -*- coding: utf-8 -*-
"""Full guided + diagrams build for maths-ocr probability-statistics-L03 (Representing Data)."""
import json, math, io

MINUS = "−"  # unicode minus

# ---------- SVG generators ----------
def pt(cx, cy, r, ang):
    th = math.radians(ang)
    return (cx + r*math.sin(th), cy - r*math.cos(th))

def pie_svg(sectors, aria, vb_w=150, cx=70, cy=70, r=52, fs=11):
    """sectors: list of (label, angle_degrees, color). Drawn clockwise from top."""
    parts = ['<svg viewBox="0 0 %d 150" role="img" aria-label="%s" style="max-width:180px">' % (vb_w, aria)]
    a0 = 0.0
    for label, ang, color in sectors:
        a1 = a0 + ang
        x0, y0 = pt(cx, cy, r, a0)
        x1, y1 = pt(cx, cy, r, a1)
        large = 1 if ang > 180 else 0
        parts.append('<path d="M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" fill="%s" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"/>'
                     % (cx, cy, x0, y0, r, r, large, x1, y1, color))
        mid = (a0 + a1) / 2.0
        lx, ly = pt(cx, cy, r*0.6, mid)
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="%d" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>'
                     % (lx, ly, fs, label))
        a0 = a1
    parts.append('</svg>')
    return "".join(parts)

def bar_svg(labels, vals, aria, ymax, step, ytitle):
    """Vertical bar chart, single series, value labels above bars."""
    left, right, top, bot = 38, 238, 22, 122
    plot_h = bot - top
    colors = ["#60a5fa", "#f59e0b", "#34d399", "#f472b6", "#a78bfa"]
    parts = ['<svg viewBox="0 0 250 160" role="img" aria-label="%s" style="max-width:280px">' % aria]
    n_lines = int(ymax // step)
    for k in range(n_lines + 1):
        v = k * step
        y = bot - (v / ymax) * plot_h
        parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (left, y, right, y))
        parts.append('<text x="%d" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="end" dominant-baseline="middle">%d</text>' % (left-4, y, v))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (left, top, left, bot))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (left, bot, right, bot))
    n = len(vals)
    slot = (right - left) / n
    bw = slot * 0.6
    for i, (lab, v) in enumerate(zip(labels, vals)):
        x = left + slot*i + (slot-bw)/2
        h = (v / ymax) * plot_h
        y = bot - h
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>' % (x, y, bw, h, colors[i % len(colors)]))
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">%d</text>' % (x+bw/2, y-3, v))
        parts.append('<text x="%.1f" y="133" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (x+bw/2, lab))
    parts.append('<text x="10" y="72" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 10 72)">%s</text>' % ytitle)
    parts.append('</svg>')
    return "".join(parts)

def stacked_svg(parts_list, aria, ymax, step):
    """Single stacked bar. parts_list: [(label, value, color), ...] bottom-to-top."""
    left, right, top, bot = 44, 144, 24, 128
    plot_h = bot - top
    p = ['<svg viewBox="0 0 190 160" role="img" aria-label="%s" style="max-width:200px">' % aria]
    n_lines = int(ymax // step)
    for k in range(n_lines + 1):
        v = k*step
        y = bot - (v/ymax)*plot_h
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (left, y, right, y))
        p.append('<text x="%d" y="%.1f" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="end" dominant-baseline="middle">%d</text>' % (left-4, y, v))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (left, top, left, bot))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>' % (left, bot, right, bot))
    bx, bw = 56, 54
    cum = 0
    for label, v, color in parts_list:
        y_bottom = bot - (cum/ymax)*plot_h
        h = (v/ymax)*plot_h
        y_top = y_bottom - h
        p.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>' % (bx, y_top, bw, h, color))
        p.append('<text x="%d" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s (%d)</text>' % (bx+bw/2, y_top+h/2, label, v))
        cum += v
    p.append('</svg>')
    return "".join(p)

# ---------- Build SVGs used in bank / opener / teach ----------
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# B3 pie: Maths 90 of 360
svg_b3 = pie_svg([("Maths 90°", 90, "#60a5fa"), ("Other", 270, "#94a3b8")],
                 "A pie chart with a Maths sector of 90 degrees")
# B5 pie: 60 sector
svg_b5 = pie_svg([("60°", 60, "#60a5fa"), ("Other", 300, "#94a3b8")],
                 "A pie chart with a sector of 60 degrees")
# S2 pie: 144 sector
svg_s2 = pie_svg([("144°", 144, "#60a5fa"), ("Other", 216, "#94a3b8")],
                 "A pie chart with a sector of 144 degrees representing 36 students")
# S5 pie: Pizza 150, Chips 90, Salad 120(?)
svg_s5 = pie_svg([("Pizza 150°", 150, "#60a5fa"), ("Chips 90°", 90, "#f59e0b"), ("Salad ?", 120, "#34d399")],
                 "A pie chart with Pizza 150 degrees, Chips 90 degrees and an unknown Salad sector")
# G2 pie: Other 72 of 360
svg_g2 = pie_svg([("Other 72°", 72, "#60a5fa"), ("Rest", 288, "#94a3b8")],
                 "A pie chart with an Other sector of 72 degrees")

# Opener pie: quarter
svg_open = pie_svg([("Pizza", 90, "#60a5fa"), ("Other", 270, "#94a3b8")],
                   "A circle with a quarter sector labelled Pizza and the rest Other")

# Bronze teach bar chart: Walk 12, Car 9, Bus 6, Cycle 3
svg_teach_b = bar_svg(["Walk", "Car", "Bus", "Cycle"], [12, 9, 6, 3],
                      "Bar chart of travel: Walk 12, Car 9, Bus 6, Cycle 3", 15, 3, "Number of students")
# Silver teach pie: Apple 40 of 360
svg_teach_s = pie_svg([("Apple 40°", 40, "#60a5fa"), ("Other", 320, "#94a3b8")],
                      "A pie chart with an Apple sector of 40 degrees, total 180 people")
# Gold teach stacked bar: Drinks 40, Snacks 30, Papers 10
svg_teach_g = stacked_svg([("Drinks", 40, "#60a5fa"), ("Snacks", 30, "#f59e0b"), ("Papers", 10, "#34d399")],
                          "A stacked bar for Monday sales: Drinks 40, Snacks 30, Papers 10", 80, 20)

print("SVG sizes:", len(svg_b3), len(svg_s5), len(svg_teach_b), len(svg_teach_g))
with open("_ps03_svgs.json", "w", encoding="utf-8") as f:
    json.dump({"b3": svg_b3, "b5": svg_b5, "s2": svg_s2, "s5": svg_s5, "g2": svg_g2,
               "open": svg_open, "tb": svg_teach_b, "ts": svg_teach_s, "tg": svg_teach_g},
              f, ensure_ascii=False, indent=1)
print("wrote _ps03_svgs.json")
