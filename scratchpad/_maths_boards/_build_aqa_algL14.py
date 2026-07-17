# -*- coding: utf-8 -*-
"""Full guided conversion of algebra-L14 (Quadratic nth Term, Functions & Iteration), board maths-aqa."""
import json, io

MINUS = "−"   # proper minus sign
ARROW = "→"
DIV = "÷"
TIMES = "×"

live = json.load(io.open("_aqa_L14_live.json", encoding="utf-8"))
pd = live  # mutate in place, preserving untouched fields

# ---------------- opener SVG (growing square patterns 2, 6, 12) ----------------
def opener_svg():
    cell = 12
    baseline = 62
    groups = [(12, 1, 2), (78, 2, 3), (150, 3, 4)]  # (x_start, rows, cols)
    rects = []
    for (x0, rows, cols) in groups:
        for r in range(rows):
            for c in range(cols):
                x = x0 + c * cell
                y = baseline - (r + 1) * cell
                rects.append(
                    '<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>'
                    % (x, y, cell, cell))
    labels = [(24, "2"), (97, "6"), (176, "12")]
    txt = "".join(
        '<text x="%d" y="78" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle">%s</text>' % (x, s)
        for (x, s) in labels)
    return ('<svg viewBox="0 0 220 88" role="img" aria-label="Three growing square patterns holding 2, 6 and 12 squares">'
            + "".join(rects) + txt + "</svg>")

opener_display = (opener_svg()
                  + "<p>Three patterns made of squares: <strong>2</strong>, then <strong>6</strong>, then <strong>12</strong>. Just count how big each jump is.</p>")

pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_display,
        "steps": [
            {
                "say": "No algebra allowed. Look at the counts under the patterns: 2, 6, 12.",
                "pre": "From pattern 1 to pattern 2, how many extra squares? 6 " + MINUS + " 2 = ",
                "post": "",
                "answer": 4,
                "hint": "Six squares take away two."
            },
            {
                "pre": "From pattern 2 to pattern 3: 12 " + MINUS + " 6 = ",
                "post": "",
                "answer": 6,
                "hint": "Twelve take away six."
            },
            {
                "say": "The jumps were 4 then 6, so the jump itself is growing.",
                "pre": "How much did the jump grow by? 6 " + MINUS + " 4 = ",
                "post": "",
                "answer": 2,
                "done": "That steady growth of the jump is the second difference.",
                "hint": "How much bigger is the second jump than the first?"
            },
            {
                "say": "That steady growth of the jump, always 2, is the <strong>second difference</strong>. When it stays constant the sequence is <strong>quadratic</strong>: its nth term has an \\(n^2\\). Halve the second difference for the number in front of \\(n^2\\) (here \\(2 \\div 2 = 1\\)), and these really are \\(n^2 + n\\): 2, 6, 12, 20."
            }
        ]
    },
    "teach": {
        "bronze": {
            "display": "If \\(f(x) = 4x - 1\\), find \\(f(5)\\)",
            "label": "Together: your first one",
            "steps": [
                {"say": "\\(f(5)\\) means put \\(x = 5\\) into \\(4x - 1\\). Read the input first.",
                 "pre": "The input x is ", "post": "", "answer": 5, "hint": "It is the number inside the brackets."},
                {"pre": "Work out 4 " + TIMES + " 5 = ", "post": "", "answer": 20, "hint": "Multiply the input by 4."},
                {"pre": "Now subtract 1: 20 " + MINUS + " 1 = ", "post": "", "answer": 19, "hint": "Take away 1."},
                {"pre": "Check: 4 " + TIMES + " 5 " + MINUS + " 1 = ", "post": "", "answer": 19,
                 "done": "Input 5 gives output 19. That is all f(5) asks.", "hint": "Multiply then subtract."}
            ]
        },
        "silver": {
            "display": "If \\(f(x) = 2x + 1\\) and \\(g(x) = x^2\\), find \\(fg(3)\\)",
            "label": "Together: the silver move",
            "steps": [
                {"say": "\\(fg(3)\\) does \\(g\\) first, then \\(f\\). Start inside with \\(g(3)\\).",
                 "pre": "g first: 3 " + TIMES + " 3 = ", "post": "", "answer": 9, "hint": "g squares the input."},
                {"pre": "Feed 9 into f: 2 " + TIMES + " 9 = ", "post": "", "answer": 18, "hint": "Multiply by 2."},
                {"pre": "Add 1: 18 + 1 = ", "post": "", "answer": 19, "hint": "Add the 1."},
                {"pre": "Check: f(g(3)) = 2 " + TIMES + " 9 + 1 = ", "post": "", "answer": 19,
                 "done": "Inside function first, every time. gf would differ.", "hint": "Multiply then add."}
            ]
        },
        "gold": {
            "display": "Find the nth term of \\(5, 12, 23, 38, 57, ...\\)",
            "label": "Together: the gold move",
            "steps": [
                {"say": "A full quadratic nth term. First the second difference.",
                 "pre": "First gaps 7 and 11. Second difference: 11 " + MINUS + " 7 = ", "post": "", "answer": 4,
                 "hint": "Difference of the differences."},
                {"pre": "Halve it for the n² coefficient: 4 " + DIV + " 2 = ", "post": "", "answer": 2,
                 "hint": "a is the second difference divided by 2."},
                {"say": "Now subtract \\(2n^2\\) from each term to leave a linear sequence.",
                 "pre": "Term 1: 5 " + MINUS + " 2 " + TIMES + " 1² = 5 " + MINUS + " 2 = ", "post": "", "answer": 3,
                 "hint": "2 times 1 squared is 2."},
                {"pre": "Term 2: 12 " + MINUS + " 2 " + TIMES + " 2² = 12 " + MINUS + " 8 = ", "post": "", "answer": 4,
                 "hint": "2 times 2 squared is 8."},
                {"say": "The remainder 3, 4, 5, ... rises by 1, giving \\(n + 2\\). So the nth term is \\(2n^2 + n + 2\\).",
                 "pre": "Check term 3: 2 " + TIMES + " 3² + 3 + 2 = 18 + 3 + 2 = ", "post": "", "answer": 23,
                 "done": "Matches the sequence, so the nth term is 2n² + n + 2.", "hint": "18 + 3 + 2."}
            ]
        }
    }
}

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: put one value in",
        "steps": [
            "Function notation \\(f(x)\\) is a machine: whatever sits in the brackets replaces every \\(x\\). \\(f(4)\\) means swap \\(x\\) for 4, then work it out.",
            "For a sequence, the <strong>second difference</strong> is the difference of the first differences. A constant one means the sequence is quadratic.",
            "Take care squaring negatives: \\((-3)^2 = 9\\), never \\(-9\\) or \\(-6\\)."
        ],
        "example": {
            "question": "If f(x) = 3x + 2, find f(4)",
            "steps": [
                {"label": "Substitute", "content": "<p>Replace \\(x\\) with 4: \\(3 \\times 4 + 2\\)</p>"},
                {"label": "Work out", "content": "<p>\\(12 + 2 = 14\\)</p>"},
                {"label": "Check", "content": "<p>Input 4, output 14 ✓</p>"},
                {"label": "Answer", "content": "<p>\\(f(4) = 14\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: two linked steps",
        "steps": [
            "Composite \\(fg(x)\\) works inside out: do \\(g\\) first, then put its answer into \\(f\\). Order matters, so \\(fg\\) and \\(gf\\) usually differ.",
            "An inverse \\(f^{-1}(x)\\) undoes \\(f\\). Write \\(y = f(x)\\), swap \\(x\\) and \\(y\\), then make \\(y\\) the subject.",
            "An iteration formula feeds each answer back in: find \\(x_1\\), then reuse it to reach \\(x_2\\)."
        ],
        "example": {
            "question": "If f(x) = x + 4 and g(x) = x², find fg(2)",
            "steps": [
                {"label": "Inside first", "content": "<p>\\(g(2) = 2^2 = 4\\)</p>"},
                {"label": "Then outside", "content": "<p>\\(f(4) = 4 + 4 = 8\\)</p>"},
                {"label": "Check", "content": "<p>g first, then f: 8 ✓</p>"},
                {"label": "Answer", "content": "<p>\\(fg(2) = 8\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: the full method",
        "steps": [
            "For a quadratic nth term, halve the second difference to get \\(a\\), then subtract \\(an^2\\) from every term to leave a linear sequence.",
            "Find the nth term of that leftover (constant difference \\(b\\)); the result is \\(an^2 + bn + c\\).",
            "To solve \\(fg(x) = k\\), build the composite, set it equal to \\(k\\), and solve. To iterate to a root, repeat the formula until the digits settle."
        ],
        "example": {
            "question": "Find the nth term of 4, 13, 28, 49, ...",
            "steps": [
                {"label": "Second difference", "content": "<p>Gaps 9, 15, 21; second difference 6, so \\(a = 3\\)</p>"},
                {"label": "Subtract 3n²", "content": "<p>\\(4-3=1,\\ 13-12=1,\\ 28-27=1\\): remainder 1</p>"},
                {"label": "Combine", "content": "<p>\\(3n^2 + 1\\)</p>"},
                {"label": "Check", "content": "<p>\\(n=2:\\ 3(4)+1 = 13\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(3n^2 + 1\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- problem_bank descriptions ----------------
pb = pd["problem_bank"]
pb["bronze_description"] = "Put one number in: find a single difference, or substitute one value into a function."
pb["silver_description"] = "Two linked steps: composite or inverse functions, or one iteration step."
pb["gold_description"] = "Full quadratic nth term, solving composite equations, or iterating to a root."

# ---------------- helper builders ----------------
def mc(sol_index, message):
    return {"expect": None, "message": message, "pattern": "explain"}

# Rebuild each tier's problems by display-key so we can reorder cleanly.
def find(tier, needle):
    for p in pb[tier]:
        if needle in p["display"]:
            return p
    raise KeyError(needle)

# ---- BRONZE ----
B1 = find("bronze", "3, 6, 11, 18, 27")
B1["hint"] = "Find the differences of the differences, not just the first gaps."
B1["misconceptions"] = [{"pattern": "first_difference", "check": "first_difference", "expect": 3,
    "message": "3, 5, 7, 9 are the first differences and they are not constant. Take the difference of those: 5 " + MINUS + " 3 = 2. The second difference is 2.",
    "note": "reports first first-difference"}]
B1["guided_steps"] = [
    {"say": "Second difference means the difference of the differences. First, the gaps between terms.",
     "pre": "6 " + MINUS + " 3 = ", "post": "", "answer": 3, "hint": "Subtract the first two terms."},
    {"pre": "11 " + MINUS + " 6 = ", "post": "", "answer": 5, "hint": "Subtract the next pair."},
    {"phase": "substitute", "pre": "Now the difference of those gaps: 5 " + MINUS + " 3 = ", "post": "", "answer": 2,
     "hint": "Subtract the first gap from the second."},
    {"phase": "substitute", "pre": "Check it stays constant: 18 " + MINUS + " 11 = 7, then 7 " + MINUS + " 5 = ", "post": "", "answer": 2,
     "done": "A constant second difference of 2, so the sequence is quadratic.", "hint": "Seven minus five."}
]

B2 = find("bronze", "second difference 6")
B2["hint"] = "The coefficient of n squared is half the second difference."
B2["misconceptions"] = [{"pattern": "forgot_halve", "check": "forgot_halve", "expect": 6,
    "message": "The coefficient of \\(n^2\\) is HALF the second difference: 6 " + DIV + " 2 = 3. Using 6 itself skips the halving.",
    "note": "forgets to halve"}]
B2["guided_steps"] = [
    {"say": "The number in front of \\(n^2\\) is always half the second difference.",
     "pre": "Write the second difference: ", "post": "", "answer": 6, "hint": "It is given in the question."},
    {"phase": "substitute", "pre": "Halve it: 6 " + DIV + " 2 = ", "post": "", "answer": 3, "hint": "Divide by 2."},
    {"phase": "substitute", "pre": "Check by doubling back: 3 " + TIMES + " 2 = ", "post": "", "answer": 6,
     "done": "Doubling returns the second difference, so a = 3 is right.", "hint": "Three times two."}
]

B3 = find("bronze", "f(x) = 2x + 3")
B3["hint"] = "Multiply the input by 2, then add 3."
B3["misconceptions"] = [{"pattern": "bracket_order", "check": "bracket_order", "expect": 14,
    "message": "\\(f(x) = 2x + 3\\) means multiply \\(x\\) by 2 THEN add 3: \\(2 \\times 4 + 3 = 11\\), not \\(2 \\times (4 + 3)\\).",
    "note": "does 2*(4+3)=14"}]
B3["guided_steps"] = [
    {"say": "\\(f(4)\\) means put \\(x = 4\\) into \\(2x + 3\\).",
     "pre": "The input x is ", "post": "", "answer": 4, "hint": "The number inside the brackets."},
    {"pre": "Work out 2 " + TIMES + " 4 = ", "post": "", "answer": 8, "hint": "Multiply the input by 2."},
    {"phase": "substitute", "pre": "Now add 3: 8 + 3 = ", "post": "", "answer": 11, "hint": "Add the 3."},
    {"phase": "substitute", "pre": "Check: 2 " + TIMES + " 4 + 3 = ", "post": "", "answer": 11,
     "done": "Input 4 gives output 11, so f(4) = 11.", "hint": "Multiply then add."}
]

B4 = find("bronze", "f(x) = x^2 - 1\\), find \\(f(3)")
B4["hint"] = "Square the input first, then subtract 1."
B4["misconceptions"] = [{"pattern": "squared_as_double", "check": "squared_as_double", "expect": 5,
    "message": "\\(x^2\\) means \\(x \\times x = 9\\), not \\(2 \\times x\\). So \\(f(3) = 9 " + MINUS + " 1 = 8\\).",
    "note": "reads x^2 as 2x -> 6-1=5"}]
B4["guided_steps"] = [
    {"say": "\\(f(3)\\) means put \\(x = 3\\) into \\(x^2 - 1\\). Here \\(x^2\\) means \\(x \\times x\\).",
     "pre": "Square the input: 3 " + TIMES + " 3 = ", "post": "", "answer": 9, "hint": "Three times three, not three times two."},
    {"phase": "substitute", "pre": "Now subtract 1: 9 " + MINUS + " 1 = ", "post": "", "answer": 8, "hint": "Take away 1."},
    {"phase": "substitute", "pre": "Check: 3 squared is 9, minus 1 = ", "post": "", "answer": 8,
     "done": "So f(3) = 8.", "hint": "Nine minus one."}
]

B5 = find("bronze", "f(-2)")
B5["display"] = "If \\(f(x) = x^2 - 1\\), find \\(f(-4)\\)"
B5["solutions"] = [15]
B5["hint"] = "A negative number squared is positive."
B5["misconceptions"] = [{"pattern": "negative_square", "check": "negative_square", "expect": -17,
    "message": "\\((-4)^2 = (-4) \\times (-4) = 16\\), positive. So \\(f(-4) = 16 " + MINUS + " 1 = 15\\). Getting " + MINUS + "17 treats \\((-4)^2\\) as " + MINUS + "16.",
    "note": "(-4)^2 taken as -16"}]
B5["guided_steps"] = [
    {"say": "\\(f(-4)\\) means put \\(x = -4\\) into \\(x^2 - 1\\). A negative squared is positive.",
     "pre": "Square it: (" + MINUS + "4) " + TIMES + " (" + MINUS + "4) = ", "post": "", "answer": 16,
     "hint": "Negative times negative is positive."},
    {"phase": "substitute", "pre": "Now subtract 1: 16 " + MINUS + " 1 = ", "post": "", "answer": 15, "hint": "Take away 1."},
    {"phase": "substitute", "pre": "Check: (" + MINUS + "4) squared is 16, minus 1 = ", "post": "", "answer": 15,
     "done": "So f(" + MINUS + "4) = 15.", "hint": "Sixteen minus one."}
]

B6 = find("bronze", "n^2 + 2n")
B6["hint"] = "Put n equals 5 into the formula."
B6["misconceptions"] = [{"pattern": "squared_as_double", "check": "squared_as_double", "expect": 20,
    "message": "The 5th term is \\(5^2 + 2 \\times 5 = 25 + 10 = 35\\). Using \\(5 \\times 2 = 10\\) for \\(5^2\\) gives 20, the slip.",
    "note": "5^2 taken as 2*5"}]
B6["guided_steps"] = [
    {"say": "The 5th term means put \\(n = 5\\) into \\(n^2 + 2n\\).",
     "pre": "Square n: 5 " + TIMES + " 5 = ", "post": "", "answer": 25, "hint": "Five times five."},
    {"pre": "The 2n part: 2 " + TIMES + " 5 = ", "post": "", "answer": 10, "hint": "Multiply five by two."},
    {"phase": "substitute", "pre": "Add them: 25 + 10 = ", "post": "", "answer": 35, "hint": "Add the two parts."},
    {"phase": "substitute", "pre": "Check: 5² + 2 " + TIMES + " 5 = 25 + 10 = ", "post": "", "answer": 35,
     "done": "The 5th term is 35.", "hint": "Twenty-five plus ten."}
]

B7 = find("bronze", "1, 4, 9, 16, 25")
B7["hint"] = "These are the square numbers."
B7["misconceptions"] = [mc(0, "These are the square numbers \\(1^2, 2^2, 3^2, 4^2, 5^2\\), so the nth term is \\(n^2\\).")]

B8 = find("bronze", "g(x) = 5x - 2")
B8["hint"] = "Anything multiplied by 0 is 0."
B8["misconceptions"] = [{"pattern": "times_zero", "check": "times_zero", "expect": 3,
    "message": "\\(5 \\times 0 = 0\\), so \\(g(0) = 0 " + MINUS + " 2 = " + MINUS + "2\\). Getting 3 treats \\(5 \\times 0\\) as 5.",
    "note": "5*0 taken as 5"}]
B8["guided_steps"] = [
    {"say": "\\(g(0)\\) means put \\(x = 0\\) into \\(5x - 2\\).",
     "pre": "The 5x part: 5 " + TIMES + " 0 = ", "post": "", "answer": 0, "hint": "Anything times zero is zero."},
    {"phase": "substitute", "pre": "Now subtract 2: 0 " + MINUS + " 2 = ", "post": "", "answer": -2, "hint": "Zero take away two."},
    {"phase": "substitute", "pre": "Check: 5 " + TIMES + " 0 " + MINUS + " 2 = ", "post": "", "answer": -2,
     "done": "So g(0) = " + MINUS + "2.", "hint": "Zero minus two."}
]

pb["bronze"] = [B1, B2, B3, B4, B5, B6, B7, B8]

# ---- SILVER ----
S1 = find("silver", "4, 10, 20, 34, 52")
S1["hint"] = "Second difference is 4, so a is 2; then find the constant left over."
S1["misconceptions"] = [mc(0, "First differences 6, 10, 14, 18; second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): 2, 2, 2, 2, 2. The remainder is 2, so the nth term is \\(2n^2 + 2\\).")]

S2 = find("silver", "0, 5, 14, 27, 44")
S2["hint"] = "Find a from the second difference, then the linear remainder."
S2["misconceptions"] = [mc(1, "First differences 5, 9, 13, 17; second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): " + MINUS + "2, " + MINUS + "3, " + MINUS + "4, " + MINUS + "5, " + MINUS + "6, which is \\(-n - 1\\). The nth term is \\(2n^2 - n - 1\\).")]

S3 = find("silver", "find \\(fg(2)")
S3["hint"] = "Do g first, then put its answer into f."
S3["misconceptions"] = [{"pattern": "wrong_order", "check": "wrong_order", "expect": 49,
    "message": "\\(fg(2)\\) applies \\(g\\) first: \\(g(2) = 2^2 = 4\\), then \\(f(4) = 3 \\times 4 + 1 = 13\\). Doing \\(f\\) first gives 49, which is \\(gf(2)\\).",
    "note": "computes gf instead"}]
S3["guided_steps"] = [
    {"say": "\\(fg(2)\\) means do \\(g\\) first, then \\(f\\). Start inside with \\(g(2)\\).",
     "pre": "g(2) = 2 " + TIMES + " 2 = ", "post": "", "answer": 4, "hint": "g squares the input: two squared."},
    {"phase": "substitute", "pre": "Now feed 4 into f: 3 " + TIMES + " 4 = ", "post": "", "answer": 12, "hint": "Multiply by 3."},
    {"phase": "substitute", "pre": "Add 1: 12 + 1 = ", "post": "", "answer": 13, "hint": "Add the 1."},
    {"phase": "substitute", "pre": "Check: f(g(2)) = 3 " + TIMES + " 4 + 1 = ", "post": "", "answer": 13,
     "done": "g first then f gives 13.", "hint": "Multiply then add."}
]

S4 = find("silver", "find \\(gf(2)")
S4["hint"] = "Do f first, then put its answer into g."
S4["misconceptions"] = [{"pattern": "wrong_order", "check": "wrong_order", "expect": 13,
    "message": "\\(gf(2)\\) applies \\(f\\) first: \\(f(2) = 3 \\times 2 + 1 = 7\\), then \\(g(7) = 7^2 = 49\\). Doing \\(g\\) first gives 13, which is \\(fg(2)\\).",
    "note": "computes fg instead"}]
S4["guided_steps"] = [
    {"say": "\\(gf(2)\\) means do \\(f\\) first, then \\(g\\). Start inside with \\(f(2)\\).",
     "pre": "f(2) = 3 " + TIMES + " 2 + 1 = ", "post": "", "answer": 7, "hint": "Multiply by 3 then add 1."},
    {"phase": "substitute", "pre": "Now feed 7 into g: 7 " + TIMES + " 7 = ", "post": "", "answer": 49, "hint": "g squares it: seven squared."},
    {"phase": "substitute", "pre": "Check: g(f(2)) = 7² = ", "post": "", "answer": 49,
     "done": "f first then g gives 49.", "hint": "Seven times seven."}
]

S5 = find("silver", "f(x) = 2x + 5")
S5["hint"] = "Reverse the steps: undo the plus 5, then undo the times 2."
S5["misconceptions"] = [{"pattern": "applied_forward", "check": "applied_forward", "expect": 27,
    "message": "\\(f^{-1}\\) reverses \\(f\\): \\(f^{-1}(x) = \\frac{x-5}{2}\\), so \\(f^{-1}(11) = 6 " + DIV + " 2 = 3\\). Putting 11 into \\(f\\) gives 27, the wrong direction.",
    "note": "computes f(11) forward"}]
S5["guided_steps"] = [
    {"say": "First reverse the function. From \\(y = 2x + 5\\), swap and rearrange: \\(f^{-1}(x) = \\frac{x - 5}{2}\\).",
     "pre": "Undo the +5: 11 " + MINUS + " 5 = ", "post": "", "answer": 6, "hint": "Undo the plus 5 first."},
    {"phase": "substitute", "pre": "Undo the " + TIMES + "2: 6 " + DIV + " 2 = ", "post": "", "answer": 3, "hint": "Divide by 2."},
    {"phase": "substitute", "pre": "Check with f: 2 " + TIMES + " 3 + 5 = ", "post": "", "answer": 11,
     "done": "f sends 3 back to 11, so f⁻¹(11) = 3.", "hint": "Put 3 into the original 2x + 5."}
]

S6 = find("silver", "\\sqrt{x_n + 5}")
S6["hint"] = "Add inside first, then take the square root."
S6["misconceptions"] = [{"pattern": "sqrt_order", "check": "sqrt_order", "expect": 6.41,
    "message": "Add inside first, then square root: \\(\\sqrt{2 + 5} = \\sqrt{7} = 2.65\\). Doing \\(\\sqrt{2}\\) then adding 5 gives 6.41.",
    "note": "sqrt(2)+5 = 6.41"}]
S6["guided_steps"] = [
    {"say": "One step of the iteration: put \\(x_0 = 2\\) into \\(\\sqrt{x_n + 5}\\). Add first, then square root.",
     "pre": "Inside first: 2 + 5 = ", "post": "", "answer": 7, "hint": "Add before the square root."},
    {"phase": "substitute", "pre": "Now square root, to 2 d.p.: √7 = ", "post": "", "answer": 2.65, "hint": "Square root of 7 on the calculator."},
    {"phase": "substitute", "pre": "Check: 2.65 squared is about 7, and 7 " + MINUS + " 5 = ", "post": "", "answer": 2,
     "done": "Squaring undoes the root back to about 7, so x₁ = 2.65.", "hint": "About seven, minus five."}
]

S7 = find("silver", "2, 8, 18, 32, 50")
S7["hint"] = "Second difference is 4, so a is 2; the remainder is zero."
S7["misconceptions"] = [mc(0, "First differences 6, 10, 14, 18; second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): all zero. The nth term is \\(2n^2\\).")]

pb["silver"] = [S3, S4, S5, S6, S1, S2, S7]

# ---- GOLD ----
G1 = find("gold", "3, 9, 19, 33, 51")
G1["hint"] = "Second difference gives a; then find the constant remainder."
G1["misconceptions"] = [mc(0, "First differences 6, 10, 14, 18; second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): 1, 1, 1, 1, 1. The nth term is \\(2n^2 + 1\\).")]

G2 = find("gold", "f^{-1}(5)")
G2["hint"] = "Reverse f: double first, then subtract 3."
G2["misconceptions"] = [{"pattern": "applied_forward", "check": "applied_forward", "expect": 4,
    "message": "\\(f^{-1}\\) reverses \\(f\\): \\(f^{-1}(x) = 2x - 3\\), so \\(f^{-1}(5) = 10 " + MINUS + " 3 = 7\\). Putting 5 into \\(f\\) gives 4, the wrong direction.",
    "note": "computes f(5) forward = (5+3)/2 = 4"}]
G2["guided_steps"] = [
    {"say": "Reverse the function first. From \\(y = \\frac{x+3}{2}\\), swap and rearrange: \\(f^{-1}(x) = 2x - 3\\).",
     "pre": "Undo the " + DIV + "2 by doubling: 2 " + TIMES + " 5 = ", "post": "", "answer": 10, "hint": "Double the input first."},
    {"phase": "substitute", "pre": "Then subtract 3: 10 " + MINUS + " 3 = ", "post": "", "answer": 7, "hint": "Undo the plus 3."},
    {"phase": "substitute", "pre": "Check with f: (7 + 3) " + DIV + " 2 = ", "post": "", "answer": 5,
     "done": "f sends 7 back to 5, so f⁻¹(5) = 7.", "hint": "Put 7 into the original (x + 3)/2."}
]

G3 = find("gold", "\\frac{10}{x_n + 3}")
G3["hint"] = "Work out x1, then feed it back to get x2."
G3["misconceptions"] = [{"pattern": "stopped_early", "check": "stopped_early", "expect": 2.5,
    "message": "\\(x_1 = 10 " + DIV + " (1 + 3) = 2.5\\) is only the first step. Go again: \\(x_2 = 10 " + DIV + " (2.5 + 3) = 10 " + DIV + " 5.5 = 1.82\\).",
    "note": "gives x1 not x2"}]
G3["guided_steps"] = [
    {"say": "Two steps from \\(x_0 = 1\\). First \\(x_1\\), then feed it back for \\(x_2\\).",
     "pre": "x₁ = 10 " + DIV + " (1 + 3) = 10 " + DIV + " 4 = ", "post": "", "answer": 2.5, "hint": "Ten divided by four."},
    {"phase": "substitute", "pre": "For x₂ the new denominator is 2.5 + 3 = ", "post": "", "answer": 5.5, "hint": "Add 3 to x₁."},
    {"phase": "substitute", "pre": "x₂ = 10 " + DIV + " 5.5, to 2 d.p. = ", "post": "", "answer": 1.82,
     "done": "Two iterations: 1 to 2.5 to 1.82, so x₂ = 1.82.", "hint": "Divide ten by 5.5."}
]

G4 = find("gold", "fg(x) = 5")
G4["display"] = "If \\(f(x) = x^2 + 1\\) and \\(g(x) = 2x - 3\\), solve \\(fg(x) = 5\\). Find the larger value of \\(x\\)."
G4["solutions"] = [2.5]
G4["hint"] = "Build the composite, set it to 5, and solve for both roots."
G4["misconceptions"] = [{"pattern": "smaller_root", "check": "smaller_root", "expect": 0.5,
    "message": "\\((2x-3)^2 = 4\\) gives \\(2x - 3 = 2\\) or \\(2x - 3 = -2\\), so \\(x = 2.5\\) or \\(x = 0.5\\). The larger value is 2.5.",
    "note": "gives smaller root"}]
G4["guided_steps"] = [
    {"say": "\\(fg(x)\\) means \\(g\\) first: \\(f(2x-3) = (2x-3)^2 + 1\\). Set it equal to 5.",
     "pre": "Subtract 1 from both sides: (2x " + MINUS + " 3)² = 5 " + MINUS + " 1 = ", "post": "", "answer": 4, "hint": "Move the plus 1 across."},
    {"pre": "Square root both sides: √4 = ", "post": "", "answer": 2, "hint": "What squared gives four?"},
    {"phase": "substitute", "pre": "The + case: 2x " + MINUS + " 3 = 2, so 2x = 5 and x = ", "post": "", "answer": 2.5, "hint": "Add 3, then halve."},
    {"phase": "substitute", "pre": "The " + MINUS + " case: 2x " + MINUS + " 3 = " + MINUS + "2, 2x = 1, x = ", "post": "", "answer": 0.5,
     "done": "Roots 2.5 and 0.5; the larger value is 2.5.", "hint": "Add 3, then halve."}
]

G5 = find("gold", "\\sqrt[3]{3x_n + 5}")
G5["solutions"] = [2.268]
G5["hint"] = "Iterate twice: find x1, then use it for x2."
G5["misconceptions"] = [{"pattern": "stopped_early", "check": "stopped_early", "expect": 2.224,
    "message": "\\(x_1 = \\sqrt[3]{3 \\times 2 + 5} = \\sqrt[3]{11} = 2.224\\) is only the first step. Go again: \\(x_2 = \\sqrt[3]{3 \\times 2.224 + 5} = \\sqrt[3]{11.672} = 2.268\\).",
    "note": "gives x1 not x2"}]
G5["guided_steps"] = [
    {"say": "Two iterations from \\(x_0 = 2\\) using \\(x_{n+1} = \\sqrt[3]{3x_n + 5}\\).",
     "pre": "Inside for x₁: 3 " + TIMES + " 2 + 5 = ", "post": "", "answer": 11, "hint": "Three times two, plus five."},
    {"pre": "x₁ = cube root of 11, to 3 d.p. = ", "post": "", "answer": 2.224, "hint": "Cube root of 11 on the calculator."},
    {"phase": "substitute", "pre": "Inside for x₂: 3 " + TIMES + " 2.224 + 5 = ", "post": "", "answer": 11.672, "hint": "Three times x₁, plus five."},
    {"phase": "substitute", "pre": "x₂ = cube root of 11.672, to 3 d.p. = ", "post": "", "answer": 2.268,
     "done": "Two iterations: 2 to 2.224 to 2.268, so x₂ = 2.268.", "hint": "Cube root of 11.672."}
]

pb["gold"] = [G2, G3, G4, G5, G1]

# ---------------- method_card (slim) ----------------
pd["method_card"] = {
    "title": "Quadratic nth Term, Functions and Iteration",
    "steps": [
        "Quadratic sequence: halve the second difference for a, subtract an² to find bn + c.",
        "f(x): replace x with the input. fg(x): do g first, then f.",
        "Inverse f⁻¹: swap x and y, then make y the subject.",
        "Iteration: put xₙ into the formula to get xₙ₊₁; repeat."
    ],
    "content": "<p>A <strong>quadratic sequence</strong> has a constant second difference \\(d_2\\). Its nth term is \\(an^2 + bn + c\\) with \\(a = d_2/2\\). Subtract \\(an^2\\) from each term, then find the nth term of the linear remainder for \\(b\\) and \\(c\\).</p><p><strong>Functions:</strong> \\(f(3)\\) substitutes \\(x = 3\\). Composite \\(fg(x)\\) applies \\(g\\) first, then \\(f\\). The inverse \\(f^{-1}(x)\\) reverses \\(f\\): swap \\(x\\) and \\(y\\), then rearrange.</p><p><strong>Iteration:</strong> \\(x_{n+1} = g(x_n)\\) turns one approximation into the next; repeat until the digits stop changing.</p>",
    "example": "<p><strong>Find the nth term of</strong> 3, 9, 19, 33, 51</p><p>Second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): 1, 1, 1, 1, 1. Remainder 1.</p><p><strong>Answer:</strong> \\(2n^2 + 1\\)</p>"
}

# ---------------- write ----------------
out = "lesson_maths-aqa_algebra-L14.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# quick word-count report for method_card content
import re
def words(s): return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card content words:", words(pd["method_card"]["content"]))
for t in ("bronze", "silver", "gold"):
    print("tier_guides", t, "words:", sum(words(s) for s in pd["tier_guides"][t]["steps"]))
print("wrote", out)
