# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # proper minus sign (not em dash)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s):
    return {"say": s}

def misc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

pd = {}

pd["method_card"] = {
    "title": "Bond Energy Calculations",
    "steps": [
        "List all bonds broken in the reactants: multiply each bond energy by how many of that bond there are.",
        "List all bonds made in the products the same way, using the coefficients (2H2O has 4 O-H bonds).",
        "ΔH = energy to break bonds " + MINUS + " energy released making bonds.",
        "Negative ΔH = exothermic; positive ΔH = endothermic."
    ],
    "content": ("<p>Two halves: <strong>bonds broken</strong> (energy in) and "
                "<strong>bonds made</strong> (energy out).</p>"
                "<p>For each bond type, multiply its bond energy by the number of that bond, then add within each half. "
                "Use the balanced equation's coefficients: 2H2O has 4 O-H bonds, not 2.</p>"
                "<p><strong>ΔH = energy in " + MINUS + " energy out.</strong> Negative means exothermic; positive means endothermic. "
                "Check whether your board gives you the bond energies or expects them stated in the question.</p>")
}

pd["topic_links"] = {"prerequisites": []}
pd["exam_context"] = {
    "marks": "3–5 per calculation",
    "paper": "Chemistry paper (combined science)",
    "frequency": "Common: bond energy questions appear regularly"
}

bronze = []

bronze.append({
    "unit": "kJ",
    "display": "H2 + Cl2 → 2HCl. Bond energies: H-H = 436, Cl-Cl = 243, H-Cl = 432 kJ/mol. What is the total energy needed to break all bonds in the reactants?",
    "solutions": [679],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Add up all bond energies in the reactants",
    "hint": "Add only the reactant bond energies: H-H plus Cl-Cl.",
    "misconceptions": [
        misc("wrong_count", 1111,
             "Only the reactant bonds break here: H-H (436) + Cl-Cl (243) = 679 kJ. The H-Cl bond is made in the product, so do not add it to the broken total.")
    ],
    "guided_steps": [
        sayonly("The reactants are H2 (one H-H bond) and Cl2 (one Cl-Cl bond). Only reactant bonds break in this step."),
        box("Number of H-H bonds breaking = ", 1, "H2 is a single H-H bond."),
        box("Number of Cl-Cl bonds breaking = ", 1, "Cl2 is a single Cl-Cl bond."),
        sayonly("Now multiply each bond energy by its count and add them."),
        box("Energy to break H-H (1 × 436) = ", 436, "One H-H bond at 436 kJ.", phase="substitute"),
        box("Energy to break Cl-Cl (1 × 243) = ", 243, "One Cl-Cl bond at 243 kJ."),
        box("Total energy in (436 + 243) = ", 679, "Add the two broken-bond energies.", done="679 kJ to break every reactant bond.")
    ]
})

bronze.append({
    "unit": "kJ",
    "display": "H2 + Cl2 → 2HCl. Bond energies: H-Cl = 432 kJ/mol. What is the total energy released making all bonds in the products (2 HCl molecules)?",
    "solutions": [864],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Multiply bond energy by number of bonds made",
    "hint": "Two HCl molecules means two H-Cl bonds, so multiply 432 by 2.",
    "misconceptions": [
        misc("forgot_coefficient", 432,
             "There are 2 HCl molecules, so 2 H-Cl bonds: 2 × 432 = 864 kJ. Using just one bond (432) misses the coefficient.")
    ],
    "guided_steps": [
        sayonly("The product is 2 HCl. Each HCl has one H-Cl bond, so count them first."),
        box("H-Cl bonds in one HCl molecule = ", 1, "H-Cl: one bond per molecule."),
        box("Number of HCl molecules = ", 2, "The coefficient in 2HCl."),
        sayonly("Total H-Cl bonds = 1 × 2. Each H-Cl bond releases 432 kJ when it forms, so multiply."),
        box("Total H-Cl bonds made (1 × 2) = ", 2, "One bond per molecule, two molecules.", phase="substitute"),
        box("Energy released (2 × 432) = ", 864, "Two H-Cl bonds at 432 kJ each.", done="864 kJ released making the product bonds.")
    ]
})

bronze.append({
    "unit": "kJ/mol",
    "display": "Using your answers above (679 kJ in, 864 kJ out), calculate ΔH for H2 + Cl2 → 2HCl.",
    "solutions": [-185],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "ΔH = energy in " + MINUS + " energy out",
    "hint": "ΔH = energy in minus energy out: 679 " + MINUS + " 864.",
    "misconceptions": [
        misc("wrong_sign", 185,
             "ΔH = energy in " + MINUS + " energy out = 679 " + MINUS + " 864 = " + MINUS + "185 kJ/mol. Getting +185 means the numbers were subtracted the wrong way round. The negative sign shows the reaction is exothermic.")
    ],
    "guided_steps": [
        sayonly("ΔH = energy in (bonds broken) " + MINUS + " energy out (bonds made)."),
        box("Energy in (bonds broken) = ", 679, "The 679 kJ you found for breaking bonds."),
        box("Energy out (bonds made) = ", 864, "The 864 kJ released making bonds."),
        sayonly("Subtract: energy in " + MINUS + " energy out."),
        box("ΔH (679 " + MINUS + " 864) = ", -185, "679 take away 864 gives a negative number.", phase="substitute"),
        box("Energy released overall (864 " + MINUS + " 679) = ", 185, "How much more came out than went in.", done="185 kJ released, so ΔH = " + MINUS + "185 kJ/mol, exothermic.")
    ]
})

bronze.append({
    "unit": "kJ/mol",
    "display": "In a bond energy calculation, bonds broken required 500 kJ and bonds made released 720 kJ. Calculate ΔH.",
    "solutions": [-220],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "ΔH = energy in " + MINUS + " energy out",
    "hint": "ΔH = bonds broken minus bonds made: 500 " + MINUS + " 720.",
    "misconceptions": [
        misc("wrong_sign", 220,
             "ΔH = broken " + MINUS + " made = 500 " + MINUS + " 720 = " + MINUS + "220 kJ/mol (exothermic). +220 comes from subtracting the wrong way round.")
    ],
    "guided_steps": [
        sayonly("ΔH = energy to break " + MINUS + " energy released."),
        box("Energy in (broken) = ", 500, "Bonds broken took in 500 kJ."),
        box("Energy out (made) = ", 720, "Bonds made released 720 kJ."),
        sayonly("Subtract: in " + MINUS + " out."),
        box("ΔH (500 " + MINUS + " 720) = ", -220, "500 take away 720 is negative.", phase="substitute"),
        box("Energy released overall (720 " + MINUS + " 500) = ", 220, "How much more came out than went in.", done="220 kJ released, so ΔH = " + MINUS + "220 kJ/mol, exothermic.")
    ]
})

bronze.append({
    "unit": "",
    "display": "In a bond energy calculation, ΔH = +150 kJ/mol. Is the reaction exothermic or endothermic? Enter 1 for exothermic or 2 for endothermic.",
    "solutions": [2],
    "calculator": False,
    "input_type": "single_value",
    "equation_hint": "Positive ΔH = endothermic; negative ΔH = exothermic",
    "hint": "Positive ΔH absorbs energy, and absorbing energy is endothermic.",
    "misconceptions": [
        misc("wrong_sign", 1,
             "Positive ΔH means energy was absorbed overall: endothermic (answer 2). Negative ΔH is exothermic. It is easy to swap these two round.")
    ],
    "guided_steps": [
        sayonly("Two facts fix the sign: energy IN breaks bonds, energy OUT makes them, and ΔH = in " + MINUS + " out."),
        box("ΔH is +150, so which was bigger? Enter 1 if energy in was bigger, 2 if energy out was bigger = ", 1, "A positive difference means the first number, energy in, was larger."),
        sayonly("More energy going in than coming out means the reaction pulls energy from its surroundings."),
        box("A reaction that takes energy in is endothermic or exothermic? Enter 2 for endothermic, 1 for exothermic = ", 2, "'Endo' means in.", phase="substitute"),
        box("So for ΔH = +150 the answer is: enter 2 for endothermic = ", 2, "Positive ΔH means endothermic.", done="Positive ΔH = endothermic. Answer: 2.")
    ]
})

silver = []

silver.append({
    "unit": "kJ",
    "display": "2H2 + O2 → 2H2O. Bond energies: H-H = 436, O=O = 498, O-H = 463 kJ/mol. Calculate the total energy to break all bonds in the reactants.",
    "solutions": [1370],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "Bonds broken: 2×H-H + 1×O=O",
    "hint": "Two H2 molecules give two H-H bonds; add the single O=O.",
    "misconceptions": [
        misc("forgot_coefficient", 934,
             "There are 2 H2 molecules, so 2 H-H bonds: 2 × 436 = 872. Add the O=O (498) for 1370 kJ. Using one H-H (436) gives 934 and undercounts.")
    ],
    "guided_steps": [
        sayonly("Reactants are 2 H2 and 1 O2. Count each bond type first."),
        box("Number of H-H bonds (2 H2) = ", 2, "Two H2 molecules, one H-H bond each."),
        box("Number of O=O bonds (1 O2) = ", 1, "One O2 molecule, one O=O bond."),
        sayonly("Multiply each count by its bond energy and add."),
        box("Energy from H-H bonds (2 × 436) = ", 872, "Two H-H bonds at 436 kJ.", phase="substitute"),
        box("Energy from O=O bond (1 × 498) = ", 498, "One O=O bond at 498 kJ."),
        box("Total energy in (872 + 498) = ", 1370, "Add the two broken-bond totals.", done="1370 kJ to break all reactant bonds.")
    ]
})

silver.append({
    "unit": "",
    "display": "2H2 + O2 → 2H2O. 2 molecules of H2O contain how many O-H bonds in total?",
    "solutions": [4],
    "calculator": False,
    "input_type": "single_value",
    "equation_hint": "Each H2O has 2 O-H bonds",
    "hint": "Each water molecule has two O-H bonds, and there are two molecules.",
    "misconceptions": [
        misc("forgot_coefficient", 2,
             "Each H2O has 2 O-H bonds and there are 2 molecules: 2 × 2 = 4. Counting only one molecule gives 2.")
    ],
    "guided_steps": [
        sayonly("Each water molecule H2O has two O-H bonds (H-O-H)."),
        box("O-H bonds in one H2O molecule = ", 2, "H-O-H: two O-H bonds."),
        sayonly("Now scale up to 2 molecules."),
        box("Total O-H bonds (2 × 2) = ", 4, "Two O-H bonds per molecule, two molecules.", phase="substitute"),
        box("Check (4 ÷ 2 molecules) = ", 2, "Divide back by the number of molecules.", done="2 O-H bonds per molecule, so 4 in total.")
    ]
})

silver.append({
    "unit": "kJ",
    "display": "2H2 + O2 → 2H2O. 4 O-H bonds are formed (energy per O-H = 463 kJ/mol). Calculate total energy released making bonds.",
    "solutions": [1852],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "4 × 463",
    "hint": "Multiply the number of bonds by the bond energy: 4 times 463.",
    "misconceptions": [
        misc("wrong_count", 926,
             "4 O-H bonds form: 4 × 463 = 1852 kJ. Using only 2 bonds (926) misses two of them.")
    ],
    "guided_steps": [
        sayonly("Every bond made releases its bond energy. Here 4 O-H bonds each release 463 kJ."),
        box("Number of O-H bonds made = ", 4, "The four O-H bonds in 2 H2O."),
        box("Energy released by one O-H bond = ", 463, "The given O-H bond energy."),
        sayonly("Multiply the count by the bond energy."),
        box("Energy released (4 × 463) = ", 1852, "Four bonds at 463 kJ each.", phase="substitute"),
        box("Check (1852 ÷ 4) = ", 463, "Divide back by the number of bonds.", done="Back to 463 per bond, so 1852 kJ released.")
    ]
})

silver.append({
    "unit": "kJ/mol",
    "display": "Using energy broken = 1,370 kJ and energy made = 1,852 kJ, calculate ΔH for 2H2 + O2 → 2H2O.",
    "solutions": [-482],
    "calculator": True,
    "input_type": "single_value",
    "equation_hint": "ΔH = energy in " + MINUS + " energy out",
    "hint": "ΔH = broken minus made: 1370 " + MINUS + " 1852.",
    "misconceptions": [
        misc("wrong_sign", 482,
             "ΔH = broken " + MINUS + " made = 1370 " + MINUS + " 1852 = " + MINUS + "482 kJ/mol (exothermic). +482 is the wrong-way subtraction.")
    ],
    "guided_steps": [
        sayonly("ΔH = energy in (broken) " + MINUS + " energy out (made)."),
        box("Energy in (broken) = ", 1370, "1370 kJ to break the reactant bonds."),
        box("Energy out (made) = ", 1852, "1852 kJ released making the product bonds."),
        sayonly("Subtract: in " + MINUS + " out."),
        box("ΔH (1370 " + MINUS + " 1852) = ", -482, "1370 take away 1852 is negative.", phase="substitute"),
        box("Energy released overall (1852 " + MINUS + " 1370) = ", 482, "How much more came out than went in.", done="482 kJ released, so ΔH = " + MINUS + "482 kJ/mol, exothermic.")
    ]
})

gold = []

gold.append({
    "unit": "kJ/mol",
    "display": "N2 + 3H2 → 2NH3. Bond energies: N≡N = 945, H-H = 436, N-H = 391 kJ/mol. Calculate ΔH.",
    "solutions": [-93],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Break all reactant bonds, make all 6 N-H bonds in 2NH3, then ΔH = in " + MINUS + " out.",
    "misconceptions": [
        misc("forgot_coefficient", 1080,
             "2 NH3 has 6 N-H bonds (3 per molecule × 2 molecules), so bonds made = 6 × 391 = 2346. Using only 3 N-H (1173) gives +1080 and the wrong sign."),
        misc("wrong_sign", 93,
             "ΔH = broken " + MINUS + " made = 2253 " + MINUS + " 2346 = " + MINUS + "93 kJ/mol. +93 is the reversed subtraction.")
    ],
    "guided_steps": [
        sayonly("Break the reactant bonds first: one N≡N and three H-H."),
        box("Energy to break N≡N (1 × 945) = ", 945, "One triple bond at 945 kJ."),
        box("Energy to break H-H (3 × 436) = ", 1308, "Three H-H bonds at 436 kJ each."),
        box("Total energy in (945 + 1308) = ", 2253, "Add the broken-bond energies."),
        sayonly("Now bonds made: 2 NH3, each with 3 N-H bonds, so 6 N-H in total."),
        box("Number of N-H bonds made (2 × 3) = ", 6, "Two molecules, three N-H bonds each."),
        box("Energy released (6 × 391) = ", 2346, "Six N-H bonds at 391 kJ each."),
        sayonly("Combine: ΔH = energy in " + MINUS + " energy out."),
        box("ΔH (2253 " + MINUS + " 2346) = ", -93, "2253 take away 2346 is a small negative.", phase="substitute"),
        box("Energy released overall (2346 " + MINUS + " 2253) = ", 93, "How much more came out than went in.", done="93 kJ released, so ΔH = " + MINUS + "93 kJ/mol, exothermic.")
    ]
})

gold.append({
    "unit": "kJ/mol",
    "display": "CH4 + 2O2 → CO2 + 2H2O. Bond energies: C-H = 412, O=O = 498, C=O = 743, O-H = 463 kJ/mol. Calculate ΔH.",
    "solutions": [-694],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Count every bond: 4 C-H and 2 O=O broken; 2 C=O and 4 O-H made. ΔH = in " + MINUS + " out.",
    "misconceptions": [
        misc("wrong_count", 49,
             "CO2 has 2 C=O bonds: 2 × 743 = 1486. With 4 O-H (1852) the bonds made total 3338, so ΔH = 2644 " + MINUS + " 3338 = " + MINUS + "694 kJ/mol. Counting only one C=O gives +49."),
        misc("wrong_sign", 694,
             "ΔH = broken " + MINUS + " made = 2644 " + MINUS + " 3338 = " + MINUS + "694 kJ/mol (exothermic). +694 is the reversed subtraction.")
    ],
    "guided_steps": [
        sayonly("Break the reactant bonds. CH4 has 4 C-H bonds; 2 O2 gives 2 O=O bonds."),
        box("Number of C-H bonds = ", 4, "CH4: four C-H bonds."),
        box("Energy to break C-H bonds (4 × 412) = ", 1648, "Four C-H bonds at 412 kJ each."),
        box("Energy to break O=O bonds (2 × 498) = ", 996, "Two O=O bonds at 498 kJ each."),
        box("Total energy in (1648 + 996) = ", 2644, "Add the broken-bond energies."),
        sayonly("Bonds made: CO2 has 2 C=O bonds; 2 H2O gives 4 O-H bonds."),
        box("Energy from C=O bonds (2 × 743) = ", 1486, "Two C=O bonds at 743 kJ each."),
        box("Energy from O-H bonds (4 × 463) = ", 1852, "Four O-H bonds at 463 kJ each."),
        box("Total energy out (1486 + 1852) = ", 3338, "Add the made-bond energies."),
        sayonly("Combine: ΔH = energy in " + MINUS + " energy out."),
        box("ΔH (2644 " + MINUS + " 3338) = ", -694, "2644 take away 3338 is negative.", phase="substitute"),
        box("Energy released overall (3338 " + MINUS + " 2644) = ", 694, "How much more came out than went in.", done="694 kJ released, so ΔH = " + MINUS + "694 kJ/mol, exothermic.")
    ]
})

gold.append({
    "unit": "kJ",
    "display": "A reaction has bonds broken = 1,200 kJ and ΔH = +300 kJ/mol. Calculate the energy released when bonds form in the products.",
    "solutions": [900],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Rearrange ΔH = in " + MINUS + " out to energy out = in " + MINUS + " ΔH.",
    "misconceptions": [
        misc("wrong_rearrange", 1500,
             "ΔH = energy in " + MINUS + " energy out, so energy out = energy in " + MINUS + " ΔH = 1200 " + MINUS + " 300 = 900 kJ. Adding (1500) rearranges it wrongly.")
    ],
    "guided_steps": [
        sayonly("ΔH = energy in " + MINUS + " energy out. Rearrange for the unknown: energy out = energy in " + MINUS + " ΔH."),
        box("Energy in (bonds broken) = ", 1200, "Given as 1200 kJ."),
        box("ΔH = +", 300, "Given as +300 kJ/mol."),
        sayonly("Substitute into energy out = energy in " + MINUS + " ΔH."),
        box("Energy out (1200 " + MINUS + " 300) = ", 900, "Subtract ΔH from the energy in.", phase="substitute"),
        box("Check (energy in " + MINUS + " energy out = 1200 " + MINUS + " 900) = ", 300, "This should give back ΔH.", done="Gives back ΔH = +300, so 900 kJ is released making bonds.")
    ]
})

pd["problem_bank"] = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "One step at a time: break the reactant bonds, make the product bonds, then combine with ΔH = energy in " + MINUS + " energy out.",
    "silver_description": "Count bonds using the balanced equation's coefficients, then work out the energy broken, energy made and ΔH.",
    "gold_description": "Full calculation in one pass: every bond type on both sides, then ΔH = total broken " + MINUS + " total made."
}

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one bond step at a time",
        "steps": [
            "A bond energy sum has two halves: energy to <strong>break</strong> the reactant bonds (energy in) and energy <strong>released</strong> making the product bonds (energy out).",
            "For each bond type, multiply its bond energy by how many of that bond there are, then add within each half.",
            "Finish with ΔH = energy in " + MINUS + " energy out. A negative answer means energy is released (exothermic)."
        ],
        "example": {
            "question": "Bonds broken need 400 kJ and bonds made release 550 kJ. Find ΔH.",
            "steps": [
                {"label": "Energy in", "content": "<p>400 kJ (bonds broken)</p>"},
                {"label": "Energy out", "content": "<p>550 kJ (bonds made)</p>"},
                {"label": "Check", "content": "<p>Energy out is bigger, so ΔH will be negative.</p>"},
                {"label": "Answer", "content": "<p>ΔH = 400 " + MINUS + " 550 = <strong>" + MINUS + "150 kJ/mol (exothermic)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: count bonds from the balanced equation",
        "steps": [
            "Use the big numbers in the equation. 2H2O means 2 molecules, and each H2O holds 2 O-H bonds, so 4 O-H bonds in total.",
            "Multiply every bond energy by its full count before adding. Miss a coefficient and the whole answer drifts.",
            "Then ΔH = total broken " + MINUS + " total made, keeping the sign."
        ],
        "example": {
            "question": "2H2 + O2 → 2H2O. H-H = 436, O=O = 498, O-H = 463. Find ΔH.",
            "steps": [
                {"label": "Bonds broken", "content": "<p>2×436 + 498 = 1370 kJ</p>"},
                {"label": "Bonds made", "content": "<p>4×463 = 1852 kJ (four O-H bonds)</p>"},
                {"label": "Check", "content": "<p>More energy out than in, so ΔH is negative.</p>"},
                {"label": "Answer", "content": "<p>ΔH = 1370 " + MINUS + " 1852 = <strong>" + MINUS + "482 kJ/mol</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: the full calculation in one pass",
        "steps": [
            "Work the whole reaction: count every bond type on both sides, multiply by bond energies and coefficients, and total each half.",
            "Watch molecules with several bonds: CH4 has 4 C-H, CO2 has 2 C=O, 2NH3 has 6 N-H.",
            "ΔH = total broken " + MINUS + " total made. Negative is exothermic, positive is endothermic."
        ],
        "example": {
            "question": "N2 + 3H2 → 2NH3. N≡N = 945, H-H = 436, N-H = 391. Find ΔH.",
            "steps": [
                {"label": "Bonds broken", "content": "<p>945 + 3×436 = 2253 kJ</p>"},
                {"label": "Bonds made", "content": "<p>6×391 = 2346 kJ (six N-H bonds)</p>"},
                {"label": "Check", "content": "<p>Energy out slightly bigger, so a small negative ΔH.</p>"},
                {"label": "Answer", "content": "<p>ΔH = 2253 " + MINUS + " 2346 = <strong>" + MINUS + "93 kJ/mol</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

pd["guided"] = {
    "opener": {
        "steps": [
            sayonly("A demolition-and-rebuild puzzle. No chemistry yet, just money."),
            box("A builder pays £679 to knock down an old shed, then gets £864 back selling salvaged materials while rebuilding. Better off by £", 185,
                "Money you got back minus money you spent: 864 " + MINUS + " 679."),
            sayonly("Now a different job."),
            box("On a second shed, knocking down costs £720 but the salvage only pays back £500. This time you end up worse off. Worse off by £", 220,
                "How much more you spent than you got back: 720 " + MINUS + " 500."),
            sayonly("That is exactly a bond energy calculation. Breaking bonds is the demolition COST (energy in); making bonds is the salvage PAYBACK (energy out), and <strong>ΔH = energy in " + MINUS + " energy out</strong>. Shed 1: 679 in, 864 out, so 185 kJ is released (exothermic, written ΔH = " + MINUS + "185). Shed 2: 720 in, 500 out, so 220 kJ is absorbed (endothermic, ΔH = +220).")
        ]
    },
    "teach": {
        "bronze": {
            "display": "Work through H2 + Br2 → 2HBr. Bond energies: H-H = 436, Br-Br = 193, H-Br = 366 kJ/mol. Find ΔH.",
            "steps": [
                sayonly("First, break the reactant bonds. H2 is one H-H bond; Br2 is one Br-Br bond."),
                box("Energy to break H-H (1 × 436) = ", 436, "One H-H bond at 436 kJ."),
                box("Energy to break Br-Br (1 × 193) = ", 193, "One Br-Br bond at 193 kJ."),
                box("Total energy in (436 + 193) = ", 629, "Add the two broken-bond energies.", done="629 kJ to break the reactants."),
                sayonly("Now the bonds made. 2 HBr means 2 H-Br bonds."),
                box("Energy released (2 × 366) = ", 732, "Two H-Br bonds at 366 kJ each."),
                sayonly("Combine: ΔH = energy in " + MINUS + " energy out."),
                box("ΔH (629 " + MINUS + " 732) = ", -103, "Subtract energy out from energy in.", done=MINUS + "103 kJ/mol, negative so exothermic. That is the whole method.")
            ]
        },
        "silver": {
            "display": "Work through N2 + O2 → 2NO. Bond energies: N≡N = 945, O=O = 498, N=O = 630 kJ/mol. Find ΔH.",
            "steps": [
                sayonly("Break the reactants. N2 is one N≡N triple bond; O2 is one O=O bond."),
                box("Energy to break N≡N = ", 945, "The triple bond, 945 kJ."),
                box("Energy to break O=O = ", 498, "498 kJ."),
                box("Total energy in (945 + 498) = ", 1443, "Add the broken-bond energies."),
                sayonly("Bonds made: 2 NO molecules, one N=O bond each. Handling that coefficient 2 is the new move."),
                box("Number of N=O bonds made (2 × 1) = ", 2, "Two molecules, one N=O bond each."),
                box("Energy released (2 × 630) = ", 1260, "Two N=O bonds at 630 kJ each."),
                sayonly("Combine."),
                box("ΔH (1443 " + MINUS + " 1260) = ", 183, "Energy in minus energy out.", done="+183 kJ/mol, positive so endothermic. The coefficient was the whole point.")
            ]
        },
        "gold": {
            "display": "Work through 2CO + O2 → 2CO2. Bond energies: C≡O = 1077, O=O = 498, C=O = 805 kJ/mol. Find ΔH.",
            "steps": [
                sayonly("Break the reactants: 2 CO (each one C≡O) and one O2."),
                box("Number of C≡O bonds (2 × 1) = ", 2, "Two CO molecules, one C≡O bond each."),
                box("Energy to break the C≡O bonds (2 × 1077) = ", 2154, "Two triple bonds at 1077 kJ each."),
                box("Energy to break O=O = ", 498, "498 kJ."),
                box("Total energy in (2154 + 498) = ", 2652, "Add the broken-bond energies."),
                sayonly("Bonds made: 2 CO2, each with two C=O bonds, so 4 C=O in total."),
                box("Number of C=O bonds made (2 × 2) = ", 4, "Two CO2 molecules, two C=O bonds each."),
                box("Energy released (4 × 805) = ", 3220, "Four C=O bonds at 805 kJ each."),
                sayonly("Combine."),
                box("ΔH (2652 " + MINUS + " 3220) = ", -568, "Energy in minus energy out.", done=MINUS + "568 kJ/mol, exothermic. Counting all four C=O bonds was the whole point.")
            ]
        }
    }
}

pd["related_videos"] = []
pd["worked_examples"] = [
    {
        "steps": [
            {"label": "Step 1: Bonds broken (energy in)", "content": "<p>1 × H-H: 436 kJ + 1 × Cl-Cl: 243 kJ = 679 kJ</p>"},
            {"label": "Step 2: Bonds made (energy out)", "content": "<p>2 × H-Cl: 2 × 432 = 864 kJ</p>"},
            {"label": "Step 3: Calculate ΔH", "content": "<p>ΔH = 679 " + MINUS + " 864</p>"},
            {"label": "Answer", "content": "<p>ΔH = <strong>" + MINUS + "185 kJ/mol (exothermic)</strong></p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "H2 + Cl2 → 2HCl. Bond energies: H-H = 436, Cl-Cl = 243, H-Cl = 432 kJ/mol. Calculate ΔH.",
        "difficulty": "Bronze"
    },
    {
        "steps": [
            {"label": "Step 1: Bonds broken", "content": "<p>2 × H-H: 872 kJ + 1 × O=O: 498 kJ = 1,370 kJ</p>"},
            {"label": "Step 2: Bonds made (2 × H2O = 4 O-H bonds)", "content": "<p>4 × O-H: 4 × 463 = 1,852 kJ</p>"},
            {"label": "Step 3: ΔH", "content": "<p>ΔH = 1,370 " + MINUS + " 1,852</p>"},
            {"label": "Answer", "content": "<p>ΔH = <strong>" + MINUS + "482 kJ/mol (exothermic)</strong></p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "2H2 + O2 → 2H2O. Bond energies: H-H = 436, O=O = 498, O-H = 463 kJ/mol. Calculate ΔH.",
        "difficulty": "Silver"
    },
    {
        "steps": [
            {"label": "Step 1: Bonds broken", "content": "<p>1 × N≡N: 945 kJ + 3 × H-H: 3×436 = 1,308 kJ. Total = 2,253 kJ</p>"},
            {"label": "Step 2: Bonds made (2 × NH3 = 6 N-H bonds)", "content": "<p>6 × N-H: 6 × 391 = 2,346 kJ</p>"},
            {"label": "Step 3: ΔH", "content": "<p>ΔH = 2,253 " + MINUS + " 2,346</p>"},
            {"label": "Answer", "content": "<p>ΔH = <strong>" + MINUS + "93 kJ/mol (exothermic)</strong></p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "N2 + 3H2 → 2NH3. Bond energies: N≡N = 945, H-H = 436, N-H = 391 kJ/mol. Calculate ΔH.",
        "difficulty": "Gold"
    }
]

out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/lesson_chemistry-calculations-L03@ab6f9a45d2.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))

EM = "—"
bad = []
def scan(o, p):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            scan(v, p + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, p + "[%d]" % i)
    elif isinstance(o, str) and EM in o:
        bad.append(p)
scan(pd, "pd")
print("wrote", out)
print("em-dash offenders in student-facing (should be empty):", bad)
