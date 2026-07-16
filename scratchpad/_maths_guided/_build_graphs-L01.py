# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open('_live_graphs-L01.json', encoding='utf-8'))
pb_live = live['problem_bank']

# preserve chart objects exactly from live silver
chart_s0 = pb_live['silver'][0]['chart']
chart_s1 = pb_live['silver'][1]['chart']
chart_s2 = pb_live['silver'][2]['chart']

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s):
    return {"say": s}

# ---------------- METHOD CARD (slim) ----------------
method_card = {
    "title": "Plotting and Reading Linear Graphs",
    "steps": [
        "In \\(y = mx + c\\), m is the gradient (steepness) and c is the y-intercept (where the line meets the y-axis).",
        "Gradient from two points: \\(m = \\dfrac{\\text{change in }y}{\\text{change in }x}\\) (rise over run).",
        "To plot: substitute a few x-values, plot the points, join them with a ruler.",
        "To read a value: go from the known axis across to the line, then to the other axis."
    ],
    "content": "<p>A <strong>linear graph</strong> is a straight line \\(y = mx + c\\): \\(m\\) is the <strong>gradient</strong> and \\(c\\) is the <strong>y-intercept</strong>. The gradient is how much \\(y\\) changes for each step of 1 in \\(x\\), found with rise over run, \\(m = \\frac{y_2 - y_1}{x_2 - x_1}\\). Put the vertical change on top. A positive gradient slopes up, a negative gradient slopes down. To read a value off a line, go from the known value across to the line, then to the other axis.</p>",
    "example": "<p><strong>Find the gradient of the line through \\((1, 3)\\) and \\((4, 9)\\).</strong></p><p>Rise \\(= 9 - 3 = 6\\), run \\(= 4 - 1 = 3\\), so \\(m = \\frac{6}{3} = 2\\).</p>"
}

# ---------------- GOLD ----------------
gold = []

gold.append({
    "display": "Find the gradient of the line through \\((-3, -5)\\) and \\((1, 7)\\).",
    "solutions": [3],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Rise over run: 7 − (−5) on top of 1 − (−3); minus a minus is plus.",
    "misconceptions": [
        {"check": "common", "expect": -6, "pattern": "sign_error",
         "message": "Rise = 7 − (−5) = 12, run = 1 − (−3) = 4, so gradient = 12 ÷ 4 = 3. Getting −6 means the run was taken as 1 − 3 = −2, dropping one of the double negatives. Subtracting a negative adds."}
    ],
    "guided_steps": [
        sayonly("Find the gradient with rise over run. Rise is the change in y, and subtracting a negative adds."),
        box("Rise: 7 − (−5) = ", 12, "7 + 5, because minus a minus is plus."),
        box("Run: 1 − (−3) = ", 4, "1 + 3, again minus a minus is plus."),
        box("12 ÷ 4 = ", 3, "How many 4s in 12?", say="Now divide rise by run.", phase="substitute"),
        box("−5 + 12 = ", 7, "−5 + 12.", say="Check by stepping from (−3, −5): a run of 4 across at gradient 3 climbs 4 × 3 = 12.", done="That reaches y = 7 at x = 1, matching the point, so the gradient 3 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "A line passes through \\((2, 3)\\) and \\((8, 15)\\). Write the equation in the form \\(y = mx + c\\). What is the value of \\(c\\)?",
    "solutions": [-1],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Find the gradient first, then put one point into y = mx + c and solve for c.",
    "misconceptions": [
        {"check": "common", "expect": 7, "pattern": "wrong_formula",
         "message": "m = (15 − 3) ÷ (8 − 2) = 12 ÷ 6 = 2. Then 3 = 2(2) + c, so c = 3 − 4 = −1. Getting 7 means 4 was added instead of subtracted when moving it across."}
    ],
    "guided_steps": [
        sayonly("Find the gradient first, with rise over run."),
        box("Rise: 15 − 3 = ", 12, "Subtract the y-values."),
        box("Run: 8 − 2 = ", 6, "Subtract the x-values."),
        box("12 ÷ 6 = ", 2, "How many 6s in 12?", say="So the gradient is 12 ÷ 6."),
        box("c = 3 − 4 = ", -1, "3 take away 4 goes below zero.", say="Now find c. Put the gradient 2 and the point (2, 3) into \\(y = mx + c\\). The gradient part is 2 × 2 = 4, so 3 = 4 + c.", phase="substitute"),
        box("2 × 8 + (−1) = ", 15, "16 − 1.", say="Check with the other point (8, 15):", done="16 − 1 = 15, matching the point, so c = −1 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "The line \\(y = mx + 5\\) passes through \\((4, 21)\\). Find \\(m\\).",
    "solutions": [4],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Put the point into the equation, take the 5 across, then divide by 4.",
    "misconceptions": [
        {"check": "common", "expect": None, "pattern": "wrong_formula",
         "message": "Substitute the point: 21 = m(4) + 5, so 4m = 16 and m = 4."}
    ],
    "guided_steps": [
        box("21 − 5 = ", 16, "Subtract the intercept 5.", say="Put the point into \\(y = mx + 5\\). With x = 4 and y = 21 the equation is \\(21 = 4m + 5\\). Take the 5 across first."),
        box("16 ÷ 4 = ", 4, "How many 4s in 16?", say="So \\(4m = 16\\). Divide by 4 to get m.", phase="substitute"),
        box("4 × 4 + 5 = ", 21, "16 + 5.", say="Check by putting m = 4 back in at x = 4.", done="16 + 5 = 21, matching the point, so m = 4 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "Two points on a line are \\((-2, 9)\\) and \\((4, -3)\\). What is the gradient?",
    "solutions": [-2],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Rise over run, keeping the subtraction order and the signs.",
    "misconceptions": [
        {"check": "common", "expect": -6, "pattern": "sign_error",
         "message": "Rise = −3 − 9 = −12, run = 4 − (−2) = 6, so gradient = −12 ÷ 6 = −2. Getting −6 means the run was taken as 4 − 2 = 2, dropping the double negative."}
    ],
    "guided_steps": [
        sayonly("Rise over run again. Rise is the change in y."),
        box("Rise: −3 − 9 = ", -12, "−3 take away 9."),
        box("Run: 4 − (−2) = ", 6, "4 + 2, minus a minus is plus."),
        box("−12 ÷ 6 = ", -2, "−12 shared into 6 is negative.", say="Divide rise by run.", phase="substitute"),
        box("9 + (−12) = ", -3, "9 − 12.", say="Check from (−2, 9): a run of 6 at gradient −2 changes y by 6 × (−2) = −12.", done="That reaches y = −3 at x = 4, matching the point, so gradient −2 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "A line has equation \\(2y = 10x - 8\\). What is the gradient?",
    "solutions": [5],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Divide every term by 2 to get y = mx + c first, then read the gradient.",
    "misconceptions": [
        {"check": "common", "expect": 10, "pattern": "forgot_step",
         "message": "Rearrange first: divide every term by 2 to get y = 5x − 4. The gradient is 5, not 10. Reading 10 skips the rearranging step."}
    ],
    "guided_steps": [
        box("10 ÷ 2 = ", 5, "Half of the 10 in front of x.", say="The equation is not yet in \\(y = mx + c\\) form: it says \\(2y\\), not \\(y\\). Divide every term by 2. Start with the x term."),
        box("−8 ÷ 2 = ", -4, "Half of −8.", say="And the constant term."),
        box("Gradient = ", 5, "It is the coefficient of x after dividing.", say="So \\(y = 5x − 4\\). The gradient is the number in front of x. Write it down.", phase="substitute"),
        box("2 × 5 = ", 10, "2 × 5.", say="Check: multiply your \\(y = 5x − 4\\) back by 2.", done="That gives 10x, matching the original 10x, so the gradient 5 is right.", phase="substitute")
    ]
})

# ---------------- BRONZE ----------------
bronze = []

bronze.append({
    "display": "Find the gradient of the line through \\((0, 2)\\) and \\((3, 8)\\).",
    "solutions": [2],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Gradient = rise ÷ run; put the change in y on top.",
    "misconceptions": [
        {"check": "common", "expect": 0.5, "pattern": "rise_run_inverted",
         "message": "Gradient = rise ÷ run = (8 − 2) ÷ (3 − 0) = 6 ÷ 3 = 2. Getting 0.5 means run was put on top instead of rise. The vertical change goes on top."}
    ],
    "guided_steps": [
        sayonly("Gradient is rise over run. Rise first."),
        box("Rise: 8 − 2 = ", 6, "Subtract the y-values."),
        box("Run: 3 − 0 = ", 3, "Subtract the x-values."),
        box("6 ÷ 3 = ", 2, "How many 3s in 6?", say="Divide rise by run.", phase="substitute"),
        box("2 + 6 = ", 8, "2 + 6.", say="Check from (0, 2): three steps across at gradient 2 add 3 × 2 = 6.", done="That reaches y = 8 at x = 3, matching the point, so gradient 2 is right.", phase="substitute")
    ]
})

# NEW B1 (replaces duplicate): negative gradient from two points
bronze.append({
    "display": "Find the gradient of the line through \\((0, 8)\\) and \\((2, 4)\\).",
    "solutions": [-2],
    "calculator": False,
    "input_type": "single_value",
    "hint": "The line falls, so the gradient is negative: work out rise ÷ run keeping the subtraction order.",
    "misconceptions": [
        {"check": "common", "expect": 2, "pattern": "sign_error",
         "message": "Subtract the y-values in the same order as the x-values: rise = 4 − 8 = −4, run = 2 − 0 = 2, so gradient = −4 ÷ 2 = −2. Getting +2 means the rise was taken as 8 − 4."},
        {"check": "common", "expect": -0.5, "pattern": "rise_run_inverted",
         "message": "Gradient = rise ÷ run = −4 ÷ 2 = −2. Putting run over rise gives −0.5. The vertical change goes on top."}
    ],
    "guided_steps": [
        box("Rise: 4 − 8 = ", -4, "4 take away 8 goes below zero.", say="Rise over run. This line goes downhill, so expect a negative gradient. Rise is the change in y, keeping the order."),
        box("Run: 2 − 0 = ", 2, "Subtract the x-values."),
        box("−4 ÷ 2 = ", -2, "−4 shared into 2 is negative.", say="Divide rise by run.", phase="substitute"),
        box("8 + (−4) = ", 4, "8 − 4.", say="Check from (0, 8): two steps across at gradient −2 change y by 2 × (−2) = −4.", done="That reaches y = 4 at x = 2, matching the point, so gradient −2 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "A line has equation \\(y = 4x + 3\\). What is the y-intercept?",
    "solutions": [3],
    "calculator": False,
    "input_type": "single_value",
    "hint": "In \\(y = mx + c\\), the y-intercept is the constant c, not the number in front of x.",
    "misconceptions": [
        {"check": "common", "expect": 4, "pattern": "confused_m_and_c",
         "message": "In y = mx + c, the y-intercept is c (the constant). Here c = 3, not 4. The 4 is the gradient."}
    ],
    "guided_steps": [
        box("Number in front of x: ", 4, "The coefficient of x.", say="The equation is in \\(y = mx + c\\) form. Read off the number in front of x first (the gradient m)."),
        box("y-intercept c = ", 3, "The number with no x attached.", say="The y-intercept is the other number, the constant on its own. Write it down."),
        box("4 × 0 = ", 0, "Anything times 0 is 0.", say="Check it: the y-intercept is y when x = 0. Work out the x part first.", phase="substitute"),
        box("0 + 3 = ", 3, "0 + 3.", say="Then add the constant.", done="So at x = 0, y = 3: the line crosses the y-axis at 3, confirming c = 3.", phase="substitute")
    ]
})

bronze.append({
    "display": "A line has equation \\(y = 5x - 1\\). What is the gradient?",
    "solutions": [5],
    "calculator": False,
    "input_type": "single_value",
    "hint": "The gradient is the number multiplying x in \\(y = mx + c\\).",
    "misconceptions": [
        {"check": "common", "expect": -1, "pattern": "confused_m_and_c",
         "message": "In y = mx + c, the gradient is m (the number multiplying x). Here m = 5, not −1. The −1 is the y-intercept."}
    ],
    "guided_steps": [
        box("Constant on its own: ", -1, "The number with no x, keep its minus sign.", say="The equation is in \\(y = mx + c\\) form. Read off the constant first (the y-intercept c)."),
        box("Gradient m = ", 5, "The coefficient of x.", say="The gradient is the other number, the one multiplying x. Write it down."),
        box("5 × 1 − 1 = ", 4, "5 − 1.", say="Check the gradient means y rises 5 for each step in x. Go from x = 0 to x = 1. At x = 0, \\(y = 5 × 0 − 1 = −1\\). At x = 1:", phase="substitute"),
        box("4 − (−1) = ", 5, "4 + 1.", say="So y went from −1 to 4 as x went from 0 to 1.", done="y rose by 5 for one step in x, confirming the gradient is 5.", phase="substitute")
    ]
})

bronze.append({
    "display": "For the line \\(y = 2x + 3\\), find \\(y\\) when \\(x = 5\\).",
    "solutions": [13],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Multiply 2 by 5 first, then add 3 (multiplication before addition).",
    "misconceptions": [
        {"check": "common", "expect": 16, "pattern": "substitution_error",
         "message": "Substitute: y = 2(5) + 3 = 10 + 3 = 13. Getting 16 means 5 and 3 were added first (2 × 8). Multiply before you add."}
    ],
    "guided_steps": [
        box("2 × 5 = ", 10, "Two fives.", say="Substitute x = 5 into \\(y = 2x + 3\\). Do the multiply before the add. Work out the x part first."),
        box("10 + 3 = ", 13, "Add 3 to your 10.", say="Now add the constant.", phase="substitute"),
        box("2 × 5 + 3 = ", 13, "10 then + 3.", say="Check by reading the sentence back: 2 lots of 5, then 3 more.", done="Multiplying first then adding gives 13, so that is right.", phase="substitute")
    ]
})

# CHANGED B5 (dedupe from 3 to 4): points (0,4)&(2,12)
bronze.append({
    "display": "A line passes through \\((0, 4)\\) and \\((2, 12)\\). What is the gradient?",
    "solutions": [4],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Gradient = rise ÷ run; put the change in y on top.",
    "misconceptions": [
        {"check": "common", "expect": 0.25, "pattern": "rise_run_inverted",
         "message": "Rise = 12 − 4 = 8, run = 2 − 0 = 2, so gradient = 8 ÷ 2 = 4. Getting 0.25 means run was put over rise. The vertical change goes on top."}
    ],
    "guided_steps": [
        sayonly("Rise over run. Rise is the change in y."),
        box("Rise: 12 − 4 = ", 8, "Subtract the y-values."),
        box("Run: 2 − 0 = ", 2, "Subtract the x-values."),
        box("8 ÷ 2 = ", 4, "How many 2s in 8?", say="Divide rise by run.", phase="substitute"),
        box("4 + 8 = ", 12, "4 + 8.", say="Check from (0, 4): two steps across at gradient 4 add 2 × 4 = 8.", done="That reaches y = 12 at x = 2, matching the point, so gradient 4 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "What is the gradient of the line \\(y = -3x + 7\\)?",
    "solutions": [-3],
    "calculator": False,
    "input_type": "single_value",
    "hint": "The gradient is the coefficient of x, and it keeps its minus sign.",
    "misconceptions": [
        {"check": "common", "expect": 3, "pattern": "sign_error",
         "message": "The gradient is the number in front of x, including its sign. Here m = −3. Dropping the minus gives 3, which is the wrong sign."}
    ],
    "guided_steps": [
        box("Constant on its own: ", 7, "The number with no x.", say="The equation is in \\(y = mx + c\\) form. The gradient is the number in front of x, and it keeps its sign. Read off the constant first."),
        box("Gradient m = ", -3, "Keep the minus in front of the 3.", say="Now the number multiplying x, including its minus sign."),
        box("−3 × 1 + 7 = ", 4, "−3 + 7.", say="Check the sign: a negative gradient slopes downhill. From x = 0 to x = 1, y should fall. At x = 0, \\(y = 7\\). At x = 1:", phase="substitute"),
        box("4 − 7 = ", -3, "4 take away 7.", say="So y went from 7 down to 4.", done="y fell by 3 for one step in x, confirming the gradient is −3.", phase="substitute")
    ]
})

bronze.append({
    "display": "For the line \\(y = x + 6\\), find \\(y\\) when \\(x = 0\\).",
    "solutions": [6],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Put x = 0 in: the x term becomes 0, leaving the constant 6.",
    "misconceptions": [
        {"check": "common", "expect": 1, "pattern": "confused_m_and_c",
         "message": "When x = 0, y = 0 + 6 = 6, which is the y-intercept. Answering 1 gives the gradient (the number in front of x) instead of the y-value."}
    ],
    "guided_steps": [
        box("1 × 0 = ", 0, "Anything times 0 is 0.", say="Substitute x = 0 into \\(y = x + 6\\). The number in front of x is 1, so the x part is 1 × 0. Work that out."),
        box("0 + 6 = ", 6, "Add 6 to your 0.", say="Now add the constant.", phase="substitute"),
        box("Value of y at x = 0: ", 6, "Only the 6 is left.", say="Check: when x = 0 the x term vanishes, leaving just the constant.", done="y = 6, which is the y-intercept, so that is right.", phase="substitute")
    ]
})

# ---------------- SILVER ----------------
silver = []

# S0: chart gradient (message rewrite per filed issue)
silver.append({
    "chart": chart_s0,
    "display": "The graph shows a straight line. What is the gradient of this line?",
    "solutions": [3],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Pick two points the line clearly passes through, then rise ÷ run.",
    "misconceptions": [
        {"check": "common", "expect": None, "pattern": "wrong_formula",
         "message": "It looks like rise and run may have been swapped, or the gradient confused with the y-intercept. Gradient = (change in y) ÷ (change in x). Pick two clear points, e.g. (0, 1) and (2, 7): (7 − 1) ÷ (2 − 0) = 6 ÷ 2 = 3."}
    ],
    "guided_steps": [
        box("Rise: 7 − 1 = ", 6, "The change in y between the two points.", say="Read two clear points off the line. It passes through (0, 1) and (2, 7). Find the rise between them."),
        box("Run: 2 − 0 = ", 2, "The change in x between the two points."),
        box("6 ÷ 2 = ", 3, "How many 2s in 6?", say="Gradient is rise over run.", phase="substitute"),
        box("6 ÷ 2 = ", 3, "Any two points on a straight line give the same gradient.", say="Check with another pair, (1, 4) and (3, 10): the rise is 10 − 4 = 6 over a run of 3 − 1 = 2.", done="Same gradient 3 from a different pair of points, so it is right.", phase="substitute")
    ]
})

# S1: chart y-intercept
silver.append({
    "chart": chart_s1,
    "display": "The graph shows a straight line. What is the y-intercept of this line?",
    "solutions": [-2],
    "calculator": False,
    "input_type": "single_value",
    "hint": "The y-intercept is the y-value where the line crosses the vertical axis (x = 0).",
    "misconceptions": [
        {"check": "common", "expect": 1, "pattern": "wrong_reading",
         "message": "The y-intercept is where the line crosses the y-axis (the vertical axis, x = 0). From the graph that is y = −2. Reading 1 is the x-intercept, where the line crosses the x-axis."}
    ],
    "guided_steps": [
        box("Rise: 2 − (−2) = ", 4, "2 + 2, minus a minus is plus.", say="The y-intercept is the y-value where the line crosses the vertical axis, at x = 0. Reading up from x = 0, the line is at y = −2. To be sure it is a straight line, find the gradient from two points, (0, −2) and (2, 2). Rise:"),
        box("Run: 2 − 0 = ", 2, "The change in x."),
        box("c = 2 − 4 = ", -2, "2 take away 4 goes below zero.", say="Gradient is 4 ÷ 2 = 2, so the line is \\(y = 2x + c\\). Put in the point (2, 2): the gradient part is 2 × 2 = 4, so 2 = 4 + c.", phase="substitute"),
        box("Read the graph at x = 0: y = ", -2, "The point on the line straight above x = 0.", say="So c = −2, which is exactly where the line meets the y-axis.", done="The graph and the algebra agree: the y-intercept is −2.", phase="substitute")
    ]
})

# S2: DEGENERATE FIX - remove equation from display
silver.append({
    "chart": chart_s2,
    "display": "The graph shows a straight line. What is the value of \\(y\\) when \\(x = 4\\)?",
    "solutions": [2],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Find x = 4 on the horizontal axis, go up to the line, then across to the y-axis.",
    "misconceptions": [
        {"check": "common", "expect": 4, "pattern": "wrong_reading",
         "message": "Find x = 4 on the horizontal axis, go straight up to the line, then across to the y-axis. The line is at y = 2 there. Reading y = 4 is the value at x = 2, not x = 4."}
    ],
    "guided_steps": [
        box("Rise: 0 − 6 = ", -6, "0 take away 6.", say="Reading a value off a straight line. Start on the horizontal axis at x = 4 and go up to the line. To be sure of the line, first read two clear points, (0, 6) and (6, 0). Find the rise."),
        box("Run: 6 − 0 = ", 6, "The change in x."),
        box("6 − 4 = ", 2, "Start at 6 and drop 4.", say="Gradient is −6 ÷ 6 = −1, so from (0, 6) the line drops 1 for each step across. After 4 steps it has dropped 4 × 1 = 4.", phase="substitute"),
        box("y when x = 4: ", 2, "Look up from x = 4 to the line.", say="So at x = 4 the line is at y = 2. Check by reading the point straight above x = 4 on the graph.", done="The graph shows y = 2 at x = 4, matching the working, so it is right.", phase="substitute")
    ]
})

silver.append({
    "display": "The line \\(y = \\frac{1}{2}x + 4\\) passes through the point \\((6, k)\\). Find \\(k\\).",
    "solutions": [7],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Work out half of 6 first, then add 4.",
    "misconceptions": [
        {"check": "common", "expect": 3, "pattern": "substitution_error",
         "message": "k = ½(6) + 4 = 3 + 4 = 7. Getting 3 means the + 4 was left out after halving."}
    ],
    "guided_steps": [
        box("½ × 6 = ", 3, "Half of 6.", say="Substitute x = 6 into \\(y = \\tfrac{1}{2}x + 4\\). Do the gradient part first: half of 6."),
        box("3 + 4 = ", 7, "Add 4 to your 3.", say="Now add the constant.", phase="substitute"),
        box("½ × 6 + 4 = ", 7, "3 + 4.", say="Check: k is the y-value at x = 6, so the point is (6, 7). Read the equation back, half of 6 is 3, plus 4.", done="That gives 7, so k = 7 is right.", phase="substitute")
    ]
})

# CHANGED S4 (dedupe 3 to 4): points (-1,3)&(2,15)
silver.append({
    "display": "Find the gradient of the line through \\((-1, 3)\\) and \\((2, 15)\\).",
    "solutions": [4],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Rise ÷ run; remember 2 − (−1) = 3.",
    "misconceptions": [
        {"check": "common", "expect": 12, "pattern": "sign_error",
         "message": "Rise = 15 − 3 = 12, run = 2 − (−1) = 3, so gradient = 12 ÷ 3 = 4. Getting 12 means the run was taken as 2 − 1 = 1, dropping the double negative."}
    ],
    "guided_steps": [
        sayonly("Rise over run. Rise is the change in y."),
        box("Rise: 15 − 3 = ", 12, "Subtract the y-values."),
        box("Run: 2 − (−1) = ", 3, "2 + 1, minus a minus is plus."),
        box("12 ÷ 3 = ", 4, "How many 3s in 12?", say="Divide rise by run.", phase="substitute"),
        box("3 + 12 = ", 15, "3 + 12.", say="Check from (−1, 3): a run of 3 across at gradient 4 adds 3 × 4 = 12.", done="That reaches y = 15 at x = 2, matching the point, so gradient 4 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "A line has gradient \\(-4\\) and passes through \\((1, 6)\\). What is the y-intercept?",
    "solutions": [10],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Put the point into \\(y = mx + c\\): 6 = −4(1) + c, then solve for c.",
    "misconceptions": [
        {"check": "common", "expect": 2, "pattern": "wrong_formula",
         "message": "Use y = mx + c: 6 = −4(1) + c, so c = 6 + 4 = 10. Getting 2 means 4 was subtracted instead of added when moving the −4 across."}
    ],
    "guided_steps": [
        box("−4 × 1 = ", -4, "−4 times 1.", say="Work backwards with \\(y = mx + c\\). The gradient is −4 and the point (1, 6) gives x and y. Work out the gradient part first: −4 × 1."),
        box("c = 6 + 4 = ", 10, "6 + 4, because moving −4 across makes it +4.", say="So \\(6 = −4 + c\\). Add 4 to both sides to free c.", phase="substitute"),
        box("−4 + 10 = ", 6, "−4 + 10.", say="Check: the line is \\(y = −4x + 10\\). Put x = 1 back in: −4 × 1 + 10.", done="That gives 6, matching the point (1, 6), so c = 10 is right.", phase="substitute")
    ]
})

# S6: multiple_choice (guided_steps omitted, allowed)
silver.append({
    "display": "Find the gradient of the line through \\((3, 5)\\) and \\((3, 11)\\).",
    "options": ["0", "6", "Undefined (vertical line)", "2"],
    "solutions": [2],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Both points have x = 3, so the run is 0: you cannot divide by zero.",
    "misconceptions": [
        {"check": "common", "expect": 1, "pattern": "vertical_line",
         "message": "The x-values are the same (both 3), so the line is vertical. Vertical lines have undefined gradient because the run is 0 and you cannot divide by zero. Choosing 6 uses the rise only."}
    ]
})

# ---------------- TIER GUIDES ----------------
tier_guides = {
    "bronze": {
        "title": "Bronze: reading a line's equation and simple gradients",
        "steps": [
            "In \\(y = mx + c\\), the number in front of \\(x\\) is the <strong>gradient</strong> \\(m\\) (the steepness) and the lone number is the <strong>y-intercept</strong> \\(c\\) (where the line meets the y-axis).",
            "To find a gradient from two points, use rise over run: \\(m = \\dfrac{\\text{change in }y}{\\text{change in }x}\\). Put the vertical change on top.",
            "To read a value, substitute the given \\(x\\) into the equation and work it out, multiplying before you add."
        ],
        "example": {
            "question": "A line has equation \\(y = 3x + 2\\). Write down its gradient, then find \\(y\\) when \\(x = 4\\).",
            "steps": [
                {"label": "Gradient", "content": "<p>The number in front of \\(x\\) is 3, so the gradient is 3.</p>"},
                {"label": "Substitute x = 4", "content": "<p>\\(y = 3(4) + 2 = 12 + 2 = 14\\)</p>"},
                {"label": "Check", "content": "<p>Gradient 3 means y rises 3 for each step in x. From \\(x = 0, y = 2\\), four steps add \\(4 \\times 3 = 12\\), giving \\(y = 14\\). ✔</p>"},
                {"label": "Answer", "content": "<p>Gradient = 3; when \\(x = 4\\), \\(y = 14\\).</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: reading graphs and working backwards",
        "steps": [
            "Read a straight-line graph by going from a value on one axis, across to the line, then to the other axis.",
            "The gradient can be a fraction or negative. Count the rise and run between two clear grid points, and remember down-sloping lines have a negative gradient.",
            "To work backwards, put what you know into \\(y = mx + c\\) and solve for the missing letter."
        ],
        "example": {
            "question": "A line has gradient \\(-2\\) and passes through \\((3, 1)\\). Find its y-intercept \\(c\\).",
            "steps": [
                {"label": "Use y = mx + c", "content": "<p>Substitute \\(m = -2\\), \\(x = 3\\), \\(y = 1\\): \\(1 = -2(3) + c\\).</p>"},
                {"label": "Solve for c", "content": "<p>\\(1 = -6 + c\\), so \\(c = 1 + 6 = 7\\).</p>"},
                {"label": "Check", "content": "<p>The line is \\(y = -2x + 7\\). At \\(x = 3\\): \\(y = -6 + 7 = 1\\). ✔ matches the point.</p>"},
                {"label": "Answer", "content": "<p>The y-intercept is \\(c = 7\\).</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: full equations and negative-number gradients",
        "steps": [
            "Find the gradient first: \\(m = \\dfrac{y_2 - y_1}{x_2 - x_1}\\). Subtracting a negative adds, so keep signs on a tight leash.",
            "Then find \\(c\\) by putting one point and your \\(m\\) into \\(y = mx + c\\).",
            "If an equation is not yet in \\(y = mx + c\\) form, rearrange it first, then read the gradient."
        ],
        "example": {
            "question": "Find the equation of the line through \\((-2, 1)\\) and \\((2, 9)\\) in the form \\(y = mx + c\\).",
            "steps": [
                {"label": "Gradient", "content": "<p>\\(m = \\dfrac{9 - 1}{2 - (-2)} = \\dfrac{8}{4} = 2\\)</p>"},
                {"label": "Find c", "content": "<p>Use \\((2, 9)\\): \\(9 = 2(2) + c\\), so \\(c = 9 - 4 = 5\\).</p>"},
                {"label": "Check", "content": "<p>\\(y = 2x + 5\\). At \\((-2, 1)\\): \\(2(-2) + 5 = -4 + 5 = 1\\). ✔</p>"},
                {"label": "Answer", "content": "<p>\\(y = 2x + 5\\).</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
    "opener": {
        "display": "A cyclist rides at a steady pace.<br>After 1 hour: 12 km.<br>After 2 hours: 24 km.<br>After 3 hours: 36 km.<br>No algebra needed, just look at the numbers.",
        "steps": [
            sayonly("Look at how far she travels in each single hour."),
            box("Each hour she rides ", 12, "She goes from 12 km to 24 km between hour 1 and hour 2.", post=" km"),
            sayonly("That steady 12 km every hour is the line's <strong>gradient</strong>: its steepness. On a distance-time graph the gradient is the speed."),
            box("So after 4 hours she has ridden ", 48, "Add one more 12 km to the 36 km at hour 3.", post=" km"),
            sayonly("You just read a value off a straight line using its steady rate. Algebra writes this as \\(y = mx + c\\). Here the gradient \\(m\\) is 12 and the start \\(c\\) is 0, so \\(y = 12x\\). The gradient is the number in front of \\(x\\), and reading a graph means finding y for a given x.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "Find the gradient of the line through \\((1, 2)\\) and \\((4, 11)\\).",
            "steps": [
                sayonly("Gradient means how far the line climbs for each step across. Work out the <strong>rise</strong> (change in y) first."),
                box("Rise: 11 − 2 = ", 9, "Subtract the two y-values."),
                box("Run: 4 − 1 = ", 3, "Subtract the two x-values."),
                box("9 ÷ 3 = ", 3, "How many 3s in 9?", say="Gradient is rise divided by run.", done="That is the gradient. Rise over run, every time."),
                box("2 + 9 = ", 11, "2 + 9.", say="Check by stepping along the line. From (1, 2), three steps of gradient 3 add 3 × 3 = 9, giving y = 2 + 9.", done="That matches the point (4, 11), so the gradient 3 is right.")
            ]
        },
        "silver": {
            "display": "A line has gradient \\(\\frac{1}{2}\\) and passes through \\((4, 5)\\). Find its y-intercept, then find \\(y\\) when \\(x = 10\\).",
            "steps": [
                box("½ × 4 = ", 2, "Half of 4.", say="Working backwards: put what you know into \\(y = mx + c\\). Here \\(m = \\tfrac{1}{2}\\), and the point \\((4, 5)\\) gives x and y. First work out the gradient part."),
                box("c = 5 − 2 = ", 3, "Take 2 from both sides.", say="So \\(5 = 2 + c\\).", done="The y-intercept is 3. That is working backwards."),
                box("½ × 10 = ", 5, "Half of 10.", say="The line is \\(y = \\tfrac{1}{2}x + 3\\). Now read forward to \\(x = 10\\). First the gradient part:"),
                box("5 + 3 = ", 8, "Add the y-intercept 3.", say="Then add the intercept.", done="So at x = 10, y = 8. Forwards and backwards use the same equation."),
                box("½ × 4 + 3 = ", 5, "2 + 3.", say="Check with the original point.", done="That gives 5, matching (4, 5), so c = 3 is right.")
            ]
        },
        "gold": {
            "display": "Find the equation of the line through \\((-2, 7)\\) and \\((2, -1)\\), giving your answer as \\(y = mx + c\\). Then state the gradient.",
            "steps": [
                box("Rise: −1 − 7 = ", -8, "−1 take away 7.", say="Find the gradient first. Rise is the change in y from the first point to the second."),
                box("Run: 2 − (−2) = ", 4, "2 + 2, because minus a minus is plus.", say="Run is the change in x. Watch the double negative: subtracting −2 adds 2."),
                box("−8 ÷ 4 = ", -2, "−8 shared into 4.", say="Gradient is rise over run.", done="Gradient −2. The line slopes downhill."),
                box("c = −1 + 4 = ", 3, "−1 add 4.", say="Now find c. Put the gradient and the point (2, −1) into \\(y = mx + c\\). The gradient part is −2 × 2 = −4, so −1 = −4 + c.", done="So the equation is y = −2x + 3."),
                box("−2 × (−2) + 3 = ", 7, "Minus times minus is plus: 4, then + 3.", say="Check the other point (−2, 7):", done="4 + 3 = 7, matching (−2, 7), so y = −2x + 3 is right.")
            ]
        }
    }
}

# ---------------- PRESERVE worked_examples but strip em dashes (style rule) ----------------
worked_examples = json.loads(json.dumps(live["worked_examples"]))
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
        if "content" in st and "—" in st["content"]:
            st["content"] = st["content"].replace(" — ", ", ").replace("—", "-")

# ---------------- ASSEMBLE ----------------
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": {
        "bronze_description": "Read the gradient and y-intercept from y = mx + c, substitute a value, or find a gradient from two whole-number points.",
        "silver_description": "Read gradients and values from a drawn graph, handle fractions and negatives, and work backwards to find c or a missing coordinate.",
        "gold_description": "Find a full equation from two points, cope with negative-number gradients, back-solve for m, and rearrange an equation into y = mx + c first.",
        "bronze": bronze,
        "silver": silver,
        "gold": gold
    },
    "tier_guides": tier_guides,
    "guided": guided,
    "related_videos": live["related_videos"],
    "worked_examples": worked_examples
}

json.dump(out, io.open('lesson_graphs-L01.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print("written lesson_graphs-L01.json")
