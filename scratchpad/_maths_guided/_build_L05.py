# -*- coding: utf-8 -*-
import json, io

SRC = "_live_now.json"
OUT = "lesson_probability-statistics-L05.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---- helpers -------------------------------------------------------------
def box(pre, answer, hint, post="", say=None, done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None:
        d["say"] = say
    if done is not None:
        d["done"] = done
    if phase:
        d["phase"] = "substitute"
    return d

def sy(say):
    return {"say": say}

# =========================================================================
# METHOD CARD (slim reference)
# =========================================================================
pd["method_card"] = {
    "title": "Cumulative Frequency, Box Plots & Histograms",
    "steps": [
        "Cumulative frequency: add running totals, plot at upper class boundaries, join with a smooth curve.",
        "Read the median at n ÷ 2, Q1 at n ÷ 4, Q3 at 3n ÷ 4. IQR = Q3 − Q1.",
        "Box plot shows five values: minimum, Q1, median, Q3, maximum.",
        "Histogram: frequency density = frequency ÷ class width, so frequency = fd × width."
    ],
    "content": "<p><strong>Cumulative frequency (CF)</strong> is a running total, plotted against the upper class boundary. Read the <strong>median</strong> at \\(n/2\\), <strong>Q1</strong> at \\(n/4\\), <strong>Q3</strong> at \\(3n/4\\); then <strong>IQR = Q3 − Q1</strong>.</p><p>A <strong>box plot</strong> shows minimum, Q1, median, Q3, maximum. <strong>Histograms</strong> use <strong>frequency density = frequency ÷ class width</strong>, so frequency = fd × width.</p>",
    "example": "<p><strong>80 students. The median is at the \\(80/2 = 40\\)th value. Read across from a cumulative frequency of 40 to find the median score.</strong></p>"
}

# =========================================================================
# TIER DESCRIPTIONS
# =========================================================================
pb = pd["problem_bank"]
pb["bronze_description"] = "One-step reads: a median, quartile, IQR, range or frequency density straight from a graph, box plot or single class."
pb["silver_description"] = "Two-step work: frequency from density and width, totals across unequal bars, or two quartiles read off a curve."
pb["gold_description"] = "Multi-step estimates: split a class, subtract from the total, or turn a quartile into a percentage or count."

# =========================================================================
# TIER GUIDES
# =========================================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: reading a single value",
        "steps": [
            "<strong>Cumulative frequency (CF)</strong> is a running total. On a CF graph the median is at position \\(n/2\\), the lower quartile \\(Q_1\\) at \\(n/4\\), the upper quartile \\(Q_3\\) at \\(3n/4\\): read up to that height, across to the curve, then down to the value.",
            "A <strong>box plot</strong> shows five values in order: minimum, \\(Q_1\\), median, \\(Q_3\\), maximum. The <strong>IQR</strong> is \\(Q_3 - Q_1\\) and the <strong>range</strong> is maximum minus minimum.",
            "For a single histogram class, <strong>frequency density = frequency ÷ class width</strong>."
        ],
        "example": {
            "question": "A box plot has minimum 8, Q1 = 15, median 20, Q3 = 27, maximum 34. Find the IQR.",
            "steps": [
                {"label": "Pick the quartiles", "content": "<p>IQR uses only the two box edges, \\(Q_3\\) and \\(Q_1\\), not the median.</p>"},
                {"label": "Check", "content": "<p>27 and 15 are the quartiles, and \\(27 - 15\\) leaves a positive spread.</p>"},
                {"label": "Answer", "content": "<p>IQR = \\(Q_3 - Q_1 = 27 - 15 = 12\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: two-step frequency and spread",
        "steps": [
            "To turn a histogram bar into a real frequency, multiply: <strong>frequency = frequency density × class width</strong>. Watch the width: a class like 20 to 50 is 30 wide, not 10.",
            "Add every bar's frequency to get the total. To go the other way, <strong>frequency density = frequency ÷ width</strong>.",
            "On a CF graph, read \\(Q_1\\) at \\(n/4\\) and \\(Q_3\\) at \\(3n/4\\), then <strong>IQR = \\(Q_3 - Q_1\\)</strong>."
        ],
        "example": {
            "question": "A histogram has classes 0 to 10 (fd 3) and 10 to 40 (fd 2). Find the total frequency.",
            "steps": [
                {"label": "First bar", "content": "<p>Width 10: \\(3 \\times 10 = 30\\).</p>"},
                {"label": "Second bar", "content": "<p>Width is 30, not 10: \\(2 \\times 30 = 60\\).</p>"},
                {"label": "Check", "content": "<p>The wider bar holds more, and \\(60 > 30\\) fits.</p>"},
                {"label": "Answer", "content": "<p>Total = \\(30 + 60 = 90\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: multi-step estimates from graphs",
        "steps": [
            "Some questions ask for <strong>part of a class</strong>. Find the whole bar's frequency (fd × width), then take the fraction you need, assuming the data is spread evenly across the class.",
            "'More than \\(x\\)' from a CF graph means <strong>total − cumulative frequency</strong> at \\(x\\): read the CF at \\(x\\), then subtract from \\(n\\).",
            "Above \\(Q_3\\) is the top <strong>25%</strong>; between \\(Q_1\\) and \\(Q_3\\) is the middle <strong>50%</strong>. Multiply the percentage by \\(n\\) for a count."
        ],
        "example": {
            "question": "A CF graph for 160 students has \\(Q_3 = 72\\). How many scored above 72?",
            "steps": [
                {"label": "Top quarter", "content": "<p>Above \\(Q_3\\) is the top 25% of the data.</p>"},
                {"label": "Check", "content": "<p>25% of 160 is a quarter, and a quarter of 160 is a whole number.</p>"},
                {"label": "Answer", "content": "<p>\\(160 \\times 0.25 = 40\\) students</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# =========================================================================
# GUIDED: opener + teach walks
# =========================================================================
pd["guided"] = {
    "opener": {
        "label": "Before any graphs",
        "display": "A shop counts customers as the morning goes on:<br>By 9am: 4 customers<br>By 10am: 10 customers<br>By 11am: 20 customers",
        "steps": [
            box("How many customers by 11am? ", 20,
                "It is the last running total, everyone counted so far.",
                say="These running totals are the cumulative frequency: each one counts everyone so far. Look at the numbers, no graph needed."),
            box("Halfway position of 20 customers: 20 ÷ 2 = the ", 10,
                "Half of 20.", post="th",
                say="The middle customer is halfway through the 20, and that halfway point marks the <strong>median</strong> time. To find its position, halve the total."),
            sy("That is the whole idea. A cumulative frequency graph plots these running totals so you can read across from the halfway height (\\(n/2\\)) to the median, and from \\(n/4\\) and \\(3n/4\\) to the quartiles. A <strong>box plot</strong> draws those key values, and a <strong>histogram</strong> handles the same grouped data using frequency density.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A cumulative frequency graph shows the marks of 60 students. Reading across from a cumulative frequency of 30 meets the curve at a mark of 52; from 15 it meets 40; from 45 it meets 64.",
            "label": "Together: your first one",
            "steps": [
                box("The median is at the n ÷ 2 position. n = 60, so n ÷ 2 = ", 30,
                    "Halve the total number of students.",
                    say="60 students sat a test. To find the median, first find its position, then read the graph."),
                box("Read up to a cumulative frequency of 30, across to the curve, then down. The median mark is ", 52,
                    "The value stated for a cumulative frequency of 30."),
                box("The lower quartile Q1 is at n ÷ 4 = 60 ÷ 4 = ", 15,
                    "Divide the total by 4.",
                    say="Now the quartiles."),
                box("Reading across from a cumulative frequency of 15 gives Q1 = 40. The upper quartile is at 3n ÷ 4 = 3 × 60 ÷ 4 = ", 45,
                    "Three quarters of 60."),
                box("Reading across from 45 gives Q3 = 64. Now the interquartile range: IQR = Q3 − Q1 = 64 − 40 = ", 24,
                    "Subtract Q1 from Q3."),
                box("Check: Q1 + IQR should return Q3. 40 + 24 = ", 64,
                    "Add the IQR onto Q1.",
                    done="It gives back Q3 = 64, so the quartiles and IQR are consistent. The median is 52.")
            ]
        },
        "silver": {
            "display": "A histogram of waiting times has three bars: 0 to 10 minutes (fd = 3), 10 to 30 minutes (fd = 4), 30 to 40 minutes (fd = 2). How many people altogether?",
            "label": "Together: the silver move",
            "steps": [
                box("Frequency = frequency density × class width. Bar 0 to 10: 3 × 10 = ", 30,
                    "Width is 10.",
                    say="A histogram's bars show frequency density. Multiply by the width to get an actual frequency. Do each bar."),
                box("Bar 10 to 30 is wider. Its width = 30 − 10 = ", 20,
                    "30 minus 10, not 10."),
                box("So its frequency = 4 × 20 = ", 80,
                    "Multiply the density 4 by the width 20."),
                box("Bar 30 to 40: 2 × 10 = ", 20,
                    "Width is 10 again."),
                box("Total frequency = 30 + 80 + 20 = ", 130,
                    "Add the three bar frequencies.",
                    done="Gone. The wide middle bar is the whole point: its width is 20, not 10."),
                box("Check: work back. The middle bar holds 80 people over a width of 20, so its fd = 80 ÷ 20 = ", 4,
                    "Divide the frequency by the width.",
                    done="It returns fd = 4, matching the graph, so the total 130 is right.")
            ]
        },
        "gold": {
            "display": "A histogram shows house prices. The 200 to 300 (£000s) bar has fd = 0.6. Estimate how many houses cost between 250 and 300 thousand pounds. Assume prices are spread evenly within the class.",
            "label": "Together: the gold move",
            "steps": [
                box("The bar runs 200 to 300 but we only want 250 to 300. First the whole bar: width = 300 − 200 = ", 100,
                    "Top of the class minus the bottom.",
                    say="We want only part of a bar, so find the whole bar's frequency, then take the slice we need."),
                box("Whole-bar frequency = fd × width = 0.6 × 100 = ", 60,
                    "Multiply the density by the width."),
                box("We want 250 to 300, a width of 300 − 250 = ", 50,
                    "300 minus 250."),
                box("That is half of the 100-wide class, so take half the frequency: 60 × (50 ÷ 100) = ", 30,
                    "Half of 60.",
                    done="Gone. Only the requested slice of the bar counts."),
                box("Check: 250 to 300 is half the class, so it should hold half of 60. Half of 60 = ", 30,
                    "Divide 60 by 2.",
                    done="It matches, so 30 houses is right.")
            ]
        }
    }
}

# =========================================================================
# PER-PROBLEM: hints, misconception edits, guided_steps
# =========================================================================
def set_hint(tier, idx, h):
    pb[tier][idx]["hint"] = h

def set_gs(tier, idx, steps):
    pb[tier][idx]["guided_steps"] = steps

# ---- BRONZE ----
set_hint("bronze", 0, "The median sits at the n ÷ 2 position; read across from there to the score.")
pb["bronze"][0]["misconceptions"][0]["message"] = (
    "To find the median you must read across from a cumulative frequency of 40, that is n ÷ 2 = 80 ÷ 2 = 40, then down to the score. "
    "Reading at a cumulative frequency of 80 (the total) instead lands at the top of the curve and gives the maximum score, not the median.")
set_gs("bronze", 0, [
    box("The median is at the n ÷ 2 position. n = 80, so n ÷ 2 = ", 40,
        "Halve the total number of students.",
        say="80 students sat a test. The cumulative frequency curve is on the card. To find the median, first find its position."),
    sy("Now use the graph: go up the cumulative frequency axis to 40, across to the curve, then straight down to the score axis."),
    box("On this curve, a cumulative frequency of 40 lines up with a score of ", 40,
        "Follow the grid across from 40, then down to the score.", phase=True),
    box("Check: the lower quartile Q1 is at n ÷ 4 = 80 ÷ 4 = ", 20,
        "Divide the total by 4.",
        done="Reading across from a cumulative frequency of 20 gives about 32, and from 60 gives 50, so the median 40 sits between the quartiles as it must. Correct.")
])

set_hint("bronze", 1, "Read up from a score of 60 to the curve, then across to the cumulative frequency.")
set_gs("bronze", 1, [
    sy("Cumulative frequency is a running total: at each score it counts everyone up to there."),
    box("First read the total: at the highest score (100) the curve reaches ", 120,
        "The top of the curve is everyone."),
    box("Now 'less than 60': read up from a score of 60 to the curve and across. The cumulative frequency is ", 80,
        "Up to the curve at 60, then across to the y-axis.", phase=True),
    box("Check: those scoring 60 or more = total − 80 = 120 − 80 = ", 40,
        "Subtract 80 from the total.",
        done="80 below and 40 at or above sum to 120, the whole group, so 80 is right.")
])

set_hint("bronze", 2, "The median is the line inside the box, not one of its edges.")
set_gs("bronze", 2, [
    sy("A box plot marks five values in order: minimum, Q1, median, Q3, maximum."),
    box("Q1 is the LEFT edge of the box. Read it: ", 160, "Left side of the box.", post=" cm"),
    box("Q3 is the RIGHT edge of the box. Read it: ", 170, "Right side of the box.", post=" cm"),
    box("The median is the line INSIDE the box, between the two edges. Read it: ", 165,
        "Not an edge, the line within the box.", post=" cm", phase=True),
    box("Check: the median must lie between Q1 and Q3. 170 − 165 = ", 5,
        "Subtract the median from Q3.",
        done="5 is positive, so 165 is below Q3 and inside the box. Correct.")
])

set_hint("bronze", 3, "IQR = Q3 − Q1, the two edges of the box.")
set_gs("bronze", 3, [
    sy("IQR = Q3 − Q1. Read the two edges of the box."),
    box("Q1 is the left edge: ", 20, "Left side of the box."),
    box("Q3 is the right edge: ", 40, "Right side of the box."),
    box("IQR = Q3 − Q1 = 40 − 20 = ", 20, "Subtract Q1 from Q3.", phase=True),
    box("Check: the IQR must be smaller than the full range. Range = max − min = 55 − 10 = ", 45,
        "Subtract the minimum from the maximum.",
        done="20 is less than the range 45, as the middle-half spread should be. Correct.")
])

set_hint("bronze", 4, "Range = maximum − minimum, the two whisker ends.")
set_gs("bronze", 4, [
    sy("Range = maximum − minimum. Those are the two whisker ends, far left and far right."),
    box("The minimum is the left whisker end: ", 10, "Far-left tip.", post=" s"),
    box("The maximum is the right whisker end: ", 20, "Far-right tip.", post=" s"),
    box("Range = max − min = 20 − 10 = ", 10, "Subtract the minimum from the maximum.", post=" s", phase=True),
    box("Check: the IQR is Q3 − Q1 = 18 − 12 = ", 6,
        "Subtract Q1 from Q3.",
        done="The IQR 6 is smaller than the range 10, correct since the middle half is narrower than the whole. Range is 10.")
])

set_hint("bronze", 5, "Frequency density = frequency ÷ class width.")
set_gs("bronze", 5, [
    sy("Frequency density = frequency ÷ class width. Find the width first."),
    box("Class width = 40 − 20 = ", 20, "Top of the class minus the bottom."),
    box("Frequency density = frequency ÷ width = 30 ÷ 20 = ", 1.5,
        "Divide 30 by the width.", phase=True),
    box("Check: multiply back. fd × width = 1.5 × 20 = ", 30,
        "Multiply the density by the width.",
        done="It returns the original frequency 30, so fd = 1.5 is right.")
])

set_hint("bronze", 6, "The box, from Q1 to Q3, always holds the middle half of the data.")
set_gs("bronze", 6, [
    sy("A box plot is split into four equal quarters by Q1, the median and Q3. Each quarter holds 25% of the data."),
    box("From Q1 up to the median is one quarter, worth ", 25, "One quarter of the data.", post="%"),
    box("From the median up to Q3 is another quarter, worth ", 25, "Another quarter.", post="%"),
    box("Between Q1 and Q3 covers both quarters: 25 + 25 = ", 50, "Add the two quarters.", post="%", phase=True),
    box("Check: the box is always the middle half of the data. Half of 100% = ", 50,
        "Halve 100.", post="%",
        done="Both routes give 50%, so the box holds 50% of the data.")
])

set_hint("bronze", 7, "IQR = Q3 − Q1; the median is not used.")
set_gs("bronze", 7, [
    sy("IQR = Q3 − Q1. The median (35) is a distractor here; it plays no part."),
    box("The upper quartile is Q3 = ", 48, "Given in the question."),
    box("The lower quartile is Q1 = ", 22, "Given in the question."),
    box("IQR = Q3 − Q1 = 48 − 22 = ", 26, "Subtract Q1 from Q3, ignore the median.", phase=True),
    box("Check: Q1 + IQR should return Q3. 22 + 26 = ", 48,
        "Add the IQR onto Q1.",
        done="It gives back Q3 = 48, so the IQR 26 is right.")
])

# ---- SILVER ----
set_hint("silver", 0, "Compare the two median lines; the one further right is the higher score.")
# S0 is multiple_choice: no guided_steps

set_hint("silver", 1, "Frequency = frequency density × class width, and the last class is 30 wide.")
set_gs("silver", 1, [
    sy("Each bar's frequency = frequency density × class width. Add them up. Watch the last bar's width."),
    box("Bar 0 to 10: fd 2 × width 10 = ", 20, "Width is 10."),
    box("Bar 10 to 20: fd 5 × width 10 = ", 50, "Width is 10."),
    box("Bar 20 to 50 is wider. Its width = 50 − 20 = ", 30, "50 minus 20, not 10."),
    box("Bar 20 to 50: fd 3 × width 30 = ", 90, "Multiply the density 3 by the width 30.", phase=True),
    box("Total frequency = 20 + 50 + 90 = ", 160,
        "Add the three bar frequencies.",
        done="The three bar frequencies add to 160, the whole data set.")
])

set_hint("silver", 2, "Read Q1 at n ÷ 4 and Q3 at 3n ÷ 4, then subtract.")
set_gs("silver", 2, [
    sy("IQR = Q3 − Q1. On a cumulative frequency graph, Q1 is at n ÷ 4 and Q3 is at 3n ÷ 4."),
    box("Q1 position = n ÷ 4 = 100 ÷ 4 = ", 25, "Divide 100 by 4."),
    box("Reading across from a cumulative frequency of 25 gives a score of ", 40,
        "Across from a cumulative frequency of 25, down to the score."),
    box("Q3 position = 3n ÷ 4 = 3 × 100 ÷ 4 = ", 75, "Three quarters of 100."),
    box("Reading across from a cumulative frequency of 75 gives a score of ", 60,
        "Across from a cumulative frequency of 75, down to the score.", phase=True),
    box("IQR = Q3 − Q1 = 60 − 40 = ", 20,
        "Subtract Q1 from Q3.",
        done="Q3 (60) minus Q1 (40) gives an IQR of 20.")
])

set_hint("silver", 3, "Frequency = frequency density × class width.")
set_gs("silver", 3, [
    sy("Frequency = frequency density × class width. Read the bar's height, then multiply by its width."),
    box("The 10 to 20 bar has a frequency density of ", 4, "Read the bar height off the y-axis."),
    box("Its class width = 20 − 10 = ", 10, "20 minus 10."),
    box("Frequency = fd × width = 4 × 10 = ", 40, "Multiply the height by the width.", phase=True),
    box("Check: divide back. 40 ÷ 10 = ", 4,
        "Divide the frequency by the width.",
        done="It returns the frequency density 4, so 40 patients is right.")
])

set_hint("silver", 4, "Frequency density = frequency ÷ class width.")
set_gs("silver", 4, [
    sy("Frequency density = frequency ÷ class width. Find the width first."),
    box("Class width = 15 − 5 = ", 10, "Top minus bottom of the class."),
    box("Frequency density = frequency ÷ width = 24 ÷ 10 = ", 2.4, "Divide 24 by the width.", phase=True),
    box("Check: multiply back. 2.4 × 10 = ", 24,
        "Multiply the density by the width.",
        done="It returns the frequency 24, so fd = 2.4 is right.")
])

# S5: reworded to an unambiguous single criterion (audit issue)
pb["silver"][5]["display"] = "Box plot A has range 40 and IQR 15. Box plot B has range 25 and IQR 20. Which data set has the greater overall range?"
set_hint("silver", 5, "Range is the full spread, maximum minus minimum, not the IQR.")
pb["silver"][5]["misconceptions"] = [
    {
        "check": "common",
        "expect": 1,
        "message": "Range is the full spread of the data: A's range is 40 and B's is 25, so A has the greater range. B only has the larger IQR (its middle 50%), which is not the overall range.",
        "pattern": "wrong_formula",
        "expect_note": "Student selects B (option index 1) because it has the larger IQR (20 > 15), confusing IQR with overall range."
    }
]
# S5 remains multiple_choice: no guided_steps; solutions stays [0] (A)

# S6: replace duplicate-of-B7 with a middle-50% count problem (audit issue)
pb["silver"][6]["display"] = "A cumulative frequency curve for 60 students gives Q1 = 28 and Q3 = 52. Estimate how many students scored between Q1 and Q3."
pb["silver"][6]["solutions"] = [30]
pb["silver"][6]["calculator"] = False
pb["silver"][6]["input_type"] = "single_value"
set_hint("silver", 6, "The middle 50% of the data lies between Q1 and Q3.")
pb["silver"][6]["misconceptions"] = [
    {
        "check": "common",
        "expect": 24,
        "message": "The middle 50% of the data lies between Q1 and Q3, so the count is 60 × 0.5 = 30 students. 24 is the IQR (52 − 28), a measure of spread, not a number of students.",
        "pattern": "wrong_formula",
        "expect_note": "Student reports the IQR (52 − 28 = 24) instead of the number of students in the middle half."
    }
]
set_gs("silver", 6, [
    sy("Between Q1 and Q3 is the middle 50% of the data: Q1 cuts off the bottom 25% and Q3 the top 25%."),
    box("The fraction of students between Q1 and Q3 = ", 50, "The middle half, two quarters.", post="%"),
    box("Number of students = 50% of 60 = 60 × 0.5 = ", 30, "Half of 60.", phase=True),
    box("Check: 30 students is the middle half, so doubling gives the whole group: 30 × 2 = ", 60,
        "Multiply 30 by 2.",
        done="It returns the total of 60, so 30 students lie between Q1 and Q3, not the IQR of 24.")
])

# ---- GOLD ----
# G0: signpost the split-bar assumption (audit issue) + clean the message dashes
pb["gold"][0]["display"] = "The histogram shows ages of visitors to a museum. Estimate the number of visitors aged between 15 and 25. Assume the ages are spread evenly within each class."
set_hint("gold", 0, "15 to 25 is half of the 10 to 20 bar plus half of the 20 to 30 bar.")
pb["gold"][0]["misconceptions"][0]["message"] = "15 to 20 is half of the 10 to 20 bar: fd 5 × width 5 = 25. 20 to 25 is half of the 20 to 30 bar: fd 3 × width 5 = 15. Total = 25 + 15 = 40."
set_gs("gold", 0, [
    sy("We want ages 15 to 25, which is not a whole bar. It is the top half of the 10 to 20 bar plus the bottom half of the 20 to 30 bar."),
    box("First the 10 to 20 bar: fd 5 × width 10 = ", 50, "Full bar frequency is fd times width."),
    box("We only want 15 to 20, half of that bar: 50 ÷ 2 = ", 25, "Half the bar, since 15 to 20 is half of 10 to 20."),
    box("Now the 20 to 30 bar: fd 3 × width 10 = ", 30, "Full bar frequency."),
    box("We only want 20 to 25, half of that bar: 30 ÷ 2 = ", 15, "Half of the bar.", phase=True),
    box("Total 15 to 25 = 25 + 15 = ", 40,
        "Add the two half-bars.",
        done="The two half-bars add to 40 visitors aged 15 to 25.")
])

set_hint("gold", 1, "'More than 75' = total − cumulative frequency at 75.")
set_gs("gold", 1, [
    sy("'More than 75' means everyone above 75. Cumulative frequency counts everyone up to 75, so subtract that from the total."),
    box("The total number of students is ", 200, "Given in the question, also the top of the curve."),
    box("Reading up from a mark of 75 to the curve gives a cumulative frequency of ", 180,
        "Up to the curve at 75, across to the y-axis."),
    box("More than 75 = total − CF at 75 = 200 − 180 = ", 20,
        "Subtract the cumulative frequency from the total.", phase=True),
    box("Check: those scoring 75 or less (180) plus those above (20) = ", 200,
        "Add 180 and 20.",
        done="180 + 20 = 200, the whole group, so 20 scored above 75.")
])

set_hint("gold", 2, "Lower outlier fence = Q1 − 1.5 × IQR.")
set_gs("gold", 2, [
    sy("An outlier lies more than 1.5 × IQR beyond a quartile. For the LOWER fence: Q1 − 1.5 × IQR. First the IQR."),
    box("IQR = Q3 − Q1 = 44 − 20 = ", 24, "Upper quartile minus lower quartile."),
    box("1.5 × IQR = 1.5 × 24 = ", 36, "Multiply the IQR by 1.5."),
    box("Lower fence = Q1 − 1.5 × IQR = 20 − 36 = ", -16,
        "Subtract 36 from Q1 = 20; the answer is negative.", phase=True),
    box("Check: the upper fence would be Q3 + 36 = 44 + 36 = ", 80,
        "Add 36 to Q3.",
        done="The lower fence −16 sits below Q1 and the upper fence 80 above Q3, so the fences straddle the data. Lower fence is −16.")
])

set_hint("gold", 3, "Find the frequency (fd × width), then write it as a percentage of 120.")
set_gs("gold", 3, [
    sy("First turn the bar into a frequency (fd × width), then express it as a percentage of the total 120."),
    box("Class width = 30 − 20 = ", 10, "30 minus 20."),
    box("Frequency = fd × width = 4.5 × 10 = ", 45, "Multiply 4.5 by the width."),
    box("Percentage = frequency ÷ total × 100 = 45 ÷ 120 × 100 = ", 37.5,
        "Divide 45 by 120, then times 100.", post="%", phase=True),
    box("Check: 37.5% of 120 should give back 45. 120 × 0.375 = ", 45,
        "Multiply 120 by 0.375.",
        done="It returns the frequency 45, so 37.5% is right.")
])

set_hint("gold", 4, "Above Q3 is the top 25%; use School A's total of 120.")
set_gs("gold", 4, [
    sy("Above Q3 is always the top quarter, 25% of that school. Use School A's total of 120. School B's numbers are a distraction."),
    box("The fraction of data above Q3 = ", 25, "Q3 cuts off the top quarter.", post="%"),
    box("School A has this many students: ", 120, "Given for School A, not B."),
    box("Students above Q3 = 25% of 120 = 120 × 0.25 = ", 30, "A quarter of 120.", phase=True),
    box("Check: a quarter of 120 is 120 ÷ 4 = ", 30,
        "Divide 120 by 4.",
        done="Both ways give 30 students above Q3.")
])

# =========================================================================
# VERIFY: each non-MC solution is hit by a guided box
# =========================================================================
report = []
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        if p.get("input_type") == "multiple_choice":
            continue
        gs = p.get("guided_steps")
        sol = p["solutions"][0]
        answers = [s["answer"] for s in gs if s.get("answer") is not None]
        if sol not in answers:
            report.append("%s[%d] solution %r not hit by any box %r" % (tier, i, sol, answers))
if report:
    print("SOLUTION-HIT PROBLEMS:")
    for r in report:
        print("  -", r)
else:
    print("All non-MC solutions are hit by a guided box.")

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
