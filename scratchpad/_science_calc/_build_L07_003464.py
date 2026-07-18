# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # proper minus sign

pd = json.load(io.open("_canonical_L07.json", encoding="utf-8"))

# ---- method_card: remove em dash, slim ----
pd["method_card"]["title"] = "Speed, Acceleration and Motion Graphs"
pd["method_card"]["steps"] = [
    "Speed = distance ÷ time (m/s = m ÷ s)",
    "Acceleration = change in speed ÷ time (m/s²). Change in speed = final " + MINUS + " start",
    "Distance-time graph: gradient = speed; a flat line means stationary",
    "Velocity-time graph: gradient = acceleration; area under the line = distance"
]
pd["method_card"]["content"] = (
    "<p>Two equations and two graph types cover this lesson.</p>"
    "<p><strong>Speed:</strong> average speed (m/s) = distance (m) ÷ time (s).</p>"
    "<p><strong>Acceleration:</strong> a (m/s²) = change in speed (m/s) ÷ time (s). "
    "A negative value means deceleration.</p>"
    "<p><strong>Distance-time graph:</strong> gradient = speed; a horizontal line means stationary.</p>"
    "<p><strong>Velocity-time graph:</strong> gradient = acceleration; area under the line = distance.</p>"
    "<p><strong>Watch out:</strong> use the change in speed (not the final speed) for acceleration, "
    "and use ½ × base × height for a triangle's area.</p>"
)

# ---- pre-existing em dashes in preserved fields: minimal repair to ": " ----
EM = "—"
if EM in pd.get("exam_context", {}).get("frequency", ""):
    pd["exam_context"]["frequency"] = pd["exam_context"]["frequency"].replace(" " + EM + " ", ": ").replace(EM, ":")
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and EM in st["label"]:
            st["label"] = st["label"].replace(" " + EM + " ", ": ").replace(EM, ":")

pb = pd["problem_bank"]
pb["bronze_description"] = "One equation, values already in m and s: substitute and go."
pb["silver_description"] = "Convert the units or find the change in speed first, or read a distance off a graph."
pb["gold_description"] = "Chain two steps: v² = u² + 2as with a square root, or a multi-part graph area."


def box(pre, ans, hint, say=None, post="", done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if say is not None:
        d["say"] = say
    if done is not None:
        d["done"] = done
    if phase:
        d["phase"] = "substitute"
    return d


def sayonly(s):
    return {"say": s}


# ================= BRONZE =================
b = pb["bronze"]

# B1 540 m / 60 s = 9
b[0]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 0.11,
    "message": "That looks like time ÷ distance. Speed is distance ÷ time: 540 ÷ 60 = 9 m/s."
}]
b[0]["guided_steps"] = [
    sayonly("Speed = distance ÷ time. The values are already in metres and seconds, so no converting."),
    box("Substitute the numbers: speed = 540 ÷ __ (the time in s)", 60, "The time given is 60 s."),
    box("540 ÷ 60 = ", 9, "Distance divided by time.", say="Now divide:", phase=True),
    box("Check: 9 × 60 = ", 540, "Speed × time should return the distance.", done="That returns the distance, so 9 m/s is right."),
    sayonly("The average speed is 9 m/s."),
]

# B2 25 m/s * 40 s = 1000
b[1]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 1.6,
    "message": "Distance = speed × time, so multiply: 25 × 40 = 1,000 m. Dividing (40 ÷ 25 = 1.6) uses the equation upside down."
}]
b[1]["guided_steps"] = [
    sayonly("Distance = speed × time. Units are already m/s and s."),
    box("Substitute: distance = 25 × __ (the time in s)", 40, "The time is 40 s."),
    box("25 × 40 = ", 1000, "Speed times time.", say="Now multiply:", phase=True),
    box("Check: 1000 ÷ 40 = ", 25, "Distance ÷ time should give the speed back.", done="That returns the speed, so 1,000 m is right."),
    sayonly("The distance covered is 1,000 m."),
]

# B3 0->30 in 6 s = 5
b[2]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 0.2,
    "message": "Acceleration = change in speed ÷ time = 30 ÷ 6 = 5 m/s². Dividing time by speed (6 ÷ 30) gives 0.2, which is upside down."
}]
b[2]["guided_steps"] = [
    sayonly("Acceleration = change in speed ÷ time. It starts from rest, so the change is just 30 m/s."),
    box("Change in speed = 30 " + MINUS + " 0 = ", 30, "Final minus start."),
    box("30 ÷ 6 = ", 5, "Change in speed divided by time.", say="Divide by the time:", phase=True),
    box("Check: 5 × 6 = ", 30, "Acceleration × time gives the change in speed.", done="That returns the speed gained, so 5 m/s² is right."),
    sayonly("The acceleration is 5 m/s²."),
]

# B4 CHANGED 24->0 in 4 s magnitude = 6
b[3]["display"] = "A ball decelerates from 24 m/s to 0 in 4 s. What is the magnitude of its acceleration in m/s²?"
b[3]["solutions"] = [6]
b[3]["equation_hint"] = "a = change in speed ÷ time. Change = 24 " + MINUS + " 0 = 24 m/s."
b[3]["misconceptions"] = [{
    "pattern": "wrong_sign", "check": "common", "expect": -6,
    "message": "The change is 24 " + MINUS + " 0 = 24 m/s over 4 s, so a = 6 m/s². The question asks for magnitude, so the answer is positive 6, not −6."
}]
b[3]["guided_steps"] = [
    sayonly("Acceleration = change in speed ÷ time. The ball slows to rest, so the change is 24 m/s."),
    box("Change in speed = 24 " + MINUS + " 0 = ", 24, "Final minus start, size only."),
    box("24 ÷ 4 = ", 6, "Change in speed divided by time.", say="Divide by the time:", phase=True),
    box("Check: 6 × 4 = ", 24, "Size of acceleration × time gives the change.", done="That returns the speed lost, so the magnitude is 6 m/s²."),
    sayonly("The magnitude of the acceleration is 6 m/s²."),
]

# B5 dropped 3 s g=10 v=30
b[4]["misconceptions"] = [{
    "pattern": "wrong_equation", "check": "common", "expect": 45,
    "message": "This asks for the speed, not the distance. Speed = g × t = 10 × 3 = 30 m/s. (½ × 10 × 3² = 45 m would be the distance fallen.)"
}]
b[4]["guided_steps"] = [
    sayonly("Dropped from rest, so final speed = acceleration × time, with g = 10 m/s²."),
    box("Substitute: v = 10 × __ (the time in s)", 3, "It falls for 3 s."),
    box("10 × 3 = ", 30, "g times time.", say="Now multiply:", phase=True),
    box("Check: 30 ÷ 3 = ", 10, "Speed ÷ time should give g back.", done="That returns g, so 30 m/s is right."),
    sayonly("The final speed is 30 m/s."),
]

# B6 convert 90 km/h to m/s = 25
b[5]["misconceptions"] = [{
    "pattern": "unit_error", "check": "common", "expect": 324,
    "message": "To go from km/h to m/s, divide by 3.6: 90 ÷ 3.6 = 25 m/s. Multiplying by 3.6 (324) goes the wrong way."
}]
b[5]["guided_steps"] = [
    sayonly("To change km/h into m/s, divide by 3.6."),
    box("Write the speed to convert: __ km/h", 90, "The value given."),
    box("90 ÷ 3.6 = ", 25, "km/h ÷ 3.6 = m/s.", say="Now divide by 3.6:", phase=True),
    box("Check: 25 × 3.6 = ", 90, "m/s × 3.6 gives km/h back.", done="That returns 90 km/h, so 25 m/s is right."),
    sayonly("90 km/h is 25 m/s."),
]

# ================= SILVER =================
s = pb["silver"]

# S1 5->25 in 8 s = 2.5
s[0]["misconceptions"] = [{
    "pattern": "final_speed", "check": "common", "expect": 3.125,
    "message": "Use the CHANGE in speed, not the final speed: 25 " + MINUS + " 5 = 20 m/s, so a = 20 ÷ 8 = 2.5 m/s². Using 25 gives 3.125."
}]
s[0]["guided_steps"] = [
    sayonly("Acceleration = change in speed ÷ time. This one does NOT start from rest, so find the change first."),
    box("Change in speed = 25 " + MINUS + " 5 = ", 20, "Final minus start."),
    box("20 ÷ 8 = ", 2.5, "Change divided by time.", say="Divide by the time:", phase=True),
    box("Check: 5 + 2.5 × 8 = ", 25, "Start + acceleration × time = final speed.", done="Start speed plus the gain returns 25 m/s, so 2.5 m/s² is right."),
    sayonly("The acceleration is 2.5 m/s²."),
]

# S2 triangle 0->20 over 10 s = 100
s[1]["misconceptions"] = [{
    "pattern": "wrong_area", "check": "common", "expect": 200,
    "message": "The shape is a triangle, so area = ½ × base × height = ½ × 10 × 20 = 100 m. Using base × height (200) forgets the ½."
}]
s[1]["guided_steps"] = [
    sayonly("Distance = area under a velocity-time line. This section is a triangle."),
    box("Base (time) = __ s", 10, "Read the time axis."),
    box("Height (top speed) = __ m/s", 20, "Read the speed axis."),
    box("½ × 10 × 20 = ", 100, "Half of base times height.", say="Triangle area = ½ × base × height:", phase=True),
    box("10 × 10 = ", 100, "Average speed × time = distance.", say="Check using average speed: average = ½ × 20 = 10 m/s, over 10 s:", done="Same 100 m, so it is right."),
    sayonly("The distance is 100 m."),
]

# S3 rectangle constant 20 for 20 s = 400
s[2]["misconceptions"] = [{
    "pattern": "wrong_area", "check": "common", "expect": 200,
    "message": "This section is a rectangle (constant speed), so area = base × height = 20 × 20 = 400 m. No ½ here; that is only for triangles."
}]
s[2]["guided_steps"] = [
    sayonly("Constant speed, so the graph section is a rectangle. Distance = area = base × height."),
    box("Base (time) = __ s", 20, "The constant-speed part lasts 20 s."),
    box("Height (speed) = __ m/s", 20, "The steady speed."),
    box("20 × 20 = ", 400, "No ½ for a rectangle.", say="Rectangle area = base × height:", phase=True),
    box("Check: 400 ÷ 20 = ", 20, "Distance ÷ time gives the speed back.", done="That returns the speed, so 400 m is right."),
    sayonly("The distance in this section is 400 m."),
]

# S4 30->0 in 5 s = 6
s[3]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 0.17,
    "message": "Deceleration = change ÷ time = 30 ÷ 5 = 6 m/s². Dividing time by change (5 ÷ 30 = 0.17) is upside down."
}]
s[3]["guided_steps"] = [
    sayonly("Deceleration = change in speed ÷ time. It slows to rest, so the change is 30 m/s."),
    box("Change in speed = 30 " + MINUS + " 0 = ", 30, "Final minus start, size only."),
    box("30 ÷ 5 = ", 6, "Change divided by time.", say="Divide by the time:", phase=True),
    box("Check: 6 × 5 = ", 30, "Deceleration × time gives the change.", done="That returns the speed lost, so 6 m/s² is right."),
    sayonly("The deceleration is 6 m/s²."),
]

# S5 train multi-section = 825
s[4]["misconceptions"] = [{
    "pattern": "wrong_area", "check": "common", "expect": 1050,
    "message": "The sloped sections are triangles, so halve them: ½ × 10 × 30 = 150 and ½ × 5 × 30 = 75. With the 600 rectangle, total = 825 m. Forgetting the halves gives 1050."
}]
s[4]["guided_steps"] = [
    sayonly("Split the graph into three areas: a triangle, a rectangle, and a triangle. Find each, then add."),
    box("Triangle 1 (speeding up) = ½ × 10 × 30 = ", 150, "Half base times height."),
    box("Rectangle (steady) = 20 × 30 = ", 600, "Base times height, no half."),
    box("Triangle 2 (slowing) = ½ × 5 × 30 = ", 75, "Half base times height."),
    box("150 + 600 + 75 = ", 825, "Sum the three areas.", say="Now add the three sections:", phase=True),
    box("Check the middle: 600 ÷ 30 = ", 20, "Rectangle distance ÷ speed gives its time.", done="That returns the 20 s of steady speed, so 825 m stands."),
    sayonly("The total distance is 825 m."),
]

# ================= GOLD =================
g = pb["gold"]

# G1 brake 20->0 in 50 m, a = 4 (v^2-u^2=2as), higher_only
g[0]["higher_only"] = True
g[0]["equation_hint"] = "v² " + MINUS + " u² = 2as, then a = (v² " + MINUS + " u²) ÷ (2s)"
g[0]["misconceptions"] = [
    {"pattern": "forgot_step", "check": "common", "expect": 8,
     "message": "a = (v² " + MINUS + " u²) ÷ (2s) = 400 ÷ (2 × 50) = 400 ÷ 100 = 4 m/s². Forgetting the 2 gives 400 ÷ 50 = 8."},
    {"pattern": "wrong_sign", "check": "common", "expect": -4,
     "message": "The calculation gives −4 m/s² (the car is slowing). The question wants the size, so the deceleration is 4 m/s²."},
]
g[0]["guided_steps"] = [
    sayonly("Rearrange v² " + MINUS + " u² = 2as to find a: a = (v² " + MINUS + " u²) ÷ (2s). Here u = 20, v = 0, s = 50."),
    box("u² = 20² = ", 400, "Square the starting speed."),
    box("v² " + MINUS + " u² = 0 " + MINUS + " 400 = ", -400, "Final squared minus start squared."),
    box("2s = 2 × 50 = ", 100, "Twice the distance."),
    box("−400 ÷ 100 = ", -4, "This is negative because it slows down.", say="Now divide:", phase=True),
    box("Magnitude = ", 4, "Drop the minus sign for the size.", say="The question asks for the size of the deceleration.", done="4 m/s², matching a car braking hard."),
    sayonly("The deceleration is 4 m/s²."),
]

# G2 cliff 45 m g=10 v=30, higher_only
g[1]["higher_only"] = True
g[1]["equation_hint"] = "v² = u² + 2as, then take the square root for v"
g[1]["misconceptions"] = [
    {"pattern": "forgot_square_root", "check": "common", "expect": 900,
     "message": "v² = 900, so take the square root: v = √900 = 30 m/s. Stopping at 900 forgets the square root."},
    {"pattern": "forgot_step", "check": "common", "expect": 21.2,
     "message": "v² = 2as = 2 × 10 × 45 = 900. Leaving out the 2 gives 450 and v ≈ 21.2 m/s, which is wrong."},
]
g[1]["guided_steps"] = [
    sayonly("Use v² = u² + 2as. Dropped from rest so u = 0, a = 10, s = 45."),
    box("2as = 2 × 10 × 45 = ", 900, "Two times a times s."),
    box("v² = 0 + 900 = ", 900, "Add u², which is zero here."),
    box("√900 = ", 30, "What squared gives 900?", say="Take the square root, the step people forget:", phase=True),
    box("Check: 30² = ", 900, "Squaring the answer should return 900.", done="Matches 2as, so 30 m/s is right."),
    sayonly("The stone hits the ground at 30 m/s."),
]

# G3 v-t graph three areas = 375
g[2]["equation_hint"] = "Distance = area under the line (triangles use ½ × base × height)"
g[2]["misconceptions"] = [{
    "pattern": "wrong_area", "check": "common", "expect": 500,
    "message": "The two sloped sections are triangles: ½ × 5 × 25 = 62.5 m each. With the middle rectangle 10 × 25 = 250 m, the total is 375 m. Forgetting the ½ gives 500."
}]
g[2]["guided_steps"] = [
    sayonly("Distance = total area. Split into triangle, rectangle, triangle."),
    box("Triangle 1 = ½ × 5 × 25 = ", 62.5, "Half base times height."),
    box("Rectangle = 10 × 25 = ", 250, "Steady section, base times height."),
    box("Triangle 2 = ½ × 5 × 25 = ", 62.5, "Same as the first triangle."),
    box("Total = 62.5 + 250 + 62.5 = ", 375, "Add the three areas.", say="Now add the sections:", phase=True),
    box("Check: the two triangles together = 62.5 + 62.5 = ", 125, "Add the triangle areas.", done="Plus the 250 rectangle gives 375 m, so it is right."),
    sayonly("The total distance is 375 m."),
]

# ================= tier_guides =================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Pick the equation the words point to: speed = distance ÷ time, or acceleration = change in speed ÷ time.",
            "The values are already in the right units (metres and seconds), so substitute them straight in.",
            "Divide, then write the answer with its unit, m/s or m/s².",
        ],
        "example": {
            "question": "A runner covers 300 m in 60 s. Find the average speed.",
            "steps": [
                {"label": "Equation", "content": "<p>speed = distance ÷ time</p>"},
                {"label": "Substitute", "content": "<p>speed = 300 ÷ 60</p>"},
                {"label": "Check", "content": "<p>5 m/s × 60 s = 300 m ✓</p>"},
                {"label": "Answer", "content": "<p><strong>5 m/s</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: convert or rearrange first",
        "steps": [
            "One thing is not ready yet: either convert the units (km/h ÷ 3.6 = m/s) or find the change in speed (final " + MINUS + " start) before dividing.",
            "Do that single set-up step first, and it becomes a bronze question.",
            "For a velocity-time graph, distance = area under the line: triangle = ½ × base × height, rectangle = base × height.",
        ],
        "example": {
            "question": "A car speeds up from 6 m/s to 24 m/s in 9 s. Find the acceleration.",
            "steps": [
                {"label": "Change in speed", "content": "<p>24 " + MINUS + " 6 = 18 m/s</p>"},
                {"label": "Divide by time", "content": "<p>18 ÷ 9</p>"},
                {"label": "Check", "content": "<p>6 + 2 × 9 = 24 m/s ✓</p>"},
                {"label": "Answer", "content": "<p><strong>2 m/s²</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two steps",
        "steps": [
            "These need more than one move: a graph split into several areas, or the equation v² = u² + 2as (check whether your board gives you this one).",
            "With v² = u² + 2as, substitute the numbers, then take the square root at the end to find v. Missing that root is the classic slip.",
            "For a multi-part graph, work out each section's area and add them up.",
        ],
        "example": {
            "question": "A car accelerates from rest at 3 m/s² over 24 m. Find its final speed (v² = u² + 2as).",
            "steps": [
                {"label": "Substitute", "content": "<p>v² = 0 + 2 × 3 × 24 = 144</p>"},
                {"label": "Square root", "content": "<p>v = √144</p>"},
                {"label": "Check", "content": "<p>12² = 144 = 2 × 3 × 24 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>12 m/s</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================= guided (opener + teach) =================
pd["guided"] = {
    "opener": {
        "label": "Before any equations",
        "display": ("Picture a car pulling away from traffic lights. Every second it gains the same amount of speed."
                    "<br>After 4 seconds it is moving at 12 m/s."),
        "steps": [
            box("Extra speed gained each second = ", 3,
                "12 m/s shared equally over 4 seconds.",
                say="No equations yet, just share it out. It gained 12 m/s evenly over 4 seconds.",
                post=" m/s"),
            box("So after 2 seconds it is moving at ", 6,
                "3 m/s gained each second, for 2 seconds.",
                say="That steady 3 m/s every second has a name: acceleration.",
                post=" m/s"),
            sayonly("That is all acceleration is: the speed added each second. As an equation, "
                    "acceleration = change in speed ÷ time = 12 ÷ 4 = 3 m/s². "
                    "The little ² just means 'per second, each second'."),
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A runner covers 400 m in 50 s. Calculate the average speed.",
            "steps": [
                {"say": "Speed tells you the distance covered each second. The equation: speed = distance ÷ time."},
                box("Write the distance in metres: ", 400, "Read it from the question."),
                box("Write the time in seconds: ", 50, "Read it from the question."),
                box("Now divide: 400 ÷ 50 = ", 8, "Distance divided by time.", done="That is the speed in m/s."),
                box("Check: 8 × 50 = ", 400, "Speed × time returns the distance.", done="Back to the 400 m we started with. Correct."),
                {"say": "So the average speed is 8 m/s."},
            ],
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "A car travelling at 72 km/h brakes to rest in 5 s. Calculate the deceleration in m/s².",
            "steps": [
                {"say": "The speed is in km/h but the answer needs m/s². Convert the units first, the silver move."},
                box("Speed in m/s = 72 ÷ 3.6 = ", 20, "km/h ÷ 3.6 = m/s.", done="Now everything is in the right units."),
                box("Change in speed = 20 " + MINUS + " 0 = ", 20, "Final minus start."),
                box("Deceleration = 20 ÷ 5 = ", 4, "Change divided by time.", done="Four metres per second squared of braking."),
                box("Check: 4 × 5 = ", 20, "Deceleration × time gives the speed lost.", done="That is the 20 m/s it lost. Correct."),
                {"say": "So the deceleration is 4 m/s²."},
            ],
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "A motorbike accelerates from rest at 4 m/s² over 18 m. Using v² = u² + 2as, find its final speed.",
            "steps": [
                {"say": "Two moves here: substitute into v² = u² + 2as, then square root at the end. Start from rest, so u = 0."},
                box("2as = 2 × 4 × 18 = ", 144, "Two times a times s."),
                box("So v² = 0 + 144 = ", 144, "Add u², which is zero."),
                box("v = √144 = ", 12, "The square-root step, easy to miss.", done="That final root is the trap."),
                box("Check: 12² = ", 144, "Squaring the answer returns 2as.", done="Matches 144. Correct."),
                {"say": "So the final speed is 12 m/s."},
            ],
        },
    },
}

with io.open("lesson_physics-calculations-L07@003464e169.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

print("written. keys:", list(pd.keys()))
