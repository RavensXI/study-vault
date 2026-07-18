# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_canonical.json", encoding="utf-8"))

# ---------------- method_card (trim to <=4 steps, <=140 words) ----------------
pd["method_card"]["title"] = "Mole Calculations"
pd["method_card"]["steps"] = [
    "Find Mᵣ by adding the Aᵣ of every atom in the formula.",
    "Moles: n = m ÷ Mᵣ, or n = c × V with volume in dm³.",
    "Reacting masses: moles of the known, scale by the equation's ratio, then m = n × Mᵣ.",
    "Convert cm³ to dm³ (÷1000) before using c × V, then state the unit.",
]
pd["method_card"]["content"] = (
    "<p>The mole is the chemist's counting unit: one mole is 6.02 × 10²³ particles "
    "(the Avogadro constant). Particles are too small to count, so we weigh them instead.</p>"
    "<p><strong>Three core equations:</strong></p>"
    "<ul><li>\\(n = \\dfrac{m}{M_r}\\), moles from mass</li>"
    "<li>\\(m = n \\times M_r\\), the rearrangement for mass</li>"
    "<li>\\(n = c \\times V\\), moles from concentration and volume in dm³</li></ul>"
    "<p><strong>Finding Mᵣ:</strong> add the Aᵣ of every atom, watching subscripts. "
    "For reacting masses, find moles of the known substance, scale by the balanced "
    "equation's ratio, then convert back to mass.</p>"
)

# ---------------- tier descriptions ----------------
pb = pd["problem_bank"]
pb["bronze_description"] = "One equation with the values ready: find Mᵣ, or go straight into n = m ÷ Mᵣ or m = n × Mᵣ."
pb["silver_description"] = "Two steps: convert a volume to dm³ first, or use the balanced equation's ratio (often 1:1) to cross from one substance to another."
pb["gold_description"] = "Multi-step: find moles, apply a ratio that is not 1:1, then convert back, sometimes via concentration and volume."

# ---------------- per-problem hints ----------------
hints = {
    ("bronze",0):"Add the Aᵣ of every atom: two H plus one O.",
    ("bronze",1):"Find Mᵣ(CO₂) first, then divide the mass by it.",
    ("bronze",2):"Divide the mass by the Mᵣ you were given.",
    ("bronze",3):"Work out Mᵣ(NaOH), then multiply by the number of moles.",
    ("bronze",4):"Multiply the moles by 6.02 × 10²³.",
    ("bronze",5):"Count 2 H, 1 S and 4 O, then add their masses.",
    ("bronze",6):"Find Mᵣ(CuSO₄), then multiply by 0.25.",
    ("bronze",7):"Find Mᵣ(NaCl), then divide the mass by it.",
    ("silver",0):"Moles of CuO first, use the 1:1 ratio, then mass = moles × Aᵣ(Cu).",
    ("silver",1):"Moles of CaCO₃, then the 1:1 ratio gives the moles of CO₂.",
    ("silver",2):"Turn 200 cm³ into dm³ first, then n = c × V.",
    ("silver",3):"The 2:2 ratio is 1:1, so moles of NaOH equal moles of Na.",
    ("silver",4):"Moles of sulfur first, then the 1:1 ratio gives moles of Mg.",
    ("silver",5):"Moles from mass ÷ Mᵣ, volume in dm³, then c = n ÷ V.",
    ("gold",0):"Moles of Fe₂O₃, double for the 1:2 ratio, then mass = moles × Aᵣ(Fe).",
    ("gold",1):"Moles of Al, the ratio is 1:1, then multiply by Mᵣ(AlCl₃) = 133.5.",
    ("gold",2):"Moles from mass ÷ Mᵣ, volume in dm³, then c = n ÷ V.",
    ("gold",3):"Moles of N₂, double for the 1:2 ratio, then mass = moles × Mᵣ(NH₃).",
    ("gold",4):"Rearrange to Mᵣ = mass ÷ moles.",
    ("gold",5):"Moles of HCl from c × V, halve for the 1:2 ratio, then mass = moles × Aᵣ(Zn).",
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        p["hint"] = hints[(tier,i)]

# ---------------- fix G5 (gold index 4): nonsensical -> real gas N2 ----------------
g5 = pb["gold"][4]
g5["display"] = ("A student identifies an unknown gas: 7.0 g of the gas contains 0.25 mol. "
                 "Calculate the Mᵣ of the gas, then name it if it is a diatomic element with Aᵣ = 14.")
g5["solutions"] = [28]
g5["accept"] = 0.5
g5["unit"] = ""
g5["misconceptions"] = [
    {"pattern":"inverse_error","check":"common",
     "message":"Rearrange n = m ÷ Mᵣ to Mᵣ = m ÷ n = 7.0 ÷ 0.25 = 28. Dividing the other way (0.25 ÷ 7.0) gives about 0.036, which is not a sensible Mᵣ.",
     "expect":0.0357},
    {"pattern":"forgot_step","check":"common",
     "message":"Mᵣ = 28 matches a diatomic element with Aᵣ 14: nitrogen, N₂. A single N atom (14) is not a whole molecule.",
     "expect":None},
]

# ---------------- expects for existing misconceptions ----------------
expects = {
    ("bronze",0):[17],
    ("bronze",1):[None],
    ("bronze",2):[162],
    ("bronze",3):[40],
    ("bronze",4):[602000000000000000000000],
    ("bronze",5):[50],
    ("bronze",6):[160],
    ("bronze",7):[None],
    ("silver",0):[16,None],
    ("silver",1):[0.1],
    ("silver",2):[100],
    ("silver",3):[None],
    ("silver",4):[96],
    ("silver",5):[0.0002],
    ("gold",0):[None,8.4],
    ("gold",1):[12.5,None],
    ("gold",2):[None,0.0002],
    ("gold",3):[None,17],
    ("gold",5):[0.1625,81.25],
}
for (tier,pidx),vals in expects.items():
    ms = pb[tier][pidx]["misconceptions"]
    for m,ev in zip(ms,vals):
        m["expect"] = ev

# ---------------- guided_steps per problem ----------------
GS = {}
GS[("bronze",0)] = [
    {"pre":"Hydrogen: 2 atoms × 1 = ","post":"","answer":2,"hint":"Two H atoms, each with Aᵣ 1."},
    {"phase":"substitute","pre":"Oxygen: 1 atom × 16 = ","post":"","answer":16,"hint":"One O atom, Aᵣ 16."},
    {"pre":"Add for the total Mᵣ: 2 + 16 = ","post":"","answer":18,"done":"Mᵣ(H₂O) = 18: the mass of one mole of water.","hint":"Total the atom masses."},
]
GS[("bronze",1)] = [
    {"pre":"Carbon: 1 × 12 = ","post":"","answer":12,"hint":"One C atom, Aᵣ 12."},
    {"pre":"Oxygen: 2 × 16 = ","post":"","answer":32,"hint":"Two O atoms."},
    {"pre":"Mᵣ(CO₂) = 12 + 32 = ","post":"","answer":44,"hint":"Add the atom masses."},
    {"say":"Now use n = m ÷ Mᵣ.","phase":"substitute","pre":"44 ÷ 44 = ","post":"","answer":1.0,"hint":"How many times does 44 go into 44?"},
    {"pre":"Check: one mole should weigh one Mᵣ, so 1 × 44 = ","post":"","answer":44,"done":"Matches the 44 g given, so n = 1.0 mol.","hint":"moles × Mᵣ."},
]
GS[("bronze",2)] = [
    {"pre":"How many grams are in one whole mole of water? The Mᵣ = ","post":"","answer":18,"hint":"It is given in the question."},
    {"say":"Now n = m ÷ Mᵣ.","phase":"substitute","pre":"9.0 ÷ 18 = ","post":"","answer":0.5,"hint":"9 is exactly half of 18."},
    {"pre":"Check: 0.5 mol should weigh half of 18, so 0.5 × 18 = ","post":"","answer":9,"done":"Matches the 9.0 g given, so n = 0.5 mol.","hint":"moles × Mᵣ."},
]
GS[("bronze",3)] = [
    {"pre":"Sodium: 1 × 23 = ","post":"","answer":23,"hint":"One Na atom."},
    {"pre":"Oxygen + hydrogen: 16 + 1 = ","post":"","answer":17,"hint":"One O and one H."},
    {"pre":"Mᵣ(NaOH) = 23 + 17 = ","post":"","answer":40,"hint":"Add the atom masses."},
    {"say":"Mass = moles × Mᵣ.","phase":"substitute","pre":"2.0 × 40 = ","post":"","answer":80,"hint":"Two lots of 40."},
    {"pre":"Check: two moles is 40 + 40 = ","post":"","answer":80,"done":"Two moles of NaOH is 80 g.","hint":"Add one mole to itself."},
]
GS[("bronze",4)] = None
GS[("bronze",5)] = [
    {"pre":"Hydrogen: 2 × 1 = ","post":"","answer":2,"hint":"Two H atoms."},
    {"pre":"Sulfur: 1 × 32 = ","post":"","answer":32,"hint":"One S atom."},
    {"phase":"substitute","pre":"Oxygen: 4 × 16 = ","post":"","answer":64,"hint":"Four O atoms."},
    {"pre":"Add all three: 2 + 32 + 64 = ","post":"","answer":98,"done":"Mᵣ(H₂SO₄) = 98.","hint":"Total the parts."},
]
GS[("bronze",6)] = [
    {"pre":"Copper + sulfur: 64 + 32 = ","post":"","answer":96,"hint":"Add the two Aᵣ values."},
    {"pre":"Oxygen: 4 × 16 = ","post":"","answer":64,"hint":"Four O atoms."},
    {"pre":"Mᵣ(CuSO₄) = 96 + 64 = ","post":"","answer":160,"hint":"Add the parts."},
    {"say":"Mass = moles × Mᵣ.","phase":"substitute","pre":"0.25 × 160 = ","post":"","answer":40,"hint":"A quarter of 160."},
    {"pre":"Check: a quarter of 160 is 160 ÷ 4 = ","post":"","answer":40,"done":"0.25 mol of CuSO₄ is 40 g.","hint":"Divide 160 by 4."},
]
GS[("bronze",7)] = [
    {"pre":"Sodium + chlorine: 23 + 35.5 = ","post":"","answer":58.5,"hint":"Add the two Aᵣ values."},
    {"say":"Now n = m ÷ Mᵣ.","phase":"substitute","pre":"5.85 ÷ 58.5 = ","post":"","answer":0.1,"hint":"5.85 is one tenth of 58.5."},
    {"pre":"Check: a tenth of 58.5 is 58.5 ÷ 10 = ","post":"","answer":5.85,"done":"Matches the 5.85 g, so n = 0.10 mol.","hint":"Divide 58.5 by 10."},
]
GS[("silver",0)] = [
    {"pre":"Mᵣ(CuO) = 64 + 16 = ","post":"","answer":80,"hint":"Add Cu and O."},
    {"pre":"Moles of CuO = 16 ÷ 80 = ","post":"","answer":0.2,"hint":"mass ÷ Mᵣ."},
    {"say":"The equation gives CuO : Cu = 1 : 1.","phase":"substitute","pre":"Moles of Cu = ","post":"","answer":0.2,"hint":"Same as the CuO, because 1:1."},
    {"pre":"Mass of Cu = 0.2 × 64 = ","post":"","answer":12.8,"hint":"moles × Aᵣ(Cu)."},
    {"pre":"Check: the oxygen lost weighs 16 − 12.8 = ","post":"","answer":3.2,"done":"0.2 mol of O is 3.2 g, and 12.8 + 3.2 = 16 g. Conserved.","hint":"Subtract from the starting mass."},
]
GS[("silver",1)] = [
    {"pre":"Moles of CaCO₃ = 10.0 ÷ 100 = ","post":"","answer":0.1,"hint":"mass ÷ Mᵣ."},
    {"say":"Ratio CaCO₃ : CO₂ = 1 : 1.","phase":"substitute","pre":"Moles of CO₂ = ","post":"","answer":0.1,"hint":"1:1 ratio."},
    {"pre":"Mass of CO₂ = 0.1 × 44 = ","post":"","answer":4.4,"hint":"moles × Mᵣ."},
    {"pre":"Check: the solid CaO left (Mᵣ 56) = 0.1 × 56 = ","post":"","answer":5.6,"done":"4.4 g gas + 5.6 g solid = 10.0 g. Conserved.","hint":"moles × Mᵣ(CaO)."},
]
GS[("silver",2)] = [
    {"pre":"Convert the volume to dm³: 200 ÷ 1000 = ","post":"","answer":0.2,"hint":"cm³ to dm³ means divide by 1000."},
    {"say":"Now n = c × V.","phase":"substitute","pre":"0.50 × 0.20 = ","post":"","answer":0.1,"hint":"concentration × volume in dm³."},
    {"pre":"Check: 0.20 dm³ is a fifth of a dm³, so 0.50 ÷ 5 = ","post":"","answer":0.1,"done":"0.10 mol in 200 cm³.","hint":"Divide the concentration by 5."},
]
GS[("silver",3)] = [
    {"pre":"Moles of Na = 4.6 ÷ 23 = ","post":"","answer":0.2,"hint":"mass ÷ Aᵣ."},
    {"say":"Ratio Na : NaOH = 2 : 2 = 1 : 1.","phase":"substitute","pre":"Moles of NaOH = ","post":"","answer":0.2,"hint":"1:1 ratio."},
    {"pre":"Mᵣ(NaOH) = 23 + 16 + 1 = ","post":"","answer":40,"hint":"Add Na, O and H."},
    {"pre":"Mass of NaOH = 0.2 × 40 = ","post":"","answer":8.0,"done":"8.0 g of sodium hydroxide.","hint":"moles × Mᵣ."},
]
GS[("silver",4)] = [
    {"pre":"Moles of S = 8 ÷ 32 = ","post":"","answer":0.25,"hint":"mass ÷ Aᵣ."},
    {"say":"Ratio Mg : S = 1 : 1.","phase":"substitute","pre":"Moles of Mg = ","post":"","answer":0.25,"hint":"1:1 ratio."},
    {"pre":"Mass of Mg = 0.25 × 24 = ","post":"","answer":6.0,"hint":"moles × Aᵣ(Mg)."},
    {"pre":"Check: MgS made = 6.0 + 8.0 = ","post":"","answer":14,"done":"0.25 mol MgS (Mᵣ 56) = 14 g. Conserved.","hint":"Add the two starting masses."},
]
GS[("silver",5)] = [
    {"pre":"Moles of NaOH = 4.0 ÷ 40 = ","post":"","answer":0.1,"hint":"mass ÷ Mᵣ."},
    {"pre":"Convert the volume: 500 ÷ 1000 = ","post":"","answer":0.5,"hint":"cm³ to dm³."},
    {"say":"Now c = n ÷ V.","phase":"substitute","pre":"0.10 ÷ 0.50 = ","post":"","answer":0.2,"hint":"moles ÷ volume in dm³."},
    {"pre":"Check: 0.20 × 0.5 = ","post":"","answer":0.1,"done":"0.10 mol, matching the moles we found. c = 0.20 mol/dm³.","hint":"c × V should return the moles."},
]
GS[("gold",0)] = [
    {"pre":"Moles of Fe₂O₃ = 24 ÷ 160 = ","post":"","answer":0.15,"hint":"mass ÷ Mᵣ."},
    {"say":"Ratio Fe₂O₃ : Fe = 1 : 2, so double the moles.","phase":"substitute","pre":"Moles of Fe = 0.15 × 2 = ","post":"","answer":0.3,"hint":"Two Fe per Fe₂O₃."},
    {"pre":"Mass of Fe = 0.30 × 56 = ","post":"","answer":16.8,"hint":"moles × Aᵣ(Fe)."},
    {"pre":"Check by mass fraction: iron is 112 of the 160, so 0.7 × 24 = ","post":"","answer":16.8,"done":"16.8 g of iron, matching both routes.","hint":"112 ÷ 160 = 0.7 of the 24 g."},
]
GS[("gold",1)] = [
    {"pre":"Moles of Al = 5.4 ÷ 27 = ","post":"","answer":0.2,"hint":"mass ÷ Aᵣ."},
    {"say":"Ratio 2Al : 2AlCl₃ = 1 : 1.","phase":"substitute","pre":"Moles of AlCl₃ = ","post":"","answer":0.2,"hint":"1:1 ratio."},
    {"pre":"Mᵣ(AlCl₃) = 27 + (3 × 35.5) = ","post":"","answer":133.5,"hint":"Add Al to three Cl."},
    {"pre":"Mass of AlCl₃ = 0.2 × 133.5 = ","post":"","answer":26.7,"done":"26.7 g of aluminium chloride.","hint":"moles × Mᵣ."},
]
GS[("gold",2)] = [
    {"pre":"Mᵣ(Na₂CO₃) = (2×23) + 12 + (3×16) = ","post":"","answer":106,"hint":"46 + 12 + 48."},
    {"pre":"Moles = 5.3 ÷ 106 = ","post":"","answer":0.05,"hint":"mass ÷ Mᵣ."},
    {"pre":"Convert the volume: 250 ÷ 1000 = ","post":"","answer":0.25,"hint":"cm³ to dm³."},
    {"say":"Now c = n ÷ V.","phase":"substitute","pre":"0.050 ÷ 0.25 = ","post":"","answer":0.2,"hint":"moles ÷ volume in dm³."},
    {"pre":"Check: 0.20 × 0.25 = ","post":"","answer":0.05,"done":"0.050 mol, matching. c = 0.20 mol/dm³.","hint":"c × V should return the moles."},
]
GS[("gold",3)] = [
    {"pre":"Mᵣ(N₂) = 2 × 14 = ","post":"","answer":28,"hint":"Two N atoms."},
    {"pre":"Moles of N₂ = 28 ÷ 28 = ","post":"","answer":1.0,"hint":"mass ÷ Mᵣ."},
    {"say":"Ratio N₂ : NH₃ = 1 : 2, so double the moles.","phase":"substitute","pre":"Moles of NH₃ = 1.0 × 2 = ","post":"","answer":2.0,"hint":"Two NH₃ per N₂."},
    {"pre":"Mᵣ(NH₃) = 14 + 3 = ","post":"","answer":17,"hint":"One N and three H."},
    {"pre":"Mass of NH₃ = 2.0 × 17 = ","post":"","answer":34,"done":"34 g of ammonia.","hint":"moles × Mᵣ."},
]
GS[("gold",4)] = [
    {"say":"n = m ÷ Mᵣ. We know n and m, so rearrange to Mᵣ = m ÷ n.","pre":"What is the mass? m = ","post":"","answer":7.0,"hint":"Read it from the question."},
    {"phase":"substitute","pre":"Now divide by the moles: 7.0 ÷ 0.25 = ","post":"","answer":28,"hint":"Dividing by 0.25 is the same as multiplying by 4."},
    {"pre":"The gas is a diatomic element with Aᵣ 14, so its Mᵣ = 2 × 14 = ","post":"","answer":28,"done":"Mᵣ = 28, which is N₂, nitrogen gas.","hint":"Two atoms, each 14."},
]
GS[("gold",5)] = [
    {"pre":"Convert the volume: 25.0 ÷ 1000 = ","post":"","answer":0.025,"hint":"cm³ to dm³."},
    {"pre":"Moles of HCl = 0.10 × 0.025 = ","post":"","answer":0.0025,"hint":"n = c × V."},
    {"say":"Ratio Zn : HCl = 1 : 2, so halve the moles.","phase":"substitute","pre":"Moles of Zn = 0.0025 ÷ 2 = ","post":"","answer":0.00125,"hint":"One Zn for every two HCl."},
    {"pre":"Mass of Zn = 0.00125 × 65 = ","post":"","answer":0.08125,"done":"About 0.0813 g of zinc reacts.","hint":"moles × Aᵣ(Zn)."},
]

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs = GS.get((tier,i))
        if gs is None:
            p["guided_skip_reason"] = "Answer is a single multiplication by the Avogadro constant giving a value near 3 × 10²³, which cannot be entered box-by-box at the engine's tolerance."
        else:
            p["guided_steps"] = gs

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Find <strong>Mᵣ</strong> by adding the Aᵣ of every atom. Watch the small subscript numbers: H₂O has <strong>two</strong> H.",
            "Then use one equation: moles <strong>n = m ÷ Mᵣ</strong>, or mass <strong>m = n × Mᵣ</strong>.",
            "State the unit: mol for moles, g for mass.",
        ],
        "example": {
            "question": "Calculate the moles in 60 g of NaOH. (Mᵣ = 40)",
            "steps": [
                {"label":"Use n = m ÷ Mᵣ","content":"<p>n = 60 ÷ 40</p>"},
                {"label":"Check","content":"<p>60 is one and a half lots of 40.</p>"},
                {"label":"Answer","content":"<p><strong>1.5 mol</strong></p>","isAnswer":True,"is_answer":True},
            ],
        },
    },
    "silver": {
        "title": "Silver: convert or use the ratio",
        "steps": [
            "Two moves may appear. <strong>Convert first</strong>: cm³ to dm³ by dividing by 1000 before n = c × V.",
            "Or <strong>cross substances</strong>: find moles of the known, then use the balanced equation's ratio (often 1:1) for the other.",
            "Finish with m = n × Mᵣ and state the unit.",
        ],
        "example": {
            "question": "CaCO₃ → CaO + CO₂. Mass of CO₂ from 5.0 g of CaCO₃? (Mᵣ: CaCO₃ 100, CO₂ 44)",
            "steps": [
                {"label":"Moles of CaCO₃","content":"<p>n = 5.0 ÷ 100 = 0.05 mol</p>"},
                {"label":"Ratio 1:1, then mass","content":"<p>n(CO₂) = 0.05, m = 0.05 × 44</p>"},
                {"label":"Check","content":"<p>Half the 10 g example, so half of 4.4.</p>"},
                {"label":"Answer","content":"<p><strong>2.2 g</strong></p>","isAnswer":True,"is_answer":True},
            ],
        },
    },
    "gold": {
        "title": "Gold: multi-step with a real ratio",
        "steps": [
            "Chain the steps. Find moles of the known with n = m ÷ Mᵣ or n = c × V.",
            "Apply the balanced equation's ratio when it is <strong>not</strong> 1:1: a 1:2 ratio doubles the moles.",
            "Convert back to mass or concentration, then check the answer looks sensible.",
        ],
        "example": {
            "question": "N₂ + 3H₂ → 2NH₃. Mass of NH₃ from 14 g of N₂? (Mᵣ: N₂ 28, NH₃ 17)",
            "steps": [
                {"label":"Moles of N₂","content":"<p>n = 14 ÷ 28 = 0.5 mol</p>"},
                {"label":"Ratio 1:2","content":"<p>n(NH₃) = 0.5 × 2 = 1.0 mol</p>"},
                {"label":"Check","content":"<p>Half the 28 g example, so half of 34.</p>"},
                {"label":"Answer","content":"<p><strong>17 g</strong></p>","isAnswer":True,"is_answer":True},
            ],
        },
    },
}

# ---------------- guided (opener + teach) ----------------
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "One 5p coin weighs 3 g.<br>A whole bag of these coins weighs 60 g.",
        "steps": [
            {"say":"A coin puzzle. No chemistry, just weighing. You cannot count the coins one by one, so use the scales.",
             "pre":"How many coins are in the bag?","post":"","answer":20,
             "hint":"How many 3 g coins fit into 60 g? Divide."},
            {"say":"You divided the total mass by the mass of one coin. Try it once more.",
             "pre":"If instead each coin weighed 4 g and the bag still weighed 60 g, how many coins?","post":"","answer":15,
             "hint":"60 ÷ 4."},
            {"say":"That is exactly how chemists count atoms: by weighing. The <strong>Mᵣ</strong> is the mass of one 'coin' (one mole), the mass is what you weigh, and <strong>moles = mass ÷ Mᵣ</strong>. Counting particles you can never see, just with a balance."},
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "Calculate the moles in 8.0 g of methane, CH₄. (Aᵣ: C = 12, H = 1)",
            "steps": [
                {"say":"First build Mᵣ by counting atoms.","pre":"Carbon: 1 × 12 = ","post":"","answer":12,"hint":"One C atom."},
                {"pre":"Hydrogen: 4 × 1 = ","post":"","answer":4,"hint":"Four H atoms."},
                {"pre":"Mᵣ(CH₄) = 12 + 4 = ","post":"","answer":16,"hint":"Add the parts."},
                {"say":"Now use n = m ÷ Mᵣ.","pre":"8.0 ÷ 16 = ","post":"","answer":0.5,"done":"That is the whole bronze move: weigh, divide by Mᵣ.","hint":"8 is half of 16."},
                {"pre":"Check: 0.5 mol should weigh half of 16, so 0.5 × 16 = ","post":"","answer":8,"done":"Matches the 8.0 g given.","hint":"moles × Mᵣ."},
            ],
        },
        "silver": {
            "label": "Together: adding the ratio",
            "display": "2Mg + O₂ → 2MgO. Calculate the mass of MgO from 6.0 g of magnesium. (Aᵣ: Mg = 24, O = 16)",
            "steps": [
                {"say":"Find the moles of the known substance first.","pre":"Moles of Mg = 6.0 ÷ 24 = ","post":"","answer":0.25,"hint":"mass ÷ Aᵣ."},
                {"say":"The equation is 2Mg : 2MgO, which is 1 : 1, so the moles carry across.","pre":"Moles of MgO = ","post":"","answer":0.25,"hint":"Same as the Mg."},
                {"pre":"Mᵣ(MgO) = 24 + 16 = ","post":"","answer":40,"hint":"Add Mg and O."},
                {"pre":"Mass of MgO = 0.25 × 40 = ","post":"","answer":10,"done":"That is the new move: cross substances with the equation's ratio.","hint":"moles × Mᵣ."},
                {"pre":"Check: oxygen added = 10 − 6 = ","post":"","answer":4,"done":"0.125 mol of O₂ is 4 g, and 6 + 4 = 10 g. Conserved.","hint":"Subtract the metal mass."},
            ],
        },
        "gold": {
            "label": "Together: a ratio that is not 1:1",
            "display": "CH₄ + 2O₂ → CO₂ + 2H₂O. Calculate the mass of water formed from 8.0 g of methane. (Aᵣ: C = 12, H = 1, O = 16)",
            "steps": [
                {"pre":"Mᵣ(CH₄) = 12 + 4 = ","post":"","answer":16,"hint":"One C and four H."},
                {"pre":"Moles of CH₄ = 8.0 ÷ 16 = ","post":"","answer":0.5,"hint":"mass ÷ Mᵣ."},
                {"say":"Ratio CH₄ : H₂O = 1 : 2, so double the moles.","pre":"Moles of H₂O = 0.5 × 2 = ","post":"","answer":1.0,"hint":"Two water molecules per methane."},
                {"pre":"Mᵣ(H₂O) = 2 + 16 = ","post":"","answer":18,"hint":"Two H and one O."},
                {"pre":"Mass of water = 1.0 × 18 = ","post":"","answer":18,"done":"The 1:2 ratio doubled the moles. That is the gold move.","hint":"moles × Mᵣ."},
            ],
        },
    },
}

# ---------------- em-dash cleanup on preserved fields ----------------
pd["exam_context"]["paper"] = pd["exam_context"]["paper"].replace(" — ", ": ").replace("—", ": ")
pd["exam_context"]["frequency"] = pd["exam_context"]["frequency"].replace(" — ", ". ").replace("—", ". ")
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ": ")

def words(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card content words:", words(pd["method_card"]["content"]))
for t in ("bronze","silver","gold"):
    print(t, "tier_guide steps words:", sum(words(s) for s in pd["tier_guides"][t]["steps"]))

io.open("lesson_higher-calculations-L01@0e4807bb9f.json","w",encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("WROTE shard")
