# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagram practice_data for maths-ocr algebra-L08
(Quadratic Formula & Completing the Square). Preserves worked_examples,
related_videos, topic_links. Slims/keeps method_card. Adds tier_guides, guided
(opener+teach), guided_steps/hint/misconceptions on every bank problem."""
import json, io, math

M = "−"  # minus sign (plain-text unicode)

live = json.load(io.open("_algL08ocr_live.json", encoding="utf-8"))
src = live["practice_data"]

# ---- preserved, verified fields ----
method_card = src["method_card"]           # already slim, correct; keep
topic_links = src.get("topic_links", {"prerequisites": []})
related_videos = src.get("related_videos", [])
worked_examples = src["worked_examples"]   # 3, all fresh-verified correct
# sanitize em dashes in preserved worked_example labels (hard style rule)
for we in worked_examples:
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d

def say(s): return {"say": s}

# =====================================================================
# BRONZE
# =====================================================================
bronze = [
 { # 0
  "display": "Find the discriminant of \\(x^2 + 4x + 3 = 0\\)",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Read off a, b, c then work out b² − 4ac.",
  "misconceptions": [
    {"pattern":"added_4ac","check":"added_4ac","expect":28,
     "message":"The discriminant subtracts 4ac: 16 − 12 = 4. Adding it gives 28, which counts 4ac the wrong way."},
    {"pattern":"stopped_at_bsq","check":"stopped_at_bsq","expect":16,
     "message":"b² = 16 is only half the job. You still take off 4ac: 16 − 12 = 4."},
  ],
  "guided_steps":[
    say("The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 4, c = 3."),
    box("b squared: 4² = ", 16, "Square the number in front of x."),
    box("4ac: 4 × 1 × 3 = ", 12, "Multiply four, a and c.", phase="substitute"),
    box("discriminant: 16 − 12 = ", 4, "Take 4ac away from b squared.", phase="substitute",
        done="Positive, so two real roots."),
  ]},
 { # 1
  "display": "Solve \\(x^2 + 2x - 8 = 0\\) using the formula. Enter the positive solution.",
  "solutions": [2], "calculator": True, "input_type": "single_value",
  "hint": "The formula starts with −b; here b = 2, so the top starts −2.",
  "misconceptions":[
    {"pattern":"plus_b","check":"plus_b","expect":4,
     "message":"The formula uses −b on top. With b = 2 that is −2, giving (−2 + 6) ÷ 2 = 2. Using +2 gives 4."},
  ],
  "guided_steps":[
    say("Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 2, c = −8."),
    box("4ac: 4 × 1 × −8 = ", -32, "Multiply four, a and c, keeping signs."),
    box("discriminant: 4 − (−32) = ", 36, "b squared minus 4ac; two minuses add.", phase="substitute"),
    box("square root: √36 = ", 6, "A whole-number root here.", phase="substitute"),
    box("positive root: (−2 + 6) ÷ 2 = ", 2, "Take the + option, then divide by 2a = 2.", phase="substitute",
        done="x = 2 (the other root is −4). Check: 2² + 2×2 − 8 = 0."),
  ]},
 { # 2
  "display": "Write \\(x^2 + 6x\\) in the form \\((x+a)^2 + b\\). What is \\(b\\)?",
  "solutions": [-9], "calculator": False, "input_type": "single_value",
  "hint": "After halving and squaring, the constant is subtracted.",
  "misconceptions":[
    {"pattern":"kept_positive","check":"kept_positive","expect":9,
     "message":"The square is taken off: b = −(3²) = −9. Leaving it positive gives 9."},
    {"pattern":"subtracted_half","check":"subtracted_half","expect":-3,
     "message":"Subtract the square of the half, not the half itself: −(3²) = −9, not −3."},
  ],
  "guided_steps":[
    say("Complete the square on \\(x^2 + 6x\\). Halve the coefficient of x."),
    box("half of 6 = ", 3, "Divide the number in front of x by 2."),
    box("square that half: 3² = ", 9, "The half times itself.", phase="substitute"),
    box("b is minus that square: 0 − 9 = ", -9, "It is negative, the square subtracted.", phase="substitute",
        done="So x² + 6x = (x + 3)² − 9; b = −9."),
  ]},
 { # 3
  "display": "Solve \\(x^2 - 4x + 3 = 0\\) using the formula. Enter the larger solution.",
  "solutions": [3], "calculator": True, "input_type": "single_value",
  "hint": "The larger root takes the + sign on top; here −b = 4.",
  "misconceptions":[
    {"pattern":"took_smaller","check":"took_smaller","expect":1,
     "message":"That is the smaller root. The larger uses the + sign: (4 + 2) ÷ 2 = 3."},
  ],
  "guided_steps":[
    say("Use the formula with a = 1, b = −4, c = 3. Note −b = 4."),
    box("4ac: 4 × 1 × 3 = ", 12, "Multiply four, a and c."),
    box("discriminant: (−4)² − 12 = 16 − 12 = ", 4, "b squared minus 4ac.", phase="substitute"),
    box("square root: √4 = ", 2, "A whole-number root here.", phase="substitute"),
    box("larger root: (4 + 2) ÷ 2 = ", 3, "Take the + option, then divide by 2a = 2.", phase="substitute",
        done="x = 3 (smaller is 1). Check: 3² − 4×3 + 3 = 0."),
  ]},
 { # 4
  "display": "Find the discriminant of \\(x^2 + 5x + 6 = 0\\)",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "Work out b² − 4ac = 25 − 24.",
  "misconceptions":[
    {"pattern":"added_4ac","check":"added_4ac","expect":49,
     "message":"Subtract 4ac, do not add: 25 − 24 = 1. Adding gives 49."},
    {"pattern":"stopped_at_bsq","check":"stopped_at_bsq","expect":25,
     "message":"b² = 25 is not the end. Take off 4ac: 25 − 24 = 1."},
  ],
  "guided_steps":[
    say("The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 5, c = 6."),
    box("b squared: 5² = ", 25, "Square the number in front of x."),
    box("4ac: 4 × 1 × 6 = ", 24, "Multiply four, a and c.", phase="substitute"),
    box("discriminant: 25 − 24 = ", 1, "Take 4ac away from b squared.", phase="substitute",
        done="Positive (just), so two real roots."),
  ]},
 { # 5
  "display": "Write \\(x^2 + 10x + 20\\) in completed square form. What is the value inside the square (the number added to x)?",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "The number added to x is half the coefficient of x.",
  "misconceptions":[
    {"pattern":"forgot_halve","check":"forgot_halve","expect":10,
     "message":"Halve the coefficient of x first: 10 ÷ 2 = 5. The number inside is 5, not 10."},
  ],
  "guided_steps":[
    say("Complete the square on \\(x^2 + 10x + 20\\). The number inside the bracket is half the coefficient of x."),
    box("half of 10 = ", 5, "Divide the coefficient of x by 2."),
    box("square it to see the shift: 5² = ", 25, "The half times itself.", phase="substitute"),
    box("the constant becomes 20 − 25 = ", -5, "Original constant minus the square.", phase="substitute"),
    box("so the form is (x + 5)² − 5; the number added to x inside is ", 5,
        "It is the half you found.", phase="substitute",
        done="The bracket is (x + 5), so 5."),
  ]},
 { # 6
  "display": "How many real roots does \\(x^2 + 2x + 5 = 0\\) have?",
  "solutions": [0], "calculator": False, "input_type": "single_value",
  "hint": "Work out the discriminant; its sign gives the count.",
  "misconceptions":[
    {"pattern":"always_two","check":"always_two","expect":2,
     "message":"The discriminant is 4 − 20 = −16, negative, so there are no real roots. A quadratic does not always have two."},
  ],
  "guided_steps":[
    say("Count roots from the discriminant \\(b^2 - 4ac\\). Read a = 1, b = 2, c = 5."),
    box("b squared: 2² = ", 4, "Square the coefficient of x."),
    box("4ac: 4 × 1 × 5 = ", 20, "Multiply four, a and c.", phase="substitute"),
    box("discriminant: 4 − 20 = ", -16, "b squared minus 4ac.", phase="substitute"),
    box("it is negative, so the number of real roots is ", 0,
        "Positive gives 2, zero gives 1, negative gives 0.", phase="substitute",
        done="Negative discriminant means no real roots."),
  ]},
 { # 7
  "display": "Solve \\(x^2 + 6x + 5 = 0\\) using the formula. Enter the solution closer to zero.",
  "solutions": [-1], "calculator": True, "input_type": "single_value",
  "hint": "Both roots are negative; the one closer to zero uses the + sign.",
  "misconceptions":[
    {"pattern":"took_farther","check":"took_farther","expect":-5,
     "message":"That is the root farther from zero. The one closer uses the + sign: (−6 + 4) ÷ 2 = −1."},
    {"pattern":"plus_b","check":"plus_b","expect":1,
     "message":"The formula uses −b on top, so −6 not +6: (−6 + 4) ÷ 2 = −1. Using +6 gives 1."},
  ],
  "guided_steps":[
    say("Use the formula with a = 1, b = 6, c = 5. Note −b = −6."),
    box("4ac: 4 × 1 × 5 = ", 20, "Multiply four, a and c."),
    box("discriminant: 6² − 20 = 36 − 20 = ", 16, "b squared minus 4ac.", phase="substitute"),
    box("square root: √16 = ", 4, "A whole-number root here.", phase="substitute"),
    box("closer to zero (use +): (−6 + 4) ÷ 2 = ", -1, "Take the + option, then divide by 2.", phase="substitute",
        done="x = −1 (the other is −5). Check: (−1)² + 6(−1) + 5 = 0."),
  ]},
]
for i,p in enumerate(bronze): p["_i"]=i

# =====================================================================
# SILVER
# =====================================================================
silver = [
 { # 0
  "display": "Solve \\(x^2 + 3x - 7 = 0\\). Give the positive root to 2 d.p.",
  "solutions": [1.54], "calculator": True, "input_type": "single_value",
  "hint": "Use the formula; the positive root takes the + sign.",
  "misconceptions":[
    {"pattern":"plus_b","check":"plus_b","expect":4.54,
     "message":"Use −b on top, and here b = 3 so −b = −3: (−3 + 6.08) ÷ 2 = 1.54. Using +3 gives 4.54."},
  ],
  "guided_steps":[
    say("Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 3, c = −7."),
    box("4ac: 4 × 1 × −7 = ", -28, "Multiply four, a and c, keeping signs."),
    box("discriminant: 9 − (−28) = ", 37, "b squared minus 4ac; two minuses add.", phase="substitute"),
    box("square root of 37, to 2 d.p. = ", 6.08, "Use a calculator.", phase="substitute"),
    box("positive root: (−3 + 6.08) ÷ 2 = ", 1.54, "Take the + option, then divide by 2a = 2.", phase="substitute",
        done="x ≈ 1.54. Substitute back to check."),
  ]},
 { # 1
  "display": "Write \\(x^2 - 4x + 1\\) in the form \\((x-p)^2 + q\\). What is \\(q\\)?",
  "solutions": [-3], "calculator": False, "input_type": "single_value",
  "hint": "Square the half, then subtract it from 1.",
  "misconceptions":[
    {"pattern":"added_square","check":"added_square","expect":5,
     "message":"Subtract the square: 1 − 4 = −3. Adding it gives 5."},
    {"pattern":"used_c","check":"used_c","expect":1,
     "message":"You still adjust the constant: 1 − 4 = −3. Leaving it as 1 skips the correction."},
  ],
  "guided_steps":[
    say("Complete the square on \\(x^2 - 4x + 1\\). Halve the coefficient of x."),
    box("half of −4 = ", -2, "Divide the coefficient of x by 2, keep the sign."),
    box("square it: (−2)² = ", 4, "The half times itself.", phase="substitute"),
    box("adjust the constant: 1 − 4 = ", -3, "Original constant minus the square.", phase="substitute",
        done="So (x − 2)² − 3; q = −3."),
  ]},
 { # 2
  "display": "Find the turning point of \\(y = x^2 + 6x + 2\\). What is the y-coordinate?",
  "solutions": [-7], "calculator": False, "input_type": "single_value",
  "hint": "The y-coordinate is the constant after completing the square.",
  "misconceptions":[
    {"pattern":"used_c","check":"used_c","expect":2,
     "message":"The y-coordinate is 2 − 9 = −7, not the original constant 2."},
    {"pattern":"added_square","check":"added_square","expect":11,
     "message":"Subtract the square: 2 − 9 = −7. Adding it gives 11."},
  ],
  "guided_steps":[
    say("The y-coordinate of the turning point is the constant after completing the square. Halve the 6."),
    box("half of 6 = ", 3, "Divide the coefficient of x by 2."),
    box("square it: 3² = ", 9, "The half times itself.", phase="substitute"),
    box("y-coordinate: 2 − 9 = ", -7, "Original constant minus the square.", phase="substitute",
        done="(x + 3)² − 7, turning point (−3, −7); y = −7."),
  ]},
 { # 3
  "display": "Solve \\(2x^2 - 5x + 1 = 0\\). Give the larger root to 2 d.p.",
  "solutions": [2.28], "calculator": True, "input_type": "single_value",
  "hint": "Divide the whole top by 2a, and here 2a = 4.",
  "misconceptions":[
    {"pattern":"divide_by_two","check":"divide_by_two","expect":4.56,
     "message":"Divide by 2a = 4, not 2: (5 + 4.12) ÷ 4 = 2.28. Dividing by 2 gives 4.56."},
    {"pattern":"took_smaller","check":"took_smaller","expect":0.22,
     "message":"That is the smaller root. The larger uses the + sign: (5 + 4.12) ÷ 4 = 2.28."},
  ],
  "guided_steps":[
    say("Use the formula with a = 2, b = −5, c = 1. Note 2a = 4."),
    box("4ac: 4 × 2 × 1 = ", 8, "Multiply four, a and c."),
    box("discriminant: 25 − 8 = ", 17, "b squared minus 4ac.", phase="substitute"),
    box("square root of 17, to 2 d.p. = ", 4.12, "Use a calculator.", phase="substitute"),
    box("larger root: (5 + 4.12) ÷ 4 = ", 2.28, "Take the + option, then divide by 2a = 4.", phase="substitute",
        done="x ≈ 2.28. Divide by 2a = 4, not 2."),
  ]},
 { # 4
  "display": "Solve \\(3x^2 + 2x - 4 = 0\\). Give the positive root to 2 d.p.",
  "solutions": [0.87], "calculator": True, "input_type": "single_value",
  "hint": "Here 2a = 6; divide the whole numerator by it.",
  "misconceptions":[
    {"pattern":"divide_by_two","check":"divide_by_two","expect":2.61,
     "message":"Divide by 2a = 6, not 2: (−2 + 7.21) ÷ 6 = 0.87. Dividing by 2 gives 2.61."},
  ],
  "guided_steps":[
    say("Use the formula with a = 3, b = 2, c = −4. Note 2a = 6."),
    box("4ac: 4 × 3 × −4 = ", -48, "Multiply four, a and c, keeping signs."),
    box("discriminant: 4 − (−48) = ", 52, "b squared minus 4ac; two minuses add.", phase="substitute"),
    box("square root of 52, to 2 d.p. = ", 7.21, "Use a calculator.", phase="substitute"),
    box("positive root: (−2 + 7.21) ÷ 6 = ", 0.87, "Take the + option, then divide by 2a = 6.", phase="substitute",
        done="x ≈ 0.87. Divide by 2a = 6."),
  ]},
 { # 5
  "display": "Write \\(x^2 + 2x - 5\\) in completed square form. What is the minimum value of the expression?",
  "solutions": [-6], "calculator": False, "input_type": "single_value",
  "hint": "The minimum value is the constant after completing the square.",
  "misconceptions":[
    {"pattern":"used_c","check":"used_c","expect":-5,
     "message":"The minimum is −5 − 1 = −6, not the original constant −5."},
    {"pattern":"added_square","check":"added_square","expect":-4,
     "message":"Subtract the square: −5 − 1 = −6. Adding it gives −4."},
  ],
  "guided_steps":[
    say("The minimum value is the constant after completing the square. Halve the 2."),
    box("half of 2 = ", 1, "Divide the coefficient of x by 2."),
    box("square it: 1² = ", 1, "The half times itself.", phase="substitute"),
    box("minimum value: −5 − 1 = ", -6, "Original constant minus the square.", phase="substitute",
        done="(x + 1)² − 6, least value −6 at x = −1."),
  ]},
 { # 6  (display clarified: was ambiguous 'How many roots?')
  "display": "Find the discriminant of \\(4x^2 - 12x + 9 = 0\\), then state how many distinct real roots it has.",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "A zero discriminant means one repeated root.",
  "misconceptions":[
    {"pattern":"equal_counts_two","check":"equal_counts_two","expect":2,
     "message":"A zero discriminant gives one repeated root, so one distinct real root, not two."},
    {"pattern":"gave_discriminant","check":"gave_discriminant","expect":0,
     "message":"The discriminant is 0, but the question asks for the number of distinct roots, which is 1."},
  ],
  "guided_steps":[
    say("Count roots from the discriminant \\(b^2 - 4ac\\). Read a = 4, b = −12, c = 9."),
    box("b squared: (−12)² = ", 144, "Square the coefficient of x."),
    box("4ac: 4 × 4 × 9 = ", 144, "Multiply four, a and c.", phase="substitute"),
    box("discriminant: 144 − 144 = ", 0, "b squared minus 4ac.", phase="substitute"),
    box("a zero discriminant gives one repeated root, so distinct real roots = ", 1,
        "Zero gives one repeated root.", phase="substitute",
        done="Discriminant 0 means one repeated root."),
  ]},
]
for i,p in enumerate(silver): p["_i"]=i

# =====================================================================
# GOLD
# =====================================================================
gold = [
 { # 0
  "display": "Solve \\(x^2 + 4x + 1 = 0\\) by completing the square. Give the positive root in surd form: \\(-2 + \\sqrt{n}\\). What is \\(n\\)?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Complete the square, then read n from (x + 2)² = n.",
  "misconceptions":[
    {"pattern":"dropped_plus1","check":"dropped_plus1","expect":4,
     "message":"After −4 + 1 the constant is −3, so (x + 2)² = 3 and n = 3. Ignoring the +1 gives 4."},
  ],
  "guided_steps":[
    say("Complete the square. Halve the 4 to get 2, giving \\((x + 2)^2\\)."),
    box("the correction to subtract is 2² = ", 4, "Square the half."),
    box("constant after completing: −4 + 1 = ", -3, "Take off 4, add the original 1.", phase="substitute"),
    box("so (x + 2)² = 3, and comparing −2 + √n gives n = ", 3, "The number left on the right.", phase="substitute",
        done="x = −2 ± √3; positive root −2 + √3, so n = 3."),
  ]},
 { # 1
  "display": "For what values of \\(k\\) does \\(x^2 + kx + 9 = 0\\) have equal roots? Give the positive value.",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Equal roots means b² − 4ac = 0; solve for k.",
  "misconceptions":[
    {"pattern":"forgot_sqrt","check":"forgot_sqrt","expect":36,
     "message":"k² = 36 gives k = 6 after square-rooting. Stopping at k² = 36 leaves 36."},
  ],
  "guided_steps":[
    say("Equal roots means the discriminant is 0. Here a = 1, b = k, c = 9."),
    box("4ac: 4 × 1 × 9 = ", 36, "Multiply four, a and c."),
    box("set k² − 36 = 0, so k² = ", 36, "Move 36 across.", phase="substitute"),
    box("positive k = √36 = ", 6, "Square root, take the positive value.", phase="substitute",
        done="k = 6 (and −6); the positive value is 6."),
  ]},
 { # 2
  "display": "Write \\(2x^2 + 12x + 5\\) in the form \\(a(x+p)^2 + q\\). What is \\(q\\)?",
  "solutions": [-13], "calculator": False, "input_type": "single_value",
  "hint": "Factor the 2 out first, then complete the square inside.",
  "misconceptions":[
    {"pattern":"forgot_multiply","check":"forgot_multiply","expect":-4,
     "message":"The −9 inside is multiplied by the 2 outside: 2 × (−9) = −18, then −18 + 5 = −13. Forgetting the ×2 gives −4."},
  ],
  "guided_steps":[
    say("Factor the 2 from the first two terms: \\(2(x^2 + 6x) + 5\\)."),
    box("half of the 6 inside is ", 3, "Half of six."),
    box("the 2 outside times that square: 2 × 3² = ", 18, "Two times three-squared.", phase="substitute"),
    box("q = −18 + 5 = ", -13, "Subtract the 18, add the 5.", phase="substitute",
        done="So 2(x + 3)² − 13; q = −13."),
  ]},
 { # 3
  "display": "Solve \\(5x^2 - 2x - 1 = 0\\). Give the positive root to 3 d.p.",
  "solutions": [0.69], "calculator": True, "input_type": "single_value",
  "hint": "Use the formula; here 2a = 10.",
  "misconceptions":[
    {"pattern":"divide_by_two","check":"divide_by_two","expect":3.45,
     "message":"Divide by 2a = 10, not 2: (2 + 4.899) ÷ 10 = 0.690. Dividing by 2 gives 3.45."},
  ],
  "guided_steps":[
    say("Use the formula with a = 5, b = −2, c = −1. Note 2a = 10."),
    box("4ac: 4 × 5 × −1 = ", -20, "Multiply four, a and c, keeping signs."),
    box("discriminant: 4 − (−20) = ", 24, "b squared minus 4ac; two minuses add.", phase="substitute"),
    box("square root of 24, to 3 d.p. = ", 4.899, "Use a calculator.", phase="substitute"),
    box("positive root: (2 + 4.899) ÷ 10 = ", 0.69, "Take the + option, then divide by 2a = 10.", phase="substitute",
        done="x ≈ 0.690. Divide by 2a = 10."),
  ]},
 { # 4
  "display": "The equation \\(2x^2 + px + 8 = 0\\) has no real roots. What is the largest integer value of \\(p\\)?",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "No real roots means b² − 4ac < 0; here that is p² < 64.",
  "misconceptions":[
    {"pattern":"took_boundary","check":"took_boundary","expect":8,
     "message":"p = 8 gives p² = 64, which is equal roots, not none. For no real roots p must be below 8, so the largest integer is 7."},
  ],
  "guided_steps":[
    say("No real roots means the discriminant is negative: \\(p^2 - 4ac < 0\\). Here a = 2, c = 8."),
    box("4ac: 4 × 2 × 8 = ", 64, "Multiply four, a and c."),
    box("so we need p² < 64; the boundary is √64 = ", 8, "Square root of 64.", phase="substitute"),
    box("p must be below 8, so the largest integer p is ", 7, "Just under the boundary.", phase="substitute",
        done="p² < 64 means −8 < p < 8; largest integer is 7."),
  ]},
]
for i,p in enumerate(gold): p["_i"]=i

# =====================================================================
# tier descriptions
# =====================================================================
bronze_description = "Read a, b and c, find the discriminant b² − 4ac, complete the square on a simple x² + bx, and read off how many roots there are."
silver_description = "Solve with the quadratic formula to a given accuracy, complete the square with a constant term, and find turning points and minimum values."
gold_description   = "Handle a in front of x², work in surd form, and use the discriminant as a condition on an unknown (equal roots, no real roots)."

# =====================================================================
# tier_guides
# =====================================================================
tier_guides = {
 "bronze": {
   "title": "Bronze: a, b, c, the discriminant, and simple squares",
   "steps": [
     "Every quadratic \\(ax^2 + bx + c = 0\\) hands you three numbers: a, b and c. Read them off, keeping every minus sign.",
     "The <strong>discriminant</strong> is \\(b^2 - 4ac\\). Its sign counts the roots: positive gives 2, zero gives 1, negative gives none.",
     "To complete the square on \\(x^2 + bx\\): halve b, then subtract the square of that half. So \\(x^2 + 6x = (x+3)^2 - 9\\).",
   ],
   "example": {
     "question": "For \\(x^2 + 2x - 8 = 0\\), find the discriminant.",
     "steps": [
       {"label":"Read off","content":"a = 1, b = 2, c = −8"},
       {"label":"b squared","content":"\\(2^2 = 4\\)"},
       {"label":"4ac","content":"\\(4 × 1 × (−8) = −32\\)"},
       {"label":"Check the subtraction","content":"\\(4 − (−32) = 4 + 32\\)"},
       {"label":"Answer","content":"Discriminant = 36 (positive, so two roots)","isAnswer":True,"is_answer":True},
     ],
   },
 },
 "silver": {
   "title": "Silver: the quadratic formula and completed squares",
   "steps": [
     "When a quadratic will not factorise, use \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\). Work out the discriminant, then its square root.",
     "The \\(\\pm\\) gives two answers: + for the larger root, − for the smaller. Divide the whole top by \\(2a\\), not just part of it.",
     "Completing the square \\(x^2 + bx + c = (x + p)^2 + q\\) puts the turning point at \\((-p, q)\\) and the minimum value at q.",
   ],
   "example": {
     "question": "Solve \\(x^2 + 4x + 1 = 0\\) to 2 d.p.",
     "steps": [
       {"label":"Discriminant","content":"\\(4^2 - 4(1)(1) = 12\\)"},
       {"label":"Square root","content":"\\(\\sqrt{12} = 3.46\\)"},
       {"label":"Check both roots","content":"\\((-4 ± 3.46) ÷ 2\\)"},
       {"label":"Answer","content":"x = −0.27 or x = −3.73","isAnswer":True,"is_answer":True},
     ],
   },
 },
 "gold": {
   "title": "Gold: harder squares and the discriminant as a condition",
   "steps": [
     "When \\(a \\neq 1\\), factor a out of the first two terms first: \\(2x^2 + 8x = 2(x^2 + 4x)\\), then complete the square inside.",
     "The discriminant is also a <strong>condition</strong>: equal roots means \\(b^2 - 4ac = 0\\); no real roots means \\(b^2 - 4ac < 0\\). Set it up and solve for the unknown.",
     "The completed form \\(a(x + p)^2 + q\\) gives the minimum value \\(q\\) straight away, reached at \\(x = -p\\).",
   ],
   "example": {
     "question": "Find the minimum value of \\(x^2 - 6x + 11\\).",
     "steps": [
       {"label":"Halve the −6","content":"half is −3, so \\((x - 3)^2\\)"},
       {"label":"Adjust","content":"\\((x-3)^2 - 9 + 11\\)"},
       {"label":"Check","content":"\\(-9 + 11 = 2\\)"},
       {"label":"Answer","content":"Minimum value = 2, at x = 3","isAnswer":True,"is_answer":True},
     ],
   },
 },
}

# =====================================================================
# guided: opener (geometric completing-the-square, with SVG) + teach walks
# =====================================================================
opener_svg = (
 '<svg viewBox="0 0 250 205" role="img" aria-label="A big square split into an x by x square, two strips, and a small corner square" style="max-width:250px">'
 '<rect x="45" y="12" width="120" height="120" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor"/>'
 '<rect x="165" y="12" width="40" height="120" fill="#34d399" fill-opacity="0.3" stroke="currentColor"/>'
 '<rect x="45" y="132" width="120" height="40" fill="#34d399" fill-opacity="0.3" stroke="currentColor"/>'
 '<rect x="165" y="132" width="40" height="40" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor"/>'
 '<text x="105" y="8" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">x</text>'
 '<text x="185" y="8" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">?</text>'
 '<text x="38" y="76" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">x</text>'
 '<text x="38" y="156" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">?</text>'
 '<text x="105" y="78" font-family="Inter" font-size="12" fill="currentColor" text-anchor="middle">x²</text>'
 '<text x="185" y="78" font-family="Inter" font-size="10" fill="currentColor" text-anchor="middle">strip</text>'
 '<text x="105" y="156" font-family="Inter" font-size="10" fill="currentColor" text-anchor="middle">strip</text>'
 '<text x="185" y="156" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">?</text>'
 '</svg>'
)

guided = {
 "opener": {
   "display": opener_svg + "You have a square tile, x by x. Someone hands you 8 thin strips, each x long, and asks you to build ONE bigger square from the tile and the strips.",
   "steps": [
     say("To grow the tile into a bigger square you add the same amount along two touching sides, the right and the bottom. So share the 8 strips equally between them."),
     box("8 strips shared equally between 2 sides means each side gets ", 4, "Half of 8.", post=" strips"),
     say("Now the big square has side (x + 4), but its bottom-right corner is still an empty hole. You fill it with one small square, 4 by 4."),
     box("area of that little corner square, 4 × 4 = ", 16, "Four times four."),
     say("So the tile plus 8 strips, that is \\(x^2 + 8x\\), makes an \\((x+4)^2\\) square with a 16 hole you had to fill. In symbols: \\(x^2 + 8x = (x+4)^2 - 16\\). Halving the 8, then taking off the square of that half, <strong>is</strong> completing the square."),
   ],
 },
 "teach": {
   "bronze": {
     "display": "For \\(x^2 + 7x + 3 = 0\\), find the discriminant, then say how many real roots it has.",
     "steps": [
       say("The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 7, c = 3."),
       box("b squared: 7 × 7 = ", 49, "Seven times seven."),
       box("4ac: 4 × 1 × 3 = ", 12, "Multiply all three together."),
       box("discriminant: 49 − 12 = ", 37, "Subtract the second from the first."),
       box("37 is positive, so the number of real roots is ", 2, "Positive discriminant means two real roots.",
           done="Positive discriminant, two roots. That is the whole point."),
     ],
   },
   "silver": {
     "display": "Solve \\(x^2 + 4x + 1 = 0\\) with the quadratic formula. Give both roots to 2 d.p.",
     "steps": [
       say("Here a = 1, b = 4, c = 1, so \\(x = \\frac{-4 \\pm \\sqrt{4^2 - 4(1)(1)}}{2}\\)."),
       box("4ac: 4 × 1 × 1 = ", 4, "Multiply all three."),
       box("discriminant: 16 − 4 = ", 12, "b squared minus 4ac."),
       box("square root of 12, to 2 d.p. = ", 3.46, "Use a calculator."),
       box("larger root: (−4 + 3.46) ÷ 2 = ", -0.27, "Use the plus, then divide by 2a = 2."),
       box("smaller root: (−4 − 3.46) ÷ 2 = ", -3.73, "Use the minus, then divide by 2.",
           done="Two roots from one formula. The ± did the work."),
     ],
   },
   "gold": {
     "display": "Write \\(2x^2 + 8x + 3\\) in the form \\(a(x + p)^2 + q\\).",
     "steps": [
       say("The a here is 2. Factor it out of the first two terms: \\(2(x^2 + 4x) + 3\\)."),
       box("coefficient of x inside the bracket = ", 4, "The number in front of x once 2 is taken out."),
       box("halve it to get p: 4 ÷ 2 = ", 2, "Half of four."),
       box("the 2 outside multiplies the correction 2²: 2 × 4 = ", 8, "Two times two-squared."),
       box("q = −8 + 3 = ", -5, "Subtract the correction, then add the original constant."),
       box("check by expanding: 2 × 2² + q = 8 + (−5) = ", 3, "It should return the original constant, 3.",
           done="Back to +3, so 2(x + 2)² − 5 is right."),
     ],
   },
 },
}

# strip helper key
for arr in (bronze, silver, gold):
    for p in arr:
        p.pop("_i", None)

pd = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": {
   "bronze": bronze,
   "silver": silver,
   "gold": gold,
   "bronze_description": bronze_description,
   "silver_description": silver_description,
   "gold_description": gold_description,
 },
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

with io.open("lesson_maths-ocr_algebra-L08.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("written lesson_maths-ocr_algebra-L08.json")
