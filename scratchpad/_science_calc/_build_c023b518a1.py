# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # unicode minus (never em dash) for pre/message text

pd = json.load(io.open("_c023_canon.json", encoding="utf-8"))

def sub(d):
    d = dict(d); d["phase"] = "substitute"; return d

def alpha_mass_walk(m, z):
    nm, nz = m-4, z-2
    return [
        {"say": "Alpha decay emits a helium nucleus. The mass number falls by 4 and the atomic number falls by 2."},
        {"pre": "The mass number falls by how much? ", "answer": 4,
         "hint": "An alpha particle is a helium nucleus: 2 protons and 2 neutrons, so 4 nucleons."},
        sub({"pre": f"New mass number = {m} {MINUS} 4 = ", "answer": nm, "hint": f"Take 4 away from {m}."}),
        {"pre": f"Check the atomic number too: {z} {MINUS} 2 = ", "answer": nz,
         "done": f"That is the daughter nucleus. The mass number is {nm}.",
         "hint": "Alpha also lowers the atomic number, by 2."},
    ]

def alpha_atomic_walk(m, z):
    nm, nz = m-4, z-2
    return [
        {"say": "Alpha decay emits a helium nucleus. The mass number falls by 4 and the atomic number falls by 2."},
        {"pre": "The atomic number falls by how much? ", "answer": 2,
         "hint": "An alpha particle carries away 2 protons."},
        sub({"pre": f"New atomic number = {z} {MINUS} 2 = ", "answer": nz, "hint": f"Take 2 away from {z}."}),
        {"pre": f"Check the mass number too: {m} {MINUS} 4 = ", "answer": nm,
         "done": f"That is the daughter nucleus. The atomic number is {nz}.",
         "hint": "Alpha also lowers the mass number, by 4."},
    ]

def beta_atomic_walk(m, z):
    nz = z+1
    return [
        {"say": "Beta decay turns a neutron into a proton. The mass number stays the same and the atomic number rises by 1."},
        {"pre": "The atomic number rises by how much? ", "answer": 1,
         "hint": "One neutron becomes one proton, so one extra proton."},
        sub({"pre": f"New atomic number = {z} + 1 = ", "answer": nz, "hint": f"Add 1 to {z}."}),
        {"pre": "Check the mass number: it does not change, so it is still ", "answer": m,
         "done": f"That is the daughter nucleus. The atomic number is {nz}.",
         "hint": "Beta decay leaves the mass number untouched."},
    ]

def activity_after_n(start, n, unit):
    steps = [{"say": f"Each half-life halves the activity. Start at {start} {unit}."}]
    val = start
    for i in range(1, n+1):
        nxt = val/2
        nxt_disp = int(nxt) if float(nxt).is_integer() else nxt
        val_disp = int(val) if float(val).is_integer() else val
        st = {"pre": f"After {i} half-life{'s' if i>1 else ''}: {val_disp} ÷ 2 = ", "answer": nxt_disp, "hint": "Halve the value."}
        if i == 2:
            st = sub(st)
        if i == n:
            st["done"] = f"After {n} half-lives, {nxt_disp} {unit} remain."
        steps.append(st)
        val = nxt
    return steps

def mass_remaining_walk(mass, hl, total, unit):
    n = total//hl
    steps = [
        {"say": "First find the number of half-lives: total time ÷ half-life."},
        {"pre": f"Number of half-lives = {total} ÷ {hl} = ", "answer": n, "hint": f"Divide the {total} hours by the {hl} hour half-life."},
    ]
    val = mass
    for i in range(1, n+1):
        nxt = val/2
        val_disp = int(val) if float(val).is_integer() else val
        nxt_disp = int(nxt) if float(nxt).is_integer() else nxt
        st = {"pre": f"{val_disp} ÷ 2 = ", "answer": nxt_disp, "hint": "Halve the mass."}
        if i == 1:
            st = sub(st)
        if i == n:
            st["done"] = f"{nxt_disp} {unit} remain after {n} half-lives."
        steps.append(st)
        val = nxt
    return steps

def hl_from_data_walk(a0, a1, time, unit):
    steps = [{"say": f"Count how many times the activity halves from {a0} down to {a1}."}]
    val = a0; n = 0
    while val > a1 + 1e-9:
        nxt = val/2; n += 1
        val_disp = int(val) if float(val).is_integer() else val
        nxt_disp = int(nxt) if float(nxt).is_integer() else nxt
        st = {"pre": f"{val_disp} ÷ 2 = ", "answer": nxt_disp, "hint": "Keep halving."}
        if abs(nxt - a1) < 1e-9:
            adisp = int(a1) if float(a1).is_integer() else a1
            st["done"] = f"Reached {adisp} in {n} halvings."
        steps.append(st)
        val = nxt
    hl = time/n
    hl_disp = int(hl) if float(hl).is_integer() else hl
    steps.append(sub({"pre": "So the number of half-lives in the time is ", "answer": n, "hint": "Count the halving arrows you just did."}))
    steps.append({"pre": f"Half-life = {time} ÷ {n} = ", "answer": hl_disp,
                  "say": "Half-life = total time ÷ number of halvings.", "hint": f"Divide the {time} {unit} by {n}."})
    steps.append({"pre": f"Check: {hl_disp} × {n} = ", "answer": time,
                  "done": f"That matches the {time} {unit} given, so the half-life is {hl_disp} {unit}.",
                  "hint": f"Multiply the half-life by {n} to get back the total time."})
    return steps

M = MINUS
MC_ = {
 ("bronze",0):[("beta_instead",226,f"Alpha decay does change the mass number. Beta decay is the one that leaves it the same. Alpha: 226 {M} 4 = 222."),
               ("wrong_drop",224,f"Alpha lowers the mass number by 4, not by 2. The 2 is the atomic-number drop. 226 {M} 4 = 222.")],
 ("bronze",1):[("wrong_drop",84,f"The atomic number drops by 2 in alpha decay, not by 4. The 4 is the mass-number drop. 88 {M} 2 = 86."),
               ("beta_instead",89,f"This is alpha decay, so the atomic number falls. Only beta raises it. 88 {M} 2 = 86.")],
 ("bronze",2):[("no_change",6,"Beta decay does change the atomic number: a neutron becomes a proton, so it rises by 1. 6 + 1 = 7."),
               ("alpha_instead",4,f"That is the alpha rule (atomic {M}2). Beta raises the atomic number by 1. 6 + 1 = 7.")],
 ("bronze",3):[("divided_linear",200,"Halve four times, do not divide by 4. 800 → 400 → 200 → 100 → 50 Bq."),
               ("wrong_count",100,"That is only three halvings. After four: 800 → 400 → 200 → 100 → 50 Bq.")],
 ("bronze",4):[("wrong_count",500,"That is only two halvings. After three: 2000 → 1000 → 500 → 250 Bq.")],
 ("bronze",5):[("wrong_drop",236,f"Alpha lowers the mass number by 4, not by 2. 238 {M} 4 = 234."),
               ("beta_instead",238,f"Alpha decay lowers the mass number; beta leaves it unchanged. 238 {M} 4 = 234.")],
 ("bronze",6):[("wrong_direction",81,"Beta raises the atomic number by 1, it does not lower it. 82 + 1 = 83."),
               ("no_change",82,"Beta decay does change the atomic number: a neutron becomes a proton. 82 + 1 = 83.")],
 ("bronze",7):[("wrong_direction",26,"Beta raises the atomic number by 1, it does not lower it. 27 + 1 = 28."),
               ("alpha_instead",25,f"That is the alpha rule (atomic {M}2). Beta raises the atomic number by 1. 27 + 1 = 28.")],
 ("silver",0):[("count_values",4,"Count the halving steps, not the numbers written down. 6400 to 400 is 4 halvings. 20 ÷ 4 = 5 minutes."),
               ("divided_by_ratio",1.25,"Divide the time by the number of halvings (4), not by the activity ratio (16). 20 ÷ 4 = 5 minutes.")],
 ("silver",1):[("count_values",7.5,"1200 to 150 is 3 halvings, not 4. Count the steps, not the numbers. 30 ÷ 3 = 10 minutes.")],
 ("silver",2):[("wrong_drop",239,f"Alpha lowers the mass number by 4, not by 2. 241 {M} 4 = 237.")],
 ("silver",3):[("wrong_direction",37,"Beta raises the atomic number by 1. 38 + 1 = 39, not 37.")],
 ("silver",4):[("wrong_count",3.125,"15 ÷ 3 = 5 half-lives, not 4. 50 → 25 → 12.5 → 6.25 → 3.125 → 1.5625 g."),
               ("subtracted",None,"You halve the mass each time, you do not subtract a fixed amount. 50 → 25 → 12.5 → 6.25 → 3.125 → 1.5625 g.")],
 ("silver",5):[("wrong_drop",208,f"Alpha lowers the mass number by 4, not by 2. 210 {M} 4 = 206.")],
 ("gold",0):[("count_values",10.4,"5000 to 312.5 is 4 halvings, not 5. Count the steps. 52 ÷ 4 = 13 days."),
             ("divided_by_ratio",3.25,"5000 ÷ 312.5 = 16 is the activity ratio, not the number of half-lives. There are 4 half-lives. 52 ÷ 4 = 13 days.")],
 ("gold",1):[("wrong_count",64,"56 ÷ 8 = 7 half-lives. The denominator is 2⁷ = 128, not 2⁶ = 64."),
             ("multiplied",14,"Do not multiply 7 by 2. Each half-life doubles the denominator, so it is 2⁷ = 128.")],
 ("gold",2):[("wrong_type",None,"The mass number stays at 234 and the atomic number rises from 90 to 91. A gain of one proton is beta decay.")],
 ("gold",3):[("forgot_step",24,f"Do both decays. Beta leaves the mass at 24, then alpha takes 4 off: 24 {M} 4 = 20."),
             ("used_atomic",10,f"The question asks for the mass number, not the atomic number. Final mass = 24 {M} 4 = 20.")],
 ("gold",4):[("unit_error",0.5,"Convert 2 hours to 120 minutes first. 120 ÷ 4 = 30 minutes, not 2 ÷ 4."),
             ("count_values",24,"480 to 30 is 4 halvings. 120 ÷ 4 = 30 minutes.")],
 ("gold",5):[("wrong_direction",52,"Beta raises the atomic number by 1. 53 + 1 = 54, not 52.")],
}

HINTS = {
 ("bronze",0):"Alpha decay drops the mass number by 4.",
 ("bronze",1):"Alpha decay drops the atomic number by 2.",
 ("bronze",2):"Beta decay raises the atomic number by 1.",
 ("bronze",3):"Halve the activity once for each half-life.",
 ("bronze",4):"Halve the activity once for each half-life.",
 ("bronze",5):"Alpha decay drops the mass number by 4.",
 ("bronze",6):"Beta decay raises the atomic number by 1.",
 ("bronze",7):"Beta decay raises the atomic number by 1.",
 ("silver",0):"Count the halvings from 6400 to 400, then divide 20 by that count.",
 ("silver",1):"Count the halvings from 1200 to 150, then divide 30 by that count.",
 ("silver",2):"Alpha decay drops the mass number by 4.",
 ("silver",3):"Beta decay raises the atomic number by 1.",
 ("silver",4):"Number of half-lives = 15 divided by 3, then halve the mass that many times.",
 ("silver",5):"Alpha decay drops the mass number by 4.",
 ("gold",0):"Count the halvings from 5000 to 312.5, then divide 52 by that count.",
 ("gold",1):"Number of half-lives = 56 divided by 8; the denominator doubles each half-life.",
 ("gold",2):"The atomic number rises by 1, so a neutron became a proton.",
 ("gold",3):"Apply beta first (mass unchanged), then alpha (mass drops 4).",
 ("gold",4):"Convert 2 hours to minutes first, then count the halvings.",
 ("gold",5):"Beta decay raises the atomic number by 1.",
}

WALKS = {
 ("bronze",0):alpha_mass_walk(226,88),
 ("bronze",1):alpha_atomic_walk(226,88),
 ("bronze",2):beta_atomic_walk(14,6),
 ("bronze",3):activity_after_n(800,4,"Bq"),
 ("bronze",4):activity_after_n(2000,3,"Bq"),
 ("bronze",5):alpha_mass_walk(238,92),
 ("bronze",6):beta_atomic_walk(214,82),
 ("bronze",7):beta_atomic_walk(60,27),
 ("silver",0):hl_from_data_walk(6400,400,20,"minutes"),
 ("silver",1):hl_from_data_walk(1200,150,30,"minutes"),
 ("silver",2):alpha_mass_walk(241,95),
 ("silver",3):beta_atomic_walk(90,38),
 ("silver",4):mass_remaining_walk(50,3,15,"g"),
 ("silver",5):alpha_mass_walk(210,84),
 ("gold",0):hl_from_data_walk(5000,312.5,52,"days"),
 ("gold",1):[
    {"say": "First find the number of half-lives: total time ÷ half-life."},
    {"pre": "Number of half-lives = 56 ÷ 8 = ", "answer": 7, "hint": "Divide the 56 hours by the 8 hour half-life."},
    sub({"pre": "The denominator doubles each half-life. Start at 1 and double 7 times: 1, 2, 4, 8, 16, 32, 64, then 64 × 2 = ", "answer": 128,
         "hint": "Double 64 once more for the seventh doubling."}),
    {"pre": "Check the count: 8 hours × 7 = ", "answer": 56,
     "done": "56 hours matches, so 7 half-lives and a denominator of 128 is right.",
     "hint": "Multiply the half-life by the number of half-lives."},
 ],
 ("gold",3):[
    {"say": "Do the two decays in order. Sodium-24 starts with mass number 24 and atomic number 11."},
    {"pre": "Beta decay leaves the mass number unchanged, so it is still ", "answer": 24, "hint": "Beta does not change the mass number."},
    sub({"pre": f"Now alpha decay takes 4 off the mass: 24 {M} 4 = ", "answer": 20, "hint": "Alpha lowers the mass number by 4."}),
    {"pre": f"Track the atomic number too: beta 11 + 1 = 12, then alpha 12 {M} 2 = ", "answer": 10,
     "done": "Neon-20 is formed. The final mass number is 20.",
     "hint": "Beta adds 1 to the atomic number, then alpha takes 2 off."},
 ],
 ("gold",4):[
    {"say": "The time is in hours but the answer must be in minutes. Convert the time first."},
    {"pre": "2 hours in minutes = 2 × 60 = ", "answer": 120, "hint": "There are 60 minutes in an hour."},
    {"say": "Now count how many times the count rate halves from 480 down to 30."},
    {"pre": "480 ÷ 2 = ", "answer": 240, "hint": "Keep halving."},
    {"pre": "240 ÷ 2 = ", "answer": 120, "hint": "Keep halving."},
    {"pre": "120 ÷ 2 = ", "answer": 60, "hint": "Keep halving."},
    {"pre": "60 ÷ 2 = ", "answer": 30, "done": "Reached 30 in 4 halvings.", "hint": "Keep halving."},
    sub({"pre": "So the number of half-lives is ", "answer": 4, "hint": "Count the halving arrows from 480 to 30."}),
    {"pre": "Half-life = 120 ÷ 4 = ", "answer": 30, "say": "Half-life = total time in minutes ÷ number of halvings.",
     "hint": "Divide the 120 minutes by 4."},
    {"pre": "Check: 30 × 4 = ", "answer": 120,
     "done": "120 minutes is 2 hours, which matches, so the half-life is 30 minutes.",
     "hint": "Multiply the half-life by 4 to get back the total time."},
 ],
 ("gold",5):beta_atomic_walk(131,53),
}

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i, p in enumerate(pb[tier]):
        key = (tier, i)
        p["hint"] = HINTS[key]
        p["misconceptions"] = [{"pattern":pat,"check":"common","message":msg,"expect":exp} for pat,exp,msg in MC_[key]]
        if key in WALKS:
            p["guided_steps"] = WALKS[key]

# gold[2] -> multiple_choice
g2 = pb["gold"][2]
g2["display"] = "Thorium-234 (atomic number 90) decays to protactinium-234 (atomic number 91). What type of decay is this?"
g2["input_type"] = "multiple_choice"
g2["options"] = ["Alpha decay", "Beta decay"]
g2["solutions"] = [1]
g2.pop("guided_steps", None)

pb["bronze_description"] = "One decay step, or a whole number of half-lives with the starting activity given."
pb["silver_description"] = "Count the halvings from data to find a half-life, sometimes converting the time unit first."
pb["gold_description"] = "Two decays chained, or working from an activity ratio, a fraction, or a longer time."

pd["method_card"] = {
 "title": "Nuclear Equations and Half-Life",
 "steps": [
   "Nuclear equations: balance the mass numbers and the atomic numbers on both sides.",
   "Alpha: mass −4, atomic −2. Beta: mass same, atomic +1.",
   "Half-life: keep halving the value and count how many halvings you need.",
   "Half-life = total time ÷ number of halvings.",
 ],
 "content": ("<p>Two skills, both really just <strong>counting</strong>.</p>"
   "<p><strong>Nuclear equations:</strong> the mass numbers (top) and the atomic numbers (bottom) must each balance on both sides. "
   "Alpha decay lowers the mass number by 4 and the atomic number by 2. Beta decay keeps the mass number the same and raises the atomic number by 1.</p>"
   "<p><strong>Half-life:</strong> the time for the activity to halve. There is no formula to memorise, just keep halving and count the steps. "
   "Number of half-lives = total time ÷ half-life. After \\(n\\) half-lives the fraction left is \\(\\left(\\tfrac{1}{2}\\right)^n\\).</p>"),
}

pd["exam_context"]["frequency"] = "High. Nuclear equations and half-life appear on almost every Paper 1."

# strip em dashes from preserved worked_examples labels ("Step 1 — X" -> "Step 1: X")
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and isinstance(st["label"], str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", "-")

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one decay or a set number of half-lives",
   "steps": [
     "For a decay, use the rule once. <strong>Alpha</strong>: mass −4, atomic −2. <strong>Beta</strong>: mass unchanged, atomic +1.",
     "For half-life, halve the activity once for every half-life that passes.",
     "The mass number is the big top number; the atomic number is the small bottom one.",
   ],
   "example": {
     "question": "Radon-220 (atomic number 86) undergoes alpha decay. Find the mass number of the daughter nucleus.",
     "steps": [
       {"label": "Rule", "content": "<p>Alpha decay lowers the mass number by 4.</p>"},
       {"label": "Work", "content": "<p>220 − 4 = 216</p>"},
       {"label": "Check", "content": "<p>Atomic number also drops by 2: 86 − 2 = 84 (polonium-216).</p>", "isCheck": True},
       {"label": "Answer", "content": "<p><strong>216</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: find a half-life from data",
   "steps": [
     "Count how many times the activity halves to get from the start value to the end value.",
     "Half-life = total time ÷ number of halvings.",
     "If the time is in hours but the answer is wanted in minutes, convert first.",
   ],
   "example": {
     "question": "A source falls from 4000 Bq to 250 Bq in 60 minutes. Find the half-life.",
     "steps": [
       {"label": "Count halvings", "content": "<p>4000 → 2000 → 1000 → 500 → 250 is 4 halvings.</p>"},
       {"label": "Work", "content": "<p>Half-life = 60 ÷ 4 = 15 minutes.</p>"},
       {"label": "Check", "content": "<p>15 × 4 = 60 minutes, which matches.</p>", "isCheck": True},
       {"label": "Answer", "content": "<p><strong>15 minutes</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: chained decays and ratios",
   "steps": [
     "For two decays, apply the first rule, then feed the result into the second.",
     "For a fraction left, the denominator is \\(2^n\\) where \\(n\\) is the number of half-lives.",
     "For an activity ratio, express it as a power of 2 to read off the number of half-lives.",
   ],
   "example": {
     "question": "A sample drops from 8000 Bq to 125 Bq in 36 hours. Find the half-life.",
     "steps": [
       {"label": "Ratio", "content": "<p>8000 ÷ 125 = 64 = 2⁶, so 6 half-lives.</p>"},
       {"label": "Work", "content": "<p>Half-life = 36 ÷ 6 = 6 hours.</p>"},
       {"label": "Check", "content": "<p>6 × 6 = 36 hours, which matches.</p>", "isCheck": True},
       {"label": "Answer", "content": "<p><strong>6 hours</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

pd["guided"] = {
 "opener": {
   "steps": [
     {"say": "No physics needed here, just halving. A radioactive sample starts at 80 Bq. Every 2 hours, half of it decays away."},
     {"pre": "After the first 2 hours, half is gone. 80 ÷ 2 = ", "post": " Bq", "answer": 40, "hint": "Half of 80."},
     {"pre": "After another 2 hours, halve again. 40 ÷ 2 = ", "post": " Bq", "answer": 20, "hint": "Half of 40."},
     {"say": "Notice the second 2 hours only removed 20 Bq, not another 40. Radioactivity always takes the same <strong>fraction</strong> (a half) each time, never the same amount. That fixed time for the activity to halve is the <strong>half-life</strong>."},
   ],
 },
 "teach": {
   "bronze": {
     "display": "Bismuth-212 (atomic number 83) undergoes alpha decay. Find the mass number and atomic number of the daughter nucleus.",
     "steps": [
       {"say": "Alpha decay emits a helium nucleus. Mass number falls by 4, atomic number falls by 2."},
       {"pre": "The mass number falls by how much? ", "answer": 4, "hint": "An alpha particle has 4 nucleons."},
       {"pre": f"New mass number = 212 {M} 4 = ", "answer": 208, "hint": "Take 4 off 212."},
       {"pre": "The atomic number falls by how much? ", "answer": 2, "hint": "An alpha particle carries 2 protons."},
       sub({"pre": f"New atomic number = 83 {M} 2 = ", "answer": 81, "hint": "Take 2 off 83."}),
       {"pre": "Check the mass numbers balance: 208 + 4 (the alpha) = ", "answer": 212,
        "done": "Balances with the original 212, so thallium-208 is correct.", "hint": "Add the daughter mass to the alpha mass."},
     ],
   },
   "silver": {
     "display": "A source falls from 3200 Bq to 200 Bq in 24 minutes. Find the half-life.",
     "steps": [
       {"say": "Count how many times the activity halves from 3200 down to 200."},
       {"pre": "3200 ÷ 2 = ", "answer": 1600, "hint": "Keep halving."},
       {"pre": "1600 ÷ 2 = ", "answer": 800, "hint": "Keep halving."},
       {"pre": "800 ÷ 2 = ", "answer": 400, "hint": "Keep halving."},
       {"pre": "400 ÷ 2 = ", "answer": 200, "done": "Reached 200 in 4 halvings.", "hint": "Keep halving."},
       sub({"pre": "So the number of half-lives is ", "answer": 4, "hint": "Count the halving arrows."}),
       {"pre": "Half-life = 24 ÷ 4 = ", "answer": 6, "hint": "Divide the 24 minutes by 4."},
       {"pre": "Check: 6 × 4 = ", "answer": 24, "done": "Matches the 24 minutes, so the half-life is 6 minutes.", "hint": "Multiply the half-life by 4."},
     ],
   },
   "gold": {
     "display": "Bismuth-211 (atomic number 83) undergoes alpha decay, then the product undergoes beta decay. Find the final mass number and atomic number.",
     "steps": [
       {"say": "Do the decays in order, tracking both numbers. Start: mass 211, atomic 83."},
       {"pre": f"Alpha: new mass = 211 {M} 4 = ", "answer": 207, "hint": "Alpha lowers the mass by 4."},
       {"pre": f"Alpha: new atomic = 83 {M} 2 = ", "answer": 81, "hint": "Alpha lowers the atomic number by 2."},
       sub({"pre": "Beta: the mass number does not change, so it is still ", "answer": 207, "hint": "Beta leaves the mass number alone."}),
       {"pre": "Beta: new atomic = 81 + 1 = ", "answer": 82, "done": "Lead-207: mass 207, atomic 82.", "hint": "Beta adds 1 to the atomic number."},
       {"pre": "Check total mass is conserved: 207 + 4 (the alpha) = ", "answer": 211,
        "done": "Balances with the original 211, so the chain is correct.", "hint": "Add the final mass to the alpha mass."},
     ],
   },
 },
}

out = "lesson_higher-calculations-L05@c023b518a1.json"
json.dump(pd, io.open(out,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
s = json.dumps(pd, ensure_ascii=False)
print("written", out)
print("em dash present:", "—" in s)
