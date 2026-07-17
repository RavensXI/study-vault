# -*- coding: utf-8 -*-
import json, io, math

MINUS = "−"  # unicode minus

def curve(fn, xmax, step=15):
    pts = []
    x = 0
    while x <= xmax:
        y = round(fn(math.radians(x)), 4)
        if y == 0:  # avoid -0.0
            y = 0.0
        pts.append({"x": x, "y": y})
        x += step
    return pts

def chart(fn, xmax, label, kline=None, xstep=90):
    ds = [{
        "type": "line",
        "data": curve(fn, xmax),
        "tension": 0.35, "fill": False,
        "borderColor": "#3b82f6", "pointRadius": 0, "label": label
    }]
    if kline is not None:
        ds.append({
            "type": "line",
            "data": [{"x": 0, "y": kline}, {"x": xmax, "y": kline}],
            "borderColor": "#9ca3af", "borderDash": [6, 4],
            "borderWidth": 1, "pointRadius": 0,
            "label": "y = " + (str(kline) if kline >= 0 else MINUS + str(abs(kline)))
        })
    return {
        "type": "scatter",
        "data": {"datasets": ds},
        "options": {"scales": {
            "x": {"min": 0, "max": xmax, "ticks": {"stepSize": xstep},
                  "grid": {"color": "rgba(0,0,0,0.05)"},
                  "title": {"text": "x (degrees)", "display": True}},
            "y": {"min": -1.2, "max": 1.2, "ticks": {"stepSize": 0.5},
                  "grid": {"color": "rgba(0,0,0,0.08)"},
                  "title": {"text": "y", "display": True}}
        }}
    }

def m(pattern, message, expect, note):
    return {"pattern": pattern, "message": message, "expect": expect, "note": note}

def say(s): return {"say": s}
def box(pre, answer, hint, post="", phase=False, done=None, sayv=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = "substitute"
    if done: d["done"] = done
    if sayv is not None: d["say"] = sayv
    return d

# ---------------- BRONZE (8) ----------------
bronze = [
 {  # B1 sin 0
  "display": "What is \\(\\sin 0°\\)?", "solutions": [0], "calculator": False,
  "input_type": "single_value", "hint": "The sine curve begins on the x-axis.",
  "misconceptions": [m("confuse_cos", "sin 0° = 0; the sine curve starts on the axis. cos 0° = 1 starts at the top, so do not swap them.", 1, "confuses sin 0 with cos 0")],
  "guided_steps": [
    say("sin 0° is where the sine curve begins. Read it straight off the graph."),
    box("The sine curve rises to a maximum of ", 1, "The top of the wave is 1."),
    box("At the very start, x = 0°, the curve sits on the x-axis, so its height is ", 0, "It passes through the origin.", phase=True),
    box("So sin 0° = ", 0, "Height at the origin is 0.", phase=True, done="The sine curve starts at (0°, 0), so sin 0° = 0.")
  ]},
 {  # B2 cos 0
  "display": "What is \\(\\cos 0°\\)?", "solutions": [1], "calculator": False,
  "input_type": "single_value", "hint": "The cosine curve begins at its highest point.",
  "misconceptions": [m("confuse_sin", "cos 0° = 1, the top of the cosine curve. sin 0° = 0 starts on the axis, so do not swap them.", 0, "confuses cos 0 with sin 0")],
  "guided_steps": [
    say("cos 0° is where the cosine curve begins."),
    box("The lowest the cosine curve ever drops is ", -1, "Cosine bottoms out at minus one."),
    box("But at the very start, x = 0°, the cosine curve is at its highest point, which is ", 1, "Cosine starts at the top.", phase=True),
    box("So cos 0° = ", 1, "One.", phase=True, done="The cosine curve starts at (0°, 1), so cos 0° = 1.")
  ]},
 {  # B3 cos 180
  "display": "What is \\(\\cos 180°\\)?", "solutions": [-1], "calculator": False,
  "input_type": "single_value", "hint": "Track the cosine curve from the top down to 180°.",
  "misconceptions": [m("forgets_sign", "cos 180° = −1, the bottom of the curve. It climbs back to +1 only at 360°.", 1, "forgets the negative sign")],
  "guided_steps": [
    say("The cosine curve starts at the top and falls. Track it as far as 180°."),
    box("At x = 0° the cosine curve is at its maximum, cos 0° = ", 1, "Cosine starts at the top."),
    box("By x = 180° it has fallen to its lowest point. The minimum value of cosine is ", -1, "Cosine bottoms out at minus one.", phase=True),
    box("So cos 180° = ", -1, "Minus one.", phase=True, done="The cosine curve reaches its lowest point, −1, at 180°.")
  ]},
 {  # B4 period sin
  "display": "What is the period of \\(\\sin x\\), in degrees?", "solutions": [360], "calculator": False,
  "input_type": "single_value", "hint": "How far along x before the wave repeats exactly.",
  "misconceptions": [m("confuse_tan_period", "sin repeats every 360°. 180° is the period of tan, not sin.", 180, "uses tan period for sin")],
  "guided_steps": [
    say("The period is how far along x you travel before the wave repeats exactly."),
    box("The sine curve reaches its first peak at x = ", 90, "The maximum is at 90°."),
    box("It returns to the same height, moving the same way, after one full turn. One full turn is ", 360, "Degrees in a whole turn.", phase=True),
    box("So the period of sin x is ", 360, "A full turn is 360°.", phase=True, done="sin repeats every 360°.")
  ]},
 {  # B5 period tan
  "display": "What is the period of \\(\\tan x\\), in degrees?", "solutions": [180], "calculator": False,
  "input_type": "single_value", "hint": "The tangent curve repeats sooner than sine and cosine.",
  "misconceptions": [m("assume_360", "tan repeats every 180°, not 360°. Its period is half that of sine and cosine.", 360, "assumes same period as sin")],
  "guided_steps": [
    say("The tangent curve repeats sooner than a sine wave."),
    box("The tan curve has its first vertical asymptote at x = ", 90, "tan is undefined at 90°."),
    box("It then repeats after only half a turn. Half of 360° = ", 180, "360 divided by 2.", phase=True),
    box("So the period of tan x is ", 180, "Half of 360 is 180.", phase=True, done="tan repeats every 180°, twice as often as sin and cos.")
  ]},
 {  # B6 sin max position (replaces sin 90 = 1 duplicate)
  "display": "For \\(0° \\le x \\le 360°\\), at what value of \\(x\\) does \\(\\sin x\\) reach its maximum? Give your answer in degrees.",
  "solutions": [90], "calculator": False, "input_type": "single_value",
  "hint": "The question asks WHERE the wave is highest, not how high.",
  "misconceptions": [m("gives_value", "The question asks WHERE, so give the angle x = 90°. The height there is 1, but that is not what was asked.", 1, "gives the value instead of the position")],
  "guided_steps": [
    say("We want WHERE the sine wave is highest, not how high it goes."),
    box("The maximum height of the sine curve is ", 1, "Sine never exceeds 1."),
    box("It first reaches that height a quarter of the way through the 360° cycle. A quarter of 360° = ", 90, "360 divided by 4.", phase=True),
    box("So sin x is at its maximum when x = ", 90, "Ninety degrees.", phase=True, done="The peak sits at (90°, 1).")
  ]},
 {  # B7 sin min position (replaces sin 270 = -1 duplicate)
  "display": "For \\(0° \\le x \\le 360°\\), at what value of \\(x\\) does \\(\\sin x\\) reach its minimum? Give your answer in degrees.",
  "solutions": [270], "calculator": False, "input_type": "single_value",
  "hint": "The lowest point of the sine wave, three-quarters of the way along.",
  "misconceptions": [
    m("gives_value", "The question asks WHERE, so give the angle x = 270°. The value there is −1, but that is not what was asked.", -1, "gives the value instead of the position"),
    m("confuse_max", "The minimum is at 270°, not 90°. The sine curve peaks at 90° and bottoms out at 270°.", 90, "confuses minimum with maximum position")],
  "guided_steps": [
    say("The sine curve bottoms out three-quarters of the way along."),
    box("The minimum height of the sine curve is ", -1, "Sine never drops below minus one."),
    box("It reaches that low point three-quarters of the way through. (3 ÷ 4) × 360° = ", 270, "Three-quarters of 360.", phase=True),
    box("So sin x is at its minimum when x = ", 270, "Two hundred and seventy.", phase=True, done="The lowest point sits at (270°, −1).")
  ]},
 {  # B8 crossings (replaces max value of sin = 1 duplicate), has chart
  "display": "For \\(0° \\le x \\le 360°\\), how many times does the graph of \\(\\sin x\\) cross the x-axis?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Count where the curve touches the axis, including both ends of the range.",
  "misconceptions": [
    m("miss_endpoint", "In 0° ≤ x ≤ 360° the curve is on the axis at 0°, 180° AND 360°, so there are 3 crossings. Missing an endpoint gives 2.", 2, "forgets one endpoint"),
    m("interior_only", "Count all three points on the axis: 0°, 180° and 360°. Counting only 180° gives 1.", 1, "counts only the interior crossing")],
  "chart": chart(math.sin, 360, "y = sin x"),
  "guided_steps": [
    say("Count where the sine curve cuts the x-axis between 0° and 360° inclusive."),
    box("It starts on the axis at x = 0°, that is crossing number ", 1, "The start counts."),
    box("It comes back to the axis at x = 180°, crossing number ", 2, "Halfway along the range.", phase=True),
    box("It finishes on the axis at x = 360°, crossing number ", 3, "The end counts too.", phase=True),
    box("So the number of crossings is ", 3, "Count them: 0, 180, 360.", phase=True, done="Crossings at 0°, 180° and 360°, that is 3.")
  ]},
]

# ---------------- SILVER (7) ----------------
silver = [
 {  # S1 sin=0.5 smaller
  "display": "Solve \\(\\sin x = 0.5\\) for \\(0° \\le x \\le 360°\\). Give the smaller solution.",
  "solutions": [30], "calculator": True, "input_type": "single_value",
  "hint": "The calculator gives the first solution directly.",
  "misconceptions": [m("gives_second", "The smaller solution is 30°. sin⁻¹(0.5) = 30°; the other solution 150° is larger.", 150, "gives the larger solution")],
  "guided_steps": [
    say("The calculator gives the first solution; the smaller one is asked for."),
    box("sin⁻¹(0.5) = ", 30, "The inverse sine of 0.5."),
    box("The second solution, by symmetry, is 180° − 30° = ", 150, "Reflect 30° in 180°.", phase=True),
    box("The smaller of 30° and 150° is ", 30, "Pick the smaller.", phase=True, done="Solutions 30° and 150°; the smaller is 30°.")
  ]},
 {  # S2 cos=0.5 smaller
  "display": "Solve \\(\\cos x = 0.5\\) for \\(0° \\le x \\le 360°\\). Give the smaller solution.",
  "solutions": [60], "calculator": True, "input_type": "single_value",
  "hint": "The calculator value is the smaller one here.",
  "misconceptions": [m("gives_second", "The smaller solution is 60°. cos⁻¹(0.5) = 60°; the other solution 300° is larger.", 300, "gives the larger solution")],
  "guided_steps": [
    say("Find the calculator value, then check which solution is smaller."),
    box("cos⁻¹(0.5) = ", 60, "The inverse cosine of 0.5."),
    box("The second solution is 360° − 60° = ", 300, "Reflect 60° in 360°.", phase=True),
    box("The smaller of 60° and 300° is ", 60, "Pick the smaller.", phase=True, done="Solutions 60° and 300°; the smaller is 60°.")
  ]},
 {  # S3 sin=0.5 second
  "display": "\\(\\sin x = 0.5\\). Give the second solution for \\(0° \\le x \\le 360°\\).",
  "solutions": [150], "calculator": True, "input_type": "single_value",
  "hint": "Use sine symmetry: 180° minus the first solution.",
  "misconceptions": [m("cos_symmetry", "For sine the second solution is 180° − 30° = 150°, not 360° − 30° = 330°. The 360° reflection is the rule for cosine.", 330, "uses cosine symmetry on sine")],
  "guided_steps": [
    say("The first solution is 30°; find the second by sine symmetry."),
    box("sin⁻¹(0.5) = ", 30, "The inverse sine of 0.5."),
    box("Sine is also positive in the second quadrant, so the second solution is 180° − 30° = ", 150, "Reflect 30° in 180°.", phase=True),
    box("So the second solution is ", 150, "One hundred and fifty.", phase=True, done="sin 150° = 0.5, the second solution.")
  ]},
 {  # S4 tan 0 (the kept zero)
  "display": "What is \\(\\tan 0°\\)?", "solutions": [0], "calculator": False,
  "input_type": "single_value", "hint": "The tangent curve starts at the origin.",
  "misconceptions": [m("thinks_undefined", "tan 0° = 0. The tangent curve passes through the origin; it is undefined at 90°, not at 0°.", None, "assumes an asymptote at 0")],
  "guided_steps": [
    say("The tangent curve starts at the origin. Build it from sine over cosine."),
    box("tan x = sin x ÷ cos x. At 0°, sin 0° = ", 0, "Sine starts at zero."),
    box("And cos 0° = ", 1, "Cosine starts at one.", phase=True),
    box("So tan 0° = 0 ÷ 1 = ", 0, "Zero divided by one.", phase=True, done="tan 0° = 0 ÷ 1 = 0.")
  ]},
 {  # S5 cos=-0.5 smaller
  "display": "\\(\\cos x = -0.5\\). Give the smaller solution for \\(0° \\le x \\le 360°\\).",
  "solutions": [120], "calculator": True, "input_type": "single_value",
  "hint": "cos is negative in the second and third quadrants.",
  "misconceptions": [m("gives_second", "cos is negative in Q2 and Q3: x = 180° − 60° = 120° and x = 180° + 60° = 240°. The smaller is 120°.", 240, "gives the larger solution")],
  "guided_steps": [
    say("cos is negative in the second and third quadrants. Find the reference angle first."),
    box("Ignoring the sign, cos⁻¹(0.5) = ", 60, "The inverse cosine of 0.5 is 60°."),
    box("In the second quadrant the solution is 180° − 60° = ", 120, "180 minus 60.", phase=True),
    box("The other solution is 180° + 60° = 240°, so the smaller is ", 120, "The smaller of 120 and 240.", phase=True, done="Solutions 120° and 240°; the smaller is 120°.")
  ]},
 {  # S6 cos=-0.5 larger (replaces sin 180=0 duplicate), chart
  "display": "\\(\\cos x = -0.5\\). Give the second (larger) solution for \\(0° \\le x \\le 360°\\).",
  "solutions": [240], "calculator": True, "input_type": "single_value",
  "hint": "cos is negative in the third quadrant too: 180° plus the reference angle.",
  "misconceptions": [m("gives_first", "The larger solution is 240°. 120° is the first (smaller) solution; the second is 180° + 60° = 240°.", 120, "gives the smaller solution")],
  "chart": chart(math.cos, 360, "y = cos x", kline=-0.5),
  "guided_steps": [
    say("The first solution is 120°; find the second in the third quadrant."),
    box("The reference angle is cos⁻¹(0.5) = ", 60, "The inverse cosine of 0.5."),
    box("In the third quadrant the solution is 180° + 60° = ", 240, "180 plus 60.", phase=True),
    box("So the larger solution is ", 240, "Two hundred and forty.", phase=True, done="cos 240° = −0.5, the larger solution.")
  ]},
 {  # S7 cos=0.5 larger (replaces cos 90=0 duplicate)
  "display": "\\(\\cos x = 0.5\\). Give the second (larger) solution for \\(0° \\le x \\le 360°\\).",
  "solutions": [300], "calculator": True, "input_type": "single_value",
  "hint": "Use cosine symmetry: 360° minus the first solution.",
  "misconceptions": [m("sine_symmetry", "For cosine the second solution is 360° − 60° = 300°, not 180° − 60° = 120°. The 180° reflection is the rule for sine.", 120, "uses sine symmetry on cosine")],
  "guided_steps": [
    say("The first solution is 60°; find the second by cosine symmetry."),
    box("cos⁻¹(0.5) = ", 60, "The inverse cosine of 0.5."),
    box("Cosine is also positive in the fourth quadrant, so the second solution is 360° − 60° = ", 300, "Reflect 60° in 360°.", phase=True),
    box("So the larger solution is ", 300, "Three hundred.", phase=True, done="cos 300° = 0.5, the larger solution.")
  ]},
]

# ---------------- GOLD (5) ----------------
gold = [
 {  # G1 sin=-0.5 smaller, chart
  "display": "Solve \\(\\sin x = -0.5\\) for \\(0° \\le x \\le 360°\\). Give the smaller solution.",
  "solutions": [210], "calculator": True, "input_type": "single_value",
  "hint": "sin is negative in the third and fourth quadrants.",
  "misconceptions": [
    m("wrong_quadrant", "sin is negative in Q3 and Q4: x = 180° + 30° = 210° and x = 360° − 30° = 330°. The smaller is 210°.", 330, "gives the larger solution"),
    m("forgets_sign", "The reference angle is 30°, but sin x = −0.5 is negative, so x is not 30°. The solutions are 210° and 330°.", 30, "ignores the negative sign")],
  "chart": chart(math.sin, 360, "y = sin x", kline=-0.5),
  "guided_steps": [
    say("sin is negative in the third and fourth quadrants. Start from the reference angle."),
    box("Ignoring the sign, sin⁻¹(0.5) = ", 30, "The inverse sine of 0.5 is 30°."),
    box("In the third quadrant the solution is 180° + 30° = ", 210, "180 plus 30.", phase=True),
    box("The other solution is 360° − 30° = 330°, so the smaller is ", 210, "The smaller of 210 and 330.", phase=True, done="Solutions 210° and 330°; the smaller is 210°.")
  ]},
 {  # G2 max 3sinx+2
  "display": "The maximum value of \\(3\\sin x + 2\\) is?", "solutions": [5], "calculator": False,
  "input_type": "single_value", "hint": "Use the largest value sin x can take.",
  "misconceptions": [
    m("uses_zero", "The maximum of sin x is 1, not 0. Maximum = 3(1) + 2 = 5.", 2, "puts sin x = 0"),
    m("forgets_shift", "Do not forget the + 2. Maximum = 3(1) + 2 = 5, not just 3 × 1.", 3, "forgets to add 2")],
  "guided_steps": [
    say("3 sin x + 2 is largest when sin x is largest."),
    box("The maximum value of sin x is ", 1, "Sine never exceeds 1."),
    box("So 3 sin x is at most 3 × 1 = ", 3, "3 times 1.", phase=True),
    box("Adding the 2: 3 + 2 = ", 5, "3 plus 2.", phase=True, done="Maximum of 3 sin x + 2 = 3(1) + 2 = 5.")
  ]},
 {  # G3 min 2cosx-1
  "display": "The minimum value of \\(2\\cos x - 1\\) is?", "solutions": [-3], "calculator": False,
  "input_type": "single_value", "hint": "Use the smallest value cos x can take.",
  "misconceptions": [
    m("uses_zero", "The minimum of cos x is −1, not 0. Minimum = 2(−1) − 1 = −3.", -1, "puts cos x = 0"),
    m("sign_slip", "cos x reaches −1, so 2(−1) − 1 = −2 − 1 = −3, not 2(1) − 1 = 1.", 1, "puts cos x = +1")],
  "guided_steps": [
    say("2 cos x − 1 is smallest when cos x is smallest."),
    box("The minimum value of cos x is ", -1, "Cosine bottoms out at minus one."),
    box("So 2 cos x is at least 2 × (−1) = ", -2, "2 times minus one.", phase=True),
    box("Subtracting 1: −2 − 1 = ", -3, "Minus two minus one.", phase=True, done="Minimum of 2 cos x − 1 = 2(−1) − 1 = −3.")
  ]},
 {  # G4 count sin=0.3 over 0-720, chart
  "display": "How many solutions does \\(\\sin x = 0.3\\) have for \\(0° \\le x \\le 720°\\)?",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Two solutions per full period; count the periods in the range.",
  "misconceptions": [m("one_period", "0° to 720° is two full periods. Each period gives 2 solutions, so 2 × 2 = 4, not 2.", 2, "counts only one period")],
  "chart": chart(math.sin, 720, "y = sin x", kline=0.3, xstep=180),
  "guided_steps": [
    say("Count solutions across the whole range by counting periods."),
    box("The period of sin x is 360°, so the number of full periods in 720° is 720 ÷ 360 = ", 2, "720 divided by 360."),
    box("The line y = 0.3 cuts each period of the sine wave this many times: ", 2, "A line between −1 and 1 meets each period twice.", phase=True),
    box("So the total number of solutions is 2 × 2 = ", 4, "2 times 2.", phase=True, done="2 solutions per period × 2 periods = 4.")
  ]},
 {  # G5 tan=1 smaller
  "display": "Solve \\(\\tan x = 1\\) for \\(0° \\le x \\le 360°\\). Give the smaller solution.",
  "solutions": [45], "calculator": True, "input_type": "single_value",
  "hint": "The calculator value is the first solution.",
  "misconceptions": [
    m("gives_second", "The smaller solution is 45°. tan⁻¹(1) = 45°; the second solution 45° + 180° = 225° is larger.", 225, "gives the larger solution"),
    m("sine_symmetry", "For tan, add the period 180° to reach the next solution, not 180° − 45° = 135°. tan 135° = −1, not 1.", 135, "uses sine symmetry on tangent")],
  "guided_steps": [
    say("tan has period 180°, so the second solution is 180° on from the first."),
    box("tan⁻¹(1) = ", 45, "The inverse tan of 1."),
    box("tan repeats every 180°, so the next solution is 45° + 180° = ", 225, "Add the period 180°.", phase=True),
    box("The smaller of 45° and 225° is ", 45, "Pick the smaller.", phase=True, done="Solutions 45° and 225°; the smaller is 45°.")
  ]},
]

problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Read an exact value or a basic feature straight off the sine, cosine or tangent curve.",
  "silver_description": "Use symmetry and quadrant signs to solve for angles beyond the first quadrant.",
  "gold_description": "Solve trigonometric equations across 0° to 360°, and find maxima, minima or the number of solutions."
}

# ---------------- tier_guides ----------------
def exstep(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d

tier_guides = {
 "bronze": {
   "title": "Bronze: read values off the curve",
   "steps": [
     "Picture the three graphs. <strong>Sine</strong> starts at 0, peaks at 1 (90°), back to 0 (180°), down to −1 (270°), back to 0 (360°).",
     "<strong>Cosine</strong> is the same wave but starts at 1. Both have period 360°. <strong>Tangent</strong> starts at 0 and repeats every 180°.",
     "Learn where each curve sits at 0°, 90°, 180° and 270°, and that sine and cosine only ever swing between −1 and 1."
   ],
   "example": {"question": "What is sin 90°?", "steps": [
     exstep("Locate", "<p>The sine curve climbs from the origin to its highest point.</p>"),
     exstep("Read", "<p>The peak is a quarter of the way along, at 90°.</p>"),
     exstep("Check", "<p>The sine curve passes through (90°, 1).</p>"),
     exstep("Answer", "<p>sin 90° = 1</p>", ans=True)]}
 },
 "silver": {
   "title": "Silver: use symmetry and signs",
   "steps": [
     "Beyond the first quadrant, find the <strong>reference angle</strong>: how far the angle sits from the nearest 0°, 180° or 360°.",
     "Take the exact value of that reference angle, then fix the sign. Sine is positive from 0° to 180°; cosine is positive from 0° to 90° and 270° to 360°.",
     "For a second solution, reflect: sine uses 180° − angle, cosine uses 360° − angle."
   ],
   "example": {"question": "What is cos 120°?", "steps": [
     exstep("Reference angle", "<p>180° − 120° = 60°.</p>"),
     exstep("Value", "<p>cos 60° = 0.5.</p>"),
     exstep("Sign", "<p>120° is in the second quadrant, where cosine is negative.</p>"),
     exstep("Answer", "<p>cos 120° = −0.5</p>", ans=True)]}
 },
 "gold": {
   "title": "Gold: solve across the full range",
   "steps": [
     "Use the calculator, or an exact value, for the <strong>first</strong> solution, the reference angle.",
     "Find the <strong>second</strong> by symmetry: sine 180° − angle, cosine 360° − angle, tangent add 180°.",
     "Read the question: it may want the smaller or larger solution, or how many there are. For a max or min, put sin or cos at plus or minus 1."
   ],
   "example": {"question": "Solve sin x = 0.5 for 0° ≤ x ≤ 360°.", "steps": [
     exstep("First solution", "<p>sin⁻¹(0.5) = 30°.</p>"),
     exstep("Second solution", "<p>Sine symmetry: 180° − 30° = 150°.</p>"),
     exstep("Check", "<p>sin 150° = 0.5 ✓</p>"),
     exstep("Answer", "<p>x = 30° and x = 150°</p>", ans=True)]}
 }
}

# ---------------- guided (opener + teach) ----------------
WHEEL_SVG = ('<svg viewBox="0 0 260 200" role="img" aria-label="A big wheel: centre 20 m above the ground, radius 15 m, one car marked at the side" style="max-width:260px">'
 '<line x1="10" y1="180" x2="250" y2="180" stroke="currentColor" stroke-width="1.5"/>'
 '<line x1="130" y1="90" x2="105" y2="180" stroke="currentColor" stroke-width="1.5"/>'
 '<line x1="130" y1="90" x2="155" y2="180" stroke="currentColor" stroke-width="1.5"/>'
 '<circle cx="130" cy="90" r="62" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
 '<circle cx="130" cy="90" r="2.5" fill="currentColor"/>'
 '<line x1="130" y1="90" x2="130" y2="28" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>'
 '<circle cx="130" cy="28" r="5" fill="#f59e0b" fill-opacity="0.5" stroke="currentColor" stroke-width="1.2"/>'
 '<circle cx="192" cy="90" r="5" fill="#f59e0b" fill-opacity="0.5" stroke="currentColor" stroke-width="1.2"/>'
 '<text x="136" y="86" font-family="Inter,sans-serif" font-size="10" fill="currentColor">centre 20 m</text>'
 '<text x="112" y="60" font-family="Inter,sans-serif" font-size="10" fill="currentColor">15 m</text>'
 '<text x="14" y="176" font-family="Inter,sans-serif" font-size="10" fill="currentColor">ground</text>'
 '</svg><span class="figure-caption">Diagram not drawn accurately</span><br>'
 'A big wheel turns. Its centre is 20 m above the ground and its radius is 15 m. One full turn takes 30 seconds.')

guided = {
 "opener": {
   "label": "Before any trig",
   "display": WHEEL_SVG,
   "steps": [
     {"say": "No trigonometry yet, just common sense about the wheel. Think about a car right at the bottom.",
      "pre": "The lowest a car gets, in metres, is ", "post": "", "answer": 5,
      "hint": "The centre is 20 m up; a car drops the 15 m radius below it."},
     {"say": None, "pre": "The highest a car gets, in metres, is ", "post": "", "answer": 35,
      "hint": "The centre is 20 m up; a car rises 15 m above it."},
     {"pre": "One full turn takes 30 s. After how many seconds is a car back at the same height, moving the same way? ",
      "post": "", "answer": 30, "hint": "A whole turn brings it right back to the start."},
     {"say": "Plot a car's height against time and you get a wave: up to 35 m, down to 5 m, repeating every 30 s. That wave is exactly the shape of \\(y = \\sin x\\). The middle line (20 m) acts like the x-axis, the 15 m swing is the <strong>amplitude</strong>, and the 30 s repeat is the <strong>period</strong>. Sine and cosine are just the maths of going round and round."}
   ]
 },
 "teach": {
   "bronze": {
     "display": "Read \\(\\cos 90°\\) from the cosine curve.",
     "label": "Together: read it off the curve",
     "steps": [
       say("Let us walk the cosine curve through its key heights, then read off 90°."),
       box("At x = 0° the cosine curve starts at its maximum, height ", 1, "Cosine starts at the top."),
       box("The cosine curve first reaches the x-axis a quarter of the way along, at x = ", 90, "A quarter of 360°."),
       box("At x = 90° the height of the cosine curve is ", 0, "It sits on the axis there."),
       box("So cos 90° = ", 0, "Read the height at 90°.", done="The cosine curve passes through (90°, 0), so cos 90° = 0. Reading key points is the whole skill.")
     ]
   },
   "silver": {
     "display": "What is \\(\\cos 240°\\)?",
     "label": "Together: reference angle and sign",
     "steps": [
       say("240° is in the third quadrant. Find the reference angle, take the exact value, then fix the sign."),
       box("Reference angle: 240° − 180° = ", 60, "How far past 180° the angle sits."),
       box("cos 60° = ", 0.5, "An exact value: cos 60° = 0.5."),
       box("Cosine is negative in the third quadrant, so cos 240° = ", -0.5, "Same size as cos 60°, but negative."),
       box("Check on the curve: the cosine wave is below the axis at 240°, so cos 240° = ", -0.5, "The value stays −0.5.", done="Reference angle 60°, third quadrant negative, gives −0.5.")
     ]
   },
   "gold": {
     "display": "Solve \\(\\cos x = 0\\) for \\(0° \\le x \\le 360°\\). Give the larger solution.",
     "label": "Together: find both, give the larger",
     "steps": [
       say("cos x = 0 where the cosine curve cuts the x-axis. Find both crossings, then give the larger."),
       box("The cosine curve first hits zero a quarter of the way along: a quarter of 360° = ", 90, "360 divided by 4."),
       box("It hits zero again three-quarters of the way along: (3 ÷ 4) × 360° = ", 270, "Three-quarters of 360."),
       box("The larger of 90° and 270° is ", 270, "Pick the bigger of the two."),
       box("Check: cos 270° = ", 0, "The cosine curve is on the axis at 270°.", done="cos 270° = 0, and 270° is the larger solution.")
     ]
   }
 }
}

# ---------------- method_card (slim) ----------------
method_card = {
 "title": "Trigonometric Graphs",
 "steps": [
   "Sine starts at 0, cosine starts at 1; both wave between −1 and 1 with period 360°.",
   "Tangent passes through 0, has period 180° and asymptotes at 90° and 270°.",
   "Exact values to know: sin 30° = 0.5, cos 60° = 0.5, tan 45° = 1.",
   "To solve sin x = k or cos x = k, take the reference angle, then use symmetry for the second solution."
 ],
 "content": "<p>The three curves repeat forever. <strong>Sine</strong> and <strong>cosine</strong> wave between −1 and 1 with period 360°; cosine is sine shifted left by 90°. <strong>Tangent</strong> climbs between asymptotes at 90° and 270°, with period 180°.</p><p>Beyond the first quadrant, use the <strong>reference angle</strong> and the sign for that quadrant. Solving \\(\\sin x = k\\) or \\(\\cos x = k\\) across 0° to 360° gives one calculator value and a second from symmetry.</p>",
 "example": "<p><strong>Solve \\(\\sin x = 0.5\\) for \\(0° \\le x \\le 360°\\).</strong></p><p>\\(\\sin^{-1}(0.5) = 30°\\). Sine is also positive in the second quadrant: \\(180° - 30° = 150°\\). So \\(x = 30°\\) or \\(x = 150°\\).</p>"
}

# ---------------- worked_examples (preserve, fix em dashes) ----------------
worked_examples = [
 {"steps": [exstep("Answer", "<p>\\(\\sin 90° = 1\\)</p>", ans=True)],
  "question": "What is the value of sin 90°?", "difficulty": "Bronze"},
 {"steps": [
   exstep("Step 1: First solution", "<p>\\(x = \\cos^{-1}(0.5) = 60°\\)</p>"),
   exstep("Step 2: Second solution", "<p>\\(x = 360° - 60° = 300°\\)</p>"),
   exstep("Answer", "<p>\\(x = 60°\\) and \\(x = 300°\\)</p>", ans=True)],
  "question": "Solve cos x = 0.5 for 0° ≤ x ≤ 360°. Give both solutions.", "difficulty": "Silver"},
 {"steps": [exstep("Answer", "<p>\\(\\tan 45° = 1\\)</p>", ans=True)],
  "question": "What is tan 45°?", "difficulty": "Gold"}
]

pd = {
 "method_card": method_card,
 "topic_links": {"prerequisites": []},
 "problem_bank": problem_bank,
 "related_videos": [],
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided
}

out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_graphs-L06.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# quick word-count report for tier_guides
def wc(s): return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
for t in ("bronze","silver","gold"):
    print(t, "tier_guide steps words:", sum(wc(s) for s in tier_guides[t]["steps"]))
print("wrote", out)
