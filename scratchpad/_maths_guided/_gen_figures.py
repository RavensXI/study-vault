# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for geometry-L05 and write new practice_data."""
import io, json, math

LIVE = "_live_L05.json"
OUT = "lesson_geometry-L05_diagrams.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))[0]["practice_data"]

# Canonical right triangle geometry (viewBox 0 0 240 168)
A = (40, 134)   # angle theta vertex (bottom-left)
B = (178, 134)  # right-angle vertex (bottom-right)
C = (178, 30)   # top vertex

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def right_triangle(adj_lbl, opp_lbl, hyp_lbl, angle_lbl, aria):
    """adj = horizontal bottom (AB), opp = vertical right (BC), hyp = AC.
    angle_lbl at A (or None). Returns svg string."""
    parts = []
    parts.append(
        '<svg viewBox="0 0 240 168" role="img" aria-label="%s" '
        'style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%%">' % esc(aria))
    # triangle
    parts.append(
        '<polygon points="%d,%d %d,%d %d,%d" fill="#60a5fa" fill-opacity="0.15" '
        'stroke="currentColor" stroke-width="1.6"/>' % (A[0], A[1], B[0], B[1], C[0], C[1]))
    # right-angle square at B
    parts.append(
        '<path d="M%d,%d h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
        % (B[0]-11, B[1]-11))
    # angle arc + label at A
    if angle_lbl:
        r = 24
        acx, acy = A
        ux, uy = (C[0]-A[0]), (C[1]-A[1])
        ln = math.hypot(ux, uy)
        ux, uy = ux/ln, uy/ln
        sx, sy = acx + r, acy
        ex, ey = acx + r*ux, acy + r*uy
        parts.append(
            '<path d="M%.1f,%.1f A%d,%d 0 0 0 %.1f,%.1f" fill="none" '
            'stroke="currentColor" stroke-width="1.2"/>' % (sx, sy, r, r, ex, ey))
        parts.append(
            '<text x="70" y="129" font-family="Inter,sans-serif" font-size="11" '
            'fill="currentColor">%s</text>' % esc(angle_lbl))
    # side labels
    if adj_lbl:
        parts.append(
            '<text x="109" y="152" font-family="Inter,sans-serif" font-size="11" '
            'fill="currentColor" text-anchor="middle">%s</text>' % esc(adj_lbl))
    if opp_lbl:
        parts.append(
            '<text x="184" y="86" font-family="Inter,sans-serif" font-size="11" '
            'fill="currentColor" text-anchor="start">%s</text>' % esc(opp_lbl))
    if hyp_lbl:
        parts.append(
            '<text x="98" y="70" font-family="Inter,sans-serif" font-size="11" '
            'fill="currentColor" text-anchor="middle">%s</text>' % esc(hyp_lbl))
    parts.append("</svg>")
    return "".join(parts)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def prepend(prob, svg):
    prob["display"] = svg + CAP + prob["display"]

pb = pd["problem_bank"]
added = []

def add(tier, i, svg, kind, what):
    prepend(pb[tier][i], svg)
    added.append({"tier": tier, "index": i, "kind": kind, "what": what})

# ---- BRONZE ----
add("bronze", 0, right_triangle("3 cm", "4 cm", "? cm", None,
    "Right-angled triangle with two shorter sides 3 cm and 4 cm and hypotenuse marked with a question mark"),
    "svg", "Pythagoras triangle, legs 3 and 4, hypotenuse ?")
add("bronze", 1, right_triangle("7 cm", "24 cm", "? cm", None,
    "Right-angled triangle with two shorter sides 7 cm and 24 cm and hypotenuse marked with a question mark"),
    "svg", "Pythagoras triangle, legs 7 and 24, hypotenuse ?")
add("bronze", 2, right_triangle("8 cm", "15 cm", "? cm", None,
    "Right-angled triangle with two shorter sides 8 cm and 15 cm and hypotenuse marked with a question mark"),
    "svg", "Pythagoras triangle, legs 8 and 15, hypotenuse ?")
add("bronze", 3, right_triangle("6 cm", "? cm", "10 cm", None,
    "Right-angled triangle with hypotenuse 10 cm, one shorter side 6 cm and the other shorter side marked with a question mark"),
    "svg", "Pythagoras triangle, hyp 10, leg 6, other leg ?")
add("bronze", 4, right_triangle("10 cm", "? cm", "26 cm", None,
    "Right-angled triangle with hypotenuse 26 cm, one shorter side 10 cm and the other shorter side marked with a question mark"),
    "svg", "Pythagoras triangle, hyp 26, leg 10, other leg ?")
add("bronze", 5, right_triangle("", "?", "20 cm", "30°",
    "Right-angled triangle with a 30 degree angle, hypotenuse 20 cm and the opposite side marked with a question mark"),
    "svg", "Trig triangle, angle 30, hyp 20, opposite ?")
add("bronze", 6, right_triangle("?", "", "14 cm", "60°",
    "Right-angled triangle with a 60 degree angle, hypotenuse 14 cm and the adjacent side marked with a question mark"),
    "svg", "Trig triangle, angle 60, hyp 14, adjacent ?")
add("bronze", 7, right_triangle("12", "5", "", "θ",
    "Right-angled triangle with opposite side 5 and adjacent side 12, angle theta marked between the adjacent side and hypotenuse"),
    "svg", "Trig triangle, opp 5, adj 12, angle theta ?")

# ---- SILVER ----
add("silver", 0, right_triangle("b = 5", "a = ?", "c = 13", None,
    "Right-angled triangle with hypotenuse c equals 13, one shorter side b equals 5 and the other shorter side a marked with a question mark"),
    "svg", "Pythagoras triangle, c=13, b=5, a=?")
add("silver", 1, right_triangle("6 cm", "8 cm", "", "θ",
    "Right-angled triangle with opposite side 8 cm and adjacent side 6 cm, angle theta marked"),
    "svg", "Trig triangle, opp 8, adj 6, angle theta ?")
add("silver", 2, right_triangle("?", "", "12 cm", "40°",
    "Right-angled triangle with a 40 degree angle, hypotenuse 12 cm and the adjacent side marked with a question mark"),
    "svg", "Trig triangle, angle 40, hyp 12, adjacent ?")
add("silver", 3, right_triangle("10 cm", "?", "", "35°",
    "Right-angled triangle with a 35 degree angle, adjacent side 10 cm and the opposite side marked with a question mark"),
    "svg", "Trig triangle, angle 35, adj 10, opposite ?")
add("silver", 4, right_triangle("2 m", "? m", "6 m", None,
    "A ladder 6 m long as the hypotenuse of a right-angled triangle, its base 2 m from the wall and the height up the wall marked with a question mark"),
    "svg", "Ladder triangle, ladder 6, base 2, height ?")
add("silver", 5, right_triangle("", "12 cm", "20 cm", "θ",
    "Right-angled triangle with opposite side 12 cm, hypotenuse 20 cm and angle theta marked"),
    "svg", "Trig triangle, opp 12, hyp 20, angle theta ?")

# silver6: isosceles triangle with height line
def isosceles_svg():
    apex = (120, 28); bl = (46, 134); br = (194, 134); foot = (120, 134)
    p = []
    p.append('<svg viewBox="0 0 240 168" role="img" aria-label="Isosceles triangle with two equal sides of 10 cm, base 12 cm, and a dashed height line to the base marked with a question mark" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">')
    p.append('<polygon points="%d,%d %d,%d %d,%d" fill="#34d399" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>' % (apex[0],apex[1],bl[0],bl[1],br[0],br[1]))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>' % (apex[0],apex[1],foot[0],foot[1]))
    # right-angle square at foot
    p.append('<path d="M%d,%d v-11 h11" fill="none" stroke="currentColor" stroke-width="1.2"/>' % (foot[0]-11, foot[1]))
    # tick marks on equal sides
    def tick(x1,y1,x2,y2):
        mx,my=(x1+x2)/2,(y1+y2)/2
        dx,dy=x2-x1,y2-y1; ln=math.hypot(dx,dy); nx,ny=-dy/ln,dx/ln
        return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.4"/>'%(mx-nx*4,my-ny*4,mx+nx*4,my+ny*4)
    p.append(tick(apex[0],apex[1],bl[0],bl[1]))
    p.append(tick(apex[0],apex[1],br[0],br[1]))
    p.append('<text x="72" y="76" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">10 cm</text>')
    p.append('<text x="168" y="76" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">10 cm</text>')
    p.append('<text x="120" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">12 cm</text>')
    p.append('<text x="126" y="92" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">?</text>')
    p.append('</svg>')
    return "".join(p)
add("silver", 6, isosceles_svg(), "svg", "Isosceles triangle, equal sides 10, base 12, height ?")

# ---- GOLD ----
add("gold", 0, right_triangle("15 km", "20 km", "? km", None,
    "Right-angled triangle with a 15 km horizontal leg east, a 20 km vertical leg north and the direct distance as the hypotenuse marked with a question mark"),
    "svg", "Ship path triangle, east 15, north 20, direct ?")
add("gold", 1, right_triangle("50 m", "30 m", "", "θ",
    "Right-angled triangle with horizontal distance 50 m, tower height 30 m and the angle of elevation theta marked at the ground"),
    "svg", "Elevation triangle, adj 50, opp 30, angle theta ?")
add("gold", 2, right_triangle("x", "x + 1", "x + 2", None,
    "Right-angled triangle with shorter sides labelled x and x plus 1 and hypotenuse labelled x plus 2"),
    "svg", "Algebraic Pythagoras triangle, legs x and x+1, hyp x+2")

# gold3: cliff, angle of depression
def cliff_svg():
    T=(46,30); Bs=(46,134); P=(206,134)
    p=[]
    p.append('<svg viewBox="0 0 240 168" role="img" aria-label="A 40 m vertical cliff with a horizontal dashed line from the top, an angle of depression of 25 degrees down to a boat, and the horizontal distance to the boat marked with a question mark" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">')
    p.append('<polygon points="%d,%d %d,%d %d,%d" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'%(T[0],T[1],Bs[0],Bs[1],P[0],P[1]))
    # horizontal dashed line of sight reference from top
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>'%(T[0],T[1],P[0],T[1]))
    # right angle at base of cliff
    p.append('<path d="M%d,%d h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>'%(Bs[0],Bs[1]-11))
    # angle of depression arc at T between horizontal (+x) and TP
    r=26; ux,uy=(P[0]-T[0]),(P[1]-T[1]); ln=math.hypot(ux,uy); ux,uy=ux/ln,uy/ln
    p.append('<path d="M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f" fill="none" stroke="currentColor" stroke-width="1.2"/>'%(T[0]+r,T[1],r,r,T[0]+r*ux,T[1]+r*uy))
    p.append('<text x="78" y="46" font-family="Inter,sans-serif" font-size="11" fill="currentColor">25°</text>')
    p.append('<text x="34" y="86" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">40 m</text>')
    p.append('<text x="126" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">? m</text>')
    # boat marker
    p.append('<text x="212" y="138" font-family="Inter,sans-serif" font-size="12" fill="currentColor">⛵</text>')
    p.append('</svg>')
    return "".join(p)
add("gold", 3, cliff_svg(), "svg", "Cliff, height 40, depression 25 deg, distance ?")

# gold4: rectangle with diagonal
def rect_svg():
    x0,y0,x1,y1=34,34,206,124
    p=[]
    p.append('<svg viewBox="0 0 240 158" role="img" aria-label="A rectangle with width 8 cm, a diagonal of 17 cm drawn corner to corner, and the length marked with a question mark" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">')
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'%(x0,y0,x1-x0,y1-y0))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>'%(x0,y1,x1,y0))
    # right angle at bottom-left
    p.append('<path d="M%d,%d h11 v-11" fill="none" stroke="currentColor" stroke-width="1.2"/>'%(x0,y1))
    p.append('<text x="26" y="82" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">8 cm</text>')
    p.append('<text x="120" y="140" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">? cm</text>')
    p.append('<text x="128" y="72" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">17 cm</text>')
    p.append('</svg>')
    return "".join(p)
add("gold", 4, rect_svg(), "svg", "Rectangle, width 8, diagonal 17, length ?")

# ---- Opener: make text fills theme-safe (currentColor) ----
op = pd["guided"]["opener"]
before = op["display"]
op["display"] = op["display"].replace('fill="#2d2a26"', 'fill="currentColor"').replace('stroke="#2d2a26"', 'stroke="currentColor"')
opener_touched = op["display"] != before

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("figures added:", len(added))
print("opener_touched:", opener_touched)
for a in added:
    print(" ", a["tier"], a["index"], a["what"])
