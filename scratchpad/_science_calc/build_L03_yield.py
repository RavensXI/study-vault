# -*- coding: utf-8 -*-
"""Build guided practice_data for higher-calculations-L03@2a30c22d67
   'Yield and Atom Economy' (canonical 8767022d..., separate-sciences-ocr-b)."""
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(s):
    return {"say": s}

pd = {}

# ---- method_card (<=140 words, <=4 steps, no em dashes) ----
pd["method_card"] = {
    "title": "Yield and Atom Economy",
    "steps": [
        "Decide which you need: percentage yield or atom economy.",
        "Percentage yield: find the theoretical yield from moles and the mole ratio, then (actual ÷ theoretical) × 100.",
        "Atom economy: (Mr of desired product ÷ Mr of all products) × 100, using every coefficient.",
        "State the answer as a percentage; yield is never above 100%."
    ],
    "content": "<p>Two calculations, easy to confuse, so decide which the question wants first.</p>"
               "<p><strong>Percentage yield</strong> compares what you actually got with the most you could have made:</p>"
               "<p>\\[\\% \\text{ yield} = \\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\]</p>"
               "<p>The theoretical yield comes from the limiting reactant using moles and the mole ratio. Yield is never above 100%.</p>"
               "<p><strong>Atom economy</strong> is a property of the balanced equation:</p>"
               "<p>\\[\\% \\text{ atom economy} = \\frac{M_r \\text{ desired product}}{M_r \\text{ all products}} \\times 100\\]</p>"
               "<p>One product means 100%; by-products lower it.</p>"
}

# ---- topic_links (preserve) ----
pd["topic_links"] = {"prerequisites": ["mole-calculations", "concentration-and-titration"]}

# ---- exam_context (em dashes removed) ----
pd["exam_context"] = {
    "marks": "3 to 5 per calculation, sometimes combined with an evaluation of industrial trade-offs",
    "paper": "Chemistry: Breadth and Depth papers",
    "frequency": "High. Yield and atom economy appear most years at Higher Tier; atom economy sometimes at Foundation"
}

# ================= PROBLEM BANK =================
bronze = []
# B0 3.2/4.0 -> 80
bronze.append({
    "unit": "%", "display": "A student obtains 3.2 g of copper from a reaction. The theoretical yield is 4.0 g. Calculate the percentage yield.",
    "solutions": [80.0], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\% \\text{ yield} = (\\text{actual} \\div \\text{theoretical}) \\times 100\\)",
    "misconceptions": [{"pattern": "inverse_error", "check": "common", "expect": 125.0,
        "message": "Percentage yield = (3.2 ÷ 4.0) × 100 = 80%. Dividing the wrong way (4.0 ÷ 3.2) gives 125%, which is impossible."}],
    "guided_steps": [
        say("Percentage yield = (actual ÷ theoretical) × 100. The actual is what you collected; the theoretical is the maximum."),
        box("Which is the theoretical maximum? Write it: ", 4.0, "The most you could have made.", post=" g"),
        box("percentage yield = (3.2 ÷ 4.0) × 100 = ", 80, "Actual over theoretical, times 100.", phase="substitute"),
        box("Check: 80% of 4.0 g = 0.80 × 4.0 = ", 3.2, "Should give back the mass collected.", done="3.2 g, matches what was collected. Yield = 80%."),
    ]})
# B1 5.6/8.0 -> 70
bronze.append({
    "unit": "%", "display": "A reaction produces 5.6 g of iron oxide. The theoretical yield is 8.0 g. Calculate the percentage yield.",
    "solutions": [70.0], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\% \\text{ yield} = (\\text{actual} \\div \\text{theoretical}) \\times 100\\)",
    "misconceptions": [{"pattern": "inverse_error", "check": "common", "expect": 142.9,
        "message": "Percentage yield = (5.6 ÷ 8.0) × 100 = 70%. Dividing 8.0 ÷ 5.6 instead gives about 143%, which cannot happen."}],
    "guided_steps": [
        say("Percentage yield = (actual ÷ theoretical) × 100."),
        box("Write the theoretical maximum: ", 8.0, "The most you could have made.", post=" g"),
        box("percentage yield = (5.6 ÷ 8.0) × 100 = ", 70, "Actual over theoretical, times 100.", phase="substitute"),
        box("Check: 70% of 8.0 g = 0.70 × 8.0 = ", 5.6, "Should give back the mass collected.", done="5.6 g, matches. Yield = 70%."),
    ]})
# B2 MC desired product CaO
bronze.append({
    "display": "Consider: CaCO₃ → CaO + CO₂. Which is the desired product if the aim is to make quicklime (CaO)?",
    "options": ["CO₂", "CaCO₃", "CaO", "Ca"], "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "hint": "The desired product is the substance you are trying to make.",
    "misconceptions": [{"pattern": "wrong_equation", "check": "common", "expect": None,
        "message": "CaO is the substance you want to collect, so it is the desired product."}]})
# B3 water only product -> 100
bronze.append({
    "unit": "%", "display": "In the reaction 2H₂ + O₂ → 2H₂O, the only product is water. What is the atom economy?",
    "solutions": [100], "calculator": False, "input_type": "single_value",
    "equation_hint": "If there is only one product, all atoms end up in it.",
    "misconceptions": [{"pattern": "wrong_formula", "check": "common", "expect": None,
        "message": "There is only one product, water, so every atom ends up in it. Atom economy = 100%."}],
    "guided_steps": [
        say("Atom economy = (Mr of the desired product ÷ Mr of ALL products) × 100."),
        box("How many different products does this reaction make? ", 1, "Only water comes out."),
        box("With one product, the desired Mr is the whole total: atom economy = (1 ÷ 1) × 100 = ", 100, "Every atom ends up in the product you want.", phase="substitute"),
        box("Fraction wasted = 100 − 100 = ", 0, "Take the atom economy from 100.", done="Nothing is wasted. Atom economy = 100%."),
    ]})
# B4 9.0/12.0 -> 75
bronze.append({
    "unit": "%", "display": "A student expects to make 12.0 g of a product but only obtains 9.0 g. Calculate the percentage yield.",
    "solutions": [75.0], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\% \\text{ yield} = (\\text{actual} \\div \\text{theoretical}) \\times 100\\)",
    "misconceptions": [{"pattern": "wrong_rearrange", "check": "common", "expect": 133.3,
        "message": "Percentage yield = (9.0 ÷ 12.0) × 100 = 75%. Dividing 12.0 ÷ 9.0 the wrong way gives about 133%, which is impossible."}],
    "guided_steps": [
        say("Percentage yield = (actual ÷ theoretical) × 100."),
        box("Which is the theoretical maximum? Write it: ", 12, "The amount expected.", post=" g"),
        box("percentage yield = (9.0 ÷ 12.0) × 100 = ", 75, "Actual over theoretical, times 100.", phase="substitute"),
        box("Check: 75% of 12.0 g = 0.75 × 12.0 = ", 9, "Should give back the mass collected.", done="9.0 g, matches. Yield = 75%."),
    ]})
# B5 NaCl 3.51/5.85 -> 60 (was 4.68/5.85=80, duplicate with B0; fixed)
bronze.append({
    "unit": "%", "display": "The theoretical yield of NaCl from a reaction is 5.85 g. The actual yield is 3.51 g. Calculate the percentage yield.",
    "solutions": [60.0], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\% \\text{ yield} = (\\text{actual} \\div \\text{theoretical}) \\times 100\\)",
    "misconceptions": [{"pattern": "rounding", "check": "common", "expect": None,
        "message": "Percentage yield = (3.51 ÷ 5.85) × 100 = 60%. Divide the actual by the theoretical, then multiply by 100."}],
    "guided_steps": [
        say("Percentage yield = (actual ÷ theoretical) × 100."),
        box("Write the theoretical maximum: ", 5.85, "The most that could form.", post=" g"),
        box("percentage yield = (3.51 ÷ 5.85) × 100 = ", 60, "Actual over theoretical, times 100.", phase="substitute"),
        box("Check: 60% of 5.85 g = 0.60 × 5.85 = ", 3.51, "Should give back the mass collected.", done="3.51 g, matches. Yield = 60%."),
    ]})
# B6 CaO atom economy -> 56 (was N2+3H2 100, duplicate with B3; fixed)
bronze.append({
    "unit": "%", "display": "Consider: CaCO₃ → CaO + CO₂. Calculate the atom economy for CaO. (Mr: CaO = 56, CO₂ = 44)",
    "solutions": [56], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{atom economy} = \\frac{M_r \\text{ desired}}{M_r \\text{ all products}} \\times 100\\)",
    "misconceptions": [{"pattern": "wrong_denominator", "check": "common", "expect": 100,
        "message": "Put the Mr of ALL products on the bottom: 56 + 44 = 100, so atom economy = (56 ÷ 100) × 100 = 56%. Using only CaO on the bottom gives 100%, which would mean no waste."}],
    "guided_steps": [
        say("Atom economy = (Mr of the desired product ÷ Mr of ALL products) × 100."),
        box("Add the Mr of all products: 56 + 44 = ", 100, "Both CaO and CO₂ count."),
        box("atom economy = (56 ÷ 100) × 100 = ", 56, "Desired Mr over total, times 100.", phase="substitute"),
        box("The waste is CO₂: 100 − 56 = ", 44, "Take the atom economy from 100.", done="44% is lost as CO₂. Atom economy = 56%."),
    ]})
# B7 MC reason yield <100
bronze.append({
    "display": "Give one reason why the percentage yield of a reaction is less than 100%.",
    "options": ["The Mr of the product is too large", "Some product is lost during filtration or evaporation",
                "Atom economy is always less than 100%", "The reaction is endothermic"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "Think about product physically lost when you transfer or purify it.",
    "misconceptions": [{"pattern": "wrong_equation", "check": "common", "expect": None,
        "message": "Yield falls below 100% because product is physically lost during transfer, filtering or evaporation, or the reaction is reversible or incomplete."}]})

silver = []
# S0 CH4 atom economy CO2 -> 55
silver.append({
    "unit": "%", "accept": 0.5, "display": "Consider: CH₄ + 2O₂ → CO₂ + 2H₂O. Calculate the atom economy for CO₂ as the desired product. (Ar: C = 12, O = 16, H = 1)",
    "solutions": [55.0], "calculator": True, "input_type": "single_value",
    "equation_hint": "% atom economy = Mr(desired product) ÷ sum of Mr of ALL products × 100. For 1 CO₂ + 2 H₂O.",
    "misconceptions": [
        {"pattern": "wrong_formula", "check": "common", "expect": 71.0,
         "message": "Multiply each product by its coefficient: 2H₂O = 36. Total = 44 + 36 = 80, so atom economy = (44 ÷ 80) × 100 = 55%. Forgetting to double the water (using 44 + 18 = 62) gives about 71%."},
        {"pattern": "forgot_step", "check": "common", "expect": None,
         "message": "Sum every product Mr with its coefficient before dividing: CO₂ (44) + 2H₂O (36) = 80. Atom economy = (44 ÷ 80) × 100 = 55%."}],
    "guided_steps": [
        say("Atom economy uses every product with its coefficient. Desired is CO₂; the products are CO₂ and 2H₂O."),
        box("Mr of 2H₂O = 2 × 18 = ", 36, "Two water molecules, each Mr 18."),
        box("Mr of all products = 44 + 36 = ", 80, "Add CO₂ and the water."),
        box("atom economy = (44 ÷ 80) × 100 = ", 55, "Desired over total, times 100.", phase="substitute"),
        box("The waste is water: 100 − 55 = ", 45, "Take the atom economy from 100.", done="45% is lost as water. Atom economy = 55%."),
    ]})
# S1 fermentation ethanol -> 51.1
silver.append({
    "unit": "%", "accept": 0.5, "display": "Ethanol can be made by fermentation: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂. Calculate the atom economy for ethanol (C₂H₅OH). (Ar: C = 12, H = 1, O = 16)",
    "solutions": [51.1], "calculator": True, "input_type": "single_value", "higher_only": True,
    "equation_hint": "Total Mr of products = 2×Mr(C₂H₅OH) + 2×Mr(CO₂). Atom economy = 2×Mr(C₂H₅OH) ÷ total × 100.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "check": "common", "expect": 25.6,
         "message": "Use coefficients: 2C₂H₅OH = 92, 2CO₂ = 88, total 180. Atom economy = (92 ÷ 180) × 100 = 51.1%. Using a single ethanol (46 ÷ 180) gives about 25.6%."},
        {"pattern": "forgot_step", "check": "common", "expect": None,
         "message": "Multiply each Mr by its coefficient before summing: 2 × 46 = 92 for ethanol, 2 × 44 = 88 for CO₂."}],
    "guided_steps": [
        say("Atom economy uses coefficients. Desired is 2C₂H₅OH; the other product is 2CO₂. Mr of one ethanol is 46."),
        box("Mr of 2C₂H₅OH = 2 × 46 = ", 92, "Two ethanol, each Mr 46."),
        box("Mr of 2CO₂ = 2 × 44 = ", 88, "Two CO₂, each Mr 44."),
        box("Mr of all products = 92 + 88 = ", 180, "Add both products."),
        box("atom economy = (92 ÷ 180) × 100 = ", 51.1, "Desired over total, times 100, to 1 d.p.", phase="substitute"),
        box("The waste (CO₂) fraction = 100 − 51.1 = ", 48.9, "Take the atom economy from 100.", done="48.9% is lost as CO₂. Atom economy = 51.1%."),
    ]})
# S2 Mg -> MgO yield 90
silver.append({
    "unit": "%", "display": "12.0 g of magnesium reacts with excess oxygen: 2Mg + O₂ → 2MgO. The student collects 18.0 g of MgO. Calculate the percentage yield. (Ar: Mg = 24, O = 16)",
    "solutions": [90.0], "calculator": True, "input_type": "single_value",
    "equation_hint": "Find theoretical yield: n(Mg) → mole ratio → n(MgO) → mass of MgO. Then % yield.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "check": "common", "expect": 150.0,
         "message": "Use the Mr of MgO (40), not Mg (24). Theoretical = 0.5 × 40 = 20 g, so yield = (18 ÷ 20) × 100 = 90%. Using Mr = 24 gives an impossible 150%."},
        {"pattern": "forgot_step", "check": "common", "expect": None,
         "message": "Find the theoretical mass first using moles, then apply the yield formula."}],
    "guided_steps": [
        say("Percentage yield from a mass: find the theoretical mass of MgO (moles, ratio, mass), then compare with the 18.0 g collected."),
        box("moles of Mg = 12.0 ÷ 24 = ", 0.5, "Mass over Ar."),
        box("2 Mg : 2 MgO is 1 : 1, so moles of MgO = ", 0.5, "One to one ratio."),
        box("theoretical mass of MgO = 0.5 × 40 = ", 20, "Moles times Mr (MgO = 40)."),
        box("percentage yield = (18.0 ÷ 20) × 100 = ", 90, "Actual over theoretical, times 100.", phase="substitute"),
        box("Check: 90% of 20 g = 0.90 × 20 = ", 18, "Should give back the mass collected.", done="18 g, matches. Yield = 90%."),
    ]})
# S3 MC increase atom economy
silver.append({
    "display": "Which of the following would increase the atom economy of an industrial process?",
    "options": ["Filtering the product more carefully", "Using a more concentrated reactant",
                "Finding a reaction pathway that produces fewer by-products", "Cooling the reaction mixture slowly"],
    "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "hint": "Atom economy depends only on the balanced equation and its products.",
    "misconceptions": [{"pattern": "wrong_equation", "check": "common", "expect": None,
        "message": "Atom economy depends on the balanced equation: the ratio of desired product Mr to total products Mr. Fewer by-products means more atoms end up where you want them."}]})
# S4 Na -> NaOH yield 94.3
silver.append({
    "unit": "%", "accept": 0.5, "display": "5.0 g of Na is reacted with excess water: 2Na + 2H₂O → 2NaOH + H₂. 8.2 g of NaOH is produced. Calculate the percentage yield. (Ar: Na = 23, O = 16, H = 1)",
    "solutions": [94.3], "calculator": True, "input_type": "single_value",
    "equation_hint": "Find theoretical mass of NaOH: n(Na) → 1:1 ratio → mass. Then % yield.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "check": "common", "expect": None,
         "message": "n(Na) = 5.0 ÷ 23 = 0.2174. Ratio 1 : 1, Mr NaOH = 40, theoretical = 8.696 g. Yield = (8.2 ÷ 8.696) × 100 = 94.3%."},
        {"pattern": "rounding", "check": "common", "expect": None,
         "message": "Keep enough decimals: 5.0 ÷ 23 = 0.2174, theoretical 8.696 g, yield 94.3%."}],
    "guided_steps": [
        say("Percentage yield from a mass: find the theoretical mass of NaOH, then compare with the 8.2 g collected. The numbers are not round, so keep a few decimals."),
        box("moles of Na = 5.0 ÷ 23 = ", 0.2174, "Mass over Ar, to 4 d.p."),
        box("1 Na : 1 NaOH, so theoretical mass of NaOH = 0.2174 × 40 = ", 8.696, "Moles times Mr (NaOH = 40)."),
        box("percentage yield = (8.2 ÷ 8.696) × 100 = ", 94.3, "Actual over theoretical, times 100, to 1 d.p.", phase="substitute"),
        box("Check: 94.3% of 8.696 g = 0.943 × 8.696 = ", 8.2, "Should give back the mass collected.", done="8.2 g (to 1 d.p.), matches. Yield = 94.3%."),
    ]})
# S5 MC difference atom economy vs yield
silver.append({
    "display": "In the Haber process, N₂ + 3H₂ → 2NH₃, the atom economy is 100%. Yet the yield is only around 15% per pass. Explain the difference between atom economy and percentage yield in one sentence.",
    "options": ["Atom economy measures what fraction of reactant atoms end up in the desired product; yield measures how much product was actually obtained compared with the maximum possible",
                "Atom economy and yield are the same thing measured differently",
                "Yield measures wasted atoms; atom economy measures how fast the reaction goes",
                "Atom economy is only relevant in industry; yield applies to school experiments"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "One is about the equation's products; the other is about what you actually collected.",
    "misconceptions": [{"pattern": "wrong_equation", "check": "common", "expect": None,
        "message": "Atom economy is about the reaction equation (types of products). Yield is about what you actually collect compared with the theoretical maximum."}]})

gold = []
# G0 Fe2O3 atom economy Fe -> 45.9
gold.append({
    "unit": "%", "accept": 0.5, "display": "Consider the industrial production of iron: Fe₂O₃ + 3CO → 2Fe + 3CO₂. Calculate the atom economy for Fe. (Ar: Fe = 56, O = 16, C = 12)",
    "solutions": [45.9], "calculator": True, "input_type": "single_value", "higher_only": True,
    "hint": "Multiply each product by its coefficient, then divide 2Fe by the total.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "check": "common", "expect": 56.0,
         "message": "Use the coefficients: 2Fe = 112, 3CO₂ = 132, total 244, so atom economy = (112 ÷ 244) × 100 = 45.9%. Ignoring the coefficients (56 ÷ 100) gives 56%."},
        {"pattern": "forgot_step", "check": "common", "expect": None,
         "message": "Sum all products with their coefficients: 2Fe (112) + 3CO₂ (132) = 244."}],
    "guided_steps": [
        say("Atom economy uses coefficients. Desired is 2Fe; the other product is 3CO₂."),
        box("Mr of 2Fe = 2 × 56 = ", 112, "Two iron atoms."),
        box("Mr of one CO₂ = 12 + (2 × 16) = ", 44, "Carbon plus two oxygens."),
        box("Mr of 3CO₂ = 3 × 44 = ", 132, "Three CO₂."),
        box("Mr of all products = 112 + 132 = ", 244, "Add both products."),
        box("atom economy = (112 ÷ 244) × 100 = ", 45.9, "Desired over total, times 100, to 1 d.p.", phase="substitute"),
        box("The waste (CO₂) fraction = 100 − 45.9 = ", 54.1, "Take the atom economy from 100.", done="54.1% is lost as CO₂. Atom economy = 45.9%."),
    ]})
# G1 Al -> AlCl3 yield 66.7
gold.append({
    "unit": "%", "accept": 0.5, "display": "24.3 g of aluminium reacts with excess chlorine: 2Al + 3Cl₂ → 2AlCl₃. The student collects 80.1 g of AlCl₃. Calculate the percentage yield. (Ar: Al = 27, Cl = 35.5)",
    "solutions": [66.7], "calculator": True, "input_type": "single_value", "higher_only": True,
    "hint": "Find n(Al), then Mr of AlCl₃, then the theoretical mass, then divide.",
    "misconceptions": [
        {"pattern": "inverse_error", "check": "common", "expect": 150.0,
         "message": "Divide actual by theoretical: (80.1 ÷ 120.15) × 100 = 66.7%. Dividing the other way (120.15 ÷ 80.1) gives 150%, which is impossible."},
        {"pattern": "mole_ratio", "check": "common", "expect": None,
         "message": "Al : AlCl₃ from 2 : 2 is 1 : 1, so 0.9 mol Al gives 0.9 mol AlCl₃."}],
    "guided_steps": [
        say("Percentage yield from a mass: find the theoretical mass of AlCl₃, then compare with the 80.1 g collected."),
        box("moles of Al = 24.3 ÷ 27 = ", 0.9, "Mass over Ar."),
        box("Mr of AlCl₃ = 27 + (3 × 35.5) = ", 133.5, "Aluminium plus three chlorines."),
        box("2 Al : 2 AlCl₃ is 1 : 1, so theoretical mass = 0.9 × 133.5 = ", 120.15, "Moles times Mr."),
        box("percentage yield = (80.1 ÷ 120.15) × 100 = ", 66.7, "Actual over theoretical, times 100, to 1 d.p.", phase="substitute"),
        box("Check: moles of AlCl₃ collected = 80.1 ÷ 133.5 = ", 0.6, "Mass over Mr.", done="0.6 mol collected from 0.9 mol possible: 0.6 ÷ 0.9 = 66.7%."),
    ]})
# G2 pharma atom economy -> 62.5
gold.append({
    "unit": "%", "display": "A pharmaceutical reaction produces the desired drug (Mr = 250) as well as a by-product (Mr = 150). The equation shows they form in a 1:1 ratio. Calculate the atom economy for the drug.",
    "solutions": [62.5], "calculator": True, "input_type": "single_value", "higher_only": True,
    "hint": "Add both products for the bottom of the fraction.",
    "misconceptions": [{"pattern": "wrong_formula", "check": "common", "expect": 37.5,
        "message": "Atom economy = (Mr desired ÷ Mr all products) × 100 = (250 ÷ 400) × 100 = 62.5%. Using the by-product (150 ÷ 400) gives 37.5%, the fraction wasted."}],
    "guided_steps": [
        say("Atom economy = (Mr of the desired product ÷ Mr of ALL products) × 100. Both products form 1 : 1."),
        box("Mr of all products = 250 + 150 = ", 400, "Add the drug and the by-product."),
        box("atom economy = (250 ÷ 400) × 100 = ", 62.5, "Desired over total, times 100.", phase="substitute"),
        box("The by-product fraction = 100 − 62.5 = ", 37.5, "Take the atom economy from 100.", done="37.5% of the atoms are wasted as by-product. Atom economy = 62.5%."),
    ]})
# G3 MC limiting reactant
gold.append({
    "display": "Which reactant is the limiting reactant when 6.0 g of Mg reacts with 8.0 g of O₂? The equation is: 2Mg + O₂ → 2MgO. (Ar: Mg = 24, O = 16)",
    "options": ["Mg, because it has the smaller mass", "O₂, because it has the smaller mass",
                "Mg, because the moles available are less than required by the mole ratio", "O₂, because there is excess after the reaction"],
    "solutions": [2], "calculator": True, "input_type": "multiple_choice", "higher_only": True,
    "hint": "Convert both masses to moles, then compare with the equation's ratio.",
    "misconceptions": [
        {"pattern": "wrong_formula", "check": "common", "expect": None,
         "message": "n(Mg) = 6 ÷ 24 = 0.25 mol. n(O₂) = 8 ÷ 32 = 0.25 mol. The ratio needed is 2 Mg : 1 O₂, so 0.25 mol O₂ would need 0.50 mol Mg but only 0.25 mol is present. Mg is limiting."},
        {"pattern": "forgot_step", "check": "common", "expect": None,
         "message": "Compare actual moles with the equation ratio. 0.25 mol Mg needs only 0.125 mol O₂, so O₂ is in excess and Mg is the limiting reactant."}]})
# G4 Zn -> H2 yield 70
gold.append({
    "unit": "%", "display": "A student reacts 6.5 g of zinc with excess hydrochloric acid: Zn + 2HCl → ZnCl₂ + H₂. She collects 0.14 g of hydrogen gas. Calculate the percentage yield. (Ar: Zn = 65, H = 1)",
    "solutions": [70.0], "calculator": True, "input_type": "single_value",
    "hint": "Find the theoretical mass of H₂ (Mr = 2), then divide the 0.14 g by it.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "check": "common", "expect": None,
         "message": "n(Zn) = 6.5 ÷ 65 = 0.1 mol. Ratio 1 : 1, Mr H₂ = 2, theoretical = 0.2 g. Yield = (0.14 ÷ 0.2) × 100 = 70%."},
        {"pattern": "wrong_product", "check": "common", "expect": None,
         "message": "The question asks for the yield of H₂, not ZnCl₂. Use Mr H₂ = 2: theoretical = 0.2 g, yield = 70%."}],
    "guided_steps": [
        say("Percentage yield of hydrogen: find the theoretical mass of H₂ from the zinc, then compare with the 0.14 g collected."),
        box("moles of Zn = 6.5 ÷ 65 = ", 0.1, "Mass over Ar."),
        box("1 Zn : 1 H₂, and Mr of H₂ = 2, so theoretical mass = 0.1 × 2 = ", 0.2, "Moles times Mr."),
        box("percentage yield = (0.14 ÷ 0.2) × 100 = ", 70, "Actual over theoretical, times 100.", phase="substitute"),
        box("Check: 70% of 0.2 g = 0.70 × 0.2 = ", 0.14, "Should give back the hydrogen collected.", done="0.14 g, matches. Yield = 70%."),
    ]})

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One formula, values already in the right units: read percentage yield straight off, or use atom economy with the Mr values given.",
    "silver_description": "Change the mass to moles first, use the balanced equation's ratio, then find the theoretical mass or the atom economy with coefficients.",
    "gold_description": "Chain the steps: work out the theoretical amount then the yield, handle a limiting reactant, or use every coefficient in atom economy."
}

pd["related_videos"] = []

# ---- worked_examples (preserve; fix literal em dash in Silver answer) ----
pd["worked_examples"] = [
    {"steps": [
        {"label": "Step 1: Write the formula", "content": "<p>\\(\\% \\text{ yield} = \\dfrac{\\text{actual yield}}{\\text{theoretical yield}} \\times 100\\)</p>"},
        {"label": "Step 2: Substitute values", "content": "<p>\\(\\% \\text{ yield} = \\dfrac{4.5}{6.0} \\times 100\\)</p>"},
        {"label": "Answer", "content": "<p>Percentage yield = <strong>75%</strong></p>", "is_answer": True}],
     "question": "A reaction produces 4.5 g of product. The theoretical yield is 6.0 g. Calculate the percentage yield.", "difficulty": "Bronze"},
    {"steps": [
        {"label": "Step 1: Find Mr of the desired product", "content": "<p>Mr of MgO = 24 + 16 = 40. From the equation, 2 moles of MgO are produced, so total = 2 × 40 = 80.</p>"},
        {"label": "Step 2: Find total Mr of all products", "content": "<p>The only product is MgO (2 moles), so total = 80.</p>"},
        {"label": "Step 3: Apply the formula", "content": "<p>\\(\\% \\text{ atom economy} = \\dfrac{80}{80} \\times 100\\)</p>"},
        {"label": "Answer", "content": "<p>Atom economy = <strong>100%</strong> (only one product, so no waste).</p>", "is_answer": True}],
     "question": "Consider the reaction: 2Mg + O₂ → 2MgO. Calculate the atom economy for MgO. (Ar: Mg = 24, O = 16)", "difficulty": "Silver"},
    {"steps": [
        {"label": "Step 1: Find moles of Mg (limiting reactant)", "content": "<p>n(Mg) = 2.4 ÷ 24 = 0.1 mol</p>"},
        {"label": "Step 2: Use mole ratio to find theoretical moles of MgCl₂", "content": "<p>Mg : MgCl₂ = 1 : 1 (from equation)</p><p>n(MgCl₂) = 0.1 mol</p>"},
        {"label": "Step 3: Calculate theoretical yield (mass)", "content": "<p>Mr of MgCl₂ = 24 + (2 × 35.5) = 95</p><p>Theoretical mass = 0.1 × 95 = 9.5 g</p>"},
        {"label": "Step 4: Calculate % yield", "content": "<p>\\(\\% \\text{ yield} = \\dfrac{8.1}{9.5} \\times 100\\)</p>"},
        {"label": "Answer", "content": "<p>(a) Theoretical yield = <strong>9.5 g</strong>; (b) Percentage yield = <strong>85.3%</strong></p>", "is_answer": True}],
     "question": "2.4 g of magnesium is reacted with excess dilute hydrochloric acid: Mg + 2HCl → MgCl₂ + H₂. The student collects 8.1 g of MgCl₂. Calculate (a) the theoretical yield and (b) the percentage yield. (Ar: Mg = 24, Cl = 35.5, H = 1)", "difficulty": "Gold"}
]

# ---- tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one formula, values ready to use",
        "steps": [
            "Spot which you need. Percentage yield: \\(\\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\). Atom economy: \\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\).",
            "The numbers are ready to use, so substitute straight in. For atom economy, add ALL the products on the bottom, not just the one you want. One product means 100%.",
            "One calculation, one answer, given as a percentage."
        ],
        "example": {
            "question": "In CaCO₃ → CaO + CO₂, atom economy of CaO? (Mr: CaO = 56, CO₂ = 44)",
            "steps": [
                {"label": "Equation", "content": "<p>\\(\\text{AE} = \\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(\\text{AE} = \\frac{56}{56 + 44} \\times 100\\)</p>"},
                {"label": "Check", "content": "<p>\\(56 + 44 = 100\\), and \\(\\frac{56}{100} \\times 100 = 56\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>56%</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: change the mass to moles first",
        "steps": [
            "Now you are given a mass, not moles. Convert first: \\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\).",
            "Use the equation's ratio to get moles of the product you want, then its mass with \\(\\text{mass} = \\text{moles} \\times M_r\\). For atom economy, multiply each product's Mr by its coefficient before adding.",
            "Put the theoretical mass into the yield formula, then check the value is sensible."
        ],
        "example": {
            "question": "6.0 g Mg burns: 2Mg + O₂ → 2MgO. Collects 8.0 g MgO. % yield? (Ar: Mg = 24, O = 16)",
            "steps": [
                {"label": "Moles", "content": "<p>\\(6.0 \\div 24 = 0.25\\) mol Mg</p>"},
                {"label": "Theoretical", "content": "<p>1 : 1, so 0.25 mol MgO; mass \\(= 0.25 \\times 40 = 10\\) g</p>"},
                {"label": "Check", "content": "<p>\\(0.80 \\times 10 = 8\\) g ✓</p>"},
                {"label": "Answer", "content": "<p><strong>80%</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: chain the steps or find the limiting reactant",
        "steps": [
            "Gold questions combine skills. For percentage yield, find the theoretical mass first (moles, ratio, Mr, mass), then compare with what was collected.",
            "For atom economy, use every coefficient: 2Fe means \\(2 \\times M_r\\), and put every product on the bottom.",
            "For a limiting reactant, convert both reactant masses to moles and compare with the equation's ratio: the one in short supply runs out first."
        ],
        "example": {
            "question": "Fe₂O₃ + 3CO → 2Fe + 3CO₂. Atom economy of Fe? (Ar: Fe = 56, C = 12, O = 16)",
            "steps": [
                {"label": "Coefficients", "content": "<p>\\(2\\text{Fe} = 112\\); \\(3\\text{CO}_2 = 3 \\times 44 = 132\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(\\frac{112}{112 + 132} \\times 100\\)</p>"},
                {"label": "Check", "content": "<p>\\(112 + 132 = 244\\), \\(\\frac{112}{244} \\times 100 = 45.9\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>45.9%</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---- guided (opener + teach walks) ----
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "You bake a tray meant to give 20 cookies.<br>5 of them burn and go in the bin.",
        "steps": [
            box("How many good cookies do you have? 20 − 5 = ", 15, "Take the 5 burnt ones off the 20 you planned.", say="No chemistry yet, just common sense."),
            box("As a percentage of the 20 you planned: (15 ÷ 20) × 100 = ", 75, "15 out of 20, written as a percentage.", say="Now as a share of what you set out to make:"),
            say("That is exactly <strong>percentage yield</strong>: what you actually got, over the most you could have got, times 100. In a reaction the 'cookies' are your product. <strong>Atom economy</strong> is the same fraction idea but for atoms: of all the atoms in the products, what share end up in the one you wanted?")
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A student expected to make 5.0 g of product but collected 4.0 g. Calculate the percentage yield.",
            "steps": [
                say("Percentage yield = (actual ÷ theoretical) × 100. Sort out which number is which first."),
                box("Which is the actual amount collected? Write it: ", 4.0, "The amount you really got.", post=" g"),
                box("Which is the theoretical maximum? Write it: ", 5.0, "The amount expected.", post=" g"),
                box("percentage yield = (4.0 ÷ 5.0) × 100 = ", 80, "Actual over theoretical, times 100.", phase="substitute"),
                box("Check: 80% of 5.0 g = 0.80 × 5.0 = ", 4.0, "Should give back the mass collected.", done="4.0 g, matches. Yield = 80%.")
            ]
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "6.0 g of magnesium burns: 2Mg + O₂ → 2MgO. The student collects 8.0 g of MgO. Calculate the percentage yield. (Ar: Mg = 24, O = 16)",
            "steps": [
                say("Percentage yield from a mass: convert to moles, use the ratio to get the theoretical mass, then compare."),
                box("moles of Mg = 6.0 ÷ 24 = ", 0.25, "Mass over Ar."),
                box("2 Mg : 2 MgO is 1 : 1, so moles of MgO = ", 0.25, "One to one ratio."),
                box("theoretical mass of MgO = 0.25 × 40 = ", 10, "Moles times Mr (MgO = 40)."),
                box("percentage yield = (8.0 ÷ 10) × 100 = ", 80, "Actual over theoretical, times 100.", phase="substitute"),
                box("Check: 80% of 10 g = 0.80 × 10 = ", 8, "Should give back the mass collected.", done="8 g, matches. Yield = 80%.")
            ]
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "14.0 g of nitrogen reacts with excess hydrogen: N₂ + 3H₂ → 2NH₃. The student collects 13.6 g of ammonia. Calculate the percentage yield. (Ar: N = 14, H = 1)",
            "steps": [
                say("Percentage yield with a ratio and an Mr to work out: moles, ratio, Mr, theoretical mass, then compare."),
                box("Mr of N₂ = 2 × 14 = ", 28, "Two nitrogen atoms."),
                box("moles of N₂ = 14.0 ÷ 28 = ", 0.5, "Mass over Mr."),
                box("1 N₂ : 2 NH₃, so moles of NH₃ = 0.5 × 2 = ", 1, "Double it for the 1 : 2 ratio."),
                box("Mr of NH₃ = 14 + (3 × 1) = ", 17, "Nitrogen plus three hydrogens."),
                box("theoretical mass of NH₃ = 1 × 17 = ", 17, "Moles times Mr."),
                box("percentage yield = (13.6 ÷ 17) × 100 = ", 80, "Actual over theoretical, times 100.", phase="substitute"),
                box("Check: 80% of 17 g = 0.80 × 17 = ", 13.6, "Should give back the ammonia collected.", done="13.6 g, matches. Yield = 80%.")
            ]
        }
    }
}

with io.open("lesson_higher-calculations-L03@2a30c22d67.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written")
