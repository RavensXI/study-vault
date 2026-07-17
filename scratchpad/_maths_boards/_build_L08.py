# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_L08.json", encoding="utf-8"))

# ---------- FIGURE HELPERS ----------
def cap():
    return '<span class="figure-caption">Diagram not drawn accurately</span>'

# Schematic triangle O-A-B
O = (28.0, 132.0); A = (196.0, 132.0); B = (84.0, 28.0)

def dot(p, r=2.1):
    return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="currentColor"/>'
def line(p, q, w=1.5, dash=False):
    d = ' stroke-dasharray="4 3"' if dash else ''
    return f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="currentColor" stroke-width="{w}"{d}/>'
def txt(p, s, size=12, weight="600", anchor="middle"):
    return f'<text x="{p[0]}" y="{p[1]}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="currentColor">{s}</text>'

def tri(aria, a_lbl, b_lbl, extras, target=None, mark_ab=None):
    # extras: list of (point, label); target: (p,q,label); mark_ab: label to put at AB midpoint
    s = (f'<svg viewBox="0 0 240 160" role="img" aria-label="{aria}" '
         'style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">')
    s += line(O, A) + line(O, B) + line(A, B)
    if target:
        s += line(target[0], target[1], w=1.4, dash=True)
    s += dot(O) + dot(A) + dot(B)
    s += txt((20.0, 140.0), "O") + txt((204.0, 140.0), "A") + txt((80.0, 20.0), "B")
    s += txt((108.0, 149.0), a_lbl, size=11)          # side OA label
    s += txt((34.0, 78.0), b_lbl, size=11)            # side OB label
    for p, lbl in extras:
        s += dot(p) + txt((p[0] + 8, p[1] - 6), lbl, size=11)
    if target:
        mx = round((target[0][0] + target[1][0]) / 2 + 6, 1)
        my = round((target[0][1] + target[1][1]) / 2 - 4, 1)
        s += txt((mx, my), target[2], size=11)
    if mark_ab:
        s += txt((150.0, 74.0), mark_ab, size=11)
    s += '</svg>'
    return s + cap() + ' '

MID_AB = (140.0, 80.0)
P_s5   = (168.0, 106.0)
P_g2   = (140.0, 132.0)
Q_g2   = (47.0, 97.0)
X_g0   = (188.0, 64.0)
M_g4   = (112.0, 132.0)
N_g4   = (56.0, 80.0)

def mag_fig(x, y, aria):
    ax, ay = abs(x), abs(y)
    sc = 88.0 / max(ax, ay)
    w = round(ax * sc, 1); h = round(ay * sc, 1)
    cx, cy = 40.0, 124.0
    R = (round(cx + w, 1), cy)
    T = (cx, round(cy - h, 1))
    s = (f'<svg viewBox="0 0 200 150" role="img" aria-label="{aria}" '
         'style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">')
    s += line((cx, cy), R, 1.6) + line((cx, cy), T, 1.6) + line(R, T, 1.6)
    # right angle square at corner
    s += (f'<path d="M {cx+9} {cy} L {cx+9} {cy-9} L {cx} {cy-9}" fill="none" '
          'stroke="currentColor" stroke-width="1"/>')
    s += txt((round((cx + R[0]) / 2, 1), 139.0), str(ax), size=11)
    s += txt((22.0, round((cy + T[1]) / 2, 1)), str(ay), size=11)
    hx = round((R[0] + T[0]) / 2 + 8, 1); hy = round((R[1] + T[1]) / 2 - 4, 1)
    s += txt((hx, hy), "?", size=12)
    s += '</svg>'
    return s + cap() + ' '

# Opener grid figure
def opener_grid():
    cell = 22.0; ox, oy = 24.0, 168.0
    S = (ox, oy)
    P = (ox + 3 * cell, oy - 2 * cell)   # (90,124)
    E = (ox + 4 * cell, oy - 7 * cell)   # (112,14)
    s = ('<svg viewBox="0 0 150 186" role="img" '
         'aria-label="A grid path: 3 east and 2 north, then 1 east and 5 north" '
         'style="max-width:260px;font-family:Inter,sans-serif" stroke-linecap="round">')
    # grid
    for c in range(5):
        gx = ox + c * cell
        s += f'<line x1="{gx}" y1="14" x2="{gx}" y2="{oy}" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>'
    for r in range(8):
        gy = oy - r * cell
        s += f'<line x1="{ox}" y1="{gy}" x2="{ox+4*cell}" y2="{gy}" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>'
    # legs
    s += line(S, P, 2.0) + line(P, E, 2.0)
    s += dot(S, 2.6) + dot(P, 2.3) + dot(E, 2.6)
    s += txt((14.0, 178.0), "S", size=11)
    s += txt((57.0, 150.0), "3 E, 2 N", size=9, weight="500")
    s += txt((100.0, 74.0), "1 E, 5 N", size=9, weight="500", anchor="end")
    s += '</svg>'
    return s + '<br>'

# teach.silver figure: triangle O,A,B, M midpoint OB, AM dashed
def teach_silver_fig():
    M = (56.0, 80.0)  # midpoint OB
    return tri("Triangle O A B with M the midpoint of O B and A M dashed",
               "a", "b", [(M, "M")], target=(A, M, "?"))

pb = live["problem_bank"]

# ---------- helper to build a step ----------
def box(pre, answer, hint, phase=False, done=None):
    d = {"pre": pre, "post": "", "answer": answer, "hint": hint}
    if phase:
        d["phase"] = "substitute"
    if done:
        d["done"] = done
    return d
def say(s):
    return {"say": s}

# ============ BRONZE ============
bz = pb["bronze"]
# b0 a+b
bz[0]["display"] = "\\(\\mathbf{a} = \\binom{3}{2}\\) and \\(\\mathbf{b} = \\binom{1}{5}\\). Find \\(\\mathbf{a} + \\mathbf{b}\\)."
bz[0]["hint"] = "Add the tops, then add the bottoms."
bz[0]["misconceptions"] = [{
    "pattern": "subtracted",
    "expect": 1,
    "message": "You subtracted instead of added. To add, sum each row: 3 + 1 and 2 + 5 give (4, 7)."
}]
bz[0]["guided_steps"] = [
    say("To add two vectors, add the top numbers, then add the bottom numbers."),
    box("Add the top numbers: 3 + 1 = ", 4, "3 plus 1."),
    box("Add the bottom numbers: 2 + 5 = ", 7, "2 plus 5.", phase=True),
    box("Subtract b's top back to check: 4 − 1 = ", 3, "Should return a's top, 3.",
        done="Back to a = (3, 2), so a + b = (4, 7)."),
]
# b1 2a
bz[1]["hint"] = "Multiply both numbers by 2, keeping signs."
bz[1]["misconceptions"] = [
    {"pattern": "added_two", "expect": 1,
     "message": "You added 2 to each number. Doubling means multiply: 5 × 2 and (−1) × 2 give (10, −2)."},
    {"pattern": "dropped_sign", "expect": 2,
     "message": "Keep the minus sign: (−1) × 2 = −2, not 2."},
]
bz[1]["guided_steps"] = [
    say("To double a vector, multiply both numbers by 2."),
    box("Top: 5 × 2 = ", 10, "Twice 5."),
    box("Bottom: (−1) × 2 = ", -2, "Keep the minus sign.", phase=True),
    box("Halve the top back to check: 10 ÷ 2 = ", 5, "Should return a's top, 5.",
        done="Back to (5, −1), so 2a = (10, −2)."),
]
# b2 |(5,12)|
bz[2]["display"] = mag_fig(5, 12, "Right-angled triangle with legs 5 and 12, hypotenuse marked question mark") + "Find the magnitude of \\(\\binom{5}{12}\\)."
bz[2]["hint"] = "Square each number, add them, then square root."
bz[2]["misconceptions"] = [{
    "pattern": "added_components", "expect": 17,
    "message": "You added the numbers. Magnitude squares them first: √(5² + 12²) = √169 = 13."
}]
bz[2]["guided_steps"] = [
    say("Magnitude squares each number, adds them, then takes the square root."),
    box("5² = ", 25, "5 times 5."),
    box("12² = ", 144, "12 times 12."),
    box("Add: 25 + 144 = ", 169, "Sum the squares.", phase=True),
    box("√169 = ", 13, "What squares to 169?", done="|v| = 13."),
]
# b3 AB
bz[3]["display"] = tri("Triangle O A B with sides O A labelled a and O B labelled b", "a", "b", [], mark_ab="?") + "\\(\\overrightarrow{OA} = \\mathbf{a}\\) and \\(\\overrightarrow{OB} = \\mathbf{b}\\). Express \\(\\overrightarrow{AB}\\) in terms of \\(\\mathbf{a}\\) and \\(\\mathbf{b}\\)."
bz[3]["hint"] = "Go from A back to O, then O to B."
bz[3]["misconceptions"] = [{
    "pattern": "wrong_direction", "expect": 1,
    "message": "You went the wrong way. AB starts at A: AB = −a + b = b − a, not a − b."
}]
bz[3]["guided_steps"] = [
    say("To go A to B, travel A to O, then O to B: \\(\\overrightarrow{AB} = \\overrightarrow{AO} + \\overrightarrow{OB}\\)."),
    box("OA = a, so AO reverses it. Coefficient of a in AO = ", -1, "Reversing flips the sign."),
    box("O to B is b, so the coefficient of b = ", 1, "OB = b."),
    box("Collect: coefficient of a in AB = ", -1, "Only AO has an a.", phase=True),
    box("Coefficient of b in AB = ", 1, "Only OB has a b.", done="AB = −a + b = b − a."),
]
# b4 p-q
bz[4]["hint"] = "Subtract q from p, row by row."
bz[4]["misconceptions"] = [
    {"pattern": "added", "expect": 1,
     "message": "You added. Subtracting q means change its signs: (4 − (−1), −3 − 2) = (5, −5)."},
    {"pattern": "reversed", "expect": 2,
     "message": "That is q − p, the reverse. Take q from p: (5, −5), not (−5, 5)."},
]
bz[4]["guided_steps"] = [
    say("To subtract, subtract the top numbers, then the bottom numbers."),
    box("Top: 4 − (−1) = ", 5, "Subtracting a negative adds."),
    box("Bottom: −3 − 2 = ", -5, "Go more negative.", phase=True),
    box("Add q's top back to check: 5 + (−1) = ", 4, "Should return p's top, 4.",
        done="Back to p = (4, −3), so p − q = (5, −5)."),
]
# b5 |(-3,4)|
bz[5]["display"] = mag_fig(3, 4, "Right-angled triangle with legs 3 and 4, hypotenuse marked question mark") + "Find the magnitude of \\(\\binom{-3}{4}\\)."
bz[5]["hint"] = "Square each number, so the minus disappears, then add and root."
bz[5]["misconceptions"] = [{
    "pattern": "subtracted", "expect": 1,
    "message": "You subtracted the numbers. Magnitude squares them: √((−3)² + 4²) = √25 = 5."
}]
bz[5]["guided_steps"] = [
    say("Magnitude squares each number, so the minus disappears."),
    box("(−3)² = ", 9, "A negative squared is positive."),
    box("4² = ", 16, "4 times 4."),
    box("Add: 9 + 16 = ", 25, "Sum the squares.", phase=True),
    box("√25 = ", 5, "What squares to 25?", done="|v| = 5."),
]
# b6 AB from BA
bz[6]["hint"] = "Reverse means flip both signs."
bz[6]["misconceptions"] = [{
    "pattern": "no_change", "expect": 1,
    "message": "AB is the reverse of BA, so flip both signs: (−3, 2). It is not the same as BA."
}]
bz[6]["guided_steps"] = [
    say("AB is the reverse of BA, so flip both signs."),
    box("Top: −(3) = ", -3, "Flip the sign of 3."),
    box("Bottom: −(−2) = ", 2, "Minus a minus is plus.", phase=True),
    box("Add the tops of AB and BA to check: −3 + 3 = ", 0, "Reverses should cancel.",
        done="AB + BA = (0, 0), so AB = (−3, 2)."),
]
# b7 3(2,-1)
bz[7]["hint"] = "Multiply both numbers by 3, keeping signs."
bz[7]["misconceptions"] = [{
    "pattern": "dropped_sign", "expect": 2,
    "message": "Keep the minus sign: 3 × (−1) = −3, so the answer is (6, −3)."
}]
bz[7]["guided_steps"] = [
    say("To scale, multiply both numbers by 3."),
    box("Top: 3 × 2 = ", 6, "Three lots of 2."),
    box("Bottom: 3 × (−1) = ", -3, "Keep the minus sign.", phase=True),
    box("Divide the top back to check: 6 ÷ 3 = ", 2, "Should return the original top, 2.",
        done="Back to (2, −1), so the answer is (6, −3)."),
]
pb["bronze_description"] = "Add, subtract or scale column vectors, or find a magnitude, in a single step."

# ============ SILVER ============
sv = pb["silver"]
# s0 OP midpoint AB
sv[0]["display"] = tri("Triangle O A B with P the midpoint of A B", "a", "b", [(MID_AB, "P")], target=(O, MID_AB, "?")) + "OA = a, OB = b. P is the midpoint of AB. Find OP in terms of a and b."
sv[0]["hint"] = "The midpoint of AB has OP = ½(a + b)."
sv[0]["misconceptions"] = [{
    "pattern": "kept_a_whole", "expect": 1,
    "message": "You halved b but kept a whole. Both halve: OP = ½(a + b) = ½a + ½b."
}]
sv[0]["guided_steps"] = [
    say("For the midpoint of AB, \\(\\overrightarrow{OP} = \\tfrac12(\\mathbf{a} + \\mathbf{b})\\): halve each."),
    box("Coefficient of a: ½ × 1 = ", 0.5, "Half of one a."),
    box("Coefficient of b: ½ × 1 = ", 0.5, "Half of one b.", phase=True),
    box("Double the a coefficient back to check: 0.5 × 2 = ", 1, "Should return one whole a.",
        done="OP = ½a + ½b."),
]
# s1 OM
sv[1]["display"] = tri("Triangle O A B with M the midpoint of A B, sides 2a and 2b", "2a", "2b", [(MID_AB, "M")], target=(O, MID_AB, "?")) + "OA = 2a, OB = 2b. M is the midpoint of AB. Find OM."
sv[1]["hint"] = "OM = ½(OA + OB) = ½(2a + 2b)."
sv[1]["misconceptions"] = [{
    "pattern": "forgot_halve", "expect": 3,
    "message": "You added without halving. The midpoint is half the sum: ½(2a + 2b) = a + b."
}]
sv[1]["guided_steps"] = [
    say("Midpoint \\(\\overrightarrow{OM} = \\tfrac12(\\overrightarrow{OA} + \\overrightarrow{OB}) = \\tfrac12(2\\mathbf{a} + 2\\mathbf{b})\\)."),
    box("Coefficient of a: ½ × 2 = ", 1, "Half of 2a."),
    box("Coefficient of b: ½ × 2 = ", 1, "Half of 2b.", phase=True),
    box("Undo the half on a to check: 1 × 2 = ", 2, "Should return 2a.",
        done="OM = a + b."),
]
# s2 AC
sv[2]["hint"] = "Multiply the whole vector AB by ⅓."
sv[2]["misconceptions"] = [
    {"pattern": "halved", "expect": 1,
     "message": "One third, not one half. AC = ⅓ of (6, −2) = (2, −⅔)."},
    {"pattern": "used_two_thirds", "expect": 2,
     "message": "That is ⅔ of AB. C is one third along, so AC = (2, −⅔)."},
]
sv[2]["guided_steps"] = [
    say("C is one third of the way from A to B, so AC = ⅓ of AB."),
    box("Top: 6 ÷ 3 = ", 2, "A third of 6."),
    box("If you halved by mistake the top would be 3. The correct top is: ", 2, "6 ÷ 3, not 6 ÷ 2."),
    box("Bottom: (−2) ÷ 3 stays as −⅔. Multiply it back by 3 to check: (−2/3) × 3 = ", -2,
        "Should return the original bottom.", phase=True),
    box("Top back: 2 × 3 = ", 6, "Should return the original top.", done="AC = (2, −⅔)."),
]
# s3 k=9
sv[3]["hint"] = "Find the multiplier from the a terms, then apply it to b."
sv[3]["misconceptions"] = [{
    "pattern": "gave_scale_factor", "expect": 3,
    "message": "3 is the multiplier, not k. Apply it to the b term: k = 3 × 3 = 9."
}]
sv[3]["guided_steps"] = [
    say("Parallel vectors are scalar multiples. Find the multiplier from the a terms."),
    box("Multiplier: 6 ÷ 2 = ", 3, "6 over 2."),
    box("Apply it to the b term: k = 3 × 3 = ", 9, "Multiplier times 3.", phase=True),
    box("Check the a term: 3 × 2 = ", 6, "Should give the 6a term.",
        done="6a + 9b = 3(2a + 3b), so k = 9."),
]
# s4 |(-8,6)|
sv[4]["display"] = mag_fig(8, 6, "Right-angled triangle with legs 8 and 6, hypotenuse marked question mark") + "Find the magnitude of \\(\\binom{-8}{6}\\)."
sv[4]["hint"] = "Square each number, add, then square root."
sv[4]["misconceptions"] = [{
    "pattern": "added_sizes", "expect": 14,
    "message": "You added the sizes. Square first: √((−8)² + 6²) = √100 = 10."
}]
sv[4]["guided_steps"] = [
    say("Square each number, add them, then take the square root."),
    box("(−8)² = ", 64, "A negative squared is positive."),
    box("6² = ", 36, "6 times 6."),
    box("Add: 64 + 36 = ", 100, "Sum the squares.", phase=True),
    box("√100 = ", 10, "What squares to 100?", done="|v| = 10."),
]
# s5 OP 1:3
sv[5]["display"] = tri("Triangle O A B with P dividing A B in ratio 1 to 3 from A", "a", "b", [(P_s5, "P")], target=(O, P_s5, "?")) + "OA = a, OB = b. Point P divides AB in ratio 1:3 from A. Find OP in terms of a and b."
sv[5]["hint"] = "Ratio 1:3 from A puts P a quarter of the way along AB."
sv[5]["misconceptions"] = [{
    "pattern": "swapped_ratio", "expect": 1,
    "message": "P is only ¼ of the way from A, so more of a remains: OP = ¾a + ¼b, not ¼a + ¾b."
}]
sv[5]["guided_steps"] = [
    say("Ratio 1:3 from A means P is one quarter of the way along AB."),
    box("Fraction along AB: 1 ÷ (1 + 3) = ", 0.25, "1 over 4."),
    box("AB = b − a, so the coefficient of a in AB = ", -1, "b − a means −1 lot of a."),
    box("OP = a + ¼(b − a). Coefficient of a: 1 − 0.25 = ", 0.75, "One minus a quarter.", phase=True),
    box("Coefficient of b: 0 + 0.25 = ", 0.25, "A quarter of b.", done="OP = ¾a + ¼b."),
]
# s6 |AB| from coords
sv[6]["display"] = mag_fig(12, 5, "Right-angled displacement triangle with legs 12 across and 5 up, distance marked question mark") + "A = (3, 2), B = (15, 7). Find |AB|."
sv[6]["solutions"] = [13]
sv[6]["hint"] = "Find the across and up steps, then use Pythagoras."
sv[6]["misconceptions"] = [{
    "pattern": "added_steps", "expect": 17,
    "message": "You added the steps across and up. Use Pythagoras: √(12² + 5²) = √169 = 13."
}]
sv[6]["guided_steps"] = [
    say("Find the across and up steps from A to B, then use Pythagoras."),
    box("Across: 15 − 3 = ", 12, "Difference in x."),
    box("Up: 7 − 2 = ", 5, "Difference in y."),
    box("Square and add: 12² + 5² = ", 169, "144 + 25.", phase=True),
    box("√169 = ", 13, "What squares to 169?", done="|AB| = 13."),
]
pb["silver_description"] = "Two or three steps: route-find with a and b, use a midpoint or ratio, or a magnitude from coordinates."

# ============ GOLD ============
gd = pb["gold"]
# g0 BX
gd[0]["display"] = tri("Triangle O A B with point X, showing B X", "a", "b", [(X_g0, "X")], target=(B, X_g0, "?")) + "OA = a, OB = b. X is such that OX = 2a − b. Express BX in terms of a and b."
gd[0]["hint"] = "Travel B to O, then O to X."
gd[0]["misconceptions"] = [{
    "pattern": "found_XB", "expect": 3,
    "message": "That is XB, the reverse. BX goes from B: BX = −b + (2a − b) = 2a − 2b."
}]
gd[0]["guided_steps"] = [
    say("Travel B to O, then O to X: \\(\\overrightarrow{BX} = \\overrightarrow{BO} + \\overrightarrow{OX}\\)."),
    box("OB = b, so BO reverses it. Coefficient of b in BO = ", -1, "Reversing flips the sign."),
    box("OX = 2a − b, so its coefficient of a = ", 2, "Read off 2a."),
    box("Collect the a terms (0 from BO, 2 from OX): ", 2, "Only OX has an a.", phase=True),
    box("Collect the b terms: −1 + (−1) = ", -2, "BO gives −1, OX gives −1.",
        done="BX = 2a − 2b."),
]
# g1 ratio (REWRITTEN display)
gd[1]["display"] = tri("Points B, A and X roughly in a line with B X shown", "a", "b", [(X_g0, "X")], target=(B, X_g0, "?")) + "OA = a and OB = b. A point X satisfies BX = 2a − 2b. Find the ratio |BX| : |BA|."
gd[1]["hint"] = "Write BA in terms of a and b, then compare it with BX."
gd[1]["misconceptions"] = [{
    "pattern": "inverted_ratio", "expect": 1,
    "message": "BX is the longer one: BX = 2 × BA, so the ratio is 2 : 1, not 1 : 2."
}]
gd[1]["guided_steps"] = [
    say("Write BA in terms of a and b, then compare it with BX."),
    box("BA = OA − OB = a − b, so the coefficient of a in BA = ", 1, "a − b."),
    box("BX = 2a − 2b, so the coefficient of a in BX = ", 2, "Read off 2a."),
    box("How many BA fit into BX: 2 ÷ 1 = ", 2, "Compare the a coefficients.", phase=True),
    box("So |BX| : |BA| = 2 : 1. Type the first number of the ratio: ", 2, "The 2 in 2 to 1.",
        done="BX = 2 × BA, so the ratio is 2 : 1."),
]
# g2 PQ
gd[2]["display"] = tri("Triangle O A B with P two thirds along O A and Q one third along O B, sides 3a and 3b", "3a", "3b", [(P_g2, "P"), (Q_g2, "Q")], target=(P_g2, Q_g2, "?")) + "OA = 3a, OB = 3b. P is ⅔ along OA. Q is ⅓ along OB. Find PQ."
gd[2]["hint"] = "Find OP and OQ, then PQ = PO + OQ."
gd[2]["misconceptions"] = [{
    "pattern": "found_QP", "expect": 1,
    "message": "That is QP, the reverse. PQ starts at P: PQ = −2a + b."
}]
gd[2]["guided_steps"] = [
    say("Find OP and OQ, then \\(\\overrightarrow{PQ} = \\overrightarrow{PO} + \\overrightarrow{OQ}\\)."),
    box("OP = ⅔ of 3a. Coefficient of a: (2 ÷ 3) × 3 = ", 2, "Two thirds of 3."),
    box("OQ = ⅓ of 3b. Coefficient of b: (1 ÷ 3) × 3 = ", 1, "A third of 3."),
    box("PO reverses OP, so the coefficient of a in PQ = ", -2, "Reverse of 2a.", phase=True),
    box("Coefficient of b in PQ, from OQ = ", 1, "OQ contributes b.", done="PQ = −2a + b."),
]
# g3 k=3
gd[3]["hint"] = "Both the p terms and the q terms must give the same multiplier."
gd[3]["misconceptions"] = [{
    "pattern": "read_q_coeff", "expect": 6,
    "message": "Check both terms give the same multiplier: 3p = 3 × p and 6q = 3 × 2q, so k = 3, not 6."
}]
gd[3]["guided_steps"] = [
    say("Parallel means one is a scalar multiple. Check both terms give the same multiplier."),
    box("From the p terms: 3 ÷ 1 = ", 3, "Coefficient of p in each."),
    box("From the q terms: 6 ÷ 2 = ", 3, "Coefficient of q in each.", phase=True),
    box("Both agree, so k = ", 3, "They give the same value.",
        done="AB = 3 × CD, parallel with k = 3."),
]
# g4 MN
gd[4]["display"] = tri("Triangle O A B with M the midpoint of O A and N the midpoint of O B", "a", "b", [(M_g4, "M"), (N_g4, "N")], target=(M_g4, N_g4, "?")) + "OA = a, OB = b. M is midpoint of OA, N is midpoint of OB. Find MN in terms of a and b."
gd[4]["hint"] = "Use MN = MO + ON, halving OA and OB."
gd[4]["misconceptions"] = [{
    "pattern": "found_NM", "expect": 3,
    "message": "That is NM, the reverse. MN starts at M: MN = −½a + ½b = ½b − ½a."
}]
gd[4]["guided_steps"] = [
    say("M is the midpoint of OA, N of OB. Use \\(\\overrightarrow{MN} = \\overrightarrow{MO} + \\overrightarrow{ON}\\)."),
    box("OM = ½a, so MO reverses it. Coefficient of a in MO = ", -0.5, "Reverse of half an a."),
    box("ON = ½b, so the coefficient of b = ", 0.5, "Half of b."),
    box("Coefficient of a in MN, from MO = ", -0.5, "Only MO has an a.", phase=True),
    box("Coefficient of b in MN, from ON = ", 0.5, "Only ON has a b.",
        done="MN = ½b − ½a, parallel to AB and half its length."),
]
pb["gold_description"] = "Chain several vectors, prove lines parallel, or find a ratio using a route through known vectors."

# ---------- tier_guides ----------
live["tier_guides"] = {
    "bronze": {
        "title": "Bronze: column vectors in one step",
        "steps": [
            "<strong>Add or subtract</strong> row by row: \\(\\binom{3}{2} + \\binom{1}{5} = \\binom{4}{7}\\).",
            "<strong>Scale</strong> by multiplying both numbers: \\(2\\binom{5}{-1} = \\binom{10}{-2}\\). A negative reverses direction.",
            "<strong>Magnitude:</strong> \\(\\left|\\binom{x}{y}\\right| = \\sqrt{x^2 + y^2}\\). Square each, add, then square root.",
        ],
        "example": {
            "question": "Find \\(\\binom{6}{-2} + \\binom{1}{5}\\).",
            "steps": [
                {"label": "Top", "content": "6 + 1 = 7"},
                {"label": "Bottom", "content": "−2 + 5 = 3"},
                {"label": "Check", "content": "Signs kept ✓"},
                {"label": "Answer", "content": "\\(\\binom{7}{3}\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: routes and midpoints",
        "steps": [
            "<strong>Route:</strong> to travel A to B, step through O. \\(\\overrightarrow{AB} = \\overrightarrow{AO} + \\overrightarrow{OB} = -\\mathbf{a} + \\mathbf{b}\\). Reversing flips the sign.",
            "<strong>Midpoint of AB:</strong> \\(\\overrightarrow{OM} = \\tfrac12(\\mathbf{a} + \\mathbf{b})\\). A point dividing AB in ratio \\(m:n\\) from A sits \\(\\tfrac{m}{m+n}\\) of the way along.",
            "<strong>Magnitude from points:</strong> find the across and up steps, then \\(\\sqrt{x^2 + y^2}\\).",
        ],
        "example": {
            "question": "OA = a, OB = b. M is the midpoint of AB. Find OM.",
            "steps": [
                {"label": "Formula", "content": "\\(\\overrightarrow{OM} = \\tfrac12(\\mathbf{a} + \\mathbf{b})\\)"},
                {"label": "Halve each", "content": "half an a, half a b"},
                {"label": "Check", "content": "halfway ✓"},
                {"label": "Answer", "content": "\\(\\tfrac12\\mathbf{a} + \\tfrac12\\mathbf{b}\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chains, ratios and parallel proofs",
        "steps": [
            "<strong>Chain a route</strong> leg by leg, keeping every sign, then collect the \\(\\mathbf{a}\\) terms and the \\(\\mathbf{b}\\) terms.",
            "<strong>Parallel:</strong> if \\(\\overrightarrow{PQ} = k\\,\\overrightarrow{RS}\\) for one number \\(k\\), the lines are parallel. The same \\(k\\) must fit both parts.",
            "<strong>Ratio:</strong> that \\(k\\) is the length ratio. \\(\\overrightarrow{BX} = 2\\overrightarrow{BA}\\) gives \\(|BX| : |BA| = 2 : 1\\).",
        ],
        "example": {
            "question": "AB = 3p + 6q, CD = p + 2q. Find k with AB = kCD.",
            "steps": [
                {"label": "p terms", "content": "3 ÷ 1 = 3"},
                {"label": "q terms", "content": "6 ÷ 2 = 3"},
                {"label": "Check", "content": "both give 3 ✓"},
                {"label": "Answer", "content": "k = 3", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided (opener + teach) ----------
live["guided"] = {
    "opener": {
        "display": opener_grid() + "A delivery robot starts at the depot (S). First it drives 3 blocks east and 2 blocks north. Then it drives 1 block east and 5 blocks north. How far east and north is it from the depot in total?",
        "steps": [
            box("Total blocks east: 3 + 1 = ", 4, "Add the two east moves."),
            box("Total blocks north: 2 + 5 = ", 7, "Add the two north moves."),
            say("You just added two vectors. Writing each move as a column, \\(\\binom{3}{2} + \\binom{1}{5} = \\binom{4}{7}\\). Adding vectors means add the eastings, then add the northings. Every question today builds on that one move."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "\\(\\mathbf{c} = \\binom{2}{5}\\), \\(\\mathbf{d} = \\binom{4}{1}\\). Find \\(\\mathbf{c} - \\mathbf{d}\\).",
            "steps": [
                say("To subtract, subtract the top numbers, then the bottom numbers."),
                box("Top: 2 − 4 = ", -2, "2 take away 4 goes negative."),
                box("Bottom: 5 − 1 = ", 4, "5 take away 1."),
                box("Add d's top back to check: −2 + 4 = ", 2, "Should return c's top, 2."),
                box("Add d's bottom back to check: 4 + 1 = ", 5, "Should return c's bottom, 5.",
                    done="Back to c = (2, 5). Subtracting row by row is the whole move."),
            ],
        },
        "silver": {
            "display": teach_silver_fig() + "OA = a, OB = b. M is the midpoint of OB. Find AM in terms of a and b.",
            "steps": [
                say("Travel A to O, then O to M: \\(\\overrightarrow{AM} = \\overrightarrow{AO} + \\overrightarrow{OM}\\)."),
                box("AO reverses OA = a, so the coefficient of a = ", -1, "Reversing flips the sign."),
                box("M is the midpoint of OB, so OM = ½b. Coefficient of b = ", 0.5, "Half of b."),
                box("Coefficient of a in AM = ", -1, "Only AO has an a."),
                box("Coefficient of b in AM = ", 0.5, "Only OM has a b.",
                    done="AM = −a + ½b. Building a route through O is the whole point."),
            ],
        },
        "gold": {
            "display": "Vectors OP = 4a + 6b and OQ = 2a + 3b. Show OP is parallel to OQ and state the ratio OP : OQ.",
            "steps": [
                say("Parallel means one is a scalar multiple. Compare the coefficients to find it."),
                box("a terms: 4 ÷ 2 = ", 2, "Coefficient of a in each."),
                box("b terms: 6 ÷ 3 = ", 2, "Coefficient of b in each."),
                box("Both agree, so OP = k × OQ with k = ", 2, "They give the same value."),
                box("So the ratio OP : OQ = 2 : ? Type the second number: ", 1, "k to 1.",
                    done="OP is twice OQ, ratio 2 : 1. Equal multipliers prove the lines are parallel."),
            ],
        },
    },
}

# ---------- method_card (slim) ----------
live["method_card"] = {
    "title": "Vectors",
    "steps": [
        "Add or subtract vectors row by row; scale by multiplying both parts.",
        "Reverse a vector by flipping its sign: \\(\\overrightarrow{BA} = -\\overrightarrow{AB}\\).",
        "Route-find through known points: \\(\\overrightarrow{AB} = \\overrightarrow{AO} + \\overrightarrow{OB}\\).",
        "Magnitude \\(= \\sqrt{x^2 + y^2}\\); parallel vectors are scalar multiples.",
    ],
    "content": "<p>A <strong>vector</strong> has size and direction, written \\(\\mathbf{a}\\) or \\(\\binom{x}{y}\\). Add or subtract by rows; multiply both parts to scale. The negative reverses direction.</p><p>To travel between points, build a route from known vectors: \\(\\overrightarrow{AB} = \\overrightarrow{AO} + \\overrightarrow{OB} = \\mathbf{b} - \\mathbf{a}\\). The midpoint M of AB has \\(\\overrightarrow{OM} = \\tfrac12(\\mathbf{a} + \\mathbf{b})\\).</p><p>The magnitude is \\(\\sqrt{x^2 + y^2}\\). If \\(\\overrightarrow{PQ} = k\\,\\overrightarrow{RS}\\), the lines are parallel and \\(k\\) is their length ratio.</p>",
}

json.dump(live, io.open("lesson_maths-aqa_geometry-L08.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("WROTE lesson_maths-aqa_geometry-L08.json")
