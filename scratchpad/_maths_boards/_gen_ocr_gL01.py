# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for maths-ocr graphs-L01."""
import json, os

MINUS = "−"  # unicode minus for student-facing text
def n(v):
    """Format a signed number for plain pre/say text (brackets on negatives, unicode minus)."""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if v < 0:
        return "(" + MINUS + str(abs(v)) + ")"
    return str(v)

def num(v):
    return int(v) if isinstance(v, float) and v.is_integer() else v

# ---- generic two-point gradient walk ----
def grad_walk(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    assert run != 0
    g = rise / run
    g = num(g)
    assert isinstance(g, int) or (rise % run == 0) or True
    steps = [
        {"say": "Gradient means rise over run: how far up for how far across. Start with the rise, the change in y."},
        {"pre": "Rise = " + n(y2) + " " + MINUS + " " + n(y1) + " = ", "post": "", "answer": num(rise),
         "hint": "Take the first y from the second y."},
        {"pre": "Run = " + n(x2) + " " + MINUS + " " + n(x1) + " = ", "post": "", "answer": num(run),
         "hint": "Take the first x from the second x. Subtracting a negative adds."},
        {"pre": "Gradient = rise " + chr(0x00F7) + " run = " + n(rise) + " " + chr(0x00F7) + " " + str(run) + " = ",
         "post": "", "answer": g, "hint": "Divide the rise by the run.", "phase": "substitute"},
        {"pre": "Check: gradient " + chr(0x00D7) + " run = " + n(g) + " " + chr(0x00D7) + " " + str(run) + " = ",
         "post": "", "answer": num(rise), "hint": "Multiply back. It should return the rise.",
         "done": "It gives the rise back, so the gradient is right.", "phase": "substitute"}
    ]
    return steps, g

DIV = chr(0x00F7)
TIMES = chr(0x00D7)

# ---------------- SVG linear-graph builder ----------------
def line_svg(aria, xmax, ymax, ystep, line_pts, label_pts, colour, ylabel, xlabel):
    """Axis with ticks (x:0..xmax step1, y:0..ymax step ystep), a straight line through line_pts,
    and small labels at label_pts=[(x,y,text),...]. All text currentColor, theme-safe."""
    x0px, x1px = 40.0, 230.0
    ytop, ybot = 15.0, 165.0
    def X(x): return x0px + (x / xmax) * (x1px - x0px)
    def Y(y): return ybot - (y / ymax) * (ybot - ytop)
    parts = []
    parts.append('<svg viewBox="0 0 260 195" role="img" aria-label="%s" style="max-width:260px" font-family="Inter, sans-serif">' % aria)
    # axes
    parts.append('<line x1="40" y1="15" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="40" y1="165" x2="235" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    # y ticks
    yv = 0
    while yv <= ymax + 1e-9:
        py = Y(yv)
        parts.append('<line x1="37" y1="%.1f" x2="40" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (py, py))
        parts.append('<text x="33" y="%.1f" font-size="9" fill="currentColor" text-anchor="end">%d</text>' % (py + 3, yv))
        yv += ystep
    # x ticks
    for xv in range(0, xmax + 1):
        px = X(xv)
        parts.append('<line x1="%.1f" y1="165" x2="%.1f" y2="168" stroke="currentColor" stroke-width="1"/>' % (px, px))
        parts.append('<text x="%.1f" y="179" font-size="9" fill="currentColor" text-anchor="middle">%d</text>' % (px, xv))
    # line
    (lx1, ly1), (lx2, ly2) = line_pts
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>' % (X(lx1), Y(ly1), X(lx2), Y(ly2), colour))
    # labelled points
    for (px_, py_, txt) in label_pts:
        parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/>' % (X(px_), Y(py_), colour))
        parts.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor">%s</text>' % (X(px_) + 5, Y(py_) - 2, txt))
    # axis titles
    parts.append('<text x="137" y="192" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % xlabel)
    parts.append('<text x="12" y="90" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 90)">%s</text>' % ylabel)
    parts.append('</svg>')
    return "".join(parts)

# ============================================================
# PROBLEM BANK
# ============================================================
def two_point_problem(x1, y1, x2, y2, hint, misc, disp=None):
    steps, g = grad_walk(x1, y1, x2, y2)
    d = disp or ("Find the gradient of the line through \\((%s, %s)\\) and \\((%s, %s)\\)." %
                 (n_latex(x1), n_latex(y1), n_latex(x2), n_latex(y2)))
    return {"display": d, "solutions": [g], "calculator": False, "input_type": "single_value",
            "hint": hint, "misconceptions": misc, "guided_steps": steps}

def n_latex(v):
    # inside LaTeX use unicode minus to match existing OCR display style
    return (MINUS + str(abs(v))) if v < 0 else str(v)

pb = {"bronze": [], "silver": [], "gold": []}

# ---- BRONZE ----
pb["bronze"].append(two_point_problem(0, 2, 3, 8,
    "Rise over run: the change in y divided by the change in x.",
    [{"pattern": "rise_run_inverted",
      "message": "Rise = 8 " + MINUS + " 2 = 6, Run = 3 " + MINUS + " 0 = 3. Gradient = 6 " + DIV + " 3 = 2. Run over rise gives 0.5, which is upside down; the vertical change goes on top.",
      "expect": 0.5, "note": "inverted run/rise = 3/6"}]))

pb["bronze"].append(two_point_problem(1, 4, 5, 16,
    "Work out the rise and the run, then divide rise by run.",
    [{"pattern": "forgot_to_divide",
      "message": "Rise = 16 " + MINUS + " 4 = 12 is only the top of the fraction. Divide by the run: 12 " + DIV + " 4 = 3.",
      "expect": 12, "note": "stops at rise before dividing"}]))

# b2: intercept of y=3x+5
pb["bronze"].append({
    "display": "A line has equation \\(y = 3x + 5\\). What is the y-intercept?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "The y-intercept is c, the number with no x next to it.",
    "misconceptions": [{"pattern": "confused_m_and_c",
        "message": "In y = mx + c the y-intercept is c, the number on its own. Here c = 5. The 3 is the gradient.",
        "expect": 3, "note": "reports m instead of c"}],
    "guided_steps": [
        {"say": "In y = mx + c, the gradient m sits in front of x and the intercept c stands alone."},
        {"pre": "The number in front of x is the gradient m = ", "post": "", "answer": 3, "hint": "It is written just before the x."},
        {"pre": "The number on its own is the intercept c = ", "post": "", "answer": 5, "hint": "It is the term with no x."},
        {"pre": "The y-intercept is c, so the answer is ", "post": "", "answer": 5, "hint": "The intercept is c, not m.", "phase": "substitute"},
        {"pre": "Check at x = 0: y = m " + TIMES + " 0 + c = ", "post": "", "answer": 5, "hint": "Anything times 0 is 0, leaving just c.",
         "done": "At x = 0 the line sits at c, which is the y-intercept.", "phase": "substitute"}
    ]})

# b3: gradient of y=4x-3
pb["bronze"].append({
    "display": "A line has equation \\(y = 4x - 3\\). What is the gradient?",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "The gradient is m, the number multiplying x.",
    "misconceptions": [{"pattern": "confused_m_and_c",
        "message": "The gradient is m, the number in front of x. Here m = 4. The " + MINUS + "3 is the y-intercept.",
        "expect": -3, "note": "reports c instead of m"}],
    "guided_steps": [
        {"say": "In y = mx + c, the gradient m is the number multiplying x."},
        {"pre": "The number on its own is the intercept c = ", "post": "", "answer": -3, "hint": "It is the term with no x."},
        {"pre": "At x = 0: y = ", "post": "", "answer": -3, "hint": "That is just c."},
        {"pre": "At x = 1: y = 4 " + TIMES + " 1 + " + n(-3) + " = ", "post": "", "answer": 1, "hint": "Work out m times 1, then add c.", "phase": "substitute"},
        {"pre": "The gradient is the rise for one step across: 1 " + MINUS + " " + n(-3) + " = ", "post": "", "answer": 4,
         "hint": "Subtract the two y-values.", "done": "y rises by m for each step, so the gradient is m.", "phase": "substitute"}
    ]})

pb["bronze"].append(two_point_problem(2, 1, 6, 5,
    "Work out the rise and the run, then divide.",
    [{"pattern": "forgot_to_divide",
      "message": "Rise = 5 " + MINUS + " 1 = 4 is only the top. Divide by the run: 4 " + DIV + " 4 = 1.",
      "expect": 4, "note": "stops at rise"}]))

# b5: y=5x+1, x=3
pb["bronze"].append({
    "display": "The line \\(y = 5x + 1\\). What is the value of \\(y\\) when \\(x = 3\\)?",
    "solutions": [16], "calculator": False, "input_type": "single_value",
    "hint": "Multiply 5 by 3 first, then add 1.",
    "misconceptions": [{"pattern": "order_of_operations",
        "message": "Multiply before adding: 5 " + TIMES + " 3 = 15, then 15 + 1 = 16. Doing 3 + 1 first, then " + TIMES + " 5, gives 20.",
        "expect": 20, "note": "5*(3+1)=20"}],
    "guided_steps": [
        {"say": "Substitute the x-value into y = mx + c, doing the multiplication first."},
        {"pre": "The gradient part: 5 " + TIMES + " 3 = ", "post": "", "answer": 15, "hint": "Multiply m by x before touching c."},
        {"pre": "Now add the intercept: 15 + 1 = ", "post": "", "answer": 16, "hint": "Add c to what you just found.", "phase": "substitute"},
        {"pre": "Check the point (3, 16) fits: 5 " + TIMES + " 3 + 1 = ", "post": "", "answer": 16, "hint": "Work the equation once more.",
         "done": "The point fits the line, so y is correct.", "phase": "substitute"}
    ]})

# b6: chart y=2x+1, read y at x=3  (preserve chart, improved fill:false)
chart_b6 = {"type": "line", "data": {"labels": [0,1,2,3,4,5],
    "datasets": [{"data": [1,3,5,7,9,11], "fill": False, "borderColor": "#3b82f6",
                  "pointRadius": 5, "pointBackgroundColor": "#3b82f6", "backgroundColor": "rgba(59,130,246,0.1)"}]},
    "options": {"scales": {"x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
        "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 2}, "title": {"text": "y", "display": True}, "beginAtZero": True}}}}
pb["bronze"].append({
    "display": "The graph shows a straight line. What is the value of \\(y\\) when \\(x = 3\\)?",
    "solutions": [7], "calculator": False, "input_type": "single_value", "chart": chart_b6,
    "hint": "Trace up from x = 3 to the line, then across to the y-axis.",
    "misconceptions": [{"pattern": "value_vs_gradient",
        "message": "The line climbs 2 for each step across, but the question wants the height at x = 3, which is 7. The 2 is the gradient, not the value asked for.",
        "expect": 2, "note": "gives gradient 2 instead of the y-value"}],
    "guided_steps": [
        {"say": "Read the height of the line at the x-value the question asks for."},
        {"pre": "At x = 0 the line is at y = ", "post": "", "answer": 1, "hint": "Where does it cross the y-axis?"},
        {"pre": "At x = 1 the line is at y = ", "post": "", "answer": 3, "hint": "Trace up from x = 1 to the line."},
        {"pre": "Each step across adds (3 " + MINUS + " 1) = ", "post": "", "answer": 2, "hint": "The jump in y for one step in x."},
        {"pre": "From x = 1 (y = 3), two more steps to x = 3: 3 + 2 " + TIMES + " 2 = ", "post": "", "answer": 7, "hint": "Add two more steps of 2.", "phase": "substitute"},
        {"pre": "Check on the graph at x = 3: y = ", "post": "", "answer": 7, "hint": "Read straight up to the line.",
         "done": "Reading and calculating agree, so y = 7.", "phase": "substitute"}
    ]})

# b7: chart y=-2x+10, gradient
chart_b7 = {"type": "line", "data": {"labels": [0,1,2,3,4,5],
    "datasets": [{"data": [10,8,6,4,2,0], "fill": False, "borderColor": "#ef4444",
                  "pointRadius": 5, "pointBackgroundColor": "#ef4444", "backgroundColor": "rgba(239,68,68,0.1)"}]},
    "options": {"scales": {"x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
        "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 2}, "title": {"text": "y", "display": True}, "beginAtZero": True}}}}
pb["bronze"].append({
    "display": "The graph shows a straight line. What is the gradient?",
    "solutions": [-2], "calculator": False, "input_type": "single_value", "chart": chart_b7,
    "hint": "The line falls, so the gradient is negative; use rise over run.",
    "misconceptions": [{"pattern": "sign_error",
        "message": "The line goes down, so the gradient is negative. Reading the steepness as 2 and dropping the minus reverses the line's direction; it is " + MINUS + "2.",
        "expect": 2, "note": "drops the sign"}],
    "guided_steps": [
        {"say": "Read two clear points, then use rise over run, keeping the sign."},
        {"pre": "At x = 0 the line is at y = ", "post": "", "answer": 10, "hint": "Where it crosses the y-axis."},
        {"pre": "At x = 1 the line is at y = ", "post": "", "answer": 8, "hint": "Trace up from x = 1 to the line."},
        {"pre": "Rise = 8 " + MINUS + " 10 = ", "post": "", "answer": -2, "hint": "Second y minus first y; it falls, so it is negative."},
        {"pre": "Run = 1 " + MINUS + " 0 = ", "post": "", "answer": 1, "hint": "Difference in the x values.", "phase": "substitute"},
        {"pre": "Gradient = rise " + DIV + " run = " + n(-2) + " " + DIV + " 1 = ", "post": "", "answer": -2, "hint": "Divide the rise by the run.",
         "done": "The line drops 2 for each step across, so the gradient is " + MINUS + "2.", "phase": "substitute"}
    ]})

# ---- SILVER ----
pb["silver"].append(two_point_problem(-1, 4, 3, -8,
    "The line falls steeply; use rise over run and keep the sign.",
    [{"pattern": "sign_error",
      "message": "Rise = " + n(-8) + " " + MINUS + " 4 = " + MINUS + "12, Run = 3 " + MINUS + " " + n(-1) + " = 4, so gradient = " + MINUS + "12 " + DIV + " 4 = " + MINUS + "3. Dropping the minus gives 3, but the line slopes down.",
      "expect": 3, "note": "drops the sign"}],
    disp="Find the gradient of the line through \\((%s, 4)\\) and \\((3, %s)\\)." % (n_latex(-1), n_latex(-8))))

# s1: y=mx+3 through (2,11), find m
pb["silver"].append({
    "display": "The line \\(y = mx + 3\\) passes through \\((2, 11)\\). Find \\(m\\).",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Substitute the point, take 3 off both sides, then divide by 2.",
    "misconceptions": [{"pattern": "forgot_to_divide",
        "message": "11 = 2m + 3, so 2m = 8 and m = 4. Writing 8 stops before dividing by 2.",
        "expect": 8, "note": "stops at 2m=8"}],
    "guided_steps": [
        {"say": "Put the point into y = mx + c and peel away the known parts."},
        {"pre": "Take the intercept off both sides: 11 " + MINUS + " 3 = ", "post": "", "answer": 8, "hint": "Subtract c from y."},
        {"pre": "So 2 " + TIMES + " m = 8. Divide by 2: m = ", "post": "", "answer": 4, "hint": "Divide by the number in front of m.", "phase": "substitute"},
        {"pre": "Check: 4 " + TIMES + " 2 + 3 = ", "post": "", "answer": 11, "hint": "Put m back and confirm the point.",
         "done": "It returns the point's y, so m is right.", "phase": "substitute"}
    ]})

# s2: 2y=6x+10, gradient
pb["silver"].append({
    "display": "A line has equation \\(2y = 6x + 10\\). What is the gradient?",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Divide every term by 2 to reach y = mx + c first.",
    "misconceptions": [{"pattern": "forgot_step",
        "message": "Divide every term by 2 first: y = 3x + 5. The gradient is 3, not 6.",
        "expect": 6, "note": "reads 6 without dividing"}],
    "guided_steps": [
        {"say": "Get the equation into y = mx + c first by dividing every term by 2."},
        {"pre": "Divide the x term by 2: 6 " + DIV + " 2 = ", "post": "x", "answer": 3, "hint": "Divide the number in front of x."},
        {"pre": "Divide the constant by 2: 10 " + DIV + " 2 = ", "post": "", "answer": 5, "hint": "Divide the lone number too."},
        {"pre": "Now y = 3x + 5. The gradient is the number in front of x: ", "post": "", "answer": 3, "hint": "Read the coefficient of x.", "phase": "substitute"},
        {"pre": "Check: from x = 0 (y = 5) to x = 1 (y = 8), the rise is 8 " + MINUS + " 5 = ", "post": "", "answer": 3, "hint": "One step across raises y by the gradient.",
         "done": "y climbs by the gradient each step, confirming it.", "phase": "substitute"}
    ]})

pb["silver"].append(two_point_problem(-2, -3, 4, 9,
    "Both coordinates change sign; subtracting a negative adds.",
    [{"pattern": "negative_run_slip",
      "message": "Run = 4 " + MINUS + " " + n(-2) + " = 6, not 4 " + MINUS + " 2 = 2. Subtracting a negative adds. Rise = 12, so gradient = 12 " + DIV + " 6 = 2.",
      "expect": 6, "note": "run taken as 2 gives 12/2=6"}],
    disp="Find the gradient of the line through \\((%s, %s)\\) and \\((4, 9)\\)." % (n_latex(-2), n_latex(-3))))

# s4 (rewritten): (0,-2)(4,18) m=5
steps_s4, g_s4 = grad_walk(0, -2, 4, 18)
pb["silver"].append({
    "display": "A line passes through \\((0, %s)\\) and \\((4, 18)\\). What is the equation of the line?  Give the value of \\(m\\)." % n_latex(-2),
    "solutions": [g_s4], "calculator": False, "input_type": "single_value",
    "hint": "Rise over run between the two points gives m.",
    "misconceptions": [{"pattern": "forgot_to_divide",
        "message": "Rise = 18 " + MINUS + " " + n(-2) + " = 20, Run = 4 " + MINUS + " 0 = 4. Gradient = 20 " + DIV + " 4 = 5. Stopping at the rise gives 20.",
        "expect": 20, "note": "stops at rise"}],
    "guided_steps": steps_s4})

# s5 (rewritten): 3y-9x=18, y-intercept=6
pb["silver"].append({
    "display": "A line has equation \\(3y - 9x = 18\\). What is the y-intercept?",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Rearrange to y = mx + c, then read the number on its own.",
    "misconceptions": [{"pattern": "forgot_step",
        "message": "Rearrange: 3y = 9x + 18, then divide every term by 3: y = 3x + 6. The y-intercept is 6, not 18.",
        "expect": 18, "note": "reads 18 without dividing"}],
    "guided_steps": [
        {"say": "Rearrange into y = mx + c, then read the intercept c."},
        {"pre": "Move " + MINUS + "9x across: 3y = 9x + 18. Divide the x term by 3: 9 " + DIV + " 3 = ", "post": "x", "answer": 3, "hint": "Divide the number in front of x."},
        {"pre": "Divide the constant by 3: 18 " + DIV + " 3 = ", "post": "", "answer": 6, "hint": "Divide the lone number too."},
        {"pre": "Now y = 3x + 6. The y-intercept is the number on its own: ", "post": "", "answer": 6, "hint": "Read the term with no x.", "phase": "substitute"},
        {"pre": "Check at x = 0: y = 3 " + TIMES + " 0 + 6 = ", "post": "", "answer": 6, "hint": "At x = 0 only c is left.",
         "done": "At x = 0 the line sits at c, the y-intercept.", "phase": "substitute"}
    ]})

# s6: (1,7)(3,3) find y-intercept = 9
pb["silver"].append({
    "display": "Two points on a line are \\((1, 7)\\) and \\((3, 3)\\). Find the y-intercept.",
    "solutions": [9], "calculator": False, "input_type": "single_value",
    "hint": "Find the gradient first, then substitute a point to find c.",
    "misconceptions": [{"pattern": "read_gradient_not_intercept",
        "message": "The gradient is " + MINUS + "2, but the question asks for the y-intercept. Substituting (1, 7) into y = " + MINUS + "2x + c gives c = 9.",
        "expect": -2, "note": "gives gradient not intercept"}],
    "guided_steps": [
        {"say": "Find the gradient, then feed a point back in to reach c."},
        {"pre": "Rise = 3 " + MINUS + " 7 = ", "post": "", "answer": -4, "hint": "Second y minus first y."},
        {"pre": "Run = 3 " + MINUS + " 1 = ", "post": "", "answer": 2, "hint": "Second x minus first x."},
        {"pre": "Gradient m = " + n(-4) + " " + DIV + " 2 = ", "post": "", "answer": -2, "hint": "Divide rise by run."},
        {"pre": "Use (1, 7): the mx part is " + n(-2) + " " + TIMES + " 1 = ", "post": "", "answer": -2, "hint": "Multiply the gradient by that x.", "phase": "substitute"},
        {"pre": "So 7 = " + n(-2) + " + c, giving c = 7 " + MINUS + " " + n(-2) + " = ", "post": "", "answer": 9, "hint": "Take the mx part off the y-value.",
         "done": "That c is where the line meets the y-axis.", "phase": "substitute"}
    ]})

# ---- GOLD ----
pb["gold"].append(two_point_problem(-3, 11, 5, -5,
    "The line falls; use rise over run and keep the sign.",
    [{"pattern": "sign_error",
      "message": "Rise = " + n(-5) + " " + MINUS + " 11 = " + MINUS + "16, Run = 5 " + MINUS + " " + n(-3) + " = 8, so gradient = " + MINUS + "16 " + DIV + " 8 = " + MINUS + "2. Dropping the minus gives 2, but the line slopes down.",
      "expect": 2, "note": "drops the sign"}],
    disp="A line passes through \\((%s, 11)\\) and \\((5, %s)\\). Find the gradient." % (n_latex(-3), n_latex(-5))))

# g1: (2,5)(6,17) find c = -1
pb["gold"].append({
    "display": "The line \\(y = mx + c\\) passes through \\((2, 5)\\) and \\((6, 17)\\). Find the value of \\(c\\).",
    "solutions": [-1], "calculator": False, "input_type": "single_value",
    "hint": "Find the gradient first, then substitute one point to find c.",
    "misconceptions": [{"pattern": "sign_error",
        "message": "From 5 = 3 " + TIMES + " 2 + c: c = 5 " + MINUS + " 6 = " + MINUS + "1. Adding instead (5 + 6) gives 11.",
        "expect": 11, "note": "adds mx instead of subtracting"}],
    "guided_steps": [
        {"say": "First find the gradient, then use a point to pin down c."},
        {"pre": "Rise = 17 " + MINUS + " 5 = ", "post": "", "answer": 12, "hint": "Second y minus first y."},
        {"pre": "Run = 6 " + MINUS + " 2 = ", "post": "", "answer": 4, "hint": "Second x minus first x."},
        {"pre": "Gradient m = 12 " + DIV + " 4 = ", "post": "", "answer": 3, "hint": "Divide rise by run."},
        {"pre": "Now use (2, 5): the mx part is 3 " + TIMES + " 2 = ", "post": "", "answer": 6, "hint": "Multiply the gradient by that x.", "phase": "substitute"},
        {"pre": "So 5 = 6 + c, giving c = 5 " + MINUS + " 6 = ", "post": "", "answer": -1, "hint": "Take the mx part off the y-value.",
         "done": "That c completes y = mx + c.", "phase": "substitute"}
    ]})

# g2: parallel? A y=2x+1, B (0,7)(2,3) -> 0
pb["gold"].append({
    "display": "Line A: \\(y = 2x + 1\\). Line B passes through \\((0, 7)\\) and \\((2, 3)\\). Are the lines parallel? Enter 1 for Yes, 0 for No.",
    "solutions": [0], "calculator": False, "input_type": "single_value",
    "hint": "Find each line's gradient; parallel lines have equal gradients.",
    "misconceptions": [{"pattern": "sign_error",
        "message": "Line B gradient = (3 " + MINUS + " 7) " + DIV + " (2 " + MINUS + " 0) = " + MINUS + "4 " + DIV + " 2 = " + MINUS + "2, while Line A is 2. They differ, so the lines are not parallel; the answer is 0. Getting 1 usually means B's minus sign was dropped.",
        "expect": 1, "note": "sign drop makes both look like 2, answers Yes"}],
    "guided_steps": [
        {"say": "Parallel lines have equal gradients. Find each gradient and compare."},
        {"pre": "Line A is y = 2x + 1, so its gradient is ", "post": "", "answer": 2, "hint": "The number in front of x."},
        {"pre": "Line B rise = 3 " + MINUS + " 7 = ", "post": "", "answer": -4, "hint": "Second y minus first y."},
        {"pre": "Line B run = 2 " + MINUS + " 0 = ", "post": "", "answer": 2, "hint": "Second x minus first x."},
        {"pre": "Line B gradient = " + n(-4) + " " + DIV + " 2 = ", "post": "", "answer": -2, "hint": "Divide rise by run.", "phase": "substitute"},
        {"pre": "The gradients are 2 and " + MINUS + "2. Equal? Enter 1 for Yes, 0 for No: ", "post": "", "answer": 0, "hint": "They are different, so not parallel.",
         "done": "Different gradients means the lines are not parallel.", "phase": "substitute"}
    ]})

# g3: 5x+2y=20 gradient = -2.5
pb["gold"].append({
    "display": "A line has equation \\(5x + 2y = 20\\). Find the gradient.",
    "solutions": [-2.5], "calculator": False, "input_type": "single_value",
    "hint": "Rearrange to y = mx + c, then read the number in front of x.",
    "misconceptions": [{"pattern": "forgot_step",
        "message": "Move 5x across: 2y = " + MINUS + "5x + 20. You must still divide every term by 2: y = " + MINUS + "2.5x + 10, so the gradient is " + MINUS + "2.5. Reading " + MINUS + "5 skips the division.",
        "expect": -5, "note": "reads -5 without dividing"}],
    "guided_steps": [
        {"say": "Rearrange into y = mx + c, then read the gradient."},
        {"pre": "Move 5x to the other side. The x term becomes " + MINUS + "5x, coefficient ", "post": "", "answer": -5, "hint": "Take 5x off both sides; the sign flips."},
        {"pre": "Divide every term by 2. The x coefficient: " + n(-5) + " " + DIV + " 2 = ", "post": "", "answer": -2.5, "hint": "Halve the coefficient.", "phase": "substitute"},
        {"pre": "So y = " + MINUS + "2.5x + 10. The gradient is the number in front of x: ", "post": "", "answer": -2.5, "hint": "Read the coefficient of x.",
         "done": "The rearranged form gives gradient " + MINUS + "2.5.", "phase": "substitute"}
    ]})

# g4: midpoint (a,3)(7,11)=(5,7) find a = 3
pb["gold"].append({
    "display": "The midpoint of \\((a, 3)\\) and \\((7, 11)\\) is \\((5, 7)\\). Find \\(a\\).",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "The midpoint x is the average of the two x-values.",
    "misconceptions": [{"pattern": "midpoint_subtract",
        "message": "Midpoint x = (a + 7) " + DIV + " 2 = 5, so a + 7 = 10 and a = 3. Doing 5 " + MINUS + " 7 = " + MINUS + "2 skips doubling the midpoint.",
        "expect": -2, "note": "5-7=-2"}],
    "guided_steps": [
        {"say": "The midpoint x is the average of the two x-values. Work backwards to find a."},
        {"pre": "The midpoint x is 5, and averaging halves, so double it back: 2 " + TIMES + " 5 = ", "post": "", "answer": 10, "hint": "Undo the divide-by-2."},
        {"pre": "That equals a + 7, so a = 10 " + MINUS + " 7 = ", "post": "", "answer": 3, "hint": "Take 7 off both sides.", "phase": "substitute"},
        {"pre": "Check the midpoint x: (3 + 7) " + DIV + " 2 = ", "post": "", "answer": 5, "hint": "Average the two x-values.",
         "done": "The x-values average to 5, so a = 3.", "phase": "substitute"}
    ]})

pb["bronze_description"] = "Read a gradient or intercept straight from y = mx + c, or find a gradient from two friendly points."
pb["silver_description"] = "Handle negatives and fractions: read gradients from points, rearrange equations, and find m or c."
pb["gold_description"] = "Work with negative coordinates, rearrange harder equations, and use gradients for c, parallel lines and midpoints."

# ============================================================
# tier_guides
# ============================================================
tier_guides = {
    "bronze": {
        "title": "Bronze: reading m and c",
        "steps": [
            "In \\(y = mx + c\\), the <strong>gradient</strong> is m (the number in front of x) and the <strong>y-intercept</strong> is c (the number on its own).",
            "For a gradient from two points, work out <strong>rise " + DIV + " run</strong>: the change in y over the change in x.",
            "To find y at a value of x, substitute it in and multiply before you add."
        ],
        "example": {"question": "Find the gradient of the line through (1, 4) and (3, 10).",
            "steps": [{"label": "Rise", "content": "10 " + MINUS + " 4 = 6"},
                      {"label": "Run", "content": "3 " + MINUS + " 1 = 2"},
                      {"label": "Check", "content": "Rise over run = 6 " + DIV + " 2"},
                      {"label": "Gradient", "content": "m = 3", "isAnswer": True, "is_answer": True}]}},
    "silver": {
        "title": "Silver: negatives and rearranging",
        "steps": [
            "When coordinates are negative, remember subtracting a negative <strong>adds</strong>, and keep the sign on a falling gradient.",
            "If an equation is not yet \\(y = mx + c\\), divide every term to rearrange it before reading m or c.",
            "To find m from a point, substitute it in, take the intercept off, then divide."
        ],
        "example": {"question": "For 2y = 8x + 6, find the gradient.",
            "steps": [{"label": "Divide by 2", "content": "y = 4x + 3"},
                      {"label": "Read m", "content": "m is the number in front of x"},
                      {"label": "Check", "content": "x = 0 to x = 1 raises y by 4"},
                      {"label": "Gradient", "content": "m = 4", "isAnswer": True, "is_answer": True}]}},
    "gold": {
        "title": "Gold: equations, parallels and midpoints",
        "steps": [
            "To find c, work out the gradient first, then substitute one point into \\(y = mx + c\\) and solve for c.",
            "Two lines are <strong>parallel</strong> when their gradients are equal, so compare the two m values.",
            "A midpoint is the average of the coordinates: double the midpoint and subtract the known value to find a missing one."
        ],
        "example": {"question": "A line through (1, 5) and (4, 14). Find c.",
            "steps": [{"label": "Gradient", "content": "(14 " + MINUS + " 5) " + DIV + " (4 " + MINUS + " 1) = 3"},
                      {"label": "Use (1, 5)", "content": "5 = 3 " + TIMES + " 1 + c"},
                      {"label": "Check", "content": "3 " + TIMES + " 1 = 3, so 5 = 3 + c"},
                      {"label": "Intercept", "content": "c = 2", "isAnswer": True, "is_answer": True}]}}
}

# ============================================================
# guided: opener + teach
# ============================================================
# Opener: taxi fare y = 2x + 3 (pickup £3, £2 per mile)
opener_svg = line_svg(
    "Line graph of taxi cost in pounds against miles travelled, a straight line rising from 3 pounds at 0 miles by 2 pounds each mile",
    xmax=4, ymax=12, ystep=3, line_pts=((0, 3), (4, 11)),
    label_pts=[(0, 3, "£3"), (1, 5, "£5")], colour="#3b82f6",
    ylabel="cost (£)", xlabel="miles")

opener = {
    "display": opener_svg + "<p>A taxi charges a fixed pickup fee, then the same amount for every mile. The graph shows the total cost as the journey gets longer.</p>",
    "steps": [
        {"pre": "What does the ride cost before you have gone anywhere, at 0 miles? £", "post": "", "answer": 3,
         "hint": "Read the height of the line where it meets 0 miles."},
        {"pre": "Each mile the cost climbs by the same step. From 0 miles (£3) to 1 mile (£5) it goes up by £", "post": "", "answer": 2,
         "hint": "How much taller is the line one mile along?"},
        {"say": "That steady £2 a mile is the line's <strong>gradient</strong>, and the £3 pickup fee is the <strong>y-intercept</strong>. In symbols the line is \\(y = 2x + 3\\). Finding \"how much per step\" is exactly what gradient measures."}
    ]
}

teach_bronze = {
    "display": "A line passes through \\((1, 3)\\) and \\((5, 15)\\). Find its gradient.",
    "steps": [
        {"say": "Gradient is rise over run. Find each piece, then divide."},
        {"pre": "Rise = 15 " + MINUS + " 3 = ", "post": "", "answer": 12, "hint": "Second y minus first y."},
        {"pre": "Run = 5 " + MINUS + " 1 = ", "post": "", "answer": 4, "hint": "Second x minus first x."},
        {"pre": "Gradient = rise " + DIV + " run = 12 " + DIV + " 4 = ", "post": "", "answer": 3, "hint": "Divide the rise by the run."},
        {"pre": "Check: 3 " + TIMES + " 4 = ", "post": "", "answer": 12, "hint": "Gradient times run should return the rise.",
         "done": "It gives the rise back, so the gradient is 3."}
    ]
}

teach_silver_svg = line_svg(
    "Straight line through the points 0 comma 1, 1 comma 3, 2 comma 5 and 3 comma 7",
    xmax=4, ymax=10, ystep=2, line_pts=((0, 1), (4, 9)),
    label_pts=[(0, 1, ""), (2, 5, "")], colour="#ef4444",
    ylabel="y", xlabel="x")
teach_silver = {
    "display": teach_silver_svg + "<p>The graph shows a straight line. Find its gradient.</p>",
    "steps": [
        {"say": "Read two clean points off the line, then use rise over run."},
        {"pre": "At x = 0 the line is at y = ", "post": "", "answer": 1, "hint": "Where does it cross the y-axis?"},
        {"pre": "At x = 2 the line is at y = ", "post": "", "answer": 5, "hint": "Trace up from x = 2 to the line."},
        {"pre": "Rise = 5 " + MINUS + " 1 = ", "post": "", "answer": 4, "hint": "Difference in the y readings."},
        {"pre": "Run = 2 " + MINUS + " 0 = ", "post": "", "answer": 2, "hint": "Difference in the x values."},
        {"pre": "Gradient = 4 " + DIV + " 2 = ", "post": "", "answer": 2, "hint": "Divide rise by run.",
         "done": "The line climbs 2 for every 1 across, so the gradient is 2."}
    ]
}

teach_gold = {
    "display": "A line passes through \\((1, 5)\\) and \\((4, 17)\\). Find \\(c\\) in \\(y = mx + c\\).",
    "steps": [
        {"say": "Find the gradient, then feed a point back in to reach c."},
        {"pre": "Rise = 17 " + MINUS + " 5 = ", "post": "", "answer": 12, "hint": "Second y minus first y."},
        {"pre": "Run = 4 " + MINUS + " 1 = ", "post": "", "answer": 3, "hint": "Second x minus first x."},
        {"pre": "Gradient m = 12 " + DIV + " 3 = ", "post": "", "answer": 4, "hint": "Divide rise by run."},
        {"pre": "Use (1, 5): the mx part is 4 " + TIMES + " 1 = ", "post": "", "answer": 4, "hint": "Multiply gradient by that x."},
        {"pre": "So 5 = 4 + c, giving c = 5 " + MINUS + " 4 = ", "post": "", "answer": 1, "hint": "Take the mx part off the y-value.",
         "done": "c = 1, so the line is y = 4x + 1."}
    ]
}

guided = {"opener": opener, "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold}}

# ============================================================
# method_card (slim, <=4 steps, <=140 words)  &  worked_examples (de-em-dashed)
# ============================================================
method_card = {
    "title": "How to Plot and Read Linear Graphs",
    "steps": [
        "Read m and c straight from \\(y = mx + c\\): m is the gradient, c is the y-intercept.",
        "Gradient between two points is rise " + DIV + " run, with the change in y on top.",
        "To plot, substitute three x-values, plot the pairs, and join them with a ruler.",
        "To find c from a point, put the point and gradient into \\(y = mx + c\\) and solve."
    ],
    "content": "<p>A <strong>linear graph</strong> is a straight line \\(y = mx + c\\), where \\(m\\) is the <strong>gradient</strong> (steepness) and \\(c\\) is the <strong>y-intercept</strong> (where it crosses the y-axis).</p><p>The gradient is the rise divided by the run: \\(m = \\frac{y_2 - y_1}{x_2 - x_1}\\), keeping the vertical change on top. A positive gradient slopes up, a negative one slopes down.</p><p>To read a value, trace from the known axis to the line, then across to the other axis.</p>",
    "example": "<p><strong>Plot \\(y = 2x - 1\\).</strong> At \\(x = 0, 1, 2\\) the y-values are \\(-1, 1, 3\\), giving points \\((0,-1), (1,1), (2,3)\\). Join them with a ruler. Gradient \\(= \\frac{3 - (-1)}{2 - 0} = 2\\)</p>"
}

worked_examples = [
    {"steps": [{"label": "Step 1: Rise", "content": "<p>\\(y_2 - y_1 = 9 - 3 = 6\\)</p>"},
               {"label": "Step 2: Run", "content": "<p>\\(x_2 - x_1 = 4 - 1 = 3\\)</p>"},
               {"label": "Answer", "content": "<p>Gradient \\(= \\frac{6}{3} = 2\\)</p>", "isAnswer": True, "is_answer": True}],
     "question": "Find the gradient of the line through (1, 3) and (4, 9).", "difficulty": "Bronze"},
    {"steps": [{"label": "Step 1: Rise", "content": "<p>\\(-1 - 5 = -6\\)</p>"},
               {"label": "Step 2: Run", "content": "<p>\\(3 - 0 = 3\\)</p>"},
               {"label": "Answer", "content": "<p>Gradient \\(= \\frac{-6}{3} = -2\\)</p>", "isAnswer": True, "is_answer": True}],
     "question": "A line passes through (0, 5) and (3, " + MINUS + "1). Find the gradient.", "difficulty": "Silver"},
    {"steps": [{"label": "Step 1: Identify two points", "content": "<p>From the graph: \\((0, 1)\\) and \\((2, 5)\\).</p>"},
               {"label": "Step 2: Find the equation", "content": "<p>\\(m = \\frac{5-1}{2-0} = 2\\), \\(c = 1\\), so \\(y = 2x + 1\\).</p>"},
               {"label": "Answer", "content": "<p>When \\(x = 4\\): \\(y = 2(4) + 1 = 9\\)</p>", "isAnswer": True, "is_answer": True}],
     "question": "The graph shows a straight line. Read the y-value when x = 4.", "difficulty": "Gold"}
]

# ============================================================
# assemble
# ============================================================
pd = {
    "method_card": method_card,
    "topic_links": {"prerequisites": []},
    "problem_bank": pb,
    "related_videos": [],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided
}

# ---- self-check: final numeric box lands on solution for each bank problem ----
def last_num(steps):
    vals = [s["answer"] for s in steps if s.get("answer") is not None]
    return vals

problems_final = {}
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if not gs:
            continue
        boxes = last_num(gs)
        sol = p["solutions"][0]
        # the solution must appear as one of the phase:substitute answers
        sub_vals = [s["answer"] for s in gs if s.get("phase") == "substitute" and s.get("answer") is not None]
        assert sol in sub_vals, "%s[%d] solution %r not reached in completion phase %r" % (tier, i, sol, sub_vals)

out = os.path.join(os.path.dirname(__file__), "lesson_maths-ocr_graphs-L01.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("bronze sols", [p["solutions"] for p in pb["bronze"]])
print("silver sols", [p["solutions"] for p in pb["silver"]])
print("gold sols", [p["solutions"] for p in pb["gold"]])
