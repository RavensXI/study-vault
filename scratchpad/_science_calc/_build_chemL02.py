# -*- coding: utf-8 -*-
import json, io

def B(pre, answer, hint, post="", phase=False, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = "substitute"
    if done: d["done"] = done
    if say is not None: d["say"] = say
    return d

def S(say):
    return {"say": say}

def M(pattern, expect, message):
    return {"pattern": pattern, "check": "common", "expect": expect, "message": message}

pd = {}

pd["method_card"] = {
    "title": "Balancing Equations and Reacting Masses",
    "steps": [
        "Balance the equation, then read the mole ratio from the big numbers in front.",
        "Convert the known mass to moles: moles = mass ÷ M_r.",
        "Use the mole ratio to find moles of the substance you want.",
        "Convert back to mass (mass = moles × M_r) and state the unit."
    ],
    "content": "<p>Reacting-mass questions use one fixed method. Start from a <strong>balanced</strong> equation: the numbers in front of each formula give the mole ratio, the bridge between substances. Do not confuse these coefficients with the small subscript numbers.</p><p>Given a mass, turn it into moles first (moles = mass ÷ \\(M_r\\)). Use the ratio to find moles of the target substance, then convert back to a mass with its own \\(M_r\\). Check whether the question wants conservation of mass (mass in = mass out) or a gas volume (moles × 24 dm³ at room conditions).</p>"
}

pd["topic_links"] = {"prerequisites": ["relative-formula-mass-and-moles"]}

pd["exam_context"] = {
    "marks": "3 to 5 per calculation",
    "paper": "Paper 1 (Chemistry)",
    "frequency": "Almost every exam. A common 4 to 5 mark multi-step question."
}

# ---------- BRONZE ----------
bronze = []

# b0: Na + Cl2 -> NaCl, front of Na = 2
bronze.append({
    "display": "Balance this equation: Na + Cl₂ → NaCl. What number goes in front of Na?",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "unit": "", "equation_hint": "\\(\\text{atoms on left} = \\text{atoms on right}\\)",
    "hint": "Two chlorine atoms on the left force two NaCl on the right, which then needs two Na.",
    "misconceptions": [
        M("unbalanced", 1, "Cl₂ has 2 chlorine atoms, but each NaCl holds only 1. You need 2NaCl, so you also need 2Na: 2Na + Cl₂ → 2NaCl. Answer 1 leaves chlorine unbalanced.")
    ],
    "guided_steps": [
        S("Count the atoms. Cl₂ on the left has 2 chlorine atoms, but NaCl on the right has only 1."),
        B("To match chlorine, how many NaCl do we need on the right? NaCl = ", 2, "Two Cl atoms on the left need two Cl atoms on the right."),
        B("2NaCl now contains 2 sodium atoms, so how many Na on the left? Na = ", 2, "Match the sodium: two on the right means two on the left.", phase=True),
        B("Check chlorine: left Cl₂ = 2, right 2 × 1 = ", 2, "Count the chlorine on each side; they must match.", done="Balanced: 2Na + Cl₂ → 2NaCl. Answer for Na is 2.")
    ]
})

# b1: Fe + O2 -> Fe2O3, front of Fe = 4
bronze.append({
    "display": "Balance this equation: Fe + O₂ → Fe₂O₃. What number goes in front of Fe?",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "unit": "", "equation_hint": "\\(\\text{atoms on left} = \\text{atoms on right}\\)",
    "hint": "Balance oxygen first: the smallest number that both 2 and 3 divide into is 6.",
    "misconceptions": [
        M("wrong_coefficient", 2, "Do not copy the small subscript 2 from Fe₂O₃. Balance oxygen first using 6 atoms: 3O₂ and 2Fe₂O₃, which needs 4Fe. Answer 2 leaves the equation unbalanced.")
    ],
    "guided_steps": [
        S("Oxygen is the tricky one. Left O₂ comes in 2s, right Fe₂O₃ has 3 O. The smallest number both divide into is 6."),
        B("How many O₂ gives 6 oxygen atoms? 6 ÷ 2 = ", 3, "Each O₂ is 2 atoms, so divide 6 by 2."),
        B("How many Fe₂O₃ gives 6 oxygen atoms? 6 ÷ 3 = ", 2, "Each Fe₂O₃ has 3 O, so divide 6 by 3."),
        B("2Fe₂O₃ contains 2 × 2 = how many Fe atoms? ", 4, "Two units of Fe₂O₃, each with 2 Fe.", phase=True),
        B("So we need 4Fe on the left. Check oxygen: 3 × 2 = ", 6, "Three O₂, each 2 atoms.", done="Balanced: 4Fe + 3O₂ → 2Fe₂O₃. 4 Fe and 6 O each side.")
    ]
})

# b2: propane combustion, front of O2 = 5  (changed from H2+O2 to break duplicate [2])
bronze.append({
    "display": "Balance this equation: C₃H₈ + O₂ → CO₂ + H₂O. What number goes in front of O₂?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "unit": "", "equation_hint": "\\(\\text{atoms on left} = \\text{atoms on right}\\)",
    "hint": "Balance carbon and hydrogen first, then count all the oxygen on the right.",
    "misconceptions": [
        M("forgot_source", 3, "Count oxygen from BOTH products. 3CO₂ gives 6 O and 4H₂O gives 4 O, so 10 in total. 10 ÷ 2 = 5 molecules of O₂. Counting only the CO₂ oxygen gives 3.")
    ],
    "guided_steps": [
        S("Balance carbon and hydrogen first. 3 carbons need 3CO₂; 8 hydrogens need 4H₂O."),
        B("Oxygen from 3CO₂ is 3 × 2 = ", 6, "Each CO₂ holds 2 oxygen atoms."),
        B("Oxygen from 4H₂O is 4 × 1 = ", 4, "Each H₂O holds 1 oxygen atom."),
        B("Total oxygen atoms on the right = 6 + 4 = ", 10, "Add the oxygen from both products."),
        B("Each O₂ gives 2 atoms, so O₂ needed = 10 ÷ 2 = ", 5, "Divide the total oxygen atoms by 2.", phase=True),
        B("Check: 5 × 2 = ", 10, "Five O₂, each 2 atoms, should match the 10 on the right.", done="Balanced: C₃H₈ + 5O₂ → 3CO₂ + 4H₂O. Answer for O₂ is 5.")
    ]
})

# b3: MC ratio Mg:MgO -> 1:1 (index 2); fixed ambiguous 2:2 option to 3:1
bronze.append({
    "display": "In the equation 2Mg + O₂ → 2MgO, what is the mole ratio of Mg to MgO in its simplest form?",
    "options": ["1 : 2", "2 : 1", "1 : 1", "3 : 1"],
    "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "unit": "", "equation_hint": "\\(\\text{mole ratio} = \\text{coefficients in balanced equation}\\)",
    "hint": "Take the coefficients 2 and 2 and simplify the ratio.",
    "misconceptions": [
        M("wrong_ratio", None, "The coefficients are 2Mg and 2MgO, giving 2:2. In its simplest form that is 1:1.")
    ]
})

# b4: ratio, moles NH3 from 3 mol N2 = 6 (changed from 1 mol->2 to break duplicate)
bronze.append({
    "display": "In the equation N₂ + 3H₂ → 2NH₃, how many moles of NH₃ are produced from 3 mol of N₂?",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "unit": "mol", "equation_hint": "\\(\\text{mole ratio} = \\text{coefficients in balanced equation}\\)",
    "hint": "Use only the N₂ and NH₃ coefficients: the ratio is 1 to 2.",
    "misconceptions": [
        M("wrong_ratio", 3, "Do not assume a 1:1 ratio. The coefficients give N₂ : NH₃ = 1 : 2, so 3 mol of N₂ makes 6 mol of NH₃. Answer 3 uses the wrong ratio.")
    ],
    "guided_steps": [
        S("Compare N₂ and NH₃ only: their coefficients are 1 and 2, so the ratio is 1 : 2."),
        B("Ratio N₂ : NH₃ = 1 : ", 2, "Read the number in front of NH₃."),
        B("3 mol N₂ × 2 = ", 6, "Multiply the moles of N₂ by 2 to get moles of NH₃.", post=" mol", phase=True),
        B("Check: twice as many NH₃ as N₂, so 3 × 2 = ", 6, "Confirm the doubling.", done="6 mol of NH₃.")
    ]
})

# b5: CaCO3 -> CaO + CO2, moles CO2 from 3 mol = 3
bronze.append({
    "display": "In the equation CaCO₃ → CaO + CO₂, how many moles of CO₂ are produced from 3 mol of CaCO₃?",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "unit": "mol", "equation_hint": "\\(\\text{mole ratio} = \\text{coefficients in balanced equation}\\)",
    "hint": "A 1:1 ratio means the moles coming out equal the moles going in.",
    "misconceptions": [
        M("wrong_ratio", 1, "The coefficients are all 1, so CaCO₃ : CO₂ is 1 : 1. That means 3 mol of CaCO₃ gives 3 mol of CO₂, not 1.")
    ],
    "guided_steps": [
        S("Balanced equation CaCO₃ → CaO + CO₂. Every coefficient is 1, so CaCO₃ : CO₂ is 1 : 1."),
        B("Ratio CaCO₃ : CO₂ = 1 : ", 1, "Read the number in front of CO₂."),
        B("Start with 3 mol CaCO₃. With a 1:1 ratio: 3 × 1 = ", 3, "Multiply the moles by 1.", post=" mol", phase=True),
        B("Check: moles out equals moles in, so 3 mol CaCO₃ gives ", 3, "Same number of moles both ways.", post=" mol", done="3 mol of CO₂.")
    ]
})

# b6: 4.8 g Mg -> MgO = 8 g
bronze.append({
    "display": "4.8 g of magnesium reacts with oxygen: 2Mg + O₂ → 2MgO. Calculate the mass of MgO produced. (\\(A_r\\): Mg = 24, O = 16)",
    "solutions": [8], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "Find moles of Mg, keep the same moles of MgO (1:1), then multiply by Mr of MgO.",
    "misconceptions": [
        M("used_wrong_mr", 4.8, "Convert moles of MgO to mass using Mr of MgO (40), not Mr of Mg (24). 0.2 × 40 = 8 g. Multiplying by 24 gives 4.8 g."),
        M("wrong_mr", 3.2, "Mr of MgO = 24 + 16 = 40, not 16. Using only the oxygen (16) gives 0.2 × 16 = 3.2 g.")
    ],
    "guided_steps": [
        S("Balanced equation 2Mg + O₂ → 2MgO. Mg : MgO is 2 : 2, which is 1 : 1."),
        B("moles of Mg = mass ÷ Mr = 4.8 ÷ 24 = ", 0.2, "Divide the mass of Mg by its Mr.", post=" mol"),
        B("Ratio is 1:1, so moles of MgO = ", 0.2, "Same number of moles as Mg.", post=" mol"),
        B("Mr of MgO = 24 + 16 = ", 40, "Add the Ar values of Mg and O.", phase=True),
        B("mass of MgO = moles × Mr = 0.2 × 40 = ", 8, "Multiply moles of MgO by its Mr.", post=" g"),
        B("Check: 8 ÷ 40 = ", 0.2, "Divide the mass back by Mr to recover the moles.", post=" mol", done="Back to 0.2 mol MgO, so the mass is 8 g.")
    ]
})

# b7: 2.4 g Mg -> H2 = 0.2 g
bronze.append({
    "display": "Magnesium reacts with hydrochloric acid: Mg + 2HCl → MgCl₂ + H₂. Calculate the mass of hydrogen gas produced from 2.4 g of magnesium. (\\(A_r\\): Mg = 24, H = 1)",
    "solutions": [0.2], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "Moles of Mg equals moles of H₂; convert with Mr of H₂ = 2.",
    "misconceptions": [
        M("used_wrong_mr", 2.4, "Use Mr of H₂ (2), not Mr of Mg. 0.1 mol × 2 = 0.2 g. Multiplying by 24 gives 2.4 g."),
        M("forgot_diatomic", 0.1, "Hydrogen gas is H₂, so its Mr is 2, not 1. 0.1 mol × 2 = 0.2 g, not 0.1 g.")
    ],
    "guided_steps": [
        S("Balanced equation Mg + 2HCl → MgCl₂ + H₂. Mg : H₂ is 1 : 1."),
        B("moles of Mg = mass ÷ Mr = 2.4 ÷ 24 = ", 0.1, "Divide the mass of Mg by its Mr.", post=" mol"),
        B("Ratio is 1:1, so moles of H₂ = ", 0.1, "Same number of moles as Mg.", post=" mol"),
        B("Mr of H₂ = 1 + 1 = ", 2, "Hydrogen gas is diatomic, so add two H atoms.", phase=True),
        B("mass of H₂ = moles × Mr = 0.1 × 2 = ", 0.2, "Multiply moles of H₂ by its Mr.", post=" g"),
        B("Check: 0.2 ÷ 2 = ", 0.1, "Divide the mass back by Mr to recover the moles.", post=" mol", done="Back to 0.1 mol H₂, so the mass is 0.2 g.")
    ]
})

# ---------- SILVER ----------
silver = []

# s0: 25 g CaCO3 -> CO2 = 11 g
silver.append({
    "display": "Calcium carbonate decomposes: CaCO₃ → CaO + CO₂. Calculate the mass of CO₂ produced from 25 g of CaCO₃. (\\(A_r\\): Ca = 40, C = 12, O = 16)",
    "solutions": [11], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "Mr of CaCO₃ is 100; the ratio to CO₂ is 1:1; Mr of CO₂ is 44.",
    "misconceptions": [
        M("used_wrong_mr", 25, "Convert back with Mr of CO₂ (44), not Mr of CaCO₃ (100). 0.25 × 44 = 11 g. Using 100 gives 25 g, the starting mass."),
        M("wrong_product", 14, "The question asks for CO₂ (Mr 44), not CaO (Mr 56). 0.25 × 44 = 11 g; 0.25 × 56 = 14 g is the mass of CaO.")
    ],
    "guided_steps": [
        S("Balanced equation CaCO₃ → CaO + CO₂, a 1 : 1 ratio."),
        B("Mr of CaCO₃ = 40 + 12 + (3 × 16) = ", 100, "Add Ca, C and three O atoms."),
        B("moles of CaCO₃ = 25 ÷ 100 = ", 0.25, "Divide the mass by Mr.", post=" mol"),
        B("Ratio 1:1, so moles of CO₂ = ", 0.25, "Same number of moles.", post=" mol"),
        B("Mr of CO₂ = 12 + (2 × 16) = ", 44, "Add carbon and two oxygen atoms.", phase=True),
        B("mass of CO₂ = 0.25 × 44 = ", 11, "Multiply moles of CO₂ by its Mr.", post=" g"),
        B("Check: 11 ÷ 44 = ", 0.25, "Divide back to recover the moles.", post=" mol", done="Back to 0.25 mol CO₂, so the mass is 11 g.")
    ]
})

# s1: 4.6 g Na -> NaOH = 8 g
silver.append({
    "display": "Sodium reacts with water: 2Na + 2H₂O → 2NaOH + H₂. Calculate the mass of NaOH produced from 4.6 g of sodium. (\\(A_r\\): Na = 23, O = 16, H = 1)",
    "solutions": [8], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "The 2:2 ratio is 1:1; convert back with Mr of NaOH = 40.",
    "misconceptions": [
        M("wrong_ratio", 4, "Na : NaOH is 2 : 2, which is 1 : 1. Halving the moles by mistake gives 0.1 mol and 4 g instead of 0.2 mol and 8 g."),
        M("used_wrong_mr", 4.6, "Convert back with Mr of NaOH (40), not Ar of Na (23). 0.2 × 40 = 8 g; 0.2 × 23 = 4.6 g is the starting mass.")
    ],
    "guided_steps": [
        S("Balanced equation 2Na + 2H₂O → 2NaOH + H₂. Na : NaOH is 2 : 2, which is 1 : 1."),
        B("moles of Na = 4.6 ÷ 23 = ", 0.2, "Divide the mass of Na by its Ar.", post=" mol"),
        B("Ratio 1:1, so moles of NaOH = ", 0.2, "Same number of moles as Na.", post=" mol"),
        B("Mr of NaOH = 23 + 16 + 1 = ", 40, "Add Na, O and H.", phase=True),
        B("mass of NaOH = 0.2 × 40 = ", 8, "Multiply moles of NaOH by its Mr.", post=" g"),
        B("Check: 8 ÷ 40 = ", 0.2, "Divide back to recover the moles.", post=" mol", done="Back to 0.2 mol NaOH, so the mass is 8 g.")
    ]
})

# s2: 32 g Fe2O3 -> Fe = 22.4 g
silver.append({
    "display": "Iron(III) oxide is reduced: Fe₂O₃ + 3CO → 2Fe + 3CO₂. Calculate the mass of iron produced from 32 g of Fe₂O₃. (\\(A_r\\): Fe = 56, O = 16)",
    "solutions": [22.4], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "The ratio Fe₂O₃ to Fe is 1:2, so double the moles before converting.",
    "misconceptions": [
        M("wrong_ratio", 11.2, "The ratio Fe₂O₃ : Fe is 1 : 2, so double the moles. 0.2 × 2 = 0.4 mol Fe, giving 22.4 g. Using 1:1 gives only 11.2 g."),
        M("wrong_mr", 32, "Mr of Fe₂O₃ = (2 × 56) + (3 × 16) = 160, not 112. Leaving out the oxygen makes the answer come out as 32 g, the whole starting mass, instead of 22.4 g.")
    ],
    "guided_steps": [
        S("Balanced equation Fe₂O₃ + 3CO → 2Fe + 3CO₂. Fe₂O₃ : Fe is 1 : 2."),
        B("Mr of Fe₂O₃ = (2 × 56) + (3 × 16) = ", 160, "Add two Fe and three O atoms."),
        B("moles of Fe₂O₃ = 32 ÷ 160 = ", 0.2, "Divide the mass by Mr.", post=" mol"),
        B("Ratio 1:2, so moles of Fe = 0.2 × 2 = ", 0.4, "Double the moles because 1 Fe₂O₃ makes 2 Fe.", post=" mol"),
        B("Mr of Fe = ", 56, "Iron is an element, so its Mr is just its Ar.", phase=True),
        B("mass of Fe = 0.4 × 56 = ", 22.4, "Multiply moles of Fe by its Ar.", post=" g"),
        B("Check: 22.4 ÷ 56 = ", 0.4, "Divide back to recover the moles.", post=" mol", done="Back to 0.4 mol Fe, so the mass is 22.4 g.")
    ]
})

# s3: 5.4 g Al -> Cu = 19.2 g
silver.append({
    "display": "Aluminium reacts with copper sulfate: 2Al + 3CuSO₄ → Al₂(SO₄)₃ + 3Cu. Calculate the mass of copper produced from 5.4 g of aluminium. (\\(A_r\\): Al = 27, Cu = 64)",
    "solutions": [19.2], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "The ratio Al to Cu is 2:3, so multiply moles of Al by 3 then divide by 2.",
    "misconceptions": [
        M("wrong_ratio", 12.8, "The ratio Al : Cu is 2 : 3, not 1 : 1. Moles Cu = 0.2 × 3 ÷ 2 = 0.3, giving 19.2 g. A 1:1 ratio gives only 12.8 g.")
    ],
    "guided_steps": [
        S("Balanced equation 2Al + 3CuSO₄ → Al₂(SO₄)₃ + 3Cu. Al : Cu is 2 : 3."),
        B("moles of Al = 5.4 ÷ 27 = ", 0.2, "Divide the mass of Al by its Ar.", post=" mol"),
        B("Apply the ratio: 0.2 × 3 = ", 0.6, "Multiply by the Cu coefficient, 3."),
        B("then ÷ 2 = ", 0.3, "Divide by the Al coefficient, 2, to get moles of Cu.", post=" mol"),
        B("Mr of Cu = ", 64, "Copper is an element, so its Mr is just its Ar.", phase=True),
        B("mass of Cu = 0.3 × 64 = ", 19.2, "Multiply moles of Cu by its Ar.", post=" g"),
        B("Check: 19.2 ÷ 64 = ", 0.3, "Divide back to recover the moles.", post=" mol", done="Back to 0.3 mol Cu, so the mass is 19.2 g.")
    ]
})

# s4: 5.6 g N2 -> NH3 = 6.8 g
silver.append({
    "display": "Nitrogen reacts with hydrogen: N₂ + 3H₂ → 2NH₃. Calculate the mass of ammonia (NH₃) produced from 5.6 g of nitrogen. (\\(A_r\\): N = 14, H = 1)",
    "solutions": [6.8], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "Mr of N₂ is 28; the ratio to NH₃ is 1:2; Mr of NH₃ is 17.",
    "misconceptions": [
        M("wrong_ratio", 3.4, "The ratio N₂ : NH₃ is 1 : 2, so double the moles. 0.2 × 2 = 0.4 mol NH₃, giving 6.8 g. A 1:1 ratio gives only 3.4 g."),
        M("used_wrong_mr", 13.6, "Nitrogen gas is N₂ with Mr 28, not 14. Using 14 doubles the moles and gives 13.6 g.")
    ],
    "guided_steps": [
        S("Balanced equation N₂ + 3H₂ → 2NH₃. N₂ : NH₃ is 1 : 2."),
        B("Mr of N₂ = 14 + 14 = ", 28, "Nitrogen gas is diatomic, so add two N atoms."),
        B("moles of N₂ = 5.6 ÷ 28 = ", 0.2, "Divide the mass by Mr.", post=" mol"),
        B("Ratio 1:2, so moles of NH₃ = 0.2 × 2 = ", 0.4, "Double the moles because 1 N₂ makes 2 NH₃.", post=" mol"),
        B("Mr of NH₃ = 14 + (3 × 1) = ", 17, "Add nitrogen and three hydrogen atoms.", phase=True),
        B("mass of NH₃ = 0.4 × 17 = ", 6.8, "Multiply moles of NH₃ by its Mr.", post=" g"),
        B("Check: 6.8 ÷ 17 = ", 0.4, "Divide back to recover the moles.", post=" mol", done="Back to 0.4 mol NH₃, so the mass is 6.8 g.")
    ]
})

# s5: 16 g CuO -> CuSO4 = 32 g
silver.append({
    "display": "Copper oxide reacts with sulfuric acid: CuO + H₂SO₄ → CuSO₄ + H₂O. Calculate the mass of copper sulfate (CuSO₄) produced from 16 g of CuO. (\\(A_r\\): Cu = 64, O = 16, S = 32, H = 1)",
    "solutions": [32], "calculator": True, "input_type": "single_value",
    "unit": "g", "equation_hint": "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\)",
    "hint": "The ratio is 1:1; convert back with Mr of CuSO₄ = 160.",
    "misconceptions": [
        M("used_wrong_mr", 16, "Convert back with Mr of CuSO₄ (160), not Mr of CuO (80). 0.2 × 160 = 32 g. Using 80 gives 16 g, the starting mass."),
        M("wrong_mr", 19.2, "Mr of CuSO₄ = 64 + 32 + (4 × 16) = 160. Forgetting all four oxygens (using 96) gives 0.2 × 96 = 19.2 g.")
    ],
    "guided_steps": [
        S("Balanced equation CuO + H₂SO₄ → CuSO₄ + H₂O, a 1 : 1 ratio."),
        B("Mr of CuO = 64 + 16 = ", 80, "Add copper and oxygen."),
        B("moles of CuO = 16 ÷ 80 = ", 0.2, "Divide the mass by Mr.", post=" mol"),
        B("Ratio 1:1, so moles of CuSO₄ = ", 0.2, "Same number of moles.", post=" mol"),
        B("Mr of CuSO₄ = 64 + 32 + (4 × 16) = ", 160, "Add Cu, S and four O atoms.", phase=True),
        B("mass of CuSO₄ = 0.2 × 160 = ", 32, "Multiply moles of CuSO₄ by its Mr.", post=" g"),
        B("Check: 32 ÷ 160 = ", 0.2, "Divide back to recover the moles.", post=" mol", done="Back to 0.2 mol CuSO₄, so the mass is 32 g.")
    ]
})

# ---------- GOLD ----------
gold = []

# g0: conservation of mass, H2 = 0.2 g
gold.append({
    "display": "6.5 g of zinc reacts with excess hydrochloric acid: Zn + 2HCl → ZnCl₂ + H₂. The mass of ZnCl₂ produced is 13.6 g. Calculate the mass of hydrogen gas produced using conservation of mass. (The total mass of HCl used is 7.3 g.)",
    "solutions": [0.2], "calculator": True, "input_type": "single_value",
    "unit": "g",
    "hint": "Total reactant mass equals total product mass, so H₂ = (6.5 + 7.3) − 13.6.",
    "misconceptions": [
        M("forgot_reactant", 7.1, "Include every reactant mass. Total in = 6.5 + 7.3 = 13.8 g, so H₂ = 13.8 − 13.6 = 0.2 g. Using only the zinc (13.6 − 6.5) gives 7.1 g."),
        M("forgot_conservation", None, "You do not need Mr here. Conservation of mass means total reactant mass equals total product mass.")
    ],
    "guided_steps": [
        S("Conservation of mass: total mass of reactants = total mass of products. Nothing is lost."),
        B("total reactant mass = 6.5 + 7.3 = ", 13.8, "Add the zinc and the hydrochloric acid masses.", post=" g"),
        S("The products are ZnCl₂ (13.6 g) plus the hydrogen gas we want."),
        B("So 13.8 = 13.6 + H₂. mass of H₂ = 13.8 − 13.6 = ", 0.2, "Subtract the known product mass from the total.", post=" g", phase=True),
        B("Check: add the products back, 13.6 + 0.2 = ", 13.8, "The products must total the reactant mass.", post=" g", done="Equals the reactant mass, so the hydrogen is 0.2 g.")
    ]
})

# g1: MC limiting reactant -> Mg (index 0)  (converted from text solution ["Mg"])
gold.append({
    "display": "12 g of magnesium reacts with 12 g of oxygen: 2Mg + O₂ → 2MgO. Which is the limiting reactant? (\\(A_r\\): Mg = 24, O = 16)",
    "options": ["Mg", "O₂"],
    "solutions": [0], "calculator": True, "input_type": "multiple_choice",
    "unit": "",
    "hint": "Find moles of each reactant and use the 2:1 ratio to see which runs out first.",
    "misconceptions": [
        M("wrong_answer", None, "Moles Mg = 12 ÷ 24 = 0.5. Moles O₂ = 12 ÷ 32 = 0.375. The ratio needs 2 Mg per 1 O₂, so 0.5 mol Mg needs only 0.25 mol O₂. Oxygen is in excess, so Mg is limiting.")
    ]
})

# g2: mass MgO from limiting Mg = 20 g
gold.append({
    "display": "12 g of magnesium reacts with 12 g of oxygen: 2Mg + O₂ → 2MgO. Magnesium is the limiting reactant. Calculate the mass of MgO formed. (\\(A_r\\): Mg = 24, O = 16)",
    "solutions": [20], "calculator": True, "input_type": "single_value",
    "unit": "g",
    "hint": "Base the answer on Mg, the limiting reactant, using a 1:1 ratio to MgO.",
    "misconceptions": [
        M("used_excess", 30, "Base the amount on the limiting reactant, Mg (0.5 mol), not the excess O₂. 0.5 mol MgO × 40 = 20 g. Using the 0.375 mol of O₂ gives 30 g."),
        M("wrong_mr", 12, "Mr of MgO = 24 + 16 = 40. Using only the magnesium (24) gives 0.5 × 24 = 12 g.")
    ],
    "guided_steps": [
        S("Magnesium is the limiting reactant, so base everything on the 12 g of Mg. The ratio 2Mg : 2MgO is 1 : 1."),
        B("moles of Mg = 12 ÷ 24 = ", 0.5, "Divide the mass of Mg by its Ar.", post=" mol"),
        B("Ratio 1:1, so moles of MgO = ", 0.5, "Same number of moles as Mg.", post=" mol"),
        B("Mr of MgO = 24 + 16 = ", 40, "Add magnesium and oxygen.", phase=True),
        B("mass of MgO = 0.5 × 40 = ", 20, "Multiply moles of MgO by its Mr.", post=" g"),
        B("Check: 20 ÷ 40 = ", 0.5, "Divide back to recover the moles.", post=" mol", done="Back to 0.5 mol MgO, so the mass is 20 g.")
    ]
})

# g3: 2.7 g Al excess CuSO4 -> Cu = 9.6 g
gold.append({
    "display": "In the reaction 2Al + 3CuSO₄ → Al₂(SO₄)₃ + 3Cu, a student reacts 2.7 g of aluminium with excess copper sulfate solution. Calculate the mass of copper produced. (\\(A_r\\): Al = 27, Cu = 64)",
    "solutions": [9.6], "calculator": True, "input_type": "single_value",
    "unit": "g",
    "hint": "The ratio Al to Cu is 2:3; multiply moles of Al by 3 then divide by 2.",
    "misconceptions": [
        M("wrong_ratio", 6.4, "The ratio Al : Cu is 2 : 3, not 1 : 1. Moles Cu = 0.1 × 3 ÷ 2 = 0.15, giving 9.6 g. A 1:1 ratio gives only 6.4 g.")
    ],
    "guided_steps": [
        S("Balanced equation 2Al + 3CuSO₄ → Al₂(SO₄)₃ + 3Cu. Al : Cu is 2 : 3. The copper sulfate is in excess, so aluminium sets the amount."),
        B("moles of Al = 2.7 ÷ 27 = ", 0.1, "Divide the mass of Al by its Ar.", post=" mol"),
        B("Apply the ratio: 0.1 × 3 = ", 0.3, "Multiply by the Cu coefficient, 3."),
        B("then ÷ 2 = ", 0.15, "Divide by the Al coefficient, 2, to get moles of Cu.", post=" mol"),
        B("Mr of Cu = ", 64, "Copper is an element, so its Mr is just its Ar.", phase=True),
        B("mass of Cu = 0.15 × 64 = ", 9.6, "Multiply moles of Cu by its Ar.", post=" g"),
        B("Check: 9.6 ÷ 64 = ", 0.15, "Divide back to recover the moles.", post=" mol", done="Back to 0.15 mol Cu, so the mass is 9.6 g.")
    ]
})

# g4: 6.5 g Zn -> volume H2 = 2.4 dm3
gold.append({
    "display": "Zinc reacts with hydrochloric acid: Zn + 2HCl → ZnCl₂ + H₂. 6.5 g of zinc is added to excess acid. Calculate the volume of hydrogen gas produced at room temperature and pressure, where 1 mole of any gas occupies 24 dm³. (\\(A_r\\): Zn = 65, H = 1)",
    "solutions": [2.4], "calculator": True, "input_type": "single_value",
    "unit": "dm³",
    "hint": "Find moles of Zn, keep the same moles of H₂, then multiply by 24 dm³.",
    "misconceptions": [
        M("forgot_volume", 0.1, "Do not stop at moles. Multiply moles of H₂ by 24 dm³: 0.1 × 24 = 2.4 dm³. Answer 0.1 is the moles, not the volume."),
        M("forgot_moles", 156, "Convert the mass to moles first. Moles Zn = 6.5 ÷ 65 = 0.1, then 0.1 × 24 = 2.4 dm³. Multiplying the mass by 24 gives 156.")
    ],
    "guided_steps": [
        S("Balanced equation Zn + 2HCl → ZnCl₂ + H₂. Zn : H₂ is 1 : 1. Gas volume uses moles × 24 dm³, not mass."),
        B("moles of Zn = 6.5 ÷ 65 = ", 0.1, "Divide the mass of Zn by its Ar.", post=" mol"),
        B("Ratio 1:1, so moles of H₂ = ", 0.1, "Same number of moles as Zn.", post=" mol"),
        B("volume of H₂ = moles × 24 = 0.1 × 24 = ", 2.4, "Multiply the moles of gas by 24 dm³.", post=" dm³", phase=True),
        B("Check: 2.4 ÷ 24 = ", 0.1, "Divide the volume back by 24 to recover the moles.", post=" mol", done="Back to 0.1 mol H₂, so the volume is 2.4 dm³.")
    ]
})

# g5: 4 g Ca -> Ca(OH)2 = 7.4 g
gold.append({
    "display": "Calcium reacts with water: Ca + 2H₂O → Ca(OH)₂ + H₂. Calculate the mass of calcium hydroxide produced from 4 g of calcium. (\\(A_r\\): Ca = 40, O = 16, H = 1)",
    "solutions": [7.4], "calculator": True, "input_type": "single_value",
    "unit": "g",
    "hint": "Remember Ca(OH)₂ has Mr = 40 + 2 × (16 + 1) = 74.",
    "misconceptions": [
        M("forgot_brackets", 5.7, "Ca(OH)₂ has TWO OH groups: Mr = 40 + 2 × (16 + 1) = 74, not 57. 0.1 × 74 = 7.4 g; using 57 gives 5.7 g."),
        M("used_wrong_mr", 4, "Convert back with Mr of Ca(OH)₂ (74), not Ar of Ca (40). 0.1 × 74 = 7.4 g; 0.1 × 40 = 4 g is the starting mass.")
    ],
    "guided_steps": [
        S("Balanced equation Ca + 2H₂O → Ca(OH)₂ + H₂. Ca : Ca(OH)₂ is 1 : 1."),
        B("moles of Ca = 4 ÷ 40 = ", 0.1, "Divide the mass of Ca by its Ar.", post=" mol"),
        B("Ratio 1:1, so moles of Ca(OH)₂ = ", 0.1, "Same number of moles as Ca.", post=" mol"),
        B("Mr of Ca(OH)₂ = 40 + 2 × (16 + 1) = ", 74, "Multiply the whole OH bracket by 2, then add calcium.", phase=True),
        B("mass of Ca(OH)₂ = 0.1 × 74 = ", 7.4, "Multiply moles of Ca(OH)₂ by its Mr.", post=" g"),
        B("Check: 7.4 ÷ 74 = ", 0.1, "Divide back to recover the moles.", post=" mol", done="Back to 0.1 mol Ca(OH)₂, so the mass is 7.4 g.")
    ]
})

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Balance an equation by counting atoms, or read a mole ratio and do a single 1:1 mass conversion.",
    "silver_description": "Convert a mass to moles, apply the mole ratio, then convert back to the mass of a different substance.",
    "gold_description": "Multi-step work: limiting reactants, gas volumes, or a mass found by conservation of mass."
}

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: balance the equation and read the ratio",
        "steps": [
            "Balance by counting atoms. The big number in front multiplies every atom in that formula; never change the small subscript numbers.",
            "The balanced coefficients ARE the mole ratio. When it is 1:1, moles out equals moles in.",
            "For a mass, find moles with moles = mass ÷ \\(M_r\\), then use the ratio."
        ],
        "example": {
            "question": "Balance this equation: H₂ + Cl₂ → HCl. What number goes in front of HCl?",
            "steps": [
                {"label": "Count atoms", "content": "<p>Left: 2 H and 2 Cl. Right: 1 H and 1 Cl.</p>"},
                {"label": "Balance", "content": "<p>Double the HCl to get 2 H and 2 Cl on the right.</p>"},
                {"label": "Check", "content": "<p>Left 2 H and 2 Cl; right 2HCl = 2 H and 2 Cl. Balanced.</p>"},
                {"label": "Answer", "content": "<p><strong>2</strong>H₂ + Cl₂... front of HCl = <strong>2</strong></p>", "is_answer": True, "isAnswer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert to moles, apply the ratio, convert back",
        "steps": [
            "Find \\(M_r\\) of the substance you know, then moles = mass ÷ \\(M_r\\).",
            "Multiply by the mole ratio from the balanced equation to get moles of the substance you want.",
            "Convert back with mass = moles × \\(M_r\\), using the \\(M_r\\) of the NEW substance."
        ],
        "example": {
            "question": "2Na + 2H₂O → 2NaOH + H₂. Mass of NaOH from 2.3 g of Na? (Ar: Na = 23, O = 16, H = 1)",
            "steps": [
                {"label": "Moles of Na", "content": "<p>moles = 2.3 ÷ 23 = 0.1 mol</p>"},
                {"label": "Apply the ratio", "content": "<p>Na : NaOH is 2 : 2 = 1 : 1, so 0.1 mol NaOH.</p>"},
                {"label": "Convert to mass", "content": "<p>\\(M_r\\) of NaOH = 40. Mass = 0.1 × 40.</p>"},
                {"label": "Check", "content": "<p>4 ÷ 40 = 0.1 mol, matching the moles found.</p>"},
                {"label": "Answer", "content": "<p><strong>4 g</strong> of NaOH</p>", "is_answer": True, "isAnswer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: limiting reactants, gas volumes and conservation",
        "steps": [
            "With two given masses, find moles of each and use the ratio to see which runs out first. That is the limiting reactant.",
            "Base the product amount on the limiting reactant only.",
            "For a gas, volume = moles × 24 dm³. For a missing mass, use conservation: reactant mass in = product mass out."
        ],
        "example": {
            "question": "Mg + 2HCl → MgCl₂ + H₂. Volume of H₂ at room conditions from 0.6 g of Mg? (Ar: Mg = 24, 1 mol gas = 24 dm³)",
            "steps": [
                {"label": "Moles of Mg", "content": "<p>moles = 0.6 ÷ 24 = 0.025 mol</p>"},
                {"label": "Apply the ratio", "content": "<p>Mg : H₂ is 1 : 1, so 0.025 mol H₂.</p>"},
                {"label": "Convert to volume", "content": "<p>Volume = moles × 24 = 0.025 × 24.</p>"},
                {"label": "Check", "content": "<p>0.6 ÷ 0.025 = 24, the Ar of Mg, so the moles are right.</p>"},
                {"label": "Answer", "content": "<p><strong>0.6 dm³</strong> of H₂</p>", "is_answer": True, "isAnswer": True}
            ]
        }
    }
}

# ---------- guided (opener + teach) ----------
pd["guided"] = {
    "opener": {
        "display": "A pancake recipe uses a fixed rule: every 1 cup of flour makes exactly 4 pancakes.<br>Use that rule to answer the two questions below.",
        "steps": [
            B("You use 3 cups of flour. How many pancakes? 3 × 4 = ", 12, "Four pancakes for each cup, three cups."),
            B("You want 20 pancakes. How many cups of flour do you need? 20 ÷ 4 = ", 5, "Work backwards: how many groups of 4 make 20?"),
            S("You just used a fixed <strong>ratio</strong> to convert between two amounts. A balanced chemical equation is exactly this, a recipe. <strong>2Mg + O₂ → 2MgO</strong> means \"2 Mg makes 2 MgO\", a fixed 2:2 ratio. Swap cups and pancakes for moles, and every reacting-mass question is the same move.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "Balance this equation: N₂ + H₂ → NH₃. Work out the number that goes in front of H₂.",
            "steps": [
                S("Start with nitrogen. N₂ on the left has 2 nitrogen atoms, but NH₃ on the right has only 1."),
                B("How many NH₃ do we need for 2 nitrogen atoms? NH₃ = ", 2, "Two N on the left need two N on the right."),
                B("2NH₃ now contains 2 × 3 = how many hydrogen atoms? ", 6, "Each NH₃ has 3 H, and there are 2 of them."),
                B("How many H₂ molecules make 6 hydrogen atoms? 6 ÷ 2 = ", 3, "Each H₂ is 2 atoms, so divide 6 by 2."),
                B("Check nitrogen: left N₂ = 2, right 2 × 1 = ", 2, "Count nitrogen on each side; they must match.", done="Balanced: N₂ + 3H₂ → 2NH₃. The number in front of H₂ is 3. Gone.")
            ]
        },
        "silver": {
            "display": "Zinc oxide is reduced by carbon: 2ZnO + C → 2Zn + CO₂. Calculate the mass of zinc produced from 8.1 g of ZnO. (Ar: Zn = 65, O = 16)",
            "steps": [
                S("The ratio ZnO : Zn is 2 : 2, which is 1 : 1. Find moles of ZnO, keep the same moles of Zn, then convert to mass."),
                B("Mr of ZnO = 65 + 16 = ", 81, "Add zinc and oxygen."),
                B("moles of ZnO = 8.1 ÷ 81 = ", 0.1, "Divide the mass by Mr.", post=" mol"),
                B("Ratio 1:1, so moles of Zn = ", 0.1, "Same number of moles as ZnO.", post=" mol"),
                B("mass of Zn = 0.1 × 65 = ", 6.5, "Multiply moles of Zn by its Ar.", post=" g"),
                B("Check: 6.5 ÷ 65 = ", 0.1, "Divide back to recover the moles.", post=" mol", done="Back to 0.1 mol Zn, so the mass is 6.5 g.")
            ]
        },
        "gold": {
            "display": "Magnesium reacts with acid: Mg + 2HCl → MgCl₂ + H₂. Calculate the volume of hydrogen gas at room conditions from 1.2 g of magnesium. (Ar: Mg = 24, 1 mol gas = 24 dm³)",
            "steps": [
                S("Mg : H₂ is 1 : 1. Find moles of Mg, keep the same moles of H₂, then use volume = moles × 24 dm³."),
                B("moles of Mg = 1.2 ÷ 24 = ", 0.05, "Divide the mass of Mg by its Ar.", post=" mol"),
                B("Ratio 1:1, so moles of H₂ = ", 0.05, "Same number of moles as Mg.", post=" mol"),
                B("volume of H₂ = 0.05 × 24 = ", 1.2, "Multiply the moles of gas by 24 dm³.", post=" dm³"),
                B("Check: 1.2 ÷ 24 = ", 0.05, "Divide the volume back by 24 to recover the moles.", post=" mol", done="Back to 0.05 mol H₂, so the volume is 1.2 dm³.")
            ]
        }
    }
}

pd["related_videos"] = []

# ---------- worked_examples (preserved, em dashes cleaned to colons/full stops) ----------
pd["worked_examples"] = [
    {
        "difficulty": "Bronze",
        "question": "Balance this equation: Mg + O₂ → MgO",
        "steps": [
            {"label": "Step 1: Count atoms on each side", "content": "<p>Left: 1 Mg, 2 O. Right: 1 Mg, 1 O. Oxygen is unbalanced.</p>"},
            {"label": "Step 2: Balance oxygen", "content": "<p>Put a 2 in front of MgO → Mg + O₂ → 2MgO. Now the right has 2 Mg, so balance Mg too.</p>"},
            {"label": "Answer", "content": "<p><strong>2</strong>Mg + O₂ → <strong>2</strong>MgO</p>", "is_answer": True}
        ]
    },
    {
        "difficulty": "Silver",
        "question": "Calcium carbonate decomposes: CaCO₃ → CaO + CO₂. Calculate the mass of calcium oxide (CaO) produced from 25 g of CaCO₃. (Ar: Ca = 40, C = 12, O = 16)",
        "steps": [
            {"label": "Step 1: Equation is already balanced (1:1:1)", "content": "<p>CaCO₃ → CaO + CO₂</p>"},
            {"label": "Step 2: Moles of CaCO₃", "content": "<p>\\(M_r\\) of CaCO₃ = 100. Moles = 25 ÷ 100 = 0.25 mol</p>"},
            {"label": "Step 3: Use the 1:1 ratio", "content": "<p>0.25 mol CaCO₃ → 0.25 mol CaO</p>"},
            {"label": "Step 4: Convert to mass", "content": "<p>\\(M_r\\) of CaO = 56. Mass = 0.25 × 56</p>"},
            {"label": "Answer", "content": "<p>Mass of CaO = <strong>14 g</strong></p>", "is_answer": True}
        ]
    },
    {
        "difficulty": "Gold",
        "question": "12 g of magnesium reacts with 12 g of oxygen: 2Mg + O₂ → 2MgO. Which reactant is the limiting reactant? Calculate the mass of MgO formed. (Ar: Mg = 24, O = 16)",
        "steps": [
            {"label": "Step 1: Find moles of each reactant", "content": "<p>Moles of Mg = 12 ÷ 24 = 0.5 mol. Moles of O₂ = 12 ÷ 32 = 0.375 mol.</p>"},
            {"label": "Step 2: Use the ratio to check which runs out", "content": "<p>Ratio is 2 Mg : 1 O₂. So 0.5 mol Mg needs 0.25 mol O₂. We have 0.375 mol O₂, which is plenty.</p><p>0.375 mol O₂ would need 0.75 mol Mg, but we only have 0.5 mol Mg, so <strong>Mg is limiting</strong>.</p>"},
            {"label": "Step 3: Calculate product from limiting reactant", "content": "<p>0.5 mol Mg → 0.5 mol MgO (2:2 ratio). Mass = 0.5 × 40</p>"},
            {"label": "Answer", "content": "<p>Mg is the limiting reactant. Mass of MgO = <strong>20 g</strong></p>", "is_answer": True}
        ]
    }
]

out = "lesson_chemistry-calculations-L02@4ec4b1a486.json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
