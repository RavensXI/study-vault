# -*- coding: utf-8 -*-
"""Guided-learning + diagrams conversion: maths-eduqas probability-statistics-L05
Cumulative Frequency, Box Plots & Histograms."""
import json, io

live = json.load(io.open("_L05e_live.json", encoding="utf-8"))
pd = live["practice_data"]

# ---------------------------------------------------------------- SVG helpers
def boxplot_svg(mn, q1, med, q3, mx, amin, amax, step, axis_label, aria):
    W = 260; x0 = 18; x1 = 242; span = x1 - x0
    X = lambda v: x0 + (v - amin) / (amax - amin) * span
    ycen = 32; bh = 22; ytop = ycen - bh / 2; ybot = ycen + bh / 2; ax = 60
    p = ['<svg viewBox="0 0 %d 82" role="img" aria-label="%s">' % (W, aria)]
    p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (X(mn), ycen, X(q1), ycen))
    p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (X(q3), ycen, X(mx), ycen))
    for v in (mn, mx):
        p.append('<line x1="%.1f" y1="%.0f" x2="%.1f" y2="%.0f" stroke="currentColor" stroke-width="1.2"/>' % (X(v), ytop + 4, X(v), ybot - 4))
    p.append('<rect x="%.1f" y="%.0f" width="%.1f" height="%d" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>' % (X(q1), ytop, X(q3) - X(q1), bh))
    p.append('<line x1="%.1f" y1="%.0f" x2="%.1f" y2="%.0f" stroke="currentColor" stroke-width="1.6"/>' % (X(med), ytop, X(med), ybot))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x0, ax, x1, ax))
    v = amin
    while v <= amax + 1e-9:
        p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1"/>' % (X(v), ax, X(v), ax + 4))
        lab = str(int(v)) if v == int(v) else str(v)
        p.append('<text x="%.1f" y="%d" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">%s</text>' % (X(v), ax + 14, lab))
        v += step
    p.append('<text x="%d" y="80" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">%s</text>' % (W // 2, axis_label))
    p.append('</svg>')
    return ''.join(p)

def hist_svg(bars, amin, amax, fd_max, axis_label, aria, marks=None):
    W = 260; x0 = 24; x1 = 246; span = x1 - x0
    ybase = 60; ytop = 8; hspan = ybase - ytop
    X = lambda v: x0 + (v - amin) / (amax - amin) * span
    Y = lambda fd: ybase - (fd / fd_max) * hspan
    p = ['<svg viewBox="0 0 %d 82" role="img" aria-label="%s">' % (W, aria)]
    for lo, hi, fd in bars:
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>' % (X(lo), Y(fd), X(hi) - X(lo), ybase - Y(fd)))
    for m in (marks or []):
        p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="3 2"/>' % (X(m), ytop, X(m), ybase))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x0, ytop, x0, ybase))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x0, ybase, x1, ybase))
    fd = 0
    while fd <= fd_max + 1e-9:
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (x0 - 3, Y(fd), x0, Y(fd)))
        lab = str(int(fd)) if fd == int(fd) else str(fd)
        p.append('<text x="%d" y="%.1f" font-family="Inter, sans-serif" font-size="8" text-anchor="end" fill="currentColor">%s</text>' % (x0 - 5, Y(fd) + 3, lab))
        fd += 1
    xs = sorted(set([b[0] for b in bars] + [b[1] for b in bars] + (marks or [])))
    for v in xs:
        p.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1"/>' % (X(v), ybase, X(v), ybase + 3))
        p.append('<text x="%.1f" y="%d" font-family="Inter, sans-serif" font-size="8" text-anchor="middle" fill="currentColor">%d</text>' % (X(v), ybase + 12, int(v)))
    p.append('<text x="%d" y="80" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">%s</text>' % ((x0 + x1) // 2, axis_label))
    p.append('</svg>')
    return ''.join(p)

def strip_svg(nums, hi_idx, aria):
    W = 260; cw = 26; x0 = 8; y = 24; ch = 30
    p = ['<svg viewBox="0 0 %d 74" role="img" aria-label="%s">' % (W, aria)]
    for i, n in enumerate(nums):
        x = x0 + i * cw
        fill = '#60a5fa' if i == hi_idx else 'none'
        op = '0.3' if i == hi_idx else '1'
        p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" fill-opacity="%s" stroke="currentColor" stroke-width="1"/>' % (x, y, cw, ch, fill, op))
        p.append('<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="11" text-anchor="middle" fill="currentColor">%d</text>' % (x + cw // 2, y + 20, n))
    p.append('<text x="%d" y="16" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">Nine scores, smallest to largest</text>' % (x0 + 9 * cw // 2))
    p.append('<text x="%d" y="68" font-family="Inter, sans-serif" font-size="9" text-anchor="middle" fill="currentColor">middle</text>' % (x0 + hi_idx * cw + cw // 2))
    p.append('</svg>')
    return ''.join(p)

# ---------------------------------------------------------------- worked_examples: preserve, strip any em dash in labels
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------------------------------------------------------------- method_card (slim)
pd["method_card"] = {
    "title": "Cumulative Frequency, Box Plots & Histograms",
    "steps": [
        "Cumulative frequency: running totals plotted at the upper class boundary, joined with a smooth curve.",
        "Read the median at n/2, Q1 at n/4, Q3 at 3n/4; IQR = Q3 − Q1.",
        "Box plot: min, Q1, median, Q3, max. Range = max − min.",
        "Histogram: frequency = frequency density × class width.",
    ],
    "content": "<p>Cumulative frequency is a running total, plotted at the upper class boundary and joined with a smooth curve. Read the median at n/2, Q1 at n/4 and Q3 at 3n/4; IQR = Q3 − Q1.</p><p>A box plot shows five numbers: minimum, Q1, median, Q3 and maximum. In a histogram, frequency density = frequency ÷ class width, so frequency = density × width, and the area of a bar equals its frequency.</p>",
    "example": "<p><strong>Box plot: min 15, Q1 25, median 35, Q3 50, max 70.</strong></p><p>IQR = 50 − 25 = 25. Range = 70 − 15 = 55.</p>",
}

pb = pd["problem_bank"]
pb["bronze_description"] = "Read one value from a box plot or cumulative frequency curve, or do a single frequency density step."
pb["silver_description"] = "Take two steps: frequencies from a histogram, differences from a cumulative frequency curve, or an IQR."
pb["gold_description"] = "Estimate across parts of bars, work with percentiles, find modal or median classes, and compare distributions."

def M(pattern, expect, message, note=""):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

# ---------------------------------------------------------------- FIX B4 chart so Q1 reads exactly 10
pb["bronze"][3]["chart"]["data"]["datasets"][0]["data"] = [0, 8, 20, 48, 64, 74, 80]

# ---------------------------------------------------------------- FIX B8: re-pose so answer (22) is unique in tier (was 20, clashing with B6)
pb["bronze"][7]["display"] = "A box plot has Q1 = 28 and Q3 = 50. Find the IQR."
pb["bronze"][7]["solutions"] = [22]

# ============================ BRONZE guided ============================
bronze = [
    # B1 median from CF (60 students) = 45
    {"hint": "The median is at n/2. Read across from that cumulative frequency to the curve, then down.",
     "misc": [M("read_cf_axis", 30, "30 is the cumulative frequency you read across at, not the score. Go down to the x-axis: the median is about 45.", "reports n/2 not the value")],
     "steps": [
        {"say": "The median splits the data in half. Find the halfway position first.", "pre": "n ÷ 2 = 60 ÷ 2 = ", "post": "", "answer": 30, "hint": "Halve the total number of students."},
        {"say": "Go up from cumulative frequency 30 to the curve, then read down to the score axis.", "phase": "substitute", "pre": "The median score is about ", "post": "", "answer": 45, "hint": "Trace across at 30, then straight down."},
        {"phase": "substitute", "pre": "Check: students scoring above the median = 60 − 30 = ", "post": "", "answer": 30, "done": "30 below and 30 above confirms 45 is the middle.", "hint": "Half of 60 sit each side."},
     ]},
    # B2 IQR from box plot = 25
    {"hint": "IQR is the width of the box: upper quartile minus lower quartile.",
     "misc": [M("range_not_iqr", 55, "55 is the range (max − min). The IQR is the box width: Q3 − Q1 = 55 − 30 = 25.", "gives range")],
     "steps": [
        {"say": "The IQR measures the middle 50%: the width of the box.", "pre": "Read the upper quartile Q3 = ", "post": "", "answer": 55, "hint": "The right-hand edge of the box."},
        {"say": "Now the lower quartile.", "phase": "substitute", "pre": "Read the lower quartile Q1 = ", "post": "", "answer": 30, "hint": "The left-hand edge of the box."},
        {"phase": "substitute", "pre": "IQR = Q3 − Q1 = 55 − 30 = ", "post": "", "answer": 25, "hint": "Subtract the two quartiles."},
        {"pre": "Check it is smaller than the range: max − min = 75 − 20 = ", "post": "", "answer": 55, "done": "55 is the range; the box (IQR 25) is smaller, as it must be. Correct.", "hint": "The whole spread is bigger than the box."},
     ]},
    # B3 median from box plot = 24
    {"hint": "The median is the line inside the box, not the midpoint of the box.",
     "misc": [M("box_midpoint", 25, "25 is the midpoint of the box, (18 + 32) ÷ 2. The median is the line actually drawn inside: 24.", "averages the edges")],
     "steps": [
        {"say": "Do not average the edges: the median is a drawn line.", "pre": "Read the left edge, Q1 = ", "post": "", "answer": 18, "hint": "Lower quartile, left edge of the box."},
        {"say": "Now the line inside the box.", "phase": "substitute", "pre": "Read the median line = ", "post": "", "answer": 24, "hint": "The line between the two box edges."},
        {"phase": "substitute", "pre": "The box midpoint would be (18 + 32) ÷ 2 = ", "post": "", "answer": 25, "done": "The median (24) is the drawn line, not the box midpoint (25). Read the line.", "hint": "Average the edges to see they differ."},
     ]},
    # B4 Q1 from CF (80 patients) = 10 (chart fixed)
    {"hint": "Q1 is at n/4. Read across from that cumulative frequency to the curve, then down.",
     "misc": [M("read_cf_axis", 20, "20 is the cumulative frequency (n ÷ 4) you read across at, not the time. Read down to the axis: Q1 is about 10 minutes.", "reports n/4 not the value")],
     "steps": [
        {"say": "Q1 is a quarter of the way through the data. Find the quarter position.", "pre": "n ÷ 4 = 80 ÷ 4 = ", "post": "", "answer": 20, "hint": "Divide the total by 4."},
        {"say": "Go up from cumulative frequency 20 to the curve, then down to the time axis.", "phase": "substitute", "pre": "Q1 is about ", "post": " minutes", "answer": 10, "hint": "Trace across at 20, then straight down."},
        {"phase": "substitute", "pre": "Check: a quarter of the 80 patients is ", "post": "", "answer": 20, "done": "20 patients (a quarter) waited under 10 minutes, confirming Q1.", "hint": "A quarter of 80."},
     ]},
    # B5 range from box plot = 30
    {"hint": "Range is the full spread: maximum minus minimum.",
     "misc": [M("iqr_not_range", 15, "15 is the IQR (Q3 − Q1, the box width). The range is the whole spread: max − min = 40 − 10 = 30.", "gives iqr")],
     "steps": [
        {"say": "The range is the full spread, from smallest to largest.", "pre": "Read the maximum (right whisker end) = ", "post": "", "answer": 40, "hint": "The far right point."},
        {"say": "Now the smallest value.", "phase": "substitute", "pre": "Read the minimum (left whisker end) = ", "post": "", "answer": 10, "hint": "The far left point."},
        {"phase": "substitute", "pre": "Range = max − min = 40 − 10 = ", "post": "", "answer": 30, "hint": "Subtract the smallest from the largest."},
        {"pre": "The IQR would be Q3 − Q1 = 30 − 15 = ", "post": "", "answer": 15, "done": "15 is the IQR (the box); the range (30) is the whole spread. Correct.", "hint": "Compare with the box width."},
     ]},
    # B6 freq = FD x width = 20
    {"hint": "Frequency is the bar's area: frequency density times class width.",
     "misc": [M("fd_as_freq", 5, "5 is the frequency density (the bar height). Multiply by the class width: 5 × 4 = 20.", "forgets x width")],
     "steps": [
        {"say": "In a histogram, frequency is the area of the bar: density times width.", "pre": "Write the frequency density: FD = ", "post": "", "answer": 5, "hint": "Given in the question."},
        {"say": "And the width of the class.", "phase": "substitute", "pre": "Class width = ", "post": "", "answer": 4, "hint": "Given in the question."},
        {"phase": "substitute", "pre": "Frequency = FD × width = 5 × 4 = ", "post": "", "answer": 20, "hint": "Multiply density by width."},
        {"pre": "Check by reversing: 20 ÷ 4 = ", "post": "", "answer": 5, "done": "Dividing the frequency by the width gives back FD = 5. Correct.", "hint": "Frequency ÷ width returns the density."},
     ]},
    # B7 FD = freq / width = 3
    {"hint": "Frequency density = frequency divided by class width.",
     "misc": [M("multiply_not_divide", 192, "192 multiplies instead of dividing. FD = frequency ÷ width = 24 ÷ 8 = 3.", "24*8")],
     "steps": [
        {"say": "Frequency density undoes the area: divide the frequency by the class width.", "pre": "Write the frequency = ", "post": "", "answer": 24, "hint": "The number of items, given."},
        {"say": "And the width of the class.", "phase": "substitute", "pre": "Class width = ", "post": "", "answer": 8, "hint": "Given in the question."},
        {"phase": "substitute", "pre": "FD = frequency ÷ width = 24 ÷ 8 = ", "post": "", "answer": 3, "hint": "Divide frequency by width."},
        {"pre": "Check by reversing: 3 × 8 = ", "post": "", "answer": 24, "done": "Density times width returns the frequency 24. Correct.", "hint": "FD × width should give the frequency back."},
     ]},
    # B8 IQR = Q3 - Q1 = 22
    {"hint": "IQR is the gap between the quartiles: Q3 minus Q1.",
     "misc": [M("added_quartiles", 78, "78 adds the quartiles. The IQR subtracts them: Q3 − Q1 = 50 − 28 = 22.", "50+28")],
     "steps": [
        {"say": "The IQR is the gap between the two quartiles.", "pre": "Upper quartile Q3 = ", "post": "", "answer": 50, "hint": "Given."},
        {"say": "And the lower quartile.", "phase": "substitute", "pre": "Lower quartile Q1 = ", "post": "", "answer": 28, "hint": "Given."},
        {"phase": "substitute", "pre": "IQR = Q3 − Q1 = 50 − 28 = ", "post": "", "answer": 22, "hint": "Subtract Q1 from Q3."},
        {"pre": "Check: Q1 + IQR = 28 + 22 = ", "post": "", "answer": 50, "done": "Adding the IQR back to Q1 returns Q3 = 50. Correct.", "hint": "Q1 plus the IQR should give Q3."},
     ]},
]

# ============================ SILVER guided ============================
silver = [
    # S1 MC consistency (idx 0) - no guided_steps
    {"hint": "More consistent means a smaller interquartile range (a narrower box).",
     "misc": [M("bigger_iqr", None, "Consistent means less spread. Year 10's IQR is 55 − 40 = 15; Year 11's is 65 − 30 = 35. The smaller IQR (Year 10) is more consistent.", "picks wider box")]},
    # S2 CF between 30 and 60 (120) = 60
    {"hint": "Read the cumulative frequency at each end, then subtract the smaller from the larger.",
     "misc": [M("no_subtract", 78, "78 is the number up to 60. Subtract those up to 30 (18): 78 − 18 = 60.", "forgets to subtract")],
     "steps": [
        {"say": "Count how many fall below each end, then subtract.", "pre": "Read the cumulative frequency at 60 = ", "post": "", "answer": 78, "hint": "Up from 60 to the curve, across to the CF axis."},
        {"say": "Now the lower end.", "phase": "substitute", "pre": "Read the cumulative frequency at 30 = ", "post": "", "answer": 18, "hint": "Up from 30 to the curve, across."},
        {"phase": "substitute", "pre": "Between 30 and 60 = 78 − 18 = ", "post": "", "answer": 60, "hint": "Subtract the lower count from the higher."},
        {"pre": "Check: 60 out of 120 is 60 ÷ 120 = ", "post": "", "answer": 0.5, "done": "Half the students fall in this middle band, which matches the curve. Correct.", "hint": "Divide by the total of 120."},
     ]},
    # S3 histogram freq 10-20 = 40
    {"hint": "Frequency is height times width, not just the height.",
     "misc": [M("read_height", 4, "4 is the frequency density (the bar height). Multiply by the class width: 4 × 10 = 40.", "reads height only")],
     "steps": [
        {"say": "Frequency is the bar's area: height times width, not just the height.", "pre": "Read the bar height (frequency density) = ", "post": "", "answer": 4, "hint": "The top of the 10 to 20 bar."},
        {"say": "Now the width of that class.", "phase": "substitute", "pre": "Class width = 20 − 10 = ", "post": "", "answer": 10, "hint": "Upper minus lower boundary."},
        {"phase": "substitute", "pre": "Frequency = FD × width = 4 × 10 = ", "post": "", "answer": 40, "hint": "Multiply height by width."},
        {"pre": "Check: 40 ÷ 10 = ", "post": "", "answer": 4, "done": "Dividing back by the width returns the density 4. Correct.", "hint": "Frequency ÷ width returns the height."},
     ]},
    # S4 IQR from Q1,med,Q3 = 27
    {"hint": "IQR uses only the quartiles: Q3 minus Q1. Ignore the median.",
     "misc": [M("used_median", 14, "14 subtracts the median (Q3 − median). The IQR uses the quartiles: Q3 − Q1 = 62 − 35 = 27.", "62-48")],
     "steps": [
        {"say": "The IQR uses only the two quartiles, not the median.", "pre": "Upper quartile Q3 = ", "post": "", "answer": 62, "hint": "Given."},
        {"say": "And the lower quartile.", "phase": "substitute", "pre": "Lower quartile Q1 = ", "post": "", "answer": 35, "hint": "Given."},
        {"phase": "substitute", "pre": "IQR = Q3 − Q1 = 62 − 35 = ", "post": "", "answer": 27, "hint": "Subtract Q1 from Q3, ignore the median."},
        {"pre": "Check: Q1 + IQR = 35 + 27 = ", "post": "", "answer": 62, "done": "Q1 plus the IQR returns Q3 = 62. Correct.", "hint": "35 + 27 should give Q3."},
     ]},
    # S5 total frequency = 100
    {"hint": "Turn each density into a frequency (density times width), then add them all.",
     "misc": [M("added_fd", 13, "13 adds the frequency densities. Add the frequencies (density × width): 15 + 25 + 40 + 20 = 100.", "3+5+4+1")],
     "steps": [
        {"say": "Turn each density into a frequency (density times width), then add.", "pre": "0 to 5: 3 × 5 = ", "post": "", "answer": 15, "hint": "Density times width for the first bar."},
        {"say": "The second bar.", "pre": "5 to 10: 5 × 5 = ", "post": "", "answer": 25, "hint": "Density times width."},
        {"say": "The third bar is wider: width 10.", "phase": "substitute", "pre": "10 to 20: 4 × 10 = ", "post": "", "answer": 40, "hint": "Density times a width of 10."},
        {"pre": "The fourth bar, width 20: 1 × 20 = ", "post": "", "answer": 20, "hint": "Density times a width of 20."},
        {"pre": "Total = 15 + 25 + 40 + 20 = ", "post": "", "answer": 100, "done": "The four bars represent 100 items in total (the area under the histogram).", "hint": "Add the four frequencies."},
     ]},
    # S6 MC compare (idx 0) - no guided_steps
    {"hint": "Higher average means a bigger median; more consistent means a smaller IQR.",
     "misc": [M("wrong_compare", None, "A's median (60) beats B's (55), so A has the higher average; A's IQR (15) is smaller than B's (25), so A is more consistent too.", "misreads which is better")]},
    # S7 above 70 = 50
    {"hint": "The cumulative frequency counts values below. Those above = total minus that count.",
     "misc": [M("gave_cf", 150, "150 is the number up to 70. Those above 70 = total − 150 = 200 − 150 = 50.", "reports cf")],
     "steps": [
        {"say": "The cumulative frequency tells you how many are below a value. Above it is the rest.", "pre": "How many are at most 70? CF = ", "post": "", "answer": 150, "hint": "Given in the question."},
        {"say": "And the total number of data points.", "phase": "substitute", "pre": "The total is ", "post": "", "answer": 200, "hint": "Given: 200 data points."},
        {"phase": "substitute", "pre": "Above 70 = total − CF = 200 − 150 = ", "post": "", "answer": 50, "hint": "Subtract the cumulative frequency from the total."},
        {"pre": "Check: 150 + 50 = ", "post": "", "answer": 200, "done": "Below plus above adds back to the total 200. Correct.", "hint": "The two parts should give the total."},
     ]},
]

# ============================ GOLD guided ============================
gold = [
    # G1 histogram estimate 15-25 = 35 (calculator true)
    {"hint": "15 to 25 cuts across two bars. Take the matching fraction of each bar's width.",
     "misc": [M("whole_bars", 70, "70 uses the whole 10 to 20 and 20 to 30 bars. Only half of each lies in 15 to 25: 4 × 5 + 3 × 5 = 35.", "4*10+3*10")],
     "steps": [
        {"say": "15 to 25 crosses two bars, so take half of each.", "pre": "15 to 20 is half of the 10 to 20 bar: FD 4 × width 5 = ", "post": "", "answer": 20, "hint": "Density 4 times the 5-year width."},
        {"say": "Now the second part.", "phase": "substitute", "pre": "20 to 25 is half of the 20 to 30 bar: FD 3 × width 5 = ", "post": "", "answer": 15, "hint": "Density 3 times the 5-year width."},
        {"phase": "substitute", "pre": "Total aged 15 to 25 = 20 + 15 = ", "post": "", "answer": 35, "hint": "Add the two part-bars."},
        {"pre": "The whole 10 to 20 bar would be 4 × 10 = ", "post": "", "answer": 40, "done": "The full bar is 40; we used only half (20), which is why we split. About 35 visitors. Correct.", "hint": "Full bar would be 40, we used half."},
     ]},
    # G2 pass mark = 30 (calculator false)
    {"hint": "80% pass means 20% fail. Find the score where the cumulative frequency reaches those 20 students.",
     "misc": [M("used_80pc", None, "80% pass, so 20% (20 students) fail. The pass mark is where CF = 20, giving 30. Reading at CF = 80 finds the top-20% boundary, not the pass mark.", "reads cf=80")],
     "steps": [
        {"say": "80% pass, so the pass mark sits above the bottom 20% who fail. Turn 20% into a number of students.", "pre": "20% of 100 students = ", "post": "", "answer": 20, "hint": "A fifth of 100."},
        {"say": "Find the score where the cumulative frequency reaches 20 (the 20 who fail sit below it).", "phase": "substitute", "pre": "Reading up from CF = 20, the score is ", "post": "", "answer": 30, "hint": "Across at 20, down to the score axis."},
        {"phase": "substitute", "pre": "Check: how many of the 100 are above 30? 100 − 20 = ", "post": "", "answer": 80, "done": "80 students (80%) score above 30, so 30 is the pass mark.", "hint": "Total minus the 20 who fail."},
     ]},
    # G3 MC modal class (idx 0) - no guided_steps
    {"hint": "The modal class has the highest frequency density (tallest bar), not the highest frequency.",
     "misc": [M("highest_freq", None, "With unequal classes the modal class is the highest frequency density, not frequency. FD = 8 in 25 to 30 is tallest.", "picks widest or highest freq")]},
    # G4 MC median class (idx 0) - no guided_steps
    {"hint": "Work out each frequency (density times width), then find which class holds the middle value.",
     "misc": [M("wrong_class", None, "Frequencies are 3×20 = 60, 5×10 = 50, 2×20 = 40; total 150, so the median is the 75th value. Cumulative: 60, then 110, so the 75th lies in 20 to 30.", "reads tallest bar")]},
    # G5 boxplot median difference = 15
    {"hint": "Compare the medians (the line inside each box) and subtract.",
     "misc": [M("used_quartile", 10, "10 compares the upper quartiles (60 − 50). The question asks about the medians: 50 − 35 = 15.", "q3 diff")],
     "steps": [
        {"say": "Compare the medians: the line inside each box.", "pre": "Group A median = ", "post": "", "answer": 35, "hint": "The line in box A."},
        {"say": "Now Group B.", "phase": "substitute", "pre": "Group B median = ", "post": "", "answer": 50, "hint": "The line in box B."},
        {"phase": "substitute", "pre": "B exceeds A by 50 − 35 = ", "post": "", "answer": 15, "hint": "Subtract A's median from B's."},
        {"pre": "Check: A's median + 15 = 35 + 15 = ", "post": "", "answer": 50, "done": "Adding 15 to A's median gives B's median. Correct.", "hint": "35 + 15 should equal B's median."},
     ]},
]

def apply(specs, probs):
    for spec, prob in zip(specs, probs):
        prob["hint"] = spec["hint"]
        prob["misconceptions"] = spec["misc"]
        if "steps" in spec:
            prob["guided_steps"] = spec["steps"]

apply(bronze, pb["bronze"])
apply(silver, pb["silver"])
apply(gold, pb["gold"])

# ---------------------------------------------------------------- ADD figures to G3, G4, S5 (histograms described in text)
def bar_chart(labels, data, xlabel, colour="#3b82f6"):
    return {
        "type": "bar",
        "data": {"labels": labels, "datasets": [{"data": data, "borderColor": colour, "borderWidth": 1, "backgroundColor": "rgba(59,130,246,0.4)"}]},
        "options": {"scales": {
            "x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": xlabel, "display": True}},
            "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": 1}, "title": {"text": "Frequency density", "display": True}, "beginAtZero": True},
        }},
    }

pb["gold"][2]["chart"] = bar_chart(["0-10", "10-25", "25-30", "30-50"], [2, 4, 8, 1.5], "Value")
pb["gold"][3]["chart"] = bar_chart(["0-20", "20-30", "30-50"], [3, 5, 2], "Value")
pb["silver"][4]["chart"] = bar_chart(["0-5", "5-10", "10-20", "20-40"], [3, 5, 4, 1], "Value")

# ============================ tier_guides ============================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: read a single value from a chart",
        "steps": [
            "On a box plot, five marks show the minimum, lower quartile Q1, median, upper quartile Q3 and maximum. The <strong>median</strong> is the line inside the box.",
            "<strong>Range</strong> = max − minimum. <strong>IQR</strong> = Q3 − Q1, the width of the box.",
            "On a cumulative frequency curve, read the median at n/2, Q1 at n/4 and Q3 at 3n/4: up to the curve, then down to the value.",
            "In a histogram, frequency = frequency density × class width.",
        ],
        "example": {
            "question": "A box plot shows min 4, Q1 12, median 18, Q3 26, max 34. Find the IQR.",
            "steps": [
                {"label": "Q3", "content": "<p>Q3 = 26</p>"},
                {"label": "Q1", "content": "<p>Q1 = 12</p>"},
                {"label": "Subtract", "content": "<p>IQR = 26 − 12 = 14</p>"},
                {"label": "Check", "content": "<p>The box (14) is narrower than the range (30) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>14</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two steps to an answer",
        "steps": [
            "Histogram frequency: multiply the bar's density by its class width. Add several bars to get a total frequency.",
            "Cumulative frequency between two values: read the CF at each end and subtract the smaller from the larger.",
            "IQR uses the quartiles only: Q3 − Q1. The median sits between them but is not used.",
        ],
        "example": {
            "question": "A histogram bar spans 20 to 40 with frequency density 3. Find the frequency.",
            "steps": [
                {"label": "Width", "content": "<p>Width = 40 − 20 = 20</p>"},
                {"label": "Frequency", "content": "<p>3 × 20 = 60</p>"},
                {"label": "Check", "content": "<p>60 ÷ 20 = 3, back to the density ✓</p>"},
                {"label": "Answer", "content": "<p><strong>60</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: estimate and interpret",
        "steps": [
            "Part of a histogram bar: take the fraction of the width you need. For 15 to 25 across bars of width 10, use 5 out of 10 of each bar's frequency.",
            "Percentiles on a CF curve: 'top 20% pass' means 80% of students sit below the pass mark. Find the matching CF, then read the value.",
            "Modal class = highest frequency <strong>density</strong> (tallest bar), not highest frequency. Compare distributions by median (average) and IQR (consistency).",
        ],
        "example": {
            "question": "A histogram: 0-20 (FD 3), 20-30 (FD 5), 30-50 (FD 2). Find the modal class.",
            "steps": [
                {"label": "Densities", "content": "<p>Bar heights: 3, 5, 2</p>"},
                {"label": "Tallest", "content": "<p>Highest density is 5</p>"},
                {"label": "Check", "content": "<p>Frequencies 60, 50, 40 do not decide it; density does ✓</p>"},
                {"label": "Answer", "content": "<p><strong>20-30</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ============================ guided (opener + teach) ============================
opener_svg = strip_svg([3, 5, 6, 8, 10, 12, 15, 18, 20], 4,
    "Nine test scores in order from 3 to 20 with the middle value 10 highlighted")

teach_b_svg = boxplot_svg(10, 15, 25, 35, 45, 0, 50, 5, "Score",
    "Box plot with minimum 10, lower quartile 15, median 25, upper quartile 35 and maximum 45")
teach_s_svg = hist_svg([(0, 10, 2), (10, 20, 5), (20, 40, 1.5)], 0, 40, 5, "Time (minutes)",
    "Histogram with bars 0 to 10 density 2, 10 to 20 density 5, 20 to 40 density 1.5")
teach_g_svg = hist_svg([(0, 10, 3), (10, 20, 5), (20, 40, 2)], 0, 40, 5, "Length (cm)",
    "Histogram with bars 0 to 10 density 3, 10 to 20 density 5, 20 to 40 density 2, dashed lines at 5 and 25", marks=[5, 25])

pd["guided"] = {
    "opener": {
        "label": "Before any formulas",
        "display": opener_svg,
        "steps": [
            {"say": "Nine test scores are lined up smallest to largest. No formulas, just point.",
             "pre": "Which score is right in the middle, with four on each side? ", "post": "", "answer": 10,
             "hint": "Count in from both ends until you meet in the middle."},
            {"say": "That middle value is the <strong>median</strong>. Now look only at the lower four: 3, 5, 6, 8.",
             "pre": "Halfway between the middle two of those (6 and 8) is ", "post": "", "answer": 7,
             "hint": "The value exactly between 6 and 8."},
            {"say": "You just found the <strong>median</strong> (the middle) and the <strong>lower quartile</strong> Q1 (the middle of the bottom half). The upper quartile Q3 is the middle of the top half. A <strong>box plot</strong> draws these five markers; a <strong>cumulative frequency curve</strong> finds them for hundreds of values by reading at n/2, n/4 and 3n/4. That is this whole lesson."},
        ],
    },
    "teach": {
        "bronze": {
            "display": teach_b_svg + "Read the five-number summary from this box plot: median, Q1, Q3, then the IQR and range. <span class=\"figure-caption\">Read each value off the scale.</span>",
            "label": "Together: your first one",
            "steps": [
                {"say": "The median is the line inside the box.", "pre": "Read the median line = ", "post": "", "answer": 25, "hint": "The line splitting the box."},
                {"say": "Now the left edge.", "pre": "Read the lower quartile Q1 = ", "post": "", "answer": 15, "hint": "Left edge of the box."},
                {"say": "And the right edge.", "pre": "Read the upper quartile Q3 = ", "post": "", "answer": 35, "hint": "Right edge of the box."},
                {"say": "IQR is the width of the box.", "pre": "IQR = Q3 − Q1 = 35 − 15 = ", "post": "", "answer": 20, "hint": "Q3 minus Q1."},
                {"say": "Range is whisker tip to whisker tip.", "pre": "Range = max − min = 45 − 10 = ", "post": "", "answer": 35, "done": "Median 25, IQR 20, range 35, all read straight off the plot. That is the bronze skill.", "hint": "Max minus min."},
            ],
        },
        "silver": {
            "display": teach_s_svg + "This histogram has unequal class widths. Find the total frequency (frequency = density × width for each bar, then add). <span class=\"figure-caption\">Areas, not heights, give the frequencies.</span>",
            "label": "Together: the silver move",
            "steps": [
                {"say": "First bar, 0 to 10: frequency = density × width.", "pre": "2 × 10 = ", "post": "", "answer": 20, "hint": "Density 2 times width 10."},
                {"say": "Second bar, 10 to 20.", "pre": "5 × 10 = ", "post": "", "answer": 50, "hint": "Density 5 times width 10."},
                {"say": "Third bar, 20 to 40, is wider: width 20.", "pre": "1.5 × 20 = ", "post": "", "answer": 30, "hint": "Density 1.5 times width 20."},
                {"say": "Add the three frequencies.", "pre": "20 + 50 + 30 = ", "post": "", "answer": 100, "done": "The bars hold 100 items altogether. Density times width for each bar, then add, is the silver skill.", "hint": "Sum the three."},
            ],
        },
        "gold": {
            "display": teach_g_svg + "Estimate how many items are between 5 and 25 (dashed lines). Take the fraction of each bar's width that falls in the range. <span class=\"figure-caption\">Split the end bars by width.</span>",
            "label": "Together: the gold move",
            "steps": [
                {"say": "5 to 10 is half of the first bar (width 5).", "pre": "FD 3 × 5 = ", "post": "", "answer": 15, "hint": "Density 3 times 5."},
                {"say": "10 to 20 is the whole second bar.", "pre": "FD 5 × 10 = ", "post": "", "answer": 50, "hint": "Density 5 times 10."},
                {"say": "20 to 25 is a quarter of the third bar (width 5).", "pre": "FD 2 × 5 = ", "post": "", "answer": 10, "hint": "Density 2 times 5."},
                {"say": "Add the parts.", "pre": "15 + 50 + 10 = ", "post": "", "answer": 75, "done": "About 75 items lie between 5 and 25. Splitting part-bars by width, then adding, is the gold skill.", "hint": "Sum the three parts."},
            ],
        },
    },
}

json.dump(pd, io.open("lesson_maths-eduqas_probability-statistics-L05.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written shard")
