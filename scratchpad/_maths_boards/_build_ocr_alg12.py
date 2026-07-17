# -*- coding: utf-8 -*-
import json, io
from _gen_svg_ocr12 import parabola_svg

live = json.load(io.open("_live_alg12.json", encoding="utf-8"))
pd = live["practice_data"]

# ---------------------------------------------------------------------------
# 1. PROBLEM BANK  (displays + solutions unchanged unless noted; add hint,
#    misconceptions with derived expects, guided_steps on single_value)
# ---------------------------------------------------------------------------

def mc(display, options, sol, hint, misc):
    return {"display": display, "options": options, "solutions": [sol],
            "calculator": False, "input_type": "multiple_choice",
            "hint": hint, "misconceptions": misc}

def sv(display, sol, hint, gsteps, misc):
    return {"display": display, "solutions": [sol], "calculator": False,
            "input_type": "single_value", "hint": hint,
            "guided_steps": gsteps, "misconceptions": misc}

def m(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

bronze = [
    mc(r"Solve \(x^2 - 4 < 0\). What is the range?",
       [r"\(-2 < x < 2\)", r"\(x < -2\) or \(x > 2\)", r"\(x < 2\)", r"\(x > -2\)"], 0,
       "Solve x squared = 4 for roots plus or minus 2, then take between them for < 0.",
       [m("wrong_region", 1, r"For \(< 0\) the U-shape dips below the axis BETWEEN the roots \(\pm 2\), so \(-2 < x < 2\). Outside the roots is where it is above zero."),
        m("one_branch", 2, r"You need both bounds: \(-2 < x < 2\). Keeping only \(x < 2\) drops the lower bound.")]),
    mc(r"Solve \(x^2 - 9 > 0\). What is the range?",
       [r"\(x < -3\) or \(x > 3\)", r"\(-3 < x < 3\)", r"\(x > 3\)", r"\(x > 0\)"], 0,
       "The roots are plus or minus 3; for > 0 take outside them.",
       [m("wrong_region", 1, r"For \(> 0\) the curve is above the axis OUTSIDE the roots \(\pm 3\): \(x < -3\) or \(x > 3\). Between the roots it is below zero."),
        m("one_branch", 2, r"You need both pieces: \(x < -3\) or \(x > 3\). Keeping only \(x > 3\) drops the left-hand piece.")]),
    mc(r"Solve \((x-1)(x-5) < 0\). What is the range?",
       [r"\(1 < x < 5\)", r"\(x < 1\) or \(x > 5\)", r"\(x > 1\)", r"\(x < 5\)"], 0,
       "The roots are 1 and 5; for < 0 take between them.",
       [m("wrong_region", 1, r"For \(< 0\) the product is negative BETWEEN the roots 1 and 5: \(1 < x < 5\). Outside the roots both brackets share a sign, giving a positive product."),
        m("one_branch", 2, r"You need both bounds: \(1 < x < 5\). Keeping only \(x > 1\) drops the upper bound.")]),
    mc(r"Solve \(x^2 - 6x + 8 \leq 0\). What is the range?",
       [r"\(2 \leq x \leq 4\)", r"\(x \leq 2\) or \(x \geq 4\)", r"\(2 < x < 4\)", r"\(x < 2\)"], 0,
       "Factorise to (x-2)(x-4); for less-than-or-equal take between, inclusive.",
       [m("wrong_region", 1, r"\((x-2)(x-4) \leq 0\): for \(\leq 0\) take BETWEEN the roots, \(2 \leq x \leq 4\). Outside is where the product is positive."),
        m("notation", 2, r"The sign is \(\leq\), so the endpoints are included: \(2 \leq x \leq 4\). Strict bounds would wrongly leave out \(x = 2\) and \(x = 4\).")]),
    sv(r"Solve \(x^2 > 25\). How many integers from \(-10\) to \(10\) satisfy this?", 10,
       "x squared > 25 means x < -5 or x > 5. Count integers on both sides.",
       [{"say": r"Find where \(x^2 = 25\) by square-rooting: the critical values are \(\pm 5\). So \(x^2 > 25\) means \(x < -5\) or \(x > 5\)."},
        {"pre": "The positive critical value is ", "post": "", "answer": 5, "hint": "The square root of 25."},
        {"pre": "The negative critical value is ", "post": "", "answer": -5, "hint": "The other square root of 25."},
        {"say": r"Now count the integers from \(-10\) to \(10\) that are below \(-5\) or above 5."},
        {"pre": "Integers -10 to -6 (all below -5): how many? ", "post": "", "phase": "substitute", "answer": 5, "hint": "-10, -9, -8, -7, -6."},
        {"pre": "There are 5 more above 5 (6 to 10). Total = ", "post": "", "phase": "substitute", "answer": 10, "done": "Ten integers in total. x = plus or minus 5 give exactly 25, not more, so they are excluded.", "hint": "Five on the left plus five on the right."}],
       [m("notation", 12, r"The sign is strict (\(> 25\)), so \(x = \pm 5\) are excluded. Using \(\geq 25\) would add both, giving 12, but only values beyond \(\pm 5\) count."),
        m("one_branch", 5, r"Count BOTH sides: 5 integers below \(-5\) and 5 above 5. Keeping only one side gives 5, but the total is 10.")]),
    mc(r"Solve \((x+3)(x-1) > 0\). What is the range?",
       [r"\(x < -3\) or \(x > 1\)", r"\(-3 < x < 1\)", r"\(x > 1\)", r"\(x > -3\)"], 0,
       "The roots are -3 and 1; for > 0 take outside them.",
       [m("wrong_region", 1, r"For \(> 0\) the product is positive OUTSIDE the roots \(-3\) and 1: \(x < -3\) or \(x > 1\). Between the roots the product is negative."),
        m("one_branch", 2, r"You need both pieces: \(x < -3\) or \(x > 1\). Keeping only \(x > 1\) drops the left-hand piece.")]),
    sv(r"How many integers satisfy \(x^2 - 3x - 4 \leq 0\)?", 6,
       "Factorise to (x-4)(x+1); the range is -1 to 4 inclusive. Count them.",
       [{"say": r"Factorise \(x^2 - 3x - 4\). Two numbers multiply to \(-4\) and add to \(-3\): they are \(-4\) and \(+1\), giving \((x-4)(x+1)\)."},
        {"pre": "From x - 4 = 0:  x = ", "post": "", "answer": 4, "hint": "x - 4 = 0 gives x = 4."},
        {"pre": "From x + 1 = 0:  x = ", "post": "", "answer": -1, "hint": "x + 1 = 0 gives x = -1."},
        {"say": r"For \(\leq 0\) the solution is between the roots, inclusive: \(-1 \leq x \leq 4\). Count every whole number from \(-1\) to 4."},
        {"pre": "They are -1, 0, 1, 2, 3, 4.  How many? ", "post": "", "phase": "substitute", "answer": 6, "hint": "Count from -1 up to 4."},
        {"pre": "Check the endpoint x = 4:  4² - 3(4) - 4 = ", "post": "", "phase": "substitute", "answer": 0, "done": "It equals 0, which satisfies the less-than-or-equal sign, so 4 IS counted. Six integers in total.", "hint": "16 - 12 - 4."}],
       [m("notation", 4, r"The sign includes equals (\(\leq 0\)), so the roots \(-1\) and 4 ARE counted. Using a strict \(< 0\) would drop both endpoints, giving 4, but the answer is 6."),
        m("off_by_one", 5, r"Count every integer from \(-1\) to 4: \(-1, 0, 1, 2, 3, 4\) is 6, not 5. Forgetting the \(-1\) end causes an off-by-one.")]),
    mc(r"Solve \(x^2 + x - 6 < 0\). What is the range?",
       [r"\(-3 < x < 2\)", r"\(x < -3\) or \(x > 2\)", r"\(x > 2\)", r"\(-3 \leq x \leq 2\)"], 0,
       "Factorise to (x+3)(x-2); for < 0 take between the roots, strict.",
       [m("wrong_region", 1, r"\((x+3)(x-2) < 0\): for \(< 0\) take BETWEEN the roots, \(-3 < x < 2\). Outside is where the product is positive."),
        m("notation", 3, r"The sign is strict (\(< 0\)), so the roots are excluded: \(-3 < x < 2\). Closed bounds would wrongly include \(x = -3\) and \(x = 2\).")]),
]

silver = [
    mc(r"Solve \(x^2 - 2x - 8 \geq 0\). What is the range?",
       [r"\(x \leq -2\) or \(x \geq 4\)", r"\(-2 \leq x \leq 4\)", r"\(x \geq 4\)", r"\(x \leq -2\)"], 0,
       "Factorise to (x-4)(x+2); for greater-than-or-equal take outside, inclusive.",
       [m("wrong_region", 1, r"\((x-4)(x+2) \geq 0\): for \(\geq 0\) take OUTSIDE the roots, \(x \leq -2\) or \(x \geq 4\). Between them the product is negative."),
        m("one_branch", 2, r"You need both pieces: \(x \leq -2\) or \(x \geq 4\). Keeping only \(x \geq 4\) drops the left-hand piece.")]),
    mc(r"Solve \(2x^2 - 5x - 3 < 0\). What is the range?",
       [r"\(-\frac{1}{2} < x < 3\)", r"\(x < -\frac{1}{2}\) or \(x > 3\)", r"\(0 < x < 3\)", r"\(-1 < x < 3\)"], 0,
       "Split the middle term to (2x+1)(x-3); for < 0 take between the roots.",
       [m("wrong_region", 1, r"\((2x+1)(x-3) < 0\): for \(< 0\) take BETWEEN the roots \(-\tfrac{1}{2}\) and 3, so \(-\tfrac{1}{2} < x < 3\). Outside is where it is positive."),
        m("wrong_roots", 3, r"Factorise to \((2x+1)(x-3)\): from \(2x+1=0\) the root is \(-\tfrac{1}{2}\), not \(-1\). Divide by the coefficient of \(x\) correctly.")]),
    sv(r"Solve \(x^2 \leq 3x + 10\). How many integers satisfy it?", 8,
       "Rearrange to x squared - 3x - 10 <= 0, factorise (x-5)(x+2), count inclusive.",
       [{"say": r"Rearrange to \(x^2 - 3x - 10 \leq 0\). Factorise: two numbers multiply to \(-10\) and add to \(-3\), namely \(-5\) and \(+2\), giving \((x-5)(x+2)\)."},
        {"pre": "From x - 5 = 0:  x = ", "post": "", "answer": 5, "hint": "x - 5 = 0 gives x = 5."},
        {"pre": "From x + 2 = 0:  x = ", "post": "", "answer": -2, "hint": "x + 2 = 0 gives x = -2."},
        {"say": r"For \(\leq 0\), take between the roots, inclusive: \(-2 \leq x \leq 5\). Count the whole numbers from \(-2\) to 5."},
        {"pre": "They are -2, -1, 0, 1, 2, 3, 4, 5.  How many? ", "post": "", "phase": "substitute", "answer": 8, "hint": "Count from -2 up to 5."},
        {"pre": "Check the endpoint x = -2:  (-2)² - 3(-2) - 10 = ", "post": "", "phase": "substitute", "answer": 0, "done": "4 + 6 - 10 = 0, which satisfies the less-than-or-equal sign, so -2 IS counted. Eight integers.", "hint": "4 + 6 - 10."}],
       [m("notation", 6, r"The sign includes equals (\(\leq\)), so the roots \(-2\) and 5 ARE counted. A strict version would drop both endpoints, giving 6, but the answer is 8."),
        m("off_by_one", 7, r"Count every integer from \(-2\) to 5: that is 8 values, not 7. Missing one endpoint causes an off-by-one.")]),
    mc(r"Solve \(-x^2 + 4x - 3 > 0\). What is the range?",
       [r"\(1 < x < 3\)", r"\(x < 1\) or \(x > 3\)", r"\(x > 1\)", r"\(x < 3\)"], 0,
       "Multiply by -1 and flip the sign: x squared - 4x + 3 < 0, then take between.",
       [m("sign_flip", 1, r"Multiplying by \(-1\) flips the sign to \(x^2 - 4x + 3 < 0\), so \((x-1)(x-3) < 0\) gives BETWEEN the roots, \(1 < x < 3\). Forgetting to flip gives the outside region."),
        m("one_branch", 2, r"You need both bounds: \(1 < x < 3\). Keeping only \(x > 1\) drops the upper bound.")]),
    mc(r"For what values of \(x\) is \(x^2 + 6x + 5 > 0\)?",
       [r"\(x < -5\) or \(x > -1\)", r"\(-5 < x < -1\)", r"\(x > -1\)", r"\(x > 0\)"], 0,
       "Factorise to (x+5)(x+1); for > 0 take outside the roots.",
       [m("wrong_region", 1, r"\((x+5)(x+1) > 0\): for \(> 0\) take OUTSIDE the roots \(-5\) and \(-1\): \(x < -5\) or \(x > -1\). Between them the product is negative."),
        m("one_branch", 2, r"You need both pieces: \(x < -5\) or \(x > -1\). Keeping only \(x > -1\) drops the left-hand piece.")]),
    sv(r"How many positive integers satisfy \(x^2 < 50\)?", 7,
       "Find the square root of 50 (about 7.07); count positive integers 1 up to 7.",
       [{"say": r"Find where \(x^2 = 50\). The square root is \(\sqrt{50} \approx 7.07\), so \(x^2 < 50\) means \(-7.07 < x < 7.07\)."},
        {"pre": "The largest whole number below 7.07 is ", "post": "", "answer": 7, "hint": "7 squared is 49, still under 50."},
        {"say": r"We want POSITIVE integers only, so count from 1 up to that value."},
        {"pre": "Count the positive integers 1, 2, 3, 4, 5, 6, 7.  How many? ", "post": "", "phase": "substitute", "answer": 7, "hint": "Count from 1 up to 7."},
        {"pre": "Check x = 7:  7² = ", "post": "", "phase": "substitute", "answer": 49, "done": "49 is below 50, so 7 works, and 8 squared is 64 which is too big. Seven positive integers.", "hint": "7 times 7."}],
       [m("includes_zero", 8, r"Zero is not a positive integer, so start from 1. Counting 0 as well gives 8, but only \(1\) to 7 are positive integers."),
        m("off_by_one", 6, r"Since \(7^2 = 49 < 50\), 7 does satisfy it. Stopping at 6 gives 6, but the answer is 7.")]),
    sv(r"Solve \(x^2 + 4x \geq 5\). What is the positive root?", 1,
       "Rearrange to x squared + 4x - 5 >= 0, factorise (x+5)(x-1); the positive root is 1.",
       [{"say": r"Rearrange to \(x^2 + 4x - 5 \geq 0\). Factorise: two numbers multiply to \(-5\) and add to \(+4\), namely \(+5\) and \(-1\), giving \((x+5)(x-1)\)."},
        {"pre": "From x + 5 = 0:  x = ", "post": "", "answer": -5, "hint": "x + 5 = 0 gives x = -5."},
        {"pre": "From x - 1 = 0:  x = ", "post": "", "phase": "substitute", "answer": 1, "hint": "x - 1 = 0 gives x = 1."},
        {"pre": "Of the roots -5 and 1, the positive one is ", "post": "", "phase": "substitute", "answer": 1, "done": "The positive root is 1. The full solution would be x <= -5 or x >= 1, but the question only asks for the positive root.", "hint": "Which root is greater than zero?"}],
       [m("wrong_sign", 5, r"From \(x - 1 = 0\) the positive root is \(x = 1\), not 5. Read the root straight from the bracket \((x-1)\)."),
        m("other_root", -5, r"\(-5\) is the other root, but it is negative. The question asks for the POSITIVE root, which is 1.")]),
]

gold = [
    mc(r"Solve \(3x^2 + 2x - 1 > 0\). What is the range?",
       [r"\(x < -1\) or \(x > \frac{1}{3}\)", r"\(-1 < x < \frac{1}{3}\)", r"\(x > \frac{1}{3}\)", r"\(x > 0\)"], 0,
       "Split the middle term to (3x-1)(x+1); for > 0 take outside the roots.",
       [m("wrong_region", 1, r"\((3x-1)(x+1) > 0\): for \(> 0\) take OUTSIDE the roots \(-1\) and \(\tfrac{1}{3}\): \(x < -1\) or \(x > \tfrac{1}{3}\). Between them the product is negative."),
        m("one_branch", 2, r"You need both pieces: \(x < -1\) or \(x > \tfrac{1}{3}\). Keeping only \(x > \tfrac{1}{3}\) drops the left-hand piece.")]),
    mc(r"Find the values of \(k\) for which \(x^2 + kx + 4 = 0\) has no real roots. What is the range?",
       [r"\(-4 < k < 4\)", r"\(k < -4\) or \(k > 4\)", r"\(k > 4\)", r"\(k < -4\)"], 0,
       "No real roots needs the discriminant < 0: solve k squared - 16 < 0.",
       [m("wrong_disc", 1, r"No real roots needs the discriminant \(< 0\): \(k^2 - 16 < 0\) gives \(-4 < k < 4\). A discriminant \(> 0\) gives the outside range and TWO real roots."),
        m("one_branch", 2, r"\(k^2 < 16\) gives a symmetric range \(-4 < k < 4\). Do not drop the lower bound.")]),
    mc(r"Find the set of values of \(x\) for which \(x^2 - 2x > x + 4\). What is the range?",
       [r"\(x < -1\) or \(x > 4\)", r"\(-1 < x < 4\)", r"\(x > 4\)", r"\(x > 0\)"], 0,
       "Rearrange to x squared - 3x - 4 > 0, factorise (x-4)(x+1), take outside.",
       [m("wrong_region", 1, r"Rearrange to \(x^2 - 3x - 4 > 0\), then \((x-4)(x+1) > 0\) gives OUTSIDE the roots, \(x < -1\) or \(x > 4\). Between the roots the expression is below \(x + 4\)."),
        m("one_branch", 2, r"You need both pieces: \(x < -1\) or \(x > 4\). Keeping only \(x > 4\) drops the left-hand piece.")]),
    sv(r"How many integers satisfy both \(x^2 - 9 \leq 0\) AND \(x + 1 > 0\)?", 4,
       "First solve x squared - 9 <= 0 for -3 <= x <= 3, then keep only x > -1. Count the overlap.",
       [{"say": r"Solve each part. First \(x^2 - 9 \leq 0\) factorises to \((x-3)(x+3) \leq 0\), giving between the roots: \(-3 \leq x \leq 3\)."},
        {"pre": "The second condition x + 1 > 0 rearranges to x > ", "post": "", "answer": -1, "hint": "Subtract 1 from both sides."},
        {"say": r"Overlap \(-3 \leq x \leq 3\) with \(x > -1\): since \(x\) must beat \(-1\), the overlap is \(-1 < x \leq 3\)."},
        {"pre": "The whole numbers with -1 < x ≤ 3 are 0, 1, 2, 3.  How many? ", "post": "", "phase": "substitute", "answer": 4, "hint": "Start just above -1, so from 0."},
        {"pre": "Check x = 3 in the first part:  3² - 9 = ", "post": "", "phase": "substitute", "answer": 0, "done": "0 satisfies the less-than-or-equal sign, and 3 > -1, so 3 is included. The four integers are 0, 1, 2, 3.", "hint": "9 - 9."}],
       [m("forgot_condition", 7, r"You must apply BOTH conditions. \(x^2 - 9 \leq 0\) alone gives \(-3 \leq x \leq 3\) (7 integers), but \(x > -1\) removes \(-3, -2, -1\), leaving 4."),
        m("notation", 5, r"\(x + 1 > 0\) is strict, so \(x = -1\) is excluded. Counting \(-1\) as well gives 5, but only 0, 1, 2, 3 satisfy both.")]),
    mc(r"Solve \(6 - x - x^2 \geq 0\). What is the range?",
       [r"\(-3 \leq x \leq 2\)", r"\(x \leq -3\) or \(x \geq 2\)", r"\(x \leq 2\)", r"\(-2 \leq x \leq 3\)"], 0,
       "Multiply by -1 and flip: x squared + x - 6 <= 0, factorise (x+3)(x-2), take between.",
       [m("sign_flip", 1, r"Multiplying by \(-1\) flips the sign to \(x^2 + x - 6 \leq 0\), so \((x+3)(x-2) \leq 0\) gives BETWEEN the roots, \(-3 \leq x \leq 2\). Forgetting to flip gives the outside region."),
        m("wrong_roots", 3, r"Factorise \(x^2 + x - 6\) to \((x+3)(x-2)\): the roots are \(-3\) and 2, not \(-2\) and 3.")]),
]

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Difference of squares and simple factors, reading between or outside the roots",
    "silver_description": "Factorise three-term quadratics, strict and inclusive signs, integer counts",
    "gold_description": "Rearranging, coefficient of x squared, discriminants and combined conditions",
}

# ---------------------------------------------------------------------------
# 2. GUIDED  (opener + three teach walks with parabola sketches)
# ---------------------------------------------------------------------------

opener = {"steps": [
    {"say": r"Here is a number machine. It multiplies \((x - 2)\) by \((x - 6)\). We want the values of x that make the answer come out BELOW zero (negative). Let us test a few."},
    {"pre": "Try x = 7. First bracket:  7 - 2 = ", "post": "", "answer": 5, "hint": "7 take away 2."},
    {"say": r"The second bracket is \(7 - 6 = 1\). Both are positive, so \(5 \times 1 = 5\), above zero. Now slide x down to 4, in between 2 and 6."},
    {"pre": "First bracket:  4 - 2 = ", "post": "", "answer": 2, "hint": "4 take away 2."},
    {"pre": "Second bracket:  4 - 6 = ", "post": "", "answer": -2, "hint": "4 is less than 6, so this drops below zero."},
    {"say": r"One bracket is positive, the other negative, and a positive times a negative is always NEGATIVE. So the answer is below zero, and that only happens when x sits BETWEEN 2 and 6. That is the whole method for a quadratic inequality: factorise to two brackets, find the two roots, and the expression is below zero between them, above zero outside them. In algebra, \((x-2)(x-6) < 0\) has the solution \(2 < x < 6\)."},
]}

svg_b, _ = parabola_svg(1, -8, 15, 3, 5, "y = x squared minus 8x plus 15", "between",
    "U-shaped parabola y = x squared minus 8x plus 15 crossing the x-axis at two points, with the region below the x-axis between the roots shaded")
svg_s, _ = parabola_svg(1, 2, -8, -4, 2, "y = x squared plus 2x minus 8", "outside",
    "U-shaped parabola y = x squared plus 2x minus 8 with the regions above the x-axis outside the two roots shaded")
svg_g, _ = parabola_svg(2, 1, -6, -2, 1.5, "y = 2x squared plus x minus 6", "outside",
    "U-shaped parabola y = 2x squared plus x minus 6 with the regions above the x-axis outside the two roots shaded")
CAP = '<span class="figure-caption">Sketch, not drawn to scale</span>'

teach = {
  "bronze": {"steps": [
     {"say": r"First factorise. We need two numbers that multiply to \(+15\) and add to \(-8\): they are \(-3\) and \(-5\), so \(x^2 - 8x + 15 = (x-3)(x-5)\). Each bracket gives a root."},
     {"pre": "The first bracket x - 3 is zero when x = ", "post": "", "answer": 3, "hint": "x - 3 = 0."},
     {"pre": "The second bracket x - 5 is zero when x = ", "post": "", "answer": 5, "hint": "x - 5 = 0."},
     {"say": r"So the curve crosses the x-axis at 3 and 5. It is a U-shape, so it dips BELOW the axis between the roots. That is where the expression is \(< 0\)."},
     {"pre": "The solution is 3 < x < 5. The lower bound is ", "post": "", "answer": 3, "hint": "The smaller of the two roots."},
     {"pre": "And the upper bound is ", "post": "", "answer": 5, "hint": "The larger of the two roots."},
     {"pre": "Check x = 4, in the middle:  4² - 8(4) + 15 = ", "post": "", "answer": -1, "done": "Below zero, so 3 < x < 5 is right. Factorise, find the roots, take the region between them: that is the whole bronze move.", "hint": "16 - 32 + 15. It should be below zero."},
  ], "display": svg_b + CAP + r"Solve \(x^2 - 8x + 15 < 0\)"},
  "silver": {"steps": [
     {"say": r"Factorise. Two numbers multiply to \(-8\) and add to \(+2\): they are \(+4\) and \(-2\), so \(x^2 + 2x - 8 = (x+4)(x-2)\)."},
     {"pre": "The bracket x + 4 is zero when x = ", "post": "", "answer": -4, "hint": "x + 4 = 0, so x is negative."},
     {"pre": "The bracket x - 2 is zero when x = ", "post": "", "answer": 2, "hint": "x - 2 = 0."},
     {"say": r"The roots are \(-4\) and 2. The sign is \(\geq 0\), so we want where the U-shape is ON or ABOVE the axis. That is OUTSIDE the roots, not between them."},
     {"pre": "The left piece is x ≤ ", "post": "", "answer": -4, "hint": "On or below the smaller root."},
     {"pre": "The right piece is x ≥ ", "post": "", "answer": 2, "hint": "On or above the larger root."},
     {"pre": "Check a value outside, x = 3:  3² + 2(3) - 8 = ", "post": "", "answer": 7, "done": "Above zero, so the outside region is right. Taking OUTSIDE the roots for a greater-than-or-equal sign is the new silver move.", "hint": "9 + 6 - 8. It should be zero or above."},
  ], "display": svg_s + CAP + r"Solve \(x^2 + 2x - 8 \geq 0\)"},
  "gold": {"steps": [
     {"say": r"With a 2 in front of \(x^2\), split the middle term. Two numbers multiply to \((2)(-6) = -12\) and add to \(+1\): they are \(+4\) and \(-3\). Grouping gives \(2x^2 + 4x - 3x - 6 = 2x(x+2) - 3(x+2) = (2x-3)(x+2)\)."},
     {"pre": "From x + 2 = 0:  x = ", "post": "", "answer": -2, "hint": "x = -2."},
     {"pre": "From 2x - 3 = 0, first 2x = ", "post": "", "answer": 3, "hint": "Add 3 to both sides."},
     {"pre": "So x = 3 ÷ 2 = ", "post": "", "answer": 1.5, "hint": "Divide by 2; it is a fraction."},
     {"say": r"The roots are \(-2\) and 1.5. The sign is \(> 0\), so we want the U-shape ABOVE the axis: OUTSIDE the roots, \(x < -2\) or \(x > 1.5\)."},
     {"pre": "The lower root, the left bound, is ", "post": "", "answer": -2, "hint": "The smaller root."},
     {"pre": "Check x = 2, outside on the right:  2(2²) + 2 - 6 = ", "post": "", "answer": 4, "done": "Above zero, so x < -2 or x > 1.5 is right. Splitting the middle term when x² has a coefficient is the gold move.", "hint": "8 + 2 - 6. It should be above zero."},
  ], "display": svg_g + CAP + r"Solve \(2x^2 + x - 6 > 0\)"},
}

pd["guided"] = {"opener": opener, "teach": teach}

# ---------------------------------------------------------------------------
# 3. TIER GUIDES
# ---------------------------------------------------------------------------

pd["tier_guides"] = {
  "bronze": {
    "title": "Bronze: reading between or outside the roots",
    "steps": [
      r"Find the two roots. For a difference of squares (\(x^2 = k\) gives \(x = \pm\sqrt{k}\)), or read a root off each bracket of a factorised pair.",
      r"Sketch the U-shape crossing at the roots. For \(< 0\) or \(\leq 0\) take BETWEEN the roots; for \(> 0\) or \(\geq 0\) take OUTSIDE them.",
      r"Write both bounds: a between answer is \(a < x < b\); an outside answer is \(x < a\) or \(x > b\).",
    ],
    "example": {
      "question": r"Solve \(x^2 - 49 < 0\). Give the upper bound.",
      "steps": [
        {"label": "Find roots", "content": r"\(x^2 = 49\), so \(x = \pm 7\)."},
        {"label": "Choose the region", "content": r"\(< 0\) means between the roots: \(-7 < x < 7\)."},
        {"label": "Check", "content": r"At \(x = 0\): \(0 - 49 = -49\), below zero. Correct."},
        {"label": "Answer", "content": r"The upper bound is \(7\).", "isAnswer": True, "is_answer": True},
      ]}},
  "silver": {
    "title": r"Silver: below and above zero, including \(\leq\) and \(\geq\)",
    "steps": [
      "Factorise the three-term quadratic to find the two roots.",
      r"For \(< 0\) or \(\leq 0\) the curve is below the axis BETWEEN the roots; for \(> 0\) or \(\geq 0\) it is above OUTSIDE them.",
      r"Use \(\leq\) or \(\geq\) for closed bounds when the sign includes equals; for a count, list the integers inside the range.",
    ],
    "example": {
      "question": r"Solve \(x^2 - x - 12 > 0\). Give the smaller critical value.",
      "steps": [
        {"label": "Factorise", "content": r"\((x-4)(x+3) = 0\), roots \(-3\) and \(4\)."},
        {"label": "Choose the region", "content": r"\(> 0\) means outside the roots: \(x < -3\) or \(x > 4\)."},
        {"label": "Check", "content": r"At \(x = 5\): \(25 - 5 - 12 = 8 > 0\). Correct."},
        {"label": "Answer", "content": r"The smaller critical value is \(-3\).", "isAnswer": True, "is_answer": True},
      ]}},
  "gold": {
    "title": r"Gold: rearranging, \(a \neq 1\), discriminants and combined conditions",
    "steps": [
      r"Rearrange so one side is 0 first; if you multiply by \(-1\), flip the inequality sign.",
      r"When \(x^2\) has a coefficient, split the middle term to factorise; roots may be fractions.",
      r"For a no-real-roots question use the discriminant \(b^2 - 4ac < 0\); for a combined condition, solve each part then take the overlap.",
    ],
    "example": {
      "question": r"Solve \(3x^2 - 5x - 2 \leq 0\). Give the smaller critical value.",
      "steps": [
        {"label": "Split the middle term", "content": r"\(3x^2 - 5x - 2 = (3x+1)(x-2)\), roots \(-\tfrac{1}{3}\) and \(2\)."},
        {"label": "Choose the region", "content": r"\(\leq 0\) means between the roots: \(-\tfrac{1}{3} \leq x \leq 2\)."},
        {"label": "Check", "content": r"At \(x = 0\): \(0 - 0 - 2 = -2 \leq 0\). Correct."},
        {"label": "Answer", "content": r"The smaller critical value is \(-\tfrac{1}{3}\).", "isAnswer": True, "is_answer": True},
      ]}},
}

# ---------------------------------------------------------------------------
# 4. METHOD CARD  (slim reference)
# ---------------------------------------------------------------------------

pd["method_card"] = {
  "title": "Solving Quadratic Inequalities",
  "steps": [
    "Rearrange so one side is 0, then factorise to find the two roots.",
    r"Sketch the U-shape (positive \(x^2\)) crossing the x-axis at the roots.",
    r"For \(< 0\) or \(\leq 0\) take BETWEEN the roots; for \(> 0\) or \(\geq 0\) take OUTSIDE them.",
    r"Use \(\leq\) or \(\geq\) for an inclusive sign, \(<\) or \(>\) for a strict one.",
  ],
  "content": r"<p>A <strong>quadratic inequality</strong> asks which values of \(x\) make a quadratic above or below zero. Solve the matching equation for the roots, sketch the parabola, then read off the region.</p><p><strong>Below zero</strong> (\(< 0\), \(\leq 0\)) sits between the roots; <strong>above zero</strong> (\(> 0\), \(\geq 0\)) sits outside them.</p>",
  "example": r"<p><strong>Solve</strong> \(x^2 - 5x + 6 < 0\).</p><p>\((x-2)(x-3) = 0\) gives roots \(2\) and \(3\). Below zero is between the roots, so \(2 < x < 3\).</p>",
}

# topic_links / related_videos preserved as-is from live.
# worked_examples: fix em dashes in step labels (hard style rule + validator).
for we in pd.get("worked_examples") or []:
    for st in we.get("steps") or []:
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, io.open("lesson_maths-ocr_algebra-L12.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_maths-ocr_algebra-L12.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
