# apply-pack: algebra__L10.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] | Move the 6 across and tidy so x² is positive; the constant term becomes [box=6,  | fix: Reorder so this ask comes BEFORE the 'So x² - 5x + 6 = 0' reveal, or reword to derive from the earlier line: 'Starting from 5x - x² = 6, move every term to the 
- [low] gold[4] | "Bring −5 and −7 together for the constant: [box=-12, NO label]" | fix: Add the intermediate move first, e.g. "Move +7 to the left, where it becomes −7; now combine −5 and −7 for the constant: ___".
- [low] bronze[0] (pattern repeats in every problem) | There is no constant, so factor out x. First root, x = [box=0, NO label] / Secon | fix: Add one bridging line at the first factorisation (bronze[0]) before the root boxes, e.g. 'A product is zero only when a bracket is zero, so set each bracket to 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: Solve \(y = x\) and \(y = x^2\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x = x^2\\). Bring every term to '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=0 text='and the constant becomes'
   step3 field=pre answer=0 text='First root, x ='
   step4 field=pre answer=1 text='Second root, x ='
   step5 field=pre answer=0 text='At x = 0: y ='
   step6 field=pre answer=1 text='At x = 1: y ='
   step7 field=pre answer=0 text='Check in the curve: 0² ='

gold[3] Q: Solve \(x + y = 5\) and \(xy = 6\). Give the two x-values.
   step0 field=say answer=None text='Make y the subject of the simple equation: \\(x + y = 5\\) becomes \\(y = 5 - x\\). Put this i'
   step1 field=pre answer=-1 text='Multiply out x(5 − x): the x-term is 5x and the x² term is'
   step2 field=pre answer=6 text='Move the 6 across and tidy so x² is positive; the constant term becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=3 text='Second root, x ='
   step5 field=pre answer=3 text='At x = 2: y = 5 − 2 ='
   step6 field=pre answer=2 text='At x = 3: y = 5 − 3 ='
   step7 field=pre answer=6 text='Check the product xy for (2, 3): 2 × 3 ='

gold[4] Q: The line \(y = kx + 2\) is a tangent to \(y = x^2 + 3\), so it touches the curve at exactl
   step0 field=say answer=None text='Where the line meets the curve, \\(kx + 2 = x^2 + 3\\). Bring all to one side: \\(x^2 - kx + '
   step1 field=pre answer=4 text='For this quadratic, a = 1, c = 1, and b = −k, so b² = k² and 4ac ='
   step2 field=pre answer=4 text='Set k² − 4 = 0, so k² ='
   step3 field=pre answer=2 text='The positive value of k is'
   step4 field=pre answer=0 text='Check: with k = 2 the quadratic is x² − 2x + 1; its discriminant 2² − 4 ='

### board=maths-edexcel
bronze[0] Q: Solve \(y = x + 3\) and \(y = x^2 + 1\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x + 3 = x^2 + 1\\). Bring every '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=-2 text='and the constant becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=-1 text='From x + 1 = 0, the second root is x ='
   step5 field=pre answer=5 text='At x = 2: y ='
   step6 field=pre answer=2 text='At x = −1: y ='
   step7 field=pre answer=5 text='Work out 2² + 1 ='

gold[3] Q: xyOx²+y²=20y=x+2??Diagram not drawn accuratelySolve \(y = x + 2\) and \(x^2 + y^2 = 20\). 
   step0 field=pre answer=4 text='The middle term, 2 × x × 2, is'
   step1 field=pre answer=2 text='Collect the two x² terms: 1 + 1 ='
   step2 field=pre answer=-16 text='The constant, 4 − 20, becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=-4 text='Second root, x ='
   step5 field=pre answer=4 text='At x = 2: y ='
   step6 field=pre answer=-2 text='At x = −4: y ='
   step7 field=pre answer=20 text='Check (2, 4) in the circle: 2² + 4² ='

gold[4] Q: Solve \(x + y = 5\) and \(x^2 - y = 7\). Give the two x-values.
   step0 field=pre answer=-12 text='Bring −5 and −7 together for the constant:'
   step1 field=pre answer=3 text='First root, x ='
   step2 field=pre answer=-4 text='Second root, x ='
   step3 field=pre answer=2 text='At x = 3: y ='
   step4 field=pre answer=9 text='At x = −4: y ='
   step5 field=pre answer=7 text='Put x = 3, y = 2 into x² − y: 3² − 2 ='

### board=maths-ocr
bronze[0] Q: Solve \(y = x + 1\) and \(y = x^2 - 2x - 3\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x + 1 = x^2 - 2x - 3\\). Bring e'
   step1 field=pre answer=-3 text='The x-term becomes'
   step2 field=pre answer=-4 text='and the constant becomes'
   step3 field=pre answer=4 text='First root, x ='
   step4 field=pre answer=-1 text='From x + 1 = 0, the second root is x ='
   step5 field=pre answer=5 text='At x = 4: y ='
   step6 field=pre answer=0 text='At x = −1: y ='
   step7 field=pre answer=5 text='Work out 4² − 2×4 − 3 ='

gold[3] Q: Solve \(2x + y = 5\) and \(xy = 2\). Give the two x-values.
   step0 field=pre answer=2 text='Expanding x(5 − 2x) gives 5x − 2x². Bring 2 across so 2x² is positive: 2x² − 5x +'
   step1 field=pre answer=2 text='First root, x ='
   step2 field=pre answer=0.5 text='From 2x − 1 = 0, the second root is x ='
   step3 field=pre answer=1 text='At x = 2: y ='
   step4 field=pre answer=4 text='At x = 0.5: y ='
   step5 field=pre answer=2 text='Check by multiplying: 2 × 1 ='

gold[4] Q: Solve \(y = 5 - 2x\) and \(x^2 + xy = 6\). Give the two x-values.
   step0 field=pre answer=-1 text='Expanding x(5 − 2x) gives 5x − 2x². Add the x²: 1 − 2 ='
   step1 field=pre answer=-5 text='Multiplying −x² + 5x = 6 by −1, the x-term becomes'
   step2 field=pre answer=6 text='and moving the constant across, the equation is x² − 5x +'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=3 text='Second root, x ='
   step5 field=pre answer=1 text='At x = 2: y ='
   step6 field=pre answer=-1 text='At x = 3: y ='
   step7 field=pre answer=6 text='Check (2, 1): x² + xy = 4 + 2×1 ='

### board=maths-eduqas
bronze[0] Q: Solve \(y = x\) and \(y = x^2\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x = x^2\\). Bring every term to '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=0 text='There is no constant, so factor out x. First root, x ='
   step3 field=pre answer=1 text='Second root, x ='
   step4 field=pre answer=0 text='At x = 0: y ='
   step5 field=pre answer=1 text='At x = 1: y ='
   step6 field=pre answer=1 text='Check: 1² ='

gold[3] Q: Solve \(y = 3 - x\) and \(xy = 2\). Give the two x-values.
   step0 field=pre answer=-3 text='Make x² positive and tidy; the x-term becomes'
   step1 field=pre answer=2 text='and the constant becomes'
   step2 field=pre answer=1 text='First root, x ='
   step3 field=pre answer=2 text='Second root, x ='
   step4 field=pre answer=2 text='At x = 1: y ='
   step5 field=pre answer=1 text='At x = 2: y ='
   step6 field=pre answer=2 text='Check x = 1, y = 2 in the product: 1 × 2 ='

gold[4] Q: Solve \(x + y = 7\) and \(xy = 10\). Give the two x-values.
   step0 field=pre answer=-7 text='Make x² positive and tidy; the x-term becomes'
   step1 field=pre answer=10 text='and the constant becomes'
   step2 field=pre answer=2 text='First root, x ='
   step3 field=pre answer=5 text='Second root, x ='
   step4 field=pre answer=5 text='At x = 2: y ='
   step5 field=pre answer=2 text='At x = 5: y ='
   step6 field=pre answer=10 text='Check x = 2, y = 5 in the product: 2 × 5 ='
