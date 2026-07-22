# apply-pack: algebra__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[2] | \(\sqrt{4}\) = [box=2] ... So (2x + 3)(2x − 3). Check the x² term: 2 × 2 = [box= | fix: Add an explicit step mirroring gold[0]: 'The square root of 4x² is 2x' (or ask \sqrt{4x^2} = [box=2, label:'x']) before presenting the (2x+3)(2x−3) bracket.
- [medium] gold[4] | \(\sqrt{9}\) = [box=3] ... So (3x + 4)(3x − 4). Check the x² term: 3 × 3 = [box= | fix: Add the missing root-of-the-variable step, e.g. 'The square root of 9x² is 3x' (or \sqrt{9x^2} = [box=3, label:'x']) before the (3x+4)(3x−4) line.
- [medium] bronze[7] | Check by expanding: 3x × 1x gives the x² term, coefficient 3 × 1 = | fix: Drop the '1x': rewrite as 'Check by expanding: 3x × x gives the x² term. Its coefficient: 3 × 1 = ' (box answer still 3, no label needed).

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[7] Q: Factorise \(x^2 - 16\)

gold[2] Q: Factorise \(3x^2 - 12\)

gold[4] Q: Factorise completely \(2x^3 - 18x\)

### board=maths-edexcel
bronze[7] Q: Factorise \(7x^2 - 14x\)
   step0 field=pre answer=7 text='Every term has an x, and the highest common factor of 7 and 14 ='
   step1 field=pre answer=1 text='So take out 7x. Divide the first term: 7x² ÷ 7x ='
   step2 field=pre answer=-2 text='Divide the second term: −14x ÷ 7x ='
   step3 field=pre answer=7 text='Check by expanding: 7x × 1x gives the x² term, coefficient 7 × 1 ='
   step4 field=pre answer=-14 text='and 7x × (−2) ='

gold[2] Q: Factorise \(4x^2 - 9\)
   step0 field=say answer=None text='This is a difference of two squares: two square terms with a minus between them, and no mi'
   step1 field=pre answer=2 text='\\(\\sqrt{4}\\) ='
   step2 field=pre answer=3 text='\\(\\sqrt{9}\\) ='
   step3 field=pre answer=4 text='So (2x + 3)(2x − 3). Check the x² term: 2 × 2 ='
   step4 field=pre answer=0 text='and the middle terms +6x and −6x add to'

gold[4] Q: Factorise \(9x^2 - 16\)
   step0 field=say answer=None text='This is a difference of two squares: two square terms with a minus between them, and no mi'
   step1 field=pre answer=3 text='\\(\\sqrt{9}\\) ='
   step2 field=pre answer=4 text='\\(\\sqrt{16}\\) ='
   step3 field=pre answer=9 text='So (3x + 4)(3x − 4). Check the x² term: 3 × 3 ='
   step4 field=pre answer=0 text='and the middle terms +12x and −12x add to'

### board=maths-ocr
bronze[7] Q: Factorise \(14p + 21q\)

gold[2] Q: Factorise completely \(2x^3 - 8x\)

gold[4] Q: Factorise \(x^2 - 6x + 9\)

### board=maths-eduqas
bronze[7] Q: Factorise \(3x^2 + 6x\)
   step0 field=pre answer=3 text='Every term has an x, and the highest common factor of 3 and 6 ='
   step1 field=pre answer=1 text='So take out 3x. Divide the first term: 3x² ÷ 3x ='
   step2 field=pre answer=2 text='Divide the second term: 6x ÷ 3x ='
   step3 field=pre answer=3 text='Check by expanding: 3x × 1x gives the x² term, coefficient 3 × 1 ='
   step4 field=pre answer=6 text='and 3x × (2) ='

gold[2] Q: Factorise \(x^2 - 6x + 9\)
   step0 field=pre answer=9 text='The number at the end, c, is'
   step1 field=pre answer=-3 text='Two numbers multiplying to 9 and adding to −6 are −3 and −3. Each number is'
   step2 field=pre answer=9 text='So (x − 3)(x − 3) = (x − 3)². Check: (−3) × (−3) ='
   step3 field=pre answer=-6 text='and (−3) + (−3) ='

gold[4] Q: Factorise completely \(5x^3 - 20x\)
   step0 field=pre answer=5 text='The highest common factor of 5 and 20 ='
   step1 field=pre answer=2 text='Now x² − 4 is a difference of two squares. √4 ='
   step2 field=pre answer=0 text='So x² − 4 = (x + 2)(x − 2). The middle terms +2x and −2x add to'
   step3 field=pre answer=-4 text='and 2 × (−2) ='
