# maths-aqa / geometry / L07 - Circle Theorems

## bronze[0] (input: single_value, main-box unit: (none))
Q: OABC124°?Diagram not drawn accurately The angle at the centre of a circle is \(124°\). Find the angle at the circumference subtended by the same arc.
   - intro: The angle at the centre is twice the angle at the circumference on the same arc.
   - ask: How many circumference angles make the centre angle? Type the multiplier:  [box expects 2 (NO unit label)]
   - ask: So circumference = 124 ÷ 2 =  [box expects 62 (NO unit label)]
   - ask: Check by doubling back: 62 × 2 =  [box expects 124 (NO unit label)]

## bronze[1] (input: single_value, main-box unit: (none))
Q: OABC?48°Diagram not drawn accurately The angle at the circumference is \(48°\). Find the angle at the centre subtended by the same arc.
   - intro: The angle at the centre is twice the angle at the circumference on the same arc.
   - ask: Type the multiplier linking centre to circumference:  [box expects 2 (NO unit label)]
   - ask: So centre = 48 × 2 =  [box expects 96 (NO unit label)]
   - ask: Check by halving: 96 ÷ 2 =  [box expects 48 (NO unit label)]

## bronze[2] (input: single_value, main-box unit: (none))
Q: ABCO?Diagram not drawn accurately AB is a diameter. C is on the circumference. Find angle ACB.
   - intro: AB is a diameter, so C sits in a semicircle.
   - ask: A diameter is a straight line. How many degrees is a straight line?  [box expects 180 (NO unit label)]
   - ask: The angle in the semicircle is half of that: 180 ÷ 2 =  [box expects 90 (NO unit label)]
   - ask: So angle ACB is a right angle. Type it:  [box expects 90 (NO unit label)]

## bronze[3] (input: single_value, main-box unit: (none))
Q: ABCD72°?Diagram not drawn accurately In a cyclic quadrilateral, one angle is \(72°\). Find the opposite angle.
   - intro: Opposite angles of a cyclic quadrilateral add up to 180°.
   - ask: What total do the opposite pair make?  [box expects 180 (NO unit label)]
   - ask: So the opposite angle = 180 − 72 =  [box expects 108 (NO unit label)]
   - ask: Check the pair: 72 + 108 =  [box expects 180 (NO unit label)]

## bronze[4] (input: single_value, main-box unit: (none))
Q: ABPQ35°xDiagram not drawn accurately Two angles in the same segment stand on the chord AB. One is \(35°\) and the other is \(x\). Find \(x\).
   - intro: Angles in the same segment, standing on the same chord, are equal.
   - ask: Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary:  [box expects 1 (NO unit label)]
   - ask: They are equal, and one is 35°, so x =  [box expects 35 (NO unit label)]
   - ask: Check the pair match: 35 and  [box expects 35 (NO unit label)]

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: OT?Diagram not drawn accurately A tangent meets a radius at point T. The angle between them is:

## bronze[6] (input: single_value, main-box unit: (none))
Q: OABC150°?Diagram not drawn accurately The angle at the centre is \(150°\). Find the angle at the circumference.
   - intro: The angle at the centre is twice the angle at the circumference on the same arc.
   - ask: Type the multiplier linking them:  [box expects 2 (NO unit label)]
   - ask: So circumference = 150 ÷ 2 =  [box expects 75 (NO unit label)]
   - ask: Check by doubling: 75 × 2 =  [box expects 150 (NO unit label)]

## bronze[7] (input: single_value, main-box unit: (none))
Q: ABCO32°?Diagram not drawn accurately Angle ACB = \(90°\) (C on the circle, AB is a diameter). Angle BAC = \(32°\). Find angle ABC.
   - intro: Angle ACB is 90° (angle in the semicircle). The three angles of triangle ACB add to 180°.
   - ask: Add the two known angles: 90 + 32 =  [box expects 122 (NO unit label)]
   - ask: Subtract from 180: 180 − 122 =  [box expects 58 (NO unit label)]
   - ask: Check all three: 90 + 32 + 58 =  [box expects 180 (NO unit label)]

## silver[0] (input: single_value, main-box unit: (none))
Q: ABCD3x2x + 10x + 40100°Diagram not drawn accurately A cyclic quadrilateral has angles \(3x\), \(2x + 10\), \(x + 40\) and \(100°\). The angles \(3x\) and \(x + 40\) are opposite. Find \(x\).
   - intro: Opposite angles of a cyclic quadrilateral add to 180°. Here 3x and x + 40 are the opposite pair.
   - ask: Add the opposite pair's x terms: 3x + x =  [box expects 4 (unit label: 'x')]
   - ask: The number part is 40, so 4x + 40 = 180. Take 40 across: 180 − 40 =  [box expects 140 (NO unit label)]
   - ask: Now 4x = 140, so x = 140 ÷ 4 =  [box expects 35 (NO unit label)]
   - ask: Check the pair: 3(35) + (35 + 40) = 105 + 75 =  [box expects 180 (NO unit label)]

## silver[1] (input: single_value, main-box unit: (none))
Q: ABC64°?Diagram not drawn accurately The angle between a tangent and a chord at the point of contact is \(64°\). Find the angle in the alternate segment.
   - intro: The alternate segment theorem: the angle between a tangent and a chord equals the angle in the alternate segment.
   - ask: Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary:  [box expects 1 (NO unit label)]
   - ask: They are equal, and the tangent-chord angle is 64°, so the alternate segment angle =  [box expects 64 (NO unit label)]
   - ask: Check the pair are equal: 64 and  [box expects 64 (NO unit label)]

## silver[2] (input: single_value, main-box unit: (none))
Q: OABCx + 50xDiagram not drawn accurately O is the centre. Angle AOB = \(x + 50\). Angle ACB = \(x\) (C on the circumference, same arc). Find \(x\).
   - intro: The angle at the centre is twice the angle at the circumference on the same arc: x + 50 = 2x.
   - ask: Take one x from each side. 2x − x leaves how many x?  [box expects 1 (unit label: 'x')]
   - ask: So 50 = x, meaning x =  [box expects 50 (NO unit label)]
   - ask: Check the centre angle: x + 50 = 50 + 50 =  [box expects 100 (NO unit label)]
   - ask: And twice the circumference: 2 × 50 =  [box expects 100 (NO unit label)]

## silver[3] (input: single_value, main-box unit: (none))
Q: TABO12 cm?Diagram not drawn accurately Two tangents from an external point T touch the circle at A and B. TA = \(12\) cm. Find TB.
   - intro: Two tangents drawn from the same external point are equal in length.
   - ask: TA and TB come from the same point T. Type 1 if they are equal, 2 if not:  [box expects 1 (NO unit label)]
   - ask: They are equal, and TA = 12 cm, so TB =  [box expects 12 (NO unit label)]
   - ask: Check the pair match: 12 and  [box expects 12 (NO unit label)]

## silver[4] (input: single_value, main-box unit: (none))
Q: BCO140°?Diagram not drawn accurately O is the centre of the circle. Angle BOC = \(140°\). Find the reflex angle BOC.
   - intro: Angles around the centre point make a full turn of 360°. The reflex angle is the rest of the turn.
   - ask: A full turn is:  [box expects 360 (NO unit label)]
   - ask: Reflex BOC = 360 − 140 =  [box expects 220 (NO unit label)]
   - ask: Check they complete a turn: 140 + 220 =  [box expects 360 (NO unit label)]

## silver[5] (input: single_value, main-box unit: (none))
Q: ABO52°?Diagram not drawn accurately The angle between a tangent at A and chord AB is \(52°\). O is the centre. Find angle AOB.
   - intro: Alternate segment: the angle in the alternate segment equals the tangent-chord angle, 52°. Then the angle at the centre is twice the angle at the circumference.
   - ask: Angle in the alternate segment = tangent-chord angle =  [box expects 52 (NO unit label)]
   - ask: Angle at the centre is twice that: 2 × 52 =  [box expects 104 (NO unit label)]
   - ask: Check by halving: 104 ÷ 2 =  [box expects 52 (NO unit label)]

## silver[6] (input: single_value, main-box unit: (none))
Q: ABC40°?55°Diagram not drawn accurately Points A, B, C lie on a circle. Angle BAC = \(40°\) and angle BCA = \(55°\). Find angle ABC.
   - intro: A, B and C are just three angles of a triangle, which add to 180°.
   - ask: Add the two known angles: 40 + 55 =  [box expects 95 (NO unit label)]
   - ask: Subtract from 180: 180 − 95 =  [box expects 85 (NO unit label)]
   - ask: Check all three: 40 + 55 + 85 =  [box expects 180 (NO unit label)]

## gold[0] (input: single_value, main-box unit: (none))
Q: ABOC?25°Diagram not drawn accurately O is the centre. A, B, C are on the circle. Angle OAB = \(25°\). Find angle ACB (C on the major arc).
   - intro: OA and OB are both radii, so triangle OAB is isosceles: the base angles are equal.
   - ask: Base angles equal, so angle OBA =  [box expects 25 (NO unit label)]
   - ask: Angles in triangle OAB add to 180. Centre angle AOB = 180 − 25 − 25 =  [box expects 130 (NO unit label)]
   - ask: Angle at the circumference is half the centre: 130 ÷ 2 =  [box expects 65 (NO unit label)]
   - ask: Check by doubling: 65 × 2 =  [box expects 130 (NO unit label)]

## gold[1] (input: single_value, main-box unit: (none))
Q: ABCD3x + 102x + 20Diagram not drawn accurately A, B, C, D lie on a circle. Angle ABC = \(3x + 10\), angle ADC = \(2x + 20\). Find angle ABC.
   - intro: ABC and ADC are opposite angles of the cyclic quadrilateral, so they add to 180°.
   - ask: Add the x terms: 3x + 2x =  [box expects 5 (unit label: 'x')]
   - ask: Add the numbers: 10 + 20 =  [box expects 30 (NO unit label)]
   - ask: So 5x + 30 = 180. Take 30 across: 180 − 30 =  [box expects 150 (NO unit label)]
   - ask: Now 5x = 150, so x = 150 ÷ 5 =  [box expects 30 (NO unit label)]
   - ask: ABC = 3x + 10 = 3(30) + 10 =  [box expects 100 (NO unit label)]

## gold[2] (input: single_value, main-box unit: (none))
Q: PTAB70°?Diagram not drawn accurately PT is a tangent at T. A and B are on the circle. Angle PTA = \(70°\). Using the alternate segment theorem, find angle ABT.
   - intro: The alternate segment theorem: the angle between tangent PT and chord TA equals the angle ABT in the alternate segment.
   - ask: Equal or supplementary? Type 1 for equal, 2 for supplementary:  [box expects 1 (NO unit label)]
   - ask: They are equal, and PTA = 70°, so ABT =  [box expects 70 (NO unit label)]
   - ask: Check the pair match: 70 and  [box expects 70 (NO unit label)]

## gold[3] (input: single_value, main-box unit: (none))
Q: ABCO28°?Diagram not drawn accurately AB is a diameter of the circle. C is a point on the circle. Angle CAB = \(28°\). Find angle ABC.
   - intro: AB is a diameter, so angle ACB stands in a semicircle and equals 90°. Then use the triangle.
   - ask: Angle ACB in the semicircle =  [box expects 90 (NO unit label)]
   - ask: Triangle ACB adds to 180. Add the two known angles: 90 + 28 =  [box expects 118 (NO unit label)]
   - ask: Subtract from 180: 180 − 118 =  [box expects 62 (NO unit label)]
   - ask: Check all three: 90 + 28 + 62 =  [box expects 180 (NO unit label)]

## gold[4] (input: single_value, main-box unit: (none))
Q: ABOC?35°Diagram not drawn accurately O is the centre. A and B are on the circle. Angle OAB = \(35°\). C is on the minor arc. Find the obtuse angle ACB.
   - intro: OA and OB are radii, so triangle OAB is isosceles. C is on the MINOR arc, so it stands on the reflex angle at the centre.
   - ask: Base angles equal, so angle OBA =  [box expects 35 (NO unit label)]
   - ask: Centre angle AOB = 180 − 35 − 35 =  [box expects 110 (NO unit label)]
   - ask: C is on the minor arc, so use the reflex angle: 360 − 110 =  [box expects 250 (NO unit label)]
   - ask: Angle ACB is half the reflex angle: 250 ÷ 2 =  [box expects 125 (NO unit label)]
