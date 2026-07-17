# -*- coding: utf-8 -*-
import json

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_gL07_live.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_graphs-L07.json"

live = json.load(open(LIVE, encoding="utf-8"))["practice_data"]

# --- preserved fields (byte-for-byte from live) ---
worked_examples = live["worked_examples"]
topic_links     = live["topic_links"]
related_videos  = live["related_videos"]

# minimal style fix: strip em dashes from preserved worked_examples labels
# (validator enforces no em dashes; replace " — " with ": " as the sibling does)
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# --- reusable charts ---
PARABOLA_PTS = [{"x":-3,"y":9},{"x":-2,"y":4},{"x":-1,"y":1},{"x":0,"y":0},
                {"x":1,"y":1},{"x":2,"y":4},{"x":3,"y":9}]
def parabola_chart():
    return {
      "type":"scatter",
      "data":{"datasets":[
        {"type":"line","data":[dict(p) for p in PARABOLA_PTS],"tension":0.4,"fill":False,
         "borderColor":"#3b82f6","pointRadius":3,"pointBackgroundColor":"#3b82f6"},
        {"type":"scatter","data":[{"x":0,"y":0}],"pointRadius":5,
         "pointBackgroundColor":"#f59e0b","borderColor":"#f59e0b"}
      ]},
      "options":{"plugins":{"legend":{"display":False}},"scales":{
        "x":{"min":-4,"max":4,"ticks":{"stepSize":1},"grid":{"color":"rgba(128,128,128,0.15)"},"title":{"text":"x","display":True}},
        "y":{"min":-1,"max":10,"ticks":{"stepSize":2},"grid":{"color":"rgba(128,128,128,0.15)"},"title":{"text":"y","display":True}}
      }}
    }

import math
def sin_chart():
    pts=[{"x":d,"y":round(math.sin(math.radians(d)),3)} for d in range(0,361,15)]
    return {
      "type":"scatter",
      "data":{"datasets":[
        {"type":"line","data":pts,"tension":0.4,"fill":False,"borderColor":"#3b82f6",
         "pointRadius":0,"borderWidth":2.4}
      ]},
      "options":{"plugins":{"legend":{"display":False}},"scales":{
        "x":{"min":0,"max":360,"ticks":{"stepSize":90},"grid":{"color":"rgba(128,128,128,0.15)"},"title":{"text":"x (degrees)","display":True}},
        "y":{"min":-1.2,"max":1.2,"ticks":{"stepSize":0.5},"grid":{"color":"rgba(128,128,128,0.15)"},"title":{"text":"y","display":True}}
      }}
    }

def box(pre, answer, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d
def say(s): return {"say": s}

# ================= BRONZE =================
bronze = [
 { "hint":"f(x) + 3 adds 3 to the y-coordinate only.",
   "display":"The point \\((2, 7)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = f(x) + 3\\).",
   "solutions":[10],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The +3 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 2."),
     box("The graph moves UP. How many units up? ",3,"The number outside the bracket, +3."),
     say("Add that to the y-coordinate."),
     box("New y = 7 + 3 = ",10,"Add the 3 onto 7.",phase="substitute"),
     box("Check how far y rose: 10 − 7 = ",3,"New y minus old y.",phase="substitute",
         done="Up 3, exactly what f(x) + 3 does, so the image y is 10.")],
   "misconceptions":[{"note":"expect 5 = used x (2+3)","check":"wrong_formula","expect":5,"pattern":"wrong_formula",
     "message":"You may have used the x-coordinate (2) instead of the y-coordinate (7). f(x) + 3 only changes y: new y = 7 + 3 = 10, not 2 + 3 = 5."}]},

 { "hint":"f(x) − 3 lowers the y-coordinate by 3.",
   "display":"The point \\((4, 1)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = f(x) - 3\\).",
   "solutions":[-2],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The −3 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 4."),
     box("The graph moves DOWN. By how many units? ",3,"The size of the number outside, 3."),
     say("Take that off the y-coordinate."),
     box("New y = 1 − 3 = ",-2,"1 take away 3 goes below zero.",phase="substitute"),
     box("Check the drop: 1 − (−2) = ",3,"Old y minus new y.",phase="substitute",
         done="Down 3, exactly f(x) − 3. The image y is −2.")],
   "misconceptions":[{"note":"expect 4 = 1+3, wrong direction","check":"confusion","expect":4,"pattern":"confusion",
     "message":"f(x) − 3 moves the graph DOWN, so subtract: 1 − 3 = −2. Adding the 3 instead gives 4, which is the wrong direction."}]},

 { "hint":"The +5 is outside the bracket, so it changes y, not x.",
   "display":"\\(y = f(x) + 5\\) is a translation. Which direction does the graph move?",
   "options":["Up","Down","Left","Right"],"solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[{"note":"expect 3 = Right, inside/outside confusion","check":"confusion","expect":3,"pattern":"confusion",
     "message":"The +5 is OUTSIDE the bracket, so it changes y and moves the graph UP, not sideways. Only changes inside the bracket move it left or right."}]},

 { "hint":"Inside the bracket does the opposite of the sign shown.",
   "display":"\\(y = f(x + 2)\\) is a translation. Which direction does the graph move?",
   "options":["Up","Down","Left","Right"],"solutions":[2],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[{"note":"expect 3 = Right, forgot inside opposite","check":"confusion","expect":3,"pattern":"confusion",
     "message":"f(x + 2) has +2 inside the bracket, and inside does the opposite: the graph moves LEFT by 2, not right."}]},

 { "hint":"f(x + 4) moves the point left 4, so subtract from x.",
   "display":"The point \\((5, 2)\\) lies on \\(y = f(x)\\). Find the \\(x\\)-coordinate of its image on \\(y = f(x + 4)\\).",
   "solutions":[1],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The +4 is INSIDE the bracket, so it changes the x-coordinate, and inside does the OPPOSITE: it moves LEFT. y stays at 2."),
     box("Moving left means we subtract. By how many? ",4,"The number inside the bracket, 4."),
     say("Take that off the x-coordinate."),
     box("New x = 5 − 4 = ",1,"5 take away 4.",phase="substitute"),
     box("Check: y is untouched, so how far did y move? ",0,"Inside the bracket never changes y.",phase="substitute",
         done="x moved left 4, y stayed put. The image x is 1.")],
   "misconceptions":[{"note":"expect 9 = 5+4 right shift","check":"confusion","expect":9,"pattern":"confusion",
     "message":"f(x + 4) moves the point LEFT by 4, so subtract: 5 − 4 = 1. Adding to get 9 is the right-shift error."}]},

 { "hint":"A negative outside the bracket flips y, reflecting in the x-axis.",
   "display":"\\(y = -f(x)\\) is a reflection. In which axis?",
   "options":["x-axis","y-axis","line y = x","line y = −x"],"solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[{"note":"expect 1 = y-axis, swapped","check":"confusion","expect":1,"pattern":"confusion",
     "message":"−f(x) has the minus OUTSIDE the bracket, so it reflects in the x-axis. f(−x), with the minus inside, is the one that reflects in the y-axis."}]},

 { "hint":"A negative inside the bracket flips x, reflecting in the y-axis.",
   "display":"\\(y = f(-x)\\) is a reflection. In which axis?",
   "options":["x-axis","y-axis","line y = x","line y = −x"],"solutions":[1],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[{"note":"expect 0 = x-axis, swapped","check":"confusion","expect":0,"pattern":"confusion",
     "message":"f(−x) has the minus INSIDE the bracket, affecting x, so it reflects in the y-axis. The x-axis reflection is −f(x)."}]},

 { "hint":"−f(x) flips the sign of the y-coordinate.",
   "display":"The point \\((3, 6)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = -f(x)\\).",
   "solutions":[-6],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The minus is OUTSIDE the bracket, so −f(x) reflects the graph in the x-axis: every y-value flips sign. x stays at 3."),
     box("Before flipping, the y-coordinate is ",6,"Read it straight from the point (3, 6)."),
     say("Reflecting multiplies that by −1."),
     box("New y = 6 × (−1) = ",-6,"Just change the sign.",phase="substitute"),
     box("Check the two heights cancel: 6 + (−6) = ",0,"A number plus its negative.",phase="substitute",
         done="Equal and opposite about the x-axis, so the image y is −6.")],
   "misconceptions":[{"note":"expect 6 = no sign change","check":"sign_error","expect":6,"pattern":"sign_error",
     "message":"−f(x) reflects in the x-axis, so the y-coordinate changes sign: 6 becomes −6. Leaving it as 6 misses the reflection."}]},
]

# ================= SILVER =================
silver = [
 { "hint":"f(−x) flips the sign of the x-coordinate.",
   "display":"The point \\((-2, 5)\\) lies on \\(y = f(x)\\). Find the \\(x\\)-coordinate of its image on \\(y = f(-x)\\).",
   "solutions":[2],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The minus is INSIDE the bracket, so f(−x) reflects the graph in the y-axis: every x-value flips sign. y stays at 5."),
     box("The x-coordinate before flipping is ",-2,"Read it from (−2, 5)."),
     say("Reflecting multiplies that by −1."),
     box("New x = (−2) × (−1) = ",2,"Two negatives make a positive.",phase="substitute"),
     box("Check the two x-values cancel: (−2) + 2 = ",0,"A number plus its negative.",phase="substitute",
         done="Equal and opposite about the y-axis, so the image x is 2.")],
   "misconceptions":[{"note":"expect -2 = no sign change","check":"confusion","expect":-2,"pattern":"confusion",
     "message":"f(−x) reflects in the y-axis, so x changes sign: −2 becomes +2. Leaving it as −2 misses the reflection."}]},

 { "hint":"f(x) − 4 lowers the maximum's y by 4.",
   "display":"The maximum point of \\(y = f(x)\\) is \\((4, 7)\\). Find the \\(y\\)-coordinate of the maximum of \\(y = f(x) - 4\\).",
   "solutions":[3],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The maximum moves with the curve. The −4 is OUTSIDE, so it lowers the y-coordinate; x stays at 4."),
     box("The graph moves DOWN by how many? ",4,"The number outside the bracket, 4."),
     say("Take that off the maximum's y-coordinate."),
     box("New y = 7 − 4 = ",3,"7 take away 4.",phase="substitute"),
     box("Check the drop: 7 − 3 = ",4,"Old y minus new y.",phase="substitute",
         done="Down 4, so the new maximum y is 3.")],
   "misconceptions":[{"note":"expect 7 = no shift","check":"wrong_formula","expect":7,"pattern":"wrong_formula",
     "message":"f(x) − 4 lowers the maximum by 4: 7 − 4 = 3. Leaving y at 7 forgets the downward shift."}]},

 { "hint":"f(x − 5) moves the minimum right 5, so add to x.",
   "display":"The minimum point of \\(y = f(x)\\) is \\((3, -2)\\). Find the \\(x\\)-coordinate of the minimum of \\(y = f(x - 5)\\).",
   "solutions":[8],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("The minimum moves with the curve. The −5 is INSIDE, and inside does the OPPOSITE, so the graph moves RIGHT; y stays at −2."),
     box("Moving right means we add. Add how many? ",5,"The number inside the bracket, 5."),
     say("Add that to the x-coordinate."),
     box("New x = 3 + 5 = ",8,"3 add 5.",phase="substitute"),
     box("Check how far right it moved: 8 − 3 = ",5,"New x minus old x.",phase="substitute",
         done="Right 5, so the new minimum x is 8.")],
   "misconceptions":[{"note":"expect -2 = 3-5 left shift","check":"confusion","expect":-2,"pattern":"confusion",
     "message":"f(x − 5) moves RIGHT by 5 (inside does the opposite), so add: 3 + 5 = 8. Subtracting to get −2 is the left-shift error."}]},

 { "hint":"The number added outside is the y-shift; inside gives the x-shift in the opposite direction.",
   "display":"The curve \\(y = x^2\\) is transformed to \\(y = (x + 2)^2 + 1\\) by a translation. Give the \\(x\\)-component of the translation vector.",
   "solutions":[-2],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("A translation vector is written as (x-shift, y-shift). Find each part from the equation."),
     box("The +1 outside the bracket shifts the curve up. That is the y-component: ",1,"The number added outside, +1."),
     say("Now the horizontal part, from inside the bracket."),
     box("Inside is (x + 2). Inside does the opposite, so the curve moves LEFT, giving x-component ",-2,"Left counts as negative: −2.",phase="substitute"),
     box("Check: a point at x = 0 on y = x² lands at x = ",-2,"0 shifted left by 2.",phase="substitute",
         done="Moved left 2, so the x-component is −2. Vector (−2, 1).")],
   "misconceptions":[{"note":"expect 2 = read +2 as right","check":"confusion","expect":2,"pattern":"confusion",
     "message":"(x + 2) has +2 inside the bracket, which means move LEFT by 2 (inside does the opposite). The x-component is −2, not +2."}],
   "chart": parabola_chart()},

 { "hint":"The −2 outside lowers the y-coordinate by 2.",
   "display":"The graph \\(y = f(x)\\) passes through \\((0, 6)\\). What point does \\(y = f(x + 2) - 2\\) pass through? Give the \\(y\\)-coordinate.",
   "solutions":[4],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("Two moves. The +2 inside changes x; the −2 outside changes y. We want the y-coordinate, which the outside part controls."),
     box("The x-part first: +2 inside moves LEFT, so new x = 0 − 2 = ",-2,"Inside does the opposite: subtract 2."),
     say("Now the y-coordinate, from the −2 outside."),
     box("New y = 6 − 2 = ",4,"Take 2 off the 6.",phase="substitute"),
     box("Check the drop in y: 6 − 4 = ",2,"Old y minus new y.",phase="substitute",
         done="Down 2, so the point is (−2, 4) and the y-coordinate is 4.")],
   "misconceptions":[{"note":"expect 6 = no vertical shift","check":"wrong_formula","expect":6,"pattern":"wrong_formula",
     "message":"The −2 outside lowers y by 2: 6 − 2 = 4. Leaving y at 6 misses the vertical shift."}]},

 { "hint":"Reflecting in the y-axis changes the sign of x.",
   "display":"The point \\((5, -3)\\) lies on \\(y = f(x)\\). It is reflected in the \\(y\\)-axis to give \\(y = f(-x)\\). Find the new \\(x\\)-coordinate.",
   "solutions":[-5],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("Reflecting in the y-axis flips the sign of every x-coordinate. y stays at −3."),
     box("The x-coordinate before reflecting is ",5,"Read it from (5, −3)."),
     say("Multiply that by −1."),
     box("New x = 5 × (−1) = ",-5,"Change the sign.",phase="substitute"),
     box("Check the two x-values cancel: 5 + (−5) = ",0,"A number plus its negative.",phase="substitute",
         done="Equal and opposite about the y-axis, so the new x is −5.")],
   "misconceptions":[{"note":"expect 5 = no sign change","check":"sign_error","expect":5,"pattern":"sign_error",
     "message":"Reflecting in the y-axis changes the sign of x: 5 becomes −5. Leaving it as 5 misses the reflection."}]},

 { "hint":"−f(x) changes the sign of y.",
   "display":"The point \\((-4, 7)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = -f(x)\\).",
   "solutions":[-7],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("−f(x) reflects in the x-axis, flipping the sign of every y-coordinate. x stays at −4."),
     box("The y-coordinate before reflecting is ",7,"Read it from (−4, 7)."),
     say("Multiply that by −1."),
     box("New y = 7 × (−1) = ",-7,"Change the sign.",phase="substitute"),
     box("Check the two y-values cancel: 7 + (−7) = ",0,"A number plus its negative.",phase="substitute",
         done="Equal and opposite about the x-axis, so the new y is −7.")],
   "misconceptions":[{"note":"expect 7 = no sign change","check":"sign_error","expect":7,"pattern":"sign_error",
     "message":"−f(x) reflects in the x-axis, so y changes sign: 7 becomes −7. Leaving it as 7 misses the reflection."}]},
]

# ================= GOLD =================
gold = [
 { "hint":"The vertex of y = x² is (0, 0); apply the shifts to it.",
   "display":"The curve \\(y = x^2\\) is transformed to \\(y = (x + 1)^2 - 4\\). State the coordinates of the vertex of the new curve. Give the \\(y\\)-coordinate.",
   "solutions":[-4],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("Start from the vertex of y = x², which sits at (0, 0). Apply the two moves to it."),
     box("Inside is (x + 1). Inside does the opposite, so the vertex moves LEFT by 1: new x = 0 − 1 = ",-1,"0 minus 1."),
     say("Now the vertical move, from the −4 outside. We want this y-coordinate."),
     box("New y = 0 − 4 = ",-4,"The vertex y drops by 4.",phase="substitute"),
     box("Check the drop: 0 − (−4) = ",4,"Old y minus new y.",phase="substitute",
         done="Down 4 from the origin, so the vertex is (−1, −4) and its y-coordinate is −4.")],
   "misconceptions":[{"note":"expect 0 = vertical shift ignored","check":"confusion","expect":0,"pattern":"confusion",
     "message":"You may have found only the horizontal shift. The vertex of y = x² starts at (0, 0); (x + 1)² moves it left to (−1, 0), and the −4 then drops it to (−1, −4). The y-coordinate is −4, not 0."}],
   "chart": parabola_chart()},

 { "hint":"Reflection in the x-axis multiplies the whole function by −1.",
   "display":"The graph of \\(y = \\sin x\\) is reflected in the \\(x\\)-axis. Write the equation of the new graph. Which of these is correct?",
   "options":["y = sin(−x)","y = −sin x","y = sin x + 1","y = cos x"],"solutions":[1],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[{"note":"expect 0 = y = sin(-x), y-axis reflection","check":"confusion","expect":0,"pattern":"confusion",
     "message":"Reflection in the x-axis multiplies the output by −1, giving y = −sin x. y = sin(−x) is a reflection in the y-axis instead."}],
   "chart": sin_chart()},

 { "hint":"Reflect the y-value first, then add 4.",
   "display":"Two transformations are applied: first \\(y = f(x)\\) becomes \\(y = -f(x)\\), then that becomes \\(y = -f(x) + 4\\). The point \\((3, 6)\\) is on the original. Find the final \\(y\\)-coordinate.",
   "solutions":[-2],"calculator":False,"input_type":"single_value",
   "guided_steps":[
     say("Two steps on the y-coordinate. First reflect, then add 4. x stays at 3."),
     box("Reflect: −f(x) flips the sign of y, so 6 becomes ",-6,"Change the sign of 6."),
     say("Now the +4 lifts that reflected y."),
     box("New y = (−6) + 4 = ",-2,"Start at −6 and add 4.",phase="substitute"),
     box("Check the lift: (−2) − (−6) = ",4,"New y minus reflected y.",phase="substitute",
         done="Up 4 from the reflection, so the final y is −2.")],
   "misconceptions":[{"note":"expect -6 = stopped after reflection","check":"wrong_formula","expect":-6,"pattern":"wrong_formula",
     "message":"You may have stopped after the reflection. −f(x) gives y = −6, but the +4 then lifts it: −6 + 4 = −2."}]},

 { "hint":"Flipping BOTH coordinates needs BOTH reflections, one for x and one for y.",
   "display":"The point \\((a, b)\\) on \\(y = f(x)\\) maps to \\((-a, -b)\\). Which two transformations produce this?",
   "options":["−f(x) then f(−x)","−f(x) only","f(−x) only","f(x) + b then f(x + a)"],"solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[
     {"note":"expect 1 = -f(x) only","check":"confusion","expect":1,"pattern":"confusion",
      "message":"−f(x) on its own only flips y, giving (a, −b). To flip x as well you also need f(−x). Both reflections together give (−a, −b)."},
     {"note":"expect 2 = f(-x) only","check":"confusion","expect":2,"pattern":"confusion",
      "message":"f(−x) on its own only flips x, giving (−a, b). You also need −f(x) to flip y. Both reflections together give (−a, −b)."}]},

 { "hint":"Move the root (6, 0) left 2, then up 3.",
   "display":"The curve \\(y = f(x)\\) has a root at \\(x = 6\\). After the transformation \\(y = f(x + 2) + 3\\), does the curve still pass through the \\(x\\)-axis at \\(x = 4\\)?",
   "options":["Yes, it still crosses the x-axis at x = 4",
              "No, the point that was the root is now at (4, 3)",
              "No, the point that was the root is now at (6, 3)",
              "No, the point that was the root is now at (8, 3)"],
   "solutions":[1],"calculator":False,"input_type":"multiple_choice",
   "misconceptions":[
     {"note":"expect 0 = vertical shift forgotten","check":"confusion","expect":0,"pattern":"confusion",
      "message":"The +3 outside lifts every point up by 3, so the old root at (4, 0) rises to (4, 3). It no longer touches the x-axis, so the answer is not Yes."},
     {"note":"expect 3 = shifted right instead of left","check":"confusion","expect":3,"pattern":"confusion",
      "message":"f(x + 2) has +2 inside the bracket, so the graph moves LEFT by 2: the root's x goes 6 to 4, not 8. Adding the +3 lands it at (4, 3)."},
     {"note":"expect 2 = horizontal shift forgotten","check":"confusion","expect":2,"pattern":"confusion",
      "message":"The +2 inside the bracket moves the root LEFT, from x = 6 to x = 4. With the +3 up, the point is at (4, 3), not (6, 3)."}]},
]

# ================= problem_bank =================
problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description":"One transformation applied to one point: a single shift or a single reflection, written in function notation.",
  "silver_description":"Combined shifts, or a transformation of a named point such as a maximum, minimum or vertex.",
  "gold_description":"Reflections stacked with shifts, translation vectors, and the effect of a shift on a root.",
}

# ================= guided (opener + teach) =================
opener_svg = ('<svg viewBox="0 0 200 180" role="img" aria-label="A gull 4 metres above a horizontal lake surface, '
 'and its mirror reflection the same distance below the surface, marked with a question mark." '
 'style="max-width:280px;width:100%;font-family:Inter,sans-serif">'
 '<rect x="20" y="90" width="160" height="70" fill="#60a5fa" fill-opacity="0.18"/>'
 '<line x1="20" y1="90" x2="180" y2="90" stroke="currentColor" stroke-width="1.4"/>'
 '<text x="176" y="86" font-size="10" fill="currentColor" text-anchor="end">lake</text>'
 '<line x1="100" y1="40" x2="100" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.6"/>'
 '<circle cx="100" cy="40" r="5" fill="#f59e0b"/>'
 '<text x="110" y="43" font-size="10" fill="currentColor">gull</text>'
 '<text x="70" y="68" font-size="10" fill="currentColor" text-anchor="end">4 m</text>'
 '<circle cx="100" cy="140" r="5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 2"/>'
 '<text x="110" y="143" font-size="11" fill="currentColor">?</text>'
 '<text x="70" y="118" font-size="10" fill="currentColor" text-anchor="end">4 m</text>'
 '</svg><div style="margin-top:6px">Reflection in the lake surface</div>')

guided = {
 "opener": {
   "display": opener_svg,
   "steps": [
     say("No algebra, just picture it. A graph is a shape you can slide up or flip over, exactly like a real object."),
     box("A hillwalk records the path's height at each kilometre. A new survey finds every height is 2 m higher than the log. At the 4 km mark the log said 30 m, so the corrected height is ",
         32,"Add the extra 2 metres on: 30 + 2.",post=" m"),
     say("Adding 2 to every reading slides the whole graph <strong>up</strong> by 2. In function notation that is \\(f(x) + 2\\): the +2 sits OUTSIDE the bracket, so it changes the y-values."),
     box("A gull flies 4 m above a calm lake. Its reflection sits the same distance below the surface. Measured as a height above the water, the reflection is at ",
         -4,"Below the surface counts as a negative height.",post=" m"),
     say("Flipping every height to the opposite side of the water is a <strong>reflection in the x-axis</strong>. That is \\(-f(x)\\): every y-value is multiplied by −1. Sliding changes the numbers you add; reflecting changes their sign. That is the whole topic."),
   ]
 },
 "teach": {
   "bronze": {
     "display":"Solve: the point (3, 4) lies on \\(y = f(x)\\). Find its image on \\(y = f(x) + 5\\).",
     "steps":[
       say("The +5 is OUTSIDE the bracket, so it changes only the y-coordinate. The x-coordinate does not move."),
       box("The x-coordinate stays the same: x = ",3,"Outside the bracket leaves x alone."),
       box("Add 5 to the y-coordinate: 4 + 5 = ",9,"Just add the 5 on."),
       say("So the image is (3, 9)."),
       box("Check how far y rose: 9 − 4 = ",5,"New y minus old y."),
       box("And how far did x move? ",0,"x was 3 and stayed 3.",done="Zero. Outside the bracket never moves x. Gone."),
     ]},
   "silver": {
     "display":"Solve: the point (1, 5) lies on \\(y = f(x)\\). Find its image on \\(y = f(x - 2) - 3\\).",
     "steps":[
       say("Two moves at once. Split them: the −2 inside the bracket moves x, the −3 outside moves y."),
       box("Inside the bracket, −2 moves the graph RIGHT by 2, so x: 1 + 2 = ",3,"Inside does the opposite, so subtracting 2 moves right, which adds."),
       box("Outside the bracket, −3 moves it DOWN by 3, so y: 5 − 3 = ",2,"Subtract the 3 from 5."),
       say("So the image is (3, 2)."),
       box("Check how far right x moved: 3 − 1 = ",2,"New x minus old x."),
       box("Check how far y moved: 2 − 5 = ",-3,"Down counts as negative.",done="Right 2, down 3, exactly f(x − 2) − 3. Gone."),
     ]},
   "gold": {
     "display":"Solve: the point (4, 1) lies on \\(y = f(x)\\). Find its image on \\(y = -f(x) + 2\\).",
     "steps":[
       say("A reflection and a shift together. Do the reflection first, then the translation."),
       box("Reflect: −f(x) multiplies y by −1, so 1 becomes ",-1,"Flip the sign of the y-coordinate."),
       box("The x-coordinate is untouched by both moves, so x = ",4,"Nothing here changes x."),
       box("Now translate: +2 adds 2 to y, so −1 + 2 = ",1,"Add 2 to the reflected y."),
       say("So the image is (4, 1)."),
       box("Check the lift from the reflection: 1 − (−1) = ",2,"New y minus reflected y.",done="Up 2 from the reflected point (4, −1), landing at (4, 1). Gone."),
     ]},
 }
}

# ================= tier_guides =================
tier_guides = {
 "bronze": {
   "title":"Bronze: one transformation, one point",
   "steps":[
     "Outside the bracket changes y: <strong>f(x) + a</strong> adds a to the y-coordinate, <strong>−f(x)</strong> flips the sign of y.",
     "Inside the bracket changes x and does the opposite: <strong>f(x + a)</strong> moves left (subtract from x), <strong>f(−x)</strong> flips the sign of x.",
     "Leave the coordinate that is not affected exactly as it was."],
   "example":{
     "question":"The point (4, 7) lies on y = f(x). Find its image on y = f(x) + 3.",
     "steps":[
       {"label":"Outside the bracket","content":"<p>\\(+3\\) is outside, so it changes the \\(y\\)-coordinate only.</p>"},
       {"label":"Add 3 to y","content":"<p>\\(7 + 3 = 10\\); the \\(x\\)-coordinate stays at 4.</p>"},
       {"label":"Check","content":"<p>Only \\(y\\) moved, and by \\(+3\\), exactly what \\(f(x) + 3\\) should do.</p>"},
       {"label":"Answer","content":"<p>New position: <strong>(4, 10)</strong></p>","isAnswer":True,"is_answer":True}]}},
 "silver": {
   "title":"Silver: combined shifts and named points",
   "steps":[
     "A curve can be shifted horizontally and vertically at once, for example <strong>f(x − 3) + 1</strong>.",
     "Split it: the inside part moves x in the opposite direction, the outside part moves y as written.",
     "A vertex, maximum or minimum moves with the curve, so transform its coordinates the same way."],
   "example":{
     "question":"The minimum of y = f(x) is (2, −3). Find the minimum of y = f(x − 1) + 4.",
     "steps":[
       {"label":"Inside the bracket","content":"<p>\\(-1\\) inside means move RIGHT by 1: \\(x\\) goes \\(2 \\to 3\\).</p>"},
       {"label":"Outside the bracket","content":"<p>\\(+4\\) means move UP by 4: \\(y\\) goes \\(-3 \\to 1\\).</p>"},
       {"label":"Check","content":"<p>Right 1 and up 4 matches \\(f(x - 1) + 4\\).</p>"},
       {"label":"Answer","content":"<p>New minimum: <strong>(3, 1)</strong></p>","isAnswer":True,"is_answer":True}]}},
 "gold": {
   "title":"Gold: reflections combined with shifts",
   "steps":[
     "Reflections and translations can stack, for example <strong>−f(x) + 3</strong> or <strong>f(x + 2) + 3</strong>.",
     "Do them in order: reflect first (flip the sign), then translate (add the shift).",
     "A root sits on the x-axis, so watch its y-value: any vertical shift lifts it off the axis."],
   "example":{
     "question":"The point (2, 5) lies on y = f(x). Find its image on y = −f(x) + 1.",
     "steps":[
       {"label":"Reflect","content":"<p>\\(-f(x)\\) flips \\(y\\): \\(5 \\to -5\\); \\(x\\) stays 2.</p>"},
       {"label":"Translate","content":"<p>\\(+1\\) lifts \\(y\\) by 1: \\(-5 \\to -4\\).</p>"},
       {"label":"Check","content":"<p>Reflect then add 1 gives \\((2, -4)\\).</p>"},
       {"label":"Answer","content":"<p>New position: <strong>(2, −4)</strong></p>","isAnswer":True,"is_answer":True}]}},
}

# ================= method_card =================
method_card = {
  "title":"Transforming Graphs with Function Notation",
  "steps":[
    "Outside the bracket changes y and does what it says: f(x) + a moves UP, −f(x) reflects in the x-axis.",
    "Inside the bracket changes x and does the OPPOSITE: f(x + a) moves LEFT, f(−x) reflects in the y-axis.",
    "Apply the rule to each key point, shifting or flipping its coordinates.",
    "Check a known point lands sensibly before sketching the new curve."],
  "content":"<p>Graph transformations use <strong>function notation</strong> \\(f(x)\\). Four moves matter. <strong>\\(f(x) + a\\)</strong> shifts up by \\(a\\). <strong>\\(f(x + a)\\)</strong> shifts left by \\(a\\), because inside the bracket does the opposite. <strong>\\(-f(x)\\)</strong> reflects in the \\(x\\)-axis. <strong>\\(f(-x)\\)</strong> reflects in the \\(y\\)-axis. In short: outside the bracket affects \\(y\\) and behaves as expected, while inside affects \\(x\\) and does the opposite.</p>",
  "example":"<p><strong>The point (3, 5) lies on \\(y = f(x)\\). Find its image on \\(y = f(x + 2)\\).</strong></p><p>The \\(+2\\) is inside the bracket, so it moves the point LEFT by 2: \\(x = 3 - 2 = 1\\). The \\(y\\)-coordinate is unchanged, so the image is \\((1, 5)\\).</p>",
}

pd = {
  "guided": guided,
  "method_card": method_card,
  "tier_guides": tier_guides,
  "topic_links": topic_links,
  "problem_bank": problem_bank,
  "related_videos": related_videos,
  "worked_examples": worked_examples,
}

json.dump(pd, open(OUT,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
# quick word counts
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
print("method_card.content words:", words(method_card["content"]))
for t in ["bronze","silver","gold"]:
    print(t,"tier_guide steps words:", sum(words(s) for s in tier_guides[t]["steps"]))
print("method_card steps:", len(method_card["steps"]))
