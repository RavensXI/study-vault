# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams build for maths-aqa graphs-L03 (Quadratic Graphs)."""
import json, io

MINUS = "−"  # unicode minus

def curve_chart(pts, xmin, xmax, xstep, ymin, ymax, ystep, color):
    return {
        "type": "scatter",
        "data": {"datasets": [{
            "type": "line",
            "data": [{"x": x, "y": y} for x, y in pts],
            "tension": 0.35, "fill": False,
            "borderColor": color, "pointRadius": 0,
            "pointBackgroundColor": color
        }]},
        "options": {"scales": {
            "x": {"min": xmin, "max": xmax, "ticks": {"stepSize": xstep},
                  "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
            "y": {"min": ymin, "max": ymax, "ticks": {"stepSize": ystep},
                  "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "y", "display": True}}
        }}
    }

def parab_pts(f, x0, x1, step):
    pts = []
    n = int(round((x1 - x0) / step))
    for i in range(n + 1):
        x = round(x0 + i * step, 3)
        pts.append((x, round(f(x), 3)))
    return pts

# ---- opener SVG: ball height h = -(t-2)^2 + 4, t in 0..4 ----
def opener_svg():
    def X(t): return 40 + t * (230 - 40) / 4.5
    def Y(h): return 165 - h * (165 - 15) / 5.0
    f = lambda t: -(t - 2) ** 2 + 4
    pts = parab_pts(f, 0, 4, 0.25)
    poly = " ".join("%.1f,%.1f" % (X(t), Y(h)) for t, h in pts)
    s = ['<svg viewBox="0 0 260 200" role="img" aria-label="Curve of a ball\'s height in metres against time in seconds: it rises from 0 at time 0 to a peak of 4 metres at time 2 seconds, then falls back to 0 at time 4 seconds" style="max-width:260px" font-family="Inter, sans-serif">']
    # axes
    s.append('<line x1="40" y1="15" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    s.append('<line x1="40" y1="165" x2="235" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    # y ticks 0..5
    for h in range(0, 6):
        yy = Y(h)
        s.append('<line x1="37" y1="%.1f" x2="40" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (yy, yy))
        s.append('<text x="33" y="%.1f" font-size="9" fill="currentColor" text-anchor="end">%d</text>' % (yy + 3, h))
    # x ticks 0..4
    for t in range(0, 5):
        xx = X(t)
        s.append('<line x1="%.1f" y1="165" x2="%.1f" y2="168" stroke="currentColor" stroke-width="1"/>' % (xx, xx))
        s.append('<text x="%.1f" y="179" font-size="9" fill="currentColor" text-anchor="middle">%d</text>' % (xx, t))
    # curve
    s.append('<polyline points="%s" fill="none" stroke="#3b82f6" stroke-width="2"/>' % poly)
    # peak marker (2,4) and ground points (0,0),(4,0)
    s.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (X(2), Y(4)))
    s.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (X(0), Y(0)))
    s.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (X(4), Y(0)))
    s.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor" text-anchor="middle">peak</text>' % (X(2), Y(4) - 5))
    s.append('<text x="137" y="193" font-size="10" fill="currentColor" text-anchor="middle">time (s)</text>')
    s.append('<text x="12" y="90" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 90)">height (m)</text>')
    s.append('</svg>')
    return "".join(s)

OP_SVG = opener_svg()

# ================= BANK =================
bronze = [
 {"display": "For \\(y = x^2\\), find \\(y\\) when \\(x = 3\\).",
  "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "Squaring 3 means 3 times 3, not 3 times 2.",
  "misconceptions": [{"pattern": "square_as_double", "message": "y = 3² means 3 × 3 = 9, not 3 × 2 = 6. Squaring is a number times itself.", "expect": 6, "note": "doubles instead of squaring"}],
  "guided_steps": [
    {"say": "For \\(y = x^2\\), just square the x-value: multiply it by itself."},
    {"pre": "Write the multiplication: 3 × 3 = ", "post": "", "answer": 9, "hint": "Three lots of three."},
    {"pre": "So when x = 3, y = ", "post": "", "answer": 9, "hint": "That squared value is y.", "phase": "substitute"},
    {"pre": "Check with the symmetric point (−3, y): (−3) × (−3) = ", "post": "", "answer": 9, "hint": "A negative times a negative is positive.", "done": "The parabola is symmetric, so x = 3 and x = −3 both give y = 9.", "phase": "substitute"}]},
 {"display": "For \\(y = x^2 + 1\\), find \\(y\\) when \\(x = 4\\).",
  "solutions": [17], "calculator": False, "input_type": "single_value",
  "hint": "Square the 4 first, then add 1.",
  "misconceptions": [{"pattern": "dropped_constant", "message": "Square first, then add: 4² + 1 = 16 + 1 = 17. Stopping at 16 forgets the + 1.", "expect": 16, "note": "forgets +1"}],
  "guided_steps": [
    {"say": "Square the x-value first, then add the rest of the equation."},
    {"pre": "Square it: 4 × 4 = ", "post": "", "answer": 16, "hint": "Four times four."},
    {"pre": "Add the + 1: 16 + 1 = ", "post": "", "answer": 17, "hint": "Add the constant after squaring.", "phase": "substitute"},
    {"pre": "Check by working it again: 4² + 1 = ", "post": "", "answer": 17, "hint": "Square, then add one.", "done": "16 + 1 = 17, so y = 17.", "phase": "substitute"}]},
 {"display": "For \\(y = x^2 - 5\\), find \\(y\\) when \\(x = 3\\).",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Square the 3 first, then subtract 5.",
  "misconceptions": [{"pattern": "sign_error", "message": "y = 3² " + MINUS + " 5 = 9 " + MINUS + " 5 = 4. Adding instead of subtracting gives 14.", "expect": 14, "note": "adds 5 instead of subtracting"}],
  "guided_steps": [
    {"say": "Square the x-value first, then subtract 5."},
    {"pre": "Square it: 3 × 3 = ", "post": "", "answer": 9, "hint": "Three times three."},
    {"pre": "Subtract 5: 9 " + MINUS + " 5 = ", "post": "", "answer": 4, "hint": "Take five away from the square.", "phase": "substitute"},
    {"pre": "Check: 3² " + MINUS + " 5 = ", "post": "", "answer": 4, "hint": "Square, then subtract five.", "done": "9 " + MINUS + " 5 = 4, so y = 4.", "phase": "substitute"}]},
 {"display": "For \\(y = x^2\\), find \\(y\\) when \\(x = -4\\).",
  "solutions": [16], "calculator": False, "input_type": "single_value",
  "hint": "A negative times a negative gives a positive.",
  "misconceptions": [{"pattern": "negative_square", "message": "(−4)² = (−4) × (−4) = 16. A negative squared is positive, so the answer is not −16.", "expect": -16, "note": "keeps the sign negative"}],
  "guided_steps": [
    {"say": "Squaring a negative: multiply the negative number by itself."},
    {"pre": "(−4) × (−4) = ", "post": "", "answer": 16, "hint": "Negative times negative is positive."},
    {"pre": "So when x = −4, y = ", "post": "", "answer": 16, "hint": "That product is y.", "phase": "substitute"},
    {"pre": "The symmetric point (4, y) matches: 4 × 4 = ", "post": "", "answer": 16, "hint": "Same height on the other side.", "done": "Both x = −4 and x = 4 give y = 16, as the curve is symmetric.", "phase": "substitute"}]},
 {"display": "Does \\(y = x^2 + 2\\) open upward or downward?",
  "options": ["Upward", "Downward", "Left", "Right"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Look at the sign of the x² term: positive opens upward.",
  "misconceptions": [{"pattern": "direction", "message": "The coefficient of x² is positive (+1), so the parabola opens upward, like a valley.", "expect": None}],
  "chart": curve_chart(parab_pts(lambda x: x*x + 2, -3, 3, 0.5), -3.5, 3.5, 1, -1, 12, 2, "#3b82f6")},
 {"display": "For \\(y = x^2 - 4\\), find the y-intercept.",
  "solutions": [-4], "calculator": False, "input_type": "single_value",
  "hint": "Put x = 0; the constant term is left, with its sign.",
  "misconceptions": [{"pattern": "sign_error", "message": "Set x = 0: y = 0 " + MINUS + " 4 = −4. The y-intercept is the constant term, keeping its sign, so it is −4 not 4.", "expect": 4, "note": "drops the minus sign"}],
  "guided_steps": [
    {"say": "The y-intercept is the height where the curve crosses the y-axis, at x = 0."},
    {"pre": "Put x = 0: 0² = ", "post": "", "answer": 0, "hint": "Zero squared is zero."},
    {"pre": "Then subtract 4: 0 " + MINUS + " 4 = ", "post": "", "answer": -4, "hint": "Only the constant term is left.", "phase": "substitute"},
    {"pre": "So the curve meets the y-axis at y = ", "post": "", "answer": -4, "hint": "That crossing height is the intercept.", "done": "At x = 0 only the constant survives, so the y-intercept is −4.", "phase": "substitute"}]},
 {"display": "For \\(y = x^2\\), find \\(y\\) when \\(x = -5\\).",
  "solutions": [25], "calculator": False, "input_type": "single_value",
  "hint": "Multiply −5 by −5; two negatives make a positive.",
  "misconceptions": [{"pattern": "negative_square", "message": "(−5)² = (−5) × (−5) = 25. Negative times negative is positive, so it is 25 not −25.", "expect": -25, "note": "keeps sign negative"}],
  "guided_steps": [
    {"say": "Square the negative: multiply it by itself."},
    {"pre": "(−5) × (−5) = ", "post": "", "answer": 25, "hint": "Negative times negative is positive."},
    {"pre": "So when x = −5, y = ", "post": "", "answer": 25, "hint": "That product is y.", "phase": "substitute"},
    {"pre": "The symmetric point (5, y): 5 × 5 = ", "post": "", "answer": 25, "hint": "Same height on the other side.", "done": "Both x = −5 and x = 5 give y = 25.", "phase": "substitute"}]},
 {"display": "What is the line of symmetry of \\(y = (x - 3)^2\\)?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "For (x − p)², the line of symmetry is x = p.",
  "misconceptions": [{"pattern": "sign_error", "message": "For y = (x " + MINUS + " p)², the line of symmetry is x = p. Here p = 3, so x = 3, not −3.", "expect": -3, "note": "sign flip on p"}],
  "guided_steps": [
    {"say": "For y = (x " + MINUS + " p)², the curve is lowest, and symmetric, where the bracket is zero."},
    {"pre": "The bracket (x " + MINUS + " 3) is zero when x = ", "post": "", "answer": 3, "hint": "What x makes x " + MINUS + " 3 equal 0?"},
    {"pre": "So the line of symmetry is x = ", "post": "", "answer": 3, "hint": "It runs through where the bracket is zero.", "phase": "substitute"},
    {"pre": "Check: at x = 3 the bracket is 3 " + MINUS + " 3 = ", "post": "", "answer": 0, "hint": "Substitute 3 into the bracket.", "done": "The bracket is zero at x = 3, the turning point, so the line of symmetry is x = 3.", "phase": "substitute"}]},
]

silver = [
 {"display": "Find the roots of \\(x^2 - 5x + 6 = 0\\).",
  "solutions": [2, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "Factorise into two brackets, then set each to zero.",
  "misconceptions": [
    {"pattern": "sign_swap", "message": "Factorise (x " + MINUS + " 2)(x " + MINUS + " 3) = 0. Setting each bracket to zero gives x = 2 and x = 3, not −2 and −3.", "expect": [-2, -3], "note": "negates both roots"},
    {"pattern": "partial", "message": "There are two roots. Set both brackets equal to zero, not just one.", "expect": None}],
  "guided_steps": [
    {"say": "Roots are where y = 0. Factorise: two numbers multiply to +6 and add to −5. They are −2 and −3, so (x " + MINUS + " 2)(x " + MINUS + " 3) = 0."},
    {"pre": "First bracket zero: x " + MINUS + " 2 = 0, so x = ", "post": "", "answer": 2, "hint": "Add 2 to both sides."},
    {"pre": "Second bracket zero: x " + MINUS + " 3 = 0, so x = ", "post": "", "answer": 3, "hint": "Add 3 to both sides.", "phase": "substitute"},
    {"pre": "Check the smaller root: 2² " + MINUS + " 5×2 + 6 = 4 " + MINUS + " 10 + 6 = ", "post": "", "answer": 0, "hint": "Substitute x = 2 into the equation.", "done": "It gives 0, so x = 2 is a root; x = 3 works the same way.", "phase": "substitute"}]},
 {"display": "Find the roots of \\(x^2 + x - 12 = 0\\).",
  "solutions": [-4, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "Two numbers multiply to −12 and add to +1.",
  "misconceptions": [
    {"pattern": "sign_swap", "message": "Factorise (x + 4)(x " + MINUS + " 3) = 0. This gives x = −4 and x = 3, not +4 and −3.", "expect": [4, -3], "note": "negates both roots"},
    {"pattern": "factor_pair", "message": "Two numbers multiply to −12 and add to +1: that is +4 and −3, giving (x + 4)(x " + MINUS + " 3) = 0.", "expect": None}],
  "guided_steps": [
    {"say": "Roots are where y = 0. Two numbers multiply to −12 and add to +1: that is +4 and −3, so (x + 4)(x " + MINUS + " 3) = 0."},
    {"pre": "First bracket zero: x + 4 = 0, so x = ", "post": "", "answer": -4, "hint": "Subtract 4 from both sides."},
    {"pre": "Second bracket zero: x " + MINUS + " 3 = 0, so x = ", "post": "", "answer": 3, "hint": "Add 3 to both sides.", "phase": "substitute"},
    {"pre": "Check x = −4: (−4)² + (−4) " + MINUS + " 12 = 16 " + MINUS + " 4 " + MINUS + " 12 = ", "post": "", "answer": 0, "hint": "Substitute x = −4.", "done": "It gives 0, so −4 is a root; 3 works too.", "phase": "substitute"}]},
 {"display": "Find the turning point of \\(y = (x - 4)^2 + 1\\). Give the x-coordinate.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "For (x − p)² + q, the turning point is (p, q).",
  "misconceptions": [{"pattern": "sign_error", "message": "For y = (x " + MINUS + " p)² + q the turning point is (p, q). Here p = 4, so x = 4, not −4.", "expect": -4, "note": "sign flip on p"}],
  "guided_steps": [
    {"say": "For y = (x " + MINUS + " p)² + q, the lowest point is where the bracket is zero."},
    {"pre": "The bracket (x " + MINUS + " 4) is zero when x = ", "post": "", "answer": 4, "hint": "What x makes x " + MINUS + " 4 equal 0?"},
    {"pre": "That value is p, the x-coordinate of the turning point: x = ", "post": "", "answer": 4, "hint": "It matches the number in the bracket.", "phase": "substitute"},
    {"pre": "Check the height there: (4 " + MINUS + " 4)² + 1 = 0 + 1 = ", "post": "", "answer": 1, "hint": "Substitute x = 4.", "done": "At x = 4 the squared bracket is 0, its smallest, so (4, 1) is the turning point.", "phase": "substitute"}]},
 {"display": "Find the turning point of \\(y = (x - 4)^2 + 1\\). Give the y-coordinate.",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "The y-coordinate of the turning point is q, the number added on.",
  "misconceptions": [{"pattern": "confused_coord", "message": "The turning point of y = (x " + MINUS + " 4)² + 1 is (4, 1). The y-coordinate is q = 1, not the 4 from the bracket.", "expect": 4, "note": "reads p instead of q"}],
  "guided_steps": [
    {"say": "For y = (x " + MINUS + " p)² + q, the turning point is (p, q); its height is q."},
    {"pre": "At the turning point the bracket is zero: (x " + MINUS + " 4)² = ", "post": "", "answer": 0, "hint": "The squared bracket is smallest at 0."},
    {"pre": "So y = 0 + 1 = ", "post": "", "answer": 1, "hint": "Add the constant q.", "phase": "substitute"},
    {"pre": "The lowest the curve reaches is y = ", "post": "", "answer": 1, "hint": "That minimum height is the y-coordinate.", "done": "The squared bracket cannot go below 0, so the minimum height is q = 1.", "phase": "substitute"}]},
 {"display": "How many roots does \\(y = x^2 + 3\\) have?",
  "solutions": [0], "calculator": False, "input_type": "single_value",
  "hint": "The lowest value of x² + 3 is 3, above the x-axis.",
  "misconceptions": [{"pattern": "assumes_two", "message": "The smallest value of x² + 3 is 3 (at x = 0), so the curve never reaches the x-axis. It has 0 roots, not 2.", "expect": 2, "note": "assumes every quadratic has 2 roots"}],
  "guided_steps": [
    {"say": "Roots are where the curve meets the x-axis (y = 0). Find the lowest point first."},
    {"pre": "The smallest value of x² is at x = 0, where x² = ", "post": "", "answer": 0, "hint": "Squares are never negative."},
    {"pre": "So the lowest y is 0 + 3 = ", "post": "", "answer": 3, "hint": "Add the constant 3.", "phase": "substitute"},
    {"pre": "The lowest point is at y = 3, above the axis, so the number of roots is ", "post": "", "answer": 0, "hint": "It never reaches y = 0.", "done": "The curve stays above the x-axis, so it has 0 roots.", "phase": "substitute"}],
  "chart": curve_chart(parab_pts(lambda x: x*x + 3, -3, 3, 0.5), -3.5, 3.5, 1, -1, 13, 2, "#22c55e")},
 {"display": "Find the roots of \\(x^2 - 9 = 0\\).",
  "solutions": [-3, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "x² = 9 has both a positive and a negative square root.",
  "misconceptions": [{"pattern": "root_not_taken", "message": "x² = 9 means x = √9 = ±3, not ±9. The roots are −3 and 3.", "expect": [-9, 9], "note": "reads 9 without square-rooting"}],
  "guided_steps": [
    {"say": "Set y = 0: x² " + MINUS + " 9 = 0, so x² = 9. Take the square root, remembering both signs."},
    {"pre": "The positive square root of 9 is x = ", "post": "", "answer": 3, "hint": "What number times itself is 9?"},
    {"pre": "The other root is the negative: x = ", "post": "", "answer": -3, "hint": "A square has a plus and a minus root.", "phase": "substitute"},
    {"pre": "Check: (−3)² " + MINUS + " 9 = 9 " + MINUS + " 9 = ", "post": "", "answer": 0, "hint": "Substitute x = −3.", "done": "Both +3 and −3 square to 9, so both are roots.", "phase": "substitute"}]},
 {"display": "What is the y-intercept of \\(y = 2x^2 - 3x + 7\\)?",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Put x = 0; only the constant term c is left.",
  "misconceptions": [{"pattern": "wrong_term", "message": "Set x = 0: y = 0 " + MINUS + " 0 + 7 = 7. The y-intercept is the constant term c = 7, not the coefficient 2.", "expect": 2, "note": "reads leading coefficient"}],
  "guided_steps": [
    {"say": "The y-intercept is the value at x = 0. Every term with an x disappears."},
    {"pre": "The 2x² term at x = 0: 2 × 0² = ", "post": "", "answer": 0, "hint": "Zero squared is zero."},
    {"pre": "The " + MINUS + "3x term at x = 0: −3 × 0 = ", "post": "", "answer": 0, "hint": "Anything times 0 is 0.", "phase": "substitute"},
    {"pre": "So y = 0 " + MINUS + " 0 + 7 = ", "post": "", "answer": 7, "hint": "Only the constant is left.", "done": "At x = 0 only the constant term 7 survives, so the y-intercept is 7.", "phase": "substitute"}]},
]

gold = [
 {"display": "Find the roots of \\(x^2 + 2x - 15 = 0\\).",
  "solutions": [-5, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "Two numbers multiply to −15 and add to +2.",
  "misconceptions": [
    {"pattern": "sign_swap", "message": "Factorise (x + 5)(x " + MINUS + " 3) = 0, giving x = −5 and x = 3, not +5 and −3.", "expect": [5, -3], "note": "negates both roots"},
    {"pattern": "factor_pair", "message": "Two numbers multiply to −15 and add to +2: that is +5 and −3, giving (x + 5)(x " + MINUS + " 3) = 0.", "expect": None}],
  "guided_steps": [
    {"say": "Roots are where y = 0. Two numbers multiply to −15 and add to +2: that is +5 and −3, so (x + 5)(x " + MINUS + " 3) = 0."},
    {"pre": "First bracket zero: x + 5 = 0, so x = ", "post": "", "answer": -5, "hint": "Subtract 5 from both sides."},
    {"pre": "Second bracket zero: x " + MINUS + " 3 = 0, so x = ", "post": "", "answer": 3, "hint": "Add 3 to both sides.", "phase": "substitute"},
    {"pre": "Check x = 3: 3² + 2×3 " + MINUS + " 15 = 9 + 6 " + MINUS + " 15 = ", "post": "", "answer": 0, "hint": "Substitute x = 3.", "done": "It gives 0, confirming x = 3 (and x = −5) are the roots.", "phase": "substitute"}]},
 {"display": "The turning point of a quadratic is \\((3, -2)\\) and it opens upward. Write the equation in the form \\(y = (x - a)^2 + b\\). What is \\(b\\)?",
  "solutions": [-2], "calculator": False, "input_type": "single_value",
  "hint": "b is the y-coordinate of the turning point, with its sign.",
  "misconceptions": [{"pattern": "sign_error", "message": "The turning point (3, −2) gives y = (x " + MINUS + " 3)² " + MINUS + " 2, so b = −2, not 2.", "expect": 2, "note": "drops the sign on q"}],
  "guided_steps": [
    {"say": "For a turning point (p, q), the equation is y = (x " + MINUS + " p)² + q. Match p and q to the coordinates."},
    {"pre": "The x-coordinate of the turning point is 3, so a = ", "post": "", "answer": 3, "hint": "a matches the first coordinate."},
    {"pre": "The y-coordinate is −2, so b = ", "post": "", "answer": -2, "hint": "b is the second coordinate, with its sign.", "phase": "substitute"},
    {"pre": "Check at x = 3: (3 " + MINUS + " 3)² + (−2) = 0 + (−2) = ", "post": "", "answer": -2, "hint": "Substitute x = 3.", "done": "At x = 3 the height is −2, matching the turning point, so b = −2.", "phase": "substitute"}]},
 {"display": "\\(y = -x^2 + 6x - 5\\). Is the turning point a maximum or minimum?",
  "options": ["Maximum", "Minimum", "Neither", "Both"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "A negative x² coefficient opens the curve downward.",
  "misconceptions": [{"pattern": "direction", "message": "The coefficient of x² is negative (−1), so the parabola opens downward, giving a maximum turning point.", "expect": None}],
  "chart": curve_chart(parab_pts(lambda x: -(x*x) + 6*x - 5, 0, 6, 0.5), -0.5, 6.5, 1, -6, 5, 2, "#ef4444")},
 {"display": "For \\(y = x^2 - 8x + 12\\), find the x-coordinate of the turning point.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "The turning point sits halfway between the two roots.",
  "misconceptions": [{"pattern": "forgot_halve", "message": "The roots are (x " + MINUS + " 2)(x " + MINUS + " 6) = 0, so x = 2 and x = 6. Halfway between them is (2 + 6) ÷ 2 = 4, not 8.", "expect": 8, "note": "adds roots without halving"}],
  "guided_steps": [
    {"say": "The turning point lies on the line of symmetry, halfway between the roots."},
    {"pre": "Factorise: (x " + MINUS + " 2)(x " + MINUS + " 6) = 0. First root x = ", "post": "", "answer": 2, "hint": "Set the first bracket to zero."},
    {"pre": "Second root x = ", "post": "", "answer": 6, "hint": "Set the second bracket to zero."},
    {"pre": "Halfway between: (2 + 6) ÷ 2 = ", "post": "", "answer": 4, "hint": "Average the two roots.", "phase": "substitute"},
    {"pre": "Check the height: 4² " + MINUS + " 8×4 + 12 = 16 " + MINUS + " 32 + 12 = ", "post": "", "answer": -4, "hint": "Substitute x = 4.", "done": "x = 4 is midway between the roots, so it is the turning point's x-coordinate (height −4).", "phase": "substitute"}]},
 {"display": "For \\(y = x^2 - 8x + 12\\), find the y-coordinate of the turning point.",
  "solutions": [-4], "calculator": False, "input_type": "single_value",
  "hint": "Substitute the turning point's x-value into the equation.",
  "misconceptions": [{"pattern": "sign_error", "message": "At x = 4, y = 16 " + MINUS + " 32 + 12 = −4. Missing the minus gives 4.", "expect": 4, "note": "sign slip in the sum"}],
  "guided_steps": [
    {"say": "The turning point is at x = 4 (halfway between the roots 2 and 6). Substitute to find its height."},
    {"pre": "Square the x: 4 × 4 = ", "post": "", "answer": 16, "hint": "Four times four."},
    {"pre": "The " + MINUS + "8x term: −8 × 4 = ", "post": "", "answer": -32, "hint": "Keep the minus sign."},
    {"pre": "Add them with the + 12: 16 " + MINUS + " 32 + 12 = ", "post": "", "answer": -4, "hint": "Combine the three terms.", "phase": "substitute"},
    {"pre": "So the lowest point is at y = ", "post": "", "answer": -4, "hint": "That is the turning point's height.", "done": "16 " + MINUS + " 32 + 12 = −4, the minimum height of the curve.", "phase": "substitute"}]},
]

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Substitute an x-value into a quadratic, read the y-intercept, and say which way the parabola opens.",
 "silver_description": "Factorise to find roots, and read the turning point from completed-square form y = (x − p)² + q.",
 "gold_description": "Find a turning point from the line of symmetry, and work with vertex form and the direction of opening.",
}

tier_guides = {
 "bronze": {
   "title": "Bronze: reading and evaluating quadratics",
   "steps": [
     "Substitute an x-value by <strong>squaring it first</strong>, then apply the rest of the equation. A negative squared is positive: \\((-2)^2 = 4\\).",
     "The parabola opens <strong>upward</strong> when the \\(x^2\\) term is positive and <strong>downward</strong> when it is negative.",
     "The <strong>y-intercept</strong> is the constant term (put \\(x = 0\\)). For \\(y = (x - p)^2\\), the line of symmetry is \\(x = p\\)."],
   "example": {"question": "For y = x² − 3, find y when x = 4.",
     "steps": [
       {"label": "Square", "content": "4 × 4 = 16"},
       {"label": "Subtract", "content": "16 − 3"},
       {"label": "Check", "content": "x = −4 gives the same height"},
       {"label": "Answer", "content": "y = 13", "isAnswer": True, "is_answer": True}]}},
 "silver": {
   "title": "Silver: roots and the turning point",
   "steps": [
     "The <strong>roots</strong> are where \\(y = 0\\). Factorise into two brackets and set each bracket equal to zero.",
     "For \\(y = (x - p)^2 + q\\), the <strong>turning point</strong> is \\((p, q)\\): read \\(p\\) from the bracket and \\(q\\) from the constant.",
     "A quadratic has 0, 1 or 2 roots. If its lowest point sits above the x-axis, it has none."],
   "example": {"question": "Find the roots of x² − 2x − 8 = 0.",
     "steps": [
       {"label": "Factorise", "content": "(x − 4)(x + 2) = 0"},
       {"label": "First root", "content": "x − 4 = 0, so x = 4"},
       {"label": "Check", "content": "Second bracket: x + 2 = 0"},
       {"label": "Roots", "content": "x = 4 and x = −2", "isAnswer": True, "is_answer": True}]}},
 "gold": {
   "title": "Gold: symmetry and vertex form",
   "steps": [
     "The turning point lies on the <strong>line of symmetry</strong>, halfway between the roots: average them, then substitute to find the height.",
     "Vertex form \\(y = (x - p)^2 + q\\) has turning point \\((p, q)\\). Match \\(p\\) and \\(q\\) to the coordinates you are given.",
     "A positive \\(x^2\\) term gives a <strong>minimum</strong> turning point; a negative one gives a <strong>maximum</strong>."],
   "example": {"question": "For y = x² − 6x + 8, find the turning point.",
     "steps": [
       {"label": "Roots", "content": "(x − 2)(x − 4) = 0, so 2 and 4"},
       {"label": "Symmetry", "content": "(2 + 4) ÷ 2 = 3"},
       {"label": "Height", "content": "9 − 18 + 8 = −1"},
       {"label": "Turning point", "content": "(3, −1)", "isAnswer": True, "is_answer": True}]}},
}

guided = {
 "opener": {
   "display": OP_SVG + "<p>A ball is thrown straight up. The graph shows its height (in metres) at each moment (in seconds) until it lands.</p>",
   "steps": [
     {"pre": "What is the greatest height the ball reaches? ", "post": " m", "answer": 4, "hint": "Read the height at the very top of the arc."},
     {"pre": "At what time does the ball come back down and land (height 0 again)? ", "post": " s", "answer": 4, "hint": "Read the time where the curve returns to height 0."},
     {"say": "The peak you read is the <strong>turning point</strong> (2, 4), the highest point of the curve. The two moments at ground level, \\(t = 0\\) and \\(t = 4\\), are the <strong>roots</strong> where height is 0, and the curve is symmetric about the peak. Every quadratic graph \\(y = ax^2 + bx + c\\) has this same arch (or valley) shape, with a turning point and up to two roots."}]},
 "teach": {
   "bronze": {
     "display": "For \\(y = x^2 - 3\\), find \\(y\\) when \\(x = 4\\), and again when \\(x = -4\\).",
     "steps": [
       {"say": "To find y, square the x-value first, then apply the rest of the equation."},
       {"pre": "Square the 4: 4 × 4 = ", "post": "", "answer": 16, "hint": "Four times four."},
       {"pre": "Subtract 3: 16 " + MINUS + " 3 = ", "post": "", "answer": 13, "hint": "Take three off the square."},
       {"pre": "Now the other x: (−4) × (−4) = ", "post": "", "answer": 16, "hint": "Negative times negative is positive."},
       {"pre": "Subtract 3 again: 16 " + MINUS + " 3 = ", "post": "", "answer": 13, "hint": "Same subtraction.", "done": "Both x = 4 and x = −4 give y = 13. A parabola is symmetric, so opposite x-values share a height."}]},
   "silver": {
     "display": "Find the roots of \\(x^2 - 2x - 8 = 0\\).",
     "steps": [
       {"say": "Roots are where y = 0. Factorise into two brackets, then set each to zero."},
       {"pre": "Two numbers multiply to −8 and add to −2. The positive one is ", "post": "", "answer": 2, "hint": "Try +2 and −4: 2 × (−4) = −8."},
       {"pre": "The negative one is ", "post": "", "answer": -4, "hint": "It pairs with +2 to add to −2."},
       {"pre": "So (x + 2)(x " + MINUS + " 4) = 0. First bracket zero: x + 2 = 0, so x = ", "post": "", "answer": -2, "hint": "Subtract 2 from both sides."},
       {"pre": "Second bracket zero: x " + MINUS + " 4 = 0, so x = ", "post": "", "answer": 4, "hint": "Add 4 to both sides.", "done": "Roots x = −2 and x = 4, where the curve crosses the x-axis."}]},
   "gold": {
     "display": "For \\(y = x^2 - 6x + 8\\), find the turning point.",
     "steps": [
       {"say": "The turning point lies on the line of symmetry, halfway between the roots."},
       {"pre": "Factorise: two numbers multiply to 8 and add to −6, both negative. First root x = ", "post": "", "answer": 2, "hint": "(x " + MINUS + " 2)(x " + MINUS + " 4) = 0."},
       {"pre": "Second root x = ", "post": "", "answer": 4, "hint": "The other bracket set to zero."},
       {"pre": "Line of symmetry is halfway: (2 + 4) ÷ 2 = ", "post": "", "answer": 3, "hint": "Average the roots."},
       {"pre": "Substitute x = 3: 9 " + MINUS + " 18 + 8 = ", "post": "", "answer": -1, "hint": "Work out 3² − 6×3 + 8.", "done": "Turning point (3, −1), the minimum of the curve."}]}}
}

method_card = {
 "title": "How to Plot and Interpret Quadratic Graphs",
 "steps": [
   "Make a table of x-values (include negatives) and work out each y.",
   "Plot the points and join them with a smooth curve, never a ruler.",
   "Roots are where the curve crosses the x-axis (y = 0).",
   "The turning point is the lowest or highest point; for y = (x − p)² + q it is (p, q)."],
 "content": "<p>A <strong>quadratic graph</strong> is a U-shaped curve (parabola), \\(y = ax^2 + bx + c\\). If \\(a > 0\\) it opens upward (a minimum); if \\(a < 0\\) it opens downward (a maximum).</p><p>The <strong>roots</strong> are where the curve meets the x-axis (\\(y = 0\\)); a quadratic has 0, 1 or 2. The <strong>turning point</strong> is the vertex, and the <strong>line of symmetry</strong> runs vertically through it. For \\(y = (x - p)^2 + q\\), the turning point is \\((p, q)\\) and the line of symmetry is \\(x = p\\).</p>",
 "example": "<p><strong>Plot \\(y = x^2 - 4x + 3\\).</strong> Roots at \\(x = 1\\) and \\(x = 3\\) (where \\(y = 0\\)); turning point \\((2, -1)\\), the lowest point. ✔</p>"
}

# preserved fields from live
live = json.load(io.open("_live_graphsL03.json", encoding="utf-8"))

pd = {
 "method_card": method_card,
 "topic_links": live["topic_links"],
 "problem_bank": problem_bank,
 "related_videos": live["related_videos"],
 "worked_examples": live["worked_examples"],
 "tier_guides": tier_guides,
 "guided": guided,
}

json.dump(pd, io.open("lesson_maths-aqa_graphs-L03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_maths-aqa_graphs-L03.json")
