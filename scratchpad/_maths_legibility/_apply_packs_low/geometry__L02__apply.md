# apply-pack: geometry__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[3] (=40) | Careful check: it is base × height, not ½ × base × height. Half would be 20, so  | fix: Simplify, e.g. 'Check straight from the formula: base × height = 8 × 5 =' (no halving for a parallelogram).
- [low] gold[0] | Add, using the calculator's full value (not the rounded 188.5), then round the t | fix: Split into two shorter sentences, e.g.: 'Add the straights to the circumference: 200 + π × 60. Use the calculator's full value for π × 60, then round the total 
- [low] gold[3] | Check: ring plus inner circle equals the outer circle. π × 16 + π × 9 = π × 25,  | fix: Split the reasoning from the sum to enter: 'The ring plus the inner circle should rebuild the outer circle. Work out π × 25, to 1 d.p. ='.
- [low] gold[1] | Circumference ≈ 50.265. Arc = 0.375 × 50.265, to 1 d.p. = [box=18.8, label:'cm'] | fix: Add a step: 'Circumference = 2 × π × 8, to 3 d.p. = ___' before using it in the arc calculation.
- [low] gold[2] | Fraction of the circle = arc ÷ circumference = 10 ÷ 31.416, to 4 d.p. = [box=0.3 | fix: Reuse the value the student just entered, or tell them to keep full calculator precision: 'using the un-rounded circumference from your calculator, 10 ÷ circumf

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[3] Q: base 8 cm5 cmDiagram not drawn accuratelyFind the area of a parallelogram with base 8 cm a
   step0 field=say answer=None text='Area of a parallelogram = base × perpendicular height. No halving.'
   step1 field=pre answer=40 text='Slide the slanted end across and it becomes a rectangle 8 by 5. That area = 8 × 5 ='
   step2 field=pre answer=40 text='So the parallelogram equals that rectangle. Write the area:'
   step3 field=pre answer=40 text='Careful check: it is base × height, not ½ × base × height. Half would be 20, so the true a'

gold[0] Q: 135°r = 8 cmDiagram not drawn accuratelyA sector has radius 8 cm and angle 135°. Find the 
   step0 field=say answer=None text='A sector is a fraction of the whole circle: fraction = angle ÷ 360.'
   step1 field=pre answer=64 text='Square the radius: 8 × 8 ='
   step2 field=pre answer=0.375 text='Fraction of the circle = 135 ÷ 360 ='
   step3 field=pre answer=75.4 text='Sector area = 0.375 × π × 64, to 1 decimal place ='
   step4 field=pre answer=75.4 text='Cross-check: the whole circle is π × 64 ≈ 201.1, and 0.375 × 201.1 ='

gold[1] Q: 72°r = 10 cmDiagram not drawn accuratelyA sector has radius 10 cm and angle 72°. Find the 
   step0 field=say answer=None text='Arc length is the same fraction of the whole circumference: (angle ÷ 360) × 2 π r.'
   step1 field=pre answer=0.2 text='Fraction of the circle = 72 ÷ 360 ='
   step2 field=pre answer=62.8 text='Full circumference = 2 × π × 10, to 1 decimal place ='
   step3 field=pre answer=12.6 text='Arc = 0.2 × 62.8, to 1 decimal place ='
   step4 field=pre answer=63 text='Cross-check: 360 ÷ 72 = 5, so five arcs make the full circle: 12.6 × 5 ='

gold[2] Q: 100 m100 md 60Diagram not drawn accuratelyA running track is two semicircles (diameter 60 
   step0 field=say answer=None text='Two semicircles of diameter 60 join into one full circle. Then add the two straight sides.'
   step1 field=pre answer=188 text='Curved part = π × diameter = π × 60, to the nearest whole ='
   step2 field=pre answer=200 text='Two straights = 2 × 100 ='
   step3 field=pre answer=388 text='Total perimeter = 188 + 200 ='
   step4 field=pre answer=188 text='Check: take the straights off, 388 − 200 ='

gold[3] Q: Area 154A circle has area 154 cm². Find the radius to 1 decimal place.
   step0 field=say answer=None text='Work area = π r² backwards. Divide by π, then take the square root.'
   step1 field=pre answer=49 text='Divide the area by π: 154 ÷ π, to the nearest whole ='
   step2 field=pre answer=7 text='That is r². Square-root it: √49 ='
   step3 field=pre answer=154 text='Check forwards: π × 7² = π × 49, to the nearest whole ='

### board=maths-edexcel
bronze[3] Q: 8 cm5 cmDiagram not drawn accuratelyFind the area of a parallelogram with base 8 cm and he
   step0 field=say answer=None text='Area of a parallelogram is base × perpendicular height. No halving, unlike a triangle.'
   step1 field=pre answer=5 text='Write the calculation, base × height = 8 ×'
   step2 field=pre answer=40 text='Now work it out: 8 × 5 ='
   step3 field=pre answer=5 text='Check by dividing back: 40 ÷ 8 ='

gold[0] Q: 100 m60 mA running track is two straight sides of 100 m and two semicircular ends of diame
   step0 field=say answer=None text='The perimeter is the two straight sides plus the two curved ends. The two semicircular end'
   step1 field=pre answer=200 text='The two straights: 2 × 100 ='
   step2 field=pre answer=188.5 text='The two ends make one full circle, circumference π × diameter. On your calculator, π × 60 '
   step3 field=pre answer=388 text="Add, using the calculator's full value (not the rounded 188.5), then round the total to th"
   step4 field=pre answer=200 text='Check the straights alone come to 200: 100 + 100 ='

gold[1] Q: 135°8 cmDiagram not drawn accuratelyA sector has radius 8 cm and angle \(135°\). Find the 
   step0 field=say answer=None text='A sector is a fraction of a whole circle. The fraction is the angle over 360.'
   step1 field=pre answer=0.375 text='The fraction of the circle: 135 ÷ 360 ='
   step2 field=pre answer=64 text='Square the radius: 8² ='
   step3 field=pre answer=75.4 text='Multiply the fraction, the square and π, then round to 1 d.p.: 0.375 × 64 × π ='
   step4 field=pre answer=135 text='Check the fraction step: 0.375 × 360 ='

gold[2] Q: C = ?Area = 200 cm²A circle has area \(200\) cm². Find the circumference to 1 d.p.
   step0 field=say answer=None text='Two stages: turn the area back into a radius, then use the radius to find the circumferenc'
   step1 field=pre answer=63.66 text='Divide the area by π: 200 ÷ π ='
   step2 field=pre answer=7.98 text='That is the radius squared. Square-root it: √63.66 ='
   step3 field=pre answer=50.1 text='Now the circumference: 2 × π × 7.98, to 1 d.p. ='
   step4 field=pre answer=200 text='Check by squaring the radius and using π: 7.98² × π ≈'

gold[3] Q: θ = ?9 cmarc 12 cmDiagram not drawn accuratelyA sector has arc length 12 cm and radius 9 c
   step0 field=say answer=None text='Arc length is a fraction of the full circumference. The fraction is the angle over 360, so'
   step1 field=pre answer=56.55 text='Full circumference = 2 × π × radius = 2 × π × 9 ='
   step2 field=pre answer=0.2122 text='The arc is 12 out of that whole circumference. Fraction of the circle: 12 ÷ 56.55 ='
   step3 field=pre answer=76 text='Multiply the fraction by 360 for the angle, to the nearest degree: 0.2122 × 360 ='
   step4 field=pre answer=12 text='Check by working forwards: 0.2122 × 56.55 ='

### board=maths-ocr
bronze[3] Q: base 7 cm4 cmDiagram not drawn accuratelyFind the area of a parallelogram with base 7 cm a
   step0 field=say answer=None text='A parallelogram fills the same space as a rectangle of the same base and height, so area i'
   step1 field=pre answer=7 text='Write the base to multiply: the base is'
   step2 field=pre answer=28 text='Multiply base × height: 7 × 4 ='
   step3 field=pre answer=28 text='Check: slide the slanted piece across to make a 7 by 4 rectangle, 7 × 4 ='

gold[0] Q: diameter 12 cmDiagram not drawn accuratelyA semicircle has diameter 12 cm. Find the area t
   step0 field=say answer=None text="A semicircle is half a circle. Find the radius, then halve the full circle's area."
   step1 field=pre answer=6 text='Radius = 12 ÷ 2 ='
   step2 field=pre answer=56.5 text='Half a circle is ½ × π × r². Work out ½ × π × 6², to 1 d.p. ='
   step3 field=pre answer=113 text='Check: two semicircles make the full circle, 56.5 × 2 ='

gold[1] Q: 135°r = 8 cmDiagram not drawn accuratelyA sector has radius 8 cm and angle 135°. Find the 
   step0 field=say answer=None text='Arc length is a fraction of the circumference. The fraction is angle ÷ 360.'
   step1 field=pre answer=0.375 text='Fraction of the circle: 135 ÷ 360 ='
   step2 field=pre answer=18.8 text='Circumference ≈ 50.265. Arc = 0.375 × 50.265, to 1 d.p. ='
   step3 field=pre answer=50.1 text='Check by scaling back up: 18.8 ÷ 0.375 ='

gold[2] Q: ?r = 5 cmarc 10 cmDiagram not drawn accuratelyA sector has radius 5 cm and arc length 10 c
   step0 field=say answer=None text='Arc = fraction × circumference, so find the fraction, then turn it into an angle out of 36'
   step1 field=pre answer=31.4 text='Circumference = 2 × π × 5, to 1 d.p. ='
   step2 field=pre answer=0.3183 text='Fraction of the circle = arc ÷ circumference = 10 ÷ 31.416, to 4 d.p. ='
   step3 field=pre answer=115 text='Angle = 0.3183 × 360, to the nearest degree ='
   step4 field=pre answer=10 text='Check forwards: arc = 0.3183 × 31.416 ='

gold[3] Q: R 5r 3Diagram not drawn accuratelyTwo circles share the same centre: radius 3 cm inside ra
   step0 field=say answer=None text="A ring (annulus) is the outer circle's area minus the inner circle's area."
   step1 field=pre answer=25 text='Square the outer radius: 5 × 5 ='
   step2 field=pre answer=9 text='Square the inner radius: 3 × 3 ='
   step3 field=pre answer=16 text='Subtract the squares: 25 − 9 ='
   step4 field=pre answer=50.3 text='Multiply by π: π × 16, to 1 d.p. ='
   step5 field=pre answer=78.5 text='Check: ring plus inner circle equals the outer circle. π × 16 + π × 9 = π × 25, to 1 d.p. '

### board=maths-eduqas
bronze[3] Q: 10 cm6 cmArea of a parallelogram: base 10 cm, perpendicular height 6 cm.Diagram not drawn 
   step0 field=say answer=None text='Parallelogram area = base × perpendicular height. No halving.'
   step1 field=pre answer=6 text='Read off the perpendicular height:'
   step2 field=pre answer=60 text='Area = 10 × 6 ='
   step3 field=pre answer=6 text='Check: 60 ÷ 10 ='

gold[0] Q: 10 cm6 cmr = 6A compound shape: rectangle 10 cm × 6 cm with a quarter-circle (radius 6 cm)
   step0 field=say answer=None text='Find the rectangle, then subtract the quarter-circle that has been removed.'
   step1 field=pre answer=60 text='Rectangle: 10 × 6 ='
   step2 field=pre answer=28.27 text='Quarter-circle: 0.25 × π × 6² (6² = 36), to 2 d.p. ='
   step3 field=pre answer=31.7 text='Subtract, to 1 d.p.: 60 − 28.27 ='
   step4 field=pre answer=60 text='Check: 31.7 + 28.27, to nearest whole ='

gold[1] Q: A = 154 cm²A circle has area 154 cm². Find its radius. (1 d.p.)Diagram not drawn accuratel
   step0 field=say answer=None text='Area = π r². Work backwards: divide by π, then square-root.'
   step1 field=pre answer=49.0 text='Divide the area by π: 154 ÷ π, to 1 d.p. ='
   step2 field=pre answer=7.0 text='Square-root it: √49, to 1 d.p. ='
   step3 field=pre answer=154 text='Check: 7² × π, to nearest whole ='

gold[2] Q: 12 cm60°A sector has area 24π cm² and radius 12 cm. Find the angle.Diagram not drawn accur
   step0 field=say answer=None text='Sector area = (θ ÷ 360) × π r². Set it equal to 24π and the π cancels.'
   step1 field=pre answer=144 text='r squared: 12² ='
   step2 field=pre answer=60 text='θ = 24 × 360 ÷ 144 ='
   step3 field=pre answer=24 text='Check: (60 ÷ 360) × 144 ='

gold[3] Q: 100 md = 60 mA running track is two straights (100 m each) and two semicircles (diameter 6
   step0 field=say answer=None text='The two straights are one length; the two semicircular ends make one full circle. Add them'
   step1 field=pre answer=200 text='Two straights: 2 × 100 ='
   step2 field=pre answer=188.5 text='The two ends make one circle, diameter 60. Circumference = π × 60, to 1 d.p. ='
   step3 field=pre answer=388.5 text='Total: 200 + 188.5 ='
   step4 field=pre answer=388 text='Before rounding, the total is really 388.49 m, which is just below 388.5, so to the neares'
   step5 field=pre answer=188 text='Check: 388 − 200 ='
