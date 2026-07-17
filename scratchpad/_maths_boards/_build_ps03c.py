# -*- coding: utf-8 -*-
import json
ns = {}
exec(compile(open("_build_ps03.py", encoding="utf-8").read(), "_build_ps03.py", "exec"), ns)
pie = ns["pie"]; barchart = ns["barchart"]; stacked_bar = ns["stacked_bar"]; semicircle_opener = ns["semicircle_opener"]

pd = json.load(open("_stage2.json", encoding="utf-8"))

def box(pre, answer, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}; d.update(kw); return d
def say(s): return {"say": s}

# ================= tier_guides =================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: reading charts and simple fractions",
        "steps": [
            "<strong>Bar charts:</strong> follow the top of a bar across to the number axis. Each gridline is worth the scale shown, so a bar 3 gridlines up on a scale of 5 means 15.",
            "<strong>Pie fractions:</strong> a slice's fraction is its frequency over the total. Simplify by dividing top and bottom by the same number.",
            "For 'how many more', read both values, then subtract the smaller from the larger."],
        "example": {"question": "A bar chart shows Red = 12, Blue = 20. How many more chose blue?",
            "steps": [
                {"label": "Read", "content": "Blue = 20, Red = 12"},
                {"label": "Subtract", "content": "20 − 12 = 8"},
                {"label": "Check", "content": "12 + 8 = 20"},
                {"label": "Answer", "content": "8 more chose blue", "isAnswer": True, "is_answer": True}]}},
    "silver": {
        "title": "Silver: comparing data and pie chart angles",
        "steps": [
            "<strong>Angle to frequency:</strong> divide the angle by 360 to get the fraction, then multiply by the total.",
            "<strong>Frequency to angle:</strong> divide the frequency by the total, then multiply by 360.",
            "<strong>Missing angle:</strong> all sectors add to 360°, so subtract the known angles from 360.",
            "<strong>Range:</strong> highest value minus lowest value."],
        "example": {"question": "A pie chart shows 90 people. Sector B is 40°. How many people is that?",
            "steps": [
                {"label": "Fraction", "content": "40 ÷ 360 = 1/9"},
                {"label": "Multiply", "content": "1/9 × 90 = 10"},
                {"label": "Check", "content": "(10 ÷ 90) × 360 = 40°"},
                {"label": "Answer", "content": "10 people", "isAnswer": True, "is_answer": True}]}},
    "gold": {
        "title": "Gold: composite charts and lines of best fit",
        "steps": [
            "<strong>Composite (stacked) bars:</strong> read each part, add them for the total, then find one part as a percentage: part ÷ total × 100.",
            "<strong>Line of best fit:</strong> substitute the x-value into the equation to estimate y, or read straight up from the axis.",
            "<strong>Reliability:</strong> estimating inside the data range (interpolation) is safe; outside it (extrapolation) is unreliable."],
        "example": {"question": "A stacked bar shows A = 30, B = 20 in one month. What percentage is A?",
            "steps": [
                {"label": "Total", "content": "30 + 20 = 50"},
                {"label": "Percentage", "content": "(30 ÷ 50) × 100 = 60%"},
                {"label": "Check", "content": "60% of 50 = 30"},
                {"label": "Answer", "content": "60%", "isAnswer": True, "is_answer": True}]}}}

# ================= guided.opener =================
pd["guided"] = {}
pd["guided"]["opener"] = {"steps": [
    say("Picture a class of 20 students. Exactly half of them, 10, chose football. Here is that split drawn as a circle."),
    dict(box("Half of the class chose football. How many students is half of 20? ", 10, "Half of 20."),
         display=semicircle_opener()),
    box("A full circle is 360°. The football half is half of the circle. How many degrees is half of 360? ", 180, "Half of 360."),
    say("You just built a pie chart slice. The fraction of people (a half) is the same as the fraction of the circle. So <strong>angle = fraction × 360°</strong>. That single idea is the whole method for pie charts.")]}

# ================= guided.teach =================
# BRONZE teach: read a bar chart (Cats 14, Dogs 22, Fish 6, Birds 8)
teach_bronze_svg = barchart(["Cats", "Dogs", "Fish", "Birds"], [14, 22, 6, 8], 25, 5,
    "Number of pets", "Bar chart of pets: Cats 14, Dogs 22, Fish 6, Birds 8")
pd["guided"]["teach"] = {}
pd["guided"]["teach"]["bronze"] = {
    "display": teach_bronze_svg + "The bar chart shows pets owned by a class. How many more chose dogs than fish?",
    "steps": [
        say("Read the two bars the question names, then compare them."),
        box("Read the Dogs bar: ", 22, "Dogs reach 22."),
        box("Read the Fish bar: ", 6, "Fish reach 6."),
        box("How many more chose dogs? 22 − 6 = ", 16, "Subtract fish from dogs."),
        box("Check: Fish plus your answer should give Dogs. 6 + 16 = ", 22, "Returns to 22.", done="16 more chose dogs. Read, then compare.")]}

# SILVER teach: pie angle -> frequency (240 people, Tea 54 deg -> 36)
teach_silver_svg = pie([(54, "#60a5fa", "Tea 54°"), (306, "#94a3b8", "Other")],
    "A pie chart with a Tea sector of 54 degrees")
pd["guided"]["teach"]["silver"] = {
    "display": teach_silver_svg + "The pie chart shows 240 people's favourite drink. The Tea sector is 54°. How many chose tea?",
    "steps": [
        say("Angle over 360 gives the fraction of people. Then scale to the total."),
        box("How many degrees in a full circle? ", 360, "A full turn is 360°."),
        box("Fraction that is Tea: 54 ÷ 360 = ", 0.15, "54 divided by 360."),
        box("Multiply by the total people: 0.15 × 240 = ", 36, "0.15 of 240."),
        box("Check: 36 out of 240 as an angle = (36 ÷ 240) × 360 = ", 54, "Returns to 54°.", done="36 chose tea. Angle to fraction to people.")]}

# GOLD teach: composite bar percentage (Books 30, Toys 10, Games 10 -> Books 60%)
teach_gold_svg = stacked_bar([("Books", 30, "#60a5fa"), ("Toys", 10, "#f59e0b"), ("Games", 10, "#34d399")], 50, 50,
    "A stacked bar for Term 1: Books 30, Toys 10, Games 10")
pd["guided"]["teach"]["gold"] = {
    "display": teach_gold_svg + "The stacked bar shows Term 1 sales (£ thousands): Books 30, Toys 10, Games 10. What percentage were Books?",
    "steps": [
        say("Find the total of the stack, then Books as a share of it."),
        box("Add the parts: 30 + 10 + 10 = ", 50, "Add all three."),
        box("Books as a fraction: 30 ÷ 50 = ", 0.6, "30 out of 50."),
        box("As a percentage: 0.6 × 100 = ", 60, "Multiply by 100."),
        box("Check: 60% of 50 = 0.6 × 50 = ", 30, "Returns to the Books value.", done="Books = 60%. Total, share, percentage.")]}

# ================= method_card (slim) =================
pd["method_card"] = {
    "title": "Representing Data",
    "steps": [
        "Bar charts: read a bar's height against the number axis (mind the scale).",
        "Pie charts: angle = (frequency ÷ total) × 360; and frequency = (angle ÷ 360) × total.",
        "Scatter graphs: describe correlation, and use the line of best fit to estimate.",
        "Interpolation (inside the data) is reliable; extrapolation (outside) is not."],
    "content": "<p><strong>Pie charts:</strong> angle over 360 is the fraction of the total. To find a frequency, do (angle ÷ 360) × total. To find an angle, do (frequency ÷ total) × 360. All sectors add to 360°.</p><p><strong>Scatter graphs:</strong> positive correlation means both rise together; negative means one rises as the other falls. The line of best fit passes through the mean point and estimates values within the data range.</p>",
    "example": "<p><strong>A pie chart represents 120 people. The Bus sector is 90°. How many travel by bus?</strong></p><p>(90 ÷ 360) × 120 = 30 people</p>"}

json.dump(pd, open("lesson_maths-aqa_probability-statistics-L03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FINAL written")
