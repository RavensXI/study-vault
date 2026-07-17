# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_geoL03.json", encoding="utf-8"))

MINUS = "−"  # unicode minus
PI = "π"

def T(x, y, s, anchor="middle", size=11):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="600" fill="currentColor">{s}</text>'

def wrap(inner, aria):
    return (f'<svg viewBox="0 0 240 160" role="img" aria-label="{aria}" '
            f'style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
            f'{inner}</svg><span class="figure-caption">Diagram not drawn accurately</span> ')

BLUE = '#60a5fa'

def cuboid(length=None, width=None, height=None, aria="A cuboid"):
    inner = (
        f'<polygon points="50,70 150,70 188,44 88,44" fill="{BLUE}" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
        f'<polygon points="150,70 188,44 188,104 150,130" fill="{BLUE}" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
        f'<rect x="50" y="70" width="100" height="60" fill="{BLUE}" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    )
    if length is not None:
        inner += T(100, 146, length)
    if height is not None:
        inner += T(42, 104, height, "end")
    if width is not None:
        inner += T(174, 52, width, "start")
    return wrap(inner, aria)

def cube(side, aria="A cube"):
    inner = (
        f'<polygon points="50,70 150,70 188,44 88,44" fill="{BLUE}" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
        f'<polygon points="150,70 188,44 188,104 150,130" fill="{BLUE}" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
        f'<rect x="50" y="70" width="100" height="60" fill="{BLUE}" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    )
    inner += T(100, 146, side)
    return wrap(inner, aria)

def cylinder(r_label=None, h_label=None, d_label=None, aria="A cylinder"):
    inner = (
        '<line x1="76" y1="44" x2="76" y2="120" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="164" y1="44" x2="164" y2="120" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="120" rx="44" ry="13" fill="{BLUE}" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="44" rx="44" ry="13" fill="{BLUE}" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>'
        '<circle cx="120" cy="44" r="2.2" fill="currentColor"/>'
    )
    if d_label is not None:
        inner += '<line x1="76" y1="44" x2="164" y2="44" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2"/>'
        inner += T(120, 38, d_label)
    elif r_label is not None:
        inner += '<line x1="120" y1="44" x2="164" y2="44" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2"/>'
        inner += T(142, 38, r_label, "middle", 10)
    if h_label is not None:
        inner += '<line x1="176" y1="44" x2="176" y2="120" stroke="currentColor" stroke-width="1"/>'
        inner += '<line x1="172" y1="44" x2="180" y2="44" stroke="currentColor" stroke-width="1"/>'
        inner += '<line x1="172" y1="120" x2="180" y2="120" stroke="currentColor" stroke-width="1"/>'
        inner += T(184, 86, h_label, "start", 10)
    return wrap(inner, aria)

def cone(r_label=None, h_label=None, slant_label=None, aria="A cone"):
    inner = (
        f'<path d="M120,26 L74,124 L166,124 Z" fill="{BLUE}" fill-opacity="0.14" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="124" rx="46" ry="13" fill="{BLUE}" fill-opacity="0.2" stroke="currentColor" stroke-width="1.6"/>'
    )
    if h_label is not None:
        inner += '<line x1="120" y1="26" x2="120" y2="124" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
        inner += '<path d="M120,116 L128,116 L128,124" fill="none" stroke="currentColor" stroke-width="1"/>'
        inner += T(128, 82, h_label, "start", 10)
    if r_label is not None:
        inner += '<line x1="120" y1="124" x2="166" y2="124" stroke="currentColor" stroke-width="1.3"/>'
        inner += '<circle cx="120" cy="124" r="2.2" fill="currentColor"/>'
        inner += T(143, 138, r_label, "middle", 10)
    if slant_label is not None:
        inner += T(150, 74, slant_label, "start", 10)
    return wrap(inner, aria)

def sphere(r_label=None, sa_label=None, aria="A sphere"):
    inner = (
        f'<circle cx="120" cy="86" r="52" fill="{BLUE}" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
        '<ellipse cx="120" cy="86" rx="52" ry="15" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
        '<circle cx="120" cy="86" r="2.4" fill="currentColor"/>'
    )
    if r_label is not None:
        inner += '<line x1="120" y1="86" x2="172" y2="86" stroke="currentColor" stroke-width="1.3"/>'
        inner += T(146, 80, r_label, "middle", 10)
    if sa_label is not None:
        inner += T(120, 24, sa_label, "middle", 11)
    return wrap(inner, aria)

def prism_tri(area_label, len_label, aria="A triangular prism"):
    inner = (
        f'<polygon points="40,124 104,124 72,60" fill="{BLUE}" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6"/>'
        '<polygon points="110,106 174,106 142,42" fill="none" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="40" y1="124" x2="110" y2="106" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="104" y1="124" x2="174" y2="106" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="72" y1="60" x2="142" y2="42" stroke="currentColor" stroke-width="1.4"/>'
    )
    inner += T(71, 112, area_label, "middle", 10)
    inner += T(120, 74, len_label, "middle", 10)
    return wrap(inner, aria)

def pyramid(base_label, h_label, aria="A square-based pyramid"):
    inner = (
        f'<polygon points="60,122 150,122 188,98 98,98" fill="{BLUE}" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="124" y1="34" x2="60" y2="122" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="124" y1="34" x2="150" y2="122" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="124" y1="34" x2="188" y2="98" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="124" y1="34" x2="98" y2="98" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="124" y1="34" x2="124" y2="110" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
        '<circle cx="124" cy="110" r="2" fill="currentColor"/>'
    )
    inner += T(103, 136, base_label, "middle", 10)
    inner += T(132, 78, h_label, "start", 10)
    return wrap(inner, aria)

def hemisphere(r_label, aria="A hemisphere"):
    inner = (
        f'<path d="M64,102 A56 56 0 0 1 176,102" fill="{BLUE}" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="102" rx="56" ry="14" fill="{BLUE}" fill-opacity="0.2" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="120" y1="102" x2="176" y2="102" stroke="currentColor" stroke-width="1.3"/>'
        '<circle cx="120" cy="102" r="2.2" fill="currentColor"/>'
    )
    inner += T(146, 96, r_label, "middle", 10)
    return wrap(inner, aria)

def cyl_hemi(r_label, h_label, aria="A cylinder with a hemisphere on top"):
    inner = (
        '<line x1="78" y1="66" x2="78" y2="132" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="162" y1="66" x2="162" y2="132" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="132" rx="42" ry="12" fill="{BLUE}" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
        f'<path d="M78,66 A42 42 0 0 1 162,66" fill="{BLUE}" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
        '<ellipse cx="120" cy="66" rx="42" ry="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>'
        '<circle cx="120" cy="66" r="2.2" fill="currentColor"/>'
        '<line x1="120" y1="66" x2="162" y2="66" stroke="currentColor" stroke-width="1.2"/>'
    )
    inner += T(140, 60, r_label, "middle", 10)
    inner += '<line x1="174" y1="66" x2="174" y2="132" stroke="currentColor" stroke-width="1"/>'
    inner += T(182, 102, h_label, "start", 10)
    return wrap(inner, aria)

def sphere_in_cyl(r_label, aria="A sphere fitting exactly inside a cylinder"):
    inner = (
        '<line x1="72" y1="42" x2="72" y2="138" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="168" y1="42" x2="168" y2="138" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="138" rx="48" ry="13" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="42" rx="48" ry="13" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        f'<circle cx="120" cy="90" r="48" fill="{BLUE}" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
        '<line x1="120" y1="90" x2="168" y2="90" stroke="currentColor" stroke-width="1.2"/>'
        '<circle cx="120" cy="90" r="2.2" fill="currentColor"/>'
    )
    inner += T(142, 84, r_label, "middle", 10)
    return wrap(inner, aria)

def frustum(aria="A frustum formed by removing a small cone from a large cone"):
    inner = (
        f'<path d="M120,24 L60,138 L180,138 Z" fill="{BLUE}" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="138" rx="60" ry="15" fill="{BLUE}" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
        '<ellipse cx="120" cy="62" rx="20" ry="6" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
        '<line x1="120" y1="24" x2="120" y2="138" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>'
        '<line x1="120" y1="138" x2="180" y2="138" stroke="currentColor" stroke-width="1.2"/>'
        '<line x1="120" y1="62" x2="140" y2="62" stroke="currentColor" stroke-width="1.2"/>'
    )
    inner += T(152, 152, "r = 6", "middle", 10)
    inner += T(146, 58, "r = 2", "start", 10)
    inner += T(112, 104, "9", "end", 10)
    inner += T(112, 46, "3", "end", 10)
    return wrap(inner, aria)

def cube_grid(aria="A box split into 1 cm cubes, 3 long, 2 deep and 2 tall"):
    inner = (
        # top face (depth) as parallelogram
        f'<polygon points="50,60 170,60 200,38 80,38" fill="{BLUE}" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>'
        f'<polygon points="170,60 200,38 200,98 170,120" fill="{BLUE}" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>'
        f'<rect x="50" y="60" width="120" height="60" fill="{BLUE}" fill-opacity="0.14" stroke="currentColor" stroke-width="1.6"/>'
        # front grid: 3 columns, 2 rows
        '<line x1="90" y1="60" x2="90" y2="120" stroke="currentColor" stroke-width="1"/>'
        '<line x1="130" y1="60" x2="130" y2="120" stroke="currentColor" stroke-width="1"/>'
        '<line x1="50" y1="90" x2="170" y2="90" stroke="currentColor" stroke-width="1"/>'
        # top grid depth lines
        '<line x1="65" y1="49" x2="185" y2="49" stroke="currentColor" stroke-width="0.8"/>'
        '<line x1="90" y1="60" x2="120" y2="38" stroke="currentColor" stroke-width="0.8"/>'
        '<line x1="130" y1="60" x2="160" y2="38" stroke="currentColor" stroke-width="0.8"/>'
    )
    inner += T(110, 138, "each cube = 1 cm", "middle", 10)
    return wrap(inner, aria)


# ---------- helpers to build steps ----------
def say(t): return {"say": t}
def box(pre, answer, hint, post="", done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}


# ================= BRONZE =================
bronze = []

# B0 cuboid 6x4x3 V=72
bronze.append({
 "display": cuboid("6 cm", "4 cm", "3 cm", "A cuboid 6 cm by 4 cm by 3 cm") + live["problem_bank"]["bronze"][0]["display"],
 "solutions": [72], "calculator": False, "input_type": "single_value",
 "hint": "Volume of a cuboid is length × width × height.",
 "misconceptions": [mc("surface_area", 108,
   "108 cm² is the surface area, 2(lw + lh + wh). Volume is l × w × h = 6 × 4 × 3 = 72 cm³.")],
 "guided_steps": [
   say("Volume of a cuboid is length × width × height. Multiply all three."),
   box("Multiply length by width: 6 × 4 = ", 24, "Six fours."),
   box("Now multiply by the height: 24 × 3 = ", 72, "24 threes.", done="That is the volume, 72 cm³.", phase="substitute"),
   box("Check another way: 4 × 3 × 6 = ", 72, "Same three numbers, any order.", done="Still 72, so V = 72 cm³.", phase="substitute"),
 ]})

# B1 SA cube side 5 =150
bronze.append({
 "display": cube("5 cm", "A cube of side 5 cm") + live["problem_bank"]["bronze"][1]["display"],
 "solutions": [150], "calculator": False, "input_type": "single_value",
 "hint": "A cube has 6 identical square faces: find one, then times by 6.",
 "misconceptions": [mc("gave_volume", 125,
   "125 cm³ is the volume (5³). Surface area = 6 × 5² = 6 × 25 = 150 cm².")],
 "guided_steps": [
   say("A cube has 6 identical square faces. Find one face, then multiply by 6."),
   box("Area of one face: 5 × 5 = ", 25, "Side times side."),
   box("Six faces: 6 × 25 = ", 150, "Six lots of 25.", done="So SA = 150 cm².", phase="substitute"),
   box("Compare: the volume would be 5 × 5 × 5 = ", 125, "Side cubed.", done="125 is the volume; the surface area is 150 cm².", phase="substitute"),
 ]})

# B2 tri prism area 12 len 10 V=120
bronze.append({
 "display": prism_tri("area 12 cm²", "length 10 cm", "A triangular prism, cross-section 12 cm squared, length 10 cm") + live["problem_bank"]["bronze"][2]["display"],
 "solutions": [120], "calculator": False, "input_type": "single_value",
 "hint": "Volume of any prism is the cross-section area times the length.",
 "misconceptions": [mc("added", 22,
   "Multiply, do not add: volume of a prism = cross-section area × length = 12 × 10 = 120 cm³.")],
 "guided_steps": [
   say("Volume of any prism is the cross-section area times the length."),
   box("Write the cross-section area: ", 12, "Given as 12 cm²."),
   box("Multiply by the length: 12 × 10 = ", 120, "12 tens.", done="So V = 120 cm³.", phase="substitute"),
   box("Check: 120 ÷ 10 = ", 12, "Divide back by the length.", done="Back to the 12 cm² cross-section, so V = 120 cm³.", phase="substitute"),
 ]})

# B3 cylinder r3 h7 V=197.9
bronze.append({
 "display": cylinder("r = 3 cm", "h = 7 cm", None, "A cylinder of radius 3 cm and height 7 cm") + live["problem_bank"]["bronze"][3]["display"],
 "solutions": [197.9], "calculator": True, "input_type": "single_value",
 "hint": "Volume of a cylinder is π r² h. Square the radius first.",
 "misconceptions": [mc("no_square", 66.0,
   "The radius must be squared: V = π × 3² × 7 = 63π = 197.9 cm³, not π × 3 × 7.")],
 "guided_steps": [
   say("Volume of a cylinder is \\(\\pi r^2 h\\). Square the radius first."),
   box("Square the radius: 3² = ", 9, "3 × 3."),
   box("Multiply by the height: 9 × 7 = ", 63, "This is the r²h part."),
   box("Multiply by π: 63 × π = ", 197.9, "Use the π button, round to 1 d.p.", done="So V = 197.9 cm³.", phase="substitute"),
   box("Check in one go: π × 3² × 7 rounds to ", 197.9, "Same calculation together.", done="Still 197.9 cm³.", phase="substitute"),
 ]})

# B4 cuboid V180 l9 w5 h=4
bronze.append({
 "display": cuboid("9 cm", "5 cm", "?", "A cuboid of length 9 cm, width 5 cm and unknown height") + live["problem_bank"]["bronze"][4]["display"],
 "solutions": [4], "calculator": False, "input_type": "single_value",
 "hint": "Height = volume ÷ (length × width).",
 "misconceptions": [mc("one_dim", 20,
   "Divide by BOTH known lengths: height = 180 ÷ (9 × 5) = 180 ÷ 45 = 4 cm. Dividing by only the 9 gives 20.")],
 "guided_steps": [
   say("Volume = length × width × height, so height = volume ÷ (length × width)."),
   box("Multiply length by width: 9 × 5 = ", 45, "This is the base area."),
   box("Divide the volume by the base area: 180 ÷ 45 = ", 4, "180 shared into 45s.", done="So the height is 4 cm.", phase="substitute"),
   box("Check: 9 × 5 × 4 = ", 180, "Rebuild the volume.", done="Back to 180 cm³, so h = 4 cm.", phase="substitute"),
 ]})

# B5 cube side 4 V=64
bronze.append({
 "display": cube("4 cm", "A cube of side 4 cm") + live["problem_bank"]["bronze"][5]["display"],
 "solutions": [64], "calculator": False, "input_type": "single_value",
 "hint": "Volume of a cube is side × side × side.",
 "misconceptions": [mc("gave_sa", 96,
   "96 cm² is the surface area (6 × 4²). Volume = 4³ = 64 cm³.")],
 "guided_steps": [
   say("Volume of a cube is side × side × side."),
   box("Square the side: 4 × 4 = ", 16, "Four fours."),
   box("Multiply by the side again: 16 × 4 = ", 64, "16 fours.", done="So V = 64 cm³.", phase="substitute"),
   box("Compare: the surface area would be 6 × 16 = ", 96, "Six faces of 4 × 4.", done="96 is the surface area; the volume is 64 cm³.", phase="substitute"),
 ]})

# B6 cylinder d10 h6 V=471.2
bronze.append({
 "display": cylinder(None, "h = 6 cm", "d = 10 cm", "A cylinder of diameter 10 cm and height 6 cm") + live["problem_bank"]["bronze"][6]["display"],
 "solutions": [471.2], "calculator": True, "input_type": "single_value",
 "hint": "The diameter is 10 cm, so halve it to get the radius first.",
 "misconceptions": [mc("used_diameter", 1885.0,
   "Halve the diameter first: radius = 5 cm, so V = π × 5² × 6 = 150π = 471.2 cm³. Using 10 as the radius gives 1885.0.")],
 "guided_steps": [
   say("The diameter is 10 cm, so halve it to get the radius first."),
   box("Radius = 10 ÷ 2 = ", 5, "Half the diameter."),
   box("Square the radius: 5² = ", 25, "5 × 5."),
   box("Multiply by the height: 25 × 6 = ", 150, "This is r²h."),
   box("Multiply by π: 150 × π = ", 471.2, "π button, 1 d.p.", done="So V = 471.2 cm³.", phase="substitute"),
   box("Check in one go: π × 5² × 6 rounds to ", 471.2, "All together.", done="Still 471.2 cm³.", phase="substitute"),
 ]})

# B7 SA cuboid 8x3x2 =92
bronze.append({
 "display": cuboid("8 cm", "3 cm", "2 cm", "A cuboid 8 cm by 3 cm by 2 cm") + live["problem_bank"]["bronze"][7]["display"],
 "solutions": [92], "calculator": False, "input_type": "single_value",
 "hint": "Surface area of a cuboid is 2(lw + lh + wh). Find the three different faces first.",
 "misconceptions": [mc("gave_volume", 48,
   "48 cm³ is the volume. Surface area = 2(lw + lh + wh) = 2(24 + 16 + 6) = 92 cm².")],
 "guided_steps": [
   say("Surface area of a cuboid is 2(lw + lh + wh). Find the three different faces first."),
   box("Top and bottom face: 8 × 3 = ", 24, "length × width."),
   box("Front and back face: 8 × 2 = ", 16, "length × height."),
   box("Side face: 3 × 2 = ", 6, "width × height."),
   box("Add the three and double: 2 × (24 + 16 + 6) = ", 92, "2 × 46.", done="So SA = 92 cm².", phase="substitute"),
   box("Check the half first: 24 + 16 + 6 = ", 46, "That is half the surface area.", done="Doubled gives 92 cm².", phase="substitute"),
 ]})


# ================= SILVER =================
silver = []

# S0 cone r5 h12 V=314.2
silver.append({
 "display": cone("r = 5 cm", "h = 12 cm", None, "A cone of radius 5 cm and height 12 cm") + live["problem_bank"]["silver"][0]["display"],
 "solutions": [314.2], "calculator": True, "input_type": "single_value",
 "hint": "Volume of a cone is one third of π r² h.",
 "misconceptions": [mc("no_third", 942.5,
   "That is the full cylinder. A cone is one third: V = ⅓ × π × 5² × 12 = 100π = 314.2 cm³.")],
 "guided_steps": [
   say("Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). Build the \\(\\pi r^2 h\\) part, then take a third."),
   box("Square the radius: 5² = ", 25, "5 × 5."),
   box("Multiply by the height: 25 × 12 = ", 300, "This is r²h."),
   box("Take one third: 300 ÷ 3 = ", 100, "The cone's ⅓ factor."),
   box("Multiply by π: 100 × π = ", 314.2, "π button, 1 d.p.", done="So V = 314.2 cm³.", phase="substitute"),
   box("Check in one go: ⅓ × π × 25 × 12 rounds to ", 314.2, "All together.", done="Still 314.2 cm³.", phase="substitute"),
 ]})

# S1 sphere r6 V=904.8
silver.append({
 "display": sphere("r = 6 cm", None, "A sphere of radius 6 cm") + live["problem_bank"]["silver"][1]["display"],
 "solutions": [904.8], "calculator": True, "input_type": "single_value",
 "hint": "Volume of a sphere is four thirds of π r³. Cube the radius first.",
 "misconceptions": [mc("squared_radius", 150.8,
   "Cube the radius, do not square it: V = \\(\\frac{4}{3}\\) × π × 6³ = 288π = 904.8 cm³.")],
 "guided_steps": [
   say("Volume of a sphere is \\(\\frac{4}{3}\\pi r^3\\). Cube the radius first."),
   box("Cube the radius: 6³ = ", 216, "6 × 6 × 6."),
   box("Multiply by 4: 216 × 4 = ", 864, "Four lots."),
   box("Divide by 3: 864 ÷ 3 = ", 288, "The four-thirds factor."),
   box("Multiply by π: 288 × π = ", 904.8, "π button, 1 d.p.", done="So V = 904.8 cm³.", phase="substitute"),
   box("Check in one go: \\(\\frac{4}{3}\\) × π × 216 rounds to ", 904.8, "All together.", done="Still 904.8 cm³.", phase="substitute"),
 ]})

# S2 sphere r4 SA=201.1
silver.append({
 "display": sphere("r = 4 cm", None, "A sphere of radius 4 cm") + live["problem_bank"]["silver"][2]["display"],
 "solutions": [201.1], "calculator": True, "input_type": "single_value",
 "hint": "Surface area of a sphere is 4 π r². Square the radius first.",
 "misconceptions": [mc("gave_volume", 268.1,
   "That is the volume. Surface area = 4 π r² = 4 × π × 4² = 64π = 201.1 cm².")],
 "guided_steps": [
   say("Surface area of a sphere is \\(4\\pi r^2\\). Square the radius first."),
   box("Square the radius: 4² = ", 16, "4 × 4."),
   box("Multiply by 4: 16 × 4 = ", 64, "Four lots of r²."),
   box("Multiply by π: 64 × π = ", 201.1, "π button, 1 d.p.", done="So SA = 201.1 cm².", phase="substitute"),
   box("Check in one go: 4 × π × 4² rounds to ", 201.1, "All together.", done="Still 201.1 cm².", phase="substitute"),
 ]})

# S3 cylinder SA=150pi r5 h=10
silver.append({
 "display": cylinder("r = 5 cm", "h = ?", None, "A cylinder of radius 5 cm and unknown height, surface area 150 pi") + live["problem_bank"]["silver"][3]["display"],
 "solutions": [10], "calculator": False, "input_type": "single_value",
 "hint": "Surface area of a cylinder is 2πr² + 2πrh. Work in multiples of π.",
 "misconceptions": [mc("forgot_ends", 15,
   "Subtract the two circular ends first: 150π − 50π = 100π = 2πrh, giving h = 10 cm. Forgetting the ends gives 15.")],
 "guided_steps": [
   say("Surface area of a cylinder is \\(2\\pi r^2 + 2\\pi r h\\). Work in multiples of π so it stays exact."),
   box("The two circular ends are 2πr². In π units: 2 × 5² = ", 50, "2πr² = 50π."),
   box("Take the ends off the total: 150 − 50 = ", 100, "150π minus 50π.", done="So the curved part is 100π.", phase="substitute"),
   box("The curved part is 2πrh = 10πh, so 100 = 10h, h = 100 ÷ 10 = ", 10, "100 shared into 10.", done="So the height is 10 cm.", phase="substitute"),
   box("Check: 50π + 2π(5)(10) in π units is 50 + 100 = ", 150, "Total in π units.", done="150π, matching the given surface area.", phase="substitute"),
 ]})

# S4 pyramid base6 h10 V=120
silver.append({
 "display": pyramid("6 cm", "h = 10 cm", "A pyramid with square base of side 6 cm and height 10 cm") + live["problem_bank"]["silver"][4]["display"],
 "solutions": [120], "calculator": False, "input_type": "single_value",
 "hint": "Volume of a pyramid is one third of base area × height.",
 "misconceptions": [mc("no_third", 360,
   "That is base area × height with no third. A pyramid is one third: V = ⅓ × 36 × 10 = 120 cm³.")],
 "guided_steps": [
   say("Volume of a pyramid is \\(\\frac{1}{3} \\times\\) base area \\(\\times h\\). Find the base area first."),
   box("Base area (square): 6 × 6 = ", 36, "Side squared."),
   box("Multiply by the height: 36 × 10 = ", 360, "base area × height."),
   box("Take one third: 360 ÷ 3 = ", 120, "The pyramid's ⅓ factor.", done="So V = 120 cm³.", phase="substitute"),
   box("Check: ⅓ × 36 × 10 = ", 120, "All together.", done="Still 120 cm³.", phase="substitute"),
 ]})

# S5 hemisphere r9 V=1526.8
silver.append({
 "display": hemisphere("r = 9 cm", "A hemisphere of radius 9 cm") + live["problem_bank"]["silver"][5]["display"],
 "solutions": [1526.8], "calculator": True, "input_type": "single_value",
 "hint": "A hemisphere is half a sphere: find the full sphere, then halve it.",
 "misconceptions": [mc("full_sphere", 3053.6,
   "A hemisphere is HALF a sphere: V = ½ × \\(\\frac{4}{3}\\) × π × 9³ = 486π = 1526.8 cm³. The full sphere (3053.6) is double.")],
 "guided_steps": [
   say("A hemisphere is half a sphere. Find the full sphere's volume, then halve it."),
   box("Cube the radius: 9³ = ", 729, "9 × 9 × 9."),
   box("Full sphere factor: 729 × 4 ÷ 3 = ", 972, "\\(\\frac{4}{3}\\) × 729."),
   box("Halve it for a hemisphere: 972 ÷ 2 = ", 486, "Half a sphere."),
   box("Multiply by π: 486 × π = ", 1526.8, "π button, 1 d.p.", done="So V = 1526.8 cm³.", phase="substitute"),
   box("Check in one go: \\(\\frac{2}{3}\\) × π × 729 rounds to ", 1526.8, "All together.", done="Still 1526.8 cm³.", phase="substitute"),
 ]})

# S6 cone V=150pi r5 h=18
silver.append({
 "display": cone("r = 5 cm", "h = ?", None, "A cone of radius 5 cm and unknown height, volume 150 pi") + live["problem_bank"]["silver"][6]["display"],
 "solutions": [18], "calculator": False, "input_type": "single_value",
 "hint": "Volume of a cone is ⅓πr²h. Work in multiples of π.",
 "misconceptions": [mc("dropped_third", 6,
   "Keep the ⅓: 150 = ⅓ × 25 × h gives 25h = 450 and h = 18 cm. Dropping the third gives 6.")],
 "guided_steps": [
   say("Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). Work in multiples of π to keep it exact."),
   box("The r² part: 5² = ", 25, "5 × 5."),
   box("So ⅓ × 25 × h = 150. Multiply both sides by 3: 150 × 3 = ", 450, "Clear the third.", done="So 25h = 450.", phase="substitute"),
   box("Divide by 25: 450 ÷ 25 = ", 18, "450 shared into 25s.", done="So the height is 18 cm.", phase="substitute"),
   box("Check: ⅓ × 25 × 18 = ", 150, "In π units.", done="150π, matching the given volume, so h = 18 cm.", phase="substitute"),
 ]})


# ================= GOLD =================
gold = []

# G0 cone r3 slant5 total SA=75.4
gold.append({
 "display": cone("r = 3 cm", None, "l = 5 cm", "A cone of radius 3 cm and slant height 5 cm") + live["problem_bank"]["gold"][0]["display"],
 "solutions": [75.4], "calculator": True, "input_type": "single_value",
 "hint": "Total surface area of a cone is π r l (curved) plus π r² (base).",
 "misconceptions": [mc("no_base", 47.1,
   "Total surface area includes the base π r² as well as the curved part π r l: 15π + 9π = 24π = 75.4 cm². The curved surface alone is 47.1.")],
 "guided_steps": [
   say("Total surface area of a cone is the curved part \\(\\pi r l\\) plus the base \\(\\pi r^2\\). Find each in π units."),
   box("Curved part factor: r × l = 3 × 5 = ", 15, "π r l = 15π."),
   box("Base factor: r² = 3² = ", 9, "π r² = 9π."),
   box("Add them: 15 + 9 = ", 24, "In π units.", done="So the total is 24π.", phase="substitute"),
   box("Multiply by π: 24 × π = ", 75.4, "π button, 1 d.p.", done="So total SA = 75.4 cm².", phase="substitute"),
   box("Check: 15π + 9π = 24π rounds to ", 75.4, "All together.", done="Still 75.4 cm².", phase="substitute"),
 ]})

# G1 frustum V=326.7
gold.append({
 "display": frustum("A frustum from a large cone radius 6 height 9 with a small cone radius 2 height 3 removed") + live["problem_bank"]["gold"][1]["display"],
 "solutions": [326.7], "calculator": True, "input_type": "single_value",
 "hint": "Big cone volume minus small cone volume. Work in multiples of π.",
 "misconceptions": [mc("added", 351.9,
   "The tip is removed, so subtract: 108π − 4π = 104π = 326.7 cm³. Adding the cones gives 351.9.")],
 "guided_steps": [
   say("The frustum is the big cone with the small tip cone removed. Find each cone in π units, then subtract."),
   box("Big cone factor: ⅓ × 6² × 9 = ⅓ × 36 × 9 = ", 108, "That is 108π."),
   box("Small cone factor: ⅓ × 2² × 3 = ⅓ × 4 × 3 = ", 4, "That is 4π."),
   box("Subtract: 108 − 4 = ", 104, "In π units.", done="So the frustum is 104π.", phase="substitute"),
   box("Multiply by π: 104 × π = ", 326.7, "π button, 1 d.p.", done="So V = 326.7 cm³.", phase="substitute"),
   box("Check: 108π − 4π = 104π rounds to ", 326.7, "All together.", done="Still 326.7 cm³.", phase="substitute"),
 ]})

# G2 sphere in cylinder gap V=261.8
gold.append({
 "display": sphere_in_cyl("r = 5 cm", "A sphere of radius 5 cm fitting exactly inside a cylinder") + live["problem_bank"]["gold"][2]["display"],
 "solutions": [261.8], "calculator": True, "input_type": "single_value",
 "hint": "The cylinder has radius 5 and height 10. Empty space = cylinder − sphere.",
 "misconceptions": [mc("forgot_subtract", 785.4,
   "That is the whole cylinder. The empty space is what is left after the sphere is removed: 250π − \\(\\frac{500\\pi}{3}\\) = \\(\\frac{250\\pi}{3}\\) = 261.8 cm³.")],
 "guided_steps": [
   say("The sphere touches the cylinder all round, so the cylinder has radius 5 and height 10 (the diameter). Empty space = cylinder − sphere."),
   box("Cylinder volume: π × 5² × 10 = 250π = ", 785.4, "250 × π, 1 d.p."),
   box("Sphere volume: \\(\\frac{4}{3}\\) × π × 5³ = \\(\\frac{500\\pi}{3}\\) = ", 523.6, "500 ÷ 3 × π, 1 d.p."),
   box("Subtract: 785.4 − 523.6 = ", 261.8, "Cylinder minus sphere.", done="So the empty space is 261.8 cm³.", phase="substitute"),
   box("Check: the gap is exactly a third of the cylinder, \\(\\frac{250\\pi}{3}\\) rounds to ", 261.8, "One third of 785.4.", done="Still 261.8 cm³.", phase="substitute"),
 ]})

# G3 cylinder+hemisphere V=636.7
gold.append({
 "display": cyl_hemi("r = 4 cm", "h = 10 cm", "A cylinder radius 4 cm height 10 cm with a hemisphere radius 4 cm on top") + live["problem_bank"]["gold"][3]["display"],
 "solutions": [636.7], "calculator": True, "input_type": "single_value",
 "hint": "Total = cylinder volume + hemisphere volume.",
 "misconceptions": [mc("full_sphere", 770.7,
   "The top is a HALF sphere: use ½ × \\(\\frac{4}{3}\\pi r^3\\) = \\(\\frac{128\\pi}{3}\\) = 134.0 cm³, giving a total of 636.7 cm³. A full sphere on top gives 770.7.")],
 "guided_steps": [
   say("Total volume = cylinder + hemisphere on top. Work each out as a decimal, then add."),
   box("Cylinder volume: π × 4² × 10 = 160π = ", 502.7, "160 × π, 1 d.p."),
   box("Hemisphere volume: ½ × \\(\\frac{4}{3}\\) × π × 4³ = \\(\\frac{128\\pi}{3}\\) = ", 134.0, "128 ÷ 3 × π, 1 d.p."),
   box("Add them: 502.7 + 134.0 = ", 636.7, "Cylinder plus hemisphere.", done="So V = 636.7 cm³.", phase="substitute"),
   box("Check in π units: 160 + \\(\\frac{128}{3}\\) = \\(\\frac{608}{3}\\), and \\(\\frac{608\\pi}{3}\\) rounds to ", 636.7, "All together.", done="Still 636.7 cm³.", phase="substitute"),
 ]})

# G4 sphere SA=100pi find r=5
gold.append({
 "display": sphere("r = ?", "SA = 100π", "A sphere with surface area 100 pi, radius unknown") + live["problem_bank"]["gold"][4]["display"],
 "solutions": [5], "calculator": False, "input_type": "single_value",
 "hint": "Surface area of a sphere is 4πr². Set it equal to 100π; the π cancels.",
 "misconceptions": [
   mc("forgot_root", 25, "25 is r², not r. Take the square root: r = √25 = 5 cm."),
   mc("forgot_four", 10, "Do not drop the 4: 100π = 4πr² gives r² = 25 and r = 5 cm, not r² = 100."),
 ],
 "guided_steps": [
   say("Surface area of a sphere is \\(4\\pi r^2\\). Set it equal to 100π and the π cancels."),
   box("Divide both sides by π: 100π ÷ π = ", 100, "The π cancels, leaving 100 = 4r²."),
   box("Divide by 4: 100 ÷ 4 = ", 25, "So r² = 25.", done="So r² = 25.", phase="substitute"),
   box("Square root: √25 = ", 5, "What squares to 25?", done="So the radius is 5 cm.", phase="substitute"),
   box("Check: 4 × π × 5² in π units is 4 × 25 = ", 100, "Rebuild the surface area.", done="100π, matching, so r = 5 cm.", phase="substitute"),
 ]})


problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Volume and surface area of cuboids, cubes, prisms and cylinders using the basic formulas.",
  "silver_description": "Cones, spheres, pyramids and hemispheres, plus reverse problems that find a missing length.",
  "gold_description": "Composite solids, joined or with a piece removed, and rearranging a formula to find a length.",
}

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: volume and surface area of basic solids",
  "steps": [
    "<strong>Cuboid:</strong> volume = length × width × height. <strong>Cube:</strong> volume = side³.",
    "<strong>Prism:</strong> volume = cross-section area × length. <strong>Cylinder:</strong> volume = π r² h.",
    "<strong>Surface area:</strong> add the area of every face. A cuboid is 2(lw + lh + wh); a cube is 6 × side².",
  ],
  "example": {
    "question": "Find the volume of a cuboid 4 cm × 3 cm × 5 cm.",
    "steps": [
      {"label": "Formula", "content": "V = l × w × h"},
      {"label": "Base", "content": "4 × 3 = 12"},
      {"label": "Multiply", "content": "12 × 5 = 60"},
      {"label": "Check", "content": "5 × 4 × 3 = 60 ✓"},
      {"label": "Answer", "content": "V = 60 cm³", "isAnswer": True, "is_answer": True},
    ],
  },
 },
 "silver": {
  "title": "Silver: cones, spheres, pyramids and reverse problems",
  "steps": [
    "<strong>Cone:</strong> V = ⅓ π r² h. <strong>Sphere:</strong> V = \\(\\frac{4}{3}\\) π r³, SA = 4 π r². <strong>Pyramid:</strong> V = ⅓ × base area × h.",
    "A <strong>hemisphere</strong> is half a sphere, so halve the sphere volume.",
    "<strong>Reverse:</strong> to find a missing length, put the numbers in and rearrange. Working in multiples of π keeps it exact.",
  ],
  "example": {
    "question": "A cone has radius 3 cm and height 4 cm. Find the volume to 1 d.p.",
    "steps": [
      {"label": "Formula", "content": "V = ⅓ π r² h"},
      {"label": "Substitute", "content": "⅓ × π × 9 × 4 = 12π"},
      {"label": "Evaluate", "content": "12π = 37.7"},
      {"label": "Check", "content": "⅓ × π × 3² × 4 = 37.7 ✓"},
      {"label": "Answer", "content": "V = 37.7 cm³", "isAnswer": True, "is_answer": True},
    ],
  },
 },
 "gold": {
  "title": "Gold: composite solids and rearranging formulae",
  "steps": [
    "<strong>Composite solid:</strong> split it into basic shapes, find each part, then add (joined) or subtract (a piece removed).",
    "Keep each part in multiples of π until the final line, then round once.",
    "<strong>Rearrange:</strong> to find a length from a given volume or area, substitute the known values and solve, cancelling π where you can.",
  ],
  "example": {
    "question": "A hemisphere has radius 3 cm. Find the volume to 1 d.p.",
    "steps": [
      {"label": "Formula", "content": "V = ½ × \\(\\frac{4}{3}\\) π r³"},
      {"label": "Substitute", "content": "½ × \\(\\frac{4}{3}\\) × π × 27 = 18π"},
      {"label": "Evaluate", "content": "18π = 56.5"},
      {"label": "Check", "content": "\\(\\frac{2}{3}\\) × π × 27 = 56.5 ✓"},
      {"label": "Answer", "content": "V = 56.5 cm³", "isAnswer": True, "is_answer": True},
    ],
  },
 },
}

# ---------- guided ----------
opener = {
 "display": cube_grid() + "A shoebox is being filled with 1 cm sugar cubes. The bottom of the box holds a layer 3 cubes long and 2 cubes deep, and the box is 2 layers tall.",
 "steps": [
   box("The bottom layer is 3 cubes long and 2 cubes deep. How many cubes in one layer? 3 × 2 = ", 6, "Count one flat layer."),
   {"say": "The box is 2 layers tall, so stack that layer up."},
   box("Total cubes: 6 × 2 = ", 12, "Two layers of six."),
   {"say": "<strong>You just found a volume.</strong> Counting the cubes that fill a shape IS its volume, and the shortcut is length × width × height = 3 × 2 × 2 = 12 cm³. Every formula today (cylinders, cones, spheres) is just a cleverer way of counting the space inside."},
 ],
}

teach = {
 "bronze": {
   "display": cuboid("5 cm", "4 cm", "2 cm", "A cuboid 5 cm by 4 cm by 2 cm") + "Find the volume of a cuboid 5 cm × 4 cm × 2 cm.",
   "steps": [
     {"say": "Volume of a cuboid is length × width × height. Let us fill one in."},
     box("Multiply length by width: 5 × 4 = ", 20, "The base layer."),
     box("Now multiply by the height: 20 × 2 = ", 40, "Stack the layers.", done="So V = 40 cm³."),
     box("Check another order: 4 × 2 × 5 = ", 40, "Any order, same volume."),
     box("How many 1 cm cubes fill it? ", 40, "The volume in cubes.", done="40 cubes. That was the whole point: multiply all three lengths."),
   ],
 },
 "silver": {
   "display": cone("r = 6 cm", "h = 6 cm", None, "A cone of radius 6 cm and height 6 cm") + "A cone has radius 6 cm and height 6 cm. Find the volume to 1 d.p.",
   "steps": [
     {"say": "Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). The new move is that ⅓."},
     box("Square the radius: 6² = ", 36, "6 × 6."),
     box("Multiply by the height: 36 × 6 = ", 216, "This is r²h."),
     box("Take one third: 216 ÷ 3 = ", 72, "The cone factor.", done="That is 72π."),
     box("Multiply by π: 72 × π = ", 226.2, "π button, 1 d.p.", done="V = 226.2 cm³. The new move: the ⅓ a cone always needs."),
   ],
 },
 "gold": {
   "display": cyl_hemi("r = 3 cm", "h = 8 cm", "A cylinder radius 3 cm height 8 cm with a cone radius 3 cm height 4 cm on top") + "A solid is a cylinder (r = 3 cm, h = 8 cm) with a cone (r = 3 cm, h = 4 cm) on top. Find the total volume to 1 d.p.",
   "steps": [
     {"say": "A composite solid is two shapes joined. Find each volume, then combine. The new move: split into parts."},
     box("Cylinder: π × 3² × 8 = 72π = ", 226.2, "72 × π, 1 d.p."),
     box("Cone: ⅓ × π × 3² × 4 = 12π = ", 37.7, "12 × π, 1 d.p."),
     box("Add them: 226.2 + 37.7 = ", 263.9, "Cylinder plus cone.", done="Total 263.9 cm³."),
     box("Check in π units: 72 + 12 = ", 84, "84π altogether.", done="84π = 263.9 cm³. The new move: split, then add."),
   ],
 },
}

# ---------- assemble ----------
pd = {
  "method_card": live["method_card"],
  "topic_links": live["topic_links"],
  "problem_bank": problem_bank,
  "related_videos": live["related_videos"],
  "worked_examples": live["worked_examples"],
  "tier_guides": tier_guides,
  "guided": {"opener": opener, "teach": teach},
}

json.dump(pd, io.open("lesson_maths-aqa_geometry-L03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_maths-aqa_geometry-L03.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
