# -*- coding: utf-8 -*-
"""SVG line-graph generator for guided openers/teach walks. Theme-safe, lean."""

def _fmt(n):
    return ("%g" % round(n, 2))

def svg_line(points, xmax, ymax, xlabel, ylabel, xticks, yticks, aria,
             W=260, H=180, shade=False, shade_color="#60a5fa"):
    L, R, T, B = 36, 12, 14, 26
    def px(x): return L + (x / xmax) * (W - L - R)
    def py(y): return (H - B) - (y / ymax) * (H - B - T)
    parts = []
    parts.append(
        '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
        'style="max-width:280px;font-family:Inter,sans-serif">' % (W, H, aria))
    # optional shaded area under the curve
    if shade:
        poly = " ".join("%s,%s" % (_fmt(px(x)), _fmt(py(y))) for x, y in points)
        poly = "%s,%s " % (_fmt(px(points[0][0])), _fmt(py(0))) + poly + \
               " %s,%s" % (_fmt(px(points[-1][0])), _fmt(py(0)))
        parts.append('<polygon points="%s" fill="%s" fill-opacity="0.3" '
                     'stroke="none"/>' % (poly, shade_color))
    # axes
    x0, y0 = _fmt(px(0)), _fmt(py(0))
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" '
                 'stroke-width="1"/>' % (x0, y0, _fmt(px(xmax)), y0))
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" '
                 'stroke-width="1"/>' % (x0, y0, x0, _fmt(py(ymax))))
    # ticks + labels
    for xt in xticks:
        X = _fmt(px(xt))
        parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" '
                     'stroke-width="0.7"/>' % (X, y0, X, _fmt(py(0) + 3)))
        parts.append('<text x="%s" y="%s" font-size="8" fill="currentColor" '
                     'text-anchor="middle">%g</text>' % (X, _fmt(py(0) + 12), xt))
    for yt in yticks:
        Y = _fmt(py(yt))
        parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" '
                     'stroke-width="0.7"/>' % (_fmt(px(0) - 3), Y, x0, Y))
        parts.append('<text x="%s" y="%s" font-size="8" fill="currentColor" '
                     'text-anchor="end">%g</text>' % (_fmt(px(0) - 5), _fmt(py(yt) + 3), yt))
    # curve
    poly = " ".join("%s,%s" % (_fmt(px(x)), _fmt(py(y))) for x, y in points)
    parts.append('<polyline points="%s" fill="none" stroke="#2563eb" '
                 'stroke-width="2"/>' % poly)
    for x, y in points:
        parts.append('<circle cx="%s" cy="%s" r="2.4" fill="#2563eb"/>'
                     % (_fmt(px(x)), _fmt(py(y))))
    # axis titles
    parts.append('<text x="%s" y="%s" font-size="9" fill="currentColor" '
                 'text-anchor="middle">%s</text>'
                 % (_fmt((L + W - R) / 2), H - 2, xlabel))
    parts.append('<text x="10" y="%s" font-size="9" fill="currentColor" '
                 'text-anchor="middle" transform="rotate(-90 10 %s)">%s</text>'
                 % (_fmt((T + H - B) / 2), _fmt((T + H - B) / 2), ylabel))
    parts.append('</svg>')
    return "".join(parts)
