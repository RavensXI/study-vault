# -*- coding: utf-8 -*-
import json

SRC = "_live_geometry-L06.json"
OUT = "lesson_maths-aqa_geometry-L06.json"

pd = json.load(open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

def set_say(tier, idx, new):
    old = pb[tier][idx]["guided_steps"][0]["say"]
    assert old != new, f"{tier}[{idx}] say unchanged"
    pb[tier][idx]["guided_steps"][0]["say"] = new
    print(f"{tier}[{idx}] say fixed")

# --- Defect 1: bronze[4] false sine rule + mislabelled givens (display a=7,A=50,B=80) ---
set_say("bronze", 4,
    "Sine rule: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\). "
    "You know the pair (\\(a=7\\), \\(A=50°\\)) and angle \\(B=80°\\), "
    "so \\(b = \\frac{a\\sin B}{\\sin A}\\).")

# --- Defect 2: silver[4] same garbled sine rule (display a=5,A=30,B=105) ---
set_say("silver", 4,
    "Sine rule: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\). "
    "You know the pair (\\(a=5\\), \\(A=30°\\)) and angle \\(B=105°\\), "
    "so \\(b = \\frac{a\\sin B}{\\sin A}\\).")

# --- Defect 3: bronze[7] cosine rule a^2 on both sides (display b=10,c=7,A=50) ---
set_say("bronze", 7,
    "Cosine rule for a side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\). "
    "Two sides 10 and 7 with the angle 50° between them.")

# --- Defect 4: silver[5] same cosine garble (display b=15,c=20,A=110) ---
set_say("silver", 5,
    "Cosine rule for a side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\). "
    "Two sides 15 and 20 with the angle 110° between them.")

# --- Defect 5: silver[1] cos C formula + wrong opposite label (display a=12,b=9,c=7; C opposite c=7) ---
set_say("silver", 1,
    "Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\), "
    "where \\(c=7\\) is opposite the angle you want.")

# --- Defect 6: bronze[1] mis-posed ambiguous SSA. Swap a<->b so the side opposite
#     the GIVEN angle is the larger one (a=12 >= b=9): B is then acute and unique. ---
b1 = pb["bronze"][1]

d = b1["display"]
def rep(s, old, new):
    assert s.count(old) == 1, (old, s.count(old))
    return s.replace(old, new)

d = rep(d,
    'aria-label="Triangle ABC with side a 9, side b 12 and angle A 35 degrees, angle B unknown"',
    'aria-label="Triangle ABC with side a 12, side b 9 and angle A 35 degrees, angle B unknown"')
d = rep(d,
    '<text x="161.9" y="80.3" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">9</text>',
    '<text x="161.9" y="80.3" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">12</text>')
d = rep(d,
    '<text x="66.1" y="79.7" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">12</text>',
    '<text x="66.1" y="79.7" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">9</text>')
d = rep(d, r'\(a = 9\), \(b = 12\)', r'\(a = 12\), \(b = 9\)')
b1["display"] = d

b1["solutions"] = [25.5]
b1["hint"] = "sin B = b sin A ÷ a, then use inverse sine."
b1["guided_steps"] = [
    {"say": "Sine rule for an angle: \\(\\frac{\\sin B}{b} = \\frac{\\sin A}{a}\\), "
            "so \\(\\sin B = \\frac{b\\sin A}{a}\\). Here \\(a=12\\), \\(b=9\\), \\(A=35°\\). "
            "Since \\(a>b\\), angle B is smaller than A, so it is acute."},
    {"pre": "Top line: 9 × sin 35° = ", "hint": "9 × sin 35, 4 d.p.", "post": "", "answer": 5.1622},
    {"pre": "Divide by 12: 5.1622 ÷ 12 = ", "hint": "That is sin B, 4 d.p.", "post": "",
     "phase": "substitute", "answer": 0.4302},
    {"pre": "Inverse sine: sin⁻¹(0.4302) = ", "done": "So B = 25.5°.",
     "hint": "Use sin⁻¹ (shift sin), 1 d.p.", "post": "", "answer": 25.5},
    {"pre": "Check the third angle: 180° − 35° − 25.5° = ",
     "done": "Angle C = 119.5°, and all three angles are positive, so B = 25.5° is the only triangle.",
     "hint": "180 minus the two known angles.", "post": "", "answer": 119.5},
]
b1["misconceptions"] = [
    {"note": "asin(12*sin35/9)", "expect": 49.9,
     "message": "You put the sides the wrong way up. sin B = b sin A ÷ a = 9 sin 35 ÷ 12. "
                "Using 12 sin 35 ÷ 9 gives sin B = 0.7648 and B = 49.9°.",
     "pattern": "swapped_sides"}]
print("bronze[1] rewritten -> solutions", b1["solutions"])

# ---- fresh-solve verification of every touched box/answer ----
import math
def approx(a, b, t=0.06):
    return abs(a - b) < t

# bronze[1]
sinB = 9 * math.sin(math.radians(35)) / 12
assert approx(round(9*math.sin(math.radians(35)),4), 5.1622)
assert approx(round(sinB,4), 0.4302)
assert approx(round(math.degrees(math.asin(sinB)),1), 25.5)
assert approx(180-35-25.5, 119.5)
assert approx(round(math.degrees(math.asin(12*math.sin(math.radians(35))/9)),1), 49.9)
# bronze[4]: b = 7 sin80/sin50
assert approx(7*math.sin(math.radians(80))/math.sin(math.radians(50)), 9.0)
# silver[4]: b = 5 sin105/sin30
assert approx(5*math.sin(math.radians(105))/math.sin(math.radians(30)), 9.7)
# bronze[7]: a^2 = 10^2+7^2-2*10*7*cos50
assert approx(math.sqrt(100+49-140*math.cos(math.radians(50))), 7.7)
# silver[5]: a = sqrt(15^2+20^2-2*15*20*cos110)
assert approx(math.sqrt(225+400-600*math.cos(math.radians(110))), 28.8)
# silver[1]: cosC=(12^2+9^2-7^2)/(2*12*9)
assert approx(math.degrees(math.acos((144+81-49)/(2*12*9))), 35.4)
print("fresh-solve verification: all touched answers land on stored solutions")

json.dump(pd, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", OUT)
