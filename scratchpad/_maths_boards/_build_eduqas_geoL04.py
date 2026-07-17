# -*- coding: utf-8 -*-
"""Build guided + diagrams practice_data for maths-eduqas geometry-L04 (Transformations)."""
import json, io

pd = json.load(io.open("_live_L04.json", encoding="utf-8"))
pb = pd["problem_bank"]

def _f(v):
    return ("%g" % round(v, 1))

def grid_svg(xmin, xmax, ymin, ymax, aria, obj=None, obj_label=None,
             img=None, line_yx=False, w_target=190):
    wu = xmax - xmin
    hu = ymax - ymin
    s = min(24.0, w_target / wu)
    m = 16.0
    W = 2 * m + wu * s
    H = 2 * m + hu * s
    def px(x): return m + (x - xmin) * s
    def py(y): return m + (ymax - y) * s
    out = []
    out.append("<svg viewBox='0 0 %s %s' role=\"img\" aria-label=\"%s\" style='max-width:220px;width:100%%;height:auto;font-family:Inter,sans-serif'>" % (_f(W), _f(H), aria))
    for xi in range(xmin, xmax + 1):
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-opacity='0.15' stroke-width='1'/>" % (_f(px(xi)), _f(py(ymax)), _f(px(xi)), _f(py(ymin))))
    for yi in range(ymin, ymax + 1):
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-opacity='0.15' stroke-width='1'/>" % (_f(px(xmin)), _f(py(yi)), _f(px(xmax)), _f(py(yi))))
    if ymin <= 0 <= ymax:
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-width='1.6'/>" % (_f(px(xmin)), _f(py(0)), _f(px(xmax)), _f(py(0))))
    if xmin <= 0 <= xmax:
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-width='1.6'/>" % (_f(px(0)), _f(py(ymax)), _f(px(0)), _f(py(ymin))))
    if line_yx:
        lo = max(xmin, ymin); hi = min(xmax, ymax)
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='#f59e0b' stroke-width='1.6' stroke-dasharray='4 3'/>" % (_f(px(lo)), _f(py(lo)), _f(px(hi)), _f(py(hi))))
        out.append("<text x='%s' y='%s' fill='currentColor' font-size='11' text-anchor='end'>y = x</text>" % (_f(px(hi) - 3), _f(py(hi) - 4)))
    if obj is not None:
        out.append("<circle cx='%s' cy='%s' r='4.5' fill='#60a5fa' fill-opacity='0.85' stroke='currentColor' stroke-width='1.4'/>" % (_f(px(obj[0])), _f(py(obj[1]))))
        if obj_label:
            out.append("<text x='%s' y='%s' fill='currentColor' font-size='11' text-anchor='start' font-weight='bold'>%s</text>" % (_f(px(obj[0]) + 7), _f(py(obj[1]) - 6), obj_label))
    if img is not None:
        out.append("<text x='%s' y='%s' fill='currentColor' font-size='13' text-anchor='middle' font-weight='bold'>?</text>" % (_f(px(img[0])), _f(py(img[1]) + 5)))
    out.append("</svg>")
    return "".join(out)

def setp(prob, hint, mis):
    prob["hint"] = hint
    prob["misconceptions"] = [{"pattern": p, "expect": e, "message": m} for (p, e, m) in mis]

B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# BRONZE
setp(B[0], "Add the vector to the point: new x = 2 + 3, new y = 5 + (−2).", [
    ("added_y", 1, "The y-part of the vector is −2, so subtract: 5 + (−2) = 3. Adding gives 7, which is wrong."),
    ("ignored_x", 3, "Do not leave x unchanged. Add 3 to it: 2 + 3 = 5."),
])
setp(B[1], "Reflecting in the x-axis keeps x the same and flips the sign of y.", [
    ("wrong_axis", 1, "You reflected in the y-axis. In the x-axis, x stays and y flips: (4, −1)."),
    ("flipped_both", 3, "Only the y-coordinate changes sign in the x-axis. x stays 4, so (4, −1)."),
])
setp(B[2], "Reflecting in the y-axis flips the sign of x and keeps y the same.", [
    ("wrong_axis", 1, "You reflected in the x-axis. In the y-axis, x flips and y stays: (−3, −2)."),
    ("flipped_both", 2, "Only the x-coordinate changes sign in the y-axis. y stays −2, so (−3, −2)."),
])
setp(B[3], "Vector = destination − start: (4 − 1, 2 − 6).", [
    ("reversed", 1, "You did start − destination. Take destination − start: (4 − 1, 2 − 6) = (3, −4)."),
    ("added", 3, "Do not add the points. Subtract start from destination: (3, −4)."),
])
setp(B[4], "Rotating 90° clockwise about the origin sends (x, y) to (y, −x).", [
    ("anticlockwise", 1, "That is the anticlockwise result. Clockwise 90°: (x, y) → (y, −x), so (0, 3) → (3, 0)."),
    ("used_180", 2, "A 180° turn gives (0, −3). A 90° clockwise turn gives (3, 0)."),
])
setp(B[5], "Area scales by the scale factor squared: 12 × 2².", [
    ("linear_scale", 1, "You multiplied by the scale factor once. Area scales by SF²: 12 × 4 = 48."),
    ("divided", 3, "An enlargement makes the area larger, not smaller. 12 × 2² = 48."),
])
setp(B[6], "Add each part of the vector: new x = −1 + (−3), new y = 4 + (−5).", [
    ("subtracted_vector", 1, "You subtracted the vector. Add it: (−1 + (−3), 4 + (−5)) = (−4, −1)."),
    ("wrong_x_sign", 3, "Both parts move in the negative direction. x: −1 + (−3) = −4, not 2."),
])
setp(B[7], "A reflection is a mirror image: it flips the shape but never changes its shape or size.", [
    ("orientation", 1, "A reflection reverses the orientation (it flips). What stays the same is the shape and size."),
    ("position", 2, "The position changes: the shape moves across the mirror line. Shape and size stay the same."),
])

# SILVER
setp(S[0], "Reflecting in the line y = x swaps the x and y coordinates.", [
    ("no_change", 1, "The point does move. Reflecting in y = x swaps the coordinates: (5, 2) → (2, 5)."),
    ("swap_and_negate", 3, "Reflecting in y = x only swaps the coordinates. Do not change the signs: (2, 5)."),
])
setp(S[1], "A 180° rotation about the origin negates both coordinates: (x, y) → (−x, −y).", [
    ("only_one", 1, "You negated only one coordinate. A 180° turn negates both: (2, −3) → (−2, 3)."),
    ("swapped", 2, "A 180° turn does not swap the coordinates. It negates both: (−2, 3)."),
])
setp(S[2], "Compare the coordinates: which one changes sign? The x-axis reflection flips y.", [
    ("wrong_axis", 1, "The x-coordinates stayed the same and only y changed sign. That is a reflection in the x-axis, not the y-axis."),
    ("rotation", 2, "A 180° rotation would flip both signs. Here only y changed sign, so it is a reflection in the x-axis."),
])
setp(S[3], "Enlargement from the origin multiplies both coordinates by the scale factor.", [
    ("added_sf", 1, "You added 3 instead of multiplying. Multiply each coordinate by 3: (6, 15)."),
    ("only_x", 2, "Multiply both coordinates by 3, not just x: (2×3, 5×3) = (6, 15)."),
])
setp(S[4], "Multiply both coordinates by ½. The signs stay the same.", [
    ("doubled", 1, "SF ½ makes the point closer to the origin. Multiply by ½: (4, −3)."),
    ("changed_sign", 2, "Do not change the sign of y. Just multiply by ½: (4, −3)."),
])
setp(S[5], "Rotating 90° anticlockwise about the origin sends (x, y) to (−y, x).", [
    ("clockwise", 1, "That is the clockwise result. Anticlockwise 90°: (x, y) → (−y, x), so (1, 0) → (0, 1)."),
    ("used_180", 2, "A 180° turn gives (−1, 0). A 90° anticlockwise turn gives (0, 1)."),
])
setp(S[6], "Area scales by the scale factor squared: (−2)² = 4, so area × 4.", [
    ("linear_scale", 1, "You multiplied by the scale factor once. Area scales by SF²: 20 × 4 = 80."),
    ("negative_area", 2, "Area is always positive. (−2)² = 4, so the area is 20 × 4 = 80."),
])

# GOLD
setp(G[0], "Find the vector from the centre (3, 2) to the point, multiply by −1, then add it back to the centre.", [
    ("from_origin", 1, "You negated the point itself. Work from the centre (3, 2): the image is (1, −2)."),
    ("sf_ignored", None, "SF −1 sends the point the same distance to the opposite side of the centre (3, 2)."),
])
setp(G[1], "Lengths multiply by the scale factor: 9 × ⅓.", [
    ("inverted_sf", 1, "You multiplied by 3. SF ⅓ makes it smaller: 9 × ⅓ = 3 cm."),
    ("used_area_scale", 2, "Lengths use the scale factor once, not squared: 9 × ⅓ = 3 cm."),
])
setp(G[2], "Add the two vectors part by part: x: 2 + (−5), y: −3 + 1.", [
    ("subtracted", 1, "You subtracted the vectors. Add them: (2 + (−5), −3 + 1) = (−3, −2)."),
    ("wrong_y_sign", 2, "The y-part is −3 + 1 = −2, not +2. The answer is (−3, −2)."),
])
setp(G[3], "Combined enlargements about the same centre multiply their scale factors: 3 × ⅓.", [
    ("sf_9", 1, "Same centre means the scale factors multiply: 3 × ⅓ = 1, not 9. The shape returns to the original."),
    ("sf_ninth", 3, "3 × ⅓ = 1, giving the original shape, not a reduction to SF ⅑."),
])
setp(G[4], "Find the vector from centre (1, 1) to the point, multiply by −2, then add it back to the centre.", [
    ("point_not_vector", 1, "Multiply the vector from the centre by −2, not the point's coordinates. The image is (−3, −5)."),
    ("positive_sf", 2, "The scale factor is negative, so the image is on the opposite side of the centre: (−3, −5)."),
])

# ---- Figures ----
def two_triangles():
    xmin, xmax, ymin, ymax = 0, 4, -4, 4
    s = 20.0; m = 16.0
    W = 2 * m + (xmax - xmin) * s
    H = 2 * m + (ymax - ymin) * s
    def px(x): return m + (x - xmin) * s
    def py(y): return m + (ymax - y) * s
    out = ["<svg viewBox='0 0 %s %s' role=\"img\" aria-label=\"Triangle A above the x-axis and its image B below, both on a coordinate grid\" style='max-width:200px;width:100%%;height:auto;font-family:Inter,sans-serif'>" % (_f(W), _f(H))]
    for xi in range(xmin, xmax + 1):
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-opacity='0.13' stroke-width='1'/>" % (_f(px(xi)), _f(py(ymax)), _f(px(xi)), _f(py(ymin))))
    for yi in range(ymin, ymax + 1):
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-opacity='0.13' stroke-width='1'/>" % (_f(px(xmin)), _f(py(yi)), _f(px(xmax)), _f(py(yi))))
    out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-width='1.6'/>" % (_f(px(xmin)), _f(py(0)), _f(px(xmax)), _f(py(0))))
    out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-width='1.6'/>" % (_f(px(0)), _f(py(ymax)), _f(px(0)), _f(py(ymin))))
    A = [(1, 1), (3, 1), (1, 3)]; Bt = [(1, -1), (3, -1), (1, -3)]
    ptsA = " ".join("%s,%s" % (_f(px(x)), _f(py(y))) for x, y in A)
    ptsB = " ".join("%s,%s" % (_f(px(x)), _f(py(y))) for x, y in Bt)
    out.append("<polygon points='%s' fill='#60a5fa' fill-opacity='0.3' stroke='currentColor' stroke-width='1.6'/>" % ptsA)
    out.append("<polygon points='%s' fill='#34d399' fill-opacity='0.3' stroke='currentColor' stroke-width='1.6'/>" % ptsB)
    out.append("<text x='%s' y='%s' fill='currentColor' font-size='11' text-anchor='middle' font-weight='bold'>A</text>" % (_f(px(1.6)), _f(py(1.7))))
    out.append("<text x='%s' y='%s' fill='currentColor' font-size='11' text-anchor='middle' font-weight='bold'>B</text>" % (_f(px(1.6)), _f(py(-1.9))))
    out.append("</svg>")
    return "".join(out)

S[2]["display"] = two_triangles() + S[2]["display"]
B[1]["display"] = grid_svg(0, 5, -2, 2, "Point (4, 1) above the x-axis, the x-axis is the mirror line", obj=(4, 1), obj_label="(4, 1)", img=(4, -1)) + B[1]["display"]
B[4]["display"] = grid_svg(-1, 4, -1, 4, "Point (0, 3) on a grid with the origin as the centre of rotation", obj=(0, 3), obj_label="(0, 3)", img=(3, 0)) + B[4]["display"]
S[0]["display"] = grid_svg(0, 6, 0, 6, "Point (5, 2) on a grid with the mirror line y equals x drawn", obj=(5, 2), obj_label="(5, 2)", img=(2, 5), line_yx=True) + S[0]["display"]
S[5]["display"] = grid_svg(-1, 2, -1, 2, "Point (1, 0) on a grid with the origin as the centre of rotation", obj=(1, 0), obj_label="(1, 0)", img=(0, 1)) + S[5]["display"]

# ---- Opener ----
def opener_svg():
    xmin, xmax, ymin, ymax = 0, 6, 0, 5
    s = 24.0; m = 16.0
    W = 2 * m + (xmax - xmin) * s
    H = 2 * m + (ymax - ymin) * s
    def px(x): return m + (x - xmin) * s
    def py(y): return m + (ymax - y) * s
    out = ["<svg viewBox='0 0 %s %s' role=\"img\" aria-label=\"A game board grid with a counter on (2, 3) and a dashed arrow sliding it 3 right and 1 up\" style='max-width:220px;width:100%%;height:auto;font-family:Inter,sans-serif'>" % (_f(W), _f(H))]
    for xi in range(xmin, xmax + 1):
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-opacity='0.15' stroke-width='1'/>" % (_f(px(xi)), _f(py(ymax)), _f(px(xi)), _f(py(ymin))))
    for yi in range(ymin, ymax + 1):
        out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-opacity='0.15' stroke-width='1'/>" % (_f(px(xmin)), _f(py(yi)), _f(px(xmax)), _f(py(yi))))
    out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-width='1.6'/>" % (_f(px(0)), _f(py(0)), _f(px(xmax)), _f(py(0))))
    out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='currentColor' stroke-width='1.6'/>" % (_f(px(0)), _f(py(0)), _f(px(0)), _f(py(ymax))))
    out.append("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='#f59e0b' stroke-width='1.6' stroke-dasharray='4 3'/>" % (_f(px(2)), _f(py(3)), _f(px(4.8)), _f(py(3.9))))
    out.append("<circle cx='%s' cy='%s' r='6' fill='#60a5fa' fill-opacity='0.85' stroke='currentColor' stroke-width='1.4'/>" % (_f(px(2)), _f(py(3))))
    out.append("<text x='%s' y='%s' fill='currentColor' font-size='11' text-anchor='middle' font-weight='bold'>(2, 3)</text>" % (_f(px(2)), _f(py(3) - 10)))
    out.append("<circle cx='%s' cy='%s' r='4' fill='none' stroke='currentColor' stroke-width='1.4' stroke-dasharray='2 2'/>" % (_f(px(5)), _f(py(4))))
    out.append("</svg>")
    return "".join(out)

pd["guided"] = {
    "opener": {
        "label": "Before any rules",
        "display": opener_svg() + "A counter sits on a game board at the point (2, 3). You slide it 3 squares right and 1 square up.",
        "steps": [
            {"say": "The counter starts at across-position 2. Sliding 3 squares right adds 3.",
             "pre": "Its new across-position (x) is 2 + 3 = ", "post": "", "answer": 5,
             "hint": "Start at 2 and count 3 squares to the right."},
            {"say": "It starts at up-position 3. Sliding 1 square up adds 1.",
             "pre": "Its new up-position (y) is 3 + 1 = ", "post": "", "answer": 4,
             "done": "The counter lands on (5, 4). Every point slid by the same amount.",
             "hint": "Start at 3 and count 1 square up."},
            {"say": "You just did a <strong>translation</strong>: sliding a shape without turning or flipping it. Maths records the slide as a column vector \\(\\binom{3}{1}\\), where the top number is the sideways move and the bottom number is the up or down move."}
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "Translate the point \\((1, 2)\\) by the vector \\(\\binom{4}{-3}\\), then reflect the image in the x-axis.",
            "steps": [
                {"say": "First the translation. Add the vector to the point. Start with x:",
                 "pre": "1 + 4 = ", "post": "", "answer": 5,
                 "hint": "Add the top number of the vector, 4, to the x-coordinate."},
                {"pre": "2 + (−3) = ", "post": "", "answer": -1,
                 "done": "So the image after the slide is (5, −1). That is the translation.",
                 "hint": "Add the bottom number, −3, to the y-coordinate."},
                {"say": "Now reflect (5, −1) in the x-axis. That keeps x the same and flips the sign of y.",
                 "pre": "New y = −(−1) = ", "post": "", "answer": 1,
                 "hint": "Flip the sign of −1."},
                {"say": "The x-coordinate is unchanged by the reflection, so check it is still 5.",
                 "pre": "1 + 4 = ", "post": "", "answer": 5,
                 "done": "x stays 5 and y becomes 1, so the final point is (5, 1)."}
            ]
        },
        "silver": {
            "label": "Together: reflect then rotate",
            "display": "Reflect \\((3, 5)\\) in the line \\(y = x\\), then rotate the image \\(90^\\circ\\) clockwise about the origin.",
            "steps": [
                {"say": "Reflecting in y = x swaps the coordinates. The old y becomes the new x:",
                 "pre": "New x = old y = ", "post": "", "answer": 5,
                 "hint": "The old y-coordinate, 5, moves to the front."},
                {"pre": "New y = old x = ", "post": "", "answer": 3,
                 "done": "So the reflection gives (5, 3). Swapping is the whole y = x move.",
                 "hint": "The old x-coordinate, 3, becomes the new y."},
                {"say": "Now rotate (5, 3) by 90° clockwise about the origin. The rule is (x, y) → (y, −x).",
                 "pre": "New x = old y = ", "post": "", "answer": 3,
                 "hint": "For a clockwise quarter turn the new x is the old y."},
                {"pre": "New y = −(old x) = −(5) = ", "post": "", "answer": -5,
                 "done": "The image is (3, −5). That is the clockwise 90° rule.",
                 "hint": "Flip the sign of the old x, which is 5."},
                {"say": "Check: a rotation never changes the distance from the origin. Compare (5, 3) and (3, −5).",
                 "pre": "3² + (−5)² = 9 + 25 = ", "post": "", "answer": 34,
                 "done": "5² + 3² = 34 too, so the distance matches and the answer checks."}
            ]
        },
        "gold": {
            "label": "Together: enlarge by a negative scale factor",
            "display": "Enlarge the point \\((4, 6)\\) by scale factor \\(-2\\), centre \\((1, 2)\\).",
            "steps": [
                {"say": "First find the vector from the centre (1, 2) to the point (4, 6). Subtract the centre. Start with x:",
                 "pre": "4 − 1 = ", "post": "", "answer": 3,
                 "hint": "Take the centre's x, 1, from the point's x, 4."},
                {"pre": "6 − 2 = ", "post": "", "answer": 4,
                 "done": "The vector from the centre to the point is (3, 4).",
                 "hint": "Take the centre's y, 2, from the point's y, 6."},
                {"say": "Multiply the vector (3, 4) by the scale factor −2.",
                 "pre": "−2 × 3 = ", "post": "", "answer": -6,
                 "hint": "Multiply 3 by −2."},
                {"pre": "−2 × 4 = ", "post": "", "answer": -8,
                 "done": "The new vector is (−6, −8). The negative sign flips it to the opposite side of the centre.",
                 "hint": "Multiply 4 by −2."},
                {"say": "Add the new vector back to the centre (1, 2).",
                 "pre": "Image x = 1 + (−6) = ", "post": "", "answer": -5,
                 "hint": "Add −6 to the centre's x, 1."},
                {"pre": "Image y = 2 + (−8) = ", "post": "", "answer": -6,
                 "done": "The image is (−5, −6).",
                 "hint": "Add −8 to the centre's y, 2."},
                {"say": "Check the scale: the new vector should be −2 times the old one. Divide matching parts.",
                 "pre": "−6 ÷ 3 = ", "post": "", "answer": -2,
                 "done": "The ratio is −2, the scale factor, so the enlargement is correct."}
            ]
        }
    }
}

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: translations and reflections in the axes",
        "steps": [
            "To <strong>translate</strong> a point, add the vector to it: the top number moves it right (or left if negative), the bottom number moves it up (or down).",
            "To <strong>reflect in the x-axis</strong>, keep x and flip the sign of y. To <strong>reflect in the y-axis</strong>, flip the sign of x and keep y.",
            "An enlargement of scale factor k multiplies every length by k and every area by k²."
        ],
        "example": {
            "question": "Translate (2, 3) by the vector \\(\\binom{5}{-1}\\).",
            "steps": [
                {"label": "Rule", "content": "<p>Add the vector to each coordinate.</p>"},
                {"label": "Add", "content": "<p>\\(x = 2 + 5 = 7\\), \\(y = 3 + (-1) = 2\\)</p>"},
                {"label": "Check", "content": "<p>Moved right 5, down 1: (2, 3) → (7, 2) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>(7, 2)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: reflect in y = x, rotate, and describe",
        "steps": [
            "Reflecting in the line <strong>y = x</strong> swaps the coordinates: (x, y) → (y, x).",
            "Rotations about the origin: <strong>90° clockwise</strong> gives (x, y) → (y, −x), <strong>90° anticlockwise</strong> gives (x, y) → (−y, x), and <strong>180°</strong> gives (x, y) → (−x, −y).",
            "To describe a transformation, compare coordinates: if only y changes sign it is a reflection in the x-axis; if both change sign it is a 180° rotation."
        ],
        "example": {
            "question": "Rotate (4, 1) by 90° anticlockwise about the origin.",
            "steps": [
                {"label": "Rule", "content": "<p>Anticlockwise 90°: (x, y) → (−y, x).</p>"},
                {"label": "Apply", "content": "<p>(4, 1) → (−1, 4)</p>"},
                {"label": "Check", "content": "<p>Distance stays: \\(4^2 + 1^2 = 17 = (-1)^2 + 4^2\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>(−1, 4)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: fractional and negative scale factors",
        "steps": [
            "Enlarge about a centre in three moves: find the <strong>vector from the centre</strong> to the point, multiply it by the scale factor, then add it back to the centre.",
            "A <strong>fractional</strong> scale factor such as ⅓ makes the shape smaller. A <strong>negative</strong> scale factor puts the image on the opposite side of the centre.",
            "Combined enlargements about the same centre multiply their scale factors, so SF 3 then SF ⅓ gives SF 1: the original shape."
        ],
        "example": {
            "question": "Enlarge (5, 4) by scale factor −1, centre (2, 1).",
            "steps": [
                {"label": "Vector", "content": "<p>From (2, 1) to (5, 4): \\((3, 3)\\)</p>"},
                {"label": "Multiply", "content": "<p>\\(\\times(-1) = (-3, -3)\\)</p>"},
                {"label": "Add back", "content": "<p>\\((2 - 3, 1 - 3) = (-1, -2)\\)</p>"},
                {"label": "Answer", "content": "<p><strong>(−1, −2)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

pd["method_card"] = {
    "title": "Transformations",
    "steps": [
        "Name it: slid = translation, flipped = reflection, turned = rotation, resized = enlargement.",
        "Translation: add the column vector to every point. Reflection: mirror image across the line.",
        "Rotation about the origin: 90° clockwise is (x, y) → (y, −x); 180° is (x, y) → (−x, −y).",
        "Enlargement: multiply the vector from the centre by the scale factor; lengths × k, areas × k²."
    ],
    "content": "<p><strong>Translation</strong>: slide by a vector \\(\\binom{a}{b}\\); a right or left, b up or down.</p><p><strong>Reflection</strong>: flip in a mirror line; the image is the same distance on the other side. In y = x the coordinates swap.</p><p><strong>Rotation</strong>: turn about a centre; give the angle and direction. About the origin, 90° clockwise is (x, y) → (y, −x) and 180° is (x, y) → (−x, −y).</p><p><strong>Enlargement</strong>: multiply the vector from the centre by the scale factor; a negative factor flips to the opposite side; lengths scale by k and areas by k².</p>",
    "example": "<p><strong>Describe A to B where every point moves 3 right and 2 down.</strong></p><p>Translation by \\(\\binom{3}{-2}\\).</p>"
}

# De-em-dash worked_examples labels
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

def wc(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card.content words:", wc(pd["method_card"]["content"]))
for t in ("bronze", "silver", "gold"):
    print("tier_guides", t, "steps words:", sum(wc(x) for x in pd["tier_guides"][t]["steps"]))

def sweep(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note",): continue
            sweep(v, path + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): sweep(v, path + "[%d]" % i)
    elif isinstance(o, str) and "—" in o:
        print("EM DASH at", path, "::", o[:60])
sweep(pd)

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        d = p.get("display", "")
        if "<svg" in d:
            print("svg", tier, i, "len", len(d))
print("opener svg+text len", len(pd["guided"]["opener"]["display"]))

json.dump(pd, io.open("lesson_maths-eduqas_geometry-L04.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written")
