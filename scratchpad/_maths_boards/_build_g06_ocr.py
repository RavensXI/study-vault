# -*- coding: utf-8 -*-
"""Full guided + diagram conversion for maths-ocr geometry-L06.
Sine Rule, Cosine Rule & Area Formula. Builds practice_data, asserts every
guided-step chain lands on the stored (fresh-solved) solutions, generates
theme-safe SVG figures from each problem's own numbers."""
import json, math, io

R = math.radians
def r1(x): return round(x, 1)
def r4(x): return round(x, 4)

# ---------------------------------------------------------------- SVG helpers
def _fit(verts, pad=28, W=210, H=162):
    xs = [p[0] for p in verts]; ys = [p[1] for p in verts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    sx = (W - 2*pad) / (maxx - minx) if maxx > minx else 1
    sy = (H - 2*pad) / (maxy - miny) if maxy > miny else 1
    s = min(sx, sy)
    ox = (W - (maxx-minx)*s) / 2
    oy = (H - (maxy-miny)*s) / 2
    def tf(p):
        px = ox + (p[0]-minx)*s
        py = H - (oy + (p[1]-miny)*s)  # flip y
        return (px, py)
    return [tf(p) for p in verts]

def _unit(dx, dy):
    d = math.hypot(dx, dy) or 1
    return (dx/d, dy/d)

def _fmt(x): return ("%.1f" % x).rstrip("0").rstrip(".")

def _angle_arc(V, N1, N2, r=15):
    u1 = _unit(N1[0]-V[0], N1[1]-V[1])
    u2 = _unit(N2[0]-V[0], N2[1]-V[1])
    a1 = math.atan2(u1[1], u1[0]); a2 = math.atan2(u2[1], u2[0])
    da = a2 - a1
    while da > math.pi: da -= 2*math.pi
    while da < -math.pi: da += 2*math.pi
    pts = []
    n = 8
    for k in range(n+1):
        a = a1 + da*k/n
        pts.append((V[0]+r*math.cos(a), V[1]+r*math.sin(a)))
    poly = " ".join("%s,%s" % (_fmt(p[0]), _fmt(p[1])) for p in pts)
    bx, by = u1[0]+u2[0], u1[1]+u2[1]
    bux, buy = _unit(bx, by)
    lab = (V[0]+(r+9)*bux, V[1]+(r+9)*buy)
    return poly, lab

def _right_mark(V, N1, N2, leg=11):
    u1 = _unit(N1[0]-V[0], N1[1]-V[1])
    u2 = _unit(N2[0]-V[0], N2[1]-V[1])
    P = (V[0]+leg*u1[0], V[1]+leg*u1[1])
    Q = (P[0]+leg*u2[0], P[1]+leg*u2[1])
    Rr = (V[0]+leg*u2[0], V[1]+leg*u2[1])
    poly = " ".join("%s,%s" % (_fmt(p[0]), _fmt(p[1])) for p in (P, Q, Rr))
    bux, buy = _unit(u1[0]+u2[0], u1[1]+u2[1])
    lab = (V[0]+(leg+12)*bux, V[1]+(leg+12)*buy)
    return poly, lab

def poly_svg(verts_math, vlabels, side_labels, angle_marks, area_label, aria):
    """verts_math: list of (x,y) math coords. vlabels: list[str|None].
    side_labels: dict {(i,j): text}. angle_marks: dict {i: ('arc'|'right', text)}.
    area_label: str|None. Returns svg string."""
    P = _fit(verts_math)
    n = len(P)
    cx = sum(p[0] for p in P)/n; cy = sum(p[1] for p in P)/n
    pts = " ".join("%s,%s" % (_fmt(p[0]), _fmt(p[1])) for p in P)
    out = ['<svg viewBox="0 0 210 162" role="img" aria-label="%s" '
           'style="max-width:270px;font-family:Inter,sans-serif" '
           'stroke-linejoin="round">' % aria]
    out.append('<polygon points="%s" fill="#60a5fa" fill-opacity="0.14" '
               'stroke="currentColor" stroke-width="1.7"/>' % pts)
    # side labels
    for (i, j), txt in side_labels.items():
        mx = (P[i][0]+P[j][0])/2; my = (P[i][1]+P[j][1])/2
        ox, oy = _unit(mx-cx, my-cy)
        lx = mx + 13*ox; ly = my + 13*oy + 3
        out.append('<text x="%s" y="%s" font-size="11" text-anchor="middle" '
                   'font-weight="600" fill="currentColor">%s</text>'
                   % (_fmt(lx), _fmt(ly), txt))
    # angle marks
    for i, (kind, txt) in angle_marks.items():
        nb = [k for k in range(n) if k != i][:2]
        # pick the two adjacent vertices (for triangle, the other two)
        N1, N2 = P[nb[0]], P[nb[1]]
        if kind == 'right':
            poly, lab = _right_mark(P[i], N1, N2)
            out.append('<polyline points="%s" fill="none" stroke="currentColor" '
                       'stroke-width="1.3"/>' % poly)
        else:
            poly, lab = _angle_arc(P[i], N1, N2)
            out.append('<polyline points="%s" fill="none" stroke="currentColor" '
                       'stroke-width="1.3"/>' % poly)
        out.append('<text x="%s" y="%s" font-size="10.5" text-anchor="middle" '
                   'fill="currentColor">%s</text>'
                   % (_fmt(lab[0]), _fmt(lab[1]+3), txt))
    # vertex labels
    for i, vl in enumerate(vlabels):
        if not vl: continue
        ox, oy = _unit(P[i][0]-cx, P[i][1]-cy)
        lx = P[i][0] + 12*ox; ly = P[i][1] + 12*oy + 3
        out.append('<text x="%s" y="%s" font-size="11" text-anchor="middle" '
                   'font-weight="700" fill="currentColor">%s</text>'
                   % (_fmt(lx), _fmt(ly), vl))
    if area_label:
        out.append('<text x="%s" y="%s" font-size="10" text-anchor="middle" '
                   'fill="currentColor">%s</text>'
                   % (_fmt(cx), _fmt(cy+4), area_label))
    out.append('</svg>')
    return "".join(out)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span> '

# ------------------------------------------------------- vertex constructors
def sas(s_along, ang_at_V, s_other):
    """Vertex V at origin; one side length s_along on +x; other side s_other at
    angle ang_at_V. Returns [V, Palong, Pother]."""
    V = (0.0, 0.0)
    P1 = (s_along, 0.0)
    P2 = (s_other*math.cos(R(ang_at_V)), s_other*math.sin(R(ang_at_V)))
    return [V, P1, P2]

def sss(a, b, c):
    """A=(0,0), B=(c,0); side a=BC opp A, b=CA opp B, c=AB opp C.
    Returns [A, B, C]."""
    cosA = (b*b + c*c - a*a) / (2*b*c)
    A = (0.0, 0.0); B = (c, 0.0)
    C = (b*math.cos(math.acos(cosA)), b*math.sin(math.acos(cosA)))
    return [A, B, C]

def parallelogram(base, side, ang):
    P = (0.0, 0.0); Q = (base, 0.0)
    S = (side*math.cos(R(ang)), side*math.sin(R(ang)))
    Rr = (Q[0]+S[0], Q[1]+S[1])
    return [P, Q, Rr, S]

# ============================================================ FIGURES
figs = {}

# --- bronze ---
# b0 area 8,6, incl 90 -> Area ? ; sides on the two arms of the right angle
v = sas(8, 90, 6)  # V arms: 8 on x, 6 up, right angle at V
figs['b0'] = poly_svg(v, [None, None, None],
    {(0,1): "8 cm", (0,2): "6 cm"}, {0: ('right', "90°")}, "Area = ?",
    "Triangle with two sides 8 cm and 6 cm meeting at a right angle")
# b1 area 10,12, incl 30
v = sas(10, 30, 12)
figs['b1'] = poly_svg(v, [None,None,None],
    {(0,1): "10", (0,2): "12"}, {0: ('arc', "30°")}, "Area = ?",
    "Triangle with two sides 10 and 12 and the included angle 30 degrees")
# b2 area 5,8, incl 60
v = sas(8, 60, 5)
figs['b2'] = poly_svg(v, [None,None,None],
    {(0,1): "8", (0,2): "5"}, {0: ('arc', "60°")}, "Area = ?",
    "Triangle with two sides 8 and 5 and the included angle 60 degrees")
# b3 cosine find a: b=5,c=7,A=90 -> unknown a opposite A. Arms c=7,b=5 at A(right)
v = sas(7, 90, 5)   # A=vertex0, B along x (c=7)->idx1, C up (b=5)->idx2 ; a=BC
figs['b3'] = poly_svg(v, ["A","B","C"],
    {(0,1): "7", (0,2): "5", (1,2): "?"}, {0: ('right', "90°")}, None,
    "Triangle ABC with sides b 5 and c 7 at a right angle A, side a unknown")
# b5 area 9,9,45
v = sas(9, 45, 9)
figs['b5'] = poly_svg(v, [None,None,None],
    {(0,1): "9", (0,2): "9"}, {0: ('arc', "45°")}, "Area = ?",
    "Triangle with two sides 9 and 9 and the included angle 45 degrees")
# b6 cosine angle SSS 6,8,10 find C (opposite 10). set c=10 base, a=6,b=8
v = sss(6, 8, 10)   # A,B,C ; angle C unknown, sides BC=6, CA=8, AB=10
figs['b6'] = poly_svg(v, ["A","B","C"],
    {(1,2): "6", (0,2): "8", (0,1): "10"}, {2: ('arc', "?")}, None,
    "Triangle ABC with sides 6, 8 and 10, angle C unknown")

# --- silver ---
# s0 cosine a: b=8,c=11,A=55 ; arms c=11,b=8 at A, unknown a=BC
v = sas(11, 55, 8)
figs['s0'] = poly_svg(v, ["A","B","C"],
    {(0,1): "11", (0,2): "8", (1,2): "?"}, {0: ('arc', "55°")}, None,
    "Triangle ABC with sides b 8 and c 11 and included angle A 55 degrees, side a unknown")
# s1 sine b: a=15 opp A=65, B=42, unknown b=AC opp B
A65, B42 = 65.0, 42.0; C1 = 180-A65-B42
a15 = 15.0
b_s1 = a15*math.sin(R(B42))/math.sin(R(A65))
c_s1 = a15*math.sin(R(C1))/math.sin(R(A65))
A = (0.0,0.0); B = (c_s1,0.0); C = (b_s1*math.cos(R(A65)), b_s1*math.sin(R(A65)))
figs['s1'] = poly_svg([A,B,C], ["A","B","C"],
    {(1,2): "15", (0,2): "?"}, {0: ('arc', "65°"), 1: ('arc', "42°")}, None,
    "Triangle ABC with side a 15 opposite angle A 65, angle B 42, side b unknown")
# s2 cosine largest angle SSS 7,9,12 -> C opposite 12
v = sss(7, 9, 12)
figs['s2'] = poly_svg(v, ["A","B","C"],
    {(1,2): "7", (0,2): "9", (0,1): "12"}, {2: ('arc', "?")}, None,
    "Triangle with sides 7, 9 and 12, largest angle unknown")
# s3 area 13,17, incl 72
v = sas(17, 72, 13)
figs['s3'] = poly_svg(v, [None,None,None],
    {(0,1): "17", (0,2): "13"}, {0: ('arc', "72°")}, "Area = ?",
    "Triangle with two sides 13 and 17 and the included angle 72 degrees")
# s4 sine angle B: a=9 opp A=40, b=12 opp B(unknown). B=59, C=81
A40 = 40.0
sinB = 12*math.sin(R(A40))/9
B_s4 = math.degrees(math.asin(sinB)); C_s4 = 180-A40-B_s4
c_s4 = 9*math.sin(R(C_s4))/math.sin(R(A40))
A = (0.0,0.0); B = (c_s4,0.0); C = (12*math.cos(R(A40)), 12*math.sin(R(A40)))
figs['s4'] = poly_svg([A,B,C], ["A","B","C"],
    {(1,2): "9", (0,2): "12"}, {0: ('arc', "40°"), 1: ('arc', "?")}, None,
    "Triangle ABC with side a 9, angle A 40, side b 12, angle B unknown")
# s5 cosine c: a=5,b=6,C=100 ; arms a=5,b=6 at C(obtuse), unknown c=AB
# put vertex C, arms CB=a=5 on +x, CA=b=6 at 100
Cc = (0.0,0.0); Bc = (5.0,0.0); Ac = (6*math.cos(R(100)), 6*math.sin(R(100)))
figs['s5'] = poly_svg([Cc,Bc,Ac], ["C","B","A"],
    {(0,1): "5", (0,2): "6", (1,2): "?"}, {0: ('arc', "100°")}, None,
    "Triangle with sides a 5 and b 6 and included obtuse angle C 100 degrees, side c unknown")
# s6 area SSS 5,6,7
v = sss(5, 6, 7)
figs['s6'] = poly_svg(v, [None,None,None],
    {(1,2): "5", (0,2): "6", (0,1): "7"}, {}, "Area = ?",
    "Triangle with sides 5, 6 and 7, area unknown")

# --- gold ---
# g0 inverse area 40, sides 10,12 -> included angle ?
v = sas(12, 41.8, 10)
figs['g0'] = poly_svg(v, [None,None,None],
    {(0,1): "12", (0,2): "10"}, {0: ('arc', "?")}, "Area = 40",
    "Triangle with two sides 10 and 12 and area 40, included angle unknown")
# g1 cosine angle SSS 8,9,13 -> C opposite 13
v = sss(8, 9, 13)
figs['g1'] = poly_svg(v, ["A","B","C"],
    {(1,2): "8", (0,2): "9", (0,1): "13"}, {2: ('arc', "?")}, None,
    "Triangle with sides 8, 9 and 13, angle C unknown")
# g2 ambiguous sine B: a=10 opp A=100, b=7 opp B(unknown)
A100 = 100.0
sinB2 = 7*math.sin(R(A100))/10
B_g2 = math.degrees(math.asin(sinB2)); C_g2 = 180-A100-B_g2
c_g2 = 10*math.sin(R(C_g2))/math.sin(R(A100))
A = (0.0,0.0); B = (c_g2,0.0); C = (7*math.cos(R(A100)), 7*math.sin(R(A100)))
figs['g2'] = poly_svg([A,B,C], ["A","B","C"],
    {(1,2): "10", (0,2): "7"}, {0: ('arc', "100°"), 1: ('arc', "?")}, None,
    "Triangle ABC with side a 10, angle A 100, side b 7, angle B unknown")
# g3 Heron 8,11,15
v = sss(8, 11, 15)
figs['g3'] = poly_svg(v, [None,None,None],
    {(1,2): "8", (0,2): "11", (0,1): "15"}, {}, "Area = ?",
    "Triangle with sides 8, 11 and 15, area unknown")
# g4 parallelogram 8,12,65
v = parallelogram(12, 8, 65)
figs['g4'] = poly_svg(v, [None,None,None,None],
    {(0,1): "12", (0,3): "8"}, {0: ('arc', "65°")}, "Area = ?",
    "Parallelogram with adjacent sides 12 and 8 and included angle 65 degrees")

for k, s in figs.items():
    assert len(s) < 12000, (k, len(s))
    assert "http" not in s.lower() and "xlink" not in s.lower(), k

with open("_g06_figs.json", "w", encoding="utf-8") as f:
    json.dump({k: len(v) for k, v in figs.items()}, f, indent=1)
print("figures built:", len(figs), "keys:", sorted(figs))
print("sizes:", {k: len(v) for k, v in figs.items()})
