# -*- coding: utf-8 -*-
"""Add exam-realism SVG figures to geometry-L02 (Area & Perimeter).
Figures are generated programmatically from each problem's own numbers.
Prepends inline SVG to the START of problem.display (and teach displays).
Theme-safe: text/strokes = currentColor, region fills soft + opacity 0.3.
"""
import json, io, math

SOFT = "#60a5fa"
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'
HEAD = '<svg viewBox="0 0 {w} {h}" role="img" aria-label="{al}" font-family="Inter, sans-serif" font-size="12">'


def arc_pts(cx, cy, R, a0, a1, n=28):
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + R * math.cos(a), cy - R * math.sin(a)))
    return pts


def poly(pts):
    return " ".join("%.1f,%.1f" % (x, y) for x, y in pts)


def txt(x, y, s, anchor="middle"):
    return '<text x="%s" y="%s" text-anchor="%s" fill="currentColor">%s</text>' % (x, y, anchor, s)


def ra_mark(x, y, dx, dy, size=9):
    p1 = (x + dx * size, y + dy * size)
    p2 = (x + dx * size + (-dy) * size, y + dy * size + (-dx) * size)
    p3 = (x + (-dy) * size, y + (-dx) * size)
    return '<polyline points="%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="none" stroke="currentColor" stroke-width="1.2"/>' % (
        p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])


def rectangle(bottom, left, al):
    s = HEAD.format(w=240, h=140, al=al)
    s += '<rect x="40" y="22" width="160" height="84" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    s += txt(120, 124, bottom)
    s += txt(32, 68, left, "end")
    return s + "</svg>"


def triangle(base, height, al):
    s = HEAD.format(w=240, h=150, al=al)
    s += '<polygon points="40,112 200,112 112,30" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    s += '<line x1="112" y1="30" x2="112" y2="112" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += ra_mark(112, 112, 1, -1)
    s += txt(120, 128, base)
    s += txt(120, 78, height, "start")
    return s + "</svg>"


def parallelogram(base, height, al):
    s = HEAD.format(w=250, h=140, al=al)
    s += '<polygon points="55,110 195,110 225,45 85,45" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    s += '<line x1="120" y1="45" x2="120" y2="110" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += ra_mark(120, 110, 1, -1)
    s += txt(125, 124, base)
    s += txt(128, 82, height, "start")
    return s + "</svg>"


def trapezium(top, bottom, height, al, area=None):
    s = HEAD.format(w=240, h=145, al=al)
    s += '<polygon points="30,110 210,110 165,45 75,45" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    s += '<line x1="120" y1="45" x2="120" y2="110" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += ra_mark(120, 110, 1, -1)
    s += txt(120, 40, top)
    s += txt(120, 124, bottom)
    s += txt(126, 82, height, "start")
    if area:
        s += txt(120, 100, area)
    return s + "</svg>"


def square_p(perim, al):
    s = HEAD.format(w=220, h=160, al=al)
    s += '<rect x="60" y="25" width="100" height="100" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    for (x, y, o) in [(110, 25, "h"), (110, 125, "h"), (60, 75, "v"), (160, 75, "v")]:
        if o == "h":
            s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.5"/>' % (x, y - 4, x, y + 4)
        else:
            s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.5"/>' % (x - 4, y, x + 4, y)
    s += txt(110, 145, perim)
    return s + "</svg>"


def circle_dia(dia, al):
    s = HEAD.format(w=240, h=170, al=al)
    s += '<circle cx="120" cy="82" r="60" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    s += '<line x1="60" y1="82" x2="180" y2="82" stroke="currentColor" stroke-width="1.4"/>'
    s += '<circle cx="120" cy="82" r="2.5" fill="currentColor"/>'
    s += txt(120, 75, dia)
    return s + "</svg>"


def circle_rad(rad, al):
    s = HEAD.format(w=240, h=170, al=al)
    s += '<circle cx="120" cy="82" r="60" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    s += '<line x1="120" y1="82" x2="180" y2="82" stroke="currentColor" stroke-width="1.4"/>'
    s += '<circle cx="120" cy="82" r="2.5" fill="currentColor"/>'
    s += txt(150, 75, rad)
    return s + "</svg>"


def circle_label(main, radlabel, al, radline=True):
    s = HEAD.format(w=240, h=175, al=al)
    s += '<circle cx="120" cy="88" r="58" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
    if radline:
        s += '<line x1="120" y1="88" x2="178" y2="88" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>'
        s += '<circle cx="120" cy="88" r="2.5" fill="currentColor"/>'
        s += txt(150, 81, radlabel)
    else:
        s += txt(120, 16, radlabel)
    s += txt(120, 108, main)
    return s + "</svg>"


def quarter_circle(rad, al):
    s = HEAD.format(w=200, h=155, al=al)
    cx, cy, R = 50, 120, 100
    pts = [(cx, cy)] + arc_pts(cx, cy, R, 0, 90)
    s += '<polygon points="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % (poly(pts), SOFT)
    s += ra_mark(cx, cy, 1, -1)
    s += txt(100, 137, rad)
    return s + "</svg>"


def semicircle(rad, al):
    s = HEAD.format(w=240, h=150, al=al)
    cx, cy, R = 120, 120, 78
    pts = arc_pts(cx, cy, R, 0, 180)
    s += '<polygon points="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % (poly(pts), SOFT)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>' % (cx, cy, cx, cy - R)
    s += '<circle cx="%d" cy="%d" r="2.5" fill="currentColor"/>' % (cx, cy)
    s += txt(cx + 6, cy - R // 2, rad, "start")
    return s + "</svg>"


def sector(rad, ang_label, theta, al, arc_label=None):
    s = HEAD.format(w=240, h=165, al=al)
    cx, cy, R = 120, 142, 80
    a0, a1 = 90 - theta / 2.0, 90 + theta / 2.0
    pts = [(cx, cy)] + arc_pts(cx, cy, R, a0, a1)
    s += '<polygon points="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % (poly(pts), SOFT)
    aa = arc_pts(cx, cy, 24, a0, a1, 16)
    s += '<polyline points="%s" fill="none" stroke="currentColor" stroke-width="1.2"/>' % poly(aa)
    s += txt(cx, cy - 34, ang_label)
    ex = cx + R * math.cos(math.radians(a0))
    ey = cy - R * math.sin(math.radians(a0))
    s += txt((cx + ex) / 2 + 6, (cy + ey) / 2, rad, "start")
    if arc_label:
        s += txt(cx, cy - R - 6, arc_label)
    return s + "</svg>"


def annulus(outer, inner, al):
    s = HEAD.format(w=240, h=170, al=al)
    cx, cy, Ro, Ri = 120, 82, 65, 40
    s += '<path d="M%s Z M%s Z" fill="%s" fill-opacity="0.3" fill-rule="evenodd" stroke="currentColor" stroke-width="2"/>' % (
        "L".join("%.1f,%.1f" % p for p in arc_pts(cx, cy, Ro, 0, 360)),
        "L".join("%.1f,%.1f" % p for p in arc_pts(cx, cy, Ri, 0, 360)),
        SOFT)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>' % (cx, cy, cx + Ro, cy)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>' % (cx, cy, cx, cy + Ri)
    s += '<circle cx="%d" cy="%d" r="2.5" fill="currentColor"/>' % (cx, cy)
    s += txt(cx + Ro - 18, cy - 5, outer)
    s += txt(cx + 6, cy + Ri - 6, inner, "start")
    return s + "</svg>"


def running_track(straight, dia, al):
    s = HEAD.format(w=270, h=160, al=al)
    r = 39
    xl, xr, cy = 65, 195, 80
    pts = [(xl, cy - r), (xr, cy - r)]
    pts += arc_pts(xr, cy, r, 90, -90)
    pts += [(xl, cy + r)]
    pts += arc_pts(xl, cy, r, -90, -270)
    s += '<polygon points="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % (poly(pts), SOFT)
    s += txt(130, cy - r - 8, straight)
    s += '<line x1="222" y1="%d" x2="222" y2="%d" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>' % (cy - r, cy + r)
    s += '<line x1="218" y1="%d" x2="226" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (cy - r, cy - r)
    s += '<line x1="218" y1="%d" x2="226" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (cy + r, cy + r)
    s += txt(245, cy + 4, dia)
    return s + "</svg>"


pd = json.load(io.open("_geomL02_live.json", encoding="utf-8"))
pb = pd["problem_bank"]
figs = []


def prepend(container, key, svg, cap=False):
    add = svg + (CAP if cap else "")
    container[key] = add + container[key]


prepend(pb["bronze"][0], "display", rectangle("9 cm", "5 cm", "Rectangle, length 9 cm, width 5 cm"))
figs.append(("bronze", 0, "svg", "rectangle 9x5, area asked"))
prepend(pb["bronze"][1], "display", rectangle("12 cm", "7 cm", "Rectangle, length 12 cm, width 7 cm"))
figs.append(("bronze", 1, "svg", "rectangle 12x7, perimeter asked"))
prepend(pb["bronze"][2], "display", triangle("10 cm", "6 cm", "Triangle, base 10 cm, height 6 cm"), cap=True)
figs.append(("bronze", 2, "svg", "triangle base 10 height 6"))
prepend(pb["bronze"][3], "display", parallelogram("8 cm", "5 cm", "Parallelogram, base 8 cm, height 5 cm"), cap=True)
figs.append(("bronze", 3, "svg", "parallelogram base 8 height 5"))
prepend(pb["bronze"][4], "display", circle_dia("14 cm", "Circle, diameter 14 cm"))
figs.append(("bronze", 4, "svg", "circle diameter 14"))
prepend(pb["bronze"][5], "display", circle_rad("5 cm", "Circle, radius 5 cm"))
figs.append(("bronze", 5, "svg", "circle radius 5"))
prepend(pb["bronze"][6], "display", trapezium("5 cm", "9 cm", "6 cm", "Trapezium, parallel sides 5 cm and 9 cm, height 6 cm"), cap=True)
figs.append(("bronze", 6, "svg", "trapezium 5,9,h6"))
prepend(pb["bronze"][7], "display", square_p("Perimeter = 48 cm", "Square, perimeter 48 cm"))
figs.append(("bronze", 7, "svg", "square perimeter 48"))

prepend(pb["silver"][0], "display", circle_dia("18 cm", "Circle, diameter 18 cm"))
figs.append(("silver", 0, "svg", "circle diameter 18"))
prepend(pb["silver"][1], "display", circle_label("C = 31.4 cm", "r = ?", "Circle, circumference 31.4 cm, radius unknown"))
figs.append(("silver", 1, "svg", "circle C=31.4, r=?"))
al = "L-shaped floor, 8 m by 4 m bottom and 3 m by 5 m upright"
s = HEAD.format(w=200, h=155, al=al)
s += '<polygon points="40,30 70,30 70,80 120,80 120,120 40,120" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>' % SOFT
s += '<line x1="40" y1="80" x2="70" y2="80" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>'
s += txt(55, 24, "3 m")
s += txt(33, 58, "5 m", "end")
s += txt(80, 135, "8 m")
s += txt(128, 104, "4 m", "start")
s += "</svg>"
prepend(pb["silver"][2], "display", s)
figs.append(("silver", 2, "svg", "L-shape 8x4 + 3x5"))
prepend(pb["silver"][3], "display", quarter_circle("10 cm", "Quarter circle, radius 10 cm"))
figs.append(("silver", 3, "svg", "quarter circle r10"))
prepend(pb["silver"][4], "display", trapezium("8 cm", "12 cm", "h = ?", "Trapezium, parallel sides 8 cm and 12 cm, area 60 cm squared, height unknown", area="Area = 60 cm²"), cap=True)
figs.append(("silver", 4, "svg", "trapezium 8,12 area60 h=?"))
prepend(pb["silver"][5], "display", semicircle("7 cm", "Semicircle, radius 7 cm"))
figs.append(("silver", 5, "svg", "semicircle r7 perimeter"))
prepend(pb["silver"][6], "display", circle_label("Area = 50.3 cm²", "r = ?", "Circle, area 50.3 cm squared, radius unknown"))
figs.append(("silver", 6, "svg", "circle area 50.3, r=?"))

prepend(pb["gold"][0], "display", running_track("100 m", "60 m", "Running track, two 100 m straights and semicircular ends of diameter 60 m"))
figs.append(("gold", 0, "svg", "running track 100m + dia60"))
prepend(pb["gold"][1], "display", sector("8 cm", "135°", 135, "Sector, radius 8 cm, angle 135 degrees"), cap=True)
figs.append(("gold", 1, "svg", "sector r8 angle135"))
prepend(pb["gold"][2], "display", circle_label("Area = 200 cm²", "C = ?", "Circle, area 200 cm squared, circumference unknown", radline=False))
figs.append(("gold", 2, "svg", "circle area 200, C=?"))
prepend(pb["gold"][3], "display", sector("9 cm", "θ = ?", 76, "Sector, radius 9 cm, arc length 12 cm, angle unknown", arc_label="arc 12 cm"), cap=True)
figs.append(("gold", 3, "svg", "sector r9 arc12 angle=?"))
prepend(pb["gold"][4], "display", annulus("10 cm", "6 cm", "Annulus, outer radius 10 cm, inner radius 6 cm"))
figs.append(("gold", 4, "svg", "annulus outer10 inner6"))

teach = pd["guided"]["teach"]
prepend(teach["bronze"], "display", trapezium("7 cm", "11 cm", "4 cm", "Trapezium, parallel sides 7 cm and 11 cm, height 4 cm"), cap=True)
figs.append(("teach-bronze", -1, "svg", "trapezium 7,11,h4"))
prepend(teach["silver"], "display", circle_dia("20 cm", "Circle, diameter 20 cm"))
figs.append(("teach-silver", -1, "svg", "circle diameter 20"))
prepend(teach["gold"], "display", sector("8 cm", "45°", 45, "Sector, radius 8 cm, angle 45 degrees"), cap=True)
figs.append(("teach-gold", -1, "svg", "sector r8 angle45"))

json.dump(pd, io.open("lesson_geometry-L02_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("figures added:", len(figs))
for f in figs:
    print(" ", f)
mx = 0
for tier in ("bronze", "silver", "gold"):
    for p in pb[tier]:
        mx = max(mx, len(p["display"]))
print("max display len:", mx)
