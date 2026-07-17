# -*- coding: utf-8 -*-
import json, math, io

def wrap(w, h, inner, label):
    return ("<svg viewBox='0 0 %d %d' role=\"img\" aria-label=\"%s\" "
            "style='max-width:250px;width:100%%;height:auto;font-family:Inter,sans-serif'>"
            "%s</svg>") % (w, h, label, inner)

def T(x, y, s, size=12, anchor='middle', weight='normal'):
    return ("<text x='%.1f' y='%.1f' fill='currentColor' font-size='%d' "
            "text-anchor='%s' font-weight='%s'>%s</text>") % (x, y, size, anchor, weight, s)

def L(x1, y1, x2, y2, w=2, dash=None):
    d = " stroke-dasharray='4 3'" if dash else ""
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='currentColor' stroke-width='%d'%s/>" % (x1, y1, x2, y2, w, d)

def pt(cx, cy, r, ang):
    return (cx + r * math.cos(math.radians(ang)), cy - r * math.sin(math.radians(ang)))

def arc(cx, cy, r, a0, a1):
    x0, y0 = pt(cx, cy, r, a0); x1, y1 = pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return ("<path d='M%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f' fill='none' "
            "stroke='currentColor' stroke-width='1.4'/>") % (x0, y0, r, r, large, x1, y1)

CAP = "<span class='figure-caption'>Diagram not drawn accurately</span>"

# ----- point diagram: rays from O with sector labels -----
def point_diagram(bounds, labels, aria, w=240, h=170, ext_r=68):
    cx, cy = 120, 92; inner = []
    for a in bounds:
        x, y = pt(cx, cy, ext_r, a)
        inner.append(L(cx, cy, x, y))
    inner.append("<circle cx='%d' cy='%d' r='3' fill='currentColor'/>" % (cx, cy))
    mids = []
    n = len(bounds)
    ordered = bounds + [bounds[0] + 360]
    for i in range(n):
        mids.append((ordered[i] + ordered[i + 1]) / 2.0)
    for m, lab in zip(mids, labels):
        lx, ly = pt(cx, cy, ext_r * 0.55, m)
        inner.append(T(lx, ly + 4, lab, 12))
    return wrap(w, h, "".join(inner), aria)

# ----- straight line two angles (B1) -----
def sl2(known, unknown, aria):
    cx, cy = 120, 112; inner = []
    inner.append(L(25, cy, 215, cy))
    ex, ey = pt(cx, cy, 78, 130)
    inner.append(L(cx, cy, ex, ey))
    inner.append("<circle cx='%d' cy='%d' r='3' fill='currentColor'/>" % (cx, cy))
    lx, ly = pt(cx, cy, 44, 65); inner.append(T(lx, ly, known, 12))
    ux, uy = pt(cx, cy, 40, 155); inner.append(T(ux - 2, uy, unknown, 13, weight='bold'))
    return wrap(240, 140, "".join(inner), aria)

# ----- straight line three angles (B8): x, x, 60 not to scale -----
def sl3(aria):
    cx, cy = 120, 118; inner = []
    inner.append(L(22, cy, 218, cy))
    for a in (55, 110):
        x, y = pt(cx, cy, 82, a); inner.append(L(cx, cy, x, y))
    inner.append("<circle cx='%d' cy='%d' r='3' fill='currentColor'/>" % (cx, cy))
    for m, lab, bold in ((27, 'x', True), (82, 'x', True), (145, '60°', False)):
        lx, ly = pt(cx, cy, 50, m); inner.append(T(lx, ly, lab, 13, weight='bold' if bold else 'normal'))
    return wrap(240, 138, "".join(inner), aria)

# ----- vertically opposite (B2) -----
def vopp(known, aria):
    cx, cy = 120, 92; inner = []
    a1, b1 = pt(cx, cy, 92, 0); a2, b2 = pt(cx, cy, 92, 180)
    inner.append(L(a2, b2, a1, b1))
    c1, d1 = pt(cx, cy, 92, 72); c2, d2 = pt(cx, cy, 92, 252)
    inner.append(L(c1, d1, c2, d2))
    inner.append("<circle cx='%d' cy='%d' r='3' fill='currentColor'/>" % (cx, cy))
    lx, ly = pt(cx, cy, 46, 36); inner.append(T(lx, ly, known, 12))
    ux, uy = pt(cx, cy, 46, 216); inner.append(T(ux, uy + 3, '?', 13, weight='bold'))
    return wrap(240, 176, "".join(inner), aria)

# ----- triangle -----
def triangle(labels, aria, right=False, iso=False, cap=True):
    if right:
        A = (45, 128); B = (208, 128); C = (45, 38)
    else:
        A = (32, 128); B = (208, 128); C = (112, 30)
    inner = []
    inner.append("<polygon points='%.0f,%.0f %.0f,%.0f %.0f,%.0f' fill='#60a5fa' fill-opacity='0.18' stroke='currentColor' stroke-width='2'/>" % (A[0], A[1], B[0], B[1], C[0], C[1]))
    if right:
        inner.append("<rect x='%.0f' y='%.0f' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.4'/>" % (A[0] + 1, A[1] - 15))
    if iso:
        # tick marks on the two equal sides AC and BC
        def tick(P, Q):
            mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
            dx, dy = Q[0] - P[0], Q[1] - P[1]
            ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
            return L(mx - nx * 5, my - ny * 5, mx + nx * 5, my + ny * 5, 1.4)
        inner.append(tick(A, C)); inner.append(tick(B, C))
    # label placement: nudge toward centroid
    G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    for V, lab in zip((A, B, C), labels):
        lx = V[0] + (G[0] - V[0]) * 0.30
        ly = V[1] + (G[1] - V[1]) * 0.30 + 4
        bold = lab.strip() in ('?',) or 'x' in lab
        inner.append(T(lx, ly, lab, 12, weight='bold' if bold else 'normal'))
    svg = wrap(240, 150, "".join(inner), aria)
    return svg + (CAP if cap else "")

# ----- parallel lines + transversal -----
def parallel(top_lab, bot_lab, kind, aria):
    inner = []
    y1, y2 = 42, 116
    inner.append(L(20, y1, 220, y1))
    inner.append(L(20, y2, 220, y2))
    # parallel arrow marks
    for yy in (y1, y2):
        inner.append("<path d='M116,%d l7,-4 M116,%d l7,4' stroke='currentColor' stroke-width='1.4' fill='none'/>" % (yy, yy))
    # transversal through (70,135)->(180,25): crosses y2 at x=90, y1 at x=160
    inner.append(L(72, 132, 178, 28))
    Ptop = (160, y1); Pbot = (90, y2)
    inner.append("<circle cx='%.0f' cy='%.0f' r='2.5' fill='currentColor'/>" % Ptop)
    inner.append("<circle cx='%.0f' cy='%.0f' r='2.5' fill='currentColor'/>" % Pbot)
    if kind == 'alternate':
        # Z-shape: known above-right of top intersection, ? below-left of bottom
        inner.append(T(Ptop[0] + 16, Ptop[1] - 6, top_lab, 12))
        inner.append(T(Pbot[0] - 16, Pbot[1] + 15, bot_lab, 12, weight='bold'))
    else:  # co-interior, same side (left), between the lines
        inner.append(T(Ptop[0] - 20, Ptop[1] + 16, top_lab, 12))
        inner.append(T(Pbot[0] - 16, Pbot[1] - 8, bot_lab, 12, weight='bold'))
    return wrap(240, 150, "".join(inner), aria)

# ----- regular polygon -----
def regpoly(n, name, aria):
    cx, cy, r = 120, 82, 60; pts = []
    for i in range(n):
        a = 90 + i * 360.0 / n
        x, y = pt(cx, cy, r, a); pts.append("%.1f,%.1f" % (x, y))
    inner = ["<polygon points='%s' fill='#34d399' fill-opacity='0.16' stroke='currentColor' stroke-width='2'/>" % " ".join(pts)]
    inner.append(T(cx, 168, name, 12))
    return wrap(240, 180, "".join(inner), aria)

# ---------------- assemble ----------------
pd = {}

pd["method_card"] = {
    "title": "Angle Facts & Properties",
    "steps": [
        "Spot which angle fact fits the figure (straight line, point, triangle, parallel lines or polygon).",
        "Write the total that those angles must make.",
        "Subtract the known angles, or solve the equation, to find the unknown.",
        "State the reason, e.g. angles on a straight line, alternate angles."
    ],
    "content": ("<p><strong>Straight line</strong> = 180°. <strong>At a point</strong> = 360°. "
                "<strong>Vertically opposite</strong> angles are equal. <strong>Triangle</strong> = 180°, "
                "<strong>quadrilateral</strong> = 360°.</p>"
                "<p><strong>Parallel lines:</strong> alternate (Z) equal, corresponding (F) equal, "
                "co-interior (C) add to 180°.</p>"
                "<p><strong>Polygon:</strong> interior angles sum to \\((n-2)\\times180^\\circ\\); each exterior "
                "angle of a regular polygon = \\(360^\\circ\\div n\\); interior + exterior = 180°.</p>"),
    "example": ("<p><strong>Find the interior angle of a regular pentagon.</strong></p>"
                "<p>Sum = \\((5 - 2) \\times 180 = 540^\\circ\\). Each angle = \\(540 \\div 5 = 108^\\circ\\).</p>")
}

pd["topic_links"] = {"prerequisites": []}
pd["related_videos"] = []

# worked_examples: preserve, de-em-dash the labels
pd["worked_examples"] = [
    {"steps": [
        {"label": "Step 1: Apply rule", "content": "<p>Angles on a straight line = \\(180^\\circ\\)</p>"},
        {"label": "Step 2: Solve", "content": "<p>\\(x = 180 - 65 = 115\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(x = 115^\\circ\\)</strong></p>", "isAnswer": True, "is_answer": True}
     ], "question": "Two angles on a straight line are 65° and x°. Find x.", "difficulty": "Bronze"},
    {"steps": [
        {"label": "Step 1: Formula", "content": "<p>Exterior angle = \\(360 \\div n\\)</p>"},
        {"label": "Step 2: Substitute", "content": "<p>\\(360 \\div 8 = 45^\\circ\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(45^\\circ\\)</strong></p>", "isAnswer": True, "is_answer": True}
     ], "question": "Find the exterior angle of a regular octagon.", "difficulty": "Silver"},
    {"steps": [
        {"label": "Step 1: Set up equation", "content": "<p>\\(2x + 3x + 40 = 180\\)</p>"},
        {"label": "Step 2: Solve", "content": "<p>\\(5x = 140\\), \\(x = 28\\)</p>"},
        {"label": "Answer", "content": "<p><strong>\\(x = 28^\\circ\\)</strong></p>", "isAnswer": True, "is_answer": True}
     ], "question": "In a triangle, angles are 2x, 3x and 40°. Find x.", "difficulty": "Gold"}
]

# ---------------- problem bank ----------------
DEG = "°"

bronze = [
 {  # B1 straight line 130, x
  "display": sl2("130" + DEG, "x", "A straight line with an angle of 130 degrees and an unknown angle x on it") +
             "Angles on a straight line: \\(x\\) and \\(130^\\circ\\). Find \\(x\\).",
  "options": ["\\(50^\\circ\\)", "\\(230^\\circ\\)", "\\(130^\\circ\\)", "\\(40^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Angles on a straight line add to 180. Take 130 away from 180.",
  "misconceptions": [
    {"pattern": "used_360", "expect": 1, "message": "Angles on a straight line add to 180°, not 360°. x = 180 − 130 = 50°."},
    {"pattern": "thinks_equal", "expect": 2, "message": "These two angles are supplementary (they add to 180°), they are not equal."}
  ]},
 {  # B2 vertically opposite 72
  "display": vopp("72" + DEG, "Two straight lines crossing, one angle is 72 degrees and its vertically opposite angle is unknown") +
             "Vertically opposite angles: one is \\(72^\\circ\\). What is the other?",
  "options": ["\\(72^\\circ\\)", "\\(108^\\circ\\)", "\\(288^\\circ\\)", "\\(36^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Vertically opposite angles are always equal.",
  "misconceptions": [
    {"pattern": "supplementary", "expect": 1, "message": "Vertically opposite angles are equal, not supplementary. The answer is 72°."},
    {"pattern": "halved", "expect": 3, "message": "Do not halve it. Vertically opposite angles are equal, so the answer is 72°."}
  ]},
 {  # B3 triangle 55,80,x
  "display": triangle(["55" + DEG, "80" + DEG, "?"], "A triangle with angles 55 degrees, 80 degrees and an unknown angle") +
             "Angles in a triangle: \\(55^\\circ\\), \\(80^\\circ\\) and \\(x\\). Find \\(x\\).",
  "options": ["\\(45^\\circ\\)", "\\(135^\\circ\\)", "\\(225^\\circ\\)", "\\(35^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Angles in a triangle add to 180. Subtract both known angles.",
  "misconceptions": [
    {"pattern": "used_360", "expect": 2, "message": "Angles in a triangle add to 180°, not 360°. x = 180 − 55 − 80 = 45°."},
    {"pattern": "added_knowns", "expect": 1, "message": "135° is the two known angles added. Subtract them from 180° instead: x = 45°."}
  ]},
 {  # B4 point 90,150,x
  "display": point_diagram([0, 90, 240], ["90" + DEG, "150" + DEG, "?"],
             "Three angles meeting at a point: 90 degrees, 150 degrees and an unknown angle") +
             "Three angles at a point are \\(90^\\circ\\), \\(150^\\circ\\) and \\(x\\). Find \\(x\\).",
  "options": ["\\(120^\\circ\\)", "\\(60^\\circ\\)", "\\(180^\\circ\\)", "\\(240^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Angles at a point add to 360. Subtract the two known angles.",
  "misconceptions": [
    {"pattern": "added_knowns", "expect": 3, "message": "240° is the two known angles added. Take that from 360°: x = 360 − 240 = 120°."},
    {"pattern": "used_180", "expect": None, "message": "Angles at a point add to 360°, not 180°."}
  ]},
 {  # B5 isosceles top 40
  "display": triangle(["?", "?", "40" + DEG], "An isosceles triangle with a top angle of 40 degrees and two equal base angles", iso=True) +
             "An isosceles triangle has a top angle of \\(40^\\circ\\). Find each base angle.",
  "options": ["\\(70^\\circ\\)", "\\(140^\\circ\\)", "\\(40^\\circ\\)", "\\(80^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "The two base angles are equal. Share what is left after the top angle between them.",
  "misconceptions": [
    {"pattern": "forgot_divide", "expect": 1, "message": "140° is the two base angles together. They are equal, so divide by 2: 70°."},
    {"pattern": "base_equals_top", "expect": 2, "message": "A base angle is not equal to the top angle. 180 − 40 = 140, then divide by 2 to get 70°."}
  ]},
 {  # B6 quadrilateral sum (fact recall, no figure)
  "display": "What is the angle sum of a quadrilateral?",
  "options": ["\\(360^\\circ\\)", "\\(180^\\circ\\)", "\\(540^\\circ\\)", "\\(720^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "A quadrilateral has 4 sides. Use (n − 2) × 180.",
  "misconceptions": [
    {"pattern": "triangle", "expect": 1, "message": "180° is a triangle. A quadrilateral has 4 sides: (4 − 2) × 180 = 360°."},
    {"pattern": "pentagon", "expect": 2, "message": "540° is a pentagon (5 sides). A quadrilateral has angle sum 360°."}
  ]},
 {  # B7 right triangle 90,35,x
  "display": triangle(["", "35" + DEG, "?"], "A right-angled triangle with a right angle, an angle of 35 degrees and an unknown angle", right=True) +
             "A right angle, \\(35^\\circ\\) and \\(x\\) are in a triangle. Find \\(x\\).",
  "options": ["\\(55^\\circ\\)", "\\(235^\\circ\\)", "\\(145^\\circ\\)", "\\(45^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "A right angle is 90. Subtract 90 and 35 from 180.",
  "misconceptions": [
    {"pattern": "forgot_right", "expect": 2, "message": "The right angle is 90°. x = 180 − 90 − 35 = 55°."},
    {"pattern": "used_360", "expect": 1, "message": "Angles in a triangle add to 180°, not 360°."}
  ]},
 {  # B8 straight line x,x,60
  "display": sl3("A straight line split into three angles: x, x and 60 degrees") +
             "Angles on a straight line: \\(x\\), \\(x\\) and \\(60^\\circ\\). Find \\(x\\).",
  "options": ["\\(60^\\circ\\)", "\\(120^\\circ\\)", "\\(150^\\circ\\)", "\\(30^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "There are two equal x angles. Set up 2x + 60 = 180.",
  "misconceptions": [
    {"pattern": "only_one_x", "expect": 1, "message": "There are two x angles. Use 2x + 60 = 180, which gives x = 60°."},
    {"pattern": "used_360", "expect": 2, "message": "Angles on a straight line add to 180°, not 360°."}
  ]}
]

silver = [
 {  # S1 alternate 65
  "display": parallel("65" + DEG, "?", "alternate", "Two parallel lines cut by a transversal, one alternate angle is 65 degrees") +
             "Parallel lines cut by a transversal. One alternate angle is \\(65^\\circ\\). Find the other.",
  "options": ["\\(65^\\circ\\)", "\\(115^\\circ\\)", "\\(25^\\circ\\)", "\\(130^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Alternate angles (Z-shape) are equal.",
  "misconceptions": [
    {"pattern": "supplementary", "expect": 1, "message": "Alternate angles are equal, not supplementary. The answer is 65°."},
    {"pattern": "complementary", "expect": 2, "message": "Alternate angles are equal (both 65°), they do not add to 90°."}
  ]},
 {  # S2 co-interior 110
  "display": parallel("110" + DEG, "?", "cointerior", "Two parallel lines cut by a transversal, one co-interior angle is 110 degrees") +
             "Co-interior angle with a parallel line: one angle is \\(110^\\circ\\). Find the other.",
  "options": ["\\(70^\\circ\\)", "\\(110^\\circ\\)", "\\(250^\\circ\\)", "\\(90^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Co-interior angles (C-shape) add to 180.",
  "misconceptions": [
    {"pattern": "equal", "expect": 1, "message": "Co-interior angles add to 180°, they are not equal. 180 − 110 = 70°."},
    {"pattern": "used_360", "expect": 2, "message": "Co-interior angles sum to 180°, not 360°."}
  ]},
 {  # S3 hexagon sum
  "display": regpoly(6, "regular hexagon", "A regular hexagon") +
             "Find the sum of the interior angles of a hexagon.",
  "options": ["\\(720^\\circ\\)", "\\(1080^\\circ\\)", "\\(540^\\circ\\)", "\\(360^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Use (n − 2) × 180 with n = 6.",
  "misconceptions": [
    {"pattern": "forgot_subtract_2", "expect": 1, "message": "Use (n − 2) × 180, not n × 180. (6 − 2) × 180 = 720°."},
    {"pattern": "wrong_n", "expect": 2, "message": "A hexagon has 6 sides, not 5. (6 − 2) × 180 = 720°."}
  ]},
 {  # S4 exterior 40 -> sides
  "display": "Each exterior angle of a regular polygon is \\(40^\\circ\\). How many sides?",
  "options": ["9", "8", "10", "40"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Number of sides = 360 ÷ exterior angle.",
  "misconceptions": [
    {"pattern": "gave_angle", "expect": 3, "message": "40 is the exterior angle, not the number of sides. Sides = 360 ÷ 40 = 9."},
    {"pattern": "used_interior", "expect": None, "message": "Divide 360 by the exterior angle, not the interior angle."}
  ]},
 {  # S5 decagon interior
  "display": regpoly(10, "regular decagon", "A regular decagon with ten sides") +
             "Find each interior angle of a regular decagon (10 sides).",
  "options": ["\\(144^\\circ\\)", "\\(140^\\circ\\)", "\\(150^\\circ\\)", "\\(36^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Interior = 180 − exterior, and exterior = 360 ÷ 10.",
  "misconceptions": [
    {"pattern": "gave_exterior", "expect": 3, "message": "36° is the exterior angle (360 ÷ 10). The interior angle is 180 − 36 = 144°."},
    {"pattern": "wrong_shape", "expect": None, "message": "A decagon has 10 sides. Interior = (10 − 2) × 180 ÷ 10 = 144°."}
  ]},
 {  # S6 exterior 30 -> interior
  "display": "An exterior angle of a regular polygon is \\(30^\\circ\\). What is the interior angle?",
  "options": ["\\(150^\\circ\\)", "\\(30^\\circ\\)", "\\(330^\\circ\\)", "\\(60^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Interior + exterior = 180.",
  "misconceptions": [
    {"pattern": "thinks_equal", "expect": 1, "message": "Interior and exterior angles add to 180°, they are not equal. 180 − 30 = 150°."},
    {"pattern": "used_360", "expect": 2, "message": "Interior and exterior angles add to 180°, not 360°."}
  ]},
 {  # S7 triangle 3x,4x,5x
  "display": triangle(["3x", "4x", "5x"], "A triangle with angles 3x, 4x and 5x") +
             "A triangle has angles \\(3x\\), \\(4x\\) and \\(5x\\). Find the largest angle.",
  "options": ["\\(75^\\circ\\)", "\\(60^\\circ\\)", "\\(45^\\circ\\)", "\\(90^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Add the parts: 3x + 4x + 5x = 180. Solve for x, then work out 5x.",
  "misconceptions": [
    {"pattern": "gave_middle", "expect": 1, "message": "60° is the middle angle (4x). The largest is 5x = 75°."},
    {"pattern": "gave_smallest", "expect": 2, "message": "45° is the smallest angle (3x). The largest is 5x = 75°."}
  ]}
]

gold = [
 {  # G1 interior 156 -> sides
  "display": "The interior angle of a regular polygon is \\(156^\\circ\\). How many sides?",
  "options": ["15", "12", "18", "24"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Exterior = 180 − 156. Then sides = 360 ÷ exterior.",
  "misconceptions": [
    {"pattern": "gave_exterior", "expect": 3, "message": "24 is the exterior angle (180 − 156). Divide 360 by it: 360 ÷ 24 = 15 sides."},
    {"pattern": "divided_by_interior", "expect": None, "message": "Do not divide 360 by the interior angle. Find the exterior angle first: 180 − 156 = 24°."}
  ]},
 {  # G2 pentagon+hexagon at a point  (FIX: correct answer is 132)
  "display": point_diagram([0, 108, 228], ["108" + DEG, "120" + DEG, "x"],
             "A regular pentagon and a regular hexagon meet at a point; their interior angles 108 and 120 degrees and the gap x") +
             "A regular pentagon and a regular hexagon share a side and meet at a point, with angle \\(x\\) in the gap between them. Find \\(x\\).",
  "options": ["\\(48^\\circ\\)", "\\(132^\\circ\\)", "\\(12^\\circ\\)", "\\(60^\\circ\\)"],
  "solutions": [1], "calculator": False, "input_type": "multiple_choice",
  "hint": "Around the point the three angles add to 360. Subtract both polygon interior angles.",
  "misconceptions": [
    {"pattern": "used_exterior", "expect": 0, "message": "48° comes from the exterior angles. Around the point use the interior angles: 360 − 108 − 120 = 132°."},
    {"pattern": "subtracted_the_two", "expect": 2, "message": "Do not subtract the two interior angles from each other. Around the point: 360 − 108 − 120 = 132°."}
  ]},
 {  # G3 parallel a=3x+10 alternate b=5x-20
  "display": parallel("3x+10", "5x−20", "alternate", "Two parallel lines cut by a transversal with alternate angles 3x plus 10 and 5x minus 20") +
             "Two parallel lines are cut by a transversal. One angle is \\(3x + 10\\) and its alternate angle is \\(5x - 20\\). Find \\(x\\).",
  "options": ["15", "55", "10", "25"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Alternate angles are equal. Set 3x + 10 = 5x − 20 and solve.",
  "misconceptions": [
    {"pattern": "gave_angle", "expect": 1, "message": "55 is the size of the angle (3(15) + 10). The question asks for x, which is 15."},
    {"pattern": "used_cointerior", "expect": None, "message": "These are alternate angles (equal), not co-interior. Set 3x + 10 = 5x − 20."}
  ]},
 {  # G4 interior = 8 x exterior
  "display": "A regular polygon has interior angles 8 times its exterior angles. How many sides?",
  "options": ["18", "16", "20", "36"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Interior + exterior = 180. Write 8e + e = 180, find e, then 360 ÷ e.",
  "misconceptions": [
    {"pattern": "gave_exterior", "expect": 2, "message": "20 is the exterior angle (e). The number of sides is 360 ÷ 20 = 18."},
    {"pattern": "swapped_ratio", "expect": None, "message": "Interior is 8 times exterior, so 8e + e = 180, giving e = 20° and 18 sides."}
  ]},
 {  # G5 proof concept
  "display": "To prove the exterior angles of any polygon sum to \\(360^\\circ\\), which fact is used?",
  "options": ["Interior + exterior = \\(180^\\circ\\) at each vertex", "Angles in a triangle = \\(180^\\circ\\)",
              "Vertically opposite angles are equal", "Angles at a point = \\(360^\\circ\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "At each vertex the interior and exterior angle together make a straight line.",
  "misconceptions": [
    {"pattern": "at_a_point", "expect": 3, "message": "Angles at a point (360°) is the result you are proving, not the fact you build from. Each interior + exterior = 180°."},
    {"pattern": "triangle", "expect": 1, "message": "The proof does not use the triangle angle sum. It uses interior + exterior = 180° at every vertex."}
  ]}
]

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Find missing angles using basic angle facts",
    "silver_description": "Parallel lines, polygon angle sums and exterior angles",
    "gold_description": "Algebraic angle problems and multi-step reasoning"
}

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: basic angle facts",
   "steps": [
     "Learn the totals. Angles on a <strong>straight line</strong> add to 180°, angles <strong>at a point</strong> add to 360°, angles in a <strong>triangle</strong> add to 180°, and <strong>vertically opposite</strong> angles are equal.",
     "Pick the fact that matches the figure, then subtract the angles you know from the total.",
     "If an angle repeats, collect it: two equal x angles plus the rest equals the total. In an isosceles triangle the two base angles are equal."
   ],
   "example": {
     "question": "Angles on a straight line are 110° and x. Find x.",
     "steps": [
       {"label": "Rule", "content": "<p>Angles on a straight line add to 180°.</p>"},
       {"label": "Subtract", "content": "<p>\\(x = 180 - 110 = 70\\)</p>"},
       {"label": "Check", "content": "<p>\\(110 + 70 = 180\\) ✓</p>"},
       {"label": "Answer", "content": "<p><strong>x = 70°</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "silver": {
   "title": "Silver: parallel lines and polygons",
   "steps": [
     "With <strong>parallel lines</strong>: alternate angles (Z) are equal, corresponding angles (F) are equal, and co-interior angles (C) add to 180°.",
     "For a polygon with n sides the interior angles add to <strong>(n − 2) × 180°</strong>. Each exterior angle of a regular polygon is <strong>360° ÷ n</strong>, and interior + exterior = 180°.",
     "To find n from an exterior angle, divide: n = 360 ÷ exterior angle."
   ],
   "example": {
     "question": "Find each interior angle of a regular octagon.",
     "steps": [
       {"label": "Exterior", "content": "<p>Exterior = \\(360 \\div 8 = 45^\\circ\\)</p>"},
       {"label": "Interior", "content": "<p>Interior = \\(180 - 45 = 135^\\circ\\)</p>"},
       {"label": "Check", "content": "<p>\\((8 - 2) \\times 180 \\div 8 = 135^\\circ\\) ✓</p>"},
       {"label": "Answer", "content": "<p><strong>135°</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "gold": {
   "title": "Gold: algebra and multi-step angles",
   "steps": [
     "When angles are given as expressions, add them and set the total equal to the correct sum, for example 3x + 4x + 5x = 180 in a triangle.",
     "Solve for the letter, then substitute back to find the angle actually asked for, which is often not x itself.",
     "For polygon problems, link the two facts: interior + exterior = 180° and exterior = 360° ÷ n, then solve."
   ],
   "example": {
     "question": "A triangle has angles 2x, 3x and 40°. Find the largest angle.",
     "steps": [
       {"label": "Set up", "content": "<p>\\(2x + 3x + 40 = 180\\)</p>"},
       {"label": "Solve", "content": "<p>\\(5x = 140\\), so \\(x = 28\\)</p>"},
       {"label": "Largest", "content": "<p>Largest = \\(3x = 84^\\circ\\)</p>"},
       {"label": "Check", "content": "<p>\\(2(28) + 3(28) + 40 = 56 + 84 + 40 = 180\\) ✓</p>"},
       {"label": "Answer", "content": "<p><strong>84°</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 }
}

# ---------------- guided (opener + teach) ----------------
pizza = (
  "<svg viewBox='0 0 240 190' role=\"img\" aria-label=\"A pizza cut from the centre into three slices of 120 degrees, 150 degrees and an unknown slice\" "
  "style='max-width:230px;width:100%;height:auto;font-family:Inter,sans-serif'>"
  "<circle cx='120' cy='95' r='72' fill='#f59e0b' fill-opacity='0.15' stroke='currentColor' stroke-width='2'/>"
)
_c = (120, 95)
for a in (0, 120, 270):
    x, y = pt(_c[0], _c[1], 72, a)
    pizza += L(_c[0], _c[1], x, y)
for m, lab in ((60, "120°"), (195, "150°"), (315, "?")):
    lx, ly = pt(_c[0], _c[1], 44, m)
    pizza += T(lx, ly + 4, lab, 13, weight='bold' if lab == '?' else 'normal')
pizza += "</svg>"

pd["guided"] = {
 "opener": {
   "label": "Before any rules",
   "display": pizza + "A pizza is cut from the centre into three slices.",
   "steps": [
     {"say": "One slice is 120° and the next is 150°. The three slices fill the whole pizza, and once round a full circle is 360°.",
      "pre": "The last slice must be ", "post": "°", "answer": 90,
      "hint": "The three slices fill 360°. Take away 120 and 150."},
     {"say": "Now picture a fresh pizza cut into 4 equal slices from the centre. Every slice is the same size.",
      "pre": "One slice = 360 ÷ 4 = ", "post": "°", "answer": 90,
      "hint": "Share 360° equally between the 4 slices."},
     {"say": "Those totals are the first angle facts: angles that meet <strong>at a point</strong> always add to <strong>360°</strong> (a full turn), and angles on a <strong>straight line</strong> (a half pizza) add to <strong>180°</strong>. Every question here is really just filling a known total."}
   ]
 },
 "teach": {
   "bronze": {
     "label": "Together: your first one",
     "display": "In a triangle the angles are \\(35^\\circ\\), \\(85^\\circ\\) and \\(a\\). The angle \\(a\\) then sits on a straight line next to angle \\(b\\). Find \\(a\\) and \\(b\\).",
     "steps": [
       {"say": "First the triangle. The three angles add to 180°. Add the two you know:",
        "pre": "35 + 85 = ", "post": "", "answer": 120, "hint": "Just add 35 and 85."},
       {"pre": "So a = 180 − 120 = ", "post": "", "answer": 60,
        "done": "That is the triangle fact: three angles make 180°.", "hint": "Take 120 away from 180."},
       {"say": "Now a and b sit on a straight line, which is 180°.",
        "pre": "b = 180 − 60 = ", "post": "", "answer": 120, "hint": "Take a (60) away from 180."},
       {"say": "Check the triangle adds up.",
        "pre": "35 + 85 + 60 = ", "post": "", "answer": 180,
        "done": "180°, so a = 60° is right.", "hint": "Add all three triangle angles."}
     ]
   },
   "silver": {
     "label": "Together: the polygon move",
     "display": "A regular polygon has 12 sides. Find the sum of its interior angles, then each interior angle, and check with the exterior angle.",
     "steps": [
       {"say": "Use the interior-angle-sum formula \\((n - 2) \\times 180\\) with \\(n = 12\\). First n − 2:",
        "pre": "12 − 2 = ", "post": "", "answer": 10, "hint": "Just 12 take away 2."},
       {"pre": "Sum = 10 × 180 = ", "post": "", "answer": 1800,
        "done": "That is the total of all 12 interior angles.", "hint": "Multiply 10 by 180."},
       {"say": "For a REGULAR polygon every angle is equal, so divide the sum by 12:",
        "pre": "1800 ÷ 12 = ", "post": "", "answer": 150, "hint": "Share 1800 between 12 angles."},
       {"say": "Check with the exterior angle. Each exterior = 360 ÷ 12 = 30, and interior + exterior = 180.",
        "pre": "180 − 30 = ", "post": "", "answer": 150,
        "done": "Both routes give 150°, so it checks.", "hint": "Take the exterior angle from 180."}
     ]
   },
   "gold": {
     "label": "Together: the algebra move",
     "display": "The angles of a quadrilateral are \\(x\\), \\(2x\\), \\(3x\\) and \\(90^\\circ\\). Find the largest angle.",
     "steps": [
       {"say": "A quadrilateral's angles add to 360°. Collect the x terms first:",
        "pre": "x + 2x + 3x = ", "post": "x", "answer": 6, "hint": "Add the numbers in front: 1 + 2 + 3."},
       {"say": "So 6x + 90 = 360. Take the 90 across:",
        "pre": "360 − 90 = ", "post": "", "answer": 270, "hint": "Subtract 90 from 360."},
       {"say": "So 6x = 270.",
        "pre": "x = 270 ÷ 6 = ", "post": "", "answer": 45, "hint": "Divide 270 by 6."},
       {"say": "The largest angle is 3x.",
        "pre": "3 × 45 = ", "post": "", "answer": 135,
        "done": "3x is the biggest angle, 135°.", "hint": "Multiply x by 3."},
       {"say": "Check all four add to 360.",
        "pre": "45 + 90 + 135 + 90 = ", "post": "", "answer": 360,
        "done": "360°, so it all fits.", "hint": "Add all four angles."}
     ]
   }
 }
}

io.open("lesson_geometry-L01.json", "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("written. bronze=%d silver=%d gold=%d" % (len(bronze), len(silver), len(gold)))
