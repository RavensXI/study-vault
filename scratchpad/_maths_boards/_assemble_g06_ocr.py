# -*- coding: utf-8 -*-
"""Assemble full practice_data for maths-ocr geometry-L06 and self-verify."""
import json, math, importlib.util

spec = importlib.util.spec_from_file_location('b', '_build_g06_ocr.py')
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
figs = B.figs
CAP = B.CAP
R = math.radians

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def sayonly(s): return {"say": s}

# preserve
live = json.load(open("_live_g06_ocr.json", encoding="utf-8"))
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]
topic_links = live["topic_links"]

def fig(k, text):
    return figs[k] + CAP + text

# ================================================================ BRONZE
bronze = []
# b0 area 8,6,90 -> 24
bronze.append({
  "display": fig('b0', "Find the area of this triangle: sides 8 cm and 6 cm with the included angle 90°."),
  "solutions": [24], "calculator": True, "input_type": "single_value",
  "hint": "Area = ½ × the two sides × the sine of the angle between them.",
  "guided_steps": [
    sayonly("Area of a triangle: \\(\\frac12 ab\\sin C\\). The two sides are 8 and 6 with the included angle 90°."),
    box("Half the product of the sides: ½ × 8 × 6 = ", 24.0, "Multiply 8 and 6, then halve."),
    box("Sine of the angle: sin 90° = ", 1.0, "sin 90 on the calculator.", phase="substitute"),
    box("Multiply: 24 × 1 = ", 24, "Product of the two.", done="So the area = 24 cm²."),
    box("Check the units: the area to 1 d.p. is ", 24, "Same value, in cm².", done="Area = 24 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "no_half", "expect": 48, "note": "8*6*sin90",
     "message": "You left out the ½. Area = ½ × 8 × 6 × sin 90° = 24 cm². Without the half you get 48 cm², which is twice too big."},
  ]})
# b1 area 10,12,30 -> 30
bronze.append({
  "display": fig('b1', "Find the area of this triangle: sides 10 and 12 with the included angle 30°."),
  "solutions": [30], "calculator": True, "input_type": "single_value",
  "hint": "Area = ½ × the two sides × the sine of the angle between them.",
  "guided_steps": [
    sayonly("Area of a triangle: \\(\\frac12 ab\\sin C\\). The two sides are 10 and 12 with the included angle 30°."),
    box("Half the product of the sides: ½ × 10 × 12 = ", 60.0, "Multiply 10 and 12, then halve."),
    box("Sine of the angle: sin 30° = ", 0.5, "sin 30 is exactly 0.5.", phase="substitute"),
    box("Multiply: 60 × 0.5 = ", 30, "Product of the two.", done="So the area = 30 cm²."),
    box("Check the units: the area to 1 d.p. is ", 30, "Same value, in cm².", done="Area = 30 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "no_half", "expect": 60, "note": "10*12*sin30",
     "message": "You left out the ½. Area = ½ × 10 × 12 × sin 30° = 30 cm². Without the half you get 60 cm²."},
  ]})
# b2 area 5,8,60 -> 17.3
bronze.append({
  "display": fig('b2', "Find the area of this triangle: sides 5 and 8 with the included angle 60°. Give to 1 d.p."),
  "solutions": [17.3], "calculator": True, "input_type": "single_value",
  "hint": "Area = ½ × the two sides × the sine of the angle between them.",
  "guided_steps": [
    sayonly("Area of a triangle: \\(\\frac12 ab\\sin C\\). The two sides are 5 and 8 with the included angle 60°."),
    box("Half the product of the sides: ½ × 5 × 8 = ", 20.0, "Multiply 5 and 8, then halve."),
    box("Sine of the angle: sin 60° = ", 0.8660, "sin 60 on the calculator, 4 d.p.", phase="substitute"),
    box("Multiply: 20 × 0.8660 = ", 17.3, "Product of the two, 1 d.p.", done="So the area = 17.3 cm²."),
    box("Check the units: the area to 1 d.p. is ", 17.3, "Same value, in cm².", done="Area = 17.3 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "no_half", "expect": 34.6, "note": "5*8*sin60",
     "message": "You left out the ½. Area = ½ × 5 × 8 × sin 60° = 17.3 cm². Without the half you get 34.6 cm²."},
  ]})
# b3 cosine a: b5,c7,A90 -> 8.6
bronze.append({
  "display": fig('b3', "Use the cosine rule to find side \\(a\\): \\(b = 5\\), \\(c = 7\\), \\(A = 90°\\). Give to 1 d.p."),
  "solutions": [8.6], "calculator": True, "input_type": "single_value",
  "hint": "a² = b² + c² − 2bc cos A, then take the square root.",
  "guided_steps": [
    sayonly("Cosine rule for a side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\), with \\(b=5\\), \\(c=7\\), \\(A=90°\\)."),
    box("Square and add: 5² + 7² = 25 + 49 = ", 74, "Square each, then add."),
    box("The last term: 2 × 5 × 7 × cos 90° = ", 0.0, "cos 90 = 0, so the whole term is 0.", phase="substitute"),
    box("So a² = 74 − 0 = ", 74, "Subtract.", done="a² = 74."),
    box("Square root: √74 = ", 8.6, "Square root, 1 d.p.", done="So a = 8.6."),
  ],
  "misconceptions": [
    {"pattern": "no_sqrt", "expect": 74, "note": "stops at a^2",
     "message": "You stopped at a². Here a² = 25 + 49 − 0 = 74, so you still need the square root: a = √74 = 8.6."},
  ]})
# b4 multiple choice
bronze.append({
  "display": "Which rule needs a matched side-angle pair (a side together with the angle opposite it)?",
  "options": ["Sine rule", "Cosine rule", "Area formula", "Pythagoras"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "One rule reads \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\): each side over the sine of its opposite angle.",
  "misconceptions": [
    {"pattern": "confused", "expect": None, "note": "sine rule pairs side with opposite angle",
     "message": "The sine rule, \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\), pairs each side with the angle opposite it, so it needs a complete pair to start."},
  ]})
# b5 area 9,9,45 -> 28.6
bronze.append({
  "display": fig('b5', "Find the area of this triangle: sides 9 and 9 with the included angle 45°. Give to 1 d.p."),
  "solutions": [28.6], "calculator": True, "input_type": "single_value",
  "hint": "Area = ½ × the two sides × the sine of the angle between them.",
  "guided_steps": [
    sayonly("Area of a triangle: \\(\\frac12 ab\\sin C\\). The two sides are 9 and 9 with the included angle 45°."),
    box("Half the product of the sides: ½ × 9 × 9 = ", 40.5, "Multiply 9 and 9, then halve."),
    box("Sine of the angle: sin 45° = ", 0.7071, "sin 45 on the calculator, 4 d.p.", phase="substitute"),
    box("Multiply: 40.5 × 0.7071 = ", 28.6, "Product of the two, 1 d.p.", done="So the area = 28.6 cm²."),
    box("Check the units: the area to 1 d.p. is ", 28.6, "Same value, in cm².", done="Area = 28.6 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "no_half", "expect": 57.3, "note": "9*9*sin45",
     "message": "You left out the ½. Area = ½ × 9 × 9 × sin 45° = 28.6 cm². Without the half you get 57.3 cm²."},
  ]})
# b6 cosine angle SSS 6,8,10 -> C=90
bronze.append({
  "display": fig('b6', "Use the cosine rule to find angle \\(C\\): \\(a = 6\\), \\(b = 8\\), \\(c = 10\\)."),
  "solutions": [90], "calculator": True, "input_type": "single_value",
  "hint": "cos C = (a² + b² − c²) ÷ (2ab), then take the inverse cosine.",
  "guided_steps": [
    sayonly("Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\), with \\(a=6\\), \\(b=8\\), \\(c=10\\)."),
    box("Top line: 6² + 8² − 10² = 36 + 64 − 100 = ", 0, "Square all three, then combine."),
    box("Bottom line: 2 × 6 × 8 = ", 96, "2 × 6 × 8."),
    box("So cos C = 0 ÷ 96 = ", 0.0, "Divide.", phase="substitute"),
    box("Angle C: cos⁻¹(0) = ", 90, "Inverse cosine of 0.", done="So C = 90°: the triangle is right angled."),
  ],
  "misconceptions": [
    {"pattern": "no_inverse", "expect": 0, "note": "types cos value not angle",
     "message": "cos C = 0 is only the cosine, not the angle. Take the inverse: cos⁻¹(0) = 90°."},
  ]})
# b7 sine ratio a/sinA a10 A30 -> 20
bronze.append({
  "display": "Sine rule: a triangle has side \\(a = 10\\) opposite angle \\(A = 30°\\). Find the ratio \\(a/\\sin A\\).",
  "solutions": [20], "calculator": True, "input_type": "single_value",
  "hint": "Divide the side by the sine of its opposite angle.",
  "guided_steps": [
    sayonly("The sine rule ratio is \\(\\frac{a}{\\sin A}\\): a side divided by the sine of the angle facing it."),
    box("Sine of the angle: sin 30° = ", 0.5, "sin 30 is exactly 0.5."),
    box("Divide: 10 ÷ 0.5 = ", 20, "Side divided by the sine.", phase="substitute", done="So a/sin A = 20."),
    box("Check: this ratio × sin 30° should return the side: 20 × 0.5 = ", 10, "Should give back a = 10.", done="Back to a = 10, so the ratio 20 is right."),
  ],
  "misconceptions": [
    {"pattern": "wrong_operation", "expect": 5, "note": "10*sin30",
     "message": "You multiplied instead of dividing: 10 × sin 30° = 5. The ratio is a ÷ sin A = 10 ÷ 0.5 = 20."},
  ]})

# ================================================================ SILVER
silver = []
# s0 cosine a: b8,c11,A55 -> 9.2
silver.append({
  "display": fig('s0', "Use the cosine rule to find side \\(a\\): \\(b = 8\\), \\(c = 11\\), \\(A = 55°\\). Give to 1 d.p."),
  "solutions": [9.2], "calculator": True, "input_type": "single_value",
  "hint": "a² = b² + c² − 2bc cos A, then take the square root.",
  "guided_steps": [
    sayonly("Cosine rule for a side: \\(a^2 = b^2 + c^2 - 2bc\\cos A = 8^2 + 11^2 - 2(8)(11)\\cos 55°\\)."),
    box("Square and add: 8² + 11² = 64 + 121 = ", 185, "Square each, then add."),
    box("The last term: 2 × 8 × 11 × cos 55° = ", 100.9495, "2 × 8 × 11 × cos 55, 4 d.p.", phase="substitute"),
    box("So a² = 185 − 100.9495 = ", 84.0505, "Subtract.", done="a² = 84.0505."),
    box("Square root: √84.0505 = ", 9.2, "Square root, 1 d.p.", done="So a = 9.2."),
  ],
  "misconceptions": [
    {"pattern": "sign_add", "expect": 16.9, "note": "185+100.9494=285.9494 sqrt",
     "message": "You added the last term instead of subtracting it. It is subtracted: a² = 185 − 100.9 = 84.1, so a = 9.2. Adding gives a = 16.9."},
    {"pattern": "no_sqrt", "expect": 84.1, "note": "stops at a^2 rounded 1dp",
     "message": "You stopped at a² = 84.1. Take the square root for the side: a = √84.1 = 9.2."},
  ]})
# s1 sine b: a15,A65,B42 -> 11.1
silver.append({
  "display": fig('s1', "Use the sine rule to find side \\(b\\): \\(a = 15\\), \\(A = 65°\\), \\(B = 42°\\). Give to 1 d.p."),
  "solutions": [11.1], "calculator": True, "input_type": "single_value",
  "hint": "The unknown side sits over its own angle: b = a sin B ÷ sin A.",
  "guided_steps": [
    sayonly("Sine rule: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\). You know the pair (\\(a=15\\), \\(A=65°\\)) and angle \\(B=42°\\), so \\(b = \\frac{a\\sin B}{\\sin A}\\)."),
    box("Top line: 15 × sin 42° = ", 10.0370, "15 × sin 42, 4 d.p."),
    box("Bottom line: sin 65° = ", 0.9063, "sin 65, 4 d.p.", phase="substitute"),
    box("Divide: 10.0370 ÷ 0.9063 = ", 11.1, "Top divided by bottom, 1 d.p.", done="So b = 11.1."),
    box("Check: 11.1 × sin 65° ÷ sin 42° rounds to ", 15, "Should return the known side a.", done="Back to a = 15, so b = 11.1 is right."),
  ],
  "misconceptions": [
    {"pattern": "inverted_ratio", "expect": 20.3, "note": "15 sin65/sin42",
     "message": "You inverted the fraction. The unknown side sits over its own angle: b = 15 sin 42° ÷ sin 65° = 11.1, not 15 sin 65° ÷ sin 42° = 20.3."},
  ]})
# s2 cosine largest angle SSS 7,9,12 -> 96.4
silver.append({
  "display": fig('s2', "Use the cosine rule to find the largest angle of a triangle with sides 7, 9 and 12. Give to 1 d.p."),
  "solutions": [96.4], "calculator": True, "input_type": "single_value",
  "hint": "The largest angle faces the longest side; use cos C = (a² + b² − c²) ÷ (2ab).",
  "guided_steps": [
    sayonly("The largest angle faces the longest side (12). Call it C, with the other sides a=7 and b=9: \\(\\cos C = \\frac{7^2 + 9^2 - 12^2}{2(7)(9)}\\)."),
    box("Top line: 7² + 9² − 12² = 49 + 81 − 144 = ", -14, "Square all three, then combine."),
    box("Bottom line: 2 × 7 × 9 = ", 126, "2 × 7 × 9."),
    box("So cos C = −14 ÷ 126 = ", -0.1111, "Divide, 4 d.p. Keep the minus.", phase="substitute"),
    box("Angle C: cos⁻¹(−0.1111) = ", 96.4, "Inverse cosine, 1 d.p. A negative cosine gives an obtuse angle.", done="So the largest angle = 96.4°."),
  ],
  "misconceptions": [
    {"pattern": "sign_slip", "expect": 83.6, "note": "arccos(+0.1111)",
     "message": "You dropped the minus sign. cos C = −0.1111 gives an obtuse angle of 96.4°. Using +0.1111 gives 83.6°, which is acute and cannot be the largest angle."},
  ]})
# s3 area 13,17,72 -> 105.1
silver.append({
  "display": fig('s3', "Find the area of this triangle: sides 13 and 17 with the included angle 72°. Give to 1 d.p."),
  "solutions": [105.1], "calculator": True, "input_type": "single_value",
  "hint": "Area = ½ × the two sides × the sine of the angle between them.",
  "guided_steps": [
    sayonly("Area of a triangle: \\(\\frac12 ab\\sin C\\). The two sides are 13 and 17 with the included angle 72°."),
    box("Half the product of the sides: ½ × 13 × 17 = ", 110.5, "Multiply 13 and 17, then halve."),
    box("Sine of the angle: sin 72° = ", 0.9511, "sin 72, 4 d.p.", phase="substitute"),
    box("Multiply: 110.5 × 0.9511 = ", 105.1, "Product of the two, 1 d.p.", done="So the area = 105.1 cm²."),
    box("Check the units: the area to 1 d.p. is ", 105.1, "Same value, in cm².", done="Area = 105.1 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "no_half", "expect": 210.2, "note": "13*17*sin72",
     "message": "You left out the ½. Area = ½ × 13 × 17 × sin 72° = 105.1 cm². Without the half you get 210.2 cm²."},
  ]})
# s4 sine angle B: a9,A40,b12 -> 59.0
silver.append({
  "display": fig('s4', "Use the sine rule to find angle \\(B\\): \\(a = 9\\), \\(A = 40°\\), \\(b = 12\\). Give to 1 d.p."),
  "solutions": [59.0], "calculator": True, "input_type": "single_value",
  "hint": "sin B = b sin A ÷ a, then take the inverse sine.",
  "guided_steps": [
    sayonly("Sine rule for an angle: \\(\\frac{\\sin B}{b} = \\frac{\\sin A}{a}\\), so \\(\\sin B = \\frac{b\\sin A}{a} = \\frac{12\\sin 40°}{9}\\)."),
    box("Top line: 12 × sin 40° = ", 7.7135, "12 × sin 40, 4 d.p."),
    box("Divide by 9: 7.7135 ÷ 9 = ", 0.8571, "That is sin B, 4 d.p.", phase="substitute"),
    box("Inverse sine: sin⁻¹(0.8571) = ", 59.0, "Use sin⁻¹, 1 d.p.", done="So B = 59.0°."),
    box("Check the third angle: 180° − 40° − 59.0° = ", 81, "180 minus the two known angles.", done="Angle C = 81°, all positive, so B = 59.0° is the triangle."),
  ],
  "misconceptions": [
    {"pattern": "swapped_sides", "expect": 28.8, "note": "asin(9 sin40/12)",
     "message": "You put the sides the wrong way up. sin B = b sin A ÷ a = 12 sin 40° ÷ 9 = 0.857, giving B = 59.0°. Using 9 sin 40° ÷ 12 gives 28.8°."},
  ]})
# s5 cosine c: a5,b6,C100 -> 8.5
silver.append({
  "display": fig('s5', "Use the cosine rule to find side \\(c\\): \\(a = 5\\), \\(b = 6\\), \\(C = 100°\\). Give to 1 d.p."),
  "solutions": [8.5], "calculator": True, "input_type": "single_value",
  "hint": "c² = a² + b² − 2ab cos C; cos 100° is negative.",
  "guided_steps": [
    sayonly("Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C = 5^2 + 6^2 - 2(5)(6)\\cos 100°\\)."),
    box("Square and add: 5² + 6² = 25 + 36 = ", 61, "Square each, then add."),
    box("The last term: 2 × 5 × 6 × cos 100° = ", -10.4189, "cos 100 = −0.1736, so 60 × (−0.1736), 4 d.p.", phase="substitute"),
    box("So c² = 61 − (−10.4189) = 61 + 10.4189 = ", 71.4189, "Subtracting a negative adds.", done="c² = 71.4189."),
    box("Square root: √71.4189 = ", 8.5, "Square root, 1 d.p.", done="So c = 8.5."),
  ],
  "misconceptions": [
    {"pattern": "sign_cos", "expect": 7.1, "note": "sqrt(61-10.4189)",
     "message": "You treated cos 100° as positive. It is −0.1736, so the term adds: c² = 61 + 10.4 = 71.4 and c = 8.5. Using +0.1736 gives c² = 50.6 and c = 7.1."},
  ]})
# s6 area SSS 5,6,7 -> 14.7
silver.append({
  "display": fig('s6', "A triangle has sides 5, 6 and 7. Find its area by first finding one angle. Give to 1 d.p."),
  "solutions": [14.7], "calculator": True, "input_type": "single_value",
  "hint": "Find an angle with the cosine rule first, then use ½ab sin C.",
  "guided_steps": [
    sayonly("No angle is given. Find the angle C between the sides 5 and 6 (opposite side 7): \\(\\cos C = \\frac{5^2 + 6^2 - 7^2}{2(5)(6)}\\)."),
    box("Top line: 5² + 6² − 7² = 25 + 36 − 49 = ", 12, "Square all three, then combine."),
    box("Bottom line: 2 × 5 × 6 = ", 60, "2 × 5 × 6."),
    box("So cos C = 12 ÷ 60 = ", 0.2, "Divide.", phase="substitute"),
    box("Angle C: cos⁻¹(0.2) = ", 78.5, "Inverse cosine, 1 d.p.", done="C = 78.5°."),
    box("Now the area: ½ × 5 × 6 × sin 78.5° = ", 14.7, "½ × 5 × 6 × sin C, 1 d.p.", done="So the area = 14.7 cm²."),
  ],
  "misconceptions": [
    {"pattern": "assume_right", "expect": 15, "note": "0.5*5*6",
     "message": "You assumed a right angle and did ½ × 5 × 6 = 15. The angle between them is 78.5°, so area = ½ × 5 × 6 × sin 78.5° = 14.7 cm²."},
  ]})

# ================================================================ GOLD
gold = []
# g0 inverse area 40, sides 10,12 -> 41.8
gold.append({
  "display": fig('g0', "A triangle has area 40 cm² and two sides 10 cm and 12 cm. Find the acute included angle to 1 d.p."),
  "solutions": [41.8], "calculator": True, "input_type": "single_value",
  "hint": "Rearrange the area formula: sin C = 2 × area ÷ (ab).",
  "guided_steps": [
    sayonly("Area = \\(\\frac12 ab\\sin C\\), so 40 = ½ × 10 × 12 × sin C. Rearrange for sin C."),
    box("Half the product of the sides: ½ × 10 × 12 = ", 60, "Multiply 10 and 12, then halve."),
    box("Rearrange for sin C: 40 ÷ 60 = ", 0.6667, "Area divided by that number, 4 d.p.", phase="substitute"),
    box("Inverse sine: sin⁻¹(0.6667) = ", 41.8, "Use sin⁻¹, 1 d.p.", done="So the acute angle = 41.8°."),
    box("Check: ½ × 10 × 12 × sin 41.8° rounds to ", 40, "Should return the area.", done="Back to area 40 cm², so 41.8° is right."),
  ],
  "misconceptions": [
    {"pattern": "no_half", "expect": 19.5, "note": "asin(40/120)",
     "message": "You left out the half, dividing by 10 × 12 = 120. That gives sin C = 40 ÷ 120 = 0.333 and C = 19.5°. With the ½ the divisor is 60, giving 41.8°."},
  ]})
# g1 cosine angle SSS 8,9,13 -> 99.6
gold.append({
  "display": fig('g1', "Use the cosine rule to find angle \\(C\\): \\(a = 8\\), \\(b = 9\\), \\(c = 13\\). Give to 1 d.p."),
  "solutions": [99.6], "calculator": True, "input_type": "single_value",
  "hint": "cos C = (a² + b² − c²) ÷ (2ab); the answer is obtuse.",
  "guided_steps": [
    sayonly("Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab} = \\frac{8^2 + 9^2 - 13^2}{2(8)(9)}\\)."),
    box("Top line: 8² + 9² − 13² = 64 + 81 − 169 = ", -24, "Square all three, then combine."),
    box("Bottom line: 2 × 8 × 9 = ", 144, "2 × 8 × 9."),
    box("So cos C = −24 ÷ 144 = ", -0.1667, "Divide, 4 d.p. Keep the minus.", phase="substitute"),
    box("Angle C: cos⁻¹(−0.1667) = ", 99.6, "Inverse cosine, 1 d.p. Negative cosine means obtuse.", done="So C = 99.6°."),
  ],
  "misconceptions": [
    {"pattern": "sign_slip", "expect": 80.4, "note": "arccos(+0.1667)",
     "message": "You dropped the minus sign. cos C = −0.1667 gives an obtuse 99.6°. Using +0.1667 gives 80.4°, but the longest side (13) must face an angle bigger than the others."},
  ]})
# g2 ambiguous sine B: a10,b7,A100 -> 43.6
gold.append({
  "display": fig('g2', "Sine rule (ambiguous case): \\(a = 10\\), \\(b = 7\\), \\(A = 100°\\). Find angle \\(B\\) to 1 d.p."),
  "solutions": [43.6], "calculator": True, "input_type": "single_value",
  "hint": "sin B = b sin A ÷ a; then check whether a second angle would fit.",
  "guided_steps": [
    sayonly("Sine rule for the angle: \\(\\sin B = \\frac{b\\sin A}{a} = \\frac{7\\sin 100°}{10}\\)."),
    box("Top line: 7 × sin 100° = ", 6.8937, "7 × sin 100, 4 d.p."),
    box("Divide by 10: 6.8937 ÷ 10 = ", 0.6894, "That is sin B, 4 d.p.", phase="substitute"),
    box("Inverse sine: sin⁻¹(0.6894) = ", 43.6, "Use sin⁻¹, 1 d.p.", done="The acute value is 43.6°."),
    box("Test the other value: 100° + (180° − 43.6°) = 100° + 136.4° = ", 236.4, "Add A to the obtuse option.", done="236.4° > 180°, so 136.4° is rejected. B = 43.6° only."),
  ],
  "misconceptions": [
    {"pattern": "extra_solution", "expect": 136.4, "note": "180-43.6",
     "message": "You kept the second angle 180° − 43.6° = 136.4°. But 100° + 136.4° > 180°, so it makes no triangle. Here B = 43.6° is the only answer."},
  ]})
# g3 Heron 8,11,15 -> 42.8
gold.append({
  "display": fig('g3', "A triangle has sides 8, 11 and 15. Find its area using Heron's formula. Give to 1 d.p."),
  "solutions": [42.8], "calculator": True, "input_type": "single_value",
  "hint": "s = half the perimeter, then area = √(s(s−a)(s−b)(s−c)).",
  "guided_steps": [
    sayonly("Heron's formula: \\(s = \\frac{a+b+c}{2}\\), then Area \\(= \\sqrt{s(s-a)(s-b)(s-c)}\\)."),
    box("Half the perimeter: (8 + 11 + 15) ÷ 2 = ", 17, "Add the three sides, then halve."),
    box("The product s(s−a)(s−b)(s−c): 17 × 9 × 6 × 2 = ", 1836, "17 × (17−8) × (17−11) × (17−15).", phase="substitute"),
    box("Square root: √1836 = ", 42.8, "Square root, 1 d.p.", done="So the area = 42.8 cm²."),
    box("Check the units: the area to 1 d.p. is ", 42.8, "Same value, in cm².", done="Area = 42.8 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "no_sqrt", "expect": 1836, "note": "stops at product",
     "message": "You stopped at the product 1836. Heron's formula takes the square root: area = √1836 = 42.8 cm²."},
  ]})
# g4 parallelogram 8,12,65 -> 87
gold.append({
  "display": fig('g4', "A parallelogram has adjacent sides 8 cm and 12 cm with the angle between them 65°. Find its area to 1 d.p."),
  "solutions": [87], "calculator": True, "input_type": "single_value",
  "hint": "A parallelogram is two triangles: area = ab sin θ, with no half.",
  "guided_steps": [
    sayonly("A parallelogram is two of these triangles, so its area is \\(ab\\sin\\theta\\) (no half): 8 × 12 × sin 65°."),
    box("Product of the sides: 8 × 12 = ", 96, "Multiply 8 and 12."),
    box("Sine of the angle: sin 65° = ", 0.9063, "sin 65, 4 d.p.", phase="substitute"),
    box("Multiply: 96 × 0.9063 = ", 87, "Product of the two, 1 d.p.", done="So the area = 87.0 cm²."),
    box("Check the units: the area to 1 d.p. is ", 87, "Same value, in cm².", done="Area = 87.0 cm² confirmed."),
  ],
  "misconceptions": [
    {"pattern": "used_half", "expect": 43.5, "note": "0.5*96*sin65",
     "message": "You used the ½ from the triangle area. A parallelogram is two triangles, so there is no half: area = 8 × 12 × sin 65° = 87.0 cm². Halving gives 43.5, which is just one triangle."},
  ]})

# ================================================================ GUIDED
opener = {
  "display": B.poly_svg(B.sas(10, 30, 5*math.cos(math.radians(0))*0+5), ["A","B","C"], {}, {}, None, "x")  # placeholder, replaced below
}
# build opener SVG: 30-60-90 triangle, side facing 30 = 5, right angle at C
# Vertices: A(30 deg), B(60 deg), C(90 deg). Use sss-like: place right angle.
# side opposite 30 = 5 (that's BC? opp A=30). Make legs: opposite30=5, opposite60=5*tan60?
# Simpler explicit: right angle at C. AC and BC legs, AB hypotenuse.
# angle A=30 at A, angle B=60 at B, C=90. side a=BC opposite A =5. AB(hyp)=10.
# AC = 5*sqrt(3)=8.66 opposite B=60.
import math as _m
oA=(0.0,0.0); oB=(10.0,0.0)
# C such that angle A=30: AC direction 30 deg, length AC=8.66
oC=(8.6603*_m.cos(_m.radians(30)), 8.6603*_m.sin(_m.radians(30)))
opener_svg = B.poly_svg([oA,oB,oC], ["A","B","C"],
  {(1,2): "5 cm"}, {0: ('arc', "30°"), 1: ('arc', "60°"), 2: ('right', "90°")}, None,
  "A 30, 60, 90 triangle with the side facing the 30 degree angle equal to 5 cm")
opener = {
  "display": opener_svg + B.CAP + "In any triangle the longer side always faces the bigger angle. This right-angled triangle has angles 30°, 60° and 90°, and the side facing the 30° angle is 5 cm.",
  "steps": [
    {"pre": "Which of the two angles, 30° or 60°, faces the longer side? Type the bigger angle: ", "post": "", "answer": 60, "hint": "The longer side always faces the bigger angle."},
    {"pre": "In a 30-60-90 triangle the longest side (facing 90°) is exactly double the shortest (facing 30°). If the short side is 5 cm, the longest side = 5 × 2 = ", "post": "", "answer": 10, "hint": "Double 5 cm."},
    {"say": "You just used the rule that a bigger angle faces a longer side. The <strong>sine rule</strong> makes this exact: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C}\\), so each side is proportional to the sine of the angle facing it. When you cannot pair a side with its opposite angle, the <strong>cosine rule</strong> \\(a^2 = b^2 + c^2 - 2bc\\cos A\\) and the area rule \\(\\frac12 ab\\sin C\\) take over."},
  ]}

# teach walks
teach = {}
# bronze: area walk (7,10, incl 40 -> 22.5)
teach['bronze'] = {
  "display": "Find the area of a triangle with sides 7 cm and 10 cm and an included angle of 40°. Give to 1 d.p.",
  "steps": [
    sayonly("Area of a triangle: \\(\\frac12 ab\\sin C\\), with the two sides 7 and 10 and the angle 40° between them."),
    box("Half the product of the sides: ½ × 7 × 10 = ", 35.0, "Multiply 7 and 10, then halve."),
    box("Sine of the angle: sin 40° = ", 0.6428, "sin 40, 4 d.p."),
    box("Multiply: 35 × 0.6428 = ", 22.5, "Product of the two, 1 d.p."),
    box("Check the units: the area to 1 d.p. is ", 22.5, "Same value, in cm².", done="Gone: that was the whole area move, ½ab sin C."),
  ]}
# silver: cosine rule side walk (6,9, incl 55 -> 7.4)
teach['silver'] = {
  "display": "A triangle has sides 6 cm and 9 cm with an included angle of 55°. Find the third side to 1 d.p.",
  "steps": [
    sayonly("No matching side-angle pair, so use the cosine rule: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\), with the sides 6 and 9 and the angle 55° between them."),
    box("Square and add: 6² + 9² = 36 + 81 = ", 117, "Square each, then add."),
    box("The last term: 2 × 6 × 9 × cos 55° = ", 61.9463, "2 × 6 × 9 × cos 55, 4 d.p."),
    box("So the third side² = 117 − 61.9463 = ", 55.0537, "Subtract."),
    box("Square root: √55.0537 = ", 7.4, "Square root, 1 d.p.", done="Gone: the cosine rule handles two sides and the angle between them."),
  ]}
# gold: ambiguous case walk (a9,b7,B45 -> 65.4 or 114.6)
teach['gold'] = {
  "display": "In triangle ABC, a = 9, b = 7, B = 45°. Find both possible values of angle A to 1 d.p.",
  "steps": [
    sayonly("Because a is longer than b, the sine rule can give two angles. Start from \\(\\sin A = \\frac{a\\sin B}{b} = \\frac{9\\sin 45°}{7}\\)."),
    box("Top line: 9 × sin 45° = ", 6.3640, "9 × sin 45, 4 d.p."),
    box("Divide by 7: 6.3640 ÷ 7 = ", 0.9091, "That is sin A, 4 d.p."),
    box("First value: sin⁻¹(0.9091) = ", 65.4, "Inverse sine, 1 d.p."),
    box("Second value: 180° − 65.4° = ", 114.6, "Sine gives two angles under 180°.", done="Both fit (114.6° + 45° < 180°), so A = 65.4° or 114.6°. Gone: that is the ambiguous case."),
  ]}

# tier_guides
tier_guides = {
  "bronze": {
    "title": "Bronze: one rule, used once",
    "steps": [
      "Area of a triangle from two sides and the angle between them: Area = \\(\\frac12 ab\\sin C\\).",
      "Sine rule when you have a matching side and angle pair: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\).",
      "Cosine rule for a side from two sides and the included angle: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\), then square root.",
    ],
    "example": {
      "question": "Find the area: sides 8 and 6, included angle 30°.",
      "steps": [
        {"label": "Set up", "content": "Area = ½ × 8 × 6 × sin 30°"},
        {"label": "Work out", "content": "½ × 8 × 6 = 24, and sin 30° = 0.5"},
        {"label": "Check", "content": "24 × 0.5, area in cm²"},
        {"label": "Answer", "content": "Area = 12 cm²", "isAnswer": True, "is_answer": True},
      ]}},
  "silver": {
    "title": "Silver: choose and carry the rule",
    "steps": [
      "Three sides and you want an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\), then inverse cosine.",
      "Two sides and the included angle for the third side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\).",
      "No angle given for an area: find one angle with the cosine rule first, then \\(\\frac12 ab\\sin C\\).",
    ],
    "example": {
      "question": "Find angle A: a = 7, b = 5, c = 6.",
      "steps": [
        {"label": "Set up", "content": "cos A = (5² + 6² − 7²) ÷ (2 × 5 × 6)"},
        {"label": "Work out", "content": "cos A = 12 ÷ 60 = 0.2"},
        {"label": "Check", "content": "cos⁻¹ gives an acute angle"},
        {"label": "Answer", "content": "A = 78.5°", "isAnswer": True, "is_answer": True},
      ]}},
  "gold": {
    "title": "Gold: combine and rearrange",
    "steps": [
      "Ambiguous case: after an acute angle from the sine rule, test 180 minus it and reject any that overshoot 180.",
      "Area rearranged for an angle: sin C = 2 × Area ÷ (ab). Heron's formula gives area straight from three sides.",
      "Parallelogram from two triangles: area = \\(ab\\sin\\theta\\), with no half.",
    ],
    "example": {
      "question": "Area 24, sides 8 and 12. Find the acute included angle.",
      "steps": [
        {"label": "Rearrange", "content": "sin C = 2 × 24 ÷ (8 × 12)"},
        {"label": "Work out", "content": "sin C = 48 ÷ 96 = 0.5"},
        {"label": "Check", "content": "acute, so use sin⁻¹"},
        {"label": "Answer", "content": "C = 30.0°", "isAnswer": True, "is_answer": True},
      ]}},
}

method_card = {
  "title": "Sine Rule, Cosine Rule & Area Formula",
  "steps": [
    "Label sides a, b, c opposite angles A, B, C.",
    "A side and its opposite angle known: use the sine rule.",
    "Two sides and the included angle, or three sides: use the cosine rule.",
    "Area from two sides and the angle between them: ½ab sin C.",
  ],
  "content": "<p><strong>Sine rule:</strong> \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\), for a side or angle with a matching pair.</p><p><strong>Cosine rule (side):</strong> \\(a^2 = b^2 + c^2 - 2bc\\cos A\\); <strong>(angle):</strong> \\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\).</p><p><strong>Area:</strong> \\(\\frac12 ab\\sin C\\).</p>",
  "example": "<p><strong>Find a when b = 8, A = 50°, B = 70°.</strong></p><p>\\(a = \\frac{8\\sin 50°}{\\sin 70°} = 6.5\\)</p>",
}

pd = {
  "guided": {"opener": opener, "teach": teach},
  "method_card": method_card,
  "tier_guides": tier_guides,
  "topic_links": topic_links,
  "problem_bank": {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One rule used once: the area formula ½ab sin C, or a single sine or cosine rule step.",
    "silver_description": "Choose the rule and carry a multi-step solve: cosine rule for a side or angle, the sine rule, or an area that needs an angle first.",
    "gold_description": "Combine or rearrange rules: the ambiguous sine case, Heron's formula, area rearranged for an angle, and shapes built from triangles.",
  },
  "related_videos": related_videos,
  "worked_examples": worked_examples,
}

out = "lesson_maths-ocr_geometry-L06.json"
json.dump(pd, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)
