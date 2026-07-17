# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_graphsL04.json", encoding="utf-8"))

MINUS = "−"  # unicode minus for plain text

# ---------- SVG line-graph generator (opener + teach figures) ----------
def svg_graph(points, xmax, xstep, ymax, ystep, xlabel, ylabel, aria):
    x0, xR, y0, yT = 40.0, 230.0, 165.0, 25.0
    W = xR - x0
    H = y0 - yT
    def px(t): return round(x0 + t / xmax * W, 1)
    def py(v): return round(y0 - v / ymax * H, 1)
    s = []
    s.append('<svg viewBox="0 0 260 200" role="img" aria-label="%s" '
             'style="max-width:260px" font-family="Inter, sans-serif">' % aria)
    # axes
    s.append('<line x1="40" y1="%s" x2="40" y2="%s" stroke="currentColor" stroke-width="1.2"/>' % (yT, y0))
    s.append('<line x1="40" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.2"/>' % (y0, xR, y0))
    # y ticks
    v = 0
    while v <= ymax + 1e-9:
        yy = py(v)
        s.append('<line x1="37" y1="%s" x2="40" y2="%s" stroke="currentColor" stroke-width="1"/>' % (yy, yy))
        s.append('<text x="33" y="%s" font-size="9" fill="currentColor" text-anchor="end">%s</text>' % (round(yy + 3, 1), int(v)))
        v += ystep
    # x ticks
    t = 0
    while t <= xmax + 1e-9:
        xx = px(t)
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>' % (xx, y0, xx, y0 + 3))
        s.append('<text x="%s" y="179" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (xx, int(t)))
        t += xstep
    # polyline
    pts = " ".join("%s,%s" % (px(a), py(b)) for a, b in points)
    s.append('<polyline points="%s" fill="none" stroke="#dc2626" stroke-width="2"/>' % pts)
    for a, b in points:
        s.append('<circle cx="%s" cy="%s" r="2.5" fill="#dc2626"/>' % (px(a), py(b)))
    # axis titles
    s.append('<text x="135" y="195" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % xlabel)
    s.append('<text x="12" y="95" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 95)">%s</text>' % ylabel)
    s.append('</svg>')
    return "".join(s)

# ---------- Chart.js scatter config (bank figures) ----------
def scatter(points, xmax, xstep, xtitle, ymax, ystep, ytitle, color):
    return {
        "type": "scatter",
        "data": {"datasets": [{
            "type": "line",
            "data": [{"x": a, "y": b} for a, b in points],
            "tension": 0, "fill": False,
            "borderColor": color, "pointRadius": 4, "pointBackgroundColor": color
        }]},
        "options": {"scales": {
            "x": {"min": 0, "max": xmax, "ticks": {"stepSize": xstep},
                  "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": xtitle, "display": True}},
            "y": {"min": 0, "max": ymax, "ticks": {"stepSize": ystep},
                  "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": ytitle, "display": True},
                  "beginAtZero": True}
        }}
    }

def box(pre, post, answer, hint, done=None, phase=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    if say is not None: d["say"] = say
    return d

def sayk(say):
    return {"say": say}

# =====================================================================
# METHOD CARD (slim)
# =====================================================================
method_card = {
    "title": "How to Interpret Real-Life Graphs",
    "steps": [
        "Check the axes first: distance-time or speed-time?",
        "Distance-time: the gradient is the speed; a flat line means stopped.",
        "Speed-time: the gradient is the acceleration; the area underneath is the distance.",
        "Match the units before dividing (turn minutes into hours)."
    ],
    "content": "<p><strong>Distance-time graphs</strong> show a journey. The gradient is the <strong>speed</strong>: steeper means faster, and a flat section means stopped.</p><p><strong>Speed-time graphs</strong> show how speed changes. The gradient is the <strong>acceleration</strong>, and the <strong>area under</strong> the line is the total <strong>distance</strong>. Split that area into triangles and rectangles.</p><p>Always read the axis labels first, and convert minutes to hours before dividing.</p>",
    "example": "<p><strong>A car travels at 60 km/h for 45 minutes. How far does it go?</strong></p><p>45 min = 0.75 h, so distance = 60 × 0.75 = 45 km.</p>"
}

# =====================================================================
# TIER GUIDES
# =====================================================================
tier_guides = {
    "bronze": {
        "title": "Bronze: speed, distance and time",
        "steps": [
            "<strong>Speed = distance ÷ time.</strong> Rearranged: distance = speed × time, and time = distance ÷ speed.",
            "On a distance-time graph, a <strong>flat line</strong> means stopped and a <strong>steeper</strong> line means faster.",
            "Keep units matched: km with hours gives km/h."
        ],
        "example": {
            "question": "A car travels 180 km in 4 hours. Find its speed.",
            "steps": [
                {"label": "Formula", "content": "speed = distance ÷ time"},
                {"label": "Substitute", "content": "= 180 ÷ 4"},
                {"label": "Speed", "content": "= 45 km/h", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: speed-time graphs and unit changes",
        "steps": [
            "On a <strong>speed-time</strong> graph the gradient is the <strong>acceleration</strong>: change in speed ÷ time.",
            "The <strong>area under</strong> a speed-time graph is the <strong>distance</strong>. Split it into triangles and rectangles.",
            "Change minutes to hours before dividing: 45 min = 45 ÷ 60 = 0.75 h."
        ],
        "example": {
            "question": "A car speeds up from 0 to 20 m/s in 8 s. Find the acceleration.",
            "steps": [
                {"label": "Gradient", "content": "(20 − 0) ÷ 8"},
                {"label": "Acceleration", "content": "= 2.5 m/s²", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: multi-stage journeys",
        "steps": [
            "Break a journey into stages: speeding up, steady, slowing down. Work out each stage on its own.",
            "For total distance, add the area of every stage: two triangles and a rectangle for a trapezium.",
            "For average speed use <strong>total distance ÷ total time</strong>, never the mean of the separate speeds."
        ],
        "example": {
            "question": "A bus goes from 0 to 15 m/s in 5 s, then holds 15 m/s for 10 s. Total distance?",
            "steps": [
                {"label": "Triangle", "content": "½ × 5 × 15 = 37.5"},
                {"label": "Rectangle", "content": "15 × 10 = 150"},
                {"label": "Total", "content": "= 187.5 m", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# =====================================================================
# OPENER (concrete hook: reading a real journey)
# =====================================================================
opener_svg = svg_graph(
    [(0, 0), (15, 6), (30, 6), (45, 0)],
    xmax=45, xstep=15, ymax=8, ystep=2,
    xlabel="Time (min)", ylabel="Distance (km)",
    aria="Distance-time graph of Sam's bike ride: distance from home rises from 0 to 6 km over the first 15 minutes, stays at 6 km from 15 to 30 minutes, then falls back to 0 by 45 minutes"
)
guided = {
    "opener": {
        "display": opener_svg + "<p>The graph shows Sam's bike ride to the park and back. Distance from home is on the up axis, time in minutes along the bottom.</p>",
        "steps": [
            {"pre": "How far away is the park? Read the highest the line reaches: ", "post": " km", "answer": 6,
             "hint": "The line climbs, then flattens. Read that flat height."},
            {"pre": "Sam waited at the park while the line is flat, from 15 min to 30 min. How many minutes is that? ", "post": " min", "answer": 15,
             "hint": "Take the start time from the end time of the flat part: 30 − 15."},
            {"pre": "The whole trip finishes where the line reaches 0 again. At what time, in minutes? ", "post": " min", "answer": 45,
             "hint": "Read the time where the line touches the bottom on the right."},
            {"say": "You just read a <strong>distance-time graph</strong> by common sense. The height is distance from home, a <strong>flat line means not moving</strong>, and a steeper slope means going faster. That slope is the <strong>speed</strong>. Speed-time graphs work the same way, and their <strong>area</strong> gives distance. That is the whole of today's lesson."}
        ]
    },
    "teach": {}
}

# --- teach bronze (no figure) ---
guided["teach"]["bronze"] = {
    "display": "A coach drives 120 km in 3 hours at a steady speed, then keeps going for 2 more hours at the same speed. How far does it travel in total?",
    "steps": [
        sayk("Steady speed means we can find one speed and reuse it for the rest of the trip."),
        box("Speed = distance ÷ time = 120 ÷ 3 = ", " km/h", 40, "Divide the distance by the time."),
        box("At that speed each hour covers ", " km", 40, "At 40 km/h you go 40 km every hour."),
        box("In 2 more hours: 40 × 2 = ", " km", 80, "Multiply the speed by 2 hours."),
        box("Total distance = 120 + 80 = ", " km", 200, "Add the first part to the extra part.",
            done="Same speed throughout, so the distances just add up. That was the whole point.")
    ]
}

# --- teach silver (speed-time SVG) ---
teach_silver_svg = svg_graph(
    [(0, 0), (6, 18), (14, 18)],
    xmax=14, xstep=2, ymax=20, ystep=5,
    xlabel="Time (s)", ylabel="Speed (m/s)",
    aria="Speed-time graph of a motorbike: speed rises from 0 to 18 metres per second over the first 6 seconds, then stays at 18 metres per second until 14 seconds"
)
guided["teach"]["silver"] = {
    "display": teach_silver_svg + "<p>The speed-time graph shows a motorbike. It speeds up from rest to 18 m/s in 6 s, then holds 18 m/s until 14 s. Find the total distance.</p>",
    "steps": [
        sayk("On a speed-time graph the <strong>area under the line</strong> is the distance. Split it into a triangle and a rectangle."),
        box("Acceleration = (18 − 0) ÷ 6 = ", " m/s²", 3, "Gradient is change in speed over time."),
        box("Triangle while speeding up: ½ × 6 × 18 = ", " m", 54, "Area of a triangle is ½ × base × height."),
        box("Rectangle at steady speed: 8 × 18 = ", " m", 144, "The steady part lasts from 6 s to 14 s, that is 8 s."),
        box("Total distance = 54 + 144 = ", " m", 198, "Add the two areas.",
            done="Area under the graph is the distance. That was the whole point.")
    ]
}

# --- teach gold (trapezium SVG) ---
teach_gold_svg = svg_graph(
    [(0, 0), (4, 12), (14, 12), (17, 0)],
    xmax=18, xstep=3, ymax=15, ystep=5,
    xlabel="Time (s)", ylabel="Speed (m/s)",
    aria="Speed-time graph of a tram forming a trapezium: speed rises from 0 to 12 metres per second over 4 seconds, stays at 12 until 14 seconds, then falls back to 0 by 17 seconds"
)
guided["teach"]["gold"] = {
    "display": teach_gold_svg + "<p>A tram speeds up from rest to 12 m/s in 4 s, holds 12 m/s for 10 s, then slows to rest in 3 s. Find the total distance.</p>",
    "steps": [
        sayk("A trapezium splits into two triangles and a rectangle. Find each area, then add."),
        box("Speeding-up triangle: ½ × 4 × 12 = ", " m", 24, "½ × base × height."),
        box("Steady rectangle: 10 × 12 = ", " m", 120, "base × height, over the 10 s at 12 m/s."),
        box("Slowing-down triangle: ½ × 3 × 12 = ", " m", 18, "½ × base × height."),
        box("Total distance = 24 + 120 + 18 = ", " m", 162, "Add all three areas.",
            done="Every stage's area adds to the total distance. That was the whole point.")
    ]
}

# =====================================================================
# PROBLEM BANK
# =====================================================================
pb = {}
pb["bronze_description"] = "Read distance-time graphs and use speed = distance ÷ time with matching units."
pb["silver_description"] = "Read speed-time graphs: gradient for acceleration, area for distance, plus minute-to-hour conversions."
pb["gold_description"] = "Multi-stage journeys: total distance from combined areas, and average speed over a whole trip."

# preserve existing bronze charts from live
live_bronze = live["problem_bank"]["bronze"]
live_silver = live["problem_bank"]["silver"]
live_gold = live["problem_bank"]["gold"]

def mc(pattern, message, expect):
    return {"check": "common", "pattern": pattern, "message": message, "expect": expect}

# ----- BRONZE -----
bronze = []

# B0 rest = 20 (keep chart)
bronze.append({
    "chart": live_bronze[0]["chart"],
    "display": "The distance-time graph shows a jogger's run. How long did the jogger rest for?",
    "solutions": [20], "calculator": False, "input_type": "single_value",
    "hint": "A rest is a flat, horizontal section; measure how long it lasts.",
    "misconceptions": [mc("wrong_reading",
        "A rest is a flat, horizontal line. It runs from 20 min to 40 min, so the rest lasts 40 − 20 = 20 minutes. If you wrote 40 you read the end time, not the length.", 40)],
    "guided_steps": [
        sayk("A rest shows up as a flat, horizontal section: the distance is not changing."),
        box("The flat part starts at time = ", " min", 20, "Read where the line first goes flat."),
        box("The flat part ends at time = ", " min", 40, "Read where the line starts climbing again.", phase="substitute"),
        box("Rest length = 40 − 20 = ", " min", 20, "Take the start time from the end time."),
        box("Check: over that flat part the distance stayed at ", " km", 6, "Read the height of the flat line.",
            done="The distance did not change, so the jogger really rested for 20 minutes.")
    ]
})

# B1 speed first 10 min = 0.4 (keep chart)
bronze.append({
    "chart": live_bronze[1]["chart"],
    "display": "The distance-time graph shows a cyclist's journey. What was the cyclist's speed during the first 10 minutes? Give your answer in km per minute.",
    "solutions": [0.4], "calculator": False, "input_type": "single_value",
    "hint": "Read the distance at 10 minutes, then divide it by 10.",
    "misconceptions": [mc("wrong_formula",
        "Speed = distance ÷ time = 4 ÷ 10 = 0.4 km/min. If you got 2.5 you divided time by distance, which is upside down.", 2.5)],
    "guided_steps": [
        sayk("Speed is distance ÷ time. Read the graph to get the distance first."),
        box("Read the distance at time = 10 min: ", " km", 4, "Follow the line up to t = 10 and read across."),
        box("Speed = distance ÷ time = 4 ÷ 10 = ", " km/min", 0.4, "Divide the 4 km by 10 minutes.", phase="substitute"),
        box("Check: 0.4 km/min × 10 min = ", " km", 4, "Multiply back to test it.",
            done="It returns the 4 km on the graph, so 0.4 km/min is right.")
    ]
})

# B2 total distance = 24 (was 20, duplicate of B0) -> new chart
b2chart = {
    "data": {
        "labels": [0, 10, 20, 30, 40, 50],
        "datasets": [{"data": [0, 6, 12, 12, 18, 24], "fill": False, "tension": 0,
                      "borderColor": "#f59e0b", "pointRadius": 4, "pointBackgroundColor": "#f59e0b"}]
    },
    "type": "line",
    "options": {"scales": {
        "x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "ticks": {"stepSize": 10},
              "title": {"text": "Time (minutes)", "display": True}},
        "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 6},
              "title": {"text": "Distance (km)", "display": True}, "beginAtZero": True}
    }}
}
bronze.append({
    "chart": b2chart,
    "display": "The distance-time graph shows a person's journey. What total distance did the person travel?",
    "solutions": [24], "calculator": False, "input_type": "single_value",
    "hint": "The total distance is the final height the line reaches.",
    "misconceptions": [mc("wrong_reading",
        "The line never comes back down, so the total distance is its final height at t = 50: 24 km. If you got 18 you stopped reading at t = 40.", 18)],
    "guided_steps": [
        sayk("The line only ever goes up or stays flat, so the total distance is the value it finishes on."),
        box("Read the distance at time = 40 min: ", " km", 18, "Follow the line up to t = 40."),
        box("Read the final distance at time = 50 min: ", " km", 24, "Follow the line to its right-hand end.", phase="substitute"),
        box("Total distance travelled = ", " km", 24, "The final height is the total distance here.",
            done="The line does not return toward 0, so 24 km is the whole distance travelled.")
    ]
})

# B3 150km in 3h -> 50
bronze.append({
    "display": "A car travels 150 km in 3 hours. What is the average speed?",
    "solutions": [50], "calculator": False, "input_type": "single_value",
    "hint": "Speed = distance ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Speed = distance ÷ time = 150 ÷ 3 = 50 km/h. Dividing time by distance (0.02) is upside down.", 0.02)],
    "guided_steps": [
        sayk("Average speed is total distance ÷ total time."),
        box("Write the distance: ", " km", 150, "The distance is given in the question."),
        box("Divide by the time: 150 ÷ 3 = ", " km/h", 50, "Share the 150 km over 3 hours.", phase="substitute"),
        box("Check: 50 km/h × 3 h = ", " km", 150, "Multiply back to test it.",
            done="It returns the 150 km given, so 50 km/h is right.")
    ]
})

# B4 40km/h for 2h -> 80
bronze.append({
    "display": "A bus travels at 40 km/h for 2 hours. How far does it go?",
    "solutions": [80], "calculator": False, "input_type": "single_value",
    "hint": "Distance = speed × time.",
    "misconceptions": [mc("wrong_formula",
        "Distance = speed × time = 40 × 2 = 80 km. If you got 20 you divided; here you multiply speed by time.", 20)],
    "guided_steps": [
        sayk("Distance = speed × time."),
        box("Write the speed: ", " km/h", 40, "The speed is given in the question."),
        box("Multiply by the time: 40 × 2 = ", " km", 80, "Two hours at 40 km each hour.", phase="substitute"),
        box("Check: 80 km ÷ 2 h = ", " km/h", 40, "Divide back to test it.",
            done="It returns the 40 km/h given, so 80 km is right.")
    ]
})

# B5 240km at 80km/h -> 3
bronze.append({
    "display": "A train covers 240 km at 80 km/h. How many hours does it take?",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Time = distance ÷ speed.",
    "misconceptions": [mc("wrong_formula",
        "Time = distance ÷ speed = 240 ÷ 80 = 3 hours. Multiplying (19200) instead of dividing is the slip.", 19200)],
    "guided_steps": [
        sayk("Time = distance ÷ speed."),
        box("Write the distance: ", " km", 240, "The distance is given in the question."),
        box("Divide by the speed: 240 ÷ 80 = ", " hours", 3, "How many 80 km chunks fit into 240 km.", phase="substitute"),
        box("Check: 80 km/h × 3 h = ", " km", 240, "Multiply back to test it.",
            done="It returns the 240 km given, so 3 hours is right.")
    ]
})

# B6 MC (keep)
bronze.append({
    "display": "On a distance-time graph, what does a horizontal line represent?",
    "options": ["Stationary (not moving)", "Constant speed", "Accelerating", "Decelerating"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "On a distance-time graph, flat means not moving.",
    "misconceptions": [mc("graph_type",
        "On a distance-time graph, horizontal means stopped. On a speed-time graph, horizontal means constant speed. Do not mix them up.", 1)]
})

# B7 MC (keep)
bronze.append({
    "display": "On a speed-time graph, what does the area under the line represent?",
    "options": ["Total distance", "Average speed", "Acceleration", "Time taken"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "The area under a speed-time graph gives distance.",
    "misconceptions": [mc("graph_type",
        "Area under a speed-time graph = distance travelled. The gradient (not the area) gives acceleration.", None)]
})

pb["bronze"] = bronze

# ----- SILVER -----
silver = []

# S0 accel first 10s = 2 (keep chart)
silver.append({
    "chart": live_silver[0]["chart"],
    "display": "The speed-time graph shows a car's journey. What is the acceleration during the first 10 seconds?",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Acceleration is the gradient: change in speed ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Acceleration = change in speed ÷ time = 20 ÷ 10 = 2 m/s². If you got 0.5 you divided time by the speed change.", 0.5)],
    "guided_steps": [
        sayk("Acceleration is the gradient of a speed-time graph: change in speed ÷ time."),
        box("Read the speed at time = 10 s: ", " m/s", 20, "Follow the line up to t = 10."),
        box("Acceleration = 20 ÷ 10 = ", " m/s²", 2, "Share the speed gain over 10 seconds.", phase="substitute"),
        box("Check: 2 m/s² for 10 s gives a speed gain of 2 × 10 = ", " m/s", 20, "Multiply back to test it.",
            done="It matches the 20 m/s on the graph, so 2 m/s² is right.")
    ]
})

# S1 total distance 20s = 300 (keep chart)
silver.append({
    "chart": live_silver[1]["chart"],
    "display": "Using the same speed-time graph, find the total distance travelled in 20 seconds.",
    "solutions": [300], "calculator": False, "input_type": "single_value",
    "hint": "Split the area into a triangle then a rectangle and add them.",
    "misconceptions": [mc("area_error",
        "Split the area: triangle (0 to 10 s) ½ × 10 × 20 = 100, plus rectangle (10 to 20 s) 10 × 20 = 200, total 300 m. Treating it all as one rectangle gives 400, too big.", 400)],
    "guided_steps": [
        sayk("Distance is the area under the line. Split it into a triangle then a rectangle."),
        box("Triangle from 0 to 10 s: ½ × 10 × 20 = ", " m", 100, "½ × base × height."),
        box("Rectangle from 10 to 20 s: 10 × 20 = ", " m", 200, "base × height.", phase="substitute"),
        box("Total distance = 100 + 200 = ", " m", 300, "Add the two areas."),
        box("Check: average speed = 300 ÷ 20 = ", " m/s", 15, "Divide distance by total time to sanity-check.",
            done="15 m/s sits between 0 and 20, so 300 m is sensible.")
    ]
})

# S2 60km/h for 45min -> 45
silver.append({
    "display": "A car travels at 60 km/h for 45 minutes. How far does it go?",
    "solutions": [45], "calculator": False, "input_type": "single_value",
    "hint": "Turn 45 minutes into 0.75 hours first, then multiply.",
    "misconceptions": [mc("unit_error",
        "Convert 45 min to 0.75 h first, then 60 × 0.75 = 45 km. Using 45 as if it were hours gives 2700 km.", 2700)],
    "guided_steps": [
        sayk("The speed is in km/h, so the time must be in hours first."),
        box("Change 45 minutes to hours: 45 ÷ 60 = ", " h", 0.75, "There are 60 minutes in an hour."),
        box("Distance = speed × time = 60 × 0.75 = ", " km", 45, "Multiply the speed by the time in hours.", phase="substitute"),
        box("Check: 45 km ÷ 0.75 h = ", " km/h", 60, "Divide back to test it.",
            done="It returns the 60 km/h given, so 45 km is right.")
    ]
})

# S3 18km in 45min -> 24
silver.append({
    "display": "A cyclist travels 18 km in 45 minutes. What is the speed in km/h?",
    "solutions": [24], "calculator": False, "input_type": "single_value",
    "hint": "Turn 45 minutes into 0.75 hours, then divide distance by it.",
    "misconceptions": [mc("unit_error",
        "Change 45 min to 0.75 h, then 18 ÷ 0.75 = 24 km/h. Dividing by 45 gives 0.4, which is km per minute, not km/h.", 0.4)],
    "guided_steps": [
        sayk("For km/h the time must be in hours first."),
        box("Change 45 minutes to hours: 45 ÷ 60 = ", " h", 0.75, "There are 60 minutes in an hour."),
        box("Speed = distance ÷ time = 18 ÷ 0.75 = ", " km/h", 24, "Divide the distance by the time in hours.", phase="substitute"),
        box("Check: 24 km/h × 0.75 h = ", " km", 18, "Multiply back to test it.",
            done="It returns the 18 km given, so 24 km/h is right.")
    ]
})

# S4 decel 30->0 in 6s -> 5 (add chart)
s4chart = scatter([(0, 30), (6, 0)], 6, 1, "Time (s)", 30, 5, "Speed (m/s)", "#6366f1")
silver.append({
    "chart": s4chart,
    "display": "The speed-time graph shows a car that decelerates from 30 m/s to 0 in 6 seconds. What is the deceleration?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Deceleration is change in speed ÷ time; give it as a positive value.",
    "misconceptions": [mc("wrong_formula",
        "Deceleration = change in speed ÷ time = 30 ÷ 6 = 5 m/s². Dividing time by the speed change (0.2) is upside down.", 0.2)],
    "guided_steps": [
        sayk("Deceleration is the size of the gradient: how fast the speed drops."),
        box("Change in speed = 30 − 0 = ", " m/s", 30, "The speed falls from 30 to 0."),
        box("Divide by the time: 30 ÷ 6 = ", " m/s²", 5, "Share the drop over 6 seconds.", phase="substitute"),
        box("Check: losing 5 m/s each second for 6 s loses 5 × 6 = ", " m/s", 30, "Multiply back to test it.",
            done="That is the full 30 m/s, from 30 down to 0, so 5 m/s² is right.")
    ]
})

# S5 constant 15 for 8s -> 120 (add chart)
s5chart = scatter([(0, 15), (8, 15)], 8, 1, "Time (s)", 20, 5, "Speed (m/s)", "#6366f1")
silver.append({
    "chart": s5chart,
    "display": "The speed-time graph shows a constant speed of 15 m/s for 8 seconds. What distance is covered?",
    "solutions": [120], "calculator": False, "input_type": "single_value",
    "hint": "A flat speed-time line gives a rectangle: base × height.",
    "misconceptions": [mc("area_error",
        "The speed is constant, so the area is a rectangle: 8 × 15 = 120 m. Using ½ (as for a triangle) gives 60, which is wrong for a flat line.", 60)],
    "guided_steps": [
        sayk("The line is flat, so the area under it is a rectangle."),
        box("Write the height (speed): ", " m/s", 15, "The speed stays at 15 m/s."),
        box("Area = base × height = 8 × 15 = ", " m", 120, "Base is the 8 seconds.", phase="substitute"),
        box("Check: 120 m ÷ 8 s = ", " m/s", 15, "Divide back to test it.",
            done="It returns the constant 15 m/s, so 120 m is right.")
    ]
})

# S6 accel 0->24 in 8s via area -> 96 (add chart)
s6chart = scatter([(0, 0), (8, 24)], 8, 1, "Time (s)", 24, 4, "Speed (m/s)", "#6366f1")
silver.append({
    "chart": s6chart,
    "display": "The speed-time graph shows a car accelerating from 0 to 24 m/s in 8 seconds. Find the distance using the area under the graph.",
    "solutions": [96], "calculator": False, "input_type": "single_value",
    "hint": "The area of the triangle is ½ × base × height.",
    "misconceptions": [mc("area_error",
        "Area of the triangle = ½ × 8 × 24 = 96 m. Leaving out the ½ gives 192, the rectangle by mistake.", 192)],
    "guided_steps": [
        sayk("The line is a straight slope from 0, so the area under it is a triangle."),
        box("The base is 8 s and the height is ", " m/s", 24, "The height is the top speed reached."),
        box("Area = ½ × base × height = ½ × 8 × 24 = ", " m", 96, "Half of base times height.", phase="substitute"),
        box("Check: average speed = (0 + 24) ÷ 2 = 12 m/s, so 12 × 8 = ", " m", 96, "Average speed times time gives distance.",
            done="Both methods give 96 m, so the answer is right.")
    ]
})

pb["silver"] = silver

# ----- GOLD -----
gold = []

# G0 v-t 0->25 in10, 25 for20, ->0 in5 -> 687.5 (add chart, calculator true)
g0chart = scatter([(0, 0), (10, 25), (30, 25), (35, 0)], 35, 5, "Time (s)", 30, 5, "Speed (m/s)", "#dc2626")
gold.append({
    "chart": g0chart,
    "display": "The speed-time graph shows a car. It accelerates from 0 to 25 m/s in 10 s, then travels at 25 m/s for 20 s, then decelerates to 0 in 5 s. Find the total distance.",
    "solutions": [687.5], "calculator": True, "input_type": "single_value",
    "hint": "Split into triangle, rectangle, triangle and add the three areas.",
    "misconceptions": [mc("area_error",
        "Triangle + rectangle + triangle = ½(10)(25) + 20(25) + ½(5)(25) = 125 + 500 + 62.5 = 687.5 m. Forgetting the ½ on the sloped parts gives 875.", 875)],
    "guided_steps": [
        sayk("The shape is a trapezium: two sloped triangles either side of a rectangle."),
        box("Triangle while speeding up: ½ × 10 × 25 = ", " m", 125, "½ × base × height."),
        box("Rectangle at steady speed: 20 × 25 = ", " m", 500, "base × height for the 20 s at 25 m/s.", phase="substitute"),
        box("Triangle while slowing down: ½ × 5 × 25 = ", " m", 62.5, "½ × base × height."),
        box("Total distance = 125 + 500 + 62.5 = ", " m", 687.5, "Add the three areas."),
        box("Check: total time = 10 + 20 + 5 = ", " s", 35, "Add the three stage times.",
            done="687.5 m over 35 s averages about 19.6 m/s, between 0 and 25, so it is sensible.")
    ]
})

# G1 400m lap, 200 in 25s, 200 in 35s, avg speed -> 6.7 (calculator true)
gold.append({
    "display": "A runner completes a 400 m lap. The first 200 m takes 25 s, and the second 200 m takes 35 s. What is the average speed for the whole lap? Give your answer to 1 d.p.",
    "solutions": [6.7], "calculator": True, "input_type": "single_value",
    "hint": "Average speed = total distance ÷ total time, not the mean of the speeds.",
    "misconceptions": [mc("average_error",
        "Average speed = total distance ÷ total time = 400 ÷ 60 = 6.7 m/s. Averaging the two speeds (8 and about 5.7) gives about 6.9, which is wrong.", 6.9)],
    "guided_steps": [
        sayk("Average speed always uses the totals, never the mean of the two separate speeds."),
        box("Total distance = 200 + 200 = ", " m", 400, "The whole lap is 400 m."),
        box("Total time = 25 + 35 = ", " s", 60, "Add the two stage times.", phase="substitute"),
        box("Average speed = 400 ÷ 60 = ", " m/s", 6.7, "Divide total distance by total time, to 1 d.p."),
        box("Check: the mean of 8 and 5.7 would be about 6.9, but total ÷ total gives ", " m/s", 6.7, "Confirm the correct method's value.",
            done="Average speed is total distance over total time, so 6.7 m/s is right.")
    ]
})

# G2 accel rest->30 in 12s -> 2.5 (calculator false)
gold.append({
    "display": "A train accelerates uniformly from rest to 30 m/s in 12 seconds. Find the acceleration.",
    "solutions": [2.5], "calculator": False, "input_type": "single_value",
    "hint": "Acceleration = change in speed ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Acceleration = change in speed ÷ time = 30 ÷ 12 = 2.5 m/s². Dividing time by the speed change (0.4) is upside down.", 0.4)],
    "guided_steps": [
        sayk("Acceleration is change in speed ÷ time. From rest means the start speed is 0."),
        box("Change in speed = 30 − 0 = ", " m/s", 30, "The speed rises from 0 to 30."),
        box("Divide by the time: 30 ÷ 12 = ", " m/s²", 2.5, "Share the gain over 12 seconds.", phase="substitute"),
        box("Check: 2.5 m/s² for 12 s gives 2.5 × 12 = ", " m/s", 30, "Multiply back to test it.",
            done="It reaches the 30 m/s given, so 2.5 m/s² is right.")
    ]
})

# G3 trapezium 0->20 in4, 20 for6, ->0 in2 -> 180 (add chart, calculator false)
g3chart = scatter([(0, 0), (4, 20), (10, 20), (12, 0)], 12, 2, "Time (s)", 25, 5, "Speed (m/s)", "#dc2626")
gold.append({
    "chart": g3chart,
    "display": "The speed-time graph shows a trapezium: speed rises from 0 to 20 m/s in 4 s, stays at 20 m/s for 6 s, then drops to 0 in 2 s. Find the total distance.",
    "solutions": [180], "calculator": False, "input_type": "single_value",
    "hint": "Add the two triangle areas and the rectangle area.",
    "misconceptions": [mc("area_error",
        "½(4)(20) + 6(20) + ½(2)(20) = 40 + 120 + 20 = 180 m. Forgetting the ½ on the sloped parts gives 240.", 240)],
    "guided_steps": [
        sayk("The trapezium splits into two triangles and a rectangle."),
        box("Triangle while speeding up: ½ × 4 × 20 = ", " m", 40, "½ × base × height."),
        box("Rectangle at steady speed: 6 × 20 = ", " m", 120, "base × height for the 6 s at 20 m/s.", phase="substitute"),
        box("Triangle while slowing down: ½ × 2 × 20 = ", " m", 20, "½ × base × height."),
        box("Total distance = 40 + 120 + 20 = ", " m", 180, "Add the three areas."),
        box("Check: total time = 4 + 6 + 2 = ", " s", 12, "Add the stage times.",
            done="180 m over 12 s averages 15 m/s, between 0 and 20, so it is sensible.")
    ]
})

# G4 two cyclists 12 & 16 km/h, after 3h -> 12 (calculator false)
gold.append({
    "display": "Two cyclists start together. Cyclist A travels at 12 km/h. Cyclist B travels at 16 km/h. After 3 hours, how far apart are they?",
    "solutions": [12], "calculator": False, "input_type": "single_value",
    "hint": "Find each distance, then subtract, or use the speed difference × time.",
    "misconceptions": [mc("wrong_formula",
        "Gap = (16 − 12) × 3 = 12 km. Adding the two distances (36 + 48 = 84) answers a different question.", 84)],
    "guided_steps": [
        sayk("They travel the same way, so the gap is the difference in how far each goes."),
        box("How far cyclist A goes: 12 × 3 = ", " km", 36, "distance = speed × time."),
        box("How far cyclist B goes: 16 × 3 = ", " km", 48, "distance = speed × time.", phase="substitute"),
        box("Gap between them = 48 − 36 = ", " km", 12, "Subtract the smaller distance from the larger."),
        box("Check: the speed gap is 16 − 12 = 4 km/h, and over 3 h that is 4 × 3 = ", " km", 12, "The gap grows by the speed difference each hour.",
            done="Both methods give 12 km, so the answer is right.")
    ]
})

pb["gold"] = gold

# =====================================================================
# ASSEMBLE (preserve topic_links, related_videos, worked_examples)
# =====================================================================
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": pb,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
    "tier_guides": tier_guides,
    "guided": guided
}

json.dump(out, io.open("lesson_maths-aqa_graphs-L04.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written lesson_maths-aqa_graphs-L04.json")
