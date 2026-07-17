# -*- coding: utf-8 -*-
"""Build full guided-learning + diagrams practice_data for maths-aqa graphs-L01.
Every box value is computed here so the arithmetic is machine-checked."""
import json, io

def num(n):
    # format a number for display: ints without .0
    if isinstance(n, float) and n.is_integer():
        n = int(n)
    return n

def s(n):
    n = num(n)
    return str(n)

def fmt(n):
    # bracket negatives for readable subtraction text
    n = num(n)
    return "(%s)" % n if (isinstance(n,(int,float)) and n < 0) else str(n)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": num(answer), "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(text):
    return {"say": text}

def misc(pattern, message, expect, note):
    return {"pattern": pattern, "message": message, "expect": num(expect) if expect is not None else None, "note": note}

# ---------- walk builders ----------
def walk_grad_points(x1,y1,x2,y2):
    rise=y2-y1; run=x2-x1; m=rise/run
    return [
        sayonly("Gradient means rise over run: how far up for how far across. Start with the rise, the change in y."),
        box("Rise = %s − %s = "%(fmt(y2),fmt(y1)), rise, "Take the first y from the second y."),
        box("Run = %s − %s = "%(fmt(x2),fmt(x1)), run, "Take the first x from the second x. Subtracting a negative adds."),
        box("Gradient = rise ÷ run = %s ÷ %s = "%(fmt(rise),fmt(run)), num(m), "Divide the rise by the run.", phase="substitute"),
        box("Check: gradient × run = %s × %s = "%(fmt(m),fmt(run)), rise, "Multiply back. It should return the rise.", done="It gives the rise back, so the gradient is right.", phase="substitute"),
    ]

def walk_read_c(m,c):
    # read the y-intercept c from y = mx + c
    x1=1; y1=m*1+c
    return [
        sayonly("In y = mx + c, the gradient m sits in front of x and the intercept c stands alone."),
        box("The number in front of x is the gradient m = ", m, "It is written just before the x."),
        box("The number on its own is the intercept c = ", c, "It is the term with no x."),
        box("The y-intercept is c, so the answer is ", c, "The intercept is c, not m.", phase="substitute"),
        box("Check at x = 0: y = m × 0 + c = ", c, "Anything times 0 is 0, leaving just c.", done="At x = 0 the line sits at c, which is the y-intercept.", phase="substitute"),
    ]

def walk_read_m(m,c):
    # read the gradient m from y = mx + c, verified by a rise of 1 in x
    y0=m*0+c; y1=m*1+c
    return [
        sayonly("In y = mx + c, the gradient m is the number multiplying x."),
        box("The number on its own is the intercept c = ", c, "It is the term with no x."),
        box("At x = 0: y = ", y0, "That is just c."),
        box("At x = 1: y = %s × 1 + %s = "%(fmt(m),fmt(c)), y1, "Work out m times 1, then add c.", phase="substitute"),
        box("The gradient is the rise for one step across: %s − %s = "%(fmt(y1),fmt(y0)), m, "Subtract the two y-values.", done="y rises by m for each step, so the gradient is m.", phase="substitute"),
    ]

def walk_sub_y(m,c,x):
    # find y = m x + c
    mx=m*x; y=mx+c
    return [
        sayonly("Substitute the x-value into y = mx + c, doing the multiplication first."),
        box("The gradient part: %s × %s = "%(fmt(m),fmt(x)), mx, "Multiply m by x before touching c."),
        box("Now add the intercept: %s + %s = "%(fmt(mx),fmt(c)), y, "Add c to what you just found.", phase="substitute"),
        box("Check the point (%s, %s) fits: %s × %s + %s = "%(s(x),s(y),fmt(m),fmt(x),fmt(c)), y, "Work the equation once more.", done="The point fits the line, so y is correct.", phase="substitute"),
    ]

def walk_find_m_from_point(m,c,x,y):
    # y = m x + c, c known, find m from point (x,y): m x = y - c
    yc=y-c
    return [
        sayonly("Put the point into y = mx + c and peel away the known parts."),
        box("Take the intercept off both sides: %s − %s = "%(fmt(y),fmt(c)), yc, "Subtract c from y."),
        box("So %s × m = %s. Divide by %s: m = "%(s(x),s(yc),s(x)), m, "Divide by the number in front of m.", phase="substitute"),
        box("Check: %s × %s + %s = "%(fmt(m),fmt(x),fmt(c)), y, "Put m back and confirm the point.", done="It returns the point's y, so m is right.", phase="substitute"),
    ]

def walk_find_c(x1,y1,x2,y2):
    # find c: first gradient, then c from a point
    rise=y2-y1; run=x2-x1; m=rise/run; mx=m*x1; c=y1-mx
    return [
        sayonly("First find the gradient, then use a point to pin down c."),
        box("Rise = %s − %s = "%(fmt(y2),fmt(y1)), rise, "Second y minus first y."),
        box("Run = %s − %s = "%(fmt(x2),fmt(x1)), run, "Second x minus first x."),
        box("Gradient m = %s ÷ %s = "%(fmt(rise),fmt(run)), num(m), "Divide rise by run."),
        box("Now use (%s, %s): the mx part is %s × %s = "%(s(x1),s(y1),fmt(m),fmt(x1)), mx, "Multiply the gradient by that x.", phase="substitute"),
        box("So %s = %s + c, giving c = %s − %s = "%(s(y1),s(mx),fmt(y1),fmt(mx)), c, "Take the mx part off the y-value.", done="That c completes y = mx + c.", phase="substitute"),
    ]

def walk_rearrange_grad(k, div, const):
    # k y? Actually: div * y = k x + const  -> y = (k/div) x + const/div ; gradient = k/div
    m=k/div; c=const/div
    return [
        sayonly("Get the equation into y = mx + c first by dividing every term."),
        box("Divide the x term by %s: %s ÷ %s = "%(s(div),fmt(k),s(div)), num(m), "Divide the number in front of x.", post="x"),
        box("Divide the constant by %s: %s ÷ %s = "%(s(div),fmt(const),s(div)), num(c), "Divide the lone number too."),
        box("Now y = %sx + %s. The gradient is the number in front of x: "%(s(m),fmt(c)), num(m), "Read the coefficient of x.", phase="substitute"),
        box("Check: from x = 0 (y = %s) to x = 1 (y = %s), the rise is %s − %s = "%(s(c),s(m+c),fmt(m+c),fmt(c)), num(m), "One step across raises y by the gradient.", done="y climbs by the gradient each step, confirming it.", phase="substitute"),
    ]

def walk_graph_grad(x1,y1,x2,y2):
    rise=y2-y1; run=x2-x1; m=rise/run
    return [
        sayonly("Read two clear points where the line crosses the grid, then use rise over run."),
        box("First point, at x = %s: read y = "%s(x1), y1, "Trace up from the x-axis to the line."),
        box("Second point, at x = %s: read y = "%s(x2), y2, "Trace up from the x-axis to the line."),
        box("Rise = %s − %s = "%(fmt(y2),fmt(y1)), rise, "Difference in the y readings."),
        box("Run = %s − %s = "%(fmt(x2),fmt(x1)), run, "Difference in the x values.", phase="substitute"),
        box("Gradient = rise ÷ run = %s ÷ %s = "%(fmt(rise),fmt(run)), num(m), "Divide the rise by the run.", done="Rise over run gives the line's gradient.", phase="substitute"),
    ]

def walk_graph_yint(xa,ya,xb,yb,grad):
    # read two points, step back to x=0
    return [
        sayonly("The y-intercept is where the line cuts the vertical axis, at x = 0."),
        box("Read a point at x = %s: y = "%s(xa), ya, "Trace up to the line."),
        box("Read another at x = %s: y = "%s(xb), yb, "Trace up to the line."),
        box("Gradient = (%s − %s) ÷ (%s − %s) = "%(fmt(yb),fmt(ya),fmt(xb),fmt(xa)), grad, "Rise over run between your two points."),
        box("Step left from (%s, %s) to x = 0: y = %s − %s = "%(s(xa),s(ya),fmt(ya),fmt(grad*xa)), ya-grad*xa, "Each step left lowers y by the gradient.", phase="substitute"),
        box("So the line crosses the y-axis at y = ", ya-grad*xa, "That crossing height is the intercept.", done="The line meets the y-axis there, so that is the y-intercept.", phase="substitute"),
    ]

def walk_graph_read_sub(m,c,x):
    mx=m*x; y=mx+c
    return [
        sayonly("Use the equation to predict the value, then check it against the graph."),
        box("The gradient part: %s × %s = "%(fmt(m),fmt(x)), mx, "Keep the sign on the gradient."),
        box("Add the intercept: %s + %s = "%(fmt(mx),fmt(c)), y, "Add c.", phase="substitute"),
        box("On the graph, trace x = %s up to the line: y = "%s(x), y, "Read across to the y-axis.", done="Calculation and reading agree.", phase="substitute"),
    ]

def walk_sub_third(x):
    # S4: y = (1/3)x + 2
    a=x//3; y=a+2
    return [
        sayonly("A gradient of one third means divide the x-value by 3, then add the intercept."),
        box("One third of %s is %s ÷ 3 = "%(s(x),s(x)), a, "Divide by 3."),
        box("Add the intercept 2: %s + 2 = "%s(a), y, "Add 2.", phase="substitute"),
        box("Check (%s, %s): %s ÷ 3 + 2 = "%(s(x),s(y),s(x)), y, "Run it through once more.", done="The point sits on the line, so the value is right.", phase="substitute"),
    ]

# ---------- SVG builders ----------
def svg_savings():
    # y = 3x + 5, weeks 0..4, £5..17. Plot origin (40,165); 47.5 px/week; 7.5 px/£
    def px(w): return 40 + w*47.5
    def py(v): return 165 - v*7.5
    p0=(px(0),py(5)); p4=(px(4),py(17)); p1=(px(1),py(8))
    parts=[]
    parts.append('<svg viewBox="0 0 260 195" role="img" aria-label="Line graph of Sam\'s savings in pounds against weeks, a straight line rising from 5 pounds at week 0 by 3 pounds each week" style="max-width:260px" font-family="Inter, sans-serif">')
    # axes
    parts.append('<line x1="40" y1="15" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="40" y1="165" x2="235" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    # y gridline ticks at 5,10,15,20
    for v in (5,10,15,20):
        y=py(v)
        parts.append('<line x1="37" y1="%.1f" x2="40" y2="%.1f" stroke="currentColor" stroke-width="1"/>'%(y,y))
        parts.append('<text x="33" y="%.1f" font-size="9" fill="currentColor" text-anchor="end">%d</text>'%(y+3,v))
    for w in (0,1,2,3,4):
        x=px(w)
        parts.append('<line x1="%.1f" y1="165" x2="%.1f" y2="168" stroke="currentColor" stroke-width="1"/>'%(x,x))
        parts.append('<text x="%.1f" y="179" font-size="9" fill="currentColor" text-anchor="middle">%d</text>'%(x,w))
    # the line
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3b82f6" stroke-width="2"/>'%(p0[0],p0[1],p4[0],p4[1]))
    # points
    for (cx,cy) in (p0,p1):
        parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>'%(cx,cy))
    parts.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor">£5</text>'%(p0[0]+5,p0[1]-2))
    parts.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor">£8</text>'%(p1[0]+4,p1[1]-2))
    # axis titles
    parts.append('<text x="137" y="192" font-size="10" fill="currentColor" text-anchor="middle">weeks</text>')
    parts.append('<text x="12" y="90" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 90)">savings (£)</text>')
    parts.append('</svg>')
    return "".join(parts)

def svg_line(points, xmin,xmax,ymin,ymax, aria):
    # generic line-through-points figure for teach; points list of (x,y)
    W=260; H=195; L=40; R=235; T=15; B=165
    def px(x): return L + (x-xmin)/(xmax-xmin)*(R-L)
    def py(y): return B - (y-ymin)/(ymax-ymin)*(B-T)
    parts=['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:260px" font-family="Inter, sans-serif">'%(W,H,aria)]
    # find y=0 axis position if within range else bottom
    y0 = py(0) if ymin<=0<=ymax else B
    x0 = px(0) if xmin<=0<=xmax else L
    parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1.2"/>'%(x0,T,x0,B))
    parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-width="1.2"/>'%(L,y0,R,y0))
    # x ticks integers
    x=xmin
    while x<=xmax:
        if x!=0:
            parts.append('<text x="%.1f" y="%.1f" font-size="8" fill="currentColor" text-anchor="middle">%d</text>'%(px(x),y0+11,x))
        x+=1
    # y ticks every 2
    yv=ymin
    while yv<=ymax:
        if yv!=0 and yv%2==0:
            parts.append('<text x="%.1f" y="%.1f" font-size="8" fill="currentColor" text-anchor="end">%d</text>'%(x0-4,py(yv)+3,yv))
        yv+=1
    # line
    p_first=points[0]; p_last=points[-1]
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ef4444" stroke-width="2"/>'%(px(p_first[0]),py(p_first[1]),px(p_last[0]),py(p_last[1])))
    for (cx,cy) in points:
        parts.append('<circle cx="%.1f" cy="%.1f" r="3" fill="#ef4444"/>'%(px(cx),py(cy)))
    parts.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor" text-anchor="middle">x</text>'%(R-2,y0-4))
    parts.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor">y</text>'%(x0+4,T+4))
    parts.append('</svg>')
    return "".join(parts)

# ---------- assemble problems ----------
def prob(display, sol, hint, walk, miscs=None, chart=None):
    d={"display":display,"solutions":[num(sol)],"calculator":False,"input_type":"single_value",
       "hint":hint,"misconceptions":miscs or [],"guided_steps":walk}
    if chart is not None: d["chart"]=chart
    return d

bronze=[
 prob("Find the gradient of the line through \\((0, 1)\\) and \\((4, 9)\\).",2,
      "Rise over run: the change in y divided by the change in x.",
      walk_grad_points(0,1,4,9),
      [misc("rise_run_inverted","Rise = 9 − 1 = 8, Run = 4 − 0 = 4. Gradient = 8 ÷ 4 = 2. Run over rise gives 0.5, which is upside down; the vertical change goes on top.",0.5,"inverted run/rise = 4/8")]),
 prob("Find the gradient of the line through \\((2, 3)\\) and \\((5, 12)\\).",3,
      "Work out the rise and the run, then divide rise by run.",
      walk_grad_points(2,3,5,12),
      [misc("forgot_to_divide","Rise = 12 − 3 = 9 is only the top of the fraction. Divide by the run: 9 ÷ 3 = 3.",9,"stops at rise before dividing")]),
 prob("A line has equation \\(y = 3x + 5\\). What is the y-intercept?",5,
      "The y-intercept is c, the number with no x next to it.",
      walk_read_c(3,5),
      [misc("confused_m_and_c","In y = mx + c the y-intercept is c, the number on its own. Here c = 5. The 3 is the gradient.",3,"reports m instead of c")]),
 prob("A line has equation \\(y = 7x - 4\\). What is the gradient?",7,
      "The gradient is m, the number multiplying x.",
      walk_read_m(7,-4),
      [misc("confused_m_and_c","The gradient is m, the number in front of x. Here m = 7. The −4 is the y-intercept.",-4,"reports c instead of m")]),
 prob("For the line \\(y = 3x + 1\\), find \\(y\\) when \\(x = 4\\).",13,
      "Multiply 3 by 4 first, then add 1.",
      walk_sub_y(3,1,4),
      [misc("order_of_operations","Multiply before adding: 3 × 4 = 12, then 12 + 1 = 13. Doing 4 + 1 first, then × 3, gives 15.",15,"3*(4+1)=15")]),
 prob("A line passes through \\((0, 5)\\) and \\((2, 13)\\). What is the gradient?",4,
      "Rise over run between the two points.",
      walk_grad_points(0,5,2,13),
      [misc("rise_run_inverted","Rise = 13 − 5 = 8, Run = 2 − 0 = 2. Gradient = 8 ÷ 2 = 4. Run over rise (0.25) is upside down.",0.25,"inverted run/rise = 2/8")]),
 prob("What is the gradient of the line \\(y = -2x + 9\\)?",-2,
      "The gradient is the number in front of x, including its sign.",
      walk_read_m(-2,9),
      [misc("sign_error","The gradient carries its sign. Here m = −2. Dropping the minus and writing 2 reverses the line's direction.",2,"drops the sign")]),
 prob("For the line \\(y = x + 8\\), find \\(y\\) when \\(x = 0\\).",8,
      "Put x = 0 into the equation and keep the + 8.",
      walk_sub_y(1,8,0),
      [misc("dropped_intercept","When x = 0, y = 0 + 8 = 8. Writing 0 forgets the + 8, which is the y-intercept.",0,"ignores the +8")]),
]

silver=[
 prob("The graph shows a straight line. What is the gradient of this line?",3,
      "Pick two points the line passes through cleanly, then use rise over run.",
      walk_graph_grad(0,2,2,8),
      [misc("forgot_to_divide","Pick (0, 2) and (2, 8). Rise = 6, Run = 2. Gradient = 6 ÷ 2 = 3. Stopping at the rise gives 6.",6,"stops at rise")],
      chart={"data":{"datasets":[{"data":[{"x":0,"y":2},{"x":1,"y":5},{"x":2,"y":8},{"x":3,"y":11},{"x":4,"y":14}],"fill":False,"type":"line","tension":0,"borderColor":"#3b82f6","pointRadius":5,"pointBackgroundColor":"#3b82f6"}]},"type":"scatter","options":{"scales":{"x":{"max":5,"min":-1,"grid":{"color":"rgba(0,0,0,0.05)"},"ticks":{"stepSize":1},"title":{"text":"x","display":True}},"y":{"max":16,"min":-1,"grid":{"color":"rgba(0,0,0,0.08)"},"ticks":{"stepSize":2},"title":{"text":"y","display":True}}}}}),
 prob("The graph shows a straight line. What is the y-intercept?",1,
      "Find where the line crosses the y-axis, at x = 0.",
      walk_graph_yint(1,5,2,9,4),
      [misc("read_gradient_not_intercept","The y-intercept is where the line meets the y-axis, at x = 0, which is y = 1. Reading the gradient (4) instead is the mix-up.",4,"gives gradient not intercept")],
      chart={"data":{"datasets":[{"data":[{"x":-2,"y":-7},{"x":-1,"y":-3},{"x":0,"y":1},{"x":1,"y":5},{"x":2,"y":9},{"x":3,"y":13}],"fill":False,"type":"line","tension":0,"borderColor":"#ef4444","pointRadius":5,"pointBackgroundColor":"#ef4444"}]},"type":"scatter","options":{"scales":{"x":{"max":4,"min":-3,"grid":{"color":"rgba(0,0,0,0.05)"},"ticks":{"stepSize":1},"title":{"text":"x","display":True}},"y":{"max":15,"min":-8,"grid":{"color":"rgba(0,0,0,0.08)"},"ticks":{"stepSize":2},"title":{"text":"y","display":True}}}}}),
 prob("The graph shows \\(y = -2x + 10\\). What is \\(y\\) when \\(x = 3\\)?",4,
      "Substitute x = 3, keeping the negative gradient, or read it off the line.",
      walk_graph_read_sub(-2,10,3),
      [misc("sign_error","−2 × 3 = −6, then −6 + 10 = 4. Treating −2 × 3 as +6 gives 16.",16,"+6 instead of -6")],
      chart={"data":{"datasets":[{"data":[{"x":0,"y":10},{"x":1,"y":8},{"x":2,"y":6},{"x":3,"y":4},{"x":4,"y":2},{"x":5,"y":0}],"fill":False,"type":"line","tension":0,"borderColor":"#22c55e","pointRadius":5,"pointBackgroundColor":"#22c55e"}]},"type":"scatter","options":{"scales":{"x":{"max":6,"min":-1,"grid":{"color":"rgba(0,0,0,0.05)"},"ticks":{"stepSize":1},"title":{"text":"x","display":True}},"y":{"max":12,"min":-1,"grid":{"color":"rgba(0,0,0,0.08)"},"ticks":{"stepSize":2},"title":{"text":"y","display":True}}}}}),
 prob("The line \\(y = \\frac{1}{3}x + 2\\) passes through \\((9, k)\\). Find \\(k\\).",5,
      "A gradient of one third means divide the x-value by 3, then add 2.",
      walk_sub_third(9),
      [misc("dropped_intercept","⅓ × 9 = 3, then add 2 to get 5. Stopping at 3 forgets the + 2.",3,"omits +2")]),
 prob("A line goes through \\((1, 2)\\) and \\((3, 14)\\). What is the gradient?",6,
      "Rise over run: divide the change in y by the change in x.",
      walk_grad_points(1,2,3,14),
      [misc("forgot_to_divide","Rise = 14 − 2 = 12, Run = 3 − 1 = 2. Gradient = 12 ÷ 2 = 6. Stopping at the rise gives 12.",12,"stops at rise")]),
 prob("A line has equation \\(y = -4x + 3\\). Find \\(y\\) when \\(x = 2\\).",-5,
      "Multiply −4 by 2, keeping the sign, then add 3.",
      walk_sub_y(-4,3,2),
      [misc("sign_error","−4 × 2 = −8, then −8 + 3 = −5. Treating −4 × 2 as +8 gives 11.",11,"+8 instead of -8")]),
 prob("Find the gradient of the line through \\((-1, 4)\\) and \\((3, 12)\\).",2,
      "Careful with the run: subtracting a negative x adds.",
      walk_grad_points(-1,4,3,12),
      [misc("negative_run_slip","Run = 3 − (−1) = 4, not 3 − 1 = 2. Subtracting a negative adds. Rise = 8, so gradient = 8 ÷ 4 = 2.",4,"run taken as 2 gives 8/2=4")]),
]

gold=[
 prob("Find the gradient of the line through \\((-4, -7)\\) and \\((2, 5)\\).",2,
      "Both coordinates change sign; subtracting negatives adds.",
      walk_grad_points(-4,-7,2,5),
      [misc("negative_run_slip","Run = 2 − (−4) = 6, not 2 − 4 = −2. Subtracting a negative adds. Rise = 12, so gradient = 12 ÷ 6 = 2.",-6,"run taken as -2 gives 12/-2=-6")]),
 prob("A line passes through \\((3, 5)\\) and \\((9, 17)\\). Write the equation in the form \\(y = mx + c\\). What is \\(c\\)?",-1,
      "Find the gradient first, then substitute one point to find c.",
      walk_find_c(3,5,9,17),
      [misc("sign_error","From 5 = 2 × 3 + c: c = 5 − 6 = −1. Adding instead (5 + 6) gives 11.",11,"adds mx instead of subtracting")]),
 prob("The line \\(y = mx + 7\\) passes through \\((2, 15)\\). Find \\(m\\).",4,
      "Substitute the point, take 7 off both sides, then divide by 2.",
      walk_find_m_from_point(4,7,2,15),
      [misc("forgot_to_divide","15 = 2m + 7, so 2m = 8 and m = 4. Writing 8 stops before dividing by 2.",8,"stops at 2m=8")]),
 prob("Two points on a line are \\((-3, 8)\\) and \\((5, -4)\\). What is the gradient?",-1.5,
      "The line falls, so the gradient is negative; use rise over run carefully.",
      walk_grad_points(-3,8,5,-4),
      [misc("sign_error","Rise = −4 − 8 = −12, Run = 5 − (−3) = 8, so gradient = −12 ÷ 8 = −1.5. Dropping the minus gives 1.5, but the line slopes down.",1.5,"drops the sign")]),
 prob("A line has equation \\(3y = 9x - 12\\). What is the gradient?",3,
      "Divide every term by 3 to reach y = mx + c first.",
      walk_rearrange_grad(9,3,-12),
      [misc("forgot_step","Divide every term by 3 first: y = 3x − 4. The gradient is 3, not 9.",9,"reads 9 without dividing")]),
]

# ---------- opener ----------
opener={
 "display": svg_savings() + "<p>Each week Sam adds the same amount to a savings jar. The graph shows the total (in £) week by week.</p>",
 "steps":[
   box("How much money was already in the jar at the start (week 0)? £", 5, "Read the height of the line where it meets week 0."),
   box("Each week the total climbs by the same step. From week 0 (£5) to week 1 (£8) it goes up by £", 3, "How much taller is the line one week along?"),
   sayonly("That steady £3 a week jump is the line's <strong>gradient</strong>, and the £5 it started with is the <strong>y-intercept</strong>. In symbols the line is \\(y = 3x + 5\\). Finding \"how much per step\" is exactly what gradient measures."),
 ]
}

# ---------- teach walks ----------
teach={
 "bronze":{
   "display":"A line passes through \\((2, 1)\\) and \\((6, 9)\\). Find its gradient.",
   "steps":[
     sayonly("Gradient is rise over run. Find each piece, then divide."),
     box("Rise = 9 − 1 = ", 8, "Second y minus first y."),
     box("Run = 6 − 2 = ", 4, "Second x minus first x."),
     box("Gradient = rise ÷ run = 8 ÷ 4 = ", 2, "Divide the rise by the run."),
     box("Check: 2 × 4 = ", 8, "Gradient times run should return the rise.", done="It gives the rise back, so the gradient is 2."),
   ]
 },
 "silver":{
   "display": svg_line([(0,-1),(1,1),(2,3),(3,5)], -1,4,-3,6, "Straight line through the points 0 comma minus 1, 1 comma 1, 2 comma 3 and 3 comma 5") + "<p>The graph shows a straight line. Find its gradient.</p>",
   "steps":[
     sayonly("Read two clean points off the line, then use rise over run."),
     box("At x = 0 the line is at y = ", -1, "Where does it cross the y-axis?"),
     box("At x = 2 the line is at y = ", 3, "Trace up from x = 2 to the line."),
     box("Rise = 3 − (−1) = ", 4, "Subtracting a negative adds."),
     box("Run = 2 − 0 = ", 2, "Difference in the x values."),
     box("Gradient = 4 ÷ 2 = ", 2, "Divide rise by run.", done="The line climbs 2 for every 1 across, so the gradient is 2."),
   ]
 },
 "gold":{
   "display":"A line passes through \\((2, 7)\\) and \\((6, 19)\\). Find \\(c\\) in \\(y = mx + c\\).",
   "steps":[
     sayonly("Find the gradient, then feed a point back in to reach c."),
     box("Rise = 19 − 7 = ", 12, "Second y minus first y."),
     box("Run = 6 − 2 = ", 4, "Second x minus first x."),
     box("Gradient m = 12 ÷ 4 = ", 3, "Divide rise by run."),
     box("Use (2, 7): the mx part is 3 × 2 = ", 6, "Multiply gradient by that x."),
     box("So 7 = 6 + c, giving c = 7 − 6 = ", 1, "Take the mx part off the y-value.", done="c = 1, so the line is y = 3x + 1."),
   ]
 }
}

# ---------- tier guides ----------
tier_guides={
 "bronze":{
   "title":"Bronze: reading m and c",
   "steps":[
     "In \\(y = mx + c\\), the <strong>gradient</strong> is m (the number in front of x) and the <strong>y-intercept</strong> is c (the number on its own).",
     "For a gradient from two points, work out <strong>rise ÷ run</strong>: the change in y over the change in x.",
     "To find y at a value of x, substitute it in and multiply before you add."
   ],
   "example":{
     "question":"Find the gradient of the line through (1, 4) and (3, 10).",
     "steps":[
       {"label":"Rise","content":"10 − 4 = 6"},
       {"label":"Run","content":"3 − 1 = 2"},
       {"label":"Check","content":"Rise over run = 6 ÷ 2"},
       {"label":"Gradient","content":"m = 3","isAnswer":True,"is_answer":True},
     ]
   }
 },
 "silver":{
   "title":"Silver: graphs and negatives",
   "steps":[
     "To read a gradient off a graph, pick two points the line passes through cleanly and use <strong>rise ÷ run</strong>.",
     "The <strong>y-intercept</strong> is the height where the line crosses the y-axis (x = 0).",
     "When the gradient is negative or a fraction, keep the sign through every step and multiply before adding."
   ],
   "example":{
     "question":"For y = −3x + 8, find y when x = 2.",
     "steps":[
       {"label":"Gradient part","content":"−3 × 2 = −6"},
       {"label":"Add intercept","content":"−6 + 8"},
       {"label":"Check","content":"Point (2, 2) sits on the line"},
       {"label":"Answer","content":"y = 2","isAnswer":True,"is_answer":True},
     ]
   }
 },
 "gold":{
   "title":"Gold: finding the equation",
   "steps":[
     "With negative coordinates, remember that subtracting a negative <strong>adds</strong> when finding rise or run.",
     "To find c, work out the gradient first, then substitute one point into \\(y = mx + c\\) and solve for c.",
     "If an equation is not yet \\(y = mx + c\\), divide every term to rearrange it before reading the gradient."
   ],
   "example":{
     "question":"A line through (1, 5) and (4, 14). Find c.",
     "steps":[
       {"label":"Gradient","content":"(14 − 5) ÷ (4 − 1) = 3"},
       {"label":"Use (1, 5)","content":"5 = 3 × 1 + c"},
       {"label":"Check","content":"3 × 1 = 3, so 5 = 3 + c"},
       {"label":"Intercept","content":"c = 2","isAnswer":True,"is_answer":True},
     ]
   }
 }
}

# ---------- method card ----------
method_card={
 "title":"How to Plot and Read Linear Graphs",
 "steps":[
   "Read m and c straight from \\(y = mx + c\\): m is the gradient, c is the y-intercept.",
   "Gradient between two points is rise ÷ run, with the change in y on top.",
   "To plot, substitute three x-values, plot the pairs, and join them with a ruler.",
   "To find c from a point, put the point and gradient into \\(y = mx + c\\) and solve."
 ],
 "content":"<p>A <strong>linear graph</strong> is a straight line \\(y = mx + c\\), where \\(m\\) is the <strong>gradient</strong> (steepness) and \\(c\\) is the <strong>y-intercept</strong> (where it crosses the y-axis).</p><p>The gradient is the rise divided by the run: \\(m = \\frac{y_2 - y_1}{x_2 - x_1}\\), keeping the vertical change on top. A positive gradient slopes up, a negative one slopes down.</p><p>To read a value, trace from the known axis to the line, then across to the other axis.</p>",
 "example":"<p><strong>Plot \\(y = 3x - 2\\).</strong> At \\(x = 0, 1, 2\\) the y-values are \\(-2, 1, 4\\), giving points \\((0,-2), (1,1), (2,4)\\). Join them with a ruler. Gradient \\(= \\frac{4 - (-2)}{2 - 0} = 3\\) ✔</p>"
}

# ---------- assemble ----------
pd=json.load(io.open("_my_pre.json",encoding="utf-8"))
pd["method_card"]=method_card
pd["problem_bank"]={
  "bronze":bronze,"silver":silver,"gold":gold,
  "bronze_description":"Read the gradient or intercept straight from y = mx + c, or find a gradient from two friendly points.",
  "silver_description":"Read gradients and intercepts off a drawn graph, and substitute into equations with negatives or fractions.",
  "gold_description":"Work backwards from negative coordinates to a gradient, then to the full equation and its intercept c.",
}
pd["tier_guides"]=tier_guides
pd["guided"]={"opener":opener,"teach":teach}
# preserve related_videos, worked_examples, topic_links (already in pd)

json.dump(pd, io.open("lesson_graphs-L01.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_graphs-L01.json")
