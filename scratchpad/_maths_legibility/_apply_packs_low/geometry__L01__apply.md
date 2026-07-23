# apply-pack: geometry__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[1] | Number of sides = 360 ÷ 30 = [box=12, NO label] | fix: Restate 'exterior angles total 360°, so sides = 360 ÷ exterior angle' before this step.
- [low] silver[0] | The two far interior angles add to the exterior angle. Type that exterior angle: | fix: Simplify to: 'The exterior angle is given on the diagram. Type it:' (box=130).
- [low] gold[3] | Q: Two regular polygons share a side. One is a square and the other is a regular | fix: Reword the stem to match the intro, e.g. 'Find the size of the gap between the two shapes at the corner where they meet.'
- [low] bronze[4] | That neighbour is opposite a 125° too, and 125 + 55 = [box=180] | fix: Drop the vertically-opposite clause and state the straight-line check plainly, e.g. 'The neighbour and the 55° sit on the same straight line: 125 + 55 ='.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[4] Q: Find the exterior angle of a regular hexagon.
   step0 field=say answer=None text='The exterior angles of any polygon add up to 360°, shared equally when it is regular.'
   step1 field=pre answer=360 text='Write the total of the exterior angles:'
   step2 field=pre answer=60 text='Share between the 6 sides: 360 ÷ 6 ='
   step3 field=pre answer=120 text='Check the matching interior angle: 180 − 60 ='

gold[1] Q: The interior angle of a regular polygon is 5 times its exterior angle. How many sides does
   step0 field=say answer=None text='Interior + exterior = 180°, and here interior = 5 × exterior, so \\(5e + e = 180\\).'
   step1 field=pre answer=6 text='Add the lots of e: 5e + e ='
   step2 field=pre answer=30 text='So 6e = 180, e = 180 ÷ 6 ='
   step3 field=pre answer=12 text='Number of sides = 360 ÷ 30 ='
   step4 field=pre answer=5 text='Check: interior = 180 − 30 = 150, and 150 ÷ 30 ='

gold[3] Q: Angles \(a\), \(b\) and \(c\) are at a point. \(a : b : c = 2 : 3 : 4\). Find angle \(b\).
   step0 field=say answer=None text='Angles at a point add to 360°. Split it in the ratio 2 : 3 : 4.'
   step1 field=pre answer=9 text='Add the ratio parts: 2 + 3 + 4 ='
   step2 field=pre answer=40 text='One part = 360 ÷ 9 ='
   step3 field=pre answer=120 text='b is 3 parts: 3 × 40 ='
   step4 field=pre answer=360 text='Check: 9 × 40 ='

silver[0] Q: 55°x130°Diagram not drawn accurately Two angles in a triangle are \(55°\) and \(x\). The e
   step0 field=say answer=None text='An exterior angle equals the sum of the two interior angles not next to it: \\(55 + x = 130'
   step1 field=pre answer=130 text='The two far interior angles add to the exterior angle. Type that exterior angle:'
   step2 field=pre answer=75 text='So x = 130 − 55 ='
   step3 field=pre answer=50 text='Check the third interior angle: 180 − 130 ='

### board=maths-edexcel
bronze[4] Q: 58°abDiagram not drawn accuratelyA transversal crosses two parallel lines. Angle \(a\) is 
   step0 field=say answer=None text='Two parallel lines with a transversal. Alternate angles (the Z shape) are equal.'
   step1 field=pre answer=58 text='Angle a is alternate to 58°, so a ='
   step2 field=pre answer=122 text='Angle b is on a straight line with a, so b = 180 − 58 ='
   step3 field=pre answer=180 text='Check a and b make a straight line: 58 + 122 ='

gold[1] Q: (3x + 10)°(2x + 20)°Diagram not drawn accuratelyIn a parallelogram, one angle is \((3x + 1
   step0 field=say answer=None text='Adjacent angles in a parallelogram (a co-interior pair) add to 180°. Add the two expressio'
   step1 field=pre answer=5 text='Combine the x terms: 3x + 2x ='
   step2 field=pre answer=30 text='Combine the numbers: 10 + 20 ='
   step3 field=pre answer=150 text='So 5x + 30 = 180, giving 5x = 180 − 30 ='
   step4 field=pre answer=30 text='x = 150 ÷ 5 ='
   step5 field=pre answer=180 text='Check the angles: 3(30) + 10 = 100 and 2(30) + 20 = 80, so 100 + 80 ='

gold[3] Q: 90°120°?Two regular polygons share a side. One is a square and the other is a regular hexa
   step0 field=say answer=None text="At the shared vertex, three angles meet and fill a full turn of 360°: the square's angle, "
   step1 field=pre answer=90 text="A square's interior angle is"
   step2 field=pre answer=120 text="A regular hexagon's interior angle is (6 − 2) × 180 ÷ 6 ="
   step3 field=pre answer=150 text='The gap = 360 − 90 − 120 ='
   step4 field=pre answer=360 text='Check they fill the turn: 90 + 120 + 150 ='

silver[0] Q: Find the interior angle sum of a nonagon (9 sides).
   step0 field=say answer=None text='The interior angle sum of a polygon is (n − 2) × 180°. A nonagon has n = 9.'
   step1 field=pre answer=7 text='First work out n − 2: 9 − 2 ='
   step2 field=pre answer=1260 text='Multiply by 180: 7 × 180 ='
   step3 field=pre answer=1260 text='Check by splitting the nonagon into 7 triangles, each 180°: 7 × 180 ='

### board=maths-ocr
bronze[4] Q: 55°?Two vertically opposite angles: one is 55°. What is the other?
   step0 field=say answer=None text='When two straight lines cross, the angles opposite each other are equal.'
   step1 field=pre answer=55 text='The given angle is 55°, so the vertically opposite one is also'
   step2 field=say answer=None text='You can check using the straight line. The angle next door fills the line with 55°.'
   step3 field=pre answer=125 text='Neighbour on the line: 180 − 55 ='
   step4 field=pre answer=180 text='That neighbour is opposite a 125° too, and 125 + 55 ='

gold[1] Q: 90°120°?Two regular polygons share a side. One is a square, the other a regular hexagon. F
   step0 field=say answer=None text='The three angles meeting at the shared corner go all the way around a point, which is 360°'
   step1 field=pre answer=90 text="A square's interior angle is"
   step2 field=pre answer=120 text="A regular hexagon's interior angles total (6 − 2) × 180 = 720, so each one is 720 ÷ 6 ="
   step3 field=pre answer=150 text='The gap fills the rest of the point: 360 − 90 − 120 ='
   step4 field=pre answer=360 text='Check: 90 + 120 + 150 ='

gold[3] Q: x2x3xDiagram not drawn accuratelyAngles in a triangle are \(x\), \(2x\), and \(3x\). Find 
   step0 field=say answer=None text='The three angles add to 180°. In parts, that is x + 2x + 3x.'
   step1 field=pre answer=6 text='Total parts: x + 2x + 3x ='
   step2 field=pre answer=30 text='So 6x = 180, giving x = 180 ÷ 6 ='
   step3 field=pre answer=90 text='The largest is 3x = 3 × 30 ='
   step4 field=pre answer=180 text='Check: 30 + 60 + 90 ='

silver[0] Q: Find the sum of interior angles of a hexagon.
   step0 field=say answer=None text='The interior angles of any polygon add up to (n − 2) × 180°. A hexagon has 6 sides.'
   step1 field=pre answer=4 text='n − 2 = 6 − 2 ='
   step2 field=pre answer=720 text='4 × 180 ='
   step3 field=pre answer=720 text='Check: a hexagon splits into 4 triangles, 4 × 180 ='

### board=maths-eduqas
bronze[4] Q: ??40°Diagram not drawn accuratelyAn isosceles triangle has a top angle of \(40^\circ\). Fi

gold[1] Q: 108°120°xA regular pentagon and a regular hexagon share a side and meet at a point, with a

gold[3] Q: A regular polygon has interior angles 8 times its exterior angles. How many sides?

silver[0] Q: 65°?Parallel lines cut by a transversal. One alternate angle is \(65^\circ\). Find the oth
