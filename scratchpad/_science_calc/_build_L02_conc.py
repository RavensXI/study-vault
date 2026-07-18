# -*- coding: utf-8 -*-
import json, io

MIN = "−"  # unicode minus
pd = json.load(io.open("_fetched_canonical.json", encoding="utf-8"))["practice_data"]
pb = pd["problem_bank"]

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post: d["post"] = post
    if say is not None: d["say"] = say
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

pd["method_card"] = {
    "title": "Concentration and Titration",
    "steps": [
        "Convert every volume from cm³ to dm³ (divide by 1000).",
        "Find moles of the substance you know: n = c × V.",
        "Cross the balanced equation by its mole ratio to reach the unknown.",
        "Divide moles by volume for the concentration, and state the unit."
    ],
    "content": ("<p><strong>Concentration</strong> is how much solute sits in each dm³ of solution.</p>"
        "<ul><li>\\(c = \\dfrac{n}{V}\\) gives mol/dm³</li>"
        "<li>\\(c_g = \\dfrac{m}{V}\\) gives g/dm³</li>"
        "<li>\\(n = \\dfrac{m}{M_r}\\) turns mass into moles</li></ul>"
        "<p>Volume must be in <strong>dm³</strong>, so divide any cm³ figure by 1000 first. "
        "In a titration, find the moles you know, cross the balanced equation by its mole ratio, "
        "then divide by the other volume. Average the concordant titres and discard the rough one.</p>")
}

pd["exam_context"] = {
    "marks": "4–6 per calculation question",
    "paper": "Chemistry: Breadth and Depth papers",
    "frequency": "High: concentration and titration calculations appear in almost every Chemistry paper"
}

for ex in pd["worked_examples"]:
    for st in ex["steps"]:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pb["bronze_description"] = "One concentration formula, units fixed first, then a single divide or multiply"
pb["silver_description"] = "A titration: moles of the known, the mole ratio, then the unknown concentration"
pb["gold_description"] = "A multi-step chain: mass to moles or flask scaling, plus a non 1:1 ratio"

def setprob(tier, idx, hint, gs, misc=None, display=None, solutions=None):
    p = pb[tier][idx]
    p["hint"] = hint
    p["guided_steps"] = gs
    if display is not None: p["display"] = display
    if solutions is not None: p["solutions"] = solutions
    if misc is not None: p["misconceptions"] = misc

# ===== BRONZE =====
setprob("bronze", 0,
    "Convert cm³ to dm³, then divide moles by volume.",
    [sayonly("Concentration in mol/dm³ is \\(c = \\dfrac{n}{V}\\), and the volume must be in dm³."),
     box("Convert the volume: 250 ÷ 1000 = ", 0.25, "Divide cm³ by 1000.", post="dm³"),
     box("Divide moles by volume: 0.5 ÷ 0.25 = ", 2.0, "c = n ÷ V.", phase="substitute"),
     box("Check by multiplying back: 2.0 × 0.25 = ", 0.5, "c × V returns the moles.",
         done="That returns the 0.5 mol we started with, so 2.0 mol/dm³ is right.")],
    misc=[{"pattern":"unit_error","check":"common","expect":0.002,
           "message":"Convert 250 cm³ to 0.25 dm³ first. Then c = 0.5 ÷ 0.25 = 2.0 mol/dm³. Dividing by 250 gives 0.002, far too small."},
          {"pattern":"inverse_error","check":"common","expect":0.125,
           "message":"Concentration = moles ÷ volume, not moles × volume. 0.5 × 0.25 = 0.125 is the wrong way round."}])

setprob("bronze", 1,
    "Convert the volume to dm³, then multiply concentration by volume.",
    [sayonly("Moles from concentration and volume: \\(n = c \\times V\\), volume in dm³."),
     box("Convert the volume: 200 ÷ 1000 = ", 0.2, "Divide by 1000.", post="dm³"),
     box("Multiply: 0.25 × 0.2 = ", 0.05, "n = c × V.", phase="substitute"),
     box("Check: 0.05 ÷ 0.2 = ", 0.25, "Dividing moles by volume returns the concentration.",
         done="Back to 0.25 mol/dm³, so 0.05 mol is right.")],
    misc=[{"pattern":"unit_error","check":"common","expect":50,
           "message":"200 cm³ = 0.2 dm³. n = 0.25 × 0.2 = 0.05 mol. Using 200 gives 50, a thousand times too big."}])

setprob("bronze", 2,
    "Rearrange to volume = moles ÷ concentration.",
    [sayonly("Rearrange \\(c = \\dfrac{n}{V}\\) for volume: \\(V = \\dfrac{n}{c}\\)."),
     box("Read off the concentration: c = ", 0.4, "0.4 mol/dm³ is given."),
     box("Divide moles by concentration: 0.06 ÷ 0.4 = ", 0.15, "V = n ÷ c.", phase="substitute"),
     box("Check: 0.4 × 0.15 = ", 0.06, "c × V should give the moles back.",
         done="Returns 0.06 mol, so the volume is 0.15 dm³.")],
    misc=[{"pattern":"inverse_error","check":"common","expect":6.6667,
           "message":"Rearrange to V = n ÷ c = 0.06 ÷ 0.4 = 0.15 dm³. Dividing c by n (0.4 ÷ 0.06) is upside down."}])

setprob("bronze", 3,
    "For g/dm³ divide the mass by the volume in dm³.",
    [sayonly("For g/dm³ use mass directly: \\(c_g = \\dfrac{m}{V}\\), no moles needed."),
     box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide by 1000.", post="dm³"),
     box("Divide mass by volume: 3.65 ÷ 0.5 = ", 7.3, "c = m ÷ V.", phase="substitute"),
     box("Check: 7.3 × 0.5 = ", 3.65, "c × V returns the mass.",
         done="Returns 3.65 g, so 7.3 g/dm³ is right.")],
    misc=[{"pattern":"unit_error","check":"common","expect":0.0073,
           "message":"500 cm³ = 0.5 dm³. c = 3.65 ÷ 0.5 = 7.3 g/dm³. Dividing by 500 gives 0.0073, far too small."}])

setprob("bronze", 4,
    "Add the Ar values for the formula mass, then divide the mass by it.",
    [sayonly("Moles from mass: \\(n = \\dfrac{\\text{mass}}{M_r}\\)."),
     box("First the relative formula mass: 23 + 16 + 1 = ", 40, "Add the Ar values for Na, O and H."),
     box("Divide mass by Mr: 4.0 ÷ 40 = ", 0.1, "n = mass ÷ Mr.", phase="substitute"),
     box("Check: 0.1 × 40 = ", 4.0, "n × Mr returns the mass.",
         done="Returns 4.0 g, so 0.1 mol is right.")],
    misc=[{"pattern":"wrong_Mr","check":"common","expect":None,
           "message":"Mr of NaOH = 23 + 16 + 1 = 40. Then n = 4.0 ÷ 40 = 0.1 mol."}])

# bronze[5] originally 0.5 mol/dm3 -> 0.05 mol, a duplicate of bronze[1] (0.05).
# Minimal fix: change the concentration to 0.3 mol/dm3 so the answer (0.03) is unique.
setprob("bronze", 5,
    "Convert to dm³, then multiply concentration by volume.",
    [sayonly("Moles from concentration and volume: \\(n = c \\times V\\)."),
     box("Convert the volume: 100 ÷ 1000 = ", 0.1, "Divide by 1000.", post="dm³"),
     box("Multiply: 0.3 × 0.1 = ", 0.03, "n = c × V.", phase="substitute"),
     box("Check: 0.03 ÷ 0.1 = ", 0.3, "Divide moles by volume to check.",
         done="Back to 0.3 mol/dm³, so 0.03 mol is right.")],
    misc=[{"pattern":"unit_error","check":"common","expect":30,
           "message":"100 cm³ = 0.1 dm³. n = 0.3 × 0.1 = 0.03 mol. Using 100 gives 30."}],
    display="A solution has a concentration of 0.3 mol/dm³. How many moles are in 100 cm³?",
    solutions=[0.03])

setprob("bronze", 6,
    "There are 1000 cm³ in a dm³, so divide by 1000.",
    [sayonly("There are 1000 cm³ in 1 dm³, so dividing by 1000 converts cm³ to dm³."),
     box("How many cm³ make 1 dm³? ", 1000, "1 dm³ = 1000 cm³."),
     box("750 ÷ 1000 = ", 0.75, "Move the decimal point three places left.", phase="substitute"),
     box("Check: 0.75 × 1000 = ", 750, "Multiplying back returns the cm³.",
         done="Back to 750 cm³, so 0.75 dm³ is right.")],
    misc=[{"pattern":"wrong_factor","check":"common","expect":7.5,
           "message":"There are 1000 cm³ in a dm³, not 100. Divide by 1000: 750 ÷ 1000 = 0.75 dm³. Dividing by 100 gives 7.5, ten times too big."}])

setprob("bronze", 7,
    "Find the formula mass, then moles, then divide by the volume in dm³.",
    [sayonly("Two steps: mass to moles with \\(n = \\dfrac{m}{M_r}\\), then \\(c = \\dfrac{n}{V}\\)."),
     box("Relative formula mass: 23 + 35.5 = ", 58.5, "Add the Ar values for Na and Cl."),
     box("Moles: 5.85 ÷ 58.5 = ", 0.1, "n = mass ÷ Mr."),
     box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide by 1000.", post="dm³"),
     box("Concentration: 0.1 ÷ 0.5 = ", 0.2, "c = n ÷ V.", phase="substitute"),
     box("Check: 0.2 × 0.5 = ", 0.1, "c × V returns the moles.",
         done="Returns 0.1 mol, so 0.2 mol/dm³ is right.")],
    misc=[{"pattern":"wrong_Mr","check":"common","expect":None,
           "message":"Mr NaCl = 23 + 35.5 = 58.5. n = 5.85 ÷ 58.5 = 0.1 mol, then c = 0.1 ÷ 0.5 = 0.2 mol/dm³."}])

# ===== SILVER =====
setprob("silver", 0,
    "Find moles of NaOH, use the 1:1 ratio, then divide by the HCl volume.",
    [sayonly("Titration order: moles you know, then mole ratio, then the unknown concentration."),
     box("Convert the NaOH volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000.", post="dm³"),
     box("Moles of NaOH: 0.150 × 0.02 = ", 0.003, "n = c × V."),
     sayonly("The ratio HCl : NaOH is 1 : 1, so the moles of HCl are the same: 0.003 mol."),
     box("Convert the HCl volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³"),
     box("Concentration of HCl: 0.003 ÷ 0.025 = ", 0.12, "c = n ÷ V, using the HCl volume.", phase="substitute"),
     box("Check: 0.12 × 0.025 = ", 0.003, "c × V returns the moles of HCl.",
         done="Returns 0.003 mol HCl, matching the 1:1 ratio, so 0.12 mol/dm³ is right.")],
    misc=[{"pattern":"forgot_convert","check":"common","expect":None,
           "message":"Keep both volumes in dm³. n(NaOH) = 0.150 × 0.020 = 0.003 mol, then c(HCl) = 0.003 ÷ 0.025 = 0.12 mol/dm³."},
          {"pattern":"wrong_volume","check":"common","expect":0.15,
           "message":"Divide by the HCl volume (0.025 dm³) in the last step, not the NaOH volume. Using 0.020 gives 0.15, which is wrong."}])

setprob("silver", 1,
    "Double the calcium hydroxide moles for the 1:2 ratio before finding concentration.",
    [sayonly("Find moles of the calcium hydroxide, apply the 1 : 2 ratio, then divide by the acid volume."),
     box("Convert the Ca(OH)₂ volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³"),
     box("Moles of Ca(OH)₂: 0.100 × 0.025 = ", 0.0025, "n = c × V."),
     box("Ratio is 1 : 2, so moles of HCl: 0.0025 × 2 = ", 0.005, "Two HCl per Ca(OH)₂, so double."),
     box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000.", post="dm³"),
     box("Concentration of HCl: 0.005 ÷ 0.02 = ", 0.25, "c = n ÷ V.", phase="substitute"),
     box("Check: 0.25 × 0.02 = ", 0.005, "c × V returns the HCl moles.",
         done="Returns 0.005 mol HCl, so 0.25 mol/dm³ is right.")],
    misc=[{"pattern":"mole_ratio","check":"common","expect":0.125,
           "message":"The ratio is 1 : 2. n(Ca(OH)₂) = 0.0025 mol, so n(HCl) = 0.005 mol and c = 0.005 ÷ 0.020 = 0.25 mol/dm³. Forgetting to double gives 0.125."},
          {"pattern":"forgot_ratio","check":"common","expect":None,
           "message":"Two moles of HCl react with every one mole of Ca(OH)₂. Double the moles before finding concentration."}])

setprob("silver", 2,
    "Double the acid moles for the 1:2 ratio to get NaOH moles.",
    [sayonly("Moles of acid, then double for NaOH (1 : 2), then divide by the NaOH volume."),
     box("Convert the H₂SO₄ volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³"),
     box("Moles of H₂SO₄: 0.20 × 0.025 = ", 0.005, "n = c × V."),
     box("Ratio 1 : 2, so moles of NaOH: 0.005 × 2 = ", 0.01, "Two NaOH per H₂SO₄."),
     box("Convert the titre: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³"),
     box("Concentration of NaOH: 0.01 ÷ 0.025 = ", 0.4, "c = n ÷ V.", phase="substitute"),
     box("Check: 0.4 × 0.025 = ", 0.01, "c × V returns the NaOH moles.",
         done="Returns 0.01 mol NaOH, so 0.40 mol/dm³ is right.")],
    misc=[{"pattern":"mole_ratio","check":"common","expect":0.2,
           "message":"n(H₂SO₄) = 0.20 × 0.025 = 0.005 mol. NaOH needs double: 0.010 mol, so c = 0.010 ÷ 0.025 = 0.40 mol/dm³. Forgetting to double gives 0.2."},
          {"pattern":"forgot_ratio","check":"common","expect":None,
           "message":"Two moles of NaOH react with every one mole of H₂SO₄. Multiply the acid moles by 2."}])

setprob("silver", 3,
    "Average only the three concordant titres and discard the rough one.",
    [sayonly("Only concordant titres (within 0.10 cm³ of each other) go into the mean. The rough titre is discarded."),
     box("Add the three concordant titres: 24.80 + 24.85 + 24.75 = ", 74.4, "Add only the three close values."),
     box("Divide by 3: 74.4 ÷ 3 = ", 24.8, "Mean = total ÷ number of values.", phase="substitute"),
     box("Check the spread: 24.85 " + MIN + " 24.75 = ", 0.1, "Largest minus smallest of the three.",
         done="The three agree within 0.10 cm³, so the mean 24.80 cm³ is valid.")],
    misc=[{"pattern":"included_rough","check":"common","expect":24.925,
           "message":"The rough titre (25.30 cm³) is discarded. Mean = (24.80 + 24.85 + 24.75) ÷ 3 = 24.80 cm³. Including the rough gives 24.925."},
          {"pattern":"rounding","check":"common","expect":None,
           "message":"Keep two decimal places for burette readings to match the precision of the equipment."}])

setprob("silver", 4,
    "1:1 ratio, so use the KOH moles as the acid moles, then the acid volume.",
    [sayonly("1 : 1 ratio, so moles of acid equal moles of base. Find KOH moles, then divide by the acid volume."),
     box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³"),
     box("Moles of KOH: 0.08 × 0.025 = ", 0.002, "n = c × V."),
     sayonly("Ratio 1 : 1, so moles of HNO₃ = 0.002 mol."),
     box("Convert the titre: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000.", post="dm³"),
     box("Concentration of HNO₃: 0.002 ÷ 0.02 = ", 0.1, "c = n ÷ V.", phase="substitute"),
     box("Check: 0.1 × 0.02 = ", 0.002, "c × V returns the acid moles.",
         done="Returns 0.002 mol, so 0.10 mol/dm³ is right.")],
    misc=[{"pattern":"wrong_volume","check":"common","expect":0.08,
           "message":"Divide by the HNO₃ volume (0.020 dm³) in the last step. n(KOH) = 0.08 × 0.025 = 0.002 mol, so c = 0.002 ÷ 0.020 = 0.10 mol/dm³. Using the KOH volume gives 0.08."}])

setprob("silver", 5,
    "For g/dm³ divide mass by the volume in dm³, no moles needed.",
    [sayonly("g/dm³ uses mass straight away: \\(c_g = \\dfrac{m}{V}\\)."),
     box("Convert the volume: 200 ÷ 1000 = ", 0.2, "Divide by 1000.", post="dm³"),
     box("Divide mass by volume: 10.6 ÷ 0.2 = ", 53.0, "c = m ÷ V.", phase="substitute"),
     box("Check: 53.0 × 0.2 = ", 10.6, "c × V returns the mass.",
         done="Returns 10.6 g, so 53.0 g/dm³ is right.")],
    misc=[{"pattern":"unit_error","check":"common","expect":0.053,
           "message":"200 cm³ = 0.2 dm³. c = 10.6 ÷ 0.2 = 53.0 g/dm³. Dividing by 200 gives 0.053."}])
pb["silver"][2]["equation_hint"] = "H₂SO₄ : NaOH = 1 : 2, so double the moles of H₂SO₄"

# ===== GOLD =====
setprob("gold", 0,
    "Work down to the sample moles, apply the 1:2 ratio, then divide by the titre.",
    [sayonly("A five step chain: Mr, moles in the flask, flask concentration, moles in the sample, then the ratio and final concentration."),
     box("Relative formula mass of Na₂CO₃: (2×23) + 12 + (3×16) = ", 106, "46 + 12 + 48."),
     box("Moles in the flask: 5.3 ÷ 106 = ", 0.05, "n = mass ÷ Mr."),
     box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000.", post="dm³"),
     box("Flask concentration: 0.05 ÷ 0.25 = ", 0.2, "c = n ÷ V."),
     box("Moles in the 25.0 cm³ sample: 0.2 × 0.025 = ", 0.005, "n = c × V, sample volume 0.025 dm³."),
     box("Ratio 1 : 2, so moles of HCl: 0.005 × 2 = ", 0.01, "Two HCl per carbonate.", phase="substitute"),
     box("Concentration of HCl: 0.01 ÷ 0.025 = ", 0.4, "c = n ÷ V, titre 0.025 dm³.", phase="substitute"),
     box("Check: 0.4 × 0.025 = ", 0.01, "c × V returns the HCl moles.",
         done="Returns 0.01 mol HCl, matching the 1:2 ratio, so 0.40 mol/dm³ is right.")],
    misc=[{"pattern":"wrong_Mr","check":"common","expect":None,
           "message":"Mr Na₂CO₃ = (2×23) + 12 + (3×16) = 106. n = 5.3 ÷ 106 = 0.05 mol, c(flask) = 0.2 mol/dm³, sample n = 0.005 mol, ratio 1:2 gives n(HCl) = 0.01, c = 0.40 mol/dm³."},
          {"pattern":"mole_ratio","check":"common","expect":0.2,
           "message":"Na₂CO₃ : HCl = 1 : 2. Double the carbonate moles to get 0.01 mol HCl. Forgetting to double gives 0.005 ÷ 0.025 = 0.2."}])

setprob("gold", 1,
    "Find total moles in the flask, scale to 500 cm³, then multiply by the formula mass.",
    [sayonly("Work back from the titration to the original mass: acid moles, base moles, base concentration, scale to the whole flask, then mass."),
     box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000.", post="dm³"),
     box("Moles of HCl: 0.10 × 0.02 = ", 0.002, "n = c × V."),
     sayonly("Ratio KOH : HCl is 1 : 1, so moles of KOH in the 25.0 cm³ sample = 0.002 mol."),
     box("Concentration of KOH: 0.002 ÷ 0.025 = ", 0.08, "c = n ÷ V, sample volume 0.025 dm³."),
     box("Scale to the whole 500 cm³ flask (0.5 dm³): 0.08 × 0.5 = ", 0.04, "Total moles = concentration × flask volume.", phase="substitute"),
     box("Relative formula mass of KOH: 39 + 16 + 1 = ", 56, "Add the Ar values."),
     box("Mass: 0.04 × 56 = ", 2.24, "mass = moles × Mr.", phase="substitute"),
     box("Check: 2.24 ÷ 56 = ", 0.04, "mass ÷ Mr returns the total moles.",
         done="Returns 0.04 mol in the flask, so 2.24 g is right.")],
    misc=[{"pattern":"forgot_step","check":"common","expect":0.112,
           "message":"You titrated 25.0 cm³ from a 500 cm³ flask, so scale up: total mol = 0.08 × 0.5 = 0.04 mol, mass = 0.04 × 56 = 2.24 g. Skipping the scale-up gives only 0.112 g."},
          {"pattern":"scale_error","check":"common","expect":None,
           "message":"The 25.0 cm³ sample is one twentieth of the 500 cm³ flask. Multiply the concentration by 0.5 dm³ to get the total moles."}])

setprob("gold", 2,
    "Moles from concentration and volume, then mass = moles × formula mass.",
    [sayonly("Moles first, then mass: \\(n = c \\times V\\) then mass = \\(n \\times M_r\\)."),
     box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide by 1000.", post="dm³"),
     box("Moles: 0.4 × 0.5 = ", 0.2, "n = c × V."),
     box("Relative formula mass of HCl: 1 + 35.5 = ", 36.5, "Add Ar of H and Cl."),
     box("Mass: 0.2 × 36.5 = ", 7.3, "mass = moles × Mr.", phase="substitute"),
     box("Check: 7.3 ÷ 36.5 = ", 0.2, "mass ÷ Mr returns the moles.",
         done="Returns 0.2 mol, so 7.3 g is right.")],
    misc=[{"pattern":"forgot_convert","check":"common","expect":7300,
           "message":"Convert 500 cm³ to 0.5 dm³ first. n = 0.4 × 0.5 = 0.2 mol, mass = 0.2 × 36.5 = 7.3 g. Using 500 gives 7300 g."},
          {"pattern":"wrong_Mr","check":"common","expect":7.2,
           "message":"Mr HCl = 1 + 35.5 = 36.5, not 36. Mass = 0.2 × 36.5 = 7.3 g. Using 36 gives 7.2 g."}])

setprob("gold", 3,
    "Mean titre first, then moles, the 1:1 ratio, and the base concentration.",
    [sayonly("First the mean titre, then moles of acid, the 1 : 1 ratio, and the base concentration."),
     box("Mean of the concordant titres: (18.70 + 18.65 + 18.75) ÷ 3 = ", 18.7, "Add the three and divide by 3."),
     box("Convert the mean titre: 18.70 ÷ 1000 = ", 0.0187, "Divide by 1000.", post="dm³"),
     box("Moles of HCl: 0.20 × 0.0187 = ", 0.00374, "n = c × V."),
     sayonly("Ratio 1 : 1, so moles of NaOH = 0.00374 mol."),
     box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³"),
     box("Concentration of NaOH: 0.00374 ÷ 0.025 = ", 0.1496, "c = n ÷ V.", phase="substitute"),
     box("Round to 3 significant figures: 0.1496 → ", 0.15, "Three sig figs: 0.150.",
         done="0.150 mol/dm³ to 3 sig figs, so the answer is right.")],
    misc=[{"pattern":"wrong_volume","check":"common","expect":0.2,
           "message":"Divide by the NaOH volume (0.025 dm³), not the titre. n(NaOH) = 0.00374 mol, so c = 0.00374 ÷ 0.025 = 0.1496 mol/dm³. Using 0.0187 gives 0.2."},
          {"pattern":"rounding","check":"common","expect":None,
           "message":"Mean titre = 18.70 cm³ = 0.01870 dm³. n(HCl) = 0.003740 mol, c = 0.1496 mol/dm³, which rounds to 0.150 to 3 sig figs."},
          {"pattern":"wrong_mean","check":"common","expect":None,
           "message":"Average the three concordant results before using the titre: (18.70 + 18.65 + 18.75) ÷ 3 = 18.70 cm³."}])

# gold[4]: REPAIR. Stored answer 0.1 was wrong (0.1 is the citric acid concentration, not the
# NaOH), and this row duplicated gold[5]. Change titre 30.0 -> 25.0 cm3: answer 0.30, correct
# and distinct from gold[5] (0.25). Stays a full multi-step titration.
setprob("gold", 4,
    "Acid concentration, then sample moles, the 1:3 ratio, then the titre volume.",
    [sayonly("Chain through: acid moles, acid concentration, sample moles, then the 1 : 3 ratio and final concentration."),
     box("Moles of citric acid in the flask: 4.80 ÷ 192 = ", 0.025, "n = mass ÷ Mr."),
     box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000.", post="dm³"),
     box("Concentration of the acid: 0.025 ÷ 0.25 = ", 0.1, "c = n ÷ V."),
     box("Moles of acid in the 25.0 cm³ sample: 0.1 × 0.025 = ", 0.0025, "n = c × V, sample 0.025 dm³."),
     box("Ratio 1 : 3, so moles of NaOH: 0.0025 × 3 = ", 0.0075, "Three NaOH per acid.", phase="substitute"),
     box("Concentration of NaOH: 0.0075 ÷ 0.025 = ", 0.3, "c = n ÷ V, titre 0.025 dm³.", phase="substitute"),
     box("Check: 0.3 × 0.025 = ", 0.0075, "c × V returns the NaOH moles.",
         done="Returns 0.0075 mol NaOH, matching the 1:3 ratio, so 0.30 mol/dm³ is right.")],
    misc=[{"pattern":"mole_ratio","check":"common","expect":0.1,
           "message":"The equation shows 3 moles of NaOH per mole of citric acid. n(acid, sample) = 0.0025 mol, so n(NaOH) = 0.0075 mol and c = 0.0075 ÷ 0.025 = 0.30 mol/dm³. Forgetting to triple gives 0.1."},
          {"pattern":"forgot_ratio","check":"common","expect":None,
           "message":"Three moles of NaOH react with one mole of citric acid. Multiply the acid moles by 3."}],
    display=("A student makes up a standard solution of citric acid (Mr = 192) by dissolving 4.80 g in water "
             "and making up to 250 cm³. She titrates 25.0 cm³ of this against NaOH; the titre is 25.0 cm³. "
             "The equation is: H₃C₆H₅O₇ + 3NaOH → Na₃C₆H₅O₇ + 3H₂O. Calculate the concentration of the NaOH in mol/dm³."),
    solutions=[0.3])

setprob("gold", 5,
    "Same chain as before but the titre is 30.0 cm³.",
    [sayonly("The same chain: acid moles, acid concentration, sample moles, ratio, final concentration."),
     box("Moles of citric acid in the flask: 4.80 ÷ 192 = ", 0.025, "n = mass ÷ Mr."),
     box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000.", post="dm³"),
     box("Concentration of the acid: 0.025 ÷ 0.25 = ", 0.1, "c = n ÷ V."),
     box("Moles of acid in the 25.0 cm³ sample: 0.1 × 0.025 = ", 0.0025, "n = c × V."),
     box("Ratio 1 : 3, so moles of NaOH: 0.0025 × 3 = ", 0.0075, "Three NaOH per acid.", phase="substitute"),
     box("Convert the titre and divide: 0.0075 ÷ 0.030 = ", 0.25, "Titre 30.0 cm³ = 0.030 dm³; c = n ÷ V.", phase="substitute"),
     box("Check: 0.25 × 0.030 = ", 0.0075, "c × V returns the NaOH moles.",
         done="Returns 0.0075 mol NaOH, so 0.25 mol/dm³ is right.")],
    misc=[{"pattern":"mole_ratio","check":"common","expect":0.0833,
           "message":"n(acid, sample) = 0.0025 mol. Ratio 1 : 3, so n(NaOH) = 0.0075 mol and c = 0.0075 ÷ 0.030 = 0.25 mol/dm³. Forgetting to triple gives 0.0833."},
          {"pattern":"forgot_ratio","check":"common","expect":None,
           "message":"Three moles of NaOH react with one mole of citric acid. Multiply the acid moles by 3."}])

# ---------- tier_guides ----------
def exstep(label, content, ans=False):
    d={"label":label,"content":content}
    if ans: d["isAnswer"]=True; d["is_answer"]=True
    return d

pd["tier_guides"] = {
 "bronze": {
  "title":"Bronze: one formula, one divide",
  "steps":[
   "A concentration question gives you two of the three parts of \\(c = \\dfrac{n}{V}\\) and asks for the third.",
   "First fix the units: volume must be in <strong>dm³</strong>, so divide any cm³ figure by 1000.",
   "Then substitute and do the single divide or multiply. State mol/dm³ or g/dm³."],
  "example":{"question":"Calculate the concentration in mol/dm³ of 0.5 mol in 250 cm³.",
   "steps":[exstep("Convert","<p>250 ÷ 1000 = 0.25 dm³</p>"),
            exstep("Divide","<p>\\(c = 0.5 ÷ 0.25 = 2.0\\)</p>"),
            exstep("Check","<p>2.0 × 0.25 = 0.5 mol ✓</p>"),
            exstep("Answer","<p><strong>2.0 mol/dm³</strong></p>",True)]}
 },
 "silver": {
  "title":"Silver: titration in three moves",
  "steps":[
   "You know the concentration and volume of one solution and one volume of the other. Find the moles you can: \\(n = c \\times V\\).",
   "Cross the balanced equation by its mole ratio to get the moles of the unknown.",
   "Divide those moles by the unknown's volume (in dm³) for its concentration."],
  "example":{"question":"25.0 cm³ of HCl is neutralised by 20.0 cm³ of 0.150 mol/dm³ NaOH (1:1). Find the HCl concentration.",
   "steps":[exstep("Known moles","<p>n(NaOH) = 0.150 × 0.020 = 0.003 mol</p>"),
            exstep("Ratio","<p>1 : 1, so n(HCl) = 0.003 mol</p>"),
            exstep("Concentration","<p>\\(c = 0.003 ÷ 0.025 = 0.12\\)</p>"),
            exstep("Check","<p>0.12 × 0.025 = 0.003 mol ✓</p>"),
            exstep("Answer","<p><strong>0.12 mol/dm³</strong></p>",True)]}
 },
 "gold": {
  "title":"Gold: the full chain",
  "steps":[
   "Extra links appear: mass to moles with \\(n = \\dfrac{m}{M_r}\\), or scaling between a titrated sample and the whole flask.",
   "Build the chain in order and keep every volume in dm³. A non 1 : 1 ratio means multiply or divide by that ratio.",
   "Finish with the quantity asked for, then check by working backwards."],
  "example":{"question":"5.3 g Na₂CO₃ made to 250 cm³; 25.0 cm³ needs 25.0 cm³ HCl (1:2). Find the HCl concentration.",
   "steps":[exstep("Moles in flask","<p>Mr = 106, n = 5.3 ÷ 106 = 0.05 mol</p>"),
            exstep("Sample moles","<p>c = 0.05 ÷ 0.25 = 0.2; n in 25 cm³ = 0.005 mol</p>"),
            exstep("Ratio and concentration","<p>1 : 2 → n(HCl) = 0.01; \\(c = 0.01 ÷ 0.025 = 0.4\\)</p>"),
            exstep("Check","<p>0.4 × 0.025 = 0.01 mol ✓</p>"),
            exstep("Answer","<p><strong>0.40 mol/dm³</strong></p>",True)]}
 }
}

# ---------- guided ----------
pd["guided"] = {
 "opener":{
  "label":"Before any formula",
  "display":"8 g of salt is stirred into 2 litres of water.",
  "steps":[
   box("Grams of salt in each litre = ", 4, "Share 8 g across 2 litres: 8 ÷ 2.",
       say="No formula needed, just share it out. If 8 g of salt is spread evenly through 2 litres, each litre holds an equal share."),
   box("Grams of salt in each litre now = ", 2, "8 ÷ 4.",
       say="Now tip the same 8 g into 4 litres instead. Same salt, more water."),
   sayonly("That share per litre is <strong>concentration</strong>: amount ÷ volume. More water with the same salt makes it weaker. Chemistry writes it \\(c_g = \\dfrac{m}{V}\\) in g/dm³, or \\(c = \\dfrac{n}{V}\\) in mol/dm³. A dm³ is just a litre.")]
 },
 "teach":{
  "bronze":{
   "display":"Calculate the concentration in mol/dm³ of 0.6 mol dissolved in 300 cm³.",
   "label":"Together: your first one",
   "steps":[
    sayonly("Bronze concentration: one formula, \\(c = \\dfrac{n}{V}\\), volume in dm³."),
    box("Read the moles given: n = ", 0.6, "The question gives 0.6 mol."),
    box("Convert the volume: 300 ÷ 1000 = ", 0.3, "Divide by 1000.", post="dm³"),
    box("Divide moles by volume: 0.6 ÷ 0.3 = ", 2.0, "c = n ÷ V.", phase="substitute"),
    box("Check: 2.0 × 0.3 = ", 0.6, "c × V returns the moles.",
        done="Back to 0.6 mol, so 2.0 mol/dm³ is right. Bronze is just this one divide.")]
  },
  "silver":{
   "display":"20.0 cm³ of 0.10 mol/dm³ NaOH is neutralised by 25.0 cm³ of HCl. NaOH + HCl → NaCl + H₂O. Calculate the concentration of the HCl.",
   "label":"Together: the silver move",
   "steps":[
    sayonly("Silver adds the titration order: moles of the known, mole ratio, then the unknown concentration."),
    box("Convert the NaOH volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000.", post="dm³"),
    box("Moles of NaOH: 0.10 × 0.02 = ", 0.002, "n = c × V."),
    sayonly("Ratio NaOH : HCl is 1 : 1, so moles of HCl = 0.002 mol."),
    box("Convert the HCl volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000.", post="dm³", phase="substitute"),
    box("Concentration of HCl: 0.002 ÷ 0.025 = ", 0.08, "c = n ÷ V."),
    box("Check: 0.08 × 0.025 = ", 0.002, "c × V returns the moles.",
        done="Returns 0.002 mol, so 0.080 mol/dm³ is right.")]
  },
  "gold":{
   "display":"1.60 g of NaOH (Mr = 40) is dissolved and made up to 250 cm³. 25.0 cm³ is titrated with 0.20 mol/dm³ H₂SO₄. 2NaOH + H₂SO₄ → Na₂SO₄ + 2H₂O. Calculate the volume of H₂SO₄ needed.",
   "label":"Together: the gold move",
   "steps":[
    sayonly("Gold chains it all: mass to moles, flask concentration, sample moles, the 2 : 1 ratio, then rearrange for volume."),
    box("Moles of NaOH in the flask: 1.60 ÷ 40 = ", 0.04, "n = mass ÷ Mr."),
    box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000.", post="dm³"),
    box("Flask concentration: 0.04 ÷ 0.25 = ", 0.16, "c = n ÷ V."),
    box("Moles of NaOH in the 25.0 cm³ sample: 0.16 × 0.025 = ", 0.004, "n = c × V."),
    box("Ratio 2 : 1, so moles of H₂SO₄: 0.004 ÷ 2 = ", 0.002, "Two NaOH per acid, so halve.", phase="substitute"),
    box("Volume of H₂SO₄: 0.002 ÷ 0.20 = ", 0.01, "V = n ÷ c, in dm³."),
    box("Convert to cm³: 0.01 × 1000 = ", 10, "Multiply dm³ by 1000.",
        done="10 cm³ of H₂SO₄, so the answer is right.")]
  }
 }
}

io.open("lesson_higher-calculations-L02@95ac3b54f8.json","w",encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("written OK")
