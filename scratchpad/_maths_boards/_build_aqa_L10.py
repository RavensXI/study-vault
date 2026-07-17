# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams build for maths-aqa algebra-L10.
Every box answer is COMPUTED and asserted, not typed, so arithmetic cannot drift."""
import json, math

M = "−"   # minus sign
SUP2 = "²"  # superscript two

live = json.load(open("_aqa_L10_live.json", encoding="utf-8"))

def rstr(r):
    """plain-text root with parentheses for negatives."""
    return "(" + M + str(abs(r)) + ")" if r < 0 else str(r)

def curve_expr(r, qx, qc):
    """plain text of x^2 + qx*x + qc evaluated-form at integer r, e.g. '(-3)^2 + 2*(-3)'."""
    s = rstr(r) + SUP2
    if qx:
        s += " " + ("+" if qx > 0 else M) + " " + (str(abs(qx)) + "×" if abs(qx) != 1 else "") + rstr(r)
    if qc:
        s += " " + ("+" if qc > 0 else M) + " " + str(abs(qc))
    return s

# ---- Family 1: y = lx*x + lc  and  y = x^2 + qx*x + qc (both y=) ----
def family1(lx, lc, qx, qc, line_latex, quad_latex, factor_say, roots, hint, misc):
    B, C = qx - lx, qc - lc
    r1, r2 = roots            # r1 presented first
    assert r1*r1 + B*r1 + C == 0 and r2*r2 + B*r2 + C == 0, (roots, B, C)
    def line(x): return lx*x + lc
    def curve(x): return x*x + qx*x + qc
    for r in roots:
        assert line(r) == curve(r), ("not on both", r)
    y1, y2 = line(r1), line(r2)
    chk = curve(r1)
    assert chk == y1
    line_rhs = line_latex.split("=", 1)[1].strip()
    quad_rhs = quad_latex.split("=", 1)[1].strip()
    steps = [
        {"say": "Both equations give y, so set the two right sides equal: \\(" + line_rhs +
                " = " + quad_rhs + "\\). Bring every term to the right so \\(x^2\\) stays positive."},
        {"pre": "The x-term becomes ", "post": "x", "answer": B,
         "hint": "Take the line's x-term across the equals sign, changing its sign, then combine."},
        {"pre": "and the constant becomes ", "post": "", "answer": C,
         "hint": "Take the line's constant across the equals sign, changing its sign."},
        {"pre": "First root, x = ", "post": "", "phase": "substitute", "answer": r1,
         "say": factor_say, "hint": "Set the first bracket to zero."},
        {"pre": "Second root, x = ", "post": "", "answer": r2,
         "hint": "Set the other bracket to zero."},
        {"pre": "At x = " + (M+str(abs(r1)) if r1 < 0 else str(r1)) + ": y = ", "post": "", "answer": y1,
         "say": "Now each x gets its y from the line \\(" + line_latex + "\\).",
         "hint": "Put the first x into the line."},
        {"pre": "At x = " + (M+str(abs(r2)) if r2 < 0 else str(r2)) + ": y = ", "post": "", "answer": y2,
         "hint": "Put the second x into the line."},
        {"pre": "Check in the curve: " + curve_expr(r1, qx, qc) + " = ", "post": "", "answer": chk,
         "say": "Last check: put the first pair into the curve.",
         "done": "It equals y = " + str(y1) + ", so (" + (M+str(abs(r1)) if r1<0 else str(r1)) + ", " +
                 str(y1) + ") is right and the other pair checks the same way.",
         "hint": "Substitute the first x into the curve; it should give the same y."},
    ]
    return {"hint": hint, "display": None, "solutions": sorted([r1, r2]),
            "calculator": False, "input_type": "two_solutions",
            "guided_steps": steps, "misconceptions": misc}

# ---- Family 2: horizontal line y = k and y = x^2 + qc (x^2 = value) ----
def family2(k, qc, line_latex, quad_latex, hint, misc):
    val = k - qc            # x^2 = val
    r = int(math.isqrt(val)); assert r*r == val
    steps = [
        {"say": "One equation is just \\(" + line_latex + "\\), so the curve must equal " + str(k) +
                ": \\(" + quad_latex + " = " + str(k) + "\\)."},
        {"pre": "Rearrange to x" + SUP2 + " = ", "post": "", "answer": val,
         "hint": "Move the number across to leave x" + SUP2 + " on its own."},
        {"pre": "First root (positive), x = ", "post": "", "phase": "substitute", "answer": r,
         "say": "\\(x^2 = " + str(val) + "\\), so x is a square root of " + str(val) +
                ", and there are TWO: \\(+" + str(r) + "\\) and \\(" + M + str(r) + "\\).",
         "hint": "The positive square root of " + str(val) + "."},
        {"pre": "Second root (negative), x = ", "post": "", "answer": -r,
         "hint": "The negative square root of " + str(val) + "."},
        {"pre": "Check the curve at x = " + str(r) + ": " + curve_expr(r, 0, qc) + " = ", "post": "", "answer": k,
         "done": "It equals " + str(k) + ", matching the line, so x = " + str(r) + " and x = " + M + str(r) + " are both right.",
         "hint": "Substitute x = " + str(r) + " into the curve; it should give " + str(k) + "."},
    ]
    return {"hint": hint, "display": None, "solutions": sorted([r, -r]),
            "calculator": False, "input_type": "two_solutions",
            "guided_steps": steps, "misconceptions": misc}

# ---- Family 3: line y = x + lc  and circle x^2 + y^2 = r2 ----
def poly2_latex(b, c):
    s = "x^2"
    if b:
        s += (" + " if b > 0 else " - ") + (str(abs(b)) if abs(b) != 1 else "") + "x"
    if c:
        s += (" + " if c > 0 else " - ") + str(abs(c))
    return s

def factor_latex(r1, r2):
    def f(r):
        if r == 0: return "x"
        return "(x - " + str(r) + ")" if r > 0 else "(x + " + str(abs(r)) + ")"
    return f(r1) + f(r2)

def family3(lc, r2, line_latex, roots, hint, misc):
    # y = x + lc ; x^2 + (x+lc)^2 = r2 -> 2x^2 + 2lc x + (lc^2 - r2) = 0
    r1, r2root = roots
    def line(x): return x + lc
    for r in roots:
        assert abs(r*r + line(r)**2 - r2) < 1e-9, ("not on circle", r)
    y1, y2 = line(r1), line(r2root)
    mid = 2*lc              # middle term coeff in (x+lc)^2 = x^2 + 2lc x + lc^2
    two_x2 = 2
    const = lc*lc - r2      # after taking r2 across: 2x^2 + 2lc x + (lc^2 - r2) = 0
    half_b = lc             # divide by 2 -> x^2 + lc x + (lc^2 - r2)/2
    hc = lc*lc - r2
    assert hc % 2 == 0
    half_c = hc // 2
    assert r1*r1 + half_b*r1 + half_c == 0 and r2root*r2root + half_b*r2root + half_c == 0
    lc_signed = str(lc) if lc > 0 else "(" + M + str(abs(lc)) + ")"
    bracket = "(x " + ("+" if lc > 0 else M) + " " + str(abs(lc)) + ")"
    twoquad = "2x^2" + (" + " + str(mid) if mid >= 0 else " - " + str(abs(mid))) + "x" + \
              (" + " + str(const) if const >= 0 else " - " + str(abs(const))) + " = 0"
    steps = [
        {"pre": "The middle term of " + bracket + SUP2 + ", 2 × " + lc_signed + ", is ",
         "post": "x", "answer": mid,
         "say": "Substitute \\(" + line_latex + "\\) into the circle: \\(x^2 + " + bracket +
                "^2 = " + str(r2) + "\\). Expand the bracket in full.",
         "hint": "2 times " + str(abs(lc)) + (", and it is negative." if lc < 0 else ".")},
        {"pre": "Collect the two x" + SUP2 + " terms, 1 + 1 = ", "post": "x" + SUP2, "answer": two_x2,
         "say": "So \\(x^2 + x^2 " + ("+ " + str(mid) if mid >= 0 else M + " " + str(abs(mid))) +
                "x + " + str(lc*lc) + " = " + str(r2) + "\\).",
         "hint": "One x" + SUP2 + " from each part."},
        {"pre": "The constant, " + str(lc*lc) + " " + M + " " + str(r2) + ", becomes ", "post": "", "answer": const,
         "say": "That gives \\(2x^2 " + ("+ " + str(mid) if mid >= 0 else M + " " + str(abs(mid))) +
                "x + " + str(lc*lc) + " = " + str(r2) + "\\). Take " + str(r2) + " across.",
         "hint": str(lc*lc) + " minus " + str(r2) + "."},
        {"pre": "First root, x = ", "post": "", "phase": "substitute", "answer": r1,
         "say": "So \\(" + twoquad + "\\). Divide every term by 2 to get \\(" + poly2_latex(half_b, half_c) +
                " = 0\\), which factorises as \\(" + factor_latex(r1, r2root) + " = 0\\).",
         "hint": "Set the first bracket to zero."},
        {"pre": "Second root, x = ", "post": "", "answer": r2root,
         "hint": "Set the other bracket to zero."},
        {"pre": "At x = " + (M+str(abs(r1)) if r1 < 0 else str(r1)) + ": y = ", "post": "", "answer": y1,
         "say": "Each x gets its y from \\(" + line_latex + "\\).",
         "hint": "Put the first x into the line."},
        {"pre": "At x = " + (M+str(abs(r2root)) if r2root < 0 else str(r2root)) + ": y = ", "post": "", "answer": y2,
         "hint": "Put the second x into the line."},
        {"pre": "Check (" + (M+str(abs(r1)) if r1<0 else str(r1)) + ", " + (M+str(abs(y1)) if y1<0 else str(y1)) +
                ") in the circle: " + rstr(r1) + SUP2 + " + " + rstr(y1) + SUP2 + " = ", "post": "", "answer": r2,
         "done": "It equals " + str(r2) + ", so that pair is right and the other checks the same way.",
         "hint": str(r1*r1) + " + " + str(y1*y1) + "."},
    ]
    return {"hint": hint, "display": None, "solutions": sorted([r1, r2root]),
            "calculator": False, "input_type": "two_solutions",
            "guided_steps": steps, "misconceptions": misc}

# ============ MISCONCEPTIONS ============
def sign_flip(quad_latex, correct_pair, flipped_pair, corr_factor, flip_factor):
    c1, c2 = correct_pair
    f1, f2 = flipped_pair
    return {"note": "sign-flipped factorisation of " + quad_latex,
            "expect": sorted(flipped_pair),
            "message": "Check the signs inside your brackets. \\(" + quad_latex + "\\) factorises as \\(" +
                       corr_factor + " = 0\\), giving \\(x = " + str(c1) + "\\) and \\(x = " + str(c2) +
                       "\\). Reversing those signs gives \\(x = " + str(f1) + "\\) and \\(x = " + str(f2) +
                       "\\), which do not fit the equations.",
            "pattern": "factor_sign_flip"}

def sqrt_pm(val):
    return {"expect": None,
            "message": "\\(x^2 = " + str(val) + "\\) has TWO answers: the positive and the negative square root. Writing only one loses half the solution.",
            "pattern": "single_root"}

def divide_by_x(quad_latex, factor):
    return {"expect": None,
            "message": "When you reach \\(" + quad_latex + "\\), factorise as \\(" + factor +
                       " = 0\\) rather than dividing both sides by x. Dividing by x throws away the solution \\(x = 0\\).",
            "pattern": "divide_by_x"}

def square_bracket(bracket, correct, wrong):
    return {"expect": None,
            "message": "Expand \\(" + bracket + "\\) in full as \\(" + correct + "\\); do not write \\(" +
                       wrong + "\\), or the middle term is lost.",
            "pattern": "square_bracket_error"}

# ============ BUILD BANK ============
bronze = [
    # b0
    dict(family1(1,0,0,0, "y = x", "y = x^2",
        "So \\(x^2 - x = 0\\). Take out a common factor of x: \\(x(x - 1) = 0\\).",
        (0,1), "Set the two right sides equal, then take out a common factor of x.",
        [divide_by_x("x^2 - x = 0", "x(x - 1)")]),
        display="Solve \\(y = x\\) and \\(y = x^2\\). Give the two x-values."),
    # b1 (Family2)
    dict(family2(3, -1, "y = 3", "x^2 - 1",
        "Set the curve equal to 3, then square-root both sides.",
        [sqrt_pm(4)]),
        display="Solve \\(y = 3\\) and \\(y = x^2 - 1\\). Give the two x-values."),
    # b2
    dict(family1(1,2,0,0, "y = x + 2", "y = x^2",
        "So \\(x^2 - x - 2 = 0\\). Two numbers multiply to \\(-2\\) and add to \\(-1\\): they are \\(-2\\) and \\(+1\\), giving \\((x - 2)(x + 1) = 0\\).",
        (2,-1), "Set the two right sides equal, rearrange to zero, then factorise.",
        [sign_flip("x^2 - x - 2", (2,-1), (-2,1), "(x - 2)(x + 1)", "(x + 2)(x - 1)")]),
        display="Solve \\(y = x + 2\\) and \\(y = x^2\\). Give the two x-values."),
    # b3 (REPLACED, was dup of b0)
    dict(family1(4,0,0,3, "y = 4x", "y = x^2 + 3",
        "So \\(x^2 - 4x + 3 = 0\\). Two numbers multiply to 3 and add to \\(-4\\): they are \\(-1\\) and \\(-3\\), giving \\((x - 1)(x - 3) = 0\\).",
        (1,3), "Set the two right sides equal, rearrange to zero, then factorise.",
        [sign_flip("x^2 - 4x + 3", (1,3), (-1,-3), "(x - 1)(x - 3)", "(x + 1)(x + 3)")]),
        display="Solve \\(y = 4x\\) and \\(y = x^2 + 3\\). Give the two x-values."),
    # b4 (REPLACED, was dup of b1)
    dict(family1(2,0,0,-3, "y = 2x", "y = x^2 - 3",
        "So \\(x^2 - 2x - 3 = 0\\). Two numbers multiply to \\(-3\\) and add to \\(-2\\): they are \\(-3\\) and \\(+1\\), giving \\((x - 3)(x + 1) = 0\\).",
        (3,-1), "Set the two right sides equal, rearrange to zero, then factorise.",
        [sign_flip("x^2 - 2x - 3", (3,-1), (-3,1), "(x - 3)(x + 1)", "(x + 3)(x - 1)")]),
        display="Solve \\(y = 2x\\) and \\(y = x^2 - 3\\). Give the two x-values."),
    # b5
    dict(family1(1,6,2,0, "y = x + 6", "y = x^2 + 2x",
        "So \\(x^2 + x - 6 = 0\\). Two numbers multiply to \\(-6\\) and add to \\(+1\\): they are \\(+3\\) and \\(-2\\), giving \\((x + 3)(x - 2) = 0\\).",
        (-3,2), "Set the two right sides equal, rearrange to zero, then factorise.",
        [sign_flip("x^2 + x - 6", (-3,2), (3,-2), "(x + 3)(x - 2)", "(x - 3)(x + 2)")]),
        display="Solve \\(y = x + 6\\) and \\(y = x^2 + 2x\\). Give the two x-values."),
    # b6 (Family2)
    dict(family2(7, -2, "y = 7", "x^2 - 2",
        "Set the curve equal to 7, then square-root both sides.",
        [sqrt_pm(9)]),
        display="Solve \\(y = 7\\) and \\(y = x^2 - 2\\). Give the two x-values."),
]

silver = [
    # s0
    dict(family1(1,3,0,1, "y = x + 3", "y = x^2 + 1",
        "So \\(x^2 - x - 2 = 0\\). Two numbers multiply to \\(-2\\) and add to \\(-1\\): they are \\(-2\\) and \\(+1\\), giving \\((x - 2)(x + 1) = 0\\).",
        (2,-1), "Set the two right sides equal, rearrange to zero, then factorise.",
        [sign_flip("x^2 - x - 2", (2,-1), (-2,1), "(x - 2)(x + 1)", "(x + 2)(x - 1)")]),
        display="Solve \\(y = x + 3\\) and \\(y = x^2 + 1\\). Give the two x-values."),
    # s1 (circle, SVG later)
    dict(family3(1, 13, "y = x + 1", (-3,2),
        "Make y the subject, substitute into the circle, and expand the bracket in full.",
        [sign_flip("x^2 + x - 6", (-3,2), (3,-2), "(x + 3)(x - 2)", "(x - 3)(x + 2)"),
         square_bracket("(x + 1)^2", "x^2 + 2x + 1", "x^2 + 1")]),
        display="Solve \\(y = x + 1\\) and \\(x^2 + y^2 = 13\\). Give the two x-values."),
    # s2 (circle, SVG later)
    dict(family3(-2, 10, "y = x - 2", (-1,3),
        "Make y the subject, substitute into the circle, and expand the bracket in full.",
        [sign_flip("x^2 - 2x - 3", (3,-1), (-3,1), "(x - 3)(x + 1)", "(x + 3)(x - 1)"),
         square_bracket("(x - 2)^2", "x^2 - 4x + 4", "x^2 + 4")]),
        display="Solve \\(y = x - 2\\) and \\(x^2 + y^2 = 10\\). Give the two x-values."),
    # s3
    dict(family1(1,5,1,1, "y = x + 5", "y = x^2 + x + 1",
        "So \\(x^2 - 4 = 0\\). This is a difference of two squares: \\((x - 2)(x + 2) = 0\\).",
        (2,-2), "After setting the two sides equal, the x-terms cancel; solve x squared equals a number.",
        [sqrt_pm(4)]),
        display="Solve \\(y = x + 5\\) and \\(y = x^2 + x + 1\\). Give the two x-values."),
    # s4
    dict(family1(3,2,2,-4, "y = 3x + 2", "y = x^2 + 2x - 4",
        "So \\(x^2 - x - 6 = 0\\). Two numbers multiply to \\(-6\\) and add to \\(-1\\): they are \\(-3\\) and \\(+2\\), giving \\((x - 3)(x + 2) = 0\\).",
        (3,-2), "Gather x-terms and numbers from both sides, then factorise.",
        [sign_flip("x^2 - x - 6", (3,-2), (-3,2), "(x - 3)(x + 2)", "(x + 3)(x - 2)")]),
        display="Solve \\(y = 3x + 2\\) and \\(y = x^2 + 2x - 4\\). Give the two x-values."),
]

# ---- Gold ----
def gold_g3():
    # x+y=5, xy=6 -> y=5-x, x(5-x)=6 -> x^2-5x+6=0 -> (x-2)(x-3)
    r1, r2 = 2, 3
    steps = [
        {"say": "Make y the subject of the simple equation: \\(x + y = 5\\) becomes \\(y = 5 - x\\). Put this into \\(xy = 6\\): \\(x(5 - x) = 6\\)."},
        {"pre": "Multiply out x(5 − x): the x-term is 5x and the x" + SUP2 + " term is ", "post": "x" + SUP2, "answer": -1,
         "say": "So \\(5x - x^2 = 6\\).", "hint": "x times −x is −x" + SUP2 + "."},
        {"pre": "Bring all to the left so x" + SUP2 + " is positive; the constant becomes ", "post": "", "answer": -6,
         "say": "Move everything to the left: \\(x^2 - 5x + 6 = 0\\).", "hint": "0 minus 6."},
        {"pre": "First root, x = ", "post": "", "phase": "substitute", "answer": r1,
         "say": "\\(x^2 - 5x + 6 = 0\\) factorises as \\((x - 2)(x - 3) = 0\\).",
         "hint": "Set x − 2 = 0."},
        {"pre": "Second root, x = ", "post": "", "answer": r2, "hint": "Set x − 3 = 0."},
        {"pre": "At x = 2: y = 5 − 2 = ", "post": "", "answer": 3,
         "say": "Each x gets its y from \\(y = 5 - x\\).", "hint": "5 minus 2."},
        {"pre": "At x = 3: y = 5 − 3 = ", "post": "", "answer": 2, "hint": "5 minus 3."},
        {"pre": "Check the product xy for (2, 3): 2 × 3 = ", "post": "", "answer": 6,
         "done": "It equals 6, so (2, 3) is right and (3, 2) checks the same way.", "hint": "2 times 3."},
    ]
    return {"hint": "Make one letter the subject of x + y = 5, substitute into xy = 6, then solve the quadratic.",
            "display": "Solve \\(x + y = 5\\) and \\(xy = 6\\). Give the two x-values.",
            "solutions": [2, 3], "calculator": False, "input_type": "two_solutions",
            "guided_steps": steps,
            "misconceptions": [sign_flip("x^2 - 5x + 6", (2,3), (-2,-3), "(x - 2)(x - 3)", "(x + 2)(x + 3)")]}

def gold_g4():
    # y=kx+2 tangent to y=x^2+3 -> x^2 - kx + 1 = 0, disc = k^2 - 4 = 0 -> k=2
    steps = [
        {"say": "Where the line meets the curve, \\(kx + 2 = x^2 + 3\\). Bring all to one side: \\(x^2 - kx + 1 = 0\\)."},
        {"pre": "For this quadratic, a = 1, c = 1, and b = −k, so b" + SUP2 + " = k" + SUP2 + " and 4ac = ", "post": "", "answer": 4,
         "say": "Tangent means the line touches once, so the discriminant \\(b^2 - 4ac\\) is zero.",
         "hint": "4 times a times c, with a = 1 and c = 1."},
        {"pre": "Set k" + SUP2 + " − 4 = 0, so k" + SUP2 + " = ", "post": "", "phase": "substitute", "answer": 4,
         "say": "So \\(k^2 - 4 = 0\\).", "hint": "Add 4 to both sides."},
        {"pre": "The positive value of k is ", "post": "", "answer": 2,
         "hint": "The positive square root of 4."},
        {"pre": "Check: with k = 2 the quadratic is x" + SUP2 + " − 2x + 1; its discriminant 2" + SUP2 + " − 4 = ", "post": "", "answer": 0,
         "done": "The discriminant is 0, so the line just touches the curve: k = 2 is correct.",
         "hint": "4 minus 4."},
    ]
    return {"hint": "Set line equal to curve, form x^2 − kx + 1 = 0, then set the discriminant b^2 − 4ac to zero.",
            "display": "The line \\(y = kx + 2\\) is a tangent to \\(y = x^2 + 3\\), so it touches the curve at exactly one point. Find the positive value of k.",
            "solutions": [2], "calculator": False, "input_type": "single_value",
            "guided_steps": steps,
            "misconceptions": [{"expect": None,
                "message": "The discriminant uses \\(b = -k\\), so \\(b^2 = k^2\\), giving \\(k^2 - 4 = 0\\) and \\(k = 2\\) for the positive value. Do not drop the square on k.",
                "pattern": "disc_error"}]}

gold = [
    # g0
    dict(family1(-1,2,0,-4, "y = 2 - x", "y = x^2 - 4",
        "So \\(x^2 + x - 6 = 0\\). Two numbers multiply to \\(-6\\) and add to \\(+1\\): they are \\(+3\\) and \\(-2\\), giving \\((x + 3)(x - 2) = 0\\).",
        (-3,2), "Set the two right sides equal, rearrange to zero, then factorise.",
        [sign_flip("x^2 + x - 6", (-3,2), (3,-2), "(x + 3)(x - 2)", "(x - 3)(x + 2)")]),
        display="Solve \\(y = 2 - x\\) and \\(y = x^2 - 4\\). Give the two x-values."),
    # g1 (REPLACED circle, SVG later)
    dict(family3(-1, 25, "y = x - 1", (-3,4),
        "Make y the subject, substitute into the circle, and expand the bracket in full.",
        [sign_flip("x^2 - x - 12", (4,-3), (-4,3), "(x - 4)(x + 3)", "(x + 4)(x - 3)"),
         square_bracket("(x - 1)^2", "x^2 - 2x + 1", "x^2 + 1")]),
        display="Solve \\(y = x - 1\\) and \\(x^2 + y^2 = 25\\). Give the two x-values."),
    # g2
    dict(family1(2,3,5,3, "y = 2x + 3", "y = x^2 + 5x + 3",
        "So \\(x^2 + 3x = 0\\). Take out a common factor of x: \\(x(x + 3) = 0\\).",
        (0,-3), "Set the two right sides equal, rearrange to zero, then factorise out x.",
        [divide_by_x("x^2 + 3x = 0", "x(x + 3)")]),
        display="Solve \\(y = 2x + 3\\) and \\(y = x^2 + 5x + 3\\). Give the two x-values."),
    gold_g3(),
    gold_g4(),
]

# attach displays that were passed via dict()
for arr in (bronze, silver, gold):
    for p in arr:
        if p.get("display") is None:
            raise SystemExit("missing display")

pb = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Both equations are given as y = something; set them equal, rearrange to zero, factorise, and read off the two x-values.",
    "silver_description": "The linear part needs rearranging first, or the second equation is a circle x² + y² = r²; substitute with care before factorising.",
    "gold_description": "Circles, non-linear pairs such as xy = 6, and tangent conditions solved with the discriminant b² − 4ac.",
}

# ============ TIER GUIDES ============
tier_guides = {
    "bronze": {
        "title": "Bronze: substitute, factorise, two answers",
        "steps": [
            "Both equations are written as <strong>y = …</strong>, so set the two right-hand sides equal to each other.",
            "Move every term to one side to get a quadratic equal to zero, then factorise it.",
            "Each bracket gives one x-value. Put each x back into the linear equation to find its y.",
        ],
        "example": {"question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 1\\)",
            "steps": [
                {"label": "Set equal", "content": "<p>\\(x + 1 = x^2 - 1\\)</p>"},
                {"label": "Rearrange", "content": "<p>\\(x^2 - x - 2 = 0\\)</p>"},
                {"label": "Factorise", "content": "<p>\\((x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\)</p>"},
                {"label": "Find y", "content": "<p>\\(x = 2: y = 3\\). \\(x = -1: y = 0\\).</p>"},
                {"label": "Check", "content": "<p>\\(x = 2\\) in \\(y = x^2 - 1\\): \\(4 - 1 = 3\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x = 2, y = 3\\) and \\(x = -1, y = 0\\)</p>", "isAnswer": True, "is_answer": True},
            ]}},
    "silver": {
        "title": "Silver: rearrange with care, then solve",
        "steps": [
            "The linear part may be \\(y = 3x + 2\\) or \\(x + y = 4\\); rearrange it to \\(y = …\\) first if needed.",
            "If the second equation is a circle \\(x^2 + y^2 = r^2\\), substitute and square the bracket in full.",
            "Gather x-terms and numbers from <strong>both</strong> sides before you factorise, watching every sign.",
        ],
        "example": {"question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 4x + 5\\)",
            "steps": [
                {"label": "Set equal", "content": "<p>\\(x + 1 = x^2 - 4x + 5\\)</p>"},
                {"label": "Rearrange", "content": "<p>\\(x^2 - 5x + 4 = 0\\)</p>"},
                {"label": "Factorise", "content": "<p>\\((x - 1)(x - 4) = 0\\), so \\(x = 1\\) or \\(x = 4\\)</p>"},
                {"label": "Find y", "content": "<p>\\(x = 1: y = 2\\). \\(x = 4: y = 5\\).</p>"},
                {"label": "Check", "content": "<p>\\(x = 4\\) in \\(y = x^2 - 4x + 5\\): \\(16 - 16 + 5 = 5\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x = 1, y = 2\\) and \\(x = 4, y = 5\\)</p>", "isAnswer": True, "is_answer": True},
            ]}},
    "gold": {
        "title": "Gold: circles, products and tangents",
        "steps": [
            "For a circle \\(x^2 + y^2 = r^2\\), rearrange the line to \\(y = …\\) and substitute, squaring the bracket in full.",
            "\\((x + a)^2 = x^2 + 2ax + a^2\\): never square the two terms separately.",
            "A tangent touches once, so its discriminant \\(b^2 - 4ac\\) is zero: use this to find an unknown.",
        ],
        "example": {"question": "Solve \\(x + y = 7\\) and \\(x^2 + y^2 = 29\\)",
            "steps": [
                {"label": "Rearrange line", "content": "<p>\\(y = 7 - x\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(x^2 + (7 - x)^2 = 29\\) → \\(2x^2 - 14x + 20 = 0\\)</p>"},
                {"label": "Simplify and factorise", "content": "<p>\\(x^2 - 7x + 10 = 0\\) → \\((x - 2)(x - 5) = 0\\), so \\(x = 2\\) or \\(x = 5\\)</p>"},
                {"label": "Find y", "content": "<p>\\(x = 2: y = 5\\). \\(x = 5: y = 2\\).</p>"},
                {"label": "Check", "content": "<p>\\((2, 5)\\): \\(4 + 25 = 29\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x = 2, y = 5\\) and \\(x = 5, y = 2\\)</p>", "isAnswer": True, "is_answer": True},
            ]}},
}

# ============ GUIDED (opener + teach) ============
def opener():
    # x^2 = x + 12 -> x=4, x=-3
    assert 4*4 == 4 + 12 and (-3)*(-3) == -3 + 12
    return {"label": "Before any algebra",
        "display": "I square my number and get 12 more than the number itself.",
        "steps": [
            {"pre": "One number that works is ", "post": "", "answer": 4,
             "say": "A guess-the-number puzzle, no algebra needed. I am thinking of a number. When I square it, I get 12 more than the number I started with.",
             "hint": "Try 4: four squared is 16, and 16 is 12 more than 4."},
            {"pre": "The other number is ", "post": "", "answer": -3,
             "say": "Good. There is a second number that also works, and it is negative.",
             "hint": "Try −3: negative three squared is 9, and 9 is 12 more than −3."},
            {"say": "You just solved \\(x^2 = x + 12\\) and found BOTH answers, \\(x = 4\\) and \\(x = -3\\). That is the whole topic: an equation with a square in it usually has TWO answers. In algebra it appears as a line \\(y = x + 12\\) crossing a curve \\(y = x^2\\); they meet at two points, so there are two x-values to find."},
        ]}

def teach_bronze():
    # y=x+4, y=x^2-2 -> x^2-x-6=0 -> (x-3)(x+2) -> 3,-2 ; y=7,2
    return {"label": "Together: your first one", "display": "Solve \\(y = x + 4\\) and \\(y = x^2 - 2\\)",
        "steps": [
            {"pre": "The x-term becomes ", "post": "x", "answer": -1,
             "say": "Both equations give y, so set them equal: \\(x + 4 = x^2 - 2\\). Bring every term to the right so \\(x^2\\) stays positive.",
             "hint": "The line's +x moves across to become −x."},
            {"pre": "and the constant becomes ", "post": "", "answer": -6,
             "hint": "The +4 moves across, and −2 stays: −4 − 2."},
            {"pre": "First root, x = ", "post": "", "answer": 3,
             "say": "So \\(x^2 - x - 6 = 0\\). Two numbers multiply to \\(-6\\) and add to \\(-1\\): they are \\(-3\\) and \\(+2\\), giving \\((x - 3)(x + 2) = 0\\).",
             "hint": "Set x − 3 = 0."},
            {"pre": "Second root, x = ", "post": "", "answer": -2, "hint": "Set x + 2 = 0."},
            {"pre": "At x = 3: y = ", "post": "", "answer": 7,
             "say": "Each x gets its y from \\(y = x + 4\\).", "hint": "3 + 4."},
            {"pre": "At x = −2: y = ", "post": "", "answer": 2, "hint": "−2 + 4."},
            {"pre": "Check x = 3 in the curve: 3² − 2 = ", "post": "", "answer": 7,
             "done": "It equals y = 7, so (3, 7) is right and (−2, 2) checks the same way.",
             "hint": "9 − 2."},
        ]}

def teach_silver():
    # y=2x+1, y=x^2-x+3 -> x^2-3x+2=0 -> (x-1)(x-2) -> 1,2 ; y=3,5
    return {"label": "Together: the silver move", "display": "Solve \\(y = 2x + 1\\) and \\(y = x^2 - x + 3\\)",
        "steps": [
            {"pre": "Collect the x-terms, −x − 2x = ", "post": "x", "answer": -3,
             "say": "Set the two right sides equal: \\(2x + 1 = x^2 - x + 3\\). There are x-terms and numbers on both sides, so move everything to the right with care.",
             "hint": "Negative 1 minus 2 is negative 3."},
            {"pre": "Collect the constants, 3 − 1 = ", "post": "", "answer": 2,
             "hint": "The +1 moves across to become −1, so 3 − 1."},
            {"pre": "First root, x = ", "post": "", "answer": 1,
             "say": "So \\(x^2 - 3x + 2 = 0\\). Two numbers multiply to 2 and add to \\(-3\\): they are \\(-1\\) and \\(-2\\), giving \\((x - 1)(x - 2) = 0\\).",
             "hint": "Set x − 1 = 0."},
            {"pre": "Second root, x = ", "post": "", "answer": 2, "hint": "Set x − 2 = 0."},
            {"pre": "At x = 1: y = ", "post": "", "answer": 3,
             "say": "Each x gets its y from \\(y = 2x + 1\\).", "hint": "2 times 1, plus 1."},
            {"pre": "At x = 2: y = ", "post": "", "answer": 5, "hint": "2 times 2, plus 1."},
            {"pre": "Check x = 2 in the curve: 2² − 2 + 3 = ", "post": "", "answer": 5,
             "done": "It equals y = 5, so (2, 5) is right and (1, 3) checks the same way.",
             "hint": "4 − 2 + 3."},
        ]}

def teach_gold():
    # x+y=6, x^2+y^2=20 -> y=6-x -> 2x^2-12x+16=0 -> x^2-6x+8=0 -> (x-2)(x-4) -> 2,4 ; y=4,2
    return {"label": "Together: the gold move", "display": "Solve \\(x + y = 6\\) and \\(x^2 + y^2 = 20\\)",
        "steps": [
            {"pre": "The middle term, 2 × 6 × (−1), is ", "post": "x", "answer": -12,
             "say": "The second equation is a circle. Rearrange the line: \\(x + y = 6\\) becomes \\(y = 6 - x\\). Substitute into \\(x^2 + y^2 = 20\\): \\(x^2 + (6 - x)^2 = 20\\). Expand \\((6 - x)^2 = 36 - 12x + x^2\\).",
             "hint": "2 times 6 is 12, and it is negative."},
            {"pre": "Collect the two x² terms: 1 + 1 = ", "post": "x²", "answer": 2,
             "say": "So \\(x^2 + 36 - 12x + x^2 = 20\\).", "hint": "One x² from each part."},
            {"pre": "The constant, 36 − 20, becomes ", "post": "", "answer": 16,
             "say": "That gives \\(2x^2 - 12x + 36 = 20\\). Take 20 across.", "hint": "36 minus 20."},
            {"pre": "Divide by 2, then the x-term −12 ÷ 2 becomes ", "post": "x", "answer": -6,
             "say": "So \\(2x^2 - 12x + 16 = 0\\). Divide every term by 2.", "hint": "Half of negative 12."},
            {"pre": "First root, x = ", "post": "", "answer": 2,
             "say": "That leaves \\(x^2 - 6x + 8 = 0\\), which factorises as \\((x - 2)(x - 4) = 0\\).",
             "hint": "Set x − 2 = 0."},
            {"pre": "Second root, x = ", "post": "", "answer": 4, "hint": "Set x − 4 = 0."},
            {"pre": "At x = 2: y = ", "post": "", "answer": 4,
             "say": "Each x gets its y from \\(y = 6 - x\\).", "hint": "6 − 2."},
            {"pre": "At x = 4: y = ", "post": "", "answer": 2, "hint": "6 − 4."},
            {"pre": "Check (2, 4) in the circle: 2² + 4² = ", "post": "", "answer": 20,
             "done": "It equals 20, so (2, 4) is right and (4, 2) checks the same way.",
             "hint": "4 + 16."},
        ]}

guided = {"opener": opener(),
          "teach": {"bronze": teach_bronze(), "silver": teach_silver(), "gold": teach_gold()}}

# ============ METHOD CARD (slim) ============
method_card = {
    "title": "Simultaneous Equations (One Linear, One Quadratic)",
    "steps": [
        "Rearrange the linear equation to make one letter the subject.",
        "Substitute it into the quadratic, expanding any bracket in full.",
        "Rearrange to a quadratic equal to zero, then factorise or use the formula.",
        "Substitute each x back into the linear equation for its y, and give both pairs.",
    ],
    "content": "<p>When one equation is a straight line and the other is a curve (a quadratic, or a circle \\(x^2 + y^2 = r^2\\)), use <strong>substitution</strong>. The line usually crosses the curve at two points, so expect two pairs of answers.</p><p>Make a letter the subject of the line, substitute it in, and simplify to a quadratic equal to zero. Solve it, then find each matching value from the line.</p>",
    "example": "<p><strong>Solve</strong> \\(y = x + 1\\) and \\(y = x^2 - 1\\)</p><p>\\(x + 1 = x^2 - 1 \\Rightarrow x^2 - x - 2 = 0 \\Rightarrow (x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\). Then \\(y = 3\\) or \\(y = 0\\): the pairs are \\((2, 3)\\) and \\((-1, 0)\\).</p>",
}

topic_links = {"prerequisites": [
    {"slug": "algebra/9", "title": "Simultaneous Equations (Linear)"},
    {"slug": "algebra/7", "title": "Solving Quadratics by Factorising"},
]}

# ============ ASSEMBLE (preserve related_videos + worked_examples byte-for-byte) ============
out = {
    "guided": guided,
    "method_card": method_card,
    "tier_guides": tier_guides,
    "topic_links": topic_links,
    "problem_bank": pb,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
}

json.dump(out, open("lesson_maths-aqa_algebra-L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("built lesson_maths-aqa_algebra-L10.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
