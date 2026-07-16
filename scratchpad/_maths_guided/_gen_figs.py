# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for geometry-L07 (Circle Theorems).
Every figure is built programmatically from the problem's own numbers.
Theme-safe: text/strokes use currentColor; region fills soft with opacity.
"""
import math, json, io

def P(cx, cy, R, ang):
    """Point on circle at math-angle ang (deg); screen y is down."""
    a = math.radians(ang)
    return (cx + R*math.cos(a), cy - R*math.sin(a))

def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")

def arc(vx, vy, dir1, dir2, r, reflex=False):
    """SVG path arc between two directions (math-deg) around vertex, radius r.
    Short way unless reflex=True."""
    d = ((dir2 - dir1 + 180) % 360) - 180  # signed short diff (-180,180]
    if not reflex:
        if d >= 0:
            a1, a2, large, sweep = dir1, dir1 + d, 0, 0
        else:
            a1, a2, large, sweep = dir1, dir1 + d, 0, 1
    else:
        # go the long way round (>180)
        if d >= 0:
            a1, a2, large, sweep = dir1, dir1 + d - 360, 1, 1
        else:
            a1, a2, large, sweep = dir1, dir1 + d + 360, 1, 0
    x1 = vx + r*math.cos(math.radians(a1)); y1 = vy - r*math.sin(math.radians(a1))
    x2 = vx + r*math.cos(math.radians(a2)); y2 = vy - r*math.sin(math.radians(a2))
    return "M%s %s A%s %s 0 %d %d %s %s" % (f(x1), f(y1), f(r), f(r), large, sweep, f(x2), f(y2))

def bisdir(dir1, dir2, reflex=False):
    d = ((dir2 - dir1 + 180) % 360) - 180
    b = dir1 + d/2.0
    if reflex:
        b += 180
    return b

def lbl_at(vx, vy, direction, r):
    x = vx + r*math.cos(math.radians(direction)); y = vy - r*math.sin(math.radians(direction))
    return x, y

TXT = 'font-family="Inter,system-ui,sans-serif"'
def text(x, y, s, size=11, anchor="middle", weight=None):
    w = ' font-weight="%s"' % weight if weight else ''
    return '<text x="%s" y="%s" %s font-size="%d" text-anchor="%s" fill="currentColor"%s>%s</text>' % (
        f(x), f(y+size*0.35), TXT, size, anchor, w, s)

def dot(x, y, r=2.4):
    return '<circle cx="%s" cy="%s" r="%s" fill="currentColor"/>' % (f(x), f(y), f(r))

def line(x1, y1, x2, y2, w=1.6, extra=""):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="%s"%s/>' % (
        f(x1), f(y1), f(x2), f(y2), f(w), extra)

def anglepath(d, w=1.4):
    return '<path d="%s" fill="none" stroke="currentColor" stroke-width="%s"/>' % (d, f(w))

def rightangle(vx, vy, dir1, dir2, size=11):
    """small square at vertex between two directions."""
    p1x = vx + size*math.cos(math.radians(dir1)); p1y = vy - size*math.sin(math.radians(dir1))
    p2x = vx + size*math.cos(math.radians(dir2)); p2y = vy - size*math.sin(math.radians(dir2))
    cx = p1x + (p2x - vx); cy = p1y + (p2y - vy)
    return '<path d="M%s %s L%s %s L%s %s" fill="none" stroke="currentColor" stroke-width="1.3"/>' % (
        f(p1x), f(p1y), f(cx), f(cy), f(p2x), f(p2y))

def tick(x1, y1, x2, y2, n=1):
    """tick marks at midpoint of segment, perpendicular."""
    mx, my = (x1+x2)/2, (y1+y2)/2
    ang = math.atan2(y2-y1, x2-x1)
    px, py = -math.sin(ang), math.cos(ang)  # perpendicular unit
    dx, dy = math.cos(ang), math.sin(ang)
    out = []
    for i in range(n):
        off = (i - (n-1)/2.0) * 4
        bx, by = mx + dx*off, my + dy*off
        out.append(line(bx-px*4, by-py*4, bx+px*4, by+py*4, 1.3))
    return "".join(out)

def svg_open(w, h, label):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
            'style="max-width:280px;width:100%%;height:auto">'
            % (w, h, label))
CIRC = '<circle cx="%s" cy="%s" r="%s" fill="#60a5fa" fill-opacity="0.10" stroke="currentColor" stroke-width="1.6"/>'
def circle(cx, cy, R):
    return CIRC % (f(cx), f(cy), f(R))

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

figs = {}

# ---------- Type A: centre / circumference angle ----------
def centre_circ(central, centre_lbl, circ_lbl, aria):
    cx, cy, R = 120, 108, 66
    half = central/2.0
    aA = 270 - half   # A
    aB = 270 + half   # B
    Ax, Ay = P(cx, cy, R, aA); Bx, By = P(cx, cy, R, aB)
    Cx, Cy = P(cx, cy, R, 90)  # top
    s = [svg_open(240, 190, aria), circle(cx, cy, R)]
    # radii
    s += [line(cx, cy, Ax, Ay), line(cx, cy, Bx, By)]
    # chords to C
    s += [line(Cx, Cy, Ax, Ay), line(Cx, Cy, Bx, By)]
    s += [dot(cx, cy), dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy)]
    # centre angle arc (between directions O->A and O->B, opening down)
    dOA = aA; dOB = aB
    s += [anglepath(arc(cx, cy, dOB, dOA, 22))]
    bd = bisdir(dOB, dOA); lx, ly = lbl_at(cx, cy, bd, 40)
    s += [text(lx, ly, centre_lbl, 11)]
    # circumference angle at C
    dCA = math.degrees(math.atan2(-(Ay-Cy), Ax-Cx))
    dCB = math.degrees(math.atan2(-(By-Cy), Bx-Cx))
    s += [anglepath(arc(Cx, Cy, dCA, dCB, 20))]
    bdc = bisdir(dCA, dCB); lx2, ly2 = lbl_at(Cx, Cy, bdc, 34)
    s += [text(lx2, ly2, circ_lbl, 11)]
    # labels
    s += [text(cx+10, cy-2, "O", 11, "start")]
    s += [text(Ax-8, Ay+4, "A", 11, "end"), text(Bx+8, By+4, "B", 11, "start"), text(Cx, Cy-8, "C", 11)]
    s.append("</svg>")
    return "".join(s)

figs[("bronze",0)] = centre_circ(120, "120°", "?", "Circle centre O with angle 120 degrees at the centre and unknown angle at circumference C")
figs[("bronze",1)] = centre_circ(70, "?", "35°", "Circle centre O with 35 degrees at circumference C and unknown angle at the centre")
figs[("bronze",6)] = centre_circ(160, "160°", "?", "Circle centre O with angle 160 degrees at the centre and unknown angle at circumference C")

# ---------- Type B: semicircle triangle ----------
def semicircle(apex_lbl, base_left=None, base_right=None, aria="", apex_pos=115, right_mark=False):
    cx, cy, R = 120, 118, 74
    Ax, Ay = cx-R, cy   # left end diameter
    Bx, By = cx+R, cy   # right end
    Cx, Cy = P(cx, cy, R, apex_pos)
    s = [svg_open(240, 168, aria)]
    # semicircle arc (top half)
    s.append('<path d="M%s %s A%s %s 0 0 1 %s %s Z" fill="#60a5fa" fill-opacity="0.10" stroke="currentColor" stroke-width="1.6"/>'
             % (f(Ax), f(Ay), f(R), f(R), f(Bx), f(By)))
    s += [line(Ax, Ay, Cx, Cy), line(Bx, By, Cx, Cy)]
    s += [dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy), dot(cx, cy)]
    # apex angle
    dCA = math.degrees(math.atan2(-(Ay-Cy), Ax-Cx))
    dCB = math.degrees(math.atan2(-(By-Cy), Bx-Cx))
    if right_mark:
        s += [rightangle(Cx, Cy, dCA, dCB, 12)]
    else:
        s += [anglepath(arc(Cx, Cy, dCA, dCB, 18))]
    bdc = bisdir(dCA, dCB); lx, ly = lbl_at(Cx, Cy, bdc, 30)
    s += [text(lx, ly, apex_lbl, 11)]
    if base_left is not None:
        dAB = math.degrees(math.atan2(-(By-Ay), Bx-Ax))
        dAC = math.degrees(math.atan2(-(Cy-Ay), Cx-Ax))
        s += [anglepath(arc(Ax, Ay, dAB, dAC, 20))]
        bx, by = lbl_at(Ax, Ay, bisdir(dAB, dAC), 34); s += [text(bx, by, base_left, 10)]
    if base_right is not None:
        dBA = math.degrees(math.atan2(-(Ay-By), Ax-Bx))
        dBC = math.degrees(math.atan2(-(Cy-By), Cx-Bx))
        s += [anglepath(arc(Bx, By, dBC, dBA, 20))]
        bx, by = lbl_at(Bx, By, bisdir(dBC, dBA), 34); s += [text(bx, by, base_right, 10)]
    s += [text(Ax-7, Ay+4, "A", 11, "end"), text(Bx+7, By+4, "B", 11, "start"), text(Cx, Cy-8, "C", 11)]
    s += [text(cx, cy+14, "diameter", 9)]
    s.append("</svg>")
    return "".join(s)

figs[("bronze",2)] = semicircle("?", aria="Triangle in a semicircle, right angle opposite the diameter unknown", apex_pos=118, right_mark=False)
figs[("silver",6)] = semicircle("90°", base_left=None, base_right="32°", aria="Triangle in a semicircle with 90 degrees at the top, 32 degrees at one base, third angle unknown", apex_pos=118, right_mark=True)
# silver6 needs the 32 at a base and ? third -> redo with both bases
def semicircle2(aria):
    cx, cy, R = 120, 118, 74
    Ax, Ay = cx-R, cy; Bx, By = cx+R, cy
    Cx, Cy = P(cx, cy, R, 122)
    s = [svg_open(240, 168, aria)]
    s.append('<path d="M%s %s A%s %s 0 0 1 %s %s Z" fill="#60a5fa" fill-opacity="0.10" stroke="currentColor" stroke-width="1.6"/>'
             % (f(Ax), f(Ay), f(R), f(R), f(Bx), f(By)))
    s += [line(Ax, Ay, Cx, Cy), line(Bx, By, Cx, Cy)]
    s += [dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy)]
    dCA = math.degrees(math.atan2(-(Ay-Cy), Ax-Cx)); dCB = math.degrees(math.atan2(-(By-Cy), Bx-Cx))
    s += [rightangle(Cx, Cy, dCA, dCB, 12)]
    lx, ly = lbl_at(Cx, Cy, bisdir(dCA, dCB), 30); s += [text(lx, ly, "90°", 10)]
    dAB = math.degrees(math.atan2(-(By-Ay), Bx-Ax)); dAC = math.degrees(math.atan2(-(Cy-Ay), Cx-Ax))
    s += [anglepath(arc(Ax, Ay, dAB, dAC, 20))]
    bx, by = lbl_at(Ax, Ay, bisdir(dAB, dAC), 34); s += [text(bx, by, "32°", 10)]
    dBA = math.degrees(math.atan2(-(Ay-By), Ax-Bx)); dBC = math.degrees(math.atan2(-(Cy-By), Cx-Bx))
    s += [anglepath(arc(Bx, By, dBC, dBA, 20))]
    bx, by = lbl_at(Bx, By, bisdir(dBC, dBA), 30); s += [text(bx, by, "?", 11)]
    s += [text(Ax-7, Ay+4, "A", 11, "end"), text(Bx+7, By+4, "B", 11, "start"), text(Cx, Cy-8, "C", 11)]
    s.append("</svg>")
    return "".join(s)
figs[("silver",6)] = semicircle2("Triangle in a semicircle: right angle at C, 32 degrees at A, third angle at B unknown")

# ---------- Type C: cyclic quadrilateral ----------
def cyclic_quad(labels, aria, verts=("A", "B", "C", "D")):
    """labels: dict keyed by vertex letter; verts gives the four letters in order."""
    cx, cy, R = 120, 105, 68
    order = list(verts)
    angs = dict(zip(order, [150, 60, -10, 215]))
    pts = {k: P(cx, cy, R, a) for k, a in angs.items()}
    s = [svg_open(240, 195, aria), circle(cx, cy, R)]
    # quad fill
    poly = " ".join("%s,%s" % (f(pts[k][0]), f(pts[k][1])) for k in order)
    s.append('<polygon points="%s" fill="#f59e0b" fill-opacity="0.14" stroke="currentColor" stroke-width="1.6"/>' % poly)
    for k in order:
        s.append(dot(*pts[k]))
    # angle labels near each vertex (toward centre)
    for k in order:
        if labels.get(k):
            px, py = pts[k]
            dirc = math.degrees(math.atan2(-(cy-py), cx-px))
            lx, ly = lbl_at(px, py, dirc, 24)
            s.append(text(lx, ly, labels[k], 10))
    # vertex letters (outward)
    for k in order:
        px, py = pts[k]
        dout = math.degrees(math.atan2(-(py-cy), px-cx))
        lx, ly = lbl_at(px, py, dout, 12)
        s.append(text(lx, ly, k, 11))
    s.append("</svg>")
    return "".join(s)

figs[("bronze",3)] = cyclic_quad({"A":"85°", "C":"x°"}, "Cyclic quadrilateral with opposite angles 85 degrees and x")
figs[("bronze",7)] = cyclic_quad({"A":"x°", "C":"105°"}, "Cyclic quadrilateral with opposite angles x and 105 degrees")
figs[("silver",2)] = cyclic_quad({"A":"3x+5", "C":"2x+15"}, "Cyclic quadrilateral ABCD with angle A 3x+5 and angle C 2x+15")
figs[("gold",3)] = cyclic_quad({"A":"2x+10", "B":"3y", "C":"x+20", "D":"2y+30"}, "Cyclic quadrilateral with angles 2x+10, 3y, x+20 and 2y+30")

# ---------- Type D: tangent-radius triangle (bronze5) ----------
def tangent_radius_triangle(aria):
    # O centre, circle; T on circle; tangent to P; right angle at T; P angle 35; ? at O
    cx, cy, R = 92, 100, 46
    Tx, Ty = P(cx, cy, R, 40)   # tangent point upper-right
    # tangent direction perpendicular to OT
    otang = 40
    tdir = otang - 90  # tangent line direction
    # P along tangent from T
    L = 96
    Px = Tx + L*math.cos(math.radians(tdir)); Py = Ty - L*math.sin(math.radians(tdir))
    s = [svg_open(240, 200, aria), circle(cx, cy, R)]
    s += [line(cx, cy, Tx, Ty), line(Tx, Ty, Px, Py), line(cx, cy, Px, Py)]
    s += [dot(cx, cy), dot(Tx, Ty), dot(Px, Py)]
    # right angle at T between T->O and T->P
    dTO = math.degrees(math.atan2(-(cy-Ty), cx-Tx)); dTP = math.degrees(math.atan2(-(Py-Ty), Px-Tx))
    s += [rightangle(Tx, Ty, dTO, dTP, 11)]
    # angle at P (35)
    dPT = math.degrees(math.atan2(-(Ty-Py), Tx-Px)); dPO = math.degrees(math.atan2(-(cy-Py), cx-Px))
    s += [anglepath(arc(Px, Py, dPT, dPO, 22))]
    bx, by = lbl_at(Px, Py, bisdir(dPT, dPO), 36); s += [text(bx, by, "35°", 10)]
    # angle at O (?)
    dOT = math.degrees(math.atan2(-(Ty-cy), Tx-cx)); dOP = math.degrees(math.atan2(-(Py-cy), Px-cx))
    s += [anglepath(arc(cx, cy, dOT, dOP, 20))]
    bx, by = lbl_at(cx, cy, bisdir(dOT, dOP), 32); s += [text(bx, by, "?", 11)]
    s += [text(cx-8, cy+4, "O", 11, "end"), text(Tx+2, Ty-8, "T", 11), text(Px+6, Py+4, "P", 11, "start")]
    s.append("</svg>")
    return "".join(s)
figs[("bronze",4)] = tangent_radius_triangle("Tangent TP meets radius OT at T, right angle at T, 35 degrees at P, angle at O unknown")

# ---------- Type E: same segment (bronze6) ----------
def same_segment(a1_lbl, a2_lbl, aria):
    cx, cy, R = 120, 110, 66
    # chord endpoints at bottom
    Ax, Ay = P(cx, cy, R, 250); Bx, By = P(cx, cy, R, 290)
    # two points on major arc (top)
    Cx, Cy = P(cx, cy, R, 130); Dx, Dy = P(cx, cy, R, 60)
    s = [svg_open(240, 190, aria), circle(cx, cy, R)]
    s += [line(Ax, Ay, Bx, By, 1.6)]  # chord
    s += [line(Cx, Cy, Ax, Ay), line(Cx, Cy, Bx, By), line(Dx, Dy, Ax, Ay), line(Dx, Dy, Bx, By)]
    s += [dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy), dot(Dx, Dy)]
    for (Vx, Vy, lbl) in [(Cx, Cy, a1_lbl), (Dx, Dy, a2_lbl)]:
        dVA = math.degrees(math.atan2(-(Ay-Vy), Ax-Vx)); dVB = math.degrees(math.atan2(-(By-Vy), Bx-Vx))
        s += [anglepath(arc(Vx, Vy, dVA, dVB, 17))]
        bx, by = lbl_at(Vx, Vy, bisdir(dVA, dVB), 30); s += [text(bx, by, lbl, 10)]
    s += [text(Ax-7, Ay+4, "A", 11, "end"), text(Bx+7, By+4, "B", 11, "start"),
          text(Cx-4, Cy-7, "C", 11, "end"), text(Dx+4, Dy-7, "D", 11, "start")]
    s.append("</svg>")
    return "".join(s)
figs[("bronze",5)] = same_segment("42°", "x°", "Two angles in the same segment on chord AB: 42 degrees and x")

# ---------- Type H: reflex angle at centre (silver1) ----------
def reflex_centre(circ_lbl, reflex_lbl, aria):
    cx, cy, R = 120, 110, 64
    Ax, Ay = P(cx, cy, R, 205); Bx, By = P(cx, cy, R, 335)
    Cx, Cy = P(cx, cy, R, 90)
    s = [svg_open(240, 195, aria), circle(cx, cy, R)]
    s += [line(cx, cy, Ax, Ay), line(cx, cy, Bx, By)]
    s += [line(Cx, Cy, Ax, Ay), line(Cx, Cy, Bx, By)]
    s += [dot(cx, cy), dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy)]
    # reflex angle at O (the major/long way, going over the top through where C is)
    dOA = 205; dOB = 335
    s += [anglepath(arc(cx, cy, dOA, dOB, 24, reflex=True))]
    lx, ly = lbl_at(cx, cy, 90, 18); s += [text(lx-14, ly, reflex_lbl, 10, "middle")]
    # circumference angle at C
    dCA = math.degrees(math.atan2(-(Ay-Cy), Ax-Cx)); dCB = math.degrees(math.atan2(-(By-Cy), Bx-Cx))
    s += [anglepath(arc(Cx, Cy, dCA, dCB, 16))]
    bx, by = lbl_at(Cx, Cy, bisdir(dCA, dCB), 26); s += [text(bx, by, circ_lbl, 10)]
    s += [text(cx+2, cy-9, "O", 10), text(Ax-7, Ay+4, "A", 11, "end"), text(Bx+7, By+4, "B", 11, "start"), text(Cx, Cy-8, "C", 11)]
    s.append("</svg>")
    return "".join(s)
figs[("silver",0)] = reflex_centre("54°", "?", "Circle centre O, 54 degrees at circumference C, reflex angle at centre unknown")

# silver5: minor arc centre 110, major arc circumference ?  -> centre angle on minor arc side + circumference on major arc
def centre_given_circ_major(centre_lbl, circ_lbl, aria):
    cx, cy, R = 120, 112, 64
    Ax, Ay = P(cx, cy, R, 210); Bx, By = P(cx, cy, R, 330)
    Cx, Cy = P(cx, cy, R, 90)  # major-arc circumference point
    s = [svg_open(240, 195, aria), circle(cx, cy, R)]
    s += [line(cx, cy, Ax, Ay), line(cx, cy, Bx, By), line(Cx, Cy, Ax, Ay), line(Cx, Cy, Bx, By)]
    s += [dot(cx, cy), dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy)]
    s += [anglepath(arc(cx, cy, 330, 210, 22))]
    bd = bisdir(330, 210); lx, ly = lbl_at(cx, cy, bd, 40); s += [text(lx, ly, centre_lbl, 10)]
    dCA = math.degrees(math.atan2(-(Ay-Cy), Ax-Cx)); dCB = math.degrees(math.atan2(-(By-Cy), Bx-Cx))
    s += [anglepath(arc(Cx, Cy, dCA, dCB, 18))]
    bx, by = lbl_at(Cx, Cy, bisdir(dCA, dCB), 30); s += [text(bx, by, circ_lbl, 10)]
    s += [text(cx+9, cy-2, "O", 10, "start"), text(Ax-7, Ay+4, "A", 11, "end"), text(Bx+7, By+4, "B", 11, "start"), text(Cx, Cy-8, "C", 11)]
    s.append("</svg>")
    return "".join(s)
figs[("silver",5)] = centre_given_circ_major("110°", "?", "Circle centre O, 110 degrees at centre on the minor arc, angle at circumference on major arc unknown")

# ---------- Type F: alternate segment (silver2 duplicate index? no, silver1 is alt seg? ) ----------
def alt_segment(tc_lbl, alt_lbl, aria, touch="T", chord_end="B", alt_pt="D"):
    cx, cy, R = 128, 96, 58
    # touch point at bottom
    Tx, Ty = P(cx, cy, R, 270)
    # tangent horizontal
    tl = (Tx-84, Ty); tr = (Tx+84, Ty)
    # chord from touch to chord_end on circle
    Bx, By = P(cx, cy, R, 30)
    # point in alternate segment
    Dx, Dy = P(cx, cy, R, 150)
    s = [svg_open(256, 190, aria), circle(cx, cy, R)]
    s += [line(tl[0], tl[1], tr[0], tr[1], 1.8)]  # tangent
    s += [line(Tx, Ty, Bx, By)]  # chord
    s += [line(Dx, Dy, Tx, Ty), line(Dx, Dy, Bx, By)]  # alternate segment angle
    s += [dot(Tx, Ty), dot(Bx, By), dot(Dx, Dy)]
    # tangent-chord angle at T (between tangent-right and chord T->B)
    dTr = math.degrees(math.atan2(-(tr[1]-Ty), tr[0]-Tx))
    dTB = math.degrees(math.atan2(-(By-Ty), Bx-Tx))
    s += [anglepath(arc(Tx, Ty, dTr, dTB, 20))]
    bx, by = lbl_at(Tx, Ty, bisdir(dTr, dTB), 33); s += [text(bx, by, tc_lbl, 10)]
    # alternate segment angle at D
    dDT = math.degrees(math.atan2(-(Ty-Dy), Tx-Dx)); dDB = math.degrees(math.atan2(-(By-Dy), Bx-Dx))
    s += [anglepath(arc(Dx, Dy, dDB, dDT, 17))]
    bx, by = lbl_at(Dx, Dy, bisdir(dDB, dDT), 30); s += [text(bx, by, alt_lbl, 10)]
    s += [text(Tx, Ty+15, touch, 11), text(Bx+7, By+2, chord_end, 11, "start"), text(Dx-7, Dy, alt_pt, 11, "end")]
    s += [text(tr[0]-2, tr[1]-6, "tangent", 8, "end")]
    s.append("</svg>")
    return "".join(s)
figs[("silver",1)] = alt_segment("?", "63°", "Tangent and chord meet at T, angle in alternate segment 63 degrees, tangent-chord angle unknown")
figs[("gold",0)] = alt_segment("x°", "40°", "Chord AB subtends 40 degrees at circumference, tangent at A makes angle x with chord AB", touch="A", chord_end="B", alt_pt="C")

# ---------- Type D2: tangent-chord-radius (silver4) ----------
def tangent_chord_radius(aria):
    cx, cy, R = 120, 84, 52
    Ax, Ay = P(cx, cy, R, 270)  # touch point at bottom
    # tangent horizontal through A
    tl = (Ax-80, Ay); tr = (Ax+80, Ay)
    # radius O to A (straight up)
    # chord A to B
    Bx, By = P(cx, cy, R, 40)
    s = [svg_open(240, 200, aria), circle(cx, cy, R)]
    s += [line(tl[0], tl[1], tr[0], tr[1], 1.8)]  # tangent AT
    s += [line(cx, cy, Ax, Ay)]  # radius OA
    s += [line(Ax, Ay, Bx, By)]  # chord AB
    s += [dot(cx, cy), dot(Ax, Ay), dot(Bx, By)]
    # right angle between radius (A->O, up) and tangent (A->T right)
    dAO = math.degrees(math.atan2(-(cy-Ay), cx-Ax)); dAtr = math.degrees(math.atan2(-(tr[1]-Ay), tr[0]-Ax))
    s += [rightangle(Ax, Ay, dAO, dAtr, 11)]
    # tangent-chord angle TAB = 55 (between tangent-right and chord A->B)
    dAB = math.degrees(math.atan2(-(By-Ay), Bx-Ax))
    s += [anglepath(arc(Ax, Ay, dAtr, dAB, 26))]
    bx, by = lbl_at(Ax, Ay, bisdir(dAtr, dAB), 38); s += [text(bx, by, "55°", 9)]
    # angle OAB = ? (between radius A->O and chord A->B)
    s += [anglepath(arc(Ax, Ay, dAB, dAO, 17))]
    bx, by = lbl_at(Ax, Ay, bisdir(dAB, dAO), 30); s += [text(bx, by, "?", 10)]
    s += [text(cx-9, cy, "O", 11, "end"), text(Ax, Ay+15, "A", 11), text(Bx+7, By+2, "B", 11, "start"),
          text(tr[0], tr[1]-6, "T", 9, "end")]
    s.append("</svg>")
    return "".join(s)
figs[("silver",3)] = tangent_chord_radius("Tangent AT touches at A, radius OA, chord AB, tangent-chord angle 55 degrees, angle OAB unknown")

# ---------- Type G: two tangents from external point (silver5 index4) ----------
def two_tangents(aria):
    cx, cy, R = 150, 100, 44
    Px, Py = 40, 100
    # tangent points: solve angle
    d = math.hypot(cx-Px, cy-Py)
    a = math.degrees(math.acos(R/d))
    base = math.degrees(math.atan2(-(Py-cy), Px-cx))  # dir O->P
    Ax, Ay = P(cx, cy, R, base + a)
    Bx, By = P(cx, cy, R, base - a)
    s = [svg_open(240, 190, aria), circle(cx, cy, R)]
    s += [line(Px, Py, Ax, Ay), line(Px, Py, Bx, By)]
    s += [line(cx, cy, Ax, Ay, 1.2, ' stroke-dasharray="3 3"'), line(cx, cy, Bx, By, 1.2, ' stroke-dasharray="3 3"')]
    s += [dot(Px, Py), dot(Ax, Ay), dot(Bx, By), dot(cx, cy)]
    # equal tick marks
    s += [tick(Px, Py, Ax, Ay, 1), tick(Px, Py, Bx, By, 1)]
    # length labels
    mx, my = (Px+Ax)/2, (Py+Ay)/2; s += [text(mx-6, my-8, "8 cm", 9, "middle")]
    mx, my = (Px+Bx)/2, (Py+By)/2; s += [text(mx-6, my+14, "? cm", 9, "middle")]
    s += [text(Px-8, Py+4, "P", 11, "end"), text(Ax+3, Ay-6, "A", 11, "start"), text(Bx+3, By+12, "B", 11, "start"), text(cx+8, cy+4, "O", 10, "start")]
    s.append("</svg>")
    return "".join(s)
figs[("silver",4)] = two_tangents("Two tangents PA and PB from external point P, PA is 8 cm, PB unknown")

# ---------- gold1: Pythagoras tangent + secant through centre (gold2 index) ----------
def tangent_secant_pythag(aria):
    cx, cy, R = 150, 104, 44
    Px, Py = 34, 104
    d = math.hypot(cx-Px, cy-Py)
    a = math.degrees(math.acos(R/d))
    base = math.degrees(math.atan2(-(Py-cy), Px-cx))
    Ax, Ay = P(cx, cy, R, base + a)  # tangent point
    # B is far intersection of line P-O with circle (through centre)
    Bx, By = cx + R, cy
    s = [svg_open(250, 200, aria), circle(cx, cy, R)]
    s += [line(Px, Py, Ax, Ay)]        # tangent PA
    s += [line(Px, Py, Bx, By, 1.6)]   # line through O to B
    s += [line(cx, cy, Ax, Ay, 1.4)]   # radius OA
    s += [dot(Px, Py), dot(Ax, Ay), dot(cx, cy), dot(Bx, By)]
    # right angle at A between A->P and A->O
    dAP = math.degrees(math.atan2(-(Py-Ay), Px-Ax)); dAO = math.degrees(math.atan2(-(cy-Ay), cx-Ax))
    s += [rightangle(Ax, Ay, dAP, dAO, 10)]
    # labels: PA=12 (on tangent), PO=13 (on secant), radius=r
    mx, my = Px + 0.62*(Ax-Px), Py + 0.62*(Ay-Py); s += [text(mx-9, my-2, "12", 10, "middle")]
    s += [text(Px + 0.5*(cx-Px), Py+15, "13", 10, "middle")]
    mx, my = (cx+Ax)/2, (cy+Ay)/2; s += [text(mx+9, my+2, "r", 10, "start")]
    s += [text(Px-8, Py+4, "P", 11, "end"), text(Ax-9, Ay+3, "A", 11, "end"), text(cx+2, cy-9, "O", 10, "middle"), text(Bx+6, By+4, "B", 11, "start")]
    s.append("</svg>")
    return "".join(s)
figs[("gold",2)] = tangent_secant_pythag("Tangent PA 12, line PB through centre O with PO 13, right angle at A, find radius")

# ---------- gold2: two circumference angles opposite arcs (index1) ----------
def opposite_arc_angles(minor_lbl, major_lbl, aria):
    cx, cy, R = 120, 108, 66
    Ax, Ay = P(cx, cy, R, 250); Bx, By = P(cx, cy, R, 290)
    Cx, Cy = P(cx, cy, R, 90)    # major arc point (top)
    Dx, Dy = P(cx, cy, R, 270)   # minor arc point (bottom) -- but between A,B on minor arc
    Dx, Dy = P(cx, cy, R, 270)
    s = [svg_open(240, 195, aria), circle(cx, cy, R)]
    s += [line(Ax, Ay, Bx, By, 1.6)]  # chord AB
    s += [line(Cx, Cy, Ax, Ay), line(Cx, Cy, Bx, By)]  # major arc angle
    s += [line(Dx, Dy, Ax, Ay), line(Dx, Dy, Bx, By)]  # minor arc angle
    s += [dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy), dot(Dx, Dy)]
    dCA = math.degrees(math.atan2(-(Ay-Cy), Ax-Cx)); dCB = math.degrees(math.atan2(-(By-Cy), Bx-Cx))
    s += [anglepath(arc(Cx, Cy, dCA, dCB, 18))]
    bx, by = lbl_at(Cx, Cy, bisdir(dCA, dCB), 30); s += [text(bx, by, major_lbl, 10)]
    dDA = math.degrees(math.atan2(-(Ay-Dy), Ax-Dx)); dDB = math.degrees(math.atan2(-(By-Dy), Bx-Dx))
    s += [anglepath(arc(Dx, Dy, dDB, dDA, 15))]
    bx, by = lbl_at(Dx, Dy, bisdir(dDB, dDA), 27); s += [text(bx, by, minor_lbl, 9)]
    s += [text(Ax-7, Ay+2, "A", 11, "end"), text(Bx+7, By+2, "B", 11, "start"), text(Cx, Cy-8, "C", 11), text(Dx, Dy+13, "D", 10)]
    s.append("</svg>")
    return "".join(s)
figs[("gold",1)] = opposite_arc_angles("28°", "?", "Chord AB, angle 28 degrees at D on minor arc, angle at C on major arc unknown")

# ---------- gold5: diameter, points both sides (index4) ----------
def diameter_same_segment(aria):
    cx, cy, R = 120, 106, 66
    Ax, Ay = P(cx, cy, R, 180); Cx, Cy = P(cx, cy, R, 0)   # diameter AC horizontal
    Bx, By = P(cx, cy, R, 55)   # B above
    Dx, Dy = P(cx, cy, R, 235)  # D below (opposite side of AC)
    s = [svg_open(240, 200, aria), circle(cx, cy, R)]
    s += [line(Ax, Ay, Cx, Cy, 1.8)]   # diameter
    s += [line(Ax, Ay, Bx, By), line(Bx, By, Cx, Cy)]  # triangle ABC
    s += [line(Ax, Ay, Dx, Dy), line(Dx, Dy, Bx, By)]  # angle ADB
    s += [dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy), dot(Dx, Dy), dot(cx, cy)]
    # right angle at B (semicircle)
    dBA = math.degrees(math.atan2(-(Ay-By), Ax-Bx)); dBC = math.degrees(math.atan2(-(Cy-By), Cx-Bx))
    s += [rightangle(Bx, By, dBA, dBC, 10)]
    # angle BAC = 34 at A between A->C and A->B
    dAC = math.degrees(math.atan2(-(Cy-Ay), Cx-Ax)); dAB = math.degrees(math.atan2(-(By-Ay), Bx-Ax))
    s += [anglepath(arc(Ax, Ay, dAC, dAB, 22))]
    bx, by = lbl_at(Ax, Ay, bisdir(dAC, dAB), 34); s += [text(bx, by, "34°", 9)]
    # angle ADB = ? at D between D->A and D->B
    dDA = math.degrees(math.atan2(-(Ay-Dy), Ax-Dx)); dDB = math.degrees(math.atan2(-(By-Dy), Bx-Dx))
    s += [anglepath(arc(Dx, Dy, dDA, dDB, 17))]
    bx, by = lbl_at(Dx, Dy, bisdir(dDA, dDB), 30); s += [text(bx, by, "?", 10)]
    s += [text(Ax-7, Ay+4, "A", 11, "end"), text(Bx+4, By-7, "B", 11, "start"), text(Cx+7, Cy+4, "C", 11, "start"), text(Dx-4, Dy+13, "D", 11, "end")]
    s.append("</svg>")
    return "".join(s)
figs[("gold",4)] = diameter_same_segment("Circle with diameter AC, angle BAC 34 degrees, B above and D below diameter, find angle ADB")

# ---------- teach-walk figures ----------
figs[("teach", "bronze")] = cyclic_quad(
    {"P": "95°", "Q": "70°", "R": "?", "S": "?"},
    "Cyclic quadrilateral PQRS with angle P 95 degrees, angle Q 70 degrees, angles R and S unknown",
    verts=("P", "Q", "R", "S"))
figs[("teach", "silver")] = cyclic_quad(
    {"A": "2x+20", "C": "3x−10"},
    "Cyclic quadrilateral with one angle 2x+20 and the opposite angle 3x minus 10")

def centre_isosceles(aria):
    # A on circumference (top), B and C at bottom; O centre; angle BAC=35; triangle OBC isosceles
    cx, cy, R = 120, 112, 66
    Ax, Ay = P(cx, cy, R, 90)      # A at top
    Bx, By = P(cx, cy, R, 215)     # B lower-left
    Cx, Cy = P(cx, cy, R, 325)     # C lower-right
    s = [svg_open(240, 200, aria), circle(cx, cy, R)]
    s += [line(Ax, Ay, Bx, By), line(Ax, Ay, Cx, Cy)]   # chords AB, AC
    s += [line(cx, cy, Bx, By), line(cx, cy, Cx, Cy)]    # radii OB, OC
    # isosceles triangle fill OBC
    s.append('<polygon points="%s,%s %s,%s %s,%s" fill="#34d399" fill-opacity="0.16" stroke="none"/>'
             % (f(cx), f(cy), f(Bx), f(By), f(Cx), f(Cy)))
    s += [dot(cx, cy), dot(Ax, Ay), dot(Bx, By), dot(Cx, Cy)]
    # angle BAC at A = 35
    dAB = math.degrees(math.atan2(-(By-Ay), Bx-Ax)); dAC = math.degrees(math.atan2(-(Cy-Ay), Cx-Ax))
    s += [anglepath(arc(Ax, Ay, dAB, dAC, 20))]
    bx, by = lbl_at(Ax, Ay, bisdir(dAB, dAC), 32); s += [text(bx, by, "35°", 10)]
    # tick marks on the two radii (equal)
    s += [tick(cx, cy, Bx, By, 1), tick(cx, cy, Cx, Cy, 1)]
    # base angle ? at B (angle OBC)
    dBO = math.degrees(math.atan2(-(cy-By), cx-Bx)); dBC = math.degrees(math.atan2(-(Cy-By), Cx-Bx))
    s += [anglepath(arc(Bx, By, dBC, dBO, 16))]
    bx, by = lbl_at(Bx, By, bisdir(dBC, dBO), 27); s += [text(bx, by, "?", 10)]
    s += [text(Ax, Ay-8, "A", 11), text(Bx-7, By+5, "B", 11, "end"), text(Cx+7, Cy+5, "C", 11, "start"),
          text(cx+3, cy+12, "O", 10, "start")]
    s.append("</svg>")
    return "".join(s)
figs[("teach", "gold")] = centre_isosceles(
    "Points A, B, C on a circle centre O; angle BAC 35 degrees; isosceles triangle OBC with base angle unknown")

# serialise
out = {("%s|%s" % (a, b)): v for (a, b), v in figs.items()}
json.dump(out, io.open("_figs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("generated", len(out), "figures")
for k in sorted(out): print(k, len(out[k]), "chars")
