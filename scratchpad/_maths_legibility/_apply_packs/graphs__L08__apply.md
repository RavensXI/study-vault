# apply-pack: graphs__L08.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] bronze[3] | y = 3y = 7h = 2Diagram not drawn accuratelyEstimate the area of one trapezium wi | fix: Keep the labels on the diagram and start the stem at 'Estimate the area of one trapezium with parallel sides y = 3 and y = 7, width h = 2.' If labels must appea
- [medium] bronze[4] | y = 5y = 5h = 4Diagram not drawn accuratelyEstimate the area of one trapezium wi | fix: Move the labels onto the diagram; begin the stem at 'Estimate the area of one trapezium with parallel sides y = 5 and y = 5, width h = 4.'
- [medium] gold[4] | 10181406t (s)Diagram not drawn accuratelyA speed-time graph is estimated using 3 | fix: Keep the diagram numbers on the diagram; start the stem at 'A speed-time graph is estimated using 3 trapeziums: area1 = 10, area2 = 18, area3 = 14.'
- [high] bronze[4] | Q: 46Diagram not drawn accuratelyEstimate the area of a triangle: base 4, height | fix: Strip the OCR artefact and space it out: 'Diagram not drawn accurately. Estimate the area of a triangle: base 4, height 6.' (or drop the diagram note entirely).
- [high] bronze[6] | Q: 464Diagram not drawn accuratelyA trapezium has parallel sides 4 and 6, height | fix: Remove the leading '464' and separate the note: 'Diagram not drawn accurately. A trapezium has parallel sides 4 and 6, height 4. Find the area.'
- [high] bronze[3] | Q: 35Estimate the area of a rectangle: width 3, height 5. | fix: Delete the leading '35' and add a space: 'Estimate the area of a rectangle: width 3, height 5.'
- [medium] bronze[7] | Q: (3, 7)(5, 7)A tangent passes through \((3, 7)\) and \((5, 7)\). Find the grad | fix: Remove the leading duplicate coordinates: 'A tangent passes through (3, 7) and (5, 7). Find the gradient.'
- [medium] silver[4] | Q: gradient = 0A curve has gradient 0 at \(x = 3\). What does this tell you? | fix: Drop the leading fragment: 'A curve has gradient 0 at x = 3. What does this tell you?'
- [medium] gold[3] | Check against the exact gradient. For \(y = x^3\) it is \(3x^2\), and at x = 2 t | fix: Replace the calculus check with one the walk supports, e.g. compare the chord estimate (12.01) back to the chord itself, or state plainly that 3x^2 is a shortcu
- [medium] bronze[0] — recurs in all 8 tangent problems: bronze[1], bronze[3], bronze[5], bronze[7], silver[2], silver[3], gold[2] | Q: xyrun 4rise 8(2, 5)(6, 13)A tangent to a curve passes through (2, 5) and (6,  | fix: Strip the diagram's axis/annotation text out of the question stem and separate the caption, e.g. render just 'A tangent to a curve passes through (2, 5) and (6,
- [medium] bronze[6] — also silver[0], gold[0] (the three y = x^2 problems) | area ≈ (1 ÷ 2) × 6 = [box=3, label:'cm²'] | fix: Add a step before the final line: 'strip width h = (2 − 0) ÷ 2 =' (box=1), or state 'strip width h = 1' in the intro, so h is not unexplained in the final formu

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: A tangent to a curve passes through \((1, 3)\) and \((5, 11)\). What is the gradient of th
   step0 field=say answer=None text='Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the ru'
   step1 field=pre answer=8 text='rise: 11 − 3 ='
   step2 field=pre answer=4 text='run: 5 − 1 ='
   step3 field=pre answer=2 text='gradient: 8 ÷ 4 ='
   step4 field=pre answer=11 text='check, from (1, 3) go across 4 and up gradient×run: 3 + (2)×4 ='

bronze[3] Q: 104height = 3Diagram not drawn accuratelyEstimate the area of a trapezium with parallel si
   step0 field=say answer=None text='Area of a trapezium = ½ × (sum of the parallel sides) × height.'
   step1 field=pre answer=14 text='sum of the parallel sides: 4 + 10 ='
   step2 field=pre answer=42 text='× height: 14 × 3 ='
   step3 field=pre answer=21 text='½ × 42 ='
   step4 field=pre answer=42 text='check by doubling: 2 × 21 ='

bronze[4] Q: 04812012345time (s)speed (m/s)5 s12 m/sArea under speed-time = distanceA rectangle on a sp
   step0 field=say answer=None text='On a speed-time graph the distance is the area of the shape. This is a rectangle: width × '
   step1 field=pre answer=5 text='width in seconds: read it off ='
   step2 field=pre answer=12 text='height in m/s: read it off ='
   step3 field=pre answer=60 text='area: 5 × 12 ='
   step4 field=pre answer=12 text='check the speed back: 60 ÷ 5 ='

bronze[6] Q: 051015200246810time (s)speed (m/s)10 s20 m/sArea under speed-time = distanceOn a speed-tim
   step0 field=say answer=None text='Distance = area under the speed-time graph. This is a triangle: ½ × base × height.'
   step1 field=pre answer=200 text='base × height: 10 × 20 ='
   step2 field=pre answer=100 text='½ × 200 ='
   step3 field=pre answer=200 text='check by doubling: 2 × 100 ='

bronze[7] Q: A tangent to a curve at \(x = 2\) passes through \((1, 2)\) and \((3, 12)\). What is the g
   step0 field=say answer=None text='Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the ru'
   step1 field=pre answer=10 text='rise: 12 − 2 ='
   step2 field=pre answer=2 text='run: 3 − 1 ='
   step3 field=pre answer=5 text='gradient: 10 ÷ 2 ='
   step4 field=pre answer=12 text='check, from (1, 2) go across 2 and up gradient×run: 2 + (5)×2 ='

gold[3] Q: Use the trapezium rule with \(h = 0.5\) and y-values 0, 0.25, 1, 2.25, 4 to estimate the a
   step0 field=say answer=None text='Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].'
   step1 field=pre answer=3.5 text='add the middle values: 0.25 + 1 + 2.25 ='
   step2 field=pre answer=7 text='double them: 2 × 3.5 ='
   step3 field=pre answer=4 text='first + last: 0 + 4 ='
   step4 field=pre answer=11 text='bracket total: 4 + 7 ='
   step5 field=pre answer=0.25 text='h ÷ 2 = 0.5 ÷ 2 ='
   step6 field=pre answer=2.75 text='A = 0.25 × 11 ='

gold[4] Q: Explain why using more strips in the trapezium rule gives a better estimate. What happens 

silver[4] Q: Use the trapezium rule with 4 strips (\(h = 1\)) and y-values 0, 3, 8, 15, 24. Estimate th
   step0 field=say answer=None text='Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].'
   step1 field=pre answer=26 text='add the middle values: 3 + 8 + 15 ='
   step2 field=pre answer=52 text='double them: 2 × 26 ='
   step3 field=pre answer=24 text='first + last: 0 + 24 ='
   step4 field=pre answer=76 text='bracket total: 24 + 52 ='
   step5 field=pre answer=0.5 text='h ÷ 2 = 1 ÷ 2 ='
   step6 field=pre answer=38 text='A = 0.5 × 76 ='

### board=maths-edexcel
bronze[0] Q: A tangent line passes through \((2, 4)\) and \((6, 12)\). What is the gradient?
   step0 field=say answer=None text='A tangent is a straight line, so its gradient is the change in y divided by the change in '
   step1 field=pre answer=8 text='change in y: 12 − 4 ='
   step2 field=pre answer=4 text='change in x: 6 − 2 ='
   step3 field=pre answer=2 text='gradient = 8 ÷ 4 ='
   step4 field=pre answer=12 text='4 + 2 × 4 ='

bronze[3] Q: y = 3y = 7h = 2Diagram not drawn accuratelyEstimate the area of one trapezium with paralle
   step0 field=say answer=None text='A trapezium strip is half of (side + side) times the width. Build it one step at a time. F'
   step1 field=pre answer=10 text='3 + 7 ='
   step2 field=pre answer=20 text='multiply by the width h = 2: 10 × 2 ='
   step3 field=pre answer=10 text='now halve it: 20 ÷ 2 ='
   step4 field=pre answer=10 text='5 × 2 ='

bronze[4] Q: y = 5y = 5h = 4Diagram not drawn accuratelyEstimate the area of one trapezium with paralle
   step0 field=say answer=None text='Same trapezium rule: half of (side + side) times the width. Add the sides first:'
   step1 field=pre answer=10 text='5 + 5 ='
   step2 field=pre answer=40 text='multiply by the width h = 4: 10 × 4 ='
   step3 field=pre answer=20 text='now halve it: 40 ÷ 2 ='
   step4 field=pre answer=20 text='5 × 4 ='

bronze[6] Q: On a speed-time graph, what does the area under the curve represent?

bronze[7] Q: On a distance-time graph, what does the gradient represent?

gold[3] Q: estimate 42actual area 40Diagram not drawn accuratelyThe trapezium rule with 5 strips give

gold[4] Q: 10181406t (s)Diagram not drawn accuratelyA speed-time graph is estimated using 3 trapezium
   step0 field=say answer=None text='The three trapezium areas add up to the total distance (the whole area under the graph).'
   step1 field=pre answer=42 text='total distance = 10 + 18 + 14 ='
   step2 field=pre answer=6 text='total time = 6 − 0 ='
   step3 field=pre answer=7 text='average speed = 42 ÷ 6 ='
   step4 field=pre answer=42 text='7 × 6 ='

silver[4] Q: The gradient of a distance-time graph at \(t = 4\) is estimated as 12. What does this tell

### board=maths-ocr
bronze[0] Q: A tangent passes through \((2, 4)\) and \((6, 12)\). Find the gradient.
   step0 field=pre answer=8 text='12 − 4 ='
   step1 field=pre answer=4 text='6 − 2 ='
   step2 field=pre answer=2 text='8 ÷ 4 ='
   step3 field=pre answer=12 text='4 + (8) ='

bronze[3] Q: 35Estimate the area of a rectangle: width 3, height 5.
   step0 field=pre answer=3 text='base ='
   step1 field=pre answer=5 text='height ='
   step2 field=pre answer=15 text='3 × 5 ='
   step3 field=pre answer=15 text='3 + 3 + 3 + 3 + 3 ='

bronze[4] Q: 46Diagram not drawn accuratelyEstimate the area of a triangle: base 4, height 6.
   step0 field=pre answer=24 text='4 × 6 ='
   step1 field=pre answer=12 text='24 ÷ 2 ='
   step2 field=pre answer=12 text='2 × 6 ='

bronze[6] Q: 464Diagram not drawn accuratelyA trapezium has parallel sides 4 and 6, height 4. Find the 
   step0 field=pre answer=10 text='4 + 6 ='
   step1 field=pre answer=5 text='average them: 10 ÷ 2 ='
   step2 field=pre answer=20 text='5 × 4 ='
   step3 field=pre answer=20 text='½ × 10 × 4 ='

bronze[7] Q: (3, 7)(5, 7)A tangent passes through \((3, 7)\) and \((5, 7)\). Find the gradient.
   step0 field=pre answer=0 text='7 − 7 ='
   step1 field=pre answer=2 text='run: 5 − 3 ='
   step2 field=pre answer=0 text='0 ÷ 2 ='
   step3 field=pre answer=0 text='gradient ='

gold[3] Q: A curve has \(y = x^3\). Estimate the gradient at \(x = 2\) using \((1.9, 6.859)\) and \((
   step0 field=pre answer=2.402 text='9.261 − 6.859 ='
   step1 field=pre answer=0.2 text='run: 2.1 − 1.9 ='
   step2 field=pre answer=12.01 text='2.402 ÷ 0.2 ='
   step3 field=pre answer=12 text='3 × 4 ='

gold[4] Q: Trapezium rule: \(h = 0.5\), y-values: 1, 1.5, 2.5, 4, 6. Find the area.
   step0 field=pre answer=7 text='1 + 6 ='
   step1 field=pre answer=16.0 text='2 × (1.5 + 2.5 + 4) ='
   step2 field=pre answer=23.0 text='7 + 16 ='
   step3 field=pre answer=5.75 text='0.25 × 23 ='
   step4 field=pre answer=5.75 text='0.625 + 1 + 1.625 + 2.5 ='

silver[4] Q: gradient = 0A curve has gradient 0 at \(x = 3\). What does this tell you?

### board=maths-eduqas
bronze[0] Q: xyrun 4rise 8(2, 5)(6, 13)A tangent to a curve passes through \((2, 5)\) and \((6, 13)\). 
   step0 field=pre answer=8 text='rise = 13 − 5 ='
   step1 field=pre answer=4 text='run = 6 − 2 ='
   step2 field=pre answer=2 text='gradient = 8 ÷ 4 ='
   step3 field=pre answer=8 text='check: run × gradient = 4 × 2 ='

bronze[3] Q: xyrun 4rise −8(0, 8)(4, 0)A tangent to a curve passes through \((0, 8)\) and \((4, 0)\). W
   step0 field=pre answer=-8 text='rise = 0 − 8 ='
   step1 field=pre answer=4 text='run = 4 − 0 ='
   step2 field=pre answer=-2 text='gradient = −8 ÷ 4 ='
   step3 field=pre answer=-8 text='check: run × gradient = 4 × −2 ='

bronze[4] Q: What does the area under a speed-time graph represent?

bronze[6] Q: Use the trapezium rule with 2 strips to estimate the area under \(y = x^2\) from \(x = 0\)
   step0 field=pre answer=4 text='first + last = 0 + 4 ='
   step1 field=pre answer=1 text='middle heights: 1 ='
   step2 field=pre answer=2 text='double the middles: 2 × 1 ='
   step3 field=pre answer=6 text='brackets: 4 + 2 ='
   step4 field=pre answer=3 text='area ≈ (1 ÷ 2) × 6 ='

bronze[7] Q: xyrun 2rise 10(1, 2)(3, 12)A tangent to a curve passes through \((1, 2)\) and \((3, 12)\).
   step0 field=pre answer=10 text='rise = 12 − 2 ='
   step1 field=pre answer=2 text='run = 3 − 1 ='
   step2 field=pre answer=5 text='gradient = 10 ÷ 2 ='
   step3 field=pre answer=10 text='check: run × gradient = 2 × 5 ='

gold[3] Q: The exact area under \(y = x^2\) from 0 to 3 is 9. The trapezium rule (3 strips) gives 9.5

gold[4] Q: Use the trapezium rule with 3 strips to estimate the area under a curve. Strip width \(h =
   step0 field=pre answer=19 text='first + last = 2 + 17 ='
   step1 field=pre answer=15 text='middle heights: 5 + 10 ='
   step2 field=pre answer=30 text='double the middles: 2 × 15 ='
   step3 field=pre answer=49 text='brackets: 19 + 30 ='
   step4 field=pre answer=98 text='area ≈ (4 ÷ 2) × 49 ='

silver[4] Q: The trapezium rule gives an overestimate when the curve is:
