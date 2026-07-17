# -*- coding: utf-8 -*-
import json, io

# ---------- opener balance SVG ----------
SVG = (
 '<svg viewBox="0 0 240 148" role="img" aria-label="A level balance: on the left pan two bags each marked x plus a 3 kg weight, on the right pan an 11 kg weight, and the beam is horizontal" style="max-width:260px;font-family:Inter,sans-serif">'
 '<line x1="120" y1="24" x2="120" y2="40" stroke="currentColor" stroke-width="2"/>'
 '<line x1="46" y1="40" x2="194" y2="40" stroke="currentColor" stroke-width="2"/>'
 '<polygon points="120,40 108,104 132,104" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>'
 '<line x1="92" y1="104" x2="148" y2="104" stroke="currentColor" stroke-width="2"/>'
 '<line x1="46" y1="40" x2="46" y2="66" stroke="currentColor" stroke-width="1"/>'
 '<line x1="194" y1="40" x2="194" y2="66" stroke="currentColor" stroke-width="1"/>'
 '<path d="M24 66 A22 12 0 0 0 68 66 Z" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>'
 '<path d="M172 66 A22 12 0 0 0 216 66 Z" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>'
 '<rect x="28" y="52" width="11" height="13" rx="2" fill="#34d399" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>'
 '<text x="33.5" y="62" fill="currentColor" font-size="9" text-anchor="middle">x</text>'
 '<rect x="42" y="52" width="11" height="13" rx="2" fill="#34d399" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>'
 '<text x="47.5" y="62" fill="currentColor" font-size="9" text-anchor="middle">x</text>'
 '<text x="60" y="62" fill="currentColor" font-size="9" text-anchor="middle">3kg</text>'
 '<text x="194" y="61" fill="currentColor" font-size="10" text-anchor="middle">11kg</text>'
 '</svg>'
)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s):
    return {"say": s}

# ======================= BANK =======================
# each: display, sol, misconceptions[list of (pattern,expect,message,note)], hint, guided_steps
def mc(pattern, expect, message, note):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

bronze = [
 {"display": "Solve \\(2x + 5 = 13\\)", "solutions":[4],
  "hint":"Subtract 5 from both sides, then divide by 2.",
  "misconceptions":[
    mc("forgot_divide", 8, "8 is the value of 2x, not x. Divide by 2: x = 4.", "stops at 2x=8"),
    mc("wrong_inverse", 9, "Undo +5 by subtracting, not adding: 13 − 5 = 8, then ÷ 2 = 4.", "adds 5")],
  "guided_steps":[
    box("Subtract 5 from both sides: 13 − 5 = ", 8, "13 take away 5.", say="Solve \\(2x + 5 = 13\\). Undo the +5 first."),
    box("Now 2x = 8. Divide by 2: 8 ÷ 2 = ", 4, "8 shared between 2.", phase="substitute"),
    box("Check: 2 × 4 + 5 = ", 13, "4 times 2, then add 5.", done="That matches the 13 we needed, so x = 4 is right.", phase="substitute")]},
 {"display": "Solve \\(3x - 4 = 11\\)", "solutions":[5],
  "hint":"Add 4 to both sides, then divide by 3.",
  "misconceptions":[
    mc("forgot_divide", 15, "15 is the value of 3x, not x. Divide by 3: x = 5.", "stops at 3x=15")],
  "guided_steps":[
    box("Add 4 to both sides: 11 + 4 = ", 15, "11 add 4.", say="Solve \\(3x - 4 = 11\\). Undo the −4 by adding 4."),
    box("Now 3x = 15. Divide by 3: 15 ÷ 3 = ", 5, "15 shared between 3.", phase="substitute"),
    box("Check: 3 × 5 − 4 = ", 11, "5 times 3, then take 4.", done="That matches the 11 we needed, so x = 5 is right.", phase="substitute")]},
 {"display": "Solve \\(4x + 1 = 25\\)", "solutions":[6],
  "hint":"Subtract 1 from both sides, then divide by 4.",
  "misconceptions":[
    mc("forgot_divide", 24, "24 is the value of 4x, not x. Divide by 4: x = 6.", "stops at 4x=24")],
  "guided_steps":[
    box("Subtract 1 from both sides: 25 − 1 = ", 24, "25 take away 1.", say="Solve \\(4x + 1 = 25\\). Undo the +1 first."),
    box("Now 4x = 24. Divide by 4: 24 ÷ 4 = ", 6, "24 shared between 4.", phase="substitute"),
    box("Check: 4 × 6 + 1 = ", 25, "6 times 4, then add 1.", done="That matches the 25 we needed, so x = 6 is right.", phase="substitute")]},
 {"display": "Solve \\(\\frac{x}{3} = 7\\)", "solutions":[21],
  "hint":"The x is divided by 3, so multiply both sides by 3.",
  "misconceptions":[
    mc("adds_instead", 10, "Adding 3 is not the inverse of dividing by 3. Multiply: 7 × 3 = 21.", "does 7+3")],
  "guided_steps":[
    box("The x has been split into equal parts. How many thirds make a whole? ", 3, "Three thirds make one whole.", say="Solve \\(\\frac{x}{3} = 7\\). Each third of x is worth 7."),
    box("Each third is 7, so x = 7 × 3 = ", 21, "7 times 3.", phase="substitute"),
    box("Check: 21 ÷ 3 = ", 7, "21 shared between 3.", done="That is the 7 we needed, so x = 21 is right.", phase="substitute")]},
 {"display": "Solve \\(5x = 35\\)", "solutions":[7],
  "hint":"5x means 5 times x, so divide both sides by 5.",
  "misconceptions":[
    mc("subtracts_instead", 30, "5x means 5 times x, so divide by 5: 35 ÷ 5 = 7. Do not subtract 5.", "does 35-5")],
  "guided_steps":[
    box("What number is multiplying x? ", 5, "It is the 5 written next to the x.", say="Solve \\(5x = 35\\). 5 equal lots of x make 35."),
    box("Divide both sides by 5: 35 ÷ 5 = ", 7, "35 shared between 5.", phase="substitute"),
    box("Check: 5 × 7 = ", 35, "5 times 7.", done="That is 35, so x = 7 is right.", phase="substitute")]},
 {"display": "Solve \\(x + 9 = 4\\)", "solutions":[-5],
  "hint":"Subtract 9 from both sides; the answer will be negative.",
  "misconceptions":[
    mc("sign_flip", 5, "Subtract 9 from both sides: 4 − 9 = −5. It is negative because 4 is smaller than 9.", "does 9-4")],
  "guided_steps":[
    box("9 is larger than 4, so the answer drops below zero. First, 9 − 4 = ", 5, "Ignore the sign for a moment: 9 take 4.", say="Solve \\(x + 9 = 4\\). Take 9 off both sides."),
    box("So x is that far below zero: x = 4 − 9 = ", -5, "Below zero, so x = −5.", phase="substitute"),
    box("Check: −5 + 9 = ", 4, "Start at −5 and count up 9.", done="That is the 4 we needed, so x = −5 is right.", phase="substitute")]},
 {"display": "Solve \\(7x + 2 = 23\\)", "solutions":[3],
  "hint":"Subtract 2 from both sides, then divide by 7.",
  "misconceptions":[
    mc("forgot_divide", 21, "21 is the value of 7x, not x. Divide by 7: x = 3.", "stops at 7x=21")],
  "guided_steps":[
    box("Subtract 2 from both sides: 23 − 2 = ", 21, "23 take away 2.", say="Solve \\(7x + 2 = 23\\). Undo the +2 first."),
    box("Now 7x = 21. Divide by 7: 21 ÷ 7 = ", 3, "21 shared between 7.", phase="substitute"),
    box("Check: 7 × 3 + 2 = ", 23, "3 times 7, then add 2.", done="That matches the 23 we needed, so x = 3 is right.", phase="substitute")]},
 {"display": "Solve \\(6x - 10 = 38\\)", "solutions":[8],
  "hint":"Add 10 to both sides, then divide by 6.",
  "misconceptions":[
    mc("forgot_divide", 48, "48 is the value of 6x, not x. Divide by 6: x = 8.", "stops at 6x=48")],
  "guided_steps":[
    box("Add 10 to both sides: 38 + 10 = ", 48, "38 add 10.", say="Solve \\(6x - 10 = 38\\). Undo the −10 by adding 10."),
    box("Now 6x = 48. Divide by 6: 48 ÷ 6 = ", 8, "48 shared between 6.", phase="substitute"),
    box("Check: 6 × 8 − 10 = ", 38, "8 times 6, then take 10.", done="That matches the 38 we needed, so x = 8 is right.", phase="substitute")]},
]

silver = [
 {"display": "Solve \\(5x - 3 = 2x + 12\\)", "solutions":[5],
  "hint":"Subtract 2x from both sides, then add 3, then divide.",
  "misconceptions":[
    mc("dropped_constant", 4, "Move the −3 across too: it becomes +3, so 3x = 12 + 3 = 15, giving x = 5.", "forgets to move the 3")],
  "guided_steps":[
    box("Subtract 2x from both sides. 5x − 2x = ", 3, "5 lots take away 2 lots leaves 3 lots.", post="x", say="Solve \\(5x - 3 = 2x + 12\\). Gather the x terms on the left."),
    box("Now 3x − 3 = 12. Add 3: 12 + 3 = ", 15, "12 add 3.", phase="substitute"),
    box("So 3x = 15. Divide by 3: 15 ÷ 3 = ", 5, "15 shared between 3.", phase="substitute"),
    box("Check: 5 × 5 − 3 = ", 22, "5 times 5, then take 3.", say="The right side: 2 × 5 + 12 = 22 as well.", done="Both sides give 22, so x = 5 is right.", phase="substitute")]},
 {"display": "Solve \\(4(x + 2) = 20\\)", "solutions":[3],
  "hint":"Expand the bracket to 4x plus 8, then solve.",
  "misconceptions":[
    mc("partial_expand", 4.5, "Multiply BOTH terms in the bracket by 4: 4x + 8, not 4x + 2. Then 4x = 12 and x = 3.", "expands to 4x+2")],
  "guided_steps":[
    box("Expand the bracket. Multiply both terms by 4: 4 × 2 = ", 8, "The bracket becomes 4x + 8.", say="Solve \\(4(x + 2) = 20\\). Expand the bracket first."),
    box("Now 4x + 8 = 20. Subtract 8: 20 − 8 = ", 12, "20 take away 8.", phase="substitute"),
    box("So 4x = 12. Divide by 4: 12 ÷ 4 = ", 3, "12 shared between 4.", phase="substitute"),
    box("Check: 4 × (3 + 2) = ", 20, "3 add 2, then times 4.", done="That is 20, so x = 3 is right.", phase="substitute")]},
 {"display": "Solve \\(3(2x - 1) = 21\\)", "solutions":[4],
  "hint":"Expand to 6x minus 3, then add 3 and divide by 6.",
  "misconceptions":[
    mc("dropped_constant", 3.5, "After expanding, 6x − 3 = 21. Add 3 first: 6x = 24, then x = 4.", "does 6x=21")],
  "guided_steps":[
    box("Expand the bracket. Multiply both terms by 3: 3 × 2 = ", 6, "The bracket becomes 6x − 3.", post="x", say="Solve \\(3(2x - 1) = 21\\). Expand first."),
    box("Now 6x − 3 = 21. Add 3: 21 + 3 = ", 24, "21 add 3.", phase="substitute"),
    box("So 6x = 24. Divide by 6: 24 ÷ 6 = ", 4, "24 shared between 6.", phase="substitute"),
    box("Check: 3 × (2 × 4 − 1) = ", 21, "2 times 4 is 8, take 1 is 7, times 3.", done="That is 21, so x = 4 is right.", phase="substitute")]},
 {"display": "Solve \\(7x + 4 = 3x + 28\\)", "solutions":[6],
  "hint":"Subtract 3x from both sides, then subtract 4, then divide.",
  "misconceptions":[
    mc("dropped_constant", 7, "Move the +4 across as well: 4x = 28 − 4 = 24, so x = 6.", "forgets to move the 4")],
  "guided_steps":[
    box("Subtract 3x from both sides. 7x − 3x = ", 4, "7 lots take away 3 lots leaves 4 lots.", post="x", say="Solve \\(7x + 4 = 3x + 28\\). Gather the x terms on the left."),
    box("Now 4x + 4 = 28. Subtract 4: 28 − 4 = ", 24, "28 take away 4.", phase="substitute"),
    box("So 4x = 24. Divide by 4: 24 ÷ 4 = ", 6, "24 shared between 4.", phase="substitute"),
    box("Check left: 7 × 6 + 4 = ", 46, "6 times 7, then add 4.", say="Right side: 3 × 6 + 28 = 46 too.", done="Both sides give 46, so x = 6 is right.", phase="substitute")]},
 {"display": "Solve \\(2(3x + 1) = 5x + 9\\)", "solutions":[7],
  "hint":"Expand the left to 6x plus 2, then collect the x terms.",
  "misconceptions":[
    mc("partial_expand", 8, "Multiply both terms by 2: 2(3x + 1) = 6x + 2, not 6x + 1. Then x = 7.", "expands to 6x+1")],
  "guided_steps":[
    box("Expand the left. Multiply both terms by 2: 2 × 3 = ", 6, "The left becomes 6x + 2.", post="x", say="Solve \\(2(3x + 1) = 5x + 9\\). Expand the left first."),
    box("Now 6x + 2 = 5x + 9. Subtract 5x: 6x − 5x = ", 1, "6 lots take away 5 lots leaves 1 lot.", post="x", phase="substitute"),
    box("So x + 2 = 9. Subtract 2: 9 − 2 = ", 7, "9 take away 2.", phase="substitute"),
    box("Check: 2 × (3 × 7 + 1) = ", 44, "3 times 7 is 21, add 1 is 22, times 2.", say="Right side: 5 × 7 + 9 = 44 too.", done="Both sides give 44, so x = 7 is right.", phase="substitute")]},
 {"display": "Solve \\(8 - 2x = 3x - 2\\)", "solutions":[2],
  "hint":"Add 2x to both sides so the x terms are positive, then solve.",
  "misconceptions":[
    mc("bad_collect", 10, "Both x terms combine to 3x + 2x = 5x, not x. So 10 = 5x and x = 2.", "treats 3x-2x giving x")],
  "guided_steps":[
    box("Add 2x to both sides so no x is negative. On the right, 3x + 2x = ", 5, "3 lots add 2 lots make 5 lots.", post="x", say="Solve \\(8 - 2x = 3x - 2\\). Move the x terms together on the right."),
    box("Now 8 = 5x − 2. Add 2: 8 + 2 = ", 10, "8 add 2.", phase="substitute"),
    box("So 5x = 10. Divide by 5: 10 ÷ 5 = ", 2, "10 shared between 5.", phase="substitute"),
    box("Check: 8 − 2 × 2 = ", 4, "2 times 2 is 4, take from 8.", say="Right side: 3 × 2 − 2 = 4 too.", done="Both sides give 4, so x = 2 is right.", phase="substitute")]},
 {"display": "Solve \\(3(x - 4) = 2(x + 1)\\)", "solutions":[14],
  "hint":"Expand both brackets, then collect x terms on one side.",
  "misconceptions":[
    mc("no_expand", 5, "Multiply everything in each bracket: 3(x − 4) = 3x − 12 and 2(x + 1) = 2x + 2. Then x = 14.", "does x-4=x+1 style")],
  "guided_steps":[
    box("Expand the left. 3 × 4 = ", 12, "The left becomes 3x − 12.", say="Solve \\(3(x - 4) = 2(x + 1)\\). Expand both brackets first."),
    box("Expand the right. 2 × 1 = ", 2, "The right becomes 2x + 2."),
    box("Now 3x − 12 = 2x + 2. Subtract 2x: 3x − 2x = ", 1, "3 lots take away 2 lots leaves 1 lot.", post="x", phase="substitute"),
    box("So x − 12 = 2. Add 12: 2 + 12 = ", 14, "2 add 12.", phase="substitute"),
    box("Check: 3 × (14 − 4) = ", 30, "14 take 4 is 10, times 3.", say="Right side: 2 × (14 + 1) = 30 too.", done="Both sides give 30, so x = 14 is right.", phase="substitute")]},
]

gold = [
 {"display": "Solve \\(\\frac{2x + 1}{3} = 5\\)", "solutions":[7],
  "hint":"Multiply both sides by 3 first to clear the fraction.",
  "misconceptions":[
    mc("no_clear", 2, "Multiply both sides by 3 first: 2x + 1 = 15, not 5. Then 2x = 14 and x = 7.", "solves 2x+1=5")],
  "guided_steps":[
    box("Multiply both sides by 3 to clear the fraction: 5 × 3 = ", 15, "The left becomes just 2x + 1.", say="Solve \\(\\frac{2x + 1}{3} = 5\\). Clear the fraction first."),
    box("Now 2x + 1 = 15. Subtract 1: 15 − 1 = ", 14, "15 take away 1.", phase="substitute"),
    box("So 2x = 14. Divide by 2: 14 ÷ 2 = ", 7, "14 shared between 2.", phase="substitute"),
    box("Check: (2 × 7 + 1) ÷ 3 = ", 5, "14 add 1 is 15, shared into 3.", done="That is the 5 we needed, so x = 7 is right.", phase="substitute")]},
 {"display": "Solve \\(\\frac{x + 3}{4} = \\frac{x - 1}{2}\\)", "solutions":[5],
  "hint":"Multiply both sides by 4, then expand the right side fully.",
  "misconceptions":[
    mc("partial_expand", 4, "Multiply the (x − 1) by 2 fully: 2(x − 1) = 2x − 2, not 2x − 1. Then x = 5.", "gets 2x-1")],
  "guided_steps":[
    box("Multiply both sides by 4. On the right, 4 ÷ 2 = ", 2, "So the right becomes 2 lots of (x − 1) = 2x − 2.", say="Solve \\(\\frac{x + 3}{4} = \\frac{x - 1}{2}\\). Clear the fractions by multiplying by 4."),
    box("Now x + 3 = 2x − 2. Subtract x: 2x − x = ", 1, "2 lots take away 1 lot leaves 1 lot.", post="x", phase="substitute"),
    box("So x − 2 = 3. Add 2: 3 + 2 = ", 5, "3 add 2.", phase="substitute"),
    box("Check left: (5 + 3) ÷ 4 = ", 2, "8 shared into 4.", say="Right: (5 − 1) ÷ 2 = 2 too.", done="Both sides give 2, so x = 5 is right.", phase="substitute")]},
 {"display": "Solve \\(\\frac{3x}{5} + 2 = \\frac{x}{2} + 4\\)", "solutions":[20],
  "hint":"Multiply every term by 10 to clear both fractions.",
  "misconceptions":[
    mc("no_scale_constants", 2, "Multiply EVERY term by 10, including the 2 and 4: 6x + 20 = 5x + 40, so x = 20.", "only scales fractions")],
  "guided_steps":[
    box("Multiply every term by 10. The 3x/5 becomes 6x, the x/2 becomes 5x, and 10 × 2 = ", 20, "Multiply the whole constant by 10.", say="Solve \\(\\frac{3x}{5} + 2 = \\frac{x}{2} + 4\\). Clear both fractions by multiplying every term by 10."),
    box("The 4 becomes 10 × 4 = ", 40, "Multiply that constant by 10 too."),
    box("Now 6x + 20 = 5x + 40. Subtract 5x: 6x − 5x = ", 1, "6 lots take away 5 lots leaves 1 lot.", post="x", phase="substitute"),
    box("So x + 20 = 40. Subtract 20: 40 − 20 = ", 20, "40 take away 20.", phase="substitute"),
    box("Check left: 3 × 20 ÷ 5 + 2 = ", 14, "60 shared into 5 is 12, add 2.", say="Right: 20 ÷ 2 + 4 = 14 too.", done="Both sides give 14, so x = 20 is right.", phase="substitute")]},
 {"display": "Solve \\(\\frac{5(x-2)}{3} = \\frac{2(x+1)}{2} + 1\\)", "solutions":[8],
  "hint":"Simplify the right side first, then clear the fraction by multiplying by 3.",
  "misconceptions":[
    mc("dropped_plus_one", 6.5, "Do not drop the + 1 on the right: it makes the right side x + 2, which gives x = 8.", "ignores the +1")],
  "guided_steps":[
    box("On the right, 2(x + 1) ÷ 2 is just x + 1. Adding the extra 1 gives x + 1 + 1 = x + ", 2, "1 + 1 = 2, so the right is x + 2.", say="Solve \\(\\frac{5(x-2)}{3} = \\frac{2(x+1)}{2} + 1\\). Simplify the right side first."),
    box("Now (5(x − 2))/3 = x + 2. Multiply both sides by 3. On the right, 3 × 2 = ", 6, "The right becomes 3(x + 2) = 3x + 6.", phase="substitute"),
    box("So 5(x − 2) = 3x + 6, giving 5x − 10 = 3x + 6. Subtract 3x: 5x − 3x = ", 2, "5 lots take away 3 lots leaves 2 lots.", post="x", phase="substitute"),
    box("So 2x − 10 = 6. Add 10: 6 + 10 = ", 16, "6 add 10.", phase="substitute"),
    box("So 2x = 16. Divide by 2: 16 ÷ 2 = ", 8, "16 shared between 2.", phase="substitute"),
    box("Check left: 5 × (8 − 2) ÷ 3 = ", 10, "8 take 2 is 6, times 5 is 30, shared into 3.", say="Right: 2 × (8 + 1) ÷ 2 + 1 = 9 + 1 = 10 too.", done="Both sides give 10, so x = 8 is right.", phase="substitute")]},
 {"display": "Solve \\(\\frac{4x - 3}{5} = \\frac{3x + 2}{4}\\)", "solutions":[22],
  "hint":"Cross-multiply, expanding each bracket fully, then solve.",
  "misconceptions":[
    mc("partial_cross", 5, "Cross-multiply the whole bracket: 4(4x − 3) = 16x − 12 and 5(3x + 2) = 15x + 10. Then x = 22.", "gets 16x-3=15x+2")],
  "guided_steps":[
    box("Cross-multiply. Left numerator times 4 gives 16x − 12. Right numerator times 5: 5 × 3x = ", 15, "Multiply 3x by 5.", post="x", say="Solve \\(\\frac{4x - 3}{5} = \\frac{3x + 2}{4}\\). Cross-multiply by both denominators."),
    box("And 5 × 2 = ", 10, "So the right becomes 15x + 10."),
    box("Now 16x − 12 = 15x + 10. Subtract 15x: 16x − 15x = ", 1, "16 lots take away 15 lots leaves 1 lot.", post="x", phase="substitute"),
    box("So x − 12 = 10. Add 12: 10 + 12 = ", 22, "10 add 12.", phase="substitute"),
    box("Check left: (4 × 22 − 3) ÷ 5 = ", 17, "88 take 3 is 85, shared into 5.", say="Right: (3 × 22 + 2) ÷ 4 = 68 ÷ 4 = 17 too.", done="Both sides give 17, so x = 22 is right.", phase="substitute")]},
]

for p in bronze + silver + gold:
    p["calculator"] = False
    p["input_type"] = "single_value"

# ======================= TEACH =======================
teach = {
 "bronze": {
  "label": "Together: your first one",
  "display": "Solve \\(5x - 2 = 18\\)",
  "steps": [
    box("Add 2 to both sides: 18 + 2 = ", 20, "18 add 2.", say="Undo the −2 first by adding 2 to both sides."),
    box("So 5x = 20. Divide by 5: 20 ÷ 5 = ", 4, "20 shared between 5.", say="Now undo the ×5."),
    box("Check by putting x = 4 back in: 5 × 4 = ", 20, "5 times 4.", say="Test the answer in the original equation."),
    box("Then 20 − 2 = ", 18, "20 take away 2.", done="That is the 18 we needed, so x = 4 is right. Undo the +/− first, then the ×.")]},
 "silver": {
  "label": "Together: the silver move",
  "display": "Solve \\(2(x + 3) = x + 10\\)",
  "steps": [
    box("Expand the bracket. 2 × 3 = ", 6, "The left becomes 2x + 6.", say="First expand: multiply both terms in the bracket by 2."),
    box("Now 2x + 6 = x + 10. Subtract x: 2x − x = ", 1, "2 lots take away 1 lot leaves 1 lot.", post="x", say="Gather the x terms on the left."),
    box("So x + 6 = 10. Subtract 6: 10 − 6 = ", 4, "10 take away 6.", say="Now undo the +6."),
    box("Check left: 2 × (4 + 3) = ", 14, "4 add 3 is 7, times 2.", say="Right: 4 + 10 = 14 too.", done="Both sides give 14, so x = 4. The new move: expand the bracket, then collect x terms.")]},
 "gold": {
  "label": "Together: the gold move",
  "display": "Solve \\(\\frac{x + 4}{2} = \\frac{2x - 1}{3}\\)",
  "steps": [
    box("Cross-multiply. Left numerator times 3 gives 3x + 12. Right numerator times 2: 2 × 2x = ", 4, "2 times 2x.", post="x", say="Multiply each numerator by the other denominator."),
    box("And 2 × 1 = ", 2, "So the right becomes 4x − 2."),
    box("Now 3x + 12 = 4x − 2. Subtract 3x: 4x − 3x = ", 1, "4 lots take away 3 lots leaves 1 lot.", post="x", say="This time it is simplest to gather x on the right."),
    box("So 12 = x − 2. Add 2: 12 + 2 = ", 14, "12 add 2.", say="Undo the −2."),
    box("Check left: (14 + 4) ÷ 2 = ", 9, "18 shared into 2.", say="Right: (2 × 14 − 1) ÷ 3 = 27 ÷ 3 = 9 too.", done="Both sides give 9, so x = 14. The gold move: cross-multiply to clear the fractions, then solve.")]},
}

# ======================= OPENER =======================
opener = {
 "label": "Before any algebra",
 "display": SVG,
 "steps": [
   box("Take the 3 kg weight off the left. To keep the balance level, take 3 kg off the right too: 11 − 3 = ", 8, "11 take away 3.", post=" kg", say="A balance stays level if you do the same to BOTH sides."),
   box("Now 2 equal bags balance 8 kg. One bag is 8 ÷ 2 = ", 4, "8 shared between 2 bags.", post=" kg", say="The two bags are identical, so split the 8 kg equally."),
   sayonly("You just solved an equation. Calling one bag \\(x\\), the left pan is \\(2x + 3\\) and it balances \\(11\\), so \\(2x + 3 = 11\\). Taking 3 off both sides gave \\(2x = 8\\), and halving gave \\(x = 4\\). Doing the SAME thing to both sides, then undoing each operation, is exactly how you <strong>solve a linear equation</strong>.")]
}

# ======================= TIER GUIDES =======================
def ex_step(label, content, is_ans=False):
    d = {"label": label, "content": content}
    if is_ans:
        d["isAnswer"] = True; d["is_answer"] = True
    return d

tier_guides = {
 "bronze": {
  "title": "Bronze: one and two step equations",
  "steps": [
    "Your goal is to get x on its own. Do the SAME thing to both sides each time.",
    "Undo in reverse order: deal with any + or − first, then the × or ÷. For \\(4x + 3 = 19\\), subtract 3 to get \\(4x = 16\\), then divide by 4 to get \\(x = 4\\).",
    "Always check by putting your answer back into the original equation."],
  "example": {
    "question": "Solve 3x − 5 = 16",
    "steps": [
      ex_step("Undo the −5", "<p>Add 5 to both sides: \\(3x = 21\\).</p>"),
      ex_step("Undo the ×3", "<p>Divide both sides by 3: \\(x = 7\\).</p>"),
      ex_step("Check", "<p>\\(3 \\times 7 - 5 = 16\\) ✓</p>"),
      ex_step("Answer", "<p>\\(x = 7\\)</p>", True)]}},
 "silver": {
  "title": "Silver: brackets and x on both sides",
  "steps": [
    "If there is a bracket, expand it first: \\(3(x + 2) = 3x + 6\\).",
    "If x appears on both sides, subtract the smaller x term so x stays positive, then collect the numbers on the other side.",
    "Finish by dividing, then check in the original equation."],
  "example": {
    "question": "Solve 5x − 4 = 2x + 11",
    "steps": [
      ex_step("Collect x", "<p>Subtract 2x: \\(3x - 4 = 11\\).</p>"),
      ex_step("Collect numbers", "<p>Add 4: \\(3x = 15\\), then divide by 3: \\(x = 5\\).</p>"),
      ex_step("Check", "<p>\\(5 \\times 5 - 4 = 21\\) and \\(2 \\times 5 + 11 = 21\\) ✓</p>"),
      ex_step("Answer", "<p>\\(x = 5\\)</p>", True)]}},
 "gold": {
  "title": "Gold: equations with fractions",
  "steps": [
    "Clear fractions first: multiply EVERY term by the denominator, or by the lowest common multiple of the denominators.",
    "Multiplying by 10 turns \\(\\frac{3x}{5} + 2\\) into \\(6x + 20\\). Expand any brackets that appear.",
    "Then collect x on one side, numbers on the other, divide, and check."],
  "example": {
    "question": "Solve (3x − 2)/5 = 2",
    "steps": [
      ex_step("Clear the fraction", "<p>Multiply both sides by 5: \\(3x - 2 = 10\\).</p>"),
      ex_step("Solve", "<p>Add 2: \\(3x = 12\\), then divide by 3: \\(x = 4\\).</p>"),
      ex_step("Check", "<p>\\((3 \\times 4 - 2) \\div 5 = 10 \\div 5 = 2\\) ✓</p>"),
      ex_step("Answer", "<p>\\(x = 4\\)</p>", True)]}},
}

# ======================= ASSEMBLE (preserve untouched) =======================
live = json.load(io.open("_L05_FRESH.json", encoding="utf-8"))
pd = {}
pd["method_card"] = live["method_card"]           # preserve byte-for-byte
pd["topic_links"] = live["topic_links"]           # preserve
pd["related_videos"] = live["related_videos"]     # preserve
pd["worked_examples"] = live["worked_examples"]   # preserve
pd["problem_bank"] = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "One and two step equations: undo the add or subtract, then the multiply or divide.",
 "silver_description": "Expand a bracket or gather x from both sides, then solve and check.",
 "gold_description": "Clear fractions by multiplying out, then expand, collect and solve.",
}
pd["guided"] = {"opener": opener, "teach": teach}
pd["tier_guides"] = tier_guides

json.dump(pd, io.open("lesson_maths-eduqas_algebra-L05.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_maths-eduqas_algebra-L05.json")
print("bronze",len(bronze),"silver",len(silver),"gold",len(gold))
