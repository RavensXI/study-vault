# apply-pack: algebra__L12.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[4] | -3-2-10123456Sketch, not to scale Find the integer values of x satisfying x^2 -  | fix: Strip the flattened axis digits from the question text so it reads cleanly, e.g. '(Sketch, not to scale.) Find the integer values of x satisfying x^2 - 3x - 10 
- [medium] gold[4] | 0123456Sketch, not to scale Solve x^2 - 6x + 5 < 0. How many integer values of x | fix: Remove the flattened axis digits so it reads cleanly, e.g. '(Sketch, not to scale.) Solve x^2 - 6x + 5 < 0. How many integer values of x satisfy this?'
- [high] silver[3] | For \(> 0\) it is above the x-axis OUTSIDE the roots, so \(x 1\). | fix: Rewrite the region as: 'so x 1.'
- [high] gold[0] | For \(> 0\) the U-shape is above the axis OUTSIDE the roots: \(x 3\). | fix: Rewrite as: 'x 3.'
- [medium] bronze[4] | intro: "...the critical values are ±5. So x^2 > 25 means x 5." | fix: Rewrite as: "So \(x^2 > 25\) means \(x 5\)."
- [high] silver[4] | The point (0, 0) satisfies which inequality: \(y x + 3\)? | fix: Restore the dropped sign, e.g. rewrite the stem as 'which inequality: \(y operator).
- [medium] gold[2] | 012345Sketch, not drawn to scale How many integers satisfy \(x^2 - 5x + 4 \leq 0 | fix: Detach the number-line/caption from the prose. Show the number line as a labelled image with 'Sketch — not drawn to scale' as its caption, and start the questio
- [medium] gold[3] | -2-1012345Sketch, not drawn to scale Find the set of values of \(x\) for which \ | fix: Separate the number-line/caption from the question text. Present the number line as a labelled diagram with 'Sketch — not drawn to scale' beneath it, and begin 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[4] Q: Solve \((x+3)(x-2) > 0\)

gold[0] Q: Solve \(6 - x - x^2 > 0\)

gold[2] Q: Find the range of values of \(k\) for which \(x^2 + kx + 9 = 0\) has no real roots.

gold[3] Q: Solve \(x^2 + 2x - 8 \le 0\) and \(x > 0\) simultaneously.

gold[4] Q: 0123456Sketch, not to scale Solve \(x^2 - 6x + 5 < 0\). How many integer values of \(x\) s
   step0 field=say answer=None text='Factorise \\(x^2 - 6x + 5\\). Two numbers multiply to \\(+5\\) and add to \\(-6\\): they are \\(-'
   step1 field=pre answer=1 text='From x - 1 = 0: x ='
   step2 field=pre answer=5 text='From x - 5 = 0: x ='
   step3 field=say answer=None text='For \\(< 0\\) the solution is between the roots: \\(1 < x < 5\\). Count the whole numbers stri'
   step4 field=pre answer=3 text='They are 2, 3, 4. How many?'
   step5 field=pre answer=0 text='Check the endpoint x = 1: 1² - 6(1) + 5 ='

silver[3] Q: Solve \(x^2 - 4x - 12 \ge 0\)

silver[4] Q: -3-2-10123456Sketch, not to scale Find the integer values of \(x\) satisfying \(x^2 - 3x -
   step0 field=say answer=None text='Factorise \\(x^2 - 3x - 10\\). Two numbers multiply to \\(-10\\) and add to \\(-3\\): they are \\'
   step1 field=pre answer=5 text='From x - 5 = 0: x ='
   step2 field=pre answer=-2 text='From x + 2 = 0: x ='
   step3 field=say answer=None text='For \\(< 0\\) the solution is between the roots: \\(-2 < x < 5\\). Count the whole numbers str'
   step4 field=pre answer=6 text='They are -1, 0, 1, 2, 3, 4. How many?'
   step5 field=pre answer=0 text='Check the endpoint x = 5: 5² - 3(5) - 10 ='

### board=maths-edexcel
bronze[4] Q: Solve \(x^2 - 10x + 24 < 0\). Give the lower bound.
   step0 field=say answer=None text='Factorise \\(x^2 - 10x + 24\\). Two numbers multiply to +24 and add to -10: they are -4 and '
   step1 field=pre answer=4 text='From x - 4 = 0: x ='
   step2 field=pre answer=6 text='From x - 6 = 0: x ='
   step3 field=say answer=None text='The curve is a U-shape crossing at 4 and 6. For \\(< 0\\) it dips below the x-axis BETWEEN t'
   step4 field=pre answer=4 text='The lower bound is the smaller root:'
   step5 field=pre answer=-1 text='Check with x = 5: 5² - 10(5) + 24 ='

gold[0] Q: Solve \(2x^2 - 5x - 3 > 0\). Give the larger critical value.
   step0 field=say answer=None text='With a 2 in front of \\(x^2\\), split the middle term. Two numbers multiply to \\((2)(-3) = -'
   step1 field=pre answer=3 text='From x - 3 = 0: x ='
   step2 field=pre answer=-1 text='From 2x + 1 = 0, first 2x ='
   step3 field=say answer=None text='So the other root is \\(x = -1 \\div 2 = -0.5\\). The roots are -0.5 and 3. For \\(> 0\\) the U'
   step4 field=pre answer=3 text='The larger critical value is'
   step5 field=pre answer=9 text='Check x = 4 (outside, to the right): 2(4²) - 5(4) - 3 ='

gold[2] Q: How many integers satisfy \(x^2 - 10x + 16 < 0\)?
   step0 field=say answer=None text='Factorise \\(x^2 - 10x + 16\\). Two numbers multiply to +16 and add to -10: they are -2 and '
   step1 field=pre answer=2 text='From x - 2 = 0: x ='
   step2 field=pre answer=8 text='From x - 8 = 0: x ='
   step3 field=say answer=None text='For \\(< 0\\) the solution is between the roots: \\(2 < x < 8\\). Count the whole numbers stri'
   step4 field=pre answer=5 text='They are 3, 4, 5, 6, 7. How many?'
   step5 field=pre answer=0 text='Check the endpoint x = 2: 2² - 10(2) + 16 ='

gold[3] Q: Solve \(x^2 + 2x + 1 > 0\). Describe the solution.

gold[4] Q: Find the range of \(k\) for which \(x^2 + kx + 9 = 0\) has no real roots.

silver[3] Q: Solve \(x^2 + 3x - 4 > 0\). Give the larger root.
   step0 field=say answer=None text='Factorise \\(x^2 + 3x - 4\\). Two numbers multiply to -4 and add to +3: they are +4 and -1, '
   step1 field=pre answer=-4 text='From x + 4 = 0: x ='
   step2 field=pre answer=1 text='From x - 1 = 0: x ='
   step3 field=say answer=None text='The curve is a U-shape crossing at -4 and 1. For \\(> 0\\) it is above the x-axis OUTSIDE th'
   step4 field=pre answer=1 text='The larger root is:'
   step5 field=pre answer=6 text='Check with x = 2: 2² + 3(2) - 4 ='

silver[4] Q: How many integers satisfy \(x^2 - 9 < 0\)?
   step0 field=say answer=None text='Factorise \\(x^2 - 9\\) as a difference of two squares: \\((x-3)(x+3)\\). Each bracket gives a'
   step1 field=pre answer=3 text='From x - 3 = 0: x ='
   step2 field=pre answer=-3 text='From x + 3 = 0: x ='
   step3 field=say answer=None text='For \\(< 0\\) the solution is between the roots: \\(-3 < x < 3\\). Count the whole numbers str'
   step4 field=pre answer=5 text='They are -2, -1, 0, 1, 2. How many?'
   step5 field=pre answer=0 text='Check the endpoint x = 3: 3² - 9 ='

### board=maths-ocr
bronze[4] Q: Solve \(x^2 > 25\). How many integers from \(-10\) to \(10\) satisfy this?
   step0 field=say answer=None text='Find where \\(x^2 = 25\\) by square-rooting: the critical values are \\(\\pm 5\\). So \\(x^2 > 2'
   step1 field=pre answer=5 text='The positive critical value is'
   step2 field=pre answer=-5 text='The negative critical value is'
   step3 field=say answer=None text='Now count the integers from \\(-10\\) to \\(10\\) that are below \\(-5\\) or above 5.'
   step4 field=pre answer=5 text='Integers -10 to -6 (all below -5): how many?'
   step5 field=pre answer=10 text='There are 5 more above 5 (6 to 10). Total ='

gold[0] Q: Solve \(3x^2 + 2x - 1 > 0\). What is the range?

gold[2] Q: Find the set of values of \(x\) for which \(x^2 - 2x > x + 4\). What is the range?

gold[3] Q: How many integers satisfy both \(x^2 - 9 \leq 0\) AND \(x + 1 > 0\)?
   step0 field=say answer=None text='Solve each part. First \\(x^2 - 9 \\leq 0\\) factorises to \\((x-3)(x+3) \\leq 0\\), giving betw'
   step1 field=pre answer=-1 text='The second condition x + 1 > 0 rearranges to x >'
   step2 field=say answer=None text='Overlap \\(-3 \\leq x \\leq 3\\) with \\(x > -1\\): since \\(x\\) must beat \\(-1\\), the overlap is'
   step3 field=pre answer=4 text='The whole numbers with -1 < x ≤ 3 are 0, 1, 2, 3. How many?'
   step4 field=pre answer=0 text='Check x = 3 in the first part: 3² - 9 ='

gold[4] Q: Solve \(6 - x - x^2 \geq 0\). What is the range?

silver[3] Q: Solve \(-x^2 + 4x - 3 > 0\). What is the range?

silver[4] Q: For what values of \(x\) is \(x^2 + 6x + 5 > 0\)?

### board=maths-eduqas
bronze[4] Q: Solve \(x^2 - 1 < 0\). Which is correct?

gold[0] Q: Solve \(2x^2 - 7x + 3 < 0\). Which is correct?

gold[2] Q: 012345Sketch, not drawn to scale How many integers satisfy \(x^2 - 5x + 4 \leq 0\)?
   step0 field=say answer=None text='Factorise \\(x^2 - 5x + 4\\). Two numbers multiply to \\(+4\\) and add to \\(-5\\): they are \\(-'
   step1 field=pre answer=1 text='From x - 1 = 0: x ='
   step2 field=pre answer=4 text='From x - 4 = 0: x ='
   step3 field=say answer=None text='The sign is \\(\\leq 0\\), so the solution is between the roots, endpoints included: \\(1 \\leq'
   step4 field=pre answer=4 text='They are 1, 2, 3, 4. How many?'
   step5 field=pre answer=0 text='Check the endpoint x = 1: 1² - 5(1) + 4 ='

gold[3] Q: -2-1012345Sketch, not drawn to scale Find the set of values of \(x\) for which \(x^2 < 3x 
   step0 field=say answer=None text='Rearrange \\(x^2 < 3x + 4\\) to \\(x^2 - 3x - 4 < 0\\). Factorise: two numbers multiply to \\(-'
   step1 field=pre answer=4 text='From x - 4 = 0: x ='
   step2 field=pre answer=-1 text='From x + 1 = 0: x ='
   step3 field=say answer=None text='For \\(< 0\\) the solution is between the roots: \\(-1 < x < 4\\). We want only the POSITIVE w'
   step4 field=pre answer=3 text='The positive integers are 1, 2, 3. How many?'
   step5 field=pre answer=0 text='Check the upper root x = 4: 4² - 3(4) - 4 ='

gold[4] Q: Solve \(x^2 + 3x - 4 > 0\) AND \(x < 3\). Which is correct?

silver[3] Q: Solve \(x^2 - 4x \leq 0\). Which is correct?

silver[4] Q: The point \((0, 0)\) satisfies which inequality: \(y x + 3\)?
