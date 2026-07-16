# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for algebra-L08 (Quadratic Formula &
Completing the Square). Every box value is computed and asserted here."""
import json, io, math

MINUS = "−"  # unicode minus
def um(x):
    return str(x).replace("-", MINUS)
def par(x):
    s = um(x)
    return "(%s)" % s if (isinstance(x, (int, float)) and x < 0) else s

live = json.load(io.open("_live_L08.json", encoding="utf-8"))

# ---------- generators ----------
def formula_integer(a, b, c, sols, signb_expect):
    """Bronze: quadratic formula, perfect-square discriminant, a=1."""
    bb = b * b
    fourac = 4 * a * c
    disc = bb - fourac
    sq = int(round(math.sqrt(disc)))
    assert sq * sq == disc, (a, b, c, disc)
    negb = -b
    twoa = 2 * a
    rp = (negb + sq) / twoa
    rm = (negb - sq) / twoa
    assert [rp, rm] == [float(sols[0]), float(sols[1])], (a, b, c, rp, rm, sols)
    r = sols[0]
    chk = r * r + b * r + c
    assert chk == 0
    steps = [
        {"say": "Read off a = %d, b = %s, c = %s. The formula needs the discriminant b² − 4ac first."
                % (a, um(b), um(c))},
        {"pre": "b squared: %s × %s = " % (par(b), par(b)), "answer": bb,
         "hint": "Multiply b by itself."},
        {"pre": "4ac: 4 × %d × %s = " % (a, par(c)), "answer": fourac,
         "hint": "Multiply 4, then a, then c. Keep the sign of c."},
        {"pre": "discriminant b² − 4ac: %d − %s = " % (bb, par(fourac)), "answer": disc,
         "hint": "b squared minus 4ac. Taking away a negative adds on."},
        {"pre": "square root: √%d = " % disc, "answer": sq,
         "hint": "What number times itself gives %d?" % disc},
        {"say": "Now x = (−b ± √) ÷ 2a, with −b = %s and 2a = %d. Take the plus first:" % (um(negb), twoa),
         "phase": "substitute",
         "pre": "x = (%s + %d) ÷ %d = " % (um(negb), sq, twoa), "answer": int(rp) if rp == int(rp) else rp,
         "hint": "Work the bracket, then divide."},
        {"phase": "substitute",
         "pre": "then the minus: x = (%s − %d) ÷ %d = " % (um(negb), sq, twoa),
         "answer": int(rm) if rm == int(rm) else rm,
         "hint": "Bracket first, then divide."},
        {"phase": "substitute",
         "pre": "check x = %s: %s² + %s × %s + %s = " % (um(r), par(r), par(b), par(r), par(c)),
         "answer": 0, "done": "It gives 0, so both roots are right.",
         "hint": "Square it, then add the parts."},
    ]
    misc = [{
        "pattern": "sign_of_b", "check": "sign_of_b", "expect": signb_expect,
        "message": "The formula uses −b, not b. Here b = %s, so the top starts %s, giving x = %s and x = %s. Slipping in %s instead gives %s and %s, which fail the equation."
                   % (um(b), um(negb), um(sols[0]), um(sols[1]), um(b), um(signb_expect[0]), um(signb_expect[1])),
        "note": "Uses +b in place of -b in the numerator.",
    }]
    return steps, misc


def formula_decimal(a, b, c, sols, sqdisp, extra_misc):
    """Silver/Gold: quadratic formula, decimal roots to 2 d.p."""
    bb = b * b
    fourac = 4 * a * c
    disc = bb - fourac
    negb = -b
    twoa = 2 * a
    rp = round((negb + math.sqrt(disc)) / twoa, 2)
    rm = round((negb - math.sqrt(disc)) / twoa, 2)
    assert [rp, rm] == [sols[0], sols[1]], (a, b, c, rp, rm, sols)
    ssum = round(rp + rm, 2)
    nba = round(-b / a, 2)
    steps = [
        {"say": "Read off a = %d, b = %s, c = %s. Work out the discriminant b² − 4ac first."
                % (a, um(b), um(c))},
        {"pre": "b squared: %s × %s = " % (par(b), par(b)), "answer": bb, "hint": "Multiply b by itself."},
        {"pre": "4ac: 4 × %d × %s = " % (a, par(c)), "answer": fourac,
         "hint": "Multiply 4, then a, then c. Keep the sign of c."},
        {"pre": "discriminant b² − 4ac: %d − %s = " % (bb, par(fourac)), "answer": disc,
         "hint": "b squared minus 4ac."},
        {"say": "√%d ≈ %s on the calculator. Now x = (−b ± √) ÷ 2a, with −b = %s and 2a = %d. Plus first:"
                % (disc, sqdisp, um(negb), twoa),
         "phase": "substitute",
         "pre": "x = (%s + %s) ÷ %d = " % (um(negb), sqdisp, twoa), "answer": rp,
         "hint": "Do the bracket, then divide. Round to 2 d.p."},
        {"phase": "substitute",
         "pre": "then minus: x = (%s − %s) ÷ %d = " % (um(negb), sqdisp, twoa), "answer": rm,
         "hint": "Bracket first, then divide. Round to 2 d.p."},
        {"phase": "substitute",
         "pre": "add your two roots to check: %s + %s = " % (par(rp), par(rm)), "answer": ssum,
         "done": "The two roots must add to −b ÷ a = %s. They do, so the pair is right." % um(nba),
         "hint": "Just add your two answers."},
    ]
    return steps, list(extra_misc)


def complete_q(b, c, disp_sign_p, extra_misc, vertex=False):
    """Silver S2/S3/S6 and Gold G3: write in (x+p)^2+q form, state q."""
    assert b % 2 == 0
    p = b // 2
    p2 = p * p
    q = c - p2
    assert p2 + q == c
    sgn = "+" if p >= 0 else "−"
    absp = abs(p)
    steps = [
        {"say": "Write it as (x + p)² + q. Start by halving b."},
        {"pre": "halve b: %s ÷ 2 = " % par(b), "answer": p, "hint": "Halve the coefficient of x."},
        {"pre": "p squared: %s² = " % par(p), "answer": p2, "hint": "Square p."},
        {"say": "q is what is left after taking p² away from c.", "phase": "substitute",
         "pre": "q = c − p² = %s − %s = " % (par(c), par(p2)), "answer": q,
         "hint": "Subtract p squared from c."},
        {"phase": "substitute",
         "pre": "check by rebuilding c: p² + q = %s + %s = " % (par(p2), par(q)), "answer": c,
         "done": ("It rebuilds c = %d and the turning point is (%s, %s), so q = %s is right."
                  % (c, um(-p), um(q), um(q))) if vertex else
                 ("It rebuilds c = %d, so q = %s is right." % (c, um(q))),
         "hint": "p squared plus q should give back c."},
    ]
    return steps, list(extra_misc)


def complete_solve(b, c, stored, want, rhsdisp, other, extra_misc):
    """Gold G0/G4: complete the square then solve (decimal single root)."""
    p = b / 2
    pi = int(p)
    assert p == pi
    p2 = pi * pi
    q = c - p2
    rhs = -q
    negp = -pi
    sgn = "+" if pi >= 0 else "−"
    absp = abs(pi)
    sq = math.sqrt(rhs)
    if want == "smaller":
        wroot = round(negp - sq, 2); oroot = round(negp + sq, 2); op1 = "−"; op2 = "+"
    else:  # positive
        wroot = round(negp + sq, 2); oroot = round(negp - sq, 2); op1 = "+"; op2 = "−"
    assert wroot == stored, (b, c, wroot, stored)
    assert round(oroot, 2) == other, (b, c, oroot, other)
    prod = round(wroot * oroot)
    label = "smaller" if want == "smaller" else "positive"
    steps = [
        {"say": "a = 1, so complete the square. Halve b first."},
        {"pre": "halve b: %s ÷ 2 = " % par(b), "answer": pi, "hint": "Halve the coefficient of x."},
        {"pre": "p squared: %s² = " % par(pi), "answer": p2, "hint": "Square p."},
        {"pre": "the constant: c − p² = %s − %s = " % (par(c), par(p2)), "answer": q,
         "hint": "Subtract p squared from c."},
        {"say": "So (x %s %d)² + %s = 0. Move %s across to the right:" % (sgn, absp, par(q), um(q)),
         "phase": "substitute",
         "pre": "(x %s %d)² = " % (sgn, absp), "answer": rhs, "hint": "Add %s to both sides." % um(rhs)},
        {"phase": "substitute",
         "pre": "%s root: %s %s √%d = %s %s %s = " % (label, par(negp), op1, rhs, par(negp), op1, rhsdisp),
         "answer": stored, "hint": "Take the square root, then round to 2 d.p."},
        {"phase": "substitute",
         "pre": "the other root: %s %s √%d = " % (par(negp), op2, rhs), "answer": other,
         "done": "Product %s × %s ≈ %s = c, so both roots are right." % (um(stored), um(other), um(prod)),
         "hint": "Use the opposite sign."},
    ]
    return steps, list(extra_misc)

# ---------- BRONZE bank ----------
bronze_specs = [
    (1, 3, -10, [2, -5], [5, -2]),
    (1, -5, 6, [3, 2], [-2, -3]),
    (1, 1, -12, [3, -4], [4, -3]),
    (1, -7, 10, [5, 2], [-2, -5]),
    (1, 5, -6, [1, -6], [6, -1]),   # replaced x^2+2x-8 (b2_error degenerate)
    (1, -4, -5, [5, -1], [1, -5]),
    (1, 6, 5, [-1, -5], [5, 1]),
    (1, -2, -3, [3, -1], [1, -3]),
]
bronze = []
for a, b, c, sols, se in bronze_specs:
    gs, misc = formula_integer(a, b, c, sols, se)
    bronze.append({
        "display": "Solve \\(x^2 %s %s = 0\\) using the quadratic formula"
                   % ("+ %dx" % b if b > 0 else ("- %dx" % (-b)),
                      "+ %d" % c if c > 0 else "- %d" % (-c)),
        "solutions": sols, "calculator": False, "input_type": "two_solutions",
        "hint": "Find the discriminant b² − 4ac, square root it, then use x = (−b ± √) ÷ 2.",
        "misconceptions": misc, "guided_steps": gs,
    })

# ---------- SILVER bank ----------
silver = []
# S0 x^2+4x+1
gs, m = formula_decimal(1, 4, 1, [-0.27, -3.73], "3.464", [
    {"pattern": "discriminant", "check": "b2_error", "expect": [-1, -3],
     "message": "It is b², not 2b. Here b = 4, so b² = 16, not 8. Using 2b makes the discriminant 4, giving the wrong pair −1 and −3.",
     "note": "2b=8; disc 8-4=4; roots -1,-3."},
    {"pattern": "formula_sign", "check": "sign_of_b", "expect": [3.73, 0.27],
     "message": "The formula uses −b. Here b = 4, so −b = −4. Slipping in +4 gives 3.73 and 0.27, the wrong signs.",
     "note": "uses +b."}])
silver.append({"display": "Solve \\(x^2 + 4x + 1 = 0\\), give answers to 2 d.p.",
               "solutions": [-0.27, -3.73], "calculator": True, "input_type": "two_solutions",
               "hint": "Use the quadratic formula and round each root to 2 d.p.",
               "misconceptions": m, "guided_steps": gs})
# S1 2x^2+3x-4
gs, m = formula_decimal(2, 3, -4, [0.85, -2.35], "6.403", [
    {"pattern": "formula_sign", "check": "sign_of_b", "expect": [2.35, -0.85],
     "message": "The formula uses −b. Here b = 3, so −b = −3. Slipping in +3 gives 2.35 and −0.85.",
     "note": "uses +b."}])
silver.append({"display": "Solve \\(2x^2 + 3x - 4 = 0\\), give answers to 2 d.p.",
               "solutions": [0.85, -2.35], "calculator": True, "input_type": "two_solutions",
               "hint": "Use the quadratic formula with a = 2, and round each root to 2 d.p.",
               "misconceptions": m, "guided_steps": gs})
# S2 x^2+10x+7 state q
gs, m = complete_q(10, 7, "+", [
    {"pattern": "forgot_subtract", "check": "forgot_subtract", "expect": 7,
     "message": "After halving b you still owe the −p². Stopping at q = c = 7 misses it; the correct q is −18.",
     "note": "q=c error."},
    {"pattern": "completing_halve", "check": "half_b", "expect": -93,
     "message": "Halve b before squaring. Using p = 10 instead of 5 gives q = 7 − 100 = −93.",
     "note": "uses b not b/2."}])
silver.append({"display": "Write \\(x^2 + 10x + 7\\) in the form \\((x+p)^2+q\\). State the value of \\(q\\).",
               "solutions": [-18], "calculator": False, "input_type": "single_value",
               "hint": "Halve the coefficient of x to get p, then q = c − p².",
               "misconceptions": m, "guided_steps": gs})
# S3 x^2-4x+1 state q
gs, m = complete_q(-4, 1, "−", [
    {"pattern": "forgot_subtract", "check": "forgot_subtract", "expect": 1,
     "message": "After halving b you still owe the −p². Stopping at q = c = 1 misses it; the correct q is −3.",
     "note": "q=c error."},
    {"pattern": "completing_halve", "check": "half_b", "expect": -15,
     "message": "Halve b before squaring. Using p = −4 instead of −2 gives q = 1 − 16 = −15.",
     "note": "uses b not b/2."}])
silver.append({"display": "Write \\(x^2 - 4x + 1\\) in the form \\((x+p)^2+q\\). State the value of \\(q\\).",
               "solutions": [-3], "calculator": False, "input_type": "single_value",
               "hint": "Halve the coefficient of x to get p, then q = c − p².",
               "misconceptions": m, "guided_steps": gs})
# S4 3x^2-2x-4
gs, m = formula_decimal(3, -2, -4, [1.54, -0.87], "7.211", [
    {"pattern": "formula_sign", "check": "sign_of_b", "expect": [0.87, -1.54],
     "message": "The formula uses −b. Here b = −2, so −b = 2. Slipping in −2 gives 0.87 and −1.54.",
     "note": "uses +b."}])
silver.append({"display": "Solve \\(3x^2 - 2x - 4 = 0\\), give answers to 2 d.p.",
               "solutions": [1.54, -0.87], "calculator": True, "input_type": "two_solutions",
               "hint": "Use the quadratic formula with a = 3, and round each root to 2 d.p.",
               "misconceptions": m, "guided_steps": gs})
# S5 discriminant value (reworded, ambiguity fix)
gs_s5 = [
    {"say": "Read off a = 1, b = 3, c = 5. The discriminant is b² − 4ac."},
    {"pre": "b squared: 3 × 3 = ", "answer": 9, "hint": "Multiply b by itself."},
    {"pre": "4ac: 4 × 1 × 5 = ", "answer": 20, "hint": "Multiply 4, a and c."},
    {"say": "Now subtract.", "phase": "substitute",
     "pre": "discriminant: 9 − 20 = ", "answer": -11, "hint": "b squared minus 4ac."},
    {"phase": "substitute",
     "pre": "a negative discriminant means the number of real solutions is ", "answer": 0,
     "done": "−11 is below 0, so there are no real solutions. The discriminant is −11.",
     "hint": "Below 0 means the curve never crosses the x-axis."},
]
m_s5 = [{"pattern": "discriminant", "check": "b2_error", "expect": -14,
         "message": "It is b², not 2b. Here b = 3, so b² = 9. Using 2b = 6 gives 6 − 20 = −14, not −11.",
         "note": "2b error."}]
silver.append({"display": "Find the discriminant of \\(x^2 + 3x + 5 = 0\\). Enter the discriminant value.",
               "solutions": [-11], "calculator": False, "input_type": "single_value",
               "hint": "Work out b² − 4ac. A negative value means no real solutions.",
               "misconceptions": m_s5, "guided_steps": gs_s5})
# S6 x^2+6x+1 state q  (was x^2+6x-2 -> q=-11 clashed with S5; changed to +1 -> q=-8)
gs, m = complete_q(6, 1, "+", [
    {"pattern": "forgot_subtract", "check": "forgot_subtract", "expect": 1,
     "message": "After halving b you still owe the −p². Stopping at q = c = 1 misses it; the correct q is −8.",
     "note": "q=c error."},
    {"pattern": "completing_halve", "check": "half_b", "expect": -35,
     "message": "Halve b before squaring. Using p = 6 instead of 3 gives q = 1 − 36 = −35.",
     "note": "uses b not b/2."}])
silver.append({"display": "Write \\(x^2 + 6x + 1\\) in completed square form. State the value of \\(q\\).",
               "solutions": [-8], "calculator": False, "input_type": "single_value",
               "hint": "Halve the coefficient of x to get p, then q = c − p².",
               "misconceptions": m, "guided_steps": gs})

# ---------- GOLD bank ----------
gold = []
# G0 x^2-8x+5 smaller root
gs, m = complete_solve(-8, 5, 0.68, "smaller", "3.317", 7.32, [
    {"pattern": "completing_halve", "check": "half_b", "expect": 0.32,
     "message": "Halve b before squaring. Using p = 8 instead of 4 gives (x − 8)² = 59 and a smaller root of 0.32.",
     "note": "uses b not b/2."}])
gold.append({"display": "Solve \\(x^2 - 8x + 5 = 0\\) by completing the square. Give the smaller root to 2 d.p.",
             "solutions": [0.68], "calculator": True, "input_type": "single_value",
             "hint": "Complete the square, rearrange to (x + p)² = k, then take the smaller root.",
             "misconceptions": m, "guided_steps": gs})
# G1 values of k
gs_g1 = [
    {"say": "Two distinct solutions means the discriminant is greater than 0. Here a = 1, b = 6, c = k."},
    {"pre": "b squared: 6 × 6 = ", "answer": 36, "hint": "Multiply b by itself."},
    {"say": "So b² − 4ac = 36 − 4k, and we need 36 − 4k > 0, so 4k < 36.",
     "pre": "the boundary: 36 ÷ 4 = ", "answer": 9, "hint": "Divide 36 by 4."},
    {"say": "So k < 9, strictly, because two DISTINCT roots need the discriminant above 0, not equal to it.",
     "phase": "substitute",
     "pre": "largest integer that is less than 9 = ", "answer": 8, "hint": "The whole number just below 9."},
    {"phase": "substitute",
     "pre": "check k = 8: 36 − 4 × 8 = ", "answer": 4,
     "done": "4 is above 0, so two solutions. k = 9 would give 0 (a repeated root), so 8 is the largest.",
     "hint": "Work out 36 − 32."},
]
m_g1 = [
    {"pattern": "discriminant", "check": "b2_error", "expect": 2,
     "message": "It is b², not 2b. Here b = 6, so b² = 36. Using 2b = 12 gives 12 − 4k > 0, so k < 3 and a wrong answer of 2.",
     "note": "2b error."},
    {"pattern": "disc_boundary", "check": "strict_vs_equal", "expect": 9,
     "message": "Two DISTINCT solutions need the discriminant above 0, not equal to it. Allowing 36 − 4k = 0 lets k = 9, but that is a repeated root: one solution, not two.",
     "note": "uses >= instead of >."},
]
gold.append({"display": "For what values of \\(k\\) does \\(x^2 + 6x + k = 0\\) have two distinct solutions? State the largest integer \\(k\\).",
             "solutions": [8], "calculator": False, "input_type": "single_value",
             "hint": "Two distinct roots need b² − 4ac > 0. Solve the inequality for k.",
             "misconceptions": m_g1, "guided_steps": gs_g1})
# G2 2x^2-12x+7  (audit-fixed solutions already [5.35,0.65])
gs, m = formula_decimal(2, -12, 7, [5.35, 0.65], "9.381", [
    {"pattern": "formula_sign", "check": "sign_of_b", "expect": [-0.65, -5.35],
     "message": "The formula uses −b. Here b = −12, so −b = 12. Slipping in −12 gives −0.65 and −5.35, the negatives of the real roots.",
     "note": "uses +b."},
    {"pattern": "wrong_2a", "check": "divide_by_2", "expect": [10.69, 1.31],
     "message": "Divide by 2a, not 2. Here 2a = 4. Dividing by 2 gives 10.69 and 1.31, which are twice too big.",
     "note": "forgets a in 2a."}])
gold.append({"display": "Solve \\(2x^2 - 12x + 7 = 0\\), give answers to 2 d.p.",
             "solutions": [5.35, 0.65], "calculator": True, "input_type": "two_solutions",
             "hint": "Use the quadratic formula with a = 2, and round each root to 2 d.p.",
             "misconceptions": m, "guided_steps": gs})
# G3 vertex q
gs, m = complete_q(4, 9, "+", [
    {"pattern": "forgot_subtract", "check": "forgot_subtract", "expect": 9,
     "message": "The turning point height is q = c − p², not c. Stopping at q = 9 misses the −p²; the correct q is 5.",
     "note": "q=c error."},
    {"pattern": "completing_halve", "check": "half_b", "expect": -7,
     "message": "Halve b before squaring. Using p = 4 instead of 2 gives q = 9 − 16 = −7.",
     "note": "uses b not b/2."}], vertex=True)
gold.append({"display": "The turning point of \\(y = x^2 + 4x + 9\\) is \\((-p, q)\\). Find \\(q\\).",
             "solutions": [5], "calculator": False, "input_type": "single_value",
             "hint": "Complete the square; the vertex of (x + p)² + q is at (−p, q).",
             "misconceptions": m, "guided_steps": gs})
# G4 x^2+2x-7 positive root
gs, m = complete_solve(2, -7, 1.83, "positive", "2.828", -3.83, [
    {"pattern": "completing_halve", "check": "half_b", "expect": 1.32,
     "message": "Halve b before squaring. Using p = 2 instead of 1 gives (x + 2)² = 11 and a positive root of 1.32.",
     "note": "uses b not b/2."}])
gold.append({"display": "Solve \\(x^2 + 2x - 7 = 0\\) by completing the square. Give the positive root to 2 d.p.",
             "solutions": [1.83], "calculator": True, "input_type": "single_value",
             "hint": "Complete the square, rearrange to (x + p)² = k, then take the positive root.",
             "misconceptions": m, "guided_steps": gs})

# ---------- guided.opener ----------
opener = {
    "label": "Before any algebra",
    "display": "A square patch of grass has an area of <strong>49 m²</strong>.",
    "steps": [
        {"say": "No algebra yet. Picture the square lawn.",
         "pre": "How long is each side, in metres? ", "answer": 7,
         "hint": "What number times itself gives 49?"},
        {"say": "You just took a square root: the side is √49 = 7. That one move finishes every completing-the-square question.",
         "pre": "A bigger square has side (x + 2) metres and the same area, 49 m². So the whole side (x + 2) is again ",
         "answer": 7, "hint": "Same area, so the same side length as before."},
        {"say": "So x + 2 = 7.",
         "pre": "Then x = ", "answer": 5, "hint": "Take 2 off both sides."},
        {"say": "That is completing the square in miniature. A hard quadratic like \\(x^2 + 4x - 45 = 0\\) is just rearranged into \\((x+2)^2 = 49\\), then square-rooted exactly like your lawn (giving x = 5 or x = −9). The quadratic formula is this same idea done once and for all."},
    ],
}
assert 5 ** 2 + 4 * 5 - 45 == 0            # x^2+4x-45 at x=5
assert (5 + 2) ** 2 == 49                  # (x+2)^2 = 49 at x=5
assert (-9) ** 2 + 4 * (-9) - 45 == 0      # the other root x=-9

# ---------- guided.teach ----------
tb_gs, _ = formula_integer(1, 5, 4, [-1, -4], [4, 6])  # not in bank
teach_bronze = {"display": "Solve \\(x^2 + 5x + 4 = 0\\)", "label": "Together: your first one",
                "steps": tb_gs}
ts_gs, _ = formula_decimal(1, 2, -4, [1.24, -3.24], "4.472", [])
teach_silver = {"display": "Solve \\(x^2 + 2x - 4 = 0\\), give answers to 2 d.p.",
                "label": "Together: the decimal move", "steps": ts_gs}
tg_gs, _ = complete_solve(-6, 2, 5.65, "positive", "2.646", 0.35, [])
# complete_solve labels 'positive' root as -p+sqrt = 3+2.646=5.65; other 0.35
teach_gold = {"display": "Solve \\(x^2 - 6x + 2 = 0\\) by completing the square. Give both roots to 2 d.p.",
              "label": "Together: the gold move", "steps": tg_gs}

# strip phase tags from teach walks (not required, keep clean)
for w in (teach_bronze, teach_silver, teach_gold):
    for st in w["steps"]:
        st.pop("phase", None)

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: the quadratic formula with whole-number answers",
        "steps": [
            "Any quadratic \\(ax^2 + bx + c = 0\\) is solved by \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\).",
            "First work out the <strong>discriminant</strong> \\(b^2 - 4ac\\), then its square root. In bronze this is always a whole number.",
            "Put \\(-b\\), the root, and \\(2a\\) into the formula. The \\(\\pm\\) gives you the two answers.",
        ],
        "example": {
            "question": "Solve x² + 4x − 5 = 0 using the quadratic formula",
            "steps": [
                {"label": "a, b, c", "content": "<p>\\(a = 1\\), \\(b = 4\\), \\(c = -5\\)</p>"},
                {"label": "Discriminant", "content": "<p>\\(b^2 - 4ac = 16 + 20 = 36\\), and \\(\\sqrt{36} = 6\\).</p>"},
                {"label": "Substitute", "content": "<p>\\(x = \\frac{-4 \\pm 6}{2}\\)</p>"},
                {"label": "Check", "content": "<p>\\((1)^2 + 4(1) - 5 = 0\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x = 1\\) or \\(x = -5\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: decimals and completing the square",
        "steps": [
            "Same formula, but now the discriminant is not a perfect square, so the roots are decimals. Round each to 2 d.p.",
            "<strong>Completing the square</strong> rewrites \\(x^2 + bx + c\\) as \\((x + p)^2 + q\\): halve b to get p, then \\(q = c - p^2\\).",
            "A quick check: expanding \\((x + p)^2 + q\\) must rebuild the original constant c.",
        ],
        "example": {
            "question": "Write x² + 8x + 3 in the form (x + p)² + q",
            "steps": [
                {"label": "Halve b", "content": "<p>Half of 8 is 4, so \\(p = 4\\).</p>"},
                {"label": "Find q", "content": "<p>\\(q = c - p^2 = 3 - 16 = -13\\).</p>"},
                {"label": "Check", "content": "<p>\\((x+4)^2 - 13\\) expands to \\(x^2 + 8x + 3\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\((x + 4)^2 - 13\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: completing the square to solve, and the discriminant",
        "steps": [
            "Complete the square, then <strong>solve</strong>: rearrange \\((x + p)^2 + q = 0\\) to \\((x + p)^2 = -q\\) and square root both sides for \\(x = -p \\pm \\sqrt{-q}\\).",
            "The discriminant \\(b^2 - 4ac\\) tells you the number of roots: above 0 means two, exactly 0 means one repeated, below 0 means none.",
            "The vertex of \\((x + p)^2 + q\\) sits at \\((-p, q)\\), which is how completing the square finds turning points.",
        ],
        "example": {
            "question": "Solve x² − 6x + 4 = 0 by completing the square (exact answers)",
            "steps": [
                {"label": "Complete", "content": "<p>\\(x^2 - 6x + 4 = (x - 3)^2 - 9 + 4 = (x - 3)^2 - 5\\)</p>"},
                {"label": "Rearrange", "content": "<p>\\((x - 3)^2 = 5\\), so \\(x - 3 = \\pm\\sqrt{5}\\).</p>"},
                {"label": "Check", "content": "<p>\\((3+\\sqrt5)(3-\\sqrt5) = 9 - 5 = 4 = c\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x = 3 \\pm \\sqrt{5}\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- method_card (slim) ----------
method_card = {
    "title": "Quadratic Formula and Completing the Square",
    "steps": [
        "Quadratic formula: \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\). Work out \\(b^2 - 4ac\\) first.",
        "The discriminant \\(b^2 - 4ac\\): above 0 gives two roots, 0 gives one, below 0 gives none.",
        "Completing the square: halve b to get p, then \\(q = c - p^2\\), giving \\((x + p)^2 + q\\).",
        "To solve by completing the square, rearrange to \\((x + p)^2 = -q\\) and square root both sides.",
    ],
    "content": "<p>The <strong>quadratic formula</strong> solves any \\(ax^2 + bx + c = 0\\). The part under the root, \\(b^2 - 4ac\\), is the <strong>discriminant</strong> and counts the solutions.</p><p><strong>Completing the square</strong> rewrites \\(x^2 + bx + c\\) as \\((x + p)^2 + q\\) with \\(p = \\frac{b}{2}\\) and \\(q = c - p^2\\). It solves quadratics and locates the vertex at \\((-p, q)\\).</p>",
    "example": "<p><strong>Solve</strong> \\(x^2 + 6x + 2 = 0\\) (1 d.p.). \\(b^2 - 4ac = 36 - 8 = 28\\), \\(\\sqrt{28} = 5.29\\), so \\(x = \\frac{-6 \\pm 5.29}{2} = -0.4\\) or \\(-5.6\\).</p>",
}

# ---------- assemble ----------
pd = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": {
        "gold": gold, "bronze": bronze, "silver": silver,
        "gold_description": "Complete the square to solve, plus discriminant reasoning for the number of roots.",
        "bronze_description": "Quadratic formula when the discriminant is a perfect square (whole-number roots).",
        "silver_description": "Quadratic formula with decimal roots (2 d.p.), and completing the square to state q.",
    },
    "related_videos": live["related_videos"],
    "worked_examples": json.loads(
        json.dumps(live["worked_examples"], ensure_ascii=False)
        .replace(" — ", ": ").replace("—", ", ")),  # strip em dashes (style gate)
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold}},
}

# em-dash guard (student-facing)
def scan(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note",):
                continue
            scan(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            scan(v, "%s[%d]" % (path, i))
    elif isinstance(o, str) and "—" in o:
        raise SystemExit("EM DASH at " + path + ": " + o)
scan(pd)

json.dump(pd, io.open("lesson_algebra-L08.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK bronze=%d silver=%d gold=%d" % (len(bronze), len(silver), len(gold)))
