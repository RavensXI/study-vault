# -*- coding: utf-8 -*-
import json, io, copy

SRC = "_live_gl01.json"
OUT = "lesson_maths-eduqas_graphs-L01.json"

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

# ---------- 1. Bank repair: strip em dashes from worked_examples labels ----------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------- 2. Misconceptions: add expect (honest diagnosis) + fix silver[6] ----------
# (tier, index) -> (expect, optional new message)
MISC = {
    ("bronze",0): (0.5, "Gradient is rise ÷ run = (9 − 1) ÷ (4 − 0) = 8 ÷ 4 = 2. Do not put the run on top."),
    ("bronze",1): (5,   "In y = mx + c the y-intercept is c, the constant. Here c = 2, not the gradient 5."),
    ("bronze",2): (-4,  "In y = mx + c the gradient is the number multiplying x. Here m = 3, not the intercept −4."),
    ("bronze",3): (10,  "Multiply before adding: y = 2(4) + 1 = 8 + 1 = 9, not 2(4 + 1)."),
    ("bronze",4): (2,   "2 is where the line starts (the y-intercept). The question asks for y at x = 2, which is 8."),
    ("bronze",5): (0.5, "Rise = 13 − 7 = 6, run = 3 − 0 = 3. Gradient = 6 ÷ 3 = 2, not run over rise."),
    ("bronze",6): (2,   "The gradient keeps its sign. The line goes downhill, so m = −2, not 2."),
    ("bronze",7): (2,   "The line falls from left to right, so the gradient is negative: −2, not 2."),
    ("silver",0): (2,   "Subtract the coordinates in the same order top and bottom. y falls, so the gradient is −2, not 2."),
    ("silver",1): (19,  "−3 × 4 = −12, not 12. Then −12 + 7 = −5."),
    ("silver",2): (1,   "The line crosses below the axis, at y = −1, so the intercept is −1, not 1."),
    ("silver",3): (23,  "The line starts at −3, so subtract: 20 − 3 = 17, not 20 + 3."),
    ("silver",4): (11,  "The x-term is half of 8, which is 4, not 8. So k = 4 + 3 = 7."),
    ("silver",5): (6,   "3 − (−1) = 4, not 2. Subtracting a negative adds. Gradient = 12 ÷ 4 = 3."),
    ("silver",6): (None,"The x-values are the same (both 2), so the line is vertical. The run (change in x) is 0, and dividing by 0 is undefined, so a vertical line has no gradient."),
    ("gold",0):   (-15, "2 − (−3) = 5, not −1. Subtracting a negative adds. Gradient = 15 ÷ 5 = 3."),
    ("gold",1):   (5,   "c is not just the y-value. Substitute a point: 5 = 2(1) + c gives c = 3."),
    ("gold",2):   (-0.5,"Subtract the 6 first: −2 − 6 = −8, then divide by 4 to get m = −2."),
    ("gold",3):   (6,   "2 − (−4) = 6, not −2. The gradient is −12 ÷ 6 = −2."),
    ("gold",4):   (9,   "Divide the whole equation by 3 first: y = 3x − 4. The gradient is 3, not 9."),
}
for (t,i),(expect,msg) in MISC.items():
    p = pb[t][i]
    ms = p.get("misconceptions") or []
    if not ms:
        ms = [{"check":"common","pattern":"common","message":msg}]
        p["misconceptions"] = ms
    ms[0]["message"] = msg
    ms[0]["expect"] = expect

# ---------- 3. Hints per problem ----------
HINTS = {
    ("bronze",0):"Gradient is the change in y divided by the change in x.",
    ("bronze",1):"The y-intercept is the constant term, the number with no x.",
    ("bronze",2):"The gradient is the number multiplying x.",
    ("bronze",3):"Substitute x = 4: work out 2 × 4 first, then add 1.",
    ("bronze",4):"Go up from x = 2 to the line, then read across to the y-axis.",
    ("bronze",5):"Gradient is the change in y divided by the change in x.",
    ("bronze",6):"Include the minus sign: the gradient is the number multiplying x.",
    ("bronze",7):"The line falls, so the gradient is negative: count the drop in y for a step of 1 in x.",
    ("silver",0):"Subtract y-values on top, x-values on the bottom, in the same order; keep the minus sign.",
    ("silver",1):"Work out −3 × 4 first, that is −12, then add 7.",
    ("silver",2):"Read where the line crosses the vertical axis, at x = 0.",
    ("silver",3):"The equation is y = 4x − 3. Work out 4 × 5, then subtract 3.",
    ("silver",4):"k is the y-value at x = 8: work out half of 8, then add 3.",
    ("silver",5):"Change in x is 3 − (−1) = 4; subtracting a negative adds.",
    ("silver",6):"Both points have x = 2. What happens to the run, the change in x?",
    ("gold",0):"Subtracting a negative adds: 8 − (−7) = 15 and 2 − (−3) = 5.",
    ("gold",1):"Find the gradient first, then put one point into y = mx + c and solve for c.",
    ("gold",2):"Put x = 4, y = −2 in: −2 = 4m + 6, then solve for m.",
    ("gold",3):"Change in y is −1 − 11 = −12; change in x is 2 − (−4) = 6.",
    ("gold",4):"Divide every term by 3 to reach y = mx + c, then read the gradient.",
}
for (t,i),h in HINTS.items():
    pb[t][i]["hint"] = h

# ---------- 4. guided_steps per problem ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre":pre, "post":post, "answer":answer, "hint":hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s): return {"say":s}

GS = {
("bronze",0):[
  say("Gradient is rise ÷ run: the change in y over the change in x."),
  box("Change in y: 9 − 1 = ", 8, "Subtract the y-values."),
  box("Change in x: 4 − 0 = ", 4, "Subtract the x-values."),
  box("Gradient = 8 ÷ 4 = ", 2, "Divide the rise by the run.", phase="substitute"),
  box("Check: y climbs by 2 for each of the 4 steps, so 2 × 4 = ", 8, "Multiply gradient by run.", done="This matches the rise of 8, so the gradient is 2."),
],
("bronze",1):[
  say("Compare with \\(y = mx + c\\). The y-intercept is \\(c\\), the number with no x."),
  box("The number multiplying x (gradient m) = ", 5, "Read the coefficient of x."),
  box("The number on its own (y-intercept c) = ", 2, "Read the constant term.", phase="substitute"),
  box("Check at x = 0: 5 × 0 + 2 = ", 2, "Put x = 0 into the equation.", done="At x = 0 the line is at y = 2, which is exactly the y-intercept."),
],
("bronze",2):[
  say("In \\(y = mx + c\\), the gradient is \\(m\\), the number multiplying x."),
  box("The number multiplying x = ", 3, "Read the coefficient of x."),
  box("The y-intercept c (number on its own) = ", -4, "Read the constant, with its sign.", phase="substitute"),
  box("Check the gradient: from x = 0 (y = −4) to x = 1, y = 3 × 1 − 4 = ", -1, "Put x = 1 in.", done="y rose from −4 to −1, a rise of 3, confirming gradient 3."),
],
("bronze",3):[
  say("Substitute \\(x = 4\\) into \\(y = 2x + 1\\)."),
  box("First, 2 × 4 = ", 8, "Multiply before adding."),
  box("Then add 1: 8 + 1 = ", 9, "Add the intercept.", phase="substitute"),
  box("Check at x = 0: 2 × 0 + 1 = ", 1, "Put x = 0 in.", done="The line starts at 1 and adds 2 per step; four steps add 8, giving 9."),
],
("bronze",4):[
  say("Read the graph. First find where the line crosses the y-axis."),
  box("The line crosses the y-axis at y = ", 2, "Read the value at x = 0."),
  box("For each step of 1 in x, the line climbs by ", 3, "Compare (0, 2) and (1, 5)."),
  box("So at x = 2: 2 + 3 × 2 = ", 8, "Start value plus two climbs.", phase="substitute"),
  box("Read straight off the graph at x = 2: y = ", 8, "Go up to the line, across to the y-axis.", done="The calculation and the graph agree, y = 8."),
],
("bronze",5):[
  say("Gradient is rise ÷ run."),
  box("Change in y: 13 − 7 = ", 6, "Subtract the y-values."),
  box("Change in x: 3 − 0 = ", 3, "Subtract the x-values."),
  box("Gradient = 6 ÷ 3 = ", 2, "Divide rise by run.", phase="substitute"),
  box("Check: y rises by 2 for each of the 3 steps, so 2 × 3 = ", 6, "Multiply gradient by run.", done="This matches the rise of 6, gradient 2 confirmed."),
],
("bronze",6):[
  say("The gradient is the number multiplying x, including its sign."),
  box("The number multiplying x = ", -2, "Read the coefficient of x, with its sign."),
  box("The y-intercept c = ", 9, "Read the constant term.", phase="substitute"),
  box("Check the sign at x = 1: −2 × 1 + 9 = ", 7, "Put x = 1 in.", done="y fell from 9 to 7 as x rose by 1, a change of −2, confirming a negative gradient."),
],
("bronze",7):[
  say("Pick two clear points on the line and use rise ÷ run."),
  box("From x = 0 to x = 1, y changes from 10 to 8, a change of ", -2, "It falls, so the change is negative."),
  box("The matching change in x is ", 1, "One step across."),
  box("Gradient = −2 ÷ 1 = ", -2, "Divide the fall by the run.", phase="substitute"),
  box("Check over a bigger gap: from (0, 10) to (5, 0), −10 ÷ 5 = ", -2, "Total fall over total run.", done="Same gradient, −2, the line goes downhill."),
],
("silver",0):[
  say("Gradient is rise ÷ run; keep the signs."),
  box("Change in y: 1 − 9 = ", -8, "y falls, so this is negative."),
  box("Change in x: 5 − 1 = ", 4, "Subtract the x-values."),
  box("Gradient = −8 ÷ 4 = ", -2, "Divide, keeping the minus.", phase="substitute"),
  box("Check: 4 steps at −2 each, 4 × (−2) = ", -8, "Multiply gradient by run.", done="This matches the fall of 8, gradient −2."),
],
("silver",1):[
  say("Substitute \\(x = 4\\) into \\(y = -3x + 7\\)."),
  box("First, −3 × 4 = ", -12, "A negative times a positive is negative."),
  box("Then add 7: −12 + 7 = ", -5, "Add the intercept.", phase="substitute"),
  box("Check at x = 0: −3 × 0 + 7 = ", 7, "Put x = 0 in.", done="The line starts at 7 and drops 3 per step; four steps drop 12, giving −5."),
],
("silver",2):[
  say("The y-intercept is where the line crosses the y-axis, the vertical axis at \\(x = 0\\)."),
  box("Find x = 0 and read the y-value there: y = ", -1, "Look where the line cuts the vertical axis."),
  box("Check the gradient: from x = 0 (y = −1) to x = 1 (y = 3), y rises by ", 4, "Subtract the y-values."),
  box("So the line is y = 4x − 1. At x = 0 this gives y = ", -1, "Put x = 0 in.", phase="substitute"),
  box("The axis crossing confirms the y-intercept = ", -1, "Read straight off the y-axis.", done="The line cuts the y-axis at −1."),
],
("silver",3):[
  say("The line starts at (0, −3), so c = −3, and gradient 4 means \\(y = 4x - 3\\)."),
  box("The gradient step: 4 × 5 = ", 20, "Multiply gradient by x."),
  box("Add the start value: 20 + (−3) = ", 17, "Add the intercept, which is negative.", phase="substitute"),
  box("Check the start at x = 0: 4 × 0 − 3 = ", -3, "Put x = 0 in.", done="This matches the given point (0, −3), so y = 17 at x = 5."),
],
("silver",4):[
  say("k is the y-value at \\(x = 8\\) on \\(y = \\frac{1}{2}x + 3\\)."),
  box("Half of 8: ½ × 8 = ", 4, "Halve the x-value."),
  box("Add 3: 4 + 3 = ", 7, "Add the intercept.", phase="substitute"),
  box("Check at x = 0: ½ × 0 + 3 = ", 3, "Put x = 0 in.", done="The line starts at 3, and half of 8 adds 4, giving k = 7."),
],
("silver",5):[
  say("Gradient is rise ÷ run; mind the negative coordinate."),
  box("Change in y: 14 − 2 = ", 12, "Subtract the y-values."),
  box("Change in x: 3 − (−1) = ", 4, "Subtracting a negative adds."),
  box("Gradient = 12 ÷ 4 = ", 3, "Divide rise by run.", phase="substitute"),
  box("Check: 4 steps at 3 each, 4 × 3 = ", 12, "Multiply gradient by run.", done="This matches the rise of 12, gradient 3."),
],
("gold",0):[
  say("Gradient is rise ÷ run; both coordinates are negative here."),
  box("Change in y: 8 − (−7) = ", 15, "Subtracting a negative adds."),
  box("Change in x: 2 − (−3) = ", 5, "Subtracting a negative adds."),
  box("Gradient = 15 ÷ 5 = ", 3, "Divide rise by run.", phase="substitute"),
  box("Check: 5 steps at 3 each, 5 × 3 = ", 15, "Multiply gradient by run.", done="This matches the rise of 15, gradient 3."),
],
("gold",1):[
  say("Find the gradient, then use a point to find c."),
  box("Change in y: 17 − 5 = ", 12, "Subtract the y-values."),
  box("Change in x: 7 − 1 = ", 6, "Subtract the x-values."),
  box("Gradient m = 12 ÷ 6 = ", 2, "Divide rise by run."),
  box("Use (1, 5): 5 = 2 × 1 + c, so c = 5 − 2 = ", 3, "Subtract mx from y.", phase="substitute"),
  box("Check with (7, 17): 2 × 7 + 3 = ", 17, "Put x = 7 in.", done="This matches the second point, so c = 3."),
],
("gold",2):[
  say("Substitute the point (4, −2) into \\(y = mx + 6\\)."),
  box("Subtract 6 from both sides: −2 − 6 = ", -8, "Move the intercept across."),
  box("So 4m = −8. Divide by 4: −8 ÷ 4 = ", -2, "Divide to isolate m.", phase="substitute"),
  box("Check: −2 × 4 + 6 = ", -2, "Put m = −2 and x = 4 in.", done="This gives −2, matching the point (4, −2), so m = −2."),
],
("gold",3):[
  say("Gradient is rise ÷ run; watch the negative coordinate."),
  box("Change in y: −1 − 11 = ", -12, "Subtract the y-values."),
  box("Change in x: 2 − (−4) = ", 6, "Subtracting a negative adds."),
  box("Gradient = −12 ÷ 6 = ", -2, "Divide, keeping the minus.", phase="substitute"),
  box("Check: 6 steps at −2 each, 6 × (−2) = ", -12, "Multiply gradient by run.", done="This matches the change of −12, gradient −2."),
],
("gold",4):[
  say("Get it into the form \\(y = mx + c\\) by dividing every term by 3."),
  box("Divide the x-term: 9 ÷ 3 = ", 3, "Divide the coefficient of x."),
  box("Divide the constant: −12 ÷ 3 = ", -4, "Divide the constant term."),
  box("So y = 3x − 4. The gradient is ", 3, "Read the number multiplying x.", phase="substitute"),
  box("Check the intercept at x = 0: y = ", -4, "Put x = 0 in.", done="y = 3x − 4, so gradient 3 and intercept −4."),
]
}
for (t,i),steps in GS.items():
    pb[t][i]["guided_steps"] = steps
# silver[6] is multiple_choice: no guided_steps (validator allows omission)

# ---------- 5. tier_guides ----------
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: read m and c from y = mx + c",
   "steps": [
     "Every straight line can be written \\(y = mx + c\\). The number multiplying \\(x\\) is the <strong>gradient</strong> \\(m\\) (how steep). The number on its own is the <strong>y-intercept</strong> \\(c\\) (where it crosses the y-axis).",
     "To find \\(y\\) for a given \\(x\\), substitute: put the x-value in and work out \\(mx + c\\).",
     "The gradient between two points is <strong>rise ÷ run</strong>: the change in \\(y\\) divided by the change in \\(x\\)."
   ],
   "example": {
     "question": "The line y = 3x + 2. Find y when x = 2.",
     "steps": [
       {"label":"Read m and c","content":"<p>\\(m = 3\\) (gradient), \\(c = 2\\) (y-intercept).</p>"},
       {"label":"Substitute","content":"<p>\\(y = 3 \\times 2 + 2 = 6 + 2\\)</p>"},
       {"label":"Check","content":"<p>At \\(x = 0\\), \\(y = 2\\), matching the intercept.</p>"},
       {"label":"Answer","content":"<p>\\(y = 8\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "silver": {
   "title": "Silver: negatives and reading from a graph",
   "steps": [
     "A line sloping <strong>downhill</strong> from left to right has a <strong>negative</strong> gradient, because \\(y\\) falls as \\(x\\) grows.",
     "From a graph, read \\(c\\) where the line crosses the y-axis, and find \\(m\\) by counting the change in \\(y\\) for a step of 1 in \\(x\\).",
     "Keep the signs: \\((y_2 - y_1) \\div (x_2 - x_1)\\), subtracting in the same order top and bottom."
   ],
   "example": {
     "question": "Find the gradient through (1, 9) and (5, 1).",
     "steps": [
       {"label":"Rise","content":"<p>\\(1 - 9 = -8\\)</p>"},
       {"label":"Run","content":"<p>\\(5 - 1 = 4\\)</p>"},
       {"label":"Check","content":"<p>Downhill, so the gradient should be negative.</p>"},
       {"label":"Answer","content":"<p>Gradient \\(= -8 \\div 4 = -2\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "gold": {
   "title": "Gold: negative coordinates and rearranging",
   "steps": [
     "With negative coordinates, subtracting a negative adds. For \\((-3, -7)\\) and \\((2, 8)\\), the run is \\(2 - (-3) = 5\\).",
     "To get the gradient from an equation like \\(3y = 9x - 12\\), divide every term by 3 to reach \\(y = mx + c\\); then \\(m\\) is the number in front of \\(x\\).",
     "For the equation of a line, find \\(m\\) first, then put one point into \\(y = mx + c\\) to solve for \\(c\\)."
   ],
   "example": {
     "question": "A line has equation 3y = 9x - 12. Find the gradient.",
     "steps": [
       {"label":"Divide by 3","content":"<p>\\(y = 3x - 4\\)</p>"},
       {"label":"Read m","content":"<p>The number multiplying \\(x\\) is 3.</p>"},
       {"label":"Check","content":"<p>Intercept is \\(-4\\), giving \\(y = 3x - 4\\).</p>"},
       {"label":"Answer","content":"<p>Gradient \\(= 3\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 }
}

# ---------- 6. guided (opener + teach) ----------
pd["guided"] = {
 "opener": {
   "label": "Before any algebra",
   "display": "You start with £5 already in a jar.<br>Every week you add £2.",
   "steps": [
     {"say":"A savings jar. No algebra, just count.",
      "pre":"After 1 week the jar holds £", "post":"", "answer":7,
      "hint":"Start with £5, then add one lot of £2."},
     {"say":"Good. Now jump ahead.",
      "pre":"After 3 weeks the jar holds £", "post":"", "answer":11,
      "hint":"Start with £5, then add £2 three times: 5 + 2 + 2 + 2."},
     {"say":"You just used a straight-line rule. The £5 you started with is the <strong>y-intercept</strong> \\(c\\), where the line begins. The £2 you add each week is the <strong>gradient</strong> \\(m\\), how fast it climbs. Written out, that jar is \\(y = 2x + 5\\). Reading a linear graph is the same: find where it crosses the axis (\\(c\\)) and how steeply it climbs (\\(m\\))."}
   ]
 },
 "teach": {
   "bronze": {
     "display": "The line \\(y = 4x + 3\\).",
     "label": "Together: read it and use it",
     "steps": [
       {"say":"Compare with \\(y = mx + c\\).",
        "pre":"The gradient m = ", "post":"", "answer":4, "hint":"The number multiplying x."},
       {"pre":"The y-intercept c = ", "post":"", "answer":3, "hint":"The number on its own."},
       {"say":"Now find y at x = 2.",
        "pre":"4 × 2 = ", "post":"", "answer":8, "hint":"Multiply the gradient by x."},
       {"pre":"8 + 3 = ", "post":"", "answer":11, "done":"So y = 11 when x = 2.", "hint":"Add the intercept."},
       {"say":"Check the start.",
        "pre":"At x = 0: 4 × 0 + 3 = ", "post":"", "answer":3,
        "done":"This matches the intercept, so the reading is right.", "hint":"Put x = 0 in."}
     ]
   },
   "silver": {
     "display": "A line passes through \\((0, 6)\\) and \\((3, 0)\\).",
     "label": "Together: a downhill line",
     "steps": [
       {"say":"Gradient is rise ÷ run.",
        "pre":"Change in y: 0 − 6 = ", "post":"", "answer":-6, "hint":"y falls, so this is negative."},
       {"pre":"Change in x: 3 − 0 = ", "post":"", "answer":3, "hint":"Subtract the x-values."},
       {"pre":"Gradient = −6 ÷ 3 = ", "post":"", "answer":-2,
        "done":"Downhill, so negative. Good.", "hint":"Divide, keeping the minus."},
       {"say":"It crosses the y-axis at (0, 6).",
        "pre":"So the y-intercept c = ", "post":"", "answer":6, "hint":"Read the value at x = 0."},
       {"say":"Check the equation y = −2x + 6.",
        "pre":"At x = 3: −2 × 3 + 6 = ", "post":"", "answer":0,
        "done":"Gives 0, matching the point (3, 0).", "hint":"Put x = 3 in."}
     ]
   },
   "gold": {
     "display": "A line passes through \\((-2, -1)\\) and \\((2, 7)\\).",
     "label": "Together: build the equation",
     "steps": [
       {"say":"Gradient is rise ÷ run; watch the negatives.",
        "pre":"Rise: 7 − (−1) = ", "post":"", "answer":8, "hint":"Subtracting a negative adds."},
       {"pre":"Run: 2 − (−2) = ", "post":"", "answer":4, "hint":"Subtracting a negative adds."},
       {"pre":"Gradient = 8 ÷ 4 = ", "post":"", "answer":2, "hint":"Divide rise by run."},
       {"say":"Now find c using the point (2, 7): 7 = 2 × 2 + c.",
        "pre":"So c = 7 − 4 = ", "post":"", "answer":3, "hint":"Subtract mx from y."},
       {"say":"Check with (−2, −1).",
        "pre":"At x = −2: 2 × (−2) + 3 = ", "post":"", "answer":-1,
        "done":"Gives −1, matching (−2, −1). Equation y = 2x + 3.", "hint":"Put x = −2 in."}
     ]
   }
 }
}

# ---------- 7. method_card (slim) ----------
pd["method_card"] = {
 "title": "Reading and Plotting Linear Graphs",
 "steps": [
   "Write the line as y = mx + c: m is the gradient, c is the y-intercept.",
   "To find y from x, substitute x and work out mx + c.",
   "Gradient between two points is rise ÷ run: change in y ÷ change in x, keeping signs.",
   "From a graph: read c where the line crosses the y-axis; read m as the y-change for a step of 1 in x."
 ],
 "content": "<p>A straight line is <strong>y = mx + c</strong>. The gradient <strong>m</strong> shows how steep it is (negative means downhill); the intercept <strong>c</strong> is where it crosses the y-axis. Substitute an x-value to find y. Between two points, the gradient is the change in y divided by the change in x.</p>"
}

# ---------- 1b. Repair duplicate-answer defects (validator-flagged) ----------
# Minimal number edits so every single_value answer is unique within its tier.
# bronze dups: 2 (idx0,1,5), -2 (idx6,7) ; gold dups: 3 (idx0,1,4), -2 (idx2,3)

# bronze[1]: y=5x+6, intercept 6 (was y=5x+2 -> 2)
p = pb["bronze"][1]
p["display"] = "A line has equation \\(y = 5x + 6\\). What is the y-intercept?"
p["solutions"] = [6]
p["misconceptions"][0]["message"] = "In y = mx + c the y-intercept is c, the constant. Here c = 6, not the gradient 5."
p["misconceptions"][0]["expect"] = 5
p["guided_steps"] = [
  say("Compare with \\(y = mx + c\\). The y-intercept is \\(c\\), the number with no x."),
  box("The number multiplying x (gradient m) = ", 5, "Read the coefficient of x."),
  box("The number on its own (y-intercept c) = ", 6, "Read the constant term.", phase="substitute"),
  box("Check at x = 0: 5 × 0 + 6 = ", 6, "Put x = 0 into the equation.", done="At x = 0 the line is at y = 6, which is exactly the y-intercept."),
]

# bronze[5]: (0,7),(3,19) gradient 4 (was (0,7),(3,13) -> 2)
p = pb["bronze"][5]
p["display"] = "A line passes through \\((0, 7)\\) and \\((3, 19)\\). What is the gradient?"
p["solutions"] = [4]
p["misconceptions"][0]["message"] = "Rise = 19 − 7 = 12, run = 3 − 0 = 3. Gradient = 12 ÷ 3 = 4, not run over rise."
p["misconceptions"][0]["expect"] = 0.25
p["guided_steps"] = [
  say("Gradient is rise ÷ run."),
  box("Change in y: 19 − 7 = ", 12, "Subtract the y-values."),
  box("Change in x: 3 − 0 = ", 3, "Subtract the x-values."),
  box("Gradient = 12 ÷ 3 = ", 4, "Divide rise by run.", phase="substitute"),
  box("Check: y rises by 4 for each of the 3 steps, so 4 × 3 = ", 12, "Multiply gradient by run.", done="This matches the rise of 12, gradient 4 confirmed."),
]

# bronze[7]: graph gradient -3 (was -2); new chart y = 9 - 3x
p = pb["bronze"][7]
p["solutions"] = [-3]
p["chart"]["data"]["datasets"][0]["data"] = [{"x":0,"y":9},{"x":1,"y":6},{"x":2,"y":3},{"x":3,"y":0}]
p["chart"]["options"]["scales"]["y"]["max"] = 10
p["chart"]["options"]["scales"]["y"]["min"] = -1
p["chart"]["options"]["scales"]["x"]["max"] = 4
p["chart"]["options"]["scales"]["x"]["min"] = -1
p["misconceptions"][0]["message"] = "The line falls from left to right, so the gradient is negative: −3, not 3."
p["misconceptions"][0]["expect"] = 3
p["hint"] = "The line falls, so the gradient is negative: count the drop in y for a step of 1 in x."
p["guided_steps"] = [
  say("Pick two clear points on the line and use rise ÷ run."),
  box("From x = 0 to x = 1, y changes from 9 to 6, a change of ", -3, "It falls, so the change is negative."),
  box("The matching change in x is ", 1, "One step across."),
  box("Gradient = −3 ÷ 1 = ", -3, "Divide the fall by the run.", phase="substitute"),
  box("Check over a bigger gap: from (0, 9) to (3, 0), −9 ÷ 3 = ", -3, "Total fall over total run.", done="Same gradient, −3, the line goes downhill."),
]

# gold[1]: (2,7),(5,19) find c = -1 (was (1,5),(7,17) -> c=3)
p = pb["gold"][1]
p["display"] = "A line passes through \\((2, 7)\\) and \\((5, 19)\\). Write the equation in the form \\(y = mx + c\\). What is the value of \\(c\\)?"
p["solutions"] = [-1]
p["misconceptions"][0]["message"] = "c is not just the y-value. Substitute a point: 7 = 4(2) + c gives c = −1."
p["misconceptions"][0]["expect"] = 7
p["guided_steps"] = [
  say("Find the gradient, then use a point to find c."),
  box("Change in y: 19 − 7 = ", 12, "Subtract the y-values."),
  box("Change in x: 5 − 2 = ", 3, "Subtract the x-values."),
  box("Gradient m = 12 ÷ 3 = ", 4, "Divide rise by run."),
  box("Use (2, 7): 7 = 4 × 2 + c, so c = 7 − 8 = ", -1, "Subtract mx from y.", phase="substitute"),
  box("Check with (5, 19): 4 × 5 + (−1) = ", 19, "Put x = 5 in.", done="This matches the second point, so c = −1."),
]

# gold[3]: (-4,13),(2,-5) gradient -3 (was (-4,11),(2,-1) -> -2)
p = pb["gold"][3]
p["display"] = "Two points on a line are \\((-4, 13)\\) and \\((2, -5)\\). What is the gradient?"
p["solutions"] = [-3]
p["misconceptions"][0]["message"] = "2 − (−4) = 6, not −2. The gradient is −18 ÷ 6 = −3."
p["misconceptions"][0]["expect"] = 9
p["hint"] = "Change in y is −5 − 13 = −18; change in x is 2 − (−4) = 6."
p["guided_steps"] = [
  say("Gradient is rise ÷ run; watch the negative coordinate."),
  box("Change in y: −5 − 13 = ", -18, "Subtract the y-values."),
  box("Change in x: 2 − (−4) = ", 6, "Subtracting a negative adds."),
  box("Gradient = −18 ÷ 6 = ", -3, "Divide, keeping the minus.", phase="substitute"),
  box("Check: 6 steps at −3 each, 6 × (−3) = ", -18, "Multiply gradient by run.", done="This matches the change of −18, gradient −3."),
]

# gold[4]: 2y = 10x - 6 -> y=5x-3, gradient 5 (was 3y=9x-12 -> 3)
p = pb["gold"][4]
p["display"] = "A line has equation \\(2y = 10x - 6\\). What is the gradient?"
p["solutions"] = [5]
p["misconceptions"][0]["message"] = "Divide the whole equation by 2 first: y = 5x − 3. The gradient is 5, not 10."
p["misconceptions"][0]["expect"] = 10
p["hint"] = "Divide every term by 2 to reach y = mx + c, then read the gradient."
p["guided_steps"] = [
  say("Get it into the form \\(y = mx + c\\) by dividing every term by 2."),
  box("Divide the x-term: 10 ÷ 2 = ", 5, "Divide the coefficient of x."),
  box("Divide the constant: −6 ÷ 2 = ", -3, "Divide the constant term."),
  box("So y = 5x − 3. The gradient is ", 5, "Read the number multiplying x.", phase="substitute"),
  box("Check the intercept at x = 0: y = ", -3, "Put x = 0 in.", done="y = 5x − 3, so gradient 5 and intercept −3."),
]

# ---------- write ----------
io.open(OUT,"w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=1))
# sanity: em dash count
whole = json.dumps(pd, ensure_ascii=False)
print("em dashes remaining:", whole.count("—"))
print("wrote", OUT)
