# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_number_L01.json", encoding="utf-8"))

def box(pre, answer, hint, post="", done=None, say=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

def mc(pattern, expect, message, note=None):
    m = {"pattern": pattern, "check": pattern, "expect": expect, "message": message}
    if note: m["note"] = note
    return m

# ---------------- METHOD CARD (slim) ----------------
method_card = {
    "title": "How to Use BIDMAS (Order of Operations)",
    "steps": [
        "Brackets first (innermost pair outward).",
        "Then Indices: powers and roots.",
        "Then Division and Multiplication, left to right.",
        "Then Addition and Subtraction, left to right.",
    ],
    "content": ("<p><strong>BIDMAS</strong> gives the order for a calculation: "
                "<strong>B</strong>rackets, <strong>I</strong>ndices, "
                "<strong>D</strong>ivision and <strong>M</strong>ultiplication, "
                "<strong>A</strong>ddition and <strong>S</strong>ubtraction.</p>"
                "<p>Division and multiplication share a tier, so work them left to right; "
                "the same goes for addition and subtraction. A fraction bar groups its "
                "whole top and bottom like brackets.</p>"),
    "example": ("<p><strong>Calculate</strong> \\(3 + 4 \\times 2^2 - (6 \\div 3)\\)</p>"
                "<p>Bracket: \\(6 \\div 3 = 2\\). Index: \\(2^2 = 4\\). Multiply: "
                "\\(4 \\times 4 = 16\\). Then \\(3 + 16 - 2 = 17\\).</p>"),
}

# ---------------- TIER GUIDES ----------------
tier_guides = {
    "bronze": {
        "title": "Bronze: one operation outranks the other",
        "steps": [
            "<strong>BIDMAS</strong> sets the order: Brackets, Indices, Division and Multiplication, then Addition and Subtraction.",
            "At Bronze, each calculation mixes a times or divide with an add or subtract. Always do the times or divide first.",
            "When two operations share a tier (both + and −, or both × and ÷), just work left to right.",
        ],
        "example": {
            "question": "Work out 20 ÷ 5 + 6",
            "steps": [
                {"label": "Divide first", "content": "20 ÷ 5 = 4"},
                {"label": "Then add", "content": "4 + 6 = 10"},
                {"label": "Check", "content": "10 − 6 = 4, which is 20 ÷ 5"},
                {"label": "Answer", "content": "10", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: powers and brackets step in",
        "steps": [
            "Now calculations include indices (powers like \\(2^3\\)) and brackets.",
            "Do everything inside brackets first, then indices, before any times, divide, add or subtract.",
            "Inside a bracket, BIDMAS still applies, so sort out any power there before you add.",
        ],
        "example": {
            "question": "Work out 30 − 2 × 3²",
            "steps": [
                {"label": "Index first", "content": "3² = 9"},
                {"label": "Multiply", "content": "2 × 9 = 18"},
                {"label": "Subtract", "content": "30 − 18 = 12"},
                {"label": "Check", "content": "12 + 18 = 30"},
                {"label": "Answer", "content": "12", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: fractions, roots and nested brackets",
        "steps": [
            "A fraction bar groups the whole top and the whole bottom, like invisible brackets around each.",
            "Work out the top and bottom fully, then divide. Roots such as \\(\\sqrt{49}\\) count as indices.",
            "For brackets inside brackets, start with the innermost pair and work outward.",
        ],
        "example": {
            "question": "Work out (7 + 9) ÷ 2³ + √9",
            "steps": [
                {"label": "Top and bottom", "content": "7 + 9 = 16 and 2³ = 8"},
                {"label": "Divide", "content": "16 ÷ 8 = 2"},
                {"label": "Root", "content": "√9 = 3"},
                {"label": "Add", "content": "2 + 3 = 5"},
                {"label": "Check", "content": "5 − 3 = 2, the fraction value"},
                {"label": "Answer", "content": "5", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------- GUIDED: opener + teach ----------------
opener = {
    "steps": [
        say("A lunch order, no maths rules needed, just common sense. You buy 1 sandwich for £3 and 2 juices at £2 each."),
        box("Total cost, in £: £", 7, "The two juices come to £4. Add on the £3 sandwich."),
        say("Notice what you did: you worked out the two juices (2 × £2 = £4) BEFORE adding the sandwich. You did the multiplication first without being told. That is the whole rule: <strong>multiplication before addition</strong>. As maths it is \\(3 + 2 \\times 2\\), and the answer is 7, not 10."),
        box("Now change from a £20 note after buying 3 sandwiches at £3 each, in £: £", 11, "Three sandwiches cost £9. Take that off £20."),
        say("Again you multiplied first (3 sandwiches = £9) then subtracted, giving £11. That is <strong>BIDMAS</strong>: Brackets, Indices, Division and Multiplication, then Addition and Subtraction. The steps ahead just apply this rule to bigger calculations."),
    ]
}

teach = {
    "bronze": {
        "display": "Work out \\(5 + 6 \\times 3 - 4\\)",
        "steps": [
            say("No brackets or indices here. Multiplication comes before add and subtract, so do 6 × 3 first."),
            box("6 × 3 = ", 18, "Just the multiplication."),
            say("Now add and subtract, left to right: 5 + 18, then take off 4."),
            box("5 + 18 = ", 23, "Add first, working left to right."),
            box("23 − 4 = ", 19, "Now subtract the 4."),
            box("Check: 19 + 4 − 18 = ", 5, "Undo the steps: add the 4, take off 18.",
                done="That rebuilds the 5 you started with. Multiply-first was the whole point."),
        ],
    },
    "silver": {
        "display": "Work out \\(40 - 3 \\times 2^3\\)",
        "steps": [
            say("Now a power appears. Indices come before multiplication, so work out 2³ first."),
            box("2³ = ", 8, "2 × 2 × 2."),
            say("Now multiply before subtracting: 3 × 8."),
            box("3 × 8 = ", 24, "Multiply."),
            say("Now the subtraction: 40 − 24."),
            box("40 − 24 = ", 16, "Subtract."),
            box("Check: 16 + 24 = ", 40, "Add the 24 back on.",
                done="That rebuilds the 40. Doing the index first was the whole point."),
        ],
    },
    "gold": {
        "display": "Work out \\(\\dfrac{18 + 6}{2^3} + \\sqrt{16}\\)",
        "steps": [
            say("The fraction bar groups the whole top and the whole bottom. Work out the top: 18 + 6."),
            box("18 + 6 = ", 24, "Top of the fraction."),
            say("Now the bottom: 2³."),
            box("2³ = ", 8, "2 × 2 × 2."),
            say("Divide top by bottom: 24 ÷ 8."),
            box("24 ÷ 8 = ", 3, "Divide."),
            say("Now the root: √16."),
            box("√16 = ", 4, "What number times itself is 16?"),
            say("Now add the two parts: 3 + 4."),
            box("3 + 4 = ", 7, "Add."),
            box("Check: 7 − 4 = ", 3, "Take the root back off.",
                done="That is the fraction value 24 ÷ 8. Treating the bar as brackets was the whole point."),
        ],
    },
}

guided = {"opener": opener, "teach": teach}

# ---------------- PROBLEM BANK ----------------
pb = live["problem_bank"]

# ---- BRONZE ----
bronze = [
    {  # B0 3+5x2=13
        "display": "\\(3 + 5 \\times 2\\)", "solutions": [13], "calculator": False, "input_type": "single_value",
        "hint": "Multiply before you add: do 5 × 2 first.",
        "misconceptions": [mc("left_to_right", 16, "You worked left to right instead of following BIDMAS. Do 5 × 2 before adding.", "(3+5)x2=16")],
        "guided_steps": [
            say("There are no brackets or indices. Multiplication outranks addition, so do 5 × 2 before the add."),
            box("5 × 2 = ", 10, "Just the multiplication for now."),
            box("3 + 10 = ", 13, "Add the two numbers.", phase="substitute", say="The calculation is now 3 + 10. Only the add is left."),
            box("Check by working backwards: 13 − 3 = ", 10, "Take the 3 back off.", done="That is exactly 5 × 2, so 13 is right.", phase="substitute"),
        ],
    },
    {  # B1 12-4x2=4
        "display": "\\(12 - 4 \\times 2\\)", "solutions": [4], "calculator": False, "input_type": "single_value",
        "hint": "Multiply before you subtract: do 4 × 2 first.",
        "misconceptions": [mc("left_to_right", 16, "You subtracted first then multiplied. Do 4 × 2 before subtracting.", "(12-4)x2=16")],
        "guided_steps": [
            say("No brackets or indices. Multiplication comes before subtraction, so do 4 × 2 first."),
            box("4 × 2 = ", 8, "Just the multiplication."),
            box("12 − 8 = ", 4, "Subtract.", phase="substitute", say="Now the calculation is 12 − 8."),
            box("Check: 4 + 8 = ", 12, "Add your answer back to the 8.", done="That rebuilds the original 12, so 4 is right.", phase="substitute"),
        ],
    },
    {  # B2 6x3+2=20
        "display": "\\(6 \\times 3 + 2\\)", "solutions": [20], "calculator": False, "input_type": "single_value",
        "hint": "Multiply before you add: do 6 × 3 first.",
        "misconceptions": [mc("add_first", 30, "You added first. Multiplication takes priority, so do 6 × 3 before adding 2.", "6x(3+2)=30")],
        "guided_steps": [
            say("Multiplication first: 6 × 3, then the add."),
            box("6 × 3 = ", 18, "Just the multiplication."),
            box("18 + 2 = ", 20, "Add.", phase="substitute", say="Now it is 18 + 2."),
            box("Check: 20 − 2 = ", 18, "Take the 2 back off.", done="That is 6 × 3, so 20 is right.", phase="substitute"),
        ],
    },
    {  # B3 15/3+7=12
        "display": "\\(15 \\div 3 + 7\\)", "solutions": [12], "calculator": False, "input_type": "single_value",
        "hint": "Divide before you add: do 15 ÷ 3 first.",
        "misconceptions": [mc("add_first", 1.5, "You added before dividing. BIDMAS says divide first: 15 ÷ 3 = 5.", "15/(3+7)=1.5")],
        "guided_steps": [
            say("Division outranks addition, so do 15 ÷ 3 first."),
            box("15 ÷ 3 = ", 5, "Just the division."),
            box("5 + 7 = ", 12, "Add.", phase="substitute", say="Now it is 5 + 7."),
            box("Check: 12 − 7 = ", 5, "Take the 7 back off.", done="That is 15 ÷ 3, so 12 is right.", phase="substitute"),
        ],
    },
    {  # B4 4+8/2=8
        "display": "\\(4 + 8 \\div 2\\)", "solutions": [8], "calculator": False, "input_type": "single_value",
        "hint": "Divide before you add: do 8 ÷ 2 first.",
        "misconceptions": [mc("left_to_right", 6, "You added first. Division has higher priority, so do 8 ÷ 2 before adding.", "(4+8)/2=6")],
        "guided_steps": [
            say("Division comes before addition, so do 8 ÷ 2 first."),
            box("8 ÷ 2 = ", 4, "Just the division."),
            box("4 + 4 = ", 8, "Add.", phase="substitute", say="Now it is 4 + 4."),
            box("Check: 8 − 4 = ", 4, "Take the first 4 back off.", done="That is 8 ÷ 2, so 8 is right.", phase="substitute"),
        ],
    },
    {  # B5 (replaced) 10-2x3+1=5
        "display": "\\(10 - 2 \\times 3 + 1\\)", "solutions": [5], "calculator": False, "input_type": "single_value",
        "hint": "Multiply first (2 × 3), then work left to right through the subtract and add.",
        "misconceptions": [
            mc("subtract_sum", 3, "Subtraction and addition are equal priority, so go left to right: do 10 − 6 before adding the 1, not 6 + 1 first.", "10-(6+1)=3"),
            mc("left_to_right", 25, "Do the multiplication 2 × 3 before the subtraction, not left to right from the start.", "((10-2)x3)+1=25"),
        ],
        "guided_steps": [
            say("Multiplication first: 2 × 3. Then the subtraction and addition are equal priority, so go left to right."),
            box("2 × 3 = ", 6, "Just the multiplication."),
            box("10 − 6 = ", 4, "Subtract before you add, working left to right.", phase="substitute", say="Now it is 10 − 6 + 1. Left to right, so subtract first."),
            box("4 + 1 = ", 5, "Now add the 1.", phase="substitute"),
            box("Check: 5 − 1 + 6 = ", 10, "Undo the steps: add the 6, take off the 1.", done="That rebuilds the 10 you started with, so 5 is right.", phase="substitute"),
        ],
    },
    {  # B6 2x3x4=24
        "display": "\\(2 \\times 3 \\times 4\\)", "solutions": [24], "calculator": False, "input_type": "single_value",
        "hint": "Only multiplication here, so work left to right.",
        "misconceptions": [mc("addition_confusion", 9, "You added instead of multiplying. The × symbol means multiply.", "2+3+4=9")],
        "guided_steps": [
            say("Every operation here is multiplication, equal priority, so just work left to right."),
            box("2 × 3 = ", 6, "Start from the left."),
            box("6 × 4 = ", 24, "Multiply by the 4.", phase="substitute", say="Now multiply that result by 4."),
            box("Check: 24 ÷ 4 = ", 6, "Divide by the last factor.", done="That is 2 × 3, so 24 is right.", phase="substitute"),
        ],
    },
    {  # B7 20/4+6=11
        "display": "\\(20 \\div 4 + 6\\)", "solutions": [11], "calculator": False, "input_type": "single_value",
        "hint": "Divide before you add: do 20 ÷ 4 first.",
        "misconceptions": [mc("add_first", 2, "You added 4 + 6 first. BIDMAS says divide before adding: 20 ÷ 4 = 5.", "20/(4+6)=2")],
        "guided_steps": [
            say("Division comes before addition, so do 20 ÷ 4 first."),
            box("20 ÷ 4 = ", 5, "Just the division."),
            box("5 + 6 = ", 11, "Add.", phase="substitute", say="Now it is 5 + 6."),
            box("Check: 11 − 6 = ", 5, "Take the 6 back off.", done="That is 20 ÷ 4, so 11 is right.", phase="substitute"),
        ],
    },
]

# ---- SILVER ----
silver = [
    {  # S0 3+2^3x2=19
        "display": "\\(3 + 2^3 \\times 2\\)", "solutions": [19], "calculator": False, "input_type": "single_value",
        "hint": "Indices first (2³ = 8), then multiply, then add.",
        "misconceptions": [
            mc("no_index", 7, "Did you forget the index? Work out 2³ = 8 first, then multiply by 2.", "treats 2^3 as 2: 3+2x2=7"),
            mc("add_first", 250, "Do the index and multiplication before the addition, not 3 + 2 first.", "(3+2)^3x2=250"),
        ],
        "guided_steps": [
            say("Indices come before multiplication. Work out 2³ first."),
            box("2³ = ", 8, "2 × 2 × 2."),
            box("8 × 2 = ", 16, "Multiply the power result by 2."),
            box("3 + 16 = ", 19, "Add.", phase="substitute", say="Now just the addition: 3 + 16."),
            box("Check: 19 − 3 = ", 16, "Take the 3 back off.", done="That is 2³ × 2, so 19 is right.", phase="substitute"),
        ],
    },
    {  # S1 18/6x3=9
        "display": "\\(18 \\div 6 \\times 3\\)", "solutions": [9], "calculator": False, "input_type": "single_value",
        "hint": "Divide and multiply are equal priority, so work left to right.",
        "misconceptions": [mc("multiply_first", 1, "Division and multiplication have equal priority, so go left to right. Do not multiply 6 × 3 first.", "18/(6x3)=1")],
        "guided_steps": [
            say("Divide and multiply are equal priority, so work left to right. Divide first."),
            box("18 ÷ 6 = ", 3, "Left operation first."),
            box("3 × 3 = ", 9, "Multiply.", phase="substitute", say="Now multiply: 3 × 3."),
            box("Check: 9 ÷ 3 = ", 3, "Divide by the 3 you multiplied by.", done="That is 18 ÷ 6, so 9 is right.", phase="substitute"),
        ],
    },
    {  # S2 (5+3)x4-10=22 ; audit fix expect 7
        "display": "\\((5 + 3) \\times 4 - 10\\)", "solutions": [22], "calculator": False, "input_type": "single_value",
        "hint": "Brackets first (5 + 3), then multiply, then subtract.",
        "misconceptions": [mc("ignore_bracket", 7, "Do the brackets first: work out 5 + 3 before anything else.", "ignoring bracket: 5+3x4-10=7")],
        "guided_steps": [
            say("Brackets first: work out 5 + 3."),
            box("5 + 3 = ", 8, "Just inside the brackets."),
            box("8 × 4 = ", 32, "Multiply the bracket result by 4."),
            box("32 − 10 = ", 22, "Subtract.", phase="substitute", say="Now the subtraction: 32 − 10."),
            box("Check: 22 + 10 = ", 32, "Add the 10 back on.", done="That is 8 × 4, so 22 is right.", phase="substitute"),
        ],
    },
    {  # S3 50-3x(4+2^2)=26
        "display": "\\(50 - 3 \\times (4 + 2^2)\\)", "solutions": [26], "calculator": False, "input_type": "single_value",
        "hint": "Inside the bracket do the index first (2² = 4), then finish the bracket, then multiply, then subtract.",
        "misconceptions": [
            mc("index_outside_bracket", -58, "The 2² is inside the bracket, so square first: 2² = 4, then 4 + 4 = 8.", "(4+2)^2=36: 50-3x36=-58"),
            mc("subtract_first", 376, "Multiply before subtracting: do 3 × 8 before taking anything from 50.", "(50-3)x8=376"),
        ],
        "guided_steps": [
            say("Brackets first, and inside the bracket indices come before adding. Work out 2² first."),
            box("2² = ", 4, "2 × 2."),
            box("4 + 4 = ", 8, "Add inside the bracket."),
            box("3 × 8 = ", 24, "Multiply the 3 by the bracket."),
            box("50 − 24 = ", 26, "Subtract.", phase="substitute", say="Now the subtraction: 50 − 24."),
            box("Check: 26 + 24 = ", 50, "Add the 24 back on.", done="That rebuilds the 50, so 26 is right.", phase="substitute"),
        ],
    },
    {  # S4 4^2-2x5=6
        "display": "\\(4^2 - 2 \\times 5\\)", "solutions": [6], "calculator": False, "input_type": "single_value",
        "hint": "Index first (4² = 16), then multiply, then subtract.",
        "misconceptions": [
            mc("subtract_first", 70, "Do 4² = 16 and 2 × 5 = 10 first, then subtract. Do not subtract before multiplying.", "(16-2)x5=70"),
            mc("index_error", -2, "4² means 4 × 4 = 16, not 4 × 2 = 8.", "4^2=8: 8-10=-2"),
        ],
        "guided_steps": [
            say("Indices first: work out 4²."),
            box("4² = ", 16, "4 × 4."),
            box("2 × 5 = ", 10, "Multiply."),
            box("16 − 10 = ", 6, "Subtract.", phase="substitute", say="Now subtract: 16 − 10."),
            box("Check: 6 + 10 = ", 16, "Add the 10 back on.", done="That is 4², so 6 is right.", phase="substitute"),
        ],
    },
    {  # S5 100/(2+3)x2=40
        "display": "\\(100 \\div (2 + 3) \\times 2\\)", "solutions": [40], "calculator": False, "input_type": "single_value",
        "hint": "Bracket first (2 + 3), then divide and multiply left to right.",
        "misconceptions": [
            mc("ignore_bracket", 56, "Do the bracket first: 2 + 3 = 5, then 100 ÷ 5 = 20.", "100/2+3x2=56"),
            mc("multiply_before_divide", 10, "After the bracket, work left to right: divide before you multiply.", "100/(5x2)=10"),
        ],
        "guided_steps": [
            say("Brackets first: work out 2 + 3."),
            box("2 + 3 = ", 5, "Just inside the brackets."),
            box("100 ÷ 5 = ", 20, "Divide by the bracket result."),
            box("20 × 2 = ", 40, "Multiply.", phase="substitute", say="Now multiply: 20 × 2."),
            box("Check: 40 ÷ 2 = ", 20, "Divide by the last 2.", done="That is 100 ÷ 5, so 40 is right.", phase="substitute"),
        ],
    },
    {  # S6 7+3x5-2^2=18
        "display": "\\(7 + 3 \\times 5 - 2^2\\)", "solutions": [18], "calculator": False, "input_type": "single_value",
        "hint": "Index first (2² = 4), then multiply, then add and subtract left to right.",
        "misconceptions": [mc("index_forgotten", 20, "Do not forget 2² = 4, not just 2.", "2^2 as 2: 7+15-2=20")],
        "guided_steps": [
            say("Indices first: work out 2²."),
            box("2² = ", 4, "2 × 2."),
            box("3 × 5 = ", 15, "Multiply."),
            box("7 + 15 = ", 22, "Add first, working left to right.", phase="substitute", say="Now add and subtract left to right: 7 + 15, then take off 4."),
            box("22 − 4 = ", 18, "Now subtract the 4.", phase="substitute"),
            box("Check: 18 + 4 − 15 = ", 7, "Undo: add the 4, take off 15.", done="That rebuilds the 7 you started with, so 18 is right.", phase="substitute"),
        ],
    },
]

# ---- GOLD ----
gold = [
    {  # G0 (12+8)/2^2 + 3x5 = 20
        "display": "\\(\\dfrac{12 + 8}{2^2} + 3 \\times 5\\)", "solutions": [20], "calculator": False, "input_type": "single_value",
        "hint": "Treat the fraction bar as brackets: work out the top and bottom separately, then divide.",
        "misconceptions": [
            mc("no_fraction_bracket", 29, "The fraction bar groups the whole top: work out 12 + 8 = 20 before dividing by 4.", "8/4=2 first: 12+2+15=29"),
            mc("index_error", 25, "2² = 4, not 2.", "denom 2^2=2: 20/2+15=25"),
            mc("add_before_multiply", 40, "After the fraction, multiply 3 × 5 before adding it on.", "(5+3)x5=40"),
        ],
        "guided_steps": [
            say("The fraction bar acts like brackets. Work out the top: 12 + 8."),
            box("12 + 8 = ", 20, "Top of the fraction."),
            box("2² = ", 4, "The bottom: 2 × 2."),
            box("20 ÷ 4 = ", 5, "Divide top by bottom."),
            box("3 × 5 = ", 15, "The other term: multiply before adding."),
            box("5 + 15 = ", 20, "Add the two parts.", phase="substitute", say="Now add the two parts: 5 + 15."),
            box("Check: 20 − 15 = ", 5, "Take the 15 back off.", done="That is the fraction value 20 ÷ 4, so 20 is right.", phase="substitute"),
        ],
    },
    {  # G1 (2+3)^2-4x(7-5)=17 ; audit fix square_wrong expect 5
        "display": "\\((2 + 3)^2 - 4 \\times (7 - 5)\\)", "solutions": [17], "calculator": False, "input_type": "single_value",
        "hint": "Both brackets first, then the index, then multiply, then subtract.",
        "misconceptions": [
            mc("index_before_bracket", -1, "Do the bracket 2 + 3 = 5 before squaring: 5² = 25, not 2² + 3.", "2^2+3=7 then 7-4x2=-1"),
            mc("square_wrong", 5, "(2 + 3)² means 5² = 25, not 2² + 3² = 13.", "(2+3)^2=13: 13-8=5"),
        ],
        "guided_steps": [
            say("Both brackets first: 2 + 3 and 7 − 5."),
            box("2 + 3 = ", 5, "First bracket."),
            box("7 − 5 = ", 2, "Second bracket."),
            box("5² = ", 25, "The index on the first bracket: 5 × 5."),
            box("4 × 2 = ", 8, "Multiply the 4 by the second bracket."),
            box("25 − 8 = ", 17, "Subtract.", phase="substitute", say="Now subtract: 25 − 8."),
            box("Check: 17 + 8 = ", 25, "Add the 8 back on.", done="That is 5², so 17 is right.", phase="substitute"),
        ],
    },
    {  # G2 6x8/4+5x(3-1)^2=32
        "display": "\\(6 \\times 8 \\div 4 + 5 \\times (3 - 1)^2\\)", "solutions": [32], "calculator": False, "input_type": "single_value",
        "hint": "Bracket then its index first, then multiply and divide left to right, then add.",
        "misconceptions": [mc("index_error", 22, "(3 − 1)² = 2² = 4, not just 2.", "(3-1)^2 as 2: 12+10=22")],
        "guided_steps": [
            say("Bracket first: 3 − 1."),
            box("3 − 1 = ", 2, "Inside the bracket."),
            box("2² = ", 4, "Its index: 2 × 2."),
            box("6 × 8 = ", 48, "The left part, left operation first."),
            box("48 ÷ 4 = ", 12, "Now divide by 4."),
            box("5 × 4 = ", 20, "The other multiplication: 5 times the bracket result."),
            box("12 + 20 = ", 32, "Add the two parts.", phase="substitute", say="Now add the two parts: 12 + 20."),
            box("Check: 32 − 20 = ", 12, "Take the 20 back off.", done="That is 6 × 8 ÷ 4, so 32 is right.", phase="substitute"),
        ],
    },
    {  # G3 2^4-(3x2+1)^0x10=6 ; audit fixes
        "display": "\\(2^4 - (3 \\times 2 + 1)^0 \\times 10\\)", "solutions": [6], "calculator": False, "input_type": "single_value",
        "hint": "Any non-zero number to the power 0 equals 1, so the bracket term becomes 1 × 10.",
        "misconceptions": [
            mc("zero_power", 16, "Anything to the power 0 equals 1, so 7⁰ = 1, not 0.", "x^0=0: 2^4-0x10=16"),
            mc("power_as_base", -54, "7⁰ is not 7. Any non-zero number to the power 0 equals 1.", "7^0=7: 16-70=-54"),
            mc("subtract_before_multiply", 150, "Do 1 × 10 before subtracting: 16 minus (1 × 10) = 6, not (16 minus 1) × 10 = 150.", "(16-1)x10=150"),
        ],
        "guided_steps": [
            say("Start with the powers and the bracket. First 2⁴."),
            box("2⁴ = ", 16, "2 × 2 × 2 × 2."),
            box("3 × 2 + 1 = ", 7, "Inside the bracket, multiply 3 × 2 first, then add 1."),
            box("1 × 10 = ", 10, "Anything to the power 0 is 1, so 7⁰ = 1. One times ten."),
            box("16 − 10 = ", 6, "Subtract.", phase="substitute", say="Now subtract: 16 − 10."),
            box("Check: 6 + 10 = ", 16, "Add the 10 back on.", done="That is 2⁴, so 6 is right.", phase="substitute"),
        ],
    },
    {  # G4 (5^2+sqrt49)/2^3=4
        "display": "\\(\\dfrac{5^2 + \\sqrt{49}}{2^3}\\)", "solutions": [4], "calculator": False, "input_type": "single_value",
        "hint": "Work out the whole top and the whole bottom separately, then divide.",
        "misconceptions": [
            mc("sqrt_error", 9.25, "√49 = 7, because 7 × 7 = 49, not 49.", "sqrt49=49: 74/8=9.25"),
            mc("fraction_order", 25.875, "Work out the whole top (25 + 7 = 32) and the whole bottom (8) before dividing.", "only sqrt/2^3: 25+7/8=25.875"),
        ],
        "guided_steps": [
            say("The fraction bar groups the top. Work out 5² first."),
            box("5² = ", 25, "5 × 5."),
            box("√49 = ", 7, "What number times itself is 49?"),
            box("25 + 7 = ", 32, "Finish the top."),
            box("2³ = ", 8, "The bottom: 2 × 2 × 2."),
            box("32 ÷ 8 = ", 4, "Divide top by bottom.", phase="substitute", say="Now divide top by bottom: 32 ÷ 8."),
            box("Check: 4 × 8 = ", 32, "Multiply back by the 8.", done="That is the top, 25 + 7, so 4 is right.", phase="substitute"),
        ],
    },
]

pb["bronze"] = bronze
pb["silver"] = silver
pb["gold"] = gold
pb["bronze_description"] = "One calculation mixing a times or divide with an add or subtract: do the times or divide first."
pb["silver_description"] = "Brackets and powers join in: sort out brackets first, then indices, before any times, divide, add or subtract."
pb["gold_description"] = "Fraction bars, roots and nested brackets: treat the top and bottom of a fraction as bracketed, then finish with the outer operations."

# worked_examples: preserve, but strip em dashes (hard style rule / validator gate).
# Labels like "Step 1 — Multiply" -> "Step 1: Multiply".
worked_examples = live["worked_examples"]
def strip_em(obj):
    if isinstance(obj, dict):
        return {k: strip_em(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_em(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ": ")
    return obj
worked_examples = strip_em(worked_examples)

# assemble; preserve related_videos, worked_examples, topic_links
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": pb,
    "tier_guides": tier_guides,
    "guided": guided,
    "related_videos": live["related_videos"],
    "worked_examples": worked_examples,
}

# ---------------- INTERNAL ARITHMETIC VERIFICATION ----------------
def num(s):
    # strip a box pre to its trailing arithmetic isn't parseable generally; we verify by explicit maps
    return None

# verify each bank walk's final math lands on stored solution and every box internally consistent
import re
def verify_walk(prob, label):
    sol = prob["solutions"][0]
    # collect box answers in order
    boxes = [st for st in prob["guided_steps"] if st.get("answer") is not None]
    # the last non-check box should equal the solution OR a check exists; ensure solution appears among boxes
    vals = [b["answer"] for b in boxes]
    assert sol in vals, f"{label}: solution {sol} not produced by any box {vals}"
    # check boundary
    subs = [i for i,st in enumerate(prob["guided_steps"]) if st.get("phase")=="substitute"]
    assert subs, f"{label}: no substitute phase"
    first_sub = subs[0]
    before = sum(1 for st in prob["guided_steps"][:first_sub] if st.get("answer") is not None)
    after = sum(1 for st in prob["guided_steps"][first_sub:] if st.get("answer") is not None)
    assert before >= 1, f"{label}: {before} boxes before boundary"
    assert after >= 2, f"{label}: only {after} live boxes after boundary"

for i,p in enumerate(bronze): verify_walk(p, f"bronze[{i}]")
for i,p in enumerate(silver): verify_walk(p, f"silver[{i}]")
for i,p in enumerate(gold): verify_walk(p, f"gold[{i}]")

# verify expects != solution
for tier,arr in (("bronze",bronze),("silver",silver),("gold",gold)):
    for i,p in enumerate(arr):
        for j,m in enumerate(p["misconceptions"]):
            e=m["expect"]
            if e is not None:
                assert abs(float(e)-float(p["solutions"][0]))>=0.011, f"{tier}[{i}].mc[{j}] expect==solution"

json.dump(out, io.open("lesson_number-L01.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("BUILD OK -> lesson_number-L01.json")
print("bronze sols", [p['solutions'] for p in bronze])
print("silver sols", [p['solutions'] for p in silver])
print("gold sols", [p['solutions'] for p in gold])
