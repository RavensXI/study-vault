# -*- coding: utf-8 -*-
"""Build full guided-learning + diagrams practice_data for graphs-L08 (maths-ocr)."""
import io, json

KEY = "graphs-L08"
base = json.load(io.open("_G08_live.json", encoding="utf-8"))["practice_data"]

# ---------- figure helpers ----------
def area_chart(xs, ys, xt="x", yt="y"):
    pts = [{"x": x, "y": y} for x, y in zip(xs, ys)]
    return {"type": "line",
            "data": {"datasets": [{"data": pts, "fill": True, "tension": 0,
                                   "borderColor": "#3b82f6",
                                   "backgroundColor": "rgba(59,130,246,0.15)",
                                   "pointRadius": 4, "pointBackgroundColor": "#3b82f6"}]},
            "options": {"plugins": {"legend": {"display": False}},
                        "scales": {"x": {"type": "linear", "title": {"text": xt, "display": True},
                                         "grid": {"color": "rgba(0,0,0,0.05)"}},
                                   "y": {"beginAtZero": True, "title": {"text": yt, "display": True},
                                         "grid": {"color": "rgba(0,0,0,0.08)"}}}}}

def curve_chord_chart():
    cx = [round(1.6 + 0.1 * i, 1) for i in range(9)]  # 1.6..2.4
    cubic = [{"x": x, "y": round(x ** 3, 4)} for x in cx]
    chord = [{"x": 1.9, "y": 6.859}, {"x": 2.1, "y": 9.261}]
    return {"type": "line",
            "data": {"datasets": [
                {"label": "y = x cubed", "data": cubic, "fill": False, "tension": 0.35,
                 "borderColor": "#3b82f6", "pointRadius": 0, "borderWidth": 2},
                {"label": "chord", "data": chord, "fill": False, "tension": 0,
                 "borderColor": "#f59e0b", "pointRadius": 5, "pointBackgroundColor": "#f59e0b",
                 "borderWidth": 2}]},
            "options": {"plugins": {"legend": {"display": False}},
                        "scales": {"x": {"type": "linear", "title": {"text": "x", "display": True},
                                         "grid": {"color": "rgba(0,0,0,0.05)"}},
                                   "y": {"title": {"text": "y", "display": True},
                                         "grid": {"color": "rgba(0,0,0,0.08)"}}}}}

def parab_chart():  # gold teach: y=x^2 near x=4 with chord
    cx = [round(3.6 + 0.1 * i, 1) for i in range(9)]
    curve = [{"x": x, "y": round(x ** 2, 4)} for x in cx]
    chord = [{"x": 3.9, "y": 15.21}, {"x": 4.1, "y": 16.81}]
    return {"type": "line",
            "data": {"datasets": [
                {"label": "y = x squared", "data": curve, "fill": False, "tension": 0.35,
                 "borderColor": "#3b82f6", "pointRadius": 0, "borderWidth": 2},
                {"label": "chord", "data": chord, "fill": False, "tension": 0,
                 "borderColor": "#f59e0b", "pointRadius": 5, "pointBackgroundColor": "#f59e0b",
                 "borderWidth": 2}]},
            "options": {"plugins": {"legend": {"display": False}},
                        "scales": {"x": {"type": "linear", "title": {"text": "x", "display": True},
                                         "grid": {"color": "rgba(0,0,0,0.05)"}},
                                   "y": {"title": {"text": "y", "display": True},
                                         "grid": {"color": "rgba(0,0,0,0.08)"}}}}}

FS = 'font-family="Inter, sans-serif"'
SVG_RECT = ('<svg viewBox="0 0 220 150" role="img" aria-label="Rectangle of width 3 and height 5" style="max-width:220px">'
            '<rect x="45" y="25" width="120" height="90" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<text x="105" y="134" text-anchor="middle" fill="currentColor" %s font-size="12">3</text>'
            '<text x="30" y="74" text-anchor="middle" fill="currentColor" %s font-size="12">5</text></svg>' % (FS, FS))

SVG_TRI = ('<svg viewBox="0 0 220 160" role="img" aria-label="Right-angled triangle with base 4 and height 6" style="max-width:220px">'
           '<polygon points="45,130 45,30 160,130" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
           '<rect x="45" y="118" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1"/>'
           '<text x="100" y="150" text-anchor="middle" fill="currentColor" %s font-size="12">4</text>'
           '<text x="32" y="84" text-anchor="middle" fill="currentColor" %s font-size="12">6</text></svg>'
           '<span class="figure-caption">Diagram not drawn accurately</span>' % (FS, FS))

SVG_TRAP = ('<svg viewBox="0 0 230 150" role="img" aria-label="Trapezium with parallel sides 4 and 6 and height 4" style="max-width:230px">'
            '<polygon points="75,30 155,30 180,118 50,118" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<text x="115" y="24" text-anchor="middle" fill="currentColor" %s font-size="12">4</text>'
            '<text x="115" y="135" text-anchor="middle" fill="currentColor" %s font-size="12">6</text>'
            '<text x="36" y="78" text-anchor="middle" fill="currentColor" %s font-size="12">4</text></svg>'
            '<span class="figure-caption">Diagram not drawn accurately</span>' % (FS, FS, FS))

SVG_TP = ('<svg viewBox="0 0 240 160" role="img" aria-label="A curve with a horizontal tangent at its highest point, where the gradient is zero" style="max-width:240px">'
          '<path d="M30,140 Q120,-8 210,140" fill="none" stroke="currentColor" stroke-width="1.8"/>'
          '<line x1="62" y1="36" x2="178" y2="36" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4 3"/>'
          '<circle cx="120" cy="36" r="3.5" fill="#3b82f6"/>'
          '<text x="120" y="26" text-anchor="middle" fill="currentColor" %s font-size="11">gradient = 0</text></svg>' % FS)

SVG_B7 = ('<svg viewBox="0 0 240 160" role="img" aria-label="A curve with a horizontal tangent touching its peak, through two points of equal height" style="max-width:240px">'
          '<path d="M30,140 Q120,-8 210,140" fill="none" stroke="currentColor" stroke-width="1.8"/>'
          '<line x1="72" y1="40" x2="172" y2="40" stroke="#3b82f6" stroke-width="1.5"/>'
          '<circle cx="96" cy="40" r="3.5" fill="#3b82f6"/><text x="96" y="31" text-anchor="middle" fill="currentColor" %s font-size="10">(3, 7)</text>'
          '<circle cx="150" cy="40" r="3.5" fill="#3b82f6"/><text x="150" y="31" text-anchor="middle" fill="currentColor" %s font-size="10">(5, 7)</text></svg>' % (FS, FS))

SVG_OPENER = ('<svg viewBox="0 0 240 165" role="img" aria-label="Speed-time graph: a flat line at 6 metres per second for 4 seconds with the area underneath shaded" style="max-width:240px">'
              '<line x1="45" y1="20" x2="45" y2="130" stroke="currentColor" stroke-width="1.5"/>'
              '<line x1="45" y1="130" x2="215" y2="130" stroke="currentColor" stroke-width="1.5"/>'
              '<rect x="45" y="60" width="130" height="70" fill="#60a5fa" fill-opacity="0.3"/>'
              '<line x1="45" y1="60" x2="175" y2="60" stroke="#3b82f6" stroke-width="2"/>'
              '<text x="36" y="64" text-anchor="end" fill="currentColor" %s font-size="11">6</text>'
              '<text x="175" y="145" text-anchor="middle" fill="currentColor" %s font-size="11">4</text>'
              '<text x="120" y="160" text-anchor="middle" fill="currentColor" %s font-size="10">time (s)</text>'
              '<text x="22" y="40" text-anchor="middle" fill="currentColor" %s font-size="10" transform="rotate(-90 22 40)">speed</text></svg>' % (FS, FS, FS, FS))

# ---------- guided_steps generators ----------
def grad_steps(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    g = rise / run
    g = int(g) if float(g).is_integer() else g
    def fmt(n):
        return str(int(n)) if float(n).is_integer() else str(n)
    end_y = y1 + rise
    return [
        {"say": "Gradient is the rise (change in y) divided by the run (change in x). Find the rise first:",
         "pre": "%s − %s = " % (fmt(y2), fmt(y1)), "post": "", "answer": rise,
         "hint": "Subtract the two y-values, %s take away %s." % (fmt(y2), fmt(y1))},
        {"pre": "%s − %s = " % (fmt(x2), fmt(x1)), "post": "", "answer": run,
         "hint": "Now the run: subtract the two x-values."},
        {"say": "Gradient = rise ÷ run.", "phase": "substitute",
         "pre": "%s ÷ %s = " % (fmt(rise), fmt(run)), "post": "", "answer": g,
         "hint": "Divide the rise by the run."},
        {"say": "Check by walking from the first point. Moving %s across should change y by %s × %s = %s:" % (fmt(run), fmt(run), fmt(g), fmt(rise)),
         "pre": "%s + (%s) = " % (fmt(y1), fmt(rise)), "post": "", "answer": end_y,
         "done": "Lands on (%s, %s). Correct." % (fmt(x2), fmt(end_y)),
         "hint": "Add the rise %s to the starting y-value %s." % (fmt(rise), fmt(y1))},
    ]

def fmt(n):
    return str(int(n)) if float(n).is_integer() else str(n)

def trap_steps(h, ys, unit="square units"):
    y0, yn = ys[0], ys[-1]
    mids = ys[1:-1]
    ends = y0 + yn
    md = 2 * sum(mids)
    bracket = ends + md
    hh = h / 2
    area = hh * bracket
    area = int(area) if float(area).is_integer() else area
    md_expr = "2 × %s" % fmt(sum(mids)) if len(mids) == 1 else "2 × (%s)" % (" + ".join(fmt(m) for m in mids))
    # individual trapezia for the check
    pieces = [round(0.5 * (ys[i] + ys[i + 1]) * h, 4) for i in range(len(ys) - 1)]
    pieces = [int(p) if float(p).is_integer() else p for p in pieces]
    piece_sum = sum(pieces)
    piece_sum = int(piece_sum) if float(piece_sum).is_integer() else round(piece_sum, 4)
    return [
        {"say": "Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:",
         "pre": "%s + %s = " % (fmt(y0), fmt(yn)), "post": "", "answer": ends,
         "hint": "Add the first y-value and the last y-value."},
        {"say": "Now the inside heights, each counted twice:",
         "pre": "%s = " % md_expr, "post": "", "answer": md,
         "hint": "Add the middle heights, then double the total."},
        {"pre": "%s + %s = " % (fmt(ends), fmt(md)), "post": "", "answer": bracket,
         "hint": "Add the two parts to get the bracket total."},
        {"say": "Multiply by h ÷ 2 = %s ÷ 2 = %s:" % (fmt(h), fmt(hh)), "phase": "substitute",
         "pre": "%s × %s = " % (fmt(hh), fmt(bracket)), "post": "", "answer": area,
         "hint": "Multiply the bracket total by %s." % fmt(hh)},
        {"say": "Check by adding the trapezia one at a time (%s):" % (" + ".join(fmt(p) for p in pieces)),
         "pre": "%s = " % (" + ".join(fmt(p) for p in pieces)), "post": "", "answer": piece_sum,
         "done": "Both methods give %s %s. Correct." % (fmt(area), unit),
         "hint": "Add the separate strip areas."},
    ]

# ---------- BRONZE ----------
bronze = [
    {  # B0 (2,4)(6,12) -> 2
        "display": "A tangent passes through \\((2, 4)\\) and \\((6, 12)\\). Find the gradient.",
        "solutions": [2], "calculator": False, "input_type": "single_value",
        "hint": "Gradient is rise over run: divide the change in y by the change in x.",
        "misconceptions": [{"pattern": "rise_run_inverted",
                            "message": "You divided run by rise. Gradient is rise over run: 8 ÷ 4, not 4 ÷ 8.",
                            "expect": 0.5}],
        "guided_steps": grad_steps(2, 4, 6, 12)},
    {  # B1 (1,5)(3,11) -> 3
        "display": "A tangent passes through \\((1, 5)\\) and \\((3, 11)\\). Find the gradient.",
        "solutions": [3], "calculator": False, "input_type": "single_value",
        "hint": "Find the change in y, the change in x, then divide.",
        "misconceptions": [{"pattern": "rise_only",
                            "message": "That is only the rise. You still need to divide by the run (the change in x).",
                            "expect": 6}],
        "guided_steps": grad_steps(1, 5, 3, 11)},
    {  # B2 (0,2)(2,10) -> 4  (was (4,10)->2, duplicate of B0)
        "display": "A tangent passes through \\((0, 2)\\) and \\((2, 10)\\). Find the gradient.",
        "solutions": [4], "calculator": False, "input_type": "single_value",
        "hint": "Rise over run: divide the change in y by the change in x.",
        "misconceptions": [{"pattern": "rise_run_inverted",
                            "message": "You divided run by rise. Gradient is rise over run: 8 ÷ 2, not 2 ÷ 8.",
                            "expect": 0.25}],
        "guided_steps": grad_steps(0, 2, 2, 10)},
    {  # B3 rectangle 3x5 -> 15
        "display": SVG_RECT + "Estimate the area of a rectangle: width 3, height 5.",
        "solutions": [15], "calculator": False, "input_type": "single_value",
        "hint": "Area of a rectangle is base times height.",
        "misconceptions": [{"pattern": "added_not_multiplied",
                            "message": "You added the sides. Area of a rectangle is base × height, so 3 × 5, not 3 + 5.",
                            "expect": 8}],
        "guided_steps": [
            {"say": "The area under a flat section is a rectangle: base × height. Read the base:",
             "pre": "base = ", "post": "", "answer": 3, "hint": "The width is 3."},
            {"pre": "height = ", "post": "", "answer": 5, "hint": "The height is 5."},
            {"say": "Multiply base by height.", "phase": "substitute",
             "pre": "3 × 5 = ", "post": "", "answer": 15, "hint": "Three fives."},
            {"say": "Check by adding five lots of 3:",
             "pre": "3 + 3 + 3 + 3 + 3 = ", "post": "", "answer": 15,
             "done": "15 square units either way. Correct.", "hint": "Add 3 five times."}]},
    {  # B4 triangle base4 height6 -> 12
        "display": SVG_TRI + "Estimate the area of a triangle: base 4, height 6.",
        "solutions": [12], "calculator": False, "input_type": "single_value",
        "hint": "Area of a triangle is half of base times height.",
        "misconceptions": [{"pattern": "forgot_half",
                            "message": "You found the surrounding rectangle. A triangle is half of that, so halve 24.",
                            "expect": 24}],
        "guided_steps": [
            {"say": "A triangle is half of the rectangle around it. Find base × height first:",
             "pre": "4 × 6 = ", "post": "", "answer": 24, "hint": "Multiply base by height."},
            {"say": "A triangle is half that rectangle.", "phase": "substitute",
             "pre": "24 ÷ 2 = ", "post": "", "answer": 12, "hint": "Halve 24."},
            {"say": "Check the other way: halve the base first, ½ × 4 = 2, then times height:",
             "pre": "2 × 6 = ", "post": "", "answer": 12,
             "done": "12 square units. Correct.", "hint": "Two sixes."}]},
    {  # B5 increasing -> 1  (was decreasing enter 0, duplicate of B7)
        "display": "A tangent to a curve at \\(x = 2\\) has gradient 5. Is the curve increasing or decreasing here? Enter 1 for increasing, 0 for decreasing.",
        "solutions": [1], "calculator": False, "input_type": "single_value",
        "hint": "A positive gradient slopes uphill as x increases.",
        "misconceptions": [{"pattern": "sign_confused",
                            "message": "A positive gradient slopes uphill as x increases, so the curve is increasing. Enter 1, not 0.",
                            "expect": 0}],
        "guided_steps": [
            {"say": "A gradient is the slope of the tangent. The gradient here is 5. Is 5 greater than 0? Enter 1 for yes, 0 for no:",
             "pre": "answer = ", "post": "", "answer": 1, "hint": "5 is greater than 0."},
            {"say": "A positive slope goes uphill as x increases, which means the curve is increasing.", "phase": "substitute",
             "pre": "enter 1 for increasing = ", "post": "", "answer": 1, "hint": "Positive gradient means increasing."},
            {"say": "Check: a line of slope 5 rises steeply from left to right, so y is going up.",
             "pre": "confirm increasing, enter 1 = ", "post": "", "answer": 1,
             "done": "Positive gradient, curve increasing. Correct.", "hint": "Enter 1."}]},
    {  # B6 trapezium 4,6 h4 -> 20  (was height 3 -> 15, duplicate of B3)
        "display": SVG_TRAP + "A trapezium has parallel sides 4 and 6, height 4. Find the area.",
        "solutions": [20], "calculator": False, "input_type": "single_value",
        "hint": "Average the parallel sides, then multiply by the height.",
        "misconceptions": [{"pattern": "forgot_half",
                            "message": "You forgot to average the parallel sides. Area is ½(4 + 6) × 4, so halve the (4 + 6) first.",
                            "expect": 40}],
        "guided_steps": [
            {"say": "A trapezium's area is the average of the two parallel sides, times the height. Add the parallel sides:",
             "pre": "4 + 6 = ", "post": "", "answer": 10, "hint": "Add the two parallel sides."},
            {"pre": "average them: 10 ÷ 2 = ", "post": "", "answer": 5, "hint": "Halve the total."},
            {"say": "Multiply the average by the height 4.", "phase": "substitute",
             "pre": "5 × 4 = ", "post": "", "answer": 20, "hint": "Five fours."},
            {"say": "Check with the full formula ½(a + b)h = ½ × 10 × 4:",
             "pre": "½ × 10 × 4 = ", "post": "", "answer": 20,
             "done": "20 square units. Correct.", "hint": "Half of 10 is 5, times 4."}]},
    {  # B7 (3,7)(5,7) -> 0 horizontal tangent
        "display": SVG_B7 + "A tangent passes through \\((3, 7)\\) and \\((5, 7)\\). Find the gradient.",
        "solutions": [0], "calculator": False, "input_type": "single_value",
        "hint": "Both points have the same height, so think about the rise.",
        "misconceptions": [{"pattern": "used_run",
                            "message": "The rise is 7 − 7 = 0, so the gradient is 0. You may have written the run (2) instead.",
                            "expect": 2}],
        "guided_steps": [
            {"say": "Gradient is rise over run. Find the rise (change in y) first:",
             "pre": "7 − 7 = ", "post": "", "answer": 0, "hint": "Subtract the y-values, both are 7."},
            {"pre": "run: 5 − 3 = ", "post": "", "answer": 2, "hint": "Subtract the x-values."},
            {"say": "Gradient = rise ÷ run.", "phase": "substitute",
             "pre": "0 ÷ 2 = ", "post": "", "answer": 0, "hint": "Zero divided by anything is 0."},
            {"say": "A gradient of 0 means the tangent is flat. Both points sit at the same height, so the tangent is horizontal. Confirm the gradient:",
             "pre": "gradient = ", "post": "", "answer": 0,
             "done": "Zero gradient: a horizontal tangent, a turning point.", "hint": "A flat line has gradient 0."}]},
]

# ---------- SILVER ----------
silver = [
    {  # S0 h2 y[1,6,13] -> 26  (was [1,5,13]->24, duplicate of S6)
        "display": "Trapezium rule: \\(h = 2\\), y-values: 1, 6, 13. Find the area.",
        "solutions": [26], "calculator": False, "input_type": "single_value",
        "hint": "Add the ends, add double the middle, then multiply by h ÷ 2.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "The middle height must be counted twice: 1 + 13 + 2 × 6, not 1 + 13 + 6.",
                            "expect": 20}],
        "chart": area_chart([0, 2, 4], [1, 6, 13]),
        "guided_steps": trap_steps(2, [1, 6, 13])},
    {  # S1 h1 y[0,1,4,9] -> 9.5
        "display": "Trapezium rule: \\(h = 1\\), y-values: 0, 1, 4, 9. Find the area.",
        "solutions": [9.5], "calculator": False, "input_type": "single_value",
        "hint": "The two inside heights each count twice.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "Every inside height counts twice. Use 0 + 9 + 2 × (1 + 4), not 0 + 9 + (1 + 4).",
                            "expect": 7}],
        "chart": area_chart([0, 1, 2, 3], [0, 1, 4, 9]),
        "guided_steps": trap_steps(1, [0, 1, 4, 9])},
    {  # S2 (-1,6)(3,-2) -> -2
        "display": "A tangent passes through \\((-1, 6)\\) and \\((3, -2)\\). Find the gradient.",
        "solutions": [-2], "calculator": False, "input_type": "single_value",
        "hint": "Keep the signs: rise and run can be negative.",
        "misconceptions": [{"pattern": "sign_error",
                            "message": "Watch the signs. Rise = −2 − 6 = −8 and run = 3 − (−1) = 4, so −8 ÷ 4 = −2, not +2.",
                            "expect": 2}],
        "guided_steps": grad_steps(-1, 6, 3, -2)},
    {  # S3 h0.5 y[2,3,5,8,12] -> 11.5  (was stored 10.5, WRONG)
        "display": "Trapezium rule: \\(h = 0.5\\), y-values: 2, 3, 5, 8, 12. Find the area.",
        "solutions": [11.5], "calculator": False, "input_type": "single_value",
        "hint": "Double the three inside heights before multiplying by h ÷ 2.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "Double the three inside heights: 2 + 12 + 2 × (3 + 5 + 8), not 2 + 12 + (3 + 5 + 8).",
                            "expect": 7.5}],
        "chart": area_chart([0, 0.5, 1, 1.5, 2], [2, 3, 5, 8, 12]),
        "guided_steps": trap_steps(0.5, [2, 3, 5, 8, 12])},
    {  # S4 MC turning point
        "display": SVG_TP + "A curve has gradient 0 at \\(x = 3\\). What does this tell you?",
        "options": ["Turning point", "Root", "y-intercept", "Asymptote"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "A gradient of 0 means the tangent is horizontal.",
        "misconceptions": [{"pattern": "concept",
                            "message": "Gradient 0 means the tangent is flat, which happens at a turning point (a peak or a valley), not at a root or asymptote.",
                            "expect": None}]},
    {  # S5 h1 y[2,4,8] -> 9  (was stored 12, WRONG)
        "display": "Trapezium rule: \\(h = 1\\), y-values: 2, 4, 8. Find the area.",
        "solutions": [9], "calculator": False, "input_type": "single_value",
        "hint": "The middle height is counted twice.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "The middle height is counted twice: 2 + 8 + 2 × 4, not 2 + 8 + 4.",
                            "expect": 7}],
        "chart": area_chart([0, 1, 2], [2, 4, 8]),
        "guided_steps": trap_steps(1, [2, 4, 8])},
    {  # S6 h2 y[0,4,16] -> 24
        "display": "Trapezium rule: \\(h = 2\\), y-values: 0, 4, 16. Find the area.",
        "solutions": [24], "calculator": False, "input_type": "single_value",
        "hint": "Double the middle height, then multiply by h ÷ 2 = 1.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "Double the middle height: 0 + 16 + 2 × 4, not 0 + 16 + 4.",
                            "expect": 20}],
        "chart": area_chart([0, 2, 4], [0, 4, 16]),
        "guided_steps": trap_steps(2, [0, 4, 16])},
]

# ---------- GOLD ----------
gold = [
    {  # G0 h1 y[1,2,5,10,17] -> 26  (was stored 25, WRONG)
        "display": "Trapezium rule: \\(h = 1\\), y-values: 1, 2, 5, 10, 17. Find the area.",
        "solutions": [26], "calculator": False, "input_type": "single_value",
        "hint": "The three inside heights each count twice.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "All three inside heights count twice: 1 + 17 + 2 × (2 + 5 + 10), not added once.",
                            "expect": 17.5}],
        "chart": area_chart([0, 1, 2, 3, 4], [1, 2, 5, 10, 17]),
        "guided_steps": trap_steps(1, [1, 2, 5, 10, 17])},
    {  # G1 speed-time -> 60 m
        "display": "The area under a speed-time graph is the distance travelled. Speeds at t = 0, 2, 4, 6 are 0, 8, 12, 20 m/s. Use the trapezium rule (h = 2) to estimate the distance.",
        "solutions": [60], "calculator": False, "input_type": "single_value",
        "hint": "Treat speed as the height: add the ends, double the inside speeds, times h ÷ 2.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "The inside speeds count twice: 0 + 20 + 2 × (8 + 12), giving 60 m, not added once.",
                            "expect": 40}],
        "chart": area_chart([0, 2, 4, 6], [0, 8, 12, 20], xt="time (s)", yt="speed (m/s)"),
        "guided_steps": trap_steps(2, [0, 8, 12, 20], unit="m")},
    {  # G2 % error -> 7.8
        "display": "The trapezium rule gives area 48.5. The exact area is 45. Find the percentage error to 1 d.p.",
        "solutions": [7.8], "calculator": True, "input_type": "single_value",
        "hint": "Percentage error is the error divided by the true value, times 100.",
        "misconceptions": [{"pattern": "wrong_base",
                            "message": "Percentage error divides by the true value: 3.5 ÷ 45, not 3.5 ÷ 48.5.",
                            "expect": 7.2}],
        "guided_steps": [
            {"say": "Percentage error = (size of error ÷ true value) × 100. First the size of the error:",
             "pre": "48.5 − 45 = ", "post": "", "answer": 3.5, "hint": "Subtract the exact value from the estimate."},
            {"say": "Divide by the true value 45, then multiply by 100.", "phase": "substitute",
             "pre": "3.5 ÷ 45 × 100 = ", "post": "", "answer": 7.8,
             "hint": "Divide by 45, then times 100. Round to 1 d.p."},
            {"say": "Check: 7.8% of 45 should give back the error. 0.078 × 45 ≈ 3.5:",
             "pre": "enter the error, 3.5 = ", "post": "", "answer": 3.5,
             "done": "The error comes back, so 7.8% is right.", "hint": "Enter 3.5."}]},
    {  # G3 chord y=x^3 at x=2 -> 12.01
        "display": "A curve has \\(y = x^3\\). Estimate the gradient at \\(x = 2\\) using \\((1.9, 6.859)\\) and \\((2.1, 9.261)\\).",
        "solutions": [12.01], "calculator": True, "input_type": "single_value",
        "hint": "Find the rise and the run between the two points, then divide.",
        "misconceptions": [{"pattern": "wrong_run",
                            "message": "The run is 2.1 − 1.9 = 0.2, not 1. Divide the rise 2.402 by 0.2.",
                            "expect": 2.402}],
        "chart": curve_chord_chart(),
        "guided_steps": [
            {"say": "Estimate the gradient with a chord between the two nearby points. Find the rise:",
             "pre": "9.261 − 6.859 = ", "post": "", "answer": 2.402, "hint": "Subtract the y-values."},
            {"pre": "run: 2.1 − 1.9 = ", "post": "", "answer": 0.2, "hint": "Subtract the x-values."},
            {"say": "Gradient = rise ÷ run.", "phase": "substitute",
             "pre": "2.402 ÷ 0.2 = ", "post": "", "answer": 12.01, "hint": "Divide 2.402 by 0.2."},
            {"say": "Check against the exact gradient. For \\(y = x^3\\) it is \\(3x^2\\), and at x = 2 that is 3 × 4:",
             "pre": "3 × 4 = ", "post": "", "answer": 12,
             "done": "The estimate 12.01 is very close to the exact 12. Correct.", "hint": "Three fours."}]},
    {  # G4 h0.5 y[1,1.5,2.5,4,6] -> 5.75  (was stored 5.5, WRONG)
        "display": "Trapezium rule: \\(h = 0.5\\), y-values: 1, 1.5, 2.5, 4, 6. Find the area.",
        "solutions": [5.75], "calculator": False, "input_type": "single_value",
        "hint": "Double the three inside heights before multiplying by h ÷ 2.",
        "misconceptions": [{"pattern": "middle_not_doubled",
                            "message": "Double the three inside heights: 1 + 6 + 2 × (1.5 + 2.5 + 4), not added once.",
                            "expect": 3.75}],
        "chart": area_chart([0, 0.5, 1, 1.5, 2], [1, 1.5, 2.5, 4, 6]),
        "guided_steps": trap_steps(0.5, [1, 1.5, 2.5, 4, 6])},
]

# Fix em dashes in preserved worked_examples labels (student-facing, validator-enforced)
for we in base.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pb = base["problem_bank"]
pb["bronze"], pb["silver"], pb["gold"] = bronze, silver, gold
pb["bronze_description"] = "Bronze: find a gradient from two points, or the area of one simple shape."
pb["silver_description"] = "Silver: apply the trapezium rule across a few strips, and read what a gradient tells you."
pb["gold_description"] = "Gold: estimate areas and curve gradients in real contexts, then judge the accuracy."

# ---------- tier_guides ----------
base["tier_guides"] = {
    "bronze": {
        "title": "Bronze: gradient from two points, area of one shape",
        "steps": [
            "Gradient means steepness. Pick two points the line goes through. Gradient = (change in \\(y\\)) ÷ (change in \\(x\\)), often called <strong>rise over run</strong>.",
            "Uphill left to right is a positive gradient, downhill is negative, and a flat line is 0.",
            "For a simple area use the shape: rectangle = base × height, triangle = ½ × base × height, trapezium = ½(a + b) × height."],
        "example": {"question": "A tangent passes through (1, 2) and (5, 10). Find the gradient.",
                    "steps": [
                        {"label": "Rise", "content": "<p>change in \\(y\\) = 10 − 2 = 8</p>"},
                        {"label": "Run", "content": "<p>change in \\(x\\) = 5 − 1 = 4</p>"},
                        {"label": "Divide", "content": "<p>gradient = 8 ÷ 4 = 2</p>"},
                        {"label": "Check", "content": "<p>Line climbs 2 for every 1 across. ✓</p>"},
                        {"label": "Answer", "content": "<p>Gradient = 2</p>", "isAnswer": True, "is_answer": True}]}},
    "silver": {
        "title": "Silver: the trapezium rule across several strips",
        "steps": [
            "Split the area under a curve into vertical strips of equal width \\(h\\). Read the height (\\(y\\)-value) at each strip edge.",
            "Trapezium rule: \\(A \\approx \\frac{h}{2}[y_0 + y_n + 2(\\text{the inside } y\\text{-values})]\\). Ends count once, every inside height counts twice.",
            "A gradient of 0 means a flat tangent: a turning point, a peak or a valley."],
        "example": {"question": "Trapezium rule with h = 1 and y-values 1, 3, 6. Find the area.",
                    "steps": [
                        {"label": "Ends", "content": "<p>\\(y_0 + y_n\\) = 1 + 6 = 7</p>"},
                        {"label": "Inside", "content": "<p>2 × 3 = 6</p>"},
                        {"label": "Combine", "content": "<p>\\(\\frac{1}{2}\\)[7 + 6] = \\(\\frac{1}{2}\\)(13) = 6.5</p>"},
                        {"label": "Check", "content": "<p>Small area under a rising curve, 6.5 is sensible. ✓</p>"},
                        {"label": "Answer", "content": "<p>Area ≈ 6.5 square units</p>", "isAnswer": True, "is_answer": True}]}},
    "gold": {
        "title": "Gold: areas and curve gradients in real contexts",
        "steps": [
            "For many strips: add every inside \\(y\\)-value once, double that total, then add the two ends. Multiply by \\(\\frac{h}{2}\\).",
            "Under a speed-time graph the area is the distance; the gradient is the acceleration.",
            "To estimate a curve's gradient at a point, take a point just before and just after, then find rise ÷ run between them."],
        "example": {"question": "Estimate the gradient of y = x squared at x = 3 using (2.9, 8.41) and (3.1, 9.61).",
                    "steps": [
                        {"label": "Rise", "content": "<p>9.61 − 8.41 = 1.2</p>"},
                        {"label": "Run", "content": "<p>3.1 − 2.9 = 0.2</p>"},
                        {"label": "Divide", "content": "<p>1.2 ÷ 0.2 = 6</p>"},
                        {"label": "Check", "content": "<p>Exact gradient \\(2x\\) = 6 at x = 3. ✓</p>"},
                        {"label": "Answer", "content": "<p>Gradient ≈ 6</p>", "isAnswer": True, "is_answer": True}]}},
}

# ---------- guided (opener + teach) ----------
base["guided"] = {
    "opener": {
        "label": "Before any formulas",
        "display": SVG_OPENER + "A car drives at a steady 6 metres per second for 4 seconds.",
        "steps": [
            {"say": "Just read the graph. The speed is flat at 6 m/s and the time is 4 s.",
             "pre": "How far does it go? 6 × 4 = ", "post": " metres", "answer": 24,
             "hint": "Distance at a steady speed is speed × time: 6 × 4."},
            {"say": "You just found the <strong>area</strong> of the rectangle under the graph (height 6 × width 4). Area under a speed-time graph = distance. Now the car speeds up: from 0 to 10 m/s in 2 seconds.",
             "pre": "How much does the speed rise each second? 10 ÷ 2 = ", "post": " m/s", "answer": 5,
             "hint": "Change in speed ÷ time taken: 10 ÷ 2."},
            {"say": "That rate, 5 m/s per second, is the <strong>gradient</strong> (steepness) of the line: rise ÷ run. Two ideas, both just reading a graph: the <strong>area</strong> underneath gives the total, and the <strong>gradient</strong> gives the rate at each moment. That is the whole lesson."}]},
    "teach": {
        "bronze": {
            "display": "Find the gradient of a tangent through \\((2, 3)\\) and \\((6, 15)\\).",
            "label": "Together: your first gradient",
            "steps": [
                {"say": "Gradient is rise over run. Find the rise (the change in y):",
                 "pre": "15 − 3 = ", "post": "", "answer": 12, "hint": "Subtract the y-values."},
                {"pre": "run: 6 − 2 = ", "post": "", "answer": 4, "hint": "Subtract the x-values."},
                {"say": "Gradient = rise ÷ run:", "pre": "12 ÷ 4 = ", "post": "", "answer": 3,
                 "done": "The line climbs 3 for every 1 across.", "hint": "Divide the rise by the run."},
                {"say": "Check: from (2, 3), moving 4 across climbs 4 × 3 = 12:",
                 "pre": "3 + 12 = ", "post": "", "answer": 15,
                 "done": "Back to (6, 15). Gone.", "hint": "Add the rise 12 to the start y-value 3."}]},
        "silver": {
            "display": "Trapezium rule with \\(h = 2\\) and y-values 3, 7, 9, 12. Find the area.",
            "label": "Together: your first trapezium rule",
            "chart": area_chart([0, 2, 4, 6], [3, 7, 9, 12]),
            "steps": [
                {"say": "Add the two end heights first:",
                 "pre": "3 + 12 = ", "post": "", "answer": 15, "hint": "First y-value plus last y-value."},
                {"say": "Add the inside heights and double them:",
                 "pre": "2 × (7 + 9) = ", "post": "", "answer": 32, "hint": "7 + 9 = 16, then double."},
                {"pre": "15 + 32 = ", "post": "", "answer": 47, "hint": "Add the two parts."},
                {"say": "Multiply by h ÷ 2 = 2 ÷ 2 = 1:", "pre": "1 × 47 = ", "post": "", "answer": 47,
                 "done": "Area ≈ 47 square units. Gone.", "hint": "h ÷ 2 is 1, so the total is unchanged."}]},
        "gold": {
            "display": "Estimate the gradient of \\(y = x^2\\) at \\(x = 4\\) using \\((3.9, 15.21)\\) and \\((4.1, 16.81)\\).",
            "label": "Together: a curve's gradient",
            "chart": parab_chart(),
            "steps": [
                {"say": "Use a chord between the two nearby points. Find the rise:",
                 "pre": "16.81 − 15.21 = ", "post": "", "answer": 1.6, "hint": "Subtract the y-values."},
                {"pre": "run: 4.1 − 3.9 = ", "post": "", "answer": 0.2, "hint": "Subtract the x-values."},
                {"say": "Gradient = rise ÷ run:", "pre": "1.6 ÷ 0.2 = ", "post": "", "answer": 8,
                 "done": "The curve's gradient at x = 4 is about 8.", "hint": "Divide 1.6 by 0.2."},
                {"say": "Check against the exact gradient \\(2x\\) at x = 4:",
                 "pre": "2 × 4 = ", "post": "", "answer": 8,
                 "done": "Matches the estimate. Gone.", "hint": "Two fours."}]},
    },
}

# ---------- method_card (trim to 4 steps) ----------
base["method_card"]["steps"] = [
    "Gradient: draw a tangent at the point, pick two clear points on it, then use rise ÷ run.",
    "Area: split the region into vertical strips of equal width \\(h\\).",
    "Trapezium rule: \\(A \\approx \\frac{h}{2}[y_0 + y_n + 2(\\text{inside } y\\text{-values})]\\).",
    "More strips give a better estimate."]

io.open("lesson_%s.json" % KEY, "w", encoding="utf-8").write(json.dumps(base, ensure_ascii=False, indent=1))
print("written lesson_%s.json" % KEY)
