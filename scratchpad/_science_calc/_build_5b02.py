# -*- coding: utf-8 -*-
import json

def num(x):
    # keep ints as ints, floats as floats
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x

def mass_walk(X, m, MrX, Y, MrY, eq, ratio_say, ratio_pre, molesX, molesY, massY):
    """Standard mass->mass reacting mass walk."""
    return [
        {"say": "Reacting mass is one chain: mass to moles, then the ratio, then back to mass. Start with the known substance, %s: moles = mass ÷ Mr." % X},
        {"pre": "moles %s = %s ÷ %s = " % (X, num(m), num(MrX)), "post": "",
         "answer": num(molesX), "hint": "Divide the given mass by the relative formula mass."},
        {"say": ratio_say},
        {"phase": "substitute", "pre": ratio_pre, "post": "",
         "answer": num(molesY), "hint": "Apply the ratio from the balanced equation to the moles you found."},
        {"pre": "mass %s = moles × Mr = %s × %s = " % (Y, num(molesY), num(MrY)), "post": "",
         "answer": num(massY), "hint": "Multiply the moles of %s by its relative formula mass." % Y},
        {"pre": "Check by reversing: %s ÷ %s = " % (num(massY), num(MrY)), "post": "",
         "answer": num(molesY),
         "done": "Back to %s mol %s, matching the ratio, so %s g is right." % (num(molesY), Y, num(massY)),
         "hint": "Mass divided by Mr should return the moles of %s." % Y},
    ]

pd = {}

# ---------------- method_card ----------------
pd["method_card"] = {
    "title": "Balancing Equations and Reacting Masses",
    "steps": [
        "Balance by changing coefficients only, never the formulae.",
        "Convert the known mass to moles: moles = mass ÷ Mr.",
        "Scale the moles using the ratio from the coefficients.",
        "Convert back to mass: mass = moles × Mr.",
    ],
    "content": "<p>Reacting mass questions follow one chain: <strong>mass → moles → ratio → mass</strong>.</p>"
               "<p>First balance the equation, then read the mole ratio from the big numbers in front of each formula. "
               "Convert the mass you are given into moles with moles = mass ÷ Mr, scale by the ratio, and convert back "
               "with mass = moles × Mr.</p>"
               "<p>Show every step: method marks are available even when the final number is wrong. Watch for changing a "
               "subscript instead of a coefficient, skipping the ratio, or working from the wrong substance.</p>",
}

# ---------------- topic_links / exam_context / related_videos ----------------
pd["topic_links"] = {"prerequisites": []}
pd["exam_context"] = {
    "marks": "3–5 per calculation",
    "paper": "Chemistry paper (combined science)",
    "frequency": "High. Reacting mass questions appear in most chemistry papers.",
}
pd["related_videos"] = []

# ---------------- problem_bank ----------------
pb = {}

# ===== BRONZE =====
bronze = []

# B1 CuCO3 -> CuO, 62 g, 1:1, ans 40
bronze.append({
    "unit": "g",
    "display": "In CuCO3 → CuO + CO2, what mass of CuO is produced from 62 g of CuCO3? (Mr: CuCO3 = 124, CuO = 80)",
    "solutions": [40],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Moles = mass ÷ Mr, then use 1:1 ratio, then mass = moles × Mr",
    "hint": "Find moles of CuCO3, keep the same moles of CuO (1:1), then convert back to mass.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 160,
         "message": "Moles = mass ÷ Mr, not Mr ÷ mass. 62 ÷ 124 = 0.5 mol, then 0.5 × 80 = 40 g."},
        {"pattern": "forgot_step", "expect": 0.5,
         "message": "0.5 is the moles of CuO. Finish by converting to mass: 0.5 × 80 = 40 g."},
    ],
    "guided_steps": mass_walk("CuCO3", 62, 124, "CuO", 80,
        "CuCO3 → CuO + CO2",
        "The balanced equation CuCO3 → CuO + CO2 has a 1:1 ratio of CuCO3 to CuO, so the moles of CuO equal the moles of CuCO3.",
        "Ratio 1:1, so moles CuO = ", 0.5, 0.5, 40),
})

# B2 Mg -> MgO, EDITED 48 g, 1:1, ans 80
bronze.append({
    "unit": "g",
    "display": "In 2Mg + O2 → 2MgO, what mass of MgO is produced from 48 g of Mg? (Mr: Mg = 24, MgO = 40)",
    "solutions": [80],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Mole ratio Mg : MgO = 2:2 = 1:1",
    "hint": "Convert 48 g of Mg to moles, the ratio is 1:1, then convert back to mass.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 20,
         "message": "Moles = mass ÷ Mr: 48 ÷ 24 = 2 mol, then 2 × 40 = 80 g. Dividing Mr by mass gives the wrong start."},
        {"pattern": "forgot_step", "expect": 2,
         "message": "2 is the moles of MgO. Convert to mass: 2 × 40 = 80 g."},
    ],
    "guided_steps": mass_walk("Mg", 48, 24, "MgO", 40,
        "2Mg + O2 → 2MgO",
        "The balanced equation 2Mg + O2 → 2MgO has 2 Mg to 2 MgO, which is a 1:1 ratio, so the moles of MgO equal the moles of Mg.",
        "Ratio 1:1, so moles MgO = ", 2, 2, 80),
})

# B3 CaCO3 -> CO2, 100 g, 1:1, ans 44
bronze.append({
    "unit": "g",
    "display": "In CaCO3 → CaO + CO2, what mass of CO2 is produced from 100 g of CaCO3? (Mr: CaCO3 = 100, CO2 = 44)",
    "solutions": [44],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "1:1 mole ratio",
    "hint": "One mole of CaCO3 gives one mole of CO2; convert moles back to mass with the CO2 Mr.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "expect": 100,
         "message": "The CO2 does not keep the mass of the CaCO3. Moles CaCO3 = 1, ratio 1:1, moles CO2 = 1, mass = 1 × 44 = 44 g."},
        {"pattern": "forgot_step", "expect": 1,
         "message": "1 is the moles of CO2. Convert to mass: 1 × 44 = 44 g."},
    ],
    "guided_steps": mass_walk("CaCO3", 100, 100, "CO2", 44,
        "CaCO3 → CaO + CO2",
        "The balanced equation CaCO3 → CaO + CO2 has a 1:1 ratio of CaCO3 to CO2, so the moles of CO2 equal the moles of CaCO3.",
        "Ratio 1:1, so moles CO2 = ", 1, 1, 44),
})

# B4 moles of iron 56 g, ans 1 mol  (moles-only)
bronze.append({
    "unit": "mol",
    "display": "How many moles are in 56 g of iron? (Ar of Fe = 56)",
    "solutions": [1],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "moles = mass ÷ Mr",
    "hint": "Divide the mass by the Ar of iron.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 3136,
         "message": "Moles = mass ÷ Ar = 56 ÷ 56 = 1 mol. Multiplying (56 × 56) is the slip."},
    ],
    "guided_steps": [
        {"say": "Just one move here: moles = mass ÷ Ar. For iron the Ar is 56."},
        {"phase": "substitute", "pre": "moles = 56 ÷ 56 = ", "post": "",
         "answer": 1, "hint": "56 divided by 56."},
        {"say": "Always sanity-check a moles answer by reversing it: mass = moles × Ar should give back the mass in the question."},
        {"pre": "mass = 1 × 56 = ", "post": "",
         "answer": 56, "hint": "Multiply your moles by the Ar."},
        {"pre": "Reverse again: 56 ÷ 56 = ", "post": "",
         "answer": 1, "done": "Back to 1 mol, and 1 × 56 = 56 g matches the question. Correct: 1 mol.",
         "hint": "Mass divided by Ar returns the moles."},
    ],
})

# B5 Na -> H2 ratio, EDITED 4 mol Na, ratio 2:1, ans 2 mol
bronze.append({
    "unit": "mol",
    "display": "In 2Na + 2H2O → 2NaOH + H2, how many moles of H2 are produced from 4 mol of Na?",
    "solutions": [2],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "The mole ratio Na : H2 = 2:1",
    "hint": "The ratio Na : H2 is 2:1, so divide the sodium moles by 2.",
    "misconceptions": [
        {"pattern": "wrong_ratio", "expect": 4,
         "message": "The ratio Na : H2 is 2:1, not 1:1. So 4 mol Na gives 4 ÷ 2 = 2 mol H2."},
        {"pattern": "inverse_error", "expect": 8,
         "message": "Divide by 2, do not multiply: 4 ÷ 2 = 2 mol H2."},
    ],
    "guided_steps": [
        {"say": "The ratio comes straight from the coefficients of 2Na + 2H2O → 2NaOH + H2: two Na to one H2."},
        {"pre": "Coefficient in front of Na = ", "post": "",
         "answer": 2, "hint": "Read the big number written before Na."},
        {"say": "So the ratio Na : H2 is 2:1. Divide the sodium moles by 2."},
        {"phase": "substitute", "pre": "moles H2 = 4 ÷ 2 = ", "post": "",
         "answer": 2, "hint": "Halve the 4 mol of sodium."},
        {"pre": "Reverse-check: 2 mol H2 needs 2 × 2 = ", "post": "",
         "answer": 4, "done": "That returns the 4 mol of sodium, so 2 mol H2 is right.",
         "hint": "Multiply the H2 moles back up by 2."},
    ],
})

pb["bronze"] = bronze
pb["bronze_description"] = "One equation given, a 1:1 mole ratio, masses already in grams: convert to moles, keep the moles, convert back."

# ===== SILVER =====
silver = []

# S1 Fe -> Fe2O3, 56 g, ratio 2:1, ans 80
silver.append({
    "unit": "g",
    "display": "In 4Fe + 3O2 → 2Fe2O3, calculate the mass of Fe2O3 produced from 56 g of iron. (Mr: Fe = 56, Fe2O3 = 160)",
    "solutions": [80],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Mole ratio Fe : Fe2O3 = 4:2 = 2:1",
    "hint": "The ratio Fe : Fe2O3 is 2:1, so halve the iron moles before converting to mass.",
    "misconceptions": [
        {"pattern": "wrong_ratio", "expect": 160,
         "message": "The ratio Fe : Fe2O3 is 4:2 = 2:1, not 1:1. Moles Fe2O3 = 1 ÷ 2 = 0.5, mass = 0.5 × 160 = 80 g."},
        {"pattern": "inverse_error", "expect": 320,
         "message": "Divide the iron moles by 2, do not multiply: 1 ÷ 2 = 0.5 mol Fe2O3, mass = 0.5 × 160 = 80 g."},
    ],
    "guided_steps": mass_walk("Fe", 56, 56, "Fe2O3", 160,
        "4Fe + 3O2 → 2Fe2O3",
        "The balanced equation has 4 Fe to 2 Fe2O3, which simplifies to 2:1. So divide the iron moles by 2.",
        "moles Fe2O3 = 1 ÷ 2 = ", 1, 0.5, 80),
})

# S2 N2 -> NH3, 28 g, ratio 1:2, ans 34
silver.append({
    "unit": "g",
    "display": "In N2 + 3H2 → 2NH3, calculate the mass of ammonia produced from 28 g of N2. (Mr: N2 = 28, NH3 = 17)",
    "solutions": [34],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Mole ratio N2 : NH3 = 1:2",
    "hint": "The ratio N2 : NH3 is 1:2, so double the nitrogen moles before converting to mass.",
    "misconceptions": [
        {"pattern": "wrong_ratio", "expect": 17,
         "message": "The ratio N2 : NH3 is 1:2, not 1:1. Moles NH3 = 1 × 2 = 2, mass = 2 × 17 = 34 g."},
        {"pattern": "forgot_step", "expect": 2,
         "message": "2 is the moles of NH3. Convert to mass: 2 × 17 = 34 g."},
    ],
    "guided_steps": mass_walk("N2", 28, 28, "NH3", 17,
        "N2 + 3H2 → 2NH3",
        "The balanced equation has 1 N2 to 2 NH3, a 1:2 ratio. So multiply the nitrogen moles by 2.",
        "moles NH3 = 1 × 2 = ", 1, 2, 34),
})

# S3 H2 -> NH3, EDITED 12 g H2, ratio 3:2, ans 68
silver.append({
    "unit": "g",
    "display": "In N2 + 3H2 → 2NH3, calculate the mass of ammonia produced from 12 g of H2. (Mr: H2 = 2, NH3 = 17)",
    "solutions": [68],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Mole ratio H2 : NH3 = 3:2",
    "hint": "The ratio H2 : NH3 is 3:2, so multiply the hydrogen moles by 2 and divide by 3.",
    "misconceptions": [
        {"pattern": "wrong_ratio", "expect": 102,
         "message": "The ratio H2 : NH3 is 3:2, not 1:1. Moles NH3 = 6 × 2 ÷ 3 = 4, mass = 4 × 17 = 68 g."},
        {"pattern": "forgot_step", "expect": 4,
         "message": "4 is the moles of NH3. Convert to mass: 4 × 17 = 68 g."},
    ],
    "guided_steps": mass_walk("H2", 12, 2, "NH3", 17,
        "N2 + 3H2 → 2NH3",
        "The balanced equation has 3 H2 to 2 NH3, a 3:2 ratio. So multiply the hydrogen moles by 2, then divide by 3.",
        "moles NH3 = 6 × 2 ÷ 3 = ", 6, 4, 68),
})

# S4 Zn -> ZnO, 13 g, ratio 1:1, ans 16.2 accept 0.1
silver.append({
    "unit": "g",
    "accept": 0.1,
    "display": "Zinc reacts with oxygen: 2Zn + O2 → 2ZnO. Calculate the mass of ZnO produced from 13 g of Zn. (Mr: Zn = 65, ZnO = 81)",
    "solutions": [16.2],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Mole ratio Zn : ZnO = 1:1",
    "hint": "Convert 13 g of Zn to moles, the ratio is 1:1, then convert back with the ZnO Mr.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 405,
         "message": "Moles = mass ÷ Mr: 13 ÷ 65 = 0.2 mol, then 0.2 × 81 = 16.2 g. Dividing Mr by mass gives the wrong start."},
        {"pattern": "forgot_step", "expect": 0.2,
         "message": "0.2 is the moles of ZnO. Convert to mass: 0.2 × 81 = 16.2 g."},
    ],
    "guided_steps": mass_walk("Zn", 13, 65, "ZnO", 81,
        "2Zn + O2 → 2ZnO",
        "The balanced equation has 2 Zn to 2 ZnO, a 1:1 ratio, so the moles of ZnO equal the moles of Zn.",
        "Ratio 1:1, so moles ZnO = ", 0.2, 0.2, 16.2),
})

pb["silver"] = silver
pb["silver_description"] = "The mole ratio is not always 1:1, so scale the moles up or down using the balanced coefficients before converting back to mass."

# ===== GOLD =====
gold = []

# G1 Al -> AlCl3, 27 g, ratio 1:1, ans 133.5
gold.append({
    "unit": "g",
    "display": "In 2Al + 3Cl2 → 2AlCl3, calculate the mass of AlCl3 produced from 27 g of Al. (Mr: Al = 27, AlCl3 = 133.5)",
    "solutions": [133.5],
    "calculator": True,
    "input_type": "single_value",
    "hint": "One mole of Al gives one mole of AlCl3 (2:2); build the AlCl3 Mr from all three chlorines.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "expect": 62.5,
         "message": "Mr AlCl3 = 27 + (3 × 35.5) = 27 + 106.5 = 133.5. Do not forget all three chlorines."},
        {"pattern": "forgot_step", "expect": 1,
         "message": "1 is the moles of AlCl3. Convert to mass: 1 × 133.5 = 133.5 g."},
    ],
    "guided_steps": mass_walk("Al", 27, 27, "AlCl3", 133.5,
        "2Al + 3Cl2 → 2AlCl3",
        "The balanced equation has 2 Al to 2 AlCl3, a 1:1 ratio, so the moles of AlCl3 equal the moles of Al.",
        "Ratio 1:1, so moles AlCl3 = ", 1, 1, 133.5),
})

# G2 H2 -> H2O, 4 g, ratio 1:1, ans 36
gold.append({
    "unit": "g",
    "display": "In 2H2 + O2 → 2H2O, calculate the mass of water produced from 4 g of H2. (Mr: H2 = 2, H2O = 18)",
    "solutions": [36],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Convert 4 g of H2 to moles, the 2H2 : 2H2O ratio is 1:1, then convert back to mass.",
    "misconceptions": [
        {"pattern": "wrong_ratio", "expect": 18,
         "message": "The ratio 2H2 : 2H2O is 1:1, so 2 mol H2 gives 2 mol H2O, mass = 2 × 18 = 36 g."},
        {"pattern": "forgot_step", "expect": 2,
         "message": "2 is the moles of water. Convert to mass: 2 × 18 = 36 g."},
    ],
    "guided_steps": mass_walk("H2", 4, 2, "H2O", 18,
        "2H2 + O2 → 2H2O",
        "The balanced equation has 2 H2 to 2 H2O, which is a 1:1 ratio, so the moles of H2O equal the moles of H2.",
        "Ratio 1:1, so moles H2O = ", 2, 2, 36),
})

# G3 CH4 -> CO2, 32 g, ratio 1:1, ans 88
gold.append({
    "unit": "g",
    "display": "Methane combustion: CH4 + 2O2 → CO2 + 2H2O. Calculate the mass of CO2 produced from 32 g of CH4. (Mr: CH4 = 16, CO2 = 44)",
    "solutions": [88],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Convert 32 g of CH4 to moles, the CH4 : CO2 ratio is 1:1, then convert back using the CO2 Mr.",
    "misconceptions": [
        {"pattern": "wrong_Mr", "expect": 32,
         "message": "Convert using the Mr of CO2 (44), not CH4 (16). Moles CH4 = 2, ratio 1:1, mass = 2 × 44 = 88 g."},
        {"pattern": "forgot_step", "expect": 2,
         "message": "2 is the moles of CO2. Convert to mass: 2 × 44 = 88 g."},
    ],
    "guided_steps": mass_walk("CH4", 32, 16, "CO2", 44,
        "CH4 + 2O2 → CO2 + 2H2O",
        "The balanced equation has 1 CH4 to 1 CO2, a 1:1 ratio, so the moles of CO2 equal the moles of CH4.",
        "Ratio 1:1, so moles CO2 = ", 2, 2, 88),
})

pb["gold"] = gold
pb["gold_description"] = "The full mass, moles, ratio, mass chain on less familiar equations with larger formula masses, so track every coefficient and Mr."

pd["problem_bank"] = pb

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, a 1:1 ratio",
        "steps": [
            "Turn the known mass into moles with <strong>moles = mass ÷ Mr</strong>.",
            "The coefficients give the ratio. When it is 1:1, the moles of the product equal the moles of the reactant.",
            "Turn moles back into mass with <strong>mass = moles × Mr</strong>, then reverse-check.",
        ],
        "example": {
            "question": "In 2Ca + O2 → 2CaO, find the mass of CaO from 40 g of Ca. (Mr: Ca = 40, CaO = 56)",
            "steps": [
                {"label": "Moles of Ca", "content": "<p>moles = 40 ÷ 40 = 1 mol</p>"},
                {"label": "Ratio 2:2 = 1:1", "content": "<p>moles CaO = 1 mol</p>"},
                {"label": "Mass of CaO", "content": "<p>mass = 1 × 56</p>"},
                {"label": "Check", "content": "<p>56 ÷ 56 = 1 mol ✓</p>"},
                {"label": "Answer", "content": "<p><strong>56 g</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: scale by the mole ratio",
        "steps": [
            "Find the moles of the known substance as before.",
            "Read the ratio from the coefficients. If it is 2:1, halve the moles; if 1:2, double them; for 3:2, multiply by 2 then divide by 3.",
            "Convert the scaled moles back to mass, then check.",
        ],
        "example": {
            "question": "In 4Fe + 3O2 → 2Fe2O3, find the mass of Fe2O3 from 112 g of Fe. (Mr: Fe = 56, Fe2O3 = 160)",
            "steps": [
                {"label": "Moles of Fe", "content": "<p>moles = 112 ÷ 56 = 2 mol</p>"},
                {"label": "Ratio 4:2 = 2:1", "content": "<p>moles Fe2O3 = 2 ÷ 2 = 1 mol</p>"},
                {"label": "Mass of Fe2O3", "content": "<p>mass = 1 × 160</p>"},
                {"label": "Check", "content": "<p>160 ÷ 160 = 1 mol ✓</p>"},
                {"label": "Answer", "content": "<p><strong>160 g</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: the full chain, trickier equations",
        "steps": [
            "The same three moves apply, but the equations are less familiar and the formula masses larger, so work slowly.",
            "Build each Mr from its atoms before you start, and take the ratio straight from the coefficients.",
            "Convert back to mass and reverse-check the answer.",
        ],
        "example": {
            "question": "In C3H8 + 5O2 → 3CO2 + 4H2O, find the mass of CO2 from 22 g of propane. (Mr: C3H8 = 44, CO2 = 44)",
            "steps": [
                {"label": "Moles of C3H8", "content": "<p>moles = 22 ÷ 44 = 0.5 mol</p>"},
                {"label": "Ratio 1:3", "content": "<p>moles CO2 = 0.5 × 3 = 1.5 mol</p>"},
                {"label": "Mass of CO2", "content": "<p>mass = 1.5 × 44</p>"},
                {"label": "Check", "content": "<p>66 ÷ 44 = 1.5 mol ✓</p>"},
                {"label": "Answer", "content": "<p><strong>66 g</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------- guided (opener + teach) ----------------
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "A pancake recipe: 2 eggs make 1 stack.<br>You crack 6 eggs.",
        "steps": [
            {"say": "A kitchen puzzle, no chemistry yet. The recipe is fixed: every stack needs 2 eggs.",
             "pre": "How many stacks can you make from 6 eggs? ", "post": "",
             "answer": 3, "hint": "Each stack needs 2 eggs, and 6 ÷ 2 = 3."},
            {"say": "You just scaled a recipe by its ratio. The bigger recipe also needs 3 cups of flour per stack.",
             "pre": "For those 3 stacks, how many cups of flour? ", "post": "",
             "answer": 9, "hint": "3 cups for each of the 3 stacks."},
            {"say": "A balanced equation is exactly this recipe. In \\(2H_2 + O_2 \\rightarrow 2H_2O\\) the big numbers (2, 1, 2) are the ratio, just like eggs to stacks. Chemists count in <strong>moles</strong> instead of eggs and scale the same way. The one extra move is swapping between grams and moles using moles = mass ÷ Mr."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Solve: In 2Ca + O2 → 2CaO, find the mass of CaO from 40 g of Ca. (Mr: Ca = 40, CaO = 56)",
            "label": "Together: your first one",
            "steps": [
                {"say": "Reacting mass is one chain: mass to moles, ratio, then back to mass. Start with the calcium: moles = mass ÷ Mr.",
                 "pre": "moles Ca = 40 ÷ 40 = ", "post": "", "answer": 1, "hint": "Divide the mass by the Ar."},
                {"say": "The equation 2Ca + O2 → 2CaO has 2 Ca to 2 CaO, a 1:1 ratio.",
                 "pre": "moles CaO = ", "post": "", "answer": 1, "hint": "1:1 means the moles are unchanged."},
                {"pre": "mass CaO = 1 × 56 = ", "post": "", "answer": 56, "hint": "Multiply moles by the Mr of CaO."},
                {"pre": "Check by reversing: 56 ÷ 56 = ", "post": "", "answer": 1,
                 "done": "Back to 1 mol, so 56 g is right. That was the whole chain.",
                 "hint": "Mass divided by Mr returns the moles."},
            ],
        },
        "silver": {
            "display": "Solve: In 3Fe + 2O2 → Fe3O4, find the mass of Fe3O4 from 168 g of Fe. (Mr: Fe = 56, Fe3O4 = 232)",
            "label": "Together: the silver move",
            "steps": [
                {"say": "Same chain, but the ratio is not 1:1 this time. Start with the iron: moles = mass ÷ Mr.",
                 "pre": "moles Fe = 168 ÷ 56 = ", "post": "", "answer": 3, "hint": "Divide the mass by the Ar."},
                {"say": "The equation has 3 Fe to 1 Fe3O4, a 3:1 ratio. This is the new move: divide the iron moles by 3.",
                 "pre": "moles Fe3O4 = 3 ÷ 3 = ", "post": "", "answer": 1, "hint": "Three iron atoms build one Fe3O4."},
                {"pre": "mass Fe3O4 = 1 × 232 = ", "post": "", "answer": 232, "hint": "Multiply moles by the Mr of Fe3O4."},
                {"pre": "Check by reversing: 232 ÷ 232 = ", "post": "", "answer": 1,
                 "done": "Back to 1 mol, so 232 g is right. Scaling by the ratio was the silver move.",
                 "hint": "Mass divided by Mr returns the moles."},
            ],
        },
        "gold": {
            "display": "Solve: In C3H8 + 5O2 → 3CO2 + 4H2O, find the mass of CO2 from 22 g of propane. (Mr: C3H8 = 44, CO2 = 44)",
            "label": "Together: the gold move",
            "steps": [
                {"say": "A less familiar combustion equation, but the same chain. Start with the propane: moles = mass ÷ Mr.",
                 "pre": "moles C3H8 = 22 ÷ 44 = ", "post": "", "answer": 0.5, "hint": "Divide the mass by the Mr."},
                {"say": "The equation has 1 C3H8 to 3 CO2, a 1:3 ratio. Multiply the propane moles by 3.",
                 "pre": "moles CO2 = 0.5 × 3 = ", "post": "", "answer": 1.5, "hint": "One propane makes three CO2."},
                {"pre": "mass CO2 = 1.5 × 44 = ", "post": "", "answer": 66, "hint": "Multiply moles by the Mr of CO2."},
                {"pre": "Check by reversing: 66 ÷ 44 = ", "post": "", "answer": 1.5,
                 "done": "Back to 1.5 mol, so 66 g is right. Bigger ratio, same three moves.",
                 "hint": "Mass divided by Mr returns the moles."},
            ],
        },
    },
}

# ---------------- worked_examples (preserve original) ----------------
pd["worked_examples"] = [
    {
        "steps": [
            {"label": "Step 1: Moles of CuCO3", "content": "<p>moles = 62 ÷ 124 = 0.5 mol</p>"},
            {"label": "Step 2: Mole ratio CuCO3 : CuO = 1:1", "content": "<p>So moles CuO = 0.5 mol</p>"},
            {"label": "Step 3: Mass of CuO", "content": "<p>mass = 0.5 × 80</p>"},
            {"label": "Answer", "content": "<p>Mass = <strong>40 g</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "In the reaction CuCO3 → CuO + CO2, what mass of CuO is produced from 62 g of CuCO3? (Mr: CuCO3 = 124, CuO = 80)",
        "difficulty": "Bronze",
    },
    {
        "steps": [
            {"label": "Step 1: Moles of Fe", "content": "<p>moles = 56 ÷ 56 = 1 mol</p>"},
            {"label": "Step 2: Mole ratio Fe : Fe2O3 = 4:2 = 2:1", "content": "<p>So moles Fe2O3 = 1 ÷ 2 = 0.5 mol</p>"},
            {"label": "Step 3: Mass of Fe2O3", "content": "<p>mass = 0.5 × 160</p>"},
            {"label": "Answer", "content": "<p>Mass = <strong>80 g</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "56 g of iron reacts with excess oxygen: 4Fe + 3O2 → 2Fe2O3. Calculate the mass of Fe2O3 produced. (Mr: Fe = 56, Fe2O3 = 160)",
        "difficulty": "Silver",
    },
    {
        "steps": [
            {"label": "Step 1: Moles of N2", "content": "<p>moles = 28 ÷ 28 = 1 mol</p>"},
            {"label": "Step 2: Mole ratio N2 : NH3 = 1:2", "content": "<p>So moles NH3 = 1 × 2 = 2 mol</p>"},
            {"label": "Step 3: Mass of NH3", "content": "<p>mass = 2 × 17</p>"},
            {"label": "Answer", "content": "<p>Mass = <strong>34 g</strong></p>", "isAnswer": True, "is_answer": True},
        ],
        "question": "In N2 + 3H2 → 2NH3, calculate the mass of NH3 produced from 28 g of N2. (Mr: N2 = 28, NH3 = 17)",
        "difficulty": "Gold",
    },
]

with open("lesson_chemistry-calculations-L02@5b02ac14f2.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written")
