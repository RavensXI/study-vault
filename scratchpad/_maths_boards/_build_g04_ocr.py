# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # unicode minus

# ---------- SVG grid generator ----------
def grid_svg(xmax, ymax, points, aria):
    """points: list of dicts {x,y,label,kind:'obj'|'img'|'centre',anchor:'start'|'end'}"""
    L, T, RW, TH = 20.0, 20.0, 184.0, 160.0
    cell = min(RW / xmax, TH / ymax)
    right = L + xmax * cell
    bottom = T + ymax * cell
    def gx(v): return L + v * cell
    def gy(v): return bottom - v * cell
    s = ['<svg viewBox="0 0 224 200" role="img" aria-label="%s" style="max-width:260px;font-family:Inter,sans-serif">' % aria]
    # faint grid
    for i in range(xmax + 1):
        x = gx(i)
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-opacity="0.12" stroke-width="1"/>' % (x, bottom, x, T))
    for j in range(ymax + 1):
        y = gy(j)
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-opacity="0.12" stroke-width="1"/>' % (L, y, right, y))
    # bold axes (x=0 vertical, y=0 horizontal)
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.6"/>' % (L, gy(0), right, gy(0)))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.6"/>' % (gx(0), bottom, gx(0), T))
    for p in points:
        px, py = gx(p["x"]), gy(p["y"])
        anchor = p.get("anchor", "start")
        lx = px + 6 if anchor == "start" else px - 6
        ly = py - 6
        if p["kind"] == "centre":
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.8"/>' % (px - 4, py - 4, px + 4, py + 4))
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.8"/>' % (px - 4, py + 4, px + 4, py - 4))
        else:
            col = "#60a5fa" if p["kind"] == "obj" else "#f59e0b"
            op = "0.55" if p["kind"] == "obj" else "0.5"
            s.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s" fill-opacity="%s" stroke="currentColor" stroke-width="1.3"/>' % (px, py, col, op))
        s.append('<text x="%.1f" y="%.1f" font-size="10" text-anchor="%s" font-weight="600" fill="currentColor">%s</text>' % (lx, ly, anchor, p["label"]))
    s.append('</svg>')
    return "".join(s)

svg_S3 = grid_svg(6, 4, [
    {"x": 5, "y": 3, "label": "(5, 3)", "kind": "obj", "anchor": "end"},
    {"x": 1, "y": 1, "label": "centre (1, 1)", "kind": "centre", "anchor": "start"},
], "Point (5, 3) and the centre of enlargement (1, 1) on a coordinate grid")

svg_S4 = grid_svg(6, 8, [
    {"x": 2, "y": 3, "label": "(2, 3)", "kind": "obj", "anchor": "start"},
    {"x": 5, "y": 7, "label": "(5, 7)", "kind": "img", "anchor": "end"},
], "A point (2, 3) and its image (5, 7) on a coordinate grid")

svg_G0 = grid_svg(4, 3, [
    {"x": 3, "y": 2, "label": "(3, 2)", "kind": "obj", "anchor": "end"},
    {"x": 1, "y": 1, "label": "centre (1, 1)", "kind": "centre", "anchor": "start"},
], "Point (3, 2) and the centre of enlargement (1, 1) on a coordinate grid")

svg_G3 = grid_svg(5, 7, [
    {"x": 4, "y": 6, "label": "(4, 6)", "kind": "obj", "anchor": "end"},
    {"x": 2, "y": 2, "label": "centre (2, 2)", "kind": "centre", "anchor": "start"},
], "Point (4, 6) and the centre of enlargement (2, 2) on a coordinate grid")

# ---------- problem bank (OCR bank preserved, enriched) ----------
def mc(display, options, correct_idx, hint, mpattern, expect, message):
    return {
        "display": display, "options": options, "solutions": [correct_idx],
        "calculator": False, "input_type": "multiple_choice",
        "misconceptions": [{"pattern": mpattern, "expect": expect, "message": message}],
        "hint": hint,
    }

def sv(display, sol, hint, mpattern, expect, message, guided_steps):
    return {
        "display": display, "solutions": [sol], "calculator": False,
        "input_type": "single_value",
        "misconceptions": [{"pattern": mpattern, "expect": expect, "message": message}],
        "hint": hint, "guided_steps": guided_steps,
    }

bronze = [
    mc("Translate \\((4, 2)\\) by \\(\\binom{3}{-1}\\).",
       ["\\((7, 1)\\)", "\\((7, 3)\\)", "\\((1, 3)\\)", "\\((1, 1)\\)"], 0,
       "Add the vector: x + 3 and y + (−1).",
       "ignored_sign", 1,
       "The vector is (3, −1), so y goes down by 1: 2 + (−1) = 1. Adding 1 instead gives (7, 3)."),
    mc("Translate \\((1, 5)\\) by \\(\\binom{-3}{2}\\).",
       ["\\((-2, 7)\\)", "\\((4, 3)\\)", "\\((-2, 3)\\)", "\\((4, 7)\\)"], 0,
       "Add each part of the vector to the matching coordinate.",
       "subtract_y", 2,
       "The vector is (−3, 2): x goes 1 − 3 = −2 and y goes 5 + 2 = 7. Subtracting the 2 instead gives (−2, 3)."),
    mc("Reflect \\((3, 2)\\) in the x-axis.",
       ["\\((3, -2)\\)", "\\((-3, 2)\\)", "\\((-3, -2)\\)", "\\((2, 3)\\)"], 0,
       "Reflecting in the x-axis keeps x and flips the sign of y.",
       "wrong_axis", 1,
       "Reflecting in the x-axis flips y: (3, 2) → (3, −2). Flipping x instead (the y-axis rule) gives (−3, 2)."),
    mc("Reflect \\((5, -1)\\) in the y-axis.",
       ["\\((-5, -1)\\)", "\\((5, 1)\\)", "\\((-5, 1)\\)", "\\((-1, 5)\\)"], 0,
       "Reflecting in the y-axis keeps y and flips the sign of x.",
       "wrong_axis", 1,
       "Reflecting in the y-axis flips x: (5, −1) → (−5, −1). Flipping y instead gives (5, 1), a reflection in the x-axis."),
    mc("Reflect \\((2, 7)\\) in the line \\(y = x\\).",
       ["\\((7, 2)\\)", "\\((-2, -7)\\)", "\\((2, -7)\\)", "\\((-7, -2)\\)"], 0,
       "Reflecting in y = x swaps the x and y coordinates.",
       "flip_not_swap", 2,
       "Reflecting in y = x swaps the coordinates: (2, 7) → (7, 2). Just changing the sign of y gives (2, −7)."),
    mc("Rotate \\((1, 0)\\) 90° anticlockwise about the origin.",
       ["\\((0, 1)\\)", "\\((-1, 0)\\)", "\\((0, -1)\\)", "\\((1, 0)\\)"], 0,
       "90° anticlockwise about the origin sends (x, y) to (−y, x).",
       "wrong_direction", 2,
       "90° anticlockwise sends (x, y) to (−y, x): (1, 0) → (0, 1). Using the clockwise rule (y, −x) gives (0, −1)."),
    mc("Enlarge \\((3, 1)\\) by SF 2 from origin.",
       ["\\((6, 2)\\)", "\\((5, 3)\\)", "\\((1.5, 0.5)\\)", "\\((3, 2)\\)"], 0,
       "From the origin, multiply each coordinate by the scale factor.",
       "add_sf", 1,
       "Multiply each coordinate by 2: (6, 2). Adding 2 to each instead gives (5, 3)."),
    mc("Enlarge \\((4, 2)\\) by SF 3 from origin.",
       ["\\((12, 6)\\)", "\\((7, 5)\\)", "\\((1, 0)\\)", "\\((4, 6)\\)"], 0,
       "Multiply each coordinate by the scale factor 3.",
       "add_sf", 1,
       "Multiply each coordinate by 3: (12, 6). Adding 3 to each instead gives (7, 5)."),
]

silver = [
    mc("Reflect \\((4, 1)\\) in the line \\(y = -x\\).",
       ["\\((-1, -4)\\)", "\\((1, 4)\\)", "\\((-4, -1)\\)", "\\((4, -1)\\)"], 0,
       "Reflecting in y = −x sends (x, y) to (−y, −x).",
       "negate_both", 2,
       "Reflecting in y = −x sends (x, y) to (−y, −x): (4, 1) → (−1, −4). Negating both coordinates instead gives (−4, −1)."),
    mc("Rotate \\((3, 1)\\) 180° about the origin.",
       ["\\((-3, -1)\\)", "\\((3, -1)\\)", "\\((-3, 1)\\)", "\\((1, 3)\\)"], 0,
       "A 180° turn about the origin flips the sign of both coordinates.",
       "one_coord_only", 1,
       "A 180° rotation negates both coordinates: (3, 1) → (−3, −1). Negating only y gives (3, −1)."),
    mc("Enlarge \\((2, 4)\\) by SF ½ from centre \\((0, 0)\\).",
       ["\\((1, 2)\\)", "\\((4, 8)\\)", "\\((2, 4)\\)", "\\((0, 2)\\)"], 0,
       "A scale factor of one half means halve each coordinate.",
       "double", 1,
       "Scale factor ½ halves each coordinate: (2, 4) → (1, 2). Multiplying by 2 instead gives (4, 8)."),
    mc(svg_S3 + " Enlarge \\((5, 3)\\) by SF 2 from centre \\((1, 1)\\).",
       ["\\((9, 5)\\)", "\\((10, 6)\\)", "\\((11, 7)\\)", "\\((3, 1)\\)"], 0,
       "Work from the centre: scale the vector from (1, 1), then add it back.",
       "from_origin", 1,
       "From the centre (1, 1): vector (4, 2) × 2 = (8, 4), added to the centre gives (9, 5). Enlarging from the origin instead gives (10, 6)."),
    sv(svg_S4 + " Describe: \\((2, 3) \\to (5, 7)\\). What is the translation vector x-component?",
       3, "The vector is the new point minus the old point.",
       "reverse", -3,
       "The vector is new − old, so 5 − 2 = 3. Doing old − new gives −3.",
       [
           {"say": "A translation is described by its vector, found as new point minus old point. Do each part separately."},
           {"pre": "First the y-part (a check): the new y minus the old y, 7 − 3 = ", "post": "", "answer": 4, "hint": "Seven take away three."},
           {"pre": "Now the x-part, which the question asks for: new x minus old x, 5 − 2 = ", "post": "", "answer": 3, "hint": "Five take away two.", "phase": "substitute"},
           {"pre": "Check by sliding the old point across: 2 + 3 = ", "post": "", "answer": 5, "hint": "Old x plus the vector x should give the new x, 5.", "done": "It lands on 5, so the x-component is 3."},
       ]),
    sv("A shape is enlarged by SF 3. If the original area is 5 cm², what is the new area?",
       45, "Area scales by the square of the scale factor.",
       "linear_not_area", 15,
       "Area scales by the square of the SF: 5 × 3² = 45. Multiplying by the SF itself gives 15.",
       [
           {"say": "Lengths scale by the scale factor, but area scales by the scale factor squared."},
           {"pre": "The area scale factor is 3² = ", "post": "", "answer": 9, "hint": "Three squared."},
           {"pre": "New area = original × area SF, so 5 × 9 = ", "post": " cm²", "answer": 45, "hint": "Five times nine.", "phase": "substitute"},
           {"pre": "Check by dividing back: 45 ÷ 9 = ", "post": " cm²", "answer": 5, "hint": "Should return the original 5.", "done": "It returns 5 cm², so the new area is 45 cm²."},
       ]),
    mc("Rotate \\((0, 4)\\) 90° clockwise about the origin.",
       ["\\((4, 0)\\)", "\\((-4, 0)\\)", "\\((0, -4)\\)", "\\((0, 4)\\)"], 0,
       "90° clockwise about the origin sends (x, y) to (y, −x).",
       "wrong_direction", 1,
       "90° clockwise sends (x, y) to (y, −x): (0, 4) → (4, 0). Using the anticlockwise rule (−y, x) gives (−4, 0)."),
]

gold = [
    mc(svg_G0 + " Enlarge \\((3, 2)\\) by SF −2 from centre \\((1, 1)\\).",
       ["\\((-3, -1)\\)", "\\((5, 3)\\)", "\\((-5, -3)\\)", "\\((-1, -3)\\)"], 0,
       "Scale the vector from the centre by −2, then add the centre back.",
       "positive_sf", 1,
       "The scale factor is −2, so vector (2, 1) becomes (−4, −2); added to the centre (1, 1) gives (−3, −1). Using +2 gives (5, 3)."),
    mc("A shape is enlarged by SF −1. This is equivalent to which transformation?",
       ["180° rotation about the centre", "Reflection in the x-axis", "Translation", "No change"], 0,
       "Think about where a point goes when it is flipped through the centre.",
       "confused_reflection", 1,
       "A scale factor of −1 about a point is a 180° rotation about that point, not a reflection. A reflection in the x-axis only flips vertically."),
    sv("A shape is enlarged by SF 2. The original perimeter is 12 cm. Find the new perimeter.",
       24, "Perimeter is a length, so it scales by the scale factor itself.",
       "used_area_sf", 48,
       "Perimeter is a length, so it scales by the SF: 12 × 2 = 24. Squaring the SF (the area rule) gives 48.",
       [
           {"say": "Perimeter is a length. Lengths scale by the scale factor itself, not its square."},
           {"pre": "The scale factor for lengths is just the SF, so it is ", "post": "", "answer": 2, "hint": "The same scale factor, 2."},
           {"pre": "New perimeter = 12 × 2 = ", "post": " cm", "answer": 24, "hint": "Twelve times two.", "phase": "substitute"},
           {"pre": "Check by dividing back: 24 ÷ 2 = ", "post": " cm", "answer": 12, "hint": "Should return the original 12.", "done": "It returns 12 cm, so the new perimeter is 24 cm."},
       ]),
    mc(svg_G3 + " Enlarge \\((4, 6)\\) by SF −½ from centre \\((2, 2)\\).",
       ["\\((1, 0)\\)", "\\((3, 4)\\)", "\\((0, -2)\\)", "\\((5, 4)\\)"], 0,
       "Scale the vector from the centre by −½, then add the centre back.",
       "positive_sf", 1,
       "With SF −½: vector (2, 4) × (−½) = (−1, −2), added to the centre (2, 2) gives (1, 0). Using +½ gives (3, 4)."),
    sv("A shape has area 8 cm². After enlargement, area = 200 cm². Find the scale factor.",
       5, "Divide the areas, then take the square root.",
       "forgot_sqrt", 25,
       "Area SF = 200 ÷ 8 = 25, and the length SF is √25 = 5. Stopping at 25 gives the area factor, not the length factor.",
       [
           {"say": "Areas scale by the square of the length scale factor, so undo that by dividing then square-rooting."},
           {"pre": "Area scale factor = 200 ÷ 8 = ", "post": "", "answer": 25, "hint": "Two hundred divided by eight."},
           {"pre": "Length scale factor = √25 = ", "post": "", "answer": 5, "hint": "The square root of 25.", "phase": "substitute"},
           {"pre": "Check: 8 × 5² = 8 × 25 = ", "post": " cm²", "answer": 200, "hint": "Should return the new area, 200.", "done": "It returns 200 cm², so the scale factor is 5."},
       ]),
]

# ---------- teach walks ----------
teach = {
    "bronze": {
        "display": "Point M(2, 5) is translated by \\(\\binom{3}{-4}\\). Find M'.",
        "steps": [
            {"say": "A translation slides every point by the vector. Do the x and y separately."},
            {"pre": "New x: 2 + 3 = ", "post": "", "answer": 5, "hint": "Two plus three."},
            {"pre": "New y: 5 + (−4) = ", "post": "", "answer": 1, "hint": "Five take away four."},
            {"say": "So M' = (5, 1)."},
            {"pre": "Check the slide right: 5 − 2 = ", "post": "", "answer": 3, "hint": "Should match the top of the vector."},
            {"pre": "Check the slide down: 1 − 5 = ", "post": "", "answer": -4, "hint": "Should match the bottom of the vector.", "done": "Matches −4, so M' = (5, 1) is right."},
        ],
    },
    "silver": {
        "display": "Point N(4, 3) is rotated 90° clockwise about the origin. Find N'.",
        "steps": [
            {"say": "90° clockwise about the origin uses the rule (x, y) → (y, −x). The new move: take the old y, then negate the old x."},
            {"pre": "The new x is the old y, so new x = ", "post": "", "answer": 3, "hint": "The old y is 3."},
            {"pre": "The new y is minus the old x: −(4) = ", "post": "", "answer": -4, "hint": "Old x is 4, negate it."},
            {"say": "So N' = (3, −4)."},
            {"pre": "Check the distance. Old: 4² + 3² = 16 + 9 = ", "post": "", "answer": 25, "hint": "Square each and add."},
            {"pre": "Image: 3² + 4² = 9 + 16 = ", "post": "", "answer": 25, "hint": "Square each and add.", "done": "Same distance 25 from the origin, so N' = (3, −4) is right."},
        ],
    },
    "gold": {
        "display": "Point R(5, 4) is enlarged by scale factor −2, centre (1, 1). Find R'.",
        "steps": [
            {"say": "About a centre that is not the origin, use the vector from the centre. The new move: scale that vector, then add the centre back. A negative factor also flips to the opposite side."},
            {"pre": "Vector from centre across: 5 − 1 = ", "post": "", "answer": 4, "hint": "Point x minus centre x."},
            {"pre": "Vector from centre up: 4 − 1 = ", "post": "", "answer": 3, "hint": "Point y minus centre y."},
            {"pre": "Scale across by −2: 4 × (−2) = ", "post": "", "answer": -8, "hint": "Four times minus two."},
            {"pre": "Add the centre back across: 1 + (−8) = ", "post": "", "answer": -7, "hint": "Centre x plus scaled across."},
            {"pre": "And up: 1 + (3 × −2) = 1 + (−6) = ", "post": "", "answer": -5, "hint": "Centre y plus scaled up.", "done": "So R' = (−7, −5)."},
            {"pre": "Check R' is on the opposite side: −7 − 1 = ", "post": "", "answer": -8, "hint": "Should be −2 times the original vector part 4.", "done": "−8 is −2 × 4, so R' = (−7, −5) is right."},
        ],
    },
}

# ---------- tier guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: single transformations on a point",
        "steps": [
            "Translation: add the column vector to the point. Right and up count as positive, left and down as negative.",
            "Reflection: in the x-axis flip the sign of y, in the y-axis flip the sign of x, in y = x swap the two coordinates.",
            "Rotation 90° anticlockwise about the origin sends (x, y) to (−y, x); enlargement from the origin multiplies each coordinate by the scale factor.",
        ],
        "example": {
            "question": "Reflect (5, 2) in the x-axis.",
            "steps": [
                {"label": "Rule", "content": "In the x-axis, flip the sign of y."},
                {"label": "Apply", "content": "(5, 2) → (5, −2)"},
                {"label": "Check", "content": "x is unchanged, y kept the same distance."},
                {"label": "Answer", "content": "(5, −2)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: rotations, y = −x, and enlargements by a factor or centre",
        "steps": [
            "Rotate about the origin: 90° clockwise (x, y) → (y, −x); anticlockwise (−y, x); 180° (−x, −y).",
            "Reflect in y = −x: (x, y) → (−y, −x).",
            "Enlarge from a centre: scale the vector from the centre by the factor, then add the centre. Areas scale by the factor squared.",
        ],
        "example": {
            "question": "Enlarge (4, 3) by scale factor 2, centre (2, 1).",
            "steps": [
                {"label": "Vector", "content": "(4 − 2, 3 − 1) = (2, 2)"},
                {"label": "Scale", "content": "× 2 = (4, 4)"},
                {"label": "Add centre", "content": "(2 + 4, 1 + 4) = (6, 5)"},
                {"label": "Check", "content": "Image is twice as far from the centre."},
                {"label": "Answer", "content": "(6, 5)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: negative enlargements and scale-factor reasoning",
        "steps": [
            "Enlarge by a negative factor about a centre: scale the vector from the centre by the negative factor, then add the centre. The image lands on the opposite side.",
            "Lengths and perimeters scale by the factor; areas scale by the factor squared.",
            "To find a length scale factor from areas, divide the areas then take the square root.",
        ],
        "example": {
            "question": "Enlarge (3, 4) by scale factor −1, centre (1, 1).",
            "steps": [
                {"label": "Vector", "content": "(3 − 1, 4 − 1) = (2, 3)"},
                {"label": "Scale", "content": "× (−1) = (−2, −3)"},
                {"label": "Add centre", "content": "(1 − 2, 1 − 3) = (−1, −2)"},
                {"label": "Check", "content": "Same distance, opposite side of the centre."},
                {"label": "Answer", "content": "(−1, −2)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- opener ----------
opener = {
    "display": "Picture a counter on a square grid, sitting on the square 2 across and 1 up, which we write as (2, 1).",
    "steps": [
        {"pre": "Slide the counter 4 squares right. Its across-number (x) goes from 2 to 2 + 4 = ", "post": "", "answer": 6, "hint": "Two plus four."},
        {"pre": "Slide it 3 squares up. Its up-number (y) goes from 1 to 1 + 3 = ", "post": "", "answer": 4, "hint": "One plus three."},
        {"say": "You just did a <strong>translation</strong>: every point slides the same way. Right adds to x, up adds to y. We record the slide as a column vector, here \\(\\binom{4}{3}\\)."},
        {"pre": "Now fold the grid flat along the horizontal middle line. A point 2 squares above it drops to 2 squares below, so a height of y = 2 becomes y = ", "post": "", "answer": -2, "hint": "Same distance, other side of the line."},
        {"say": "That fold is a <strong>reflection</strong>. Translation (slide), reflection (flip), rotation (turn) and enlargement (resize) are the four moves in this lesson."},
    ],
}

# ---------- method card ----------
method_card = {
    "title": "Transformations",
    "steps": [
        "Translation: add the column vector to each coordinate.",
        "Reflection: x-axis flips y, y-axis flips x, y = x swaps, y = −x goes to (−y, −x).",
        "Rotation about the origin: 90° CW (y, −x), 90° ACW (−y, x), 180° (−x, −y).",
        "Enlargement: scale the vector from the centre by the SF, then add the centre. Areas scale by SF².",
    ],
    "content": "<p><strong>Translation:</strong> slide by a column vector \\(\\binom{a}{b}\\); add a to x and b to y.</p><p><strong>Reflection:</strong> mirror in a line. In the x-axis flip y, in the y-axis flip x, in y = x swap the coordinates.</p><p><strong>Rotation:</strong> turn about a centre; state the angle and direction. About the origin, 90° clockwise sends (x, y) to (y, −x).</p><p><strong>Enlargement:</strong> scale from a centre by a factor. A negative factor flips through the centre; a fraction shrinks. Lengths scale by the factor, areas by the factor squared.</p>",
    "example": "<p><strong>Translate \\((3, 2)\\) by \\(\\binom{-4}{1}\\).</strong></p><p>New point: \\((3-4, 2+1) = (-1, 3)\\).</p>",
}

worked_examples = [
    {"steps": [{"label": "Answer", "content": "<p>(5−2, 3+4) = (3, 7)</p>", "isAnswer": True, "is_answer": True}],
     "question": "Translate (5, 3) by the vector (−2, 4). Find the image.", "difficulty": "Bronze"},
    {"steps": [{"label": "Step 1", "content": "<p>Reflection in y = x: swap x and y.</p>"},
               {"label": "Answer", "content": "<p>(1, 4)</p>", "isAnswer": True, "is_answer": True}],
     "question": "Reflect (4, 1) in the line y = x. Find the image.", "difficulty": "Silver"},
    {"steps": [{"label": "Step 1", "content": "<p>Vector from centre: (1, 2). ×(−2): (−2, −4).</p>"},
               {"label": "Answer", "content": "<p>Image: (1−2, 1−4) = (−1, −3)</p>", "isAnswer": True, "is_answer": True}],
     "question": "Enlarge (2, 3) by SF −2 from centre (1, 1). Find the image.", "difficulty": "Gold"},
]

pd = {
    "method_card": method_card,
    "topic_links": {"prerequisites": []},
    "problem_bank": {
        "bronze": bronze,
        "silver": silver,
        "gold": gold,
        "bronze_description": "Apply one transformation to a point: translate, reflect in an axis or y = x, rotate about the origin, or enlarge from the origin.",
        "silver_description": "Reflect in y = −x, rotate 180° or 90°, enlarge by a fraction or about a given centre, and use area scale factors.",
        "gold_description": "Enlarge by a negative scale factor about a centre, and reason with perimeter and area scale factors.",
    },
    "related_videos": [],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
}

with io.open("lesson_maths-ocr_geometry-L04.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("written lesson_maths-ocr_geometry-L04.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
