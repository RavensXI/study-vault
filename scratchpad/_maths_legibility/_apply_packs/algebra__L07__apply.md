# apply-pack: algebra__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[0] (also gold[2], gold[4]) | The −6 on the right moves left and becomes + [box=6, NO label] vs gold[2] 'The 5 | fix: Standardise so the box always holds the complete signed number: delete the stray '+' in gold[0] so it reads 'becomes [box]' with box=6, matching gold[2]/gold[4]

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: Solve \(2x^2 + 5x - 3 = 0\)
   step0 field=pre answer=-1 text='Multiply a by c: 2 × (−3) = −6. Find two numbers that multiply to −6 and add to +5: 6 and'
   step1 field=pre answer=0.5 text='Split the middle: 2x² + 6x − x − 3, group to 2x(x+3) − 1(x+3) = (2x − 1)(x + 3). Set 2x − '
   step2 field=pre answer=-3 text='Set the second bracket to 0: x + 3 = 0 gives x ='
   step3 field=pre answer=0 text='Check x = 0.5: 2×0.5² + 5×0.5 − 3 ='

### board=maths-edexcel
gold[0] Q: \(x^2 = 5x - 6\)
   step0 field=say answer=None text='First rearrange so one side is 0. Move every term on the right across to the left; each on'
   step1 field=pre answer=-5 text='The 5x on the right moves left and becomes'
   step2 field=pre answer=6 text='The −6 on the right moves left and becomes +'
   step3 field=say answer=None text='So \\(x^2 − 5x + 6 = 0\\). Now two numbers multiply to \\(6\\) and add to \\(−5\\).'
   step4 field=pre answer=-3 text='The smaller of the two numbers is'
   step5 field=pre answer=-2 text='The larger of the two numbers is'
   step6 field=say answer=None text='So \\((x − 3)(x − 2) = 0\\).'
   step7 field=pre answer=3 text='First bracket zero: x − 3 = 0, so x ='
   step8 field=pre answer=2 text='Second bracket zero: x − 2 = 0, so x ='
   step9 field=pre answer=0 text='Check x = 3: (3)² − 5×(3) + 6 ='

### board=maths-ocr
gold[0] Q: Solve \(4x^2 + 4x - 3 = 0\)
   step0 field=pre answer=-2 text='Two numbers multiply to −12 and add to 4: 6 and'
   step1 field=pre answer=0.5 text='Split: 4x² + 6x − 2x − 3, group to 2x(2x+3) − 1(2x+3) = (2x + 3)(2x − 1). Set 2x − 1 = 0: '
   step2 field=pre answer=-1.5 text='Set 2x + 3 = 0: 2x = −3, x ='
   step3 field=pre answer=0 text='Check x = 0.5: 4×(0.5)² + 4×(0.5) − 3 ='

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
