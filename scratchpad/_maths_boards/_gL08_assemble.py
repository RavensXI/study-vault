# -*- coding: utf-8 -*-
import json, io
import importlib.util, os
spec = importlib.util.spec_from_file_location("b", os.path.join(os.path.dirname(__file__), "_gL08_build.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

tangent_svg = b.tangent_svg; trap_svg = b.trap_svg; ramp_svg = b.ramp_svg
trap_chart = b.trap_chart; tangent_steps = b.tangent_steps; trap_steps = b.trap_steps
s = b.s; numify = b.numify; MINUS = b.MINUS
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

live = json.load(io.open(os.path.join(os.path.dirname(__file__), "_gL08_live.json"), encoding="utf-8"))

# ---- sanity checks on every bank problem (fresh solve) ----
b.assert_tangent(2, 5, 6, 13, 2)
b.assert_tangent(1, 4, 4, 16, 4)   # B1 fixed (was 6,10 dup=2)
b.assert_tangent(0, 8, 4, 0, -2)
b.assert_tangent(1, 2, 3, 12, 5)
b.assert_tangent(2, 10, 6, 30, 5)
b.assert_tangent(0, 10, 4, -2, -3)
b.assert_tangent(4, 18, 10, 6, -2)
b.assert_trap([0, 1, 4], 1, 3)
b.assert_trap([0, 1, 4, 9], 1, 9.5)
b.assert_trap([0, 3, 8, 15, 24], 2, 76)
b.assert_trap([1, 4, 9], 3, 27)
b.assert_trap([0, 1, 4, 9, 16], 1, 22)
b.assert_trap([0, 2, 6, 12, 20, 30], 2, 110)
b.assert_trap([2, 5, 10, 17], 4, 98)
print("all fresh-solve asserts passed")

def tangent_problem(x1, y1, x2, y2, sol, hint, misc):
    disp = (tangent_svg(x1, y1, x2, y2)
            + "A tangent to a curve passes through \\((%s, %s)\\) and \\((%s, %s)\\). What is the gradient?" % (s(x1), s(y1), s(x2), s(y2))
            + CAP)
    return {"display": disp, "solutions": [sol], "calculator": False,
            "input_type": "single_value", "hint": hint,
            "misconceptions": misc, "guided_steps": tangent_steps(x1, y1, x2, y2)}

def trap_problem(text, heights, h, sol, hint, misc):
    return {"display": text, "solutions": [sol], "calculator": False,
            "input_type": "single_value", "hint": hint, "chart": trap_chart(heights, h),
            "misconceptions": misc, "guided_steps": trap_steps(heights, h)}

def mc(display, options, sol, hint, msg, pattern):
    return {"display": display, "options": options, "solutions": [sol], "calculator": False,
            "input_type": "multiple_choice", "hint": hint,
            "misconceptions": [{"pattern": pattern, "expect": None, "message": msg}]}

def m_inv(run, rise, ex):
    return {"pattern": "rise_run_inverted", "expect": ex,
            "message": "Gradient is rise ÷ run, not run ÷ rise. Dividing the run by the rise, %s ÷ %s, gives the wrong value; put the change in y on top." % (s(run), s(rise)),
            "note": "run/rise = %s/%s" % (run, rise)}

def m_sign(ex):
    return {"pattern": "sign_error", "expect": ex,
            "message": "Keep the same order top and bottom. Going down the curve gives a negative rise, so the gradient is negative here. A positive answer flips one sign.",
            "note": "sign flip"}

def m_nodouble(ex):
    return {"pattern": "middles_not_doubled", "expect": ex,
            "message": "The middle heights must be doubled. Only the first and last heights are used once; every height in between is counted twice.",
            "note": "forgot to double middles"}

def m_hfactor(ex, hval):
    return {"pattern": "wrong_h_factor", "expect": ex,
            "message": "The factor outside is h ÷ 2, and here h = %d, so it is %s, not a half. Using a half shrinks the whole estimate." % (hval, s(hval / 2 if False else numify(hval / 2))),
            "note": "used 1/2 instead of h/2"}

hint_tan = "Gradient is rise ÷ run: divide the change in y by the change in x."
hint_trap = "Use A ≈ (h ÷ 2) × [first + last + 2 × (all the middle heights)]."

bronze = [
    tangent_problem(2, 5, 6, 13, 2, hint_tan, [m_inv(4, 8, 0.5)]),
    tangent_problem(1, 4, 4, 16, 4, hint_tan, [m_inv(3, 12, 0.25)]),
    mc("A tangent at a point on a speed-time graph has gradient 5. What does this represent?",
       ["Speed of 5 m/s", "Acceleration of 5 m/s²", "Distance of 5 m", "Time of 5 s"], 1,
       "On a speed-time graph, the tangent's gradient is the acceleration.",
       "On a speed-time graph the gradient of a tangent gives the acceleration at that instant.", "confusion"),
    tangent_problem(0, 8, 4, 0, -2, hint_tan, [m_sign(2)]),
    mc("What does the area under a speed-time graph represent?",
       ["Acceleration", "Distance", "Speed", "Gradient"], 1,
       "Area under a speed-time graph is the distance travelled.",
       "The area between a speed-time graph and the time axis is the distance travelled.", "confusion"),
    tangent_problem(3, 7, 5, 7, 0, hint_tan,
       [{"pattern": "flat_tangent", "expect": None,
         "message": "Both y-values are equal, so the tangent is horizontal and its gradient is 0. This happens at a turning point of the curve.",
         "note": "no single determinate wrong value"}]),
    trap_problem("Use the trapezium rule with 2 strips to estimate the area under \\(y = x^2\\) from \\(x = 0\\) to \\(x = 2\\). Heights: \\(y_0 = 0, y_1 = 1, y_2 = 4\\).",
                 [0, 1, 4], 1, 3, hint_trap, [m_nodouble(2.5)]),
    tangent_problem(1, 2, 3, 12, 5, hint_tan, [m_inv(2, 10, 0.2)]),
]

silver = [
    trap_problem("Use the trapezium rule with 3 strips to estimate the area under \\(y = x^2\\) from \\(x = 0\\) to \\(x = 3\\). Heights: \\(y_0 = 0, y_1 = 1, y_2 = 4, y_3 = 9\\).",
                 [0, 1, 4, 9], 1, 9.5, hint_trap, [m_nodouble(7)]),
    trap_problem("Use the trapezium rule with 4 strips to estimate the area under a curve. Strip width \\(h = 2\\), heights: \\(y_0 = 0, y_1 = 3, y_2 = 8, y_3 = 15, y_4 = 24\\).",
                 [0, 3, 8, 15, 24], 2, 76, hint_trap, [m_hfactor(38, 2)]),
    tangent_problem(2, 10, 6, 30, 5, "On a distance-time graph the tangent's gradient is the speed. Gradient is rise ÷ run.",
                    [m_inv(4, 20, 0.2)]),
    tangent_problem(0, 10, 4, -2, -3, hint_tan, [m_sign(3)]),
    mc("The trapezium rule gives an <strong>overestimate</strong> when the curve is:",
       ["Concave (curves downward)", "Convex (curves upward)", "Straight", "S-shaped"], 1,
       "Straight strip-tops sit above a curve that bows upward.",
       "When a curve bows upward (convex), the straight strip-tops lie above the curve, so the estimate is too big.", "confusion"),
    trap_problem("Use the trapezium rule with 2 strips to estimate the area under a curve. Strip width \\(h = 3\\), heights: \\(y_0 = 1, y_1 = 4, y_2 = 9\\).",
                 [1, 4, 9], 3, 27, hint_trap, [m_nodouble(21)]),
    mc("Why does the gradient of a tangent to a distance-time graph give the speed?",
       ["Because gradient = distance ÷ time = speed", "Because area = distance", "Because tangent = acceleration", "Because gradient = time ÷ distance"], 0,
       "Gradient is change in distance ÷ change in time.",
       "Gradient is change in y ÷ change in x, which on a distance-time graph is change in distance ÷ change in time, and that is speed.", "confusion"),
]

# tweak silver tangent displays to name the context (speed / gradient at x)
silver[2]["display"] = (tangent_svg(2, 10, 6, 30)
    + "A tangent drawn to a distance-time curve at \\(t = 4\\) passes through \\((2, 10)\\) and \\((6, 30)\\). What is the speed at \\(t = 4\\)?" + CAP)
silver[3]["display"] = (tangent_svg(0, 10, 4, -2)
    + "A tangent to a curve at \\(x = 2\\) passes through \\((0, 10)\\) and \\((4, -2)\\). What is the gradient at \\(x = 2\\)?" + CAP)

gold = [
    trap_problem("Use the trapezium rule with 4 strips to estimate the area under \\(y = x^2\\) from \\(x = 0\\) to \\(x = 4\\). Heights: \\(y_0 = 0, y_1 = 1, y_2 = 4, y_3 = 9, y_4 = 16\\).",
                 [0, 1, 4, 9, 16], 1, 22, hint_trap, [m_nodouble(15)]),
    trap_problem("Use the trapezium rule with 5 strips to estimate the area under a curve. Strip width \\(h = 2\\), heights: \\(y_0 = 0, y_1 = 2, y_2 = 6, y_3 = 12, y_4 = 20, y_5 = 30\\).",
                 [0, 2, 6, 12, 20, 30], 2, 110, hint_trap, [m_hfactor(55, 2)]),
    tangent_problem(4, 18, 10, 6, -2, "On a speed-time graph the tangent's gradient is the acceleration. Gradient is rise ÷ run.",
                    [m_sign(2)]),
    mc("The exact area under \\(y = x^2\\) from 0 to 3 is 9. The trapezium rule (3 strips) gives 9.5. Is this an overestimate or underestimate?",
       ["Overestimate", "Underestimate"], 0,
       "Compare 9.5 with 9: which is bigger?",
       "9.5 is bigger than 9, so it is an overestimate. The parabola bows upward, so the strip-tops sit above it.", "confusion"),
    trap_problem("Use the trapezium rule with 3 strips to estimate the area under a curve. Strip width \\(h = 4\\), heights: \\(y_0 = 2, y_1 = 5, y_2 = 10, y_3 = 17\\).",
                 [2, 5, 10, 17], 4, 98, hint_trap, [m_hfactor(24.5, 4)]),
]

# name gold speed-time tangent context
gold[2]["display"] = (tangent_svg(4, 18, 10, 6)
    + "A speed-time curve has a tangent at \\(t = 6\\) passing through \\((4, 18)\\) and \\((10, 6)\\). What is the acceleration at \\(t = 6\\)?" + CAP)

# ---- tier guides ----
tier_guides = {
    "bronze": {
        "title": "Bronze: gradient of a tangent",
        "steps": [
            "A curve's steepness changes as you move along it. To read it at one point, a straight <strong>tangent</strong> is drawn touching the curve there.",
            "The gradient of that tangent is the gradient of the curve at the point: gradient = rise ÷ run, using two clear points on the tangent.",
            "Rise is the change in y (top), run is the change in x (bottom). A downhill tangent gives a negative gradient."
        ],
        "example": {
            "question": "A tangent passes through (1, 3) and (5, 11). Find its gradient.",
            "steps": [
                {"label": "Rise", "content": "<p>rise = \\(11 - 3 = 8\\)</p>"},
                {"label": "Run", "content": "<p>run = \\(5 - 1 = 4\\)</p>"},
                {"label": "Divide", "content": "<p>gradient = \\(8 ÷ 4 = 2\\)</p>"},
                {"label": "Check", "content": "<p>run × gradient = \\(4 × 2 = 8\\), the rise. ✓</p>"},
                {"label": "Answer", "content": "<p><strong>2</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: trapezium rule and rate of change",
        "steps": [
            "To estimate the area under a curve, split it into equal strips of width \\(h\\) and treat each strip top as a straight line.",
            "A ≈ (h ÷ 2) × [first height + last height + 2 × (all the middle heights)]. Every middle height is counted twice.",
            "A tangent's gradient also has meaning: on a distance-time graph it is the speed, on a speed-time graph it is the acceleration."
        ],
        "example": {
            "question": "Trapezium rule, 3 strips, h = 1, heights 0, 2, 6, 12.",
            "steps": [
                {"label": "Ends", "content": "<p>\\(0 + 12 = 12\\)</p>"},
                {"label": "Middles", "content": "<p>\\(2 + 6 = 8\\), doubled \\(= 16\\)</p>"},
                {"label": "Brackets", "content": "<p>\\(12 + 16 = 28\\)</p>"},
                {"label": "Check", "content": "<p>\\((1 ÷ 2) × 28 = 14\\)</p>"},
                {"label": "Answer", "content": "<p><strong>14 square units</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: harder areas and their meaning",
        "steps": [
            "The trapezium rule works for any strip width. When \\(h\\) is not 1, the factor h ÷ 2 changes: \\(h = 4\\) gives a factor of 2.",
            "A curve that bows upward (convex) gives an overestimate, because the straight strip-tops sit above the curve.",
            "Always read the axes: area can be a distance, and a tangent gradient can be a speed or an acceleration, with a sign that shows the direction."
        ],
        "example": {
            "question": "Trapezium rule, 3 strips, h = 4, heights 0, 3, 10, 21.",
            "steps": [
                {"label": "Ends", "content": "<p>\\(0 + 21 = 21\\)</p>"},
                {"label": "Middles", "content": "<p>\\(3 + 10 = 13\\), doubled \\(= 26\\)</p>"},
                {"label": "Brackets", "content": "<p>\\(21 + 26 = 47\\)</p>"},
                {"label": "Check", "content": "<p>\\((4 ÷ 2) × 47 = 94\\)</p>"},
                {"label": "Answer", "content": "<p><strong>94 square units</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---- opener ----
opener = {
    "label": "Before any graphs",
    "display": ramp_svg(),
    "steps": [
        {"say": "Two skateboard ramps. Steepness is just how many metres up for every metre across: rise ÷ run. Look at the gentle one, which rises 6 over a run of 3.",
         "pre": "steepness = 6 ÷ 3 = ", "post": "", "answer": 2,
         "hint": "How many metres up for each metre across? 6 shared over 3."},
        {"say": "The steeper ramp rises the same 6 but over a shorter run of 2, so it must be steeper.",
         "pre": "its steepness = 6 ÷ 2 = ", "post": "", "answer": 3,
         "hint": "6 shared over 2."},
        {"say": "That number is the <strong>gradient</strong>. A curve bends, so its steepness keeps changing. To measure it at one exact point, rest a ruler on the curve there (a <strong>tangent</strong>) and read the same rise ÷ run off the ruler. And the space underneath a graph, added up, gives a total, like the distance under a speed graph."}
    ]
}

# ---- teach ----
teach = {
    "bronze": {
        "display": tangent_svg(2, 4, 5, 16) + "A tangent to a curve passes through \\((2, 4)\\) and \\((5, 16)\\). Find its gradient." + CAP,
        "label": "Together: your first one",
        "steps": [
            {"say": "Gradient of a tangent is rise ÷ run.",
             "pre": "rise = 16 %s 4 = " % MINUS, "post": "", "answer": 12, "hint": "Take the first y from the second y."},
            {"pre": "run = 5 %s 2 = " % MINUS, "post": "", "answer": 3, "hint": "Take the first x from the second x."},
            {"say": "Now divide rise by run.",
             "pre": "gradient = 12 ÷ 3 = ", "post": "", "answer": 4, "hint": "Rise divided by run."},
            {"pre": "check: run × gradient = 3 × 4 = ", "post": "", "answer": 12,
             "done": "That matches the rise, so the gradient is 4.", "hint": "Run times gradient should give the rise."}
        ]
    },
    "silver": {
        "display": trap_svg([0, 2, 6, 12], 1) + "Use the trapezium rule with 3 strips. Strip width \\(h = 1\\), heights: \\(y_0 = 0, y_1 = 2, y_2 = 6, y_3 = 12\\)." + CAP,
        "label": "Together: the trapezium rule",
        "steps": [
            {"say": "Trapezium rule: A ≈ (h ÷ 2) × [first + last + 2 × middles].",
             "pre": "first + last = 0 + 12 = ", "post": "", "answer": 12, "hint": "Add the two end heights."},
            {"pre": "middles: 2 + 6 = ", "post": "", "answer": 8, "hint": "Add the in-between heights."},
            {"pre": "double the middles: 2 × 8 = ", "post": "", "answer": 16, "hint": "Multiply the middle total by 2."},
            {"pre": "brackets: 12 + 16 = ", "post": "", "answer": 28, "hint": "Add ends to doubled middles."},
            {"pre": "area ≈ (1 ÷ 2) × 28 = ", "post": "", "answer": 14,
             "done": "The estimated area is 14 square units.", "hint": "Multiply the bracket by h ÷ 2."}
        ]
    },
    "gold": {
        "display": trap_svg([0, 3, 10, 21], 4) + "Use the trapezium rule with 3 strips. Strip width \\(h = 4\\), heights: \\(y_0 = 0, y_1 = 3, y_2 = 10, y_3 = 21\\)." + CAP,
        "label": "Together: a bigger strip width",
        "steps": [
            {"say": "Same rule, but now h = 4, so the factor h ÷ 2 = 2.",
             "pre": "first + last = 0 + 21 = ", "post": "", "answer": 21, "hint": "Add the two end heights."},
            {"pre": "middles: 3 + 10 = ", "post": "", "answer": 13, "hint": "Add the in-between heights."},
            {"pre": "double the middles: 2 × 13 = ", "post": "", "answer": 26, "hint": "Multiply the middle total by 2."},
            {"pre": "brackets: 21 + 26 = ", "post": "", "answer": 47, "hint": "Add ends to doubled middles."},
            {"pre": "area ≈ (4 ÷ 2) × 47 = ", "post": "", "answer": 94,
             "done": "The estimated area is 94 square units.", "hint": "Multiply the bracket by h ÷ 2, and h ÷ 2 = 2."}
        ]
    }
}

# ---- method card (slim, no em dash) ----
method_card = {
    "title": "Gradients of Curves and Areas Under Graphs",
    "steps": [
        "Gradient at a point: draw a tangent, pick two points on it, then gradient = rise ÷ run.",
        "Area under a curve stands for a total, such as distance from a speed-time graph.",
        "Estimate area with the trapezium rule: A ≈ (h ÷ 2) × [first + last + 2 × (middle heights)].",
        "Read the axes to fix the units and the meaning of the answer."
    ],
    "content": "<p>A curve's steepness changes at every point. To measure it at one point, rest a ruler on the curve there (a <strong>tangent</strong>) and read gradient = rise ÷ run off the ruler. A downhill tangent gives a negative gradient.</p><p>The <strong>area</strong> between a curve and the x-axis stands for a total quantity. Estimate it with the <strong>trapezium rule</strong>: split the area into equal strips of width \\(h\\), then A ≈ (h ÷ 2) × [first height + last height + 2 × (all the middle heights)].</p>",
    "example": "<p><strong>Estimate the area under \\(y = x^2\\) from \\(x = 0\\) to \\(x = 3\\), trapezium rule, 3 strips.</strong></p><p>\\(h = 1\\). Heights: 0, 1, 4, 9.</p><p>A ≈ (1 ÷ 2) × [0 + 9 + 2(1 + 4)] = 0.5 × 19 = 9.5 square units.</p>"
}

# ---- fix em dashes in preserved worked_examples labels ----
we = live["worked_examples"]
for ex in we:
    for st in ex.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pd = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": {
        "bronze": bronze, "silver": silver, "gold": gold,
        "bronze_description": "Find gradients of tangents from given coordinates",
        "silver_description": "Use the trapezium rule and interpret gradient as rate of change",
        "gold_description": "Harder trapezium rule, estimating areas, and interpreting real-life contexts"
    },
    "related_videos": live.get("related_videos", []),
    "worked_examples": we,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach}
}

out = os.path.join(os.path.dirname(__file__), "lesson_maths-eduqas_graphs-L08.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
