# -*- coding: utf-8 -*-
import json, io

SRC = "_L01_titration_canonical.json"
OUT = "lesson_higher-calculations-L01@146c1cc6d7.json"
pd = json.load(io.open(SRC, encoding="utf-8"))

# ---------- 1. method_card: slim to <=140 words, remove em dash ----------
pd["method_card"]["content"] = (
    "<p>Titration and concentration questions all use the same toolkit. Pick the "
    "formula that links what you know to what you want.</p>"
    "<p><strong>Core formulas:</strong> moles = concentration × volume; "
    "concentration = moles ÷ volume; moles = mass ÷ Mr.</p>"
    "<p>Volumes must be in <strong>dm³</strong>: divide cm³ by 1000 before you "
    "start. In a titration, find the moles of the solution you fully know, use the "
    "balanced equation's ratio to reach the other substance, then divide by its "
    "volume. If a sample is taken from a larger flask, scale the moles up to the "
    "whole flask at the end.</p>"
)
# method_card.steps kept as-is (clean)

# ---------- 2. exam_context: kill em dash ----------
pd["exam_context"]["frequency"] = (
    "High: titration calculations appear almost every year in Separate Chemistry"
)

# ---------- 3. worked_examples: replace em-dash labels with colon ----------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pb = pd["problem_bank"]

# ---------- 4. tier descriptions ----------
pb["bronze_description"] = ("One formula and, where needed, one unit conversion: "
                            "moles, concentration, or volume in a single step.")
pb["silver_description"] = ("A titration in one pass: moles of the known solution, "
                            "the balanced ratio, then the other concentration.")
pb["gold_description"] = ("Multi-step: mass to moles, scaling a sample up to the whole "
                          "flask, then chaining to a final mass or concentration.")

# ============================================================
# Helpers to build steps
# ============================================================
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def sayonly(say):
    return {"say": say}

def setmc(prob, idx, expect, message=None):
    m = prob["misconceptions"][idx]
    m["expect"] = expect
    if message is not None:
        m["message"] = message

# ============================================================
# BRONZE
# ============================================================
B = pb["bronze"]

# B0: moles in 25 cm3 of 0.1 mol/dm3  -> 0.0025
B[0]["hint"] = "Convert 25.0 cm³ to dm³ first, then multiply by the concentration."
B[0]["guided_steps"] = [
    sayonly("The formula is moles = concentration × volume, with the volume in dm³."),
    box("First convert the volume. 25.0 ÷ 1000 = ", 0.025, "Divide cm³ by 1000."),
    box("moles = 0.1 × 0.025 = ", 0.0025, "Multiply concentration by volume.", phase="substitute"),
    box("Check by dividing back: 0.0025 ÷ 0.025 = ", 0.1,
        "Divide moles by the volume; it should return the concentration.", phase="substitute",
        done="That returns the 0.1 mol/dm³ we started with, so 0.0025 mol is right."),
]
setmc(B[0], 0, 2.5)  # used 25 (not converted)
setmc(B[0], 1, 0.025,
      "If you divided by 100 instead of 1000 you would get 0.025 mol. The step is ÷1000: "
      "25.0 cm³ = 0.025 dm³, so moles = 0.1 × 0.025 = 0.0025 mol.")

# B1: c = 0.5/0.25 -> 2
B[1]["hint"] = "Concentration = moles ÷ volume. The volume is already in dm³."
B[1]["guided_steps"] = [
    sayonly(r"Concentration = moles ÷ volume. The volume is already 0.25 dm³, so no conversion is needed."),
    box("Write the number you divide by (the volume in dm³): ", 0.25, "Copy the volume; it is already in dm³."),
    box("Now divide: 0.5 ÷ 0.25 = ", 2, "How many 0.25s fit into 0.5? Two.", phase="substitute"),
    box("Check: 2 × 0.25 = ", 0.5, "Multiply concentration by volume to get moles back.",
        phase="substitute", done="Back to 0.5 mol, so 2 mol/dm³ is right."),
]
setmc(B[1], 0, 0.125)  # multiplied instead of divided: 0.5*0.25

# B2: V = 0.2/0.5 -> 0.4
B[2]["hint"] = "Rearrange to volume = moles ÷ concentration."
B[2]["guided_steps"] = [
    sayonly("Rearrange concentration = moles ÷ volume into volume = moles ÷ concentration."),
    box("Write the concentration you divide by: ", 0.5, "Copy the concentration."),
    box("volume = 0.2 ÷ 0.5 = ", 0.4, "How many 0.5s make 0.2? Less than one.", phase="substitute"),
    box("Check: 0.5 × 0.4 = ", 0.2, "Multiply back to reach the moles.",
        phase="substitute", done="That gives back 0.2 mol, so 0.4 dm³ is right."),
]
setmc(B[2], 0, 0.1)  # multiplied c x V instead of rearranging

# B3: moles NaOH = 4/40 -> 0.1
B[3]["hint"] = "Find the Mr of NaOH, then moles = mass ÷ Mr. The volume is not needed."
B[3]["guided_steps"] = [
    sayonly("Moles = mass ÷ Mr. First find the Mr of NaOH."),
    box("Mr of NaOH = 23 + 16 + 1 = ", 40, "Add the three Ar values."),
    box("moles = 4.0 ÷ 40 = ", 0.1, "Divide the mass by the Mr.", phase="substitute"),
    box("Check: 0.1 × 40 = ", 4, "Multiply moles by Mr to get the mass back.",
        phase="substitute", done="Back to 4.0 g, so 0.1 mol is right. The 500 cm³ was not needed here."),
]
setmc(B[3], 0, None)

# B4: c = 0.15/0.5 -> 0.3
B[4]["hint"] = "Convert 500 cm³ to dm³, then concentration = moles ÷ volume."
B[4]["guided_steps"] = [
    sayonly("Concentration = moles ÷ volume, with the volume in dm³."),
    box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide cm³ by 1000."),
    box("concentration = 0.15 ÷ 0.5 = ", 0.3, "Divide moles by volume.", phase="substitute"),
    box("Check: 0.3 × 0.5 = ", 0.15, "Multiply back to reach the moles.",
        phase="substitute", done="Back to 0.15 mol, so 0.3 mol/dm³ is right."),
]
setmc(B[4], 0, 0.0003)  # divided by 500 not 0.5

# B5: moles in 100 cm3 of 0.25 -> 0.025
B[5]["hint"] = "Convert 100 cm³ to dm³, then moles = concentration × volume."
B[5]["guided_steps"] = [
    sayonly("Moles = concentration × volume, with the volume in dm³."),
    box("Convert the volume: 100 ÷ 1000 = ", 0.1, "Divide cm³ by 1000."),
    box("moles = 0.25 × 0.1 = ", 0.025, "Multiply concentration by volume.", phase="substitute"),
    box("Check: 0.025 ÷ 0.1 = ", 0.25, "Divide back to reach the concentration.",
        phase="substitute", done="Back to the concentration, so 0.025 mol is right."),
]
setmc(B[5], 0, 25)  # used 100 not 0.1

# B6: convert 50 cm3 -> 0.05
B[6]["hint"] = "There are 1000 cm³ in 1 dm³, so divide by 1000."
B[6]["guided_steps"] = [
    sayonly("To convert cm³ to dm³, divide by 1000 (there are 1000 cm³ in 1 dm³)."),
    box("How many cm³ are in 1 dm³? ", 1000, "1 dm³ = 1 litre = 1000 cm³."),
    box("50 ÷ 1000 = ", 0.05, "Move the decimal three places to the left.", phase="substitute"),
    box("Check by reversing: 0.05 × 1000 = ", 50, "Multiply back to cm³.",
        phase="substitute", done="Back to 50 cm³, so 0.05 dm³ is right."),
]
setmc(B[6], 0, 0.5)  # divided by 100

# B7: moles = 2/36.5 -> 0.0548
B[7]["hint"] = "Mr of HCl = 1 + 35.5, then moles = mass ÷ Mr, to 3 s.f."
B[7]["guided_steps"] = [
    sayonly("Moles = mass ÷ Mr. Find the Mr of HCl first."),
    box("Mr of HCl = 1 + 35.5 = ", 36.5, "Add the Ar of H and Cl."),
    box("moles = 2.0 ÷ 36.5 = ", 0.0548, "Divide, then round to 3 significant figures.", phase="substitute"),
    box("Check: 0.0548 × 36.5 = ", 2, "Multiply back to reach the mass (about 2.0 g).",
        phase="substitute", done="Back to about 2.0 g, so 0.0548 mol is right."),
]
setmc(B[7], 0, None)

# ============================================================
# SILVER  (titration, one pass)
# ============================================================
S = pb["silver"]

# S0: 25 NaOH unknown, 20 cm3 0.125 HCl, 1:1 -> 0.1
S[0]["hint"] = "Moles of HCl, then 1:1 ratio, then divide by the NaOH volume."
S[0]["guided_steps"] = [
    sayonly("Method: moles of HCl (the one we know), then the ratio, then divide by the NaOH volume."),
    box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "cm³ ÷ 1000."),
    box("moles HCl = 0.125 × 0.02 = ", 0.0025, "concentration × volume."),
    box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000."),
    box("The ratio HCl : NaOH is 1 : 1, so moles NaOH = ", 0.0025,
        "Same as the moles of HCl.", phase="substitute"),
    box("concentration NaOH = 0.0025 ÷ 0.025 = ", 0.1, "moles ÷ volume in dm³.", phase="substitute"),
    box("Check: 0.1 × 0.025 = ", 0.0025, "Multiply back to reach the NaOH moles.",
        phase="substitute", done="That returns 0.0025 mol NaOH, so 0.1 mol/dm³ is right."),
]
setmc(S[0], 0, None)  # forgot to convert both cancels -> same answer
setmc(S[0], 1, 0.125)  # used HCl volume 0.02 in final step

# S1: 25 cm3 0.2 NaOH, 20 cm3 H2SO4, 1:2 -> 0.125
S[1]["hint"] = "Moles of NaOH, halve for the 2:1 ratio, then divide by the acid volume."
S[1]["guided_steps"] = [
    sayonly("Find moles of NaOH first, then use the 2:1 ratio, then divide by the H₂SO₄ volume."),
    box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000."),
    box("moles NaOH = 0.2 × 0.025 = ", 0.005, "concentration × volume."),
    box("Convert the acid volume: 20.0 ÷ 1000 = ", 0.02, "cm³ ÷ 1000."),
    box("2 moles NaOH react with 1 mole H₂SO₄, so moles H₂SO₄ = 0.005 ÷ 2 = ", 0.0025,
        "Halve the NaOH moles.", phase="substitute"),
    box("concentration = 0.0025 ÷ 0.02 = ", 0.125, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.125 × 0.02 × 2 = ", 0.005, "Reverse the steps back to the NaOH moles.",
        phase="substitute", done="That returns the 0.005 mol of NaOH, so 0.125 mol/dm³ is right."),
]
setmc(S[1], 0, 0.25)   # used 1:1 (ignored the 2)
setmc(S[1], 1, 0.5)    # doubled instead of halved
S[1]["misconceptions"][1]["message"] = (
    "One mole of H₂SO₄ reacts with two moles of NaOH, so you need HALF as many moles "
    "of acid: divide by 2, do not multiply. Doubling gives 0.5 mol/dm³, which is wrong.")

# S2: 25 cm3 0.15 HCl, 18.75 cm3 NaOH, 1:1 -> 0.2
S[2]["hint"] = "Moles of HCl, 1:1 ratio, then divide by the NaOH volume (18.75 cm³)."
S[2]["guided_steps"] = [
    sayonly("Moles of HCl first, ratio 1:1, then divide by the NaOH volume."),
    box("Convert the HCl volume: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000."),
    box("moles HCl = 0.15 × 0.025 = ", 0.00375, "concentration × volume."),
    box("Convert the NaOH volume: 18.75 ÷ 1000 = ", 0.01875, "cm³ ÷ 1000."),
    box("Ratio 1 : 1, so moles NaOH = ", 0.00375, "Same as the HCl moles.", phase="substitute"),
    box("concentration NaOH = 0.00375 ÷ 0.01875 = ", 0.2, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.2 × 0.01875 = ", 0.00375, "Multiply back to reach the NaOH moles.",
        phase="substitute", done="That returns 0.00375 mol NaOH, so 0.2 mol/dm³ is right."),
]
setmc(S[2], 0, 0.15)  # used HCl volume 0.025 in final division

# S3: CHANGED -> 0.15 Ca(OH)2, 25 cm3, Ca(OH)2+2HCl, 20 cm3 HCl -> 0.375
S[3]["display"] = ("25.0 cm³ of 0.15 mol/dm³ Ca(OH)₂ is neutralised by 20.0 cm³ of HCl. "
                   "The equation is: Ca(OH)₂ + 2HCl → CaCl₂ + 2H₂O. "
                   "Calculate the concentration of the HCl in mol/dm³.")
S[3]["solutions"] = [0.375]
S[3]["hint"] = "Moles of Ca(OH)₂, double for the 1:2 ratio, then divide by the HCl volume."
S[3]["guided_steps"] = [
    sayonly("Moles of Ca(OH)₂ first, then the 1:2 ratio (2 HCl per Ca(OH)₂), then divide by the HCl volume."),
    box("Convert the Ca(OH)₂ volume: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000."),
    box("moles Ca(OH)₂ = 0.15 × 0.025 = ", 0.00375, "concentration × volume."),
    box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "cm³ ÷ 1000."),
    box("1 Ca(OH)₂ gives 2 HCl, so moles HCl = 0.00375 × 2 = ", 0.0075,
        "Double the Ca(OH)₂ moles.", phase="substitute"),
    box("concentration HCl = 0.0075 ÷ 0.02 = ", 0.375, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.375 × 0.02 = ", 0.0075, "Multiply back to reach the HCl moles.",
        phase="substitute", done="That returns 0.0075 mol HCl; halving gives 0.00375 mol Ca(OH)₂, "
        "so 0.375 mol/dm³ is right."),
]
setmc(S[3], 0, 0.1875,
      "Ca(OH)₂ : HCl = 1 : 2. Moles Ca(OH)₂ = 0.15 × 0.025 = 0.00375. "
      "Moles HCl = 0.00375 × 2 = 0.0075. Conc = 0.0075 ÷ 0.02 = 0.375 mol/dm³.")
setmc(S[3], 1, None,
      "The equation shows 2 moles of HCl per mole of Ca(OH)₂, so double the moles.")

# S4: 25 cm3 0.2 KOH, 20 cm3 HNO3, 1:1 -> 0.25
S[4]["hint"] = "Moles of KOH, 1:1 ratio, then divide by the HNO₃ volume."
S[4]["guided_steps"] = [
    sayonly("Moles of KOH first, ratio 1:1, then divide by the HNO₃ volume."),
    box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000."),
    box("moles KOH = 0.2 × 0.025 = ", 0.005, "concentration × volume."),
    box("Convert the HNO₃ volume: 20.0 ÷ 1000 = ", 0.02, "cm³ ÷ 1000."),
    box("Ratio 1 : 1, so moles HNO₃ = ", 0.005, "Same as the KOH moles.", phase="substitute"),
    box("concentration HNO₃ = 0.005 ÷ 0.02 = ", 0.25, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.25 × 0.02 = ", 0.005, "Multiply back to reach the HNO₃ moles.",
        phase="substitute", done="That returns 0.005 mol, so 0.25 mol/dm³ is right."),
]
setmc(S[4], 0, 0.2)  # used KOH volume 0.025 in final division

# S5: CHANGED -> 25 cm3 0.5 KOH, H2SO4+2KOH, 12.5 cm3 H2SO4 -> 0.5
S[5]["display"] = ("25.0 cm³ of 0.5 mol/dm³ KOH is neutralised by 12.5 cm³ of H₂SO₄. "
                   "The equation is: H₂SO₄ + 2KOH → K₂SO₄ + 2H₂O. "
                   "Calculate the concentration of the H₂SO₄ in mol/dm³.")
S[5]["solutions"] = [0.5]
S[5]["hint"] = "Moles of KOH, halve for the 2:1 ratio, then divide by the acid volume (12.5 cm³)."
S[5]["guided_steps"] = [
    sayonly("Moles of KOH first, then the 2:1 ratio, then divide by the H₂SO₄ volume."),
    box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000."),
    box("moles KOH = 0.5 × 0.025 = ", 0.0125, "concentration × volume."),
    box("Convert the acid volume: 12.5 ÷ 1000 = ", 0.0125, "cm³ ÷ 1000."),
    box("2 KOH per H₂SO₄, so moles H₂SO₄ = 0.0125 ÷ 2 = ", 0.00625,
        "Halve the KOH moles.", phase="substitute"),
    box("concentration = 0.00625 ÷ 0.0125 = ", 0.5, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.5 × 0.0125 × 2 = ", 0.0125, "Reverse back to the KOH moles.",
        phase="substitute", done="That returns the 0.0125 mol of KOH, so 0.5 mol/dm³ is right."),
]
setmc(S[5], 0, 1.0,
      "H₂SO₄ : KOH = 1 : 2. Moles KOH = 0.5 × 0.025 = 0.0125. "
      "Moles H₂SO₄ = 0.0125 ÷ 2 = 0.00625. Conc = 0.00625 ÷ 0.0125 = 0.5 mol/dm³.")
setmc(S[5], 1, None,
      "Two moles of KOH react with one mole of H₂SO₄. Halve the moles of KOH.")

# ============================================================
# GOLD  (multi-step)
# ============================================================
G = pb["gold"]

# G0: 2.0 g NaOH Mr40 -> 200 cm3, 25 cm3, titre 31.25 cm3, 1:1 -> 0.2
G[0]["hint"] = "Flask concentration first, then sample moles, ratio, then divide by the titre."
G[0]["guided_steps"] = [
    sayonly("Get the flask concentration, take the sample moles, apply the ratio, then divide by the titre."),
    box("moles NaOH in the flask = 2.0 ÷ 40 = ", 0.05, "mass ÷ Mr."),
    box("Convert the flask volume: 200 ÷ 1000 = ", 0.2, "cm³ ÷ 1000."),
    box("concentration in the flask = 0.05 ÷ 0.2 = ", 0.25, "moles ÷ volume."),
    box("moles in the 25.0 cm³ sample = 0.25 × 0.025 = ", 0.00625, "concentration × 0.025 dm³."),
    box("Ratio NaOH : HCl is 1 : 1, so moles HCl = ", 0.00625, "Same as the NaOH moles.", phase="substitute"),
    box("Convert the titre: 31.25 ÷ 1000 = ", 0.03125, "cm³ ÷ 1000.", phase="substitute"),
    box("concentration HCl = 0.00625 ÷ 0.03125 = ", 0.2, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.2 × 0.03125 = ", 0.00625, "Multiply back to reach the HCl moles.",
        phase="substitute", done="That returns 0.00625 mol HCl, so 0.2 mol/dm³ is right."),
]
setmc(G[0], 0, None)
setmc(G[0], 1, 1.6)  # used 200 cm3 (0.2 dm3) as the sample volume

# G1: 5.3 g Na2CO3 -> 250 cm3, 25 cm3, titre 25 cm3, 1:2 -> 0.4
G[1]["hint"] = "Mass to moles to flask concentration, then sample, the 1:2 ratio, then the titre."
G[1]["guided_steps"] = [
    sayonly("Mass to moles to flask concentration, then sample, ratio, and titre."),
    box("Mr Na₂CO₃ = (2×23) + 12 + (3×16) = ", 106, "Two sodiums, one carbon, three oxygens."),
    box("moles in the flask = 5.3 ÷ 106 = ", 0.05, "mass ÷ Mr."),
    box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "cm³ ÷ 1000."),
    box("concentration in the flask = 0.05 ÷ 0.25 = ", 0.2, "moles ÷ volume."),
    box("moles in the 25.0 cm³ sample = 0.2 × 0.025 = ", 0.005, "concentration × 0.025 dm³."),
    box("Na₂CO₃ : HCl is 1 : 2, so moles HCl = 0.005 × 2 = ", 0.01, "Double it.", phase="substitute"),
    box("Convert the titre: 25.0 ÷ 1000 = ", 0.025, "cm³ ÷ 1000.", phase="substitute"),
    box("concentration HCl = 0.01 ÷ 0.025 = ", 0.4, "moles ÷ volume.", phase="substitute"),
    box("Check: 0.4 × 0.025 = ", 0.01, "Multiply back to reach the HCl moles.",
        phase="substitute", done="That returns 0.01 mol HCl, so 0.4 mol/dm³ is right."),
]
setmc(G[1], 0, None)
setmc(G[1], 1, 0.2)  # used 1:1 instead of 1:2

# G2: mass HCl for 250 cm3 of 0.5 -> 4.6 (accept 0.1)
G[2]["hint"] = "Moles from concentration × volume, then mass = moles × Mr, to 1 d.p."
G[2]["guided_steps"] = [
    sayonly("Find moles from concentration and volume, then turn moles into mass with the Mr."),
    box("Convert the volume: 250 ÷ 1000 = ", 0.25, "cm³ ÷ 1000."),
    box("moles = 0.5 × 0.25 = ", 0.125, "concentration × volume."),
    box("Mr HCl = 1 + 35.5 = ", 36.5, "Add the Ar values.", phase="substitute"),
    box("mass = 0.125 × 36.5 = ", 4.5625, "moles × Mr.", phase="substitute"),
    box("Round to 1 decimal place: 4.5625 → ", 4.6, "Second decimal is 6, so round up.", phase="substitute"),
    box("Check: 4.5625 ÷ 36.5 = ", 0.125, "Divide the mass back by the Mr to reach the moles.",
        phase="substitute", done="Back to 0.125 mol, so 4.6 g is right."),
]
setmc(G[2], 0, 4562.5,
      "You must convert 250 cm³ to 0.25 dm³ first. Using 250 gives moles = 0.5 × 250 = 125 "
      "and a mass of 4562.5 g, which is nonsense. Volume = 250 ÷ 1000 = 0.25 dm³.")
setmc(G[2], 1, None)

# G3: KOH -> 500 cm3, 25 cm3 vs 20 cm3 0.1 HCl, 1:1, mass KOH -> 2.24 (accept 0.01)
G[3]["hint"] = "Titre to moles, 1:1 ratio, scale up to the 500 cm³ flask, then mass."
G[3]["guided_steps"] = [
    sayonly("Work back from the titration to moles, up to the flask, then to mass."),
    box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "cm³ ÷ 1000."),
    box("moles HCl = 0.1 × 0.02 = ", 0.002, "concentration × volume."),
    box("1:1 ratio, so moles KOH in the 25.0 cm³ sample = ", 0.002, "Same as the HCl moles."),
    box("concentration KOH = 0.002 ÷ 0.025 = ", 0.08, "moles ÷ 0.025 dm³ gives the flask concentration."),
    box("The flask holds 500 cm³ = 0.5 dm³, so total moles KOH = 0.08 × 0.5 = ", 0.04,
        "concentration × 0.5.", phase="substitute"),
    box("Mr KOH = 39 + 16 + 1 = ", 56, "Add the Ar values.", phase="substitute"),
    box("mass = 0.04 × 56 = ", 2.24, "moles × Mr.", phase="substitute"),
    box("Check: 2.24 ÷ 56 = ", 0.04, "Divide the mass back by the Mr.",
        phase="substitute", done="Back to 0.04 mol, so 2.24 g is right."),
]
setmc(G[3], 0, None)
setmc(G[3], 1, 0.112,
      "The titration only uses 25.0 cm³ of a 500 cm³ flask. Find the concentration "
      "(0.08 mol/dm³), then scale up: total moles = 0.08 × 0.5 = 0.04 mol, mass = 2.24 g. "
      "Skipping the scale-up gives just 0.112 g.")

# G4: NaOH -> 250 cm3, 25 cm3 vs 20 cm3 0.2 HNO3, 1:1, mass NaOH -> 1.6
G[4]["hint"] = "Titre to moles, 1:1 ratio, scale up to the 250 cm³ flask, then mass."
G[4]["guided_steps"] = [
    sayonly("From the titre to moles, to the flask total, to the mass."),
    box("Convert the HNO₃ volume: 20.0 ÷ 1000 = ", 0.02, "cm³ ÷ 1000."),
    box("moles HNO₃ = 0.2 × 0.02 = ", 0.004, "concentration × volume."),
    box("1:1 ratio, so moles NaOH in the 25.0 cm³ sample = ", 0.004, "Same as the HNO₃ moles."),
    box("concentration NaOH = 0.004 ÷ 0.025 = ", 0.16, "moles ÷ 0.025 dm³."),
    box("The flask holds 250 cm³ = 0.25 dm³, so total moles = 0.16 × 0.25 = ", 0.04,
        "concentration × 0.25.", phase="substitute"),
    box("Mr NaOH = 23 + 16 + 1 = ", 40, "Add the Ar values.", phase="substitute"),
    box("mass = 0.04 × 40 = ", 1.6, "moles × Mr.", phase="substitute"),
    box("Check: 1.6 ÷ 40 = ", 0.04, "Divide the mass back by the Mr.",
        phase="substitute", done="Back to 0.04 mol, so 1.6 g is right."),
]
setmc(G[4], 0, None)
setmc(G[4], 1, 0.16,
      "You titrated 25.0 cm³ from a 250 cm³ flask, so scale up by 10: total moles = "
      "conc × 0.25 = 0.04 mol, mass = 1.6 g. Using only the sample moles gives just 0.16 g.")

# G5: Na2CO3 -> 500 cm3, 25 cm3 vs 12.5 cm3 0.1 H2SO4, 1:1, mass -> 2.65 (accept 0.01)
G[5]["hint"] = "Titre to moles, 1:1 ratio, scale up to the 500 cm³ flask, then mass with the Mr."
G[5]["guided_steps"] = [
    sayonly("Titre to moles, ratio, flask total, then mass with the Mr."),
    box("Convert the H₂SO₄ volume: 12.5 ÷ 1000 = ", 0.0125, "cm³ ÷ 1000."),
    box("moles H₂SO₄ = 0.1 × 0.0125 = ", 0.00125, "concentration × volume."),
    box("Na₂CO₃ : H₂SO₄ is 1 : 1, so moles Na₂CO₃ in the sample = ", 0.00125, "Same as the acid moles."),
    box("concentration Na₂CO₃ = 0.00125 ÷ 0.025 = ", 0.05, "moles ÷ 0.025 dm³."),
    box("The flask holds 500 cm³ = 0.5 dm³, so total moles = 0.05 × 0.5 = ", 0.025,
        "concentration × 0.5.", phase="substitute"),
    box("Mr Na₂CO₃ = (2×23) + 12 + (3×16) = ", 106, "Two sodiums, one carbon, three oxygens.", phase="substitute"),
    box("mass = 0.025 × 106 = ", 2.65, "moles × Mr.", phase="substitute"),
    box("Check: 2.65 ÷ 106 = ", 0.025, "Divide the mass back by the Mr.",
        phase="substitute", done="Back to 0.025 mol, so 2.65 g is right."),
]
setmc(G[5], 0, 0.1325,
      "You titrated 25.0 cm³ from a 500 cm³ flask. Scale up: concentration = 0.05 mol/dm³, "
      "total moles = 0.05 × 0.5 = 0.025 mol, Mr = 106, mass = 2.65 g. Using only the sample "
      "moles gives just 0.1325 g.")
setmc(G[5], 1, None)

# ============================================================
# tier_guides
# ============================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one formula, one step",
        "steps": [
            "<strong>Pick the formula</strong> that links what you know to what you want: "
            "moles = concentration × volume, concentration = moles ÷ volume, or moles = mass ÷ Mr.",
            "<strong>Convert the volume to dm³ first</strong> by dividing cm³ by 1000. "
            "This is where most marks are lost.",
            "Substitute your numbers, work it out, and state the unit: mol, mol/dm³, or dm³.",
        ],
        "example": {
            "question": "Calculate the moles in 40 cm³ of a 0.2 mol/dm³ solution.",
            "steps": [
                {"label": "Convert the volume", "content": "<p>40 ÷ 1000 = 0.04 dm³</p>"},
                {"label": "Substitute", "content": "<p>moles = 0.2 × 0.04 = 0.008 mol</p>"},
                {"label": "Check", "content": "<p>0.008 ÷ 0.04 = 0.2 mol/dm³, the concentration we started with</p>"},
                {"label": "Answer", "content": "<p><strong>0.008 mol</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: one titration, one ratio",
        "steps": [
            "<strong>Find the moles of the solution you fully know</strong> (concentration × volume in dm³).",
            "<strong>Use the balanced equation's ratio</strong> to turn those moles into moles of the "
            "other substance. The ratio is not always 1:1.",
            "Divide by the other solution's volume in dm³ to get its concentration.",
        ],
        "example": {
            "question": "25.0 cm³ of 0.1 mol/dm³ HCl neutralises 20.0 cm³ of NaOH (1:1). Find the NaOH concentration.",
            "steps": [
                {"label": "Moles of HCl", "content": "<p>0.1 × 0.025 = 0.0025 mol</p>"},
                {"label": "Ratio", "content": "<p>1 : 1, so moles NaOH = 0.0025 mol</p>"},
                {"label": "Concentration", "content": "<p>0.0025 ÷ 0.02 = 0.125 mol/dm³</p>"},
                {"label": "Check", "content": "<p>0.125 × 0.02 = 0.0025 mol NaOH, matches</p>"},
                {"label": "Answer", "content": "<p><strong>0.125 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain the steps",
        "steps": [
            "<strong>Work in stages.</strong> If you are given a mass, turn it into moles with "
            "moles = mass ÷ Mr first.",
            "A sample is often taken from a larger flask. The concentration is the same throughout, "
            "so <strong>scale the moles up</strong> to the whole flask at the end.",
            "Chain the steps (moles, ratio, concentration or mass) and track the unit on every line.",
        ],
        "example": {
            "question": "2.0 g of NaOH (Mr = 40) is made up to 200 cm³. Find the concentration in the flask.",
            "steps": [
                {"label": "Moles", "content": "<p>2.0 ÷ 40 = 0.05 mol</p>"},
                {"label": "Convert the volume", "content": "<p>200 ÷ 1000 = 0.2 dm³</p>"},
                {"label": "Concentration", "content": "<p>0.05 ÷ 0.2 = 0.25 mol/dm³</p>"},
                {"label": "Check", "content": "<p>0.25 × 0.2 = 0.05 mol, matches</p>"},
                {"label": "Answer", "content": "<p><strong>0.25 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ============================================================
# guided: opener + teach
# ============================================================
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "6 spoons of powder → 2 litres of squash<br>6 spoons of powder → 3 litres of squash",
        "steps": [
            {"say": "Picture making orange squash. You stir 6 spoons of powder into 2 litres of water and taste it.",
             "pre": "How many spoons are in each litre? 6 ÷ 2 = ", "post": "", "answer": 3,
             "hint": "Share the 6 spoons across the 2 litres."},
            {"say": "Now the same 6 spoons go into 3 litres instead, so it tastes weaker.",
             "pre": "Spoons per litre now? 6 ÷ 3 = ", "post": "", "answer": 2,
             "hint": "Share 6 spoons across 3 litres."},
            {"say": r"That 'per litre' number is <strong>concentration</strong>: amount ÷ volume. In "
                    r"chemistry the spoons become <strong>moles</strong> and the volume is in dm³ (litres), "
                    r"so \(c = \dfrac{n}{V}\). Same sum, chemistry words."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Calculate the number of moles in 250 cm³ of a 0.40 mol/dm³ solution, then find the moles in 500 cm³ of the same solution.",
            "label": "Together: your first one",
            "steps": [
                {"say": "The formula is moles = concentration × volume, with the volume in dm³.",
                 "pre": "First convert the volume: 250 ÷ 1000 = ", "post": "", "answer": 0.25,
                 "hint": "Divide cm³ by 1000."},
                {"pre": "moles = 0.40 × 0.25 = ", "post": "", "answer": 0.1,
                 "hint": "Multiply concentration by volume."},
                {"pre": "Check by reversing: 0.1 ÷ 0.25 = ", "post": "", "answer": 0.4,
                 "done": "That is the concentration we started with, so 0.1 mol is right.",
                 "hint": "Divide moles by volume to get the concentration back."},
                {"say": "Now the same solution fills a 500 cm³ beaker.",
                 "pre": "Convert: 500 ÷ 1000 = ", "post": "", "answer": 0.5,
                 "hint": "Divide cm³ by 1000."},
                {"pre": "moles = 0.40 × 0.5 = ", "post": "", "answer": 0.2,
                 "done": "Twice the volume, twice the moles.",
                 "hint": "Multiply concentration by volume."},
            ],
        },
        "silver": {
            "display": "24.0 cm³ of 0.050 mol/dm³ H₂SO₄ neutralises 20.0 cm³ of NaOH. H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O. Find the concentration of the NaOH.",
            "label": "Together: the ratio move",
            "steps": [
                {"say": "Find the moles of the acid first. Watch the ratio, it is not 1:1 here.",
                 "pre": "Convert the acid volume: 24.0 ÷ 1000 = ", "post": "", "answer": 0.024,
                 "hint": "Divide cm³ by 1000."},
                {"pre": "moles H₂SO₄ = 0.050 × 0.024 = ", "post": "", "answer": 0.0012,
                 "hint": "concentration × volume."},
                {"say": "1 mole of H₂SO₄ reacts with 2 moles of NaOH.",
                 "pre": "moles NaOH = 0.0012 × 2 = ", "post": "", "answer": 0.0024,
                 "done": "That doubling is the whole point of the ratio.",
                 "hint": "Double the acid moles."},
                {"pre": "Convert the NaOH volume: 20.0 ÷ 1000 = ", "post": "", "answer": 0.02,
                 "hint": "Divide cm³ by 1000."},
                {"pre": "concentration NaOH = 0.0024 ÷ 0.02 = ", "post": "", "answer": 0.12,
                 "hint": "moles ÷ volume."},
                {"pre": "Check: 0.12 × 0.02 = ", "post": "", "answer": 0.0024,
                 "done": "That returns the 0.0024 mol of NaOH, so 0.12 mol/dm³ is right.",
                 "hint": "Multiply back to reach the NaOH moles."},
            ],
        },
        "gold": {
            "display": "3.7 g of Ca(OH)₂ (Mr = 74) is made up to 250 cm³. A 25.0 cm³ sample is titrated with 0.10 mol/dm³ HCl. Ca(OH)₂ + 2HCl → CaCl₂ + 2H₂O. Find the titre volume of HCl in cm³.",
            "label": "Together: the whole chain",
            "steps": [
                {"say": "This has everything: a mass, a flask, a sample, and a ratio. Take it one line at a time.",
                 "pre": "moles Ca(OH)₂ in the flask = 3.7 ÷ 74 = ", "post": "", "answer": 0.05,
                 "hint": "mass ÷ Mr."},
                {"pre": "Convert the flask volume: 250 ÷ 1000 = ", "post": "", "answer": 0.25,
                 "hint": "Divide cm³ by 1000."},
                {"pre": "concentration in the flask = 0.05 ÷ 0.25 = ", "post": "", "answer": 0.2,
                 "hint": "moles ÷ volume."},
                {"say": "The 25.0 cm³ sample is 0.025 dm³.",
                 "pre": "moles Ca(OH)₂ in the sample = 0.2 × 0.025 = ", "post": "", "answer": 0.005,
                 "hint": "concentration × volume."},
                {"pre": "1 Ca(OH)₂ gives 2 HCl, so moles HCl = 0.005 × 2 = ", "post": "", "answer": 0.01,
                 "done": "Doubled by the ratio.", "hint": "Double the Ca(OH)₂ moles."},
                {"pre": "volume HCl = 0.01 ÷ 0.10 = ", "post": "", "answer": 0.1,
                 "hint": "moles ÷ concentration gives the volume in dm³."},
                {"pre": "Convert to cm³: 0.1 × 1000 = ", "post": "", "answer": 100,
                 "done": "So the titre is 100 cm³.", "hint": "Multiply dm³ by 1000."},
            ],
        },
    },
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("WROTE", OUT)
