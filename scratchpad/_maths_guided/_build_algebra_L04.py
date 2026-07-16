# -*- coding: utf-8 -*-
"""Build guided-format practice_data for algebra-L04 (Formulae & Substitution)."""
import json, io

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

# ---------------- BANK PROBLEMS ----------------

bronze = [
    {  # B0
        "display": "Find the value of \\(2x + 5\\) when \\(x = 3\\)",
        "solutions": [11],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply the 2 by 3 first, then add the 5.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 16,
             "message": "Multiplication comes before addition. Do 2 × 3 = 6 first, then add 5 to get 11. Adding first, 2 × (3 + 5) = 16, breaks BIDMAS.",
             "note": "add-before-multiply: 2*(3+5)=16"}
        ],
        "guided_steps": [
            say("Substitute x = 3, so the expression is 2 × 3 + 5. BIDMAS says do the multiply before the add."),
            box("2 × 3 = ", 6, "Two lots of 3."),
            box("now add the 5: 6 + 5 = ", 11, "Add on the 5 you set aside.", phase="substitute"),
            box("Check by reading the original back: two 3s make 6, plus 5 gives ", 11,
                "Same total, counted the other way.", done="11 it is. Multiply first, then add.", phase="substitute"),
        ],
    },
    {  # B1
        "display": "Find the value of \\(4x - 1\\) when \\(x = 6\\)",
        "solutions": [23],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply 4 by 6 first, then take away 1.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 20,
             "message": "Multiply before you subtract. Do 4 × 6 = 24 first, then take 1 to get 23. Subtracting first, 4 × (6 − 1) = 20, breaks BIDMAS.",
             "note": "sub-before-multiply: 4*(6-1)=20"}
        ],
        "guided_steps": [
            say("Substitute x = 6, so 4x means 4 × 6. BIDMAS: multiply before you take away the 1."),
            box("4 × 6 = ", 24, "Four lots of 6."),
            box("now subtract 1: 24 − 1 = ", 23, "Take the 1 off.", phase="substitute"),
            box("Check: four 6s make 24, less 1 is ", 23,
                "Same total again.", done="23. Multiply, then subtract.", phase="substitute"),
        ],
    },
    {  # B2
        "display": "Find the value of \\(3a + 2b\\) when \\(a = 4\\) and \\(b = 5\\)",
        "solutions": [22],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Work out 3 times 4 and 2 times 5, then add the two results.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 14,
             "message": "Each term is a multiplication: 3 × 4 = 12 and 2 × 5 = 10, giving 22. Adding coefficient to letter, (3 + 4) + (2 + 5) = 14, is not how substitution works.",
             "note": "additive slip: (3+4)+(2+5)=14"}
        ],
        "guided_steps": [
            say("Substitute a = 4 and b = 5, giving 3 × 4 + 2 × 5. Do both multiplications first, then add."),
            box("3 × 4 = ", 12, "Three lots of 4."),
            box("2 × 5 = ", 10, "Two lots of 5.", phase="substitute"),
            box("add the two parts: 12 + 10 = ", 22,
                "Put the two products together.", done="22. Multiply each term, then total them.", phase="substitute"),
        ],
    },
    {  # B3
        "display": "Find the value of \\(5x - 3\\) when \\(x = -2\\)",
        "solutions": [-13],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply 5 by negative 2 first, then subtract 3.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": -25,
             "message": "Multiply first: 5 × (−2) = −10, then subtract 3 to get −13. Subtracting first, 5 × (−2 − 3) = 5 × (−5) = −25, breaks BIDMAS.",
             "note": "sub-before-multiply: 5*(-2-3)=-25"},
            {"pattern": "sign_error", "expect": 7,
             "message": "A positive times a negative is negative: 5 × (−2) = −10, not 10. Dropping the sign gives 10 − 3 = 7, which is wrong.",
             "note": "sign dropped on product: 10-3=7"}
        ],
        "guided_steps": [
            say("Substitute x = −2, in brackets to keep the sign safe: 5 × (−2) − 3. BIDMAS: multiply first."),
            box("5 × (−2) = ", -10, "A positive times a negative is negative."),
            box("now subtract 3: −10 − 3 = ", -13, "Going more negative: −10 take away 3.", phase="substitute"),
            box("Read the original back: five lots of −2 is −10, less 3 is ", -13,
                "Same total.", done="−13. The sign on the product carried through.", phase="substitute"),
        ],
    },
    {  # B4 (replaced duplicate B4/B7: two-variable positive result, per issue 4)
        "display": "Find the value of \\(4a - b\\) when \\(a = 5\\) and \\(b = 3\\)",
        "solutions": [17],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply 4 by 5 first, then subtract 3.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 8,
             "message": "Only the 4a is a product: 4 × 5 = 20, then subtract b to get 17. Treating it as 4(a − b) = 4 × 2 = 8 groups the wrong terms.",
             "note": "wrong grouping: 4*(5-3)=8"}
        ],
        "guided_steps": [
            say("Substitute a = 5 and b = 3, giving 4 × 5 − 3. The multiply comes before the subtraction."),
            box("4 × 5 = ", 20, "Four lots of 5."),
            box("subtract b: 20 − 3 = ", 17, "Take the 3 off.", phase="substitute"),
            box("Check: four 5s make 20, less 3 is ", 17,
                "Same total.", done="17. Multiply the 4a first, then subtract b.", phase="substitute"),
        ],
    },
    {  # B5
        "display": "Find the value of \\(\\frac{x}{2} + 3\\) when \\(x = 10\\)",
        "solutions": [8],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Divide 10 by 2 first, then add 3.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 6.5,
             "message": "Divide first: 10 ÷ 2 = 5, then add 3 to get 8. Adding before dividing, (10 + 3) ÷ 2 = 6.5, breaks BIDMAS.",
             "note": "add-before-divide: (10+3)/2=6.5"}
        ],
        "guided_steps": [
            say("Substitute x = 10, giving (10 ÷ 2) + 3. The division happens before the +3."),
            box("10 ÷ 2 = ", 5, "Half of 10."),
            box("now add 3: 5 + 3 = ", 8, "Add the 3.", phase="substitute"),
            box("Read it back: half of 10 is 5, plus 3 is ", 8,
                "Same total.", done="8. Divide first, then add.", phase="substitute"),
        ],
    },
    {  # B6
        "display": "Find the value of \\(6x + y\\) when \\(x = 3\\) and \\(y = -4\\)",
        "solutions": [14],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply 6 by 3 first, then add negative 4, which means subtract 4.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": -6,
             "message": "Only 6x is a product: 6 × 3 = 18, then add y to get 14. Treating it as 6(x + y) = 6 × (−1) = −6 groups the wrong terms.",
             "note": "wrong grouping: 6*(3+(-4))=-6"},
            {"pattern": "sign_error", "expect": 22,
             "message": "y is −4, so you add a negative, which subtracts: 18 + (−4) = 14. Ignoring the minus and doing 18 + 4 = 22 is the slip.",
             "note": "sign dropped: 18+4=22"}
        ],
        "guided_steps": [
            say("Substitute x = 3 and y = −4, giving 6 × 3 + (−4). Multiply the 6 × 3 first."),
            box("6 × 3 = ", 18, "Six lots of 3."),
            box("add y, which is −4: 18 + (−4) = ", 14, "Adding −4 is the same as taking 4 away.", phase="substitute"),
            box("Check: 18 with 4 taken off is ", 14,
                "Same total.", done="14. Adding a negative means subtracting.", phase="substitute"),
        ],
    },
    {  # B7
        "display": "Find the value of \\(10 - 3x\\) when \\(x = 5\\)",
        "solutions": [-5],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply 3 by 5 first, then subtract that from 10.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 35,
             "message": "Multiply first: 3 × 5 = 15, then 10 − 15 = −5. Subtracting first, (10 − 3) × 5 = 35, breaks BIDMAS.",
             "note": "sub-before-multiply: (10-3)*5=35"}
        ],
        "guided_steps": [
            say("Substitute x = 5, giving 10 − 3 × 5. The 3 × 5 multiply comes before the subtraction."),
            box("3 × 5 = ", 15, "Three lots of 5."),
            box("now do 10 − 15 = ", -5, "Taking 15 from 10 drops below zero.", phase="substitute"),
            box("Read the original back: 10 take away three 5s (15) is ", -5,
                "Same total.", done="−5. Multiply before subtracting.", phase="substitute"),
        ],
    },
]

silver = [
    {  # S0 (changed x^2+3 -> x^2+5, answer 21 not 19, per issue 5)
        "display": "Find the value of \\(x^2 + 5\\) when \\(x = 4\\)",
        "solutions": [21],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Square the 4 first, then add 5.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 81,
             "message": "Square first: 4² = 16, then add 5 to get 21. Adding before squaring, (4 + 5)² = 81, breaks BIDMAS.",
             "note": "add-before-square: (4+5)^2=81"}
        ],
        "guided_steps": [
            say("Substitute x = 4, giving 4² + 5. BIDMAS: the power comes first."),
            box("4² = 4 × 4 = ", 16, "Four times four."),
            box("now add 5: 16 + 5 = ", 21, "Add on the 5.", phase="substitute"),
            box("Read it back: 4 squared is 16, plus 5 is ", 21,
                "Same total.", done="21. Square first, then add.", phase="substitute"),
        ],
    },
    {  # S1
        "display": "Find the value of \\(x^2 - 5x\\) when \\(x = 6\\)",
        "solutions": [6],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Square the 6, work out 5 times 6, then subtract.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 186,
             "message": "Both terms use x = 6: 6² = 36 and 5 × 6 = 30, giving 36 − 30 = 6. Doing (x² − 5) × x = (36 − 5) × 6 = 186 groups it wrongly.",
             "note": "wrong grouping: (36-5)*6=186"}
        ],
        "guided_steps": [
            say("Substitute x = 6, giving 6² − 5 × 6. Power first, then the multiply, then subtract."),
            box("6² = ", 36, "Six times six."),
            box("5 × 6 = ", 30, "Five lots of 6.", phase="substitute"),
            box("now subtract: 36 − 30 = ", 6,
                "Take the 30 from the 36.", done="6. Square, then subtract five lots of x.", phase="substitute"),
        ],
    },
    {  # S2
        "display": "Find the value of \\(2x^2 + 1\\) when \\(x = -3\\)",
        "solutions": [19],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Square negative 3 in brackets to get 9, multiply by 2, then add 1.",
        "misconceptions": [
            {"pattern": "negative_squared", "expect": -17,
             "message": "Squaring a negative gives a positive: (−3)² = 9, not −9. Using −9 gives 2 × (−9) + 1 = −17, which is wrong.",
             "note": "(-3)^2 taken as -9: 2*(-9)+1=-17"},
            {"pattern": "order_of_ops", "expect": 37,
             "message": "The power acts on x alone before the 2 multiplies: 2 × (−3)² = 2 × 9 = 18, then +1 = 19. Doing (2 × −3)² + 1 = 37 squares too much.",
             "note": "mult-before-square: (2*-3)^2+1=37"}
        ],
        "guided_steps": [
            say("Substitute x = −3, in brackets: 2 × (−3)² + 1. BIDMAS: the power first, before the 2 multiplies."),
            box("(−3)² = (−3) × (−3) = ", 9, "Negative times negative is positive."),
            box("2 × 9 = ", 18, "Two lots of 9.", phase="substitute"),
            box("now add 1: 18 + 1 = ", 19,
                "Add the last 1.", done="19. Square the bracket first, multiply, then add.", phase="substitute"),
        ],
    },
    {  # S3 (changed u=0 -> u=5,a=4,t=3, answer 17, per issue 3)
        "display": "Given \\(v = u + at\\), find \\(v\\) when \\(u = 5\\), \\(a = 4\\), \\(t = 3\\)",
        "solutions": [17],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Multiply a by t first, then add u.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 27,
             "message": "The at term is a multiplication done first: 4 × 3 = 12, then add u to get 5 + 12 = 17. Adding u + a before multiplying, (5 + 4) × 3 = 27, breaks BIDMAS.",
             "note": "add-before-multiply: (5+4)*3=27"}
        ],
        "guided_steps": [
            say("Substitute u = 5, a = 4, t = 3 into v = u + at, giving v = 5 + 4 × 3. The at multiply first."),
            box("4 × 3 = ", 12, "a times t."),
            box("now add u: 5 + 12 = ", 17, "Add the 5.", phase="substitute"),
            box("Read it back: u (5) plus at (12) is ", 17,
                "Same total.", done="17. Work out at, then add u.", phase="substitute"),
        ],
    },
    {  # S4
        "display": "Find the value of \\(3x^2 - 2x + 4\\) when \\(x = 2\\)",
        "solutions": [12],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Square the 2 first, then do each multiplication, then combine.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 36,
             "message": "The power acts on x alone: 3 × 2² = 3 × 4 = 12. Squaring the whole 3x, (3 × 2)² = 36, gives 36 − 4 + 4 = 36, which is wrong.",
             "note": "square whole 3x: (3*2)^2-4+4=36"}
        ],
        "guided_steps": [
            say("Substitute x = 2, giving 3 × 2² − 2 × 2 + 4. BIDMAS: the power 2² first, then the multiplies."),
            box("2² = ", 4, "Two times two."),
            box("3 × 4 = ", 12, "Three lots of the squared value.", phase="substitute"),
            box("2 × 2 = ", 4, "The middle term, 2x.", phase="substitute"),
            box("put it together: 12 − 4 + 4 = ", 12,
                "12 take 4 is 8, add 4 back.", done="12. Square first, then each multiply, then combine.", phase="substitute"),
        ],
    },
    {  # S5
        "display": "Find the value of \\(\\frac{x^2 + 1}{5}\\) when \\(x = 3\\)",
        "solutions": [2],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Work out the whole top, 3 squared plus 1, then divide by 5.",
        "misconceptions": [
            {"pattern": "order_of_ops", "expect": 9.2,
             "message": "The whole top is divided by 5: (9 + 1) ÷ 5 = 2. Dividing only the 1, giving 9 + (1 ÷ 5) = 9.2, ignores the fraction bar.",
             "note": "division on 1 only: 9+0.2=9.2"}
        ],
        "guided_steps": [
            say("Substitute x = 3, giving (3² + 1) ÷ 5. The whole top is worked out first, then divided by 5."),
            box("3² = ", 9, "Three times three."),
            box("the top becomes 9 + 1 = ", 10, "Finish the numerator before dividing.", phase="substitute"),
            box("now divide by 5: 10 ÷ 5 = ", 2,
                "How many 5s in 10.", done="2. Whole top first, then divide.", phase="substitute"),
        ],
    },
    {  # S6
        "display": "Find the value of \\(x^2 + 2x - 8\\) when \\(x = -4\\)",
        "solutions": [0],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Square negative 4 to get 16, work out 2 times negative 4, then subtract 8.",
        "misconceptions": [
            {"pattern": "negative_squared", "expect": -32,
             "message": "Squaring a negative gives a positive: (−4)² = 16, not −16. Using −16 gives −16 − 8 − 8 = −32, which is wrong.",
             "note": "(-4)^2 taken as -16: -16-8-8=-32"}
        ],
        "guided_steps": [
            say("Substitute x = −4, in brackets: (−4)² + 2 × (−4) − 8. BIDMAS: the power first."),
            box("(−4)² = ", 16, "Negative times negative is positive."),
            box("2 × (−4) = ", -8, "Two lots of −4.", phase="substitute"),
            box("combine: 16 + (−8) − 8 = ", 0,
                "16 take 8 is 8, take another 8 is 0.", done="0. Square first, then the 2x term, then subtract 8.", phase="substitute"),
        ],
    },
]

gold = [
    {  # G0
        "display": "Make \\(x\\) the subject of \\(y = 5x + 2\\)",
        "options": ["\\(x = \\frac{y - 2}{5}\\)", "\\(x = \\frac{y + 2}{5}\\)", "\\(x = 5y - 2\\)", "\\(x = \\frac{y}{5} - 2\\)"],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Subtract 2 from both sides, then divide by 5.",
        "misconceptions": [
            {"pattern": "wrong_rearrange", "expect": 1,
             "message": "To undo +2 you subtract, not add. Subtract 2 from both sides to get y − 2 = 5x, then divide by 5. Adding gives (y + 2)/5, which is wrong.",
             "note": "add instead of subtract -> option 1"},
            {"pattern": "order_of_ops", "expect": 3,
             "message": "Undo the +2 before the ×5. Subtract 2 first, then divide the whole side by 5. Dividing first gives y/5 − 2, which is wrong.",
             "note": "divide before subtract -> option 3"}
        ],
    },
    {  # G1
        "display": "Make \\(t\\) the subject of \\(v = u + at\\)",
        "options": ["\\(t = \\frac{v - u}{a}\\)", "\\(t = \\frac{v + u}{a}\\)", "\\(t = v - u - a\\)", "\\(t = \\frac{u - v}{a}\\)"],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Subtract u from both sides, then divide by a.",
        "misconceptions": [
            {"pattern": "wrong_rearrange", "expect": 1,
             "message": "To undo +u you subtract it: v − u = at, then divide by a. Adding u gives (v + u)/a, which is wrong.",
             "note": "add instead of subtract -> option 1"},
            {"pattern": "inverse_error", "expect": 2,
             "message": "a multiplies t, so undo it by dividing, not subtracting. After v − u = at, divide by a. Subtracting a gives v − u − a, which is wrong.",
             "note": "subtract a instead of divide -> option 2"}
        ],
    },
    {  # G2
        "display": "Make \\(r\\) the subject of \\(A = \\pi r^2\\)",
        "options": ["\\(r = \\sqrt{\\frac{A}{\\pi}}\\)", "\\(r = \\frac{A}{\\pi}\\)", "\\(r = \\sqrt{A\\pi}\\)", "\\(r = \\frac{\\sqrt{A}}{\\pi}\\)"],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Divide by pi first, then take the square root.",
        "misconceptions": [
            {"pattern": "inverse_error", "expect": 1,
             "message": "Dividing by π gives r² = A/π, but you must still undo the square by taking a root. Stopping at A/π forgets that step.",
             "note": "forgot square root -> option 1"},
            {"pattern": "order_of_ops", "expect": 3,
             "message": "Divide by π before rooting. r² = A/π, so r = √(A/π). Rooting only the A, giving √A/π, undoes things in the wrong order.",
             "note": "root before divide -> option 3"}
        ],
    },
    {  # G3
        "display": "Make \\(b\\) the subject of \\(A = \\frac{1}{2}bh\\)",
        "options": ["\\(b = \\frac{A}{2h}\\)", "\\(b = \\frac{2A}{h}\\)", "\\(b = \\frac{A}{h}\\)", "\\(b = 2Ah\\)"],
        "solutions": [1],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Multiply both sides by 2, then divide by h.",
        "misconceptions": [
            {"pattern": "inverse_error", "expect": 2,
             "message": "The half must be undone by multiplying both sides by 2: 2A = bh, then divide by h to get 2A/h. Dividing by h alone, giving A/h, keeps the half in.",
             "note": "forgot to multiply by 2 -> option 2"}
        ],
    },
    {  # G4
        "display": "Make \\(x\\) the subject of \\(y = \\frac{x - 3}{4}\\)",
        "options": ["\\(x = 4y + 3\\)", "\\(x = 4y - 3\\)", "\\(x = \\frac{y + 3}{4}\\)", "\\(x = 4(y + 3)\\)"],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Multiply both sides by 4, then add 3.",
        "misconceptions": [
            {"pattern": "sign_error", "expect": 1,
             "message": "Multiplying by 4 gives x − 3 = 4y, then add 3 to both sides: x = 4y + 3. Subtracting 3 instead gives 4y − 3, which is wrong.",
             "note": "subtract 3 instead of add -> option 1"},
            {"pattern": "wrong_rearrange", "expect": 3,
             "message": "Once x − 3 = 4y, add 3 to isolate x: x = 4y + 3. Leaving it as 4(y + 3) never cleared the bracket correctly.",
             "note": "leaves 4(y+3) -> option 3"}
        ],
    },
]

problem_bank = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "Substitute single values into simple expressions",
    "silver_description": "Substitute into formulae with powers and negatives",
    "gold_description": "Rearrange formulae to change the subject",
}

# ---------------- GUIDED (opener + teach) ----------------

guided = {
    "opener": {
        "steps": [
            say("A taxi charges £3 just to get in, then £2 for every mile. No algebra, just work out the fares."),
            box("A 4-mile trip costs £", 11, "£3 to start, then £2 for each of the 4 miles: 3 + 2 × 4."),
            say("Without noticing, you did the £2 × 4 first and added the £3 after. Multiplying before adding is <strong>BIDMAS</strong>."),
            box("A 6-mile trip costs £", 15, "£3 plus £2 for each of the 6 miles."),
            say("That rule, fare = 3 + 2 × miles, is a <strong>formula</strong>. Writing miles as a letter gives \\(f = 3 + 2m\\). Putting a number in place of \\(m\\) and working it out is <strong>substitution</strong>, and it is the whole of this lesson."),
        ]
    },
    "teach": {
        "bronze": {
            "display": "Find \\(5a + 2b\\) when \\(a = 3\\) and \\(b = 4\\)",
            "steps": [
                say("The one move here: swap each letter for its number, then follow BIDMAS, multiply before you add."),
                box("5 × 3 = ", 15, "Five lots of 3."),
                box("2 × 4 = ", 8, "Two lots of 4."),
                box("add the parts: 15 + 8 = ", 23, "Put the two products together."),
                box("Check by reading the original back: five 3s (15) and two 4s (8) total ", 23,
                    "Same total.", done="Gone. Substitute, multiply each term, then add. That was the whole point."),
            ],
        },
        "silver": {
            "display": "Find \\(2x^2 - 3\\) when \\(x = -5\\)",
            "steps": [
                say("The new move: put the negative in brackets and deal with the power first. Write 2 × (−5)² − 3."),
                box("(−5)² = (−5) × (−5) = ", 25, "Negative times negative is positive."),
                box("2 × 25 = ", 50, "Two lots of 25."),
                box("now subtract 3: 50 − 3 = ", 47, "Take the 3 off."),
                box("Check: (−5) squared is 25, doubled is 50, less 3 is ", 47,
                    "Same total.", done="Gone. Bracket the negative, power first, then multiply, then combine."),
            ],
        },
        "gold": {
            "display": "Make \\(x\\) the subject of \\(y = 4x + 12\\)",
            "steps": [
                say("The new move: rearranging undoes the formula step by step, in reverse BIDMAS. Right now x is multiplied by 4, then 12 is added. Undo the +12 first."),
                box("To undo the +12, subtract it from both sides. The number you subtract is ", 12, "Undo addition with subtraction."),
                say("That leaves \\(y - 12 = 4x\\). Now x is only multiplied by 4, so undo that."),
                box("To undo the ×4, divide both sides by ", 4, "Undo multiplication with division."),
                say("So \\(x = \\dfrac{y - 12}{4}\\). Test it with a number. If \\(y = 20\\):"),
                box("x = (20 − 12) ÷ 4 = ", 2, "Do the bracket first, then divide."),
                box("Check forwards: put x = 2 back into 4x + 12 to get ", 20,
                    "4 × 2 + 12.", done="Gone. Undo the operations in reverse, then a number test proves it."),
            ],
        },
    },
}

# ---------------- TIER GUIDES ----------------

tier_guides = {
    "bronze": {
        "title": "Bronze: substituting single values",
        "steps": [
            "<strong>Substitute</strong> means swap each letter for the number you are given, then work out the result.",
            "Follow <strong>BIDMAS</strong>: do any multiplication or division before addition or subtraction.",
            "Write the calculation out fully before you touch the arithmetic. It stops silly slips.",
        ],
        "example": {
            "question": "Find \\(4x + 3\\) when \\(x = 2\\)",
            "steps": [
                {"label": "Substitute", "content": "\\(4 \\times 2 + 3\\)"},
                {"label": "Multiply first", "content": "\\(8 + 3\\)"},
                {"label": "Check", "content": "8, then add the 3"},
                {"label": "Answer", "content": "\\(11\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: powers and negative values",
        "steps": [
            "Deal with <strong>powers first</strong>: square the value before any multiply or add.",
            "Put negative values in <strong>brackets</strong> so the sign is safe: \\((-3)^2 = 9\\), not \\(-9\\).",
            "Then finish with BIDMAS: multiplications, then additions and subtractions.",
        ],
        "example": {
            "question": "Find \\(x^2 - 4\\) when \\(x = -3\\)",
            "steps": [
                {"label": "Substitute", "content": "\\((-3)^2 - 4\\)"},
                {"label": "Power first", "content": "\\(9 - 4\\)"},
                {"label": "Check", "content": "nine take four"},
                {"label": "Answer", "content": "\\(5\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: changing the subject",
        "steps": [
            "<strong>Rearranging</strong> means getting one letter on its own using inverse operations.",
            "Work in reverse BIDMAS: undo adding and subtracting first, then multiplying and dividing, then powers with a root.",
            "Whatever you do to one side, do to the other. A quick number test proves the result.",
        ],
        "example": {
            "question": "Make \\(x\\) the subject of \\(y = 2x - 6\\)",
            "steps": [
                {"label": "Add 6 to both sides", "content": "\\(y + 6 = 2x\\)"},
                {"label": "Divide both sides by 2", "content": "\\(\\frac{y + 6}{2} = x\\)"},
                {"label": "Check with y = 4", "content": "\\((4 + 6) \\div 2 = 5\\), and \\(2 \\times 5 - 6 = 4\\)"},
                {"label": "Answer", "content": "\\(x = \\frac{y + 6}{2}\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------- METHOD CARD (slim) ----------------

method_card = {
    "title": "Substitute and Rearrange Formulae",
    "steps": [
        "Write out the formula.",
        "Replace each letter with its value, using brackets around negatives.",
        "Follow BIDMAS: powers, then multiply or divide, then add or subtract.",
        "To change the subject, undo operations in reverse with the inverse of each.",
    ],
    "content": "<p><strong>Substitution</strong> swaps letters for given numbers, then evaluates with BIDMAS. Brackets around a negative keep its sign safe, so \\((-3)^2 = 9\\).</p><p><strong>Rearranging</strong> (changing the subject) isolates one letter using inverse operations in reverse BIDMAS order. Whatever you do to one side, do to the other, then test with a number.</p>",
    "example": "<p><strong>Given</strong> \\(v = u + at\\), find \\(v\\) when \\(u = 5\\), \\(a = 3\\), \\(t = 4\\): \\(v = 5 + 3 \\times 4 = 5 + 12 = 17\\).</p>",
}

# ---------------- PRESERVED FIELDS ----------------

topic_links = {
    "prerequisites": [
        {"slug": "algebra/1", "title": "Simplifying Expressions"}
    ]
}

related_videos = [
    {"url": "https://www.youtube.com/watch?v=ZkC2FX5TOJ8", "title": "Substitution into Expressions", "channel": "Corbett Maths"}
]

# worked_examples preserved; em dashes in labels replaced with colons (validator forbids em dash)
worked_examples = [
    {
        "steps": [
            {"label": "Step 1: Substitute", "content": "<p>\\(3(4) + 2\\)</p>"},
            {"label": "Step 2: Calculate", "content": "<p>\\(12 + 2 = 14\\)</p>"},
            {"label": "Answer", "content": "<p><strong>14</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "Find the value of 3x + 2 when x = 4",
        "difficulty": "Bronze",
    },
    {
        "steps": [
            {"label": "Step 1: Substitute", "content": "<p>\\(A = \\frac{1}{2} \\times 8 \\times 5\\)</p>"},
            {"label": "Step 2: Calculate", "content": "<p>\\(A = \\frac{1}{2} \\times 40 = 20\\)</p>"},
            {"label": "Answer", "content": "<p><strong>\\(A = 20\\)</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "Given A = ½bh, find A when b = 8 and h = 5",
        "difficulty": "Silver",
    },
    {
        "steps": [
            {"label": "Step 1: Substitute", "content": "<p>\\((-2)^2 - 3(-2) + 1\\)</p>"},
            {"label": "Step 2: Calculate powers", "content": "<p>\\(4 - 3(-2) + 1\\)</p>"},
            {"label": "Step 3: Multiply", "content": "<p>\\(4 + 6 + 1 = 11\\)</p>"},
            {"label": "Answer", "content": "<p><strong>11</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "Find the value of x² − 3x + 1 when x = −2",
        "difficulty": "Silver",
    },
    {
        "steps": [
            {"label": "Step 1: Add 7 to both sides", "content": "<p>\\(y + 7 = 3x\\)</p>"},
            {"label": "Step 2: Divide both sides by 3", "content": "<p>\\(\\frac{y + 7}{3} = x\\)</p>"},
            {"label": "Answer", "content": "<p><strong>\\(x = \\frac{y + 7}{3}\\)</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "Make x the subject of y = 3x − 7",
        "difficulty": "Gold",
    },
]

practice_data = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": problem_bank,
    "tier_guides": tier_guides,
    "guided": guided,
    "related_videos": related_videos,
    "worked_examples": worked_examples,
}

with io.open("lesson_algebra-L04.json", "w", encoding="utf-8") as f:
    json.dump(practice_data, f, indent=1, ensure_ascii=False)

print("written lesson_algebra-L04.json")
