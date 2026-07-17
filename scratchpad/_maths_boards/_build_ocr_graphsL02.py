# -*- coding: utf-8 -*-
"""Build guided + diagrams practice_data for maths-ocr graphs-L02 (Equation of a Line)."""
import json, io

OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_graphs-L02.json"

# ---------- G5 coordinate-grid SVG (generated from its own numbers) ----------
# Points (2,0) and (0,-6); line y = 3x - 6.
def px(x):  # math x [-1,3] -> pixels [30,210]
    return round(30 + (x - (-1)) * 45.0, 1)
def py(y):  # math y [1,-7] -> pixels [20,180]
    return round(20 + (1 - y) * 20.0, 1)

# line endpoints inside grid: at y=1 -> x=7/3; at y=-7 -> x=-1/3
lx1, ly1 = px(-1/3.0), py(-7)   # bottom
lx2, ly2 = px(7/3.0), py(1)     # top
ax_y0 = py(0)                    # x-axis pixel row
ax_x0 = px(0)                    # y-axis pixel col
p1x, p1y = px(2), py(0)          # (2,0)
p2x, p2y = px(0), py(-6)         # (0,-6)

g5_svg = (
    '<svg viewBox="0 0 240 200" role="img" '
    'aria-label="Coordinate grid with points (2, 0) and (0, minus 6) joined by a straight line" '
    'style="max-width:240px">'
    f'<line x1="{ax_x0}" y1="20" x2="{ax_x0}" y2="184" stroke="currentColor" stroke-width="1"/>'
    f'<line x1="26" y1="{ax_y0}" x2="214" y2="{ax_y0}" stroke="currentColor" stroke-width="1"/>'
    f'<line x1="{lx1}" y1="{ly1}" x2="{lx2}" y2="{ly2}" stroke="#60a5fa" stroke-width="2" fill="none"/>'
    f'<circle cx="{p1x}" cy="{p1y}" r="3.5" fill="currentColor"/>'
    f'<circle cx="{p2x}" cy="{p2y}" r="3.5" fill="currentColor"/>'
    f'<text x="{p1x+5}" y="{p1y-5}" font-family="Inter,sans-serif" font-size="11" fill="currentColor">(2, 0)</text>'
    f'<text x="{p2x+6}" y="{p2y+4}" font-family="Inter,sans-serif" font-size="11" fill="currentColor">(0, −6)</text>'
    f'<text x="208" y="{ax_y0-5}" font-family="Inter,sans-serif" font-size="10" fill="currentColor">x</text>'
    f'<text x="{ax_x0+5}" y="28" font-family="Inter,sans-serif" font-size="10" fill="currentColor">y</text>'
    f'<text x="{ax_x0-9}" y="{ax_y0+12}" font-family="Inter,sans-serif" font-size="10" fill="currentColor">0</text>'
    '</svg>'
)

# ---------- opener line-graph SVG (plumber) ----------
# (0,£30) -> (40,113) ; (3,£90) -> (220,40)  [60px/hour, 1.2222 px/£]
opener_svg = (
    '<svg viewBox="0 0 260 180" role="img" '
    'aria-label="Line graph of a plumber cost against hours: it starts at thirty pounds at zero hours and rises to ninety pounds at three hours" '
    'style="max-width:260px">'
    '<line x1="40" y1="22" x2="40" y2="150" stroke="currentColor" stroke-width="1"/>'
    '<line x1="40" y1="150" x2="252" y2="150" stroke="currentColor" stroke-width="1"/>'
    '<line x1="40" y1="113" x2="220" y2="40" stroke="#60a5fa" stroke-width="2.5" fill="none"/>'
    '<circle cx="40" cy="113" r="3.5" fill="currentColor"/>'
    '<circle cx="220" cy="40" r="3.5" fill="currentColor"/>'
    '<text x="48" y="110" font-family="Inter,sans-serif" font-size="11" fill="currentColor">(0, £30)</text>'
    '<text x="158" y="34" font-family="Inter,sans-serif" font-size="11" fill="currentColor">(3, £90)</text>'
    '<text x="150" y="171" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">hours</text>'
    '<text x="14" y="88" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" transform="rotate(-90 14 88)">cost (£)</text>'
    '<text x="40" y="164" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">0</text>'
    '<text x="220" y="164" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">3</text>'
    '</svg>'
)


def mc(display, options, sol_idx, hint, patt, message, expect=None):
    return {
        "display": display, "options": options, "solutions": [sol_idx],
        "calculator": False, "input_type": "multiple_choice", "hint": hint,
        "misconceptions": [{"pattern": patt, "expect": expect, "message": message}],
    }


def sv(display, sol, hint, miscon, steps):
    return {
        "display": display, "solutions": [sol], "calculator": False,
        "input_type": "single_value", "hint": hint,
        "misconceptions": miscon, "guided_steps": steps,
    }


bronze = [
    mc("A line has gradient 5 and y-intercept 3. Write the equation.",
       ["\\(y = 5x + 3\\)", "\\(y = 3x + 5\\)", "\\(y = 5x - 3\\)", "\\(y = -5x + 3\\)"],
       0, "In y = mx + c, the gradient is m and the y-intercept is c.",
       "confused_m_c", "In y = mx + c, m is the gradient and c is the y-intercept, so y = 5x + 3."),
    sv("A line has equation \\(y = 7x - 4\\). What is the gradient?", 7,
       "The gradient is the number in front of x.",
       [{"pattern": "confused_m_c", "expect": -4,
         "message": "The gradient is the number in front of x, which is 7. The −4 is the y-intercept, not the gradient."}],
       [{"say": "In \\(y = mx + c\\), the gradient \\(m\\) is the number multiplying \\(x\\).",
         "pre": "the number in front of x here is ", "post": "", "answer": 7,
         "hint": "Look at what multiplies x in y = 7x − 4."},
        {"say": "That number IS the gradient. The −4 is the y-intercept, not part of the gradient.",
         "phase": "substitute", "pre": "so the gradient m = ", "post": "", "answer": 7,
         "hint": "Same number in front of x."},
        {"pre": "check: at x = 0, y = −4; at x = 1, y = 3. The rise for 1 across is 3 − (−4) = ",
         "post": "", "answer": 7, "done": "Up 7 for every 1 across is exactly the gradient.",
         "hint": "3 minus negative 4."}]),
    sv("A line has equation \\(y = -2x + 6\\). What is the y-intercept?", 6,
       "The y-intercept is the constant term, c.",
       [{"pattern": "confused_m_c", "expect": -2,
         "message": "The y-intercept is c = 6. The −2 is the gradient, not the y-intercept."}],
       [{"say": "The y-intercept is \\(c\\), the constant added at the end of \\(y = mx + c\\).",
         "pre": "the constant at the end here is ", "post": "", "answer": 6,
         "hint": "The number after the x term."},
        {"say": "The y-intercept is where the line crosses the y-axis, at \\(x = 0\\).",
         "phase": "substitute", "pre": "put x = 0: y = −2×0 + 6 = ", "post": "", "answer": 6,
         "hint": "−2 times 0 is 0, leaving 6."},
        {"pre": "so the line crosses the y-axis at (0, 6). The y-intercept is ", "post": "", "answer": 6,
         "done": "It is c = 6.", "hint": "Read the value where x = 0."}]),
    sv("A line passes through \\((0, -2)\\) with gradient 3. What is the equation? Give the value of \\(c\\).", -2,
       "The point (0, c) sits on the y-axis, so it gives c directly.",
       [{"pattern": "wrong_sub", "expect": 2,
         "message": "The line crosses the y-axis at (0, −2), so c = −2. Dropping the minus sign gives 2 by mistake."}],
       [{"say": "The point \\((0, -2)\\) is on the y-axis, because its x-value is 0.",
         "pre": "the y-value where x = 0 is ", "post": "", "answer": -2,
         "hint": "Read the second number in (0, −2), keep the minus."},
        {"say": "The y-intercept c is exactly that y-value.",
         "phase": "substitute", "pre": "so c = ", "post": "", "answer": -2,
         "hint": "Same value, with its sign."},
        {"pre": "check the equation y = 3x − 2 at x = 0: y = 3×0 − 2 = ", "post": "", "answer": -2,
         "done": "It crosses at (0, −2), so c = −2.", "hint": "3 times 0 is 0, leaving −2."}]),
    mc("Which line is parallel to \\(y = 4x + 1\\)?",
       ["\\(y = 4x - 7\\)", "\\(y = -4x + 1\\)", "\\(y = \\frac{1}{4}x + 1\\)", "\\(y = x + 4\\)"],
       0, "Parallel lines have the same gradient.",
       "confused_parallel", "Parallel lines share the same gradient. Only y = 4x − 7 has gradient 4."),
    sv("A line has equation \\(y = -x + 5\\). What is the gradient?", -1,
       "y = −x means the number in front of x is −1.",
       [{"pattern": "confused_m_c", "expect": 5,
         "message": "The gradient is the number in front of x, which is −1. The 5 is the y-intercept, not the gradient."}],
       [{"say": "\\(y = -x + 5\\) is the same as \\(y = -1x + 5\\).",
         "pre": "the number in front of x is ", "post": "", "answer": -1, "hint": "−x means −1 times x."},
        {"say": "That number IS the gradient.",
         "phase": "substitute", "pre": "so the gradient m = ", "post": "", "answer": -1,
         "hint": "Same number in front of x."},
        {"pre": "check: at x = 0, y = 5; at x = 1, y = 4. The rise for 1 across is 4 − 5 = ",
         "post": "", "answer": -1, "done": "Down 1 for every 1 across is a gradient of −1.",
         "hint": "4 minus 5."}]),
    sv("The equation of a line is \\(y = \\frac{1}{2}x + 4\\). What is \\(y\\) when \\(x = 8\\)?", 8,
       "Substitute x = 8 into the equation.",
       [{"pattern": "wrong_sub", "expect": 4,
         "message": "y = ½×8 + 4 = 4 + 4 = 8. Forgetting to add the 4 gives just 4."}],
       [{"say": "To find \\(y\\), substitute \\(x = 8\\) into \\(y = \\frac{1}{2}x + 4\\).",
         "pre": "the x part: ½×8 = ", "post": "", "answer": 4, "hint": "Half of 8."},
        {"say": "Now add the y-intercept, 4.",
         "phase": "substitute", "pre": "y = 4 + 4 = ", "post": "", "answer": 8, "hint": "Add the constant."},
        {"pre": "check: ½×8 + 4 = ", "post": "", "answer": 8, "done": "So y = 8 when x = 8.",
         "hint": "4 plus 4."}]),
    sv("Find the gradient of the line through \\((0, 1)\\) and \\((4, 9)\\).", 2,
       "Gradient is (change in y) over (change in x).",
       [{"pattern": "rise_run_inverted", "expect": 0.5,
         "message": "Divide change in y by change in x: 8 ÷ 4 = 2. Doing 4 ÷ 8 = 0.5 flips the fraction."}],
       [{"say": "Gradient is (change in y) over (change in x). Use \\((0, 1)\\) and \\((4, 9)\\).",
         "pre": "change in y = 9 − 1 = ", "post": "", "answer": 8, "hint": "Top y minus bottom y."},
        {"pre": "change in x = 4 − 0 = ", "post": "", "answer": 4, "hint": "Right x minus left x."},
        {"say": "Now divide to get the gradient.",
         "phase": "substitute", "pre": "m = 8 ÷ 4 = ", "post": "", "answer": 2,
         "hint": "Divide change in y by change in x."},
        {"pre": "check: from (0, 1), up 2 per 1 across, at x = 4 gives y = 1 + 2×4 = ", "post": "", "answer": 9,
         "done": "It lands on (4, 9), so m = 2.", "hint": "1 plus 8."}]),
]

silver = [
    sv("Find the equation of the line through \\((1, 5)\\) and \\((3, 11)\\). What is the y-intercept \\(c\\)?", 2,
       "Find the gradient from the two points, then substitute to find c.",
       [{"pattern": "wrong_formula", "expect": 8,
         "message": "From 5 = 3 + c, subtract 3: c = 2. Adding the 3 gives 8, which does not fit the points."}],
       [{"say": "Two points and no gradient, so find \\(m\\) first: (change in y) over (change in x).",
         "pre": "change in y = 11 − 5 = ", "post": "", "answer": 6, "hint": "Top y minus bottom y."},
        {"pre": "change in x = 3 − 1 = ", "post": "", "answer": 2, "hint": "Right x minus left x."},
        {"pre": "m = 6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Divide."},
        {"say": "Substitute \\((1, 5)\\) into \\(y = 3x + c\\). The x part is 3×1 = 3, so \\(5 = 3 + c\\):",
         "phase": "substitute", "pre": "c = 5 − 3 = ", "post": "", "answer": 2, "hint": "Take the x part off both sides."},
        {"pre": "check with (3, 11): 3×3 + 2 = ", "post": "", "answer": 11, "done": "It gives 11, so c = 2.",
         "hint": "9 plus 2."}]),
    sv("A line has equation \\(3y = 9x - 6\\). What is the gradient?", 3,
       "Divide the whole equation by 3 to reach y = mx + c.",
       [{"pattern": "forgot_step", "expect": 9,
         "message": "Divide every term by 3 first: y = 3x − 2, gradient 3. Reading 9 straight off forgets to make y the subject."}],
       [{"say": "The equation is not in \\(y = mx + c\\) form. Divide every term by 3.",
         "pre": "9x ÷ 3 gives the x coefficient: 9 ÷ 3 = ", "post": "", "answer": 3,
         "hint": "Divide the x-coefficient by 3."},
        {"pre": "−6 ÷ 3 = ", "post": "", "answer": -2, "hint": "Divide the constant by 3."},
        {"say": "So \\(y = 3x - 2\\). Now read the gradient.",
         "phase": "substitute", "pre": "the number in front of x is ", "post": "", "answer": 3,
         "hint": "Coefficient of x in y = 3x − 2."},
        {"pre": "it is 3, not the original 9. The gradient is ", "post": "", "answer": 3,
         "done": "Always divide to reach y = mx + c before reading m.", "hint": "Read m from y = 3x − 2."}]),
    sv("Line A: \\(y = 2x + 5\\). Line B is parallel to A and passes through \\((0, -3)\\). What is the equation of Line B? Give \\(c\\).", -3,
       "Parallel lines have the same gradient; the point (0, c) gives c.",
       [{"pattern": "sign_error", "expect": 3,
         "message": "Line B crosses the y-axis at (0, −3), so c = −3. Dropping the minus sign gives 3."}],
       [{"say": "Parallel lines share the same gradient, so Line B also has gradient 2.",
         "pre": "the gradient of Line B is ", "post": "", "answer": 2, "hint": "Same as Line A."},
        {"say": "Line B passes through \\((0, -3)\\), which is on the y-axis.",
         "phase": "substitute", "pre": "the y-value where x = 0 gives c = ", "post": "", "answer": -3,
         "hint": "Read the y-value of (0, −3), keep the minus."},
        {"pre": "check the equation y = 2x − 3 at x = 0: y = 2×0 − 3 = ", "post": "", "answer": -3,
         "done": "It crosses at (0, −3), so c = −3.", "hint": "2 times 0 is 0, leaving −3."}]),
    sv("Find the equation of the line through \\((2, 1)\\) and \\((5, 13)\\). What is the gradient?", 4,
       "Gradient is (change in y) over (change in x).",
       [{"pattern": "rise_run_inverted", "expect": 0.25,
         "message": "Divide change in y by change in x: 12 ÷ 3 = 4. Doing 3 ÷ 12 = 0.25 flips the fraction."}],
       [{"say": "Gradient is (change in y) over (change in x). Use \\((2, 1)\\) and \\((5, 13)\\).",
         "pre": "change in y = 13 − 1 = ", "post": "", "answer": 12, "hint": "Top y minus bottom y."},
        {"pre": "change in x = 5 − 2 = ", "post": "", "answer": 3, "hint": "Right x minus left x."},
        {"say": "Now divide to get the gradient.",
         "phase": "substitute", "pre": "m = 12 ÷ 3 = ", "post": "", "answer": 4,
         "hint": "Divide change in y by change in x."},
        {"pre": "check: from (2, 1), up 4 per 1 across, at x = 5 gives y = 1 + 4×3 = ", "post": "", "answer": 13,
         "done": "It lands on (5, 13), so m = 4.", "hint": "1 plus 12."}]),
    sv("The line \\(y = mx + 2\\) passes through \\((3, -10)\\). Find \\(m\\).", -4,
       "Substitute the point, then solve for m.",
       [{"pattern": "forgot_step", "expect": -12,
         "message": "From −10 = 3m + 2, take 2 off: 3m = −12, then divide by 3: m = −4. Stopping at −12 forgets to divide."}],
       [{"say": "Substitute \\((3, -10)\\) into \\(y = mx + 2\\): \\(-10 = 3m + 2\\).",
         "pre": "take 2 off both sides: 3m = −10 − 2 = ", "post": "", "answer": -12, "hint": "−10 minus 2."},
        {"say": "Now divide by 3.",
         "phase": "substitute", "pre": "m = −12 ÷ 3 = ", "post": "", "answer": -4, "hint": "Divide by 3."},
        {"pre": "check: 3×(−4) + 2 = ", "post": "", "answer": -10, "done": "It gives −10, so m = −4.",
         "hint": "−12 plus 2."}]),
    sv("A line has equation \\(4x + 2y = 10\\). What is the gradient?", -2,
       "Rearrange to y = mx + c before reading the gradient.",
       [{"pattern": "forgot_step", "expect": -4,
         "message": "Make y the subject: 2y = −4x + 10, then divide by 2: y = −2x + 5, gradient −2. Reading −4 forgets to divide by 2."}],
       [{"say": "Rearrange to \\(y = mx + c\\). Move \\(4x\\) across: \\(2y = -4x + 10\\).",
         "pre": "the x coefficient is now ", "post": "", "answer": -4, "hint": "Moving +4x across makes it −4x."},
        {"say": "Divide every term by 2 to make y the subject.",
         "phase": "substitute", "pre": "−4 ÷ 2 gives the gradient: ", "post": "", "answer": -2, "hint": "Divide −4 by 2."},
        {"pre": "so \\(y = -2x + 5\\). Check the y-intercept at x = 0: y = ", "post": "", "answer": 5,
         "done": "The gradient is −2, the number in front of x.", "hint": "−2 times 0 plus 5."}]),
    sv("Two lines are perpendicular. One has gradient 4. What is the gradient of the other? Give as a decimal.", -0.25,
       "Perpendicular gradient is the negative reciprocal: flip and change sign.",
       [{"pattern": "no_flip", "expect": -4,
         "message": "The perpendicular gradient is the negative RECIPROCAL: flip 4 to one quarter as well as change the sign, giving −0.25. Only changing the sign gives −4."},
        {"pattern": "no_sign", "expect": 0.25,
         "message": "Flip 4 to one quarter AND change the sign: the perpendicular gradient is −0.25, not +0.25."}],
       [{"say": "Perpendicular gradients are negative reciprocals: flip the number and change the sign.",
         "pre": "flip 4 (that is 1 ÷ 4) to a decimal: ", "post": "", "answer": 0.25, "hint": "1 divided by 4."},
        {"say": "Now change the sign to make it negative.",
         "phase": "substitute", "pre": "the perpendicular gradient is −(0.25) = ", "post": "", "answer": -0.25,
         "hint": "Put a minus in front."},
        {"pre": "check: perpendicular gradients multiply to −1, so 4 × (−0.25) = ", "post": "", "answer": -1,
         "done": "They multiply to −1, so −0.25 is correct.", "hint": "4 times −0.25."}]),
]

gold = [
    sv("Find the equation of the line through \\((-1, 8)\\) and \\((3, -4)\\). What is the value of \\(c\\)?", 5,
       "Find the gradient first, watching the negative x-value, then substitute.",
       [{"pattern": "sign_error", "expect": 2,
         "message": "The x-gap is 3 − (−1) = 4, not 3 − 1 = 2. Using 2 gives m = −6 and then c = 2, which fits neither point."}],
       [{"say": "Two points, no gradient given, so find \\(m\\) first: (change in y) over (change in x).",
         "pre": "change in y = −4 − 8 = ", "post": "", "answer": -12, "hint": "Top y minus bottom y: −4 minus 8."},
        {"pre": "change in x = 3 − (−1) = ", "post": "", "answer": 4, "hint": "Subtract the x-values: 3 minus −1."},
        {"pre": "m = −12 ÷ 4 = ", "post": "", "answer": -3, "hint": "Divide the change in y by the change in x."},
        {"say": "Substitute \\((-1, 8)\\) into \\(y = -3x + c\\). The x part is −3×(−1) = 3, so \\(8 = 3 + c\\):",
         "phase": "substitute", "pre": "c = 8 − 3 = ", "post": "", "answer": 5, "hint": "Take the x part off both sides."},
        {"pre": "check with (3, −4): −3×3 + 5 = ", "post": "", "answer": -4, "done": "It gives −4, so c = 5.",
         "hint": "−9 plus 5."}]),
    sv("Line P: \\(y = 5x - 2\\). Find the gradient of a line perpendicular to P. Give as a decimal.", -0.2,
       "Perpendicular gradient is the negative reciprocal of 5.",
       [{"pattern": "no_flip", "expect": -5,
         "message": "The perpendicular gradient is the negative reciprocal: flip 5 to one fifth AND change the sign, giving −0.2. Only changing the sign gives −5."}],
       [{"say": "The gradient of P is 5. Perpendicular gradients are negative reciprocals: flip and change sign.",
         "pre": "flip 5 (that is 1 ÷ 5) to a decimal: ", "post": "", "answer": 0.2, "hint": "1 divided by 5."},
        {"say": "Now change the sign to negative.",
         "phase": "substitute", "pre": "the perpendicular gradient is −(0.2) = ", "post": "", "answer": -0.2,
         "hint": "Put a minus in front."},
        {"pre": "check: 5 × (−0.2) = ", "post": "", "answer": -1,
         "done": "Perpendicular gradients multiply to −1, so −0.2 is correct.", "hint": "5 times −0.2."}]),
    sv("The line \\(x + 4y = 12\\) is perpendicular to \\(y = mx + 1\\). Find \\(m\\).", 4,
       "Rearrange to find the first line's gradient, then take its negative reciprocal.",
       [{"pattern": "no_sign_change", "expect": -4,
         "message": "Rearranged, x + 4y = 12 gives y = −0.25x + 3, gradient −0.25. Its negative reciprocal flips to −4 then changes sign to +4. Stopping at −4 forgets the sign change."}],
       [{"say": "First find the gradient of \\(x + 4y = 12\\). Make y the subject: \\(4y = -x + 12\\), then divide by 4.",
         "pre": "the x coefficient is −1 ÷ 4 = ", "post": "", "answer": -0.25, "hint": "−1 divided by 4."},
        {"say": "So the first line has gradient −0.25 (negative one quarter). Perpendicular gradients are negative reciprocals: flip and change sign.",
         "pre": "flip negative one quarter to get ", "post": "", "answer": -4, "hint": "Turn −1/4 upside down: −4."},
        {"say": "Now change the sign to get m.",
         "phase": "substitute", "pre": "m = −(−4) = ", "post": "", "answer": 4, "hint": "Negative of −4."},
        {"pre": "check: gradient −0.25 times m must equal −1, so −0.25 × 4 = ", "post": "", "answer": -1,
         "done": "They multiply to −1, so m = 4.", "hint": "−0.25 times 4."}]),
    sv("Show the lines \\(y = 2x + 3\\) and \\(y = 2x - 5\\) are parallel. What is their common gradient?", 2,
       "Compare the numbers in front of x in each equation.",
       [{"pattern": "confused_m_c", "expect": 3,
         "message": "Parallel lines share the gradient m, the number in front of x, which is 2 for both. The 3 is a y-intercept, not the gradient."}],
       [{"say": "Read the gradient of each line: it is the number in front of \\(x\\).",
         "pre": "the gradient of \\(y = 2x + 3\\) is ", "post": "", "answer": 2,
         "hint": "Number in front of x in the first line."},
        {"say": "Now the second line.",
         "phase": "substitute", "pre": "the gradient of \\(y = 2x - 5\\) is ", "post": "", "answer": 2,
         "hint": "Number in front of x in the second line."},
        {"pre": "both gradients are equal, so the lines are parallel. The common gradient is ", "post": "", "answer": 2,
         "done": "Equal gradients mean parallel. The common gradient is 2.",
         "hint": "Both lines have the same number in front of x."}]),
    sv(g5_svg + "A line passes through \\((2, 0)\\) and \\((0, -6)\\). Find the gradient.", 3,
       "Gradient is (change in y) over (change in x); keep the points in order.",
       [{"pattern": "sign_error", "expect": -3,
         "message": "Keep the points in the same order. Change in y = −6 − 0 = −6 and change in x = 0 − 2 = −2, so m = −6 ÷ −2 = 3. Mixing the order gives −3."}],
       [{"say": "Gradient is (change in y) over (change in x). Take the points in order, from \\((2, 0)\\) to \\((0, -6)\\).",
         "pre": "change in y = −6 − 0 = ", "post": "", "answer": -6, "hint": "Second y minus first y."},
        {"pre": "change in x = 0 − 2 = ", "post": "", "answer": -2, "hint": "Second x minus first x."},
        {"say": "Now divide. A negative divided by a negative is positive.",
         "phase": "substitute", "pre": "m = −6 ÷ (−2) = ", "post": "", "answer": 3, "hint": "−6 divided by −2."},
        {"pre": "check: from (0, −6), up 3 per 1 across, at x = 2 gives y = −6 + 3×2 = ", "post": "", "answer": 0,
         "done": "It lands on (2, 0), so m = 3.", "hint": "−6 plus 6."}]),
]

problem_bank = {
    "bronze_description": "Read the gradient and y-intercept straight from y = mx + c, or substitute an x-value to find y.",
    "silver_description": "Find c by substituting a point, find the gradient from two points, or rearrange before reading m.",
    "gold_description": "Combine two-point gradients, perpendicular and parallel lines, and unknown values in multi-step problems.",
    "bronze": bronze, "silver": silver, "gold": gold,
}

method_card = {
    "title": "Equation of a Line",
    "steps": [
        "Read m and c straight from y = mx + c, or rearrange the equation into that form first.",
        "From two points, gradient m = (change in y) ÷ (change in x), then substitute one point to find c.",
        "Parallel lines share the same gradient m.",
        "A perpendicular gradient is the negative reciprocal, −1/m: flip the fraction and change the sign.",
    ],
    "content": "<p>A straight line is \\(y = mx + c\\): \\(m\\) is the gradient (steepness) and \\(c\\) is the y-intercept (where it crosses the y-axis).</p><p><strong>Parallel</strong> lines share the same gradient. <strong>Perpendicular</strong> gradients multiply to \\(-1\\), so flip the fraction and change the sign: \\(m \\to -\\frac{1}{m}\\).</p><p>If a line is written as \\(ax + by = c\\), rearrange to make \\(y\\) the subject before reading the gradient.</p>",
    "example": "<p><strong>Find the equation of the line through \\((2, 7)\\) with gradient 3.</strong></p><p>\\(m = 3\\), then substitute: \\(7 = 3(2) + c\\), so \\(7 = 6 + c\\) and \\(c = 1\\).</p><p><strong>Answer:</strong> \\(y = 3x + 1\\)</p>",
}

tier_guides = {
    "bronze": {
        "title": "Bronze: reading y = mx + c",
        "steps": [
            "In \\(y = mx + c\\), the gradient is \\(m\\), the number in front of \\(x\\), and the y-intercept is \\(c\\), where the line crosses the y-axis.",
            "To build an equation, put the gradient in the \\(m\\) slot and the y-intercept in the \\(c\\) slot, keeping every minus sign.",
            "To find \\(y\\) at a given \\(x\\), substitute the \\(x\\)-value and work out \\(mx + c\\).",
        ],
        "example": {
            "question": "A line has gradient 2 and crosses the y-axis at (0, −3). Find y when x = 5.",
            "steps": [
                {"label": "Write the equation", "content": "<p>\\(m = 2\\), \\(c = -3\\), so \\(y = 2x - 3\\).</p>"},
                {"label": "Substitute x = 5", "content": "<p>\\(y = 2(5) - 3 = 10 - 3\\)</p>"},
                {"label": "Check", "content": "<p>\\(10 - 3 = 7\\)</p>"},
                {"label": "Answer", "content": "<p>\\(y = 7\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: finding c and rearranging",
        "steps": [
            "When the gradient is given but \\(c\\) is not, substitute a known point into \\(y = mx + c\\) and solve for \\(c\\).",
            "With two points, first find the gradient from (change in y) over (change in x), then substitute one point to get \\(c\\).",
            "Rearrange any equation into \\(y = mx + c\\) form before reading a gradient. Parallel lines share the same gradient.",
        ],
        "example": {
            "question": "Find the equation of the line through (1, 6) with gradient 3. Give c.",
            "steps": [
                {"label": "Substitute the point", "content": "<p>\\(6 = 3(1) + c\\)</p>"},
                {"label": "Solve for c", "content": "<p>\\(6 = 3 + c\\), so \\(c = 3\\)</p>"},
                {"label": "Check", "content": "<p>\\(3(1) + 3 = 6\\)</p>"},
                {"label": "Answer", "content": "<p>\\(y = 3x + 3\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: two points, perpendicular lines and unknowns",
        "steps": [
            "Gradient from two points: subtract the y-values and divide by the matching subtraction of the x-values, keeping the same order top and bottom.",
            "A perpendicular gradient is the negative reciprocal: flip the fraction and change the sign.",
            "For an unknown coordinate, write the gradient formula, set it equal to the given gradient, and solve.",
        ],
        "example": {
            "question": "Find the gradient of the line through (−1, 2) and (3, 10).",
            "steps": [
                {"label": "Change in y", "content": "<p>\\(10 - 2 = 8\\)</p>"},
                {"label": "Change in x", "content": "<p>\\(3 - (-1) = 4\\)</p>"},
                {"label": "Check", "content": "<p>\\(8 \\div 4 = 2\\)</p>"},
                {"label": "Answer", "content": "<p>gradient \\(= 2\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

guided = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_svg + "<br>A plumber charges £30 to come out, then £20 for every hour of work.",
        "steps": [
            {"say": "No algebra, just the price list. A plumber charges £30 to come out, then £20 per hour.",
             "pre": "A job that takes no time at all (0 hours) still costs £", "post": "", "answer": 30,
             "hint": "You still pay the £30 call-out, even for 0 hours."},
            {"say": "That £30 you always pay, the cost before any work, is the <strong>y-intercept</strong>, the value when \\(x = 0\\).",
             "pre": "Each extra hour adds £", "post": "", "answer": 20, "hint": "The rate is £20 for every hour."},
            {"say": "That £20 per hour, the steady climb, is the <strong>gradient</strong>. So a 3-hour job costs 30 + 20×3:",
             "pre": "£", "post": "", "answer": 90, "hint": "Start at £30, then add £20 three times: 30 + 60."},
            {"say": "Write hours as \\(x\\) and cost as \\(y\\) and you have a line: \\(y = 20x + 30\\). The gradient \\(m = 20\\) is the rate, the intercept \\(c = 30\\) is the start. Every line equation reads the same way."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "A line has gradient 4 and crosses the y-axis at \\((0, -5)\\). Write it as \\(y = mx + c\\).",
            "label": "Together: your first one",
            "steps": [
                {"say": "In \\(y = mx + c\\), \\(m\\) is the gradient and \\(c\\) is where the line meets the y-axis.",
                 "pre": "the gradient goes in the m slot: m = ", "post": "", "answer": 4, "hint": "The gradient is given as 4."},
                {"pre": "the line crosses the y-axis at (0, −5), so c = ", "post": "", "answer": -5,
                 "hint": "Read the y-value where x = 0, keep the minus."},
                {"say": "So the equation is \\(y = 4x - 5\\). Test it at \\(x = 2\\):",
                 "pre": "y = 4×2 − 5 = ", "post": "", "answer": 3, "hint": "8 minus 5."},
                {"pre": "and at x = 0: y = 4×0 − 5 = ", "post": "", "answer": -5,
                 "done": "That is the y-intercept, exactly c. Reading m and c is the whole bronze move.",
                 "hint": "4 times 0 is 0, leaving −5."},
            ],
        },
        "silver": {
            "display": "Find the equation of the line through \\((4, 9)\\) with gradient 2. Give \\(c\\).",
            "label": "Together: the silver move",
            "steps": [
                {"say": "You know \\(m = 2\\) but not \\(c\\). Substitute the point \\((4, 9)\\) into \\(y = mx + c\\).",
                 "pre": "the x part: m×x = 2×4 = ", "post": "", "answer": 8, "hint": "Multiply the gradient by the x-value."},
                {"say": "So \\(9 = 8 + c\\). Take 8 off both sides:",
                 "pre": "c = 9 − 8 = ", "post": "", "answer": 1, "hint": "Subtract 8 from 9."},
                {"say": "The equation is \\(y = 2x + 1\\). Check it lands on the point:",
                 "pre": "2×4 + 1 = ", "post": "", "answer": 9, "hint": "8 plus 1."},
                {"pre": "and the y-intercept, at x = 0: y = 2×0 + 1 = ", "post": "", "answer": 1,
                 "done": "The point fits and c = 1. Substituting a point to find c is the silver move.",
                 "hint": "2 times 0 is 0, leaving 1."},
            ],
        },
        "gold": {
            "display": "Find the equation of the line through \\((2, 5)\\) and \\((6, 17)\\). Give \\(c\\).",
            "label": "Together: the gold move",
            "steps": [
                {"say": "Two points and no gradient, so find \\(m\\) first from (change in y) over (change in x).",
                 "pre": "change in y = 17 − 5 = ", "post": "", "answer": 12, "hint": "Top y minus bottom y."},
                {"pre": "change in x = 6 − 2 = ", "post": "", "answer": 4, "hint": "Right x minus left x."},
                {"pre": "m = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "Divide the change in y by the change in x."},
                {"say": "Now substitute \\((2, 5)\\) into \\(y = 3x + c\\). The x part is 3×2 = 6, so \\(5 = 6 + c\\):",
                 "pre": "c = 5 − 6 = ", "post": "", "answer": -1, "hint": "Subtract 6 from 5."},
                {"say": "Check with the other point \\((6, 17)\\):",
                 "pre": "3×6 + (−1) = ", "post": "", "answer": 17,
                 "done": "It gives 17, so c = −1. Finding m from two points then substituting is the gold move.",
                 "hint": "18 minus 1."},
            ],
        },
    },
}

pd = {
    "method_card": method_card,
    "topic_links": {"prerequisites": []},
    "problem_bank": problem_bank,
    "related_videos": [],
    "worked_examples": [
        {"steps": [
            {"label": "Step 1: Gradient", "content": "<p>\\(m = 2\\) (given).</p>"},
            {"label": "Step 2: y-intercept", "content": "<p>The line passes through \\((0, 3)\\) so \\(c = 3\\).</p>"},
            {"label": "Answer", "content": "<p>\\(y = 2x + 3\\)</p>", "isAnswer": True, "is_answer": True},
        ], "question": "Find the equation of the line through (0, 3) with gradient 2.", "difficulty": "Bronze"},
        {"steps": [
            {"label": "Step 1: Gradient", "content": "<p>\\(m = \\frac{11-5}{4-2} = \\frac{6}{2} = 3\\)</p>"},
            {"label": "Step 2: Find c", "content": "<p>\\(5 = 3(2) + c \\Rightarrow c = 5 - 6 = -1\\)</p>"},
            {"label": "Answer", "content": "<p>\\(y = 3x - 1\\)</p>", "isAnswer": True, "is_answer": True},
        ], "question": "Find the equation of the line through (2, 5) and (4, 11).", "difficulty": "Silver"},
        {"steps": [
            {"label": "Step 1: Perpendicular gradient", "content": "<p>Gradient of A = 4. Perpendicular gradient = \\(-\\frac{1}{4}\\).</p>"},
            {"label": "Step 2: y-intercept", "content": "<p>Passes through \\((0, 7)\\) so \\(c = 7\\).</p>"},
            {"label": "Answer", "content": "<p>\\(y = -\\frac{1}{4}x + 7\\)</p>", "isAnswer": True, "is_answer": True},
        ], "question": "Line A has equation y = 4x − 3. Find the equation of a line perpendicular to A that passes through (0, 7).", "difficulty": "Gold"},
    ],
    "tier_guides": tier_guides,
    "guided": guided,
}

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("wrote", OUT)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
print("g5_svg len", len(g5_svg), "opener_svg len", len(opener_svg))
