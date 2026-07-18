# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s):
    return {"say": s}

pd = json.load(io.open("_canon_chemL03_d1de9ba347.json", encoding="utf-8"))

# ---------------- method_card (slim) ----------------
pd["method_card"] = {
    "title": "Bond Energy Calculations",
    "steps": [
        "Count every bond: multiply each bond energy by how many of that bond there are.",
        "Add the reactant bond energies for the total broken; add the product bond energies for the total made.",
        "ΔH = bonds broken − bonds made.",
        "Negative means exothermic (energy out); positive means endothermic (energy in)."
    ],
    "content": ("<p><strong>ΔH = bonds broken − bonds made.</strong> Breaking bonds takes "
        "energy in (endothermic); making bonds gives energy out (exothermic).</p>"
        "<p>Count carefully: multiply each bond energy by the number of those bonds "
        "(4 C–H in CH₄, not 1). Add the reactant bonds for <em>broken</em>, the product "
        "bonds for <em>made</em>, then subtract.</p>"
        "<p>A negative answer means energy is released overall (exothermic); a positive "
        "answer means energy is absorbed (endothermic).</p>")
}

# ---------------- exam_context: strip em dash ----------------
pd["exam_context"]["frequency"] = "Common: often appears as a 4 to 5 mark structured question"

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: add up, then subtract",
        "steps": [
            "Every bond has an energy. Breaking a bond needs energy in; making a bond gives energy out.",
            "Add all the bond energies in the reactants (bonds <strong>broken</strong>) and all in the products (bonds <strong>made</strong>). Multiply each by how many of that bond there are.",
            "<strong>ΔH = bonds broken − bonds made.</strong> A negative answer means the reaction gives out energy (exothermic)."
        ],
        "example": {
            "question": "Calculate ΔH for H₂ + Cl₂ → 2HCl. Bond energies: H–H = 436, Cl–Cl = 242, H–Cl = 431 kJ/mol.",
            "steps": [
                {"label": "Broken", "content": "<p>H–H + Cl–Cl = 436 + 242 = 678 kJ</p>"},
                {"label": "Made", "content": "<p>2 × H–Cl = 2 × 431 = 862 kJ</p>"},
                {"label": "Subtract", "content": "<p>ΔH = 678 − 862</p>"},
                {"label": "Check", "content": "<p>862 + (−184) = 678, the broken energy ✓</p>"},
                {"label": "Answer", "content": "<p>ΔH = −184 kJ/mol (exothermic)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: count carefully or rearrange",
        "steps": [
            "Molecules can hold several of the same bond: CH₄ has 4 C–H bonds, 2H₂O has 4 O–H bonds. Multiply each bond energy by its count before adding.",
            "If the question gives ΔH and one total, rearrange: made = broken − ΔH, or broken = ΔH + made.",
            "Read the sign: negative ΔH is exothermic (energy out), positive ΔH is endothermic (energy in)."
        ],
        "example": {
            "question": "Calculate ΔH for CH₄ + 2O₂ → CO₂ + 2H₂O. Bond energies: C–H = 413, O=O = 498, C=O = 803, O–H = 464 kJ/mol.",
            "steps": [
                {"label": "Broken", "content": "<p>4 × C–H + 2 × O=O = 1652 + 996 = 2648 kJ</p>"},
                {"label": "Made", "content": "<p>2 × C=O + 4 × O–H = 1606 + 1856 = 3462 kJ</p>"},
                {"label": "Subtract", "content": "<p>ΔH = 2648 − 3462</p>"},
                {"label": "Check", "content": "<p>3462 + (−814) = 2648, the broken energy ✓</p>"},
                {"label": "Answer", "content": "<p>ΔH = −814 kJ/mol (exothermic)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: multi-step problems",
        "steps": [
            "Big molecules mean many bonds: draw them out and count every C–H, C=C, C=O and O–H before you multiply.",
            "If the equation shows more than one mole of fuel, find ΔH for the whole equation, then divide by the number of moles for a per-mole answer.",
            "To compare fuels per gram, divide each energy change by the mass of that many moles (mass = moles × Mr)."
        ],
        "example": {
            "question": "Calculate ΔH for the combustion of ethene: C₂H₄ + 3O₂ → 2CO₂ + 2H₂O. Bond energies: C=C = 614, C–H = 413, O=O = 498, C=O = 803, O–H = 464 kJ/mol.",
            "steps": [
                {"label": "Broken", "content": "<p>C=C + 4 × C–H + 3 × O=O = 614 + 1652 + 1494 = 3760 kJ</p>"},
                {"label": "Made", "content": "<p>4 × C=O + 4 × O–H = 3212 + 1856 = 5068 kJ</p>"},
                {"label": "Subtract", "content": "<p>ΔH = 3760 − 5068</p>"},
                {"label": "Check", "content": "<p>5068 + (−1308) = 3760, the broken energy ✓</p>"},
                {"label": "Answer", "content": "<p>ΔH = −1308 kJ/mol (exothermic)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- guided.opener + teach ----------------
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": ("You dismantle an old shed and build a fence from the reclaimed wood.<br>"
                    "Taking the shed apart <strong>costs</strong> you £678.<br>"
                    "Selling the finished fence <strong>earns</strong> you £862."),
        "steps": [
            box("Overall, how many £ better off are you? 862 − 678 = ", 184,
                "Take the cost away from what you earn.",
                say="A money puzzle first, no chemistry needed."),
            box("Chemists write the change as cost − earning, in the same order every time: 678 − 862 = ", -184,
                "Cost first, then take away the earning. The answer comes out negative.",
                say="Notice the size is the same, £184, but written this way it is negative."),
            say("You gained £184, and chemists write that gain as <strong>ΔH = −184 kJ/mol</strong>. "
                "Breaking bonds is the cost (energy in), making bonds is the earning (energy out), and "
                "<strong>ΔH = bonds broken − bonds made</strong>. A negative answer means energy was "
                "released: the reaction is exothermic. That is the whole method.")
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "Calculate ΔH for H₂ + F₂ → 2HF. Bond energies: H–H = 436, F–F = 158, H–F = 568 kJ/mol.",
            "steps": [
                box("Break the reactant bonds: H–H + F–F = 436 + 158 = ", 594,
                    "Add the two reactant bond energies.",
                    say="Break every bond in the reactants first."),
                box("Make the product bonds: 2 HF means 2 × H–F = 2 × 568 = ", 1136,
                    "Two HF molecules form, so double the H–F energy.",
                    say="Now the bonds made in the two product molecules."),
                box("ΔH = broken − made = 594 − 1136 = ", -542,
                    "Subtract made from broken; it comes out negative."),
                box("Check: made + ΔH = 1136 + (−542) = ", 594,
                    "Adding ΔH back to made should return the broken energy.",
                    done="Returns 594, the broken energy, so ΔH = −542 kJ/mol (exothermic). That was the whole method.")
            ]
        },
        "silver": {
            "label": "Together: counting and the sign",
            "display": "Calculate ΔH for N₂ + O₂ → 2NO. Bond energies: N≡N = 945, O=O = 498, N=O = 630 kJ/mol.",
            "steps": [
                box("Break the reactant bonds: N≡N + O=O = 945 + 498 = ", 1443,
                    "Add the two reactant bond energies.",
                    say="One N≡N triple bond and one O=O double bond break."),
                box("Make the product bonds: 2 NO means 2 × N=O = 2 × 630 = ", 1260,
                    "Two NO molecules form, so double the N=O energy.",
                    say="Two NO molecules form, each with one N=O bond."),
                box("ΔH = broken − made = 1443 − 1260 = ", 183,
                    "Subtract made from broken; here it comes out positive."),
                box("Check: made + ΔH = 1260 + 183 = ", 1443,
                    "Adding ΔH back to made should return the broken energy.",
                    done="Returns 1443, and the positive sign means this reaction is endothermic. Counting the bonds and reading the sign was the point.")
            ]
        },
        "gold": {
            "label": "Together: whole equation, then per mole",
            "display": ("Calculate ΔH per mole of C₂H₂ for: 2C₂H₂ + 5O₂ → 4CO₂ + 2H₂O. "
                        "Bond energies: C≡C = 839, C–H = 413, O=O = 498, C=O = 803, O–H = 464 kJ/mol."),
            "steps": [
                box("Break: 2 × C≡C + 4 × C–H = 1678 + 1652 = ", 3330,
                    "Two C₂H₂ molecules: 2 triple bonds and 4 C–H bonds.",
                    say="Two ethyne molecules, so 2 C≡C and 4 C–H, plus the oxygen bonds."),
                box("Add the oxygen: 3330 + 5 × O=O = 3330 + 2490 = ", 5820,
                    "Five O=O bonds: 5 × 498 = 2490, then add."),
                box("Make: 4CO₂ has 8 C=O = 8 × 803 = ", 6424,
                    "Four CO₂ molecules, each with 2 C=O bonds.",
                    say="Now the bonds made in the products."),
                box("Add the water: 6424 + 4 × O–H = 6424 + 1856 = ", 8280,
                    "2H₂O has 4 O–H bonds: 4 × 464 = 1856, then add."),
                box("ΔH for the whole equation = 5820 − 8280 = ", -2460,
                    "Broken minus made for the full equation."),
                box("Per mole of C₂H₂ (the equation burns 2): −2460 ÷ 2 = ", -1230,
                    "Divide the whole-equation ΔH by 2.",
                    done="−1230 kJ per mole of ethyne. Finding the whole ΔH then dividing by the coefficient was the new move.")
            ]
        }
    }
}

# ---------------- per-problem: hint, guided_steps, expects ----------------
pb = pd["problem_bank"]
pb["bronze_description"] = "One equation, values given: add the reactant bonds, add the product bonds, subtract."
pb["silver_description"] = "Count several bonds per molecule, or rearrange ΔH = broken − made to find a missing total."
pb["gold_description"] = "Multi-step: many bonds to count, a per-mole division, or a per-gram comparison."

# ---- BRONZE ----
b = pb["bronze"]
b[0]["hint"] = "Only add the reactant bonds: H–H plus Cl–Cl."
b[0]["guided_steps"] = [
    say("Break only the reactant bonds. There are two: one H–H and one Cl–Cl."),
    box("Energy to break H–H = ", 436, "That is the H–H bond energy."),
    box("Energy to break Cl–Cl = ", 242, "That is the Cl–Cl bond energy.", phase="substitute"),
    box("Add them: 436 + 242 = ", 678, "Add the two bond energies.",
        done="That is the total energy to break the reactant bonds: 678 kJ.")
]
b[0]["misconceptions"] = [
    {"pattern": "included_products", "check": "common", "expect": 1540,
     "message": "Only the reactant bonds are broken. Adding the product bonds too gives 436 + 242 + 862 = 1540, which is wrong. Broken = 436 + 242 = 678 kJ."}
]

b[1]["hint"] = "Two HCl molecules means two H–Cl bonds, so double it."
b[1]["guided_steps"] = [
    say("Two HCl molecules form, so two H–Cl bonds are made."),
    box("Energy released by one H–Cl = ", 431, "That is the H–Cl bond energy."),
    box("There are 2 of them: 2 × 431 = ", 862, "Multiply by the number of bonds.", phase="substitute"),
    box("Check: 862 ÷ 2 = ", 431, "Divide by 2 to undo.",
        done="Back to one H–Cl bond, so 862 kJ is right.")
]
b[1]["misconceptions"] = [
    {"pattern": "forgot_coefficient", "check": "common", "expect": 431,
     "message": "There are 2 HCl molecules, so 2 × H–Cl = 862 kJ. Using just one H–Cl (431) forgets the coefficient."}
]

b[2]["hint"] = "Broken minus made: 678 − 862."
b[2]["guided_steps"] = [
    say("First find the energy to break the reactant bonds, then the energy released making the product bonds."),
    box("Break: H–H + Cl–Cl = 436 + 242 = ", 678, "Add the reactant bonds."),
    box("Make: 2 × H–Cl = 2 × 431 = ", 862, "Two HCl molecules, so double."),
    box("ΔH = broken − made = 678 − 862 = ", -184, "Subtract made from broken; the answer is negative.", phase="substitute"),
    box("Check: made + ΔH = 862 + (−184) = ", 678, "Adding ΔH back to made should give broken.",
        done="Returns the broken energy, so ΔH = −184 kJ/mol is right.")
]
b[2]["misconceptions"] = [
    {"pattern": "wrong_subtraction", "check": "common", "expect": 184,
     "message": "ΔH = broken − made, not made − broken. 678 − 862 = −184 kJ/mol. Doing 862 − 678 = 184 flips the sign."},
    {"pattern": "sign_error", "check": "common", "expect": None,
     "message": "The answer is negative (−184), so the reaction is exothermic: energy is given out."}
]

b[3]["hint"] = "A negative energy change means energy is given out."
b[3]["misconceptions"] = [
    {"pattern": "sign_confusion", "check": "common", "expect": None,
     "message": "A negative ΔH means exothermic: more energy is released making new bonds than is needed to break the old ones."}
]

b[4]["hint"] = "Count 2 H–H and 1 O=O to break, and 4 O–H made."
b[4]["guided_steps"] = [
    say("Break every reactant bond: 2 H–H bonds and 1 O=O bond."),
    box("2 × H–H = 2 × 436 = ", 872, "Two H₂ molecules, so double."),
    box("Add the O=O: 872 + 498 = ", 1370, "Add the single O=O bond energy."),
    say("Now the product bonds. 2H₂O has 4 O–H bonds."),
    box("4 × O–H = 4 × 464 = ", 1856, "Four O–H bonds in two water molecules."),
    box("ΔH = broken − made = 1370 − 1856 = ", -486, "Subtract made from broken.", phase="substitute"),
    box("Check: made + ΔH = 1856 + (−486) = ", 1370, "Adding ΔH back should return the broken energy.",
        done="Returns 1370, so ΔH = −486 kJ/mol is right.")
]
b[4]["misconceptions"] = [
    {"pattern": "wrong_count", "check": "common", "expect": None,
     "message": "Broken: 2 × H–H + 1 × O=O = 872 + 498 = 1370 kJ. Made: 4 × O–H = 1856 kJ. ΔH = 1370 − 1856 = −486 kJ/mol."},
    {"pattern": "forgot_coefficient", "check": "common", "expect": 442,
     "message": "2H₂O has 4 O–H bonds, not 2. Using 2 × 464 = 928 gives +442, the wrong answer. Made = 4 × 464 = 1856 kJ."}
]

b[5]["hint"] = "Break H–H and Br–Br, make two H–Br bonds."
b[5]["guided_steps"] = [
    say("Break the reactant bonds: one H–H and one Br–Br."),
    box("H–H + Br–Br = 436 + 193 = ", 629, "Add the two reactant bonds."),
    say("Make the product bonds: 2 H–Br."),
    box("2 × H–Br = 2 × 366 = ", 732, "Two HBr molecules, so double."),
    box("ΔH = broken − made = 629 − 732 = ", -103, "Subtract made from broken.", phase="substitute"),
    box("Check: made + ΔH = 732 + (−103) = ", 629, "Adding ΔH back should return the broken energy.",
        done="Returns 629, so ΔH = −103 kJ/mol is right.")
]
b[5]["misconceptions"] = [
    {"pattern": "wrong_count", "check": "common", "expect": 263,
     "message": "There are 2 HBr molecules, so 2 × H–Br = 732 kJ. Using one H–Br (366) gives 263 by mistake. ΔH = 629 − 732 = −103 kJ/mol."}
]

b[6]["hint"] = "Break one N≡N and three H–H, make six N–H bonds."
b[6]["guided_steps"] = [
    say("Break the reactant bonds: 1 N≡N and 3 H–H bonds."),
    box("3 × H–H = 3 × 436 = ", 1308, "Three H₂ molecules."),
    box("Add the N≡N: 1308 + 945 = ", 2253, "Add the single N≡N bond energy."),
    say("Make the product bonds: 2NH₃ has 6 N–H bonds (3 per molecule)."),
    box("6 × N–H = 6 × 391 = ", 2346, "Six N–H bonds in total."),
    box("ΔH = broken − made = 2253 − 2346 = ", -93, "Subtract made from broken.", phase="substitute"),
    box("Check: made + ΔH = 2346 + (−93) = ", 2253, "Adding ΔH back should return the broken energy.",
        done="Returns 2253, so ΔH = −93 kJ/mol is right.")
]
b[6]["misconceptions"] = [
    {"pattern": "wrong_count", "check": "common", "expect": None,
     "message": "Broken: 1 × N≡N + 3 × H–H = 945 + 1308 = 2253 kJ. Made: 6 × N–H = 2346 kJ. ΔH = 2253 − 2346 = −93 kJ/mol."},
    {"pattern": "forgot_coefficient", "check": "common", "expect": 1080,
     "message": "2NH₃ has 6 N–H bonds (3 per molecule × 2). Using 3 N–H (1173) gives 1080, the wrong answer."}
]

b[7]["hint"] = "Two water molecules, each with two O–H bonds."
b[7]["guided_steps"] = [
    say("Count the product molecules: 2H₂O is two water molecules."),
    box("O–H bonds in one water molecule = ", 2, "Water is H–O–H: two O–H bonds."),
    box("Two molecules: 2 × 2 = ", 4, "Multiply bonds per molecule by the number of molecules.", phase="substitute"),
    box("Check: 4 ÷ 2 = ", 2, "Divide back by the number of molecules.",
        done="Two O–H bonds per water molecule, so 4 in total.")
]
b[7]["misconceptions"] = [
    {"pattern": "forgot_coefficient", "check": "common", "expect": 2,
     "message": "Each water molecule has 2 O–H bonds and there are 2 molecules, so 2 × 2 = 4 bonds. Counting 2 forgets one molecule."},
    {"pattern": "wrong_count", "check": "common", "expect": None,
     "message": "Count bonds, not molecules: 2H₂O is 2 molecules × 2 O–H bonds each = 4 O–H bonds."}
]

# ---- SILVER ----
s = pb["silver"]
s[0]["hint"] = "Break 4 C–H and 2 O=O; make 2 C=O and 4 O–H."
s[0]["guided_steps"] = [
    say("Break the reactant bonds: 4 C–H bonds and 2 O=O bonds."),
    box("4 × C–H = 4 × 413 = ", 1652, "Methane has 4 C–H bonds."),
    box("2 × O=O = 2 × 498 = ", 996, "Two O₂ molecules."),
    box("Total broken = 1652 + 996 = ", 2648, "Add the reactant bond totals."),
    say("Make the product bonds: CO₂ has 2 C=O bonds, and 2H₂O has 4 O–H bonds."),
    box("2 × C=O = 2 × 803 = ", 1606, "One CO₂ molecule, two C=O bonds."),
    box("Add 4 O–H (4 × 464 = 1856): 1606 + 1856 = ", 3462, "Add the water bonds to the CO₂ bonds."),
    box("ΔH = broken − made = 2648 − 3462 = ", -814, "Subtract made from broken.", phase="substitute"),
    box("Check: made + ΔH = 3462 + (−814) = ", 2648, "Adding ΔH back should return the broken energy.",
        done="Returns 2648, so ΔH = −814 kJ/mol is right.")
]
s[0]["misconceptions"] = [
    {"pattern": "wrong_count", "check": "common", "expect": None,
     "message": "Broken: 4 × C–H + 2 × O=O = 1652 + 996 = 2648 kJ. Made: 2 × C=O + 4 × O–H = 1606 + 1856 = 3462 kJ. ΔH = 2648 − 3462 = −814 kJ/mol."},
    {"pattern": "forgot_water_bonds", "check": "common", "expect": 114,
     "message": "2H₂O has 4 O–H bonds, not 2. Using 2 × 464 makes made = 2534 and gives +114 by mistake. Made = 3462 kJ."}
]

s[1]["hint"] = "Rearrange ΔH = broken − made to made = broken − ΔH."
s[1]["guided_steps"] = [
    say("Rearrange ΔH = broken − made to made = broken − ΔH."),
    box("ΔH is −814, so made = 2648 − (−814). Subtracting a negative adds it: 2648 + ", 814,
        "Two minus signs together become a plus."),
    box("2648 + 814 = ", 3462, "Add.", phase="substitute"),
    box("Check with ΔH = broken − made = 2648 − 3462 = ", -814, "This should return the given ΔH.",
        done="That is the given ΔH, so made = 3462 kJ is right.")
]
s[1]["misconceptions"] = [
    {"pattern": "wrong_rearrange", "check": "common", "expect": 1834,
     "message": "Rearrange ΔH = broken − made to made = broken − ΔH = 2648 − (−814) = 2648 + 814 = 3462 kJ. Adding ΔH instead (2648 + (−814) = 1834) is the slip."}
]

s[2]["hint"] = "Subtract: 1845 − 2130, then read the sign."
s[2]["guided_steps"] = [
    say("Find ΔH = broken − made, then decide exothermic or endothermic."),
    box("Difference in size: 2130 − 1845 = ", 285, "How much bigger the made value is."),
    box("More is made than broken, so ΔH is negative: 1845 − 2130 = ", -285,
        "Broken minus made comes out negative here.", phase="substitute"),
    box("Check: made + ΔH = 2130 + (−285) = ", 1845, "Adding ΔH back should return bonds broken.",
        done="Returns bonds broken, so ΔH = −285 kJ/mol (exothermic).")
]
s[2]["misconceptions"] = [
    {"pattern": "wrong_subtraction", "check": "common", "expect": 285,
     "message": "ΔH = broken − made = 1845 − 2130 = −285 kJ/mol (exothermic). Doing 2130 − 1845 = 285 flips the sign."},
    {"pattern": "sign_error", "check": "common", "expect": None,
     "message": "More energy is released making bonds (2130) than breaking them (1845), so ΔH is negative: exothermic."}
]

s[3]["hint"] = "Subtract: 1520 − 1380, then read the sign."
s[3]["guided_steps"] = [
    say("ΔH = broken − made, with broken = 1520 and made = 1380."),
    box("1520 − 1380 = ", 140, "Broken minus made; here it is positive."),
    box("Positive ΔH means endothermic. Check by adding back: 1380 + 140 = ", 1520,
        "Made plus ΔH should return bonds broken.", phase="substitute"),
    box("And bonds made should be broken − ΔH: 1520 − 140 = ", 1380,
        "This should return bonds made.",
        done="Returns bonds made, so ΔH = +140 kJ/mol (endothermic) is right.")
]
s[3]["misconceptions"] = [
    {"pattern": "sign_error", "check": "common", "expect": -140,
     "message": "ΔH = broken − made = 1520 − 1380 = +140 kJ/mol. Doing made − broken = −140 flips the sign. Positive means endothermic."}
]

s[4]["hint"] = "Two water molecules, two O–H bonds each."
s[4]["guided_steps"] = [
    say("Count the product molecules: 2H₂O is two water molecules."),
    box("O–H bonds in one water molecule = ", 2, "Water is H–O–H: two O–H bonds."),
    box("Two molecules: 2 × 2 = ", 4, "Multiply bonds per molecule by the number of molecules.", phase="substitute"),
    box("Check: 4 ÷ 2 = ", 2, "Divide back by the number of molecules.",
        done="Two O–H bonds per molecule, so 4 formed in total.")
]
s[4]["misconceptions"] = [
    {"pattern": "forgot_coefficient", "check": "common", "expect": 2,
     "message": "2H₂O is two water molecules, each with 2 O–H bonds, so 2 × 2 = 4 bonds made."}
]

s[5]["hint"] = "Positive means energy is taken in overall."
s[5]["misconceptions"] = [
    {"pattern": "sign_confusion", "check": "common", "expect": None,
     "message": "Positive ΔH means more energy is absorbed breaking bonds than released making them. The reaction is endothermic: it takes in heat from the surroundings."}
]

# ---- GOLD ----
g = pb["gold"]
g[0]["hint"] = "Break C=C, 4 C–H and 3 O=O; make 4 C=O and 4 O–H."
g[0]["guided_steps"] = [
    say("Break the reactant bonds: C₂H₄ has 1 C=C and 4 C–H; then 3 O=O."),
    box("4 × C–H = 4 × 413 = ", 1652, "Ethene has 4 C–H bonds, two on each carbon."),
    box("Add C=C and 3 O=O: 1652 + 614 + 1494 = ", 3760, "3 × O=O = 1494; add the C=C too."),
    say("Make the product bonds: 2CO₂ has 4 C=O, 2H₂O has 4 O–H."),
    box("4 × C=O = 4 × 803 = ", 3212, "Two CO₂ molecules, two C=O bonds each."),
    box("Add 4 O–H (1856): 3212 + 1856 = ", 5068, "Add the water bonds."),
    box("ΔH = broken − made = 3760 − 5068 = ", -1308, "Subtract made from broken.", phase="substitute"),
    box("Check: made + ΔH = 5068 + (−1308) = ", 3760, "Adding ΔH back should return the broken energy.",
        done="Returns 3760, so ΔH = −1308 kJ/mol is right.")
]
g[0]["misconceptions"] = [
    {"pattern": "wrong_count", "check": "common", "expect": None,
     "message": "Broken: 1 × C=C + 4 × C–H + 3 × O=O = 614 + 1652 + 1494 = 3760 kJ. Made: 4 × C=O + 4 × O–H = 3212 + 1856 = 5068 kJ. ΔH = 3760 − 5068 = −1308 kJ/mol."},
    {"pattern": "ch_count", "check": "common", "expect": -2134,
     "message": "C₂H₄ has 4 C–H bonds (2 on each carbon), not 2. Using 2 C–H makes broken = 2934 and gives −2134 by mistake."}
]

g[1]["hint"] = "Work out ΔH for the whole equation, then divide by 2 for one mole."
g[1]["guided_steps"] = [
    say("This equation burns 2 moles of ethane. Work out ΔH for the whole equation, then divide by 2."),
    box("12 × C–H = 12 × 413 = ", 4956, "Two C₂H₆ molecules, 6 C–H each."),
    box("Add 2 C–C (694) and 7 O=O (3486): 4956 + 694 + 3486 = ", 9136, "Total energy to break all reactant bonds."),
    say("Now the bonds made: 4CO₂ has 8 C=O, 6H₂O has 12 O–H."),
    box("8 × C=O = 8 × 803 = ", 6424, "Four CO₂ molecules, two C=O each."),
    box("Add 12 O–H (5568): 6424 + 5568 = ", 11992, "Total energy released making product bonds."),
    box("ΔH for the whole equation = 9136 − 11992 = ", -2856, "Broken minus made for the full equation."),
    box("Per mole of C₂H₆: −2856 ÷ 2 = ", -1428, "Divide by 2 because the equation burns 2 mol.", phase="substitute"),
    box("Check: 2 × (−1428) = ", -2856, "Multiplying back by 2 should give the whole-equation ΔH.",
        done="Returns the whole-equation ΔH, so −1428 kJ/mol per mole of ethane is right.")
]
g[1]["misconceptions"] = [
    {"pattern": "wrong_count", "check": "common", "expect": None,
     "message": "For 2C₂H₆: 2 × C–C + 12 × C–H + 7 × O=O = 694 + 4956 + 3486 = 9136 kJ. Made: 8 × C=O + 12 × O–H = 6424 + 5568 = 11992 kJ. Whole ΔH = −2856 kJ; per mole = −1428 kJ/mol."},
    {"pattern": "forgot_divide", "check": "common", "expect": -2856,
     "message": "The equation burns 2 mol of C₂H₆, so divide the whole ΔH by 2: −2856 ÷ 2 = −1428 kJ/mol. Leaving it as −2856 forgets the per-mole step."}
]

g[2]["hint"] = "Rearrange to made = broken − ΔH, and mind the double negative."
g[2]["guided_steps"] = [
    say("Rearrange ΔH = broken − made to made = broken − ΔH."),
    box("ΔH is −285, so made = 1845 − (−285). Subtracting a negative adds it: 1845 + ", 285,
        "Two minus signs together become a plus."),
    box("1845 + 285 = ", 2130, "Add.", phase="substitute"),
    box("Check with ΔH = broken − made = 1845 − 2130 = ", -285, "This should return the given ΔH.",
        done="That is the given ΔH, so made = 2130 kJ is right.")
]
g[2]["misconceptions"] = [
    {"pattern": "wrong_rearrange", "check": "common", "expect": 1560,
     "message": "made = broken − ΔH = 1845 − (−285) = 1845 + 285 = 2130 kJ. Doing 1845 + (−285) = 1560 mishandles the double negative."},
    {"pattern": "sign_error", "check": "common", "expect": None,
     "message": "Subtracting −285 means adding 285: 1845 + 285 = 2130 kJ."}
]

g[3]["hint"] = "Rearrange to broken = ΔH + made."
g[3]["guided_steps"] = [
    say("Rearrange ΔH = broken − made to broken = ΔH + made."),
    box("ΔH is +140 and made is 1380, so broken = 140 + ", 1380, "Add the made energy to ΔH."),
    box("140 + 1380 = ", 1520, "Add.", phase="substitute"),
    box("Check with ΔH = broken − made = 1520 − 1380 = ", 140, "This should return the given ΔH.",
        done="That is the given ΔH, so broken = 1520 kJ is right.")
]
g[3]["misconceptions"] = [
    {"pattern": "wrong_rearrange", "check": "common", "expect": 1240,
     "message": "broken = ΔH + made = 140 + 1380 = 1520 kJ. Doing made − ΔH = 1240 subtracts when you should add."}
]

# g[4]: convert A/B string answer to multiple_choice
g[4] = {
    "display": "Reaction A has ΔH = −184 kJ/mol. Reaction B has ΔH = −814 kJ/mol. Which reaction releases more energy per mole?",
    "options": ["Reaction A", "Reaction B"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "The more negative the energy change, the more energy is released.",
    "misconceptions": [
        {"pattern": "sign_confusion", "check": "common", "expect": None,
         "message": "−814 is more negative than −184, so Reaction B releases more energy. A larger negative number means more exothermic."},
        {"pattern": "magnitude_error", "check": "common", "expect": None,
         "message": "Compare the size of the negative values: 814 > 184, so Reaction B releases more energy per mole."}
    ]
}

# g[5]: convert per-gram string answer to numeric single_value
g[5] = {
    "display": ("When 2 mol of hydrogen burns (2H₂ + O₂ → 2H₂O), 486 kJ of energy is released. "
                "Calculate the energy released per gram of hydrogen. (Mr of H₂ = 2, so 1 mol of H₂ has a mass of 2 g.)"),
    "unit": "kJ/g",
    "solutions": [121.5],
    "accept": 0.5,
    "calculator": True,
    "input_type": "single_value",
    "hint": "Find the mass of 2 mol of H₂ in grams, then divide the energy by that mass.",
    "misconceptions": [
        {"pattern": "per_mole_not_gram", "check": "common", "expect": 243,
         "message": "Per gram, not per mole: 2 mol of H₂ weighs 4 g, so 486 ÷ 4 = 121.5 kJ/g. Dividing by 2 mol instead gives 243 kJ/mol, a different quantity."}
    ],
    "guided_steps": [
        say("When 2 mol of H₂ burns, 486 kJ is released. First find the mass of 2 mol of H₂."),
        box("1 mol of H₂ weighs 2 g, so 2 mol weighs 2 × 2 = ", 4, "Multiply moles by the mass of one mole."),
        box("Energy per gram = total ÷ mass = 486 ÷ 4 = ", 121.5, "Divide the energy by the mass in grams.", phase="substitute"),
        box("Check: 4 g × 121.5 = ", 486, "Multiplying back should return the total energy.",
            done="Returns 486 kJ, so 121.5 kJ/g is right.")
    ]
}

# ---------------- sanitize em dashes in preserved fields (worked_examples labels) ----------------
def desanitize(o):
    if isinstance(o, dict):
        return {k: desanitize(v) for k, v in o.items()}
    if isinstance(o, list):
        return [desanitize(v) for v in o]
    if isinstance(o, str):
        return o.replace(" — ", ": ").replace("—", ", ")
    return o
pd = desanitize(pd)

# ---------------- write ----------------
out = json.dumps(pd, ensure_ascii=False, indent=1)
assert "—" not in out, "EM DASH present!"
io.open("lesson_chem_L03_d1de9ba347.json", "w", encoding="utf-8").write(out)
print("OK written, no em dash:", "—" not in out)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
