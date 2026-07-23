# apply-pack: graphs__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[0] | Symmetry check: the vertex is at x = 0, so x = −3 gives the same y. | fix: Replace "vertex" with "turning point" (or write "turning point (vertex)") for consistency with the rest of the pack.
- [low] gold[2] | Check it is a maximum: a = −1 < 0, so the ∩ curve peaks here. | fix: Rephrase to plain words: "Because a is negative (a = −1), the curve is n-shaped and has a highest point here."
- [low] silver[2] | Turning point x = −b/(2a) = 4/2 = [box=2] | fix: Show the substitution: 'a = 1, b = −4, so −b = 4 and 2a = 2, giving −b/(2a) = 4/2'.
- [low] gold[1] | Turning point x = −b/(2a) = 8/4 = [box=2] | fix: Precede with 'a = 2, b = −8, so −b = 8 and 2a = 4, giving −b/(2a) = 8/4'.
- [low] gold[3] | Check with the constant term: c/a = −15/1 = [box=-15] | fix: Name the rule in plain words, e.g. 'For x² + bx + c, the roots multiply to c: here c = −15, so the product should be −15' — or drop the shortcut check entirely.
- [low] silver[1] | Check by symmetry: y at x = 1 is 1 − 4 + 1 = −2; y at x = 3 is 9 − 12 + 1 = −2.  | fix: Split into two shorter lines (compute y at x=1, then y at x=3, then conclude) or trim to one worked pair, e.g. 'Both x = 1 and x = 3 give y = −2, so the turning
- [low] gold[0] | x = −6 ÷ (−2) = [box=3, NO label] | fix: Insert a top-of-fraction step first, e.g. 'Top: −b = −(6) = [box=-6]', then 'x = −6 ÷ (−2) ='.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: For \(y = x^2\), find \(y\) when \(x = 3\).
   step0 field=say answer=None text='For \\(y = x^2\\), just square the x-value: multiply it by itself.'
   step1 field=pre answer=9 text='Write the multiplication: 3 × 3 ='
   step2 field=pre answer=9 text='So when x = 3, y ='
   step3 field=pre answer=9 text='Check with the symmetric point (−3, y): (−3) × (−3) ='

gold[0] Q: Find the roots of \(x^2 + 2x - 15 = 0\).
   step0 field=say answer=None text='Roots are where y = 0. Two numbers multiply to −15 and add to +2: that is +5 and −3, so (x'
   step1 field=pre answer=-5 text='First bracket zero: x + 5 = 0, so x ='
   step2 field=pre answer=3 text='Second bracket zero: x − 3 = 0, so x ='
   step3 field=pre answer=0 text='Check x = 3: 3² + 2×3 − 15 = 9 + 6 − 15 ='

gold[1] Q: The turning point of a quadratic is \((3, -2)\) and it opens upward. Write the equation in
   step0 field=say answer=None text='For a turning point (p, q), the equation is y = (x − p)² + q. Match p and q to the coordin'
   step1 field=pre answer=3 text='The x-coordinate of the turning point is 3, so a ='
   step2 field=pre answer=-2 text='The y-coordinate is −2, so b ='
   step3 field=pre answer=-2 text='Check at x = 3: (3 − 3)² + (−2) = 0 + (−2) ='

gold[2] Q: \(y = -x^2 + 6x - 5\). Is the turning point a maximum or minimum?

gold[3] Q: For \(y = x^2 - 8x + 12\), find the x-coordinate of the turning point.
   step0 field=say answer=None text='The turning point lies on the line of symmetry, halfway between the roots.'
   step1 field=pre answer=2 text='Factorise: (x − 2)(x − 6) = 0. First root x ='
   step2 field=pre answer=6 text='Second root x ='
   step3 field=pre answer=4 text='Halfway between: (2 + 6) ÷ 2 ='
   step4 field=pre answer=-4 text='Check the height: 4² − 8×4 + 12 = 16 − 32 + 12 ='

silver[1] Q: Find the roots of \(x^2 + x - 12 = 0\).
   step0 field=say answer=None text='Roots are where y = 0. Two numbers multiply to −12 and add to +1: that is +4 and −3, so (x'
   step1 field=pre answer=-4 text='First bracket zero: x + 4 = 0, so x ='
   step2 field=pre answer=3 text='Second bracket zero: x − 3 = 0, so x ='
   step3 field=pre answer=0 text='Check x = −4: (−4)² + (−4) − 12 = 16 − 4 − 12 ='

silver[2] Q: Find the turning point of \(y = (x - 4)^2 + 1\). Give the x-coordinate.
   step0 field=say answer=None text='For y = (x − p)² + q, the lowest point is where the bracket is zero.'
   step1 field=pre answer=4 text='The bracket (x − 4) is zero when x ='
   step2 field=pre answer=4 text='That value is p, the x-coordinate of the turning point: x ='
   step3 field=pre answer=1 text='Check the height there: (4 − 4)² + 1 = 0 + 1 ='

### board=maths-edexcel
bronze[0] Q: For \(y = x^2 + 2\), find \(y\) when \(x = 3\).
   step0 field=pre answer=9 text='3² = 3 × 3 ='
   step1 field=pre answer=11 text='Add the constant: 9 + 2 ='
   step2 field=pre answer=11 text='Symmetry check: the vertex is at x = 0, so x = −3 gives the same y. (−3)² + 2 ='

gold[0] Q: Find the turning point of \(y = x^2 - 8x + 12\). Give the y-coordinate.
   step0 field=pre answer=4 text='x = 8 ÷ 2 ='
   step1 field=pre answer=16 text='Substitute x = 4: square it, 4² ='
   step2 field=pre answer=-4 text='Now y = 16 − 8(4) + 12 = 16 − 32 + 12 ='
   step3 field=pre answer=4 text='Check via the roots: x² − 8x + 12 = (x − 2)(x − 6), roots 2 and 6; midpoint (2 + 6) ÷ 2 ='

gold[1] Q: The turning point of \(y = x^2 + bx + 10\) is at \(x = -3\). Find \(b\).
   step0 field=pre answer=-6 text='Set up −3 = −b ÷ 2 and multiply both sides by 2: −b = −3 × 2 ='
   step1 field=pre answer=6 text='So −b = −6, which means b ='
   step2 field=pre answer=-3 text='Check: with b = 6, x = −b ÷ (2a) = −6 ÷ 2 ='

gold[2] Q: For \(y = -x^2 + 6x - 5\), find the maximum y-value.
   step0 field=pre answer=3 text='Denominator 2 × (−1) = −2, so x = −6 ÷ (−2) ='
   step1 field=pre answer=9 text='Substitute x = 3: square first, 3² ='
   step2 field=pre answer=4 text='y = −(9) + 6(3) − 5 = −9 + 18 − 5 ='
   step3 field=pre answer=4 text='Check it is a maximum: a = −1 < 0, so the ∩ curve peaks here. Confirm 18 − 9 − 5 ='

gold[3] Q: A quadratic \(y = x^2 + bx + c\) has roots at \(x = 1\) and \(x = 5\). Find \(c\).
   step0 field=pre answer=-6 text='Expand (x − 1)(x − 5). The x terms: −5x − x ='
   step1 field=pre answer=5 text='The constant term is (−1) × (−5) ='
   step2 field=pre answer=0 text='Check x = 5 is a root: (5 − 1)(5 − 5) = 4 × 0 ='

silver[1] Q: Find the roots of \(y = x^2 - 5x + 6\).
   step0 field=pre answer=6 text='Two numbers multiply to +6 and add to −5: they are −2 and −3. Product: (−2) × (−3) ='
   step1 field=pre answer=2 text='So the factors are (x − 2)(x − 3) = 0, and each bracket can equal 0. From x − 2 = 0: x ='
   step2 field=pre answer=3 text='Second root, from (x − 3) = 0: x ='
   step3 field=pre answer=5 text='Check: the roots should add to −b = 5. 2 + 3 ='

silver[2] Q: For \(y = x^2 - 2x - 8\), what is the y-value of the turning point?
   step0 field=pre answer=1 text='x = 2 ÷ 2 ='
   step1 field=pre answer=1 text='Substitute x = 1: the square term 1² ='
   step2 field=pre answer=-9 text='Now y = 1 − 2(1) − 8 = 1 − 2 − 8 ='
   step3 field=pre answer=1 text='Check via the roots: (x − 4)(x + 2) gives roots 4 and −2; midpoint (4 + (−2)) ÷ 2 ='

### board=maths-ocr
bronze[0] Q: For \(y = x^2 + 3\), find \(y\) when \(x = 2\).
   step0 field=pre answer=4 text='Substitute x = 2. First the x² part: 2² ='
   step1 field=pre answer=7 text='Now add the constant: 4 + 3 ='
   step2 field=pre answer=7 text='Check the point (2, 7): 2² + 3 ='

gold[0] Q: \(y = 2x^2 - 8x + 6\). Find the x-coordinate of the turning point.
   step0 field=pre answer=4 text='Read a and b: a = 2, b = −8. Work out 2a = 2 × 2 ='
   step1 field=pre answer=8 text='Now −b = −(−8) ='
   step2 field=pre answer=2 text='Divide: 8 ÷ 4 ='
   step3 field=pre answer=2 text='Check: 2x² − 8x + 6 factors to 2(x − 1)(x − 3), roots 1 and 3; their midpoint is (1 + 3)/2'

gold[1] Q: \(y = 2x^2 - 8x + 6\). Find the y-coordinate of the turning point.
   step0 field=pre answer=2 text='Turning point x = −b/(2a) = 8/4 ='
   step1 field=pre answer=8 text='Substitute x = 2. The 2x² term: 2 × 2² = 2 × 4 ='
   step2 field=pre answer=-16 text='The −8x term: −8 × 2 ='
   step3 field=pre answer=-2 text='Add with +6: 8 + (−16) + 6 ='
   step4 field=pre answer=-2 text='Shape check: a = 2 > 0, so it opens up and this is the minimum, y ='

gold[2] Q: The roots of a quadratic are \(x = -1\) and \(x = 9\). Find the x-coordinate of the turnin
   step0 field=pre answer=8 text='The turning point is halfway between the roots. Add them: −1 + 9 ='
   step1 field=pre answer=4 text='Halve it: 8 ÷ 2 ='
   step2 field=pre answer=4 text='So the turning point x-coordinate is'
   step3 field=pre answer=4 text='Check the distances: 4 is 5 away from −1 and 5 away from 9. Equal, so the midpoint x is'

gold[3] Q: \(y = x^2 - 2x - 15\). Find the product of the roots.
   step0 field=pre answer=5 text='Factorise: x² − 2x − 15 = (x − 5)(x + 3). One root: x ='
   step1 field=pre answer=-3 text='The other root: x ='
   step2 field=pre answer=-15 text='Multiply them: 5 × (−3) ='
   step3 field=pre answer=-15 text='Check with the constant term: c/a = −15/1 ='

silver[1] Q: Find the turning point of \(y = x^2 - 4x + 1\). Give the x-coordinate.
   step0 field=pre answer=2 text='Read a and b: a = 1, b = −4. Work out 2a = 2 × 1 ='
   step1 field=pre answer=4 text='Now −b = −(−4) ='
   step2 field=pre answer=2 text='Divide: 4 ÷ 2 ='
   step3 field=pre answer=2 text='Check by symmetry: y at x = 1 is 1 − 4 + 1 = −2; y at x = 3 is 9 − 12 + 1 = −2. Equal, so '

silver[2] Q: Find the turning point of \(y = x^2 - 4x + 1\). Give the y-coordinate.
   step0 field=pre answer=2 text='Turning point x = −b/(2a) = 4/2 ='
   step1 field=pre answer=4 text='Substitute x = 2. The x² term: 2² ='
   step2 field=pre answer=-8 text='The −4x term: −4 × 2 ='
   step3 field=pre answer=-3 text='Add with the +1: 4 + (−8) + 1 ='
   step4 field=pre answer=-3 text='Shape check: a = 1 > 0, so this is the lowest point, y ='

### board=maths-eduqas
bronze[0] Q: For \(y = x^2 + 3x + 2\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text='Substitute x = 2 into each term.'
   step1 field=pre answer=4 text='The square: 2² ='
   step2 field=pre answer=6 text='The middle term: 3 × 2 ='
   step3 field=pre answer=12 text='Add the three parts: y = 4 + 6 + 2 ='
   step4 field=pre answer=12 text='Check by re-adding: 4 + 6 = 10, then 10 + 2 ='

gold[0] Q: For \(y = -x^2 + 6x - 5\), find the \(y\)-coordinate of the turning point.
   step0 field=say answer=None text='Turning point x = −b ÷ (2a), with a = −1 and b = 6.'
   step1 field=pre answer=-2 text='Bottom of the formula: 2a = 2 × (−1) ='
   step2 field=pre answer=3 text='x = −6 ÷ (−2) ='
   step3 field=say answer=None text='Now substitute x = 3 to find the y of the turning point.'
   step4 field=pre answer=-9 text='The square term: −(3²) ='
   step5 field=pre answer=18 text='The middle term: 6 × 3 ='
   step6 field=pre answer=4 text='So y = −9 + 18 − 5 ='
   step7 field=pre answer=4 text='Check: −9 + 18 = 9, then 9 − 5 ='

gold[1] Q: A quadratic \(y = x^2 - 8x + k\) touches the x-axis at exactly one point. Find \(k\).
   step0 field=say answer=None text='Touching at one point means the two roots are equal, so the discriminant b² − 4ac = 0. Her'
   step1 field=pre answer=64 text='b² = (−8)² ='
   step2 field=pre answer=4 text='The 4ac part is 4 × 1 × k = 4k. The number in front of k is'
   step3 field=pre answer=16 text='Set it to zero: 64 − 4k = 0, so 4k = 64 and k = 64 ÷ 4 ='
   step4 field=pre answer=4 text='Check: with k = 16, x² − 8x + 16 = (x − 4)². Its repeated root is x ='

gold[2] Q: The curve \(y = (x - 3)^2 - 4\) is in completed square form. What are the coordinates of t
   step0 field=say answer=None text='Completed square form \\(y = (x - a)^2 + b\\) has its turning point at (a, b). Compare (x − '
   step1 field=pre answer=3 text='The number inside the bracket gives a: x − 3 means a ='
   step2 field=pre answer=-4 text='The number outside gives b, the y of the turning point: (x − 3)² − 4 means b ='
   step3 field=pre answer=-4 text='Check by substituting x = 3: (3 − 3)² − 4 = 0 − 4 ='

gold[3] Q: For \(y = 3x^2 - 12x + 7\), find the \(x\)-coordinate of the turning point.
   step0 field=say answer=None text='Turning point x = −b ÷ (2a), with a = 3 and b = −12.'
   step1 field=pre answer=6 text='Bottom: 2a = 2 × 3 ='
   step2 field=pre answer=12 text='Top: −b = −(−12) ='
   step3 field=pre answer=2 text='x = 12 ÷ 6 ='
   step4 field=pre answer=-5 text='Check with the y: 3×4 − 12×2 + 7 = 12 − 24 + 7 ='

silver[1] Q: For \(y = x^2 - 4x - 5\), find the \(y\)-coordinate of the turning point.
   step0 field=say answer=None text='The roots are −1 and 5, so the turning point x = (−1 + 5) ÷ 2 = 2. Now substitute x = 2.'
   step1 field=pre answer=4 text='The square: 2² ='
   step2 field=pre answer=-8 text='The middle term: −4 × 2 ='
   step3 field=pre answer=-9 text='So y = 4 + (−8) + (−5) ='
   step4 field=pre answer=-9 text='Check: 4 − 8 = −4, then −4 − 5 ='

silver[2] Q: Which shape does the graph \(y = -3x^2 + 2x + 1\) have?
