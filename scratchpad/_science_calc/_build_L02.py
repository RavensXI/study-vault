# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_canonical_fetch.json", encoding="utf-8"))

# ---------------------------------------------------------------- method_card
pd["method_card"]["content"] = (
 "<p>Three calculations that test different ideas.</p>"
 "<p><strong>Gas volume at RTP:</strong> one mole of any gas occupies 24 dm³ "
 "(24,000 cm³). Volume = moles × 24; moles = volume ÷ 24.</p>"
 "<p><strong>Atom economy</strong> is about the balanced equation: Mr of the desired "
 "product ÷ Mr of all products × 100. Use product Mr values, never reactants, "
 "and include the coefficients.</p>"
 "<p><strong>Percentage yield</strong> is about the experiment: actual ÷ theoretical "
 "× 100. It is always below 100% because of losses and side reactions.</p>"
)

# ---------------------------------------------------------------- tier descriptions
pb = pd["problem_bank"]
pb["bronze_description"] = ("One equation with values already in the right units: molar "
 "volume, or atom economy where there is a single desired product.")
pb["silver_description"] = ("Convert a mass to moles, or use the equation's ratio, before "
 "the gas law, in one clean chain.")
pb["gold_description"] = ("Multi-step problems: a theoretical amount then percentage yield, "
 "unit conversions (dm³ to cm³), or atom economy with coefficients.")

# ---------------------------------------------------------------- helpers
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post: d["post"] = post
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(text): return {"say": text}

# ---------------------------------------------------------------- guided.opener
pd["guided"] = {"opener": {"steps": [
    say("A sweets factory melts 100 g of mixture in a tray. Out of every 100 g, 75 g sets "
        "into the sweet they sell and 25 g stays stuck to the tray as waste."),
    box("Out of 100 g of product, what percentage is the sweet you actually want? ", 75,
        "75 out of 100 is what percentage?", post="%"),
    say("You just found the <strong>atom economy</strong>: the share of the total product "
        "that is the thing you want. In a reaction the masses come from the balanced equation "
        "(the \\(M_r\\) of each product), but the idea is identical: desired ÷ all products × 100."),
    box("Now gases. One mole of any gas at RTP fills 24 dm³, like identical balloons. "
        "Three moles fill ", 72, "Three lots of 24.", post=" dm³"),
    say("That is <strong>molar volume</strong>: volume = moles × 24. Two ideas, both just "
        "scaling and sharing, and that is the whole lesson."),
]}}

# ---------------------------------------------------------------- guided.teach
pd["guided"]["teach"] = {
 "bronze": {
   "display": "Calculate the volume of 0.25 mol of carbon dioxide at RTP, in dm³.",
   "steps": [
     say("Molar volume: at RTP one mole of any gas fills 24 dm³, so volume = moles × 24."),
     box("moles of gas = ", 0.25, "It is given in the question."),
     box("the molar volume in dm³ = ", 24, "One mole of any gas at RTP fills this."),
     box("now multiply: 0.25 × 24 = ", 6, "A quarter of 24."),
     box("Check: 24 ÷ 6 = ", 4, "Divide the molar volume by your answer.",
         done="0.25 mol is a quarter of a mole, so a quarter of 24 dm³. State it as 6 dm³."),
   ]},
 "silver": {
   "display": "8.0 g of methane, CH₄, burns completely: CH₄ + 2O₂ → CO₂ + 2H₂O. "
              "Calculate the volume of CO₂ produced at RTP, in dm³. (Mr: CH₄ = 16)",
   "steps": [
     say("Mass is given, so find moles first, then use the ratio, then \\(V = n \\times 24\\)."),
     box("moles CH₄ = 8.0 ÷ 16 = ", 0.5, "Mass over Mr."),
     say("The ratio CH₄ : CO₂ is 1 : 1."),
     box("moles CO₂ = ", 0.5, "Same as the moles of CH₄."),
     box("volume = 0.5 × 24 = ", 12, "Half of 24."),
     box("Check: 12 ÷ 24 = ", 0.5, "Divide back by the molar volume.",
         done="Returns 0.5 mol, so the volume of CO₂ is 12 dm³."),
   ]},
 "gold": {
   "display": "4.0 g of calcium carbonate is heated: CaCO₃ → CaO + CO₂. The student "
              "collects 720 cm³ of CO₂ at RTP. Calculate the percentage yield. (Mr: CaCO₃ = 100)",
   "steps": [
     say("Plan: find the theoretical volume of CO₂, convert it to cm³, then compare with the 720 cm³ collected."),
     box("moles CaCO₃ = 4.0 ÷ 100 = ", 0.04, "Mass over Mr."),
     box("moles CO₂ (ratio 1 : 1) = ", 0.04, "Same as CaCO₃."),
     box("theoretical volume in dm³ = 0.04 × 24 = ", 0.96, "0.04 lots of 24."),
     box("convert to cm³ to match the data: 0.96 × 1000 = ", 960, "1 dm³ = 1000 cm³."),
     box("yield = (720 ÷ 960) × 100 = ", 75, "720 over 960, times 100."),
     box("Check: 75% of 960 = 0.75 × 960 = ", 720, "Take 75% of the theoretical volume.",
         done="Matches the 720 cm³ collected, so the percentage yield is 75%."),
   ]},
}

# ---------------------------------------------------------------- tier_guides
def ex_step(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one gas-law step",
   "steps": [
     "<strong>Molar volume:</strong> at RTP one mole of any gas fills 24 dm³. Volume = moles × 24; moles = volume ÷ 24.",
     "<strong>Atom economy</strong> for a single desired product = \\(M_r\\) of that product ÷ \\(M_r\\) of all products × 100.",
     "Values arrive ready to use. Pick the equation, substitute, then state the unit (dm³, mol or %).",
   ],
   "example": {"question": "Calculate the volume of 3 mol of nitrogen gas at RTP, in dm³.",
     "steps": [ex_step("Equation", "<p>volume = moles × 24</p>"),
               ex_step("Substitute", "<p>volume = 3 × 24</p>"),
               ex_step("Check", "<p>72 ÷ 24 = 3 mol ✓</p>"),
               ex_step("Answer", "<p><strong>72 dm³</strong></p>", ans=True)]}},
 "silver": {
   "title": "Silver: convert to moles first",
   "steps": [
     "A mass or a different substance is given, so <strong>find moles first</strong>: moles = mass ÷ \\(M_r\\).",
     "Use the balanced equation's <strong>ratio</strong> to switch to the gas you want, then volume = moles × 24.",
     "For yield, turn moles into a theoretical mass (moles × \\(A_r\\)), then actual ÷ theoretical × 100.",
   ],
   "example": {"question": "6.0 g of carbon burns: C + O₂ → CO₂. Calculate the volume of CO₂ at RTP, in dm³. (Ar: C = 12)",
     "steps": [ex_step("Moles", "<p>moles C = 6 ÷ 12 = 0.5</p>"),
               ex_step("Ratio", "<p>C : CO₂ = 1 : 1, so moles CO₂ = 0.5</p>"),
               ex_step("Volume", "<p>0.5 × 24 = 12</p>"),
               ex_step("Check", "<p>12 ÷ 24 = 0.5 mol ✓</p>"),
               ex_step("Answer", "<p><strong>12 dm³</strong></p>", ans=True)]}},
 "gold": {
   "title": "Gold: two ideas chained",
   "steps": [
     "Multi-step: often a <strong>theoretical amount</strong> then a comparison, so plan the route before you start.",
     "Watch units: molar volume gives dm³, but collected gas is often in cm³. <strong>1 dm³ = 1000 cm³.</strong>",
     "Atom economy needs the <strong>coefficients</strong> in every \\(M_r\\) (2Fe means 2 × 56). Round only at the very end.",
   ],
   "example": {"question": "1.2 g of magnesium reacts with excess HCl: Mg + 2HCl → MgCl₂ + H₂. It gives 960 cm³ of H₂ at RTP. Find the percentage yield. (Ar: Mg = 24)",
     "steps": [ex_step("Moles", "<p>1.2 ÷ 24 = 0.05 mol Mg, so 0.05 mol H₂</p>"),
               ex_step("Theoretical volume", "<p>0.05 × 24 = 1.2 dm³ = 1200 cm³</p>"),
               ex_step("Yield", "<p>(960 ÷ 1200) × 100</p>"),
               ex_step("Check", "<p>0.8 × 1200 = 960 cm³ ✓</p>"),
               ex_step("Answer", "<p><strong>80%</strong></p>", ans=True)]}},
}

# ---------------------------------------------------------------- per-problem: hints, misconceptions(+expect), guided_steps
# helper for a misconception
def mis(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "message": message, "expect": expect}

B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# ---- BRONZE ----
B[0]["hint"] = "Multiply the moles by 24."
B[0]["misconceptions"] = [mis("inverse_error",
  "Multiply by 24, don't divide. Volume = moles × 24 = 0.5 × 24 = 12 dm³.", 0.0208)]
B[0]["guided_steps"] = [
  say("At RTP one mole of any gas fills 24 dm³, so volume = moles × 24."),
  box("moles of gas = ", 0.5, "Read it from the question."),
  box("volume = 0.5 × 24 = ", 12, "Half of 24.", phase="substitute"),
  box("Check: 12 ÷ 24 = ", 0.5, "Divide back by the molar volume.",
      done="Returns our 0.5 mol, so the volume is 12 dm³."),
]

B[1]["hint"] = "Divide the volume by 24."
B[1]["misconceptions"] = [mis("inverse_error",
  "Moles = volume ÷ 24 = 4.8 ÷ 24 = 0.2 mol. Divide, don't multiply.", 115.2)]
B[1]["guided_steps"] = [
  say("Volume is given and moles are wanted, so divide: moles = volume ÷ 24."),
  box("volume in dm³ = ", 4.8, "Read it from the question."),
  box("moles = 4.8 ÷ 24 = ", 0.2, "4.8 over 24.", phase="substitute"),
  box("Check: 0.2 × 24 = ", 4.8, "Multiply back.",
      done="Returns 4.8 dm³, so 0.2 mol is right."),
]

B[2]["hint"] = "Multiply the moles by 24."
B[2]["misconceptions"] = [mis("inverse_error",
  "Volume = moles × 24 = 2 × 24 = 48 dm³. Multiply, don't divide.", 0.0833)]
B[2]["guided_steps"] = [
  say("At RTP volume = moles × 24."),
  box("moles of gas = ", 2, "Read it from the question."),
  box("volume = 2 × 24 = ", 48, "Two lots of 24.", phase="substitute"),
  box("Check: 48 ÷ 24 = ", 2, "Divide back.",
      done="Returns 2 mol, so 48 dm³ is right."),
]

B[3]["hint"] = "Add the two product Mr values for the denominator, then divide 56 by it."
B[3]["misconceptions"] = [mis("wrong_product",
  "The desired product is CaO (Mr 56), not CO₂. Atom economy = 56 ÷ (56 + 44) × 100 = 56%.", 44)]
B[3]["guided_steps"] = [
  say("Atom economy = \\(M_r\\) of desired product ÷ \\(M_r\\) of all products × 100."),
  box("Mr of all products, 56 + 44 = ", 100, "Add both product Mr values."),
  box("atom economy = (56 ÷ 100) × 100 = ", 56, "56 over 100, times 100.", phase="substitute"),
  box("Check: waste CO₂ share = 100 − 56 = ", 44, "Subtract the useful part from 100.",
      done="44 g of every 100 is wasted as CO₂, so atom economy is 56%."),
]

B[4]["hint"] = "With only one product, every atom ends up where you want it."
B[4]["misconceptions"] = [mis("wrong_denominator",
  "O₂ is a reactant, not a product. The only product is MgO, so atom economy = 100%.", 71.43)]
B[4]["guided_steps"] = [
  say("Atom economy = \\(M_r\\) of desired product ÷ \\(M_r\\) of all products × 100."),
  box("How many products are there in 2Mg + O₂ → 2MgO? ", 1, "Count what is right of the arrow."),
  box("With one product every atom is wanted: (all ÷ all) × 100 = ", 100,
      "Anything divided by itself is 1, times 100.", phase="substitute"),
  box("Check: waste = 100 − 100 = ", 0, "Nothing is left over.",
      done="No waste at all, so atom economy is 100%."),
]

B[5]["hint"] = "Put actual over theoretical, then times 100."
B[5]["misconceptions"] = [mis("inverse_error",
  "Yield = actual ÷ theoretical × 100 = (7.5 ÷ 10) × 100 = 75%. Actual goes on top.", 133.33)]
B[5]["guided_steps"] = [
  say("Percentage yield = actual ÷ theoretical × 100."),
  box("theoretical (expected) yield in g = ", 10, "The amount you expected to make."),
  box("yield = (7.5 ÷ 10) × 100 = ", 75, "7.5 over 10, times 100.", phase="substitute"),
  box("Check: 75% of 10 g = 0.75 × 10 = ", 7.5, "Take 75% of the expected amount.",
      done="Matches the 7.5 g actually made, so 75%."),
]

B[6]["hint"] = "Halve the H₂O₂ moles for O₂, then multiply by 24."
B[6]["misconceptions"] = [mis("forgot_ratio",
  "From 2H₂O₂ → 2H₂O + O₂, 2 mol H₂O₂ give 1 mol O₂, so 0.1 mol H₂O₂ gives 0.05 mol O₂. Volume = 0.05 × 24 = 1.2 dm³.", 2.4)]
B[6]["guided_steps"] = [
  say("Use the equation ratio to find moles of O₂, then multiply by 24."),
  box("moles of H₂O₂ per mole of O₂ in 2H₂O₂ → 2H₂O + O₂ = ", 2, "Coefficient of H₂O₂ over coefficient of O₂."),
  box("moles of O₂ = 0.1 ÷ 2 = ", 0.05, "Halve the H₂O₂ moles."),
  box("volume = 0.05 × 24 = ", 1.2, "0.05 lots of 24.", phase="substitute"),
  box("Check: 1.2 ÷ 24 = ", 0.05, "Divide back.",
      done="Returns 0.05 mol O₂, so 1.2 dm³."),
]

B[7]["hint"] = "Divide the volume by 24."
B[7]["misconceptions"] = [mis("inverse_error",
  "Moles = volume ÷ 24 = 7.2 ÷ 24 = 0.3 mol. Divide, don't multiply.", 172.8)]
B[7]["guided_steps"] = [
  say("Moles are wanted from a volume, so divide by 24."),
  box("volume in dm³ = ", 7.2, "Read it from the question."),
  box("moles = 7.2 ÷ 24 = ", 0.3, "7.2 over 24.", phase="substitute"),
  box("Check: 0.3 × 24 = ", 7.2, "Multiply back.",
      done="Returns 7.2 dm³, so 0.3 mol."),
]

# ---- SILVER ----
S[0]["hint"] = "Find moles from the mass, then multiply by 24."
S[0]["misconceptions"] = [mis("forgot_step",
  "Find moles first: 5.0 ÷ 100 = 0.05. Volume = 0.05 × 24 = 1.2 dm³. Do not multiply the mass by 24.", 120)]
S[0]["guided_steps"] = [
  say("Mass is given, so find moles first, then use the 1 : 1 ratio, then multiply by 24."),
  box("moles CaCO₃ = 5.0 ÷ 100 = ", 0.05, "Mass over Mr."),
  box("moles CO₂ (ratio 1 : 1) = ", 0.05, "Same as CaCO₃."),
  box("volume = 0.05 × 24 = ", 1.2, "0.05 lots of 24.", phase="substitute"),
  box("Check: 1.2 ÷ 24 = ", 0.05, "Divide back.",
      done="Returns 0.05 mol, so 1.2 dm³ of CO₂."),
]

S[1]["display"] = ("4.6 g of sodium reacts with water: 2Na + 2H₂O → 2NaOH + H₂. "
  "Calculate the volume of hydrogen gas produced at RTP in dm³. (Ar: Na = 23)")
S[1]["solutions"] = [2.4]
S[1]["hint"] = "Moles of Na, then halve for H₂, then multiply by 24."
S[1]["misconceptions"] = [mis("forgot_ratio",
  "2 mol Na make 1 mol H₂, so halve: moles H₂ = 0.2 ÷ 2 = 0.1. Volume = 0.1 × 24 = 2.4 dm³.", 4.8)]
S[1]["guided_steps"] = [
  say("Find moles of Na, then use the 2 : 1 ratio, then multiply by 24."),
  box("moles Na = 4.6 ÷ 23 = ", 0.2, "Mass over Ar."),
  box("moles H₂ = 0.2 ÷ 2 = ", 0.1, "Two Na make one H₂, so halve."),
  box("volume = 0.1 × 24 = ", 2.4, "0.1 lots of 24.", phase="substitute"),
  box("Check: 2.4 ÷ 24 = ", 0.1, "Divide back.",
      done="Returns 0.1 mol H₂, so 2.4 dm³."),
]

S[2]["hint"] = "Find moles from the mass, ratio 1:1, then multiply by 24."
S[2]["misconceptions"] = [mis("forgot_step",
  "Find moles first: 0.6 ÷ 24 = 0.025. Volume = 0.025 × 24 = 0.6 dm³. Do not multiply the mass by 24.", 14.4)]
S[2]["guided_steps"] = [
  say("Find moles of Mg first, ratio 1 : 1 with H₂, then multiply by 24."),
  box("moles Mg = 0.6 ÷ 24 = ", 0.025, "Mass over Ar."),
  box("moles H₂ (ratio 1 : 1) = ", 0.025, "Same as Mg."),
  box("volume = 0.025 × 24 = ", 0.6, "0.025 lots of 24.", phase="substitute"),
  box("Check: 0.6 ÷ 24 = ", 0.025, "Divide back.",
      done="Returns 0.025 mol, so 0.6 dm³."),
]

S[3]["hint"] = "Find the theoretical mass of iron, then actual over theoretical times 100."
S[3]["misconceptions"] = [mis("mole_ratio",
  "The ratio 2Fe₂O₃ : 4Fe is 1 : 2, so moles Fe = 0.125 and theoretical mass = 7.0 g. Yield = (5.6 ÷ 7.0) × 100 = 80%.", 160)]
S[3]["guided_steps"] = [
  say("Find the theoretical mass of iron, then compare it with the 5.6 g actually made."),
  box("moles Fe₂O₃ = 10 ÷ 160 = ", 0.0625, "Mass over Mr."),
  box("ratio 2Fe₂O₃ : 4Fe = 1 : 2, so moles Fe = 0.0625 × 2 = ", 0.125, "Double it."),
  box("theoretical mass Fe = 0.125 × 56 = ", 7, "Moles × Ar."),
  box("yield = (5.6 ÷ 7) × 100 = ", 80, "5.6 over 7, times 100.", phase="substitute"),
  box("Check: 80% of 7 g = 0.8 × 7 = ", 5.6, "Take 80% of the theoretical mass.",
      done="Matches the 5.6 g made, so 80%."),
]

S[4]["hint"] = "Use the Mr of every product with its coefficient, then divide 112 by the total."
S[4]["misconceptions"] = [mis("coefficient_error",
  "Include the coefficients: 2Fe (Mr 112) and 3CO₂ (Mr 132). Atom economy = 112 ÷ 244 × 100 = 45.9%.", 56)]
S[4]["guided_steps"] = [
  say("Atom economy uses the \\(M_r\\) of every product, coefficients included."),
  box("Mr of desired 2Fe = 2 × 56 = ", 112, "Two iron atoms."),
  box("Mr of 3CO₂ = 3 × 44 = ", 132, "Three CO₂."),
  box("Mr of all products = 112 + 132 = ", 244, "Add them."),
  box("atom economy = (112 ÷ 244) × 100, to 1 d.p. = ", 45.9,
      "112 over 244, times 100.", phase="substitute"),
  box("Check: waste CO₂ share = 100 − 45.9 = ", 54.1, "Subtract from 100.",
      done="About 54% of the product mass is waste CO₂, so atom economy is 45.9%."),
]

S[5]["hint"] = "With only one product, every atom is wanted."
S[5]["misconceptions"] = [mis("wrong_denominator",
  "NH₃ is the only product, so all atoms end up in it. Atom economy = 100%.", None)]
S[5]["guided_steps"] = [
  say("Atom economy = \\(M_r\\) of desired ÷ \\(M_r\\) of all products × 100."),
  box("How many products in N₂ + 3H₂ → 2NH₃? ", 1, "Count what is right of the arrow."),
  box("One product means all atoms are wanted: (all ÷ all) × 100 = ", 100,
      "Itself over itself, times 100.", phase="substitute"),
  box("Check: waste = 100 − 100 = ", 0, "Nothing is left over.",
      done="No waste, so atom economy is 100%."),
]

# ---- GOLD ----
G[0]["hint"] = "Find the theoretical volume of H₂, convert to cm³, then compare with 960 cm³."
G[0]["misconceptions"] = [
  mis("unit_error",
    "Match the units before dividing: theoretical volume is 1.2 dm³ = 1200 cm³. Yield = (960 ÷ 1200) × 100 = 80%.", 80000),
  mis("inverse_error",
    "Put the actual amount on top: (960 ÷ 1200) × 100 = 80%, not (1200 ÷ 960) × 100.", 125)]
G[0]["guided_steps"] = [
  say("Find the theoretical volume of H₂, convert it to cm³, then compare with the 960 cm³ collected."),
  box("moles Zn = 3.25 ÷ 65 = ", 0.05, "Mass over Ar."),
  box("moles H₂ (ratio 1 : 1) = ", 0.05, "Same as Zn."),
  box("theoretical volume in dm³ = 0.05 × 24 = ", 1.2, "0.05 lots of 24."),
  box("convert to cm³ to match the data: 1.2 × 1000 = ", 1200, "1 dm³ = 1000 cm³.", phase="substitute"),
  box("yield = (960 ÷ 1200) × 100 = ", 80, "960 over 1200, times 100."),
  box("Check: 80% of 1200 = 0.8 × 1200 = ", 960, "Take 80% of the theoretical volume.",
      done="Matches the 960 cm³ collected, so 80%."),
]

G[1]["hint"] = "Route B has two products: add their Mr, then divide 56 by the total."
G[1]["misconceptions"] = [
  mis("wrong_route",
    "This is Route B (Ca(OH)₂ → CaO + H₂O): AE = 56 ÷ 74 × 100 = 75.7%. Route A would give 56%.", 56),
  mis("wrong_product",
    "The desired product is CaO (56), not H₂O (18). AE = 56 ÷ 74 × 100 = 75.7%.", 24.3)]
G[1]["guided_steps"] = [
  say("Route B is Ca(OH)₂ → CaO + H₂O. Atom economy uses the two products."),
  box("Mr of all products = 56 + 18 = ", 74, "CaO plus H₂O."),
  box("atom economy = (56 ÷ 74) × 100, to 2 d.p. = ", 75.68, "56 over 74, times 100.", phase="substitute"),
  box("Check: waste H₂O share = 100 − 75.68 = ", 24.32, "Subtract from 100.",
      done="About a quarter is waste water; to 1 decimal place the atom economy is 75.7%."),
]

G[2]["hint"] = "Find moles of Fe₂O₃, multiply by 3 for CO₂, then multiply by 24."
G[2]["misconceptions"] = [mis("mole_ratio",
  "One Fe₂O₃ makes three CO₂, so moles CO₂ = 0.2 × 3 = 0.6. Volume = 0.6 × 24 = 14.4 dm³.", 4.8)]
G[2]["guided_steps"] = [
  say("Find moles of Fe₂O₃, scale by the 1 : 3 ratio to CO₂, then multiply by 24."),
  box("moles Fe₂O₃ = 32 ÷ 160 = ", 0.2, "Mass over Mr."),
  box("moles CO₂ = 0.2 × 3 = ", 0.6, "One Fe₂O₃ makes three CO₂."),
  box("volume = 0.6 × 24 = ", 14.4, "0.6 lots of 24.", phase="substitute"),
  box("Check: 14.4 ÷ 24 = ", 0.6, "Divide back.",
      done="Returns 0.6 mol CO₂, so 14.4 dm³."),
]

G[3]["hint"] = "Find Mr of KClO₃, then moles, then the 2:3 ratio to O₂, then multiply by 24."
G[3]["misconceptions"] = [mis("mole_ratio",
  "The ratio 2KClO₃ : 3O₂ gives moles O₂ = 0.1 × 3 ÷ 2 = 0.15. Volume = 0.15 × 24 = 3.6 dm³.", 2.4)]
G[3]["guided_steps"] = [
  say("Find Mr of KClO₃, then moles, then the 2 : 3 ratio, then multiply by 24."),
  box("Mr KClO₃ = 39 + 35.5 + (3 × 16) = ", 122.5, "K + Cl + three O."),
  box("moles KClO₃ = 12.25 ÷ 122.5 = ", 0.1, "Mass over Mr."),
  box("moles O₂ = 0.1 × 3 ÷ 2 = ", 0.15, "Ratio 2KClO₃ : 3O₂."),
  box("volume = 0.15 × 24 = ", 3.6, "0.15 lots of 24.", phase="substitute"),
  box("Check: 3.6 ÷ 24 = ", 0.15, "Divide back.",
      done="Returns 0.15 mol O₂, so 3.6 dm³."),
]

G[4]["hint"] = "Find the theoretical volume of CO₂ in cm³, then compare with 504 cm³."
G[4]["misconceptions"] = [
  mis("unit_error",
    "Match the units: theoretical volume is 0.6 dm³ = 600 cm³. Yield = (504 ÷ 600) × 100 = 84%.", 84000),
  mis("inverse_error",
    "Put the actual amount on top: (504 ÷ 600) × 100 = 84%, not (600 ÷ 504) × 100.", 119.05)]
G[4]["guided_steps"] = [
  say("Find the theoretical volume of CO₂ in cm³, then compare with the 504 cm³ collected."),
  box("moles CaCO₃ = 2.5 ÷ 100 = ", 0.025, "Mass over Mr."),
  box("moles CO₂ (ratio 1 : 1) = ", 0.025, "Same as CaCO₃."),
  box("theoretical volume in dm³ = 0.025 × 24 = ", 0.6, "0.025 lots of 24."),
  box("convert to cm³: 0.6 × 1000 = ", 600, "1 dm³ = 1000 cm³.", phase="substitute"),
  box("yield = (504 ÷ 600) × 100 = ", 84, "504 over 600, times 100."),
  box("Check: 84% of 600 = 0.84 × 600 = ", 504, "Take 84% of the theoretical volume.",
      done="Matches the 504 cm³ collected, so 84%."),
]

G[5]["hint"] = "Use the Mr of every product with its coefficient, then divide 96 by the total."
G[5]["misconceptions"] = [mis("coefficient_error",
  "Include the coefficients: 3O₂ (Mr 96) and 2KCl (Mr 149), total 245. Atom economy = 96 ÷ 245 × 100 = 39.2%.", 30.05)]
G[5]["guided_steps"] = [
  say("Oxygen is the desired product. Include the coefficients: 3O₂ and 2KCl."),
  box("Mr of 3O₂ = 3 × 32 = ", 96, "Three O₂ molecules, each 32."),
  box("Mr of 2KCl = 2 × 74.5 = ", 149, "Two KCl, each 74.5 (39 + 35.5)."),
  box("Mr of all products = 96 + 149 = ", 245, "Add them."),
  box("atom economy = (96 ÷ 245) × 100, to 2 d.p. = ", 39.18, "96 over 245, times 100.", phase="substitute"),
  box("Check: waste KCl share = 100 − 39.18 = ", 60.82, "Subtract from 100.",
      done="About 61% is waste KCl; to 1 decimal place the atom economy is 39.2%."),
]

# ---------------------------------------------------------------- fix pre-existing em dashes
EM = "—"
pd["exam_context"]["frequency"] = pd["exam_context"]["frequency"].replace(EM, ":")
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if EM in st.get("label", ""):
            st["label"] = st["label"].replace(" " + EM + " ", ": ").replace(EM, ":")

# safety: assert no em dash anywhere student-facing survives
def _scan(o):
    if isinstance(o, dict):
        return any(_scan(v) for k, v in o.items() if k not in ("note", "guided_skip_reason"))
    if isinstance(o, list):
        return any(_scan(v) for v in o)
    return isinstance(o, str) and EM in o
assert not _scan(pd), "em dash still present"

# ---------------------------------------------------------------- write
json.dump(pd, io.open("lesson_higher-calculations-L02@6e6bcbcbc7.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written")
