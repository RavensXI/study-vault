# -*- coding: utf-8 -*-
import json, io

M = "−"  # unicode minus

def num(x):
    # format a number for plain-text display with unicode minus
    if isinstance(x, float) and x == int(x):
        x = int(x)
    s = str(x)
    return s.replace("-", M)

def paren(root):
    return "(" + num(root) + ")"

def check_expr(root, b, c, a=1):
    # build plain-text "(root)^2 ... = " for a*x^2 + b*x + c
    lead = "" if a == 1 else num(a) + "×"
    s = lead + paren(root) + "²"
    if b:
        s += (" + " if b > 0 else " " + M + " ") + num(abs(b)) + "×" + paren(root)
    if c:
        s += (" + " if c > 0 else " " + M + " ") + num(abs(c))
    return s

def bsign(k):
    # "+ k" or "- k" for a bracket number k inside plain text
    return ("+ " + num(k)) if k >= 0 else (M + " " + num(abs(k)))

def latex_bracket(k):
    return ("+ " + str(k)) if k >= 0 else ("- " + str(abs(k)))

def a1_walk(disp, b, c, m, n):
    """Standard a=1: numbers m,n with m+n=b, m*n=c. roots=(-m,-n). m<=n."""
    lo, hi = (m, n) if m <= n else (n, m)
    r1, r2 = -lo, -hi
    dl = disp.replace("Solve ", "").strip()
    steps = [
        {"say": "Solve " + dl + " by finding two numbers that multiply to \\(" +
                str(c) + "\\) and add to \\(" + str(b) + "\\)."},
        {"pre": "The smaller of the two numbers is ", "post": "", "answer": lo,
         "hint": "List pairs that multiply to " + num(c) + "; take the pair that adds to " +
                 num(b) + ", then the smaller one."},
        {"pre": "The larger of the two numbers is ", "post": "", "answer": hi,
         "hint": "The two numbers add to " + num(b) + ", and the smaller was " + num(lo) + "."},
        {"say": "So it factorises to \\((x " + latex_bracket(lo) + ")(x " + latex_bracket(hi) +
                ") = 0\\). Each bracket can be zero."},
        {"phase": "substitute", "pre": "First bracket zero: x " + bsign(lo) + " = 0, so x = ",
         "post": "", "answer": r1,
         "hint": "Move " + num(lo) + " across; the sign flips."},
        {"phase": "substitute", "pre": "Second bracket zero: x " + bsign(hi) + " = 0, so x = ",
         "post": "", "answer": r2,
         "hint": "Move " + num(hi) + " across; the sign flips."},
        {"pre": "Check x = " + num(r1) + ": " + check_expr(r1, b, c) + " = ", "post": "",
         "answer": 0, "hint": "Work out the arithmetic; a correct root gives 0.",
         "done": "It gives 0, so x = " + num(r1) + " is right, and x = " + num(r2) +
                 " checks the same way."},
    ]
    return steps

def factor_pair_mis(expect):
    return {
        "pattern": "factor_pair_not_solved", "check": "negated", "expect": expect,
        "message": "Those are the numbers that go inside the brackets, not the answers. Set each "
                   "bracket to zero: the sign of each number flips as it crosses. The solutions are "
                   "the flipped values.",
        "note": "Reporting the raw in-bracket numbers (or forgetting the sign flip) lands on the "
                "negation of the roots."
    }

def one_correct_mis():
    return {
        "pattern": "one_correct", "check": "partial", "expect": None,
        "message": "One of your two answers is right, but the other is not. Recheck your number "
                   "pair: they must multiply to the constant AND add to the coefficient of x.",
        "note": "No single determinate wrong answer; fires only via the partial check."
    }

# ---------------------------------------------------------------------------
# Load live and start from it (preserve everything else)
live = json.load(io.open("_algL07ocr_live.json", encoding="utf-8"))
pd = live  # mutate in place; we add guided fields + repair gold[0]

pb = pd["problem_bank"]

# ---- descriptions ----
pb["bronze_description"] = ("Factorise a quadratic with a = 1 into two brackets, then set each "
                            "bracket to zero to find both solutions.")
pb["silver_description"] = ("Handle negatives, a difference of two squares, a common factor, or a "
                            "rearrange before factorising.")
pb["gold_description"] = ("Solve quadratics where x squared has a coefficient above 1, using the "
                          "split the middle term method.")

# =========================== BRONZE ========================================
bronze = pb["bronze"]
# b0 x^2+5x+6 -> m2 n3
bronze[0]["hint"] = "Two numbers multiply to 6 and add to 5, then flip their signs."
bronze[0]["misconceptions"] = [factor_pair_mis([2, 3]), one_correct_mis()]
bronze[0]["guided_steps"] = a1_walk(bronze[0]["display"], 5, 6, 2, 3)
# b1 x^2+3x+2 -> 1,2
bronze[1]["hint"] = "Two numbers multiply to 2 and add to 3, then flip their signs."
bronze[1]["misconceptions"] = [factor_pair_mis([1, 2]), one_correct_mis()]
bronze[1]["guided_steps"] = a1_walk(bronze[1]["display"], 3, 2, 1, 2)
# b2 x^2-7x+10 -> -2,-5 roots 2,5
bronze[2]["hint"] = "Two numbers multiply to 10 and add to -7, then flip their signs."
bronze[2]["misconceptions"] = [factor_pair_mis([-2, -5]), one_correct_mis()]
bronze[2]["guided_steps"] = a1_walk(bronze[2]["display"], -7, 10, -2, -5)
# b3 x^2+8x+15 -> 3,5
bronze[3]["hint"] = "Two numbers multiply to 15 and add to 8, then flip their signs."
bronze[3]["misconceptions"] = [factor_pair_mis([3, 5]), one_correct_mis()]
bronze[3]["guided_steps"] = a1_walk(bronze[3]["display"], 8, 15, 3, 5)
# b4 x^2-9 DOTS roots 3,-3
bronze[4]["hint"] = "There is no middle term, so it is a difference of two squares: split into (x + 3)(x - 3)."
bronze[4]["misconceptions"] = [one_correct_mis()]
bronze[4]["guided_steps"] = a1_walk(bronze[4]["display"], 0, -9, -3, 3)
# b5 x^2-4x common factor roots 0,4
bronze[5]["hint"] = "Both terms share an x; take it out, then set each factor to zero."
bronze[5]["misconceptions"] = [
    {"pattern": "factor_pair_not_solved", "check": "negated", "expect": [0, -4],
     "message": "The factor is x(x " + M + " 4). Set each to zero: x = 0, and x " + M +
                " 4 = 0 gives x = 4. The solutions are 0 and 4.",
     "note": "Not flipping the 4 gives 0 and -4."},
    one_correct_mis()]
bronze[5]["guided_steps"] = [
    {"say": "Solve \\(x^2 - 4x = 0\\). There is no constant, so both terms share the factor \\(x\\)."},
    {"pre": "Divide the second term by x: " + M + "4x ÷ x = ", "post": "", "answer": -4,
     "hint": "4 ÷ 1 = 4, and x ÷ x = 1; keep the minus sign."},
    {"say": "So \\(x(x - 4) = 0\\). Either factor can be zero."},
    {"phase": "substitute", "pre": "The first factor is just x, so one solution is x = ", "post": "",
     "answer": 0, "hint": "x on its own is zero when x = 0."},
    {"phase": "substitute", "pre": "Second factor: x " + M + " 4 = 0, so x = ", "post": "",
     "answer": 4, "hint": "Add 4 to both sides."},
    {"pre": "Check x = 4: " + check_expr(4, -4, 0) + " = ", "post": "", "answer": 0,
     "hint": "16 " + M + " 16.", "done": "It gives 0, so x = 4 is right, and x = 0 also gives 0."},
]
# b6 x^2+x-6 -> -2,3 roots 2,-3 ; brackets (x-2)(x+3)
bronze[6]["hint"] = "Two numbers multiply to -6 and add to 1, then flip their signs."
bronze[6]["misconceptions"] = [factor_pair_mis([-2, 3]), one_correct_mis()]
bronze[6]["guided_steps"] = a1_walk(bronze[6]["display"], 1, -6, -2, 3)
# b7 x^2-6x+8 -> -2,-4 roots 2,4
bronze[7]["hint"] = "Two numbers multiply to 8 and add to -6, then flip their signs."
bronze[7]["misconceptions"] = [factor_pair_mis([-2, -4]), one_correct_mis()]
bronze[7]["guided_steps"] = a1_walk(bronze[7]["display"], -6, 8, -2, -4)

# =========================== SILVER ========================================
silver = pb["silver"]
# s0 x^2-2x-15 -> -5,3 roots 5,-3
silver[0]["hint"] = "Two numbers multiply to -15 and add to -2; one is negative."
silver[0]["misconceptions"] = [factor_pair_mis([-5, 3]), one_correct_mis()]
silver[0]["guided_steps"] = a1_walk(silver[0]["display"], -2, -15, -5, 3)
# s1 x^2+4x-21 -> -3,7 roots 3,-7
silver[1]["hint"] = "Two numbers multiply to -21 and add to 4; one is negative."
silver[1]["misconceptions"] = [factor_pair_mis([-3, 7]), one_correct_mis()]
silver[1]["guided_steps"] = a1_walk(silver[1]["display"], 4, -21, -3, 7)
# s2 2x^2+3x-2 a!=1 roots 0.5,-2 ; (2x-1)(x+2); ac=-4 -> 4,-1
silver[2]["hint"] = "Multiply a by c, split the middle term, factorise by grouping, then divide by the coefficient."
silver[2]["misconceptions"] = [
    {"pattern": "forgot_divide_coeff", "check": "wrong", "expect": [1, -2],
     "message": "It looks like you solved 2x " + M + " 1 = 0 as x = 1. But 2x = 1 means x = 1/2: "
                "divide by the number in front of x.",
     "note": "Forgetting to divide the first bracket by 2 gives 1 instead of 0.5."},
    one_correct_mis()]
silver[2]["guided_steps"] = [
    {"say": "With a coefficient on \\(x^2\\), use split the middle. Multiply the ends: \\(2 \\times (-2) = -4\\).",
     "pre": "Two numbers multiply to " + M + "4 and add to 3: 4 and ", "post": "", "answer": -1,
     "hint": "4 × (" + M + "1) = " + M + "4 and 4 + (" + M + "1) = 3."},
    {"say": "Grouping gives \\((2x - 1)(x + 2) = 0\\).", "phase": "substitute",
     "pre": "Split: 2x² + 4x " + M + " x " + M + " 2, group to 2x(x+2) " + M +
            " 1(x+2) = (2x " + M + " 1)(x + 2). Set 2x " + M + " 1 = 0: 2x = 1, x = ",
     "post": "", "answer": 0.5, "hint": "Divide 1 by 2."},
    {"pre": "Set x + 2 = 0: x = ", "post": "", "answer": -2, "hint": "Subtract 2 from both sides."},
    {"pre": "Check x = 0.5: " + check_expr(0.5, 3, -2, a=2) + " = ", "post": "", "answer": 0,
     "hint": "0.5 + 1.5 " + M + " 2.",
     "done": "0.5 + 1.5 " + M + " 2 = 0, and x = " + M + "2 gives 8 " + M + " 6 " + M +
             " 2 = 0 too. Solutions x = 0.5 and x = " + M + "2."},
]
# s3 x^2=5x+14 rearrange roots 7,-2 ; (x-7)(x+2)
silver[3]["hint"] = "Rearrange to = 0 first, then find two numbers that multiply to -14 and add to -5."
silver[3]["misconceptions"] = [
    {"pattern": "not_rearranged", "check": "negated", "expect": [-7, 2],
     "message": "Rearrange to x² " + M + " 5x " + M + " 14 = 0 first, then (x " + M +
                " 7)(x + 2) = 0. Flipping the signs gives x = 7 and x = " + M + "2.",
     "note": "Reporting the raw bracket numbers -7 and 2 is the negation of the roots."},
    one_correct_mis()]
silver[3]["guided_steps"] = [
    {"say": "First rearrange so one side is 0. Move every term on the right across to the left; each changes sign."},
    {"pre": "The 5x on the right moves left and becomes ", "post": "x", "answer": -5,
     "hint": "+5x on the right becomes " + M + "5x on the left."},
    {"pre": "The 14 on the right moves left and becomes ", "post": "", "answer": -14,
     "hint": "+14 on the right becomes " + M + "14 on the left."},
    {"say": "So \\(x^2 - 5x - 14 = 0\\). Now two numbers multiply to \\(-14\\) and add to \\(-5\\)."},
    {"pre": "The smaller of the two numbers is ", "post": "", "answer": -7,
     "hint": "List pairs that multiply to " + M + "14; take the pair that adds to " + M + "5, then the smaller."},
    {"pre": "The larger of the two numbers is ", "post": "", "answer": 2,
     "hint": "They add to " + M + "5, and the smaller was " + M + "7."},
    {"say": "So \\((x - 7)(x + 2) = 0\\)."},
    {"phase": "substitute", "pre": "First bracket zero: x " + M + " 7 = 0, so x = ", "post": "",
     "answer": 7, "hint": "Add 7 to both sides."},
    {"phase": "substitute", "pre": "Second bracket zero: x + 2 = 0, so x = ", "post": "",
     "answer": -2, "hint": "Subtract 2 from both sides."},
    {"pre": "Check x = 7: " + check_expr(7, -5, -14) + " = ", "post": "", "answer": 0,
     "hint": "49 " + M + " 35 " + M + " 14.",
     "done": "It gives 0, so x = 7 is right, and x = " + M + "2 checks the same way."},
]
# s4 x^2-25 DOTS roots 5,-5
silver[4]["hint"] = "There is no middle term, so it is a difference of two squares: split into (x + 5)(x - 5)."
silver[4]["misconceptions"] = [one_correct_mis()]
silver[4]["guided_steps"] = a1_walk(silver[4]["display"], 0, -25, -5, 5)
# s5 3x^2-12x common factor roots 0,4
silver[5]["hint"] = "Both terms share 3x; take it out, then set each factor to zero."
silver[5]["misconceptions"] = [
    {"pattern": "factor_pair_not_solved", "check": "negated", "expect": [0, -4],
     "message": "The factor is 3x(x " + M + " 4). Set each to zero: x = 0, and x " + M +
                " 4 = 0 gives x = 4. The solutions are 0 and 4.",
     "note": "Not flipping the 4 gives 0 and -4."},
    one_correct_mis()]
silver[5]["guided_steps"] = [
    {"say": "Solve \\(3x^2 - 12x = 0\\). Both terms share the common factor \\(3x\\)."},
    {"pre": "Divide the second term by 3x: 12x ÷ 3x = ", "post": "", "answer": 4,
     "hint": "12 ÷ 3 = 4, and x ÷ x = 1."},
    {"say": "So \\(3x(x - 4) = 0\\). Either factor can be zero."},
    {"phase": "substitute", "pre": "First factor: 3x = 0, so x = ", "post": "", "answer": 0,
     "hint": "3 times x is 0 only when x itself is 0."},
    {"phase": "substitute", "pre": "Second factor: x " + M + " 4 = 0, so x = ", "post": "",
     "answer": 4, "hint": "Add 4 to both sides."},
    {"pre": "Check x = 4: " + check_expr(4, -12, 0, a=3) + " = ", "post": "", "answer": 0,
     "hint": "3×16 = 48, and 12×4 = 48.",
     "done": "48 " + M + " 48 = 0, so x = 4 is right, and x = 0 also gives 0."},
]
# s6 x^2-10x+25 repeated root 5,5 ; (x-5)^2
silver[6]["hint"] = "It is a perfect square: two equal numbers multiply to 25 and add to -10."
silver[6]["misconceptions"] = [
    {"pattern": "factor_pair_not_solved", "check": "negated", "expect": [-5, -5],
     "message": "The bracket is (x " + M + " 5), so the sign flips: x = 5. It is a repeated root, so "
                "enter 5 for both.",
     "note": "Not flipping the 5 gives -5, -5."},
    {"pattern": "one_correct", "check": "partial", "expect": None,
     "message": "This is a perfect square, (x " + M + " 5)² = 0, so there is one repeated root: "
                "x = 5. Enter 5 for both solutions.",
     "note": "Repeated root; both values are 5."}]
silver[6]["guided_steps"] = [
    {"say": "Solve \\(x^2 - 10x + 25 = 0\\). Two equal numbers multiply to 25 and add to \\(-10\\)."},
    {"pre": "The first of the two equal numbers is ", "post": "", "answer": -5,
     "hint": M + "5 × " + M + "5 = 25 and " + M + "5 + " + M + "5 = " + M + "10."},
    {"pre": "The second (equal) number is ", "post": "", "answer": -5,
     "hint": "It is the same as the first."},
    {"say": "So \\((x - 5)(x - 5) = (x - 5)^2 = 0\\). A perfect square: the root is repeated."},
    {"phase": "substitute", "pre": "x " + M + " 5 = 0, so x = ", "post": "", "answer": 5,
     "hint": "Add 5 to both sides."},
    {"phase": "substitute", "pre": "The root is repeated, so the second solution is also x = ",
     "post": "", "answer": 5, "hint": "Both brackets are the same, so both give 5."},
    {"pre": "Check x = 5: " + check_expr(5, -10, 25) + " = ", "post": "", "answer": 0,
     "hint": "25 " + M + " 50 + 25.",
     "done": "It gives 0, so the repeated root x = 5 is right."},
]

# =========================== GOLD ==========================================
gold = pb["gold"]
# g0 REPAIR: 6x^2+x-2 (root -2/3 = -0.667 messy) -> 4x^2+4x-3 roots 0.5,-1.5
gold[0]["display"] = "Solve \\(4x^2 + 4x - 3 = 0\\)"
gold[0]["solutions"] = [0.5, -1.5]
gold[0]["hint"] = "Multiply a by c, split the middle term, factorise by grouping, then divide by the coefficient."
gold[0]["misconceptions"] = [
    {"pattern": "forgot_divide_coeff", "check": "wrong", "expect": [1, -3],
     "message": "It looks like you solved 2x " + M + " 1 = 0 as x = 1 and 2x + 3 = 0 as x = " + M +
                "3. But 2x = 1 means x = 1/2, and 2x = " + M + "3 means x = " + M + "3/2: divide by "
                "the number in front of x.",
     "note": "Forgetting to divide both brackets by 2 gives 1 and -3."},
    one_correct_mis()]
gold[0]["guided_steps"] = [
    {"say": "With a coefficient on \\(x^2\\), use split the middle. Multiply the ends: \\(4 \\times (-3) = -12\\).",
     "pre": "Two numbers multiply to " + M + "12 and add to 4: 6 and ", "post": "", "answer": -2,
     "hint": "6 × (" + M + "2) = " + M + "12 and 6 + (" + M + "2) = 4."},
    {"say": "Grouping gives \\((2x + 3)(2x - 1) = 0\\).", "phase": "substitute",
     "pre": "Split: 4x² + 6x " + M + " 2x " + M + " 3, group to 2x(2x+3) " + M +
            " 1(2x+3) = (2x + 3)(2x " + M + " 1). Set 2x " + M + " 1 = 0: 2x = 1, x = ",
     "post": "", "answer": 0.5, "hint": "Divide 1 by 2."},
    {"pre": "Set 2x + 3 = 0: 2x = " + M + "3, x = ", "post": "", "answer": -1.5,
     "hint": "Divide " + M + "3 by 2."},
    {"pre": "Check x = 0.5: " + check_expr(0.5, 4, -3, a=4) + " = ", "post": "", "answer": 0,
     "hint": "1 + 2 " + M + " 3.",
     "done": "1 + 2 " + M + " 3 = 0, and x = " + M + "1.5 gives 9 " + M + " 6 " + M +
             " 3 = 0 too. Solutions x = 0.5 and x = " + M + "1.5."},
]
# g1 4x^2-1 DOTS a!=1 roots 0.5,-0.5 ; (2x+1)(2x-1)
gold[1]["hint"] = "No middle term: a difference of two squares. 4x squared is (2x) squared."
gold[1]["misconceptions"] = [
    {"pattern": "forgot_divide_coeff", "check": "wrong", "expect": [1, -1],
     "message": "It looks like you solved 2x = 1 as x = 1 and 2x = " + M + "1 as x = " + M +
                "1. But 2x = 1 means x = 1/2: divide by the 2 in front of x.",
     "note": "Forgetting to divide by 2 gives 1 and -1."},
    one_correct_mis()]
gold[1]["guided_steps"] = [
    {"say": "There is no middle term, so this is a difference of two squares: \\(4x^2\\) is \\((2x)^2\\) and \\(1\\) is \\(1^2\\)."},
    {"phase": "substitute", "pre": "So it factorises to (2x + 1)(2x " + M +
            " 1) = 0. Set 2x " + M + " 1 = 0: 2x = 1, x = ", "post": "", "answer": 0.5,
     "hint": "Divide 1 by 2."},
    {"pre": "Set 2x + 1 = 0: 2x = " + M + "1, x = ", "post": "", "answer": -0.5,
     "hint": "Divide " + M + "1 by 2."},
    {"pre": "Check x = 0.5: " + check_expr(0.5, 0, -1, a=4) + " = ", "post": "", "answer": 0,
     "hint": "4 × 0.25 " + M + " 1.",
     "done": "1 " + M + " 1 = 0, so x = 0.5 is right, and x = " + M + "0.5 checks the same way."},
]
# g2 2x^2+7x+3 roots -0.5,-3 ; (2x+1)(x+3) ; ac=6 -> 6,1
gold[2]["hint"] = "Multiply a by c, split the middle term, factorise by grouping, then divide by the coefficient."
gold[2]["misconceptions"] = [
    {"pattern": "forgot_divide_coeff", "check": "wrong", "expect": [-1, -3],
     "message": "It looks like you solved 2x + 1 = 0 as x = " + M + "1. But 2x = " + M +
                "1 means x = " + M + "1/2: divide by the 2 in front of x.",
     "note": "Forgetting to divide the first bracket by 2 gives -1 instead of -0.5."},
    one_correct_mis()]
gold[2]["guided_steps"] = [
    {"say": "With a coefficient on \\(x^2\\), use split the middle. Multiply the ends: \\(2 \\times 3 = 6\\).",
     "pre": "Two numbers multiply to 6 and add to 7: 6 and ", "post": "", "answer": 1,
     "hint": "6 × 1 = 6 and 6 + 1 = 7."},
    {"say": "Grouping gives \\((2x + 1)(x + 3) = 0\\).", "phase": "substitute",
     "pre": "Split: 2x² + 6x + x + 3, group to 2x(x+3) + 1(x+3) = (2x + 1)(x + 3). "
            "Set 2x + 1 = 0: 2x = " + M + "1, x = ", "post": "", "answer": -0.5,
     "hint": "Divide " + M + "1 by 2."},
    {"pre": "Set x + 3 = 0: x = ", "post": "", "answer": -3, "hint": "Subtract 3 from both sides."},
    {"pre": "Check x = " + M + "0.5: " + check_expr(-0.5, 7, 3, a=2) + " = ", "post": "",
     "answer": 0, "hint": "0.5 " + M + " 3.5 + 3.",
     "done": "0.5 " + M + " 3.5 + 3 = 0, and x = " + M + "3 gives 18 " + M + " 21 + 3 = 0 too. "
             "Solutions x = " + M + "0.5 and x = " + M + "3."},
]
# g3 x^2+3x=18 rearrange a=1 roots 3,-6 ; (x+6)(x-3)
gold[3]["hint"] = "Rearrange to = 0 first, then find two numbers that multiply to -18 and add to 3."
gold[3]["misconceptions"] = [
    {"pattern": "not_rearranged", "check": "negated", "expect": [6, -3],
     "message": "Move 18 across first: x² + 3x " + M + " 18 = 0, then (x + 6)(x " + M +
                " 3) = 0. Flipping the signs gives x = " + M + "6 and x = 3.",
     "note": "Reporting the raw bracket numbers 6 and -3 is the negation of the roots."},
    one_correct_mis()]
gold[3]["guided_steps"] = [
    {"say": "First rearrange so one side is 0. Subtract 18 from both sides."},
    {"pre": "The 18 moves left and becomes ", "post": "", "answer": -18,
     "hint": "Subtracting 18 from both sides turns +18 into " + M + "18 on the left."},
    {"say": "So \\(x^2 + 3x - 18 = 0\\). Now two numbers multiply to \\(-18\\) and add to \\(3\\)."},
    {"pre": "The smaller of the two numbers is ", "post": "", "answer": -3,
     "hint": "List pairs that multiply to " + M + "18; take the pair that adds to 3, then the smaller."},
    {"pre": "The larger of the two numbers is ", "post": "", "answer": 6,
     "hint": "They add to 3, and the smaller was " + M + "3."},
    {"say": "So \\((x - 3)(x + 6) = 0\\)."},
    {"phase": "substitute", "pre": "First bracket zero: x " + M + " 3 = 0, so x = ", "post": "",
     "answer": 3, "hint": "Add 3 to both sides."},
    {"phase": "substitute", "pre": "Second bracket zero: x + 6 = 0, so x = ", "post": "",
     "answer": -6, "hint": "Subtract 6 from both sides."},
    {"pre": "Check x = 3: " + check_expr(3, 3, -18) + " = ", "post": "", "answer": 0,
     "hint": "9 + 9 " + M + " 18.",
     "done": "It gives 0, so x = 3 is right, and x = " + M + "6 checks the same way."},
]
# g4 5x^2-3x-2 roots 1,-0.4 ; (5x+2)(x-1) ; ac=-10 -> 2,-5
gold[4]["hint"] = "Multiply a by c, split the middle term, factorise by grouping, then divide by the coefficient."
gold[4]["misconceptions"] = [
    {"pattern": "forgot_divide_coeff", "check": "wrong", "expect": [1, -2],
     "message": "It looks like you solved 5x + 2 = 0 as x = " + M + "2. But 5x = " + M +
                "2 means x = " + M + "2/5: divide by the 5 in front of x.",
     "note": "Forgetting to divide the second bracket by 5 gives -2 instead of -0.4."},
    one_correct_mis()]
gold[4]["guided_steps"] = [
    {"say": "With a coefficient on \\(x^2\\), use split the middle. Multiply the ends: \\(5 \\times (-2) = -10\\).",
     "pre": "Two numbers multiply to " + M + "10 and add to " + M + "3: 2 and ", "post": "",
     "answer": -5, "hint": "2 × (" + M + "5) = " + M + "10 and 2 + (" + M + "5) = " + M + "3."},
    {"say": "Grouping gives \\((5x + 2)(x - 1) = 0\\).", "phase": "substitute",
     "pre": "Split: 5x² " + M + " 5x + 2x " + M + " 2, group to 5x(x " + M +
            " 1) + 2(x " + M + " 1) = (5x + 2)(x " + M + " 1). Set x " + M + " 1 = 0: x = ",
     "post": "", "answer": 1, "hint": "Add 1 to both sides."},
    {"pre": "Set 5x + 2 = 0: 5x = " + M + "2, x = ", "post": "", "answer": -0.4,
     "hint": "Divide " + M + "2 by 5."},
    {"pre": "Check x = 1: " + check_expr(1, -3, -2, a=5) + " = ", "post": "", "answer": 0,
     "hint": "5 " + M + " 3 " + M + " 2.",
     "done": "5 " + M + " 3 " + M + " 2 = 0, and x = " + M + "0.4 gives 0.8 + 1.2 " + M +
             " 2 = 0 too. Solutions x = 1 and x = " + M + "0.4."},
]

# =========================== tier_guides ===================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: quadratics already in the form \\(x^2 + bx + c = 0\\)",
        "steps": [
            "Find two numbers that <strong>multiply to \\(c\\)</strong> (the last number) and "
            "<strong>add to \\(b\\)</strong> (the middle number).",
            "Write them in brackets: \\((x + p)(x + q) = 0\\).",
            "Set each bracket to zero. \\(x + p = 0\\) gives \\(x = -p\\), so both signs flip."
        ],
        "example": {
            "question": "Solve \\(x^2 + 9x + 20 = 0\\)",
            "steps": [
                {"label": "Find the pair", "content": "<p>Two numbers multiply to \\(20\\) and add to \\(9\\): that is \\(4\\) and \\(5\\).</p>"},
                {"label": "Factorise", "content": "<p>\\((x + 4)(x + 5) = 0\\)</p>"},
                {"label": "Check", "content": "<p>Put \\(x = -4\\) into \\(x^2 + 9x + 20\\): \\(16 - 36 + 20 = 0\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\(x = -4\\) or \\(x = -5\\)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: negatives, a common factor, or a difference of two squares",
        "steps": [
            "With a negative constant, one bracket number is negative: two numbers multiply to \\(c\\) and add to \\(b\\).",
            "If both terms share a factor, like \\(3x^2 - 12x\\), take it out: \\(3x(x - 4) = 0\\).",
            "A <strong>difference of two squares</strong> like \\(x^2 - 25\\) has no middle term: it splits into \\((x + 5)(x - 5)\\)."
        ],
        "example": {
            "question": "Solve \\(x^2 - 2x - 8 = 0\\)",
            "steps": [
                {"label": "Find the pair", "content": "<p>Two numbers multiply to \\(-8\\) and add to \\(-2\\): that is \\(2\\) and \\(-4\\).</p>"},
                {"label": "Factorise", "content": "<p>\\((x + 2)(x - 4) = 0\\)</p>"},
                {"label": "Check", "content": "<p>Put \\(x = 4\\) into \\(x^2 - 2x - 8\\): \\(16 - 8 - 8 = 0\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\(x = -2\\) or \\(x = 4\\)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: quadratics where the x squared term has a coefficient",
        "steps": [
            "<strong>When \\(ax^2 + bx + c\\) has \\(a > 1\\)</strong>, multiply \\(a\\) by \\(c\\), then find two numbers multiplying to \\(ac\\) and adding to \\(b\\).",
            "<strong>Split the middle term</strong> with those two numbers, then factorise by grouping into two brackets.",
            "Set each bracket to 0. A bracket like \\(2x - 1 = 0\\) gives \\(x = \\tfrac{1}{2}\\), so divide by the number in front."
        ],
        "example": {
            "question": "Solve \\(2x^2 + 7x + 3 = 0\\)",
            "steps": [
                {"label": "Split the middle (2×3 = 6)", "content": "<p>\\(2x^2 + 6x + x + 3\\)</p>"},
                {"label": "Factorise by grouping", "content": "<p>\\((2x + 1)(x + 3) = 0\\)</p>"},
                {"label": "Solve each bracket", "content": "<p>\\(x = -\\tfrac{1}{2}\\) or \\(x = -3\\)</p>"},
                {"label": "Check", "content": "<p>\\(2(-3)^2 + 7(-3) + 3 = 0\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\(x = -0.5\\) or \\(x = -3\\)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# =========================== guided (opener + teach) =======================
pd["guided"] = {
    "opener": {
        "steps": [
            {"say": "Two quick puzzles, no algebra needed. First: I am thinking of two numbers that "
                    "<strong>multiply to 15</strong> and <strong>add to 8</strong>."},
            {"pre": "The smaller of my two numbers is ", "post": "", "answer": 3,
             "hint": "Try pairs that multiply to 15: 1 and 15, 3 and 5. Which pair adds to 8?"},
            {"say": "The pair is 3 and 5. Finding two numbers that multiply and add like that "
                    "<strong>is</strong> factorising. For \\(x^2 + 8x + 15\\) you look for two numbers "
                    "that multiply to 15 (the last number) and add to 8 (the middle number): 3 and 5. "
                    "So it becomes \\((x + 3)(x + 5)\\)."},
            {"say": "Now the second half. If two numbers multiply together to give <strong>0</strong>, "
                    "at least one of them must be 0. Suppose 7 times something equals 0."},
            {"pre": "7 × (something) = 0, so that something must be ", "post": "", "answer": 0,
             "hint": "7 times what gives 0?"},
            {"say": "That is the <strong>zero product rule</strong>. Once you have \\((x + 3)(x + 5) = 0\\), "
                    "one bracket must be 0: \\(x + 3 = 0\\) gives \\(x = -3\\), and \\(x + 5 = 0\\) gives "
                    "\\(x = -5\\). Finding the pair and using the zero rule are the whole method."}
        ]
    },
    "teach": {
        "bronze": {
            "display": "Solve \\(x^2 + 7x + 12 = 0\\)",
            "steps": [
                {"say": "It is already \\(= 0\\). Look for two numbers that multiply to 12 and add to 7."},
                {"pre": "The smaller number is ", "post": "", "answer": 3,
                 "hint": "Pairs of 12: 1 and 12, 2 and 6, 3 and 4. Which adds to 7?"},
                {"pre": "The larger number is ", "post": "", "answer": 4, "hint": "7 " + M + " 3."},
                {"say": "So \\((x + 3)(x + 4) = 0\\). Each bracket can be zero."},
                {"pre": "x + 3 = 0, so x = ", "post": "", "answer": -3,
                 "hint": "Subtract 3 from both sides; the sign flips.",
                 "done": "The sign flips: a plus in the bracket becomes a minus in the answer. That is the whole point."},
                {"pre": "x + 4 = 0, so x = ", "post": "", "answer": -4, "hint": "Subtract 4 from both sides."},
                {"pre": "Check x = " + M + "3: " + check_expr(-3, 7, 12) + " = ", "post": "", "answer": 0,
                 "hint": "9 " + M + " 21 + 12.",
                 "done": "It gives 0, so x = " + M + "3 works, and x = " + M + "4 works the same way."}
            ]
        },
        "silver": {
            "display": "Solve \\(x^2 - x - 12 = 0\\)",
            "steps": [
                {"say": "The constant is negative, so one of the two numbers is negative. They multiply to \\(-12\\) and add to \\(-1\\)."},
                {"pre": "The negative number is ", "post": "", "answer": -4,
                 "hint": "Try 3 and " + M + "4: 3×(" + M + "4) = " + M + "12 and 3 + (" + M + "4) = " + M + "1."},
                {"pre": "The positive number is ", "post": "", "answer": 3,
                 "hint": M + "1 " + M + " (" + M + "4) = 3.",
                 "done": "One negative, one positive: that is the new move when the constant is negative."},
                {"say": "So \\((x - 4)(x + 3) = 0\\)."},
                {"pre": "x " + M + " 4 = 0, so x = ", "post": "", "answer": 4, "hint": "Add 4 to both sides."},
                {"pre": "x + 3 = 0, so x = ", "post": "", "answer": -3, "hint": "Subtract 3 from both sides."},
                {"pre": "Check x = 4: " + check_expr(4, -1, -12) + " = ", "post": "", "answer": 0,
                 "hint": "16 " + M + " 4 " + M + " 12.",
                 "done": "It gives 0, so x = 4 works, and x = " + M + "3 works the same way."}
            ]
        },
        "gold": {
            "display": "Solve \\(2x^2 + 5x - 3 = 0\\)",
            "steps": [
                {"say": "With a coefficient on \\(x^2\\), use the split the middle method. First multiply the ends: \\(2 \\times (-3) = -6\\).",
                 "pre": "Two numbers multiply to " + M + "6 and add to 5: 6 and ", "post": "", "answer": -1,
                 "hint": "6 × (" + M + "1) = " + M + "6 and 6 + (" + M + "1) = 5."},
                {"say": "Grouping gives \\((2x - 1)(x + 3) = 0\\).",
                 "pre": "Split: 2x² + 6x " + M + " x " + M + " 3, group to 2x(x+3) " + M +
                        " 1(x+3) = (2x " + M + " 1)(x + 3). Set 2x " + M + " 1 = 0: 2x = 1, x = ",
                 "post": "", "answer": 0.5, "hint": "Divide 1 by 2."},
                {"pre": "Set x + 3 = 0: x = ", "post": "", "answer": -3, "hint": "Subtract 3 from both sides."},
                {"pre": "Check x = 0.5: " + check_expr(0.5, 5, -3, a=2) + " = ", "post": "", "answer": 0,
                 "hint": "0.5 + 2.5 " + M + " 3.",
                 "done": "0.5 + 2.5 " + M + " 3 = 0, and x = " + M + "3 gives 18 " + M + " 15 " + M +
                         " 3 = 0 too. Solutions x = 0.5 and x = " + M + "3."}
            ]
        }
    }
}

# =========================== method_card (slim) ============================
pd["method_card"] = {
    "title": "Solving Quadratics by Factorising",
    "steps": [
        "Rearrange so one side equals zero",
        "Factorise the quadratic into two brackets",
        "Set each bracket equal to zero",
        "Solve each mini equation for x"
    ],
    "content": "<p>A <strong>quadratic</strong> \\(ax^2 + bx + c = 0\\) usually has two solutions. Get "
               "one side to zero, factorise, then use the <strong>zero product rule</strong>: if "
               "\\(A \\times B = 0\\), then \\(A = 0\\) or \\(B = 0\\). Set each bracket to zero. A "
               "bracket \\(x + 3 = 0\\) gives \\(x = -3\\), so the sign flips. When \\(a > 1\\), split "
               "the middle term first.</p>",
    "example": "<p><strong>Solve</strong> \\(x^2 + 5x + 6 = 0\\): \\((x + 2)(x + 3) = 0\\), so "
               "\\(x = -2\\) or \\(x = -3\\).</p>"
}

# preserve related_videos, worked_examples, topic_links; only strip em dashes
# from worked_example labels (style rule is hard + validator-enforced)
for we in pd.get("worked_examples") or []:
    for st in we.get("steps") or []:
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

out = "lesson_maths-ocr_algebra-L07.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)
