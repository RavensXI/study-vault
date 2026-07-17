# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_ocr_algL03.json", encoding="utf-8"))

# ---- 1. Fix em dashes in preserved worked_examples labels (style law) ----
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---- 2. Trim method_card, remove em dash ----
pd["method_card"]["title"] = "How to Factorise Expressions"
pd["method_card"]["steps"] = [
    "Look for a common factor first (always check this)",
    "For x² + bx + c: find two numbers that multiply to c and add to b",
    "For a² − b²: use difference of two squares = (a+b)(a−b)",
    "Check by expanding your answer back",
]
pd["method_card"]["content"] = (
    "<p><strong>Factorising</strong> is the reverse of expanding: you put an "
    "expression back into brackets.</p>"
    "<p><strong>Common factor:</strong> take out the highest common factor (HCF). "
    "For \\(6x + 9\\), the HCF is 3, so \\(3(2x + 3)\\).</p>"
    "<p><strong>Quadratics</strong> \\(x^2 + bx + c\\): find two numbers that "
    "multiply to \\(c\\) and add to \\(b\\). For \\(x^2 + 7x + 12\\) that is 3 and 4, "
    "giving \\((x + 3)(x + 4)\\).</p>"
    "<p><strong>Difference of two squares:</strong> \\(a^2 - b^2 = (a + b)(a - b)\\).</p>"
)
# keep existing example (no em dash there)

# ---- 3. hints + expect:null on misconceptions ----
hints = {
    "bronze": [
        "Find the highest common factor of 6 and 12, then divide each term by it.",
        "Take out the common factor 5, and keep the minus sign inside the bracket.",
        "Find the highest common factor of 8 and 12, then divide each term by it.",
        "Both terms share an x, so take x outside the bracket.",
        "The common factor is 3x, not just 3 or just x.",
        "The highest common factor of 10 and 4 is 2.",
        "Take out 3x, the highest factor shared by both terms.",
        "Find the highest common factor of 14 and 21.",
    ],
    "silver": [
        "Find two numbers that multiply to 12 and add to 7.",
        "Find two numbers that multiply to 6 and add to −5, so both are negative.",
        "Find two numbers that multiply to −15 and add to 2, so one is negative.",
        "This is a difference of two squares: x² minus 3².",
        "Find two numbers that multiply to −12 and add to −1.",
        "Difference of two squares: the square roots are 2x and 5.",
        "A perfect square: the same number multiplies to 25 and doubles to 10.",
    ],
    "gold": [
        "Multiply a by c (2×3), find factors that add to 5, then split the middle term.",
        "Multiply a by c (3×−4 = −12), find factors that add to −11.",
        "Take out 2x first, then factorise the difference of two squares that is left.",
        "Multiply a by c (6×−2 = −12), find factors that add to 1.",
        "A perfect square: it factorises to a single bracket squared.",
    ],
}
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        p["hint"] = hints[tier][i]
        for m in p.get("misconceptions", []):
            if "expect" not in m:
                m["expect"] = None   # MC: fires on any wrong choice, no single numeric expect

# ---- 4. tier descriptions ----
pd["problem_bank"]["bronze_description"] = "Take out the highest common factor and write it outside a single bracket."
pd["problem_bank"]["silver_description"] = "Factorise a quadratic into two brackets, or spot a difference of two squares."
pd["problem_bank"]["gold_description"] = "Common factor first, harder quadratics with a leading number, or factorise completely."

# ---- 5. tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: take out the common factor",
        "steps": [
            "Find the highest common factor (HCF): the biggest number, and any letter, that divides into every term.",
            "Write the HCF outside a bracket, then divide each term by it to fill the bracket.",
            "Check by expanding: multiply back out and you should get the original.",
        ],
        "example": {
            "question": "Factorise 6a + 15",
            "steps": [
                {"label": "HCF", "content": "<p>HCF of 6 and 15 is \\(3\\).</p>"},
                {"label": "Divide", "content": "<p>\\(6a \\div 3 = 2a\\) and \\(15 \\div 3 = 5\\).</p>"},
                {"label": "Check", "content": "<p>\\(3(2a + 5) = 6a + 15\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(3(2a + 5)\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: quadratics and difference of two squares",
        "steps": [
            "For \\(x^2 + bx + c\\): find two numbers that MULTIPLY to \\(c\\) and ADD to \\(b\\); they fill \\((x + \\square)(x + \\square)\\).",
            "Watch signs: a positive \\(c\\) with a negative \\(b\\) means both numbers are negative.",
            "Difference of two squares: \\(a^2 - b^2 = (a + b)(a - b)\\), for example \\(x^2 - 9 = (x + 3)(x - 3)\\).",
        ],
        "example": {
            "question": "Factorise x² + 9x + 20",
            "steps": [
                {"label": "Two numbers", "content": "<p>Multiply to \\(20\\), add to \\(9\\): \\(4\\) and \\(5\\).</p>"},
                {"label": "Brackets", "content": "<p>\\((x + 4)(x + 5)\\).</p>"},
                {"label": "Check", "content": "<p>\\(4 \\times 5 = 20\\), \\(4 + 5 = 9\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\((x + 4)(x + 5)\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: common factor first, then the ac method",
        "steps": [
            "Always take out a common factor first: \\(2x^3 - 8x = 2x(x^2 - 4)\\), then keep going.",
            "For \\(ax^2 + bx + c\\), find two numbers that multiply to \\(a \\times c\\) and add to \\(b\\).",
            "Split the middle term with those two numbers, then factorise in two pairs (grouping).",
        ],
        "example": {
            "question": "Factorise 2x² + 7x + 6",
            "steps": [
                {"label": "ac", "content": "<p>\\(a \\times c = 2 \\times 6 = 12\\). Two numbers: \\(3\\) and \\(4\\) (\\(\\times 12\\), \\(+7\\)).</p>"},
                {"label": "Split and group", "content": "<p>\\(2x^2 + 3x + 4x + 6 = x(2x + 3) + 2(2x + 3)\\).</p>"},
                {"label": "Check", "content": "<p>\\((2x + 3)(x + 2)\\); with \\(x = 1\\): \\(5 \\times 3 = 15\\); original \\(2 + 7 + 6 = 15\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\((2x + 3)(x + 2)\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- 6. guided: opener (SVG) + teach walks ----
# Opener SVG: 12 sweets (circles) + 8 chocolates (squares)
def opener_svg():
    parts = ['<svg viewBox="0 0 260 122" role="img" aria-label="A group of 12 sweets shown as circles and a group of 8 chocolates shown as squares" style="max-width:260px;font-family:Inter,sans-serif">']
    # 12 sweets, two rows of 6
    idx = 0
    for row in range(2):
        for col in range(6):
            cx = 24 + col * 26
            cy = 20 + row * 20
            parts.append('<circle cx="%d" cy="%d" r="7" fill="#f472b6" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>' % (cx, cy))
            idx += 1
    parts.append('<text x="130" y="58" fill="currentColor" font-size="11" text-anchor="middle">12 sweets</text>')
    # 8 chocolates, one row of 8
    for col in range(8):
        x = 22 + col * 26
        parts.append('<rect x="%d" y="76" width="13" height="13" rx="2" fill="#d97706" fill-opacity="0.45" stroke="currentColor" stroke-width="1"/>' % x)
    parts.append('<text x="130" y="112" fill="currentColor" font-size="11" text-anchor="middle">8 chocolates</text>')
    parts.append('</svg>')
    return "".join(parts)

pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_svg(),
        "steps": [
            {
                "pre": "Biggest number of identical bags = ",
                "say": "You have 12 sweets and 8 chocolates. You want to fill identical party bags with nothing left over. Just use common sense.",
                "hint": "What is the biggest number that divides into both 12 and 8?",
                "post": " bags",
                "answer": 4,
            },
            {
                "pre": "Sweets in each bag: 12 ÷ 4 = ",
                "say": "Share the sweets equally between the 4 bags.",
                "hint": "Divide 12 by 4.",
                "post": " sweets",
                "answer": 3,
            },
            {
                "pre": "Chocolates in each bag: 8 ÷ 4 = ",
                "hint": "Divide 8 by 4.",
                "post": " chocolates",
                "answer": 2,
            },
            {
                "say": "So 12 sweets and 8 chocolates split into 4 bags of (3 sweets + 2 chocolates). In algebra that is exactly \\(12s + 8c = 4(3s + 2c)\\). The number outside the bracket is the biggest shared factor (the HCF), and putting it there is called <strong>factorising</strong>. It is expanding done in reverse."
            },
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "Factorise \\(8a + 20\\)",
            "steps": [
                {
                    "pre": "HCF of 8 and 20 = ",
                    "say": "Find the biggest number that divides into both 8 and 20.",
                    "hint": "Factors shared by 8 and 20: the largest is 4.",
                    "post": "",
                    "answer": 4,
                },
                {
                    "pre": "8a ÷ 4 = ",
                    "hint": "Divide 8 by 4; the a stays.",
                    "post": "a",
                    "answer": 2,
                },
                {
                    "pre": "20 ÷ 4 = ",
                    "say": "So it factorises to \\(4(2a + 5)\\).",
                    "hint": "Divide 20 by 4.",
                    "post": "",
                    "answer": 5,
                },
                {
                    "pre": "Check with a = 1: 4(2×1 + 5) = 4×7 = ",
                    "done": "Original 8(1) + 20 = 28 too, so 4(2a + 5) is right. The HCF goes outside the bracket.",
                    "hint": "Work out 4 times 7.",
                    "post": "",
                    "answer": 28,
                },
            ],
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "Factorise \\(x^2 + 8x + 15\\)",
            "steps": [
                {
                    "pre": "Two numbers multiply to 15 and add to 8. Try 3 and 5: 3 × 5 = ",
                    "say": "For \\(x^2 + bx + c\\), hunt for two numbers that multiply to c and add to b.",
                    "hint": "Multiply 3 by 5.",
                    "post": "",
                    "answer": 15,
                },
                {
                    "pre": "and 3 + 5 = ",
                    "say": "Both checks pass, so the numbers are 3 and 5, giving \\((x + 3)(x + 5)\\).",
                    "hint": "Add 3 and 5.",
                    "post": "",
                    "answer": 8,
                },
                {
                    "pre": "Check the number term: 3 × 5 = ",
                    "hint": "The last term of the expansion is 3 times 5.",
                    "post": "",
                    "answer": 15,
                },
                {
                    "pre": "Check with x = 1: (1+3)(1+5) = 4×6 = ",
                    "done": "Original 1 + 8 + 15 = 24 too, so \\((x + 3)(x + 5)\\) is right.",
                    "hint": "Work out 4 times 6.",
                    "post": "",
                    "answer": 24,
                },
            ],
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "Factorise \\(2x^2 + 7x + 3\\)",
            "steps": [
                {
                    "pre": "a × c = 2 × 3 = ",
                    "say": "When the number in front of \\(x^2\\) is not 1, use the ac method: multiply a by c first.",
                    "hint": "Multiply 2 by 3.",
                    "post": "",
                    "answer": 6,
                },
                {
                    "pre": "Two numbers multiply to 6 and add to 7. Try 1 and 6: 1 + 6 = ",
                    "say": "Find two numbers that multiply to 6 (the ac) and add to 7 (the b).",
                    "hint": "Add 1 and 6.",
                    "post": "",
                    "answer": 7,
                },
                {
                    "pre": "Split the middle: 2x² + x + 6x + 3, then group to \\((2x + 1)(x + 3)\\). Number term 1 × 3 = ",
                    "hint": "Multiply the numbers in the two brackets: 1 and 3.",
                    "post": "",
                    "answer": 3,
                },
                {
                    "pre": "Check with x = 1: (2+1)(1+3) = 3×4 = ",
                    "done": "Original 2 + 7 + 3 = 12 too, so \\((2x + 1)(x + 3)\\) is right. Split the middle, then group.",
                    "hint": "Work out 3 times 4.",
                    "post": "",
                    "answer": 12,
                },
            ],
        },
    },
}

json.dump(pd, io.open("lesson_maths-ocr_algebra-L03.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-ocr_algebra-L03.json")
# word counts for tier guide steps
def wc(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    tot=sum(wc(s) for s in pd["tier_guides"][t]["steps"])
    print(t,"tier_guide steps words:",tot)
