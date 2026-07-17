# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion of maths-ocr probability-statistics-L05."""
import json, io

MINUS = "−"  # unicode minus for student-facing maths

# ---------- figure generators ----------
def boxplot_svg(mn, q1, med, q3, mx, axmin, axmax, ticks, aria):
    def sx(v):
        return 20 + (v - axmin) / (axmax - axmin) * 220.0
    p = ['<svg viewBox="0 0 260 100" role="img" aria-label="%s" style="display:block;margin:0 auto 0.4rem;max-width:280px;width:100%%">' % aria]
    p.append('<line x1="20" y1="74" x2="240" y2="74" stroke="currentColor" stroke-width="1"/>')
    for t in ticks:
        x = sx(t)
        p.append('<line x1="%.1f" y1="74" x2="%.1f" y2="78" stroke="currentColor" stroke-width="1"/>' % (x, x))
        p.append('<text x="%.1f" y="90" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % (x, t))
    xmn, xq1, xmed, xq3, xmx = sx(mn), sx(q1), sx(med), sx(q3), sx(mx)
    p.append('<line x1="%.1f" y1="40" x2="%.1f" y2="40" stroke="currentColor" stroke-width="1.4"/>' % (xmn, xq1))
    p.append('<line x1="%.1f" y1="40" x2="%.1f" y2="40" stroke="currentColor" stroke-width="1.4"/>' % (xq3, xmx))
    p.append('<line x1="%.1f" y1="31" x2="%.1f" y2="49" stroke="currentColor" stroke-width="1.4"/>' % (xmn, xmn))
    p.append('<line x1="%.1f" y1="31" x2="%.1f" y2="49" stroke="currentColor" stroke-width="1.4"/>' % (xmx, xmx))
    p.append('<rect x="%.1f" y="24" width="%.1f" height="32" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>' % (xq1, xq3 - xq1))
    p.append('<line x1="%.1f" y1="24" x2="%.1f" y2="56" stroke="currentColor" stroke-width="1.8"/>' % (xmed, xmed))
    p.append('</svg>')
    return "".join(p)

def two_box_svg(a, b, axmin, axmax, ticks, aria, show_median):
    def sx(v):
        return 24 + (v - axmin) / (axmax - axmin) * 214.0
    p = ['<svg viewBox="0 0 260 122" role="img" aria-label="%s" style="display:block;margin:0 auto 0.4rem;max-width:280px;width:100%%">' % aria]
    p.append('<line x1="24" y1="98" x2="238" y2="98" stroke="currentColor" stroke-width="1"/>')
    for t in ticks:
        x = sx(t)
        p.append('<line x1="%.1f" y1="98" x2="%.1f" y2="102" stroke="currentColor" stroke-width="1"/>' % (x, x))
        p.append('<text x="%.1f" y="114" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % (x, t))
    for row, (band_y, box, lab, colour) in enumerate([(18, a, "A", "#60a5fa"), (54, b, "B", "#f59e0b")]):
        xq1, xq3 = sx(box["q1"]), sx(box["q3"])
        p.append('<rect x="%.1f" y="%d" width="%.1f" height="26" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>' % (xq1, band_y, xq3 - xq1, colour))
        if show_median and "med" in box:
            xm = sx(box["med"])
            p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1.8"/>' % (xm, band_y, xm, band_y + 26))
        p.append('<text x="14" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (band_y + 17, lab))
    p.append('</svg>')
    return "".join(p)

def histogram_svg(classes, xmin, xmax, ymax, aria):
    # classes: list of (lo, hi, fd)
    def sx(v):
        return 32 + (v - xmin) / (xmax - xmin) * 206.0
    def sy(fd):
        return 100.0 - (fd / ymax) * 84.0
    p = ['<svg viewBox="0 0 260 130" role="img" aria-label="%s" style="display:block;margin:0 auto 0.4rem;max-width:280px;width:100%%">' % aria]
    # axes
    p.append('<line x1="32" y1="100" x2="238" y2="100" stroke="currentColor" stroke-width="1"/>')
    p.append('<line x1="32" y1="12" x2="32" y2="100" stroke="currentColor" stroke-width="1"/>')
    colours = ["#60a5fa", "#34d399", "#f59e0b"]
    bounds = set()
    for i, (lo, hi, fd) in enumerate(classes):
        x1, x2, y = sx(lo), sx(hi), sy(fd)
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1.4"/>' % (x1, y, x2 - x1, 100.0 - y, colours[i % 3]))
        p.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle">%s</text>' % ((x1 + x2) / 2, y - 3, fd))
        bounds.add(lo); bounds.add(hi)
    for b in sorted(bounds):
        x = sx(b)
        p.append('<text x="%.1f" y="112" font-family="Inter,sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle">%s</text>' % (x, b))
    p.append('<text x="8" y="58" font-family="Inter,sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle" transform="rotate(-90 8 58)">Freq density</text>')
    p.append('</svg>')
    return "".join(p)

def opener_line_svg():
    p = ['<svg viewBox="0 0 240 58" role="img" aria-label="Nine people standing in a line from shortest to tallest, the fifth one in the middle highlighted" style="display:block;margin:0 auto 0.4rem;max-width:260px;width:100%">']
    for i in range(9):
        cx = 22 + i * 24
        r = 6 + i * 0.6
        if i == 4:
            p.append('<circle cx="%.1f" cy="34" r="%.1f" fill="#f59e0b" fill-opacity="0.55" stroke="currentColor" stroke-width="1.6"/>' % (cx, r))
        else:
            p.append('<circle cx="%.1f" cy="34" r="%.1f" fill="#60a5fa" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>' % (cx, r))
    p.append('<text x="22" y="52" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">shortest</text>')
    p.append('<text x="214" y="52" font-family="Inter,sans-serif" font-size="9" fill="currentColor" text-anchor="middle">tallest</text>')
    p.append('</svg>')
    return "".join(p)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# box plot for B3/B4 (min10 Q1 15 med20 Q3 28 max35)
bp_b = boxplot_svg(10, 15, 20, 28, 35, 0, 40, [0, 10, 20, 30, 40],
    "Box plot on a scale from 0 to 40 with minimum 10, lower quartile 15, median 20, upper quartile 28 and maximum 35")

# ---------- problem bank ----------
bank = {
 "bronze_description": "Read values straight off: cumulative totals, quartile positions, and spreads from a box plot.",
 "silver_description": "Frequency density both ways, quartile positions for larger samples, and reading a cumulative frequency curve.",
 "gold_description": "Unequal class widths, comparing distributions, interquartile ranges from a graph, and outlier boundaries.",
 "bronze": [
  {  # B0
   "display": "Frequencies: 4, 8, 12, 10, 5. Find the cumulative frequency after the 3rd class.",
   "solutions": [24], "calculator": False, "input_type": "single_value",
   "hint": "Add the frequencies of the first three classes only.",
   "misconceptions": [
    {"pattern": "added_all", "message": "That is the total of all five classes. The cumulative frequency after the 3rd class only adds the first three: 4 + 8 + 12 = 24.", "expect": 39},
    {"pattern": "one_too_many", "message": "That includes the 4th class. Stop after the 3rd: 4 + 8 + 12 = 24.", "expect": 34}
   ],
   "guided_steps": [
    {"say": "Cumulative frequency is a running total. Add the frequencies one class at a time up to the 3rd."},
    {"pre": "First two classes: 4 + 8 = ", "post": "", "answer": 12, "hint": "Add the first two frequencies."},
    {"phase": "substitute", "pre": "Add the 3rd class: 12 + 12 = ", "post": "", "answer": 24, "hint": "Add the third frequency to your running total."},
    {"pre": "Check by adding all three straight: 4 + 8 + 12 = ", "post": "", "answer": 24, "done": "Same total, so the cumulative frequency after the 3rd class is 24.", "hint": "Add the three frequencies in one go."}
   ]},
  {  # B1
   "display": "A cumulative frequency graph has a total frequency of 80. What cumulative frequency do you read across from to find the median?",
   "solutions": [40], "calculator": False, "input_type": "single_value",
   "hint": "The median position is the total divided by 2.",
   "misconceptions": [
    {"pattern": "used_quarter", "message": "That is the lower quartile position (n ÷ 4). The median is halfway: n ÷ 2 = 80 ÷ 2 = 40.", "expect": 20}
   ],
   "guided_steps": [
    {"say": "The median sits at the middle of the data. For n values that middle position is n ÷ 2."},
    {"pre": "How many values in total? n = ", "post": "", "answer": 80, "hint": "Read the total frequency from the question."},
    {"phase": "substitute", "pre": "Median position = n ÷ 2 = 80 ÷ 2 = ", "post": "", "answer": 40, "hint": "Divide the total by 2."},
    {"pre": "So you read across from a cumulative frequency of ", "post": "", "answer": 40, "done": "At CF = 40 you read the median off the curve.", "hint": "It is the position you just found."}
   ]},
  {  # B2
   "display": "A cumulative frequency graph has a total frequency of 60. What cumulative frequency do you read across from to find the lower quartile Q1?",
   "solutions": [15], "calculator": False, "input_type": "single_value",
   "hint": "The lower quartile position is the total divided by 4.",
   "misconceptions": [
    {"pattern": "used_half", "message": "That is the median position (n ÷ 2). Q1 is a quarter of the way in: n ÷ 4 = 60 ÷ 4 = 15.", "expect": 30}
   ],
   "guided_steps": [
    {"say": "The lower quartile Q1 sits a quarter of the way through the data: position n ÷ 4."},
    {"pre": "Total values: n = ", "post": "", "answer": 60, "hint": "Read n from the question."},
    {"phase": "substitute", "pre": "Q1 position = n ÷ 4 = 60 ÷ 4 = ", "post": "", "answer": 15, "hint": "Divide the total by 4."},
    {"pre": "So Q1 is read across from a cumulative frequency of ", "post": "", "answer": 15, "done": "At CF = 15 you read Q1 off the curve.", "hint": "The position you just found."}
   ]},
  {  # B3
   "display": bp_b + CAP + "The box plot shows min = 10, Q1 = 15, median = 20, Q3 = 28, max = 35. Find the interquartile range (IQR).",
   "solutions": [13], "calculator": False, "input_type": "single_value",
   "hint": "Interquartile range is the upper quartile minus the lower quartile.",
   "misconceptions": [
    {"pattern": "gave_range", "message": "That is the range (max − min). The IQR is the box width: Q3 − Q1 = 28 − 15 = 13.", "expect": 25},
    {"pattern": "q3_minus_median", "message": "That is Q3 − median. The IQR runs across the whole box: Q3 − Q1 = 28 − 15 = 13.", "expect": 8}
   ],
   "guided_steps": [
    {"say": "The interquartile range is the width of the box: Q3 − Q1."},
    {"pre": "Read Q3, the right side of the box: Q3 = ", "post": "", "answer": 28, "hint": "The right edge of the box."},
    {"pre": "Read Q1, the left side of the box: Q1 = ", "post": "", "answer": 15, "hint": "The left edge of the box."},
    {"phase": "substitute", "pre": "IQR = Q3 − Q1 = 28 − 15 = ", "post": "", "answer": 13, "hint": "Subtract Q1 from Q3."},
    {"pre": "Check: 15 + 13 should return Q3, so 15 + 13 = ", "post": "", "answer": 28, "done": "That gives Q3 back, so the IQR of 13 is right.", "hint": "Add the IQR onto Q1."}
   ]},
  {  # B4
   "display": bp_b + CAP + "The box plot shows min = 10, Q1 = 15, median = 20, Q3 = 28, max = 35. Find the range.",
   "solutions": [25], "calculator": False, "input_type": "single_value",
   "hint": "Range is the largest value minus the smallest.",
   "misconceptions": [
    {"pattern": "gave_iqr", "message": "That is the interquartile range (Q3 − Q1). The range spans the whole data: max − min = 35 − 10 = 25.", "expect": 13}
   ],
   "guided_steps": [
    {"say": "The range is the full spread, from the lowest value to the highest: max − min."},
    {"pre": "Read the maximum, the right whisker end: max = ", "post": "", "answer": 35, "hint": "The far right of the whisker."},
    {"pre": "Read the minimum, the left whisker end: min = ", "post": "", "answer": 10, "hint": "The far left of the whisker."},
    {"phase": "substitute", "pre": "Range = max − min = 35 − 10 = ", "post": "", "answer": 25, "hint": "Subtract the smallest from the largest."},
    {"pre": "Check: 10 + 25 should return the maximum, so 10 + 25 = ", "post": "", "answer": 35, "done": "That gives the maximum back, so the range of 25 is right.", "hint": "Add the range onto the minimum."}
   ]},
  {  # B5
   "display": "A histogram class runs 0 to 20 with frequency 10. Find the frequency density.",
   "solutions": [0.5], "calculator": False, "input_type": "single_value",
   "hint": "Frequency density is frequency divided by class width.",
   "misconceptions": [
    {"pattern": "inverted", "message": "That is width ÷ frequency, upside down. Frequency density is frequency ÷ width = 10 ÷ 20 = 0.5.", "expect": 2}
   ],
   "guided_steps": [
    {"say": "Frequency density spreads the frequency evenly across the class: frequency ÷ class width."},
    {"pre": "Class width: 20 − 0 = ", "post": "", "answer": 20, "hint": "Top of the class minus the bottom."},
    {"phase": "substitute", "pre": "Frequency density = frequency ÷ width = 10 ÷ 20 = ", "post": "", "answer": 0.5, "hint": "Divide the frequency by the width."},
    {"pre": "Check: width × density = 20 × 0.5 = ", "post": "", "answer": 10, "done": "That returns the frequency, so the density 0.5 is right.", "hint": "Multiply width by density to get frequency back."}
   ]},
  {  # B6 (keep chart)
   "display": "The frequency chart shows test scores. What is the total frequency?",
   "solutions": [45], "calculator": False, "input_type": "single_value",
   "hint": "Add the heights of all four bars.",
   "chart": {"type": "bar", "data": {"labels": ["0-10", "10-20", "20-30", "30-40"], "datasets": [{"data": [5, 12, 18, 10], "borderRadius": 6, "backgroundColor": "#3b82f6"}]},
             "options": {"scales": {"x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "Score", "display": True}}, "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 5}, "title": {"text": "Frequency", "display": True}, "beginAtZero": True}}}},
   "misconceptions": [
    {"pattern": "dropped_bar", "message": "That leaves out the last bar. All four bars count: 5 + 12 + 18 + 10 = 45.", "expect": 35}
   ],
   "guided_steps": [
    {"say": "The total frequency adds up the height of every bar."},
    {"pre": "Add the first two bars: 5 + 12 = ", "post": "", "answer": 17, "hint": "Add the first two frequencies."},
    {"pre": "Add the next bar: 17 + 18 = ", "post": "", "answer": 35, "hint": "Add the third frequency."},
    {"phase": "substitute", "pre": "Add the last bar: 35 + 10 = ", "post": "", "answer": 45, "hint": "Add the final frequency."},
    {"pre": "Check by adding all four straight: 5 + 12 + 18 + 10 = ", "post": "", "answer": 45, "done": "Same total, so 45 is right.", "hint": "Add all four frequencies."}
   ]},
  {  # B7
   "display": "Frequencies: 3, 7, 15, 10, 6. Find the total cumulative frequency.",
   "solutions": [41], "calculator": False, "input_type": "single_value",
   "hint": "Add every frequency together.",
   "misconceptions": [
    {"pattern": "dropped_last", "message": "That stops before the last class. The total adds all five: 3 + 7 + 15 + 10 + 6 = 41.", "expect": 35}
   ],
   "guided_steps": [
    {"say": "The total cumulative frequency is every frequency added together."},
    {"pre": "First three: 3 + 7 + 15 = ", "post": "", "answer": 25, "hint": "Add the first three frequencies."},
    {"phase": "substitute", "pre": "Add the rest: 25 + 10 + 6 = ", "post": "", "answer": 41, "hint": "Add the last two frequencies to your running total."},
    {"pre": "Check by adding all five straight: 3 + 7 + 15 + 10 + 6 = ", "post": "", "answer": 41, "done": "Same total, so the final cumulative frequency is 41.", "hint": "Add all five frequencies."}
   ]}
 ],
 "silver": [
  {  # S0
   "display": "A histogram class runs 15 to 25 with frequency 20. Find the frequency density.",
   "solutions": [2], "calculator": False, "input_type": "single_value",
   "hint": "Frequency density is frequency divided by class width.",
   "misconceptions": [
    {"pattern": "inverted", "message": "That is width ÷ frequency, inverted. Frequency density is frequency ÷ width = 20 ÷ 10 = 2.", "expect": 0.5}
   ],
   "guided_steps": [
    {"say": "Frequency density = frequency ÷ class width."},
    {"pre": "Class width: 25 − 15 = ", "post": "", "answer": 10, "hint": "Top minus bottom of the class."},
    {"phase": "substitute", "pre": "Frequency density = 20 ÷ 10 = ", "post": "", "answer": 2, "hint": "Divide frequency by width."},
    {"pre": "Check: width × density = 10 × 2 = ", "post": "", "answer": 20, "done": "That returns the frequency, so density 2 is right.", "hint": "Width times density gives frequency."}
   ]},
  {  # S1
   "display": "A histogram bar covers the class 0 to 5 with frequency density 3. Find the frequency.",
   "solutions": [15], "calculator": False, "input_type": "single_value",
   "hint": "Frequency is frequency density times class width.",
   "misconceptions": [
    {"pattern": "divided", "message": "That divides instead of multiplying. Frequency = density × width = 3 × 5 = 15.", "expect": 0.6}
   ],
   "guided_steps": [
    {"say": "On a histogram the frequency is the area of the bar: frequency density × class width."},
    {"pre": "Class width: 5 − 0 = ", "post": "", "answer": 5, "hint": "Top minus bottom of the class."},
    {"phase": "substitute", "pre": "Frequency = density × width = 3 × 5 = ", "post": "", "answer": 15, "hint": "Multiply density by width."},
    {"pre": "Check: 15 ÷ 5 = ", "post": "", "answer": 3, "done": "That returns the density, so the frequency 15 is right.", "hint": "Frequency divided by width gives density back."}
   ]},
  {  # S2
   "display": "A cumulative frequency diagram has n = 100. At what position is the lower quartile Q1?",
   "solutions": [25], "calculator": False, "input_type": "single_value",
   "hint": "The lower quartile position is n divided by 4.",
   "misconceptions": [
    {"pattern": "used_half", "message": "That is the median position (n ÷ 2). Q1 is at n ÷ 4 = 100 ÷ 4 = 25.", "expect": 50}
   ],
   "guided_steps": [
    {"say": "The lower quartile Q1 sits a quarter of the way through the data: position n ÷ 4."},
    {"pre": "Total values: n = ", "post": "", "answer": 100, "hint": "Read n from the question."},
    {"phase": "substitute", "pre": "Q1 position = n ÷ 4 = 100 ÷ 4 = ", "post": "", "answer": 25, "hint": "Divide the total by 4."},
    {"pre": "Check another way: a quarter of 100 = ", "post": "", "answer": 25, "done": "A quarter of 100 is 25, so Q1 is at position 25.", "hint": "One quarter of the total."}
   ]},
  {  # S3 MC
   "display": two_box_svg({"q1": 20, "q3": 45}, {"q1": 25, "q3": 55}, 0, 60, [0, 10, 20, 30, 40, 50, 60],
     "Two boxes on a shared scale from 0 to 60: box A from 20 to 45, box B from 25 to 55", False) + CAP +
     "The boxes show the middle 50% of two data sets. A: Q1 = 20, Q3 = 45. B: Q1 = 25, Q3 = 55. Which has the larger interquartile range?",
   "options": ["B (IQR=30)", "A (IQR=25)", "Same", "Cannot tell"],
   "solutions": [0], "calculator": False, "input_type": "multiple_choice",
   "hint": "Work out each interquartile range, Q3 minus Q1, then compare.",
   "misconceptions": [
    {"pattern": "compare_iqr", "message": "A has IQR 45 − 20 = 25 and B has IQR 55 − 25 = 30, so B has the wider box.", "expect": None}
   ]},
  {  # S4
   "display": "A histogram bar covers the class 10 to 30 (width 20) with frequency density 1.5. Find the frequency.",
   "solutions": [30], "calculator": False, "input_type": "single_value",
   "hint": "Frequency is density times the class width, and the width here is 20.",
   "misconceptions": [
    {"pattern": "wrong_width", "message": "That uses width 10. The class 10 to 30 is 20 wide, so frequency = 1.5 × 20 = 30.", "expect": 15}
   ],
   "guided_steps": [
    {"say": "Frequency = frequency density × class width. The wide class needs its full width."},
    {"pre": "Class width: 30 − 10 = ", "post": "", "answer": 20, "hint": "Top minus bottom of the class."},
    {"phase": "substitute", "pre": "Frequency = 1.5 × 20 = ", "post": "", "answer": 30, "hint": "Multiply density by 20."},
    {"pre": "Check: 30 ÷ 20 = ", "post": "", "answer": 1.5, "done": "That returns the density 1.5, so the frequency 30 is right.", "hint": "Divide frequency by width."}
   ]},
  {  # S5 chart CF
   "display": "The cumulative frequency diagram shows exam scores for 50 students. Estimate the median score.",
   "solutions": [20], "calculator": False, "input_type": "single_value",
   "hint": "Find the position n divided by 2, read across to the curve, then down to the score.",
   "chart": {"type": "line", "data": {"labels": [0, 10, 20, 30, 40, 50], "datasets": [{"data": [0, 12, 25, 35, 45, 50], "fill": False, "borderColor": "#3b82f6", "pointRadius": 5}]},
             "options": {"scales": {"x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "Score", "display": True}}, "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 10}, "title": {"text": "Cumulative Frequency", "display": True}, "beginAtZero": True}}}},
   "misconceptions": [
    {"pattern": "read_cf_as_score", "message": "That is the cumulative frequency you read across from, not the score. Follow the curve down to the horizontal axis: the median score is 20.", "expect": 25}
   ],
   "guided_steps": [
    {"say": "The median is the middle value. Find its position, then read across the curve and down to the score."},
    {"pre": "50 students, so the median is at position 50 ÷ 2 = ", "post": "", "answer": 25, "hint": "Halve the total frequency."},
    {"phase": "substitute", "pre": "Read across from cumulative frequency 25 to the curve, then down. The score is ", "post": "", "answer": 20, "hint": "The curve reaches CF = 25 at a score of 20."},
    {"pre": "Confirm: how many students scored 20 or less? Read the curve up at score 20: ", "post": "", "answer": 25, "done": "Half of the 50 students (25) scored 20 or less, so 20 is the median.", "hint": "Read the cumulative frequency at score 20."}
   ]},
  {  # S6
   "display": "A cumulative frequency table reads: up to 10 = 8, up to 20 = 22, up to 30 = 40, up to 40 = 50. Find the frequency in the 20 to 30 class.",
   "solutions": [18], "calculator": False, "input_type": "single_value",
   "hint": "Subtract the cumulative frequency at 20 from the cumulative frequency at 30.",
   "misconceptions": [
    {"pattern": "read_cf_as_freq", "message": "That is the cumulative frequency up to 30, a running total. The frequency in the class is the jump: 40 − 22 = 18.", "expect": 40},
    {"pattern": "wrong_classes", "message": "That is the 30 to 40 frequency. For 20 to 30 subtract the two totals either side: 40 − 22 = 18.", "expect": 10}
   ],
   "guided_steps": [
    {"say": "A cumulative frequency is a running total. The frequency IN a class is the jump in cumulative frequency across it."},
    {"pre": "Cumulative frequency up to 30: ", "post": "", "answer": 40, "hint": "Read the total at the top of the class."},
    {"pre": "Cumulative frequency up to 20: ", "post": "", "answer": 22, "hint": "Read the total at the bottom of the class."},
    {"phase": "substitute", "pre": "Frequency in 20 to 30 = 40 − 22 = ", "post": "", "answer": 18, "hint": "Subtract the lower running total from the higher."},
    {"pre": "Check: 22 + 18 should give the total up to 30, so 22 + 18 = ", "post": "", "answer": 40, "done": "That returns 40, so 18 is the frequency in the 20 to 30 class.", "hint": "Add the frequency back onto the earlier total."}
   ]}
 ],
 "gold": [
  {  # G0 histogram
   "display": histogram_svg([(0, 10, 1.2), (10, 20, 2.5), (20, 40, 1.8)], 0, 40, 2.5,
     "Histogram with three bars: 0 to 10 at frequency density 1.2, 10 to 20 at 2.5, and 20 to 40 at 1.8") + CAP +
     "The histogram has classes 0-10 (FD 1.2), 10-20 (FD 2.5) and 20-40 (FD 1.8). Find the frequency of the 20-40 class.",
   "solutions": [36], "calculator": False, "input_type": "single_value",
   "hint": "Frequency is density times width, and this class is 20 wide.",
   "misconceptions": [
    {"pattern": "wrong_width", "message": "That uses width 10. The class 20 to 40 is 20 wide, so frequency = 1.8 × 20 = 36.", "expect": 18}
   ],
   "guided_steps": [
    {"say": "Frequency is the area of the bar: frequency density × class width. Mind the wider class."},
    {"pre": "Width of the 20 to 40 class: 40 − 20 = ", "post": "", "answer": 20, "hint": "Top minus bottom of that class."},
    {"phase": "substitute", "pre": "Frequency = density × width = 1.8 × 20 = ", "post": "", "answer": 36, "hint": "Multiply the density by 20, not by 10."},
    {"pre": "Check: 36 ÷ 20 = ", "post": "", "answer": 1.8, "done": "That returns the density 1.8, so the frequency 36 is right.", "hint": "Divide frequency by width to get density back."}
   ]},
  {  # G1 MC two box plots (Q1, med, Q3)
   "display": two_box_svg({"q1": 15, "med": 22, "q3": 30}, {"q1": 18, "med": 25, "q3": 32}, 0, 40, [0, 10, 20, 30, 40],
     "Two boxes with median lines on a scale from 0 to 40: box A from 15 to 30 with median 22, box B from 18 to 32 with median 25", True) + CAP +
     "The boxes show two data sets. A: Q1 = 15, median = 22, Q3 = 30. B: Q1 = 18, median = 25, Q3 = 32. Which has the higher median?",
   "options": ["B", "A", "Same", "Cannot tell"],
   "solutions": [0], "calculator": False, "input_type": "multiple_choice",
   "hint": "Compare the median lines of the two boxes.",
   "misconceptions": [
    {"pattern": "compare_median", "message": "A has median 22 and B has median 25, so B has the higher median line.", "expect": None}
   ]},
  {  # G2
   "display": "A cumulative frequency graph has total 80. The median at position 40 reads 32, Q1 at position 20 reads 24, and Q3 at position 60 reads 42. Find the IQR.",
   "solutions": [18], "calculator": False, "input_type": "single_value",
   "hint": "Interquartile range is the upper quartile reading minus the lower quartile reading.",
   "misconceptions": [
    {"pattern": "used_positions", "message": "Those are the positions (60 and 20), not the readings. The IQR uses the values off the curve: 42 − 24 = 18.", "expect": 40},
    {"pattern": "q3_minus_median", "message": "That is Q3 − median. The IQR is Q3 − Q1 = 42 − 24 = 18.", "expect": 10}
   ],
   "guided_steps": [
    {"say": "The interquartile range is Q3 − Q1, using the values read off the curve, not the positions."},
    {"pre": "Upper quartile read from the curve: Q3 = ", "post": "", "answer": 42, "hint": "The value given at position 60."},
    {"pre": "Lower quartile read from the curve: Q1 = ", "post": "", "answer": 24, "hint": "The value given at position 20."},
    {"phase": "substitute", "pre": "IQR = Q3 − Q1 = 42 − 24 = ", "post": "", "answer": 18, "hint": "Subtract Q1 from Q3."},
    {"pre": "Check: 24 + 18 should return Q3, so 24 + 18 = ", "post": "", "answer": 42, "done": "That returns Q3, so the IQR of 18 is right.", "hint": "Add the IQR back onto Q1."}
   ]},
  {  # G3 FIXED sol 50 -> 70
   "display": histogram_svg([(0, 5, 4), (5, 15, 2), (15, 20, 6)], 0, 20, 6,
     "Histogram with three bars of unequal width: 0 to 5 at frequency density 4, 5 to 15 at 2, and 15 to 20 at 6") + CAP +
     "The histogram has classes 0-5 (FD 4), 5-15 (FD 2) and 15-20 (FD 6). Find the total frequency.",
   "solutions": [70], "calculator": False, "input_type": "single_value",
   "hint": "Work out each bar as density times its own width, then add, watching the widths.",
   "misconceptions": [
    {"pattern": "equal_widths", "message": "That uses width 5 for every class. The middle class 5 to 15 is 10 wide: 4 × 5 + 2 × 10 + 6 × 5 = 70.", "expect": 60}
   ],
   "guided_steps": [
    {"say": "Total frequency adds up every bar's area: frequency density × width for each class, then sum."},
    {"pre": "First class 0 to 5 (width 5): 4 × 5 = ", "post": "", "answer": 20, "hint": "Density times width, width = 5."},
    {"pre": "Second class 5 to 15 (width 10): 2 × 10 = ", "post": "", "answer": 20, "hint": "Width is 15 − 5 = 10."},
    {"pre": "Third class 15 to 20 (width 5): 6 × 5 = ", "post": "", "answer": 30, "hint": "Width is 20 − 15 = 5."},
    {"phase": "substitute", "pre": "Total frequency = 20 + 20 + 30 = ", "post": "", "answer": 70, "hint": "Add the three frequencies."},
    {"pre": "Check by adding the areas again: 20 + 20 + 30 = ", "post": "", "answer": 70, "done": "All three bar areas add to 70, so the total frequency is 70.", "hint": "Add the three areas once more."}
   ]},
  {  # G4
   "display": "An outlier is defined as more than 1.5 × IQR above Q3. Q3 = 45 and IQR = 20. Find the upper outlier boundary.",
   "solutions": [75], "calculator": False, "input_type": "single_value",
   "hint": "Add 1.5 times the interquartile range onto the upper quartile.",
   "misconceptions": [
    {"pattern": "one_iqr", "message": "That adds only one IQR. The rule uses 1.5 IQRs: 45 + 1.5 × 20 = 75.", "expect": 65},
    {"pattern": "forgot_q3", "message": "That is just 1.5 × IQR. Add it onto Q3: 45 + 30 = 75.", "expect": 30}
   ],
   "guided_steps": [
    {"say": "The upper outlier boundary is Q3 plus 1.5 lots of the IQR."},
    {"pre": "1.5 × IQR = 1.5 × 20 = ", "post": "", "answer": 30, "hint": "Multiply the IQR by 1.5."},
    {"phase": "substitute", "pre": "Boundary = Q3 + that = 45 + 30 = ", "post": "", "answer": 75, "hint": "Add to Q3."},
    {"pre": "Check: 75 − 45 should be 1.5 × 20 = 30, and 75 − 45 = ", "post": "", "answer": 30, "done": "That returns 30 = 1.5 × IQR, so the boundary 75 is right.", "hint": "Subtract Q3 from your boundary."}
   ]}
 ]
}

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: totals, positions and box plot spreads",
  "steps": [
   "Cumulative frequency is a running total: add each class frequency onto the last. The final total is n.",
   "The median is at position n ÷ 2, the lower quartile Q1 at n ÷ 4, and the upper quartile Q3 at 3n ÷ 4.",
   "From a box plot: IQR = Q3 − Q1 (the box width) and range = max − min (whisker to whisker)."
  ],
  "example": {
   "question": "Frequencies 5, 9, 6. Find the total cumulative frequency and the median position.",
   "steps": [
    {"label": "Running total", "content": "<p>5, then 5 + 9 = 14, then 14 + 6 = 20. So n = 20.</p>"},
    {"label": "Median position", "content": "<p>n ÷ 2 = 20 ÷ 2 = 10.</p>"},
    {"label": "Check", "content": "<p>5 + 9 + 6 = 20 ✓</p>"},
    {"label": "Answer", "content": "<p><strong>Total 20, median at position 10.</strong></p>", "isAnswer": True, "is_answer": True}
   ]}
 },
 "silver": {
  "title": "Silver: frequency density and reading a curve",
  "steps": [
   "Frequency density = frequency ÷ class width, so a bar's frequency is density × width (its area). The formula runs both ways.",
   "Quartile positions still use n ÷ 4, n ÷ 2 and 3n ÷ 4, whatever the sample size.",
   "To read a cumulative frequency curve: go up to the position, across to the curve, then down to the value."
  ],
  "example": {
   "question": "A histogram bar spans 10 to 30 with frequency density 3. Find the frequency.",
   "steps": [
    {"label": "Width", "content": "<p>30 − 10 = 20.</p>"},
    {"label": "Frequency", "content": "<p>density × width = 3 × 20 = 60.</p>"},
    {"label": "Check", "content": "<p>60 ÷ 20 = 3 ✓</p>"},
    {"label": "Answer", "content": "<p><strong>Frequency = 60.</strong></p>", "isAnswer": True, "is_answer": True}
   ]}
 },
 "gold": {
  "title": "Gold: unequal widths, comparisons and outliers",
  "steps": [
   "When class widths differ, work out each bar's frequency separately as density × its own width, then add for the total.",
   "Compare distributions from box plots using the median (average) and the IQR (spread).",
   "An outlier lies more than 1.5 × IQR beyond a quartile: above Q3 + 1.5 IQR or below Q1 − 1.5 IQR."
  ],
  "example": {
   "question": "Classes 0 to 20 (FD 1) and 20 to 30 (FD 4). Find the total frequency.",
   "steps": [
    {"label": "Each bar", "content": "<p>0 to 20: 1 × 20 = 20. 20 to 30: 4 × 10 = 40.</p>"},
    {"label": "Total", "content": "<p>20 + 40 = 60.</p>"},
    {"label": "Check", "content": "<p>Widths 20 and 10 used correctly ✓</p>"},
    {"label": "Answer", "content": "<p><strong>Total frequency = 60.</strong></p>", "isAnswer": True, "is_answer": True}
   ]}
 }
}

# ---------- guided (opener + teach) ----------
guided = {
 "opener": {
  "label": "Before any graphs",
  "display": opener_line_svg() + "Nine students stand in a line, shortest to tallest.",
  "steps": [
   {"say": "No maths yet, just look at the line. As many people should stand to the left of the middle person as to the right.",
    "pre": "Which position is the exact middle? Position ", "post": "", "answer": 5, "hint": "Count in from both ends until you meet: with 9 people the middle is the 5th."},
   {"say": "Now a bigger line: 80 people, shortest to tallest. The middle sits halfway along.",
    "pre": "Middle position: 80 ÷ 2 = ", "post": "", "answer": 40, "hint": "Halve the total number of people."},
   {"say": "You just found the <strong>median</strong> by its position, n ÷ 2. On a cumulative frequency graph you read across from that position. And counting people up as you move along the line is exactly <strong>cumulative frequency</strong>."}
  ]
 },
 "teach": {
  "bronze": {
   "display": "Frequencies for four classes: 6, 10, 9, 5. Build the cumulative frequency, then find the median position.",
   "label": "Together: your first one",
   "steps": [
    {"say": "Cumulative frequency is a running total. Start at the first class and keep adding.",
     "pre": "After class 1: 0 + 6 = ", "post": "", "answer": 6, "hint": "Start from zero and add the first frequency."},
    {"pre": "After class 2: 6 + 10 = ", "post": "", "answer": 16, "hint": "Add the second frequency to your total."},
    {"pre": "After class 3: 16 + 9 = ", "post": "", "answer": 25, "hint": "Add the third frequency."},
    {"pre": "After class 4: 25 + 5 = ", "post": "", "answer": 30, "hint": "Add the last frequency; this total is n."},
    {"say": "The full total is n = 30.", "pre": "Median position = n ÷ 2 = 30 ÷ 2 = ", "post": "", "answer": 15, "done": "Position 15 is where you read the median off the curve. Running total, then halve: that is the whole bronze move.", "hint": "Halve the total."}
   ]
  },
  "silver": {
   "display": "One histogram bar covers 20 to 40 with frequency 50. Another covers 0 to 10 with frequency density 4. Work frequency density one way, then frequency the other.",
   "label": "Together: the silver move",
   "steps": [
    {"say": "Frequency density shares the frequency across the width: density = frequency ÷ width. It also runs backwards.",
     "pre": "Width of 20 to 40: 40 − 20 = ", "post": "", "answer": 20, "hint": "Top minus bottom."},
    {"pre": "Frequency density of 20 to 40 = 50 ÷ 20 = ", "post": "", "answer": 2.5, "hint": "Frequency divided by width."},
    {"say": "Now backwards: given a density, find a frequency.", "pre": "Width of 0 to 10: 10 − 0 = ", "post": "", "answer": 10, "hint": "Top minus bottom."},
    {"pre": "Frequency of 0 to 10 = density × width = 4 × 10 = ", "post": "", "answer": 40, "done": "Density divides, frequency multiplies. That two-way move is the silver skill.", "hint": "Multiply density by width."}
   ]
  },
  "gold": {
   "display": histogram_svg([(0, 10, 1.5), (10, 30, 2), (30, 60, 1)], 0, 60, 2,
     "Histogram with three bars of unequal width: 0 to 10 at frequency density 1.5, 10 to 30 at 2, and 30 to 60 at 1") + CAP +
     "A histogram has classes 0-10 (FD 1.5), 10-30 (FD 2) and 30-60 (FD 1). Find the total frequency.",
   "label": "Together: the gold move",
   "steps": [
    {"say": "With unequal widths, each frequency is density × its own width. Then add.",
     "pre": "Class 0 to 10 (width 10): 1.5 × 10 = ", "post": "", "answer": 15, "hint": "Density times width."},
    {"pre": "Class 10 to 30 (width 20): 2 × 20 = ", "post": "", "answer": 40, "hint": "Width is 30 − 10 = 20."},
    {"pre": "Class 30 to 60 (width 30): 1 × 30 = ", "post": "", "answer": 30, "hint": "Width is 60 − 30 = 30."},
    {"pre": "Total frequency = 15 + 40 + 30 = ", "post": "", "answer": 85, "done": "The wide middle bar contributes most because it is 20 across. Watching the widths is the gold move.", "hint": "Add the three frequencies."}
   ]
  }
 }
}

# ---------- method_card (slim, <=4 steps) ----------
method_card = {
 "title": "Cumulative Frequency, Box Plots & Histograms",
 "steps": [
  "Cumulative frequency: keep a running total; plot each total at the top of its class.",
  "Median at n ÷ 2, Q1 at n ÷ 4, Q3 at 3n ÷ 4; read across the curve, then down.",
  "Box plot shows min, Q1, median, Q3, max. IQR = Q3 − Q1, range = max − min.",
  "Histogram: frequency density = frequency ÷ class width; frequency = area of the bar."
 ],
 "content": "<p><strong>Cumulative frequency</strong> is a running total of frequencies, plotted at the upper class boundary. Read the median across from ½n, Q1 from ¼n and Q3 from ¾n.</p><p>A <strong>box plot</strong> shows min, Q1, median, Q3 and max. IQR = Q3 − Q1; range = max − min.</p><p>On a <strong>histogram</strong>, frequency density = frequency ÷ class width, and the area of each bar equals its frequency.</p>",
 "example": "<p><strong>Class 10 to 20, frequency 15, width 10.</strong></p><p>Frequency density = 15 ÷ 10 = 1.5.</p>"
}

# ---------- assemble, preserving untouched fields ----------
live = json.load(io.open("_L05ocr_livefresh.json", encoding="utf-8"))
out = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": bank,
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": live.get("related_videos", []),
 "worked_examples": live.get("worked_examples", [])
}

with io.open("lesson_maths-ocr_probability-statistics-L05.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written. sizes:", {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in out.items() if k in ("related_videos", "worked_examples")})
print("em dash present:", "—" in json.dumps(out, ensure_ascii=False))
