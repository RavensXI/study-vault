# apply-pack: graphs__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[3] step 3 | Divide the second by the first: the a cancels, so b = 24 ÷ 3 = 8 | fix: Add a bridging line: 'On top you have a×b², on the bottom a×b. The a's cancel and one b cancels, leaving b on the left. So b = 24 ÷ 3.'
- [medium] bronze[5], step 2 | See the trap route: 3 × 2 = [box=6, NO label] | fix: Name the error plainly: 'A common mistake is to multiply 3 × 2 instead of 3 × 3. Work out that wrong route: 3 × 2 =' (box stays NO label — it is a plain number)

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[5] Q: For \(y = 3^x\), find \(y\) when \(x = 0\).
   step0 field=say answer=None text='Let us build down the powers of 3 to see what 3⁰ must be.'
   step1 field=pre answer=9 text='3² = 3 × 3 ='
   step2 field=pre answer=3 text='3¹ ='
   step3 field=pre answer=1 text='Each step down divides by 3, so 3⁰ = 3 ÷ 3 ='
   step4 field=pre answer=1 text='So any base to the power 0 equals'

gold[3] Q: For \(y = 10^x\), find \(y\) when \(x = -1\).
   step0 field=say answer=None text='A negative power means take the reciprocal, that is 1 over the positive power.'
   step1 field=pre answer=10 text='Positive power first: 10¹ ='
   step2 field=pre answer=0.1 text='Reciprocal: 1 ÷ 10 ='
   step3 field=pre answer=0.1 text='So 10⁻¹ ='

### board=maths-edexcel
bronze[5] Q: Is the gradient of \(y = x^3\) positive or negative at \(x = 1\)?

gold[3] Q: A curve passes through (1, 3) and (2, 24). It has equation \(y = a \times b^x\). Find the 
   step0 field=say answer=None text='Substitute both points into \\(y = a \\times b^x\\) to get two facts.'
   step1 field=pre answer=3 text='At x = 1: a × b ='
   step2 field=pre answer=24 text='At x = 2: a × b² ='
   step3 field=pre answer=8 text='Divide the second by the first: the a cancels, so b = 24 ÷ 3 ='
   step4 field=pre answer=3 text='Check with the first point: a = 3 ÷ 8 = 0.375, and a × b = 0.375 × 8 ='

### board=maths-ocr
bronze[5] Q: Which graph type has asymptotes at \(x = 0\) and \(y = 0\)?

gold[3] Q: For \(y = 10 \times 0.8^x\), find \(y\) when \(x = 1\).
   step0 field=say answer=None text='The base 0.8 is below 1, so this is decay. At x = 1 you only need 0.8¹.'
   step1 field=pre answer=0.8 text='0.8 to the power 1 is just'
   step2 field=pre answer=8 text='Multiply by 10: 10 × 0.8 ='
   step3 field=pre answer=8 text='Check it fell from the start value: it began at 10 and dropped to'

### board=maths-eduqas
bronze[5] Q: For \(y = 3^x\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text='A power of 2 means multiply the base by itself once.'
   step1 field=pre answer=9 text='Write it out: 3 × 3 ='
   step2 field=pre answer=6 text='See the trap route: 3 × 2 ='
   step3 field=pre answer=9 text='The power route is correct, so type the real y:'

gold[3] Q: For \(y = 2^x\), find \(y\) when \(x = -3\).
   step0 field=say answer=None text='A negative power means the reciprocal: 2⁻³ = 1 over 2³.'
   step1 field=pre answer=8 text='Work out the positive power 2³: 2 × 2 × 2 ='
   step2 field=pre answer=8 text='The reciprocal is 1 over that. Type the bottom number of the fraction:'
   step3 field=pre answer=1 text='And the top number of the fraction is'
