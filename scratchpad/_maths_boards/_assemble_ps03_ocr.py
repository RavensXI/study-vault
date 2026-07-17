# -*- coding: utf-8 -*-
import json, io, copy

live = json.load(io.open("_live_psL03ocr.json", encoding="utf-8"))
svg = json.load(io.open("_ps03_svgs.json", encoding="utf-8"))
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

pb = copy.deepcopy(live["problem_bank"])
B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

def box(pre, answer, hint, post="", done=None, phase=None, say=None, display=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    if say: d["say"] = say
    if display: d["display"] = display
    return d
def sayb(s): return {"say": s}

# ================= BRONZE =================
# B0: swimming = 20  (bars Football30 Tennis15 Swimming20 Rugby10, step 5)
B[0]["hint"] = "Follow the top of the Swimming bar across to the number axis."
B[0]["guided_steps"] = [
    sayb("Read the Swimming bar against the number axis. Each gridline is worth 5 students."),
    box("The Swimming bar reaches how many gridlines above zero? ", 4, "It lines up 4 gridlines up."),
    box("Each gridline is 5 students, so 4 × 5 = ", 20, "Multiply the gridlines by 5.", phase="substitute"),
    box("Check against the chart: the Swimming bar sits level with which number? ", 20, "It lines up with 20.", done="Swimming = 20 students."),
]
B[0]["misconceptions"] = [
    {"note": "counts gridlines as 1 each", "expect": 4, "pattern": "gridline_not_scaled",
     "message": "Each gridline is worth 5, not 1. The Swimming bar is 4 gridlines up, so 4 × 5 = 20."},
]
# B1: total = 75
B[1]["hint"] = "Add the height of every bar together."
B[1]["guided_steps"] = [
    sayb("The total is the sum of every bar. The bars read 30, 15, 20 and 10."),
    box("Add the first two bars: 30 + 15 = ", 45, "Thirty plus fifteen."),
    box("Add the next bar: 45 + 20 = ", 65, "Add twenty.", phase="substitute"),
    box("Add the last bar: 65 + 10 = ", 75, "Add ten."),
    box("Check another way: (30 + 20) + (15 + 10) = 50 + 25 = ", 75, "Same total.", done="75 students were surveyed."),
]
B[1]["misconceptions"] = [
    {"note": "forgets the rugby bar", "expect": 65, "pattern": "missed_a_bar",
     "message": "Add every bar, including Rugby. 30 + 15 + 20 + 10 = 75."},
]
# B2: pie total 200, Maths 90 -> 50  (add svg)
B[2]["display"] = svg["b3"] + "A pie chart represents 200 students. The Maths sector has an angle of 90°. How many students chose Maths?"
B[2]["hint"] = "Angle over 360 gives the fraction; multiply that by 200."
B[2]["guided_steps"] = [
    sayb("Angle over 360 gives the fraction of students. Then scale up to the total."),
    box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
    box("Fraction that is Maths: 90 ÷ 360 = ", 0.25, "90 divided by 360.", phase="substitute"),
    box("Multiply by the total students: 0.25 × 200 = ", 50, "0.25 of 200."),
    box("Check: 50 out of 200 as an angle = (50 ÷ 200) × 360 = ", 90, "Returns to 90°.", done="Maths = 50 students."),
]
B[2]["misconceptions"] = [
    {"note": "reports the angle", "expect": 90, "pattern": "angle_as_count",
     "message": "90 is the angle, not the number of students. Work out (90/360) × 200 = 50."},
]
# B3: freq table 8,12,5,15 -> 40
B[3]["hint"] = "Add all four frequencies together."
B[3]["guided_steps"] = [
    sayb("The total frequency is the sum of every frequency: 8, 12, 5 and 15."),
    box("Add the first two: 8 + 12 = ", 20, "Eight plus twelve."),
    box("Add the next: 20 + 5 = ", 25, "Add five.", phase="substitute"),
    box("Add the last: 25 + 15 = ", 40, "Add fifteen."),
    box("Check another way: (8 + 12) + (5 + 15) = 20 + 20 = ", 40, "Same total.", done="Total frequency = 40."),
]
B[3]["misconceptions"] = [
    {"note": "drops the last frequency", "expect": 25, "pattern": "missed_a_value",
     "message": "Add all four frequencies. 8 + 12 + 5 + 15 = 40."},
]
# B4: pie total 72, sector 60 -> 12  (add svg)
B[4]["display"] = svg["b5"] + "A pie chart represents 72 people. One sector has an angle of 60°. How many people does it represent?"
B[4]["hint"] = "Work out how many 60° sectors fit in 360°, then share 72 between them."
B[4]["guided_steps"] = [
    sayb("The sector is 60° out of 360°. Work out how many equal sectors that makes, then share the total."),
    box("Simplify 60/360 by dividing both by 60. Bottom: 360 ÷ 60 = ", 6, "360 divided by 60, so the fraction is 1/6."),
    box("Number who chose it = 72 ÷ 6 = ", 12, "72 divided by 6.", phase="substitute"),
    box("Check: 12 out of 72 as an angle = (12 ÷ 72) × 360 = ", 60, "Returns to 60°.", done="12 people chose that sector."),
]
B[4]["misconceptions"] = [
    {"note": "multiplies instead of dividing", "expect": 432, "pattern": "multiplied_not_divided",
     "message": "6 is how many 60° sectors fit in the circle. Divide the total by 6, do not multiply: 72 ÷ 6 = 12."},
]
# B5: 40 people, 15 chose A, angle -> 135 (calc true)
B[5]["hint"] = "Fraction of people times 360 gives the angle."
B[5]["guided_steps"] = [
    sayb("Frequency over total gives the fraction of the circle. Multiply by 360 for the angle."),
    box("Fraction that chose A: 15 ÷ 40 = ", 0.375, "15 divided by 40."),
    box("Angle = 0.375 × 360 = ", 135, "Multiply the fraction by 360.", phase="substitute"),
    box("Check: a 135° sector out of 40 people = (135 ÷ 360) × 40 = ", 15, "Returns to 15.", done="Sector A is 135°."),
]
B[5]["misconceptions"] = [
    {"note": "times number of people not 360", "expect": 15, "pattern": "times_total_not_360",
     "message": "Multiply the fraction by 360°, not by the number of people. (15/40) × 360 = 135."},
]
# B6: MC positive correlation
B[6]["hint"] = "As one quantity rises, does the other rise, fall, or show no pattern?"
B[6]["misconceptions"] = [
    {"expect": None, "pattern": "mislabels_trend",
     "message": "Both quantities increase together, so this is positive correlation."},
]
# B7: MC no correlation
B[7]["hint"] = "Is there any clear pattern linking the two quantities?"
B[7]["misconceptions"] = [
    {"expect": None, "pattern": "mislabels_trend",
     "message": "There is no pattern linking the two, so this is no correlation."},
]

# ================= SILVER =================
# S0: dual bar Drama diff = 15
S[0]["hint"] = "Read both Drama bars, then subtract boys from girls."
S[0]["guided_steps"] = [
    sayb("Read both Drama bars, then find the difference."),
    box("Read the Girls Drama bar: ", 25, "Girls reach 25."),
    box("Read the Boys Drama bar: ", 10, "Boys reach 10."),
    box("How many more girls? 25 − 10 = ", 15, "Subtract boys from girls.", phase="substitute"),
    box("Check: Boys plus your answer should give Girls. 10 + 15 = ", 25, "Returns to 25.", done="15 more girls chose Drama."),
]
S[0]["misconceptions"] = [
    {"note": "adds the bars", "expect": 35, "pattern": "added_not_subtracted",
     "message": "How many MORE girls means subtract boys from girls: 25 − 10 = 15, not add."},
]
# S1: pie 144 = 36 students, total -> 90 (add svg)
S[1]["display"] = svg["s2"] + "A pie chart has a sector of 144° representing 36 students. Find the total number of students."
S[1]["hint"] = "The sector is 2/5 of the circle, so 36 is 2/5 of the total."
S[1]["guided_steps"] = [
    sayb("The sector's share of 360° equals its share of the total. Simplify the fraction, then scale back up."),
    box("Simplify 144/360 by dividing both by 72. Top: 144 ÷ 72 = ", 2, "144 divided by 72."),
    box("Bottom: 360 ÷ 72 = ", 5, "360 divided by 72, so the fraction is 2/5."),
    box("So 36 is 2/5 of the total. One fifth = 36 ÷ 2 = ", 18, "Half of 36.", phase="substitute"),
    box("Total = five fifths = 18 × 5 = ", 90, "Five lots of one fifth."),
    box("Check: (144 ÷ 360) × 90 = ", 36, "Returns to 36.", done="The total is 90 students."),
]
S[1]["misconceptions"] = [
    {"note": "method reminder, no single determinate slip", "expect": None, "pattern": "scaled_wrong",
     "message": "The sector is 2/5 of the circle, so 36 is 2/5 of the total. Total = 36 ÷ 2 × 5 = 90."},
]
# S2: two-way table females pass -> 12
S[2]["hint"] = "Female passes = total passes minus male passes."
S[2]["guided_steps"] = [
    sayb("A two-way table splits by two things at once. Total passes minus male passes leaves female passes."),
    box("Total who passed: ", 30, "30 passed in all."),
    box("Males who passed: ", 18, "18 males passed."),
    box("Females who passed = 30 − 18 = ", 12, "Subtract male passes from total passes.", phase="substitute"),
    box("Check: females who failed = 22 − 12 = 10, males who failed = 28 − 18 = 10, total fails = ", 20, "10 + 10 should give the 20 fails.", done="12 females passed."),
]
S[2]["misconceptions"] = [
    {"note": "gives male fails cell", "expect": 10, "pattern": "wrong_cell",
     "message": "10 is the number of males who failed. Female passes = total passes (30) − male passes (18) = 12."},
]
# S3: MC negative correlation
S[3]["hint"] = "As TV hours go up, do scores go up or down?"
S[3]["misconceptions"] = [
    {"expect": None, "pattern": "mislabels_trend",
     "message": "Negative correlation means as one rises the other falls: more TV, lower scores."},
]
# S4: pie Pizza150 Chips90 Salad -> 24 (add svg)
S[4]["display"] = svg["s5"] + "A pie chart shows lunch choices. The Pizza sector is 150° and the Chips sector is 90°. The rest is Salad. There are 72 people in total. How many chose Salad?"
S[4]["hint"] = "Find the Salad angle first (angles fill 360°), then turn it into people."
S[4]["guided_steps"] = [
    sayb("Find the Salad angle first (all sectors fill 360°), then convert that angle to people."),
    box("Add the two known angles: 150 + 90 = ", 240, "Pizza plus Chips."),
    box("Salad angle = 360 − 240 = ", 120, "Subtract from 360."),
    box("Salad is 120/360 = 1/3 of the circle. Number = 72 ÷ 3 = ", 24, "A third of 72.", phase="substitute"),
    box("Check: Pizza (150°) + Chips (90°) + Salad (120°) = ", 360, "They fill the circle.", done="24 chose Salad."),
]
S[4]["misconceptions"] = [
    {"note": "reports the salad angle", "expect": 120, "pattern": "angle_as_count",
     "message": "120 is the Salad angle, not the number of people. (120/360) × 72 = 24."},
]
# S5: grouped freq 5,12,8 -> 25
S[5]["hint"] = "Add the three group frequencies together."
S[5]["guided_steps"] = [
    sayb("Total frequency is the sum of the group frequencies: 5, 12 and 8."),
    box("Add the first two: 5 + 12 = ", 17, "Five plus twelve."),
    box("Add the last: 17 + 8 = ", 25, "Add eight.", phase="substitute"),
    box("Check another way: 5 + 8 = 13, then 13 + 12 = ", 25, "Same total.", done="Total frequency = 25."),
]
S[5]["misconceptions"] = [
    {"note": "drops a group", "expect": 17, "pattern": "missed_a_value",
     "message": "Add all three group frequencies. 5 + 12 + 8 = 25."},
]
# S6: travel -> 5 (was degenerate 45->0; fix total to 50)
S[6]["display"] = "In a survey of 50 students, 20 walk to school, 15 take the bus and 10 come by car. The rest cycle. How many cycle?"
S[6]["solutions"] = [5]
S[6]["hint"] = "Subtract the three known groups from the total of 50."
S[6]["guided_steps"] = [
    sayb("The four travel methods add up to everyone. Subtract the known three from the total."),
    box("Add the three known groups: 20 + 15 + 10 = ", 45, "Walk plus bus plus car."),
    box("Number who cycle = 50 − 45 = ", 5, "Subtract from the total of 50.", phase="substitute"),
    box("Check: 20 + 15 + 10 + 5 = ", 50, "They add to 50.", done="5 students cycle."),
]
S[6]["misconceptions"] = [
    {"note": "forgets to subtract from total", "expect": 45, "pattern": "forgot_subtract",
     "message": "45 is how many walk, bus or drive. Cyclists = 50 − 45 = 5."},
]

# ================= GOLD =================
# G0: scatter TV vs test, estimate at 28 -> 36 (add LOBF line)
G[0]["hint"] = "Read the trend at 28 hours, using the points at 25 and 30 hours."
# add line of best fit dataset to existing scatter chart
G[0]["chart"]["data"]["datasets"].append({
    "type": "line", "label": "Line of best fit",
    "data": [{"x": 10, "y": 49}, {"x": 45, "y": 23}],
    "borderColor": "#1e40af", "borderWidth": 2, "fill": False, "pointRadius": 0, "tension": 0
})
G[0]["guided_steps"] = [
    sayb("Estimate by reading the trend at 28 hours. Use the plotted points either side."),
    box("The point at 25 hours reads what test score? ", 38, "At 25 hours, 38%."),
    box("The point at 30 hours reads what test score? ", 35, "At 30 hours, 35%."),
    box("28 hours is most of the way from 25 to 30, so the trend reads just above 35. Read it as ", 36, "About 36%.", phase="substitute"),
    box("Check: the line of best fit at 28 hours passes through about ", 36, "It sits between 35 and 38.", done="About 36% at 28 hours of TV."),
]
G[0]["misconceptions"] = [
    {"note": "reads the 25-hour point", "expect": 38, "pattern": "read_wrong_x",
     "message": "38% is the score at 25 hours. At 28 hours the trend gives about 36%."},
]
# G1: pie Other 72, total 500 -> 100 (add svg)
G[1]["display"] = svg["g2"] + "A pie chart represents 500 people. The 'Other' sector has an angle of 72°. How many chose Other?"
G[1]["hint"] = "Angle over 360 gives the fraction; multiply by 500."
G[1]["guided_steps"] = [
    sayb("Angle over 360 gives the fraction of people. Simplify, then apply it to the total."),
    box("Simplify 72/360 by dividing both by 72. Bottom: 360 ÷ 72 = ", 5, "360 divided by 72, so the fraction is 1/5."),
    box("Number = 500 ÷ 5 = ", 100, "A fifth of 500.", phase="substitute"),
    box("Check: 100 out of 500 as an angle = (100 ÷ 500) × 360 = ", 72, "Returns to 72°.", done="100 people chose Other."),
]
G[1]["misconceptions"] = [
    {"note": "reports the angle", "expect": 72, "pattern": "angle_as_count",
     "message": "72 is the angle, not the number of people. (72/360) × 500 = 100."},
]
# G2: histogram frequency density -> 2.5 (fix wording from frequency polygon)
G[2]["display"] = "A histogram has a bar for the class 30 to 40 with frequency 25 and class width 10. What is the frequency density?"
G[2]["hint"] = "Frequency density = frequency divided by class width."
G[2]["guided_steps"] = [
    sayb("Frequency density spreads the frequency evenly across the class width: frequency ÷ class width."),
    box("Write the frequency: ", 25, "The bar's frequency is 25."),
    box("Write the class width: ", 10, "From 30 to 40 is a width of 10."),
    box("Frequency density = 25 ÷ 10 = ", 2.5, "Divide frequency by class width.", phase="substitute"),
    box("Check: frequency density × class width = 2.5 × 10 = ", 25, "Returns to the frequency 25.", done="Frequency density = 2.5."),
]
G[2]["misconceptions"] = [
    {"note": "multiplies instead of dividing", "expect": 250, "pattern": "multiplied_not_divided",
     "message": "Frequency density divides by the width: 25 ÷ 10 = 2.5, not 25 × 10."},
]
# G3: comparative bar diff -> 7
G[3]["hint"] = "Percentage point difference is one percentage minus the other."
G[3]["guided_steps"] = [
    sayb("Percentage point difference is simply one percentage minus the other."),
    box("Write the Year 11 percentage: ", 72, "Year 11 scored 72."),
    box("Write the Year 10 percentage: ", 65, "Year 10 scored 65."),
    box("Difference = 72 − 65 = ", 7, "Subtract the smaller from the larger.", phase="substitute"),
    box("Check: 65 + 7 = ", 72, "Returns to 72.", done="A 7 percentage point difference."),
]
G[3]["misconceptions"] = [
    {"note": "adds the two percentages", "expect": 137, "pattern": "added_not_subtracted",
     "message": "'Difference' means subtract, not add: 72 − 65 = 7."},
]
# G4: composite bar Q4 clothing % -> 25 (calc true)
G[4]["hint"] = "Add the three Q4 parts for the total, then Clothing as a percentage of it."
G[4]["guided_steps"] = [
    sayb("For a percentage of the stack, find the Q4 total, then Clothing as a share of it."),
    box("Q4 total: 55 + 25 + 20 = ", 100, "Add the three Q4 parts."),
    box("Clothing as a fraction: 25 ÷ 100 = ", 0.25, "25 out of 100.", phase="substitute"),
    box("As a percentage: 0.25 × 100 = ", 25, "Multiply by 100."),
    box("Check: 25% of 100 = 0.25 × 100 = ", 25, "Returns to the Clothing value.", done="Clothing = 25% of Q4."),
]
G[4]["misconceptions"] = [
    {"note": "no single determinate slip that is not the answer", "expect": None, "pattern": "wrong_total",
     "message": "Q4 total = 55 + 25 + 20 = 100. Clothing = 25, so 25/100 × 100 = 25%."},
]

# descriptions
pb["bronze_description"] = "Read a single value straight off a bar chart, or turn a pie chart sector into a frequency."
pb["silver_description"] = "Compare two data sets, convert between pie chart angles and frequencies, and read two-way tables."
pb["gold_description"] = "Combine steps: composite bar charts, frequency density, and estimating from a line of best fit."

# ================= guided (opener + teach) =================
guided = {
    "opener": {
        "steps": [
            sayb("Picture a class of 24 students choosing a lunch. Exactly a quarter of them chose pizza. Here is that choice drawn as a circle."),
            box("A quarter of the class chose pizza. How many students is a quarter of 24? ", 6, "24 divided by 4.",
                display=svg["open"]),
            box("A full circle is 360°. The pizza slice is a quarter of the circle. How many degrees is a quarter of 360? ", 90, "360 divided by 4."),
            sayb("You just built a pie chart slice. The fraction of people (a quarter) is the same as the fraction of the circle. So <strong>angle = fraction × 360°</strong>, and turned around, <strong>frequency = (angle ÷ 360) × total</strong>. That one idea powers every pie chart question."),
        ]
    },
    "teach": {
        "bronze": {
            "display": svg["tb"] + "The bar chart shows how a class travels to school. How many more walk than cycle?",
            "steps": [
                sayb("Read the two bars the question names, then compare them."),
                box("Read the Walk bar: ", 12, "Walk reaches 12."),
                box("Read the Cycle bar: ", 3, "Cycle reaches 3."),
                box("How many more walk? 12 − 3 = ", 9, "Subtract cycle from walk."),
                box("Check: Cycle plus your answer should give Walk. 3 + 9 = ", 12, "Returns to 12.", done="9 more walk than cycle. Read, then compare."),
            ],
        },
        "silver": {
            "display": svg["ts"] + "The pie chart shows 180 people's favourite fruit. The Apple sector is 40°. How many chose apple?",
            "steps": [
                sayb("Angle over 360 gives the fraction of people. Then scale to the total."),
                box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
                box("Simplify 40/360: bottom is 360 ÷ 40 = ", 9, "360 divided by 40, so the fraction is 1/9."),
                box("Number = 180 ÷ 9 = ", 20, "180 divided by 9."),
                box("Check: 20 out of 180 as an angle = (20 ÷ 180) × 360 = ", 40, "Returns to 40°.", done="20 chose apple. Angle to fraction to people."),
            ],
        },
        "gold": {
            "display": svg["tg"] + "The stacked bar shows a shop's Monday sales (£): Drinks 40, Snacks 30, Papers 10. What percentage were Drinks?",
            "steps": [
                sayb("Find the total of the stack, then Drinks as a share of it."),
                box("Add the parts: 40 + 30 + 10 = ", 80, "Add all three."),
                box("Drinks as a fraction: 40 ÷ 80 = ", 0.5, "40 out of 80."),
                box("As a percentage: 0.5 × 100 = ", 50, "Multiply by 100."),
                box("Check: 50% of 80 = 0.5 × 80 = ", 40, "Returns to the Drinks value.", done="Drinks = 50%. Total, share, percentage."),
            ],
        },
    },
}

# ================= tier_guides =================
tier_guides = {
    "bronze": {
        "title": "Bronze: reading charts and simple pie sectors",
        "steps": [
            "<strong>Bar charts:</strong> follow the top of a bar across to the number axis. Each gridline is worth the scale shown, so a bar 4 gridlines up on a scale of 5 means 20.",
            "<strong>Pie sectors:</strong> a sector's share is its frequency over the total. Turn a sector into people with (angle ÷ 360) × total.",
            "For 'how many more', read both values, then subtract the smaller from the larger.",
        ],
        "example": {
            "question": "A bar chart shows Green = 15, Blue = 25. How many more chose blue?",
            "steps": [
                {"label": "Read", "content": "Green = 15, Blue = 25"},
                {"label": "Subtract", "content": "25 − 15 = 10"},
                {"label": "Check", "content": "15 + 10 = 25"},
                {"label": "Answer", "content": "10 more chose blue", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: comparing data, pie angles and two-way tables",
        "steps": [
            "<strong>Angle to frequency:</strong> divide the angle by 360 to get the fraction, then multiply by the total.",
            "<strong>Frequency to angle:</strong> divide the frequency by the total, then multiply by 360.",
            "<strong>Missing angle:</strong> all sectors add to 360°, so subtract the known angles from 360.",
            "<strong>Two-way tables:</strong> each row and column adds to its total, so fill a gap by subtracting.",
        ],
        "example": {
            "question": "A pie chart shows 90 people. Sector B is 40°. How many people is that?",
            "steps": [
                {"label": "Fraction", "content": "40 ÷ 360 = 1/9"},
                {"label": "Multiply", "content": "1/9 × 90 = 10"},
                {"label": "Check", "content": "(10 ÷ 90) × 360 = 40°"},
                {"label": "Answer", "content": "10 people", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: composite charts, density and lines of best fit",
        "steps": [
            "<strong>Composite (stacked) bars:</strong> read each part, add them for the total, then one part as a percentage: part ÷ total × 100.",
            "<strong>Frequency density:</strong> for a histogram bar, frequency density = frequency ÷ class width.",
            "<strong>Line of best fit:</strong> read straight up from the x-value to estimate y; inside the data range (interpolation) is reliable, outside (extrapolation) is not.",
        ],
        "example": {
            "question": "A stacked bar shows A = 30, B = 20 in one month. What percentage is A?",
            "steps": [
                {"label": "Total", "content": "30 + 20 = 50"},
                {"label": "Percentage", "content": "(30 ÷ 50) × 100 = 60%"},
                {"label": "Check", "content": "60% of 50 = 30"},
                {"label": "Answer", "content": "60%", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================= method_card (slim) =================
method_card = {
    "title": "Representing Data",
    "steps": [
        "Bar charts: read a bar's height against the number axis, minding the scale.",
        "Pie charts: frequency = (angle ÷ 360) × total; angle = (frequency ÷ total) × 360.",
        "Scatter graphs: describe correlation and estimate with the line of best fit.",
        "Two-way tables: every row and column adds to its total.",
    ],
    "content": "<p><strong>Pie charts:</strong> a sector's angle over 360 is its fraction of the total. Frequency = (angle ÷ 360) × total; angle = (frequency ÷ total) × 360. All sectors add to 360°.</p><p><strong>Scatter graphs:</strong> positive correlation means both rise together; negative means one rises as the other falls. Read the line of best fit to estimate, but only trust estimates inside the data range.</p>",
    "example": "<p><strong>A pie chart represents 120 people. The Bus sector is 90°. How many travel by bus?</strong></p><p>(90 ÷ 360) × 120 = 30 people</p>",
}

# ================= assemble (preserve untouched fields) =================
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],          # preserved
    "problem_bank": pb,
    "related_videos": live["related_videos"],     # preserved (empty)
    "worked_examples": live["worked_examples"],   # preserved
    "tier_guides": tier_guides,
    "guided": guided,
}

with open("lesson_maths-ocr_probability-statistics-L03.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote lesson shard. em dash present:", "—" in json.dumps(out, ensure_ascii=False))
