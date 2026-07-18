# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open('_canonical_fresh.json', encoding='utf-8'))

EM = '—'
def strip_em(o):
    if isinstance(o, dict):
        return {k: (v if k in ('note','guided_skip_reason') else strip_em(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [strip_em(x) for x in o]
    if isinstance(o, str):
        return o.replace(' ' + EM + ' ', ': ').replace(EM, ':')
    return o
pd = strip_em(pd)

MINUS = '−'

def say(t): return {"say": t}
def box(pre, ans, hint, post=None, phase=False, done=None):
    d = {"pre": pre, "answer": ans, "hint": hint}
    if post is not None: d["post"] = post
    if phase: d["phase"] = "substitute"
    if done is not None: d["done"] = done
    return d

def walk_mean(vals, unit):
    s = " + ".join(str(v) for v in vals)
    total = sum(vals); n = len(vals); m = total / n
    m = int(m) if m == int(m) else m
    total = int(total) if total == int(total) else total
    ut = (" " + unit) if unit else ""
    return [
        say("Mean = sum of values ÷ number of values. State the equation before the numbers."),
        box("Add all the values: " + s + " =", total, "Add every value together.", phase=True),
        box("Count how many values there are:", n, "Count them carefully."),
        box("Divide the sum by the count: " + str(total) + " ÷ " + str(n) + " =", m, "Share the total between " + str(n) + "."),
        say("So the mean is <strong>" + str(m) + ut + "</strong>."),
        box("Check: mean × count should give back the sum. " + str(m) + " × " + str(n) + " =", total,
            "Multiply back to the sum.", done="It returns " + str(total) + ", so " + str(m) + ut + " is right."),
    ]

def walk_pct(new, orig, ans, decrease=False, dp=None, note_over100=False):
    change = new - orig
    ch_s = ("%g" % change)
    frac = change / orig
    disp = str(new) + " " + MINUS + " " + str(orig)
    steps = [say(_pct_lead(decrease, note_over100)),
             box("Change = new " + MINUS + " original = " + disp + " =", change,
                 "Take the starting value from the new one.", phase=True)]
    if dp is None:
        steps.append(box("Divide by the original (" + str(orig) + "): " + ch_s + " ÷ " + str(orig) + " =", frac,
                         "Divide the change by the starting value."))
        steps.append(box("Multiply by 100: " + ("%g" % frac) + " × 100 =", change/orig*100,
                         "Shift two places for a percentage."))
    else:
        fr = round(frac, 3)
        steps.append(box("Divide by the original (" + str(orig) + "): " + ch_s + " ÷ " + str(orig) + " = (to 3 d.p.)", fr,
                         "Divide the change by the starting value."))
        steps.append(box("Multiply by 100: " + ("%g" % fr) + " × 100 =", fr*100,
                         "Shift two places for a percentage."))
    if decrease:
        base = abs(frac if dp is None else round(frac, 3))
        chk = abs(change) if dp is None else round(base*orig, 1)
        computed = (change/orig*100) if dp is None else (round(frac, 3)*100)
        if abs(computed - ans) > 1e-9:
            # stored answer is the positive magnitude (question asks for the decrease)
            steps.append(say("That is negative because the value fell. The question asks for the SIZE of the decrease, so drop the sign."))
            steps.append(box("Size of the decrease =", ans, "Give the positive value, no minus sign."))
        else:
            steps.append(say("So the percentage change is <strong>" + ("%g" % ans) + "%</strong>, a decrease."))
        steps.append(box("Check: " + ("%g" % abs(ans)) + "% of " + str(orig) + " is " + ("%g" % base) + " × " + str(orig) + " =" + (" (to 1 d.p.)" if dp else ""),
                         chk, "Should match the fall you found.",
                         done="It matches the fall of " + ("%g" % abs(change)) + ", so " + ("%g" % abs(ans)) + "% is right."))
    else:
        steps.append(say("So the percentage change is <strong>" + ("%g" % ans) + "%</strong>, an increase."))
        steps.append(box("Check: " + ("%g" % ans) + "% of " + str(orig) + " is " + ("%g" % frac) + " × " + str(orig) + " =", change,
                         "Should match the change you found.",
                         done="It matches the change of " + ("%g" % change) + ", so " + ("%g" % ans) + "% is right."))
    return steps

def _pct_lead(decrease, note_over100):
    lead = "Percentage change = (new " + MINUS + " original) ÷ original × 100. The ORIGINAL goes on the bottom."
    if decrease: lead += " A fall gives a negative; the question wants the size of the decrease."
    if note_over100: lead += " A rise can exceed 100% when a value more than doubles."
    return lead

def walk_pop(mean, ta, qa, ans, thing):
    nq = ta / qa; nq = int(nq) if nq == int(nq) else nq
    dens = mean / qa; dens = int(dens) if dens == int(dens) else dens
    return [
        say("Population = mean per quadrat × (total area ÷ quadrat area). Scale the mean up to the whole area."),
        box("How many quadrats fit the field: " + str(ta) + " ÷ " + str(qa) + " =", nq,
            "Field area over one quadrat's area.", phase=True),
        box("Population = mean × number of quadrats: " + str(mean) + " × " + str(nq) + " =", ans,
            "Multiply the mean by " + str(nq) + "."),
        say("So the estimated population is <strong>" + str(ans) + " " + thing + "</strong>."),
        box("Check via density: plants per m² = " + str(mean) + " ÷ " + str(qa) + " =", dens,
            "How many in a full square metre."),
        box(str(dens) + " × " + str(ta) + " =", ans, "Density times total area.",
            done="Same " + str(ans) + " by a second route, so it is right."),
    ]

pb = pd["problem_bank"]
pb["bronze"][0]["guided_steps"] = walk_mean([12,15,14,13,16], "cm")
pb["bronze"][1]["guided_steps"] = walk_pct(650, 500, 30)
pb["bronze"][2]["guided_steps"] = walk_mean([68,72,74,70,66], "bpm")
pb["bronze"][3]["guided_steps"] = walk_pct(2.8, 2.0, 40)
pb["bronze"][5]["guided_steps"] = walk_mean([8,5,7,4], "")
pb["bronze"][6]["guided_steps"] = walk_pct(60, 80, -25, decrease=True)
pb["bronze"][7]["guided_steps"] = walk_mean([3,5,4,6,3,3], "")

pb["silver"][0]["guided_steps"] = walk_pop(6, 100, 0.25, 2400, "clover plants")
pb["silver"][1]["guided_steps"] = walk_pct(5.6, 8.4, 33.3, decrease=True, dp=1)
pb["silver"][2]["guided_steps"] = [
    say("Two moves: exclude the anomaly, then average the four values that remain."),
    box("The anomaly sits far from the rest. Type the value you exclude:", 0.38,
        "0.38 mm is far above the cluster near 0.12 mm."),
    box("Add the four remaining values: 0.12 + 0.14 + 0.11 + 0.13 =", 0.5,
        "Add only the four that stay in.", phase=True),
    box("How many values remain after removing the anomaly?", 4, "You dropped one from five."),
    box("Mean = 0.5 ÷ 4 =", 0.125, "Divide by 4, not 5."),
    say("So the mean length is <strong>0.125 mm</strong>."),
    box("Check: 0.125 × 4 =", 0.5, "Multiply back to the sum.",
        done="Returns 0.5, so 0.125 mm is right."),
]
pb["silver"][3]["guided_steps"] = [
    say("Two steps: find the mean per quadrat, then scale up. Population = mean × (total area ÷ quadrat area)."),
    box("Add the eight counts: 3 + 5 + 2 + 4 + 6 + 3 + 5 + 4 =", 32, "Add all eight.", phase=True),
    box("Mean per quadrat = 32 ÷ 8 =", 4, "Divide by the 8 quadrats."),
    box("Quadrats in the meadow = 500 ÷ 1 =", 500, "Field area over quadrat area."),
    box("Population = 4 × 500 =", 2000, "Mean times number of quadrats."),
    say("So the estimated population is <strong>2000 plantain</strong>."),
    box("Check: 2000 ÷ 500 should return the mean. 2000 ÷ 500 =", 4, "Divide back to recover the mean.",
        done="It returns the mean of 4, so 2000 is right."),
]
pb["silver"][4]["guided_steps"] = walk_pct(162, 72, 125, note_over100=True)
pb["silver"][5]["guided_steps"] = walk_pct(9, 15, 40, decrease=True)

pb["gold"][0]["guided_steps"] = [
    say("The middle years are a distraction. Percentage change compares only 2020 (450) and 2025 (468)."),
    box("Identify the original, the 2020 value:", 450, "The starting year is 2020."),
    box("Change = 468 " + MINUS + " 450 =", 18, "Final minus original.", phase=True),
    box("18 ÷ 450 =", 0.04, "Divide by the 2020 value."),
    box("0.04 × 100 =", 4, "Multiply by 100 for a percentage."),
    say("So the overall change is <strong>4%</strong>, an increase."),
    box("Check: 4% of 450 is 0.04 × 450 =", 18, "Should match the rise.",
        done="It matches the rise of 18, so 4% is right."),
]
pb["gold"][1]["guided_steps"] = [
    say("Population scales with the mean, so the percentage change in population equals the change in the mean. Find both means."),
    box("First survey sum: 2 + 4 + 3 + 1 + 5 + 3 + 4 + 2 + 3 + 3 =", 30, "Add all ten."),
    box("First mean = 30 ÷ 10 =", 3, "Divide by 10."),
    box("Second survey sum: 5 + 7 + 6 + 4 + 8 + 6 + 5 + 7 + 6 + 6 =", 60, "Add all ten."),
    box("Second mean = 60 ÷ 10 =", 6, "Divide by 10."),
    box("Change in the mean = 6 " + MINUS + " 3 =", 3, "New mean minus old mean.", phase=True),
    box("(3 ÷ 3) × 100 =", 100, "Divide by the original mean of 3, then ×100."),
    say("So the population rose by <strong>100%</strong>: it doubled."),
    box("Check: a doubling means the new mean is twice the old. 2 × 3 =", 6, "Is 6 double 3?",
        done="6 is double 3, confirming a 100% increase."),
]
pb["gold"][3]["guided_steps"] = [
    say("Two divisions, keep them apart: total count ÷ number of quadrats gives the mean; total area ÷ quadrat area gives the scale-up."),
    box("Mean per quadrat = 90 ÷ 15 =", 6, "Total plants over number of quadrats."),
    box("Quadrats that fit the field = 750 ÷ 0.25 =", 3000, "Field area over quadrat area, not 750 ÷ 15.", phase=True),
    box("Population = mean × quadrats = 6 × 3000 =", 18000, "Multiply the mean by 3000."),
    say("So the estimated population is <strong>18000 clover plants</strong>."),
    box("Check via density: plants per m² = 6 ÷ 0.25 =", 24, "How many in a full square metre."),
    box("24 × 750 =", 18000, "Density times total area.",
        done="Same 18000 by a second route, so it is right."),
]
pb["gold"][4]["guided_steps"] = [
    say("Read the days carefully: day 0 = 0.2, day 14 = 3.8. Percentage change = (new " + MINUS + " original) ÷ original × 100."),
    box("Identify the original, the day 0 reading:", 0.2, "The day 0 value."),
    box("Change = 3.8 " + MINUS + " 0.2 =", 3.6, "Day 14 minus day 0.", phase=True),
    box("3.6 ÷ 0.2 =", 18, "Divide by the tiny original, 0.2."),
    box("18 × 100 =", 1800, "Multiply by 100 for a percentage."),
    say("So the change is <strong>1800%</strong>: it rose eighteen-fold."),
    box("Check: 1800% of 0.2 is 18 × 0.2 =", 3.6, "Should match the rise.",
        done="It matches the rise of 3.6, so 1800% is right."),
]

def se(tier, idx, vals):
    ms = pb[tier][idx].get("misconceptions") or []
    for m, e in zip(ms, vals):
        m["expect"] = e
se("bronze",0,[None]); se("bronze",1,[None,0.3]); se("bronze",2,[None]); se("bronze",3,[None])
se("bronze",4,[None]); se("bronze",5,[None]); se("bronze",6,[25,None]); se("bronze",7,[None])
se("silver",0,[150,600]); se("silver",1,[-33.3,50]); se("silver",2,[0.176,0.1])
se("silver",3,[16000,32]); se("silver",4,[None,None]); se("silver",5,[None,-40])
se("gold",0,[-20,10]); se("gold",1,[50,None]); se("gold",2,[None,None])
se("gold",3,[270000,300]); se("gold",4,[600,1700]); se("gold",5,[None,None])

hints = {
 ("bronze",0):"Add the five heights, then divide by five.",
 ("bronze",1):"Change over the original value, times 100.",
 ("bronze",2):"Add the five rates, then divide by five.",
 ("bronze",3):"Divide the rise by the starting mass, times 100.",
 ("bronze",4):"Look for the value far from the cluster.",
 ("bronze",5):"Add the four counts, then divide by four.",
 ("bronze",6):"It fell, so expect a negative percentage; divide by 80.",
 ("bronze",7):"Add the six counts, then divide by six.",
 ("silver",0):"How many quadrats fit the field first, then multiply by the mean.",
 ("silver",1):"Divide the fall by the original 8.4, then round to 1 d.p.",
 ("silver",2):"Drop the outlier, then average the four that remain.",
 ("silver",3):"Find the mean per quadrat, then scale by area.",
 ("silver",4):"Divide the rise by the resting rate, times 100.",
 ("silver",5):"Divide the fall by the original 15, times 100.",
 ("gold",0):"Compare only the first and last years; ignore the middle.",
 ("gold",1):"Find both means, then the percentage change between them.",
 ("gold",2):"Compare percentages, not the raw tonnage increases.",
 ("gold",3):"Total over quadrats for the mean; area over area to scale up.",
 ("gold",4):"Use the day 0 and day 14 readings only.",
 ("gold",5):"Think which change makes the sample more representative.",
}
for (t,i),h in hints.items():
    pb[t][i]["hint"] = h

EQ_PCT = "\\(\\% \\text{ change} = \\frac{\\text{new} - \\text{original}}{\\text{original}} \\times 100\\)"
EQ_POP = "\\(\\text{population} = \\text{mean per quadrat} \\times \\frac{\\text{total area}}{\\text{quadrat area}}\\)"
pb["gold"][0]["equation_hint"] = EQ_PCT
pb["gold"][1]["equation_hint"] = EQ_PCT
pb["gold"][3]["equation_hint"] = EQ_POP
pb["gold"][4]["equation_hint"] = EQ_PCT

pb["bronze_description"] = "One calculation with the values given: find a mean, or a straight percentage change."
pb["silver_description"] = "Convert or scale first: estimate a population, exclude an anomaly, or work a percentage to a stated decimal place."
pb["gold_description"] = "Chain two steps: two means then a percentage change, a population from a raw total, or compare percentages."

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one calculation, values given",
   "steps": [
     "<strong>Mean:</strong> add the values, then divide by how many there are.",
     "<strong>Percentage change:</strong> (new − original) ÷ original × 100. The starting value goes on the bottom.",
     "Everything you need is in the question. No converting, no scaling."
   ],
   "example": {"question": "Calculate the mean of 4, 6, 5, 5.",
     "steps": [
       {"label":"Add the values","content":"4 + 6 + 5 + 5 = 20"},
       {"label":"Divide by the count","content":"20 ÷ 4 = 5"},
       {"label":"Check","content":"5 × 4 = 20, back to the sum"},
       {"label":"Answer","content":"Mean = 5","isAnswer":True,"is_answer":True}]}
 },
 "silver": {
   "title": "Silver: convert or scale first",
   "steps": [
     "<strong>Population:</strong> mean per quadrat × (total area ÷ quadrat area). Work out how many quadrats fit the field, then multiply.",
     "<strong>Anomaly:</strong> spot the outlier, remove it, then average what remains, and remember the count drops by one.",
     "<strong>Decimals:</strong> percentage answers may need rounding to the decimal place the question states."
   ],
   "example": {"question": "0.5 m² quadrats in a 100 m² field, mean 5 per quadrat. Estimate the population.",
     "steps": [
       {"label":"Quadrats in the field","content":"100 ÷ 0.5 = 200"},
       {"label":"Scale up","content":"5 × 200 = 1000"},
       {"label":"Check","content":"1000 ÷ 200 = 5, back to the mean"},
       {"label":"Answer","content":"Population = 1000","isAnswer":True,"is_answer":True}]}
 },
 "gold": {
   "title": "Gold: chain two steps",
   "steps": [
     "Two ideas in one question: often a mean (or two) followed by a percentage change, or a population built from a raw total.",
     "Do each part in order and label your intermediate values so you feed the right number into the next step.",
     "Read the data carefully: use the exact years or days named, and ignore distractor values."
   ],
   "example": {"question": "A mean count rises from 5 to 8. Find the percentage change.",
     "steps": [
       {"label":"Change","content":"8 − 5 = 3"},
       {"label":"Divide by the original","content":"3 ÷ 5 = 0.6"},
       {"label":"Times 100","content":"0.6 × 100 = 60"},
       {"label":"Answer","content":"60% increase","isAnswer":True,"is_answer":True}]}
 }
}

pd["guided"] = {
 "opener": {"steps": [
   say("Two quick puzzles, no formulas, just common sense."),
   box("Five friends pool their pocket money: £4, £8, £6, £7, £5. Shared out equally, how much each? £",
       6, "Add it up (£30), then split between 5."),
   say("That equal share is the <strong>mean</strong>: add everything, divide by how many."),
   box("You earned £8 an hour. Your boss adds £2, so now £10. Out of your original £8, the £2 rise is what percentage? ",
       25, "£2 is a quarter of £8, and a quarter is 25%.", post="%"),
   say("That is <strong>percentage change</strong>: the rise divided by what you STARTED with, times 100. The original (£8) always goes on the bottom. Mean and percentage change are two of the three skills here; the third, estimating a population from quadrats, is just a mean scaled up.")
 ]},
 "teach": {
   "bronze": {"display":"A student measures 5 leaf lengths: 6 cm, 9 cm, 7 cm, 8 cm, 10 cm. Calculate the mean length.",
     "steps": [
       say("Mean = sum of values ÷ number of values."),
       box("Add them: 6 + 9 + 7 + 8 + 10 =", 40, "Add all five lengths."),
       box("How many values are there?", 5, "Count them."),
       box("Mean = 40 ÷ 5 =", 8, "Divide the sum by 5."),
       say("So the mean length is <strong>8 cm</strong>."),
       box("Check: mean × count returns the sum. 8 × 5 =", 40, "Multiply back.",
           done="It gives 40, the sum, so 8 cm is right.")]},
   "silver": {"display":"A student uses 0.5 m² quadrats in a 400 m² field. The mean number of buttercups per quadrat is 8. Estimate the population.",
     "steps": [
       say("Population = mean per quadrat × (total area ÷ quadrat area). The new move is scaling the mean up to the whole field."),
       box("How many quadrats fit the field: 400 ÷ 0.5 =", 800, "Field area over one quadrat's area."),
       box("Population = mean × quadrats = 8 × 800 =", 6400, "Multiply the mean by 800."),
       say("So the estimate is <strong>6400 buttercups</strong>."),
       box("Check by density: buttercups per m² = 8 ÷ 0.5 =", 16, "8 in half a square metre."),
       box("16 × 400 =", 6400, "Density times total area.", done="Same 6400 both ways. Gone.")]},
   "gold": {"display":"A pond is sampled in 5 quadrats. In spring the frog counts are 2, 4, 3, 5, 6. In summer the same quadrats give 6, 8, 7, 9, 10. Calculate the percentage change in the mean count.",
     "steps": [
       say("The new move is chaining: find each mean first, then the percentage change between them."),
       box("Spring sum: 2 + 4 + 3 + 5 + 6 =", 20, "Add the five spring counts."),
       box("Spring mean = 20 ÷ 5 =", 4, "Divide by 5."),
       box("Summer sum: 6 + 8 + 7 + 9 + 10 =", 40, "Add the five summer counts."),
       box("Summer mean = 40 ÷ 5 =", 8, "Divide by 5."),
       box("Change in the mean = 8 − 4 =", 4, "New mean minus old mean."),
       box("(4 ÷ 4) × 100 =", 100, "Divide by the original mean of 4, then ×100."),
       say("So the mean count rose by <strong>100%</strong>: it doubled. Gone, that was the whole point.")]}
 }
}

pd["method_card"] = {
 "title": "Sampling, Mean and Percentage Change",
 "steps": [
   "Decide which you need: a mean, a percentage change, or a population estimate.",
   "Mean: add the values, then divide by how many there are (drop any anomaly if told to).",
   "Percentage change: (new − original) ÷ original × 100. The original goes on the bottom.",
   "Population: mean per quadrat × (total area ÷ quadrat area)."
 ],
 "content": ("<p>Three calculations that recur across both Biology papers.</p>"
   "<p><strong>Mean:</strong> add every value, then divide by how many there are. Watch for an <strong>anomalous result</strong> (an outlier): the question may tell you to leave it out.</p>"
   "<p><strong>Percentage change:</strong> (new − original) ÷ original × 100. Always divide by the <em>original</em>. A negative answer is a decrease; an answer above 100% just means the value more than doubled.</p>"
   "<p><strong>Population estimate:</strong> find the mean count per quadrat, then scale up by (total area ÷ quadrat area). Keep the two divisions apart: count over quadrats for the mean, area over area for the scale.</p>")
}

io.open('lesson_biology-data-skills-L03@40fdb75726.json','w',encoding='utf-8').write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("written OK")
