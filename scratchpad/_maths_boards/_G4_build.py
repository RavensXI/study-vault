# -*- coding: utf-8 -*-
import json, io, sys
sys.path.insert(0, r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards")
from _G4_svglib import svg_line

LIVE = r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_G4_live.json"
live = json.load(io.open(LIVE, encoding="utf-8"))["practice_data"]

def chart(labels, data, xt, yt, color, xstep, ystep, beginZero=True):
    return {
        "type": "line",
        "data": {"labels": labels, "datasets": [{
            "data": data, "fill": False, "tension": 0,
            "borderColor": color, "pointRadius": 4,
            "pointBackgroundColor": color}]},
        "options": {"scales": {
            "x": {"grid": {"color": "rgba(0,0,0,0.05)"},
                  "ticks": {"stepSize": xstep},
                  "title": {"text": xt, "display": True}},
            "y": {"grid": {"color": "rgba(0,0,0,0.08)"},
                  "ticks": {"stepSize": ystep},
                  "title": {"text": yt, "display": True},
                  "beginAtZero": beginZero}}}}

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint, "post": post}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(s): return {"say": s}

# ---- shared bronze journey chart (FIXED: flat 20->30 only) ----
bronze_journey = chart([0,10,20,30,40,50,60], [0,3,6,6,8,10,12],
                       "Time (minutes)", "Distance (km)", "#3b82f6", 10, 3)

# ============ PROBLEM BANK ============
bronze = [
 # B0 read distance at 20 min
 {"chart": bronze_journey,
  "display": "The distance-time graph shows a journey. How far had the person travelled after 20 minutes?",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Go up from 20 minutes to the line, then across to the distance axis.",
  "misconceptions": [
    {"pattern": "axis_confusion", "expect": [20],
     "message": "Read up from 20 on the time axis to the line, THEN across to the distance axis. The distance is 6 km, not the time value 20.",
     "note": "reads the x-axis value as the distance"}],
  "guided_steps": [
    box("At 10 minutes, read up to the line then across. Distance (km) = ", 3, "Go up from 10, across to the distance axis."),
    say("Now the value the question asks for."),
    box("At 20 minutes, read up to the line then across. Distance (km) = ", 6, "20 is two gridlines along; the line sits at 6.", phase="substitute"),
    box("At 30 minutes the line is still level, so the distance has not changed. Distance (km) = ", 6, "The flat part means the same height.", done="The line sits at 6 km from 20 to 30 minutes, so 6 km is right.", phase="substitute")]},
 # B1 stationary minutes
 {"chart": bronze_journey,
  "display": "Using the same journey graph, for how many minutes was the person stationary?",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Find the flat part of the line, then work out how long it lasts.",
  "misconceptions": [
    {"pattern": "reads_distance_not_time", "expect": [6],
     "message": "The flat part is where the distance does not change. It runs from 20 to 30 minutes, so the stationary time is 30 − 20 = 10 minutes, not the distance 6 km.",
     "note": "gives the height of the flat part instead of its duration"}],
  "guided_steps": [
    box("The line first goes level at a time of (minutes) ", 20, "Where does the line stop climbing?"),
    say("It stays level until the line starts climbing again."),
    box("The line starts climbing again at (minutes) ", 30, "The next point where the height increases.", phase="substitute"),
    box("Stationary time = 30 − 20 = ", 10, "Subtract the start time from the end time.", done="10 minutes with no distance gained.", phase="substitute")]},
 # B2 car 60km 2h
 {"display": "A car travels 60 km in 2 hours at constant speed. What is its speed in km/h?",
  "solutions": [30], "calculator": False, "input_type": "single_value",
  "hint": "Speed = distance ÷ time.",
  "misconceptions": [
    {"pattern": "multiply_not_divide", "expect": [120],
     "message": "Speed = distance ÷ time, so 60 ÷ 2 = 30 km/h. Multiplying gives 120, which would be a distance, not a speed.",
     "note": "60 × 2 = 120"}],
  "guided_steps": [
    box("Read the distance travelled (km) = ", 60, "It is given in the question."),
    say("Speed = distance ÷ time."),
    box("60 ÷ 2 = ", 30, "Sixty shared into two.", phase="substitute"),
    box("Check: 30 × 2 = ", 60, "Multiply back to test it.", done="Matches the 60 km, so 30 km/h is right.", phase="substitute")]},
 # B3 conversion 10 miles
 {"chart": chart([0,5,10,15], [0,8,16,24], "Distance (miles)", "Distance (km)", "#3b82f6", 5, 8),
  "display": "A conversion graph shows that 5 miles = 8 km. How many km is 10 miles?",
  "solutions": [16], "calculator": False, "input_type": "single_value",
  "hint": "10 miles is double 5 miles, so double the number of km.",
  "misconceptions": [
    {"pattern": "additive_not_multiplicative", "expect": [13],
     "message": "10 miles is double 5 miles, so double the km: 8 × 2 = 16 km. Adding the extra 5 to 8 (giving 13) treats miles and km as the same size, which they are not.",
     "note": "8 + (10 − 5) = 13"}],
  "guided_steps": [
    box("One mile in km: 8 ÷ 5 = ", 1.6, "Share 8 km across 5 miles."),
    say("Now scale up to 10 miles."),
    box("10 × 1.6 = ", 16, "Ten lots of 1.6.", phase="substitute"),
    box("Or double 5 miles: 2 × 8 = ", 16, "10 miles is twice 5 miles.", done="Both routes give 16 km.", phase="substitute")]},
 # B4 MC horizontal line
 {"display": "On a distance-time graph, what does a horizontal line mean?",
  "options": ["Constant speed", "Stationary (not moving)", "Accelerating", "Moving backwards"],
  "solutions": [1], "calculator": False, "input_type": "multiple_choice",
  "hint": "A horizontal line means the distance is not changing.",
  "misconceptions": [
    {"pattern": "confuses_graph_type", "expect": [0],
     "message": "A horizontal line on a distance-time graph means the distance is not changing, so the object is stationary. Constant speed would be a straight sloping line.",
     "note": "picks constant speed"}]},
 # B5 walker km/min
 {"display": "A walker covers 4 km in 1 hour. What is their speed in km per minute? Give your answer to 3 decimal places.",
  "solutions": [0.067], "calculator": True, "input_type": "single_value",
  "hint": "There are 60 minutes in an hour, so divide the distance by 60.",
  "misconceptions": [
    {"pattern": "wrong_time_unit", "expect": [4],
     "message": "4 km in 1 hour is 4 km/h. Per minute, divide by 60: 4 ÷ 60 ≈ 0.067 km/min. Leaving it as 4 keeps the units as km per hour.",
     "note": "leaves answer in km/h"}],
  "guided_steps": [
    box("Minutes in one hour = ", 60, "How many minutes make an hour?"),
    say("Speed per minute = distance ÷ number of minutes."),
    box("4 ÷ 60 = (3 d.p.) ", 0.067, "Use the calculator, round to 3 decimal places.", phase="substitute"),
    box("Check: 0.067 × 60 ≈ ", 4, "Multiply back by 60 minutes.", done="About 4 km in an hour, matching the question.", phase="substitute")]},
 # B6 MC area under speed-time
 {"display": "On a speed-time graph, what does the area under the graph represent?",
  "options": ["Acceleration", "Distance travelled", "Speed", "Time taken"],
  "solutions": [1], "calculator": False, "input_type": "multiple_choice",
  "hint": "Think about speed × time, which is what an area multiplies together.",
  "misconceptions": [
    {"pattern": "area_vs_gradient", "expect": [0],
     "message": "The area under a speed-time graph is the distance travelled. Acceleration is the gradient (the steepness), not the area.",
     "note": "picks acceleration"}]},
 # B7 bus 40km/h 3h
 {"display": "A bus travels at a constant speed of 40 km/h for 3 hours. How far does it go?",
  "solutions": [120], "calculator": False, "input_type": "single_value",
  "hint": "Distance = speed × time.",
  "misconceptions": [
    {"pattern": "divide_not_multiply", "expect": [13.33],
     "message": "Distance = speed × time = 40 × 3 = 120 km. Dividing (40 ÷ 3) finds a speed, not a distance.",
     "note": "40 ÷ 3 = 13.33"}],
  "guided_steps": [
    box("The time travelled (hours) = ", 3, "Read it from the question."),
    say("Distance = speed × time."),
    box("40 × 3 = ", 120, "Three lots of 40.", phase="substitute"),
    box("Check: 120 ÷ 3 = ", 40, "Divide back by the time.", done="Back to 40 km/h, so 120 km is right.", phase="substitute")]},
]

silver = [
 # S0 chart accel first 10s
 {"chart": chart([0,5,10,15,20,25,30], [0,10,20,20,15,10,0], "Time (seconds)", "Speed (m/s)", "#dc2626", 5, 5),
  "display": "The speed-time graph shows a car's journey. What is the acceleration during the first 10 seconds?",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Acceleration = change in speed ÷ time.",
  "misconceptions": [
    {"pattern": "reads_final_speed", "expect": [20],
     "message": "Acceleration = change in speed ÷ time = (20 − 0) ÷ 10 = 2 m/s². Giving 20 is the speed reached, not the acceleration.",
     "note": "gives speed at 10 s"},
    {"pattern": "inverted_ratio", "expect": [0.5],
     "message": "Acceleration is change in speed ÷ time, not time ÷ speed. 10 ÷ 20 = 0.5 is upside down; the right way up is 20 ÷ 10 = 2.",
     "note": "10 ÷ 20"}],
  "guided_steps": [
    box("At 0 s the speed is 0. At 10 s the speed (m/s) = ", 20, "Read the line at 10 seconds."),
    say("Acceleration = change in speed ÷ time."),
    box("(20 − 0) ÷ 10 = ", 2, "Twenty divided by ten.", phase="substitute"),
    box("Check: 2 × 10 = ", 20, "Multiply back by the 10 seconds.", done="Speed rises by 20 in 10 s, matching the graph.", phase="substitute")]},
 # S1 cyclist 15km 30min
 {"chart": chart([0,10,20,30], [0,5,10,15], "Time (minutes)", "Distance (km)", "#dc2626", 10, 5),
  "display": "A distance-time graph shows a cyclist covering 15 km in 30 minutes. What is the speed in km/h?",
  "solutions": [30], "calculator": False, "input_type": "single_value",
  "hint": "Change 30 minutes into hours first, then divide.",
  "misconceptions": [
    {"pattern": "no_unit_conversion", "expect": [0.5],
     "message": "30 minutes is 0.5 hours. Speed = 15 ÷ 0.5 = 30 km/h. Dividing by 30 minutes instead gives 0.5, which mixes up the units.",
     "note": "15 ÷ 30"}],
  "guided_steps": [
    box("30 minutes as a fraction of an hour = ", 0.5, "30 out of 60 minutes."),
    say("Speed = distance ÷ time in hours."),
    box("15 ÷ 0.5 = ", 30, "Dividing by a half doubles it.", phase="substitute"),
    box("Check: 30 × 0.5 = ", 15, "Multiply back by half an hour.", done="15 km in half an hour, matching.", phase="substitute")]},
 # S2 constant 12 for 20s
 {"chart": chart([0,5,10,15,20], [12,12,12,12,12], "Time (seconds)", "Speed (m/s)", "#dc2626", 5, 3),
  "display": "A speed-time graph shows a constant speed of 12 m/s for 20 seconds. What is the distance?",
  "solutions": [240], "calculator": False, "input_type": "single_value",
  "hint": "Distance is the area, which for a rectangle is height × width.",
  "misconceptions": [
    {"pattern": "add_not_multiply", "expect": [32],
     "message": "Distance = area = speed × time = 12 × 20 = 240 m. Adding gives 32, but the area of a rectangle needs multiplying.",
     "note": "12 + 20"}],
  "guided_steps": [
    box("The rectangle's height (speed, m/s) = ", 12, "The constant speed."),
    say("Distance = area = height × width."),
    box("12 × 20 = ", 240, "Twelve lots of 20.", phase="substitute"),
    box("Check: 240 ÷ 20 = ", 12, "Divide back by the 20 seconds.", done="Back to 12 m/s, so 240 m is right.", phase="substitute")]},
 # S3 accel 0->30 in 6s
 {"chart": chart([0,2,4,6], [0,10,20,30], "Time (seconds)", "Speed (m/s)", "#dc2626", 2, 5),
  "display": "A speed-time graph shows a car accelerating from 0 to 30 m/s in 6 seconds. What is the acceleration?",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Acceleration = change in speed ÷ time.",
  "misconceptions": [
    {"pattern": "reads_final_speed", "expect": [30],
     "message": "Acceleration = (30 − 0) ÷ 6 = 5 m/s². The 30 is the speed reached, not how fast it built up.",
     "note": "gives final speed"}],
  "guided_steps": [
    box("Change in speed = 30 − 0 = ", 30, "Final minus starting speed."),
    say("Acceleration = change in speed ÷ time."),
    box("30 ÷ 6 = ", 5, "Thirty divided by six.", phase="substitute"),
    box("Check: 5 × 6 = ", 30, "Multiply back by the 6 seconds.", done="Speed gains 30 in 6 s, matching.", phase="substitute")]},
 # S4 MC steeper line
 {"display": "On a distance-time graph, a steeper line represents:",
  "options": ["Slower speed", "Faster speed", "Deceleration", "No change"],
  "solutions": [1], "calculator": False, "input_type": "multiple_choice",
  "hint": "A steeper line covers more distance in the same time.",
  "misconceptions": [
    {"pattern": "gradient_reversed", "expect": [0],
     "message": "A steeper line on a distance-time graph means more distance in the same time, so a faster speed. Slower speed is a shallower line.",
     "note": "picks slower"}]},
 # S5 decel 30->6 in 8s (REWRITTEN from 25->5 in 10s to avoid duplicate answer 2)
 {"chart": chart([0,2,4,6,8], [30,24,18,12,6], "Time (seconds)", "Speed (m/s)", "#dc2626", 2, 6),
  "display": "A speed-time graph shows a car decelerating from 30 m/s to 6 m/s in 8 seconds. What is the deceleration?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Deceleration = change in speed ÷ time; give it as a positive number.",
  "misconceptions": [
    {"pattern": "forgets_divide_time", "expect": [24],
     "message": "Deceleration = change in speed ÷ time = (30 − 6) ÷ 8 = 3 m/s². The 24 is just the drop in speed, before dividing by the time.",
     "note": "gives the speed change"}],
  "guided_steps": [
    box("Change in speed = 30 − 6 = ", 24, "Starting minus final speed."),
    say("Deceleration = change in speed ÷ time (given positive)."),
    box("24 ÷ 8 = ", 3, "Twenty-four divided by eight.", phase="substitute"),
    box("Check: 6 + 3 × 8 = ", 30, "Add the loss back over 8 seconds.", done="Slowing by 3 each second from 30 reaches 6, matching.", phase="substitute")]},
 # S6 inch conversion
 {"chart": chart([0,2,4,6,8,10], [0,5.08,10.16,15.24,20.32,25.4], "Length (inches)", "Length (cm)", "#dc2626", 2, 5),
  "display": "A conversion graph shows that 1 inch = 2.54 cm. How many cm is 8 inches?",
  "solutions": [20.32], "calculator": True, "input_type": "single_value",
  "hint": "Multiply the number of inches by 2.54.",
  "misconceptions": [
    {"pattern": "divide_wrong_way", "expect": [3.15],
     "message": "Each inch is 2.54 cm, so 8 inches = 8 × 2.54 = 20.32 cm. Dividing goes the wrong way, from cm back to inches.",
     "note": "8 ÷ 2.54 = 3.15"}],
  "guided_steps": [
    box("Centimetres in one inch = ", 2.54, "Read it from the question."),
    say("Multiply the number of inches by 2.54."),
    box("8 × 2.54 = ", 20.32, "Use the calculator.", phase="substitute"),
    box("Check: 20.32 ÷ 2.54 = ", 8, "Divide back to test it.", done="Back to 8 inches, so 20.32 cm is right.", phase="substitute")]},
]

gold = [
 # G0 chart total distance (four regions)
 {"chart": chart([0,4,8,12,16,20], [0,20,20,20,10,0], "Time (seconds)", "Speed (m/s)", "#7c3aed", 4, 5),
  "display": "Find the total distance travelled for the entire journey shown in the speed-time graph.",
  "solutions": [280], "calculator": False, "input_type": "single_value",
  "hint": "Split the area into a triangle, a rectangle, a trapezium and a triangle, then add.",
  "misconceptions": [
    {"pattern": "whole_rectangle", "expect": [400],
     "message": "The speed is not 20 for the whole journey. Split it into a triangle, a rectangle, a trapezium and a triangle: 40 + 160 + 60 + 20 = 280 m. Treating it as 20 × 20 gives 400.",
     "note": "20 × 20"},
    {"pattern": "forgets_slowdown", "expect": [200],
     "message": "The journey keeps going after 12 seconds. Add the slowing-down parts too: 40 + 160 + 60 + 20 = 280 m. Stopping at the rectangle gives only 200 m.",
     "note": "40 + 160 only"}],
  "guided_steps": [
    box("Region 1, triangle (0 to 4 s): ½ × 4 × 20 = ", 40, "Half base times height."),
    box("Region 2, rectangle (4 to 12 s): 8 × 20 = ", 160, "Width 8, height 20."),
    box("Region 3, trapezium (12 to 16 s): ½ × (20 + 10) × 4 = ", 60, "Half the two heights added, times the width."),
    say("One region left, then add them all."),
    box("Region 4, triangle (16 to 20 s): ½ × 4 × 10 = ", 20, "Half base times height.", phase="substitute"),
    box("Total = 40 + 160 + 60 + 20 = ", 280, "Add the four regions.", phase="substitute"),
    box("Time check: 4 + 8 + 4 + 4 = ", 20, "The regions should span the whole journey.", done="They cover the full 20 seconds, so 280 m is right.", phase="substitute")]},
 # G1 three-phase (REWORDED to remove en dashes, chart added)
 {"chart": chart([0,5,10,15,20], [0,15,15,15,0], "Time (seconds)", "Speed (m/s)", "#7c3aed", 5, 5),
  "display": "A speed-time graph shows a car speed up from 0 to 15 m/s over the first 5 seconds, hold 15 m/s until 15 seconds, then slow to 0 at 20 seconds. Find the total distance.",
  "solutions": [225], "calculator": False, "input_type": "single_value",
  "hint": "Split the area into a triangle, a rectangle and a triangle, then add.",
  "misconceptions": [
    {"pattern": "whole_rectangle", "expect": [300],
     "message": "The car is not at 15 m/s for the whole 20 seconds. Triangle + rectangle + triangle = 37.5 + 150 + 37.5 = 225 m. Using 15 × 20 gives 300.",
     "note": "15 × 20"},
    {"pattern": "rectangle_only", "expect": [150],
     "message": "The speeding-up and slowing-down parts still cover distance. Add both triangles: 37.5 + 150 + 37.5 = 225 m. The middle rectangle alone is only 150 m.",
     "note": "rectangle only"}],
  "guided_steps": [
    box("Triangle (0 to 5 s): ½ × 5 × 15 = ", 37.5, "Half base times height."),
    box("Rectangle (5 to 15 s): 10 × 15 = ", 150, "Width 10, height 15."),
    say("One triangle left, then total."),
    box("Triangle (15 to 20 s): ½ × 5 × 15 = ", 37.5, "Half base times height.", phase="substitute"),
    box("Total = 37.5 + 150 + 37.5 = ", 225, "Add the three regions.", phase="substitute"),
    box("Time check: 5 + 10 + 5 = ", 20, "The regions should span the whole journey.", done="They cover the full 20 seconds, so 225 m is right.", phase="substitute")]},
 # G2 runner first-20s speed
 {"display": "A distance-time graph shows a runner covering 400 m in 50 seconds. For the first 20 seconds they ran at constant speed, covering 200 m. What was their speed (m/s) in the first 20 seconds?",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Use only the first part: its distance divided by its time.",
  "misconceptions": [
    {"pattern": "uses_whole_run", "expect": [8],
     "message": "For the first part, use only its numbers: 200 m in 20 s gives 200 ÷ 20 = 10 m/s. Using the whole run, 400 ÷ 50 = 8 m/s, answers a different question.",
     "note": "400 ÷ 50"}],
  "guided_steps": [
    box("Distance in the first part (m) = ", 200, "The metres covered in the first 20 seconds."),
    say("Speed = distance ÷ time, using only the first part."),
    box("200 ÷ 20 = ", 10, "Two hundred over twenty.", phase="substitute"),
    box("Check: 10 × 20 = ", 200, "Multiply back by the 20 seconds.", done="10 m/s for 20 s covers 200 m, matching.", phase="substitute")]},
 # G3 accel 5->25 over 8s
 {"chart": chart([0,2,4,6,8], [5,10,15,20,25], "Time (seconds)", "Speed (m/s)", "#7c3aed", 2, 5),
  "display": "A speed-time graph shows constant acceleration from 5 m/s to 25 m/s over 8 seconds. What is the acceleration?",
  "solutions": [2.5], "calculator": False, "input_type": "single_value",
  "hint": "Use the change in speed, not the final speed, divided by the time.",
  "misconceptions": [
    {"pattern": "forgets_start_speed", "expect": [3.125],
     "message": "Use the change in speed: (25 − 5) ÷ 8 = 20 ÷ 8 = 2.5 m/s². Dividing 25 by 8 forgets that it started at 5 m/s.",
     "note": "25 ÷ 8"}],
  "guided_steps": [
    box("Change in speed = 25 − 5 = ", 20, "Final minus starting speed."),
    say("Acceleration = change in speed ÷ time."),
    box("20 ÷ 8 = ", 2.5, "Twenty over eight.", phase="substitute"),
    box("Check: 5 + 2.5 × 8 = ", 25, "Add the gain back over 8 seconds.", done="Starting at 5 and gaining 2.5 each second reaches 25, matching.", phase="substitute")]},
 # G4 triangle 0->30 over 12s
 {"chart": chart([0,3,6,9,12], [0,7.5,15,22.5,30], "Time (seconds)", "Speed (m/s)", "#7c3aed", 3, 5),
  "display": "A speed-time graph is a triangle: speed increases from 0 to 30 m/s over 12 seconds, then instantly drops to 0. What is the total distance?",
  "solutions": [180], "calculator": False, "input_type": "single_value",
  "hint": "Area of a triangle = ½ × base × height.",
  "misconceptions": [
    {"pattern": "forgets_half", "expect": [360],
     "message": "A triangle is half of the surrounding rectangle. Area = ½ × 12 × 30 = 180 m. Using 30 × 12 = 360 forgets the ½.",
     "note": "30 × 12"}],
  "guided_steps": [
    box("The surrounding rectangle: 12 × 30 = ", 360, "Width times height."),
    say("A triangle is half of that rectangle."),
    box("Area = ½ × 360 = ", 180, "Halve the rectangle.", phase="substitute"),
    box("Or directly: ½ × 12 × 30 = ", 180, "Half base times height.", done="Both routes give 180 m.", phase="substitute")]},
]

# ============ TIER GUIDES ============
tier_guides = {
 "bronze": {
  "title": "Bronze: read straight off the graph",
  "steps": [
    "On a distance-time graph the height is how far you have gone. Go up from the time axis to the line, then across to the distance axis to read a value.",
    "A flat, horizontal line means the distance is not changing, so the object is stationary. Measure the width of the flat part in time.",
    "Speed = distance ÷ time. Keep the units the axes use."],
  "example": {"question": "A car travels 90 km in 3 hours. Find its speed.",
    "steps": [
      {"label": "Formula", "content": "<p>Speed = distance ÷ time.</p>"},
      {"label": "Divide", "content": "<p>\\(90 \\div 3 = 30\\)</p>"},
      {"label": "Check", "content": "<p>\\(30 \\times 3 = 90\\) ✓</p>"},
      {"label": "Answer", "content": "<p><strong>30 km/h</strong></p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
  "title": "Silver: speed and acceleration as gradients",
  "steps": [
    "Speed is the gradient of a distance-time graph: change in distance ÷ change in time. Change minutes to hours first if the answer must be in km/h (30 min = 0.5 h).",
    "On a speed-time graph the gradient is the acceleration: change in speed ÷ time, in m/s².",
    "A downward gradient is deceleration; give it as a positive number."],
  "example": {"question": "A car speeds up from 0 to 24 m/s in 8 seconds. Find the acceleration.",
    "steps": [
      {"label": "Change in speed", "content": "<p>\\(24 - 0 = 24\\)</p>"},
      {"label": "Divide by time", "content": "<p>\\(24 \\div 8 = 3\\)</p>"},
      {"label": "Check", "content": "<p>\\(3 \\times 8 = 24\\) ✓</p>"},
      {"label": "Answer", "content": "<p><strong>3 m/s²</strong></p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
  "title": "Gold: area under a speed-time graph",
  "steps": [
    "The area under a speed-time graph is the distance travelled. Split the shape into triangles, rectangles and trapeziums.",
    "Triangle = ½ × base × height. Rectangle = base × height. Trapezium = ½ × (top + bottom) × width.",
    "Work out each region, then add them all for the total distance."],
  "example": {"question": "A speed-time graph rises from 0 to 20 m/s in 5 s, then holds 20 m/s for 10 s. Find the distance.",
    "steps": [
      {"label": "Triangle", "content": "<p>\\(\\tfrac12 \\times 5 \\times 20 = 50\\)</p>"},
      {"label": "Rectangle", "content": "<p>\\(10 \\times 20 = 200\\)</p>"},
      {"label": "Total", "content": "<p>\\(50 + 200 = 250\\)</p>"},
      {"label": "Answer", "content": "<p><strong>250 m</strong></p>", "isAnswer": True, "is_answer": True}]}},
}

# ============ GUIDED (opener + teach) ============
opener_svg = svg_line([(0,0),(15,6),(25,6),(40,0)], 40, 8,
                      "Time (minutes)", "Distance (km)", [0,10,20,30,40], [0,2,4,6,8],
                      "Distance-time graph of a cycle trip out to a friend's house and back")
teachB_svg = svg_line([(0,0),(10,4),(20,8),(30,8),(40,10),(50,12)], 50, 12,
                      "Time (minutes)", "Distance (km)", [0,10,20,30,40,50], [0,4,8,12],
                      "Distance-time graph of a journey with a stationary flat section")
teachS_svg = svg_line([(0,0),(8,20),(14,20)], 14, 20,
                      "Time (seconds)", "Speed (m/s)", [0,2,4,6,8,10,12,14], [0,5,10,15,20],
                      "Speed-time graph rising to 20 metres per second then holding")
teachG_svg = svg_line([(0,0),(4,12),(10,12),(14,0)], 14, 12,
                      "Time (seconds)", "Speed (m/s)", [0,2,4,6,8,10,12,14], [0,4,8,12],
                      "Speed-time graph forming a triangle, rectangle and triangle",
                      shade=True, shade_color="#34d399")

guided = {
 "opener": {
  "label": "Before any formulas",
  "display": opener_svg + "<br>You cycle to a friend's house and back. The graph shows how far you are from home.",
  "steps": [
    {"say": "No formulas, just read the picture. The height of the line is how far you are from home.",
     "pre": "How far away is your friend's house? (the highest point, in km) ", "post": "", "answer": 6,
     "hint": "Read the top of the graph across to the distance axis."},
    {"say": "The line goes flat while you are there, because your distance from home is not changing.",
     "pre": "For how many minutes did you stay? (length of the flat part) ", "post": "", "answer": 10,
     "hint": "The flat part runs from 15 to 25 minutes."},
    {"say": "You just read a distance-time graph with no algebra. Height above the axis is your distance from home, a flat line means you are not moving, and a line sloping back down means you are heading home. That is the whole skill in this lesson."}]},
 "teach": {
  "bronze": {
   "display": teachB_svg + "<br>The distance-time graph shows a journey. Read the values.",
   "label": "Together: reading the graph",
   "steps": [
     {"say": "Start with a straight read. Go up from the time axis to the line, then across.",
      "pre": "Distance after 10 minutes (km) = ", "post": "", "answer": 4, "hint": "Up from 10, across to the distance axis."},
     {"pre": "Distance after 20 minutes (km) = ", "post": "", "answer": 8, "hint": "Up from 20, across to the distance axis."},
     {"say": "The line is flat from 20 to 30 minutes, so the person is stationary there.",
      "pre": "Stationary time = 30 − 20 = ", "post": "", "answer": 10, "hint": "End time minus start time of the flat part."},
     {"pre": "Distance at the end, 50 minutes (km) = ", "post": "", "answer": 12, "hint": "Read the last point across to the distance axis."},
     {"pre": "Distance gained during the flat part (km) = ", "post": "", "answer": 0, "done": "A flat line adds no distance. That was the whole point.", "hint": "The height does not change while the line is flat."}]},
  "silver": {
   "display": teachS_svg + "<br>A speed-time graph shows a car speeding up then holding a steady speed.",
   "label": "Together: acceleration from the gradient",
   "steps": [
     {"say": "First read the speed the car reaches.",
      "pre": "Speed at 8 seconds (m/s) = ", "post": "", "answer": 20, "hint": "Read the line at 8 seconds."},
     {"say": "Acceleration is the gradient: change in speed ÷ time.",
      "pre": "Change in speed = 20 − 0 = ", "post": "", "answer": 20, "hint": "Final minus starting speed."},
     {"pre": "Acceleration = 20 ÷ 8 = ", "post": "", "answer": 2.5, "hint": "Twenty over eight."},
     {"say": "After 8 seconds the line is flat, so the speed is steady.",
      "pre": "Acceleration while the line is flat = ", "post": "", "answer": 0, "done": "A flat speed-time line means no acceleration. That was the whole point.", "hint": "No change in speed means no acceleration."}]},
  "gold": {
   "display": teachG_svg + "<br>A speed-time graph rises to 12 m/s, holds it, then falls back to 0. Find the distance as an area.",
   "label": "Together: distance as the area",
   "steps": [
     {"say": "The distance is the area under the line. Split it into a triangle, a rectangle and a triangle.",
      "pre": "Triangle (0 to 4 s): ½ × 4 × 12 = ", "post": "", "answer": 24, "hint": "Half base times height."},
     {"pre": "Rectangle (4 to 10 s): 6 × 12 = ", "post": "", "answer": 72, "hint": "Width 6, height 12."},
     {"pre": "Triangle (10 to 14 s): ½ × 4 × 12 = ", "post": "", "answer": 24, "hint": "Half base times height."},
     {"pre": "Total distance = 24 + 72 + 24 = ", "post": "", "answer": 120, "hint": "Add the three regions."},
     {"pre": "Time check: 4 + 6 + 4 = ", "post": "", "answer": 14, "done": "The regions span the full 14 seconds, so 120 m is right.", "hint": "The widths should add to the whole journey time."}]}}}

# ============ METHOD CARD (slim) ============
method_card = {
 "title": "How to Read Real-Life Graphs",
 "steps": [
   "Read a value: go up from one axis to the line, then across to the other axis.",
   "Distance-time: gradient = speed; a flat line = stationary.",
   "Speed-time: gradient = acceleration; area under the line = distance.",
   "Check which quantity each axis shows before writing your answer."],
 "content": "<p>Real-life graphs turn a story into a picture. On a <strong>distance-time</strong> graph the gradient is the <strong>speed</strong>, and a flat line means the object is <strong>stationary</strong>. On a <strong>speed-time</strong> graph the gradient is the <strong>acceleration</strong>, and the <strong>area under the line</strong> is the <strong>distance travelled</strong>. Split areas into triangles, rectangles and trapeziums, then add them. Conversion graphs are straight lines that swap one unit for another: read across, then up or down. Always keep the units each axis shows.</p>",
 "example": "<p><strong>A speed-time graph rises from 0 to 20 m/s in 5 s, then holds 20 m/s for 10 s.</strong></p><p>Triangle: ½ × 5 × 20 = 50 m. Rectangle: 10 × 20 = 200 m.</p><p>Total distance = <strong>250 m</strong>.</p>",
}

# worked_examples preserved, but strip pre-existing em dashes from labels (style law)
worked = live["worked_examples"]
for we in worked:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ============ ASSEMBLE (preserve untouched fields) ============
pd = {
 "method_card": method_card,
 "topic_links": live["topic_links"],
 "problem_bank": {
   "gold": gold, "bronze": bronze, "silver": silver,
   "gold_description": "Calculate areas under speed-time graphs and interpret acceleration",
   "bronze_description": "Read values from distance-time and conversion graphs",
   "silver_description": "Calculate speeds, interpret stationary periods, and read speed-time graphs",
 },
 "related_videos": live["related_videos"],
 "worked_examples": worked,
 "tier_guides": tier_guides,
 "guided": guided,
}

OUT = r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L04.json"
json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
print("svg sizes:", len(opener_svg), len(teachB_svg), len(teachS_svg), len(teachG_svg))
