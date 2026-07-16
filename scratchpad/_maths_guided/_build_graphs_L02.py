# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_graphs_L02.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {}
    if say is not None: d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    if phase: d["phase"] = phase
    if done: d["done"] = done
    d["hint"] = hint
    return d

def sayonly(say, phase=None):
    d = {"say": say}
    if phase: d["phase"] = phase
    return d

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

# ---------------- BRONZE ----------------
bronze = []

# B0 (NEW: substitution, replaces triple read-off)
bronze.append({
 "display": r"A line has gradient 3 and passes through \((2, 10)\). Find \(c\).",
 "solutions": [4], "calculator": False, "input_type": "single_value",
 "hint": "Put the point into y = 3x + c, then subtract to find c.",
 "misconceptions": [mc("substitution_error", 16,
   r"Substitute and subtract the mx part: \(10 = 3(2) + c\) gives \(c = 10 - 6 = 4\). Adding the 6 instead gives 16.")],
 "guided_steps": [
   sayonly(r"The gradient is given, \(m = 3\), so the line is \(y = 3x + c\). Substitute the point \((2, 10)\):"),
   box("3 × 2 = ", 6, "gradient × x-coordinate."),
   sayonly("So 10 = 6 + c."),
   box("10 − 6 = c, so c = ", 4, "Take the 6 across: 10 − 6.", phase="substitute"),
   box("Check: 3 × 2 + 4 = ", 10, "It must give the y-coordinate 10.", phase="substitute",
       done="It returns 10, the point's y-value, so c = 4 is right."),
 ]})

# B1
bronze.append({
 "display": r"A line has gradient 4 and passes through \((1, 6)\). Find the value of \(c\).",
 "solutions": [2], "calculator": False, "input_type": "single_value",
 "hint": "Substitute (1, 6) into y = 4x + c and solve for c.",
 "misconceptions": [mc("substitution_error", 10,
   r"\(6 = 4(1) + c\) means \(c = 6 - 4 = 2\). Adding gives 10, the slip.")],
 "guided_steps": [
   sayonly(r"The gradient is given, \(m = 4\), so the line is \(y = 4x + c\). Substitute the point \((1, 6)\):"),
   box("4 × 1 = ", 4, "gradient × x-coordinate."),
   sayonly("So 6 = 4 + c."),
   box("6 − 4 = c, so c = ", 2, "Take the 4 across: 6 − 4.", phase="substitute"),
   box("Check: 4 × 1 + 2 = ", 6, "It must give 6.", phase="substitute",
       done="It returns 6, the point's y-value, so c = 2 is right."),
 ]})

# B2 (point changed (0,-3) -> (2,1) to remove degeneracy)
bronze.append({
 "display": r"A line has gradient 2 and passes through \((2, 1)\). Find the y-intercept \(c\).",
 "solutions": [-3], "calculator": False, "input_type": "single_value",
 "hint": "Substitute (2, 1) into y = 2x + c; c can be negative.",
 "misconceptions": [mc("substitution_error", 5,
   r"\(1 = 2(2) + c\) means \(c = 1 - 4 = -3\). Adding the 4 instead gives 5.")],
 "guided_steps": [
   sayonly(r"The gradient is given, \(m = 2\), so the line is \(y = 2x + c\). Substitute the point \((2, 1)\):"),
   box("2 × 2 = ", 4, "gradient × x-coordinate."),
   sayonly("So 1 = 4 + c."),
   box("1 − 4 = c, so c = ", -3, "1 − 4 = −3.", phase="substitute"),
   box("Check: 2 × 2 + (−3) = ", 1, "4 − 3 = 1.", phase="substitute",
       done="It returns 1, matching the point, so c = −3 is right."),
 ]})

# B3
bronze.append({
 "display": r"A line has gradient 1 and passes through \((5, 8)\). Find \(c\).",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Substitute (5, 8) into y = x + c and solve for c.",
 "misconceptions": [mc("substitution_error", 13,
   r"\(8 = 1(5) + c\) means \(c = 8 - 5 = 3\). Adding gives 13.")],
 "guided_steps": [
   sayonly(r"The gradient is given, \(m = 1\), so the line is \(y = x + c\). Substitute the point \((5, 8)\):"),
   box("1 × 5 = ", 5, "gradient × x-coordinate."),
   sayonly("So 8 = 5 + c."),
   box("8 − 5 = c, so c = ", 3, "Take the 5 across: 8 − 5.", phase="substitute"),
   box("Check: 1 × 5 + 3 = ", 8, "It must give 8.", phase="substitute",
       done="It returns 8, so c = 3 is right."),
 ]})

# B4 (read-off gradient, keep)
bronze.append({
 "display": r"Find the gradient of the line with equation \(y = 7x - 2\).",
 "solutions": [7], "calculator": False, "input_type": "single_value",
 "hint": "In y = mx + c, the gradient is the number multiplying x.",
 "misconceptions": [mc("confused_m_and_c", -2,
   r"In \(y = mx + c\) the gradient is the number multiplying x, so \(m = 7\). The −2 is the intercept c, not the gradient.")],
 "guided_steps": [
   sayonly(r"In \(y = mx + c\) the gradient sits with the x and the intercept sits alone. Line up \(y = 7x - 2\) against \(y = mx + c\)."),
   box("The number with x is the gradient. m = ", 7, "It multiplies x."),
   box("The number on its own is the intercept. c = ", -2, "The constant term, with its sign."),
   box("At x = 1: 7 × 1 − 2 = ", 5, "7 − 2.", phase="substitute"),
   box("From x = 0 (y = −2) to x = 1 (y = 5), y climbs 5 − (−2) = ", 7, "5 minus −2.", phase="substitute",
       done="y rose by 7 as x rose by 1, confirming the gradient is 7."),
 ]})

# B5
bronze.append({
 "display": r"A line has gradient \(-1\) and passes through \((2, 3)\). Find \(c\).",
 "solutions": [5], "calculator": False, "input_type": "single_value",
 "hint": "Substitute (2, 3) into y = −x + c; mind the sign of −1 × 2.",
 "misconceptions": [mc("sign_error", 1,
   r"\(-1 \times 2 = -2\), so \(3 = -2 + c\) and \(c = 3 + 2 = 5\). Treating it as +2 and subtracting gives 1, the sign slip.")],
 "guided_steps": [
   sayonly(r"The gradient is given, \(m = -1\), so the line is \(y = -x + c\). Substitute the point \((2, 3)\):"),
   box("−1 × 2 = ", -2, "Negative one times 2, keep the minus."),
   sayonly("So 3 = −2 + c."),
   box("3 − (−2) = c, so c = ", 5, "Subtracting −2 adds 2: 3 + 2 = 5.", phase="substitute"),
   box("Check: −1 × 2 + 5 = ", 3, "−2 + 5 = 3.", phase="substitute",
       done="It returns 3, matching the point, so c = 5 is right."),
 ]})

# B6 (point changed (4,5)->(4,8) to make answer unique)
bronze.append({
 "display": r"A line has gradient \(\frac{1}{2}\) and passes through \((4, 8)\). Find \(c\).",
 "solutions": [6], "calculator": False, "input_type": "single_value",
 "hint": "Substitute (4, 8) into y = ½x + c and solve for c.",
 "misconceptions": [mc("substitution_error", 10,
   r"\(\frac{1}{2} \times 4 = 2\), so \(8 = 2 + c\) and \(c = 8 - 2 = 6\). Adding gives 10.")],
 "guided_steps": [
   sayonly(r"The gradient is given, \(m = \frac{1}{2}\), so the line is \(y = \frac{1}{2}x + c\). Substitute the point \((4, 8)\):"),
   box("½ × 4 = ", 2, "Half of 4 is 2."),
   sayonly("So 8 = 2 + c."),
   box("8 − 2 = c, so c = ", 6, "Take the 2 across: 8 − 2.", phase="substitute"),
   box("Check: ½ × 4 + 6 = ", 8, "2 + 6 = 8.", phase="substitute",
       done="It returns 8, so c = 6 is right."),
 ]})

# B7 (read-off intercept, keep)
bronze.append({
 "display": r"What is the y-intercept of the line \(y = -5x + 12\)?",
 "solutions": [12], "calculator": False, "input_type": "single_value",
 "hint": "The y-intercept is the constant term at the end.",
 "misconceptions": [mc("confused_m_and_c", -5,
   r"The y-intercept is the constant term \(c = 12\). The −5 is the gradient m, the number with x.")],
 "guided_steps": [
   sayonly(r"In \(y = mx + c\) the intercept c sits alone and the gradient m sits with x. Line up \(y = -5x + 12\) against \(y = mx + c\)."),
   box("The number with x is the gradient. m = ", -5, "It multiplies x, keep the minus."),
   box("The number on its own is the intercept. c = ", 12, "The constant term."),
   box("The y-intercept is where x = 0. At x = 0: −5 × 0 = ", 0, "Anything times 0 is 0.", phase="substitute"),
   box("So y = 0 + 12 = ", 12, "0 + 12.", phase="substitute",
       done="The line crosses the y-axis at 12, so the y-intercept is 12."),
 ]})

# ---------------- SILVER ----------------
silver = []

# S0 two-point -> c=0
silver.append({
 "display": r"Find the equation of the line through \((1, 3)\) and \((3, 9)\). What is \(c\)?",
 "solutions": [0], "calculator": False, "input_type": "single_value",
 "hint": "Find the gradient from the two points first, then substitute one point.",
 "misconceptions": [mc("confused_m_and_c", 3,
   r"3 is the gradient m, not c. Once you have \(m = 3\), substitute a point to finish: \(3 = 3(1) + c\), so \(c = 0\).")],
 "guided_steps": [
   sayonly(r"No gradient given, so find it first: rise over run, \((y_2 - y_1) \div (x_2 - x_1)\), using \((1, 3)\) and \((3, 9)\)."),
   box("top: 9 − 3 = ", 6, "Change in y."),
   box("bottom: 3 − 1 = ", 2, "Change in x."),
   box("m = 6 ÷ 2 = ", 3, "Divide rise by run."),
   sayonly(r"Now substitute \((1, 3)\) into \(y = 3x + c\):", phase="substitute"),
   box("3 − 3 × 1 = c, so c = ", 0, "3 − 3 = 0.", phase="substitute"),
   box("Check the other point: 3 × 3 + 0 = ", 9, "It must return 9.", phase="substitute",
       done="It gives 9, matching (3, 9), so c = 0 is right."),
 ]})

# S1 two-point -> c=-5
silver.append({
 "display": r"Find the equation of the line through \((2, 1)\) and \((5, 10)\). What is \(c\)?",
 "solutions": [-5], "calculator": False, "input_type": "single_value",
 "hint": "Work out the gradient with rise over run, then find c.",
 "misconceptions": [mc("substitution_error", 7,
   r"After \(m = 3\), substitute \((2, 1)\): \(1 = 3(2) + c\). Subtract the 6: \(c = 1 - 6 = -5\). Adding it gives +7, the common slip.")],
 "guided_steps": [
   sayonly(r"Find the gradient first from \((2, 1)\) and \((5, 10)\): rise over run."),
   box("top: 10 − 1 = ", 9, "Change in y."),
   box("bottom: 5 − 2 = ", 3, "Change in x."),
   box("m = 9 ÷ 3 = ", 3, "Divide rise by run."),
   sayonly(r"Substitute \((2, 1)\) into \(y = 3x + c\):", phase="substitute"),
   box("3 × 2 = ", 6, "gradient × x-coordinate.", phase="substitute"),
   box("1 − 6 = c, so c = ", -5, "1 − 6 = −5.", phase="substitute"),
   box("Check (5, 10): 3 × 5 + (−5) = ", 10, "15 − 5 = 10.", phase="substitute",
       done="15 − 5 = 10, matching (5, 10), so c = −5 is right."),
 ]})

# S2 (NEW: two-point, fractional gradient) -> c=1
silver.append({
 "display": r"Find the equation of the line through \((2, 2)\) and \((6, 4)\). What is \(c\)?",
 "solutions": [1], "calculator": False, "input_type": "single_value",
 "hint": "The gradient is a fraction here: rise over run, then find c.",
 "misconceptions": [mc("reversed_gradient", -2,
   r"Gradient is rise over run: \((4 - 2) \div (6 - 2) = \frac{2}{4} = \frac{1}{2}\), not 2. Reversing it to run over rise gives \(m = 2\) and a wrong c of −2.")],
 "guided_steps": [
   sayonly(r"Find the gradient first from \((2, 2)\) and \((6, 4)\). The rise is smaller than the run, so expect a fraction: rise over run."),
   box("top: 4 − 2 = ", 2, "Change in y."),
   box("bottom: 6 − 2 = ", 4, "Change in x."),
   box("m = 2 ÷ 4 = ", 0.5, "2 ÷ 4 = 0.5, or one half."),
   sayonly(r"Substitute \((2, 2)\) into \(y = 0.5x + c\):", phase="substitute"),
   box("0.5 × 2 = ", 1, "Half of 2 is 1.", phase="substitute"),
   box("2 − 1 = c, so c = ", 1, "2 − 1 = 1.", phase="substitute"),
   box("Check (6, 4): 0.5 × 6 + 1 = ", 4, "3 + 1 = 4.", phase="substitute",
       done="3 + 1 = 4, matching (6, 4), so c = 1 is right."),
 ]})

# S3 gradient only -> -1
silver.append({
 "display": r"Find the gradient of the line through \((0, 4)\) and \((6, -2)\).",
 "solutions": [-1], "calculator": False, "input_type": "single_value",
 "hint": "Gradient only: divide the change in y by the change in x.",
 "misconceptions": [mc("sign_error", 1,
   r"\(m = (-2 - 4) \div (6 - 0) = \frac{-6}{6} = -1\). Dropping the minus gives +1, but the line falls, so the gradient is negative.")],
 "guided_steps": [
   sayonly(r"This one only wants the gradient: rise over run from \((0, 4)\) and \((6, -2)\)."),
   box("top: −2 − 4 = ", -6, "Change in y: −2 minus 4."),
   box("bottom: 6 − 0 = ", 6, "Change in x."),
   sayonly("Now divide, and mind the sign:", phase="substitute"),
   box("−6 ÷ 6 = ", -1, "A negative divided by a positive is negative.", phase="substitute"),
   box("Check by climbing: from (0, 4) to (6, −2), y falls 6 as x rises 6, a change of ", -1,
       "−6 over 6 is −1 per unit.", phase="substitute",
       done="y changes by −1 for each step in x, confirming the gradient is −1."),
 ]})

# S4 gradient only -> 2
silver.append({
 "display": r"A line passes through \((4, 3)\) and \((-2, -9)\). Find the gradient.",
 "solutions": [2], "calculator": False, "input_type": "single_value",
 "hint": "Gradient only: a negative over a negative is positive.",
 "misconceptions": [mc("sign_error", -2,
   r"\(m = (-9 - 3) \div (-2 - 4) = \frac{-12}{-6} = 2\). A negative over a negative is positive; keeping only one minus gives −2.")],
 "guided_steps": [
   sayonly(r"Gradient only: rise over run from \((4, 3)\) and \((-2, -9)\). Keep the order the same top and bottom."),
   box("top: −9 − 3 = ", -12, "Change in y: −9 minus 3."),
   box("bottom: −2 − 4 = ", -6, "Change in x: −2 minus 4."),
   sayonly("Now divide, two negatives:", phase="substitute"),
   box("−12 ÷ (−6) = ", 2, "A negative divided by a negative is positive.", phase="substitute"),
   box("Check: from (−2, −9) to (4, 3), y rises 12 as x rises 6, a climb of ", 2,
       "12 over 6 is 2.", phase="substitute",
       done="y climbs 2 for each step in x, so the gradient is 2."),
 ]})

# S5 parallel -> 8
silver.append({
 "display": r"Line P has equation \(y = -3x + 2\). Line Q is parallel to P and passes through \((1, 5)\). What is the y-intercept of Q?",
 "solutions": [8], "calculator": False, "input_type": "single_value",
 "hint": "Copy the gradient of P, then use the point to find Q's intercept.",
 "misconceptions": [mc("parallel_error", 2,
   r"Parallel means the same gradient, −3, but the intercept is your own to find. Using \((1, 5)\): \(5 = -3(1) + c\) gives \(c = 8\), not the 2 copied from line P.")],
 "guided_steps": [
   sayonly(r"Parallel lines share a gradient. Read P's gradient from \(y = -3x + 2\):"),
   box("m = ", -3, "The number with x in line P, minus and all."),
   sayonly(r"Q has the same gradient, so \(y = -3x + c\). Substitute \((1, 5)\):"),
   box("−3 × 1 = ", -3, "−3 times 1."),
   sayonly("So 5 = −3 + c.", phase="substitute"),
   box("5 − (−3) = c, so c = ", 8, "Subtracting −3 adds 3: 5 + 3 = 8.", phase="substitute"),
   box("Check (1, 5): −3 × 1 + 8 = ", 5, "−3 + 8 = 5.", phase="substitute",
       done="−3 + 8 = 5, matching (1, 5), so the y-intercept is 8."),
 ]})

# S6 rearrange -> gradient 3
silver.append({
 "display": r"The equation of a line is \(3y = 9x - 6\). Find the gradient.",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Divide the whole equation by 3 before reading the gradient.",
 "misconceptions": [mc("forgot_step", 9,
   r"Divide every term by 3 first: \(3y = 9x - 6\) becomes \(y = 3x - 2\). The gradient is 3, not the 9 from the unsimplified equation.")],
 "guided_steps": [
   sayonly(r"The equation is not yet in \(y = mx + c\) form. Divide every term by 3 to get y alone."),
   box("9x ÷ 3 = ", 3, "9 ÷ 3.", post="x"),
   box("−6 ÷ 3 = ", -2, "−6 ÷ 3, keep the minus."),
   sayonly(r"So \(y = 3x - 2\). Read off the gradient:", phase="substitute"),
   box("the number with x is m = ", 3, "It multiplies x.", phase="substitute"),
   box("In y = 3x − 2, at x = 1: 3 × 1 − 2 = ", 1, "3 − 2 = 1.", phase="substitute",
       done="The original at x = 1 gives 3y = 3, so y = 1 too; the form y = 3x − 2 is right and m = 3."),
 ]})

# ---------------- GOLD ----------------
gold = []

# G0 two-point with negatives -> c=3
gold.append({
 "display": r"Find the equation of the line through \((-1, 5)\) and \((3, -3)\). What is \(c\)?",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Find the gradient carefully across the negatives, then find c.",
 "misconceptions": [mc("sign_error", 1,
   r"The denominator is \(3 - (-1) = 4\), not 2. With \(m = \frac{-8}{4} = -2\) and the point \((-1, 5)\): \(5 = -2(-1) + c\) gives \(c = 3\). Using 2 gives \(m = -4\) and \(c = 1\).")],
 "guided_steps": [
   sayonly(r"Find the gradient first from \((-1, 5)\) and \((3, -3)\). Watch the double negatives."),
   box("top: −3 − 5 = ", -8, "Change in y: −3 minus 5."),
   box("bottom: 3 − (−1) = ", 4, "Subtracting −1 adds 1: 3 + 1."),
   box("m = −8 ÷ 4 = ", -2, "−8 over 4."),
   sayonly(r"Substitute \((-1, 5)\) into \(y = -2x + c\):", phase="substitute"),
   box("−2 × (−1) = ", 2, "Negative times negative is positive.", phase="substitute"),
   box("5 − 2 = c, so c = ", 3, "5 − 2 = 3.", phase="substitute"),
   box("Check (3, −3): −2 × 3 + 3 = ", -3, "−6 + 3 = −3.", phase="substitute",
       done="−6 + 3 = −3, matching (3, −3), so c = 3 is right."),
 ]})

# G1 perpendicular -> c=5
gold.append({
 "display": r"A line is perpendicular to \(y = 2x + 1\) and passes through \((4, 3)\). Find \(c\).",
 "solutions": [5], "calculator": False, "input_type": "single_value",
 "hint": "Use the perpendicular gradient −1/2, then substitute the point.",
 "misconceptions": [mc("perpendicular_error", -5,
   r"Perpendicular gradient is \(-\frac{1}{m} = -\frac{1}{2}\), not 2. Using \(-\frac{1}{2}\): \(3 = -\frac{1}{2}(4) + c\) gives \(c = 5\). Using the original 2 gives −5.")],
 "guided_steps": [
   sayonly(r"The given gradient is 2. The perpendicular gradient is its negative reciprocal: flip and change sign."),
   box("perpendicular m = −1 ÷ 2 = ", -0.5, "−1 divided by 2 is −0.5."),
   sayonly(r"So the line is \(y = -0.5x + c\). Substitute \((4, 3)\):"),
   box("−0.5 × 4 = ", -2, "Half of 4 is 2, negative."),
   sayonly("So 3 = −2 + c.", phase="substitute"),
   box("3 − (−2) = c, so c = ", 5, "3 + 2 = 5.", phase="substitute"),
   box("Check (4, 3): −0.5 × 4 + 5 = ", 3, "−2 + 5 = 3.", phase="substitute",
       done="−2 + 5 = 3, matching (4, 3), so c = 5 is right."),
 ]})

# G2 find m -> -3
gold.append({
 "display": r"The line \(y = mx + 4\) passes through \((-2, 10)\). Find \(m\).",
 "solutions": [-3], "calculator": False, "input_type": "single_value",
 "hint": "Substitute the point into y = mx + 4 and solve for m.",
 "misconceptions": [mc("sign_error", 3,
   r"\(10 = -2m + 4\) gives \(-2m = 6\), so \(m = 6 \div (-2) = -3\). Dropping the minus gives +3.")],
 "guided_steps": [
   sayonly(r"Here c is known (4) and m is missing. Substitute \((-2, 10)\) into \(y = mx + 4\), so \(10 = m \times (-2) + 4\)."),
   box("Take the 4 across: 10 − 4 = ", 6, "10 − 4."),
   sayonly("So −2m = 6. Divide by −2:", phase="substitute"),
   box("6 ÷ (−2) = m = ", -3, "A positive divided by a negative is negative.", phase="substitute"),
   box("Check: −3 × (−2) + 4 = ", 10, "6 + 4 = 10.", phase="substitute",
       done="6 + 4 = 10, matching the point, so m = −3 is right."),
 ]})

# G3 (reworded: perpendicular through the point, find c) -> c=-2
gold.append({
 "display": r"Find the equation of the line perpendicular to \(y = -\frac{1}{3}x + 2\) that passes through \((3, 7)\). What is \(c\)?",
 "solutions": [-2], "calculator": False, "input_type": "single_value",
 "hint": "Flip and negate −1/3 to get the gradient, then find c.",
 "misconceptions": [mc("perpendicular_error", 8,
   r"The perpendicular gradient is the negative reciprocal of \(-\frac{1}{3}\), which is 3, not \(-\frac{1}{3}\). With \(m = 3\): \(7 = 3(3) + c\) gives \(c = -2\). Using \(-\frac{1}{3}\) gives 8.")],
 "guided_steps": [
   sayonly(r"The given gradient is \(-\frac{1}{3}\). The perpendicular gradient is the negative reciprocal: flip \(-\frac{1}{3}\) to −3, then change the sign to +3."),
   box("perpendicular m = ", 3, "Negative reciprocal of −1/3 is 3."),
   sayonly(r"So the line is \(y = 3x + c\). Substitute \((3, 7)\):"),
   box("3 × 3 = ", 9, "gradient × x-coordinate."),
   sayonly("So 7 = 9 + c.", phase="substitute"),
   box("7 − 9 = c, so c = ", -2, "7 − 9 = −2.", phase="substitute"),
   box("Check (3, 7): 3 × 3 + (−2) = ", 7, "9 − 2 = 7.", phase="substitute",
       done="9 − 2 = 7, matching (3, 7), so c = −2 is right."),
 ]})

# G4 midpoint -> c=9
gold.append({
 "display": r"The midpoint of \(A(1, 2)\) and \(B(5, 10)\) lies on the line \(y = mx + c\) with gradient \(-1\). Find \(c\).",
 "solutions": [9], "calculator": False, "input_type": "single_value",
 "hint": "Find the midpoint first, then substitute it with gradient −1.",
 "misconceptions": [mc("midpoint_error", 18,
   r"The midpoint halves each sum: \((\frac{1+5}{2}, \frac{2+10}{2}) = (3, 6)\). Forgetting to divide by 2 gives \((6, 12)\) and \(c = 18\). With \((3, 6)\): \(6 = -1(3) + c\), so \(c = 9\).")],
 "guided_steps": [
   sayonly(r"First find the midpoint of \(A(1, 2)\) and \(B(5, 10)\): average the x's and average the y's."),
   box("midpoint x: (1 + 5) ÷ 2 = ", 3, "Average the x-coordinates."),
   box("midpoint y: (2 + 10) ÷ 2 = ", 6, "Average the y-coordinates."),
   sayonly(r"So the midpoint is \((3, 6)\). The gradient is given as −1, so \(y = -x + c\). Substitute \((3, 6)\):", phase="substitute"),
   box("−1 × 3 = ", -3, "−1 times 3.", phase="substitute"),
   box("6 − (−3) = c, so c = ", 9, "6 + 3 = 9.", phase="substitute"),
   box("Check: at x = 3, −1 × 3 + 9 = ", 6, "−3 + 9 = 6.", phase="substitute",
       done="−3 + 9 = 6, the midpoint's y-value, so c = 9 is right."),
 ]})

# ---------------- tier_guides ----------------
tier_guides = {
 "bronze": {
   "title": "Bronze: you are told the gradient",
   "steps": [
     r"You are given the gradient m. Read m and the intercept c straight off an equation like \(y = 7x - 2\) (m = 7, c = −2).",
     r"Given m and a point instead? Put the point into \(y = mx + c\) and solve for c: take the mx part away from the y-value.",
     r"Write the full line \(y = mx + c\), then check the point fits."
   ],
   "example": {
     "question": "A line has gradient 4 and passes through (1, 6). Find c.",
     "steps": [
       {"label": "Substitute", "content": r"<p>\(6 = 4(1) + c\)</p>"},
       {"label": "Solve", "content": r"<p>\(6 = 4 + c\) → \(c = 2\)</p>"},
       {"label": "Check", "content": r"<p>\(4(1) + 2 = 6\) ✓</p>"},
       {"label": "Answer", "content": r"<p>\(c = 2\), so \(y = 4x + 2\)</p>", "isAnswer": True, "is_answer": True},
     ]
   }
 },
 "silver": {
   "title": "Silver: find the gradient first",
   "steps": [
     r"The gradient is not handed to you. Build it: from two points use rise over run, \(m = (y_2 - y_1) \div (x_2 - x_1)\).",
     r"Parallel lines share a gradient; a tilted equation like \(3y = 9x - 6\) must be divided through to reach \(y = mx + c\).",
     r"Once you have m, it is a Bronze question: substitute a point and solve for c."
   ],
   "example": {
     "question": "Find the equation of the line through (1, 3) and (3, 9). Find c.",
     "steps": [
       {"label": "Gradient", "content": r"<p>\(m = \frac{9 - 3}{3 - 1} = \frac{6}{2} = 3\)</p>"},
       {"label": "Substitute", "content": r"<p>\(3 = 3(1) + c\)</p>"},
       {"label": "Solve", "content": r"<p>\(c = 0\)</p>"},
       {"label": "Check", "content": r"<p>\(3(3) + 0 = 9\) ✓</p>"},
       {"label": "Answer", "content": r"<p>\(c = 0\), so \(y = 3x\)</p>", "isAnswer": True, "is_answer": True},
     ]
   }
 },
 "gold": {
   "title": "Gold: perpendicular and hidden points",
   "steps": [
     r"Perpendicular gradients are negative reciprocals: flip the fraction and change the sign, so 2 becomes \(-\frac{1}{2}\) and \(-\frac{1}{3}\) becomes 3.",
     r"Some questions hide the point: find a midpoint by averaging coordinates first, or rearrange to get m.",
     r"After the twist, finish the Bronze way: substitute a point and solve for c."
   ],
   "example": {
     "question": "A line is perpendicular to y = 2x + 1 and passes through (4, 3). Find c.",
     "steps": [
       {"label": "Perpendicular gradient", "content": r"<p>\(-\frac{1}{m} = -\frac{1}{2}\)</p>"},
       {"label": "Substitute", "content": r"<p>\(-\frac{1}{2}(4) + c = 3\)</p>"},
       {"label": "Solve", "content": r"<p>\(-2 + c = 3\) → \(c = 5\)</p>"},
       {"label": "Check", "content": r"<p>\(-\frac{1}{2}(4) + 5 = 3\) ✓</p>"},
       {"label": "Answer", "content": r"<p>\(c = 5\), so \(y = -\frac{1}{2}x + 5\)</p>", "isAnswer": True, "is_answer": True},
     ]
   }
 }
}

# ---------------- guided (opener + teach) ----------------
guided = {
 "opener": {
   "label": "Before any algebra",
   "display": "Taxi fare<br>£3 to get in, then £2 for every mile",
   "steps": [
     box("A 4-mile trip costs £", 11,
         "Start at £3, then add £2 for each of the 4 miles: 3 + 2 + 2 + 2 + 2.",
         say="A taxi puzzle. No formulas, just common sense."),
     box("Before you travel any miles, the fare is £", 3,
         "Zero miles means no mileage charge yet, just the fixed charge to get in.",
         say="You just used a <strong>rate</strong> (£2 each mile) on top of a <strong>start</strong> (£3). Now the other way:"),
     sayonly(r"That fixed £3 is the <strong>y-intercept</strong> \(c\), the cost when \(x = 0\). The £2 per mile is the <strong>gradient</strong> \(m\), how much \(y\) climbs each step. The rule cost \(= 2 \times\) miles \(+ 3\) is exactly \(y = 2x + 3\). Finding a line's equation just means finding its start \(c\) and its rate \(m\)."),
   ]
 },
 "teach": {
   "bronze": {
     "display": r"A line has gradient 5 and passes through \((2, 13)\). Find its equation \(y = mx + c\).",
     "label": "Together: your first one",
     "steps": [
       box("The gradient is given. m = ", 5, "It is stated in the question.",
           say=r"When the gradient is handed to you, only c is missing. Read it first:"),
       box("5 × 2 = ", 10, "gradient × x-coordinate.",
           say=r"So the line is \(y = 5x + c\). Substitute the point \((2, 13)\), so x = 2 and y = 13:"),
       box("13 − 10 = c, so c = ", 3, "Take the 10 across: 13 − 10.",
           say="So 13 = 10 + c.", done="That is the whole Bronze move: one substitution, one subtraction."),
       box("Check: 5 × 2 + 3 = ", 13, "It must give the y-coordinate 13.",
           say=r"The equation is \(y = 5x + 3\). Check it against the point:",
           done="It returns 13, matching (2, 13), so c = 3 is right."),
     ]
   },
   "silver": {
     "display": r"Find the equation of the line through \((1, 1)\) and \((4, 10)\).",
     "label": "Together: the silver move",
     "steps": [
       box("top: 10 − 1 = ", 9, "The change in y.",
           say=r"Nothing is given this time. The silver move is to find the gradient yourself: rise over run, \((y_2 - y_1) \div (x_2 - x_1)\)."),
       box("bottom: 4 − 1 = ", 3, "The change in x."),
       box("gradient m = 9 ÷ 3 = ", 3, "Divide the rise by the run.",
           done="There it is: the gradient you had to build yourself."),
       box("1 − 3 × 1 = c, so c = ", -2, "1 − 3 = −2.",
           say=r"Now it is a Bronze question. Substitute \((1, 1)\) into \(y = 3x + c\):"),
       box("Check the other point: 3 × 4 − 2 = ", 10, "It must return 10.",
           say=r"The equation is \(y = 3x - 2\). Check \((4, 10)\):",
           done="It gives 10, matching (4, 10), so the line is right."),
     ]
   },
   "gold": {
     "display": r"Find the equation of the line perpendicular to \(y = 2x + 5\) that passes through \((4, 1)\).",
     "label": "Together: the gold move",
     "steps": [
       box("Perpendicular gradient = −1 ÷ 2 = ", -0.5, "−1 divided by 2 is −0.5, or −½.",
           say=r"The gold move is the perpendicular gradient: flip the number over and change its sign (the negative reciprocal). The given gradient is 2."),
       box("−0.5 × 4 = ", -2, "Half of 4 is 2, and it is negative.",
           say=r"So the new line is \(y = -0.5x + c\). Substitute \((4, 1)\):"),
       box("1 − (−2) = c, so c = ", 3, "1 + 2 = 3.",
           say="So 1 = −2 + c.",
           done="The negative reciprocal was the only new idea; the rest is the Bronze substitution."),
       box("Check the point: −0.5 × 4 + 3 = ", 1, "It must give the y-coordinate 1.",
           say=r"The equation is \(y = -0.5x + 3\). Check \((4, 1)\):",
           done="It returns 1, matching (4, 1), so c = 3 is right."),
     ]
   }
 }
}

# ---------------- method_card (slim) ----------------
method_card = {
 "title": "Finding the Equation of a Line",
 "steps": [
   r"Read m (with the x) and c (alone) straight from \(y = mx + c\).",
   r"No gradient? Find it: two points give \(m = (y_2 - y_1) \div (x_2 - x_1)\); parallel lines copy it; perpendicular flips and negates it.",
   r"Substitute a known point into \(y = mx + c\) and solve for c.",
   r"Write \(y = mx + c\) and check the point fits."
 ],
 "content": r"<p>Every straight line is <strong>\(y = mx + c\)</strong>, a steady rate m (the gradient) plus a start value c (the y-intercept).</p><p>If m is given, substitute a point to find c. If not, build m first: rise over run from two points, the same gradient as a parallel line, or the negative reciprocal for a perpendicular one. Then substitute and solve for c as before.</p>",
 "example": r"<p><strong>Line through \((1, 4)\) and \((3, 10)\).</strong> Gradient \(m = \frac{10 - 4}{3 - 1} = 3\). Substitute \((1, 4)\): \(4 = 3(1) + c\), so \(c = 1\). Answer: \(y = 3x + 1\). Check: \(3(3) + 1 = 10\) ✓</p>"
}

# ---------------- worked_examples (preserve, fix em dashes only) ----------------
worked_examples = json.loads(json.dumps(live["worked_examples"]))
for ex in worked_examples:
    for st in ex["steps"]:
        st["label"] = st["label"].replace(" — ", ": ")

# ---------------- assemble ----------------
out = {
 "method_card": method_card,
 "topic_links": live["topic_links"],
 "problem_bank": {
   "bronze": bronze,
   "bronze_description": "You are given the gradient. Read m and c off the equation, or substitute one point into y = mx + c to find c.",
   "silver": silver,
   "silver_description": "The gradient is hidden. Find it from two points, a parallel line, or by rearranging, then find c.",
   "gold": gold,
   "gold_description": "Perpendicular gradients, midpoints, and finding m: an extra twist before the usual substitution.",
 },
 "related_videos": live["related_videos"],
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

json.dump(out, io.open("lesson_graphs-L02.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_graphs-L02.json")
