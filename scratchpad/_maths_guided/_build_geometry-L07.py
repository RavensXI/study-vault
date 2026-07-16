# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_geometry-L07.json", encoding="utf-8"))

# ---- method_card: fix the double </p>, keep slim (already <=140 words / 4 steps) ----
pd["method_card"]["content"] = (
    "<p>Key theorems:</p>"
    "<p>1. Angle at the <strong>centre</strong> is <strong>twice</strong> the angle at the circumference (from the same arc).</p>"
    "<p>2. Angle in a <strong>semicircle</strong> is \\(90°\\).</p>"
    "<p>3. Angles in the <strong>same segment</strong> are equal.</p>"
    "<p>4. <strong>Opposite angles</strong> in a cyclic quadrilateral sum to \\(180°\\).</p>"
    "<p>5. A <strong>tangent</strong> meets the radius at \\(90°\\).</p>"
    "<p>6. <strong>Tangents</strong> from an external point are equal in length.</p>"
    "<p>7. <strong>Alternate segment</strong>: the angle between a tangent and a chord equals the angle in the alternate segment.</p>"
)

def M(pattern, expect, message, note=None):
    d = {"pattern": pattern, "check": pattern, "expect": expect, "message": message}
    if note:
        d["note"] = note
    return d

def say(s):
    return {"say": s}

def box(pre, answer, hint, post="", done=None, phase=None, say_=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done:
        d["done"] = done
    if phase:
        d["phase"] = phase
    if say_ is not None:
        d["say"] = say_
    return d

# =========================== BRONZE ===========================
bronze = [
 # b0  (completion problem)  120 -> 60
 {
  "display": "Angle at centre = \\(120°\\). Find the angle at the circumference.",
  "solutions": [60], "calculator": False, "input_type": "single_value",
  "hint": "The angle at the centre is twice the angle at the circumference, so halve it.",
  "misconceptions": [M("doubled_instead_of_halved", 240,
    "The centre angle is twice the circumference angle, so you halve to go from centre to edge: 120 ÷ 2 = 60°. Doubling instead gives 240°, bigger than a full turn.")],
  "guided_steps": [
    say("The angle at the <strong>centre</strong> is twice the angle at the <strong>circumference</strong> on the same arc, so the circumference angle is half the centre angle."),
    box("The centre angle is how many times the circumference angle? ", 2, "The centre angle is twice as big."),
    box("So halve it: 120 ÷ 2 = ", 60, "Divide the centre angle by 2.", phase="substitute"),
    box("Check by doubling back: 60 × 2 = ", 120, "Double your answer; it should give the centre angle.",
        done="That returns the centre angle of 120°, so 60° is right."),
  ],
 },
 # b1  35 -> 70
 {
  "display": "Angle at circumference = \\(35°\\). Find the angle at the centre.",
  "solutions": [70], "calculator": False, "input_type": "single_value",
  "hint": "The centre angle is twice the circumference angle, so double it.",
  "misconceptions": [M("halved_instead_of_doubled", 17.5,
    "From the edge to the centre you double, not halve: 35 × 2 = 70°. Halving gives 17.5°, smaller than the edge angle, so it cannot be the bigger centre angle.")],
  "guided_steps": [
    say("Going the other way, the centre angle is twice the circumference angle, so double it."),
    box("The centre angle is how many times the circumference angle? ", 2, "Twice as big."),
    box("So double it: 35 × 2 = ", 70, "Multiply the circumference angle by 2.", phase="substitute"),
    box("Check by halving back: 70 ÷ 2 = ", 35, "Halve your answer; it should give the circumference angle.",
        done="That returns the circumference angle of 35°, so 70° is right."),
  ],
 },
 # b2  semicircle -> 90
 {
  "display": "A triangle is drawn in a semicircle with the diameter as one side. What is the angle opposite the diameter?",
  "solutions": [90], "calculator": False, "input_type": "single_value",
  "hint": "The angle in a semicircle is always a right angle.",
  "misconceptions": [M("forgot_to_halve", 180,
    "The diameter subtends 180° at the centre, and the angle at the circumference is half of that: 180 ÷ 2 = 90°. Using 180° forgets to halve.")],
  "guided_steps": [
    say("The diameter passes through the centre, so it makes a straight angle at the centre."),
    box("The straight angle across the diameter, at the centre, is ", 180, "A straight line is 180°."),
    box("The angle at the circumference is half the centre angle: 180 ÷ 2 = ", 90,
        "Halve the 180°.", phase="substitute"),
    box("So the other two angles of the triangle add up to 180 − 90 = ", 90,
        "The triangle's three angles total 180°.",
        done="The right angle plus the other two (90°) totals 180°, the triangle's angle sum, so the angle opposite the diameter is 90°."),
  ],
 },
 # b3  cyclic quad 85 -> 95
 {
  "display": "Cyclic quadrilateral: opposite angles are \\(85°\\) and \\(x°\\). Find \\(x\\).",
  "solutions": [95], "calculator": False, "input_type": "single_value",
  "hint": "Opposite angles in a cyclic quadrilateral add up to 180°.",
  "misconceptions": [M("thought_equal", 85,
    "Opposite angles in a cyclic quadrilateral are supplementary, not equal: x = 180 − 85 = 95°. Answering 85° treats them as equal, which is the same-segment rule, not the cyclic-quad rule.")],
  "guided_steps": [
    say("Opposite angles in a cyclic quadrilateral add up to 180°."),
    box("The two opposite angles must total ", 180, "Opposite angles are supplementary."),
    box("So x = 180 − 85 = ", 95, "Subtract the known angle from 180.", phase="substitute"),
    box("Check they add to 180: 85 + 95 = ", 180, "The pair should total 180°.",
        done="They total 180°, so x = 95° is right."),
  ],
 },
 # b4  NEW (was degenerate 'tangent meets radius')  -> 55
 {
  "display": "OT is a radius and TP is a tangent touching the circle at T. In triangle OTP, the angle at P is \\(35°\\). Find angle TOP (the angle at O).",
  "solutions": [55], "calculator": False, "input_type": "single_value",
  "hint": "The tangent meets the radius at 90°; the three angles of the triangle add to 180°.",
  "misconceptions": [M("forgot_right_angle", 145,
    "The tangent meets the radius at 90°, so the triangle already has a right angle. Angle TOP = 180 − 90 − 35 = 55°. Forgetting the right angle and doing 180 − 35 gives 145°.")],
  "guided_steps": [
    say("A tangent meets a radius at 90°, so the angle at T, angle OTP, is a right angle."),
    box("The angle at T (radius meets tangent) is ", 90, "Tangent meets radius at a right angle."),
    box("The three angles add to 180°, so angle TOP = 180 − 90 − 35 = ", 55,
        "Subtract the right angle and the 35° from 180.", phase="substitute"),
    box("Check the three angles: 90 + 35 + 55 = ", 180, "They should total 180°.",
        done="They total 180°, the triangle's angle sum, so angle TOP = 55° is right."),
  ],
 },
 # b5  same segment 42 (message fixed)
 {
  "display": "Two angles are in the same segment. One is \\(42°\\), the other is \\(x°\\). Find \\(x\\).",
  "solutions": [42], "calculator": False, "input_type": "single_value",
  "hint": "Angles in the same segment are equal, so x matches the 42°.",
  "misconceptions": [M("confused_with_cyclic_quad", 138,
    "You may have confused this with the cyclic quadrilateral rule. Angles in the same segment are EQUAL, not supplementary, so x = 42°, not 180 − 42 = 138°.")],
  "guided_steps": [
    say("Angles in the same segment stand on the same chord and are <strong>equal</strong>."),
    box("Equal angles, so the difference between them is ", 0, "Equal angles differ by zero."),
    box("So x equals the given angle: x = ", 42, "Copy the equal angle.", phase="substitute"),
    box("Check the difference: 42 − 42 = ", 0, "Equal angles should differ by zero.",
        done="Zero difference confirms they are equal, so x = 42°."),
  ],
 },
 # b6  160 -> 80
 {
  "display": "Angle at centre = \\(160°\\). Find the angle at the circumference.",
  "solutions": [80], "calculator": False, "input_type": "single_value",
  "hint": "The centre angle is twice the circumference angle, so halve it.",
  "misconceptions": [M("doubled_instead_of_halved", 320,
    "Halve to go from centre to edge: 160 ÷ 2 = 80°. Doubling gives 320°, more than a full turn, so it cannot be an angle at the edge.")],
  "guided_steps": [
    say("The centre angle is twice the circumference angle, so halve it."),
    box("The centre angle is how many times the circumference angle? ", 2, "Twice as big."),
    box("So halve it: 160 ÷ 2 = ", 80, "Divide the centre angle by 2.", phase="substitute"),
    box("Check by doubling back: 80 × 2 = ", 160, "Double your answer; it should give the centre angle.",
        done="That returns the centre angle of 160°, so 80° is right."),
  ],
 },
 # b7  CHANGED (was 110 -> 70, duplicate of b1) now 105 -> 75
 {
  "display": "Cyclic quadrilateral: opposite angles are \\(x°\\) and \\(105°\\). Find \\(x\\).",
  "solutions": [75], "calculator": False, "input_type": "single_value",
  "hint": "Opposite angles in a cyclic quadrilateral add up to 180°.",
  "misconceptions": [M("thought_equal", 105,
    "Opposite angles in a cyclic quadrilateral are supplementary: x = 180 − 105 = 75°. Answering 105° treats them as equal, which is wrong for a cyclic quadrilateral.")],
  "guided_steps": [
    say("Opposite angles in a cyclic quadrilateral add up to 180°."),
    box("The two opposite angles must total ", 180, "Opposite angles are supplementary."),
    box("So x = 180 − 105 = ", 75, "Subtract the known angle from 180.", phase="substitute"),
    box("Check they add to 180: 105 + 75 = ", 180, "The pair should total 180°.",
        done="They total 180°, so x = 75° is right."),
  ],
 },
]

# =========================== SILVER ===========================
silver = [
 # s0 (completion problem)  reworded; 54 -> reflex 252
 {
  "display": "The angle at the circumference is \\(54°\\). Find the reflex angle at the centre standing on the same arc.",
  "solutions": [252], "calculator": False, "input_type": "single_value",
  "hint": "Double the circumference angle for the centre angle, then subtract from 360° for the reflex.",
  "misconceptions": [M("gave_centre_not_reflex", 108,
    "You found the ordinary centre angle, 2 × 54 = 108°, but the question asks for the reflex angle: 360 − 108 = 252°.")],
  "guided_steps": [
    say("First the ordinary angle at the centre is twice the circumference angle."),
    box("Centre angle = 54 × 2 = ", 108, "Double the circumference angle."),
    box("The reflex angle is the rest of the full turn: 360 − 108 = ", 252,
        "Subtract from 360°.", phase="substitute"),
    box("Check: 108 + 252 = ", 360, "The two centre angles should complete a full turn.",
        done="The two centre angles complete 360°, so the reflex angle is 252°."),
  ],
 },
 # s1  alternate segment 63
 {
  "display": "A tangent and a chord meet at a point on the circle. The angle in the alternate segment is \\(63°\\). Find the angle between the tangent and the chord.",
  "solutions": [63], "calculator": False, "input_type": "single_value",
  "hint": "Alternate segment theorem: the tangent-chord angle equals the angle in the alternate segment.",
  "misconceptions": [M("thought_supplementary", 117,
    "The alternate segment theorem makes them equal, not supplementary: the angle is 63°. Doing 180 − 63 = 117° wrongly treats them as adding to 180°.")],
  "guided_steps": [
    say("The alternate segment theorem: the angle between a tangent and a chord equals the angle in the alternate segment."),
    box("Write the angle in the alternate segment: ", 63, "Read it from the question."),
    box("By the theorem the tangent-chord angle equals it, so it is ", 63,
        "The tangent-chord angle equals the alternate angle.", phase="substitute"),
    box("Two equal angles: their sum is 63 + 63 = ", 126, "Add the two equal angles.",
        done="Two equal 63° angles sum to 126°, confirming the tangent-chord angle is 63°."),
  ],
 },
 # s2  cyclic quad algebra -> 32
 {
  "display": "In a cyclic quadrilateral ABCD, angle A = \\(3x + 5\\) and angle C = \\(2x + 15\\). Find \\(x\\).",
  "solutions": [32], "calculator": False, "input_type": "single_value",
  "hint": "Opposite angles sum to 180°. Add the two expressions and set the total equal to 180.",
  "misconceptions": [M("used_360", 68,
    "Opposite angles in a cyclic quadrilateral sum to 180°, not 360°: 5x + 20 = 180 gives x = 32. Using 360 gives 5x + 20 = 360, so x = 68.")],
  "guided_steps": [
    say("A and C are opposite angles, so they add to 180°: \\((3x + 5) + (2x + 15) = 180\\)."),
    box("Add the x-terms: 3x + 2x = ", 5, "3x + 2x.", post="x"),
    box("Add the numbers: 5 + 15 = ", 20, "5 + 15."),
    box("So 5x + 20 = 180. Subtract 20: 5x = 180 − 20 = ", 160, "180 − 20.", phase="substitute"),
    box("x = 160 ÷ 5 = ", 32, "Divide by 5."),
    box("Check angle A: 3 × 32 + 5 = ", 101, "Work out 3 × 32 + 5.",
        done="Angle C = 2 × 32 + 15 = 79, and 101 + 79 = 180, so x = 32 is right."),
  ],
 },
 # s3  NEW (was duplicate of tangent-radius fact)  -> 35
 {
  "display": "AT is a tangent to a circle with centre O, touching at A. AB is a chord. The angle between the tangent and the chord, angle TAB, is \\(55°\\). Find angle OAB.",
  "solutions": [35], "calculator": False, "input_type": "single_value",
  "hint": "The radius meets the tangent at 90°; the chord splits that right angle.",
  "misconceptions": [M("read_off_tangent_chord_angle", 55,
    "The radius and tangent meet at 90°, and the chord splits that into angle OAB and the 55° angle. So angle OAB = 90 − 55 = 35°. Answering 55° gives the tangent-chord angle instead.")],
  "guided_steps": [
    say("OA is a radius and AT is a tangent, so they meet at 90°: angle OAT = 90°."),
    box("The right angle between radius and tangent is ", 90, "Tangent meets radius at a right angle."),
    box("The chord AB splits that right angle, so angle OAB = 90 − 55 = ", 35,
        "Subtract the tangent-chord angle from 90.", phase="substitute"),
    box("Check the two parts: 35 + 55 = ", 90, "The two parts should rebuild the right angle.",
        done="The two parts rebuild the 90° right angle, so angle OAB = 35° is right."),
  ],
 },
 # s4  tangents equal -> 8
 {
  "display": "From point P outside a circle, two tangents PA and PB are drawn. PA = 8 cm. Find PB.",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Tangents drawn from an external point are equal in length.",
  "misconceptions": [M("no_determinate_error", None,
    "Tangents from the same external point are equal, so PB = PA = 8 cm.")],
  "guided_steps": [
    say("Two tangents drawn from the same external point are equal in length."),
    box("Write the length of PA: ", 8, "Read it from the question.", post=" cm"),
    box("PB equals PA, so PB = ", 8, "Copy the length of PA.", post=" cm", phase="substitute"),
    box("Total length of both tangents: 8 + 8 = ", 16, "Add the two equal lengths.", post=" cm",
        done="Two equal 8 cm tangents total 16 cm, so PB = 8 cm."),
  ],
 },
 # s5  reflex then halve -> 125
 {
  "display": "Angle at centre (minor arc) = \\(110°\\). Find the angle at the circumference from the major arc.",
  "solutions": [125], "calculator": False, "input_type": "single_value",
  "hint": "Use the reflex angle at the centre (360 − 110), then halve it.",
  "misconceptions": [M("halved_wrong_centre_angle", 55,
    "The major-arc angle stands on the reflex centre angle. Reflex = 360 − 110 = 250°, then halve: 250 ÷ 2 = 125°. Halving the 110° directly gives 55°, the wrong centre angle.")],
  "guided_steps": [
    say("The 110° at the centre is on the minor-arc side. The major-arc circumference angle stands on the reflex angle at the centre."),
    box("Reflex angle at the centre = 360 − 110 = ", 250, "Subtract from 360°."),
    box("Angle at the circumference is half the reflex: 250 ÷ 2 = ", 125,
        "Halve the reflex angle.", phase="substitute"),
    box("Check by doubling back: 125 × 2 = ", 250, "Double your answer; it should give the reflex angle.",
        done="Doubling returns the reflex centre angle of 250°, so 125° is right."),
  ],
 },
 # s6  triangle in semicircle -> 58
 {
  "display": "A triangle inscribed in a semicircle has one angle of \\(90°\\) (at the circumference) and another of \\(32°\\). Find the third angle.",
  "solutions": [58], "calculator": False, "input_type": "single_value",
  "hint": "The angle in the semicircle is 90°; the three angles of the triangle sum to 180°.",
  "misconceptions": [M("forgot_right_angle", 148,
    "All three angles of the triangle add to 180°: third = 180 − 90 − 32 = 58°. Forgetting the 90° and doing 180 − 32 gives 148°.")],
  "guided_steps": [
    say("The 90° is the angle in the semicircle. The three angles of the triangle add to 180°."),
    box("Add the two known angles: 90 + 32 = ", 122, "Add them."),
    box("Third angle = 180 − 122 = ", 58, "Subtract from 180°.", phase="substitute"),
    box("Check all three: 90 + 32 + 58 = ", 180, "They should total 180°.",
        done="They total 180°, the triangle's angle sum, so the third angle is 58°."),
  ],
 },
]

# =========================== GOLD ===========================
gold = [
 # g0 (completion problem)  alternate segment -> 40
 {
  "display": "A chord AB subtends \\(40°\\) at the circumference. A tangent at A makes angle \\(x°\\) with the chord AB. Find \\(x\\).",
  "solutions": [40], "calculator": False, "input_type": "single_value",
  "hint": "Alternate segment theorem: the tangent-chord angle equals the angle the chord subtends in the alternate segment.",
  "misconceptions": [M("thought_supplementary", 140,
    "By the alternate segment theorem the tangent-chord angle equals the angle in the alternate segment, so x = 40°. Doing 180 − 40 = 140° treats them as supplementary, which is wrong.")],
  "guided_steps": [
    say("The alternate segment theorem: the tangent-chord angle equals the angle in the alternate segment. The chord AB subtends 40° at the circumference, which is that alternate angle."),
    box("Write the angle in the alternate segment: ", 40, "The angle the chord subtends at the circumference."),
    box("By the theorem, x equals it: x = ", 40, "The tangent-chord angle equals the alternate angle.", phase="substitute"),
    box("Both angles stand on chord AB and are equal, so their sum is 40 + 40 = ", 80,
        "Add the two equal angles.",
        done="Two equal 40° angles, so x = 40° is right."),
  ],
 },
 # g1  minor/major arc circumference -> 152
 {
  "display": "Angle at circumference from the minor arc = \\(28°\\). Find the angle at circumference from the major arc.",
  "solutions": [152], "calculator": False, "input_type": "single_value",
  "hint": "Double to the centre, take the reflex (360 minus it), then halve.",
  "misconceptions": [M("thought_same_segment_equal", 28,
    "The two angles stand on opposite arcs, so they are supplementary, not equal. Centre (minor) = 56°, reflex = 304°, half = 152°. Answering 28° treats them as angles in the same segment.")],
  "guided_steps": [
    say("Work through the centre. The minor-arc angle at the circumference is 28°, so the centre angle on the minor arc is twice that."),
    box("Centre angle (minor arc) = 28 × 2 = ", 56, "Double the circumference angle."),
    box("Reflex centre angle (major arc) = 360 − 56 = ", 304, "Subtract from 360°."),
    box("Major-arc circumference angle = half the reflex: 304 ÷ 2 = ", 152,
        "Halve the reflex angle.", phase="substitute"),
    box("Check they are supplementary: 28 + 152 = ", 180, "Opposite-arc angles should total 180°.",
        done="They total 180°, opposite angles on the two arcs, so 152° is right."),
  ],
 },
 # g2  tangent + Pythagoras -> 5  (message rewritten)
 {
  "display": "From P outside a circle, tangent PA has length 12 and line PB passes through centre O, with PO = 13. Find the radius.",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "The tangent meets the radius at 90°; use Pythagoras in the right-angled triangle.",
  "misconceptions": [M("subtracted_lengths", 1,
    "PA is a tangent, so it meets radius OA at 90°. Use Pythagoras: r² + 12² = 13², so r² = 169 − 144 = 25 and r = 5. Simply subtracting 13 − 12 = 1 skips Pythagoras.")],
  "guided_steps": [
    say("PA is a tangent, so it meets the radius OA at 90°. Triangle OAP is right-angled at A, with radius OA and tangent PA as the short sides and PO as the hypotenuse."),
    box("Square the hypotenuse: 13 × 13 = ", 169, "13 × 13."),
    box("Square the tangent: 12 × 12 = ", 144, "12 × 12."),
    box("Pythagoras: r² = 169 − 144 = ", 25, "Subtract the squares.", phase="substitute"),
    box("So r = √25 = ", 5, "Square root of 25."),
    box("Check: 5 × 5 + 12 × 12 = 25 + 144 = ", 169, "This should equal 13 × 13.",
        done="That equals 13², so the radius is 5."),
  ],
 },
 # g3  CHANGED (was x -> 40, duplicate of g0) now constants give x -> 50
 {
  "display": "In a cyclic quadrilateral, angle A = \\(2x + 10\\), angle B = \\(3y\\), angle C = \\(x + 20\\), angle D = \\(2y + 30\\). Find \\(x\\).",
  "solutions": [50], "calculator": False, "input_type": "single_value",
  "hint": "Angles A and C are opposite, so add them and set the total equal to 180°.",
  "misconceptions": [M("used_360", 110,
    "Opposite angles in a cyclic quadrilateral sum to 180°, not 360°: 3x + 30 = 180 gives x = 50. Using 360 gives 3x + 30 = 360, so x = 110.")],
  "guided_steps": [
    say("Angles A and C are opposite, so they add to 180°: \\((2x + 10) + (x + 20) = 180\\). (B and D are the other pair.)"),
    box("Add the x-terms of A and C: 2x + x = ", 3, "2x + x.", post="x"),
    box("Add the numbers: 10 + 20 = ", 30, "10 + 20."),
    box("So 3x + 30 = 180. Subtract 30: 3x = 180 − 30 = ", 150, "180 − 30.", phase="substitute"),
    box("x = 150 ÷ 3 = ", 50, "Divide by 3."),
    box("Check angle A: 2 × 50 + 10 = ", 110, "Work out 2 × 50 + 10.",
        done="Angle C = 50 + 20 = 70, and 110 + 70 = 180, so x = 50 is right."),
  ],
 },
 # g4  NEW (was off-topic intersecting chords) multi-theorem -> 56
 {
  "display": "A, B, C and D are points on a circle. AC is a diameter and angle BAC = \\(34°\\). B and D lie on opposite sides of the diameter AC. Find angle ADB.",
  "solutions": [56], "calculator": False, "input_type": "single_value",
  "hint": "The diameter gives a 90° angle at B; find angle BCA, then use angles in the same segment on chord AB.",
  "misconceptions": [M("thought_supplementary", 124,
    "Angle BCA = 56° from the semicircle right angle and the triangle's angle sum. Since C and D lie on the same arc, angle ADB = angle BCA = 56°. Treating them as supplementary gives 180 − 56 = 124°, which only applies to points on opposite arcs.")],
  "guided_steps": [
    say("AC is a diameter, so the angle in the semicircle at B is 90°: angle ABC = 90°."),
    box("The angle in the semicircle, angle ABC, is ", 90, "Angle in a semicircle is a right angle."),
    box("Triangle ABC angle sum: angle BCA = 180 − 90 − 34 = ", 56,
        "Subtract 90 and 34 from 180."),
    say("Angle ADB and angle BCA both stand on chord AB, and C and D are on the same arc, so they are angles in the <strong>same segment</strong>: equal."),
    box("So angle ADB = angle BCA = ", 56, "Equal to the angle you just found.", phase="substitute"),
    box("Check triangle ABC: 34 + 90 + 56 = ", 180, "The triangle's angles should total 180°.",
        done="The triangle totals 180°, and angle ADB equals angle BCA in the same segment, so angle ADB = 56°."),
  ],
 },
]

pb = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Recall and apply one circle theorem in a single step.",
 "silver_description": "Combine a theorem with a second step: a reflex angle, an angle sum, or a short equation.",
 "gold_description": "Chain two or more theorems, or bring in Pythagoras, to reach the answer.",
}
pd["problem_bank"] = pb

# ---- tier_guides ----
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: one theorem, one step",
  "steps": [
   "Spot which single circle theorem the diagram is about: angle at the centre, angle in a semicircle, same segment, cyclic quadrilateral, or tangent meeting a radius.",
   "Write the fact as a sum or a halving or doubling, then read off the answer.",
   "The angle at the <strong>centre</strong> is twice the angle at the <strong>circumference</strong>; opposite angles in a cyclic quadrilateral add to 180°.",
  ],
  "example": {
   "question": "Angle at the centre is 100°. Find the angle at the circumference.",
   "steps": [
    {"label": "Theorem", "content": "<p>The angle at the centre is twice the angle at the circumference, so halve it.</p>"},
    {"label": "Check", "content": "<p>\\(100 ÷ 2 = 50°\\), and \\(50 × 2 = 100°\\) returns the centre angle.</p>"},
    {"label": "Answer", "content": "<p>\\(50°\\)</p>", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "silver": {
  "title": "Silver: two steps, or an equation",
  "steps": [
   "Apply the theorem, then make a second move: take a reflex angle (360° minus the centre angle), add up a triangle's angles, or form an equation.",
   "For a reflex angle at the centre, subtract from 360° before halving to the circumference.",
   "When angles are given as expressions like \\(3x + 5\\), set the opposite pair equal to 180°, then solve for x.",
  ],
  "example": {
   "question": "Cyclic quadrilateral: opposite angles are \\(2x\\) and \\(x + 30\\). Find x.",
   "steps": [
    {"label": "Set up", "content": "<p>Opposite angles add to 180°: \\(2x + x + 30 = 180\\).</p>"},
    {"label": "Solve", "content": "<p>\\(3x = 150\\), so \\(x = 50\\).</p>"},
    {"label": "Check", "content": "<p>Angles are 100° and 80°; \\(100 + 80 = 180°\\).</p>"},
    {"label": "Answer", "content": "<p>\\(x = 50\\)</p>", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "gold": {
  "title": "Gold: chain theorems together",
  "steps": [
   "Gold questions need two or more facts in a row. Find every angle you can from one theorem, then feed it into the next.",
   "A diameter gives a 90° angle in the semicircle; two radii make an isosceles triangle; a tangent meets a radius at 90° so Pythagoras can find a length.",
   "Finish by checking your angles add to 180° in a triangle, or 360° in a quadrilateral.",
  ],
  "example": {
   "question": "A, B, C lie on a circle, centre O. Angle BAC = 40° at the circumference. Find the base angle of isosceles triangle OBC.",
   "steps": [
    {"label": "Centre angle", "content": "<p>Angle BOC = \\(2 × 40 = 80°\\) (angle at the centre).</p>"},
    {"label": "Isosceles", "content": "<p>OB = OC (radii), so the base angles are equal: \\((180 − 80) ÷ 2 = 50°\\).</p>"},
    {"label": "Check", "content": "<p>\\(80 + 50 + 50 = 180°\\), the triangle's angle sum.</p>"},
    {"label": "Answer", "content": "<p>\\(50°\\)</p>", "isAnswer": True, "is_answer": True},
   ],
  },
 },
}

# ---- guided (opener + teach) ----
pd["guided"] = {
 "opener": {
  "label": "Before any circle theorems",
  "display": "A bicycle wheel rests on flat, level ground.<br>One spoke points straight down to the exact spot where the tyre touches the road.",
  "steps": [
   {
    "say": "A puzzle about a bicycle wheel. No circle theorems needed yet, just picture it.",
    "pre": "The spoke meets the road at ",
    "post": "°",
    "answer": 90,
    "hint": "The spoke points straight down and the road is flat and level.",
   },
   {
    "say": "The road only touches the wheel at that one point, so it is a <strong>tangent</strong>. The spoke is a <strong>radius</strong>. A tangent and a radius always meet at 90°. That is one of the seven circle theorems you will use today. Now a straight stick leans against the tyre at that same point, rising at 25° from the ground.",
    "pre": "The angle between the stick and the downward spoke is ",
    "post": "°",
    "answer": 65,
    "hint": "The stick splits the right angle: 90 − 25.",
   },
   {
    "say": "You just used a right angle as a stepping stone, splitting 90° into two parts. That is exactly the move the harder questions need: find one angle, then use it to reach the next.",
   },
  ],
 },
 "teach": {
  "bronze": {
   "display": "A cyclic quadrilateral PQRS has angle P = \\(95°\\) and angle Q = \\(70°\\). Find angle R and angle S.",
   "label": "Together: your first one",
   "steps": [
    say("In a cyclic quadrilateral, each pair of <strong>opposite</strong> angles adds to 180°. P is opposite R, and Q is opposite S."),
    box("P and R are opposite: R = 180 − 95 = ", 85, "Subtract 95 from 180."),
    box("Q and S are opposite: S = 180 − 70 = ", 110, "Subtract 70 from 180."),
    box("Check the first pair: 95 + 85 = ", 180, "Opposite angles should total 180."),
    box("Check the second pair: 70 + 110 = ", 180, "Opposite angles should total 180.",
        done="Both opposite pairs total 180°, so R = 85° and S = 110°."),
   ],
  },
  "silver": {
   "display": "One angle of a cyclic quadrilateral is \\(2x + 20\\) and the angle opposite it is \\(3x - 10\\). Find x, then both angles.",
   "label": "Together: the silver move",
   "steps": [
    say("Opposite angles add to 180°, so \\((2x + 20) + (3x - 10) = 180\\). Collect the x-terms and the numbers."),
    box("Add the x-terms: 2x + 3x = ", 5, "2x + 3x.", post="x"),
    box("Add the numbers: 20 + (−10) = ", 10, "20 minus 10."),
    box("Now 5x + 10 = 180, so 5x = 180 − 10 = ", 170, "Subtract 10 from 180."),
    box("x = 170 ÷ 5 = ", 34, "Divide by 5."),
    box("Check one angle: 2 × 34 + 20 = ", 88,
        "Work out 2 × 34 + 20.",
        done="The opposite angle is 3 × 34 − 10 = 92, and 88 + 92 = 180, so x = 34."),
   ],
  },
  "gold": {
   "display": "A, B and C are points on a circle, centre O. Angle BAC = \\(35°\\) at the circumference. Find the base angle of the isosceles triangle OBC.",
   "label": "Together: the gold move",
   "steps": [
    say("Two theorems chain here. First, the angle at the centre is twice the angle at the circumference. Then triangle OBC is isosceles because OB and OC are both radii."),
    box("Angle at the centre: BOC = 2 × 35 = ", 70, "Double the circumference angle."),
    box("The two base angles together: 180 − 70 = ", 110, "Subtract 70 from 180."),
    box("Each base angle: 110 ÷ 2 = ", 55, "Split equally between the two equal angles."),
    box("Check the triangle: 70 + 55 + 55 = ", 180, "Add all three angles.",
        done="The angles total 180°, so each base angle is 55°."),
   ],
  },
 },
}

with io.open("lesson_geometry-L07.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("written; keys:", list(pd.keys()))
