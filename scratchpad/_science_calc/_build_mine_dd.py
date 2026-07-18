# -*- coding: utf-8 -*-
"""Build guided practice_data for chemistry-calculations-L01@dd9dbc80e5
(Relative Formula Mass and Moles). Loads canonical, augments in place."""
import json, io

pd = json.load(io.open("_mine_dd_canonical.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---- helper to fix em dashes in preserved fields ----
def fix_dashes(o):
    if isinstance(o, dict):
        return {k: fix_dashes(v) for k, v in o.items()}
    if isinstance(o, list):
        return [fix_dashes(v) for v in o]
    if isinstance(o, str):
        return o.replace(" — ", ": ").replace("—", ":")
    return o

# fix worked_examples labels + exam_context (preserved otherwise)
pd["worked_examples"] = fix_dashes(pd["worked_examples"])
pd["exam_context"]["frequency"] = "Every exam: Mr and moles appear on every Paper 1"

# ---------------- method_card (slim) ----------------
pd["method_card"] = {
    "title": "Relative Formula Mass and Moles",
    "steps": [
        "Write the formula and count every atom, watching subscripts and brackets.",
        "Add the Ar values to get Mr (Mr has no unit).",
        "For amount, use moles = mass ÷ Mr, and rearrange it for mass or Mr.",
        "State the answer with its unit: mol, g, or %.",
    ],
    "content": (
        "<p>\\(M_r\\) is the sum of the \\(A_r\\) of every atom in the formula. "
        "A subscript multiplies the atom before it, and a bracket multiplies "
        "everything inside it.</p>"
        "<p>Amount links to mass through \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\), "
        "which rearranges to \\(\\text{mass} = \\text{moles} \\times M_r\\) or "
        "\\(M_r = \\dfrac{\\text{mass}}{\\text{moles}}\\).</p>"
        "<p>Percentage by mass of an element is \\(\\dfrac{\\text{its mass in the formula}}{M_r} \\times 100\\).</p>"
    ),
}

# ---------------- tier descriptions ----------------
pb["bronze_description"] = ("One equation with the numbers ready: add up an Mr, or put mass "
                            "and Mr straight into moles = mass ÷ Mr.")
pb["silver_description"] = ("Handle a bracket in the formula, or build the Mr yourself before "
                            "finding moles or mass.")
pb["gold_description"] = ("Chain two steps: work out an Mr then a percentage by mass, or rearrange "
                          "to find an Mr from a measured mass and amount.")

# ---------------- hints + guided_steps + expects, per problem ----------------
# order-indexed data
BRONZE = {
    0: dict(hint="Add the two Ar values: 23 + 35.5.",
        expects={"wrong_ar": None},
        steps=[
            {"say": "The rule is \\(M_r = \\) the sum of the \\(A_r\\) of every atom. NaCl has one sodium and one chlorine."},
            {"pre": "Sodium: 1 × 23 = ", "post": "", "answer": 23, "hint": "One sodium atom, Ar 23."},
            {"phase": "substitute", "pre": "Chlorine: 1 × 35.5 = ", "post": "", "answer": 35.5, "hint": "One chlorine atom, Ar 35.5."},
            {"pre": "Add the two: 23 + 35.5 = ", "post": "", "answer": 58.5, "done": "Mr = 58.5. Relative formula mass has no unit.", "hint": "Add your two contributions."},
        ]),
    1: dict(hint="Two hydrogens: 2 × 1, then add the oxygen.",
        expects={"forgot_subscript": 17},
        steps=[
            {"say": "\\(M_r\\) sums every atom's \\(A_r\\). H₂O has two hydrogens and one oxygen."},
            {"pre": "Oxygen: 1 × 16 = ", "post": "", "answer": 16, "hint": "One oxygen atom, Ar 16."},
            {"phase": "substitute", "pre": "Hydrogen: the small 2 means 2 × 1 = ", "post": "", "answer": 2, "hint": "The subscript 2 doubles the hydrogen."},
            {"pre": "Add them: 16 + 2 = ", "post": "", "answer": 18, "done": "Mr = 18, no unit.", "hint": "Add the two contributions."},
        ]),
    2: dict(hint="Two oxygens: 12 + 2 × 16.",
        expects={"forgot_subscript": 28},
        steps=[
            {"say": "\\(M_r\\) sums every atom. CO₂ is one carbon and two oxygens."},
            {"pre": "Carbon: 1 × 12 = ", "post": "", "answer": 12, "hint": "One carbon atom, Ar 12."},
            {"phase": "substitute", "pre": "Oxygen: the small 2 means 2 × 16 = ", "post": "", "answer": 32, "hint": "Two oxygen atoms, each Ar 16."},
            {"pre": "Add them: 12 + 32 = ", "post": "", "answer": 44, "done": "Mr = 44, no unit.", "hint": "Add the two contributions."},
        ]),
    3: dict(hint="Three oxygens: 40 + 12 + 3 × 16.",
        expects={"forgot_subscript": 68},
        steps=[
            {"say": "\\(M_r\\) sums every atom. CaCO₃ has one calcium, one carbon and three oxygens."},
            {"pre": "Calcium and carbon: 40 + 12 = ", "post": "", "answer": 52, "hint": "Add the single Ca and C first."},
            {"phase": "substitute", "pre": "Oxygen: the small 3 means 3 × 16 = ", "post": "", "answer": 48, "hint": "Three oxygen atoms, each Ar 16."},
            {"pre": "Add both parts: 52 + 48 = ", "post": "", "answer": 100, "done": "Mr = 100, no unit.", "hint": "Add the two parts."},
        ]),
    4: dict(hint="Divide mass by Mr: 36 ÷ 18.",
        expects={"inverted": 648},
        steps=[
            {"say": "The equation is \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\). Mass and Mr are already in the right units, so no conversion is needed."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 36, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide mass by Mr: 36 ÷ 18 = ", "post": "", "answer": 2, "hint": "Divide, do not multiply."},
            {"pre": "Check by reversing: 2 × 18 = ", "post": "", "answer": 36, "done": "It returns 36 g, so the amount is 2 mol.", "hint": "moles × Mr should give the mass back."},
        ]),
    5: dict(hint="Divide mass by Mr: 5.5 ÷ 44.",
        expects={"inverted": 242},
        steps=[
            {"say": "Use \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\). Both values are given in the right units."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 5.5, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide: 5.5 ÷ 44 = ", "post": "", "answer": 0.125, "hint": "Divide the mass by the Mr."},
            {"pre": "Check by reversing: 0.125 × 44 = ", "post": "", "answer": 5.5, "done": "It returns 5.5 g, so the amount is 0.125 mol.", "hint": "moles × Mr should give the mass back."},
        ]),
    6: dict(hint="Divide mass by Mr: 4.8 ÷ 40.",
        expects={"inverted": 192},
        steps=[
            {"say": "Use \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\)."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 4.8, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide: 4.8 ÷ 40 = ", "post": "", "answer": 0.12, "hint": "Divide the mass by the Mr."},
            {"pre": "Check by reversing: 0.12 × 40 = ", "post": "", "answer": 4.8, "done": "It returns 4.8 g, so the amount is 0.12 mol.", "hint": "moles × Mr should give the mass back."},
        ]),
    7: dict(hint="Multiply moles by Mr: 0.5 × 18.",
        expects={"divided": 36},
        steps=[
            {"say": "Rearrange to \\(\\text{mass} = \\text{moles} \\times M_r\\)."},
            {"pre": "Write the number of moles: ", "post": "", "answer": 0.5, "hint": "Read the amount from the question."},
            {"phase": "substitute", "pre": "Multiply moles by Mr: 0.5 × 18 = ", "post": "", "answer": 9, "hint": "Multiply, do not divide."},
            {"pre": "Check by reversing: 9 ÷ 18 = ", "post": "", "answer": 0.5, "done": "It returns 0.5 mol, so the mass is 9 g.", "hint": "mass ÷ Mr should give the moles back."},
        ]),
}

SILVER = {
    0: dict(hint="The bracket doubles OH: 40 + 2 × (16 + 1).",
        expects={"forgot_brackets": 57, "single_oh": None},
        steps=[
            {"say": "\\(M_r\\) sums every atom, and a bracket multiplies everything inside it. Ca(OH)₂ has one calcium and two OH groups."},
            {"pre": "Inside one bracket, O + H = 16 + 1 = ", "post": "", "answer": 17, "hint": "Add the oxygen and hydrogen inside the bracket."},
            {"phase": "substitute", "pre": "The small 2 doubles the whole bracket: 2 × 17 = ", "post": "", "answer": 34, "hint": "Multiply the bracket total by 2."},
            {"pre": "Add the calcium: 40 + 34 = ", "post": "", "answer": 74, "done": "Mr = 74, no unit.", "hint": "Add Ca to the doubled bracket."},
        ]),
    1: dict(hint="Double the whole NO₃ group: 24 + 2 × (14 + 3 × 16).",
        expects={"forgot_brackets": 86},
        steps=[
            {"say": "A bracket multiplies everything inside. Mg(NO₃)₂ has one magnesium and two NO₃ groups."},
            {"pre": "Inside one bracket, N + 3 × O = 14 + 48 = ", "post": "", "answer": 62, "hint": "One nitrogen plus three oxygens."},
            {"phase": "substitute", "pre": "The small 2 doubles the bracket: 2 × 62 = ", "post": "", "answer": 124, "hint": "Multiply the bracket total by 2."},
            {"pre": "Add the magnesium: 24 + 124 = ", "post": "", "answer": 148, "done": "Mr = 148, no unit.", "hint": "Add Mg to the doubled bracket."},
        ]),
    2: dict(hint="Divide mass by Mr: 11.7 ÷ 58.5.",
        expects={"inverted": 684.45},
        steps=[
            {"say": "Use \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\)."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 11.7, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide: 11.7 ÷ 58.5 = ", "post": "", "answer": 0.2, "hint": "Divide the mass by the Mr."},
            {"pre": "Check by reversing: 0.2 × 58.5 = ", "post": "", "answer": 11.7, "done": "It returns 11.7 g, so the amount is 0.2 mol.", "hint": "moles × Mr should give the mass back."},
        ]),
    3: dict(hint="Divide mass by Mr: 25 ÷ 100.",
        expects={"inverted": 2500},
        steps=[
            {"say": "Use \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\)."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 25, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide: 25 ÷ 100 = ", "post": "", "answer": 0.25, "hint": "Divide the mass by the Mr."},
            {"pre": "Check by reversing: 0.25 × 100 = ", "post": "", "answer": 25, "done": "It returns 25 g, so the amount is 0.25 mol.", "hint": "moles × Mr should give the mass back."},
        ]),
    4: dict(hint="Multiply moles by Mr: 0.25 × 100.",
        expects={"divided": 400},
        steps=[
            {"say": "Rearrange to \\(\\text{mass} = \\text{moles} \\times M_r\\)."},
            {"pre": "Write the number of moles: ", "post": "", "answer": 0.25, "hint": "Read the amount from the question."},
            {"phase": "substitute", "pre": "Multiply: 0.25 × 100 = ", "post": "", "answer": 25, "hint": "Multiply moles by Mr."},
            {"pre": "Check by reversing: 25 ÷ 100 = ", "post": "", "answer": 0.25, "done": "It returns 0.25 mol, so the mass is 25 g.", "hint": "mass ÷ Mr should give the moles back."},
        ]),
    5: dict(hint="Build the Mr of Na₂CO₃ first, then multiply by 0.4.",
        expects={"wrong_mr": 33.2},
        steps=[
            {"say": "First build the \\(M_r\\), then use \\(\\text{mass} = \\text{moles} \\times M_r\\). Na₂CO₃ has two sodiums, one carbon and three oxygens."},
            {"pre": "Mr = 2 × 23 + 12 + 3 × 16 = ", "post": "", "answer": 106, "hint": "Add 46 + 12 + 48."},
            {"phase": "substitute", "pre": "Multiply by the moles: 0.4 × 106 = ", "post": "", "answer": 42.4, "hint": "Multiply moles by Mr."},
            {"pre": "Check by reversing: 42.4 ÷ 106 = ", "post": "", "answer": 0.4, "done": "It returns 0.4 mol, so the mass is 42.4 g.", "hint": "mass ÷ Mr should give the moles back."},
        ]),
}

GOLD = {
    0: dict(hint="Mr is 100; find 40 ÷ 100, then × 100.",
        expects={"wrong_mr": None, "forgot_multiply_100": 0.4},
        steps=[
            {"say": "Percentage by mass = \\(\\dfrac{\\text{mass of that element in the formula}}{M_r} \\times 100\\). Build the \\(M_r\\) first."},
            {"pre": "Mr of CaCO₃ = 40 + 12 + 48 = ", "post": "", "answer": 100, "hint": "Add Ca, C and three oxygens."},
            {"phase": "substitute", "pre": "Calcium's share as a fraction: 40 ÷ 100 = ", "post": "", "answer": 0.4, "hint": "One calcium, Ar 40, over the Mr."},
            {"pre": "Turn it into a percentage: 0.4 × 100 = ", "post": "", "answer": 40, "done": "Calcium is 40% by mass.", "hint": "Multiply the fraction by 100."},
        ]),
    1: dict(hint="Mr is 101; find 14 ÷ 101, then × 100, to 1 d.p.",
        expects={"wrong_mr": 20.3, "wrong_element": 38.6},
        steps=[
            {"say": "Percentage by mass = \\(\\dfrac{\\text{element mass}}{M_r} \\times 100\\). Build the \\(M_r\\) first."},
            {"pre": "Mr of KNO₃ = 39 + 14 + 48 = ", "post": "", "answer": 101, "hint": "Potassium, nitrogen and three oxygens."},
            {"phase": "substitute", "pre": "Nitrogen's fraction (round to 3 d.p.): 14 ÷ 101 = ", "post": "", "answer": 0.139, "hint": "One nitrogen, Ar 14, over the Mr."},
            {"pre": "As a percentage to 1 d.p.: 0.139 × 100 = ", "post": "", "answer": 13.9, "done": "Nitrogen is 13.9% by mass.", "hint": "Multiply by 100 and round to 1 d.p."},
        ]),
    2: dict(hint="Mr is 18; find 16 ÷ 18, then × 100, to 1 d.p.",
        expects={"wrong_mr": 94.1, "wrong_element": 11.1},
        steps=[
            {"say": "Percentage by mass = \\(\\dfrac{\\text{element mass}}{M_r} \\times 100\\)."},
            {"pre": "Mr of H₂O = 2 + 16 = ", "post": "", "answer": 18, "hint": "Two hydrogens plus one oxygen."},
            {"phase": "substitute", "pre": "Oxygen's fraction (round to 3 d.p.): 16 ÷ 18 = ", "post": "", "answer": 0.889, "hint": "One oxygen, Ar 16, over the Mr."},
            {"pre": "As a percentage to 1 d.p.: 0.889 × 100 = ", "post": "", "answer": 88.9, "done": "Oxygen is 88.9% by mass.", "hint": "Multiply by 100 and round to 1 d.p."},
        ]),
    3: dict(hint="Rearrange to Mr = mass ÷ moles: 7.1 ÷ 0.1.",
        expects={"inverted": None, "wrong_rearrange": 0.71},
        steps=[
            {"say": "Rearrange \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\) to \\(M_r = \\dfrac{\\text{mass}}{\\text{moles}}\\)."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 7.1, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide mass by moles: 7.1 ÷ 0.1 = ", "post": "", "answer": 71, "hint": "Mass over moles gives the Mr."},
            {"pre": "Check by reversing: 0.1 × 71 = ", "post": "", "answer": 7.1, "done": "It returns 7.1 g, so the Mr is 71 (no unit).", "hint": "moles × Mr should give the mass back."},
        ]),
    4: dict(hint="Rearrange to Mr = mass ÷ moles: 4.9 ÷ 0.05.",
        expects={"inverted": None, "wrong_rearrange": 0.245},
        steps=[
            {"say": "Rearrange to \\(M_r = \\dfrac{\\text{mass}}{\\text{moles}}\\)."},
            {"pre": "Write the mass in grams: ", "post": "", "answer": 4.9, "hint": "Read the mass from the question."},
            {"phase": "substitute", "pre": "Divide mass by moles: 4.9 ÷ 0.05 = ", "post": "", "answer": 98, "hint": "Mass over moles gives the Mr."},
            {"pre": "Check by reversing: 0.05 × 98 = ", "post": "", "answer": 4.9, "done": "It returns 4.9 g, so the Mr is 98, which matches H₂SO₄.", "hint": "moles × Mr should give the mass back."},
        ]),
    5: dict(hint="Find the Mr of CO₂ (44), then mass = 3 × 44.",
        expects={"wrong_mr": 84, "divided": None},
        steps=[
            {"say": "First find the \\(M_r\\), then use \\(\\text{mass} = \\text{moles} \\times M_r\\)."},
            {"pre": "Mr of CO₂ = 12 + 2 × 16 = ", "post": "", "answer": 44, "hint": "Carbon plus two oxygens."},
            {"phase": "substitute", "pre": "Multiply by the moles: 3 × 44 = ", "post": "", "answer": 132, "hint": "Multiply moles by Mr."},
            {"pre": "Check by reversing: 132 ÷ 44 = ", "post": "", "answer": 3, "done": "It returns 3 mol, so the mass is 132 g.", "hint": "mass ÷ Mr should give the moles back."},
        ]),
}

def apply(tier_list, spec):
    for i, prob in enumerate(tier_list):
        s = spec[i]
        prob["hint"] = s["hint"]
        prob["guided_steps"] = s["steps"]
        # attach expects to misconceptions by pattern
        exp = s["expects"]
        for m in prob.get("misconceptions", []):
            pat = m.get("pattern")
            if pat in exp:
                m["expect"] = exp[pat]
            else:
                m["expect"] = None  # any un-mapped misconception: never fires
        # safety: ensure every misconception has an expect key
        for m in prob.get("misconceptions", []):
            if "expect" not in m:
                m["expect"] = None

apply(pb["bronze"], BRONZE)
apply(pb["silver"], SILVER)
apply(pb["gold"], GOLD)

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, numbers ready to use",
        "steps": [
            "<strong>Mr:</strong> add one \\(A_r\\) for every atom in the formula. A small subscript multiplies the atom before it, so CO₂ has two oxygens.",
            "<strong>Amount:</strong> \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\), and rearranged \\(\\text{mass} = \\text{moles} \\times M_r\\).",
            "Mr has no unit. Moles are in mol and mass in g, so state the unit in your final answer.",
        ],
        "example": {
            "question": "Calculate the moles in 88 g of carbon dioxide, CO₂ (Mr = 44).",
            "steps": [
                {"label": "Equation", "content": "<p>\\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(\\text{moles} = \\dfrac{88}{44}\\)</p>"},
                {"label": "Check", "content": "<p>2 × 44 = 88 g, which matches the mass given.</p>"},
                {"label": "Answer", "content": "<p><strong>2 mol</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: brackets, or work out Mr before you use it",
        "steps": [
            "A bracket multiplies everything inside it. Mg(NO₃)₂ means two whole NO₃ groups: \\(2 \\times (14 + 48) = 124\\).",
            "When only the formula is given, build the \\(M_r\\) first, then substitute into \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\) or \\(\\text{mass} = \\text{moles} \\times M_r\\).",
            "Keep the unit with the final answer: mol or g.",
        ],
        "example": {
            "question": "Calculate the Mr of sodium sulfate, Na₂SO₄ (Ar: Na = 23, S = 32, O = 16).",
            "steps": [
                {"label": "Count atoms", "content": "<p>Two Na, one S, four O.</p>"},
                {"label": "Add Ar values", "content": "<p>\\(2 \\times 23 + 32 + 4 \\times 16 = 46 + 32 + 64\\)</p>"},
                {"label": "Check", "content": "<p>46 + 32 + 64 = 142.</p>"},
                {"label": "Answer", "content": "<p><strong>142</strong> (no unit)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: two steps chained, or a rearrangement",
        "steps": [
            "<strong>Percentage by mass:</strong> \\(\\dfrac{\\text{mass of that element}}{M_r} \\times 100\\). Find \\(M_r\\) first, then the element's share, then × 100.",
            "<strong>Finding Mr from a measurement:</strong> rearrange \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\) to \\(M_r = \\dfrac{\\text{mass}}{\\text{moles}}\\).",
            "Round only at the end, to the decimal places the question asks for.",
        ],
        "example": {
            "question": "Calculate the percentage by mass of oxygen in magnesium oxide, MgO (Ar: Mg = 24, O = 16).",
            "steps": [
                {"label": "Mr", "content": "<p>24 + 16 = 40</p>"},
                {"label": "Oxygen fraction", "content": "<p>\\(\\dfrac{16}{40} = 0.4\\)</p>"},
                {"label": "Check", "content": "<p>0.4 × 100 = 40, and Mg is the other 60%. 40 + 60 = 100. ✓</p>"},
                {"label": "Answer", "content": "<p><strong>40%</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------- guided (opener + teach) ----------------
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "A charity bucket is full of identical 5p coins.<br>Each coin weighs 4 g. The whole bucket of coins weighs 2000 g.",
        "steps": [
            {"say": "No counting one by one. Just use the two weights.",
             "pre": "How many coins are in the bucket? 2000 ÷ 4 = ", "post": "", "answer": 500,
             "hint": "Divide the total weight by the weight of one coin."},
            {"say": "You just <strong>counted by weighing</strong>. Atoms are the coins: far too many to count, but each has a known mass. Chemists deal in a huge fixed pile called a <strong>mole</strong>, and the mass of one mole is the \\(M_r\\) in grams.",
             "pre": "If one mole of water weighs 18 g, how many moles are in 36 g? 36 ÷ 18 = ", "post": "", "answer": 2,
             "hint": "Same move: total mass ÷ mass of one mole."},
            {"say": "That is the whole idea: \\(\\text{moles} = \\dfrac{\\text{mass}}{M_r}\\). Weigh the sample, divide by the mass of one mole, and you have counted the particles."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Work out the Mr of ammonia, NH₃ (Ar: N = 14, H = 1).",
            "label": "Together: your first Mr",
            "steps": [
                {"say": "\\(M_r\\) is the sum of every atom's \\(A_r\\). Count the atoms: one nitrogen and three hydrogens.",
                 "pre": "Nitrogen: 1 × 14 = ", "post": "", "answer": 14, "hint": "One nitrogen atom, Ar 14."},
                {"pre": "Hydrogen: the small 3 means 3 × 1 = ", "post": "", "answer": 3, "hint": "The subscript 3 triples the hydrogen."},
                {"say": "Now add the two contributions.", "phase": "substitute",
                 "pre": "14 + 3 = ", "post": "", "answer": 17, "hint": "Add nitrogen and hydrogen."},
                {"pre": "Recount to be sure, N + H + H + H = 14 + 1 + 1 + 1 = ", "post": "", "answer": 17,
                 "done": "Both counts agree: Mr = 17, no unit.", "hint": "Adding one atom at a time should give the same total."},
            ],
        },
        "silver": {
            "display": "Work out the Mr of copper(II) nitrate, Cu(NO₃)₂ (Ar: Cu = 64, N = 14, O = 16).",
            "label": "Together: a bracket",
            "steps": [
                {"say": "A bracket multiplies everything inside it, and there are two NO₃ groups. Start inside one bracket.",
                 "pre": "One NO₃ group: 14 + 3 × 16 = ", "post": "", "answer": 62, "hint": "One nitrogen plus three oxygens."},
                {"pre": "The small 2 doubles the whole bracket: 2 × 62 = ", "post": "", "answer": 124, "hint": "Multiply the bracket total by 2."},
                {"say": "Now add the copper.", "phase": "substitute",
                 "pre": "64 + 124 = ", "post": "", "answer": 188, "hint": "Add Cu to the doubled bracket."},
                {"pre": "Recount the oxygens: there are 2 × 3 = 6, worth 6 × 16 = ", "post": "", "answer": 96,
                 "done": "Cu 64 + 2 N (28) + 6 O (96) = 188, so Mr = 188.", "hint": "Two brackets, three oxygens each."},
            ],
        },
        "gold": {
            "display": "Find the percentage by mass of nitrogen in ammonium nitrate, NH₄NO₃ (Ar: N = 14, H = 1, O = 16).",
            "label": "Together: two steps chained",
            "steps": [
                {"say": "Percentage by mass = \\(\\dfrac{\\text{mass of that element}}{M_r} \\times 100\\). Build the \\(M_r\\) first: two nitrogens, four hydrogens, three oxygens.",
                 "pre": "Mr = 2 × 14 + 4 × 1 + 3 × 16 = 28 + 4 + 48 = ", "post": "", "answer": 80, "hint": "Add 28 + 4 + 48."},
                {"pre": "Mass of nitrogen in the formula: 2 × 14 = ", "post": "", "answer": 28, "hint": "There are two nitrogen atoms."},
                {"say": "Now the nitrogen's share of the whole.", "phase": "substitute",
                 "pre": "Fraction: 28 ÷ 80 = ", "post": "", "answer": 0.35, "hint": "Nitrogen mass over the Mr."},
                {"pre": "Turn it into a percentage: 0.35 × 100 = ", "post": "", "answer": 35,
                 "done": "Nitrogen is 35% by mass. Two steps: Mr, then the share.", "hint": "Multiply the fraction by 100."},
            ],
        },
    },
}

pd = fix_dashes(pd)  # sweep any remaining preserved em dashes (e.g. legacy misconception text)

with io.open("lesson_chemistry-calculations-L01@dd9dbc80e5.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written. keys:", list(pd.keys()))
