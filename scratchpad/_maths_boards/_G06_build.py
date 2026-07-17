# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion for graphs-L06 (Trigonometric
Graphs), board maths-eduqas. Fresh-solved bank, duplicate-answer disease
repaired, guided walks, openers, tier_guides, misconception expects, Chart.js
figures. Emits _G06_final.json."""
import json, io, math

live = json.load(io.open("_G06_live.json", encoding="utf-8"))

# ---------------------------------------------------------------- chart helper
def sin_pts(step=5):
    return [{"x": d, "y": round(math.sin(math.radians(d)), 4)} for d in range(0, 361, step)]
def cos_pts(step=5):
    return [{"x": d, "y": round(math.cos(math.radians(d)), 4)} for d in range(0, 361, step)]
def tan_pts(step=5):
    out = []
    for d in range(0, 361, step):
        if d in (90, 270):
            out.append({"x": d, "y": None}); continue
        y = math.tan(math.radians(d))
        out.append({"x": d, "y": None if abs(y) > 6 else round(y, 4)})
    return out

def chart(curve, k=None):
    tan = curve == "tan"
    pts = {"sin": sin_pts, "cos": cos_pts, "tan": tan_pts}[curve]()
    ds = [{"data": pts, "type": "line", "fill": False,
           "tension": 0 if tan else 0.35, "borderColor": "#3b82f6",
           "pointRadius": 0, "spanGaps": False}]
    if k is not None:
        ds.append({"data": [{"x": 0, "y": k}, {"x": 360, "y": k}],
                   "type": "line", "fill": False, "tension": 0,
                   "borderColor": "#f59e0b", "borderDash": [6, 4], "pointRadius": 0})
    if tan:
        yopts = {"min": -6, "max": 6, "grid": {"color": "rgba(148,163,184,0.2)"},
                 "ticks": {"stepSize": 2}, "title": {"text": "y", "display": True}}
    else:
        yopts = {"min": -1.2, "max": 1.2, "grid": {"color": "rgba(148,163,184,0.2)"},
                 "ticks": {"stepSize": 0.5}, "title": {"text": "y", "display": True}}
    return {"type": "scatter", "data": {"datasets": ds},
            "options": {"plugins": {"legend": {"display": False}},
                        "scales": {"x": {"min": 0, "max": 360,
                                         "grid": {"color": "rgba(148,163,184,0.15)"},
                                         "ticks": {"stepSize": 90},
                                         "title": {"text": "x (degrees)", "display": True}},
                                   "y": yopts}}}

def box(pre, answer, hint, post="", done=None, phase=None):
    b = {"pre": pre, "answer": answer, "hint": hint, "post": post}
    if done: b["done"] = done
    if phase: b["phase"] = phase
    return b
def say(s):
    return {"say": s}
def mis(pattern, message, expect, note=None):
    m = {"check": "common", "pattern": pattern, "message": message, "expect": expect}
    if note: m["note"] = note
    return m

SKIP = "Single exact value to recall directly from the graph; there are no intermediate steps to walk."

# ------------------------------------------------------------------ BRONZE bank
bronze = [
  # b0 angle of sin max = 90 (walk)
  {"display": "For \\(0° \\le x \\le 360°\\), at what angle does \\(y = \\sin x\\) reach its maximum? Give your answer in degrees.",
   "solutions": [90], "calculator": False, "input_type": "single_value",
   "hint": "Find where the sine curve is highest, then read that angle off the x-axis.",
   "chart": chart("sin"),
   "guided_steps": [
     say("The height of the sine curve at angle x is \\(\\sin x\\). We want where that height is greatest."),
     box("The sine curve never rises above its top value. Its maximum height is ", 1,
         "Sine tops out at 1."),
     box("Read across to where the curve first reaches that height. On the sine graph the peak is at x = ", 90,
         "A quarter of the way through the 360° wave.", post="°", phase="substitute"),
     box("Check with the period: a quarter of 360° is 360 ÷ 4 = ", 90,
         "360 divided by 4.", post="°", done="The maximum of y = sin x is at x = 90°."),
   ],
   "misconceptions": [
     mis("value_not_angle", "The question asks for the angle, not the height. The maximum height is 1, but it occurs at x = 90°.", 1),
   ]},
  # b1 sin0 = 0 (recall skip)
  {"display": "What is the value of \\(\\sin 0°\\)?",
   "solutions": [0], "calculator": False, "input_type": "single_value",
   "hint": "The sine curve starts at the origin.", "guided_skip_reason": SKIP,
   "misconceptions": [
     mis("sin_cos_swap", "sin 0° = 0: the sine curve starts at the origin. cos 0° = 1, which is the likely mix-up.", 1),
   ]},
  # b2 cos0 = 1 (recall skip)
  {"display": "What is the value of \\(\\cos 0°\\)?",
   "solutions": [1], "calculator": False, "input_type": "single_value",
   "hint": "The cosine curve starts at its highest point.", "guided_skip_reason": SKIP,
   "misconceptions": [
     mis("sin_cos_swap", "cos 0° = 1: the cosine curve starts at its maximum. sin 0° = 0, which is the likely mix-up.", 0),
   ]},
  # b3 sin30 = 0.5 (recall skip)
  {"display": "What is the value of \\(\\sin 30°\\)?",
   "solutions": [0.5], "calculator": False, "input_type": "single_value",
   "hint": "An exact value worth memorising: a half.", "guided_skip_reason": SKIP,
   "misconceptions": [
     mis("angle_as_decimal", "sin 30° is the exact value 0.5, not 0.3. Do not turn the angle 30 into a decimal; read the height off the sine curve.", 0.3),
   ]},
  # b4 cos180 = -1 (recall skip)
  {"display": "What is the value of \\(\\cos 180°\\)?",
   "solutions": [-1], "calculator": False, "input_type": "single_value",
   "hint": "The cosine curve is at its lowest point at 180°.", "guided_skip_reason": SKIP,
   "misconceptions": [
     mis("sign", "cos 180° = −1, not 1: the cosine curve is at its minimum (its lowest point) at 180°.", 1),
   ]},
  # b5 period of tan (MC keep)
  {"display": "What is the period of the \\(\\tan\\) graph?",
   "options": ["90°", "180°", "270°", "360°"],
   "solutions": [1], "calculator": False, "input_type": "multiple_choice",
   "hint": "The tan graph repeats twice as fast as sin and cos.",
   "chart": chart("tan"),
   "misconceptions": [
     mis("confusion", "The tan graph repeats every 180°, not 360°. Unlike sin and cos, tan completes a full cycle twice as fast.", 3),
   ]},
  # b6 period of sin = 360 (walk)
  {"display": "What is the period of the graph \\(y = \\sin x\\)? Give your answer in degrees.",
   "solutions": [360], "calculator": False, "input_type": "single_value",
   "hint": "Measure the x-length of one complete wave.",
   "chart": chart("sin"),
   "guided_steps": [
     say("The period is the horizontal length of one complete wave, before the pattern repeats."),
     box("A quarter of the wave, from the start up to the first peak, spans 90°. One quarter = ", 90,
         "From 0° up to the peak at 90°.", post="°"),
     box("A full wave is 4 of those quarters: 4 × 90 = ", 360,
         "Four quarter-waves.", post="°", phase="substitute"),
     box("That full-wave length is the period. Reading the graph, sine returns to 0 rising at x = ", 360,
         "Back to the start height, one full loop.", post="°",
         done="One complete wave of y = sin x spans 360°, so the period is 360°."),
   ],
   "misconceptions": [
     mis("confusion", "The period of y = sin x is 360°. 180° is the period of the tan graph, a common mix-up.", 180),
   ]},
  # b7 angle of cos min = 180 (walk)
  {"display": "For \\(0° \\le x \\le 360°\\), at what angle does \\(y = \\cos x\\) reach its minimum? Give your answer in degrees.",
   "solutions": [180], "calculator": False, "input_type": "single_value",
   "hint": "Find where the cosine curve is lowest, then read that angle.",
   "chart": chart("cos"),
   "guided_steps": [
     say("The cosine curve starts at its maximum and dips to its minimum. We want the angle of that lowest point."),
     box("Cosine bottoms out at its lowest value. That minimum height is ", -1,
         "Cosine never falls below −1."),
     box("Read across to where the curve reaches −1. On the cosine graph that trough is at x = ", 180,
         "Halfway along the wave.", post="°", phase="substitute"),
     box("Confirm: the trough sits halfway through the 360° wave, 360 ÷ 2 = ", 180,
         "360 divided by 2.", post="°",
         done="y = cos x is at its minimum, −1, when x = 180°."),
   ],
   "misconceptions": [
     mis("value_not_angle", "The question asks for the angle, not the height. The minimum height is −1, but it occurs at x = 180°.", -1),
   ]},
]

# ------------------------------------------------------------------ SILVER bank
silver = [
  # s0 sin x = 1 -> 90 (walk)  [first-of-tier: completion deal]
  {"display": "Solve \\(\\sin x = 1\\) for \\(0° \\le x \\le 360°\\). Give your answer in degrees.",
   "solutions": [90], "calculator": False, "input_type": "single_value",
   "hint": "sin x = 1 at the single peak of the curve.",
   "chart": chart("sin", 1),
   "guided_steps": [
     say("\\(\\sin x = 1\\) means the height of the sine curve is at its maximum."),
     box("The maximum height of the sine curve is ", 1, "Sine never exceeds 1."),
     box("In 0° to 360° the curve hits that peak just once. Reading across, the peak is at x = ", 90,
         "A quarter of the way through the wave.", post="°", phase="substitute"),
     box("Check the period: a quarter of 360° is 360 ÷ 4 = ", 90,
         "360 divided by 4.", post="°", done="sin x = 1 only at x = 90°, so the solution is 90°."),
   ],
   "misconceptions": [
     mis("peak_trough_swap", "sin x = 1 (not −1) is the PEAK, at x = 90°. The trough where sin x = −1 is at 270°.", 270),
   ]},
  # s1 cos x = -1 -> 180 (walk)
  {"display": "Solve \\(\\cos x = -1\\) for \\(0° \\le x \\le 360°\\). Give your answer in degrees.",
   "solutions": [180], "calculator": False, "input_type": "single_value",
   "hint": "cos x = −1 at the single trough of the curve.",
   "chart": chart("cos", -1),
   "guided_steps": [
     say("\\(\\cos x = -1\\) means the cosine curve is at its minimum."),
     box("The minimum height of the cosine curve is ", -1, "Cosine bottoms out at −1."),
     box("The curve reaches −1 at its single trough. Reading across, that trough is at x = ", 180,
         "Halfway through the wave.", post="°", phase="substitute"),
     box("Check: halfway through the 360° wave is 360 ÷ 2 = ", 180,
         "360 divided by 2.", post="°", done="cos x = −1 only at x = 180°, so the solution is 180°."),
   ],
   "misconceptions": [
     mis("max_min_swap", "cos x = −1 is the minimum, at x = 180°. At x = 0° cosine is +1 (its maximum), the opposite point.", 0),
   ]},
  # s2 sin x = 0 count = 3 (walk)
  {"display": "Solve \\(\\sin x = 0\\) for \\(0° \\le x \\le 360°\\). How many solutions are there?",
   "solutions": [3], "calculator": False, "input_type": "single_value",
   "hint": "Count every crossing of the x-axis, including both endpoints.",
   "chart": chart("sin", 0),
   "guided_steps": [
     say("\\(\\sin x = 0\\) where the sine curve crosses the x-axis."),
     box("It crosses at the very start, x = 0°, then again halfway along at x = ", 180,
         "The curve returns to 0 at the halfway point.", post="°"),
     box("It crosses once more before the range ends, at x = ", 360,
         "Back to 0 at the end of one full wave.", post="°", phase="substitute"),
     box("Count the crossings at 0°, 180° and 360°: that is ", 3,
         "Three x-values.", post=" solutions", done="sin x = 0 at 0°, 180° and 360°, so there are 3 solutions."),
   ],
   "misconceptions": [
     mis("endpoint", "There are 3 solutions: x = 0°, 180° and 360°. Both endpoints are included in 0° ≤ x ≤ 360°.", 2),
   ]},
  # s3 sin30 = 0.5 (recall skip)
  {"display": "What is the value of \\(\\sin 30°\\)?",
   "solutions": [0.5], "calculator": False, "input_type": "single_value",
   "hint": "An exact value: a half.", "guided_skip_reason": SKIP,
   "misconceptions": [
     mis("angle_as_decimal", "sin 30° is the exact value 0.5, not 0.3. Do not turn the angle 30 into a decimal; read the height off the sine curve.", 0.3),
   ]},
  # s4 cos120 = -0.5 (walk)  [changed from cos60 to remove duplicate 0.5]
  {"display": "What is the value of \\(\\cos 120°\\)?",
   "solutions": [-0.5], "calculator": False, "input_type": "single_value",
   "hint": "Past 90°, cosine is negative; its size matches cos 60°.",
   "chart": chart("cos", -0.5),
   "guided_steps": [
     say("120° is past 90°, so on the cosine curve the height is negative here."),
     box("Find the reference angle, how far 120° is from 180°: 180 − 120 = ", 60,
         "180 minus 120.", post="°"),
     box("The matching first-quadrant value is cos 60° = ", 0.5,
         "An exact value: a half.", phase="substitute"),
     box("In the second quadrant cosine is negative, so cos 120° = ", -0.5,
         "Negative of 0.5.", done="cos 120° = −cos 60° = −0.5."),
   ],
   "misconceptions": [
     mis("sign", "cos 120° = −0.5, not 0.5: past 90° cosine is negative. Its size matches cos 60° = 0.5, but the sign is negative.", 0.5),
   ]},
  # s5 tan asymptotes MC (keep)
  {"display": "At what angles does the \\(\\tan\\) graph have vertical asymptotes between \\(0°\\) and \\(360°\\)?",
   "options": ["0° and 180°", "90° and 270°", "180° and 360°", "45° and 225°"],
   "solutions": [1], "calculator": False, "input_type": "multiple_choice",
   "hint": "Asymptotes are where tan is undefined, not where it is zero.",
   "chart": chart("tan"),
   "misconceptions": [
     mis("zero_vs_asymptote", "tan is undefined (its asymptotes) at 90° and 270°. At 0° and 180° tan = 0, where it crosses zero, not where it blows up.", 0),
   ]},
  # s6 cos x = 0 larger = 270 (walk)  [changed from smaller=90 to remove duplicate 90]
  {"display": "Solve \\(\\cos x = 0\\) for \\(0° \\le x \\le 360°\\). Give the <strong>larger</strong> solution.",
   "solutions": [270], "calculator": False, "input_type": "single_value",
   "hint": "cos x = 0 twice; you want the second, larger crossing.",
   "chart": chart("cos", 0),
   "guided_steps": [
     say("\\(\\cos x = 0\\) where the cosine curve crosses the x-axis. In this range it crosses twice."),
     box("The smaller crossing is a quarter of the way along, at x = ", 90,
         "A quarter of the way along.", post="°"),
     box("By symmetry the larger crossing sits at 360 − 90 = ", 270,
         "360 minus 90.", post="°", phase="substitute"),
     box("Check: cos 270° = 0, and 270° is bigger than 90°, so the larger solution is ", 270,
         "The second crossing.", post="°", done="cos x = 0 at 90° and 270°; the larger is 270°."),
   ],
   "misconceptions": [
     mis("which_solution", "cos x = 0 at 90° and 270°. 90° is the smaller; the question asks for the larger, 270°.", 90),
   ]},
]

# -------------------------------------------------------------------- GOLD bank
gold = [
  # g0 sin x = 0.5 larger = 150 (walk)  [first-of-tier]
  {"display": "Solve \\(\\sin x = 0.5\\) for \\(0° \\le x \\le 360°\\). Give the <strong>larger</strong> solution.",
   "solutions": [150], "calculator": False, "input_type": "single_value",
   "hint": "Find the reference angle, then use 180° minus it.",
   "chart": chart("sin", 0.5),
   "guided_steps": [
     say("Start from the exact value: \\(\\sin 30° = 0.5\\)."),
     box("The reference angle, the exact angle whose sine is 0.5, is ", 30,
         "sin of what angle is 0.5?", post="°"),
     box("Sine is positive in the second quadrant too. The second solution is 180 − 30 = ", 150,
         "180 minus the reference angle.", post="°", phase="substitute"),
     box("The two solutions are 30° and 150°; the larger is ", 150,
         "The bigger of the two.", post="°", done="sin x = 0.5 at 30° and 150° (symmetry about 90°); larger = 150°."),
   ],
   "misconceptions": [
     mis("which_solution", "sin x = 0.5 at 30° and 150°. 30° is the smaller; the larger, by symmetry about 90° (180° − 30°), is 150°.", 30),
   ]},
  # g1 cos x = 0.5 larger = 300 (walk)
  {"display": "Solve \\(\\cos x = 0.5\\) for \\(0° \\le x \\le 360°\\). Give the <strong>larger</strong> solution.",
   "solutions": [300], "calculator": False, "input_type": "single_value",
   "hint": "Find the reference angle, then use 360° minus it.",
   "chart": chart("cos", 0.5),
   "guided_steps": [
     say("Start from the exact value: \\(\\cos 60° = 0.5\\)."),
     box("The reference angle, the exact angle whose cosine is 0.5, is ", 60,
         "cos of what angle is 0.5?", post="°"),
     box("Cosine is positive in the fourth quadrant too. The second solution is 360 − 60 = ", 300,
         "360 minus the reference angle.", post="°", phase="substitute"),
     box("The two solutions are 60° and 300°; the larger is ", 300,
         "The bigger of the two.", post="°", done="cos x = 0.5 at 60° and 300° (symmetry about 360°); larger = 300°."),
   ],
   "misconceptions": [
     mis("which_solution", "cos x = 0.5 at 60° and 300°. 60° is the smaller; the larger, by symmetry (360° − 60°), is 300°.", 60),
   ]},
  # g2 sin x = -1 -> 270 (walk)
  {"display": "Solve \\(\\sin x = -1\\) for \\(0° \\le x \\le 360°\\). Give your answer in degrees.",
   "solutions": [270], "calculator": False, "input_type": "single_value",
   "hint": "sin x = −1 at the trough, three quarters along the wave.",
   "chart": chart("sin", -1),
   "guided_steps": [
     say("\\(\\sin x = -1\\) is the lowest point of the sine curve."),
     box("The minimum value of the sine curve is ", -1, "Sine bottoms out at −1."),
     box("The trough sits three quarters of the way through the 360° wave: 3 × 90 = ", 270,
         "Three quarter-waves along.", post="°", phase="substitute"),
     box("Check by reading the graph: the sine curve is at its lowest at x = ", 270,
         "The trough.", post="°", done="sin x = −1 only at x = 270° in the range, so x = 270°."),
   ],
   "misconceptions": [
     mis("peak_trough_swap", "sin x = −1 (not +1) is the TROUGH, at x = 270°. The peak where sin x = 1 is at 90°.", 90),
   ]},
  # g3 tan x = 0 count = 3 (walk)
  {"display": "Solve \\(\\tan x = 0\\) for \\(0° \\le x \\le 360°\\). How many solutions are there?",
   "solutions": [3], "calculator": False, "input_type": "single_value",
   "hint": "tan is zero wherever sin is zero: count them in the range.",
   "chart": chart("tan", 0),
   "guided_steps": [
     say("\\(\\tan x = 0\\) where the tangent curve crosses the x-axis, which is where \\(\\sin x = 0\\)."),
     box("The first zero is at x = 0°. The tan graph repeats every 180°, so the next zero is at x = ", 180,
         "Add one period of 180°.", post="°"),
     box("The next zero after 180° is at x = ", 360,
         "Add another 180°.", post="°", phase="substitute"),
     box("Count the zeros at 0°, 180° and 360°: that is ", 3,
         "Three x-values.", post=" solutions", done="tan x = 0 at 0°, 180° and 360°, so 3 solutions."),
   ],
   "misconceptions": [
     mis("endpoint", "tan x = 0 at 0°, 180° and 360°, so 3 solutions. Both endpoints of 0° ≤ x ≤ 360° count.", 2),
   ]},
  # g4 cos x = -0.5 smaller = 120 (walk)
  {"display": "Solve \\(\\cos x = -0.5\\) for \\(0° \\le x \\le 360°\\). Give the <strong>smaller</strong> solution.",
   "solutions": [120], "calculator": False, "input_type": "single_value",
   "hint": "Reference angle 60°; cosine is negative in two quadrants.",
   "chart": chart("cos", -0.5),
   "guided_steps": [
     say("\\(\\cos 60° = 0.5\\), so the reference angle is 60°. Cosine is negative in the second and third quadrants."),
     box("The second-quadrant solution is 180 − 60 = ", 120,
         "180 minus the reference angle.", post="°"),
     box("The third-quadrant solution is 180 + 60 = ", 240,
         "180 plus the reference angle.", post="°", phase="substitute"),
     box("The two solutions are 120° and 240°; the smaller is ", 120,
         "The smaller of the two.", post="°", done="cos x = −0.5 at 120° and 240°; the smaller is 120°."),
   ],
   "misconceptions": [
     mis("which_solution", "cos x = −0.5 at 120° and 240°. 240° is the larger; the question asks for the smaller, 120°.", 240),
   ]},
]

# --------------------------------------------------------------------- opener
wheel_svg = (
 '<svg viewBox="0 0 260 210" role="img" aria-label="A big wheel of radius 10 m; '
 'the top is +10 m above the centre line, the bottom is -10 m, the start point at the right is level with the centre at 0 m" '
 'style="max-width:280px;width:100%;height:auto;display:block;margin:0 auto 8px">'
 '<line x1="46" y1="105" x2="214" y2="105" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity="0.7"/>'
 '<circle cx="130" cy="105" r="64" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
 '<circle cx="130" cy="41" r="3.5" fill="currentColor"/>'
 '<circle cx="130" cy="169" r="3.5" fill="currentColor"/>'
 '<circle cx="194" cy="105" r="4.5" fill="#f59e0b" stroke="currentColor" stroke-width="1"/>'
 '<path d="M206 92 A22 22 0 0 0 190 76" fill="none" stroke="currentColor" stroke-width="1.4"/>'
 '<path d="M190 76 l6 1 l-3 5 z" fill="currentColor"/>'
 '<text x="130" y="30" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">top: +10 m</text>'
 '<text x="130" y="188" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">bottom: −10 m</text>'
 '<text x="150" y="123" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">start: 0 m</text>'
 '<text x="130" y="120" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.8">centre line</text>'
 '</svg><span class="figure-caption">Diagram not drawn accurately</span>'
 'A big wheel of radius 10 m turns anticlockwise.<br>Height is measured above the dashed centre line.'
)

opener = {
  "label": "Before any graphs",
  "display": wheel_svg,
  "steps": [
    box("You ride a big wheel of radius 10 m, starting level with the centre (height 0 m). A quarter turn (90°) later you are right at the top. Your height there is ",
        10, "One full radius above the centre.", post=" m"),
    say("Plot height against the angle turned and you trace a wave: 0 at 0°, up to +10 at 90°, back to 0 at 180°, down to −10 at 270°, back to 0 at 360°. That IS the sine curve, scaled. \\(\\sin x\\) is exactly this height when the radius is 1, running 0, 1, 0, −1, 0."),
    box("Keep turning. After a half turn (180°) you are back level with the centre, so your height is ",
        0, "Halfway round, level with the middle again.", post=" m"),
    box("After three quarters of a turn (270°) you are at the very bottom, one radius below the centre. Your height is ",
        -10, "One radius below the centre.", post=" m"),
    say("The height repeats every full turn (360°): that repeat length is the <strong>period</strong>. \\(y = \\sin x\\) models this with radius 1 (heights −1 to 1), \\(y = \\cos x\\) is the same wheel started from the top, and \\(y = \\tan x\\) is their ratio. Reading a trig graph is just reading this wheel's height."),
  ],
}

# ---------------------------------------------------------------------- teach
teach = {
  "bronze": {
    "label": "Together: read the sine curve",
    "display": "Trace the sine curve and read its height at each quarter turn.",
    "steps": [
      box("Start at the origin: sin 0° = ", 0, "The curve starts at 0."),
      box("A quarter turn on, at the peak: sin 90° = ", 1, "The highest point."),
      box("Halfway, back on the axis: sin 180° = ", 0, "Back to 0."),
      box("Three quarters, at the trough: sin 270° = ", -1,
          "The lowest point.", done="Those four heights, 0, 1, 0, −1, are the shape of the whole sine wave."),
    ],
  },
  "silver": {
    "label": "Together: solve a simple equation",
    "display": "Solve \\(\\cos x = 1\\) for \\(0° \\le x \\le 360°\\).",
    "steps": [
      box("cos x = 1 means the cosine is at its maximum. Its maximum value is ", 1, "Cosine tops out at 1."),
      box("The cosine curve is at 1 at the very start, x = ", 0, "cos 0° = 1.", post="°"),
      box("It returns to 1 after one full period: 0 + 360 = ", 360, "One period later.", post="°"),
      box("So in 0° to 360° the number of solutions is ", 2,
          "Count 0° and 360°.", done="cos x = 1 at x = 0° and x = 360°: the two ends of one full wave."),
    ],
  },
  "gold": {
    "label": "Together: symmetry with a negative value",
    "display": "Solve \\(\\sin x = -0.5\\) for \\(0° \\le x \\le 360°\\).",
    "steps": [
      box("sin 30° = 0.5, so the reference angle is ", 30, "The angle whose sine is 0.5.", post="°"),
      box("Sine is negative in the third quadrant: 180 + 30 = ", 210, "180 plus the reference angle.", post="°"),
      box("Sine is negative in the fourth quadrant too: 360 − 30 = ", 330, "360 minus the reference angle.", post="°"),
      box("The larger of 210° and 330° is ", 330,
          "The bigger of the two.", done="sin x = −0.5 at 210° and 330°: that is the symmetry move for negative values."),
    ],
  },
}

# ------------------------------------------------------------------ tier_guides
tier_guides = {
  "bronze": {
    "title": "Bronze: know the curves and their key values",
    "steps": [
      "The three curves: <strong>sin</strong> starts at 0 and waves between −1 and 1; <strong>cos</strong> starts at 1 and waves between −1 and 1; <strong>tan</strong> repeats every 180° with asymptotes at 90° and 270°.",
      "Memorise the exact values: sin 0° = 0, sin 30° = 0.5, sin 90° = 1; cos 0° = 1, cos 90° = 0, cos 180° = −1.",
      "Key features: sin and cos have period 360°; the sine peak is at 90°, the cosine trough at 180°.",
    ],
    "example": {
      "question": "What is the value of cos 90°?",
      "steps": [
        {"label": "Locate", "content": "<p>Find x = 90° on the cosine curve.</p>"},
        {"label": "Read", "content": "<p>The cosine curve crosses the x-axis at 90°, so its height is 0.</p>"},
        {"label": "Check", "content": "<p>cos starts at 1 (x = 0°) and falls to 0 by 90°.</p>"},
        {"label": "Answer", "content": "<p>cos 90° = 0.</p>", "isAnswer": True, "is_answer": True},
      ],
    },
  },
  "silver": {
    "title": "Silver: read values and solve simple equations",
    "steps": [
      "To solve sin x = k or cos x = k, draw the line y = k across the curve and read every x where they meet in the range.",
      "Endpoints count: 0° ≤ x ≤ 360° includes both 0° and 360°, so sin x = 0 has 3 solutions.",
      "Past 90° the size matches a first-quadrant angle but the sign can be negative: cos 120° = −cos 60° = −0.5.",
    ],
    "example": {
      "question": "Solve cos x = 0 for 0° ≤ x ≤ 360°.",
      "steps": [
        {"label": "Draw", "content": "<p>Mark the axis line y = 0 on the cosine curve.</p>"},
        {"label": "Read", "content": "<p>The curve crosses the axis at x = 90° and x = 270°.</p>"},
        {"label": "Check", "content": "<p>cos 90° = 0 and cos 270° = 0.</p>"},
        {"label": "Answer", "content": "<p>x = 90° or x = 270°.</p>", "isAnswer": True, "is_answer": True},
      ],
    },
  },
  "gold": {
    "title": "Gold: use symmetry for the second solution",
    "steps": [
      "Find the reference angle from the exact value (sin 30° = 0.5 gives 30°), then use symmetry for its partner.",
      "For sin, the two solutions are the reference angle and 180° − it. For cos, they are the reference angle and 360° − it.",
      "When the value is negative, the solutions move to the quadrants where that curve is negative: cos x = −0.5 gives 120° and 240°.",
    ],
    "example": {
      "question": "Solve sin x = 0.5 for 0° ≤ x ≤ 360°.",
      "steps": [
        {"label": "Reference", "content": "<p>sin 30° = 0.5, so the reference angle is 30°.</p>"},
        {"label": "Symmetry", "content": "<p>The second solution is 180° − 30° = 150°.</p>"},
        {"label": "Check", "content": "<p>sin 150° = sin 30° = 0.5.</p>"},
        {"label": "Answer", "content": "<p>x = 30° or x = 150°.</p>", "isAnswer": True, "is_answer": True},
      ],
    },
  },
}

# ------------------------------------------------------------------ method_card
method_card = {
  "title": "Sketch and Use Trigonometric Graphs",
  "steps": [
    "Identify the curve: sin starts at 0, cos starts at 1, tan repeats every 180°.",
    "Mark the key points at 0°, 90°, 180°, 270°, 360° with their known heights.",
    "To solve sin x = k or cos x = k, draw y = k and read every crossing in the range.",
    "Use symmetry for the second solution, and watch the sign past 90°.",
  ],
  "content": ("<p>The three graphs to know: \\(y = \\sin x\\) waves from 0 between −1 and 1 (period 360°); "
              "\\(y = \\cos x\\) is the same wave started at 1 (period 360°); \\(y = \\tan x\\) repeats every 180° "
              "with asymptotes at 90° and 270°. Learn the exact heights: sin 0° = 0, sin 30° = 0.5, sin 90° = 1, "
              "cos 0° = 1, cos 90° = 0, cos 180° = −1. To solve an equation, draw the line \\(y = k\\) and read every "
              "x where it meets the curve in the range; both endpoints count. For a negative value or a second "
              "solution, use the wave's symmetry: sin gives 180° − x, cos gives 360° − x.</p>"),
  "example": ("<p><strong>Use the graph of \\(y = \\sin x\\) to solve \\(\\sin x = 0.5\\) for \\(0° \\le x \\le 360°\\).</strong></p>"
              "<p><strong>Step 1:</strong> Draw the line \\(y = 0.5\\) on the sine graph.</p>"
              "<p><strong>Step 2:</strong> Read where it meets the curve: \\(x = 30°\\) and \\(x = 150°\\).</p>"
              "<p><strong>Answer:</strong> \\(x = 30°\\) or \\(x = 150°\\).</p>"),
}

# ------------------------------------------------------ worked_examples (dashes)
we = json.loads(json.dumps(live["worked_examples"]))
for ex in we:
    for st in ex.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ": ")

# ---------------------------------------------------------------- assemble
pd = {
  "method_card": method_card,
  "topic_links": live["topic_links"],
  "tier_guides": tier_guides,
  "guided": {"opener": opener, "teach": teach},
  "problem_bank": {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": live["problem_bank"]["bronze_description"],
    "silver_description": live["problem_bank"]["silver_description"],
    "gold_description": live["problem_bank"]["gold_description"],
  },
  "related_videos": live["related_videos"],
  "worked_examples": we,
}

json.dump(pd, io.open("_G06_final.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote _G06_final.json")
# quick self-checks
for t, arr in (("bronze", bronze), ("silver", silver), ("gold", gold)):
    sols = [tuple(p["solutions"]) for p in arr if p.get("input_type") != "multiple_choice"]
    dup = len(sols) != len(set(sols))
    print(t, "non-MC sols", sols, "DUPLICATE!" if dup else "ok")
