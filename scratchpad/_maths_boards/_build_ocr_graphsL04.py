# -*- coding: utf-8 -*-
"""Build guided-learning + diagrams practice_data for maths-ocr graphs-L04
(Real-Life Graphs). Repairs bank (3 dup fixes + 1 mis-posed replace), adds
opener/teach/tier_guides/guided_steps/hints/expects, and figures."""
import json, io

MINUS = "−"  # unicode minus, not em dash

# ---------------------------------------------------------------- SVG helper
def axis_svg(points, xticks, yticks, xlabel, ylabel, aria, color="#dc2626"):
    xmax = max(xticks); ymax = max(yticks)
    def xp(t): return 40 + (t / xmax) * 190.0
    def yp(v): return 165 - (v / ymax) * 140.0
    def fmt(n): return str(int(n)) if float(n).is_integer() else str(n)
    s = ['<svg viewBox="0 0 260 200" role="img" aria-label="%s" '
         'style="max-width:260px" font-family="Inter, sans-serif">' % aria]
    s.append('<line x1="40" y1="25.0" x2="40" y2="165.0" stroke="currentColor" stroke-width="1.2"/>')
    s.append('<line x1="40" y1="165.0" x2="230.0" y2="165.0" stroke="currentColor" stroke-width="1.2"/>')
    for yt in yticks:
        y = yp(yt)
        s.append('<line x1="37" y1="%.1f" x2="40" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (y, y))
        s.append('<text x="33" y="%.1f" font-size="9" fill="currentColor" text-anchor="end">%s</text>' % (y + 3, fmt(yt)))
    for xt in xticks:
        x = xp(xt)
        s.append('<line x1="%.1f" y1="165.0" x2="%.1f" y2="168.0" stroke="currentColor" stroke-width="1"/>' % (x, x))
        s.append('<text x="%.1f" y="179" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (x, fmt(xt)))
    pts = " ".join("%.1f,%.1f" % (xp(t), yp(v)) for t, v in points)
    s.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2"/>' % (pts, color))
    for t, v in points:
        s.append('<circle cx="%.1f" cy="%.1f" r="2.5" fill="%s"/>' % (xp(t), yp(v), color))
    s.append('<text x="135" y="195" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % xlabel)
    s.append('<text x="12" y="95" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 95)">%s</text>' % ylabel)
    s.append('</svg>')
    return "".join(s)

def chart_line(points, xmax, xstep, ymax, ystep, xtitle, ytitle, color="#3b82f6"):
    return {
        "type": "scatter",
        "data": {"datasets": [{
            "type": "line",
            "data": [{"x": t, "y": v} for t, v in points],
            "tension": 0, "fill": False, "borderColor": color,
            "pointRadius": 4, "pointBackgroundColor": color}]},
        "options": {"scales": {
            "x": {"min": 0, "max": xmax, "ticks": {"stepSize": xstep},
                  "grid": {"color": "rgba(0,0,0,0.05)"},
                  "title": {"text": xtitle, "display": True}},
            "y": {"min": 0, "max": ymax, "ticks": {"stepSize": ystep},
                  "grid": {"color": "rgba(0,0,0,0.08)"},
                  "title": {"text": ytitle, "display": True}, "beginAtZero": True}}}}

# --------------------------------------------------------- load live, preserve
pd = json.load(io.open("_gL04_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

def mc(pattern, message, expect):
    return {"check": "common", "pattern": pattern, "message": message, "expect": expect}

# ============================================================ BRONZE
b = pb["bronze"]
# keep existing distance-time chart for B0/B1
dt_chart = b[0]["chart"]

b[0].update({
    "hint": "The distance is the height of the line; read it at the time given.",
    "misconceptions": [mc("wrong_reading",
        "At t = 2 hours the line sits at 60 km. Reading its final height at t = 4 gives 90 km, which is the whole journey, not the first 2 hours.", 90)],
    "guided_steps": [
        {"say": "The distance travelled is the height of the line. Read it at the time you are asked for."},
        {"pre": "Read the height at time = 1 hour: ", "post": " km", "answer": 30, "hint": "Follow the line up to t = 1."},
        {"pre": "Read the height at time = 2 hours: ", "post": " km", "answer": 60, "hint": "Follow the line up to t = 2.", "phase": "substitute"},
        {"pre": "So the distance in the first 2 hours is ", "post": " km", "answer": 60, "hint": "It is the height you just read at t = 2.",
         "done": "The graph reads 60 km at 2 hours, so that is the distance travelled."}]})

b[1].update({
    "hint": "A stop is a flat, horizontal section; measure how long it lasts.",
    "misconceptions": [mc("wrong_reading",
        "The flat section runs from t = 2 to t = 3, so the stop lasts 3 " + MINUS + " 2 = 1 hour. Writing 3 reads the end time, not the length.", 3)],
    "guided_steps": [
        {"say": "A stop shows up as a flat, horizontal section: the distance is not changing."},
        {"pre": "The flat part starts at time = ", "post": " hours", "answer": 2, "hint": "Read where the line first goes flat."},
        {"pre": "The flat part ends at time = ", "post": " hours", "answer": 3, "hint": "Read where the line starts climbing again.", "phase": "substitute"},
        {"pre": "Stop length = 3 " + MINUS + " 2 = ", "post": " hours", "answer": 1, "hint": "Take the start time from the end time."},
        {"pre": "Check: over the flat part the distance stayed at ", "post": " km", "answer": 60, "hint": "Read the height of the flat line.",
         "done": "The distance did not change, so the stop lasted 1 hour."}]})

b[2].update({
    "hint": "Average speed = distance ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Speed = distance ÷ time = 120 ÷ 3 = 40 km/h. Dividing time by distance (3 ÷ 120 = 0.025) is upside down.", 0.025)],
    "guided_steps": [
        {"say": "Average speed is total distance ÷ total time."},
        {"pre": "Write the distance: ", "post": " km", "answer": 120, "hint": "It is given in the question."},
        {"pre": "Divide by the time: 120 ÷ 3 = ", "post": " km/h", "answer": 40, "hint": "Share 120 km over 3 hours.", "phase": "substitute"},
        {"pre": "Check: 40 km/h × 3 h = ", "post": " km", "answer": 120, "hint": "Multiply back to test it.",
         "done": "It returns the 120 km, so 40 km/h is right."}]})

b[3].update({
    "hint": "Distance = speed × time.",
    "misconceptions": [mc("wrong_formula",
        "Distance = speed × time = 15 × 2 = 30 km. Dividing (15 ÷ 2 = 7.5) instead of multiplying is the slip.", 7.5)],
    "guided_steps": [
        {"say": "Distance = speed × time."},
        {"pre": "Write the speed: ", "post": " km/h", "answer": 15, "hint": "It is given in the question."},
        {"pre": "Multiply by the time: 15 × 2 = ", "post": " km", "answer": 30, "hint": "Two hours at 15 km each hour.", "phase": "substitute"},
        {"pre": "Check: 30 km ÷ 2 h = ", "post": " km/h", "answer": 15, "hint": "Divide back to test it.",
         "done": "It returns the 15 km/h, so 30 km is right."}]})

b[4].update({
    "hint": "Speed = distance ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Speed = distance ÷ time = 50 ÷ 2.5 = 20 mph. Dividing time by distance (2.5 ÷ 50 = 0.05) is upside down.", 0.05)],
    "guided_steps": [
        {"say": "Speed = distance ÷ time."},
        {"pre": "Write the distance: ", "post": " miles", "answer": 50, "hint": "It is given in the question."},
        {"pre": "Divide by the time: 50 ÷ 2.5 = ", "post": " mph", "answer": 20, "hint": "Share 50 miles over 2.5 hours.", "phase": "substitute"},
        {"pre": "Check: 20 mph × 2.5 h = ", "post": " miles", "answer": 50, "hint": "Multiply back to test it.",
         "done": "It returns the 50 miles, so 20 mph is right."}]})

# B5 REPLACED (was mis-posed "enter 1 for stationary" duplicating B1's answer of 1)
b[5] = {
    "display": "A conversion graph shows 5 miles ≈ 8 km. Use it to convert 15 miles to kilometres.",
    "solutions": [24],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Miles are the bigger unit, so scale up: find the km in 1 mile first.",
    "misconceptions": [mc("wrong_direction",
        "5 miles is 8 km, so 1 mile is 8 ÷ 5 = 1.6 km, and 15 × 1.6 = 24 km. Going the wrong way (15 ÷ 8 × 5 = 9.375) gives fewer km than miles, which is impossible.", 9.375)],
    "guided_steps": [
        {"say": "Miles are bigger than kilometres, so the km number will be larger. Find the km in one mile first."},
        {"pre": "Kilometres in 1 mile: 8 ÷ 5 = ", "post": " km", "answer": 1.6, "hint": "Divide 8 by 5."},
        {"pre": "15 miles × 1.6 = ", "post": " km", "answer": 24, "hint": "Multiply the miles by 1.6.", "phase": "substitute"},
        {"pre": "Check: 24 ÷ 1.6 = ", "post": " miles", "answer": 15, "hint": "Divide back to test it.",
         "done": "It returns the 15 miles, so 24 km is right."}]}

b[6].update({
    "hint": "Speed = distance ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Speed = distance ÷ time = 800 ÷ 200 = 4 m/s. Dividing time by distance (200 ÷ 800 = 0.25) is upside down.", 0.25)],
    "guided_steps": [
        {"say": "Speed = distance ÷ time."},
        {"pre": "Write the distance: ", "post": " m", "answer": 800, "hint": "It is given in the question."},
        {"pre": "Divide by the time: 800 ÷ 200 = ", "post": " m/s", "answer": 4, "hint": "Share 800 m over 200 seconds.", "phase": "substitute"},
        {"pre": "Check: 4 m/s × 200 s = ", "post": " m", "answer": 800, "hint": "Multiply back to test it.",
         "done": "It returns the 800 m, so 4 m/s is right."}]})

b[7].update({
    "hint": "Distance = speed × time.",
    "misconceptions": [mc("wrong_formula",
        "Distance = speed × time = 60 × 1.5 = 90 miles. Dividing (60 ÷ 1.5 = 40) instead of multiplying is the slip.", 40)],
    "guided_steps": [
        {"say": "Distance = speed × time."},
        {"pre": "Write the speed: ", "post": " mph", "answer": 60, "hint": "It is given in the question."},
        {"pre": "Multiply by the time: 60 × 1.5 = ", "post": " miles", "answer": 90, "hint": "60 miles each hour for 1.5 hours.", "phase": "substitute"},
        {"pre": "Check: 90 miles ÷ 1.5 h = ", "post": " mph", "answer": 60, "hint": "Divide back to test it.",
         "done": "It returns the 60 mph, so 90 miles is right."}]})

# ============================================================ SILVER
s = pb["silver"]

s[0].update({
    "hint": "Acceleration is the gradient: change in speed ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Acceleration = change in speed ÷ time = 25 ÷ 5 = 5 m/s². Dividing time by the speed change (5 ÷ 25 = 0.2) is upside down.", 0.2)],
    "guided_steps": [
        {"say": "Acceleration is the gradient of a speed-time graph: change in speed ÷ time."},
        {"pre": "Change in speed = 25 " + MINUS + " 0 = ", "post": " m/s", "answer": 25, "hint": "The speed rises from 0 to 25."},
        {"pre": "Acceleration = 25 ÷ 5 = ", "post": " m/s²", "answer": 5, "hint": "Divide the speed gain by the time.", "phase": "substitute"},
        {"pre": "Check: 5 m/s² for 5 s gains 5 × 5 = ", "post": " m/s", "answer": 25, "hint": "Multiply back to test it.",
         "done": "It reaches the 25 m/s, so 5 m/s² is right."}]})

# S1 keep existing speed-time chart [0,10,20,20,20,0]@[0,2,4,6,8,10]
s[1].update({
    "hint": "Split the area into a triangle, a rectangle, then a triangle, and add them.",
    "misconceptions": [mc("area_error",
        "Split the area: triangle 40, rectangle 80, triangle 20, total 140 m. Treating it all as one rectangle (10 × 20) gives 200, too big.", 200)],
    "guided_steps": [
        {"say": "Distance is the area under the line. Split it into a triangle, a rectangle, then a triangle."},
        {"pre": "Triangle while speeding up (0 to 4 s): ½ × 4 × 20 = ", "post": " m", "answer": 40, "hint": "½ × base × height."},
        {"pre": "Rectangle at steady speed (4 to 8 s): 4 × 20 = ", "post": " m", "answer": 80, "hint": "base × height."},
        {"pre": "Triangle while slowing down (8 to 10 s): ½ × 2 × 20 = ", "post": " m", "answer": 20, "hint": "½ × base × height.", "phase": "substitute"},
        {"pre": "Total distance = 40 + 80 + 20 = ", "post": " m", "answer": 140, "hint": "Add the three areas."},
        {"pre": "Check: total time = 4 + 4 + 2 = ", "post": " s", "answer": 10, "hint": "Add the three stage times.",
         "done": "140 m over 10 s averages 14 m/s, between 0 and 20, so it is sensible."}]})

# S2 FIXED (was 20->0 in 4s = 5, duplicating S0). New: 24->0 in 3s = 8.
s[2].update({
    "display": "A car decelerates from 24 m/s to 0 in 3 seconds. What is the deceleration in m/s²?",
    "solutions": [8],
    "hint": "Deceleration is the size of the gradient: change in speed ÷ time.",
    "misconceptions": [mc("wrong_formula",
        "Deceleration = 24 ÷ 3 = 8 m/s². Dividing time by the speed change (3 ÷ 24 = 0.125) is upside down.", 0.125)],
    "guided_steps": [
        {"say": "Deceleration is the size of the gradient: how fast the speed drops."},
        {"pre": "Change in speed = 24 " + MINUS + " 0 = ", "post": " m/s", "answer": 24, "hint": "The speed falls from 24 to 0."},
        {"pre": "Deceleration = 24 ÷ 3 = ", "post": " m/s²", "answer": 8, "hint": "Divide the drop by the time.", "phase": "substitute"},
        {"pre": "Check: losing 8 m/s each second for 3 s loses 8 × 3 = ", "post": " m/s", "answer": 24, "hint": "Multiply back to test it.",
         "done": "That is the full 24 m/s, so 8 m/s² is right."}]})

s[3].update({
    "hint": "Speed = distance ÷ time; read the climb off the graph.",
    "misconceptions": [mc("wrong_reading",
        "Speed = distance ÷ time = 90 ÷ 1.5 = 60 km/h. Writing 90 gives the distance, not the speed.", 90)],
    "guided_steps": [
        {"say": "Speed on a distance-time graph is distance ÷ time."},
        {"pre": "Distance climbed = ", "post": " km", "answer": 90, "hint": "The line rises to 90 km."},
        {"pre": "Speed = 90 ÷ 1.5 = ", "post": " km/h", "answer": 60, "hint": "Divide the distance by 1.5 hours.", "phase": "substitute"},
        {"pre": "Check: 60 km/h × 1.5 h = ", "post": " km", "answer": 90, "hint": "Multiply back to test it.",
         "done": "It returns the 90 km, so 60 km/h is right."}]})

s[4].update({
    "hint": "Convert from pounds to euros by multiplying by the rate 1.15.",
    "misconceptions": [mc("wrong_direction",
        "£ to € means multiply by 1.15: 200 × 1.15 = €230. Leaving it as 200 forgets to convert.", 200)],
    "guided_steps": [
        {"say": "To go from pounds to euros, multiply by the exchange rate 1.15."},
        {"pre": "Write the rate: £1 = €", "post": "", "answer": 1.15, "hint": "Read the exchange rate given."},
        {"pre": "200 × 1.15 = ", "post": " euros", "answer": 230, "hint": "Multiply the pounds by 1.15.", "phase": "substitute"},
        {"pre": "Check: 230 ÷ 1.15 = ", "post": " pounds", "answer": 200, "hint": "Divide back to test it.",
         "done": "It returns the £200, so €230 is right."}]})

s[5].update({
    "hint": "A flat speed-time line gives a rectangle: base × height.",
    "misconceptions": [mc("area_error",
        "The speed is constant, so the area is a rectangle: 8 × 15 = 120 m. Using ½ (as for a triangle) gives 60, which is wrong for a flat line.", 60)],
    "guided_steps": [
        {"say": "The line is flat, so the area under it is a rectangle."},
        {"pre": "Write the height (speed): ", "post": " m/s", "answer": 15, "hint": "The speed stays at 15 m/s."},
        {"pre": "Area = base × height = 8 × 15 = ", "post": " m", "answer": 120, "hint": "Base is the 8 seconds.", "phase": "substitute"},
        {"pre": "Check: 120 m ÷ 8 s = ", "post": " m/s", "answer": 15, "hint": "Divide back to test it.",
         "done": "It returns the constant 15 m/s, so 120 m is right."}]})

s[6].update({
    "hint": "Kilometres are smaller than miles, so scale down: find the miles in 1 km first.",
    "misconceptions": [mc("wrong_direction",
        "8 km is 5 miles, so 40 ÷ 8 × 5 = 25 miles. Going the wrong way (40 ÷ 5 × 8 = 64) gives more than the km, impossible since miles are the bigger unit.", 64)],
    "guided_steps": [
        {"say": "Kilometres are smaller than miles, so the miles number will be smaller. Find the miles in one km first."},
        {"pre": "Miles in 1 km: 5 ÷ 8 = ", "post": " miles", "answer": 0.625, "hint": "Divide 5 by 8."},
        {"pre": "40 km × 0.625 = ", "post": " miles", "answer": 25, "hint": "Multiply the km by 0.625.", "phase": "substitute"},
        {"pre": "Check: 25 ÷ 0.625 = ", "post": " km", "answer": 40, "hint": "Divide back to test it.",
         "done": "It returns the 40 km, so 25 miles is right."}]})

# ============================================================ GOLD
g = pb["gold"]

# G0 add speed-time chart (0,0)(4,10)(10,10)(15,0)
g[0]["chart"] = chart_line([(0,0),(4,10),(10,10),(15,0)], 15, 5, 10, 2, "Time (s)", "Speed (m/s)", "#ef4444")
g[0].update({
    "hint": "Split the shape into triangle, rectangle, triangle and add the three areas.",
    "misconceptions": [mc("area_error",
        "½(4)(10) + 6(10) + ½(5)(10) = 20 + 60 + 25 = 105 m. Forgetting the ½ on the sloped parts gives 40 + 60 + 50 = 150.", 150)],
    "guided_steps": [
        {"say": "Distance is the total area. Split the trapezium into two triangles and a rectangle."},
        {"pre": "Speeding-up triangle: ½ × 4 × 10 = ", "post": " m", "answer": 20, "hint": "½ × base × height."},
        {"pre": "Steady rectangle: 6 × 10 = ", "post": " m", "answer": 60, "hint": "base × height, over the 6 s at 10 m/s."},
        {"pre": "Slowing-down triangle: ½ × 5 × 10 = ", "post": " m", "answer": 25, "hint": "½ × base × height.", "phase": "substitute"},
        {"pre": "Total distance = 20 + 60 + 25 = ", "post": " m", "answer": 105, "hint": "Add the three areas."},
        {"pre": "Check: total time = 4 + 6 + 5 = ", "post": " s", "answer": 15, "hint": "Add the three stage times.",
         "done": "105 m over 15 s averages 7 m/s, between 0 and 10, so it is sensible."}]})

g[1].update({
    "hint": "Time to stop = speed ÷ deceleration; the steady part does not matter.",
    "misconceptions": [mc("wrong_formula",
        "Time = speed ÷ deceleration = 30 ÷ 6 = 5 s. Multiplying (30 × 6 = 180) instead of dividing is the slip.", 180)],
    "guided_steps": [
        {"say": "The 10 s at steady speed does not affect the stopping time. Only the deceleration does."},
        {"pre": "Speed it must lose = ", "post": " m/s", "answer": 30, "hint": "It slows from 30 m/s to 0."},
        {"pre": "Time = speed ÷ deceleration = 30 ÷ 6 = ", "post": " s", "answer": 5, "hint": "Divide the speed by the deceleration.", "phase": "substitute"},
        {"pre": "Check: losing 6 m/s each second for 5 s loses 6 × 5 = ", "post": " m/s", "answer": 30, "hint": "Multiply back to test it.",
         "done": "That is the full 30 m/s, so 5 s is right."}]})

# G2 add distance-time chart (0,0)(2,40)(3,40)(5,100)
g[2]["chart"] = chart_line([(0,0),(2,40),(3,40),(5,100)], 5, 1, 100, 20, "Time (hours)", "Distance (km)", "#3b82f6")
g[2].update({
    "hint": "Speed is the gradient of the last section: change in distance ÷ change in time.",
    "misconceptions": [mc("wrong_formula",
        "Speed = change in distance ÷ change in time = (100 " + MINUS + " 40) ÷ (5 " + MINUS + " 3) = 60 ÷ 2 = 30 km/h. Dividing by the whole time 5 instead of the 2-hour section gives 12.", 12)],
    "guided_steps": [
        {"say": "Speed on a distance-time graph is the gradient. Use only the final section, from t = 3 to t = 5."},
        {"pre": "Change in distance: 100 " + MINUS + " 40 = ", "post": " km", "answer": 60, "hint": "Subtract the distances at the two ends."},
        {"pre": "Change in time: 5 " + MINUS + " 3 = ", "post": " hours", "answer": 2, "hint": "Subtract the times."},
        {"pre": "Speed = 60 ÷ 2 = ", "post": " km/h", "answer": 30, "hint": "Divide the distance change by the time change.", "phase": "substitute"},
        {"pre": "Check: 30 km/h for 2 h covers 30 × 2 = ", "post": " km", "answer": 60, "hint": "Multiply back to test it.",
         "done": "That matches the 60 km climb, so 30 km/h is right."}]})

# G3 add SVG triangle (reverse area: base 8, height v, area 80)
g3_svg = ('<svg viewBox="0 0 240 180" role="img" aria-label="Speed-time graph: a straight '
          'line rises from the origin at 0 seconds to an unknown speed v at 8 seconds; the '
          'triangular area underneath is 80 metres" style="max-width:240px" font-family="Inter, sans-serif">'
          '<line x1="35" y1="25" x2="35" y2="150" stroke="currentColor" stroke-width="1.2"/>'
          '<line x1="35" y1="150" x2="210" y2="150" stroke="currentColor" stroke-width="1.2"/>'
          '<polygon points="35,150 200,150 200,40" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>'
          '<line x1="35" y1="150" x2="200" y2="40" stroke="#dc2626" stroke-width="2"/>'
          '<line x1="200" y1="40" x2="35" y2="40" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,3"/>'
          '<text x="30" y="44" font-size="11" fill="currentColor" text-anchor="end">v</text>'
          '<line x1="35" y1="153" x2="200" y2="153" stroke="currentColor" stroke-width="0.8"/>'
          '<text x="117" y="166" font-size="10" fill="currentColor" text-anchor="middle">8 s</text>'
          '<text x="140" y="120" font-size="10" fill="currentColor" text-anchor="middle">area = 80 m</text>'
          '<text x="120" y="178" font-size="10" fill="currentColor" text-anchor="middle">Time (s)</text>'
          '<text x="12" y="88" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 88)">Speed (m/s)</text>'
          '</svg>')
g[3]["display"] = g3_svg + '<p>A speed-time graph shows a car accelerating from rest to speed v in 8 seconds. The distance travelled (the area under the graph) is 80 m. Find v.</p>'
g[3].update({
    "hint": "The area of the triangle is ½ × base × height; set it equal to 80 and solve for v.",
    "misconceptions": [mc("area_error",
        "½ × 8 × v = 80, so 4v = 80 and v = 20 m/s. Forgetting the ½ gives 80 ÷ 8 = 10, too small.", 10)],
    "guided_steps": [
        {"say": "The distance is the area of the triangle: ½ × base × height. Here the height is the unknown speed v."},
        {"pre": "½ × 8 = ", "post": "", "answer": 4, "hint": "Half of the base 8."},
        {"pre": "4 × v = 80, so v = 80 ÷ 4 = ", "post": " m/s", "answer": 20, "hint": "Divide 80 by 4.", "phase": "substitute"},
        {"pre": "Check: ½ × 8 × 20 = ", "post": " m", "answer": 80, "hint": "Put v = 20 back into the area.",
         "done": "It gives the 80 m area, so v = 20 m/s is right."}]})

# G4 FIXED (was 3 m/s^2 for 10s = 30, duplicating G2). New: 4 m/s^2 for 10s = 40.
g[4].update({
    "display": "A car accelerates from rest at 4 m/s² for 10 seconds. What is the final speed?",
    "solutions": [40],
    "hint": "Final speed = acceleration × time when starting from rest.",
    "misconceptions": [mc("wrong_formula",
        "Final speed = acceleration × time = 4 × 10 = 40 m/s. Dividing (10 ÷ 4 = 2.5) instead of multiplying is the slip.", 2.5)],
    "guided_steps": [
        {"say": "Final speed = start speed + acceleration × time. From rest means the start speed is 0."},
        {"pre": "Speed gained = acceleration × time = 4 × 10 = ", "post": " m/s", "answer": 40, "hint": "Multiply the acceleration by the time."},
        {"pre": "Final speed = 0 + 40 = ", "post": " m/s", "answer": 40, "hint": "Add the gain to the start speed of 0.", "phase": "substitute"},
        {"pre": "Check: gaining 4 m/s each second for 10 s gives 4 × 10 = ", "post": " m/s", "answer": 40, "hint": "Multiply back to confirm.",
         "done": "That is the 40 m/s, so the final speed is right."}]})

# ============================================================ descriptions
pb["bronze_description"] = "Read distance-time graphs and use speed = distance ÷ time with matching units."
pb["silver_description"] = "Read speed-time graphs for acceleration and area, plus unit and currency conversions."
pb["gold_description"] = "Multi-stage speed-time journeys, reverse area problems, and reading a single graph section."

# ============================================================ tier_guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: speed, distance and time",
        "steps": [
            "<strong>Speed = distance ÷ time.</strong> Rearranged: distance = speed × time, and time = distance ÷ speed.",
            "On a distance-time graph the height is the distance, a <strong>flat line</strong> means stopped, and a steeper line means faster.",
            "Keep units matched: km with hours gives km/h."],
        "example": {"question": "A car travels 150 km in 3 hours. Find its speed.",
            "steps": [
                {"label": "Formula", "content": "speed = distance ÷ time"},
                {"label": "Substitute", "content": "= 150 ÷ 3"},
                {"label": "Speed", "content": "= 50 km/h", "isAnswer": True, "is_answer": True}]}},
    "silver": {
        "title": "Silver: speed-time graphs and conversions",
        "steps": [
            "On a <strong>speed-time</strong> graph the gradient is the <strong>acceleration</strong>: change in speed ÷ time.",
            "The <strong>area under</strong> a speed-time graph is the <strong>distance</strong>. Split it into triangles and rectangles.",
            "For conversions, scale the right way: miles are bigger than km, and pounds are worth more than euros here."],
        "example": {"question": "A car speeds up from 0 to 18 m/s in 6 s. Find the acceleration.",
            "steps": [
                {"label": "Gradient", "content": "(18 − 0) ÷ 6"},
                {"label": "Acceleration", "content": "= 3 m/s²", "isAnswer": True, "is_answer": True}]}},
    "gold": {
        "title": "Gold: multi-stage journeys",
        "steps": [
            "Break a journey into stages: speeding up, steady, slowing down. Work out each stage on its own.",
            "For total distance, add the area of every stage: two triangles and a rectangle for a trapezium.",
            "To find a missing speed from a known area, write ½ × base × height = area and solve."],
        "example": {"question": "A bus goes 0 to 16 m/s in 4 s, then holds 16 m/s for 6 s. Total distance?",
            "steps": [
                {"label": "Triangle", "content": "½ × 4 × 16 = 32"},
                {"label": "Rectangle", "content": "16 × 6 = 96"},
                {"label": "Total", "content": "= 128 m", "isAnswer": True, "is_answer": True}]}}}

# ============================================================ guided (opener + teach)
opener_svg = axis_svg(
    [(0,0),(1,30),(2,30),(3,0)], [0,1,2,3], [0,10,20,30,40],
    "Time (hours)", "Distance (km)",
    "Distance-time graph of Maya's drive: distance from home rises from 0 to 30 km over the first hour, stays at 30 km from 1 to 2 hours, then falls back to 0 by 3 hours",
    "#dc2626")

teach_silver_svg = axis_svg(
    [(0,0),(4,16),(12,16)], [0,2,4,6,8,10,12], [0,4,8,12,16,20],
    "Time (s)", "Speed (m/s)",
    "Speed-time graph of a motorbike: speed rises from 0 to 16 metres per second over the first 4 seconds, then stays at 16 metres per second until 12 seconds",
    "#dc2626")

teach_gold_svg = axis_svg(
    [(0,0),(4,20),(14,20),(20,0)], [0,4,8,12,16,20], [0,5,10,15,20],
    "Time (s)", "Speed (m/s)",
    "Speed-time graph of a tram forming a trapezium: speed rises from 0 to 20 metres per second over 4 seconds, stays at 20 until 14 seconds, then falls back to 0 by 20 seconds",
    "#dc2626")

pd["guided"] = {
    "opener": {
        "display": opener_svg + "<p>The graph shows Maya's drive to her aunt's house and back. Distance from home is up the side, time in hours along the bottom.</p>",
        "steps": [
            {"pre": "How far away is the aunt's house? Read the highest the line reaches: ", "post": " km", "answer": 30, "hint": "The line climbs, then flattens. Read that flat height."},
            {"pre": "Maya rested while the line is flat, from 1 hour to 2 hours. How many hours is that? ", "post": " hours", "answer": 1, "hint": "Take the start time from the end time of the flat part: 2 − 1."},
            {"pre": "The whole trip finishes when the line reaches 0 again. At what time, in hours? ", "post": " hours", "answer": 3, "hint": "Read the time where the line touches the bottom on the right."},
            {"say": "You just read a <strong>distance-time graph</strong> by common sense. The height is distance from home, a <strong>flat line means not moving</strong>, and a steeper slope means going faster. That slope is the <strong>speed</strong>. Speed-time graphs work the same way, and their <strong>area</strong> gives the distance. That is the whole of today's lesson."}]},
    "teach": {
        "bronze": {
            "display": "A van drives 90 km in 2 hours at a steady speed, then carries on for 3 more hours at the same speed. How far does it travel in total?",
            "steps": [
                {"say": "Steady speed means we can find one speed and reuse it for the rest of the trip."},
                {"pre": "Speed = distance ÷ time = 90 ÷ 2 = ", "post": " km/h", "answer": 45, "hint": "Divide the distance by the time."},
                {"pre": "At that speed each hour covers ", "post": " km", "answer": 45, "hint": "At 45 km/h you go 45 km every hour."},
                {"pre": "In 3 more hours: 45 × 3 = ", "post": " km", "answer": 135, "hint": "Multiply the speed by 3 hours."},
                {"pre": "Total distance = 90 + 135 = ", "post": " km", "answer": 225, "hint": "Add the first part to the extra part.",
                 "done": "Same speed throughout, so the distances just add up. That was the whole point."}]},
        "silver": {
            "display": teach_silver_svg + "<p>The speed-time graph shows a motorbike. It speeds up from rest to 16 m/s in 4 s, then holds 16 m/s until 12 s. Find the total distance.</p>",
            "steps": [
                {"say": "On a speed-time graph the <strong>area under the line</strong> is the distance. Split it into a triangle and a rectangle."},
                {"pre": "Acceleration = (16 − 0) ÷ 4 = ", "post": " m/s²", "answer": 4, "hint": "Gradient is change in speed over time."},
                {"pre": "Triangle while speeding up: ½ × 4 × 16 = ", "post": " m", "answer": 32, "hint": "Area of a triangle is ½ × base × height."},
                {"pre": "Rectangle at steady speed: 8 × 16 = ", "post": " m", "answer": 128, "hint": "The steady part lasts from 4 s to 12 s, that is 8 s."},
                {"pre": "Total distance = 32 + 128 = ", "post": " m", "answer": 160, "hint": "Add the two areas.",
                 "done": "Area under the graph is the distance. That was the whole point."}]},
        "gold": {
            "display": teach_gold_svg + "<p>A tram speeds up from rest to 20 m/s in 4 s, holds 20 m/s for 10 s, then slows to rest in 6 s. Find the total distance.</p>",
            "steps": [
                {"say": "A trapezium splits into two triangles and a rectangle. Find each area, then add."},
                {"pre": "Speeding-up triangle: ½ × 4 × 20 = ", "post": " m", "answer": 40, "hint": "½ × base × height."},
                {"pre": "Steady rectangle: 10 × 20 = ", "post": " m", "answer": 200, "hint": "base × height, over the 10 s at 20 m/s."},
                {"pre": "Slowing-down triangle: ½ × 6 × 20 = ", "post": " m", "answer": 60, "hint": "½ × base × height."},
                {"pre": "Total distance = 40 + 200 + 60 = ", "post": " m", "answer": 300, "hint": "Add all three areas.",
                 "done": "Every stage's area adds to the total distance. That was the whole point."}]}}}

# ============================================================ method_card trim to 4 steps
pd["method_card"]["steps"] = [
    "Check the axes first: distance-time or speed-time?",
    "Distance-time: the gradient is the speed; a flat line means stopped.",
    "Speed-time: the gradient is the acceleration; the area underneath is the distance.",
    "Match the units before dividing: turn minutes into hours."]

# ------------------------------------- fix em dashes in preserved worked_examples labels
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------------------------------------------------------------- write shard
io.open("lesson_maths-ocr_graphs-L04.json", "w", encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("shard written")
