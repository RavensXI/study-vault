# -*- coding: utf-8 -*-
import json

pd = json.load(open("lesson_maths-eduqas_geometry-L08.json", encoding="utf-8"))
pb = pd["problem_bank"]

CAP = "<span class=\"figure-caption\">Diagram not drawn accurately</span>"

def svg(vb, inner, aria):
    return (f"<svg viewBox='{vb}' role=\"img\" aria-label=\"{aria}\" "
            f"style='max-width:230px;width:100%;height:auto;font-family:Inter,sans-serif'>"
            + inner + "</svg>")

# ---- right-triangle magnitude figure: legs |x|,|y|, hyp = ? ----
def mag_triangle(ax, ay, aria):
    # place right angle at the corner; horizontal leg |ax|, vertical leg |ay|
    import math
    ux = 88 / max(abs(ax), 1)      # scale so bigger leg ~ fits
    uy = 96 / max(abs(ay), 1)
    u = min(ux, uy)
    w = abs(ax) * u
    h = abs(ay) * u
    x0, y0 = 24, 24 + h            # bottom-left corner
    # horizontal to the right, vertical up (we label with magnitudes only)
    cx, cy = x0 + w, y0           # right-angle corner
    tx, ty = cx, cy - h           # top
    inner = []
    inner.append(f"<polygon points='{x0},{y0} {cx},{cy} {tx},{ty}' fill='#60a5fa' fill-opacity='0.18' stroke='currentColor' stroke-width='1.6'/>")
    # right angle square at (cx,cy)
    s = 9
    inner.append(f"<path d='M {cx-s},{cy} L {cx-s},{cy-s} L {cx},{cy-s}' fill='none' stroke='currentColor' stroke-width='1.2'/>")
    # leg labels
    inner.append(f"<text x='{(x0+cx)/2}' y='{cy+15}' fill='currentColor' font-size='12' text-anchor='middle'>{abs(ax)}</text>")
    inner.append(f"<text x='{cx+7}' y='{(cy+ty)/2+4}' fill='currentColor' font-size='12'>{abs(ay)}</text>")
    # hypotenuse label ?
    inner.append(f"<text x='{(x0+tx)/2-14}' y='{(y0+ty)/2-2}' fill='currentColor' font-size='12'>?</text>")
    W = int(cx + 24); H = int(y0 + 24)
    return svg(f"0 0 {W} {H}", "".join(inner), aria)

# silver[0]: (3,4)
pb["silver"][0]["display"] = mag_triangle(3, 4,
    "Right-angled triangle with horizontal side 3, vertical side 4 and unknown hypotenuse") + \
    CAP + pb["silver"][0]["display"]
# silver[1]: (-6,8) -> legs 6 and 8
pb["silver"][1]["display"] = mag_triangle(6, 8,
    "Right-angled triangle with horizontal side 6, vertical side 8 and unknown hypotenuse") + \
    CAP + pb["silver"][1]["display"]

# ---- O-A-B schematic triangle ----
def oab(mark=None):
    # O bottom-left, A upper-left, B right
    O = (30, 118); A = (74, 28); B = (168, 92)
    inner = []
    def arrow(p, q, col, lbl, lblpos):
        inner.append(f"<line x1='{p[0]}' y1='{p[1]}' x2='{q[0]}' y2='{q[1]}' stroke='{col}' stroke-width='2'/>")
        inner.append(f"<text x='{lblpos[0]}' y='{lblpos[1]}' fill='currentColor' font-size='12'>{lbl}</text>")
    # a = O->A, b = O->B
    arrow(O, A, "#3b82f6", "a", ((O[0]+A[0])/2-14, (O[1]+A[1])/2))
    arrow(O, B, "#f59e0b", "b", ((O[0]+B[0])/2-2, (O[1]+B[1])/2+16))
    # AB line
    inner.append(f"<line x1='{A[0]}' y1='{A[1]}' x2='{B[0]}' y2='{B[1]}' stroke='currentColor' stroke-width='1.4' stroke-dasharray='4 3'/>")
    for P, nm, dx, dy in [(O,"O",-12,4),(A,"A",-4,-6),(B,"B",6,4)]:
        inner.append(f"<circle cx='{P[0]}' cy='{P[1]}' r='3' fill='currentColor'/>")
        inner.append(f"<text x='{P[0]+dx}' y='{P[1]+dy}' fill='currentColor' font-size='12' font-weight='bold'>{nm}</text>")
    if mark == "AB?":
        mx, my = (A[0]+B[0])/2, (A[1]+B[1])/2
        inner.append(f"<text x='{mx-4}' y='{my-6}' fill='currentColor' font-size='12'>?</text>")
    if mark == "P21":
        # P divides AB 2:1 from A -> 2/3 along
        Px = A[0] + (2/3)*(B[0]-A[0]); Py = A[1] + (2/3)*(B[1]-A[1])
        inner.append(f"<circle cx='{Px:.1f}' cy='{Py:.1f}' r='3' fill='#34d399'/>")
        inner.append(f"<text x='{Px+5:.1f}' y='{Py-5:.1f}' fill='currentColor' font-size='12' font-weight='bold'>P</text>")
        inner.append(f"<text x='{(A[0]+Px)/2-14:.1f}' y='{(A[1]+Py)/2-4:.1f}' fill='currentColor' font-size='10'>2</text>")
        inner.append(f"<text x='{(Px+B[0])/2+2:.1f}' y='{(Py+B[1])/2-4:.1f}' fill='currentColor' font-size='10'>1</text>")
    if mark == "Mmid":
        Mx, My = (A[0]+B[0])/2, (A[1]+B[1])/2
        inner.append(f"<circle cx='{Mx}' cy='{My}' r='3' fill='#34d399'/>")
        inner.append(f"<text x='{Mx+5}' y='{My-5}' fill='currentColor' font-size='12' font-weight='bold'>M</text>")
    return svg("0 0 196 140", "".join(inner), "Triangle O A B with position vectors a and b from O")

# silver[2]: find AB
pb["silver"][2]["display"] = oab("AB?") + CAP + pb["silver"][2]["display"]
# gold[0]: P divides AB 2:1
pb["gold"][0]["display"] = oab("P21") + CAP + pb["gold"][0]["display"]
# gold[1]: M midpoint (schematic; OA=3a, OB=6b labelled in text)
pb["gold"][1]["display"] = oab("Mmid") + CAP + pb["gold"][1]["display"]

# ---- silver[3]: coordinate grid with O,A(2,6),B(8,2),M(5,4) ----
def grid_pts():
    ox, oy, u = 22, 140, 18
    def X(g): return ox + u*g
    def Y(g): return oy - u*g
    inner = []
    for gx in range(9):
        inner.append(f"<line x1='{X(gx)}' y1='{Y(0)}' x2='{X(gx)}' y2='{Y(7)}' stroke='currentColor' stroke-opacity='0.10' stroke-width='1'/>")
    for gy in range(8):
        inner.append(f"<line x1='{X(0)}' y1='{Y(gy)}' x2='{X(8)}' y2='{Y(gy)}' stroke='currentColor' stroke-opacity='0.10' stroke-width='1'/>")
    inner.append(f"<line x1='{X(0)}' y1='{Y(0)}' x2='{X(8)}' y2='{Y(0)}' stroke='currentColor' stroke-width='1.2'/>")
    inner.append(f"<line x1='{X(0)}' y1='{Y(0)}' x2='{X(0)}' y2='{Y(7)}' stroke='currentColor' stroke-width='1.2'/>")
    A=(2,6); B=(8,2); M=(5,4)
    inner.append(f"<line x1='{X(A[0])}' y1='{Y(A[1])}' x2='{X(B[0])}' y2='{Y(B[1])}' stroke='#3b82f6' stroke-width='1.6'/>")
    for (g,nm,col,dx,dy) in [((0,0),"O","currentColor",-12,13),(A,"A","#3b82f6",4,-4),(B,"B","#3b82f6",5,4),(M,"M","#34d399",6,-4)]:
        inner.append(f"<circle cx='{X(g[0])}' cy='{Y(g[1])}' r='3.2' fill='{col}'/>")
        inner.append(f"<text x='{X(g[0])+dx}' y='{Y(g[1])+dy}' fill='currentColor' font-size='11' font-weight='bold'>{nm}</text>")
    return svg("0 0 190 156", "".join(inner),
               "Coordinate grid showing O at origin, A at (2,6), B at (8,2) and midpoint M at (5,4)")
pb["silver"][3]["display"] = grid_pts() + pb["silver"][3]["display"]

# ---- silver[5]: segment P..R..Q with R at 1/3 ----
def seg_PRQ():
    P=(24,38); Q=(188,100)  # direction roughly (6,-2)
    Rx = P[0] + (1/3)*(Q[0]-P[0]); Ry = P[1] + (1/3)*(Q[1]-P[1])
    inner = []
    inner.append(f"<line x1='{P[0]}' y1='{P[1]}' x2='{Q[0]}' y2='{Q[1]}' stroke='currentColor' stroke-width='1.6'/>")
    for (pt,nm,col,dx,dy) in [(P,"P","currentColor",-14,4),(Q,"Q","currentColor",6,4),((Rx,Ry),"R","#34d399",-4,-8)]:
        inner.append(f"<circle cx='{pt[0]:.1f}' cy='{pt[1]:.1f}' r='3.2' fill='{col}'/>")
        inner.append(f"<text x='{pt[0]+dx:.1f}' y='{pt[1]+dy:.1f}' fill='currentColor' font-size='12' font-weight='bold'>{nm}</text>")
    inner.append(f"<text x='{(P[0]+Rx)/2-6:.1f}' y='{(P[1]+Ry)/2-6:.1f}' fill='currentColor' font-size='10'>⅓</text>")
    return svg("0 0 210 120", "".join(inner),
               "Line segment P to Q with R marked one third of the way from P")
pb["silver"][5]["display"] = seg_PRQ() + CAP + pb["silver"][5]["display"]

# ---- bronze[6]: grid arrow A->B by (3,4) ----
def arrow_grid():
    ox, oy, u = 20, 152, 22
    def X(g): return ox + u*g
    def Y(g): return oy - u*g
    inner = []
    for gx in range(7):
        inner.append(f"<line x1='{X(gx)}' y1='{Y(0)}' x2='{X(gx)}' y2='{Y(6)}' stroke='currentColor' stroke-opacity='0.10' stroke-width='1'/>")
    for gy in range(7):
        inner.append(f"<line x1='{X(0)}' y1='{Y(gy)}' x2='{X(6)}' y2='{Y(gy)}' stroke='currentColor' stroke-opacity='0.10' stroke-width='1'/>")
    A=(1,1); B=(4,5)   # displacement (3,4)
    inner.append(f"<line x1='{X(A[0])}' y1='{Y(A[1])}' x2='{X(B[0])}' y2='{Y(B[1])}' stroke='#3b82f6' stroke-width='2'/>")
    for (g,nm,dx,dy) in [(A,"A",-13,4),(B,"B",5,0)]:
        inner.append(f"<circle cx='{X(g[0])}' cy='{Y(g[1])}' r='3.2' fill='currentColor'/>")
        inner.append(f"<text x='{X(g[0])+dx}' y='{Y(g[1])+dy}' fill='currentColor' font-size='12' font-weight='bold'>{nm}</text>")
    mx=(X(A[0])+X(B[0]))/2; my=(Y(A[1])+Y(B[1]))/2
    inner.append(f"<text x='{mx+4}' y='{my}' fill='currentColor' font-size='10'>(3, 4)</text>")
    return svg("0 0 172 168", "".join(inner),
               "Grid showing point A and point B with an arrow from A to B representing the vector (3, 4)")
pb["bronze"][6]["display"] = arrow_grid() + pb["bronze"][6]["display"]

json.dump(pd, open("lesson_maths-eduqas_geometry-L08_diagrams.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written diagrams shard")
