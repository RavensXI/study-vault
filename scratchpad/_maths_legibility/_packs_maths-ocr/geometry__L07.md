# maths-ocr / geometry / L07 - Circle Theorems

## bronze[0] (input: single_value, main-box unit: (none))
Q: OABC100°?The angle at the centre is 100°. Find the angle at the circumference standing on the same arc. Diagram not drawn accurately
   - intro: The angle at the centre and the angle at the circumference stand on the same arc AB. The one at the centre is always twice the one at the edge.
   - ask: Write the angle at the centre:  [box=100, label:'°']
   - ask: Halve it to reach the circumference: 100 ÷ 2 =  [box=50, label:'°']
   - ask: Check by doubling your answer: 50 × 2 =  [box=100, label:'°']

## bronze[1] (input: single_value, main-box unit: (none))
Q: OABC?35°The angle at the circumference is 35°. Find the angle at the centre standing on the same arc. Diagram not drawn accurately
   - intro: This time we work outwards: the centre angle is double the circumference angle.
   - ask: Write the angle at the circumference:  [box=35, label:'°']
   - ask: Double it to reach the centre: 35 × 2 =  [box=70, label:'°']
   - ask: Check by halving your answer: 70 ÷ 2 =  [box=35, label:'°']

## bronze[2] (input: single_value, main-box unit: (none))
Q: ABC?AB is a diameter and C is a point on the circle. Find angle ACB. Diagram not drawn accurately
   - intro: AB is a diameter, so at the centre the angle AOB is a straight line: 180°. Angle ACB stands on the same arc, so it is half of that.
   - ask: The straight angle along the diameter AB is  [box=180, label:'°']
   - ask: Angle ACB is half of it: 180 ÷ 2 =  [box=90, label:'°']
   - ask: So angle ACB =  [box=90, label:'°']

## bronze[3] (input: single_value, main-box unit: (none))
Q: OTP55°?A tangent touches a circle at T, and O is the centre. In triangle OTP the angle at T, where the tangent meets the radius, is 90° and the angle at O is 55°. Find the angle at P. Diagram not drawn accurately
   - intro: A tangent always meets a radius at 90°, so triangle OTP has a right angle at T. The three angles of any triangle add to 180°.
   - ask: Add the two known angles: 90 + 55 =  [box=145, label:'°']
   - ask: The angle at P = 180 − 145 =  [box=35, label:'°']
   - ask: Check all three add to 180: 90 + 55 + 35 =  [box=180, label:'°']

## bronze[4] (input: single_value, main-box unit: (none))
Q: ABCD42°?Two angles stand in the same segment on the same arc AB. One is 42°. Find the other. Diagram not drawn accurately
   - intro: Both angles stand on the same arc AB, so they are angles in the same segment. Angles in the same segment are equal.
   - ask: Write the angle you are given:  [box=42, label:'°']
   - ask: Same segment means equal, so the other angle =  [box=42, label:'°']
   - ask: Both are 42°, so together they make 42 + 42 =  [box=84, label:'°']

## bronze[5] (input: single_value, main-box unit: (none))
Q: ABCD80°?ABCD is a cyclic quadrilateral. Angle A = 80°. Find angle C, the opposite angle. Diagram not drawn accurately
   - intro: A, B, C, D all sit on the circle, so ABCD is a cyclic quadrilateral. Opposite angles add up to 180°.
   - ask: Write the given angle A:  [box=80, label:'°']
   - ask: Opposite angles sum to 180, so C = 180 − 80 =  [box=100, label:'°']
   - ask: Check the pair adds to 180: 80 + 100 =  [box=180, label:'°']

## bronze[6] (input: single_value, main-box unit: (none))
Q: OABC160°?The angle at the centre is 160°. Find the angle at the circumference on the same arc. Diagram not drawn accurately
   - intro: Same arc, so the circumference angle is half the centre angle.
   - ask: Write the angle at the centre:  [box=160, label:'°']
   - ask: Halve it: 160 ÷ 2 =  [box=80, label:'°']
   - ask: Check by doubling: 80 × 2 =  [box=160, label:'°']

## bronze[7] (input: single_value, main-box unit: (none))
Q: ABC50°?A triangle is drawn inside a semicircle, so one of its angles is 90°. Another angle is 50°. Find the third angle. Diagram not drawn accurately
   - intro: The triangle sits in a semicircle, so one angle is 90°. The three angles add to 180°.
   - ask: Add the two known angles: 90 + 50 =  [box=140, label:'°']
   - ask: The third angle = 180 − 140 =  [box=40, label:'°']
   - ask: Check: 90 + 50 + 40 =  [box=180, label:'°']

## silver[0] (input: single_value, main-box unit: (none))
Q: ABCD2x3x2x+20yA cyclic quadrilateral has angles \(2x\), \(3x\), \(2x+20\), and \(y\). Opposite pairs sum to 180°. Given that \(2x\) and \(2x+20\) are opposite, find \(x\). Diagram not drawn accurately
   - intro: The opposite pair is \(2x\) and \(2x + 20\). Opposite angles of a cyclic quadrilateral sum to 180°.
   - ask: Add the coefficients of x in 2x + (2x + 20):  [box=4, NO label]
   - ask: So 4x + 20 = 180. Subtract 20: 4x =  [box=160, NO label]
   - ask: x = 160 ÷ 4 =  [box=40, NO label]
   - ask: Check: 2(40) + (2(40) + 20) = 80 + 100 =  [box=180, label:'°']

## silver[1] (input: single_value, main-box unit: (none))
Q: TAB55°?A tangent makes an angle of 55° with a chord at the point of contact. Find the angle in the alternate segment. Diagram not drawn accurately
   - intro: The alternate segment theorem: the angle between a tangent and a chord equals the angle in the alternate segment (subtended by that chord on the far arc).
   - ask: Write the tangent-chord angle:  [box=55, label:'°']
   - ask: The alternate segment angle equals it, so it =  [box=55, label:'°']
   - ask: Both equal 55°, so together they make 55 + 55 =  [box=110, label:'°']

## silver[2] (input: single_value, main-box unit: (none))
Q: OABP70°?Two tangents are drawn from an external point P to a circle, centre O. The line PO makes an angle of 70° with each tangent. Find the angle between the two tangents. Diagram not drawn accurately
   - intro: PO bisects the angle between the two tangents, so each half is 70°. The full angle at P is twice one half.
   - ask: One half of the angle at P is 70°. Write it:  [box=70, label:'°']
   - ask: The full angle between the tangents is twice this: 70 × 2 =  [box=140, label:'°']
   - ask: Check with the kite: 90 + 90 + 140 + centre = 360, so the centre angle = 360 − 320 =  [box=40, label:'°']

## silver[3] (input: single_value, main-box unit: (none))
Q: OABC260°?The reflex angle at the centre is 260°. Find the angle at the circumference standing on the same arc. Diagram not drawn accurately
   - intro: The circumference angle is half the centre angle it stands on. Here that centre angle is the reflex 260°, not the smaller one.
   - ask: Write the reflex angle at the centre:  [box=260, label:'°']
   - ask: Halve it: 260 ÷ 2 =  [box=130, label:'°']
   - ask: Check by doubling: 130 × 2 =  [box=260, label:'°']

## silver[4] (input: single_value, main-box unit: (none))
Q: OABP8 cm?Two tangents are drawn from a point P to a circle, touching at A and B. PA = 8 cm. Find PB. Diagram not drawn accurately
   - intro: Two tangents drawn from the same external point are always equal in length.
   - ask: Write the length PA:  [box=8, label:'cm']
   - ask: PB equals PA, so PB =  [box=8, NO label]
   - ask: Together the two tangents measure 8 + 8 =  [box=16, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: OABC3x − 20xThe angle at the circumference is \(x\) and the angle at the centre on the same arc is \(3x - 20\). Find \(x\). Diagram not drawn accurately
   - intro: The centre angle is twice the circumference angle, so \(3x - 20 = 2x\).
   - ask: Subtract 2x from both sides. 3x − 2x leaves how many x?  [box=1, NO label]
   - ask: So x − 20 = 0, giving x =  [box=20, NO label]
   - ask: Circumference angle = x =  [box=20, label:'°']
   - ask: Centre angle = 3(20) − 20 =  [box=40, label:'°']

## silver[6] (input: single_value, main-box unit: (none))
Q: BCA28°?In a semicircle, angle BAC = 90° and angle ABC = 28°. Find angle ACB. Diagram not drawn accurately
   - intro: Angle BAC = 90° is the right angle in the semicircle. The three angles of the triangle add to 180°.
   - ask: Add the two known angles: 90 + 28 =  [box=118, label:'°']
   - ask: Angle ACB = 180 − 118 =  [box=62, label:'°']
   - ask: Check: 90 + 28 + 62 =  [box=180, label:'°']

## gold[0] (input: single_value, main-box unit: (none))
Q: OABC8x − 103x + 5The angle at the centre is \(8x - 10\) and the angle at the circumference on the same arc is \(3x + 5\). Using the fact that the centre angle is twice the circumference angle, find \(x\). Diagram not drawn accurately
   - intro: Centre is twice circumference, so \(8x - 10 = 2(3x + 5)\). Expand the bracket first.
   - ask: Expand: 2 × (3x + 5) gives how many x?  [box=6, NO label]
   - ask: So 8x − 10 = 6x + 10. Subtract 6x: 8x − 6x leaves how many x?  [box=2, NO label]
   - ask: 2x − 10 = 10, so 2x = 20 and x =  [box=10, NO label]
   - ask: Check: centre 8(10) − 10 = 70, circumference 3(10) + 5 = 35, and 70 ÷ 2 =  [box=35, label:'°']

## gold[1] (input: single_value, main-box unit: (none))
Q: ABCD4x5xA cyclic quadrilateral has one pair of opposite angles equal to \(4x\) and \(5x\). Find \(x\). Diagram not drawn accurately
   - intro: The pair \(4x\) and \(5x\) are opposite angles of the cyclic quadrilateral, so they sum to 180°.
   - ask: Add the pair: 4x + 5x gives how many x?  [box=9, NO label]
   - ask: So 9x = 180, and x = 180 ÷ 9 =  [box=20, NO label]
   - ask: The first angle 4x = 4 × 20 =  [box=80, label:'°']
   - ask: The opposite angle 5x = 5 × 20 = 100, and 80 + 100 =  [box=180, label:'°']

## gold[2] (input: single_value, main-box unit: (none))
Q: TAB48°?A tangent touches a circle at T, and TA is a chord. The angle between the tangent and TA is 48°. B is a point on the major arc. Find the angle TBA in the alternate segment. Diagram not drawn accurately
   - intro: The alternate segment theorem: the angle between the tangent and chord TA equals angle TBA in the alternate segment.
   - ask: Write the tangent-chord angle:  [box=48, label:'°']
   - ask: Angle TBA equals it, so it =  [box=48, label:'°']
   - ask: Both equal 48°, so together 48 + 48 =  [box=96, label:'°']

## gold[3] (input: single_value, main-box unit: (none))
Q: ABCDP384?Two chords AB and CD intersect at P inside a circle. PA = 3, PB = 8, PC = 4. Find PD. Diagram not drawn accurately
   - intro: When two chords cross inside a circle, the products of their two parts are equal: \(PA \times PB = PC \times PD\).
   - ask: Multiply the first chord's parts: 3 × 8 =  [box=24, NO label]
   - ask: So 4 × PD = 24, and PD = 24 ÷ 4 =  [box=6, NO label]
   - ask: Check: PC × PD = 4 × 6 =  [box=24, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: PTAB128?A tangent from P touches a circle at T. A secant from P passes through A and B on the circle. PT = 12, PA = 8. Find PB. Diagram not drawn accurately
   - intro: For a tangent and a secant from the same point: \(PT^2 = PA \times PB\), where PB is the whole secant from P to the far point B.
   - ask: Square the tangent: 12² =  [box=144, NO label]
   - ask: So 8 × PB = 144, and PB = 144 ÷ 8 =  [box=18, NO label]
   - ask: Check: PA × PB = 8 × 18 =  [box=144, NO label]
