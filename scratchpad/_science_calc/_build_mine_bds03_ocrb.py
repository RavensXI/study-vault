# -*- coding: utf-8 -*-
import json, io

KEY = "biology-data-skills-L03@86a105121c"

def prob(unit, display, sol, misc, gs, hint, accept=None, eqh=None):
    p = {"unit": unit, "display": display, "solutions": [sol],
         "calculator": True, "input_type": "single_value",
         "hint": hint, "misconceptions": misc, "guided_steps": gs}
    if accept is not None: p["accept"] = accept
    if eqh is not None: p["equation_hint"] = eqh
    return p

def m(pattern, message, expect):
    return {"check": "common", "pattern": pattern, "message": message, "expect": expect}

# ---------------- BRONZE ----------------
bronze = [
 prob("", "A student records earthworm counts in 6 quadrats: 4, 7, 5, 6, 4, 8. Calculate the mean number per quadrat to 2 decimal places.",
   5.67,
   [m("forgot_divide", "Sum = 34. Mean = 34 ÷ 6 = 5.67. You must divide the total by how many values there are, not stop at the sum.", 34)],
   [
    {"say": "Mean = sum of values ÷ number of values. State the equation before the numbers."},
    {"pre": "Add all the values: 4 + 7 + 5 + 6 + 4 + 8 =", "answer": 34, "hint": "Add every value together.", "phase": "substitute"},
    {"pre": "Count how many values there are:", "answer": 6, "hint": "Count them carefully."},
    {"pre": "Divide the sum by the count: 34 ÷ 6 = (to 2 d.p.)", "answer": 5.67, "hint": "Share the total between 6, then round to 2 d.p."},
    {"say": "So the mean is <strong>5.67 earthworms per quadrat</strong>."},
    {"pre": "Check: 5.67 × 6 =", "answer": 34.02, "hint": "Multiply back; it should land near the sum.", "done": "It returns about 34, the sum, allowing for rounding, so 5.67 is right."}
   ],
   "Add the six counts, then divide by six and round to 2 d.p.",
   accept=0.01, eqh="mean = sum ÷ number of values"),

 prob("%", "A population was 200 in Year 1 and 250 in Year 2. Calculate the percentage change.",
   25,
   [m("wrong_denominator", "Divide by the ORIGINAL value (200): (250 − 200) ÷ 200 × 100 = 25%. Dividing by the new value (250) gives 20%, which is wrong.", 20)],
   [
    {"say": "Percentage change = (new − original) ÷ original × 100. The ORIGINAL goes on the bottom."},
    {"pre": "Change = new − original = 250 − 200 =", "answer": 50, "hint": "Take the starting value from the new one.", "phase": "substitute"},
    {"pre": "Divide by the original (200): 50 ÷ 200 =", "answer": 0.25, "hint": "Divide the change by the starting value."},
    {"pre": "Multiply by 100: 0.25 × 100 =", "answer": 25, "hint": "Shift two places for a percentage."},
    {"say": "So the percentage change is <strong>25%</strong>, an increase."},
    {"pre": "Check: 25% of 200 is 0.25 × 200 =", "answer": 50, "hint": "Should match the change you found.", "done": "It matches the change of 50, so 25% is right."}
   ],
   "Change over the original value (200), times 100.",
   eqh="% change = (new − original) ÷ original × 100"),

 prob("%", "A population was 300 in Year 1 and 240 in Year 3. Calculate the percentage change (include sign).",
   -20,
   [m("wrong_denominator", "Divide by the ORIGINAL (300): (240 − 300) ÷ 300 × 100 = −60 ÷ 300 × 100 = −20%. Dividing by the new value (240) gives −25%.", -25)],
   [
    {"say": "Percentage change = (new − original) ÷ original × 100. A fall gives a negative answer."},
    {"pre": "Change = new − original = 240 − 300 =", "answer": -60, "hint": "Take the starting value from the new one.", "phase": "substitute"},
    {"pre": "Divide by the original (300): -60 ÷ 300 =", "answer": -0.2, "hint": "Divide the change by the starting value."},
    {"pre": "Multiply by 100: -0.2 × 100 =", "answer": -20, "hint": "Shift two places for a percentage."},
    {"say": "So the percentage change is <strong>-20%</strong>, a decrease."},
    {"pre": "Check: -20% of 300 is -0.2 × 300 =", "answer": -60, "hint": "Should match the fall you found.", "done": "It matches the fall of 60, so -20% is right."}
   ],
   "It fell, so expect a negative; divide the change by 300.",
   eqh="Negative result means a decrease"),

 prob("", "Five quadrats (each 1 m²) placed in a 50 m² area count 3, 2, 4, 3, 3 plants. Calculate the mean per quadrat.",
   3,
   [m("forgot_divide", "Sum = 15. Mean = 15 ÷ 5 = 3 plants per quadrat. Do not stop at the sum of 15.", 15)],
   [
    {"say": "Mean = sum of values ÷ number of values."},
    {"pre": "Add all the values: 3 + 2 + 4 + 3 + 3 =", "answer": 15, "hint": "Add every value together.", "phase": "substitute"},
    {"pre": "Count how many values there are:", "answer": 5, "hint": "Count them carefully."},
    {"pre": "Divide the sum by the count: 15 ÷ 5 =", "answer": 3, "hint": "Share the total between 5."},
    {"say": "So the mean is <strong>3 plants per quadrat</strong>."},
    {"pre": "Check: mean × count returns the sum. 3 × 5 =", "answer": 15, "hint": "Multiply back to the sum.", "done": "It returns 15, the sum, so 3 is right."}
   ],
   "Add the five counts, then divide by five.",
   eqh="mean = sum ÷ 5"),

 prob("", "Using the mean of 3 plants per quadrat (1 m² quadrats) in a 50 m² area, estimate the total population.",
   150,
   [m("wrong_formula", "Population = mean per quadrat × (total area ÷ quadrat area) = 3 × (50 ÷ 1) = 3 × 50 = 150. Scale the mean up to the whole area.", None)],
   [
    {"say": "Population = mean per quadrat × (total area ÷ quadrat area)."},
    {"pre": "How many quadrats fit the area: 50 ÷ 1 =", "answer": 50, "hint": "Total area over one quadrat's area.", "phase": "substitute"},
    {"pre": "Population = mean × quadrats = 3 × 50 =", "answer": 150, "hint": "Multiply the mean by 50."},
    {"say": "So the estimated population is <strong>150 plants</strong>."},
    {"pre": "Check: 150 ÷ 50 should return the mean. 150 ÷ 50 =", "answer": 3, "hint": "Divide back to recover the mean.", "done": "It returns the mean of 3, so 150 is right."}
   ],
   "Multiply the mean by (total area ÷ quadrat area).",
   eqh="population = mean × (total area ÷ quadrat area)"),

 prob("%", "A plant was 5 cm tall in Week 1 and 15 cm tall in Week 4. Calculate the percentage change in height.",
   200,
   [m("wrong_denominator", "Divide by the ORIGINAL height (5): (15 − 5) ÷ 5 × 100 = 10 ÷ 5 × 100 = 200%. Dividing by the new value (15) gives about 67%.", 66.67)],
   [
    {"say": "Percentage change = (new − original) ÷ original × 100."},
    {"pre": "Change = new − original = 15 − 5 =", "answer": 10, "hint": "New minus original.", "phase": "substitute"},
    {"pre": "Divide by the original (5): 10 ÷ 5 =", "answer": 2, "hint": "Divide the change by the starting height."},
    {"pre": "Multiply by 100: 2 × 100 =", "answer": 200, "hint": "Shift two places for a percentage."},
    {"say": "So the percentage change is <strong>200%</strong>: the plant tripled in height."},
    {"pre": "Check: 200% of 5 is 2 × 5 =", "answer": 10, "hint": "Should match the rise you found.", "done": "It matches the rise of 10, so 200% is right."}
   ],
   "Divide the rise by the starting height (5), times 100.",
   eqh="% change = (new − original) ÷ original × 100"),
]

# ---------------- SILVER ----------------
silver = [
 prob("", "A student places 10 quadrats (each 1 m²) in a 200 m² meadow. Dandelion counts: 3,5,4,6,3,5,4,4,6,5. Calculate the estimated total population.",
   900,
   [m("forgot_step", "Find the MEAN first: sum = 45, mean = 45 ÷ 10 = 4.5. Then scale: 4.5 × (200 ÷ 1) = 900. Multiplying the raw total 45 by 200 skips the mean and gives 9000.", 9000)],
   [
    {"say": "Two steps: find the mean per quadrat, then scale up. Population = mean × (total area ÷ quadrat area)."},
    {"pre": "Add the ten counts: 3 + 5 + 4 + 6 + 3 + 5 + 4 + 4 + 6 + 5 =", "answer": 45, "hint": "Add all ten.", "phase": "substitute"},
    {"pre": "Mean per quadrat = 45 ÷ 10 =", "answer": 4.5, "hint": "Divide by the 10 quadrats."},
    {"pre": "Quadrats in the meadow = 200 ÷ 1 =", "answer": 200, "hint": "Field area over quadrat area."},
    {"pre": "Population = 4.5 × 200 =", "answer": 900, "hint": "Mean times number of quadrats."},
    {"say": "So the estimated population is <strong>900 dandelions</strong>."},
    {"pre": "Check: 900 ÷ 200 should return the mean. 900 ÷ 200 =", "answer": 4.5, "hint": "Divide back to recover the mean.", "done": "It returns the mean of 4.5, so 900 is right."}
   ],
   "Find the mean per quadrat, then scale by area.",
   eqh="First find mean, then multiply by total area ÷ quadrat area"),

 prob("%", "A field study recorded 240 bird territories in Year 1. By Year 5 it had fallen to 180. Calculate the percentage change.",
   -25,
   [m("wrong_denominator", "Divide by the ORIGINAL (240): (180 − 240) ÷ 240 × 100 = −60 ÷ 240 × 100 = −25%. Dividing by the new value (180) gives about −33%.", -33.33)],
   [
    {"say": "Percentage change = (new − original) ÷ original × 100. A fall gives a negative answer."},
    {"pre": "Change = new − original = 180 − 240 =", "answer": -60, "hint": "New minus original.", "phase": "substitute"},
    {"pre": "Divide by the original (240): -60 ÷ 240 =", "answer": -0.25, "hint": "Divide by the starting value."},
    {"pre": "Multiply by 100: -0.25 × 100 =", "answer": -25, "hint": "Shift two places for a percentage."},
    {"say": "So the percentage change is <strong>-25%</strong>, a decrease of one quarter."},
    {"pre": "Check: -25% of 240 is -0.25 × 240 =", "answer": -60, "hint": "Should match the fall you found.", "done": "It matches the fall of 60, so -25% is right."}
   ],
   "Divide the fall by the original 240, times 100.",
   eqh="% change = (new − original) ÷ original × 100"),

 prob("", "Quadrat counts for a 0.5 m² quadrat in a 100 m² area: 2, 3, 1, 4, 2. Calculate the estimated total population.",
   480,
   [m("wrong_area", "The quadrat is 0.5 m², so total area ÷ quadrat area = 100 ÷ 0.5 = 200 (not 100). Mean = 2.4, population = 2.4 × 200 = 480. Using 100 directly gives 240.", 240)],
   [
    {"say": "Find the mean, then scale. Population = mean × (total area ÷ quadrat area). The quadrat is 0.5 m², not 1."},
    {"pre": "Add the five counts: 2 + 3 + 1 + 4 + 2 =", "answer": 12, "hint": "Add all five.", "phase": "substitute"},
    {"pre": "Mean per quadrat = 12 ÷ 5 =", "answer": 2.4, "hint": "Divide by the 5 quadrats."},
    {"pre": "Quadrats that fit the area = 100 ÷ 0.5 =", "answer": 200, "hint": "Total area over quadrat area, not 100 ÷ 5."},
    {"pre": "Population = 2.4 × 200 =", "answer": 480, "hint": "Mean times number of quadrats."},
    {"say": "So the estimated population is <strong>480 plants</strong>."},
    {"pre": "Check: 480 ÷ 200 should return the mean. 480 ÷ 200 =", "answer": 2.4, "hint": "Divide back to recover the mean.", "done": "It returns the mean of 2.4, so 480 is right."}
   ],
   "Mean first, then multiply by (total area ÷ 0.5).",
   eqh="Mean = sum/5. Population = mean × (total area ÷ quadrat area)"),

 prob("%", "A woodland had 350 oak trees in Year 1 and 427 in Year 4. Calculate the percentage change to 1 decimal place.",
   22.0,
   [m("wrong_denominator", "Divide by the ORIGINAL (350): (427 − 350) ÷ 350 × 100 = 77 ÷ 350 × 100 = 22.0%. Dividing by the new value (427) gives about 18%.", 18.03)],
   [
    {"say": "Percentage change = (new − original) ÷ original × 100. Round to 1 decimal place at the end."},
    {"pre": "Change = new − original = 427 − 350 =", "answer": 77, "hint": "New minus original.", "phase": "substitute"},
    {"pre": "Divide by the original (350): 77 ÷ 350 =", "answer": 0.22, "hint": "Divide by the starting count."},
    {"pre": "Multiply by 100: 0.22 × 100 =", "answer": 22, "hint": "Shift two places for a percentage."},
    {"say": "So the percentage change is <strong>22.0%</strong>, an increase."},
    {"pre": "Check: 22% of 350 is 0.22 × 350 =", "answer": 77, "hint": "Should match the rise you found.", "done": "It matches the rise of 77, so 22.0% is right."}
   ],
   "Divide the rise by the original 350, then round to 1 d.p.",
   accept=0.1, eqh="% change = (427 − 350) ÷ 350 × 100"),
]

# ---------------- GOLD ----------------
gold = [
 prob("", "A student records dandelion counts in eight 0.5 m² quadrats in a 400 m² field: 5, 3, 6, 4, 5, 7, 4, 6. Estimate the total population.",
   4000,
   [
    m("wrong_area", "The quadrat is 0.5 m². Total area ÷ quadrat area = 400 ÷ 0.5 = 800 (not 400). Mean = 5, population = 5 × 800 = 4000. Using 400 directly gives 2000.", 2000),
    m("forgot_step", "Find the MEAN first (40 ÷ 8 = 5), then scale: 5 × 800 = 4000. Multiplying the raw total 40 by 800 skips the mean and gives 32000.", 32000)
   ],
   [
    {"say": "Two steps: find the mean per quadrat, then scale to the whole field. The quadrat is 0.5 m², so watch the area division."},
    {"pre": "Add the eight counts: 5 + 3 + 6 + 4 + 5 + 7 + 4 + 6 =", "answer": 40, "hint": "Add all eight."},
    {"pre": "Mean per quadrat = 40 ÷ 8 =", "answer": 5, "hint": "Divide by the 8 quadrats."},
    {"pre": "Quadrats that fit the field = 400 ÷ 0.5 =", "answer": 800, "hint": "Total area over quadrat area, not 400 ÷ 8.", "phase": "substitute"},
    {"pre": "Population = mean × quadrats = 5 × 800 =", "answer": 4000, "hint": "Multiply the mean by 800."},
    {"say": "So the estimated population is <strong>4000 dandelions</strong>."},
    {"pre": "Check via density: plants per m² = 5 ÷ 0.5 =", "answer": 10, "hint": "How many in a full square metre."},
    {"pre": "10 × 400 =", "answer": 4000, "hint": "Density times total area.", "done": "Same 4000 by a second route, so it is right."}
   ],
   "Mean per quadrat first, then multiply by (400 ÷ 0.5).",
   eqh="population = mean × (total area ÷ quadrat area)"),

 prob("%", "Mean seedling height was 3 cm at Week 1 and 7.8 cm at Week 4. Calculate the percentage change in height.",
   160,
   [m("wrong_denominator", "Divide by the ORIGINAL (3): (7.8 − 3) ÷ 3 × 100 = 4.8 ÷ 3 × 100 = 160%. Dividing by the new value (7.8) gives about 62%.", 61.54)],
   [
    {"say": "Percentage change = (new − original) ÷ original × 100."},
    {"pre": "Change = new − original = 7.8 − 3 =", "answer": 4.8, "hint": "New minus original.", "phase": "substitute"},
    {"pre": "Divide by the original (3): 4.8 ÷ 3 =", "answer": 1.6, "hint": "Divide by the starting height."},
    {"pre": "Multiply by 100: 1.6 × 100 =", "answer": 160, "hint": "Shift two places for a percentage."},
    {"say": "So the percentage change is <strong>160%</strong>, an increase."},
    {"pre": "Check: 160% of 3 is 1.6 × 3 =", "answer": 4.8, "hint": "Should match the rise you found.", "done": "It matches the rise of 4.8, so 160% is right."}
   ],
   "Divide the rise by the starting height (3), times 100.",
   eqh="% change = (new − original) ÷ original × 100"),

 prob("%", "In a habitat survey, the mean number of wood lice per 1 m² quadrat was 12. The total habitat area is 800 m². Estimate the population. If next year the count gives a mean of 9 per quadrat, calculate the percentage change in estimated population.",
   -25,
   [m("wrong_denominator", "Year 1: 12 × 800 = 9600. Year 2: 9 × 800 = 7200. Divide by the ORIGINAL (9600): (7200 − 9600) ÷ 9600 × 100 = −25%. Dividing by the new value (7200) gives about −33%.", -33.33)],
   [
    {"say": "Three moves: estimate each year's population, then the percentage change between them. The quadrat is 1 m², so quadrats = 800 ÷ 1 = 800."},
    {"pre": "Year 1 population = 12 × 800 =", "answer": 9600, "hint": "Mean times the 800 quadrat-sized units."},
    {"pre": "Year 2 population = 9 × 800 =", "answer": 7200, "hint": "New mean times 800."},
    {"pre": "Change = new − original = 7200 − 9600 =", "answer": -2400, "hint": "Year 2 minus Year 1.", "phase": "substitute"},
    {"pre": "Divide by the original (9600): -2400 ÷ 9600 =", "answer": -0.25, "hint": "Divide by Year 1's population."},
    {"pre": "Multiply by 100: -0.25 × 100 =", "answer": -25, "hint": "Shift two places for a percentage."},
    {"say": "So the estimated population fell by <strong>25%</strong>."},
    {"pre": "Check via the means: (9 − 12) ÷ 12 × 100 =", "answer": -25, "hint": "The 800 cancels, so the means give the same percentage.", "done": "Same -25% from the means alone, so it is right."}
   ],
   "Estimate both populations, then work the percentage change on them.",
   eqh="% change = (new − original) ÷ original × 100"),
]

pd = {
 "method_card": {
  "title": "Sampling, Mean and Percentage Change",
  "steps": [
   "Mean: add the values, then divide by how many there are.",
   "Percentage change: (new − original) ÷ original × 100. The original goes on the bottom.",
   "Population: mean per quadrat × (total area ÷ quadrat area).",
   "State the unit or % with your final answer."
  ],
  "content": "<p>Three data skills recur in biology questions.</p><p><strong>Mean:</strong> add every value, then divide by the count.</p><p><strong>Percentage change:</strong> (new − original) ÷ original × 100. Always divide by the <em>original</em>. A negative answer is a decrease; above 100% just means the value more than doubled.</p><p><strong>Population estimate:</strong> find the mean count per quadrat, then scale up by (total area ÷ quadrat area). Keep the two divisions apart: count over quadrats for the mean, area over area for the scale.</p>"
 },
 "topic_links": {"prerequisites": []},
 "exam_context": {
  "marks": "2–4 per question",
  "paper": "Biology paper (combined science)",
  "frequency": "Medium: data skills questions appear in most biology papers"
 },
 "problem_bank": {
  "bronze": bronze,
  "silver": silver,
  "gold": gold,
  "bronze_description": "One calculation with the values given: find a mean, or a straight percentage change.",
  "silver_description": "Scale or round: estimate a population from quadrats, or work a percentage change to a stated decimal place.",
  "gold_description": "Multi-step: chain a mean or population into a percentage change, using the exact data given."
 },
 "related_videos": [],
 "worked_examples": [
  {
   "steps": [
    {"label": "Step 1: Calculate mean", "content": "<p>Sum = 45. Mean = 45 ÷ 10 = 4.5 per m²</p>"},
    {"label": "Step 2: Estimate population", "content": "<p>Population = 4.5 × (200 ÷ 1) = 4.5 × 200</p>"},
    {"label": "Answer", "content": "<p>Estimated population = <strong>900 dandelions</strong></p>", "isAnswer": True, "is_answer": True}
   ],
   "question": "A student places ten 1 m² quadrats in a 200 m² meadow and counts dandelions: 3,5,4,6,3,5,4,4,6,5. Calculate the mean and estimate the total population.",
   "difficulty": "Bronze"
  },
  {
   "steps": [
    {"label": "Step 1: Identify values", "content": "<p>Original = 240; new = 180</p>"},
    {"label": "Step 2: Apply formula", "content": "<p>% change = (180 − 240) ÷ 240 × 100 = −60/240 × 100</p>"},
    {"label": "Answer", "content": "<p>% change = <strong>−25% (a decrease of 25%)</strong></p>", "isAnswer": True, "is_answer": True}
   ],
   "question": "A field study recorded 240 blue tit territories in Year 1. By Year 5 the number had fallen to 180. Calculate the percentage change.",
   "difficulty": "Silver"
  },
  {
   "steps": [
    {"label": "Step 1: Apply formula", "content": "<p>% change = (427 − 350) ÷ 350 × 100 = 77 ÷ 350 × 100</p>"},
    {"label": "Step 2: Round to 1 d.p.", "content": "<p>= 22.0%</p>"},
    {"label": "Answer", "content": "<p>% change = <strong>+22.0% (an increase)</strong></p>", "isAnswer": True, "is_answer": True}
   ],
   "question": "In Year 1, a woodland had 350 oak trees. By Year 4, the population had risen to 427. Calculate the percentage change to one decimal place.",
   "difficulty": "Gold"
  }
 ],
 "tier_guides": {
  "bronze": {
   "title": "Bronze: one calculation, values given",
   "steps": [
    "<strong>Mean:</strong> add the values, then divide by how many there are.",
    "<strong>Percentage change:</strong> (new − original) ÷ original × 100. The starting value goes on the bottom.",
    "Everything you need is in the question. No converting, no scaling."
   ],
   "example": {
    "question": "Calculate the mean of 4, 6, 5, 5.",
    "steps": [
     {"label": "Add the values", "content": "4 + 6 + 5 + 5 = 20"},
     {"label": "Divide by the count", "content": "20 ÷ 4 = 5"},
     {"label": "Check", "content": "5 × 4 = 20, back to the sum"},
     {"label": "Answer", "content": "Mean = 5", "isAnswer": True, "is_answer": True}
    ]
   }
  },
  "silver": {
   "title": "Silver: scale up or round",
   "steps": [
    "<strong>Population:</strong> find the mean per quadrat, then multiply by (total area ÷ quadrat area). Watch the quadrat size.",
    "<strong>Percentage change:</strong> (new − original) ÷ original × 100, rounding to the decimal place asked for.",
    "Two moves, done in order: mean or change first, then scale or round."
   ],
   "example": {
    "question": "0.5 m² quadrats in a 100 m² field, mean 5 per quadrat. Estimate the population.",
    "steps": [
     {"label": "Quadrats in the field", "content": "100 ÷ 0.5 = 200"},
     {"label": "Scale up", "content": "5 × 200 = 1000"},
     {"label": "Check", "content": "1000 ÷ 200 = 5, back to the mean"},
     {"label": "Answer", "content": "Population = 1000", "isAnswer": True, "is_answer": True}
    ]
   }
  },
  "gold": {
   "title": "Gold: chain two steps",
   "steps": [
    "Two ideas in one question: often a mean or population followed by a percentage change.",
    "Do each part in order and label your intermediate values so you feed the right number into the next step.",
    "Read the data carefully: use the exact values named, and watch the quadrat size."
   ],
   "example": {
    "question": "A mean count rises from 5 to 8. Find the percentage change.",
    "steps": [
     {"label": "Change", "content": "8 − 5 = 3"},
     {"label": "Divide by the original", "content": "3 ÷ 5 = 0.6"},
     {"label": "Times 100", "content": "0.6 × 100 = 60"},
     {"label": "Answer", "content": "60% increase", "isAnswer": True, "is_answer": True}
    ]
   }
  }
 },
 "guided": {
  "opener": {
   "steps": [
    {"say": "Two quick puzzles, no formulas, just common sense."},
    {"pre": "Five friends pool their pocket money: £4, £8, £6, £7, £5. Shared out equally, how much each? £", "answer": 6, "hint": "Add it up (£30), then split between 5."},
    {"say": "That equal share is the <strong>mean</strong>: add everything, divide by how many."},
    {"pre": "You earned £8 an hour. Your boss adds £2, so now £10. Out of your original £8, the £2 rise is what percentage? ", "answer": 25, "hint": "£2 is a quarter of £8, and a quarter is 25%.", "post": "%"},
    {"say": "That is <strong>percentage change</strong>: the rise divided by what you STARTED with, times 100. The original (£8) always goes on the bottom. Mean and percentage change are two of the three skills here; the third, estimating a population from quadrats, is just a mean scaled up."}
   ]
  },
  "teach": {
   "bronze": {
    "display": "A student measures 5 leaf lengths: 6 cm, 9 cm, 7 cm, 8 cm, 10 cm. Calculate the mean length.",
    "steps": [
     {"say": "Mean = sum of values ÷ number of values."},
     {"pre": "Add them: 6 + 9 + 7 + 8 + 10 =", "answer": 40, "hint": "Add all five lengths."},
     {"pre": "How many values are there?", "answer": 5, "hint": "Count them."},
     {"pre": "Mean = 40 ÷ 5 =", "answer": 8, "hint": "Divide the sum by 5."},
     {"say": "So the mean length is <strong>8 cm</strong>."},
     {"pre": "Check: mean × count returns the sum. 8 × 5 =", "answer": 40, "hint": "Multiply back.", "done": "It gives 40, the sum, so 8 cm is right."}
    ]
   },
   "silver": {
    "display": "A student uses 0.5 m² quadrats in a 400 m² field. The mean number of buttercups per quadrat is 8. Estimate the population.",
    "steps": [
     {"say": "Population = mean per quadrat × (total area ÷ quadrat area). The new move is scaling the mean up to the whole field."},
     {"pre": "How many quadrats fit the field: 400 ÷ 0.5 =", "answer": 800, "hint": "Field area over one quadrat's area."},
     {"pre": "Population = mean × quadrats = 8 × 800 =", "answer": 6400, "hint": "Multiply the mean by 800."},
     {"say": "So the estimate is <strong>6400 buttercups</strong>."},
     {"pre": "Check by density: buttercups per m² = 8 ÷ 0.5 =", "answer": 16, "hint": "8 in half a square metre."},
     {"pre": "16 × 400 =", "answer": 6400, "hint": "Density times total area.", "done": "Same 6400 both ways. Gone."}
    ]
   },
   "gold": {
    "display": "A pond is sampled in 5 quadrats. In spring the frog counts are 2, 4, 3, 5, 6. In summer the same quadrats give 6, 8, 7, 9, 10. Calculate the percentage change in the mean count.",
    "steps": [
     {"say": "The new move is chaining: find each mean first, then the percentage change between them."},
     {"pre": "Spring sum: 2 + 4 + 3 + 5 + 6 =", "answer": 20, "hint": "Add the five spring counts."},
     {"pre": "Spring mean = 20 ÷ 5 =", "answer": 4, "hint": "Divide by 5."},
     {"pre": "Summer sum: 6 + 8 + 7 + 9 + 10 =", "answer": 40, "hint": "Add the five summer counts."},
     {"pre": "Summer mean = 40 ÷ 5 =", "answer": 8, "hint": "Divide by 5."},
     {"pre": "Change in the mean = 8 − 4 =", "answer": 4, "hint": "New mean minus old mean."},
     {"pre": "(4 ÷ 4) × 100 =", "answer": 100, "hint": "Divide by the original mean of 4, then ×100."},
     {"say": "So the mean count rose by <strong>100%</strong>: it doubled. Gone, that was the whole point."}
    ]
   }
  }
 }
}

fn = "lesson_" + KEY + ".json"
with io.open(fn, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", fn)
