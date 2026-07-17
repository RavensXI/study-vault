# -*- coding: utf-8 -*-
"""Build guided-learning + diagrams practice_data for maths-ocr algebra-L11 (Inequalities)."""
import json, io

MINUS = "−"  # unicode minus for student-facing text

live = json.load(io.open("_ocrL11_live.json", encoding="utf-8"))

# ---- preserved fields ----
def de_emdash(obj):
    if isinstance(obj, dict):
        return {k: de_emdash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [de_emdash(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ": ")
    return obj

# worked_examples carry em dashes from the original board pipeline; the house
# style + validator forbid them. Minimal, non-mathematical repair: swap em
# dashes for colons in the preserved labels/text. Nothing else is touched.
worked_examples = de_emdash(live.get("worked_examples") or [])
related_videos = live.get("related_videos") or []
topic_links = live.get("topic_links") or {"prerequisites": []}


def numberline(axis_min, axis_max, lo, lo_closed, hi, hi_closed, label):
    """Return a lean, theme-safe number-line SVG marking lo..hi."""
    W, H = 260, 62
    m = 16
    span = axis_max - axis_min
    plot = W - 2 * m

    def X(v):
        return m + (v - axis_min) / span * plot

    y = 30
    parts = []
    parts.append(
        '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
        'style="max-width:280px;font-family:Inter,sans-serif">' % (W, H, label))
    # highlighted segment
    parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#60a5fa" '
                 'stroke-width="5" stroke-opacity="0.5" stroke-linecap="round"/>'
                 % (X(lo), y, X(hi), y))
    # main axis
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                 'stroke-width="1.2"/>' % (m - 4, y, W - m + 4, y))
    # ticks + labels
    for v in range(axis_min, axis_max + 1):
        parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" '
                     'stroke-width="1"/>' % (X(v), y - 4, X(v), y + 4))
        txt = (MINUS + str(-v)) if v < 0 else str(v)
        parts.append('<text x="%.1f" y="%d" fill="currentColor" font-size="10" '
                     'text-anchor="middle">%s</text>' % (X(v), y + 18, txt))
    # endpoint circles: closed = filled, open = hollow
    for val, closed in ((lo, lo_closed), (hi, hi_closed)):
        if closed:
            parts.append('<circle cx="%.1f" cy="%d" r="5" fill="currentColor"/>'
                         % (X(val), y))
        else:
            parts.append('<circle cx="%.1f" cy="%d" r="5" fill="none" '
                         'stroke="currentColor" stroke-width="1.6"/>' % (X(val), y))
    parts.append('</svg>')
    return "".join(parts)


# ===================== PROBLEM BANK =====================
def P(display, sol, it, hint, misc, gs):
    d = {"display": display, "solutions": sol, "input_type": it,
         "calculator": False, "hint": hint, "misconceptions": misc}
    if gs is not None:
        d["guided_steps"] = gs
    return d


def m(pattern, expect, message, note):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}


# ---------- BRONZE ----------
bronze = []

# bronze[0]  x+3>7  smallest int = 5
bronze.append(P(
    "Solve \\(x + 3 > 7\\). What is the smallest integer solution?",
    [5], "single_value",
    "Take 3 off both sides, then find the first whole number inside the range.",
    [m("includes_boundary", 4,
       "x > 4 does not include 4 itself, because > is strict. The smallest whole number bigger than 4 is 5. If the sign were ≥, then 4 would count.",
       "Treats > as inclusive: says 4.")],
    [
        {"say": "Solve it just like an equation. Subtract 3 from both sides."},
        {"pre": "7 " + MINUS + " 3 = ", "post": "", "answer": 4,
         "hint": "Take 3 off the right-hand side."},
        {"say": "So x > 4. The answer is every number above 4."},
        {"pre": "x > 4 does not include 4, so the smallest whole number is ", "post": "",
         "answer": 5, "phase": "substitute", "hint": "The first integer above 4."},
        {"pre": "Check: 5 + 3 = ", "post": "", "answer": 8, "phase": "substitute",
         "done": "8 > 7 is true, and 4 + 3 = 7 is not, so 5 is the smallest. Gone.",
         "hint": "Put x = 5 back in."},
    ]))

# bronze[1]  2x-1<9  largest int = 4
bronze.append(P(
    "Solve \\(2x - 1 < 9\\). What is the largest integer solution?",
    [4], "single_value",
    "Add 1, divide by 2, then find the last whole number inside the range.",
    [m("includes_boundary", 5,
       "x < 5 does not include 5, because < is strict. The largest whole number below 5 is 4. Only ≤ would let 5 count.",
       "Treats < as inclusive: says 5.")],
    [
        {"say": "Solve it like an equation. Add 1 to both sides."},
        {"pre": "9 + 1 = ", "post": "", "answer": 10, "hint": "Add 1 to the right-hand side."},
        {"say": "So 2x < 10. Divide both sides by 2."},
        {"pre": "10 ÷ 2 = ", "post": "", "answer": 5, "phase": "substitute",
         "hint": "Half of 10."},
        {"say": "So x < 5, every number below 5."},
        {"pre": "x < 5 does not include 5, so the largest whole number is ", "post": "",
         "answer": 4, "phase": "substitute", "hint": "The first integer below 5."},
        {"pre": "Check: 2 × 4 " + MINUS + " 1 = ", "post": "", "answer": 7,
         "phase": "substitute", "done": "7 < 9 is true, so x = 4 works. Gone.",
         "hint": "Put x = 4 back in."},
    ]))

# bronze[2]  RE-POSED 3x>=9  smallest solution = 3
bronze.append(P(
    "Solve \\(3x \\geq 9\\). What is the smallest solution?",
    [3], "single_value",
    "Divide both sides by 3. The ≥ sign means the boundary itself is allowed.",
    [m("treats_ge_as_strict", 4,
       "x ≥ 3 includes 3 itself, because ≥ means 'greater than or equal to'. So the smallest value is 3, not 4.",
       "Treats ≥ as strict >: says 4.")],
    [
        {"say": "Solve it like an equation. Divide both sides by 3."},
        {"pre": "9 ÷ 3 = ", "post": "", "answer": 3, "hint": "9 shared into 3 parts."},
        {"say": "So x ≥ 3. The ≥ sign includes 3 itself, so the smallest value x can take is 3."},
        {"pre": "Smallest solution: x = ", "post": "", "answer": 3, "phase": "substitute",
         "hint": "≥ includes the boundary number."},
        {"pre": "Check by putting x = 3 in: 3 × 3 = ", "post": "", "answer": 9,
         "phase": "substitute",
         "done": "9 ≥ 9 is true, so x = 3 is allowed and is the smallest. Gone.",
         "hint": "Work out 3 times 3."},
    ]))

# bronze[3]  RE-POSED count -2<=x<6 = 8  (+ number line figure)
bronze.append(P(
    numberline(-3, 7, -2, True, 6, False, "Number line from minus 3 to 7 with a closed circle at minus 2 and an open circle at 6")
    + "<span class=\"figure-caption\">Closed circle = included, open circle = not included</span>"
    + " How many integers satisfy \\(-2 \\leq x < 6\\)?",
    [8], "single_value",
    "The low end ≤ is included, the high end < is not. List and count carefully.",
    [m("includes_open_end", 9,
       "The top end uses < , so 6 is not included. Counting from " + MINUS + "2 up to 5 gives 8 integers. Including 6 by mistake gives 9.",
       "Counts 6 as well: says 9.")],
    [
        {"say": "List the integers from the low end up to the high end, watching which ends are included."},
        {"pre": MINUS + "2 has ≤ so it IS included, and 6 has < so it is NOT. The largest integer allowed is ",
         "post": "", "answer": 5, "hint": "6 is excluded, so stop at 5."},
        {"say": "So the integers run from " + MINUS + "2 up to 5."},
        {"pre": "Count " + MINUS + "2, " + MINUS + "1, 0, 1, 2, 3, 4, 5. How many? ", "post": "",
         "answer": 8, "phase": "substitute", "hint": "Count each number in the list."},
        {"pre": "Quick check using 5 " + MINUS + " (" + MINUS + "2) + 1 = ", "post": "",
         "answer": 8, "phase": "substitute",
         "done": "Highest minus lowest, plus 1, gives 8. It matches. Gone.",
         "hint": "5 " + MINUS + " (" + MINUS + "2) = 7, then add 1."},
    ]))

# bronze[4]  RE-POSED 5x+4<=49  largest int = 9
bronze.append(P(
    "Solve \\(5x + 4 \\leq 49\\). What is the largest integer solution?",
    [9], "single_value",
    "Subtract 4, divide by 5. The ≤ sign means the boundary itself is allowed.",
    [m("treats_le_as_strict", 8,
       "x ≤ 9 includes 9, because ≤ means 'less than or equal to'. So the largest value is 9, not 8.",
       "Treats ≤ as strict <: says 8.")],
    [
        {"say": "Solve it like an equation. Subtract 4 from both sides."},
        {"pre": "49 " + MINUS + " 4 = ", "post": "", "answer": 45, "hint": "Take 4 off the right."},
        {"say": "So 5x ≤ 45. Divide both sides by 5."},
        {"pre": "45 ÷ 5 = ", "post": "", "answer": 9, "phase": "substitute",
         "hint": "45 shared into 5."},
        {"say": "So x ≤ 9. The ≤ sign includes 9."},
        {"pre": "Largest integer value of x = ", "post": "", "answer": 9, "phase": "substitute",
         "hint": "≤ includes the boundary, so 9 itself."},
        {"pre": "Check: 5 × 9 + 4 = ", "post": "", "answer": 49, "phase": "substitute",
         "done": "49 ≤ 49 is true, so x = 9 is allowed and is the largest. Gone.",
         "hint": "Put x = 9 back in."},
    ]))

# bronze[5]  x/2>3  smallest int = 7
bronze.append(P(
    "Solve \\(\\frac{x}{2} > 3\\). What is the smallest integer?",
    [7], "single_value",
    "The x is divided by 2, so multiply both sides by 2 to undo it.",
    [
        m("includes_boundary", 6,
          "x > 6 does not include 6, because > is strict. The smallest whole number above 6 is 7.",
          "Treats > as inclusive: says 6."),
        m("divided_not_multiplied", 2,
          "The x is divided by 2, so undo it by multiplying: 3 × 2 = 6, giving x > 6. Dividing 3 by 2 gives 1.5 and the wrong smallest integer, 2.",
          "Divides instead of multiplying: 3/2 = 1.5, smallest int 2."),
    ],
    [
        {"say": "Solve it like an equation. Multiply both sides by 2."},
        {"pre": "3 × 2 = ", "post": "", "answer": 6,
         "hint": "Undo the divide by 2 by multiplying."},
        {"say": "So x > 6, every number above 6."},
        {"pre": "x > 6 does not include 6, so the smallest whole number is ", "post": "",
         "answer": 7, "phase": "substitute", "hint": "The first integer above 6."},
        {"pre": "Check: 7 ÷ 2 = ", "post": "", "answer": 3.5, "phase": "substitute",
         "done": "3.5 > 3 is true, and 6 ÷ 2 = 3 is not, so 7 is the smallest. Gone.",
         "hint": "Half of 7."},
    ]))

# bronze[6]  count 1<x<8 = 6  (+ number line figure)
bronze.append(P(
    numberline(0, 9, 1, False, 8, False, "Number line from 0 to 9 with open circles at 1 and 8")
    + "<span class=\"figure-caption\">Open circles = ends not included</span>"
    + " How many integers satisfy \\(1 < x < 8\\)?",
    [6], "single_value",
    "Both ends use strict < , so neither 1 nor 8 is counted.",
    [m("includes_both_ends", 8,
       "Both ends use strict < , so 1 and 8 are both excluded. The integers 2 to 7 give 6. Counting 1 and 8 as well gives 8.",
       "Counts both endpoints: says 8.")],
    [
        {"say": "Both ends use strict < , so neither 1 nor 8 is included. List what is left."},
        {"pre": "The smallest integer bigger than 1 is ", "post": "", "answer": 2,
         "hint": "1 is excluded, so start at 2."},
        {"say": "The largest integer below 8 is 7. So the list runs 2 to 7."},
        {"pre": "Count 2, 3, 4, 5, 6, 7. How many? ", "post": "", "answer": 6,
         "phase": "substitute", "hint": "Count each number."},
        {"pre": "Quick check using 7 " + MINUS + " 2 + 1 = ", "post": "", "answer": 6,
         "phase": "substitute",
         "done": "Highest minus lowest, plus 1, gives 6. It matches. Gone.",
         "hint": "7 " + MINUS + " 2 = 5, then add 1."},
    ]))

# bronze[7]  MC  4x-3>5 -> x>2 (index 0)
bronze.append(P(
    "Solve \\(4x - 3 > 5\\). What is \\(x\\)?",
    [0], "multiple_choice",
    "Add 3 to both sides, then divide by 4. No negative is divided by, so the sign stays >.",
    [
        m("skipped_divide", 2,
          "After 4x > 8, divide both sides by 4 to get x > 2. Leaving it as x > 8 skips the divide by 4.",
          "Reads 4x>8 as x>8: option index 2."),
        m("strict_as_inclusive", 1,
          "4x " + MINUS + " 3 > 5 uses a strict >, so the answer is x > 2, not x ≥ 2. The value 2 itself is not included.",
          "Treats > as ≥: option index 1."),
    ],
    None))
bronze[7]["options"] = ["\\(x > 2\\)", "\\(x \\geq 2\\)", "\\(x > 8\\)", "\\(x < 2\\)"]

# ---------- SILVER ----------
silver = []

# silver[0]  MC  -2x>6 -> x<-3 (index 0)
silver.append(P(
    "Solve \\(-2x > 6\\). What is \\(x\\)?",
    [0], "multiple_choice",
    "Divide both sides by −2. Dividing by a negative flips the sign, so > becomes <.",
    [
        m("no_flip", 1,
          "Dividing both sides by " + MINUS + "2 flips the inequality, so > becomes <, giving x < " + MINUS + "3. Forgetting to flip leaves x > " + MINUS + "3.",
          "No flip: option index 1."),
        m("lost_negative", 3,
          "6 ÷ (" + MINUS + "2) = " + MINUS + "3, not 3. Keep the negative on the boundary: x < " + MINUS + "3.",
          "Flips but drops the negative on 3: option index 3."),
    ],
    None))
silver[0]["options"] = ["\\(x < -3\\)", "\\(x > -3\\)", "\\(x > 3\\)", "\\(x < 3\\)"]

# silver[1]  1<=2x-3<9  largest int = 5
silver.append(P(
    "Solve \\(1 \\leq 2x - 3 < 9\\). What is the largest integer?",
    [5], "single_value",
    "This is a three-part inequality: do every step to all three parts.",
    [m("includes_open_end", 6,
       "After 2 ≤ x < 6, the < means 6 is not included, so the largest integer is 5. Treating it as ≤ 6 wrongly gives 6.",
       "Counts 6: says 6.")],
    [
        {"say": "This is a three-part inequality. Do every step to all three parts. First add 3 to all three."},
        {"pre": "On the left: 1 + 3 = ", "post": "", "answer": 4, "hint": "Add 3 to the 1."},
        {"pre": "On the right: 9 + 3 = ", "post": "", "answer": 12, "hint": "Add 3 to the 9."},
        {"say": "So 4 ≤ 2x < 12. Now divide all three parts by 2."},
        {"pre": "Left: 4 ÷ 2 = ", "post": "", "answer": 2, "phase": "substitute",
         "hint": "Half of 4."},
        {"pre": "Right: 12 ÷ 2 = ", "post": "", "answer": 6, "phase": "substitute",
         "hint": "Half of 12."},
        {"say": "So 2 ≤ x < 6. The right end uses < , so 6 is not included."},
        {"pre": "Largest integer value of x = ", "post": "", "answer": 5, "phase": "substitute",
         "hint": "6 is excluded, so 5."},
        {"pre": "Check x = 5: 2 × 5 " + MINUS + " 3 = ", "post": "", "answer": 7,
         "phase": "substitute",
         "done": "1 ≤ 7 < 9 holds, so x = 5 works. Gone.",
         "hint": "Put x = 5 into 2x " + MINUS + " 3."},
    ]))

# silver[2]  MC  3(x-2)<x+4 -> x<5 (index 0)
silver.append(P(
    "Solve \\(3(x - 2) < x + 4\\). What is \\(x\\)?",
    [0], "multiple_choice",
    "Expand the bracket first, then collect the x terms on one side.",
    [m("wrong_direction", 1,
       "No negative was divided by, so the sign stays the same: x < 5, not x > 5.",
       "Flips for no reason: option index 1.")],
    None))
silver[2]["options"] = ["\\(x < 5\\)", "\\(x > 5\\)", "\\(x < 1\\)", "\\(x > 1\\)"]

# silver[3]  count -3<2x+1<=11 = 7
silver.append(P(
    "How many integers satisfy \\(-3 < 2x + 1 \\leq 11\\)?",
    [7], "single_value",
    "Do every step to all three parts, then list the integers in the final range.",
    [m("includes_open_left", 8,
       "The left end is " + MINUS + "2 < x , strict, so " + MINUS + "2 is not counted. The integers " + MINUS + "1 to 5 give 7. Counting " + MINUS + "2 as well gives 8.",
       "Counts the open left end: says 8.")],
    [
        {"say": "Do every step to all three parts. First subtract 1 from all three."},
        {"pre": "Left: " + MINUS + "3 " + MINUS + " 1 = ", "post": "", "answer": -4,
         "hint": "Take 1 off the " + MINUS + "3."},
        {"pre": "Right: 11 " + MINUS + " 1 = ", "post": "", "answer": 10, "hint": "Take 1 off the 11."},
        {"say": "So " + MINUS + "4 < 2x ≤ 10. Now divide all three parts by 2."},
        {"pre": "Left: " + MINUS + "4 ÷ 2 = ", "post": "", "answer": -2, "phase": "substitute",
         "hint": "Half of " + MINUS + "4."},
        {"pre": "Right: 10 ÷ 2 = ", "post": "", "answer": 5, "phase": "substitute",
         "hint": "Half of 10."},
        {"say": "So " + MINUS + "2 < x ≤ 5. The left uses < (so " + MINUS + "2 is out); the right uses ≤ (so 5 is in). Integers run " + MINUS + "1 to 5."},
        {"pre": "Count " + MINUS + "1, 0, 1, 2, 3, 4, 5. How many? ", "post": "", "answer": 7,
         "phase": "substitute", "done": "Seven integers fit. Gone.",
         "hint": "Count each number in the list."},
    ]))

# silver[4]  MC  5-3x>=14 -> x<=-3 (index 0)
silver.append(P(
    "Solve \\(5 - 3x \\geq 14\\). What is \\(x\\)?",
    [0], "multiple_choice",
    "Subtract 5, then divide by −3. Dividing by a negative flips ≥ to ≤.",
    [
        m("no_flip", 1,
          "Dividing by " + MINUS + "3 flips ≥ to ≤, giving x ≤ " + MINUS + "3. Without the flip you get x ≥ " + MINUS + "3, which is wrong.",
          "No flip: option index 1."),
        m("lost_negative", 2,
          "9 ÷ (" + MINUS + "3) = " + MINUS + "3, not 3. The boundary is negative: x ≤ " + MINUS + "3.",
          "Flips but drops the negative on 3: option index 2."),
    ],
    None))
silver[4]["options"] = ["\\(x \\leq -3\\)", "\\(x \\geq -3\\)", "\\(x \\leq 3\\)", "\\(x \\geq 3\\)"]

# silver[5]  (x+1)/3<=4  largest int = 11
silver.append(P(
    "Solve \\(\\frac{x+1}{3} \\leq 4\\). What is the largest integer?",
    [11], "single_value",
    "Multiply both sides by 3 to clear the fraction, then subtract 1.",
    [m("forgot_subtract", 12,
       "After x + 1 ≤ 12, subtract 1 to get x ≤ 11. Forgetting the " + MINUS + "1 leaves x ≤ 12 and the wrong largest integer, 12.",
       "Skips the subtract 1: says 12.")],
    [
        {"say": "Solve it like an equation. Multiply both sides by 3 to clear the fraction."},
        {"pre": "4 × 3 = ", "post": "", "answer": 12, "hint": "Undo the divide by 3 by multiplying."},
        {"say": "So x + 1 ≤ 12. Subtract 1 from both sides."},
        {"pre": "12 " + MINUS + " 1 = ", "post": "", "answer": 11, "phase": "substitute",
         "hint": "Take 1 off both sides."},
        {"say": "So x ≤ 11. The ≤ sign includes 11."},
        {"pre": "Largest integer value of x = ", "post": "", "answer": 11, "phase": "substitute",
         "hint": "≤ includes the boundary, so 11 itself."},
        {"pre": "Check: (11 + 1) ÷ 3 = ", "post": "", "answer": 4, "phase": "substitute",
         "done": "4 ≤ 4 is true, so x = 11 is allowed and is the largest. Gone.",
         "hint": "12 ÷ 3."},
    ]))

# silver[6]  count 1<=x<4 (from -1<=3x-4<8) = 3
silver.append(P(
    "List the integer solutions of \\(-1 \\leq 3x - 4 < 8\\). How many are there?",
    [3], "single_value",
    "Do every step to all three parts, then list the integers.",
    [m("includes_open_right", 4,
       "The top end is x < 4, strict, so 4 is not included. The integers 1, 2 and 3 give 3. Counting 4 as well gives 4.",
       "Counts the open right end: says 4.")],
    [
        {"say": "Do every step to all three parts. First add 4 to all three."},
        {"pre": "Left: " + MINUS + "1 + 4 = ", "post": "", "answer": 3, "hint": "Add 4 to the " + MINUS + "1."},
        {"pre": "Right: 8 + 4 = ", "post": "", "answer": 12, "hint": "Add 4 to the 8."},
        {"say": "So 3 ≤ 3x < 12. Now divide all three parts by 3."},
        {"pre": "Left: 3 ÷ 3 = ", "post": "", "answer": 1, "phase": "substitute",
         "hint": "3 shared into 3."},
        {"pre": "Right: 12 ÷ 3 = ", "post": "", "answer": 4, "phase": "substitute",
         "hint": "12 shared into 3."},
        {"say": "So 1 ≤ x < 4. The left ≤ includes 1; the right < excludes 4. Integers: 1, 2, 3."},
        {"pre": "How many integers is that? ", "post": "", "answer": 3, "phase": "substitute",
         "done": "Three values: 1, 2 and 3. Gone.", "hint": "Count 1, 2, 3."},
    ]))

# ---------- GOLD ----------
gold = []

# gold[0]  MC  combined -> -4<x<5 (index 0)
gold.append(P(
    "Solve \\(2x + 3 > x - 1\\) AND \\(3x - 4 < 11\\). What is the range of \\(x\\)?",
    [0], "multiple_choice",
    "Solve each inequality separately, then keep only the overlap of the two ranges.",
    [
        m("includes_boundary", 1,
          "The second inequality is strict (3x " + MINUS + " 4 < 11 gives x < 5), so 5 is not included. The range is " + MINUS + "4 < x < 5, not " + MINUS + "4 < x ≤ 5.",
          "Uses ≤ on the strict upper end: option index 1."),
        m("first_only", 2,
          "Both conditions must hold. x > " + MINUS + "4 alone ignores the second inequality, which caps x below 5.",
          "Keeps only the first inequality: option index 2."),
    ],
    None))
gold[0]["options"] = ["\\(-4 < x < 5\\)", "\\(-4 < x \\leq 5\\)", "\\(x > -4\\)", "\\(x < 5\\)"]

# gold[1]  x^2<16  count = 7
gold.append(P(
    "Solve \\(x^2 < 16\\). How many integer solutions?",
    [7], "single_value",
    "Take the square root of 16 to find the boundary, then remember the negative side.",
    [m("positive_only", 4,
       "x² < 16 means " + MINUS + "4 < x < 4, so negative values count too. The integers " + MINUS + "3 to 3 give 7. Missing the negatives gives just 4.",
       "Counts 0,1,2,3 only: says 4.")],
    [
        {"say": "For x² < 16, take the square root of 16 to find the boundary."},
        {"pre": "√16 = ", "post": "", "answer": 4, "hint": "What number times itself is 16?"},
        {"say": "So the solution is the band " + MINUS + "4 < x < 4 (both ends strict, so 4 and " + MINUS + "4 are out)."},
        {"pre": "The largest integer inside is ", "post": "", "answer": 3, "phase": "substitute",
         "hint": "4 is excluded, so 3."},
        {"say": "By symmetry the smallest is " + MINUS + "3. Integers run " + MINUS + "3 to 3."},
        {"pre": "Count " + MINUS + "3, " + MINUS + "2, " + MINUS + "1, 0, 1, 2, 3. How many? ",
         "post": "", "answer": 7, "phase": "substitute",
         "done": "Seven integers, including 0. Gone.", "hint": "Count each, do not forget 0."},
    ]))

# gold[2]  (2x-1)/3 >= (x+2)/2  smallest int = 8
gold.append(P(
    "Solve \\(\\frac{2x-1}{3} \\geq \\frac{x+2}{2}\\). What is the smallest integer?",
    [8], "single_value",
    "Multiply every term by 6 (the common denominator) to clear both fractions.",
    [m("wrong_operation", 4,
       "After x " + MINUS + " 2 ≥ 6, add 2 to both sides: x ≥ 8. Subtracting 2 instead gives x ≥ 4 and the wrong smallest integer, 4.",
       "Subtracts 2 instead of adding: says 4.")],
    [
        {"say": "Clear both fractions by multiplying every term by 6, the common denominator."},
        {"pre": "The left, (2x " + MINUS + " 1)/3, times 6 is 2 lots of (2x " + MINUS + " 1). The number in front of x is 2 × 2 = ",
         "post": "", "answer": 4, "hint": "6 ÷ 3 = 2, then 2 × the 2x."},
        {"pre": "The right, (x + 2)/2, times 6 is 3 lots of (x + 2). The number in front of x is 3 × 1 = ",
         "post": "", "answer": 3, "hint": "6 ÷ 2 = 3, then 3 × the x."},
        {"say": "So 4x " + MINUS + " 2 ≥ 3x + 6. Subtract 3x from both sides."},
        {"pre": "4x " + MINUS + " 3x = ", "post": "x", "answer": 1, "phase": "substitute",
         "hint": "One lot of x is left."},
        {"say": "So x " + MINUS + " 2 ≥ 6. Add 2 to both sides."},
        {"pre": "6 + 2 = ", "post": "", "answer": 8, "phase": "substitute",
         "hint": "Add 2 to both sides."},
        {"say": "So x ≥ 8. The ≥ includes 8, so the smallest value is 8."},
        {"pre": "Check x = 8: left (2×8 " + MINUS + " 1)/3 = 15/3 = 5, right (8 + 2)/2 = ",
         "post": "", "answer": 5, "phase": "substitute",
         "done": "5 ≥ 5 is true, so x = 8 works and is the smallest. Gone.", "hint": "10 ÷ 2."},
    ]))

# gold[3]  RE-POSED  n^2+2n-15<=0  count -5..3 = 9
gold.append(P(
    "Find the integer values of \\(n\\) where \\(n^2 + 2n - 15 \\leq 0\\). How many are there?",
    [9], "single_value",
    "Factorise into two brackets, find the roots, then count the integers between them.",
    [m("forgot_plus_one", 8,
       "Count the endpoints too: from " + MINUS + "5 to 3 is 3 " + MINUS + " (" + MINUS + "5) + 1 = 9 integers. Forgetting to add 1 gives 8.",
       "Uses 3 " + MINUS + " (" + MINUS + "5) = 8 without +1: says 8.")],
    [
        {"say": "Factorise the quadratic. Find two numbers that multiply to " + MINUS + "15 and add to +2."},
        {"pre": "Those numbers are +5 and " + MINUS + "3. The larger root comes from n " + MINUS + " 3 = 0, giving n = ",
         "post": "", "answer": 3, "hint": "Set n " + MINUS + " 3 = 0."},
        {"pre": "The other root comes from n + 5 = 0, giving n = ", "post": "", "answer": -5,
         "hint": "Set n + 5 = 0."},
        {"say": "The parabola opens upward, so it is ≤ 0 BETWEEN the roots: " + MINUS + "5 ≤ n ≤ 3. Both ends use ≤, so both are included."},
        {"pre": "The integers run from " + MINUS + "5 to 3. Using 3 " + MINUS + " (" + MINUS + "5) + 1 = ",
         "post": "", "answer": 9, "phase": "substitute", "hint": "3 " + MINUS + " (" + MINUS + "5) = 8, then add 1."},
        {"pre": "Check the top root n = 3: 3² + 2 × 3 " + MINUS + " 15 = 9 + 6 " + MINUS + " 15 = ",
         "post": "", "answer": 0, "phase": "substitute",
         "done": "0 ≤ 0 is true, so n = 3 is included, confirming the range. Gone.",
         "hint": "9 + 6 " + MINUS + " 15."},
    ]))

# gold[4]  -5<3-2x<=7  smallest int = -2
gold.append(P(
    "Solve \\(-5 < 3 - 2x \\leq 7\\). What is the smallest integer?",
    [-2], "single_value",
    "Three-part inequality: subtract 3 from all parts, then divide by −2 and flip both signs.",
    [m("treats_as_strict", -1,
       "After dividing by " + MINUS + "2, the ≤ becomes ≥, so " + MINUS + "2 IS included: " + MINUS + "2 ≤ x. The smallest value is " + MINUS + "2, not " + MINUS + "1.",
       "Treats the closed end as strict: says " + MINUS + "1.")],
    [
        {"say": "Do every step to all three parts. First subtract 3 from all three."},
        {"pre": "Left: " + MINUS + "5 " + MINUS + " 3 = ", "post": "", "answer": -8,
         "hint": "Take 3 off the " + MINUS + "5."},
        {"pre": "Right: 7 " + MINUS + " 3 = ", "post": "", "answer": 4, "hint": "Take 3 off the 7."},
        {"say": "So " + MINUS + "8 < " + MINUS + "2x ≤ 4. Now divide all three parts by " + MINUS + "2. Dividing by a negative <strong>flips</strong> both signs."},
        {"pre": "Left becomes: " + MINUS + "8 ÷ (" + MINUS + "2) = ", "post": "", "answer": 4,
         "phase": "substitute", "hint": "A negative divided by a negative is positive."},
        {"pre": "Right becomes: 4 ÷ (" + MINUS + "2) = ", "post": "", "answer": -2,
         "phase": "substitute", "hint": "A positive divided by a negative is negative."},
        {"say": "After flipping, the chain reads 4 > x ≥ " + MINUS + "2, i.e. " + MINUS + "2 ≤ x < 4. The ≤ end means " + MINUS + "2 is included."},
        {"pre": "Smallest integer value of x = ", "post": "", "answer": -2, "phase": "substitute",
         "done": MINUS + "2 is included, so it is the smallest allowed value. Gone.",
         "hint": "The ≤ end includes its boundary."},
    ]))

problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One and two-step linear inequalities: solve like an equation, then read off the smallest or largest integer.",
    "silver_description": "Inequalities with brackets, three parts at once, or a negative to divide by (flip the sign).",
    "gold_description": "Combined ranges, quadratic inequalities, and fractions on both sides.",
}

# ===================== TIER GUIDES =====================
tier_guides = {
    "bronze": {
        "title": "Bronze: solve a linear inequality",
        "steps": [
            "Treat < , > , ≤ and ≥ exactly like an = sign. Get x on its own by doing the same to both sides.",
            "Undo any adding or subtracting first, then undo any multiply or divide.",
            "The answer is a range, like <strong>x > 4</strong>. For the smallest integer, pick the first whole number inside the range.",
        ],
        "example": {
            "question": "Solve \\(3x + 2 \\geq 14\\). Give the smallest integer.",
            "steps": [
                {"label": "Subtract 2 from both sides", "content": "\\(3x \\geq 12\\)"},
                {"label": "Divide both sides by 3", "content": "\\(x \\geq 4\\)"},
                {"label": "Check the boundary", "content": "\\(3 \\times 4 + 2 = 14\\), and 14 ≥ 14 is true, so 4 is included."},
                {"label": "Smallest integer", "content": "\\(x = 4\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: three parts and the flip rule",
        "steps": [
            "If you multiply or divide by a <strong>negative</strong>, flip the inequality sign: < becomes >.",
            "For a three-part inequality, do every step to all three parts at once.",
            "Expand any brackets first, then collect x on one side as usual.",
        ],
        "example": {
            "question": "Solve \\(1 \\leq 2x - 3 < 7\\). Give the largest integer.",
            "steps": [
                {"label": "Add 3 to all three parts", "content": "\\(4 \\leq 2x < 10\\)"},
                {"label": "Divide all three parts by 2", "content": "\\(2 \\leq x < 5\\)"},
                {"label": "Check the top end", "content": "x < 5 does not include 5, so the largest whole number is 4."},
                {"label": "Largest integer", "content": "\\(x = 4\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: ranges and quadratics",
        "steps": [
            "Two conditions joined by AND: solve each, then keep only the overlap as one range.",
            "For \\(x^2 < k\\), the answer is the band \\(-\\sqrt{k} < x < \\sqrt{k}\\) around zero.",
            "Count integers by listing both ends carefully, checking whether each end is included.",
        ],
        "example": {
            "question": "Solve \\(x^2 < 9\\). How many integer solutions?",
            "steps": [
                {"label": "Square root of 9", "content": "\\(\\sqrt{9} = 3\\)"},
                {"label": "Write the band", "content": "\\(-3 < x < 3\\)"},
                {"label": "List the integers", "content": "−2, −1, 0, 1, 2"},
                {"label": "How many", "content": "\\(5\\) integers", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ===================== GUIDED (opener + teach) =====================
guided = {
    "opener": {
        "prompt": "Before any algebra, try this with common sense.",
        "steps": [
            {"say": "You are saving for a £30 game. You have £6 now and add £4 to your money box every week."},
            {"pre": "After 4 weeks your money is 6 + 4 + 4 + 4 + 4 = £", "post": "", "answer": 22,
             "hint": "Start at 6 and add 4 four times."},
            {"pre": "Not enough yet. What is the fewest whole weeks to reach at least £30? weeks = ",
             "post": "", "answer": 6, "hint": "Keep adding 4: 22, 26, 30. Count the weeks."},
            {"say": "You just solved an inequality. 'At least £30' means 6 + 4w ≥ 30. Solving it gives w ≥ 6, so 6 whole weeks. The answer is a <strong>range</strong> (6 or more), not a single number, and that is what makes inequalities different from equations."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Solve \\(2x + 5 < 17\\). What is the largest integer value of \\(x\\)?",
            "steps": [
                {"say": "Solve it like an equation. First subtract 5 from both sides."},
                {"pre": "17 " + MINUS + " 5 = ", "post": "", "answer": 12, "hint": "Take 5 off the right-hand side."},
                {"say": "So 2x < 12. Now divide both sides by 2."},
                {"pre": "12 ÷ 2 = ", "post": "", "answer": 6, "hint": "Half of 12."},
                {"say": "So x < 6. The answer is a range: every number below 6."},
                {"pre": "x < 6 does not include 6, so the largest whole number is ", "post": "", "answer": 5,
                 "hint": "The first integer below 6."},
                {"pre": "Check: 2 × 5 + 5 = ", "post": "", "answer": 15,
                 "done": "15 < 17 is true, so x = 5 works and 6 would not. Gone.", "hint": "Put x = 5 back in."},
            ],
        },
        "silver": {
            "display": "Solve \\(4 - 2x > 10\\). What is the largest integer value of \\(x\\)?",
            "steps": [
                {"say": "Get the x term by itself. Subtract 4 from both sides."},
                {"pre": "10 " + MINUS + " 4 = ", "post": "", "answer": 6, "hint": "Take 4 off the right-hand side."},
                {"say": "So " + MINUS + "2x > 6. Now divide both sides by " + MINUS + "2. Dividing by a negative <strong>flips</strong> the sign, so > becomes <."},
                {"pre": "6 ÷ (" + MINUS + "2) = ", "post": "", "answer": -3, "hint": "A positive divided by a negative is negative."},
                {"say": "So x < " + MINUS + "3. Flipping the sign is the one move you must not forget."},
                {"pre": "x < " + MINUS + "3 does not include " + MINUS + "3, so the largest whole number is ",
                 "post": "", "answer": -4, "hint": "The first integer below " + MINUS + "3."},
                {"pre": "Check: 4 " + MINUS + " 2 × (" + MINUS + "4) = ", "post": "", "answer": 12,
                 "done": "12 > 10 is true, so x = " + MINUS + "4 works. The flip was right.", "hint": "Remember " + MINUS + "2 × " + MINUS + "4 = +8."},
            ],
        },
        "gold": {
            "display": "Solve \\(x + 2 > 1\\) AND \\(2x - 1 \\leq 9\\). Give the range of \\(x\\).",
            "steps": [
                {"say": "Solve each inequality separately, then keep the overlap. Start with the first: subtract 2 from both sides."},
                {"pre": "1 " + MINUS + " 2 = ", "post": "", "answer": -1, "hint": "1 take away 2."},
                {"say": "So x > " + MINUS + "1. Now the second: add 1 to both sides to get 2x ≤ 10, then divide by 2."},
                {"pre": "10 ÷ 2 = ", "post": "", "answer": 5, "hint": "Half of 10."},
                {"say": "So x ≤ 5. Now combine: x is bigger than " + MINUS + "1 AND no more than 5."},
                {"pre": "The lower end of the range is x > ", "post": "", "answer": -1, "hint": "From the first inequality."},
                {"pre": "The upper end is x ≤ ", "post": "", "answer": 5,
                 "done": "So " + MINUS + "1 < x ≤ 5. Both conditions hold only between these ends. Gone.",
                 "hint": "From the second inequality."},
            ],
        },
    },
}

# ===================== METHOD CARD (slim) =====================
method_card = {
    "title": "Inequalities",
    "steps": [
        "Solve an inequality just like an equation: do the same to both sides to get x on its own.",
        "One golden rule: if you multiply or divide by a negative, flip the sign (< becomes >).",
        "For a three-part inequality like a ≤ 2x < b, do every step to all three parts.",
        "Read the answer as a range, then pick the smallest or largest integer, or count them, as asked.",
    ],
    "content": "<p><strong>Inequalities</strong> compare two amounts that are not equal. Solve them exactly like equations, keeping x on one side. The one extra rule: multiplying or dividing both sides by a <strong>negative</strong> flips the inequality sign.</p><p>The answer is a range of values, not a single number. If a question asks for the smallest or largest integer, or how many integers fit, mark the range on a number line and check each end carefully.</p>",
    "example": "<p><strong>Solve</strong> \\(2x - 1 \\geq 7\\)</p><p>Add 1: \\(2x \\geq 8\\). Divide by 2: \\(x \\geq 4\\). The ≥ includes 4, so the smallest integer is 4.</p>",
}

practice_data = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": problem_bank,
    "tier_guides": tier_guides,
    "guided": guided,
    "related_videos": related_videos,
    "worked_examples": worked_examples,
}

# guided-only shard (no figures)
import copy
guided_only = copy.deepcopy(practice_data)
for t in ("bronze", "silver", "gold"):
    for p in guided_only["problem_bank"][t]:
        d = p["display"]
        if "<svg" in d:
            p["display"] = d[d.rindex("</span>") + 7:].lstrip() if "</span>" in d else d

io.open("lesson_maths-ocr_algebra-L11.json", "w", encoding="utf-8").write(
    json.dumps(guided_only, ensure_ascii=False, indent=1))
io.open("lesson_maths-ocr_algebra-L11_diagrams.json", "w", encoding="utf-8").write(
    json.dumps(practice_data, ensure_ascii=False, indent=1))
print("wrote both shards")
print("figures in:", [t + str(i) for t in ("bronze","silver","gold")
      for i, p in enumerate(practice_data["problem_bank"][t]) if "<svg" in p["display"]])
