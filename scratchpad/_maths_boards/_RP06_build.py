# -*- coding: utf-8 -*-
import json, math

live = json.load(open("_RP06_live.json", encoding="utf-8"))

# ---------- SVG generators (theme-safe: currentColor text/strokes, soft fills) ----------
def svg_dt():
    # distance-time straight line origin -> (4,80)
    ox, oy, rx, ty = 40, 135, 215, 20
    def X(x): return ox + x*((rx-ox)/4.0)
    def Y(y): return oy - y*((oy-ty)/80.0)
    x4, y80 = X(4), Y(80)
    return (
    '<svg viewBox="0 0 240 160" role="img" aria-label="Distance-time graph: a straight line from the origin to the point 4 hours, 80 km">'
    f'<line x1="{ox}" y1="{ty-2}" x2="{ox}" y2="{oy}" stroke="currentColor" stroke-width="1"/>'
    f'<line x1="{ox}" y1="{oy}" x2="{rx+5}" y2="{oy}" stroke="currentColor" stroke-width="1"/>'
    f'<line x1="{ox}" y1="{oy}" x2="{x4:.1f}" y2="{y80:.1f}" stroke="#3b82f6" stroke-width="2"/>'
    f'<circle cx="{x4:.1f}" cy="{y80:.1f}" r="3.5" fill="#3b82f6"/>'
    f'<text x="18" y="{y80+4:.0f}" font-family="Inter, sans-serif" font-size="11" fill="currentColor">80</text>'
    f'<text x="{x4-4:.0f}" y="{oy+15}" font-family="Inter, sans-serif" font-size="11" fill="currentColor">4</text>'
    f'<text x="10" y="16" font-family="Inter, sans-serif" font-size="10" fill="currentColor">km</text>'
    f'<text x="{rx-30}" y="{oy+15}" font-family="Inter, sans-serif" font-size="10" fill="currentColor">hours</text>'
    '</svg>')

def svg_st():
    # speed-time horizontal line at 12 m/s for 8 s (y scaled 0..16)
    ox, oy, rx, ty = 40, 135, 210, 20
    def X(t): return ox + t*((rx-ox)/8.0)
    def Y(v): return oy - v*((oy-ty)/16.0)
    yv = Y(12); x8 = X(8)
    return (
    '<svg viewBox="0 0 240 160" role="img" aria-label="Speed-time graph: a horizontal line at 12 metres per second from 0 to 8 seconds">'
    f'<line x1="{ox}" y1="{ty-2}" x2="{ox}" y2="{oy}" stroke="currentColor" stroke-width="1"/>'
    f'<line x1="{ox}" y1="{oy}" x2="{rx+5}" y2="{oy}" stroke="currentColor" stroke-width="1"/>'
    f'<line x1="{ox}" y1="{yv:.1f}" x2="{x8:.1f}" y2="{yv:.1f}" stroke="#3b82f6" stroke-width="2"/>'
    f'<line x1="{x8:.1f}" y1="{yv:.1f}" x2="{x8:.1f}" y2="{oy}" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3"/>'
    f'<circle cx="{ox}" cy="{yv:.1f}" r="3" fill="#3b82f6"/><circle cx="{x8:.1f}" cy="{yv:.1f}" r="3" fill="#3b82f6"/>'
    f'<text x="18" y="{yv+4:.0f}" font-family="Inter, sans-serif" font-size="11" fill="currentColor">12</text>'
    f'<text x="{x8-4:.0f}" y="{oy+15}" font-family="Inter, sans-serif" font-size="11" fill="currentColor">8</text>'
    f'<text x="6" y="16" font-family="Inter, sans-serif" font-size="10" fill="currentColor">m/s</text>'
    f'<text x="{rx-6}" y="{oy+15}" font-family="Inter, sans-serif" font-size="10" fill="currentColor">s</text>'
    '</svg>')

def svg_trap():
    # y = x^2 on 0..4, four trapezium strips width 1
    ox, oy, rx, ty = 45, 155, 225, 20
    def X(x): return ox + x*((rx-ox)/4.0)
    def Y(y): return oy - y*((oy-ty)/16.0)
    # smooth parabola
    pts = []
    xx = 0.0
    while xx <= 4.0001:
        pts.append(f"{X(xx):.1f},{Y(xx*xx):.1f}")
        xx += 0.25
    poly = " ".join(pts)
    parts = ['<svg viewBox="0 0 250 175" role="img" aria-label="Curve y equals x squared from x=0 to x=4 with four trapezium strips of width 1 and heights 0, 1, 4, 9, 16">']
    parts.append(f'<line x1="{ox}" y1="{ty-2}" x2="{ox}" y2="{oy}" stroke="currentColor" stroke-width="1"/>')
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{rx+8}" y2="{oy}" stroke="currentColor" stroke-width="1"/>')
    # shaded strips (trapezium tops as straight chords) + verticals
    heights = [0,1,4,9,16]
    for i in range(4):
        x0,x1 = i, i+1
        y0,y1 = heights[i], heights[i+1]
        p = f"{X(x0):.1f},{oy} {X(x0):.1f},{Y(y0):.1f} {X(x1):.1f},{Y(y1):.1f} {X(x1):.1f},{oy}"
        parts.append(f'<polygon points="{p}" fill="#60a5fa" fill-opacity="0.25" stroke="#3b82f6" stroke-width="0.8"/>')
    # true curve on top
    parts.append(f'<polyline points="{poly}" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    # x labels and height labels
    for i,x in enumerate([0,1,2,3,4]):
        parts.append(f'<text x="{X(x)-3:.0f}" y="{oy+14}" font-family="Inter, sans-serif" font-size="10" fill="currentColor">{x}</text>')
    for x,h in zip([0,1,2,3,4], heights):
        parts.append(f'<text x="{X(x)-4:.0f}" y="{Y(h)-4:.0f}" font-family="Inter, sans-serif" font-size="10" fill="currentColor">{h}</text>')
    parts.append(f'<text x="{rx-12}" y="{oy+14}" font-family="Inter, sans-serif" font-size="10" fill="currentColor">x</text>')
    parts.append('</svg>')
    return "".join(parts)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---------- BRONZE ----------
bronze = [
 {  # B1 distance-time speed (figure)
  "display": svg_dt() + "<p>A distance-time graph is a straight line from the origin to the point (4, 80), where distance is in km and time in hours. What is the speed?</p>",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Speed is the gradient: distance travelled divided by the time taken.",
  "guided_steps": [
    {"pre": "Distance travelled (the y-value at the end): ", "post": "", "answer": 80, "hint": "Read the height of the endpoint."},
    {"pre": "Time taken (the x-value at the end): ", "post": "", "answer": 4, "hint": "Read across to the endpoint."},
    {"pre": "Speed = distance ÷ time = 80 ÷ 4 = ", "post": "", "answer": 20, "hint": "80 shared into 4.", "say": "Speed is the steepness of the line.", "phase": "substitute"},
    {"pre": "Check: speed × time = 20 × 4 = ", "post": "", "answer": 80, "hint": "Multiply speed by time to get distance back.", "done": "That matches the 80 km travelled, so the speed is 20 km/h."}
  ],
  "misconceptions": [
    {"expect": 80, "message": "80 km is the total distance, not the speed. Speed = distance ÷ time = 80 ÷ 4 = 20 km/h.", "pattern": "read_distance", "note": "answered the distance"}
  ]
 },
 {  # B2 gradient two points
  "display": "A straight line passes through (1, 4) and (5, 20). Find its gradient.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Gradient = change in y divided by change in x (rise over run).",
  "guided_steps": [
    {"pre": "Rise (top y minus bottom y): 20 − 4 = ", "post": "", "answer": 16, "hint": "20 take away 4."},
    {"pre": "Run (right x minus left x): 5 − 1 = ", "post": "", "answer": 4, "hint": "5 take away 1."},
    {"pre": "Gradient = rise ÷ run = 16 ÷ 4 = ", "post": "", "answer": 4, "hint": "16 shared into 4.", "say": "Now put the two together.", "phase": "substitute"},
    {"pre": "Check: gradient × run = 4 × 4 = ", "post": "", "answer": 16, "hint": "Multiply gradient by run.", "done": "That matches the rise of 16, so the gradient is 4."}
  ],
  "misconceptions": [
    {"expect": 16, "message": "16 is the change in y only. Divide by the change in x, 5 − 1 = 4, to get 16 ÷ 4 = 4.", "pattern": "forgot_divide", "note": "gave rise, not gradient"}
  ]
 },
 {  # B3 iteration add 4, x2
  "display": "Use \\(x_{n+1} = x_n + 4\\) with \\(x_0 = 3\\). Find \\(x_2\\).",
  "solutions": [11], "calculator": False, "input_type": "single_value",
  "hint": "Add 4 each time: find x1 first, then x2.",
  "guided_steps": [
    {"pre": "x₁ = 3 + 4 = ", "post": "", "answer": 7, "hint": "Start value 3, add 4."},
    {"pre": "x₂ = 7 + 4 = ", "post": "", "answer": 11, "hint": "Feed x₁ back in, add 4.", "say": "Feed each answer back into the same rule.", "phase": "substitute"},
    {"pre": "Check: from the start, two jumps of 4 is 3 + 8 = ", "post": "", "answer": 11, "hint": "Two lots of 4 is 8, added to the start.", "done": "Same answer, so x₂ = 11."}
  ],
  "misconceptions": [
    {"expect": 7, "message": "7 is x₁. The question asks for x₂, so apply the rule once more: 7 + 4 = 11.", "pattern": "stopped_early", "note": "stopped at x1"}
  ]
 },
 {  # B4 iteration 2x-1, x1
  "display": "Use \\(x_{n+1} = 2x_n - 1\\) with \\(x_0 = 4\\). Find \\(x_1\\).",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Multiply the start value by 2 first, then subtract 1.",
  "guided_steps": [
    {"pre": "First multiply: 2 × 4 = ", "post": "", "answer": 8, "hint": "Double 4."},
    {"pre": "Then subtract 1: 8 − 1 = ", "post": "", "answer": 7, "hint": "Take 1 from the double.", "say": "The rule is: double, then take away 1.", "phase": "substitute"},
    {"pre": "Check: reverse it, (7 + 1) ÷ 2 = ", "post": "", "answer": 4, "hint": "Add 1, then halve.", "done": "That returns the start value 4, so x₁ = 7."}
  ],
  "misconceptions": [
    {"expect": 6, "message": "6 comes from 2 × (4 − 1). Multiply first, then subtract: 2 × 4 − 1 = 7.", "pattern": "wrong_order", "note": "subtracted before multiplying"}
  ]
 },
 {  # B5 speed-time horizontal, acceleration 0 (figure)
  "display": svg_st() + "<p>A speed-time graph shows a horizontal line at 12 m/s for 8 seconds. What is the acceleration?</p>",
  "solutions": [0], "calculator": False, "input_type": "single_value",
  "hint": "Acceleration is the gradient of a speed-time graph. A flat line has gradient 0.",
  "guided_steps": [
    {"pre": "The speed starts at 12 and ends at 12, so the change in speed is 12 − 12 = ", "post": "", "answer": 0, "hint": "The speed does not change."},
    {"pre": "The time taken is ", "post": " seconds", "answer": 8, "hint": "Read the end of the line."},
    {"pre": "Acceleration = change in speed ÷ time = 0 ÷ 8 = ", "post": "", "answer": 0, "hint": "Zero shared by anything is zero.", "say": "Acceleration is how fast the speed changes.", "phase": "substitute"},
    {"pre": "Check: acceleration × time = 0 × 8 = ", "post": "", "answer": 0, "hint": "That should equal the change in speed.", "done": "The change in speed was 0, so the acceleration is 0 m/s²."}
  ],
  "misconceptions": [
    {"expect": 1.5, "message": "1.5 comes from 12 ÷ 8, but the speed is constant. There is no change in speed, so the acceleration is 0.", "pattern": "divided_speed", "note": "divided the speed by time"}
  ]
 },
 {  # B6 iteration x^2-4, x1
  "display": "Use \\(x_{n+1} = x_n^2 - 4\\) with \\(x_0 = 3\\). Find \\(x_1\\).",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Square the start value first, then subtract 4.",
  "guided_steps": [
    {"pre": "Square the start value: 3² = ", "post": "", "answer": 9, "hint": "3 times 3."},
    {"pre": "Then subtract 4: 9 − 4 = ", "post": "", "answer": 5, "hint": "Take 4 from the square.", "say": "The rule is: square, then take away 4.", "phase": "substitute"},
    {"pre": "Check: 5 + 4 = ", "post": "", "answer": 9, "hint": "Add 4 back on.", "done": "That rebuilds 3² = 9, so x₁ = 5."}
  ],
  "misconceptions": [
    {"expect": 9, "message": "9 is just 3². You still need to subtract 4: 9 − 4 = 5.", "pattern": "forgot_subtract", "note": "stopped at the square"}
  ]
 },
 {  # B7 acceleration 48/6
  "display": "A car speeds up from 0 to 48 m/s in 6 seconds. What is the acceleration?",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Acceleration = change in speed ÷ time.",
  "guided_steps": [
    {"pre": "Change in speed: 48 − 0 = ", "post": "", "answer": 48, "hint": "Final speed minus start speed."},
    {"pre": "Time taken: ", "post": " seconds", "answer": 6, "hint": "Given in the question."},
    {"pre": "Acceleration = 48 ÷ 6 = ", "post": "", "answer": 8, "hint": "48 shared into 6.", "say": "Divide the change in speed by the time.", "phase": "substitute"},
    {"pre": "Check: 8 × 6 = ", "post": "", "answer": 48, "hint": "Multiply acceleration by time.", "done": "That matches the change in speed of 48, so the acceleration is 8 m/s²."}
  ],
  "misconceptions": [
    {"expect": 0.125, "message": "0.125 is 6 ÷ 48, the wrong way round. Acceleration = change in speed ÷ time = 48 ÷ 6 = 8.", "pattern": "inverted", "note": "divided time by speed"}
  ]
 },
 {  # B8 conceptual MC (kept)
  "display": "What does the gradient of a distance-time graph represent?",
  "options": ["Speed", "Acceleration", "Distance", "Time"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Gradient is how much the distance changes for each unit of time.",
  "misconceptions": [
    {"expect": None, "message": "Acceleration is the gradient of a speed-time graph. On a distance-time graph, the gradient is the speed.", "pattern": "confused_graphs"}
  ]
 },
]

# ---------- SILVER ----------
silver = [
 {  # S1 iteration 10/(x+1) x2
  "display": "Use \\(x_{n+1} = \\frac{10}{x_n + 1}\\) with \\(x_0 = 3\\). Find \\(x_2\\) to 2 d.p.",
  "solutions": [2.86], "calculator": True, "input_type": "single_value",
  "hint": "Add 1 to the term for the denominator, then divide 10 by it. Do it twice.",
  "guided_steps": [
    {"pre": "x₁: denominator 3 + 1 = 4, so 10 ÷ 4 = ", "post": "", "answer": 2.5, "hint": "Bottom is 3 + 1 = 4, then 10 ÷ 4."},
    {"pre": "x₂: denominator 2.5 + 1 = 3.5, so 10 ÷ 3.5 to 2 d.p. = ", "post": "", "answer": 2.86, "hint": "10 ÷ 3.5 = 2.857..., round to 2 d.p.", "say": "Feed x₁ back in for x₂.", "phase": "substitute"},
    {"pre": "Check: 2.86 × 3.5 = ", "post": "", "answer": 10.01, "hint": "Should come back to about 10.", "done": "≈ 10, so x₂ = 2.86 is right."}
  ],
  "misconceptions": [
    {"expect": 2.5, "message": "2.5 is x₁. One more step is needed: x₂ = 10 ÷ (2.5 + 1) = 2.86.", "pattern": "stopped_at_x1", "note": "stopped at x1"}
  ]
 },
 {  # S2 deceleration
  "display": "A car decelerates from 25 m/s to 5 m/s in 4 seconds. Find the deceleration.",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Deceleration = size of the change in speed divided by the time.",
  "guided_steps": [
    {"pre": "Change in speed (start minus end): 25 − 5 = ", "post": "", "answer": 20, "hint": "25 take away 5."},
    {"pre": "Deceleration = 20 ÷ 4 = ", "post": "", "answer": 5, "hint": "20 shared into 4.", "say": "Divide the change in speed by the time.", "phase": "substitute"},
    {"pre": "Check: 5 × 4 = ", "post": "", "answer": 20, "hint": "Multiply deceleration by time.", "done": "That matches the 20 m/s drop, so the deceleration is 5 m/s²."}
  ],
  "misconceptions": [
    {"expect": 20, "message": "20 is the total change in speed. Divide by the 4 seconds: 20 ÷ 4 = 5.", "pattern": "forgot_divide", "note": "gave the change, not the rate"}
  ]
 },
 {  # S3 iteration (x^2+5)/(2x) x1
  "display": "Use \\(x_{n+1} = \\frac{x_n^2 + 5}{2x_n}\\) with \\(x_0 = 3\\). Find \\(x_1\\) to 3 d.p.",
  "solutions": [2.333], "calculator": True, "input_type": "single_value",
  "hint": "Work out the numerator and denominator separately, then divide.",
  "guided_steps": [
    {"pre": "Numerator: 3² + 5 = ", "post": "", "answer": 14, "hint": "9 plus 5."},
    {"pre": "Denominator: 2 × 3 = ", "post": "", "answer": 6, "hint": "Double the term."},
    {"pre": "x₁ = 14 ÷ 6 to 3 d.p. = ", "post": "", "answer": 2.333, "hint": "14 ÷ 6 = 2.333...", "say": "Now divide the numerator by the denominator.", "phase": "substitute"},
    {"pre": "Check: 2.333 × 6 (to the nearest whole number) = ", "post": "", "answer": 14, "hint": "Multiply back by the denominator.", "done": "≈ 14, the numerator, so x₁ = 2.333."}
  ],
  "misconceptions": [
    {"expect": 4.667, "message": "4.667 divides by 3 instead of 2 × 3. The denominator is 2 × 3 = 6, so 14 ÷ 6 = 2.333.", "pattern": "wrong_denominator", "note": "used x not 2x"}
  ]
 },
 {  # S4 sign change f(2)
  "display": "\\(f(x) = x^3 - x - 5\\). Show that a root lies between \\(x = 1\\) and \\(x = 2\\). What is \\(f(2)\\)?",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "Work out f(1) and f(2); a sign change traps a root.",
  "guided_steps": [
    {"pre": "f(1) = 1³ − 1 − 5 = 1 − 1 − 5 = ", "post": "", "answer": -5, "hint": "1 − 1 − 5."},
    {"pre": "Now 2³ = ", "post": "", "answer": 8, "hint": "2 × 2 × 2."},
    {"pre": "f(2) = 8 − 2 − 5 = ", "post": "", "answer": 1, "hint": "8 − 2 − 5.", "say": "Now evaluate f at x = 2.", "phase": "substitute"},
    {"pre": "f(1) = −5 (negative) and f(2) is positive. The value asked for, f(2), is ", "post": "", "answer": 1, "hint": "Read off f(2) from the line above.", "done": "Sign change from − to +, so a root lies between x = 1 and x = 2."}
  ],
  "misconceptions": [
    {"expect": -1, "message": "−1 uses 2³ = 6. It is 2 × 2 × 2 = 8, so f(2) = 8 − 2 − 5 = 1.", "pattern": "cubed_wrong", "note": "treated 2^3 as 6"}
  ]
 },
 {  # S5 acceleration 12/3
  "display": "A car speeds up from 8 m/s to 20 m/s in 3 seconds. Find the acceleration.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Acceleration = change in speed divided by time.",
  "guided_steps": [
    {"pre": "Change in speed: 20 − 8 = ", "post": "", "answer": 12, "hint": "20 take away 8."},
    {"pre": "Acceleration = 12 ÷ 3 = ", "post": "", "answer": 4, "hint": "12 shared into 3.", "say": "Divide the change in speed by the time.", "phase": "substitute"},
    {"pre": "Check: 4 × 3 = ", "post": "", "answer": 12, "hint": "Multiply acceleration by time.", "done": "That matches the 12 m/s gain, so the acceleration is 4 m/s²."}
  ],
  "misconceptions": [
    {"expect": 12, "message": "12 is the change in speed. Divide by the 3 seconds: 12 ÷ 3 = 4.", "pattern": "forgot_divide", "note": "gave the change, not the rate"}
  ]
 },
 {  # S6 iteration sqrt(3x+1) x2
  "display": "Use \\(x_{n+1} = \\sqrt{3x_n + 1}\\) with \\(x_0 = 1\\). Find \\(x_2\\) to 2 d.p.",
  "solutions": [2.65], "calculator": True, "input_type": "single_value",
  "hint": "Work out the inside first, take the square root, then repeat.",
  "guided_steps": [
    {"pre": "First iteration, inside the root: 3 × 1 + 1 = ", "post": "", "answer": 4, "hint": "3 × 1 = 3, then + 1."},
    {"pre": "x₁ = √4 = ", "post": "", "answer": 2, "hint": "Square root of 4."},
    {"pre": "Second iteration, inside the root: 3 × 2 + 1 = ", "post": "", "answer": 7, "hint": "3 × 2 = 6, then + 1.", "say": "Feed x₁ back in for x₂.", "phase": "substitute"},
    {"pre": "x₂ = √7 to 2 d.p. = ", "post": "", "answer": 2.65, "hint": "Square root of 7 is 2.645..., round to 2 d.p.", "done": "x₂ ≈ 2.65, the sequence is settling."}
  ],
  "misconceptions": [
    {"expect": 2, "message": "2 is x₁. Apply the formula once more: x₂ = √(3 × 2 + 1) = √7 ≈ 2.65.", "pattern": "stopped_at_x1", "note": "stopped at x1"}
  ]
 },
 {  # S7 iteration sqrt(2x+3) x2
  "display": "Use \\(x_{n+1} = \\sqrt{2x_n + 3}\\) with \\(x_0 = 4\\). Find \\(x_2\\) to 3 d.p.",
  "solutions": [3.104], "calculator": True, "input_type": "single_value",
  "hint": "Keep the full value of x1, then use it to find x2.",
  "guided_steps": [
    {"pre": "First iteration, inside the root: 2 × 4 + 3 = ", "post": "", "answer": 11, "hint": "2 × 4 = 8, then + 3."},
    {"pre": "x₁ = √11 to 4 d.p. = ", "post": "", "answer": 3.3166, "hint": "Square root of 11. Keep 4 d.p."},
    {"pre": "Second iteration, inside the root: 2 × 3.3166 + 3 to 4 d.p. = ", "post": "", "answer": 9.6332, "hint": "2 × 3.3166 = 6.6332, then + 3.", "say": "Feed x₁ back in, keeping full precision.", "phase": "substitute"},
    {"pre": "x₂ = √9.6332 to 3 d.p. = ", "post": "", "answer": 3.104, "hint": "Square root of 9.6332.", "done": "x₂ ≈ 3.104, converging toward the root of x² = 2x + 3."}
  ],
  "misconceptions": [
    {"expect": 3.317, "message": "3.317 is x₁ (√11). One more step is needed: x₂ = √(2 × 3.3166 + 3) ≈ 3.104.", "pattern": "stopped_at_x1", "note": "stopped at x1"}
  ]
 },
]

# ---------- GOLD ----------
gold = [
 {  # G1 tangent gradient two points
  "display": "A tangent to a curve at \\(x = 2\\) passes through the points (0, 1) and (4, 13). Find the rate of change at \\(x = 2\\).",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "The rate of change is the gradient of the tangent: rise ÷ run.",
  "guided_steps": [
    {"pre": "Rise (top y minus bottom y): 13 − 1 = ", "post": "", "answer": 12, "hint": "13 take away 1."},
    {"pre": "Run (right x minus left x): 4 − 0 = ", "post": "", "answer": 4, "hint": "4 take away 0."},
    {"pre": "Rate of change = rise ÷ run = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "12 shared into 4.", "say": "The rate of change is the gradient of the tangent.", "phase": "substitute"},
    {"pre": "Check: 3 × 4 = ", "post": "", "answer": 12, "hint": "Multiply gradient by run.", "done": "That matches the rise of 12, so the rate of change is 3."}
  ],
  "misconceptions": [
    {"expect": 0.333, "message": "0.333 is run ÷ rise, upside down. Rate of change = rise ÷ run = 12 ÷ 4 = 3.", "pattern": "inverted_gradient", "note": "divided run by rise"}
  ]
 },
 {  # G2 Newton-Raphson x2
  "display": "Use \\(x_{n+1} = \\frac{2x_n^3 + 5}{3x_n^2}\\) with \\(x_0 = 2\\). Find \\(x_2\\) to 3 d.p.",
  "solutions": [1.711], "calculator": True, "input_type": "single_value",
  "hint": "Work the numerator and denominator separately, then divide. Repeat to x2.",
  "guided_steps": [
    {"pre": "x₁ numerator: 2 × 2³ + 5 = 2 × 8 + 5 = ", "post": "", "answer": 21, "hint": "2³ = 8, doubled is 16, plus 5."},
    {"pre": "x₁ denominator: 3 × 2² = 3 × 4 = ", "post": "", "answer": 12, "hint": "2² = 4, times 3."},
    {"pre": "x₁ = 21 ÷ 12 = ", "post": "", "answer": 1.75, "hint": "21 ÷ 12 = 1.75.", "say": "Now feed x₁ back into the same formula for x₂.", "phase": "substitute"},
    {"pre": "x₂ = (2 × 1.75³ + 5) ÷ (3 × 1.75²) to 3 d.p. = ", "post": "", "answer": 1.711, "hint": "Numerator ≈ 15.719, denominator ≈ 9.188."},
    {"pre": "Check: 1.711³ to the nearest whole number = ", "post": "", "answer": 5, "hint": "1.711 × 1.711 × 1.711.", "done": "≈ 5, so x₂ solves x³ = 5. The answer is 1.711."}
  ],
  "misconceptions": [
    {"expect": 1.75, "message": "1.75 is x₁, only one substitution. x₂ needs the formula applied again, feeding x₁ back in: 1.711.", "pattern": "single_substitution", "note": "stopped at x1"},
    {"expect": 1.119, "message": "1.119 drops the 2 in the numerator. The top is 2x³ + 5, not x³ + 5; redo each step with the full formula.", "pattern": "missing_coefficient", "note": "used x^3+5"}
  ]
 },
 {  # G3 applied rate (population)
  "display": "The population \\(P\\) of a town is modelled by \\(P = 2000 \\times 1.05^t\\), where \\(t\\) is in years. Find the average rate of change between \\(t = 0\\) and \\(t = 10\\), to the nearest whole number.",
  "solutions": [126], "calculator": True, "input_type": "single_value",
  "hint": "Find P at both times, subtract, then divide by the 10 years.",
  "guided_steps": [
    {"pre": "P(0) = 2000 × 1.05⁰ = ", "post": "", "answer": 2000, "hint": "Anything to the power 0 is 1."},
    {"pre": "P(10) = 2000 × 1.05¹⁰, to the nearest whole number = ", "post": "", "answer": 3258, "hint": "1.05 to the power 10, times 2000."},
    {"pre": "Change in P = 3258 − 2000 = ", "post": "", "answer": 1258, "hint": "Subtract the two populations.", "say": "The average rate of change is the total change over the time.", "phase": "substitute"},
    {"pre": "Rate = 1258 ÷ 10 = 125.8, to the nearest whole number = ", "post": "", "answer": 126, "hint": "Divide by the 10 years, then round.", "done": "The population grows by about 126 people per year on average."}
  ],
  "misconceptions": [
    {"expect": 1258, "message": "1258 is the total change over 10 years. Divide by 10 for the rate: 1258 ÷ 10 ≈ 126.", "pattern": "forgot_divide", "note": "gave total change"}
  ]
 },
 {  # G4 trapezium rule (figure)
  "display": svg_trap() + "<p>Use the trapezium rule with 4 strips (each of width 1) to estimate the area under \\(y = x^2\\) from \\(x = 0\\) to \\(x = 4\\). The heights are 0, 1, 4, 9 and 16.</p>" + CAP,
  "solutions": [22], "calculator": False, "input_type": "single_value",
  "hint": "Use ½ × width × (first height + last height + 2 × the middle heights).",
  "guided_steps": [
    {"pre": "Height at x = 2: 2² = ", "post": "", "answer": 4, "hint": "2 squared."},
    {"pre": "Height at x = 3: 3² = ", "post": "", "answer": 9, "hint": "3 squared."},
    {"pre": "Add the two end heights: 0 + 16 = ", "post": "", "answer": 16, "hint": "First height plus last height."},
    {"pre": "Double the middle heights: 2 × (1 + 4 + 9) = ", "post": "", "answer": 28, "hint": "1 + 4 + 9 = 14, then × 2.", "say": "Now apply the trapezium rule.", "phase": "substitute"},
    {"pre": "Area = ½ × 1 × (16 + 28) = ", "post": "", "answer": 22, "hint": "16 + 28 = 44, then halve.", "done": "The trapezium-rule estimate is 22 square units."}
  ],
  "misconceptions": [
    {"expect": 15, "message": "15 forgets to double the middle heights. Area ≈ ½ × [(0 + 16) + 2 × (1 + 4 + 9)] = ½ × 44 = 22.", "pattern": "forgot_double_middles", "note": "did not double middles"}
  ]
 },
 {  # G5 convergence form equation
  "display": "An iteration converges to the solution of \\(x = \\sqrt{2x + 15}\\). Find the positive value it converges to.",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Square both sides, rearrange to a quadratic, factorise, take the positive root.",
  "guided_steps": [
    {"say": "When the iteration settles, x stops changing, so \\(x = \\sqrt{2x + 15}\\). Square both sides: \\(x^2 = 2x + 15\\), which rearranges to \\(x^2 - 2x - 15 = 0\\)."},
    {"pre": "Two numbers that multiply to −15 and add to −2: one is −5, the other is ", "post": "", "answer": 3, "hint": "−5 × 3 = −15 and −5 + 3 = −2."},
    {"pre": "So (x − 5)(x + 3) = 0. The negative root is x = ", "post": "", "answer": -3, "hint": "x + 3 = 0 gives x = −3.", "say": "Set each bracket to zero to find the roots.", "phase": "substitute"},
    {"pre": "The question wants the positive value, so x = ", "post": "", "answer": 5, "hint": "5 is positive, −3 is not."},
    {"pre": "Check: 2 × 5 + 15 = ", "post": "", "answer": 25, "hint": "2 × 5 = 10, plus 15.", "done": "√25 = 5 = x, so it balances and the value is 5."}
  ],
  "misconceptions": [
    {"expect": -3, "message": "−3 is the other root. The question asks for the positive value, which is 5.", "pattern": "wrong_root_sign", "note": "gave negative root"}
  ]
 },
]

problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Find a rate of change from a straight-line graph or two points, and take the first steps of a simple iteration.",
  "silver_description": "Iterate to x2 with a calculator, calculate acceleration or deceleration, and test an interval for a sign change.",
  "gold_description": "Tangent gradients, Newton-Raphson iteration, the trapezium rule, convergence and real-life rates of change.",
}

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: rates of change and first iteration steps",
  "steps": [
    "<strong>Rate of change</strong> = gradient of the line: (change in y) ÷ (change in x), or rise ÷ run.",
    "<strong>Iteration</strong>: start at \\(x_0\\), put it into the formula for \\(x_1\\), then feed \\(x_1\\) back in for \\(x_2\\).",
    "Work one step at a time and write each term down. Watch the sign whenever a value is negative."
  ],
  "example": {
    "question": "A line passes through (1, 3) and (5, 15). Find the gradient.",
    "steps": [
      {"label": "Rise", "content": "15 − 3 = 12"},
      {"label": "Run", "content": "5 − 1 = 4"},
      {"label": "Check", "content": "4 × 3 = 12, matching the rise"},
      {"label": "Answer", "content": "Gradient = 12 ÷ 4 = 3", "isAnswer": True, "is_answer": True}
    ]
  }
 },
 "silver": {
  "title": "Silver: calculator iteration, acceleration and sign changes",
  "steps": [
    "Keep the <strong>full calculator value</strong> for each term. Round only the final term, to the decimal places asked for.",
    "For \\(x_2\\), apply the formula twice: each answer becomes the next input.",
    "On a speed-time graph the gradient is an <strong>acceleration</strong>. A <strong>sign change</strong> in \\(f(x)\\) traps a root."
  ],
  "example": {
    "question": "Use \\(x_{n+1} = \\sqrt{4x_n + 5}\\) with \\(x_0 = 1\\). Find \\(x_2\\) to 2 d.p.",
    "steps": [
      {"label": "x₁", "content": "√(4 × 1 + 5) = √9 = 3"},
      {"label": "Inside for x₂", "content": "4 × 3 + 5 = 17"},
      {"label": "Check", "content": "√17 sits between √16 = 4 and √25 = 5"},
      {"label": "Answer", "content": "\\(x_2 = \\sqrt{17} = 4.12\\) (2 d.p.)", "isAnswer": True, "is_answer": True}
    ]
  }
 },
 "gold": {
  "title": "Gold: Newton-Raphson, trapezium rule and real rates",
  "steps": [
    "A <strong>Newton-Raphson</strong> formula is a fraction such as \\(\\frac{2x_n^3 + a}{3x_n^2}\\): work numerator and denominator separately, then divide.",
    "<strong>Trapezium rule</strong>: ½ × strip width × (first height + last height + 2 × the middle heights).",
    "For a real-life model, the average rate of change is (change in output) ÷ (change in input) between the two given values."
  ],
  "example": {
    "question": "Use \\(x_{n+1} = \\frac{2x_n^3 + 7}{3x_n^2}\\) with \\(x_0 = 2\\). Find \\(x_1\\) to 3 d.p.",
    "steps": [
      {"label": "Numerator", "content": "2 × 2³ + 7 = 16 + 7 = 23"},
      {"label": "Denominator", "content": "3 × 2² = 12"},
      {"label": "Check", "content": "23 ÷ 12 ≈ 1.92, close to ∛7 ≈ 1.91"},
      {"label": "Answer", "content": "\\(x_1 = 23 \\div 12 = 1.917\\) (3 d.p.)", "isAnswer": True, "is_answer": True}
    ]
  }
 }
}

# ---------- guided (opener + teach) ----------
guided = {
 "opener": {
   "steps": [
     {"say": "A fish tank holds 200 litres. Each day you drain half the water, then top it up with 60 litres of fresh water. No algebra, just do the two sums."},
     {"pre": "After day 1 the tank holds ", "post": " litres", "answer": 160, "hint": "Halve 200 to get 100, then add the 60 litres."},
     {"say": "Now take that new amount, 160 litres, through the <strong>same</strong> rule again."},
     {"pre": "After day 2 the tank holds ", "post": " litres", "answer": 140, "hint": "Halve 160 to get 80, then add 60."},
     {"say": "Each new amount was the old one put through one rule: halve, then add 60. Feeding an answer back into the same rule, over and over, is called <strong>iteration</strong>. In algebra we write the rule as \\(x_{n+1} = \\frac{x_n}{2} + 60\\), with \\(x_0 = 200\\) the starting amount (the levels settle toward 120 litres). The other half of this lesson reads a <strong>rate of change</strong> straight off a graph: the steepness, or gradient, of the line, rise ÷ run."}
   ]
 },
 "teach": {
   "bronze": {
     "display": "A tangent to a curve passes through (1, 3) and (5, 15). Find the rate of change.",
     "steps": [
       {"say": "Rate of change is the steepness of the line: how much y climbs for the x you move across. It is rise ÷ run."},
       {"pre": "Rise (top y minus bottom y): 15 − 3 = ", "post": "", "answer": 12, "hint": "15 take away 3."},
       {"pre": "Run (right x minus left x): 5 − 1 = ", "post": "", "answer": 4, "hint": "5 take away 1."},
       {"pre": "Rate of change = rise ÷ run = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "12 shared into 4."},
       {"pre": "Check: a gradient of 3 over a run of 4 climbs 3 × 4 = ", "post": "", "answer": 12, "hint": "Multiply gradient by run.", "done": "That matches the rise of 12. Gone. That was the whole point: rise over run."}
     ]
   },
   "silver": {
     "display": "Use \\(x_{n+1} = \\frac{12}{x_n + 2}\\) with \\(x_0 = 2\\). Find \\(x_2\\).",
     "steps": [
       {"say": "The new move here: iterate with a calculator, keeping full precision, feeding each answer back in."},
       {"pre": "x₁ denominator: 2 + 2 = ", "post": "", "answer": 4, "hint": "Add 2 to the start value."},
       {"pre": "x₁ = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "12 shared into 4."},
       {"pre": "x₂ denominator: 3 + 2 = ", "post": "", "answer": 5, "hint": "Add 2 to x₁."},
       {"pre": "x₂ = 12 ÷ 5 = ", "post": "", "answer": 2.4, "hint": "12 ÷ 5 = 2.4."},
       {"pre": "Check: 2.4 × 5 = ", "post": "", "answer": 12, "hint": "Should come back to 12.", "done": "= 12, so x₂ = 2.4. That was the whole point: feed each answer back in."}
     ]
   },
   "gold": {
     "display": "Use \\(x_{n+1} = \\frac{2x_n^3 + 20}{3x_n^2}\\) with \\(x_0 = 3\\). Find \\(x_2\\) to 3 d.p.",
     "steps": [
       {"say": "The new move: a Newton-Raphson formula. Work the numerator and denominator separately, then divide, and repeat."},
       {"pre": "x₁ numerator: 2 × 3³ + 20 = 2 × 27 + 20 = ", "post": "", "answer": 74, "hint": "3³ = 27, doubled is 54, plus 20."},
       {"pre": "x₁ denominator: 3 × 3² = 3 × 9 = ", "post": "", "answer": 27, "hint": "3² = 9, times 3."},
       {"pre": "x₁ = 74 ÷ 27 to 4 d.p. = ", "post": "", "answer": 2.7407, "hint": "74 ÷ 27 = 2.7407..."},
       {"pre": "x₂ = (2 × 2.7407³ + 20) ÷ (3 × 2.7407²) to 3 d.p. = ", "post": "", "answer": 2.715, "hint": "Numerator ≈ 61.18, denominator ≈ 22.53."},
       {"pre": "Check: 2.715³ to the nearest whole number = ", "post": "", "answer": 20, "hint": "2.715 × 2.715 × 2.715.", "done": "≈ 20, so x₂ solves x³ = 20. Gone. That was the whole point of the Newton-Raphson step."}
     ]
   }
 }
}

# ---------- method_card (slim) ----------
method_card = {
 "title": "How to Work with Rates of Change & Iteration",
 "steps": [
   "Rate of change = gradient: (change in y) ÷ (change in x) between two points on the line or tangent.",
   "Iteration: start at x₀ and apply xₙ₊₁ = f(xₙ) repeatedly, feeding each answer back in.",
   "Keep full accuracy between steps; round only the final term to the accuracy asked for.",
   "A sign change in f(x) between two x-values shows a root lies between them."
 ],
 "content": "<p>A <strong>rate of change</strong> is the gradient of a graph: on a distance-time graph it is a speed, on a speed-time graph an acceleration. Find it with (change in y) ÷ (change in x).</p><p>An <strong>iterative process</strong> uses \\(x_{n+1} = f(x_n)\\): start at \\(x_0\\), substitute to get \\(x_1\\), then feed that back in for \\(x_2\\), and so on until the values settle.</p>",
 "example": "<p><strong>Iterate \\(x_{n+1} = \\sqrt{3x_n + 1}\\) with \\(x_0 = 1\\).</strong></p><p>\\(x_1 = \\sqrt{3(1)+1} = \\sqrt{4} = 2\\)</p><p>\\(x_2 = \\sqrt{3(2)+1} = \\sqrt{7} \\approx 2.65\\)</p>"
}

# ---------- assemble, preserving byte-for-byte ----------
# Minimal style repair: preserved worked_examples labels use em dashes ("Step 1 — Gradient"),
# which the style law / validator forbids. Replace " — " with ": " in labels only; content untouched.
we = json.loads(json.dumps(live["worked_examples"]))
for ex in we:
    for st in ex.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

out = {
  "method_card": method_card,
  "topic_links": live["topic_links"],       # preserved
  "problem_bank": problem_bank,
  "related_videos": live["related_videos"], # preserved ([])
  "worked_examples": we,                     # preserved (em dash in labels repaired)
  "tier_guides": tier_guides,
  "guided": guided,
}

with open("lesson_maths-eduqas_ratio-proportion-L06.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("written. method_card content words:",
      len(method_card["content"].replace("\\("," ").replace("\\)"," ").split()))
for t in ("bronze","silver","gold"):
    tot = sum(len(s.replace("\\("," ").replace("\\)"," ").split()) for s in tier_guides[t]["steps"])
    print(t, "tier_guide words:", tot)
