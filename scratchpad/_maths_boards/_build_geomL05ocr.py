# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion of OCR geometry-L05.
Preserves worked_examples / related_videos / topic_links byte-for-byte."""
import json, math, io

SRC = "_geomL05ocr_live.json"
OUT = "lesson_maths-ocr_geometry-L05.json"
pd = json.load(io.open(SRC, encoding="utf-8"))

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---------- SVG helpers (currentColor text, soft fills, no external refs) ----
def right_triangle(base_u, height_u, base_lbl, left_lbl, hyp_lbl,
                   theta_lbl=None, aria="Right-angled triangle"):
    """Right angle bottom-left (A). Vertical left leg = 'left', horizontal
    bottom leg = 'base', hypotenuse from top-left(C) to bottom-right(B).
    theta (if any) sits at B (bottom-right)."""
    m = max(base_u, height_u)
    scale = 120.0 / m
    base = base_u * scale
    height = height_u * scale
    # keep legibility
    if base < 34: base = 34.0
    if height < 34: height = 34.0
    pl, pt, pb, pr = 42, 20, 30, 46
    Ax, Ay = pl, pt + height
    Cx, Cy = pl, pt
    Bx, By = pl + base, pt + height
    vw = pl + base + pr
    vh = pt + height + pb
    # right-angle marker at A (into triangle: up + right)
    ra = "M %.1f %.1f L %.1f %.1f L %.1f %.1f" % (Ax, Ay-11, Ax+11, Ay-11, Ax+11, Ay)
    parts = []
    parts.append('<svg viewBox="0 0 %.0f %.0f" role="img" aria-label="%s" '
                 'style="max-width:280px;height:auto">' % (vw, vh, aria))
    parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>' % (Ax,Ay,Bx,By,Cx,Cy))
    parts.append('<path d="%s" fill="none" stroke="currentColor" stroke-width="1.3"/>' % ra)
    # angle arc at B
    if theta_lbl is not None:
        # direction B->A is (-1,0); B->C is unit(C-B)
        dx, dy = Cx-Bx, Cy-By
        L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
        r = 20
        p1x, p1y = Bx - r, By          # along B->A
        p2x, p2y = Bx + ux*r, By + uy*r
        parts.append('<path d="M %.1f %.1f A %d %d 0 0 1 %.1f %.1f" fill="none" stroke="currentColor" stroke-width="1.2"/>' % (p1x,p1y,r,r,p2x,p2y))
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">%s</text>' % (Bx-24, By-7, theta_lbl))
    # side labels
    parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % ((Ax+Bx)/2, By+18, base_lbl))
    parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">%s</text>' % (Ax-6, (Ay+Cy)/2+4, left_lbl))
    parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>' % ((Cx+Bx)/2+7, (Cy+By)/2-5, hyp_lbl))
    parts.append('</svg>')
    return "".join(parts)

def wall_triangle(base_lbl, up_lbl, hyp_lbl, aria):
    """Ladder against wall: vertical wall (left), ground (bottom), ladder=hyp."""
    return right_triangle(3, 4, base_lbl, up_lbl, hyp_lbl, None, aria)

def rectangle_svg(w_lbl, h_lbl, diag_lbl):
    x0,y0,W,H = 30,20,150,112  # 8:6 ~ 150:112
    x1,y1 = x0+W, y0+H
    p=[]
    p.append('<svg viewBox="0 0 220 175" role="img" aria-label="Rectangle with a diagonal" style="max-width:280px;height:auto">')
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#34d399" fill-opacity="0.13" stroke="currentColor" stroke-width="1.6"/>'%(x0,y0,W,H))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 3"/>'%(x0,y1,x1,y0))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>'%((x0+x1)//2, y1+18, w_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>'%(x1+6, (y0+y1)//2, h_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">%s</text>'%((x0+x1)//2-6, (y0+y1)//2-4, diag_lbl))
    p.append('</svg>')
    return "".join(p)

def isosceles_svg(equal_lbl, base_lbl, h_lbl):
    # apex top-centre, base bottom, dashed height
    ax,ay = 110,22
    blx,bly = 40,150
    brx,bry = 180,150
    mx = (blx+brx)//2
    p=[]
    p.append('<svg viewBox="0 0 230 185" role="img" aria-label="Isosceles triangle with height drawn to the base" style="max-width:280px;height:auto">')
    p.append('<polygon points="%d,%d %d,%d %d,%d" fill="#60a5fa" fill-opacity="0.13" stroke="currentColor" stroke-width="1.6"/>'%(ax,ay,blx,bly,brx,bry))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3"/>'%(ax,ay,mx,bly))
    p.append('<path d="M %d %d L %d %d L %d %d" fill="none" stroke="currentColor" stroke-width="1.1"/>'%(mx-10,bly, mx-10,bly-10, mx,bly-10))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">%s</text>'%((ax+blx)//2-4,(ay+bly)//2, equal_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>'%((ax+brx)//2+4,(ay+bry)//2, equal_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>'%(mx, bly+18, base_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>'%(mx+6, (ay+bly)//2, h_lbl))
    p.append('</svg>')
    return "".join(p)

def cuboid_svg(w_lbl,d_lbl,h_lbl,diag_lbl):
    # simple isometric cuboid, space diagonal dashed
    p=[]
    p.append('<svg viewBox="0 0 230 190" role="img" aria-label="Cuboid with its space diagonal" style="max-width:280px;height:auto">')
    # front face
    fx,fy,fw,fh = 40,60,110,90
    ox,oy = 45,-38  # offset for depth
    # front rectangle
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#f59e0b" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>'%(fx,fy,fw,fh))
    # top edges
    p.append('<path d="M %d %d L %d %d L %d %d" fill="none" stroke="currentColor" stroke-width="1.3"/>'%(fx,fy, fx+ox,fy+oy, fx+ox+fw,fy+oy))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.3"/>'%(fx+fw,fy, fx+ox+fw,fy+oy))
    # back verticals (dashed hidden)
    p.append('<path d="M %d %d L %d %d L %d %d" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>'%(fx+ox,fy+oy, fx+ox,fy+oy+fh, fx+fw+ox,fy+oy+fh))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>'%(fx+ox,fy+oy+fh, fx,fy+fh))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>'%(fx+fw+ox,fy+oy+fh, fx+fw,fy+fh))
    # space diagonal front-bottom-left to back-top-right
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>'%(fx,fy+fh, fx+fw+ox,fy+oy))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>'%(fx+fw//2, fy+fh+17, w_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">%s</text>'%(fx-6, fy+fh//2, h_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>'%(fx+fw+ox//2+4, fy+oy//2+6, d_lbl))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>'%(fx+fw//2+18, fy+fh//2+2, diag_lbl))
    p.append('</svg>')
    return "".join(p)

def opener_svg():
    # right triangle 3-4-5 with tiled square on each short leg
    u = 24
    # A right angle bottom-left
    Ax,Ay = 96,150
    Cx,Cy = 96, 150-3*u   # top (vertical leg 3 units)
    Bx,By = 96+4*u, 150   # right (horizontal leg 4 units)
    p=[]
    p.append('<svg viewBox="0 0 216 262" role="img" aria-label="A right-angled triangle with a 3 by 3 tiled square on one short side and a 4 by 4 tiled square on the other" style="max-width:280px;height:auto">')
    # left square (on AB vertical leg) extends left
    lx = Cx-3*u
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.3"/>'%(lx,Cy,3*u,3*u))
    for i in range(1,3):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>'%(lx+i*u,Cy,lx+i*u,Cy+3*u))
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>'%(lx,Cy+i*u,lx+3*u,Cy+i*u))
    # bottom square (on AC horizontal leg) extends down
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#34d399" fill-opacity="0.18" stroke="currentColor" stroke-width="1.3"/>'%(Ax,Ay,4*u,4*u))
    for i in range(1,4):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>'%(Ax+i*u,Ay,Ax+i*u,Ay+4*u))
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>'%(Ax,Ay+i*u,Ax+4*u,Ay+i*u))
    # triangle
    p.append('<polygon points="%d,%d %d,%d %d,%d" fill="none" stroke="currentColor" stroke-width="1.8"/>'%(Ax,Ay,Bx,By,Cx,Cy))
    p.append('<path d="M %d %d L %d %d L %d %d" fill="none" stroke="currentColor" stroke-width="1.1"/>'%(Ax,Ay-11,Ax+11,Ay-11,Ax+11,Ay))
    # labels
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">9 tiles</text>'%(lx+3*u//2, Cy+3*u//2+4))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">16 tiles</text>'%(Ax+4*u//2, Ay+4*u//2+4))
    p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">c = ?</text>'%((Cx+Bx)//2+6,(Cy+By)//2-5))
    p.append('</svg>')
    return "".join(p)

# ---------- guided_steps builders --------------------------------------------
def gs_pyth_hyp(a,b,ans):
    add=a*a+b*b
    return [
        {"say":"Two shorter sides, no angle: Pythagoras. Square each, add, then square root."},
        {"pre":"%d² = "%a,"hint":"%d × %d."%(a,a),"answer":a*a},
        {"pre":"%d² = "%b,"hint":"%d × %d."%(b,b),"answer":b*b},
        {"pre":"Add the squares: %d + %d = "%(a*a,b*b),"hint":"Just add the two squares.","answer":add},
        {"pre":"Square root to get the hypotenuse: √%d = "%add,"hint":"What number times itself makes %d?"%add,"phase":"substitute","answer":ans},
        {"pre":"Check: %g² = "%ans,"done":"%d matches %d + %d, so the hypotenuse is %g."%(add,a*a,b*b,ans),"hint":"%g × %g."%(ans,ans),"answer":add},
    ]

def gs_pyth_leg(hyp,leg,ans):
    diff=hyp*hyp-leg*leg
    return [
        {"say":"The hypotenuse is known, so this time subtract: square both, take the smaller from the larger, then root."},
        {"pre":"%d² = "%hyp,"hint":"%d × %d."%(hyp,hyp),"answer":hyp*hyp},
        {"pre":"%d² = "%leg,"hint":"%d × %d."%(leg,leg),"answer":leg*leg},
        {"pre":"Subtract, because the hypotenuse is known: %d − %d = "%(hyp*hyp,leg*leg),"hint":"Bigger square minus smaller square.","answer":diff},
        {"pre":"√%d = "%diff,"hint":"What number times itself makes %d?"%diff,"phase":"substitute","answer":ans},
        {"pre":"Check: %g² + %d² = "%(ans,leg),"done":"%d = %d², so the missing side is %g."%(hyp*hyp,hyp,ans),"hint":"%d + %d."%(diff,leg*leg),"answer":hyp*hyp},
    ]

# ---------- assemble problem_bank -------------------------------------------
pb = pd["problem_bank"]

def setp(prob, svg, hint, gs, misc):
    if svg:
        prob["display"] = svg + CAP + prob["display"]
    prob["hint"] = hint
    if gs is not None:
        prob["guided_steps"] = gs
    prob["misconceptions"] = misc

# BRONZE ----------------------------------------------------------------------
b = pb["bronze"]
setp(b[0], right_triangle(8,6,"8 cm","6 cm","?",None,"Right-angled triangle, legs 8 cm and 6 cm, hypotenuse unknown"),
     "Square both legs, add them, then square root.",
     gs_pyth_hyp(6,8,10),
     [{"check":"common","pattern":"wrong_formula","expect":14,"message":"You added the sides: 6 + 8 = 14. Pythagoras squares first: c = √(6² + 8²) = √(36 + 64) = √100 = 10."}])
setp(b[1], right_triangle(12,5,"?","5 cm","13 cm",None,"Right-angled triangle, hypotenuse 13 cm, one leg 5 cm, other leg unknown"),
     "The hypotenuse is known, so subtract: √(13² − 5²).",
     gs_pyth_leg(13,5,12),
     [{"check":"common","pattern":"forgot_step","expect":13.9,"message":"You added: √(13² + 5²) = √194 ≈ 13.9. The hypotenuse is known, so SUBTRACT: √(169 − 25) = √144 = 12."}])
setp(b[2], right_triangle(12,5,"12 cm","5 cm","?",None,"Right-angled triangle, legs 12 cm and 5 cm, hypotenuse unknown"),
     "Square both legs, add them, then square root.",
     gs_pyth_hyp(5,12,13),
     [{"check":"common","pattern":"wrong_formula","expect":17,"message":"You added the sides: 5 + 12 = 17. Pythagoras squares first: c = √(5² + 12²) = √169 = 13."}])
setp(b[3], right_triangle(8,6,"?","6 cm","10 cm",None,"Right-angled triangle, hypotenuse 10 cm, one leg 6 cm, other leg unknown"),
     "The hypotenuse is known, so subtract: √(10² − 6²).",
     gs_pyth_leg(10,6,8),
     [{"check":"common","pattern":"forgot_step","expect":11.7,"message":"You added: √(10² + 6²) = √136 ≈ 11.7. When the hypotenuse is known you SUBTRACT: √(100 − 36) = √64 = 8."}])
setp(b[4], right_triangle(12,9,"12 cm","9 cm","?",None,"Right-angled triangle, legs 12 cm and 9 cm, hypotenuse unknown"),
     "Square both legs, add them, then square root.",
     gs_pyth_hyp(9,12,15),
     [{"check":"common","pattern":"wrong_formula","expect":21,"message":"You added the sides: 9 + 12 = 21. Pythagoras squares first: c = √(9² + 12²) = √225 = 15."}])
# b[5] multiple choice, no svg, no guided_steps
b[5]["hint"] = "Match the two named sides to the ratio: SOH, CAH, TOA."
b[5]["misconceptions"] = [{"check":"common","pattern":"confused_ratio","expect":None,"message":"SOH means sin = opposite ÷ hypotenuse, so opposite and hypotenuse point to sin. cos pairs adjacent and hypotenuse; tan pairs opposite and adjacent."}]
setp(b[6], right_triangle(15,8,"15 cm","8 cm","?",None,"Right-angled triangle, legs 15 cm and 8 cm, hypotenuse unknown"),
     "Square both legs, add them, then square root.",
     gs_pyth_hyp(8,15,17),
     [{"check":"common","pattern":"wrong_formula","expect":23,"message":"You added the sides: 8 + 15 = 23. Pythagoras squares first: c = √(8² + 15²) = √289 = 17."}])
setp(b[7], right_triangle(24,7,"?","7 cm","25 cm",None,"Right-angled triangle, hypotenuse 25 cm, one leg 7 cm, other leg unknown"),
     "The hypotenuse is known, so subtract: √(25² − 7²).",
     gs_pyth_leg(25,7,24),
     [{"check":"common","pattern":"forgot_step","expect":26.0,"message":"You added: √(25² + 7²) = √674 ≈ 26.0. The hypotenuse is known, so SUBTRACT: √(625 − 49) = √576 = 24."}])

# SILVER ----------------------------------------------------------------------
s = pb["silver"]
# S0 find theta opp5 adj12 -> 22.6 (tan)
setp(s[0], right_triangle(12,5,"12 cm","5 cm","",u"θ = ?","Right-angled triangle with opposite 5 cm, adjacent 12 cm, angle theta unknown"),
     "Opposite and adjacent point to tan: θ = tan⁻¹(5 ÷ 12).",
     [{"say":"You have the opposite (5) and the adjacent (12). Opposite over adjacent is tan, so use inverse tan to get the angle."},
      {"pre":"The ratio, opposite ÷ adjacent: 5 ÷ 12, to 2 d.p. = ","hint":"Divide 5 by 12.","answer":0.42},
      {"pre":"θ = tan⁻¹(5 ÷ 12) = ","hint":"Press tan⁻¹, then 5 ÷ 12; keep full accuracy.","phase":"substitute","answer":22.6},
      {"pre":"Check: tan22.6°, to 2 d.p. = ","done":"0.42 matches 5 ÷ 12, so θ = 22.6°.","hint":"Type tan(22.6) and round to 2 d.p.","answer":0.42}],
     [{"check":"common","pattern":"wrong_formula","expect":67.4,"message":"You may have used 12 ÷ 5: tan⁻¹(12 ÷ 5) ≈ 67.4°. The opposite is 5 and the adjacent is 12, so θ = tan⁻¹(5 ÷ 12) ≈ 22.6°."}])
# S1 find opposite 40 adj10 -> 8.4 (tan)
setp(s[1], right_triangle(10,8.4,"10 cm","?","",u"40°","Right-angled triangle, angle 40 degrees, adjacent 10 cm, opposite unknown"),
     "Opposite with adjacent means tan: O = 10 × tan40°.",
     [{"say":"You know the adjacent (10) and want the opposite, with the angle 40°. Opposite over adjacent is tan, so O = adjacent × tan40°."},
      {"pre":"tan40°, to 2 d.p. = ","hint":"Type tan(40) on the calculator.","answer":0.84},
      {"pre":"O = 10 × tan40° = ","hint":"Multiply 10 by tan40°, keeping full accuracy.","phase":"substitute","answer":8.4},
      {"pre":"Check: O ÷ 10 = 8.4 ÷ 10 = ","done":"0.84 = tan40°, so the opposite side is 8.4 cm.","hint":"8.4 divided by 10.","answer":0.84}],
     [{"check":"common","pattern":"wrong_ratio","expect":6.4,"message":"You may have used sine: 10 × sin40° ≈ 6.4. Opposite with adjacent means tan: O = 10 × tan40° ≈ 8.4 cm."}])
# S2 find hyp 30 opp7 -> 14 (sin)
setp(s[2], right_triangle(12.1,7,"","7 cm","?",u"30°","Right-angled triangle, angle 30 degrees, opposite 7 cm, hypotenuse unknown"),
     "Opposite with hypotenuse means sin: H = 7 ÷ sin30°.",
     [{"say":"You know the opposite (7) and want the hypotenuse, with angle 30°. sin30° = opposite ÷ hypotenuse, so hypotenuse = opposite ÷ sin30°."},
      {"pre":"sin30° = ","hint":"A known value: sin30° is exactly 0.5.","answer":0.5},
      {"pre":"H = 7 ÷ 0.5 = ","hint":"Divide 7 by 0.5 (the same as doubling).","phase":"substitute","answer":14},
      {"pre":"Check: opposite ÷ hypotenuse = 7 ÷ 14 = ","done":"0.5 = sin30°, so the hypotenuse is 14 cm.","hint":"Seven divided by fourteen.","answer":0.5}],
     [{"check":"common","pattern":"wrong_formula","expect":3.5,"message":"You may have multiplied: 7 × sin30° = 3.5. The hypotenuse is bigger than the opposite, so DIVIDE: H = 7 ÷ sin30° = 14 cm."}])
# S3 find theta adj8 hyp10 -> 36.9 (cos)
setp(s[3], right_triangle(8,6,"8 cm","","10 cm",u"θ = ?","Right-angled triangle, adjacent 8 cm, hypotenuse 10 cm, angle theta unknown"),
     "Adjacent and hypotenuse point to cos: θ = cos⁻¹(8 ÷ 10).",
     [{"say":"You have the adjacent (8) and the hypotenuse (10). Adjacent over hypotenuse is cos, so use inverse cos for the angle."},
      {"pre":"The ratio, adjacent ÷ hypotenuse: 8 ÷ 10 = ","hint":"Divide 8 by 10.","answer":0.8},
      {"pre":"θ = cos⁻¹(0.8) = ","hint":"Press cos⁻¹, then 0.8.","phase":"substitute","answer":36.9},
      {"pre":"Check: cos36.9°, to 2 d.p. = ","done":"0.80 matches 8 ÷ 10, so θ = 36.9°.","hint":"Type cos(36.9) and round to 2 d.p.","answer":0.8}],
     [{"check":"common","pattern":"wrong_formula","expect":53.1,"message":"You may have used sin⁻¹: sin⁻¹(8 ÷ 10) ≈ 53.1°. Adjacent with hypotenuse means cos: θ = cos⁻¹(0.8) ≈ 36.9°."}])
# S4 ladder 5 base3 height 4 (pyth, calc)
setp(s[4], wall_triangle("3 m","?","5 m","A ladder 5 m as the hypotenuse, base 3 m along the ground, height up the wall unknown"),
     "The ladder is the hypotenuse, so subtract: √(5² − 3²).",
     [{"say":"The ladder leans to make a right triangle: the ladder (5) is the hypotenuse, the base (3) is along the ground, the wall height is the third side. Subtract."},
      {"pre":"5² = ","hint":"Five squared is 5 × 5.","answer":25},
      {"pre":"3² = ","hint":"Three squared is 3 × 3.","answer":9},
      {"pre":"Subtract, because the ladder is the hypotenuse: 25 − 9 = ","hint":"Bigger square minus smaller square.","answer":16},
      {"pre":"√16 = ","hint":"What number times itself makes 16?","phase":"substitute","answer":4},
      {"pre":"Check: 4² + 3² = ","done":"25 = 5², so the ladder reaches 4 m up the wall.","hint":"16 + 9.","answer":25}],
     [{"check":"common","pattern":"forgot_step","expect":5.8,"message":"You added: √(5² + 3²) = √34 ≈ 5.8. The ladder is the hypotenuse, so SUBTRACT: √(25 − 9) = √16 = 4 m."}])
# S5 find adjacent 50 hyp15 -> 9.6 (cos)
setp(s[5], right_triangle(9.6,11.5,"?","","15 cm",u"50°","Right-angled triangle, angle 50 degrees, hypotenuse 15 cm, adjacent unknown"),
     "Adjacent with hypotenuse means cos: A = 15 × cos50°.",
     [{"say":"You know the hypotenuse (15) and want the adjacent, with angle 50°. cos50° = adjacent ÷ hypotenuse, so adjacent = hypotenuse × cos50°."},
      {"pre":"cos50°, to 2 d.p. = ","hint":"Type cos(50) on the calculator.","answer":0.64},
      {"pre":"A = 15 × cos50° = ","hint":"Multiply 15 by cos50°, keeping full accuracy.","phase":"substitute","answer":9.6},
      {"pre":"Check: A ÷ 15 = 9.6 ÷ 15, to 2 d.p. = ","done":"0.64 = cos50°, so the adjacent side is 9.6 cm.","hint":"9.6 divided by 15.","answer":0.64}],
     [{"check":"common","pattern":"wrong_ratio","expect":11.5,"message":"You may have used sine: 15 × sin50° ≈ 11.5. Adjacent with hypotenuse means cos: A = 15 × cos50° ≈ 9.6 cm."}])
# S6 (FIXED) find theta opp7 hyp25 -> 16.3 (sin). display rewritten.
s[6]["display"] = right_triangle(24,7,"","7 cm","25 cm",u"θ = ?","Right-angled triangle, opposite 7 cm, hypotenuse 25 cm, angle theta unknown") + CAP + u"Find angle \\(\\theta\\): opposite = 7, hypotenuse = 25. To 1 d.p."
s[6]["solutions"] = [16.3]
s[6]["hint"] = "Opposite and hypotenuse point to sin: θ = sin⁻¹(7 ÷ 25)."
s[6]["guided_steps"] = [
    {"say":"You have the opposite (7) and the hypotenuse (25). Opposite over hypotenuse is sin, so use inverse sin for the angle."},
    {"pre":"The ratio, opposite ÷ hypotenuse: 7 ÷ 25 = ","hint":"Divide 7 by 25.","answer":0.28},
    {"pre":"θ = sin⁻¹(0.28) = ","hint":"Press sin⁻¹, then 0.28.","phase":"substitute","answer":16.3},
    {"pre":"Check: sin16.3°, to 2 d.p. = ","done":"0.28 matches 7 ÷ 25, so θ = 16.3°.","hint":"Type sin(16.3) and round to 2 d.p.","answer":0.28}]
s[6]["misconceptions"] = [{"check":"common","pattern":"wrong_formula","expect":73.7,"message":"You may have used cos⁻¹: cos⁻¹(0.28) ≈ 73.7°. Opposite with hypotenuse means sin: θ = sin⁻¹(0.28) ≈ 16.3°."}]

# GOLD ------------------------------------------------------------------------
g = pb["gold"]
# G0 rectangle 8x6 diagonal 10
setp(g[0], rectangle_svg("8 cm","6 cm","?"),
     "The diagonal is the hypotenuse of an 8 by 6 right triangle: √(8² + 6²).",
     [{"say":"A rectangle's diagonal splits it into two right triangles with legs 8 and 6. The diagonal is the hypotenuse, so use Pythagoras."},
      {"pre":"8² = ","hint":"8 × 8.","answer":64},
      {"pre":"6² = ","hint":"6 × 6.","answer":36},
      {"pre":"Add: 64 + 36 = ","hint":"Just add the two squares.","answer":100},
      {"pre":"√100 = ","hint":"What number times itself makes 100?","phase":"substitute","answer":10},
      {"pre":"Check: 10² = ","done":"100 = 64 + 36, so the diagonal is 10 cm.","hint":"10 × 10.","answer":100}],
     [{"check":"common","pattern":"wrong_formula","expect":14,"message":"You added the sides: 8 + 6 = 14. The diagonal is the hypotenuse: √(8² + 6²) = √100 = 10 cm."}])
# G1 isosceles equal10 base12 height8
setp(g[1], isosceles_svg("10 cm","12 cm","?"),
     "Drop the height to split the base in half, then use Pythagoras with 10 and 6.",
     [{"say":"The height drops to the middle of the base, splitting it into two equal halves and making a right triangle with hypotenuse 10."},
      {"pre":"Half the base: 12 ÷ 2 = ","hint":"The height splits the base into two equal halves.","answer":6},
      {"pre":"The equal side is the hypotenuse: 10² = ","hint":"10 × 10.","answer":100},
      {"pre":"6² = ","hint":"6 × 6.","answer":36},
      {"pre":"Subtract: 100 − 36 = ","hint":"Bigger square minus smaller square.","answer":64},
      {"pre":"√64 = ","hint":"What number times itself makes 64?","phase":"substitute","answer":8},
      {"pre":"Check: 8² + 6² = ","done":"100 = 10², so the height is 8 cm.","hint":"64 + 36.","answer":100}],
     [{"note":"Using full base 12 gives sqrt(100-144), not real: no determinate wrong value.","check":"common","pattern":"forgot_step","expect":None,"message":"Halve the base first. The height makes a right triangle with hypotenuse 10 and base 6 (half of 12): h = √(10² − 6²) = √64 = 8 cm. Using the full base of 12 has no real answer."}])
# G2 cuboid 3x4x12 space diagonal 13
setp(g[2], cuboid_svg("4","3","12","?"),
     "Space diagonal: square all three edges, add, then square root.",
     [{"say":"The space diagonal of a cuboid uses all three edges: d = √(length² + width² + height²)."},
      {"pre":"3² = ","hint":"3 × 3.","answer":9},
      {"pre":"4² = ","hint":"4 × 4.","answer":16},
      {"pre":"12² = ","hint":"12 × 12.","answer":144},
      {"pre":"Add all three: 9 + 16 + 144 = ","hint":"Sum the three squares.","answer":169},
      {"pre":"√169 = ","hint":"What number times itself makes 169?","phase":"substitute","answer":13},
      {"pre":"Check: 13² = ","done":"169 = 9 + 16 + 144, so the space diagonal is 13.","hint":"13 × 13.","answer":169}],
     [{"check":"common","pattern":"forgot_step","expect":5,"message":"You may have used only two edges: √(3² + 4²) = 5. A space diagonal needs all three: √(3² + 4² + 12²) = √169 = 13."}])
# G3 (FIXED) ship 9N 12E -> 15
g[3]["display"] = right_triangle(12,9,"12 km","9 km","?",None,"Two legs of a journey at a right angle, 9 km north and 12 km east, direct distance unknown") + CAP + u"A ship sails 9 km North then 12 km East. How far is it from the start?"
g[3]["solutions"] = [15]
g[3]["hint"] = "The two legs meet at a right angle, so the direct distance is √(9² + 12²)."
g[3]["guided_steps"] = [
    {"say":"North then East turns a right angle, so the two legs are 9 and 12 and the straight line back is the hypotenuse."},
    {"pre":"9² = ","hint":"9 × 9.","answer":81},
    {"pre":"12² = ","hint":"12 × 12.","answer":144},
    {"pre":"Add: 81 + 144 = ","hint":"Just add the two squares.","answer":225},
    {"pre":"√225 = ","hint":"What number times itself makes 225?","phase":"substitute","answer":15},
    {"pre":"Check: 15² = ","done":"225 = 81 + 144, so the ship is 15 km from the start.","hint":"15 × 15.","answer":225}]
g[3]["misconceptions"] = [{"check":"common","pattern":"wrong_formula","expect":21,"message":"You added the distances: 9 + 12 = 21. The direct line is the hypotenuse: √(9² + 12²) = √225 = 15 km."}]
# G4 elevation 32, 50m -> 31.2 (tan)
setp(g[4], right_triangle(50,31.2,"50 m","?","",u"32°","Right-angled triangle, distance 50 m along the ground, angle of elevation 32 degrees, tree height unknown"),
     "Height is opposite, distance is adjacent: height = 50 × tan32°.",
     [{"say":"The tree height is opposite the 32° angle and the 50 m distance is adjacent. Opposite over adjacent is tan, so height = 50 × tan32°."},
      {"pre":"tan32°, to 2 d.p. = ","hint":"Type tan(32) on the calculator.","answer":0.62},
      {"pre":"h = 50 × tan32° = ","hint":"Multiply 50 by tan32°, keeping full accuracy.","phase":"substitute","answer":31.2},
      {"pre":"Check: h ÷ 50 = 31.2 ÷ 50, to 2 d.p. = ","done":"0.62 = tan32°, so the tree is 31.2 m tall.","hint":"31.2 divided by 50.","answer":0.62}],
     [{"check":"common","pattern":"wrong_ratio","expect":26.5,"message":"You may have used sine, treating 50 m as the hypotenuse: 50 × sin32° ≈ 26.5. Here 50 m is the adjacent, so use tan: h = 50 × tan32° ≈ 31.2 m."}])

# descriptions
pb["bronze_description"] = "Put the numbers straight into one formula: for Pythagoras square, add or subtract and root; for a trig side multiply the hypotenuse by a known sine or cosine, or use inverse tan for an angle."
pb["silver_description"] = "Decide the method first, then rearrange it: choose Pythagoras or the ratio that pairs your two sides (sin, cos or tan), substitute and solve, often inside a real shape."
pb["gold_description"] = "Turn a worded or 3D situation into a right-angled triangle, then finish with Pythagoras or trigonometry: journeys and diagonals give sides, elevation and depression give angles."

# ---------- guided (opener + teach) -----------------------------------------
pd["guided"] = {
  "opener": {
    "label":"Before any formula",
    "display": opener_svg() + u"A right angle with a tiled square built on each short side.<br>One square is 3 by 3 (9 tiles), the other is 4 by 4 (16 tiles).",
    "steps":[
      {"say":"Here is a right-angled triangle with a square of tiles built on each short side. No formula needed, just count and add.",
       "pre":"The two smaller squares hold 9 tiles and 16 tiles. Altogether that is 9 + 16 = ","hint":"Just add the two tile counts.","answer":25},
      {"say":"The clever bit: the square built on the longest side holds exactly that many tiles too, 25.",
       "pre":"A square made of 25 tiles is how many tiles along each edge? ","hint":"What number times itself makes 25?","answer":5},
      {"say":"So the longest side is 5. In symbols, the short sides \\(a\\) and \\(b\\) and the longest side \\(c\\) obey \\(a^2 + b^2 = c^2\\). Squaring a side counts the tiles in its square; square rooting turns the tile count back into a length."}
    ]
  },
  "teach": {
    "bronze": {
      "label":"Together: your first one",
      "display": right_triangle(16,12,"16 cm","12 cm","?",None,"Right-angled triangle, legs 16 cm and 12 cm, hypotenuse unknown") + CAP + "Find the hypotenuse of a right triangle with shorter sides 12 cm and 16 cm.",
      "steps":[
        {"say":"The two shorter sides are 12 and 16, and no angle is involved. Pythagoras: square each, add, then square root."},
        {"pre":"12² = ","hint":"12 × 12.","answer":144},
        {"pre":"16² = ","hint":"16 × 16.","answer":256},
        {"pre":"Add the squares: 144 + 256 = ","hint":"Just add them.","answer":400},
        {"pre":"Square root to get the hypotenuse: √400 = ","done":"Square, add, root. That is the whole method.","hint":"What number times itself makes 400? Try 20.","answer":20},
        {"pre":"Check: 20² = ","done":"400 = 144 + 256, so the hypotenuse is 20 cm.","hint":"20 × 20.","answer":400}
      ]
    },
    "silver": {
      "label":"Together: the silver move",
      "display": right_triangle(12,9,"12 cm","9 cm","",u"θ = ?","Right-angled triangle, opposite 9 cm, adjacent 12 cm, angle theta unknown") + CAP + u"In a right triangle the opposite side is 9 cm and the adjacent side is 12 cm. Find the angle \\(\\theta\\) to 1 d.p.",
      "steps":[
        {"say":"You know the opposite and the adjacent, so the ratio is tan. To get the angle back, use inverse tan, the new move at this level."},
        {"pre":"The ratio, opposite ÷ adjacent: 9 ÷ 12 = ","hint":"Divide 9 by 12.","answer":0.75},
        {"pre":"Inverse tan turns that ratio into the angle: θ = tan⁻¹(0.75) = ","done":"Inverse tan undoes tan to reveal the angle. That was the point.","hint":"Press tan⁻¹, then 0.75.","answer":36.9},
        {"pre":"The two acute angles add to 90°, so the other one is 90 − 36.9 = ","hint":"Ninety minus 36.9.","answer":53.1},
        {"pre":"Check: tan36.9°, to 2 d.p. = ","done":"0.75 matches 9 ÷ 12, so θ = 36.9°.","hint":"Type tan(36.9) and round to 2 d.p.","answer":0.75}
      ]
    },
    "gold": {
      "label":"Together: the gold move",
      "display": right_triangle(9,2,"9 m","?","",u"θ = ?","Right-angled triangle, horizontal run 9 m, rise unknown, angle theta unknown") + CAP + u"A ramp rises 2 m over a horizontal run of 9 m. Find the angle the ramp makes with the ground, to 1 d.p.",
      "steps":[
        {"say":"Read the triangle out of the words: the rise, 2 m, is opposite the angle; the run, 9 m, is adjacent. Opposite and adjacent means tan."},
        {"pre":"The ratio, rise ÷ run: 2 ÷ 9, to 2 d.p. = ","hint":"Divide 2 by 9.","answer":0.22},
        {"pre":"Inverse tan gives the angle: θ = tan⁻¹(2 ÷ 9) = ","done":"Building the triangle from the words is the gold move.","hint":"Press tan⁻¹, then 2 ÷ 9; keep full accuracy.","answer":12.5},
        {"pre":"Check: tan12.5°, to 2 d.p. = ","done":"0.22 matches 2 ÷ 9, so the ramp sits at 12.5°.","hint":"Type tan(12.5) and round to 2 d.p.","answer":0.22},
        {"pre":"The ramp itself is the hypotenuse: √(2² + 9²) = √85, to 1 d.p. = ","done":"Same triangle, Pythagoras gives the ramp's length: 9.2 m.","hint":"Square root of 85 on the calculator.","answer":9.2}
      ]
    }
  }
}

# ---------- tier_guides ------------------------------------------------------
pd["tier_guides"] = {
  "bronze": {
    "title":"Bronze: one formula, straight in",
    "steps":[
      "Read the two known values straight off the triangle. No rearranging yet.",
      "For Pythagoras: square both, then add for the hypotenuse, or subtract then root for a shorter side.",
      "For a trig side you are given the ratio (like <strong>sin30° = 0.5</strong>): multiply the hypotenuse by it. For an angle, use \\(\\tan^{-1}\\) on the ratio."
    ],
    "example":{
      "question":"Find the hypotenuse: sides 6 cm and 8 cm.",
      "steps":[
        {"label":"Square and add","content":"<p>\\(6^2 + 8^2 = 36 + 64 = 100\\)</p>"},
        {"label":"Square root","content":"<p>\\(c = \\sqrt{100} = 10\\)</p>"},
        {"label":"Check","content":"<p>\\(6^2 + 8^2 = 100 = 10^2\\) ✓</p>"},
        {"label":"Answer","content":"<p>\\(c = 10\\) cm</p>","isAnswer":True,"is_answer":True}
      ]
    }
  },
  "silver": {
    "title":"Silver: choose and rearrange",
    "steps":[
      "Nothing is ready to use. First decide: Pythagoras (three sides, no angle) or a trig ratio (an angle is involved).",
      "Pick the ratio that pairs your two sides: \\(\\sin\\) for O and H, \\(\\cos\\) for A and H, \\(\\tan\\) for O and A. Rearrange for the unknown.",
      "Real shapes count too: split an isosceles triangle down the middle, or read a rectangle's diagonal as a hypotenuse."
    ],
    "example":{
      "question":"Find angle θ when the adjacent is 8 cm and the hypotenuse is 10 cm.",
      "steps":[
        {"label":"Choose ratio","content":"<p>Adjacent and hypotenuse, so \\(\\cos\\theta = \\frac{A}{H} = \\frac{8}{10}\\).</p>"},
        {"label":"Inverse","content":"<p>\\(\\theta = \\cos^{-1}(0.8) = 36.9°\\)</p>"},
        {"label":"Check","content":"<p>\\(\\cos 36.9° = 0.80 = 8 \\div 10\\) ✓</p>"},
        {"label":"Answer","content":"<p>\\(\\theta = 36.9°\\)</p>","isAnswer":True,"is_answer":True}
      ]
    }
  },
  "gold": {
    "title":"Gold: build the triangle from the words",
    "steps":[
      "The right triangle is hidden in a story, a 3D solid or a shape. Sketch it and label the sides you are told.",
      "Journeys and diagonals give two legs (find the hypotenuse). Elevation and depression give an angle with a height and a distance (use \\(\\tan\\)).",
      "For a cuboid's space diagonal, square all three edges before rooting: \\(d = \\sqrt{a^2 + b^2 + c^2}\\)."
    ],
    "example":{
      "question":"A ship sails 9 km north then 12 km east. How far is it from the start?",
      "steps":[
        {"label":"Set up","content":"<p>The two legs are 9 and 12; the direct distance is the hypotenuse.</p>"},
        {"label":"Pythagoras","content":"<p>\\(9^2 + 12^2 = 81 + 144 = 225\\)</p>"},
        {"label":"Check","content":"<p>\\(\\sqrt{225} = 15\\), and \\(15^2 = 225\\) ✓</p>"},
        {"label":"Answer","content":"<p>\\(15\\) km</p>","isAnswer":True,"is_answer":True}
      ]
    }
  }
}

# ---------- method_card (trim to <=4 steps, <=140 words) --------------------
pd["method_card"] = {
  "title":"How to Use Pythagoras & SOHCAHTOA",
  "steps":[
    "Label the sides: hypotenuse (longest, opposite the right angle), then opposite and adjacent relative to the angle.",
    "Two sides and no angle: use Pythagoras. An angle is involved: use SOHCAHTOA.",
    "Substitute and solve: square root for Pythagoras, or inverse trig for an angle. Keep the calculator in degrees."
  ],
  "content":"<p><strong>Pythagoras:</strong> in a right-angled triangle \\(a^2 + b^2 = c^2\\), where \\(c\\) is the hypotenuse. Find the hypotenuse with \\(c = \\sqrt{a^2 + b^2}\\); find a shorter side with \\(a = \\sqrt{c^2 - b^2}\\).</p><p><strong>SOHCAHTOA:</strong> \\(\\sin\\theta = \\frac{O}{H}\\), \\(\\cos\\theta = \\frac{A}{H}\\), \\(\\tan\\theta = \\frac{O}{A}\\). To find a side, rearrange; to find an angle, use \\(\\sin^{-1}\\), \\(\\cos^{-1}\\) or \\(\\tan^{-1}\\).</p>",
  "example":"<p><strong>Find the hypotenuse of a right triangle with sides 5 cm and 12 cm.</strong></p><p>\\(c = \\sqrt{5^2 + 12^2} = \\sqrt{25 + 144} = \\sqrt{169} = 13\\) cm</p>"
}

# preserve topic_links, related_videos, worked_examples untouched (already in pd)

json.dump(pd, io.open(OUT,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", OUT)
# sanity: em dash scan
import re
raw = io.open(OUT,encoding="utf-8").read()
print("em dashes:", raw.count("—"))
