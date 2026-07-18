# -*- coding: utf-8 -*-
import json, io

OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/lesson_higher-calculations-L01@34b52b21dc.json"
pd = json.load(io.open(OUT, encoding="utf-8"))
pb = pd["problem_bank"]

def box(pre, ans, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    d.update(kw)
    return d
def say(s, **kw):
    d = {"say": s}; d.update(kw); return d

# ---------- BRONZE guided_steps ----------
bronze_steps = [
 # B0
 [ say(r"Concentration links moles and volume: \(n = c \times V\). But the volume has to be in dm³ first."),
   box("Convert the volume: 25.0 ÷ 1000 = ", 0.025, "Divide the cm³ by 1000."),
   box("Now multiply: moles = 0.1 × 0.025 = ", 0.0025, "Concentration times volume in dm³.", phase="substitute"),
   box("Check by reversing: 0.0025 ÷ 0.025 = ", 0.1, "Moles divided by volume gives the concentration back.",
       done="Back to the concentration we started with, so 0.0025 mol is right.") ],
 # B1
 [ say(r"Concentration is moles over volume: \(c = \frac{n}{V}\). The volume is already in dm³, so nothing to convert."),
   box("Which number is the volume, in dm³? V = ", 0.25, "Read it from the question: 0.25 dm³."),
   box("concentration = 0.5 ÷ 0.25 = ", 2, "Divide the moles by the volume.", phase="substitute"),
   box("Check: 2 × 0.25 = ", 0.5, "Concentration times volume should give the moles back.",
       done="That is the moles we were given, so 2 mol/dm³ is right.") ],
 # B2
 [ say(r"This asks for a volume, so rearrange: \(V = \frac{n}{c}\)."),
   box("Which number is the moles? n = ", 0.2, "Read it from the question: 0.2 mol."),
   box("volume = 0.2 ÷ 0.5 = ", 0.4, "Moles divided by concentration.", phase="substitute"),
   box("Check: 0.5 × 0.4 = ", 0.2, "Concentration times volume should give the moles.",
       done="That gives the 0.2 mol we needed, so 0.4 dm³ is right.") ],
 # B3
 [ say(r"A mass, so start with \(n = \frac{\text{mass}}{M_r}\). The 500 cm³ of water is not needed for the moles."),
   box("Work out the Mr: 23 + 16 + 1 = ", 40, "Add the Ar values for Na, O and H."),
   box("moles = 4.0 ÷ 40 = ", 0.1, "Mass divided by Mr.", phase="substitute"),
   box("Check: 0.1 × 40 = ", 4, "Moles times Mr should give the mass back.",
       done="That is the 4.0 g we started with, so 0.1 mol is right.") ],
 # B4
 [ say(r"Concentration is moles over volume: \(c = \frac{n}{V}\), with the volume in dm³."),
   box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide the cm³ by 1000."),
   box("concentration = 0.15 ÷ 0.5 = ", 0.3, "Moles divided by volume in dm³.", phase="substitute"),
   box("Check: 0.3 × 0.5 = ", 0.15, "Concentration times volume gives the moles back.",
       done="Back to 0.15 mol, so 0.3 mol/dm³ is right.") ],
 # B5
 [ say(r"\(n = c \times V\), with the volume in dm³."),
   box("Convert the volume: 100 ÷ 1000 = ", 0.1, "Divide the cm³ by 1000."),
   box("moles = 0.25 × 0.1 = ", 0.025, "Concentration times volume in dm³.", phase="substitute"),
   box("Check: 0.025 ÷ 0.1 = ", 0.25, "Moles divided by volume gives the concentration.",
       done="Back to the concentration, so 0.025 mol is right.") ],
 # B6
 [ say("A pure unit conversion. Remember how many cm³ fit in one dm³."),
   box("How many cm³ make 1 dm³? ", 1000, "A dm³ is a litre, which is 1000 cm³."),
   box("So 50 ÷ 1000 = ", 0.05, "Divide by 1000.", phase="substitute"),
   box("Check: 0.05 × 1000 = ", 50, "Multiplying by 1000 should give the cm³ back.",
       done="Back to 50 cm³, so 0.05 dm³ is right.") ],
 # B7
 [ say(r"A mass, so \(n = \frac{\text{mass}}{M_r}\)."),
   box("Work out the Mr: 1 + 35.5 = ", 36.5, "Add the Ar values for H and Cl."),
   box("moles = 2.0 ÷ 36.5 = (to 3 s.f.) ", 0.0548, "Mass divided by Mr, rounded to 3 significant figures.", phase="substitute"),
   box("Check: 0.0548 × 36.5 = (about 2) ", 2, "Moles times Mr should come back to about 2 g.",
       done="Close to the 2.0 g we started with, so 0.0548 mol is right.") ],
]

# ---------- SILVER guided_steps ----------
silver_steps = [
 # S0
 [ say("Three moves: moles of the acid you know, the mole ratio, then the concentration of the base."),
   box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "Divide the cm³ by 1000."),
   box("moles HCl = 0.125 × 0.02 = ", 0.0025, "Concentration times volume in dm³."),
   say(r"The ratio HCl : NaOH is 1 : 1, so moles of NaOH = 0.0025 as well."),
   box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide the cm³ by 1000."),
   box("concentration NaOH = 0.0025 ÷ 0.025 = ", 0.1, "Moles of NaOH divided by its own volume.", phase="substitute"),
   box("Check: 0.1 × 0.025 = ", 0.0025, "Concentration times volume gives the moles back.",
       done="Back to the NaOH moles, so 0.1 mol/dm³ is right.") ],
 # S1
 [ say("Moles of the base, then halve for the 1:2 ratio, then the acid's concentration."),
   box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles NaOH = 0.2 × 0.025 = ", 0.005, "Concentration times volume."),
   box("The ratio H₂SO₄ : NaOH is 1 : 2, so moles H₂SO₄ = 0.005 ÷ 2 = ", 0.0025, "Half as much acid as base."),
   box("Convert the H₂SO₄ volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000."),
   box("concentration H₂SO₄ = 0.0025 ÷ 0.02 = ", 0.125, "Acid moles divided by acid volume.", phase="substitute"),
   box("Check: 0.125 × 0.02 = ", 0.0025, "Concentration times volume gives the moles back.",
       done="Back to the acid moles, so 0.125 mol/dm³ is right.") ],
 # S2
 [ say("Moles of the acid, 1:1 ratio, then divide by the base volume."),
   box("Convert the HCl volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles HCl = 0.15 × 0.025 = ", 0.00375, "Concentration times volume."),
   say("The ratio is 1 : 1, so moles of NaOH = 0.00375."),
   box("Convert the NaOH volume: 18.75 ÷ 1000 = ", 0.01875, "Divide by 1000."),
   box("concentration NaOH = 0.00375 ÷ 0.01875 = ", 0.2, "Base moles divided by base volume.", phase="substitute"),
   box("Check: 0.2 × 0.01875 = ", 0.00375, "Concentration times volume gives the moles back.",
       done="Back to the moles, so 0.2 mol/dm³ is right.") ],
 # S3 (rebuilt Ca(OH)2 -> 0.5)
 [ say("Moles of the base, double for the 1:2 ratio, then the acid concentration."),
   box("Convert the Ca(OH)₂ volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles Ca(OH)₂ = 0.1 × 0.025 = ", 0.0025, "Concentration times volume."),
   box("The ratio Ca(OH)₂ : HCl is 1 : 2, so moles HCl = 0.0025 × 2 = ", 0.005, "Twice as much acid as base."),
   box("Convert the HCl volume: 10.0 ÷ 1000 = ", 0.01, "Divide by 1000."),
   box("concentration HCl = 0.005 ÷ 0.01 = ", 0.5, "Acid moles divided by acid volume.", phase="substitute"),
   box("Check: 0.5 × 0.01 = ", 0.005, "Concentration times volume gives the moles back.",
       done="Back to the acid moles, so 0.5 mol/dm³ is right.") ],
 # S4 (rebuilt KOH+HNO3 -> 0.4)
 [ say("Moles of the base, 1:1 ratio, then divide by the acid volume."),
   box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles KOH = 0.2 × 0.025 = ", 0.005, "Concentration times volume."),
   say("The ratio is 1 : 1, so moles of HNO₃ = 0.005."),
   box("Convert the HNO₃ volume: 12.5 ÷ 1000 = ", 0.0125, "Divide by 1000."),
   box("concentration HNO₃ = 0.005 ÷ 0.0125 = ", 0.4, "Acid moles divided by acid volume.", phase="substitute"),
   box("Check: 0.4 × 0.0125 = ", 0.005, "Concentration times volume gives the moles back.",
       done="Back to the moles, so 0.4 mol/dm³ is right.") ],
 # S5
 [ say("Moles of the base, halve for the 1:2 ratio, then the acid concentration."),
   box("Convert the KOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles KOH = 0.5 × 0.025 = ", 0.0125, "Concentration times volume."),
   box("The ratio H₂SO₄ : KOH is 1 : 2, so moles H₂SO₄ = 0.0125 ÷ 2 = ", 0.00625, "Half as much acid as base."),
   box("Convert the H₂SO₄ volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("concentration H₂SO₄ = 0.00625 ÷ 0.025 = ", 0.25, "Acid moles divided by acid volume.", phase="substitute"),
   box("Check: 0.25 × 0.025 = ", 0.00625, "Concentration times volume gives the moles back.",
       done="Back to the acid moles, so 0.25 mol/dm³ is right.") ],
]

# ---------- GOLD guided_steps ----------
gold_steps = [
 # G0
 [ say("Start from the solid NaOH, find the flask concentration, then work the titration through to the HCl."),
   box("moles NaOH = 2.0 ÷ 40 = ", 0.05, "Mass divided by Mr."),
   box("Convert the flask volume: 200 ÷ 1000 = ", 0.2, "Divide by 1000."),
   box("concentration in the flask = 0.05 ÷ 0.2 = ", 0.25, "Moles divided by flask volume."),
   box("Convert the 25.0 cm³ sample: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles NaOH in the sample = 0.25 × 0.025 = ", 0.00625, "Flask concentration times sample volume."),
   say("The ratio NaOH : HCl is 1 : 1, so moles HCl = 0.00625."),
   box("Convert the titre: 31.25 ÷ 1000 = ", 0.03125, "Divide by 1000."),
   box("concentration HCl = 0.00625 ÷ 0.03125 = ", 0.2, "HCl moles divided by the titre volume.", phase="substitute"),
   box("Check: 0.2 × 0.03125 = ", 0.00625, "Concentration times volume gives the moles back.",
       done="Back to the HCl moles, so 0.2 mol/dm³ is right.") ],
 # G1
 [ say("Find the Mr and moles of the solid, the flask concentration, then the titration chain with a 1:2 ratio."),
   box("Mr of Na₂CO₃ = (2×23) + 12 + (3×16) = ", 106, "Add 46, 12 and 48."),
   box("moles Na₂CO₃ = 5.3 ÷ 106 = ", 0.05, "Mass divided by Mr."),
   box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000."),
   box("concentration in the flask = 0.05 ÷ 0.25 = ", 0.2, "Moles divided by flask volume."),
   box("Convert the 25.0 cm³ sample: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("moles Na₂CO₃ in the sample = 0.2 × 0.025 = ", 0.005, "Flask concentration times sample volume."),
   box("The ratio Na₂CO₃ : HCl is 1 : 2, so moles HCl = 0.005 × 2 = ", 0.01, "Twice as much acid."),
   box("The titre is also 25.0 cm³ = 0.025 dm³. concentration HCl = 0.01 ÷ 0.025 = ", 0.4,
       "HCl moles divided by the titre volume.", phase="substitute"),
   box("Check: 0.4 × 0.025 = ", 0.01, "Concentration times volume gives the moles back.",
       done="Back to the HCl moles, so 0.4 mol/dm³ is right.") ],
 # G2 (mass HCl -> 4.6)
 [ say("Find the moles from concentration and volume, then turn moles into mass with the Mr."),
   box("Convert the volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000."),
   box("moles = 0.5 × 0.25 = ", 0.125, "Concentration times volume."),
   box("Mr of HCl = 1 + 35.5 = ", 36.5, "Add the Ar values for H and Cl."),
   box("mass = 0.125 × 36.5 = ", 4.5625, "Moles times Mr.", phase="substitute"),
   box("Round to 1 decimal place: 4.5625 → ", 4.6, "The second decimal is a 6, so round the first decimal up.",
       done="So the mass of HCl is 4.6 g.") ],
 # G3 (mass KOH -> 2.24)
 [ say("The titration gives the concentration in the flask. Scale it up to the whole 500 cm³, then find the mass."),
   box("Convert the HCl volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000."),
   box("moles HCl = 0.1 × 0.02 = ", 0.002, "Concentration times volume."),
   say("The ratio is 1 : 1, so moles of KOH in the sample = 0.002."),
   box("Convert the sample volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("concentration of KOH = 0.002 ÷ 0.025 = ", 0.08, "Sample moles divided by sample volume."),
   box("Convert the flask volume: 500 ÷ 1000 = ", 0.5, "Divide by 1000."),
   box("total moles KOH = 0.08 × 0.5 = ", 0.04, "Flask concentration times flask volume."),
   box("Mr of KOH = 39 + 16 + 1 = ", 56, "Add the Ar values for K, O and H."),
   box("mass = 0.04 × 56 = ", 2.24, "Total moles times Mr.", phase="substitute"),
   box("Check: 2.24 ÷ 56 = ", 0.04, "Mass divided by Mr gives the moles back.",
       done="Back to the total moles, so 2.24 g is right.") ],
 # G4 (mass NaOH -> 1.6)
 [ say("The titration gives the flask concentration. Scale up to 250 cm³, then find the mass."),
   box("Convert the HNO₃ volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000."),
   box("moles HNO₃ = 0.2 × 0.02 = ", 0.004, "Concentration times volume."),
   say("The ratio is 1 : 1, so moles of NaOH in the sample = 0.004."),
   box("Convert the sample volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("concentration of NaOH = 0.004 ÷ 0.025 = ", 0.16, "Sample moles divided by sample volume."),
   box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000."),
   box("total moles NaOH = 0.16 × 0.25 = ", 0.04, "Flask concentration times flask volume."),
   box("Mr of NaOH = 23 + 16 + 1 = ", 40, "Add the Ar values for Na, O and H."),
   box("mass = 0.04 × 40 = ", 1.6, "Total moles times Mr.", phase="substitute"),
   box("Check: 1.6 ÷ 40 = ", 0.04, "Mass divided by Mr gives the moles back.",
       done="Back to the total moles, so 1.6 g is right.") ],
 # G5 (mass Na2CO3 -> 2.65)
 [ say("The titration gives the flask concentration. Scale up to 500 cm³, then find the mass."),
   box("Convert the H₂SO₄ volume: 12.5 ÷ 1000 = ", 0.0125, "Divide by 1000."),
   box("moles H₂SO₄ = 0.1 × 0.0125 = ", 0.00125, "Concentration times volume."),
   say("The ratio Na₂CO₃ : H₂SO₄ is 1 : 1, so moles of Na₂CO₃ in the sample = 0.00125."),
   box("Convert the sample volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
   box("concentration of Na₂CO₃ = 0.00125 ÷ 0.025 = ", 0.05, "Sample moles divided by sample volume."),
   box("Convert the flask volume: 500 ÷ 1000 = ", 0.5, "Divide by 1000."),
   box("total moles Na₂CO₃ = 0.05 × 0.5 = ", 0.025, "Flask concentration times flask volume."),
   box("Mr of Na₂CO₃ = (2×23) + 12 + (3×16) = ", 106, "Add 46, 12 and 48."),
   box("mass = 0.025 × 106 = ", 2.65, "Total moles times Mr.", phase="substitute"),
   box("Check: 2.65 ÷ 106 = ", 0.025, "Mass divided by Mr gives the moles back.",
       done="Back to the total moles, so 2.65 g is right.") ],
]

for i, gs in enumerate(bronze_steps):
    pb["bronze"][i]["guided_steps"] = gs
for i, gs in enumerate(silver_steps):
    pb["silver"][i]["guided_steps"] = gs
for i, gs in enumerate(gold_steps):
    pb["gold"][i]["guided_steps"] = gs

# ---------- tier_guides ----------
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one formula, right units",
   "steps": [
     r"Concentration links three things: moles, volume in dm³, and concentration in mol/dm³. Use \(c = \frac{n}{V}\), or rearrange it for whatever is missing.",
     "Volumes in these questions often come in cm³. Divide by 1000 to get dm³ BEFORE you substitute. This is the step that catches most people out.",
     r"If you are given a mass, turn it into moles first with \(n = \frac{\text{mass}}{M_r}\).",
   ],
   "example": {
     "question": "Calculate the number of moles in 50 cm³ of a 0.4 mol/dm³ solution.",
     "steps": [
       {"label": "Convert", "content": "<p>50 ÷ 1000 = 0.05 dm³</p>"},
       {"label": "Substitute", "content": r"<p>\(n = c \times V = 0.4 \times 0.05\)</p>"},
       {"label": "Check", "content": "<p>0.02 ÷ 0.05 = 0.4 mol/dm³ ✓</p>"},
       {"label": "Answer", "content": "<p><strong>0.02 mol</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: the three-step titration",
   "steps": [
     r"Step one: find the moles of the solution you fully know, using \(n = c \times V\) with the volume in dm³.",
     "Step two: read the mole ratio from the balanced equation. It is often 1:1, but acids like H₂SO₄ and bases like Ca(OH)₂ make it 1:2.",
     "Step three: divide those moles by the other solution's volume in dm³ to get its concentration.",
   ],
   "example": {
     "question": "25.0 cm³ of 0.1 mol/dm³ HCl neutralises 20.0 cm³ of NaOH. HCl + NaOH → NaCl + H₂O. Find the NaOH concentration.",
     "steps": [
       {"label": "Moles", "content": "<p>0.1 × 0.025 = 0.0025 mol HCl</p>"},
       {"label": "Ratio", "content": "<p>1:1, so 0.0025 mol NaOH</p>"},
       {"label": "Concentration", "content": "<p>0.0025 ÷ 0.02 = 0.125 mol/dm³</p>"},
       {"label": "Answer", "content": "<p><strong>0.125 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: flasks, scaling and mass",
   "steps": [
     "A volumetric flask holds a big volume (say 250 cm³), but you titrate only a small sample (say 25.0 cm³). The concentration is the same in both.",
     "Find the concentration from the titration, then scale to the whole flask: total moles = concentration × flask volume in dm³.",
     "If the question wants a mass, finish with mass = moles × Mr. If it gives a mass, start with moles = mass ÷ Mr.",
   ],
   "example": {
     "question": "4.0 g of NaOH (Mr 40) is made up to 200 cm³. Find the concentration in mol/dm³.",
     "steps": [
       {"label": "Moles", "content": "<p>4.0 ÷ 40 = 0.1 mol</p>"},
       {"label": "Convert", "content": "<p>200 ÷ 1000 = 0.2 dm³</p>"},
       {"label": "Concentration", "content": "<p>0.1 ÷ 0.2 = 0.5 mol/dm³</p>"},
       {"label": "Check", "content": "<p>0.5 × 0.2 = 0.1 mol ✓</p>"},
       {"label": "Answer", "content": "<p><strong>0.5 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

# ---------- guided: opener + teach ----------
pd["guided"] = {
 "opener": {
   "label": "Before any chemistry",
   "display": "A 2 litre jug of squash is made with 4 scoops of powder.",
   "steps": [
     say("No chemistry yet, just share it out.",
         pre="How many scoops are in each litre? ", post="", answer=2,
         hint="Split 4 scoops evenly across 2 litres."),
     say("That is <strong>concentration</strong>: amount shared over volume. In chemistry the amount is counted in <strong>moles</strong> and the volume in dm³, and a dm³ is just a litre.",
         pre="You pour out half a litre. How many scoops come with it? ", post="", answer=1,
         hint="Each litre holds 2 scoops, and you took half a litre."),
     say(r"That second move is <strong>moles = concentration × volume</strong>. A titration just does these two moves twice: once for the solution you know, once for the one you are after. One habit to build: chemistry gives volumes in cm³, so divide by 1000 to get dm³ first."),
   ],
 },
 "teach": {
   "bronze": {
     "label": "Together: your first one",
     "display": r"Calculate the number of moles in 250 cm³, then in 500 cm³, of a 0.2 mol/dm³ solution.",
     "steps": [
       say(r"Same equation each time: \(n = c \times V\), volume in dm³."),
       box("Convert 250 cm³: 250 ÷ 1000 = ", 0.25, "Divide by 1000."),
       box("moles = 0.2 × 0.25 = ", 0.05, "Concentration times volume."),
       box("Now 500 cm³: 500 ÷ 1000 = ", 0.5, "Divide by 1000."),
       box("moles = 0.2 × 0.5 = ", 0.1, "Concentration times the new volume.",
           done="Double the volume, double the moles, and the concentration never changed."),
     ],
   },
   "silver": {
     "label": "Together: the silver move",
     "display": r"25.0 cm³ of 0.1 mol/dm³ NaOH is neutralised by 20.0 cm³ of H₂SO₄. The equation is: H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O. Calculate the concentration of the H₂SO₄.",
     "steps": [
       say("The new move: read the mole ratio from the equation and use it in the middle."),
       box("Convert the NaOH volume: 25.0 ÷ 1000 = ", 0.025, "Divide by 1000."),
       box("moles NaOH = 0.1 × 0.025 = ", 0.0025, "Concentration times volume."),
       box("Ratio H₂SO₄ : NaOH = 1 : 2, so moles H₂SO₄ = 0.0025 ÷ 2 = ", 0.00125, "Half as much acid as base."),
       box("Convert the H₂SO₄ volume: 20.0 ÷ 1000 = ", 0.02, "Divide by 1000."),
       box("concentration H₂SO₄ = 0.00125 ÷ 0.02 = ", 0.0625, "Acid moles divided by acid volume.",
           done="The ratio step is the whole point of silver. That was it."),
     ],
   },
   "gold": {
     "label": "Together: the gold move",
     "display": r"8.0 g of NaOH (Mr = 40) is dissolved and made up to 250 cm³. A 25.0 cm³ sample is titrated against HCl, and the titre is 40.0 cm³. NaOH + HCl → NaCl + H₂O. Calculate the concentration of the HCl.",
     "steps": [
       say("The new move: a sample taken from a bigger flask. Find the flask concentration, then titrate the sample."),
       box("moles NaOH = 8.0 ÷ 40 = ", 0.2, "Mass divided by Mr."),
       box("Convert the flask volume: 250 ÷ 1000 = ", 0.25, "Divide by 1000."),
       box("concentration in the flask = 0.2 ÷ 0.25 = ", 0.8, "Moles divided by flask volume."),
       box("moles NaOH in the 25.0 cm³ sample = 0.8 × 0.025 = ", 0.02, "Flask concentration times sample volume (0.025 dm³)."),
       box("Ratio 1 : 1, and the titre is 40.0 cm³ = 0.04 dm³. concentration HCl = 0.02 ÷ 0.04 = ", 0.5,
           "HCl moles divided by the titre volume.",
           done="Flask to sample to titre. That is the gold move."),
     ],
   },
 },
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("build stage 2 ok")
