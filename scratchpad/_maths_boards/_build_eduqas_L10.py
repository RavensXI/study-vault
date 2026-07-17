# -*- coding: utf-8 -*-
import json, math

M = "−"          # unicode minus for plain text
SUP2 = "²"        # superscript two

# ---------- LaTeX helpers ----------
def lterm(c, var):
    """LaTeX signed term, e.g. ' - 3x', ' + x', '' if 0. Uses ascii - inside LaTeX."""
    if c == 0:
        return ""
    a = abs(c)
    sign = "+" if c > 0 else "-"
    if var and a == 1:
        body = var
    else:
        body = ("%g" % a) + var
    return " %s %s" % (sign, body)

def quad_latex(B, C):
    return "x^2" + lterm(B, "x") + lterm(C, "")

def bracket(r):
    # (x - r) if r>=0 else (x + |r|)
    if r >= 0:
        return "(x - %g)" % r
    return "(x + %g)" % (abs(r))

def factor_latex(r1, r2):
    return bracket(r1) + bracket(r2)

# ---------- builders ----------
def std_parabola(la, lb, cp, cq, r1, r2, line_tex, curve_tex, check_tex):
    """line y = la*x + lb ; curve y = x^2 + cp*x + cq. Set equal -> x^2 + Bx + C=0."""
    B = cp - la
    C = cq - lb
    # verify factorisation
    assert r1 + r2 == -B, (la, lb, cp, cq, r1, r2, B)
    assert r1 * r2 == C, (la, lb, cp, cq, r1, r2, C)
    L = lambda x: la * x + lb
    Q = lambda x: x * x + cp * x + cq
    assert L(r1) == Q(r1) and L(r2) == Q(r2)
    y1, y2 = L(r1), L(r2)
    # factor say
    n1, n2 = -r1, -r2   # the numbers inside brackets
    fac_say = ("So \\(%s = 0\\). Two numbers multiply to %g and add to %g: they are %g and %g, giving \\(%s = 0\\)."
               % (quad_latex(B, C), C, B, n1, n2, factor_latex(r1, r2)))
    steps = [
        {"say": "Both equations give y, so set the two right sides equal: \\(%s = %s\\). Bring every term to the right so \\(x^2\\) stays positive." % (line_tex, curve_tex)},
        {"pre": "The x-term becomes ", "post": "x", "answer": B,
         "hint": "Take the line's x-term across the equals sign, changing its sign, then combine."},
        {"pre": "and the constant becomes ", "post": "", "answer": C,
         "hint": "Take the line's constant across the equals sign, changing its sign."},
        {"pre": "First root, x = ", "post": "", "phase": "substitute", "answer": r1,
         "say": fac_say, "hint": "Set the bracket %s to zero." % bracket(r1)},
        {"pre": "Second root, x = ", "post": "", "answer": r2,
         "hint": "Set the other bracket to zero."},
        {"pre": "At x = %g: y = " % r1, "post": "", "answer": y1,
         "say": "Now each x gets its y from the line \\(%s\\)." % line_tex,
         "hint": "Put x = %g into the line." % r1},
        {"pre": "At x = %g: y = " % r2, "post": "", "answer": y2,
         "hint": "Put x = %g into the line." % r2},
        {"pre": "Check: %s = " % check_tex, "post": "", "answer": Q(r1),
         "say": "Last check: put the first pair into the curve.",
         "done": "It equals y = %g, so (%g, %g) is right and (%g, %g) checks the same way." % (y1, r1, y1, r2, y2),
         "hint": "Substitute x = %g into the curve; it should give y = %g." % (r1, y1)},
    ]
    return steps, [r1, r2], (n1, n2, B, C, r1, r2)

def horizontal(b, cq, k, r_pos, curve_tex, check_tex):
    """line y = b (constant) ; curve y = x^2 + cq. x^2 = b - cq = k, roots +-r_pos."""
    assert b - cq == k and r_pos * r_pos == k
    steps = [
        {"say": "Both sides give y, so set them equal: \\(%g = %s\\). Get \\(x^2\\) on its own." % (b, curve_tex)},
        {"pre": "So x² = ", "post": "", "answer": k,
         "hint": "Move the number across the equals sign to leave x squared by itself."},
        {"pre": "First root (positive), x = ", "post": "", "phase": "substitute", "answer": r_pos,
         "say": "\\(x^2 = %g\\) has TWO roots, one positive and one negative." % k,
         "hint": "The positive square root of %g." % k},
        {"pre": "Second root (negative), x = ", "post": "", "answer": -r_pos,
         "hint": "The negative square root of %g." % k},
        {"pre": "Both roots give the same y. y = ", "post": "", "answer": b,
         "say": "The line is flat, so y is the same at both points.",
         "hint": "Read it straight off the line."},
        {"pre": "Check: %s = " % check_tex, "post": "", "answer": r_pos * r_pos + cq,
         "done": "It equals y = %g, so (%g, %g) is right and (%g, %g) checks the same way." % (b, r_pos, b, -r_pos, b),
         "hint": "Substitute x = %g into the curve; it should give y = %g." % (r_pos, b)},
    ]
    return steps, [r_pos, -r_pos]

def common_factor(la, cp, cq, r_nonzero, line_tex, curve_tex, check_tex):
    """y = la*x ; y = x^2 + cp*x + cq (cq=0 here). Set equal -> x^2 + (cp-la)x = 0."""
    B = cp - la
    assert cq == 0 and -B == r_nonzero
    L = lambda x: la * x
    Q = lambda x: x * x + cp * x + cq
    y0, y1 = L(0), L(r_nonzero)
    steps = [
        {"say": "Both equations give y, so set the two right sides equal: \\(%s = %s\\). Bring every term to the right so \\(x^2\\) stays positive." % (line_tex, curve_tex)},
        {"pre": "The x-term becomes ", "post": "x", "answer": B,
         "hint": "Take the line's x-term across the equals sign, changing its sign, then combine."},
        {"pre": "There is no constant, so factor out x. First root, x = ", "post": "", "phase": "substitute", "answer": 0,
         "say": "So \\(x^2%s = 0\\). Take out a common factor of x: \\(x(x%s) = 0\\)." % (lterm(B, "x"), lterm(B, "")),
         "hint": "Setting the factor x to zero gives x = 0."},
        {"pre": "Second root, x = ", "post": "", "answer": r_nonzero,
         "hint": "Set the other bracket to zero."},
        {"pre": "At x = 0: y = ", "post": "", "answer": y0,
         "say": "Now each x gets its y from the line \\(%s\\)." % line_tex,
         "hint": "Put x = 0 into the line."},
        {"pre": "At x = %g: y = " % r_nonzero, "post": "", "answer": y1,
         "hint": "Put x = %g into the line." % r_nonzero},
        {"pre": "Check: %s = " % check_tex, "post": "", "answer": Q(r_nonzero),
         "done": "It equals y = %g, so (%g, %g) is right and (0, 0) checks the same way." % (y1, r_nonzero, y1),
         "hint": "Substitute x = %g into the curve; it should give y = %g." % (r_nonzero, y1)},
    ]
    return steps, [0, r_nonzero]

print("helpers loaded")

def circle_divide(la, lb, R, r1, r2, orig_line_tex, middle_desc, expand_tex, collected_tex):
    """line y = la*x + lb, circle x^2+y^2=R. A=1+la^2 divides through."""
    A = 1 + la * la
    Bc = 2 * la * lb
    Cc = lb * lb - R
    # monic after dividing by A
    mB = Bc // A
    mC = Cc // A
    assert Bc % A == 0 and Cc % A == 0
    assert r1 + r2 == -mB and r1 * r2 == mC
    L = lambda x: la * x + lb
    # verify pairs on circle
    for x in (r1, r2):
        assert abs(x * x + L(x) ** 2 - R) < 1e-9, (x, L(x), R)
    y1, y2 = L(r1), L(r2)
    fac = factor_latex(r1, r2)
    steps = [
        {"pre": "The middle term, %s, is " % middle_desc, "post": "x", "answer": Bc,
         "say": "%s Expand \(%s\)." % (orig_line_tex, expand_tex),
         "hint": "Double the product of the two terms in the bracket."},
        {"pre": "Collect the two x² terms: 1 + %g = " % (la * la), "post": "x²", "answer": A,
         "say": "So \(%s\)." % collected_tex,
         "hint": "One x² from the first part, %g from the bracket." % (la * la)},
        {"pre": "The constant, %g − %g, becomes " % (lb * lb, R), "post": "", "answer": Cc,
         "hint": "%g minus %g." % (lb * lb, R)},
        {"pre": "First root, x = ", "post": "", "phase": "substitute", "answer": r1,
         "say": "So \(%gx^2%s%s = 0\). Divide every term by %g to get \(%s = 0\), which factorises as \(%s = 0\)."
                % (A, lterm(Bc, "x"), lterm(Cc, ""), A, quad_latex(mB, mC), fac),
         "hint": "Set the bracket %s to zero." % bracket(r1)},
        {"pre": "Second root, x = ", "post": "", "answer": r2,
         "hint": "Set the bracket %s to zero." % bracket(r2)},
        {"pre": "At x = %g: y = " % r1, "post": "", "answer": y1,
         "say": "Each x gets its y from the line \(y = %g%s%s\)." % (la, "x", lterm(lb, "")) if False else "Each x gets its y from the line.",
         "hint": "Put x = %g into the line." % r1},
        {"pre": "At x = %g: y = " % r2, "post": "", "answer": y2,
         "hint": "Put x = %g into the line." % r2},
        {"pre": "Check (%g, %g) in the circle: %g² + %g² = " % (r1, y1, r1, y1), "post": "", "answer": R,
         "done": "It equals %g, so (%g, %g) is right and (%g, %g) checks the same way." % (R, r1, y1, r2, y2),
         "hint": "%g squared plus %g squared." % (r1, y1)},
    ]
    return steps, [r1, r2]

def hyperbola(la, lb, k, r1, r2, orig_line_tex, line_solved_tex, sub_tex):
    """line rearranged y = la*x + lb, product xy = k. la assumed -1 (or general)."""
    # x(la x + lb) = k -> la x^2 + lb x - k = 0 ; multiply by -1 (la=-1) -> x^2 - lb x + k
    assert la == -1
    B = -lb
    C = k
    assert r1 + r2 == -B and r1 * r2 == C
    L = lambda x: la * x + lb
    for x in (r1, r2):
        assert abs(x * L(x) - k) < 1e-9, (x, L(x), k)
    y1, y2 = L(r1), L(r2)
    fac = factor_latex(r1, r2)
    steps = [
        {"pre": "Make x² positive and tidy; the x-term becomes ", "post": "x", "answer": B,
         "say": "The second equation is \(xy = %g\). Rearrange the line to \(%s\) and substitute: \(%s\). Expanding gives \(%gx - x^2 = %g\); multiply through by \(-1\) so \(x^2\) is positive." % (k, line_solved_tex, sub_tex, lb, k),
         "hint": "After multiplying by −1 the x-term is %g." % B},
        {"pre": "and the constant becomes ", "post": "", "answer": C,
         "hint": "The %g moves across and its sign flips to +%g." % (k, k)},
        {"pre": "First root, x = ", "post": "", "phase": "substitute", "answer": r1,
         "say": "So \(%s = 0\), which factorises as \(%s = 0\)." % (quad_latex(B, C), fac),
         "hint": "Set the bracket %s to zero." % bracket(r1)},
        {"pre": "Second root, x = ", "post": "", "answer": r2,
         "hint": "Set the bracket %s to zero." % bracket(r2)},
        {"pre": "At x = %g: y = " % r1, "post": "", "answer": y1,
         "say": "Each x gets its y from the line \(%s\)." % line_solved_tex,
         "hint": "Put x = %g into the line." % r1},
        {"pre": "At x = %g: y = " % r2, "post": "", "answer": y2,
         "hint": "Put x = %g into the line." % r2},
        {"pre": "Check x = %g, y = %g in the product: %g × %g = " % (r1, y1, r1, y1), "post": "", "answer": k,
         "done": "It equals %g, so (%g, %g) is right and (%g, %g) checks the same way." % (k, r1, y1, r2, y2),
         "hint": "Multiply the pair together."},
    ]
    return steps, [r1, r2]

print("all builders loaded")
