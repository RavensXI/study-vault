# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open('_live_graphs-L04.json', encoding='utf-8'))
pb = pd['problem_bank']

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s):
    return {"say": s}

# ---------- tier descriptions ----------
pb['bronze_description'] = "Read distance-time graphs and use speed = distance ÷ time with whole numbers."
pb['silver_description'] = "Find distance as the area under a speed-time graph, plus rests, conversions and acceleration."
pb['gold_description'] = "Combine several areas or stages, and find average speed and acceleration from a full journey."

# ================= GOLD =================
g = pb['gold']
g[0]['hint'] = "Split into a triangle plus a rectangle, work out each area, then add."
g[0]['misconceptions'] = [{
  "pattern": "area_confusion", "check": "common", "expect": 100,
  "message": "If you got 100 m you found only the rectangle (10 × 10) and missed the triangle for the speed-up: ½ × 5 × 10 = 25 m. Total = 125 m."}]
g[0]['guided_steps'] = [
  say("Distance is the area under a speed-time graph. Split it into a triangle for the speed-up and a rectangle for the steady part."),
  box("Triangle, 0 to 5 s (speed 0 to 10): ½ × 5 × 10 = ", 25, "Half of base × height.", post="m"),
  box("Rectangle, 5 to 15 s is 10 s at 10 m/s: 10 × 10 = ", 100, "Base × height. The base is 15 − 5 = 10 s.", post="m"),
  say("Add the two areas to get the total distance."),
  box("Total distance = 25 + 100 = ", 125, "Add the triangle and the rectangle.", post="m", phase="substitute"),
  box("Check with the trapezium: ½ × (top 10 + base 15) × 10 = ", 125, "½ × 25 × 10.", post="m", phase="substitute", done="It matches the triangle-plus-rectangle total, so 125 m is right."),
]
g[1]['hint'] = "Braking makes a triangle: area = ½ × base × height."
g[1]['misconceptions'] = [{
  "pattern": "area_confusion", "check": "common", "expect": 360,
  "message": "If you got 360 you used base × height (12 × 30) and forgot the ½ for a triangle. Area = ½ × 12 × 30 = 180 m."}]
g[1]['guided_steps'] = [
  say("Distance is the area under the graph. Slowing from 30 m/s to 0 makes a triangle."),
  box("Base of the triangle (the time) = ", 12, "The braking lasts 12 seconds.", post="s"),
  box("Height of the triangle (the start speed) = ", 30, "It starts at 30 m/s.", post="m/s"),
  say("Area of a triangle is ½ × base × height."),
  box("Distance = ½ × 12 × 30 = ", 180, "Half of 12 × 30.", post="m", phase="substitute"),
  box("Check: average speed while braking = 30 ÷ 2 = 15 m/s, and 15 × 12 = ", 180, "15 × 12.", post="m", phase="substitute", done="Both routes give 180 m, so it is right."),
]
g[2]['hint'] = "Average speed = total distance ÷ total time, and rests count in the time."
g[2]['misconceptions'] = [{
  "pattern": "wrong_formula", "check": "common", "expect": 40,
  "message": "If you got 40 you divided by the moving time (1.5 h) and ignored the rests. Rests still count: total time = 2.5 h, so 60 ÷ 2.5 = 24 km/h."}]
g[2]['guided_steps'] = [
  say("Average speed is the total distance divided by the total time, rests included."),
  box("Total distance (the final height on the graph) = ", 60, "Read the top of the line at the end.", post="km"),
  box("Total time (the far right of the time axis) = ", 2.5, "The graph ends at 2.5 hours.", post="hours"),
  say("Now divide, and keep the rest periods in the time."),
  box("Average speed = 60 ÷ 2.5 = ", 24, "60 shared over 2.5 hours.", post="km/h", phase="substitute"),
  box("Check: 24 km/h × 2.5 h = ", 60, "24 × 2.5.", post="km", phase="substitute", done="That returns the total distance, so 24 km/h is right."),
]
g[3]['hint'] = "Acceleration = change in speed ÷ time."
g[3]['misconceptions'] = [{
  "pattern": "gradient_meaning", "check": "common", "expect": 3.125,
  "message": "If you got 3.125 you used 25 ÷ 8 (final speed ÷ time). Use the change in speed: (25 − 5) ÷ 8 = 20 ÷ 8 = 2.5 m/s²."}]
g[3]['guided_steps'] = [
  say("Acceleration is the gradient of a speed-time graph: the change in speed divided by the time."),
  box("Change in speed = 25 − 5 = ", 20, "Final speed minus start speed.", post="m/s"),
  box("Time taken = ", 8, "It happens over 8 seconds.", post="s"),
  say("Divide the change in speed by the time."),
  box("Acceleration = 20 ÷ 8 = ", 2.5, "20 shared over 8 seconds.", post="m/s²", phase="substitute"),
  box("Check: after 8 s at 2.5 m/s² the speed rises by 2.5 × 8 = ", 20, "2.5 × 8.", post="m/s", phase="substitute", done="That is the change from 5 to 25, so 2.5 m/s² is right."),
]
g[4]['hint'] = "Three shapes (triangle, rectangle, triangle): find each area and add."
g[4]['misconceptions'] = [{
  "pattern": "area_confusion", "check": "common", "expect": 120,
  "message": "If you got 120 you found only the rectangle and missed the two triangles (40 m each) for speeding up and slowing down. Total = 40 + 120 + 40 = 200 m."}]
g[4]['guided_steps'] = [
  say("Three parts: speed up (triangle), hold (rectangle), slow down (triangle). Find each area."),
  box("Triangle 1, 0 to 4 s: ½ × 4 × 20 = ", 40, "Half of base × height.", post="m"),
  box("Rectangle, 4 to 10 s is 6 s at 20 m/s: 6 × 20 = ", 120, "Base × height. Base is 10 − 4 = 6 s.", post="m"),
  box("Triangle 2, 10 to 14 s: ½ × 4 × 20 = ", 40, "Half of base × height again.", post="m"),
  say("Add all three areas."),
  box("Total distance = 40 + 120 + 40 = ", 200, "Add the two triangles and the rectangle.", post="m", phase="substitute"),
  box("Check with the trapezium: ½ × (top 6 + base 14) × 20 = ", 200, "½ × 20 × 20.", post="m", phase="substitute", done="It matches the three-piece total, so 200 m is right."),
]

# ================= BRONZE =================
b = pb['bronze']
b[0]['hint'] = "Read the distance at 20 minutes, then divide by the time."
b[0]['misconceptions'] = [{
  "pattern": "wrong_formula", "check": "common", "expect": 4,
  "message": "It looks like you inverted the formula. Speed = distance ÷ time, not time ÷ distance. At 20 minutes the distance is 5 km, so speed = 5 ÷ 20 = 0.25 km/min."}]
b[0]['guided_steps'] = [
  say("Speed is distance ÷ time. Read both from the graph for the first 20 minutes."),
  box("Distance at 20 minutes (read up from 20) = ", 5, "Follow the line up at 20 minutes.", post="km"),
  box("Time = ", 20, "The first part lasts 20 minutes.", post="minutes"),
  say("Now divide distance by time."),
  box("Speed = 5 ÷ 20 = ", 0.25, "5 shared over 20 minutes.", post="km/min", phase="substitute"),
  box("Check: 0.25 km/min × 20 min = ", 5, "0.25 × 20.", post="km", phase="substitute", done="That is the 5 km on the graph, so 0.25 km/min is right."),
]
b[1]['hint'] = "A rest is the flat section: find where it starts and ends."
b[1]['misconceptions'] = [{
  "pattern": "wrong_reading", "check": "common", "expect": 10,
  "message": "A rest is a flat line. Here the distance stays at 4 km from 20 min to 35 min, so the rest is 35 − 20 = 15 minutes. If you got 10, you measured only part of the flat section."}]
b[1]['guided_steps'] = [
  say("A rest is a flat (horizontal) section: the distance does not change. Find where the line goes flat."),
  box("The flat part starts at ", 20, "The line first stops rising at 20 minutes.", post="minutes"),
  box("The flat part ends at ", 35, "The line starts rising again at 35 minutes.", post="minutes"),
  say("The rest lasts from the start of the flat part to its end."),
  box("Rest time = 35 − 20 = ", 15, "End time minus start time.", post="minutes", phase="substitute"),
  box("Check: 20 + 15 = ", 35, "20 + 15.", post="minutes", phase="substitute", done="That lands on 35 min where the line moves again, so 15 minutes is right."),
]
b[2]['hint'] = "Read the final height of the line at the end of the journey."
b[2]['misconceptions'] = [{
  "pattern": "wrong_reading", "check": "common", "expect": 5,
  "message": "Read the distance at the very end of the journey. At 30 minutes the line reaches 6 km. If you got 5, you read the value at 25 minutes instead of the end."}]
b[2]['guided_steps'] = [
  say("The total distance is the final height of the line. Read the graph at the end, not partway."),
  box("Distance at 25 minutes = ", 5, "Follow the line up at 25 minutes.", post="km"),
  box("Distance at 30 minutes, the very end = ", 6, "The line rises again to 6 by 30 minutes.", post="km"),
  say("The journey ends at 30 minutes, so use the final value, not the 25-minute one."),
  box("Total distance = ", 6, "The final value, 6 km.", post="km", phase="substitute"),
  box("Check: the line rose from 5 km at 25 min to 6 km at 30 min, a rise of 6 − 5 = ", 1, "6 − 5.", post="km", phase="substitute", done="The last section adds 1 km to reach 6 km, so 6 km is the total."),
]
b[3]['display'] = "A car travels 150 km at a constant speed of 50 km/h. How long does the journey take, in hours?"
b[3]['solutions'] = [3]
b[3]['hint'] = "Time = distance ÷ speed."
b[3]['misconceptions'] = [{
  "pattern": "formula_error", "check": "common", "expect": 7500,
  "message": "Time = distance ÷ speed = 150 ÷ 50 = 3 hours. If you got 7500 you multiplied 150 × 50 instead of dividing."}]
b[3]['guided_steps'] = [
  say("Time is distance ÷ speed. The car covers 150 km at 50 km/h."),
  box("Distance = ", 150, "The car travels 150 km.", post="km"),
  box("Speed = ", 50, "It moves at 50 km/h.", post="km/h"),
  say("Divide the distance by the speed."),
  box("Time = 150 ÷ 50 = ", 3, "How many 50s fit into 150?", post="hours", phase="substitute"),
  box("Check: 50 km/h × 3 h = ", 150, "50 × 3.", post="km", phase="substitute", done="That returns the 150 km, so 3 hours is right."),
]
b[4]['hint'] = "Average speed = distance ÷ time."
b[4]['misconceptions'] = [{
  "pattern": "formula_error", "check": "common", "expect": 80,
  "message": "Average speed = distance ÷ time = 20 ÷ 4 = 5 km/h. If you got 80 you multiplied instead of dividing."}]
b[4]['guided_steps'] = [
  say("Average speed is total distance ÷ total time."),
  box("Distance = ", 20, "The journey is 20 km.", post="km"),
  box("Time = ", 4, "It takes 4 hours.", post="hours"),
  say("Divide distance by time."),
  box("Average speed = 20 ÷ 4 = ", 5, "20 shared over 4 hours.", post="km/h", phase="substitute"),
  box("Check: 5 km/h × 4 h = ", 20, "5 × 4.", post="km", phase="substitute", done="That returns 20 km, so 5 km/h is right."),
]
b[5]['display'] = "A speed-time graph rises with a positive gradient, then becomes horizontal. During which section is the object accelerating?"
b[5]['options'] = ["The sloping section", "The horizontal section", "Both sections", "Neither section"]
b[5]['solutions'] = [0]
b[5]['hint'] = "Acceleration happens where the line slopes, not where it is flat."
b[5]['misconceptions'] = [{
  "pattern": "gradient_meaning", "check": "common", "expect": 1,
  "message": "The horizontal section is constant speed, so there is no acceleration there. Acceleration happens where the line slopes, because the speed is changing."}]
b[5].pop('guided_steps', None)
b[6]['hint'] = "Speed = distance ÷ time."
b[6]['misconceptions'] = [{
  "pattern": "formula_error", "check": "common", "expect": 360,
  "message": "Speed = distance ÷ time = 180 ÷ 2 = 90 km/h. If you got 360 you multiplied 180 × 2 instead of dividing."}]
b[6]['guided_steps'] = [
  say("Speed is distance ÷ time."),
  box("Distance = ", 180, "The train travels 180 km.", post="km"),
  box("Time = ", 2, "It takes 2 hours.", post="hours"),
  say("Divide distance by time."),
  box("Speed = 180 ÷ 2 = ", 90, "180 shared over 2 hours.", post="km/h", phase="substitute"),
  box("Check: 90 km/h × 2 h = ", 180, "90 × 2.", post="km", phase="substitute", done="That returns 180 km, so 90 km/h is right."),
]
b[7]['hint'] = "Distance = speed × time."
b[7]['misconceptions'] = [{
  "pattern": "formula_error", "check": "common", "expect": 4.8,
  "message": "Distance = speed × time = 12 × 2.5 = 30 km. If you got 4.8 you divided 12 ÷ 2.5 instead of multiplying."}]
b[7]['guided_steps'] = [
  say("Distance is speed × time."),
  box("Speed = ", 12, "The cyclist rides at 12 km/h.", post="km/h"),
  box("Time = ", 2.5, "For 2.5 hours.", post="hours"),
  say("Multiply speed by time."),
  box("Distance = 12 × 2.5 = ", 30, "12 for each hour, over 2.5 hours.", post="km", phase="substitute"),
  box("Check: 30 ÷ 2.5 = ", 12, "30 ÷ 2.5.", post="km/h", phase="substitute", done="That returns the 12 km/h speed, so 30 km is right."),
]

# ================= SILVER =================
s = pb['silver']
s[0]['hint'] = "Distance is the area: a triangle plus a rectangle, added together."
s[0]['misconceptions'] = [{
  "pattern": "wrong_formula", "check": "common", "expect": 600,
  "message": "If you got 600 you treated the whole thing as a 30 × 20 rectangle. The first 10 s is a triangle: ½ × 10 × 20 = 100 m, plus the rectangle 20 × 20 = 400 m, total 500 m."}]
s[0]['guided_steps'] = [
  say("Distance is the area under the speed-time graph. Split it into a triangle and a rectangle."),
  box("Triangle, 0 to 10 s (speed 0 to 20): ½ × 10 × 20 = ", 100, "Half of base × height.", post="m"),
  box("Rectangle, 10 to 30 s is 20 s at 20 m/s: 20 × 20 = ", 400, "Base × height. Base is 30 − 10 = 20 s.", post="m"),
  say("Add the two areas."),
  box("Total distance = 100 + 400 = ", 500, "Add the triangle and the rectangle.", post="m", phase="substitute"),
  box("Check with the trapezium: ½ × (top 20 + base 30) × 20 = ", 500, "½ × 50 × 20.", post="m", phase="substitute", done="It matches, so 500 m is right."),
]
s[1]['hint'] = "The acceleration phase is a triangle: area = ½ × base × height."
s[1]['misconceptions'] = [{
  "pattern": "area_confusion", "check": "common", "expect": 200,
  "message": "If you got 200 you used base × height (10 × 20) and forgot the ½ for a triangle. Area = ½ × 10 × 20 = 100 m."}]
s[1]['guided_steps'] = [
  say("During acceleration the graph is a triangle. The distance is its area."),
  box("Base of the triangle (the time) = ", 10, "The acceleration lasts 10 s.", post="s"),
  box("Height of the triangle (the top speed) = ", 20, "It reaches 20 m/s.", post="m/s"),
  say("Area of a triangle is ½ × base × height."),
  box("Distance = ½ × 10 × 20 = ", 100, "Half of 10 × 20.", post="m", phase="substitute"),
  box("Check: average speed = 20 ÷ 2 = 10 m/s, and 10 × 10 = ", 100, "10 × 10.", post="m", phase="substitute", done="Both routes give 100 m, so it is right."),
]
s[2]['hint'] = "Average speed = total distance ÷ total time, including the rest."
s[2]['misconceptions'] = [{
  "pattern": "forgot_rest", "check": "common", "expect": 50,
  "message": "If you got 50 you divided by 2 hours and forgot the 30-minute rest. Total time = 1 + 0.5 + 1 = 2.5 h, so 100 ÷ 2.5 = 40 km/h."}]
s[2]['guided_steps'] = [
  say("Average speed is total distance ÷ total time. Add the moving parts AND the rest."),
  box("Total distance = 60 + 40 = ", 100, "Add the two travelling distances.", post="km"),
  box("Total time = 1 + 0.5 + 1 = ", 2.5, "Include the 30-minute rest as 0.5 hours.", post="hours"),
  say("Now divide the total distance by the total time."),
  box("Average speed = 100 ÷ 2.5 = ", 40, "100 shared over 2.5 hours.", post="km/h", phase="substitute"),
  box("Check: 40 km/h × 2.5 h = ", 100, "40 × 2.5.", post="km", phase="substitute", done="That returns the 100 km total, so 40 km/h is right."),
]
s[3]['hint'] = "Acceleration = change in speed ÷ time."
s[3]['misconceptions'] = [{
  "pattern": "gradient_meaning", "check": "common", "expect": 30,
  "message": "If you got 30 you gave the final speed, not the acceleration. Acceleration = change in speed ÷ time = 30 ÷ 6 = 5 m/s²."}]
s[3]['guided_steps'] = [
  say("Acceleration is the gradient of a speed-time graph: change in speed ÷ time."),
  box("Change in speed = 30 − 0 = ", 30, "Final speed minus start speed.", post="m/s"),
  box("Time = ", 6, "It takes 6 seconds.", post="s"),
  say("Divide the change in speed by the time."),
  box("Acceleration = 30 ÷ 6 = ", 5, "30 shared over 6 seconds.", post="m/s²", phase="substitute"),
  box("Check: after 6 s at 5 m/s² the speed rises by 5 × 6 = ", 30, "5 × 6.", post="m/s", phase="substitute", done="That is the change from 0 to 30, so 5 m/s² is right."),
]
s[4]['display'] = "The conversion graph shows miles to kilometres. Use it to convert 30 miles to km."
s[4]['solutions'] = [48]
s[4]['hint'] = "Read up from the miles axis to the line, then across to km."
s[4]['misconceptions'] = [{
  "pattern": "wrong_reading", "check": "common", "expect": None,
  "message": "Go up from 30 on the miles axis to the line, then across to the km axis: 48 km."}]
s[4]['guided_steps'] = [
  say("A conversion graph turns one unit into another. Find how many km are in an easy number of miles, then scale up."),
  box("From the graph, 5 miles = ", 8, "Read up from 5 miles: the line is level with 8 km.", post="km"),
  say("So every 5 miles is 8 km, and 30 miles is several lots of 5 miles."),
  box("Number of 5-mile steps in 30 miles: 30 ÷ 5 = ", 6, "How many 5s in 30?"),
  say("Multiply the km per step by the number of steps."),
  box("30 miles = 6 × 8 = ", 48, "6 lots of 8 km.", post="km", phase="substitute"),
  box("Check on the graph: read up from 30 miles and across to ", 48, "Read straight off the graph at 30 miles.", post="km", phase="substitute", done="The line meets 48 km at 30 miles, so it is right."),
]
s[5]['hint'] = "Speed = distance ÷ time."
s[5]['misconceptions'] = [{
  "pattern": "formula_error", "check": "common", "expect": 1250,
  "message": "Speed = distance ÷ time = 100 ÷ 12.5 = 8 m/s. If you got 1250 you multiplied 100 × 12.5 instead of dividing."}]
s[5]['guided_steps'] = [
  say("Speed is distance ÷ time."),
  box("Distance = ", 100, "The runner covers 100 m.", post="m"),
  box("Time = ", 12.5, "It takes 12.5 seconds.", post="s"),
  say("Divide distance by time."),
  box("Speed = 100 ÷ 12.5 = ", 8, "How many 12.5s make 100?", post="m/s", phase="substitute"),
  box("Check: 8 m/s × 12.5 s = ", 100, "8 × 12.5.", post="m", phase="substitute", done="That returns 100 m, so 8 m/s is right."),
]
s[6]['hint'] = "A steeper gradient means faster movement."
s[6]['misconceptions'] = [{
  "pattern": "gradient_meaning", "check": "common", "expect": 0,
  "message": "Steeper gradient = higher speed. Section B (gradient 25) is faster than Section A (gradient 15)."}]
s[6].pop('guided_steps', None)

# ================= tier_guides =================
pd['tier_guides'] = {
  "bronze": {
    "title": "Bronze: Reading distance-time graphs",
    "steps": [
      "<strong>Speed = distance ÷ time.</strong> On a distance-time graph this is the steepness (gradient) of the line: read a distance off the up axis and the matching time off the across axis, then divide.",
      "A <strong>flat line</strong> means a rest: the distance is not changing, so the speed is 0. The rest lasts from where the line goes flat to where it starts rising again.",
      "The <strong>total distance</strong> is the highest value the line reaches, read at the very end of the journey."
    ],
    "example": {
      "question": "A distance-time graph shows a cyclist riding 8 km in 2 hours. Find the speed.",
      "steps": [
        {"label": "Read the graph", "content": "Distance = 8 km, time = 2 hours."},
        {"label": "Divide", "content": "Speed = 8 ÷ 2 = 4 km/h."},
        {"label": "Check", "content": "4 km/h × 2 h = 8 km, matching the graph."},
        {"label": "Answer", "content": "<strong>4 km/h</strong>", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "silver": {
    "title": "Silver: Area under a speed-time graph",
    "steps": [
      "On a <strong>speed-time graph the distance is the area</strong> under the line. Split the shape into a triangle (for speeding up or slowing down) and a rectangle (for constant speed), then add the areas.",
      "Triangle area = <strong>½ × base × height</strong>; rectangle area = <strong>base × height</strong>. The base is a time, the height is a speed.",
      "For <strong>acceleration</strong>, use the gradient: change in speed ÷ time. For a <strong>conversion graph</strong>, read up to the line then across to the other axis."
    ],
    "example": {
      "question": "A speed-time graph shows a car reaching 10 m/s in 4 s, then holding 10 m/s for 6 s. Find the distance.",
      "steps": [
        {"label": "Triangle", "content": "½ × 4 × 10 = 20 m."},
        {"label": "Rectangle", "content": "6 × 10 = 60 m."},
        {"label": "Check", "content": "Trapezium: ½ × (6 + 10) × 10 = 80 m, the same total."},
        {"label": "Answer", "content": "<strong>80 m</strong> (20 + 60)", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "gold": {
    "title": "Gold: Full journeys and average speed",
    "steps": [
      "A full speed-time journey has <strong>three areas</strong>: a triangle for speeding up, a rectangle for the steady middle, and a triangle for slowing down. Find each and add for the total distance.",
      "<strong>Average speed = total distance ÷ total time.</strong> On a distance-time graph, include every rest in the total time.",
      "<strong>Acceleration = change in speed ÷ time</strong>, the gradient of a speed-time line."
    ],
    "example": {
      "question": "A speed-time graph: 0 to 12 m/s in 3 s, hold 12 m/s for 5 s, slow to 0 in 2 s. Find the distance.",
      "steps": [
        {"label": "Three areas", "content": "½ × 3 × 12 = 18 m, then 5 × 12 = 60 m, then ½ × 2 × 12 = 12 m."},
        {"label": "Add", "content": "18 + 60 + 12 = 90 m."},
        {"label": "Check", "content": "Trapezium: ½ × (5 + 10) × 12 = 90 m."},
        {"label": "Answer", "content": "<strong>90 m</strong>", "isAnswer": True, "is_answer": True}
      ]
    }
  }
}

# ================= guided (opener + teach) =================
pd['guided'] = {
  "opener": {
    "steps": [
      say("Picture a real car journey you could read off a road-trip chart. No formulas, just common sense."),
      box("You drive 60 miles and it takes 2 hours. So each hour you cover ", 30, "Split 60 miles evenly across the 2 hours.", post="miles"),
      say("That ‘30 miles each hour’ is the car’s <strong>speed</strong>. You just did distance ÷ time, which on a distance-time graph is the steepness (gradient) of the line."),
      box("Now the car parks for lunch. While parked, how many miles does it cover each hour? ", 0, "It is not moving, so it covers no distance.", post="miles"),
      say("Zero miles each hour is a <strong>flat line</strong> on the graph: the car is resting. Speed is just distance ÷ time, and a steeper line means a faster journey. That is the whole idea behind real-life graphs.")
    ]
  },
  "teach": {
    "bronze": {
      "display": "A distance-time graph shows a hiker walking a steady 12 km in 3 hours, then stopping to rest.",
      "steps": [
        say("Read the numbers straight off the axes first."),
        box("Distance travelled = ", 12, "Read the height the line reaches.", post="km"),
        box("Time taken = ", 3, "Read across the bottom axis.", post="hours"),
        say("Speed is distance ÷ time, the steepness of the line."),
        box("Speed = 12 ÷ 3 = ", 4, "Share 12 km across 3 hours.", post="km/h"),
        say("Now the hiker rests. A rest is a flat line where the distance stops changing."),
        box("During the rest, speed = ", 0, "No distance is covered, so the speed is 0.", post="km/h", done="Gone. Flat line means resting, speed 0. That was the whole point.")
      ]
    },
    "silver": {
      "display": "A speed-time graph shows a car reaching 12 m/s in 4 s, then holding 12 m/s for 6 s. Find the distance.",
      "steps": [
        say("On a speed-time graph the distance is the AREA under the line. Split it into shapes."),
        box("Top speed reached = ", 12, "Read the highest point of the line.", post="m/s"),
        say("First 4 seconds: the speed rises from 0 to 12 m/s, a triangle."),
        box("Triangle area = ½ × 4 × 12 = ", 24, "Half of base × height.", post="m"),
        say("Next 6 seconds: the speed holds at 12 m/s, a rectangle."),
        box("Rectangle area = 6 × 12 = ", 72, "Base × height.", post="m"),
        say("Add the two areas for the total distance."),
        box("Total distance = 24 + 72 = ", 96, "Add the triangle and the rectangle.", post="m", done="Gone. Distance is the area: triangle plus rectangle.")
      ]
    },
    "gold": {
      "display": "A speed-time graph shows a train accelerating from 0 to 20 m/s in 4 s, holding 20 m/s for 10 s, then slowing to 0 in 6 s. Find the distance.",
      "steps": [
        say("A full journey has three parts: speed up, hold, slow down. Find each area, then add."),
        say("Part 1, 0 to 4 s: accelerate 0 to 20 m/s, a triangle."),
        box("Triangle 1 = ½ × 4 × 20 = ", 40, "Half of base × height.", post="m"),
        say("Part 2, 4 to 14 s: hold 20 m/s for 10 s, a rectangle."),
        box("Rectangle = 10 × 20 = ", 200, "Base × height.", post="m"),
        say("Part 3, 14 to 20 s: slow 20 to 0 in 6 s, another triangle."),
        box("Triangle 2 = ½ × 6 × 20 = ", 60, "Half of base × height again.", post="m"),
        say("Add all three areas."),
        box("Total distance = 40 + 200 + 60 = ", 300, "Add the two triangles and the rectangle.", post="m", done="Gone. Three shapes, three areas, add them up.")
      ]
    }
  }
}

# ================= method_card (slim) =================
mc = pd['method_card']
mc['title'] = "How to Interpret Real-Life Graphs"
mc['steps'] = [
  "Distance-time graph: gradient = speed; a flat line = a rest; use speed = distance ÷ time.",
  "Speed-time graph: the area under the line = distance; the gradient = acceleration.",
  "Split an area into a triangle (½ × base × height) plus a rectangle (base × height), then add.",
  "Conversion graph: read up to the line, then across to the other axis. Always give units."
]
mc['content'] = ("<p>Real-life graphs show how one quantity changes with another. On a <strong>distance-time</strong> "
  "graph the gradient is the speed, a flat line is a rest, and the total distance is the final height. "
  "Speed = distance ÷ time.</p><p>On a <strong>speed-time</strong> graph the area under the line is the distance "
  "travelled, and the gradient is the acceleration (change in speed ÷ time). Break the area into a triangle for any "
  "speeding up or slowing down and a rectangle for constant speed, then add them.</p><p>A <strong>conversion</strong> "
  "graph swaps units: read up to the line, then across. Always write the units in your answer.</p>")
mc['example'] = ("<p><strong>A car accelerates from 0 to 20 m/s in 5 s, then holds 20 m/s for 10 s. Find the distance.</strong></p>"
  "<p>Triangle: ½ × 5 × 20 = 50 m. Rectangle: 10 × 20 = 200 m. Total = <strong>250 m</strong>.</p>")

# ---- normalise em dashes in preserved worked_examples labels (style gate) ----
for we in pd.get('worked_examples', []):
    for st in we.get('steps', []):
        if isinstance(st.get('label'), str) and "—" in st['label']:
            st['label'] = st['label'].replace(" — ", ": ").replace("—", ":")

json.dump(pd, io.open('lesson_graphs-L04.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print("written lesson_graphs-L04.json")
b_sols=[p['solutions'] for p in pb['bronze']]
s_sols=[p['solutions'] for p in pb['silver']]
g_sols=[p['solutions'] for p in pb['gold']]
print("bronze", b_sols)
print("silver", s_sols)
print("gold", g_sols)
