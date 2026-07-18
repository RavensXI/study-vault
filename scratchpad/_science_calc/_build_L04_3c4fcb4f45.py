# -*- coding: utf-8 -*-
"""Build guided practice_data for higher-calculations-L04@3c4fcb4f45
Gas Volumes, Atom Economy and Percentage Yield (canonical 123bb55f...)."""
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_myL04_live.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/lesson_higher-calculations-L04@3c4fcb4f45.json"

row = json.load(io.open(LIVE, encoding="utf-8"))
pd = row["practice_data"]

# ---- strip pre-existing em dashes from preserved student-facing fields ----
EM = "—"
ec = pd.get("exam_context", {})
if isinstance(ec.get("frequency"), str):
    ec["frequency"] = "High. Atom economy and gas volumes are common in Separate Chemistry"
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and EM in st["label"]:
            st["label"] = st["label"].replace(" " + EM + " ", ": ").replace(EM, ":")

# ---- method_card (slim, <=140 words, <=4 steps) ----
pd["method_card"]["title"] = "Gas Volumes, Atom Economy and Percentage Yield"
pd["method_card"]["steps"] = [
    "Decide which calculation it is: gas volume, atom economy, or percentage yield",
    "Gas volume at RTP: volume = moles × 24 (and moles = volume ÷ 24)",
    "Atom economy: (Mr of desired product ÷ total Mr of reactants) × 100",
    "Percentage yield: (actual ÷ theoretical) × 100, never above 100%",
]
pd["method_card"]["content"] = (
    "<p>Three separate calculations. <strong>Gas volume at RTP:</strong> one mole of any "
    "gas fills 24 dm³, so \\(V = \\text{moles} \\times 24\\) (and \\(\\text{moles} = V \\div 24\\)). "
    "<strong>Atom economy</strong> is about the balanced equation: "
    "\\((M_r\\text{ desired} \\div \\text{total } M_r\\text{ reactants}) \\times 100\\). "
    "<strong>Percentage yield</strong> is about the experiment: "
    "\\((\\text{actual} \\div \\text{theoretical}) \\times 100\\), and can never exceed 100%. "
    "Remember 1 dm³ = 1000 cm³.</p>"
)

# ---- tier descriptions ----
pb = pd["problem_bank"]
pb["bronze_description"] = "One step, values ready to use: volume = moles × 24, or a single-step atom economy or yield."
pb["silver_description"] = "Convert a mass to moles first, then use the equation's ratio before finding a volume or yield."
pb["gold_description"]   = "Chain several steps: mass to moles, ratios, cm³/dm³ conversions, or comparing reaction routes."

# ---- helpers ----
def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d
def say(s): return {"say": s}

# ======================= BRONZE =======================
B = pb["bronze"]

# B0: 0.5 mol H2 -> V (12 dm3)  [completion problem]
B[0]["hint"] = "One mole of any gas at RTP fills 24 dm³, so multiply the moles by 24."
B[0]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 0.0208,
    "message": "Multiply by 24, do not divide: 0.5 × 24 = 12 dm³. Dividing gives 0.0208, far too small for a gas volume.",
    "note": "0.5/24 = 0.02083"}]
B[0]["guided_steps"] = [
    say("Gas volume at RTP uses one move: \\(V = \\text{moles} \\times 24\\)."),
    box("One mole of any gas at RTP fills how many dm³? = ", 24, "The molar volume you memorise for RTP."),
    box("We have 0.5 mol, so 0.5 × 24 = ", 12, "Half of 24.", say="Now multiply the moles by 24.", phase="substitute"),
    box("Check by reversing: moles = volume ÷ 24 = 12 ÷ 24 = ", 0.5,
        "Divide the volume by 24.", done="Back to 0.5 mol, so 12 dm³ is right."),
]

# B1: 4.8 dm3 -> moles (0.2)
B[1]["hint"] = "To turn a gas volume into moles at RTP, divide by 24."
B[1]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 115.2,
    "message": "Divide by 24, do not multiply: 4.8 ÷ 24 = 0.2 mol. Multiplying gives 115.2, far too many moles.",
    "note": "4.8*24 = 115.2"}]
B[1]["guided_steps"] = [
    say("Going from volume to moles reverses the rule: \\(\\text{moles} = \\frac{V}{24}\\)."),
    box("One mole of any gas at RTP fills how many dm³? = ", 24, "The molar volume for RTP."),
    box("So moles = 4.8 ÷ 24 = ", 0.2, "Divide the volume by 24.", say="Divide the 4.8 dm³ by 24.", phase="substitute"),
    box("Check by reversing: 0.2 × 24 = ", 4.8, "Multiply back by 24.", done="Back to 4.8 dm³, so 0.2 mol is right."),
]

# B2: CaCO3 -> CaO + CO2, AE of CaO (56)
B[2]["hint"] = "The denominator is the total Mr of the reactants, not the products."
B[2]["misconceptions"] = [{
    "pattern": "wrong_route", "check": "common", "expect": 44,
    "message": "The desired product is CaO (56), not CO₂. Atom economy = (56 ÷ 100) × 100 = 56%. Using CO₂ (44) gives 44%.",
    "note": "44/100*100 = 44"}]
B[2]["guided_steps"] = [
    say("Atom economy compares the desired product's \\(M_r\\) to the total \\(M_r\\) of the reactants."),
    box("Total Mr of the reactant CaCO₃ = 56 + 44 = ", 100, "The single reactant splits into CaO (56) and CO₂ (44)."),
    box("Mr of the desired product CaO = ", 56, "Given in the question."),
    box("Atom economy = (56 ÷ 100) × 100 = ", 56, "Divide, then times 100.", say="Now put them into the formula.", phase="substitute"),
    box("Check: the wasted CO₂ is 44%. Useful plus wasted must be 100, so 56 + 44 = ", 100, "Add the useful and wasted percentages.", done="100%, so the 56% atom economy is right."),
]

# B3: expected 10 g, got 7.5 g, yield (75)
B[3]["hint"] = "Percentage yield is actual over theoretical, times 100."
B[3]["misconceptions"] = [{
    "pattern": "inverse_error", "check": "common", "expect": 133.3,
    "message": "Actual over theoretical: (7.5 ÷ 10) × 100 = 75%. Flipping the fraction gives 133%, and yield can never exceed 100%.",
    "note": "10/7.5*100 = 133.3"}]
B[3]["guided_steps"] = [
    say("Percentage yield is \\(\\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\)."),
    box("Actual yield (what the student got) = ", 7.5, "The mass actually obtained."),
    box("Theoretical yield (what was expected) = ", 10, "The mass you could have made."),
    box("(7.5 ÷ 10) × 100 = ", 75, "Divide, then times 100.", say="Put them into the formula.", phase="substitute"),
    box("Check: the lost 2.5 g is 25%. 75 + 25 = ", 100, "Made plus lost must total 100.", done="100%, so a 75% yield is right."),
]

# B4: 2H2O2 -> 2H2O + O2, 0.1 mol H2O2 -> V O2 (1.2)
B[4]["hint"] = "Use the 2:1 ratio to find moles of O₂ first, then multiply by 24."
B[4]["misconceptions"] = [{
    "pattern": "mole_ratio", "check": "common", "expect": 2.4,
    "message": "From 2H₂O₂ → 1O₂, halve the moles first: 0.05 mol O₂, so 0.05 × 24 = 1.2 dm³. Using 0.1 mol gives 2.4 dm³, double the answer.",
    "note": "0.1*24 = 2.4"}]
B[4]["guided_steps"] = [
    say("Two moves: the equation's ratio for moles of gas, then \\(V = \\text{moles} \\times 24\\)."),
    box("From 2H₂O₂ → 2H₂O + O₂, moles O₂ = 0.1 ÷ 2 = ", 0.05, "The ratio is 2:1, so halve the H₂O₂ moles."),
    box("Volume = 0.05 × 24 = ", 1.2, "Moles of gas times 24.", say="Now find the volume.", phase="substitute"),
    box("Check: 1.2 ÷ 24 = ", 0.05, "Reverse the last step.", done="0.05 mol O₂, matching the ratio, so 1.2 dm³ is right."),
]

# B5: 2Mg + O2 -> 2MgO, AE (100)
B[5]["hint"] = "When there is only one product, every atom is useful."
B[5]["misconceptions"] = [{
    "pattern": "wrong_denominator", "check": "common", "expect": 60,
    "message": "Every atom of the reactants ends up in MgO, the only product, so atom economy = 100%. Comparing only the magnesium (48 ÷ 80) gives 60%, but the oxygen is useful too.",
    "note": "48/80*100 = 60"}]
B[5]["guided_steps"] = [
    say("Atom economy is desired \\(M_r\\) ÷ total reactant \\(M_r\\), times 100. Look for the single-product shortcut."),
    box("How many different products does 2Mg + O₂ → 2MgO have? = ", 1, "Count the products on the right."),
    box("If every atom ends up in that one product, what percentage is wasted? = ", 0, "Nothing else is made."),
    box("So atom economy = 100 − 0 = ", 100, "All the atoms are useful.", say="No atoms are lost, so:", phase="substitute"),
    box("Confirm with masses: reactants 2Mg + O₂ = 48 + 32 = 80; product 2MgO = 80; (80 ÷ 80) × 100 = ", 100, "Divide the product mass by the reactant mass.", done="100%, so no atoms are wasted."),
]

# ======================= SILVER =======================
S = pb["silver"]

# S0: 5.0 g CaCO3 -> CaO + CO2, V CO2 (1.2)  [completion problem]
S[0]["hint"] = "Mass to moles, then the 1:1 ratio, then multiply by 24."
S[0]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 120,
    "message": "Convert mass to moles first: 5 ÷ 100 = 0.05 mol, then × 24 = 1.2 dm³. Treating the 5 g as if it were moles gives 120 dm³, far too large.",
    "note": "5*24 = 120"}]
S[0]["guided_steps"] = [
    say("Three steps: mass to moles, the equation's ratio, then \\(V = \\text{moles} \\times 24\\)."),
    box("Moles CaCO₃ = mass ÷ Mr = 5.0 ÷ 100 = ", 0.05, "Divide the mass by the Mr."),
    box("Ratio CaCO₃ : CO₂ is 1 : 1, so moles CO₂ = ", 0.05, "One-to-one, so the same number."),
    box("Volume = 0.05 × 24 = ", 1.2, "Moles of gas times 24.", say="Now the volume.", phase="substitute"),
    box("Check: 1.2 ÷ 24 = ", 0.05, "Reverse the last step.", done="0.05 mol CO₂, matching the ratio, so 1.2 dm³ is right."),
]

# S1: CHANGED 2.3 g Na (1.2) -> 4.6 g Na (2.4) to remove duplicate with S0
S[1]["display"] = "4.6 g of sodium reacts with water: 2Na + 2H₂O → 2NaOH + H₂. Calculate the volume of hydrogen gas produced at RTP in dm³. (Ar: Na = 23)"
S[1]["solutions"] = [2.4]
S[1]["hint"] = "Mass to moles, then the 2:1 ratio, then multiply by 24."
S[1]["misconceptions"] = [{
    "pattern": "mole_ratio", "check": "common", "expect": 4.8,
    "message": "Moles Na = 4.6 ÷ 23 = 0.2. From 2Na → 1H₂, halve it: 0.1 mol H₂, so 0.1 × 24 = 2.4 dm³. Forgetting to halve gives 4.8 dm³.",
    "note": "0.2*24 = 4.8"}]
S[1]["guided_steps"] = [
    say("Mass to moles, then the 2 : 1 ratio, then times 24."),
    box("Moles Na = 4.6 ÷ 23 = ", 0.2, "Mass divided by the Ar."),
    box("From 2Na → 1H₂, moles H₂ = 0.2 ÷ 2 = ", 0.1, "Two sodium make one hydrogen molecule, so halve it."),
    box("Volume = 0.1 × 24 = ", 2.4, "Moles of gas times 24.", say="Now the volume.", phase="substitute"),
    box("Check: 2.4 ÷ 24 = ", 0.1, "Reverse the last step.", done="0.1 mol H₂, matching the ratio, so 2.4 dm³ is right."),
]

# S2: 10 g Fe2O3, 2Fe2O3+3C->4Fe+3CO2, 5.6 g Fe, yield (80)
S[2]["hint"] = "Find the theoretical mass of iron from the ratio, then compare with what was made."
S[2]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 160,
    "message": "The equation makes 4 Fe from 2 Fe₂O₃, so double the moles: 0.125 mol → 7.0 g theoretical. Yield = (5.6 ÷ 7.0) × 100 = 80%. Forgetting to double gives 3.5 g and an impossible 160%.",
    "note": "5.6/3.5*100 = 160"}]
S[2]["guided_steps"] = [
    say("Work out the theoretical mass of iron, then compare with the 5.6 g actually made."),
    box("Moles Fe₂O₃ = 10 ÷ 160 = ", 0.0625, "Mass divided by the Mr."),
    box("From 2Fe₂O₃ → 4Fe, moles Fe = 0.0625 × 2 = ", 0.125, "The 2:4 ratio doubles the moles."),
    box("Theoretical mass Fe = moles × Ar = 0.125 × 56 = ", 7, "Moles times 56."),
    box("Percentage yield = (5.6 ÷ 7) × 100 = ", 80, "Actual over theoretical, times 100.", say="Now the yield.", phase="substitute"),
    box("Check: the lost iron is 7 − 5.6 = 1.4 g, which is 20%. 80 + 20 = ", 100, "Made plus lost must total 100.", done="100%, so an 80% yield is right."),
]

# S3: Fe2O3+3CO->2Fe+3CO2, AE of Fe (45.9)
S[3]["hint"] = "Add the Mr of every reactant for the denominator; the desired product is 2Fe."
S[3]["misconceptions"] = [{
    "pattern": "wrong_denominator", "check": "common", "expect": 70,
    "message": "The reactants are Fe₂O₃ and 3CO, total Mr 244. AE = (112 ÷ 244) × 100 = 45.9%. Leaving out the CO (using 160) gives 70%.",
    "note": "112/160*100 = 70"}]
S[3]["guided_steps"] = [
    say("Add up the \\(M_r\\) of every reactant, then compare with the desired product."),
    box("Total Mr of reactants = 160 + (3 × 28) = 160 + 84 = ", 244, "Fe₂O₃ plus three CO."),
    box("Mr of the desired product 2Fe = 2 × 56 = ", 112, "Two iron atoms."),
    box("Atom economy = (112 ÷ 244) × 100 = ", 45.9, "Divide, times 100, round to 1 d.p. Type 45.9.", say="Now the formula.", phase="substitute"),
    box("Check: the wasted 3CO₂ (132) is 54.1%. 45.9 + 54.1 = ", 100, "Useful plus wasted must total 100.", done="100%, so 45.9% is right."),
]

# S4: 0.6 g Mg, Mg+2HCl->MgCl2+H2, V H2 (0.6)
S[4]["hint"] = "Mass to moles, 1:1 ratio, then multiply by 24."
S[4]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 14.4,
    "message": "Convert mass to moles first: 0.6 ÷ 24 = 0.025 mol, then × 24 = 0.6 dm³. Treating the 0.6 g as if it were moles gives 14.4 dm³.",
    "note": "0.6*24 = 14.4"}]
S[4]["guided_steps"] = [
    say("Mass to moles, the 1 : 1 ratio, then times 24."),
    box("Moles Mg = 0.6 ÷ 24 = ", 0.025, "Mass divided by the Ar."),
    box("Ratio Mg : H₂ is 1 : 1, so moles H₂ = ", 0.025, "Same number."),
    box("Volume = 0.025 × 24 = ", 0.6, "Moles of gas times 24.", say="Now the volume.", phase="substitute"),
    box("Check: 0.6 ÷ 24 = ", 0.025, "Reverse the last step.", done="0.025 mol H₂, matching the ratio, so 0.6 dm³ is right."),
]

# ======================= GOLD =======================
G = pb["gold"]

# G0: 3.25 g Zn, Zn+2HCl->ZnCl2+H2, 960 cm3, yield (80)  [completion problem]
G[0]["hint"] = "Find the theoretical volume, convert dm³ to cm³, then compare with 960 cm³."
G[0]["misconceptions"] = [{
    "pattern": "unit_error", "check": "common", "expect": 80000,
    "message": "Convert the theoretical volume to cm³ first: 1.2 dm³ = 1200 cm³. Yield = (960 ÷ 1200) × 100 = 80%. Comparing 960 cm³ with 1.2 dm³ directly gives a nonsensical 80000%.",
    "note": "960/1.2*100 = 80000"}]
G[0]["guided_steps"] = [
    say("Find the theoretical volume in cm³, then compare with the 960 cm³ collected. The molar volume 24 is in dm³, so mind the units."),
    box("Moles Zn = 3.25 ÷ 65 = ", 0.05, "Mass divided by the Ar."),
    box("Ratio Zn : H₂ is 1 : 1, so moles H₂ = ", 0.05, "Same number."),
    box("Theoretical volume in dm³ = 0.05 × 24 = ", 1.2, "Moles times 24 gives dm³."),
    box("Convert to cm³: 1.2 × 1000 = ", 1200, "1 dm³ = 1000 cm³."),
    box("Percentage yield = (960 ÷ 1200) × 100 = ", 80, "Actual over theoretical, times 100.", say="Now the yield.", phase="substitute"),
    box("Check: the lost gas is 1200 − 960 = 240 cm³, which is 20%. 80 + 20 = ", 100, "Collected plus lost must total 100.", done="100%, so an 80% yield is right."),
]

# G1: Route B Ca(OH)2->CaO+H2O, AE (75.7)
G[1]["hint"] = "Use only Route B's reactant, Ca(OH)₂ (Mr 74), in the denominator."
G[1]["misconceptions"] = [{
    "pattern": "wrong_route", "check": "common", "expect": 56,
    "message": "Route B's reactant is Ca(OH)₂ (Mr 74), so AE = (56 ÷ 74) × 100 = 75.7%. Using Route A's CaCO₃ (100) gives 56%.",
    "note": "56/100*100 = 56"}]
G[1]["guided_steps"] = [
    say("Only Route B matters here. Its reactant is Ca(OH)₂ and the desired product is CaO."),
    box("Total Mr of the reactant Ca(OH)₂ = ", 74, "Given for Route B."),
    box("Mr of the desired product CaO = ", 56, "Given in the question."),
    box("Atom economy = (56 ÷ 74) × 100 = ", 75.7, "Divide, times 100, round to 1 d.p. Type 75.7.", say="Now the formula.", phase="substitute"),
    box("Check: the wasted H₂O (18) is 24.3%. 75.7 + 24.3 = ", 100, "Useful plus wasted must total 100.", done="100%, so Route B's atom economy is 75.7%."),
]

# G2: 32 g Fe2O3, Fe2O3+3CO->2Fe+3CO2, V CO2 (14.4)
G[2]["hint"] = "Mass to moles, the 1:3 ratio to CO₂, then multiply by 24."
G[2]["misconceptions"] = [{
    "pattern": "mole_ratio", "check": "common", "expect": 4.8,
    "message": "The equation makes 3 CO₂ per Fe₂O₃, so moles CO₂ = 0.2 × 3 = 0.6, and V = 0.6 × 24 = 14.4 dm³. Forgetting the × 3 gives 4.8 dm³.",
    "note": "0.2*24 = 4.8"}]
G[2]["guided_steps"] = [
    say("Mass to moles, the 1 : 3 ratio to CO₂, then times 24."),
    box("Moles Fe₂O₃ = 32 ÷ 160 = ", 0.2, "Mass divided by the Mr."),
    box("From 1 Fe₂O₃ → 3 CO₂, moles CO₂ = 0.2 × 3 = ", 0.6, "Three CO₂ per Fe₂O₃, so times 3."),
    box("Volume = 0.6 × 24 = ", 14.4, "Moles of gas times 24.", say="Now the volume.", phase="substitute"),
    box("Check: 14.4 ÷ 24 = ", 0.6, "Reverse the last step.", done="0.6 mol CO₂, matching the ratio, so 14.4 dm³ is right."),
]

# G3: 2.5 g CaCO3, CaCO3+2HCl->CaCl2+H2O+CO2, 504 cm3, yield (84)
G[3]["hint"] = "Find the theoretical volume of CO₂ in cm³, then compare with 504 cm³."
G[3]["misconceptions"] = [{
    "pattern": "unit_error", "check": "common", "expect": 84000,
    "message": "Convert the theoretical volume to cm³: 0.6 dm³ = 600 cm³. Yield = (504 ÷ 600) × 100 = 84%. Comparing 504 cm³ with 0.6 dm³ gives an impossible 84000%.",
    "note": "504/0.6*100 = 84000"}]
G[3]["guided_steps"] = [
    say("Find the theoretical volume of CO₂ in cm³, then compare with the 504 cm³ collected."),
    box("Moles CaCO₃ = 2.5 ÷ 100 = ", 0.025, "Mass divided by the Mr."),
    box("Ratio CaCO₃ : CO₂ is 1 : 1, so moles CO₂ = ", 0.025, "Same number."),
    box("Theoretical volume in dm³ = 0.025 × 24 = ", 0.6, "Moles times 24."),
    box("Convert to cm³: 0.6 × 1000 = ", 600, "1 dm³ = 1000 cm³."),
    box("Percentage yield = (504 ÷ 600) × 100 = ", 84, "Actual over theoretical, times 100.", say="Now the yield.", phase="substitute"),
    box("Check: the lost gas is 600 − 504 = 96 cm³, which is 16%. 84 + 16 = ", 100, "Collected plus lost must total 100.", done="100%, so an 84% yield is right."),
]

# ======================= tier_guides =======================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one step, values ready to use",
        "steps": [
            "<strong>Gas volume at RTP:</strong> one mole of any gas fills 24 dm³. Volume = moles × 24, and moles = volume ÷ 24.",
            "<strong>Atom economy:</strong> \\((M_r\\text{ desired product} \\div \\text{total } M_r\\text{ reactants}) \\times 100\\).",
            "<strong>Percentage yield:</strong> \\((\\text{actual} \\div \\text{theoretical}) \\times 100\\). Yield never goes above 100%.",
        ],
        "example": {
            "question": "Calculate the volume of 2 mol of oxygen at RTP.",
            "steps": [
                {"label": "Recall the molar volume", "content": "<p>1 mol of any gas at RTP = 24 dm³</p>"},
                {"label": "Multiply", "content": "<p>2 × 24 = 48</p>"},
                {"label": "Check", "content": "<p>48 ÷ 24 = 2 mol, back to the start</p>"},
                {"label": "Answer", "content": "<p><strong>48 dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: convert to moles first",
        "steps": [
            "The mass is not the number of moles. Start with <strong>moles = mass ÷ M_r</strong> (use Ar for an element).",
            "Read the balanced equation's ratio to get the moles of the gas or product you want.",
            "Finish with volume = moles × 24, or (actual ÷ theoretical) × 100 for a yield.",
        ],
        "example": {
            "question": "4 g of CaCO₃ decomposes: CaCO₃ → CaO + CO₂. Volume of CO₂ at RTP? (Mr: CaCO₃ = 100)",
            "steps": [
                {"label": "Mass to moles", "content": "<p>4 ÷ 100 = 0.04 mol</p>"},
                {"label": "Ratio 1:1", "content": "<p>moles CO₂ = 0.04</p>"},
                {"label": "Volume", "content": "<p>0.04 × 24 = 0.96</p>"},
                {"label": "Check", "content": "<p>0.96 ÷ 24 = 0.04, back to the start</p>"},
                {"label": "Answer", "content": "<p><strong>0.96 dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain the steps and watch units",
        "steps": [
            "Multi-step problems link mass, moles, ratio and volume. Do one step at a time and keep a unit beside every number.",
            "For a yield from a gas, find the theoretical volume, then convert: <strong>1 dm³ = 1000 cm³</strong> before comparing.",
            "For competing routes, only use the reactants of the route named in the question.",
        ],
        "example": {
            "question": "6.5 g Zn + excess HCl → H₂; 2160 cm³ collected at RTP. Yield? (Ar: Zn = 65)",
            "steps": [
                {"label": "Moles Zn", "content": "<p>6.5 ÷ 65 = 0.1</p>"},
                {"label": "Theoretical volume", "content": "<p>0.1 × 24 = 2.4 dm³ = 2400 cm³</p>"},
                {"label": "Yield", "content": "<p>(2160 ÷ 2400) × 100 = 90</p>"},
                {"label": "Check", "content": "<p>lost 240 cm³ is 10%, 90 + 10 = 100</p>"},
                {"label": "Answer", "content": "<p><strong>90%</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ======================= guided (opener + teach) =======================
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "A party shop fills every balloon with exactly 24 litres of gas,<br>and it is 24 litres whichever gas goes in.",
        "steps": [
            box("You buy 3 balloons' worth of gas. Total litres = 3 × 24 = ", 72,
                "Three lots of 24.", say="No chemistry needed, just picture the balloons."),
            box("And a tiny sample, half a balloon's worth: 0.5 × 24 = ", 12,
                "Half of 24.", say="Now a smaller amount."),
            say("That is the whole trick for gas volumes. In chemistry one <strong>mole</strong> of any gas at RTP fills 24 dm³ (24 litres), so <strong>volume = moles × 24</strong>. You just did it with 3 and with 0.5. The other two skills here, atom economy and percentage yield, are both percentages you meet next."),
        ],
    },
    "teach": {
        "bronze": {
            "label": "Bronze walk: straight molar volume",
            "display": "Calculate the volume of 0.4 mol of nitrogen gas at RTP. Give it in dm³, then in cm³.",
            "steps": [
                box("One mole of any gas at RTP fills how many dm³? = ", 24,
                    "The value you memorise for RTP.", say="Gas volume at RTP always uses the same molar volume."),
                box("Volume in dm³ = 0.4 × 24 = ", 9.6, "Moles times 24.", say="We have 0.4 mol."),
                box("Convert to cm³: 9.6 × 1000 = ", 9600, "1 dm³ = 1000 cm³."),
                box("Check by reversing: 9600 ÷ 24000 = ", 0.4,
                    "Divide the cm³ by 24000 cm³ per mole.",
                    done="Back to 0.4 mol, so 9.6 dm³ (9600 cm³) is right."),
            ],
        },
        "silver": {
            "label": "Silver walk: mass to moles first",
            "display": "4 g of calcium carbonate decomposes: CaCO₃ → CaO + CO₂. Calculate the volume of CO₂ at RTP. (Mr: CaCO₃ = 100)",
            "steps": [
                box("Moles CaCO₃ = 4 ÷ 100 = ", 0.04, "Mass divided by the Mr.", say="The mass is not the moles, so convert first."),
                box("CaCO₃ : CO₂ is 1 : 1, so moles CO₂ = ", 0.04, "One-to-one.", say="Now read the ratio from the equation."),
                box("Volume = 0.04 × 24 = ", 0.96, "Moles of gas times 24."),
                box("Check: 0.96 ÷ 24 = ", 0.04, "Reverse the last step.", done="0.04 mol CO₂, matching the ratio, so 0.96 dm³ is right."),
            ],
        },
        "gold": {
            "label": "Gold walk: chain to a yield",
            "display": "6.5 g of zinc reacts with excess HCl: Zn + 2HCl → ZnCl₂ + H₂. The student collects 2160 cm³ of H₂ at RTP. Calculate the percentage yield. (Ar: Zn = 65)",
            "steps": [
                box("Moles Zn = 6.5 ÷ 65 = ", 0.1, "Mass divided by the Ar.", say="Build up to the theoretical volume, then compare."),
                box("Theoretical volume in dm³ = 0.1 × 24 = ", 2.4, "Moles times 24.", say="Ratio Zn : H₂ is 1 : 1."),
                box("Convert to cm³: 2.4 × 1000 = ", 2400, "1 dm³ = 1000 cm³."),
                box("Yield = (2160 ÷ 2400) × 100 = ", 90, "Divide, then times 100.",
                    done="90%. Actual over theoretical, times 100, so the walk lands on 90%."),
            ],
        },
    },
}

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("WROTE", OUT)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
