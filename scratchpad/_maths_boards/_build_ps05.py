# -*- coding: utf-8 -*-
import json, io, copy

SUB = "−"   # minus sign
DIV = "÷"
MUL = "×"

def box(pre, answer, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    d.update(kw)
    return d

def say(text, **kw):
    d = {"say": text}; d.update(kw); return d

pd = json.load(io.open("_live_ps05.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---------- 1. correctness fix: bronze[3] Q1 read 10 -> 8 ----------
pb["bronze"][3]["solutions"] = [8]

# ---------- reorder silver so first problem is walkable (single_value) ----------
# original order: [S0 MC, S1, S2, S3, S4, S5 MC, S6]  -> move S1 to front
s = pb["silver"]
pb["silver"] = [s[1], s[0], s[2], s[3], s[4], s[5], s[6]]

# ---------- tier descriptions ----------
pb["bronze_description"] = "Read one value straight from a box plot or cumulative frequency curve, or use frequency = frequency density " + MUL + " class width."
pb["silver_description"] = "Combine two readings: gaps on a cumulative frequency curve, histogram frequencies, and comparisons of two distributions."
pb["gold_description"] = "Estimate within a class, work back from a percentage, and identify the modal or median class on a histogram."

# ---------- misconceptions (new format) + hints + guided_steps ----------

# ===== BRONZE =====
B = pb["bronze"]

# B0 median 45  (CF, 80 students) -- COMPLETION problem
B[0]["hint"] = "The median is at position n divided by 2; read across from that cumulative frequency."
B[0]["misconceptions"] = [{"pattern":"position_as_value","expect":[40],
  "message":"40 is the position (n "+DIV+" 2), not the median score. Read across from cumulative frequency 40 to the curve, then down to the score: about 45."}]
B[0]["guided_steps"] = [
  say("The median is the middle value, half way through the data."),
  box("Total students, n = ", 80, "Given: 80 students."),
  box("Median position = n "+DIV+" 2 = 80 "+DIV+" 2 = ", 40, "Half of 80.", phase="substitute"),
  box("Read across from cumulative frequency 40 to the curve, then down. Median score = ", 45,
      "It sits half way between 40 and 50.", done="At score 45 the cumulative frequency is 40, half of 80, so 45 is the median."),
]

# B1 IQR 20 (box plot q1 35 q3 55)
B[1]["hint"] = "IQR is the width of the box: right side minus left side."
B[1]["misconceptions"] = [{"pattern":"used_range","expect":[60],
  "message":"That is the range (max "+SUB+" min = 80 "+SUB+" 20 = 60). The IQR is the box width: Q3 "+SUB+" Q1 = 55 "+SUB+" 35 = 20."}]
B[1]["guided_steps"] = [
  say("The IQR is the width of the box: Q3 "+SUB+" Q1."),
  box("Read Q3, the right side of the box = ", 55, "Right edge of the box."),
  box("Read Q1, the left side of the box = ", 35, "Left edge of the box.", phase="substitute"),
  box("IQR = 55 "+SUB+" 35 = ", 20, "Subtract the quartiles.",
      done="20 is the spread of the middle half of the data."),
]

# B2 median 168 (box plot)
B[2]["hint"] = "The median is the line inside the box."
B[2]["misconceptions"] = [{"pattern":"midpoint_of_range","expect":[170],
  "message":"The median is not the middle of the range. Read the line inside the box: 168, not (150 + 190) "+DIV+" 2 = 170."}]
B[2]["guided_steps"] = [
  say("The median is the line drawn inside the box."),
  box("Read Q1, the left edge of the box = ", 160, "Left side of the box."),
  box("Read Q3, the right edge of the box = ", 175, "Right side of the box.", phase="substitute"),
  box("The median is the line inside the box, between 160 and 175. Read it = ", 168,
      "Look for the line splitting the box.", done="168 lies between 160 and 175, so it sits inside the box, as it must."),
]

# B3 Q1 8 (CF, 60 patients) -- FIXED answer
B[3]["hint"] = "Q1 is at position n divided by 4; read across from that cumulative frequency."
B[3]["misconceptions"] = [{"pattern":"position_as_value","expect":[15],
  "message":"15 is the position (n "+DIV+" 4), not the value. Read across from cumulative frequency 15 to the curve, then down: Q1 is about 8 minutes."}]
B[3]["guided_steps"] = [
  say("Q1 is the lower quartile: a quarter of the way through the data."),
  box("Total patients, n = ", 60, "Given: 60 patients."),
  box("Q1 position = n "+DIV+" 4 = 60 "+DIV+" 4 = ", 15, "A quarter of 60.", phase="substitute"),
  box("Read across from cumulative frequency 15 to the curve, then down. Q1 = ", 8,
      "It lands between 5 and 10 minutes, near 8.",
      done="At about 8 minutes the cumulative frequency is roughly 15, a quarter of 60."),
]

# B4 range 40 (box plot)
B[4]["hint"] = "Range is the distance between the two whisker ends: max minus min."
B[4]["misconceptions"] = [{"pattern":"used_iqr","expect":[20],
  "message":"That is the IQR (Q3 "+SUB+" Q1 = 70 "+SUB+" 50 = 20). The range is max "+SUB+" min = 80 "+SUB+" 40 = 40."}]
B[4]["guided_steps"] = [
  say("The range is the full spread: max "+SUB+" min, from whisker end to whisker end."),
  box("Read the left whisker end (minimum) = ", 40, "Far left of the plot."),
  box("Read the right whisker end (maximum) = ", 80, "Far right of the plot.", phase="substitute"),
  box("Range = 80 "+SUB+" 40 = ", 40, "Subtract the smallest from the largest.",
      done="40 kg is the full spread of the weights."),
]

# B5 frequency 25 (FD 5, width 5) -- retuned from 20 to break tier duplicate with B1
B[5]["display"] = "A histogram bar has frequency density 5 and class width 5. Find the frequency."
B[5]["solutions"] = [25]
B[5]["hint"] = "Frequency is the area of the bar: FD times class width."
B[5]["misconceptions"] = [{"pattern":"divided","expect":[1],
  "message":"Frequency is FD "+MUL+" width = 5 "+MUL+" 5 = 25, not FD "+DIV+" width. Multiply, because the frequency is the area of the bar."}]
B[5]["guided_steps"] = [
  say("On a histogram, frequency = frequency density "+MUL+" class width (the area of the bar)."),
  box("Frequency density = ", 5, "Given as 5."),
  box("Class width = ", 5, "Given as 5.", phase="substitute"),
  box("Frequency = 5 "+MUL+" 5 = ", 25, "Multiply density by width.",
      done="25 is the number of items in that class."),
]

# B6 FD 3 (freq 30, width 10)
B[6]["hint"] = "Frequency density is frequency divided by class width."
B[6]["misconceptions"] = [{"pattern":"multiplied","expect":[300],
  "message":"FD = frequency "+DIV+" width = 30 "+DIV+" 10 = 3, not frequency "+MUL+" width. Divide to get the bar height."}]
B[6]["guided_steps"] = [
  say("Rearrange: frequency density = frequency "+DIV+" class width."),
  box("Frequency (number of items) = ", 30, "Given as 30."),
  box("Class width = ", 10, "Given as 10.", phase="substitute"),
  box("FD = 30 "+DIV+" 10 = ", 3, "Divide frequency by width.",
      done="3 is the height of the bar on the frequency density axis."),
]

# B7 IQR 30 (Q1 25 Q3 55)
B[7]["hint"] = "IQR is Q3 minus Q1."
B[7]["misconceptions"] = [{"pattern":"added","expect":[80],
  "message":"IQR = Q3 "+SUB+" Q1 = 55 "+SUB+" 25 = 30. Subtract the quartiles, do not add them."}]
B[7]["guided_steps"] = [
  say("The IQR is Q3 "+SUB+" Q1."),
  box("Q3 = ", 55, "The upper quartile."),
  box("Q1 = ", 25, "The lower quartile.", phase="substitute"),
  box("IQR = 55 "+SUB+" 25 = ", 30, "Subtract the quartiles.",
      done="30 is the width of the middle half of the data."),
]

# ===== SILVER (new order) =====
S = pb["silver"]
# S[0] = old S1 : between 30 and 50, 100 students, answer 40  -- COMPLETION problem
S[0]["hint"] = "Read the cumulative frequency at each mark, then subtract the smaller from the larger."
S[0]["misconceptions"] = [{"pattern":"gave_upper_cf","expect":[55],
  "message":"55 is the number scoring up to 50. Subtract those scoring up to 30 (which is 15): 55 "+SUB+" 15 = 40."}]
S[0]["guided_steps"] = [
  say("To count how many lie between two values, read the cumulative frequency at each and subtract."),
  box("Read the cumulative frequency at mark 30 = ", 15, "Go up from 30 to the curve."),
  box("Read the cumulative frequency at mark 50 = ", 55, "Go up from 50 to the curve.", phase="substitute"),
  box("Number between 30 and 50 = 55 "+SUB+" 15 = ", 40, "Subtract the lower reading.",
      done="40 students scored between 30 and 50."),
]

# S[1] = old S0 MC : consistency, sol 0
S[1]["hint"] = "Compare the box widths: a smaller IQR means more consistent."
S[1]["misconceptions"] = [{"pattern":"picked_larger_iqr","expect":[1],
  "message":"Class B has the larger IQR (35 versus 15), so Class B is less consistent. The smaller box, Class A, is more consistent."}]

# S[2] = old S2 : histogram 10-20, answer 30
S[2]["hint"] = "Frequency equals frequency density times the class width."
S[2]["misconceptions"] = [{"pattern":"read_height","expect":[3],
  "message":"3 is the frequency density, the bar height. Frequency = FD "+MUL+" width = 3 "+MUL+" 10 = 30 people."}]
S[2]["guided_steps"] = [
  say("Read the bar's frequency density, then frequency = FD "+MUL+" width."),
  box("Frequency density of the 10 to 20 bar = ", 3, "Height of that bar."),
  box("Class width = 20 "+SUB+" 10 = ", 10, "Right boundary minus left.", phase="substitute"),
  box("Frequency = 3 "+MUL+" 10 = ", 30, "Density times width.",
      done="30 people waited between 10 and 20 minutes."),
]

# S[3] = old S3 : IQR from Q1 28 med 42 Q3 56, answer 28
S[3]["hint"] = "IQR uses only the quartiles: Q3 minus Q1."
S[3]["misconceptions"] = [
  {"pattern":"added","expect":[84],
   "message":"IQR = Q3 "+SUB+" Q1 = 56 "+SUB+" 28 = 28. Subtract the quartiles, do not add them (56 + 28 = 84)."},
  {"pattern":"used_median","expect":[14],
   "message":"The IQR ignores the median. It is Q3 "+SUB+" Q1 = 56 "+SUB+" 28 = 28, not 56 "+SUB+" 42 = 14."},
]
S[3]["guided_steps"] = [
  say("The IQR uses only the quartiles: Q3 "+SUB+" Q1. The median is not needed."),
  box("Q3 = ", 56, "The upper quartile."),
  box("Q1 = ", 28, "The lower quartile.", phase="substitute"),
  box("IQR = 56 "+SUB+" 28 = ", 28, "Subtract the quartiles.",
      done="28 is the spread of the middle half."),
]

# S[4] = old S4 : total frequency, answer 90
S[4]["hint"] = "Work out each bar's frequency with FD times width, then add them all."
S[4]["misconceptions"] = [{"pattern":"added_fd","expect":[12],
  "message":"You added the frequency densities (2 + 6 + 3 + 1 = 12). Multiply each by its class width first: 10 + 30 + 30 + 20 = 90."}]
S[4]["guided_steps"] = [
  say("Total frequency = the sum of (FD "+MUL+" width) for every bar."),
  box("0 to 5: FD 2 "+MUL+" width 5 = ", 10, "Width is 5."),
  box("5 to 10: FD 6 "+MUL+" width 5 = ", 30, "Width is 5.", phase="substitute"),
  box("10 to 20: FD 3 "+MUL+" width 10 = ", 30, "Width is 10."),
  box("20 to 40: FD 1 "+MUL+" width 20 = ", 20, "Width is 20."),
  box("Total = 10 + 30 + 30 + 20 = ", 90, "Add the four frequencies.",
      done="90 is the total number of values."),
]

# S[5] = old S5 MC : sol 0
S[5]["hint"] = "A higher median means a higher average; a smaller IQR means more consistent."
S[5]["misconceptions"] = [{"pattern":"b_better_all","expect":[2],
  "message":"B has the higher median but the larger IQR (30 versus 10), so B is less consistent, not better in every way. A is the more consistent set."}]

# S[6] = old S6 : above 65, answer 60
S[6]["hint"] = "Above a value equals the total minus the cumulative frequency at that value."
S[6]["misconceptions"] = [{"pattern":"gave_cf","expect":[140],
  "message":"140 is how many scored 65 or below. Above 65 = total "+SUB+" 140 = 200 "+SUB+" 140 = 60."}]
S[6]["guided_steps"] = [
  say("'Above 65' = the total minus how many are 65 or below (the cumulative frequency at 65)."),
  box("Total data points, n = ", 200, "Given as 200."),
  box("Cumulative frequency at 65 (number 65 or below) = ", 140, "Given as 140.", phase="substitute"),
  box("Above 65 = 200 "+SUB+" 140 = ", 60, "Subtract the cumulative frequency.",
      done="60 data points are above 65."),
]

# ===== GOLD =====
G = pb["gold"]

# G0 histogram 15-25, answer 35 -- COMPLETION problem (calculator true)
G[0]["hint"] = "The range 15 to 25 covers parts of two bars; find each part with FD times width and add."
G[0]["misconceptions"] = [{"pattern":"whole_bars","expect":[70],
  "message":"15 to 25 is only part of each bar. Use the part widths (5 each): 4 "+MUL+" 5 = 20 and 3 "+MUL+" 5 = 15, giving 35, not the whole bars (40 + 30 = 70)."}]
G[0]["guided_steps"] = [
  say("15 to 25 spans parts of two bars. Find each part's frequency with FD "+MUL+" width, then add."),
  box("The 15 to 20 part sits in the 10 to 20 bar (FD 4), width 5. Frequency = 4 "+MUL+" 5 = ", 20,
      "Width from 15 to 20 is 5."),
  box("The 20 to 25 part sits in the 20 to 30 bar (FD 3), width 5. Frequency = 3 "+MUL+" 5 = ", 15,
      "Width from 20 to 25 is 5.", phase="substitute"),
  box("Total between 15 and 25 = 20 + 15 = ", 35, "Add the two parts.",
      done="An estimated 35 visitors were aged between 15 and 25."),
]

# G1 pass mark 30, answer 30 (calc false)
G[1]["hint"] = "If 75% pass, 25% fail; find the score with that many students below it."
G[1]["misconceptions"] = [{"pattern":"used_pass_count","expect":[90],
  "message":"90 is the number who pass (75% of 120), not a score. The pass mark is the score with 25% (30 students) below it: read where cumulative frequency = 30, giving 30."}]
G[1]["guided_steps"] = [
  say("If 75% pass, 25% fail. The pass mark is the score with 25% of students below it."),
  box("25% of 120 students = 0.25 "+MUL+" 120 = ", 30, "A quarter of 120."),
  box("So 30 students are below the pass mark. On the curve, the cumulative frequency we look for is = ", 30,
      "The number who fail.", phase="substitute"),
  box("Read down from cumulative frequency 30 to the score axis. Pass mark = ", 30,
      "Where the curve reaches 30.", done="At a score of 30 the cumulative frequency is 30, so 90 students (75%) score above it."),
]

# G2 MC modal class, sol 0  -> add histogram chart
G[2]["hint"] = "The modal class has the highest frequency density, not the highest frequency."
G[2]["misconceptions"] = [{"pattern":"highest_frequency","expect":[1],
  "message":"With unequal classes the modal class has the highest frequency density (FD 6 in 25-30), not the highest frequency. 10-25 has the most values (60) but a lower bar."}]
G[2]["chart"] = {
  "type":"bar",
  "data":{"labels":["0–10","10–25","25–30","30–50"],
    "datasets":[{"data":[3,4,6,2],"borderColor":"#3b82f6","borderWidth":1,
      "backgroundColor":"rgba(59,130,246,0.4)"}]},
  "options":{"scales":{
    "x":{"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"Class","display":True}},
    "y":{"grid":{"color":"rgba(0,0,0,0.08)"},"ticks":{"stepSize":1},
      "title":{"text":"Frequency density","display":True},"beginAtZero":True}}}}

# G3 MC median class, sol 0  -> add histogram chart
G[3]["hint"] = "Find each class frequency (FD times width), then locate the class holding the middle value."
G[3]["misconceptions"] = [{"pattern":"highest_frequency_class","expect":[2],
  "message":"The median class holds the middle value, not the largest frequency. Frequencies 40, 50, 60 total 150; the 75th value sits in 20-30 (cumulative 90 there), so 30-50 is wrong."}]
G[3]["chart"] = {
  "type":"bar",
  "data":{"labels":["0–20","20–30","30–50"],
    "datasets":[{"data":[2,5,3],"borderColor":"#22c55e","borderWidth":1,
      "backgroundColor":"rgba(34,197,94,0.4)"}]},
  "options":{"scales":{
    "x":{"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"Class","display":True}},
    "y":{"grid":{"color":"rgba(0,0,0,0.08)"},"ticks":{"stepSize":1},
      "title":{"text":"Frequency density","display":True},"beginAtZero":True}}}}

# G4 diff of medians, answer 10
G[4]["hint"] = "Read each median line, then subtract the smaller from the larger."
G[4]["misconceptions"] = [{"pattern":"wrong_order","expect":[-10],
  "message":"Take Class B's median minus Class A's: 50 "+SUB+" 40 = 10. Doing 40 "+SUB+" 50 gives "+SUB+"10; the question asks how much B exceeds A."}]
G[4]["guided_steps"] = [
  say("Read each median, the line inside each box, then subtract."),
  box("Class A median (line inside the lower box) = ", 40, "Middle line of Class A."),
  box("Class B median (line inside the upper box) = ", 50, "Middle line of Class B.", phase="substitute"),
  box("Difference = 50 "+SUB+" 40 = ", 10, "B minus A.",
      done="Class B's median is 10 marks above Class A's."),
]

# ---------- add S4 histogram chart (silver index 4) ----------
S[4]["chart"] = {
  "type":"bar",
  "data":{"labels":["0–5","5–10","10–20","20–40"],
    "datasets":[{"data":[2,6,3,1],"borderColor":"#8b5cf6","borderWidth":1,
      "backgroundColor":"rgba(139,92,246,0.4)"}]},
  "options":{"scales":{
    "x":{"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"Class","display":True}},
    "y":{"grid":{"color":"rgba(0,0,0,0.08)"},"ticks":{"stepSize":1},
      "title":{"text":"Frequency density","display":True},"beginAtZero":True}}}}

# ---------- guided: opener + teach ----------
pd["guided"] = {
  "opener": {"steps": [
    say("A café counts new customers each hour. Hour 1: 5 people. Hour 2: 8 more. Hour 3: 6 more. Let us keep a running total."),
    box("By the end of hour 2, the total who had arrived is 5 + 8 = ", 13, "Add hour 1 and hour 2."),
    box("By the end of hour 3, the total is 13 + 6 = ", 19, "Add the next hour on to your running total."),
    say("You kept a <strong>running total</strong>: each number counts everyone so far. That is <strong>cumulative frequency</strong>. Plot it against the top of each group and you get a curve. Reading across at half the total, \\(n/2\\), finds the <strong>median</strong>; a quarter and three quarters give \\(Q_1\\) and \\(Q_3\\)."),
  ]},
  "teach": {
    "bronze": {
      "display": "A box plot has minimum 12, lower quartile 20, median 26, upper quartile 35, maximum 48. Find the median, the interquartile range and the range.",
      "steps": [
        box("Median (the line inside the box) = ", 26, "Read the middle line."),
        box("Upper quartile Q3 (right side of the box) = ", 35, "Right edge of the box."),
        box("Lower quartile Q1 (left side of the box) = ", 20, "Left edge of the box."),
        box("IQR = Q3 "+SUB+" Q1 = 35 "+SUB+" 20 = ", 15, "Width of the box.",
            done="The box holds the middle half of the data."),
        box("Range = max "+SUB+" min = 48 "+SUB+" 12 = ", 36, "Distance between the whiskers.",
            done="That is the point: the box gives the IQR, the whiskers give the range."),
      ]},
    "silver": {
      "display": "A histogram has three bars: 0 to 10 (frequency density 3), 10 to 30 (frequency density 5), 30 to 40 (frequency density 2). Find the frequency of each class and the total.",
      "steps": [
        box("0 to 10: FD 3 "+MUL+" width 10 = ", 30, "Frequency is FD times width."),
        box("10 to 30: FD 5 "+MUL+" width 20 = ", 100, "Width is 30 "+SUB+" 10 = 20.",
            done="A wide bar can hold a lot even at a low height."),
        box("30 to 40: FD 2 "+MUL+" width 10 = ", 20, "Width is 10."),
        box("Total frequency = 30 + 100 + 20 = ", 150, "Add the three frequencies.",
            done="That was the point: read area, not height."),
      ]},
    "gold": {
      "display": "A histogram bar covers 20 to 40 with frequency density 4. Assuming the values are spread evenly, estimate how many lie between 25 and 40.",
      "steps": [
        box("Full bar width = 40 "+SUB+" 20 = ", 20, "Right boundary minus left."),
        box("Full frequency = FD 4 "+MUL+" width 20 = ", 80, "FD times width."),
        box("The part 25 to 40 has width = 40 "+SUB+" 25 = ", 15, "Just the part asked for."),
        box("Estimate = FD 4 "+MUL+" 15 = ", 60, "Same density, smaller width.",
            done="Even spread means frequency follows width: 15/20 of 80 is 60."),
      ]},
  }
}

# ---------- tier_guides ----------
pd["tier_guides"] = {
  "bronze": {
    "title": "Bronze: reading a single value from a chart",
    "steps": [
      "On a <strong>box plot</strong>: the middle line is the median, the box edges are Q1 and Q3, the whisker ends are the minimum and maximum.",
      "IQR = Q3 "+SUB+" Q1 (the box width). Range = max "+SUB+" min (whisker to whisker).",
      "On a <strong>histogram</strong>: frequency = frequency density "+MUL+" class width. Rearranged, FD = frequency "+DIV+" width.",
    ],
    "example": {
      "question": "A box plot shows min 10, Q1 24, median 31, Q3 40, max 58. Find the IQR.",
      "steps": [
        {"label":"Q3","content":"Q3 = 40"},
        {"label":"Q1","content":"Q1 = 24"},
        {"label":"Check","content":"IQR is the box width, Q3 "+SUB+" Q1"},
        {"label":"Answer","content":"IQR = 40 "+SUB+" 24 = 16","isAnswer":True,"is_answer":True},
      ]}},
  "silver": {
    "title": "Silver: combining two readings",
    "steps": [
      "Between two values on a <strong>cumulative frequency</strong> curve: read the CF at each and subtract.",
      "For a histogram frequency, do FD "+MUL+" width for each bar; add them for a total.",
      "To compare two distributions, compare the medians (average) and the IQRs (spread: smaller is more consistent).",
    ],
    "example": {
      "question": "A CF curve of 80 people gives CF = 60 at 40 and CF = 20 at 20. How many are between 20 and 40?",
      "steps": [
        {"label":"Upper","content":"CF at 40 = 60"},
        {"label":"Lower","content":"CF at 20 = 20"},
        {"label":"Check","content":"Subtract to count the gap"},
        {"label":"Answer","content":"60 "+SUB+" 20 = 40 people","isAnswer":True,"is_answer":True},
      ]}},
  "gold": {
    "title": "Gold: estimating and working back",
    "steps": [
      "Part of a bar: use the part's width, not the whole class. Frequency = FD "+MUL+" part width.",
      "From a percentage: turn it into a count (percentage of the total), then read the matching score on the curve.",
      "Modal class = tallest bar by <strong>frequency density</strong>. The median class holds the middle value once the frequencies are listed.",
    ],
    "example": {
      "question": "A histogram bar spans 30 to 50 (FD 3). Estimate how many lie between 40 and 50.",
      "steps": [
        {"label":"Part width","content":"50 "+SUB+" 40 = 10"},
        {"label":"Estimate","content":"FD "+MUL+" part width = 3 "+MUL+" 10"},
        {"label":"Check","content":"Half the bar's width, so half its frequency"},
        {"label":"Answer","content":"3 "+MUL+" 10 = 30","isAnswer":True,"is_answer":True},
      ]}},
}

json.dump(pd, io.open("lesson_maths-aqa_probability-statistics-L05.json","w",encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_probability-statistics-L05.json")
