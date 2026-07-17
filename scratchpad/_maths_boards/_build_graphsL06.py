# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion of maths-aqa graphs-L06 (Trigonometric Graphs)."""
import json, io, math, os

LIVE = "_live_graphs-L06.json"
live = json.load(io.open(LIVE, encoding="utf-8"))

# ---- preserve byte-for-byte ----
topic_links = live["topic_links"]
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]

# ---------------------------------------------------------------------------
# Chart helpers (sine / cosine over 0..360 degrees)
# ---------------------------------------------------------------------------
def curve_points(fn, step=15):
    pts = []
    x = 0
    while x <= 360.0001:
        y = fn(math.radians(x))
        pts.append({"x": x, "y": round(y, 4)})
        x += step
    return pts

def sin_curve(color="#3b82f6", label="y = sin x"):
    return {"type": "line", "data": curve_points(math.sin),
            "tension": 0.35, "fill": False, "borderColor": color,
            "pointRadius": 0, "label": label}

def cos_curve(color="#3b82f6", label="y = cos x"):
    return {"type": "line", "data": curve_points(math.cos),
            "tension": 0.35, "fill": False, "borderColor": color,
            "pointRadius": 0, "label": label}

def hline(k, label):
    return {"type": "line", "data": [{"x": 0, "y": k}, {"x": 360, "y": k}],
            "borderColor": "#9ca3af", "borderDash": [6, 4], "borderWidth": 1,
            "pointRadius": 0, "label": label}

def trig_options():
    return {"scales": {
        "x": {"min": 0, "max": 360, "ticks": {"stepSize": 90},
              "grid": {"color": "rgba(0,0,0,0.05)"},
              "title": {"text": "x (degrees)", "display": True}},
        "y": {"min": -1.2, "max": 1.2, "ticks": {"stepSize": 0.5},
              "grid": {"color": "rgba(0,0,0,0.08)"},
              "title": {"text": "y", "display": True}}}}

def chart(datasets):
    return {"type": "scatter", "data": {"datasets": datasets}, "options": trig_options()}

# ---------------------------------------------------------------------------
# Opener  (Ferris-wheel: centre 30 m, radius 25 m, one turn 40 s)
# ---------------------------------------------------------------------------
FERRIS_SVG = (
    '<svg viewBox="0 0 260 200" role="img" '
    'aria-label="A big wheel: centre 30 m above the ground, radius 25 m, one car marked at the side" '
    'style="max-width:260px">'
    '<line x1="10" y1="180" x2="250" y2="180" stroke="currentColor" stroke-width="1.5"/>'
    '<line x1="130" y1="90" x2="105" y2="180" stroke="currentColor" stroke-width="1.5"/>'
    '<line x1="130" y1="90" x2="155" y2="180" stroke="currentColor" stroke-width="1.5"/>'
    '<circle cx="130" cy="90" r="62" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
    '<circle cx="130" cy="90" r="2.5" fill="currentColor"/>'
    '<line x1="130" y1="90" x2="130" y2="28" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>'
    '<circle cx="130" cy="28" r="5" fill="#f59e0b" fill-opacity="0.5" stroke="currentColor" stroke-width="1.2"/>'
    '<circle cx="192" cy="90" r="5" fill="#f59e0b" fill-opacity="0.5" stroke="currentColor" stroke-width="1.2"/>'
    '<text x="136" y="86" font-family="Inter,sans-serif" font-size="10" fill="currentColor">centre 30 m</text>'
    '<text x="112" y="60" font-family="Inter,sans-serif" font-size="10" fill="currentColor">25 m</text>'
    '<text x="14" y="176" font-family="Inter,sans-serif" font-size="10" fill="currentColor">ground</text>'
    '</svg>'
    '<span class="figure-caption">Diagram not drawn accurately</span>'
)

opener = {
    "label": "Before any trig",
    "display": FERRIS_SVG +
        "<br>A big wheel turns. Its centre is 30 m above the ground and its "
        "radius is 25 m. One full turn takes 40 seconds.",
    "steps": [
        {"say": "No trigonometry yet, just common sense about the wheel. Think about a car right at the bottom.",
         "pre": "The lowest a car gets, in metres, is ", "post": "",
         "answer": 5, "hint": "The centre is 30 m up; a car drops by the 25 m radius below it."},
        {"say": None,
         "pre": "The highest a car gets, in metres, is ", "post": "",
         "answer": 55, "hint": "The centre is 30 m up; a car rises 25 m above it."},
        {"pre": "One full turn takes 40 s. After how many seconds is a car back at the same height, moving the same way? ",
         "post": "", "answer": 40,
         "hint": "A whole turn brings it right back to where it started."},
        {"say": "Plot a car's height against time and you get a wave: up to 55 m, down to 5 m, "
                "repeating every 40 s. That wave is exactly the shape of \\(y = \\sin x\\). The "
                "middle line (30 m) acts like the x-axis, the 25 m swing is the <strong>amplitude</strong>, "
                "and the 40 s repeat is the <strong>period</strong>. Sine and cosine are just the maths "
                "of going round and round."}
    ]
}

# ---------------------------------------------------------------------------
# Teach walks
# ---------------------------------------------------------------------------
teach = {
    "bronze": {
        "display": "Read \\(\\sin 180°\\) from the sine curve.",
        "label": "Together: read it off the curve",
        "steps": [
            {"say": "Let us walk the sine curve through its key heights, then read off 180°."},
            {"pre": "At x = 0° the sine curve starts on the axis, height ", "post": "",
             "answer": 0, "hint": "It passes through the origin."},
            {"pre": "At x = 90°, the peak, the height is ", "post": "",
             "answer": 1, "hint": "The maximum of sine is 1."},
            {"pre": "At x = 180° the curve is back on the axis, height ", "post": "",
             "answer": 0, "hint": "Halfway along, sine has returned to zero."},
            {"pre": "So sin 180° = ", "post": "", "answer": 0,
             "done": "The sine curve returns to 0 at 180°. Knowing the key points is the whole skill.",
             "hint": "Read the height at 180°."}
        ]
    },
    "silver": {
        "display": "What is \\(\\cos 240°\\)?",
        "label": "Together: reference angle and sign",
        "steps": [
            {"say": "240° is in the third quadrant. Find the reference angle, take the exact value, then fix the sign."},
            {"pre": "Reference angle: 240° − 180° = ", "post": "",
             "answer": 60, "hint": "How far past 180° the angle sits."},
            {"pre": "cos 60° = ", "post": "", "answer": 0.5,
             "hint": "An exact value: cos 60° = 0.5."},
            {"pre": "Cosine is negative in the third quadrant, so cos 240° = ", "post": "",
             "answer": -0.5, "hint": "Same size as cos 60°, but negative."},
            {"pre": "Check on the curve: the cosine wave is below the axis at 240°, so cos 240° = ", "post": "",
             "answer": -0.5,
             "done": "Reference angle 60°, third quadrant negative, gives −0.5.",
             "hint": "The value stays −0.5."}
        ]
    },
    "gold": {
        "display": "Solve \\(\\cos x = 0\\) for \\(0° \\leq x \\leq 360°\\). Give the larger solution.",
        "label": "Together: find both, give the larger",
        "steps": [
            {"say": "cos x = 0 where the cosine curve cuts the x-axis. Find both crossings, then give the larger."},
            {"pre": "The cosine curve first hits zero a quarter of the way along: a quarter of 360° = ", "post": "",
             "answer": 90, "hint": "360 divided by 4."},
            {"pre": "It hits zero again three-quarters of the way along: (3 ÷ 4) × 360° = ", "post": "",
             "answer": 270, "hint": "Three-quarters of 360."},
            {"pre": "The larger of 90° and 270° is ", "post": "", "answer": 270,
             "hint": "Pick the bigger of the two."},
            {"pre": "Check: cos 270° = ", "post": "", "answer": 0,
             "done": "cos 270° = 0 ✓, and 270° is the larger solution.",
             "hint": "The cosine curve is on the axis at 270°."}
        ]
    }
}

# ---------------------------------------------------------------------------
# tier_guides
# ---------------------------------------------------------------------------
tier_guides = {
    "bronze": {
        "title": "Bronze: read exact values off the curve",
        "steps": [
            "Picture the standard graphs. <strong>Sine</strong> starts at 0, rises to 1 at 90°, back to 0 at 180°, down to −1 at 270°, and back to 0 at 360°.",
            "<strong>Cosine</strong> is the same wave but starts at 1. Both have period 360°. <strong>Tangent</strong> starts at 0 and repeats every 180°.",
            "Memorise the key exact values: sin 30° = 0.5, cos 60° = 0.5, tan 45° = 1, plus the whole-number points at 0°, 90°, 180° and 270°."
        ],
        "example": {
            "question": "What is cos 90°?",
            "steps": [
                {"label": "Locate", "content": "<p>The cosine curve starts at 1 and falls, reaching zero a quarter of the way along.</p>"},
                {"label": "Read", "content": "<p>A quarter of 360° is 90°, where the curve sits on the x-axis.</p>"},
                {"label": "Check", "content": "<p>The cosine curve passes through (90°, 0).</p>"},
                {"label": "Answer", "content": "<p>cos 90° = 0</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: use symmetry and signs",
        "steps": [
            "Outside the first quadrant, find the <strong>reference angle</strong>: how far the angle sits from the nearest horizontal axis (0°, 180° or 360°).",
            "Take the exact value of that reference angle, then fix the sign. Sine is positive from 0° to 180°; cosine is positive from 0° to 90° and from 270° to 360°.",
            "For counting questions, sketch the line y = k across the wave and count how many times it cuts the curve between 0° and 360°."
        ],
        "example": {
            "question": "What is sin 150°?",
            "steps": [
                {"label": "Reference angle", "content": "<p>180° − 150° = 30°.</p>"},
                {"label": "Value", "content": "<p>sin 30° = 0.5.</p>"},
                {"label": "Sign", "content": "<p>150° is in the second quadrant, where sine is positive.</p>"},
                {"label": "Check", "content": "<p>The sine curve is symmetric about 90°, so sin 150° = sin 30°.</p>"},
                {"label": "Answer", "content": "<p>sin 150° = 0.5</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: solve equations across the full range",
        "steps": [
            "Use the calculator (or an exact value) for the <strong>first</strong> solution, the reference angle.",
            "Find the <strong>second</strong> solution by symmetry: for sine use 180° − angle, for cosine use 360° − angle, for tangent add 180°.",
            "Read the question carefully: it may want the larger solution, both values, or how many there are in the range."
        ],
        "example": {
            "question": "Solve cos x = 0.5 for 0° ≤ x ≤ 360°.",
            "steps": [
                {"label": "First solution", "content": "<p>cos⁻¹(0.5) = 60°.</p>"},
                {"label": "Second solution", "content": "<p>Cosine symmetry: 360° − 60° = 300°.</p>"},
                {"label": "Check", "content": "<p>cos 300° = 0.5 ✓</p>"},
                {"label": "Answer", "content": "<p>x = 60° and x = 300°</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# Problem bank
# ---------------------------------------------------------------------------
def M(pattern, message, expect, note=None):
    d = {"pattern": pattern, "message": message, "expect": expect}
    if note:
        d["note"] = note
    return d

bronze = [
    {   # B1 sin 90 = 1
        "display": "What is \\(\\sin 90°\\)?",
        "solutions": [1], "calculator": False, "input_type": "single_value",
        "hint": "Read the height at the very top of the sine curve.",
        "misconceptions": [
            M("confuse_cos", "sin 90° = 1, the maximum of the sine curve. cos 90° = 0; do not mix the two curves up.", 0,
              "slip: confuses sin 90 with cos 90")
        ],
        "guided_steps": [
            {"say": "The sine curve climbs from 0 to its highest point. Let us pin down that peak."},
            {"pre": "The sine curve starts at the origin, so at x = 0° its height is ", "post": "",
             "answer": 0, "hint": "It passes through (0, 0)."},
            {"phase": "substitute",
             "pre": "It reaches its maximum at x = 90°. The maximum value of sine is ", "post": "",
             "answer": 1, "hint": "Sine never goes above 1."},
            {"phase": "substitute", "pre": "So sin 90° = ", "post": "", "answer": 1,
             "done": "The peak of the sine curve sits at (90°, 1), so sin 90° = 1.",
             "hint": "Read the height at the top."}
        ]
    },
    {   # B2 sin 0 = 0
        "display": "What is \\(\\sin 0°\\)?",
        "solutions": [0], "calculator": False, "input_type": "single_value",
        "hint": "The sine curve begins on the x-axis.",
        "misconceptions": [
            M("confuse_cos", "sin 0° = 0; the sine curve starts on the axis. cos 0° = 1 starts at the top, so do not swap them.", 1,
              "slip: confuses sin 0 with cos 0")
        ],
        "guided_steps": [
            {"say": "sin 0° is where the sine curve begins. Read it from the graph."},
            {"pre": "The sine curve rises to a maximum of ", "post": "",
             "answer": 1, "hint": "The top of the wave is at height 1."},
            {"phase": "substitute",
             "pre": "But at the very start, x = 0°, the curve is on the x-axis, so its height is ", "post": "",
             "answer": 0, "hint": "It passes through the origin."},
            {"phase": "substitute", "pre": "So sin 0° = ", "post": "", "answer": 0,
             "done": "The sine curve starts at (0°, 0), so sin 0° = 0.",
             "hint": "Height at the origin is 0."}
        ]
    },
    {   # B3 sin 30 = 0.5
        "display": "What is \\(\\sin 30°\\)?",
        "solutions": [0.5], "calculator": False, "input_type": "single_value",
        "hint": "One of the exact values you must memorise.",
        "misconceptions": [
            M("wrong_exact", "sin 30° = 0.5 exactly. 0.866 is sin 60° (also cos 30°); the smaller angle gives the smaller value.", 0.866,
              "slip: confuses sin 30 with sin 60")
        ],
        "guided_steps": [
            {"say": "sin 30° is a key exact value. Build it from the maximum."},
            {"pre": "The maximum of sine, sin 90°, is ", "post": "",
             "answer": 1, "hint": "The top of the sine curve."},
            {"phase": "substitute",
             "pre": "sin 30° is exactly half of that maximum. Half of 1 = ", "post": "",
             "answer": 0.5, "hint": "1 divided by 2."},
            {"phase": "substitute", "pre": "So sin 30° = ", "post": "", "answer": 0.5,
             "done": "sin 30° = 0.5 is one of the exact values to memorise.",
             "hint": "0.5 exactly."}
        ]
    },
    {   # B4 period sin = 360
        "display": "What is the period of \\(y = \\sin x\\), in degrees?",
        "solutions": [360], "calculator": False, "input_type": "single_value",
        "hint": "How far along x before the wave repeats exactly.",
        "misconceptions": [
            M("confuse_tan_period", "sin repeats every 360°. 180° is the period of tan, not sin.", 180,
              "slip: uses tan period for sin")
        ],
        "guided_steps": [
            {"say": "The period is how far along x you travel before the wave repeats exactly."},
            {"pre": "The sine curve reaches its first peak at x = ", "post": "",
             "answer": 90, "hint": "The maximum is at 90°."},
            {"phase": "substitute",
             "pre": "It returns to the same height, moving the same way, after one full turn. A full turn is ", "post": "",
             "answer": 360, "hint": "Degrees in a whole turn, like once round a circle."},
            {"phase": "substitute", "pre": "So the period of y = sin x is ", "post": "", "answer": 360,
             "done": "sin repeats every 360°.", "hint": "A full turn is 360°."}
        ]
    },
    {   # B5 period tan = 180
        "display": "What is the period of \\(y = \\tan x\\), in degrees?",
        "solutions": [180], "calculator": False, "input_type": "single_value",
        "hint": "The tangent curve repeats sooner than sine and cosine.",
        "misconceptions": [
            M("assume_360", "tan repeats every 180°, not 360°. Its period is half that of sine and cosine.", 360,
              "slip: assumes same period as sin")
        ],
        "guided_steps": [
            {"say": "The tangent curve shoots up to an asymptote, then repeats sooner than a sine wave."},
            {"pre": "The tan curve has its first vertical asymptote at x = ", "post": "",
             "answer": 90, "hint": "tan is undefined at 90°."},
            {"phase": "substitute",
             "pre": "It repeats after only half a turn. Half of 360° = ", "post": "",
             "answer": 180, "hint": "360 divided by 2."},
            {"phase": "substitute", "pre": "So the period of y = tan x is ", "post": "", "answer": 180,
             "done": "tan repeats every 180°, twice as often as sin and cos.",
             "hint": "Half of 360 is 180."}
        ]
    },
    {   # B6 max at 90
        "display": "For \\(0° \\leq x \\leq 360°\\), at what value of \\(x\\) does \\(y = \\sin x\\) reach its maximum? Give your answer in degrees.",
        "solutions": [90], "calculator": False, "input_type": "single_value",
        "hint": "The question asks WHERE the wave is highest, not how high.",
        "misconceptions": [
            M("gives_value", "The question asks WHERE, so give the angle: x = 90°. The height there is 1, but that is not what was asked.", 1,
              "slip: gives the maximum value instead of its position")
        ],
        "guided_steps": [
            {"say": "We want WHERE the sine wave is highest, not how high it goes."},
            {"pre": "The maximum height of the sine curve is ", "post": "",
             "answer": 1, "hint": "Sine never exceeds 1."},
            {"phase": "substitute",
             "pre": "The curve first reaches that height a quarter of the way through a 360° cycle. A quarter of 360° = ", "post": "",
             "answer": 90, "hint": "360 divided by 4."},
            {"phase": "substitute", "pre": "So y = sin x is at its maximum when x = ", "post": "", "answer": 90,
             "done": "The peak sits at (90°, 1).", "hint": "Ninety degrees."}
        ]
    },
    {   # B7 crossings = 3  (CHART)
        "display": "For \\(0° \\leq x \\leq 360°\\), how many times does the graph of \\(y = \\sin x\\) cross the x-axis?",
        "solutions": [3], "calculator": False, "input_type": "single_value",
        "hint": "Count where the curve touches the x-axis, including the ends of the range.",
        "misconceptions": [
            M("miss_endpoint", "In 0° ≤ x ≤ 360° the curve is on the axis at 0°, 180° AND 360°, so there are 3 crossings. Missing an endpoint gives 2.", 2,
              "slip: forgets one endpoint"),
            M("interior_only", "Count all three points on the axis: 0°, 180°, 360°. Counting only 180° gives 1.", 1,
              "slip: counts only the interior crossing")
        ],
        "chart": chart([sin_curve()]),
        "guided_steps": [
            {"say": "Count where the sine curve cuts the x-axis between 0° and 360° inclusive."},
            {"pre": "It starts on the axis at x = 0°, that is crossing number ", "post": "",
             "answer": 1, "hint": "The start counts."},
            {"phase": "substitute",
             "pre": "It comes back to the axis at x = 180°, crossing number ", "post": "",
             "answer": 2, "hint": "Halfway along the range."},
            {"phase": "substitute",
             "pre": "It finishes on the axis at x = 360°, crossing number ", "post": "",
             "answer": 3, "hint": "The end counts too."},
            {"phase": "substitute", "pre": "So the number of crossings is ", "post": "", "answer": 3,
             "done": "Crossings at 0°, 180° and 360°, that is 3.",
             "hint": "Count them: 0, 180, 360."}
        ]
    },
    {   # B8 cos 180 = -1
        "display": "What is \\(\\cos 180°\\)?",
        "solutions": [-1], "calculator": False, "input_type": "single_value",
        "hint": "Track the cosine curve from the top down to 180°.",
        "misconceptions": [
            M("forgets_sign", "cos 180° = −1, the bottom of the curve. It returns to +1 only at 360°.", 1,
              "slip: forgets the negative sign")
        ],
        "guided_steps": [
            {"say": "The cosine curve starts at the top and falls. Track it to 180°."},
            {"pre": "At x = 0° the cosine curve is at its maximum, cos 0° = ", "post": "",
             "answer": 1, "hint": "Cosine starts at the top."},
            {"phase": "substitute",
             "pre": "By x = 180° it has fallen to its minimum. The minimum value of cosine is ", "post": "",
             "answer": -1, "hint": "Cosine bottoms out at minus one."},
            {"phase": "substitute", "pre": "So cos 180° = ", "post": "", "answer": -1,
             "done": "The cosine curve reaches its lowest point, −1, at 180°.",
             "hint": "Minus one."}
        ]
    }
]

silver = [
    {   # S1 sin 150 = 0.5
        "display": "What is \\(\\sin 150°\\)?",
        "solutions": [0.5], "calculator": False, "input_type": "single_value",
        "hint": "150° is in the second quadrant. Use the symmetry of the sine curve.",
        "misconceptions": [
            M("wrong_sign", "sin 150° = +0.5. Sine is positive in the second quadrant (0° to 180°), so it does not turn negative here.", -0.5,
              "slip: makes it negative")
        ],
        "guided_steps": [
            {"say": "150° is in the second quadrant, where sine is still positive. Use symmetry about 90°."},
            {"pre": "The reference angle is 180° − 150° = ", "post": "",
             "answer": 30, "hint": "How far 150° sits from 180°."},
            {"phase": "substitute",
             "pre": "So sin 150° equals sin 30°, which is ", "post": "",
             "answer": 0.5, "hint": "The exact value of sin 30°."},
            {"phase": "substitute", "pre": "So sin 150° = ", "post": "", "answer": 0.5,
             "done": "sin 150° = sin 30° = 0.5 by the symmetry of the sine curve.",
             "hint": "Same as sin 30°."}
        ]
    },
    {   # S2 cos 120 = -0.5
        "display": "What is \\(\\cos 120°\\)?",
        "solutions": [-0.5], "calculator": False, "input_type": "single_value",
        "hint": "120° is in the second quadrant, where cosine is negative.",
        "misconceptions": [
            M("forgets_sign", "cos 120° = −0.5. Cosine is negative between 90° and 270°, so the sign matters.", 0.5,
              "slip: forgets the negative sign")
        ],
        "guided_steps": [
            {"say": "120° is in the second quadrant, where cosine is negative. Find the reference angle first."},
            {"pre": "The reference angle is 180° − 120° = ", "post": "",
             "answer": 60, "hint": "How far 120° sits from 180°."},
            {"phase": "substitute",
             "pre": "The exact value cos 60° = ", "post": "",
             "answer": 0.5, "hint": "An exact value: cos 60° = 0.5."},
            {"phase": "substitute",
             "pre": "Cosine is negative in the second quadrant, so cos 120° = ", "post": "",
             "answer": -0.5,
             "done": "Reference angle 60° gives 0.5; the second quadrant makes it −0.5.",
             "hint": "Same size as cos 60°, but negative."}
        ]
    },
    {   # S3 tan 180 = 0
        "display": "What is \\(\\tan 180°\\)?",
        "solutions": [0], "calculator": False, "input_type": "single_value",
        "hint": "The tangent curve passes through zero at the start of each cycle.",
        "misconceptions": [
            M("thinks_undefined", "tan 180° = 0, not undefined. The asymptotes are at 90° and 270°, where tan shoots off, but 180° sits on the axis.", None,
              "slip: assumes an asymptote at 180")
        ],
        "guided_steps": [
            {"say": "The tangent curve passes through zero at the start of each 180° cycle."},
            {"pre": "tan 0° = ", "post": "",
             "answer": 0, "hint": "The tan curve starts at the origin."},
            {"phase": "substitute",
             "pre": "tan has period 180°, so tan 180° equals tan 0°, which is ", "post": "",
             "answer": 0, "hint": "One full tan cycle later, it is back to the same value."},
            {"phase": "substitute", "pre": "So tan 180° = ", "post": "", "answer": 0,
             "done": "tan 180° = tan 0° = 0, since tan repeats every 180°.",
             "hint": "Zero."}
        ]
    },
    {   # S4 sin 270 = -1
        "display": "What is \\(\\sin 270°\\)?",
        "solutions": [-1], "calculator": False, "input_type": "single_value",
        "hint": "270° is three-quarters of the way round, at the bottom of the sine wave.",
        "misconceptions": [
            M("wrong_sign", "sin 270° = −1, the minimum. The maximum +1 is at 90°, not 270°.", 1,
              "slip: confuses minimum with maximum")
        ],
        "guided_steps": [
            {"say": "270° is three-quarters of the way round, at the bottom of the sine wave."},
            {"pre": "Three-quarters of a full 360° cycle is (3 ÷ 4) × 360° = ", "post": "",
             "answer": 270, "hint": "Three-quarters of 360."},
            {"phase": "substitute",
             "pre": "At that point the sine curve is at its lowest. The minimum value of sine is ", "post": "",
             "answer": -1, "hint": "Sine bottoms out at minus one."},
            {"phase": "substitute", "pre": "So sin 270° = ", "post": "", "answer": -1,
             "done": "The sine curve reaches its minimum, −1, at 270°.",
             "hint": "Minus one."}
        ]
    },
    {   # S5 cos x = 0 first = 90  (CHART)
        "display": "Solve \\(\\cos x = 0\\) for \\(0° \\leq x \\leq 360°\\). Give the first (smaller) value.",
        "solutions": [90], "calculator": False, "input_type": "single_value",
        "hint": "Where does the cosine curve first cross the x-axis?",
        "misconceptions": [
            M("gives_second", "The first crossing is 90°. Cosine is also zero at 270°, but the question asks for the first (smaller) value.", 270,
              "slip: gives the second crossing")
        ],
        "chart": chart([cos_curve()]),
        "guided_steps": [
            {"say": "cos x = 0 where the cosine curve crosses the x-axis. Find the first such angle."},
            {"pre": "The cosine curve starts at its maximum, cos 0° = ", "post": "",
             "answer": 1, "hint": "Cosine starts at the top."},
            {"phase": "substitute",
             "pre": "It first drops to zero a quarter of a cycle later. A quarter of 360° = ", "post": "",
             "answer": 90, "hint": "360 divided by 4."},
            {"phase": "substitute", "pre": "So the first solution of cos x = 0 is x = ", "post": "", "answer": 90,
             "done": "cos x = 0 at 90° and again at 270°; the first is 90°.",
             "hint": "Ninety degrees."}
        ]
    },
    {   # S6 cos x = -1 = 180
        "display": "Solve \\(\\cos x = -1\\) for \\(0° \\leq x \\leq 360°\\).",
        "solutions": [180], "calculator": False, "input_type": "single_value",
        "hint": "cos x = −1 happens at the very bottom of the cosine curve.",
        "misconceptions": [
            M("confuse_max", "cos x = −1 at x = 180°, the bottom of the curve. cos 0° = +1 is the top, so 0° is wrong.", 0,
              "slip: confuses the minimum with the maximum")
        ],
        "guided_steps": [
            {"say": "cos x = −1 happens at the very bottom of the cosine curve."},
            {"pre": "The minimum value of the cosine curve is ", "post": "",
             "answer": -1, "hint": "Cosine bottoms out at minus one."},
            {"phase": "substitute",
             "pre": "It reaches that minimum halfway through the cycle. Half of 360° = ", "post": "",
             "answer": 180, "hint": "360 divided by 2."},
            {"phase": "substitute", "pre": "So cos x = −1 when x = ", "post": "", "answer": 180,
             "done": "The cosine curve reaches −1 exactly once in the range, at 180°.",
             "hint": "One hundred and eighty."}
        ]
    },
    {   # S7 count cos x = 0.5 -> 2  (CHART)
        "display": "How many solutions does \\(\\cos x = 0.5\\) have for \\(0° \\leq x \\leq 360°\\)?",
        "solutions": [2], "calculator": False, "input_type": "single_value",
        "hint": "Draw the line y = 0.5 across the cosine curve and count the crossings.",
        "misconceptions": [
            M("stops_at_one", "There are 2 solutions: 60° and 300°. Stopping at the calculator value 60° misses the second one.", 1,
              "slip: only finds the first solution")
        ],
        "chart": chart([cos_curve(), hline(0.5, "y = 0.5")]),
        "guided_steps": [
            {"say": "Draw the line y = 0.5 across the cosine curve and count the crossings between 0° and 360°."},
            {"pre": "The exact value cos 60° = 0.5, so one solution is x = ", "post": "",
             "answer": 60, "hint": "An exact value: cos 60° = 0.5."},
            {"phase": "substitute",
             "pre": "By symmetry there is a second, in the fourth quadrant, at 360° − 60° = ", "post": "",
             "answer": 300, "hint": "Reflect 60° in 360°."},
            {"phase": "substitute", "pre": "That is two crossings, so the number of solutions is ", "post": "", "answer": 2,
             "done": "cos x = 0.5 at 60° and 300°: 2 solutions.",
             "hint": "Count them: 60° and 300°."}
        ]
    }
]

gold = [
    {   # G1 sin x = 0.5 larger = 150  (CHART)
        "display": "Solve \\(\\sin x = 0.5\\) for \\(0° \\leq x \\leq 360°\\). Give the larger solution.",
        "solutions": [150], "calculator": True, "input_type": "single_value",
        "hint": "Find the first solution, then use sine symmetry (180° − angle) for the second.",
        "misconceptions": [
            M("first_only", "The larger solution is 150°. 30° is the calculator value; the second solution is 180° − 30° = 150°.", 30,
              "slip: gives the calculator value")
        ],
        "chart": chart([sin_curve(), hline(0.5, "y = 0.5")]),
        "guided_steps": [
            {"say": "Two solutions lie in the range. Find the first with the calculator, the second by symmetry, and give the larger."},
            {"pre": "sin⁻¹(0.5) = ", "post": "",
             "answer": 30, "hint": "The inverse sine of 0.5."},
            {"phase": "substitute",
             "pre": "Sine is also positive in the second quadrant, so the other solution is 180° − 30° = ", "post": "",
             "answer": 150, "hint": "Reflect 30° in 180°."},
            {"phase": "substitute", "pre": "The larger of 30° and 150° is ", "post": "", "answer": 150,
             "done": "Solutions 30° and 150°; the larger is 150°.",
             "hint": "Pick the bigger value."}
        ]
    },
    {   # G2 cos x = 0.5 larger = 300
        "display": "Solve \\(\\cos x = 0.5\\) for \\(0° \\leq x \\leq 360°\\). Give the larger solution.",
        "solutions": [300], "calculator": True, "input_type": "single_value",
        "hint": "Find the first solution, then use cosine symmetry (360° − angle) for the second.",
        "misconceptions": [
            M("first_only", "The larger solution is 300°. 60° is the calculator value; the second solution is 360° − 60° = 300°.", 60,
              "slip: gives the calculator value"),
            M("sine_symmetry", "For cosine the second solution is 360° − 60° = 300°, not 180° − 60° = 120°. The 180° reflection is the rule for sine.", 120,
              "slip: uses sine symmetry on cosine")
        ],
        "guided_steps": [
            {"say": "Find the first solution, then use cosine symmetry about 360°, and give the larger."},
            {"pre": "cos⁻¹(0.5) = ", "post": "",
             "answer": 60, "hint": "The inverse cosine of 0.5."},
            {"phase": "substitute",
             "pre": "Cosine is also positive in the fourth quadrant, so the other solution is 360° − 60° = ", "post": "",
             "answer": 300, "hint": "Reflect 60° in 360°."},
            {"phase": "substitute", "pre": "The larger of 60° and 300° is ", "post": "", "answer": 300,
             "done": "Solutions 60° and 300°; the larger is 300°.",
             "hint": "Pick the bigger value."}
        ]
    },
    {   # G3 tan x = 1 larger = 225
        "display": "Solve \\(\\tan x = 1\\) for \\(0° \\leq x \\leq 360°\\). Give the larger solution.",
        "solutions": [225], "calculator": True, "input_type": "single_value",
        "hint": "tan has period 180°, so add 180° to the first solution.",
        "misconceptions": [
            M("first_only", "The larger solution is 225°. 45° is the calculator value; add the period 180° to reach 225°.", 45,
              "slip: gives the calculator value"),
            M("sine_symmetry", "For tan, add the period 180° to get 225°, not 180° − 45° = 135°. tan 135° = −1, not 1.", 135,
              "slip: uses sine symmetry on tangent")
        ],
        "guided_steps": [
            {"say": "tan has period 180°, so the second solution is a straight 180° on from the first. Give the larger."},
            {"pre": "tan⁻¹(1) = ", "post": "",
             "answer": 45, "hint": "The inverse tan of 1."},
            {"phase": "substitute",
             "pre": "tan repeats every 180°, so the next solution is 45° + 180° = ", "post": "",
             "answer": 225, "hint": "Add the period, 180°."},
            {"phase": "substitute", "pre": "The larger of 45° and 225° is ", "post": "", "answer": 225,
             "done": "Solutions 45° and 225°; the larger is 225°.",
             "hint": "Pick the bigger value."}
        ]
    },
    {   # G4 sin 210 = -0.5
        "display": "What is \\(\\sin 210°\\)?",
        "solutions": [-0.5], "calculator": False, "input_type": "single_value",
        "hint": "210° is in the third quadrant, where sine is negative. Use the reference angle.",
        "misconceptions": [
            M("forgets_sign", "sin 210° = −0.5. Sine is negative in the third quadrant (180° to 270°), so the sign is essential.", 0.5,
              "slip: forgets the negative sign")
        ],
        "guided_steps": [
            {"say": "210° is in the third quadrant, where sine is negative. Use the reference angle."},
            {"pre": "The reference angle is 210° − 180° = ", "post": "",
             "answer": 30, "hint": "How far past 180° the angle sits."},
            {"phase": "substitute",
             "pre": "The exact value sin 30° = ", "post": "",
             "answer": 0.5, "hint": "An exact value: sin 30° = 0.5."},
            {"phase": "substitute",
             "pre": "Sine is negative in the third quadrant, so sin 210° = ", "post": "",
             "answer": -0.5,
             "done": "Reference angle 30° gives 0.5; the third quadrant makes it −0.5.",
             "hint": "Same size as sin 30°, but negative."}
        ]
    },
    {   # G5 cos 300 = 0.5
        "display": "What is \\(\\cos 300°\\)?",
        "solutions": [0.5], "calculator": False, "input_type": "single_value",
        "hint": "300° is in the fourth quadrant, where cosine is positive. Use the reference angle.",
        "misconceptions": [
            M("wrong_sign", "cos 300° = +0.5. Cosine is positive in the fourth quadrant (270° to 360°), so it does not turn negative.", -0.5,
              "slip: makes it negative")
        ],
        "guided_steps": [
            {"say": "300° is in the fourth quadrant, where cosine is positive. Use the reference angle."},
            {"pre": "The reference angle is 360° − 300° = ", "post": "",
             "answer": 60, "hint": "How far 300° sits from 360°."},
            {"phase": "substitute",
             "pre": "The exact value cos 60° = ", "post": "",
             "answer": 0.5, "hint": "An exact value: cos 60° = 0.5."},
            {"phase": "substitute",
             "pre": "Cosine is positive in the fourth quadrant, so cos 300° = ", "post": "",
             "answer": 0.5,
             "done": "Reference angle 60° gives 0.5, and cosine is positive here, so cos 300° = 0.5.",
             "hint": "Positive one half."}
        ]
    }
]

problem_bank = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "Read an exact value or a basic feature straight off the sine, cosine or tangent curve.",
    "silver_description": "Use symmetry, reference angles and signs to reach values beyond the first quadrant, and count solutions.",
    "gold_description": "Solve trigonometric equations across 0° to 360°, giving the second solution or the value the question asks for."
}

# ---------------------------------------------------------------------------
# method_card (slim reference; <=4 steps, content <=140 words)
# ---------------------------------------------------------------------------
method_card = {
    "title": "Trigonometric Graphs (sin, cos, tan)",
    "steps": [
        "Know the shapes: sine starts at 0, cosine starts at 1, both wave between −1 and 1 with period 360°.",
        "Tangent passes through 0, has period 180° and asymptotes at 90° and 270°.",
        "Learn the exact values: sin 30° = 0.5, cos 60° = 0.5, tan 45° = 1, plus the points at 0° and 90°.",
        "To solve an equation, find the reference angle, then use symmetry for the second solution in the range."
    ],
    "content": "<p>The three curves repeat forever. <strong>Sine</strong> and <strong>cosine</strong> wave smoothly between −1 and 1 with period 360°; cosine is sine shifted left by 90°. <strong>Tangent</strong> climbs from −∞ to +∞ between asymptotes at 90° and 270°, with period 180°.</p><p>Beyond the first quadrant, use the <strong>reference angle</strong> and the sign for that quadrant. To solve \\(\\sin x = k\\) or \\(\\cos x = k\\) across 0° to 360°, one answer comes from the calculator and the second from symmetry.</p>",
    "example": "<p><strong>Solve \\(\\sin x = 0.5\\) for \\(0° \\leq x \\leq 360°\\).</strong></p><p>\\(\\sin^{-1}(0.5) = 30°\\). Sine is also positive in the second quadrant: \\(180° - 30° = 150°\\). So \\(x = 30°\\) or \\(x = 150°\\).</p>"
}

# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------
pd = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": problem_bank,
    "related_videos": related_videos,
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach}
}

out = "lesson_maths-aqa_graphs-L06.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, indent=2, ensure_ascii=False))
print("wrote", out)
# quick self-check: em dash scan
s = json.dumps(pd, ensure_ascii=False)
print("EM DASH present:", "—" in s)
print("bronze sols:", [p["solutions"] for p in bronze])
print("silver sols:", [p["solutions"] for p in silver])
print("gold sols:", [p["solutions"] for p in gold])
