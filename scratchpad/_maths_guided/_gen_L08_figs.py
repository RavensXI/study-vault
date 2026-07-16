# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for geometry-L08 (Vectors) from each
problem's own numbers, prepend to the relevant displays, dump practice_data."""
import json, io

SRC = "_L08_live_fresh.json"
OUT = "lesson_geometry-L08_diagrams.json"

def n(v):
    # tidy number -> str
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)

# ---------- coordinate grid (geomL04 house style) ----------
def grid(xmin, xmax, ymin, ymax, points, segments, aria, u=None, label_every=1):
    LP, TP, RP, BP = 16, 10, 10, 16
    if u is None:
        u = 18
    def sx(x): return round(LP + (x - xmin) * u, 1)
    def sy(y): return round(TP + (ymax - y) * u, 1)
    W = round(LP + (xmax - xmin) * u + RP, 1)
    H = round(TP + (ymax - ymin) * u + BP, 1)
    s = ['<svg viewBox="0 0 %s %s" role="img" aria-label="%s" '
         'style="max-width:260px;width:100%%;height:auto;font-family:Inter,sans-serif">'
         % (n(W), n(H), aria)]
    # faint grid
    s.append('<g stroke="currentColor" stroke-opacity="0.15" stroke-width="0.5">')
    for x in range(xmin, xmax + 1):
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(sx(x)), n(sy(ymin)), n(sx(x)), n(sy(ymax))))
    for y in range(ymin, ymax + 1):
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(sx(xmin)), n(sy(y)), n(sx(xmax)), n(sy(y))))
    s.append('</g>')
    # axes emphasised
    s.append('<g stroke="currentColor" stroke-opacity="0.5" stroke-width="1">')
    if ymin <= 0 <= ymax:
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(sx(xmin)), n(sy(0)), n(sx(xmax)), n(sy(0))))
    if xmin <= 0 <= xmax:
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(sx(0)), n(sy(ymin)), n(sx(0)), n(sy(ymax))))
    s.append('</g>')
    # tick labels
    s.append('<g fill="currentColor" fill-opacity="0.6" font-size="6.5">')
    for x in range(xmin, xmax + 1):
        if x % label_every: continue
        if x == 0: continue
        s.append('<text x="%s" y="%s" text-anchor="middle">%d</text>' % (n(sx(x)), n(sy(ymin) + 8), x))
    for y in range(ymin, ymax + 1):
        if y % label_every: continue
        if y == 0: continue
        s.append('<text x="%s" y="%s" text-anchor="end">%d</text>' % (n(sx(xmin) - 3), n(sy(y) + 2.3), y))
    if xmin <= 0 <= xmax and ymin <= 0 <= ymax:
        s.append('<text x="%s" y="%s" text-anchor="end">O</text>' % (n(sx(0) - 3), n(sy(0) + 8)))
    s.append('</g>')
    # segments (lines through points)
    for seg in segments:
        (ax, ay), (bx, by) = seg["from"], seg["to"]
        dash = ' stroke-dasharray="3 2"' if seg.get("dash") else ''
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.5"%s/>'
                 % (n(sx(ax)), n(sy(ay)), n(sx(bx)), n(sy(by)), seg.get("colour", "#3b82f6"), dash))
        if seg.get("mid_label"):
            mx, my = (ax + bx) / 2.0, (ay + by) / 2.0
            s.append('<text x="%s" y="%s" text-anchor="middle" fill="currentColor" font-size="8">%s</text>'
                     % (n(sx(mx) + seg.get("dx", 0)), n(sy(my) + seg.get("dy", -3)), seg["mid_label"]))
    # points
    for pt in points:
        px, py = pt["at"]
        s.append('<circle cx="%s" cy="%s" r="3" fill="%s"/>' % (n(sx(px)), n(sy(py)), pt.get("colour", "#3b82f6")))
        lx = sx(px) + pt.get("dx", 6)
        ly = sy(py) + pt.get("dy", -5)
        anc = pt.get("anchor", "start")
        s.append('<text x="%s" y="%s" text-anchor="%s" fill="currentColor" font-size="9">%s</text>'
                 % (n(lx), n(ly), anc, pt["label"]))
    s.append('</svg>')
    return "".join(s)

# ---------- right-angled triangle for magnitude ----------
def rt_triangle(h_lab, v_lab, hyp_lab, scale, aria):
    LP, TP, RP, BP = 34, 12, 20, 20
    hpx = abs(int(round(float(h_lab.strip('-')) if h_lab.replace('-','').isdigit() else 0)))
    # use provided pixel legs
    hlen = scale[0]; vlen = scale[1]
    ox, oy = LP, TP + vlen  # right-angle corner (bottom-left)
    rx, ry = ox + hlen, oy   # bottom-right
    tx, ty = ox, TP          # top-left
    W = ox + hlen + RP
    H = oy + BP
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
         'style="max-width:230px;width:100%%;height:auto;font-family:Inter,sans-serif">' % (W, H, aria)]
    s.append('<polygon points="%d,%d %d,%d %d,%d" fill="#60a5fa" fill-opacity="0.3" '
             'stroke="currentColor" stroke-width="1.5"/>' % (ox, oy, rx, ry, tx, ty))
    # right-angle square (inside the corner)
    s.append('<rect x="%d" y="%d" width="9" height="9" fill="none" stroke="currentColor" stroke-width="1"/>'
             % (ox, oy - 9))
    # labels
    s.append('<text x="%d" y="%d" text-anchor="middle" fill="currentColor" font-size="11">%s</text>'
             % ((ox + rx) // 2, oy + 14, h_lab))
    s.append('<text x="%d" y="%d" text-anchor="end" fill="currentColor" font-size="11">%s</text>'
             % (ox - 5, (oy + ty) // 2 + 4, v_lab))
    s.append('<text x="%d" y="%d" text-anchor="start" fill="currentColor" font-size="11">%s</text>'
             % ((rx + tx) // 2 + 6, (ry + ty) // 2 - 2, hyp_lab))
    s.append('</svg>')
    return "".join(s)

# ---------- parallelogram OABC ----------
def parallelogram():
    O=(30,150); A=(42,52); C=(178,150); B=(190,52)
    P=(A[0]+(B[0]-A[0])/3.0, A[1]+(B[1]-A[1])/3.0)  # 1/3 from A
    aria=("Parallelogram OABC with vector a from O to A, vector c from O to C, "
          "and point P on AB dividing it in the ratio 1 to 2 from A.")
    s=['<svg viewBox="0 0 220 172" role="img" aria-label="%s" '
       'style="max-width:250px;width:100%%;height:auto;font-family:Inter,sans-serif">' % aria]
    s.append('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="#60a5fa" fill-opacity="0.3" '
             'stroke="currentColor" stroke-width="1.5"/>' % (O[0],O[1],A[0],A[1],B[0],B[1],C[0],C[1]))
    # arrow O->A (a) and O->C (c)
    def arrow(p,q,colour):
        import math
        ang=math.atan2(q[1]-p[1],q[0]-p[0])
        # shorten to before vertex
        qx=q[0]-8*math.cos(ang); qy=q[1]-8*math.sin(ang)
        head=[(qx,qy),
              (qx-7*math.cos(ang-0.4),qy-7*math.sin(ang-0.4)),
              (qx-7*math.cos(ang+0.4),qy-7*math.sin(ang+0.4))]
        out='<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>'%(p[0],p[1],qx,qy,colour)
        out+='<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'%(head[0][0],head[0][1],head[1][0],head[1][1],head[2][0],head[2][1],colour)
        return out
    s.append(arrow(O,A,"#f59e0b"))
    s.append(arrow(O,C,"#34d399"))
    s.append('<text x="%d" y="%d" fill="currentColor" font-size="12" font-style="italic" text-anchor="end">a</text>'%(O[0]-4,(O[1]+A[1])//2))
    s.append('<text x="%d" y="%d" fill="currentColor" font-size="12" font-style="italic" text-anchor="middle">c</text>'%((O[0]+C[0])//2,O[1]+15))
    # P
    s.append('<circle cx="%.1f" cy="%.1f" r="3" fill="#3b82f6"/>'%(P[0],P[1]))
    s.append('<text x="%.1f" y="%.1f" fill="currentColor" font-size="10" text-anchor="middle">P</text>'%(P[0],P[1]-6))
    # ratio marks along AB
    s.append('<text x="%.1f" y="%.1f" fill="currentColor" fill-opacity="0.7" font-size="8" text-anchor="middle">1</text>'%((A[0]+P[0])/2,A[1]-4))
    s.append('<text x="%.1f" y="%.1f" fill="currentColor" fill-opacity="0.7" font-size="8" text-anchor="middle">2</text>'%((P[0]+B[0])/2,A[1]-4))
    # vertex labels
    s.append('<text x="%d" y="%d" fill="currentColor" font-size="11" text-anchor="end">O</text>'%(O[0]-3,O[1]+11))
    s.append('<text x="%d" y="%d" fill="currentColor" font-size="11" text-anchor="end">A</text>'%(A[0]-3,A[1]-2))
    s.append('<text x="%d" y="%d" fill="currentColor" font-size="11" text-anchor="start">B</text>'%(B[0]+3,B[1]-2))
    s.append('<text x="%d" y="%d" fill="currentColor" font-size="11" text-anchor="start">C</text>'%(C[0]+3,C[1]+11))
    s.append('</svg>')
    return "".join(s)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def main():
    pd = json.load(io.open(SRC, encoding="utf-8"))
    added = []

    # gold[0] parallelogram
    g0 = pd["problem_bank"]["gold"][0]
    g0["display"] = parallelogram() + g0["display"] + CAP
    added.append(("gold", 0, "svg", "parallelogram OABC, vectors a and c, P on AB ratio 1:2"))

    # gold[3] grid A(3,1) B(-1,5) N on AB ratio 3:1
    g3 = pd["problem_bank"]["gold"][3]
    fig = grid(-1, 4, 0, 5,
               points=[{"at":(3,1),"label":"A(3, 1)","dx":-6,"dy":-4,"anchor":"end"},
                       {"at":(-1,5),"label":"B(-1, 5)","dx":10,"dy":-4},
                       {"at":(0,4),"label":"N","colour":"#f59e0b","dx":6,"dy":-4}],
               segments=[{"from":(3,1),"to":(-1,5),"colour":"#3b82f6"}],
               aria="Coordinate grid: points A at (3, 1) and B at minus 1, 5, with N on segment AB dividing it 3 to 1.")
    g3["display"] = fig + g3["display"]
    added.append(("gold", 3, "svg", "grid A(3,1), B(-1,5), N on AB (3:1)"))

    # gold[4] collinear A(1,2) B(4,8) C(6,12)
    g4 = pd["problem_bank"]["gold"][4]
    fig = grid(0, 6, 0, 12,
               points=[{"at":(1,2),"label":"A(1, 2)","dx":6,"dy":-3},
                       {"at":(4,8),"label":"B(4, 8)","dx":6,"dy":-3},
                       {"at":(6,12),"label":"C(6, 12)","dx":-2,"dy":11,"anchor":"end"}],
               segments=[{"from":(1,2),"to":(6,12),"colour":"#34d399"}],
               aria="Coordinate grid: points A(1, 2), B(4, 8) and C(6, 12) lie on one straight line.",
               u=13, label_every=2)
    g4["display"] = fig + g4["display"]
    added.append(("gold", 4, "svg", "grid: collinear A(1,2), B(4,8), C(6,12)"))

    # silver[4] midpoint A(1,5) B(7,3)
    s4 = pd["problem_bank"]["silver"][4]
    fig = grid(0, 7, 0, 5,
               points=[{"at":(1,5),"label":"A(1, 5)","dx":6,"dy":-3},
                       {"at":(7,3),"label":"B(7, 3)","dx":-2,"dy":-5,"anchor":"end"},
                       {"at":(4,4),"label":"M","colour":"#f59e0b","dx":4,"dy":-5}],
               segments=[{"from":(1,5),"to":(7,3),"colour":"#3b82f6"}],
               aria="Coordinate grid: A(1, 5), B(7, 3) with M the midpoint of AB.")
    s4["display"] = fig + s4["display"]
    added.append(("silver", 4, "svg", "grid: A(1,5), B(7,3), midpoint M"))

    # bronze[5] |(3,4)|
    b5 = pd["problem_bank"]["bronze"][5]
    fig = rt_triangle("3", "4", "?", (66, 88),
                      "Right-angled triangle: horizontal side 3, vertical side 4, hypotenuse marked with a question mark.")
    b5["display"] = fig + b5["display"] + CAP
    added.append(("bronze", 5, "svg", "right triangle legs 3 and 4, hyp ?"))

    # silver[6] |(-5,12)|
    s6 = pd["problem_bank"]["silver"][6]
    fig = rt_triangle("5", "12", "?", (45, 108),
                      "Right-angled triangle: horizontal side 5, vertical side 12, hypotenuse marked with a question mark.")
    s6["display"] = fig + s6["display"] + CAP
    added.append(("silver", 6, "svg", "right triangle legs 5 and 12, hyp ?"))

    # gold teach walk grid A(2,0) B(8,6) P divides 1:2
    gt = pd["guided"]["teach"]["gold"]
    fig = grid(0, 8, 0, 6,
               points=[{"at":(2,0),"label":"A(2, 0)","dx":2,"dy":11},
                       {"at":(8,6),"label":"B(8, 6)","dx":-2,"dy":-4,"anchor":"end"},
                       {"at":(4,2),"label":"P","colour":"#f59e0b","dx":6,"dy":-3}],
               segments=[{"from":(2,0),"to":(8,6),"colour":"#3b82f6"}],
               aria="Coordinate grid: A(2, 0), B(8, 6) with P on AB dividing it 1 to 2 from A.",
               u=16)
    gt["display"] = fig + gt["display"]
    added.append(("teach.gold", None, "svg", "grid: A(2,0), B(8,6), P on AB (1:2)"))

    json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote", OUT)
    for a in added:
        print("  +", a)

if __name__ == "__main__":
    main()
