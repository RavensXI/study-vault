# -*- coding: utf-8 -*-
"""Build guided + diagrams practice_data for maths-ocr probability-statistics-L04 (Averages & Spread)."""
import json, io, statistics

MINUS = "−"   # true minus sign
TIMES = "×"
DIV = "÷"
SIGMA = "Σ"

live = json.load(io.open("_L04_live_fetch.json", encoding="utf-8"))["practice_data"]

# ---------------- SVG frequency-table generator (theme-safe) ----------------
def svg_table(aria, label_w, col_w, rows, h=26):
    ncol = len(rows[0][1])
    W = label_w + ncol * col_w
    Hrows = len(rows) * h
    parts = [f'<svg viewBox="0 0 {W} {Hrows+2}" role="img" aria-label="{aria}" style="max-width:{W}px;height:auto">']
    parts.append(f'<rect x="0" y="0" width="{W}" height="{h}" fill="#60a5fa" fill-opacity="0.15"/>')
    for r in range(len(rows) + 1):
        y = r * h
        parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="currentColor" stroke-opacity="0.4"/>')
    xs = [0] + [label_w + c * col_w for c in range(ncol + 1)]
    for x in xs:
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{Hrows}" stroke="currentColor" stroke-opacity="0.4"/>')
    for r, (lab, cells) in enumerate(rows):
        ty = r * h + h / 2 + 4
        parts.append(f'<text x="{label_w/2:.0f}" y="{ty:.0f}" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">{lab}</text>')
        for c, val in enumerate(cells):
            cx = label_w + c * col_w + col_w / 2
            parts.append(f'<text x="{cx:.0f}" y="{ty:.0f}" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">{val}</text>')
    parts.append('</svg>')
    return ''.join(parts)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayk(text):
    return {"say": text}

# ============================ BRONZE ============================
bronze = [
 {  # B0 mean 2,4,6,8,10 = 6
  "display": "Mean of 2, 4, 6, 8, 10.",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Add all five, then divide by how many there are.",
  "misconceptions": [
    {"pattern": "no_divide", "message": "30 is the total, not the mean. Share it between the 5 values: 30 " + DIV + " 5 = 6.", "expect": 30, "note": "forgot to divide"}],
  "guided_steps": [
    sayk("Mean = total " + DIV + " how many. Find the total first."),
    box("Add them: 2 + 4 + 6 + 8 + 10 = ", 30, "Add left to right."),
    box("How many values are there? ", 5, "Count them."),
    box("Mean = 30 " + DIV + " 5 = ", 6, "Total divided by the count.", phase="substitute"),
    box("Check: 6 " + TIMES + " 5 = ", 30, "Multiply your mean by the count.", done="Mean " + TIMES + " count gives the total back, so 6 is right.")]},
 {  # B1 median 3,5,7,9,11 = 7
  "display": "Median of 3, 5, 7, 9, 11.",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Put them in order (already done) and read the middle one.",
  "misconceptions": [
    {"pattern": "mode_for_median", "message": "The median is the middle value in order, not the most common. With no repeats, look at position, not frequency.", "expect": None, "note": "no determinate wrong value here"}],
  "guided_steps": [
    sayk("Median = the middle value once the list is in order."),
    box("Already in order. How many values? ", 5, "Count them."),
    box("The middle position of 5 values is position ", 3, "(5 + 1) " + DIV + " 2."),
    box("The value in position 3 is ", 7, "Count in: 3, 5, 7.", phase="substitute"),
    box("Check: how many values sit above 7? ", 2, "Count 9 and 11.", done="Two below (3, 5) and two above (9, 11), so 7 is dead centre.")]},
 {  # B2 mode = 3
  "display": "Mode of 2, 3, 3, 5, 7, 3, 8.",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Tally each value; the mode is the one with the biggest tally.",
  "misconceptions": [
    {"pattern": "largest_for_mode", "message": "8 is the largest value, but mode means most frequent, not biggest. 3 appears three times.", "expect": 8, "note": "picks max"}],
  "guided_steps": [
    sayk("Mode = the value that appears most often. Tally each."),
    box("How many times does 3 appear? ", 3, "Count the 3s."),
    box("Does any other value appear more than twice? Enter 0 for no. ", 0, "2, 5, 7 and 8 each appear once."),
    box("So the most frequent value, the mode, is ", 3, "The value with the highest tally.", phase="substitute"),
    box("Check: is 3 one of the listed values? Enter 1 for yes. ", 1, "Yes, 3 is there.", done="3 appears three times, more than any other, so the mode is 3.")]},
 {  # B3 range 4,8,2,15,6 = 13
  "display": "Range of 4, 8, 2, 15, 6.",
  "solutions": [13], "calculator": False, "input_type": "single_value",
  "hint": "Range = largest value minus smallest value.",
  "misconceptions": [
    {"pattern": "add_extremes", "message": "Range is a gap, so subtract: 15 " + MINUS + " 2 = 13. Adding gives 17.", "expect": 17, "note": "adds instead of subtracts"}],
  "guided_steps": [
    sayk("Range = largest " + MINUS + " smallest."),
    box("Largest value: ", 15, "Scan for the biggest."),
    box("Smallest value: ", 2, "Scan for the smallest."),
    box("Range = 15 " + MINUS + " 2 = ", 13, "Subtract smallest from largest.", phase="substitute"),
    box("Check: is 13 smaller than the largest value, 15? Enter 1 for yes. ", 1, "13 < 15, yes.", done="A range is a gap, so it must be less than the biggest value. 13 fits.")]},
 {  # B4 mean 10,20,30 = 20
  "display": "Mean of 10, 20, 30.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Add all three, then divide by 3.",
  "misconceptions": [
    {"pattern": "no_divide", "message": "60 is the total. The mean shares it between the 3 values: 60 " + DIV + " 3 = 20.", "expect": 60, "note": "forgot to divide"}],
  "guided_steps": [
    sayk("Mean = total " + DIV + " how many."),
    box("Add them: 10 + 20 + 30 = ", 60, "Add up."),
    box("How many values? ", 3, "Count."),
    box("Mean = 60 " + DIV + " 3 = ", 20, "Total " + DIV + " count.", phase="substitute"),
    box("Check: 20 " + TIMES + " 3 = ", 60, "Multiply back.", done="Mean " + TIMES + " count returns the total, so 20 is right.")]},
 {  # B5 median even 1..6 = 3.5
  "display": "Median of 1, 2, 3, 4, 5, 6. (Even number of values.)",
  "solutions": [3.5], "calculator": False, "input_type": "single_value",
  "hint": "Even count: average the two middle values.",
  "misconceptions": [
    {"pattern": "single_middle", "message": "With an even count there are two middles (3 and 4); average them for 3.5. Picking 3 alone forgets the pair.", "expect": 3, "note": "takes one middle"}],
  "guided_steps": [
    sayk("Even number of values, so the median is the average of the middle two."),
    box("How many values? ", 6, "Count."),
    box("The two middle values are 3 and 4. Their total: 3 + 4 = ", 7, "Add the middle pair."),
    box("Median = 7 " + DIV + " 2 = ", 3.5, "Halve the total of the middle pair.", phase="substitute"),
    box("Check: is 3.5 between 3 and 4? Enter 1 for yes. ", 1, "Yes, 3.5 is between them.", done="The median sits halfway between the two middle values, so 3.5 is right.")]},
 {  # B6 mean 8, count 5, total = 40
  "display": "Five numbers have mean 8. What is their total?",
  "solutions": [40], "calculator": False, "input_type": "single_value",
  "hint": "Total = mean multiplied by how many.",
  "misconceptions": [
    {"pattern": "divide_not_multiply", "message": "To get the total, multiply: 8 " + TIMES + " 5 = 40. Dividing gives 1.6, smaller than the mean, which cannot be a total.", "expect": 1.6, "note": "divides mean by count"}],
  "guided_steps": [
    sayk("Total = mean " + TIMES + " how many. Reverse the mean formula."),
    box("The mean is ", 8, "It is given."),
    box("How many numbers? ", 5, "Five numbers."),
    box("Total = 8 " + TIMES + " 5 = ", 40, "Mean " + TIMES + " count.", phase="substitute"),
    box("Check: 40 " + DIV + " 5 = ", 8, "Total " + DIV + " count = mean.", done="Dividing the total by 5 returns the mean of 8, so 40 is right.")]},
 {  # B7 range 12,5,8,3,15,7 = 12
  "display": "Range of 12, 5, 8, 3, 15, 7.",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Range = largest value minus smallest value.",
  "misconceptions": [
    {"pattern": "add_extremes", "message": "Range is a gap, so subtract: 15 " + MINUS + " 3 = 12. Adding gives 18.", "expect": 18, "note": "adds instead of subtracts"}],
  "guided_steps": [
    sayk("Range = largest " + MINUS + " smallest."),
    box("Largest value: ", 15, "Biggest."),
    box("Smallest value: ", 3, "Smallest."),
    box("Range = 15 " + MINUS + " 3 = ", 12, "Subtract.", phase="substitute"),
    box("Check: is 12 less than the largest, 15? Enter 1 for yes. ", 1, "12 < 15.", done="The gap must be smaller than the biggest value. 12 fits.")]},
]

# ============================ SILVER ============================
s0_svg = svg_table("Frequency table. Value 1 frequency 4, value 2 frequency 6, value 3 frequency 5, value 4 frequency 5.", 68, 42,
                   [("Value", ["1", "2", "3", "4"]), ("Frequency", ["4", "6", "5", "5"])])
s2_svg = svg_table("Grouped data. Midpoint 5 frequency 8, midpoint 15 frequency 14, midpoint 25 frequency 8.", 72, 44,
                   [("Midpoint", ["5", "15", "25"]), ("Frequency", ["8", "14", "8"])])
s3_svg = svg_table("Grouped frequency table. Class 0-10 frequency 3, 10-20 frequency 7, 20-30 frequency 10, 30-40 frequency 5.", 60, 50,
                   [("Class", ["0-10", "10-20", "20-30", "30-40"]), ("Frequency", ["3", "7", "10", "5"])])
s6_svg = svg_table("Frequency table. Value 0 frequency 2, 1 frequency 5, 2 frequency 8, 3 frequency 3, 4 frequency 2.", 66, 40,
                   [("Value", ["0", "1", "2", "3", "4"]), ("Frequency", ["2", "5", "8", "3", "2"])])

silver = [
 {  # S0 freq mean = 2.55
  "display": s0_svg + "<br>Find the mean.",
  "solutions": [2.55], "calculator": False, "input_type": "single_value",
  "hint": "Mean = " + SIGMA + "fx divided by " + SIGMA + "f (the total frequency).",
  "misconceptions": [
    {"pattern": "divide_by_rows", "message": "Divide by the total frequency (20 people), not the number of rows (4): 51 " + DIV + " 20 = 2.55.", "expect": 12.75, "note": "51/4"},
    {"pattern": "unweighted", "message": "Each value must be weighted by its frequency, not averaged on its own. (1+2+3+4) " + DIV + " 4 = 2.5 ignores how often each occurs.", "expect": 2.5, "note": "mean of the values"}],
  "guided_steps": [
    sayk("For a frequency table, mean = " + SIGMA + "fx " + DIV + " " + SIGMA + "f. Multiply each value by its frequency first."),
    box("1 " + TIMES + " 4 = ", 4, "value " + TIMES + " frequency."),
    box("2 " + TIMES + " 6 = ", 12, "value " + TIMES + " frequency."),
    box("3 " + TIMES + " 5 = ", 15, "value " + TIMES + " frequency."),
    box("4 " + TIMES + " 5 = ", 20, "value " + TIMES + " frequency."),
    box("Add those: 4 + 12 + 15 + 20 = ", 51, "That is " + SIGMA + "fx."),
    box("Total frequency: 4 + 6 + 5 + 5 = ", 20, "That is " + SIGMA + "f, the number of people."),
    box("Mean = 51 " + DIV + " 20 = ", 2.55, SIGMA + "fx " + DIV + " " + SIGMA + "f.", phase="substitute"),
    box("Check: is 2.55 between the smallest value 1 and largest 4? Enter 1 for yes. ", 1, "Yes, between 1 and 4.", done="A mean must lie within the data, and 2.55 does, so it is right.")]},
 {  # S1 new mean = 14
  "display": "The mean of 5 numbers is 12. A 6th number (24) is added. Find the new mean.",
  "solutions": [14], "calculator": False, "input_type": "single_value",
  "hint": "Rebuild the total, add 24, then divide by 6.",
  "misconceptions": [
    {"pattern": "average_of_two", "message": "You cannot average the old mean with the new value. Rebuild the total: (60 + 24) " + DIV + " 6 = 14. (12 + 24) " + DIV + " 2 = 18 is the slip.", "expect": 18, "note": "(12+24)/2"}],
  "guided_steps": [
    sayk("Rebuild the total, add the new number, then divide by the new count."),
    box("Original total = 12 " + TIMES + " 5 = ", 60, "Mean " + TIMES + " count."),
    box("New total = 60 + 24 = ", 84, "Add the 6th number."),
    box("New count = 5 + 1 = ", 6, "One more number."),
    box("New mean = 84 " + DIV + " 6 = ", 14, "New total " + DIV + " new count.", phase="substitute"),
    box("Check: 14 " + TIMES + " 6 = ", 84, "Multiply back.", done="The new mean times the new count returns 84, so 14 is right.")]},
 {  # S2 grouped midpoints mean = 15 (FIXED freqs 8,14,8)
  "display": s2_svg + "<br>Find the estimated mean.",
  "solutions": [15], "calculator": False, "input_type": "single_value",
  "hint": "Estimated mean = " + SIGMA + "(midpoint " + TIMES + " frequency) " + DIV + " " + SIGMA + "f.",
  "misconceptions": [
    {"pattern": "divide_by_groups", "message": "Divide by the total frequency (30), not the number of groups (3): 450 " + DIV + " 30 = 15.", "expect": 150, "note": "450/3"}],
  "guided_steps": [
    sayk("Estimated mean = " + SIGMA + "(midpoint " + TIMES + " frequency) " + DIV + " " + SIGMA + "f."),
    box("5 " + TIMES + " 8 = ", 40, "midpoint " + TIMES + " frequency."),
    box("15 " + TIMES + " 14 = ", 210, "midpoint " + TIMES + " frequency."),
    box("25 " + TIMES + " 8 = ", 200, "midpoint " + TIMES + " frequency."),
    box("Add those: 40 + 210 + 200 = ", 450, "That is " + SIGMA + "fx."),
    box("Total frequency: 8 + 14 + 8 = ", 30, "That is " + SIGMA + "f."),
    box("Mean = 450 " + DIV + " 30 = ", 15, SIGMA + "fx " + DIV + " " + SIGMA + "f.", phase="substitute"),
    box("Check: is 15 between the smallest midpoint 5 and largest 25? Enter 1 for yes. ", 1, "Yes.", done="The estimated mean sits inside the midpoint range, so 15 is right.")]},
 {  # S3 median class MC -> index 0 "20-30"
  "display": s3_svg + "<br>Total = 25. Which class contains the median?",
  "options": ["20-30", "10-20", "30-40", "0-10"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Find the median position (the 13th), then run a cumulative total down the classes.",
  "misconceptions": [
    {"pattern": "stops_early", "message": "Running totals are 3, then 10, then 20. The 13th value is the first past 10, so it lands in 20-30, not 10-20.", "expect": 1, "note": "picks 10-20"}]},
 {  # S4 mode = 8
  "display": "Data: 5, 5, 7, 8, 8, 8, 10. Identify the mode.",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "The mode is the value with the highest tally.",
  "misconceptions": [
    {"pattern": "reports_count", "message": "The mode is the value that repeats most, which is 8, not how many times it repeats (3).", "expect": 3, "note": "reports frequency"},
    {"pattern": "largest_for_mode", "message": "Mode means most frequent, not the biggest. 8 appears three times; 10 only once.", "expect": 10, "note": "picks max"}],
  "guided_steps": [
    sayk("Mode = the value with the highest tally."),
    box("How many times does 8 appear? ", 3, "Count the 8s."),
    box("How many times does 5 appear? ", 2, "Count the 5s."),
    box("The value with the biggest tally is ", 8, "8 beats 5.", phase="substitute"),
    box("Check: does any value appear more than 3 times? Enter 0 for no. ", 0, "No value appears 4 times.", done="Nothing beats three, so the mode is 8.")]},
 {  # S5 fourth number = 20
  "display": "Mean of four numbers is 15. Three are 10, 12, 18. Find the fourth.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Find the required total, then subtract the three you know.",
  "misconceptions": [
    {"pattern": "fourth_is_mean", "message": "The fourth value is not the mean. The four must total 60; take away the 40 you have: 60 " + MINUS + " 40 = 20.", "expect": 15, "note": "guesses the mean"}],
  "guided_steps": [
    sayk("Find the required total, then subtract the three you know."),
    box("Total of all four = 15 " + TIMES + " 4 = ", 60, "Mean " + TIMES + " count."),
    box("Sum of the three known: 10 + 12 + 18 = ", 40, "Add them."),
    box("Fourth number = 60 " + MINUS + " 40 = ", 20, "Required total minus the known part.", phase="substitute"),
    box("Check: new mean = (10 + 12 + 18 + 20) " + DIV + " 4 = ", 15, "Add all four, divide by 4.", done="All four average to 15, so the fourth number is 20.")]},
 {  # S6 freq median = 2
  "display": s6_svg + "<br>Find the median.",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Total the frequencies, find the middle position, then read down the running totals.",
  "misconceptions": [
    {"pattern": "median_of_freqs", "message": "Find the median of the data values, not of the frequencies. The frequencies (2, 5, 8, 3, 2) count how often each value occurs, they are not the values.", "expect": 3, "note": "median of 2,2,3,5,8"}],
  "guided_steps": [
    sayk("Total the frequencies, find the middle position, then read down the running totals."),
    box("Total frequency: 2 + 5 + 8 + 3 + 2 = ", 20, "Add the frequencies."),
    box("With 20 values the median averages the 10th and 11th. Running total after value 1: 2 + 5 = ", 7, "Cumulative frequency."),
    box("Running total after value 2: 7 + 8 = ", 15, "Add the frequency of 2."),
    box("The 10th and 11th values both fall in this block, so the median value is ", 2, "Positions 8 to 15 are all the value 2.", phase="substitute"),
    box("Check: are both the 10th and 11th between positions 8 and 15? Enter 1 for yes. ", 1, "Yes, 10 and 11 are in 8 to 15.", done="Both middle positions land on the value 2, so the median is 2.")]},
]

# ============================ GOLD ============================
g0_svg = svg_table("Grouped frequency table. Class 0-10 frequency 6, 10-20 frequency 15, 20-30 frequency 9.", 60, 52,
                   [("Class", ["0-10", "10-20", "20-30"]), ("Frequency", ["6", "15", "9"])])

gold = [
 {  # G0 grouped mean = 16 (FIXED freqs 6,15,9)
  "display": g0_svg + "<br>Estimate the mean.",
  "solutions": [16], "calculator": False, "input_type": "single_value",
  "hint": "Find each class midpoint, then " + SIGMA + "fx " + DIV + " " + SIGMA + "f.",
  "misconceptions": [
    {"pattern": "divide_by_classes", "message": "Divide by the total frequency (30), not the number of classes (3): 480 " + DIV + " 30 = 16.", "expect": 160, "note": "480/3"},
    {"pattern": "upper_bounds", "message": "Use the midpoint of each class (5, 15, 25), not the top value. Tops give 21, an overestimate.", "expect": 21, "note": "10,20,30 as x"}],
  "guided_steps": [
    sayk("First find each class midpoint, then " + SIGMA + "(midpoint " + TIMES + " frequency) " + DIV + " " + SIGMA + "f."),
    box("Midpoint of 0 to 10: (0 + 10) " + DIV + " 2 = ", 5, "Halfway across the class."),
    box("Midpoints of the other classes are 15 and 25. Now 5 " + TIMES + " 6 = ", 30, "midpoint " + TIMES + " frequency."),
    box("15 " + TIMES + " 15 = ", 225, "midpoint " + TIMES + " frequency."),
    box("25 " + TIMES + " 9 = ", 225, "midpoint " + TIMES + " frequency."),
    box("Add those: 30 + 225 + 225 = ", 480, "That is " + SIGMA + "fx."),
    box("Total frequency: 6 + 15 + 9 = ", 30, "That is " + SIGMA + "f."),
    box("Estimated mean = 480 " + DIV + " 30 = ", 16, SIGMA + "fx " + DIV + " " + SIGMA + "f.", phase="substitute"),
    box("Check: is 16 inside the data, between 0 and 30? Enter 1 for yes. ", 1, "Yes.", done="The estimate lies within the range, so 16 is right.")]},
 {  # G1 find n = 9
  "display": "The mean of n numbers is 20. When 30 is added, the mean becomes 21. Find n.",
  "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "The added value sits above the old mean; that surplus lifts every number by 1.",
  "misconceptions": [
    {"pattern": "forgets_extra_count", "message": "The new mean applies to n+1 numbers, not n. Setting 20n + 30 = 21n forgets the added number and gives n = 30.", "expect": 30, "note": "21n instead of 21(n+1)"}],
  "guided_steps": [
    sayk("Compare totals. The n originals sit exactly at the old mean, so only the new value adds surplus."),
    box("How far is the new value 30 above the old mean of 20? 30 " + MINUS + " 20 = ", 10, "The surplus the new value brings in."),
    box("After adding, every number averages 21, which is 21 " + MINUS + " 20 = ", 1, "How much each number rises above 20."),
    box("That surplus of 10 is shared as +1 across all the numbers, so n + 1 = ", 10, "10 surplus " + DIV + " 1 each = 10 numbers.", phase="substitute"),
    box("So n = 10 " + MINUS + " 1 = ", 9, "Take off the number you added."),
    box("Check: (20 " + TIMES + " 9 + 30) " + DIV + " 10 = ", 21, "Total 210 over 10.", done="Nine numbers plus 30 average 21, so n = 9.")]},
 {  # G2 IQR = 7
  "display": "Interquartile range: data is 2, 3, 5, 7, 8, 10, 12, 15. Find the IQR.",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Split the ordered data into a lower and upper half; IQR = Q3 minus Q1.",
  "misconceptions": [
    {"pattern": "uses_full_range", "message": "The IQR uses the quartiles (11 and 4), not the extremes. 15 " + MINUS + " 2 = 13 is the full range.", "expect": 13, "note": "full range"}],
  "guided_steps": [
    sayk("IQR = upper quartile " + MINUS + " lower quartile. Split the 8 ordered values into halves."),
    box("Lower half is 2, 3, 5, 7. Its median (Q1) = (3 + 5) " + DIV + " 2 = ", 4, "Average the middle two of the lower half."),
    box("Upper half is 8, 10, 12, 15. Its median (Q3) = (10 + 12) " + DIV + " 2 = ", 11, "Average the middle two of the upper half."),
    box("IQR = 11 " + MINUS + " 4 = ", 7, "Q3 minus Q1.", phase="substitute"),
    box("Check: is the IQR less than the full range, 15 " + MINUS + " 2 = 13? Enter 1 for yes. ", 1, "7 < 13, yes.", done="The middle 50% spread (7) is less than the full range (13), so 7 is right.")]},
 {  # G3 combined mean = 71
  "display": "Two groups: Group A mean = 65 (20 students). Group B mean = 75 (30 students). Combined mean?",
  "solutions": [71], "calculator": False, "input_type": "single_value",
  "hint": "Rebuild each group's total, add them, then divide by the total number of students.",
  "misconceptions": [
    {"pattern": "average_of_means", "message": "You cannot just average the two means when the groups differ in size. Weight by totals: 3550 " + DIV + " 50 = 71. (65 + 75) " + DIV + " 2 = 70 ignores that B is bigger.", "expect": 70, "note": "mean of means"}],
  "guided_steps": [
    sayk("Combine by totals, never by averaging the two means. Rebuild each total first."),
    box("Group A total = 65 " + TIMES + " 20 = ", 1300, "Mean " + TIMES + " count."),
    box("Group B total = 75 " + TIMES + " 30 = ", 2250, "Mean " + TIMES + " count."),
    box("Combined total = 1300 + 2250 = ", 3550, "Add the totals."),
    box("Combined count = 20 + 30 = ", 50, "Add the counts."),
    box("Combined mean = 3550 " + DIV + " 50 = ", 71, "Combined total " + DIV + " combined count.", phase="substitute"),
    box("Check: is 71 between 65 and 75, nearer 75 (the bigger group)? Enter 1 for yes. ", 1, "Yes, between and closer to 75.", done="The combined mean leans toward the larger group, so 71 is right.")]},
 {  # G4 outlier yes = 1
  "display": "A dataset has median 15, Q1 = 10, Q3 = 22. A value of 50 is added. Is 50 an outlier using the 1.5 " + TIMES + " IQR rule? Enter 1 for yes.",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "Build the upper fence Q3 + 1.5 " + TIMES + " IQR, then compare 50 to it.",
  "misconceptions": [
    {"pattern": "uses_3iqr", "message": "The standard fence uses 1.5 " + TIMES + " IQR, giving 40, and 50 is past it. Using 3 " + TIMES + " IQR (the extreme test) pushes the fence to 58 and wrongly clears 50.", "expect": 0, "note": "3xIQR fence"}],
  "guided_steps": [
    sayk("An outlier lies beyond a fence set 1.5 IQRs past a quartile. Build the upper fence."),
    box("IQR = Q3 " + MINUS + " Q1 = 22 " + MINUS + " 10 = ", 12, "Upper quartile minus lower."),
    box("1.5 " + TIMES + " IQR = 1.5 " + TIMES + " 12 = ", 18, "Multiply the IQR by 1.5."),
    box("Upper fence = Q3 + 18 = 22 + 18 = ", 40, "Add to the upper quartile."),
    box("Is 50 beyond the fence of 40? Enter 1 for yes, 0 for no: ", 1, "50 > 40.", phase="substitute"),
    box("Check: 50 " + MINUS + " 40 = ", 10, "The gap past the fence.", done="50 sits 10 above the fence, so yes, it is an outlier.")]},
]

# ============================ tier_guides ============================
tier_guides = {
 "bronze": {
   "title": "Bronze: one average from a list",
   "steps": [
     "The <strong>mean</strong> is total " + DIV + " how many. The <strong>median</strong> is the middle value once ordered (average the two middle ones if the count is even).",
     "The <strong>mode</strong> is the value that appears most often. The <strong>range</strong> is largest " + MINUS + " smallest, a measure of spread.",
     "Always order the list before finding a median, and check a mean sits inside the data."],
   "example": {"question": "Find the median of 4, 1, 7, 3, 5",
     "steps": [
       {"label": "Order", "content": "<p>1, 3, 4, 5, 7</p>"},
       {"label": "Middle", "content": "<p>5 values, so the 3rd is the middle: 4.</p>"},
       {"label": "Check", "content": "<p>Two below (1, 3), two above (5, 7).</p>"},
       {"label": "Answer", "content": "<p>Median = 4</p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
   "title": "Silver: tables and grouped data",
   "steps": [
     "For a <strong>frequency table</strong>, mean = " + SIGMA + "fx " + DIV + " " + SIGMA + "f: multiply each value by its frequency, add those, and divide by the total frequency.",
     "For <strong>grouped data</strong>, use the midpoint of each class in place of a value, then do the same " + SIGMA + "fx " + DIV + " " + SIGMA + "f.",
     "For a missing value, rebuild the required total from the mean, then subtract what you know."],
   "example": {"question": "Frequency table: value 2 (f=3), 3 (f=5), 4 (f=2). Find the mean.",
     "steps": [
       {"label": SIGMA + "fx", "content": "<p>2" + TIMES + "3 + 3" + TIMES + "5 + 4" + TIMES + "2 = 6 + 15 + 8 = 29</p>"},
       {"label": SIGMA + "f", "content": "<p>3 + 5 + 2 = 10</p>"},
       {"label": "Divide", "content": "<p>29 " + DIV + " 10 = 2.9</p>"},
       {"label": "Answer", "content": "<p>Mean = 2.9</p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
   "title": "Gold: combining and spread",
   "steps": [
     "To <strong>combine means</strong>, never average the averages: rebuild each group's total (mean " + TIMES + " count), add the totals, and divide by the total count.",
     "For a <strong>grouped mean</strong>, find each midpoint first, then " + SIGMA + "fx " + DIV + " " + SIGMA + "f.",
     "<strong>Quartiles</strong> split ordered data into four. IQR = Q3 " + MINUS + " Q1; a value past Q3 + 1.5 " + TIMES + " IQR is an outlier."],
   "example": {"question": "10 students average 6; 30 students average 10. Combined mean?",
     "steps": [
       {"label": "Totals", "content": "<p>6" + TIMES + "10 = 60 and 10" + TIMES + "30 = 300</p>"},
       {"label": "Combine", "content": "<p>Total 360 over 40 students</p>"},
       {"label": "Divide", "content": "<p>360 " + DIV + " 40 = 9</p>"},
       {"label": "Answer", "content": "<p>Combined mean = 9</p>", "isAnswer": True, "is_answer": True}]}},
}

# ============================ guided (opener + teach) ============================
teach_silver_svg = svg_table("Frequency table. Value 2 frequency 3, value 3 frequency 4, value 4 frequency 3.", 68, 42,
                             [("Value", ["2", "3", "4"]), ("Frequency", ["3", "4", "3"])])
teach_gold_svg = svg_table("Grouped frequency table. Class 0-10 frequency 6, 10-20 frequency 8, 20-30 frequency 6.", 60, 52,
                           [("Class", ["0-10", "10-20", "20-30"]), ("Frequency", ["6", "8", "6"])])

guided = {
 "opener": {
   "label": "Before any formulas",
   "display": "Three friends pool their birthday money:<br>Sam &pound;2, Priya &pound;3, Leo &pound;7.",
   "steps": [
     sayk("No formulas yet, just fair play. They tip all the money into one pot and share it out equally.") | {},
     box("Each friend ends up with &pound;", 4, "Total the money, then split it three ways."),
     box("Now the spread: the most anyone had minus the least, 7 " + MINUS + " 2 = &pound;", 5, "Biggest minus smallest."),
     sayk("The fair share you found first is the <strong>mean</strong>: total " + DIV + " how many, here 12 " + DIV + " 3 = 4. The gap you found second is the <strong>range</strong>, a measure of spread. Averages tell you a typical value; spread tells you how stretched out the data is.")],
 },
 "teach": {
   "bronze": {
     "display": "Find the mean of 3, 8, 4, 9, 6.",
     "label": "Together: your first mean",
     "steps": [
       sayk("Mean = total " + DIV + " how many."),
       box("Add them: 3 + 8 + 4 + 9 + 6 = ", 30, "Add up."),
       box("How many values? ", 5, "Count."),
       box("Mean = 30 " + DIV + " 5 = ", 6, "Total " + DIV + " count.", done="That is the mean."),
       box("Check: 6 " + TIMES + " 5 = ", 30, "Multiply back.", done="Mean " + TIMES + " count returns the total.")]},
   "silver": {
     "display": teach_silver_svg + "<br>Find the mean.",
     "label": "Together: the frequency-table move",
     "steps": [
       sayk("Weight each value by its frequency: " + SIGMA + "fx " + DIV + " " + SIGMA + "f."),
       box("2 " + TIMES + " 3 = ", 6, "value " + TIMES + " frequency."),
       box("3 " + TIMES + " 4 = ", 12, "value " + TIMES + " frequency."),
       box("4 " + TIMES + " 3 = ", 12, "value " + TIMES + " frequency."),
       box(SIGMA + "fx = 6 + 12 + 12 = ", 30, "Add the products."),
       box(SIGMA + "f = 3 + 4 + 3 = ", 10, "Total frequency."),
       box("Mean = 30 " + DIV + " 10 = ", 3, SIGMA + "fx " + DIV + " " + SIGMA + "f.", done="The frequency-weighted mean.")]},
   "gold": {
     "display": teach_gold_svg + "<br>Estimate the mean.",
     "label": "Together: the grouped-data move",
     "steps": [
       sayk("Use the midpoint of each class, then " + SIGMA + "fx " + DIV + " " + SIGMA + "f."),
       box("Midpoint of 0 to 10 = ", 5, "Halfway across the class."),
       box("5 " + TIMES + " 6 = ", 30, "midpoint " + TIMES + " frequency."),
       box("15 " + TIMES + " 8 = ", 120, "midpoint " + TIMES + " frequency."),
       box("25 " + TIMES + " 6 = ", 150, "midpoint " + TIMES + " frequency."),
       box(SIGMA + "fx = 30 + 120 + 150 = ", 300, "Add the products."),
       box(SIGMA + "f = 6 + 8 + 6 = ", 20, "Total frequency."),
       box("Estimated mean = 300 " + DIV + " 20 = ", 15, SIGMA + "fx " + DIV + " " + SIGMA + "f.", done="The estimated mean.")]},
 },
}

# Fix opener step 0 (the |{} was a no-op guard); rebuild cleanly
guided["opener"]["steps"] = [
  sayk("No formulas yet, just fair play. They tip all the money into one pot and share it out equally."),
  box("Each friend ends up with &pound;", 4, "Total the money, then split it three ways."),
  box("Now the spread: the most anyone had minus the least, 7 " + MINUS + " 2 = &pound;", 5, "Biggest minus smallest."),
  sayk("The fair share you found first is the <strong>mean</strong>: total " + DIV + " how many, here 12 " + DIV + " 3 = 4. The gap you found second is the <strong>range</strong>, a measure of spread. Averages tell you a typical value; spread tells you how stretched out the data is."),
]

# ============================ method_card (slim) ============================
method_card = {
 "title": "Averages & Spread",
 "steps": [
   "Mean = total " + DIV + " how many",
   "Median = middle value in order (even count: average the middle two)",
   "Mode = most frequent; Range = largest " + MINUS + " smallest",
   "Frequency or grouped data: mean = " + SIGMA + "fx " + DIV + " " + SIGMA + "f (use midpoints when grouped)"],
 "content": "<p>The <strong>mean</strong> shares the total equally: total " + DIV + " count. The <strong>median</strong> is the middle of the ordered list. The <strong>mode</strong> is the most common value. These describe a typical value.</p><p><strong>Spread</strong>: the range is largest " + MINUS + " smallest; the interquartile range is Q3 " + MINUS + " Q1, the middle half. For a frequency table, mean = " + SIGMA + "fx " + DIV + " " + SIGMA + "f; grouped data uses class midpoints.</p>",
 "example": "<p><strong>Data: 3, 5, 7, 7, 8. Mean?</strong></p><p>(3+5+7+7+8)/5 = 30/5 = 6.</p>",
}

# ============================ assemble ============================
pd = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description": "Read a single average or the range straight from a short list of numbers.",
   "silver_description": "Work with frequency tables, grouped data, and a missing value using totals.",
   "gold_description": "Combine means, estimate from grouped classes, and measure spread with quartiles.",
 },
 "related_videos": live.get("related_videos", []),
 "worked_examples": live.get("worked_examples", []),
 "tier_guides": tier_guides,
 "guided": guided,
}

json.dump(pd, io.open("../_maths_guided/lesson_maths-ocr_probability-statistics-L04.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(pd, io.open("lesson_maths-ocr_probability-statistics-L04.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written. bronze", len(bronze), "silver", len(silver), "gold", len(gold))
