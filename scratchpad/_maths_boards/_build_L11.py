# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L11_live.json", encoding="utf-8"))

# Preserve: method_card, topic_links, related_videos, worked_examples
pd = {}
pd["method_card"] = live["method_card"]
pd["topic_links"] = live["topic_links"]

MINUS = "−"  # unicode minus

def mc(display, options, sols, hint, miscs):
    return {"display": display, "options": options, "solutions": sols,
            "calculator": False, "input_type": "multiple_choice",
            "hint": hint, "misconceptions": miscs}

def sv(display, sol, hint, miscs, steps):
    return {"display": display, "solutions": [sol], "calculator": False,
            "input_type": "single_value", "hint": hint,
            "misconceptions": miscs, "guided_steps": steps}

def m(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect,
            "message": message, "note": note}

# ---------------- BRONZE ----------------
bronze = [
    mc("Solve \\(x + 4 > 9\\). Which is the solution?",
       ["\\(x > 5\\)", "\\(x > 13\\)", "\\(x < 5\\)", "\\(x > 4\\)"], [0],
       "Subtract 4 from both sides to get x on its own.",
       [m("arithmetic", 1, "Take 4 off both sides, do not add it: x > 9 " + MINUS + " 4 = 5.", "Adds 4: x>13."),
        m("wrong_direction", 2, "You have the right boundary, but the arrow points the wrong way. x > 5 means x is bigger than 5.", "Reverses to x<5.")]),
    mc("Solve \\(2x < 10\\). Which is the solution?",
       ["\\(x < 5\\)", "\\(x < 20\\)", "\\(x > 5\\)", "\\(x < 8\\)"], [0],
       "Divide both sides by 2.",
       [m("arithmetic", 1, "To undo 2 times x, divide by 2, do not multiply: x < 10 ÷ 2 = 5.", "Multiplies by 2: x<20."),
        m("wrong_direction", 2, "The boundary 5 is right, but the arrow is reversed. Dividing by a positive keeps the same symbol.", "Reverses to x>5."),
        m("arithmetic", 3, "To undo 2 times x, divide by 2, do not subtract 2: x < 5.", "Subtracts 2: 10" + MINUS + "2=8.")]),
    mc("Solve \\(x - 3 \\geq 7\\). Which is the solution?",
       ["\\(x \\geq 10\\)", "\\(x \\geq 4\\)", "\\(x \\leq 10\\)", "\\(x > 10\\)"], [0],
       "Add 3 to both sides.",
       [m("arithmetic", 1, "Add 3 to both sides, do not subtract it: x ≥ 7 + 3 = 10.", "Subtracts 3: 7" + MINUS + "3=4."),
        m("wrong_direction", 2, "The boundary 10 is right, but the arrow points the wrong way.", "Reverses to x<=10."),
        m("strict_vs_nonstrict", 3, "The question uses ≥, so 10 is included. x > 10 wrongly leaves 10 out.", "Uses > instead of >=.")]),
    mc("Solve \\(3x + 1 > 16\\). Which is the solution?",
       ["\\(x > 5\\)", "\\(x > 17\\)", "\\(x < 5\\)", "\\(x > 6\\)"], [0],
       "Subtract 1 from both sides, then divide by 3.",
       [m("wrong_direction", 2, "The boundary 5 is right, but the arrow is reversed. No negative was divided, so the sign stays.", "Reverses to x<5.")]),
    mc("Solve \\(4x \\leq 20\\). Which is the solution?",
       ["\\(x \\leq 5\\)", "\\(x \\geq 5\\)", "\\(x < 5\\)", "\\(x \\leq 16\\)"], [0],
       "Divide both sides by 4.",
       [m("wrong_direction", 1, "The boundary 5 is right, but the arrow is reversed. Dividing by a positive keeps the symbol.", "Reverses to x>=5."),
        m("strict_vs_nonstrict", 2, "The question uses ≤, so 5 is included. x < 5 wrongly leaves 5 out.", "Uses < instead of <=."),
        m("arithmetic", 3, "To undo 4 times x, divide by 4, do not subtract 4: x ≤ 5.", "Subtracts 4: 20" + MINUS + "4=16.")]),
    mc("Solve \\(x + 7 < 3\\). Which is the solution?",
       ["\\(x < -4\\)", "\\(x < 10\\)", "\\(x > -4\\)", "\\(x < 4\\)"], [0],
       "Subtract 7 from both sides.",
       [m("arithmetic", 1, "Take 7 off both sides, do not add it: x < 3 " + MINUS + " 7 = " + MINUS + "4.", "Adds 7: 3+7=10."),
        m("wrong_direction", 2, "The boundary " + MINUS + "4 is right, but the arrow points the wrong way.", "Reverses to x>-4."),
        m("arithmetic", 3, "3 " + MINUS + " 7 = " + MINUS + "4, not 4. The answer is negative.", "Drops the minus sign.")]),
    sv("How many integer values of \\(n\\) satisfy \\(2 < n \\leq 6\\)?", 4,
       "List the whole numbers above 2 and up to 6, then count them.",
       [m("strict_vs_nonstrict", 5, "2 < n is strict, so 2 is not included. The integers are 3, 4, 5, 6, which is 4.", "Includes 2: counts 5."),
        m("strict_vs_nonstrict", 3, "n ≤ 6 includes 6. Count 3, 4, 5, 6, which is 4.", "Drops 6: counts 3.")],
       [{"say": "You want every whole number bigger than 2 but no bigger than 6."},
        {"say": "2 < n is strict, so 2 itself is left out. Start just above it."},
        {"pre": "The smallest integer bigger than 2 is ", "post": "", "answer": 3, "hint": "The next whole number above 2."},
        {"pre": "n ≤ 6 includes 6, so the largest integer is ", "post": "", "answer": 6, "hint": "≤ keeps the boundary in.", "phase": "substitute"},
        {"pre": "Count the integers from 3 up to 6: ", "post": "", "answer": 4, "hint": "Count 3, 4, 5, 6.", "done": "Four integers. The traps are including 2 or dropping 6.", "phase": "substitute"}]),
    mc("Solve \\(5x - 2 > 18\\). Which is the solution?",
       ["\\(x > 4\\)", "\\(x > 16\\)", "\\(x > 3.2\\)", "\\(x < 4\\)"], [0],
       "Add 2 to both sides, then divide by 5.",
       [m("wrong_direction", 3, "The boundary 4 is right, but the arrow points the wrong way.", "Reverses to x<4."),
        m("arithmetic", 2, "Move the " + MINUS + "2 across by adding: 5x > 18 + 2 = 20, then divide by 5 to get x > 4.", "Subtracts: 5x>16, x>3.2.")]),
]

# ---------------- SILVER ----------------
silver = [
    mc("Solve \\(5 - 2x \\geq 1\\). Which is the solution?",
       ["\\(x \\leq 2\\)", "\\(x \\geq 2\\)", "\\(x \\leq -2\\)", "\\(x \\geq -2\\)"], [0],
       "Subtract 5, then divide by minus 2 and flip the sign.",
       [m("didnt_flip", 1, "When you divide both sides by a negative number, flip the inequality sign: ≥ becomes ≤.", "Divides by -2 without flipping: x>=2."),
        m("arithmetic", 3, "The coefficient is " + MINUS + "2, not 2. Divide " + MINUS + "4 by " + MINUS + "2 and flip: x ≤ 2.", "Divides -4 by 2 without flipping: x>=-2.")]),
    mc("Solve \\(7 - 3x < 1\\). Which is the solution?",
       ["\\(x > 2\\)", "\\(x < 2\\)", "\\(x > -2\\)", "\\(x < -2\\)"], [0],
       "Subtract 7, then divide by minus 3 and flip the sign.",
       [m("didnt_flip", 1, "When you divide both sides by a negative number, flip the inequality sign: < becomes >.", "Divides by -3 without flipping: x<2."),
        m("arithmetic", 2, "A negative divided by a negative is positive: " + MINUS + "6 ÷ " + MINUS + "3 = 2, so x > 2.", "Computes -6/-3 as -2: x>-2.")]),
    mc("Solve \\(2(x + 3) > 10\\). Which is the solution?",
       ["\\(x > 2\\)", "\\(x > 5\\)", "\\(x > 3.5\\)", "\\(x > 4\\)"], [0],
       "Expand the bracket first, then solve.",
       [m("arithmetic", 1, "After x + 3 > 5 you still subtract 3: x > 2, not x > 5.", "Divides by 2 first then forgets to subtract 3: x>5."),
        m("arithmetic", 2, "Expanding gives 2x + 6, so subtract 6: 2x > 4 and x > 2.", "Only subtracts 3, not 6: 2x>7, x>3.5.")]),
    sv("List the integer values of \\(x\\) where \\(-3 \\leq x < 2\\). How many?", 5,
       "List every whole number from minus 3 up to but not including 2, then count.",
       [m("strict_vs_nonstrict", 6, "x < 2 is strict, so 2 is not included. Count " + MINUS + "3, " + MINUS + "2, " + MINUS + "1, 0, 1, which is 5.", "Includes 2: counts 6."),
        m("arithmetic", 2, "Do not skip the negatives. " + MINUS + "3, " + MINUS + "2, " + MINUS + "1 all count, giving " + MINUS + "3, " + MINUS + "2, " + MINUS + "1, 0, 1, which is 5.", "Counts only 0,1: gives 2.")],
       [{"say": "You want every whole number from " + MINUS + "3 up to, but not including, 2."},
        {"pre": MINUS + "3 ≤ x means " + MINUS + "3 is allowed, so the smallest integer is ", "post": "", "answer": -3, "hint": "≤ keeps the boundary in."},
        {"pre": "x < 2 is strict, so the largest integer allowed is ", "post": "", "answer": 1, "hint": "The whole number just below 2.", "phase": "substitute"},
        {"pre": "Count the integers from " + MINUS + "3 to 1: ", "post": "", "answer": 5, "hint": "Count " + MINUS + "3, " + MINUS + "2, " + MINUS + "1, 0, 1.", "done": "Five integers. The traps are dropping the negatives or including 2.", "phase": "substitute"}]),
    mc("Solve \\(3x + 5 \\leq 2x + 9\\). Which is the solution?",
       ["\\(x \\leq 4\\)", "\\(x \\geq 4\\)", "\\(x \\leq 14\\)", "\\(x < 4\\)"], [0],
       "Subtract 2x from both sides, then subtract 5.",
       [m("wrong_direction", 1, "The boundary 4 is right, but the arrow is reversed. No negative was divided, so the symbol stays.", "Reverses to x>=4."),
        m("arithmetic", 2, "Move the 2x across: 3x " + MINUS + " 2x = x, and 9 " + MINUS + " 5 = 4, so x ≤ 4.", "Adds constants: 5+9=14."),
        m("strict_vs_nonstrict", 3, "The question uses ≤, so 4 is included. x < 4 wrongly leaves 4 out.", "Uses < instead of <=.")]),
    mc("Solve \\(4 - x > 2x - 5\\). Which is the solution?",
       ["\\(x < 3\\)", "\\(x > 3\\)", "\\(x < -3\\)", "\\(x > -3\\)"], [0],
       "Add x to both sides and add 5, then divide by 3.",
       [m("wrong_direction", 1, "Gathering the terms gives 9 > 3x, which means 3x < 9, so x < 3. The arrow points the other way.", "Keeps x>3.")]),
    sv("Solve \\(-1 < 2x + 3 \\leq 9\\). Give the largest integer value of \\(x\\).", 3,
       "Subtract 3 from all three parts, divide by 2, then take the largest integer allowed.",
       [m("strict_vs_nonstrict", 2, "The right symbol is ≤, so x = 3 is allowed. The largest integer is 3, not 2.", "Treats <= as <: gives 2."),
        m("arithmetic", 6, "Divide by 2: 2x ≤ 6 gives x ≤ 3, not x ≤ 6.", "Forgets to divide the x by 2: reads x<=6.")],
       [{"say": "First get x on its own. Subtract 3 from each part of \\(-1 < 2x + 3 \\leq 9\\)."},
        {"pre": "Left part: " + MINUS + "1 " + MINUS + " 3 = ", "post": "", "answer": -4, "hint": "Subtract 3 from " + MINUS + "1."},
        {"pre": "Right part: 9 " + MINUS + " 3 = ", "post": "", "answer": 6, "hint": "Subtract 3 from 9."},
        {"say": "So \\(-4 < 2x \\leq 6\\). Divide all three parts by 2."},
        {"pre": "Right part: 6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Divide 6 by 2.", "phase": "substitute"},
        {"pre": "So x ≤ 3. The largest integer x can be is ", "post": "", "answer": 3, "hint": "≤ 3 means 3 is allowed.", "done": "The largest is 3, because ≤ keeps the boundary in.", "phase": "substitute"}]),
]

# ---------------- GOLD ----------------
gold = [
    mc("Solve \\(\\frac{x+1}{3} > 2\\). Which is the solution?",
       ["\\(x > 5\\)", "\\(x > 7\\)", "\\(x > 1\\)", "\\(x < 5\\)"], [0],
       "Multiply both sides by 3, then subtract 1.",
       [m("arithmetic", 1, "After x + 1 > 6, subtract 1: x > 5, not x > 7.", "Adds 1: x>7."),
        m("arithmetic", 2, "Multiply both sides by 3 first: x + 1 > 6, then x > 5.", "Forgets to multiply by 3: x+1>2, x>1."),
        m("wrong_direction", 3, "The boundary 5 is right, but the arrow points the wrong way.", "Reverses to x<5.")]),
    mc("Solve \\(3(1-x) \\geq 2(x+4)\\). Which is the solution?",
       ["\\(x \\leq -1\\)", "\\(x \\geq -1\\)", "\\(x \\leq 1\\)", "\\(x \\geq 1\\)"], [0],
       "Expand both brackets, gather the x terms, then divide.",
       [m("wrong_direction", 1, MINUS + "5 ≥ 5x means 5x ≤ " + MINUS + "5, so x ≤ " + MINUS + "1. The arrow points the other way.", "Keeps x>=-1."),
        m("arithmetic", 2, "3 " + MINUS + " 8 = " + MINUS + "5, so 5x ≤ " + MINUS + "5 and x ≤ " + MINUS + "1, a negative.", "Drops the minus: x<=1.")]),
    sv("Find the integer values of \\(n\\) that satisfy \\(n^2 \\leq 16\\). How many?", 9,
       "Include negative whole numbers, because squaring removes the minus sign.",
       [m("positive_only", 5, "n can be negative: (" + MINUS + "4)² = 16 ≤ 16. Count " + MINUS + "4 to 4, which is 9.", "Counts only 0..4: gives 5."),
        m("strict_vs_nonstrict", 7, "16 ≤ 16 is true, so ±4 both count. That gives 9 integers.", "Excludes +/-4: counts 7.")],
       [{"say": "\\(n^2 \\leq 16\\) asks which whole numbers, squared, stay at 16 or below."},
        {"pre": "The largest n that works: 4² = 16, which is ≤ 16, so the largest is ", "post": "", "answer": 4, "hint": "4 squared is 16."},
        {"say": "Negatives work too, because squaring cancels the minus: \\((-4)^2 = 16\\)."},
        {"pre": "The smallest (most negative) n that fits is ", "post": "", "answer": -4, "hint": "(" + MINUS + "4)² = 16 ≤ 16.", "phase": "substitute"},
        {"pre": "Count every integer from " + MINUS + "4 to 4 inclusive: ", "post": "", "answer": 9, "hint": "Count " + MINUS + "4, " + MINUS + "3, " + MINUS + "2, " + MINUS + "1, 0, 1, 2, 3, 4.", "done": "Nine integers. The trap is forgetting the negatives.", "phase": "substitute"}]),
    sv("Solve \\(2x + 1 < 3\\) AND \\(x + 5 > 3\\). How many integers satisfy both?", 2,
       "Solve each inequality, then count the whole numbers that satisfy both at once.",
       [m("strict_vs_nonstrict", 4, "Both symbols are strict, so " + MINUS + "2 and 1 are excluded. Only " + MINUS + "1 and 0 fit, which is 2.", "Includes both ends: counts 4."),
        m("arithmetic", 1, MINUS + "1 is greater than " + MINUS + "2, so it counts: " + MINUS + "1 and 0 give 2.", "Drops -1: counts only 0.")],
       [{"say": "Solve each inequality on its own, then find the whole numbers that fit both."},
        {"pre": "2x + 1 < 3: subtract 1, then divide by 2 to get x < ", "post": "", "answer": 1, "hint": "2x < 2, so x < 1."},
        {"pre": "x + 5 > 3: subtract 5 to get x > ", "post": "", "answer": -2, "hint": "3 " + MINUS + " 5 = " + MINUS + "2."},
        {"say": "So x is between " + MINUS + "2 and 1, and both ends are strict, so neither is included."},
        {"pre": "The smallest integer greater than " + MINUS + "2 is ", "post": "", "answer": -1, "hint": MINUS + "2 is excluded, so start at " + MINUS + "1.", "phase": "substitute"},
        {"pre": "Count the integers from " + MINUS + "1 up to 0 (1 is excluded): ", "post": "", "answer": 2, "hint": "Count " + MINUS + "1 and 0.", "done": "Two integers. Both ends are open, so " + MINUS + "2 and 1 are out.", "phase": "substitute"}]),
    mc("Solve \\(\\frac{x}{2} + 1 > 4\\). Which is the solution?",
       ["\\(x > 6\\)", "\\(x > 10\\)", "\\(x > 3\\)", "\\(x < 6\\)"], [0],
       "Subtract 1, then multiply both sides by 2.",
       [m("arithmetic", 1, "Take 1 off both sides, do not add it: x/2 > 4 " + MINUS + " 1 = 3, so x > 6.", "Adds 1 then doubles: x>10."),
        m("arithmetic", 2, "After x/2 > 3, multiply by 2: x > 6, not x > 3.", "Forgets to multiply by 2: x>3."),
        m("wrong_direction", 3, "The boundary 6 is right, but the arrow points the wrong way.", "Reverses to x<6.")]),
]

pd["problem_bank"] = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "One-step and two-step inequalities",
    "silver_description": "Negatives requiring a sign flip, and double inequalities",
    "gold_description": "Fractional and bracketed inequalities, integer solutions, combined inequalities",
}

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one and two step inequalities",
        "steps": [
            "Solve an inequality just like an equation. Undo the <strong>+</strong> or <strong>−</strong> first, then the <strong>×</strong> or <strong>÷</strong>.",
            "Do the same thing to both sides, and keep the same symbol the whole way through.",
            "Your answer is a range, like \\(x > 3\\): every number bigger than 3, not a single value."
        ],
        "example": {
            "question": "Solve \\(2x + 1 < 9\\)",
            "steps": [
                {"label": "Subtract 1", "content": "\\(2x < 8\\)"},
                {"label": "Divide by 2", "content": "\\(x < 4\\)"},
                {"label": "Check", "content": "Try \\(x = 3\\): \\(2(3)+1 = 7 < 9\\), so 3 fits."},
                {"label": "Answer", "content": "\\(x < 4\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: negatives and double inequalities",
        "steps": [
            "If you divide or multiply by a <strong>negative</strong>, flip the sign, so \\(<\\) becomes \\(>\\).",
            "For a double inequality like \\(1 < 2x \\leq 8\\), do the same step to all three parts.",
            "A strict symbol (\\(<\\)) leaves the boundary out; \\(\\leq\\) keeps it in."
        ],
        "example": {
            "question": "Solve \\(5 - 2x \\geq 1\\)",
            "steps": [
                {"label": "Subtract 5", "content": "\\(-2x \\geq -4\\)"},
                {"label": "Divide by −2 and flip", "content": "\\(x \\leq 2\\)"},
                {"label": "Check", "content": "Try \\(x = 2\\): \\(5 - 2(2) = 1 \\geq 1\\), so 2 fits."},
                {"label": "Answer", "content": "\\(x \\leq 2\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: integer solutions and combined inequalities",
        "steps": [
            "Rearrange to a range first, then <strong>list every integer</strong> inside it, negatives included.",
            "Watch each end: a strict symbol excludes the boundary, \\(\\leq\\) or \\(\\geq\\) includes it.",
            "For two separate inequalities, solve each, then combine them into one overlapping range."
        ],
        "example": {
            "question": "List the integers satisfying \\(-2 \\leq 3x - 1 < 11\\)",
            "steps": [
                {"label": "Add 1 to all parts", "content": "\\(-1 \\leq 3x < 12\\)"},
                {"label": "Divide by 3", "content": "\\(-\\tfrac{1}{3} \\leq x < 4\\)"},
                {"label": "Check ends", "content": "0 is the first integer above \\(-\\tfrac13\\); 4 is excluded, so 3 is the last."},
                {"label": "Answer", "content": "0, 1, 2, 3", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- guided ----------------
pd["guided"] = {
    "opener": {
        "steps": [
            {"say": "A puzzle first, no algebra needed. A £20 hoodie: you have £8 saved and add £4 every week."},
            {"pre": "Fewest whole weeks until you can afford it? ", "post": "weeks", "answer": 3, "hint": "You need £12 more and save £4 each week."},
            {"say": "3 weeks works, and so do 4, 5, and up. The answer is a whole <strong>range</strong>, 3 or more, not one number. Writing your savings as \\(8 + 4w\\), you found where \\(8 + 4w \\geq 20\\). That is an <strong>inequality</strong>: solve it like an equation, but the answer is a range."},
            {"pre": "Check the boundary: after exactly 3 weeks, how much have you saved, in £? ", "post": "", "answer": 20, "hint": "Start at £8 and add £4 three times."},
            {"say": "£20, exactly enough. That boundary is where \\(8 + 4w = 20\\), and the inequality says 3 weeks or more. One warning for later: if you ever divide by a negative, the inequality sign flips over."}
        ]
    },
    "teach": {
        "bronze": {
            "display": "Solve \\(4x + 3 < 19\\)",
            "steps": [
                {"say": "Solve \\(4x + 3 < 19\\) the same way you solve an equation. First take 3 off both sides."},
                {"pre": "19 " + MINUS + " 3 = ", "post": "", "answer": 16, "hint": "Subtract 3 from the right-hand side."},
                {"say": "So \\(4x < 16\\). Now divide both sides by 4."},
                {"pre": "16 ÷ 4 = ", "post": "", "answer": 4, "hint": "Divide the right-hand side by 4."},
                {"say": "So \\(x < 4\\): every number less than 4. Keep the same symbol, \\(<\\), because we did not divide by a negative."},
                {"pre": "Test x = 3: 4 × 3 + 3 = ", "post": "", "answer": 15, "hint": "Work out 4 × 3 + 3.", "done": "15 is less than 19, so x = 3 fits."},
                {"pre": "Test the boundary x = 4: 4 × 4 + 3 = ", "post": "", "answer": 19, "hint": "Work out 4 × 4 + 3.", "done": "19 is not less than 19, so 4 is NOT included. That is why its circle is open."}
            ]
        },
        "silver": {
            "display": "Solve \\(3 - 2x \\leq 9\\)",
            "steps": [
                {"say": "Solve \\(3 - 2x \\leq 9\\). Take 3 off both sides first."},
                {"pre": "9 " + MINUS + " 3 = ", "post": "", "answer": 6, "hint": "Subtract 3 from the right."},
                {"say": "So \\(-2x \\leq 6\\). Now divide by −2. Because we divide by a NEGATIVE, the sign flips: \\(\\leq\\) becomes \\(\\geq\\)."},
                {"pre": "6 ÷ (−2) = ", "post": "", "answer": -3, "hint": "A positive divided by a negative is negative."},
                {"say": "So \\(x \\geq -3\\). The flip is the whole point: dividing by a negative reverses the arrow."},
                {"pre": "Test x = 0 (more than −3): 3 " + MINUS + " 2 × 0 = ", "post": "", "answer": 3, "hint": "2 × 0 is 0.", "done": "3 is less than 9, so x = 0 fits, matching x ≥ −3."},
                {"pre": "Test x = −4 (less than −3): 3 " + MINUS + " 2 × (−4) = ", "post": "", "answer": 11, "hint": "−2 × −4 = +8, then add 3.", "done": "11 is not ≤ 9, so −4 fails. The arrow really does point the other way."}
            ]
        },
        "gold": {
            "display": "How many integers satisfy \\(-2 \\leq 3x + 4 < 13\\)?",
            "steps": [
                {"say": "How many integers satisfy \\(-2 \\leq 3x + 4 < 13\\)? Do the same step to all three parts. First subtract 4 from each part."},
                {"pre": "Left part: " + MINUS + "2 " + MINUS + " 4 = ", "post": "", "answer": -6, "hint": "Subtract 4 from " + MINUS + "2."},
                {"pre": "Right part: 13 " + MINUS + " 4 = ", "post": "", "answer": 9, "hint": "Subtract 4 from 13."},
                {"say": "So \\(-6 \\leq 3x < 9\\). Divide all three parts by 3."},
                {"pre": MINUS + "6 ÷ 3 = ", "post": "", "answer": -2, "hint": "Divide " + MINUS + "6 by 3."},
                {"pre": "9 ÷ 3 = ", "post": "", "answer": 3, "hint": "Divide 9 by 3."},
                {"say": "So \\(-2 \\leq x < 3\\). List the integers, negatives included. −2 is in (\\(\\leq\\)), 3 is out (\\(<\\))."},
                {"pre": "Count −2, −1, 0, 1, 2: ", "post": "", "answer": 5, "hint": "Count −2, −1, 0, 1, 2.", "done": "Five integers. The trap is forgetting −2 and −1."}
            ]
        }
    }
}

# Preserve remaining live fields byte-for-byte
pd["related_videos"] = live["related_videos"]
pd["worked_examples"] = live["worked_examples"]

with io.open("lesson_maths-eduqas_algebra-L11.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("written lesson_maths-eduqas_algebra-L11.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
