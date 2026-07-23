# apply-pack: algebra__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[6] step 2 | What is left: 150 − 120 = 30, and 30 ÷ 6 = [box=5] | fix: Separate the two: 'Now find what is left: 150 − 120 = 30. Then 30 ÷ 6 = [5].'
- [low] silver[2] | Substitute x = −3, in brackets: 2 × (−3)² + 1. BIDMAS: the power first, before t | fix: Rephrase to: "the power first, before you multiply by 2."
- [low] gold[4] | Times the last −1: (−8) × (−1) = | fix: Rephrase to name the value: "Now multiply by c = −1: (−8) × (−1) =".

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[6] Q: If \(s = \frac{d}{t}\), find \(s\) when \(d = 150\) and \(t = 6\)
   step0 field=pre answer=120 text='Build up 150 ÷ 6. First, 6 × 20 ='
   step1 field=pre answer=5 text='What is left: 150 − 120 = 30, and 30 ÷ 6 ='
   step2 field=pre answer=25 text='So s = 20 + 5 ='
   step3 field=pre answer=150 text='Check: 6 × 25 ='

gold[4] Q: If \(y = 3x^2 - 5\), find the positive value of \(x\) when \(y = 43\)
   step0 field=pre answer=48 text='Substitute y = 43: 43 = 3x² − 5. Add 5 to both sides: 43 + 5 ='
   step1 field=pre answer=16 text='Now 3x² = 48. Divide both sides by 3: x² = 48 ÷ 3 ='
   step2 field=pre answer=4 text='So x² = 16, and the positive root is x = √16 ='
   step3 field=pre answer=43 text='Check: 3 × 4² − 5 = 3 × 16 − 5 = 48 − 5 ='

silver[2] Q: If \(y = 5 - 2x\), find \(x\) when \(y = -3\)
   step0 field=pre answer=-8 text='Substitute y = −3, giving −3 = 5 − 2x. Take 5 from both sides: −3 − 5 ='
   step1 field=pre answer=4 text='Now −8 = −2x. Divide both sides by −2: x = (−8) ÷ (−2) ='
   step2 field=pre answer=-3 text='Check: 5 − 2 × 4 = 5 − 8 ='

### board=maths-edexcel
bronze[6] Q: Find the value of \(6x + y\) when \(x = 3\) and \(y = -4\)
   step0 field=say answer=None text='Substitute x = 3 and y = −4, giving 6 × 3 + (−4). Multiply the 6 × 3 first.'
   step1 field=pre answer=18 text='6 × 3 ='
   step2 field=pre answer=14 text='add y, which is −4: 18 + (−4) ='
   step3 field=pre answer=14 text='Check: 18 with 4 taken off is'

gold[4] Q: Make \(x\) the subject of \(y = \frac{x - 3}{4}\)

silver[2] Q: Find the value of \(2x^2 + 1\) when \(x = -3\)
   step0 field=say answer=None text='Substitute x = −3, in brackets: 2 × (−3)² + 1. BIDMAS: the power first, before the 2 multi'
   step1 field=pre answer=9 text='(−3)² = (−3) × (−3) ='
   step2 field=pre answer=18 text='2 × 9 ='
   step3 field=pre answer=19 text='now add 1: 18 + 1 ='

### board=maths-ocr
bronze[6] Q: If \(a = 3\) and \(b = 4\), find \(a^2 + b^2\)
   step0 field=say answer=None text='Substitute a = 3 and b = 4 into \\(a^2 + b^2\\). Square each letter separately.'
   step1 field=pre answer=9 text='a² = 3 × 3 ='
   step2 field=pre answer=16 text='b² = 4 × 4 ='
   step3 field=pre answer=25 text='Add the two squares: 9 + 16 ='
   step4 field=pre answer=25 text='Check: 3² + 4² ='

gold[4] Q: If \(a = -2\), \(b = 3\), \(c = -1\), find \(b^2 - 4ac\)
   step0 field=say answer=None text='Substitute a = −2, b = 3, c = −1 into \\(b^2 - 4ac\\).'
   step1 field=pre answer=9 text='Square b: 3² ='
   step2 field=pre answer=-8 text='Start 4ac: 4 × (−2) ='
   step3 field=pre answer=8 text='Times the last −1: (−8) × (−1) ='
   step4 field=pre answer=1 text='Subtract: 9 − 8 ='
   step5 field=pre answer=1 text='Check: 3² − 4(−2)(−1) = 9 − 8 ='

silver[2] Q: Make \(x\) the subject: \(y = 4x + 7\)

### board=maths-eduqas
bronze[6] Q: \(v = u + at\). Find \(v\) when \(u = 10\), \(a = 2\), \(t = 3\).
   step0 field=pre answer=6 text='Work out a × t: 2 × 3 ='
   step1 field=pre answer=16 text='Add u: 10 + 6 ='
   step2 field=pre answer=3 text='Check by reversing: (16 − 10) ÷ 2 ='

gold[4] Q: \(T = 2\pi\sqrt{\frac{l}{g}}\). Make \(l\) the subject. Which is correct?

silver[2] Q: \(v = u + at\). Make \(t\) the subject. Which is correct?
