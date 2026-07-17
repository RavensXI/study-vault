# -*- coding: utf-8 -*-
"""Build guided-learning + diagrams practice_data for maths-aqa geometry-L07 (Circle Theorems)."""
import json, io, math

def P(deg, R, cx=120, cy=84):
    return (cx + R*math.cos(math.radians(deg)), cy - R*math.sin(math.radians(deg)))

def L(x1,y1,x2,y2,w=1.6):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="{w}"/>'
def CIRC(cx,cy,R):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
def DOT(x,y):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="currentColor"/>'
def T(x,y,s,size=12,anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="600" fill="currentColor">{s}</text>'
def RASQ(vx,vy, ax,ay, bx,by, s=9):
    d1=(ax-vx,ay-vy); l1=math.hypot(*d1); u1=(d1[0]/l1,d1[1]/l1)
    d2=(bx-vx,by-vy); l2=math.hypot(*d2); u2=(d2[0]/l2,d2[1]/l2)
    p1=(vx+u1[0]*s, vy+u1[1]*s); p2=(vx+(u1[0]+u2[0])*s, vy+(u1[1]+u2[1])*s); p3=(vx+u2[0]*s, vy+u2[1]*s)
    return f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="currentColor" stroke-width="1.3"/>'
def POLY(pts, fill="#60a5fa"):
    s=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    return f'<polygon points="{s}" fill="{fill}" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6"/>'
def SVG(aria, body, w=240, h=160):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">{body}</svg>')
CAP = '<span class="figure-caption">Diagram not drawn accurately</span> '

# ---- figure templates ----
def fig_centre_circ(center_lbl, circ_lbl, aria):
    O=(120,84); R=52
    A=P(212,R); B=P(328,R); C=P(90,R)
    b = CIRC(*O,R)
    b += L(*O,*A)+L(*O,*B)+L(*C,*A)+L(*C,*B)
    b += DOT(*O)+DOT(*A)+DOT(*B)+DOT(*C)
    b += T(120,98,"O",11)
    b += T(60,120,"A")+T(180,120,"B")+T(120,24,"C")
    b += T(120,112,center_lbl)          # between radii, below O
    b += T(120,50,circ_lbl)             # just below C
    return SVG(aria,b)

def fig_semicircle(aA,aB,aC,right_at_C,aria):
    O=(120,84); R=52
    A=P(180,R); B=P(0,R); C=P(64,R)
    b = CIRC(*O,R)
    b += L(*A,*B)+L(*C,*A)+L(*C,*B)
    b += DOT(*O)+DOT(*A)+DOT(*B)+DOT(*C)
    if right_at_C: b += RASQ(C[0],C[1], A[0],A[1], B[0],B[1])
    b += T(56,88,"A")+T(184,88,"B")+T(150,30,"C")+T(112,96,"O",10)
    if aA: b += T(86,80,aA)
    if aB: b += T(156,80,aB)
    if aC: b += T(132,54,aC)
    return SVG(aria,b)

def fig_cyclic(lA,lB,lC,lD,aria):
    O=(120,82); R=54
    A=P(128,R,120,82); B=P(52,R,120,82); C=P(308,R,120,82); D=P(232,R,120,82)
    b = CIRC(120,82,R)
    b += POLY([A,B,C,D])
    b += DOT(*A)+DOT(*B)+DOT(*C)+DOT(*D)
    b += T(76,32,"A")+T(164,32,"B")+T(166,136,"C")+T(74,136,"D")
    b += T(99,55,lA)+T(141,55,lB)+T(141,113,lC)+T(99,113,lD)
    return SVG(aria,b)

# s1: tangent-chord + alternate segment (no centre)
def fig_ts_alt(tc_lbl, alt_lbl, aria):
    O=(120,80); R=50
    A=P(270,R); B=P(38,R); C=P(150,R)
    b = CIRC(*O,R)
    b += L(64,A[1],176,A[1])            # tangent through A (horizontal)
    b += L(*A,*B)+L(*C,*A)+L(*C,*B)
    b += DOT(*A)+DOT(*B)+DOT(*C)
    b += T(120,A[1]+14,"A")+T(B[0]+10,B[1]-2,"B")+T(C[0]-11,C[1]-2,"C")
    b += T(138,A[1]-9,tc_lbl,11)
    b += T(C[0]+16,C[1]+14,alt_lbl,11)
    return SVG(aria,b)

# s5: tangent-chord + centre angle
def fig_ts_centre(tc_lbl, centre_lbl, aria):
    O=(120,78); R=48
    A=P(270,R,120,78); B=P(40,R,120,78)
    b = CIRC(120,78,R)
    b += L(66,A[1],174,A[1])            # tangent
    b += L(*A,*B)+L(120,78,A[0],A[1])+L(120,78,B[0],B[1])
    b += DOT(120,78)+DOT(*A)+DOT(*B)
    b += T(120,A[1]+14,"A")+T(B[0]+11,B[1]-1,"B")+T(108,80,"O",10)
    b += T(138,A[1]-9,tc_lbl,11)
    b += T(120,64,centre_lbl,11)
    return SVG(aria,b)

# g2: tangent PT at T, chord TA, point B in alternate segment
def fig_tangent_named(tc_lbl, aria):
    O=(120,78); R=48
    Tp=P(270,R,120,78); A=P(158,R,120,78); B=P(22,R,120,78)
    b = CIRC(120,78,R)
    b += L(58,Tp[1],176,Tp[1])          # tangent, P end to left
    b += L(*Tp,*A)+L(*B,*Tp)+L(*B,*A)
    b += DOT(*Tp)+DOT(*A)+DOT(*B)
    b += T(62,Tp[1]-4,"P")+T(120,Tp[1]+14,"T")+T(A[0]-10,A[1]-2,"A")+T(B[0]+11,B[1]-1,"B")
    b += T(100,Tp[1]-9,tc_lbl,11)
    b += T(B[0]-14,B[1]+13,"?",12)
    return SVG(aria,b)

# g0/g4/teach-gold: isosceles radii, C on major or minor arc
def fig_iso_radii(oab_lbl, acb_lbl, minor_arc, aria):
    O=(120,80); R=52
    if minor_arc:
        A=P(205,R,120,80); B=P(335,R,120,80); C=P(270,R,120,80)
    else:
        A=P(200,R,120,80); B=P(340,R,120,80); C=P(90,R,120,80)
    b = CIRC(120,80,R)
    b += L(120,80,A[0],A[1])+L(120,80,B[0],B[1])+L(*C,*A)+L(*C,*B)+L(*A,*B)
    b += DOT(120,80)+DOT(*A)+DOT(*B)+DOT(*C)
    b += T(A[0]-9,A[1]+4,"A")+T(B[0]+9,B[1]+4,"B")+T(112,84,"O",10)
    if minor_arc:
        b += T(C[0],C[1]+14,"C")+T(C[0],C[1]-8,acb_lbl,11)
    else:
        b += T(C[0],C[1]-6,"C")+T(C[0],C[1]+18,acb_lbl,11)
    b += T(A[0]+16,A[1]-2,oab_lbl,11)
    return SVG(aria,b)

# s3: two tangents from external point
def fig_two_tangents(ta_lbl, tb_lbl, aria):
    O=(150,84); R=42
    Tp=(40,84)
    A=P(148,R,150,84); B=P(212,R,150,84)
    b = CIRC(*O,R)
    b += L(*Tp,*A)+L(*Tp,*B)
    b += DOT(*Tp)+DOT(*A)+DOT(*B)+DOT(*O)
    b += T(32,88,"T")+T(A[0]-2,A[1]-6,"A")+T(B[0]-2,B[1]+14,"B")+T(158,88,"O",10)
    b += T((Tp[0]+A[0])/2,(Tp[1]+A[1])/2-6,ta_lbl,11)
    b += T((Tp[0]+B[0])/2,(Tp[1]+B[1])/2+13,tb_lbl,11)
    return SVG(aria,b)

# s6: triangle inscribed
def fig_tri_in_circle(aA,aB,aC,aria):
    O=(120,84); R=54
    A=P(150,R); B=P(30,R); C=P(270,R)
    b = CIRC(*O,R)
    b += POLY([A,B,C])
    b += DOT(*A)+DOT(*B)+DOT(*C)
    b += T(A[0]-10,A[1]-2,"A")+T(B[0]+10,B[1]-2,"B")+T(C[0],C[1]+15,"C")
    b += T(A[0]+15,A[1]+11,aA,11)+T(B[0]-15,B[1]+11,aB,11)+T(C[0],C[1]-9,aC,11)
    return SVG(aria,b)

# s4: reflex angle at centre
def fig_reflex(given_lbl, reflex_lbl, aria):
    O=(120,84); R=50
    B=P(203,R); C=P(337,R)
    b = CIRC(*O,R)
    b += L(*O,*B)+L(*O,*C)
    b += DOT(*O)+DOT(*B)+DOT(*C)
    b += T(B[0]-9,B[1]+4,"B")+T(C[0]+9,C[1]+4,"C")+T(112,88,"O",10)
    b += T(120,116,given_lbl,11)        # obtuse below
    b += T(120,58,reflex_lbl,11)        # reflex above
    return SVG(aria,b)

# b5: tangent meets radius
def fig_tan_radius(aria):
    O=(120,80); R=48
    A=P(270,R,120,80)
    b = CIRC(120,80,R)
    b += L(120,80,A[0],A[1])            # radius
    b += L(70,A[1],170,A[1])            # tangent
    b += DOT(120,80)+DOT(*A)
    b += T(110,78,"O",11)+T(120,A[1]+15,"T")
    b += T(133,A[1]-8,"?",12)
    return SVG(aria,b)

# ============ BANK ============
bronze = [
 {"display": fig_centre_circ("124°","?","Angle at the centre and at the circumference on the same arc")+CAP+
   "The angle at the centre of a circle is \\(124°\\). Find the angle at the circumference subtended by the same arc.",
  "solutions":[62],"calculator":False,"input_type":"single_value",
  "hint":"The angle at the circumference is half the angle at the centre.",
  "misconceptions":[{"pattern":"doubled_not_halved","expect":248,
    "message":"The angle at the circumference is HALF the angle at the centre, not double. 124 ÷ 2 = 62°."}],
  "guided_steps":[
    {"say":"The angle at the centre is twice the angle at the circumference on the same arc."},
    {"pre":"How many circumference angles make the centre angle? Type the multiplier: ","post":"","answer":2,"hint":"The centre angle is TWICE the circumference angle."},
    {"pre":"So circumference = 124 ÷ 2 = ","post":"","answer":62,"hint":"124 shared into 2.","phase":"substitute"},
    {"pre":"Check by doubling back: 62 × 2 = ","post":"","answer":124,"hint":"Twice 62 should return the centre angle.","done":"Back to 124°, so 62° is correct."}]},

 {"display": fig_centre_circ("?","48°","Angle at the circumference and at the centre on the same arc")+CAP+
   "The angle at the circumference is \\(48°\\). Find the angle at the centre subtended by the same arc.",
  "solutions":[96],"calculator":False,"input_type":"single_value",
  "hint":"The angle at the centre is twice the angle at the circumference.",
  "misconceptions":[{"pattern":"halved_not_doubled","expect":24,
    "message":"The angle at the centre is TWICE the angle at the circumference. 48 × 2 = 96°."}],
  "guided_steps":[
    {"say":"The angle at the centre is twice the angle at the circumference on the same arc."},
    {"pre":"Type the multiplier linking centre to circumference: ","post":"","answer":2,"hint":"The centre is TWICE the circumference."},
    {"pre":"So centre = 48 × 2 = ","post":"","answer":96,"hint":"Double 48.","phase":"substitute"},
    {"pre":"Check by halving: 96 ÷ 2 = ","post":"","answer":48,"hint":"Half of 96 returns the circumference angle.","done":"Back to 48°, so 96° is right."}]},

 {"display": fig_semicircle("","","?",False,"AB a diameter with C on the circle, angle ACB unknown")+CAP+
   "AB is a diameter. C is on the circumference. Find angle ACB.",
  "solutions":[90],"calculator":False,"input_type":"single_value",
  "hint":"The angle in a semicircle is always a right angle.",
  "misconceptions":[{"pattern":"used_straight_line","expect":180,
    "message":"A diameter is a straight line (180°), but the angle at C on the circle is half of that. The angle in a semicircle is 90°."}],
  "guided_steps":[
    {"say":"AB is a diameter, so C sits in a semicircle."},
    {"pre":"A diameter is a straight line. How many degrees is a straight line? ","post":"","answer":180,"hint":"Half a full turn."},
    {"pre":"The angle in the semicircle is half of that: 180 ÷ 2 = ","post":"","answer":90,"hint":"Half of 180.","phase":"substitute"},
    {"pre":"So angle ACB is a right angle. Type it: ","post":"","answer":90,"hint":"You just found it.","done":"90°, and it is 90° wherever C sits on the arc."}]},

 {"display": fig_cyclic("72°","","?","","A cyclic quadrilateral with one angle and its opposite marked")+CAP+
   "In a cyclic quadrilateral, one angle is \\(72°\\). Find the opposite angle.",
  "solutions":[108],"calculator":False,"input_type":"single_value",
  "hint":"Opposite angles of a cyclic quadrilateral add up to 180 degrees.",
  "misconceptions":[{"pattern":"thought_equal","expect":72,
    "message":"Opposite angles of a cyclic quadrilateral add to 180°, they are not equal. 180 − 72 = 108°."}],
  "guided_steps":[
    {"say":"Opposite angles of a cyclic quadrilateral add up to 180°."},
    {"pre":"What total do the opposite pair make? ","post":"","answer":180,"hint":"Cyclic quadrilateral opposite angles sum to this."},
    {"pre":"So the opposite angle = 180 − 72 = ","post":"","answer":108,"hint":"180 take away 72.","phase":"substitute"},
    {"pre":"Check the pair: 72 + 108 = ","post":"","answer":180,"hint":"Add the pair back.","done":"They sum to 180°, so 108° is right."}]},

 {"display": fig_ts_alt("","","Two points on the same arc subtending a chord")+  # replaced below
   "",
  "solutions":[35],"calculator":False,"input_type":"single_value",
  "hint":"Angles in the same segment are equal.",
  "misconceptions":[{"pattern":"thought_supplementary","expect":145,
    "message":"Angles in the same segment are equal, not supplementary. They stand on the same chord, so x = 35°."}],
  "guided_steps":[
    {"say":"Angles in the same segment, standing on the same chord, are equal."},
    {"pre":"Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary: ","post":"","answer":1,"hint":"Same-segment angles are equal."},
    {"pre":"They are equal, and one is 35°, so x = ","post":"","answer":35,"hint":"Copy the equal angle.","phase":"substitute"},
    {"pre":"Check the pair match: 35 and ","post":"","answer":35,"hint":"They must be the same.","done":"Equal, so x = 35°."}]},

 {"display": fig_tan_radius("A tangent meeting a radius at the point of contact")+CAP+
   "A tangent meets a radius at point T. The angle between them is:",
  "options":["90°","180°","45°","It depends on the circle"],
  "solutions":[0],"calculator":False,"input_type":"multiple_choice",
  "hint":"A tangent always meets the radius at a right angle.",
  "misconceptions":[]},

 {"display": fig_centre_circ("150°","?","Angle at the centre and at the circumference on the same arc")+CAP+
   "The angle at the centre is \\(150°\\). Find the angle at the circumference.",
  "solutions":[75],"calculator":False,"input_type":"single_value",
  "hint":"Halve the angle at the centre to get the angle at the circumference.",
  "misconceptions":[{"pattern":"doubled_not_halved","expect":300,
    "message":"The circumference angle is half the centre angle: 150 ÷ 2 = 75°. Doubling gives 300, which is more than a straight line."}],
  "guided_steps":[
    {"say":"The angle at the centre is twice the angle at the circumference on the same arc."},
    {"pre":"Type the multiplier linking them: ","post":"","answer":2,"hint":"The centre is TWICE the circumference."},
    {"pre":"So circumference = 150 ÷ 2 = ","post":"","answer":75,"hint":"150 shared into 2.","phase":"substitute"},
    {"pre":"Check by doubling: 75 × 2 = ","post":"","answer":150,"hint":"Twice 75.","done":"Back to 150°, so 75° is correct."}]},

 {"display": fig_semicircle("32°","?","",True,"Right-angled triangle in a semicircle, angle at A is 32 degrees")+CAP+
   "Angle ACB = \\(90°\\) (C on the circle, AB is a diameter). Angle BAC = \\(32°\\). Find angle ABC.",
  "solutions":[58],"calculator":False,"input_type":"single_value",
  "hint":"The right angle is 90; the three angles of the triangle add to 180.",
  "misconceptions":[{"pattern":"forgot_right_angle","expect":148,
    "message":"Angle ACB is 90° (angle in a semicircle). Use all three: 180 − 90 − 32 = 58°. Forgetting the 90 gives 148."}],
  "guided_steps":[
    {"say":"Angle ACB is 90° (angle in the semicircle). The three angles of triangle ACB add to 180°."},
    {"pre":"Add the two known angles: 90 + 32 = ","post":"","answer":122,"hint":"90 plus 32."},
    {"pre":"Subtract from 180: 180 − 122 = ","post":"","answer":58,"hint":"180 take away 122.","phase":"substitute"},
    {"pre":"Check all three: 90 + 32 + 58 = ","post":"","answer":180,"hint":"Add the three angles back.","done":"Back to 180°, so ABC = 58°."}]},
]

silver = [
 {"display": fig_cyclic("3x","2x + 10","x + 40","100°","A cyclic quadrilateral with four angles in terms of x")+CAP+
   "A cyclic quadrilateral has angles \\(3x\\), \\(2x + 10\\), \\(x + 40\\) and \\(100°\\). The angles \\(3x\\) and \\(x + 40\\) are opposite. Find \\(x\\).",
  "solutions":[35],"calculator":False,"input_type":"single_value",
  "hint":"Add the opposite pair 3x and x + 40 and set it equal to 180.",
  "misconceptions":[{"pattern":"wrong_pair","expect":34,
    "message":"Use the OPPOSITE pair 3x and x + 40, which sum to 180: 4x + 40 = 180, so x = 35. Pairing 3x with the adjacent 2x + 10 gives x = 34."}],
  "guided_steps":[
    {"say":"Opposite angles of a cyclic quadrilateral add to 180°. Here 3x and x + 40 are the opposite pair."},
    {"pre":"Add the opposite pair's x terms: 3x + x = ","post":"x","answer":4,"hint":"3 lots plus 1 lot of x."},
    {"pre":"The number part is 40, so 4x + 40 = 180. Take 40 across: 180 − 40 = ","post":"","answer":140,"hint":"180 take away 40."},
    {"pre":"Now 4x = 140, so x = 140 ÷ 4 = ","post":"","answer":35,"hint":"140 shared into 4.","phase":"substitute"},
    {"pre":"Check the pair: 3(35) + (35 + 40) = 105 + 75 = ","post":"","answer":180,"hint":"Work out both angles and add.","done":"They sum to 180°, so x = 35."}]},

 {"display": fig_ts_alt("64°","?","Tangent and chord with the angle in the alternate segment")+CAP+
   "The angle between a tangent and a chord at the point of contact is \\(64°\\). Find the angle in the alternate segment.",
  "solutions":[64],"calculator":False,"input_type":"single_value",
  "hint":"The tangent-chord angle equals the angle in the alternate segment.",
  "misconceptions":[{"pattern":"supplement","expect":116,
    "message":"The alternate segment angle EQUALS the tangent-chord angle, it is not supplementary. So it is 64°, not 116."}],
  "guided_steps":[
    {"say":"The alternate segment theorem: the angle between a tangent and a chord equals the angle in the alternate segment."},
    {"pre":"Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary: ","post":"","answer":1,"hint":"Alternate segment means equal."},
    {"pre":"They are equal, and the tangent-chord angle is 64°, so the alternate segment angle = ","post":"","answer":64,"hint":"Copy the 64.","phase":"substitute"},
    {"pre":"Check the pair are equal: 64 and ","post":"","answer":64,"hint":"They must match.","done":"Equal by the alternate segment theorem, so 64°."}]},

 {"display": fig_centre_circ("x + 50","x","Angle at the centre x plus 50 and at the circumference x")+CAP+
   "O is the centre. Angle AOB = \\(x + 50\\). Angle ACB = \\(x\\) (C on the circumference, same arc). Find \\(x\\).",
  "solutions":[50],"calculator":False,"input_type":"single_value",
  "hint":"Write centre = twice circumference: x + 50 = 2x.",
  "misconceptions":[{"pattern":"forgot_factor_two","expect":None,
    "message":"The angle at the centre is twice the circumference angle: x + 50 = 2x, so x = 50. Setting them equal (forgetting the factor of 2) has no solution."}],
  "guided_steps":[
    {"say":"The angle at the centre is twice the angle at the circumference on the same arc: x + 50 = 2x."},
    {"pre":"Take one x from each side. 2x − x leaves how many x? ","post":"x","answer":1,"hint":"2 lots take away 1 lot."},
    {"pre":"So 50 = x, meaning x = ","post":"","answer":50,"hint":"The equation says x equals 50.","phase":"substitute"},
    {"pre":"Check the centre angle: x + 50 = 50 + 50 = ","post":"","answer":100,"hint":"Substitute x = 50 into x + 50."},
    {"pre":"And twice the circumference: 2 × 50 = ","post":"","answer":100,"hint":"Double the circumference angle.","done":"Both give 100°, so x = 50."}]},

 {"display": fig_two_tangents("12 cm","?","Two tangents from an external point T")+CAP+
   "Two tangents from an external point T touch the circle at A and B. TA = \\(12\\) cm. Find TB.",
  "solutions":[12],"calculator":False,"input_type":"single_value",
  "hint":"Two tangents from the same point are equal in length.",
  "misconceptions":[{"pattern":"equal_tangents","expect":None,
    "message":"Two tangents from the same external point are equal, so TB = TA = 12 cm."}],
  "guided_steps":[
    {"say":"Two tangents drawn from the same external point are equal in length."},
    {"pre":"TA and TB come from the same point T. Type 1 if they are equal, 2 if not: ","post":"","answer":1,"hint":"Two tangents from a point are equal."},
    {"pre":"They are equal, and TA = 12 cm, so TB = ","post":"","answer":12,"hint":"Copy the length.","phase":"substitute"},
    {"pre":"Check the pair match: 12 and ","post":"","answer":12,"hint":"Both tangents equal.","done":"Equal, so TB = 12 cm."}]},

 {"display": fig_reflex("140°","?","Angle BOC at the centre with its reflex")+CAP+
   "O is the centre of the circle. Angle BOC = \\(140°\\). Find the reflex angle BOC.",
  "solutions":[220],"calculator":False,"input_type":"single_value",
  "hint":"The reflex angle is 360 minus the given angle.",
  "misconceptions":[{"pattern":"used_straight_line","expect":40,
    "message":"The reflex angle plus 140° make a full turn of 360°, so reflex = 360 − 140 = 220°. Using 180 − 140 = 40 treats it as a straight line, which it is not."}],
  "guided_steps":[
    {"say":"Angles around the centre point make a full turn of 360°. The reflex angle is the rest of the turn."},
    {"pre":"A full turn is: ","post":"","answer":360,"hint":"Angles around a point."},
    {"pre":"Reflex BOC = 360 − 140 = ","post":"","answer":220,"hint":"360 take away 140.","phase":"substitute"},
    {"pre":"Check they complete a turn: 140 + 220 = ","post":"","answer":360,"hint":"The two should make a full turn.","done":"A full 360°, so the reflex angle is 220°."}]},

 {"display": fig_ts_centre("52°","?","Tangent-chord angle with the angle at the centre")+CAP+
   "The angle between a tangent at A and chord AB is \\(52°\\). O is the centre. Find angle AOB.",
  "solutions":[104],"calculator":False,"input_type":"single_value",
  "hint":"Find the alternate segment angle first, then double it for the centre.",
  "misconceptions":[{"pattern":"forgot_double","expect":52,
    "message":"First the alternate segment angle is 52°. Then the angle at the CENTRE is twice that: 2 × 52 = 104°. Stopping at 52 forgets the centre step."}],
  "guided_steps":[
    {"say":"Alternate segment: the angle in the alternate segment equals the tangent-chord angle, 52°. Then the angle at the centre is twice the angle at the circumference."},
    {"pre":"Angle in the alternate segment = tangent-chord angle = ","post":"","answer":52,"hint":"They are equal."},
    {"pre":"Angle at the centre is twice that: 2 × 52 = ","post":"","answer":104,"hint":"Double 52.","phase":"substitute"},
    {"pre":"Check by halving: 104 ÷ 2 = ","post":"","answer":52,"hint":"Half the centre angle returns the circumference angle.","done":"Back to 52°, so AOB = 104°."}]},

 {"display": fig_tri_in_circle("40°","?","55°","A triangle inscribed in a circle with two angles given")+CAP+
   "Points A, B, C lie on a circle. Angle BAC = \\(40°\\) and angle BCA = \\(55°\\). Find angle ABC.",
  "solutions":[85],"calculator":False,"input_type":"single_value",
  "hint":"The three angles of the triangle add up to 180.",
  "misconceptions":[{"pattern":"added_not_subtracted","expect":95,
    "message":"The three angles of the triangle add to 180: ABC = 180 − 40 − 55 = 85°. Adding 40 + 55 gives 95, which is the pair total, not the missing angle."}],
  "guided_steps":[
    {"say":"A, B and C are just three angles of a triangle, which add to 180°."},
    {"pre":"Add the two known angles: 40 + 55 = ","post":"","answer":95,"hint":"40 plus 55."},
    {"pre":"Subtract from 180: 180 − 95 = ","post":"","answer":85,"hint":"180 take away 95.","phase":"substitute"},
    {"pre":"Check all three: 40 + 55 + 85 = ","post":"","answer":180,"hint":"Add the three angles back.","done":"Back to 180°, so ABC = 85°."}]},
]

gold = [
 {"display": fig_iso_radii("25°","?",False,"Triangle formed by two radii, with C on the major arc")+CAP+
   "O is the centre. A, B, C are on the circle. Angle OAB = \\(25°\\). Find angle ACB (C on the major arc).",
  "solutions":[65],"calculator":False,"input_type":"single_value",
  "hint":"Use the equal radii to find the centre angle, then halve it.",
  "misconceptions":[{"pattern":"forgot_halve","expect":130,
    "message":"Angle AOB at the centre is 130°, but ACB at the circumference is HALF of that: 130 ÷ 2 = 65°. Using 130 forgets to halve."}],
  "guided_steps":[
    {"say":"OA and OB are both radii, so triangle OAB is isosceles: the base angles are equal."},
    {"pre":"Base angles equal, so angle OBA = ","post":"","answer":25,"hint":"Same as angle OAB."},
    {"pre":"Angles in triangle OAB add to 180. Centre angle AOB = 180 − 25 − 25 = ","post":"","answer":130,"hint":"180 take away both 25s."},
    {"pre":"Angle at the circumference is half the centre: 130 ÷ 2 = ","post":"","answer":65,"hint":"Half of 130.","phase":"substitute"},
    {"pre":"Check by doubling: 65 × 2 = ","post":"","answer":130,"hint":"Twice ACB returns the centre angle.","done":"Back to 130°, so ACB = 65°."}]},

 {"display": fig_cyclic("","3x + 10","","2x + 20","Cyclic quadrilateral with two opposite angles in terms of x")+CAP+
   "A, B, C, D lie on a circle. Angle ABC = \\(3x + 10\\), angle ADC = \\(2x + 20\\). Find angle ABC.",
  "solutions":[100],"calculator":False,"input_type":"single_value",
  "hint":"Opposite angles sum to 180; form an equation in x.",
  "misconceptions":[{"pattern":"set_equal","expect":40,
    "message":"Opposite angles SUM to 180, they are not equal. 3x + 10 + 2x + 20 = 180 gives x = 30 and ABC = 100°. Setting the expressions equal gives x = 10 and ABC = 40."}],
  "guided_steps":[
    {"say":"ABC and ADC are opposite angles of the cyclic quadrilateral, so they add to 180°."},
    {"pre":"Add the x terms: 3x + 2x = ","post":"x","answer":5,"hint":"3 lots plus 2 lots of x."},
    {"pre":"Add the numbers: 10 + 20 = ","post":"","answer":30,"hint":"The two constants."},
    {"pre":"So 5x + 30 = 180. Take 30 across: 180 − 30 = ","post":"","answer":150,"hint":"180 take away 30."},
    {"pre":"Now 5x = 150, so x = 150 ÷ 5 = ","post":"","answer":30,"hint":"150 shared into 5.","phase":"substitute"},
    {"pre":"ABC = 3x + 10 = 3(30) + 10 = ","post":"","answer":100,"hint":"Substitute x = 30 into 3x + 10.","done":"ABC = 100°. Check: ADC = 2(30)+20 = 80, and 100 + 80 = 180."}]},

 {"display": fig_tangent_named("70°","Tangent PT at T with chord TA and point B in the alternate segment")+CAP+
   "PT is a tangent at T. A and B are on the circle. Angle PTA = \\(70°\\). Using the alternate segment theorem, find angle ABT.",
  "solutions":[70],"calculator":False,"input_type":"single_value",
  "hint":"The tangent-chord angle equals the angle in the alternate segment.",
  "misconceptions":[{"pattern":"supplement","expect":110,
    "message":"The alternate segment angle equals the tangent-chord angle, so ABT = 70°. It is not the supplement (110)."}],
  "guided_steps":[
    {"say":"The alternate segment theorem: the angle between tangent PT and chord TA equals the angle ABT in the alternate segment."},
    {"pre":"Equal or supplementary? Type 1 for equal, 2 for supplementary: ","post":"","answer":1,"hint":"Alternate segment angles are equal."},
    {"pre":"They are equal, and PTA = 70°, so ABT = ","post":"","answer":70,"hint":"Copy the 70.","phase":"substitute"},
    {"pre":"Check the pair match: 70 and ","post":"","answer":70,"hint":"Equal by the theorem.","done":"Equal, so ABT = 70°."}]},

 {"display": fig_semicircle("28°","?","",True,"Right-angled triangle in a semicircle with angle CAB 28 degrees")+CAP+
   "AB is a diameter of the circle. C is a point on the circle. Angle CAB = \\(28°\\). Find angle ABC.",
  "solutions":[62],"calculator":False,"input_type":"single_value",
  "hint":"The semicircle gives a 90 angle; then use the triangle sum.",
  "misconceptions":[{"pattern":"answered_semicircle","expect":90,
    "message":"90° is angle ACB (the semicircle right angle), not the angle asked. Put it in the triangle: 180 − 90 − 28 = 62°."}],
  "guided_steps":[
    {"say":"AB is a diameter, so angle ACB stands in a semicircle and equals 90°. Then use the triangle."},
    {"pre":"Angle ACB in the semicircle = ","post":"","answer":90,"hint":"Angle in a semicircle."},
    {"pre":"Triangle ACB adds to 180. Add the two known angles: 90 + 28 = ","post":"","answer":118,"hint":"90 plus 28."},
    {"pre":"Subtract from 180: 180 − 118 = ","post":"","answer":62,"hint":"180 take away 118.","phase":"substitute"},
    {"pre":"Check all three: 90 + 28 + 62 = ","post":"","answer":180,"hint":"Add the three angles.","done":"Back to 180°, so ABC = 62°."}]},

 {"display": fig_iso_radii("35°","?",True,"Triangle of two radii with C on the minor arc")+CAP+
   "O is the centre. A and B are on the circle. Angle OAB = \\(35°\\). C is on the minor arc. Find the obtuse angle ACB.",
  "solutions":[125],"calculator":False,"input_type":"single_value",
  "hint":"C is on the minor arc, so use the reflex angle at the centre.",
  "misconceptions":[{"pattern":"used_minor_central","expect":55,
    "message":"C is on the MINOR arc, so it stands on the REFLEX angle at the centre. AOB = 110°, reflex = 250°, and ACB = 250 ÷ 2 = 125°. Halving 110 gives 55, the wrong arc."}],
  "guided_steps":[
    {"say":"OA and OB are radii, so triangle OAB is isosceles. C is on the MINOR arc, so it stands on the reflex angle at the centre."},
    {"pre":"Base angles equal, so angle OBA = ","post":"","answer":35,"hint":"Same as angle OAB."},
    {"pre":"Centre angle AOB = 180 − 35 − 35 = ","post":"","answer":110,"hint":"180 take away both 35s."},
    {"pre":"C is on the minor arc, so use the reflex angle: 360 − 110 = ","post":"","answer":250,"hint":"A full turn take away 110.","phase":"substitute"},
    {"pre":"Angle ACB is half the reflex angle: 250 ÷ 2 = ","post":"","answer":125,"hint":"Half of 250.","done":"125°, which is obtuse as expected."}]},
]

# fix bronze[4] (same-segment) figure: needs a two-points-same-arc figure
def fig_same_segment(a1,a2,aria):
    O=(120,82); R=52
    A=P(220,R,120,82); B=P(320,R,120,82); Pp=P(140,R,120,82); Q=P(40,R,120,82)
    b=CIRC(120,82,R)
    b += L(*Pp,*A)+L(*Pp,*B)+L(*Q,*A)+L(*Q,*B)+L(*A,*B)
    b += DOT(*A)+DOT(*B)+DOT(*Pp)+DOT(*Q)
    b += T(A[0]-6,A[1]+13,"A")+T(B[0]+6,B[1]+13,"B")+T(Pp[0]-10,Pp[1]-2,"P")+T(Q[0]+10,Q[1]-2,"Q")
    b += T(Pp[0]+6,Pp[1]+15,a1,11)+T(Q[0]-6,Q[1]+15,a2,11)
    return SVG(aria,b)
bronze[4]["display"] = fig_same_segment("35°","x","Two angles in the same segment standing on chord AB")+CAP+\
    "Two angles in the same segment stand on the chord AB. One is \\(35°\\) and the other is \\(x\\). Find \\(x\\)."

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description":"One theorem applied in a single step to find a missing angle or length.",
 "silver_description":"One theorem giving a short equation, or two facts combined in a couple of steps.",
 "gold_description":"Several theorems chained together, often with an equation in x to solve.",
}

# ============ tier_guides ============
tier_guides = {
 "bronze":{"title":"Bronze: one theorem, one step",
   "steps":[
     "<strong>Angle at the centre</strong> is twice the angle at the circumference on the same arc: halve or double.",
     "<strong>Semicircle:</strong> the angle in a semicircle is 90°. <strong>Same segment:</strong> angles on the same chord are equal.",
     "<strong>Cyclic quadrilateral:</strong> opposite angles add to 180°. <strong>Tangents</strong> meet a radius at 90°, and two from a point are equal."],
   "example":{"question":"The angle at the centre is 100°. Find the angle at the circumference.",
     "steps":[{"label":"Rule","content":"Centre is twice the circumference."},
              {"label":"Halve","content":"100 ÷ 2 = 50"},
              {"label":"Check","content":"50 × 2 = 100 ✓"},
              {"label":"Answer","content":"50°","isAnswer":True,"is_answer":True}]}},
 "silver":{"title":"Silver: one equation or two facts",
   "steps":[
     "Turn the theorem into an equation: centre = 2 × circumference, or opposite angles sum to 180°.",
     "For the alternate segment, the tangent-chord angle equals the angle in the alternate segment.",
     "Solve the short equation, then substitute back to check."],
   "example":{"question":"A cyclic quadrilateral has opposite angles 2x and x + 30. Find x.",
     "steps":[{"label":"Set up","content":"2x + x + 30 = 180"},
              {"label":"Collect","content":"3x + 30 = 180"},
              {"label":"Solve","content":"3x = 150, x = 50"},
              {"label":"Check","content":"2(50) = 100, 50 + 30 = 80, 100 + 80 = 180 ✓"},
              {"label":"Answer","content":"x = 50","isAnswer":True,"is_answer":True}]}},
 "gold":{"title":"Gold: chain the theorems",
   "steps":[
     "Add every fact you can: radii make isosceles triangles, diameters make 90° angles.",
     "Work from what you know to the centre angle, then halve for the circumference.",
     "If letters appear, build one equation in x, solve, then substitute back."],
   "example":{"question":"O is the centre. Angle OAB = 40°. Find angle ACB (C on the major arc).",
     "steps":[{"label":"Isosceles","content":"OA = OB, so OBA = 40°"},
              {"label":"Centre","content":"AOB = 180 − 40 − 40 = 100°"},
              {"label":"Halve","content":"ACB = 100 ÷ 2 = 50°"},
              {"label":"Check","content":"50 × 2 = 100 ✓"},
              {"label":"Answer","content":"ACB = 50°","isAnswer":True,"is_answer":True}]}},
}

# ============ guided (opener + teach) ============
opener_svg = fig_centre_circ("124°","?","A centre swinging 124 degrees and a point on the circle")
guided = {
 "opener":{
   "display": opener_svg + "<br>Stand at the centre of a circular track (point O). To look from runner A across to runner B you swing your head through 124°. A spectator C waits on the far side of the track. Because C is twice as far around the curve, they turn their head only half as much to follow the same two runners.",
   "steps":[
     {"pre":"Half of the centre's swing: 124 ÷ 2 = ","post":"","answer":62,"hint":"Halve 124."},
     {"say":"Now try another. If the swing at the centre were 90°, the spectator on the far side turns half of that."},
     {"pre":"90 ÷ 2 = ","post":"","answer":45,"hint":"Halve 90."},
     {"say":"<strong>That is today's key fact.</strong> The angle at the <strong>centre</strong> is twice the angle at the <strong>circumference</strong> standing on the same arc. Every other circle theorem builds on angles like these."}]},
 "teach":{
   "bronze":{
     "display": fig_centre_circ("80°","?","Angle at the centre 80 degrees, find the circumference angle")+CAP+
       "The angle at the centre is 80°. Find the angle at the circumference on the same arc.",
     "steps":[
       {"say":"The angle at the centre is twice the angle at the circumference on the same arc. Let us find the circumference angle."},
       {"pre":"How many circumference angles make the centre angle? Type the multiplier: ","post":"","answer":2,"hint":"The centre is TWICE."},
       {"pre":"So circumference = 80 ÷ 2 = ","post":"","answer":40,"hint":"80 shared into 2."},
       {"pre":"Check by doubling: 40 × 2 = ","post":"","answer":80,"hint":"Twice 40."},
       {"pre":"Is 40 smaller than 80? Type 1 for yes: ","post":"","answer":1,"hint":"The circumference angle is the smaller one.","done":"Smaller, as it should be. Halving the centre angle is the whole move."}]},
   "silver":{
     "display": fig_ts_centre("50°","?","Tangent-chord angle 50 degrees with the angle at the centre")+CAP+
       "A tangent touches a circle at A. The angle between the tangent and chord AB is 50°. O is the centre. Find angle AOB.",
     "steps":[
       {"say":"Two theorems combine here: alternate segment, then angle at the centre. The tangent-chord angle is 50°."},
       {"pre":"Angle in the alternate segment = tangent-chord angle = ","post":"","answer":50,"hint":"They are equal."},
       {"pre":"Angle at the centre is twice the circumference angle: 2 × 50 = ","post":"","answer":100,"hint":"Double 50."},
       {"pre":"Check by halving: 100 ÷ 2 = ","post":"","answer":50,"hint":"Half returns the circumference angle."},
       {"pre":"Is the centre angle bigger than the circumference angle? Type 1 for yes: ","post":"","answer":1,"hint":"The centre is twice as big.","done":"Bigger, as it must be. The new move: chain two theorems in one question."}]},
   "gold":{
     "display": fig_iso_radii("20°","?",False,"Two radii forming an isosceles triangle, C on the major arc")+CAP+
       "O is the centre. Angle OAB = 20°. Find angle ACB (C on the major arc).",
     "steps":[
       {"say":"OA and OB are radii, so triangle OAB is isosceles. We climb from the base angle to the centre, then halve for the circumference."},
       {"pre":"Base angles equal, so angle OBA = ","post":"","answer":20,"hint":"Same as angle OAB."},
       {"pre":"Centre angle AOB = 180 − 20 − 20 = ","post":"","answer":140,"hint":"180 take away both 20s."},
       {"pre":"Circumference angle ACB = 140 ÷ 2 = ","post":"","answer":70,"hint":"Half the centre angle."},
       {"pre":"Check by doubling: 70 × 2 = ","post":"","answer":140,"hint":"Twice 70 returns the centre angle.","done":"Back to 140°. The new move: turn two equal radii into the centre angle, then halve."}]},
 },
}

# ============ method_card (slim) ============
method_card = {
 "title":"Circle Theorems",
 "steps":[
   "Draw in radii, mark equal lengths, and name the theorem you will use.",
   "Angle at the centre = twice the angle at the circumference (same arc).",
   "Semicircle angle = 90°; same-segment angles equal; cyclic-quad opposites sum to 180°.",
   "Tangent meets radius at 90°; two tangents from a point are equal; alternate-segment angles are equal."],
 "content":"<p>Every circle theorem starts from a picture. Draw in radii to make isosceles triangles, and look for a diameter (which gives a 90° angle in a semicircle).</p><p>The workhorse fact is that the <strong>angle at the centre is twice the angle at the circumference</strong> on the same arc. Halve to go inward, double to go outward.</p>",
 "example":"<p><strong>Angle at centre = 110°. Find the angle at the circumference.</strong></p><p>Circumference = \\(110 \\div 2 = 55°\\) (centre is twice the circumference).</p>",
}

# ============ assemble (preserve related_videos, topic_links, worked_examples) ============
live = json.load(io.open("_live_geometry-L07.json", encoding="utf-8"))
pd = {
 "method_card": method_card,
 "topic_links": live["topic_links"],
 "problem_bank": problem_bank,
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": live["related_videos"],
 "worked_examples": live["worked_examples"],
}
json.dump(pd, io.open("lesson_maths-aqa_geometry-L07.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_geometry-L07.json")
print("bronze",len(bronze),"silver",len(silver),"gold",len(gold))
