# -*- coding: utf-8 -*-
import math

SOFT = ["#60a5fa", "#f59e0b", "#34d399", "#f472b6", "#a78bfa"]

def _pt(cx, cy, r, deg):
    # deg measured clockwise from top (12 o'clock)
    t = math.radians(deg)
    return (cx + r*math.sin(t), cy - r*math.cos(t))

def pie_svg(sectors, aria, r=52, cx=70, cy=70, vb="0 0 150 150", maxw=180, other_label="Other"):
    """sectors: list of (label, angle_degrees). If angles don't sum to 360,
    a final 'Other' sector fills the remainder (unlabelled amount)."""
    total = sum(a for _, a in sectors)
    segs = list(sectors)
    if total < 359.9:
        segs = segs + [(other_label, 360 - total)]
    parts = [f'<svg viewBox="{vb}" role="img" aria-label="{aria}" style="max-width:{maxw}px">']
    a0 = 0.0
    for i, (label, ang) in enumerate(segs):
        a1 = a0 + ang
        x0, y0 = _pt(cx, cy, r, a0)
        x1, y1 = _pt(cx, cy, r, a1)
        large = 1 if ang > 180 else 0
        col = "#94a3b8" if label == other_label else SOFT[i % len(SOFT)]
        parts.append(
            f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} Z" '
            f'fill="{col}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"/>')
        mid = (a0 + a1) / 2
        lx, ly = _pt(cx, cy, r*0.6, mid)
        parts.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Inter,sans-serif" font-size="11" '
            f'fill="currentColor" text-anchor="middle" dominant-baseline="middle">{label}</text>')
        a0 = a1
    parts.append("</svg>")
    return "".join(parts)

def bar_svg(bars, aria, ymax, step, ytitle, vb="0 0 250 160", maxw=280):
    """bars: list of (label, value). Axis 0..ymax, gridlines every step."""
    x_axis_y = 122.0
    top_y = 22.0
    plot_h = x_axis_y - top_y
    left = 38
    right = 238
    parts = [f'<svg viewBox="{vb}" role="img" aria-label="{aria}" style="max-width:{maxw}px">']
    n_lines = int(round(ymax/step))
    for k in range(n_lines+1):
        val = k*step
        y = x_axis_y - (val/ymax)*plot_h
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>')
        parts.append(f'<text x="{left-4}" y="{y:.1f}" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="end" dominant-baseline="middle">{val}</text>')
    parts.append(f'<line x1="{left}" y1="{top_y}" x2="{left}" y2="{x_axis_y}" stroke="currentColor" stroke-width="1.3"/>')
    parts.append(f'<line x1="{left}" y1="{x_axis_y}" x2="{right}" y2="{x_axis_y}" stroke="currentColor" stroke-width="1.3"/>')
    n = len(bars)
    slot = (right - (left+10)) / n
    bw = min(30.0, slot*0.6)
    for i, (label, val) in enumerate(bars):
        cx = left + 10 + slot*i + slot/2
        x = cx - bw/2
        h = (val/ymax)*plot_h
        y = x_axis_y - h
        col = SOFT[i % len(SOFT)]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{col}" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>')
        parts.append(f'<text x="{cx:.1f}" y="{y-3:.1f}" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">{val}</text>')
        parts.append(f'<text x="{cx:.1f}" y="133" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">{label}</text>')
    parts.append(f'<text x="10" y="72" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 10 72)">{ytitle}</text>')
    parts.append("</svg>")
    return "".join(parts)

def two_pies_svg(pieA, pieB, aria):
    """pieA/pieB: dict {sectors, caption}. Two pies in one wide svg."""
    parts = [f'<svg viewBox="0 0 300 175" role="img" aria-label="{aria}" style="max-width:280px">']
    for (px, py, pie) in ((75, 78, pieA), (225, 78, pieB)):
        r = 45
        segs = list(pie["sectors"])
        total = sum(a for _, a in segs)
        if total < 359.9:
            segs = segs + [("Other", 360-total)]
        a0 = 0.0
        for i, (label, ang) in enumerate(segs):
            a1 = a0 + ang
            x0, y0 = _pt(px, py, r, a0)
            x1, y1 = _pt(px, py, r, a1)
            large = 1 if ang > 180 else 0
            col = "#94a3b8" if label == "Other" else SOFT[i % len(SOFT)]
            parts.append(f'<path d="M{px} {py} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} Z" fill="{col}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"/>')
            mid = (a0+a1)/2
            lx, ly = _pt(px, py, r*0.62, mid)
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle" dominant-baseline="middle">{label}</text>')
            a0 = a1
        parts.append(f'<text x="{px}" y="152" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">{pie["caption"]}</text>')
    parts.append("</svg>")
    return "".join(parts)

if __name__ == "__main__":
    # quick geometry sanity
    print(pie_svg([("Walk", 90)], "test quarter")[:200])
