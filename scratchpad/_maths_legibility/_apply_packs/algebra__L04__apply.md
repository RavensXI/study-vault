# apply-pack: algebra__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[0] step 1 | Substitute y = 3 and clear the fraction: 3 × (x − 1). Work out 3 × 1 = [box=3] | fix: Split and connect it: e.g. 'Multiply out 3(x − 1). The number part is 3 × 1 = [3], so 3(x − 1) = 3x − 3.'
- [medium] gold[2] step 1 | Substitute y = 3 and clear the fraction: 3 × (x + 1). Work out 3 × 1 = [box=3] | fix: Reword to make the expansion explicit: 'Multiply out 3(x + 1). The number part is 3 × 1 = [3], so 3(x + 1) = 3x + 3.'
- [medium] bronze[1] | Q: 73Diagram not drawn accurately\(P = 2l + 2w\). Find P when l = 7, w = 3. | fix: Split it out and drop the stray number: 'Diagram not drawn accurately. \(P = 2l + 2w\). Find P when l = 7 cm, w = 3 cm.'
- [medium] bronze[4] | Q: 69Diagram not drawn accurately\(A = bh\). Find A when b = 6, h = 9. | fix: Split it out and drop the stray number: 'Diagram not drawn accurately. \(A = bh\). Find A when b = 6 cm, h = 9 cm.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[1] Q: If \(P = 2l + 2w\), find \(P\) when \(l = 8\) and \(w = 3\)
   step0 field=pre answer=16 text='The 2l part: 2 × 8 ='
   step1 field=pre answer=6 text='The 2w part: 2 × 3 ='
   step2 field=pre answer=22 text='Add them: 16 + 6 ='
   step3 field=pre answer=22 text='Check: 2 × 8 + 2 × 3 ='

bronze[4] Q: If \(y = x^2 - 4\), find \(y\) when \(x = -3\)
   step0 field=pre answer=9 text='Square x: (−3) × (−3) ='
   step1 field=pre answer=5 text='Subtract 4: 9 − 4 ='
   step2 field=pre answer=9 text='Confirm the sign: (−3) × (−3) ='

gold[0] Q: If \(y = \frac{x + 3}{x - 1}\), find \(x\) when \(y = 3\)
   step0 field=pre answer=3 text='Substitute y = 3 and clear the fraction: 3 × (x − 1). Work out 3 × 1 ='
   step1 field=pre answer=2 text='So 3x − 3 = x + 3. Take x from both sides: 3x − x ='
   step2 field=pre answer=6 text='Add 3 to both sides: 3 + 3 ='
   step3 field=pre answer=3 text='Now 2x = 6, so x = 6 ÷ 2 ='
   step4 field=pre answer=3 text='Check: (3 + 3) ÷ (3 − 1) = 6 ÷ 2 ='

gold[2] Q: If \(y = \frac{2x}{x + 1}\), find \(x\) when \(y = 3\)
   step0 field=pre answer=3 text='Substitute y = 3 and clear the fraction: 3 × (x + 1). Work out 3 × 1 ='
   step1 field=pre answer=1 text='So 3x + 3 = 2x. Take 2x from both sides: 3x − 2x ='
   step2 field=pre answer=-3 text='Now x + 3 = 0, so x = 0 − 3 ='
   step3 field=pre answer=3 text='Check: 2 × (−3) ÷ (−3 + 1) = −6 ÷ (−2) ='

### board=maths-edexcel
bronze[1] Q: Find the value of \(4x - 1\) when \(x = 6\)
   step0 field=say answer=None text='Substitute x = 6, so 4x means 4 × 6. BIDMAS: multiply before you take away the 1.'
   step1 field=pre answer=24 text='4 × 6 ='
   step2 field=pre answer=23 text='now subtract 1: 24 − 1 ='
   step3 field=pre answer=23 text='Check: four 6s make 24, less 1 is'

bronze[4] Q: Find the value of \(4a - b\) when \(a = 5\) and \(b = 3\)
   step0 field=say answer=None text='Substitute a = 5 and b = 3, giving 4 × 5 − 3. The multiply comes before the subtraction.'
   step1 field=pre answer=20 text='4 × 5 ='
   step2 field=pre answer=17 text='subtract b: 20 − 3 ='
   step3 field=pre answer=17 text='Check: four 5s make 20, less 3 is'

gold[0] Q: Make \(x\) the subject of \(y = 5x + 2\)

gold[2] Q: Make \(r\) the subject of \(A = \pi r^2\)

### board=maths-ocr
bronze[1] Q: If \(x = 4\) and \(y = 3\), find \(2x + y\)
   step0 field=say answer=None text='Substitute x = 4 and y = 3 into \\(2x + y\\).'
   step1 field=pre answer=8 text='Only x is doubled: 2 × 4 ='
   step2 field=pre answer=11 text='Add y = 3: 8 + 3 ='
   step3 field=pre answer=11 text='Check: 2(4) + 3 ='

bronze[4] Q: If \(x = -2\), find \(5x\)
   step0 field=say answer=None text='Substitute x = −2 into \\(5x\\), which means 5 × x.'
   step1 field=pre answer=10 text='Ignore the sign for a moment: 5 × 2 ='
   step2 field=pre answer=-10 text='Positive × negative is negative, so 5 × (−2) ='
   step3 field=pre answer=-10 text='Check: 5 × (−2) ='

gold[0] Q: Make \(x\) the subject: \(y = \frac{3x + 1}{x - 2}\)

gold[2] Q: If \(x = 2\), find \(\frac{3x^3 + x^2 - 4}{x + 1}\)
   step0 field=say answer=None text='Substitute x = 2 into \\(\\frac{3x^3 + x^2 - 4}{x + 1}\\). Work the numerator and denominator'
   step1 field=pre answer=24 text='Cube term: 3 × 2³ = 3 × 8 ='
   step2 field=pre answer=4 text='Square term: 2² ='
   step3 field=pre answer=24 text='Numerator: 24 + 4 − 4 ='
   step4 field=pre answer=3 text='Denominator: 2 + 1 ='
   step5 field=pre answer=8 text='Divide: 24 ÷ 3 ='
   step6 field=pre answer=8 text='Check: numerator 24, denominator 3, so 24 ÷ 3 ='

### board=maths-eduqas
bronze[1] Q: 73Diagram not drawn accurately\(P = 2l + 2w\). Find \(P\) when \(l = 7\), \(w = 3\).
   step0 field=pre answer=14 text='Two lots of the length: 2 × 7 ='
   step1 field=pre answer=6 text='Two lots of the width: 2 × 3 ='
   step2 field=pre answer=20 text='Add them: 14 + 6 ='

bronze[4] Q: 69Diagram not drawn accurately\(A = bh\). Find \(A\) when \(b = 6\), \(h = 9\).
   step0 field=pre answer=60 text='First 6 × 10 ='
   step1 field=pre answer=6 text='Then 6 × 1 ='
   step2 field=pre answer=54 text='6 × 9 = 60 − 6 ='

gold[0] Q: \(v^2 = u^2 + 2as\). Make \(s\) the subject. Which is correct?

gold[2] Q: Make \(x\) the subject of \(y = \frac{x + 3}{x - 1}\). Which is correct?
