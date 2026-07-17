# -*- coding: utf-8 -*-
"""Programmatic SVG figures for geometry-L07 (Circle Theorems), maths-ocr.
Every label is driven from the problem's own numbers. Theme-safe:
text + strokes use currentColor; region fills soft with fill-opacity.
"""
import math

def Pt(cx, cy, r, ang):
    a = math.radians(ang)
    return (cx + r * math.cos(a), cy - r * math.sin(a))

def n(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")

def circle(cx, cy, r):
    return '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="currentColor" stroke-width="1.5"/>' % (n(cx), n(cy), n(r))

def line(x1, y1, x2, y2, w="1.4", dash=""):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="%s"%s/>' % (n(x1), n(y1), n(x2), n(y2), w, d)

def dot(cx, cy, r=2.6):
    return '<circle cx="%s" cy="%s" r="%s" fill="currentColor"/>' % (n(cx), n(cy), n(r))

def txt(x, y, s, size=12, anchor="middle", weight="normal"):
    return '<text x="%s" y="%s" font-family="Inter, sans-serif" font-size="%d" text-anchor="%s" font-weight="%s" fill="currentColor">%s</text>' % (n(x), n(y), size, anchor, weight, s)

def arc(cx, cy, r, a1, a2, reflex=False):
    d = (a2 - a1 + 540) % 360 - 180
    if reflex:
        d = d - 360 if d > 0 else d + 360
    steps = max(3, int(abs(d) / 7))
    pts = []
    for i in range(steps + 1):
        ang = a1 + d * i / steps
        x, y = Pt(cx, cy, r, ang)
        pts.append("%s,%s" % (n(x), n(y)))
    return '<polyline points="%s" fill="none" stroke="currentColor" stroke-width="1.2"/>' % " ".join(pts)

def rasq(vx, vy, d1, d2, s=11):
    p1 = Pt(vx, vy, s, d1)
    p2 = Pt(vx, vy, s, d2)
    cxp = p1[0] + p2[0] - vx
    cyp = p1[1] + p2[1] - vy
    return '<polyline points="%s,%s %s,%s %s,%s" fill="none" stroke="currentColor" stroke-width="1.2"/>' % (
        n(p1[0]), n(p1[1]), n(cxp), n(cyp), n(p2[0]), n(p2[1]))

def ang_dir(fx, fy, tx, ty):
    return math.degrees(math.atan2(-(ty - fy), tx - fx))

def wrap(inner, label, w=240, h=210):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:250px;height:auto">%s</svg>'
            % (w, h, label, inner))

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---- figure builders ----

def fig_centre_circ(centre_label, circ_label, label):
    """Angle at centre and at circumference on the same chord AB, apex C on top."""
    cx, cy, r = 120, 118, 78
    A = Pt(cx, cy, r, 208); B = Pt(cx, cy, r, 332); C = Pt(cx, cy, r, 82)
    s = [circle(cx, cy, r)]
    s.append(line(cx, cy, A[0], A[1]))
    s.append(line(cx, cy, B[0], B[1]))
    s.append(line(C[0], C[1], A[0], A[1]))
    s.append(line(C[0], C[1], B[0], B[1]))
    s.append(dot(cx, cy)); s.append(dot(*A)); s.append(dot(*B)); s.append(dot(*C))
    s.append(txt(cx - 12, cy - 6, "O", 11, "end"))
    s.append(txt(A[0] - 8, A[1] + 4, "A", 11, "end"))
    s.append(txt(B[0] + 8, B[1] + 4, "B", 11, "start"))
    s.append(txt(C[0], C[1] - 8, "C", 11))
    # centre angle arc between OA and OB (downward)
    dOA = ang_dir(cx, cy, *A); dOB = ang_dir(cx, cy, *B)
    s.append(arc(cx, cy, 20, dOA, dOB))
    s.append(txt(cx, cy + 40, centre_label, 12))
    # circumference angle arc at C
    dCA = ang_dir(C[0], C[1], *A); dCB = ang_dir(C[0], C[1], *B)
    s.append(arc(C[0], C[1], 20, dCA, dCB))
    s.append(txt(C[0], C[1] + 26, circ_label, 12))
    return wrap("".join(s), label)

def fig_centre_reflex(centre_label, circ_label, label):
    """Reflex angle at centre; circumference angle on the minor arc side."""
    cx, cy, r = 120, 112, 76
    A = Pt(cx, cy, r, 200); B = Pt(cx, cy, r, 340); C = Pt(cx, cy, r, 270)
    s = [circle(cx, cy, r)]
    s.append(line(cx, cy, A[0], A[1]))
    s.append(line(cx, cy, B[0], B[1]))
    s.append(line(C[0], C[1], A[0], A[1]))
    s.append(line(C[0], C[1], B[0], B[1]))
    s.append(dot(cx, cy)); s.append(dot(*A)); s.append(dot(*B)); s.append(dot(*C))
    s.append(txt(cx + 12, cy - 4, "O", 11, "start"))
    s.append(txt(A[0] - 8, A[1], "A", 11, "end"))
    s.append(txt(B[0] + 8, B[1], "B", 11, "start"))
    s.append(txt(C[0], C[1] + 16, "C", 11))
    dOA = ang_dir(cx, cy, *A); dOB = ang_dir(cx, cy, *B)
    # reflex arc goes the long way (through top)
    s.append(arc(cx, cy, 24, dOA, dOB, reflex=True))
    s.append(txt(cx, cy - 34, centre_label, 12))
    dCA = ang_dir(C[0], C[1], *A); dCB = ang_dir(C[0], C[1], *B)
    s.append(arc(C[0], C[1], 18, dCA, dCB))
    s.append(txt(C[0], C[1] - 8, circ_label, 11))
    return wrap("".join(s), label)

def fig_semicircle(right_vertex, a_ang, ldiam, rdiam, apex_ang,
                   ra_label, other_at, other_label, ask_at, ask_label,
                   names, label):
    """Diameter horizontal; apex on circle. right_vertex = which point has 90.
    names: dict mapping 'L','R','T' -> letters for left-diam, right-diam, apex."""
    cx, cy, r = 120, 115, 78
    L = (cx - r, cy); R = (cx + r, cy)
    T = Pt(cx, cy, r, apex_ang)
    s = [circle(cx, cy, r)]
    s.append(line(L[0], L[1], R[0], R[1]))
    s.append(line(L[0], L[1], T[0], T[1]))
    s.append(line(R[0], R[1], T[0], T[1]))
    s.append(dot(*L)); s.append(dot(*R)); s.append(dot(*T))
    s.append(txt(L[0] - 8, L[1] + 4, names["L"], 11, "end"))
    s.append(txt(R[0] + 8, R[1] + 4, names["R"], 11, "start"))
    s.append(txt(T[0], T[1] - 8, names["T"], 11))
    # right angle marker at apex T
    if right_vertex == "T":
        dTL = ang_dir(T[0], T[1], *L); dTR = ang_dir(T[0], T[1], *R)
        s.append(rasq(T[0], T[1], dTL, dTR))
    elif right_vertex == "Lapex":
        pass
    return cx, cy, r, L, R, T, s

def fig_semi_full(cfg, label):
    """cfg is a dict describing a semicircle triangle figure."""
    cx, cy, r = 120, 115, 78
    L = (cx - r, cy); R = (cx + r, cy)
    T = Pt(cx, cy, r, cfg["apex"])
    pts = {"L": L, "R": R, "T": T}
    s = [circle(cx, cy, r)]
    s.append(line(L[0], L[1], R[0], R[1]))
    s.append(line(L[0], L[1], T[0], T[1]))
    s.append(line(R[0], R[1], T[0], T[1]))
    s.append(dot(*L)); s.append(dot(*R)); s.append(dot(*T))
    s.append(txt(L[0] - 8, L[1] + 4, cfg["names"]["L"], 11, "end"))
    s.append(txt(R[0] + 8, R[1] + 4, cfg["names"]["R"], 11, "start"))
    s.append(txt(T[0], T[1] - 8, cfg["names"]["T"], 11))
    for vert, lab, is_ra in cfg["marks"]:
        v = pts[vert]
        others = [pts[o] for o in ("L", "R", "T") if o != vert]
        d1 = ang_dir(v[0], v[1], *others[0]); d2 = ang_dir(v[0], v[1], *others[1])
        if is_ra:
            s.append(rasq(v[0], v[1], d1, d2))
            lx, ly = Pt(v[0], v[1], 24, (d1 + d2) / 2.0)
            if lab:
                s.append(txt(lx, ly + 4, lab, 11))
        else:
            s.append(arc(v[0], v[1], 17, d1, d2))
            lx, ly = Pt(v[0], v[1], 30, (d1 + d2) / 2.0)
            s.append(txt(lx, ly + 4, lab, 11))
    return wrap("".join(s), label)

def fig_tangent_radius(centre_ang_label, ask_label, label):
    """Tangent at T (bottom), radius OT, external point P; triangle OTP."""
    cx, cy, r = 108, 100, 66
    T = (cx, cy + r)  # bottom
    P = (cx + 96, cy + r)
    s = [circle(cx, cy, r)]
    s.append(line(cx - 62, T[1], cx + 116, T[1], "1.4"))  # tangent line
    s.append(line(cx, cy, T[0], T[1]))  # radius
    s.append(line(cx, cy, P[0], P[1]))  # O to P
    s.append(dot(cx, cy)); s.append(dot(*T)); s.append(dot(*P))
    s.append(txt(cx - 9, cy, "O", 11, "end"))
    s.append(txt(T[0] - 6, T[1] + 15, "T", 11, "end"))
    s.append(txt(P[0] + 6, P[1] + 4, "P", 11, "start"))
    # right angle at T between TO and TP
    dTO = ang_dir(T[0], T[1], cx, cy); dTP = ang_dir(T[0], T[1], *P)
    s.append(rasq(T[0], T[1], dTO, dTP))
    # angle at O
    dOT = ang_dir(cx, cy, T[0], T[1]); dOP = ang_dir(cx, cy, *P)
    s.append(arc(cx, cy, 20, dOT, dOP))
    lx, ly = Pt(cx, cy, 34, (dOT + dOP) / 2.0)
    s.append(txt(lx, ly + 4, centre_ang_label, 11))
    # angle at P
    dPO = ang_dir(P[0], P[1], cx, cy); dPT = ang_dir(P[0], P[1], T[0], T[1])
    s.append(arc(P[0], P[1], 20, dPO, dPT))
    lx, ly = Pt(P[0], P[1], 34, (dPO + dPT) / 2.0)
    s.append(txt(lx, ly + 4, ask_label, 11))
    return wrap("".join(s), label)

def fig_tangent_only(label):
    """A tangent meeting a radius, pure fact (unused now)."""
    return ""

def fig_alt_segment(tc_label, ask_label, label):
    """Tangent at T (bottom), chord TA, point B on major arc, angle TBA."""
    cx, cy, r = 120, 112, 76
    T = Pt(cx, cy, r, 270)
    A = Pt(cx, cy, r, 25)
    B = Pt(cx, cy, r, 150)
    s = [circle(cx, cy, r)]
    s.append(line(cx - 66, T[1], cx + 66, T[1], "1.4"))  # tangent
    s.append(line(T[0], T[1], A[0], A[1]))  # chord TA
    s.append(line(B[0], B[1], T[0], T[1]))
    s.append(line(B[0], B[1], A[0], A[1]))
    s.append(dot(*T)); s.append(dot(*A)); s.append(dot(*B))
    s.append(txt(T[0], T[1] + 16, "T", 11))
    s.append(txt(A[0] + 8, A[1], "A", 11, "start"))
    s.append(txt(B[0] - 8, B[1], "B", 11, "end"))
    # angle between tangent (pointing right, dir 0) and chord TA
    dTtan = 0.0
    dTA = ang_dir(T[0], T[1], *A)
    s.append(arc(T[0], T[1], 22, dTtan, dTA))
    lx, ly = Pt(T[0], T[1], 40, (dTtan + dTA) / 2.0)
    s.append(txt(lx + 4, ly, tc_label, 11, "start"))
    # angle at B (TBA)
    dBT = ang_dir(B[0], B[1], *T); dBA = ang_dir(B[0], B[1], *A)
    s.append(arc(B[0], B[1], 20, dBT, dBA))
    lx, ly = Pt(B[0], B[1], 32, (dBT + dBA) / 2.0)
    s.append(txt(lx, ly + 4, ask_label, 11))
    return wrap("".join(s), label)

def fig_two_tangents(mode, label):
    """Two tangents from external point P touching at A (upper) and B (lower).
    mode 'angle': show 70 half-angle and ? full. mode 'length': PA=8, PB=?"""
    cx, cy, r = 96, 110, 62
    P = (cx + 132, cy)
    A = Pt(cx, cy, r, 46)
    B = Pt(cx, cy, r, 314)
    s = [circle(cx, cy, r)]
    s.append(line(P[0], P[1], A[0], A[1]))
    s.append(line(P[0], P[1], B[0], B[1]))
    s.append(line(cx, cy, A[0], A[1]))  # radii
    s.append(line(cx, cy, B[0], B[1]))
    s.append(line(cx, cy, P[0], P[1], "1.1", "3 3"))  # line to centre
    s.append(dot(cx, cy)); s.append(dot(*A)); s.append(dot(*B)); s.append(dot(*P))
    s.append(txt(cx - 9, cy + 4, "O", 11, "end"))
    s.append(txt(A[0] - 4, A[1] - 6, "A", 11, "end"))
    s.append(txt(B[0] - 4, B[1] + 12, "B", 11, "end"))
    s.append(txt(P[0] + 6, P[1] + 4, "P", 11, "start"))
    # right angles at A and B
    dAO = ang_dir(A[0], A[1], cx, cy); dAP = ang_dir(A[0], A[1], *P)
    s.append(rasq(A[0], A[1], dAO, dAP, 9))
    dBO = ang_dir(B[0], B[1], cx, cy); dBP = ang_dir(B[0], B[1], *P)
    s.append(rasq(B[0], B[1], dBO, dBP, 9))
    if mode == "angle":
        dPA = ang_dir(P[0], P[1], *A); dPO = ang_dir(P[0], P[1], cx, cy)
        s.append(arc(P[0], P[1], 26, dPA, dPO))
        lx, ly = Pt(P[0], P[1], 42, (dPA + dPO) / 2.0)
        s.append(txt(lx, ly, "70°", 11, "end"))
        dPB = ang_dir(P[0], P[1], *B)
        s.append(arc(P[0], P[1], 15, dPA, dPB))
        s.append(txt(P[0] - 20, P[1] + 4, "?", 12, "end"))
    else:
        mA = ((P[0] + A[0]) / 2.0, (P[1] + A[1]) / 2.0)
        mB = ((P[0] + B[0]) / 2.0, (P[1] + B[1]) / 2.0)
        s.append(txt(mA[0], mA[1] - 6, "8 cm", 11))
        s.append(txt(mB[0], mB[1] + 12, "?", 12))
    return wrap("".join(s), label)

def fig_cyclic_quad(labels, label):
    """Cyclic quad ABCD with angle labels at each vertex (labels dict A/B/C/D)."""
    cx, cy, r = 120, 112, 78
    ang = {"A": 118, "B": 42, "C": 312, "D": 218}
    Pmap = {k: Pt(cx, cy, r, v) for k, v in ang.items()}
    order = ["A", "B", "C", "D"]
    s = [circle(cx, cy, r)]
    for i in range(4):
        p = Pmap[order[i]]; q = Pmap[order[(i + 1) % 4]]
        s.append(line(p[0], p[1], q[0], q[1]))
    for k in order:
        p = Pmap[k]
        s.append(dot(*p))
        off = {"A": (-8, -4), "B": (8, -4), "C": (8, 10), "D": (-8, 10)}[k]
        s.append(txt(p[0] + off[0], p[1] + off[1], k, 11, "middle"))
    for k, lab in labels.items():
        if not lab:
            continue
        p = Pmap[k]
        dx, dy = cx - p[0], cy - p[1]
        L = math.hypot(dx, dy)
        px, py = p[0] + dx / L * 26, p[1] + dy / L * 26
        s.append(txt(px, py + 4, lab, 11))
    return wrap("".join(s), label)

def fig_same_segment(known_label, ask_label, label):
    """Chord AB; two apexes C, D on major arc; equal angles in same segment."""
    cx, cy, r = 120, 116, 78
    A = Pt(cx, cy, r, 214); B = Pt(cx, cy, r, 326)
    C = Pt(cx, cy, r, 112); D = Pt(cx, cy, r, 68)
    s = [circle(cx, cy, r)]
    s.append(line(A[0], A[1], B[0], B[1]))
    for X in (C, D):
        s.append(line(X[0], X[1], A[0], A[1]))
        s.append(line(X[0], X[1], B[0], B[1]))
    for nm, X in (("A", A), ("B", B), ("C", C), ("D", D)):
        s.append(dot(*X))
    s.append(txt(A[0] - 8, A[1] + 4, "A", 11, "end"))
    s.append(txt(B[0] + 8, B[1] + 4, "B", 11, "start"))
    s.append(txt(C[0] - 8, C[1] - 4, "C", 11, "end"))
    s.append(txt(D[0] + 8, D[1] - 4, "D", 11, "start"))
    for X, lab in ((C, known_label), (D, ask_label)):
        dXA = ang_dir(X[0], X[1], *A); dXB = ang_dir(X[0], X[1], *B)
        s.append(arc(X[0], X[1], 18, dXA, dXB))
        lx, ly = Pt(X[0], X[1], 30, (dXA + dXB) / 2.0)
        s.append(txt(lx, ly + 4, lab, 11))
    return wrap("".join(s), label)

def _seg_intersect(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

def fig_intersecting_chords_custom(la, lb, lc, ld, label):
    """Chords AB and CD cross at P inside; segment labels supplied."""
    cx, cy, r = 120, 112, 80
    A = Pt(cx, cy, r, 165); B = Pt(cx, cy, r, 350)
    C = Pt(cx, cy, r, 65); D = Pt(cx, cy, r, 245)
    P = _seg_intersect(A, B, C, D)
    s = [circle(cx, cy, r)]
    s.append(line(A[0], A[1], B[0], B[1]))
    s.append(line(C[0], C[1], D[0], D[1]))
    s.append(dot(*A)); s.append(dot(*B)); s.append(dot(*C)); s.append(dot(*D)); s.append(dot(*P))
    s.append(txt(A[0] - 8, A[1], "A", 11, "end"))
    s.append(txt(B[0] + 8, B[1] + 4, "B", 11, "start"))
    s.append(txt(C[0] + 8, C[1] - 2, "C", 11, "start"))
    s.append(txt(D[0] - 8, D[1] + 10, "D", 11, "end"))
    s.append(txt(P[0] + 6, P[1] - 5, "P", 11, "start"))

    def mid(u, v, f=0.5):
        return (u[0] + (v[0] - u[0]) * f, u[1] + (v[1] - u[1]) * f)
    for X, lab in ((A, la), (B, lb), (C, lc), (D, ld)):
        m = mid(P, X, 0.5)
        s.append(txt(m[0], m[1] - 3, lab, 11))
    return wrap("".join(s), label)

def fig_intersecting_chords(label):
    """Chords AB and CD cross at P inside; PA=3,PB=8,PC=4,PD=?"""
    return fig_intersecting_chords_custom("3", "8", "4", "?", label)

def _fig_intersecting_chords_old(label):
    cx, cy, r = 120, 112, 80
    A = Pt(cx, cy, r, 165); B = Pt(cx, cy, r, 350)
    C = Pt(cx, cy, r, 65); D = Pt(cx, cy, r, 245)
    P = _seg_intersect(A, B, C, D)
    s = [circle(cx, cy, r)]
    s.append(line(A[0], A[1], B[0], B[1]))
    s.append(line(C[0], C[1], D[0], D[1]))
    s.append(dot(*A)); s.append(dot(*B)); s.append(dot(*C)); s.append(dot(*D)); s.append(dot(*P))
    s.append(txt(A[0] - 8, A[1], "A", 11, "end"))
    s.append(txt(B[0] + 8, B[1] + 4, "B", 11, "start"))
    s.append(txt(C[0] + 8, C[1] - 2, "C", 11, "start"))
    s.append(txt(D[0] - 8, D[1] + 10, "D", 11, "end"))
    s.append(txt(P[0] + 6, P[1] - 5, "P", 11, "start"))

    def mid(u, v, f=0.5):
        return (u[0] + (v[0] - u[0]) * f, u[1] + (v[1] - u[1]) * f)
    for X, lab in ((A, "3"), (B, "8"), (C, "4"), (D, "?")):
        m = mid(P, X, 0.5)
        s.append(txt(m[0], m[1] - 3, lab, 11))
    return wrap("".join(s), label)

def fig_tangent_secant(label):
    """Tangent PT and secant PAB from external point P; PT=12, PA=8, PB=?"""
    cx, cy, r = 150, 108, 62
    P = (28, 150)
    T = Pt(cx, cy, r, 232)  # tangent point lower-left
    # secant through A (near) and B (far)
    A = Pt(cx, cy, r, 200); B = Pt(cx, cy, r, 38)
    s = [circle(cx, cy, r)]
    s.append(line(P[0], P[1], T[0], T[1]))       # tangent
    s.append(line(P[0], P[1], B[0], B[1]))       # secant (through A to B)
    s.append(dot(*P)); s.append(dot(*T)); s.append(dot(*A)); s.append(dot(*B))
    s.append(txt(P[0] - 4, P[1] + 12, "P", 11, "end"))
    s.append(txt(T[0] - 6, T[1] + 6, "T", 11, "end"))
    s.append(txt(A[0] - 6, A[1] + 12, "A", 11, "end"))
    s.append(txt(B[0] + 8, B[1], "B", 11, "start"))

    def mid(u, v, f=0.5):
        return (u[0] + (v[0] - u[0]) * f, u[1] + (v[1] - u[1]) * f)
    mT = mid(P, T, 0.5); s.append(txt(mT[0] - 4, mT[1] - 4, "12", 11, "end"))
    mA = mid(P, A, 0.55); s.append(txt(mA[0], mA[1] - 5, "8", 11))
    mB = mid(P, B, 0.82); s.append(txt(mB[0], mB[1] - 5, "?", 11))
    return wrap("".join(s), label)

if __name__ == "__main__":
    # smoke test: emit one of each and check validator-relevant props
    outs = {
        "centre_circ": fig_centre_circ("100°", "?", "Angle at the centre 100 degrees, angle at circumference marked with a question mark"),
        "reflex": fig_centre_reflex("260°", "?", "Reflex angle at the centre 260 degrees"),
        "tangent_radius": fig_tangent_radius("55°", "?", "Tangent meets radius at T, right angle, angle at O is 55"),
        "alt_seg": fig_alt_segment("55°", "?", "Tangent chord angle 55 degrees, alternate segment"),
        "two_tan_angle": fig_two_tangents("angle", "Two tangents from P"),
        "two_tan_len": fig_two_tangents("length", "Two tangents from P, PA 8 cm"),
        "cyclic": fig_cyclic_quad({"A": "80°", "C": "?"}, "Cyclic quadrilateral"),
        "same_seg": fig_same_segment("42°", "?", "Same segment"),
        "chords": fig_intersecting_chords("Intersecting chords"),
        "secant": fig_tangent_secant("Tangent and secant"),
        "semi": fig_semi_full({"apex": 70, "names": {"L": "A", "R": "B", "T": "C"},
                               "marks": [("T", "", True), ("L", "55°", False)]}, "Semicircle"),
    }
    for k, v in outs.items():
        bad = ("http" in v.lower()) or ("xlink" in v.lower())
        print(k, len(v), "OK" if ("viewBox" in v and 'role="img"' in v and "aria-label" in v and not bad) else "PROBLEM")
