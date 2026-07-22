# apply-pack: graphs__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] gold[3] | ACBxy0Show that \(A(1, 3)\), \(B(5, 7)\) and \(C(3, 5)\) are collinear. What is  | fix: Delete the 'ACBxy0' prefix so the stem reads: 'Show that A(1, 3), B(5, 7) and C(3, 5) are collinear. What is the gradient of AB?'
- [high] silver[5] | 2(1, 5)PQLine P has equation \(y = -3x + 2\). Line Q is parallel to P and passes | fix: Strip the artifact so the stem starts cleanly: 'Line P has equation y = -3x + 2. Line Q is parallel to P and passes through (1, 5). What is the y-intercept of Q
- [high] gold[4] | A(1, 2)B(5, 10)MThe midpoint of \(A(1, 2)\) and \(B(5, 10)\) lies on the line \( | fix: Remove the artifact so the stem begins: 'The midpoint of A(1, 2) and B(5, 10) lies on the line y = mx + c with gradient -1. Find c.'
- [high] gold[4] | Q: (2, 0)(0, −6)xy0A line passes through (2, 0) and (0, -6). Find the gradient. | fix: Delete the leading '(2, 0)(0, −6)xy0' so the question reads exactly: 'A line passes through (2, 0) and (0, -6). Find the gradient.'
- [medium] gold[0] | Q: (−2, 7)(4, −5)xy0Find the equation of the line through (−2, 7) and (4, −5). W | fix: Delete the leading '(−2, 7)(4, −5)xy0' so the question reads simply: 'Find the equation of the line through (−2, 7) and (4, −5). What is c?' (Any coordinate/axi

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: Find the equation of the line through \((-2, 3)\) and \((4, 15)\). Give the value of \(c\)
   step0 field=pre answer=12 text='change in y = 15 - 3 ='
   step1 field=pre answer=6 text='change in x = 4 - (-2) ='
   step2 field=pre answer=2 text='m = 12 ÷ 6 ='
   step3 field=pre answer=7 text='c = 3 - (-4) ='
   step4 field=pre answer=15 text='check with (4, 15): 2×4 + 7 ='

gold[3] Q: ACBxy0Show that \(A(1, 3)\), \(B(5, 7)\) and \(C(3, 5)\) are collinear. What is the gradie
   step0 field=pre answer=4 text='change in y = 7 - 3 ='
   step1 field=pre answer=4 text='change in x = 5 - 1 ='
   step2 field=pre answer=1 text='gradient AB = 4 ÷ 4 ='
   step3 field=pre answer=1 text='check collinear: gradient AC = (5 - 3) ÷ (3 - 1) = 2 ÷ 2 ='

gold[4] Q: A line through \((p, 10)\) and \((5, 4)\) has gradient \(-3\). Find \(p\).
   step0 field=pre answer=-6 text='the change in y = 4 - 10 ='
   step1 field=pre answer=2 text='5 - p = -6 ÷ (-3) ='
   step2 field=pre answer=3 text='5 - p = 2, so p = 5 - 2 ='
   step3 field=pre answer=-3 text='check: (4 - 10) ÷ (5 - 3) = -6 ÷ 2 ='

silver[5] Q: The line \(4y = 8x + 12\). What is the gradient?
   step0 field=pre answer=2 text='8x ÷ 4 gives the x term coefficient: 8 ÷ 4 ='
   step1 field=pre answer=3 text='12 ÷ 4 ='
   step2 field=pre answer=2 text='the number in front of x is'
   step3 field=pre answer=2 text='it is 2, not the original 8. The gradient is'

### board=maths-edexcel
gold[0] Q: Find the equation of the line through \((-1, 5)\) and \((3, -3)\). What is \(c\)?
   step0 field=say answer=None text='Find the gradient first from \\((-1, 5)\\) and \\((3, -3)\\). Watch the double negatives.'
   step1 field=pre answer=-8 text='top: −3 − 5 ='
   step2 field=pre answer=4 text='bottom: 3 − (−1) ='
   step3 field=pre answer=-2 text='m = −8 ÷ 4 ='
   step4 field=say answer=None text='Substitute \\((-1, 5)\\) into \\(y = -2x + c\\):'
   step5 field=pre answer=2 text='−2 × (−1) ='
   step6 field=pre answer=3 text='5 − 2 = c, so c ='
   step7 field=pre answer=-3 text='Check (3, −3): −2 × 3 + 3 ='

gold[3] Q: Find the equation of the line perpendicular to \(y = -\frac{1}{3}x + 2\) that passes throu
   step0 field=say answer=None text='The given gradient is \\(-\\frac{1}{3}\\). The perpendicular gradient is the negative recipro'
   step1 field=pre answer=3 text='perpendicular m ='
   step2 field=say answer=None text='So the line is \\(y = 3x + c\\). Substitute \\((3, 7)\\):'
   step3 field=pre answer=9 text='3 × 3 ='
   step4 field=say answer=None text='So 7 = 9 + c.'
   step5 field=pre answer=-2 text='7 − 9 = c, so c ='
   step6 field=pre answer=7 text='Check (3, 7): 3 × 3 + (−2) ='

gold[4] Q: A(1, 2)B(5, 10)MThe midpoint of \(A(1, 2)\) and \(B(5, 10)\) lies on the line \(y = mx + c
   step0 field=say answer=None text="First find the midpoint of \\(A(1, 2)\\) and \\(B(5, 10)\\): average the x's and average the y"
   step1 field=pre answer=3 text='midpoint x: (1 + 5) ÷ 2 ='
   step2 field=pre answer=6 text='midpoint y: (2 + 10) ÷ 2 ='
   step3 field=say answer=None text='So the midpoint is \\((3, 6)\\). The gradient is given as −1, so \\(y = -x + c\\). Substitute '
   step4 field=pre answer=-3 text='−1 × 3 ='
   step5 field=pre answer=9 text='6 − (−3) = c, so c ='
   step6 field=pre answer=6 text='Check: at x = 3, −1 × 3 + 9 ='

silver[5] Q: 2(1, 5)PQLine P has equation \(y = -3x + 2\). Line Q is parallel to P and passes through \
   step0 field=say answer=None text="Parallel lines share a gradient. Read P's gradient from \\(y = -3x + 2\\):"
   step1 field=pre answer=-3 text='m ='
   step2 field=say answer=None text='Q has the same gradient, so \\(y = -3x + c\\). Substitute \\((1, 5)\\):'
   step3 field=pre answer=-3 text='−3 × 1 ='
   step4 field=say answer=None text='So 5 = −3 + c.'
   step5 field=pre answer=8 text='5 − (−3) = c, so c ='
   step6 field=pre answer=5 text='Check (1, 5): −3 × 1 + 8 ='

### board=maths-ocr
gold[0] Q: Find the equation of the line through \((-1, 8)\) and \((3, -4)\). What is the value of \(
   step0 field=pre answer=-12 text='change in y = −4 − 8 ='
   step1 field=pre answer=4 text='change in x = 3 − (−1) ='
   step2 field=pre answer=-3 text='m = −12 ÷ 4 ='
   step3 field=pre answer=5 text='c = 8 − 3 ='
   step4 field=pre answer=-4 text='check with (3, −4): −3×3 + 5 ='

gold[3] Q: Show the lines \(y = 2x + 3\) and \(y = 2x - 5\) are parallel. What is their common gradie
   step0 field=pre answer=2 text='the gradient of \\(y = 2x + 3\\) is'
   step1 field=pre answer=2 text='the gradient of \\(y = 2x - 5\\) is'
   step2 field=pre answer=2 text='both gradients are equal, so the lines are parallel. The common gradient is'

gold[4] Q: (2, 0)(0, −6)xy0A line passes through \((2, 0)\) and \((0, -6)\). Find the gradient.
   step0 field=pre answer=-6 text='change in y = −6 − 0 ='
   step1 field=pre answer=-2 text='change in x = 0 − 2 ='
   step2 field=pre answer=3 text='m = −6 ÷ (−2) ='
   step3 field=pre answer=0 text='check: from (0, −6), up 3 per 1 across, at x = 2 gives y = −6 + 3×2 ='

silver[5] Q: A line has equation \(4x + 2y = 10\). What is the gradient?
   step0 field=pre answer=-4 text='the x coefficient is now'
   step1 field=pre answer=-2 text='−4 ÷ 2 gives the gradient:'
   step2 field=pre answer=5 text='so \\(y = -2x + 5\\). Check the y-intercept at x = 0: y ='

### board=maths-eduqas
gold[0] Q: (−2, 7)(4, −5)xy0Find the equation of the line through \((-2, 7)\) and \((4, -5)\). What i
   step0 field=pre answer=-12 text='change in y = −5 − 7 ='
   step1 field=pre answer=6 text='change in x = 4 − (−2) ='
   step2 field=pre answer=-2 text='m = −12 ÷ 6 ='
   step3 field=pre answer=3 text='c = 7 − 4 ='
   step4 field=pre answer=-5 text='check with (4, −5): −2×4 + 3 ='

gold[3] Q: A line passes through \((5, 2)\) and is perpendicular to \(y = -\frac{1}{2}x + 6\). Find t
   step0 field=pre answer=-2 text='flip −½ (turn it upside down) to get'
   step1 field=pre answer=2 text='the perpendicular gradient is −(−2) ='
   step2 field=pre answer=-1 text='check: perpendicular gradients multiply to −1, so −½ × 2 ='

gold[4] Q: The midpoint of \(A(2, 3)\) and \(B(6, 9)\) lies on the line \(y = mx + c\) with gradient 
   step0 field=pre answer=4 text='the x of the midpoint: (2 + 6) ÷ 2 ='
   step1 field=pre answer=6 text='the y of the midpoint: (3 + 9) ÷ 2 ='
   step2 field=pre answer=-8 text='m×x = −2×4 ='
   step3 field=pre answer=14 text='c = 6 + 8 ='
   step4 field=pre answer=6 text='check: −2×4 + 14 ='

silver[5] Q: Line P has equation \(y = -2x + 9\). Line Q is parallel to P and passes through \((3, 1)\)
   step0 field=pre answer=-2 text='the gradient of Q is m ='
   step1 field=pre answer=-6 text='the x part: m×x = −2×3 ='
   step2 field=pre answer=7 text='c = 1 + 6 ='
   step3 field=pre answer=1 text='check: −2×3 + 7 ='
