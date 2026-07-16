# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for graphs-L02 (Equation of a Line).
Every pixel coordinate is computed from the problem's own numbers.
Figures added:
  1. opener  : taxi-fare real-life line graph (cost = 2*miles + 3)
  2. gold[4] : midpoint scene, A(1,2) & B(5,10) with midpoint M
  3. silver[5]: parallel lines P (y=-3x+2) and Q through (1,5)
"""
import json, io

def f(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")

# ---------------------------------------------------------------- FIGURE 1
# Taxi fare: cost = 3 + 2*miles.  x = miles 0..5, y = cost 0..13.
def build_taxi():
    ox = lambda m: 44 + m * 40.0          # mile 0 -> 44, mile 5 -> 244
    oy = lambda c: 165 - c * 10.4         # cost 0 -> 165, cost 13 -> 29.8
    x0, y0 = ox(0), oy(3)                 # start (0 miles, £3)
    x1, y1 = ox(5), oy(13)               # (5 miles, £13)
    # verify: gradient in data-units = (13-3)/(5-0) = 2  (matches £2/mile)
    assert (13 - 3) / (5 - 0) == 2
    parts = []
    parts.append('<svg viewBox="0 0 260 190" role="img" aria-label="Line graph of taxi cost against miles: it starts at £3 for zero miles and rises steadily by £2 each mile." style="max-width:280px;width:100%;font-family:Inter,sans-serif">')
    # axes
    parts.append('<line x1="44" y1="165" x2="252" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="44" y1="165" x2="44" y2="20" stroke="currentColor" stroke-width="1.2"/>')
    # mile ticks + labels
    for m in range(1, 6):
        x = ox(m)
        parts.append('<line x1="%s" y1="165" x2="%s" y2="169" stroke="currentColor" stroke-width="1"/>' % (f(x), f(x)))
        parts.append('<text x="%s" y="180" font-size="10" fill="currentColor" text-anchor="middle">%d</text>' % (f(x), m))
    # £3 start guide + label (given in the prompt text)
    parts.append('<line x1="40" y1="%s" x2="44" y2="%s" stroke="currentColor" stroke-width="1"/>' % (f(y0), f(y0)))
    parts.append('<text x="37" y="%s" font-size="10" fill="currentColor" text-anchor="end">£3</text>' % f(y0 + 3))
    # the fare line
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#f59e0b" stroke-width="2.4"/>' % (f(x0), f(y0), f(x1), f(y1)))
    parts.append('<circle cx="%s" cy="%s" r="3.2" fill="#f59e0b"/>' % (f(x0), f(y0)))
    # axis titles
    parts.append('<text x="148" y="189" font-size="10.5" fill="currentColor" text-anchor="middle">Miles</text>')
    parts.append('<text x="20" y="14" font-size="10.5" fill="currentColor">Cost (£)</text>')
    parts.append('</svg>')
    return "".join(parts)

# ---------------------------------------------------------------- FIGURE 2
# Midpoint scene. A(1,2), B(5,10). Grid x 0..6, y 0..11.
def build_midpoint():
    A = (1, 2); B = (5, 10)
    M = ((A[0] + B[0]) / 2.0, (A[1] + B[1]) / 2.0)   # (3, 6)
    assert M == (3, 6)
    gx = lambda xv: 34 + xv * 30.0        # x0 -> 34, x6 -> 214
    gy = lambda yv: 180 - yv * 14.0       # y0 -> 180, y11 -> 26
    parts = []
    parts.append('<svg viewBox="0 0 232 200" role="img" aria-label="Coordinate grid with points A at (1, 2) and B at (5, 10), the line segment AB, and its midpoint M marked." style="max-width:280px;width:100%;font-family:Inter,sans-serif">')
    # faint grid
    for xv in range(0, 7):
        x = gx(xv)
        parts.append('<line x1="%s" y1="30" x2="%s" y2="180" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>' % (f(x), f(x)))
    for yv in range(0, 12):
        y = gy(yv)
        parts.append('<line x1="34" y1="%s" x2="214" y2="%s" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>' % (f(y), f(y)))
    # axes
    parts.append('<line x1="34" y1="180" x2="220" y2="180" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="34" y1="180" x2="34" y2="26" stroke="currentColor" stroke-width="1.2"/>')
    # segment AB
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#60a5fa" stroke-width="2"/>' % (f(gx(A[0])), f(gy(A[1])), f(gx(B[0])), f(gy(B[1]))))
    # points A and B
    parts.append('<circle cx="%s" cy="%s" r="3.4" fill="#60a5fa"/>' % (f(gx(A[0])), f(gy(A[1]))))
    parts.append('<text x="%s" y="%s" font-size="10.5" fill="currentColor">A(1, 2)</text>' % (f(gx(A[0]) + 6), f(gy(A[1]) + 12)))
    parts.append('<circle cx="%s" cy="%s" r="3.4" fill="#60a5fa"/>' % (f(gx(B[0])), f(gy(B[1]))))
    parts.append('<text x="%s" y="%s" font-size="10.5" fill="currentColor" text-anchor="end">B(5, 10)</text>' % (f(gx(B[0]) - 6), f(gy(B[1]) + 4)))
    # midpoint M (coordinates deliberately NOT labelled: that is the first task)
    parts.append('<circle cx="%s" cy="%s" r="3.4" fill="#f59e0b"/>' % (f(gx(M[0])), f(gy(M[1]))))
    parts.append('<text x="%s" y="%s" font-size="10.5" fill="currentColor">M</text>' % (f(gx(M[0]) + 6), f(gy(M[1]) - 5)))
    parts.append('</svg>')
    return "".join(parts)

# ---------------------------------------------------------------- FIGURE 3
# Parallel lines. P: y=-3x+2. Q: parallel through (1,5), gradient -3.
# Grid x -1..3, y -4..7. Q's intercept (0,8) is off-grid on purpose.
def build_parallel():
    mP = -3; cP = 2
    mQ = -3
    pt = (1, 5); cQ = pt[1] - mQ * pt[0]   # 5 - (-3)(1) = 8
    assert cQ == 8
    px = lambda xv: 40 + (xv + 1) * 44.0    # x-1 -> 40, x3 -> 216
    py = lambda yv: 190 - (yv + 4) * 16.0   # y-4 -> 190, y7 -> 14
    def clip_line(m, c):
        # return the two endpoints of the line within the box x[-1,3], y[-4,7]
        pts = []
        for xv in (-1, 3):
            yv = m * xv + c
            if -4 <= yv <= 7:
                pts.append((xv, yv))
        for yv in (-4, 7):
            xv = (yv - c) / m
            if -1 <= xv <= 3:
                pts.append((xv, yv))
        # dedupe, keep two extremes by x
        pts = sorted(set(round(a, 4) for a in ()) or pts)
        return pts[0], pts[-1]
    P0, P1 = clip_line(mP, cP)
    Q0, Q1 = clip_line(mQ, cQ)
    ax0, ax1 = px(0), px(0)                 # y-axis at x=0
    ay = py(0)                              # x-axis at y=0
    parts = []
    parts.append('<svg viewBox="0 0 232 210" role="img" aria-label="Two parallel lines on a grid: line P with y-intercept 2, and line Q which is parallel to P and passes through the point (1, 5)." style="max-width:280px;width:100%;font-family:Inter,sans-serif">')
    # faint grid
    for xv in range(-1, 4):
        x = px(xv)
        parts.append('<line x1="%s" y1="14" x2="%s" y2="190" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>' % (f(x), f(x)))
    for yv in range(-4, 8):
        y = py(yv)
        parts.append('<line x1="40" y1="%s" x2="216" y2="%s" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>' % (f(y), f(y)))
    # axes
    parts.append('<line x1="40" y1="%s" x2="220" y2="%s" stroke="currentColor" stroke-width="1.2"/>' % (f(ay), f(ay)))
    parts.append('<line x1="%s" y1="14" x2="%s" y2="195" stroke="currentColor" stroke-width="1.2"/>' % (f(ax0), f(ax1)))
    # line P (solid)
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#60a5fa" stroke-width="2.2"/>' % (f(px(P0[0])), f(py(P0[1])), f(px(P1[0])), f(py(P1[1]))))
    # P intercept marker at (0,2) (given in the equation)
    parts.append('<circle cx="%s" cy="%s" r="2.8" fill="#60a5fa"/>' % (f(px(0)), f(py(2))))
    parts.append('<text x="%s" y="%s" font-size="10" fill="currentColor" text-anchor="end">2</text>' % (f(px(0) - 4), f(py(2) - 3)))
    # line Q (dashed, intercept off-grid so it is not revealed)
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#f59e0b" stroke-width="2.2" stroke-dasharray="5 3"/>' % (f(px(Q0[0])), f(py(Q0[1])), f(px(Q1[0])), f(py(Q1[1]))))
    # point (1,5) on Q
    parts.append('<circle cx="%s" cy="%s" r="3.2" fill="#f59e0b"/>' % (f(px(1)), f(py(5))))
    parts.append('<text x="%s" y="%s" font-size="10" fill="currentColor">(1, 5)</text>' % (f(px(1) + 5), f(py(5) - 4)))
    # line labels
    parts.append('<text x="%s" y="%s" font-size="11" fill="currentColor" font-weight="600">P</text>' % (f(px(P0[0]) + 4), f(py(P0[1]) + 12)))
    parts.append('<text x="%s" y="%s" font-size="11" fill="currentColor" font-weight="600">Q</text>' % (f(px(Q1[0]) - 14), f(py(Q1[1]) - 4)))
    parts.append('</svg>')
    return "".join(parts), (P0, P1, Q0, Q1, cQ)

pd = json.load(io.open("_live_L02.json", encoding="utf-8"))

taxi = build_taxi()
mid = build_midpoint()
par, pinfo = build_parallel()

# Insert at the START of each display, preserving the original text.
op = pd["guided"]["opener"]
op["display"] = taxi + '<div style="margin-top:6px">' + op["display"] + '</div>'

g4 = pd["problem_bank"]["gold"][4]
assert "midpoint" in g4["display"].lower()
g4["display"] = mid + '<div style="margin-top:6px">' + g4["display"] + '</div>'

s5 = pd["problem_bank"]["silver"][5]
assert "parallel" in s5["display"].lower()
s5["display"] = par + '<div style="margin-top:6px">' + s5["display"] + '</div>'

json.dump(pd, io.open("lesson_graphs-L02_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("taxi len", len(taxi))
print("mid len", len(mid))
print("par len", len(par), "P", pinfo[0], pinfo[1], "Q", pinfo[2], pinfo[3], "cQ(hidden)", pinfo[4])
print("WROTE lesson_graphs-L02_diagrams.json")
