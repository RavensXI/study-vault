# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for maths-eduqas geometry-L02
(Area & Perimeter). Converts the all-multiple-choice bank to single_value numeric with
guided_steps, honest-diagnosis expects, tier_guides, opener, teach walks, and SVG figures.
Fixes two flat-wrong stored answers (S5 76.9->77.0, G3 489->388) and a duplicate (B5 35->42)."""
import json, io, math

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'
FONT = 'font-family="Inter,sans-serif"'

def svg_open(w, h, aria):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:%dpx">'
            % (w, h, aria, min(w, 280)))

def txt(x, y, s, size=11, anchor="start"):
    return '<text x="%s" y="%s" %s font-size="%d" fill="currentColor" text-anchor="%s">%s</text>' % (x, y, FONT, size, anchor, s)

def rect_fig(wlab, hlab, aria, wpx=120, hpx=80):
    x0, y0 = 45, 18
    s = svg_open(x0*2+wpx+20, y0+hpx+34, aria)
    s += '<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>' % (x0, y0, wpx, hpx)
    s += txt(x0+wpx/2, y0-5, wlab, 11, "middle")
    s += txt(x0-8, y0+hpx/2+4, hlab, 11, "end")
    s += '</svg>'
    return s

def triangle_fig(blab, hlab, aria, bpx=130, hpx=78):
    x0, y0 = 30, 18
    apex_x = x0 + bpx*0.42
    baseY = y0 + hpx
    s = svg_open(x0+bpx+30, baseY+34, aria)
    s += '<polygon points="%d,%d %d,%d %.1f,%d" fill="#34d399" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>' % (x0, baseY, x0+bpx, baseY, apex_x, y0)
    s += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>' % (apex_x, y0, apex_x, baseY)
    s += '<rect x="%.1f" y="%d" width="8" height="8" fill="none" stroke="currentColor" stroke-width="1"/>' % (apex_x, baseY-8)
    s += txt((x0*2+bpx)/2, baseY+18, blab, 11, "middle")
    s += txt(apex_x+6, y0+hpx/2, hlab, 11, "start")
    s += '</svg>'
    return s

def para_fig(blab, hlab, aria, bpx=120, hpx=64, skew=28):
    x0, y0 = 30, 18
    baseY = y0 + hpx
    s = svg_open(x0+bpx+skew+30, baseY+34, aria)
    s += '<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="#f59e0b" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>' % (x0+skew, y0, x0+skew+bpx, y0, x0+bpx, baseY, x0, baseY)
    hx = x0 + skew
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>' % (hx, y0, hx, baseY)
    s += '<rect x="%d" y="%d" width="8" height="8" fill="none" stroke="currentColor" stroke-width="1"/>' % (hx, baseY-8)
    s += txt(x0+skew+bpx/2, baseY+18, blab, 11, "middle")
    s += txt(hx-6, y0+hpx/2, hlab, 11, "end")
    s += '</svg>'
    return s

def square_fig(sidelab, aria, spx=80):
    x0, y0 = 45, 16
    s = svg_open(x0*2+spx, y0+spx+32, aria)
    s += '<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>' % (x0, y0, spx, spx)
    s += txt(x0+spx/2, y0+spx+18, sidelab, 11, "middle")
    s += '</svg>'
    return s

def circle_fig(centerlab, aria, kind="r", r=52):
    cx, cy = 90, 62
    s = svg_open(180, 138, aria)
    s += '<circle cx="%d" cy="%d" r="%d" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>' % (cx, cy, r)
    s += '<circle cx="%d" cy="%d" r="2.5" fill="currentColor"/>' % (cx, cy)
    if kind == "r":
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (cx, cy, cx+r, cy)
        s += txt(cx+r/2, cy-5, centerlab, 11, "middle")
    else:
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (cx-r, cy, cx+r, cy)
        s += txt(cx, cy-6, centerlab, 11, "middle")
    s += '</svg>'
    return s

def sector_fig(rlab, angle, aria, r=64):
    cx, cy = 60, 92
    a = math.radians(angle)
    x2 = cx + r*math.cos(a)
    y2 = cy - r*math.sin(a)
    large = 1 if angle > 180 else 0
    s = svg_open(180, 150, aria)
    s += '<path d="M %d %d L %d %d A %d %d 0 %d 0 %.2f %.2f Z" fill="#f59e0b" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>' % (cx, cy, cx+r, cy, r, r, large, x2, y2)
    ar = 20
    ax = cx + ar; ay = cy
    bx = cx + ar*math.cos(a); by = cy - ar*math.sin(a)
    s += '<path d="M %.1f %.1f A %d %d 0 0 0 %.1f %.1f" fill="none" stroke="currentColor" stroke-width="1"/>' % (ax, ay, ar, ar, bx, by)
    s += txt(cx+r*0.5, cy-6, rlab, 11, "middle")
    s += txt(cx+26, cy-12, str(angle)+"°", 10, "start")
    s += '</svg>'
    return s

def semicircle_fig(dlab, aria, r=64, show="d"):
    cx, cy = 80, 88
    s = svg_open(180, 122, aria)
    s += '<path d="M %d %d A %d %d 0 0 1 %d %d Z" fill="#34d399" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>' % (cx-r, cy, r, r, cx+r, cy)
    if show == "d":
        s += txt(cx, cy+16, dlab, 11, "middle")
    else:
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2"/>' % (cx, cy, cx+r, cy)
        s += txt(cx+r/2, cy-5, dlab, 11, "middle")
    s += '</svg>'
    return s

def annulus_fig(Rlab, rlab, aria, R=60, ri=36):
    cx, cy = 74, 74
    s = svg_open(180, 156, aria)
    s += '<circle cx="%d" cy="%d" r="%d" fill="#60a5fa" fill-opacity="0.22" stroke="currentColor" stroke-width="1.5"/>' % (cx, cy, R)
    s += '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="currentColor" stroke-width="1.5"/>' % (cx, cy, ri)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.1"/>' % (cx, cy, cx+R, cy)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.1" stroke-dasharray="3 2"/>' % (cx, cy, cx, cy-ri)
    s += '<circle cx="%d" cy="%d" r="2" fill="currentColor"/>' % (cx, cy)
    s += txt(cx+R*0.55, cy-5, Rlab, 11, "middle")
    s += txt(cx+4, cy-ri/2, rlab, 10, "start")
    s += '</svg>'
    return s

def track_fig(aria):
    x0, y0 = 40, 30
    L = 150; H = 70; r = H/2
    s = svg_open(x0*2+L+H, y0+H+34, aria)
    left = x0; right = x0+L; top = y0; bot = y0+H
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.8"/>' % (left, top, right, top)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.8"/>' % (left, bot, right, bot)
    s += '<path d="M %d %d A %.1f %.1f 0 0 1 %d %d" fill="none" stroke="currentColor" stroke-width="1.8"/>' % (right, top, r, r, right, bot)
    s += '<path d="M %d %d A %.1f %.1f 0 0 1 %d %d" fill="none" stroke="currentColor" stroke-width="1.8"/>' % (left, bot, r, r, left, top)
    s += txt((left+right)/2, top-6, "100 m", 11, "middle")
    s += txt(right+r+6, (top+bot)/2+4, "d = 60 m", 10, "start")
    s += '</svg>'
    return s

def compound_fig(aria):
    x0, y0 = 40, 20
    wpx = 140; hpx = 84; rpx = 84
    s = svg_open(x0+wpx+30, y0+hpx+34, aria)
    cxr = x0+wpx; cyr = y0
    s += ('<path d="M %d %d L %d %d L %d %d L %d %d A %d %d 0 0 1 %d %d Z" '
          'fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
          % (x0, y0, x0, y0+hpx, x0+wpx, y0+hpx, cxr, cyr+rpx, rpx, rpx, cxr-rpx, cyr))
    s += txt(x0+wpx/2, y0+hpx+18, "10 cm", 11, "middle")
    s += txt(x0-8, y0+hpx/2+4, "6 cm", 11, "end")
    s += txt(cxr-rpx*0.5, cyr+rpx*0.5, "r = 6", 10, "middle")
    s += '</svg>'
    return s

def compound_add_fig(aria):
    # rectangle 10x4 with semicircle diameter 4 added on the right end
    x0, y0 = 30, 30
    wpx = 130; hpx = 52; r = hpx/2
    s = svg_open(x0+wpx+r+30, y0+hpx+34, aria)
    top = y0; bot = y0+hpx; right = x0+wpx
    s += ('<path d="M %d %d L %d %d L %d %d A %.1f %.1f 0 0 1 %d %d L %d %d Z" '
          'fill="#34d399" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
          % (x0, top, right, top, right, top, r, r, right, bot, x0, bot))
    s += txt(x0+wpx/2, bot+18, "10 cm", 11, "middle")
    s += txt(x0-8, y0+hpx/2+4, "4 cm", 11, "end")
    s += '</svg>'
    return s

def trapezium_fig(alab, blab, hlab, aria):
    x0, y0 = 26, 18
    topw = 80; botw = 150; hpx = 66
    left_off = (botw-topw)/2
    tl = x0+left_off; tr = x0+left_off+topw; bl = x0; br = x0+botw
    s = svg_open(x0+botw+30, y0+hpx+34, aria)
    s += '<polygon points="%.1f,%d %.1f,%d %d,%d %d,%d" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>' % (tl, y0, tr, y0, br, y0+hpx, bl, y0+hpx)
    s += txt((tl+tr)/2, y0-5, alab, 11, "middle")
    s += txt((bl+br)/2, y0+hpx+18, blab, 11, "middle")
    s += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>' % (tl, y0, tl, y0+hpx)
    s += '<rect x="%.1f" y="%d" width="8" height="8" fill="none" stroke="currentColor" stroke-width="1"/>' % (tl, y0+hpx-8)
    s += txt(tl-6, y0+hpx/2, hlab, 10, "end")
    s += '</svg>'
    return s

def grid_fig(cols, rows, aria, cell=22):
    x0, y0 = 20, 12
    s = svg_open(x0*2+cols*cell, y0*2+rows*cell, aria)
    for c in range(cols):
        for rr in range(rows):
            s += '<rect x="%d" y="%d" width="%d" height="%d" fill="#f59e0b" fill-opacity="0.16" stroke="currentColor" stroke-width="1"/>' % (x0+c*cell, y0+rr*cell, cell, cell)
    s += '</svg>'
    return s

# ---------- assemble ----------
pd = json.load(io.open("_live_geoL02.json", encoding="utf-8"))

def prob(display_txt, sol, calc, hint, miscs, steps, svg=None):
    d = (svg + display_txt + CAP) if svg else display_txt
    return {"display": d, "solutions": [sol], "calculator": calc,
            "input_type": "single_value", "hint": hint,
            "misconceptions": miscs, "guided_steps": steps}

def mc(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message, "note": note}

def sb(pre, ans, hint, phase=None, say=None, post="", done=None):
    st = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if phase: st["phase"] = phase
    if say: st["say"] = say
    if done: st["done"] = done
    return st

def ss(say):
    return {"say": say}

bronze = [
 prob("Area of a rectangle 7 cm by 5 cm.", 35, False,
   "Multiply the two side lengths.",
   [mc("perimeter", 24, "That is the perimeter. Area = length × width = 7 × 5 = 35 cm².", "2(7+5)=24"),
    mc("added", 12, "Multiply, do not add: 7 × 5 = 35 cm².", "7+5=12")],
   [ss("Area of a rectangle = length × width."),
    sb("Read off the width: ", 5, "The shorter side."),
    sb("Area = 7 × 5 = ", 35, "Seven fives.", "substitute", "Now multiply length by width."),
    sb("Check: 35 ÷ 5 = ", 7, "Divide the area by the width.", "substitute", done="That gives the length 7 cm back, so 35 cm² is right.")],
   rect_fig("7 cm", "5 cm", "Rectangle 7 cm wide and 5 cm tall")),
 prob("Perimeter of a rectangle 9 cm by 4 cm.", 26, False,
   "Add length and width, then double.",
   [mc("area", 36, "That is the area. Perimeter = 2(9 + 4) = 26 cm.", "9x4=36"),
    mc("forgot_double", 13, "Add length + width then double: 2(9 + 4) = 26.", "9+4=13")],
   [ss("Perimeter = the distance all the way round = 2 × (length + width)."),
    sb("Add the two different sides: 9 + 4 = ", 13, "Length plus width."),
    sb("Perimeter = 2 × 13 = ", 26, "Two thirteens.", "substitute", "Double it: there are two of each side."),
    sb("Check: 26 ÷ 2 = ", 13, "Halve the perimeter.", "substitute", done="That is 9 + 4 again, so 26 cm is right.")],
   rect_fig("9 cm", "4 cm", "Rectangle 9 cm wide and 4 cm tall")),
 prob("Area of a triangle: base 12 cm, height 8 cm.", 48, False,
   "Multiply base by height, then halve.",
   [mc("forgot_half", 96, "Triangle area = ½ × base × height. Do not forget the ½: 96 ÷ 2 = 48.", "12x8=96"),
    mc("added", 20, "Multiply base by height, then halve. Do not add.", "12+8=20")],
   [ss("Triangle area = ½ × base × height."),
    sb("Base × height: 12 × 8 = ", 96, "Multiply the two given lengths."),
    sb("Halve it: 96 ÷ 2 = ", 48, "Ninety-six shared into two.", "substitute", "A triangle is half of its surrounding rectangle."),
    sb("Check: 48 × 2 = ", 96, "Double the area.", "substitute", done="That is 12 × 8, the full rectangle, so 48 cm² is right.")],
   triangle_fig("12 cm", "8 cm", "Triangle, base 12 cm, perpendicular height 8 cm")),
 prob("Area of a parallelogram: base 10 cm, perpendicular height 6 cm.", 60, False,
   "Base times perpendicular height, no halving.",
   [mc("halved", 30, "A parallelogram is not halved: area = base × height = 60 cm².", "half of 60=30"),
    mc("added", 16, "Multiply base and height, do not add: 10 × 6 = 60.", "10+6=16")],
   [ss("Parallelogram area = base × perpendicular height. No halving."),
    sb("Read off the perpendicular height: ", 6, "The straight-up height, not a slanted side."),
    sb("Area = 10 × 6 = ", 60, "Ten sixes.", "substitute", "Multiply base by height, and stop there."),
    sb("Check: 60 ÷ 10 = ", 6, "Divide by the base.", "substitute", done="That gives the height 6 cm back, so 60 cm² is right.")],
   para_fig("10 cm", "6 cm", "Parallelogram, base 10 cm, perpendicular height 6 cm")),
 prob("A square has perimeter 36 cm. What is its area?", 81, False,
   "Find one side (perimeter ÷ 4) first, then square it.",
   [mc("gave_side", 9, "9 cm is the side length. Area = 9 × 9 = 81 cm².", "side not squared"),
    mc("gave_perimeter", 36, "36 cm is the perimeter, not the area. Find the side, then square it.", "gave P")],
   [ss("A square has four equal sides. Find one side first, then square it."),
    sb("One side: 36 ÷ 4 = ", 9, "Perimeter shared into four equal sides."),
    sb("Area = 9 × 9 = ", 81, "Nine squared.", "substitute", "Area of a square = side × side."),
    sb("Check: 9 × 4 = ", 36, "Four sides of 9.", "substitute", done="That rebuilds the 36 cm perimeter, so 81 cm² is right.")],
   square_fig("P = 36 cm", "Square with perimeter 36 cm")),
 prob("Area of a triangle: base 14 cm, height 6 cm.", 42, False,
   "Multiply base by height, then halve.",
   [mc("forgot_half", 84, "½ × 14 × 6 = 42. Remember the ½.", "14x6=84"),
    mc("added", 20, "Area = ½ × base × height, not base + height.", "14+6=20")],
   [ss("Triangle area = ½ × base × height."),
    sb("Base × height: 14 × 6 = ", 84, "Multiply the two lengths."),
    sb("Halve it: 84 ÷ 2 = ", 42, "Eighty-four shared into two.", "substitute", "Then take half."),
    sb("Check: 42 × 2 = ", 84, "Double the area.", "substitute", done="That is 14 × 6, so 42 cm² is right.")],
   triangle_fig("14 cm", "6 cm", "Triangle, base 14 cm, perpendicular height 6 cm")),
 prob("A rectangle has area 48 cm² and length 8 cm. What is the width?", 6, False,
   "Divide the area by the length.",
   [mc("multiplied", 384, "Width = area ÷ length = 48 ÷ 8 = 6 cm, not 48 × 8.", "48x8=384"),
    mc("added", 56, "Divide the area by the length to find the width.", "48+8=56")],
   [ss("Area = length × width, so width = area ÷ length."),
    sb("Read off the area: ", 48, "Given in the question, in cm²."),
    sb("Width = 48 ÷ 8 = ", 6, "How many eights in forty-eight?", "substitute", "Divide the area by the length."),
    sb("Check: 8 × 6 = ", 48, "Length times your width.", "substitute", done="That rebuilds the 48 cm² area, so the width is 6 cm.")],
   rect_fig("8 cm", "? cm", "Rectangle, length 8 cm, area 48 cm squared, width unknown")),
 prob("Perimeter of an equilateral triangle with side 9 cm.", 27, False,
   "Three equal sides: multiply the side by 3.",
   [mc("two_sides", 18, "An equilateral triangle has 3 sides, so 3 × 9 = 27, not 2 × 9.", "2x9=18"),
    mc("squared", 81, "Perimeter adds the sides: 3 × 9 = 27. That is not 9².", "9^2=81")],
   [ss("An equilateral triangle has three equal sides. Perimeter = 3 × side."),
    sb("Number of equal sides: ", 3, "Equilateral means all three the same."),
    sb("Perimeter = 3 × 9 = ", 27, "Three nines.", "substitute", "Add the three equal 9 cm sides."),
    sb("Check: 27 ÷ 3 = ", 9, "Share the perimeter into three.", "substitute", done="That gives one 9 cm side back, so 27 cm is right.")],
   triangle_fig("9 cm", "9 cm", "Equilateral triangle with each side 9 cm", bpx=110, hpx=70)),
]

silver = [
 prob("Circumference of a circle with radius 7 cm. (Use π = 3.14)", 43.96, True,
   "Circumference = 2 × π × r, with π = 3.14.",
   [mc("area", 153.86, "That is the area (πr²). Circumference = 2πr = 2 × 3.14 × 7 = 43.96 cm.", "3.14x49=153.86"),
    mc("used_as_diameter", 21.98, "7 is the radius. Use C = 2πr = 43.96 cm, not πr.", "3.14x7=21.98")],
   [ss("Circumference = 2 × π × r. Here r = 7 and π = 3.14."),
    sb("2 × radius: 2 × 7 = ", 14, "Double the radius to get the diameter."),
    sb("× π: 14 × 3.14 = ", 43.96, "Fourteen times 3.14.", "substitute", "Multiply by π."),
    sb("Check: 43.96 ÷ 3.14 = ", 14, "Divide by π.", "substitute", done="That is 2 × 7, so 43.96 cm is right.")],
   circle_fig("r = 7 cm", "Circle with radius 7 cm", "r")),
 prob("Area of a circle with diameter 10 cm. Give your answer to 1 d.p.", 78.5, True,
   "Halve the diameter, then use π r².",
   [mc("used_diameter", 314.2, "Radius = 5 cm. Area = π × 5² = 78.5 cm², not π × 10².", "pi*100=314.2"),
    mc("circumference", 31.4, "Area = πr², not 2πr. 2π × 5 = 31.4 is a length.", "2pi*5=31.4")],
   [ss("Area = π × r². The diameter is 10, so halve it for the radius."),
    sb("Radius = 10 ÷ 2 = ", 5, "Radius is half the diameter."),
    sb("r squared: 5² = ", 25, "Five times five."),
    sb("× π, to 1 d.p.: 25 × π = ", 78.5, "Twenty-five times 3.14159.", "substitute", "Multiply by π and round."),
    sb("Check: 78.5 ÷ π, to nearest whole = ", 25, "Divide by π.", "substitute", done="That is 5², so 78.5 cm² is right.")],
   circle_fig("d = 10 cm", "Circle with diameter 10 cm", "d")),
 prob("__TRAP__", 32, False,
   "Add the parallel sides, times height, then halve.",
   [mc("forgot_half", 64, "Area = ½(a + b)h = ½ × 16 × 4 = 32 cm². Remember the ½.", "16x4=64"),
    mc("one_side", 12, "Add BOTH parallel sides: 6 + 10 = 16, not just one side.", "0.5x6x4=12")],
   [ss("Trapezium area = ½ × (a + b) × h, where a and b are the parallel sides."),
    sb("Add the parallel sides: 6 + 10 = ", 16, "The two parallel sides."),
    sb("× height: 16 × 4 = ", 64, "Multiply by the height."),
    sb("Halve it: 64 ÷ 2 = ", 32, "Sixty-four into two.", "substitute", "Then take half."),
    sb("Check: 32 × 2 ÷ 4 = ", 16, "Undo the half and the height.", "substitute", done="That is 6 + 10, so 32 cm² is right.")],
   None),
 prob("Arc length of a sector: radius 10 cm, angle 72°. (1 d.p.)", 12.6, True,
   "Take the angle over 360 as a fraction of 2 π r.",
   [mc("full_circle", 62.8, "Multiply by the fraction 72/360 = 0.2: arc = 0.2 × 2π × 10 = 12.6 cm.", "2pi*10=62.8"),
    mc("fraction_inverted", 314.2, "The fraction is 72/360 = 0.2, not 360/72 = 5.", "5x62.8=314.2")],
   [ss("Arc length = (angle ÷ 360) × 2 × π × r. Find the full circumference first."),
    sb("Full circumference: 2 × π × 10, to 1 d.p. = ", 62.8, "2 × π × radius."),
    sb("Fraction of the circle: 72 ÷ 360 = ", 0.2, "The angle out of 360."),
    sb("Arc = 62.8 × 0.2 = ", 12.6, "62.8 times 0.2.", "substitute", "Take that fraction of the circumference."),
    sb("Check: 62.8 ÷ 5, to 1 d.p. = ", 12.6, "A fifth of the circumference.", "substitute", done="0.2 is one fifth, so 12.6 cm is right.")],
   sector_fig("10 cm", 72, "Sector, radius 10 cm, angle 72 degrees")),
 prob("Area of a sector: radius 6 cm, angle 120°. (1 d.p.)", 37.7, True,
   "Take the angle over 360 as a fraction of π r².",
   [mc("full_circle", 113.1, "Multiply by the fraction 120/360 = 1/3: area = π × 36 ÷ 3 = 37.7 cm².", "pi*36=113.1"),
    mc("arc_not_area", 12.6, "Area uses πr², not 2πr. (1/3) × 2π × 6 = 12.6 is a length.", "third of 2pi*6=12.6")],
   [ss("Sector area = (angle ÷ 360) × π × r². Full circle area first."),
    sb("r squared: 6² = ", 36, "Six times six."),
    sb("Full circle: 36 × π, to 1 d.p. = ", 113.1, "π r²."),
    sb("113.1 ÷ 3, to 1 d.p. = ", 37.7, "A third of the full area.", "substitute", "120° is a third of 360°."),
    sb("Check: 37.7 × 3, to 1 d.p. = ", 113.1, "Three thirds make the whole.", "substitute", done="That rebuilds the full circle area, so 37.7 cm² is right.")],
   sector_fig("6 cm", 120, "Sector, radius 6 cm, angle 120 degrees")),
 prob("A semicircle has diameter 14 cm. Find its area. (1 d.p.)", 77.0, True,
   "Halve the diameter, find π r², then halve for a semicircle.",
   [mc("full_circle", 153.9, "A semicircle is HALF a circle: ½ × π × 7² = 77.0 cm².", "pi*49=153.9"),
    mc("used_diameter", 307.9, "Use radius 7 cm, not diameter 14 cm, in πr².", "0.5pi*196=307.9")],
   [ss("A semicircle is half a circle. Area = ½ × π × r². Diameter 14, so radius 7."),
    sb("Radius = 14 ÷ 2 = ", 7, "Half the diameter."),
    sb("r squared: 7² = ", 49, "Seven times seven."),
    sb("Full circle: 49 × π, to 1 d.p. = ", 153.9, "π r²."),
    sb("Halve it: 153.9 ÷ 2, to 1 d.p. = ", 77.0, "Share the circle area in two.", "substitute", "A semicircle is half the circle."),
    sb("Check: 153.9 ÷ 77.0, to nearest whole = ", 2, "How many halves in the whole?", "substitute", done="The full circle is twice the semicircle, so 77.0 cm² is right.")],
   semicircle_fig("14 cm", "Semicircle with diameter 14 cm", show="d")),
 prob("A semicircle has radius 5 cm. Find its perimeter (the curved part plus the diameter). (1 d.p.)", 25.7, True,
   "Curved part is π r; add the straight diameter 2r.",
   [mc("arc_only", 15.7, "Add the straight diameter too: perimeter = π × 5 + 2 × 5 = 25.7 cm.", "pi*5=15.7"),
    mc("used_full_circumference", 41.4, "The curved part is HALF the circumference (πr), not the full 2πr.", "2pi*5+10=41.4")],
   [ss("The perimeter of a semicircle = the curved part + the straight diameter = π r + 2r."),
    sb("Curved part (half the circumference): π × 5, to 1 d.p. = ", 15.7, "π × radius."),
    sb("Straight part (the diameter): 2 × 5 = ", 10, "Twice the radius."),
    sb("Add them: 15.7 + 10 = ", 25.7, "Fifteen point seven plus ten.", "substitute", "Curved plus straight."),
    sb("Check: 25.7 − 10 = ", 15.7, "Take off the diameter.", "substitute", done="That leaves the curved part π × 5, so 25.7 cm is right.")],
   semicircle_fig("r = 5 cm", "Semicircle with radius 5 cm", show="r")),
]
silver[2]["display"] = (trapezium_fig("6 cm", "10 cm", "4 cm", "Trapezium, parallel sides 6 cm and 10 cm, height 4 cm")
    + "Area of a trapezium: parallel sides 6 cm and 10 cm, height 4 cm." + CAP)

gold = [
 prob("A compound shape: rectangle 10 cm × 6 cm with a quarter-circle (radius 6 cm) removed. Find the area. (1 d.p.)", 31.7, True,
   "Rectangle area minus the quarter-circle removed.",
   [mc("added", 88.3, "The quarter-circle is REMOVED, so subtract: 60 − 28.27 = 31.7 cm².", "60+28.27=88.3"),
    mc("semicircle", 3.5, "It is a quarter-circle, not a semicircle. Subtract ¼π(6²) = 28.27, not ½π(6²).", "60-56.55=3.5")],
   [ss("Find the rectangle, then subtract the quarter-circle that has been removed."),
    sb("Rectangle: 10 × 6 = ", 60, "Length × width."),
    sb("Quarter-circle: 0.25 × π × 36, to 2 d.p. = ", 28.27, "A quarter of π × 6²."),
    sb("Subtract, to 1 d.p.: 60 − 28.27 = ", 31.7, "About sixty minus twenty-eight.", "substitute", "Take the removed piece away and round."),
    sb("Check: 31.7 + 28.27, to nearest whole = ", 60, "Add the quarter-circle back.", "substitute", done="That rebuilds the rectangle, so 31.7 cm² is right.")],
   compound_fig("Rectangle 10 cm by 6 cm with a quarter-circle of radius 6 cm removed")),
 prob("A circle has area 154 cm². Find its radius. (1 d.p.)", 7.0, True,
   "Divide the area by π, then square-root.",
   [mc("forgot_root", 49.0, "49.0 is r². Take the square root: r = √49 = 7.0 cm.", "154/pi=49"),
    mc("used_circumference", 24.5, "Use A = πr², so r = √(A/π) = 7.0. Do not use A = 2πr.", "154/2pi=24.5")],
   [ss("Area = π r². Work backwards: divide by π, then square-root."),
    sb("Divide the area by π: 154 ÷ π, to 1 d.p. = ", 49.0, "Undo the × π."),
    sb("Square-root it: √49, to 1 d.p. = ", 7.0, "What number squared is about 49?", "substitute", "Undo the squaring."),
    sb("Check: 7² × π, to nearest whole = ", 154, "Square it and times π.", "substitute", done="That rebuilds the 154 cm² area, so r = 7.0 cm.")],
   circle_fig("A = 154 cm²", "Circle with area 154 cm squared, radius unknown", "d")),
 prob("A sector has area 24π cm² and radius 12 cm. Find the angle.", 60, False,
   "The π cancels; solve 24 = (θ/360) × 144 for θ.",
   [mc("forgot_square", 720, "Square the radius: use r² = 144, not r = 12. Then θ = 60°.", "24*360/12=720"),
    mc("used_arc", 360, "24π is an AREA, so use πr² (144π), not the arc formula 2πr.", "arc gives 360")],
   [ss("Sector area = (θ ÷ 360) × π r². Set it equal to 24π and the π cancels."),
    sb("r squared: 12² = ", 144, "Twelve times twelve."),
    sb("θ = 24 × 360 ÷ 144 = ", 60, "24 × 360, then share by 144.", "substitute", "Cancel π, then rearrange for θ."),
    sb("Check: (60 ÷ 360) × 144 = ", 24, "A sixth of 144.", "substitute", done="That is the 24 (before the π), so 60° is right.")],
   sector_fig("12 cm", 60, "Sector, radius 12 cm, area 24 pi, angle unknown")),
 prob("A running track is two straights (100 m each) and two semicircles (diameter 60 m). Find the total length. (nearest m)", 388, True,
   "Two straights plus one full circle (πd) for the two ends.",
   [mc("straights_only", 200, "Add the curved ends too: the two semicircles make a full circle, πd = 188.5 m.", "only straights=200"),
    mc("used_radius", 577, "60 m is the DIAMETER, so C = π × 60 = 188.5 m, not 2π × 60.", "2pi*60+200=577")],
   [ss("The two straights are one length; the two semicircular ends make one full circle. Add them."),
    sb("Two straights: 2 × 100 = ", 200, "Both straights."),
    sb("The two ends make one circle, diameter 60. Circumference = π × 60, to 1 d.p. = ", 188.5, "π times the diameter."),
    sb("Total: 200 + 188.5 = ", 388.5, "Two hundred plus 188.5.", "substitute", "Add the straights and the curved ends."),
    sb("The fuller value is 388.49, just under 388.5, so to the nearest metre it is ", 388, "Under a half rounds down.", "substitute", "Round to the nearest metre."),
    sb("Check: 388 − 200 = ", 188, "Take off the straights.", "substitute", done="That is the curved circle length π × 60 ≈ 188.5, so 388 m is right.")],
   track_fig("Running track: two 100 m straights with two semicircular ends of diameter 60 m")),
 prob("An annulus has outer radius 10 cm and inner radius 6 cm. Find its area. (1 d.p.)", 201.1, True,
   "Outer circle area minus inner circle area.",
   [mc("subtracted_radii", 50.3, "Subtract AREAS, not radii: π(10²) − π(6²) = 64π = 201.1 cm².", "pi*16=50.3"),
    mc("forgot_subtract", 314.2, "An annulus is a ring: subtract the inner circle from the outer circle.", "outer only=314.2")],
   [ss("An annulus is a ring: outer circle area minus inner circle area."),
    sb("Outer area: π × 10², to 1 d.p. = ", 314.2, "π R²."),
    sb("Inner area: π × 6², to 1 d.p. = ", 113.1, "π r²."),
    sb("Subtract: 314.2 − 113.1 = ", 201.1, "Outer minus inner.", "substitute", "Take the hole out of the disc."),
    sb("Check: 201.1 + 113.1, to nearest whole = ", 314, "Add the inner circle back.", "substitute", done="That rebuilds the outer circle, so 201.1 cm² is right.")],
   annulus_fig("R = 10", "r = 6", "Annulus, outer radius 10 cm, inner radius 6 cm")),
]

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Area and perimeter of rectangles, triangles, parallelograms and squares",
    "silver_description": "Circles, sectors, trapeziums and semicircles",
    "gold_description": "Compound shapes, reverse problems, sectors and the annulus",
}

pd["tier_guides"] = {
 "bronze": {"title": "Bronze: rectangles, triangles and parallelograms",
  "steps": [
   "<strong>Rectangle</strong>: area = length × width; perimeter = 2 × (length + width).",
   "<strong>Triangle</strong>: area = ½ × base × height, using the perpendicular height.",
   "<strong>Parallelogram</strong>: area = base × perpendicular height, no halving. A square's side is its perimeter ÷ 4."],
  "example": {"question": "Find the area of a triangle with base 10 cm and height 6 cm.",
   "steps": [{"label": "Base × height", "content": "10 × 6 = 60"},
    {"label": "Halve it", "content": "60 ÷ 2 = 30"},
    {"label": "Check", "content": "30 × 2 = 60, the full rectangle"},
    {"label": "Answer", "content": "30 cm²", "isAnswer": True, "is_answer": True}]}},
 "silver": {"title": "Silver: circles, sectors and trapeziums",
  "steps": [
   "<strong>Circle</strong>: area = \\(\\pi r^2\\); circumference = \\(2\\pi r\\). Halve a diameter to get the radius first.",
   "<strong>Sector</strong>: take the fraction (angle ÷ 360) of the whole circle: of the area for a sector area, of \\(2\\pi r\\) for an arc.",
   "<strong>Trapezium</strong>: area = ½ × (a + b) × h, adding the two parallel sides."],
  "example": {"question": "Find the area of a sector with radius 8 cm and angle 90°.",
   "steps": [{"label": "Full circle", "content": "\\(\\pi \\times 8^2 = 201.06\\)"},
    {"label": "Fraction", "content": "90 ÷ 360 = ¼, so 201.06 ÷ 4 = 50.27"},
    {"label": "Check", "content": "50.27 × 4 ≈ 201, the whole circle"},
    {"label": "Answer", "content": "50.3 cm² (1 d.p.)", "isAnswer": True, "is_answer": True}]}},
 "gold": {"title": "Gold: compound shapes and reverse problems",
  "steps": [
   "Split a compound shape into simple parts, then <strong>add</strong> areas that join or <strong>subtract</strong> a piece that is removed.",
   "For a reverse problem, run the formula backwards: to find a radius from an area, divide by \\(\\pi\\) then square-root.",
   "An annulus (a ring) is the outer circle area minus the inner circle area."],
  "example": {"question": "A rectangle 12 cm by 8 cm has a semicircle of diameter 8 cm removed. Find the area.",
   "steps": [{"label": "Rectangle", "content": "12 × 8 = 96"},
    {"label": "Semicircle", "content": "½ × π × 4² = 25.13"},
    {"label": "Subtract and check", "content": "96 − 25.13 = 70.87; 70.87 + 25.13 = 96"},
    {"label": "Answer", "content": "70.9 cm² (1 d.p.)", "isAnswer": True, "is_answer": True}]}}
}

pd["guided"] = {
 "opener": {"steps": [
   {"say": "A kitchen floor is tiled with square tiles, 5 across and 3 down. No formulas needed, just count.",
    "display": grid_fig(5, 3, "A grid of square tiles, 5 across and 3 down")},
   {"pre": "How many tiles cover the whole floor? ", "post": "", "answer": 15,
    "hint": "5 tiles in each row, and there are 3 rows: 5 × 3."},
   {"say": "You worked out 5 × 3 = 15. Counting how many unit squares fill a shape IS finding its <strong>area</strong>. So area of a rectangle = length × width."},
   {"pre": "Now walk right around the very edge, one tile-length at a time. How many tile-lengths is the whole loop? ", "post": "", "answer": 16,
    "hint": "5 + 3 + 5 + 3, or 2 × (5 + 3)."},
   {"say": "That loop is the <strong>perimeter</strong>: the distance all the way round, \\(2 \\times (5 + 3) = 16\\). Area fills the inside; perimeter measures the border. Every problem ahead uses one or the other."}
 ]},
 "teach": {
  "bronze": {"display": rect_fig("8 cm", "5 cm", "Rectangle 8 cm by 5 cm") + CAP,
   "steps": [
    {"say": "A rectangle is 8 cm by 5 cm. Find its area, then its perimeter."},
    {"pre": "Area = length × width: 8 × 5 = ", "post": "", "answer": 40, "hint": "Multiply the two sides."},
    {"say": "Now the perimeter: add all four sides, which is 2 × (length + width)."},
    {"pre": "Add the two different sides: 8 + 5 = ", "post": "", "answer": 13, "hint": "Length plus width."},
    {"pre": "Double it: 2 × 13 = ", "post": "", "answer": 26, "hint": "Two of each side."},
    {"pre": "Check the area: 40 ÷ 8 = ", "post": "", "answer": 5, "hint": "Divide the area by the length.",
     "done": "That gives the width 5 cm back, so area 40 cm² and perimeter 26 cm are right."}]},
  "silver": {"display": sector_fig("9 cm", 120, "Sector, radius 9 cm, angle 120 degrees") + CAP,
   "steps": [
    {"say": "A sector has radius 9 cm and angle 120°. Find its area, to 1 d.p."},
    {"pre": "r squared: 9² = ", "post": "", "answer": 81, "hint": "Nine times nine."},
    {"pre": "Full circle: 81 × π, to 1 d.p. = ", "post": "", "answer": 254.5, "hint": "π r²."},
    {"say": "120° out of 360° is one third of the circle."},
    {"pre": "One third: 254.5 ÷ 3, to 1 d.p. = ", "post": "", "answer": 84.8, "hint": "Share the full area into three."},
    {"pre": "Check: 84.8 × 3, to nearest whole = ", "post": "", "answer": 254, "hint": "Three thirds make the whole.",
     "done": "That rebuilds the full circle area, so 84.8 cm² is right."}]},
  "gold": {"display": compound_add_fig("Rectangle 10 cm by 4 cm with a semicircle of diameter 4 cm added on one end") + CAP,
   "steps": [
    {"say": "A rectangle 10 cm by 4 cm has a semicircle of diameter 4 cm added on one end. Find the total area, to 1 d.p."},
    {"pre": "Rectangle: 10 × 4 = ", "post": "", "answer": 40, "hint": "Length × width."},
    {"say": "The semicircle has diameter 4, so radius 2."},
    {"pre": "Semicircle: 0.5 × π × 2², to 1 d.p. = ", "post": "", "answer": 6.3, "hint": "Half of π × 2²."},
    {"pre": "Add them: 40 + 6.3 = ", "post": "", "answer": 46.3, "hint": "Rectangle plus semicircle."},
    {"pre": "Check: 46.3 − 40, to 1 d.p. = ", "post": "", "answer": 6.3, "hint": "Take the rectangle off.",
     "done": "That leaves the semicircle area, so 46.3 cm² is right."}]}
 }
}

pd["method_card"] = {
 "title": "Area & Perimeter Formulas",
 "steps": [
  "Pick the shape and its formula.",
  "Put in the given lengths, using the perpendicular height for triangles and parallelograms.",
  "Work it out and add the unit: cm² for area, cm for length.",
  "For a compound shape, split into parts and add or subtract the areas."],
 "content": "<p>Rectangle area is length times width; its perimeter is twice the sum of length and width. A triangle is half of base times height. A parallelogram is base times perpendicular height. A trapezium is half of the two parallel sides added, times the height. A circle has area \\(\\pi r^2\\) and circumference \\(2\\pi r\\). A sector or arc takes the angle over 360 as its fraction of the whole circle.</p>",
 "example": "<p><strong>Trapezium, parallel sides 8 cm and 12 cm, height 5 cm:</strong> area = \\(\\tfrac{1}{2}(8 + 12) \\times 5 = 50\\) cm².</p>"
}

for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

out = "lesson_maths-eduqas_geometry-L02.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", list(pd.keys()))
