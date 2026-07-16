# -*- coding: utf-8 -*-
import json, io, math

M = "−"  # unicode minus
SRC = "_live_geometry_L06.json"
OUT = "lesson_geometry-L06.json"

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def sayonly(say):
    return {"say": say}

# ---------------------------------------------------------------------------
# 1 + 2. Repairs + rewritten misconceptions (honest diagnosis, expect verified)
# ---------------------------------------------------------------------------
# bronze[1]: sides 8x5 (area 20) duplicated bronze[2]'s answer 20 -> change to 8x6 (area 24)
pb["bronze"][1]["display"] = "Find the area of a triangle with sides 8 cm and 6 cm and included angle \\(90°\\)."
pb["bronze"][1]["solutions"] = [24]

# silver[0]: duplicate solution [12,12] -> [12]
pb["silver"][0]["solutions"] = [12]

def setmc(tier, i, expect, message, note):
    p = pb[tier][i]
    p["misconceptions"] = [{
        "pattern": "wrong_formula", "check": "common",
        "expect": expect, "message": message, "note": note
    }]

# BRONZE
setmc("bronze",0,30,
 "You may have left out the ½. Area is HALF of a × b × sinC: ½ × 6 × 10 × 0.5 = 15, not 30. Dropping the ½ doubles your answer.",
 "6*10*sin30 = 30")
setmc("bronze",1,48,
 "That is a × b × sinC without the ½. The area is half of it: ½ × 8 × 6 × sin90° = 24.",
 "8*6*sin90 = 48")
setmc("bronze",2,5,
 "You divided the wrong way. b = a × sinB ÷ sinA = 10 × 1 ÷ 0.5 = 20. Getting 5 means sinA and sinB were swapped.",
 "10*sin30/sin90 = 5")
setmc("bronze",3,42,
 "That is ½ × 7 × 12 on its own. You still multiply by sin45° (0.7071): ½ × 7 × 12 × 0.7071 ≈ 29.7.",
 "half*7*12 = 42, sin dropped")
setmc("bronze",4,3.75,
 "The ratio is upside down. b = a × sinB ÷ sinA = 6 × 0.8 ÷ 0.5 = 9.6. Dividing sinB by sinA the other way gives 3.75.",
 "6*0.5/0.8 = 3.75")
setmc("bronze",5,40.5,
 "That is ½ × 9 × 9, before the angle is used. Multiply by sin60° (0.8660) to finish: ≈ 35.1 cm².",
 "half*81 = 40.5, sin dropped")
setmc("bronze",6,74,
 "You stopped at 25 + 49. The formula still subtracts 70cos60°: 74 " + M + " 70 × 0.5 = 74 " + M + " 35 = 39.",
 "25+49 = 74, last term dropped")
setmc("bronze",7,140,
 "That is a × b without the ½. Halve it: ½ × 10 × 14 × sin90° = 70 cm².",
 "10*14*1 = 140")

# SILVER
setmc("silver",0,5.3,
 "The ratio is inverted. b = a × sinB ÷ sinA = 8 × 0.9659 ÷ 0.6428 ≈ 12.0. Dividing the other way gives about 5.3.",
 "8*sin40/sin75 = 5.3")
setmc("silver",1,8.6,
 "You dropped the " + M + "2ab·cosC term. c² = 25 + 49 " + M + " 70cos50° = 74 " + M + " 45.0 = 29.0, so c ≈ 5.4, not √74 ≈ 8.6.",
 "sqrt(74) = 8.6")
setmc("silver",2,0,
 "cosA works out as 0, but an angle with cosine 0 is 90°, not 0°. Remember cos0° = 1; it is cos90° that equals 0. So A = 90°.",
 "cos0 vs cos90 confusion")
setmc("silver",3,30.9,
 "sinB and a are the wrong way round. sinB = b × sinA ÷ a = 15 × 0.6428 ÷ 12 = 0.804, giving B ≈ 53.5°. Using 12 × sin40° ÷ 15 gives 0.514 and the wrong 30.9°.",
 "12*sin40/15 -> 30.9")
setmc("silver",4,71.5,
 "That is ½ × 11 × 13 before the angle. Multiply by sin52° (0.7880): ≈ 56.3 cm².",
 "half*143 = 71.5, sin dropped")
setmc("silver",5,91.7,
 "Watch the sign of the top line. a² + b² " + M + " c² = 81 + 121 " + M + " 196 = +6, not " + M + "6. A positive cosine gives an acute angle: C ≈ 88.3°. A minus sign here would wrongly give 91.7°.",
 "sign slip on numerator")
setmc("silver",6,17.2,
 "The ratio is inverted. a = c × sinA ÷ sinC = 10 × 0.5736 ÷ 0.9848 ≈ 5.8. Dividing the other way gives about 17.2.",
 "10*sin80/sin35 = 17.2")

# GOLD
setmc("gold",0,19.9,
 "You may have left out the ½. Area = ½ × a × b × sinC, so sinC = 2 × 30 ÷ 88 = 0.6818 and C ≈ 43.0°. Using 30 ÷ 88 = 0.3409 (no ½) gives the wrong 19.9°.",
 "30/88 -> 19.9")
setmc("gold",1,8.2,
 "Check the sign of cos120°. It is " + M + "0.5, so " + M + "2ab·cosC = " + M + "126 × (" + M + "0.5) = +63 and c² = 130 + 63 = 193, giving c ≈ 13.9. Treating cos120° as +0.5 gives c² = 67 and the wrong 8.2 cm.",
 "sign error -> sqrt(67)=8.2")
setmc("gold",2,44.4,
 "The largest angle is opposite the longest side (7), not the shortest. Using side 7: cosC = 12 ÷ 60 = 0.2, so C ≈ 78.5°. Finding the angle opposite 5 gives 44.4°.",
 "angle opposite 5 = 44.4")
setmc("gold",3,44.4,
 "That is the acute value. The question asks for the OBTUSE angle: since sinB = 0.7, B = 180 " + M + " 44.4 = 135.6°.",
 "acute value 44.4")
setmc("gold",4,43.5,
 "That is the area of ONE triangle (½ × 8 × 12 × sin65°). A parallelogram is two of them, so double it: 8 × 12 × sin65° ≈ 87.0 cm².",
 "one triangle = 43.5")

# ---------------------------------------------------------------------------
# 3. hints per problem
# ---------------------------------------------------------------------------
hints = {
 ("bronze",0):"Area is half of the two sides multiplied together, times the sine of the angle between them.",
 ("bronze",1):"Use Area = half times a times b times sinC, with sin90 equal to 1.",
 ("bronze",2):"Rearrange the sine rule to b = a times sinB divided by sinA.",
 ("bronze",3):"Half of 7 times 12, then multiply by sin45.",
 ("bronze",4):"b = a times sinB divided by sinA.",
 ("bronze",5):"Half of 9 times 9, then multiply by sin60.",
 ("bronze",6):"Work out 25 plus 49 first, then subtract 70 times cos60.",
 ("bronze",7):"Half of 10 times 14, and sin90 is 1.",
 ("silver",0):"b = a times sinB divided by sinA.",
 ("silver",1):"c squared = a squared plus b squared minus 2ab times cosC, then square root.",
 ("silver",2):"cosA = (b squared plus c squared minus a squared) divided by 2bc, then inverse cosine.",
 ("silver",3):"sinB = b times sinA divided by a, then inverse sine.",
 ("silver",4):"Half of 11 times 13, then multiply by sin52.",
 ("silver",5):"cosC = (a squared plus b squared minus c squared) divided by 2ab, then inverse cosine.",
 ("silver",6):"a = c times sinA divided by sinC.",
 ("gold",0):"Rearrange the area formula: sinC = 2 times area divided by ab, then inverse sine.",
 ("gold",1):"c squared = a squared plus b squared minus 2ab times cosC, and cos120 is negative.",
 ("gold",2):"The largest angle is opposite the longest side. Use the cosine rule for an angle.",
 ("gold",3):"Find the acute angle first, then take it from 180 for the obtuse one.",
 ("gold",4):"A parallelogram is two triangles: work out ab times sinC (no half).",
}
for (t,i),h in hints.items():
    pb[t][i]["hint"] = h

# ---------------------------------------------------------------------------
# 3b. tier descriptions
# ---------------------------------------------------------------------------
pb["bronze_description"] = "One formula, plugged straight in: area = ½ab sinC, or a single sine or cosine rule substitution."
pb["silver_description"] = "Choose the right rule (sine or cosine) and rearrange it to reach the unknown."
pb["gold_description"] = "Work backwards from an area, handle the two-angle (ambiguous) case, or adapt the formula to a new shape."

# ---------------------------------------------------------------------------
# 7. guided_steps on every bank problem
# ---------------------------------------------------------------------------
GS = {}
# ---- BRONZE ----
GS[("bronze",0)] = [
 sayonly("Area of any triangle = \\(\\tfrac{1}{2}ab\\sin C\\). Here a = 6, b = 10 and the angle between them is C = 30°."),
 box("Multiply the two sides: 6 × 10 = ",60,"Just 6 times 10."),
 box("Halve that (the ½ in the formula): 60 ÷ 2 = ",30,"Half of 60.",phase="substitute"),
 box("Now multiply by sin30°, which is exactly 0.5: 30 × 0.5 = ",15,"Half of 30.",done="That is the area: 15 cm²."),
]
GS[("bronze",1)] = [
 sayonly("Area = \\(\\tfrac{1}{2}ab\\sin C\\), with a = 8, b = 6, C = 90°."),
 box("First the two sides: 8 × 6 = ",48,"Eight sixes."),
 box("Halve it: 48 ÷ 2 = ",24,"Half of 48.",phase="substitute"),
 box("Multiply by sin90°, which is 1: 24 × 1 = ",24,"Anything times 1 is itself.",done="Area = 24 cm². A right angle makes sinC = 1, so the formula is just ½ base × height."),
]
GS[("bronze",2)] = [
 sayonly("Sine rule: \\(\\frac{b}{\\sin B} = \\frac{a}{\\sin A}\\), so b = a × sinB ÷ sinA. Here a = 10, A = 30°, B = 90°, with sin90° = 1 and sin30° = 0.5."),
 box("First a × sinB = 10 × 1 = ",10,"Ten times one."),
 box("Now divide by sinA: 10 ÷ 0.5 = ",20,"Dividing by 0.5 doubles it.",phase="substitute",done="b = 20."),
 box("Check the ratios balance: b ÷ sinB = 20 ÷ 1 = ",20,"Twenty over one.",done="and a ÷ sinA = 10 ÷ 0.5 = 20 too, so the sine rule holds."),
]
GS[("bronze",3)] = [
 sayonly("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 7, b = 12, C = 45°, and sin45° = 0.7071 (4 d.p.)."),
 box("The two sides: 7 × 12 = ",84,"Seven twelves."),
 box("Halve it: 84 ÷ 2 = ",42,"Half of 84.",phase="substitute"),
 box("Multiply by sin45°: 42 × 0.7071 = ?  (to 1 d.p.) ",29.7,"About 42 × 0.71.",done="Area ≈ 29.7 cm²."),
]
GS[("bronze",4)] = [
 sayonly("Sine rule rearranged: b = a × sinB ÷ sinA. a = 6, sinA = 0.5, sinB = 0.8."),
 box("a × sinB = 6 × 0.8 = ",4.8,"Six times 0.8."),
 box("Divide by sinA: 4.8 ÷ 0.5 = ",9.6,"Dividing by 0.5 doubles it.",phase="substitute",done="b = 9.6."),
 box("Check: a ÷ sinA = 6 ÷ 0.5 = ",12,"Six divided by 0.5.",done="and b ÷ sinB = 9.6 ÷ 0.8 = 12 too, so it balances."),
]
GS[("bronze",5)] = [
 sayonly("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 9, b = 9, C = 60°, and sin60° = 0.8660 (4 d.p.)."),
 box("The two sides: 9 × 9 = ",81,"Nine squared."),
 box("Halve it: 81 ÷ 2 = ",40.5,"Half of 81.",phase="substitute"),
 box("Multiply by sin60°: 40.5 × 0.8660 = ?  (to 1 d.p.) ",35.1,"About 40.5 × 0.87.",done="Area ≈ 35.1 cm²."),
]
GS[("bronze",6)] = [
 sayonly("You are given \\(a^2 = 25 + 49 - 70\\cos 60°\\). Just work it out. cos60° = 0.5."),
 box("First 25 + 49 = ",74,"Add the two numbers."),
 box("The last term: 70 × cos60° = 70 × 0.5 = ",35,"Half of 70.",phase="substitute"),
 box("Subtract: 74 " + M + " 35 = ",39,"74 take away 35.",done="a² = 39. (You would square-root it for a, but only a² was asked.)"),
]
GS[("bronze",7)] = [
 sayonly("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 10, b = 14, C = 90°, and sin90° = 1."),
 box("The two sides: 10 × 14 = ",140,"Ten times fourteen."),
 box("Halve it: 140 ÷ 2 = ",70,"Half of 140.",phase="substitute"),
 box("Multiply by sin90° = 1: 70 × 1 = ",70,"Times one.",done="Area = 70 cm²."),
]
# ---- SILVER ----
GS[("silver",0)] = [
 sayonly("Sine rule: b = a × sinB ÷ sinA. a = 8, A = 40°, B = 75°. sin75° = 0.9659, sin40° = 0.6428 (4 d.p.)."),
 box("a × sinB = 8 × 0.9659 = ?  (to 2 d.p.) ",7.73,"Eight times 0.9659."),
 box("Divide by sinA: 7.73 ÷ 0.6428 = ?  (to 1 d.p.) ",12.0,"About 7.73 ÷ 0.64.",phase="substitute",done="b ≈ 12.0 cm."),
 box("Check: a ÷ sinA = 8 ÷ 0.6428 = ?  (to 1 d.p.) ",12.4,"Eight over 0.6428.",done="b ÷ sinB = 12.0 ÷ 0.9659 = 12.4 too, so the ratios match."),
]
GS[("silver",1)] = [
 sayonly("Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\). a = 5, b = 7, C = 50°. cos50° = 0.6428 (4 d.p.), and 2ab = 70."),
 box("a² + b² = 25 + 49 = ",74,"Add the two squares."),
 box("The last term, 2ab × cosC = 70 × 0.6428 = ?  (to 1 d.p.) ",45.0,"Seventy times 0.6428."),
 box("c² = 74 " + M + " 45.0 = ",29,"74 take away 45.",phase="substitute"),
 box("c = √29 = ?  (to 1 d.p.) ",5.4,"Square root of 29 is about 5.4.",done="c ≈ 5.4 cm."),
]
GS[("silver",2)] = [
 sayonly("Cosine rule for an angle: \\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\). Side a is opposite A. a = 10, b = 8, c = 6, so 2bc = 96."),
 box("Top line, b² + c² " + M + " a² = 64 + 36 " + M + " 100 = ",0,"64 + 36 is 100, then minus 100."),
 box("cosA = 0 ÷ 96 = ",0,"Zero divided by anything is 0.",phase="substitute"),
 box("A = cos⁻¹(0) = ?  degrees ",90,"The angle whose cosine is 0 is a right angle.",done="A = 90°. The 6, 8, 10 triangle is right-angled (6² + 8² = 10²)."),
]
GS[("silver",3)] = [
 sayonly("Sine rule for an angle: sinB = b × sinA ÷ a. a = 12, A = 40°, b = 15. sin40° = 0.6428 (4 d.p.)."),
 box("b × sinA = 15 × 0.6428 = ?  (to 2 d.p.) ",9.64,"Fifteen times 0.6428."),
 box("sinB = 9.64 ÷ 12 = ?  (to 4 d.p.) ",0.8033,"Divide by 12.",phase="substitute"),
 box("B = sin⁻¹(0.8033) = ?  (to 1 d.p.) ",53.5,"Inverse sine of about 0.80.",done="B ≈ 53.5°."),
]
GS[("silver",4)] = [
 sayonly("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 11, b = 13, C = 52°, and sin52° = 0.7880 (4 d.p.)."),
 box("The two sides: 11 × 13 = ",143,"Eleven thirteens."),
 box("Halve it: 143 ÷ 2 = ",71.5,"Half of 143.",phase="substitute"),
 box("Multiply by sin52°: 71.5 × 0.7880 = ?  (to 1 d.p.) ",56.3,"About 71.5 × 0.79.",done="Area ≈ 56.3 cm²."),
]
GS[("silver",5)] = [
 sayonly("Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\). Side c is opposite C. a = 9, b = 11, c = 14, so 2ab = 198."),
 box("Top line, a² + b² " + M + " c² = 81 + 121 " + M + " 196 = ",6,"81 + 121 is 202, then minus 196."),
 box("cosC = 6 ÷ 198 = ?  (to 4 d.p.) ",0.0303,"Six over 198 is small and positive.",phase="substitute"),
 box("C = cos⁻¹(0.0303) = ?  (to 1 d.p.) ",88.3,"Inverse cosine of about 0.03.",done="C ≈ 88.3°, just under a right angle."),
]
GS[("silver",6)] = [
 sayonly("Sine rule: a = c × sinA ÷ sinC. c = 10, A = 35°, C = 80°. sin35° = 0.5736, sin80° = 0.9848 (4 d.p.)."),
 box("c × sinA = 10 × 0.5736 = ",5.736,"Ten times 0.5736."),
 box("Divide by sinC: 5.736 ÷ 0.9848 = ?  (to 1 d.p.) ",5.8,"About 5.74 ÷ 0.98.",phase="substitute",done="a ≈ 5.8 cm."),
 box("Sense check: A (35°) is the smaller angle, so side a must be shorter than c = 10. Enter a once more: ",5.8,"You found a = 5.8.",done="5.8 is less than 10, so it fits."),
]
# ---- GOLD ----
GS[("gold",0)] = [
 sayonly("Work backwards from the area. Area = \\(\\tfrac{1}{2}ab\\sin C\\), so sinC = 2 × Area ÷ (a × b). Area = 30, a = 8, b = 11."),
 box("a × b = 8 × 11 = ",88,"Eight elevens."),
 box("sinC = (2 × 30) ÷ 88 = 60 ÷ 88 = ?  (to 4 d.p.) ",0.6818,"Sixty over 88.",phase="substitute"),
 box("C = sin⁻¹(0.6818) = ?  (to 1 d.p.) ",43.0,"Inverse sine of about 0.68.",done="The included angle is about 43.0°."),
]
GS[("gold",1)] = [
 sayonly("Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\). a = 7, b = 9, C = 120°. cos120° = " + M + "0.5, and 2ab = 126."),
 box("a² + b² = 49 + 81 = ",130,"Add the two squares."),
 box("The last term, 2ab × cosC = 126 × (" + M + "0.5) = ",-63,"126 times minus a half."),
 box("c² = 130 " + M + " (" + M + "63) = 130 + 63 = ",193,"Subtracting a negative adds it on.",phase="substitute"),
 box("c = √193 = ?  (to 1 d.p.) ",13.9,"Square root of 193 is about 13.9.",done="c ≈ 13.9 cm. The obtuse angle makes c longer than either side, which fits."),
]
GS[("gold",2)] = [
 sayonly("The largest angle sits opposite the longest side, which is 7. Call it C. \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\) with a = 5, b = 6, c = 7, so 2ab = 60."),
 box("Top line, a² + b² " + M + " c² = 25 + 36 " + M + " 49 = ",12,"25 + 36 is 61, then minus 49."),
 box("cosC = 12 ÷ 60 = ",0.2,"Twelve sixtieths.",phase="substitute"),
 box("C = cos⁻¹(0.2) = ?  (to 1 d.p.) ",78.5,"Inverse cosine of 0.2.",done="The largest angle is about 78.5°."),
]
GS[("gold",3)] = [
 sayonly("Sine rule for an angle: sinB = b × sinA ÷ a. a = 10, b = 14, A = 30°, and sin30° = 0.5."),
 box("b × sinA = 14 × 0.5 = ",7,"Half of 14."),
 box("sinB = 7 ÷ 10 = ",0.7,"Seven tenths.",phase="substitute"),
 box("The acute answer, sin⁻¹(0.7) = ?  (to 1 d.p.) ",44.4,"Inverse sine of 0.7."),
 box("The question wants the OBTUSE angle: 180 " + M + " 44.4 = ",135.6,"180 take away 44.4.",done="B = 135.6°. Both 44.4° and 135.6° have sine 0.7; here the obtuse one is asked for."),
]
GS[("gold",4)] = [
 sayonly("A parallelogram is two identical triangles. Each triangle is \\(\\tfrac{1}{2}\\times 8\\times 12\\times\\sin 65°\\). sin65° = 0.9063 (4 d.p.)."),
 box("One triangle first: ½ × 8 × 12 = ",48,"Half of 8 × 12."),
 box("That triangle's area: 48 × 0.9063 = ?  (to 1 d.p.) ",43.5,"About 48 × 0.91.",phase="substitute"),
 box("Two triangles make the parallelogram: 43.5 × 2 = ",87.0,"Double one triangle.",done="Area ≈ 87.0 cm², the same as a × b × sinθ."),
]
for k,v in GS.items():
    pb[k[0]][k[1]]["guided_steps"] = v

# ---------------------------------------------------------------------------
# 4. tier_guides
# ---------------------------------------------------------------------------
def exstep(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d

pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: one formula, straight in",
  "steps": [
   "Two sides and the angle between them give the area: <strong>Area = ½ab sinC</strong>. Multiply the sides, halve, then times the sine of the angle.",
   "For a missing side or angle you are handed the sine rule set up: just rearrange to b = a sinB ÷ sinA and work it through.",
   "Keep sin90° = 1 and sin30° = 0.5 in mind; they turn up a lot."
  ],
  "example": {
   "question": "Find the area of a triangle with sides 5 cm and 8 cm and included angle 30°.",
   "steps": [
    exstep("Formula","<p>Area = \\(\\tfrac{1}{2}ab\\sin C\\) = \\(\\tfrac{1}{2}\\times 5\\times 8\\times\\sin 30°\\)</p>"),
    exstep("Work","<p>\\(\\tfrac{1}{2}\\times 40 = 20\\), then \\(20\\times 0.5\\)</p>"),
    exstep("Check","<p>sin30° = 0.5, so the area is half of 20</p>"),
    exstep("Answer","<p>Area = 10 cm²</p>",True),
   ]
  }
 },
 "silver": {
  "title": "Silver: pick the rule and rearrange",
  "steps": [
   "Decide which rule fits. A side with its opposite angle known: <strong>sine rule</strong>. Two sides and the included angle, or all three sides: <strong>cosine rule</strong>.",
   "Substitute the numbers, then rearrange to the unknown. For an angle, finish with inverse sine or inverse cosine.",
   "Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\), then square root."
  ],
  "example": {
   "question": "Find side c when a = 6, b = 10, C = 60°.",
   "steps": [
    exstep("Cosine rule","<p>\\(c^2 = 36 + 100 - 2(6)(10)\\cos 60°\\)</p>"),
    exstep("Work","<p>\\(= 136 - 120\\times 0.5 = 136 - 60 = 76\\)</p>"),
    exstep("Check","<p>\\(c = \\sqrt{76}\\), which sits between 6 and 10 plus a bit</p>"),
    exstep("Answer","<p>c ≈ 8.7 cm</p>",True),
   ]
  }
 },
 "gold": {
  "title": "Gold: backwards and the two-angle case",
  "steps": [
   "Gold problems bend the formulas: find an angle from a known area, or spot the ambiguous case where a sine gives two possible angles.",
   "For an area target, rearrange to sinC = 2 × Area ÷ ab. For an ambiguous angle, the obtuse partner is 180° minus the acute one.",
   "New shapes reuse the same idea: a parallelogram is just two triangles."
  ],
  "example": {
   "question": "Find the obtuse angle B when a = 8, b = 12, A = 25°.",
   "steps": [
    exstep("Sine rule","<p>sinB = \\(\\frac{12\\sin 25°}{8}\\) = 0.6339</p>"),
    exstep("Acute","<p>\\(\\sin^{-1}(0.6339) = 39.3°\\)</p>"),
    exstep("Check","<p>Sine gives two angles; the obtuse one is 180° − 39.3°</p>"),
    exstep("Answer","<p>B = 140.7°</p>",True),
   ]
  }
 },
}

# ---------------------------------------------------------------------------
# 5 + 6. guided (opener + teach)
# ---------------------------------------------------------------------------
pd["guided"] = {
 "opener": {
  "label": "Before any formula",
  "display": "A right-angled triangular flag.<br>The two straight edges meeting at the corner are 4 m and 10 m.",
  "steps": [
   box("A triangular flag. Forget formulas: a right-angled triangle is exactly half of a rectangle. The 4 m by 10 m rectangle has area 40 m², so the triangle's area = ",20,"Half of 40.",post=" m²",
       say="A triangular flag. No formulas yet, just common sense."),
   sayonly("You just used ½ × base × height. That works because the corner is 90°. Tilt the corner and the triangle squashes: its true height shrinks to (side × sinC). So for ANY angle, <strong>Area = ½ × a × b × sinC</strong>. At 90°, sin90° = 1, and you get ½ base × height back."),
   box("Same edges 4 m and 10 m, but now they meet at 30°. Area = ½ × 4 × 10 × sin30°. Since sin30° = 0.5: 20 × 0.5 = ",10,"Half of 20.",post=" m²"),
   sayonly("That sinC factor is the whole idea. It powers the area formula, the sine rule and the cosine rule, stretching right-angle trig to every triangle. Algebra just labels the sides a, b, c opposite angles A, B, C."),
  ]
 },
 "teach": {
  "bronze": {
   "display": "Find the area of a triangle with sides 5 cm and 8 cm and included angle \\(30°\\).",
   "label": "Together: the area formula",
   "steps": [
    sayonly("Area of any triangle = \\(\\tfrac{1}{2}ab\\sin C\\). Here a = 5, b = 8 and the included angle C = 30°."),
    box("Multiply the two sides: 5 × 8 = ",40,"Five eights."),
    box("Halve it (the ½): 40 ÷ 2 = ",20,"Half of 40."),
    box("sin30° is worth knowing by heart. sin30° = ",0.5,"One half."),
    box("Multiply: 20 × 0.5 = ",10,"Half of 20.",done="Area = 10 cm². That is the whole move: sides, halve, times the sine."),
   ]
  },
  "silver": {
   "display": "Find side \\(c\\) when \\(a = 6\\), \\(b = 10\\), \\(C = 60°\\). Use the cosine rule.",
   "label": "Together: the cosine rule (a side)",
   "steps": [
    sayonly("Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\). a = 6, b = 10, C = 60°, and cos60° = 0.5."),
    box("a² + b² = 36 + 100 = ",136,"Add the two squares."),
    box("2ab = 2 × 6 × 10 = ",120,"Two times 6 times 10."),
    box("c² = 136 " + M + " 120 × 0.5 = 136 " + M + " 60 = ",76,"120 × 0.5 = 60, then subtract."),
    box("c = √76 = ?  (to 1 d.p.) ",8.7,"Square root of 76 is about 8.7.",done="c ≈ 8.7 cm. New move: the cosine rule finds the third side from two sides and the angle between them."),
   ]
  },
  "gold": {
   "display": "Find the obtuse angle \\(B\\) when \\(a = 8\\), \\(b = 12\\), \\(A = 25°\\).",
   "label": "Together: the ambiguous case",
   "steps": [
    sayonly("The ambiguous case. sinB = b × sinA ÷ a = 12 × sin25° ÷ 8. sin25° = 0.4226 (4 d.p.)."),
    box("b × sinA = 12 × 0.4226 = ?  (to 2 d.p.) ",5.07,"Twelve times 0.4226."),
    box("sinB = 5.07 ÷ 8 = ?  (to 4 d.p.) ",0.6338,"Divide by 8."),
    box("The acute answer: sin⁻¹(0.6338) = ?  (to 1 d.p.) ",39.3,"Inverse sine of about 0.63."),
    box("The obtuse partner: 180 " + M + " 39.3 = ",140.7,"180 take away 39.3.",done="B = 140.7°. Any sine has TWO angles between 0° and 180°; always ask which one the triangle needs."),
   ]
  },
 }
}

# ---------------------------------------------------------------------------
# 8. method_card (slim)
# ---------------------------------------------------------------------------
pd["method_card"] = {
 "title": "Sine Rule, Cosine Rule & Area Formula",
 "steps": [
  "Label sides a, b, c opposite angles A, B, C.",
  "Two sides and the angle between them: Area = ½ab sinC, or cosine rule for the third side.",
  "A side with its opposite angle known: sine rule, a ÷ sinA = b ÷ sinB.",
  "All three sides: cosine rule rearranged gives an angle."
 ],
 "content": "<p>These tools work in <strong>any</strong> triangle, not just right-angled ones.</p><p><strong>Area</strong> = \\(\\tfrac{1}{2}ab\\sin C\\) uses two sides and the angle between them.</p><p><strong>Sine rule</strong> pairs each side with its opposite angle: use it when you know one such pair plus one more side or angle.</p><p><strong>Cosine rule</strong> covers the rest: two sides and the included angle to find the third side, or all three sides to find an angle. A sine value gives two possible angles between 0° and 180°, so check whether an obtuse answer is wanted.</p>",
 "example": "<p><strong>Find c when a = 7, b = 9, C = 60°.</strong></p><p>\\(c^2 = 49 + 81 - 2(7)(9)\\cos 60° = 130 - 63 = 67\\), so \\(c = \\sqrt{67} \\approx 8.2\\) cm.</p>"
}

# ---------------------------------------------------------------------------
# SELF-VERIFY
# ---------------------------------------------------------------------------
r = math.radians
problems = {
 ("bronze",0):15,("bronze",1):24,("bronze",2):20,("bronze",3):29.7,("bronze",4):9.6,
 ("bronze",5):35.1,("bronze",6):39,("bronze",7):70,
 ("silver",0):12,("silver",1):5.4,("silver",2):90,("silver",3):53.5,("silver",4):56.3,
 ("silver",5):88.3,("silver",6):5.8,
 ("gold",0):43,("gold",1):13.9,("gold",2):78.5,("gold",3):135.6,("gold",4):87,
}
errs=[]
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        sols=tuple(p["solutions"])
        if sols in seen: errs.append("DUP solution %s[%d] %s"%(tier,i,sols))
        seen.add(sols)
        # final guided box should equal solution
        gs=p["guided_steps"]
        boxes=[s for s in gs if s.get("answer") is not None]
        if abs(boxes[-1]["answer"]-p["solutions"][0])>0.011:
            errs.append("%s[%d] last box %s != sol %s"%(tier,i,boxes[-1]["answer"],p["solutions"][0]))
        # boundary
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub: errs.append("%s[%d] no substitute"%(tier,i))
        else:
            live=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None)
            if live<2: errs.append("%s[%d] only %d live after sub"%(tier,i,live))
            if sub[0]<1: errs.append("%s[%d] sub at 0"%(tier,i))
        # expect != solution
        for m in p["misconceptions"]:
            e=m["expect"]
            if e is not None and abs(float(e)-p["solutions"][0])<0.011:
                errs.append("%s[%d] expect==sol"%(tier,i))
if errs:
    print("VERIFY FAIL:"); [print(" -",e) for e in errs]
else:
    print("VERIFY OK: solutions unique per tier, walks land on solutions, boundaries valid, expects distinct")

json.dump(pd, io.open(OUT,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote",OUT)
