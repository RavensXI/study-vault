# -*- coding: utf-8 -*-
"""Build the guided-learning practice_data for Geography Skills L01."""
import io, json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_live_L01.json"), encoding="utf-8"))
pb = pd["problem_bank"]

# ----------------------------------------------------------------- helpers --
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    st = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say: st["say"] = say
    if done: st["done"] = done
    if phase: st["phase"] = phase
    return st

def say(text):
    return {"say": text}

def mis(pattern, message, expect, note=None):
    m = {"pattern": pattern, "message": message, "expect": expect}
    if note: m["note"] = note
    return m

# --------------------------------------------------------------------- SVG --
TXT = 'font-family="Inter,Segoe UI,sans-serif" fill="#2d2a26"'

def grid(ys, x0, x1, labels):
    out = []
    for y, lab in zip(ys, labels):
        out.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="#d8d2c8" stroke-width="1"/>' % (x0, y, x1, y))
        out.append('<text x="%d" y="%s" text-anchor="end" font-size="9" %s>%s</text>' % (x0 - 6, float(y) + 3, TXT, lab))
    return "".join(out)

# opener: two bars, Monday 30mm, Tuesday 50mm, scale 0-60 step 10
OPENER_SVG = (
 '<svg viewBox="0 0 280 180" role="img" aria-label="Bar chart of rainfall on two days.'
 ' Monday reaches 30 millimetres and Tuesday reaches 50 millimetres on a scale from 0 to 60 millimetres.">'
 '<rect x="0" y="0" width="280" height="180" fill="#faf8f5"/>'
 + grid([150, 130, 110, 90, 70, 50, 30], 50, 265, ["0", "10", "20", "30", "40", "50", "60"]) +
 '<line x1="50" y1="30" x2="50" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 '<line x1="50" y1="150" x2="265" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 '<rect x="80" y="90" width="60" height="60" fill="#93c5fd" stroke="#3b82f6"/>'
 '<rect x="175" y="50" width="60" height="100" fill="#93c5fd" stroke="#3b82f6"/>'
 '<text x="110" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Monday</text>'
 '<text x="205" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Tuesday</text>'
 '<text x="50" y="20" font-size="10" ' + TXT + '>Rainfall (mm)</text>'
 '</svg>')

# teach bronze: four beaches, 20 / 35 / 15 / 30, scale 0-40 step 10
def bar(x, v, scale_top, base=150, top=30, w=40, fill="#93c5fd", stroke="#3b82f6"):
    h = (base - top) * v / float(scale_top)
    return '<rect x="%d" y="%g" width="%d" height="%g" fill="%s" stroke="%s"/>' % (x, base - h, w, h, fill, stroke)

TEACH_B_SVG = (
 '<svg viewBox="0 0 290 180" role="img" aria-label="Bar chart of litter items collected on four beaches.'
 ' Beach A 20, Beach B 35, Beach C 15 and Beach D 30, on a scale from 0 to 40.">'
 '<rect x="0" y="0" width="290" height="180" fill="#faf8f5"/>'
 + grid([150, 120, 90, 60, 30], 50, 275, ["0", "10", "20", "30", "40"]) +
 '<line x1="50" y1="30" x2="50" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 '<line x1="50" y1="150" x2="275" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 + bar(70, 20, 40) + bar(120, 35, 40) + bar(170, 15, 40) + bar(220, 30, 40) +
 '<text x="90" y="164" text-anchor="middle" font-size="10" ' + TXT + '>A</text>'
 '<text x="140" y="164" text-anchor="middle" font-size="10" ' + TXT + '>B</text>'
 '<text x="190" y="164" text-anchor="middle" font-size="10" ' + TXT + '>C</text>'
 '<text x="240" y="164" text-anchor="middle" font-size="10" ' + TXT + '>D</text>'
 '<text x="50" y="20" font-size="10" ' + TXT + '>Litter items collected</text>'
 '</svg>')

# teach silver: grouped bars, two towns, four seasons, scale 0-80 step 20
def gbar(x, v, fill, stroke, w=22):
    h = 120.0 * v / 80.0
    return '<rect x="%d" y="%g" width="%d" height="%g" fill="%s" stroke="%s"/>' % (x, 150 - h, w, h, fill, stroke)

TEACH_S_SVG = (
 '<svg viewBox="0 0 300 195" role="img" aria-label="Dual bar chart of seasonal rainfall in two towns.'
 ' Town X reads 40, 20, 60 and 80 millimetres and Town Y reads 30, 35, 45 and 50 millimetres'
 ' across spring, summer, autumn and winter, on a scale from 0 to 80.">'
 '<rect x="0" y="0" width="300" height="195" fill="#faf8f5"/>'
 + grid([150, 120, 90, 60, 30], 50, 285, ["0", "20", "40", "60", "80"]) +
 '<line x1="50" y1="30" x2="50" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 '<line x1="50" y1="150" x2="285" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 + "".join(gbar(x, v, "#93c5fd", "#3b82f6") for x, v in
           zip((60, 115, 170, 225), (40, 20, 60, 80)))
 + "".join(gbar(x + 24, v, "#fcd34d", "#d97706") for x, v in
           zip((60, 115, 170, 225), (30, 35, 45, 50))) +
 '<text x="93" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Spring</text>'
 '<text x="148" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Summer</text>'
 '<text x="203" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Autumn</text>'
 '<text x="258" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Winter</text>'
 '<rect x="60" y="178" width="10" height="10" fill="#93c5fd" stroke="#3b82f6"/>'
 '<text x="75" y="187" font-size="10" ' + TXT + '>Town X</text>'
 '<rect x="140" y="178" width="10" height="10" fill="#fcd34d" stroke="#d97706"/>'
 '<text x="155" y="187" font-size="10" ' + TXT + '>Town Y</text>'
 '<text x="50" y="20" font-size="10" ' + TXT + '>Rainfall (mm)</text>'
 '</svg>')

# teach gold: two stacked bars to 100%, scale 0-100 step 20
def stack(x, parts, w=60):
    out, running = [], 0
    cols = [("#86efac", "#16a34a"), ("#fcd34d", "#d97706"), ("#93c5fd", "#3b82f6")]
    for v, (f, s) in zip(parts, cols):
        h = 120.0 * v / 100.0
        y = 150 - 120.0 * (running + v) / 100.0
        out.append('<rect x="%d" y="%g" width="%d" height="%g" fill="%s" stroke="%s"/>' % (x, y, w, h, f, s))
        running += v
    return "".join(out)

TEACH_G_SVG = (
 '<svg viewBox="0 0 300 195" role="img" aria-label="Two stacked percentage bars of employment by sector.'
 ' Country P is 10 percent primary, 30 percent secondary and 60 percent tertiary.'
 ' Country Q is 40 percent primary, 25 percent secondary and 35 percent tertiary.">'
 '<rect x="0" y="0" width="300" height="195" fill="#faf8f5"/>'
 + grid([150, 126, 102, 78, 54, 30], 50, 285, ["0", "20", "40", "60", "80", "100"]) +
 '<line x1="50" y1="30" x2="50" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 '<line x1="50" y1="150" x2="285" y2="150" stroke="#2d2a26" stroke-width="1"/>'
 + stack(90, [10, 30, 60]) + stack(190, [40, 25, 35]) +
 '<text x="120" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Country P</text>'
 '<text x="220" y="164" text-anchor="middle" font-size="10" ' + TXT + '>Country Q</text>'
 '<rect x="55" y="178" width="10" height="10" fill="#86efac" stroke="#16a34a"/>'
 '<text x="70" y="187" font-size="10" ' + TXT + '>Primary</text>'
 '<rect x="135" y="178" width="10" height="10" fill="#fcd34d" stroke="#d97706"/>'
 '<text x="150" y="187" font-size="10" ' + TXT + '>Secondary</text>'
 '<rect x="225" y="178" width="10" height="10" fill="#93c5fd" stroke="#3b82f6"/>'
 '<text x="240" y="187" font-size="10" ' + TXT + '>Tertiary</text>'
 '<text x="50" y="20" font-size="10" ' + TXT + '>% of workforce</text>'
 '</svg>')

# ------------------------------------------------------------- method card --
pd["method_card"] = {
 "title": "Bar Charts & Line Graphs",
 "steps": [
  "Read the axis titles and units first",
  "Find your category or year on the bottom axis",
  "Read across to the side axis, checking the gridline step",
  "Then compare, total or subtract as the question asks"
 ],
 "content": (
  "<p><strong>Bar charts</strong> compare separate categories: the taller the bar, the bigger the value. "
  "<strong>Line graphs</strong> show change over time, so they reveal trends, peaks and troughs.</p>"
  "<p>Always check the <strong>gridline step</strong> before you read a value. A step might be worth 1, 5, 10 "
  "or 5,000. Bar tops and plotted points often sit between gridlines, so judge the fraction of the gap.</p>"
  "<p><strong>Stacked bars</strong> sit sections on top of each other, so a section's size is the level at its "
  "top minus the level below it. <strong>Dual charts</strong> show two sets of data together, so use the legend "
  "to pick the right one before reading.</p>"),
 "example": (
  "<p><strong>Question:</strong> A bar chart shows summer rainfall: June 70 mm, July 65 mm, August 75 mm. "
  "Find the total.</p><p><strong>Step 1:</strong> Read each bar top across to the side axis.</p>"
  "<p><strong>Step 2:</strong> Add them: 70 + 65 + 75.</p><p><strong>Answer:</strong> 210 mm</p>")
}

# -------------------------------------------------------------- tier guides --
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: one reading, straight off the chart",
  "steps": [
   "Start with the <strong>axis titles</strong>. They tell you what is being measured and in what units.",
   "Find your category or year along the bottom axis, then move up to the bar top or the plotted point.",
   "Slide across to the side axis and read the value. Check the gridline step first, because bar tops often land between labels."
  ],
  "example": {
   "question": "A bar chart of monthly rainfall. Read the value for March.",
   "steps": [
    {"label": "Locate", "content": "<p>Count along the bottom axis. March is the third bar.</p>"},
    {"label": "Check the scale", "content": "<p>The side axis is labelled every 10 mm, so one gridline step is worth 10 mm.</p>"},
    {"label": "Read across", "content": "<p>March's bar top sits one full gridline above 40, so it reads 50 mm.</p>"},
    {"label": "Check", "content": "<p>February reads 40 mm and April reads 55 mm, so 50 mm sits sensibly between them. ✓</p>"},
    {"label": "Answer", "content": "<p><strong>50 mm</strong></p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "silver": {
  "title": "Silver: two readings, then a calculation",
  "steps": [
   "Silver questions need <strong>two or more readings</strong>, so take each one carefully before you calculate anything.",
   "Use the <strong>legend</strong> to tell paired bars or lines apart, and read both at the same place on the bottom axis.",
   "Then do the move the question asks for: a difference, a total, a range or a percentage change. Subtract the smaller or earlier value from the larger or later one."
  ],
  "example": {
   "question": "A dual bar chart of rainfall in two towns. Find the difference in their annual totals.",
   "steps": [
    {"label": "Total the first town", "content": "<p>Add all twelve of Town A's bars: 620 mm.</p>"},
    {"label": "Total the second", "content": "<p>Add all twelve of Town B's bars: 480 mm.</p>"},
    {"label": "Subtract", "content": "<p>620 − 480 = 140 mm.</p>"},
    {"label": "Check", "content": "<p>480 + 140 = 620, back on Town A's total. ✓</p>"},
    {"label": "Answer", "content": "<p><strong>140 mm</strong></p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "gold": {
  "title": "Gold: stacked bars, two data sets, and what the pattern shows",
  "steps": [
   "In a <strong>stacked bar</strong> each section begins where the last one ended, so a section's size is the level at its top minus the level below.",
   "When two data sets share a chart, check which line or colour belongs to which before you read anything.",
   "Finish by saying what the pattern <strong>means</strong>: a trend, a lag, a stage, a climate type. Back it up with a number you have read."
  ],
  "example": {
   "question": "A stacked bar shows employment by sector. Find the size of the tertiary section.",
   "steps": [
    {"label": "Top of the bar", "content": "<p>The whole bar fills to 100%.</p>"},
    {"label": "Level below", "content": "<p>The secondary section ends at the 35% level.</p>"},
    {"label": "Subtract", "content": "<p>Tertiary = 100 − 35 = 65%.</p>"},
    {"label": "Check", "content": "<p>Primary 10 + secondary 25 + tertiary 65 = 100. ✓</p>"},
    {"label": "Answer", "content": "<p><strong>65%</strong></p>", "isAnswer": True, "is_answer": True}
   ]
  }
 }
}

# ------------------------------------------------------------------ guided --
pd["guided"] = {
 "opener": {
  "label": "Before any graph rules",
  "display": "<p>Rainfall measured at one weather station on two days:</p>" + OPENER_SVG,
  "steps": [
   box("Tuesday's bar reaches ", 50, "Follow the top of the taller bar straight across to the scale on the left.",
       post=" mm", say="No rules yet. Just look at the two bars."),
   box("Monday's bar reaches 30 mm, so Tuesday had ", 20,
       "Take Monday's 30 mm away from the number you just read.", post=" mm more rain."),
   say("<strong>That is the whole skill.</strong> You matched a bar top to a number on the side axis, then "
       "subtracted one reading from another to compare them. Every question in this lesson is those two moves "
       "on a bigger chart.")
  ]
 },
 "teach": {
  "bronze": {
   "label": "Together: your first reading",
   "display": "<p>Litter collected on four beaches. Read the count for beach C.</p>" + TEACH_B_SVG,
   "steps": [
    box("Counting from the left, beach C is bar number ", 3,
        "The bars are labelled A, B, C, D in order along the bottom axis.",
        say="Locate before you read. Find the bar the question names."),
    box("One gridline step on the side axis is worth ", 10,
        "Look at two labelled gridlines next to each other and see how much the number goes up.",
        done="Never read a value until you know what one step is worth."),
    box("Beach C's bar top sits half a step above 10, so it reads ", 15,
        "Half of a 10 step is 5, added onto the gridline below.",
        done="Bar tops do not always land on a label. Judge the fraction of the gap."),
    box("The tallest bar is beach B. It reads ", 35,
        "Its top sits half a step above 30."),
    box("So beach B has ", 20, "Take beach C's count away from beach B's.",
        post=" more items than beach C.",
        done="Read, then compare. That pair of moves handles every bronze question.")
   ]
  },
  "silver": {
   "label": "Together: two readings at once",
   "display": "<p>Seasonal rainfall in two towns. Compare them.</p>" + TEACH_S_SVG,
   "steps": [
    box("Counting from the left, autumn is pair number ", 3,
        "The pairs run spring, summer, autumn, winter.",
        say="Two bars per season now, so the legend matters."),
    box("In winter, Town X reads ", 80, "Use the legend: Town X is the blue bar of each pair.",
        post=" mm."),
    box("In winter, Town Y reads ", 50, "Town Y is the yellow bar, the right-hand one of the pair.",
        post=" mm."),
    box("So the winter gap between the towns is ", 30,
        "Subtract the smaller winter reading from the larger one.", post=" mm."),
    box("In summer Town X reads 20 mm and Town Y reads 35 mm, so the summer gap is ", 15,
        "Same move, but this time Town Y is the taller of the two.", post=" mm.",
        done="Gaps can run either way round. Always subtract the smaller from the larger."),
    box("Adding Town X's four bars gives an annual total of ", 200,
        "40 + 20 + 60 + 80.", post=" mm.",
        done="Silver is about combining readings: differences and totals, not single values.")
   ]
  },
  "gold": {
   "label": "Together: reading a stacked bar",
   "display": "<p>Employment by sector in two countries. How big is Country P's tertiary section?</p>" + TEACH_G_SVG,
   "steps": [
    box("Counting from the bottom of the bar, tertiary is section number ", 3,
        "The legend lists the sections in the order they are stacked.",
        say="In a stacked bar the sections sit on top of each other, so nothing starts at zero except the first."),
    box("Country P's whole bar reaches the ", 100, "Follow the very top of the bar across to the side axis.",
        post=" level.",
        done="A stacked percentage bar always fills to 100."),
    box("The secondary section of Country P ends at the ", 40,
        "That is the line where the yellow band stops and the blue band starts.", post=" level.",
        done="This level is where tertiary begins, not how big tertiary is."),
    box("So the tertiary section is worth ", 60,
        "Take the level where tertiary starts away from the level where the bar ends.", post="%."),
    box("Check: primary 10 + secondary 30 + tertiary gives ", 100,
        "Add all three sections together.",
        done="The sections fill the bar exactly, so the subtraction was right. Subtracting levels is the gold move.")
   ]
  }
 }
}

# ------------------------------------------------------- tier descriptions --
pb["bronze_description"] = "Take a single value off a bar top or a plotted point, or pick out the highest or lowest."
pb["silver_description"] = "Take two or more readings, then find a difference, a total, a range or a percentage change."
pb["gold_description"] = "Work with stacked bars and paired data sets, then explain what the pattern shows."

# --------------------------------------------------------------- BRONZE ----
b = pb["bronze"]

b[0]["hint"] = "Find October along the bottom axis, then read straight across from the top of its bar to the side axis."
b[0]["guided_steps"] = [
 box("Counting from the left, October is bar number ", 10,
     "The bars run January to December in order.",
     say="Locate first. Find the month the question names before you read anything."),
 box("On the side axis, one gridline step is worth ", 10,
     "Compare two labelled gridlines next to each other."),
 box("Read across from the top of October's bar. It reads ", 60,
     "It lands on a labelled gridline, so no fractions needed.", post=" mm.", phase="substitute"),
 box("Only one other bar on the chart is taller than October's. That is ", 1,
     "Scan the twelve bar tops and count how many rise above October's.", post=" bar.",
     done="Your reading has to be the second highest on the chart, and it is. If it were not, you have read the wrong bar.")
]
b[0]["misconceptions"] = [
 mis("read_neighbour_month", "You have read the bar next to October. Line the bar up with its own label along the bottom axis before you read the top.", 52,
     note="September = 52"),
 mis("read_tallest_bar", "That is the tallest bar on the chart, not the one the question names. Find October first, then read.", 65,
     note="November = 65")
]

b[1]["hint"] = "Compare the tops of the four named bars, not their positions along the chart."
b[1]["guided_steps"] = [
 box("Counting from the left, November is bar number ", 11,
     "The bars run January to December in order.",
     say="The four options are October, November, December and January. Locate each one first."),
 box("October's bar reads ", 60, "Read across from its top to the side axis.", post=" mm."),
 box("November's bar reads ", 65, "It is half a step above the 60 gridline.", post=" mm.",
     phase="substitute"),
 box("December and January both read 55 mm. Of the four named months, the number reading above 60 mm is ", 1,
     "Compare each of the four readings with 60.", post=" month.",
     done="Only one of the four rises above the rest, so that month is the wettest of the group.")
]
b[1]["misconceptions"] = [
 mis("picked_the_last_bar", "December sits at the right-hand end of the chart, but being last is not the same as being tallest. Compare bar tops, not positions.", 2),
 mis("stopped_at_the_first_rise", "October is where the rainfall starts climbing, but the climb carries on past it. Follow the bars right until they stop rising.", 0)
]

b[2]["hint"] = "Line April up with its own bar, then judge where the bar top sits between the labelled gridlines."
b[2]["guided_steps"] = [
 box("Counting from the left, April is bar number ", 4,
     "January is bar 1, so count on from there.",
     say="Find April's bar before you read any value."),
 box("On the side axis, one labelled step is worth ", 5,
     "Look at the gap between two labelled gridlines."),
 box("April's bar top sits between two gridlines. It reads ", 22,
     "It is a small fraction of a 5 step above the 20 gridline.", post=" °C.",
     phase="substitute"),
 box("March reads 18 °C, so April is warmer by ", 4,
     "Subtract March's reading from yours.", post=" °C.",
     done="Neighbouring months should differ by a few degrees, not by ten or more. A jump that big means you have read the wrong bar.")
]
b[2]["misconceptions"] = [
 mis("counted_one_bar_too_far", "You have counted one bar too far to the right. January is bar 1, so check which bar sits directly above the April label.", 26,
     note="May = 26"),
 mis("read_the_bar_before", "That is the bar to the left of April. Line each bar up with its own label before reading.", 18,
     note="March = 18")
]

b[3]["hint"] = "Find 2010 on the bottom axis, go up to the plotted point, then read across, remembering the axis counts people in thousands."
b[3]["guided_steps"] = [
 box("Counting from the left, 2010 is plotted point number ", 3,
     "The points sit at 2000, 2005, 2010, 2015 and 2020.",
     say="Line graphs are read the same way as bars: locate the point first."),
 box("One labelled step on the side axis is worth ", 5000,
     "Compare two labels next to each other on the side axis."),
 box("Reading across from the 2010 point gives a population of ", 35000,
     "It sits exactly on a labelled gridline.", phase="substitute"),
 box("The 2005 point reads 28,000. Your reading is bigger by ", 7000,
     "Subtract 28,000 from your reading.",
     done="The 2015 point reads 40,000, so a value a few thousand above 2005 and below 2015 is exactly where 2010 should sit.")
]
b[3]["misconceptions"] = [
 mis("read_the_point_to_the_left", "That is the point one place to the left. Check the year label directly under the point before you read across.", 28000,
     note="2005 = 28000"),
 mis("dropped_the_scale", "You have read the position on the axis correctly but ignored what the axis counts in. Check the labels on the side axis.", 35,
     note="reading 35 instead of 35000")
]

b[4]["hint"] = "Range means the gap between the highest and the lowest points anywhere on the line."
b[4]["guided_steps"] = [
 box("The line climbs to a flat top in midsummer. The first month at that peak is month number ", 7,
     "Count along from January as month 1.",
     say="Range needs two readings: the highest point and the lowest. Find them on the line first."),
 box("The peak reads ", 19, "Read across from the flat top of the line.", post=" °C."),
 box("The lowest part of the line reads ", 5, "The line is flattest and lowest at the start of the year.",
     post=" °C.", phase="substitute"),
 box("Range = highest − lowest = ", 14, "Subtract your second reading from your first.", post=" °C."),
 box("Check: add your range back onto the lowest reading and you get ", 19,
     "Lowest reading plus the range.",
     done="It lands exactly on the peak, so the range spans the whole line.")
]
b[4]["misconceptions"] = [
 mis("used_first_and_last", "You have used January and December rather than the highest and lowest points anywhere on the line. Scan the whole line for its peak and its trough.", 1,
     note="Dec 6 − Jan 5 = 1"),
 mis("added_the_two", "You have added the two readings together. A range measures the gap between them, so subtract.", 24,
     note="19 + 5 = 24")
]

b[5]["hint"] = "Read both named bars first, then subtract the smaller from the larger."
b[5]["guided_steps"] = [
 box("The bars run France, Spain, Italy, UK, Germany. Counting from the left, Italy is bar number ", 3,
     "Match each country name to the bar directly above it.",
     say="Two bars are named in the question. Locate both before you read either."),
 box("Spain's bar reads ", 85, "Read across from its top to the side axis.", post=" thousand."),
 box("Italy's bar reads ", 75, "Read across from Italy's bar top the same way.", post=" thousand.",
     phase="substitute"),
 box("So Spain had ", 10, "Subtract Italy's reading from Spain's.", post=" thousand more arrivals."),
 box("Check: add your difference back onto Italy's reading and you get ", 85,
     "Italy's reading plus the difference.",
     done="It lands back on Spain's bar top, so the subtraction went the right way round.")
]
b[5]["misconceptions"] = [
 mis("used_the_tallest_bar", "You have used the tallest bar rather than the one labelled Spain. Match each country name to the bar directly above it.", 15,
     note="France 90 − Italy 75 = 15"),
 mis("added_the_bars", "You have added the two readings. A question asking how many more wants the gap between them.", 160,
     note="85 + 75 = 160")
]

b[6]["hint"] = "The question asks for a time, so once you have found the highest point, read down to the bottom axis."
b[6]["guided_steps"] = [
 box("The bottom axis counts hours in steps of 2. Counting from the left, the highest point on the line is point number ", 5,
     "The first point sits at hour 0, so count that as point 1.",
     say="Find the peak of the line before you read anything off either axis."),
 box("At that peak the discharge reads ", 25, "Read across to the side axis.", post=" cumecs."),
 box("Now read down to the bottom axis instead. That point sits at hour ", 8,
     "The bottom axis is labelled every 2 hours.", phase="substitute"),
 box("Scanning the whole line, the number of points reading higher than 25 cumecs is ", 0,
     "Compare every plotted point with the peak you read.",
     done="Nothing on the line rises above it, so that really is the peak.")
]
b[6]["misconceptions"] = [
 mis("gave_the_discharge", "That is the discharge value from the side axis. The question asks for a time, which is read off the bottom axis.", 25),
 mis("counted_points_not_hours", "You have given the position of the point along the line, not the hour printed under it. Read the number on the bottom axis.", 5)
]

b[7]["hint"] = "Compare the two shortest bars carefully against the gridlines before you choose."
b[7]["guided_steps"] = [
 box("Six bars, labelled left to right. Counting from the left, India is bar number ", 4,
     "The order is USA, China, UK, India, Germany, Brazil.",
     say="Lowest means shortest bar. Locate the short ones first."),
 box("India's bar reads ", 2, "Read across from its top to the side axis.", post=" tonnes."),
 box("Brazil's bar is the only other short one. It reads ", 2.5,
     "Its top sits a quarter of a step above the 2 gridline.", post=" tonnes.",
     phase="substitute"),
 box("So Brazil's bar is taller than India's by ", 0.5, "Subtract the smaller reading from the larger.",
     post=" tonnes.",
     done="A small but real gap, so the two are not tied and the shorter one is clear."),
 say("The shortest bar of all is <strong>India</strong>. Choose that option.")
]
b[7]["misconceptions"] = [
 mis("picked_the_second_shortest", "Brazil's bar is short, but one bar is shorter still. Compare the two shortest tops against the gridlines.", 5),
 mis("picked_a_low_but_not_lowest_bar", "The UK sits well below the tallest bars, but lowest means the shortest bar in the whole chart, not simply a low one.", 2)
]

# --------------------------------------------------------------- SILVER ----
s = pb["silver"]

s[0]["hint"] = "Work out the size of the gap between the two lines in each named month, taking care with values below zero."
s[0]["guided_steps"] = [
 box("The four options are January, April, July and October. Counting from the left, October is point number ", 10,
     "January is point 1, so count along the bottom axis.",
     say="Greatest difference means the widest gap between the two lines, so measure gaps, not heights."),
 box("In January, London's line reads ", 5, "Use the legend to pick out London's line first.", post=" °C."),
 box("In January, Moscow's line reads ", -8,
     "It sits below the zero line, so give a negative number.", post=" °C.", phase="substitute"),
 box("So the January gap between them is ", 13,
     "Subtract Moscow's value from London's, remembering that subtracting a negative adds.", post=" °C."),
 box("In July London reads 19 °C and Moscow reads 20 °C, so the July gap is ", 1, post=" °C.",
     hint="Subtract the smaller July reading from the larger.",
     done="April (11 and 8) and October (12 and 6) give gaps of 3 and 6, so the winter gap is far the widest."),
 say("The widest gap between the two lines is in <strong>January</strong>. Choose that option.")
]
s[0]["misconceptions"] = [
 mis("picked_the_hottest_month", "July is where both lines are highest, but the question asks where they are furthest apart, not where they are warmest.", 2),
 mis("ignored_the_negative_values", "October does show a clear gap, but check the winter months, where one line drops below zero and the gap is measured across the zero line too.", 3)
]

s[1]["hint"] = "Find the increase first, then divide it by the starting value and multiply by 100."
s[1]["guided_steps"] = [
 box("The line runs from 1950 to 2020. The number of plotted points is ", 8,
     "One point per labelled decade along the bottom axis.",
     say="Percentage change always needs two readings: the starting value and the finishing value."),
 box("The 1950 point reads ", 50, "Read across from the left-hand end of the line.", post=" million."),
 box("The 2020 point reads ", 66, "Read across from the right-hand end of the line.", post=" million.",
     phase="substitute"),
 box("Increase = later − earlier = ", 16, "Subtract the 1950 reading from the 2020 reading.", post=" million."),
 box("Percentage increase = increase ÷ starting value × 100 = ", 32,
     "Divide by the 1950 value, not the 2020 one, then multiply by 100.", post="%."),
 box("Check: take that percentage of 50 million and add it on. You get ", 66,
     "A third of 50 is roughly 16, and 50 + 16 should land on the 2020 reading.", post=" million.",
     done="It returns to the 2020 point, so the percentage was measured against the right value.")
]
s[1]["misconceptions"] = [
 mis("divided_by_the_new_value", "You have divided by the finishing value. Percentage change is always measured against the starting value.", 24,
     note="16/66*100 = 24.2 -> 24"),
 mis("gave_the_raw_increase", "That is the increase in millions, not a percentage. Divide it by the starting value, then multiply by 100.", 16)
]

s[2]["hint"] = "Add every bar on the chart, then count the bars you used to be sure none was missed."
s[2]["guided_steps"] = [
 box("The chart has one bar per vehicle type. The number of bars is ", 5,
     "Count the labels along the bottom axis.",
     say="A total means every bar, so start by knowing how many there are."),
 box("The tallest bar, cars, reads ", 95, "Its top sits half a step above the 90 gridline."),
 box("Vans and lorries read 40 and 25, so together they come to ", 65,
     "Add the two readings.", phase="substitute"),
 box("Buses and motorcycles are the same height. Doubling one of them gives ", 30,
     "Each reads 15, so add it to itself."),
 box("Adding your three subtotals gives a total of ", 190,
     "95 + 65 + 30.", post=" vehicles."),
 box("Check: the number of bars you have used is ", 5,
     "Count them: cars, vans, lorries, buses, motorcycles.",
     done="Five bars used and five bars on the chart, so nothing has been left out of the total.")
]
s[2]["misconceptions"] = [
 mis("left_a_bar_out", "One bar has been missed out of the total. Count the bars you added and compare that with the number on the chart.", 175,
     note="omitting motorcycles (15)"),
 mis("counted_the_bars", "That is how many bars there are, not how many vehicles. Add the bar heights rather than counting bars.", 5)
]

s[3]["hint"] = "Add all twelve bars for each city separately, then subtract one annual total from the other."
s[3]["guided_steps"] = [
 box("Each month has one bar per city. The number of pairs of bars on the chart is ", 12,
     "One pair per month along the bottom axis.",
     say="Annual totals mean every bar counts, so work through one city at a time."),
 box("Manchester's first six bars are 80, 60, 65, 55, 60, 70. They add to ", 390,
     "Add them in pairs if it helps: 80 + 60, then 65 + 55, then 60 + 70.", post=" mm."),
 box("Manchester's last six bars are 65, 75, 70, 85, 80, 75. They add to ", 450,
     "Again, add them in pairs.", post=" mm.", phase="substitute"),
 box("So Manchester's annual total is ", 840, "Add your two half-year subtotals.", post=" mm."),
 box("London's twelve bars are 55, 40, 42, 45, 50, 48, 47, 50, 52, 60, 65, 55. They add to ", 609,
     "Work in halves again: the first six, then the last six.", post=" mm."),
 box("The difference in annual rainfall is ", 231,
     "Subtract London's total from Manchester's.", post=" mm."),
 box("Check: add your difference back onto London's total and you get ", 840,
     "London's annual total plus the difference.",
     done="It lands exactly on Manchester's total, so the subtraction was the right way round.")
]
s[3]["misconceptions"] = [
 mis("used_one_month_only", "That is the gap for a single month, not for the year. Add all twelve bars for each city before you subtract.", 25,
     note="October: 85 - 60 = 25"),
 mis("added_the_totals", "You have added the two annual totals. A difference asks you to subtract one from the other.", 1449,
     note="840 + 609 = 1449")
]

s[4]["hint"] = "Work out the fall for each pair of years listed, then compare those falls."
s[4]["guided_steps"] = [
 box("The line runs from 2004 to 2010. The number of plotted points is ", 7,
     "One point per year along the bottom axis.",
     say="A decrease is a subtraction, so each option needs working out before you can compare them."),
 box("2004 reads 27 and 2005 reads 19, so the fall is ", 8, "Subtract the later value from the earlier one.",
     post=" thousand km²."),
 box("2005 to 2006 goes from 19 to 14, a fall of ", 5, "Same move, next pair.", post=" thousand km².",
     phase="substitute"),
 box("2008 to 2009 goes from 13 to 7, a fall of ", 6, "Same move again.", post=" thousand km²."),
 box("2006 to 2007 goes from 14 to 12, a fall of ", 2, "The gentlest section of the line.",
     post=" thousand km².",
     done="Four falls compared: 8, 5, 6 and 2. The steepest section of the line is the first one."),
 say("The biggest single-year fall is from <strong>2004 to 2005</strong>. Choose that option.")
]
s[4]["misconceptions"] = [
 mis("picked_a_later_steep_fall", "That pair does show a clear fall, but one earlier pair falls further. Work out every fall before choosing.", 3),
 mis("picked_the_lowest_point", "The line is at its lowest towards the right, but the question asks where it falls furthest in one step, not where it ends up lowest.", 2)
]

s[5]["hint"] = "Use the legend to find the tertiary colour, and read only the bars above the Country B label."
s[5]["guided_steps"] = [
 box("Each country has three bars, in the order primary, secondary, tertiary. Within Country B's group, tertiary is bar number ", 3,
     "The legend gives the order and the colours.",
     say="Two groups of three bars. Locate the right group before you read anything."),
 box("Country B's primary bar reads ", 55, "Primary is the green bar in Country B's group.", post="%."),
 box("Country B's secondary bar reads ", 15, "Secondary is the yellow bar in the same group.", post="%.",
     phase="substitute"),
 box("The three sectors must total 100%, so the tertiary bar should read ", 30,
     "Subtract your two readings from 100.", post="%."),
 box("Now read the tertiary bar itself. It reads ", 30, "The blue bar in Country B's group.", post="%.",
     done="Your prediction and your reading agree, and the three sectors add to 100%, so the reading is sound.")
]
s[5]["misconceptions"] = [
 mis("read_the_other_country", "You have read the tertiary bar from the other country's group. Check which group of three sits above the Country B label.", 75,
     note="Country A tertiary = 75"),
 mis("read_the_primary_bar", "That is Country B's primary bar. Use the legend to find which colour shows the tertiary sector.", 55)
]

s[6]["hint"] = "Find the hour of each peak along the bottom axis, then subtract one time from the other."
s[6]["guided_steps"] = [
 box("The bottom axis counts hours in steps of 4. Counting from the left, hour 16 is plotted point number ", 5,
     "The first point sits at hour 0, so count that as point 1.",
     say="Lag time is a gap between two times, so both peaks must be located on the bottom axis first."),
 box("The rainfall line peaks at hour ", 8, "Find the highest point on the rainfall line, then read down."),
 box("The discharge line peaks at hour ", 16,
     "Find the highest point on the discharge line, then read down.", phase="substitute"),
 box("Lag time = peak discharge time − peak rainfall time = ", 8, "Subtract the earlier hour from the later one.",
     post=" hours."),
 box("Check: add your lag time onto the rainfall peak hour and you get hour ", 16,
     "Rainfall peak hour plus the lag.",
     done="It lands on the discharge peak, so the lag has been measured the right way round.")
]
s[6]["misconceptions"] = [
 mis("gave_the_discharge_peak_time", "That is the hour the discharge peaks, not the gap between the two peaks. Subtract the rainfall peak hour from it.", 16),
 mis("subtracted_the_peak_heights", "You have subtracted the two peak heights. Lag time is measured along the bottom axis, in hours.", 10,
     note="18 - 8 = 10")
]

# ----------------------------------------------------------------- GOLD ----
g = pb["gold"]

g[0]["hint"] = "In a stacked bar, a section's size is the level at its top minus the level where it starts."
g[0]["guided_steps"] = [
 box("Three bars, one per year, each split into three stacked sections. Counting from the left, 2020 is bar number ", 3,
     "The years run 2000, 2010, 2020 along the bottom axis.",
     say="Stacked bars pile the sections on top of each other, so locate the right bar first."),
 box("The whole 2020 bar reaches the ", 100, "Read the very top of the bar across to the side axis.",
     post=" level.", done="A stacked percentage bar always fills to 100."),
 box("The two sections below tertiary are primary (1%) and secondary (23%). Together they reach the ", 24,
     "Add the two lower sections.", post=" level.", phase="substitute"),
 box("Tertiary fills the rest of the bar, so it is worth ", 76,
     "Take the level where tertiary starts away from the level at the top of the bar.", post="%."),
 box("Check: the three sections add to ", 100, "Add all three percentages together.",
     done="They fill the bar exactly, which is what a stacked percentage bar must do.")
]
g[0]["misconceptions"] = [
 mis("read_where_the_section_starts", "You have read the level where the tertiary section begins, not how tall it is. In a stacked bar, subtract the level below from the level above.", 24),
 mis("read_the_wrong_year", "That is a different year's tertiary section. Check the year label under the bar before you read it.", 73,
     note="2010 tertiary = 73")
]

g[1]["hint"] = "Use the legend colour to follow one country's line, then compare its first and last points."
g[1]["guided_steps"] = [
 box("Three lines share the chart. Each one has ", 5, "Count the labelled years along the bottom axis.",
     post=" plotted points.",
     say="Three lines means the legend matters. Pick out the right one before reading."),
 box("China's line starts in 2000 at ", 3000, "Use the legend colour, then read the left-hand end of that line.",
     post=" million tonnes."),
 box("China's line finishes in 2020 at ", 10000, "Read the right-hand end of the same line.",
     post=" million tonnes.", phase="substitute"),
 box("Increase = 2020 value − 2000 value = ", 7000, "Subtract the earlier reading from the later one.",
     post=" million tonnes."),
 box("Check: add your increase onto the 2000 reading and you get ", 10000,
     "The 2000 reading plus the increase.",
     done="It returns to the 2020 point on China's line, so the increase is right.")
]
g[1]["misconceptions"] = [
 mis("followed_the_wrong_line", "You have followed a different country's line. Match the legend colour before reading either point.", 1600,
     note="India 2600 - 1000 = 1600"),
 mis("gave_the_final_value", "That is the 2020 reading, not the change. Take the 2000 reading away from it.", 10000)
]

g[2]["display"] = ("The bar chart shows average monthly rainfall for a town. "
                   "Which statement best describes its rainfall pattern?")
g[2]["options"] = [
 "Wet all year, with the most rain in summer",
 "Dry summers and wet winters, a Mediterranean pattern",
 "Rain spread evenly through the year",
 "Almost no rain in any month"
]
g[2]["hint"] = "Compare the midsummer bars with the midwinter ones before you choose."
g[2]["guided_steps"] = [
 box("Twelve bars, January to December. Counting from the left, July is bar number ", 7,
     "January is bar 1, so count on from there.",
     say="A pattern question still starts with readings. Take one from midsummer and one from midwinter."),
 box("July's bar reads ", 5, "It is the shortest bar on the chart.", post=" mm."),
 box("December's bar reads ", 85, "It is the tallest bar on the chart.", post=" mm.", phase="substitute"),
 box("So December's rainfall is bigger than July's by a factor of ", 17,
     "Divide the taller reading by the shorter one.",
     done="A winter month with many times the rain of a midsummer month is the signature of dry summers and wet winters."),
 say("Dry summers, wet winters: that is the <strong>Mediterranean</strong> pattern. Choose that option.")
]
g[2]["misconceptions"] = [
 mis("summer_maximum", "The wettest bars sit at the two ends of the year, not in the middle. Compare the midsummer bars with the midwinter ones.", 0),
 mis("assumed_even_rainfall", "The bars are far from even: check the shortest bar against the tallest before you decide.", 2)
]

g[3]["display"] = ("The line graph shows life expectancy in the UK from 1900 to 2020. Calculate the average "
                   "increase in life expectancy per decade. Give your answer to the nearest whole year.")
g[3]["hint"] = "Find the total rise first, then divide it by the number of ten year blocks between the first and last year."
g[3]["guided_steps"] = [
 box("The bottom axis runs 1900 to 2020 in 20 year steps. The number of plotted points is ", 7,
     "Count the labelled years along the bottom axis.",
     say="An average per decade needs two things: the total rise, and how many decades it happened over."),
 box("The 1900 point reads ", 47, "Read the left-hand end of the line across to the side axis.", post=" years."),
 box("The 2020 point reads ", 81, "Read the right-hand end of the line.", post=" years.", phase="substitute"),
 box("Total increase across the whole period = ", 34, "Subtract the 1900 reading from the 2020 reading.",
     post=" years."),
 box("Between 1900 and 2020 the number of decades is ", 12,
     "That is 120 years, and a decade is ten years."),
 box("Dividing the increase by the number of decades, then rounding to the nearest whole year, gives ", 3,
     "34 ÷ 12 comes out just under 3.", post=" years per decade."),
 box("Check: multiply your rounded answer by 12 decades to get ", 36, "Your answer times 12.", post=" years.",
     done="36 years is close to the true rise of 34, so rounding to the nearest whole year is fair.")
]
g[3]["misconceptions"] = [
 mis("gave_the_total_rise", "That is the whole rise across 120 years. The question asks for the average rise in a single decade, so divide.", 34),
 mis("divided_by_the_points", "You have divided by the number of plotted points rather than the number of decades. Count how many ten year blocks fit between the first and last year.", 5,
     note="34/7 = 4.86 -> 5")
]

g[4]["hint"] = "Stage 3 begins where the birth rate line starts falling steeply, after the death rate has already dropped."
g[4]["guided_steps"] = [
 box("Two lines share the chart, one per rate. The bottom axis runs 1960 to 2020, so each line has ", 7,
     "Count the labelled years along the bottom axis.", post=" plotted points.",
     say="Stage 3 is about which line is falling and when, so measure both falls."),
 box("The death rate goes from 25 in 1960 to 12 in 1980, a fall of ", 13,
     "Subtract the later reading from the earlier one."),
 box("Over the same years the birth rate goes from 45 to 40, a fall of only ", 5,
     "Same move, this time on the birth rate line.", phase="substitute"),
 box("From 1980 to 2000 the birth rate goes from 40 to 24, a fall of ", 16,
     "Subtract the 2000 reading from the 1980 reading.",
     done="The death rate did its falling first, while the birth rate barely moved. The birth rate only starts dropping steeply after 1980, and that switch is Stage 3."),
 say("The country enters Stage 3 in <strong>1980</strong>. Choose that option.")
]
g[4]["misconceptions"] = [
 mis("picked_the_start", "In 1960 both rates are still high and the birth rate has barely moved. Look for where the birth rate begins its steep fall.", 0),
 mis("picked_too_late", "By 2000 the birth rate has already been falling for years. Stage 3 starts when that fall begins, not part way through it.", 2)
]

# ------------------------------------------------------------------ write --
out = os.path.join(HERE, "lesson_L01.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("wrote", out, os.path.getsize(out))
