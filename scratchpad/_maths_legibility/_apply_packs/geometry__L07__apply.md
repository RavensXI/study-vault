# apply-pack: geometry__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] bronze[4] | Check the pair match: 35 and [box=35, NO label] | fix: Rewrite as a full instruction, e.g. 'Both angles are equal, so type the matching angle: [35]'
- [medium] silver[1] | Check the pair are equal: 64 and [box=64, NO label] | fix: Rewrite as 'The two angles are equal, so type the matching angle: [64]'
- [medium] silver[3] | Check the pair match: 12 and [box=12, NO label] | fix: Rewrite as 'The two tangents are equal, so type the matching length: [12]'
- [medium] gold[2] | Check the pair match: 70 and [box=70, NO label] | fix: Rewrite as 'The two angles are equal, so type the matching angle: [70]'
- [medium] silver[5] | Angle at the centre is twice that: 2 × 52 = [box=104, label:'degrees'] | fix: Add a bridging line: 'That 52 degrees is the angle at the circumference standing on AB. The angle at the centre is twice it: 2 × 52 = [104]'
- [medium] bronze[2] | The straight angle across the diameter, at the centre, is [box=180, NO label] | fix: State the fact before the box, e.g. 'A straight line makes 180 degrees at the centre, so the angle is' and label the box [box=180, label:'degrees'].
- [medium] silver[2] | Check with the kite: 90 + 90 + 140 + centre = 360, so the centre angle = 360 − 3 | fix: Either drop this check, or build it first: state that OA and OB are radii meeting the tangents at 90°, that OABP is a kite, and that its four angles add to 360°
- [medium] bronze[3] (also bronze[5], silver[2]) | Check the pair match: 48 and [box=48, NO label] | fix: Reword to a full instruction, e.g. 'Angles in the same segment are equal, so the second angle is also ___' (and the equivalent for the tangent lengths in silver
- [medium] all problems (e.g. bronze[0]) | Q: OABC140°?Diagram not drawn accurately The angle at the centre of a circle is  | fix: Separate the diagram labels from the prose and let the sentence start cleanly, e.g. make 'Diagram not drawn accurately.' its own line and drop or space out the 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: ABCO?Diagram not drawn accurately AB is a diameter. C is on the circumference. Find angle 
   step0 field=say answer=None text='AB is a diameter, so C sits in a semicircle.'
   step1 field=pre answer=180 text='A diameter is a straight line. How many degrees is a straight line?'
   step2 field=pre answer=90 text='The angle in the semicircle is half of that: 180 ÷ 2 ='
   step3 field=pre answer=90 text='So angle ACB is a right angle. Type it:'

bronze[3] Q: ABCD72°?Diagram not drawn accurately In a cyclic quadrilateral, one angle is \(72°\). Find
   step0 field=say answer=None text='Opposite angles of a cyclic quadrilateral add up to 180°.'
   step1 field=pre answer=180 text='What total do the opposite pair make?'
   step2 field=pre answer=108 text='So the opposite angle = 180 − 72 ='
   step3 field=pre answer=180 text='Check the pair: 72 + 108 ='

bronze[4] Q: ABPQ35°xDiagram not drawn accurately Two angles in the same segment stand on the chord AB.
   step0 field=say answer=None text='Angles in the same segment, standing on the same chord, are equal.'
   step1 field=pre answer=1 text='Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary:'
   step2 field=pre answer=35 text='They are equal, and one is 35°, so x ='
   step3 field=pre answer=35 text='Check the pair match: 35 and'

gold[2] Q: PTAB70°?Diagram not drawn accurately PT is a tangent at T. A and B are on the circle. Angl
   step0 field=say answer=None text='The alternate segment theorem: the angle between tangent PT and chord TA equals the angle '
   step1 field=pre answer=1 text='Equal or supplementary? Type 1 for equal, 2 for supplementary:'
   step2 field=pre answer=70 text='They are equal, and PTA = 70°, so ABT ='
   step3 field=pre answer=70 text='Check the pair match: 70 and'

silver[1] Q: ABC64°?Diagram not drawn accurately The angle between a tangent and a chord at the point o
   step0 field=say answer=None text='The alternate segment theorem: the angle between a tangent and a chord equals the angle in'
   step1 field=pre answer=1 text='Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary:'
   step2 field=pre answer=64 text='They are equal, and the tangent-chord angle is 64°, so the alternate segment angle ='
   step3 field=pre answer=64 text='Check the pair are equal: 64 and'

silver[2] Q: OABCx + 50xDiagram not drawn accurately O is the centre. Angle AOB = \(x + 50\). Angle ACB
   step0 field=say answer=None text='The angle at the centre is twice the angle at the circumference on the same arc: x + 50 = '
   step1 field=pre answer=1 text='Take one x from each side. 2x − x leaves how many x?'
   step2 field=pre answer=50 text='So 50 = x, meaning x ='
   step3 field=pre answer=100 text='Check the centre angle: x + 50 = 50 + 50 ='
   step4 field=pre answer=100 text='And twice the circumference: 2 × 50 ='

silver[3] Q: TABO12 cm?Diagram not drawn accurately Two tangents from an external point T touch the cir
   step0 field=say answer=None text='Two tangents drawn from the same external point are equal in length.'
   step1 field=pre answer=1 text='TA and TB come from the same point T. Type 1 if they are equal, 2 if not:'
   step2 field=pre answer=12 text='They are equal, and TA = 12 cm, so TB ='
   step3 field=pre answer=12 text='Check the pair match: 12 and'

silver[5] Q: ABO52°?Diagram not drawn accurately The angle between a tangent at A and chord AB is \(52°
   step0 field=say answer=None text='Alternate segment: the angle in the alternate segment equals the tangent-chord angle, 52°.'
   step1 field=pre answer=52 text='Angle in the alternate segment = tangent-chord angle ='
   step2 field=pre answer=104 text='Angle at the centre is twice that: 2 × 52 ='
   step3 field=pre answer=52 text='Check by halving: 104 ÷ 2 ='

### board=maths-edexcel
bronze[2] Q: ?ABCdiameterDiagram not drawn accuratelyA triangle is drawn in a semicircle with the diame
   step0 field=say answer=None text='The diameter passes through the centre, so it makes a straight angle at the centre.'
   step1 field=pre answer=180 text='The straight angle across the diameter, at the centre, is'
   step2 field=pre answer=90 text='The angle at the circumference is half the centre angle: 180 ÷ 2 ='
   step3 field=pre answer=90 text='So the other two angles of the triangle add up to 180 − 90 ='

bronze[3] Q: 85°x°ABCDDiagram not drawn accuratelyCyclic quadrilateral: opposite angles are \(85°\) and
   step0 field=say answer=None text='Opposite angles in a cyclic quadrilateral add up to 180°.'
   step1 field=pre answer=180 text='The two opposite angles must total'
   step2 field=pre answer=95 text='So x = 180 − 85 ='
   step3 field=pre answer=180 text='Check they add to 180: 85 + 95 ='

bronze[4] Q: 35°?OTPDiagram not drawn accuratelyOT is a radius and TP is a tangent touching the circle 
   step0 field=say answer=None text='A tangent meets a radius at 90°, so the angle at T, angle OTP, is a right angle.'
   step1 field=pre answer=90 text='The angle at T (radius meets tangent) is'
   step2 field=pre answer=55 text='The three angles add to 180°, so angle TOP = 180 − 90 − 35 ='
   step3 field=pre answer=180 text='Check the three angles: 90 + 35 + 55 ='

gold[2] Q: 1213rPAOBDiagram not drawn accuratelyFrom P outside a circle, tangent PA has length 12 and
   step0 field=say answer=None text='PA is a tangent, so it meets the radius OA at 90°. Triangle OAP is right-angled at A, with'
   step1 field=pre answer=169 text='Square the hypotenuse: 13 × 13 ='
   step2 field=pre answer=144 text='Square the tangent: 12 × 12 ='
   step3 field=pre answer=25 text='Pythagoras: r² = 169 − 144 ='
   step4 field=pre answer=5 text='So r = √25 ='
   step5 field=pre answer=169 text='Check: 5 × 5 + 12 × 12 = 25 + 144 ='

silver[1] Q: ?63°TBDtangentDiagram not drawn accuratelyA tangent and a chord meet at a point on the cir
   step0 field=say answer=None text='The alternate segment theorem: the angle between a tangent and a chord equals the angle in'
   step1 field=pre answer=63 text='Write the angle in the alternate segment:'
   step2 field=pre answer=63 text='By the theorem the tangent-chord angle equals it, so it is'
   step3 field=pre answer=126 text='Two equal angles: their sum is 63 + 63 ='

silver[2] Q: 3x+52x+15ABCDDiagram not drawn accuratelyIn a cyclic quadrilateral ABCD, angle A = \(3x + 
   step0 field=say answer=None text='A and C are opposite angles, so they add to 180°: \\((3x + 5) + (2x + 15) = 180\\).'
   step1 field=pre answer=5 text='Add the x-terms: 3x + 2x ='
   step2 field=pre answer=20 text='Add the numbers: 5 + 15 ='
   step3 field=pre answer=160 text='So 5x + 20 = 180. Subtract 20: 5x = 180 − 20 ='
   step4 field=pre answer=32 text='x = 160 ÷ 5 ='
   step5 field=pre answer=101 text='Check angle A: 3 × 32 + 5 ='

silver[3] Q: 55°?OABTDiagram not drawn accuratelyAT is a tangent to a circle with centre O, touching at
   step0 field=say answer=None text='OA is a radius and AT is a tangent, so they meet at 90°: angle OAT = 90°.'
   step1 field=pre answer=90 text='The right angle between radius and tangent is'
   step2 field=pre answer=35 text='The chord AB splits that right angle, so angle OAB = 90 − 55 ='
   step3 field=pre answer=90 text='Check the two parts: 35 + 55 ='

silver[5] Q: 110°?OABCDiagram not drawn accuratelyAngle at centre (minor arc) = \(110°\). Find the angl
   step0 field=say answer=None text='The 110° at the centre is on the minor-arc side. The major-arc circumference angle stands '
   step1 field=pre answer=250 text='Reflex angle at the centre = 360 − 110 ='
   step2 field=pre answer=125 text='Angle at the circumference is half the reflex: 250 ÷ 2 ='
   step3 field=pre answer=250 text='Check by doubling back: 125 × 2 ='

### board=maths-ocr
bronze[2] Q: ABC?AB is a diameter and C is a point on the circle. Find angle ACB. Diagram not drawn acc
   step0 field=say answer=None text='AB is a diameter, so at the centre the angle AOB is a straight line: 180°. Angle ACB stand'
   step1 field=pre answer=180 text='The straight angle along the diameter AB is'
   step2 field=pre answer=90 text='Angle ACB is half of it: 180 ÷ 2 ='
   step3 field=pre answer=90 text='So angle ACB ='

bronze[3] Q: OTP55°?A tangent touches a circle at T, and O is the centre. In triangle OTP the angle at 
   step0 field=say answer=None text='A tangent always meets a radius at 90°, so triangle OTP has a right angle at T. The three '
   step1 field=pre answer=145 text='Add the two known angles: 90 + 55 ='
   step2 field=pre answer=35 text='The angle at P = 180 − 145 ='
   step3 field=pre answer=180 text='Check all three add to 180: 90 + 55 + 35 ='

bronze[4] Q: ABCD42°?Two angles stand in the same segment on the same arc AB. One is 42°. Find the othe
   step0 field=say answer=None text='Both angles stand on the same arc AB, so they are angles in the same segment. Angles in th'
   step1 field=pre answer=42 text='Write the angle you are given:'
   step2 field=pre answer=42 text='Same segment means equal, so the other angle ='
   step3 field=pre answer=84 text='Both are 42°, so together they make 42 + 42 ='

gold[2] Q: TAB48°?A tangent touches a circle at T, and TA is a chord. The angle between the tangent a
   step0 field=say answer=None text='The alternate segment theorem: the angle between the tangent and chord TA equals angle TBA'
   step1 field=pre answer=48 text='Write the tangent-chord angle:'
   step2 field=pre answer=48 text='Angle TBA equals it, so it ='
   step3 field=pre answer=96 text='Both equal 48°, so together 48 + 48 ='

silver[1] Q: TAB55°?A tangent makes an angle of 55° with a chord at the point of contact. Find the angl
   step0 field=say answer=None text='The alternate segment theorem: the angle between a tangent and a chord equals the angle in'
   step1 field=pre answer=55 text='Write the tangent-chord angle:'
   step2 field=pre answer=55 text='The alternate segment angle equals it, so it ='
   step3 field=pre answer=110 text='Both equal 55°, so together they make 55 + 55 ='

silver[2] Q: OABP70°?Two tangents are drawn from an external point P to a circle, centre O. The line PO
   step0 field=say answer=None text='PO bisects the angle between the two tangents, so each half is 70°. The full angle at P is'
   step1 field=pre answer=70 text='One half of the angle at P is 70°. Write it:'
   step2 field=pre answer=140 text='The full angle between the tangents is twice this: 70 × 2 ='
   step3 field=pre answer=40 text='Check with the kite: 90 + 90 + 140 + centre = 360, so the centre angle = 360 − 320 ='

silver[3] Q: OABC260°?The reflex angle at the centre is 260°. Find the angle at the circumference stand
   step0 field=say answer=None text='The circumference angle is half the centre angle it stands on. Here that centre angle is t'
   step1 field=pre answer=260 text='Write the reflex angle at the centre:'
   step2 field=pre answer=130 text='Halve it: 260 ÷ 2 ='
   step3 field=pre answer=260 text='Check by doubling: 130 × 2 ='

silver[5] Q: OABC3x − 20xThe angle at the circumference is \(x\) and the angle at the centre on the sam
   step0 field=say answer=None text='The centre angle is twice the circumference angle, so \\(3x - 20 = 2x\\).'
   step1 field=pre answer=1 text='Subtract 2x from both sides. 3x − 2x leaves how many x?'
   step2 field=pre answer=20 text='So x − 20 = 0, giving x ='
   step3 field=pre answer=20 text='Circumference angle = x ='
   step4 field=pre answer=40 text='Centre angle = 3(20) − 20 ='

### board=maths-eduqas
bronze[2] Q: ABCO?Diagram not drawn accurately A triangle is inscribed in a circle so that one side, AB
   step0 field=say answer=None text='AB is a diameter, so C sits in a semicircle.'
   step1 field=pre answer=180 text='A diameter is a straight line. How many degrees is a straight line?'
   step2 field=pre answer=90 text='The angle in the semicircle is half of that: 180 ÷ 2 ='
   step3 field=pre answer=90 text='So angle ACB is a right angle. Type it:'

bronze[3] Q: ABPQ48°xDiagram not drawn accurately Two angles in the same segment stand on the chord AB.
   step0 field=say answer=None text='Angles in the same segment, standing on the same chord, are equal.'
   step1 field=pre answer=1 text='Are the two angles equal or supplementary? Type 1 for equal, 2 for supplementary:'
   step2 field=pre answer=48 text='They are equal, and one is 48°, so x ='
   step3 field=pre answer=48 text='Check the pair match: 48 and'

bronze[4] Q: ABCO?Diagram not drawn accurately A diameter subtends an angle at the circumference. What 

gold[2] Q: The angle between a tangent and a chord equals the angle in the alternate segment, the ang

silver[1] Q: OT?Diagram not drawn accurately A tangent meets a radius at the point of contact. What is 

silver[2] Q: TABO12 cm?Diagram not drawn accurately Two tangents are drawn from an external point T, to
   step0 field=say answer=None text='Two tangents drawn from the same external point are equal in length.'
   step1 field=pre answer=1 text='TA and TB come from the same point T. Type 1 if they are equal, 2 if not:'
   step2 field=pre answer=12 text='They are equal, and TA = 12 cm, so TB ='
   step3 field=pre answer=12 text='Check the pair match: 12 and'

silver[3] Q: ABCD85°110°?Diagram not drawn accurately ABCD is a cyclic quadrilateral. Angle DAB = \(85°
   step0 field=say answer=None text='Opposite angles of a cyclic quadrilateral add to 180°. Angle BCD is opposite angle DAB.'
   step1 field=pre answer=1 text='Which angle is opposite BCD? Type 1 for DAB (85°), 2 for ABC (110°):'
   step2 field=pre answer=95 text='So angle BCD = 180 − 85 ='
   step3 field=pre answer=180 text='Check the opposite pair: 85 + 95 ='

silver[5] Q: OABC40°Diagram not drawn accurately C is on the major arc. The angle at the circumference,
   step0 field=say answer=None text='The angle at the centre is twice the angle at the circumference. Then the reflex angle is '
   step1 field=pre answer=80 text='First the centre angle: 2 × 40 ='
   step2 field=pre answer=280 text='The reflex angle is 360 − 80 ='
   step3 field=pre answer=360 text='Check they complete a turn: 80 + 280 ='
