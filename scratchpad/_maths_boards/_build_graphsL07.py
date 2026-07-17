# -*- coding: utf-8 -*-
"""Build guided + diagrams practice_data for maths-aqa graphs-L07 Graph Transformations."""
import json, io, math

MINUS = "−"  # proper minus sign

# ---------- figure generators ----------
def opener_svg():
    # hill / drone height curve, peak at (2,5); axes 0..5 x, 0..8 y
    pts = [(0,1),(1,3),(2,5),(3,4),(4,2)]
    x0,x1 = 40,235; y0,yTop = 165,15
    def px(t): return x0 + t*(x1-x0)/5.0
    def py(h): return y0 - h*(y0-yTop)/8.0
    parts = []
    parts.append('<svg viewBox="0 0 260 200" role="img" aria-label="Height curve of a drone against time, peaking at height 5 at time 2 seconds" style="max-width:260px" font-family="Inter, sans-serif">')
    parts.append('<line x1="40" y1="15" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="40" y1="165" x2="235" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    for h in range(0,9,2):
        y = py(h)
        parts.append(f'<line x1="37" y1="{y:.1f}" x2="40" y2="{y:.1f}" stroke="currentColor" stroke-width="1"/>')
        parts.append(f'<text x="33" y="{y+3:.1f}" font-size="9" fill="currentColor" text-anchor="end">{h}</text>')
    for t in range(0,6):
        x = px(t)
        parts.append(f'<line x1="{x:.1f}" y1="165" x2="{x:.1f}" y2="168" stroke="currentColor" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="178" font-size="9" fill="currentColor" text-anchor="middle">{t}</text>')
    parts.append('<text x="137" y="193" font-size="9" fill="currentColor" text-anchor="middle">time (s)</text>')
    parts.append('<text x="12" y="90" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 90)">height (m)</text>')
    poly = " ".join(f"{px(t):.1f},{py(h):.1f}" for t,h in pts)
    parts.append(f'<polyline points="{poly}" fill="none" stroke="#f59e0b" stroke-width="2"/>')
    for t,h in pts:
        parts.append(f'<circle cx="{px(t):.1f}" cy="{py(h):.1f}" r="2.6" fill="#f59e0b"/>')
    # mark peak
    parts.append(f'<text x="{px(2):.1f}" y="{py(5)-6:.1f}" font-size="9" fill="currentColor" text-anchor="middle">peak 5</text>')
    parts.append('</svg>')
    return "".join(parts)

def g4_svg():
    # point (1,4) max and its image (1,-4) min under reflection in x-axis
    ox,oy = 110,110  # origin
    sx,sy = 30,18
    def px(x): return ox + x*sx
    def py(y): return oy - y*sy
    p = []
    p.append('<svg viewBox="0 0 220 220" role="img" aria-label="Coordinate grid showing a maximum at (1, 4) and its image, a minimum at (1, -4), after reflection in the x-axis" style="max-width:240px" font-family="Inter, sans-serif">')
    # axes
    p.append(f'<line x1="{px(-3):.0f}" y1="{oy}" x2="{px(3):.0f}" y2="{oy}" stroke="currentColor" stroke-width="1.2"/>')
    p.append(f'<line x1="{ox}" y1="{py(5):.0f}" x2="{ox}" y2="{py(-5):.0f}" stroke="currentColor" stroke-width="1.2"/>')
    p.append(f'<text x="{px(3)-2:.0f}" y="{oy-4}" font-size="9" fill="currentColor" text-anchor="end">x</text>')
    p.append(f'<text x="{ox+5}" y="{py(5)+8:.0f}" font-size="9" fill="currentColor">y</text>')
    # connector (reflection)
    p.append(f'<line x1="{px(1):.0f}" y1="{py(4):.0f}" x2="{px(1):.0f}" y2="{py(-4):.0f}" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.6"/>')
    # points
    p.append(f'<circle cx="{px(1):.0f}" cy="{py(4):.0f}" r="3.2" fill="#60a5fa"/>')
    p.append(f'<text x="{px(1)+6:.0f}" y="{py(4)-2:.0f}" font-size="9" fill="currentColor">(1, 4) max</text>')
    p.append(f'<circle cx="{px(1):.0f}" cy="{py(-4):.0f}" r="3.2" fill="#f59e0b"/>')
    p.append(f'<text x="{px(1)+6:.0f}" y="{py(-4)+10:.0f}" font-size="9" fill="currentColor">(1, {MINUS}4) ?</text>')
    p.append('</svg>')
    return "".join(p)

def parabola_chart(f_blue, f_orange, xs, xmin, xmax, ymin, ymax, lbl_blue, lbl_orange, ystep=2):
    def ds(fn, color, lbl):
        data = [{"x": round(x,2), "y": round(fn(x),3)} for x in xs]
        return {"type":"line","data":data,"tension":0.35,"fill":False,"borderColor":color,"pointRadius":0,"label":lbl}
    return {
        "type":"scatter",
        "data":{"datasets":[ds(f_blue,"#3b82f6",lbl_blue), ds(f_orange,"#f59e0b",lbl_orange)]},
        "options":{"scales":{
            "x":{"min":xmin,"max":xmax,"ticks":{"stepSize":1},"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"x","display":True}},
            "y":{"min":ymin,"max":ymax,"ticks":{"stepSize":ystep},"grid":{"color":"rgba(0,0,0,0.08)"},"title":{"text":"y","display":True}}
        }}
    }

def frange(a,b,step):
    xs=[]; x=a
    while x<=b+1e-9:
        xs.append(round(x,4)); x+=step
    return xs

# S1: y=x^2 and y=x^2+7
xs1 = frange(-3,3,0.5)
chart_s1 = parabola_chart(lambda x:x*x, lambda x:x*x+7, xs1, -3,3, 0,16, "y = x²", "y = x² + 7")
# S2: y=x^2 and y=(x+5)^2
xs2 = frange(-7,2,0.5)
chart_s2 = parabola_chart(lambda x:x*x, lambda x:(x+5)**2, xs2, -7,2, 0,16, "y = x²", "y = (x + 5)²")
# S7: y=sin x and y=-sin x (degrees)
xs7 = frange(0,360,15)
def s_deg(x): return math.sin(math.radians(x))
chart_s7 = {
    "type":"scatter",
    "data":{"datasets":[
        {"type":"line","data":[{"x":x,"y":round(s_deg(x),3)} for x in xs7],"tension":0.35,"fill":False,"borderColor":"#3b82f6","pointRadius":0,"label":"y = sin x"},
        {"type":"line","data":[{"x":x,"y":round(-s_deg(x),3)} for x in xs7],"tension":0.35,"fill":False,"borderColor":"#f59e0b","pointRadius":0,"label":"y = −sin x"},
    ]},
    "options":{"scales":{
        "x":{"min":0,"max":360,"ticks":{"stepSize":90},"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"x (degrees)","display":True}},
        "y":{"min":-1.2,"max":1.2,"ticks":{"stepSize":0.5},"grid":{"color":"rgba(0,0,0,0.08)"},"title":{"text":"y","display":True}}
    }}
}

# ---------- problem bank ----------
def gs(*steps): return list(steps)
def sy(t): return {"say": t}
def box(pre, ans, hint, post="", done=None, phase=None):
    d={"pre":pre,"post":post,"answer":ans,"hint":hint}
    if done: d["done"]=done
    if phase: d["phase"]=phase
    return d

bank = {"bronze": [], "silver": [], "gold": []}

# ---- BRONZE ----
bank["bronze"] = [
  { "display": r"\(y = f(x) + 5\) is a translation. How many units up?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "The +5 is outside f, so it lifts every point by that amount.",
    "misconceptions": [ {"pattern":"direction","check":"direction","expect": None,
      "message": "+5 outside f adds 5 to every y-value, so the graph shifts up by 5.","note":"explanatory"} ],
    "guided_steps": gs(
      sy(r"The +5 is <strong>outside</strong> f, so it changes the y-values. Every point rises by the same amount."),
      box("Take a point at height 2. Add 5: 2 + 5 = ", 7, "Two add five."),
      box("Take a point at height 10. Add 5: 10 + 5 = ", 15, "Ten add five.", phase="substitute"),
      box("Every point rose by the same jump. That jump is the number of units up: ", 5, "The amount you added each time.", done="Adding 5 outside f lifts the whole graph up by 5.", phase="substitute"),
    ) },
  { "display": r"\(y = f(x) - 3\) is a translation. How many units and which direction?",
    "options": ["Down 3","Up 3","Right 3","Left 3"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"Outside f, a subtraction lowers every y-value.",
    "misconceptions":[{"pattern":"direction","check":"direction","expect":None,
      "message":"−3 outside f takes 3 off every y-value, so the graph shifts down by 3.","note":"MC"}] },
  { "display": r"\(y = f(x - 4)\) is a translation. Which direction?",
    "options":["Right 4","Left 4","Up 4","Down 4"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"Inside f the effect is opposite to the sign you see.",
    "misconceptions":[{"pattern":"inside_opposite","check":"inside_opposite","expect":None,
      "message":"Inside f the effect is opposite: f(x − 4) shifts right by 4, not left.","note":"MC"}] },
  { "display": r"\(y = f(x + 2)\) is a translation. Which direction?",
    "options":["Left 2","Right 2","Up 2","Down 2"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"Inside f the effect is opposite to the sign you see.",
    "misconceptions":[{"pattern":"inside_opposite","check":"inside_opposite","expect":None,
      "message":"f(x + 2) shifts left by 2, opposite to the plus sign inside.","note":"MC"}] },
  { "display": r"\(y = -f(x)\) is a reflection. In which axis?",
    "options":["x-axis","y-axis","Line y = x","Line x = 0"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"A minus outside f flips the sign of every y-value.",
    "misconceptions":[{"pattern":"reflect","check":"reflect","expect":None,
      "message":"Negative outside f: reflect in the x-axis, because every y-value flips sign.","note":"MC"}] },
  { "display": r"\(y = f(-x)\) is a reflection. In which axis?",
    "options":["y-axis","x-axis","Line y = x","Line x = 1"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"A minus inside f flips the sign of every x-value.",
    "misconceptions":[{"pattern":"reflect","check":"reflect","expect":None,
      "message":"Negative inside f: reflect in the y-axis, because every x-value flips sign.","note":"MC"}] },
  { "display": r"The point \((3, 5)\) is on \(y = f(x)\). What point is on \(y = f(x) + 4\)?",
    "options": [r"\((3, 9)\)", r"\((7, 5)\)", r"\((3, 1)\)", r"\((-1, 5)\)"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"The +4 is outside f, so only the y-value changes.",
    "misconceptions":[{"pattern":"direction","check":"direction","expect":None,
      "message":"+4 outside f shifts y up: (3, 5 + 4) = (3, 9). The x stays the same.","note":"MC"}] },
  { "display": r"The point \((2, 6)\) is on \(y = f(x)\). What point is on \(y = f(x - 1)\)?",
    "options":[r"\((3, 6)\)", r"\((1, 6)\)", r"\((2, 7)\)", r"\((2, 5)\)"], "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"Inside f, x moves the opposite way to the sign.",
    "misconceptions":[{"pattern":"inside_opposite","check":"inside_opposite","expect":None,
      "message":"f(x − 1) shifts right by 1: (2 + 1, 6) = (3, 6). The y stays the same.","note":"MC"}] },
]

# ---- SILVER ----
bank["silver"] = [
  { "display": r"Describe the transformation from \(y = x^2\) to \(y = x^2 + 7\).",
    "options":["Translation up 7","Translation right 7","Vertical stretch ×7","Translation down 7"], "solutions":[0],
    "calculator":False, "input_type":"multiple_choice",
    "hint":"The +7 is outside, added after squaring.",
    "chart": chart_s1,
    "misconceptions":[{"pattern":"direction","check":"direction","expect":None,
      "message":"+7 is outside the function, so it is a vertical shift up by 7.","note":"MC"}] },
  { "display": r"Describe the transformation from \(y = x^2\) to \(y = (x + 5)^2\).",
    "options":["Translation left 5","Translation right 5","Translation up 5","Translation down 5"], "solutions":[0],
    "calculator":False, "input_type":"multiple_choice",
    "hint":"The +5 is inside the bracket, so the effect is opposite.",
    "chart": chart_s2,
    "misconceptions":[{"pattern":"inside_opposite","check":"inside_opposite","expect":None,
      "message":"+5 inside the bracket means left 5, opposite to the plus sign.","note":"MC"}] },
  { "display": r"\(y = 3f(x)\). What is the scale factor of the vertical stretch?",
    "solutions":[3], "calculator":False, "input_type":"single_value",
    "hint":"The 3 multiplies f(x), so it multiplies every y-value.",
    "misconceptions":[{"pattern":"stretch","check":"stretch","expect":None,
      "message":"3 outside f multiplies every y-value by 3: a vertical stretch, scale factor 3.","note":"explanatory"}],
    "guided_steps": gs(
      sy(r"The 3 is <strong>outside</strong> f, multiplying the whole function. That multiplies every y-value."),
      box("A point at height 2 becomes 3 × 2 = ", 6, "Three times two."),
      box("A point at height 5 becomes 3 × 5 = ", 15, "Three times five.", phase="substitute"),
      box("Every height was multiplied by the same number. That number is the scale factor: ", 3, "The multiplier you used.", done="Every y-value is tripled, so the vertical stretch scale factor is 3.", phase="substitute"),
    ) },
  { "display": r"\(y = f(2x)\). What is the scale factor of the horizontal stretch?",
    "solutions":[1,2], "calculator":False, "input_type":"fraction",
    "hint":"Inside f, the stretch factor is the reciprocal of the number.",
    "misconceptions":[{"pattern":"reciprocal","check":"reciprocal","expect":None,
      "message":"f(2x) squashes the graph: horizontal stretch scale factor ½, the reciprocal of 2.","note":"explanatory"}],
    "guided_steps": gs(
      sy(r"The 2 is <strong>inside</strong> f, so it changes x, and the stretch factor is the <strong>reciprocal</strong> of 2."),
      box("Flip the 2 into a fraction: 1 ÷ 2 = ", 0.5, "One half as a decimal."),
      box("Check with a point: x = 6 moves to 6 ÷ 2 = ", 3, "Six shared into two.", phase="substitute"),
      box("The width halves, so as a decimal the scale factor is ", 0.5, "The reciprocal of 2.", done="f(2x) has horizontal stretch scale factor ½ = 0.5; the graph is half as wide.", phase="substitute"),
    ) },
  { "display": r"The point \((4, 3)\) is on \(y = f(x)\). What is the corresponding point on \(y = 2f(x)\)?",
    "options":[r"\((4, 6)\)", r"\((8, 3)\)", r"\((2, 3)\)", r"\((4, 1.5)\)"], "solutions":[0],
    "calculator":False, "input_type":"multiple_choice",
    "hint":"A vertical stretch changes y and leaves x alone.",
    "misconceptions":[{"pattern":"stretch","check":"stretch","expect":None,
      "message":"Vertical stretch ×2: y doubles, x stays. (4, 3 × 2) = (4, 6).","note":"MC"}] },
  { "display": r"The point \((6, 2)\) is on \(y = f(x)\). What is the corresponding point on \(y = f(3x)\)?",
    "options":[r"\((2, 2)\)", r"\((18, 2)\)", r"\((6, 6)\)", r"\((6, \frac{2}{3})\)"], "solutions":[0],
    "calculator":False, "input_type":"multiple_choice",
    "hint":"A horizontal stretch divides x by the number and leaves y alone.",
    "misconceptions":[{"pattern":"reciprocal","check":"reciprocal","expect":None,
      "message":"Horizontal stretch, factor ⅓: x divides by 3, y stays. (6 ÷ 3, 2) = (2, 2).","note":"MC"}] },
  { "display": r"Describe the transformation from \(y = \sin x\) to \(y = -\sin x\).",
    "options":["Reflection in the x-axis","Reflection in the y-axis","Translation down 1","Vertical stretch ×(−1)"], "solutions":[0],
    "calculator":False, "input_type":"multiple_choice",
    "hint":"A minus outside the function flips y-values.",
    "chart": chart_s7,
    "misconceptions":[{"pattern":"reflect","check":"reflect","expect":None,
      "message":"Negative outside the function is a reflection in the x-axis: every y-value flips sign.","note":"MC"}] },
]

# ---- GOLD ----
bank["gold"] = [
  { "display": r"Describe the single transformation from \(y = x^2\) to \(y = (x - 4)^2 + 3\). Give the horizontal component of the translation vector.",
    "solutions":[4], "calculator":False, "input_type":"single_value",
    "hint":"Read the bracket for the horizontal move; it is opposite to the sign.",
    "misconceptions":[
      {"pattern":"swap_components","check":"swap_components","expect":3,
       "message":"The horizontal component comes from the bracket: (x − 4) gives right 4. The 3 is the vertical component.","note":"error: gives vertical 3"},
      {"pattern":"inside_sign","check":"inside_sign","expect":-4,
       "message":"(x − 4) shifts right 4, so the horizontal component is +4, not −4.","note":"error: keeps sign, -4"},
    ],
    "guided_steps": gs(
      sy(r"Compare with \(y = x^2\). Look at the bracket for the horizontal move and the number added outside for the vertical move."),
      box("Inside the bracket is (x − 4). Inside shifts are opposite the sign, so this is right by ", 4, "Opposite of minus is a move to the right."),
      box("Outside is + 3, which lifts the curve up by ", 3, "Added outside means up.", phase="substitute"),
      box("The translation vector is (right, up) = (4, 3). Type the horizontal component: ", 4, "The first number in the vector.", done="Translation vector (4, 3): the horizontal component is 4.", phase="substitute"),
    ) },
  { "display": r"The point \((5, -1)\) is on \(y = f(x)\). Find the point on \(y = f(x + 3) - 2\). Give the x-coordinate.",
    "solutions":[2], "calculator":False, "input_type":"single_value",
    "hint":"The +3 is inside f, so x moves the opposite way.",
    "misconceptions":[
      {"pattern":"inside_sign","check":"inside_sign","expect":8,
       "message":"f(x + 3) shifts left 3, so x = 5 − 3 = 2. Moving right gives 8 and is the wrong direction.","note":"error: 5+3=8"},
    ],
    "guided_steps": gs(
      sy(r"The +3 is <strong>inside</strong> f, so it moves x the opposite way: left 3. The −2 is outside and moves y."),
      box("Inside +3 means shift left 3. New x = 5 − 3 = ", 2, "Take three off the x-value."),
      box("The −2 outside changes y: −1 − 2 = ", -3, "Two below negative one.", phase="substitute"),
      box("The question asks only for the x-coordinate. Type it: ", 2, "The new x-value.", done="The image is (2, −3); the x-coordinate is 2.", phase="substitute"),
    ) },
  { "display": r"The point \((5, -1)\) is on \(y = f(x)\). Find the point on \(y = f(x + 3) - 2\). Give the y-coordinate.",
    "solutions":[-3], "calculator":False, "input_type":"single_value",
    "hint":"The −2 is outside f, so it lowers the y-value.",
    "misconceptions":[
      {"pattern":"outside_sign","check":"outside_sign","expect":1,
       "message":"−2 outside f subtracts 2: y = −1 − 2 = −3. Adding 2 instead gives 1.","note":"error: -1+2=1"},
      {"pattern":"ignore_outside","check":"ignore_outside","expect":-1,
       "message":"The −2 must be applied: y = −1 − 2 = −3. Leaving y unchanged gives −1.","note":"error: ignores outside shift"},
    ],
    "guided_steps": gs(
      sy(r"The +3 inside only moves x. The −2 outside is what changes the y-value."),
      box("The inside +3 changes x, not y, so first find new x = 5 − 3 = ", 2, "Left three."),
      box("Now the −2 outside changes y: −1 − 2 = ", -3, "Two below negative one.", phase="substitute"),
      box("The question asks only for the y-coordinate. Type it: ", -3, "The new y-value.", done="The image is (2, −3); the y-coordinate is −3.", phase="substitute"),
    ) },
  { "display": r"\(y = f(x)\) has a maximum at \((1, 4)\). Describe the corresponding turning point on \(y = -f(x)\).",
    "options":[r"Minimum at \((1, -4)\)", r"Maximum at \((-1, 4)\)", r"Maximum at \((1, -4)\)", r"Minimum at \((-1, -4)\)"],
    "solutions":[0], "calculator":False, "input_type":"multiple_choice",
    "hint":"Reflecting in the x-axis flips y-values and turns a maximum into a minimum.",
    "misconceptions":[{"pattern":"reflect","check":"reflect","expect":None,
      "message":"Reflection in the x-axis: the y-value flips sign and a maximum becomes a minimum, so (1, 4) becomes a minimum at (1, −4).","note":"MC"}] },
  { "display": r"\(y = f(x)\) passes through \((0, 3)\) and \((6, 0)\). \(y = f(2x)\) passes through \((a, 3)\) and \((b, 0)\). Find \(b\).",
    "solutions":[3], "calculator":False, "input_type":"single_value",
    "hint":"Inside f, the 2 divides every x-value by 2.",
    "misconceptions":[
      {"pattern":"multiply_not_divide","check":"multiply_not_divide","expect":12,
       "message":"f(2x) halves x-values: b = 6 ÷ 2 = 3. Multiplying by 2 gives 12 and is the wrong way.","note":"error: 6x2=12"},
      {"pattern":"x_unchanged","check":"x_unchanged","expect":6,
       "message":"f(2x) does change x: b = 6 ÷ 2 = 3. Leaving x as 6 ignores the stretch.","note":"error: leaves 6"},
    ],
    "guided_steps": gs(
      sy(r"For \(y = f(2x)\) the 2 is <strong>inside</strong> f, so every x-value is divided by 2. The y-values do not change."),
      box("Take the point (6, 0). Halve its x: 6 ÷ 2 = ", 3, "Six shared into two."),
      box("Check the other point (0, 3). Halve its x: 0 ÷ 2 = ", 0, "Zero halved.", phase="substitute"),
      box("So (6, 0) maps to (3, 0). The value of b is ", 3, "The new x where the curve crosses.", done="Under f(2x), (6, 0) becomes (3, 0), so b = 3.", phase="substitute"),
    ) },
]

bank["bronze_description"] = "Name a single shift or reflection of a graph, and apply it to one point."
bank["silver_description"] = "Describe shifts and stretches in words, and find scale factors and image points."
bank["gold_description"] = "Handle combined transformations, translation vectors and reflected turning points."

# ---------- tier_guides ----------
tier_guides = {
  "bronze": {
    "title": "Bronze: shifts and reflections of a graph",
    "steps": [
      r"Outside f changes y: \(f(x) + a\) moves up a, \(f(x) - a\) moves down a.",
      r"Inside f changes x, opposite to the sign: \(f(x - a)\) moves right a, \(f(x + a)\) moves left a.",
      r"Reflections: \(-f(x)\) flips in the x-axis; \(f(-x)\) flips in the y-axis.",
    ],
    "example": {
      "question": "The point (2, 6) is on y = f(x). Find its image on y = f(x − 1).",
      "steps": [
        {"label":"Spot the change","content":"(x − 1) is inside f: an inside shift"},
        {"label":"Apply it","content":"Opposite the sign: right 1, so x = 2 + 1 = 3"},
        {"label":"Check","content":"Only x moves for an inside shift; y stays 6"},
        {"label":"Answer","content":"(3, 6)","isAnswer":True,"is_answer":True},
      ]
    }
  },
  "silver": {
    "title": "Silver: describing shifts and stretches",
    "steps": [
      r"\(af(x)\) is a vertical stretch, scale factor a: every y-value is multiplied by a.",
      r"\(f(ax)\) is a horizontal stretch, scale factor \(\frac{1}{a}\): every x-value is divided by a.",
      r"For \(y = x^2\): \((x + 5)^2\) reads as left 5, and \(x^2 + 7\) as up 7.",
    ],
    "example": {
      "question": "The point (4, 3) is on y = f(x). Find its image on y = 2f(x).",
      "steps": [
        {"label":"Spot the change","content":"2 outside f: a vertical stretch"},
        {"label":"Apply it","content":"y doubles: 3 × 2 = 6; x is unchanged"},
        {"label":"Check","content":"A vertical stretch keeps x the same"},
        {"label":"Answer","content":"(4, 6)","isAnswer":True,"is_answer":True},
      ]
    }
  },
  "gold": {
    "title": "Gold: combined transformations and vectors",
    "steps": [
      r"Combine an inside change with an outside one: \(f(x + a) + b\) shifts left a and up b.",
      r"Translation vector (right, up): \((x - 2)^2 + 3\) gives the vector \(\binom{2}{3}\).",
      r"Under \(-f(x)\), a maximum becomes a minimum: the y-value flips sign, x stays.",
    ],
    "example": {
      "question": "Describe y = x² to y = (x − 2)² + 3.",
      "steps": [
        {"label":"Inside","content":"(x − 2): right 2"},
        {"label":"Outside","content":"+ 3: up 3"},
        {"label":"Check","content":"Vector reads (right, up)"},
        {"label":"Answer","content":"Translation (2, 3)","isAnswer":True,"is_answer":True},
      ]
    }
  },
}

# ---------- guided (opener + teach) ----------
opener = {
  "display": opener_svg() + '<span class="figure-caption">A drone’s height over time (peak 5 m)</span><p>To make the drone fly the whole path 3 m higher, add 3 to every height.</p>',
  "steps": [
    {"pre":"The peak was at height 5. After adding 3, the new peak height is 5 + 3 = ","post":"","answer":8,"hint":"Five add three."},
    {"pre":"A point that was at height 1 rises to 1 + 3 = ","post":"","answer":4,"hint":"One add three."},
    {"say": r"Every point rose by the same 3. That is exactly \(y = f(x) + 3\): adding a number <strong>outside</strong> f shifts the whole graph <strong>up</strong>. In this lesson you also meet inside changes like \(f(x - a)\) (which move sideways), stretches \(af(x)\) and \(f(ax)\), and reflections \(-f(x)\) and \(f(-x)\)."},
  ]
}

teach = {
  "bronze": {
    "display": r"The point \((2, 5)\) is on \(y = f(x)\). Find its image on \(y = f(x - 3) + 1\).",
    "steps": [
      sy(r"Inside the bracket changes x (opposite the sign); the number outside changes y."),
      box("Inside is (x − 3): opposite sign means right, so new x = 2 + 3 = ", 5, "Add three to the x-value."),
      box("Outside is + 1: shift up, so new y = 5 + 1 = ", 6, "Add one to the y-value."),
      box("Type the x-coordinate of the image point: ", 5, "The x you just found."),
      box("Type the y-coordinate of the image point: ", 6, "The y you just found.", done="Inside moved x right 3, outside moved y up 1: the image is (5, 6)."),
    ]
  },
  "silver": {
    "display": r"The point \((4, 6)\) is on \(y = f(x)\). Find its image on \(y = 2f(x)\), then on \(y = f(2x)\).",
    "steps": [
      sy(r"Outside multipliers stretch y; inside multipliers divide x (the reciprocal)."),
      box("For 2f(x), multiply y by 2: 6 × 2 = ", 12, "Six doubled."),
      box("x is unchanged, so that image is (4, 12). Now f(2x): divide x by 2: 4 ÷ 2 = ", 2, "Four shared into two."),
      box("The horizontal stretch factor of f(2x) is 1 ÷ 2 = ", 0.5, "The reciprocal of 2."),
      box("The vertical stretch factor of 2f(x) is ", 2, "The multiplier outside f.", done="2f(x) doubles y (factor 2); f(2x) halves x (factor ½)."),
    ]
  },
  "gold": {
    "display": r"\(y = x^2\) is transformed to \(y = (x + 1)^2 - 4\). Find the coordinates of the new vertex.",
    "steps": [
      sy(r"The vertex of \(y = x^2\) is at (0, 0). Move it by the inside and outside changes."),
      box("Inside (x + 1): opposite sign means left, so the vertex x = 0 − 1 = ", -1, "One to the left of zero."),
      box("Outside − 4: shift down, so the vertex y = 0 − 4 = ", -4, "Four below zero."),
      box("Type the x-coordinate of the new vertex: ", -1, "The x you just found."),
      box("Type the y-coordinate of the new vertex: ", -4, "The y you just found.", done="Left 1 and down 4 move the vertex from (0, 0) to (−1, −4)."),
    ]
  },
}
# add a chart to the gold teach: y=x^2 and y=(x+1)^2-4
teach["gold"]["chart"] = parabola_chart(lambda x:x*x, lambda x:(x+1)**2-4, frange(-5,3,0.5), -5,3, -5,12, "y = x²", "y = (x + 1)² − 4")

# ---------- method_card (slim) ----------
method_card = {
  "title": "How to Transform Graphs",
  "steps": [
    r"Outside f changes y: \(f(x) + a\) is up a; \(af(x)\) stretches y by a.",
    r"Inside f changes x, opposite: \(f(x - a)\) is right a; \(f(ax)\) stretches x by \(\frac{1}{a}\).",
    r"\(-f(x)\) reflects in the x-axis; \(f(-x)\) reflects in the y-axis.",
    r"Combine them: \(f(x - a) + b\) translates by vector \(\binom{a}{b}\).",
  ],
  "content": r"<p>Starting from \(y = f(x)\):</p><p><strong>Outside</strong> the function changes y directly. \(f(x) + a\) shifts up a; \(af(x)\) stretches vertically by a; \(-f(x)\) reflects in the x-axis.</p><p><strong>Inside</strong> the function changes x, and always the opposite way you expect. \(f(x - a)\) shifts right a; \(f(ax)\) stretches horizontally by \(\frac{1}{a}\); \(f(-x)\) reflects in the y-axis.</p>",
  "example": r"<p><strong>\(y = x^2 \to y = (x - 3)^2 + 2\).</strong> Inside \((x - 3)\): right 3. Outside \(+2\): up 2. Translation vector \(\binom{3}{2}\).</p>",
}

# ---------- assemble ----------
live = json.load(io.open("_live_graphsL07.json", encoding="utf-8"))
pd = {
  "method_card": method_card,
  "topic_links": live["topic_links"],
  "problem_bank": bank,
  "related_videos": live.get("related_videos", []),
  "worked_examples": live.get("worked_examples", []),
  "tier_guides": tier_guides,
  "guided": {"opener": opener, "teach": teach},
}

json.dump(pd, io.open("lesson_maths-aqa_graphs-L07.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_graphs-L07.json")

# quick em-dash scan
def scan(o,p=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,p+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{p}[{i}]")
    elif isinstance(o,str) and "—" in o:
        print("EMDASH at",p)
scan(pd)
print("emdash scan done")
