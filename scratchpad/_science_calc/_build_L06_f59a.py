# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_canonical_fresh.json", encoding="utf-8"))

# ---------- 1. method_card (slim, board-neutral, no em dash) ----------
pd["method_card"] = {
    "title": "Transformers and Electromagnetic Induction",
    "steps": [
        "Pick the equation: turns ratio for voltage or turns, power balance (Vp Ip = Vs Is) for current.",
        "Rearrange for the unknown, then substitute the values.",
        "Two-step questions: find the missing voltage or current first.",
        "State the answer with its unit (V, A, %, or W).",
    ],
    "content": (
        "<p>Two equations solve almost every transformer question.</p>"
        "<ul>"
        "<li><strong>Turns ratio:</strong> \\(\\frac{V_p}{V_s} = \\frac{n_p}{n_s}\\). "
        "More secondary turns steps the voltage up (current down); fewer steps it down.</li>"
        "<li><strong>Power balance</strong> for a 100% efficient transformer: \\(V_p I_p = V_s I_s\\). "
        "Use it for current questions.</li>"
        "</ul>"
        "<p>The National Grid transmits at very high voltage so the current is small. "
        "Power lost as heat in cables is \\(I^2R\\), and because current is squared, a small "
        "current means far less waste.</p>"
    ),
}

# ---------- 2. exam_context em dash fix ----------
pd["exam_context"]["frequency"] = "High. Transformers appear on almost every Paper 2"

# ---------- 3. worked_examples label em dash -> colon ----------
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ")

pb = pd["problem_bank"]

pb["bronze_description"] = "One equation, all values already in the right units: substitute and solve."
pb["silver_description"] = "Rearrange the equation, or use the power balance Vp Ip = Vs Is, before substituting."
pb["gold_description"] = "Two steps chained: find a voltage or current first, then efficiency or grid power loss."

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

def sayb(pre, answer, hint, text, post="", phase=None, done=None):
    d = {"say": text, "pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

def S(text):
    return {"say": text}

# BRONZE walks
gs_bronze = {
 (11.5,): [
    S("Turns ratio: \\(\\frac{V_p}{V_s} = \\frac{n_p}{n_s}\\). Rearranged for the secondary voltage: \\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."),
    box("First the turns fraction, ns ÷ np = 50 ÷ 1000 = ", 0.05, "Divide the secondary turns by the primary turns."),
    sayb("Now Vs = 230 × 0.05 = ", 11.5, "Multiply the primary voltage by the turns fraction.", "Fewer secondary turns, so the voltage steps down.", phase="substitute"),
    box("Check: 11.5 ÷ 230 = ", 0.05, "Divide your answer by 230; it should return the turns fraction.", done="That matches the turns fraction 0.05, so Vs = 11.5 V."),
 ],
 (24,): [
    S("\\(V_s = V_p \\times \\frac{n_s}{n_p}\\), and here we want ns, so \\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."),
    box("Top of the fraction first: np × Vs = 460 × 12 = ", 5520, "Multiply primary turns by secondary voltage."),
    sayb("Now divide by Vp: 5520 ÷ 230 = ", 24, "Divide by the primary voltage.", "That is the number of secondary turns.", phase="substitute"),
    box("Check: 24 × 230 = ", 5520, "Multiply your answer by the primary voltage.", done="Equals np × Vs = 5520, so ns = 24 turns."),
 ],
 (100,): [
    S("\\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."),
    box("Turns fraction, ns ÷ np = 2000 ÷ 500 = ", 4, "Divide the secondary turns by the primary turns."),
    sayb("Now Vs = 25 × 4 = ", 100, "Multiply the primary voltage by the turns fraction.", "More secondary turns, so this is a step-up: the voltage rises.", phase="substitute"),
    box("Check: 100 ÷ 25 = ", 4, "Divide your answer by 25.", done="Matches the turns ratio 4, so Vs = 100 V."),
 ],
 (12,): [
    S("\\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."),
    box("Turns fraction, ns ÷ np = 60 ÷ 1200 = ", 0.05, "Divide the secondary turns by the primary turns."),
    sayb("Now Vs = 240 × 0.05 = ", 12, "Multiply the primary voltage by the turns fraction.", "Fewer secondary turns, so step-down: the voltage falls.", phase="substitute"),
    box("Check: 12 ÷ 240 = ", 0.05, "Divide your answer by 240.", done="Matches the turns fraction 0.05, so Vs = 12 V."),
 ],
 (20,): [
    S("\\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."),
    box("Top of the fraction first: np × Vs = 400 × 11.5 = ", 4600, "Multiply primary turns by secondary voltage."),
    sayb("Now divide by Vp: 4600 ÷ 230 = ", 20, "Divide by the primary voltage.", "That is the number of secondary turns.", phase="substitute"),
    box("Check: 20 × 230 = ", 4600, "Multiply your answer by the primary voltage.", done="Equals np × Vs = 4600, so ns = 20 turns."),
 ],
 (60,): [
    S("\\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."),
    box("Turns fraction, ns ÷ np = 300 ÷ 600 = ", 0.5, "Divide the secondary turns by the primary turns."),
    sayb("Now Vs = 120 × 0.5 = ", 60, "Multiply the primary voltage by the turns fraction.", "Half the turns, so half the voltage.", phase="substitute"),
    box("Check: 60 ÷ 120 = ", 0.5, "Divide your answer by 120.", done="Matches the turns fraction 0.5, so Vs = 60 V."),
 ],
}

gs_silver = {
 (0.2,): [
    S("Power in = power out for a 100% efficient transformer: \\(V_p I_p = V_s I_s\\). Rearranged: \\(I_p = \\frac{V_s I_s}{V_p}\\)."),
    box("Secondary power first: Vs × Is = 11.5 × 4 = ", 46, "Multiply secondary voltage by secondary current."),
    sayb("Now Ip = 46 ÷ 230 = ", 0.2, "Divide by the primary voltage.", "Low-voltage side carries the higher current, so the primary current is small.", phase="substitute"),
    box("Check: 230 × 0.2 = ", 46, "Multiply your answer by the primary voltage.", done="Equals Vs Is = 46, so Ip = 0.2 A."),
 ],
 (1,): [
    S("Two moves: the turns ratio gives Vs, then power balance gives Is."),
    box("Turns ratio 10,000 ÷ 500 = 20, so Vs = 25 × 20 = ", 500, "Multiply the primary voltage by the turns ratio."),
    sayb("Power in = Vp × Ip = 25 × 20 = ", 500, "Multiply primary voltage by primary current.", "That is the power passing through, in watts.", phase="substitute"),
    box("Is = 500 ÷ Vs = 500 ÷ 500 = ", 1, "Divide the power by the secondary voltage."),
    box("Check: Vs × Is = 500 × 1 = ", 500, "Multiply secondary voltage by your answer.", done="Equals the input power 500 W, so Is = 1 A."),
 ],
 (5,): [
    S("\\(V_p I_p = V_s I_s\\), so \\(I_s = \\frac{V_p I_p}{V_s}\\)."),
    box("Primary power first: Vp × Ip = 230 × 0.5 = ", 115, "Multiply primary voltage by primary current."),
    sayb("Now Is = 115 ÷ 23 = ", 5, "Divide by the secondary voltage.", "Lower secondary voltage, so a bigger secondary current.", phase="substitute"),
    box("Check: 23 × 5 = ", 115, "Multiply the secondary voltage by your answer.", done="Equals Vp Ip = 115, so Is = 5 A."),
 ],
 (100,): [
    S("\\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."),
    box("Voltage fraction, Vs ÷ Vp = 220 ÷ 11,000 = ", 0.02, "Divide the secondary voltage by the primary voltage."),
    sayb("Now ns = 5000 × 0.02 = ", 100, "Multiply the primary turns by the voltage fraction.", "Far fewer turns on the secondary: a big step-down.", phase="substitute"),
    box("Check the turns ratio: 5000 ÷ 100 = ", 50, "Divide primary turns by your answer.", done="Equals the voltage ratio 11,000 ÷ 220 = 50, so ns = 100 turns."),
 ],
 (0.8,): [
    S("\\(V_p I_p = V_s I_s\\), so \\(I_p = \\frac{V_s I_s}{V_p}\\)."),
    box("Secondary power first: Vs × Is = 220 × 40 = ", 8800, "Multiply secondary voltage by secondary current."),
    sayb("Now Ip = 8800 ÷ 11,000 = ", 0.8, "Divide by the primary voltage.", "Step-down: low voltage means high current on the secondary, so the primary current is small.", phase="substitute"),
    box("Check: 11,000 × 0.8 = ", 8800, "Multiply the primary voltage by your answer.", done="Equals Vs Is = 8800, so Ip = 0.8 A."),
 ],
 (120,): [
    S("\\(V_p I_p = V_s I_s\\), so \\(V_p = \\frac{V_s I_s}{I_p}\\)."),
    box("Secondary power first: Vs × Is = 6 × 2 = ", 12, "Multiply secondary voltage by secondary current."),
    sayb("Now Vp = 12 ÷ 0.1 = ", 120, "Divide by the primary current.", "Tiny primary current, so a large primary voltage.", phase="substitute"),
    box("Check: 120 × 0.1 = ", 12, "Multiply your answer by the primary current.", done="Equals Vs Is = 12, so Vp = 120 V."),
 ],
}

gs_gold = {
 (39.1,): [
    S("Two steps: find the current at the transmission voltage, then the heating loss \\(= I^2 R\\). Work in base units first."),
    box("Power in watts: 25 MW = 25 × 1,000,000 = ", 25000000, "1 MW = 1,000,000 W."),
    box("Current at 400,000 V: I = P ÷ V = 25,000,000 ÷ 400,000 = ", 62.5, "Divide power by voltage."),
    sayb("Square the current: I² = 62.5 × 62.5 = ", 3906.25, "Square the current before multiplying by resistance.", "The current is squared: this is the whole reason high voltage helps.", phase="substitute"),
    box("Loss = I²R = 3906.25 × 10 = ", 39062.5, "Multiply by the cable resistance."),
    box("In kilowatts: 39,062.5 ÷ 1000 = ", 39.0625, "Divide watts by 1000; keep the exact value for now.", done="Rounded to 1 decimal place, the power lost is 39.1 kW."),
 ],
 (10,): [
    S("Same method with no step-up transformer: find the current, then loss \\(= I^2 R\\)."),
    box("Power in watts: 25 MW = 25 × 1,000,000 = ", 25000000, "1 MW = 1,000,000 W."),
    box("Current at 25,000 V: I = P ÷ V = 25,000,000 ÷ 25,000 = ", 1000, "Divide power by voltage."),
    sayb("Square the current: I² = 1000 × 1000 = ", 1000000, "Square the current first.", "Ten times the current of the step-up case, and it is squared.", phase="substitute"),
    box("Loss = I²R = 1,000,000 × 10 = ", 10000000, "Multiply by the cable resistance."),
    box("In megawatts: 10,000,000 ÷ 1,000,000 = ", 10, "Divide watts by 1,000,000.", done="10 MW lost out of 25 MW, about 40% wasted, so the answer is 10 MW."),
 ],
 (80,): [
    S("\\(\\text{efficiency} = \\frac{\\text{power out}}{\\text{power in}} \\times 100\\)."),
    box("Power out = Vs × Is = 12 × 4 = ", 48, "Secondary voltage times secondary current."),
    box("Power in = Vp × Ip = 240 × 0.25 = ", 60, "Primary voltage times primary current."),
    sayb("Fraction: efficiency = 48 ÷ 60 = ", 0.8, "Divide output power by input power.", "That is the fraction; now turn it into a percentage.", phase="substitute"),
    box("As a percentage: 0.8 × 100 = ", 80, "Multiply the fraction by 100.", done="80% efficient: 48 W out of 60 W in, so the answer is 80%."),
 ],
 (920,): [
    S("Turns ratio \\(\\frac{V_p}{V_s} = \\frac{n_p}{n_s}\\), rearranged for the primary turns: \\(n_p = n_s \\times \\frac{V_p}{V_s}\\)."),
    box("Top of the fraction first: ns × Vp = 36 × 230 = ", 8280, "Secondary turns times primary voltage."),
    sayb("Now divide by Vs: 8280 ÷ 9 = ", 920, "Divide by the secondary voltage.", "A big step-down needs far more turns on the primary side.", phase="substitute"),
    box("Check: 920 × 9 = ", 8280, "Multiply your answer by the secondary voltage.", done="Equals ns × Vp = 8280, so np = 920 turns."),
 ],
 (8000,): [
    S("\\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."),
    box("Voltage ratio, Vs ÷ Vp = 400,000 ÷ 25,000 = ", 16, "Divide the secondary voltage by the primary voltage."),
    sayb("Now ns = 500 × 16 = ", 8000, "Multiply the primary turns by the voltage ratio.", "Step-up: many more turns on the secondary.", phase="substitute"),
    box("Check: 8000 ÷ 500 = ", 16, "Divide your answer by the primary turns.", done="Equals the voltage ratio 16, so ns = 8000 turns."),
 ],
 (20.7,): [
    S("Not 100% efficient, so power out = power in × efficiency, then \\(I_s = \\frac{\\text{power out}}{V_s}\\)."),
    box("Power in = Vp × Ip = 230 × 2 = ", 460, "Primary voltage times primary current."),
    box("Power out = 460 × 0.9 = ", 414, "Multiply by the efficiency as a decimal (0.9)."),
    sayb("Now Is = 414 ÷ 20 = ", 20.7, "Divide output power by the secondary voltage.", "Lower secondary voltage, so a larger secondary current.", phase="substitute"),
    box("Check: 20 × 20.7 = ", 414, "Multiply the secondary voltage by your answer.", done="Equals the output power 414 W, so Is = 20.7 A."),
 ],
}

hints_bronze = {(11.5,):"Multiply the primary voltage by the turns fraction ns over np.",
 (24,):"Rearrange to ns = np × Vs ÷ Vp, then work it out.",
 (100,):"More secondary turns, so multiply Vp by the turns ratio ns over np.",
 (12,):"Multiply Vp by ns ÷ np; fewer secondary turns means a smaller voltage.",
 (20,):"Rearrange to ns = np × Vs ÷ Vp.",
 (60,):"Halve the primary voltage: the turns ratio is 300 over 600."}
hints_silver = {(0.2,):"Use Vp Ip = Vs Is, then divide Vs Is by Vp.",
 (1,):"Find Vs from the turns ratio first, then use power in = power out.",
 (5,):"Is = Vp Ip ÷ Vs.",
 (100,):"ns = np × Vs ÷ Vp.",
 (0.8,):"Ip = Vs Is ÷ Vp.",
 (120,):"Vp = Vs Is ÷ Ip."}
hints_gold = {(39.1,):"Find the current with I = P ÷ V, then loss = I² R; remember to square the current.",
 (10,):"Same steps as the step-up case but with the full 1000 A current.",
 (80,):"Efficiency = power out ÷ power in × 100.",
 (920,):"np = ns × Vp ÷ Vs; a big step-down needs more primary turns.",
 (8000,):"ns = np × Vs ÷ Vp.",
 (20.7,):"Power out = power in × 0.9, then Is = power out ÷ Vs."}

exp_bronze = {(11.5,):[4600],(24,):[8816.67],(100,):[6.25],(12,):[4800],(20,):[8000],(60,):[240]}
exp_silver = {(0.2,):[46,80],(1,):[None,400],(5,):[115],(100,):[250000],(0.8,):[8800,2000],(120,):[12]}
exp_gold = {(39.1,):[None,0.625],(10,):[None,0.01],(80,):[None,125],(920,):[None,1.41],(8000,):[None,31.25],(20.7,):[23,None]}

def apply(tier, gs_map, hint_map, exp_map):
    for p in pb[tier]:
        sols = p.get("solutions")
        if sols and isinstance(sols[0], str):
            up = sols[0] == "step-up"
            p["input_type"] = "multiple_choice"
            p["options"] = ["Step-up", "Step-down"]
            p["solutions"] = [0 if up else 1]
            p["display"] = p["display"].split(" Enter ")[0].strip()
            p["display"] = p["display"].replace("Is this a step-up or step-down transformer?",
                                                "Is it a step-up or a step-down transformer?")
            for m in p.get("misconceptions", []):
                m["expect"] = None
            continue
        s = tuple(sols)
        p["hint"] = hint_map[s]
        p["guided_steps"] = gs_map[s]
        for m, e in zip(p.get("misconceptions", []), exp_map[s]):
            m["expect"] = e

apply("bronze", gs_bronze, hints_bronze, exp_bronze)
apply("silver", gs_silver, hints_silver, exp_silver)
apply("gold", gs_gold, hints_gold, exp_gold)

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one transformer equation",
   "steps": [
     "The turns ratio links voltage and turns: \\(\\frac{V_p}{V_s} = \\frac{n_p}{n_s}\\). More secondary turns steps the voltage UP; fewer steps it DOWN.",
     "Rearrange for the unknown, then substitute. To find a secondary voltage: \\(V_s = V_p \\times \\frac{n_s}{n_p}\\).",
     "Check: your voltage ratio should equal your turns ratio.",
   ],
   "example": {
     "question": "A transformer has 800 primary turns and 200 secondary turns. The primary voltage is 240 V. Find the secondary voltage.",
     "steps": [
       {"label": "Equation", "content": "<p>\\(V_s = V_p \\times \\frac{n_s}{n_p}\\)</p>"},
       {"label": "Substitute", "content": "<p>\\(V_s = 240 \\times \\frac{200}{800} = 240 \\times 0.25\\)</p>"},
       {"label": "Check", "content": "<p>\\(60 \\div 240 = 0.25\\), the same as the turns ratio ✓</p>"},
       {"label": "Answer", "content": "<p>\\(V_s\\) = <strong>60 V</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: rearrange, or use power balance",
   "steps": [
     "Sometimes you must rearrange the turns ratio first, for example \\(n_s = n_p \\times \\frac{V_s}{V_p}\\).",
     "For currents, a 100% efficient transformer obeys power in = power out: \\(V_p I_p = V_s I_s\\). The low-voltage side carries the higher current.",
     "Pick the equation that already contains three of your four quantities, then solve for the fourth.",
   ],
   "example": {
     "question": "A transformer has Vp = 230 V, Ip = 0.5 A and Vs = 46 V. Find Is (100% efficient).",
     "steps": [
       {"label": "Equation", "content": "<p>\\(V_p I_p = V_s I_s\\)</p>"},
       {"label": "Substitute", "content": "<p>\\(230 \\times 0.5 = 46 \\times I_s\\), so \\(115 = 46 I_s\\)</p>"},
       {"label": "Solve", "content": "<p>\\(I_s = 115 \\div 46\\)</p>"},
       {"label": "Check", "content": "<p>\\(46 \\times 2.5 = 115\\) ✓</p>"},
       {"label": "Answer", "content": "<p>\\(I_s\\) = <strong>2.5 A</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: two steps chained",
   "steps": [
     "Gold questions need two equations. You might find a voltage from the turns ratio, then a current from \\(V_p I_p = V_s I_s\\).",
     "Grid questions use power loss \\(= I^2 R\\). Because current is squared, transmitting at high voltage (small current) cuts the heating loss sharply.",
     "For efficiency: \\(\\text{efficiency} = \\frac{\\text{power out}}{\\text{power in}} \\times 100\\).",
   ],
   "example": {
     "question": "230 V and Ip = 2 A go into a transformer that is 80% efficient. Find the power output.",
     "steps": [
       {"label": "Power in", "content": "<p>\\(P = V_p I_p = 230 \\times 2 = 460\\) W</p>"},
       {"label": "Apply efficiency", "content": "<p>\\(P_{out} = 460 \\times 0.8\\)</p>"},
       {"label": "Check", "content": "<p>\\(368 \\div 460 = 0.8\\) ✓</p>"},
       {"label": "Answer", "content": "<p>\\(P_{out}\\) = <strong>368 W</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

pd["guided"] = {
 "opener": {
   "label": "Before any physics",
   "display": ("A bike in low gear: you pedal fast but the wheel pushes hard and turns slowly.<br>"
               "In high gear: the wheel spins fast but pushes gently.<br>"
               "The power you put in comes straight out either way."),
   "steps": [
     {"say": "No physics yet. Suppose you pedal in 100 watts of power. In a perfect gear system, how many watts come out at the wheel?",
      "pre": "Power out = ", "post": " W", "answer": 100,
      "hint": "A gear trades speed for force, but it cannot create energy. What goes in comes out."},
     {"say": "Exactly. A gear trades speed for force but keeps the power the same. A transformer does the identical trick with electricity: it trades <strong>voltage</strong> for <strong>current</strong>, keeping <strong>power</strong> the same.",
      "pre": "So if a transformer takes in 12 W, how many watts come out (100% efficient)? ", "post": " W", "answer": 12,
      "hint": "Same rule: power in = power out."},
     {"say": "That is the whole idea: \\(V_p I_p = V_s I_s\\), power in equals power out. Step the voltage UP and the current must come DOWN to keep the product the same. The turns ratio \\(\\frac{V_p}{V_s} = \\frac{n_p}{n_s}\\) sets how big the trade is."},
   ],
 },
 "teach": {
   "bronze": {
     "display": "A transformer steps 230 V down to 46 V. The primary coil has 1500 turns. Find the number of secondary turns.",
     "label": "Together: your first one",
     "steps": [
       S("Turns and voltages share the same ratio: \\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."),
       box("Voltage fraction, Vs ÷ Vp = 46 ÷ 230 = ", 0.2, "Divide the secondary voltage by the primary voltage."),
       sayb("Now ns = 1500 × 0.2 = ", 300, "Multiply the primary turns by the voltage fraction.", "Fewer secondary turns, exactly as you would expect for a step-down.", phase="substitute"),
       box("Check the turns ratio: 1500 ÷ 300 = ", 5, "Divide the primary turns by your answer."),
       box("And the voltage ratio: 230 ÷ 46 = ", 5, "Divide the primary voltage by the secondary voltage.", done="Turns ratio 5 = voltage ratio 5, so ns = 300 turns."),
     ],
   },
   "silver": {
     "display": "A step-down transformer has 2000 primary turns, 100 secondary turns, a primary voltage of 230 V and a secondary current of 8 A. Find the primary current (100% efficient).",
     "label": "Together: the silver move",
     "steps": [
       S("Two moves: the turns ratio gives Vs, then power balance \\(V_p I_p = V_s I_s\\) gives Ip."),
       box("Vs = 230 × (100 ÷ 2000) = 230 × 0.05 = ", 11.5, "Multiply the primary voltage by the turns ratio."),
       sayb("Secondary power = Vs × Is = 11.5 × 8 = ", 92, "Multiply the secondary voltage by the secondary current.", "Power in equals power out, so the primary carries this same 92 W.", phase="substitute"),
       sayb("Now Ip = 92 ÷ 230 = ", 0.4, "Divide the power by the primary voltage.", "Small primary current, big secondary current: that is step-down."),
       box("Check: 230 × 0.4 = ", 92, "Multiply the primary voltage by your answer.", done="Equals the secondary power 92 W, so Ip = 0.4 A."),
     ],
   },
   "gold": {
     "display": "A generator produces 20 MW at 20,000 V. The cables have a total resistance of 5 Ω. Find the power lost in the cables, in MW.",
     "label": "Together: the gold move",
     "steps": [
       S("Find the current with \\(I = \\frac{P}{V}\\), then the heating loss \\(= I^2 R\\). Convert MW to W first."),
       box("Power in watts: 20 MW = 20 × 1,000,000 = ", 20000000, "1 MW = 1,000,000 W."),
       box("Current: I = 20,000,000 ÷ 20,000 = ", 1000, "Divide power by voltage."),
       sayb("Square it: I² = 1000 × 1000 = ", 1000000, "Square the current before multiplying by resistance.", "Current squared: the key to why the grid uses high voltage.", phase="substitute"),
       box("Loss = I²R = 1,000,000 × 5 = ", 5000000, "Multiply by the cable resistance."),
       box("In megawatts: 5,000,000 ÷ 1,000,000 = ", 5, "Divide watts by 1,000,000.", done="5 MW lost out of 20 MW generated, so the answer is 5 MW."),
     ],
   },
 },
}

# sweep any remaining em dashes in preserved misconception messages
for tier in ("bronze", "silver", "gold"):
    for p in pb[tier]:
        for m in p.get("misconceptions", []):
            if m.get("message") and "—" in m["message"]:
                m["message"] = m["message"].replace(" — ", ": ").replace("—", ": ")

# em dash guard
EM = "—"
bad = []
def scan(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            scan(v, path + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, path + "[%d]" % i)
    elif isinstance(o, str) and EM in o:
        bad.append(path)
scan(pd, "pd")
if bad:
    raise SystemExit("EM DASH found at: " + "; ".join(bad))

json.dump(pd, io.open("lesson_higher-calculations-L06@f59adbb41d.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written OK; bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
