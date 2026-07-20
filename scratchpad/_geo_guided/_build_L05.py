# -*- coding: utf-8 -*-
"""Build guided practice_data for Geography Skills L05 (Mean, Median, Mode & Range)."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_live_L05.json"), encoding="utf-8"))

B = pd["problem_bank"]["bronze"]
S = pd["problem_bank"]["silver"]
G = pd["problem_bank"]["gold"]


def box(pre, answer, hint, done=None, phase=None, post=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post: d["post"] = post
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d


def say(text):
    return {"say": text}


# ----------------------------------------------------------------- method card
pd["method_card"]["steps"] = [
    "Mean: add every value, then divide by how many values there are",
    "Median: sort the values, then take the middle one",
    "Mode: the value that appears most often",
    "Range: largest minus smallest. IQR: Q3 − Q1",
]
pd["method_card"]["content"] = (
    "<p><strong>Mean</strong> adds every value and divides by the count. It uses all the "
    "data, but one extreme value can drag it away from typical.</p>"
    "<p><strong>Median</strong> is the middle value once the data is sorted. With an even "
    "count, average the two middle values. Outliers barely move it, so it suits skewed data "
    "such as house prices.</p>"
    "<p><strong>Mode</strong> is the most common value or class. It is the only average that "
    "works for categories such as land use.</p>"
    "<p><strong>Range</strong> is largest minus smallest and shows total spread. The "
    "<strong>interquartile range</strong> (Q3 − Q1) covers the middle half, so it describes "
    "typical spread without the extremes.</p>"
)

# ------------------------------------------------------------ tier descriptions
pd["problem_bank"]["bronze_description"] = (
    "One small set of values: work out the mean, median, mode or range that the question asks for."
)
pd["problem_bank"]["silver_description"] = (
    "Bigger or repeated data: means from frequencies and bar charts, medians when an outlier is "
    "present, and the interquartile range."
)
pd["problem_bank"]["gold_description"] = (
    "Judge and compare: choose the fairest average, work with quartiles, and say what the spread "
    "shows about a place."
)

# ------------------------------------------------------------------ tier guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one small data set, one measure",
        "steps": [
            "Read the question to see which measure is wanted: mean, median, mode or range.",
            "Mean: add every value, then divide by how many values there are.",
            "Median: sort the values first, then take the middle one. Mode: the value that repeats most.",
            "Range: largest value minus smallest value.",
        ],
        "example": {
            "question": "Beach litter counts on 5 days: 12, 9, 15, 9, 10. Find the mean and the mode.",
            "steps": [
                {"label": "Count the values", "content": "<p>There are 5 daily counts.</p>"},
                {"label": "Add them", "content": "<p>12 + 9 + 15 + 9 + 10 = 55</p>"},
                {"label": "Divide by the count", "content": "<p>55 ÷ 5 = 11</p>"},
                {"label": "Check", "content": "<p>11 sits between the lowest count (9) and the highest (15), so it is believable. Only 9 repeats.</p>"},
                {"label": "Answer", "content": "<p>Mean = 11 items per day, mode = 9 items</p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: repeated values, charts and spread",
        "steps": [
            "When values repeat, multiply each value by its frequency, add the products, then divide by the total frequency.",
            "From a bar chart, read every bar off the vertical axis before calculating anything.",
            "If one value sits far from the rest, the median describes the group better than the mean.",
            "Interquartile range: sort, take Q1 (middle of the lower half) and Q3 (middle of the upper half), then subtract.",
        ],
        "example": {
            "question": "Quadrat counts: 1 plant in 3 quadrats, 2 plants in 5 quadrats, 3 plants in 2 quadrats. Find the mean.",
            "steps": [
                {"label": "Total quadrats", "content": "<p>3 + 5 + 2 = 10</p>"},
                {"label": "Total plants", "content": "<p>(1×3) + (2×5) + (3×2) = 3 + 10 + 6 = 19</p>"},
                {"label": "Divide", "content": "<p>19 ÷ 10 = 1.9</p>"},
                {"label": "Check", "content": "<p>1.9 lies between the smallest count (1) and the largest (3), so it is believable.</p>"},
                {"label": "Answer", "content": "<p>Mean = 1.9 plants per quadrat</p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: choosing and comparing",
        "steps": [
            "Decide which average is fair: extreme values pull the mean, so the median often describes a place better.",
            "Quote an average and a measure of spread together, because two places can share a mean yet differ hugely.",
            "Range covers everything including outliers. Interquartile range covers the middle half only.",
        ],
        "example": {
            "question": "Village house prices (£1000s): 180, 190, 195, 200, 950. Which average is fairer, and why?",
            "steps": [
                {"label": "Mean", "content": "<p>(180 + 190 + 195 + 200 + 950) ÷ 5 = 1715 ÷ 5 = 343</p>"},
                {"label": "Median", "content": "<p>Sorted: 180, 190, 195, 200, 950. Middle value = 195</p>"},
                {"label": "Check", "content": "<p>Four of the five houses cost under £200,000, so £343,000 describes none of them.</p>"},
                {"label": "Answer", "content": "<p>The median, £195,000, is fairer because the £950,000 house is an outlier</p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ----------------------------------------------------------------------- opener
OPENER_SVG = (
    '<p>Five friends compare what they get each week:</p>'
    '<svg viewBox="0 0 470 135" role="img" aria-label="Five friends and their weekly pocket money: '
    'Amy five pounds, Ben six pounds, Cara five pounds, Dan four pounds, Eve one hundred pounds">'
    '<circle cx="45" cy="52" r="32" fill="#eef3ec" stroke="#7a8b74" stroke-width="2"/>'
    '<text x="45" y="59" text-anchor="middle" font-size="18" fill="#2d2a26">£5</text>'
    '<text x="45" y="112" text-anchor="middle" font-size="13" fill="#5b564e">Amy</text>'
    '<circle cx="135" cy="52" r="32" fill="#eef3ec" stroke="#7a8b74" stroke-width="2"/>'
    '<text x="135" y="59" text-anchor="middle" font-size="18" fill="#2d2a26">£6</text>'
    '<text x="135" y="112" text-anchor="middle" font-size="13" fill="#5b564e">Ben</text>'
    '<circle cx="225" cy="52" r="32" fill="#eef3ec" stroke="#7a8b74" stroke-width="2"/>'
    '<text x="225" y="59" text-anchor="middle" font-size="18" fill="#2d2a26">£5</text>'
    '<text x="225" y="112" text-anchor="middle" font-size="13" fill="#5b564e">Cara</text>'
    '<circle cx="315" cy="52" r="32" fill="#eef3ec" stroke="#7a8b74" stroke-width="2"/>'
    '<text x="315" y="59" text-anchor="middle" font-size="18" fill="#2d2a26">£4</text>'
    '<text x="315" y="112" text-anchor="middle" font-size="13" fill="#5b564e">Dan</text>'
    '<circle cx="410" cy="52" r="32" fill="#f7ecd8" stroke="#c08a3e" stroke-width="2"/>'
    '<text x="410" y="59" text-anchor="middle" font-size="16" fill="#2d2a26">£100</text>'
    '<text x="410" y="112" text-anchor="middle" font-size="13" fill="#5b564e">Eve</text>'
    "</svg>"
)

pd["guided"] = {
    "opener": {
        "display": OPENER_SVG,
        "steps": [
            say("Amy, Ben, Cara and Dan get a few pounds each. Eve has a very generous grandma."),
            box(
                "Without doing any maths, what would you say a typical friend in this group gets each week, in pounds?",
                5,
                "Look at the amount that keeps coming up, and ignore the odd one out for now.",
                done="Almost everyone picks that. You chose it because it sits in the middle of the group and because it comes up more than any other amount.",
            ),
            box(
                "Now add all five amounts together and divide by 5. What do you get, in pounds?",
                24,
                "Add 5 + 6 + 5 + 4 + 100, then share the total equally between the five friends.",
                done="Not one of the five friends gets anything close to that. Eve on her own has dragged it up.",
            ),
            say(
                "You have just used all four measures in this lesson. The amount you picked by instinct is "
                "both the <strong>median</strong> (the middle value once sorted) and the <strong>mode</strong> "
                "(the most common value). The number you calculated is the <strong>mean</strong>. Eve is an "
                "<strong>outlier</strong>, and outliers pull the mean but leave the median alone. The "
                "<strong>range</strong>, 100 − 4 = 96, measures how spread out the group is."
            ),
        ],
    },
    "teach": {
        "bronze": {
            "display": "A student counted the cars parked on six streets: 5, 7, 8, 7, 9, 6. Find the mean, median, mode and range.",
            "steps": [
                say("Four different measures, one small data set. Start by getting your bearings in the data."),
                box("How many street counts are listed?", 6,
                    "Count the numbers in the list one by one.",
                    done="The mean always divides by this count, so get it right first."),
                box("Add the six counts together. What is the total?", 42,
                    "Add them in pairs: 5 + 7, then 8 + 7, then 9 + 6."),
                box("Divide the total by the number of streets to get the mean.", 7,
                    "Share the total equally between the six streets.",
                    done="The mean uses every value, so a single unusual street would move it."),
                say("Sorted smallest to largest, the counts run 5, 6, 7, 7, 8, 9."),
                box("With six values there is no single middle one. Add the two middle values and divide by 2. What is the median?", 7,
                    "The third and fourth values in the sorted list are the middle pair."),
                box("Which count appears more than once? That is the mode.", 7,
                    "Tally each value and look for the one that repeats."),
                box("Subtract the smallest count from the largest to get the range.", 4,
                    "Take 5 away from 9.",
                    done="Mean, median and mode all landed on the same number here, which tells you the data is evenly spread."),
                say("<strong>Check:</strong> the mean and median must both sit inside the range of the data, between 5 and 9. They do, so the answers are believable."),
            ],
        },
        "silver": {
            "display": "A student counted daisies in 20 quadrats: 1 daisy in 4 quadrats, 2 daisies in 6 quadrats, 3 daisies in 7 quadrats, 4 daisies in 3 quadrats. Calculate the mean number of daisies per quadrat.",
            "steps": [
                say("Here each value is repeated many times, so you cannot just add four numbers and divide by four."),
                box("How many different daisy counts are listed in the table?", 4,
                    "Count the distinct numbers of daisies, not the quadrats.",
                    done="Four values, but far more than four quadrats. That is the trap."),
                box("Add the four frequencies. How many quadrats were surveyed altogether?", 20,
                    "Add 4 + 6 + 7 + 3."),
                box("Multiply each daisy count by its frequency and add the results. How many daisies were counted in total?", 49,
                    "Work out 1×4, 2×6, 3×7 and 4×3, then add them together.",
                    done="This is the new move: value × frequency, summed. It is the same as writing every quadrat out and adding them."),
                box("Divide the total number of daisies by the number of quadrats. What is the mean?", 2.45,
                    "Share 49 daisies equally between 20 quadrats."),
                box("Which daisy count came up in the most quadrats? That is the mode.", 3,
                    "Look for the largest frequency, then read the daisy count next to it."),
                say("<strong>Check:</strong> the mean must lie between the smallest and largest counts, 1 and 4. It does, and it sits just below the modal value, which fits a data set with a few empty-ish quadrats."),
            ],
        },
        "gold": {
            "display": "Rainfall totals (mm) at 8 weather stations: 62, 48, 55, 71, 50, 66, 58, 44. Find the range and the interquartile range, then say which better describes typical spread.",
            "steps": [
                say("Two measures of spread, side by side. Sorted, the totals run 44, 48, 50, 55, 58, 62, 66, 71."),
                box("How many stations reported a rainfall total?", 8,
                    "Count the values in the list.",
                    done="An even count splits cleanly into two halves of four."),
                box("How many values sit in the lower half of the sorted list?", 4,
                    "Split the eight sorted values down the middle."),
                box("Q1 is the middle of the lower four, so average the 2nd and 3rd sorted values. What is Q1 in mm?", 49,
                    "The lower half runs 44, 48, 50, 55, so average its middle pair.",
                    done="Q1 is the value a quarter of the way through the data."),
                box("Q3 is the middle of the upper four. What is Q3 in mm?", 64,
                    "The upper half runs 58, 62, 66, 71, so average its middle pair."),
                box("Subtract Q1 from Q3 to get the interquartile range in mm.", 15,
                    "Take the lower quartile away from the upper quartile.",
                    done="This is the gold move: spread measured across the middle half only."),
                box("Now find the range: largest total minus smallest, in mm.", 27,
                    "Take 44 away from 71."),
                say("<strong>Check:</strong> the interquartile range must always be smaller than the range, because it throws away the top and bottom quarters. It is, so the working holds. The interquartile range describes typical spread better, since one unusually wet or dry station cannot inflate it."),
            ],
        },
    },
}

# =============================================================== BRONZE PROBLEMS
B[0]["hint"] = "Add every reading first, then divide by how many readings there are."
B[0]["misconceptions"] = [
    {"pattern": "divided_by_wrong_count",
     "message": "You have divided by the wrong number of readings. Count the days in the list again before you divide.",
     "expect": 16.8, "note": "101 divided by 6 instead of 7"},
    {"pattern": "gave_median",
     "message": "That is the middle reading once sorted, not the mean. The mean shares the total between every reading.",
     "expect": 14},
    {"pattern": "gave_range",
     "message": "That is the gap between the hottest and coldest day, not an average.",
     "expect": 5},
]
B[0]["guided_steps"] = [
    say("Seven daily temperatures were recorded: 14, 16, 13, 17, 15, 14, 12."),
    box("Get your bearings in the data first. How many temperature readings are listed?", 7,
        "Count the numbers in the list one by one.",
        done="The mean will divide by this count."),
    box("Add all the readings together. What is the total in °C?", 101,
        "Add in pairs if it helps: 14 + 16, then 13 + 17, and so on.", phase="substitute"),
    box("Divide the total by the number of readings. Give the mean to 1 decimal place.", 14.4,
        "Divide your total by 7 and round to one decimal place."),
    box("Check: the mean must sit between the coldest and hottest days. What was the coldest reading in °C?", 12,
        "Scan the list for the lowest number.",
        done="Your mean lies between 12 and 17, so it is believable."),
]

B[1]["hint"] = "Order the data from smallest to largest first."
B[1]["misconceptions"] = [
    {"pattern": "not_ordered",
     "message": "You have taken the middle of the list as it was written. The depths must be sorted before you pick the middle one.",
     "expect": 1.5, "note": "4th value of the unsorted list"},
    {"pattern": "gave_range",
     "message": "That is the spread from shallowest to deepest, not the middle value.",
     "expect": 1.2},
]
B[1]["guided_steps"] = [
    say("Seven depths were measured across the channel: 0.3, 0.8, 1.2, 1.5, 1.1, 0.7, 0.4."),
    box("Start with the shape of the data. How many depth readings are there?", 7,
        "Count the values listed.",
        done="An odd count means there is one true middle value."),
    box("Sort the depths in your head. What is the shallowest depth in metres?", 0.3,
        "Look for the lowest number in the list."),
    box("With seven sorted values, which position is the middle one? Give the position number.", 4,
        "The middle of seven has three values below it and three above it.", phase="substitute"),
    box("Count along your sorted list to that position. What depth is there, in metres?", 0.8,
        "Your sorted list starts 0.3, 0.4, 0.7, so keep counting along."),
    box("Check: how many of the depths are deeper than your median?", 3,
        "Count the values above it in your sorted list.",
        done="Three deeper and three shallower confirms you have the middle value."),
]

B[2]["hint"] = "Tally how many times each land use appears, then pick the biggest tally."
B[2]["misconceptions"] = [
    {"pattern": "chose_rarest",
     "message": "You have chosen one of the least common categories. The mode is the one that appears most often.",
     "expect": 3},
    {"pattern": "undercounted",
     "message": "Count the entries again, including every repeat. Another category appears more times than this one.",
     "expect": 1},
]
B[2]["guided_steps"] = [
    say("The survey listed: residential, residential, commercial, residential, parkland, commercial, residential, industrial, residential."),
    box("Locate yourself in the data. How many survey entries are there altogether?", 9,
        "Count every entry, including the repeats."),
    box("How many entries say commercial?", 2,
        "Read along the list and tally each time commercial appears."),
    box("How many entries say residential?", 5,
        "Read along the list again and tally residential.", phase="substitute"),
    box("Parkland and industrial each appear how many times?", 1,
        "Tally the two remaining categories."),
    say("Residential has the biggest tally, so the modal land use is <strong>residential</strong>."),
]

B[3]["hint"] = "Find the largest and smallest monthly totals, then subtract."
B[3]["misconceptions"] = [
    {"pattern": "first_minus_last",
     "message": "You have used the first and last values as written. Scan the whole list for the true largest and smallest.",
     "expect": 10},
    {"pattern": "added_extremes",
     "message": "You have added the two extremes. The range is a difference, so it needs a subtraction.",
     "expect": 95},
]
B[3]["guided_steps"] = [
    say("Six months of rainfall were recorded: 45, 38, 52, 41, 60, 35 mm."),
    box("How many months of data are listed?", 6,
        "Count the values in the list."),
    box("Scan the whole list. What is the largest monthly rainfall in mm?", 60,
        "Look for the highest number, wherever it sits in the list."),
    box("Now find the smallest monthly rainfall in mm.", 35,
        "Look for the lowest number, wherever it sits in the list.", phase="substitute"),
    box("Subtract the smallest from the largest to get the range in mm.", 25,
        "Take the smaller value away from the larger one."),
    box("Check: how many of the six months fall outside your largest and smallest values?", 0,
        "Look for any month above the highest or below the lowest.",
        done="Nothing lies outside, so the range really does cover all the data."),
]

B[4]["hint"] = "Look for the count that comes up more often than any other."
B[4]["misconceptions"] = [
    {"pattern": "gave_median",
     "message": "That is the middle value once the counts are sorted, not the most frequent one.",
     "expect": 131.5},
    {"pattern": "gave_frequency",
     "message": "You have given how many times it appeared rather than the traffic count itself.",
     "expect": 3},
    {"pattern": "gave_maximum",
     "message": "That is the busiest count recorded, not the one that came up most often.",
     "expect": 140},
]
B[4]["guided_steps"] = [
    say("Eight traffic counts were taken at the junction: 120, 135, 128, 140, 135, 115, 135, 122."),
    box("How many counts were recorded?", 8,
        "Count the values in the list."),
    box("How many different values appear, counting each one only once?", 6,
        "Ignore repeats: how many distinct numbers are there?"),
    box("Tally each distinct value. What is the biggest tally any single value reaches?", 3,
        "Go through the list marking off each value, then look for the largest tally.", phase="substitute"),
    box("Type the traffic count that reached that tally.", 135,
        "Find which number you tallied more than once."),
    box("Check: how many times does each of the other five values appear?", 1,
        "Look at the values you did not pick.",
        done="No other value repeats, so the mode is unique."),
]

B[5]["hint"] = "Read every bar's height off the vertical axis, add them, then divide by the number of months."
B[5]["misconceptions"] = [
    {"pattern": "wrong_divisor",
     "message": "You have divided by the wrong number of months. Count the bars along the bottom axis again.",
     "expect": 60, "note": "600 divided by 10"},
    {"pattern": "gave_mode",
     "message": "That is the bar height that appears twice, not the mean of all the months.",
     "expect": 70},
]
B[5]["guided_steps"] = [
    say("The bar chart shows tourist arrivals, in thousands, for each month of the year."),
    box("Start on the chart. Count the bars along the bottom axis: how many months are shown?", 12,
        "Every labelled month from Jan to Dec has its own bar.",
        done="This count is what you will divide by later."),
    box("Find the tallest bar and read its height off the vertical axis, in thousands.", 80,
        "Trace across from the top of the tallest bar to the scale on the left."),
    box("Read every bar in turn and add the heights. What is the total, in thousands?", 600,
        "Work along the chart from Jan to Dec, keeping a running total.", phase="substitute"),
    box("Divide the total by the number of months to get the mean, in thousands.", 50,
        "Share the total equally between the twelve months."),
    box("Check: how many bars are taller than your mean?", 6,
        "Picture a horizontal line at your mean and count the bars poking above it.",
        done="Six bars above and six below is exactly what a sensible average looks like."),
]

B[6]["hint"] = "Find the reading that comes up more often than any other."
B[6]["misconceptions"] = [
    {"pattern": "gave_median",
     "message": "That is the middle reading once sorted, not the most frequent one.",
     "expect": 5.65},
    {"pattern": "gave_frequency",
     "message": "You have given how many times it occurred rather than the pH value itself.",
     "expect": 3},
    {"pattern": "gave_range",
     "message": "That is the spread of the readings, not the most common one.",
     "expect": 1.1},
]
B[6]["guided_steps"] = [
    say("Eight soil pH readings were taken: 5.2, 6.1, 5.8, 5.5, 6.3, 5.2, 5.9, 5.2."),
    box("How many pH readings are listed?", 8,
        "Count the values one by one."),
    box("How many different pH values appear, counting each one only once?", 6,
        "Ignore repeats: how many distinct readings are there?"),
    box("Tally each distinct reading. What is the largest number of times any single reading appears?", 3,
        "Mark off each reading as you go, then look for the biggest tally.", phase="substitute"),
    box("Type the pH reading that appears that many times.", 5.2,
        "Find the reading you tallied more than once."),
    box("Check: how many times does each of the other readings appear?", 1,
        "Look at the readings you did not pick.",
        done="Every other reading occurs once, so the repeated one is the mode."),
]

B[7]["hint"] = "With an even number of values, find the mean of the two middle values."
B[7]["misconceptions"] = [
    {"pattern": "not_ordered",
     "message": "You have used the middle of the list as it was written. Sort the speeds into order first.",
     "expect": 21.5},
    {"pattern": "one_middle_only",
     "message": "With six values there is no single middle one, so you need both middle speeds.",
     "expect": 18},
    {"pattern": "gave_range",
     "message": "That is the spread from calmest to windiest, not the middle value.",
     "expect": 13},
]
B[7]["guided_steps"] = [
    say("Six wind speeds were recorded: 15, 22, 18, 25, 20, 12 km/h."),
    box("How many wind speed readings are there?", 6,
        "Count the values listed.",
        done="An even count means there is no single middle value."),
    box("Sort them. What is the lowest wind speed in km/h?", 12,
        "Look for the smallest number in the list."),
    box("The middle pair sit in positions 3 and 4 of your sorted list. What is the value in position 3, in km/h?", 18,
        "Count along your sorted list to the third value.", phase="substitute"),
    box("What is the value in position 4, in km/h?", 20,
        "It is the next value up from the third one."),
    box("Add the two middle speeds and divide by 2 to get the median in km/h.", 19,
        "Add them together, then halve the total."),
    box("Check: how many of the six speeds are below your median?", 3,
        "Count the sorted values that sit underneath it.",
        done="Three below and three above, which is exactly what a median does."),
]

# =============================================================== SILVER PROBLEMS
S[0]["display"] = ("A student measured pebble sizes (cm) on a beach. The bar chart shows how many "
                   "pebbles of each size were found. Calculate the mean pebble size, to the nearest "
                   "whole centimetre.")
S[0]["hint"] = "Multiply each size by its frequency, sum the products, then divide by total frequency."
S[0]["misconceptions"] = [
    {"pattern": "divided_by_bars",
     "message": "You have divided by the number of bars rather than by the total number of pebbles counted.",
     "expect": 32.4},
    {"pattern": "gave_total_frequency",
     "message": "That is how many pebbles were measured, not their mean size.",
     "expect": 40},
]
S[0]["guided_steps"] = [
    say("The bar chart shows how many pebbles of each size the student found."),
    box("Start on the chart. Read along the bottom axis: how many different pebble sizes are shown?", 5,
        "Each labelled group along the bottom is one size.",
        done="Five sizes, but far more than five pebbles. That is what makes this a frequency problem."),
    box("Read the height of the tallest bar off the vertical axis. How many pebbles were that size?", 12,
        "Trace across from the top of the tallest bar to the frequency scale."),
    box("Add all five bar heights. How many pebbles were measured altogether?", 40,
        "Read each bar's frequency in turn and keep a running total."),
    box("Multiply each size by its frequency and add the results. What is the total length of all the pebbles, in cm?", 162,
        "Work out 2×5, 3×8, 4×12, 5×10 and 6×5, then add them.", phase="substitute"),
    box("Divide that total by the number of pebbles, then round to the nearest whole centimetre.", 4,
        "Share the total length equally between all the pebbles you counted, then round."),
    box("Check: your mean must lie between the smallest and largest sizes on the chart. What is the largest size shown, in cm?", 6,
        "Read the label on the last group along the bottom axis.",
        done="The mean sits inside the range of sizes on the chart, so it is believable."),
]

S[1]["hint"] = "Sort the ten readings first, then average the two middle ones."
S[1]["misconceptions"] = [
    {"pattern": "not_ordered",
     "message": "You have used the middle of the list as it was written. Sort the readings before finding the middle.",
     "expect": 32},
    {"pattern": "gave_mean",
     "message": "That is the mean, and the extreme reading has dragged it upwards. The question asks for the middle value.",
     "expect": 21.5},
    {"pattern": "one_middle_only",
     "message": "With ten values there is no single middle reading, so you need both of the middle pair.",
     "expect": 19},
]
S[1]["guided_steps"] = [
    say("Ten noon temperatures were recorded: 18, 22, 15, 20, 45, 19, 21, 17, 20, 18 °C."),
    box("How many temperature readings are there?", 10,
        "Count the values listed."),
    box("One reading is far above all the others. What is it, in °C?", 45,
        "Look for the value that does not fit with the rest.",
        done="That outlier is exactly why the median is the safer average here."),
    box("Sort the readings. With ten values the middle pair sit in positions 5 and 6. What is the value in position 5, in °C?", 19,
        "Count along your sorted list to the fifth value.", phase="substitute"),
    box("What is the value in position 6, in °C?", 20,
        "It is the next value up in your sorted list."),
    box("Add the two middle readings and divide by 2. What is the median, in °C?", 19.5,
        "Add them together, then halve the total."),
    box("Check: how many readings sit below your median?", 5,
        "Count the sorted values underneath it.",
        done="Five below and five above. Notice the 45°C outlier barely moved it."),
]

S[2]["hint"] = "Order the data. Q1 = median of lower half, Q3 = median of upper half. IQR = Q3 − Q1."
S[2]["misconceptions"] = [
    {"pattern": "gave_range",
     "message": "That is the full range. The interquartile range uses only the middle half of the data.",
     "expect": 0.8},
    {"pattern": "added_quartiles",
     "message": "You have added the quartiles. The interquartile range is a difference between them.",
     "expect": 2.1},
    {"pattern": "gave_median",
     "message": "That is the middle value, not a measure of how spread out the middle half is.",
     "expect": 1.05},
]
S[2]["guided_steps"] = [
    say("Eight velocities were recorded: 0.8, 1.2, 0.9, 1.5, 1.1, 1.3, 0.7, 1.0 m/s."),
    box("How many velocity readings are there?", 8,
        "Count the values listed."),
    box("Sorted, what is the slowest velocity in m/s?", 0.7,
        "Scan the list for the lowest value."),
    box("Split the sorted list down the middle. How many readings are in each half?", 4,
        "Share the eight values evenly between two halves."),
    box("Q1 is the middle of the lower four, so average the 2nd and 3rd sorted values. What is Q1 in m/s?", 0.85,
        "The lower half runs 0.7, 0.8, 0.9, 1.0, so average its middle pair.", phase="substitute"),
    box("Q3 is the middle of the upper four. What is Q3 in m/s?", 1.25,
        "The upper half runs 1.1, 1.2, 1.3, 1.5, so average its middle pair."),
    box("Subtract Q1 from Q3 to get the interquartile range, in m/s.", 0.4,
        "Take the lower quartile away from the upper quartile."),
    box("Check: how many of the eight readings lie between Q1 and Q3?", 4,
        "Count the sorted values that sit between your two quartiles.",
        done="Half the readings sit inside it, which is exactly what the interquartile range measures."),
]

S[3]["hint"] = "Compare the frequencies and pick the class with the biggest one."
S[3]["misconceptions"] = [
    {"pattern": "second_highest",
     "message": "Another class has a higher frequency than this one. Compare all four frequencies again.",
     "expect": 2},
    {"pattern": "tallest_plants",
     "message": "You have picked the tallest plants rather than the most common height band. The modal class is about frequency.",
     "expect": 3},
]
S[3]["guided_steps"] = [
    say("The table gives four height bands with their frequencies: 0-10cm: 8, 10-20cm: 15, 20-30cm: 12, 30-40cm: 5."),
    box("Get oriented in the table. How many class intervals are listed?", 4,
        "Count the height bands down the left of the table."),
    box("Add the four frequencies. How many plants were measured altogether?", 40,
        "Add 8, 15, 12 and 5."),
    box("What is the highest frequency in the table?", 15,
        "Compare all four frequencies and take the biggest.", phase="substitute"),
    box("How many plants fall in the band immediately above the one with the highest frequency?", 12,
        "Read the frequency next to the 20-30cm band."),
    say("The 10-20cm band holds more plants than any other, so the modal class is <strong>10-20cm</strong>."),
]

S[4]["hint"] = "A smaller range means the values are packed more closely together."
S[4]["misconceptions"] = [
    {"pattern": "range_confusion",
     "message": "You have read a large range as consistency. A big range means the values are spread far apart.",
     "expect": 0},
    {"pattern": "said_cannot_tell",
     "message": "There is enough information here. The range on its own tells you how spread out the sizes are.",
     "expect": 3},
]
S[4]["guided_steps"] = [
    say("Beach A: mean 4.2cm, range 8. Beach B: mean 4.0cm, range 3."),
    box("Locate the spread figures first. What is the range of pebble sizes on Beach A, in cm?", 8,
        "Read the range quoted for Beach A, not the mean."),
    box("What is the range on Beach B, in cm?", 3,
        "Read the range quoted for Beach B."),
    box("Subtract the smaller range from the larger. How much wider is one spread than the other, in cm?", 5,
        "Take the smaller range away from the larger one.", phase="substitute"),
    box("Which beach has the smaller range? Type 1 for Beach A or 2 for Beach B.", 2,
        "The smaller of the two range figures wins."),
    say("The beach with the smaller range has pebbles that are far more similar in size, so <strong>Beach B</strong> is the more consistent one. The means are almost identical, so spread is what separates them."),
]

S[5]["hint"] = "Add all twelve monthly totals, divide by twelve, then round."
S[5]["misconceptions"] = [
    {"pattern": "wrong_divisor",
     "message": "You have divided by the wrong number of months. Count the values in the list again.",
     "expect": 58},
    {"pattern": "gave_median",
     "message": "That is the middle value once sorted, not the mean.",
     "expect": 47},
    {"pattern": "gave_range",
     "message": "That is the spread between the wettest and driest month, not an average.",
     "expect": 24},
]
S[5]["guided_steps"] = [
    say("Twelve monthly rainfall totals were recorded: 45, 38, 42, 55, 62, 48, 50, 44, 52, 40, 58, 46 mm."),
    box("How many monthly totals are listed?", 12,
        "Count the values in the list."),
    box("What is the largest monthly total, in mm?", 62,
        "Scan the whole list for the highest number."),
    box("Add all twelve totals. What is the sum, in mm?", 580,
        "Add them in groups of four, then combine the group totals.", phase="substitute"),
    box("Divide the sum by twelve and round to the nearest whole millimetre.", 48,
        "Share the total equally between the twelve months, then round."),
    box("Check: your mean must sit between the driest and wettest months. What is the smallest monthly total, in mm?", 38,
        "Scan the list for the lowest number.",
        done="Your mean lies between 38 and 62, so it is believable."),
]

S[6]["hint"] = "Work out all three measures separately, then match them to an option."
S[6]["misconceptions"] = [
    {"pattern": "mode_as_mean",
     "message": "You have used the most common reading as the mean. The mean shares the total between all six sites.",
     "expect": 1},
    {"pattern": "unsorted_and_lowest",
     "message": "The middle of the list as written is not the median, and the mode is not the lowest reading. Sort first, then tally.",
     "expect": 3},
]
S[6]["guided_steps"] = [
    say("Six sites were measured: 12, 14, 11, 13, 14, 14 °C."),
    box("How many sites were measured?", 6,
        "Count the readings listed."),
    box("Add the six temperatures. What is the total, in °C?", 78,
        "Add them in pairs, then combine."),
    box("Divide the total by the number of sites to get the mean, in °C.", 13,
        "Share the total equally between the six sites.", phase="substitute"),
    box("Sorted, the readings run 11, 12, 13, 14, 14, 14. Average the middle pair to get the median, in °C.", 13.5,
        "The third and fourth sorted values are the middle pair."),
    box("Which temperature appears three times? Type it, in °C.", 14,
        "Tally each reading and find the one that repeats most."),
    say("A mean of 13, a median of 13.5 and a mode of 14 match the <strong>first option</strong>. Notice the three measures disagree because the readings are bunched at the top."),
]

# ================================================================= GOLD PROBLEMS
G[0]["hint"] = "Order all 12 values. Q1 = median of lower 6, Q3 = median of upper 6."
G[0]["misconceptions"] = [
    {"pattern": "gave_range",
     "message": "That is the full range. The interquartile range uses only the middle half of the sites.",
     "expect": 3.1},
    {"pattern": "gave_median",
     "message": "That is the middle value, not a measure of how spread out the middle half is.",
     "expect": 3.2},
    {"pattern": "added_quartiles",
     "message": "You have added the quartiles instead of subtracting one from the other.",
     "expect": 6.7},
]
G[0]["guided_steps"] = [
    say("Twelve river widths were recorded: 2.1, 3.4, 2.8, 5.2, 3.1, 2.5, 4.8, 3.6, 2.9, 3.3, 4.1, 3.0 m."),
    box("How many width measurements are there?", 12,
        "Count the values listed."),
    box("Sorted, what is the narrowest width, in metres?", 2.1,
        "Scan the list for the smallest value."),
    box("Split the sorted list down the middle. How many values are in each half?", 6,
        "Share the twelve values evenly between two halves."),
    box("Q1 is the middle of the lower six, so average the 3rd and 4th sorted values. What is Q1, in metres?", 2.85,
        "The lower half runs 2.1, 2.5, 2.8, 2.9, 3.0, 3.1, so average its middle pair.", phase="substitute"),
    box("Q3 is the middle of the upper six. What is Q3, in metres?", 3.85,
        "The upper half runs 3.3, 3.4, 3.6, 4.1, 4.8, 5.2, so average its middle pair."),
    box("Subtract Q1 from Q3 to get the interquartile range, in metres.", 1.0,
        "Take the lower quartile away from the upper quartile."),
    box("Check: how many of the twelve widths lie between Q1 and Q3?", 6,
        "Count the sorted values sitting between your two quartiles.",
        done="Six of the twelve, the middle half, which is exactly what the interquartile range measures."),
]

G[1]["options"] = [
    "River B is faster on average but more variable, while River A is slower and more consistent, suggesting a more uniform channel",
    "River A is faster and more consistent",
    "River B is faster and more consistent",
    "Both rivers have similar characteristics",
]
G[1]["hint"] = "Compare the two means first, then compare the two interquartile ranges."
G[1]["misconceptions"] = [
    {"pattern": "mismatched_spread",
     "message": "You have paired the higher mean with the smaller spread. Check which river has the larger interquartile range.",
     "expect": 2},
    {"pattern": "misread_mean",
     "message": "Read the two mean velocities again. The river with the higher mean is the faster one on average.",
     "expect": 1},
    {"pattern": "said_similar",
     "message": "The two rivers differ on both figures given, so look at the numbers again before calling them alike.",
     "expect": 3},
]
G[1]["guided_steps"] = [
    say("River A: mean 0.8 m/s, IQR 0.3 m/s. River B: mean 1.2 m/s, IQR 0.9 m/s."),
    box("Locate the averages first. What is River B's mean velocity, in m/s?", 1.2,
        "Read the mean quoted for River B, not its IQR."),
    box("How much faster is River B's mean than River A's, in m/s?", 0.4,
        "Subtract River A's mean from River B's mean."),
    box("Now move to the spread. What is River B's interquartile range, in m/s?", 0.9,
        "Read the IQR quoted for River B.", phase="substitute"),
    box("How many times bigger is River B's interquartile range than River A's?", 3,
        "Divide River B's IQR by River A's IQR."),
    say("River B is faster on average, but its velocities vary three times as much, so River A is the steadier river with the more uniform channel. That is the <strong>first option</strong>."),
]

G[2]["hint"] = "Think about what single number a grouped table uses to stand in for every value in a class."
G[2]["misconceptions"] = [
    {"pattern": "blamed_error",
     "message": "A slip is always possible, but an estimate from grouped data is expected to differ. Think about what value the table uses for each class.",
     "expect": 1},
    {"pattern": "always_higher",
     "message": "A grouped estimate can land either side of the true value, depending on where the readings sit inside each class.",
     "expect": 2},
]
G[2]["guided_steps"] = [
    say("The team took 20 temperature readings. Grouped estimate: 16.5°C. Actual mean from raw data: 17.2°C."),
    box("Locate the two figures. What is the estimated mean from the grouped table, in °C?", 16.5,
        "Read the figure that came from the grouped frequency table."),
    box("What is the actual mean from the raw data, in °C?", 17.2,
        "Read the figure that came from the original readings."),
    box("How much higher is the actual mean than the estimate, in °C?", 0.7,
        "Subtract the estimate from the actual mean.", phase="substitute"),
    box("How many readings were taken altogether?", 20,
        "Read the number of readings from the question."),
    say("A grouped table replaces every reading in a class with the class mid-point. If the real readings sit above those mid-points, the estimate comes out low, which is why it is 0.7°C under the true mean here. That is the <strong>first option</strong>."),
]

G[3]["options"] = [
    "Median = 402.5, because the 1200 reading is an extreme outlier that would skew the mean",
    "Mean = 480.5, because it includes all the data",
    "Mode, because it ignores all outliers completely",
    "Range = 820, because it shows the full spread",
]
G[3]["hint"] = "Work out both averages, then judge which one the extreme reading has distorted."
G[3]["misconceptions"] = [
    {"pattern": "chose_mean",
     "message": "The mean uses every value including the extreme one, so it ends up higher than any ordinary site.",
     "expect": 1},
    {"pattern": "chose_range",
     "message": "The range measures spread, not a typical value, so it cannot answer this question.",
     "expect": 3},
    {"pattern": "chose_mode",
     "message": "Every reading here is different, so this measure has nothing to pick out.",
     "expect": 2},
]
G[3]["guided_steps"] = [
    say("Ten sites were sampled: 380, 395, 410, 425, 1200, 390, 405, 415, 400, 385 ppm."),
    box("Locate the data. How many sites were sampled?", 10,
        "Count the readings listed."),
    box("One reading sits far above the rest. What is it, in ppm?", 1200,
        "Look for the value that does not fit the pattern."),
    box("Add all ten readings. What is the total, in ppm?", 4805,
        "Add the nine ordinary readings first, then add the extreme one.", phase="substitute"),
    box("Divide by the number of sites to get the mean, in ppm.", 480.5,
        "Share the total equally between the ten sites."),
    box("Sorted, the middle pair sit in positions 5 and 6. Average them to get the median, in ppm.", 402.5,
        "Sorted, the readings run 380, 385, 390, 395, then continue counting along."),
    say("Nine of the ten sites lie between 380 and 425 ppm. The mean is higher than every single one of them, while the median sits right among them, so the median describes typical conditions. That is the <strong>first option</strong>."),
]

G[4]["options"] = [
    "Both have the same average but City B varies far more because of continentality, since the sea moderates City A's temperatures",
    "City B is hotter because it has a larger range",
    "The range is irrelevant, only the mean matters",
    "City A must be further from the equator because its range is smaller",
]
G[4]["hint"] = "Compare the two means first, then ask what the difference in range says about distance from the sea."
G[4]["misconceptions"] = [
    {"pattern": "range_as_heat",
     "message": "A larger range means a bigger gap between hottest and coldest, not a higher average temperature.",
     "expect": 1},
    {"pattern": "ignored_range",
     "message": "The two means are identical here, so the mean on its own cannot tell the cities apart.",
     "expect": 2},
    {"pattern": "blamed_latitude",
     "message": "Latitude is not the only control on temperature range. Think about how far each city is from the sea.",
     "expect": 3},
]
G[4]["guided_steps"] = [
    say("City A (coastal): mean 12°C, range 8°C. City B (inland): mean 12°C, range 22°C."),
    box("Locate the averages first. What is City A's mean temperature, in °C?", 12,
        "Read the mean quoted for City A, not its range."),
    box("What is the difference between the two mean temperatures, in °C?", 0,
        "Subtract one mean from the other."),
    box("Now move to the spread. What is City B's range, in °C?", 22,
        "Read the range quoted for City B.", phase="substitute"),
    box("How much larger is City B's range than City A's, in °C?", 14,
        "Subtract City A's range from City B's range."),
    say("Identical means but a range 14°C wider tells you the two climates behave very differently. The sea warms and cools slowly, so coastal City A has mild winters and cooler summers, while inland City B swings between extremes. That is the <strong>first option</strong>."),
]

out = os.path.join(HERE, "lesson_L05.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", out)
