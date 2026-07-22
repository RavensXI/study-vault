# apply-pack: algebra__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[2] | The x term of the first product: 2x × 3 + 1 × x, coefficient = [box=7, label:'x' | fix: Split into two boxes matching the rest of the pack: 'Outer: 2x × 3 = [6]' and 'Inner: 1 × x = [1]', then 'Add the x terms: 6 + 1 = [7]'. Or at minimum write the

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: Expand \((x + 1)(x + 2)(x + 3)\)

### board=maths-edexcel
gold[2] Q: Expand and simplify \((2x + 1)(x + 3)\)

### board=maths-ocr
gold[2] Q: Expand \((3x + 4)(2x - 5)\)
   step0 field=say answer=None text='FOIL. First: 3x × 2x = 6x².'
   step1 field=pre answer=6 text='First coefficient: 3 × 2 ='
   step2 field=pre answer=-15 text='Outer: 3x × (−5) ='
   step3 field=pre answer=8 text='Inner: 4 × 2x ='
   step4 field=pre answer=-20 text='Last: 4 × (−5) ='
   step5 field=pre answer=-7 text='−15 + 8 ='
   step6 field=pre answer=20 text='So the expansion is 6x² − 7x −'
   step7 field=pre answer=-21 text='(3 + 4)(2 − 5) = 7 × (−3) ='
   step8 field=pre answer=-21 text='and 6 − 7 − 20 ='

### board=maths-eduqas
gold[2] Q: Expand \((2x + 1)(x + 3)(x - 2)\). What is the coefficient of \(x^2\)?
   step0 field=say answer=None text='Do two brackets first: \\((2x+1)(x+3) = 2x^2 + 7x + 3\\).'
   step1 field=pre answer=2 text='The x² term of the first product: 2x × x ='
   step2 field=pre answer=7 text='The x term of the first product: 2x × 3 + 1 × x, coefficient ='
   step3 field=say answer=None text='Now multiply (2x² + 7x + 3) by (x − 2). The x² term comes from two products.'
   step4 field=pre answer=-4 text='2x² × (−2) ='
   step5 field=pre answer=7 text='7x × x ='
   step6 field=pre answer=3 text='Add them: (−4) + 7 ='
