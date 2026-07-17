# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for
maths-eduqas probability-statistics-L04 (Averages & Spread).
Starts from the live row to preserve untouched fields.
"""
import json, io

live = json.load(io.open("_psL04_live.json", encoding="utf-8"))

# ---------- SVG generators (programmatic from numbers) ----------
def svg_table(header, rows, aria):
    """header=(left,right); rows=[(left,right),...]; theme-safe."""
    total = len(rows) + 1
    inner = 22 * total
    vbh = inner + 2
    parts = []
    parts.append(
        '<svg viewBox="0 0 164 %d" role="img" aria-label="%s" style="max-width:200px">' % (vbh, aria))
    parts.append('<rect x="1" y="1" width="162" height="22" fill="#60a5fa" fill-opacity="0.15"/>')
    parts.append('<rect x="1" y="1" width="162" height="%d" fill="none" stroke="currentColor" stroke-width="1.2"/>' % inner)
    parts.append('<line x1="97" y1="1" x2="97" y2="%d" stroke="currentColor" stroke-width="1"/>' % (inner + 1))
    for i in range(1, total):
        y = 1 + 22 * i
        parts.append('<line x1="1" y1="%d" x2="163" y2="%d" stroke="currentColor" stroke-width="1"/>' % (y, y))
    def cell(x, y, text, bold=False):
        w = ' font-weight="600"' if bold else ''
        return ('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" '
                'fill="currentColor" text-anchor="middle" dominant-baseline="middle"%s>%s</text>'
                % (x, y, w, text))
    parts.append(cell(49, 12, header[0], True))
    parts.append(cell(130, 12, header[1], True))
    for i, (lft, rgt) in enumerate(rows):
        y = 12 + 22 * (i + 1)
        parts.append(cell(49, y, str(lft)))
        parts.append(cell(130, y, str(rgt)))
    parts.append('</svg>')
    return "".join(parts)

def aria_freq(rows, grouped=False):
    kind = "Grouped frequency table" if grouped else "Frequency table"
    unit = "class" if grouped else "score"
    bits = []
    for lft, rgt in rows:
        lbl = str(lft).replace("-", " to ") if grouped else str(lft)
        bits.append("%s %s has frequency %s" % (unit, lbl, rgt))
    return kind + ": " + ", ".join(bits)

# opener money bar chart
def svg_money(items):
    # items = [(name, pounds)], bar heights scaled 8px per pound, base y=100
    xs = [24, 88, 152]
    parts = ['<svg viewBox="0 0 210 128" role="img" aria-label="%s" style="max-width:220px">'
             % ("Three money amounts: " + ", ".join("%s has %d pounds" % (n, p) for n, p in items))]
    for (name, p), x in zip(items, xs):
        h = p * 8
        y = 100 - h
        cx = x + 20
        parts.append('<rect x="%d" y="%d" width="40" height="%d" fill="#34d399" fill-opacity="0.35" stroke="currentColor" stroke-width="1.2" rx="3"/>' % (x, y, h))
        parts.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="12" fill="currentColor" text-anchor="middle">£%d</text>' % (cx, y - 5, p))
        parts.append('<text x="%d" y="118" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (cx, name))
    parts.append('<line x1="10" y1="100" x2="200" y2="100" stroke="currentColor" stroke-width="1"/>')
    parts.append('</svg>')
    return "".join(parts)

# ---------- helpers ----------
def box(pre, answer, hint, say=None, post="", done=None, phase=None, display=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if phase:
        d["phase"] = phase
    if done:
        d["done"] = done
    if display:
        d["display"] = display
    return d

def sayonly(say):
    return {"say": say}

def mis(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

# =================== PROBLEM BANK ===================
bronze = []
# B1 mean 6,10,4,8,12 = 8
bronze.append({
    "display": "Find the mean of 6, 10, 4, 8, 12.",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "Add all five numbers, then divide by 5.",
    "misconceptions": [mis("gave_total", 40, "40 is the total, not the mean. Share it out: 40 ÷ 5 = 8.")],
    "guided_steps": [
        box("Add all five values: 6 + 10 + 4 + 8 + 12 = ", 40, "Add the five numbers."),
        box("How many numbers are there? ", 5, "Count them.", say="Now share the total equally.", phase="substitute"),
        box("Mean = 40 ÷ 5 = ", 8, "Divide the total by 5.", phase="substitute", done="The mean is 8."),
        box("Check: 8 × 5 = ", 40, "Multiply back.", done="It matches the total 40, so 8 is right."),
    ]})
# B2 median 7,2,9,4,3 -> 4
bronze.append({
    "display": "Find the median of 7, 2, 9, 4, 3.",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Put them in order first, then take the middle one.",
    "misconceptions": [mis("no_order", 9, "Order the list first. The middle of the unordered list is 9, but ordered (2, 3, 4, 7, 9) the middle is 4.")],
    "guided_steps": [
        box("How many values are in the list? ", 5, "Count them.", say="The median is the middle value, but only once the list is ordered. Ordered: 2, 3, 4, 7, 9."),
        box("Middle position = (5 + 1) ÷ 2 = ", 3, "(5+1)÷2.", phase="substitute"),
        box("The 3rd value in 2, 3, 4, 7, 9 is ", 4, "Count to the third.", phase="substitute", done="Median is 4."),
        box("Check: values below 4 are 2 and 3, that is ", 2, "Count them.", done="Two below and two above, so 4 is the middle."),
    ]})
# B3 mode 3,7,3,9,5,3,8 -> 3
bronze.append({
    "display": "Find the mode of 3, 7, 3, 9, 5, 3, 8.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "The mode is the value that appears most often.",
    "misconceptions": [mis("found_median", 5, "That is the median (the middle when ordered). The mode is the most frequent value, which is 3 (it appears 3 times).")],
    "guided_steps": [
        box("How many times does 3 appear in 3, 7, 3, 9, 5, 3, 8? ", 3, "Count the 3s.", say="The mode is the value that appears most often. Count how often each value shows up."),
        box("The mode is the value that appears 3 times: ", 3, "Which value repeated?", say="Every other value appears just once, so 3 wins.", phase="substitute", done="Mode is 3."),
        box("How many values appear exactly once (7, 9, 5, 8)? ", 4, "Count them.", phase="substitute", done="Four singles and one triple, so the mode is 3."),
    ]})
# B4 range 18,5,11,24,9 -> 19
bronze.append({
    "display": "Find the range of 18, 5, 11, 24, 9.",
    "solutions": [19], "calculator": False, "input_type": "single_value",
    "hint": "Range is the largest value take away the smallest.",
    "misconceptions": [mis("gave_max", 24, "24 is the largest value, not the range. Range = largest − smallest = 24 − 5 = 19.")],
    "guided_steps": [
        box("Largest value in 18, 5, 11, 24, 9 is ", 24, "Pick the biggest.", say="Range measures spread: the gap between the biggest and smallest values."),
        box("Smallest value is ", 5, "Pick the smallest.", phase="substitute"),
        box("Range = 24 − 5 = ", 19, "Largest minus smallest.", phase="substitute", done="Range is 19."),
    ]})
# B5 mean of 6 numbers is 9, total = 54
bronze.append({
    "display": "The mean of 6 numbers is 9. Find the total.",
    "solutions": [54], "calculator": False, "input_type": "single_value",
    "hint": "Total = mean × how many numbers there are.",
    "misconceptions": [mis("added", 15, "Do not add the two numbers. Total = mean × count = 9 × 6 = 54.")],
    "guided_steps": [
        box("The mean is 9 and there are 6 numbers. Count = ", 6, "How many numbers?", say="The mean is the total shared equally, so total = mean × count."),
        box("Total = mean × count = 9 × 6 = ", 54, "Multiply mean by count.", phase="substitute", done="Total is 54."),
        box("Check: 54 shared between 6 gives 54 ÷ 6 = ", 9, "Divide back.", phase="substitute", done="It gives the mean 9, so 54 is right."),
    ]})
# B6 median 8,3,12,5,10,2 -> 6.5
bronze.append({
    "display": "Find the median of 8, 3, 12, 5, 10, 2.",
    "solutions": [6.5], "calculator": False, "input_type": "single_value",
    "hint": "Order them first, then average the middle two.",
    "misconceptions": [mis("no_order", 8.5, "Order the list first. Averaging the two middle values of the unordered list gives 8.5, but ordered (2, 3, 5, 8, 10, 12) the middle two are 5 and 8, mean 6.5.")],
    "guided_steps": [
        box("How many values? ", 6, "Count them.", say="Six values, an even amount, so the median is the average of the middle two. Ordered: 2, 3, 5, 8, 10, 12."),
        box("The 3rd and 4th values are 5 and ", 8, "Read the 4th value.", say="With 6 values the middle two are the 3rd and 4th.", phase="substitute"),
        box("Median = (5 + 8) ÷ 2 = ", 6.5, "Average the middle two.", phase="substitute", done="Median is 6.5."),
    ]})
# B7 mean 15,20,10,25,30 -> 20
bronze.append({
    "display": "Find the mean of 15, 20, 10, 25, 30.",
    "solutions": [20], "calculator": False, "input_type": "single_value",
    "hint": "Add all five, then divide by 5.",
    "misconceptions": [mis("gave_total", 100, "100 is the total. The mean divides that by 5: 100 ÷ 5 = 20.")],
    "guided_steps": [
        box("Add all five: 15 + 20 + 10 + 25 + 30 = ", 100, "Add them up."),
        box("How many numbers? ", 5, "Count them.", say="Now share the total equally.", phase="substitute"),
        box("Mean = 100 ÷ 5 = ", 20, "Divide the total by 5.", phase="substitute", done="Mean is 20."),
    ]})
# B8 mode 45,52,52,60,65,70,75,80 -> 52
bronze.append({
    "display": "Eight students scored: 45, 52, 52, 60, 65, 70, 75, 80. What is the mode?",
    "solutions": [52], "calculator": False, "input_type": "single_value",
    "hint": "The mode is the score that appears most often.",
    "misconceptions": [mis("found_median", 62.5, "That is the median (the mean of the 4th and 5th of the eight ordered scores). The mode is the most frequent value, which is 52.")],
    "guided_steps": [
        box("How many times does 52 appear? ", 2, "Count the 52s.", say="The mode is the most common value. Scan for any score that repeats."),
        box("The mode is ", 52, "The repeated score.", say="Every other score appears once, so 52 is the mode.", phase="substitute", done="Mode is 52."),
        box("Careful: the median is the mean of the 4th and 5th ordered scores, 60 and 65, that is (60 + 65) ÷ 2 = ", 62.5, "Average 60 and 65.", phase="substitute", done="Median 62.5 is not what mode asks for. Mode is 52."),
    ]})

# =================== SILVER ===================
silver = []
# S1 freq table 2/3,3/7,4/6,5/4 mean 3.55
s1_rows = [(2, 3), (3, 7), (4, 6), (5, 4)]
silver.append({
    "display": svg_table(("Score", "Frequency"), s1_rows, aria_freq(s1_rows)) +
               " The frequency table shows a set of scores. Find the mean.",
    "solutions": [3.55], "calculator": True, "input_type": "single_value",
    "hint": "Work out score × frequency for each row, add them, then divide by the total frequency.",
    "misconceptions": [mis("ignored_frequency", 3.5, "Averaging the scores 2, 3, 4, 5 gives 3.5, but each score must be weighted by its frequency: 71 ÷ 20 = 3.55.")],
    "guided_steps": [
        box("Row 1: 2 × 3 = ", 6, "Score × frequency.", say="Add an fx column: score × frequency for each row."),
        box("Row 2: 3 × 7 = ", 21, "Score × frequency."),
        box("Row 3: 4 × 6 = ", 24, "Score × frequency."),
        box("Row 4: 5 × 4 = ", 20, "Score × frequency."),
        box("Σfx = 6 + 21 + 24 + 20 = ", 71, "Add the fx values.", say="Total the fx column and the frequency column.", phase="substitute"),
        box("Σf = 3 + 7 + 6 + 4 = ", 20, "Add the frequencies.", phase="substitute"),
        box("Mean = 71 ÷ 20 = ", 3.55, "Divide Σfx by Σf.", phase="substitute", done="Mean is 3.55."),
    ]})
# S2 grouped 0-10/5,10-20/15,20-30/10 est mean 16.7
s2_rows = [("0-10", 5), ("10-20", 15), ("20-30", 10)]
silver.append({
    "display": svg_table(("Class", "Frequency"), s2_rows, aria_freq(s2_rows, grouped=True)) +
               " The grouped frequency table shows a set of values. Estimate the mean to 1 d.p.",
    "solutions": [16.7], "calculator": True, "input_type": "single_value",
    "hint": "Use the midpoint of each class, multiply by frequency, add, then divide by 30.",
    "misconceptions": [
        mis("ignored_frequency", 15, "Averaging the midpoints 5, 15, 25 gives 15, but each midpoint must be weighted by its frequency: 500 ÷ 30 = 16.7."),
        mis("used_upper_bounds", 21.7, "Use the class midpoints (5, 15, 25), not the upper boundaries (10, 20, 30). Midpoints give 500 ÷ 30 = 16.7."),
    ],
    "guided_steps": [
        box("Midpoint of 0-10 = (0 + 10) ÷ 2 = ", 5, "Halfway across.", say="You only have classes, so use each class midpoint as the value."),
        box("Midpoint of 10-20 = ", 15, "Halfway between 10 and 20."),
        box("Midpoint of 20-30 = ", 25, "Halfway between 20 and 30."),
        box("5×5 + 15×15 + 10×25 = 25 + 225 + 250 = ", 500, "Add the three products.", say="Now f × midpoint for each class and add.", phase="substitute"),
        box("Total frequency Σf = 5 + 15 + 10 = ", 30, "Add the frequencies.", phase="substitute"),
        box("Estimated mean = 500 ÷ 30 = 16.66..., to 1 d.p. = ", 16.7, "Divide, then round to 1 d.p.", phase="substitute", done="Estimated mean is 16.7."),
    ]})
# S3 reverse mean sixth number 30
silver.append({
    "display": "The mean of 5 numbers is 12. A sixth number is added and the mean becomes 15. What is the sixth number?",
    "solutions": [30], "calculator": False, "input_type": "single_value",
    "hint": "Find the total of all 6 numbers, then take away the total of the first 5.",
    "misconceptions": [mis("used_new_mean", 15, "15 is the new mean, not the sixth number. The sixth number must lift the total from 60 to 90, so it is 90 − 60 = 30.")],
    "guided_steps": [
        box("Original total of the 5 numbers = 5 × 12 = ", 60, "Mean × count.", say="Turn each mean into a total: total = mean × count."),
        box("New total = 6 × 15 = ", 90, "New mean × new count.", say="After adding the sixth number there are 6 numbers with mean 15.", phase="substitute"),
        box("Sixth number = new total − old total = 90 − 60 = ", 30, "Subtract the totals.", phase="substitute", done="The sixth number is 30."),
    ]})
# S4 modal class MC
s4_rows = [("0-20", 8), ("20-40", 12), ("40-60", 10)]
silver.append({
    "display": svg_table(("Class", "Frequency"), s4_rows, aria_freq(s4_rows, grouped=True)) +
               " Which is the modal class?",
    "options": ["20-40", "0-20", "40-60", "Cannot tell"], "solutions": [0],
    "calculator": False, "input_type": "multiple_choice",
    "hint": "The modal class is the one with the highest frequency.",
    "misconceptions": [mis("wrong", None, "The modal class has the highest frequency, which is 20-40 (f=12).")],
})
# S5 median class MC, 40 values
s5_rows = [("0-10", 8), ("10-20", 15), ("20-30", 12), ("30-40", 5)]
silver.append({
    "display": svg_table(("Class", "Frequency"), s5_rows, aria_freq(s5_rows, grouped=True)) +
               " There are 40 values. Find the median class.",
    "options": ["10-20", "20-30", "0-10", "30-40"], "solutions": [0],
    "calculator": False, "input_type": "multiple_choice",
    "hint": "Find the halfway position (n ÷ 2) and track the running totals.",
    "misconceptions": [mis("wrong", None, "n ÷ 2 = 20. The running totals are 8, 23, 35, 40, so the 20th value lands in 10-20.")],
})
# S6 freq table median 1/4,2/6,3/10,4/5,5/5 -> 3
s6_rows = [(1, 4), (2, 6), (3, 10), (4, 5), (5, 5)]
silver.append({
    "display": svg_table(("Score", "Frequency"), s6_rows, aria_freq(s6_rows)) +
               " The frequency table shows a set of scores. Find the median.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Build a running total of the frequencies to find where the middle values land.",
    "misconceptions": [mis("position_as_value", 15, "n ÷ 2 = 15 is a position, not the value there. Track the cumulative frequency: the 15th and 16th values fall in score 3, so the median is 3.")],
    "guided_steps": [
        box("There are 30 values in total. Running total after score 1 (f=4) is ", 4, "Just the first frequency.", say="Build a running total (cumulative frequency) to find where the middle values sit."),
        box("After score 2 (f=6): 4 + 6 = ", 10, "Add the next frequency."),
        box("After score 3 (f=10): 10 + 10 = ", 20, "Add the next frequency."),
        box("Middle position = (30 + 1) ÷ 2 = ", 15.5, "(30+1)÷2.", say="With 30 values the median is the average of the 15th and 16th values.", phase="substitute"),
        box("The 15th and 16th values both fall in the score-3 group (running total goes from 10 to 20). The median is ", 3, "Which score covers positions 11 to 20?", phase="substitute", done="Median is 3."),
    ]})
# S7 median-becomes-7 MC (textual list)
silver.append({
    "display": "Data: 4, 6, 6, 8, 10, 14. One more value is added and the median becomes 7. What could the new value be?",
    "options": ["7", "3", "2", "16"], "solutions": [0],
    "calculator": False, "input_type": "multiple_choice",
    "hint": "With 7 values the median is the 4th when ordered; test which option puts 7 there.",
    "misconceptions": [mis("wrong", None, "With 7 values the median is the 4th when ordered. Inserting 7 gives 4, 6, 6, 7, 8, 10, 14, whose 4th value is 7.")],
})

# =================== GOLD ===================
gold = []
# G1 grouped 10-50 est mean 31.7
g1_rows = [("10-20", 4), ("20-30", 8), ("30-40", 12), ("40-50", 6)]
gold.append({
    "display": svg_table(("Class", "Frequency"), g1_rows, aria_freq(g1_rows, grouped=True)) +
               " Estimate the mean to 1 d.p.",
    "solutions": [31.7], "calculator": True, "input_type": "single_value",
    "hint": "Use midpoints 15, 25, 35, 45, multiply by frequency, add, then divide by 30.",
    "misconceptions": [mis("used_upper_bounds", 36.7, "Using the upper class boundaries (20, 30, 40, 50) instead of midpoints gives 36.7. Use midpoints 15, 25, 35, 45: 950 ÷ 30 = 31.7.")],
    "guided_steps": [
        box("Midpoints are 15, 25, 35, 45. For 10-20: 4 × 15 = ", 60, "Frequency × midpoint.", say="Use class midpoints as the values."),
        box("For 20-30: 8 × 25 = ", 200, "Frequency × midpoint."),
        box("For 30-40: 12 × 35 = ", 420, "Frequency × midpoint."),
        box("For 40-50: 6 × 45 = ", 270, "Frequency × midpoint."),
        box("Σfx = 60 + 200 + 420 + 270 = ", 950, "Add the four products.", say="Add them up and divide by the total frequency.", phase="substitute"),
        box("Σf = 4 + 8 + 12 + 6 = ", 30, "Add the frequencies.", phase="substitute"),
        box("Estimated mean = 950 ÷ 30 = 31.66..., to 1 d.p. = ", 31.7, "Divide, then round to 1 d.p.", phase="substitute", done="Estimated mean is 31.7."),
    ]})
# G2 mean of last 3 = 20
gold.append({
    "display": "The mean of a set of 8 numbers is 15. The mean of the first 5 is 12. Find the mean of the last 3.",
    "solutions": [20], "calculator": False, "input_type": "single_value",
    "hint": "Turn each mean into a total first, then work with the totals.",
    "misconceptions": [mis("forgot_to_subtract", 40, "Dividing the whole total 120 by 3 gives 40, but the last 3 are only what remains after the first 5: 120 − 60 = 60, then 60 ÷ 3 = 20.")],
    "guided_steps": [
        box("Total of all 8 numbers = 8 × 15 = ", 120, "Mean × count.", say="Turn each mean into a total first."),
        box("Total of the first 5 = 5 × 12 = ", 60, "Mean × count."),
        box("Total of the last 3 = 120 − 60 = ", 60, "Subtract the first-5 total from the whole.", say="The last 3 make up the rest of the total.", phase="substitute"),
        box("Mean of the last 3 = 60 ÷ 3 = ", 20, "Divide by 3.", phase="substitute", done="Mean of the last 3 is 20."),
    ]})
# G3 range x4 -> 80
gold.append({
    "display": "A data set has mean 15 and range 20. Each value is multiplied by 4. What is the new range?",
    "solutions": [80], "calculator": False, "input_type": "single_value",
    "hint": "Multiplying every value scales the range by the same amount.",
    "misconceptions": [
        mis("range_unchanged", 20, "The range does change. Multiplying every value by 4 multiplies the range by 4: 4 × 20 = 80."),
        mis("gave_mean", 60, "The question asks for the new range, not the mean. The range becomes 4 × 20 = 80."),
    ],
    "guided_steps": [
        box("Old range is 20. The range is multiplied by the same factor as the values, which is ", 4, "The scale factor.", say="Multiplying every value by 4 stretches the whole data set, so the spread scales by the same factor."),
        box("New range = 4 × 20 = ", 80, "4 times the old range.", phase="substitute"),
        box("Check with sample ends 10 and 30 (range 20): after ×4 they are 40 and 120, so 120 − 40 = ", 80, "120 − 40.", phase="substitute", done="Same answer 80, so the range quadruples."),
    ]})
# G4 +10 -> new mean 35
gold.append({
    "display": "A data set has mean 25 and range 12. The value 10 is added to every number. What is the new mean?",
    "solutions": [35], "calculator": False, "input_type": "single_value",
    "hint": "Adding the same number to every value shifts the mean by that number.",
    "misconceptions": [mis("mean_unchanged", 25, "The mean does change. Adding 10 to every value adds 10 to the mean: 25 + 10 = 35.")],
    "guided_steps": [
        box("Adding 10 to every value changes the range by ", 0, "The gap between values does not change.", say="First, what happens to the spread? Adding the same number to every value moves them all together."),
        box("New mean = old mean + 10 = 25 + 10 = ", 35, "Add 10 to the mean.", say="So the range stays 12. Now the mean: every value rose by 10, so their average rises by 10.", phase="substitute"),
        box("Check: sample values 20, 25, 30 (mean 25) each gain 10 to give 30, 35, 40, mean = 105 ÷ 3 = ", 35, "Add them and divide by 3.", phase="substitute", done="Mean rises to 35, exactly the shift of 10."),
    ]})
# G5 find k = 10
g5_rows = [("0-20", 5), ("20-40", 10), ("40-60", "k"), ("60-80", 5)]
gold.append({
    "display": svg_table(("Class", "Frequency"), g5_rows, aria_freq(g5_rows, grouped=True)) +
               " The estimated mean is 40. Find \\(k\\).",
    "solutions": [10], "calculator": True, "input_type": "single_value",
    "hint": "Write Σfx and Σf in terms of k, set the mean to 40, then solve.",
    "misconceptions": [mis("wrong_setup", None, "Use midpoints and keep k in both sums: (700 + 50k) ÷ (20 + k) = 40 gives 10k = 100, so k = 10.")],
    "guided_steps": [
        box("Known part of Σfx: 5×10 + 10×30 + 5×70 = 50 + 300 + 350 = ", 700, "Add the three known products.", say="Use midpoints 10, 30, 50, 70. Write Σfx with k in it."),
        box("Total known frequency: 5 + 10 + 5 = ", 20, "Add the three known frequencies.", say="The class 40-60 has midpoint 50 and frequency k, adding 50k. So Σfx = 700 + 50k and Σf = 20 + k."),
        box("Collect k terms: 50k − 40k = 800 − 700, so 10k = ", 100, "800 − 700.", say="Set the mean to 40: (700 + 50k) ÷ (20 + k) = 40. Multiply out: 700 + 50k = 40(20 + k) = 800 + 40k.", phase="substitute"),
        box("k = 100 ÷ 10 = ", 10, "Divide by 10.", phase="substitute", done="k = 10."),
        box("Check: Σf = 30 and Σfx = 700 + 500 = 1200, so mean = 1200 ÷ 30 = ", 40, "Confirm it gives 40.", phase="substitute", done="Mean is 40, so k = 10 is right."),
    ]})

# =================== TIER GUIDES ===================
tier_guides = {
    "bronze": {
        "title": "Bronze: one list of numbers",
        "steps": [
            "<strong>Mean</strong>: add every value, then divide by how many there are. <strong>Median</strong>: order the values and take the middle (average the middle two if there is an even number).",
            "<strong>Mode</strong>: the value that appears most often. <strong>Range</strong>: largest value minus smallest value, a measure of spread.",
            "Always order the list before finding the median. The mean uses every value, so one very large number pulls it upward.",
        ],
        "example": {
            "question": "Find the median of 9, 4, 12, 7, 6.",
            "steps": [
                {"label": "Order", "content": "<p>4, 6, 7, 9, 12</p>"},
                {"label": "Middle", "content": "<p>5 values, so the middle is the 3rd: 7</p>"},
                {"label": "Answer", "content": "<p>Median = 7</p>", "isAnswer": True, "is_answer": True},
            ]}},
    "silver": {
        "title": "Silver: tables and reverse problems",
        "steps": [
            "<strong>Mean from a frequency table</strong>: add an fx column (value × frequency), total it, then divide by the total frequency Σf.",
            "<strong>Grouped data</strong>: use the midpoint of each class as the value, so the mean is an estimate. The <strong>modal class</strong> has the highest frequency.",
            "<strong>Reverse mean</strong>: turn a mean back into a total using total = mean × count, then work with the totals.",
        ],
        "example": {
            "question": "Score 1 (f=2), 2 (f=4), 3 (f=4). Find the mean.",
            "steps": [
                {"label": "fx column", "content": "<p>1×2=2, 2×4=8, 3×4=12</p>"},
                {"label": "Totals", "content": "<p>Σfx = 22, Σf = 10</p>"},
                {"label": "Mean", "content": "<p>22 ÷ 10 = 2.2</p>", "isAnswer": True, "is_answer": True},
            ]}},
    "gold": {
        "title": "Gold: estimates, changes and missing values",
        "steps": [
            "<strong>Estimated mean</strong> from grouped data: Σ(f × midpoint) ÷ Σf, and state that it is an estimate.",
            "<strong>Changing every value</strong>: adding k shifts the mean by k but leaves the range unchanged; multiplying by k scales both the mean and the range by k.",
            "<strong>Missing frequency</strong>: write Σfx and Σf using the unknown, set the mean equal to the given value, then solve.",
        ],
        "example": {
            "question": "Mean of 7 numbers is 4. An 8th number, 12, is added. Find the new mean.",
            "steps": [
                {"label": "Old total", "content": "<p>7 × 4 = 28</p>"},
                {"label": "New total", "content": "<p>28 + 12 = 40</p>"},
                {"label": "New mean", "content": "<p>40 ÷ 8 = 5</p>", "isAnswer": True, "is_answer": True},
            ]}},
}

# =================== GUIDED (opener + teach) ===================
guided = {
    "opener": {
        "label": "Before any formula",
        "steps": [
            sayonly("Three friends empty their pockets and pool their money to share it out equally."),
            box("Ben £5, Amy £7, Cal £9. Pool it all: 5 + 7 + 9 = £", 21, "Add the three amounts.",
                display=svg_money([("Ben", 5), ("Amy", 7), ("Cal", 9)])),
            box("Now share the £21 equally between the 3 friends: 21 ÷ 3 = £", 7, "Split it three ways."),
            sayonly("That shared-out figure, £7, is the <strong>mean</strong>. Every mean is just this: pool everything, then share it equally, so mean = total ÷ how many. Median and mode are two other kinds of 'middle' you will meet in a moment."),
        ]},
    "teach": {
        "bronze": {
            "display": "Five test marks: 8, 2, 9, 4, 7. Find the mean, then the median.",
            "label": "Together: your first one",
            "steps": [
                box("8 + 2 + 9 + 4 + 7 = ", 30, "Add the five marks.", say="Mean first: pool all the marks, then share equally."),
                box("Divide by how many marks: 30 ÷ 5 = ", 6, "30 shared between 5."),
                box("5 values, so the middle is position (5+1) ÷ 2 = ", 3, "(5+1)÷2.", say="Now the median. Put them in order: 2, 4, 7, 8, 9."),
                box("The 3rd value in 2, 4, 7, 8, 9 is ", 7, "Count to the third.", done="Median 7, mean 6. Both are 'averages', found in different ways."),
            ]},
        "silver": {
            "display": "A frequency table: value 2 (f=4), value 4 (f=4), value 5 (f=2). Find the mean.",
            "label": "Together: a frequency table",
            "steps": [
                box("Row 1: 2 × 4 = ", 8, "Value times frequency.", say="Add an fx column: multiply each value by its frequency."),
                box("Row 2: 4 × 4 = ", 16, "Value times frequency."),
                box("Row 3: 5 × 2 = ", 10, "Value times frequency."),
                box("Σfx = 8 + 16 + 10 = ", 34, "Add the fx values.", say="Total the fx column, then the frequency column."),
                box("Σf = 4 + 4 + 2 = ", 10, "Add the frequencies."),
                box("Mean = 34 ÷ 10 = ", 3.4, "Divide Σfx by Σf.", done="Not (2+4+5)÷3. The frequencies weight each value."),
            ]},
        "gold": {
            "display": "Grouped data: 0-10 (f=3), 10-20 (f=4), 20-30 (f=3). Estimate the mean.",
            "label": "Together: estimate from grouped data",
            "steps": [
                box("Midpoint of 0-10 = (0 + 10) ÷ 2 = ", 5, "Halfway across the class.", say="You do not have exact values, so use each class midpoint."),
                box("Midpoint of 10-20 = ", 15, "Halfway between 10 and 20."),
                box("Midpoint of 20-30 = ", 25, "Halfway between 20 and 30."),
                box("3×5 + 4×15 + 3×25 = 15 + 60 + 75 = ", 150, "Add the three products.", say="Now f × midpoint for each class, and add."),
                box("Total frequency: 3 + 4 + 3 = ", 10, "Add the frequencies."),
                box("Estimated mean = 150 ÷ 10 = ", 15, "Divide by the total frequency.", done="It is an estimate because we used midpoints, not the real values."),
            ]},
    },
}

# =================== ASSEMBLE ===================
pd = dict(live)  # preserve method_card, topic_links, related_videos, worked_examples
pd["problem_bank"] = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "One list of numbers: find its mean, median, mode or range.",
    "silver_description": "Averages from frequency tables and grouped data, plus reverse mean problems.",
    "gold_description": "Estimated means, combined or transformed data sets, and a missing frequency.",
}
pd["tier_guides"] = tier_guides
pd["guided"] = guided

json.dump(pd, io.open("lesson_maths-eduqas_probability-statistics-L04.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written. bronze=%d silver=%d gold=%d" % (len(bronze), len(silver), len(gold)))
