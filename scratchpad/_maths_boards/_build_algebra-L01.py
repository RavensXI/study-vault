# -*- coding: utf-8 -*-
"""Build guided-learning + (no) diagrams practice_data for maths-aqa algebra-L01
Simplifying Expressions. Keeps all problems multiple_choice (answers are
expressions, so numeric typed answers are impossible -> MC is the correct type;
guided_steps omission is sanctioned for MC). Adds required spine: hints,
tier descriptions, tier_guides, opener, three teach walks, slim method_card.
Fixes gold[2] broken options."""
import json, io

LIVE = "_live_fetch_algebra-L01.json"
OUT  = "lesson_algebra-L01.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))
pb = pd["problem_bank"]

# ---- helper: attach hint + expect:null to a problem ----
def fix(prob, hint):
    prob["hint"] = hint
    for m in prob.get("misconceptions", []):
        if "expect" not in m:
            m["expect"] = None
    return prob

# ---------- BRONZE ----------
bronze_hints = [
    "Both are x terms, so add the numbers in front.",
    "All y terms: work left to right, 7 minus 3 plus 2.",
    "Collect the a terms and the b terms separately.",
    "Collect the x terms, then the plain numbers; watch the minus.",
    "Multiply the numbers, and m times m gives m squared.",
    "Multiply the numbers, then add the powers of x.",
    "Divide the number only; the x stays.",
    "Divide the numbers, then subtract the powers of x.",
]
for p, h in zip(pb["bronze"], bronze_hints):
    fix(p, h)

# ---------- SILVER ----------
silver_hints = [
    "Collect x squared terms and x terms in separate groups.",
    "Multiply the numbers, then add the powers of a and of b.",
    "Divide the numbers, then subtract the powers of x.",
    "Expand both brackets first, then collect like terms; mind the minus.",
    "Divide the numbers, then subtract the powers of x and of y.",
    "Three groups: the p squared terms, the p terms, and the number.",
    "Cube the 3, and multiply the power inside by 3.",
]
for p, h in zip(pb["silver"], silver_hints):
    fix(p, h)

# ---------- GOLD ----------
# Fix broken gold[2] options: correct answer is 4x, none of the options showed it.
g2 = pb["gold"][2]
assert "(2x)^3" in g2["display"], g2["display"]
g2["options"] = ["\\(4x\\)", "\\(4x^5\\)", "\\(24x^3\\)", "\\(x\\)"]
# solutions stays [0]; misconception message already reads "= 4x" (correct).

gold_hints = [
    "Divide each top term by 3x separately.",
    "Divide each top term by 2x; keep the minus.",
    "Work out (2x) cubed as 8x cubed first, then multiply and divide.",
    "Expand the squared bracket fully, multiply by 3, then subtract.",
    "Factorise x squared minus 9 as a difference of two squares, then cancel.",
]
for p, h in zip(pb["gold"], gold_hints):
    fix(p, h)

# ---------- tier descriptions ----------
pb["bronze_description"] = "Collect like terms, or multiply and divide single terms using the index laws."
pb["silver_description"] = "Two steps: use an index law or expand a bracket, then collect the like terms."
pb["gold_description"]   = "Simplify tougher expressions: divide each term, factorise and cancel, or expand a square then collect."

# ---------- slim method_card ----------
pd["method_card"]["content"] = (
    "<p><strong>Simplifying</strong> means writing an expression in its shortest "
    "form by <strong>collecting like terms</strong>. Like terms share the same "
    "letter and the same power, so \\(3x\\) and \\(5x\\) combine but \\(3x\\) and "
    "\\(3x^2\\) do not.</p><p>Add or subtract the numbers in front of like terms; "
    "plain numbers combine with each other. To <strong>multiply</strong> terms, "
    "multiply the numbers and add the powers. To <strong>divide</strong>, divide "
    "the numbers and subtract the powers.</p>"
)

# ---------- OPENER (fruit bowl: collecting like terms) ----------
def fruit_svg():
    parts = []
    parts.append('<svg viewBox="0 0 260 118" role="img" '
                 'aria-label="A fruit bowl: a group of 3 apples plus a group of 5 apples, '
                 'and a group of 2 bananas plus a group of 4 bananas" '
                 'style="max-width:260px;font-family:Inter,sans-serif">')
    def apple(cx, cy):
        return ('<circle cx="%d" cy="%d" r="7" fill="#f87171" fill-opacity="0.5" '
                'stroke="currentColor" stroke-width="1"/>') % (cx, cy)
    def banana(cx, cy):
        return ('<ellipse cx="%d" cy="%d" rx="9" ry="5" fill="#fbbf24" fill-opacity="0.55" '
                'stroke="currentColor" stroke-width="1"/>') % (cx, cy)
    def plus(x, y):
        return ('<text x="%d" y="%d" fill="currentColor" font-size="15" '
                'text-anchor="middle">+</text>') % (x, y)
    def lab(x, y, t):
        return ('<text x="%d" y="%d" fill="currentColor" font-size="11" '
                'text-anchor="middle">%s</text>') % (x, y, t)
    # apples row y=30
    ax = [24, 42, 60]
    for x in ax: parts.append(apple(x, 30))
    parts.append(plus(78, 35))
    bx = [96, 114, 132, 150, 168]
    for x in bx: parts.append(apple(x, 30))
    parts.append(lab(96, 52, "apples"))
    # bananas row y=82
    for x in [24, 42]: parts.append(banana(x, 82))
    parts.append(plus(60, 87))
    for x in [80, 98, 116, 134]: parts.append(banana(x, 82))
    parts.append(lab(79, 104, "bananas"))
    parts.append('</svg>')
    return "".join(parts)

opener = {
    "label": "Before any algebra",
    "display": fruit_svg(),
    "steps": [
        {
            "say": "A fruit bowl. Just count what you see, no algebra needed.",
            "pre": "3 apples + 5 apples = ",
            "post": " apples",
            "answer": 8,
            "hint": "Count the apples: 3, then 5 more."
        },
        {
            "say": "Now the other kind of fruit.",
            "pre": "2 bananas + 4 bananas = ",
            "post": " bananas",
            "answer": 6,
            "hint": "Count the bananas: 2, then 4 more."
        },
        {
            "say": "You could NOT say \"8 apples + 6 bananas = 14 fruits\" and stop, because apples and bananas are different things. You leave it as 8 apples and 6 bananas. Algebra is identical: call an apple \\(x\\) and a banana \\(y\\), so \\(3x + 5x = 8x\\) and \\(2y + 4y = 6y\\), giving \\(8x + 6y\\). Putting the same kind of term together is called <strong>collecting like terms</strong>, and that is the whole of simplifying."
        }
    ]
}

# ---------- TEACH walks (>= 4 numeric boxes each) ----------
teach_bronze = {
    "display": "Simplify \\(5x + 4y + 3x + 2y\\)",
    "label": "Together: your first one",
    "steps": [
        {"say": "Two kinds of term here: x terms and y terms. Keep them in separate groups.",
         "pre": "x terms: 5x + 3x, so 5 + 3 = ", "post": "x", "answer": 8,
         "hint": "Add the numbers in front of x."},
        {"pre": "y terms: 4y + 2y, so 4 + 2 = ", "post": "y", "answer": 6,
         "hint": "Add the numbers in front of y."},
        {"say": "So it tidies to \\(8x + 6y\\). You cannot merge x with y, they are different letters.",
         "pre": "Check with x = 1 and y = 1. The original is 5 + 4 + 3 + 2 = ", "post": "", "answer": 14,
         "hint": "Add all four terms."},
        {"pre": "And 8x + 6y with x = 1, y = 1 is 8 + 6 = ", "post": "", "answer": 14,
         "done": "Both give 14, so 8x + 6y is right. Collecting like terms is just tidy grouping.",
         "hint": "Add 8 and 6."}
    ]
}

teach_silver = {
    "display": "Simplify \\(3a^2b \\times 4ab^3\\)",
    "label": "Together: the silver move",
    "steps": [
        {"say": "Multiply single terms in two moves: multiply the numbers, then handle each letter's powers.",
         "pre": "numbers: 3 × 4 = ", "post": "", "answer": 12,
         "hint": "Just multiply the two numbers in front."},
        {"say": "For the letters, when you MULTIPLY you ADD the powers.",
         "pre": "a: a² × a means 2 + 1 = ", "post": " so a to that power", "answer": 3,
         "hint": "Add the powers of a: 2 and 1."},
        {"pre": "b: b × b³ means 1 + 3 = ", "post": " so b to that power", "answer": 4,
         "hint": "Add the powers of b: 1 and 3."},
        {"say": "So the answer is \\(12a^3b^4\\).",
         "pre": "Check with a = 1, b = 1: 12 × 1 × 1 = ", "post": "", "answer": 12,
         "done": "Multiply the numbers, add the powers. That is the one new move.",
         "hint": "Anything to a power is still 1 when the letter is 1."}
    ]
}

teach_gold = {
    "display": "Simplify \\(\\frac{10x^2 + 15x}{5x}\\)",
    "label": "Together: the gold move",
    "steps": [
        {"say": "A fraction like this splits up: divide EACH top term by the bottom, 5x, separately.",
         "pre": "First term 10x² ÷ 5x. Numbers: 10 ÷ 5 = ", "post": "", "answer": 2,
         "hint": "Divide the numbers only for now."},
        {"say": "For the x powers, when you DIVIDE you SUBTRACT them.",
         "pre": "x² ÷ x means 2 − 1 = ", "post": " so x to that power", "answer": 1,
         "hint": "Subtract the powers: 2 take away 1."},
        {"say": "So the first term is \\(2x\\). Now the second term, 15x ÷ 5x.",
         "pre": "15 ÷ 5 = ", "post": "", "answer": 3,
         "hint": "The x over x cancels to 1, so just divide the numbers."},
        {"say": "So the answer is \\(2x + 3\\).",
         "pre": "Check with x = 1: top is 10 + 15 = 25, bottom is 5, and 25 ÷ 5 = ", "post": "", "answer": 5,
         "done": "And 2(1) + 3 = 5 too, so 2x + 3 is right. Divide every top term separately.",
         "hint": "Work out 25 divided by 5."}
    ]
}

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: collect like terms",
        "steps": [
            "Like terms have the SAME letter and the SAME power, for example \\(3x\\) and \\(5x\\). Group them together.",
            "Add or subtract the numbers in front (the coefficients). The letter part stays: \\(3x + 5x = 8x\\).",
            "Plain numbers combine with each other, and different letters never mix. To multiply or divide single terms, multiply or divide the numbers and use the index laws on the powers."
        ],
        "example": {
            "question": "Simplify 4a + 3b − a + 5b",
            "steps": [
                {"label": "Group", "content": "<p>a terms: \\(4a - a\\). b terms: \\(3b + 5b\\).</p>"},
                {"label": "Collect", "content": "<p>\\(4a - a = 3a\\) and \\(3b + 5b = 8b\\).</p>"},
                {"label": "Check", "content": "<p>With \\(a=1, b=1\\): original \\(4+3-1+5 = 11\\); answer \\(3+8 = 11\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(3a + 8b\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: one index law, then collect",
        "steps": [
            "Multiplying terms: multiply the numbers, ADD the powers, so \\(2x^3 \\times 5x^2 = 10x^5\\).",
            "Dividing terms: divide the numbers, SUBTRACT the powers. A power of a power multiplies: \\((x^2)^3 = x^6\\).",
            "If there are brackets, expand them first, then collect the like terms."
        ],
        "example": {
            "question": "Simplify 2x(3x+4) − x(x−5)",
            "steps": [
                {"label": "Expand", "content": "<p>\\(2x(3x+4) = 6x^2 + 8x\\). \\(x(x-5) = x^2 - 5x\\).</p>"},
                {"label": "Subtract and collect", "content": "<p>\\(6x^2 + 8x - (x^2 - 5x) = 5x^2 + 13x\\). The minus flips \\(-5x\\) to \\(+5x\\).</p>"},
                {"label": "Check", "content": "<p>With \\(x=1\\): original \\(2(7) - 1(-4) = 18\\); answer \\(5 + 13 = 18\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(5x^2 + 13x\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: divide, factorise or expand, then simplify",
        "steps": [
            "For a fraction, divide EVERY top term by the bottom separately: \\(\\frac{6x^2+9x}{3x} = 2x + 3\\).",
            "If the top factorises, factorise and cancel a matching bracket: \\(\\frac{x^2-9}{x+3} = x - 3\\).",
            "To simplify a squared bracket, expand it in full first, then collect like terms."
        ],
        "example": {
            "question": "Simplify (x² − 9) ÷ (x + 3)",
            "steps": [
                {"label": "Factorise the top", "content": "<p>\\(x^2 - 9 = (x+3)(x-3)\\), a difference of two squares.</p>"},
                {"label": "Cancel", "content": "<p>\\(\\frac{(x+3)(x-3)}{x+3} = x - 3\\), cancelling the \\((x+3)\\).</p>"},
                {"label": "Check", "content": "<p>With \\(x=1\\): top \\(1-9 = -8\\), bottom \\(4\\), \\(-8 \\div 4 = -2\\); answer \\(1-3 = -2\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x - 3\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

pd["tier_guides"] = tier_guides
pd["guided"] = {
    "opener": opener,
    "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold}
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# quick self-checks
def wc(s):
    return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    tot = sum(wc(s) for s in tier_guides[t]["steps"])
    print(t, "tier_guide words:", tot)
print("method_card words:", wc(pd["method_card"]["content"]))
print("EM DASH present anywhere:", "—" in json.dumps(pd, ensure_ascii=False))
print("wrote", OUT)
