# apply-pack: geometry__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[1] | Number of sides = 360 ÷ 24 = [box=15, NO label] | fix: Add a line before the step: 'The exterior angles add up to 360°, so number of sides = 360 ÷ one exterior angle.'
- [medium] gold[1] | A regular hexagon's interior angle is 720 ÷ 6 = [box=120] | fix: Build the 720 first, e.g. 'A regular hexagon's interior angles total (6 - 2) x 180 = 720, so each one is 720 / 6 =' (or add an intro line stating where 720 come

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[1] Q: The interior angle of a regular polygon is 5 times its exterior angle. How many sides does
   step0 field=say answer=None text='Interior + exterior = 180°, and here interior = 5 × exterior, so \\(5e + e = 180\\).'
   step1 field=pre answer=6 text='Add the lots of e: 5e + e ='
   step2 field=pre answer=30 text='So 6e = 180, e = 180 ÷ 6 ='
   step3 field=pre answer=12 text='Number of sides = 360 ÷ 30 ='
   step4 field=pre answer=5 text='Check: interior = 180 − 30 = 150, and 150 ÷ 30 ='

silver[1] Q: A regular polygon has an interior angle of \(156°\). How many sides does it have?
   step0 field=say answer=None text='Work through the exterior angle: interior + exterior = 180°.'
   step1 field=pre answer=24 text='Exterior angle = 180 − 156 ='
   step2 field=pre answer=15 text='Number of sides = 360 ÷ 24 ='
   step3 field=pre answer=360 text='Check: 24 × 15 ='

### board=maths-edexcel
gold[1] Q: (3x + 10)°(2x + 20)°Diagram not drawn accuratelyIn a parallelogram, one angle is \((3x + 1
   step0 field=say answer=None text='Adjacent angles in a parallelogram (a co-interior pair) add to 180°. Add the two expressio'
   step1 field=pre answer=5 text='Combine the x terms: 3x + 2x ='
   step2 field=pre answer=30 text='Combine the numbers: 10 + 20 ='
   step3 field=pre answer=150 text='So 5x + 30 = 180, giving 5x = 180 − 30 ='
   step4 field=pre answer=30 text='x = 150 ÷ 5 ='
   step5 field=pre answer=180 text='Check the angles: 3(30) + 10 = 100 and 2(30) + 20 = 80, so 100 + 80 ='

silver[1] Q: ?Find each interior angle of a regular hexagon.
   step0 field=say answer=None text='A regular hexagon has 6 equal angles. Find the total, then share it out.'
   step1 field=pre answer=720 text='Interior sum = (6 − 2) × 180 = 4 × 180 ='
   step2 field=pre answer=120 text='Regular, so divide by 6: 720 ÷ 6 ='
   step3 field=pre answer=720 text='Check: 6 × 120 ='

### board=maths-ocr
gold[1] Q: 90°120°?Two regular polygons share a side. One is a square, the other a regular hexagon. F
   step0 field=say answer=None text='The three angles meeting at the shared corner go all the way around a point, which is 360°'
   step1 field=pre answer=90 text="A square's interior angle is"
   step2 field=pre answer=120 text="A regular hexagon's interior angle is 720 ÷ 6 ="
   step3 field=pre answer=150 text='The gap fills the rest of the point: 360 − 90 − 120 ='
   step4 field=pre answer=360 text='Check: 90 + 120 + 150 ='

silver[1] Q: Each interior angle of a regular polygon is 120°. How many sides?
   step0 field=say answer=None text='Work through the exterior angle. Interior and exterior angles on a straight line add to 18'
   step1 field=pre answer=60 text='Exterior angle: 180 − 120 ='
   step2 field=pre answer=6 text='Exterior angles add to 360°, so sides = 360 ÷ 60 ='
   step3 field=pre answer=120 text='Check: interior sum = (6 − 2) × 180 = 720, and 720 ÷ 6 ='

### board=maths-eduqas
gold[1] Q: 108°120°xA regular pentagon and a regular hexagon share a side and meet at a point, with a

silver[1] Q: 110°?Co-interior angle with a parallel line: one angle is \(110^\circ\). Find the other.
