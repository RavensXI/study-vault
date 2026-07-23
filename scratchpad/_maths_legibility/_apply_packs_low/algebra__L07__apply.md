# apply-pack: algebra__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[0] | Split the middle: 2x² + 6x − x − 3, group to 2x(x+3) − 1(x+3) = (2x − 1)(x + 3). | fix: Split into two steps: one that ends at '= (2x − 1)(x + 3) = 0', then a separate step 'Set 2x − 1 = 0: 2x = 1, x = ___'.
- [low] silver[6] | So 3(x² − 4) = 0. Divide by 3: x² − 4 = 0, a difference of two squares (x+2)(x−2 | fix: Break into two steps: '3(x² − 4) = 0, divide by 3 → x² − 4 = 0 = (x+2)(x−2) = 0', then 'Set x + 2 = 0: x = ___'.
- [low] gold[0] | Multiply a by c: 2 × (−3) = −6. Find two numbers that multiply to −6 and add to  | fix: Replace 'Multiply a by c' with 'Multiply the two ends (the number in front of x² and the last number): 2 × (−3) = −6'.
- [low] gold[1] (also gold[3]) | First factor: 2x = 0, so x = [box=0] | fix: Add a one-line build, e.g. 'A number times x equals 0 only when x = 0, so 2x = 0 gives x = 0 (divide both sides by 2).'
- [low] silver[2] | Split: 2x² + 4x − x − 2, group to 2x(x+2) − 1(x+2) = (2x − 1)(x + 2). Set 2x − 1 | fix: Break into two steps: first show/confirm the factorisation ((2x − 1)(x + 2) = 0), then a separate 'Set 2x − 1 = 0, so 2x = 1, x = ___' step.
- [low] gold[4] | Split: 5x² − 5x + 2x − 2, group to 5x(x − 1) + 2(x − 1) = (5x + 2)(x − 1). Set x | fix: Split into a factorisation step and a separate 'Set x − 1 = 0, so x = ___' solve step.
- [low] gold[0] | intro: Split and factor: 2x² + 6x − x − 3 = (2x − 1)(x + 3) = 0. | fix: Add one intro step showing the grouping: 'Group in pairs: 2x(x+3) − 1(x+3), then take out the common (x+3) to get (2x−1)(x+3).'
- [low] gold[1] | ask: Add the roots over 3: 3/3 + (−2/3) = 1/3. The numerator is [box=1, NO label | fix: Spell out the common denominator: 'Write both solutions over 3: 1 = 3/3, so 3/3 + (−2/3) = 1/3.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: Solve \(2x^2 + 5x - 3 = 0\)
   step0 field=pre answer=-1 text='Multiply a by c: 2 × (−3) = −6. Find two numbers that multiply to −6 and add to +5: 6 and'
   step1 field=pre answer=0.5 text='Split the middle: 2x² + 6x − x − 3, group to 2x(x+3) − 1(x+3) = (2x − 1)(x + 3). Set 2x − '
   step2 field=pre answer=-3 text='Set the second bracket to 0: x + 3 = 0 gives x ='
   step3 field=pre answer=0 text='Check x = 0.5: 2×0.5² + 5×0.5 − 3 ='

gold[1] Q: Solve \(5x^2 - 9x - 2 = 0\)
   step0 field=pre answer=-10 text='Multiply a by c: 5 × (−2) = −10. Find two numbers that multiply to −10 and add to −9: 1 an'
   step1 field=pre answer=-0.2 text='Split the middle: 5x² − 10x + x − 2, group to 5x(x−2) + 1(x−2) = (5x + 1)(x − 2). Set 5x +'
   step2 field=pre answer=2 text='Set the second bracket to 0: x − 2 = 0 gives x ='
   step3 field=pre answer=0 text='Check x = 2: 5×2² − 9×2 − 2 ='

gold[4] Q: Solve \(4x^2 - 1 = 0\)
   step0 field=pre answer=1 text='A difference of two squares: 4x² = (2x)² and 1 = 1². So 4x² − 1 = (2x + 1)(2x −'
   step1 field=pre answer=-0.5 text='So (2x + 1)(2x − 1) = 0. Set the first bracket to 0: 2x + 1 = 0, 2x = −1, x ='
   step2 field=pre answer=0.5 text='Set the second bracket to 0: 2x − 1 = 0, 2x = 1, x ='
   step3 field=pre answer=0 text='Check x = 0.5: 4×0.5² − 1 ='

silver[2] Q: Solve \(x^2 - 8x + 16 = 0\). Enter both solutions (they are equal).
   step0 field=pre answer=4 text='Find two numbers that multiply to +16 and add to −8. Both are the same: −4 and −4. So this'
   step1 field=pre answer=4 text='Set the repeated bracket to 0: x − 4 = 0 gives x ='
   step2 field=pre answer=4 text='Because the bracket is squared, the second solution is the same value: x ='
   step3 field=pre answer=0 text='Check x = 4: 4² − 8×4 + 16 ='

silver[6] Q: Solve \(3x^2 - 12 = 0\)
   step0 field=pre answer=4 text='Take out the common factor 3: 3x² − 12 = 3(x² −'
   step1 field=pre answer=-2 text='So 3(x² − 4) = 0. Divide by 3: x² − 4 = 0, a difference of two squares (x+2)(x−2) = 0. Set'
   step2 field=pre answer=2 text='Set the second bracket to 0: x − 2 = 0 gives x ='
   step3 field=pre answer=0 text='Check x = 2: 3×2² − 12 ='

### board=maths-edexcel
gold[0] Q: \(x^2 = 5x - 6\)
   step0 field=say answer=None text='First rearrange so one side is 0. Move every term on the right across to the left; each on'
   step1 field=pre answer=-5 text='The 5x on the right moves left and becomes'
   step2 field=pre answer=6 text='The −6 on the right moves left and becomes'
   step3 field=say answer=None text='So \\(x^2 − 5x + 6 = 0\\). Now two numbers multiply to \\(6\\) and add to \\(−5\\).'
   step4 field=pre answer=-3 text='The smaller of the two numbers is'
   step5 field=pre answer=-2 text='The larger of the two numbers is'
   step6 field=say answer=None text='So \\((x − 3)(x − 2) = 0\\).'
   step7 field=pre answer=3 text='First bracket zero: x − 3 = 0, so x ='
   step8 field=pre answer=2 text='Second bracket zero: x − 2 = 0, so x ='
   step9 field=pre answer=0 text='Check x = 3: (3)² − 5×(3) + 6 ='

gold[1] Q: \(2x^2 + 6x = 0\)
   step0 field=say answer=None text='Both terms share a common factor. Take out the largest one, which is \\(2x\\).'
   step1 field=pre answer=3 text='Divide the second term by 2x: 6x ÷ 2x ='
   step2 field=say answer=None text='So \\(2x(x + 3) = 0\\). Either factor can be zero.'
   step3 field=pre answer=0 text='First factor: 2x = 0, so x ='
   step4 field=pre answer=-3 text='Second factor: x + 3 = 0, so x ='
   step5 field=pre answer=0 text='Check x = −3: 2×(−3)² + 6×(−3) ='

gold[4] Q: \(x^2 + x = 6\)
   step0 field=say answer=None text='First rearrange so one side is 0. Move every term on the right across to the left; each on'
   step1 field=pre answer=-6 text='The 6 on the right moves left and becomes'
   step2 field=say answer=None text='So \\(x^2 + x − 6 = 0\\). Now two numbers multiply to \\(−6\\) and add to \\(1\\).'
   step3 field=pre answer=-2 text='The smaller of the two numbers is'
   step4 field=pre answer=3 text='The larger of the two numbers is'
   step5 field=say answer=None text='So \\((x − 2)(x + 3) = 0\\).'
   step6 field=pre answer=2 text='First bracket zero: x − 2 = 0, so x ='
   step7 field=pre answer=-3 text='Second bracket zero: x + 3 = 0, so x ='
   step8 field=pre answer=0 text='Check x = 2: (2)² + 1×(2) − 6 ='

silver[2] Q: \(x^2 - x - 12 = 0\)
   step0 field=say answer=None text='Solve \\(x^2 - x - 12 = 0\\) by finding two numbers that multiply to \\(−12\\) and add to \\(−1'
   step1 field=pre answer=-4 text='The smaller of the two numbers is'
   step2 field=pre answer=3 text='The larger of the two numbers is'
   step3 field=say answer=None text='So it factorises to \\((x − 4)(x + 3) = 0\\). Each bracket can be zero.'
   step4 field=pre answer=4 text='First bracket zero: x − 4 = 0, so x ='
   step5 field=pre answer=-3 text='Second bracket zero: x + 3 = 0, so x ='
   step6 field=pre answer=0 text='Check x = 4: (4)² − 1×(4) − 12 ='

silver[6] Q: \(x^2 - 9 = 0\)
   step0 field=say answer=None text='Solve \\(x^2 - 9 = 0\\) by finding two numbers that multiply to \\(−9\\) and add to \\(0\\).'
   step1 field=pre answer=-3 text='The smaller of the two numbers is'
   step2 field=pre answer=3 text='The larger of the two numbers is'
   step3 field=say answer=None text='So it factorises to \\((x − 3)(x + 3) = 0\\). Each bracket can be zero.'
   step4 field=pre answer=3 text='First bracket zero: x − 3 = 0, so x ='
   step5 field=pre answer=-3 text='Second bracket zero: x + 3 = 0, so x ='
   step6 field=pre answer=0 text='Check x = 3: (3)² − 9 ='

### board=maths-ocr
gold[0] Q: Solve \(4x^2 + 4x - 3 = 0\)
   step0 field=pre answer=-2 text='Two numbers multiply to −12 and add to 4: 6 and'
   step1 field=pre answer=0.5 text='Split: 4x² + 6x − 2x − 3, group to 2x(2x+3) − 1(2x+3) = (2x + 3)(2x − 1). Set 2x − 1 = 0: '
   step2 field=pre answer=-1.5 text='Set 2x + 3 = 0: 2x = −3, x ='
   step3 field=pre answer=0 text='Check x = 0.5: 4×(0.5)² + 4×(0.5) − 3 ='

gold[1] Q: Solve \(4x^2 - 1 = 0\)
   step0 field=say answer=None text='There is no middle term, so this is a difference of two squares: \\(4x^2\\) is \\((2x)^2\\) an'
   step1 field=pre answer=0.5 text='So it factorises to (2x + 1)(2x − 1) = 0. Set 2x − 1 = 0: 2x = 1, x ='
   step2 field=pre answer=-0.5 text='Set 2x + 1 = 0: 2x = −1, x ='
   step3 field=pre answer=0 text='Check x = 0.5: 4×(0.5)² − 1 ='

gold[4] Q: Solve \(5x^2 - 3x - 2 = 0\)
   step0 field=pre answer=-5 text='Two numbers multiply to −10 and add to −3: 2 and'
   step1 field=pre answer=1 text='Split: 5x² − 5x + 2x − 2, group to 5x(x − 1) + 2(x − 1) = (5x + 2)(x − 1). Set x − 1 = 0: '
   step2 field=pre answer=-0.4 text='Set 5x + 2 = 0: 5x = −2, x ='
   step3 field=pre answer=0 text='Check x = 1: 5×(1)² − 3×(1) − 2 ='

silver[2] Q: Solve \(2x^2 + 3x - 2 = 0\)
   step0 field=pre answer=-1 text='Two numbers multiply to −4 and add to 3: 4 and'
   step1 field=pre answer=0.5 text='Split: 2x² + 4x − x − 2, group to 2x(x+2) − 1(x+2) = (2x − 1)(x + 2). Set 2x − 1 = 0: 2x ='
   step2 field=pre answer=-2 text='Set x + 2 = 0: x ='
   step3 field=pre answer=0 text='Check x = 0.5: 2×(0.5)² + 3×(0.5) − 2 ='

silver[6] Q: Solve \(x^2 - 10x + 25 = 0\)
   step0 field=say answer=None text='Solve \\(x^2 - 10x + 25 = 0\\). Two equal numbers multiply to 25 and add to \\(-10\\).'
   step1 field=pre answer=-5 text='The first of the two equal numbers is'
   step2 field=pre answer=-5 text='The second (equal) number is'
   step3 field=say answer=None text='So \\((x - 5)(x - 5) = (x - 5)^2 = 0\\). A perfect square: the root is repeated.'
   step4 field=pre answer=5 text='x − 5 = 0, so x ='
   step5 field=pre answer=5 text='The root is repeated, so the second solution is also x ='
   step6 field=pre answer=0 text='Check x = 5: (5)² − 10×(5) + 25 ='

### board=maths-eduqas
gold[0] Q: Solve \(2x^2 + 5x - 3 = 0\). Find the positive solution as a fraction (give the numerator)
   step0 field=say answer=None text='Solve \\(2x^2 + 5x - 3 = 0\\). Because \\(a = 2\\), split the middle term: two numbers multipl'
   step1 field=pre answer=6 text='The positive number is'
   step2 field=pre answer=1 text='The negative number is −'
   step3 field=say answer=None text='Split and factor: \\(2x^2 + 6x - x - 3 = (2x - 1)(x + 3) = 0\\).'
   step4 field=pre answer=2 text='First bracket: 2x − 1 = 0, so 2x = 1 and x = 1 over'
   step5 field=pre answer=-3 text='Second bracket: x + 3 = 0, so x ='
   step6 field=pre answer=1 text='The positive solution is 1/2. Its numerator (top number) is'
   step7 field=pre answer=0 text='Check x = 1/2: 2×(1/2)² + 5×(1/2) − 3 = 0.5 + 2.5 − 3 ='

gold[1] Q: Solve \(3x^2 - x - 2 = 0\). Find the sum of both solutions as a fraction.
   step0 field=say answer=None text='Solve \\(3x^2 - x - 2 = 0\\). Split the middle term: two numbers multiply to \\(3 \\times (-2)'
   step1 field=pre answer=3 text='The negative number is −'
   step2 field=pre answer=2 text='The positive number is'
   step3 field=say answer=None text='Split and factor: \\(3x^2 - 3x + 2x - 2 = (3x + 2)(x - 1) = 0\\).'
   step4 field=pre answer=1 text='First bracket: x − 1 = 0, so x ='
   step5 field=pre answer=3 text='Second bracket: 3x + 2 = 0, so x = −2 over'
   step6 field=pre answer=1 text='Add the roots over 3: 3/3 + (−2/3) = 1/3. The numerator is'
   step7 field=pre answer=3 text='The denominator is'
   step8 field=pre answer=0 text='Check x = 1: 3×(1)² − 1 − 2 = 3 − 1 − 2 ='

gold[4] Q: Solve \(4x^2 = 9\). Find the positive solution as a fraction.
   step0 field=say answer=None text='Solve \\(4x^2 = 9\\). First move 9 across to get \\(4x^2 - 9 = 0\\), a difference of two squar'
   step1 field=pre answer=3 text='√(4x²) = 2x and √9 = 3, so it factors as (2x + 3)(2x −'
   step2 field=say answer=None text='So \\((2x + 3)(2x - 3) = 0\\).'
   step3 field=pre answer=2 text='Second bracket: 2x − 3 = 0, so 2x = 3 and x = 3 over'
   step4 field=pre answer=3 text='First bracket: 2x + 3 = 0 gives x = −3/2 (negative). The positive root is 3/2, whose numer'
   step5 field=pre answer=2 text='The denominator of the positive solution 3/2 is'
   step6 field=pre answer=9 text='Check x = 3/2: 4×(3/2)² = 4×(9/4) ='

silver[2] Q: Solve \(x^2 - 2x - 35 = 0\). Find the negative solution.
   step0 field=say answer=None text='Solve \\(x^2 - 2x - 35 = 0\\). Two numbers multiply to \\(-35\\) and add to \\(-2\\): that is 5 '
   step1 field=pre answer=5 text='The positive number is'
   step2 field=pre answer=-7 text='The negative number is'
   step3 field=say answer=None text='So \\((x + 5)(x - 7) = 0\\).'
   step4 field=pre answer=-5 text='x + 5 = 0, so x ='
   step5 field=pre answer=7 text='x − 7 = 0, so x ='
   step6 field=pre answer=-5 text='The negative solution is'
   step7 field=pre answer=0 text='Check x = −5: (−5)² − 2×(−5) − 35 ='

silver[6] Q: Solve \(x^2 - 10x + 25 = 0\). How many different solutions are there?
   step0 field=say answer=None text='Solve \\(x^2 - 10x + 25 = 0\\). Two numbers multiply to 25 and add to \\(-10\\): they are \\(-5'
   step1 field=pre answer=5 text='The repeated number is −'
   step2 field=say answer=None text='So \\((x - 5)(x - 5) = 0\\), which is \\((x - 5)^2 = 0\\).'
   step3 field=pre answer=5 text='First bracket: x − 5 = 0, so x ='
   step4 field=pre answer=5 text='The second bracket is the same, so it also gives x ='
   step5 field=pre answer=1 text='Both brackets give the same value, so the number of different solutions is'
   step6 field=pre answer=0 text='Check x = 5: (5)² − 10×(5) + 25 ='
