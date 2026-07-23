# apply-pack: algebra__L12.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[0] | From 2x + 1 = 0, first 2x = [box=-1] | fix: Reword to make the intermediate step explicit, e.g. 'Rearrange 2x + 1 = 0 to get 2x = ___'.
- [low] gold[1] | From 3x - 2 = 0, first 3x = [box=2] | fix: Reword, e.g. 'Rearrange 3x - 2 = 0 to get 3x = ___'.
- [low] gold[3] | intro: "Overlap -3 ≤ x ≤ 3 with x > -1: since x must beat -1, the overlap is -1  | fix: Replace "since x must beat -1" with "since x must be greater than -1".

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: Solve \(6 - x - x^2 > 0\)

gold[1] Q: Find the set of values of \(x\) for which \(x^2 - 2x > 3\)

gold[3] Q: Solve \(x^2 + 2x - 8 \le 0\) and \(x > 0\) simultaneously.

### board=maths-edexcel
gold[0] Q: Solve \(2x^2 - 5x - 3 > 0\). Give the larger critical value.
   step0 field=say answer=None text='With a 2 in front of \\(x^2\\), split the middle term. Two numbers multiply to \\((2)(-3) = -'
   step1 field=pre answer=3 text='From x - 3 = 0: x ='
   step2 field=pre answer=-1 text='From 2x + 1 = 0, first 2x ='
   step3 field=say answer=None text='So the other root is \\(x = -1 \\div 2 = -0.5\\). The roots are -0.5 and 3. For \\(> 0\\) the U'
   step4 field=pre answer=3 text='The larger critical value is'
   step5 field=pre answer=9 text='Check x = 4 (outside, to the right): 2(4²) - 5(4) - 3 ='

gold[1] Q: Solve \(3x^2 + x - 2 \leq 0\). Give the upper critical value as a fraction.
   step0 field=say answer=None text='Split the middle term. Two numbers multiply to \\((3)(-2) = -6\\) and add to +1: they are +3'
   step1 field=pre answer=-1 text='From x + 1 = 0: x ='
   step2 field=pre answer=2 text='From 3x - 2 = 0, first 3x ='
   step3 field=say answer=None text='So the second root is \\(x = 2 \\div 3 = \\tfrac{2}{3}\\). The roots are -1 and \\(\\tfrac{2}{3}'
   step4 field=pre answer=2 text='Enter the numerator of the upper value (two thirds):'
   step5 field=pre answer=3 text='Enter its denominator:'
   step6 field=pre answer=-2 text='Check x = 0 (between the roots): 3(0²) + 0 - 2 ='

gold[3] Q: Solve \(x^2 + 2x + 1 > 0\). Describe the solution.

### board=maths-ocr
gold[0] Q: Solve \(3x^2 + 2x - 1 > 0\). What is the range?

gold[1] Q: Find the values of \(k\) for which \(x^2 + kx + 4 = 0\) has no real roots. What is the ran

gold[3] Q: How many integers satisfy both \(x^2 - 9 \leq 0\) AND \(x + 1 > 0\)?
   step0 field=say answer=None text='Solve each part. First \\(x^2 - 9 \\leq 0\\) factorises to \\((x-3)(x+3) \\leq 0\\), giving betw'
   step1 field=pre answer=-1 text='The second condition x + 1 > 0 rearranges to x >'
   step2 field=say answer=None text='Overlap \\(-3 \\leq x \\leq 3\\) with \\(x > -1\\): since \\(x\\) must beat \\(-1\\), the overlap is'
   step3 field=pre answer=4 text='The whole numbers with -1 < x ≤ 3 are 0, 1, 2, 3. How many?'
   step4 field=pre answer=0 text='Check x = 3 in the first part: 3² - 9 ='

### board=maths-eduqas
gold[0] Q: Solve \(2x^2 - 7x + 3 < 0\). Which is correct?

gold[1] Q: Solve \(3x^2 + 5x - 2 \geq 0\). Which is correct?

gold[3] Q: -2-1012345Sketch, not drawn to scale Find the set of values of \(x\) for which \(x^2 < 3x 
   step0 field=say answer=None text='Rearrange \\(x^2 < 3x + 4\\) to \\(x^2 - 3x - 4 < 0\\). Factorise: two numbers multiply to \\(-'
   step1 field=pre answer=4 text='From x - 4 = 0: x ='
   step2 field=pre answer=-1 text='From x + 1 = 0: x ='
   step3 field=say answer=None text='For \\(< 0\\) the solution is between the roots: \\(-1 < x < 4\\). We want only the POSITIVE w'
   step4 field=pre answer=3 text='The positive integers are 1, 2, 3. How many?'
   step5 field=pre answer=0 text='Check the upper root x = 4: 4² - 3(4) - 4 ='
