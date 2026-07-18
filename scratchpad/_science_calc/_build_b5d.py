# -*- coding: utf-8 -*-
"""Build guided practice_data for higher-calculations-L01@b5d94e42c2 (OCR titrations)."""
import json, io

SRC = "_b5d_live.json"
OUT = "lesson_higher-calculations-L01@b5d94e42c2.json"

pd = json.load(io.open(SRC, encoding="utf-8"))


def box(pre, answer, hint, say=None, done=None, phase=False):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    d["post"] = ""
    d["answer"] = answer
    d["hint"] = hint
    if done is not None:
        d["done"] = done
    if phase:
        d["phase"] = "substitute"
    return d


def sayp(text, phase=False):
    d = {"say": text}
    if phase:
        d["phase"] = "substitute"
    return d


# ---------------------------------------------------------------------------
# 1. Em-dash repair on preserved fields (validator forbids em dashes)
# ---------------------------------------------------------------------------
mc = pd["method_card"]
mc["content"] = mc["content"].replace(" — ", ", ").replace("—", ", ")
pd["exam_context"]["frequency"] = pd["exam_context"]["frequency"].replace(" — ", ": ").replace("—", ": ")
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ": ")

# ---------------------------------------------------------------------------
# 2. Tier descriptions
# ---------------------------------------------------------------------------
pb = pd["problem_bank"]
pb["bronze_description"] = "One equation, values ready to use: convert the volume to dm³, then substitute once."
pb["silver_description"] = "One titration: find the known moles, apply the mole ratio, then the unknown concentration."
pb["gold_description"] = "Several steps chained: a mass at one end, and a flask larger than the sample titrated."

# ---------------------------------------------------------------------------
# 3. Helpers to attach hint / expect / guided_steps by tier+index
# ---------------------------------------------------------------------------
bronze = pb["bronze"]
silver = pb["silver"]
gold = pb["gold"]

# --- hints (plain text, one sentence each) ---
bronze_hints = [
    "Convert 25 cm³ to dm³, then use n = c × V.",
    "Divide the moles by the volume.",
    "Rearrange to volume = moles ÷ concentration.",
    "Find the Mr, then divide the mass by it.",
    "Turn 500 cm³ into dm³ first, then divide moles by volume.",
    "Convert 100 cm³ to dm³, then multiply by the concentration.",
    "Divide by 1000, because 1 dm³ = 1000 cm³.",
    "Add the Ar values for Mr, then divide the mass by it.",
]
silver_hints = [
    "Find the HCl moles, then divide by the NaOH volume in dm³.",
    "Find the NaOH moles, halve for the 1:2 ratio, then divide by the acid volume.",
    "Find the HCl moles, then divide by the NaOH volume (18.75 cm³).",
    "Find the Ca(OH)₂ moles, double for the 1:2 ratio, then divide by the HCl volume.",
    "Find the KOH moles, then divide by the HNO₃ volume in dm³.",
    "Find the KOH moles, halve for the 1:2 ratio, then divide by the acid volume.",
]
gold_hints = [
    "Mass to moles to flask concentration, then the 25 cm³ sample and the 1:1 ratio.",
    "Find the flask concentration, take the sample moles, then double for the 1:2 ratio.",
    "Find the moles first, then mass = moles × Mr.",
    "Work back from the titration, then scale the sample concentration up to 500 cm³.",
    "Work back from the titration, then scale up to the 250 cm³ flask.",
    "Work back from the titration, then scale up to the 500 cm³ flask before finding the mass.",
]
for p, h in zip(bronze, bronze_hints):
    p["hint"] = h
for p, h in zip(silver, silver_hints):
    p["hint"] = h
for p, h in zip(gold, gold_hints):
    p["hint"] = h

# --- expects (add expect key to every misconception) ---
# bronze
bronze[0]["misconceptions"][0]["expect"] = 2.5      # unit_error: 0.1 x 25
bronze[1]["misconceptions"][0]["expect"] = 0.125    # inverse: 0.5 x 0.25
bronze[2]["misconceptions"][0]["expect"] = 2.5      # inverse: 0.5 / 0.2
bronze[3]["misconceptions"][0]["expect"] = None     # wrong_Mr indeterminate
bronze[4]["misconceptions"][0]["expect"] = 0.0003   # unit_error: 0.15 / 500
bronze[5]["misconceptions"][0]["expect"] = 25       # unit_error: 0.25 x 100
bronze[6]["misconceptions"][0]["expect"] = 0.5      # wrong_factor: /100
bronze[7]["misconceptions"][0]["expect"] = None     # wrong_Mr indeterminate
# silver
silver[0]["misconceptions"][0]["expect"] = None     # forgot_convert cancels -> same answer
silver[0]["misconceptions"][1]["expect"] = 0.125    # wrong_volume: /0.02
silver[1]["misconceptions"][0]["expect"] = 0.25     # mole_ratio: skip /2
silver[2]["misconceptions"][0]["expect"] = 0.15     # wrong_volume: /0.025
silver[3]["misconceptions"][0]["expect"] = 0.125    # mole_ratio: skip x2
# silver[4], silver[5] rebuilt below
# gold
gold[0]["misconceptions"][0]["expect"] = None       # forgot_step vague
gold[0]["misconceptions"][1]["expect"] = 1.6        # wrong_volume: use 200 cm3 as sample
gold[1]["misconceptions"][0]["expect"] = None       # wrong_Mr indeterminate
gold[1]["misconceptions"][1]["expect"] = 0.2        # mole_ratio: skip x2
gold[2]["misconceptions"][0]["expect"] = 4562.5     # forgot_convert: V=250
gold[3]["misconceptions"][0]["expect"] = None       # forgot_step vague
gold[3]["misconceptions"][1]["expect"] = 0.112      # scale_error: sample moles only
gold[4]["misconceptions"][0]["expect"] = 0.16       # scale_error: sample moles only
gold[5]["misconceptions"][0]["expect"] = 0.1325     # forgot_step: no flask scale-up

# ---------------------------------------------------------------------------
# 4. Repair silver duplicate answers (S4 -> 0.4, S5 -> 0.5)
# ---------------------------------------------------------------------------
silver[4]["display"] = ("25.0 cm³ of 0.2 mol/dm³ KOH is neutralised by 12.5 cm³ of HNO₃. "
                        "The equation is: KOH + HNO₃ → KNO₃ + H₂O. Calculate the concentration "
                        "of the HNO₃ in mol/dm³.")
silver[4]["solutions"] = [0.4]
silver[4]["misconceptions"] = [{
    "check": "common",
    "pattern": "wrong_volume",
    "expect": 0.2,
    "message": ("Moles KOH = 0.2 × 0.025 = 0.005. Ratio 1:1, so moles HNO₃ = 0.005. Use the HNO₃ "
                "volume (12.5 cm³ = 0.0125 dm³): conc = 0.005 ÷ 0.0125 = 0.4 mol/dm³. Dividing by "
                "the KOH volume by mistake gives 0.2."),
}]

silver[5]["display"] = ("25.0 cm³ of 0.5 mol/dm³ KOH is neutralised by 12.5 cm³ of H₂SO₄. "
                        "The equation is: H₂SO₄ + 2KOH → K₂SO₄ + 2H₂O. Calculate the concentration "
                        "of the H₂SO₄ in mol/dm³.")
silver[5]["solutions"] = [0.5]
silver[5]["misconceptions"] = [{
    "check": "common",
    "pattern": "mole_ratio",
    "expect": 1.0,
    "message": ("H₂SO₄ : KOH = 1 : 2. Moles KOH = 0.5 × 0.025 = 0.0125. Moles H₂SO₄ = 0.0125 ÷ 2 "
                "= 0.00625. Conc = 0.00625 ÷ 0.0125 = 0.5 mol/dm³. Forgetting to halve gives 1.0."),
}]

# ---------------------------------------------------------------------------
# 5. guided_steps per problem
# ---------------------------------------------------------------------------
CONV = "cm³ ÷ 1000."

bronze[0]["guided_steps"] = [
    sayp("The equation is \\(n = c \\times V\\). It needs the volume in dm³, but you are given cm³."),
    box("First convert the volume: 25.0 ÷ 1000 = ", 0.025, "Divide cm³ by 1000."),
    sayp("Now substitute the concentration and this volume.", phase=True),
    box("n = 0.1 × 0.025 = ", 0.0025, "Multiply the two numbers.", phase=True),
    box("Check by reversing it: 0.0025 ÷ 0.025 = ", 0.1,
        "Dividing moles by volume returns the concentration.",
        done="Back to 0.1 mol/dm³, so 0.0025 mol is right.", phase=True),
]

bronze[1]["guided_steps"] = [
    sayp("The equation is \\(c = n \\div V\\). The volume is already in dm³, so no conversion is needed."),
    box("Units check, write the volume in dm³: V = ", 0.25, "It is already in dm³, just write it."),
    sayp("Substitute into \\(c = n \\div V\\).", phase=True),
    box("c = 0.5 ÷ 0.25 = ", 2.0, "Divide moles by volume.", phase=True),
    box("Check: 2 × 0.25 = ", 0.5,
        "Concentration times volume should return the moles.",
        done="Back to the 0.5 mol we started with, so 2 mol/dm³ is right.", phase=True),
]

bronze[2]["guided_steps"] = [
    sayp("Rearrange \\(n = c \\times V\\) to \\(V = n \\div c\\). The values are ready to use."),
    box("Write the moles you need to fit in: n = ", 0.2, "Just write the moles given."),
    sayp("Substitute into \\(V = n \\div c\\).", phase=True),
    box("V = 0.2 ÷ 0.5 = ", 0.4, "Divide moles by concentration.", phase=True),
    box("Check: 0.4 × 0.5 = ", 0.2,
        "Volume times concentration should return the moles.",
        done="Back to 0.2 mol, so 0.4 dm³ is right.", phase=True),
]

bronze[3]["guided_steps"] = [
    sayp("The equation is \\(n = \\text{mass} \\div M_r\\). First find the \\(M_r\\) of NaOH."),
    box("Mr = 23 + 16 + 1 = ", 40, "Add the Ar values: Na 23, O 16, H 1."),
    sayp("Substitute the mass and the Mr.", phase=True),
    box("n = 4.0 ÷ 40 = ", 0.1, "Divide mass by Mr.", phase=True),
    box("Check: 0.1 × 40 = ", 4.0,
        "Moles times Mr should return the mass.",
        done="Back to 4.0 g, so 0.1 mol is right.", phase=True),
]

bronze[4]["guided_steps"] = [
    sayp("The equation is \\(c = n \\div V\\), with V in dm³. The 500 is in cm³."),
    box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide cm³ by 1000."),
    sayp("Substitute the moles and this volume.", phase=True),
    box("c = 0.15 ÷ 0.5 = ", 0.3, "Divide moles by volume.", phase=True),
    box("Check: 0.3 × 0.5 = ", 0.15,
        "Concentration times volume should return the moles.",
        done="Back to 0.15 mol, so 0.3 mol/dm³ is right.", phase=True),
]

bronze[5]["guided_steps"] = [
    sayp("The equation is \\(n = c \\times V\\), with V in dm³. Convert the 100 cm³ first."),
    box("Convert the volume: 100 ÷ 1000 = ", 0.1, "Divide cm³ by 1000."),
    sayp("Substitute the concentration and this volume.", phase=True),
    box("n = 0.25 × 0.1 = ", 0.025, "Multiply the two numbers.", phase=True),
    box("Check: 0.025 ÷ 0.1 = ", 0.25,
        "Moles divided by volume returns the concentration.",
        done="Back to 0.25 mol/dm³, so 0.025 mol is right.", phase=True),
]

bronze[6]["guided_steps"] = [
    sayp("To go from cm³ to dm³ you divide by 1000, because a litre (1 dm³) is 1000 cm³."),
    box("How many cm³ are in 1 dm³? ", 1000, "1 dm³ = 1000 cm³ (a litre)."),
    sayp("So divide the volume by that number.", phase=True),
    box("50 ÷ 1000 = ", 0.05, "Move the decimal point three places to the left.", phase=True),
    box("Check: 0.05 × 1000 = ", 50,
        "Multiplying back by 1000 should return the cm³.",
        done="Back to 50 cm³, so 0.05 dm³ is right.", phase=True),
]

bronze[7]["guided_steps"] = [
    sayp("The equation is \\(n = \\text{mass} \\div M_r\\). Find the Mr of HCl, then round the answer to 3 significant figures."),
    box("Mr of HCl = 1 + 35.5 = ", 36.5, "Add the Ar values: H 1, Cl 35.5."),
    sayp("Substitute the mass and the Mr.", phase=True),
    box("n = 2.0 ÷ 36.5 = (to 3 s.f.) ", 0.0548, "Divide, then round to 3 significant figures.", phase=True),
    box("Check: 0.0548 × 36.5 = ", 2.0,
        "Moles times Mr should return about the mass.",
        done="About 2.0 g, so 0.0548 mol is right.", phase=True),
]

# --- silver ---
silver[0]["guided_steps"] = [
    sayp("Titration ritual: moles of the known, then the ratio, then the concentration of the unknown. The known here is the HCl."),
    box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, CONV),
    box("Moles HCl = 0.125 × 0.02 = ", 0.0025, "n = c × V."),
    sayp("The ratio HCl : NaOH is 1 : 1, so moles NaOH = moles HCl = 0.0025."),
    sayp("Now the unknown. Convert the NaOH volume, then divide.", phase=True),
    box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, CONV, phase=True),
    box("c = 0.0025 ÷ 0.025 = ", 0.1, "Moles ÷ volume.", phase=True),
    box("Check: 0.1 × 0.025 = ", 0.0025,
        "Concentration times volume returns the NaOH moles.",
        done="Back to the 0.0025 mol of NaOH, so 0.1 mol/dm³ is right.", phase=True),
]

silver[1]["guided_steps"] = [
    sayp("The known is NaOH. Find its moles, apply the ratio, then find the H₂SO₄ concentration."),
    box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, CONV),
    box("Moles NaOH = 0.2 × 0.025 = ", 0.005, "n = c × V."),
    sayp("The equation is H₂SO₄ + 2NaOH, ratio 1 : 2, so moles H₂SO₄ = moles NaOH ÷ 2."),
    sayp("Now find the H₂SO₄ concentration.", phase=True),
    box("Moles H₂SO₄ = 0.005 ÷ 2 = ", 0.0025, "Divide by 2 for the 1:2 ratio.", phase=True),
    box("Convert the H₂SO₄ volume: 20.0 ÷ 1000 = ", 0.02, CONV, phase=True),
    box("c = 0.0025 ÷ 0.02 = ", 0.125, "Moles ÷ volume.", phase=True),
    box("Check: 0.125 × 0.02 × 2 = ", 0.005,
        "Working back through the ratio should return the NaOH moles.",
        done="Back to the 0.005 mol of NaOH, so 0.125 mol/dm³ is right.", phase=True),
]

silver[2]["guided_steps"] = [
    sayp("The known is HCl. Moles, then the 1 : 1 ratio, then the NaOH concentration."),
    box("Convert the HCl volume: 25.0 ÷ 1000 = ", 0.025, CONV),
    box("Moles HCl = 0.15 × 0.025 = ", 0.00375, "n = c × V."),
    sayp("Ratio 1 : 1, so moles NaOH = 0.00375."),
    sayp("Find the NaOH concentration. Use the NaOH volume, 18.75 cm³.", phase=True),
    box("Convert the NaOH volume: 18.75 ÷ 1000 = ", 0.01875, CONV, phase=True),
    box("c = 0.00375 ÷ 0.01875 = ", 0.2, "Moles ÷ volume.", phase=True),
    box("Check: 0.2 × 0.01875 = ", 0.00375,
        "Concentration times volume returns the NaOH moles.",
        done="Back to 0.00375 mol, so 0.2 mol/dm³ is right.", phase=True),
]

silver[3]["guided_steps"] = [
    sayp("The known is Ca(OH)₂. Moles, then the ratio, then the HCl concentration."),
    box("Convert the Ca(OH)₂ volume: 25.0 ÷ 1000 = ", 0.025, CONV),
    box("Moles Ca(OH)₂ = 0.1 × 0.025 = ", 0.0025, "n = c × V."),
    sayp("Ca(OH)₂ + 2HCl, ratio 1 : 2, so moles HCl = moles Ca(OH)₂ × 2."),
    sayp("Now find the HCl concentration.", phase=True),
    box("Moles HCl = 0.0025 × 2 = ", 0.005, "Double it for the 1:2 ratio.", phase=True),
    box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, CONV, phase=True),
    box("c = 0.005 ÷ 0.02 = ", 0.25, "Moles ÷ volume.", phase=True),
    box("Check: 0.25 × 0.02 = ", 0.005,
        "Concentration times volume returns the HCl moles.",
        done="Back to the 0.005 mol of HCl, so 0.25 mol/dm³ is right.", phase=True),
]

silver[4]["guided_steps"] = [
    sayp("The known is KOH. Moles, then the 1 : 1 ratio, then the HNO₃ concentration."),
    box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, CONV),
    box("Moles KOH = 0.2 × 0.025 = ", 0.005, "n = c × V."),
    sayp("Ratio 1 : 1, so moles HNO₃ = 0.005."),
    sayp("Find the HNO₃ concentration. Its volume is 12.5 cm³.", phase=True),
    box("Convert the HNO₃ volume: 12.5 ÷ 1000 = ", 0.0125, CONV, phase=True),
    box("c = 0.005 ÷ 0.0125 = ", 0.4, "Moles ÷ volume.", phase=True),
    box("Check: 0.4 × 0.0125 = ", 0.005,
        "Concentration times volume returns the HNO₃ moles.",
        done="Back to 0.005 mol, so 0.4 mol/dm³ is right.", phase=True),
]

silver[5]["guided_steps"] = [
    sayp("The known is KOH. Moles, then the 1 : 2 ratio, then the H₂SO₄ concentration."),
    box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, CONV),
    box("Moles KOH = 0.5 × 0.025 = ", 0.0125, "n = c × V."),
    sayp("H₂SO₄ + 2KOH, ratio 1 : 2, so moles H₂SO₄ = moles KOH ÷ 2."),
    sayp("Now find the H₂SO₄ concentration. Its volume is 12.5 cm³.", phase=True),
    box("Moles H₂SO₄ = 0.0125 ÷ 2 = ", 0.00625, "Halve it for the 1:2 ratio.", phase=True),
    box("Convert the H₂SO₄ volume: 12.5 ÷ 1000 = ", 0.0125, CONV, phase=True),
    box("c = 0.00625 ÷ 0.0125 = ", 0.5, "Moles ÷ volume.", phase=True),
    box("Check: 0.5 × 0.0125 × 2 = ", 0.0125,
        "Working back through the ratio should return the KOH moles.",
        done="Back to the 0.0125 mol of KOH, so 0.5 mol/dm³ is right.", phase=True),
]

# --- gold ---
gold[0]["guided_steps"] = [
    sayp("Big picture: mass to moles, to flask concentration, to the moles in the 25 cm³ sample, then the ratio, then the HCl concentration."),
    box("Moles NaOH = 2.0 ÷ 40 = ", 0.05, "n = mass ÷ Mr."),
    box("Flask volume in dm³ = 200 ÷ 1000 = ", 0.2, CONV),
    box("Flask concentration = 0.05 ÷ 0.2 = ", 0.25, "Moles ÷ volume."),
    sayp("That is the NaOH concentration. Only 25.0 cm³ of it is used in the titration."),
    sayp("Find the moles in the 25.0 cm³ sample, then the HCl concentration.", phase=True),
    box("Moles NaOH in the sample = 0.25 × 0.025 = ", 0.00625, "n = c × V, with V = 0.025 dm³.", phase=True),
    box("Ratio 1 : 1, so moles HCl = 0.00625. Titre in dm³ = 31.25 ÷ 1000 = ", 0.03125, CONV, phase=True),
    box("c = 0.00625 ÷ 0.03125 = ", 0.2, "Moles ÷ volume.", phase=True),
    box("Check: 0.2 × 0.03125 = ", 0.00625,
        "Concentration times titre volume returns the HCl moles.",
        done="Back to the 0.00625 mol, so 0.2 mol/dm³ is right.", phase=True),
]

gold[1]["guided_steps"] = [
    sayp("Mass to moles, to flask concentration, to the sample moles, then the 1 : 2 ratio, then the HCl concentration."),
    box("Mr of Na₂CO₃ = (2×23) + 12 + (3×16) = ", 106, "46 + 12 + 48."),
    box("Moles Na₂CO₃ = 5.3 ÷ 106 = ", 0.05, "n = mass ÷ Mr."),
    box("Flask concentration = 0.05 ÷ 0.25 = ", 0.2, "Moles ÷ 0.25 dm³ (250 cm³)."),
    sayp("Only 25.0 cm³ of the flask is titrated."),
    sayp("Sample moles, then the ratio, then the HCl concentration.", phase=True),
    box("Moles Na₂CO₃ in the sample = 0.2 × 0.025 = ", 0.005, "n = c × V.", phase=True),
    box("Na₂CO₃ : HCl is 1 : 2, so moles HCl = 0.005 × 2 = ", 0.01, "Double it for the 1:2 ratio.", phase=True),
    box("c = 0.01 ÷ 0.025 = ", 0.4, "Moles ÷ 0.025 dm³ (titre 25.0 cm³).", phase=True),
    box("Check: 0.4 × 0.025 ÷ 2 = ", 0.005,
        "Working back through the ratio should return the Na₂CO₃ moles.",
        done="Back to the 0.005 mol of Na₂CO₃, so 0.4 mol/dm³ is right.", phase=True),
]

gold[2]["guided_steps"] = [
    sayp("Work the moles first, then the mass. Use \\(n = c \\times V\\), then mass = n × Mr."),
    box("Convert the volume: 250 ÷ 1000 = ", 0.25, CONV),
    box("Moles = 0.5 × 0.25 = ", 0.125, "n = c × V."),
    box("Mr of HCl = 1 + 35.5 = ", 36.5, "H 1 + Cl 35.5."),
    sayp("Now the mass. mass = moles × Mr.", phase=True),
    box("mass = 0.125 × 36.5 = (to 1 d.p.) ", 4.6, "Multiply, then round to 1 decimal place.", phase=True),
    box("Check: 4.6 ÷ 36.5 = ", 0.126,
        "Dividing the mass by Mr should return about the moles, 0.125.",
        done="About 0.125 mol, so 4.6 g is right.", phase=True),
]

gold[3]["guided_steps"] = [
    sayp("Work back from the titration to the flask: titre moles, ratio, sample concentration, then scale up and find the mass."),
    box("Convert the titre: 20.0 ÷ 1000 = ", 0.02, CONV),
    box("Moles HCl = 0.1 × 0.02 = ", 0.002, "n = c × V."),
    box("Ratio 1 : 1, so moles KOH in the sample = 0.002. Sample concentration = 0.002 ÷ 0.025 = ", 0.08,
        "Moles ÷ 0.025 dm³ (25 cm³)."),
    sayp("That concentration fills the whole 500 cm³ flask."),
    sayp("Scale up to the flask, then find the mass.", phase=True),
    box("Total moles KOH = 0.08 × 0.5 = ", 0.04, "Concentration × 0.5 dm³ (500 cm³).", phase=True),
    box("Mr of KOH = 39 + 16 + 1 = ", 56, "K 39 + O 16 + H 1.", phase=True),
    box("mass = 0.04 × 56 = ", 2.24, "mass = moles × Mr.", phase=True),
    box("Check: 2.24 ÷ 56 = ", 0.04,
        "Dividing the mass by Mr should return the total moles.",
        done="Back to the 0.04 mol, so 2.24 g is right.", phase=True),
]

gold[4]["guided_steps"] = [
    sayp("Work back from the titration to the flask: titre moles, ratio, sample concentration, then scale up and find the mass."),
    box("Convert the titre: 20.0 ÷ 1000 = ", 0.02, CONV),
    box("Moles HNO₃ = 0.2 × 0.02 = ", 0.004, "n = c × V."),
    box("Ratio 1 : 1, so moles NaOH in the sample = 0.004. Sample concentration = 0.004 ÷ 0.025 = ", 0.16,
        "Moles ÷ 0.025 dm³ (25 cm³)."),
    sayp("That concentration fills the whole 250 cm³ flask."),
    sayp("Scale up to the flask, then find the mass.", phase=True),
    box("Total moles = 0.16 × 0.25 = ", 0.04, "Concentration × 0.25 dm³ (250 cm³).", phase=True),
    box("Mr of NaOH = 23 + 16 + 1 = ", 40, "Na 23 + O 16 + H 1.", phase=True),
    box("mass = 0.04 × 40 = ", 1.6, "mass = moles × Mr.", phase=True),
    box("Check: 1.6 ÷ 40 = ", 0.04,
        "Dividing the mass by Mr should return the total moles.",
        done="Back to 0.04 mol, so 1.6 g is right.", phase=True),
]

gold[5]["guided_steps"] = [
    sayp("Work back from the titration to the flask: titre moles, ratio, sample concentration, then scale up and find the mass."),
    box("Convert the titre: 12.5 ÷ 1000 = ", 0.0125, CONV),
    box("Moles H₂SO₄ = 0.1 × 0.0125 = ", 0.00125, "n = c × V."),
    box("Na₂CO₃ : H₂SO₄ is 1 : 1, so moles Na₂CO₃ in the sample = 0.00125. Sample concentration = 0.00125 ÷ 0.025 = ", 0.05,
        "Moles ÷ 0.025 dm³ (25 cm³)."),
    sayp("That concentration fills the whole 500 cm³ flask."),
    sayp("Scale up to the flask, then find the mass.", phase=True),
    box("Total moles = 0.05 × 0.5 = ", 0.025, "Concentration × 0.5 dm³ (500 cm³).", phase=True),
    box("Mr of Na₂CO₃ = (2×23) + 12 + (3×16) = ", 106, "46 + 12 + 48.", phase=True),
    box("mass = 0.025 × 106 = ", 2.65, "mass = moles × Mr.", phase=True),
    box("Check: 2.65 ÷ 106 = ", 0.025,
        "Dividing the mass by Mr should return the total moles.",
        done="Back to 0.025 mol, so 2.65 g is right.", phase=True),
]

# ---------------------------------------------------------------------------
# 6. tier_guides
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, one step",
        "steps": [
            "Every concentration question is built on \\(n = c \\times V\\): moles \\(n\\), concentration \\(c\\) in mol/dm³, volume \\(V\\) in dm³. Rearrange it for whatever is missing.",
            "Volumes are almost always given in cm³. Divide by 1000 to get dm³ before you substitute. This one habit saves the most marks.",
            "If you are given a mass, get moles first with \\(n = \\text{mass} \\div M_r\\).",
        ],
        "example": {
            "question": "Calculate the moles in 50 cm³ of a 0.2 mol/dm³ solution.",
            "steps": [
                {"label": "Convert", "content": "<p>50 ÷ 1000 = 0.05 dm³</p>"},
                {"label": "Substitute", "content": "<p>\\(n = 0.2 \\times 0.05\\)</p>"},
                {"label": "Check", "content": "<p>0.01 ÷ 0.05 = 0.2 mol/dm³ ✓</p>"},
                {"label": "Answer", "content": "<p><strong>0.01 mol</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: one titration, mind the ratio",
        "steps": [
            "A titration links two solutions. Start with the one you fully know (both concentration and volume) and find its moles with \\(n = c \\times V\\).",
            "Read the mole ratio from the balanced equation. If it is 1 : 2 the moles are not equal, so double or halve as the equation says.",
            "Divide the unknown's moles by the unknown's volume in dm³ to get its concentration.",
        ],
        "example": {
            "question": "20.0 cm³ of 0.1 mol/dm³ HCl neutralises 25.0 cm³ of NaOH (1 : 1). Find the NaOH concentration.",
            "steps": [
                {"label": "Known moles", "content": "<p>0.1 × 0.02 = 0.002 mol HCl</p>"},
                {"label": "Ratio", "content": "<p>1 : 1, so 0.002 mol NaOH</p>"},
                {"label": "Concentration", "content": "<p>0.002 ÷ 0.025</p>"},
                {"label": "Check", "content": "<p>0.08 × 0.025 = 0.002 mol ✓</p>"},
                {"label": "Answer", "content": "<p><strong>0.08 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain the steps, keep units straight",
        "steps": [
            "Gold questions add a step at each end: a mass to turn into moles first, or a mass to find at the finish, and a flask larger than the sample titrated.",
            "Only part of the flask is titrated. Find the sample's concentration, then scale to the whole flask with \\(n = c \\times V\\) using the full flask volume.",
            "Work in a fixed order and convert every volume to dm³ as you meet it. End with mass = moles × \\(M_r\\) when a mass is asked for.",
        ],
        "example": {
            "question": "5.3 g of Na₂CO₃ is made up to 250 cm³. 25.0 cm³ is titrated with 25.0 cm³ HCl (1 : 2). Find the HCl concentration.",
            "steps": [
                {"label": "Flask concentration", "content": "<p>5.3 ÷ 106 = 0.05 mol, ÷ 0.25 = 0.2 mol/dm³</p>"},
                {"label": "Sample moles", "content": "<p>0.2 × 0.025 = 0.005 mol</p>"},
                {"label": "Ratio", "content": "<p>1 : 2, so 0.01 mol HCl</p>"},
                {"label": "Concentration", "content": "<p>0.01 ÷ 0.025 = 0.4 mol/dm³ ✓</p>"},
                {"label": "Answer", "content": "<p><strong>0.4 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 7. guided (opener + teach)
# ---------------------------------------------------------------------------
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "A jug holds 2 spoonfuls of sugar dissolved in 1 litre of water.",
        "steps": [
            box("You pour out half the jug (½ a litre). How many spoonfuls of sugar are in that half? ",
                1, "Half the liquid carries half the sugar.",
                say="No chemistry yet, just common sense."),
            box("And the strength of the sugar water in that glass, in spoonfuls per litre? ",
                2, "Pouring some out does not make it weaker, it is the same water. Still 2 per litre.",
                say="You just did amount = concentration × volume: 2 spoonfuls per litre × ½ litre = 1 spoonful. Chemists call the amount <strong>moles</strong> and the strength <strong>concentration</strong>."),
            sayp("That is the whole idea of a titration: a small sample has the <strong>same concentration</strong> as the flask it came from, but fewer moles. Swap spoonfuls for moles and litres for dm³ and you have \\(n = c \\times V\\)."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Calculate the moles in 250 cm³ of a 0.4 mol/dm³ solution.",
            "label": "Together: your first one",
            "steps": [
                sayp("The equation is \\(n = c \\times V\\), with V in dm³. Convert first."),
                box("Convert the volume: 250 ÷ 1000 = ", 0.25, "Divide cm³ by 1000."),
                box("n = 0.4 × 0.25 = ", 0.1, "Multiply concentration by volume."),
                box("Same solution, but 500 cm³ this time (double the volume). Moles = ", 0.2,
                    "Double the volume means double the moles.",
                    say="A quick sense check on how moles scale:"),
                box("Check the first answer: 0.1 ÷ 0.25 = ", 0.4,
                    "Moles ÷ volume returns the concentration.",
                    done="Back to 0.4 mol/dm³, so 0.1 mol in 250 cm³ is right."),
            ],
        },
        "silver": {
            "display": "20.0 cm³ of 0.1 mol/dm³ HCl neutralises 25.0 cm³ of NaOH. HCl + NaOH → NaCl + H₂O. Find the NaOH concentration.",
            "label": "Together: the ratio move",
            "steps": [
                sayp("The known is HCl. Moles, then ratio, then the NaOH concentration. The new move is that the balanced equation links the two solutions."),
                box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "Divide cm³ by 1000."),
                box("Moles HCl = 0.1 × 0.02 = ", 0.002, "n = c × V."),
                sayp("Ratio 1 : 1, so moles NaOH = 0.002."),
                box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide cm³ by 1000."),
                box("c = 0.002 ÷ 0.025 = ", 0.08, "Moles ÷ volume."),
                box("Check: 0.08 × 0.025 = ", 0.002,
                    "Concentration times volume returns the NaOH moles.",
                    done="Back to 0.002 mol, the NaOH is 0.08 mol/dm³."),
            ],
        },
        "gold": {
            "display": "1.0 g of NaOH (Mr = 40) is made up to 250 cm³. 25.0 cm³ is titrated with HCl, titre 25.0 cm³. NaOH + HCl → NaCl + H₂O. Find the HCl concentration.",
            "label": "Together: the gold move",
            "steps": [
                sayp("The gold moves: a mass to convert at the start, and a flask larger than the sample."),
                box("Moles NaOH = 1.0 ÷ 40 = ", 0.025, "n = mass ÷ Mr."),
                box("Flask concentration = 0.025 ÷ 0.25 = ", 0.1, "Moles ÷ 0.25 dm³ (250 cm³)."),
                box("Moles in the 25.0 cm³ sample = 0.1 × 0.025 = ", 0.0025, "n = c × V."),
                sayp("Ratio 1 : 1, so moles HCl = 0.0025. The titre is 25.0 cm³ = 0.025 dm³."),
                box("c = 0.0025 ÷ 0.025 = ", 0.1, "Moles ÷ volume."),
                box("Check: 0.1 × 0.025 = ", 0.0025,
                    "Concentration times titre volume returns the HCl moles.",
                    done="Back to the 0.0025 mol, the HCl is 0.1 mol/dm³."),
            ],
        },
    },
}

# ---------------------------------------------------------------------------
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("written", OUT)
