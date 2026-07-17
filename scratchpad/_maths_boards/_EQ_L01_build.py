# -*- coding: utf-8 -*-
import json, io

with io.open("_EQ_L01_live.json", encoding="utf-8") as f:
    pd = json.load(f)

pb = pd["problem_bank"]

# ---- 1. FIX gold[4]: correct answer is xy (option index 2), stored [0]="x" is WRONG ----
g4 = pb["gold"][4]
g4["options"] = ["\\(xy\\)", "\\(x\\)", "\\(x^2y^2\\)", "\\(2xy\\)"]
g4["solutions"] = [0]
# (misconception message rewritten below in the enrichment loop)

# ---- 2. Enrichment: hint + cleaned message + expect:null on every problem ----
HINTS = {
    "bronze": [
        "Both are x terms, so add the numbers in front.",
        "Both are y terms, so subtract: 7 take away 3.",
        "Collect the a terms; the b term has nothing to pair with.",
        "Collect the m terms; the n term stays as it is.",
        "All p terms: work left to right, 4 add 2 take away 1.",
        "Collect the x terms and the y terms separately.",
        "Same term taken from itself: what does that leave?",
        "Collect the a terms, then the plain numbers.",
    ],
    "silver": [
        "Collect the x squared terms and the x terms in separate groups.",
        "Multiply the numbers; a times a gives a squared.",
        "Divide the numbers, then subtract the powers of x.",
        "Multiply the numbers, then add the powers of y.",
        "Collect x terms and y terms; watch the minus on 5x.",
        "Divide the numbers, then subtract the powers of x.",
        "Add the powers of a, then add the powers of b.",
    ],
    "gold": [
        "Divide the numbers, then subtract the powers for a and for b.",
        "Cube the 3, and multiply the inside power by 3.",
        "Multiply the numbers, then add the powers: negative 2 add 5.",
        "Cube the bracket first to get 8x cubed, then divide.",
        "Simplify each fraction on its own first, then multiply the results.",
    ],
}
MSGS = {
    "bronze": [
        "Add the coefficients: 3 + 5 = 8. Answer: 8x.",
        "Both are y terms: 7 − 3 = 4. Answer: 4y.",
        "Collect a terms: 2a + 4a = 6a. The b term stays: 6a + 3b.",
        "Collect m terms: 5m − 2m = 3m. The n term stays: 3m + 4n.",
        "Work left to right: 4 + 2 − 1 = 5. Answer: 5p.",
        "x terms: 8x − 3x = 5x. y terms: 2y − y = y. Answer: 5x + y.",
        "6t − 6t = 0. A term minus itself is 0.",
        "a terms: 3a + 2a = 5a. Numbers: 7 − 3 = 4. Answer: 5a + 4.",
    ],
    "silver": [
        "x² terms: 3x² − 2x² = x². x terms: 5x + x = 6x. Answer: x² + 6x.",
        "Multiply numbers: 4 × 3 = 12. a × a = a². Answer: 12a².",
        "6 ÷ 2 = 3. x² ÷ x = x. Answer: 3x.",
        "5 × 2 = 10. Add powers: y³ × y² = y⁵. Answer: 10y⁵.",
        "x terms: 2x − 5x = −3x. y terms: 3y + y = 4y. Answer: −3x + 4y.",
        "12 ÷ 4 = 3. x³ ÷ x = x². Answer: 3x².",
        "a: 2 + 1 = 3. b: 1 + 3 = 4. Answer: a³b⁴.",
    ],
    "gold": [
        "8 ÷ 2 = 4. a³ ÷ a² = a. b² ÷ b = b. Answer: 4ab.",
        "3³ = 27. (x²)³ = x⁶. Answer: 27x⁶.",
        "5 × 2 = 10. Add powers: −2 + 5 = 3. Answer: 10x³.",
        "(2x)³ = 8x³. Then 8 ÷ 4 = 2 and x³ ÷ x² = x. Answer: 2x.",
        "First fraction: 6x⁴y³ ÷ 3x²y = 2x²y². Second: 2xy ÷ 4x²y² = 1/(2xy). Multiply: 2x²y² × 1/(2xy) = xy.",
    ],
}
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        p["hint"] = HINTS[tier][i]
        mcs = p.get("misconceptions") or []
        if mcs:
            mcs[0]["message"] = MSGS[tier][i]
            mcs[0]["expect"] = None
        p["misconceptions"] = mcs

# ---- 3. tier descriptions ----
pb["bronze_description"] = "Collect like terms, or multiply and divide single terms with the index laws."
pb["silver_description"] = "Two steps: use one index law or expand a bracket, then collect the like terms."
pb["gold_description"] = "Tougher work: simplify fractions, powers of brackets, negative indices, then combine."

# ---- 4. Opener SVG (my own numbers: 2+4 apples, 3+2 bananas) ----
def circle(cx, cy):
    return ('<circle cx="%d" cy="%d" r="7" fill="#f87171" fill-opacity="0.5" '
            'stroke="currentColor" stroke-width="1"/>' % (cx, cy))
def banana(cx, cy):
    return ('<ellipse cx="%d" cy="%d" rx="9" ry="5" fill="#fbbf24" fill-opacity="0.55" '
            'stroke="currentColor" stroke-width="1"/>' % (cx, cy))
def txt(x, y, s, size=11):
    return '<text x="%d" y="%d" fill="currentColor" font-size="%d" text-anchor="middle">%s</text>' % (x, y, size, s)

parts = ['<svg viewBox="0 0 170 118" role="img" aria-label="A fruit bowl: a group of 2 apples plus a group of 4 apples, and a group of 3 bananas plus a group of 2 bananas" style="max-width:250px;font-family:Inter,sans-serif">']
# apples row cy=30: 2 apples, +, 4 apples
ax = [24, 42]
for x in ax: parts.append(circle(x, 30))
parts.append(txt(60, 35, "+", 15))
bx = [78, 96, 114, 132]
for x in bx: parts.append(circle(x, 30))
parts.append(txt(90, 52, "apples", 11))
# bananas row cy=82: 3 bananas, +, 2 bananas
cx3 = [24, 42, 60]
for x in cx3: parts.append(banana(x, 82))
parts.append(txt(78, 87, "+", 15))
dx = [96, 114]
for x in dx: parts.append(banana(x, 82))
parts.append(txt(84, 104, "bananas", 11))
parts.append("</svg>")
opener_svg = "".join(parts)

opener = {
    "label": "Before any algebra",
    "display": opener_svg,
    "steps": [
        {"pre": "2 apples + 4 apples = ", "post": " apples", "answer": 6,
         "say": "A fruit bowl. Just count what you see, no algebra needed.",
         "hint": "Count the apples: 2, then 4 more."},
        {"pre": "3 bananas + 2 bananas = ", "post": " bananas", "answer": 5,
         "say": "Now the other kind of fruit.",
         "hint": "Count the bananas: 3, then 2 more."},
        {"say": "You could not write \"6 apples + 5 bananas = 11 fruits\" and stop, because apples and bananas are different things. You leave it as 6 apples and 5 bananas. Algebra works the same way: call an apple \\(x\\) and a banana \\(y\\), so \\(2x + 4x = 6x\\) and \\(3y + 2y = 5y\\), giving \\(6x + 5y\\). Putting the same kind of term together is called <strong>collecting like terms</strong>, and that is the whole of simplifying."},
    ],
}

# ---- 5. teach walks (fresh problems NOT in the bank, every box verified) ----
teach = {
    "bronze": {
        "label": "Together: your first one",
        "display": "Simplify \\(6x + 2y + 3x + 5y\\)",
        "steps": [
            {"pre": "x terms: 6x + 3x, so 6 + 3 = ", "post": "x", "answer": 9,
             "say": "Two kinds of term: x terms and y terms. Keep them in separate groups.",
             "hint": "Add the numbers in front of x."},
            {"pre": "y terms: 2y + 5y, so 2 + 5 = ", "post": "y", "answer": 7,
             "hint": "Add the numbers in front of y."},
            {"pre": "Check with x = 1 and y = 1. The original is 6 + 2 + 3 + 5 = ", "post": "", "answer": 16,
             "say": "So it tidies to \\(9x + 7y\\). You cannot merge x with y, they are different letters.",
             "hint": "Add all four terms."},
            {"pre": "And 9x + 7y with x = 1, y = 1 is 9 + 7 = ", "post": "", "answer": 16,
             "done": "Both give 16, so 9x + 7y is right. Collecting like terms is just tidy grouping.",
             "hint": "Add 9 and 7."},
        ],
    },
    "silver": {
        "label": "Together: the silver move",
        "display": "Simplify \\(4a^2b \\times 2ab^4\\)",
        "steps": [
            {"pre": "numbers: 4 × 2 = ", "post": "", "answer": 8,
             "say": "Multiply single terms in two moves: multiply the numbers, then handle each letter's powers.",
             "hint": "Just multiply the two numbers in front."},
            {"pre": "a: a² × a means 2 + 1 = ", "post": " so a to that power", "answer": 3,
             "say": "For the letters, when you MULTIPLY you ADD the powers.",
             "hint": "Add the powers of a: 2 and 1."},
            {"pre": "b: b × b⁴ means 1 + 4 = ", "post": " so b to that power", "answer": 5,
             "hint": "Add the powers of b: 1 and 4."},
            {"pre": "Check with a = 1, b = 1: 8 × 1 × 1 = ", "post": "", "answer": 8,
             "say": "So the answer is \\(8a^3b^5\\).",
             "done": "Multiply the numbers, add the powers. That is the one new move.",
             "hint": "Anything to a power is still 1 when the letter is 1."},
        ],
    },
    "gold": {
        "label": "Together: the gold move",
        "display": "Simplify \\(\\frac{(3x)^2 \\times 2x}{6x^2}\\)",
        "steps": [
            {"pre": "First deal with (3x)². Square the 3: 3 × 3 = ", "post": "", "answer": 9,
             "say": "A power on a bracket hits everything inside. (3x)² means 3² times x².",
             "hint": "Just square the number 3."},
            {"pre": "Now the top number: 9 × 2 = ", "post": "", "answer": 18,
             "say": "So the numerator is \\(9x^2 \\times 2x = 18x^3\\) (powers 2 + 1 = 3).",
             "hint": "Multiply 9 by 2."},
            {"pre": "Divide the numbers: 18 ÷ 6 = ", "post": "", "answer": 3,
             "say": "Now divide top by bottom. Numbers first.",
             "hint": "Work out 18 divided by 6."},
            {"pre": "Powers of x: x³ ÷ x² means 3 − 2 = ", "post": " so x to that power", "answer": 1,
             "say": "When you DIVIDE, you SUBTRACT the powers. So the answer is \\(3x\\).",
             "hint": "Subtract the powers: 3 take away 2."},
            {"pre": "Check with x = 1: top is (3)² × 2 = 18, bottom is 6, and 18 ÷ 6 = ", "post": "", "answer": 3,
             "done": "And 3x with x = 1 is 3 too, so 3x is right. Square the bracket, then divide.",
             "hint": "Work out 18 divided by 6."},
        ],
    },
}

pd["guided"] = {"opener": opener, "teach": teach}

# ---- 6. tier_guides (my own; examples fully verified) ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: collect like terms",
        "steps": [
            "Like terms share the SAME letter and the SAME power, such as \\(4x\\) and \\(9x\\). Group them together.",
            "Add or subtract the numbers in front (the coefficients); the letter stays: \\(4x + 9x = 13x\\).",
            "Plain numbers combine with each other, and different letters never mix. To multiply or divide single terms, work on the numbers and use the index laws on the powers.",
        ],
        "example": {
            "question": "Simplify 7a + 2b − 3a + 6b",
            "steps": [
                {"label": "Group", "content": "<p>a terms: \\(7a - 3a\\). b terms: \\(2b + 6b\\).</p>"},
                {"label": "Collect", "content": "<p>\\(7a - 3a = 4a\\) and \\(2b + 6b = 8b\\).</p>"},
                {"label": "Check", "content": "<p>With \\(a=1, b=1\\): original \\(7+2-3+6 = 12\\); answer \\(4+8 = 12\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(4a + 8b\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: one index law, then collect",
        "steps": [
            "Multiplying terms: multiply the numbers, ADD the powers, so \\(3x^2 \\times 4x^3 = 12x^5\\).",
            "Dividing terms: divide the numbers, SUBTRACT the powers, so \\(\\frac{12x^5}{3x^2} = 4x^3\\).",
            "If there is a bracket, expand it first, then collect the like terms.",
        ],
        "example": {
            "question": "Simplify 2x(x + 3) + x²",
            "steps": [
                {"label": "Expand", "content": "<p>\\(2x(x+3) = 2x^2 + 6x\\).</p>"},
                {"label": "Collect", "content": "<p>\\(2x^2 + 6x + x^2 = 3x^2 + 6x\\).</p>"},
                {"label": "Check", "content": "<p>With \\(x=1\\): original \\(2(4) + 1 = 9\\); answer \\(3 + 6 = 9\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(3x^2 + 6x\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: fractions, powers and negative indices",
        "steps": [
            "For a fraction, divide EACH top term by the bottom separately: \\(\\frac{8x^2 + 6x}{2x} = 4x + 3\\).",
            "A power on a bracket hits everything inside: \\((3x^2)^2 = 9x^4\\), and a power of a power multiplies.",
            "A negative index still ADDS when multiplying: \\(x^{-2} \\times x^5 = x^3\\).",
        ],
        "example": {
            "question": "Simplify (2x³)² ÷ 4x²",
            "steps": [
                {"label": "Square the bracket", "content": "<p>\\((2x^3)^2 = 4x^6\\): square the 2, double the power.</p>"},
                {"label": "Divide", "content": "<p>\\(4x^6 \\div 4x^2 = x^4\\): \\(4 \\div 4 = 1\\), \\(6 - 2 = 4\\).</p>"},
                {"label": "Check", "content": "<p>With \\(x=1\\): \\((2)^2 \\div 4 = 1\\); answer \\(x^4 = 1\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x^4\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- 7. method_card preserved as-is (already slim, <=140 words, <=4 steps) ----

with io.open("lesson_maths-eduqas_algebra-L01.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

# em-dash guard
raw = json.dumps(pd, ensure_ascii=False)
print("em dash present:", "—" in raw)
print("shard written. top keys:", list(pd.keys()))
