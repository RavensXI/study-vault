# -*- coding: utf-8 -*-
import json, io, math

pd = json.load(io.open("_geomL01_live.json", encoding="utf-8"))

def pt(V, r, ang):
    return (V[0] + r*math.cos(math.radians(ang)), V[1] - r*math.sin(math.radians(ang)))
def f(p):
    return "%.1f,%.1f" % (p[0], p[1])
def arc(V, r, a0, a1, n=16):
    return " ".join(f(pt(V, r, a0 + (a1-a0)*i/n)) for i in range(n+1))
def POLY(pts, fill=None, op=None):
    s = '<polygon points="%s" ' % " ".join(f(p) for p in pts)
    if fill:
        s += 'fill="%s" fill-opacity="%s" ' % (fill, op)
    else:
        s += 'fill="none" '
    s += 'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    return s
def LINE(a, b, w=1.6, dash=None):
    d = ' stroke-dasharray="4 3"' if dash else ''
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="%s"%s/>' % (a[0], a[1], b[0], b[1], w, d)
def ARC(V, r, a0, a1):
    return '<polyline points="%s" fill="none" stroke="currentColor" stroke-width="1.2"/>' % arc(V, r, a0, a1)
def T(p, s, size=11):
    return '<text x="%.1f" y="%.1f" font-family="Inter, sans-serif" font-size="%s" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>' % (p[0], p[1], size, s)
def SVG(vb, aria, inner):
    return ('<svg viewBox="%s" style="display:block;margin:0 auto 0.25rem;max-width:260px;width:100%%" '
            'role="img" aria-label="%s">%s</svg>') % (vb, aria, inner)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def tickmarks(a, b):
    mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
    dx, dy = b[0]-a[0], b[1]-a[1]
    L = math.hypot(dx, dy); ux, uy = dx/L, dy/L; px, py = -uy, ux
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.4"/>' % (mx-px*4, my-py*4, mx+px*4, my+py*4)

def chev(cx, y):
    return '<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="currentColor" stroke-width="1.4"/>' % (cx-6, y-4, cx, y, cx-6, y+4)

def toward(P, c, t):
    return (P[0]+(c[0]-P[0])*t, P[1]+(c[1]-P[1])*t)

figs = {}

# ---------- BRONZE ----------
# B0: straight line, x and 72 (ray drawn at true 72 deg)
V = (120, 110)
inner = LINE((22, 110), (218, 110)) + LINE(V, pt(V, 82, 72))
inner += ARC(V, 34, 0, 72) + ARC(V, 30, 72, 180)
inner += T(pt(V, 44, 36), "72°") + T(pt(V, 42, 126), "x°")
figs[("bronze", 0)] = SVG("0 0 240 140", "Two angles on a straight line, one 72 degrees and one marked x", inner) + CAP

# B1: vertically opposite 68 and ?
V = (120, 80); A0, B0 = 20, 88
inner = LINE(pt(V, 92, A0), pt(V, 92, A0+180)) + LINE(pt(V, 70, B0), pt(V, 70, B0+180))
inner += ARC(V, 34, A0, B0) + ARC(V, 34, A0+180, B0+180)
inner += T(pt(V, 46, (A0+B0)/2), "68°") + T(pt(V, 46, (A0+B0)/2+180), "?")
figs[("bronze", 1)] = SVG("0 0 240 160", "Two crossing lines, one angle 68 degrees and the vertically opposite angle marked with a question mark", inner) + CAP

# B2: triangle 40,75,x
A, B, C = (30, 122), (212, 122), (150, 34)
cen = ((A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3)
inner = POLY([A, B, C]) + T(toward(A, cen, 0.28), "40°") + T(toward(B, cen, 0.24), "75°") + T(toward(C, cen, 0.32), "x°")
figs[("bronze", 2)] = SVG("0 0 240 150", "Triangle with angles 40 degrees, 75 degrees and x", inner) + CAP

# B3: angles at a point 90,145,x
V = (120, 88)
inner = "".join(LINE(V, pt(V, 70, a)) for a in (0, 90, 235))
inner += ARC(V, 30, 0, 90) + ARC(V, 34, 90, 235) + ARC(V, 30, 235, 360)
inner += T(pt(V, 40, 45), "90°") + T(pt(V, 42, 162), "145°") + T(pt(V, 40, 297), "x°")
figs[("bronze", 3)] = SVG("0 0 240 165", "Three angles meeting at a point, 90 degrees, 145 degrees and x", inner) + CAP

# B4: transversal + parallel lines, alternate 58, a, b
Pb = (95, 122); Pt = (95 + 75/math.tan(math.radians(58)), 47)
inner = LINE((28, 47), (212, 47)) + LINE((28, 122), (212, 122))
d = (Pt[0]-Pb[0], Pt[1]-Pb[1]); L = math.hypot(*d); u = (d[0]/L, d[1]/L)
inner += LINE((Pb[0]-u[0]*22, Pb[1]-u[1]*22), (Pt[0]+u[0]*22, Pt[1]+u[1]*22))
inner += chev(150, 47) + chev(150, 122)
inner += ARC(Pb, 26, 0, 58) + T(pt(Pb, 34, 29), "58°")
inner += T((Pt[0]-20, Pt[1]+15), "a") + T((Pt[0]+13, Pt[1]+17), "b")
figs[("bronze", 4)] = SVG("0 0 240 165", "A transversal crossing two parallel lines, with a 58 degree angle, angle a alternate to it, and angle b next to a", inner) + CAP

# B5: co-interior 110 and ? (transversal at true 70 deg -> interior 110 / 70 pair, same side)
Ttop = (122.4, 50); Tbot = (97.6, 118)
inner = LINE((28, 50), (212, 50)) + LINE((28, 118), (212, 118)) + chev(150, 50) + chev(150, 118)
inner += LINE((127.5, 35.9), (92.5, 132.1))
inner += ARC(Ttop, 24, 0, -110) + ARC(Tbot, 24, 0, 70)
inner += T(pt(Ttop, 30, 305), "110°") + T(pt(Tbot, 30, 35), "?")
figs[("bronze", 5)] = SVG("0 0 240 150", "Two parallel lines with a transversal, co-interior angles of 110 degrees and one marked with a question mark", inner) + CAP

# B6: isosceles, base 70/70, top ?
C, A, B = (120, 28), (50, 132), (190, 132)
inner = POLY([A, B, C]) + tickmarks(C, A) + tickmarks(C, B)
inner += T((72, 122), "70°") + T((168, 122), "70°") + T((120, 54), "?")
figs[("bronze", 6)] = SVG("0 0 240 155", "Isosceles triangle with two equal base angles of 70 degrees and the top angle marked with a question mark", inner) + CAP

# B7: quadrilateral 80,100,95,x
A, B, C, D = (40, 60), (200, 45), (210, 132), (55, 138)
cen = ((A[0]+B[0]+C[0]+D[0])/4, (A[1]+B[1]+C[1]+D[1])/4)
inner = POLY([A, B, C, D])
inner += T(toward(A, cen, 0.28), "80°") + T(toward(B, cen, 0.26), "100°") + T(toward(C, cen, 0.26), "95°") + T(toward(D, cen, 0.24), "x°")
figs[("bronze", 7)] = SVG("0 0 240 160", "Quadrilateral with angles 80 degrees, 100 degrees, 95 degrees and x", inner) + CAP

# ---------- SILVER ----------
def regpoly(n, V, r, rot=90):
    return [pt(V, r, rot + 360*i/n) for i in range(n)]

# S0: nonagon (9)
V = (120, 88)
figs[("silver", 0)] = SVG("0 0 240 175", "A regular nine-sided polygon (nonagon)", POLY(regpoly(9, V, 62, 90)))

# S1: regular hexagon, mark one interior ?
V = (120, 85); verts = regpoly(6, V, 60, 0)
vx = verts[1]; dirc = (V[0]-vx[0], V[1]-vx[1]); L = math.hypot(*dirc)
inner = POLY(verts) + T((vx[0]+dirc[0]/L*20, vx[1]+dirc[1]/L*20), "?")
figs[("silver", 1)] = SVG("0 0 240 175", "A regular hexagon with one interior angle marked with a question mark", inner)

# S3: interior 156, exterior ? at a vertex on a straight line
V = (120, 92)
inner = LINE((32, 92), V) + LINE(V, (210, 92), dash=True) + LINE(V, pt(V, 82, 24))
inner += ARC(V, 40, 24, 180) + ARC(V, 44, 0, 24)
inner += T(pt(V, 54, 102), "156°") + T(pt(V, 56, 12), "?")
figs[("silver", 3)] = SVG("0 0 240 130", "A vertex of a polygon with interior angle 156 degrees and exterior angle marked, on a straight line", inner)

# S4: triangle 3x,5x,44
A, B, C = (32, 126), (208, 126), (132, 34)
cen = ((A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3)
inner = POLY([A, B, C]) + T(toward(A, cen, 0.30), "3x°") + T(toward(B, cen, 0.26), "5x°") + T(toward(C, cen, 0.32), "44°")
figs[("silver", 4)] = SVG("0 0 240 155", "Triangle with angles 3x, 5x and 44 degrees", inner) + CAP

# S6: pentagon 100,110,120,130,x
P = [(120, 22), (206, 88), (172, 152), (68, 152), (34, 88)]
cen = (sum(p[0] for p in P)/5, sum(p[1] for p in P)/5)
inner = POLY(P)
for p, lb in zip(P, ["100°", "110°", "120°", "130°", "x°"]):
    inner += T(toward(p, cen, 0.30), lb, 10)
figs[("silver", 6)] = SVG("0 0 240 170", "Pentagon with angles 100, 110, 120, 130 degrees and x", inner) + CAP

# ---------- GOLD ----------
# G1: parallelogram (3x+10) and (2x+20) adjacent
A, B, C, D = (40, 122), (162, 122), (212, 46), (90, 46)
inner = POLY([A, B, C, D]) + T((58, 111), "(3x + 10)°", 10) + T((150, 111), "(2x + 20)°", 10)
figs[("gold", 1)] = SVG("0 0 240 150", "Parallelogram with two adjacent angles labelled (3x plus 10) degrees and (2x plus 20) degrees", inner) + CAP

# G3: square + regular hexagon sharing a side, gap ?
V = (110, 120)
sq = [(110, 120), (50, 120), (50, 60), (110, 60)]
hexv = [(110, 120), (110, 60), (162, 30), (214, 60), (214, 120), (162, 150)]
inner = POLY(sq, "#60a5fa", 0.28) + POLY(hexv, "#34d399", 0.28)
inner += T(pt(V, 30, 135), "90°", 10) + T(pt(V, 34, 30), "120°", 10) + T(pt(V, 33, 255), "?")
figs[("gold", 3)] = SVG("0 0 240 175", "A square and a regular hexagon sharing a side, with square angle 90 degrees, hexagon angle 120 degrees and the gap angle marked", inner)

# G4: exterior x, interior 4x, straight line
V = (120, 95)
inner = LINE((40, 95), V) + LINE(V, (212, 95), dash=True) + LINE(V, pt(V, 78, 36))
inner += ARC(V, 40, 36, 180) + ARC(V, 46, 0, 36)
inner += T(pt(V, 54, 108), "4x°", 10) + T(pt(V, 58, 18), "x°")
figs[("gold", 4)] = SVG("0 0 240 130", "A vertex on a straight line with interior angle 4x and exterior angle x", inner) + CAP

# ---------- inject into bank ----------
pb = pd["problem_bank"]
added = []
for (tier, idx), svg in figs.items():
    prob = pb[tier][idx]
    if "<svg" in prob["display"]:
        raise SystemExit("already svg %s %d" % (tier, idx))
    prob["display"] = svg + prob["display"]
    added.append((tier, idx))

# ---------- opener display ----------
V = (120, 92)
inner = LINE((26, 92), (214, 92)) + LINE(V, pt(V, 78, 120))
inner += ARC(V, 34, 0, 120) + ARC(V, 30, 120, 180)
inner += T(pt(V, 46, 60), "120°") + T(pt(V, 40, 150), "?")
pd["guided"]["opener"]["display"] = SVG("0 0 240 120", "Two angles on a straight line, one 120 degrees and the other marked with a question mark", inner) + CAP

# ---------- teach displays ----------
A, B, C = (30, 120), (210, 120), (145, 36)
cen = ((A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3)
inner = POLY([A, B, C]) + T(toward(A, cen, 0.28), "50°") + T(toward(B, cen, 0.26), "60°") + T(toward(C, cen, 0.32), "x°")
tb = SVG("0 0 240 150", "Triangle with angles 50 degrees, 60 degrees and x", inner) + CAP
pd["guided"]["teach"]["bronze"]["display"] = tb + pd["guided"]["teach"]["bronze"]["display"]

V = (120, 88); verts = regpoly(8, V, 60, 22.5)
vx = verts[0]; dirc = (V[0]-vx[0], V[1]-vx[1]); L = math.hypot(*dirc)
inner = POLY(verts) + T((vx[0]+dirc[0]/L*20, vx[1]+dirc[1]/L*20), "?")
ts = SVG("0 0 240 175", "A regular octagon with one interior angle marked with a question mark", inner)
pd["guided"]["teach"]["silver"]["display"] = ts + pd["guided"]["teach"]["silver"]["display"]

json.dump(pd, io.open("lesson_geometry-L01_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("bank figures:", len(added), added)
print("opener + teach set")
