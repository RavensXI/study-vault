# -*- coding: utf-8 -*-
"""Rebuild the two defective circle-theorem figures on geometry-L07.
gold[1]: inscribed 28 deg (major-arc vertex) -> 152 (minor-arc vertex).
silver[5]: central 110 deg (minor arc) -> 125 (major-arc angle = vertex on minor arc).
Figures are drawn so the DRAWN angle matches the numbers and ? marks the asked value."""
import json, io, math

def u(v):
    m = math.hypot(*v); return (v[0]/m, v[1]/m)

def angle_arc(V, P1, P2, ar):
    """Arc path string spanning the interior angle P1-V-P2, radius ar, at vertex V.
    Chooses sweep so the arc bulges through the interior (bisector) side."""
    u1 = u((P1[0]-V[0], P1[1]-V[1]))
    u2 = u((P2[0]-V[0], P2[1]-V[1]))
    s = (V[0]+ar*u1[0], V[1]+ar*u1[1])
    e = (V[0]+ar*u2[0], V[1]+ar*u2[1])
    a1 = math.atan2(u1[1], u1[0]); a2 = math.atan2(u2[1], u2[0])
    # interior angle
    d = abs(a2-a1); d = min(d, 2*math.pi-d)
    large = 1 if d > math.pi else 0
    # bisector direction (interior)
    bis = u((u1[0]+u2[0], u1[1]+u2[1]))
    # for each sweep flag, arc midpoint direction from V; pick the one aligned with bisector
    best = 0; bestdot = -9
    for sw in (0, 1):
        # midpoint of circular arc from a1 to a2 in SVG sweep sw (sw=1 => positive/CW in y-down)
        # go from a1 toward a2; sweep=1 increases angle
        span = (a2 - a1)
        if sw == 1:
            while span < 0: span += 2*math.pi
        else:
            while span > 0: span -= 2*math.pi
        am = a1 + span/2.0
        md = (math.cos(am), math.sin(am))
        dot = md[0]*bis[0] + md[1]*bis[1]
        if dot > bestdot: bestdot = dot; best = sw
    return "M%.2f %.2f A%d %d 0 %d %d %.2f %.2f" % (s[0], s[1], ar, ar, large, best, e[0], e[1])

def drawn_angle(V, P1, P2):
    a = (P1[0]-V[0], P1[1]-V[1]); b = (P2[0]-V[0], P2[1]-V[1])
    cfor = (a[0]*b[0]+a[1]*b[1])/(math.hypot(*a)*math.hypot(*b))
    return math.degrees(math.acos(max(-1,min(1,cor if False else cfor if False else cor if False else cfor)))) if False else math.degrees(math.acos(max(-1,min(1,cfor if False else (a[0]*b[0]+a[1]*b[1])/(math.hypot(*a)*math.hypot(*b))))))

def dang(V, P1, P2):
    a = (P1[0]-V[0], P1[1]-V[1]); b = (P2[0]-V[0], P2[1]-V[1])
    c = (a[0]*b[0]+a[1]*b[1])/(math.hypot(*a)*math.hypot(*b))
    return math.degrees(math.acos(max(-1,min(1,c))))

def T(x, y, s, size=11, anchor="middle"):
    return ('<text x="%.2f" y="%.2f" font-family="Inter,system-ui,sans-serif" '
            'font-size="%d" text-anchor="%s" fill="currentColor">%s</text>') % (x, y, size, anchor, s)

def dot(p):
    return '<circle cx="%.2f" cy="%.2f" r="2.4" fill="currentColor"/>' % p

def line(p, q):
    return '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="currentColor" stroke-width="1.6"/>' % (p[0],p[1],q[0],q[1])

DEG = "°"; MINUS = "−"; TIMES = "×"; DIV = "÷"

# ---------------- GOLD[1] : 28 (major-arc vertex C, top) -> 152 (minor-arc vertex D, bottom)
def build_gold1():
    O = (120, 100); r = 66
    half = math.radians(28)               # minor central AOB = 56 deg, 28 each side of downward vertical
    A = (O[0] - r*math.sin(half), O[1] + r*math.cos(half))
    B = (O[0] + r*math.sin(half), O[1] + r*math.cos(half))
    C = (O[0], O[1] - r)                   # top, on MAJOR arc  -> angle 28
    D = (O[0], O[1] + r)                   # bottom, on MINOR arc -> angle 152 (?)
    aC = dang(C, A, B); aD = dang(D, A, B)
    svg = ['<svg viewBox="0 0 240 200" role="img" aria-label="Circle with chord AB; vertex C on the major arc shows 28 degrees, vertex D on the minor arc is unknown" style="max-width:280px;width:100%;height:auto">']
    svg.append('<circle cx="%d" cy="%d" r="%d" fill="#60a5fa" fill-opacity="0.10" stroke="currentColor" stroke-width="1.6"/>' % (O[0],O[1],r))
    svg.append(line(A,B))
    for P in (A,B):
        svg.append(line(C,P)); svg.append(line(D,P))
    for P in (A,B,C,D): svg.append(dot(P))
    # angle at C (28)
    svg.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.4"/>' % angle_arc(C, A, B, 20))
    svg.append(T(C[0], C[1]+30, "28"+DEG, 10))
    # angle at D (?)
    svg.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.4"/>' % angle_arc(D, A, B, 20))
    svg.append(T(D[0], D[1]-14, "?", 11))
    svg.append(T(A[0]-8, A[1]+4, "A", 11, "end"))
    svg.append(T(B[0]+8, B[1]+4, "B", 11, "start"))
    svg.append(T(C[0], C[1]-6, "C", 11))
    svg.append(T(D[0], D[1]+16, "D", 11))
    svg.append('</svg>')
    disp = "".join(svg) + '<span class="figure-caption">Diagram not drawn accurately</span>' \
        + "Angle at the circumference from the minor arc = \\(28" + DEG + "\\). Find the angle at the circumference from the major arc."
    return disp, aC, aD

# ---------------- SILVER[5] : central 110 (minor arc) -> 125 at vertex C on MINOR arc
def build_silver5():
    O = (120, 100); r = 66
    half = math.radians(55)               # central AOB = 110, opening downward
    A = (O[0] - r*math.sin(half), O[1] + r*math.cos(half))
    B = (O[0] + r*math.sin(half), O[1] + r*math.cos(half))
    C = (O[0], O[1] + r)                   # bottom, on the MINOR arc -> inscribed 125
    aO = dang(O, A, B); aC = dang(C, A, B)
    svg = ['<svg viewBox="0 0 240 200" role="img" aria-label="Circle centre O; 110 degrees at the centre on the minor arc; vertex C on the minor arc subtends the major arc, angle unknown" style="max-width:280px;width:100%;height:auto">']
    svg.append('<circle cx="%d" cy="%d" r="%d" fill="#60a5fa" fill-opacity="0.10" stroke="currentColor" stroke-width="1.6"/>' % (O[0],O[1],r))
    svg.append(line(O,A)); svg.append(line(O,B))     # radii
    svg.append(line(C,A)); svg.append(line(C,B))     # chords from circumference vertex
    for P in (O,A,B,C): svg.append(dot(P))
    # central angle 110 at O (opens downward toward C)
    svg.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.4"/>' % angle_arc(O, A, B, 24))
    svg.append(T(O[0], O[1]+30, "110"+DEG, 10))
    # inscribed angle ? at C (opens upward toward chord)
    svg.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.4"/>' % angle_arc(C, A, B, 20))
    svg.append(T(C[0], C[1]-12, "?", 11))
    svg.append(T(O[0]+9, O[1]+4, "O", 10, "start"))
    svg.append(T(A[0]-8, A[1]+4, "A", 11, "end"))
    svg.append(T(B[0]+8, B[1]+4, "B", 11, "start"))
    svg.append(T(C[0], C[1]+16, "C", 11))
    svg.append('</svg>')
    disp = "".join(svg) + '<span class="figure-caption">Diagram not drawn accurately</span>' \
        + "Angle at the centre from the minor arc = \\(110" + DEG + "\\). Find the angle at the circumference from the major arc."
    return disp, aO, aC

gd, aC, aD = build_gold1()
sd, aO, aC2 = build_silver5()
print("GOLD1 drawn: angle at C(top,major)=%.1f (want ~28), angle at D(bottom,minor)=%.1f (want ~152)" % (aC, aD))
print("SILVER5 drawn: central at O=%.1f (want ~110), inscribed at C(minor arc)=%.1f (want ~125)" % (aO, aC2))
print("gold len", len(gd), "silver len", len(sd))
io.open("_gold1_disp.txt","w",encoding="utf-8").write(gd)
io.open("_silver5_disp.txt","w",encoding="utf-8").write(sd)
