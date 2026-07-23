# apply-pack: geometry__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[0] | Check the pair: 3(35) + (35 + 40) = 105 + 75 = [box=180, NO label] | fix: Break it up / spell out the multiply: 'First angle = 3 × 35 = 105. Opposite angle = 35 + 40 = 75. Check: 105 + 75 = [180]'
- [low] bronze[0] | How many circumference angles make the centre angle? Type the multiplier: [box=2 | fix: Rephrase to match bronze[1]: 'The centre angle is how many times the circumference angle? Type the multiplier: [2]'
- [low] bronze[5] | Equal angles, so the difference between them is [box=0, NO label] | fix: Drop the difference framing and go straight to the equality, e.g. 'Angles in the same segment are equal, so x = the given angle: x = [box=42, label:'degrees']'.
- [low] silver[0] | A cyclic quadrilateral has angles 2x, 3x, 2x+20, and y ... Given that 2x and 2x+ | fix: Drop the unused 3x and y, or say plainly: 'Two opposite angles are 2x and 2x+20 — find x.'
- [low] silver[6] | Check all three: 90 + 30 + 60 = [box=180, NO label] | fix: Add a line computing 2x before the check, e.g. '2x = 2 × 30 = 60', then 'Check all three: 90 + 30 + 60 ='.
- [low] gold[1] | Check the pair: 4(25) + (2×25 + 30) = 100 + 80 = [box=180, NO label] | fix: Spell it out: '4 × 25 = 100, and 2 × 25 + 30 = 80, so 100 + 80 = ___'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: OABC124°?Diagram not drawn accurately The angle at the centre of a circle is \(124°\). Fin
   step0 field=say answer=None text='The angle at the centre is twice the angle at the circumference on the same arc.'
   step1 field=pre answer=2 text='How many circumference angles make the centre angle? Type the multiplier:'
   step2 field=pre answer=62 text='So circumference = 124 ÷ 2 ='
   step3 field=pre answer=124 text='Check by doubling back: 62 × 2 ='

bronze[5] Q: OT?Diagram not drawn accurately A tangent meets a radius at point T. The angle between the

gold[1] Q: ABCD3x + 102x + 20Diagram not drawn accurately A, B, C, D lie on a circle. Angle ABC = \(3
   step0 field=say answer=None text='ABC and ADC are opposite angles of the cyclic quadrilateral, so they add to 180°.'
   step1 field=pre answer=5 text='Add the x terms: 3x + 2x ='
   step2 field=pre answer=30 text='Add the numbers: 10 + 20 ='
   step3 field=pre answer=150 text='So 5x + 30 = 180. Take 30 across: 180 − 30 ='
   step4 field=pre answer=30 text='Now 5x = 150, so x = 150 ÷ 5 ='
   step5 field=pre answer=100 text='ABC = 3x + 10 = 3(30) + 10 ='

silver[0] Q: ABCD3x2x + 10x + 40100°Diagram not drawn accurately A cyclic quadrilateral has angles \(3x
   step0 field=say answer=None text='Opposite angles of a cyclic quadrilateral add to 180°. Here 3x and x + 40 are the opposite'
   step1 field=pre answer=4 text="Add the opposite pair's x terms: 3x + x ="
   step2 field=pre answer=140 text='The number part is 40, so 4x + 40 = 180. Take 40 across: 180 − 40 ='
   step3 field=pre answer=35 text='Now 4x = 140, so x = 140 ÷ 4 ='
   step4 field=pre answer=180 text='Check the pair: 3(35) + (35 + 40) = 105 + 75 ='

silver[6] Q: ABC40°?55°Diagram not drawn accurately Points A, B, C lie on a circle. Angle BAC = \(40°\)
   step0 field=say answer=None text='A, B and C are just three angles of a triangle, which add to 180°.'
   step1 field=pre answer=95 text='Add the two known angles: 40 + 55 ='
   step2 field=pre answer=85 text='Subtract from 180: 180 − 95 ='
   step3 field=pre answer=180 text='Check all three: 40 + 55 + 85 ='

### board=maths-edexcel
bronze[0] Q: 120°?OABCDiagram not drawn accuratelyAngle at centre = \(120°\). Find the angle at the cir
   step0 field=say answer=None text='The angle at the centre is twice the angle at the circumference on the same arc, so the ci'
   step1 field=pre answer=2 text='The centre angle is how many times the circumference angle?'
   step2 field=pre answer=60 text='So halve it: 120 ÷ 2 ='
   step3 field=pre answer=120 text='Check by doubling back: 60 × 2 ='

bronze[5] Q: 42°x°ABCDDiagram not drawn accuratelyTwo angles are in the same segment. One is \(42°\), t
   step0 field=say answer=None text='Angles in the same segment stand on the same chord and are equal.'
   step1 field=pre answer=0 text='Equal angles, so the difference between them is'
   step2 field=pre answer=42 text='So x equals the given angle: x ='
   step3 field=pre answer=0 text='Check the difference: 42 − 42 ='

gold[1] Q: 28°?ABCDDiagram not drawn accuratelyAngle at circumference from the minor arc = \(28°\). F
   step0 field=say answer=None text='Work through the centre. The minor-arc angle at the circumference is 28°, so the centre an'
   step1 field=pre answer=56 text='Centre angle (minor arc) = 28 × 2 ='
   step2 field=pre answer=304 text='Reflex centre angle (major arc) = 360 − 56 ='
   step3 field=pre answer=152 text='Major-arc circumference angle = half the reflex: 304 ÷ 2 ='
   step4 field=pre answer=180 text='Check they are supplementary: 28 + 152 ='

silver[0] Q: ?54°OABCDiagram not drawn accuratelyThe angle at the circumference is \(54°\). Find the re
   step0 field=say answer=None text='First the ordinary angle at the centre is twice the circumference angle.'
   step1 field=pre answer=108 text='Centre angle = 54 × 2 ='
   step2 field=pre answer=252 text='The reflex angle is the rest of the full turn: 360 − 108 ='
   step3 field=pre answer=360 text='Check: 108 + 252 ='

silver[6] Q: 90°32°?ABCDiagram not drawn accuratelyA triangle inscribed in a semicircle has one angle o
   step0 field=say answer=None text='The 90° is the angle in the semicircle. The three angles of the triangle add to 180°.'
   step1 field=pre answer=122 text='Add the two known angles: 90 + 32 ='
   step2 field=pre answer=58 text='Third angle = 180 − 122 ='
   step3 field=pre answer=180 text='Check all three: 90 + 32 + 58 ='

### board=maths-ocr
bronze[0] Q: OABC100°?The angle at the centre is 100°. Find the angle at the circumference standing on 
   step0 field=say answer=None text='The angle at the centre and the angle at the circumference stand on the same arc AB. The o'
   step1 field=pre answer=100 text='Write the angle at the centre:'
   step2 field=pre answer=50 text='Halve it to reach the circumference: 100 ÷ 2 ='
   step3 field=pre answer=100 text='Check by doubling your answer: 50 × 2 ='

bronze[5] Q: ABCD80°?ABCD is a cyclic quadrilateral. Angle A = 80°. Find angle C, the opposite angle. D
   step0 field=say answer=None text='A, B, C, D all sit on the circle, so ABCD is a cyclic quadrilateral. Opposite angles add u'
   step1 field=pre answer=80 text='Write the given angle A:'
   step2 field=pre answer=100 text='Opposite angles sum to 180, so C = 180 − 80 ='
   step3 field=pre answer=180 text='Check the pair adds to 180: 80 + 100 ='

gold[1] Q: ABCD4x5xA cyclic quadrilateral has one pair of opposite angles equal to \(4x\) and \(5x\).
   step0 field=say answer=None text='The pair \\(4x\\) and \\(5x\\) are opposite angles of the cyclic quadrilateral, so they sum to'
   step1 field=pre answer=9 text='Add the pair: 4x + 5x gives how many x?'
   step2 field=pre answer=20 text='So 9x = 180, and x = 180 ÷ 9 ='
   step3 field=pre answer=80 text='The first angle 4x = 4 × 20 ='
   step4 field=pre answer=180 text='The opposite angle 5x = 5 × 20 = 100, and 80 + 100 ='

silver[0] Q: ABCD2x3x2x+20yA cyclic quadrilateral has angles \(2x\), \(3x\), \(2x+20\), and \(y\). Oppo
   step0 field=say answer=None text='The opposite pair is \\(2x\\) and \\(2x + 20\\). Opposite angles of a cyclic quadrilateral sum'
   step1 field=pre answer=4 text='Add the coefficients of x in 2x + (2x + 20):'
   step2 field=pre answer=160 text='So 4x + 20 = 180. Subtract 20: 4x ='
   step3 field=pre answer=40 text='x = 160 ÷ 4 ='
   step4 field=pre answer=180 text='Check: 2(40) + (2(40) + 20) = 80 + 100 ='

silver[6] Q: BCA28°?In a semicircle, angle BAC = 90° and angle ABC = 28°. Find angle ACB. Diagram not d
   step0 field=say answer=None text='Angle BAC = 90° is the right angle in the semicircle. The three angles of the triangle add'
   step1 field=pre answer=118 text='Add the two known angles: 90 + 28 ='
   step2 field=pre answer=62 text='Angle ACB = 180 − 118 ='
   step3 field=pre answer=180 text='Check: 90 + 28 + 62 ='

### board=maths-eduqas
bronze[0] Q: OABC140°?Diagram not drawn accurately The angle at the centre of a circle is \(140°\). Fin
   step0 field=say answer=None text='The angle at the centre is twice the angle at the circumference on the same arc.'
   step1 field=pre answer=2 text='How many circumference angles make the centre angle? Type the multiplier:'
   step2 field=pre answer=70 text='So circumference = 140 ÷ 2 ='
   step3 field=pre answer=140 text='Check by doubling back: 70 × 2 ='

bronze[5] Q: ABPQx55°Diagram not drawn accurately Two angles subtended by the same chord from the same 
   step0 field=say answer=None text='Angles in the same segment, standing on the same chord, are equal.'
   step1 field=pre answer=1 text='Equal or supplementary? Type 1 for equal, 2 for supplementary:'
   step2 field=pre answer=55 text='They are equal, and one is 55°, so x ='
   step3 field=pre answer=55 text='Check the pair match: 55 and'

gold[1] Q: ABCD4x2x + 30Diagram not drawn accurately ABCD is a cyclic quadrilateral. Angle A = \(4x\)
   step0 field=say answer=None text='Angle A and angle C are opposite angles of the cyclic quadrilateral, so they add to 180°.'
   step1 field=pre answer=6 text='Add the x terms: 4x + 2x ='
   step2 field=pre answer=150 text='So 6x + 30 = 180. Take 30 across: 180 − 30 ='
   step3 field=pre answer=25 text='Now 6x = 150, so x = 150 ÷ 6 ='
   step4 field=pre answer=180 text='Check the pair: 4(25) + (2×25 + 30) = 100 + 80 ='

silver[0] Q: ABCD72°?Diagram not drawn accurately ABCD is a cyclic quadrilateral. Angle A is \(72°\). F
   step0 field=say answer=None text='Opposite angles of a cyclic quadrilateral add up to 180°.'
   step1 field=pre answer=180 text='What total do the opposite pair make?'
   step2 field=pre answer=108 text='So angle C = 180 − 72 ='
   step3 field=pre answer=180 text='Check the pair: 72 + 108 ='

silver[6] Q: ABCOx2xDiagram not drawn accurately AB is a diameter, so angle ACB = \(90°\). The other tw
   step0 field=say answer=None text='Angle ACB is 90° (angle in a semicircle). The three angles of the triangle add to 180°.'
   step1 field=pre answer=90 text='Take the 90° from 180: 180 − 90 ='
   step2 field=pre answer=3 text='The other two are x and 2x, so x + 2x = how many x?'
   step3 field=pre answer=30 text='So 3x = 90, meaning x = 90 ÷ 3 ='
   step4 field=pre answer=180 text='Check all three: 90 + 30 + 60 ='
