# apply-pack: number__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] bronze[2] | 12 lands on 144, so write \(\sqrt{144}\). [box=12, NO label] | fix: Reword to: '12 × 12 = 144, so √144 = 12. Enter 12.'
- [medium] bronze[3] | 3 cubed lands on 27, so write \(\sqrt[3]{27}\). [box=3, NO label] | fix: Reword to: '3 × 3 × 3 = 27, so ³√27 = 3. Enter 3.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: Calculate \(\sqrt[3]{27}\)
   step0 field=say answer=None text='A cube root asks what number times itself three times gives 27.'
   step1 field=pre answer=8 text='Try 2 × 2 × 2 ='
   step2 field=pre answer=27 text='Try 3 × 3 × 3 ='
   step3 field=pre answer=3 text='3 cubed lands on 27, so write \\(\\sqrt[3]{27}\\).'

bronze[3] Q: Calculate \(2^5\)
   step0 field=say answer=None text='\\(2^5\\) means five 2s multiplied together.'
   step1 field=pre answer=8 text='First three 2s: 2 × 2 × 2 ='
   step2 field=pre answer=16 text='Multiply by the fourth 2: 8 × 2 ='
   step3 field=pre answer=32 text='Multiply by the fifth 2: 16 × 2 ='

### board=maths-edexcel
bronze[2] Q: Calculate \(\sqrt[3]{64}\)
   step0 field=say answer=None text='\\(\\sqrt[3]{64}\\) asks what number cubed (times itself three times) makes 64.'
   step1 field=pre answer=16 text='Try 4. First 4 × 4 ='
   step2 field=pre answer=64 text='Now × 4 again: 16 × 4 ='
   step3 field=pre answer=4 text='That equals 64, so the cube root is'

bronze[3] Q: Write \(56 000\) in standard form
   step0 field=say answer=None text='Standard form is \\(A \\times 10^n\\) with A between 1 and 10. Start with A.'
   step1 field=pre answer=5.6 text='Slide the point left until one digit sits in front. A ='
   step2 field=pre answer=4 text='Count how many places the point moved from 56 000 to 5.6:'
   step3 field=pre answer=4 text='It is a large number, so n is positive. n ='
   step4 field=pre answer=56000 text='Check by expanding: 5.6 × 10 000 ='

### board=maths-ocr
bronze[2] Q: Evaluate \(10^3\)
   step0 field=pre answer=100 text='10 × 10 ='
   step1 field=pre answer=1000 text='Now the third 10: 100 × 10 ='
   step2 field=pre answer=3 text='The power 3 gives this many zeros:'

bronze[3] Q: Evaluate \(\sqrt[3]{27}\)
   step0 field=pre answer=8 text='2 × 2 × 2 ='
   step1 field=pre answer=27 text='3 × 3 × 3 ='
   step2 field=pre answer=3 text='So ∛27 ='

### board=maths-eduqas
bronze[2] Q: \(\sqrt{144}\)
   step0 field=say answer=None text='A square root reverses squaring: it asks what number times itself gives 144.'
   step1 field=pre answer=121 text='Try 11 × 11 ='
   step2 field=pre answer=144 text='Try the next one: 12 × 12 ='
   step3 field=pre answer=12 text='12 lands on 144, so write \\(\\sqrt{144}\\).'

bronze[3] Q: \(\sqrt[3]{27}\)
   step0 field=say answer=None text='A cube root asks what number times itself three times gives 27.'
   step1 field=pre answer=8 text='Try 2 × 2 × 2 ='
   step2 field=pre answer=27 text='Try 3 × 3 × 3 ='
   step3 field=pre answer=3 text='3 cubed lands on 27, so write \\(\\sqrt[3]{27}\\).'
