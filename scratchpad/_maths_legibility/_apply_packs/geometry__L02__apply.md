# apply-pack: geometry__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[4] box (=24, labelled cm²) | Area of one triangle: first 6 × 4 = | fix: Reword the lead-in to 'Base × height first: 6 × 4 =' (24 cm² is legitimate as the rectangle/base×height area — just don't call it the triangle's area).
- [medium] silver[6] | Q stem: 'r 312 cm8 cm...A rectangle 12 cm by 8 cm has a circle of radius 3 cm cu | fix: Separate the diagram labels: 'r = 3 cm; rectangle 12 cm x 8 cm' (and likewise for gold[2]/gold[3]).
- [medium] gold[0] | Quarter-circle: 0.25 × π × 36, to 2 d.p. = [box=28.27, NO label] | fix: Add an explicit 'r squared: 6² = [36]' step before this one, or write the formula as '0.25 × π × 6²'.
- [medium] gold[3] | The fuller value is 388.49, just under 388.5, so to the nearest metre it is | fix: Rephrase, e.g. 'Before rounding, the total is 388.49 m, which rounds down to 388 m.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: 135°r = 8 cmDiagram not drawn accuratelyA sector has radius 8 cm and angle 135°. Find the 
   step0 field=say answer=None text='A sector is a fraction of the whole circle: fraction = angle ÷ 360.'
   step1 field=pre answer=64 text='Square the radius: 8 × 8 ='
   step2 field=pre answer=0.375 text='Fraction of the circle = 135 ÷ 360 ='
   step3 field=pre answer=75.4 text='Sector area = 0.375 × π × 64, to 1 decimal place ='
   step4 field=pre answer=75.4 text='Cross-check: the whole circle is π × 64 ≈ 201.1, and 0.375 × 201.1 ='

gold[3] Q: Area 154A circle has area 154 cm². Find the radius to 1 decimal place.
   step0 field=say answer=None text='Work area = π r² backwards. Divide by π, then take the square root.'
   step1 field=pre answer=49 text='Divide the area by π: 154 ÷ π, to the nearest whole ='
   step2 field=pre answer=7 text='That is r². Square-root it: √49 ='
   step3 field=pre answer=154 text='Check forwards: π × 7² = π × 49, to the nearest whole ='

silver[4] Q: base 6 cm4 cmDiagram not drawn accuratelyTwo congruent triangles with base 6 cm and height
   step0 field=say answer=None text='Two identical triangles slot together into a parallelogram, area base × height.'
   step1 field=pre answer=24 text='Area of one triangle: first 6 × 4 ='
   step2 field=pre answer=12 text='Halve it for the triangle: 24 ÷ 2 ='
   step3 field=pre answer=24 text='Two triangles make the parallelogram: 12 × 2 ='
   step4 field=pre answer=24 text='Or straight from base × height: 6 × 4 ='

silver[6] Q: 6 cm5 cm24Diagram not drawn accuratelyAn L-shape is formed by cutting a 2 cm × 4 cm rectan
   step0 field=say answer=None text='The L-shape is the whole rectangle minus the cut-out corner.'
   step1 field=pre answer=30 text='Whole rectangle = 6 × 5 ='
   step2 field=pre answer=8 text='Cut-out corner = 2 × 4 ='
   step3 field=pre answer=22 text='Subtract: 30 − 8 ='
   step4 field=pre answer=8 text='Check: the L-shape is smaller than the rectangle by exactly the corner, 30 − 22 ='

### board=maths-edexcel
gold[0] Q: 100 m60 mA running track is two straight sides of 100 m and two semicircular ends of diame
   step0 field=say answer=None text='The perimeter is the two straight sides plus the two curved ends. The two semicircular end'
   step1 field=pre answer=200 text='The two straights: 2 × 100 ='
   step2 field=pre answer=188.5 text='The two ends make one full circle, circumference π × diameter. On your calculator, π × 60 '
   step3 field=pre answer=388 text="Add, using the calculator's full value (not the rounded 188.5), then round the total to th"
   step4 field=pre answer=200 text='Check the straights alone come to 200: 100 + 100 ='

gold[3] Q: θ = ?9 cmarc 12 cmDiagram not drawn accuratelyA sector has arc length 12 cm and radius 9 c
   step0 field=say answer=None text='Arc length is a fraction of the full circumference. The fraction is the angle over 360, so'
   step1 field=pre answer=56.55 text='Full circumference = 2 × π × radius = 2 × π × 9 ='
   step2 field=pre answer=0.2122 text='The arc is 12 out of that whole circumference. Fraction of the circle: 12 ÷ 56.55 ='
   step3 field=pre answer=76 text='Multiply the fraction by 360 for the angle, to the nearest degree: 0.2122 × 360 ='
   step4 field=pre answer=12 text='Check by working forwards: 0.2122 × 56.55 ='

silver[4] Q: 8 cm12 cmh = ?Area = 60 cm²Diagram not drawn accuratelyA trapezium has area 60 cm², parall
   step0 field=say answer=None text='Use the trapezium formula backwards. Area = half × (sum of parallel sides) × height, and t'
   step1 field=pre answer=20 text='Add the parallel sides: 8 + 12 ='
   step2 field=pre answer=10 text='Half of that: 20 ÷ 2 ='
   step3 field=pre answer=6 text='So area = 10 × height. Divide to find the height: 60 ÷ 10 ='
   step4 field=pre answer=60 text='Check by working forwards: 10 × 6 ='

silver[6] Q: r = ?Area = 50.3 cm²The area of a circle is 50.3 cm². Find the radius to 1 d.p.
   step0 field=say answer=None text='Area is π × radius². The area is known, so undo it: divide by π, then square-root.'
   step1 field=pre answer=16.0 text='Divide the area by π: 50.3 ÷ π ='
   step2 field=pre answer=4 text='That is the radius squared. Square-root it: √16 ='
   step3 field=pre answer=50.3 text='Check by working forwards: 4² × π = 16 × π ='

### board=maths-ocr
gold[0] Q: diameter 12 cmDiagram not drawn accuratelyA semicircle has diameter 12 cm. Find the area t
   step0 field=say answer=None text="A semicircle is half a circle. Find the radius, then halve the full circle's area."
   step1 field=pre answer=6 text='Radius = 12 ÷ 2 ='
   step2 field=pre answer=56.5 text='Half a circle is ½ × π × r². Work out ½ × π × 6², to 1 d.p. ='
   step3 field=pre answer=113 text='Check: two semicircles make the full circle, 56.5 × 2 ='

gold[3] Q: R 5r 3Diagram not drawn accuratelyTwo circles share the same centre: radius 3 cm inside ra
   step0 field=say answer=None text="A ring (annulus) is the outer circle's area minus the inner circle's area."
   step1 field=pre answer=25 text='Square the outer radius: 5 × 5 ='
   step2 field=pre answer=9 text='Square the inner radius: 3 × 3 ='
   step3 field=pre answer=16 text='Subtract the squares: 25 − 9 ='
   step4 field=pre answer=50.3 text='Multiply by π: π × 16, to 1 d.p. ='
   step5 field=pre answer=78.5 text='Check: ring plus inner circle equals the outer circle. π × 16 + π × 9 = π × 25, to 1 d.p. '

silver[4] Q: 90°r = 6 cmDiagram not drawn accuratelyA sector has radius 6 cm and angle 90°. Find the ar
   step0 field=say answer=None text='A sector is a fraction of the whole circle. The fraction is angle ÷ 360.'
   step1 field=pre answer=36 text='Square the radius: 6 × 6 ='
   step2 field=pre answer=113.1 text='Full circle area = π × 36, to 1 d.p. ='
   step3 field=pre answer=0.25 text='Fraction of the circle: 90 ÷ 360 ='
   step4 field=pre answer=28.3 text='Sector area = 0.25 × 113.1 ='
   step5 field=pre answer=113.2 text='Check: four quarter-sectors rebuild the circle, 28.3 × 4 ='

silver[6] Q: r 312 cm8 cmA rectangle 12 cm by 8 cm has a circle of radius 3 cm cut out. Find the remain
   step0 field=say answer=None text="Find the rectangle's area, then subtract the circle that is cut out."
   step1 field=pre answer=96 text='Rectangle area: 12 × 8 ='
   step2 field=pre answer=28.3 text='Circle area: π × 3², to 1 d.p. ='
   step3 field=pre answer=67.7 text='Subtract the cut-out: 96 − 28.3 ='
   step4 field=pre answer=96 text='Check by adding the circle back: 67.7 + 28.3 ='

### board=maths-eduqas
gold[0] Q: 10 cm6 cmr = 6A compound shape: rectangle 10 cm × 6 cm with a quarter-circle (radius 6 cm)
   step0 field=say answer=None text='Find the rectangle, then subtract the quarter-circle that has been removed.'
   step1 field=pre answer=60 text='Rectangle: 10 × 6 ='
   step2 field=pre answer=28.27 text='Quarter-circle: 0.25 × π × 36, to 2 d.p. ='
   step3 field=pre answer=31.7 text='Subtract, to 1 d.p.: 60 − 28.27 ='
   step4 field=pre answer=60 text='Check: 31.7 + 28.27, to nearest whole ='

gold[3] Q: 100 md = 60 mA running track is two straights (100 m each) and two semicircles (diameter 6
   step0 field=say answer=None text='The two straights are one length; the two semicircular ends make one full circle. Add them'
   step1 field=pre answer=200 text='Two straights: 2 × 100 ='
   step2 field=pre answer=188.5 text='The two ends make one circle, diameter 60. Circumference = π × 60, to 1 d.p. ='
   step3 field=pre answer=388.5 text='Total: 200 + 188.5 ='
   step4 field=pre answer=388 text='The fuller value is 388.49, just under 388.5, so to the nearest metre it is'
   step5 field=pre answer=188 text='Check: 388 − 200 ='

silver[4] Q: 6 cm120°Area of a sector: radius 6 cm, angle 120°. (1 d.p.)Diagram not drawn accurately
   step0 field=say answer=None text='Sector area = (angle ÷ 360) × π × r². Full circle area first.'
   step1 field=pre answer=36 text='r squared: 6² ='
   step2 field=pre answer=113.1 text='Full circle: 36 × π, to 1 d.p. ='
   step3 field=pre answer=37.7 text='113.1 ÷ 3, to 1 d.p. ='
   step4 field=pre answer=113.1 text='Check: 37.7 × 3, to 1 d.p. ='

silver[6] Q: r = 5 cmA semicircle has radius 5 cm. Find its perimeter (the curved part plus the diamete
   step0 field=say answer=None text='The perimeter of a semicircle = the curved part + the straight diameter = π r + 2r.'
   step1 field=pre answer=15.7 text='Curved part (half the circumference): π × 5, to 1 d.p. ='
   step2 field=pre answer=10 text='Straight part (the diameter): 2 × 5 ='
   step3 field=pre answer=25.7 text='Add them: 15.7 + 10 ='
   step4 field=pre answer=15.7 text='Check: 25.7 − 10 ='
