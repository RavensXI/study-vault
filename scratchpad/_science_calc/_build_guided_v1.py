# -*- coding: utf-8 -*-
import json, io

SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_L01_34b52b21dc_canonical.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/lesson_higher-calculations-L01@34b52b21dc.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---- slim method_card ----
pd["method_card"] = {
    "title": "Titrations and Molar Concentrations",
    "steps": [
        "Convert every volume from cm³ to dm³ by dividing by 1000.",
        "Find the moles of the solution you know: moles = concentration × volume.",
        "Use the mole ratio from the balanced equation to get the moles of the unknown.",
        "Find the unknown's concentration (moles ÷ volume) or mass (moles × Mr).",
    ],
    "content": ("<p>Every titration calculation is the same three moves: <strong>moles of what you know</strong>, "
                "the <strong>mole ratio</strong>, then <strong>the unknown</strong>.</p>"
                "<p>Volumes arrive in cm³. Divide by 1000 to reach dm³ before using \\(c = \\frac{n}{V}\\). "
                "Check the ratio in the balanced equation, as it is not always 1:1. If a mass is given, start with "
                "\\(n = \\frac{\\text{mass}}{M_r}\\). If a volumetric flask is used, the concentration is the same in the "
                "small sample and the whole flask, so scale the moles up by the volumes.</p>"),
    "example": ("<p><strong>Solve:</strong> 20.0 cm³ of 0.125 mol/dm³ HCl neutralises 25.0 cm³ of NaOH (ratio 1:1).</p>"
                "<p>Moles HCl = 0.125 × 0.02 = 0.0025. Ratio 1:1, so 0.0025 mol NaOH. "
                "Concentration = 0.0025 ÷ 0.025 = 0.1 mol/dm³.</p>"),
}

# ---- exam_context: kill em dash in frequency ----
pd["exam_context"]["frequency"] = "High: titration calculations appear almost every year in Separate Chemistry"

# ---- worked_examples: replace em dash in step labels ----
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and isinstance(st["label"], str):
            st["label"] = st["label"].replace(" — ", ": ")

pb = pd["problem_bank"]

# ---- tier descriptions ----
pb["bronze_description"] = ("One formula, one step: convert the volume to dm³ if needed, then use "
                            "moles = concentration × volume, or rearrange it for whatever is missing.")
pb["silver_description"] = ("A full titration: moles of the solution you know, the mole ratio from the "
                            "balanced equation, then the concentration of the one you do not know.")
pb["gold_description"] = ("Multi-step: a mass or a volumetric flask, scaling a small sample up to the whole "
                          "flask, and finishing with mass from moles.")

# ---- add plain hints ----
bronze_hints = [
    "Turn the volume into dm³ first, then multiply by the concentration.",
    "Concentration is moles divided by volume. The volume is already in dm³.",
    "Rearrange to volume = moles ÷ concentration.",
    "Work out the Mr, then moles = mass ÷ Mr. The volume is not needed here.",
    "Change 500 cm³ into dm³, then divide the moles by it.",
    "Change 100 cm³ into dm³, then multiply by the concentration.",
    "One dm³ is 1000 cm³, so divide by 1000.",
    "Work out the Mr of HCl, then divide the mass by it.",
]
silver_hints = [
    "Moles of HCl first, then a 1:1 ratio, then divide by the NaOH volume.",
    "Find moles of NaOH, halve for the 1:2 ratio, then divide by the acid volume.",
    "Moles of HCl, 1:1 ratio, then divide by the NaOH volume.",
    "Moles of Ca(OH)₂, double for the 1:2 ratio, then divide by the HCl volume.",
    "Moles of KOH, 1:1 ratio, then divide by the HNO₃ volume.",
    "Moles of KOH, halve for the 1:2 ratio, then divide by the acid volume.",
]
gold_hints = [
    "Find moles of NaOH, its concentration in the flask, then work through the titration to the HCl.",
    "Work out Mr and moles first, then the flask concentration, then the titration chain.",
    "Moles first (concentration × volume in dm³), then mass = moles × Mr.",
    "The titration gives the concentration in the flask. Scale up to 500 cm³, then find the mass.",
    "Find the concentration from the titration, scale to 250 cm³, then mass = moles × Mr.",
    "The titration gives the flask concentration. Scale to 500 cm³, then multiply by Mr.",
]
for i, h in enumerate(bronze_hints):
    pb["bronze"][i]["hint"] = h
for i, h in enumerate(silver_hints):
    pb["silver"][i]["hint"] = h
for i, h in enumerate(gold_hints):
    pb["gold"][i]["hint"] = h

# ---- rebuild S4 (silver idx3) and S5 (silver idx4) to remove duplicate 0.25 ----
pb["silver"][3]["display"] = ("25.0 cm³ of 0.1 mol/dm³ Ca(OH)₂ is neutralised by 10.0 cm³ of HCl. The equation is: "
                              "Ca(OH)₂ + 2HCl → CaCl₂ + 2H₂O. Calculate the concentration of the HCl in mol/dm³.")
pb["silver"][3]["solutions"] = [0.5]
pb["silver"][3]["misconceptions"] = [
    {"check": "common", "pattern": "mole_ratio",
     "message": ("Ca(OH)₂ : HCl = 1 : 2. Moles Ca(OH)₂ = 0.1 × 0.025 = 0.0025. Moles HCl = 0.0025 × 2 = 0.005. "
                 "Conc = 0.005 ÷ 0.01 = 0.5 mol/dm³."), "expect": 0.25},
    {"check": "common", "pattern": "forgot_ratio",
     "message": "The equation shows 2 moles of HCl per mole of Ca(OH)₂, so double the moles.", "expect": None},
]
pb["silver"][4]["display"] = ("25.0 cm³ of 0.2 mol/dm³ KOH is neutralised by 12.5 cm³ of HNO₃. The equation is: "
                              "KOH + HNO₃ → KNO₃ + H₂O. Calculate the concentration of the HNO₃ in mol/dm³.")
pb["silver"][4]["solutions"] = [0.4]
pb["silver"][4]["misconceptions"] = [
    {"check": "common", "pattern": "wrong_volume",
     "message": ("Moles KOH = 0.2 × 0.025 = 0.005. Ratio 1:1. Conc HNO₃ = 0.005 ÷ 0.0125 = 0.4 mol/dm³. "
                 "Use the HNO₃ volume (12.5 cm³) in the final step."), "expect": 0.2},
]

# ---- expects for all other misconceptions (tier, prob_idx, misc_idx) -> value ----
expects = {
    ("bronze", 0, 0): 2.5, ("bronze", 0, 1): None,
    ("bronze", 1, 0): 0.125,
    ("bronze", 2, 0): 0.1,
    ("bronze", 3, 0): None,
    ("bronze", 4, 0): 0.0003,
    ("bronze", 5, 0): 25,
    ("bronze", 6, 0): 0.5,
    ("bronze", 7, 0): None,
    ("silver", 0, 0): None, ("silver", 0, 1): 0.125,
    ("silver", 1, 0): 0.25, ("silver", 1, 1): None,
    ("silver", 2, 0): 0.15,
    ("silver", 5, 0): 0.5, ("silver", 5, 1): None,
    ("gold", 0, 0): None, ("gold", 0, 1): 1.6,
    ("gold", 1, 0): None, ("gold", 1, 1): 0.2,
    ("gold", 2, 0): 4562.5, ("gold", 2, 1): None,
    ("gold", 3, 0): None, ("gold", 3, 1): 0.112,
    ("gold", 4, 0): None, ("gold", 4, 1): 0.16,
    ("gold", 5, 0): 0.1325, ("gold", 5, 1): None,
}
for (tier, pi, mi), val in expects.items():
    pb[tier][pi]["misconceptions"][mi]["expect"] = val

print("build stage 1 ok")
json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
