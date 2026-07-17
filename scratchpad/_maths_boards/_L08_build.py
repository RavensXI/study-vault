# -*- coding: utf-8 -*-
import json

MINUS = "−"  # unicode minus (never em dash)

pd = json.load(open("_L08_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---------------------------------------------------------------
# 1. HINTS (plain text, one sentence, method move) for every bank problem
# ---------------------------------------------------------------
bronze_hints = [
    "Add the tops and add the bottoms: 2+3 and 5+(−1).",
    "Subtract component by component: 4−1 and −3−2.",
    "Multiply both components by 3.",
    "The minus in front flips the sign of both components.",
    "Add tops to tops and bottoms to bottoms; a zero leaves the other number unchanged.",
    "Double the first vector first, then add the second.",
    "Reverse means negate: B to A is the negative of A to B.",
    "Add the components; opposite vectors cancel to zero.",
]
silver_hints = [
    "Magnitude = √(3² + 4²).",
    "Magnitude = √((−6)² + 8²); the squares are positive.",
    "AB = OB − OA = b − a.",
    "Midpoint: add the two position vectors and halve.",
    "Parallel means a scalar multiple: do the components scale by the same factor?",
    "Multiply the whole vector by one third.",
    "A unit vector has magnitude exactly 1; test each with √(x² + y²).",
]
gold_hints = [
    "P is 2/3 of the way from A to B: OP = a + ⅔(b − a).",
    "OM = ½(OA + OB), then factor out to compare with a + 2b.",
    "A scalar multiple means the same direction.",
    "AC = OC − OA.",
    "Work out 2a − b first, then take its magnitude.",
]
for i, h in enumerate(bronze_hints): pb["bronze"][i]["hint"] = h
for i, h in enumerate(silver_hints): pb["silver"][i]["hint"] = h
for i, h in enumerate(gold_hints):   pb["gold"][i]["hint"] = h

# ---------------------------------------------------------------
# 2. FIX defective options (fresh-solve repairs)
# ---------------------------------------------------------------
# gold[1]: option[2] "(3/2)a+3b" duplicates the correct answer -> replace
pb["gold"][1]["options"][2] = "\\(\\frac{3}{2}\\mathbf{a} + 6\\mathbf{b}\\)"
# gold[3]: option[1] "2a+b-a" (= a+b) duplicates correct -> replace
pb["gold"][3]["options"][1] = "\\(2\\mathbf{a} + \\mathbf{b}\\)"
# gold[4]: correct answer sqrt(26) was at index 1 but solutions marked index 0 ("5").
#          Reorder so the correct answer is index 0 (house convention), keep solutions [0].
pb["gold"][4]["options"] = ["\\(\\sqrt{26}\\)", "5", "\\(\\sqrt{10}\\)", "\\(\\sqrt{5}\\)"]

# ---------------------------------------------------------------
# 3. MISCONCEPTIONS (expect = option index of the distractor produced)
# ---------------------------------------------------------------
def M(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

pb["bronze"][0]["misconceptions"] = [
    M("subtracted", 1, "This is addition, so add each component: (2+3, 5+(−1)) = (5, 4). Subtracting gives (−1, 6)."),
    M("sign_y", 2, "The y-parts add: 5 + (−1) = 4, not −4."),
]
pb["bronze"][1]["misconceptions"] = [
    M("added", 1, "This is subtraction: (4−1, −3−2) = (3, −5). Adding gives (5, −1)."),
    M("reversed", 3, "Subtract the second from the first, not the other way round: (4−1, −3−2) = (3, −5)."),
]
pb["bronze"][2]["misconceptions"] = [
    M("added_scalar", 1, "Multiply, do not add: 3 × 2 = 6 and 3 × (−4) = −12."),
    M("sign", 2, "3 × (−4) = −12, not +12."),
]
pb["bronze"][3]["misconceptions"] = [
    M("only_x", 2, "Negate both parts: the y also flips, −2 becomes +2, giving (−5, 2)."),
    M("swapped", 3, "Negate each part in place, do not swap them: (−5, 2)."),
]
pb["bronze"][4]["misconceptions"] = [
    M("sign_x", 1, "0 + (−3) = −3, so the x-part is negative: (−3, 7)."),
    M("swapped", 3, "Add tops to tops and bottoms to bottoms; do not swap the components."),
]
pb["bronze"][5]["misconceptions"] = [
    M("forgot_scalar", 1, "Double the first vector: 2 × (1, 3) = (2, 6), then add (4, −1) to get (6, 5)."),
    M("sign_y", 3, "The y-part is 2×3 + (−1) = 6 − 1 = 5, not −5."),
]
pb["bronze"][6]["misconceptions"] = [
    M("same", 1, "Reversing direction negates the vector: B to A = −(3, 4) = (−3, −4)."),
    M("swapped", 3, "Change the sign of each part in place, do not swap them: (−3, −4)."),
]
pb["bronze"][7]["misconceptions"] = [
    M("subtracted", 1, "Add the components: (−1+1, 6+(−6)) = (0, 0). These vectors are opposites."),
    M("dropped_sign", 3, "The second y is −6, so 6 + (−6) = 0, not 12."),
]

pb["silver"][0]["misconceptions"] = [
    M("added", 1, "Use Pythagoras: √(3² + 4²) = √25 = 5. Adding 3 + 4 gives 7."),
    M("forgot_root", 3, "25 is the magnitude squared. Take the square root: √25 = 5."),
]
pb["silver"][1]["misconceptions"] = [
    M("added", 1, "√((−6)² + 8²) = √100 = 10. Adding 6 + 8 gives 14."),
    M("forgot_root", 3, "100 is the square. The magnitude is √100 = 10."),
]
pb["silver"][2]["misconceptions"] = [
    M("added", 1, "AB = OB − OA = b − a. Do not add the position vectors."),
    M("reversed", 2, "a − b is the reverse (BA). From A to B: −a + b = b − a."),
]
pb["silver"][3]["misconceptions"] = [
    M("forgot_half", 1, "Halve the sum: ½(10, 8) = (5, 4). (10, 8) is OA + OB before halving."),
    M("subtracted", 2, "Add the position vectors then halve; do not subtract them."),
]
pb["silver"][4]["misconceptions"] = [
    M("swapped", 1, "(6, 4) swaps the components; it is not a multiple of (4, 6). But (2, 3) = ½(4, 6)."),
    M("sign", 2, "(4, −6) flips the y-sign, so it is not a multiple of (4, 6)."),
]
pb["silver"][5]["misconceptions"] = [
    M("multiplied", 1, "Multiply by one third, not by 3: ⅓(6, −2) = (2, −2/3)."),
    M("partial", 2, "Scale both parts: ⅓ × (−2) = −2/3, not −2."),
]
pb["silver"][6]["misconceptions"] = [
    M("ones", 1, "|(1, 1)| = √2 ≈ 1.41, not 1. |(0.6, 0.8)| = √(0.36 + 0.64) = 1."),
    M("integer", 3, "|(3, 4)| = 5, not 1. A unit vector has length exactly 1."),
]

pb["gold"][0]["misconceptions"] = [
    M("reversed_ratio", 1, "2:1 means P is 2/3 of the way from A, so OP = a + ⅔(b − a) = ⅓a + ⅔b."),
    M("raw_coeffs", 3, "Do not use 2 and 1 as coefficients. Split AB: OP = a + ⅔(b − a)."),
]
pb["gold"][1]["misconceptions"] = [
    M("forgot_half", 1, "OM is the midpoint vector ½(3a + 6b). 3a + 6b is OA + OB, not halved."),
    M("partial_half", 2, "Halve both terms: ½(3a + 6b) = (3/2)a + 3b = (3/2)(a + 2b)."),
]
pb["gold"][2]["misconceptions"] = [
    M("equal", 1, "A scalar multiple gives the same direction (parallel), not the same length unless k = 1."),
    M("collinear", 2, "Parallel, yes. Collinear also needs a shared point, which is not given."),
]
pb["gold"][3]["misconceptions"] = [
    M("forgot_subtract", 1, "AC = OC − OA. Subtract a: (2a + b) − a = a + b. 2a + b is just OC."),
    M("added", 2, "AC = OC − OA, so subtract. Adding gives (2a + b) + a = 3a + b."),
]
pb["gold"][4]["misconceptions"] = [
    M("one_component", 1, "Find the full magnitude: |(−1, 5)| = √(1 + 25) = √26. 5 alone ignores the x-part."),
    M("wrong_vector", 3, "Work out 2a − b = (−1, 5) first, then √26. √5 is only |a|."),
]

# ---------------------------------------------------------------
# 4. tier_guides
# ---------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: adding, subtracting and scaling column vectors",
        "steps": [
            "A <strong>column vector</strong> \\(\\binom{x}{y}\\) means move x across and y up. Add or subtract two vectors component by component: tops with tops, bottoms with bottoms.",
            "To <strong>scalar multiply</strong>, multiply both components: \\(k\\binom{x}{y} = \\binom{kx}{ky}\\). A minus in front flips both signs.",
            "Reversing a vector's direction negates both parts: B to A is the negative of A to B.",
        ],
        "example": {
            "question": "Work out \\(\\binom{5}{2} - \\binom{1}{4}\\).",
            "steps": [
                {"label": "Rule", "content": "<p>Subtract each component separately.</p>"},
                {"label": "Subtract", "content": "<p>\\(x = 5 - 1 = 4\\), \\(y = 2 - 4 = -2\\)</p>"},
                {"label": "Check", "content": "<p>Tops: 5 − 1 = 4. Bottoms: 2 − 4 = −2.</p>"},
                {"label": "Answer", "content": "<p><strong>\\(\\binom{4}{-2}\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: magnitude, paths and midpoints",
        "steps": [
            "The <strong>magnitude</strong> (length) uses Pythagoras: \\(|\\binom{x}{y}| = \\sqrt{x^2 + y^2}\\).",
            "For a <strong>path</strong>, travel along known vectors: \\(\\overrightarrow{AB} = \\overrightarrow{OB} - \\overrightarrow{OA} = \\mathbf{b} - \\mathbf{a}\\).",
            "The <strong>midpoint</strong> M of AB has \\(\\overrightarrow{OM} = \\tfrac{1}{2}(\\overrightarrow{OA} + \\overrightarrow{OB})\\).",
        ],
        "example": {
            "question": "Find the magnitude of \\(\\binom{5}{12}\\).",
            "steps": [
                {"label": "Formula", "content": "<p>\\(\\sqrt{5^2 + 12^2} = \\sqrt{25 + 144} = \\sqrt{169}\\)</p>"},
                {"label": "Check", "content": "<p>\\(13 \\times 13 = 169\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>13</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: parallel vectors, ratios and proofs",
        "steps": [
            "Two vectors are <strong>parallel</strong> when one is a scalar multiple of the other: \\(\\overrightarrow{AB} = k\\,\\overrightarrow{CD}\\).",
            "To divide AB in the ratio \\(m:n\\) at P, go a fraction \\(\\frac{m}{m+n}\\) along from A: \\(\\overrightarrow{OP} = \\mathbf{a} + \\frac{m}{m+n}(\\mathbf{b} - \\mathbf{a})\\).",
            "In a proof, write the target as a single multiple of the given expression to show it is parallel.",
        ],
        "example": {
            "question": "OA = a, OB = b. M is the midpoint of AB. Find OM.",
            "steps": [
                {"label": "Path", "content": "<p>\\(\\overrightarrow{AB} = \\mathbf{b} - \\mathbf{a}\\), so \\(\\overrightarrow{OM} = \\mathbf{a} + \\tfrac{1}{2}(\\mathbf{b} - \\mathbf{a})\\)</p>"},
                {"label": "Simplify", "content": "<p>\\(= \\tfrac{1}{2}\\mathbf{a} + \\tfrac{1}{2}\\mathbf{b}\\)</p>"},
                {"label": "Answer", "content": "<p><strong>\\(\\tfrac{1}{2}(\\mathbf{a} + \\mathbf{b})\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------
# 5. guided.opener  (concrete drone-on-a-grid hook)
# ---------------------------------------------------------------
def grid_svg():
    ox, oy, u = 20, 156, 24          # origin px and unit size
    def X(gx): return ox + u * gx
    def Y(gy): return oy - u * gy
    parts = ["<svg viewBox='0 0 184 176' role=\"img\" aria-label=\"A grid. A drone at (0,0) flies 3 right and 2 up, then 1 right and 4 up, ending at (4,6)\" style='max-width:220px;width:100%;height:auto;font-family:Inter,sans-serif'>"]
    for gx in range(7):
        parts.append(f"<line x1='{X(gx)}' y1='{Y(0)}' x2='{X(gx)}' y2='{Y(6)}' stroke='currentColor' stroke-opacity='0.12' stroke-width='1'/>")
    for gy in range(7):
        parts.append(f"<line x1='{X(0)}' y1='{Y(gy)}' x2='{X(6)}' y2='{Y(gy)}' stroke='currentColor' stroke-opacity='0.12' stroke-width='1'/>")
    # axes emphasised
    parts.append(f"<line x1='{X(0)}' y1='{Y(0)}' x2='{X(6)}' y2='{Y(0)}' stroke='currentColor' stroke-width='1.4'/>")
    parts.append(f"<line x1='{X(0)}' y1='{Y(0)}' x2='{X(0)}' y2='{Y(6)}' stroke='currentColor' stroke-width='1.4'/>")
    # flight 1: (0,0)->(3,2)
    parts.append(f"<line x1='{X(0)}' y1='{Y(0)}' x2='{X(3)}' y2='{Y(2)}' stroke='#3b82f6' stroke-width='2'/>")
    parts.append(f"<circle cx='{X(3)}' cy='{Y(2)}' r='3.2' fill='#3b82f6'/>")
    # flight 2: (3,2)->(4,6)
    parts.append(f"<line x1='{X(3)}' y1='{Y(2)}' x2='{X(4)}' y2='{Y(6)}' stroke='#f59e0b' stroke-width='2'/>")
    parts.append(f"<circle cx='{X(4)}' cy='{Y(6)}' r='3.2' fill='#f59e0b'/>")
    # start marker
    parts.append(f"<circle cx='{X(0)}' cy='{Y(0)}' r='3.2' fill='currentColor'/>")
    parts.append(f"<text x='{X(0)+4}' y='{Y(0)+13}' fill='currentColor' font-size='10'>start</text>")
    parts.append(f"<text x='{X(4)+4}' y='{Y(6)+4}' fill='currentColor' font-size='10'>end?</text>")
    parts.append("</svg>")
    return "".join(parts)

pd["guided"] = {
    "opener": {
        "label": "Before any notation",
        "display": grid_svg() + "A drone at the corner flies <strong>3 right and 2 up</strong> (blue), then <strong>1 right and 4 up</strong> (orange). Where does it finish?",
        "steps": [
            {"say": "Two moves, one journey. Just total up each direction on its own."},
            {"pre": "Total moved right: 3 + 1 = ", "post": "", "answer": 4,
             "hint": "Add the two rightward amounts."},
            {"pre": "Total moved up: 2 + 4 = ", "post": "", "answer": 6,
             "hint": "Add the two upward amounts.",
             "done": "So the drone finishes 4 right and 6 up: the point (4, 6)."},
            {"say": "You just added two vectors: \\(\\binom{3}{2} + \\binom{1}{4} = \\binom{4}{6}\\). Adding column vectors means adding the acrosses and adding the ups, exactly what you did by common sense."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Work out \\(2\\binom{3}{-1} + \\binom{-4}{5}\\).",
            "steps": [
                {"say": "Deal with the scalar first: multiply <strong>both</strong> parts of the first vector by 2."},
                {"pre": "2 × 3 = ", "answer": 6, "hint": "Multiply the top of the first vector by 2."},
                {"pre": "2 × (−1) = ", "answer": -2, "hint": "Multiply the bottom by 2; keep the sign.",
                 "done": "So 2 times (3, −1) is (6, −2). The scalar hit both parts."},
                {"say": "Now add \\(\\binom{-4}{5}\\), tops to tops and bottoms to bottoms."},
                {"pre": "Top: 6 + (−4) = ", "answer": 2, "hint": "Add the two top numbers."},
                {"pre": "Bottom: −2 + 5 = ", "answer": 3, "hint": "Add the two bottom numbers.",
                 "done": "The result is (2, 3)."},
                {"say": "Check: (6, −2) + (−4, 5) = (2, 3). Nose to tail lands at (2, 3). Gone. That was the whole point."},
            ],
        },
        "silver": {
            "display": "Find the magnitude of \\(\\binom{8}{-6}\\).",
            "steps": [
                {"say": "Magnitude is the length: \\(|\\binom{x}{y}| = \\sqrt{x^2 + y^2}\\). Square each part, add, then root."},
                {"pre": "8² = ", "answer": 64, "hint": "Eight squared."},
                {"pre": "(−6)² = ", "answer": 36, "hint": "A negative squared is positive: (−6) × (−6)."},
                {"pre": "Add the squares: 64 + 36 = ", "answer": 100, "hint": "Add your two results."},
                {"pre": "√100 = ", "answer": 10, "hint": "What number times itself gives 100?",
                 "done": "So the length is 10."},
                {"say": "Check: \\(\\sqrt{64 + 36} = \\sqrt{100} = 10\\). The negative sign vanished when we squared. Gone."},
            ],
        },
        "gold": {
            "display": "\\(\\overrightarrow{OA} = \\mathbf{a}\\), \\(\\overrightarrow{OB} = \\mathbf{b}\\). P divides AB in the ratio 3:1. Find \\(\\overrightarrow{OP}\\).",
            "steps": [
                {"say": "P sits on AB. First find how far along AB it is. The ratio 3:1 splits AB into 3 + 1 parts."},
                {"pre": "Total parts: 3 + 1 = ", "answer": 4, "hint": "Add the two ratio numbers."},
                {"pre": "Fraction of AB from A: 3 ÷ 4 = ", "answer": 0.75, "hint": "Divide the first ratio number by the total.",
                 "done": "So P is 0.75 of the way from A to B."},
                {"say": "\\(\\overrightarrow{OP} = \\mathbf{a} + 0.75(\\mathbf{b} - \\mathbf{a}) = \\mathbf{a} + 0.75\\mathbf{b} - 0.75\\mathbf{a}\\). Collect the a terms."},
                {"pre": "Coefficient of a: 1 − 0.75 = ", "answer": 0.25, "hint": "One whole a minus 0.75 of a."},
                {"pre": "Coefficient of b (from 0.75b): ", "answer": 0.75, "hint": "The b term is 0.75b.",
                 "done": "So OP = 0.25a + 0.75b, that is ¼a + ¾b."},
                {"say": "Check: at A the fraction is 0 (OP = a); at B it is 1 (OP = b). 0.75 lands three quarters along, nearer B. Gone."},
            ],
        },
    },
}

# ---------------------------------------------------------------
# 6. Style fix: strip em dashes from preserved worked_examples labels
#    (validator-enforced; " — " -> ": ")
# ---------------------------------------------------------------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, open("lesson_maths-eduqas_geometry-L08.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_maths-eduqas_geometry-L08.json")
