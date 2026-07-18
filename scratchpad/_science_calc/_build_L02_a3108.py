# -*- coding: utf-8 -*-
import json, io

CANON_ID = 'fee04afb-d041-4b63-8f67-73da3b882d74'
allrows = json.load(io.open('_pre_dump_all.json', encoding='utf-8'))
pd = [r for r in allrows if r['id'] == CANON_ID][0]['pd']
pb = pd['problem_bank']

pd['exam_context'] = {
    "marks": "3 to 5 per calculation",
    "paper": "Paper 1 (Chemistry) or Paper 2 (Chemistry)",
    "frequency": "High: atom economy and gas volumes are common higher chemistry calculations"
}

pd['method_card']['title'] = "Gas Volumes and Atom Economy"
pd['method_card']['steps'] = [
    "Identify which calculation: gas volume, atom economy, or percentage yield",
    "For a gas volume: find moles of the gas from the equation, then multiply by 24",
    "For atom economy: Mr of desired product ÷ Mr of ALL products × 100",
    "For yield: actual ÷ theoretical × 100, and state the unit"
]
pd['method_card']['content'] = (
    "<p>Three calculations, three different questions.</p>"
    "<p><strong>Gas volume at RTP:</strong> one mole of any gas fills 24 dm³. "
    "Multiply moles by 24 for the volume, or divide by 24 to get moles.</p>"
    "<p><strong>Atom economy</strong> is about the equation: the fraction of the "
    "product mass that is the substance you want, "
    "\\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\). "
    "Multiply each product's Mr by its coefficient first.</p>"
    "<p><strong>Percentage yield</strong> is about the experiment: "
    "\\(\\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\), always below 100%.</p>"
    "<p>Check whether your board gives you the molar volume or expects you to recall it.</p>"
)

pb['bronze_description'] = ("One equation, values already in the right units: molar volume "
    "(× or ÷ 24), a single atom economy, or a straight percentage yield.")
pb['silver_description'] = ("Two moves: convert mass to moles or apply a mole ratio first, "
    "then find the volume, yield or atom economy.")
pb['gold_description'] = ("Multi-step: chain mass, ratio, volume and a unit conversion, or work "
    "a yield or atom economy from a full balanced equation.")

# FIX duplicate silver solution: S1 (sodium) 2.3 g -> 4.6 g so V = 2.4 dm3
s1 = pb['silver'][1]
assert 'sodium' in s1['display'], s1['display']
s1['display'] = ("4.6 g of sodium reacts with water: 2Na + 2H₂O → 2NaOH + H₂. "
    "Calculate the volume of hydrogen gas produced at RTP in dm³. (Ar: Na = 23)")
s1['solutions'] = [2.4]
s1['misconceptions'][0]['message'] = ("Moles Na = 4.6/23 = 0.2. From equation: 2Na → 1H₂, "
    "so moles H₂ = 0.2/2 = 0.1. Volume = 0.1 × 24 = 2.4 dm³.")
s1['misconceptions'][1]['message'] = "2 moles of Na produce 1 mole of H₂. Halve the moles of Na."

HINTS = {
 ('bronze',0): "Multiply the moles by 24, the molar volume at RTP.",
 ('bronze',1): "Divide the volume by 24 to get moles.",
 ('bronze',2): "Multiply the moles by 24.",
 ('bronze',3): "Add both product Mr for the denominator, then divide the desired Mr and times 100.",
 ('bronze',4): "Only one product means every atom ends up in it.",
 ('bronze',5): "Actual over theoretical, times 100.",
 ('bronze',6): "Use the equation ratio to get moles of O₂ first, then times 24.",
 ('bronze',7): "Divide the volume by 24.",
 ('silver',0): "Mass to moles, then the 1:1 ratio, then times 24.",
 ('silver',1): "Mass to moles, halve for the 2:1 ratio, then times 24.",
 ('silver',2): "Mass to moles, 1:1 ratio, then times 24.",
 ('silver',3): "Find theoretical mass of Fe first, then actual over theoretical times 100.",
 ('silver',4): "Multiply each product Mr by its coefficient before adding.",
 ('silver',5): "Only one product, so atom economy is 100%.",
 ('gold',0): "Theoretical volume in cm³ first, then actual over theoretical times 100.",
 ('gold',1): "Add both Route B product Mr, then desired over total times 100.",
 ('gold',2): "Mass to moles, apply the 1:3 ratio, then times 24.",
 ('gold',3): "Find Mr, then moles, then the 2:3 ratio, then times 24.",
 ('gold',4): "Theoretical volume of CO₂ in cm³ first, then actual over theoretical times 100.",
 ('gold',5): "Multiply each product Mr by its coefficient before adding.",
}
EXPECTS = {
 ('bronze',0): [None], ('bronze',1): [115.2], ('bronze',2): [None], ('bronze',3): [None],
 ('bronze',4): [None], ('bronze',5): [133.33], ('bronze',6): [2.4], ('bronze',7): [None, 172.8],
 ('silver',0): [0.05], ('silver',1): [4.8, None], ('silver',2): [0.025], ('silver',3): [None, 160],
 ('silver',4): [None, 56], ('silver',5): [None],
 ('gold',0): [None, 80000], ('gold',1): [56, None], ('gold',2): [4.8, None], ('gold',3): [None, 2.4],
 ('gold',4): [None, 84000], ('gold',5): [30.0, None],
}
for tier in ('bronze','silver','gold'):
    for i, p in enumerate(pb[tier]):
        p['hint'] = HINTS[(tier,i)]
        exps = EXPECTS[(tier,i)]
        ms = p.get('misconceptions') or []
        assert len(ms) == len(exps), (tier, i, len(ms), len(exps))
        for m, e in zip(ms, exps):
            m['expect'] = e

def box(pre, answer, hint, **kw):
    d = {"pre": pre, "answer": answer, "hint": hint}; d.update(kw); return d
def say(s):
    return {"say": s}

GS = {}
GS[('bronze',0)] = [
 say("At RTP, one mole of any gas fills 24 dm³, whatever the gas. \\(V = \\text{moles} \\times 24\\)."),
 box("Write the molar volume at RTP, in dm³: ", 24, "One mole of any gas fills this many dm³ at RTP."),
 box("Substitute the moles: 0.5 × 24 = ", 12, "Multiply the number of moles by 24.", phase="substitute"),
 box("Check by halving: 24 ÷ 2 = ", 12, "Half of 24.", done="Matches. Half a mole fills half of 24 dm³, so the volume is 12 dm³."),
]
GS[('bronze',1)] = [
 say("Turn the equation around: \\(\\text{moles} = \\frac{V}{24}\\)."),
 box("Write the molar volume at RTP, in dm³: ", 24, "Divide by this to go from volume to moles."),
 box("Substitute: moles = 4.8 ÷ 24 = ", 0.2, "Divide the volume by 24.", phase="substitute"),
 box("Check: 0.2 × 24 = ", 4.8, "Multiply your moles back by 24.", done="Back to 4.8 dm³, so 0.2 mol is right."),
]
GS[('bronze',2)] = [
 say("At RTP, one mole of any gas fills 24 dm³. \\(V = \\text{moles} \\times 24\\)."),
 box("Write the molar volume at RTP, in dm³: ", 24, "One mole of any gas at RTP."),
 box("Substitute: volume = 2 × 24 = ", 48, "Multiply the moles by 24.", phase="substitute"),
 box("Check: 48 ÷ 24 should give the moles back: 48 ÷ 24 = ", 2, "Divide the volume by 24.", done="Two moles, exactly what we started with, so 48 dm³ is right."),
]
GS[('bronze',3)] = [
 say("Atom economy is the fraction of the product mass that is the bit you want. \\(\\text{AE} = \\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\)."),
 box("Add the Mr of all products: 56 + 44 = ", 100, "Add both product Mr values."),
 box("The desired product (CaO) has Mr 56. Atom economy = (56 ÷ 100) × 100 = ", 56, "Divide 56 by the total, then times 100.", phase="substitute"),
 box("Check: the waste CO₂ is 44 out of 100, so 44%. Useful plus waste: 56 + 44 = ", 100, "Add the useful percent and the waste percent.", done="They add to 100%, so an atom economy of 56% is right."),
]
GS[('bronze',4)] = [
 say("Atom economy: \\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\). Count the products first."),
 box("How many different products in 2Mg + O₂ → 2MgO? ", 1, "Look to the right of the arrow."),
 box("With only one product, every atom ends up in it, so atom economy = ", 100, "One product means no waste.", phase="substitute"),
 box("Check: the waste is 0%, so useful = 100 − 0 = ", 100, "100 minus the waste percent.", done="No waste product, so the atom economy is 100%."),
]
GS[('bronze',5)] = [
 say("Percentage yield compares what you got to what you could have got. \\(\\%\\text{ yield} = \\frac{\\text{actual}}{\\text{theoretical}} \\times 100\\)."),
 box("Write the theoretical (expected) mass, in g: ", 10, "The mass you expected to make."),
 box("Yield = (7.5 ÷ 10) × 100 = ", 75, "Divide actual by theoretical, then times 100.", phase="substitute"),
 box("Check: 75% of 10 g = 0.75 × 10 = ", 7.5, "Multiply 10 by 0.75.", done="That equals the 7.5 g actually made, so 75% is right."),
]
GS[('bronze',6)] = [
 say("First the ratio, then the volume. From 2H₂O₂ → 2H₂O + O₂, two moles of H₂O₂ make one mole of O₂."),
 box("Moles of O₂ from 0.1 mol H₂O₂: 0.1 ÷ 2 = ", 0.05, "Two H₂O₂ make one O₂, so halve."),
 box("Now the volume: 0.05 × 24 = ", 1.2, "Multiply the moles of gas by 24.", phase="substitute"),
 box("Check: 1.2 ÷ 24 = ", 0.05, "Divide the volume by 24.", done="Back to 0.05 mol of O₂, so 1.2 dm³ is right."),
]
GS[('bronze',7)] = [
 say("Turn the equation around: \\(\\text{moles} = \\frac{V}{24}\\)."),
 box("Write the molar volume at RTP, in dm³: ", 24, "Divide by this."),
 box("Substitute: moles = 7.2 ÷ 24 = ", 0.3, "Divide 7.2 by 24.", phase="substitute"),
 box("Check: 0.3 × 24 = ", 7.2, "Multiply back by 24.", done="Back to 7.2 dm³, so 0.3 mol is right."),
]
GS[('silver',0)] = [
 say("Three moves: mass to moles, ratio, then volume. \\(n = \\frac{\\text{mass}}{M_r}\\)."),
 box("Moles of CaCO₃: 5.0 ÷ 100 = ", 0.05, "Divide the mass by the Mr."),
 box("Ratio CaCO₃ : CO₂ is 1 : 1, so moles of CO₂ = ", 0.05, "Same number of moles, the ratio is one to one."),
 box("Volume of CO₂: 0.05 × 24 = ", 1.2, "Multiply the moles of gas by 24.", phase="substitute"),
 box("Check: 1.2 ÷ 24 = ", 0.05, "Divide by 24.", done="Back to 0.05 mol, so 1.2 dm³ of CO₂ is right."),
]
GS[('silver',1)] = [
 say("Mass to moles, then halve for the ratio, then volume."),
 box("Moles of Na: 4.6 ÷ 23 = ", 0.2, "Divide the mass by the Ar."),
 box("Ratio 2Na : 1H₂, so moles of H₂ = 0.2 ÷ 2 = ", 0.1, "Two sodiums make one hydrogen molecule, so halve."),
 box("Volume of H₂: 0.1 × 24 = ", 2.4, "Multiply the moles of gas by 24.", phase="substitute"),
 box("Check: 2.4 ÷ 24 = ", 0.1, "Divide the volume by 24.", done="Back to 0.1 mol of H₂, so 2.4 dm³ is right."),
]
GS[('silver',2)] = [
 say("Mass to moles, then volume. Ratio Mg : H₂ is 1 : 1."),
 box("Moles of Mg: 0.6 ÷ 24 = ", 0.025, "Divide the mass by the Ar."),
 box("Ratio 1 : 1, so moles of H₂ = ", 0.025, "Same number of moles."),
 box("Volume of H₂: 0.025 × 24 = ", 0.6, "Multiply moles by 24.", phase="substitute"),
 box("Check: 0.6 ÷ 24 = ", 0.025, "Divide by 24.", done="Back to 0.025 mol, so 0.6 dm³ of H₂ is right."),
]
GS[('silver',3)] = [
 say("Yield needs the theoretical mass first. Mass to moles, ratio, moles to mass, then compare."),
 box("Moles of Fe₂O₃: 10 ÷ 160 = ", 0.0625, "Divide the mass by the Mr."),
 box("Ratio 2Fe₂O₃ : 4Fe is 1 : 2, so moles of Fe = 0.0625 × 2 = ", 0.125, "Double the moles."),
 box("Theoretical mass of Fe: 0.125 × 56 = ", 7, "Moles times Ar."),
 box("Yield = (5.6 ÷ 7) × 100 = ", 80, "Actual over theoretical, times 100.", phase="substitute"),
 box("Check: 80% of 7 g = 0.8 × 7 = ", 5.6, "Multiply 7 by 0.8.", done="That equals the 5.6 g obtained, so 80% is right."),
]
GS[('silver',4)] = [
 say("Watch the coefficients. The desired product is 2Fe, and the products are 2Fe and 3CO₂."),
 box("Mr of 2Fe = 2 × 56 = ", 112, "Two irons."),
 box("Mr of 3CO₂ = 3 × 44 = ", 132, "Three carbon dioxides."),
 box("Total Mr of products = 112 + 132 = ", 244, "Add the two."),
 box("Atom economy = (112 ÷ 244) × 100 = (to 1 d.p.) ", 45.9, "Desired over total, times 100.", phase="substitute"),
 box("Check: waste 3CO₂ is about 54.1%. Useful plus waste = 45.9 + 54.1 = ", 100, "Add the useful and waste percentages.", done="They add to 100%, so 45.9% is right."),
]
GS[('silver',5)] = [
 say("Only one product here, so no atoms are wasted."),
 box("How many different products in N₂ + 3H₂ → 2NH₃? ", 1, "Look to the right of the arrow."),
 box("Mr of the desired product NH₃ = 14 + (3 × 1) = ", 17, "N is 14, three H are 3."),
 box("With only NH₃ as product, atom economy = (17 ÷ 17) × 100 = ", 100, "Desired over total; they are the same.", phase="substitute"),
 box("Check: waste mass = 0, so useful = 100 − 0 = ", 100, "100 minus 0.", done="One product means 100% atom economy."),
]
GS[('gold',0)] = [
 say("A yield with a gas: find the theoretical volume, match the units, then compare. Ratio Zn : H₂ is 1 : 1."),
 box("Moles of Zn: 3.25 ÷ 65 = ", 0.05, "Divide the mass by the Ar."),
 box("Ratio 1 : 1, so theoretical moles of H₂ = ", 0.05, "Same number of moles."),
 box("Theoretical volume in dm³: 0.05 × 24 = ", 1.2, "Moles of gas times 24."),
 box("The collected gas is in cm³, so convert: 1.2 × 1000 = ", 1200, "1 dm³ = 1000 cm³."),
 box("Yield = (960 ÷ 1200) × 100 = ", 80, "Actual over theoretical, times 100.", phase="substitute"),
 box("Check: 80% of 1200 cm³ = 0.8 × 1200 = ", 960, "Multiply 1200 by 0.8.", done="That equals the 960 cm³ collected, so 80% is right."),
]
GS[('gold',1)] = [
 say("Route B only. The products are CaO and H₂O."),
 box("Mr of all products (Route B): 56 + 18 = ", 74, "Add the two product Mr values."),
 box("The desired product CaO has Mr = ", 56, "Given in the data."),
 box("Atom economy = (56 ÷ 74) × 100 = (to 1 d.p.) ", 75.7, "Desired over total, times 100.", phase="substitute"),
 box("Check: waste H₂O is about 24.3%. Useful plus waste = 75.7 + 24.3 = ", 100, "Add useful and waste percentages.", done="They total 100%, so Route B is 75.7%."),
]
GS[('gold',2)] = [
 say("Mass to moles, then the 1 : 3 ratio to CO₂, then volume."),
 box("Moles of Fe₂O₃: 32 ÷ 160 = ", 0.2, "Divide the mass by the Mr."),
 box("Ratio 1 Fe₂O₃ : 3 CO₂, so moles of CO₂ = 0.2 × 3 = ", 0.6, "Multiply by 3."),
 box("Volume of CO₂: 0.6 × 24 = ", 14.4, "Moles of gas times 24.", phase="substitute"),
 box("Check: 14.4 ÷ 24 = ", 0.6, "Divide by 24.", done="Back to 0.6 mol of CO₂, so 14.4 dm³ is right."),
]
GS[('gold',3)] = [
 say("Find Mr, then moles, then the 2 : 3 ratio, then volume."),
 box("Mr of KClO₃ = 39 + 35.5 + (3 × 16) = ", 122.5, "Add K, Cl and three O."),
 box("Moles of KClO₃: 12.25 ÷ 122.5 = ", 0.1, "Divide the mass by the Mr."),
 box("Ratio 2KClO₃ : 3O₂, so moles of O₂ = 0.1 × 3 ÷ 2 = ", 0.15, "Times 3, divided by 2."),
 box("Volume of O₂: 0.15 × 24 = ", 3.6, "Moles of gas times 24.", phase="substitute"),
 box("Check: 3.6 ÷ 24 = ", 0.15, "Divide by 24.", done="Back to 0.15 mol of O₂, so 3.6 dm³ is right."),
]
GS[('gold',4)] = [
 say("Theoretical volume of CO₂ first, then match units, then compare. Ratio CaCO₃ : CO₂ is 1 : 1."),
 box("Moles of CaCO₃: 2.5 ÷ 100 = ", 0.025, "Divide the mass by the Mr."),
 box("Ratio 1 : 1, so theoretical moles of CO₂ = ", 0.025, "Same number of moles."),
 box("Theoretical volume in dm³: 0.025 × 24 = ", 0.6, "Moles times 24."),
 box("Convert to cm³: 0.6 × 1000 = ", 600, "1 dm³ = 1000 cm³."),
 box("Yield = (504 ÷ 600) × 100 = ", 84, "Actual over theoretical, times 100.", phase="substitute"),
 box("Check: 84% of 600 cm³ = 0.84 × 600 = ", 504, "Multiply 600 by 0.84.", done="That equals the 504 cm³ collected, so 84% is right."),
]
GS[('gold',5)] = [
 say("The desired product is 3O₂. Use the coefficients on every product."),
 box("Mr of 3O₂ = 3 × 32 = ", 96, "Three oxygen molecules, each 32."),
 box("Mr of 2KCl = 2 × 74.5 = ", 149, "Two KCl, each 74.5."),
 box("Total Mr of products = 96 + 149 = ", 245, "Add the two."),
 box("Atom economy = (96 ÷ 245) × 100 = (to 1 d.p.) ", 39.2, "Desired over total, times 100.", phase="substitute"),
 box("Check: waste 2KCl is about 60.8%. Useful plus waste = 39.2 + 60.8 = ", 100, "Add useful and waste percentages.", done="They total 100%, so 39.2% is right."),
]
for tier in ('bronze','silver','gold'):
    for i, p in enumerate(pb[tier]):
        p['guided_steps'] = GS[(tier,i)]

def exstep(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d
pd['tier_guides'] = {
 "bronze": {
  "title": "Bronze: one equation, straight in",
  "steps": [
    "For a gas at RTP, one mole fills 24 dm³. Multiply moles by 24 for the volume; divide volume by 24 for the moles.",
    "Atom economy = <strong>Mr of the product you want ÷ Mr of all products × 100</strong>. Percentage yield = <strong>actual ÷ theoretical × 100</strong>.",
    "Always finish with the unit: dm³, mol, or %."
  ],
  "example": {
    "question": "Calculate the volume of 0.25 mol of carbon dioxide at RTP, in dm³.",
    "steps": [
      exstep("Equation", "<p>\\(V = \\text{moles} \\times 24\\)</p>"),
      exstep("Substitute", "<p>V = 0.25 × 24</p>"),
      exstep("Check", "<p>6 ÷ 24 = 0.25 mol, back to the start</p>"),
      exstep("Answer", "<p><strong>6 dm³</strong></p>", True),
    ]
  }
 },
 "silver": {
  "title": "Silver: convert first, then solve",
  "steps": [
    "Turn grams into moles before anything else: \\(n = \\frac{\\text{mass}}{M_r}\\).",
    "Then use the balanced equation's ratio to get the moles of the substance you actually want.",
    "Finish the job: × 24 for a gas volume, or × Ar for a mass, then state the unit."
  ],
  "example": {
    "question": "4.0 g of calcium reacts fully with water: Ca + 2H₂O → Ca(OH)₂ + H₂. Find the volume of H₂ at RTP, in dm³. (Ar: Ca = 40)",
    "steps": [
      exstep("Mass to moles", "<p>n = 4.0 ÷ 40 = 0.1 mol</p>"),
      exstep("Ratio", "<p>Ca : H₂ = 1 : 1, so 0.1 mol H₂</p>"),
      exstep("Volume", "<p>V = 0.1 × 24</p>"),
      exstep("Answer", "<p><strong>2.4 dm³</strong></p>", True),
    ]
  }
 },
 "gold": {
  "title": "Gold: chain the whole method",
  "steps": [
    "For yield: find the theoretical amount from the equation, match units (1 dm³ = 1000 cm³), then <strong>actual ÷ theoretical × 100</strong>.",
    "For atom economy from a balanced equation, multiply every product's Mr by its coefficient before adding them up.",
    "Keep each stage separate so one slip does not sink the rest."
  ],
  "example": {
    "question": "16 g of copper(II) oxide is reduced: 2CuO + C → 2Cu + CO₂. Find the volume of CO₂ at RTP, in dm³. (Mr: CuO = 80)",
    "steps": [
      exstep("Mass to moles", "<p>n = 16 ÷ 80 = 0.2 mol CuO</p>"),
      exstep("Ratio", "<p>2CuO : 1CO₂, so 0.1 mol CO₂</p>"),
      exstep("Volume", "<p>V = 0.1 × 24</p>"),
      exstep("Answer", "<p><strong>2.4 dm³</strong></p>", True),
    ]
  }
 }
}

pd['guided'] = {
 "opener": {
  "display": ("You buy 100 g of oranges to make juice.<br>When you squeeze them you get "
     "40 g of juice. The other 60 g is peel and pith, which you throw away."),
  "steps": [
    box("What percentage of the 100 g became juice? ", 40, "40 out of 100 is what percent?"),
    say("Now a bigger bag: 120 g of oranges gives 30 g of juice."),
    box("What percentage is juice this time? 30 ÷ 120 × 100 = ", 25, "30 out of 120."),
    say("That fraction, the useful stuff out of everything that came out, is exactly "
        "<strong>atom economy</strong>. In a reaction it is "
        "\\(\\frac{M_r\\text{ of the product you want}}{M_r\\text{ of all products}} \\times 100\\): "
        "of all the atoms produced, what share ends up in the product you actually wanted."),
  ]
 },
 "teach": {
  "bronze": {
    "display": ("In the thermal decomposition CuCO₃ → CuO + CO₂ the desired product is "
       "copper oxide. Calculate the atom economy. (Mr: CuO = 80, CO₂ = 44)"),
    "steps": [
      say("Atom economy = \\(\\frac{M_r\\text{ desired}}{M_r\\text{ all products}} \\times 100\\). Both products count."),
      box("Mr of the desired product CuO = ", 80, "Given in the data."),
      box("Mr of the other product CO₂ = ", 44, "Given in the data."),
      box("Total Mr of all products = 80 + 44 = ", 124, "Add both."),
      box("Atom economy = (80 ÷ 124) × 100 = (to 1 d.p.) ", 64.5, "Desired over total, times 100.",
          done="So 64.5% of the mass is useful; the CO₂ carries the rest away."),
    ]
  },
  "silver": {
    "display": ("4.0 g of calcium reacts fully with water: Ca + 2H₂O → Ca(OH)₂ + H₂. "
       "Calculate the volume of hydrogen produced at RTP, in dm³. (Ar: Ca = 40)"),
    "steps": [
      say("Mass to moles first: \\(n = \\frac{\\text{mass}}{M_r}\\)."),
      box("Moles of Ca: 4.0 ÷ 40 = ", 0.1, "Divide mass by Ar."),
      box("Ratio Ca : H₂ is 1 : 1, so moles of H₂ = ", 0.1, "One to one."),
      box("Volume of H₂: 0.1 × 24 = ", 2.4, "Moles times 24."),
      box("Check: 2.4 ÷ 24 = ", 0.1, "Divide back by 24.", done="Back to 0.1 mol, so 2.4 dm³ is right."),
    ]
  },
  "gold": {
    "display": ("6.5 g of zinc reacts with excess sulfuric acid: Zn + H₂SO₄ → ZnSO₄ + H₂. "
       "The student collects 1800 cm³ of hydrogen at RTP. Calculate the percentage yield. (Ar: Zn = 65)"),
    "steps": [
      say("A yield with a gas: find the theoretical volume, match the units, then compare."),
      box("Moles of Zn: 6.5 ÷ 65 = ", 0.1, "Mass over Ar."),
      box("Ratio 1 : 1, so theoretical moles of H₂ = ", 0.1, "One to one."),
      box("Theoretical volume in dm³: 0.1 × 24 = ", 2.4, "Moles times 24."),
      box("Convert to cm³: 2.4 × 1000 = ", 2400, "1 dm³ = 1000 cm³."),
      box("Yield = (1800 ÷ 2400) × 100 = ", 75, "Actual over theoretical, times 100.",
          done="75% collected; some hydrogen escaped before it was measured."),
    ]
  }
 }
}

# preserved worked_examples use em dashes in step labels: convert to colons (style rule)
for we in pd.get('worked_examples', []):
    for st in we.get('steps', []):
        if 'label' in st and '—' in st['label']:
            st['label'] = st['label'].replace(' — ', ': ').replace('—', ':')

# final safety: assert no em dash anywhere student-facing
def _scan(o, p, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('note', 'guided_skip_reason'): continue
            _scan(v, p + '.' + str(k), out)
    elif isinstance(o, list):
        for i, v in enumerate(o): _scan(v, p + '[%d]' % i, out)
    elif isinstance(o, str) and '—' in o:
        out.append(p)
_e = []; _scan(pd, 'pd', _e)
assert not _e, ('EM DASH remains: ' + str(_e))

OUT = 'lesson_higher-calculations-L02@a3108b4601.json'
json.dump(pd, io.open(OUT,'w',encoding='utf-8'), indent=1, ensure_ascii=False)
print("built OK ->", OUT)
