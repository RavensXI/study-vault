# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for maths-aqa graphs-L08."""
import json, io

MINUS = "−"  # unicode minus
TIMES = "×"
DIV = "÷"

# ---------------------------------------------------------------- SVG helpers
def st_graph(pts, xmax, ymax, xticks, yticks, xlabel, ylabel, aria, caption,
             fill="#60a5fa", annots=None):
    """Speed/distance-time style axis plot. pts in data coords (closed polygon)."""
    X0, X1 = 44.0, 240.0
    Y0, Y1 = 155.0, 20.0  # baseline, top
    def px(x): return X0 + (x / xmax) * (X1 - X0)
    def py(y): return Y0 + (y / ymax) * (Y1 - Y0)
    s = [f'<svg viewBox="0 0 262 195" role="img" aria-label="{aria}" '
         f'style="max-width:262px" font-family="Inter, sans-serif">']
    # axes
    s.append(f'<line x1="{X0}" y1="15" x2="{X0}" y2="{Y0}" stroke="currentColor" stroke-width="1.2"/>')
    s.append(f'<line x1="{X0}" y1="{Y0}" x2="{X1+3}" y2="{Y0}" stroke="currentColor" stroke-width="1.2"/>')
    # y ticks
    for v in yticks:
        yy = py(v)
        s.append(f'<line x1="{X0-3}" y1="{yy:.1f}" x2="{X0}" y2="{yy:.1f}" stroke="currentColor" stroke-width="1"/>')
        s.append(f'<text x="{X0-6}" y="{yy+3:.1f}" font-size="9" fill="currentColor" text-anchor="end">{v}</text>')
    # x ticks
    for v in xticks:
        xx = px(v)
        s.append(f'<line x1="{xx:.1f}" y1="{Y0}" x2="{xx:.1f}" y2="{Y0+3}" stroke="currentColor" stroke-width="1"/>')
        s.append(f'<text x="{xx:.1f}" y="{Y0+13:.1f}" font-size="9" fill="currentColor" text-anchor="middle">{v}</text>')
    # axis labels
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="184" font-size="9" fill="currentColor" text-anchor="middle">{xlabel}</text>')
    s.append(f'<text x="13" y="{(Y0+Y1)/2:.0f}" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 13 {(Y0+Y1)/2:.0f})">{ylabel}</text>')
    # polygon (region)
    poly = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in pts)
    s.append(f'<polygon points="{poly}" fill="{fill}" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>')
    if annots:
        for (ax, ay, txt, anchor) in annots:
            s.append(f'<text x="{px(ax):.1f}" y="{py(ay):.1f}" font-size="9.5" fill="currentColor" text-anchor="{anchor}">{txt}</text>')
    s.append('</svg>')
    if caption:
        s.append(f'<span class="figure-caption">{caption}</span>')
    return "".join(s)

def chart_curve_area(xs, ys, fill="#60a5fa", border="#3b82f6", xmin=None, xmax=None,
                     ymin=0, ymax=None, tension=0.35):
    """Chart.js line-through-points with filled area under (trapezium rule visual)."""
    pts = [{"x": x, "y": y} for x, y in zip(xs, ys)]
    if xmin is None: xmin = min(xs)
    if xmax is None: xmax = max(xs)
    if ymax is None: ymax = max(ys) + 1
    return {
        "type": "scatter",
        "data": {"datasets": [{
            "type": "line", "data": pts, "tension": tension, "fill": "origin",
            "borderColor": border, "backgroundColor": "rgba(96,165,250,0.25)",
            "pointRadius": 4, "pointBackgroundColor": border
        }]},
        "options": {"plugins": {"legend": {"display": False}}, "scales": {
            "x": {"min": xmin, "max": xmax, "ticks": {"stepSize": 1},
                  "grid": {"color": "rgba(128,128,128,0.15)"}, "title": {"text": "x", "display": True}},
            "y": {"min": ymin, "max": ymax,
                  "grid": {"color": "rgba(128,128,128,0.15)"}, "title": {"text": "y", "display": True}}}}
    }

def chart_curve_tangent(fx, x_lo, x_hi, tp1, tp2, tangent_x, curve_label,
                        cmin, cmax, ymin, ymax):
    """Chart.js: a curve fx over [x_lo,x_hi] plus a straight tangent through tp1,tp2."""
    n = 41
    curve = [{"x": round(x_lo + (x_hi - x_lo) * i / (n - 1), 3),
              "y": round(fx(x_lo + (x_hi - x_lo) * i / (n - 1)), 3)} for i in range(n)]
    (x1, y1), (x2, y2) = tp1, tp2
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    line = [{"x": cmin, "y": round(m * cmin + c, 3)}, {"x": cmax, "y": round(m * cmax + c, 3)}]
    tpt = [{"x": tangent_x, "y": round(fx(tangent_x), 3)}]
    return {
        "type": "scatter",
        "data": {"datasets": [
            {"type": "line", "data": curve, "tension": 0.35, "fill": False,
             "borderColor": "#3b82f6", "pointRadius": 0, "label": curve_label},
            {"type": "line", "data": line, "tension": 0, "fill": False,
             "borderColor": "#f59e0b", "borderDash": [6, 4], "pointRadius": 0, "label": "tangent"},
            {"type": "scatter", "data": tpt, "pointRadius": 5, "pointBackgroundColor": "#f59e0b",
             "borderColor": "#f59e0b", "label": "point"}
        ]},
        "options": {"plugins": {"legend": {"display": True}}, "scales": {
            "x": {"min": cmin, "max": cmax, "ticks": {"stepSize": 1},
                  "grid": {"color": "rgba(128,128,128,0.15)"}, "title": {"text": "x", "display": True}},
            "y": {"min": ymin, "max": ymax,
                  "grid": {"color": "rgba(128,128,128,0.15)"}, "title": {"text": "y", "display": True}}}}
    }

# ------------------------------------------------------- guided-step builders
def grad_steps(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    rise = y2 - y1
    run = x2 - x1
    g = rise / run
    g = int(g) if g == int(g) else g
    check = y1 + g * run
    return [
        {"say": "Gradient of a straight tangent = rise " + DIV + " run. First the rise (the change in y), then the run (the change in x)."},
        {"pre": f"rise: {y2} {MINUS} ({y1}) = " if y1 < 0 else f"rise: {y2} {MINUS} {y1} = ",
         "post": "", "answer": rise, "hint": "Second y take away the first y."},
        {"pre": f"run: {x2} {MINUS} {x1} = ", "post": "", "answer": run,
         "hint": "Second x take away the first x."},
        {"say": "Now divide the rise by the run.", "phase": "substitute",
         "pre": f"gradient: {rise} {DIV} {run} = ", "post": "", "answer": g,
         "hint": "Rise on top, run underneath."},
        {"phase": "substitute",
         "pre": f"check, from ({x1}, {y1}) go across {run} and up gradient{TIMES}run: {y1} + ({g}){TIMES}{run} = ",
         "post": "", "answer": check,
         "done": f"It lands on ({x2}, {y2}), so the gradient is {g}.",
         "hint": "Add the rise back on; you should reach the second point's y."}
    ], g

def trap_steps(ys, h, derive_h_from=None):
    """derive_h_from = (span, strips) to add an h-derivation box first."""
    middles = ys[1:-1]
    ms = sum(middles)
    dbl = 2 * ms
    ends = ys[0] + ys[-1]
    bracket = ends + dbl
    halfh = h / 2
    A = halfh * bracket
    def num(v): return int(v) if float(v) == int(v) else v
    ms_expr = " + ".join(str(num(m)) for m in middles)
    steps = [{"say": "Trapezium rule: A = (h " + DIV + " 2) " + TIMES + " [first + last + 2 " + TIMES + " (all the middle values)]."}]
    if derive_h_from:
        span, strips = derive_h_from
        steps.append({"pre": f"strip width h = span {DIV} strips = {span} {DIV} {strips} = ",
                      "post": "", "answer": num(h), "hint": "Total width divided by the number of strips."})
    steps += [
        {"pre": f"add the middle values: {ms_expr} = ", "post": "", "answer": num(ms),
         "hint": "Every y-value except the first and last."},
        {"pre": f"double them: 2 {TIMES} {num(ms)} = ", "post": "", "answer": num(dbl),
         "hint": "The inside values all count twice."},
        {"pre": f"first + last: {num(ys[0])} + {num(ys[-1])} = ", "post": "", "answer": num(ends),
         "hint": "Only the two end values, each once."},
        {"pre": f"bracket total: {num(ends)} + {num(dbl)} = ", "post": "", "answer": num(bracket),
         "hint": "Add the ends to the doubled middles."},
        {"say": "Now multiply by h " + DIV + " 2 to finish.", "phase": "substitute",
         "pre": f"h {DIV} 2 = {num(h)} {DIV} 2 = ", "post": "", "answer": num(halfh),
         "hint": "Half the strip width."},
        {"phase": "substitute",
         "pre": f"A = {num(halfh)} {TIMES} {num(bracket)} = ", "post": "", "answer": num(A),
         "done": f"The estimated area is {num(A)}.",
         "hint": "Multiply the half-width by the bracket."}
    ]
    return steps, num(A), dict(ms=num(ms), dbl=num(dbl), ends=num(ends), bracket=num(bracket),
                               halfh=num(halfh), A=num(A))

def tri_area_steps(base, height, context=None, unit=""):
    prod = base * height
    A = prod / 2
    A = int(A) if A == int(A) else A
    lead = ("Distance = area under the speed-time graph. This is a triangle: " if context
            else "Area of a triangle = ") + "½ " + TIMES + " base " + TIMES + " height."
    return [
        {"say": lead},
        {"pre": f"base {TIMES} height: {base} {TIMES} {height} = ", "post": "", "answer": prod,
         "hint": "Multiply the two lengths first."},
        {"say": "A triangle is half of that rectangle.", "phase": "substitute",
         "pre": f"½ {TIMES} {prod} = ", "post": "", "answer": A,
         "hint": "Halve it."},
        {"phase": "substitute",
         "pre": f"check by doubling: 2 {TIMES} {A} = ", "post": "", "answer": prod,
         "done": f"Doubling returns base {TIMES} height, so the area is {A}{unit}.",
         "hint": "Twice the area should give base times height."}
    ], A

# ================================================================ BUILD
P = {}  # problem_bank

# ---- BRONZE ----
bronze = []

# b0 gradient (1,3)-(5,11) -> 2  (completion problem: boundary matters)
gs, g = grad_steps((1, 3), (5, 11)); assert g == 2
bronze.append({
    "display": "A tangent to a curve passes through \\((1, 3)\\) and \\((5, 11)\\). What is the gradient of the tangent?",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Gradient is rise over run: (change in y) divided by (change in x).",
    "misconceptions": [
        {"pattern": "swap_rise_run",
         "message": "You have divided the run by the rise. Gradient is rise " + DIV + " run, so (change in y) on top: (11 " + MINUS + " 3) " + DIV + " (5 " + MINUS + " 1) = 8 " + DIV + " 4 = 2.",
         "expect": [0.5], "note": "run/rise = 4/8 = 0.5"}],
    "guided_steps": gs})

# b1 gradient (2,10)-(6,2) -> -2
gs, g = grad_steps((2, 10), (6, 2)); assert g == -2
bronze.append({
    "display": "A tangent passes through \\((2, 10)\\) and \\((6, 2)\\). Find the gradient.",
    "solutions": [-2], "calculator": False, "input_type": "single_value",
    "hint": "The line falls, so expect a negative gradient. rise is second y minus first y.",
    "misconceptions": [
        {"pattern": "lost_sign",
         "message": "The line goes down as x increases, so the gradient is negative. rise = 2 " + MINUS + " 10 = " + MINUS + "8, and " + MINUS + "8 " + DIV + " 4 = " + MINUS + "2.",
         "expect": [2], "note": "ignoring the sign gives 8/4 = 2"}],
    "guided_steps": gs})

# b2 triangle base6 height8 -> 24 (figure)
gs, A = tri_area_steps(6, 8); assert A == 24
tri_svg = ('<svg viewBox="0 0 210 170" role="img" '
           'aria-label="Right-angled triangle with base 6 and perpendicular height 8" '
           'style="max-width:210px" font-family="Inter, sans-serif">'
           '<polygon points="34,140 190,140 34,32" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>'
           '<rect x="34" y="126" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1"/>'
           '<text x="112" y="157" font-size="11" fill="currentColor" text-anchor="middle">base = 6</text>'
           '<text x="20" y="88" font-size="11" fill="currentColor" text-anchor="middle" transform="rotate(-90 20 88)">height = 8</text>'
           '</svg><span class="figure-caption">Diagram not drawn accurately</span>')
bronze.append({
    "display": tri_svg + "Estimate the area of a triangle with base 6 and height 8.",
    "solutions": [24], "calculator": False, "input_type": "single_value",
    "hint": "Area of a triangle is half the base times the height.",
    "misconceptions": [
        {"pattern": "forgot_half",
         "message": "That is base " + TIMES + " height, which is the whole rectangle. A triangle is half of it: ½ " + TIMES + " 6 " + TIMES + " 8 = 24.",
         "expect": [48], "note": "6*8 = 48 without the half"}],
    "guided_steps": gs})

# b3 trapezium 4,10 height3 -> 21 (figure)
prod_add = (4 + 10)
gs = [
    {"say": "Area of a trapezium = ½ " + TIMES + " (sum of the parallel sides) " + TIMES + " height."},
    {"pre": "sum of the parallel sides: 4 + 10 = ", "post": "", "answer": 14,
     "hint": "Add the two parallel sides."},
    {"pre": f"{TIMES} height: 14 {TIMES} 3 = ", "post": "", "answer": 42,
     "hint": "Multiply the sum by the height."},
    {"say": "Now halve it.", "phase": "substitute",
     "pre": f"½ {TIMES} 42 = ", "post": "", "answer": 21, "hint": "Take half."},
    {"phase": "substitute", "pre": f"check by doubling: 2 {TIMES} 21 = ", "post": "", "answer": 42,
     "done": "Doubling returns (sum of sides) " + TIMES + " height, so the area is 21.",
     "hint": "Twice the area should give 42."}]
trap_svg = ('<svg viewBox="0 0 230 160" role="img" '
            'aria-label="Trapezium with parallel sides 4 (top) and 10 (bottom) and height 3" '
            'style="max-width:230px" font-family="Inter, sans-serif">'
            '<polygon points="22,124 208,124 160,40 70,40" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>'
            '<text x="115" y="142" font-size="11" fill="currentColor" text-anchor="middle">10</text>'
            '<text x="115" y="33" font-size="11" fill="currentColor" text-anchor="middle">4</text>'
            '<text x="14" y="84" font-size="11" fill="currentColor" text-anchor="middle" transform="rotate(-90 14 84)">height = 3</text>'
            '</svg><span class="figure-caption">Diagram not drawn accurately</span>')
bronze.append({
    "display": trap_svg + "Estimate the area of a trapezium with parallel sides 4 and 10 and height 3.",
    "solutions": [21], "calculator": False, "input_type": "single_value",
    "hint": "Add the parallel sides, multiply by the height, then halve.",
    "misconceptions": [
        {"pattern": "forgot_half",
         "message": "You have found (sum of sides) " + TIMES + " height. The trapezium is half of that: ½ " + TIMES + " 14 " + TIMES + " 3 = 21.",
         "expect": [42], "note": "14*3 = 42 without the half"}],
    "guided_steps": gs})

# b4 rectangle speed-time 5s x 12 -> 60 (figure)
rect_svg = st_graph([(0, 0), (5, 0), (5, 12), (0, 12)], xmax=6, ymax=14,
                    xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 4, 8, 12],
                    xlabel="time (s)", ylabel="speed (m/s)",
                    aria="Speed-time graph: a rectangle of width 5 seconds and height 12 metres per second",
                    caption="Area under speed-time = distance",
                    annots=[(2.5, -1.6, "5 s", "middle"), (5.3, 6, "12 m/s", "start")])
gs = [
    {"say": "On a speed-time graph the distance is the area of the shape. This is a rectangle: width " + TIMES + " height."},
    {"pre": "width in seconds: read it off = ", "post": "", "answer": 5,
     "hint": "The base of the rectangle."},
    {"pre": "height in m/s: read it off = ", "post": "", "answer": 12,
     "hint": "The height of the rectangle."},
    {"say": "Multiply width by height for the area.", "phase": "substitute",
     "pre": f"area: 5 {TIMES} 12 = ", "post": "", "answer": 60,
     "hint": "Base times height."},
    {"phase": "substitute", "pre": f"check the speed back: 60 {DIV} 5 = ", "post": "", "answer": 12,
     "done": "Distance " + DIV + " time returns the steady speed 12 m/s, so the distance is 60 m.",
     "hint": "Distance divided by time gives the speed."}]
bronze.append({
    "display": rect_svg + "A rectangle on a speed-time graph has width 5 s and height 12 m/s. What area (distance) does it represent?",
    "solutions": [60], "calculator": False, "input_type": "single_value",
    "hint": "Area of the rectangle is width times height, and that area is the distance.",
    "misconceptions": [
        {"pattern": "added_not_multiplied",
         "message": "Add is not the operation here. Area = width " + TIMES + " height = 5 " + TIMES + " 12 = 60 m.",
         "expect": [17], "note": "5+12 = 17"}],
    "guided_steps": gs})

# b5 MC: distance-time gradient 15 -> instantaneous speed
bronze.append({
    "display": "A tangent at a point on a distance-time graph has gradient 15. What does this represent?",
    "options": ["Instantaneous speed of 15 units/s", "Acceleration of 15", "Distance of 15", "Average speed of 15"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "On a distance-time graph, gradient tells you speed; at a single point it is the speed right then.",
    "misconceptions": [
        {"pattern": "grad_is_accel",
         "message": "Acceleration comes from a speed-time graph. On a distance-time graph the gradient is speed, and at one point it is the instantaneous speed.",
         "expect": [1], "note": "confusing distance-time gradient with acceleration"}]})

# b6 triangle speed-time base10 height20 -> 100 (figure)
gs, A = tri_area_steps(10, 20, context=True, unit=" m"); assert A == 100
tri_st_svg = st_graph([(0, 0), (10, 0), (10, 20)], xmax=12, ymax=24,
                      xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 5, 10, 15, 20],
                      xlabel="time (s)", ylabel="speed (m/s)",
                      aria="Speed-time graph: a triangle with base 10 seconds and height 20 metres per second",
                      caption="Area under speed-time = distance",
                      annots=[(5, -1.6, "10 s", "middle"), (10.4, 11, "20 m/s", "start")])
bronze.append({
    "display": tri_st_svg + "On a speed-time graph, a triangular area has base 10 s and height 20 m/s. What distance does it represent?",
    "solutions": [100], "calculator": False, "input_type": "single_value",
    "hint": "The distance is the triangle's area: half the base times the height.",
    "misconceptions": [
        {"pattern": "forgot_half",
         "message": "That is base " + TIMES + " height, the full rectangle. The triangle is half: ½ " + TIMES + " 10 " + TIMES + " 20 = 100 m.",
         "expect": [200], "note": "10*20 = 200 without the half"}],
    "guided_steps": gs})

# b7 gradient (1,2)-(3,12) -> 5  (distinct from b0=2)
gs, g = grad_steps((1, 2), (3, 12)); assert g == 5
bronze.append({
    "display": "A tangent to a curve at \\(x = 2\\) passes through \\((1, 2)\\) and \\((3, 12)\\). What is the gradient at \\(x = 2\\)?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Use the two points on the tangent: rise over run.",
    "misconceptions": [
        {"pattern": "swap_rise_run",
         "message": "Rise goes on top: (12 " + MINUS + " 2) " + DIV + " (3 " + MINUS + " 1) = 10 " + DIV + " 2 = 5. You have divided run by rise.",
         "expect": [0.2], "note": "2/10 = 0.2"}],
    "guided_steps": gs})

P["bronze"] = bronze
P["bronze_description"] = "One step: read a gradient as rise over run, or find the area of a single simple shape."

# ---- SILVER ----
silver = []

# s0 trap rule h=2 ys 0,4,12,24 -> 56  (completion problem)
gs, A, aux = trap_steps([0, 4, 12, 24], 2); assert A == 56
s0_chart = chart_curve_area([0, 2, 4, 6], [0, 4, 12, 24], ymax=26)
silver.append({
    "display": "Use the trapezium rule with 3 strips (\\(h = 2\\)) and y-values 0, 4, 12, 24 to estimate the area.",
    "solutions": [56], "calculator": False, "input_type": "single_value",
    "hint": "Double the middle values, add the ends, then multiply by h over 2.",
    "chart": s0_chart,
    "misconceptions": [
        {"pattern": "no_half",
         "message": "You have left out the ½ in h " + DIV + " 2. Multiply the bracket by h " + DIV + " 2 = 1, not by h = 2. The answer is 56, not 112.",
         "expect": [112], "note": "h*bracket = 2*56 = 112"},
        {"pattern": "middles_not_doubled",
         "message": "The middle values 4 and 12 must be doubled. With them counted once you get (2 " + DIV + " 2)(0 + 24 + 16) = 40; doubled it is 56.",
         "expect": [40], "note": "(h/2)(ends+ms) = 1*(24+16) = 40"}],
    "guided_steps": gs})

# s1 trap rule h=1 ys 1,4,9,16 -> 21.5
gs, A, aux = trap_steps([1, 4, 9, 16], 1); assert A == 21.5
s1_chart = chart_curve_area([0, 1, 2, 3], [1, 4, 9, 16], ymax=18)
silver.append({
    "display": "Use the trapezium rule with \\(h = 1\\), y-values: 1, 4, 9, 16. Estimate the area.",
    "solutions": [21.5], "calculator": False, "input_type": "single_value",
    "hint": "Ends 1 and 16, middles 4 and 9 doubled, all times h over 2.",
    "chart": s1_chart,
    "misconceptions": [
        {"pattern": "no_half",
         "message": "Do not forget the ½. h " + DIV + " 2 = 0.5, so A = 0.5 " + TIMES + " 43 = 21.5, not 43.",
         "expect": [43], "note": "h*bracket = 1*43 = 43"},
        {"pattern": "middles_not_doubled",
         "message": "Double the middles 4 and 9. Counting them once gives 0.5(1 + 16 + 13) = 15; doubled it is 21.5.",
         "expect": [15], "note": "0.5*(17+13) = 15"}],
    "guided_steps": gs})

# s2 composite speed-time -> 150 (figure)
gs = [
    {"say": "Split the journey into a triangle, a rectangle, then a triangle, and add the areas."},
    {"pre": f"speeding up, t = 0 to 5: ½ {TIMES} 5 {TIMES} 10 = ", "post": "", "answer": 25,
     "hint": "Triangle: half base times height."},
    {"pre": f"steady, t = 5 to 15: 10 {TIMES} 10 = ", "post": "", "answer": 100,
     "hint": "Rectangle: width times height."},
    {"pre": f"slowing down, t = 15 to 20: ½ {TIMES} 5 {TIMES} 10 = ", "post": "", "answer": 25,
     "hint": "Triangle: half base times height."},
    {"say": "Add the three pieces for the total distance.", "phase": "substitute",
     "pre": "total: 25 + 100 + 25 = ", "post": "", "answer": 150,
     "hint": "Sum the three areas."},
    {"phase": "substitute",
     "pre": f"check as one trapezium: ½ {TIMES} (10 + 20) {TIMES} 10 = ", "post": "", "answer": 150,
     "done": "Half the sum of the parallel sides times the height gives 150 m too.",
     "hint": "Parallel sides 10 (top) and 20 (bottom), height 10."}]
comp_svg = st_graph([(0, 0), (5, 10), (15, 10), (20, 0)], xmax=22, ymax=13,
                    xticks=[0, 5, 10, 15, 20], yticks=[0, 5, 10],
                    xlabel="time (s)", ylabel="speed (m/s)",
                    aria="Speed-time graph rising from 0 to 10 by t=5, steady 10 until t=15, then falling to 0 at t=20",
                    caption="Area = total distance",
                    annots=[(10, 11.8, "10 m/s", "middle")])
silver.append({
    "display": comp_svg + "A speed-time graph shows: speed 0 at t=0, speed 10 at t=5, speed 10 at t=15, speed 0 at t=20. Estimate the total distance.",
    "solutions": [150], "calculator": False, "input_type": "single_value",
    "hint": "Break it into triangle, rectangle, triangle and add the areas.",
    "misconceptions": [
        {"pattern": "forgot_rectangle",
         "message": "Do not miss the middle rectangle, where the speed stays at 10 for 10 s (area 100). The two end triangles alone give only 50; the total is 150 m.",
         "expect": [50], "note": "25+25 = 50, rectangle dropped"}],
    "guided_steps": gs})

# s3 gradient (0,-4)-(3,8) on y=x^2 -> 4 (figure)
gs, g = grad_steps((0, -4), (3, 8)); assert g == 4
s3_chart = chart_curve_tangent(lambda x: x * x, -1, 4, (0, -4), (3, 8), 2,
                               "y = x²", -1, 4, -6, 18)
silver.append({
    "display": "A tangent at \\(x = 2\\) on \\(y = x^2\\) passes through \\((0, -4)\\) and \\((3, 8)\\). Find the gradient.",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Use the two points on the tangent: rise over run.",
    "chart": s3_chart,
    "misconceptions": [
        {"pattern": "swap_rise_run",
         "message": "Rise on top: (8 " + MINUS + " (" + MINUS + "4)) " + DIV + " (3 " + MINUS + " 0) = 12 " + DIV + " 3 = 4. Dividing run by rise gives 0.25 by mistake.",
         "expect": [0.25], "note": "3/12 = 0.25"}],
    "guided_steps": gs})

# s4 trap rule h=1 ys 0,3,8,15,24 -> 38
gs, A, aux = trap_steps([0, 3, 8, 15, 24], 1); assert A == 38
s4_chart = chart_curve_area([0, 1, 2, 3, 4], [0, 3, 8, 15, 24], ymax=26)
silver.append({
    "display": "Use the trapezium rule with 4 strips (\\(h = 1\\)) and y-values 0, 3, 8, 15, 24. Estimate the area.",
    "solutions": [38], "calculator": False, "input_type": "single_value",
    "hint": "Middles are 3, 8 and 15; double them, add the ends, times h over 2.",
    "chart": s4_chart,
    "misconceptions": [
        {"pattern": "no_half",
         "message": "Keep the ½. h " + DIV + " 2 = 0.5, so A = 0.5 " + TIMES + " 76 = 38, not 76.",
         "expect": [76], "note": "h*bracket = 1*76 = 76"},
        {"pattern": "middles_not_doubled",
         "message": "Double the middles 3, 8, 15. Counted once you get 0.5(0 + 24 + 26) = 25; doubled it is 38.",
         "expect": [25], "note": "0.5*(24+26) = 25"}],
    "guided_steps": gs})

# s5 trap rule 3 strips x 0..6 ys 0,6,8,6 -> 34 (h derived) (figure)
gs, A, aux = trap_steps([0, 6, 8, 6], 2, derive_h_from=(6, 3)); assert A == 34
s5_chart = chart_curve_area([0, 2, 4, 6], [0, 6, 8, 6], ymax=10)
silver.append({
    "display": "Estimate the area under a curve between \\(x = 0\\) and \\(x = 6\\) using 3 strips. y-values: 0, 6, 8, 6.",
    "solutions": [34], "calculator": False, "input_type": "single_value",
    "hint": "First find h = 6 divided by 3 strips, then apply the trapezium rule.",
    "chart": s5_chart,
    "misconceptions": [
        {"pattern": "wrong_h",
         "message": "With 3 strips over a width of 6, h = 6 " + DIV + " 3 = 2. Using h = 1 halves the area to 17; the correct estimate is 34.",
         "expect": [17], "note": "using h=1 gives 0.5*34 = 17"},
        {"pattern": "no_half",
         "message": "Do not drop the ½. h " + DIV + " 2 = 1, so A = 1 " + TIMES + " 34 = 34; multiplying by h = 2 would double it to 68.",
         "expect": [68], "note": "h*bracket = 2*34 = 68"}],
    "guided_steps": gs})

# s6 context: distance-time tangent gradient 12 -> speed 12
gs = [
    {"say": "On a distance-time graph, the gradient at a point is the instantaneous speed there."},
    {"pre": "read the gradient of the tangent = ", "post": "", "answer": 12,
     "hint": "It is given in the question."},
    {"say": "Speed equals that gradient.", "phase": "substitute",
     "pre": "so the speed at t = 5 = ", "post": "", "answer": 12,
     "hint": "Gradient of distance-time is speed."},
    {"phase": "substitute",
     "pre": f"check the units: 12 metres per second means in 1 s distance rises 12 {DIV} 1 = ",
     "post": "", "answer": 12,
     "done": "A gradient of 12 metres per second is a speed of 12 m/s.",
     "hint": "Distance change over time change, per second."}]
silver.append({
    "display": "A tangent to a distance-time curve at \\(t = 5\\) has gradient 12. What is the speed at \\(t = 5\\)?",
    "solutions": [12], "calculator": False, "input_type": "single_value",
    "hint": "Gradient of a distance-time graph is the speed, so read it straight off.",
    "misconceptions": [],
    "guided_steps": gs})

P["silver"] = silver
P["silver_description"] = "Apply the trapezium rule across several strips, or combine shapes to find a full distance."

# ---- GOLD ----
gold = []

# g0 trap rule 5 strips h=1 ys 1,2,5,10,17,26 -> 47.5 (calc) (completion)
gs, A, aux = trap_steps([1, 2, 5, 10, 17, 26], 1); assert A == 47.5
g0_chart = chart_curve_area([0, 1, 2, 3, 4, 5], [1, 2, 5, 10, 17, 26], ymax=28)
gold.append({
    "display": "Use the trapezium rule with 5 strips (\\(h = 1\\)) and y-values 1, 2, 5, 10, 17, 26. Estimate the area.",
    "solutions": [47.5], "calculator": True, "input_type": "single_value",
    "hint": "Double the four middle values, add the ends 1 and 26, then multiply by 0.5.",
    "chart": g0_chart,
    "misconceptions": [
        {"pattern": "no_half",
         "message": "h " + DIV + " 2 = 0.5, so A = 0.5 " + TIMES + " 95 = 47.5. Leaving out the ½ gives 95, which is double the true estimate.",
         "expect": [95], "note": "h*bracket = 1*95 = 95"},
        {"pattern": "middles_not_doubled",
         "message": "The four middles 2, 5, 10, 17 must be doubled. Counted once you get 0.5(27 + 34) = 30.5; doubled it is 47.5.",
         "expect": [30.5], "note": "0.5*(27+34) = 30.5"}],
    "guided_steps": gs})

# g1 MC over/under estimate -> overestimate
gold.append({
    "display": "The area under a speed-time curve from \\(t = 0\\) to \\(t = 10\\) is estimated as 85 m using the trapezium rule. The exact area is 83 m. Is the trapezium rule an overestimate or underestimate?",
    "options": ["Overestimate", "Underestimate", "Exact", "Cannot tell"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Compare the estimate with the exact value: is 85 bigger or smaller than 83?",
    "misconceptions": [
        {"pattern": "wrong_direction",
         "message": "85 is bigger than 83, so the estimate is too large: an overestimate. For a curve bending upward the trapeziums sit above it.",
         "expect": [1], "note": "picking underestimate"}]})

# g2 gradient (1,-4)-(3,20) on y=x^3 -> 12 (figure)
gs, g = grad_steps((1, -4), (3, 20)); assert g == 12
g2_chart = chart_curve_tangent(lambda x: x ** 3, 0, 3.2, (1, -4), (3, 20), 2,
                               "y = x³", 0, 3.2, -8, 30)
gold.append({
    "display": "On \\(y = x^3\\), a tangent at \\(x = 2\\) passes through \\((1, -4)\\) and \\((3, 20)\\). Find the gradient.",
    "solutions": [12], "calculator": False, "input_type": "single_value",
    "hint": "Use the two tangent points: rise over run, minding the negative.",
    "chart": g2_chart,
    "misconceptions": [
        {"pattern": "sign_slip",
         "message": "rise = 20 " + MINUS + " (" + MINUS + "4) = 24, not 16. So gradient = 24 " + DIV + " 2 = 12. Subtracting a negative adds.",
         "expect": [8], "note": "20-4=16 then 16/2=8 if the double-negative is missed"}],
    "guided_steps": gs})

# g3 trap rule h=0.5 ys 0,0.25,1,2.25,4 -> 2.75 (calc) (figure)
gs, A, aux = trap_steps([0, 0.25, 1, 2.25, 4], 0.5); assert A == 2.75
g3_chart = chart_curve_area([0, 0.5, 1, 1.5, 2], [0, 0.25, 1, 2.25, 4], xmax=2, ymax=4.5)
gold.append({
    "display": "Use the trapezium rule with \\(h = 0.5\\) and y-values 0, 0.25, 1, 2.25, 4 to estimate the area under \\(y = x^2\\) from 0 to 2.",
    "solutions": [2.75], "calculator": True, "input_type": "single_value",
    "hint": "Middles 0.25, 1, 2.25 doubled, ends 0 and 4, all times h over 2 which is 0.25.",
    "chart": g3_chart,
    "misconceptions": [
        {"pattern": "no_half",
         "message": "h " + DIV + " 2 = 0.25, so A = 0.25 " + TIMES + " 11 = 2.75. Multiplying by h = 0.5 instead gives 5.5, twice too big.",
         "expect": [5.5], "note": "h*bracket = 0.5*11 = 5.5"},
        {"pattern": "middles_not_doubled",
         "message": "Double the middles 0.25, 1, 2.25. Counted once you get 0.25(4 + 3.5) = 1.875; doubled it is 2.75.",
         "expect": [1.875], "note": "0.25*(4+3.5) = 1.875"}],
    "guided_steps": gs})

# g4 MC more strips -> better accuracy
gold.append({
    "display": "Explain why using more strips in the trapezium rule gives a better estimate. What happens to the accuracy as the number of strips increases?",
    "options": ["Accuracy increases, strips better approximate the curve",
                "Accuracy decreases, more rounding errors",
                "No change, it is always exact",
                "Accuracy depends on the curve shape only"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Think about how well a narrow straight-topped strip matches a curve compared with a wide one.",
    "misconceptions": [
        {"pattern": "thinks_worse",
         "message": "More strips means each strip is narrower, so its straight top hugs the curve more closely. The estimate gets better, not worse.",
         "expect": [1], "note": "picking accuracy decreases"}]})

P["gold"] = gold
P["gold_description"] = "Harder strips with decimals, plus interpreting accuracy and what a gradient or area means."

# ---------------------------------------------------------- tier_guides
tier_guides = {
    "bronze": {
        "title": "Bronze: gradient by rise over run, and simple areas",
        "steps": [
            "Gradient of a straight tangent = rise " + DIV + " run. Pick two clear points; rise is the change in y, run is the change in x.",
            "Area of a triangle = ½ " + TIMES + " base " + TIMES + " height. Trapezium = ½ " + TIMES + " (a + b) " + TIMES + " height. Rectangle = width " + TIMES + " height.",
            "On a speed-time graph the area is the distance; on a distance-time graph the gradient is the speed."],
        "example": {"question": "A tangent passes through (1, 2) and (4, 8). Find its gradient.",
                    "steps": [{"label": "Rise", "content": "8 " + MINUS + " 2 = 6"},
                              {"label": "Run", "content": "4 " + MINUS + " 1 = 3"},
                              {"label": "Check", "content": "from (1, 2) up 2" + TIMES + "3 = 6 reaches (4, 8)"},
                              {"label": "Gradient", "content": "6 " + DIV + " 3 = 2", "isAnswer": True, "is_answer": True}]}},
    "silver": {
        "title": "Silver: the trapezium rule",
        "steps": [
            "Split the area into equal strips of width h (h = total width " + DIV + " number of strips).",
            "A " + "≈" + " (h " + DIV + " 2) " + TIMES + " [first + last + 2 " + TIMES + " (all the middle values)].",
            "Read the y-values in order; double only the inside ones, and keep the ½ in h " + DIV + " 2."],
        "example": {"question": "h = 2, y-values 0, 5, 8. Estimate the area.",
                    "steps": [{"label": "Bracket", "content": "0 + 8 + 2" + TIMES + "5 = 18"},
                              {"label": "Half-width", "content": "h " + DIV + " 2 = 1"},
                              {"label": "Check", "content": "middle counted twice, ends once"},
                              {"label": "Area", "content": "1 " + TIMES + " 18 = 18", "isAnswer": True, "is_answer": True}]}},
    "gold": {
        "title": "Gold: harder strips and interpretation",
        "steps": [
            "Decimal strip widths and y-values work the same way: keep h " + DIV + " 2 exact.",
            "More strips means narrower strips, so the estimate fits the curve more closely and improves.",
            "For a curve bending upward the trapeziums lie above it, so the rule overestimates."],
        "example": {"question": "An estimate gives 51; the exact area is 50. Over or under, and by how much?",
                    "steps": [{"label": "Compare", "content": "51 is bigger than 50"},
                              {"label": "Type", "content": "estimate too large, so overestimate"},
                              {"label": "Check", "content": "curve bends up, trapeziums sit above"},
                              {"label": "Difference", "content": "51 " + MINUS + " 50 = 1", "isAnswer": True, "is_answer": True}]}}
}
P_tier_guides = tier_guides

# ---------------------------------------------------------- opener
opener_svg = st_graph([(0, 0), (3, 0), (3, 20), (0, 20)], xmax=4, ymax=24,
                      xticks=[0, 1, 2, 3], yticks=[0, 5, 10, 15, 20],
                      xlabel="time (s)", ylabel="speed (m/s)",
                      aria="Speed-time graph of a steady 20 metres per second for 3 seconds: a rectangle 3 wide and 20 tall",
                      caption="Steady 20 m/s for 3 s",
                      annots=[(1.5, -1.7, "3 s", "middle"), (3.3, 11, "20 m/s", "start")])
opener = {
    "display": opener_svg + "<p>A car travels at a steady <strong>20 m/s</strong>. Here is its speed-time graph for the first 3 seconds.</p>",
    "steps": [
        {"pre": "How far does it travel? distance = speed " + TIMES + " time = 20 " + TIMES + " 3 = ",
         "post": "", "answer": 60, "hint": "Multiply the speed by the time."},
        {"pre": "That distance is exactly the shaded AREA of the graph (a 3 by 20 rectangle): 3 " + TIMES + " 20 = ",
         "post": "", "answer": 60, "hint": "Width times height of the rectangle."},
        {"say": "You just found a distance by taking the <strong>area under a speed-time graph</strong>. When the graph is a neat rectangle it is easy. When it <strong>curves</strong>, we chop the area into thin strips and add them (the <strong>trapezium rule</strong>). And the <strong>steepness</strong> of a graph at a point has meaning too: on a distance-time graph the gradient of the tangent is the speed right then."}]
}

# ---------------------------------------------------------- teach walks
teach = {
    "bronze": {
        "display": "<p>A tangent to a curve passes through <strong>(2, 1)</strong> and <strong>(6, 9)</strong>. Find its gradient.</p>",
        "steps": [
            {"say": "Gradient = rise " + DIV + " run. Work out the rise first."},
            {"pre": "rise: 9 " + MINUS + " 1 = ", "post": "", "answer": 8, "hint": "Second y minus first y."},
            {"pre": "run: 6 " + MINUS + " 2 = ", "post": "", "answer": 4, "hint": "Second x minus first x."},
            {"pre": "gradient: 8 " + DIV + " 4 = ", "post": "", "answer": 2, "hint": "Rise over run.",
             "done": "That is the whole move: rise over run."},
            {"pre": "check, from (2, 1) go across 4 and up 2" + TIMES + "4: 1 + 8 = ", "post": "",
             "answer": 9, "hint": "Add the rise back on.", "done": "Reaches (6, 9), so the gradient is 2."}]},
    "silver": {
        "display": "<p>Use the trapezium rule with 3 strips (<strong>h = 1</strong>) and y-values <strong>2, 5, 10, 17</strong> to estimate the area.</p>",
        "steps": [
            {"say": "A " + "≈" + " (h " + DIV + " 2) " + TIMES + " [first + last + 2 " + TIMES + " (middles)]. Build the bracket."},
            {"pre": "add the middles: 5 + 10 = ", "post": "", "answer": 15, "hint": "Inside values only."},
            {"pre": "double them: 2 " + TIMES + " 15 = ", "post": "", "answer": 30, "hint": "Middles count twice."},
            {"pre": "first + last: 2 + 17 = ", "post": "", "answer": 19, "hint": "The two ends, once each."},
            {"pre": "bracket total: 19 + 30 = ", "post": "", "answer": 49, "hint": "Ends plus doubled middles."},
            {"pre": "A = (1 " + DIV + " 2) " + TIMES + " 49 = 0.5 " + TIMES + " 49 = ", "post": "", "answer": 24.5,
             "hint": "Half of 49.", "done": "The half-width finishes it: 24.5."}]},
    "gold": {
        "display": "<p>Use the trapezium rule with 5 strips (<strong>h = 1</strong>) and y-values <strong>0, 1, 4, 9, 16, 25</strong> to estimate the area under <strong>y = x²</strong> from 0 to 5.</p>",
        "steps": [
            {"say": "Six y-values, five strips. A " + "≈" + " (h " + DIV + " 2) " + TIMES + " [first + last + 2 " + TIMES + " (middles)]."},
            {"pre": "add the four middles: 1 + 4 + 9 + 16 = ", "post": "", "answer": 30, "hint": "All but the first and last."},
            {"pre": "double them: 2 " + TIMES + " 30 = ", "post": "", "answer": 60, "hint": "Inside values twice."},
            {"pre": "first + last: 0 + 25 = ", "post": "", "answer": 25, "hint": "The two ends."},
            {"pre": "bracket total: 25 + 60 = ", "post": "", "answer": 85, "hint": "Add them."},
            {"pre": "A = 0.5 " + TIMES + " 85 = ", "post": "", "answer": 42.5, "hint": "Half of 85.",
             "done": "42.5. The true area is 41.67, so this slightly overestimates: the curve bends upward."}]}
}

guided = {"opener": opener, "teach": teach}

# ---------------------------------------------------------- method_card (slim)
method_card = {
    "title": "Estimating Gradients of Curves & Areas Under Graphs",
    "steps": [
        "Gradient at a point: draw the tangent, then rise " + DIV + " run.",
        "Area: use the trapezium rule, A " + "≈" + " (h " + DIV + " 2)[first + last + 2(middles)].",
        "Speed-time area = distance; distance-time gradient = speed.",
        "Keep the ½ and double only the inside y-values."],
    "content": "<p>The <strong>gradient of a curve</strong> at a point is the gradient of the <strong>tangent</strong> there (rise " + DIV + " run). The <strong>area under a curve</strong> is estimated with the <strong>trapezium rule</strong>:</p><p>$$A \\approx \\frac{h}{2}\\left[y_0 + y_n + 2(y_1 + \\ldots + y_{n-1})\\right]$$</p><p>where h is the strip width. On a speed-time graph the area is the distance; on a distance-time graph the gradient is the speed.</p>",
    "example": "<p><strong>Estimate the area under \\(y = x^2\\) from 0 to 4, 4 strips (h = 1).</strong> y-values 0, 1, 4, 9, 16.</p><p>$$A \\approx \\tfrac{1}{2}[0 + 16 + 2(1 + 4 + 9)] = \\tfrac{1}{2}(44) = 22$$</p>"
}

# ---------------------------------------------------------- assemble
live = json.load(io.open("_live_gl08.json", encoding="utf-8"))
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],           # preserved
    "problem_bank": P,
    "tier_guides": P_tier_guides,
    "guided": guided,
    "related_videos": live["related_videos"],      # preserved
    "worked_examples": live["worked_examples"],    # preserved
}

# ---------------------------------------------------------- self-verify
def trap_true(ys, h):
    return (h / 2) * (ys[0] + ys[-1] + 2 * sum(ys[1:-1]))
errs = []
# check every guided_steps final live boxes land on solutions
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(P[tier]):
        if p["input_type"] == "multiple_choice":
            continue
        gs = p["guided_steps"]
        # last box value must equal solution
        last_box = [s for s in gs if s.get("answer") is not None][-1]
        # find the box that states the final area/gradient (the substitute box before check)
        sub_boxes = [s for s in gs if s.get("phase") == "substitute" and s.get("answer") is not None]
        target = p["solutions"][0]
        vals = [s["answer"] for s in sub_boxes]
        if target not in vals and abs(last_box["answer"] - target) > 0.011:
            errs.append(f"{tier}[{i}] solution {target} not hit by substitute boxes {vals}")
        # em dash scan
        for s in gs:
            for k in ("pre", "post", "say", "hint", "done"):
                if isinstance(s.get(k), str) and "—" in s[k]:
                    errs.append(f"{tier}[{i}] em dash in {k}")
        # misconception expect != solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if isinstance(e, list) and len(e) == 1 and abs(e[0] - target) < 0.011:
                errs.append(f"{tier}[{i}] expect equals solution")

print("SELF-CHECK errors:", errs if errs else "none")
json.dump(out, io.open("lesson_maths-aqa_graphs-L08.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_graphs-L08.json")
