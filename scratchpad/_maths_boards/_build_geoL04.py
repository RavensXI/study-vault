# -*- coding: utf-8 -*-
"""Build guided-learning + diagrams practice_data for maths-aqa geometry-L04 (Transformations)."""
import json, io

MINUS = "−"  # unicode minus

pd = json.load(io.open("_live_geometry-L04.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---------- coordinate-grid SVG generator ----------
def grid_svg(markers, aria):
    """markers: list of dicts {x,y,label,kind}. kind in point/centre/image."""
    xs = [m["x"] for m in markers] + [0]
    ys = [m["y"] for m in markers] + [0]
    xmin, xmax = min(xs) - 1, max(xs) + 1
    ymin, ymax = min(ys) - 1, max(ys) + 1
    W, H, pad = 224, 200, 20
    u = min((W - 2 * pad) / (xmax - xmin), (H - 2 * pad) / (ymax - ymin))
    ox = pad - xmin * u
    oy = pad + ymax * u
    def sx(x): return round(ox + x * u, 1)
    def sy(y): return round(oy - y * u, 1)
    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:260px;font-family:Inter,sans-serif">' % (W, H, aria)]
    # gridlines
    gx = xmin
    while gx <= xmax:
        parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-opacity="0.12" stroke-width="1"/>' % (sx(gx), sy(ymin), sx(gx), sy(ymax)))
        gx += 1
    gy = ymin
    while gy <= ymax:
        parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-opacity="0.12" stroke-width="1"/>' % (sx(xmin), sy(gy), sx(xmax), sy(gy)))
        gy += 1
    # axes
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.6"/>' % (sx(xmin), sy(0), sx(xmax), sy(0)))
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.6"/>' % (sx(0), sy(ymin), sx(0), sy(ymax)))
    # markers
    for m in markers:
        px, py = sx(m["x"]), sy(m["y"])
        lab = m["label"].replace("-", MINUS)
        anchor = "start"
        lx, ly = px + 6, py - 6
        if m["x"] >= xmax - 1:  # near right edge, put label left
            anchor = "end"; lx = px - 6
        if m["kind"] == "centre":
            parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.8"/>' % (px - 4, py - 4, px + 4, py + 4))
            parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.8"/>' % (px - 4, py + 4, px + 4, py - 4))
        elif m["kind"] == "image":
            parts.append('<circle cx="%s" cy="%s" r="3.4" fill="#f59e0b" fill-opacity="0.5" stroke="currentColor" stroke-width="1.3"/>' % (px, py))
        else:
            parts.append('<circle cx="%s" cy="%s" r="3.4" fill="#60a5fa" fill-opacity="0.55" stroke="currentColor" stroke-width="1.3"/>' % (px, py))
        parts.append('<text x="%s" y="%s" font-size="10" text-anchor="%s" font-weight="600" fill="currentColor">%s</text>' % (lx, ly, anchor, lab))
    parts.append('</svg>')
    return "".join(parts)

# ---------- tier descriptions ----------
pb["bronze_description"] = "Apply one transformation to a point: translate, reflect, or enlarge from the origin."
pb["silver_description"] = "Rotations about the origin, reflections in y = ±x, and negative or fractional enlargements."
pb["gold_description"] = "Enlarge about a given centre, combine transformations, and describe a transformation fully."

# ---------- per-problem hints + honest expects ----------
# helper to set fields
def setp(tier, i, hint, misc):
    p = pb[tier][i]
    p["hint"] = hint
    p["misconceptions"] = misc

# BRONZE
setp("bronze", 0, "Add the vector to the point: x + 4 and y + (−1).",
     [{"pattern": "wrong_direction", "expect": 1,
       "message": "The vector is (4, −1), so the y-part goes down by 1: 3 + (−1) = 2. Adding 1 instead gives (6, 4). A' = (6, 2)."}])
setp("bronze", 1, "Reflecting in the x-axis keeps x and flips the sign of y.",
     [{"pattern": "y_axis", "expect": 1,
       "message": "Reflecting in the x-axis flips the y-coordinate, not the x: (5, 1) → (5, −1). Negating x gives (−5, 1), which is a reflection in the y-axis."}])
setp("bronze", 2, "Reflecting in the y-axis keeps y and flips the sign of x.",
     [{"pattern": "x_axis", "expect": 1,
       "message": "Reflecting in the y-axis flips the x-coordinate: (−3, 4) → (3, 4). Flipping the y instead gives (−3, −4), which is a reflection in the x-axis."}])
setp("bronze", 3, "The vector is the new point minus the old point.",
     [{"pattern": "subtract_wrong_way", "expect": 1,
       "message": "Vector = new − old = (4 − 1, 2 − 5) = (3, −3). Doing old − new gives (−3, 3), the reverse journey."}])
setp("bronze", 4, "Add each part of the vector to the matching coordinate.",
     [{"pattern": "subtract_vector", "expect": 1,
       "message": "Add the vector as given: (5 + (−2), 1 + 3) = (3, 4). Subtracting it instead gives (7, −2)."}])
setp("bronze", 5, "Reflecting in y = x swaps the x and y coordinates.",
     [{"pattern": "flipped_sign", "expect": 1,
       "message": "Reflecting in y = x swaps the coordinates: (0, 6) → (6, 0). Flipping the sign of y gives (0, −6), a different reflection."}])
setp("bronze", 6, "Multiply each coordinate by the scale factor 3.",
     [{"pattern": "add_sf", "expect": 1,
       "message": "Multiply each coordinate by 3: (2 × 3, 1 × 3) = (6, 3). Adding 3 to each gives (5, 4)."}])
setp("bronze", 7, "A 180° turn about the origin flips the sign of both coordinates.",
     [{"pattern": "one_coord_only", "expect": 1,
       "message": "A 180° rotation about the origin negates both coordinates: (3, 2) → (−3, −2). Negating only the y gives (3, −2)."}])

# SILVER
setp("silver", 0, "90° anticlockwise about the origin sends (x, y) to (−y, x).",
     [{"pattern": "clockwise_rule", "expect": 1,
       "message": "90° anticlockwise sends (x, y) to (−y, x): (4, −1) → (1, 4). Using the clockwise rule (y, −x) gives (−1, −4)."}])
setp("silver", 1, "Multiply each coordinate by the scale factor, keeping the negative sign.",
     [{"pattern": "positive_sf", "expect": 1,
       "message": "A negative scale factor inverts through the centre, so multiply by −2: (1 × −2, 2 × −2) = (−2, −4). Ignoring the minus gives (2, 4)."}])
# S2: FIX degeneracy — add a second point so only reflection in x-axis fits.
s2 = pb["silver"][2]
s2["display"] = grid_svg(
    [{"x": 2, "y": 3, "label": "(2, 3)", "kind": "point"},
     {"x": 5, "y": 4, "label": "(5, 4)", "kind": "point"},
     {"x": 2, "y": -3, "label": "(2, -3)", "kind": "image"},
     {"x": 5, "y": -4, "label": "(5, -4)", "kind": "image"}],
    "A shape and its image plotted on a coordinate grid") + \
    " Describe the single transformation that maps (2, 3) to (2, −3) and (5, 4) to (5, −4)."
s2["hint"] = "See which coordinate stays the same and which flips its sign, for both points."
s2["misconceptions"] = [{"pattern": "translation", "expect": 3,
    "message": "Both points keep their x and flip the sign of y, so the whole shape mirrors in the x-axis. A translation (0, −6) fits (2, 3) but sends (5, 4) to (5, −2), not (5, −4)."}]
setp("silver", 3, "A scale factor of one half means halve each coordinate.",
     [{"pattern": "double", "expect": 1,
       "message": "Scale factor ½ means halve each coordinate: (8 × ½, 6 × ½) = (4, 3). Multiplying by 2 gives (16, 12)."}])
setp("silver", 4, "Reflecting in y = −x sends (x, y) to (−y, −x).",
     [{"pattern": "y_equals_x", "expect": 1,
       "message": "Reflecting in y = −x sends (x, y) to (−y, −x): (−2, 5) → (−5, 2). Just swapping the coordinates (the y = x rule) gives (5, −2)."}])
setp("silver", 5, "Work from the centre: scale the vector from (1, 0), then add it back.",
     [{"pattern": "from_origin", "expect": 1,
       "message": "Measure from the centre (1, 0): vector (2, 1) × 2 = (4, 2), added to the centre gives (5, 2). Enlarging from the origin instead gives (6, 2)."}])
# S6: single-point describe, only CW fits among options — keep, add grid.
s6 = pb["silver"][6]
s6["display"] = grid_svg(
    [{"x": 1, "y": 4, "label": "(1, 4)", "kind": "point"},
     {"x": 4, "y": -1, "label": "(4, -1)", "kind": "image"}],
    "A point and its image plotted on a coordinate grid") + \
    " Describe the single transformation mapping (1, 4) to (4, −1)."
s6["hint"] = "Test each rotation rule until one sends (1, 4) to (4, −1)."
s6["misconceptions"] = [{"pattern": "wrong_direction", "expect": 1,
    "message": "90° clockwise sends (x, y) to (y, −x): (1, 4) → (4, −1). The anticlockwise rule (−y, x) would give (−4, 1)."}]

# GOLD
# G0: fix distractor idx1 to a derivable error (scale from origin then add centre).
g0 = pb["gold"][0]
g0["options"] = ["(−1, −1)", "(−3, −2)", "(2, 1)", "(−1, −3)"]
g0["display"] = grid_svg(
    [{"x": 2, "y": 1, "label": "centre (2, 1)", "kind": "centre"},
     {"x": 5, "y": 3, "label": "G (5, 3)", "kind": "point"}],
    "Point G and the centre of enlargement on a coordinate grid") + \
    " Point G(5, 3) is enlarged by scale factor −1, centre (2, 1). What are the coordinates of G'?"
g0["hint"] = "A half turn about (2, 1): the centre is the midpoint of G and its image."
g0["misconceptions"] = [{"pattern": "scale_then_shift", "expect": 1,
    "message": "Enlargement by −1 about (2, 1) is a half turn about that centre: G' = (2×2 − 5, 2×1 − 3) = (−1, −1). Scaling from the origin and then adding the centre gives (−3, −2)."}]
# G1: enlargement centre (0,6), add grid; expect distractor idx2 (from origin).
g1 = pb["gold"][1]
g1["display"] = grid_svg(
    [{"x": 0, "y": 6, "label": "centre (0, 6)", "kind": "centre"},
     {"x": 9, "y": 0, "label": "(9, 0)", "kind": "point"}],
    "A vertex and the centre of enlargement on a coordinate grid") + \
    " A triangle is enlarged by scale factor \\(\\frac{1}{3}\\), centre (0, 6). Vertex (9, 0) maps to:"
g1["hint"] = "Scale the vector from the centre (0, 6) by one third, then add the centre back."
g1["misconceptions"] = [{"pattern": "from_origin", "expect": 2,
    "message": "Measure from the centre (0, 6): vector (9, −6) × ⅓ = (3, −2), added to the centre gives (3, 4). Scaling from the origin instead gives (3, 0)."}]
# G2: FIX degeneracy — points were both on x-axis. New off-axis points.
g2 = pb["gold"][2]
g2["display"] = grid_svg(
    [{"x": 2, "y": 1, "label": "(2, 1)", "kind": "point"},
     {"x": 4, "y": 2, "label": "(4, 2)", "kind": "point"},
     {"x": 1, "y": -2, "label": "(1, -2)", "kind": "image"},
     {"x": 2, "y": -4, "label": "(2, -4)", "kind": "image"}],
    "A shape and its image plotted on a coordinate grid") + \
    " Describe the single transformation that maps (2, 1) to (1, −2) and (4, 2) to (2, −4)."
g2["options"] = ["Rotation 90° clockwise about the origin",
                 "Rotation 90° anticlockwise about the origin",
                 "Enlargement scale factor −1, centre the origin",
                 "Reflection in y = −x"]
g2["hint"] = "Test each rule on both points; only one maps them both correctly."
g2["misconceptions"] = [{"pattern": "wrong_direction", "expect": 1,
    "message": "90° clockwise sends (x, y) to (y, −x): (2, 1) → (1, −2) and (4, 2) → (2, −4). The anticlockwise rule (−y, x) would send (2, 1) to (−1, 2)."}]
# G3: two parallel reflections -> translation.
setp("gold", 3, "Two reflections in parallel lines make a translation of twice the gap.",
     [{"pattern": "gap_not_double", "expect": 1,
       "message": "Two reflections in parallel lines give a translation of twice the gap. The gap is 5 − 2 = 3, so the translation is 2 × 3 = 6 to the right, vector (6, 0). Using the gap itself gives (3, 0)."}])
# G4: enlargement SF-2 centre (1,1); add grid; distractor idx2 positive SF.
g4 = pb["gold"][4]
g4["display"] = grid_svg(
    [{"x": 1, "y": 1, "label": "centre (1, 1)", "kind": "centre"},
     {"x": 4, "y": 2, "label": "(4, 2)", "kind": "point"}],
    "A point and the centre of enlargement on a coordinate grid") + \
    " A shape at (4, 2) is enlarged by scale factor −2, centre (1, 1). Where is the image?"
g4["hint"] = "Scale the vector from the centre by −2, then add the centre back."
g4["misconceptions"] = [{"pattern": "positive_sf", "expect": 2,
    "message": "The scale factor is −2, so the vector (3, 1) becomes (−6, −2); added to the centre (1, 1) that gives (−5, −1). Using +2 gives (7, 3)."}]

# ---------- method_card (trim to <=4 steps) ----------
pd["method_card"]["steps"] = [
    "Name the transformation: translation, reflection, rotation or enlargement.",
    "Translation: add the column vector. Reflection: flip across the mirror line.",
    "Rotation: use the centre, angle and direction (90° CW gives (y, −x)).",
    "Enlargement: from the centre, scale the vector to the point, then add the centre."
]
pd["method_card"]["content"] = ("<p><strong>Translation:</strong> slide every point by a column vector "
    "\\(\\binom{x}{y}\\). Positive x is right, positive y is up.</p>"
    "<p><strong>Reflection:</strong> in the x-axis flip y; in the y-axis flip x; in y = x swap x and y; "
    "in y = −x go to (−y, −x).</p>"
    "<p><strong>Rotation about the origin:</strong> 90° clockwise (x, y) → (y, −x); "
    "anticlockwise (x, y) → (−y, x); 180° (x, y) → (−x, −y).</p>"
    "<p><strong>Enlargement:</strong> scale the vector from the centre by the factor, then add the centre. "
    "A negative factor flips through the centre.</p>")

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: single transformations on a point",
        "steps": [
            "Translation: add the column vector to the point. Right and up are positive, left and down negative.",
            "Reflection: in the x-axis flip the sign of y, in the y-axis flip the sign of x, in y = x swap the coordinates.",
            "Enlargement from the origin: multiply each coordinate by the scale factor."
        ],
        "example": {
            "question": "Reflect (4, 2) in the x-axis.",
            "steps": [
                {"label": "Rule", "content": "In the x-axis, flip the sign of y."},
                {"label": "Apply", "content": "(4, 2) → (4, −2)"},
                {"label": "Check", "content": "x is unchanged, y distance kept."},
                {"label": "Answer", "content": "(4, −2)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: rotations and negative or fractional enlargements",
        "steps": [
            "Rotate about the origin: 90° clockwise (x, y) → (y, −x); anticlockwise (x, y) → (−y, x); 180° (x, y) → (−x, −y).",
            "Reflect in y = −x: (x, y) → (−y, −x).",
            "Enlarge from the origin: multiply by the factor. A fraction shrinks, a negative factor also flips through the centre."
        ],
        "example": {
            "question": "Rotate (1, 3) by 90° anticlockwise about the origin.",
            "steps": [
                {"label": "Rule", "content": "(x, y) → (−y, x)"},
                {"label": "Apply", "content": "(1, 3) → (−3, 1)"},
                {"label": "Check", "content": "Distance 1 + 9 = 10 kept."},
                {"label": "Answer", "content": "(−3, 1)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: enlargement about a centre, and describing transformations",
        "steps": [
            "Enlarge about a centre: find the vector from the centre to the point, multiply it by the scale factor, then add the centre back.",
            "A negative scale factor sends the image to the opposite side of the centre.",
            "To describe a transformation, test the coordinate rules until one maps every point correctly, then state its full details."
        ],
        "example": {
            "question": "Enlarge (4, 1) by scale factor 2, centre (2, 1).",
            "steps": [
                {"label": "Vector", "content": "(4 − 2, 1 − 1) = (2, 0)"},
                {"label": "Scale", "content": "× 2 = (4, 0)"},
                {"label": "Add centre", "content": "(2 + 4, 1 + 0) = (6, 1)"},
                {"label": "Check", "content": "Image is twice as far from the centre."},
                {"label": "Answer", "content": "(6, 1)", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------- guided.opener + teach ----------
pd["guided"] = {
    "opener": {
        "display": ("Picture a counter sitting on a square grid, on the square 1 across and 2 up, "
                    "which we write as (1, 2)."),
        "steps": [
            {"pre": "You slide the counter 3 squares right. Its across-number (x) goes from 1 to 1 + 3 = ",
             "post": "", "answer": 4, "hint": "One plus three."},
            {"pre": "You also slide it 2 squares up. Its up-number (y) goes from 2 to 2 + 2 = ",
             "post": "", "answer": 4, "hint": "Two plus two."},
            {"say": "You just did a <strong>translation</strong>: every point slides the same way. Right adds to x, up adds to y. We record the slide as a column vector, here \\(\\binom{3}{2}\\)."},
            {"pre": "Now fold the grid flat along the horizontal middle line. A point 3 squares above it lands 3 squares below, so a height of y = 3 becomes y = ",
             "post": "", "answer": -3, "hint": "Same distance, other side of the line."},
            {"say": "That fold is a <strong>reflection</strong>. Translation (slide), reflection (flip), rotation (turn) and enlargement (resize) are the four moves in this lesson."}
        ]
    },
    "teach": {
        "bronze": {
            "display": "Point M(3, 4) is translated by \\(\\binom{2}{-5}\\). Find M'.",
            "steps": [
                {"say": "A translation slides every point by the vector. Do the x and y separately."},
                {"pre": "New x: 3 + 2 = ", "post": "", "answer": 5, "hint": "Three plus two."},
                {"pre": "New y: 4 + (−5) = ", "post": "", "answer": -1, "hint": "Four take away five."},
                {"say": "So M' = (5, −1)."},
                {"pre": "Check the slide right: 5 − 3 = ", "post": "", "answer": 2,
                 "hint": "Should match the top of the vector.", "done": "Matches +2."},
                {"pre": "Check the slide down: −1 − 4 = ", "post": "", "answer": -5,
                 "hint": "Should match the bottom of the vector.",
                 "done": "Matches −5, so M' = (5, −1) is right."}
            ]
        },
        "silver": {
            "display": "Point N(3, 4) is rotated 90° clockwise about the origin. Find N'.",
            "steps": [
                {"say": "90° clockwise about the origin uses the rule (x, y) → (y, −x). The new move: take the old y, then negate the old x."},
                {"pre": "The new x is the old y, so new x = ", "post": "", "answer": 4,
                 "hint": "The old y is 4."},
                {"pre": "The new y is minus the old x: −(3) = ", "post": "", "answer": -3,
                 "hint": "Old x is 3, negate it."},
                {"say": "So N' = (4, −3)."},
                {"pre": "Check the distance is kept. Old: 3² + 4² = 9 + 16 = ", "post": "", "answer": 25,
                 "hint": "Square each and add."},
                {"pre": "Image: 4² + 3² = 16 + 9 = ", "post": "", "answer": 25,
                 "hint": "Square each and add.",
                 "done": "Same distance 25 from the origin, so N' = (4, −3) is right."}
            ]
        },
        "gold": {
            "display": "Point R(7, 5) is enlarged by scale factor 2, centre (1, 2). Find R'.",
            "steps": [
                {"say": "About a centre that is not the origin, use the vector from the centre. The new move: scale that vector, then add the centre back."},
                {"pre": "Vector from centre across: 7 − 1 = ", "post": "", "answer": 6,
                 "hint": "Point x minus centre x."},
                {"pre": "Vector from centre up: 5 − 2 = ", "post": "", "answer": 3,
                 "hint": "Point y minus centre y."},
                {"pre": "Scale across by 2: 6 × 2 = ", "post": "", "answer": 12, "hint": "Double the 6."},
                {"pre": "Add the centre back across: 1 + 12 = ", "post": "", "answer": 13,
                 "hint": "Centre x plus scaled across."},
                {"pre": "And up: 2 + (3 × 2) = 2 + 6 = ", "post": "", "answer": 8,
                 "hint": "Centre y plus scaled up.", "done": "So R' = (13, 8)."},
                {"pre": "Check R' is twice as far: 13 − 1 = ", "post": "", "answer": 12,
                 "hint": "Should be double the original 6.",
                 "done": "12 is 2 × 6, so R' = (13, 8) is right."}
            ]
        }
    }
}

json.dump(pd, io.open("lesson_maths-aqa_geometry-L04.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written lesson_maths-aqa_geometry-L04.json")

# quick word counts for budgets
def words(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
for t in ("bronze", "silver", "gold"):
    print(t, "guide steps words:", sum(words(s) for s in pd["tier_guides"][t]["steps"]))
print("method content words:", words(pd["method_card"]["content"]))
print("method steps:", len(pd["method_card"]["steps"]))
