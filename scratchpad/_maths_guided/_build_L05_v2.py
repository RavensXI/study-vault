# -*- coding: utf-8 -*-
import json, io

MIN = "−"  # minus sign
DIV = "÷"
MUL = "×"

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None:
        d["done"] = done
    if phase is not None:
        d["phase"] = phase
    return d

def say(text):
    return {"say": text}

def mc(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message, "note": note}

pd = {}

pd["method_card"] = {
    "title": "Solving Linear Equations",
    "steps": [
        "Expand any brackets, and clear fractions by multiplying both sides by the denominator.",
        "Collect the x-terms on one side and the numbers on the other.",
        "Simplify, then divide to find x.",
        "Check by substituting your answer back into the equation."
    ],
    "content": "<p>A <strong>linear equation</strong> has x to the power 1 only. Solve it with <strong>inverse operations</strong>: undo each step in reverse order, always doing the same to both sides.</p><p>If x is on both sides, move the smaller x-term across first. If there are brackets, expand them before collecting. If there is a fraction, multiply both sides by the denominator to clear it.</p>",
    "example": "<p><strong>Solve</strong> \\(2(x + 3) = x + 10\\)</p><p>Expand: \\(2x + 6 = x + 10\\). Subtract x: \\(x + 6 = 10\\). Subtract 6: \\(x = 4\\). Check: \\(2(7) = 14\\) and \\(4 + 10 = 14\\) ✔</p>"
}

pd["topic_links"] = {
    "prerequisites": [
        {"slug": "algebra/1", "title": "Simplifying Expressions"},
        {"slug": "algebra/4", "title": "Formulae & Substitution"}
    ]
}

bank = {}
bronze = []

bronze.append({
    "display": "Solve \\(2x + 3 = 11\\)",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 3 from both sides, then divide by 2.",
    "misconceptions": [
        mc("forgot_to_divide", 8, "You worked out 2x = 8 but stopped there, and 8 is 2 lots of x, not x. Divide both sides by 2 to finish: x = 4.", "8 is 2x before dividing"),
        mc("sign_error", 7, "It looks like you added the 3 instead of subtracting it. The +3 becomes " + MIN + "3 when it crosses the equals sign: 2x = 11 " + MIN + " 3 = 8, so x = 4.", "adds 3: 2x=14, x=7")
    ],
    "guided_steps": [
        say("Undo in reverse. The +3 was added last, so subtract 3 from both sides first."),
        box("11 " + MIN + " 3 = ", 8, "Take 3 off both sides."),
        say("So 2x = 8. Now undo the " + MUL + "2 by dividing both sides by 2."),
        box("8 " + DIV + " 2 = ", 4, "Half of 8.", phase="substitute"),
        say("Check by putting x = 4 back in."),
        box("2 " + MUL + " 4 + 3 = ", 11, "Work out 2 " + MUL + " 4, then add 3.", done="It gives 11, so x = 4 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(3x " + MIN + " 5 = 10\\)",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Add 5 to both sides, then divide by 3.",
    "misconceptions": [
        mc("forgot_to_divide", 15, "You reached 3x = 15, but that is 3 lots of x. Divide both sides by 3 to get x = 5.", "15 is 3x before dividing")
    ],
    "guided_steps": [
        say("Undo in reverse. The " + MIN + "5 is undone by adding 5 to both sides."),
        box("10 + 5 = ", 15, "Add 5 to both sides."),
        say("So 3x = 15. Now undo the " + MUL + "3 by dividing both sides by 3."),
        box("15 " + DIV + " 3 = ", 5, "15 shared into 3 equal parts.", phase="substitute"),
        say("Check by putting x = 5 back in."),
        box("3 " + MUL + " 5 " + MIN + " 5 = ", 10, "Work out 3 " + MUL + " 5, then subtract 5.", done="It gives 10, so x = 5 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(4x + 1 = 25\\)",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 1 from both sides, then divide by 4.",
    "misconceptions": [
        mc("forgot_to_divide", 24, "You found 4x = 24, but that is 4 lots of x. Divide both sides by 4 to get x = 6.", "24 is 4x before dividing"),
        mc("sign_error", 6.5, "It looks like you added the 1 instead of subtracting it. The +1 becomes " + MIN + "1 across the equals sign: 4x = 25 " + MIN + " 1 = 24, so x = 6.", "adds 1: 4x=26, x=6.5")
    ],
    "guided_steps": [
        say("Undo in reverse. The +1 was added last, so subtract 1 from both sides first."),
        box("25 " + MIN + " 1 = ", 24, "Take 1 off both sides."),
        say("So 4x = 24. Now divide both sides by 4."),
        box("24 " + DIV + " 4 = ", 6, "24 shared into 4 equal parts.", phase="substitute"),
        say("Check by putting x = 6 back in."),
        box("4 " + MUL + " 6 + 1 = ", 25, "Work out 4 " + MUL + " 6, then add 1.", done="It gives 25, so x = 6 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(7x " + MIN + " 2 = 19\\)",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Add 2 to both sides, then divide by 7.",
    "misconceptions": [
        mc("forgot_to_divide", 21, "You reached 7x = 21, which is 7 lots of x. Divide both sides by 7 to get x = 3.", "21 is 7x before dividing")
    ],
    "guided_steps": [
        say("Undo in reverse. The " + MIN + "2 is undone by adding 2 to both sides."),
        box("19 + 2 = ", 21, "Add 2 to both sides."),
        say("So 7x = 21. Now divide both sides by 7."),
        box("21 " + DIV + " 7 = ", 3, "21 shared into 7 equal parts.", phase="substitute"),
        say("Check by putting x = 3 back in."),
        box("7 " + MUL + " 3 " + MIN + " 2 = ", 19, "Work out 7 " + MUL + " 3, then subtract 2.", done="It gives 19, so x = 3 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(\\frac{x}{3} = 5\\)",
    "solutions": [15], "calculator": False, "input_type": "single_value",
    "hint": "x is divided by 3, so multiply both sides by 3.",
    "misconceptions": [],
    "guided_steps": [
        say("x is divided by 3. To undo dividing, multiply both sides by 3. The left side, (x " + DIV + " 3) " + MUL + " 3, just leaves x."),
        box("Right side: 5 " + MUL + " 3 = ", 15, "Three lots of 5."),
        say("So x = 15. Check it: 15 " + DIV + " 3 should give the 5 we started with."),
        box("15 " + DIV + " 3 = ", 5, "Split 15 into three equal parts.", phase="substitute"),
        say("That matches the 5 on the right. As a final tick, multiply back:"),
        box("3 " + MUL + " 5 = ", 15, "Three fives.", done="Back to 15, so x = 15 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(6x + 4 = 46\\)",
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 4 from both sides, then divide by 6.",
    "misconceptions": [
        mc("forgot_to_divide", 42, "You found 6x = 42, but that is 6 lots of x. Divide both sides by 6 to get x = 7.", "42 is 6x before dividing")
    ],
    "guided_steps": [
        say("Undo in reverse. The +4 was added last, so subtract 4 from both sides first."),
        box("46 " + MIN + " 4 = ", 42, "Take 4 off both sides."),
        say("So 6x = 42. Now divide both sides by 6."),
        box("42 " + DIV + " 6 = ", 7, "42 shared into 6 equal parts.", phase="substitute"),
        say("Check by putting x = 7 back in."),
        box("6 " + MUL + " 7 + 4 = ", 46, "Work out 6 " + MUL + " 7, then add 4.", done="It gives 46, so x = 7 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(5x " + MIN + " 8 = 2\\)",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Add 8 to both sides, then divide by 5.",
    "misconceptions": [
        mc("forgot_to_divide", 10, "You reached 5x = 10, which is 5 lots of x. Divide both sides by 5 to get x = 2.", "10 is 5x before dividing")
    ],
    "guided_steps": [
        say("Undo in reverse. The " + MIN + "8 is undone by adding 8 to both sides."),
        box("2 + 8 = ", 10, "Add 8 to both sides."),
        say("So 5x = 10. Now divide both sides by 5."),
        box("10 " + DIV + " 5 = ", 2, "10 shared into 5 equal parts.", phase="substitute"),
        say("Check by putting x = 2 back in."),
        box("5 " + MUL + " 2 " + MIN + " 8 = ", 2, "Work out 5 " + MUL + " 2, then subtract 8.", done="It gives 2, so x = 2 is right.", phase="substitute")
    ]
})

bronze.append({
    "display": "Solve \\(\\frac{x}{4} + 2 = 5\\)",
    "solutions": [12], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 2 from both sides, then multiply by 4.",
    "misconceptions": [
        mc("sign_error", 28, "It looks like you added the 2 instead of subtracting it. The +2 becomes " + MIN + "2 across the equals sign: x " + DIV + " 4 = 5 " + MIN + " 2 = 3, so x = 12.", "adds 2: x/4=7, x=28"),
        mc("forgot_to_multiply", 3, "You found x " + DIV + " 4 = 3 but stopped. Undo the divide by multiplying both sides by 4: x = 12.", "3 is the value of x/4")
    ],
    "guided_steps": [
        say("Undo the +2 first: subtract 2 from both sides."),
        box("5 " + MIN + " 2 = ", 3, "Take 2 off both sides."),
        say("So x " + DIV + " 4 = 3. Now undo the divide by 4: multiply both sides by 4."),
        box("3 " + MUL + " 4 = ", 12, "Four lots of 3.", phase="substitute"),
        say("Check by putting x = 12 back in."),
        box("12 " + DIV + " 4 + 2 = ", 5, "12 " + DIV + " 4 is 3, then add 2.", done="It gives 5, so x = 12 is right.", phase="substitute")
    ]
})

bank["bronze"] = bronze

silver = []

silver.append({
    "display": "Solve \\(5x + 2 = 3x + 10\\)",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 3x from both sides, then solve the two-step equation left.",
    "misconceptions": [
        mc("sign_error_variable", 1, "It looks like you added 3x instead of subtracting it. To clear x from the right, subtract 3x from both sides: 5x " + MIN + " 3x = 2x, giving 2x + 2 = 10 and x = 4.", "keeps +3x: 8x=8, x=1"),
        mc("sign_error_constant", 6, "It looks like you added the 2 instead of subtracting it. The +2 becomes " + MIN + "2 across the equals sign: 2x = 10 " + MIN + " 2 = 8, so x = 4.", "keeps +2: 2x=12, x=6")
    ],
    "guided_steps": [
        say("Get the x-terms together. Subtract 3x from both sides so the right loses its x."),
        box("Left x-terms: 5x " + MIN + " 3x = ", 2, "5 " + MIN + " 3.", post="x"),
        say("Now 2x + 2 = 10. Subtract 2 from both sides."),
        box("10 " + MIN + " 2 = ", 8, "Take 2 off both sides."),
        say("So 2x = 8. Now divide both sides by 2."),
        box("8 " + DIV + " 2 = ", 4, "Half of 8.", phase="substitute"),
        say("Check both sides with x = 4."),
        box("5 " + MUL + " 4 + 2 = ", 22, "20 + 2.", phase="substitute"),
        box("3 " + MUL + " 4 + 10 = ", 22, "12 + 10.", done="Both sides give 22, so x = 4 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "Solve \\(7x " + MIN + " 3 = 4x + 12\\)",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 4x from both sides, then add 3 and divide by 3.",
    "misconceptions": [
        mc("sign_error_constant", 3, "You kept the " + MIN + "3 as a subtraction. Moving it across the equals sign makes it +3: 3x = 12 + 3 = 15, so x = 5.", "keeps -3: 3x=9, x=3")
    ],
    "guided_steps": [
        say("Collect the x-terms: subtract 4x from both sides."),
        box("7x " + MIN + " 4x = ", 3, "7 " + MIN + " 4.", post="x"),
        say("Now 3x " + MIN + " 3 = 12. Undo the " + MIN + "3 by adding 3 to both sides."),
        box("12 + 3 = ", 15, "Add 3 to both sides."),
        say("So 3x = 15. Now divide both sides by 3."),
        box("15 " + DIV + " 3 = ", 5, "15 shared into 3.", phase="substitute"),
        say("Check both sides with x = 5."),
        box("7 " + MUL + " 5 " + MIN + " 3 = ", 32, "35 " + MIN + " 3.", phase="substitute"),
        box("4 " + MUL + " 5 + 12 = ", 32, "20 + 12.", done="Both sides give 32, so x = 5 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "Solve \\(2(x + 3) = 18\\)",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Expand the bracket first, then subtract 6 and divide by 2.",
    "misconceptions": [
        mc("didnt_expand", 15, "You dropped the bracket without multiplying. The 2 multiplies both terms: 2(x + 3) = 2x + 6, so 2x + 6 = 18 and x = 6.", "drops bracket: x+3=18, x=15"),
        mc("sign_error", 12, "It looks like you added the 6 instead of subtracting it after expanding: 2x = 18 " + MIN + " 6 = 12, so x = 6.", "keeps +6: 2x=24, x=12")
    ],
    "guided_steps": [
        say("Expand the bracket: multiply everything inside by 2."),
        box("2 " + MUL + " x = ", 2, "Two times x.", post="x"),
        box("2 " + MUL + " 3 = ", 6, "The 2 multiplies the +3 too."),
        say("So 2x + 6 = 18. Subtract 6 from both sides."),
        box("18 " + MIN + " 6 = ", 12, "Take 6 off both sides."),
        say("So 2x = 12. Now divide both sides by 2."),
        box("12 " + DIV + " 2 = ", 6, "Half of 12.", phase="substitute"),
        say("Check x = 6 in the original."),
        box("2 " + MUL + " (6 + 3) = ", 18, "Inside first: 6 + 3 = 9, then " + MUL + " 2.", done="It gives 18, so x = 6 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "Solve \\(4(2x + 1) = 20\\)",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Expand the bracket first, then subtract 4 and divide by 8.",
    "misconceptions": [
        mc("didnt_expand", 9.5, "You dropped the 4 without multiplying. Every term in the bracket is multiplied: 4(2x + 1) = 8x + 4, so 8x + 4 = 20 and x = 2.", "drops mult: 2x+1=20, x=9.5"),
        mc("sign_error", 3, "It looks like you added the 4 instead of subtracting it after expanding: 8x = 20 " + MIN + " 4 = 16, so x = 2.", "keeps +4: 8x=24, x=3")
    ],
    "guided_steps": [
        say("Expand the bracket: multiply everything inside by 4."),
        box("4 " + MUL + " 2x = ", 8, "Multiply the number in front.", post="x"),
        box("4 " + MUL + " 1 = ", 4, "The 4 multiplies the +1 too."),
        say("So 8x + 4 = 20. Subtract 4 from both sides."),
        box("20 " + MIN + " 4 = ", 16, "Take 4 off both sides."),
        say("So 8x = 16. Now divide both sides by 8."),
        box("16 " + DIV + " 8 = ", 2, "16 shared into 8.", phase="substitute"),
        say("Check x = 2 in the original."),
        box("4 " + MUL + " (2 " + MUL + " 2 + 1) = ", 20, "Inside first: 4 + 1 = 5, then " + MUL + " 4.", done="It gives 20, so x = 2 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "Solve \\(8x + 1 = 5x + 25\\)",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 5x from both sides, then subtract 1 and divide by 3.",
    "misconceptions": [
        mc("forgot_to_divide", 24, "You reached 3x = 24, which is 3 lots of x. Divide both sides by 3 to get x = 8.", "24 is 3x before dividing")
    ],
    "guided_steps": [
        say("Subtract 5x from both sides to collect x."),
        box("8x " + MIN + " 5x = ", 3, "8 " + MIN + " 5.", post="x"),
        say("Now 3x + 1 = 25. Subtract 1 from both sides."),
        box("25 " + MIN + " 1 = ", 24, "Take 1 off both sides."),
        say("So 3x = 24. Now divide both sides by 3."),
        box("24 " + DIV + " 3 = ", 8, "24 shared into 3.", phase="substitute"),
        say("Check both sides with x = 8."),
        box("8 " + MUL + " 8 + 1 = ", 65, "64 + 1.", phase="substitute"),
        box("5 " + MUL + " 8 + 25 = ", 65, "40 + 25.", done="Both sides give 65, so x = 8 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "Solve \\(4(x " + MIN + " 2) = 20\\)",
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "Expand the bracket first, then add 8 and divide by 4.",
    "misconceptions": [
        mc("didnt_expand", 22, "You dropped the bracket without multiplying. The 4 multiplies both terms: 4(x " + MIN + " 2) = 4x " + MIN + " 8, so 4x " + MIN + " 8 = 20 and x = 7.", "drops bracket: x-2=20, x=22"),
        mc("sign_error", 3, "You kept the " + MIN + "8 as a subtraction. It becomes +8 across the equals sign: 4x = 20 + 8 = 28, so x = 7.", "keeps -8: 4x=12, x=3")
    ],
    "guided_steps": [
        say("Expand the bracket: multiply everything inside by 4."),
        box("4 " + MUL + " x = ", 4, "Four times x.", post="x"),
        box("4 " + MUL + " (" + MIN + "2) = ", -8, "The 4 multiplies the " + MIN + "2 too; keep the minus."),
        say("So 4x " + MIN + " 8 = 20. Undo the " + MIN + "8 by adding 8 to both sides."),
        box("20 + 8 = ", 28, "Add 8 to both sides."),
        say("So 4x = 28. Now divide both sides by 4."),
        box("28 " + DIV + " 4 = ", 7, "28 shared into 4.", phase="substitute"),
        say("Check x = 7 in the original."),
        box("4 " + MUL + " (7 " + MIN + " 2) = ", 20, "Inside first: 7 " + MIN + " 2 = 5, then " + MUL + " 4.", done="It gives 20, so x = 7 is right.", phase="substitute")
    ]
})

silver.append({
    "display": "Solve \\(9x " + MIN + " 5 = 6x + 4\\)",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Subtract 6x from both sides, then add 5 and divide by 3.",
    "misconceptions": [
        mc("forgot_to_divide", 9, "You reached 3x = 9, which is 3 lots of x. Divide both sides by 3 to get x = 3.", "9 is 3x before dividing")
    ],
    "guided_steps": [
        say("Subtract 6x from both sides to collect x."),
        box("9x " + MIN + " 6x = ", 3, "9 " + MIN + " 6.", post="x"),
        say("Now 3x " + MIN + " 5 = 4. Undo the " + MIN + "5 by adding 5 to both sides."),
        box("4 + 5 = ", 9, "Add 5 to both sides."),
        say("So 3x = 9. Now divide both sides by 3."),
        box("9 " + DIV + " 3 = ", 3, "9 shared into 3.", phase="substitute"),
        say("Check both sides with x = 3."),
        box("9 " + MUL + " 3 " + MIN + " 5 = ", 22, "27 " + MIN + " 5.", phase="substitute"),
        box("6 " + MUL + " 3 + 4 = ", 22, "18 + 4.", done="Both sides give 22, so x = 3 is right.", phase="substitute")
    ]
})

bank["silver"] = silver

gold = []

gold.append({
    "display": "Solve \\(3(x + 4) = 2(x + 7)\\)",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Expand both brackets, subtract 2x, then subtract 12.",
    "misconceptions": [
        mc("sign_error", 26, "You kept the +12 as an addition. Moving it across the equals sign makes it " + MIN + "12: x = 14 " + MIN + " 12 = 2.", "keeps +12: x=26"),
        mc("forgot_multiply_constant", 10, "It looks like the 3 only multiplied the x, not the 4. Every term inside is multiplied: 3(x + 4) = 3x + 12, which gives x = 2.", "3x+4=2x+14, x=10")
    ],
    "guided_steps": [
        say("Expand both brackets first."),
        box("Left: 3 " + MUL + " x = ", 3, "Three times x.", post="x"),
        box("Left: 3 " + MUL + " 4 = ", 12, "The 3 multiplies the +4 too."),
        box("Right: 2 " + MUL + " x = ", 2, "Two times x.", post="x"),
        box("Right: 2 " + MUL + " 7 = ", 14, "The 2 multiplies the +7 too."),
        say("So 3x + 12 = 2x + 14. Subtract 2x from both sides."),
        box("3x " + MIN + " 2x = ", 1, "3 " + MIN + " 2.", post="x"),
        say("Now x + 12 = 14. Subtract 12 from both sides."),
        box("14 " + MIN + " 12 = ", 2, "Take 12 off both sides.", phase="substitute"),
        say("So x = 2. Check both sides."),
        box("3 " + MUL + " (2 + 4) = ", 18, "Inside first: 2 + 4 = 6, then " + MUL + " 3.", phase="substitute"),
        box("2 " + MUL + " (2 + 7) = ", 18, "9 " + MUL + " 2.", done="Both sides give 18, so x = 2 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "Solve \\(5(2x " + MIN + " 3) = 3(x + 2)\\)",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Expand both brackets, subtract 3x, then add 15 and divide by 7.",
    "misconceptions": [
        mc("forgot_to_divide", 21, "You reached 7x = 21, which is 7 lots of x. Divide both sides by 7 to get x = 3.", "21 is 7x before dividing")
    ],
    "guided_steps": [
        say("Expand both brackets first."),
        box("Left: 5 " + MUL + " 2x = ", 10, "Multiply the number in front.", post="x"),
        box("Left: 5 " + MUL + " (" + MIN + "3) = ", -15, "The 5 multiplies the " + MIN + "3 too; keep the minus."),
        box("Right: 3 " + MUL + " x = ", 3, "Three times x.", post="x"),
        box("Right: 3 " + MUL + " 2 = ", 6, "The 3 multiplies the +2 too."),
        say("So 10x " + MIN + " 15 = 3x + 6. Subtract 3x from both sides."),
        box("10x " + MIN + " 3x = ", 7, "10 " + MIN + " 3.", post="x"),
        say("Now 7x " + MIN + " 15 = 6. Add 15 to both sides."),
        box("6 + 15 = ", 21, "Add 15 to both sides."),
        say("So 7x = 21. Now divide both sides by 7."),
        box("21 " + DIV + " 7 = ", 3, "21 shared into 7.", phase="substitute"),
        say("Check both sides with x = 3."),
        box("5 " + MUL + " (2 " + MUL + " 3 " + MIN + " 3) = ", 15, "Inside: 6 " + MIN + " 3 = 3, then " + MUL + " 5.", phase="substitute"),
        box("3 " + MUL + " (3 + 2) = ", 15, "3 " + MUL + " 5.", done="Both sides give 15, so x = 3 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "Solve \\(4(x + 2) = 2(3x " + MIN + " 1)\\)",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Expand both brackets, subtract 4x, then add 2 and divide by 2.",
    "misconceptions": [
        mc("didnt_expand", 1.5, "You dropped both brackets without multiplying. Expand fully: 4(x + 2) = 4x + 8 and 2(3x " + MIN + " 1) = 6x " + MIN + " 2, which gives x = 5.", "x+2=3x-1, x=1.5"),
        mc("forgot_multiply_constant", 2, "It looks like the 4 only multiplied the x, not the 2. Every term is multiplied: 4(x + 2) = 4x + 8, which gives x = 5.", "4x+2=6x-2, x=2")
    ],
    "guided_steps": [
        say("Expand both brackets first."),
        box("Left: 4 " + MUL + " x = ", 4, "Four times x.", post="x"),
        box("Left: 4 " + MUL + " 2 = ", 8, "The 4 multiplies the +2 too."),
        box("Right: 2 " + MUL + " 3x = ", 6, "Multiply the number in front.", post="x"),
        box("Right: 2 " + MUL + " (" + MIN + "1) = ", -2, "The 2 multiplies the " + MIN + "1 too; keep the minus."),
        say("So 4x + 8 = 6x " + MIN + " 2. The bigger x-term is on the right, so subtract 4x from both sides."),
        box("6x " + MIN + " 4x = ", 2, "6 " + MIN + " 4.", post="x"),
        say("Now 8 = 2x " + MIN + " 2. Add 2 to both sides."),
        box("8 + 2 = ", 10, "Add 2 to both sides."),
        say("So 2x = 10. Now divide both sides by 2."),
        box("10 " + DIV + " 2 = ", 5, "Half of 10.", phase="substitute"),
        say("Check both sides with x = 5."),
        box("4 " + MUL + " (5 + 2) = ", 28, "Inside: 5 + 2 = 7, then " + MUL + " 4.", phase="substitute"),
        box("2 " + MUL + " (3 " + MUL + " 5 " + MIN + " 1) = ", 28, "Inside: 15 " + MIN + " 1 = 14, then " + MUL + " 2.", done="Both sides give 28, so x = 5 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "Solve \\(\\frac{2x + 1}{3} = 5\\)",
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "Multiply both sides by 3 first, then subtract 1 and divide by 2.",
    "misconceptions": [
        mc("didnt_clear_fraction", 2, "You forgot to clear the fraction. Multiply both sides by 3 first: 2x + 1 = 15, so 2x = 14 and x = 7.", "ignores /3: 2x+1=5, x=2"),
        mc("forgot_to_divide", 14, "You reached 2x = 14, which is 2 lots of x. Divide both sides by 2 to get x = 7.", "14 is 2x before dividing")
    ],
    "guided_steps": [
        say("Clear the fraction: multiply both sides by 3."),
        box("Right: 5 " + MUL + " 3 = ", 15, "Three lots of 5."),
        say("So 2x + 1 = 15. Subtract 1 from both sides."),
        box("15 " + MIN + " 1 = ", 14, "Take 1 off both sides."),
        say("So 2x = 14. Now divide both sides by 2."),
        box("14 " + DIV + " 2 = ", 7, "Half of 14.", phase="substitute"),
        say("Check x = 7 in the original."),
        box("2 " + MUL + " 7 + 1 = ", 15, "14 + 1.", phase="substitute"),
        box("then " + DIV + " 3 = ", 5, "15 " + DIV + " 3.", done="It gives 5, so x = 7 is right.", phase="substitute")
    ]
})

gold.append({
    "display": "Solve \\(7(x " + MIN + " 2) = 3(2x + 1)\\)",
    "solutions": [17], "calculator": False, "input_type": "single_value",
    "hint": "Expand both brackets, subtract 6x, then add 14.",
    "misconceptions": [
        mc("didnt_expand", -3, "You dropped both brackets without multiplying. Expand fully: 7(x " + MIN + " 2) = 7x " + MIN + " 14 and 3(2x + 1) = 6x + 3, which gives x = 17.", "x-2=2x+1, x=-3"),
        mc("sign_error", -11, "You kept the " + MIN + "14 as a subtraction. It becomes +14 across the equals sign: x = 3 + 14 = 17.", "keeps -14: x=-11")
    ],
    "guided_steps": [
        say("Expand both brackets first."),
        box("Left: 7 " + MUL + " x = ", 7, "Seven times x.", post="x"),
        box("Left: 7 " + MUL + " (" + MIN + "2) = ", -14, "The 7 multiplies the " + MIN + "2 too; keep the minus."),
        box("Right: 3 " + MUL + " 2x = ", 6, "Multiply the number in front.", post="x"),
        box("Right: 3 " + MUL + " 1 = ", 3, "The 3 multiplies the +1 too."),
        say("So 7x " + MIN + " 14 = 6x + 3. Subtract 6x from both sides."),
        box("7x " + MIN + " 6x = ", 1, "7 " + MIN + " 6.", post="x"),
        say("Now x " + MIN + " 14 = 3. Add 14 to both sides."),
        box("3 + 14 = ", 17, "Add 14 to both sides.", phase="substitute"),
        say("So x = 17. Check both sides."),
        box("7 " + MUL + " (17 " + MIN + " 2) = ", 105, "Inside: 17 " + MIN + " 2 = 15, then " + MUL + " 7.", phase="substitute"),
        box("3 " + MUL + " (2 " + MUL + " 17 + 1) = ", 105, "Inside: 34 + 1 = 35, then " + MUL + " 3.", done="Both sides give 105, so x = 17 is right.", phase="substitute")
    ]
})

bank["gold"] = gold

bank["bronze_description"] = "One-step and two-step equations"
bank["silver_description"] = "Unknowns on both sides, and brackets"
bank["gold_description"] = "Multi-step with brackets on both sides"

pd["problem_bank"] = bank

pd["related_videos"] = [
    {"url": "https://www.youtube.com/watch?v=30S7WxKcPwg", "title": "Solving Equations", "channel": "Corbett Maths"},
    {"url": "https://www.youtube.com/watch?v=85ZM3ZKqRhY", "title": "Solving Equations with Letters on Both Sides", "channel": "Corbett Maths"}
]

pd["worked_examples"] = [
    {"steps": [
        {"label": "Step 1: Add 3 to both sides", "content": "<p>\\(5x = 20\\)</p>"},
        {"label": "Step 2: Divide by 5", "content": "<p>\\(x = 4\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(x = 4\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ], "question": "Solve 5x − 3 = 17", "difficulty": "Bronze"},
    {"steps": [
        {"label": "Step 1: Subtract 2x from both sides", "content": "<p>\\(2x + 5 = 13\\)</p>"},
        {"label": "Step 2: Subtract 5", "content": "<p>\\(2x = 8\\)</p>"},
        {"label": "Step 3: Divide by 2", "content": "<p>\\(x = 4\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(x = 4\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ], "question": "Solve 4x + 5 = 2x + 13", "difficulty": "Silver"},
    {"steps": [
        {"label": "Step 1: Expand bracket", "content": "<p>\\(6x - 3 = 21\\)</p>"},
        {"label": "Step 2: Add 3", "content": "<p>\\(6x = 24\\)</p>"},
        {"label": "Step 3: Divide by 6", "content": "<p>\\(x = 4\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(x = 4\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ], "question": "Solve 3(2x − 1) = 21", "difficulty": "Silver"},
    {"steps": [
        {"label": "Step 1: Expand both brackets", "content": "<p>\\(5x + 10 = 3x + 24\\)</p>"},
        {"label": "Step 2: Subtract 3x", "content": "<p>\\(2x + 10 = 24\\)</p>"},
        {"label": "Step 3: Subtract 10", "content": "<p>\\(2x = 14\\)</p>"},
        {"label": "Step 4: Divide by 2", "content": "<p>\\(x = 7\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(x = 7\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ], "question": "Solve 5(x + 2) = 3(x + 8)", "difficulty": "Gold"}
]

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one and two step equations",
        "steps": [
            "<strong>Undo in reverse.</strong> Look at what has been done to x, then undo each step in the opposite order, doing the same to both sides.",
            "First undo any <strong>+</strong> or <strong>" + MIN + "</strong> number by subtracting or adding it. Then undo the <strong>" + MUL + "</strong> or <strong>" + DIV + "</strong> by dividing or multiplying.",
            "Always <strong>check</strong>: put your answer back in and make sure both sides match."
        ],
        "example": {
            "question": "Solve 3x + 4 = 19",
            "steps": [
                {"label": "Undo the +4", "content": "<p>Subtract 4 from both sides: \\(3x = 15\\)</p>"},
                {"label": "Undo the " + MUL + "3", "content": "<p>Divide both sides by 3: \\(x = 5\\)</p>"},
                {"label": "Check", "content": "<p>\\(3 × 5 + 4 = 19\\) ✔</p>"},
                {"label": "Answer", "content": "<p>\\(x = 5\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: unknowns on both sides, and brackets",
        "steps": [
            "If there are <strong>brackets</strong>, expand them first: multiply every term inside by the number outside.",
            "If x is on <strong>both sides</strong>, subtract the smaller x-term from both sides so x is left on one side only.",
            "Then it is an ordinary two-step equation: undo the number, then undo the multiply. <strong>Check</strong> your answer in both sides."
        ],
        "example": {
            "question": "Solve 4(x − 1) = 2x + 6",
            "steps": [
                {"label": "Expand", "content": "<p>\\(4x - 4 = 2x + 6\\)</p>"},
                {"label": "Collect and solve", "content": "<p>Subtract 2x: \\(2x - 4 = 6\\). Add 4: \\(2x = 10\\), so \\(x = 5\\)</p>"},
                {"label": "Check", "content": "<p>\\(4(5 - 1) = 16\\) and \\(2 × 5 + 6 = 16\\) ✔</p>"},
                {"label": "Answer", "content": "<p>\\(x = 5\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: brackets on both sides",
        "steps": [
            "<strong>Expand both brackets</strong> first. Multiply every term inside each bracket by the number in front, keeping any minus signs.",
            "Now x is on both sides. Subtract the smaller x-term from both sides, then solve the two-step equation that is left.",
            "Fractions? Multiply both sides by the denominator first to clear them. Always <strong>check</strong> both sides at the end."
        ],
        "example": {
            "question": "Solve 2(2x + 1) = 3(x + 4)",
            "steps": [
                {"label": "Expand both", "content": "<p>\\(4x + 2 = 3x + 12\\)</p>"},
                {"label": "Collect and solve", "content": "<p>Subtract 3x: \\(x + 2 = 12\\). Subtract 2: \\(x = 10\\)</p>"},
                {"label": "Check", "content": "<p>\\(2(2 × 10 + 1) = 42\\) and \\(3(10 + 4) = 42\\) ✔</p>"},
                {"label": "Answer", "content": "<p>\\(x = 10\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": "I pick a secret number.<br>I double it, then add 3.<br>Out comes 11.",
        "steps": [
            box("11 " + MIN + " 3 = ", 8, "Take the 3 back off the 11.",
                say="A number machine. No algebra needed yet, just work backwards. The last thing done was add 3, so undo that first."),
            box("8 " + DIV + " 2 = ", 4, "Halve the 8 to undo the doubling.",
                say="Good. That is an inverse operation: to undo 'add 3' you subtract 3. Before that, the number was doubled, so undo the doubling."),
            say("That secret number was 4. Writing the number as \\(x\\), 'double it and add 3 makes 11' is the equation \\(2x + 3 = 11\\). Solving it is exactly what you just did: undo the operations in reverse, subtract then divide, doing the same to both sides.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "Solve \\(4x + 5 = 17\\)",
            "label": "Together: your first one",
            "steps": [
                box("17 " + MIN + " 5 = ", 12, "Take 5 off both sides.",
                    say="Solve \\(4x + 5 = 17\\). The +5 was added last, so undo it first: subtract 5 from both sides."),
                say("So 4x = 12. Now undo the " + MUL + "4 by dividing both sides by 4."),
                box("12 " + DIV + " 4 = ", 3, "12 shared into 4 equal parts.", done="That is x. Two undo-steps: subtract, then divide."),
                say("Always check. Put x = 3 back into the original:"),
                box("4 " + MUL + " 3 = ", 12, "Four threes."),
                box("then + 5 = ", 17, "Add the 5 back on.", done="It gives 17, so x = 3 is right.")
            ]
        },
        "silver": {
            "display": "Solve \\(6x + 1 = 4x + 9\\)",
            "label": "Together: the silver move",
            "steps": [
                box("6x " + MIN + " 4x = ", 2, "6 " + MIN + " 4.", post="x",
                    say="Solve \\(6x + 1 = 4x + 9\\). The new move: get the x-terms on one side. Subtract 4x from both sides so the right loses its x."),
                say("The right side has no x now, so 2x + 1 = 9. Undo the +1 by subtracting 1 from both sides."),
                box("9 " + MIN + " 1 = ", 8, "Take 1 off both sides."),
                say("So 2x = 8. Now divide both sides by 2."),
                box("8 " + DIV + " 2 = ", 4, "Half of 8.", done="x found. Clearing x from one side first was the whole trick."),
                say("Check both sides with x = 4:"),
                box("6 " + MUL + " 4 + 1 = ", 25, "24 + 1."),
                box("4 " + MUL + " 4 + 9 = ", 25, "16 + 9.", done="Both sides give 25, so x = 4 is right.")
            ]
        },
        "gold": {
            "display": "Solve \\(2(3x + 1) = 4(x + 3)\\)",
            "label": "Together: the gold move",
            "steps": [
                box("Left: 2 " + MUL + " 3x = ", 6, "Multiply the number in front.", post="x",
                    say="Solve \\(2(3x + 1) = 4(x + 3)\\). The new move: expand BOTH brackets first, multiplying every term inside by the number outside."),
                box("Left: 2 " + MUL + " 1 = ", 2, "The 2 multiplies the +1 too."),
                box("Right: 4 " + MUL + " x = ", 4, "Four times x.", post="x"),
                box("Right: 4 " + MUL + " 3 = ", 12, "The 4 multiplies the +3 too."),
                say("So 6x + 2 = 4x + 12. Now clear x from one side: subtract 4x from both."),
                box("6x " + MIN + " 4x = ", 2, "6 " + MIN + " 4.", post="x"),
                say("That gives 2x + 2 = 12. Undo the +2 by subtracting 2 from both sides."),
                box("12 " + MIN + " 2 = ", 10, "Take 2 off both sides."),
                say("So 2x = 10. Now divide both sides by 2."),
                box("10 " + DIV + " 2 = ", 5, "Half of 10.", done="Expanding both brackets was the whole new step."),
                say("Check both sides with x = 5:"),
                box("2 " + MUL + " (3 " + MUL + " 5 + 1) = ", 32, "Inside first: 15 + 1 = 16, then " + MUL + " 2."),
                box("4 " + MUL + " (5 + 3) = ", 32, "8 " + MUL + " 4.", done="Both sides give 32, so x = 5 is right.")
            ]
        }
    }
}

io.open("lesson_algebra-L05.json", "w", encoding="utf-8").write(json.dumps(pd, indent=1, ensure_ascii=False))
print("written lesson_algebra-L05.json")
