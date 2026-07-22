# apply-pack: graphs__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[1] | First root, from (x − 2) = 0: x = [box=2] | fix: Add an intermediate step before the first-root ask: "So the factors are (x − 2)(x − 3) = 0. Each bracket can equal 0."
- [medium] silver[6] | First root, from (x + 4) = 0: x = [box=-4] | fix: Insert "So the factors are (x + 4)(x − 3) = 0" and show that x + 4 = 0 rearranges to x = −4.
- [medium] silver[5] | Turning point x = −b/(2a) = −2/(−2) = [box=1] | fix: Add a preceding step reading a and b and computing 2a and −b before writing −2/(−2), e.g. 'a = −1, b = 2, so 2a = −2 and −b = −2; then −b/(2a) = −2/(−2)'.
- [medium] gold[2] | Q: What are the coordinates of the turning point?Give the y-coordinate. | fix: Add the missing space and make the ask single: 'Find the y-coordinate of the turning point.' (or 'What are the coordinates of the turning point? Give the y-coor

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: \(y = -x^2 + 6x - 5\). Is the turning point a maximum or minimum?

silver[1] Q: Find the roots of \(x^2 + x - 12 = 0\).
   step0 field=say answer=None text='Roots are where y = 0. Two numbers multiply to −12 and add to +1: that is +4 and −3, so (x'
   step1 field=pre answer=-4 text='First bracket zero: x + 4 = 0, so x ='
   step2 field=pre answer=3 text='Second bracket zero: x − 3 = 0, so x ='
   step3 field=pre answer=0 text='Check x = −4: (−4)² + (−4) − 12 = 16 − 4 − 12 ='

silver[5] Q: Find the roots of \(x^2 - 9 = 0\).
   step0 field=say answer=None text='Set y = 0: x² − 9 = 0, so x² = 9. Take the square root, remembering both signs.'
   step1 field=pre answer=3 text='The positive square root of 9 is x ='
   step2 field=pre answer=-3 text='The other root is the negative: x ='
   step3 field=pre answer=0 text='Check: (−3)² − 9 = 9 − 9 ='

silver[6] Q: What is the y-intercept of \(y = 2x^2 - 3x + 7\)?
   step0 field=say answer=None text='The y-intercept is the value at x = 0. Every term with an x disappears.'
   step1 field=pre answer=0 text='The 2x² term at x = 0: 2 × 0² ='
   step2 field=pre answer=0 text='The −3x term at x = 0: −3 × 0 ='
   step3 field=pre answer=7 text='So y = 0 − 0 + 7 ='

### board=maths-edexcel
gold[2] Q: For \(y = -x^2 + 6x - 5\), find the maximum y-value.
   step0 field=pre answer=3 text='Denominator 2 × (−1) = −2, so x = −6 ÷ (−2) ='
   step1 field=pre answer=9 text='Substitute x = 3: square first, 3² ='
   step2 field=pre answer=4 text='y = −(9) + 6(3) − 5 = −9 + 18 − 5 ='
   step3 field=pre answer=4 text='Check it is a maximum: a = −1 < 0, so the ∩ curve peaks here. Confirm 18 − 9 − 5 ='

silver[1] Q: Find the roots of \(y = x^2 - 5x + 6\).
   step0 field=pre answer=6 text='Two numbers multiply to +6 and add to −5: they are −2 and −3. Product: (−2) × (−3) ='
   step1 field=pre answer=2 text='First root, from (x − 2) = 0: x ='
   step2 field=pre answer=3 text='Second root, from (x − 3) = 0: x ='
   step3 field=pre answer=5 text='Check: the roots should add to −b = 5. 2 + 3 ='

silver[5] Q: For \(y = x^2 - 4x\), find the x-coordinate of the turning point.
   step0 field=pre answer=4 text='The formula needs −b: −(−4) ='
   step1 field=pre answer=2 text='Divide by 2a = 2: x = 4 ÷ 2 ='
   step2 field=pre answer=2 text='Check with the roots: x(x − 4) = 0 gives roots 0 and 4; midpoint (0 + 4) ÷ 2 ='

silver[6] Q: Find the roots of \(y = x^2 + x - 12\).
   step0 field=pre answer=-12 text='Two numbers multiply to −12 and add to +1: they are +4 and −3. Product: 4 × (−3) ='
   step1 field=pre answer=-4 text='First root, from (x + 4) = 0: x ='
   step2 field=pre answer=3 text='Second root, from (x − 3) = 0: x ='
   step3 field=pre answer=-1 text='Check: the roots should add to −b = −1. (−4) + 3 ='

### board=maths-ocr
gold[2] Q: The roots of a quadratic are \(x = -1\) and \(x = 9\). Find the x-coordinate of the turnin
   step0 field=pre answer=8 text='The turning point is halfway between the roots. Add them: −1 + 9 ='
   step1 field=pre answer=4 text='Halve it: 8 ÷ 2 ='
   step2 field=pre answer=4 text='So the turning point x-coordinate is'
   step3 field=pre answer=4 text='Check the distances: 4 is 5 away from −1 and 5 away from 9. Equal, so the midpoint x is'

silver[1] Q: Find the turning point of \(y = x^2 - 4x + 1\). Give the x-coordinate.
   step0 field=pre answer=2 text='Read a and b: a = 1, b = −4. Work out 2a = 2 × 1 ='
   step1 field=pre answer=4 text='Now −b = −(−4) ='
   step2 field=pre answer=2 text='Divide: 4 ÷ 2 ='
   step3 field=pre answer=2 text='Check by symmetry: y at x = 1 is 1 − 4 + 1 = −2; y at x = 3 is 9 − 12 + 1 = −2. Equal, so '

silver[5] Q: For \(y = -x^2 + 2x + 3\), what is the maximum value of \(y\)?
   step0 field=pre answer=1 text='Turning point x = −b/(2a) = −2/(−2) ='
   step1 field=pre answer=-1 text='Substitute x = 1. The −x² term: −(1²) ='
   step2 field=pre answer=2 text='The +2x term: 2 × 1 ='
   step3 field=pre answer=4 text='Add with +3: −1 + 2 + 3 ='
   step4 field=pre answer=4 text='Shape check: a = −1 < 0, so it opens down and this is the highest point. Max y ='

silver[6] Q: How many roots does \(y = x^2 + 4\) have?
   step0 field=pre answer=0 text='Roots are where y = 0. The smallest x² can be is at x = 0: 0² ='
   step1 field=pre answer=4 text='Then the lowest y is 0 + 4 ='
   step2 field=pre answer=0 text='The bottom of the curve is y = 4, above the x-axis, so it never reaches 0. Number of cross'
   step3 field=pre answer=0 text='Check: x² is never negative, so x² + 4 is always at least 4, never 0. Number of roots ='

### board=maths-eduqas
gold[2] Q: The curve \(y = (x - 3)^2 - 4\) is in completed square form. What are the coordinates of t
   step0 field=say answer=None text='Completed square form \\(y = (x - a)^2 + b\\) has its turning point at (a, b). Compare (x − '
   step1 field=pre answer=3 text='The number inside the bracket gives a: x − 3 means a ='
   step2 field=pre answer=-4 text='The number outside gives b, the y of the turning point: (x − 3)² − 4 means b ='
   step3 field=pre answer=-4 text='Check by substituting x = 3: (3 − 3)² − 4 = 0 − 4 ='

silver[1] Q: For \(y = x^2 - 4x - 5\), find the \(y\)-coordinate of the turning point.
   step0 field=say answer=None text='The roots are −1 and 5, so the turning point x = (−1 + 5) ÷ 2 = 2. Now substitute x = 2.'
   step1 field=pre answer=4 text='The square: 2² ='
   step2 field=pre answer=-8 text='The middle term: −4 × 2 ='
   step3 field=pre answer=-9 text='So y = 4 + (−8) + (−5) ='
   step4 field=pre answer=-9 text='Check: 4 − 8 = −4, then −4 − 5 ='

silver[5] Q: A quadratic has roots at \(x = 2\) and \(x = 6\). What is the \(x\)-coordinate of the line
   step0 field=say answer=None text='The line of symmetry runs through the turning point, halfway between the roots.'
   step1 field=pre answer=8 text='Add the roots: 2 + 6 ='
   step2 field=pre answer=4 text='Halfway means divide by 2: 8 ÷ 2 ='
   step3 field=pre answer=2 text='Check the gaps: from 2 to 4 is 2, and from 4 to 6 is'

silver[6] Q: For \(y = 2x^2 - 8x + 6\), find \(y\) when \(x = 1\).
   step0 field=say answer=None text='Substitute x = 1. The first term has a 2 in front.'
   step1 field=pre answer=2 text='The squared term: 2 × 1² = 2 × 1 ='
   step2 field=pre answer=-8 text='The middle term: −8 × 1 ='
   step3 field=pre answer=0 text='So y = 2 − 8 + 6 ='
   step4 field=pre answer=0 text='Check: 2 − 8 = −6, then −6 + 6 ='
