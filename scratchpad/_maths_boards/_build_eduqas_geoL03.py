# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for
maths-eduqas geometry-L03 (Volume & Surface Area).
Preserves topic_links, related_videos, worked_examples (em-dash fixed).
Converts MC bank -> single_value with figures, guided_steps, expects."""
import json, io

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'
HEAD = '<svg viewBox="0 0 240 160" role="img" aria-label="{a}" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'

def cuboid(a, bottom, left, right):
    s = HEAD.format(a=a)
    s += '<polygon points="50,70 150,70 188,44 88,44" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
    s += '<polygon points="150,70 188,44 188,104 150,130" fill="#60a5fa" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
    s += '<rect x="50" y="70" width="100" height="60" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<text x="100" y="146" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % bottom
    if left is not None:
        s += '<text x="42" y="104" font-size="11" text-anchor="end" font-weight="600" fill="currentColor">%s</text>' % left
    if right is not None:
        s += '<text x="174" y="52" font-size="11" text-anchor="start" font-weight="600" fill="currentColor">%s</text>' % right
    return s + '</svg>' + CAP + ' '

def cube(a, bottom, top=None):
    s = HEAD.format(a=a)
    s += '<polygon points="50,70 150,70 188,44 88,44" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
    s += '<polygon points="150,70 188,44 188,104 150,130" fill="#60a5fa" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
    s += '<rect x="50" y="70" width="100" height="60" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    if top is not None:
        s += '<text x="100" y="30" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % top
    s += '<text x="100" y="146" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % bottom
    return s + '</svg>' + CAP + ' '

def tri_prism(a, arealab, lenlab):
    s = HEAD.format(a=a)
    s += '<polygon points="40,124 104,124 72,60" fill="#60a5fa" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6"/>'
    s += '<polygon points="110,106 174,106 142,42" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="40" y1="124" x2="110" y2="106" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="104" y1="124" x2="174" y2="106" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="72" y1="60" x2="142" y2="42" stroke="currentColor" stroke-width="1.4"/>'
    s += '<text x="71" y="112" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % arealab
    s += '<text x="120" y="74" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % lenlab
    return s + '</svg>' + CAP + ' '

def cylinder(a, rlab, hlab, rdashed=True):
    s = HEAD.format(a=a)
    s += '<line x1="76" y1="44" x2="76" y2="120" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="164" y1="44" x2="164" y2="120" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="120" rx="44" ry="13" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="44" rx="44" ry="13" fill="#60a5fa" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>'
    s += '<circle cx="120" cy="44" r="2.2" fill="currentColor"/>'
    s += '<line x1="120" y1="44" x2="164" y2="44" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2"/>'
    s += '<text x="142" y="38" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % rlab
    s += '<line x1="176" y1="44" x2="176" y2="120" stroke="currentColor" stroke-width="1"/>'
    s += '<line x1="172" y1="44" x2="180" y2="44" stroke="currentColor" stroke-width="1"/>'
    s += '<line x1="172" y1="120" x2="180" y2="120" stroke="currentColor" stroke-width="1"/>'
    s += '<text x="184" y="86" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">%s</text>' % hlab
    return s + '</svg>' + CAP + ' '

def cone(a, rlab, hlab):
    s = HEAD.format(a=a)
    s += '<path d="M120,26 L74,124 L166,124 Z" fill="#60a5fa" fill-opacity="0.14" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="124" rx="46" ry="13" fill="#60a5fa" fill-opacity="0.2" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="120" y1="26" x2="120" y2="124" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += '<path d="M120,116 L128,116 L128,124" fill="none" stroke="currentColor" stroke-width="1"/>'
    s += '<text x="128" y="82" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">%s</text>' % hlab
    s += '<line x1="120" y1="124" x2="166" y2="124" stroke="currentColor" stroke-width="1.3"/>'
    s += '<circle cx="120" cy="124" r="2.2" fill="currentColor"/>'
    s += '<text x="143" y="138" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % rlab
    return s + '</svg>' + CAP + ' '

def sphere(a, rlab, toplab=None):
    s = HEAD.format(a=a)
    s += '<circle cx="120" cy="86" r="52" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="86" rx="52" ry="15" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += '<circle cx="120" cy="86" r="2.4" fill="currentColor"/>'
    s += '<line x1="120" y1="86" x2="172" y2="86" stroke="currentColor" stroke-width="1.3"/>'
    s += '<text x="146" y="80" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % rlab
    if toplab is not None:
        s += '<text x="120" y="24" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % toplab
    return s + '</svg>' + CAP + ' '

def hemisphere(a, rlab):
    s = HEAD.format(a=a)
    s += '<path d="M64,102 A56 56 0 0 1 176,102" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="102" rx="56" ry="14" fill="#60a5fa" fill-opacity="0.2" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="120" y1="102" x2="176" y2="102" stroke="currentColor" stroke-width="1.3"/>'
    s += '<circle cx="120" cy="102" r="2.2" fill="currentColor"/>'
    s += '<text x="146" y="96" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % rlab
    return s + '</svg>' + CAP + ' '

def pyramid(a, baselab, hlab):
    s = HEAD.format(a=a)
    s += '<polygon points="60,122 150,122 188,98 98,98" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="124" y1="34" x2="60" y2="122" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="124" y1="34" x2="150" y2="122" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="124" y1="34" x2="188" y2="98" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="124" y1="34" x2="98" y2="98" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="124" y1="34" x2="124" y2="110" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += '<circle cx="124" cy="110" r="2" fill="currentColor"/>'
    s += '<text x="103" y="136" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % baselab
    s += '<text x="132" y="78" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">%s</text>' % hlab
    return s + '</svg>' + CAP + ' '

def trap_prism(a):
    # trapezium cross-section: bottom 9, top 5, height 4; length 12
    s = HEAD.format(a=a)
    # front trapezium
    s += '<polygon points="46,124 118,124 104,72 60,72" fill="#60a5fa" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6"/>'
    # back trapezium (offset +40,-16)
    s += '<polygon points="86,108 158,108 144,56 100,56" fill="none" stroke="currentColor" stroke-width="1.3"/>'
    # connectors
    s += '<line x1="46" y1="124" x2="86" y2="108" stroke="currentColor" stroke-width="1.3"/>'
    s += '<line x1="118" y1="124" x2="158" y2="108" stroke="currentColor" stroke-width="1.3"/>'
    s += '<line x1="104" y1="72" x2="144" y2="56" stroke="currentColor" stroke-width="1.3"/>'
    s += '<line x1="60" y1="72" x2="100" y2="56" stroke="currentColor" stroke-width="1.3"/>'
    s += '<text x="82" y="138" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">9 cm</text>'
    s += '<text x="82" y="66" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">5 cm</text>'
    s += '<text x="40" y="102" font-size="10" text-anchor="end" font-weight="600" fill="currentColor">4 cm</text>'
    s += '<text x="150" y="86" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">length 12 cm</text>'
    return s + '</svg>' + CAP + ' '

def cone_vs_cyl(a):
    # cylinder left (r5,h12), cone right (r5,h12)
    s = HEAD.format(a=a)
    # cylinder
    s += '<line x1="34" y1="40" x2="34" y2="122" stroke="currentColor" stroke-width="1.5"/>'
    s += '<line x1="96" y1="40" x2="96" y2="122" stroke="currentColor" stroke-width="1.5"/>'
    s += '<ellipse cx="65" cy="122" rx="31" ry="9" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>'
    s += '<ellipse cx="65" cy="40" rx="31" ry="9" fill="#60a5fa" fill-opacity="0.28" stroke="currentColor" stroke-width="1.5"/>'
    s += '<text x="65" y="150" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">cylinder</text>'
    # cone
    s += '<path d="M175,36 L146,122 L204,122 Z" fill="#60a5fa" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>'
    s += '<ellipse cx="175" cy="122" rx="29" ry="9" fill="#60a5fa" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>'
    s += '<text x="175" y="150" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">cone</text>'
    s += '<text x="120" y="76" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">r = 5, h = 12</text>'
    return s + '</svg>' + CAP + ' '

def cyl_hemi(a, rlab, hlab):
    # cylinder r,h with hemisphere on top
    s = HEAD.format(a=a)
    s += '<line x1="78" y1="66" x2="78" y2="132" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="162" y1="66" x2="162" y2="132" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="132" rx="42" ry="12" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
    s += '<path d="M78,66 A42 42 0 0 1 162,66" fill="#60a5fa" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="66" rx="42" ry="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>'
    s += '<circle cx="120" cy="66" r="2.2" fill="currentColor"/>'
    s += '<line x1="120" y1="66" x2="162" y2="66" stroke="currentColor" stroke-width="1.2"/>'
    s += '<text x="140" y="60" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % rlab
    s += '<line x1="174" y1="66" x2="174" y2="132" stroke="currentColor" stroke-width="1"/>'
    s += '<text x="182" y="102" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">%s</text>' % hlab
    return s + '</svg>' + CAP + ' '

def cyl_cone(a, rlab, hlab):
    # cylinder body with a cone on top (both same radius)
    s = HEAD.format(a=a)
    s += '<line x1="78" y1="66" x2="78" y2="132" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="162" y1="66" x2="162" y2="132" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="132" rx="42" ry="12" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
    s += '<polygon points="120,26 78,66 162,66" fill="#60a5fa" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
    s += '<ellipse cx="120" cy="66" rx="42" ry="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>'
    s += '<circle cx="120" cy="66" r="2.2" fill="currentColor"/>'
    s += '<line x1="120" y1="66" x2="162" y2="66" stroke="currentColor" stroke-width="1.2"/>'
    s += '<text x="140" y="60" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>' % rlab
    s += '<line x1="174" y1="66" x2="174" y2="132" stroke="currentColor" stroke-width="1"/>'
    s += '<text x="182" y="102" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">%s</text>' % hlab
    return s + '</svg>' + CAP + ' '

def opener_box(a):
    # box 4 long (front width) x 3 tall (front height) grid, depth 2
    s = HEAD.format(a=a)
    # top face (iso)
    s += '<polygon points="50,48 170,48 200,26 80,26" fill="#60a5fa" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>'
    # right face
    s += '<polygon points="170,48 200,26 200,116 170,138" fill="#60a5fa" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>'
    # front face
    s += '<rect x="50" y="48" width="120" height="90" fill="#60a5fa" fill-opacity="0.14" stroke="currentColor" stroke-width="1.6"/>'
    # front vertical grid lines (4 columns -> 3 internal at 30px)
    for x in (80, 110, 140):
        s += '<line x1="%d" y1="48" x2="%d" y2="138" stroke="currentColor" stroke-width="1"/>' % (x, x)
    # front horizontal grid lines (3 rows -> 2 internal at 30px)
    for y in (78, 108):
        s += '<line x1="50" y1="%d" x2="170" y2="%d" stroke="currentColor" stroke-width="1"/>' % (y, y)
    s += '<text x="110" y="152" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">4 cm</text>'
    s += '<text x="42" y="96" font-size="10" text-anchor="end" font-weight="600" fill="currentColor">3 cm</text>'
    s += '<text x="188" y="40" font-size="10" text-anchor="start" font-weight="600" fill="currentColor">2 cm</text>'
    s += '<text x="110" y="20" font-size="9" text-anchor="middle" font-weight="600" fill="currentColor">each square = 1 cm</text>'
    return s + '</svg>' + CAP + ' '


def box(pre, answer, hint, post="", done=None, say=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if say: d["say"] = say
    if phase: d["phase"] = phase
    return d

def say(t): return {"say": t}

def mis(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

def prob(display, sol, calc, hint, misc, steps):
    return {"display": display, "solutions": [sol], "calculator": calc,
            "input_type": "single_value", "hint": hint,
            "misconceptions": misc, "guided_steps": steps}

pd = {}

# ---------- preserved fields ----------
pd["method_card"] = {
    "steps": [
        "Identify the 3D shape and pick the right formula",
        "For a prism, find the cross-section area first, then multiply by the length",
        "Substitute carefully: watch radius vs diameter, and the ⅓ for cones and pyramids",
        "Calculate and give units (cm³ for volume, cm² for surface area)"
    ],
    "title": "Volume & Surface Area",
    "content": "<p><strong>Prism:</strong> V = cross-section area × length. <strong>Cuboid:</strong> V = \\(lwh\\), SA = \\(2(lw + lh + wh)\\). <strong>Cylinder:</strong> V = \\(\\pi r^2 h\\), SA = \\(2\\pi r^2 + 2\\pi rh\\).</p><p><strong>Cone:</strong> V = \\(\\frac{1}{3}\\pi r^2 h\\). <strong>Pyramid:</strong> V = \\(\\frac{1}{3}\\times\\) base area \\(\\times h\\). <strong>Sphere:</strong> V = \\(\\frac{4}{3}\\pi r^3\\), SA = \\(4\\pi r^2\\).</p>",
    "example": "<p><strong>Volume of a cylinder: radius 5 cm, height 12 cm.</strong></p><p>V = \\(\\pi \\times 5^2 \\times 12 = 300\\pi \\approx 942.5\\) cm³</p>"
}
pd["topic_links"] = {"prerequisites": [{"slug": "geometry/2", "title": "Area & Perimeter"}]}
pd["related_videos"] = []
pd["worked_examples"] = [
    {"steps": [
        {"label": "Step 1: Formula", "content": "<p>V = l × w × h</p>"},
        {"label": "Step 2: Calculate", "content": "<p>V = 8 × 5 × 3 = 120 cm³</p>"},
        {"label": "Answer", "content": "<p><strong>120 cm³</strong></p>", "isAnswer": True, "is_answer": True}],
     "question": "Find the volume of a cuboid: 8 cm by 5 cm by 3 cm.", "difficulty": "Bronze"},
    {"steps": [
        {"label": "Step 1: Formula", "content": "<p>V = \\(\\frac{1}{3}\\pi r^2 h\\)</p>"},
        {"label": "Step 2: Substitute", "content": "<p>\\(\\frac{1}{3} \\times \\pi \\times 36 \\times 10 = 120\\pi = 376.99...\\)</p>"},
        {"label": "Answer", "content": "<p><strong>377.0 cm³</strong></p>", "isAnswer": True, "is_answer": True}],
     "question": "A cone has radius 6 cm and height 10 cm. Find the volume. (1 d.p.)", "difficulty": "Silver"},
    {"steps": [
        {"label": "Step 1: Formula", "content": "<p>SA = \\(4\\pi r^2\\)</p>"},
        {"label": "Step 2: Substitute", "content": "<p>\\(4 \\times \\pi \\times 16 = 64\\pi = 201.06...\\)</p>"},
        {"label": "Answer", "content": "<p><strong>201.1 cm²</strong></p>", "isAnswer": True, "is_answer": True}],
     "question": "Find the surface area of a sphere with radius 4 cm. (1 d.p.)", "difficulty": "Gold"}
]

# ---------- BRONZE ----------
bronze = []
# b0 cuboid 6x4x3
bronze.append(prob(
    cuboid("A cuboid 6 cm by 4 cm by 3 cm", "6 cm", "3 cm", "4 cm") + "Find the volume of a cuboid with length 6 cm, width 4 cm and height 3 cm.",
    72, False, "Volume of a cuboid is length × width × height.",
    [mis("surface_area", 108, "108 cm² is the surface area, 2(lw + lh + wh). Volume is 6 × 4 × 3 = 72 cm³."),
     mis("added", 13, "Multiply the three lengths, do not add: 6 × 4 × 3 = 72 cm³.")],
    [say("Volume of a cuboid is length × width × height. Multiply all three."),
     box("Multiply length by width: 6 × 4 = ", 24, "Six fours."),
     box("Now multiply by the height: 24 × 3 = ", 72, "24 threes.", done="That is the volume, 72 cm³.", phase="substitute"),
     box("Check another order: 4 × 3 × 6 = ", 72, "Same three numbers, any order.", done="Still 72, so V = 72 cm³.", phase="substitute")]))
# b1 cube side 5
bronze.append(prob(
    cube("A cube of side 5 cm", "5 cm") + "Find the volume of a cube with side length 5 cm.",
    125, False, "Volume of a cube is side × side × side.",
    [mis("squared", 25, "Cube the side, do not square it: 5³ = 5 × 5 × 5 = 125 cm³."),
     mis("surface_area", 150, "150 cm² is the surface area (6 × 5²). Volume = 5³ = 125 cm³.")],
    [say("Volume of a cube is side × side × side."),
     box("Square the side: 5 × 5 = ", 25, "Five fives."),
     box("Multiply by the side again: 25 × 5 = ", 125, "25 fives.", done="So V = 125 cm³.", phase="substitute"),
     box("Compare: the surface area would be 6 × 25 = ", 150, "Six faces of 5 × 5.", done="150 is the surface area; the volume is 125 cm³.", phase="substitute")]))
# b2 triangular prism area 20 length 9
bronze.append(prob(
    tri_prism("A triangular prism, cross-section area 20 cm squared, length 9 cm", "area 20 cm²", "length 9 cm") + "A triangular prism has cross-section area 20 cm² and length 9 cm. Find its volume.",
    180, False, "Volume of any prism is the cross-section area times the length.",
    [mis("added", 29, "Multiply, do not add: volume of a prism = cross-section area × length = 20 × 9 = 180 cm³."),
     mis("halved", 90, "The cross-section area is already given as 20. Do not halve it again: 20 × 9 = 180 cm³.")],
    [say("Volume of any prism is the cross-section area times the length."),
     box("Write the cross-section area: ", 20, "Given as 20 cm²."),
     box("Multiply by the length: 20 × 9 = ", 180, "20 nines.", done="So V = 180 cm³.", phase="substitute"),
     box("Check: 180 ÷ 9 = ", 20, "Divide back by the length.", done="Back to the 20 cm² cross-section, so V = 180 cm³.", phase="substitute")]))
# b3 SA cube side 4
bronze.append(prob(
    cube("A cube of side 4 cm", "4 cm") + "Find the surface area of a cube with side length 4 cm.",
    96, False, "A cube has 6 identical square faces: find one, then times by 6.",
    [mis("volume", 64, "64 cm³ is the volume (4³). Surface area = 6 × 4² = 6 × 16 = 96 cm²."),
     mis("one_face", 16, "A cube has 6 faces, not one: SA = 6 × 4² = 96 cm².")],
    [say("A cube has 6 identical square faces. Find one face, then multiply by 6."),
     box("Area of one face: 4 × 4 = ", 16, "Side times side."),
     box("Six faces: 6 × 16 = ", 96, "Six lots of 16.", done="So SA = 96 cm².", phase="substitute"),
     box("Compare: the volume would be 4 × 4 × 4 = ", 64, "Side cubed.", done="64 is the volume; the surface area is 96 cm².", phase="substitute")]))
# b4 cuboid 10x5x2
bronze.append(prob(
    cuboid("A cuboid 10 cm by 5 cm by 2 cm", "10 cm", "2 cm", "5 cm") + "A cuboid is 10 cm by 5 cm by 2 cm. Find its volume.",
    100, False, "Volume of a cuboid is length × width × height.",
    [mis("added", 17, "Multiply, do not add: 10 × 5 × 2 = 100 cm³."),
     mis("surface_area", 160, "160 cm² is the surface area. Volume = 10 × 5 × 2 = 100 cm³.")],
    [say("Volume of a cuboid is length × width × height. Multiply all three."),
     box("Multiply length by width: 10 × 5 = ", 50, "Ten fives."),
     box("Now multiply by the height: 50 × 2 = ", 100, "Double it.", done="So V = 100 cm³.", phase="substitute"),
     box("Check another order: 5 × 2 × 10 = ", 100, "Same numbers, any order.", done="Still 100, so V = 100 cm³.", phase="substitute")]))
# b5 rectangular prism 6x3 length 15
bronze.append(prob(
    cuboid("A cuboid with cross-section 6 cm by 3 cm and length 15 cm", "15 cm", "3 cm", "6 cm") + "A prism has a rectangular cross-section 6 cm by 3 cm and is 15 cm long. Find its volume.",
    270, False, "Find the cross-section area (6 × 3) first, then multiply by the length.",
    [mis("forgot_length", 18, "That is just the cross-section area. Multiply by the length: 18 × 15 = 270 cm³."),
     mis("added", 24, "Multiply, do not add: (6 × 3) × 15 = 270 cm³.")],
    [say("Volume of a prism is the cross-section area times the length. The cross-section here is a 6 by 3 rectangle."),
     box("Cross-section area: 6 × 3 = ", 18, "Rectangle area."),
     box("Multiply by the length: 18 × 15 = ", 270, "18 fifteens.", done="So V = 270 cm³.", phase="substitute"),
     box("Check: 270 ÷ 15 = ", 18, "Divide back by the length.", done="Back to the 18 cm² cross-section, so V = 270 cm³.", phase="substitute")]))
# b6 cube volume 27 find side
bronze.append(prob(
    cube("A cube of volume 27 cm cubed with unknown side", "?", top="V = 27 cm³") + "A cube has volume 27 cm³. Find the side length.",
    3, False, "Cube root: find the number that, cubed, gives 27.",
    [mis("divided_by_3", 9, "Do not divide by 3. Find the cube root: 3³ = 27, so the side is 3 cm."),
     mis("halved", 13.5, "Do not divide by 2. Take the cube root: 3³ = 27, so the side is 3 cm.")],
    [say("Volume of a cube is side³, so we need the number whose cube is 27."),
     box("Try a side of 3. First 3 × 3 = ", 9, "Square it."),
     box("Now multiply by 3 again: 9 × 3 = ", 27, "Cube it.", done="27 matches the volume.", phase="substitute"),
     box("So the side length is ", 3, "The number we cubed.", done="Side = 3 cm.", phase="substitute")]))
# b7 litre conversion
bronze.append(prob(
    cube("A cube 10 cm on every side, holding 1 litre", "10 cm") + "How many cm³ are there in 1 litre?",
    1000, False, "1 litre fills a cube 10 cm on every side.",
    [mis("wrong_conversion", 100, "1 litre = 1000 cm³. A 10 cm cube holds 10 × 10 × 10 = 1000."),
     mis("too_many", 10000, "1 litre = 1000 cm³, not 10 000.")],
    [say("1 litre is exactly the space inside a cube 10 cm on every side. Count the cm³ cubes."),
     box("Base layer: 10 × 10 = ", 100, "One flat layer."),
     box("Stack 10 layers up: 100 × 10 = ", 1000, "Ten layers of 100.", done="So 1 litre = 1000 cm³.", phase="substitute"),
     box("Check: 10 × 10 × 10 = ", 1000, "Volume of the cube.", done="Still 1000 cm³, so 1 litre = 1000 cm³.", phase="substitute")]))

# ---------- SILVER ----------
silver = []
# s0 cylinder r4 h10
silver.append(prob(
    cylinder("A cylinder of radius 4 cm and height 10 cm", "r = 4 cm", "h = 10 cm") + "Find the volume of a cylinder with radius 4 cm and height 10 cm. Give your answer to 1 d.p.",
    502.7, True, "Volume of a cylinder is π r² h. Square the radius first.",
    [mis("forgot_square", 125.7, "The radius must be squared: V = π × 4² × 10 = 160π = 502.7 cm³, not π × 4 × 10.")],
    [say("Volume of a cylinder is \\(\\pi r^2 h\\). Square the radius first."),
     box("Square the radius: 4² = ", 16, "4 × 4."),
     box("Multiply by the height: 16 × 10 = ", 160, "This is r²h."),
     box("Multiply by π: 160 × π = ", 502.7, "Use the π button, round to 1 d.p.", done="So V = 502.7 cm³.", phase="substitute"),
     box("Check in one go: π × 4² × 10 rounds to ", 502.7, "Same calculation together.", done="Still 502.7 cm³.", phase="substitute")]))
# s1 cone r3 h7
silver.append(prob(
    cone("A cone of radius 3 cm and height 7 cm", "r = 3 cm", "h = 7 cm") + "Find the volume of a cone with radius 3 cm and height 7 cm. Give your answer to 1 d.p.",
    66.0, True, "Volume of a cone is one third of π r² h.",
    [mis("forgot_third", 197.9, "That is the full cylinder. A cone is one third: V = ⅓ × π × 3² × 7 = 21π = 66.0 cm³."),
     mis("forgot_square", 22.0, "Square the radius: V = ⅓ × π × 3² × 7 = 21π = 66.0 cm³.")],
    [say("Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). Build \\(\\pi r^2 h\\), then take a third."),
     box("Square the radius: 3² = ", 9, "3 × 3."),
     box("Multiply by the height: 9 × 7 = ", 63, "This is r²h."),
     box("Take one third: 63 ÷ 3 = ", 21, "The cone's ⅓ factor."),
     box("Multiply by π: 21 × π = ", 66.0, "π button, 1 d.p.", done="So V = 66.0 cm³.", phase="substitute"),
     box("Check in one go: ⅓ × π × 9 × 7 rounds to ", 66.0, "All together.", done="Still 66.0 cm³.", phase="substitute")]))
# s2 pyramid base 6 height 8
silver.append(prob(
    pyramid("A pyramid with square base of side 6 cm and height 8 cm", "6 cm", "h = 8 cm") + "A pyramid has a square base of side 6 cm and height 8 cm. Find its volume.",
    96, False, "Volume of a pyramid is one third of base area × height.",
    [mis("forgot_third", 288, "That is base area × height with no third. A pyramid is one third: V = ⅓ × 36 × 8 = 96 cm³."),
     mis("used_side", 16, "Use the base AREA (6 × 6 = 36), not the side: V = ⅓ × 36 × 8 = 96 cm³.")],
    [say("Volume of a pyramid is \\(\\frac{1}{3} \\times\\) base area \\(\\times h\\). Find the base area first."),
     box("Base area (square): 6 × 6 = ", 36, "Side squared."),
     box("Multiply by the height: 36 × 8 = ", 288, "base area × height."),
     box("Take one third: 288 ÷ 3 = ", 96, "The pyramid's ⅓ factor.", done="So V = 96 cm³.", phase="substitute"),
     box("Check: ⅓ × 36 × 8 = ", 96, "All together.", done="Still 96 cm³.", phase="substitute")]))
# s3 SA cylinder r3 h10
silver.append(prob(
    cylinder("A cylinder of radius 3 cm and height 10 cm", "r = 3 cm", "h = 10 cm") + "Find the total surface area of a cylinder with radius 3 cm and height 10 cm. Give your answer to 1 d.p.",
    245.0, True, "Surface area of a cylinder is 2πr² (two ends) + 2πrh (curved part).",
    [mis("only_curved", 188.5, "Add the two circular ends too: SA = 2πr² + 2πrh = 18π + 60π = 78π = 245.0 cm²."),
     mis("just_ends", 56.5, "That is only the two ends. Add the curved part 2πrh = 60π: total 78π = 245.0 cm².")],
    [say("Surface area of a cylinder is \\(2\\pi r^2 + 2\\pi r h\\). Work in multiples of π, then multiply once."),
     box("The two ends, 2πr², in π units: 2 × 3² = ", 18, "2 × 9 = 18π."),
     box("The curved part, 2πrh, in π units: 2 × 3 × 10 = ", 60, "2 × 30 = 60π."),
     box("Add them: 18 + 60 = ", 78, "In π units.", done="So the total is 78π.", phase="substitute"),
     box("Multiply by π: 78 × π = ", 245.0, "π button, 1 d.p.", done="So SA = 245.0 cm².", phase="substitute")]))
# s4 cylinder V=500pi r10 find h
silver.append(prob(
    cylinder("A cylinder of radius 10 cm and unknown height, volume 500 pi", "r = 10 cm", "h = ?") + "A cylinder has volume \\(500\\pi\\) cm³ and radius 10 cm. Find its height.",
    5, False, "Volume of a cylinder is πr²h. Work in multiples of π; the π cancels.",
    [mis("forgot_square", 50, "Square the radius: 500π = π × 10² × h = 100πh, so h = 500 ÷ 100 = 5 cm.")],
    [say("Volume of a cylinder is \\(\\pi r^2 h\\). Work in π units so the π cancels."),
     box("Square the radius: 10² = ", 100, "10 × 10."),
     box("So 100 × h = 500 (in π units). Divide: 500 ÷ 100 = ", 5, "Share 500 into 100s.", done="So the height is 5 cm.", phase="substitute"),
     box("Check: π × 10² × 5 in π units is 100 × 5 = ", 500, "Rebuild the volume.", done="500π, matching, so h = 5 cm.", phase="substitute")]))
# s5 hemisphere r6
silver.append(prob(
    hemisphere("A hemisphere of radius 6 cm", "r = 6 cm") + "Find the volume of a hemisphere with radius 6 cm. Give your answer to 1 d.p.",
    452.4, True, "A hemisphere is half a sphere: find the full sphere, then halve it.",
    [mis("full_sphere", 904.8, "A hemisphere is HALF a sphere: V = ½ × \\(\\frac{4}{3}\\) × π × 6³ = 144π = 452.4 cm³. The full sphere (904.8) is double."),
     mis("squared_radius", 75.4, "Cube the radius, do not square it: V = ½ × \\(\\frac{4}{3}\\) × π × 6³ = 144π = 452.4 cm³.")],
    [say("A hemisphere is half a sphere. Find the full sphere's volume, then halve it."),
     box("Cube the radius: 6³ = ", 216, "6 × 6 × 6."),
     box("Full sphere factor: 216 × 4 ÷ 3 = ", 288, "\\(\\frac{4}{3}\\) × 216."),
     box("Halve it for a hemisphere: 288 ÷ 2 = ", 144, "Half a sphere."),
     box("Multiply by π: 144 × π = ", 452.4, "π button, 1 d.p.", done="So V = 452.4 cm³.", phase="substitute"),
     box("Check in one go: \\(\\frac{2}{3}\\) × π × 216 rounds to ", 452.4, "All together.", done="Still 452.4 cm³.", phase="substitute")]))
# s6 trapezium prism
silver.append(prob(
    trap_prism("A prism with a trapezium cross-section, parallel sides 5 cm and 9 cm, height 4 cm, length 12 cm") + "A prism has a trapezium cross-section with parallel sides 5 cm and 9 cm and height 4 cm. The prism is 12 cm long. Find its volume.",
    336, False, "Find the trapezium area, ½(a + b)h, then multiply by the length.",
    [mis("forgot_length", 28, "That is just the cross-section area. Multiply by the length: 28 × 12 = 336 cm³."),
     mis("forgot_half", 672, "Trapezium area is ½(a + b)h. Do not drop the ½: area = 28, so V = 28 × 12 = 336 cm³.")],
    [say("Volume of a prism is cross-section area × length. First find the trapezium area, \\(\\frac{1}{2}(a+b)h\\)."),
     box("Add the parallel sides: 5 + 9 = ", 14, "a + b."),
     box("Trapezium area: ½ × 14 × 4 = ", 28, "Half of 14 × 4.", done="Cross-section area is 28 cm².", phase="substitute"),
     box("Multiply by the length: 28 × 12 = ", 336, "28 twelves.", done="So V = 336 cm³.", phase="substitute")]))

# ---------- GOLD ----------
gold = []
# g0 sphere r9
gold.append(prob(
    sphere("A sphere of radius 9 cm", "r = 9 cm") + "Find the volume of a sphere with radius 9 cm. Give your answer to the nearest whole number.",
    3054, True, "Volume of a sphere is four thirds of π r³. Cube the radius first.",
    [mis("forgot_four_thirds", 2290, "Include the four thirds: V = \\(\\frac{4}{3}\\) × π × 9³ = 972π = 3054 cm³, not just πr³."),
     mis("surface_area", 1018, "That is close to the surface area (4πr²). Volume = \\(\\frac{4}{3}\\)πr³ = 972π = 3054 cm³.")],
    [say("Volume of a sphere is \\(\\frac{4}{3}\\pi r^3\\). Cube the radius first."),
     box("Cube the radius: 9³ = ", 729, "9 × 9 × 9."),
     box("Multiply by 4: 729 × 4 = ", 2916, "Four lots."),
     box("Divide by 3: 2916 ÷ 3 = ", 972, "The four-thirds factor."),
     box("Multiply by π and round: 972 × π = ", 3054, "π button, nearest whole.", done="So V = 3054 cm³.", phase="substitute"),
     box("Check in one go: \\(\\frac{4}{3}\\) × π × 729 rounds to ", 3054, "All together.", done="Still 3054 cm³.", phase="substitute")]))
# g1 SA sphere r5
gold.append(prob(
    sphere("A sphere of radius 5 cm", "r = 5 cm") + "Find the surface area of a sphere with radius 5 cm. Give your answer to 1 d.p.",
    314.2, True, "Surface area of a sphere is 4 π r². Square the radius first.",
    [mis("volume", 523.6, "That is the volume. Surface area = 4πr² = 4 × π × 25 = 100π = 314.2 cm²."),
     mis("one_circle", 78.5, "Surface area is 4πr², not πr² (that is one circle): 100π = 314.2 cm².")],
    [say("Surface area of a sphere is \\(4\\pi r^2\\). Square the radius first."),
     box("Square the radius: 5² = ", 25, "5 × 5."),
     box("Multiply by 4: 25 × 4 = ", 100, "Four lots of r².", done="So it is 100π.", phase="substitute"),
     box("Multiply by π: 100 × π = ", 314.2, "π button, 1 d.p.", done="So SA = 314.2 cm².", phase="substitute")]))
# g2 sphere V=256/3 pi find r
gold.append(prob(
    sphere("A sphere with volume 256 over 3 pi and unknown radius", "r = ?", toplab="V = (256/3)π") + "A sphere has volume \\(\\frac{256}{3}\\pi\\) cm³. Find the radius.",
    4, False, "Volume of a sphere is \\(\\frac{4}{3}\\)πr³. Work in π units, then take the cube root.",
    [mis("forgot_cube_root", 64, "64 is r³, not r. Take the cube root: r = ∛64 = 4 cm."),
     mis("square_root", 8, "Cube root, not square root: r³ = 64, so r = ∛64 = 4 cm.")],
    [say("Volume of a sphere is \\(\\frac{4}{3}\\pi r^3\\). Set \\(\\frac{4}{3}r^3 = \\frac{256}{3}\\) in π units."),
     box("Multiply both sides by 3: \\(\\frac{256}{3}\\) × 3 gives 4r³ = ", 256, "Clear the thirds."),
     box("Divide by 4: 256 ÷ 4 = ", 64, "So r³ = 64.", done="So r³ = 64.", phase="substitute"),
     box("Cube root: ∛64 = ", 4, "What cubes to 64?", done="So the radius is 4 cm.", phase="substitute"),
     box("Check: \\(\\frac{4}{3}\\) × 4³ in π units is \\(\\frac{4}{3}\\) × 64 = ", 256/3 if False else 85.3333, "Rebuild the volume.", done="That is \\(\\frac{256}{3}\\)π, matching, so r = 4 cm.", phase="substitute")]))
# g3 cone vs cylinder r5 h12 difference
gold.append(prob(
    cone_vs_cyl("A cylinder and a cone, both radius 5 cm and height 12 cm") + "A cone and a cylinder both have radius 5 cm and height 12 cm. How much more volume does the cylinder have? Give your answer to 1 d.p.",
    628.3, True, "Cylinder volume minus cone volume. A cone is one third of the cylinder.",
    [mis("cone_only", 314.2, "That is the cone's volume. The extra = cylinder − cone = 300π − 100π = 200π = 628.3 cm³."),
     mis("whole_cylinder", 942.5, "That is the whole cylinder. The extra is cylinder − cone = 200π = 628.3 cm³.")],
    [say("The cone is \\(\\frac{1}{3}\\) of the cylinder, so the difference is \\(\\frac{2}{3}\\) of the cylinder. Work in π units."),
     box("Cylinder factor: r²h = 5² × 12 = ", 300, "That is 300π."),
     box("Cone is a third: 300 ÷ 3 = ", 100, "That is 100π."),
     box("Difference: 300 − 100 = ", 200, "In π units.", done="So the extra is 200π.", phase="substitute"),
     box("Multiply by π: 200 × π = ", 628.3, "π button, 1 d.p.", done="So the cylinder has 628.3 cm³ more.", phase="substitute")]))
# g4 cylinder r3 h10 + hemisphere r3
gold.append(prob(
    cyl_hemi("A cylinder radius 3 cm height 10 cm with a hemisphere radius 3 cm on top", "r = 3 cm", "h = 10 cm") + "A solid is a cylinder (radius 3 cm, height 10 cm) with a hemisphere (radius 3 cm) on top. Find the total volume. Give your answer to 1 d.p.",
    339.3, True, "Total = cylinder volume + hemisphere volume.",
    [mis("forgot_hemisphere", 282.7, "Add the hemisphere on top: cylinder 90π + hemisphere 18π = 108π = 339.3 cm³."),
     mis("full_sphere", 395.8, "The top is a HALF sphere, not a whole one: 90π + 18π = 108π = 339.3 cm³.")],
    [say("Total volume = cylinder + hemisphere on top. Work each in π units, then add."),
     box("Cylinder factor: r²h = 3² × 10 = ", 90, "That is 90π."),
     box("Hemisphere factor: \\(\\frac{2}{3}\\) × 3³ = \\(\\frac{2}{3}\\) × 27 = ", 18, "That is 18π."),
     box("Add them: 90 + 18 = ", 108, "In π units.", done="So the total is 108π.", phase="substitute"),
     box("Multiply by π: 108 × π = ", 339.3, "π button, 1 d.p.", done="So V = 339.3 cm³.", phase="substitute")]))

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Volume and surface area of cuboids, cubes and simple prisms.",
    "silver_description": "Cylinders, cones, pyramids and hemispheres, plus a reverse problem that finds a missing length.",
    "gold_description": "Spheres, composite solids and rearranging a formula to find a length."
}

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: volume and surface area of basic solids",
        "steps": [
            "<strong>Cuboid:</strong> volume = length × width × height. <strong>Cube:</strong> volume = side³.",
            "<strong>Prism:</strong> volume = cross-section area × length.",
            "<strong>Surface area:</strong> add the area of every face. A cube is 6 × side²; a cuboid is 2(lw + lh + wh)."
        ],
        "example": {
            "question": "Find the volume of a cuboid 4 cm × 3 cm × 5 cm.",
            "steps": [
                {"label": "Formula", "content": "V = l × w × h"},
                {"label": "Base", "content": "4 × 3 = 12"},
                {"label": "Multiply", "content": "12 × 5 = 60"},
                {"label": "Check", "content": "5 × 4 × 3 = 60 ✓"},
                {"label": "Answer", "content": "V = 60 cm³", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: cones, spheres, pyramids and reverse problems",
        "steps": [
            "<strong>Cylinder:</strong> V = π r² h. <strong>Cone:</strong> V = ⅓ π r² h. <strong>Pyramid:</strong> V = ⅓ × base area × h.",
            "A <strong>hemisphere</strong> is half a sphere, so halve the sphere volume \\(\\frac{4}{3}\\)πr³.",
            "<strong>Reverse:</strong> to find a missing length, substitute the numbers and rearrange. Working in multiples of π keeps it exact."
        ],
        "example": {
            "question": "A cone has radius 3 cm and height 4 cm. Find the volume to 1 d.p.",
            "steps": [
                {"label": "Formula", "content": "V = ⅓ π r² h"},
                {"label": "Substitute", "content": "⅓ × π × 9 × 4 = 12π"},
                {"label": "Evaluate", "content": "12π = 37.7"},
                {"label": "Check", "content": "⅓ × π × 3² × 4 = 37.7 ✓"},
                {"label": "Answer", "content": "V = 37.7 cm³", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: spheres, composite solids and rearranging formulae",
        "steps": [
            "<strong>Sphere:</strong> V = \\(\\frac{4}{3}\\)πr³, SA = 4πr². <strong>Composite:</strong> split into basic shapes, then add (joined) or subtract (a piece removed).",
            "Keep each part in multiples of π until the final line, then round once.",
            "<strong>Rearrange:</strong> to find a length from a given volume or area, substitute and solve, cancelling π where you can."
        ],
        "example": {
            "question": "A hemisphere has radius 3 cm. Find the volume to 1 d.p.",
            "steps": [
                {"label": "Formula", "content": "V = ½ × \\(\\frac{4}{3}\\) π r³"},
                {"label": "Substitute", "content": "½ × \\(\\frac{4}{3}\\) × π × 27 = 18π"},
                {"label": "Evaluate", "content": "18π = 56.5"},
                {"label": "Check", "content": "\\(\\frac{2}{3}\\) × π × 27 = 56.5 ✓"},
                {"label": "Answer", "content": "V = 56.5 cm³", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------- guided (opener + teach) ----------
pd["guided"] = {
    "opener": {
        "display": opener_box("A box drawn as a grid of 1 cm cubes, 4 wide, 3 tall and 2 deep") + "A tray is being packed with 1 cm sugar cubes. The front face fills up 4 cubes across and 3 cubes high, and the tray is 2 cubes deep.",
        "steps": [
            box("The front face is 4 across and 3 high. How many cubes fill it? 4 × 3 = ", 12, "Count the flat front."),
            say("The tray is 2 cubes deep, so there is a second identical layer behind the front."),
            box("Total cubes: 12 × 2 = ", 24, "Two layers of twelve."),
            say("<strong>You just found a volume.</strong> Counting the 1 cm cubes that fill a shape IS its volume, and the shortcut is length × width × height = 4 × 3 × 2 = 24 cm³. Every formula today (cylinders, cones, spheres) is just a cleverer way of counting the space inside.")
        ]
    },
    "teach": {
        "bronze": {
            "display": cuboid("A cuboid 7 cm by 3 cm by 2 cm", "7 cm", "2 cm", "3 cm") + "Find the volume of a cuboid 7 cm × 3 cm × 2 cm.",
            "steps": [
                say("Volume of a cuboid is length × width × height. Let us fill one in."),
                box("Multiply length by width: 7 × 3 = ", 21, "The base layer."),
                box("Now multiply by the height: 21 × 2 = ", 42, "Stack the layers.", done="So V = 42 cm³."),
                box("Check another order: 3 × 2 × 7 = ", 42, "Any order, same volume."),
                box("How many 1 cm cubes fill it? ", 42, "The volume in cubes.", done="42 cubes. That was the whole point: multiply all three lengths.")
            ]
        },
        "silver": {
            "display": cone("A cone of radius 6 cm and height 9 cm", "r = 6 cm", "h = 9 cm") + "A cone has radius 6 cm and height 9 cm. Find the volume to 1 d.p.",
            "steps": [
                say("Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). The new move is that ⅓."),
                box("Square the radius: 6² = ", 36, "6 × 6."),
                box("Multiply by the height: 36 × 9 = ", 324, "This is r²h."),
                box("Take one third: 324 ÷ 3 = ", 108, "The cone factor.", done="That is 108π."),
                box("Multiply by π: 108 × π = ", 339.3, "π button, 1 d.p.", done="V = 339.3 cm³. The new move: the ⅓ a cone always needs.")
            ]
        },
        "gold": {
            "display": cyl_cone("A cylinder radius 4 cm height 6 cm with a cone radius 4 cm height 6 cm on top", "r = 4 cm", "h = 6 cm") + "A solid is a cylinder (r = 4 cm, h = 6 cm) with a cone (r = 4 cm, h = 6 cm) on top. Find the total volume to 1 d.p.",
            "steps": [
                say("A composite solid is two shapes joined. Find each volume, then add. The new move: split into parts."),
                box("Cylinder: π × 4² × 6 = 96π = ", 301.6, "96 × π, 1 d.p."),
                box("Cone: ⅓ × π × 4² × 6 = 32π = ", 100.5, "32 × π, 1 d.p."),
                box("Add them: 301.6 + 100.5 = ", 402.1, "Cylinder plus cone.", done="Total 402.1 cm³."),
                box("Check in π units: 96 + 32 = ", 128, "128π altogether.", done="128π = 402.1 cm³. The new move: split, then add.")
            ]
        }
    }
}

# fix g2 last check box value (avoid the inline-False hack)
pd["problem_bank"]["gold"][2]["guided_steps"][-1]["answer"] = round(256/3, 1)

json.dump(pd, io.open("lesson_maths-eduqas_geometry-L03.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written. bronze=%d silver=%d gold=%d" % (len(bronze), len(silver), len(gold)))
