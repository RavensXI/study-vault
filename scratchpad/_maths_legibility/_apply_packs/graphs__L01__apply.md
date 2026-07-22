# apply-pack: graphs__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[1] | intro: 'The y-intercept is the y-value where the line crosses the vertical axis, | fix: Cut the gradient detour. Read the intercept straight off: 'The y-intercept is where the line crosses the vertical axis (at x = 0). Read up from x = 0 - the line
- [medium] bronze[3] | The gradient is the rise for one step across: 1 - (-3) = [box=4, NO label] | fix: Either answer directly from the intro's rule ('The number multiplying x is the gradient m = [box=4]'), or add a step that states run = 1 and defines gradient = 
- [medium] bronze[6] | From x = 1 (y = 3), two more steps to x = 3: 3 + 2 x 2 = [box=7, NO label] | fix: Remove the order-of-operations trap and spell it out: 'Each step adds 2, and there are two steps: 3 + 2 + 2 = [box=7]' (or at minimum bracket it as 3 + (2 x 2))
- [medium] gold[4] | The midpoint x is 5, and averaging halves, so double it back: 2 x 5 = [box=10, N | fix: Rephrase concretely so the reasoning is visible: 'The midpoint x (5) is the average of a and 7, so a + 7 must equal 2 x 5 = [box=10]'.
- [medium] gold[2] | Subtract 6 from both sides: −2 − 6 = [box=-8, NO label] | fix: Insert an intermediate step showing the substitution, e.g. add 'Substituting gives −2 = 4m + 6' before the 'Subtract 6 from both sides' line.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[3] Q: A line has equation \(y = 7x - 4\). What is the gradient?
   step0 field=say answer=None text='In y = mx + c, the gradient m is the number multiplying x.'
   step1 field=pre answer=-4 text='The number on its own is the intercept c ='
   step2 field=pre answer=-4 text='At x = 0: y ='
   step3 field=pre answer=3 text='At x = 1: y = 7 × 1 + (-4) ='
   step4 field=pre answer=7 text='The gradient is the rise for one step across: 3 − (-4) ='

bronze[6] Q: What is the gradient of the line \(y = -2x + 9\)?
   step0 field=say answer=None text='In y = mx + c, the gradient m is the number multiplying x.'
   step1 field=pre answer=9 text='The number on its own is the intercept c ='
   step2 field=pre answer=9 text='At x = 0: y ='
   step3 field=pre answer=7 text='At x = 1: y = (-2) × 1 + 9 ='
   step4 field=pre answer=-2 text='The gradient is the rise for one step across: 7 − 9 ='

gold[2] Q: The line \(y = mx + 7\) passes through \((2, 15)\). Find \(m\).
   step0 field=say answer=None text='Put the point into y = mx + c and peel away the known parts.'
   step1 field=pre answer=8 text='Take the intercept off both sides: 15 − 7 ='
   step2 field=pre answer=4 text='So 2 × m = 8. Divide by 2: m ='
   step3 field=pre answer=15 text='Check: 4 × 2 + 7 ='

gold[4] Q: A line has equation \(3y = 9x - 12\). What is the gradient?
   step0 field=say answer=None text='Get the equation into y = mx + c first by dividing every term.'
   step1 field=pre answer=3 text='Divide the x term by 3: 9 ÷ 3 ='
   step2 field=pre answer=-4 text='Divide the constant by 3: (-12) ÷ 3 ='
   step3 field=pre answer=3 text='Now y = 3x + (-4). The gradient is the number in front of x:'
   step4 field=pre answer=3 text='Check: from x = 0 (y = -4) to x = 1 (y = -1), the rise is (-1) − (-4) ='

silver[1] Q: The graph shows a straight line. What is the y-intercept?
   step0 field=say answer=None text='The y-intercept is where the line cuts the vertical axis, at x = 0.'
   step1 field=pre answer=5 text='Read a point at x = 1: y ='
   step2 field=pre answer=9 text='Read another at x = 2: y ='
   step3 field=pre answer=4 text='Gradient = (9 − 5) ÷ (2 − 1) ='
   step4 field=pre answer=1 text='Step left from (1, 5) to x = 0: y = 5 − 4 ='
   step5 field=pre answer=1 text='So the line crosses the y-axis at y ='

### board=maths-edexcel
bronze[3] Q: A line has equation \(y = 5x - 1\). What is the gradient?
   step0 field=pre answer=-1 text='Constant on its own:'
   step1 field=pre answer=5 text='Gradient m ='
   step2 field=pre answer=4 text='5 × 1 − 1 ='
   step3 field=pre answer=5 text='4 − (−1) ='

bronze[6] Q: What is the gradient of the line \(y = -3x + 7\)?
   step0 field=pre answer=7 text='Constant on its own:'
   step1 field=pre answer=-3 text='Gradient m ='
   step2 field=pre answer=4 text='−3 × 1 + 7 ='
   step3 field=pre answer=-3 text='4 − 7 ='

gold[2] Q: The line \(y = mx + 5\) passes through \((4, 21)\). Find \(m\).
   step0 field=pre answer=16 text='21 − 5 ='
   step1 field=pre answer=4 text='16 ÷ 4 ='
   step2 field=pre answer=21 text='4 × 4 + 5 ='

gold[4] Q: A line has equation \(2y = 10x - 8\). What is the gradient?
   step0 field=pre answer=5 text='10 ÷ 2 ='
   step1 field=pre answer=-4 text='−8 ÷ 2 ='
   step2 field=pre answer=5 text='Gradient ='
   step3 field=pre answer=10 text='2 × 5 ='

silver[1] Q: The graph shows a straight line. What is the y-intercept of this line?
   step0 field=pre answer=4 text='Rise: 2 − (−2) ='
   step1 field=pre answer=2 text='Run: 2 − 0 ='
   step2 field=pre answer=-2 text='c = 2 − 4 ='
   step3 field=pre answer=-2 text='Read the graph at x = 0: y ='

### board=maths-ocr
bronze[3] Q: A line has equation \(y = 4x - 3\). What is the gradient?
   step0 field=say answer=None text='In y = mx + c, the gradient m is the number multiplying x.'
   step1 field=pre answer=-3 text='The number on its own is the intercept c ='
   step2 field=pre answer=-3 text='At x = 0: y ='
   step3 field=pre answer=1 text='At x = 1: y = 4 × 1 + (−3) ='
   step4 field=pre answer=4 text='The gradient is the rise for one step across: 1 − (−3) ='

bronze[6] Q: The graph shows a straight line. What is the value of \(y\) when \(x = 3\)?
   step0 field=say answer=None text='Read the height of the line at the x-value the question asks for.'
   step1 field=pre answer=1 text='At x = 0 the line is at y ='
   step2 field=pre answer=3 text='At x = 1 the line is at y ='
   step3 field=pre answer=2 text='Each step across adds (3 − 1) ='
   step4 field=pre answer=7 text='From x = 1 (y = 3), two more steps to x = 3: 3 + 2 × 2 ='
   step5 field=pre answer=7 text='Check on the graph at x = 3: y ='

gold[2] Q: Line A: \(y = 2x + 1\). Line B passes through \((0, 7)\) and \((2, 3)\). Are the lines par
   step0 field=say answer=None text='Parallel lines have equal gradients. Find each gradient and compare.'
   step1 field=pre answer=2 text='Line A is y = 2x + 1, so its gradient is'
   step2 field=pre answer=-4 text='Line B rise = 3 − 7 ='
   step3 field=pre answer=2 text='Line B run = 2 − 0 ='
   step4 field=pre answer=-2 text='Line B gradient = (−4) ÷ 2 ='
   step5 field=pre answer=0 text='The gradients are 2 and −2. Equal? Enter 1 for Yes, 0 for No:'

gold[4] Q: The midpoint of \((a, 3)\) and \((7, 11)\) is \((5, 7)\). Find \(a\).
   step0 field=say answer=None text='The midpoint x is the average of the two x-values. Work backwards to find a.'
   step1 field=pre answer=10 text='The midpoint x is 5, and averaging halves, so double it back: 2 × 5 ='
   step2 field=pre answer=3 text='That equals a + 7, so a = 10 − 7 ='
   step3 field=pre answer=5 text='Check the midpoint x: (3 + 7) ÷ 2 ='

silver[1] Q: The line \(y = mx + 3\) passes through \((2, 11)\). Find \(m\).
   step0 field=say answer=None text='Put the point into y = mx + c and peel away the known parts.'
   step1 field=pre answer=8 text='Take the intercept off both sides: 11 − 3 ='
   step2 field=pre answer=4 text='So 2 × m = 8. Divide by 2: m ='
   step3 field=pre answer=11 text='Check: 4 × 2 + 3 ='

### board=maths-eduqas
bronze[3] Q: For the line \(y = 2x + 1\), find \(y\) when \(x = 4\).
   step0 field=say answer=None text='Substitute \\(x = 4\\) into \\(y = 2x + 1\\).'
   step1 field=pre answer=8 text='First, 2 × 4 ='
   step2 field=pre answer=9 text='Then add 1: 8 + 1 ='
   step3 field=pre answer=1 text='Check at x = 0: 2 × 0 + 1 ='

bronze[6] Q: What is the gradient of the line \(y = -2x + 9\)?
   step0 field=say answer=None text='The gradient is the number multiplying x, including its sign.'
   step1 field=pre answer=-2 text='The number multiplying x ='
   step2 field=pre answer=9 text='The y-intercept c ='
   step3 field=pre answer=7 text='Check the sign at x = 1: −2 × 1 + 9 ='

gold[2] Q: The line \(y = mx + 6\) passes through \((4, -2)\). Find \(m\).
   step0 field=say answer=None text='Substitute the point (4, −2) into \\(y = mx + 6\\).'
   step1 field=pre answer=-8 text='Subtract 6 from both sides: −2 − 6 ='
   step2 field=pre answer=-2 text='So 4m = −8. Divide by 4: −8 ÷ 4 ='
   step3 field=pre answer=-2 text='Check: −2 × 4 + 6 ='

gold[4] Q: A line has equation \(2y = 10x - 6\). What is the gradient?
   step0 field=say answer=None text='Get it into the form \\(y = mx + c\\) by dividing every term by 2.'
   step1 field=pre answer=5 text='Divide the x-term: 10 ÷ 2 ='
   step2 field=pre answer=-3 text='Divide the constant: −6 ÷ 2 ='
   step3 field=pre answer=5 text='So y = 5x − 3. The gradient is'
   step4 field=pre answer=-3 text='Check the intercept at x = 0: y ='

silver[1] Q: A line has equation \(y = -3x + 7\). Find \(y\) when \(x = 4\).
   step0 field=say answer=None text='Substitute \\(x = 4\\) into \\(y = -3x + 7\\).'
   step1 field=pre answer=-12 text='First, −3 × 4 ='
   step2 field=pre answer=-5 text='Then add 7: −12 + 7 ='
   step3 field=pre answer=7 text='Check at x = 0: −3 × 0 + 7 ='
