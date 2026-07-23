# apply-pack: graphs__L08.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[0] (same phrasing in bronze[1], bronze[7], silver[3], gold[2]) | check, from (1, 3) go across 4 and up gradient×run: 3 + (2)×4 = | fix: Reword, e.g. 'from (1, 3) go across the run (4), then up by gradient × run = 2 × 4, so 3 + 8 ='.
- [low] gold[2] | (2, 18)(6, 2)x = 4Diagram not drawn accuratelyThe tangent to a curve at x = 4 pa | fix: Move the labels to the diagram and begin the stem at 'The tangent to a curve at x = 4 passes through (2, 18) and (6, 2).'
- [low] gold[3] | estimate 42actual area 40Diagram not drawn accuratelyThe trapezium rule with 5 s | fix: Put the callouts on the diagram; begin the stem at 'The trapezium rule with 5 strips gives an area of 42. The actual area is 40.'
- [low] silver[0] | Check by adding the trapezia one at a time (7 + 19): ask: 7 + 19 = [box=26, NO l | fix: Show one strip before summing, e.g. 'first strip = ½(1+6)×2 = 7, second strip = ½(6+13)×2 = 19', then add.
- [low] bronze[6] — also silver[5] | middle heights: 1 = [box=1] | fix: Reword the single-middle case, e.g. 'there is only one middle height, so write it here: 1' or 'middle heights (just one): 1'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: A tangent to a curve passes through \((1, 3)\) and \((5, 11)\). What is the gradient of th
   step0 field=say answer=None text='Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the ru'
   step1 field=pre answer=8 text='rise: 11 − 3 ='
   step2 field=pre answer=4 text='run: 5 − 1 ='
   step3 field=pre answer=2 text='gradient: 8 ÷ 4 ='
   step4 field=pre answer=11 text='check, from (1, 3) go across 4 and up gradient×run: 3 + (2)×4 ='

bronze[6] Q: 051015200246810time (s)speed (m/s)10 s20 m/sArea under speed-time = distanceOn a speed-tim
   step0 field=say answer=None text='Distance = area under the speed-time graph. This is a triangle: ½ × base × height.'
   step1 field=pre answer=200 text='base × height: 10 × 20 ='
   step2 field=pre answer=100 text='½ × 200 ='
   step3 field=pre answer=200 text='check by doubling: 2 × 100 ='

gold[2] Q: On \(y = x^3\), a tangent at \(x = 2\) passes through \((1, -4)\) and \((3, 20)\). Find th
   step0 field=say answer=None text='Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the ru'
   step1 field=pre answer=24 text='rise: 20 − (-4) ='
   step2 field=pre answer=2 text='run: 3 − 1 ='
   step3 field=pre answer=12 text='gradient: 24 ÷ 2 ='
   step4 field=pre answer=20 text='check, from (1, -4) go across 2 and up gradient×run: -4 + (12)×2 ='

gold[3] Q: Use the trapezium rule with \(h = 0.5\) and y-values 0, 0.25, 1, 2.25, 4 to estimate the a
   step0 field=say answer=None text='Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].'
   step1 field=pre answer=3.5 text='add the middle values: 0.25 + 1 + 2.25 ='
   step2 field=pre answer=7 text='double them: 2 × 3.5 ='
   step3 field=pre answer=4 text='first + last: 0 + 4 ='
   step4 field=pre answer=11 text='bracket total: 4 + 7 ='
   step5 field=pre answer=0.25 text='h ÷ 2 = 0.5 ÷ 2 ='
   step6 field=pre answer=2.75 text='A = 0.25 × 11 ='

silver[0] Q: Use the trapezium rule with 3 strips (\(h = 2\)) and y-values 0, 4, 12, 24 to estimate the
   step0 field=say answer=None text='Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].'
   step1 field=pre answer=16 text='add the middle values: 4 + 12 ='
   step2 field=pre answer=32 text='double them: 2 × 16 ='
   step3 field=pre answer=24 text='first + last: 0 + 24 ='
   step4 field=pre answer=56 text='bracket total: 24 + 32 ='
   step5 field=pre answer=1 text='h ÷ 2 = 2 ÷ 2 ='
   step6 field=pre answer=56 text='A = 1 × 56 ='

### board=maths-edexcel
bronze[0] Q: A tangent line passes through \((2, 4)\) and \((6, 12)\). What is the gradient?
   step0 field=say answer=None text='A tangent is a straight line, so its gradient is the change in y divided by the change in '
   step1 field=pre answer=8 text='change in y: 12 − 4 ='
   step2 field=pre answer=4 text='change in x: 6 − 2 ='
   step3 field=pre answer=2 text='gradient = 8 ÷ 4 ='
   step4 field=pre answer=12 text='4 + 2 × 4 ='

bronze[6] Q: On a speed-time graph, what does the area under the curve represent?

gold[2] Q: (2, 18)(6, 2)x = 4Diagram not drawn accuratelyThe tangent to a curve at \(x = 4\) passes t

gold[3] Q: estimate 42actual area 40Diagram not drawn accuratelyThe trapezium rule with 5 strips give

silver[0] Q: Use the trapezium rule with 2 strips to estimate the area under a curve: \(y_0 = 2, y_1 = 
   step0 field=say answer=None text='The strip width h is the total x-range shared equally between the strips. Find the range f'
   step1 field=pre answer=6 text='total x-range: 6 − 0 ='
   step2 field=pre answer=2 text='number of strips:'
   step3 field=pre answer=3 text='strip width h = 6 ÷ 2 ='
   step4 field=pre answer=3 text='3 − 0 ='

### board=maths-ocr
bronze[0] Q: A tangent passes through \((2, 4)\) and \((6, 12)\). Find the gradient.
   step0 field=pre answer=8 text='12 − 4 ='
   step1 field=pre answer=4 text='6 − 2 ='
   step2 field=pre answer=2 text='8 ÷ 4 ='
   step3 field=pre answer=12 text='4 + (8) ='

bronze[6] Q: 464Diagram not drawn accuratelyA trapezium has parallel sides 4 and 6, height 4. Find the 
   step0 field=pre answer=10 text='4 + 6 ='
   step1 field=pre answer=5 text='average them: 10 ÷ 2 ='
   step2 field=pre answer=20 text='5 × 4 ='
   step3 field=pre answer=20 text='½ × 10 × 4 ='

gold[2] Q: The trapezium rule gives area 48.5. The exact area is 45. Find the percentage error to 1 d
   step0 field=pre answer=3.5 text='48.5 − 45 ='
   step1 field=pre answer=7.8 text='3.5 ÷ 45 × 100 ='
   step2 field=pre answer=3.5 text='enter the error, 3.5 ='

gold[3] Q: A curve has \(y = x^3\). Estimate the gradient at \(x = 2\) using \((1.9, 6.859)\) and \((
   step0 field=pre answer=2.402 text='9.261 − 6.859 ='
   step1 field=pre answer=0.2 text='run: 2.1 − 1.9 ='
   step2 field=pre answer=12.01 text='2.402 ÷ 0.2 ='
   step3 field=pre answer=12 text='the exact gradient is 3x², so at x = 2 it is 3 × 4 ='

silver[0] Q: Trapezium rule: \(h = 2\), y-values: 1, 6, 13. Find the area.
   step0 field=pre answer=14 text='1 + 13 ='
   step1 field=pre answer=12 text='2 × 6 ='
   step2 field=pre answer=26 text='14 + 12 ='
   step3 field=pre answer=26 text='1 × 26 ='
   step4 field=pre answer=26 text='7 + 19 ='

### board=maths-eduqas
bronze[0] Q: xyrun 4rise 8(2, 5)(6, 13)A tangent to a curve passes through \((2, 5)\) and \((6, 13)\). 
   step0 field=pre answer=8 text='rise = 13 − 5 ='
   step1 field=pre answer=4 text='run = 6 − 2 ='
   step2 field=pre answer=2 text='gradient = 8 ÷ 4 ='
   step3 field=pre answer=8 text='check: run × gradient = 4 × 2 ='

bronze[6] Q: Use the trapezium rule with 2 strips to estimate the area under \(y = x^2\) from \(x = 0\)
   step0 field=pre answer=4 text='first + last = 0 + 4 ='
   step1 field=pre answer=1 text='middle heights: 1 ='
   step2 field=pre answer=2 text='double the middles: 2 × 1 ='
   step3 field=pre answer=6 text='brackets: 4 + 2 ='
   step4 field=pre answer=3 text='each strip has width h = 1, so area ≈ (h ÷ 2) × 6 = (1 ÷ 2) × 6 ='

gold[2] Q: xyrun 6rise −12(4, 18)(10, 6)A speed-time curve has a tangent at \(t = 6\) passing through
   step0 field=pre answer=-12 text='rise = 6 − 18 ='
   step1 field=pre answer=6 text='run = 10 − 4 ='
   step2 field=pre answer=-2 text='gradient = −12 ÷ 6 ='
   step3 field=pre answer=-12 text='check: run × gradient = 6 × −2 ='

gold[3] Q: The exact area under \(y = x^2\) from 0 to 3 is 9. The trapezium rule (3 strips) gives 9.5

silver[0] Q: Use the trapezium rule with 3 strips to estimate the area under \(y = x^2\) from \(x = 0\)
   step0 field=pre answer=9 text='first + last = 0 + 9 ='
   step1 field=pre answer=5 text='middle heights: 1 + 4 ='
   step2 field=pre answer=10 text='double the middles: 2 × 5 ='
   step3 field=pre answer=19 text='brackets: 9 + 10 ='
   step4 field=pre answer=9.5 text='area ≈ (1 ÷ 2) × 19 ='
