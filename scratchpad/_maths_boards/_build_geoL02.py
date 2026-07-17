# -*- coding: utf-8 -*-
"""Build guided-learning + diagrams practice_data for maths-aqa geometry-L02
(Area & Perimeter). Loads live row, preserves untouched fields, rebuilds the
guided stack, verifies every box and expect, emits shard + changes files."""
import json, io, math

PI = math.pi
live = json.load(io.open("_live_geoL02.json", encoding="utf-8"))

# ---- tiny SVG helpers (theme-safe: currentColor strokes/text, soft fills) ----
FONT = 'font-family="Inter,sans-serif" font-size="12" fill="currentColor"'
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def svg(vb, body, label):
    return ('<svg viewBox="%s" role="img" aria-label="%s">%s</svg>'
            % (vb, label, body))

def rect_fig(wl, hl, label, ask_area=True):
    b = ('<rect x="35" y="20" width="150" height="72" fill="#60a5fa" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<text x="110" y="110" %s text-anchor="middle">%s</text>'
         '<text x="22" y="60" %s text-anchor="middle" transform="rotate(-90 22 60)">%s</text>'
         % (FONT, wl, FONT, hl))
    return svg("0 0 210 122", b, label)

def square_fig(label):
    # tick marks show equal sides; perimeter labelled, side unknown
    b = ('<rect x="45" y="20" width="90" height="90" fill="#34d399" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<text x="90" y="128" %s text-anchor="middle">Perimeter = 28 cm</text>'
         # tick marks
         '<line x1="87" y1="17" x2="93" y2="23" stroke="currentColor"/>'
         '<line x1="87" y1="107" x2="93" y2="113" stroke="currentColor"/>'
         '<line x1="42" y1="62" x2="48" y2="68" stroke="currentColor"/>'
         '<line x1="132" y1="62" x2="138" y2="68" stroke="currentColor"/>'
         '<text x="90" y="70" %s text-anchor="middle">Area = ?</text>'
         % (FONT, FONT))
    return svg("0 0 180 138", b, label)

def triangle_fig(base_l, h_l, label, area_l=None):
    # apex offset so it reads as a triangle; right-angle mark on height
    b = ('<polygon points="30,105 190,105 95,25" fill="#f59e0b" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         # height dashed
         '<line x1="95" y1="105" x2="95" y2="25" stroke="currentColor" '
         'stroke-dasharray="4 3"/>'
         '<rect x="95" y="97" width="8" height="8" fill="none" stroke="currentColor"/>'
         '<text x="110" y="125" %s text-anchor="middle">%s</text>'
         '<text x="112" y="70" %s text-anchor="start">%s</text>'
         % (FONT, base_l, FONT, h_l))
    if area_l:
        b += '<text x="70" y="92" %s text-anchor="middle">%s</text>' % (FONT, area_l)
    return svg("0 0 210 132", b, label)

def parallelogram_fig(base_l, h_l, label):
    b = ('<polygon points="45,100 175,100 205,30 75,30" fill="#60a5fa" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<line x1="75" y1="100" x2="75" y2="30" stroke="currentColor" '
         'stroke-dasharray="4 3"/>'
         '<rect x="75" y="92" width="8" height="8" fill="none" stroke="currentColor"/>'
         '<text x="110" y="118" %s text-anchor="middle">%s</text>'
         '<text x="58" y="70" %s text-anchor="middle" transform="rotate(-90 58 70)">%s</text>'
         % (FONT, base_l, FONT, h_l))
    return svg("0 0 220 128", b, label)

def trapezium_fig(a_l, b_l, h_l, label):
    b = ('<polygon points="55,100 165,100 195,30 85,30" fill="#34d399" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<line x1="85" y1="100" x2="85" y2="30" stroke="currentColor" '
         'stroke-dasharray="4 3"/>'
         '<rect x="85" y="92" width="8" height="8" fill="none" stroke="currentColor"/>'
         '<text x="140" y="24" %s text-anchor="middle">%s</text>'   # top a
         '<text x="110" y="118" %s text-anchor="middle">%s</text>'  # bottom b
         '<text x="70" y="70" %s text-anchor="middle" transform="rotate(-90 70 70)">%s</text>'
         % (FONT, a_l, FONT, b_l, FONT, h_l))
    return svg("0 0 220 128", b, label)

def circle_fig(label, centre_note, r_from=True):
    b = ('<circle cx="80" cy="70" r="55" fill="#60a5fa" fill-opacity="0.3" '
         'stroke="currentColor" stroke-width="1.5"/>'
         '<circle cx="80" cy="70" r="2.5" fill="currentColor"/>'
         '<line x1="80" y1="70" x2="135" y2="70" stroke="currentColor"/>'
         '<text x="107" y="64" %s text-anchor="middle">%s</text>'
         % (FONT, centre_note))
    return svg("0 0 170 145", b, label)

def circle_area_label(label, note):
    b = ('<circle cx="75" cy="70" r="55" fill="#f59e0b" fill-opacity="0.3" '
         'stroke="currentColor" stroke-width="1.5"/>'
         '<text x="75" y="74" %s text-anchor="middle">%s</text>'
         % (FONT, note))
    return svg("0 0 160 145", b, label)

def semicircle_fig(label, note, note2=None):
    b = ('<path d="M 20 100 A 60 60 0 0 1 140 100 Z" fill="#60a5fa" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<text x="80" y="118" %s text-anchor="middle">%s</text>' % (FONT, note))
    if note2:
        b += '<text x="80" y="70" %s text-anchor="middle">%s</text>' % (FONT, note2)
    return svg("0 0 160 128", b, label)

def rect_hole_fig(wl, hl, label):
    b = ('<rect x="20" y="20" width="180" height="96" fill="#60a5fa" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<circle cx="110" cy="68" r="26" fill="#faf8f5" fill-opacity="0.9" '
         'stroke="currentColor" stroke-width="1.5"/>'
         '<line x1="110" y1="68" x2="136" y2="68" stroke="currentColor"/>'
         '<text x="123" y="63" %s text-anchor="middle">r 3</text>'
         '<text x="110" y="134" %s text-anchor="middle">%s</text>'
         '<text x="10" y="68" %s text-anchor="middle" transform="rotate(-90 10 68)">%s</text>'
         % (FONT, FONT, wl, FONT, hl))
    return svg("0 0 220 142", b, label)

def lshape_fig(label):
    # 6 wide x 5 tall rectangle with 2x4 corner removed (top-right)
    # scale 24 px per cm. width 6->144, height5->120. corner 2x4 -> 48x... 4cm tall=96,2cm wide=48
    b = ('<polygon points="20,20 116,20 116,116 164,116 164,140 20,140" '
         'fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<text x="92" y="156" %s text-anchor="middle">6 cm</text>'
         '<text x="10" y="80" %s text-anchor="middle" transform="rotate(-90 10 80)">5 cm</text>'
         '<text x="140" y="112" %s text-anchor="middle">2</text>'
         '<text x="126" y="72" %s text-anchor="middle">4</text>'
         % (FONT, FONT, FONT, FONT))
    return svg("0 0 190 164", b, label)

def sector_fig(r_l, ang, label, ask="area"):
    # sector from a circle centre (80,95); draw a wedge of angle `ang`
    cx, cy, R = 80, 95, 62
    a0 = -90  # start pointing up
    a1 = a0 + ang
    import math as _m
    x0 = cx + R*_m.cos(_m.radians(a0)); y0 = cy + R*_m.sin(_m.radians(a0))
    x1 = cx + R*_m.cos(_m.radians(a1)); y1 = cy + R*_m.sin(_m.radians(a1))
    large = 1 if ang > 180 else 0
    col = "#f59e0b" if ask == "area" else "#34d399"
    b = ('<path d="M %d %d L %.1f %.1f A %d %d 0 %d 1 %.1f %.1f Z" fill="%s" '
         'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
         '<text x="%d" y="%d" %s text-anchor="middle">%s</text>'
         '<text x="%d" y="%d" %s text-anchor="middle">%s</text>'
         % (cx, cy, x0, y0, R, R, large, x1, y1, col,
            cx+18, cy-14, FONT, ang_str(ang),
            cx-4, cy+30, FONT, r_l))
    return svg("0 0 170 170", b, label)

def ang_str(a):
    return "%d°" % a

def annulus_fig(label):
    b = ('<circle cx="80" cy="80" r="62" fill="#60a5fa" fill-opacity="0.3" '
         'stroke="currentColor" stroke-width="1.5"/>'
         '<circle cx="80" cy="80" r="37" fill="#faf8f5" fill-opacity="0.9" '
         'stroke="currentColor" stroke-width="1.5"/>'
         '<line x1="80" y1="80" x2="142" y2="80" stroke="currentColor"/>'
         '<line x1="80" y1="80" x2="80" y2="43" stroke="currentColor"/>'
         '<text x="112" y="74" %s text-anchor="middle">R 10</text>'
         '<text x="96" y="66" %s text-anchor="middle">r 6</text>'
         % (FONT, FONT))
    return svg("0 0 160 162", b, label)

def track_fig(label):
    b = ('<path d="M 40 30 L 170 30 A 40 40 0 0 1 170 110 L 40 110 '
         'A 40 40 0 0 1 40 30 Z" fill="#34d399" fill-opacity="0.3" '
         'stroke="currentColor" stroke-width="1.5"/>'
         '<text x="105" y="24" %s text-anchor="middle">100 m</text>'
         '<text x="105" y="128" %s text-anchor="middle">100 m</text>'
         '<text x="192" y="74" %s text-anchor="middle" transform="rotate(-90 192 74)">d 60</text>'
         % (FONT, FONT, FONT))
    return svg("0 0 215 140", b, label)

# ---------------- box + step builders ----------------
def box(pre, ans, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(text):
    return {"say": text}

def mc(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect,
            "message": message, "note": note}

# ---------------- assemble problems ----------------
def P(display_fig, question, sols, calc, hint, miscs, steps):
    disp = question if display_fig is None else (display_fig + question)
    return {"display": disp, "solutions": sols, "calculator": calc,
            "input_type": "single_value", "hint": hint,
            "misconceptions": miscs, "guided_steps": steps}

bronze = []
# B1 rectangle area 12x5 = 60
bronze.append(P(
    rect_fig("12 cm", "5 cm", "Rectangle, length 12 cm and width 5 cm"),
    "Find the area of a rectangle with length 12 cm and width 5 cm.",
    [60], False, "Area of a rectangle is length times width.",
    [mc("perimeter", 34, "That is the perimeter, 2 × (12 + 5) = 34 cm. Area is the space inside: length × width = 12 × 5 = 60 cm².", "adds sides instead of multiplying")],
    [sayonly("Area of a rectangle is length × width, so 12 × 5. Do it in two easy pieces."),
     box("First, 10 × 5 = ", 50, "Ten fives."),
     box("Now 2 × 5 = ", 10, "Two fives."),
     box("Add the pieces: 50 + 10 = ", 60, "Add them together.", phase="substitute"),
     box("Check the other way, 5 rows of 12: 5 × 12 = ", 60, "Five twelves.",
         done="Both routes give 60, so the area is 60 cm².")]))
# B2 rectangle perimeter 9x4 = 26
bronze.append(P(
    rect_fig("9 cm", "4 cm", "Rectangle, length 9 cm and width 4 cm"),
    "Find the perimeter of a rectangle with length 9 cm and width 4 cm.",
    [26], False, "Perimeter is twice the length plus twice the width.",
    [mc("area", 36, "That is the area, 9 × 4 = 36 cm². Perimeter is the distance round the edge: 2 × (9 + 4) = 26 cm.", "multiplies instead of adding round")],
    [sayonly("Perimeter is the distance all the way round: 9 + 4 + 9 + 4."),
     box("Add one length and one width: 9 + 4 = ", 13, "Just add the two."),
     box("There are two of each, so double it: 13 × 2 = ", 26, "Times two.", phase="substitute"),
     box("Check by adding all four sides: 9 + 9 + 4 + 4 = ", 26, "Add the four sides.",
         done="Same total, so the perimeter is 26 cm.")]))
# B3 triangle area base10 h6 = 30
bronze.append(P(
    triangle_fig("base 10 cm", "6 cm", "Triangle, base 10 cm and height 6 cm"),
    "Find the area of a triangle with base 10 cm and perpendicular height 6 cm.",
    [30], False, "Half of base times height.",
    [mc("no_half", 60, "You found base × height, 60. A triangle is half of its rectangle: 60 ÷ 2 = 30 cm².", "forgot to halve")],
    [sayonly("Area of a triangle = ½ × base × height."),
     box("First multiply base × height: 10 × 6 = ", 60, "Ten sixes."),
     box("Now take half: 60 ÷ 2 = ", 30, "Halve it.", phase="substitute"),
     box("Sense check: a triangle is half its surrounding 10 by 6 rectangle, and half of 60 = ", 30, "Half of 60.",
         done="The halving is the whole point, so 30 cm².")]))
# B4 parallelogram base8 h5 = 40
bronze.append(P(
    parallelogram_fig("base 8 cm", "5 cm", "Parallelogram, base 8 cm and height 5 cm"),
    "Find the area of a parallelogram with base 8 cm and perpendicular height 5 cm.",
    [40], False, "Base times height, and do not halve for a parallelogram.",
    [mc("halve", 20, "A parallelogram is not halved. Base × height = 8 × 5 = 40 cm², double the triangle you may be picturing.", "wrongly halved")],
    [sayonly("Area of a parallelogram = base × perpendicular height. No halving."),
     box("Slide the slanted end across and it becomes a rectangle 8 by 5. That area = 8 × 5 = ", 40, "Eight fives."),
     box("So the parallelogram equals that rectangle. Write the area: ", 40, "Same as the rectangle.", phase="substitute"),
     box("Careful check: it is base × height, not ½ × base × height. Half would be 20, so the true area is 20 × 2 = ", 40, "Twenty doubled.",
         done="No halving for a parallelogram, so 40 cm².")]))
# B5 trapezium 5,9,6 = 42
bronze.append(P(
    trapezium_fig("5 cm", "9 cm", "6 cm", "Trapezium, parallel sides 5 cm and 9 cm, height 6 cm"),
    "Find the area of a trapezium with parallel sides 5 cm and 9 cm, and height 6 cm.",
    [42], False, "Add the parallel sides, halve, then times the height.",
    [mc("no_half", 84, "That is (a + b) × h = 14 × 6 = 84. The trapezium formula halves it: 84 ÷ 2 = 42 cm².", "forgot the half")],
    [sayonly("Area of a trapezium = ½ × (a + b) × height. Average the parallel sides, then × height."),
     box("Add the parallel sides: 5 + 9 = ", 14, "Add them."),
     box("Average them: 14 ÷ 2 = ", 7, "Halve it."),
     box("Multiply by the height: 7 × 6 = ", 42, "Seven sixes.", phase="substitute"),
     box("Check the other order, ½ × 14 × 6: first 14 × 6 = 84, then half: 84 ÷ 2 = ", 42, "Half of 84.",
         done="Both orders give 42 cm².")]))
# B6 square perimeter28 -> area 49
bronze.append(P(
    square_fig("Square, perimeter 28 cm, area unknown"),
    "A square has perimeter 28 cm. Find its area.",
    [49], False, "Find the side first: perimeter divided by four, then square it.",
    [mc("half_perimeter", 196, "The side is perimeter ÷ 4, not ÷ 2. 28 ÷ 4 = 7, so area = 7 × 7 = 49 cm².", "divided perimeter by 2: side 14, area 196")],
    [sayonly("Find the side first, then the area. All four sides of a square are equal."),
     box("Side = perimeter ÷ 4 = 28 ÷ 4 = ", 7, "Divide by four."),
     box("Area = side × side = 7 × 7 = ", 49, "Seven sevens.", phase="substitute"),
     box("Check the perimeter of a side-7 square: 7 × 4 = ", 28, "Four sevens.",
         done="That matches the given perimeter, so area 49 cm².")]))
# B7 circumference r7 -> 44.0
bronze.append(P(
    circle_fig("Circle, radius 7 cm", "r = 7 cm"),
    "Find the circumference of a circle with radius 7 cm. Give your answer to 1 decimal place.",
    [44], True, "Circumference is 2 times pi times the radius.",
    [mc("area_confusion", 153.9, "That is the area, π × 7² ≈ 153.9. The circumference is the distance round: 2 × π × 7 ≈ 44.0 cm.", "used pi r squared")],
    [sayonly("Circumference = 2 × π × r. This is a calculator question."),
     box("Double the radius first: 2 × 7 = ", 14, "Two sevens."),
     box("Multiply by π, to 1 decimal place: 14 × π = ", 44, "Times pi, then round to 1 dp.", phase="substitute"),
     box("Cross-check: the area would be π × 49 ≈ 153.9, a different thing. The distance round is 14 × π ≈ ", 44, "14 × pi to 1 dp.",
         done="Circumference 44.0 cm, not the area.")]))
# B8 circle area r5 -> 78.5
bronze.append(P(
    circle_fig("Circle, radius 5 cm", "r = 5 cm"),
    "Find the area of a circle with radius 5 cm. Give your answer to 1 decimal place.",
    [78.5], True, "Area is pi times the radius squared.",
    [mc("circumference_confusion", 31.4, "That is the circumference, 2 × π × 5 ≈ 31.4. The area is π × r² = π × 25 ≈ 78.5 cm².", "used 2 pi r")],
    [sayonly("Area = π × r². Square the radius first."),
     box("Square the radius: 5 × 5 = ", 25, "Five fives."),
     box("Multiply by π, to 1 decimal place: 25 × π = ", 78.5, "Times pi, then round to 1 dp.", phase="substitute"),
     box("Cross-check: the circumference would be 2 × π × 5 ≈ 31.4, a length not an area. The area is π × 25 ≈ ", 78.5, "25 × pi to 1 dp.",
         done="Area 78.5 cm².")]))

silver = []
# S1 semicircle diameter12 -> 56.5
silver.append(P(
    semicircle_fig("Semicircle, diameter 12 cm", "diameter 12 cm"),
    "A semicircle has diameter 12 cm. Find its area. Give your answer to 1 decimal place.",
    [56.5], True, "Halve the diameter for the radius, find the circle area, then halve for a semicircle.",
    [mc("full_circle", 113.1, "That is the whole circle, π × 6² ≈ 113.1. A semicircle is half of it: 113.1 ÷ 2 ≈ 56.5 cm².", "did not halve for the semicircle"),
     mc("diameter_as_radius", 226.2, "You used the diameter 12 as the radius. Halve it first: radius 6, then ½ × π × 6² ≈ 56.5 cm².", "used d as r: half pi 144 = 226.2")],
    [sayonly("A semicircle is half a circle. Find the radius, then take half the circle's area."),
     box("Radius = diameter ÷ 2 = 12 ÷ 2 = ", 6, "Halve the diameter."),
     box("Square it: 6 × 6 = ", 36, "Six sixes."),
     box("Half circle area = ½ × π × 36, to 1 decimal place = ", 56.5, "Half of 36 pi, to 1 dp.", phase="substitute"),
     box("Check the radius fits: 2 × 6 = ", 12, "Double the radius.",
         done="That matches the given diameter, so 56.5 cm².")]))
# S2 rect 15x8 minus circle r3 -> 91.7
silver.append(P(
    rect_hole_fig("15 cm", "8 cm", "Rectangle 15 cm by 8 cm with a circle of radius 3 cm removed from the middle"),
    "A rectangle is 15 cm by 8 cm. A circle of radius 3 cm is cut from the middle. Find the remaining area to 1 decimal place.",
    [91.7], True, "Rectangle area minus circle area.",
    [mc("add_not_subtract", 148.3, "The circle is cut out, so subtract it: 120 − 28.3 ≈ 91.7 cm². Adding gives 148.3, bigger than the whole rectangle.", "added the circle instead of subtracting")],
    [sayonly("Find the rectangle, then subtract the circle that is cut out."),
     box("Rectangle area = 15 × 8 = ", 120, "Fifteen eights."),
     box("Square the circle's radius: 3 × 3 = ", 9, "Three threes."),
     box("Circle area = π × 9, to 2 decimal places = ", 28.27, "9 × pi to 2 dp."),
     box("Subtract, to 1 decimal place: 120 − 28.27 = ", 91.7, "Take the circle away, then round.", phase="substitute"),
     box("Sense check: the hole is small, so 120 − 91.7 = ", 28.3, "120 minus your answer.",
         done="That is the circle we removed, so 91.7 cm² remains.")]))
# S3 triangle area36 base9 -> height 8
silver.append(P(
    triangle_fig("base 9 cm", "h = ?", "Triangle, area 36 cm squared, base 9 cm, height unknown", area_l="Area 36"),
    "A triangle has area 36 cm² and base 9 cm. Find the perpendicular height.",
    [8], False, "Rearrange: height is area divided by half the base.",
    [mc("forgot_half", 4, "You divided the area by the base, 36 ÷ 9 = 4. But area = ½ × base × height, so height = 36 ÷ 4.5 = 8 cm.", "divided by base not half-base")],
    [sayonly("Work the area formula backwards. Area = ½ × base × height."),
     box("Half the base: ½ × 9 = ", 4.5, "Half of nine."),
     box("So 4.5 × height = 36, meaning height = 36 ÷ 4.5 = ", 8, "Divide 36 by 4.5.", phase="substitute"),
     box("Check forwards: ½ × 9 × 8 means 4.5 × 8 = ", 36, "4.5 times 8.",
         done="Back to the given area, so the height is 8 cm.")]))
# S4 semicircle perimeter25.7 -> radius 5
silver.append(P(
    semicircle_fig("Semicircle, perimeter 25.7 cm, radius unknown", "perimeter 25.7 cm", note2="r = ?"),
    "The perimeter of a semicircle is 25.7 cm. Find the radius to the nearest whole number.",
    [5], True, "The semicircle perimeter is the radius times pi plus 2; divide to find the radius.",
    [mc("arc_only", 8, "That uses only the curved part, π r = 25.7. The whole perimeter also has the straight diameter: π r + 2 r = 25.7, giving radius 5 cm.", "forgot the diameter: 25.7 over pi is about 8")],
    [sayonly("Perimeter of a semicircle = the curved half plus the straight diameter: π r + 2 r = r × (π + 2)."),
     box("Add the two multipliers: π + 2, to 2 decimal places = ", 5.14, "Pi plus two."),
     box("So 5.14 × r = 25.7, meaning r = 25.7 ÷ 5.14 = ", 5, "Divide 25.7 by 5.14.", phase="substitute"),
     box("Check: 5 × (π + 2) = 5 × 5.14 = ", 25.7, "Five times 5.14.",
         done="That matches the given perimeter, so the radius is 5 cm.")]))
# S5 two triangles -> parallelogram base6 h4 = 24
silver.append(P(
    parallelogram_fig("base 6 cm", "4 cm", "Parallelogram made of two triangles, base 6 cm and height 4 cm"),
    "Two congruent triangles with base 6 cm and height 4 cm are put together to form a parallelogram. Find the area of the parallelogram.",
    [24], False, "Base times height gives the parallelogram directly.",
    [mc("one_triangle", 12, "That is one triangle, ½ × 6 × 4 = 12. The parallelogram is two of them: 12 × 2 = 24 cm², or simply base × height = 24.", "gave a single triangle")],
    [sayonly("Two identical triangles slot together into a parallelogram, area base × height."),
     box("Area of one triangle: first 6 × 4 = ", 24, "Six fours."),
     box("Halve it for the triangle: 24 ÷ 2 = ", 12, "Halve it."),
     box("Two triangles make the parallelogram: 12 × 2 = ", 24, "Double it.", phase="substitute"),
     box("Or straight from base × height: 6 × 4 = ", 24, "Six fours.",
         done="Both routes give 24 cm².")]))
# S6 circular garden circumference31.4 -> area 78.5 (fixed to 1 dp)
silver.append(P(
    circle_fig("Circular garden, circumference 31.4 m", "C = 31.4 m"),
    "A circular garden has circumference 31.4 m. Find its area to 1 decimal place.",
    [78.5], True, "Find the radius from the circumference first, then use pi r squared.",
    [mc("forgot_half_radius", 314.2, "You used r = C ÷ π = 10. But C = 2 π r, so r = C ÷ (2π) = 5. Area = π × 5² ≈ 78.5 m².", "divided by pi not 2 pi: r 10, area 314.2")],
    [sayonly("Get the radius from the circumference, then find the area."),
     box("C = 2 × π × r, so first work out 2 × π, to 2 decimal places = ", 6.28, "Two pi."),
     box("Radius = 31.4 ÷ 6.28 = ", 5, "Divide the circumference by that."),
     box("Area = π × r² = π × 25, to 1 decimal place = ", 78.5, "25 × pi to 1 dp.", phase="substitute"),
     box("Check the circumference of a radius-5 circle: 2 × π × 5, to 1 dp = ", 31.4, "10 × pi to 1 dp.",
         done="That matches, so the area is 78.5 m².")]))
# S7 L-shape (2x4 cut from 6x5) = 22  [FIXED: was 2x3 -> 24, duplicate of S5]
silver.append(P(
    lshape_fig("L-shape: a 2 cm by 4 cm corner removed from a 6 cm by 5 cm rectangle"),
    "An L-shape is formed by cutting a 2 cm × 4 cm rectangle from a corner of a 6 cm × 5 cm rectangle. Find the remaining area.",
    [22], False, "Whole rectangle minus the cut-out corner.",
    [mc("forgot_subtract", 30, "That is the whole rectangle, 6 × 5 = 30. Take away the cut-out corner 2 × 4 = 8: 30 − 8 = 22 cm².", "gave the full rectangle")],
    [sayonly("The L-shape is the whole rectangle minus the cut-out corner."),
     box("Whole rectangle = 6 × 5 = ", 30, "Six fives."),
     box("Cut-out corner = 2 × 4 = ", 8, "Two fours."),
     box("Subtract: 30 − 8 = ", 22, "Take the corner away.", phase="substitute"),
     box("Check: the L-shape is smaller than the rectangle by exactly the corner, 30 − 22 = ", 8, "30 minus your answer.",
         done="That is the corner removed, so 22 cm².")]))

gold = []
# G1 sector r8 angle135 -> area 75.4
gold.append(P(
    sector_fig("r = 8 cm", 135, "Sector, radius 8 cm, angle 135 degrees", ask="area"),
    "A sector has radius 8 cm and angle 135°. Find the area to 1 decimal place.",
    [75.4], True, "Multiply the fraction angle over 360 by pi r squared.",
    [mc("whole_circle", 201.1, "That is the whole circle, π × 8² ≈ 201.1. A sector is a fraction of it: (135 ÷ 360) × 201.1 ≈ 75.4 cm².", "ignored the fraction"),
     mc("arc_not_area", 18.8, "That is the arc length, (135 ÷ 360) × 2 × π × 8 ≈ 18.8 cm. The area uses π r²: (135 ÷ 360) × π × 64 ≈ 75.4 cm².", "found arc not area")],
    [sayonly("A sector is a fraction of the whole circle: fraction = angle ÷ 360."),
     box("Square the radius: 8 × 8 = ", 64, "Eight eights."),
     box("Fraction of the circle = 135 ÷ 360 = ", 0.375, "Divide the angle by 360."),
     box("Sector area = 0.375 × π × 64, to 1 decimal place = ", 75.4, "0.375 × 64 × pi, then round.", phase="substitute"),
     box("Cross-check: the whole circle is π × 64 ≈ 201.1, and 0.375 × 201.1 = ", 75.4, "0.375 of 201.1.",
         done="Under half the circle, so 75.4 cm².")]))
# G2 sector r10 angle72 -> arc 12.6
gold.append(P(
    sector_fig("r = 10 cm", 72, "Sector, radius 10 cm, angle 72 degrees, find the arc", ask="arc"),
    "A sector has radius 10 cm and angle 72°. Find the arc length to 1 decimal place.",
    [12.6], True, "Arc is the fraction angle over 360 of the full circumference.",
    [mc("area_not_arc", 62.8, "That is the sector area, (72 ÷ 360) × π × 10² ≈ 62.8 cm². The arc length uses the circumference: (72 ÷ 360) × 2 × π × 10 ≈ 12.6 cm.", "found area not arc")],
    [sayonly("Arc length is the same fraction of the whole circumference: (angle ÷ 360) × 2 π r."),
     box("Fraction of the circle = 72 ÷ 360 = ", 0.2, "Divide the angle by 360."),
     box("Full circumference = 2 × π × 10, to 1 decimal place = ", 62.8, "20 × pi to 1 dp."),
     box("Arc = 0.2 × 62.8, to 1 decimal place = ", 12.6, "A fifth of the circumference.", phase="substitute"),
     box("Cross-check: 360 ÷ 72 = 5, so five arcs make the full circle: 12.6 × 5 = ", 63, "12.6 times 5.",
         done="About the full 62.8, so the arc is 12.6 cm.")]))
# G3 track two semicircles d60 + two straights100 -> 388
gold.append(P(
    track_fig("Running track: two semicircles of diameter 60 m joined by two 100 m straights"),
    "A running track is two semicircles (diameter 60 m) joined by two straights of 100 m. Find the total perimeter to the nearest whole number.",
    [388], True, "Two semicircles make one full circle; add the two straights.",
    [mc("radius_for_diameter", 577, "The 60 is the diameter, not the radius. Two semicircles make one circle of circumference π × 60 ≈ 188.5, plus the 200 of straights: 388 m.", "used 60 as radius: 2 pi 60 = 377, +200 = 577")],
    [sayonly("Two semicircles of diameter 60 join into one full circle. Then add the two straight sides."),
     box("Curved part = π × diameter = π × 60, to the nearest whole = ", 188, "60 × pi, then round."),
     box("Two straights = 2 × 100 = ", 200, "Two hundreds."),
     box("Total perimeter = 188 + 200 = ", 388, "Add them.", phase="substitute"),
     box("Check: take the straights off, 388 − 200 = ", 188, "388 minus 200.",
         done="That is the full circle's circumference, so 388 m.")]))
# G4 circle area154 -> radius 7
gold.append(P(
    circle_area_label("Circle, area 154 cm squared, radius unknown", "Area 154"),
    "A circle has area 154 cm². Find the radius to 1 decimal place.",
    [7], True, "Divide the area by pi, then square-root to get the radius.",
    [mc("forgot_sqrt", 49, "That is r², 154 ÷ π ≈ 49. Take the square root to get the radius: √49 = 7.0 cm.", "stopped at r squared")],
    [sayonly("Work area = π r² backwards. Divide by π, then take the square root."),
     box("Divide the area by π: 154 ÷ π, to the nearest whole = ", 49, "154 over pi, then round."),
     box("That is r². Square-root it: √49 = ", 7, "What number squared is 49?", phase="substitute"),
     box("Check forwards: π × 7² = π × 49, to the nearest whole = ", 154, "49 × pi, then round.",
         done="Back to the given area, so the radius is 7.0 cm.")]))
# G5 annulus outer10 inner6 -> 201.1
gold.append(P(
    annulus_fig("Annulus, outer radius 10 cm, inner radius 6 cm"),
    "An annulus (ring) has outer radius 10 cm and inner radius 6 cm. Find the area to 1 decimal place.",
    [201.1], True, "Subtract the two areas, pi R squared minus pi r squared.",
    [mc("subtract_radii", 50.3, "Subtract the areas, not the radii. π × (10 − 6)² = π × 16 ≈ 50.3 is wrong; π × 10² − π × 6² = 64π ≈ 201.1 cm².", "subtracted radii first: pi 16 = 50.3")],
    [sayonly("An annulus is the big circle minus the small circle. Subtract the AREAS, never the radii."),
     box("Big circle: π × 10² = π × 100, to 1 decimal place = ", 314.2, "100 × pi to 1 dp."),
     box("Small circle: π × 6² = π × 36, to 1 decimal place = ", 113.1, "36 × pi to 1 dp."),
     box("Subtract: 314.2 − 113.1 = ", 201.1, "Big minus small.", phase="substitute"),
     box("Shortcut check: π × (100 − 36) = π × 64, to 1 decimal place = ", 201.1, "64 × pi to 1 dp.",
         done="Same as subtracting the areas, so 201.1 cm².")]))

# ---------------- tier_guides ----------------
tier_guides = {
 "bronze": {
  "title": "Bronze: one shape, one formula",
  "steps": [
   "Name the shape, then pick its formula. Rectangle: length × width. Triangle: ½ × base × height. Parallelogram: base × height. Trapezium: ½(a + b) × height.",
   "Put the measurements in and work it out. <strong>Halve</strong> for a triangle; do <strong>not</strong> halve for a parallelogram.",
   "Perimeter is the distance round the edge; area is the space inside. Give area in square units, like cm²."
  ],
  "example": {
   "question": "Find the area of a triangle with base 8 cm and height 6 cm.",
   "steps": [
    {"label": "Formula", "content": "<p>Area = ½ × base × height</p>"},
    {"label": "Substitute", "content": "<p>= ½ × 8 × 6</p>"},
    {"label": "Check the halving", "content": "<p>8 × 6 = 48, and a triangle is half of its rectangle</p>"},
    {"label": "Answer", "content": "<p>48 ÷ 2 = 24 cm²</p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "silver": {
  "title": "Silver: halves, circles and missing sides",
  "steps": [
   "Semicircle: find the full circle, then halve. A semicircle's perimeter is π r + 2 r (curve plus diameter).",
   "Compound shape: work out each piece, then add or subtract. A cut-out is subtracted.",
   "Missing length: put what you know into the formula and solve backwards, for example height = area ÷ (½ × base)."
  ],
  "example": {
   "question": "A semicircle has diameter 10 cm. Find its area to 1 decimal place.",
   "steps": [
    {"label": "Radius", "content": "<p>10 ÷ 2 = 5 cm</p>"},
    {"label": "Full circle", "content": "<p>π × 5² = π × 25</p>"},
    {"label": "Halve it", "content": "<p>a semicircle is half a circle</p>"},
    {"label": "Answer", "content": "<p>½ × π × 25 = 39.3 cm²</p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "gold": {
  "title": "Gold: sectors, arcs and rings",
  "steps": [
   "A sector is a fraction of a circle: fraction = angle ÷ 360. Sector area = (angle ÷ 360) × π r².",
   "Arc length is the same fraction of the circumference: (angle ÷ 360) × 2 π r.",
   "Annulus (ring): subtract the two <strong>areas</strong>, π R² − π r², never the radii."
  ],
  "example": {
   "question": "A sector has radius 6 cm and angle 60°. Find its area to 1 decimal place.",
   "steps": [
    {"label": "Fraction", "content": "<p>60 ÷ 360 = 1/6</p>"},
    {"label": "Full circle", "content": "<p>π × 6² = π × 36</p>"},
    {"label": "Check", "content": "<p>a 60° slice is one sixth of the circle</p>"},
    {"label": "Answer", "content": "<p>(1/6) × π × 36 = 18.8 cm²</p>", "isAnswer": True, "is_answer": True}
   ]
  }
 }
}

# ---------------- guided (opener + teach) ----------------
tile_svg = svg("0 0 240 170",
  # 5 across x 3 up grid of unit squares, soft fill
  "".join(
    '<rect x="%d" y="%d" width="36" height="36" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>'
    % (20 + c*36, 20 + r*36) for r in range(3) for c in range(5)
  ) +
  '<text x="110" y="160" %s text-anchor="middle">5 tiles across</text>' % FONT +
  '<text x="12" y="74" %s text-anchor="middle" transform="rotate(-90 12 74)">3 up</text>' % FONT,
  "A floor tiled 5 squares across and 3 squares up")

guided = {
 "opener": {
  "label": "Before any formula",
  "display": tile_svg + "A kitchen floor is tiled with square tiles: 5 tiles across and 3 tiles up.",
  "steps": [
   {"say": "No formula needed, just look at the grid of tiles.",
    "pre": "How many tiles cover the whole floor? ", "post": "", "answer": 15,
    "hint": "5 in a row, and 3 rows: 5 + 5 + 5, or 5 × 3."},
   {"say": "That is <strong>area</strong>: the number of unit squares that fit inside. You just did length × width. Each tile is 1 metre square, so the area is 15 m².",
    "pre": "Now the fence. Walking right round the edge is 5 + 3 + 5 + 3 metres. That total is ", "post": "", "answer": 16,
    "hint": "Two sides of 5 and two sides of 3: 10 + 6."},
   {"say": "That distance round the outside is the <strong>perimeter</strong>, 16 m. Every shape in this lesson comes back to those two ideas: <strong>area</strong> is the space inside, <strong>perimeter</strong> is the distance round."}
  ]
 },
 "teach": {
  "bronze": {
   "display": trapezium_fig("4 cm", "10 cm", "6 cm", "Trapezium, parallel sides 4 cm and 10 cm, height 6 cm") +
              "Find the area of a trapezium with parallel sides 4 cm and 10 cm, and height 6 cm.",
   "label": "Together: your first one",
   "steps": [
    {"say": "The trapezium formula averages the two parallel sides, then multiplies by the height.",
     "pre": "Add the parallel sides: 4 + 10 = ", "post": "", "answer": 14, "hint": "Just add the two."},
    {"pre": "Average them: 14 ÷ 2 = ", "post": "", "answer": 7, "hint": "Halve it."},
    {"pre": "Multiply by the height: 7 × 6 = ", "post": "", "answer": 42,
     "done": "That is the trapezium's area, 42 cm².", "hint": "Seven sixes."},
    {"say": "Check it the other way, ½ × (a + b) × h with the multiply first:",
     "pre": "14 × 6 = ", "post": "", "answer": 84, "hint": "Fourteen sixes."},
    {"pre": "then half: 84 ÷ 2 = ", "post": "", "answer": 42,
     "done": "Same answer, so 42 cm². Averaging first or halving last, both work.", "hint": "Half of 84."}
   ]
  },
  "silver": {
   "display": semicircle_fig("Semicircle, diameter 20 cm", "diameter 20 cm") +
              "Find the area of a semicircle with diameter 20 cm, to 1 decimal place.",
   "label": "Together: the silver move",
   "steps": [
    {"say": "A semicircle is half a circle. Radius first, then the circle's area, then halve.",
     "pre": "Radius = 20 ÷ 2 = ", "post": "", "answer": 10, "hint": "Halve the diameter."},
    {"pre": "Square it: 10 × 10 = ", "post": "", "answer": 100, "hint": "Ten tens."},
    {"pre": "Full circle area = π × 100, to 1 decimal place = ", "post": "", "answer": 314.2,
     "hint": "100 × pi to 1 dp."},
    {"pre": "Semicircle is half: 314.2 ÷ 2 = ", "post": "", "answer": 157.1,
     "done": "Half a circle, so 157.1 cm².", "hint": "Halve it."},
    {"say": "Sanity check: two of these halves rebuild the whole circle.",
     "pre": "157.1 × 2 = ", "post": "", "answer": 314.2,
     "done": "Back to the full circle, so the half is right.", "hint": "Double your answer."}
   ]
  },
  "gold": {
   "display": sector_fig("r = 6 cm", 90, "Sector, radius 6 cm, angle 90 degrees", ask="area") +
              "Find the area of a sector with radius 6 cm and angle 90°, to 1 decimal place.",
   "label": "Together: the gold move",
   "steps": [
    {"say": "A sector is a fraction of the whole circle. The fraction is angle ÷ 360.",
     "pre": "Square the radius: 6 × 6 = ", "post": "", "answer": 36, "hint": "Six sixes."},
    {"pre": "Full circle area = π × 36, to 1 decimal place = ", "post": "", "answer": 113.1,
     "hint": "36 × pi to 1 dp."},
    {"pre": "Fraction of the circle = 90 ÷ 360 = ", "post": "", "answer": 0.25,
     "hint": "Ninety over 360 is a quarter."},
    {"pre": "Sector area = 0.25 × 113.1 = ", "post": "", "answer": 28.3,
     "done": "A quarter of the circle, so 28.3 cm².", "hint": "A quarter of 113.1, to 1 dp."},
    {"say": "Check: four quarter-sectors make the full circle.",
     "pre": "28.3 × 4 = ", "post": "", "answer": 113.2,
     "done": "Back to about the whole circle (113.1), so the quarter is right.", "hint": "Times four."}
   ]
  }
 }
}

# ---------------- method_card (preserve trimmed live one) ----------------
method_card = live["method_card"]

# ---------------- assemble practice_data ----------------
pd = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description": "Find the area or perimeter of one standard shape by putting numbers straight into its formula.",
   "silver_description": "Halves and circles, compound shapes, and working a formula backwards to find a missing length.",
   "gold_description": "Sectors and arcs (a fraction of a circle), composite perimeters, and rings between two circles."
 },
 "related_videos": live["related_videos"],
 "worked_examples": live["worked_examples"],
 "tier_guides": tier_guides,
 "guided": guided
}

# add "Diagram not drawn accurately" caption after svg for not-to-scale figures
NOT_TO_SCALE = {
 "bronze": [2,3,4,5],       # triangle, parallelogram, trapezium, square
 "silver": [0,2,3,4,6],     # semicircle, triangle, semicircle, parallelogram, L-shape
 "gold": [0,1,2,4]          # sectors, track, annulus
}
for tier, idxs in NOT_TO_SCALE.items():
    for i in idxs:
        p = pd["problem_bank"][tier][i]
        if "<svg" in p["display"]:
            p["display"] = p["display"].replace("</svg>", "</svg>" + CAP, 1)

json.dump(pd, io.open("lesson_maths-aqa_geometry-L02.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written lesson_maths-aqa_geometry-L02.json")
