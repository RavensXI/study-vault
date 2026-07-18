# -*- coding: utf-8 -*-
import json, io

KEY = "higher-calculations-L02@689e4ebed1"
src = json.load(io.open("_L02_689e_canon.json", encoding="utf-8"))
pd = src["practice_data"]

def box(pre, answer, hint, post="", say=None, done=None, phase=False):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None:
        d["done"] = done
    if phase:
        d["phase"] = "substitute"
    return d

def sy(text):
    return {"say": text}

# ---------- method_card (slim, de-dashed, <=140 words) ----------
pd["method_card"]["title"] = "Gas Volumes, Atom Economy and Percentage Yield"
pd["method_card"]["steps"] = [
    "Spot which of the three you need: gas volume, atom economy, or percentage yield",
    "For gas volume: find moles of the gas (mass over Mr, then the ratio), then multiply by 24 dm³",
    "For atom economy: Mr of desired product over the Mr of ALL products, times 100",
    "For percentage yield: actual mass or volume over theoretical, times 100",
]
pd["method_card"]["content"] = (
    "<p>Three calculations, each with its own formula.</p>"
    "<p><strong>Gas volume at RTP:</strong> one mole of any gas fills 24 dm³, so "
    "\\(V = \\text{moles} \\times 24\\). For cm³, multiply by 1000.</p>"
    "<p><strong>Atom economy:</strong> a property of the balanced equation, "
    "\\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\). "
    "Use every coefficient, and put ALL products on the bottom.</p>"
    "<p><strong>Percentage yield:</strong> a property of the experiment, "
    "\\(\\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\).</p>"
    "<p>From a mass, always find moles first: "
    "\\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\).</p>"
)

# ---------- exam_context (de-dash) ----------
pd["exam_context"]["marks"] = "3 to 5 per calculation"
pd["exam_context"]["frequency"] = (
    "High. Atom economy and gas volumes are common in the higher-tier chemistry papers"
)

# ---------- worked_examples (de-dash labels) ----------
for ex in pd.get("worked_examples", []):
    for st in ex.get("steps", []):
        if "label" in st and " — " in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

# ---------- tier descriptions ----------
pb = pd["problem_bank"]
pb["bronze_description"] = (
    "One formula, values already in the right units: use the molar volume of 24 dm³, "
    "or read atom economy and percentage yield straight off."
)
pb["silver_description"] = (
    "Change the mass to moles first, use the balanced equation's ratio, then find the "
    "gas volume or the yield."
)
pb["gold_description"] = (
    "Chain the steps: theoretical amount then yield, watch the cm³ and dm³ units, and "
    "use every coefficient in atom economy."
)

WALKS = {}
HINTS = {}
MISC = {}

# ---- BRONZE ----
HINTS[("bronze", 0)] = "Multiply the moles by the molar volume, 24 dm³."
WALKS[("bronze", 0)] = [
    sy("Gas volume at RTP: one mole of any gas is 24 dm³, so \\(V = \\text{moles} \\times 24\\)."),
    box("The moles are given as 0.5. First write the molar volume: at RTP, 1 mole = ", 24,
        "The molar volume of any gas at RTP.", post=" dm³"),
    box("volume = 0.5 × 24 = ", 12, "Multiply the moles by the molar volume.", phase=True),
    box("Check by reversing: 12 ÷ 24 = ", 0.5,
        "Dividing the volume by 24 should give the moles back.",
        done="0.5 mol, back to the start. Volume = 12 dm³."),
]
MISC[("bronze", 0)] = ("inverse_error", 0.0208,
    "Volume = moles × 24, so 0.5 × 24 = 12 dm³. Dividing by 24 instead gives about 0.02, far too small for half a mole of gas.")

HINTS[("bronze", 1)] = "Divide the volume by 24 to get moles."
WALKS[("bronze", 1)] = [
    sy("To go from volume to moles, divide by the molar volume: \\(\\text{moles} = V \\div 24\\)."),
    box("Write the molar volume at RTP: 1 mole = ", 24, "The molar volume at RTP.", post=" dm³"),
    box("moles = 4.8 ÷ 24 = ", 0.2, "Divide the volume by 24.", phase=True),
    box("Check: 0.2 × 24 = ", 4.8, "Multiplying the moles by 24 should give the volume back.",
        done="4.8 dm³, matches. Moles = 0.2 mol."),
]
MISC[("bronze", 1)] = ("inverse_error", 115.2,
    "Moles = volume ÷ 24 = 4.8 ÷ 24 = 0.2 mol. Multiplying by 24 instead gives 115.2, which is not a sensible number of moles.")

HINTS[("bronze", 2)] = "Multiply the moles by 24."
WALKS[("bronze", 2)] = [
    sy("Gas volume at RTP: \\(V = \\text{moles} \\times 24\\)."),
    box("Write the molar volume at RTP: 1 mole = ", 24, "The molar volume at RTP.", post=" dm³"),
    box("volume = 2 × 24 = ", 48, "Multiply the moles by 24.", phase=True),
    box("Check: 48 ÷ 24 = ", 2, "Dividing by 24 should give the moles back.",
        done="2 mol, matches. Volume = 48 dm³."),
]
MISC[("bronze", 2)] = ("inverse_error", 0.0833,
    "Volume = moles × 24 = 2 × 24 = 48 dm³. Dividing gives about 0.08, far too small.")

HINTS[("bronze", 3)] = "Add up the Mr of every product for the bottom of the fraction."
WALKS[("bronze", 3)] = [
    sy("Atom economy = (Mr of the desired product ÷ Mr of ALL products) × 100."),
    box("Add the Mr of all products: 56 + 44 = ", 100, "Both CaO and CO₂ count."),
    box("atom economy = (56 ÷ 100) × 100 = ", 56, "Desired Mr over the total, times 100.", phase=True),
    box("The waste is CO₂: 100 − 56 = ", 44, "Take the atom economy from 100.",
        done="44% is lost as CO₂. Atom economy = 56%."),
]
MISC[("bronze", 3)] = ("wrong_denominator", 100,
    "Use the Mr of ALL products on the bottom: 56 + 44 = 100, so atom economy = (56 ÷ 100) × 100 = 56%. Putting only CaO on the bottom gives 100%, which would mean no waste.")

HINTS[("bronze", 4)] = "With only one product, all the atoms end up where you want them."
WALKS[("bronze", 4)] = [
    sy("Atom economy = (Mr desired ÷ Mr all products) × 100. Count the products of 2Mg + O₂ → 2MgO."),
    box("How many different products are there? ", 1, "Only MgO comes out."),
    box("With one product the desired Mr is the whole total, so atom economy = (1 ÷ 1) × 100 = ", 100,
        "Every atom ends up in the product you want.", phase=True),
    box("Fraction wasted = 100 − 100 = ", 0, "Take the atom economy from 100.",
        done="No atoms wasted. Atom economy = 100%."),
]
MISC[("bronze", 4)] = ("wrong_denominator", None,
    "There is only one product, MgO, so every atom ends up in it. Atom economy = 100%.")

HINTS[("bronze", 5)] = "Divide the actual mass by the theoretical mass, then times 100."
WALKS[("bronze", 5)] = [
    sy("Percentage yield = (actual ÷ theoretical) × 100."),
    box("Which is the theoretical maximum? Write it: ", 10, "The amount you expected to make.", post=" g"),
    box("percentage yield = (7.5 ÷ 10) × 100 = ", 75, "Actual over theoretical, times 100.", phase=True),
    box("Check: 75% of 10 g = 0.75 × 10 = ", 7.5, "Should give back the actual mass collected.",
        done="7.5 g, matches. Yield = 75%."),
]
MISC[("bronze", 5)] = ("inverse_error", 133.3,
    "Percentage yield = actual ÷ theoretical × 100 = 7.5 ÷ 10 × 100 = 75%. Dividing the wrong way (10 ÷ 7.5) gives 133%, which is impossible.")

HINTS[("bronze", 6)] = "Use the 2 to 1 ratio to get moles of O₂ before multiplying by 24."
WALKS[("bronze", 6)] = [
    sy("Gas volume needs moles of the gas first, then \\(V = \\text{moles} \\times 24\\). Read the ratio from the equation."),
    box("2 H₂O₂ make 1 O₂, so moles of O₂ = 0.1 ÷ 2 = ", 0.05, "Halve the moles of H₂O₂."),
    box("volume = 0.05 × 24 = ", 1.2, "Multiply moles of O₂ by 24.", phase=True),
    box("Check: 1.2 ÷ 24 = ", 0.05, "Dividing by 24 should give the moles of O₂ back.",
        done="0.05 mol of O₂, matches. Volume = 1.2 dm³."),
]
MISC[("bronze", 6)] = ("mole_ratio", 2.4,
    "From 2H₂O₂ → 2H₂O + O₂, 2 mol H₂O₂ make 1 mol O₂, so 0.1 mol gives 0.05 mol O₂ and 1.2 dm³. Skipping the ratio gives 2.4 dm³.")

HINTS[("bronze", 7)] = "Divide the volume by 24."
WALKS[("bronze", 7)] = [
    sy("Volume to moles: divide by the molar volume, \\(\\text{moles} = V \\div 24\\)."),
    box("Write the molar volume at RTP: 1 mole = ", 24, "The molar volume at RTP.", post=" dm³"),
    box("moles = 7.2 ÷ 24 = ", 0.3, "Divide the volume by 24.", phase=True),
    box("Check: 0.3 × 24 = ", 7.2, "Multiplying by 24 should give the volume back.",
        done="7.2 dm³, matches. Moles = 0.3 mol."),
]
MISC[("bronze", 7)] = ("inverse_error", 172.8,
    "Moles = volume ÷ 24 = 7.2 ÷ 24 = 0.3 mol. Multiplying by 24 instead gives 172.8.")

# ---- SILVER ----
HINTS[("silver", 0)] = "Turn the mass into moles first, then use the ratio, then times 24."
WALKS[("silver", 0)] = [
    sy("Gas volume from a mass: \\(\\text{moles} = \\text{mass} \\div M_r\\), use the ratio, then \\(V = \\text{moles} \\times 24\\)."),
    box("moles of CaCO₃ = 5.0 ÷ 100 = ", 0.05, "Mass over Mr."),
    box("1 CaCO₃ : 1 CO₂, so moles of CO₂ = ", 0.05, "The ratio is one to one."),
    box("volume = 0.05 × 24 = ", 1.2, "Moles of CO₂ times 24.", phase=True),
    box("Check: 1.2 ÷ 24 = ", 0.05, "Dividing by 24 should give the moles back.",
        done="0.05 mol, matches. Volume = 1.2 dm³."),
]
MISC[("silver", 0)] = ("forgot_step", 120,
    "Convert the mass to moles first: 5 ÷ 100 = 0.05 mol, then V = 0.05 × 24 = 1.2 dm³. Using the 5 g straight as moles gives 120 dm³, far too big.")

# S2 EDITED: 2.3 g -> 4.6 g to break duplicate 1.2 with S1; new answer 2.4
s2 = pb["silver"][1]
s2["display"] = ("4.6 g of sodium reacts with water: 2Na + 2H₂O → 2NaOH + H₂. "
                 "Calculate the volume of hydrogen gas produced at RTP in dm³. (Ar: Na = 23)")
s2["solutions"] = [2.4]
HINTS[("silver", 1)] = "Find moles of sodium, halve for H₂, then times 24."
WALKS[("silver", 1)] = [
    sy("Mass to gas volume: moles = mass ÷ Ar, then the ratio, then \\(V = \\text{moles} \\times 24\\)."),
    box("moles of Na = 4.6 ÷ 23 = ", 0.2, "Mass over Ar."),
    box("2 Na make 1 H₂, so moles of H₂ = 0.2 ÷ 2 = ", 0.1, "Halve the moles of sodium."),
    box("volume = 0.1 × 24 = ", 2.4, "Moles of H₂ times 24.", phase=True),
    box("Check: 2.4 ÷ 24 = ", 0.1, "Dividing by 24 should give the moles of H₂ back.",
        done="0.1 mol of H₂, matches. Volume = 2.4 dm³."),
]
MISC[("silver", 1)] = ("mole_ratio", 4.8,
    "2 Na make 1 H₂, so moles H₂ = 0.2 ÷ 2 = 0.1 and V = 2.4 dm³. Forgetting to halve gives 4.8 dm³.")

HINTS[("silver", 2)] = "Mass over Ar for moles, then times 24."
WALKS[("silver", 2)] = [
    sy("moles = mass ÷ Ar, ratio, then \\(V = \\text{moles} \\times 24\\)."),
    box("moles of Mg = 0.6 ÷ 24 = ", 0.025, "Mass over Ar."),
    box("1 Mg : 1 H₂, so moles of H₂ = ", 0.025, "One to one ratio."),
    box("volume = 0.025 × 24 = ", 0.6, "Moles times 24.", phase=True),
    box("Check: 0.6 ÷ 24 = ", 0.025, "Dividing by 24 should give the moles back.",
        done="0.025 mol, matches. Volume = 0.6 dm³."),
]
MISC[("silver", 2)] = ("forgot_step", 14.4,
    "Change grams to moles first: 0.6 ÷ 24 = 0.025 mol, then V = 0.025 × 24 = 0.6 dm³. Treating 0.6 g as moles gives 14.4 dm³.")

HINTS[("silver", 3)] = "Find the theoretical mass of iron, then compare with 5.6 g."
WALKS[("silver", 3)] = [
    sy("Percentage yield from a mass: find the theoretical mass of iron (moles, ratio, mass), then compare with the 5.6 g collected."),
    box("moles of Fe₂O₃ = 10 ÷ 160 = ", 0.0625, "Mass over Mr."),
    box("2 Fe₂O₃ make 4 Fe, so moles of Fe = 0.0625 × 2 = ", 0.125, "The ratio 2 : 4 doubles it."),
    box("theoretical mass of Fe = 0.125 × 56 = ", 7, "Moles times Ar."),
    box("percentage yield = (5.6 ÷ 7) × 100 = ", 80, "Actual over theoretical, times 100.", phase=True),
    box("Check: 80% of 7 g = 0.80 × 7 = ", 5.6, "Should give back the iron actually collected.",
        done="5.6 g, matches. Yield = 80%."),
]
MISC[("silver", 3)] = ("mole_ratio", 160,
    "2 Fe₂O₃ make 4 Fe, so double the moles: 0.125 mol Fe, theoretical mass 7.0 g, yield 80%. Forgetting the ratio gives an impossible 160%.")

HINTS[("silver", 4)] = "Multiply each product by its coefficient before dividing."
WALKS[("silver", 4)] = [
    sy("Atom economy uses the coefficients. The desired product is 2Fe; all products are 2Fe and 3CO₂."),
    box("Mr of 2Fe = 2 × 56 = ", 112, "Two iron atoms."),
    box("Mr of 3CO₂ = 3 × 44 = ", 132, "Three CO₂ molecules."),
    box("Mr of all products = 112 + 132 = ", 244, "Add both products."),
    box("atom economy = (112 ÷ 244) × 100 = ", 45.9, "Desired over total, times 100, to 1 d.p.", phase=True),
    box("The waste (CO₂) fraction = 100 − 45.9 = ", 54.1, "Take the atom economy from 100.",
        done="54.1% is lost as CO₂. Atom economy = 45.9%."),
]
MISC[("silver", 4)] = ("coefficient_error", 56,
    "Use the coefficients: desired 2Fe = 112, all products 112 + 132 = 244, so AE = (112 ÷ 244) × 100 = 45.9%. Ignoring the coefficients gives 56%.")

HINTS[("silver", 5)] = "Only one product means 100%."
WALKS[("silver", 5)] = [
    sy("Atom economy = (Mr desired ÷ Mr all products) × 100. Count the products of N₂ + 3H₂ → 2NH₃."),
    box("How many products are there? ", 1, "Only ammonia forms."),
    box("One product means the desired Mr is the whole total, so atom economy = (1 ÷ 1) × 100 = ", 100,
        "All atoms end up in ammonia.", phase=True),
    box("Fraction wasted = 100 − 100 = ", 0, "Take the atom economy from 100.",
        done="No atoms wasted. Atom economy = 100%."),
]
MISC[("silver", 5)] = ("wrong_denominator", None,
    "Ammonia is the only product, so all atoms end up in it. Atom economy = 100%.")

# ---- GOLD ----
HINTS[("gold", 0)] = "Find the theoretical volume, convert to cm³, then divide."
WALKS[("gold", 0)] = [
    sy("Percentage yield = (actual ÷ theoretical) × 100. Find the theoretical volume from the zinc, and mind the cm³ and dm³ units."),
    box("moles of Zn = 3.25 ÷ 65 = ", 0.05, "Mass over Ar."),
    box("1 Zn : 1 H₂, theoretical volume = 0.05 × 24 = ", 1.2, "Moles times 24, in dm³."),
    box("The gas was collected in cm³, so convert: 1.2 × 1000 = ", 1200, "1 dm³ = 1000 cm³."),
    box("percentage yield = (960 ÷ 1200) × 100 = ", 80, "Actual over theoretical, times 100.", phase=True),
    box("Check: 80% of 1200 cm³ = 0.80 × 1200 = ", 960, "Should give back the gas actually collected.",
        done="960 cm³, matches what was collected. Yield = 80%."),
]
MISC[("gold", 0)] = ("unit_error", None,
    "Theoretical volume = 0.05 × 24 = 1.2 dm³ = 1200 cm³. Yield = (960 ÷ 1200) × 100 = 80%. Match the units (dm³ and cm³) before dividing.")

HINTS[("gold", 1)] = "Add both products of Route B for the bottom of the fraction."
WALKS[("gold", 1)] = [
    sy("Atom economy for Route B: the desired product is CaO; the products are CaO and H₂O."),
    box("Mr of all products = 56 + 18 = ", 74, "Add CaO and water."),
    box("atom economy = (56 ÷ 74) × 100 = ", 75.7, "Desired over total, times 100, to 1 d.p.", phase=True),
    box("The waste (water) fraction = 100 − 75.7 = ", 24.3, "Take the atom economy from 100.",
        done="24.3% is lost as water. Route B atom economy = 75.7%."),
]
MISC[("gold", 1)] = ("wrong_route", 56,
    "Route B products are CaO + H₂O (56 + 18 = 74), so AE = (56 ÷ 74) × 100 = 75.7%. Using Route A's numbers (56 + 44) gives 56%.")

HINTS[("gold", 2)] = "Use the 1 to 3 ratio for CO₂, then times 24."
WALKS[("gold", 2)] = [
    sy("Gas volume from a mass: moles, then the ratio, then \\(V = \\text{moles} \\times 24\\)."),
    box("moles of Fe₂O₃ = 32 ÷ 160 = ", 0.2, "Mass over Mr."),
    box("1 Fe₂O₃ makes 3 CO₂, so moles of CO₂ = 0.2 × 3 = ", 0.6, "Multiply by 3."),
    box("volume = 0.6 × 24 = ", 14.4, "Moles of CO₂ times 24.", phase=True),
    box("Check: 14.4 ÷ 24 = ", 0.6, "Dividing by 24 should give the moles of CO₂ back.",
        done="0.6 mol of CO₂, matches. Volume = 14.4 dm³."),
]
MISC[("gold", 2)] = ("mole_ratio", 4.8,
    "1 Fe₂O₃ makes 3 CO₂, so moles CO₂ = 0.2 × 3 = 0.6 and V = 14.4 dm³. Forgetting the ×3 ratio gives 4.8 dm³.")

HINTS[("gold", 3)] = "Find Mr, then moles, then the 2 to 3 ratio, then times 24."
WALKS[("gold", 3)] = [
    sy("Find Mr of KClO₃, then moles, then the 2 : 3 ratio, then \\(V = \\text{moles} \\times 24\\)."),
    box("Mr of KClO₃ = 39 + 35.5 + (3 × 16) = ", 122.5, "Add K, Cl and three oxygens."),
    box("moles of KClO₃ = 12.25 ÷ 122.5 = ", 0.1, "Mass over Mr."),
    box("2 KClO₃ make 3 O₂, so moles of O₂ = 0.1 × 3 ÷ 2 = ", 0.15, "Multiply by 3, divide by 2."),
    box("volume = 0.15 × 24 = ", 3.6, "Moles of O₂ times 24.", phase=True),
    box("Check: 3.6 ÷ 24 = ", 0.15, "Dividing by 24 should give the moles of O₂ back.",
        done="0.15 mol of O₂, matches. Volume = 3.6 dm³."),
]
MISC[("gold", 3)] = ("mole_ratio", 2.4,
    "2 KClO₃ make 3 O₂, so moles O₂ = 0.1 × 3 ÷ 2 = 0.15 and V = 3.6 dm³. Ignoring the ratio gives 2.4 dm³.")

HINTS[("gold", 4)] = "Theoretical volume in cm³, then divide the 504 by it."
WALKS[("gold", 4)] = [
    sy("Percentage yield: theoretical volume of CO₂ from the CaCO₃, then compare with the 504 cm³ collected. Mind the cm³ and dm³ units."),
    box("moles of CaCO₃ = 2.5 ÷ 100 = ", 0.025, "Mass over Mr."),
    box("1 CaCO₃ : 1 CO₂, theoretical volume = 0.025 × 24 = ", 0.6, "Moles times 24, in dm³."),
    box("convert to cm³: 0.6 × 1000 = ", 600, "1 dm³ = 1000 cm³."),
    box("percentage yield = (504 ÷ 600) × 100 = ", 84, "Actual over theoretical, times 100.", phase=True),
    box("Check: 84% of 600 cm³ = 0.84 × 600 = ", 504, "Should give back the CO₂ actually collected.",
        done="504 cm³, matches. Yield = 84%."),
]
MISC[("gold", 4)] = ("unit_error", None,
    "Theoretical volume = 0.025 × 24 = 0.6 dm³ = 600 cm³. Yield = (504 ÷ 600) × 100 = 84%. Convert dm³ to cm³ before dividing.")

HINTS[("gold", 5)] = "Multiply each product by its coefficient, then divide 3O₂ by the total."
WALKS[("gold", 5)] = [
    sy("Atom economy for oxygen: the desired product is 3O₂; the products are 2KCl and 3O₂. Use the coefficients."),
    box("Mr of 3O₂ = 3 × 32 = ", 96, "Three O₂, each Mr 32."),
    box("Mr of 2KCl = 2 × (39 + 35.5) = ", 149, "Two KCl, each Mr 74.5."),
    box("Mr of all products = 96 + 149 = ", 245, "Add both products."),
    box("atom economy = (96 ÷ 245) × 100 = ", 39.2, "Desired over total, times 100, to 1 d.p.", phase=True),
    box("The waste (KCl) fraction = 100 − 39.2 = ", 60.8, "Take the atom economy from 100.",
        done="60.8% is the KCl. Oxygen atom economy = 39.2%."),
]
MISC[("gold", 5)] = ("coefficient_error", 56.3,
    "There are 2 KCl (Mr 149) and 3 O₂ (Mr 96), total 245, so AE = (96 ÷ 245) × 100 = 39.2%. Counting only one KCl (74.5) gives 56.3%.")

# apply
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        p["hint"] = HINTS[(tier, i)]
        p["guided_steps"] = WALKS[(tier, i)]
        pattern, expect, message = MISC[(tier, i)]
        p["misconceptions"] = [{
            "pattern": pattern,
            "check": "common",
            "expect": expect,
            "message": message,
        }]

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one formula, values ready to use",
        "steps": [
            "Spot which of the three you need. Gas volume: \\(V = \\text{moles} \\times 24\\) (dm³ at RTP). Atom economy: \\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\). Percentage yield: \\(\\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\).",
            "Numbers are already in the right units, so substitute straight in. For atom economy, add ALL the products on the bottom, not just the one you want.",
            "One calculation, one answer. State the unit: dm³, mol or %.",
        ],
        "example": {
            "question": "Calculate the volume of 0.4 mol of CO₂ at RTP.",
            "steps": [
                {"label": "Equation", "content": "<p>\\(V = \\text{moles} \\times 24\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(V = 0.4 \\times 24\\)</p>"},
                {"label": "Check", "content": "<p>\\(9.6 \\div 24 = 0.4\\) mol ✓</p>"},
                {"label": "Answer", "content": "<p><strong>9.6 dm³</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: find the moles first",
        "steps": [
            "Now you get a mass, not moles. Convert first: \\(\\text{moles} = \\frac{\\text{mass}}{M_r}\\).",
            "Use the equation's ratio to get moles of the gas or product you want, then \\(V = \\text{moles} \\times 24\\), or its mass with \\(\\text{mass} = \\text{moles} \\times M_r\\).",
            "Substitute back and check the value fits.",
        ],
        "example": {
            "question": "10 g of CaCO₃ → CaO + CO₂. Volume of CO₂ at RTP? (Mr: CaCO₃ = 100)",
            "steps": [
                {"label": "Moles", "content": "<p>\\(10 \\div 100 = 0.1\\) mol CaCO₃</p>"},
                {"label": "Ratio", "content": "<p>1 : 1, so 0.1 mol CO₂</p>"},
                {"label": "Volume", "content": "<p>\\(0.1 \\times 24 = 2.4\\)</p>"},
                {"label": "Check", "content": "<p>\\(2.4 \\div 24 = 0.1\\) mol ✓</p>"},
                {"label": "Answer", "content": "<p><strong>2.4 dm³</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two steps or convert units",
        "steps": [
            "Gold questions combine skills. For percentage yield from a gas, find the theoretical amount first (mass, moles, ratio, volume), then compare with what was collected.",
            "Watch the units: if the gas is in cm³ but the molar volume gives dm³, convert with \\(1\\text{ dm}^3 = 1000\\text{ cm}^3\\) before dividing.",
            "For atom economy, use every coefficient: \\(2\\text{Fe}\\) means \\(2 \\times M_r\\), then \\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\).",
        ],
        "example": {
            "question": "3.25 g Zn → H₂, collects 960 cm³ at RTP. % yield? (Ar: Zn = 65)",
            "steps": [
                {"label": "Theoretical moles", "content": "<p>\\(3.25 \\div 65 = 0.05\\) mol H₂</p>"},
                {"label": "Theoretical volume", "content": "<p>\\(0.05 \\times 24 = 1.2\\) dm³ \\(= 1200\\) cm³</p>"},
                {"label": "Yield", "content": "<p>\\((960 \\div 1200) \\times 100\\)</p>"},
                {"label": "Check", "content": "<p>\\(0.80 \\times 1200 = 960\\) cm³ ✓</p>"},
                {"label": "Answer", "content": "<p><strong>80%</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided: opener + teach ----------
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "You order 200 g of chips.<br>50 g are soggy, so you bin them.",
        "steps": [
            box("How many grams do you actually eat? 200 − 50 = ", 150,
                "Take the wasted 50 g off the 200 g you started with.",
                say="No chemistry yet, just common sense."),
            box("Now as a percentage of what you paid for: (150 ÷ 200) × 100 = ", 75,
                "150 out of 200, written as a percentage.",
                say="Now as a fraction of what you paid for:"),
            sy("That is exactly <strong>percentage yield</strong>: what you actually got, over the most you could have got, times 100. In a reaction the 'chips' are your product. <strong>Atom economy</strong> is the same fraction idea for atoms: of all the atoms in the products, what share are in the one you wanted?"),
        ],
    },
    "teach": {
        "bronze": {
            "display": "In the reaction CH₄ + 2O₂ → CO₂ + 2H₂O, the desired product is carbon dioxide. Calculate the atom economy. (Mr: CO₂ = 44, H₂O = 18)",
            "label": "Together: your first one",
            "steps": [
                sy("Atom economy = (Mr desired ÷ Mr all products) × 100. Both products count."),
                box("Mr of 2H₂O = 2 × 18 = ", 36, "Two water molecules."),
                box("Mr of all products = 44 + 36 = ", 80, "Add CO₂ and the water."),
                box("atom economy = (44 ÷ 80) × 100 = ", 55, "Desired over total, times 100.", phase=True),
                box("The waste is water: 100 − 55 = ", 45, "Take the atom economy from 100.",
                    done="45% is wasted as water. Atom economy = 55%."),
            ],
        },
        "silver": {
            "display": "8.0 g of methane burns: CH₄ + 2O₂ → CO₂ + 2H₂O. Calculate the volume of CO₂ produced at RTP in dm³. (Mr: CH₄ = 16)",
            "label": "Together: the silver move",
            "steps": [
                sy("Gas volume from a mass: moles = mass ÷ Mr, use the ratio, then \\(V = \\text{moles} \\times 24\\)."),
                box("moles of CH₄ = 8.0 ÷ 16 = ", 0.5, "Mass over Mr."),
                box("1 CH₄ : 1 CO₂, so moles of CO₂ = ", 0.5, "One to one ratio."),
                box("volume = 0.5 × 24 = ", 12, "Moles of CO₂ times 24.", phase=True),
                box("Check: 12 ÷ 24 = ", 0.5, "Dividing by 24 should give the moles back.",
                    done="0.5 mol, matches. Volume = 12 dm³."),
            ],
        },
        "gold": {
            "display": "6.5 g of zinc reacts: Zn + H₂SO₄ → ZnSO₄ + H₂. The student collects 1800 cm³ of hydrogen at RTP. Calculate the percentage yield. (Ar: Zn = 65)",
            "label": "Together: the gold move",
            "steps": [
                sy("Percentage yield = (actual ÷ theoretical) × 100. Find the theoretical volume from the zinc, and mind the cm³ and dm³ units."),
                box("moles of Zn = 6.5 ÷ 65 = ", 0.1, "Mass over Ar."),
                box("1 Zn : 1 H₂, theoretical volume = 0.1 × 24 = ", 2.4, "Moles times 24, in dm³."),
                box("convert to cm³: 2.4 × 1000 = ", 2400, "1 dm³ = 1000 cm³."),
                box("percentage yield = (1800 ÷ 2400) × 100 = ", 75, "Actual over theoretical, times 100.", phase=True),
                box("Check: 75% of 2400 cm³ = 0.75 × 2400 = ", 1800, "Should give back the gas collected.",
                    done="1800 cm³, matches. Yield = 75%."),
            ],
        },
    },
}

out = "lesson_" + KEY + ".json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)

def words(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card content words:", words(pd["method_card"]["content"]))
for t in ("bronze", "silver", "gold"):
    print("tier_guide", t, "step words:", sum(words(x) for x in pd["tier_guides"][t]["steps"]))
