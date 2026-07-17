# -*- coding: utf-8 -*-
"""Build guided-learning + opener SVG for maths-aqa algebra-L03 (Factorising)."""
import json, io

LIVE = "_live_algebra-L03.json"
OUT = "lesson_maths-aqa_algebra-L03.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))
pb = pd["problem_bank"]

# ---- opener SVG: 3 rows x (2 blue + 5 gold) counters ----
cells = []
for r, ytop in enumerate((6, 28, 50)):
    for c in range(7):
        xleft = 6 + c * 22
        col = "#60a5fa" if c < 2 else "#f59e0b"
        cells.append(
            '<rect x="%d" y="%d" width="20" height="20" fill="%s" fill-opacity="0.3" '
            'stroke="currentColor" stroke-width="1.5"/>' % (xleft, ytop, col)
        )
svg = ('<svg viewBox="0 0 170 82" role="img" aria-label="Three equal rows of counters, '
       'each row two blue counters then five gold counters">' + "".join(cells) + "</svg>")
opener_display = svg + "<br>3 equal rows. Each row has 2 blue and 5 gold counters."

pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_display,
        "steps": [
            {
                "say": "Count one row on its own: 2 blue counters and 5 gold counters.",
                "pre": "Counters in one row: 2 + 5 = ",
                "post": "",
                "answer": 7,
                "hint": "Add the two blue and five gold."
            },
            {
                "say": "There are 3 identical rows.",
                "pre": "All 3 rows together: 3 × 7 = ",
                "post": "",
                "answer": 21,
                "hint": "Three lots of seven."
            },
            {
                "say": "So 21 is 3 lots of (2 + 5), which is 3 × (2 + 5). Splitting a total into equal groups is factorising: you write the shared 3 outside a bracket. Now swap the counts for \\(x\\): 6 blue and 15 gold become \\(6x + 15\\), and the same 3 rows give \\(6x + 15 = 3(2x + 5)\\). Taking out the common factor is exactly sharing into equal rows."
            }
        ]
    },
    "teach": {
        "bronze": {
            "display": "Factorise \\(6x + 15\\)",
            "label": "Together: your first one",
            "steps": [
                {
                    "say": "Look for the highest common factor of 6x and 15.",
                    "pre": "Biggest number that divides both 6 and 15: ",
                    "post": "",
                    "answer": 3,
                    "hint": "What divides into 6 and into 15?"
                },
                {
                    "pre": "6x ÷ 3 = ",
                    "post": "x",
                    "answer": 2,
                    "hint": "Divide the 6 by 3."
                },
                {
                    "pre": "15 ÷ 3 = ",
                    "post": "",
                    "answer": 5,
                    "hint": "Divide the 15 by 3."
                },
                {
                    "say": "So \\(6x + 15 = 3(2x + 5)\\). Check by putting x = 1 into both forms.",
                    "pre": "3(2 + 5) = 3 × 7 = ",
                    "post": "",
                    "answer": 21,
                    "hint": "Work out the bracket first, then times 3."
                },
                {
                    "pre": "and 6 × 1 + 15 = ",
                    "post": "",
                    "answer": 21,
                    "done": "Both give 21, so 3(2x + 5) is right.",
                    "hint": "Put x = 1 into 6x + 15."
                }
            ]
        },
        "silver": {
            "display": "Factorise \\(x^2 + 8x + 15\\)",
            "label": "Together: the silver move",
            "steps": [
                {
                    "say": "For \\(x^2 + bx + c\\), find two numbers that multiply to c and add to b.",
                    "pre": "Their product must be ",
                    "post": "",
                    "answer": 15,
                    "hint": "The last number in the expression."
                },
                {
                    "pre": "Their sum must be ",
                    "post": "",
                    "answer": 8,
                    "hint": "The number in front of x."
                },
                {
                    "say": "The pair 3 and 5 fits.",
                    "pre": "3 × 5 = ",
                    "post": "",
                    "answer": 15,
                    "hint": "Multiply the pair."
                },
                {
                    "pre": "3 + 5 = ",
                    "post": "",
                    "answer": 8,
                    "hint": "Add the pair."
                },
                {
                    "say": "So \\(x^2 + 8x + 15 = (x + 3)(x + 5)\\). Check with x = 1.",
                    "pre": "(1 + 3)(1 + 5) = 4 × 6 = ",
                    "post": "",
                    "answer": 24,
                    "hint": "Work out each bracket at x = 1, then multiply."
                },
                {
                    "pre": "and 1 + 8 + 15 = ",
                    "post": "",
                    "answer": 24,
                    "done": "Both give 24, so (x + 3)(x + 5) is right.",
                    "hint": "Put x = 1 into x² + 8x + 15."
                }
            ]
        },
        "gold": {
            "display": "Factorise \\(9x^2 - 16\\)",
            "label": "Together: the gold move",
            "steps": [
                {
                    "say": "Two square terms with a minus between them: this is a difference of two squares. Square-root each term.",
                    "pre": "√(9x²) = ",
                    "post": "x",
                    "answer": 3,
                    "hint": "√9 = 3 and √(x²) = x."
                },
                {
                    "pre": "√16 = ",
                    "post": "",
                    "answer": 4,
                    "hint": "What number squares to 16?"
                },
                {
                    "say": "So \\(9x^2 - 16 = (3x + 4)(3x - 4)\\). Check with x = 1.",
                    "pre": "(3 + 4)(3 − 4) = 7 × (−1) = ",
                    "post": "",
                    "answer": -7,
                    "hint": "Work out each bracket at x = 1, then multiply."
                },
                {
                    "pre": "and 9 × 1 − 16 = ",
                    "post": "",
                    "answer": -7,
                    "done": "Both give −7, so (3x + 4)(3x − 4) is right.",
                    "hint": "Put x = 1 into 9x² − 16."
                }
            ]
        }
    }
}

# ---- tier descriptions ----
pb["bronze_description"] = "Common factor: find the highest common factor of every term and take it outside a single bracket."
pb["silver_description"] = "Quadratic trinomials x² + bx + c: find two numbers that multiply to c and add to b, giving two brackets."
pb["gold_description"] = "Harder factorising: difference of two squares, perfect squares, and taking out a common factor first. Factorise fully."

# ---- tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: common factor",
        "steps": [
            "Factorising reverses expanding. For a single bracket, find the <strong>highest common factor</strong> (HCF) of every term and write it outside.",
            "Divide each term by the HCF to get what goes inside: \\(6x + 15 = 3(2x + 5)\\) because \\(6x ÷ 3 = 2x\\) and \\(15 ÷ 3 = 5\\).",
            "Take out letters too. If every term has an \\(x\\), the HCF includes \\(x\\): \\(5x^2 + 15x = 5x(x + 3)\\). Check by expanding back."
        ],
        "example": {
            "question": "Factorise \\(8x - 12\\)",
            "steps": [
                {"label": "Find the HCF", "content": "<p>HCF of \\(8x\\) and \\(12\\) is \\(4\\)</p>"},
                {"label": "Divide each term", "content": "<p>\\(8x ÷ 4 = 2x\\), \\(12 ÷ 4 = 3\\)</p>"},
                {"label": "Check by expanding", "content": "<p>\\(4(2x - 3) = 8x - 12\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(4(2x - 3)\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: quadratic trinomials",
        "steps": [
            "For \\(x^2 + bx + c\\), find two numbers that <strong>multiply to \\(c\\)</strong> and <strong>add to \\(b\\)</strong>. They become the numbers in the two brackets.",
            "Watch the signs. If \\(c\\) is positive, both numbers share \\(b\\)'s sign; if \\(c\\) is negative, one is positive and one is negative.",
            "Write \\((x + p)(x + q)\\) with your two numbers, then expand to check the middle term."
        ],
        "example": {
            "question": "Factorise \\(x^2 - 5x + 6\\)",
            "steps": [
                {"label": "Multiply to 6, add to −5", "content": "<p>\\(-2\\) and \\(-3\\): \\(-2 × -3 = 6\\), \\(-2 + -3 = -5\\)</p>"},
                {"label": "Write the brackets", "content": "<p>\\((x - 2)(x - 3)\\)</p>"},
                {"label": "Check the middle", "content": "<p>\\(-2x - 3x = -5x\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\((x - 2)(x - 3)\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: DOTS, squares and factor first",
        "steps": [
            "<strong>Difference of two squares:</strong> \\(a^2 - b^2 = (a + b)(a - b)\\). Square-root each term: \\(4x^2 - 25 = (2x + 5)(2x - 5)\\).",
            "Always take out a <strong>common factor first</strong>, then keep going: \\(3x^2 - 12 = 3(x^2 - 4) = 3(x + 2)(x - 2)\\).",
            "A perfect square has a middle term: \\(x^2 - 10x + 25 = (x - 5)^2\\). Check the number doubled gives the middle term."
        ],
        "example": {
            "question": "Factorise completely \\(2x^3 - 18x\\)",
            "steps": [
                {"label": "Take out the common factor", "content": "<p>\\(2x(x^2 - 9)\\)</p>"},
                {"label": "Difference of two squares", "content": "<p>\\(x^2 - 9 = (x + 3)(x - 3)\\)</p>"},
                {"label": "Check by expanding", "content": "<p>\\(2x(x + 3)(x - 3) = 2x^3 - 18x\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(2x(x + 3)(x - 3)\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---- hints + reshaped misconceptions (expect = original option index) ----
NOTE = "expect = original option index of this distractor"

def setp(tier, idx, hint, misc):
    p = pb[tier][idx]
    p["hint"] = hint
    p["misconceptions"] = [dict(pattern=pat, expect=exp, message=msg, note=NOTE) for (pat, exp, msg) in misc]

# GOLD
setp("gold", 0, "Difference of two squares: square-root each term to get 2x and 5.", [
    ("same_sign", 3, "(2x−5)² gives 4x²−20x+25, which has an extra −20x term. A difference of two squares needs one plus and one minus bracket: (2x+5)(2x−5)."),
    ("mismatched_roots", 2, "(2x+25)(2x−1) mixes up the square roots. √(4x²)=2x and √25=5, so it is (2x+5)(2x−5)."),
])
setp("gold", 1, "This is a perfect square: the number is −5, so it is (x − 5) squared.", [
    ("wrong_sign", 1, "(x+5)² gives +10x in the middle, but the expression has −10x. The number is −5: (x−5)²."),
    ("used_dots", 2, "(x−5)(x+5) is x²−25 with no middle term. The −10x here means it is the perfect square (x−5)²."),
])
setp("gold", 2, "Take out 3 first, then factorise the difference of two squares.", [
    ("stopped_early", 1, "3(x²−4) is only half done. x²−4 is a difference of two squares, so factorise again: 3(x+2)(x−2)."),
    ("hidden_factor", 2, "(3x+6)(x−2) still hides a common factor of 3 inside the first bracket. Take it fully outside: 3(x+2)(x−2)."),
    ("wrong_signs", 3, "3(x−2)² expands to 3x²−12x+12, not 3x²−12. Use one plus and one minus: 3(x+2)(x−2)."),
])
setp("gold", 3, "Group x²−6x+9 as a perfect square, then use the difference of two squares with y.", [
    ("stopped_early", 1, "(x−3)²−y² is not finished. It is a difference of two squares, so factorise: (x−3+y)(x−3−y)."),
    ("wrong_grouping", 3, "(x−3)(x−3−y) expands wrongly. Group x²−6x+9 as (x−3)², then apply the difference of two squares with y: (x−3+y)(x−3−y)."),
])
setp("gold", 4, "Take out 2x first, then factorise the difference of two squares.", [
    ("stopped_early", 1, "2x(x²−9) stops too early. x²−9 is a difference of two squares: 2x(x+3)(x−3)."),
    ("partial_factor", 2, "x(2x²−18) misses part of the common factor. The HCF is 2x, and 2x²−18 factorises further: 2x(x+3)(x−3)."),
    ("hidden_factor", 3, "2(x³−9x) still has an x in every bracket term. Take out 2x, then use the difference of two squares: 2x(x+3)(x−3)."),
])

# BRONZE
setp("bronze", 0, "The highest common factor of 3x and 9 is 3.", [
    ("wrong_hcf", 1, "9(x+1) expands to 9x+9, not 3x+9. The highest common factor of 3x and 9 is 3: 3(x+3)."),
    ("bad_divide", 2, "3(x+9) expands to 3x+27. After dividing, 9÷3=3, so the bracket is (x+3)."),
    ("wrong_letter", 3, "x(3+9) treats x as the common factor, but 9 has no x in it. The common factor is 3: 3(x+3)."),
])
setp("bronze", 1, "Both terms divide by 4, so take out 4.", [
    ("partial_factor", 1, "2(4x−6) is not fully factorised: 4x−6 still shares a factor of 2. The full HCF is 4: 4(2x−3)."),
    ("wrong_hcf", 2, "8(x−4) expands to 8x−32, not 8x−12. 8 does not divide 12, so the HCF is 4: 4(2x−3)."),
    ("sign_error", 3, "4(2x+3) expands to 8x+12. The −12 keeps its minus sign, so it is 4(2x−3)."),
])
setp("bronze", 2, "Both terms share a 5 and an x, so the factor is 5x.", [
    ("missed_letter", 1, "5(x²+3x) still has an x in both bracket terms. The HCF is 5x, not just 5: 5x(x+3)."),
    ("missed_number", 2, "x(5x+15) still has a factor of 5 inside. The HCF is 5x: 5x(x+3)."),
    ("bad_divide", 3, "5x(x+15) is wrong: 15x÷5x=3, not 15. The bracket is (x+3)."),
])
setp("bronze", 3, "Both terms share a 3 and a y, so the factor is 3y.", [
    ("missed_letter", 1, "3(2xy+3y) still has a y in both terms. Take out the full HCF 3y: 3y(2x+3)."),
    ("wrong_hcf", 2, "6y(x+9) expands to 6xy+54y, not 6xy+9y. The HCF of 6xy and 9y is 3y: 3y(2x+3)."),
    ("missed_number", 3, "y(6x+9) still has a factor of 3 inside. The HCF is 3y: 3y(2x+3)."),
])
setp("bronze", 4, "Both terms share an x, so take out x.", [
    ("not_factorised", 1, "5(x+x) simplifies to 10x, not x²+5x. The common factor is x: x(x+5)."),
    ("over_factored", 2, "x²(1+5) simplifies to 6x², not x²+5x. Only one x is common to both terms: x(x+5)."),
    ("extra_x", 3, "x(x+5x) has an extra x that should not be there: 5x÷x=5, so the bracket is (x+5)."),
])
setp("bronze", 5, "Both terms divide by 4 and share an x, so take out 4x.", [
    ("missed_letter", 1, "4(3x²−2x) still has an x in both terms. The HCF is 4x: 4x(3x−2)."),
    ("partial_factor", 2, "2x(6x−4) is not fully factorised: 6x−4 shares a factor of 2. The full HCF is 4x: 4x(3x−2)."),
    ("sign_error", 3, "4x(3x+2) expands to 12x²+8x. The −8x keeps its minus, so it is 4x(3x−2)."),
])
setp("bronze", 6, "No middle term and a minus: use the difference of two squares.", [
    ("wrong_method", 3, "x(x−4) expands to x²−4x, not x²−4. There is no middle term, so use the difference of two squares: (x+2)(x−2)."),
    ("wrong_pair", 1, "(x−4)(x+1) expands to x²−3x−4. x²−4 is a difference of two squares: x²−2²=(x+2)(x−2)."),
])
setp("bronze", 7, "No middle term and a minus: use the difference of two squares.", [
    ("wrong_method", 3, "x(x−16) expands to x²−16x, not x²−16. Use the difference of two squares: x²−4²=(x+4)(x−4)."),
    ("wrong_pair", 1, "(x−8)(x+2) expands to x²−6x−16. Here there is no middle term: x²−16=(x+4)(x−4)."),
])

# SILVER
setp("silver", 0, "Find two numbers that multiply to 12 and add to 7.", [
    ("wrong_pair", 1, "(x+2)(x+6) gives 2+6=8 in the middle, but we need 7. The pair is 3 and 4: (x+3)(x+4)."),
    ("wrong_pair_alt", 3, "(x+6)(x+2) also adds to 8, not 7. Two numbers that multiply to 12 and add to 7 are 3 and 4."),
])
setp("silver", 1, "Find two numbers that multiply to 6 and add to −5; both are negative.", [
    ("sign_error", 1, "(x+2)(x−3) gives a constant of −6, but we need +6. Both numbers are negative: (x−2)(x−3)."),
    ("both_positive", 3, "(x+2)(x+3) gives +5x in the middle. We need −5x, so both numbers are negative: (x−2)(x−3)."),
    ("wrong_pair", 2, "(x−1)(x−6) adds to −7, not −5. The pair is −2 and −3: (x−2)(x−3)."),
])
setp("silver", 2, "Find two numbers that multiply to −15 and add to 2.", [
    ("swapped_signs", 1, "(x−5)(x+3) gives −2x in the middle. Swap the signs so the +5 goes with the larger number: (x+5)(x−3)."),
    ("both_positive", 3, "(x+5)(x+3) gives +15, but we need −15. One number must be negative: (x+5)(x−3)."),
    ("wrong_pair", 2, "(x+15)(x−1) multiplies to −15 but adds to +14, not +2. The pair is +5 and −3."),
])
setp("silver", 3, "Find two numbers that multiply to −20 and add to −1.", [
    ("swapped_signs", 1, "(x+5)(x−4) gives +x in the middle. We need −x, so the larger number is negative: (x−5)(x+4)."),
    ("both_negative", 3, "(x−5)(x−4) gives +20, but we need −20. One number must be positive: (x−5)(x+4)."),
    ("wrong_pair", 2, "(x−10)(x+2) multiplies to −20 but adds to −8, not −1. The pair is −5 and +4."),
])
setp("silver", 4, "No middle term: use the difference of two squares with √81 = 9.", [
    ("used_square", 3, "(x−9)² gives −18x in the middle. A difference of two squares has no middle term: (x+9)(x−9)."),
    ("wrong_root", 1, "(x−81)(x+1) expands to x²−80x−81. 81 is 9², so x²−81=(x+9)(x−9)."),
    ("wrong_pair", 2, "(x+3)(x−27) is not a difference of two squares. √81=9, so x²−81=(x+9)(x−9)."),
])
setp("silver", 5, "Find two numbers that multiply to −28 and add to 3.", [
    ("swapped_signs", 1, "(x−7)(x+4) gives −3x in the middle. We need +3x, so the 7 is positive: (x+7)(x−4)."),
    ("both_positive", 3, "(x+7)(x+4) gives +28, but we need −28. One number must be negative: (x+7)(x−4)."),
    ("wrong_pair", 2, "(x+14)(x−2) multiplies to −28 but adds to +12, not +3. The pair is +7 and −4."),
])
setp("silver", 6, "Take out the common factor 2 first, then factorise the trinomial.", [
    ("hidden_factor", 1, "(2x+4)(x+3) still hides a factor of 2 in the first bracket. Take out the 2 first: 2(x+2)(x+3)."),
    ("hidden_factor_alt", 3, "(x+2)(2x+6) still has a factor of 2 in the second bracket. Take out the 2 first: 2(x+2)(x+3)."),
    ("wrong_pair", 2, "2(x+6)(x+1) expands to 2x²+14x+12, not 2x²+10x+12. After taking out 2, factorise x²+5x+6 as (x+2)(x+3)."),
])

# ---- fix em dash in preserved method_card step (style law) ----
pd["method_card"]["steps"] = [s.replace(" — ", ": ") for s in pd["method_card"]["steps"]]

# ---- slim method_card content ----
pd["method_card"]["content"] = ("<p><strong>Factorising</strong> is the reverse of expanding: write an expression as a "
    "product of factors.</p><p><strong>Common factor:</strong> take the highest common factor of every term "
    "outside a bracket. \\(6x + 15 = 3(2x + 5)\\).</p><p><strong>Quadratic</strong> \\(x^2 + bx + c\\): two "
    "numbers that multiply to \\(c\\) and add to \\(b\\). \\(x^2 + 7x + 12 = (x + 3)(x + 4)\\).</p>"
    "<p><strong>Difference of two squares:</strong> \\(a^2 - b^2 = (a + b)(a - b)\\), so "
    "\\(x^2 - 25 = (x + 5)(x - 5)\\). Always factorise fully.</p>")

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT)
# quick self-checks
assert "—" not in json.dumps(pd, ensure_ascii=False), "EM DASH present"
print("no em dash; problems:", {t: len(pb[t]) for t in ('bronze','silver','gold')})
