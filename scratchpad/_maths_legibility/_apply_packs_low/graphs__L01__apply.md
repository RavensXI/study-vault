# apply-pack: graphs__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[3] | intro: 'Check the gradient means y rises 5 for each step in x. Go from x = 0 to  | fix: Break the arithmetic out of the sentence: 'Check it. At x = 0, y = -1. Now step to x = 1 and work out y:' then the box '5 x 1 - 1 ='.
- [low] gold[4] | intro: 'Check: multiply your y = 5x - 4 back by 2.' -> ask: '2 x 5 = [box=10]' | fix: Make the target explicit: 'Check: doubling y = 5x - 4 should rebuild 2y = 10x - 8. The x term is 2 x 5 =' so the student sees the 10 reproduces the 10x.
- [low] bronze[4] | So at x = 2: 2 + 3 × 2 = [box=8, NO label] | fix: Name the parts and cue BIDMAS, e.g. 'intercept 2 + gradient 3 × x-value 2 (do 3 × 2 first) ='.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[3] Q: A line has equation \(y = 7x - 4\). What is the gradient?
   step0 field=say answer=None text='In y = mx + c, the gradient m is the number multiplying x.'
   step1 field=pre answer=-4 text='The number on its own is the intercept c ='
   step2 field=pre answer=-4 text='At x = 0: y ='
   step3 field=pre answer=3 text='At x = 1: y = 7 × 1 + (-4) ='
   step4 field=pre answer=7 text='One step across means the run is 1, so the gradient is just the rise. From y = -4 up to y '

bronze[4] Q: For the line \(y = 3x + 1\), find \(y\) when \(x = 4\).
   step0 field=say answer=None text='Substitute the x-value into y = mx + c, doing the multiplication first.'
   step1 field=pre answer=12 text='The gradient part: 3 × 4 ='
   step2 field=pre answer=13 text='Now add the intercept: 12 + 1 ='
   step3 field=pre answer=13 text='Check the point (4, 13) fits: 3 × 4 + 1 ='

gold[4] Q: A line has equation \(3y = 9x - 12\). What is the gradient?
   step0 field=say answer=None text='Get the equation into y = mx + c first by dividing every term.'
   step1 field=pre answer=3 text='Divide the x term by 3: 9 ÷ 3 ='
   step2 field=pre answer=-4 text='Divide the constant by 3: (-12) ÷ 3 ='
   step3 field=pre answer=3 text='Now y = 3x + (-4). The gradient is the number in front of x:'
   step4 field=pre answer=3 text='Check: from x = 0 (y = -4) to x = 1 (y = -1), the rise is (-1) − (-4) ='

### board=maths-edexcel
bronze[3] Q: A line has equation \(y = 5x - 1\). What is the gradient?
   step0 field=pre answer=-1 text='Constant on its own:'
   step1 field=pre answer=5 text='Gradient m ='
   step2 field=pre answer=4 text='5 × 1 − 1 ='
   step3 field=pre answer=5 text='4 − (−1) ='

bronze[4] Q: For the line \(y = 2x + 3\), find \(y\) when \(x = 5\).
   step0 field=pre answer=10 text='2 × 5 ='
   step1 field=pre answer=13 text='10 + 3 ='
   step2 field=pre answer=13 text='2 × 5 + 3 ='

gold[4] Q: A line has equation \(2y = 10x - 8\). What is the gradient?
   step0 field=pre answer=5 text='10 ÷ 2 ='
   step1 field=pre answer=-4 text='−8 ÷ 2 ='
   step2 field=pre answer=5 text='Gradient ='
   step3 field=pre answer=10 text='2 × 5 ='

### board=maths-ocr
bronze[3] Q: A line has equation \(y = 4x - 3\). What is the gradient?
   step0 field=say answer=None text='In y = mx + c, the gradient m is the number multiplying x.'
   step1 field=pre answer=-3 text='The number on its own is the intercept c ='
   step2 field=pre answer=-3 text='At x = 0: y ='
   step3 field=pre answer=1 text='At x = 1: y = 4 × 1 + (−3) ='
   step4 field=pre answer=4 text='One step across means the run is 1, so the gradient is just the rise. From y = −3 up to y '

bronze[4] Q: Find the gradient of the line through \((2, 1)\) and \((6, 5)\).
   step0 field=say answer=None text='Gradient means rise over run: how far up for how far across. Start with the rise, the chan'
   step1 field=pre answer=4 text='Rise = 5 − 1 ='
   step2 field=pre answer=4 text='Run = 6 − 2 ='
   step3 field=pre answer=1 text='Gradient = rise ÷ run = 4 ÷ 4 ='
   step4 field=pre answer=4 text='Check: gradient × run = 1 × 4 ='

gold[4] Q: The midpoint of \((a, 3)\) and \((7, 11)\) is \((5, 7)\). Find \(a\).
   step0 field=say answer=None text='The midpoint x is the average of the two x-values. Work backwards to find a.'
   step1 field=pre answer=10 text='The midpoint x (5) is the average of a and 7. To undo the ÷ 2, double it: a + 7 = 2 × 5 ='
   step2 field=pre answer=3 text='That equals a + 7, so a = 10 − 7 ='
   step3 field=pre answer=5 text='Check the midpoint x: (3 + 7) ÷ 2 ='

### board=maths-eduqas
bronze[3] Q: For the line \(y = 2x + 1\), find \(y\) when \(x = 4\).
   step0 field=say answer=None text='Substitute \\(x = 4\\) into \\(y = 2x + 1\\).'
   step1 field=pre answer=8 text='First, 2 × 4 ='
   step2 field=pre answer=9 text='Then add 1: 8 + 1 ='
   step3 field=pre answer=1 text='Check at x = 0: 2 × 0 + 1 ='

bronze[4] Q: The graph shows a straight line. What is the value of \(y\) when \(x = 2\)?
   step0 field=say answer=None text='Read the graph. First find where the line crosses the y-axis.'
   step1 field=pre answer=2 text='The line crosses the y-axis at y ='
   step2 field=pre answer=3 text='For each step of 1 in x, the line climbs by'
   step3 field=pre answer=8 text='So at x = 2: 2 + 3 × 2 ='
   step4 field=pre answer=8 text='Read straight off the graph at x = 2: y ='

gold[4] Q: A line has equation \(2y = 10x - 6\). What is the gradient?
   step0 field=say answer=None text='Get it into the form \\(y = mx + c\\) by dividing every term by 2.'
   step1 field=pre answer=5 text='Divide the x-term: 10 ÷ 2 ='
   step2 field=pre answer=-3 text='Divide the constant: −6 ÷ 2 ='
   step3 field=pre answer=5 text='So y = 5x − 3. The gradient is'
   step4 field=pre answer=-3 text='Check the intercept at x = 0: y ='
