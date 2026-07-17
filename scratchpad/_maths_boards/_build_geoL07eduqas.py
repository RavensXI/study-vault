# -*- coding: utf-8 -*-
"""Assemble the full guided + diagrams practice_data for maths-eduqas
geometry-L07 (Circle Theorems). Preserves topic_links / related_videos /
worked_examples byte-for-byte from the live row."""
import json, io
from _build_geoL07eduqas_svg import (
    svg_cc, svg_semicircle_plain, svg_semicircle_marked, svg_cyclicquad,
    svg_samesegment, svg_tangent_radius, svg_two_tangents, svg_altsegment,
    svg_tangent_chord_centre, svg_isosceles_major, svg_tangent_chord_radius,
    svg_chord_through_centre)

live = json.load(io.open("_geoL07eduqas_live.json", encoding="utf-8"))
LPD = live["practice_data"]

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s): return {"say": s}

# ---------------- BRONZE ----------------
bronze = [
  {  # b1 centre 140 -> circ 70
   "display": svg_cc("140°","?","Angle at the centre 140 degrees, find the circumference angle") +
     " The angle at the centre of a circle is \\(140°\\). Find the angle at the circumference standing on the same arc.",
   "solutions":[70],"calculator":False,"input_type":"single_value",
   "hint":"The angle at the circumference is half the angle at the centre.",
   "misconceptions":[{"pattern":"doubled_not_halved","expect":280,
     "message":"The angle at the circumference is HALF the angle at the centre, not double. 140 ÷ 2 = 70°."}],
   "guided_steps":[
     say("The angle at the centre is twice the angle at the circumference on the same arc."),
     box("How many circumference angles make the centre angle? Type the multiplier: ",2,"The centre angle is TWICE the circumference angle."),
     box("So circumference = 140 ÷ 2 = ",70,"140 shared into 2.",phase="substitute"),
     box("Check by doubling back: 70 × 2 = ",140,"Twice 70 should return the centre angle.",done="Back to 140°, so 70° is correct.")]},
  {  # b2 circ 34 -> centre 68
   "display": svg_cc("?","34°","Angle at the circumference 34 degrees, find the centre angle") +
     " The angle at the circumference is \\(34°\\). Find the angle at the centre standing on the same arc.",
   "solutions":[68],"calculator":False,"input_type":"single_value",
   "hint":"The angle at the centre is twice the angle at the circumference.",
   "misconceptions":[{"pattern":"halved_not_doubled","expect":17,
     "message":"The angle at the centre is TWICE the angle at the circumference. 34 × 2 = 68°."}],
   "guided_steps":[
     say("The angle at the centre is twice the angle at the circumference on the same arc."),
     box("Type the multiplier linking circumference to centre: ",2,"The centre is TWICE the circumference."),
     box("So centre = 34 × 2 = ",68,"Double 34.",phase="substitute"),
     box("Check by halving: 68 ÷ 2 = ",34,"Half of 68 returns the circumference angle.",done="Back to 34°, so 68° is right.")]},
  {  # b3 semicircle -> 90
   "display": svg_semicircle_plain("Triangle inscribed in a semicircle, AB is the diameter") +
     " A triangle is inscribed in a circle so that one side, AB, is a diameter. C is on the circle. Find angle ACB, the angle opposite the diameter.",
   "solutions":[90],"calculator":False,"input_type":"single_value",
   "hint":"The angle in a semicircle is always a right angle.",
   "misconceptions":[{"pattern":"used_straight_line","expect":180,
     "message":"A diameter is a straight line (180°), but the angle at C on the circle is half of that. The angle in a semicircle is 90°."}],
   "guided_steps":[
     say("AB is a diameter, so C sits in a semicircle."),
     box("A diameter is a straight line. How many degrees is a straight line? ",180,"Half a full turn."),
     box("The angle in the semicircle is half of that: 180 ÷ 2 = ",90,"Half of 180.",phase="substitute"),
     box("So angle ACB is a right angle. Type it: ",90,"You just found it.",done="90°, and it is 90° wherever C sits on the arc.")]},
  {  # b4 same segment 48 -> 48
   "display": svg_samesegment("48°","x","Two angles in the same segment standing on chord AB") +
     " Two angles in the same segment stand on the chord AB. One is \\(48°\\) and the other is \\(x\\). Find \\(x\\).",
   "solutions":[48],"calculator":False,"input_type":"single_value",
   "hint":"Angles in the same segment are equal.",
   "misconceptions":[{"pattern":"thought_supplementary","expect":132,
     "message":"Angles in the same segment are equal, not supplementary. They stand on the same chord, so x = 48°."}],
   "guided_steps":[
     say("Angles in the same segment, standing on the same chord, are equal."),
     box("Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary: ",1,"Same-segment angles are equal."),
     box("They are equal, and one is 48°, so x = ",48,"Copy the equal angle.",phase="substitute"),
     box("Check the pair match: 48 and ",48,"They must be the same.",done="Equal, so x = 48°.")]},
  {  # b5 MC diameter subtends -> 90
   "display": svg_semicircle_plain("A diameter subtends an angle at the circumference") +
     " A diameter subtends an angle at the circumference. What is that angle?",
   "options":["\\(90°\\)","\\(180°\\)","\\(60°\\)","\\(45°\\)"],
   "solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "hint":"The angle in a semicircle is always a right angle.",
   "misconceptions":[{"pattern":"half_circle","expect":None,
     "message":"180° is the angle of the diameter itself, not the angle it subtends. The angle in a semicircle is 90°."}]},
  {  # b6 same segment 55 -> 55
   "display": svg_samesegment("x","55°","Two angles subtended by the same chord from the same side") +
     " Two angles subtended by the same chord from the same side are \\(x\\) and \\(55°\\). Find \\(x\\).",
   "solutions":[55],"calculator":False,"input_type":"single_value",
   "hint":"Angles in the same segment are equal.",
   "misconceptions":[{"pattern":"thought_supplementary","expect":125,
     "message":"Angles in the SAME segment are equal, not supplementary. x = 55°."}],
   "guided_steps":[
     say("Angles in the same segment, standing on the same chord, are equal."),
     box("Equal or supplementary? Type 1 for equal, 2 for supplementary: ",1,"Same-segment angles are equal."),
     box("They are equal, and one is 55°, so x = ",55,"Copy the equal angle.",phase="substitute"),
     box("Check the pair match: 55 and ",55,"They must be the same.",done="Equal, so x = 55°.")]},
  {  # b7 MC chord through centre -> diameter
   "display": svg_chord_through_centre("A chord passing through the centre of a circle") +
     " A chord passes through the centre of the circle. What is it called?",
   "options":["A diameter","A tangent","A radius","A secant"],
   "solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "hint":"It is the longest chord, running right across through the centre.",
   "misconceptions":[{"pattern":"radius","expect":None,
     "message":"A radius goes from the centre to the circumference, only half way. A chord through the centre reaches both sides, so it is a diameter."}]},
  {  # b8 centre 90 -> circ 45
   "display": svg_cc("90°","?","Angle at the centre 90 degrees, find the circumference angle") +
     " The angle at the centre is \\(90°\\). Find the angle at the circumference on the same arc.",
   "solutions":[45],"calculator":False,"input_type":"single_value",
   "hint":"Halve the angle at the centre to get the angle at the circumference.",
   "misconceptions":[{"pattern":"same_as_centre","expect":90,
     "message":"The circumference angle is HALF the centre angle: 90 ÷ 2 = 45°, not the same as the centre."}],
   "guided_steps":[
     say("The angle at the centre is twice the angle at the circumference on the same arc."),
     box("Type the multiplier linking them: ",2,"The centre is TWICE the circumference."),
     box("So circumference = 90 ÷ 2 = ",45,"90 shared into 2.",phase="substitute"),
     box("Check by doubling: 45 × 2 = ",90,"Twice 45.",done="Back to 90°, so 45° is correct.")]},
]

# ---------------- SILVER ----------------
silver = [
  {  # s1 cyclic quad 72 -> 108
   "display": svg_cyclicquad("72°","","?","","Cyclic quadrilateral with one angle 72 degrees and its opposite unknown") +
     " ABCD is a cyclic quadrilateral. Angle A is \\(72°\\). Find the opposite angle, angle C.",
   "solutions":[108],"calculator":False,"input_type":"single_value",
   "hint":"Opposite angles of a cyclic quadrilateral add up to 180 degrees.",
   "misconceptions":[{"pattern":"thought_equal","expect":72,
     "message":"Opposite angles of a cyclic quadrilateral add to 180°, they are not equal. 180 − 72 = 108°."}],
   "guided_steps":[
     say("Opposite angles of a cyclic quadrilateral add up to 180°."),
     box("What total do the opposite pair make? ",180,"Cyclic quadrilateral opposite angles sum to this."),
     box("So angle C = 180 − 72 = ",108,"180 take away 72.",phase="substitute"),
     box("Check the pair: 72 + 108 = ",180,"Add the pair back.",done="They sum to 180°, so angle C = 108°.")]},
  {  # s2 MC tangent-radius -> 90
   "display": svg_tangent_radius("A tangent meeting a radius at the point of contact") +
     " A tangent meets a radius at the point of contact. What is the angle between them?",
   "options":["\\(90°\\)","\\(180°\\)","\\(45°\\)","It depends on the circle"],
   "solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "hint":"A tangent is perpendicular to the radius at the point of contact.",
   "misconceptions":[{"pattern":"depends","expect":None,
     "message":"It is always 90°: the tangent is perpendicular to the radius at the point of contact, whatever the circle."}]},
  {  # s3 two tangents 12 -> 12
   "display": svg_two_tangents("12 cm","Two tangents from an external point T to the circle") +
     " Two tangents are drawn from an external point T, touching the circle at A and B. TA = \\(12\\) cm. Find TB.",
   "solutions":[12],"calculator":False,"input_type":"single_value",
   "hint":"Two tangents from the same external point are equal in length.",
   "misconceptions":[{"pattern":"doubled","expect":24,
     "message":"Two tangents from the same external point are equal, so TB = TA = 12 cm, not double."}],
   "guided_steps":[
     say("Two tangents drawn from the same external point are equal in length."),
     box("TA and TB come from the same point T. Type 1 if they are equal, 2 if not: ",1,"Two tangents from a point are equal."),
     box("They are equal, and TA = 12 cm, so TB = ",12,"Copy the length.",phase="substitute"),
     box("Check the pair match: 12 and ",12,"Both tangents equal.",done="Equal, so TB = 12 cm.")]},
  {  # s4 cyclic quad DAB 85, ABC 110 -> BCD 95
   "display": svg_cyclicquad("85°","110°","?","","Cyclic quadrilateral ABCD with angle A 85 degrees and angle B 110 degrees") +
     " ABCD is a cyclic quadrilateral. Angle DAB = \\(85°\\) and angle ABC = \\(110°\\). Find angle BCD.",
   "solutions":[95],"calculator":False,"input_type":"single_value",
   "hint":"Angle BCD is opposite angle DAB, and opposite angles sum to 180 degrees.",
   "misconceptions":[{"pattern":"used_adjacent","expect":70,
     "message":"Angle BCD is opposite angle DAB (85°), so BCD = 180 − 85 = 95°. Pairing it with the adjacent 110° gives 70, the wrong pair."}],
   "guided_steps":[
     say("Opposite angles of a cyclic quadrilateral add to 180°. Angle BCD is opposite angle DAB."),
     box("Which angle is opposite BCD? Type 1 for DAB (85°), 2 for ABC (110°): ",1,"BCD and DAB sit at opposite corners."),
     box("So angle BCD = 180 − 85 = ",95,"180 take away 85.",phase="substitute"),
     box("Check the opposite pair: 85 + 95 = ",180,"Add the opposite pair back.",done="They sum to 180°, so BCD = 95°.")]},
  {  # s5 tangent-chord 50, chord-radius 40
   "display": svg_tangent_chord_radius("50°","?","Tangent, chord and radius meeting at the point of contact A") +
     " A tangent touches the circle at A. The angle between the tangent and chord AB is \\(50°\\). OA is a radius. Find the angle between the chord AB and the radius OA.",
   "solutions":[40],"calculator":False,"input_type":"single_value",
   "hint":"The tangent meets the radius at 90 degrees; the chord splits that right angle.",
   "misconceptions":[{"pattern":"copied_tangent_chord","expect":50,
     "message":"The tangent-radius angle is 90°, split into the tangent-chord part (50°) and the chord-radius part. So chord-radius = 90 − 50 = 40°, not 50."}],
   "guided_steps":[
     say("The tangent is perpendicular to the radius, so the tangent-radius angle is 90°. The chord AB splits it into two parts."),
     box("The whole angle between tangent and radius is: ",90,"Tangent meets radius at a right angle."),
     box("Take away the tangent-chord part: 90 − 50 = ",40,"90 take away 50.",phase="substitute"),
     box("Check the two parts rebuild the right angle: 50 + 40 = ",90,"They should add back to the right angle.",done="Back to 90°, so the chord-radius angle is 40°.")]},
  {  # s6 circ 40 -> reflex centre 280
   "display": svg_cc("","40°","Angle 40 degrees at the circumference, standing on the major arc") +
     " C is on the major arc. The angle at the circumference, angle ACB, is \\(40°\\). Find the reflex angle at the centre, angle AOB.",
   "solutions":[280],"calculator":False,"input_type":"single_value",
   "hint":"Double for the centre angle, then take it from 360 degrees for the reflex.",
   "misconceptions":[
     {"pattern":"forgot_reflex","expect":80,
      "message":"The (non-reflex) centre angle is 2 × 40 = 80°. The REFLEX angle is the rest of the full turn: 360 − 80 = 280°."},
     {"pattern":"used_circumference","expect":320,
      "message":"Double the circumference angle first: 2 × 40 = 80°, then reflex = 360 − 80 = 280°. Using 360 − 40 = 320 forgets to double."}],
   "guided_steps":[
     say("The angle at the centre is twice the angle at the circumference. Then the reflex angle is the rest of the full turn of 360°."),
     box("First the centre angle: 2 × 40 = ",80,"Double the circumference angle."),
     box("The reflex angle is 360 − 80 = ",280,"A full turn take away 80.",phase="substitute"),
     box("Check they complete a turn: 80 + 280 = ",360,"The two centre angles make a full turn.",done="A full 360°, so the reflex angle is 280°.")]},
  {  # s7 semicircle x, 2x -> x 30
   "display": svg_semicircle_marked("x","2x","Right-angled triangle in a semicircle with angles x and 2x at the ends") +
     " AB is a diameter, so angle ACB = \\(90°\\). The other two angles of triangle ABC are \\(x\\) at A and \\(2x\\) at B. Find \\(x\\).",
   "solutions":[30],"calculator":False,"input_type":"single_value",
   "hint":"The three angles of the triangle add to 180; one of them is 90.",
   "misconceptions":[{"pattern":"forgot_right_angle","expect":60,
     "message":"Do not forget the 90° angle. All three add to 180: 90 + x + 2x = 180, so 3x = 90 and x = 30. Ignoring the 90 gives x = 60."}],
   "guided_steps":[
     say("Angle ACB is 90° (angle in a semicircle). The three angles of the triangle add to 180°."),
     box("Take the 90° from 180: 180 − 90 = ",90,"What the other two angles must share."),
     box("The other two are x and 2x, so x + 2x = how many x? ",3,"1 lot plus 2 lots.",post="x"),
     box("So 3x = 90, meaning x = 90 ÷ 3 = ",30,"90 shared into 3.",phase="substitute"),
     box("Check all three: 90 + 30 + 60 = ",180,"Add 90, x and 2x.",done="Back to 180°, so x = 30°.")]},
]

# ---------------- GOLD ----------------
gold = [
  {  # g1 tangent-chord 65 -> centre 130
   "display": svg_tangent_chord_centre("65°","?","Tangent and chord at A with the angle at the centre") +
     " A tangent touches the circle at A. The angle between the tangent and chord AB is \\(65°\\). O is the centre. Find angle AOB, the angle at the centre standing on chord AB.",
   "solutions":[130],"calculator":False,"input_type":"single_value",
   "hint":"Use the alternate segment angle first, then double it for the centre.",
   "misconceptions":[{"pattern":"forgot_double","expect":65,
     "message":"First the alternate segment angle equals the tangent-chord angle, 65°. Then the angle at the CENTRE is twice that: 2 × 65 = 130°. Stopping at 65 forgets the centre step."}],
   "guided_steps":[
     say("Two theorems combine. Alternate segment: the angle in the alternate segment equals the tangent-chord angle. Then the angle at the centre is twice the angle at the circumference."),
     box("Angle in the alternate segment = tangent-chord angle = ",65,"They are equal by the alternate segment theorem."),
     box("Angle at the centre is twice that: 2 × 65 = ",130,"Double 65.",phase="substitute"),
     box("Check by halving: 130 ÷ 2 = ",65,"Half the centre angle returns the circumference angle.",done="Back to 65°, so AOB = 130°.")]},
  {  # g2 cyclic quad 4x and 2x+30 -> x 25
   "display": svg_cyclicquad("4x","","2x + 30","","Cyclic quadrilateral with opposite angles 4x and 2x plus 30") +
     " ABCD is a cyclic quadrilateral. Angle A = \\(4x\\) and the opposite angle C = \\(2x + 30\\). Find \\(x\\).",
   "solutions":[25],"calculator":False,"input_type":"single_value",
   "hint":"Opposite angles sum to 180; form an equation in x and solve.",
   "misconceptions":[{"pattern":"set_equal","expect":15,
     "message":"Opposite angles SUM to 180, they are not equal. 4x + 2x + 30 = 180 gives x = 25. Setting 4x = 2x + 30 gives x = 15."}],
   "guided_steps":[
     say("Angle A and angle C are opposite angles of the cyclic quadrilateral, so they add to 180°."),
     box("Add the x terms: 4x + 2x = ",6,"4 lots plus 2 lots of x.",post="x"),
     box("So 6x + 30 = 180. Take 30 across: 180 − 30 = ",150,"180 take away 30."),
     box("Now 6x = 150, so x = 150 ÷ 6 = ",25,"150 shared into 6.",phase="substitute"),
     box("Check the pair: 4(25) + (2×25 + 30) = 100 + 80 = ",180,"Work out both angles and add.",done="They sum to 180°, so x = 25.")]},
  {  # g3 MC which theorem -> alternate segment
   "display": "The angle between a tangent and a chord equals the angle in the alternate segment, the angle at the circumference on the other side of the chord. Which theorem is this?",
   "options":["Alternate segment theorem","Angle at the centre theorem","Tangent-radius theorem","Angles in the same segment"],
   "solutions":[0],"calculator":False,"input_type":"multiple_choice",
   "hint":"It links a tangent-chord angle to an angle in the far segment.",
   "misconceptions":[{"pattern":"tangent_radius","expect":None,
     "message":"Tangent-radius is about the 90° between a tangent and a radius. This links a tangent-chord angle to the alternate segment, so it is the alternate segment theorem."}]},
  {  # g4 O centre OAB 26 -> ACB 64
   "display": svg_isosceles_major("26°","?","Two radii forming an isosceles triangle, C on the major arc") +
     " O is the centre. A and B are on the circle and angle OAB = \\(26°\\). C is on the major arc. Find angle ACB.",
   "solutions":[64],"calculator":False,"input_type":"single_value",
   "hint":"Use the equal radii to find the centre angle, then halve it.",
   "misconceptions":[{"pattern":"forgot_halve","expect":128,
     "message":"Angle AOB at the centre is 128°, but ACB at the circumference is HALF of that: 128 ÷ 2 = 64°. Using 128 forgets to halve."}],
   "guided_steps":[
     say("OA and OB are both radii, so triangle OAB is isosceles: the base angles are equal."),
     box("Base angles equal, so angle OBA = ",26,"Same as angle OAB."),
     box("Angles in triangle OAB add to 180. Centre angle AOB = 180 − 26 − 26 = ",128,"180 take away both 26s."),
     box("Angle at the circumference is half the centre: 128 ÷ 2 = ",64,"Half of 128.",phase="substitute"),
     box("Check by doubling: 64 × 2 = ",128,"Twice ACB returns the centre angle.",done="Back to 128°, so ACB = 64°.")]},
  {  # g5 AB diameter, CAB 34 -> ABC 56
   "display": svg_semicircle_marked("34°","?","Right-angled triangle in a semicircle with angle CAB 34 degrees") +
     " AB is a diameter of the circle. C is on the circle. Angle CAB = \\(34°\\). Find angle ABC.",
   "solutions":[56],"calculator":False,"input_type":"single_value",
   "hint":"The semicircle gives a 90 degree angle at C; then use the triangle sum.",
   "misconceptions":[{"pattern":"answered_semicircle","expect":90,
     "message":"90° is angle ACB (the semicircle right angle), not the angle asked. Put it in the triangle: 180 − 90 − 34 = 56°."}],
   "guided_steps":[
     say("AB is a diameter, so angle ACB stands in a semicircle and equals 90°. Then use the triangle."),
     box("Angle ACB in the semicircle = ",90,"Angle in a semicircle."),
     box("Triangle ACB adds to 180. Add the two known angles: 90 + 34 = ",124,"90 plus 34."),
     box("Subtract from 180: 180 − 124 = ",56,"180 take away 124.",phase="substitute"),
     box("Check all three: 90 + 34 + 56 = ",180,"Add the three angles.",done="Back to 180°, so ABC = 56°.")]},
]

problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description":"One theorem applied in a single step to find a missing angle or length.",
  "silver_description":"One theorem written as a short equation, or two facts combined in a couple of steps.",
  "gold_description":"Several theorems chained together, often with an equation in x to solve.",
}

tier_guides = {
  "bronze":{
    "title":"Bronze: one theorem, one step",
    "steps":[
      "<strong>Angle at the centre</strong> is twice the angle at the circumference on the same arc: halve to go in, double to go out.",
      "<strong>Semicircle:</strong> the angle in a semicircle is 90°. <strong>Same segment:</strong> angles on the same chord are equal.",
      "<strong>Cyclic quadrilateral:</strong> opposite angles add to 180°. A <strong>tangent</strong> meets a radius at 90°, and two tangents from a point are equal."],
    "example":{"question":"The angle at the centre is 100°. Find the angle at the circumference.",
      "steps":[{"label":"Rule","content":"Centre is twice the circumference."},
               {"label":"Halve","content":"100 ÷ 2 = 50"},
               {"label":"Check","content":"50 × 2 = 100 ✓"},
               {"label":"Answer","content":"50°","isAnswer":True,"is_answer":True}]}},
  "silver":{
    "title":"Silver: one equation or two facts",
    "steps":[
      "Turn a theorem into an equation: centre = 2 × circumference, or opposite angles of a cyclic quadrilateral sum to 180°.",
      "For the alternate segment, the tangent-chord angle equals the angle in the alternate segment.",
      "Solve the short equation, then substitute back to check."],
    "example":{"question":"A cyclic quadrilateral has opposite angles 2x and x + 30. Find x.",
      "steps":[{"label":"Set up","content":"2x + x + 30 = 180"},
               {"label":"Collect","content":"3x + 30 = 180"},
               {"label":"Solve","content":"3x = 150, x = 50"},
               {"label":"Check","content":"2(50) = 100, 50 + 30 = 80, 100 + 80 = 180 ✓"},
               {"label":"Answer","content":"x = 50","isAnswer":True,"is_answer":True}]}},
  "gold":{
    "title":"Gold: chain the theorems",
    "steps":[
      "Add every fact you can: radii make isosceles triangles, diameters make 90° angles in a semicircle.",
      "Work from what you know to the centre angle, then halve for the circumference.",
      "If letters appear, build one equation in x, solve, then substitute back."],
    "example":{"question":"O is the centre. Angle OAB = 40°. Find angle ACB (C on the major arc).",
      "steps":[{"label":"Isosceles","content":"OA = OB, so OBA = 40°"},
               {"label":"Centre","content":"AOB = 180 − 40 − 40 = 100°"},
               {"label":"Halve","content":"ACB = 100 ÷ 2 = 50°"},
               {"label":"Check","content":"50 × 2 = 100 ✓"},
               {"label":"Answer","content":"ACB = 50°","isAnswer":True,"is_answer":True}]}},
}

guided = {
  "opener":{
    "display": svg_cc("120°","?","A lighthouse beam swinging 120 degrees at the centre of a bay") +
      "<br>A lighthouse stands at the centre O of a circular bay. Its beam swings from boat A to boat B through 120°. A person on the shore (on the edge of the bay) watches the same two boats. Because they are further round the curve, they turn their head only half as much.",
    "steps":[
      box("Half of the beam's swing: 120 ÷ 2 = ",60,"Halve 120."),
      say("Now try another. If the beam swept 80° at the centre, the watcher on the shore turns half of that."),
      box("80 ÷ 2 = ",40,"Halve 80."),
      say("<strong>That is today's key fact.</strong> The angle at the <strong>centre</strong> is twice the angle at the <strong>circumference</strong> standing on the same arc. Every other circle theorem builds on angles like these.")]},
  "teach":{
    "bronze":{
      "display": svg_cc("100°","?","Angle at the centre 100 degrees, find the circumference angle") +
        " The angle at the centre is 100°. Find the angle at the circumference on the same arc.",
      "steps":[
        say("The angle at the centre is twice the angle at the circumference on the same arc. Let us find the circumference angle."),
        box("How many circumference angles make the centre angle? Type the multiplier: ",2,"The centre is TWICE."),
        box("So circumference = 100 ÷ 2 = ",50,"100 shared into 2."),
        box("Check by doubling: 50 × 2 = ",100,"Twice 50."),
        box("Is 50 smaller than 100? Type 1 for yes: ",1,"The circumference angle is the smaller one.",done="Smaller, as it should be. Halving the centre angle is the whole move.")]},
    "silver":{
      "display": svg_cyclicquad("3x","","x + 40","","Cyclic quadrilateral with opposite angles 3x and x plus 40") +
        " A cyclic quadrilateral has opposite angles 3x and x + 40. Find x.",
      "steps":[
        say("Opposite angles of a cyclic quadrilateral add to 180°. Turn that into an equation."),
        box("Add the x terms: 3x + x = ",4,"3 lots plus 1 lot.",post="x"),
        box("The number is 40, so 4x + 40 = 180. Take 40 across: 180 − 40 = ",140,"180 take away 40."),
        box("Now 4x = 140, so x = 140 ÷ 4 = ",35,"140 shared into 4."),
        box("Check: 3(35) + (35 + 40) = 105 + 75 = ",180,"Work out both angles and add.",done="They sum to 180°. The new move: turn a theorem into an equation.")]},
    "gold":{
      "display": svg_isosceles_major("20°","?","Two radii forming an isosceles triangle, C on the major arc") +
        " O is the centre. Angle OAB = 20°. Find angle ACB (C on the major arc).",
      "steps":[
        say("OA and OB are radii, so triangle OAB is isosceles. We climb from the base angle to the centre, then halve for the circumference."),
        box("Base angles equal, so angle OBA = ",20,"Same as angle OAB."),
        box("Centre angle AOB = 180 − 20 − 20 = ",140,"180 take away both 20s."),
        box("Circumference angle ACB = 140 ÷ 2 = ",70,"Half the centre angle."),
        box("Check by doubling: 70 × 2 = ",140,"Twice 70 returns the centre angle.",done="Back to 140°. The new move: two equal radii give the centre angle, then halve.")]},
  },
}

method_card = {
  "title":"Circle Theorems",
  "steps":[
    "Draw in radii to make isosceles triangles, and look for a diameter (a 90° angle in a semicircle).",
    "Angle at the centre = twice the angle at the circumference on the same arc.",
    "Same-segment angles are equal; cyclic-quad opposite angles sum to 180°.",
    "Tangent meets radius at 90°; two tangents from a point are equal; alternate-segment angles are equal."],
  "content":"<p>Every circle theorem starts from a picture. Draw in radii to make isosceles triangles, and look for a diameter, which gives a 90° angle in a semicircle.</p><p>The workhorse fact is that the <strong>angle at the centre is twice the angle at the circumference</strong> on the same arc. Halve to go inward, double to go outward.</p>",
  "example":"<p><strong>Angle at centre = 110°. Find the angle at the circumference.</strong></p><p>Circumference = \\(110 \\div 2 = 55°\\) (the centre is twice the circumference).</p>",
}

# preserve worked_examples, but strip pre-existing em dashes in labels
# (style rule + validator forbid them; only touch the dash, nothing else)
we = json.loads(json.dumps(LPD["worked_examples"]))
for ex in we:
    for st in ex.get("steps", []):
        if isinstance(st.get("label"), str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pd = {
  "method_card": method_card,
  "topic_links": LPD["topic_links"],            # preserved byte-for-byte
  "problem_bank": problem_bank,
  "tier_guides": tier_guides,
  "guided": guided,
  "related_videos": LPD.get("related_videos", []),   # preserved ([])
  "worked_examples": we,      # preserved (only em dashes in labels sanitised)
}

json.dump(pd, io.open("lesson_maths-eduqas_geometry-L07.json","w",encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_maths-eduqas_geometry-L07.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
