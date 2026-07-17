# -*- coding: utf-8 -*-
import json, math, copy

live = json.load(open("_geoL02ocr_live.json", encoding="utf-8"))
pd = copy.deepcopy(live)

# ---------- SVG helpers ----------
FONT = 'font-family="Inter,sans-serif" font-size="12" fill="currentColor"'
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def T(x, y, s, anchor="middle", rot=None):
    r = f' transform="rotate({rot[0]} {rot[1]} {rot[2]})"' if rot else ""
    return f'<text x="{x}" y="{y}" {FONT} text-anchor="{anchor}"{r}>{s}</text>'

def rect_svg(wl, hl, aria):
    s = f'<svg viewBox="0 0 220 140" role="img" aria-label="{aria}">'
    s += '<rect x="20" y="20" width="180" height="96" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += T(110, 133, wl) + T(10, 68, hl, rot=(-90, 10, 68))
    return s + "</svg>"

def square_svg(sl, aria):
    s = f'<svg viewBox="0 0 150 150" role="img" aria-label="{aria}">'
    s += '<rect x="25" y="20" width="100" height="100" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += T(75, 137, sl) + T(14, 70, sl, rot=(-90, 14, 70))
    return s + "</svg>"

def triangle_svg(bl, hl, aria):
    s = f'<svg viewBox="0 0 210 132" role="img" aria-label="{aria}">'
    s += '<polygon points="30,105 190,105 95,25" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += '<line x1="95" y1="105" x2="95" y2="25" stroke="currentColor" stroke-dasharray="4 3"/>'
    s += '<rect x="95" y="97" width="8" height="8" fill="none" stroke="currentColor"/>'
    s += T(110, 125, bl) + T(112, 70, hl, anchor="start")
    return s + "</svg>"

def equilateral_svg(sl, aria):
    s = f'<svg viewBox="0 0 180 140" role="img" aria-label="{aria}">'
    s += '<polygon points="30,110 150,110 90,15" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += T(90, 128, sl) + T(48, 66, sl, anchor="middle", rot=(-58, 48, 66)) + T(132, 66, sl, anchor="middle", rot=(58, 132, 66))
    return s + "</svg>"

def parallelogram_svg(bl, hl, aria):
    s = f'<svg viewBox="0 0 220 128" role="img" aria-label="{aria}">'
    s += '<polygon points="45,100 175,100 205,30 75,30" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += '<line x1="75" y1="100" x2="75" y2="30" stroke="currentColor" stroke-dasharray="4 3"/>'
    s += '<rect x="75" y="92" width="8" height="8" fill="none" stroke="currentColor"/>'
    s += T(110, 118, bl) + T(58, 70, hl, rot=(-90, 58, 70))
    return s + "</svg>"

def trapezium_svg(top_l, bot_l, hl, aria):
    s = f'<svg viewBox="0 0 220 128" role="img" aria-label="{aria}">'
    s += '<polygon points="55,100 165,100 195,30 85,30" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += '<line x1="85" y1="100" x2="85" y2="30" stroke="currentColor" stroke-dasharray="4 3"/>'
    s += '<rect x="85" y="92" width="8" height="8" fill="none" stroke="currentColor"/>'
    s += T(140, 24, top_l) + T(110, 118, bot_l) + T(70, 70, hl, rot=(-90, 70, 70))
    return s + "</svg>"

def circle_svg(kind, label, aria):
    # kind: 'radius' | 'diameter' | 'area'
    s = f'<svg viewBox="0 0 160 150" role="img" aria-label="{aria}">'
    s += '<circle cx="80" cy="72" r="56" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    if kind == "radius":
        s += '<line x1="80" y1="72" x2="136" y2="72" stroke="currentColor"/>'
        s += '<circle cx="80" cy="72" r="2.5" fill="currentColor"/>'
        s += T(108, 66, label)
    elif kind == "diameter":
        s += '<line x1="24" y1="72" x2="136" y2="72" stroke="currentColor"/>'
        s += T(80, 66, label)
    else:  # area label in centre
        s += T(80, 76, label)
    return s + "</svg>"

def semicircle_svg(dl, aria):
    s = f'<svg viewBox="0 0 160 120" role="img" aria-label="{aria}">'
    s += '<path d="M 20 96 A 60 60 0 0 1 140 96 Z" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += T(80, 114, dl)
    return s + "</svg>"

def annulus_svg(Rl, rl, aria):
    s = f'<svg viewBox="0 0 160 162" role="img" aria-label="{aria}">'
    s += '<circle cx="80" cy="80" r="62" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += '<circle cx="80" cy="80" r="37" fill="#faf8f5" fill-opacity="0.9" stroke="currentColor" stroke-width="1.5"/>'
    s += '<line x1="80" y1="80" x2="142" y2="80" stroke="currentColor"/>'
    s += '<line x1="80" y1="80" x2="80" y2="43" stroke="currentColor"/>'
    s += T(112, 74, Rl) + T(96, 66, rl)
    return s + "</svg>"

def rect_minus_circle_svg(wl, hl, rl, aria):
    s = f'<svg viewBox="0 0 220 142" role="img" aria-label="{aria}">'
    s += '<rect x="20" y="20" width="180" height="96" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    s += '<circle cx="110" cy="68" r="26" fill="#faf8f5" fill-opacity="0.9" stroke="currentColor" stroke-width="1.5"/>'
    s += '<line x1="110" y1="68" x2="136" y2="68" stroke="currentColor"/>'
    s += T(123, 63, rl) + T(110, 134, wl) + T(10, 68, hl, rot=(-90, 10, 68))
    return s + "</svg>"

def sector_svg(deg, r_label=None, arc_label=None, angle_label=None, aria=""):
    cx, cy, R = 82, 92, 62
    a = math.radians(deg)
    ex = cx + R * math.sin(a)
    ey = cy - R * math.cos(a)
    large = 1 if deg > 180 else 0
    s = f'<svg viewBox="0 0 174 174" role="img" aria-label="{aria}">'
    s += (f'<path d="M {cx} {cy} L {cx} {cy-R} A {R} {R} 0 {large} 1 {ex:.1f} {ey:.1f} Z" '
          'fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
    # angle label near centre along bisector
    half = math.radians(deg / 2)
    lx = cx + 26 * math.sin(half)
    ly = cy - 26 * math.cos(half)
    if angle_label:
        s += T(round(lx), round(ly) + 4, angle_label)
    # radius label along the first (upward) edge
    if r_label:
        s += T(cx - 10, cy - 30, r_label, anchor="end")
    if arc_label:
        # place near the far edge midpoint outside
        mx = cx + (R + 14) * math.sin(half)
        my = cy - (R + 14) * math.cos(half)
        s += T(round(mx), round(my), arc_label)
    return s + "</svg>"

# ---------- misconception + guided assembly ----------
def M(pattern, expect, message, note=None):
    d = {"pattern": pattern, "expect": expect, "message": message}
    if note:
        d["note"] = note
    return d

def say(t): return {"say": t}
def box(pre, ans, hint, post="", done=None, phase=None, sayf=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    if sayf: d["say"] = sayf
    return d

pb = pd["problem_bank"]

# ---- tier descriptions ----
pb["bronze_description"] = "Find the area or perimeter of one standard shape by putting the measurements straight into its formula."
pb["silver_description"] = "Circles, halves and compound shapes, and working a formula backwards to find a missing radius."
pb["gold_description"] = "Sectors and arcs (a fraction of a circle), rings between two circles, and finding an angle from an area or arc."

# =================== BRONZE ===================
b = pb["bronze"]

# [0] rectangle 9x4 = 36
b[0]["display"] = rect_svg("9 cm", "4 cm", "Rectangle, 9 cm by 4 cm") + CAP + "Find the area of a rectangle 9 cm by 4 cm."
b[0]["hint"] = "Area of a rectangle is length times width."
b[0]["misconceptions"] = [M("perimeter", 26,
    "That is the perimeter, 2 × (9 + 4) = 26 cm. Area is length × width: 9 × 4 = 36 cm².", "added round instead of multiplying")]
b[0]["guided_steps"] = [
    say("Area is the number of 1 cm squares that fit inside: length × width."),
    box("Write the two measurements to multiply. Length is 9, width is ", 4, "The width given is 4 cm."),
    box("Multiply them: 9 × 4 = ", 36, "Nine fours.", done="36 squares fit inside, so the area is 36 cm².", phase="substitute"),
    box("Check by adding four rows of 9: 9 + 9 + 9 + 9 = ", 36, "Add 9 four times.", done="Same total, so the area is 36 cm²."),
]

# [1] triangle base 10 height 6 = 30
b[1]["display"] = triangle_svg("base 10 cm", "6 cm", "Triangle, base 10 cm, height 6 cm") + CAP + "Find the area of a triangle with base 10 cm and height 6 cm."
b[1]["hint"] = "Area of a triangle is half of base times height."
b[1]["misconceptions"] = [M("forgot_half", 60,
    "That is base × height, 60. A triangle is half of that: 60 ÷ 2 = 30 cm².", "did not halve")]
b[1]["guided_steps"] = [
    say("A triangle is half the rectangle around it, so area is ½ × base × height."),
    box("Multiply base by height: 10 × 6 = ", 60, "Ten sixes."),
    box("Halve it, because a triangle is half its rectangle: 60 ÷ 2 = ", 30, "Half of 60.", done="So the area is 30 cm².", phase="substitute"),
    box("Check: does the answer double back to the rectangle? 30 × 2 = ", 60, "Double 30.", done="Yes, 60 = 10 × 6, so 30 cm² is right."),
]

# [2] perimeter rectangle 8x5 = 26
b[2]["display"] = rect_svg("8 cm", "5 cm", "Rectangle, 8 cm by 5 cm") + CAP + "Find the perimeter of a rectangle 8 cm by 5 cm."
b[2]["hint"] = "Perimeter is twice the length plus twice the width."
b[2]["misconceptions"] = [M("area", 40,
    "That is the area, 8 × 5 = 40 cm². Perimeter is the distance round: 2 × (8 + 5) = 26 cm.", "multiplied instead of going round")]
b[2]["guided_steps"] = [
    say("Perimeter is the distance all the way round the edge: 8 + 5 + 8 + 5."),
    box("Add one length and one width: 8 + 5 = ", 13, "Just add the two."),
    box("There are two of each, so double it: 13 × 2 = ", 26, "Double 13.", done="So the perimeter is 26 cm.", phase="substitute"),
    box("Check all four sides: 8 + 8 + 5 + 5 = ", 26, "Add all four.", done="Same total, so 26 cm."),
]

# [3] parallelogram base 7 height 4 = 28
b[3]["display"] = parallelogram_svg("base 7 cm", "4 cm", "Parallelogram, base 7 cm, height 4 cm") + CAP + "Find the area of a parallelogram with base 7 cm and height 4 cm."
b[3]["hint"] = "Area of a parallelogram is base times perpendicular height, with no halving."
b[3]["misconceptions"] = [M("halved", 14,
    "You halved it like a triangle. A parallelogram is base × height with no halving: 7 × 4 = 28 cm².", "treated it like a triangle")]
b[3]["guided_steps"] = [
    say("A parallelogram fills the same space as a rectangle of the same base and height, so area is base × height."),
    box("Write the base to multiply: the base is ", 7, "The base is 7 cm."),
    box("Multiply base × height: 7 × 4 = ", 28, "Seven fours.", done="So the area is 28 cm².", phase="substitute"),
    box("Check: slide the slanted piece across to make a 7 by 4 rectangle, 7 × 4 = ", 28, "Seven fours again.", done="Same space, 28 cm²."),
]

# [4] trapezium 6,10 height 4 = 32
b[4]["display"] = trapezium_svg("6 cm", "10 cm", "4 cm", "Trapezium, parallel sides 6 cm and 10 cm, height 4 cm") + CAP + "Find the area of a trapezium with parallel sides 6 cm and 10 cm and height 4 cm."
b[4]["hint"] = "Average the two parallel sides, then multiply by the height."
b[4]["misconceptions"] = [M("no_average", 64,
    "You multiplied the sum of the sides by the height without averaging. Area is ½ × (6 + 10) × 4 = 32 cm².", "forgot to halve the average")]
b[4]["guided_steps"] = [
    say("Trapezium area averages the two parallel sides, then multiplies by the height."),
    box("Add the parallel sides: 6 + 10 = ", 16, "Add the two."),
    box("Average them: 16 ÷ 2 = ", 8, "Halve 16.", phase="substitute"),
    box("Multiply by the height: 8 × 4 = ", 32, "Eight fours.", done="So the area is 32 cm²."),
    box("Check the other order, 16 × 4 = 64 then halve: 64 ÷ 2 = ", 32, "Half of 64.", done="Same answer, 32 cm²."),
]

# [5] circumference circle radius 7 = 44.0
b[5]["display"] = circle_svg("radius", "r = 7 cm", "Circle, radius 7 cm") + "Find the circumference of a circle with radius 7 cm. Give your answer to 1 d.p."
b[5]["hint"] = "Circumference is pi times the diameter, and the diameter is twice the radius."
b[5]["misconceptions"] = [
    M("used_area", 153.9, "That is the area, π × 7² ≈ 153.9 cm². Circumference is π × diameter = π × 14 ≈ 44.0 cm.", "used pi r squared"),
    M("radius_as_diameter", 22.0, "You multiplied π by the radius. Circumference uses the diameter: π × 14 ≈ 44.0 cm.", "forgot to double the radius"),
]
b[5]["guided_steps"] = [
    say("Circumference is π × diameter, or 2 × π × radius."),
    box("Double the radius to get the diameter: 2 × 7 = ", 14, "Twice the radius."),
    box("Multiply by π: π × 14, to 1 d.p. = ", 44, "π × 14 ≈ 43.98.", done="So the circumference ≈ 44.0 cm.", phase="substitute"),
    box("Check with 2 × π × r: 2 × π × 7, to 1 d.p. = ", 44, "Same value.", done="Same answer, 44.0 cm."),
]

# [6] square side 9 area = 81
b[6]["display"] = square_svg("9 cm", "Square, side 9 cm") + "Find the area of a square with side 9 cm."
b[6]["hint"] = "A square's area is side times side."
b[6]["misconceptions"] = [M("perimeter", 36,
    "That is the perimeter, 4 × 9 = 36 cm. Area is side × side: 9 × 9 = 81 cm².", "found perimeter not area")]
b[6]["guided_steps"] = [
    say("A square is a rectangle with equal sides, so its area is side × side."),
    box("Both sides are the same. Write the side: ", 9, "The side is 9 cm."),
    box("Multiply side × side: 9 × 9 = ", 81, "Nine nines.", done="So the area is 81 cm².", phase="substitute"),
    box("Check: 9² means 9 × 9 = ", 81, "Nine squared.", done="Same, 81 cm²."),
]

# [7] perimeter equilateral triangle side 5 = 15
b[7]["display"] = equilateral_svg("5 cm", "Equilateral triangle, side 5 cm") + CAP + "Find the perimeter of an equilateral triangle with side 5 cm."
b[7]["hint"] = "An equilateral triangle has three equal sides, so add all three."
b[7]["misconceptions"] = [M("two_sides", 10,
    "You added only two sides. An equilateral triangle has three equal sides: 3 × 5 = 15 cm.", "missed a side")]
b[7]["guided_steps"] = [
    say("Perimeter is the distance round. An equilateral triangle has three equal sides."),
    box("How many equal sides does the triangle have? ", 3, "A triangle has 3 sides."),
    box("Each side is 5, so 3 × 5 = ", 15, "Three fives.", done="So the perimeter is 15 cm.", phase="substitute"),
    box("Check by adding them: 5 + 5 + 5 = ", 15, "Add three fives.", done="Same, 15 cm."),
]

# =================== SILVER ===================
s = pb["silver"]

# [0] area circle radius 6 = 113.1
s[0]["display"] = circle_svg("radius", "r = 6 cm", "Circle, radius 6 cm") + "Find the area of a circle with radius 6 cm. Give your answer to 1 d.p."
s[0]["hint"] = "Area of a circle is pi times the radius squared."
s[0]["misconceptions"] = [
    M("forgot_square", 18.8, "You did not square the radius. Area is π × 6² = π × 36 ≈ 113.1 cm².", "used pi times r not r squared"),
    M("used_circumference", 37.7, "That is the circumference, 2 × π × 6 ≈ 37.7 cm. Area is π × r² ≈ 113.1 cm².", "used circumference formula"),
]
s[0]["guided_steps"] = [
    say("Area of a circle is π × r². Square the radius first."),
    box("Square the radius: 6 × 6 = ", 36, "Six sixes."),
    box("Multiply by π: π × 36, to 1 d.p. = ", 113.1, "π × 36 ≈ 113.10.", done="So the area ≈ 113.1 cm².", phase="substitute"),
    box("Check the size: area ÷ r² should be about π. 113.1 ÷ 36 = ", 3.1, "Divide area by 36.", done="About 3.14 = π, so 113.1 cm² is right."),
]

# [1] circumference diameter 14 = 44.0
s[1]["display"] = circle_svg("diameter", "d = 14 cm", "Circle, diameter 14 cm") + "A circle has diameter 14 cm. Find the circumference to 1 d.p."
s[1]["hint"] = "Circumference is pi times the diameter, and the diameter is already given."
s[1]["misconceptions"] = [
    M("used_area", 153.9, "That is the area with radius 7, π × 7² ≈ 153.9 cm². Circumference is π × diameter = π × 14 ≈ 44.0 cm.", "used pi r squared"),
    M("doubled_diameter", 88.0, "You used the diameter as the radius. Circumference is π × diameter directly: π × 14 ≈ 44.0 cm.", "treated diameter as radius"),
]
s[1]["guided_steps"] = [
    say("Circumference is π × diameter, and the diameter is given here."),
    box("Write the diameter to use: ", 14, "The diameter is 14 cm."),
    box("Multiply by π: π × 14, to 1 d.p. = ", 44, "π × 14 ≈ 43.98.", done="So the circumference ≈ 44.0 cm.", phase="substitute"),
    box("Check with 2 × π × r, where r = 7: 2 × π × 7, to 1 d.p. = ", 44, "Radius is half the diameter, 7.", done="Same answer, 44.0 cm."),
]

# [2] circle area 50.3 -> radius 4
s[2]["display"] = circle_svg("area", "area 50.3", "Circle with area 50.3 cm squared") + "A circle has area 50.3 cm². Find the radius to 1 d.p."
s[2]["hint"] = "Divide the area by pi to get r squared, then take the square root."
s[2]["misconceptions"] = [
    M("forgot_root", 16, "That is r², not r. Take the square root: √16 = 4 cm.", "gave r squared not r"),
    M("divided_by_2pi", 8.0, "Divide by π, not 2π, then square root: 50.3 ÷ π = 16, √16 = 4 cm.", "used circumference formula"),
]
s[2]["guided_steps"] = [
    say("Area = π × r², so work backwards: divide by π, then square root."),
    box("Divide the area by π: 50.3 ÷ π, to the nearest whole number = ", 16, "50.3 ÷ 3.14159 ≈ 16."),
    box("That is r². Take the square root: √16 = ", 4, "What number squared is 16?", done="So the radius ≈ 4.0 cm.", phase="substitute"),
    box("Check forwards: π × 4² = π × 16, to 1 d.p. = ", 50.3, "π × 16 ≈ 50.27.", done="Back to 50.3, so r = 4.0 cm."),
]

# [3] trapezium 5,11 height 8 = 64
s[3]["display"] = trapezium_svg("5 cm", "11 cm", "8 cm", "Trapezium, parallel sides 5 cm and 11 cm, height 8 cm") + CAP + "A trapezium has parallel sides 5 cm and 11 cm and height 8 cm. Find the area."
s[3]["hint"] = "Average the two parallel sides, then multiply by the height."
s[3]["misconceptions"] = [M("no_average", 128,
    "You did not average the parallel sides. Area is ½ × (5 + 11) × 8 = 64 cm².", "forgot to halve")]
s[3]["guided_steps"] = [
    say("Trapezium area averages the two parallel sides, then multiplies by the height."),
    box("Add the parallel sides: 5 + 11 = ", 16, "Add the two."),
    box("Average them: 16 ÷ 2 = ", 8, "Halve 16.", phase="substitute"),
    box("Multiply by the height: 8 × 8 = ", 64, "Eight eights.", done="So the area is 64 cm²."),
    box("Check the other order, 16 × 8 = 128 then halve: 128 ÷ 2 = ", 64, "Half of 128.", done="Same answer, 64 cm²."),
]

# [4] sector r6 angle 90 area = 28.3
s[4]["display"] = sector_svg(90, r_label="r = 6 cm", angle_label="90°", aria="Sector, radius 6 cm, angle 90 degrees") + CAP + "A sector has radius 6 cm and angle 90°. Find the area. Give your answer to 1 d.p."
s[4]["hint"] = "A sector is a fraction of the circle: fraction is the angle over 360."
s[4]["misconceptions"] = [M("forgot_fraction", 113.1,
    "That is the whole circle. A 90° sector is 90 ÷ 360 = ¼ of it: 0.25 × 113.1 ≈ 28.3 cm².", "used the full circle")]
s[4]["guided_steps"] = [
    say("A sector is a fraction of the whole circle. The fraction is angle ÷ 360."),
    box("Square the radius: 6 × 6 = ", 36, "Six sixes."),
    box("Full circle area = π × 36, to 1 d.p. = ", 113.1, "π × 36 ≈ 113.10."),
    box("Fraction of the circle: 90 ÷ 360 = ", 0.25, "Ninety over 360.", phase="substitute"),
    box("Sector area = 0.25 × 113.1 = ", 28.3, "A quarter of 113.1.", done="So the area ≈ 28.3 cm²."),
    box("Check: four quarter-sectors rebuild the circle, 28.3 × 4 = ", 113.2, "Times 4.", done="About 113.1, the whole circle, so correct."),
]

# [5] arc r10 angle 72 = 12.6
s[5]["display"] = sector_svg(72, r_label="r = 10 cm", angle_label="72°", aria="Sector, radius 10 cm, angle 72 degrees") + CAP + "Find the arc length of a sector with radius 10 cm and angle 72°. Give your answer to 1 d.p."
s[5]["hint"] = "Arc length is a fraction of the circumference: fraction is the angle over 360."
s[5]["misconceptions"] = [M("forgot_fraction", 62.8,
    "That is the full circumference. The arc is 72 ÷ 360 = 0.2 of it: 0.2 × 62.8 ≈ 12.6 cm.", "used the full circumference")]
s[5]["guided_steps"] = [
    say("Arc length is a fraction of the circumference. The fraction is angle ÷ 360."),
    box("Circumference = 2 × π × 10, to 1 d.p. = ", 62.8, "2 × π × 10 ≈ 62.83."),
    box("Fraction of the circle: 72 ÷ 360 = ", 0.2, "72 over 360 = 0.2.", phase="substitute"),
    box("Arc length = 0.2 × 62.8 = ", 12.6, "A fifth of 62.8.", done="So the arc length ≈ 12.6 cm."),
    box("Check: five of these arcs make the whole circle, 12.6 × 5 = ", 63, "Times 5.", done="About 62.8, the circumference, so correct."),
]

# [6] rect 12x8 minus circle r3 = 67.7
s[6]["display"] = rect_minus_circle_svg("12 cm", "8 cm", "r 3", "Rectangle 12 cm by 8 cm with a circle of radius 3 cm removed") + "A rectangle 12 cm by 8 cm has a circle of radius 3 cm cut out. Find the remaining area to 1 d.p."
s[6]["hint"] = "Find the rectangle's area, then subtract the circle's area."
s[6]["misconceptions"] = [M("added", 124.3,
    "You added the circle instead of subtracting the cut-out: 96 − 28.3 ≈ 67.7 cm².", "added instead of subtracting")]
s[6]["guided_steps"] = [
    say("Find the rectangle's area, then subtract the circle that is cut out."),
    box("Rectangle area: 12 × 8 = ", 96, "Twelve eights."),
    box("Circle area: π × 3², to 1 d.p. = ", 28.3, "π × 9 ≈ 28.27."),
    box("Subtract the cut-out: 96 − 28.3 = ", 67.7, "Take the circle from the rectangle.", done="So the remaining area ≈ 67.7 cm².", phase="substitute"),
    box("Check by adding the circle back: 67.7 + 28.3 = ", 96, "Add the circle back.", done="Back to the rectangle, 96 cm², so correct."),
]

# =================== GOLD ===================
g = pb["gold"]

# [0] semicircle diameter 12 area = 56.5
g[0]["display"] = semicircle_svg("diameter 12 cm", "Semicircle, diameter 12 cm") + CAP + "A semicircle has diameter 12 cm. Find the area to 1 d.p."
g[0]["hint"] = "Find the radius, then the full circle's area, then halve it."
g[0]["misconceptions"] = [
    M("forgot_half", 113.1, "That is the full circle. A semicircle is half: ½ × π × 36 ≈ 56.5 cm².", "did not halve"),
    M("diameter_as_radius", 226.2, "You used the diameter as the radius. Radius = 12 ÷ 2 = 6, area = ½ × π × 6² ≈ 56.5 cm².", "used diameter as radius"),
]
g[0]["guided_steps"] = [
    say("A semicircle is half a circle. Find the radius, then halve the full circle's area."),
    box("Radius = 12 ÷ 2 = ", 6, "Half the diameter."),
    box("Half a circle is ½ × π × r². Work out ½ × π × 6², to 1 d.p. = ", 56.5, "½ × π × 36 ≈ 56.55.", done="So the area ≈ 56.5 cm².", phase="substitute"),
    box("Check: two semicircles make the full circle, 56.5 × 2 = ", 113, "Double it.", done="About 113.1, the whole circle, so correct."),
]

# [1] sector r8 angle 135 arc = 18.8
g[1]["display"] = sector_svg(135, r_label="r = 8 cm", angle_label="135°", aria="Sector, radius 8 cm, angle 135 degrees") + CAP + "A sector has radius 8 cm and angle 135°. Find the arc length to 1 d.p."
g[1]["hint"] = "Arc length is a fraction of the circumference: fraction is the angle over 360."
g[1]["misconceptions"] = [
    M("used_area", 75.4, "That is the sector area (using r²). Arc length uses the circumference: 0.375 × 2 × π × 8 ≈ 18.8 cm.", "found area not arc"),
    M("forgot_fraction", 50.3, "That is the full circumference. The arc is 135 ÷ 360 = 0.375 of it: 0.375 × 50.3 ≈ 18.8 cm.", "used full circumference"),
]
g[1]["guided_steps"] = [
    say("Arc length is a fraction of the circumference. The fraction is angle ÷ 360."),
    box("Fraction of the circle: 135 ÷ 360 = ", 0.375, "135 over 360."),
    box("Circumference ≈ 50.265. Arc = 0.375 × 50.265, to 1 d.p. = ", 18.8, "0.375 of 50.265.", done="So the arc length ≈ 18.8 cm.", phase="substitute"),
    box("Check by scaling back up: 18.8 ÷ 0.375 = ", 50.1, "Divide by 0.375.", done="About 50.3, the circumference, so correct."),
]

# [2] sector r5 arc 10 -> angle 115
g[2]["display"] = sector_svg(115, r_label="r = 5 cm", arc_label="arc 10 cm", angle_label="?", aria="Sector, radius 5 cm, arc length 10 cm, angle unknown") + CAP + "A sector has radius 5 cm and arc length 10 cm. Find the angle in degrees. Round to the nearest degree."
g[2]["hint"] = "The arc is a fraction of the circumference; turn that fraction into an angle out of 360."
g[2]["misconceptions"] = [M("half_circle", 57,
    "A full circle is 360°, not 180°. Angle = (10 ÷ 31.42) × 360 ≈ 115°.", "used 180 instead of 360")]
g[2]["guided_steps"] = [
    say("Arc = fraction × circumference, so find the fraction, then turn it into an angle out of 360°."),
    box("Circumference = 2 × π × 5, to 1 d.p. = ", 31.4, "2 × π × 5 ≈ 31.42."),
    box("Fraction of the circle = arc ÷ circumference = 10 ÷ 31.416, to 4 d.p. = ", 0.3183, "Ten over 31.416.", phase="substitute"),
    box("Angle = 0.3183 × 360, to the nearest degree = ", 115, "0.3183 × 360 ≈ 114.6, rounds to 115.", done="So the angle is 115°."),
    box("Check forwards: arc = 0.3183 × 31.416 = ", 10, "Fraction × circumference.", done="Back to the arc of 10 cm, so 115° is right."),
]

# [3] ring r3 inside r5 = 50.3
g[3]["display"] = annulus_svg("R 5", "r 3", "Ring between an outer circle radius 5 cm and inner circle radius 3 cm") + CAP + "Two circles share the same centre: radius 3 cm inside radius 5 cm. Find the area of the ring to 1 d.p."
g[3]["hint"] = "Subtract the two areas: pi times the outer radius squared minus pi times the inner radius squared."
g[3]["misconceptions"] = [
    M("subtracted_radii", 12.6, "Do not subtract the radii first. Subtract the areas: π × 5² − π × 3² = π × 16 ≈ 50.3 cm².", "squared the difference of radii"),
    M("added", 106.8, "You added the two circles. A ring subtracts the inner from the outer: π × (25 − 9) ≈ 50.3 cm².", "added the areas"),
]
g[3]["guided_steps"] = [
    say("A ring (annulus) is the outer circle's area minus the inner circle's area."),
    box("Square the outer radius: 5 × 5 = ", 25, "Five fives."),
    box("Square the inner radius: 3 × 3 = ", 9, "Three threes."),
    box("Subtract the squares: 25 − 9 = ", 16, "Twenty-five take nine.", phase="substitute"),
    box("Multiply by π: π × 16, to 1 d.p. = ", 50.3, "π × 16 ≈ 50.27.", done="So the ring area ≈ 50.3 cm²."),
    box("Check: ring plus inner circle equals the outer circle. π × 16 + π × 9 = π × 25, to 1 d.p. = ", 78.5, "π × 25 ≈ 78.54.", done="The outer circle, so the ring is right."),
]

# [4] sector area 75 r10 -> angle 86
g[4]["display"] = sector_svg(86, r_label="r = 10 cm", angle_label="?", aria="Sector, radius 10 cm, area 75 cm squared, angle unknown") + CAP + "A sector has area 75 cm² and radius 10 cm. Find the angle to the nearest degree."
g[4]["hint"] = "The sector area is a fraction of the full circle's area; turn that fraction into an angle out of 360."
g[4]["misconceptions"] = [M("half_circle", 43,
    "A full circle is 360°, not 180°: 0.2387 × 360 ≈ 86°.", "used 180 instead of 360")]
g[4]["guided_steps"] = [
    say("Sector area = fraction × full circle, so find the fraction, then turn it into an angle out of 360°."),
    box("Full circle area = π × 10², to 1 d.p. = ", 314.2, "π × 100 ≈ 314.16."),
    box("Fraction = sector area ÷ full circle = 75 ÷ 314.16, to 4 d.p. = ", 0.2387, "Seventy-five over 314.16.", phase="substitute"),
    box("Angle = 0.2387 × 360, to the nearest degree = ", 86, "0.2387 × 360 ≈ 85.9.", done="So the angle is 86°."),
    box("Check forwards: sector area = 0.2387 × 314.16 = ", 75, "Fraction × full circle.", done="Back to 75 cm², so 86° is right."),
]

# =================== tier_guides ===================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one shape, one formula",
        "steps": [
            "Name the shape, then pick its formula. Rectangle: length × width. Triangle: ½ × base × height. Parallelogram: base × height. Trapezium: ½(a + b) × height.",
            "Put the numbers in and work it out. <strong>Halve</strong> for a triangle; do <strong>not</strong> halve for a parallelogram.",
            "Perimeter is the distance round the edge; area is the space inside. Give area in square units, like cm².",
        ],
        "example": {
            "question": "Find the area of a triangle with base 8 cm and height 5 cm.",
            "steps": [
                {"label": "Formula", "content": "<p>Area = ½ × base × height</p>"},
                {"label": "Substitute", "content": "<p>= ½ × 8 × 5</p>"},
                {"label": "Check the halving", "content": "<p>8 × 5 = 40, and a triangle is half its rectangle</p>"},
                {"label": "Answer", "content": "<p>40 ÷ 2 = 20 cm²</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: circles, halves and missing sides",
        "steps": [
            "Circle area is π × r²; circumference is π × d. Square the radius before multiplying by π for area.",
            "Compound shape: work out each piece, then add or subtract. A cut-out is subtracted.",
            "Missing radius: work backwards, r² = area ÷ π, then take the square root.",
        ],
        "example": {
            "question": "Find the area of a circle with radius 5 cm, to 1 decimal place.",
            "steps": [
                {"label": "Square the radius", "content": "<p>5 × 5 = 25</p>"},
                {"label": "Multiply by π", "content": "<p>π × 25</p>"},
                {"label": "Check", "content": "<p>a bit more than 3 × 25 = 75</p>"},
                {"label": "Answer", "content": "<p>π × 25 ≈ 78.5 cm²</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: sectors, arcs and rings",
        "steps": [
            "A sector is a fraction of a circle: fraction = angle ÷ 360. Sector area = fraction × π r²; arc length = fraction × 2 π r.",
            "Working back from an area or arc: fraction = part ÷ whole, then angle = fraction × 360.",
            "Ring (annulus): subtract the two <strong>areas</strong>, π R² − π r², never the radii.",
        ],
        "example": {
            "question": "A sector has radius 6 cm and angle 60°. Find its area, to 1 decimal place.",
            "steps": [
                {"label": "Fraction", "content": "<p>60 ÷ 360 = one sixth</p>"},
                {"label": "Full circle", "content": "<p>π × 6² = π × 36 ≈ 113.1</p>"},
                {"label": "Check", "content": "<p>a 60° slice is one sixth of the circle</p>"},
                {"label": "Answer", "content": "<p>113.1 ÷ 6 ≈ 18.8 cm²</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =================== guided (opener + teach) ===================
def grid_svg(across, up, cell=26, x0=20, y0=18):
    parts = [f'<svg viewBox="0 0 {x0*2+across*cell} {y0+up*cell+34}" role="img" aria-label="A patio paved {across} slabs across and {up} slabs up">']
    for r in range(up):
        for c in range(across):
            x = x0 + c * cell
            y = y0 + r * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>')
    midx = x0 + across * cell / 2
    parts.append(T(round(midx), y0 + up * cell + 22, f"{across} slabs across"))
    parts.append(T(x0 - 8, round(y0 + up * cell / 2), f"{up} up", rot=(-90, x0 - 8, round(y0 + up * cell / 2))))
    parts.append("</svg>")
    return "".join(parts)

pd["guided"] = {
    "opener": {
        "label": "Before any formula",
        "display": grid_svg(6, 4) + "A patio is paved with square slabs: 6 slabs across and 4 slabs up. Each slab is 1 metre square.",
        "steps": [
            {"say": "No formula needed, just read the grid of slabs.",
             "pre": "How many slabs cover the whole patio? ", "post": "", "answer": 24,
             "hint": "6 in a row, and 4 rows: 6 × 4."},
            {"say": "That is <strong>area</strong>: the number of unit squares that fit inside. You just did length × width, so the area is 24 m².",
             "pre": "Now a fence round the edge. Walking right round is 6 + 4 + 6 + 4 metres. That total is ", "post": "", "answer": 20,
             "hint": "Two sides of 6 and two sides of 4: 12 + 8."},
            {"say": "That distance round the outside is the <strong>perimeter</strong>, 20 m. Every shape in this lesson comes back to those two ideas: <strong>area</strong> is the space inside, <strong>perimeter</strong> is the distance round."},
        ],
    },
    "teach": {
        "bronze": {
            "display": triangle_svg("base 8 cm", "5 cm", "Triangle, base 8 cm, height 5 cm") + CAP + "Find the area of a triangle with base 8 cm and height 5 cm.",
            "label": "Together: your first one",
            "steps": [
                {"say": "A triangle is exactly half the rectangle drawn around it. Start with that rectangle.",
                 "pre": "Rectangle around it: 8 × 5 = ", "post": "", "answer": 40, "hint": "Eight fives."},
                {"pre": "A triangle is half that rectangle: 40 ÷ 2 = ", "post": "", "answer": 20,
                 "done": "So the triangle's area is 20 cm².", "hint": "Half of 40."},
                {"say": "Now the formula way, ½ × base × height, to show it matches.",
                 "pre": "Half the base first: ½ × 8 = ", "post": "", "answer": 4, "hint": "Half of 8."},
                {"pre": "Then multiply by the height: 4 × 5 = ", "post": "", "answer": 20,
                 "done": "Same answer, 20 cm². Both routes agree.", "hint": "Four fives."},
            ],
        },
        "silver": {
            "display": semicircle_svg("diameter 16 cm", "Semicircle, diameter 16 cm") + CAP + "Find the area of a semicircle with diameter 16 cm, to 1 decimal place.",
            "label": "Together: your first one",
            "steps": [
                {"say": "A semicircle is half a circle. Radius first, then the full circle, then halve.",
                 "pre": "Radius = 16 ÷ 2 = ", "post": "", "answer": 8, "hint": "Half the diameter."},
                {"pre": "Square it: 8 × 8 = ", "post": "", "answer": 64, "hint": "Eight eights."},
                {"pre": "Half a circle is ½ × π × 64, to 1 decimal place = ", "post": "", "answer": 100.5,
                 "done": "So the semicircle's area ≈ 100.5 cm².", "hint": "½ × π × 64 ≈ 100.53."},
                {"say": "Sanity check: two of these halves rebuild the whole circle.",
                 "pre": "100.5 × 2 = ", "post": "", "answer": 201,
                 "done": "About 201.1 = π × 64, the full circle, so the half is right.", "hint": "Double it."},
            ],
        },
        "gold": {
            "display": sector_svg(60, r_label="r = 6 cm", angle_label="60°", aria="Sector, radius 6 cm, angle 60 degrees") + CAP + "Find the area of a sector with radius 6 cm and angle 60°, to 1 decimal place.",
            "label": "Together: your first one",
            "steps": [
                {"say": "A sector is a fraction of the whole circle. 60° out of 360° is one sixth.",
                 "pre": "Square the radius: 6 × 6 = ", "post": "", "answer": 36, "hint": "Six sixes."},
                {"pre": "Full circle area = π × 36, to 1 decimal place = ", "post": "", "answer": 113.1, "hint": "π × 36 ≈ 113.10."},
                {"pre": "A 60° slice is one sixth, so 113.097 ÷ 6, to 1 decimal place = ", "post": "", "answer": 18.8,
                 "done": "So the sector area ≈ 18.8 cm².", "hint": "One sixth of the circle."},
                {"say": "Check: six of these sectors rebuild the whole circle.",
                 "pre": "18.8 × 6 = ", "post": "", "answer": 112.8,
                 "done": "About 113.1, the whole circle, so the sixth is right.", "hint": "Times 6."},
            ],
        },
    },
}

# =================== method_card (trim to 4 steps) ===================
pd["method_card"]["steps"] = [
    "Identify the shape and choose the correct formula",
    "Substitute the measurements and work it out",
    "Composite shapes: split into simpler shapes, then add or subtract",
    "Units: area in cm², perimeter in cm",
]

# =================== worked_examples: fix em dashes ===================
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ": ")

out = "lesson_maths-ocr_geometry-L02.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", out)
