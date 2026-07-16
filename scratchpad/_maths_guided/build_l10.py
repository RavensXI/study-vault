# -*- coding: utf-8 -*-
"""Build algebra-L10 guided practice_data. Computes & verifies every number."""
import json, io, os, urllib.request
from fractions import Fraction as F

MINUS = "−"   # unicode minus for plain-text prose
TIMES = "×"
SUP2 = "²"

# ---------- verification helpers ----------
def approx(a, b): return abs(float(a) - float(b)) < 1e-9

def sq_plain(x):
    """plain-text  x^2 value display like  3²  or  (−2)² """
    xs = num_plain(x)
    return ("(" + xs + ")" if x < 0 else xs) + SUP2

def num_plain(x):
    """plain-text number using unicode minus; ints render clean"""
    if isinstance(x, float) and x == int(x): x = int(x)
    s = str(x)
    return s.replace("-", MINUS)

def latex_num(x):
    if isinstance(x, float) and x == int(x): x = int(x)
    return str(x)

# ---------- category A (both y=) generator ----------
def factor_latex(r):
    r = int(r)
    if r == 0: return "x"
    if r > 0: return "(x - %d)" % r
    return "(x + %d)" % (-r)

def quad_latex(b, c):
    # x^2 + b x + c
    s = "x^2"
    if b: s += (" + %dx" % b) if b > 0 else (" - %dx" % (-b))
    if c: s += (" + %d" % c) if c > 0 else (" - %d" % (-c))
    return s

def catA_steps(m, k, qb, qc, r1, r2, lin_tex, quad_tex):
    """y = m x + k  ;  y = x^2 + qb x + qc.  roots r1,r2 (order as presented)."""
    B = qb - m
    C = qc - k
    # verify roots
    for r in (r1, r2):
        assert approx(r*r + B*r + C, 0), (B, C, r)
        # both pairs satisfy both originals
        y = m*r + k
        assert approx(y, r*r + qb*r + qc)
    y1 = m*r1 + k
    y2 = m*r2 + k
    steps = []
    steps.append({"say": "Both equations give y, so set the two right sides equal: \\(%s = %s\\). Bring every term to the right so \\(x^2\\) stays positive." % (lin_tex, quad_tex)})
    # x-term box
    if m >= 0:
        hb = "The line's x-term moves across and changes sign."
    else:
        hb = "The line's x-term moves across and changes sign."
    steps.append({"pre": "The x-term becomes ", "post": "x", "answer": B,
                  "hint": "Combine the x-terms: %s minus %s." % (num_plain(qb), num_plain(m)) if False else "Take the line's x-term across the equals sign, changing its sign, then combine."})
    steps.append({"pre": "and the constant becomes ", "post": "", "answer": C,
                  "hint": "Take the line's constant across the equals sign, changing its sign."})
    if C == 0:
        fac_say = "So \\(%s = 0\\). Take out a common factor of x: \\(%s = 0\\)." % (quad_latex(B, C), "x" + factor_latex(r1 if r1 != 0 else r2))
    else:
        n1, n2 = -r1, -r2
        fac_say = "So \\(%s = 0\\). Two numbers multiply to %s and add to %s: they are %s and %s, giving \\(%s%s = 0\\)." % (
            quad_latex(B, C), latex_num(C), latex_num(B), latex_num(n1), latex_num(n2),
            factor_latex(r1), factor_latex(r2))
    # first root box carries the factor say + phase
    steps.append({"say": fac_say, "phase": "substitute",
                  "pre": "First root, x = ", "post": "", "answer": r1,
                  "hint": "Set the bracket %s to zero." % factor_latex(r1)})
    steps.append({"pre": "Second root, x = ", "post": "", "answer": r2,
                  "hint": "Set the other bracket to zero."})
    steps.append({"say": "Now each x gets its y from the line \\(y = %s\\)." % lin_tex,
                  "pre": "At x = %s: y = " % num_plain(r1), "post": "", "answer": y1,
                  "hint": "Put x = %s into the line." % num_plain(r1)})
    steps.append({"pre": "At x = %s: y = " % num_plain(r2), "post": "", "answer": y2,
                  "hint": "Put x = %s into the line." % num_plain(r2)})
    # check in the curve at r1
    chk = sq_plain(r1)
    if qb: chk += (" + %s%s%s" % (abs(qb), TIMES, ("(" + num_plain(r1) + ")" if r1 < 0 else num_plain(r1)))) if qb > 0 else (" %s %s%s%s" % (MINUS, abs(qb), TIMES, ("(" + num_plain(r1) + ")" if r1 < 0 else num_plain(r1))))
    if qc: chk += (" + %d" % qc) if qc > 0 else (" %s %d" % (MINUS, -qc))
    steps.append({"say": "Last check: put the first pair into the curve.",
                  "pre": "Work out %s = " % chk, "post": "", "answer": y1,
                  "done": "It equals y = %s, so (%s, %s) is right and (%s, %s) checks the same way." % (
                      num_plain(y1), num_plain(r1), num_plain(y1), num_plain(r2), num_plain(y2)),
                  "hint": "Substitute x = %s into the curve; it should give y = %s." % (num_plain(r1), num_plain(y1))})
    return steps, [r1, r2]

def sign_flip_expect(r1, r2):
    return [(-r1), (-r2)]

# ---------- assemble bank ----------
def prob(display, sols, steps, misc, hint, calculator=False):
    return {"hint": hint, "display": display, "solutions": sols,
            "calculator": calculator, "input_type": "two_solutions",
            "misconceptions": misc, "guided_steps": steps}

HINT_A = "Set the two right-hand sides equal, rearrange to a quadratic equal to zero, then factorise."

def sf_misc(quad_tex, facs, r1, r2):
    e = sign_flip_expect(r1, r2)
    return {"pattern": "factor_sign_flip", "expect": [int(e[0]), int(e[1])],
            "message": "Check the signs inside your brackets. \\(%s\\) factorises as \\(%s = 0\\), giving \\(x = %s\\) and \\(x = %s\\). Reversing those signs gives \\(x = %s\\) and \\(x = %s\\), which do not fit the equations." % (
                quad_tex, facs, latex_num(int(r1)), latex_num(int(r2)), latex_num(int(e[0])), latex_num(int(e[1]))),
            "note": "sign-flipped factorisation of %s" % quad_tex}

def facs_latex(r1, r2):
    return factor_latex(r1) + factor_latex(r2)

# ------- BRONZE -------
bronze = []
# B0 y=x+3 ; y=x^2+1 -> x^2-x-2 roots 2,-1
s,_ = catA_steps(1,3, 0,1, 2,-1, "y = x + 3", "y = x^2 + 1")
bronze.append(prob("Solve \\(y = x + 3\\) and \\(y = x^2 + 1\\). Give the two x-values.", [2,-1], s,
    [sf_misc("x^2 - x - 2", facs_latex(2,-1), 2,-1)], HINT_A))
# B1 y=x+6 ; y=x^2 -> x^2-x-6 roots 3,-2  (was duplicate)
s,_ = catA_steps(1,6, 0,0, 3,-2, "y = x + 6", "y = x^2")
bronze.append(prob("Solve \\(y = x + 6\\) and \\(y = x^2\\). Give the two x-values.", [3,-2], s,
    [sf_misc("x^2 - x - 6", facs_latex(3,-2), 3,-2)], HINT_A))
# B2 y=x+1 ; y=x^2-2x-3 -> x^2-3x-4 roots 4,-1  (was duplicate)
s,_ = catA_steps(1,1, -2,-3, 4,-1, "y = x + 1", "y = x^2 - 2x - 3")
bronze.append(prob("Solve \\(y = x + 1\\) and \\(y = x^2 - 2x - 3\\). Give the two x-values.", [4,-1], s,
    [sf_misc("x^2 - 3x - 4", facs_latex(4,-1), 4,-1)], HINT_A))
# B3 y=2x ; y=x^2 -> x^2-2x roots 0,2
s,_ = catA_steps(2,0, 0,0, 0,2, "y = 2x", "y = x^2")
bronze.append(prob("Solve \\(y = 2x\\) and \\(y = x^2\\). Give the two x-values.", [0,2], s,
    [{"pattern":"divide_by_x","expect":None,
      "message":"When you reach \\(x^2 - 2x = 0\\), factorise as \\(x(x - 2) = 0\\) rather than dividing both sides by x. Dividing by x throws away the solution \\(x = 0\\)."}], HINT_A))
# B4 y=x ; y=x^2+5x+3 -> x^2+4x+3 roots -1,-3  (was duplicate)
s,_ = catA_steps(1,0, 5,3, -1,-3, "y = x", "y = x^2 + 5x + 3")
bronze.append(prob("Solve \\(y = x\\) and \\(y = x^2 + 5x + 3\\). Give the two x-values.", [-1,-3], s,
    [sf_misc("x^2 + 4x + 3", facs_latex(-1,-3), -1,-3)], HINT_A))
# B5 y=x-1 ; y=x^2-3x+2 -> x^2-4x+3 roots 1,3
s,_ = catA_steps(1,-1, -3,2, 1,3, "y = x - 1", "y = x^2 - 3x + 2")
bronze.append(prob("Solve \\(y = x - 1\\) and \\(y = x^2 - 3x + 2\\). Give the two x-values.", [1,3], s,
    [sf_misc("x^2 - 4x + 3", facs_latex(1,3), 1,3)], HINT_A))
# B6 y=3x ; y=x^2+2 -> x^2-3x+2 roots 1,2
s,_ = catA_steps(3,0, 0,2, 1,2, "y = 3x", "y = x^2 + 2")
bronze.append(prob("Solve \\(y = 3x\\) and \\(y = x^2 + 2\\). Give the two x-values.", [1,2], s,
    [sf_misc("x^2 - 3x + 2", facs_latex(1,2), 1,2)], HINT_A))
# B7 y=x+4 ; y=x^2+x -> x^2-4 roots 2,-2
s,_ = catA_steps(1,4, 1,0, 2,-2, "y = x + 4", "y = x^2 + x")
bronze.append(prob("Solve \\(y = x + 4\\) and \\(y = x^2 + x\\). Give the two x-values.", [2,-2], s,
    [{"pattern":"positive_root_only","expect":None,
      "message":"\\(x^2 - 4 = 0\\) means \\(x^2 = 4\\), so \\(x = 2\\) and \\(x = -2\\). Remember the negative square root as well as the positive one."}], HINT_A))

# ------- SILVER -------
silver = []
# S0 y=2x+1 ; y=x^2+x-1 -> x^2-x-2 roots 2,-1
s,_ = catA_steps(2,1, 1,-1, 2,-1, "y = 2x + 1", "y = x^2 + x - 1")
silver.append(prob("Solve \\(y = 2x + 1\\) and \\(y = x^2 + x - 1\\). Give the two x-values.", [2,-1], s,
    [sf_misc("x^2 - x - 2", facs_latex(2,-1), 2,-1)], HINT_A))
# S1 y=x+3 ; y=x^2-2x-1 -> x^2-3x-4 roots 4,-1  (was duplicate)
s,_ = catA_steps(1,3, -2,-1, 4,-1, "y = x + 3", "y = x^2 - 2x - 1")
silver.append(prob("Solve \\(y = x + 3\\) and \\(y = x^2 - 2x - 1\\). Give the two x-values.", [4,-1], s,
    [sf_misc("x^2 - 3x - 4", facs_latex(4,-1), 4,-1)], HINT_A))
# S2 y=3-x ; y=x^2-3 -> x^2+x-6 roots 2,-3
s,_ = catA_steps(-1,3, 0,-3, 2,-3, "y = 3 - x", "y = x^2 - 3")
silver.append(prob("Solve \\(y = 3 - x\\) and \\(y = x^2 - 3\\). Give the two x-values.", [2,-3], s,
    [sf_misc("x^2 + x - 6", facs_latex(2,-3), 2,-3)], HINT_A))
# S3 y=2x-3 ; y=x^2-3 -> x^2-2x roots 0,2
s,_ = catA_steps(2,-3, 0,-3, 0,2, "y = 2x - 3", "y = x^2 - 3")
silver.append(prob("Solve \\(y = 2x - 3\\) and \\(y = x^2 - 3\\). Give the two x-values.", [0,2], s,
    [{"pattern":"divide_by_x","expect":None,
      "message":"When you reach \\(x^2 - 2x = 0\\), factorise as \\(x(x - 2) = 0\\) rather than dividing both sides by x, or you lose the solution \\(x = 0\\)."}], HINT_A))
# S4 x+y=4 ; xy=3 -> x^2-4x+3 roots 1,3 (special build below)
# S5 y=5-2x ; y=x^2-4x+2 -> x^2-2x-3 roots 3,-1
s,_ = catA_steps(-2,5, -4,2, 3,-1, "y = 5 - 2x", "y = x^2 - 4x + 2")
S5 = prob("Solve \\(y = 5 - 2x\\) and \\(y = x^2 - 4x + 2\\). Give the two x-values.", [3,-1], s,
    [sf_misc("x^2 - 2x - 3", facs_latex(3,-1), 3,-1)], HINT_A)
# S6 y=x+2 ; y=x^2+x-2 -> x^2-4 roots 2,-2
s,_ = catA_steps(1,2, 1,-2, 2,-2, "y = x + 2", "y = x^2 + x - 2")
S6 = prob("Solve \\(y = x + 2\\) and \\(y = x^2 + x - 2\\). Give the two x-values.", [2,-2], s,
    [{"pattern":"positive_root_only","expect":None,
      "message":"\\(x^2 - 4 = 0\\) gives \\(x^2 = 4\\), so \\(x = 2\\) and \\(x = -2\\). Do not stop at the positive root."}], HINT_A)

# S4 special (xy=3)
S4_steps = [
  {"say":"Rearrange the line: \\(x + y = 4\\) becomes \\(y = 4 - x\\). Substitute into \\(xy = 3\\): \\(x(4 - x) = 3\\), which expands to \\(4x - x^2 = 3\\). Bring everything to one side so \\(x^2\\) is positive.",
   "pre":"The equation becomes x² − 4x + ", "post":" = 0", "answer":3, "hint":"Move the 3 across to join the left side."},
  {"say":"So \\(x^2 - 4x + 3 = 0\\). Two numbers multiply to 3 and add to \\(-4\\): they are \\(-1\\) and \\(-3\\), giving \\((x - 1)(x - 3) = 0\\).",
   "phase":"substitute","pre":"First root, x = ","post":"","answer":1,"hint":"Set x − 1 = 0."},
  {"pre":"Second root, x = ","post":"","answer":3,"hint":"Set x − 3 = 0."},
  {"say":"Each x gets its y from \\(y = 4 - x\\).","pre":"At x = 1: y = ","post":"","answer":3,"hint":"4 − 1."},
  {"pre":"At x = 3: y = ","post":"","answer":1,"hint":"4 − 3."},
  {"say":"Notice the pairs are (1, 3) and (3, 1): the same two numbers.","pre":"Check by multiplying: 1 × 3 = ","post":"","answer":3,
   "done":"It equals 3, so both pairs satisfy xy = 3.","hint":"1 times 3."},
]
S4 = prob("Solve \\(x + y = 4\\) and \\(xy = 3\\). Give the two x-values.", [3,1], S4_steps,
    [sf_misc("x^2 - 4x + 3", facs_latex(1,3), 1,3)],
    "Write y = 4 − x, substitute into xy = 3, and solve the quadratic in x.")
# verify S4
for r,y in [(1,3),(3,1)]:
    assert approx(r+y,4) and approx(r*y,3)

silver.append(S4)
silver.append(S5)
silver.append(S6)
# silver order: S0,S1,S2,S3,S4,S5,S6  -> matches indices
silver = [silver[0], silver[1], silver[2], silver[3], S4, S5, S6]

# ------- GOLD (circles + G4) -------
HINT_CIRCLE = "Rearrange the line to make y the subject, substitute into the circle, and expand the bracket in full."

def circle_check(r, k):
    return "%s + %s = " % (sq_plain(r).replace("(","").replace(")","") if r>=0 else sq_plain(r), None)

# G0 x+y=7 ; x^2+y^2=25 -> y=7-x -> x^2-7x+12 roots 3,4
def verify_circle(m,k,K,r1,r2):
    for r in (r1,r2):
        y=m*r+k
        assert approx(r*r + y*y, K), (r,y,K)
    return m*r1+k, m*r2+k

y1,y2 = verify_circle(-1,7,25,3,4)
G0 = prob("Solve \\(x + y = 7\\) and \\(x^2 + y^2 = 25\\). Give the two x-values.", [4,3], [
  {"say":"Rearrange the line: \\(x + y = 7\\) becomes \\(y = 7 - x\\). Substitute into the circle: \\(x^2 + (7 - x)^2 = 25\\). Expand \\((7 - x)^2 = 49 - 14x + x^2\\).",
   "pre":"The middle term, 2 × 7 × (−1), is ","post":"x","answer":-14,"hint":"2 times 7 is 14, and it is negative."},
  {"say":"So \\(x^2 + 49 - 14x + x^2 = 25\\).","pre":"Collect the two x² terms: 1 + 1 = ","post":"x²","answer":2,"hint":"One x² from each part."},
  {"say":"That gives \\(2x^2 - 14x + 49 = 25\\). Take 25 across.","pre":"The constant, 49 − 25, becomes ","post":"","answer":24,"hint":"49 minus 25."},
  {"say":"So \\(2x^2 - 14x + 24 = 0\\). Divide every term by 2 to get \\(x^2 - 7x + 12 = 0\\), which factorises as \\((x - 3)(x - 4) = 0\\).",
   "phase":"substitute","pre":"First root, x = ","post":"","answer":3,"hint":"Set x − 3 = 0."},
  {"pre":"Second root, x = ","post":"","answer":4,"hint":"Set x − 4 = 0."},
  {"say":"Each x gets its y from \\(y = 7 - x\\).","pre":"At x = 3: y = ","post":"","answer":4,"hint":"7 − 3."},
  {"pre":"At x = 4: y = ","post":"","answer":3,"hint":"7 − 4."},
  {"pre":"Check (3, 4) in the circle: 3² + 4² = ","post":"","answer":25,"done":"It equals 25, so (3, 4) is right and (4, 3) checks the same way.","hint":"9 + 16."},
], [sf_misc("x^2 - 7x + 12", facs_latex(3,4), 3,4),
    {"pattern":"square_bracket_error","expect":None,
     "message":"Expand \\((7 - x)^2\\) in full as \\(49 - 14x + x^2\\); do not square the terms separately to \\(49 + x^2\\), or the middle term is lost."}], HINT_CIRCLE)

# G1 y=2x+1 ; x^2+y^2=10 -> 5x^2+4x-9 roots 1,-1.8
for r,y in [(1,3),(-1.8,-2.6)]:
    assert approx(r*r+y*y,10), (r,y)
G1 = prob("Solve \\(y = 2x + 1\\) and \\(x^2 + y^2 = 10\\). Give the two x-values.", [1,-1.8], [
  {"say":"Substitute \\(y = 2x + 1\\) into the circle: \\(x^2 + (2x + 1)^2 = 10\\). Expand \\((2x + 1)^2 = 4x^2 + 4x + 1\\).",
   "pre":"The middle term, 2 × 2x × 1, is ","post":"x","answer":4,"hint":"2 times 2 times 1 is 4."},
  {"say":"So \\(x^2 + 4x^2 + 4x + 1 = 10\\).","pre":"Collect the x² terms: 1 + 4 = ","post":"x²","answer":5,"hint":"One x² from the first part, four from the bracket."},
  {"say":"That gives \\(5x^2 + 4x + 1 = 10\\). Take 10 across.","pre":"The constant, 1 − 10, becomes ","post":"","answer":-9,"hint":"1 minus 10 is negative 9."},
  {"say":"So \\(5x^2 + 4x - 9 = 0\\). This factorises as \\((5x + 9)(x - 1) = 0\\).",
   "phase":"substitute","pre":"From x − 1 = 0, the first root is x = ","post":"","answer":1,"hint":"Set x − 1 = 0."},
  {"say":"From \\(5x + 9 = 0\\), \\(5x = -9\\).","pre":"So the second root is x = ","post":"","answer":-1.8,"hint":"Negative 9 divided by 5 is negative 1.8."},
  {"say":"Each x gets its y from \\(y = 2x + 1\\).","pre":"At x = 1: y = ","post":"","answer":3,"hint":"2 times 1, plus 1."},
  {"pre":"At x = −1.8: y = ","post":"","answer":-2.6,"hint":"2 times negative 1.8 is negative 3.6, plus 1."},
  {"pre":"Check (1, 3) in the circle: 1² + 3² = ","post":"","answer":10,"done":"It equals 10, so (1, 3) is right and (−1.8, −2.6) checks the same way.","hint":"1 + 9."},
], [{"pattern":"factor_sign_flip","expect":[1.8,-1],
     "message":"\\(5x^2 + 4x - 9 = 0\\) factorises as \\((5x + 9)(x - 1) = 0\\), giving \\(x = 1\\) and \\(x = -1.8\\). Reversing the signs gives \\(x = 1.8\\) and \\(x = -1\\), which do not satisfy the circle.",
     "note":"sign-flipped factorisation of 5x^2+4x-9"},
    {"pattern":"square_bracket_error","expect":None,
     "message":"Expand \\((2x + 1)^2\\) in full as \\(4x^2 + 4x + 1\\); squaring the terms separately to \\(4x^2 + 1\\) loses the middle term 4x."}], HINT_CIRCLE)

# G2 x-y=1 ; x^2+y^2=13 -> y=x-1 -> x^2-x-6 roots 3,-2
verify_circle(1,-1,13,3,-2)
G2 = prob("Solve \\(x - y = 1\\) and \\(x^2 + y^2 = 13\\). Give the two x-values.", [3,-2], [
  {"say":"Rearrange the line: \\(x - y = 1\\) becomes \\(y = x - 1\\). Substitute: \\(x^2 + (x - 1)^2 = 13\\). Expand \\((x - 1)^2 = x^2 - 2x + 1\\).",
   "pre":"The middle term, 2 × x × (−1), is ","post":"x","answer":-2,"hint":"2 times 1 is 2, and it is negative."},
  {"say":"So \\(x^2 + x^2 - 2x + 1 = 13\\).","pre":"Collect the two x² terms: 1 + 1 = ","post":"x²","answer":2,"hint":"One x² from each part."},
  {"say":"That gives \\(2x^2 - 2x + 1 = 13\\). Take 13 across.","pre":"The constant, 1 − 13, becomes ","post":"","answer":-12,"hint":"1 minus 13 is negative 12."},
  {"say":"So \\(2x^2 - 2x - 12 = 0\\). Divide by 2 to get \\(x^2 - x - 6 = 0\\), which factorises as \\((x - 3)(x + 2) = 0\\).",
   "phase":"substitute","pre":"First root, x = ","post":"","answer":3,"hint":"Set x − 3 = 0."},
  {"pre":"Second root, x = ","post":"","answer":-2,"hint":"Set x + 2 = 0."},
  {"say":"Each x gets its y from \\(y = x - 1\\).","pre":"At x = 3: y = ","post":"","answer":2,"hint":"3 − 1."},
  {"pre":"At x = −2: y = ","post":"","answer":-3,"hint":"Negative 2, minus 1."},
  {"pre":"Check (3, 2) in the circle: 3² + 2² = ","post":"","answer":13,"done":"It equals 13, so (3, 2) is right and (−2, −3) checks the same way.","hint":"9 + 4."},
], [sf_misc("x^2 - x - 6", facs_latex(3,-2), 3,-2),
    {"pattern":"square_bracket_error","expect":None,
     "message":"Expand \\((x - 1)^2\\) in full as \\(x^2 - 2x + 1\\); do not write \\(x^2 - 1\\), or the middle term is lost."}], HINT_CIRCLE)

# G3 y=x+2 ; x^2+y^2=20 -> x^2+2x-8 roots 2,-4
verify_circle(1,2,20,2,-4)
G3 = prob("Solve \\(y = x + 2\\) and \\(x^2 + y^2 = 20\\). Give the two x-values.", [2,-4], [
  {"say":"Substitute \\(y = x + 2\\) into the circle: \\(x^2 + (x + 2)^2 = 20\\). Expand \\((x + 2)^2 = x^2 + 4x + 4\\).",
   "pre":"The middle term, 2 × x × 2, is ","post":"x","answer":4,"hint":"2 times 2 is 4."},
  {"say":"So \\(x^2 + x^2 + 4x + 4 = 20\\).","pre":"Collect the two x² terms: 1 + 1 = ","post":"x²","answer":2,"hint":"One x² from each part."},
  {"say":"That gives \\(2x^2 + 4x + 4 = 20\\). Take 20 across.","pre":"The constant, 4 − 20, becomes ","post":"","answer":-16,"hint":"4 minus 20 is negative 16."},
  {"say":"So \\(2x^2 + 4x - 16 = 0\\). Divide by 2 to get \\(x^2 + 2x - 8 = 0\\), which factorises as \\((x - 2)(x + 4) = 0\\).",
   "phase":"substitute","pre":"First root, x = ","post":"","answer":2,"hint":"Set x − 2 = 0."},
  {"pre":"Second root, x = ","post":"","answer":-4,"hint":"Set x + 4 = 0."},
  {"say":"Each x gets its y from \\(y = x + 2\\).","pre":"At x = 2: y = ","post":"","answer":4,"hint":"2 + 2."},
  {"pre":"At x = −4: y = ","post":"","answer":-2,"hint":"Negative 4, plus 2."},
  {"pre":"Check (2, 4) in the circle: 2² + 4² = ","post":"","answer":20,"done":"It equals 20, so (2, 4) is right and (−4, −2) checks the same way.","hint":"4 + 16."},
], [sf_misc("x^2 + 2x - 8", facs_latex(2,-4), 2,-4),
    {"pattern":"square_bracket_error","expect":None,
     "message":"Expand \\((x + 2)^2\\) in full as \\(x^2 + 4x + 4\\); do not write \\(x^2 + 4\\), or the middle term 4x is lost."}], HINT_CIRCLE)

# G4 x+y=5 ; x^2-y=7 -> y=5-x -> x^2+x-12 roots 3,-4
for r in (3,-4):
    y=5-r
    assert approx(r+y,5) and approx(r*r - y,7)
G4 = prob("Solve \\(x + y = 5\\) and \\(x^2 - y = 7\\). Give the two x-values.", [3,-4], [
  {"say":"Rearrange the line: \\(x + y = 5\\) becomes \\(y = 5 - x\\). Substitute into \\(x^2 - y = 7\\): \\(x^2 - (5 - x) = 7\\). Removing the bracket gives \\(x^2 - 5 + x = 7\\).",
   "pre":"Bring −5 and −7 together for the constant: ","post":"","answer":-12,"hint":"Negative 5 from the bracket, and negative 7 from moving 7 across."},
  {"say":"So \\(x^2 + x - 12 = 0\\). Two numbers multiply to \\(-12\\) and add to \\(+1\\): they are \\(+4\\) and \\(-3\\), giving \\((x + 4)(x - 3) = 0\\).",
   "phase":"substitute","pre":"First root, x = ","post":"","answer":3,"hint":"Set x − 3 = 0."},
  {"pre":"Second root, x = ","post":"","answer":-4,"hint":"Set x + 4 = 0."},
  {"say":"Each x gets its y from \\(y = 5 - x\\).","pre":"At x = 3: y = ","post":"","answer":2,"hint":"5 − 3."},
  {"pre":"At x = −4: y = ","post":"","answer":9,"hint":"5 minus negative 4 is 5 + 4."},
  {"say":"Check the first pair in the second equation.","pre":"Put x = 3, y = 2 into x² − y: 3² − 2 = ","post":"","answer":7,
   "done":"It equals 7, so (3, 2) is right and (−4, 9) checks the same way.","hint":"9 − 2."},
], [sf_misc("x^2 + x - 12", facs_latex(3,-4), 3,-4)],
   "Make y the subject of the linear equation, substitute into x² − y = 7, then solve the quadratic.")

gold = [G0, G1, G2, G3, G4]

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
   "title": "Bronze: substitute, factorise, two answers",
   "steps": [
     "Both equations are written as <strong>y = …</strong>, so set the two right-hand sides equal to each other.",
     "Move every term to one side to get a quadratic equal to zero, then factorise it.",
     "Each bracket gives one x-value. Put each x back into the linear equation to find its y."
   ],
   "example": {
     "question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 1\\)",
     "steps": [
       {"label":"Set equal","content":"<p>\\(x + 1 = x^2 - 1\\)</p>"},
       {"label":"Rearrange","content":"<p>\\(x^2 - x - 2 = 0\\)</p>"},
       {"label":"Factorise","content":"<p>\\((x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\)</p>"},
       {"label":"Find y","content":"<p>\\(x = 2: y = 3\\). \\(x = -1: y = 0\\).</p>"},
       {"label":"Check","content":"<p>\\(x = 2\\) in \\(y = x^2 - 1\\): \\(4 - 1 = 3\\) ✓</p>"},
       {"label":"Answer","content":"<p>\\(x = 2, y = 3\\) and \\(x = -1, y = 0\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "silver": {
   "title": "Silver: rearrange with care, then solve",
   "steps": [
     "The linear part may be \\(y = 2x - 3\\) or \\(x + y = 4\\); rearrange it to \\(y = …\\) first if needed.",
     "After substituting, gather x-terms and numbers from <strong>both</strong> sides before you factorise.",
     "Watch every sign as terms cross the equals sign; one slip changes the whole quadratic."
   ],
   "example": {
     "question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 4x + 5\\)",
     "steps": [
       {"label":"Set equal","content":"<p>\\(x + 1 = x^2 - 4x + 5\\)</p>"},
       {"label":"Rearrange","content":"<p>\\(x^2 - 5x + 4 = 0\\)</p>"},
       {"label":"Factorise","content":"<p>\\((x - 1)(x - 4) = 0\\), so \\(x = 1\\) or \\(x = 4\\)</p>"},
       {"label":"Find y","content":"<p>\\(x = 1: y = 2\\). \\(x = 4: y = 5\\).</p>"},
       {"label":"Check","content":"<p>\\(x = 4\\) in \\(y = x^2 - 4x + 5\\): \\(16 - 16 + 5 = 5\\) ✓</p>"},
       {"label":"Answer","content":"<p>\\(x = 1, y = 2\\) and \\(x = 4, y = 5\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "gold": {
   "title": "Gold: circles and the quadratic formula",
   "steps": [
     "For a circle \\(x^2 + y^2 = r^2\\), rearrange the line to \\(y = …\\) and substitute, squaring the bracket in full.",
     "\\((a - x)^2 = a^2 - 2ax + x^2\\): never square the two terms separately.",
     "If the quadratic will not factorise, use the formula and round the two x-values as asked."
   ],
   "example": {
     "question": "Solve \\(x + y = 7\\) and \\(x^2 + y^2 = 29\\)",
     "steps": [
       {"label":"Rearrange line","content":"<p>\\(y = 7 - x\\)</p>"},
       {"label":"Substitute","content":"<p>\\(x^2 + (7 - x)^2 = 29\\) → \\(2x^2 - 14x + 20 = 0\\)</p>"},
       {"label":"Simplify and factorise","content":"<p>\\(x^2 - 7x + 10 = 0\\) → \\((x - 2)(x - 5) = 0\\), so \\(x = 2\\) or \\(x = 5\\)</p>"},
       {"label":"Find y","content":"<p>\\(x = 2: y = 5\\). \\(x = 5: y = 2\\).</p>"},
       {"label":"Check","content":"<p>\\((2, 5)\\): \\(4 + 25 = 29\\) ✓</p>"},
       {"label":"Answer","content":"<p>\\(x = 2, y = 5\\) and \\(x = 5, y = 2\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 }
}
# verify tier_guide examples
assert approx(2*2, 2+1+1)  # bronze x=2: x^2-1=3, x+1=3
for r in (2,5):  # gold example circle 29 with y=7-x
    y=7-r; assert approx(r*r+y*y,29)
for r in (1,4):  # silver example
    y=r+1; assert approx(y, r*r-4*r+5)

# ---------- guided (opener + teach) ----------
guided = {
 "opener": {
   "label": "Before any algebra",
   "display": "I square my number and get 6 more than the number itself.",
   "steps": [
     {"say":"A guess-the-number puzzle, no algebra needed. I am thinking of a number. When I square it, I get 6 more than the number I started with.",
      "pre":"One number that works is ","post":"","answer":3,
      "hint":"Try 3: three squared is 9, and 9 is 6 more than 3."},
     {"say":"Good. There is a second number that also works, and it is negative.",
      "pre":"The other number is ","post":"","answer":-2,
      "hint":"Try −2: negative two squared is 4, and 4 is 6 more than −2."},
     {"say":"You just solved \\(x^2 = x + 6\\) and found BOTH answers, \\(x = 3\\) and \\(x = -2\\). That is the whole topic: an equation with a square in it usually has TWO answers. In algebra it appears as a line \\(y = x + 6\\) crossing a curve \\(y = x^2\\); they meet at two points, so there are two x-values to find."}
   ]
 },
 "teach": {
   "bronze": {
     "display": "Solve \\(y = x + 2\\) and \\(y = x^2\\)",
     "label": "Together: your first one",
     "steps": [
       {"say":"Both equations give y, so set them equal: \\(x + 2 = x^2\\). Bring every term to the right so \\(x^2\\) stays positive.",
        "pre":"The x-term becomes ","post":"x","answer":-1,"hint":"The line's +x moves across to become −x."},
       {"pre":"and the constant becomes ","post":"","answer":-2,"hint":"The +2 moves across to become −2."},
       {"say":"So \\(x^2 - x - 2 = 0\\). Two numbers multiply to \\(-2\\) and add to \\(-1\\): they are \\(-2\\) and \\(+1\\), giving \\((x - 2)(x + 1) = 0\\).",
        "pre":"First root, x = ","post":"","answer":2,"hint":"Set x − 2 = 0."},
       {"pre":"Second root, x = ","post":"","answer":-1,"hint":"Set x + 1 = 0."},
       {"say":"Now each x gets its y from \\(y = x + 2\\).","phase":"substitute",
        "pre":"At x = 2: y = ","post":"","answer":4,"hint":"2 + 2."},
       {"pre":"At x = −1: y = ","post":"","answer":1,"hint":"Negative 1, plus 2."},
       {"pre":"Check x = 2 in the curve: 2² = ","post":"","answer":4,
        "done":"It equals y = 4, so (2, 4) is right and (−1, 1) checks the same way.","hint":"2 squared."}
     ]
   },
   "silver": {
     "display": "Solve \\(y = 2x - 1\\) and \\(y = x^2 - 3x + 5\\)",
     "label": "Together: the silver move",
     "steps": [
       {"say":"Set the two right sides equal: \\(2x - 1 = x^2 - 3x + 5\\). There are x-terms and numbers on both sides, so move everything to the right with care.",
        "pre":"Collect the x-terms, −3x − 2x = ","post":"x","answer":-5,"hint":"Negative 3 minus 2 is negative 5."},
       {"pre":"Collect the constants, 5 + 1 = ","post":"","answer":6,"hint":"The −1 moves across to become +1, so 5 + 1."},
       {"say":"So \\(x^2 - 5x + 6 = 0\\). Two numbers multiply to 6 and add to \\(-5\\): they are \\(-2\\) and \\(-3\\), giving \\((x - 2)(x - 3) = 0\\).",
        "pre":"First root, x = ","post":"","answer":2,"hint":"Set x − 2 = 0."},
       {"pre":"Second root, x = ","post":"","answer":3,"hint":"Set x − 3 = 0."},
       {"say":"Now each x gets its y from \\(y = 2x - 1\\).","phase":"substitute",
        "pre":"At x = 2: y = ","post":"","answer":3,"hint":"2 times 2, minus 1."},
       {"pre":"At x = 3: y = ","post":"","answer":5,"hint":"2 times 3, minus 1."},
       {"pre":"Check x = 3 in the curve: 3² − 3×3 + 5 = ","post":"","answer":5,
        "done":"It equals y = 5, so (3, 5) is right and (2, 3) checks the same way.","hint":"9 − 9 + 5."}
     ]
   },
   "gold": {
     "display": "Solve \\(x + y = 5\\) and \\(x^2 + y^2 = 13\\)",
     "label": "Together: the gold move",
     "steps": [
       {"say":"The second equation is a circle. Rearrange the line: \\(x + y = 5\\) becomes \\(y = 5 - x\\). Substitute into \\(x^2 + y^2 = 13\\): \\(x^2 + (5 - x)^2 = 13\\). Expand \\((5 - x)^2 = 25 - 10x + x^2\\).",
        "pre":"The middle term, 2 × 5 × (−1), is ","post":"x","answer":-10,"hint":"2 times 5 is 10, and it is negative."},
       {"say":"So \\(x^2 + 25 - 10x + x^2 = 13\\).","pre":"Collect the two x² terms: 1 + 1 = ","post":"x²","answer":2,"hint":"One x² from each part."},
       {"say":"That gives \\(2x^2 - 10x + 25 = 13\\). Take 13 across.","pre":"The constant, 25 − 13, becomes ","post":"","answer":12,"hint":"25 minus 13."},
       {"say":"So \\(2x^2 - 10x + 12 = 0\\). Divide every term by 2.","pre":"The x-term, −10 ÷ 2, becomes ","post":"x","answer":-5,"hint":"Half of negative 10."},
       {"say":"That leaves \\(x^2 - 5x + 6 = 0\\), which factorises as \\((x - 2)(x - 3) = 0\\).","phase":"substitute",
        "pre":"First root, x = ","post":"","answer":2,"hint":"Set x − 2 = 0."},
       {"pre":"Second root, x = ","post":"","answer":3,"hint":"Set x − 3 = 0."},
       {"say":"Each x gets its y from \\(y = 5 - x\\).","pre":"At x = 2: y = ","post":"","answer":3,"hint":"5 − 2."},
       {"pre":"At x = 3: y = ","post":"","answer":2,"hint":"5 − 3."},
       {"pre":"Check (2, 3) in the circle: 2² + 3² = ","post":"","answer":13,
        "done":"It equals 13, so (2, 3) is right and (3, 2) checks the same way.","hint":"4 + 9."}
     ]
   }
 }
}

# ---------- method_card ----------
method_card = {
 "title": "Simultaneous Equations (One Linear, One Quadratic)",
 "steps": [
   "Rearrange the linear equation to make one letter the subject.",
   "Substitute it into the quadratic, expanding any bracket in full.",
   "Rearrange to a quadratic equal to zero, then factorise or use the formula.",
   "Substitute each x back into the linear equation for its y, and give both pairs."
 ],
 "content": "<p>When one equation is a straight line and the other is a curve (a quadratic, or a circle \\(x^2 + y^2 = r^2\\)), use <strong>substitution</strong>. The line usually crosses the curve at two points, so expect two pairs of answers.</p><p>Make a letter the subject of the line, substitute it in, and simplify to a quadratic equal to zero. Solve it, then find each matching value from the line. Always give answers as pairs.</p>",
 "example": "<p><strong>Solve</strong> \\(y = x + 1\\) and \\(y = x^2 - 1\\)</p><p>\\(x + 1 = x^2 - 1 \\Rightarrow x^2 - x - 2 = 0 \\Rightarrow (x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\). Then \\(y = 3\\) or \\(y = 0\\): the pairs are \\((2, 3)\\) and \\((-1, 0)\\).</p>"
}

# ---------- fetch live, preserve, de-em-dash worked_examples ----------
key = os.environ['SUPABASE_SERVICE_KEY']
url = 'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.ddb5e897-f8ce-4c64-961a-7d6095d41a7c&select=practice_data'
req = urllib.request.Request(url, headers={'apikey':key,'Authorization':'Bearer '+key})
live = json.load(urllib.request.urlopen(req))[0]['practice_data']

we = json.loads(json.dumps(live.get('worked_examples')))  # deep copy
for ex in we:
    for st in ex.get('steps', []):
        if 'label' in st and '—' in st['label']:
            st['label'] = st['label'].replace(' — ', ': ').replace('—', ':')

pd = {
 "method_card": method_card,
 "topic_links": live.get('topic_links'),
 "problem_bank": {
   "gold": gold, "bronze": bronze, "silver": silver,
   "gold_description": "Circles \\(x^2 + y^2\\), or a quadratic that needs the formula",
   "bronze_description": "Both equations are y = …; simple substitution and easy factorising",
   "silver_description": "Careful rearrangement after substitution before factorising"
 },
 "related_videos": live.get('related_videos'),
 "worked_examples": we,
 "tier_guides": tier_guides,
 "guided": guided
}

out = "C:\\Users\\tshau\\Documents\\Study Vault\\.claude\\worktrees\\sandbox\\scratchpad\\_maths_guided\\lesson_algebra-L10.json"
io.open(out, 'w', encoding='utf-8').write(json.dumps(pd, ensure_ascii=False, indent=1))
print("WROTE", out)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
# quick em-dash scan
blob = json.dumps(pd, ensure_ascii=False)
print("em dashes in full blob:", blob.count('—'))
