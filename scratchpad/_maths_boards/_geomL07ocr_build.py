# -*- coding: utf-8 -*-
"""Build the full guided + diagrams practice_data for geometry-L07 (Circle
Theorems), maths-ocr. Fresh-solved and repaired; figures programmatic."""
import json, io
import _geomL07ocr_figs as F

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_geomL07ocr_live.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_geometry-L07.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))

# ---------------------------------------------------------------- helpers
def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None:
        d["say"] = say
    if phase:
        d["phase"] = phase
    if done:
        d["done"] = done
    return d

def sayonly(say):
    return {"say": say}

CAP = F.CAP

# ---------------------------------------------------------------- BRONZE
bronze = pd["problem_bank"]["bronze"]

# b0: centre 100 -> circ 50
bronze[0]["display"] = (F.fig_centre_circ("100°", "?", "Angle at the centre is 100 degrees; the angle at the circumference on the same arc is marked with a question mark") +
    "The angle at the centre is 100°. Find the angle at the circumference standing on the same arc. " + CAP)
bronze[0]["hint"] = "The angle at the circumference is half the angle at the centre."
bronze[0]["misconceptions"] = [{
    "pattern": "doubled_not_halved",
    "message": "The angle at the circumference is HALF the angle at the centre: 100 ÷ 2 = 50°. Getting 200 means you doubled instead of halved.",
    "expect": 200, "note": "100*2"}]
bronze[0]["guided_steps"] = [
    sayonly("The angle at the centre and the angle at the circumference stand on the same arc AB. The one at the centre is always twice the one at the edge."),
    box("Write the angle at the centre: ", 100, "It is given in the question.", post="°"),
    box("Halve it to reach the circumference: 100 ÷ 2 = ", 50, "Divide the centre angle by 2.", post="°", phase="substitute"),
    box("Check by doubling your answer: 50 × 2 = ", 100, "Multiply your answer by 2; it should return the centre angle.", post="°",
        done="Doubling gives back 100°, so 50° is right."),
]

# b1: circ 35 -> centre 70
bronze[1]["display"] = (F.fig_centre_circ("?", "35°", "The angle at the circumference is 35 degrees; the angle at the centre is marked with a question mark") +
    "The angle at the circumference is 35°. Find the angle at the centre standing on the same arc. " + CAP)
bronze[1]["hint"] = "The angle at the centre is twice the angle at the circumference."
bronze[1]["misconceptions"] = [{
    "pattern": "halved_not_doubled",
    "message": "The angle at the centre is TWICE the angle at the circumference: 35 × 2 = 70°. Halving gives 17.5, which is the wrong direction.",
    "expect": 17.5, "note": "35/2"}]
bronze[1]["guided_steps"] = [
    sayonly("This time we work outwards: the centre angle is double the circumference angle."),
    box("Write the angle at the circumference: ", 35, "It is given in the question.", post="°"),
    box("Double it to reach the centre: 35 × 2 = ", 70, "Multiply the circumference angle by 2.", post="°", phase="substitute"),
    box("Check by halving your answer: 70 ÷ 2 = ", 35, "Divide your answer by 2; it should return the circumference angle.", post="°",
        done="Halving gives back 35°, so 70° is right."),
]

# b2: diameter -> ACB 90
bronze[2]["display"] = (F.fig_semi_full({"apex": 74, "names": {"L": "A", "R": "B", "T": "C"},
    "marks": [("T", "?", False)]}, "AB is a diameter and C is on the circle; angle ACB is marked with a question mark") +
    "AB is a diameter and C is a point on the circle. Find angle ACB. " + CAP)
bronze[2]["hint"] = "The angle in a semicircle is always a right angle."
bronze[2]["misconceptions"] = [{
    "pattern": "straight_angle",
    "message": "The angle in a semicircle is 90°, because the diameter AB is a straight angle of 180° at the centre and the circumference angle is half of it. 180° is the straight line itself, not the angle at C.",
    "expect": 180, "note": "confuses diameter straight angle with angle at C"}]
bronze[2]["guided_steps"] = [
    sayonly("AB is a diameter, so at the centre the angle AOB is a straight line: 180°. Angle ACB stands on the same arc, so it is half of that."),
    box("The straight angle along the diameter AB is ", 180, "A straight line is 180°.", post="°"),
    box("Angle ACB is half of it: 180 ÷ 2 = ", 90, "Halve the straight angle.", post="°", phase="substitute"),
    box("So angle ACB = ", 90, "It is the half you just found.", post="°",
        done="Any point C on the circle gives this same right angle: the angle in a semicircle is 90°."),
]

# b3: tangent-radius triangle 90 + 55 + P = 180 -> 35  (REPAIR: was duplicate 90)
bronze[3]["display"] = (F.fig_tangent_radius("55°", "?", "Tangent touches at T where it meets the radius at a right angle; angle at O is 55 degrees; angle at P marked with a question mark") +
    "A tangent touches a circle at T, and O is the centre. In triangle OTP the angle at T, where the tangent meets the radius, is 90° and the angle at O is 55°. Find the angle at P. " + CAP)
bronze[3]["solutions"] = [35]
bronze[3]["hint"] = "A tangent meets a radius at 90°, then use the triangle angle sum of 180°."
bronze[3]["misconceptions"] = [{
    "pattern": "forgot_right_angle",
    "message": "The tangent meets the radius at 90°, so 90 + 55 + P = 180 and P = 35°. Forgetting the right angle and doing 180 − 55 = 125 is the usual slip.",
    "expect": 125, "note": "180-55"}]
bronze[3]["guided_steps"] = [
    sayonly("A tangent always meets a radius at 90°, so triangle OTP has a right angle at T. The three angles of any triangle add to 180°."),
    box("Add the two known angles: 90 + 55 = ", 145, "Add the right angle and the angle at O.", post="°"),
    box("The angle at P = 180 − 145 = ", 35, "Subtract from the triangle total of 180°.", post="°", phase="substitute"),
    box("Check all three add to 180: 90 + 55 + 35 = ", 180, "Add your three angles together.", post="°",
        done="They sum to 180°, so the angle at P is 35°."),
]

# b4: same segment -> 42
bronze[4]["display"] = (F.fig_same_segment("42°", "?", "Two angles in the same segment stand on chord AB; one is 42 degrees, the other marked with a question mark") +
    "Two angles stand in the same segment on the same arc AB. One is 42°. Find the other. " + CAP)
bronze[4]["hint"] = "Angles in the same segment are equal."
bronze[4]["misconceptions"] = [{
    "pattern": "assumed_supplementary",
    "message": "Angles in the same segment are EQUAL, both 42°. They are not supplementary, so 180 − 42 = 138 is wrong.",
    "expect": 138, "note": "180-42"}]
bronze[4]["guided_steps"] = [
    sayonly("Both angles stand on the same arc AB, so they are angles in the same segment. Angles in the same segment are equal."),
    box("Write the angle you are given: ", 42, "It is stated in the question.", post="°"),
    box("Same segment means equal, so the other angle = ", 42, "Copy the equal angle.", post="°", phase="substitute"),
    box("Both are 42°, so together they make 42 + 42 = ", 84, "Add the two equal angles.", post="°",
        done="Two equal angles of 42° confirm the match."),
]

# b5: cyclic quad opposite A80 -> C100
bronze[5]["display"] = (F.fig_cyclic_quad({"A": "80°", "C": "?"}, "Cyclic quadrilateral ABCD; angle A is 80 degrees, opposite angle C marked with a question mark") +
    "ABCD is a cyclic quadrilateral. Angle A = 80°. Find angle C, the opposite angle. " + CAP)
bronze[5]["hint"] = "Opposite angles of a cyclic quadrilateral add up to 180°."
bronze[5]["misconceptions"] = [{
    "pattern": "assumed_equal",
    "message": "Opposite angles of a cyclic quadrilateral SUM to 180°, they are not equal. 180 − 80 = 100°. Copying 80 treats them as equal.",
    "expect": 80, "note": "copies angle A"}]
bronze[5]["guided_steps"] = [
    sayonly("A, B, C, D all sit on the circle, so ABCD is a cyclic quadrilateral. Opposite angles add up to 180°."),
    box("Write the given angle A: ", 80, "It is stated in the question.", post="°"),
    box("Opposite angles sum to 180, so C = 180 − 80 = ", 100, "Subtract angle A from 180°.", post="°", phase="substitute"),
    box("Check the pair adds to 180: 80 + 100 = ", 180, "Add the two opposite angles.", post="°",
        done="The opposite pair sums to 180°, so angle C = 100°."),
]

# b6: centre 160 -> circ 80
bronze[6]["display"] = (F.fig_centre_circ("160°", "?", "Angle at the centre is 160 degrees; angle at the circumference on the same arc marked with a question mark") +
    "The angle at the centre is 160°. Find the angle at the circumference on the same arc. " + CAP)
bronze[6]["hint"] = "Halve the angle at the centre to get the angle at the circumference."
bronze[6]["misconceptions"] = [{
    "pattern": "doubled_not_halved",
    "message": "Halve the centre angle: 160 ÷ 2 = 80°. Doubling gives 320, the wrong direction.",
    "expect": 320, "note": "160*2"}]
bronze[6]["guided_steps"] = [
    sayonly("Same arc, so the circumference angle is half the centre angle."),
    box("Write the angle at the centre: ", 160, "It is given in the question.", post="°"),
    box("Halve it: 160 ÷ 2 = ", 80, "Divide the centre angle by 2.", post="°", phase="substitute"),
    box("Check by doubling: 80 × 2 = ", 160, "Multiply your answer by 2.", post="°",
        done="Doubling returns 160°, so 80° is right."),
]

# b7: semicircle triangle 90 + 50 + x = 180 -> 40  (reword)
bronze[7]["display"] = (F.fig_semi_full({"apex": 66, "names": {"L": "A", "R": "B", "T": "C"},
    "marks": [("T", "", True), ("L", "50°", False), ("R", "?", False)]},
    "Triangle in a semicircle; the angle at C is a right angle, the angle at A is 50 degrees, the angle at B marked with a question mark") +
    "A triangle is drawn inside a semicircle, so one of its angles is 90°. Another angle is 50°. Find the third angle. " + CAP)
bronze[7]["hint"] = "One angle is 90° (semicircle), so the three angles sum to 180°."
bronze[7]["misconceptions"] = [{
    "pattern": "forgot_right_angle",
    "message": "The angle in the semicircle is 90°, so 90 + 50 + x = 180 and x = 40°. Forgetting the right angle gives 180 − 50 = 130.",
    "expect": 130, "note": "180-50"}]
bronze[7]["guided_steps"] = [
    sayonly("The triangle sits in a semicircle, so one angle is 90°. The three angles add to 180°."),
    box("Add the two known angles: 90 + 50 = ", 140, "Add the right angle and the 50° angle.", post="°"),
    box("The third angle = 180 − 140 = ", 40, "Subtract from the triangle total of 180°.", post="°", phase="substitute"),
    box("Check: 90 + 50 + 40 = ", 180, "Add all three angles.", post="°",
        done="They sum to 180°, so the third angle is 40°."),
]

# ---------------------------------------------------------------- SILVER
silver = pd["problem_bank"]["silver"]

# s0: cyclic quad 2x + (2x+20) = 180 -> x = 40
silver[0]["display"] = (F.fig_cyclic_quad({"A": "2x", "B": "3x", "C": "2x+20", "D": "y"},
    "Cyclic quadrilateral with angles 2x, 3x, 2x+20 and y; opposite pairs sum to 180 degrees") +
    "A cyclic quadrilateral has angles \\(2x\\), \\(3x\\), \\(2x+20\\), and \\(y\\). Opposite pairs sum to 180°. Given that \\(2x\\) and \\(2x+20\\) are opposite, find \\(x\\). " + CAP)
silver[0]["hint"] = "Add the opposite pair 2x and 2x+20 and set the sum to 180°."
silver[0]["misconceptions"] = [{
    "pattern": "used_360",
    "message": "Opposite angles SUM to 180°, not 360°. 2x + (2x + 20) = 180 gives 4x = 160 and x = 40. Using 360 gives 4x = 340 and x = 85.",
    "expect": 85, "note": "(360-20)/4"}]
silver[0]["guided_steps"] = [
    sayonly("The opposite pair is \\(2x\\) and \\(2x + 20\\). Opposite angles of a cyclic quadrilateral sum to 180°."),
    box("Add the coefficients of x in 2x + (2x + 20): ", 4, "2x plus 2x makes how many x?"),
    box("So 4x + 20 = 180. Subtract 20: 4x = ", 160, "Take 20 from 180.", phase="substitute"),
    box("x = 160 ÷ 4 = ", 40, "Divide by 4."),
    box("Check: 2(40) + (2(40) + 20) = 80 + 100 = ", 180, "Add the two opposite angles.", post="°",
        done="The opposite pair sums to 180°, so x = 40."),
]

# s1: alt segment 55
silver[1]["display"] = (F.fig_alt_segment("55°", "?", "Tangent meets a chord at 55 degrees; the angle in the alternate segment is marked with a question mark") +
    "A tangent makes an angle of 55° with a chord at the point of contact. Find the angle in the alternate segment. " + CAP)
silver[1]["hint"] = "The angle in the alternate segment equals the tangent-chord angle."
silver[1]["misconceptions"] = [{
    "pattern": "used_90_complement",
    "message": "By the alternate segment theorem the angle EQUALS the tangent-chord angle: 55°. Subtracting from 90 (giving 35) confuses it with the tangent-radius right angle.",
    "expect": 35, "note": "90-55"}]
silver[1]["guided_steps"] = [
    sayonly("The alternate segment theorem: the angle between a tangent and a chord equals the angle in the alternate segment (subtended by that chord on the far arc)."),
    box("Write the tangent-chord angle: ", 55, "It is stated in the question.", post="°"),
    box("The alternate segment angle equals it, so it = ", 55, "Copy the equal angle.", post="°", phase="substitute"),
    box("Both equal 55°, so together they make 55 + 55 = ", 110, "Add the two equal angles.", post="°",
        done="Equal angles of 55° confirm the alternate segment result."),
]

# s2: two tangents, angle between = 140  (REPAIR: was 40, wrong quantity + duplicate)
silver[2]["display"] = (F.fig_two_tangents("angle", "Two tangents from external point P; the line PO makes 70 degrees with each tangent; the angle between the two tangents is marked with a question mark") +
    "Two tangents are drawn from an external point P to a circle, centre O. The line PO makes an angle of 70° with each tangent. Find the angle between the two tangents. " + CAP)
silver[2]["solutions"] = [140]
silver[2]["hint"] = "The line to the centre bisects the angle between the tangents, so double the 70°."
silver[2]["misconceptions"] = [{
    "pattern": "gave_centre_angle",
    "message": "The angle between the two tangents is at P: it is 2 × 70° = 140°. 40° is the angle at the centre O (found from 360 − 90 − 90 − 140), a different angle.",
    "expect": 40, "note": "the centre angle, not the angle at P"}]
silver[2]["guided_steps"] = [
    sayonly("PO bisects the angle between the two tangents, so each half is 70°. The full angle at P is twice one half."),
    box("One half of the angle at P is 70°. Write it: ", 70, "It is the angle PO makes with a tangent.", post="°"),
    box("The full angle between the tangents is twice this: 70 × 2 = ", 140, "Double the half-angle.", post="°", phase="substitute"),
    box("Check with the kite: 90 + 90 + 140 + centre = 360, so the centre angle = 360 − 320 = ", 40, "Subtract the known three from 360°.", post="°",
        done="The 140° at P and the 40° at O with the two 90° radii close the kite to 360°, so 140° is right."),
]

# s3: reflex centre 260 -> circ 130
silver[3]["display"] = (F.fig_centre_reflex("260°", "?", "Reflex angle at the centre is 260 degrees; the angle at the circumference on the same major arc marked with a question mark") +
    "The reflex angle at the centre is 260°. Find the angle at the circumference standing on the same arc. " + CAP)
silver[3]["hint"] = "Halve the reflex angle at the centre."
silver[3]["misconceptions"] = [{
    "pattern": "used_non_reflex",
    "message": "The 260° reflex angle stands on the same arc as the circumference angle, so halve it: 130°. Using the non-reflex 100° (from 360 − 260) and halving gives 50°, the wrong arc.",
    "expect": 50, "note": "(360-260)/2"}]
silver[3]["guided_steps"] = [
    sayonly("The circumference angle is half the centre angle it stands on. Here that centre angle is the reflex 260°, not the smaller one."),
    box("Write the reflex angle at the centre: ", 260, "It is given in the question.", post="°"),
    box("Halve it: 260 ÷ 2 = ", 130, "Divide the reflex angle by 2.", post="°", phase="substitute"),
    box("Check by doubling: 130 × 2 = ", 260, "Multiply your answer by 2.", post="°",
        done="Doubling returns the reflex 260°, so 130° is right."),
]

# s4: two tangents equal PB = 8
silver[4]["display"] = (F.fig_two_tangents("length", "Two tangents from point P; PA is 8 cm, PB marked with a question mark") +
    "Two tangents are drawn from a point P to a circle, touching at A and B. PA = 8 cm. Find PB. " + CAP)
silver[4]["hint"] = "Two tangents from the same point are equal in length."
silver[4]["misconceptions"] = []
silver[4]["guided_steps"] = [
    sayonly("Two tangents drawn from the same external point are always equal in length."),
    box("Write the length PA: ", 8, "It is stated in the question."),
    box("PB equals PA, so PB = ", 8, "Copy the equal length.", phase="substitute"),
    box("Together the two tangents measure 8 + 8 = ", 16, "Add the two equal lengths.",
        done="Equal tangents of 8 cm confirm PB = 8 cm."),
]

# s5: circ x, centre 3x-20 = 2x -> x = 20
silver[5]["display"] = (F.fig_centre_circ("3x − 20", "x", "Angle at the circumference is x; angle at the centre is 3x minus 20") +
    "The angle at the circumference is \\(x\\) and the angle at the centre on the same arc is \\(3x - 20\\). Find \\(x\\). " + CAP)
silver[5]["hint"] = "Set the centre angle equal to twice the circumference angle."
silver[5]["misconceptions"] = [{
    "pattern": "set_equal_not_double",
    "message": "The centre angle is TWICE the circumference angle: 3x − 20 = 2x, so x = 20. Setting them equal gives 3x − 20 = x and x = 10.",
    "expect": 10, "note": "3x-20=x -> 2x=20 -> x=10"}]
silver[5]["guided_steps"] = [
    sayonly("The centre angle is twice the circumference angle, so \\(3x - 20 = 2x\\)."),
    box("Subtract 2x from both sides. 3x − 2x leaves how many x? ", 1, "3x take away 2x."),
    box("So x − 20 = 0, giving x = ", 20, "Add 20 to both sides.", phase="substitute"),
    box("Circumference angle = x = ", 20, "It is the x you just found.", post="°"),
    box("Centre angle = 3(20) − 20 = ", 40, "Work out 3 times 20 then take 20.", post="°",
        done="40° is twice 20°, so x = 20 is right."),
]

# s6: semicircle 90 + 28 + ACB = 180 -> 62
silver[6]["display"] = (F.fig_semi_full({"apex": 112, "names": {"L": "B", "R": "C", "T": "A"},
    "marks": [("T", "", True), ("L", "28°", False), ("R", "?", False)]},
    "Triangle in a semicircle; angle BAC is a right angle, angle ABC is 28 degrees, angle ACB marked with a question mark") +
    "In a semicircle, angle BAC = 90° and angle ABC = 28°. Find angle ACB. " + CAP)
silver[6]["hint"] = "The right angle is 90°, so the triangle's angles sum to 180°."
silver[6]["misconceptions"] = [{
    "pattern": "forgot_right_angle",
    "message": "Angle BAC is the 90° right angle in the semicircle, so 90 + 28 + ACB = 180 and ACB = 62°. Forgetting the 90° and doing 180 − 28 gives 152.",
    "expect": 152, "note": "180-28"}]
silver[6]["guided_steps"] = [
    sayonly("Angle BAC = 90° is the right angle in the semicircle. The three angles of the triangle add to 180°."),
    box("Add the two known angles: 90 + 28 = ", 118, "Add the right angle and the 28° angle.", post="°"),
    box("Angle ACB = 180 − 118 = ", 62, "Subtract from the triangle total of 180°.", post="°", phase="substitute"),
    box("Check: 90 + 28 + 62 = ", 180, "Add all three angles.", post="°",
        done="They sum to 180°, so angle ACB = 62°."),
]

# ---------------------------------------------------------------- GOLD
gold = pd["problem_bank"]["gold"]

# g0: 8x-10 = 2(3x+5) -> x = 10
gold[0]["display"] = (F.fig_centre_circ("8x − 10", "3x + 5", "Angle at the centre is 8x minus 10; angle at the circumference is 3x plus 5") +
    "The angle at the centre is \\(8x - 10\\) and the angle at the circumference on the same arc is \\(3x + 5\\). Using the fact that the centre angle is twice the circumference angle, find \\(x\\). " + CAP)
gold[0]["hint"] = "Set centre = 2 × circumference and expand the bracket."
gold[0]["misconceptions"] = [{
    "pattern": "forgot_factor_2",
    "message": "The centre angle is twice the circumference: 8x − 10 = 2(3x + 5) = 6x + 10, so x = 10. Forgetting the factor of 2 (8x − 10 = 3x + 5) gives 5x = 15 and x = 3.",
    "expect": 3, "note": "8x-10=3x+5 -> 5x=15 -> x=3"}]
gold[0]["guided_steps"] = [
    sayonly("Centre is twice circumference, so \\(8x - 10 = 2(3x + 5)\\). Expand the bracket first."),
    box("Expand: 2 × (3x + 5) gives how many x? ", 6, "2 times 3x."),
    box("So 8x − 10 = 6x + 10. Subtract 6x: 8x − 6x leaves how many x? ", 2, "8x take away 6x.", phase="substitute"),
    box("2x − 10 = 10, so 2x = 20 and x = ", 10, "Add 10, then divide by 2."),
    box("Check: centre 8(10) − 10 = 70, circumference 3(10) + 5 = 35, and 70 ÷ 2 = ", 35, "Halve the centre angle.", post="°",
        done="35° matches the circumference angle, so x = 10."),
]

# g1: cyclic quad opposite 4x & 5x -> x = 20  (REPAIR: degenerate 3x,4x,5x,6x)
gold[1]["display"] = (F.fig_cyclic_quad({"A": "4x", "C": "5x"},
    "Cyclic quadrilateral with one pair of opposite angles 4x and 5x") +
    "A cyclic quadrilateral has one pair of opposite angles equal to \\(4x\\) and \\(5x\\). Find \\(x\\). " + CAP)
gold[1]["hint"] = "Opposite angles sum to 180°, so 4x + 5x = 180."
gold[1]["misconceptions"] = [{
    "pattern": "used_360",
    "message": "Opposite angles of a cyclic quadrilateral sum to 180°: 4x + 5x = 180, so 9x = 180 and x = 20. Using 360° gives 9x = 360 and x = 40.",
    "expect": 40, "note": "360/9"}]
gold[1]["guided_steps"] = [
    sayonly("The pair \\(4x\\) and \\(5x\\) are opposite angles of the cyclic quadrilateral, so they sum to 180°."),
    box("Add the pair: 4x + 5x gives how many x? ", 9, "4x plus 5x."),
    box("So 9x = 180, and x = 180 ÷ 9 = ", 20, "Divide 180 by 9.", phase="substitute"),
    box("The first angle 4x = 4 × 20 = ", 80, "Multiply 4 by your x.", post="°"),
    box("The opposite angle 5x = 5 × 20 = 100, and 80 + 100 = ", 180, "Add the opposite pair.", post="°",
        done="Opposite angles sum to 180°, so x = 20."),
]

# g2: alt segment 48  (reword)
gold[2]["display"] = (F.fig_alt_segment("48°", "?", "Tangent meets chord TA at 48 degrees; the angle TBA in the alternate segment is marked with a question mark") +
    "A tangent touches a circle at T, and TA is a chord. The angle between the tangent and TA is 48°. B is a point on the major arc. Find the angle TBA in the alternate segment. " + CAP)
gold[2]["hint"] = "The alternate segment angle equals the tangent-chord angle."
gold[2]["misconceptions"] = [{
    "pattern": "used_90_complement",
    "message": "By the alternate segment theorem, angle TBA equals the tangent-chord angle: 48°. Subtracting from 90 (giving 42) confuses it with the tangent-radius right angle.",
    "expect": 42, "note": "90-48"}]
gold[2]["guided_steps"] = [
    sayonly("The alternate segment theorem: the angle between the tangent and chord TA equals angle TBA in the alternate segment."),
    box("Write the tangent-chord angle: ", 48, "It is stated in the question.", post="°"),
    box("Angle TBA equals it, so it = ", 48, "Copy the equal angle.", post="°", phase="substitute"),
    box("Both equal 48°, so together 48 + 48 = ", 96, "Add the two equal angles.", post="°",
        done="Equal angles of 48° confirm the alternate segment result."),
]

# g3: intersecting chords 3*8 = 4*PD -> 6
gold[3]["display"] = (F.fig_intersecting_chords("Chords AB and CD cross at P inside the circle; PA is 3, PB is 8, PC is 4, PD marked with a question mark") +
    "Two chords AB and CD intersect at P inside a circle. PA = 3, PB = 8, PC = 4. Find PD. " + CAP)
gold[3]["hint"] = "Use PA × PB = PC × PD."
gold[3]["misconceptions"] = [{
    "pattern": "added_not_multiplied",
    "message": "Intersecting chords multiply: PA × PB = PC × PD, so 3 × 8 = 4 × PD and PD = 6. Adding instead (3 + 8 = 4 + PD) gives PD = 7.",
    "expect": 7, "note": "3+8-4"}]
gold[3]["guided_steps"] = [
    sayonly("When two chords cross inside a circle, the products of their two parts are equal: \\(PA \\times PB = PC \\times PD\\)."),
    box("Multiply the first chord's parts: 3 × 8 = ", 24, "Work out 3 times 8."),
    box("So 4 × PD = 24, and PD = 24 ÷ 4 = ", 6, "Divide 24 by 4.", phase="substitute"),
    box("Check: PC × PD = 4 × 6 = ", 24, "Multiply the other chord's parts.",
        done="24 matches PA × PB, so PD = 6."),
]

# g4: tangent-secant 12^2 = 8*PB -> 18
gold[4]["display"] = (F.fig_tangent_secant("Tangent PT and secant through A and B from external point P; PT is 12, PA is 8, PB marked with a question mark") +
    "A tangent from P touches a circle at T. A secant from P passes through A and B on the circle. PT = 12, PA = 8. Find PB. " + CAP)
gold[4]["hint"] = "Use PT² = PA × PB with the whole secant PB."
gold[4]["misconceptions"] = [{
    "pattern": "used_chord_part",
    "message": "The whole secant is used: PT² = PA × PB, so 144 = 8 × PB and PB = 18 (measured P to B). Working out the chord part AB = 144 ÷ 8 = 18 and then adding PA gives 26, which is too far.",
    "expect": 26, "note": "144/8 = 18 taken as AB, +8"}]
gold[4]["guided_steps"] = [
    sayonly("For a tangent and a secant from the same point: \\(PT^2 = PA \\times PB\\), where PB is the whole secant from P to the far point B."),
    box("Square the tangent: 12² = ", 144, "12 times 12."),
    box("So 8 × PB = 144, and PB = 144 ÷ 8 = ", 18, "Divide 144 by 8.", phase="substitute"),
    box("Check: PA × PB = 8 × 18 = ", 144, "Multiply to confirm it equals PT².",
        done="144 equals PT², so PB = 18."),
]

# ---------------------------------------------------------------- tier descriptions
pd["problem_bank"]["bronze_description"] = "One theorem, one step: name the rule the figure shows and read off the angle."
pd["problem_bank"]["silver_description"] = "Two steps or a short equation: combine a theorem with the angle sum, or solve for x."
pd["problem_bank"]["gold_description"] = "Form and solve an equation, or use the chord and tangent length rules."

# ---------------------------------------------------------------- tier_guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one theorem, one step",
        "steps": [
            "Name the theorem the figure shows: angle at centre, semicircle, same segment, cyclic quadrilateral, or tangent.",
            "Angle at the centre = 2 × angle at the circumference, so halve to go inwards, double to go outwards.",
            "Semicircle angle = 90°; same-segment angles are equal; opposite cyclic-quad angles sum to 180°."
        ],
        "example": {
            "question": "The angle at the centre is 130°. Find the angle at the circumference.",
            "steps": [
                {"label": "Step 1", "content": "<p>The circumference angle is half the centre angle.</p>"},
                {"label": "Step 2", "content": "<p>130 ÷ 2 = 65.</p>"},
                {"label": "Check", "content": "<p>Double back: 65 × 2 = 130. ✓</p>"},
                {"label": "Answer", "content": "<p>65°</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two steps or a short equation",
        "steps": [
            "Use one theorem to get an angle, then the triangle sum (180°) or a straight line (180°) for the next.",
            "For algebra, turn the theorem into an equation: opposite angles 2x and 2x+20 give 2x + (2x+20) = 180.",
            "Solve for x, then substitute back to find the angle asked for, and check it fits."
        ],
        "example": {
            "question": "Angle at circumference = x, angle at centre = 4x − 30. Find x.",
            "steps": [
                {"label": "Step 1", "content": "<p>Centre = 2 × circumference: 4x − 30 = 2x.</p>"},
                {"label": "Step 2", "content": "<p>2x = 30, so x = 15.</p>"},
                {"label": "Check", "content": "<p>Centre = 4(15) − 30 = 30 = 2 × 15. ✓</p>"},
                {"label": "Answer", "content": "<p>x = 15</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: form and solve an equation",
        "steps": [
            "Write the theorem as an equation in x, expanding any brackets: centre 8x − 10 = 2(3x + 5).",
            "Collect like terms and solve for x, keeping signs under control.",
            "For chords and tangents from a point, use PA × PB = PC × PD or PT² = PA × PB."
        ],
        "example": {
            "question": "Circumference angle = 2x + 5, centre angle = 5x − 5. Find x.",
            "steps": [
                {"label": "Step 1", "content": "<p>Centre = 2 × circumference: 5x − 5 = 2(2x + 5).</p>"},
                {"label": "Step 2", "content": "<p>5x − 5 = 4x + 10, so x = 15.</p>"},
                {"label": "Check", "content": "<p>Centre = 5(15) − 5 = 70, circumference = 2(15) + 5 = 35, and 70 = 2 × 35. ✓</p>"},
                {"label": "Answer", "content": "<p>x = 15</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------- guided (opener + teach)
opener_svg = F.fig_centre_circ("80°", "?", "From the centre of a circular gallery the painting fills 80 degrees; from the wall it fills the angle marked with a question mark")
pd["guided"] = {
    "opener": {
        "display": (opener_svg +
            "Two guides stand in a circular gallery, both looking at the same painting on the curved wall (the chord AB).<br>"
            "From the <strong>centre</strong> of the room the painting fills an angle of 80°.<br>"
            "From a spot <strong>on the wall</strong> (point C), the same painting fills exactly half that angle."),
        "steps": [
            box("Half of 80° is ", 40, "Halve 80.", post="°"),
            sayonly("Now the gallery is wider. From the centre the next painting fills 100°."),
            box("Half of 100° is ", 50, "Halve 100.", post="°"),
            sayonly("You just used the biggest circle theorem: the <strong>angle at the centre is twice the angle at the circumference</strong> standing on the same arc. To go from the centre to the edge, halve; to go back out, double. A special case: when the painting is a whole diameter the centre angle is 180°, so the edge angle is 90°, the angle in a semicircle."),
        ],
    },
    "teach": {
        "bronze": {
            "display": (F.fig_semi_full({"apex": 72, "names": {"L": "A", "R": "B", "T": "C"},
                "marks": [("T", "", True), ("L", "55°", False), ("R", "?", False)]},
                "AB is a diameter, C on the circle; angle at C is a right angle, angle CAB is 55 degrees, angle ABC marked with a question mark") +
                "AB is a diameter and C is on the circle. Angle CAB = 55°. Find angle ACB, then angle ABC. " + CAP),
            "steps": [
                sayonly("AB is a diameter, so the angle at C is the angle in a semicircle."),
                box("The angle in a semicircle is a right angle. Write angle ACB: ", 90, "A semicircle angle is 90°.", post="°"),
                box("Angles in a triangle sum to 180. So far 90 + 55 = ", 145, "Add the right angle and 55°.", post="°"),
                box("The last angle ABC = 180 − 145 = ", 35, "Subtract from 180°.", post="°"),
                box("Check all three: 90 + 55 + 35 = ", 180, "Add your three angles.", post="°",
                    done="They sum to 180°. Gone: the semicircle gives the right angle, the triangle sum gives the rest."),
            ],
        },
        "silver": {
            "display": (F.fig_centre_circ("4x − 30", "x", "Angle at the circumference is x; angle at the centre is 4x minus 30") +
                "The angle at the circumference is \\(x\\) and the angle at the centre on the same arc is \\(4x - 30\\). Find \\(x\\), then both angles. " + CAP),
            "steps": [
                sayonly("The centre angle is twice the circumference angle, so \\(4x - 30 = 2x\\)."),
                box("Subtract 2x from both sides. 4x − 2x leaves how many x? ", 2, "4x take away 2x."),
                box("So 2x − 30 = 0, giving 2x = ", 30, "Add 30 to both sides."),
                box("x = 30 ÷ 2 = ", 15, "Divide by 2."),
                box("Centre angle = 4(15) − 30 = ", 30, "Work out 4 times 15 then take 30.", post="°",
                    done="30° is twice the circumference 15°. Gone: turning the theorem into an equation is the whole silver move."),
            ],
        },
        "gold": {
            "display": (F.fig_intersecting_chords_custom("4", "9", "6", "?", "Chords AB and CD cross at P; PA is 4, PB is 9, PC is 6, PD marked with a question mark") +
                "Two chords AB and CD cross at P inside a circle. PA = 4, PB = 9, PC = 6. Find PD. " + CAP),
            "steps": [
                sayonly("When two chords cross, the products of their parts are equal: \\(PA \\times PB = PC \\times PD\\)."),
                box("Multiply the first chord's parts: 4 × 9 = ", 36, "Work out 4 times 9."),
                box("The other chord: PC × PD = 6 × PD, and this equals 36, so 6 × PD = ", 36, "It matches the first product."),
                box("PD = 36 ÷ 6 = ", 6, "Divide 36 by 6."),
                box("Check both products match: 6 × 6 = ", 36, "Multiply 6 by your PD.",
                    done="Both products are 36. Gone: equal products is the whole intersecting-chords idea."),
            ],
        },
    },
}
# ---------------------------------------------------------------- method_card (slim)
pd["method_card"] = {
    "title": "Circle Theorems",
    "steps": [
        "Angle at the centre = 2 × angle at the circumference (same arc).",
        "Angle in a semicircle = 90°; angles in the same segment are equal.",
        "Cyclic quadrilateral: opposite angles sum to 180°.",
        "Tangent meets radius at 90°; tangent-chord = alternate segment angle.",
    ],
    "content": "<p>Spot which theorem the figure shows, then read off the angle or set up a short equation.</p><p>The headline rule: the <strong>angle at the centre is twice the angle at the circumference</strong> on the same arc. A special case is the <strong>angle in a semicircle = 90°</strong>. Angles in the <strong>same segment are equal</strong>. In a <strong>cyclic quadrilateral, opposite angles sum to 180°</strong>. A <strong>tangent meets a radius at 90°</strong>, two tangents from a point are equal, and the <strong>alternate segment</strong> angle equals the tangent-chord angle.</p>",
    "example": "<p><strong>Angle at the centre = 120°. Find the angle at the circumference on the same arc.</strong></p><p>120 ÷ 2 = 60°.</p>",
}

# topic_links: preserve (was empty prerequisites); leave as-is

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", OUT)
print("bronze sols:", [p["solutions"] for p in pd["problem_bank"]["bronze"]])
print("silver sols:", [p["solutions"] for p in pd["problem_bank"]["silver"]])
print("gold sols:", [p["solutions"] for p in pd["problem_bank"]["gold"]])
