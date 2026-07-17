# -*- coding: utf-8 -*-
import json, importlib.util, sys

# import svg helpers from _build_ps03 by exec
ns = {}
exec(compile(open("_build_ps03.py", encoding="utf-8").read(), "_build_ps03.py", "exec"), ns)
pie = ns["pie"]; two_pies = ns["two_pies"]; barchart = ns["barchart"]
stacked_bar = ns["stacked_bar"]; semicircle_opener = ns["semicircle_opener"]

pd = json.load(open("_stage1.json", encoding="utf-8"))
B = pd["problem_bank"]["bronze"]
S = pd["problem_bank"]["silver"]
G = pd["problem_bank"]["gold"]

def box(pre, answer, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    d.update(kw)
    return d
def say(s):
    return {"say": s}

# ================= HINTS =================
B[0]["hint"] = "Follow the top of the Football bar across to the number axis."
B[1]["hint"] = "Read the Blue and Green bars, then subtract the smaller from the larger."
B[2]["hint"] = "Write car over total, then divide both by their highest common factor."
B[3]["hint"] = "Add the heights of all five bars together."
B[4]["hint"] = "Angle over 360 gives the fraction; multiply that by 200."
B[5]["hint"] = "Fraction of people times 360 gives the angle."
B[6]["hint"] = "Find the tallest bar and read its value."
B[7]["hint"] = "As one quantity rises, does the other rise or fall?"
S[0]["hint"] = "Read both Drama bars, then subtract boys from girls."
S[1]["hint"] = "Check whether sales rise or fall as temperature rises."
S[2]["hint"] = "The four angles add to 360, so subtract the three you know."
S[3]["hint"] = "Angle over 360 gives the fraction; multiply by 150."
S[4]["hint"] = "Range is the highest value minus the lowest value."
S[5]["hint"] = "The modal class is the group with the highest frequency."
S[6]["hint"] = "Check whether reaction time rises or falls as age rises."
G[0]["hint"] = "Add the three Q1 parts for the total, then divide Electronics by it and times 100."
G[1]["hint"] = "Work out the football fans for each school using angle over 360 times the total."
G[2]["hint"] = "Put x = 8 into the equation and work it out."
G[3]["hint"] = "Is x = 20 inside or outside the data range 2 to 12?"
G[4]["hint"] = "Read the errors value straight up from 6 hours on the trend."

# ================= MISCONCEPTIONS (honest, expect derived) =================
B[0]["misconceptions"] = [
    {"pattern": "gridline_not_scaled", "message": "Each gridline is worth 5, not 1. The Football bar is 6 gridlines up, so 6 × 5 = 30.", "expect": 6, "note": "counts gridlines"}]
B[1]["misconceptions"] = [
    {"pattern": "added_not_subtracted", "message": "The question asks how many MORE, so subtract: 25 − 15 = 10, not add.", "expect": 40, "note": "25+15"}]
B[2]["misconceptions"] = [
    {"pattern": "not_simplified", "message": "40/80 is right but not simplified. Divide top and bottom by 40 to get 1/2.", "expect": [40, 80], "note": "unsimplified"}]
B[3]["misconceptions"] = [
    {"pattern": "missed_a_bar", "message": "Add every bar, including Size 9. 3 + 9 + 10 + 6 + 4 = 32.", "expect": 28, "note": "drops the 4"}]
B[4]["misconceptions"] = [
    {"pattern": "angle_as_count", "message": "72 is the angle, not the number of students. Multiply the fraction 72/360 by 200 to get 40.", "expect": 72, "note": "reports angle"}]
B[5]["misconceptions"] = [
    {"pattern": "times_total_not_360", "message": "Multiply the fraction by 360°, not by the number of people. (45/180) × 360 = 90.", "expect": 45, "note": "times 180"}]
B[6]["misconceptions"] = [
    {"pattern": "second_tallest", "message": "Wednesday reaches 22, but Thursday is taller at 25, so the highest temperature is 25.", "expect": 22, "note": "picks Wednesday"}]
B[7]["misconceptions"] = [
    {"pattern": "mislabels_trend", "message": "As revision hours rise, the score rises too, so this is positive correlation.", "expect": None}]
S[0]["misconceptions"] = [
    {"pattern": "added_not_subtracted", "message": "How many MORE girls means subtract boys from girls: 25 − 10 = 15, not add.", "expect": 35, "note": "25+10"}]
S[1]["misconceptions"] = [
    {"pattern": "mislabels_trend", "message": "As temperature rises, sales rise too, so this is positive correlation.", "expect": None}]
S[2]["misconceptions"] = [
    {"pattern": "forgot_subtract", "message": "260° is the total of the three known angles. The fourth is 360 − 260 = 100.", "expect": 260, "note": "stops at the sum"}]
S[3]["misconceptions"] = [
    {"pattern": "angle_as_count", "message": "96 is the angle, not the number of people. Work out (96/360) × 150 = 40.", "expect": 96, "note": "reports angle"}]
S[4]["misconceptions"] = [
    {"pattern": "gave_maximum", "message": "22 is the highest temperature, not the range. Range = highest − lowest = 22 − 12 = 10.", "expect": 22, "note": "gives max"}]
S[5]["misconceptions"] = [
    {"pattern": "used_midpoint", "message": "The modal class is the group with the highest frequency (15), which is 10 to 20.", "expect": None}]
S[6]["misconceptions"] = [
    {"pattern": "mislabels_trend", "message": "As age rises, reaction time rises too, so this is positive correlation.", "expect": None}]
G[0]["misconceptions"] = [
    {"pattern": "count_not_percent", "message": "40 is the number of sales, not the percentage. Divide by the Q1 total (80) and times 100 to get 50%.", "expect": 40, "note": "gives count"}]
G[1]["misconceptions"] = [
    {"pattern": "angle_only", "message": "School A: (90/360) × 200 = 50. School B: (60/360) × 300 = 50. Both have 50, so they are equal.", "expect": None}]
G[2]["misconceptions"] = [
    {"pattern": "forgot_plus_c", "message": "You found 3 × 8 = 24 but forgot the + 10. y = 24 + 10 = 34.", "expect": 24, "note": "drops +10"},
    {"pattern": "added_coeff", "message": "3x means 3 times x, not 3 plus x. Work out 3 × 8 = 24, then add 10 to get 34.", "expect": 21, "note": "3+8+10"}]
G[3]["misconceptions"] = [
    {"pattern": "trusts_lobf", "message": "x = 20 is outside the data range 2 to 12, so this is extrapolation and is unreliable.", "expect": None}]
G[4]["misconceptions"] = [
    {"pattern": "read_wrong_x", "message": "That is the value at 5 hours of sleep. At 6 hours the trend gives about 8 errors.", "expect": 10, "note": "reads x=5"}]

# ================= fix em dashes in preserved MC options =================
G[1]["options"] = ["Equal: both have 50 fans",
                   "School A has 50, School B has 50, they are equal",
                   "School B has 50 vs School A's 50, they are equal",
                   "School A has more by 10"]
G[3]["options"] = ["No, this is extrapolation (outside the data range)",
                   "Yes, the line of best fit is always accurate",
                   "Yes, if the correlation is strong it's fine",
                   "No, because x = 20 is a negative value"]

# ================= SVG FIGURES on text-only pie problems =================
B[4]["display"] = pie([(72, "#60a5fa", "Science 72°"), (288, "#94a3b8", "Other")],
    "A pie chart with a Science sector of 72 degrees") + \
    "The pie chart represents 200 students. The Science sector has an angle of 72°. How many students chose Science?"
S[2]["display"] = pie([(120, "#60a5fa", "120°"), (80, "#f59e0b", "80°"), (60, "#34d399", "60°"), (100, "#f472b6", "?")],
    "A pie chart with three known sectors of 120, 80 and 60 degrees and one unknown sector") + \
    "The pie chart has four sectors. Three angles are 120°, 80° and 60°. Find the angle of the fourth sector."
S[3]["display"] = pie([(96, "#60a5fa", "A 96°"), (264, "#94a3b8", "Other")],
    "A pie chart with sector A of 96 degrees") + \
    "The pie chart represents 150 people. Sector A has an angle of 96°. How many people does sector A represent?"
G[1]["display"] = two_pies(
    [(90, "#60a5fa", "90°"), (270, "#94a3b8", "")], "School A (200)",
    [(60, "#f59e0b", "60°"), (300, "#94a3b8", "")], "School B (300)",
    "Two pie charts: School A with a 90 degree football sector, School B with a 60 degree football sector") + \
    "School A has 200 students (Football sector 90°). School B has 300 students (Football sector 60°). Which school has more football fans and by how many?"

# ================= GUIDED_STEPS on every non-MC problem =================
B[0]["guided_steps"] = [
    say("Read the Football bar against the number axis. Each gridline is worth 5 students."),
    box("The Football bar reaches how many gridlines above zero? ", 6, "It lines up 6 gridlines up."),
    dict(box("Each gridline is 5 students, so 6 × 5 = ", 30, "Multiply the gridlines by 5."), phase="substitute"),
    box("Check against the chart: the Football bar sits level with which number? ", 30, "It lines up with 30.", done="Football = 30 students.")]

B[1]["guided_steps"] = [
    say("Read both bars first, then compare them."),
    box("Read the Blue bar: ", 25, "Blue reaches 25."),
    box("Read the Green bar: ", 15, "Green reaches 15."),
    dict(box("How many more chose blue? 25 − 15 = ", 10, "Subtract green from blue."), phase="substitute"),
    box("Check: Green plus your answer should give Blue. 15 + 10 = ", 25, "It returns to 25.", done="10 more chose blue.")]

B[2]["guided_steps"] = [
    say("A fraction is the part over the whole, then simplify."),
    box("How many people travel by car? ", 40, "The Car sector shows 40."),
    box("How many people in total? ", 80, "80 people altogether."),
    dict(box("Simplify 40/80 by dividing both by 40. Top: 40 ÷ 40 = ", 1, "40 divided by 40."), phase="substitute"),
    box("Bottom: 80 ÷ 40 = ", 2, "80 divided by 40."),
    box("Check: does 1/2 of 80 equal 40? 80 ÷ 2 = ", 40, "Yes, it returns to 40.", done="Fraction = 1/2.")]

B[3]["guided_steps"] = [
    say("The total is the sum of every bar. The bars read 3, 9, 10, 6, 4."),
    box("Add the first two bars: 3 + 9 = ", 12, "Three plus nine."),
    dict(box("Add the next bar: 12 + 10 = ", 22, "Add ten."), phase="substitute"),
    box("Add the next: 22 + 6 = ", 28, "Add six."),
    box("Add the last: 28 + 4 = ", 32, "Add four."),
    box("Check another way: (3 + 4) + (9 + 6) + 10 = 7 + 15 + 10 = ", 32, "Same total.", done="32 students in total.")]

B[4]["guided_steps"] = [
    say("Angle over 360 gives the fraction of students. Then scale up to the total."),
    box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
    dict(box("Fraction that is Science: 72 ÷ 360 = ", 0.2, "72 divided by 360."), phase="substitute"),
    box("Multiply by the total students: 0.2 × 200 = ", 40, "0.2 of 200."),
    box("Check: 40 out of 200 as an angle = (40 ÷ 200) × 360 = ", 72, "Returns to 72°.", done="Science = 40 students.")]

B[5]["guided_steps"] = [
    say("Frequency over total gives the fraction of the circle. Multiply by 360 for the angle."),
    box("Simplify 45/180 by dividing both by 45. Bottom: 180 ÷ 45 = ", 4, "180 divided by 45, so the fraction is 1/4."),
    dict(box("Angle = (1/4) × 360 = 360 ÷ 4 = ", 90, "Divide 360 by 4."), phase="substitute"),
    box("Check: a 90° sector out of 180 people = (90 ÷ 360) × 180 = ", 45, "Returns to 45.", done="The Walk sector is 90°.")]

B[6]["guided_steps"] = [
    say("The highest temperature is the tallest bar. Compare the top candidates."),
    box("The two tallest bars are Wednesday and Thursday. Read Wednesday: ", 22, "Wednesday reaches 22."),
    dict(box("Read Thursday: ", 25, "Thursday reaches 25."), phase="substitute"),
    box("Thursday (25) beats Wednesday (22), so the highest temperature is ", 25, "The taller bar wins.", done="Highest = 25°C.")]

S[0]["guided_steps"] = [
    say("Read both Drama bars, then find the difference."),
    box("Read the Girls Drama bar: ", 25, "Girls reach 25."),
    box("Read the Boys Drama bar: ", 10, "Boys reach 10."),
    dict(box("How many more girls? 25 − 10 = ", 15, "Subtract boys from girls."), phase="substitute"),
    box("Check: Boys plus your answer should give Girls. 10 + 15 = ", 25, "Returns to 25.", done="15 more girls chose Drama.")]

S[2]["guided_steps"] = [
    say("Every sector of a pie chart adds to 360°."),
    box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
    box("Add the two largest known angles: 120 + 80 = ", 200, "One hundred and twenty plus eighty."),
    dict(box("Add the third: 200 + 60 = ", 260, "Add sixty."), phase="substitute"),
    box("Fourth angle = 360 − 260 = ", 100, "Subtract from 360."),
    box("Check: 120 + 80 + 60 + 100 = ", 360, "They fill the circle.", done="Fourth angle = 100°.")]

S[3]["guided_steps"] = [
    say("Angle over 360 gives the fraction of people. Simplify to keep numbers whole."),
    box("Simplify 96/360 by dividing both by 24. Top: 96 ÷ 24 = ", 4, "96 divided by 24."),
    box("Bottom: 360 ÷ 24 = ", 15, "360 divided by 24, so the fraction is 4/15."),
    dict(box("People = (4/15) × 150 = 4 × (150 ÷ 15) = 4 × 10 = ", 40, "150 divided by 15 is 10, times 4."), phase="substitute"),
    box("Check: 40 out of 150 as an angle = (40 ÷ 150) × 360 = ", 96, "Returns to 96°.", done="Sector A = 40 people.")]

S[4]["guided_steps"] = [
    say("Range is the gap between the highest and lowest points on the line."),
    box("Read the highest point (Friday): ", 22, "The peak is 22."),
    box("Read the lowest point (Monday): ", 12, "The lowest is 12."),
    dict(box("Range = highest − lowest = 22 − 12 = ", 10, "Subtract the lowest from the highest."), phase="substitute"),
    box("Check: lowest plus range = 12 + 10 = ", 22, "Returns to the peak.", done="Range = 10°C.")]

G[0]["guided_steps"] = [
    say("For a percentage of the stack, find the Q1 total, then Electronics as a share of it."),
    box("Q1 total: 40 + 20 + 20 = ", 80, "Add all three Q1 parts."),
    dict(box("Electronics as a fraction: 40 ÷ 80 = ", 0.5, "40 out of 80."), phase="substitute"),
    box("As a percentage: 0.5 × 100 = ", 50, "Multiply by 100."),
    box("Check: 50% of 80 = 0.5 × 80 = ", 40, "Returns to the Electronics value.", done="Electronics = 50% of Q1.")]

G[2]["guided_steps"] = [
    say("Substitute the x-value into the line of best fit equation y = 3x + 10."),
    box("Work out 3x: 3 × 8 = ", 24, "Three times eight."),
    dict(box("Add 10: 24 + 10 = ", 34, "Add the constant."), phase="substitute"),
    box("Check: reverse it. (34 − 10) ÷ 3 = ", 8, "Returns to x = 8.", done="Estimated y = 34.")]

G[4]["guided_steps"] = [
    say("Estimate by reading the trend at x = 6. Use the points either side."),
    box("The point at x = 5 reads how many errors? ", 10, "At 5 hours, 10 errors."),
    box("The point at x = 7 reads how many errors? ", 6, "At 7 hours, 6 errors."),
    dict(box("x = 6 is halfway between them: (10 + 6) ÷ 2 = ", 8, "Average the two values."), phase="substitute"),
    box("Check against the plotted point at x = 6: it reads ", 8, "The trend gives 8.", done="About 8 errors at 6 hours.")]

json.dump(pd, open("_stage2.json", "w", encoding="utf-8"), ensure_ascii=False)
print("stage 2 ok")
