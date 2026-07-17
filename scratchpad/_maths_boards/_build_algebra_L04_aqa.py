# -*- coding: utf-8 -*-
"""Full guided-learning conversion of maths-aqa algebra-L04 (Formulae & Substitution)."""
import json, io

SRC = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_live_algebra-L04.json"
OUT = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-aqa_algebra-L04.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

MINUS = "−"  # unicode minus

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s):
    return {"say": s}

# ---------------------------------------------------------------- method_card
pd["method_card"] = {
    "title": "Substituting and Rearranging Formulae",
    "steps": [
        "Replace each letter with its value in brackets, then use BIDMAS.",
        "A negative number squared is positive.",
        "To change the subject, undo operations on both sides in reverse order.",
        "If the new subject appears twice, collect those terms, factorise, then divide.",
    ],
    "content": ("<p><strong>Substitution</strong> means replacing letters with numbers and working the "
                "result out with BIDMAS: brackets and powers before × and ÷, and those before "
                "+ and " + MINUS + ".</p>"
                "<p><strong>Rearranging</strong> a formula changes which letter is the subject. Undo each "
                "operation on both sides in reverse order, so a + becomes a " + MINUS + ", a × becomes "
                "a ÷, and a power becomes a root.</p>"
                "<p>When the new subject appears more than once, gather its terms on one side, factorise it "
                "out, then divide.</p>"),
    "example": ("<p><strong>Given</strong> \\(v = u + at\\), find \\(v\\) when \\(u = 5\\), \\(a = 3\\), "
                "\\(t = 4\\).</p><p>\\(v = 5 + 3 \\times 4 = 5 + 12 = 17\\)</p>"),
}

# ---------------------------------------------------------------- tier_guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: substitute numbers into a formula",
        "steps": [
            "Write the formula, then replace each letter with its value in brackets.",
            "Work it out with <strong>BIDMAS</strong>: powers and brackets before × and ÷, and those before + and " + MINUS + ".",
            "Watch signs: a negative value squared is positive.",
        ],
        "example": {
            "question": "If \\(y = 2x + 5\\), find \\(y\\) when \\(x = 3\\)",
            "steps": [
                {"label": "Substitute", "content": "\\(y = 2(3) + 5\\)"},
                {"label": "Multiply first", "content": "\\(y = 6 + 5\\)"},
                {"label": "Check", "content": "Multiply before adding, so the order is right."},
                {"label": "Answer", "content": "\\(y = 11\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: rearrange, then substitute",
        "steps": [
            "To change the subject, undo operations in reverse, doing the same to both sides.",
            "To find a letter that is not the subject, substitute the known values first, then solve.",
            "Undo + and " + MINUS + " first, then × and ÷, then powers with roots.",
        ],
        "example": {
            "question": "If \\(y = 4x " + MINUS + " 1\\), find \\(x\\) when \\(y = 11\\)",
            "steps": [
                {"label": "Substitute y", "content": "\\(11 = 4x - 1\\)"},
                {"label": "Add 1 to both sides", "content": "\\(12 = 4x\\)"},
                {"label": "Check", "content": "Divide both sides by 4 to leave x alone."},
                {"label": "Answer", "content": "\\(x = 3\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: powers, roots and repeated subjects",
        "steps": [
            "Clear fractions first: multiply both sides by the denominator.",
            "If the new subject appears twice, gather those terms, factorise, then divide.",
            "Undo a power with a root, and a root with a power, at the very end.",
        ],
        "example": {
            "question": "Make \\(x\\) the subject of \\(y = \\frac{x + 4}{2}\\)",
            "steps": [
                {"label": "Multiply by 2", "content": "\\(2y = x + 4\\)"},
                {"label": "Subtract 4", "content": "\\(2y - 4 = x\\)"},
                {"label": "Check", "content": "x is now alone, so read it off."},
                {"label": "Answer", "content": "\\(x = 2y - 4\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------- guided
pd["guided"] = {
    "opener": {
        "steps": [
            sayonly("A taxi charges £3 to get in, then £2 for every mile you travel."),
            box("A 4-mile trip costs £", 11, "£3 to start, then £2 four times: 3 + 2 × 4."),
            box("A 6-mile trip costs £", 15, "Same idea: 3 + 2 × 6."),
            sayonly("You just used a formula. Call the cost \\(C\\) and the miles \\(m\\): every trip is "
                    "\\(C = 3 + 2m\\). <strong>Substituting</strong> means putting the number of miles in "
                    "for \\(m\\) and working it out. That is the whole of this lesson."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "If \\(y = 2x^2 + 3x\\), find \\(y\\) when \\(x = 4\\)",
            "steps": [
                sayonly("Substitution means swapping the letter for its number, then using BIDMAS. Put "
                        "\\(x = 4\\) into \\(y = 2x^2 + 3x\\)."),
                box("Powers first. \\(x^2 = 4 × 4 = \\)", 16, "4 squared is 4 times 4."),
                box("Now the 2 in front: 2 × 16 = ", 32, "Multiply your 16 by 2."),
                box("The other term, 3x = 3 × 4 = ", 12, "Multiply 3 by the x value."),
                box("Add the two parts: 32 + 12 = ", 44, "Add the two pieces together.",
                    done="y = 44. Powers, then ×, then +. That order is the whole trick."),
            ],
        },
        "silver": {
            "display": "If \\(E = \\frac{1}{2}mv^2\\), find \\(v\\) when \\(E = 90\\) and \\(m = 5\\)",
            "steps": [
                sayonly("We want v, and v is squared, so unwrap it in stages. Substitute \\(E = 90\\), "
                        "\\(m = 5\\) into \\(E = \\frac{1}{2}mv^2\\)."),
                box("The ½m part: ½ × 5 = ", 2.5, "Half of 5."),
                sayonly("So \\(90 = 2.5\\,v^2\\)."),
                box("Divide both sides by 2.5: v² = 90 ÷ 2.5 = ", 36, "Undo the × 2.5 by dividing."),
                sayonly("Now \\(v^2 = 36\\), so take the square root."),
                box("v = √36 = ", 6, "What number times itself gives 36?"),
                box("Check: ½ × 5 × 6² = ½ × 5 × 36 = ", 90,
                    "Put v = 6 back in.",
                    done="It gives 90, so v = 6 is right. Undo the × before the power, then square root last."),
            ],
        },
        "gold": {
            "display": "If \\(y = \\frac{3x}{x - 4}\\), find \\(x\\) when \\(y = 6\\)",
            "steps": [
                sayonly("y is given, and x sits top and bottom. Clear the fraction: multiply both sides by "
                        "\\((x - 4)\\). Substitute \\(y = 6\\)."),
                box("On the left, 6 × (x " + MINUS + " 4) gives 6x " + MINUS + " 24. Work out 6 × 4 = ",
                    24, "6 times 4."),
                sayonly("So \\(6x - 24 = 3x\\). Gather x terms: take 3x from both sides."),
                box("6x " + MINUS + " 3x = ", 3, "Subtract the x coefficients: 6 " + MINUS + " 3.", post="x"),
                sayonly("Now \\(3x = 24\\)."),
                box("Divide both sides by 3: x = 24 ÷ 3 = ", 8, "Undo the × 3."),
                box("Check: 3 × 8 ÷ (8 " + MINUS + " 4) = 24 ÷ 4 = ", 6, "Put x = 8 back in.",
                    done="It gives 6, so x = 8. Clearing the fraction turned it into a straight-line solve."),
            ],
        },
    },
}

# ---------------------------------------------------------------- problem_bank
pb = pd["problem_bank"]
pb["bronze_description"] = "Put the given numbers in place of the letters and work it out using BIDMAS."
pb["silver_description"] = "Change the subject of a formula, or substitute into a bigger formula and solve for a value that is not the subject."
pb["gold_description"] = "Rearrange formulae with powers, roots, or the new subject appearing more than once."

def misc(pattern, message, expect, note=None):
    d = {"pattern": pattern, "check": pattern, "message": message, "expect": expect}
    if note is not None: d["note"] = note
    return d

# ---- BRONZE ----
b = pb["bronze"]

b[0]["hint"] = "Work out 3 × 4 first, then add 7."
b[0]["misconceptions"] = []
b[0]["guided_steps"] = [
    box("The 3x part: 3 × 4 = ", 12, "Multiply the number in front of x by the x value."),
    box("Add the 7: 12 + 7 = ", 19, "Add what is left in the formula.", phase="substitute"),
    box("Check with the original: 3 × 4 + 7 = ", 19, "Work it straight through.",
        phase="substitute", done="It gives 19, so y = 19 is right."),
]

b[1]["hint"] = "Work out 2 × 8 and 2 × 3, then add them."
b[1]["misconceptions"] = [
    misc("half_doubled", "Both terms are doubled: 2 × 8 = 16 and 2 × 3 = 6, giving 22. "
         "Doubling only l and adding a single w gives 19.", 19, note="2l + w = 16 + 3 = 19"),
]
b[1]["guided_steps"] = [
    box("The 2l part: 2 × 8 = ", 16, "Double the length."),
    box("The 2w part: 2 × 3 = ", 6, "Double the width."),
    box("Add them: 16 + 6 = ", 22, "Add the two doubled parts.", phase="substitute"),
    box("Check: 2 × 8 + 2 × 3 = ", 22, "Work it straight through.",
        phase="substitute", done="It gives 22, so P = 22 is right."),
]

b[2]["hint"] = "Square the radius first (5 × 5), then multiply by π and round to 1 d.p."
b[2]["misconceptions"] = [
    misc("squared_as_double", "r² means r × r = 25, not r × 2. π × 25 = 78.5. "
         "Doubling the radius gives π × 10 = 31.4, which is wrong.", 31.4,
         note="pi*10 = 31.415... = 31.4"),
]
b[2]["guided_steps"] = [
    box("Square the radius: 5 × 5 = ", 25, "5 squared is 5 times 5."),
    box("Multiply by π and round to 1 d.p.: π × 25 = ", 78.5, "Use the π button, then round.",
        phase="substitute"),
    box("Check the squaring: 5 × 5 = ", 25, "Confirm the first step.",
        phase="substitute", done="25 lots of π rounds to 78.5, so A = 78.5 is right."),
]

b[3]["hint"] = "Work out a × t = (" + MINUS + "2) × 6 first, then add u = 3. Mind the minus."
b[3]["misconceptions"] = [
    misc("dropped_minus", "a is " + MINUS + "2, so at = (" + MINUS + "2) × 6 = " + MINUS + "12, "
         "and 3 + (" + MINUS + "12) = " + MINUS + "9. Ignoring the minus gives 3 + 12 = 15.", 15,
         note="drops sign on a: 3 + 12 = 15"),
]
b[3]["guided_steps"] = [
    box("The at part: (" + MINUS + "2) × 6 = ", -12, "Multiply, and keep the minus sign."),
    box("Add u: 3 + (" + MINUS + "12) = ", -9, "Adding a negative is the same as subtracting.",
        phase="substitute"),
    box("Check: 3 + (" + MINUS + "2) × 6 = ", -9, "Work it straight through.",
        phase="substitute", done="It gives " + MINUS + "9, so v = " + MINUS + "9 is right."),
]

b[4]["hint"] = "A negative squared is positive: (" + MINUS + "3) × (" + MINUS + "3) = 9, then subtract 4."
b[4]["misconceptions"] = [
    misc("neg_square_sign", "(" + MINUS + "3)² = (" + MINUS + "3) × (" + MINUS + "3) = 9, a "
         "positive. Then 9 " + MINUS + " 4 = 5. Reading it as " + MINUS + "9 gives " + MINUS + "9 " + MINUS + " 4 = " + MINUS + "13.",
         -13, note="treats (-3)^2 as -9: -9-4 = -13"),
]
b[4]["guided_steps"] = [
    box("Square x: (" + MINUS + "3) × (" + MINUS + "3) = ", 9, "A negative times a negative is positive."),
    box("Subtract 4: 9 " + MINUS + " 4 = ", 5, "Take 4 from the squared value.", phase="substitute"),
    box("Confirm the sign: (" + MINUS + "3) × (" + MINUS + "3) = ", 9, "Check the square is positive.",
        phase="substitute", done="9 " + MINUS + " 4 = 5, so y = 5 is right."),
]

b[5]["hint"] = "Do the bracket 68 " + MINUS + " 32 first, then × 5, then ÷ 9."
b[5]["misconceptions"] = []
b[5]["guided_steps"] = [
    box("Bracket first: 68 " + MINUS + " 32 = ", 36, "Work inside the bracket before anything else."),
    box("Multiply by 5: 5 × 36 = ", 180, "Multiply the bracket result by 5."),
    box("Divide by 9: 180 ÷ 9 = ", 20, "Divide the top by 9.", phase="substitute"),
    box("Check: does 20 × 9 = 180? 20 × 9 = ", 180, "Multiplying back should give 180.",
        phase="substitute", done="It does, so C = 20 is right."),
]

b[6]["hint"] = "Speed = distance ÷ time, so work out 150 ÷ 6."
b[6]["misconceptions"] = [
    misc("inverted_divide", "Speed = distance ÷ time = 150 ÷ 6 = 25. Doing time ÷ distance = "
         "6 ÷ 150 = 0.04 turns the fraction upside down.", 0.04, note="t/d = 6/150 = 0.04"),
]
b[6]["guided_steps"] = [
    box("Build up 150 ÷ 6. First, 6 × 20 = ", 120, "How far do twenty 6s reach?"),
    box("What is left: 150 " + MINUS + " 120 = 30, and 30 ÷ 6 = ", 5, "Share the remaining 30 into 6s."),
    box("So s = 20 + 5 = ", 25, "Add the two parts of the division.", phase="substitute"),
    box("Check: 6 × 25 = ", 150, "Multiplying back should give the distance.",
        phase="substitute", done="It gives 150, so s = 25 is right."),
]

b[7]["hint"] = "Square x first (2² = 4), then double it, then add 3x."
b[7]["misconceptions"] = [
    misc("bracket_the_coefficient", "2x² means 2 × (x × x) = 2 × 4 = 8, not (2x)². "
         "Squaring 2x gives (2 × 2)² = 16, and 16 + 6 = 22, which is wrong.", 22,
         note="(2x)^2 + 3x = 16 + 6 = 22"),
]
b[7]["guided_steps"] = [
    box("Square x only: 2 × 2 = ", 4, "x squared is 2 times 2."),
    box("Now the 2 in front: 2 × 4 = ", 8, "Multiply the squared value by 2."),
    box("The other term, 3x = 3 × 2 = ", 6, "Multiply 3 by the x value."),
    box("Add the parts: 8 + 6 = ", 14, "Add the two terms.", phase="substitute"),
    box("Check by adding again: 8 + 6 = ", 14, "Confirm the total.",
        phase="substitute", done="It gives 14, so y = 14 is right."),
]

# ---- SILVER ----
s = pb["silver"]

# silver[0] MC - keep, add hint + real distractor diagnostic (expect = wrong option index)
s[0]["hint"] = "Subtract c, then divide by m. The bottom of the fraction is what you divide by."
s[0]["misconceptions"] = [
    misc("mc_wrong_denominator", "The denominator is what you divide by. From \\(x = \\frac{y - c}{m}\\) "
         "you divide by m, not c. c is subtracted, not divided.", 1, note="picks option 1 (c)"),
]

# silver[1] REPLACED (was mis-posed) -> well-posed substitution on the same formula
s[1] = {
    "display": "If \\(v^2 = u^2 + 2as\\), find \\(s\\) when \\(v = 10\\), \\(u = 4\\), \\(a = 6\\)",
    "solutions": [7],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Work out v², u² and 2a, then solve 100 = 16 + 12s for s.",
    "misconceptions": [
        misc("forgot_to_square", "v and u must be squared: v² = 100 and u² = 16, giving "
             "100 = 16 + 12s and s = 7. Leaving them unsquared gives 10 = 4 + 12s, so s = 0.5.", 0.5,
             note="10 = 4 + 12s -> s = 0.5"),
        misc("used_a_not_2a", "The s term is 2as, so its coefficient is 2 × 6 = 12, not 6. Using 6 "
             "gives 84 ÷ 6 = 14 instead of 84 ÷ 12 = 7.", 14, note="84/6 = 14"),
    ],
    "guided_steps": [
        box("Square v: 10 × 10 = ", 100, "v squared is 10 times 10."),
        box("Square u: 4 × 4 = ", 16, "u squared is 4 times 4."),
        box("The coefficient of s: 2 × 6 = ", 12, "2a means 2 times a."),
        box("So 100 = 16 + 12s. Subtract 16 from both sides: 100 " + MINUS + " 16 = ", 84,
            "Undo the +16 by subtracting 16."),
        box("Now 12s = 84, so s = 84 ÷ 12 = ", 7, "Divide both sides by 12.", phase="substitute"),
        box("Check: 4² + 2 × 6 × 7 = 16 + 84 = ", 100, "Put s = 7 back in.",
            phase="substitute", done="It gives 100 = v², so s = 7 is right."),
    ],
}

s[2]["hint"] = "Substitute y = " + MINUS + "3, then undo: subtract 5, then divide by " + MINUS + "2."
s[2]["misconceptions"] = [
    misc("divide_sign_slip", "The x term is " + MINUS + "2x, so divide by " + MINUS + "2. "
         "(" + MINUS + "8) ÷ (" + MINUS + "2) = 4. Dividing by 2 gives " + MINUS + "4, the wrong sign.",
         -4, note="-8/2 = -4"),
]
s[2]["guided_steps"] = [
    box("Substitute y = " + MINUS + "3, giving " + MINUS + "3 = 5 " + MINUS + " 2x. Take 5 from both sides: "
        + MINUS + "3 " + MINUS + " 5 = ", -8, "Undo the +5 by subtracting 5."),
    box("Now " + MINUS + "8 = " + MINUS + "2x. Divide both sides by " + MINUS + "2: x = (" + MINUS + "8) ÷ (" + MINUS + "2) = ",
        4, "A negative divided by a negative is positive.", phase="substitute"),
    box("Check: 5 " + MINUS + " 2 × 4 = 5 " + MINUS + " 8 = ", -3, "Put x = 4 back in.",
        phase="substitute", done="It gives " + MINUS + "3, so x = 4 is right."),
]

# silver[3] MC keep
s[3]["hint"] = "Multiply both sides by 2, then divide by (a + b)."
s[3]["misconceptions"] = [
    misc("mc_half_wrong_way", "Multiplying by 2 clears the ½, giving \\(h = \\frac{2A}{a+b}\\). "
         "Dividing by 2 instead gives \\(\\frac{A}{2(a+b)}\\), the ½ handled backwards.", 1,
         note="picks option 1"),
]

s[4]["hint"] = "Work out ut and ½at² separately (remember t² first), then add."
s[4]["misconceptions"] = [
    misc("forgot_half", "The second term is ½ × 4 × 9 = 18, giving s = 30 + 18 = 48. "
         "Forgetting the ½ makes it 4 × 9 = 36, so s = 66.", 66, note="30 + 36 = 66"),
]
s[4]["guided_steps"] = [
    box("First term, ut = 10 × 3 = ", 30, "Multiply u by t."),
    box("Square t: 3 × 3 = ", 9, "t squared is 3 times 3."),
    box("Second term, ½ × 4 × 9 = ", 18, "Half of 4 times 9."),
    box("Add the terms: 30 + 18 = ", 48, "Add the two parts.", phase="substitute"),
    box("Check: 10 × 3 + ½ × 4 × 9 = 30 + 18 = ", 48, "Work it straight through.",
        phase="substitute", done="It gives 48, so s = 48 is right."),
]

# silver[5] MC keep
s[5]["hint"] = "Divide by 2π, then square both sides, then multiply by g."
s[5]["misconceptions"] = [
    misc("mc_inverted", "Squaring \\(\\frac{T}{2\\pi}\\) puts T² on top: \\(l = \\frac{T^2 g}{4\\pi^2}\\). "
         "The option with T² on the bottom squares the wrong side.", 1, note="picks option 1"),
]

s[6]["hint"] = "Find ½m first, divide E by it to get v², then square root."
s[6]["misconceptions"] = [
    misc("forgot_root", "v² = 25, so v = √25 = 5. Stopping at 25 forgets the final square root.",
         25, note="stops at v^2 = 25"),
]
s[6]["guided_steps"] = [
    box("The ½m part: ½ × 8 = ", 4, "Half of 8."),
    box("So 100 = 4v². Divide both sides by 4: v² = 100 ÷ 4 = ", 25, "Undo the × 4 by dividing."),
    box("Now v² = 25, so v = √25 = ", 5, "What number times itself gives 25?", phase="substitute"),
    box("Check: ½ × 8 × 5² = 4 × 25 = ", 100, "Put v = 5 back in.",
        phase="substitute", done="It gives 100, so v = 5 is right."),
]

# ---- GOLD ----
g = pb["gold"]

# gold[0] REPLACED (meta 'find a' -> numeric solve on same formula)
g[0] = {
    "display": "If \\(y = \\frac{x + 3}{x - 1}\\), find \\(x\\) when \\(y = 3\\)",
    "solutions": [3],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Multiply both sides by (x " + MINUS + " 1), expand, gather x terms, then solve.",
    "misconceptions": [
        misc("partial_bracket", "3 × (x " + MINUS + " 1) = 3x " + MINUS + " 3, so 3x " + MINUS + " 3 = x + 3 "
             "and x = 3. Multiplying only the x, as 3x " + MINUS + " 1, gives x = 2.", 2,
             note="3x-1 = x+3 -> 2x=4 -> x=2"),
    ],
    "guided_steps": [
        box("Substitute y = 3 and clear the fraction: 3 × (x " + MINUS + " 1). Work out 3 × 1 = ",
            3, "Multiply the 3 by the 1 inside the bracket."),
        box("So 3x " + MINUS + " 3 = x + 3. Take x from both sides: 3x " + MINUS + " x = ", 2,
            "Subtract the x coefficients: 3 " + MINUS + " 1.", post="x"),
        box("Add 3 to both sides: 3 + 3 = ", 6, "Move the " + MINUS + "3 across to the numbers."),
        box("Now 2x = 6, so x = 6 ÷ 2 = ", 3, "Divide both sides by 2.", phase="substitute"),
        box("Check: (3 + 3) ÷ (3 " + MINUS + " 1) = 6 ÷ 2 = ", 3, "Put x = 3 back in.",
            phase="substitute", done="It gives 3, so x = 3 is right."),
    ],
}

# gold[1] MC keep
g[1]["hint"] = "Multiply by 3, divide by 4π, then take the cube root."
g[1]["misconceptions"] = [
    misc("mc_forgot_cube_root", "\\(r^3 = \\frac{3V}{4\\pi}\\), so r is the cube root of that. "
         "Leaving it as \\(\\frac{3V}{4\\pi}\\) forgets to undo the cube.", 1, note="picks option 1"),
]

g[2]["hint"] = "Multiply both sides by (x + 1), expand, gather x terms, then solve."
g[2]["misconceptions"] = [
    misc("sign_slip", "From x + 3 = 0 the answer is x = " + MINUS + "3. Reading it as x = 3 flips the sign.",
         3, note="x+3=0 -> x=-3, slip gives 3"),
]
g[2]["guided_steps"] = [
    box("Substitute y = 3 and clear the fraction: 3 × (x + 1). Work out 3 × 1 = ", 3,
        "Multiply the 3 by the 1 inside the bracket."),
    box("So 3x + 3 = 2x. Take 2x from both sides: 3x " + MINUS + " 2x = ", 1,
        "Subtract the x coefficients: 3 " + MINUS + " 2.", post="x"),
    box("Now x + 3 = 0, so x = 0 " + MINUS + " 3 = ", -3, "Move the +3 across to make x alone.",
        phase="substitute"),
    box("Check: 2 × (" + MINUS + "3) ÷ (" + MINUS + "3 + 1) = " + MINUS + "6 ÷ (" + MINUS + "2) = ",
        3, "Put x = " + MINUS + "3 back in.",
        phase="substitute", done="It gives 3, so x = " + MINUS + "3 is right."),
]

# gold[3] MC keep
g[3]["hint"] = "Subtract ut, then multiply by 2, then divide by t²."
g[3]["misconceptions"] = [
    misc("mc_forgot_double", "Multiplying by 2 clears the ½: \\(a = \\frac{2(s - ut)}{t^2}\\). "
         "Dropping the 2 gives \\(\\frac{s - ut}{t^2}\\).", 1, note="picks option 1"),
]

g[4]["hint"] = "Add 5, divide by 3, then take the positive square root."
g[4]["misconceptions"] = [
    misc("forgot_root", "x² = 16, so x = √16 = 4. Stopping at 16 forgets the final square root.",
         16, note="stops at x^2 = 16"),
]
g[4]["guided_steps"] = [
    box("Substitute y = 43: 43 = 3x² " + MINUS + " 5. Add 5 to both sides: 43 + 5 = ", 48,
        "Undo the " + MINUS + "5 by adding 5."),
    box("Now 3x² = 48. Divide both sides by 3: x² = 48 ÷ 3 = ", 16, "Undo the × 3 by dividing."),
    box("So x² = 16, and the positive root is x = √16 = ", 4,
        "What positive number times itself gives 16?", phase="substitute"),
    box("Check: 3 × 4² " + MINUS + " 5 = 3 × 16 " + MINUS + " 5 = 48 " + MINUS + " 5 = ", 43,
        "Put x = 4 back in.", phase="substitute", done="It gives 43, so x = 4 is right."),
]

# ---------------------------------------------------------------- write
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("wrote", OUT)
