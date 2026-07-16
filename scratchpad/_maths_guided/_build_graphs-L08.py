# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_graphs-L08.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text): return {"say": text}

def mis(pattern, expect, message):
    return {"pattern": pattern, "check": "common", "expect": expect, "message": message}

pd = {}

# ---- method_card (slim) ----
pd["method_card"] = {
    "title": "How to Estimate Gradients and Areas from Curves",
    "steps": [
        "Gradient at a point: draw the tangent, pick two points on it, and work out change in y ÷ change in x.",
        "Area under a curve: split it into equal strips of width h and use the trapezium rule.",
        "Trapezium rule: Area ≈ (h/2)[first + last + 2 × (all the middle values)].",
        "Interpret in context: the gradient is a rate (e.g. speed), the area is a total (e.g. distance).",
    ],
    "content": "<p>Two estimates come from curves: the <strong>gradient at a point</strong> and the <strong>area underneath</strong>.</p><p><strong>Gradient:</strong> draw a <strong>tangent</strong> that just touches the curve, pick two points far apart on it, and work out \\(\\frac{\\Delta y}{\\Delta x}\\). A tangent, not a chord, gives the instantaneous rate.</p><p><strong>Area:</strong> use the <strong>trapezium rule</strong> \\(\\frac{h}{2}[y_0 + y_n + 2(y_1 + \\cdots + y_{n-1})]\\). End values count once, middle values twice.</p><p><strong>Context:</strong> on a speed-time graph the gradient is acceleration and the area is distance.</p>",
    "example": "<p><strong>Speed-time graph:</strong> \\(v = 0, 6, 10, 12\\) at \\(t = 0, 2, 4, 6\\) (\\(h = 2\\)).</p><p>Area \\(\\approx \\frac{2}{2}[0 + 12 + 2(6 + 10)] = 1 \\times 44 = 44\\) m.</p>",
}

# ---- preserved byte-for-byte ----
pd["topic_links"] = live["topic_links"]
pd["related_videos"] = live["related_videos"]
# worked_examples preserved, except em dashes must be removed (hard style rule,
# validator-enforced). Minimal edit: colon in step labels, comma in prose.
we = json.loads(json.dumps(live["worked_examples"]))
for ex in we:
    for st in ex.get("steps", []):
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
        if "content" in st:
            st["content"] = st["content"].replace(" — ", ", ").replace("—", ",")
pd["worked_examples"] = we

# ================= PROBLEM BANK =================
pb = {}

# ---------- BRONZE ----------
bronze = []

# B0 gradient (2,4)->(6,12) = 2  [completion problem]
bronze.append({
    "display": "A tangent line passes through \\((2, 4)\\) and \\((6, 12)\\). What is the gradient?",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Divide the change in y by the change in x.",
    "misconceptions": [mis("inverted_fraction", 0.5,
        "A common mistake is to invert the fraction: Δx ÷ Δy = (6 − 2) ÷ (12 − 4) = 4/8 = 0.5. Always put the change in y on top: gradient = Δy ÷ Δx = 8/4 = 2.")],
    "guided_steps": [
        say("A tangent is a straight line, so its gradient is the change in y divided by the change in x. Work out each change first, keeping both subtractions in the same order."),
        box("change in y: 12 − 4 = ", 8, "Subtract the y-values, second point first."),
        box("change in x: 6 − 2 = ", 4, "Subtract the x-values in the same order."),
        box("gradient = 8 ÷ 4 = ", 2, "Divide the change in y by the change in x.", phase="substitute",
            say="Now divide to get the gradient:"),
        box("1 check: 4 + 2 × 4 = ".replace("1 check: ", ""), 12, "Add the rise to the starting y.",
            say="Check: from x = 2 to x = 6 is a run of 4, so at gradient 2 the y-value should climb 2 × 4 = 8, from 4 up to 12.",
            done="Lands on 12, the second point, so gradient = 2 is right."),
    ],
})

# B1 gradient (0,5)->(4,1) = -1
bronze.append({
    "display": "A tangent line passes through \\((0, 5)\\) and \\((4, 1)\\). What is the gradient?",
    "solutions": [-1], "calculator": False, "input_type": "single_value",
    "hint": "Divide the change in y by the change in x, and keep the minus sign.",
    "misconceptions": [mis("sign_error", 1,
        "Careful with the sign: (1 − 5) gives −4, not +4. Dividing gives −4/4 = −1. Dropping the negative is a common slip; the line slopes downward, so the gradient must be negative.")],
    "guided_steps": [
        say("Gradient is the change in y over the change in x. Take both points in the same order and keep track of the minus sign."),
        box("change in y: 1 − 5 = ", -4, "1 take away 5 goes below zero."),
        box("change in x: 4 − 0 = ", 4, "Subtract the x-values in the same order."),
        box("gradient = −4 ÷ 4 = ", -1, "A negative divided by a positive is negative.", phase="substitute",
            say="Now divide, keeping the minus:"),
        box("5 + (−1) × 4 = ", 1, "Add the rise (here negative) to the start y.",
            say="Check: starting at y = 5, a gradient of −1 over a run of 4 drops the value by 4.",
            done="Starts at 5, drops by 4, lands on 1. Gradient = −1 is right."),
    ],
})

# B2 MC tangent
bronze.append({
    "display": "To estimate the gradient of a curve at a point, which should you draw?",
    "options": ["A chord", "A tangent", "A normal", "A secant"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "You need the line that just touches the curve at one point.",
    "misconceptions": [mis("confusion", 0,
        "A tangent just touches the curve at one point and gives the gradient there. A chord joins two points on the curve and gives the average gradient, not the instantaneous one.")],
})

# B3 single trapezium 3,7 h=2 = 10
bronze.append({
    "display": "Estimate the area of one trapezium with parallel sides \\(y = 3\\) and \\(y = 7\\), width \\(h = 2\\).",
    "solutions": [10], "calculator": False, "input_type": "single_value",
    "hint": "A trapezium is half the sum of the parallel sides, times the width.",
    "misconceptions": [mis("forgot_half", 20,
        "It looks like the ½ was left out: (3 + 7) × 2 = 20 is double the real area. A trapezium is ½(a + b) × h = ½(3 + 7) × 2 = 10.")],
    "guided_steps": [
        say("A trapezium strip is half of (side + side) times the width. Build it one step at a time. First add the two parallel sides:"),
        box("3 + 7 = ", 10, "Add the two y-values."),
        box("multiply by the width h = 2: 10 × 2 = ", 20, "Multiply the sum by 2."),
        box("now halve it: 20 ÷ 2 = ", 10, "A trapezium is half of base-sum times width.", phase="substitute",
            say="Halve it for the trapezium:"),
        box("5 × 2 = ", 10, "Average height times width.",
            say="Check another way: the average of the two sides is (3 + 7) ÷ 2 = 5, and area = average height × width.",
            done="Same area, 10 square units."),
    ],
})

# B4 single trapezium 5,5 h=4 = 20
bronze.append({
    "display": "Estimate the area of one trapezium with parallel sides \\(y = 5\\) and \\(y = 5\\), width \\(h = 4\\).",
    "solutions": [20], "calculator": False, "input_type": "single_value",
    "hint": "Half the sum of the two sides, times the width.",
    "misconceptions": [mis("forgot_half", 40,
        "Leaving out the ½ gives (5 + 5) × 4 = 40. A trapezium is always ½(a + b) × h, so the area is ½ × 10 × 4 = 20. Here both sides are equal, so it is really a 5 by 4 rectangle.")],
    "guided_steps": [
        say("Same trapezium rule: half of (side + side) times the width. Add the sides first:"),
        box("5 + 5 = ", 10, "Add the two y-values."),
        box("multiply by the width h = 4: 10 × 4 = ", 40, "Multiply the sum by 4."),
        box("now halve it: 40 ÷ 2 = ", 20, "Halve it for the trapezium.", phase="substitute",
            say="Halve it:"),
        box("5 × 4 = ", 20, "Both sides equal, so it is really a rectangle.",
            say="Check: both sides are 5, so the strip is a 5 by 4 rectangle, area = 5 × 4.",
            done="A 5 by 4 rectangle is also 20, so it checks."),
    ],
})

# B5 (REPLACED) gradient (-2,1)->(2,13) = 3  -- de-duplicates B0, raises demand with a negative coordinate
bronze.append({
    "display": "A tangent passes through \\((-2, 1)\\) and \\((2, 13)\\). What is the gradient?",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Divide the change in y by the change in x; subtracting a negative x adds.",
    "misconceptions": [mis("order_mixed", -3,
        "Keep both subtractions in the same order. Doing the y as (13 − 1) = 12 but the x as (−2 − 2) = −4 flips the sign and gives −3. Take both from the same point: change in x = 2 − (−2) = 4, so gradient = 12/4 = 3.")],
    "guided_steps": [
        say("The tangent is a straight line. Its gradient is the change in y over the change in x. Take both points in the same order, and watch the negative coordinate."),
        box("change in y: 13 − 1 = ", 12, "Subtract the y-values."),
        box("change in x: 2 − (−2) = ", 4, "Subtracting a negative adds: 2 + 2."),
        box("gradient = 12 ÷ 4 = ", 3, "Divide the change in y by the change in x.", phase="substitute",
            say="Now divide:"),
        box("1 + 3 × 4 = ", 13, "Add the rise to the start y.",
            say="Check: from (−2, 1), a run of 4 at gradient 3 climbs 3 × 4 = 12.",
            done="Climbs from 1 to 13, the second point. Gradient = 3 is right."),
    ],
})

# B6 MC area under speed-time = distance
bronze.append({
    "display": "On a speed-time graph, what does the area under the curve represent?",
    "options": ["Speed", "Acceleration", "Distance", "Time"],
    "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "hint": "Area under a speed-time graph builds up distance.",
    "misconceptions": [mis("confusion", 1,
        "The area under a speed-time graph is the distance travelled. It is the gradient of a speed-time graph that gives acceleration.")],
})

# B7 MC gradient of distance-time = speed
bronze.append({
    "display": "On a distance-time graph, what does the gradient represent?",
    "options": ["Distance", "Time", "Speed", "Acceleration"],
    "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "hint": "Steepness of a distance-time line tells you how fast.",
    "misconceptions": [mis("confusion", 3,
        "The gradient of a distance-time graph is speed. Acceleration is the gradient of a speed-time graph, which is a different graph.")],
})

pb["bronze"] = bronze
pb["bronze_description"] = "Find a gradient from two points on a tangent, work out one trapezium strip, and read what gradient and area mean on a graph."

# ---------- SILVER ----------
silver = []

# S0 give h = 3  [completion problem]
silver.append({
    "display": "Use the trapezium rule with 2 strips to estimate the area under a curve: \\(y_0 = 2, y_1 = 6, y_2 = 8\\) at \\(x = 0, 3, 6\\). Give the strip width \\(h\\).",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Strip width is the total x-range divided by the number of strips.",
    "misconceptions": [mis("range_not_divided", 6,
        "That is the total x-range, not the strip width. Divide it by the number of strips: h = (6 − 0) ÷ 2 = 3.")],
    "guided_steps": [
        say("The strip width h is the total x-range shared equally between the strips. Find the range first."),
        box("total x-range: 6 − 0 = ", 6, "Subtract the first x from the last x."),
        box("number of strips: ", 2, "The question says 2 strips (the gaps 0 to 3 and 3 to 6)."),
        box("strip width h = 6 ÷ 2 = ", 3, "Divide the range by the number of strips.", phase="substitute",
            say="Divide the range by the number of strips:"),
        box("3 − 0 = ", 3, "Check one gap, from x = 0 to x = 3.",
            say="Check: each gap should equal h. The first gap is from x = 0 to x = 3.",
            done="Each step (0 to 3, 3 to 6) is 3, so h = 3 is right."),
    ],
})

# S1 (REWRITTEN self-contained) trapezium rule = 33
silver.append({
    "display": "Use the trapezium rule with \\(h = 3\\) and \\(y_0 = 2, y_1 = 6, y_2 = 8\\) to estimate the area under the curve.",
    "solutions": [33], "calculator": False, "input_type": "single_value",
    "hint": "Use h/2 times [first + last + 2 × the middle value].",
    "misconceptions": [mis("forgot_double", 24,
        "The middle value must be doubled. Forgetting it gives (3/2)[2 + 8 + 6] = (3/2)(16) = 24. With the doubling: (3/2)[2 + 8 + 2(6)] = 1.5 × 22 = 33.")],
    "guided_steps": [
        say("The trapezium rule is (h/2) × [first + last + 2 × (middle values)]. Start with the two ends."),
        box("first + last: 2 + 8 = ", 10, "Add y0 and y2."),
        box("the middle value counts twice: 2 × 6 = ", 12, "Double the interior value y1."),
        box("bracket total: 10 + 12 = ", 22, "Add the ends to the doubled middle."),
        box("1.5 × 22 = ", 33, "Multiply the bracket by h/2.", phase="substitute",
            say="Now scale by h/2. Here h/2 = 3 ÷ 2 = 1.5:"),
        box("12 + 21 = ", 33, "Add the two strip areas.",
            say="Check by strips: strip one is ½(2 + 6) × 3 = 12, strip two is ½(6 + 8) × 3 = 21.",
            done="Both routes give 33 square units."),
    ],
})

# S2 tangent gradient (1,-3)->(5,21) = 6
silver.append({
    "display": "A tangent to the curve \\(y = x^2\\) at \\(x = 3\\) passes through \\((1, -3)\\) and \\((5, 21)\\). Estimate the gradient at \\(x = 3\\).",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Divide the change in y by the change in x; watch the double negative.",
    "misconceptions": [mis("double_negative", 4.5,
        "Treating the −3 as +3 gives (21 − 3)/(5 − 1) = 18/4 = 4.5. Subtracting a negative adds: (21 − (−3))/(5 − 1) = 24/4 = 6.")],
    "guided_steps": [
        say("Gradient of the tangent is the change in y over the change in x. The lower point has a negative y, so take care with the subtraction."),
        box("change in y: 21 − (−3) = ", 24, "Subtracting a negative adds: 21 + 3."),
        box("change in x: 5 − 1 = ", 4, "Subtract the x-values."),
        box("gradient = 24 ÷ 4 = ", 6, "Divide the change in y by the change in x.", phase="substitute",
            say="Now divide:"),
        box("−3 + 6 × 4 = ", 21, "Add the rise to the start y.",
            say="Check: from (1, −3), a run of 4 at gradient 6 climbs 6 × 4 = 24.",
            done="Reaches 21, the second point. Gradient = 6 is right."),
    ],
})

# S3 speed-time trapezium = 75
silver.append({
    "display": "A speed-time graph has values: \\(t = 0, v = 0\\); \\(t = 5, v = 10\\); \\(t = 10, v = 10\\). Use the trapezium rule to estimate the distance. Use 2 strips.",
    "solutions": [75], "calculator": False, "input_type": "single_value",
    "hint": "Find h first, then use h/2 times [ends + 2 × middle].",
    "misconceptions": [mis("used_h_not_half", 150,
        "Multiply by h/2, not h. Using h = 5 gives 5 × [0 + 10 + 2(10)] = 5 × 30 = 150, which is double the real distance. With h/2 = 2.5: 2.5 × 30 = 75 metres.")],
    "guided_steps": [
        say("Distance is the area under the graph. Use the trapezium rule. First find the strip width h."),
        box("strip width h = (10 − 0) ÷ 2 = ", 5, "Total time divided by the number of strips."),
        box("first + last speed: 0 + 10 = ", 10, "Add the two end speeds."),
        box("double the middle: 2 × 10 = ", 20, "The middle speed counts twice."),
        box("bracket total: 10 + 20 = ", 30, "Add the ends to the doubled middle."),
        box("2.5 × 30 = ", 75, "Multiply the bracket by h/2.", phase="substitute",
            say="Now scale by h/2. Here h/2 = 5 ÷ 2 = 2.5:"),
        box("25 + 50 = ", 75, "Add the two strip distances.",
            say="Check by strips: ½(0 + 10) × 5 = 25 and ½(10 + 10) × 5 = 50.",
            done="Both give 75 metres."),
    ],
})

# S4 MC gradient of distance-time = speed
silver.append({
    "display": "The gradient of a distance-time graph at \\(t = 4\\) is estimated as 12. What does this tell you?",
    "options": ["The object has travelled 12 metres", "The object is 12 metres from the start",
                "The speed at t = 4 is 12 m/s", "The acceleration is 12 m/s²"],
    "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "hint": "Gradient of a distance-time graph is speed.",
    "misconceptions": [mis("confusion", 3,
        "The gradient of a distance-time graph gives the speed at that instant, so the speed at t = 4 is 12 m/s. Acceleration is the gradient of a speed-time graph.")],
})

# S5 trapezium 5 values = 18
silver.append({
    "display": "Use the trapezium rule: \\(y_0 = 0, y_1 = 4, y_2 = 6, y_3 = 6, y_4 = 4\\). Strip width \\(h = 1\\). Estimate the area.",
    "solutions": [18], "calculator": False, "input_type": "single_value",
    "hint": "Use h/2 times [first + last + 2 × (all the middle values)].",
    "misconceptions": [mis("forgot_double", 10,
        "The interior values must be doubled. Forgetting it gives (1/2)[0 + 4 + (4 + 6 + 6)] = (1/2)(20) = 10. Doubling: (1/2)[0 + 4 + 2(4 + 6 + 6)] = 0.5 × 36 = 18.")],
    "guided_steps": [
        say("Trapezium rule again: (h/2) × [first + last + 2 × (middle values)]. Start with the ends."),
        box("first + last: 0 + 4 = ", 4, "Add y0 and y4."),
        box("add the middle values: 4 + 6 + 6 = ", 16, "Add y1, y2 and y3."),
        box("double them: 2 × 16 = ", 32, "Interior values count twice."),
        box("bracket total: 4 + 32 = ", 36, "Ends plus the doubled middle."),
        box("0.5 × 36 = ", 18, "Multiply the bracket by h/2.", phase="substitute",
            say="Now scale by h/2. Here h/2 = 1 ÷ 2 = 0.5:"),
        box("2 + 5 + 6 + 5 = ", 18, "Add the four strip areas.",
            say="Check by strips: ½(0+4), ½(4+6), ½(6+6), ½(6+4), each × 1, give 2, 5, 6, 5.",
            done="Four strips also total 18 square units."),
    ],
})

# S6 MC negative gradient = decreasing
silver.append({
    "display": "A curve has a negative gradient at \\(x = 2\\). Is the curve increasing or decreasing at this point?",
    "options": ["Increasing", "Decreasing", "Stationary", "Cannot tell"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "A downhill slope means the value is falling.",
    "misconceptions": [mis("confusion", 0,
        "A negative gradient means the curve is going downhill, so it is decreasing at that point. A positive gradient would mean increasing.")],
})

pb["silver"] = silver
pb["silver_description"] = "Apply the full trapezium rule across several strips and estimate a gradient where negative values appear."

# ---------- GOLD ----------
gold = []

# G0 trapezium 4 strips = 49  [completion problem]
gold.append({
    "display": "Use the trapezium rule with 4 strips: \\(y_0 = 1, y_1 = 3, y_2 = 7, y_3 = 9, y_4 = 10\\) at \\(x = 0, 2, 4, 6, 8\\). Estimate the area.",
    "solutions": [49], "calculator": False, "input_type": "single_value",
    "hint": "h/2 times [first + last + 2 × (interior values)].",
    "misconceptions": [mis("forgot_double", 30,
        "The interior values must be doubled. Forgetting it gives 1 × [1 + 10 + (3 + 7 + 9)] = 30. With the doubling: (2/2)[1 + 10 + 2(3 + 7 + 9)] = 1 × 49 = 49.")],
    "guided_steps": [
        say("Here h = 2. Trapezium rule: (h/2) × [first + last + 2 × (interior values)]. Build it up."),
        box("first + last: 1 + 10 = ", 11, "Add y0 and y4."),
        box("add the interior values: 3 + 7 + 9 = ", 19, "Add y1, y2 and y3."),
        box("double them: 2 × 19 = ", 38, "Interior values count twice."),
        box("bracket total: 11 + 38 = ", 49, "Ends plus the doubled middle.", phase="substitute",
            say="Now assemble the bracket, then scale by h/2 (here h/2 = 2 ÷ 2 = 1)."),
        box("1 × 49 = ", 49, "h/2 = 1, so the area equals the bracket."),
        box("4 + 10 + 16 + 19 = ", 49, "Add the four strip areas.",
            say="Check by strips: ½(1+3)×2, ½(3+7)×2, ½(7+9)×2, ½(9+10)×2 give 4, 10, 16, 19.",
            done="Strip-by-strip also gives 49 square units."),
    ],
})

# G1 velocity-time 4 strips = 72
gold.append({
    "display": "A velocity-time graph shows: \\(t = 0, v = 0\\); \\(t = 2, v = 8\\); \\(t = 4, v = 12\\); \\(t = 6, v = 12\\); \\(t = 8, v = 8\\). Use 4 strips to estimate the total distance in metres.",
    "solutions": [72], "calculator": False, "input_type": "single_value",
    "hint": "Distance is the area: h/2 times [ends + 2 × middle speeds].",
    "misconceptions": [mis("forgot_double", 40,
        "The middle speeds must be doubled. Forgetting it gives 1 × [0 + 8 + (8 + 12 + 12)] = 40. With the doubling: (2/2)[0 + 8 + 2(8 + 12 + 12)] = 1 × 72 = 72 metres.")],
    "guided_steps": [
        say("Distance is the area under the velocity-time graph. Here h = 2. Use (h/2) × [first + last + 2 × (middle speeds)]."),
        box("first + last: 0 + 8 = ", 8, "Add the two end speeds."),
        box("add the middle speeds: 8 + 12 + 12 = ", 32, "Add the three interior speeds."),
        box("double them: 2 × 32 = ", 64, "Interior speeds count twice."),
        box("bracket total: 8 + 64 = ", 72, "Ends plus the doubled middle.", phase="substitute",
            say="Now assemble the bracket, then scale by h/2 (here h/2 = 2 ÷ 2 = 1)."),
        box("1 × 72 = ", 72, "h/2 = 1, so the distance equals the bracket."),
        box("8 + 20 + 24 + 20 = ", 72, "Add the four strip distances.",
            say="Check by strips: ½(0+8)×2, ½(8+12)×2, ½(12+12)×2, ½(12+8)×2 give 8, 20, 24, 20.",
            done="72 metres either way."),
    ],
})

# G2 MC interpret gradient (falling)
gold.append({
    "display": "The tangent to a curve at \\(x = 4\\) passes through \\((2, 18)\\) and \\((6, 2)\\). The curve represents the height (m) of a ball after \\(x\\) seconds. Interpret the gradient.",
    "options": ["The ball is 4 m high", "The ball is falling at 4 m/s",
                "The ball is rising at 4 m/s", "The ball has travelled 4 m"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "A negative gradient of height means the ball is coming down.",
    "misconceptions": [mis("dropped_sign", 2,
        "Gradient = (2 − 18)/(6 − 2) = −16/4 = −4. The negative sign means the height is decreasing, so the ball is falling at 4 m/s, not rising.")],
})

# G3 MC over/under estimate  [display + message fixed]
gold.append({
    "display": "The trapezium rule with 5 strips gives an area of 42. The actual area is 40. Is the trapezium rule estimate an overestimate or underestimate? (Assume the curve is concave upward, shaped like a U or bowl.)",
    "options": ["Overestimate", "Underestimate", "Exact", "Cannot tell"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "For a bowl-shaped (concave-up) curve the straight tops sit above the curve.",
    "misconceptions": [mis("wrong_direction", 1,
        "For a concave-up curve (shaped like a bowl), the straight top of each trapezium lies above the curve, so the rule overestimates. For a concave-down curve (arch shape) the straight top lies below the curve, giving an underestimate.")],
})

# G4 average speed = 7
gold.append({
    "display": "A speed-time graph is estimated using 3 trapeziums: area₁ = 10, area₂ = 18, area₃ = 14. The time interval is 0 to 6 seconds. What is the estimated total distance and the estimated average speed?  Give the average speed in m/s.",
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "Add the strip areas for distance, then divide by total time for average speed.",
    "misconceptions": [mis("stopped_at_distance", 42,
        "That is the total distance, not the average speed. Divide by the total time: average speed = 42 ÷ 6 = 7 m/s.")],
    "guided_steps": [
        say("The three trapezium areas add up to the total distance (the whole area under the graph)."),
        box("total distance = 10 + 18 + 14 = ", 42, "Add the three strip areas."),
        box("total time = 6 − 0 = ", 6, "From 0 to 6 seconds."),
        box("average speed = 42 ÷ 6 = ", 7, "Average speed = total distance ÷ total time.", phase="substitute",
            say="Average speed is total distance divided by total time:"),
        box("7 × 6 = ", 42, "Multiply average speed by time.",
            say="Check: at 7 m/s for 6 s the distance would be:",
            done="That matches the total area of 42 m, so 7 m/s is right."),
    ],
})

pb["gold"] = gold
pb["gold_description"] = "Use four strips on a velocity-time graph, interpret the result, and judge whether the estimate is too big or too small."

pd["problem_bank"] = pb

# ================= TIER GUIDES =================
def exstep(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans:
        d["isAnswer"] = True; d["is_answer"] = True
    return d

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: gradient from two points and one trapezium strip",
        "steps": [
            "Gradient of a straight tangent is the change in y divided by the change in x. Subtract the two y-values, subtract the two x-values in the same order, then divide. A downward slope gives a negative gradient.",
            "One trapezium strip has area <strong>half of (a + b) times h</strong>, where a and b are the parallel sides and h is the width.",
            "On a graph, a gradient is a rate (like speed) and the area underneath is a total built up (like distance).",
        ],
        "example": {
            "question": "A tangent passes through (2, 1) and (6, 9). Find the gradient.",
            "steps": [
                exstep("Change in y", "<p>\\(9 - 1 = 8\\)</p>"),
                exstep("Change in x", "<p>\\(6 - 2 = 4\\)</p>"),
                exstep("Check", "<p>From \\(x = 2\\) to \\(x = 6\\), a gradient of 2 climbs \\(2 \\times 4 = 8\\), from 1 up to 9. ✓</p>"),
                exstep("Answer", "<p>Gradient \\(= 8 \\div 4 = 2\\)</p>", ans=True),
            ],
        },
    },
    "silver": {
        "title": "Silver: the full trapezium rule and gradients with negatives",
        "steps": [
            "The trapezium rule adds several strips at once: area is <strong>(h/2) × [first + last + 2 × (all the middle values)]</strong>. End values count once, middle values twice.",
            "Work out the strip width first: h is the total x-range divided by the number of strips.",
            "For a gradient, subtracting a negative coordinate adds, so \\(21 - (-3) = 24\\). Keep the signs tidy.",
        ],
        "example": {
            "question": "Trapezium rule, 2 strips: y₀ = 1, y₁ = 4, y₂ = 5, h = 2.",
            "steps": [
                exstep("Ends", "<p>\\(1 + 5 = 6\\)</p>"),
                exstep("Double the middle", "<p>\\(2 \\times 4 = 8\\)</p>"),
                exstep("Check by strips", "<p>\\(\\tfrac{1}{2}(1+4)\\times 2 + \\tfrac{1}{2}(4+5)\\times 2 = 5 + 9 = 14\\) ✓</p>"),
                exstep("Answer", "<p>\\(\\tfrac{2}{2}[6 + 8] = 14\\)</p>", ans=True),
            ],
        },
    },
    "gold": {
        "title": "Gold: velocity-time graphs and judging the estimate",
        "steps": [
            "On a velocity-time graph, the area under the curve is the distance travelled. Estimate it with the trapezium rule across every strip.",
            "Average speed is the total distance divided by the total time.",
            "A bowl-shaped (concave-up) curve makes the straight trapezium tops sit above the curve, so the rule overestimates. An arch-shaped curve underestimates.",
        ],
        "example": {
            "question": "Velocity-time: v = 0, 6, 10, 12 at t = 0, 2, 4, 6, h = 2. Estimate the distance.",
            "steps": [
                exstep("Ends", "<p>\\(0 + 12 = 12\\)</p>"),
                exstep("Double the middle", "<p>\\(2 \\times (6 + 10) = 32\\)</p>"),
                exstep("Check by strips", "<p>\\(6 + 16 + 22 = 44\\) m ✓</p>"),
                exstep("Answer", "<p>\\(\\tfrac{2}{2}[12 + 32] = 44\\) m</p>", ans=True),
            ],
        },
    },
}

# ================= GUIDED =================
pd["guided"] = {
    "opener": {
        "label": "Before any graphs",
        "display": "A car drives at a steady <strong>20 metres every second</strong>.<br>It keeps this up for <strong>3 seconds</strong>.",
        "steps": [
            box("How far does it travel in total? ", 60, "20 metres each second, for 3 seconds: 20 × 3.", post=" m",
                say="Forget graphs for a second, this is just common sense."),
            box("On a distance-time graph the line climbs from 0 m to 60 m over those 3 seconds. How many metres does it climb each second? ", 20,
                "Share the 60 m climb over 3 seconds: 60 ÷ 3.", post=" m",
                say="You just did speed × time. Drawn on a <strong>speed-time graph</strong>, a steady 20 m/s is a flat line, and 20 × 3 is exactly the <strong>area</strong> of the rectangle underneath it. When the speed keeps changing that area turns into an awkward shape, so we slice it into strips and add them up. That is the <strong>trapezium rule</strong>."),
            say("That climb per second, the rise divided by the run, is the <strong>gradient</strong>, and here it equals the speed, 20 m/s. Two ideas, one lesson: the <strong>gradient</strong> of a graph is how fast it is changing, and the <strong>area</strong> underneath is the total built up. On curves we estimate both."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Estimate the area of one trapezium strip with parallel sides \\(y = 4\\) and \\(y = 8\\), width \\(h = 3\\).",
            "label": "Together: your first one",
            "steps": [
                box("4 + 8 = ", 12, "Add the two y-values.",
                    say="A trapezium strip is <strong>half of (side + side) times the width</strong>. Build it up one step at a time. First add the two parallel sides:"),
                box("multiply by the width h = 3: 12 × 3 = ", 36, "Multiply the sum by 3."),
                box("now halve it: 36 ÷ 2 = ", 18, "A trapezium is half of base-sum times width.",
                    done="That is the strip's area, 18 square units."),
                box("(4 + 8) ÷ 2 = ", 6, "Add the sides and halve.",
                    say="Check it a second way. The average of the two sides is the height of an equal rectangle:"),
                box("6 × 3 = ", 18, "Average height times width.",
                    done="Same answer, 18. The strip is right."),
            ],
        },
        "silver": {
            "display": "Use the trapezium rule with 3 strips: \\(y_0 = 1, y_1 = 5, y_2 = 6, y_3 = 2\\), width \\(h = 2\\). Estimate the area.",
            "label": "Together: the silver move",
            "steps": [
                box("first + last: 1 + 2 = ", 3, "Add y0 and y3.",
                    say="The rule adds every strip in one go: <strong>(h/2) × [first + last + 2 × (middle values)]</strong>. Start with the two ends:"),
                box("add the middle values: 5 + 6 = ", 11, "Add y1 and y2."),
                box("the middle counts twice, so double it: 2 × 11 = ", 22, "Interior values count twice.",
                    done="That doubling is the whole trick of the rule."),
                box("bracket total: 3 + 22 = ", 25, "Ends plus the doubled middle."),
                box("1 × 25 = ", 25, "Multiply the bracket by h/2.",
                    say="Here h/2 = 2 ÷ 2 = 1, so the area is just the bracket:",
                    done="25 square units, the whole rule in one line."),
            ],
        },
        "gold": {
            "display": "A velocity-time graph shows \\(v = 2, 5, 8, 9, 6\\) at \\(t = 0, 1, 2, 3, 4\\), width \\(h = 1\\). Estimate the distance travelled.",
            "label": "Together: the gold move",
            "steps": [
                box("first + last: 2 + 6 = ", 8, "Add the two end speeds.",
                    say="On a velocity-time graph the <strong>area is the distance</strong>. Use the trapezium rule across all four strips. Ends first:"),
                box("add the three middle speeds: 5 + 8 + 9 = ", 22, "Add y1, y2 and y3."),
                box("double the middle: 2 × 22 = ", 44, "Interior values count twice.",
                    done="Interior values always count twice."),
                box("bracket: 8 + 44 = ", 52, "Ends plus doubled middle."),
                box("0.5 × 52 = ", 26, "Multiply the bracket by 0.5.",
                    say="h/2 = 1 ÷ 2 = 0.5, so:",
                    done="26 metres of distance, read straight off the area."),
            ],
        },
    },
}

json.dump(pd, io.open("lesson_graphs-L08.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_graphs-L08.json")

# quick self-audit: em dash scan + word counts
s = json.dumps(pd, ensure_ascii=False)
print("em dash present:", "—" in s)
def wc(t): return len([w for w in t.replace("\\("," ").replace("\\)"," ").split() if w])
print("method_card content words:", wc(pd["method_card"]["content"]))
for tier in ("bronze","silver","gold"):
    print(tier, "tier_guide step words:", sum(wc(x) for x in pd["tier_guides"][tier]["steps"]))
