# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_graphs-L06.json", encoding="utf-8"))

# ---- preserved verbatim ----
topic_links = live["topic_links"]
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]
# Hard style rule: no em dashes in student-facing strings. The preserved
# worked_examples use " — " in step labels; swap for a colon (only change).
for _we in worked_examples:
    for _st in _we.get("steps", []):
        if isinstance(_st.get("label"), str):
            _st["label"] = _st["label"].replace(" — ", ": ").replace("—", ":")

# ---- method_card (slim) ----
method_card = {
    "title": "How to Work with Trigonometric Graphs",
    "steps": [
        "Know the three shapes: sin starts at 0, cos starts at 1, tan starts at 0 with asymptotes.",
        "sin and cos swing between −1 and 1 (amplitude 1) and repeat every 360°; tan repeats every 180°.",
        "To solve an equation, read where the wave reaches the required height, then use symmetry for the second solution.",
        "Sine's second solution is 180° − first; cosine's is 360° − first.",
    ],
    "content": "<p>The three trig graphs are waves you read like a map. <strong>\\(y=\\sin x\\)</strong> starts at 0, peaks at 1 (90°), returns to 0 (180°), dips to −1 (270°) and back to 0 (360°). <strong>\\(y=\\cos x\\)</strong> is the same wave starting at 1. Both have amplitude 1 and period 360°. <strong>\\(y=\\tan x\\)</strong> starts at 0, has period 180°, and shoots to infinity at asymptotes (90°, 270°, and so on).</p><p>To solve \\(\\sin x = k\\), find the principal value, then use symmetry: sine repeats a height at \\(180° - x\\), cosine at \\(360° - x\\).</p>",
    "example": "<p><strong>Solve \\(\\sin x = 0.5\\) for \\(0° \\leq x \\leq 360°\\)</strong></p><p><strong>Step 1:</strong> The principal value is \\(x = \\sin^{-1}(0.5) = 30°\\).</p><p><strong>Step 2:</strong> The sine graph is positive in the 1st and 2nd quadrants. The second solution is \\(180° - 30° = 150°\\).</p><p><strong>Answer:</strong> \\(x = 30°\\) and \\(x = 150°\\).</p>",
}

# ---- BRONZE ----
bronze = [
    {  # 0 : cos 0 = 1  (value 1)
        "display": "What is the value of \\(\\cos 0°\\)?",
        "solutions": [1],
        "calculator": False,
        "input_type": "single_value",
        "hint": "The cosine graph starts at its highest point.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 0,
             "message": "cos starts at 1 (not 0). It is sin that starts at 0."}
        ],
        "guided_steps": [
            {"say": "Picture the cosine wave. Step round from 0° in ninety-degree jumps, reading the height each time."},
            {"pre": "cos falls to the middle line at 90°. cos 90° = ", "post": "", "answer": 0,
             "hint": "Cosine crosses zero at 90°."},
            {"pre": "It keeps falling to the bottom at 180°. cos 180° = ", "post": "", "answer": -1,
             "hint": "Cosine bottoms out at 180°."},
            {"phase": "substitute", "say": "Back to the question. The wave BEGINS at its highest point, so read the height right at 0°.",
             "pre": "cos 0° = ", "post": "", "answer": 1, "hint": "Cosine starts at the very top, its maximum of 1."},
            {"pre": "Check with symmetry: a full turn returns to the start, so cos 360° = ", "post": "", "answer": 1,
             "done": "Same peak height at 0° and 360°, both 1. So cos 0° = 1.",
             "hint": "A full turn brings cosine back to its start."},
        ],
    },
    {  # 1 : period of tan = 180  (CHANGED from sin 0)
        "display": "What is the period of \\(y = \\tan x\\) in degrees?",
        "solutions": [180],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Count how many degrees before the tangent graph repeats itself.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 360,
             "message": "sin and cos have period 360°, but tan repeats twice as often, every 180°."}
        ],
        "guided_steps": [
            {"say": "The period is how far along you go before the graph repeats exactly. Trace tan and spot the repeat."},
            {"pre": "tan has its first asymptote at ", "post": "°", "answer": 90,
             "hint": "Tan is undefined at 90°."},
            {"pre": "Just after 90° it climbs from far below and crosses zero again at ", "post": "°", "answer": 180,
             "hint": "Tan is back on the axis at 180°."},
            {"phase": "substitute", "say": "At 180° the graph looks exactly as it did at 0°: the whole pattern has repeated. The period is that repeat distance.",
             "pre": "period = ", "post": "°", "answer": 180, "hint": "The gap from one repeat to the next is 180°."},
            {"pre": "Check: the next asymptote should be 90 + 180 = ", "post": "°", "answer": 270,
             "done": "Asymptotes 180° apart confirm the period is 180°.",
             "hint": "Add one period to the first asymptote at 90°."},
        ],
    },
    {  # 2 : sin 270 = -1  (value -1)
        "display": "What is the value of \\(\\sin 270°\\)?",
        "solutions": [-1],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Trace the sine wave round to 270°, the lowest point.",
        "misconceptions": [
            {"check": "common", "pattern": "sign_error", "expect": 1,
             "message": "At 270°, sin reaches its minimum value of −1, not +1."}
        ],
        "guided_steps": [
            {"say": "Walk the sine wave round from 0° in ninety-degree steps, reading the height."},
            {"pre": "sin 0° (the start) = ", "post": "", "answer": 0, "hint": "Sine starts on the middle line."},
            {"pre": "sin 90° (the peak) = ", "post": "", "answer": 1, "hint": "Sine reaches its maximum at 90°."},
            {"pre": "sin 180° (back to the middle) = ", "post": "", "answer": 0, "hint": "Sine returns to zero at 180°."},
            {"phase": "substitute", "say": "One more quarter-turn to 270°, the lowest point of the wave.",
             "pre": "sin 270° = ", "post": "", "answer": -1, "hint": "Sine reaches its minimum, −1, at 270°."},
            {"pre": "Check: a full turn returns to the start, so sin 360° = ", "post": "", "answer": 0,
             "done": "Back to 0 after a full turn, with the dip to −1 at 270°. So sin 270° = −1.",
             "hint": "Sine is back to zero after 360°."},
        ],
    },
    {  # 3 : mc period of sin = 360 (index 3)
        "display": "What is the period of \\(y = \\sin x\\)?",
        "options": ["90°", "180°", "270°", "360°"],
        "solutions": [3],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Count the degrees before the sine wave repeats.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 1,
             "message": "Sin and cos both have period 360°. Only tan has period 180°."}
        ],
    },
    {  # 4 : angle where sin is minimum = 270  (CHANGED from cos 180)
        "display": "At which angle does \\(\\sin x\\) reach its minimum for \\(0° \\leq x \\leq 360°\\)?",
        "solutions": [270],
        "calculator": False,
        "input_type": "single_value",
        "hint": "The minimum of the sine wave is a quarter-turn past 180°.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 90,
             "message": "90° is where sine is at its MAXIMUM. Its minimum, the lowest dip, is at 270°."}
        ],
        "guided_steps": [
            {"say": "The minimum is the lowest point of the sine wave. Trace round to find where the graph dips lowest."},
            {"pre": "Sine starts at 0 and reaches its maximum at ", "post": "°", "answer": 90,
             "hint": "Sine is highest at 90°."},
            {"pre": "It falls back to zero at ", "post": "°", "answer": 180, "hint": "Sine crosses zero again at 180°."},
            {"phase": "substitute", "say": "It keeps falling below the line. The very bottom of the dip is one more quarter-turn on.",
             "pre": "lowest point at ", "post": "°", "answer": 270, "hint": "The minimum sits at 270°, opposite the peak."},
            {"pre": "Check the height there: sin 270° = ", "post": "", "answer": -1,
             "done": "Height −1 at 270° is the lowest sine ever gets, so the minimum is at 270°.",
             "hint": "At the minimum the height is −1."},
        ],
    },
    {  # 5 : tan 0 = 0  (value 0)  -- AUDIT message fix
        "display": "What is the value of \\(\\tan 0°\\)?",
        "solutions": [0],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Use tan = sin divided by cos at 0°.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 1,
             "message": "A common error is writing tan 0° = 1. Remember tan x = sin x ÷ cos x, so tan 0° = sin 0° ÷ cos 0° = 0 ÷ 1 = 0, not 1."}
        ],
        "guided_steps": [
            {"say": "Use the rule tan x = sin x ÷ cos x. Work out the top and the bottom at 0°, then divide."},
            {"pre": "sin 0° = ", "post": "", "answer": 0, "hint": "Sine starts at zero."},
            {"pre": "cos 0° = ", "post": "", "answer": 1, "hint": "Cosine starts at its maximum, 1."},
            {"phase": "substitute", "say": "Now divide the top by the bottom.",
             "pre": "tan 0° = 0 ÷ 1 = ", "post": "", "answer": 0, "hint": "Zero divided by anything is zero."},
            {"pre": "Check on the tan graph: it passes through the origin, so at 0° its height is ", "post": "", "answer": 0,
             "done": "The graph goes through (0, 0), confirming tan 0° = 0. It is NOT 1.",
             "hint": "The tan curve starts at the origin."},
        ],
    },
    {  # 6 : first asymptote of tan = 90
        "display": "At which angle does \\(y = \\tan x\\) have its first asymptote (for \\(x > 0°\\))?",
        "solutions": [90],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Tan blows up where cosine equals zero.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 180,
             "message": "The graph passes through zero at 180°, but it shoots off to infinity (the asymptote) a quarter-turn earlier, at 90°, where cos = 0."}
        ],
        "guided_steps": [
            {"say": "tan x = sin x ÷ cos x. Dividing by zero is impossible, so tan explodes wherever cos x = 0. Find that angle."},
            {"pre": "cos 0° = ", "post": "", "answer": 1, "hint": "Cosine starts at 1, not zero."},
            {"phase": "substitute", "say": "Step on: cosine falls and first reaches zero a quarter-turn later.",
             "pre": "cos x = 0 first at x = ", "post": "°", "answer": 90, "hint": "Cosine is zero at 90°."},
            {"pre": "So tan is undefined there. Confirm: the next place cos = 0 (the next asymptote) is at ", "post": "°", "answer": 270,
             "done": "cos = 0 at 90° and 270°, so the first asymptote of tan is at 90°.",
             "hint": "Cosine is zero again at 270°."},
        ],
    },
    {  # 7 : x where tan first = 1  => 45  (CHANGED from amplitude)
        "display": "At which angle does \\(\\tan x\\) first equal 1 (for \\(x > 0°\\))?",
        "solutions": [45],
        "calculator": False,
        "input_type": "single_value",
        "hint": "tan equals 1 where sine and cosine are equal.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 90,
             "message": "At 90° tan is undefined (an asymptote), not 1. tan = 1 at 45°, where sin and cos are equal."}
        ],
        "guided_steps": [
            {"say": "tan x = 1 means sin x and cos x are equal, since tan = sin ÷ cos and any number over itself is 1. Find where they meet."},
            {"pre": "At the start, sin 0° = 0 and cos 0° = 1, so tan 0° = 0 ÷ 1 = ", "post": "", "answer": 0,
             "hint": "tan 0° = 0, not 1 yet."},
            {"phase": "substitute", "say": "As x grows, sine rises and cosine falls. They meet exactly halfway to 90°.",
             "pre": "halfway from 0° to 90° is ", "post": "°", "answer": 45, "hint": "Halfway between 0 and 90 is 45."},
            {"pre": "Check: at 45° sin and cos are both about 0.707, so tan 45° = 0.707 ÷ 0.707 = ", "post": "", "answer": 1,
             "done": "Equal top and bottom give tan 45° = 1, so x = 45°.",
             "hint": "Equal numbers divided give 1."},
        ],
    },
]

# ---- SILVER ----
silver = [
    {  # 0 : sin x = 1 smallest x => 90
        "display": "\\(\\sin x = 1\\). Find the smallest positive value of \\(x\\) in degrees.",
        "solutions": [90],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Sine reaches its maximum of 1 at one special angle.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 0,
             "message": "sin x reaches its maximum of 1 at x = 90°, not at the start."}
        ],
        "guided_steps": [
            {"say": "sin x = 1 means the sine wave is at its highest point. Find where the peak is."},
            {"pre": "The maximum value sine can reach is ", "post": "", "answer": 1, "hint": "Sine never goes above 1."},
            {"pre": "On the graph, sine starts on the middle line. sin 0° = ", "post": "", "answer": 0, "hint": "Sine starts at zero."},
            {"phase": "substitute", "say": "The very first time it reaches the peak of 1 is a quarter-turn in.",
             "pre": "smallest x with sin x = 1 is ", "post": "°", "answer": 90, "hint": "Sine peaks at 90°."},
            {"pre": "Check: sin 90° = ", "post": "", "answer": 1,
             "done": "Height 1 at 90° matches sin x = 1, so x = 90°.", "hint": "Read the peak height at 90°."},
        ],
    },
    {  # 1 : cos x = 0, LARGER solution => 270  (CHANGED to larger; AUDIT wording)
        "display": "\\(\\cos x = 0\\) has two solutions for \\(0° \\leq x \\leq 360°\\). Give the larger one.",
        "solutions": [270],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Cosine crosses zero twice; pick the larger angle.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 90,
             "message": "cos x = 0 at x = 90° and x = 270°. You were asked for the LARGER, which is 270°, not 90°."}
        ],
        "guided_steps": [
            {"say": "cos x = 0 wherever the cosine wave crosses the middle line. Trace it and note both crossings."},
            {"pre": "Cosine starts at its maximum. cos 0° = ", "post": "", "answer": 1, "hint": "Cosine starts at 1."},
            {"pre": "It first crosses zero a quarter-turn in, at ", "post": "°", "answer": 90, "hint": "First zero at 90°."},
            {"phase": "substitute", "say": "After dipping to its minimum it rises back through zero once more. That second crossing is the larger solution.",
             "pre": "second crossing at ", "post": "°", "answer": 270, "hint": "Cosine is zero again at 270°."},
            {"pre": "The two solutions are 90° and 270°. The larger is ", "post": "", "answer": 270,
             "done": "Of 90° and 270°, the larger is 270°.", "hint": "270 is bigger than 90."},
        ],
    },
    {  # 2 : sin x = 0.5 other => 150
        "display": "\\(\\sin x = 0.5\\). One solution is \\(30°\\). Find the other solution for \\(0° \\leq x \\leq 360°\\).",
        "solutions": [150],
        "calculator": False,
        "input_type": "single_value",
        "hint": "For sine, the second solution is 180 minus the first.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 210,
             "message": "Sin is positive in the 1st and 2nd quadrants. The second solution is 180° − 30° = 150°, not 180° + 30°."}
        ],
        "guided_steps": [
            {"say": "Sine is positive in the first two quadrants. The two angles sit symmetrically about the peak at 90°."},
            {"pre": "The given solution 30° is how far below the peak angle 90°? 90 − 30 = ", "post": "°", "answer": 60,
             "hint": "Subtract 30 from 90."},
            {"phase": "substitute", "say": "The second solution is the same distance the OTHER side of the peak. Use the rule 180 − first.",
             "pre": "other solution = 180 − 30 = ", "post": "°", "answer": 150, "hint": "Take the first solution from 180."},
            {"pre": "Check the symmetry: midpoint (30 + 150) ÷ 2 = ", "post": "°", "answer": 90,
             "done": "Both angles are 60° either side of the peak at 90°, so the other solution is 150°.",
             "hint": "Average the two angles."},
        ],
    },
    {  # 3 : count sin x = 0 values => 3  (AUDIT wording)
        "display": "How many values of \\(x\\) satisfy \\(\\sin x = 0\\) for \\(0° \\leq x \\leq 360°\\)?",
        "solutions": [3],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Count every angle where the sine wave sits on the axis, endpoints included.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 2,
             "message": "sin x = 0 at x = 0°, 180° and 360°. Do not forget the endpoints: that is 3 values."}
        ],
        "guided_steps": [
            {"say": "sin x = 0 wherever the sine wave sits on the middle line. Count every such angle in the range, endpoints included."},
            {"pre": "sin 0° = ", "post": "", "answer": 0, "hint": "Sine is zero at the very start."},
            {"pre": "The next time it is zero is halfway along, at ", "post": "°", "answer": 180, "hint": "Sine crosses zero at 180°."},
            {"phase": "substitute", "say": "It returns to zero once more at the end of the range. The full list is 0°, 180°, 360°.",
             "pre": "the third zero is at ", "post": "°", "answer": 360, "hint": "Sine is zero again at 360°."},
            {"pre": "Now count them: 0°, 180°, 360° makes a total of ", "post": "", "answer": 3,
             "done": "Three angles give sin x = 0, so the answer is 3.", "hint": "Count the three angles you listed."},
        ],
    },
    {  # 4 : max of 4 sin x => 4  (CHANGED from 3 sin x)
        "display": "What is the maximum value of \\(4\\sin x\\)?",
        "solutions": [4],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiplying sine by 4 multiplies its peak height by 4.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 1,
             "message": "The maximum of sin x is 1. Multiplying by 4 stretches the graph, so the maximum becomes 4 × 1 = 4."}
        ],
        "guided_steps": [
            {"say": "Multiplying sine by a number stretches the wave vertically. The peak stretches by the same factor."},
            {"pre": "The maximum value of plain sin x is ", "post": "", "answer": 1, "hint": "Sine peaks at 1."},
            {"pre": "That peak happens at x = ", "post": "°", "answer": 90, "hint": "Sine is highest at 90°."},
            {"phase": "substitute", "say": "Multiplying the whole thing by 4 multiplies that peak height by 4.",
             "pre": "maximum of 4 sin x = 4 × 1 = ", "post": "", "answer": 4, "hint": "Four times the peak of 1."},
            {"pre": "Check at the peak: 4 × sin 90° = 4 × 1 = ", "post": "", "answer": 4,
             "done": "The stretched wave peaks at 4, so the maximum is 4.", "hint": "Put sin 90° = 1 into 4 sin x."},
        ],
    },
    {  # 5 : cycles of tan in 360 => 2
        "display": "How many complete cycles does \\(y = \\tan x\\) complete between \\(0°\\) and \\(360°\\)?",
        "solutions": [2],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Divide the range by the tangent period of 180.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 1,
             "message": "tan has period 180°. In 360° it completes 360 ÷ 180 = 2 full cycles."}
        ],
        "guided_steps": [
            {"say": "A complete cycle is one full repeat of the tan pattern. Its length is the period. Count how many fit in 360°."},
            {"pre": "The period of tan, one full repeat, is ", "post": "°", "answer": 180, "hint": "Tan repeats every 180°."},
            {"pre": "The range from 0° to 360° has width ", "post": "°", "answer": 360, "hint": "The full range width is 360°."},
            {"phase": "substitute", "say": "The number of cycles is the range divided by one period.",
             "pre": "cycles = 360 ÷ 180 = ", "post": "", "answer": 2, "hint": "Divide 360 by 180."},
            {"pre": "Check: 2 cycles × 180° each = ", "post": "°", "answer": 360,
             "done": "Two periods of 180° fill the 360° range exactly, so 2 complete cycles.",
             "hint": "Multiply 2 by 180."},
        ],
    },
    {  # 6 : cos x = -1 => 180
        "display": "\\(\\cos x = -1\\). Find \\(x\\) for \\(0° \\leq x \\leq 360°\\).",
        "solutions": [180],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Cosine reaches minus one at the bottom of its wave.",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 270,
             "message": "cos x reaches its minimum of −1 at exactly x = 180°. There is only one solution in this range."}
        ],
        "guided_steps": [
            {"say": "cos x = −1 means the cosine wave is at its lowest point. Find where the trough is."},
            {"pre": "Cosine starts at its maximum. cos 0° = ", "post": "", "answer": 1, "hint": "Cosine starts at 1."},
            {"pre": "It falls to the middle line at 90°. cos 90° = ", "post": "", "answer": 0, "hint": "Cosine is zero at 90°."},
            {"phase": "substitute", "say": "It keeps falling to the very bottom of the wave a further quarter-turn on.",
             "pre": "lowest point at x = ", "post": "°", "answer": 180, "hint": "Cosine bottoms out at 180°."},
            {"pre": "Check the height there: cos 180° = ", "post": "", "answer": -1,
             "done": "Height −1 at 180° matches cos x = −1, so x = 180°.", "hint": "Read the trough height at 180°."},
        ],
    },
]

# ---- GOLD ----
gold = [
    {  # 0 : cos x = 0.5 larger => 300
        "display": "Solve \\(\\cos x = 0.5\\) for \\(0° \\leq x \\leq 360°\\). Give the larger solution.",
        "solutions": [300],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Find the principal value, then use 360 minus it for the fourth quadrant.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 60,
             "message": "cos⁻¹(0.5) = 60°. Cos is positive in Q1 and Q4. The solutions are 60° and 360° − 60° = 300°; the larger is 300°."}
        ],
        "guided_steps": [
            {"say": "Find the principal value with inverse cosine, use symmetry for the second solution, then pick the larger."},
            {"pre": "Principal value: cos⁻¹(0.5) = ", "post": "°", "answer": 60, "hint": "cos⁻¹(0.5) is 60°."},
            {"pre": "Cosine is positive in the 1st and 4th quadrants. The Q1 solution is ", "post": "°", "answer": 60,
             "hint": "The Q1 solution equals the principal value, 60°."},
            {"phase": "substitute", "say": "The 4th-quadrant solution is 360 minus the principal value.",
             "pre": "second solution = 360 − 60 = ", "post": "°", "answer": 300, "hint": "Subtract 60 from 360."},
            {"pre": "The two solutions are 60° and 300°. The larger is ", "post": "°", "answer": 300,
             "done": "Of 60° and 300°, the larger is 300°.", "hint": "300 is bigger than 60."},
        ],
    },
    {  # 1 : sin x = -root2/2 smaller => 225
        "display": "Solve \\(\\sin x = -\\frac{\\sqrt{2}}{2}\\) for \\(0° \\leq x \\leq 360°\\). Give the smaller solution.",
        "solutions": [225],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Take the inverse sine of the positive value, then place it in the negative quadrants.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 315,
             "message": "sin⁻¹(√2/2) = 45°. Sin is negative in Q3 and Q4: 180° + 45° = 225° and 360° − 45° = 315°. The smaller is 225°, not 315°."}
        ],
        "guided_steps": [
            {"say": "Take the inverse sine of the positive value first, place both solutions in the negative quadrants, then pick the smaller."},
            {"pre": "Ignore the minus for a moment: sin⁻¹(√2/2) = ", "post": "°", "answer": 45,
             "hint": "sin⁻¹(√2/2) is 45°, since √2/2 is about 0.707."},
            {"pre": "Sine is negative in the 3rd and 4th quadrants. Q3 solution = 180 + 45 = ", "post": "°", "answer": 225,
             "hint": "Add 45 to 180."},
            {"phase": "substitute", "say": "The 4th-quadrant solution is 360 minus 45.",
             "pre": "Q4 solution = 360 − 45 = ", "post": "°", "answer": 315, "hint": "Subtract 45 from 360."},
            {"pre": "The two solutions are 225° and 315°. The smaller is ", "post": "°", "answer": 225,
             "done": "Of 225° and 315°, the smaller is 225°.", "hint": "225 is less than 315."},
        ],
    },
    {  # 2 : mc translation => index 1
        "display": "The graph of \\(y = \\sin x\\) is translated by the vector \\(\\begin{pmatrix} 90 \\\\ 0 \\end{pmatrix}\\). What is the equation of the new graph?",
        "options": ["y = sin(x + 90°)", "y = sin(x − 90°)", "y = cos x", "y = sin x + 90"],
        "solutions": [1],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Translating a graph right by 90 replaces x with (x minus 90).",
        "misconceptions": [
            {"check": "common", "pattern": "confusion", "expect": 0,
             "message": "A translation of 90 to the right replaces x with (x − 90). Note sin(x − 90°) = -cos x, not cos x. The answer is y = sin(x − 90°)."}
        ],
    },
    {  # 3 : tan x = 1 sum => 270
        "display": "Solve \\(\\tan x = 1\\) for \\(0° \\leq x \\leq 360°\\). Give the sum of both solutions.",
        "solutions": [270],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Tan repeats every 180, so add 180 for the second solution.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 180,
             "message": "tan⁻¹(1) = 45°. Tan repeats every 180° (not 180 − x like sine), so the second solution is 45° + 180° = 225°. Sum = 45 + 225 = 270."}
        ],
        "guided_steps": [
            {"say": "Find the first solution with inverse tan, add the period for the second, then add them together."},
            {"pre": "Principal value: tan⁻¹(1) = ", "post": "°", "answer": 45, "hint": "tan⁻¹(1) is 45°."},
            {"pre": "Tan repeats every 180°, so the second solution is 45 + 180 = ", "post": "°", "answer": 225,
             "hint": "Add the period, 180°."},
            {"phase": "substitute", "say": "Now add the two solutions together.",
             "pre": "sum = 45 + 225 = ", "post": "", "answer": 270, "hint": "Add 45 and 225."},
            {"pre": "Check both lie in 0° to 360°: 45° and 225° do, and 45 + 225 = ", "post": "", "answer": 270,
             "done": "Both solutions are in range and add to 270.", "hint": "Re-add 45 and 225."},
        ],
    },
    {  # 4 : 2 sin x - 1 = 0 number of solutions => 2
        "display": "The equation \\(2\\sin x - 1 = 0\\) has solutions in \\(0° \\leq x \\leq 360°\\). Find the number of solutions.",
        "solutions": [2],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Rearrange to sin x = 0.5, then count how many angles reach that height.",
        "misconceptions": [
            {"check": "common", "pattern": "wrong_formula", "expect": 1,
             "message": "Rearrange to sin x = 0.5. This has two solutions (30° and 150°) in the range 0° to 360°, so the answer is 2."}
        ],
        "guided_steps": [
            {"say": "Rearrange to make sin x the subject, then count how many times the sine graph reaches that height in the range."},
            {"pre": "2 sin x − 1 = 0 gives 2 sin x = 1, so sin x = 1 ÷ 2 = ", "post": "", "answer": 0.5,
             "hint": "Add 1 to both sides, then divide by 2."},
            {"pre": "The principal value is sin⁻¹(0.5) = ", "post": "°", "answer": 30, "hint": "sin⁻¹(0.5) is 30°."},
            {"phase": "substitute", "say": "Sine is positive in two quadrants, so there is a second solution: 180 − 30.",
             "pre": "second solution 180 − 30 = ", "post": "°", "answer": 150, "hint": "Take 30 from 180."},
            {"pre": "So the solutions are 30° and 150°: a total of ", "post": "", "answer": 2,
             "done": "Two angles solve the equation, so the number of solutions is 2.", "hint": "Count 30° and 150°."},
        ],
    },
]

problem_bank = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "Recall the fixed values and key features of the sine, cosine and tangent graphs at standard angles.",
    "silver_description": "Solve simple trig equations and read features like maxima, zeros and cycles straight from the graph.",
    "gold_description": "Handle exact (surd) values, negative results, sums of solutions, and graph transformations.",
}

# ---- tier_guides ----
tier_guides = {
    "bronze": {
        "title": "Bronze: reading values off the three graphs",
        "steps": [
            "<strong>Know the three shapes.</strong> \\(y=\\sin x\\) starts at 0, peaks at 90°, back to 0 at 180°, dips to −1 at 270°, back to 0 at 360°. \\(y=\\cos x\\) is the same wave starting at 1. \\(y=\\tan x\\) starts at 0 and shoots to an asymptote at 90°.",
            "<strong>Learn the landmarks.</strong> sin and cos swing between −1 and 1 (amplitude 1) and repeat every 360°. tan has no maximum and repeats every 180°, with asymptotes at 90°, 270°, and so on.",
            "To read a value, trace the wave round in 90° steps and note the height at the angle you want.",
        ],
        "example": {
            "question": "What is the value of cos 90°?",
            "steps": [
                {"label": "Trace the cosine graph", "content": "<p>Cosine starts at 1 and falls to the middle line after a quarter-turn.</p>"},
                {"label": "Read the height at 90°", "content": "<p>At 90° the cosine wave is exactly on the middle line.</p>"},
                {"label": "Check", "content": "<p>By symmetry cosine is also 0 at 270°, a quarter-turn from a peak, which confirms a height of 0 at 90°.</p>"},
                {"label": "Answer", "content": "<p>\\(\\cos 90° = 0\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: solving simple equations with the graph",
        "steps": [
            "<strong>Solve by reading heights.</strong> To solve \\(\\sin x = k\\), find where the wave reaches height \\(k\\). Most heights are reached <strong>twice</strong> between 0° and 360°.",
            "For sine, the second solution is \\(180° - \\text{first}\\); for cosine it is \\(360° - \\text{first}\\). Peaks, troughs and zeros sit at set angles you read off.",
            "<strong>Stretches and counts:</strong> multiplying sine by \\(n\\) makes the maximum \\(n\\); to count cycles, divide the range by the period.",
        ],
        "example": {
            "question": "Solve cos x = 0.5 for 0° ≤ x ≤ 360°.",
            "steps": [
                {"label": "Principal value", "content": "<p>\\(\\cos^{-1}(0.5) = 60°\\).</p>"},
                {"label": "Second solution", "content": "<p>Cosine is positive in the 1st and 4th quadrants, so the other angle is \\(360° - 60° = 300°\\).</p>"},
                {"label": "Check", "content": "<p>Reading the cosine graph at 60° and at 300° gives a height of 0.5 both times.</p>"},
                {"label": "Answer", "content": "<p>\\(x = 60°\\) and \\(x = 300°\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: surds, sums and transformations",
        "steps": [
            "<strong>Exact values.</strong> sin or cos of 30°, 45°, 60° give surds like \\(\\frac{\\sqrt{2}}{2}\\). Take the inverse of the positive value, then place the solutions in the correct quadrants for the sign.",
            "<strong>Combine solutions.</strong> A question may want the sum, the larger, or a count. Find every solution in range first, then answer what is actually asked.",
            "<strong>Transformations.</strong> \\(y=\\sin(x-90°)\\) shifts the graph right by 90°; adding a number outside shifts it up. Changing \\(x\\) moves the graph sideways.",
        ],
        "example": {
            "question": "Solve sin x = √3/2 for 0° ≤ x ≤ 360° and give the sum.",
            "steps": [
                {"label": "Inverse", "content": "<p>\\(\\sin^{-1}\\!\\left(\\frac{\\sqrt{3}}{2}\\right) = 60°\\).</p>"},
                {"label": "Both solutions", "content": "<p>Sine is positive in Q1 and Q2: \\(60°\\) and \\(180° - 60° = 120°\\).</p>"},
                {"label": "Check", "content": "<p>Both angles lie in range and mirror about the peak at 90°.</p>"},
                {"label": "Answer", "content": "<p>Sum \\(= 60° + 120° = 180°\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- guided ----
guided = {
    "opener": {
        "label": "Before any trig",
        "display": "You get on a big wheel at the bottom (0 m up).<br>The very top of the wheel is 10 m above the platform.",
        "steps": [
            {"say": "Forget algebra for a moment. Ride a big wheel. You get on at the bottom, level with the platform, so your height is 0 m. The very top of the wheel is 10 m up. The wheel turns steadily.",
             "pre": "A quarter-turn later you are level with the middle of the wheel, exactly halfway up. Your height is ", "post": " m",
             "answer": 5, "hint": "Halfway between 0 m and the 10 m top."},
            {"say": "Keep going. Another quarter-turn takes you to the very top.",
             "pre": "At the top your height is ", "post": " m", "answer": 10, "hint": "The top of the wheel is 10 m up."},
            {"say": "Then you come back down: 5 m, then 0 m at the bottom, and it all repeats on the next turn.",
             "pre": "After a full turn you are back at the bottom, so your height is ", "post": " m", "answer": 0,
             "hint": "A full turn brings you back to where you started."},
            {"say": "Plot your height against the angle turned and you get a smooth wave: up to a peak, down to the bottom, repeating every full turn. That wave IS the graph of \\(y = \\sin x\\). How far it swings from the middle is the <strong>amplitude</strong>; one full turn before the pattern repeats is the <strong>period</strong>, which for sine and cosine is <strong>360°</strong>. sin and cos just write this wheel-height pattern using angles."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Read the five key heights of \\(y = \\sin x\\), at 0°, 90°, 180°, 270° and 360°.",
            "label": "Together: reading the wave",
            "steps": [
                {"say": "The sine wave has five easy landmarks in one full turn, a quarter-turn apart. Read the height at each."},
                {"pre": "sin 0° (the start) = ", "post": "", "answer": 0, "hint": "Sine starts on the middle line."},
                {"pre": "sin 90° (the peak) = ", "post": "", "answer": 1, "hint": "The highest point of the wave."},
                {"pre": "sin 180° (back to the middle) = ", "post": "", "answer": 0, "hint": "Halfway round, back to zero."},
                {"pre": "sin 270° (the trough) = ", "post": "", "answer": -1, "hint": "The lowest point of the wave."},
                {"pre": "sin 360° (full turn, back to the start) = ", "post": "", "answer": 0,
                 "done": "Those five heights, 0, 1, 0, −1, 0, are the whole shape of the sine wave. Learn them and you can read any value.",
                 "hint": "A full turn returns sine to its start."},
            ],
        },
        "silver": {
            "display": "Solve \\(\\sin x = 0.5\\) for \\(0° \\leq x \\leq 360°\\), giving both solutions.",
            "label": "Together: the silver move",
            "steps": [
                {"say": "The new move: one equation, but the wave reaches the same height twice. Find both angles."},
                {"pre": "Principal value: sin⁻¹(0.5) = ", "post": "°", "answer": 30, "hint": "sin⁻¹(0.5) is 30°."},
                {"pre": "Sine is positive in the 1st and 2nd quadrants. Second solution = 180 − 30 = ", "post": "°", "answer": 150,
                 "hint": "Take the first solution from 180."},
                {"pre": "How many solutions in the range? ", "post": "", "answer": 2, "hint": "You found 30° and 150°."},
                {"pre": "Check they are symmetric about the peak at 90°: midpoint (30 + 150) ÷ 2 = ", "post": "°", "answer": 90,
                 "done": "Both angles sit 60° either side of the peak at 90°. That mirror trick finds the second solution every time.",
                 "hint": "Average 30 and 150."},
            ],
        },
        "gold": {
            "display": "Solve \\(\\cos x = -\\frac{\\sqrt{3}}{2}\\) for \\(0° \\leq x \\leq 360°\\) and give the sum of the solutions.",
            "label": "Together: the gold move",
            "steps": [
                {"say": "At this level the value is a surd and negative, and we combine both solutions. Take it in stages."},
                {"pre": "Take the inverse cosine of the positive surd: cos⁻¹(√3/2) = ", "post": "°", "answer": 30, "hint": "cos⁻¹(√3/2) is 30°."},
                {"pre": "Cosine is negative in the 2nd and 3rd quadrants. Q2 solution = 180 − 30 = ", "post": "°", "answer": 150, "hint": "Take 30 from 180."},
                {"pre": "Q3 solution = 180 + 30 = ", "post": "°", "answer": 210, "hint": "Add 30 to 180."},
                {"pre": "Sum of the solutions = 150 + 210 = ", "post": "", "answer": 360, "hint": "Add 150 and 210."},
                {"pre": "Check the symmetry about 180°: midpoint (150 + 210) ÷ 2 = ", "post": "°", "answer": 180,
                 "done": "Both solutions sit 30° either side of 180° and add to 360. Surd, sign and sum handled together: that is the gold move.",
                 "hint": "Average 150 and 210."},
            ],
        },
    },
}

practice_data = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": problem_bank,
    "tier_guides": tier_guides,
    "guided": guided,
    "related_videos": related_videos,
    "worked_examples": worked_examples,
}

json.dump(practice_data, io.open("lesson_graphs-L06.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote lesson_graphs-L06.json")
