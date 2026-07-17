# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion for maths-ocr geometry-L08 (Vectors)."""
import json, io, math

live = json.load(io.open('_geoL08_live.json', encoding='utf-8'))

# ---------------------------------------------------------------------------
# SVG helpers (theme-safe: currentColor strokes/text, soft opacity fills)
# ---------------------------------------------------------------------------
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'
FONT = 'font-family="Inter,sans-serif"'

def tri_svg(hlabel, vlabel, hyplabel, aria):
    return (
        '<svg viewBox="0 0 210 160" role="img" aria-label="%s" style="max-width:230px">'
        '<polygon points="34,132 184,132 184,34" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>'
        '<rect x="170" y="118" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<text x="109" y="150" %s font-size="12" text-anchor="middle" fill="currentColor">%s</text>'
        '<text x="190" y="86" %s font-size="12" text-anchor="start" fill="currentColor">%s</text>'
        '<text x="98" y="78" %s font-size="12" text-anchor="middle" fill="currentColor">%s</text>'
        '</svg>'
    ) % (aria, FONT, hlabel, FONT, vlabel, FONT, hyplabel)

def opener_grid():
    O = (34, 196); cell = 26
    def px(i): return 34 + i * cell
    def py(j): return 196 - j * cell
    parts = ['<svg viewBox="0 0 196 212" role="img" aria-label="A grid map: walk 3 squares east and 2 north, then 1 east and 4 north." style="max-width:230px">']
    for i in range(6):
        parts.append('<line x1="%d" y1="14" x2="%d" y2="196" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (px(i), px(i)))
    for j in range(8):
        parts.append('<line x1="34" y1="%d" x2="164" y2="%d" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (py(j), py(j)))
    A = (px(3), py(2)); T = (px(4), py(6))
    # legs
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3b82f6" stroke-width="2.5"/>' % (O[0], O[1], A[0], A[1]))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3b82f6" stroke-width="2.5"/>' % (A[0], A[1], T[0], T[1]))
    parts.append('<circle cx="%d" cy="%d" r="3.5" fill="currentColor"/>' % O)
    parts.append('<circle cx="%d" cy="%d" r="3.5" fill="#3b82f6"/>' % A)
    parts.append('<circle cx="%d" cy="%d" r="4.5" fill="#f59e0b"/>' % T)
    parts.append('<text x="%d" y="%d" %s font-size="11" fill="currentColor">Start</text>' % (O[0] + 6, O[1] - 6, FONT))
    parts.append('<text x="%d" y="%d" %s font-size="11" fill="currentColor">Treasure</text>' % (T[0] - 8, T[1] - 8, FONT))
    parts.append('<text x="150" y="208" %s font-size="10" fill="currentColor">E &#8594;</text>' % FONT)
    parts.append('</svg>')
    return ''.join(parts)

def line_points_svg(points, aria, ratio_label=None):
    # points: list of (label, frac) along a horizontal line 0..1
    x0, x1, y = 24, 196, 60
    parts = ['<svg viewBox="0 0 210 96" role="img" aria-label="%s" style="max-width:230px">' % aria]
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="2"/>' % (x0, y, x1, y))
    for label, frac in points:
        x = x0 + (x1 - x0) * frac
        col = '#f59e0b' if label == 'P' else 'currentColor'
        parts.append('<circle cx="%.1f" cy="%d" r="4" fill="%s"/>' % (x, y, col))
        parts.append('<text x="%.1f" y="%d" %s font-size="12" text-anchor="middle" fill="currentColor">%s</text>' % (x, y - 12, FONT, label))
    if ratio_label:
        parts.append('<text x="110" y="%d" %s font-size="11" text-anchor="middle" fill="currentColor">%s</text>' % (y + 22, FONT, ratio_label))
    parts.append('</svg>')
    return ''.join(parts)

def om_schematic():
    # O bottom-left, A top, B right, M midpoint of AB
    O = (30, 150); A = (70, 30); B = (180, 70)
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    p = ['<svg viewBox="0 0 210 172" role="img" aria-label="Point O with position vectors a to A and b to B; M is the midpoint of AB." style="max-width:230px">']
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.5" stroke-width="1.5" stroke-dasharray="4 3"/>' % (A[0], A[1], B[0], B[1]))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3b82f6" stroke-width="2"/>' % (O[0], O[1], A[0], A[1]))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3b82f6" stroke-width="2"/>' % (O[0], O[1], B[0], B[1]))
    p.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#f59e0b" stroke-width="2"/>' % (O[0], O[1], M[0], M[1]))
    for pt, lab, col in [(O, 'O', 'currentColor'), (A, 'A', '#3b82f6'), (B, 'B', '#3b82f6'), (M, 'M', '#f59e0b')]:
        p.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/>' % (pt[0], pt[1], col))
        p.append('<text x="%.1f" y="%.1f" %s font-size="12" fill="currentColor">%s</text>' % (pt[0] - 12, pt[1] - 6, FONT, lab))
    p.append('<text x="42" y="94" %s font-size="12" font-style="italic" fill="currentColor">a</text>' % FONT)
    p.append('<text x="112" y="118" %s font-size="12" font-style="italic" fill="currentColor">b</text>' % FONT)
    p.append('<text x="96" y="150" %s font-size="12" fill="currentColor">?</text>' % FONT)
    p.append('</svg>')
    return ''.join(p)

def parallel_svg():
    O = (28, 150)
    v1 = (O[0] + 46, O[1] - 92)   # shorter (2,6)-ish
    v2 = (O[0] + 66, O[1] - 132)  # longer (3,9)-ish
    p = ['<svg viewBox="0 0 150 168" role="img" aria-label="Two vectors drawn from the same point, both pointing up and to the right in the same direction." style="max-width:180px">']
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3b82f6" stroke-width="2.5"/>' % (O[0], O[1], v2[0], v2[1]))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#f59e0b" stroke-width="2.5"/>' % (O[0], O[1], v1[0], v1[1]))
    p.append('<circle cx="%d" cy="%d" r="3" fill="currentColor"/>' % O)
    p.append('<text x="%d" y="%d" %s font-size="11" fill="currentColor">(2,6)</text>' % (v1[0] + 4, v1[1] + 4, FONT))
    p.append('<text x="%d" y="%d" %s font-size="11" fill="currentColor">(3,9)</text>' % (v2[0] - 6, v2[1] - 4, FONT))
    p.append('</svg>')
    return ''.join(p)

def ab_grid():
    # A(1,3), B(5,7) on a grid; arrow A->B, run & rise dashed
    cell = 20; ox = 26; oy = 174  # origin pixel, x0..6, y0..8
    def px(i): return ox + i * cell
    def py(j): return oy - j * cell
    p = ['<svg viewBox="0 0 168 196" role="img" aria-label="A grid showing point A at (1,3) and B at (5,7), with the vector AB drawn from A to B." style="max-width:210px">']
    for i in range(7):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.13" stroke-width="1"/>' % (px(i), py(0), px(i), py(8)))
    for j in range(9):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.13" stroke-width="1"/>' % (px(0), py(j), px(6), py(j)))
    A = (px(1), py(3)); B = (px(5), py(7))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.4" stroke-width="1.5" stroke-dasharray="3 3"/>' % (A[0], A[1], B[0], A[1]))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.4" stroke-width="1.5" stroke-dasharray="3 3"/>' % (B[0], A[1], B[0], B[1]))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3b82f6" stroke-width="2.5"/>' % (A[0], A[1], B[0], B[1]))
    p.append('<circle cx="%d" cy="%d" r="3.5" fill="currentColor"/>' % A)
    p.append('<circle cx="%d" cy="%d" r="3.5" fill="#3b82f6"/>' % B)
    p.append('<text x="%d" y="%d" %s font-size="11" fill="currentColor">A</text>' % (A[0] - 12, A[1] + 4, FONT))
    p.append('<text x="%d" y="%d" %s font-size="11" fill="currentColor">B</text>' % (B[0] + 4, B[1], FONT))
    p.append('</svg>')
    return ''.join(p)

# ---------------------------------------------------------------------------
# guided_steps builders (every box value asserted against the solution)
# ---------------------------------------------------------------------------
def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d

def sayonly(say): return {"say": say}

def opnd(v):
    return ("(−%d)" % abs(v)) if v < 0 else ("%d" % v)

def kf(k):
    return ("−%d" % abs(k)) if k < 0 else ("%d" % k)

def pairstr(p0, p1, op):
    return "%d %s %s" % (p0, "+" if op == '+' else "−", opnd(p1))

def walk_addsub(ax, ay, bx, by, op, asked, av="", bv=""):
    # op '+' or '-', asked 'x' or 'y'
    if op == '+':
        rx, ry = ax + bx, ay + by; word = "Add"
    else:
        rx, ry = ax - bx, ay - by; word = "Subtract"
    want = rx if asked == 'x' else ry
    other = ry if asked == 'x' else rx
    oname = 'y' if asked == 'x' else 'x'
    a_o = (ay, by) if asked == 'x' else (ax, bx)
    a_w = (ax, bx) if asked == 'x' else (ay, by)
    sign = '+' if op == '+' else '−'
    steps = [
        sayonly("%s column vectors by working down the columns: the two %s parts together, the two %s parts together." % (word, "x" if asked=='x' else 'y', 'y' if asked=='x' else 'x')),
        box("First the %s parts, %s = " % (oname, pairstr(a_o[0], a_o[1], op)), other,
            "Work down the %s row." % oname),
        box("Now the %s parts, the one asked for, %s = " % (asked, pairstr(a_w[0], a_w[1], op)), want,
            "Work down the %s row, keeping any minus signs." % asked, phase="substitute"),
        box("So the full answer is a column vector. Its %s-component = " % asked, want,
            "Read it straight off the %s row." % asked, phase="substitute",
            done="Both parts add straight down the column."),
    ]
    return steps, want

def walk_scalar(k, vx, vy, asked):
    rx, ry = k * vx, k * vy
    want = rx if asked == 'x' else ry
    other = ry if asked == 'x' else rx
    ov = vy if asked == 'x' else vx
    wv = vx if asked == 'x' else vy
    oname = 'y' if asked == 'x' else 'x'
    steps = [
        sayonly("Scalar multiply means multiply BOTH parts by %s." % kf(k)),
        box("The %s part: %s × %s = " % (oname, kf(k), opnd(ov)), other, "Multiply, keeping the sign of the number."),
        box("The %s part, the one asked for: %s × %s = " % (asked, kf(k), opnd(wv)), want,
            "Two negatives make a positive." if (k < 0 and wv < 0) else "Multiply the two numbers.", phase="substitute"),
        box("So the %s-component = " % asked, want, "Read it off.", phase="substitute",
            done="Every part of the vector is stretched by the same number."),
    ]
    return steps, want

def walk_mag(x, y, ans):
    ax, ay = abs(x), abs(y)
    sq1, sq2 = ax * ax, ay * ay
    s = sq1 + sq2
    steps = [
        sayonly("Magnitude is the length of the arrow, found with Pythagoras on the two parts."),
        box("Square the x part: %d² = " % ax, sq1, "Multiply the number by itself."),
        box("Square the y part: %d² = " % ay, sq2, "Multiply the number by itself. A minus squared is positive."),
        box("Add the squares: %d + %d = " % (sq1, sq2), s, "Add your two results.", phase="substitute"),
        box("Square root: √%d = " % s, ans, "What number times itself gives that?", phase="substitute",
            done="That length is the magnitude."),
    ]
    return steps, ans

# ---------------------------------------------------------------------------
# Build problem banks (with fixes, hints, misconceptions, guided_steps, figures)
# ---------------------------------------------------------------------------
def mag_display(x, y, extra=""):
    return tri_svg("%d" % abs(x), "%d" % abs(y), "?", "Right-angled triangle with horizontal side %d, vertical side %d and unknown hypotenuse." % (abs(x), abs(y)))

problems_fixed = []
figures_added = []

# ---- BRONZE ----
bronze = []

# b0: (2,5)+(1,-1) x  [FIX: was (3,-1) x=5 duplicate of |(3,4)|; new (1,-1) x=3]
st, ans = walk_addsub(2, 5, 1, -1, '+', 'x')
bronze.append({
    "display": "\\(\\binom{2}{5} + \\binom{1}{-1}\\). Give the x-component.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Add the two top numbers.",
    "misconceptions": [
        {"pattern": "wrong_row", "expect": 4,
         "message": "The x-component is the top row: 2 + 1 = 3. Getting 4 means you added the bottom row instead."}
    ],
    "guided_steps": st,
})
problems_fixed.append({"tier": "bronze", "index": 0, "what": "duplicate solution 5 within bronze (also |(3,4)|); changed second vector (3,-1)->(1,-1)", "old": 5, "new": 3})

# b1: (2,5)+(1,-1) y  = 4 (unchanged value, display vector updated to match b0)
st, ans = walk_addsub(2, 5, 1, -1, '+', 'y')
bronze.append({
    "display": "\\(\\binom{2}{5} + \\binom{1}{-1}\\). Give the y-component.",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Add the two bottom numbers, keeping the minus.",
    "misconceptions": [
        {"pattern": "dropped_minus", "expect": 6,
         "message": "The bottom row is 5 + (−1) = 4. Getting 6 means the minus on −1 was dropped."}
    ],
    "guided_steps": st,
})

# b2: 3*(2,-1) x = 6
st, ans = walk_scalar(3, 2, -1, 'x')
bronze.append({
    "display": "\\(3 \\times \\binom{2}{-1}\\). Give the x-component.",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Multiply the top number by 3.",
    "misconceptions": [
        {"pattern": "added_not_multiplied", "expect": 5,
         "message": "Scalar multiply means times, not plus: 3 × 2 = 6. Getting 5 is 3 + 2."}
    ],
    "guided_steps": st,
})

# b3: (4,3)-(1,5) y = -2
st, ans = walk_addsub(4, 3, 1, 5, '-', 'y')
bronze.append({
    "display": "\\(\\binom{4}{3} - \\binom{1}{5}\\). Give the y-component.",
    "solutions": [-2], "calculator": False, "input_type": "single_value",
    "hint": "Subtract the bottom numbers in order: top vector minus bottom vector.",
    "misconceptions": [
        {"pattern": "reversed_subtraction", "expect": 2,
         "message": "Subtract in the order given: 3 − 5 = −2. Getting 2 means you did 5 − 3 the wrong way round."}
    ],
    "guided_steps": st,
})

# b4: |(3,4)| = 5  [figure]
st, ans = walk_mag(3, 4, 5)
bronze.append({
    "display": mag_display(3, 4) + "\\(|\\binom{3}{4}|\\) = ? " + CAP,
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Square each part, add, then square root.",
    "misconceptions": [
        {"pattern": "added_parts", "expect": 7,
         "message": "Magnitude is not 3 + 4. Square first: 9 + 16 = 25, then √25 = 5."},
        {"pattern": "no_square_root", "expect": 25,
         "message": "9 + 16 = 25 is only halfway. The magnitude is √25 = 5."}
    ],
    "guided_steps": st,
})
figures_added.append({"tier": "bronze", "index": 4, "kind": "svg", "what": "right triangle, legs 3 and 4, hypotenuse ? for magnitude"})

# b5: -2*(3,-4) y = 8
st, ans = walk_scalar(-2, 3, -4, 'y')
bronze.append({
    "display": "\\(-2 \\times \\binom{3}{-4}\\). Give the y-component.",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "Multiply the bottom number by −2; two minuses make a plus.",
    "misconceptions": [
        {"pattern": "sign_error", "expect": -8,
         "message": "−2 × (−4) = +8. A negative times a negative is positive, so the answer is not −8."}
    ],
    "guided_steps": st,
})

# b6: (1,2)+(-1,-2) x = 0
st, ans = walk_addsub(1, 2, -1, -2, '+', 'x')
bronze.append({
    "display": "\\(\\binom{1}{2} + \\binom{-1}{-2}\\). Give the x-component.",
    "solutions": [0], "calculator": False, "input_type": "single_value",
    "hint": "Add the top numbers, keeping the minus.",
    "misconceptions": [
        {"pattern": "dropped_minus", "expect": 2,
         "message": "1 + (−1) = 0, the zero vector. Getting 2 means the minus was ignored."}
    ],
    "guided_steps": st,
})

# b7: |(5,12)| = 13 [figure]
st, ans = walk_mag(5, 12, 13)
bronze.append({
    "display": mag_display(5, 12) + "\\(|\\binom{5}{12}|\\) = ? " + CAP,
    "solutions": [13], "calculator": False, "input_type": "single_value",
    "hint": "Square each part, add, then square root.",
    "misconceptions": [
        {"pattern": "added_parts", "expect": 17,
         "message": "Not 5 + 12. Square first: 25 + 144 = 169, then √169 = 13."},
        {"pattern": "no_square_root", "expect": 169,
         "message": "25 + 144 = 169 is only halfway. Take the square root: √169 = 13."}
    ],
    "guided_steps": st,
})
figures_added.append({"tier": "bronze", "index": 7, "kind": "svg", "what": "right triangle, legs 5 and 12, hypotenuse ? for magnitude"})

# ---- SILVER ----
silver = []

# s0: AB = OB-OA, A(1,3) B(5,7) x = 4 [figure grid]
def walk_ab(ax, ay, bx, by, asked):
    rx, ry = bx - ax, by - ay
    want = rx if asked == 'x' else ry
    other = ry if asked == 'x' else rx
    steps = [
        sayonly("To travel A to B, subtract the start from the end: \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\)."),
        box("The %s part: %d − %d = " % ('y' if asked=='x' else 'x', by if asked=='x' else bx, ay if asked=='x' else ax),
            other, "End minus start, down that row."),
        box("The %s part, the one asked for: %d − %d = " % (asked, bx if asked=='x' else by, ax if asked=='x' else ay),
            want, "End minus start: B row take away A row.", phase="substitute"),
        box("So the x-component of AB = " if asked=='x' else "So the y-component of AB = ", want,
            "Read it off.", phase="substitute", done="AB always goes end minus start, never start minus end."),
    ]
    return steps, want
st, ans = walk_ab(1, 3, 5, 7, 'x')
silver.append({
    "display": ab_grid() + "OA = \\(\\binom{1}{3}\\), OB = \\(\\binom{5}{7}\\). Find AB's x-component. " + CAP,
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "AB = OB − OA, so subtract the x-coordinates.",
    "misconceptions": [
        {"pattern": "reversed", "expect": -4,
         "message": "AB = b − a = 5 − 1 = 4. Getting −4 is a − b, the wrong way round (that would be BA)."}
    ],
    "guided_steps": st,
})
figures_added.append({"tier": "silver", "index": 0, "kind": "svg", "what": "grid with A(1,3), B(5,7) and vector AB"})

# s1: 2a-3b x, a(4,1) b(2,-1) = 2
def walk_comb(ma, a, mb, b, asked):
    # ma*a + mb*b (mb may be negative)
    idx = 0 if asked == 'x' else 1
    oidx = 1 - idx
    ta = ma * a[idx]; tb = mb * b[idx]
    want = ta + tb
    to_a = ma * a[oidx]; to_b = mb * b[oidx]
    other = to_a + to_b
    def combo(oi):
        return "%s × %s and %s × %s" % (kf(ma), opnd(a[oi]), kf(mb), opnd(b[oi]))
    steps = [
        sayonly("Scale each vector first, then combine the matching parts."),
        box("The %s parts: %s, combined = " % ('y' if asked == 'x' else 'x', combo(oidx)), other,
            "Work out each product, then combine them (a minus coefficient subtracts)."),
        box("The %s parts: %s, combined = " % (asked, combo(idx)), want,
            "Multiply each, watching signs, then combine.", phase="substitute"),
        box("So the %s-component = " % asked, want, "Read it off.", phase="substitute", done="Scale, then combine, one row at a time."),
    ]
    return steps, want
st, ans = walk_comb(2, (4, 1), -3, (2, -1), 'x')
silver.append({
    "display": "\\(2\\mathbf{a} - 3\\mathbf{b}\\) where \\(\\mathbf{a} = \\binom{4}{1}\\), \\(\\mathbf{b} = \\binom{2}{-1}\\). Give x-component.",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Work out 2×4 then subtract 3×2.",
    "misconceptions": [
        {"pattern": "added_not_subtracted", "expect": 14,
         "message": "It is 2a minus 3b: 8 − 6 = 2. Getting 14 means you added (8 + 6)."}
    ],
    "guided_steps": st,
})

# s2: 2a-3b y = 5
st, ans = walk_comb(2, (4, 1), -3, (2, -1), 'y')
silver.append({
    "display": "\\(2\\mathbf{a} - 3\\mathbf{b}\\) where \\(\\mathbf{a} = \\binom{4}{1}\\), \\(\\mathbf{b} = \\binom{2}{-1}\\). Give y-component.",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Work out 2×1 then subtract 3×(−1).",
    "misconceptions": [
        {"pattern": "double_negative", "expect": -1,
         "message": "2(1) − 3(−1) = 2 + 3 = 5. Subtracting a negative adds; getting −1 dropped that."}
    ],
    "guided_steps": st,
})

# s3: parallel (2,6)&(3,9) -> 1 [figure]
silver.append({
    "display": parallel_svg() + "Are \\(\\binom{2}{6}\\) and \\(\\binom{3}{9}\\) parallel? Enter 1 for Yes, 0 for No.",
    "solutions": [1], "calculator": False, "input_type": "single_value",
    "hint": "Check if one vector is a single number times the other.",
    "misconceptions": [
        {"pattern": "thinks_not_parallel", "expect": 0,
         "message": "(3,9) = 1.5 × (2,6): the SAME multiplier works for both parts, so they are parallel. Answer 1."}
    ],
    "guided_steps": [
        sayonly("Parallel means one vector is a scalar multiple of the other: the same number times BOTH parts."),
        box("Compare the x parts: 3 ÷ 2 = ", 1.5, "Divide the x of the second by the x of the first."),
        box("Compare the y parts: 9 ÷ 6 = ", 1.5, "Divide the y of the second by the y of the first.", phase="substitute"),
        box("Same multiplier both times means parallel. Enter 1 for Yes: ", 1, "The two ratios matched, so type 1.", phase="substitute", done="Equal ratios in both parts is the parallel test."),
    ],
})

# s4: midpoint A(2,4) B(10,10) x [FIX from B(8,10) x=5 dup -> x=6] [figure]
def walk_mid(ax, ay, bx, by, asked):
    rx, ry = (ax + bx) / 2, (ay + by) / 2
    want = rx if asked == 'x' else ry
    other = ry if asked == 'x' else rx
    want = int(want) if want == int(want) else want
    other = int(other) if other == int(other) else other
    steps = [
        sayonly("The midpoint is the average of the two ends: add the coordinates and halve."),
        box("The %s coordinate: (%d + %d) ÷ 2 = " % ('y' if asked=='x' else 'x', ay if asked=='x' else ax, by if asked=='x' else bx), other, "Add the two, then halve."),
        box("The %s coordinate, the one asked for: (%d + %d) ÷ 2 = " % (asked, ax if asked=='x' else ay, bx if asked=='x' else by), want, "Add the two x values, then halve.", phase="substitute"),
        box("So M's %s-component = " % asked, want, "Read it off.", phase="substitute", done="Midpoint is just the average of each coordinate."),
    ]
    return steps, want
st, ans = walk_mid(2, 4, 10, 10, 'x')
silver.append({
    "display": line_points_svg([("A", 0.0), ("M", 0.5), ("B", 1.0)], "A line segment AB with midpoint M marked exactly halfway.") +
               "M is the midpoint of AB. A = \\(\\binom{2}{4}\\), B = \\(\\binom{10}{10}\\). Find M's x-component. " + CAP,
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Average the two x-coordinates: add them and halve.",
    "misconceptions": [
        {"pattern": "subtracted", "expect": 4,
         "message": "Midpoint averages, not subtracts: (2 + 10) ÷ 2 = 6. Getting 4 is (10 − 2) ÷ 2."},
        {"pattern": "forgot_halve", "expect": 12,
         "message": "2 + 10 = 12 is only half done. Divide by 2 to get the midpoint: 6."}
    ],
    "guided_steps": st,
})
problems_fixed.append({"tier": "silver", "index": 4, "what": "duplicate solution 5 within silver; changed B from (8,10) to (10,10) so midpoint x = 6", "old": 5, "new": 6})
figures_added.append({"tier": "silver", "index": 4, "kind": "svg", "what": "segment AB with midpoint M"})

# s5: |(-6,8)| = 10 [FIX from |(-3,4)|=5 dup] [figure]
st, ans = walk_mag(-6, 8, 10)
silver.append({
    "display": mag_display(-6, 8) + "\\(|\\binom{-6}{8}|\\) = ? " + CAP,
    "solutions": [10], "calculator": False, "input_type": "single_value",
    "hint": "Square each part (a minus squared is positive), add, then square root.",
    "misconceptions": [
        {"pattern": "no_square_root", "expect": 100,
         "message": "36 + 64 = 100 is only halfway. The magnitude is √100 = 10."},
        {"pattern": "added_parts", "expect": 14,
         "message": "Not 6 + 8. Square first: 36 + 64 = 100, then √100 = 10."}
    ],
    "guided_steps": st,
})
problems_fixed.append({"tier": "silver", "index": 5, "what": "duplicate solution 5 within silver (three 5s); changed |(-3,4)|=5 to |(-6,8)|=10", "old": 5, "new": 10})
figures_added.append({"tier": "silver", "index": 5, "kind": "svg", "what": "right triangle, legs 6 and 8, hypotenuse ? for magnitude"})

# s6: (6,-8) = k(3,k) find k = -4
silver.append({
    "display": "\\(\\binom{6}{-8}\\) is a scalar multiple of \\(\\binom{3}{k}\\). Find \\(k\\).",
    "solutions": [-4], "calculator": False, "input_type": "single_value",
    "hint": "Find the multiplier from the x parts first, then apply it to the y parts.",
    "misconceptions": [
        {"pattern": "dropped_minus", "expect": 4,
         "message": "The multiplier is 6 ÷ 3 = 2, so k = −8 ÷ 2 = −4. Getting 4 dropped the minus sign."}
    ],
    "guided_steps": [
        sayonly("A scalar multiple stretches both parts by the SAME number. Find that number from the parts you know."),
        box("The x parts go 3 to 6, so the multiplier is 6 ÷ 3 = ", 2, "Divide the new x by the old x."),
        box("Apply it to the y parts: the (3,k) becomes (6,−8), so 2 × k = −8. Then k = −8 ÷ 2 = ", -4, "Divide −8 by the multiplier 2.", phase="substitute"),
        box("So k = ", -4, "Read it off, keeping the minus.", phase="substitute", done="Same multiplier on both parts is what makes them a scalar multiple."),
    ],
})

# ---- GOLD ----
gold = []

# g0: OM = 1/2(a+b), a(2,6) b(10,2) x = 6 [figure]
gold.append({
    "display": om_schematic() + "OA = a, OB = b. M is the midpoint of AB. Find OM in terms of a and b, then with a = \\(\\binom{2}{6}\\) and b = \\(\\binom{10}{2}\\), find OM's x-component. " + CAP,
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "OM = ½(a + b); add the x parts and halve.",
    "misconceptions": [
        {"pattern": "forgot_halve", "expect": 12,
         "message": "OM = ½(a + b). The x parts give 2 + 10 = 12, then halve to 6. Getting 12 skipped the halving."},
        {"pattern": "used_half_ab", "expect": 4,
         "message": "OM is not ½(b − a). It is ½(a + b): (2 + 10) ÷ 2 = 6, not (10 − 2) ÷ 2 = 4."}
    ],
    "guided_steps": [
        sayonly("To reach M, go to A then half of AB: \\(OM = a + \\tfrac{1}{2}(b - a) = \\tfrac{1}{2}(a + b)\\). It is the average of a and b."),
        box("Add the y parts of a and b: 6 + 2 = ", 8, "Add the bottom rows."),
        box("Halve it for OM's y part: 8 ÷ 2 = ", 4, "Divide by 2."),
        box("Now the x parts, the one asked for: add 2 + 10 = ", 12, "Add the top rows.", phase="substitute"),
        box("Halve it: 12 ÷ 2 = ", 6, "Divide by 2 to reach the midpoint.", phase="substitute", done="OM = ½(a + b), so each part is the average."),
    ],
})
figures_added.append({"tier": "gold", "index": 0, "kind": "svg", "what": "position-vector diagram: O, a to A, b to B, midpoint M"})

# g1: P = A + 1/3(B-A), A(1,3) B(7,9) ratio 1:2, y = 5 [figure]
gold.append({
    "display": line_points_svg([("A", 0.0), ("P", 1.0/3), ("B", 1.0)], "Line segment AB with P one third of the way from A to B.", "AP : PB = 1 : 2") +
               "P divides AB in ratio 1:2. A = \\(\\binom{1}{3}\\), B = \\(\\binom{7}{9}\\). Find P's y-component. " + CAP,
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "AP:PB = 1:2 puts P one third of the way from A to B.",
    "misconceptions": [
        {"pattern": "used_midpoint", "expect": 6,
         "message": "Ratio 1:2 means P is ⅓ along, not halfway. P's y = 3 + ⅓(9 − 3) = 5, not the midpoint 6."},
        {"pattern": "used_two_thirds", "expect": 7,
         "message": "AP:PB = 1:2 gives the fraction ⅓ (the 1 out of 1+2). Using ⅔ gives 7; the correct y is 3 + ⅓(6) = 5."}
    ],
    "guided_steps": [
        sayonly("Ratio 1:2 splits AB into 3 equal parts, and P is 1 part along, so P = A + \\(\\tfrac{1}{3}\\)(B − A)."),
        box("First the fraction: 1 out of (1 + 2) parts, so the fraction is 1 ÷ 3 which we use as ⅓. The step B − A in y is 9 − 3 = ", 6, "End minus start on the y row."),
        box("Take a third of that: 6 ÷ 3 = ", 2, "Divide the rise by 3.", phase="substitute"),
        box("Add it onto A's y: 3 + 2 = ", 5, "Start at A's y and move a third of the way.", phase="substitute", done="P = A + ⅓(B − A), one third from A to B."),
    ],
})
figures_added.append({"tier": "gold", "index": 1, "kind": "svg", "what": "segment AB with P at 1/3 (ratio 1:2)"})

# g2: collinear A(1,2) B(4,6) C(7,10), AB x = 3 [figure]
gold.append({
    "display": line_points_svg([("A", 0.0), ("B", 0.5), ("C", 1.0)], "Three points A, B and C lying on one straight line, equally spaced.") +
               "Show that A(1,2), B(4,6), C(7,10) are collinear. AB has what x-component? " + CAP,
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "AB = B − A; subtract the x-coordinates.",
    "misconceptions": [
        {"pattern": "reversed", "expect": -3,
         "message": "AB = B − A = 4 − 1 = 3. Getting −3 is A − B, the reverse direction."}
    ],
    "guided_steps": [
        sayonly("Collinear means the points lie on one straight line: AB and BC must be parallel and share B."),
        box("AB in y: 6 − 2 = ", 4, "End minus start on the y row."),
        box("AB in x, the one asked for: 4 − 1 = ", 3, "End minus start on the x row.", phase="substitute"),
        box("Check BC in x: 7 − 4 = ", 3, "BC has the same x-step, so BC = AB and the points are collinear.", phase="substitute", done="AB = BC = (3,4) and they share B, so A, B, C are collinear."),
    ],
})
figures_added.append({"tier": "gold", "index": 2, "kind": "svg", "what": "three collinear points A, B, C"})

# g3: |(a,a)| = 10 -> a = 7.1 (calculator) [figure]
gold.append({
    "display": tri_svg("a", "a", "10", "Right-angled triangle with both shorter sides equal to a and hypotenuse 10.") +
               "\\(|\\binom{a}{a}| = 10\\). Find \\(a\\) (positive value). To 1 d.p. " + CAP,
    "solutions": [7.1], "calculator": True, "input_type": "single_value",
    "hint": "Set up a² + a² = 10², then solve for a.",
    "misconceptions": [
        {"pattern": "halved", "expect": 5,
         "message": "It is not 2a = 10. Pythagoras gives a² + a² = 100, so 2a² = 100 and a = √50 ≈ 7.1, not 5."},
        {"pattern": "forgot_double", "expect": 10,
         "message": "There are TWO a² terms: 2a² = 100, so a² = 50 and a ≈ 7.1. Treating it as a² = 100 gives a = 10, forgetting the second a²."}
    ],
    "guided_steps": [
        sayonly("Magnitude squared: \\(a^2 + a^2 = 10^2\\). Both parts are a, so there are two a² terms."),
        box("Square the length: 10² = ", 100, "Ten times ten."),
        box("Combine the two a² terms: a² + a² = ", 2, "How many a² is that? Type the number in front.", post="a²"),
        box("So 2a² = 100, giving a² = 100 ÷ 2 = ", 50, "Divide 100 by 2.", phase="substitute"),
        box("Square root for a: √50 = ", 7.1, "Use your calculator, round to 1 d.p.", phase="substitute", done="a ≈ 7.1, and 7.1² + 7.1² ≈ 100."),
    ],
})
figures_added.append({"tier": "gold", "index": 3, "kind": "svg", "what": "right triangle, legs a and a, hypotenuse 10"})

# g4: P = A + 2/3(B-A), A(3,1) B(9,5) ratio 2:1, x = 7 [figure]
gold.append({
    "display": line_points_svg([("A", 0.0), ("P", 2.0/3), ("B", 1.0)], "Line segment AB with P two thirds of the way from A to B.", "AP : PB = 2 : 1") +
               "A = \\(\\binom{3}{1}\\), B = \\(\\binom{9}{5}\\). Point P is on AB such that AP:PB = 2:1. Find P's x-component. " + CAP,
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "AP:PB = 2:1 puts P two thirds of the way from A to B.",
    "misconceptions": [
        {"pattern": "used_one_third", "expect": 5,
         "message": "AP:PB = 2:1 makes the fraction ⅔ (the 2 out of 2+1). Using ⅓ gives 5; the correct x is 3 + ⅔(6) = 7."},
        {"pattern": "used_midpoint", "expect": 6,
         "message": "Ratio 2:1 is not halfway. P is ⅔ along: 3 + ⅔(9 − 3) = 7, not the midpoint 6."}
    ],
    "guided_steps": [
        sayonly("Ratio 2:1 splits AB into 3 equal parts, and P is 2 parts along, so P = A + \\(\\tfrac{2}{3}\\)(B − A)."),
        box("The step B − A in x: 9 − 3 = ", 6, "End minus start on the x row."),
        box("Take two thirds of it: 6 × 2 ÷ 3 = ", 4, "Two thirds of the run.", phase="substitute"),
        box("Add it onto A's x: 3 + 4 = ", 7, "Start at A's x and move two thirds of the way.", phase="substitute", done="P = A + ⅔(B − A), two thirds from A to B."),
    ],
})
figures_added.append({"tier": "gold", "index": 4, "kind": "svg", "what": "segment AB with P at 2/3 (ratio 2:1)"})

# ---------------------------------------------------------------------------
# tier descriptions
# ---------------------------------------------------------------------------
problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Work down the columns: add, subtract or scalar-multiply the two parts, and find a magnitude with Pythagoras.",
    "silver_description": "Combine and compare vectors: AB = b − a, mixtures like 2a − 3b, midpoints, the parallel test and finding a missing part.",
    "gold_description": "Position vectors in problems: midpoints and points dividing a line in a ratio, collinearity, and magnitude equations.",
}

# ---------------------------------------------------------------------------
# tier_guides
# ---------------------------------------------------------------------------
tier_guides = {
    "bronze": {
        "title": "Bronze: column-vector arithmetic",
        "steps": [
            "A vector \\(\\binom{x}{y}\\) is an instruction: x across, y up. To <strong>add</strong> or <strong>subtract</strong>, work straight down the columns, matching part with matching part.",
            "To <strong>scalar multiply</strong>, multiply BOTH parts by the number, keeping every sign.",
            "The <strong>magnitude</strong> (length) uses Pythagoras: \\(|\\binom{x}{y}| = \\sqrt{x^2 + y^2}\\)."
        ],
        "example": {
            "question": "Find \\(\\binom{3}{1} + \\binom{2}{4}\\), then its magnitude.",
            "steps": [
                {"label": "Add x parts", "content": "<p>\\(3 + 2 = 5\\)</p>"},
                {"label": "Add y parts", "content": "<p>\\(1 + 4 = 5\\)</p>"},
                {"label": "Magnitude", "content": "<p>\\(\\sqrt{5^2 + 5^2} = \\sqrt{50}\\)</p>"},
                {"label": "Check", "content": "<p>\\(\\sqrt{50} \\approx 7.07\\), a bit longer than each part</p>"},
                {"label": "Answer", "content": "<p>\\(\\binom{5}{5}\\), magnitude \\(\\sqrt{50} \\approx 7.1\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: combining and comparing vectors",
        "steps": [
            "To go from A to B, subtract start from end: \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\). The <strong>midpoint</strong> is the average of the ends.",
            "For a mixture like \\(2\\mathbf{a} - 3\\mathbf{b}\\), scale each vector first, then combine one row at a time, watching signs.",
            "Two vectors are <strong>parallel</strong> when one is a scalar multiple of the other: the same number times BOTH parts."
        ],
        "example": {
            "question": "OA = \\(\\binom{2}{1}\\), OB = \\(\\binom{6}{4}\\). Find AB.",
            "steps": [
                {"label": "Rule", "content": "<p>\\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\)</p>"},
                {"label": "x part", "content": "<p>\\(6 - 2 = 4\\)</p>"},
                {"label": "y part", "content": "<p>\\(4 - 1 = 3\\)</p>"},
                {"label": "Check", "content": "<p>From A, move 4 right and 3 up to reach B</p>"},
                {"label": "Answer", "content": "<p>\\(\\vec{AB} = \\binom{4}{3}\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: position vectors, midpoints and ratios",
        "steps": [
            "Build a route from vectors you know. Midpoint of AB: \\(OM = \\tfrac{1}{2}(\\mathbf{a} + \\mathbf{b})\\).",
            "A point dividing AB in ratio \\(m:n\\) sits a fraction \\(\\tfrac{m}{m+n}\\) along: \\(P = \\mathbf{a} + \\tfrac{m}{m+n}(\\mathbf{b} - \\mathbf{a})\\).",
            "Points are <strong>collinear</strong> when two vectors along them are parallel and share a point."
        ],
        "example": {
            "question": "A = \\(\\binom{1}{2}\\), B = \\(\\binom{7}{8}\\). Find the midpoint M.",
            "steps": [
                {"label": "Rule", "content": "<p>\\(M = \\tfrac{1}{2}(\\mathbf{a} + \\mathbf{b})\\)</p>"},
                {"label": "Add", "content": "<p>\\(\\binom{1}{2} + \\binom{7}{8} = \\binom{8}{10}\\)</p>"},
                {"label": "Halve", "content": "<p>\\(\\tfrac{1}{2}\\binom{8}{10} = \\binom{4}{5}\\)</p>"},
                {"label": "Check", "content": "<p>\\(\\binom{4}{5}\\) is halfway between A and B</p>"},
                {"label": "Answer", "content": "<p>\\(M = \\binom{4}{5}\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# guided (opener + teach)
# ---------------------------------------------------------------------------
guided = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_grid() + "You follow a treasure map. From Start you walk <strong>3 squares east and 2 north</strong>, then <strong>1 square east and 4 north</strong> to the treasure.",
        "steps": [
            {"say": "No algebra, just count squares on the map.",
             "pre": "How many squares EAST in total? ", "post": "", "answer": 4,
             "hint": "Add the two eastward moves: 3 then 1."},
            {"say": "Now the other direction.",
             "pre": "How many squares NORTH in total? ", "post": "", "answer": 6,
             "hint": "Add the two northward moves: 2 then 4."},
            {"say": "That is all a vector sum is. Each leg is a column vector, east on top, north below: \\(\\binom{3}{2} + \\binom{1}{4} = \\binom{4}{6}\\). You just added them by working down each column."}
        ]
    },
    "teach": {
        "bronze": {
            "display": "Find \\(\\binom{3}{1} + \\binom{0}{3}\\), then the magnitude of the result.",
            "label": "Together: your first one",
            "steps": [
                {"say": "Add by working down the columns. Start with the x parts (top row):",
                 "pre": "3 + 0 = ", "post": "x", "answer": 3, "hint": "Add the two top numbers."},
                {"say": None, "pre": "Now the y parts (bottom row): 1 + 3 = ", "post": "y", "answer": 4,
                 "hint": "Add the two bottom numbers."},
                {"say": "The result is \\(\\binom{3}{4}\\). Its length uses Pythagoras: square each part and add.",
                 "pre": "3² + 4² = ", "post": "", "answer": 25, "hint": "9 + 16."},
                {"pre": "√25 = ", "post": "", "answer": 5, "done": "That was the whole point: add down the columns, then Pythagoras for length.",
                 "hint": "What times itself is 25?"}
            ]
        },
        "silver": {
            "display": "OA = \\(\\binom{2}{1}\\), OB = \\(\\binom{6}{4}\\). Find AB and its magnitude.",
            "label": "Together: the silver move",
            "steps": [
                {"say": "The new move: to go A to B, subtract start from end, \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\). x parts first:",
                 "pre": "6 − 2 = ", "post": "x", "answer": 4, "hint": "End minus start on the top row."},
                {"say": None, "pre": "y parts: 4 − 1 = ", "post": "y", "answer": 3,
                 "hint": "End minus start on the bottom row."},
                {"say": "So \\(\\vec{AB} = \\binom{4}{3}\\). Now its length with Pythagoras:",
                 "pre": "4² + 3² = ", "post": "", "answer": 25, "hint": "16 + 9."},
                {"pre": "√25 = ", "post": "", "answer": 5, "done": "AB is end minus start, then Pythagoras gives its length.",
                 "hint": "What times itself is 25?"}
            ]
        },
        "gold": {
            "display": "OA = a = \\(\\binom{4}{2}\\), OB = b = \\(\\binom{8}{6}\\). M is the midpoint of AB. Find OM.",
            "label": "Together: the gold move",
            "steps": [
                {"say": "The new move: the midpoint is the average, \\(OM = \\tfrac{1}{2}(\\mathbf{a} + \\mathbf{b})\\). Add the x parts first:",
                 "pre": "4 + 8 = ", "post": "", "answer": 12, "hint": "Add the two top numbers."},
                {"say": None, "pre": "Add the y parts: 2 + 6 = ", "post": "", "answer": 8,
                 "hint": "Add the two bottom numbers."},
                {"say": "Now halve each part to reach the midpoint. x:",
                 "pre": "12 ÷ 2 = ", "post": "", "answer": 6, "hint": "Half of 12."},
                {"pre": "y: 8 ÷ 2 = ", "post": "", "answer": 4, "done": "OM = ½(a + b), so each part is just the average of the ends.",
                 "hint": "Half of 8."}
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# method_card (slim: <=4 steps, content <=140 words)
# ---------------------------------------------------------------------------
method_card = {
    "title": "Vectors",
    "steps": [
        "Add or subtract: work down the columns, matching part with matching part.",
        "Scalar multiply: multiply BOTH parts by the number, keeping signs.",
        "Length: \\(|\\binom{x}{y}| = \\sqrt{x^2 + y^2}\\) (Pythagoras).",
        "A to B: \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\); parallel means one is a scalar multiple of the other."
    ],
    "content": "<p>A <strong>vector</strong> has size and direction, written \\(\\binom{x}{y}\\) or \\(\\mathbf{a}\\). Combine them by working down the columns; a scalar stretches both parts. The <strong>magnitude</strong> is the arrow's length by Pythagoras.</p><p>The <strong>midpoint</strong> of AB is \\(\\tfrac{1}{2}(\\mathbf{a} + \\mathbf{b})\\); a point splitting AB in ratio \\(m:n\\) is \\(\\mathbf{a} + \\tfrac{m}{m+n}(\\mathbf{b} - \\mathbf{a})\\).</p>",
    "example": "<p><strong>\\(\\mathbf{a} = \\binom{3}{1}\\), \\(\\mathbf{b} = \\binom{-1}{4}\\). Find \\(2\\mathbf{a} + \\mathbf{b}\\).</strong></p><p>\\(\\binom{6}{2} + \\binom{-1}{4} = \\binom{5}{6}\\).</p>"
}

# ---------------------------------------------------------------------------
# assemble: preserve related_videos, topic_links, worked_examples byte-for-byte
# ---------------------------------------------------------------------------
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": problem_bank,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
    "tier_guides": tier_guides,
    "guided": guided,
}

json.dump(out, io.open('lesson_maths-ocr_geometry-L08.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("wrote lesson_maths-ocr_geometry-L08.json")

# ---------------------------------------------------------------------------
# self-check: recompute final live box of every guided_steps == solution
# ---------------------------------------------------------------------------
bad = 0
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(out["problem_bank"][tier]):
        gs = p.get("guided_steps")
        sol = p["solutions"][0]
        if not gs:
            print("NO WALK", tier, i); bad += 1; continue
        live_boxes = [s for s in gs if s.get("phase") == "substitute" and s.get("answer") is not None]
        if not live_boxes:
            print("no substitute boxes", tier, i); bad += 1; continue
        final = live_boxes[-1]["answer"]
        if abs(float(final) - float(sol)) > 1e-9:
            print("FINAL MISMATCH", tier, i, "final", final, "sol", sol); bad += 1
        # every misconception expect != solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(float(e) - float(sol)) < 1e-9:
                print("EXPECT==SOL", tier, i, e); bad += 1
print("self-check issues:", bad)
print("problems_fixed:", len(problems_fixed), "figures_added:", len(figures_added))
