# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_canon.json", encoding="utf-8"))

COR = "border:2px solid #2d2a26; padding:0.5em 1em; text-align:center; font-family:'Source Serif 4',serif; font-size:1.15em; font-weight:600; min-width:2.6em;background:#f5f5f5; border:none;"
TOP = "border:2px solid #2d2a26; padding:0.5em 1em; text-align:center; font-family:'Source Serif 4',serif; font-size:1.15em; font-weight:600; min-width:2.6em;background:#fef2f2; color:#7c2d12;"
SID = "border:2px solid #2d2a26; padding:0.5em 1em; text-align:center; font-family:'Source Serif 4',serif; font-size:1.15em; font-weight:600; min-width:2.6em;background:#eff6ff; color:#1e3a8a;"
CEL = "border:2px solid #2d2a26; padding:0.5em 1em; text-align:center; font-family:'Source Serif 4',serif; font-size:1.15em; font-weight:600; min-width:2.6em;background:#faf8f5;"

def punnett(caption, top, side, cells):
    h = '<figure style="margin:0.8em auto; max-width:fit-content;"><table style="border-collapse:collapse; margin:0 auto;">'
    h += '<tr><th style="%s"></th><th style="%s">%s</th><th style="%s">%s</th></tr>' % (COR, TOP, top[0], TOP, top[1])
    h += '<tr><th style="%s">%s</th><td style="%s">%s</td><td style="%s">%s</td></tr>' % (SID, side[0], CEL, cells[0][0], CEL, cells[0][1])
    h += '<tr><th style="%s">%s</th><td style="%s">%s</td><td style="%s">%s</td></tr>' % (SID, side[1], CEL, cells[1][0], CEL, cells[1][1])
    h += '<figcaption style="text-align:center; font-style:italic; color:#5a5650; margin-top:0.4em; font-size:0.95em;">%s</figcaption></figure>' % caption
    return h

pb = live["problem_bank"]

def box(pre, answer, hint, say=None, post="", phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

def sayx(say): return {"say": say}

# ================= BRONZE =================
bronze = []

b0 = pb["bronze"][0]
b0["hint"] = "Count how many of the 4 cells contain a T, then divide by 4."
b0["misconceptions"] = [
 {"pattern":"forgot_dominant","expect":0.25,"message":"Tt shows the tall phenotype too, because T is dominant. The tall cells are TT, Tt and Tt = 3 out of 4 = 0.75. Only tt (0.25) is short."},
 {"pattern":"gave_count","expect":3,"message":"Give it as a decimal, not a count. 3 tall cells out of 4 = 3 divided by 4 = 0.75."},
]
b0["guided_steps"] = [
 sayx("Each Tt parent makes two gametes, T and t. Combining them fills a 2×2 grid with 4 equally likely cells: <strong>TT, Tt, Tt, tt</strong>."),
 box("How many of the 4 cells show the tall phenotype (contain at least one T)? ", 3, "TT, Tt and Tt all carry a T. Only tt has none."),
 box("Now write that as a decimal. 3 ÷ 4 = ", 0.75, "Divide 3 by 4.", phase="substitute"),
 box("Check: the short cells are 4 − 3 = 1, and 1 ÷ 4 = 0.25. Tall + short = 0.75 + 0.25 = ", 1, "Add 0.75 and 0.25.", phase="substitute", done="The two probabilities cover all 4 cells, so 0.75 (three-quarters tall) is right."),
]
bronze.append(b0)

b1 = pb["bronze"][1]
b1["hint"] = "Count the tt cells, divide by 4, then multiply by 100."
b1["misconceptions"] = [
 {"pattern":"confused_phenotype","expect":75,"message":"tt is the recessive (short) phenotype: 1 cell out of 4 = 25%. 75% is the tall phenotype (the other 3 cells)."},
 {"pattern":"genotype_mixup","expect":50,"message":"Only 1 cell is tt. The 2 middle cells are Tt (heterozygous, 50%), which is a different genotype. tt = 1 out of 4 = 25%."},
]
b1["guided_steps"] = [
 sayx("The Tt × Tt grid has 4 cells: <strong>TT, Tt, Tt, tt</strong>."),
 box("How many cells are tt (short, homozygous recessive)? ", 1, "Only the bottom-right cell has two t alleles."),
 box("As a percentage: (1 ÷ 4) × 100 = ", 25, "1 divided by 4 is 0.25, times 100.", phase="substitute"),
 box("Check: the other 3 cells are tall, (3 ÷ 4) × 100 = 75%, and 25 + 75 = ", 100, "Add 25 and 75.", phase="substitute", done="All four cells add to 100%, so 25% short is right."),
]
bronze.append(b1)

b2 = pb["bronze"][2]
b2["hint"] = "One parent gives only b, so count the cells with a B and divide by 4."
b2["misconceptions"] = [
 {"pattern":"assumed_3to1","expect":0.75,"message":"This is Bb × bb, not a two-carrier cross. Because bb gives only b, the grid is Bb, bb, Bb, bb: dominant = 2 out of 4 = 0.5, not 0.75."},
 {"pattern":"counted_one","expect":0.25,"message":"Two cells are Bb (dominant), not one. 2 out of 4 = 0.5."},
]
b2["guided_steps"] = [
 sayx("One parent is Bb (makes B and b); the other is bb (makes only b). The grid: <strong>Bb, bb, Bb, bb</strong>."),
 box("How many of the 4 cells show the dominant phenotype (contain a B)? ", 2, "The two Bb cells. The bb cells are recessive."),
 box("As a decimal: 2 ÷ 4 = ", 0.5, "Divide 2 by 4.", phase="substitute"),
 box("Check: the recessive bb cells = 2, 2 ÷ 4 = 0.5, and 0.5 + 0.5 = ", 1, "Add 0.5 and 0.5.", phase="substitute", done="Dominant and recessive each fill half the grid, so 0.5 is right."),
]
bronze.append(b2)

# B3 EDITED: Bb x Bb % heterozygous (Bb) = 50
b3 = pb["bronze"][3]
b3["display"] = "In a Bb × Bb cross, what percentage of offspring are expected to be heterozygous (Bb)?"
grid_bbBb = punnett("Bb × Bb offspring", ["B","b"], ["B","b"], [["BB","Bb"],["Bb","bb"]])
b3["question"] = grid_bbBb + '<p style="margin-top:0.8em;">In a <strong>Bb × Bb</strong> cross, what percentage of offspring are expected to be heterozygous (Bb)?</p>'
b3["solutions"] = [50]
b3["equation_hint"] = "Bb appears in 2 of the 4 cells"
b3["hint"] = "Heterozygous means one of each letter (Bb): count those cells, divide by 4, times 100."
b3["misconceptions"] = [
 {"pattern":"counted_homozygous","expect":25,"message":"Bb (one of each letter) appears in 2 cells, not 1: 2 out of 4 = 50%. Each homozygous type, BB or bb, is a 25% outcome."},
 {"pattern":"counted_phenotype","expect":75,"message":"Heterozygous means exactly Bb, the 2 middle cells = 50%. 75% counts every cell with a B, which is the dominant phenotype (BB and Bb)."},
]
b3["guided_steps"] = [
 sayx("The Bb × Bb grid has 4 cells: <strong>BB, Bb, Bb, bb</strong>."),
 box("How many cells are heterozygous (Bb, one of each letter)? ", 2, "The two middle cells, Bb and Bb. BB and bb are homozygous."),
 box("As a percentage: (2 ÷ 4) × 100 = ", 50, "2 divided by 4 is 0.5, times 100.", phase="substitute"),
 box("Check: the homozygous cells are BB (1) and bb (1) = 2 cells = 50%, and 50 + 50 = ", 100, "Add 50 and 50.", phase="substitute", done="Heterozygous and homozygous each make up half the grid, so 50% is right."),
]
bronze.append(b3)

b4 = pb["bronze"][4]
b4["hint"] = "Count how many cells have one T and one t."
b4["misconceptions"] = [
 {"pattern":"counted_homozygous","expect":1,"message":"Tt (one T and one t) fills 2 cells, the two mixed ones. TT and tt each fill only 1 cell."},
 {"pattern":"counted_phenotype","expect":3,"message":"The ratio asks for the Tt genotype only, which is 2. 3 is how many show the tall phenotype (TT plus both Tt)."},
]
b4["guided_steps"] = [
 sayx("The Tt × Tt grid has 4 cells: <strong>TT, Tt, Tt, tt</strong>. The genotype ratio counts each genotype separately."),
 box("How many cells are TT? ", 1, "Only the top-left cell has two T alleles."),
 box("How many cells are Tt (one T, one t)? ", 2, "The top-right and bottom-left cells.", phase="substitute"),
 box("Check the whole ratio adds up: 1 (TT) + 2 (Tt) + 1 (tt) = ", 4, "Add 1 + 2 + 1.", phase="substitute", done="The ratio 1:2:1 covers all 4 cells, so Tt = 2 is right."),
]
bronze.append(b4)

# ================= SILVER =================
silver = []

s0 = pb["silver"][0]
s0["hint"] = "Only ff has the condition: count that cell, divide by 4, times 100."
s0["misconceptions"] = [
 {"pattern":"carriers_counted","expect":50,"message":"Carriers (Ff) do not have cystic fibrosis, because F is dominant. Only ff is affected: 1 out of 4 = 25%. The 50% are healthy carriers."},
 {"pattern":"confused_unaffected","expect":75,"message":"ff (affected) is 1 cell = 25%. 75% is the chance of NOT having the condition."},
]
s0["guided_steps"] = [
 sayx("Both parents are carriers, Ff, so each makes F and f gametes. The grid: <strong>FF, Ff, Ff, ff</strong>."),
 box("How many of the 4 cells are ff (two recessive alleles, so has cystic fibrosis)? ", 1, "Only the bottom-right cell has two f alleles."),
 box("As a percentage: (1 ÷ 4) × 100 = ", 25, "1 divided by 4 is 0.25, times 100.", phase="substitute"),
 box("Check: the unaffected cells (FF, Ff, Ff) = 3, (3 ÷ 4) × 100 = 75%, and 25 + 75 = ", 100, "Add 25 and 75.", phase="substitute", done="Affected and unaffected cover all 4 cells, so a 25% chance of cystic fibrosis is right."),
]
silver.append(s0)

s1 = pb["silver"][1]
s1["hint"] = "A carrier is Ff: count both middle cells, divide by 4, times 100."
s1["misconceptions"] = [
 {"pattern":"counted_one","expect":25,"message":"Ff appears in 2 cells, not 1: 2 out of 4 = 50%. A single cell (25%) would be FF or ff."},
 {"pattern":"added_FF","expect":75,"message":"A carrier is Ff specifically, the 2 middle cells = 50%. 75% counts everyone without the disease (FF and Ff together)."},
]
s1["guided_steps"] = [
 sayx("Same Ff × Ff grid: <strong>FF, Ff, Ff, ff</strong>. A carrier has one F and one f but does not have the condition."),
 box("How many cells are Ff (carriers)? ", 2, "The two middle cells, Ff and Ff."),
 box("As a percentage: (2 ÷ 4) × 100 = ", 50, "2 divided by 4 is 0.5, times 100.", phase="substitute"),
 box("Check: FF (1) + Ff (2) + ff (1) = ", 4, "Add 1 + 2 + 1.", phase="substitute", done="Healthy FF (25%), carriers Ff (50%) and affected ff (25%) fill all 4 cells, so 50% carriers is right."),
]
silver.append(s1)

s2 = pb["silver"][2]
s2["hint"] = "Find the probability of bb from the grid, then multiply by 20."
s2["misconceptions"] = [
 {"pattern":"used_quarter","expect":5,"message":"Bb × bb gives a 1:1 ratio, so half are recessive: 0.5 × 20 = 10. Using a quarter (5) is the Tt × Tt result, not this cross."},
 {"pattern":"used_threequarter","expect":15,"message":"This is not a two-carrier cross. bb gives only b, so recessive = 2 out of 4 = half = 10, not three-quarters."},
]
s2["guided_steps"] = [
 sayx("Bb × bb grid: <strong>Bb, bb, Bb, bb</strong>. The recessive phenotype is bb."),
 box("How many of the 4 cells are bb (recessive)? ", 2, "The two bb cells."),
 box("That is a probability of 2 ÷ 4 = 0.5. Expected number = 0.5 × 20 = ", 10, "Half of 20.", phase="substitute"),
 box("Check: the other half, 0.5 × 20 = 10, are dominant, and 10 + 10 = ", 20, "Add 10 and 10.", phase="substitute", done="The two groups add back to all 20 offspring, so 10 recessive is right."),
]
silver.append(s2)

# S3 EDITED: Tt x Tt out of 80, Tt = 40
s3 = pb["silver"][3]
s3["display"] = "In a Tt × Tt cross, how many out of 80 expected offspring would be heterozygous (Tt)?"
grid_ttTt = punnett("Tt × Tt offspring", ["T","t"], ["T","t"], [["TT","Tt"],["Tt","tt"]])
s3["question"] = grid_ttTt + '<p style="margin-top:0.8em;">In a <strong>Tt × Tt</strong> cross, how many out of 80 expected offspring would be heterozygous (Tt)?</p>'
s3["solutions"] = [40]
s3["equation_hint"] = "Tt occurs in 2 of 4 cells = 50%"
s3["hint"] = "Tt fills 2 of the 4 cells (half), so find half of 80."
s3["misconceptions"] = [
 {"pattern":"used_quarter","expect":20,"message":"Tt fills 2 of the 4 cells, so half: 0.5 × 80 = 40. A quarter (20) would be just one genotype, like TT."},
 {"pattern":"used_phenotype","expect":60,"message":"Heterozygous Tt is 2 cells = half = 40. Three-quarters (60) is the tall phenotype, which also includes TT."},
]
s3["guided_steps"] = [
 sayx("Tt × Tt grid: <strong>TT, Tt, Tt, tt</strong>. Heterozygous means Tt."),
 box("How many of the 4 cells are Tt? ", 2, "The two mixed cells."),
 box("That is 2 ÷ 4 = 0.5. Expected number = 0.5 × 80 = ", 40, "Half of 80.", phase="substitute"),
 box("Check: the homozygous offspring (TT and tt) are the other half, 0.5 × 80 = 40, and 40 + 40 = ", 80, "Add 40 and 40.", phase="substitute", done="Both halves add back to 80, so 40 heterozygous is right."),
]
silver.append(s3)

# ================= GOLD =================
gold = []

# G0 REBUILT: test cross, tall unknown x tt, short appear -> Tt = 2
g0 = pb["gold"][0]
g0["unit"] = ""
g0["display"] = "A tall pea plant has an unknown genotype: it could be TT or Tt (T = tall dominant, t = short recessive). It is crossed with a short plant (tt). Some of the offspring are short. What is the tall plant's genotype? Enter 1 for TT or 2 for Tt."
gA = punnett("If TT × tt: every offspring is Tt (all tall)", ["T","T"], ["t","t"], [["Tt","Tt"],["Tt","Tt"]])
gB = punnett("If Tt × tt: offspring are Tt, tt, Tt, tt (half short)", ["T","t"], ["t","t"], [["Tt","tt"],["Tt","tt"]])
g0["question"] = ('<p style="text-align:center; font-style:italic; color:#5a5650;">A tall plant could be TT or Tt. Test each cross against the short parent (tt), which passes on only t.</p>'
 + gA + gB
 + '<p style="margin-top:0.8em;">Some of the offspring are <strong>short</strong>. What is the tall plant’s genotype? <em>Enter 1 for TT or 2 for Tt.</em></p>')
g0["solutions"] = [2]
g0["calculator"] = False
g0["input_type"] = "single_value"
g0["hint"] = "Only one of the two crosses can produce short (tt) offspring: pick that parent's genotype."
g0["misconceptions"] = [
 {"pattern":"chose_TT","expect":1,"message":"TT × tt gives only Tt offspring, all tall, so no short ones could appear. Because short offspring DID appear, the tall parent must carry a t: it is Tt."},
]
g0["guided_steps"] = [
 sayx("For short offspring (tt) to appear, both parents must pass on a t. The short parent tt gives only t, so the tall parent must also carry a t. Test both possibilities."),
 box("First try TT × tt. Every offspring cell is Tt. How many of the 4 cells are short (tt)? ", 0, "TT gives only T, so no cell can be tt."),
 box("Now try Tt × tt. The cells are Tt, tt, Tt, tt. How many are short (tt)? ", 2, "The two tt cells.", phase="substitute"),
 box("Short offspring actually appeared, so the tall parent is the one that can make them. Enter 1 for TT or 2 for Tt: ", 2, "The Tt cross is the only one that produces short offspring.", phase="substitute"),
 box("Check: Tt × tt makes 2 short out of 4, a probability of 2 ÷ 4 = ", 0.5, "Divide 2 by 4.", phase="substitute", done="About half the offspring are expected short, which matches seeing short ones. So the tall plant is Tt."),
]
gold.append(g0)

# G1 EDITED: 6 children, expected girls = 3
g1 = pb["gold"][1]
g1["unit"] = ""
g1["display"] = "In humans, sex is determined by X and Y chromosomes. A couple have 6 children. Based on expected probability (50% each), how many would be expected to be girls? Enter as a whole number."
grid_xy = punnett("XX (mother) × XY (father): XX = girl, XY = boy", ["X","Y"], ["X","X"], [["XX","XY"],["XX","XY"]])
g1["question"] = grid_xy + '<p style="margin-top:0.8em;">In humans, sex is determined by X and Y chromosomes. A couple have 6 children. Based on expected probability (50% each), how many would be expected to be girls?</p>'
g1["solutions"] = [3]
g1["hint"] = "Girls (XX) are half the outcomes: find half of 6."
g1["misconceptions"] = [
 {"pattern":"used_grid_count","expect":2,"message":"2 is the number of girl (XX) cells in the 4-cell grid. Scale it to the 6 children: half of 6 = 0.5 × 6 = 3."},
]
g1["guided_steps"] = [
 sayx("Sex is decided like a coin flip. The mother is XX (gives only X); the father is XY (gives X or Y). The grid: <strong>XX, XY, XX, XY</strong>."),
 box("How many of the 4 cells are XX (girl)? ", 2, "The two XX cells."),
 box("That is a probability of 2 ÷ 4 = 0.5. Expected girls = 0.5 × 6 = ", 3, "Half of 6.", phase="substitute"),
 box("Check: expected boys = 0.5 × 6 = 3, and 3 + 3 = ", 6, "Add 3 and 3.", phase="substitute", done="Girls and boys are expected in equal halves, adding to all 6 children, so 3 is right."),
]
gold.append(g1)

# G2: 28/40 tall % = 70
g2 = pb["gold"][2]
g2["hint"] = "Actual percentage = (number tall ÷ total) × 100."
g2["misconceptions"] = [
 {"pattern":"gave_expected","expect":75,"message":"The expected ratio gives 75%, but the question asks for the ACTUAL percentage from the data: (28 ÷ 40) × 100 = 70%. Real results differ from the expected ratio because fertilisation is random."},
 {"pattern":"gave_count","expect":28,"message":"28 is the number of tall plants, not a percentage. Turn it into a percentage: (28 ÷ 40) × 100 = 70%."},
]
g2["guided_steps"] = [
 sayx("The Tt × Tt grid expects 3 out of 4 tall = 75%. But here we have real data: 28 tall out of 40. The question wants the ACTUAL percentage."),
 box("The 28 tall plants are out of how many offspring in total? ", 40, "The total number of offspring produced."),
 box("Actual percentage tall = (28 ÷ 40) × 100 = ", 70, "28 divided by 40, times 100.", phase="substitute"),
 box("Check: short plants = 40 − 28 = 12, (12 ÷ 40) × 100 = 30%, and 70 + 30 = ", 100, "Add 70 and 30.", phase="substitute", done="Tall and short percentages cover all the offspring, so 70% is right, close to the expected 75%."),
]
gold.append(g2)

pb_new = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Read a probability straight from the Punnett square as a fraction, decimal or percentage.",
 "silver_description": "Scale the probability to a number of offspring, or work with a real genetic condition.",
 "gold_description": "Deduce a hidden genotype from the offspring, or compare real results with the expected ratio.",
}

def ex_step(label, content, is_answer=False):
    d = {"label": label, "content": content}
    if is_answer:
        d["isAnswer"] = True; d["is_answer"] = True
    return d

tier_guides = {
 "bronze": {
  "title": "Bronze: read the probability off the grid",
  "steps": [
   "Write each parent's gametes, then fill the 2×2 Punnett square. Every cross gives 4 equally likely cells.",
   "Count how many cells match the outcome asked for, and put that over 4 (for example 3 out of 4).",
   "Convert to the form asked for: a decimal (3 ÷ 4 = 0.75) or a percentage (× 100 = 75%)."
  ],
  "example": {
   "question": "In a Gg × Gg cross (G dominant), what fraction of offspring are homozygous recessive (gg)? Give a decimal.",
   "steps": [
    ex_step("Fill grid", "<p>Gg × Gg gives GG, Gg, Gg, gg.</p>"),
    ex_step("Count", "<p>gg appears in 1 cell out of 4.</p>"),
    ex_step("Convert", "<p>1 ÷ 4 = 0.25</p>"),
    ex_step("Check", "<p>Dominant = 3/4 = 0.75, and 0.25 + 0.75 = 1 ✓</p>"),
    ex_step("Answer", "<p><strong>0.25</strong></p>", True),
   ]
  }
 },
 "silver": {
  "title": "Silver: turn a probability into a number",
  "steps": [
   "Find the probability from the grid as a fraction over 4, as usual.",
   "For an expected count, multiply that probability by the total number of offspring: 0.5 × 20 = 10.",
   "Watch the cross type: Bb × bb gives a 1:1 ratio (half recessive), not the 3:1 of a two-carrier cross."
  ],
  "example": {
   "question": "A Bb × bb cross gives 24 offspring. How many are expected to be recessive (bb)?",
   "steps": [
    ex_step("Fill grid", "<p>Bb × bb gives Bb, bb, Bb, bb.</p>"),
    ex_step("Probability", "<p>bb = 2 out of 4 = 0.5.</p>"),
    ex_step("Scale", "<p>0.5 × 24 = 12</p>"),
    ex_step("Check", "<p>Dominant = 0.5 × 24 = 12, and 12 + 12 = 24 ✓</p>"),
    ex_step("Answer", "<p><strong>12 offspring</strong></p>", True),
   ]
  }
 },
 "gold": {
  "title": "Gold: reason backwards, or compare with real data",
  "steps": [
   "If you are given the offspring and asked for a hidden genotype, test each possible cross with a Punnett square and keep the one that fits.",
   "If you are given real numbers, find the actual percentage with (count ÷ total) × 100.",
   "Remember real results wobble around the expected ratio, because fertilisation is random."
  ],
  "example": {
   "question": "A Tt × Tt cross gave 60 offspring, of which 42 were tall. What percentage were tall?",
   "steps": [
    ex_step("Real data", "<p>42 tall out of 60 total.</p>"),
    ex_step("Percentage", "<p>(42 ÷ 60) × 100 = 70%</p>"),
    ex_step("Compare", "<p>Expected was 3/4 = 75%, so results are close but not exact.</p>"),
    ex_step("Check", "<p>Short = 18, (18 ÷ 60) × 100 = 30%, and 70 + 30 = 100 ✓</p>"),
    ex_step("Answer", "<p><strong>70%</strong></p>", True),
   ]
  }
 }
}

guided = {
 "opener": {
  "label": "Before any genetics",
  "display": "Flip two coins together.<br>The four equally likely results:<br><strong>HH&nbsp;&nbsp;HT&nbsp;&nbsp;TH&nbsp;&nbsp;TT</strong>",
  "steps": [
   {"say":"Two coins, flipped together, give four equally likely results: HH, HT, TH, TT. No genetics yet, just count.",
    "pre":"How many of the 4 results show two tails (TT)? ","post":"","answer":1,
    "hint":"Only the last one, TT."},
   {"say":"So the chance of two tails is 1 out of 4. Write it as a percentage:",
    "pre":"(1 ÷ 4) × 100 = ","post":"","answer":25,
    "hint":"1 divided by 4 is 0.25, times 100."},
   {"say":"That is genetics. Each <strong>Tt</strong> parent is like a coin: half its gametes carry T, half carry t. A <strong>Tt × Tt</strong> cross has the same four equally likely results, TT, Tt, Tt, tt, and 'two smalls' (tt) turns up 1 time in 4, exactly 25%. A Punnett square is just this table of outcomes."}
  ]
 },
 "teach": {
  "bronze": {
   "display": "In an Rr × Rr cross (R = round dominant, r = wrinkled recessive), what percentage of offspring are wrinkled (rr)?",
   "label": "Together: your first one",
   "steps": [
    sayx("Each Rr parent makes R and r gametes. Fill the 2×2 grid: <strong>RR, Rr, Rr, rr</strong>."),
    box("How many of the 4 cells are RR? ", 1, "Top-left only."),
    box("How many cells are Rr? ", 2, "The two mixed cells."),
    box("How many cells are rr (wrinkled)? ", 1, "Bottom-right only."),
    box("So wrinkled is 1 out of 4. As a percentage: (1 ÷ 4) × 100 = ", 25, "1 divided by 4, times 100.", done="Gone. Count the matching cells, put them over 4, turn it into a percentage. That is the whole method."),
   ]
  },
  "silver": {
   "display": "A Dd × Dd cross produces 60 offspring (D dominant). How many are expected to show the recessive phenotype (dd)?",
   "label": "Together: the silver move",
   "steps": [
    sayx("Dd × Dd grid: <strong>DD, Dd, Dd, dd</strong>. The recessive phenotype is dd."),
    box("How many of the 4 cells are dd? ", 1, "Bottom-right only."),
    box("As a probability that is 1 ÷ 4 = ", 0.25, "Divide 1 by 4."),
    box("Expected number = 0.25 × 60 = ", 15, "A quarter of 60."),
    box("Check: the dominant phenotype is the other 3 cells, 0.75 × 60 = 45, and 15 + 45 = ", 60, "Add 15 and 45.", done="The two groups rebuild all 60 offspring, so 15 is right. The new move: turn the probability into a count by multiplying by the number of offspring."),
   ]
  },
  "gold": {
   "display": "A tall plant of unknown genotype is crossed with a short plant (tt). Some offspring are short. Is the tall plant TT or Tt? Enter 1 for TT or 2 for Tt.",
   "label": "Together: the gold move",
   "steps": [
    sayx("Test both possibilities against the short parent tt, which passes on only t."),
    box("First try TT × tt. Every offspring is Tt. How many of the 4 cells are short (tt)? ", 0, "TT gives only T, so no cell can be tt."),
    box("Now try Tt × tt: the cells are Tt, tt, Tt, tt. How many are short (tt)? ", 2, "The two tt cells."),
    box("Short offspring appeared, so which genotype is the tall parent? Enter 1 for TT or 2 for Tt: ", 2, "Only the Tt cross makes short offspring."),
    box("Check: Tt × tt makes 2 short out of 4, probability 2 ÷ 4 = ", 0.5, "Divide 2 by 4.", done="Half the offspring are expected short, matching the real short ones. The tall plant is Tt. The new move: rule genotypes in or out by which cross fits the evidence."),
   ]
  }
 }
}

method_card = {
 "title": "Punnett Squares and Genetic Probability",
 "steps": [
  "Write parental genotypes and identify the gametes each parent can produce",
  "Draw the 2×2 Punnett square, placing gametes along the top and left side",
  "Fill in the four cells by combining one allele from each parent",
  "Count outcomes, then express probability as a fraction, decimal or percentage"
 ],
 "content": ("<p>A <strong>Punnett square</strong> predicts the probability of each offspring genotype. It does not guarantee exact numbers.</p>"
  "<p>A capital letter is the dominant allele (its effect shows in BB or Bb); a lower-case letter is recessive (its effect shows only in bb).</p>"
  "<p>Every 2×2 cross gives <strong>4 equally likely cells</strong>. Count how many cells match the outcome, put that over 4, then convert: a decimal (÷ 4) or a percentage (÷ 4, × 100).</p>"
  "<p>A Tt × Tt cross gives a 3:1 phenotype ratio (75% dominant); a Bb × bb cross gives 1:1 (50% each). Do not confuse the genotype ratio (1:2:1) with the phenotype ratio (3:1), and always count all 4 cells, never 3.</p>"),
 "example": "<p><strong>Tt × Tt, chance of short (tt)?</strong> Grid: TT, Tt, Tt, tt. tt = 1 of 4 = 1 ÷ 4 = 0.25 = 25%.</p>"
}

def strip_em(obj):
    if isinstance(obj, dict):
        return {k: strip_em(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_em(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ", ")
    return obj

worked_examples = strip_em(live.get("worked_examples", []))
exam_context = strip_em(live.get("exam_context", {}))
topic_links = live.get("topic_links", {"prerequisites": []})
related_videos = live.get("related_videos", [])

out = {
 "method_card": method_card,
 "topic_links": topic_links,
 "exam_context": exam_context,
 "problem_bank": pb_new,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

out = strip_em(out)
s = json.dumps(out, ensure_ascii=False)
assert "—" not in s, "EM DASH remains"

json.dump(out, io.open("lesson_biology-data-skills-L02@6e66d8eeba.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK bronze", [p["solutions"] for p in bronze], "silver", [p["solutions"] for p in silver], "gold", [p["solutions"] for p in gold])
