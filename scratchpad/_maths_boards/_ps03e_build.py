# -*- coding: utf-8 -*-
import json, sys, copy
sys.stdout.reconfigure(encoding="utf-8")
from _ps03e_svglib import pie_svg, bar_svg, two_pies_svg

live = json.load(open("_ps03e_live.json", encoding="utf-8"))["practice_data"]
pd = copy.deepcopy(live)
pb = pd["problem_bank"]

# --- fix pre-existing em dashes in preserved fields (style law) ---
pd["method_card"]["content"] = pd["method_card"]["content"].replace(
    "<strong>Positive correlation</strong> — both increase.",
    "<strong>Positive correlation</strong>: both increase.").replace(
    "<strong>Negative correlation</strong> — one increases, other decreases.",
    "<strong>Negative correlation</strong>: one increases, the other decreases.").replace(
    "<strong>No correlation</strong> — no pattern.",
    "<strong>No correlation</strong>: no pattern.")
we2 = pd["worked_examples"][2]["steps"][1]
we2["content"] = we2["content"].replace(
    "x = 8 is within the data range (2–12) — interpolation, so reliable.",
    "x = 8 is within the data range (2 to 12), so this is interpolation and reliable.")

def box(pre, ans, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d
def say(s): return {"say": s}

# ---------- misconception helper ----------
def mis(pattern, expect, message, note=None):
    m = {"pattern": pattern, "expect": expect, "message": message}
    if note: m["note"] = note
    return m

# =================== BRONZE ===================
pb["bronze_description"] = ("Read a value straight off a bar chart, work out a pie chart "
    "fraction or angle, and name a correlation.")

b = pb["bronze"]
# [0] cat = 25
b[0]["hint"] = "Follow the top of the Cat bar across to the number axis."
b[0]["guided_steps"] = [
    say("Find the Cat bar, then read across to the number axis. The scale goes up in 5s."),
    box("The Cat bar is how many gridlines above zero? ", 5, "Count the gridlines; each one is worth 5."),
    box("Each gridline is 5 students, so 5 × 5 = ", 25, "Five fives.", phase="substitute"),
    box("Check: the Cat bar sits level with which number on the axis? ", 25,
        "It reaches 25.", done="Cat = 25. Read straight across."),
]
b[0]["misconceptions"] = [
    mis("gridline_not_scaled", 5, "Each gridline is worth 5, not 1. The Cat bar is 5 gridlines up, so 5 × 5 = 25."),
]
# [1] PE - Art = 10
b[1]["hint"] = "Read both bars the question names, then subtract Art from PE."
b[1]["guided_steps"] = [
    say("Read the two bars the question names, PE and Art, then subtract."),
    box("Read the PE bar: ", 30, "PE reaches 30."),
    box("Read the Art bar: ", 20, "Art reaches 20."),
    box("How many more chose PE? 30 − 20 = ", 10, "Subtract Art from PE.", phase="substitute"),
    box("Check: Art plus your answer should give PE. 20 + 10 = ", 30,
        "Returns to 30.", done="10 more chose PE. Read both, then subtract."),
]
b[1]["misconceptions"] = [
    mis("added_not_subtracted", 50, "How many MORE means subtract, not add: 30 − 20 = 10."),
    mis("gave_pe_only", 30, "30 is just the PE bar. The question asks how many MORE than Art, so 30 − 20 = 10."),
]
# [2] fraction 1/2
b[2]["hint"] = "Write car over the total, then simplify by dividing both by their common factor."
b[2]["guided_steps"] = [
    say("A fraction is the part over the whole. Car is 30 out of 60, then simplify."),
    box("How many people in total? ", 60, "The whole survey is 60 people."),
    box("Car is 30 out of 60. Divide top and bottom by 30. Top: 30 ÷ 30 = ", 1,
        "30 divided by 30.", phase="substitute"),
    box("Bottom: 60 ÷ 30 = ", 2, "60 divided by 30."),
    box("Check: does 1 out of 2 match 30 out of 60? 60 ÷ 2 = ", 30,
        "Half of 60.", done="30/60 = 1/2. Simplify by dividing both by 30."),
]
b[2]["misconceptions"] = [
    mis("not_simplified", None, "30 out of 60 is right, but simplify it: divide both by 30 to get 1/2."),
]
# [3] total 28
b[3]["hint"] = "Add the height of every bar together."
b[3]["guided_steps"] = [
    say("The total is every bar added together. The bars read 2, 6, 10, 7 and 3."),
    box("Add the first two: 2 + 6 = ", 8, "2 plus 6."),
    box("Add the next: 8 + 10 = ", 18, "8 plus 10.", phase="substitute"),
    box("Add the next: 18 + 7 = ", 25, "18 plus 7."),
    box("Add the last: 25 + 3 = ", 28, "25 plus 3."),
    box("Check another way: (2 + 3) + (6 + 7) + 10 = 5 + 13 + 10 = ", 28,
        "5 + 13 + 10.", done="28 students in total. Add every bar."),
]
b[3]["misconceptions"] = [
    mis("missed_a_bar", 25, "Add every bar, including the D grade. 2 + 6 + 10 + 7 + 3 = 28."),
]
# [4] history 30 (add pie svg)
b[4]["hint"] = "Angle over 360 gives the fraction; multiply that by 200."
svg_hist = pie_svg([("History 54°", 54)], "A pie chart with a History sector of 54 degrees, total 200 students")
b[4]["display"] = svg_hist + b[4]["display"]
b[4]["guided_steps"] = [
    say("Angle over 360 gives the fraction. Then scale up to the total of 200."),
    box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
    box("Fraction that is History: 54 ÷ 360 = ", 0.15, "54 divided by 360.", phase="substitute"),
    box("Multiply by the total: 0.15 × 200 = ", 30, "0.15 of 200."),
    box("Check: 30 out of 200 as an angle = (30 ÷ 200) × 360 = ", 54,
        "Returns to 54°.", done="30 chose History. Angle to fraction to people."),
]
b[4]["misconceptions"] = [
    mis("angle_as_count", 54, "54 is the angle, not the number of students. Work out (54 ÷ 360) × 200 = 30."),
]
# [5] angle 54
b[5]["hint"] = "Fraction of people times 360 gives the angle."
b[5]["guided_steps"] = [
    say("Frequency over total gives the fraction of the circle. Multiply by 360 for the angle."),
    box("Fraction that chose Cycling: 36 ÷ 240 = ", 0.15, "36 divided by 240."),
    box("Angle = 0.15 × 360 = ", 54, "0.15 of 360.", phase="substitute"),
    box("Check: a 54° sector out of 240 people = (54 ÷ 360) × 240 = ", 36,
        "Returns to 36.", done="The Cycling angle is 54°. Fraction of people, times 360."),
]
b[5]["misconceptions"] = [
    mis("times_people_not_360", 36, "Multiply the fraction by 360°, not by the number of people. 0.15 × 360 = 54."),
]
# [6] MC most rainfall
b[6]["hint"] = "Find the tallest bar and read off its month."
b[6]["misconceptions"] = [mis("wrong_bar", None, "The tallest bar is November at 95 mm.")]
# [7] MC negative correlation
b[7]["hint"] = "As exercise goes up, does resting heart rate rise or fall?"
b[7]["misconceptions"] = [mis("mislabels_trend", None,
    "As exercise increases, heart rate decreases, so this is negative correlation.")]

# =================== SILVER ===================
pb["silver_description"] = ("Compare two data sets, convert between pie chart angles and "
    "frequencies, read a line graph range, and find a modal class.")
s = pb["silver"]
# [0] girls - boys swimming = 10
s[0]["hint"] = "Read both Swimming bars, then subtract boys from girls."
s[0]["guided_steps"] = [
    say("Read both Swimming bars, then find the difference."),
    box("Read the Girls Swimming bar: ", 25, "Girls reach 25."),
    box("Read the Boys Swimming bar: ", 15, "Boys reach 15."),
    box("How many more girls? 25 − 15 = ", 10, "Subtract boys from girls.", phase="substitute"),
    box("Check: Boys plus your answer should give Girls. 15 + 10 = ", 25,
        "Returns to 25.", done="10 more girls chose swimming. Read both, then subtract."),
]
s[0]["misconceptions"] = [
    mis("added_not_subtracted", 40, "How many MORE girls means subtract: 25 − 15 = 10, not add."),
]
# [1] MC positive
s[1]["hint"] = "As temperature rises, do sales rise or fall?"
s[1]["misconceptions"] = [mis("mislabels_trend", None,
    "As temperature increases, sales increase, so this is positive correlation.")]
# [2] fourth sector 100
s[2]["hint"] = "All sectors add to 360°, so subtract the known angles from 360."
s[2]["display"] = pie_svg([("100°", 100), ("90°", 90), ("70°", 70), ("?", 100)],
    "A pie chart with sectors of 100, 90 and 70 degrees and a fourth unknown sector") + " " + s[2]["display"]
s[2]["guided_steps"] = [
    say("All sectors of a pie add to 360°. Add the known angles, then subtract from 360."),
    box("Add the first two known angles: 100 + 90 = ", 190, "100 plus 90."),
    box("Add the third: 190 + 70 = ", 260, "190 plus 70.", phase="substitute"),
    box("Fourth sector = 360 − 260 = ", 100, "360 minus 260."),
    box("Check: 100 + 90 + 70 + 100 = ", 360, "All four should total 360.",
        done="The fourth sector is 100°. Sectors fill 360°."),
]
s[2]["misconceptions"] = [
    mis("gave_sum_not_remainder", 260, "260 is the total of the three known angles. The fourth = 360 − 260 = 100."),
]
# [3] 30 people (add pie svg)
s[3]["hint"] = "Angle over 360 gives the fraction; multiply that by 180."
s[3]["display"] = pie_svg([("A 60°", 60)], "A pie chart with sector A of 60 degrees, total 180 people") + " " + s[3]["display"]
s[3]["guided_steps"] = [
    say("Angle over 360 gives the fraction. Then multiply by the total of 180."),
    box("Simplify 60/360: divide both by 60. Bottom: 360 ÷ 60 = ", 6, "So the fraction is 1/6."),
    box("Number = 180 ÷ 6 = ", 30, "180 divided by 6.", phase="substitute"),
    box("Check: 30 out of 180 as an angle = (30 ÷ 180) × 360 = ", 60,
        "Returns to 60°.", done="Sector A is 30 people. Angle to fraction to people."),
]
s[3]["misconceptions"] = [
    mis("angle_as_count", 60, "60 is the angle, not the number of people. (60 ÷ 360) × 180 = 30."),
]
# [4] range 8
s[4]["hint"] = "Range is the highest value minus the lowest."
s[4]["guided_steps"] = [
    say("Range is the highest value minus the lowest. Scan the line for both."),
    box("Read the highest point on the line: ", 22, "The peak is on Friday."),
    box("Read the lowest point on the line: ", 14, "The lowest is on Monday."),
    box("Range = 22 − 14 = ", 8, "Highest minus lowest.", phase="substitute"),
    box("Check: lowest plus range should give highest. 14 + 8 = ", 22,
        "Returns to 22.", done="The range is 8°C. Highest minus lowest."),
]
s[4]["misconceptions"] = [
    mis("added_not_subtracted", 36, "Range means highest minus lowest, not add: 22 − 14 = 8."),
]
# [5] MC modal class 10-20 (add freq polygon chart)
s[5]["hint"] = "Find the midpoint with the highest frequency, then name its class."
s[5]["chart"] = {"type": "line", "data": {"datasets": [{"data": [
    {"x": 5, "y": 6}, {"x": 15, "y": 14}, {"x": 25, "y": 10}, {"x": 35, "y": 4}],
    "fill": False, "tension": 0, "borderColor": "#3b82f6", "pointRadius": 4,
    "pointBackgroundColor": "#3b82f6"}]},
    "options": {"scales": {
        "x": {"type": "linear", "min": 0, "max": 40, "ticks": {"stepSize": 10},
              "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "Midpoint", "display": True}},
        "y": {"min": 0, "max": 16, "ticks": {"stepSize": 2},
              "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "Frequency", "display": True},
              "beginAtZero": True}}}}
s[5]["misconceptions"] = [mis("mislabels_modal", None,
    "Midpoint 15 has the highest frequency (14), so the modal class is 10 to 20.")]
# [6] MC positive
s[6]["hint"] = "As age rises, does reaction time rise or fall?"
s[6]["misconceptions"] = [mis("mislabels_trend", None,
    "As age increases, reaction time increases, so this is positive correlation.")]

# =================== GOLD ===================
pb["gold_description"] = ("Combine steps: stacked bar percentages, comparing two pie charts, "
    "and estimating from a line of best fit.")
g = pb["gold"]
# [0] north % of Q2 = 40
g[0]["hint"] = "Add the Q2 parts for the total, then North as a percentage of it."
g[0]["guided_steps"] = [
    say("Add the parts of the Q2 stack for the total, then North as a percentage of it."),
    box("Add the Q2 parts: 40 + 30 + 30 = ", 100, "North plus South plus East."),
    box("North as a fraction: 40 ÷ 100 = ", 0.4, "40 out of 100.", phase="substitute"),
    box("As a percentage: 0.4 × 100 = ", 40, "Multiply by 100."),
    box("Check: 40% of 100 = 0.4 × 100 = ", 40, "Returns to 40.",
        done="North is 40% of Q2. Total, share, percentage."),
]
g[0]["misconceptions"] = [
    mis("missed_a_part", 57, "Add all three Q2 parts for the total: 40 + 30 + 30 = 100, then 40 ÷ 100 × 100 = 40."),
]
# [1] two pies, difference 0 (add two-pie svg)
g[1]["hint"] = "Convert each school's Drama sector to a count, then compare the counts."
g[1]["display"] = two_pies_svg(
    {"sectors": [("Drama 72°", 72)], "caption": "School A (150)"},
    {"sectors": [("Drama 54°", 54)], "caption": "School B (200)"},
    "Two pie charts: School A Drama sector 72 degrees of 150, School B Drama sector 54 degrees of 200") + " " + g[1]["display"]
g[1]["guided_steps"] = [
    say("Work out each school's drama fans with (angle ÷ 360) × total, then compare."),
    box("School A: 72 ÷ 360 = ", 0.2, "72 out of 360."),
    box("School A drama fans: 0.2 × 150 = ", 30, "0.2 of 150."),
    box("School B: 54 ÷ 360 = ", 0.15, "54 out of 360.", phase="substitute"),
    box("School B drama fans: 0.15 × 200 = ", 30, "0.15 of 200."),
    box("Difference = 30 − 30 = ", 0, "Subtract the smaller from the larger."),
    box("Check: both schools have 30 fans, so the difference is ", 0,
        "Equal counts give 0.", done="Both have 30 drama fans, so the difference is 0. Convert each, then compare."),
]
g[1]["misconceptions"] = [
    mis("compared_angles", 18, "Compare the number of fans, not the angles. Both schools work out to 30, so the difference is 0."),
]
# [2] LOBF estimate 29
g[2]["hint"] = "Substitute x = 6 into y = 4x + 5."
g[2]["guided_steps"] = [
    say("Substitute the x-value into the line of best fit equation \\(y = 4x + 5\\)."),
    box("Work out 4 × 6: ", 24, "4 times 6."),
    box("Add 5: 24 + 5 = ", 29, "24 plus 5.", phase="substitute"),
    box("Check with the gradient: at x = 7, y = 4 × 7 + 5 = ", 33,
        "4 × 7 + 5.", done="y ≈ 29 at x = 6. The line climbs 4 each step."),
]
g[2]["misconceptions"] = [
    mis("forgot_intercept", 24, "Do not forget the + 5. y = 4 × 6 + 5 = 29."),
]
# [3] MC extrapolation - FIX em dashes in options + message
g[3]["hint"] = "Is x = 15 inside or outside the data range 1 to 10?"
g[3]["options"] = [
    "No, this is extrapolation outside the data range",
    "Yes, the line of best fit is always accurate",
    "Yes, if the correlation is strong it works",
    "No, because x = 15 is negative",
]
g[3]["misconceptions"] = [mis("trusts_extrapolation", None,
    "x = 15 is outside the data range (1 to 10). This is extrapolation and is unreliable.")]
# [4] scatter estimate 6
g[4]["hint"] = "Read the trend value straight up from x = 5."
g[4]["guided_steps"] = [
    say("The scatter shows errors falling as study hours rise. Use the trend at x = 5."),
    box("Read the errors at x = 4 hours: ", 8, "The point at 4 hours."),
    box("Read the errors at x = 6 hours: ", 4, "The point at 6 hours."),
    box("x = 5 is halfway between. Halfway between 8 and 4: (8 + 4) ÷ 2 = ", 6,
        "The average of 8 and 4.", phase="substitute"),
    box("Check against the point at x = 5 on the graph: ", 6,
        "The trend gives about 6.", done="About 6 errors at 5 hours. Read the trend between the points."),
]
g[4]["misconceptions"] = [
    mis("read_wrong_point", None, "Read straight up from x = 5 to the trend line: about 6 errors."),
]

# =================== TIER GUIDES ===================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: reading charts and simple pie sectors",
        "steps": [
            "<strong>Bar charts:</strong> follow the top of a bar across to the number axis. Each gridline is worth the scale shown, so a bar 5 gridlines up on a scale of 5 means 25.",
            "<strong>Pie sectors:</strong> turn an angle into people with (angle ÷ 360) × total, and a frequency into an angle with (frequency ÷ total) × 360.",
            "<strong>Correlation:</strong> both quantities rising together is positive; one rising as the other falls is negative; no pattern means none.",
        ],
        "example": {
            "question": "A bar chart shows Cats = 25, Dogs = 30. How many more chose dogs?",
            "steps": [
                {"label": "Read", "content": "Cats = 25, Dogs = 30"},
                {"label": "Subtract", "content": "30 − 25 = 5"},
                {"label": "Check", "content": "25 + 5 = 30"},
                {"label": "Answer", "content": "5 more chose dogs", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: comparing data, pie angles and ranges",
        "steps": [
            "<strong>Angle to frequency:</strong> divide the angle by 360 to get the fraction, then multiply by the total.",
            "<strong>Frequency to angle:</strong> divide the frequency by the total, then multiply by 360. A missing sector = 360 minus the known angles.",
            "<strong>Range:</strong> highest value minus lowest. <strong>Modal class:</strong> the group with the highest frequency.",
        ],
        "example": {
            "question": "A pie chart shows 240 people. The Bus sector is 90°. How many travel by bus?",
            "steps": [
                {"label": "Fraction", "content": "90 ÷ 360 = 1/4"},
                {"label": "Multiply", "content": "1/4 × 240 = 60"},
                {"label": "Check", "content": "(60 ÷ 240) × 360 = 90°"},
                {"label": "Answer", "content": "60 people", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: composite charts and lines of best fit",
        "steps": [
            "<strong>Stacked bars:</strong> read each part, add them for the total, then one part as a percentage: part ÷ total × 100.",
            "<strong>Comparing pie charts:</strong> convert each chart's sector to a frequency first, because equal angles on different totals mean different counts.",
            "<strong>Line of best fit:</strong> substitute the x-value into its equation to estimate y. Inside the data range (interpolation) is reliable, outside (extrapolation) is not.",
        ],
        "example": {
            "question": "A stacked bar shows North = 40, South = 30, East = 30. What percentage is North?",
            "steps": [
                {"label": "Total", "content": "40 + 30 + 30 = 100"},
                {"label": "Percentage", "content": "(40 ÷ 100) × 100 = 40%"},
                {"label": "Check", "content": "40% of 100 = 40"},
                {"label": "Answer", "content": "40%", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =================== GUIDED (opener + teach) ===================
opener_pie = pie_svg([("Walk", 90)], "A circle with a quarter sector labelled Walk and the rest Other")
teach_bronze_bar = bar_svg([("Football", 14), ("Rugby", 10), ("Tennis", 8), ("Golf", 4)],
    "Bar chart of favourite sports: Football 14, Rugby 10, Tennis 8, Golf 4", 16, 2, "Number of students")
teach_silver_pie = pie_svg([("Bus 90°", 90)], "A pie chart with a Bus sector of 90 degrees, total 240 people")

pd["guided"] = {
    "opener": {
        "steps": [
            say("Picture a form group of 20 students. Exactly a quarter of them walk to school. Here is that quarter drawn as a slice of a circle."),
            {"pre": "A quarter of the group walks. How many students is a quarter of 20? ",
             "post": "", "answer": 5, "hint": "20 divided by 4.", "display": opener_pie},
            box("A full circle is 360°. The walking slice is a quarter of the circle. How many degrees is a quarter of 360? ",
                90, "360 divided by 4."),
            say("You just built a pie chart slice. The fraction of people (a quarter) is the same as the fraction of the circle. So <strong>angle = fraction × 360°</strong>, and turned around, <strong>frequency = (angle ÷ 360) × total</strong>. That one idea powers every pie chart question."),
        ]
    },
    "teach": {
        "bronze": {
            "display": teach_bronze_bar + "The bar chart shows favourite sports in a class. How many more chose Football than Tennis?",
            "steps": [
                say("Read the two bars the question names, then compare them."),
                box("Read the Football bar: ", 14, "Football reaches 14."),
                box("Read the Tennis bar: ", 8, "Tennis reaches 8."),
                box("How many more chose Football? 14 − 8 = ", 6, "Subtract tennis from football."),
                box("Check: Tennis plus your answer should give Football. 8 + 6 = ", 14,
                    "Returns to 14.", done="6 more chose football. Read, then compare."),
            ],
        },
        "silver": {
            "display": teach_silver_pie + "The pie chart shows how 240 people travel. The Bus sector is 90°. How many travel by bus?",
            "steps": [
                say("Angle over 360 gives the fraction of people. Then scale to the total."),
                box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
                box("Simplify 90/360: divide both by 90. Bottom: 360 ÷ 90 = ", 4, "So the fraction is 1/4."),
                box("Number = 240 ÷ 4 = ", 60, "240 divided by 4."),
                box("Check: 60 out of 240 as an angle = (60 ÷ 240) × 360 = ", 90,
                    "Returns to 90°.", done="60 travel by bus. Angle to fraction to people."),
            ],
        },
        "gold": {
            "display": "A scatter graph of practice hours and goals scored has line of best fit \\(y = 3x + 2\\). The data covers x = 1 to x = 8. Estimate y when x = 4, and check it is reliable.",
            "steps": [
                say("Gold questions estimate from a line of best fit. Use its equation, then check the estimate is inside the data range."),
                box("The line of best fit is \\(y = 3x + 2\\). Work out 3 × 4: ", 12, "3 times 4."),
                box("Add the 2: 12 + 2 = ", 14, "12 plus 2."),
                box("x = 4 is inside the range 1 to 8, so this estimate is reliable. Read the line at x = 0: 3 × 0 + 2 = ", 2, "3 times 0, plus 2."),
                box("Check the climb: at x = 5, y = 3 × 5 + 2 = ", 17,
                    "3 × 5 + 2.", done="The line climbs 3 each step, so y = 14 at x = 4. Estimate, then check the range."),
            ],
        },
    },
}

json.dump(pd, open("_ps03e_shard.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written _ps03e_shard.json")
print("top keys:", list(pd.keys()))
