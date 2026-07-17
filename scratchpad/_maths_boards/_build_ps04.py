# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion for maths-aqa probability-statistics-L04
(Averages & Spread). Loads live, repairs bank, adds guided/teach/opener/tier_guides/
guided_steps/hints, adds SVG table figures, slims method_card, writes shard."""
import json, io, os

SRC = "_live_ps04.json"
OUT = "lesson_maths-aqa_probability-statistics-L04.json"
live = json.load(io.open(SRC, encoding="utf-8"))

# ---------- SVG helpers ----------
def table_svg(header, rows, aria):
    c1, c2, rh = 96, 66, 22
    W, n = c1 + c2, len(rows)
    H = rh * (n + 1)
    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:200px">' % (W + 2, H + 2, aria)]
    # header background
    parts.append('<rect x="1" y="1" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.15"/>' % (W, rh))
    # outer box
    parts.append('<rect x="1" y="1" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.2"/>' % (W, H))
    # vertical divider
    parts.append('<line x1="%d" y1="1" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (1 + c1, 1 + c1, 1 + H))
    # horizontal lines
    for i in range(1, n + 1):
        y = 1 + rh * i
        parts.append('<line x1="1" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (y, 1 + W, y))
    def cell(x, y, w, txt, bold=False):
        wt = ' font-weight="600"' if bold else ''
        return '<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle"%s>%s</text>' % (x + w / 2, y + rh / 2, wt, txt)
    # header row
    parts.append(cell(1, 1, c1, header[0], True))
    parts.append(cell(1 + c1, 1, c2, header[1], True))
    for i, (a, b) in enumerate(rows):
        y = 1 + rh * (i + 1)
        parts.append(cell(1, y, c1, str(a)))
        parts.append(cell(1 + c1, y, c2, str(b)))
    parts.append('</svg>')
    return "".join(parts)

def money_svg():
    # three bars for £4, £6, £8
    base = 100
    data = [("Sam", 4), ("Kim", 6), ("Jo", 8)]
    xs = [24, 88, 152]
    w = 40
    parts = ['<svg viewBox="0 0 210 128" role="img" aria-label="Three money amounts: Sam has 4 pounds, Kim has 6 pounds, Jo has 8 pounds" style="max-width:220px">']
    for (name, val), x in zip(data, xs):
        h = val * 9
        y = base - h
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#34d399" fill-opacity="0.35" stroke="currentColor" stroke-width="1.2" rx="3"/>' % (x, y, w, h))
        parts.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="12" fill="currentColor" text-anchor="middle">£%d</text>' % (x + w / 2, y - 5, val))
        parts.append('<text x="%d" y="118" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (x + w / 2, name))
    parts.append('<line x1="10" y1="100" x2="200" y2="100" stroke="currentColor" stroke-width="1"/>')
    parts.append('</svg>')
    return "".join(parts)

# ---------- method_card (slim) ----------
method_card = {
    "title": "Averages & Spread",
    "steps": [
        "Mean: add all values, divide by how many.",
        "Median: order the list, take the middle. Mode: the most frequent value.",
        "Frequency table: mean = Σfx ÷ Σf. Grouped: use midpoints (an estimate).",
        "Range = largest − smallest (a measure of spread)."
    ],
    "content": "<p><strong>Mean</strong> = sum ÷ count. <strong>Median</strong> = middle value when ordered. <strong>Mode</strong> = most frequent. <strong>Range</strong> = largest − smallest.</p><p><strong>Frequency table:</strong> mean = \\(\\frac{\\sum fx}{\\sum f}\\). <strong>Grouped data:</strong> use class midpoints, so the mean is an <strong>estimate</strong>; the <strong>modal class</strong> has the highest frequency and the <strong>median class</strong> holds the \\(\\frac{n}{2}\\)th value.</p>",
    "example": "<p><strong>Find the mean of 3, 7, 5, 9, 6.</strong></p><p>Mean = (3+7+5+9+6) ÷ 5 = 30 ÷ 5 = 6</p>"
}

# ---------- descriptions ----------
bronze_desc = "One list of numbers: find its mean, median, mode or range."
silver_desc = "Averages from frequency tables and grouped data, plus reverse mean problems."
gold_desc = "Estimated means, combined or transformed data sets, and a missing frequency."

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: one list of numbers",
        "steps": [
            "<strong>Mean</strong>: add every value, then divide by how many there are. <strong>Median</strong>: order the values and take the middle (average the middle two if there is an even number).",
            "<strong>Mode</strong>: the value that appears most often. <strong>Range</strong>: largest value minus smallest value, a measure of spread.",
            "Always order the list before finding the median. The mean uses every value, so one very large number pulls it upward."
        ],
        "example": {
            "question": "Find the median of 8, 3, 11, 6, 5.",
            "steps": [
                {"label": "Order", "content": "<p>3, 5, 6, 8, 11</p>"},
                {"label": "Middle", "content": "<p>5 values, so the middle is the 3rd: 6</p>"},
                {"label": "Answer", "content": "<p>Median = 6</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: tables and reverse problems",
        "steps": [
            "<strong>Mean from a frequency table</strong>: add an fx column (value × frequency), total it, then divide by the total frequency Σf.",
            "<strong>Grouped data</strong>: use the midpoint of each class as the value, so the mean is an estimate. The <strong>modal class</strong> has the highest frequency.",
            "<strong>Reverse mean</strong>: turn a mean back into a total using total = mean × count, then work with the totals."
        ],
        "example": {
            "question": "Score 1 (f=2), 2 (f=3), 3 (f=5). Find the mean.",
            "steps": [
                {"label": "fx column", "content": "<p>1×2=2, 2×3=6, 3×5=15</p>"},
                {"label": "Totals", "content": "<p>Σfx = 23, Σf = 10</p>"},
                {"label": "Mean", "content": "<p>23 ÷ 10 = 2.3</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: estimates, changes and missing values",
        "steps": [
            "<strong>Estimated mean</strong> from grouped data: Σ(f × midpoint) ÷ Σf, and state that it is an estimate.",
            "<strong>Changing every value</strong>: adding k shifts the mean by k but leaves the range unchanged; multiplying by k scales both the mean and the range by k.",
            "<strong>Missing frequency</strong>: write Σfx and Σf using the unknown, set the mean equal to the given value, then solve."
        ],
        "example": {
            "question": "Mean of 6 numbers is 5. A 7th number, 12, is added. Find the new mean.",
            "steps": [
                {"label": "Old total", "content": "<p>6 × 5 = 30</p>"},
                {"label": "New total", "content": "<p>30 + 12 = 42</p>"},
                {"label": "New mean", "content": "<p>42 ÷ 7 = 6</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------- guided (opener + teach) ----------
guided = {
    "opener": {
        "label": "Before any formula",
        "steps": [
            {"say": "Three friends empty their pockets and pool their money to share it out equally."},
            {"pre": "Sam £4, Kim £6, Jo £8. Pool it all: 4 + 6 + 8 = £", "post": "", "answer": 18,
             "hint": "Add the three amounts.", "display": money_svg()},
            {"pre": "Now share the £18 equally between the 3 friends: 18 ÷ 3 = £", "post": "", "answer": 6,
             "hint": "Split it three ways."},
            {"say": "That shared-out figure, £6, is the <strong>mean</strong>. Every mean is just this: pool everything, then share it equally, so mean = total ÷ how many. Median and mode are two other kinds of 'middle' you will meet in a moment."}
        ]
    },
    "teach": {
        "bronze": {
            "display": "Five test marks: 7, 2, 9, 4, 6. Find the mean, then the median.",
            "label": "Together: your first one",
            "steps": [
                {"say": "Mean first: pool all the marks, then share equally.",
                 "pre": "7 + 2 + 9 + 4 + 6 = ", "post": "", "answer": 28, "hint": "Add the five marks."},
                {"pre": "Divide by how many marks: 28 ÷ 5 = ", "post": "", "answer": 5.6,
                 "hint": "28 shared between 5."},
                {"say": "Now the median. Put them in order: 2, 4, 6, 7, 9.",
                 "pre": "5 values, so the middle is position (5+1) ÷ 2 = ", "post": "", "answer": 3,
                 "hint": "(5+1)÷2."},
                {"pre": "The 3rd value in 2, 4, 6, 7, 9 is ", "post": "", "answer": 6,
                 "hint": "Count to the third.",
                 "done": "Median 6, mean 5.6. Both are 'averages', found in different ways."}
            ]
        },
        "silver": {
            "display": "A frequency table: value 2 (f=4), value 3 (f=6), value 5 (f=10). Find the mean.",
            "label": "Together: a frequency table",
            "steps": [
                {"say": "Add an fx column: multiply each value by its frequency.",
                 "pre": "Row 1: 2 × 4 = ", "post": "", "answer": 8, "hint": "Value times frequency."},
                {"pre": "Row 2: 3 × 6 = ", "post": "", "answer": 18, "hint": "Value times frequency."},
                {"pre": "Row 3: 5 × 10 = ", "post": "", "answer": 50, "hint": "Value times frequency."},
                {"say": "Total the fx column, then the frequency column.",
                 "pre": "Σfx = 8 + 18 + 50 = ", "post": "", "answer": 76, "hint": "Add the fx values."},
                {"pre": "Σf = 4 + 6 + 10 = ", "post": "", "answer": 20, "hint": "Add the frequencies."},
                {"pre": "Mean = 76 ÷ 20 = ", "post": "", "answer": 3.8,
                 "hint": "Divide Σfx by Σf.",
                 "done": "Not (2+3+5)÷3. The frequencies weight each value."}
            ]
        },
        "gold": {
            "display": "Grouped data: 0-10 (f=2), 10-20 (f=5), 20-30 (f=3). Estimate the mean.",
            "label": "Together: estimate from grouped data",
            "steps": [
                {"say": "You do not have exact values, so use each class midpoint.",
                 "pre": "Midpoint of 0-10 = (0+10) ÷ 2 = ", "post": "", "answer": 5, "hint": "Halfway across the class."},
                {"pre": "Midpoint of 10-20 = ", "post": "", "answer": 15, "hint": "Halfway between 10 and 20."},
                {"pre": "Midpoint of 20-30 = ", "post": "", "answer": 25, "hint": "Halfway between 20 and 30."},
                {"say": "Now f × midpoint for each class, and add.",
                 "pre": "2×5 + 5×15 + 3×25 = 10 + 75 + 75 = ", "post": "", "answer": 160,
                 "hint": "Add the three products."},
                {"pre": "Total frequency: 2 + 5 + 3 = ", "post": "", "answer": 10, "hint": "Add the frequencies."},
                {"pre": "Estimated mean = 160 ÷ 10 = ", "post": "", "answer": 16,
                 "hint": "Divide by the total frequency.",
                 "done": "It is an estimate because we used midpoints, not the real values."}
            ]
        }
    }
}

# ---------- problem bank (repaired + guided_steps + figures) ----------
bronze = [
    {  # b0 mean 7
        "display": "Find the mean of 4, 8, 6, 10, 7.",
        "solutions": [7], "calculator": False, "input_type": "single_value",
        "hint": "Add all five numbers, then divide by 5.",
        "misconceptions": [
            {"pattern": "gave_total", "check": "gave_total", "expect": 35,
             "message": "35 is the total, not the mean. Share it out: 35 ÷ 5 = 7."}
        ],
        "guided_steps": [
            {"pre": "Add all five values: 4 + 8 + 6 + 10 + 7 = ", "post": "", "answer": 35, "hint": "Add the five numbers."},
            {"say": "Now share that total equally between the numbers.", "phase": "substitute",
             "pre": "How many numbers are there? ", "post": "", "answer": 5, "hint": "Count them."},
            {"phase": "substitute", "pre": "Mean = 35 ÷ 5 = ", "post": "", "answer": 7,
             "hint": "Divide the total by 5.", "done": "The mean is 7."},
            {"pre": "Check: 7 × 5 = ", "post": "", "answer": 35, "hint": "Multiply back.",
             "done": "It matches the total 35, so 7 is right."}
        ]
    },
    {  # b1 median 5
        "display": "Find the median of 3, 9, 1, 7, 5.",
        "solutions": [5], "calculator": False, "input_type": "single_value",
        "hint": "Put them in order first, then take the middle one.",
        "misconceptions": [
            {"pattern": "no_order", "check": "no_order", "expect": 1,
             "message": "Order the list first. The middle of the unordered list is 1, but ordered (1, 3, 5, 7, 9) the middle is 5."}
        ],
        "guided_steps": [
            {"say": "The median is the middle value, but only once the list is ordered. Ordered: 1, 3, 5, 7, 9.",
             "pre": "How many values are in the list? ", "post": "", "answer": 5, "hint": "Count them."},
            {"phase": "substitute", "pre": "Middle position = (5 + 1) ÷ 2 = ", "post": "", "answer": 3, "hint": "(5+1)÷2."},
            {"phase": "substitute", "pre": "The 3rd value in 1, 3, 5, 7, 9 is ", "post": "", "answer": 5,
             "hint": "Count to the third.", "done": "Median is 5."},
            {"pre": "Check: values below 5 are 1 and 3, that is ", "post": "", "answer": 2,
             "hint": "Count them.", "done": "Two below and two above, so 5 is the middle."}
        ]
    },
    {  # b2 mode 2 (was mode=5 duplicate -> changed)
        "display": "Find the mode of 7, 2, 8, 2, 5, 2, 9.",
        "solutions": [2], "calculator": False, "input_type": "single_value",
        "hint": "The mode is the value that appears most often.",
        "misconceptions": [
            {"pattern": "found_median", "check": "found_median", "expect": 5,
             "message": "That is the median (the middle when ordered). The mode is the most frequent value, which is 2 (it appears 3 times)."}
        ],
        "guided_steps": [
            {"say": "The mode is the value that appears most often. Count how often each value shows up.",
             "pre": "How many times does 2 appear in 7, 2, 8, 2, 5, 2, 9? ", "post": "", "answer": 3, "hint": "Count the 2s."},
            {"say": "Every other value appears just once, so 2 wins.", "phase": "substitute",
             "pre": "The mode is the value that appears 3 times: ", "post": "", "answer": 2,
             "hint": "Which value repeated?", "done": "Mode is 2."},
            {"phase": "substitute", "pre": "How many values appear exactly once (7, 8, 5, 9)? ", "post": "", "answer": 4,
             "hint": "Count them.", "done": "Four singles and one triple, so the mode is 2."}
        ]
    },
    {  # b3 range 19
        "display": "Find the range of 14, 3, 8, 22, 11.",
        "solutions": [19], "calculator": False, "input_type": "single_value",
        "hint": "Range is the largest value take away the smallest.",
        "misconceptions": [
            {"pattern": "gave_max", "check": "gave_max", "expect": 22,
             "message": "22 is the largest value, not the range. Range = largest − smallest = 22 − 3 = 19."}
        ],
        "guided_steps": [
            {"say": "Range measures spread: the gap between the biggest and smallest values.",
             "pre": "Largest value in 14, 3, 8, 22, 11 is ", "post": "", "answer": 22, "hint": "Pick the biggest."},
            {"phase": "substitute", "pre": "Smallest value is ", "post": "", "answer": 3, "hint": "Pick the smallest."},
            {"phase": "substitute", "pre": "Range = 22 − 3 = ", "post": "", "answer": 19,
             "hint": "Largest minus smallest.", "done": "Range is 19."}
        ]
    },
    {  # b4 total 40
        "display": "The mean of 5 numbers is 8. Find the total.",
        "solutions": [40], "calculator": False, "input_type": "single_value",
        "hint": "Total = mean × how many numbers there are.",
        "misconceptions": [
            {"pattern": "added", "check": "added", "expect": 13,
             "message": "Do not add the two numbers. Total = mean × count = 8 × 5 = 40."}
        ],
        "guided_steps": [
            {"say": "The mean is the total shared equally, so total = mean × count.",
             "pre": "The mean is 8 and there are 5 numbers. Count = ", "post": "", "answer": 5, "hint": "How many numbers?"},
            {"phase": "substitute", "pre": "Total = mean × count = 8 × 5 = ", "post": "", "answer": 40,
             "hint": "Multiply mean by count.", "done": "Total is 40."},
            {"phase": "substitute", "pre": "Check: 40 shared between 5 gives 40 ÷ 5 = ", "post": "", "answer": 8,
             "hint": "Divide back.", "done": "It gives the mean 8, so 40 is right."}
        ]
    },
    {  # b5 median 8 (was 6,2,9,4,7,1 median=5 duplicate -> changed)
        "display": "Find the median of 10, 4, 15, 7, 9, 3.",
        "solutions": [8], "calculator": False, "input_type": "single_value",
        "hint": "Order them first, then average the middle two.",
        "misconceptions": [
            {"pattern": "no_order", "check": "no_order", "expect": 11,
             "message": "Order the list first. Averaging the two middle values of the unordered list gives 11, but ordered (3, 4, 7, 9, 10, 15) the middle two are 7 and 9, mean 8."}
        ],
        "guided_steps": [
            {"say": "Six values, an even amount, so the median is the average of the middle two. Ordered: 3, 4, 7, 9, 10, 15.",
             "pre": "How many values? ", "post": "", "answer": 6, "hint": "Count them."},
            {"say": "With 6 values the middle two are the 3rd and 4th.", "phase": "substitute",
             "pre": "The 3rd and 4th values are 7 and ", "post": "", "answer": 9, "hint": "Read the 4th value."},
            {"phase": "substitute", "pre": "Median = (7 + 9) ÷ 2 = ", "post": "", "answer": 8,
             "hint": "Average the middle two.", "done": "Median is 8."}
        ]
    },
    {  # b6 mean 18
        "display": "Find the mean of 12, 15, 18, 21, 24.",
        "solutions": [18], "calculator": False, "input_type": "single_value",
        "hint": "Add all five, then divide by 5.",
        "misconceptions": [
            {"pattern": "gave_total", "check": "gave_total", "expect": 90,
             "message": "90 is the total. The mean divides that by 5: 90 ÷ 5 = 18."}
        ],
        "guided_steps": [
            {"pre": "Add all five: 12 + 15 + 18 + 21 + 24 = ", "post": "", "answer": 90, "hint": "Add them up."},
            {"say": "Now share the total equally.", "phase": "substitute",
             "pre": "How many numbers? ", "post": "", "answer": 5, "hint": "Count them."},
            {"phase": "substitute", "pre": "Mean = 90 ÷ 5 = ", "post": "", "answer": 18,
             "hint": "Divide the total by 5.", "done": "Mean is 18."}
        ]
    },
    {  # b7 mode 60
        "display": "Seven students scored: 50, 60, 60, 65, 70, 75, 80. What is the mode?",
        "solutions": [60], "calculator": False, "input_type": "single_value",
        "hint": "The mode is the score that appears most often.",
        "misconceptions": [
            {"pattern": "found_median", "check": "found_median", "expect": 65,
             "message": "That is the median (the 4th of the seven ordered scores). The mode is the most frequent value, which is 60."}
        ],
        "guided_steps": [
            {"say": "The mode is the most common value. Scan for any score that repeats.",
             "pre": "How many times does 60 appear? ", "post": "", "answer": 2, "hint": "Count the 60s."},
            {"say": "Every other score appears once, so 60 is the mode.", "phase": "substitute",
             "pre": "The mode is ", "post": "", "answer": 60, "hint": "The repeated score.", "done": "Mode is 60."},
            {"phase": "substitute", "pre": "Careful: the median (4th of the 7 ordered scores) is a different value: ",
             "post": "", "answer": 65, "hint": "Count to the 4th score.",
             "done": "Median 65 is not what mode asks for. Mode is 60."}
        ]
    }
]

silver = [
    {  # s0 mean 2.65 (freq table figure)
        "display": table_svg(["Score", "Frequency"], [(1, 3), (2, 5), (3, 8), (4, 4)],
                             "Frequency table: score 1 has frequency 3, score 2 has frequency 5, score 3 has frequency 8, score 4 has frequency 4")
                   + " The frequency table shows a set of scores. Find the mean.",
        "solutions": [2.65], "calculator": True, "input_type": "single_value",
        "hint": "Work out score × frequency for each row, add them, then divide by the total frequency.",
        "misconceptions": [
            {"pattern": "ignored_frequency", "check": "ignored_frequency", "expect": 2.5,
             "message": "Averaging the scores 1, 2, 3, 4 gives 2.5, but each score must be weighted by its frequency: 53 ÷ 20 = 2.65."}
        ],
        "guided_steps": [
            {"say": "Add an fx column: score × frequency for each row.",
             "pre": "Row 1: 1 × 3 = ", "post": "", "answer": 3, "hint": "Score × frequency."},
            {"pre": "Row 2: 2 × 5 = ", "post": "", "answer": 10, "hint": "Score × frequency."},
            {"pre": "Row 3: 3 × 8 = ", "post": "", "answer": 24, "hint": "Score × frequency."},
            {"pre": "Row 4: 4 × 4 = ", "post": "", "answer": 16, "hint": "Score × frequency."},
            {"say": "Total the fx column and the frequency column.", "phase": "substitute",
             "pre": "Σfx = 3 + 10 + 24 + 16 = ", "post": "", "answer": 53, "hint": "Add the fx values."},
            {"phase": "substitute", "pre": "Σf = 3 + 5 + 8 + 4 = ", "post": "", "answer": 20, "hint": "Add the frequencies."},
            {"phase": "substitute", "pre": "Mean = 53 ÷ 20 = ", "post": "", "answer": 2.65,
             "hint": "Divide Σfx by Σf.", "done": "Mean is 2.65."}
        ]
    },
    {  # s1 est mean 16 (grouped figure)
        "display": table_svg(["Class", "Frequency"], [("0-10", 4), ("10-20", 10), ("20-30", 6)],
                             "Grouped frequency table: class 0 to 10 has frequency 4, class 10 to 20 has frequency 10, class 20 to 30 has frequency 6")
                   + " The grouped frequency table shows a set of values. Estimate the mean.",
        "solutions": [16], "calculator": False, "input_type": "single_value",
        "hint": "Use the midpoint of each class, multiply by frequency, add, then divide by 20.",
        "misconceptions": [
            {"pattern": "ignored_frequency", "check": "ignored_frequency", "expect": 15,
             "message": "Averaging the midpoints 5, 15, 25 gives 15, but each midpoint must be weighted by its frequency: 320 ÷ 20 = 16."}
        ],
        "guided_steps": [
            {"say": "You only have classes, so use each class midpoint as the value.",
             "pre": "Midpoint of 0-10 = (0+10) ÷ 2 = ", "post": "", "answer": 5, "hint": "Halfway across."},
            {"pre": "Midpoint of 10-20 = ", "post": "", "answer": 15, "hint": "Halfway between 10 and 20."},
            {"pre": "Midpoint of 20-30 = ", "post": "", "answer": 25, "hint": "Halfway between 20 and 30."},
            {"say": "Now f × midpoint for each class and add.", "phase": "substitute",
             "pre": "4×5 + 10×15 + 6×25 = 20 + 150 + 150 = ", "post": "", "answer": 320, "hint": "Add the three products."},
            {"phase": "substitute", "pre": "Total frequency Σf = 4 + 10 + 6 = ", "post": "", "answer": 20, "hint": "Add the frequencies."},
            {"phase": "substitute", "pre": "Estimated mean = 320 ÷ 20 = ", "post": "", "answer": 16,
             "hint": "Divide by Σf.", "done": "Estimated mean is 16."}
        ]
    },
    {  # s2 fifth number 30
        "display": "The mean of 4 numbers is 15. A fifth number is added and the mean becomes 18. What is the fifth number?",
        "solutions": [30], "calculator": False, "input_type": "single_value",
        "hint": "Find the total of all 5 numbers, then take away the total of the first 4.",
        "misconceptions": [
            {"pattern": "used_new_mean", "check": "used_new_mean", "expect": 18,
             "message": "18 is the new mean, not the fifth number. The fifth number must lift the total from 60 to 90, so it is 90 − 60 = 30."}
        ],
        "guided_steps": [
            {"say": "Turn each mean into a total: total = mean × count.",
             "pre": "Original total of the 4 numbers = 4 × 15 = ", "post": "", "answer": 60, "hint": "Mean × count."},
            {"say": "After adding the fifth number there are 5 numbers with mean 18.", "phase": "substitute",
             "pre": "New total = 5 × 18 = ", "post": "", "answer": 90, "hint": "New mean × new count."},
            {"phase": "substitute", "pre": "Fifth number = new total − old total = 90 − 60 = ", "post": "", "answer": 30,
             "hint": "Subtract the totals.", "done": "The fifth number is 30."}
        ]
    },
    {  # s3 MC modal class (grouped figure)
        "display": table_svg(["Class", "Frequency"], [("0-20", 5), ("20-40", 15), ("40-60", 10)],
                             "Grouped frequency table: class 0 to 20 has frequency 5, class 20 to 40 has frequency 15, class 40 to 60 has frequency 10")
                   + " Which is the modal class?",
        "options": ["20-40", "0-20", "40-60", "Cannot tell"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "The modal class is the one with the highest frequency.",
        "misconceptions": [
            {"pattern": "wrong", "check": "wrong", "expect": None,
             "message": "The modal class has the highest frequency, which is 20-40 (f=15)."}
        ]
    },
    {  # s4 MC median class (grouped figure)
        "display": table_svg(["Class", "Frequency"], [("0-10", 6), ("10-20", 12), ("20-30", 8), ("30-40", 4)],
                             "Grouped frequency table: class 0 to 10 has frequency 6, class 10 to 20 has frequency 12, class 20 to 30 has frequency 8, class 30 to 40 has frequency 4")
                   + " There are 30 values. Find the median class.",
        "options": ["10-20", "20-30", "0-10", "30-40"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "Find the halfway position (n ÷ 2) and track the running totals.",
        "misconceptions": [
            {"pattern": "wrong", "check": "wrong", "expect": None,
             "message": "n ÷ 2 = 15. The running totals are 6, 18, 26, 30, so the 15th value lands in 10-20."}
        ]
    },
    {  # s5 median 5 (freq table figure)
        "display": table_svg(["Score", "Frequency"], [(3, 2), (4, 5), (5, 8), (6, 3), (7, 2)],
                             "Frequency table: score 3 has frequency 2, score 4 has frequency 5, score 5 has frequency 8, score 6 has frequency 3, score 7 has frequency 2")
                   + " The frequency table shows a set of scores. Find the median.",
        "solutions": [5], "calculator": False, "input_type": "single_value",
        "hint": "Build a running total of the frequencies to find where the middle values land.",
        "misconceptions": [
            {"pattern": "found_mean", "check": "found_mean", "expect": 4.9,
             "message": "4.9 is the mean (98 ÷ 20). The median is the middle value: the 10th and 11th both fall in score 5, so the median is 5."}
        ],
        "guided_steps": [
            {"say": "Build a running total (cumulative frequency) to find where the middle values sit.",
             "pre": "There are 20 values in total. Running total after score 3 (f=2) is ", "post": "", "answer": 2, "hint": "Just the first frequency."},
            {"pre": "After score 4 (f=5): 2 + 5 = ", "post": "", "answer": 7, "hint": "Add the next frequency."},
            {"pre": "After score 5 (f=8): 7 + 8 = ", "post": "", "answer": 15, "hint": "Add the next frequency."},
            {"say": "With 20 values the median is the average of the 10th and 11th values.", "phase": "substitute",
             "pre": "Middle position = (20 + 1) ÷ 2 = ", "post": "", "answer": 10.5, "hint": "(20+1)÷2."},
            {"phase": "substitute", "pre": "The 10th and 11th values both fall in the score-5 group (running total goes from 7 to 15). The median is ",
             "post": "", "answer": 5, "hint": "Which score covers positions 8 to 15?", "done": "Median is 5."}
        ]
    },
    {  # s6 MC add value median 6
        "display": "Data set: 2, 5, 5, 7, 8, 12. One more value is added and the median becomes 6. What could the new value be?",
        "options": ["6", "3", "1", "15"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "With 7 values the median is the 4th when ordered; test which option puts 6 there.",
        "misconceptions": [
            {"pattern": "wrong", "check": "wrong", "expect": None,
             "message": "With 7 values the median is the 4th when ordered. Inserting 6 gives 2, 5, 5, 6, 7, 8, 12, whose 4th value is 6."}
        ]
    }
]

gold = [
    {  # g0 est mean 23.3 (grouped figure)
        "display": table_svg(["Class", "Frequency"], [("0-10", 3), ("10-20", 7), ("20-30", 12), ("30-40", 8)],
                             "Grouped frequency table: class 0 to 10 has frequency 3, class 10 to 20 has frequency 7, class 20 to 30 has frequency 12, class 30 to 40 has frequency 8")
                   + " Estimate the mean to 1 d.p.",
        "solutions": [23.3], "calculator": True, "input_type": "single_value",
        "hint": "Use midpoints 5, 15, 25, 35, multiply by frequency, add, then divide by 30.",
        "misconceptions": [
            {"pattern": "used_upper_bounds", "check": "used_upper_bounds", "expect": 28.3,
             "message": "Using the upper class boundaries (10, 20, 30, 40) instead of midpoints gives 28.3. Use midpoints 5, 15, 25, 35: 700 ÷ 30 = 23.3."}
        ],
        "guided_steps": [
            {"say": "Use class midpoints as the values.",
             "pre": "Midpoints are 5, 15, 25, 35. For 0-10: 3 × 5 = ", "post": "", "answer": 15, "hint": "Frequency × midpoint."},
            {"pre": "For 10-20: 7 × 15 = ", "post": "", "answer": 105, "hint": "Frequency × midpoint."},
            {"pre": "For 20-30: 12 × 25 = ", "post": "", "answer": 300, "hint": "Frequency × midpoint."},
            {"pre": "For 30-40: 8 × 35 = ", "post": "", "answer": 280, "hint": "Frequency × midpoint."},
            {"say": "Add them up and divide by the total frequency.", "phase": "substitute",
             "pre": "Σfx = 15 + 105 + 300 + 280 = ", "post": "", "answer": 700, "hint": "Add the four products."},
            {"phase": "substitute", "pre": "Σf = 3 + 7 + 12 + 8 = ", "post": "", "answer": 30, "hint": "Add the frequencies."},
            {"phase": "substitute", "pre": "Estimated mean = 700 ÷ 30 = 23.33..., to 1 d.p. = ", "post": "", "answer": 23.3,
             "hint": "Divide, then round to 1 d.p.", "done": "Estimated mean is 23.3."}
        ]
    },
    {  # g1 last-4 mean 15
        "display": "The mean of a set of 10 numbers is 12. The mean of the first 6 is 10. Find the mean of the last 4.",
        "solutions": [15], "calculator": False, "input_type": "single_value",
        "hint": "Turn each mean into a total first, then work with the totals.",
        "misconceptions": [
            {"pattern": "forgot_to_subtract", "check": "forgot_to_subtract", "expect": 30,
             "message": "Dividing the whole total 120 by 4 gives 30, but the last 4 are only what remains after the first 6: 120 − 60 = 60, then 60 ÷ 4 = 15."}
        ],
        "guided_steps": [
            {"say": "Turn the means into totals first.",
             "pre": "Total of all 10 numbers = 10 × 12 = ", "post": "", "answer": 120, "hint": "Mean × count."},
            {"pre": "Total of the first 6 = 6 × 10 = ", "post": "", "answer": 60, "hint": "Mean × count."},
            {"say": "The last 4 make up the rest of the total.", "phase": "substitute",
             "pre": "Total of the last 4 = 120 − 60 = ", "post": "", "answer": 60, "hint": "Subtract the first-6 total from the whole."},
            {"phase": "substitute", "pre": "Mean of the last 4 = 60 ÷ 4 = ", "post": "", "answer": 15,
             "hint": "Divide by 4.", "done": "Mean of the last 4 is 15."}
        ]
    },
    {  # g2 new range 45
        "display": "A data set has mean 20 and range 15. Each value is multiplied by 3. What is the new range?",
        "solutions": [45], "calculator": False, "input_type": "single_value",
        "hint": "Multiplying every value scales the range by the same amount.",
        "misconceptions": [
            {"pattern": "range_unchanged", "check": "range_unchanged", "expect": 15,
             "message": "The range does change. Multiplying every value by 3 multiplies the range by 3: 3 × 15 = 45."}
        ],
        "guided_steps": [
            {"say": "Multiplying every value by 3 stretches the whole data set, so the spread scales by the same factor.",
             "pre": "Old range is 15. The range is multiplied by the same factor as the values, which is ", "post": "", "answer": 3, "hint": "The scale factor."},
            {"phase": "substitute", "pre": "New range = 3 × 15 = ", "post": "", "answer": 45, "hint": "3 times the old range."},
            {"phase": "substitute", "pre": "Check with sample ends 10 and 25 (range 15): after ×3 they are 30 and 75, so 75 − 30 = ",
             "post": "", "answer": 45, "hint": "75 − 30.", "done": "Same answer 45, so the range triples."}
        ]
    },
    {  # g3 new mean 25
        "display": "A data set has mean 20 and range 15. The value 5 is added to every number. What is the new mean?",
        "solutions": [25], "calculator": False, "input_type": "single_value",
        "hint": "Adding the same number to every value shifts the mean by that number.",
        "misconceptions": [
            {"pattern": "mean_unchanged", "check": "mean_unchanged", "expect": 20,
             "message": "The mean does change. Adding 5 to every value adds 5 to the mean: 20 + 5 = 25."}
        ],
        "guided_steps": [
            {"say": "First, what happens to the spread? Adding the same number to every value moves them all together.",
             "pre": "Adding 5 to every value changes the range by ", "post": "", "answer": 0, "hint": "The gap between values does not change."},
            {"say": "So the range stays 15. Now the mean: every value rose by 5, so their average rises by 5.", "phase": "substitute",
             "pre": "New mean = old mean + 5 = 20 + 5 = ", "post": "", "answer": 25, "hint": "Add 5 to the mean."},
            {"phase": "substitute", "pre": "Check: sample values 15, 20, 25 (mean 20) each gain 5 to give 20, 25, 30, mean = 75 ÷ 3 = ",
             "post": "", "answer": 25, "hint": "Add them and divide by 3.", "done": "Mean rises to 25, exactly the shift of 5."}
        ]
    },
    {  # g4 k=10 (grouped figure with k)
        "display": table_svg(["Class", "Frequency"], [("100-120", 5), ("120-140", 10), ("140-160", "k"), ("160-180", 5)],
                             "Grouped frequency table: class 100 to 120 has frequency 5, class 120 to 140 has frequency 10, class 140 to 160 has frequency k, class 160 to 180 has frequency 5")
                   + " The estimated mean is 140. Find \\(k\\).",
        "solutions": [10], "calculator": True, "input_type": "single_value",
        "hint": "Write Σfx and Σf in terms of k, set the mean to 140, then solve.",
        "misconceptions": [
            {"pattern": "wrong_setup", "check": "wrong_setup", "expect": None,
             "message": "Use midpoints and keep k in both sums: (2700 + 150k) ÷ (20 + k) = 140 gives 10k = 100, so k = 10."}
        ],
        "guided_steps": [
            {"say": "Use midpoints 110, 130, 150, 170. Write Σfx with k in it.",
             "pre": "Known part of Σfx: 5×110 + 10×130 + 5×170 = 550 + 1300 + 850 = ", "post": "", "answer": 2700, "hint": "Add the three known products."},
            {"say": "The class 140-160 has midpoint 150 and frequency k, adding 150k. So Σfx = 2700 + 150k and Σf = 20 + k.",
             "pre": "Total known frequency: 5 + 10 + 5 = ", "post": "", "answer": 20, "hint": "Add the three known frequencies."},
            {"say": "Set the mean to 140: (2700 + 150k) ÷ (20 + k) = 140. Multiply out: 2700 + 150k = 140(20 + k) = 2800 + 140k.", "phase": "substitute",
             "pre": "Collect k terms: 150k − 140k = 2800 − 2700, so 10k = ", "post": "", "answer": 100, "hint": "2800 − 2700."},
            {"phase": "substitute", "pre": "k = 100 ÷ 10 = ", "post": "", "answer": 10, "hint": "Divide by 10.", "done": "k = 10."},
            {"phase": "substitute", "pre": "Check: Σf = 30 and Σfx = 2700 + 1500 = 4200, so mean = 4200 ÷ 30 = ",
             "post": "", "answer": 140, "hint": "Confirm it gives 140.", "done": "Mean is 140, so k = 10 is right."}
        ]
    }
]

# ---------- assemble ----------
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],           # preserved
    "problem_bank": {
        "bronze": bronze, "silver": silver, "gold": gold,
        "bronze_description": bronze_desc,
        "silver_description": silver_desc,
        "gold_description": gold_desc
    },
    "related_videos": live["related_videos"],      # preserved
    "worked_examples": live["worked_examples"],    # preserved
    "tier_guides": tier_guides,
    "guided": guided
}

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
