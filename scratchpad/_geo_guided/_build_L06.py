# -*- coding: utf-8 -*-
"""Build guided practice_data for Geography Skills L06 (Quartiles & IQR)."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
live = json.load(io.open(os.path.join(HERE, "_live_L06.json"), encoding="utf-8"))
pb = live["problem_bank"]


def box(pre, answer, hint, done=None, phase=None, post=None, say=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post: d["post"] = post
    if done: d["done"] = done
    if phase: d["phase"] = phase
    if say: d["say"] = say
    return d


def say(text):
    return {"say": text}


def mis(pattern, message, expect):
    return {"pattern": pattern, "message": message, "expect": expect}


# ---------------------------------------------------------------- opener SVG
def queue_svg():
    parts = ['<svg viewBox="0 0 480 118" role="img" aria-label="A queue of eight '
             'people standing one behind the other, numbered 1 at the front to 8 at the back">',
             '<rect x="0" y="0" width="480" height="118" rx="10" fill="#faf6ee" stroke="#e3dccd"/>']
    for i in range(8):
        cx = 42 + i * 56
        parts.append('<circle cx="%d" cy="38" r="12" fill="#e6d7b4" stroke="#8a7a55" stroke-width="2"/>' % cx)
        parts.append('<rect x="%d" y="54" width="20" height="30" rx="9" fill="#cddbe6" stroke="#5c7a94" stroke-width="2"/>' % (cx - 10))
        parts.append('<text x="%d" y="104" font-size="13" text-anchor="middle" fill="#5a5348">%d</text>' % (cx, i + 1))
    parts.append('<text x="42" y="16" font-size="11" text-anchor="middle" fill="#8a7a55">front</text>')
    parts.append('</svg>')
    return "".join(parts)


def boxplot_svg():
    def x(v):
        return 60 + v * 72

    p = ['<svg viewBox="0 0 560 232" role="img" aria-label="Two horizontal box plots '
         'of river width in metres. The upper plot, River Aln, has a box from 2.0 to 4.5 '
         'with a median line at 3.0 and whiskers from 1.0 to 5.5. The lower plot, River '
         'Coquet, has a box from 2.5 to 4.0 with a median line at 3.0 and whiskers from 1.5 to 5.0.">',
         '<rect x="0" y="0" width="560" height="232" rx="10" fill="#faf6ee" stroke="#e3dccd"/>']
    rows = [("River Aln", 30, 60, 1.0, 2.0, 3.0, 4.5, 5.5, "#3b82f6", "rgba(59,130,246,0.22)"),
            ("River Coquet", 108, 138, 1.5, 2.5, 3.0, 4.0, 5.0, "#ef4444", "rgba(239,68,68,0.22)")]
    for label, ly, cy, mn, q1, med, q3, mx, stroke, fillc in rows:
        p.append('<text x="60" y="%d" font-size="13" fill="#5a5348">%s</text>' % (ly, label))
        p.append('<line x1="%g" y1="%d" x2="%g" y2="%d" stroke="%s" stroke-width="2"/>' % (x(mn), cy, x(q1), cy, stroke))
        p.append('<line x1="%g" y1="%d" x2="%g" y2="%d" stroke="%s" stroke-width="2"/>' % (x(q3), cy, x(mx), cy, stroke))
        for v in (mn, mx):
            p.append('<line x1="%g" y1="%d" x2="%g" y2="%d" stroke="%s" stroke-width="2"/>' % (x(v), cy - 10, x(v), cy + 10, stroke))
        p.append('<rect x="%g" y="%d" width="%g" height="28" fill="%s" stroke="%s" stroke-width="2"/>'
                 % (x(q1), cy - 14, x(q3) - x(q1), fillc, stroke))
        p.append('<line x1="%g" y1="%d" x2="%g" y2="%d" stroke="%s" stroke-width="3"/>' % (x(med), cy - 14, x(med), cy + 14, stroke))
    p.append('<line x1="60" y1="180" x2="492" y2="180" stroke="#8a7a55" stroke-width="2"/>')
    v = 0.0
    while v <= 6.0001:
        big = abs(v - round(v)) < 1e-9
        p.append('<line x1="%g" y1="180" x2="%g" y2="%d" stroke="#8a7a55" stroke-width="1"/>' % (x(v), x(v), 188 if big else 184))
        if big:
            p.append('<text x="%g" y="204" font-size="12" text-anchor="middle" fill="#5a5348">%d</text>' % (x(v), int(round(v))))
        v += 0.5
    p.append('<text x="276" y="224" font-size="12" text-anchor="middle" fill="#5a5348">River width (m)</text>')
    p.append('</svg>')
    return "".join(p)


# ---------------------------------------------------------------- guided
guided = {
    "opener": {
        "display": ("<p>Eight people are queuing at a bus stop. You want to split the "
                    "queue into four equal groups, front to back.</p>" + queue_svg()),
        "steps": [
            say("No maths method needed yet. Just share the queue out fairly."),
            box("How many people are in each of the four groups?", 2,
                "Share 8 people equally between 4 groups.",
                done="Splitting into four equal groups means three cuts fall between the people."),
            box("The middle cut falls exactly halfway down the queue. How many people stand in front of it?", 4,
                "Half of the queue stands in front of the middle cut."),
            box("How many people stand between the first cut and the last cut?", 4,
                "Count the people who are not in the front group and not in the back group.",
                done="Half the queue sits between the outer two cuts."),
            say("Those three cuts are the <strong>quartiles</strong>. The first cut is "
                "<strong>Q1</strong>, the middle cut is the <strong>median (Q2)</strong> and the last "
                "cut is <strong>Q3</strong>. The stretch between Q1 and Q3 holds the middle half of "
                "the data, and its size is the <strong>interquartile range (IQR)</strong>. You have "
                "just done the whole idea with people instead of numbers."),
        ],
    },
    "teach": {
        "bronze": {
            "display": ("<p>Stream depth (cm) measured at 7 points along a channel, already in "
                        "order: 6, 9, 14, 20, 26, 33, 45.</p><p>Find Q1, Q3 and the IQR.</p>"),
            "steps": [
                say("Odd number of values, so there is one clear middle depth. Find it first."),
                box("How many depths are listed?", 7, "Count them left to right.",
                    done="The count tells you where the middle sits."),
                box("Which position holds the middle depth? Count positions from the left.", 4,
                    "Add 1 to the count, then halve it.",
                    done="With 7 values the median is at position (7 + 1) ÷ 2 = 4."),
                box("Write that middle depth, in cm.", 20, "Count along to the 4th number."),
                box("Now ignore the median. The lower half is 6, 9, 14. Give its middle value. This is Q1.", 9,
                    "Three values means the middle one is the second.",
                    done="Q1 is just a median again, taken on the lower half only."),
                box("The upper half is 26, 33, 45. Give its middle value. This is Q3.", 33,
                    "Same move as Q1, but on the values above the median."),
                box("Subtract Q1 from Q3 to get the IQR, in cm.", 24, "Q3 minus Q1."),
                box("Check: how many of the seven depths lie between Q1 and Q3?", 3,
                    "Count the depths that are bigger than Q1 and smaller than Q3.",
                    done="Three of the seven depths sit inside the band, roughly the middle half, "
                         "which is exactly what the IQR should measure."),
            ],
        },
        "silver": {
            "display": ("<p>Air temperature (°C) logged at 8 survey points across a city, listed in "
                        "the order the sites were visited: 21, 26, 19, 30, 23, 34, 28, 25.</p>"
                        "<p>Find the IQR.</p>"),
            "steps": [
                say("These are in visiting order, not size order. Reordering is the first job, and "
                    "it is the step most often skipped."),
                box("How many temperatures are listed?", 8, "Count them.",
                    done="An even count means there is no single middle value."),
                box("Put them in order from smallest to largest. What is the smallest?", 19,
                    "Scan the whole list for the lowest number.",
                    done="In order: 19, 21, 23, 25, 26, 28, 30, 34."),
                box("How many temperatures are in the lower half?", 4,
                    "An even list splits into two equal halves with nothing left over.",
                    done="With an even count you do not leave a median out. Each half is simply half the list."),
                box("The lower half is 19, 21, 23, 25. Add its two middle values.", 44,
                    "Add the 2nd and 3rd of those four."),
                box("Halve that total to get Q1, in °C.", 22, "Divide by 2.",
                    done="With an even half you average the two middle values instead of picking one."),
                box("The upper half is 26, 28, 30, 34. Give Q1 of that half in the same way, which is Q3.", 29,
                    "Average 28 and 30."),
                box("Subtract Q1 from Q3 to get the IQR.", 7, "Q3 minus Q1."),
                box("Check: how many of the eight temperatures lie between Q1 and Q3?", 4,
                    "Count the values above Q1 and below Q3.",
                    done="Four of the eight, exactly the middle half, so the quartiles are in the right places."),
            ],
        },
        "gold": {
            "display": ("<p>Two box plots show river width at two survey sites.</p>" + boxplot_svg() +
                        "<p>How much wider is the middle half of the River Aln widths than the "
                        "middle half of the River Coquet widths?</p>"),
            "steps": [
                say("On a box plot the shaded box runs from Q1 to Q3, so the <strong>width of the "
                    "box is the IQR</strong>. The line inside is the median and the whiskers reach "
                    "the smallest and largest values."),
                box("Find the upper row, labelled River Aln. Reading down to the scale, what value "
                    "does the left edge of its box sit on, in metres?", 2,
                    "The left edge of the box is the lower quartile. Read straight down to the scale below.",
                    done="Locating yourself on the right plot before reading anything is the habit that "
                         "stops most box plot errors."),
                box("What value does the line inside the River Aln box sit on?", 3,
                    "The line inside the box marks the median."),
                box("What value does the right edge of the River Aln box sit on?", 4.5,
                    "The right edge of the box is the upper quartile. It is halfway between two labelled marks."),
                box("Subtract the left edge value from the right edge value to get the River Aln IQR.", 2.5,
                    "Q3 minus Q1 for the upper plot."),
                box("Now do the same for the River Coquet box: right edge minus left edge.", 1.5,
                    "Its box runs from 2.5 to 4.0."),
                box("Subtract the smaller IQR from the larger one.", 1,
                    "Take the Coquet IQR away from the Aln IQR.",
                    done="The Aln box is visibly the wider of the two, so a positive difference is "
                         "what the picture should give. Comparing box widths compares spreads, "
                         "which is not the same as comparing the median lines."),
            ],
        },
    },
}

# ---------------------------------------------------------------- tier guides
tier_guides = {
    "bronze": {
        "title": "Bronze: ordering data and finding the middle values",
        "steps": [
            "Put the values in order from smallest to largest before doing anything else.",
            "With an odd number of values the median is the single middle one, at position (n + 1) ÷ 2.",
            "Q1 is the middle of the values below the median. Q3 is the middle of the values above it. Leave the median itself out of both halves.",
            "The <strong>range</strong> is largest minus smallest. The <strong>IQR</strong> is Q3 minus Q1.",
        ],
        "example": {
            "question": "Slope angles (°) at 7 sites: 6, 9, 11, 14, 18, 22, 27. Find Q1.",
            "steps": [
                {"label": "Count and find the median",
                 "content": "<p>7 values, so the median sits at position (7 + 1) ÷ 2 = 4, which is 14°.</p>"},
                {"label": "Take the lower half",
                 "content": "<p>Values below the median: 6, 9, 11. The median itself is left out.</p>"},
                {"label": "Check",
                 "content": "<p>Three values in the lower half, so its middle one is the 2nd of the three.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p>Q1 = <strong>9°</strong></p>"},
            ],
        },
    },
    "silver": {
        "title": "Silver: even data sets and data you must reorder first",
        "steps": [
            "If the values are not already in size order, reorder them first. This is where most marks are lost.",
            "With an even number of values there is no single middle one, so split the list into two equal halves.",
            "For a quartile of an even half, add its two middle values and divide by 2.",
            "IQR = Q3 − Q1. A smaller IQR means the data is more tightly clustered.",
        ],
        "example": {
            "question": "Pebble masses (g) at 8 points: 24, 11, 30, 46, 15, 41, 21, 33. Find the IQR.",
            "steps": [
                {"label": "Order and split",
                 "content": "<p>11, 15, 21, 24 | 30, 33, 41, 46</p>"},
                {"label": "Quartiles",
                 "content": "<p>Q1 = (15 + 21) ÷ 2 = 18 g and Q3 = (33 + 41) ÷ 2 = 37 g</p>"},
                {"label": "Check",
                 "content": "<p>Two masses sit below Q1 and two sit above Q3, so both quartiles are central to their own half.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p>IQR = 37 − 18 = <strong>19 g</strong></p>"},
            ],
        },
    },
    "gold": {
        "title": "Gold: comparing spreads and reading box plots",
        "steps": [
            "On a box plot the box runs from Q1 to Q3, the line inside is the median and the whiskers reach the smallest and largest values.",
            "The width of the box is the IQR, so comparing two boxes compares two spreads directly.",
            "To compare, work out each IQR first and then subtract. Do not compare medians when the question asks about spread.",
            "An outlier is usually any value more than 1.5 × IQR above Q3 or below Q1.",
        ],
        "example": {
            "question": "Two box plots of river width: Site 1 has Q1 = 2.0 m and Q3 = 4.5 m; Site 2 has Q1 = 2.5 m and Q3 = 4.0 m. Which site varies more, and by how much?",
            "steps": [
                {"label": "IQR of each site",
                 "content": "<p>Site 1: 4.5 − 2.0 = 2.5 m. Site 2: 4.0 − 2.5 = 1.5 m.</p>"},
                {"label": "Check",
                 "content": "<p>The Site 1 box is the wider one on the scale, so the larger IQR belongs to Site 1 as expected.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p>Site 1 varies more, by <strong>2.5 − 1.5 = 1.0 m</strong></p>"},
            ],
        },
    },
}

# ---------------------------------------------------------------- method card
method_card = {
    "title": "Quartiles & IQR",
    "steps": [
        "Put every value in ascending order",
        "Q2 (median): the middle of the whole set",
        "Q1 and Q3: the medians of the lower and upper halves",
        "IQR = Q3 − Q1",
    ],
    "content": ("<p>Quartiles cut an <strong>ordered</strong> data set into four equal parts. "
                "<strong>Q1</strong> is the median of the lower half, <strong>Q2</strong> is the "
                "median of the whole set and <strong>Q3</strong> is the median of the upper half. "
                "The <strong>interquartile range</strong> is Q3 − Q1, the spread of the middle 50% "
                "of the data.</p><p>With an odd number of values, leave the median out of both "
                "halves. With an even number, split the list in two and average the middle pair of "
                "each half.</p><p>A smaller IQR means more consistent data. The IQR is more "
                "reliable than the range for fieldwork because extreme values are ignored.</p>"),
    "example": ("<p><strong>River widths (m) at 9 sites, ordered:</strong> 1.8, 2.1, 2.5, 3.0, 3.4, "
                "4.2, 4.8, 5.6, 6.1</p><p>Q2 = 5th value = 3.4. Q1 = (2.1 + 2.5) ÷ 2 = 2.3. "
                "Q3 = (4.8 + 5.6) ÷ 2 = 5.2.</p><p><strong>IQR = 5.2 − 2.3 = 2.9 m</strong></p>"),
}

# ---------------------------------------------------------------- bank edits
B = pb["bronze"]
S = pb["silver"]
G = pb["gold"]

# ---- bronze -----------------------------------------------------------------
B[0]["hint"] = "The list is already in order, so count how many values there are and step to the middle one."
B[0]["misconceptions"] = [
    mis("range_not_median",
        "That is the gap between the coldest and warmest months, not the middle month. The median is a value from the list, not a difference.",
        19),
    mis("midrange_not_median",
        "Averaging only the smallest and largest value ignores the five months in between. Step along the ordered list to the middle position instead.",
        13.5),
]
B[0]["guided_steps"] = [
    say("The list is already smallest to largest, so you can work straight down it."),
    box("How many temperatures are in the list?", 7, "Count the numbers one at a time, left to right.",
        done="The count decides where the middle falls."),
    box("With 7 values, which position holds the middle value? Count positions from the left.", 4,
        "Add 1 to the count, then halve it.", done="Position (7 + 1) ÷ 2 = 4.", phase="substitute"),
    box("Write the temperature in that position, in °C.", 14, "Count along to the 4th number in the list."),
    box("Check: how many temperatures sit above the one you picked?", 3,
        "Count the values to the right of it.",
        done="Three below and three above means the value really does split the set in half, so it is the median."),
]

B[1]["hint"] = "Leave the overall median out, then take the middle of the readings below it."
B[1]["misconceptions"] = [
    mis("included_median",
        "The overall median belongs to neither half. Including it leaves four readings in the lower half, so you end up averaging the wrong pair.",
        0.65),
    mis("gave_q3",
        "That is the middle of the upper half. Q1 comes from the readings below the median.",
        1.7),
]
B[1]["guided_steps"] = [
    say("Q1 is the middle of the lower half, so first find where the halfway point is."),
    box("How many velocity readings are listed?", 7, "Count them left to right."),
    box("Which position holds the overall median?", 4, "Add 1 to the count and halve it.",
        done="Position 4 splits the seven readings into three below and three above."),
    box("How many readings are in the lower half, once the median itself is left out?", 3,
        "Count only the readings to the left of position 4.", phase="substitute"),
    box("Give the middle reading of that lower half, in m/s. This is Q1.", 0.5,
        "Three readings means the middle one is the second."),
    box("Check: how many of the seven readings are smaller than the value you gave?", 1,
        "Count the readings to its left.",
        done="One reading below and one above inside the lower half is exactly what a lower quartile should look like."),
]

B[2]["hint"] = "Leave the median out, then find the mean of the two figures above it."
B[2]["misconceptions"] = [
    mis("picked_value",
        "With only two figures in the upper half you cannot pick one of them. Add the pair and halve it.",
        910),
    mis("used_maximum",
        "That is the wettest region, not the upper quartile. Q3 is a middle value of the upper half.",
        1050),
]
B[2]["guided_steps"] = [
    say("With five values the median is the middle one, and Q3 is the middle of what is left above it."),
    box("How many rainfall figures are listed?", 5, "Count them."),
    box("Which position holds the median?", 3, "Add 1 to the count and halve it."),
    box("How many figures sit above the median?", 2, "Count the figures to the right of position 3.",
        phase="substitute", done="Only two figures make up the upper half, so Q3 must fall between them."),
    box("Add those two figures together, in mm.", 1960, "Add the two largest figures."),
    box("Halve that total to get Q3, in mm.", 980, "Divide by 2."),
    box("Check: how many of the five figures are larger than Q3?", 1, "Count the figures above it.",
        done="Q3 lands between the two largest figures, so exactly one is above it, which is what an upper quartile does."),
]

B[3]["hint"] = "Find the middle of the lower three and the middle of the upper three, then subtract."
B[3]["misconceptions"] = [
    mis("range_not_iqr",
        "That is the full range, highest minus lowest. The IQR uses the quartiles and ignores both extremes.",
        48),
    mis("included_median",
        "The median has been counted in both halves, which puts four values in each half and shifts both quartiles inwards.",
        19.5),
]
B[3]["guided_steps"] = [
    say("The IQR compares the two quartiles, so build each one before subtracting."),
    box("How many countries are in the list?", 7, "Count them."),
    box("Which position holds the median?", 4, "Add 1 to the count and halve it.",
        done="The value at position 4 belongs to neither half."),
    box("The lower half is the three values before the median. Give its middle value. This is Q1.", 8,
        "Take the second of those three.", phase="substitute"),
    box("The upper half is the three values after the median. Give its middle value. This is Q3.", 34,
        "Take the second of those three."),
    box("Subtract Q1 from Q3 to get the interquartile range.", 26, "Q3 minus Q1."),
    box("Check: how many of the seven rates lie between Q1 and Q3?", 3,
        "Count the values that are bigger than Q1 and smaller than Q3.",
        done="Three of the seven sit inside the band, about the middle half, which is what the IQR is meant to cover."),
]

B[4]["hint"] = "With nine values the median is left out, so the lower half has an even number and needs averaging."
B[4]["misconceptions"] = [
    mis("included_median",
        "Counting the median into the lower half gives five values there, so the middle one you pick is too far up the list.",
        42),
    mis("gave_median",
        "That is the middle of the whole set, not the middle of the lower half.",
        63),
]
B[4]["guided_steps"] = [
    say("Nine values, so the median is a single value and each half has four."),
    box("How many areas are listed?", 9, "Count them."),
    box("Which position holds the median?", 5, "Add 1 to the count and halve it."),
    box("How many values are in the lower half once the median is left out?", 4,
        "Count the values to the left of position 5.", phase="substitute",
        done="Four values in the half means no single middle one, so you will average a pair."),
    box("Add the two middle values of that lower half.", 70, "Add the 2nd and 3rd of the four."),
    box("Halve that total to get Q1.", 35, "Divide by 2."),
    box("Check: how many of the nine values are smaller than Q1?", 2, "Count the values below it.",
        done="Two below and two above inside the lower half, so Q1 sits centrally in that half."),
]

B[5]["hint"] = "The range uses only the two ends of the list, nothing in between."
B[5]["misconceptions"] = [
    mis("iqr_not_range",
        "That is the interquartile range, the spread of the middle days only. The range uses the two extreme days.",
        6),
]
B[5]["guided_steps"] = [
    say("The range uses only the two ends of the ordered list."),
    box("How many daily temperatures are listed?", 7, "Count them."),
    box("Read the highest temperature, in °C.", 29, "It is the last value in an ordered list.",
        phase="substitute"),
    box("Read the lowest temperature, in °C.", 19, "It is the first value in an ordered list."),
    box("Subtract the lowest from the highest to get the range.", 10, "Highest minus lowest."),
    box("Check: how many of the seven temperatures fall between those two ends?", 5,
        "Count the values that are neither the highest nor the lowest.",
        done="All five of the other readings sit inside the range, which is exactly what the range should cover."),
]

B[6]["hint"] = "Find the median first, then take the middle of the three values above it."
B[6]["misconceptions"] = [
    mis("included_median",
        "The median has been pulled into the upper half, which gives four values there and drags the quartile down.",
        81),
    mis("used_maximum",
        "That is the highest rate, not the upper quartile. Q3 is a middle value of the upper half.",
        91),
]
B[6]["guided_steps"] = [
    say("Q3 is the middle of the upper half, so find the median first and then work above it."),
    box("How many nations are listed?", 7, "Count them."),
    box("Which position holds the median?", 4, "Add 1 to the count and halve it."),
    box("How many values sit above the median?", 3, "Count the values to the right of position 4.",
        phase="substitute", done="The median itself is not part of the upper half."),
    box("Give the middle value of those three. This is Q3.", 84, "Take the second of the three."),
    box("Check: how many of the seven rates are larger than the value you gave?", 1,
        "Count the rates above it.",
        done="One above and one below inside the upper half means Q3 is central to that half."),
]

B[7]["hint"] = "Work out both quartiles from the three values on each side of the median, then subtract."
B[7]["misconceptions"] = [
    mis("range_not_iqr",
        "That is the full range, the windiest day minus the calmest. The IQR ignores both extremes.",
        23),
    mis("included_median",
        "Counting the median into both halves puts four values in each, so both quartiles shift towards the middle.",
        10),
]
B[7]["guided_steps"] = [
    say("Find both quartiles first, then subtract."),
    box("How many daily wind speeds are listed?", 7, "Count them."),
    box("Which position holds the median?", 4, "Add 1 to the count and halve it."),
    box("Give the middle value of the three speeds below the median. This is Q1.", 12,
        "Take the second of those three.", phase="substitute"),
    box("Give the middle value of the three speeds above the median. This is Q3.", 25,
        "Take the second of those three."),
    box("Subtract Q1 from Q3 to get the IQR, then check it comes out below the full range of 23.", 13,
        "Q3 minus Q1.",
        done="It has to be smaller than the range, because the windiest and calmest days are left out."),
]

# ---- silver ------------------------------------------------------------------
S[0]["hint"] = "Leave the median out and take the middle reading of each half of five."
S[0]["misconceptions"] = [
    mis("range_not_iqr",
        "That is the full range, largest minus smallest. The IQR only spans the middle half.",
        7),
    mis("included_median",
        "The median has been counted into both halves, giving six readings in each and moving both quartiles inwards.",
        3.5),
]
S[0]["guided_steps"] = [
    say("Eleven values: the median is a single reading and each half has five."),
    box("How many monitoring points are listed?", 11, "Count them."),
    box("Which position holds the median?", 6, "Add 1 to the count and halve it."),
    box("How many readings are in the lower half once the median is left out?", 5,
        "Count the readings to the left of position 6.", phase="substitute"),
    box("Give the middle reading of that lower half. This is Q1.", 3.8,
        "Five readings means the middle one is the third."),
    box("Give the middle reading of the upper half. This is Q3.", 8,
        "Same move, on the five readings above the median."),
    box("Subtract Q1 from Q3 to get the IQR.", 4.2, "Q3 minus Q1."),
    box("Check: how many of the eleven readings lie between Q1 and Q3?", 5,
        "Count the readings bigger than Q1 and smaller than Q3.",
        done="Five of eleven sit inside the band, close to half the data, so the quartiles are placed correctly."),
]

S[1]["hint"] = "An even list splits into two halves of four, so the quartile is the mean of a pair."
S[1]["misconceptions"] = [
    mis("picked_value",
        "With four values in the lower half there is no single middle one, so a value copied straight from the list cannot be the quartile. Average the middle pair.",
        2800),
    mis("gave_q3",
        "That is the quartile of the upper half. Q1 comes from the four smallest values.",
        23600),
]
S[1]["guided_steps"] = [
    say("An even number of values splits cleanly into two halves with nothing left over."),
    box("How many countries are listed?", 8, "Count them."),
    box("How many countries are in the lower half?", 4, "Split the list straight down the middle.",
        phase="substitute", done="With an even list no value is left out, so each half is simply half the list."),
    box("Add the two middle values of that lower half, in dollars.", 7300, "Add the 2nd and 3rd of the four."),
    box("Halve that total to get Q1.", 3650, "Divide by 2."),
    box("Check: how many of the eight values are smaller than Q1?", 2, "Count the values below it.",
        done="Two below and two above inside the lower half, so Q1 sits in the middle of that half."),
]

S[2]["hint"] = "Site B gives you its quartiles, so work out its IQR and compare it with the IQR you are given for Site A."
S[2]["misconceptions"] = [
    mis("chose_listed_data",
        "Site A was picked without working out Site B's spread. Site B's quartiles are enough to find its IQR.",
        0),
    mis("thought_insufficient",
        "There is enough information here: a pair of quartiles is all you need for an IQR.",
        3),
]
S[2]["guided_steps"] = [
    say("Site B gives its quartiles, so you can work out its IQR and compare the two spreads."),
    box("How many pebble measurements are listed for Site A?", 9, "Count the values given for Site A."),
    box("Read Site B's upper quartile from the question.", 11, "Q3 is the larger of Site B's two quartiles."),
    box("Read Site B's lower quartile.", 4, "Q1 is the smaller of Site B's two quartiles.", phase="substitute"),
    box("Subtract to get Site B's IQR.", 7, "Q3 minus Q1 for Site B."),
    box("Site A's IQR is given as 5.0. How much larger is Site B's IQR?", 2,
        "Take Site A's IQR away from Site B's.",
        done="A wider middle half means the pebble sizes are more spread out, so the site with the bigger IQR varies more."),
    say("So the option to choose is <strong>Site B</strong>."),
]

S[3]["hint"] = "Reorder from smallest to largest first, then work on the top six values."
S[3]["misconceptions"] = [
    mis("used_original_order",
        "The months are still in calendar order. Quartiles only mean anything once the values are sorted by size.",
        13.5),
    mis("gave_q1",
        "That is the quartile of the lower half. Q3 comes from the six largest temperatures.",
        7),
]
S[3]["guided_steps"] = [
    say("The months are listed in calendar order, not size order, so the very first job is to reorder them."),
    box("How many monthly temperatures are listed?", 12, "Count them."),
    box("Once reordered, what is the smallest temperature, in °C?", 5, "Scan the whole list for the lowest value.",
        done="In order: 5, 6, 6, 8, 8, 10, 12, 13, 15, 16, 17, 18."),
    box("How many temperatures are in the upper half?", 6, "An even list splits into two equal halves.",
        phase="substitute"),
    box("Add the two middle values of that upper half, the 3rd and 4th of the six.", 31,
        "The upper half is 12, 13, 15, 16, 17, 18."),
    box("Halve that total to get Q3.", 15.5, "Divide by 2."),
    box("Check: how many of the twelve temperatures are higher than Q3?", 3, "Count the values above it.",
        done="Three of twelve sit above Q3, a quarter of the data, which is what an upper quartile should leave above it."),
]

S[4]["hint"] = "Read the two edges of the shaded box on the urban row, then subtract."
S[4]["misconceptions"] = [
    mis("range_not_iqr",
        "That is the whisker to whisker spread, the full range. The IQR is the width of the shaded box only.",
        28),
    mis("read_wrong_plot",
        "That is the width of the other row's box. Check the row label before reading the edges.",
        8),
]
S[4]["guided_steps"] = [
    say("Two box plots share one scale. The shaded box runs from Q1 to Q3, so its width is the IQR."),
    box("Find the row labelled Urban. Reading down to the scale, what value does the left edge of its shaded box sit on?",
        18, "The left edge of the box is the lower quartile. Read straight down to the scale.",
        done="Fixing which row you are on before reading any value is what stops most box plot mistakes."),
    box("What value does the right edge of the Urban box sit on?", 31,
        "The right edge of the box is the upper quartile.", phase="substitute"),
    box("Subtract the left edge value from the right edge value to get the IQR.", 13, "Q3 minus Q1."),
    box("Check: the whisker ends mark the coolest and warmest days, 12 and 40. What is the full range?", 28,
        "Largest minus smallest.",
        done="The IQR must come out well below the range, because the box covers only the middle half of the days."),
]

S[5]["display"] = ("Rainfall data (mm) for two regions. Region X: Q1 = 45, Q3 = 82. "
                   "Region Y: Q1 = 60, Q3 = 71. Which region has more consistent rainfall?")
S[5]["hint"] = "Work out both IQRs, then remember that consistent means tightly clustered."
S[5]["misconceptions"] = [
    mis("larger_means_consistent",
        "The region with the wider middle half has been chosen. A wider spread means the totals disagree with each other more, not less.",
        0),
    mis("thought_insufficient",
        "A pair of quartiles is all you need to compare spreads, so more data is not required.",
        3),
]
S[5]["guided_steps"] = [
    say("Both regions give their quartiles, so work out both IQRs and compare them."),
    box("Read Region X's upper quartile from the question.", 82, "Q3 is the larger of the two values for Region X."),
    box("Subtract Region X's lower quartile from it to get Region X's IQR.", 37, "Q3 minus Q1 for Region X.",
        phase="substitute"),
    box("Now do the same for Region Y.", 11, "Q3 minus Q1 for Region Y."),
    box("How much smaller is Region Y's IQR than Region X's?", 26, "Subtract the smaller IQR from the larger.",
        done="The narrower middle half means those rainfall totals sit closer together, and closer together is what consistent means."),
    say("So the option to choose is <strong>Region Y</strong>."),
]

S[6]["hint"] = "Ten values split into two halves of five, so each quartile is a single middle score."
S[6]["misconceptions"] = [
    mis("range_not_iqr",
        "That is the best score minus the worst, the full range. The IQR leaves both extremes out.",
        14),
    mis("stopped_at_q3",
        "That is the upper quartile on its own. The question asks for the gap between the two quartiles.",
        15),
]
S[6]["guided_steps"] = [
    say("Ten values split into two halves of five, with no middle value left over."),
    box("How many sites are listed?", 10, "Count them."),
    box("How many scores are in each half?", 5, "Split the list straight down the middle."),
    box("Give the middle score of the lower five. This is Q1.", 7,
        "Five scores means the middle one is the third.", phase="substitute"),
    box("Give the middle score of the upper five. This is Q3.", 15, "Same move on the top five scores."),
    box("Subtract Q1 from Q3 to get the IQR, then check it comes out below the full range of 14.", 8,
        "Q3 minus Q1.",
        done="Leaving out the best and worst sites always makes the IQR smaller than the range."),
]

# ---- gold --------------------------------------------------------------------
G[0]["hint"] = "Work out the width of each shaded box separately, then compare the two widths."
G[0]["misconceptions"] = [
    mis("compared_medians",
        "The lines inside the boxes have been compared. Those are medians, which say where the middle sits, not how spread out the widths are.",
        0.4),
    mis("compared_ranges",
        "That compares whisker to whisker, the full ranges. The question is about the interquartile ranges, the shaded boxes only.",
        1.5),
    mis("one_iqr_only",
        "That is one river's interquartile range on its own. The question asks by how much one exceeds the other.",
        2.1),
]
G[0]["guided_steps"] = [
    say("Two box plots share one scale. The shaded box runs from Q1 to Q3, so its width is the IQR."),
    box("Find the row labelled River Exe. Reading down to the scale, what value does the left edge of its box sit on, in metres?",
        1.5, "The left edge of the box is the lower quartile.",
        done="Settle which plot you are reading before taking any value off the scale."),
    box("What value does the right edge of the River Exe box sit on?", 3.6,
        "The right edge of the box is the upper quartile."),
    box("Subtract to get the River Exe interquartile range, in metres.", 2.1, "Q3 minus Q1 for the Exe.",
        phase="substitute"),
    box("Now do the same for the River Dart box: right edge minus left edge.", 1.2, "Q3 minus Q1 for the Dart."),
    box("Subtract the smaller interquartile range from the larger one.", 0.9,
        "Take the Dart value away from the Exe value.",
        done="The Exe box is visibly wider on the chart, so a small positive difference is exactly what the picture shows."),
]

G[1]["hint"] = "Split the twelve values into two halves of six, then average the middle pair of the upper half."
G[1]["misconceptions"] = [
    mis("picked_value",
        "With six values in the upper half there is no single middle one, so a value copied straight from the list cannot be the quartile.",
        0.8),
    mis("gave_median",
        "That is the median of the whole set. Q3 comes from the upper half only.",
        0.66),
]
G[1]["guided_steps"] = [
    say("Twelve values split into two halves of six, with nothing left over."),
    box("How many HDI values are listed?", 12, "Count them."),
    box("How many values are in the upper half?", 6, "Split the list straight down the middle."),
    box("Within that upper half of six, add the 3rd and 4th values.", 1.65,
        "The upper half starts at the 7th value of the whole list.", phase="substitute"),
    box("Halve that total to get Q3.", 0.825, "Divide by 2."),
    box("Check: how many of the twelve values are larger than Q3?", 3, "Count the values above it.",
        done="Three of twelve, a quarter of the data, sit above Q3, which is exactly what an upper quartile should leave above it."),
]

G[2]["hint"] = "Leave the median out, then build each quartile from the six values on its own side."
G[2]["misconceptions"] = [
    mis("range_not_iqr",
        "That is the most alkaline minus the most acidic, the full range. The IQR ignores both ends.",
        3.2),
    mis("included_median",
        "The median has been counted into both halves, giving seven values in each and pulling both quartiles towards the centre.",
        1.4),
]
G[2]["guided_steps"] = [
    say("Thirteen values: one median, then six values in each half."),
    box("How many sample points are listed?", 13, "Count them."),
    box("Which position holds the median?", 7, "Add 1 to the count and halve it.",
        done="The value at position 7 belongs to neither half."),
    box("In the lower six, add the 3rd and 4th values and halve the total. This is Q1.", 4.95,
        "The lower half is the six values before position 7.", phase="substitute"),
    box("Do the same in the upper six to get Q3.", 6.65, "The upper half is the six values after position 7."),
    box("Subtract Q1 from Q3 to get the IQR, then check it comes out below the full range of 3.2.", 1.7,
        "Q3 minus Q1.",
        done="Ignoring the most acidic and most alkaline points must leave the IQR below the range."),
]

G[3]["hint"] = "Build Q1 and Q3 first, then the IQR, and only then apply the 1.5 × IQR rule."
G[3]["misconceptions"] = [
    mis("forgot_1_5",
        "The interquartile range has been added to Q3 without multiplying it by 1.5 first.",
        20),
    mis("gave_iqr",
        "That is the interquartile range on its own. The boundary sits above Q3, not at the width of the box.",
        8.5),
    mis("multiplier_only",
        "That is 1.5 × IQR by itself. The rule adds that amount on top of Q3.",
        12.75),
]
G[3]["guided_steps"] = [
    say("The boundary needs Q3 and the IQR, so build both before using the rule."),
    box("How many national parks are listed?", 9, "Count them."),
    box("Which position holds the median?", 5, "Add 1 to the count and halve it."),
    box("Average the two middle values of the lower four to get Q1.", 3,
        "The lower half is the four values before position 5.", phase="substitute"),
    box("Average the two middle values of the upper four to get Q3.", 11.5,
        "The upper half is the four values after position 5."),
    box("Subtract Q1 from Q3 to get the IQR.", 8.5, "Q3 minus Q1."),
    box("Multiply the IQR by 1.5.", 12.75, "IQR × 1.5."),
    box("Add that to Q3 to get the boundary, then compare it with the largest value of 15.8.", 24.25,
        "Q3 plus 1.5 × IQR.",
        done="The largest visitor figure sits well below the boundary, so it is not an outlier."),
]

G[4]["hint"] = "Subtracting a negative lower quartile adds, so build the IQR carefully before comparing."
G[4]["misconceptions"] = [
    mis("forgot_negative",
        "The lower quartile is negative, and subtracting a negative adds. Treating it as positive makes the interquartile range too small.",
        39.7),
    mis("inverted_ratio",
        "The two values have been divided the wrong way round. The question asks what share of the IQR the median is.",
        316),
    mis("range_not_iqr",
        "That uses the full range, largest minus smallest, instead of the gap between the quartiles.",
        15.2),
]
G[4]["guided_steps"] = [
    say("Work out the median and the IQR first, then compare them as a percentage."),
    box("How many countries are listed?", 11, "Count them."),
    box("Which position holds the median?", 6, "Add 1 to the count and halve it."),
    box("Give the median value, in thousands.", 25, "Read the value at position 6.", phase="substitute"),
    box("The lower half is the five values below the median. Give its middle value. This is Q1.", -8,
        "Five values means the middle one is the third. Keep its sign."),
    box("Give the middle value of the upper five. This is Q3.", 71, "Take the third of the top five."),
    box("Subtract Q1 from Q3 to get the IQR. Subtracting a negative adds.", 79, "Q3 minus Q1."),
    box("Divide the median by the IQR, multiply by 100, and round to 1 decimal place.", 31.6,
        "Median ÷ IQR × 100.",
        done="The median is under half the IQR, which fits a data set where the middle half is wide compared with where the middle value sits."),
]

# ---------------------------------------------------------------- assemble
pb["bronze_description"] = "Ordered data, odd numbers of values: find the median, then Q1, Q3, the range and the IQR."
pb["silver_description"] = "Even data sets and unsorted data: reorder first, split into equal halves and average the middle pair."
pb["gold_description"] = "Read quartiles from box plots and use the IQR to compare spreads, test outliers and build further calculations."

out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": pb,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
    "tier_guides": tier_guides,
    "guided": guided,
}

# strip any legacy check keys just in case
for tier in ("bronze", "silver", "gold"):
    for p in pb[tier]:
        for m in p.get("misconceptions") or []:
            m.pop("check", None)

path = os.path.join(HERE, "lesson_L06.json")
with io.open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote", path, os.path.getsize(path))
