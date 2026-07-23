# apply-pack: algebra__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] | Middle term of (x+4)²: 2 × 4 = [box=8, label:'x'] | fix: Add an intro line before the ask, e.g. 'In (x+4)² the two middle products are both x × 4 = 4x, and 4x + 4x = 2 × 4 = 8x.' Then keep the 2 × 4 ask. (Same shortcu
- [low] silver[0] | and 1 + 7 + 12 = [box=20, NO label] | fix: Add a short intro before this ask, e.g. 'Now put x = 1 into your expansion x² + 7x + 12: that is 1 + 7 + 12.' Then both sides should match at 20.
- [low] gold[2] | So the expansion is 6x² − 7x − [box=20, NO label] | fix: Keep the sign consistent with the value just computed, e.g. ask '6x² − 7x + [box=-20]', or state it in prose: 'the constant term is −20, giving 6x² − 7x − 20'.
- [low] silver[0] | FOIL. First is x × x = x², the x² term. Now the Outer and Inner products. | fix: Spell the mnemonic out once on first use: 'FOIL means multiply each pair in turn — First, Outer, Inner, Last.'
- [low] silver[4] | The x terms cancel (4x − 4x = 0). The constant is the Last pair. | fix: Spell it out: 'The constant term is the last term of each bracket, multiplied together.' Apply the same rewrite in silver[1] and silver[6].

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: Expand \((x + 1)(x + 2)(x + 3)\)

gold[3] Q: Show that \((x + 4)^2 - (x + 2)^2\) simplifies to \(ax + b\). Find \(a\).
   step0 field=say answer=None text='Expand each square fully, keeping the middle term. Start with \\((x+4)^2\\).'
   step1 field=pre answer=8 text='Middle term of (x+4)²: 2 × 4 ='
   step2 field=pre answer=16 text='Constant of (x+4)²: 4 × 4 ='
   step3 field=say answer=None text='So \\((x+4)^2 = x^2 + 8x + 16\\). Now \\((x+2)^2\\).'
   step4 field=pre answer=4 text='Middle term of (x+2)²: 2 × 2 ='
   step5 field=pre answer=4 text='Constant of (x+2)²: 2 × 2 ='
   step6 field=pre answer=4 text='x terms: 8 − 4 ='
   step7 field=pre answer=12 text='constants: 16 − 4 ='
   step8 field=say answer=None text='So it simplifies to 4x + 12, which matches ax + b.'
   step9 field=pre answer=4 text='The question asks for a, the number in front of x. a ='

silver[0] Q: Expand and simplify \((x + 4)(x + 3)\)
   step0 field=say answer=None text='FOIL. First is x × x = x², the x² term. Now the Outer and Inner products.'
   step1 field=pre answer=3 text='Outer: x × 3 ='
   step2 field=pre answer=4 text='Inner: 4 × x ='
   step3 field=pre answer=12 text='Last: 4 × 3 ='
   step4 field=say answer=None text='Collect the two middle terms: 3x + 4x.'
   step5 field=pre answer=7 text='3 + 4 ='
   step6 field=pre answer=12 text='So the expansion is x² + 7x +'
   step7 field=pre answer=20 text='(1+4)(1+3) = 5 × 4 ='
   step8 field=pre answer=20 text='and 1 + 7 + 12 ='

silver[4] Q: Expand \((x + 5)^2\)

### board=maths-edexcel
gold[2] Q: Expand and simplify \((2x + 1)(x + 3)\)

gold[3] Q: Expand and simplify \((3x - 2)(2x + 5)\)

silver[0] Q: Expand and simplify \((x + 2)(x + 5)\)

silver[4] Q: Expand and simplify \((x + 4)(x + 4)\)

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

gold[3] Q: Expand \((x + 1)^3\)

silver[0] Q: Expand \((x + 3)(x + 5)\)
   step0 field=say answer=None text='FOIL. First is x × x = x², the x² term. Now the Outer and Inner products.'
   step1 field=pre answer=5 text='Outer: x × 5 ='
   step2 field=pre answer=3 text='Inner: 3 × x ='
   step3 field=pre answer=15 text='Last: 3 × 5 ='
   step4 field=say answer=None text='Collect the two middle terms: 5x + 3x.'
   step5 field=pre answer=8 text='5 + 3 ='
   step6 field=pre answer=15 text='So the expansion is x² + 8x +'
   step7 field=pre answer=24 text='(1+3)(1+5) = 4 × 6 ='
   step8 field=pre answer=24 text='and 1 + 8 + 15 ='

silver[4] Q: Expand \((x + 4)^2\)
   step0 field=say answer=None text='Squaring means (x+4)(x+4). First: x × x = x². Now the middle, which appears twice.'
   step1 field=pre answer=4 text='One middle term: x × 4 ='
   step2 field=pre answer=8 text='It appears twice, so the middle total is 2 × 4 ='
   step3 field=pre answer=16 text='Last: 4 × 4 ='
   step4 field=pre answer=25 text='(1+4)² = 5² ='
   step5 field=pre answer=25 text='and 1 + 8 + 16 ='

### board=maths-eduqas
gold[2] Q: Expand \((2x + 1)(x + 3)(x - 2)\). What is the coefficient of \(x^2\)?
   step0 field=say answer=None text='Do two brackets first: \\((2x+1)(x+3) = 2x^2 + 7x + 3\\).'
   step1 field=pre answer=2 text='The x² term of the first product: 2x × x ='
   step2 field=pre answer=7 text='The x term comes from two products: 2x × 3 = 6x, and 1 × x = 1x. Add those coefficients: 6'
   step3 field=say answer=None text='Now multiply (2x² + 7x + 3) by (x − 2). The x² term comes from two products.'
   step4 field=pre answer=-4 text='2x² × (−2) ='
   step5 field=pre answer=7 text='7x × x ='
   step6 field=pre answer=3 text='Add them: (−4) + 7 ='

gold[3] Q: Expand \((x + 2)^3\). What is the coefficient of \(x^2\)?
   step0 field=say answer=None text='A cube is three brackets. First square: \\((x+2)(x+2) = x^2 + 4x + 4\\).'
   step1 field=pre answer=4 text='Confirm the x term of the square: 2 + 2 ='
   step2 field=say answer=None text='Now multiply (x² + 4x + 4) by (x + 2). The x² term comes from two products.'
   step3 field=pre answer=2 text='x² × 2 ='
   step4 field=pre answer=4 text='4x × x ='
   step5 field=pre answer=6 text='Add them: 2 + 4 ='

silver[0] Q: Expand \((x + 2)(x + 5)\). What is the coefficient of \(x\)?
   step0 field=pre answer=5 text='Outer: x × 5 ='
   step1 field=pre answer=2 text='Inner: 2 × x ='
   step2 field=say answer=None text='Add the two x terms to get the coefficient.'
   step3 field=pre answer=7 text='5 + 2 ='
   step4 field=pre answer=7 text='Full expansion x² + 7x + 10. Coefficient of x ='

silver[4] Q: Expand \((x - 4)(x + 4)\). What is the constant term?
   step0 field=pre answer=4 text='Outer: x × 4 ='
   step1 field=pre answer=-4 text='Inner: (−4) × x ='
   step2 field=say answer=None text='The x terms cancel (4x − 4x = 0). The constant is the Last pair.'
   step3 field=pre answer=-16 text='Last: (−4) × 4 ='
   step4 field=pre answer=-16 text='Full expansion x² − 16. Constant term ='
