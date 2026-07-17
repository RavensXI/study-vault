# -*- coding: utf-8 -*-
import json, io, math

# ---------- SVG helpers (theme-safe: currentColor, soft fills, Inter) ----------
def P(cx, cy, r, ang):
    return (cx + r*math.cos(math.radians(ang)), cy - r*math.sin(math.radians(ang)))

def arc(cx, cy, r, a1, a2, n=10):
    pts = []
    for i in range(n+1):
        a = a1 + (a2-a1)*i/n
        x, y = P(cx, cy, r, a)
        pts.append(f"{x:.1f},{y:.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="currentColor" stroke-width="1"/>'

def T(x, y, s, size=11):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,sans-serif" font-size="{size}" fill="currentColor" text-anchor="middle">{s}</text>'

def L(x1, y1, x2, y2, w=1.5):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="{w}"/>'

def wrap(vb_w, vb_h, aria, body):
    return (f'<svg viewBox="0 0 {vb_w} {vb_h}" role="img" aria-label="{aria}">'
            f'{body}</svg>')

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def fig_line(known, unk="x"):
    cx, cy = 120, 90
    theta = 180 - known
    ex, ey = P(cx, cy, 78, theta)
    lx, ly = P(cx, cy, 46, (theta+180)/2)
    rx, ry = P(cx, cy, 46, theta/2)
    body = (L(25, cy, 215, cy) + L(cx, cy, ex, ey)
            + arc(cx, cy, 26, theta, 180) + arc(cx, cy, 26, 0, theta)
            + f'<circle cx="{cx}" cy="{cy}" r="2" fill="currentColor"/>'
            + T(lx, ly+4, f"{known}°") + T(rx, ry+4, f"{unk}°"))
    aria = f"A straight line split by a ray into an angle of {known} degrees and an unknown angle {unk}."
    return wrap(240, 120, aria, body)

def fig_point(vals, labels, aria):
    cx, cy = 120, 82
    start = 18
    dirs = [start]
    for v in vals:
        dirs.append(dirs[-1] + v)
    body = ""
    for d in dirs[:-1]:
        ex, ey = P(cx, cy, 66, d)
        body += L(cx, cy, ex, ey)
    for i, lab in enumerate(labels):
        mid = (dirs[i] + dirs[i+1]) / 2
        r = 40 if (dirs[i+1]-dirs[i]) > 55 else 48
        tx, ty = P(cx, cy, r, mid)
        body += T(tx, ty+4, lab, size=10)
    body += f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="currentColor"/>'
    return wrap(240, 164, aria, body)

def fig_triangle(top, bl, br, iso=False):
    if iso:
        A, B, C = (120, 26), (58, 112), (182, 112)
    else:
        A, B, C = (108, 26), (30, 112), (206, 112)
    body = (L(A[0], A[1], B[0], B[1]) + L(B[0], B[1], C[0], C[1]) + L(C[0], C[1], A[0], A[1]))
    if iso:
        def tick(p, q):
            mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
            dx, dy = q[0]-p[0], q[1]-p[1]
            ln = math.hypot(dx, dy); nx, ny = -dy/ln, dx/ln
            return L(mx-4*nx, my-4*ny, mx+4*nx, my+4*ny, 1.3)
        body += tick(A, B) + tick(A, C)
    body += T(A[0], A[1]+22, top) + T(B[0]+22, B[1]-8, bl) + T(C[0]-22, C[1]-8, br)
    aria = f"A triangle with angles labelled {top}, {bl} and {br}."
    return wrap(240, 130, aria, body)

def fig_vertically_opposite(known, unk="?"):
    cx, cy = 120, 74
    for a in (25, 330):
        pass
    body = ""
    for a in (25, 330):
        p1 = P(cx, cy, 92, a); p2 = P(cx, cy, 92, a+180)
        body += L(p1[0], p1[1], p2[0], p2[1])
    gm = (25 + (-30)) / 2
    gx, gy = P(cx, cy, 50, gm)
    om = (150 + 205) / 2
    ox, oy = P(cx, cy, 50, om)
    body += arc(cx, cy, 30, -30, 25) + arc(cx, cy, 30, 150, 205)
    body += f'<circle cx="{cx}" cy="{cy}" r="2" fill="currentColor"/>'
    body += T(gx, gy+4, f"{known}°") + T(ox, oy+4, f"{unk}")
    aria = f"Two straight lines crossing. One angle is {known} degrees; the vertically opposite angle is marked {unk}."
    return wrap(240, 148, aria, body)

def fig_parallel(l1, l2, relation):
    y1, y2 = 35, 95
    Ux, Lx = 75, 135
    body = (L(20, y1, 220, y1) + L(20, y2, 220, y2)
            + L(Ux-30, y1-30, Lx+30, y2+30))
    def chev(y):
        return (L(150, y-4, 156, y, 1) + L(156, y, 150, y+4, 1)
                + L(158, y-4, 164, y, 1) + L(164, y, 158, y+4, 1))
    body += chev(y1) + chev(y2)
    if relation == "alternate":
        body += T(94, 50, l1, 10) + T(112, 86, l2, 10)
    else:
        body += T(94, 50, l1, 10) + T(152, 86, l2, 10)
    body += f'<circle cx="{Ux}" cy="{y1}" r="2" fill="currentColor"/>'
    body += f'<circle cx="{Lx}" cy="{y2}" r="2" fill="currentColor"/>'
    aria = f"Two parallel lines cut by a transversal, with {relation} angles marked."
    return wrap(240, 130, aria, body)

def fig_polygon(n, aria):
    cx, cy, r = 120, 68, 50
    pts = [P(cx, cy, r, 90 + i*360/n) for i in range(n)]
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    body = f'<polygon points="{d}" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
    return wrap(240, 140, aria, body)

def answer_boxes(steps):
    return [st["answer"] for st in steps if st.get("answer") is not None]

def mc(pattern, expect, message):
    return {"check": pattern, "pattern": pattern, "expect": expect, "message": message}

bronze = [
 {"display": fig_line(72, "x") + "Two angles on a straight line: 72° and \\(x°\\). Find \\(x\\).",
  "solutions": [108], "calculator": False, "input_type": "single_value",
  "hint": "Angles on a straight line add to 180°, so subtract the known angle.",
  "misconceptions": [mc("used_point_total", 288, "A straight line totals 180°, not 360°. Take 72 from 180: 180 − 72 = 108.")],
  "guided_steps": [
    {"say": "Angles on a straight line always add up to 180°. The two angles here fill that straight line."},
    {"pre": "The total to fill for a straight line is ", "post": "°", "answer": 180, "hint": "A straight line is a half turn, which is 180°."},
    {"say": "Now take the angle you know from that total."},
    {"pre": "180 − 72 = ", "post": "°", "answer": 108, "phase": "substitute", "hint": "Subtract 72 from 180."},
    {"pre": "Check: 72 + 108 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "It rebuilds the straight line, so x = 108°.", "hint": "Add your answer to 72; it should give 180."},
  ]},
 {"display": fig_point([90,120,85,65], ["90°","120°","85°","x°"], "Four angles meeting at a point: 90 degrees, 120 degrees, 85 degrees and an unknown angle x.") + "Angles at a point: 90°, 120°, 85°, \\(x°\\). Find \\(x\\).",
  "solutions": [65], "calculator": False, "input_type": "single_value",
  "hint": "The angles around a point add to 360°. Add the three you know, then subtract from 360.",
  "misconceptions": [mc("summed_and_stopped", 295, "295° is the total of the three known angles. The four angles fill a full turn of 360°, so subtract: 360 − 295 = 65.")],
  "guided_steps": [
    {"say": "The angles around a point make a full turn, which is 360°."},
    {"pre": "The total to fill for a point is ", "post": "°", "answer": 360, "hint": "A full turn is 360°."},
    {"say": "Add the three angles you know."},
    {"pre": "90 + 120 + 85 = ", "post": "°", "answer": 295, "hint": "Add them in any order."},
    {"pre": "360 − 295 = ", "post": "°", "answer": 65, "phase": "substitute", "hint": "Subtract the known total from 360."},
    {"pre": "Check: 295 + 65 = ", "post": "°", "answer": 360, "phase": "substitute", "done": "It fills the full turn, so x = 65°.", "hint": "Add your answer to 295; it should give 360."},
  ]},
 {"display": fig_triangle("?", "50°", "70°") + CAP + "A triangle has angles 50° and 70°. Find the third angle.",
  "solutions": [60], "calculator": False, "input_type": "single_value",
  "hint": "The three angles of a triangle add to 180°.",
  "misconceptions": [mc("summed_two", 120, "120° is 50 + 70, the two known angles. The three angles of a triangle add to 180°, so the third is 180 − 120 = 60.")],
  "guided_steps": [
    {"say": "The three angles inside a triangle always add up to 180°."},
    {"pre": "The total for a triangle is ", "post": "°", "answer": 180, "hint": "Every triangle's angles sum to 180°."},
    {"pre": "Add the two you know: 50 + 70 = ", "post": "°", "answer": 120, "hint": "Add the two given angles."},
    {"pre": "180 − 120 = ", "post": "°", "answer": 60, "phase": "substitute", "hint": "Subtract from 180."},
    {"pre": "Check: 50 + 70 + 60 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "All three make 180°, so the third angle is 60°.", "hint": "Add all three; it should give 180."},
  ]},
 {"display": fig_triangle("40°", "?", "?", iso=True) + CAP + "An isosceles triangle has a top angle of 40°. Find each base angle.",
  "solutions": [70], "calculator": False, "input_type": "single_value",
  "hint": "Take the top angle from 180°, then halve, because the two base angles are equal.",
  "misconceptions": [mc("forgot_to_halve", 140, "140° is what the two base angles share between them. They are equal, so each is 140 ÷ 2 = 70.")],
  "guided_steps": [
    {"say": "The two base angles of an isosceles triangle are equal, and all three still add to 180°."},
    {"pre": "First take the top angle from 180: 180 − 40 = ", "post": "°", "answer": 140, "hint": "Subtract the top angle from 180."},
    {"say": "That 140° is shared equally between the two base angles."},
    {"pre": "140 ÷ 2 = ", "post": "°", "answer": 70, "phase": "substitute", "hint": "Halve 140."},
    {"pre": "Check: 40 + 70 + 70 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "The three angles make 180°, so each base angle is 70°.", "hint": "Add the top and both base angles; it should give 180."},
  ]},
 {"display": fig_vertically_opposite(55) + "Two vertically opposite angles: one is 55°. What is the other?",
  "solutions": [55], "calculator": False, "input_type": "single_value",
  "hint": "Vertically opposite angles are equal.",
  "misconceptions": [mc("thought_supplementary", 125, "Vertically opposite angles are equal, not supplementary. The other angle is also 55°. 125° would be the angle next to it on the straight line.")],
  "guided_steps": [
    {"say": "When two straight lines cross, the angles opposite each other are equal."},
    {"pre": "The given angle is 55°, so the vertically opposite one is also ", "post": "°", "answer": 55, "hint": "Vertically opposite angles are equal."},
    {"say": "You can check using the straight line. The angle next door fills the line with 55°."},
    {"pre": "Neighbour on the line: 180 − 55 = ", "post": "°", "answer": 125, "phase": "substitute", "hint": "Subtract 55 from 180."},
    {"pre": "That neighbour is opposite a 125° too, and 125 + 55 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "The pairs 55° and 125° both check out, so the answer is 55°.", "hint": "Add 125 and 55; a straight line is 180."},
  ]},
 {"display": fig_parallel("63°", "?", "alternate") + "Alternate angles on parallel lines: one is 63°. Find the other.",
  "solutions": [63], "calculator": False, "input_type": "single_value",
  "hint": "Alternate angles (the Z shape) are equal.",
  "misconceptions": [mc("thought_supplementary", 117, "Alternate angles (the Z shape) are equal, so the other is 63°. 117° would be a co-interior partner, which is the C shape.")],
  "guided_steps": [
    {"say": "Alternate angles lie on opposite sides of the line crossing the parallels, in a Z shape, and they are equal."},
    {"pre": "The given alternate angle is 63°, so the other is also ", "post": "°", "answer": 63, "hint": "Alternate angles are equal."},
    {"say": "Check with the co-interior angle on the same side, which should add with it to 180°."},
    {"pre": "Co-interior partner: 180 − 63 = ", "post": "°", "answer": 117, "phase": "substitute", "hint": "Subtract 63 from 180."},
    {"pre": "And 117 + 63 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "The C-shape pair makes 180°, confirming the Z-shape pair is 63°.", "hint": "Add 117 and 63; co-interior angles total 180."},
  ]},
 {"display": fig_parallel("105°", "?", "co-interior") + "Co-interior angles on parallel lines: one is 105°. Find the other.",
  "solutions": [75], "calculator": False, "input_type": "single_value",
  "hint": "Co-interior angles (the C shape) add to 180°.",
  "misconceptions": [mc("thought_equal", 105, "Co-interior angles (the C shape) add to 180°, they are not equal. 180 − 105 = 75.")],
  "guided_steps": [
    {"say": "Co-interior angles sit on the same side of the crossing line, in a C shape, and add up to 180°."},
    {"pre": "The total for a co-interior pair is ", "post": "°", "answer": 180, "hint": "Co-interior angles add to 180°."},
    {"pre": "180 − 105 = ", "post": "°", "answer": 75, "phase": "substitute", "hint": "Subtract 105 from 180."},
    {"pre": "Check: 105 + 75 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "The C-shape pair totals 180°, so the other angle is 75°.", "hint": "Add 105 and 75; it should give 180."},
  ]},
 {"display": "Sum of angles in a quadrilateral?",
  "solutions": [360], "calculator": False, "input_type": "single_value",
  "hint": "A quadrilateral is two triangles, so its angles add to 360°.",
  "misconceptions": [mc("used_triangle_total", 180, "180° is a triangle's total. A quadrilateral is two triangles, so 2 × 180 = 360°.")],
  "guided_steps": [
    {"say": "A quadrilateral can be split into two triangles by drawing one diagonal."},
    {"pre": "Each triangle's angles add to ", "post": "°", "answer": 180, "hint": "A triangle is 180°."},
    {"pre": "Two triangles: 2 × 180 = ", "post": "°", "answer": 360, "phase": "substitute", "hint": "Double 180."},
    {"pre": "Check with the formula (4 − 2) × 180 = ", "post": "°", "answer": 360, "phase": "substitute", "done": "Both methods give 360°, the angle sum of any quadrilateral.", "hint": "(n − 2) × 180 with n = 4."},
  ]},
]

silver = [
 {"display": fig_polygon(6, "A regular hexagon.") + "Find the sum of interior angles of a hexagon.",
  "solutions": [720], "calculator": False, "input_type": "single_value",
  "hint": "Use (n − 2) × 180° with n = 6.",
  "misconceptions": [mc("forgot_minus_two", 1080, "The formula is (n − 2) × 180°, not n × 180°. (6 − 2) × 180 = 720.")],
  "guided_steps": [
    {"say": "The interior angles of any polygon add up to (n − 2) × 180°. A hexagon has 6 sides."},
    {"pre": "n − 2 = 6 − 2 = ", "post": "", "answer": 4, "hint": "Take 2 from the number of sides."},
    {"pre": "4 × 180 = ", "post": "°", "answer": 720, "phase": "substitute", "hint": "Multiply by 180."},
    {"pre": "Check: a hexagon splits into 4 triangles, 4 × 180 = ", "post": "°", "answer": 720, "phase": "substitute", "done": "Four triangles of 180° give 720°.", "hint": "Four triangles, each 180°."},
  ]},
 {"display": "Each interior angle of a regular polygon is 120°. How many sides?",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Find the exterior angle first (180° − interior), then divide 360° by it.",
  "misconceptions": [mc("divided_360_by_interior", 3, "Divide 360° by the exterior angle, not the interior. Exterior = 180 − 120 = 60°, and 360 ÷ 60 = 6. Dividing 360 by 120 gives 3, which is wrong.")],
  "guided_steps": [
    {"say": "Work through the exterior angle. Interior and exterior angles on a straight line add to 180°."},
    {"pre": "Exterior angle: 180 − 120 = ", "post": "°", "answer": 60, "hint": "Subtract the interior angle from 180."},
    {"pre": "Exterior angles add to 360°, so sides = 360 ÷ 60 = ", "post": "", "answer": 6, "phase": "substitute", "hint": "Divide 360 by the exterior angle."},
    {"pre": "Check: interior sum = (6 − 2) × 180 = 720, and 720 ÷ 6 = ", "post": "°", "answer": 120, "phase": "substitute", "done": "Each interior angle comes back to 120°, so 6 sides is right.", "hint": "Find the interior sum, then divide by 6."},
  ]},
 {"display": fig_polygon(8, "A regular octagon.") + "Find each exterior angle of a regular octagon.",
  "solutions": [45], "calculator": False, "input_type": "single_value",
  "hint": "Exterior angles add to 360°, so divide 360° by the number of sides.",
  "misconceptions": [mc("used_180", 22.5, "Exterior angles add to 360°, not 180°. 360 ÷ 8 = 45°.")],
  "guided_steps": [
    {"say": "The exterior angles of any polygon always add up to 360°. A regular octagon has 8 equal exterior angles."},
    {"pre": "There are 8 equal exterior angles totalling ", "post": "°", "answer": 360, "hint": "Exterior angles always sum to 360°."},
    {"pre": "360 ÷ 8 = ", "post": "°", "answer": 45, "phase": "substitute", "hint": "Divide 360 by 8."},
    {"pre": "Check: interior angle = 180 − 45 = ", "post": "°", "answer": 135, "phase": "substitute", "done": "Each interior angle is 135°, matching a regular octagon.", "hint": "180 minus the exterior angle."},
  ]},
 {"display": fig_polygon(5, "A regular pentagon.") + "Find each interior angle of a regular pentagon.",
  "solutions": [108], "calculator": False, "input_type": "single_value",
  "hint": "Find the total with (5 − 2) × 180°, then divide by 5.",
  "misconceptions": [mc("gave_the_sum", 540, "540° is the total of all five angles. Each one is 540 ÷ 5 = 108°.")],
  "guided_steps": [
    {"say": "First find the total of all the interior angles with (n − 2) × 180°, then share it equally. A pentagon has 5 sides."},
    {"pre": "Interior sum: (5 − 2) × 180 = 3 × 180 = ", "post": "°", "answer": 540, "hint": "Three lots of 180."},
    {"pre": "Each angle: 540 ÷ 5 = ", "post": "°", "answer": 108, "phase": "substitute", "hint": "Divide the sum by 5."},
    {"pre": "Check: exterior = 180 − 108 = 72, and 72 × 5 = ", "post": "°", "answer": 360, "phase": "substitute", "done": "The exterior angles total 360°, so 108° is correct.", "hint": "Exterior angle times 5 should give 360."},
  ]},
 {"display": fig_parallel("2x°", "(3x+10)°", "co-interior") + "Two angles on parallel lines are co-interior. One is \\(2x°\\) and the other is \\(3x + 10°\\). Find \\(x\\).",
  "solutions": [34], "calculator": False, "input_type": "single_value",
  "hint": "Co-interior angles add to 180°, so form 2x + 3x + 10 = 180.",
  "misconceptions": [mc("set_equal", -10, "Co-interior angles add to 180°, they are not equal. 2x + 3x + 10 = 180, so 5x = 170 and x = 34.")],
  "guided_steps": [
    {"say": "Co-interior angles add to 180°. So 2x + (3x + 10) = 180."},
    {"pre": "Combine the x terms: 2x + 3x = ", "post": "x", "answer": 5, "hint": "Add 2x and 3x."},
    {"pre": "So 5x + 10 = 180. Take 10 from both sides: 180 − 10 = ", "post": "", "answer": 170, "hint": "Subtract 10 from 180."},
    {"pre": "5x = 170, so x = 170 ÷ 5 = ", "post": "", "answer": 34, "phase": "substitute", "hint": "Divide 170 by 5."},
    {"pre": "Check: 2×34 + 3×34 + 10 = 68 + 102 + 10 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "The two angles total 180°, so x = 34.", "hint": "Work out both angles and add; should be 180."},
  ]},
 {"display": "A regular polygon has exterior angles of 24°. How many sides?",
  "solutions": [15], "calculator": False, "input_type": "single_value",
  "hint": "The exterior angles add to 360°, so divide 360° by 24°.",
  "misconceptions": [mc("used_180", 7.5, "Exterior angles total 360°, not 180°. 360 ÷ 24 = 15 sides.")],
  "guided_steps": [
    {"say": "The exterior angles of a polygon add up to 360°, so the number of sides is 360 divided by one exterior angle."},
    {"pre": "The exterior angles total ", "post": "°", "answer": 360, "hint": "Exterior angles always sum to 360°."},
    {"pre": "360 ÷ 24 = ", "post": "", "answer": 15, "phase": "substitute", "hint": "Divide 360 by 24."},
    {"pre": "Check: 15 × 24 = ", "post": "°", "answer": 360, "phase": "substitute", "done": "Fifteen exterior angles of 24° make 360°, so 15 sides.", "hint": "Multiply 15 by 24; should give 360."},
  ]},
 {"display": "The interior angle sum of a polygon is 1440°. How many sides?",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Solve (n − 2) × 180 = 1440 for n.",
  "misconceptions": [mc("forgot_add_two", 8, "1440 ÷ 180 = 8 gives n − 2, not n. Add the 2 back: n = 10.")],
  "guided_steps": [
    {"say": "The interior sum formula is (n − 2) × 180°. Set it equal to 1440 and solve for n."},
    {"pre": "Divide by 180: 1440 ÷ 180 = ", "post": "", "answer": 8, "hint": "How many 180s in 1440?"},
    {"pre": "That 8 equals n − 2, so n = 8 + 2 = ", "post": "", "answer": 10, "phase": "substitute", "hint": "Add 2 to undo the formula."},
    {"pre": "Check: (10 − 2) × 180 = ", "post": "°", "answer": 1440, "phase": "substitute", "done": "Ten sides give an interior sum of 1440°.", "hint": "(n − 2) × 180 with n = 10."},
  ]},
]

gold = [
 {"display": fig_triangle("42°", "65°", "?") + CAP + "A triangle on parallel lines: angle at top = 42°, angle at bottom-left = 65°. Find the angle at bottom-right.",
  "solutions": [73], "calculator": False, "input_type": "single_value",
  "hint": "The three angles of the triangle still add to 180°.",
  "misconceptions": [mc("summed_two", 107, "107° is 42 + 65. The three angles total 180°, so the third is 180 − 107 = 73.")],
  "guided_steps": [
    {"say": "The three angles of any triangle add to 180°, whatever lines it sits on."},
    {"pre": "The total for a triangle is ", "post": "°", "answer": 180, "hint": "A triangle's angles sum to 180°."},
    {"pre": "Add the two known angles: 42 + 65 = ", "post": "°", "answer": 107, "hint": "Add 42 and 65."},
    {"pre": "180 − 107 = ", "post": "°", "answer": 73, "phase": "substitute", "hint": "Subtract from 180."},
    {"pre": "Check: 42 + 65 + 73 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "All three make 180°, so the bottom-right angle is 73°.", "hint": "Add all three; should give 180."},
  ]},
 {"display": fig_point([90,120,150], ["90°","120°","?"], "Three angles meeting at a point where a square and a regular hexagon share a corner: 90 degrees, 120 degrees, and the gap marked with a question mark.") + "Two regular polygons share a side. One is a square, the other a regular hexagon. Find the angle between them at the shared vertex.",
  "solutions": [150], "calculator": False, "input_type": "single_value",
  "hint": "A square angle is 90° and a hexagon angle is 120°. They meet around a point (360°).",
  "misconceptions": [mc("summed_two", 210, "210° is 90 + 120, the two interior angles. They meet at a point (360°), so the gap is 360 − 210 = 150.")],
  "guided_steps": [
    {"say": "The three angles meeting at the shared corner go all the way around a point, which is 360°."},
    {"pre": "A square's interior angle is ", "post": "°", "answer": 90, "hint": "Every angle in a square is 90°."},
    {"pre": "A regular hexagon's interior angle is 720 ÷ 6 = ", "post": "°", "answer": 120, "hint": "Interior sum 720 divided by 6."},
    {"pre": "The gap fills the rest of the point: 360 − 90 − 120 = ", "post": "°", "answer": 150, "phase": "substitute", "hint": "Subtract both known angles from 360."},
    {"pre": "Check: 90 + 120 + 150 = ", "post": "°", "answer": 360, "phase": "substitute", "done": "The three angles make a full turn of 360°, so the gap is 150°.", "hint": "Add all three; should give 360."},
  ]},
 {"display": "Interior angle of a regular polygon is 5× its exterior angle. Find the number of sides.",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Interior and exterior add to 180°, and interior is 5 times the exterior.",
  "misconceptions": [mc("divided_180_by_5", 10, "Interior + exterior = 180°, and interior = 5 × exterior, so 6 × exterior = 180 and exterior = 30°. Sides = 360 ÷ 30 = 12. Dividing 180 by 5 gives 36° and the wrong count.")],
  "guided_steps": [
    {"say": "Interior and exterior angles sit on a straight line, so they add to 180°. Here the interior is 5 times the exterior."},
    {"pre": "Interior is 5 parts, exterior 1 part, so 6 parts make 180. One part (the exterior) = 180 ÷ 6 = ", "post": "°", "answer": 30, "hint": "Divide 180 by 6."},
    {"pre": "Number of sides = 360 ÷ 30 = ", "post": "", "answer": 12, "phase": "substitute", "hint": "Divide 360 by the exterior angle."},
    {"pre": "Check: interior = 5 × 30 = 150, and 150 + 30 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "Interior 150° and exterior 30° make a straight line, so 12 sides.", "hint": "Add interior and exterior; should be 180."},
  ]},
 {"display": fig_triangle("x", "2x", "3x") + CAP + "Angles in a triangle are \\(x\\), \\(2x\\), and \\(3x\\). Find the largest angle.",
  "solutions": [90], "calculator": False, "input_type": "single_value",
  "hint": "Add x + 2x + 3x = 180 to find x, then the largest angle is 3x.",
  "misconceptions": [mc("gave_x", 30, "x = 30, but the question asks for the largest angle, which is 3x = 90°.")],
  "guided_steps": [
    {"say": "The three angles add to 180°. In parts, that is x + 2x + 3x."},
    {"pre": "Total parts: x + 2x + 3x = ", "post": "x", "answer": 6, "hint": "Add the coefficients 1, 2 and 3."},
    {"pre": "So 6x = 180, giving x = 180 ÷ 6 = ", "post": "°", "answer": 30, "hint": "Divide 180 by 6."},
    {"pre": "The largest is 3x = 3 × 30 = ", "post": "°", "answer": 90, "phase": "substitute", "hint": "Multiply x by 3."},
    {"pre": "Check: 30 + 60 + 90 = ", "post": "°", "answer": 180, "phase": "substitute", "done": "The three angles make 180°, and the largest is 90°.", "hint": "Add x, 2x and 3x; should give 180."},
  ]},
 {"display": fig_parallel("(3x−10)°", "(2x+15)°", "alternate") + "Two angles are alternate on parallel lines: \\(3x - 10\\) and \\(2x + 15\\). Find \\(x\\).",
  "solutions": [25], "calculator": False, "input_type": "single_value",
  "hint": "Alternate angles are equal, so set the two expressions equal.",
  "misconceptions": [mc("set_sum_180", 35, "Alternate angles are equal, so 3x − 10 = 2x + 15 giving x = 25. Adding them to 180 (treating them as co-interior) gives x = 35, the wrong rule.")],
  "guided_steps": [
    {"say": "Alternate angles are equal, so set the two expressions equal: 3x − 10 = 2x + 15."},
    {"pre": "Take 2x from both sides: 3x − 2x = ", "post": "x", "answer": 1, "hint": "3x minus 2x."},
    {"pre": "So x − 10 = 15. Add 10 to both sides: 15 + 10 = ", "post": "", "answer": 25, "phase": "substitute", "hint": "Add 10 to 15."},
    {"pre": "Check both angles: 3×25 − 10 = 65 and 2×25 + 15 = ", "post": "°", "answer": 65, "phase": "substitute", "done": "Both work out to 65°, equal as alternate angles should be, so x = 25.", "hint": "Work out 2×25 + 15."},
  ]},
]

bronze_desc = "One angle fact per question: straight lines, points, triangles, and parallel lines. Fill the total, then subtract."
silver_desc = "Polygon angle rules: interior sums, exterior angles, and working backwards to the number of sides."
gold_desc = "Combine several facts or set up an equation: algebraic angles, mixed shapes, and multi-step reasoning."

tier_guides = {
 "bronze": {
   "title": "Bronze: one angle fact",
   "steps": [
     "Spot the total the angles must fill: a straight line is <strong>180°</strong>, angles at a point make <strong>360°</strong>, and a triangle is <strong>180°</strong>.",
     "Add up every angle you already know.",
     "Subtract that from the total to find the missing angle. For equal angles (vertically opposite, alternate) just copy the value across; co-interior angles add to 180°.",
   ],
   "example": {
     "question": "Angles on a straight line: 110° and x°. Find x.",
     "steps": [
       {"label": "Total", "content": "<p>A straight line is 180°.</p>"},
       {"label": "Subtract", "content": "<p>180° − 110° = 70°</p>"},
       {"label": "Check", "content": "<p>110° + 70° = 180° ✓</p>"},
       {"label": "Answer", "content": "<p>x = 70°</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: polygon rules",
   "steps": [
     "Interior angle sum = <strong>(n − 2) × 180°</strong>. For a regular polygon, each interior angle is that sum divided by n.",
     "Exterior angles always add to <strong>360°</strong>, so each exterior angle of a regular polygon is 360° ÷ n.",
     "Interior + exterior = 180°. To find n from an angle, work out the exterior angle, then n = 360° ÷ exterior.",
   ],
   "example": {
     "question": "Find each interior angle of a regular hexagon.",
     "steps": [
       {"label": "Sum", "content": "<p>(6 − 2) × 180° = 720°</p>"},
       {"label": "Divide", "content": "<p>720° ÷ 6 = 120°</p>"},
       {"label": "Check", "content": "<p>Exterior = 180° − 120° = 60°, and 60° × 6 = 360° ✓</p>"},
       {"label": "Answer", "content": "<p>Each interior angle = 120°</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: combine and set up equations",
   "steps": [
     "When angles are given as expressions (like <strong>2x</strong> or <strong>3x + 10</strong>), turn the angle fact into an equation and solve for x.",
     "For mixed shapes, find each known angle, then use angles at a point (360°) or on a line (180°) to reach the unknown.",
     "Always answer the exact question: it may want the largest angle or the number of sides, not x itself.",
   ],
   "example": {
     "question": "A triangle has angles x, x + 30, and x + 60. Find the largest angle.",
     "steps": [
       {"label": "Equation", "content": "<p>x + (x + 30) + (x + 60) = 180</p>"},
       {"label": "Solve", "content": "<p>3x + 90 = 180, so 3x = 90 and x = 30</p>"},
       {"label": "Largest", "content": "<p>x + 60 = 30 + 60 = 90°</p>"},
       {"label": "Check", "content": "<p>30° + 60° + 90° = 180° ✓</p>"},
       {"label": "Answer", "content": "<p>Largest angle = 90°</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

opener = {
  "label": "Before any formulas",
  "display": fig_line(130, "?"),
  "steps": [
    {"say": "Here is a flat, straight line with a pole leaning on it, splitting the flat line into two angles. A straight line is a half turn, worth 180°. The left angle is 130°.",
     "pre": "So the right-hand angle is 180 − 130 = ", "post": "°", "answer": 50,
     "hint": "The two angles fill the straight line, so subtract 130 from 180."},
    {"say": "Now picture turning all the way around in a full circle, like a clock hand going right round to where it started. That whole turn is 360°. Three fence panels meet at the centre: two of them are 150° and 90°.",
     "pre": "The third panel fills the rest: 360 − 150 − 90 = ", "post": "°", "answer": 120,
     "hint": "Take both known angles from 360."},
    {"say": "You just used the only two facts you need to start: angles on a straight line add to <strong>180°</strong>, and angles around a point add to <strong>360°</strong>. Every question in this lesson is the same idea: the angles must fill their total, so add up what you know and subtract. Triangles (180°) and polygons all grow from this."},
  ],
}

teach = {
 "bronze": {
   "label": "Together: your first one",
   "display": fig_point([100,80,95,85], ["100°","80°","95°","t°"], "Four angles meeting at a point: 100 degrees, 80 degrees, 95 degrees and an unknown angle t.") + "Angles at a point: 100°, 80°, 95°, and \\(t°\\). Find \\(t\\).",
   "steps": [
     {"say": "Angles around a point make a full turn of 360°.",
      "pre": "Add the first two known angles: 100 + 80 = ", "post": "°", "answer": 180, "hint": "Start with the first two."},
     {"pre": "180 + 95 = ", "post": "°", "answer": 275, "hint": "Add the third angle."},
     {"pre": "360 − 275 = ", "post": "°", "answer": 85, "hint": "Subtract from 360."},
     {"pre": "Check: 100 + 80 + 95 + 85 = ", "post": "°", "answer": 360, "done": "They fill the whole turn, so t = 85°. That is the whole method: fill the total, subtract what you know.", "hint": "Add all four; should give 360."},
   ],
 },
 "silver": {
   "label": "Together: the silver move",
   "display": fig_polygon(8, "A regular octagon.") + "Find each interior angle of a regular octagon.",
   "steps": [
     {"say": "First find the total of all the interior angles, then share it between the 8 equal angles.",
      "pre": "n − 2 = 8 − 2 = ", "post": "", "answer": 6, "hint": "Take 2 from 8."},
     {"pre": "Interior sum: 6 × 180 = ", "post": "°", "answer": 1080, "hint": "Multiply by 180."},
     {"pre": "Each angle: 1080 ÷ 8 = ", "post": "°", "answer": 135, "hint": "Divide the sum by 8."},
     {"pre": "Check with the exterior angle: 360 ÷ 8 = 45, and 180 − 45 = ", "post": "°", "answer": 135, "done": "Both routes give 135°. That is the polygon method: sum with (n − 2) × 180, then divide.", "hint": "180 minus the exterior angle."},
   ],
 },
 "gold": {
   "label": "Together: the gold move",
   "display": fig_triangle("x", "x+20", "x+40") + CAP + "A triangle has angles \\(x\\), \\(x + 20\\), and \\(x + 40\\). Find the largest angle.",
   "steps": [
     {"say": "The three angles add to 180°. Write that as an equation and solve for x.",
      "pre": "Add the numbers: 20 + 40 = ", "post": "", "answer": 60, "hint": "Add 20 and 40."},
     {"pre": "So 3x + 60 = 180. Take 60 from both sides: 180 − 60 = ", "post": "", "answer": 120, "hint": "Subtract 60 from 180."},
     {"pre": "3x = 120, so x = 120 ÷ 3 = ", "post": "°", "answer": 40, "hint": "Divide 120 by 3."},
     {"pre": "The largest is x + 40 = 40 + 40 = ", "post": "°", "answer": 80, "done": "Check: 40 + 60 + 80 = 180°. That is the gold move: turn the fact into an equation, solve, then answer what was asked.", "hint": "Add 40 to x."},
   ],
 },
}

method_card = {
  "title": "Angle Facts & Properties",
  "steps": [
    "Angles on a straight line add to 180°; angles at a point add to 360°.",
    "Vertically opposite angles are equal. On parallel lines: alternate and corresponding angles are equal; co-interior angles add to 180°.",
    "Triangle = 180°, quadrilateral = 360°. Polygon interior sum = (n − 2) × 180°.",
    "Exterior angles of any polygon add to 360°; interior + exterior = 180°.",
  ],
  "content": "<p>Key angle facts: angles on a straight line = 180°, angles at a point = 360°, vertically opposite angles are equal. For <strong>parallel lines</strong>: alternate angles (Z) are equal, corresponding angles (F) are equal, co-interior angles (C) add to 180°.</p><p><strong>Polygons:</strong> Interior angle sum = \\((n-2) \\times 180°\\). Exterior angles sum = 360°.</p>",
  "example": "<p><strong>Find the interior angle of a regular hexagon.</strong></p><p>Sum = (6−2) × 180° = 720°. Each angle = 720° ÷ 6 = 120°.</p>",
}

live = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_geoL01_live.json", encoding="utf-8"))
pd = live["practice_data"]
pd["method_card"] = method_card
pd["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": bronze_desc, "silver_description": silver_desc, "gold_description": gold_desc,
}
pd["tier_guides"] = tier_guides
pd["guided"] = {"opener": opener, "teach": teach}

# ---------- VERIFY MATHS ----------
exp = {
  "bronze": [180-72, 360-(90+120+85), 180-50-70, (180-40)//2, 55, 63, 180-105, 360],
  "silver": [(6-2)*180, 360//(180-120), 360//8, (5-2)*180//5, (180-10)//5, 360//24, 1440//180+2],
  "gold": [180-42-65, 360-90-120, 360//(180//6), 3*(180//6), 25],
}
errs = []
for tier, probs in (("bronze",bronze),("silver",silver),("gold",gold)):
    seen = set()
    for i, p in enumerate(probs):
        sol = p["solutions"][0]
        if abs(sol - exp[tier][i]) > 1e-9:
            errs.append(f"{tier}[{i}] solution {sol} != recomputed {exp[tier][i]}")
        if sol in seen:
            errs.append(f"{tier}[{i}] duplicate solution {sol}")
        seen.add(sol)
        gs = p["guided_steps"]
        boxes = answer_boxes(gs)
        if sol not in boxes:
            errs.append(f"{tier}[{i}] solution {sol} not among boxes {boxes}")
        sub = next((k for k,st in enumerate(gs) if st.get("phase")=="substitute"), None)
        if sub is None: errs.append(f"{tier}[{i}] no substitute")
        else:
            live_boxes = sum(1 for st in gs[sub:] if st.get("answer") is not None)
            if live_boxes < 2: errs.append(f"{tier}[{i}] only {live_boxes} live boxes")
            if sub < 1: errs.append(f"{tier}[{i}] sub at 0")
        for m in p.get("misconceptions",[]):
            e = m.get("expect")
            if isinstance(e,(int,float)) and abs(e-sol) < 0.011:
                errs.append(f"{tier}[{i}] expect equals solution")
for t,td in teach.items():
    if len(answer_boxes(td["steps"])) < 4:
        errs.append(f"teach {t} <4 boxes")
if len(answer_boxes(opener["steps"])) < 1:
    errs.append("opener no boxes")
if errs:
    print("VERIFY ERRORS:")
    for e in errs: print("  -", e)
    raise SystemExit(1)
print("VERIFY OK: solutions, boxes, boundaries, expects all checked")

out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_geometry-L01_maths-ocr.json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("wrote", out)
