# apply-pack: number__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] bronze[0] | Rewrite \(\frac{1}{4}\) over 12. Its new top is [box=3] | fix: Add a bridging line before the ask, e.g. '12 ÷ 4 = 3, so multiply the top by 3: 1 × 3 = ___', mirroring how the mixed-number steps spell out 'top = a × b + c'.
- [medium] silver[1] | The lowest common denominator of 6 and 8 is [box=24] | fix: Add a one-line method, e.g. 'The LCD is the smallest number both 6 and 8 divide into — count 8, 16, 24: 24 works for both. (It is not always the two bottoms mul
- [medium] bronze[0] | Rewrite \frac{1}{4} over 12. Its new top is [box=3] | fix: Add a sub-step showing the multiplier before asking for the new top, e.g. 'To get from 4 to 12 you multiply by 12 ÷ 4 = 3, so the new top is 1 × 3 = ___'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: \(\frac{1}{4} + \frac{1}{3}\)
   step0 field=say answer=None text='Add and subtract fractions only when the bottoms match. First make them match.'
   step1 field=pre answer=12 text='The lowest common denominator of 4 and 3 is'
   step2 field=pre answer=3 text='Rewrite \\(\\frac{1}{4}\\) over 12. Its new top is'
   step3 field=pre answer=4 text='Rewrite \\(\\frac{1}{3}\\) over 12. Its new top is'
   step4 field=pre answer=7 text='Now add the tops over 12: 3 + 4 ='
   step5 field=pre answer=7 text='\\(\\frac{7}{12}\\) is already in lowest terms. The final top is'
   step6 field=pre answer=12 text='and the final bottom is'
   step7 field=say answer=None text='Quick check: \\(\\frac{7}{12}\\) is the answer, in lowest terms.'

silver[1] Q: \(\frac{5}{6} - \frac{3}{8}\)
   step0 field=say answer=None text='Add and subtract fractions only when the bottoms match. First make them match.'
   step1 field=pre answer=24 text='The lowest common denominator of 6 and 8 is'
   step2 field=pre answer=20 text='Rewrite \\(\\frac{5}{6}\\) over 24. Its new top is'
   step3 field=pre answer=9 text='Rewrite \\(\\frac{3}{8}\\) over 24. Its new top is'
   step4 field=pre answer=11 text='Now subtract the tops over 24: 20 − 9 ='
   step5 field=pre answer=11 text='\\(\\frac{11}{24}\\) is already in lowest terms. The final top is'
   step6 field=pre answer=24 text='and the final bottom is'
   step7 field=say answer=None text='Quick check: \\(\\frac{11}{24}\\) is the answer, in lowest terms.'

### board=maths-edexcel
bronze[0] Q: \(\frac{1}{3} + \frac{1}{6}\)
   step0 field=pre answer=6 text='The lowest number both 3 and 6 divide into is the common denominator. It is'
   step1 field=pre answer=2 text='Convert 1/3 into sixths. 3 goes into 6 twice, so the new top is'
   step2 field=say answer=None text='The second fraction, 1/6, is already in sixths.'
   step3 field=pre answer=3 text='Now add the tops: 2 + 1 ='
   step4 field=pre answer=1 text='That gives 3/6. Simplify by dividing top and bottom by 3. Top: 3 ÷ 3 ='
   step5 field=pre answer=2 text='Bottom: 6 ÷ 3 ='
   step6 field=pre answer=3 text='Check: turn 1/2 back into sixths. 1 × 3 ='

silver[1] Q: \(\frac{2}{3} + \frac{5}{8}\)
   step0 field=pre answer=24 text='The common denominator of 3 and 8 is'
   step1 field=pre answer=16 text='Convert 2/3 into 24ths: 3 goes into 24 eight times, so 2 × 8 ='
   step2 field=pre answer=15 text='Convert 5/8 into 24ths: 8 goes into 24 three times, so 5 × 3 ='
   step3 field=pre answer=31 text='Add the tops: 16 + 15 ='
   step4 field=pre answer=24 text='The denominator stays'
   step5 field=pre answer=16 text='Check: 31 is prime, so 31/24 will not simplify. Subtract back 31 − 15 ='

### board=maths-ocr
bronze[0] Q: \(\frac{1}{4} + \frac{1}{3}\)
   step0 field=say answer=None text='Add fractions only when the bottoms match. First make them match.'
   step1 field=pre answer=12 text='The lowest common denominator of 4 and 3 is'
   step2 field=pre answer=3 text='Rewrite \\(\\frac{1}{4}\\) over 12. Its new top is'
   step3 field=pre answer=4 text='Rewrite \\(\\frac{1}{3}\\) over 12. Its new top is'
   step4 field=pre answer=7 text='Now add the tops over 12: 3 + 4 ='
   step5 field=pre answer=12 text='\\(\\frac{7}{12}\\) is already in lowest terms, so the final bottom stays'
   step6 field=pre answer=3 text='Check by subtracting back: 7 − 4 ='

silver[1] Q: \(\frac{3}{4} - \frac{2}{5}\)
   step0 field=say answer=None text='Subtract fractions only when the bottoms match. Find the common denominator.'
   step1 field=pre answer=20 text='The lowest common denominator of 4 and 5 is'
   step2 field=pre answer=15 text='Rewrite \\(\\frac{3}{4}\\) over 20. Its new top is'
   step3 field=pre answer=8 text='Rewrite \\(\\frac{2}{5}\\) over 20. Its new top is'
   step4 field=pre answer=7 text='Subtract the tops over 20: 15 − 8 ='
   step5 field=pre answer=20 text='\\(\\frac{7}{20}\\) is already in lowest terms, so the final bottom stays'
   step6 field=pre answer=15 text='Check by adding back: 7 + 8 ='

### board=maths-eduqas
bronze[0] Q: \(\frac{1}{4} + \frac{1}{3}\)
   step0 field=pre answer=12 text='The common denominator of 4 and 3 is'
   step1 field=pre answer=3 text='Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 ='
   step2 field=pre answer=4 text='Convert 1/3 into twelfths: 3 goes into 12 four times, so 1 × 4 ='
   step3 field=pre answer=7 text='Add the tops: 3 + 4 ='
   step4 field=pre answer=12 text='The denominator stays'
   step5 field=pre answer=3 text='Check: 7 and 12 share no factor, so 7/12 is simplest. Subtract back 7 − 4 ='

silver[1] Q: \(\frac{4}{5} \times \frac{5}{8}\)
   step0 field=pre answer=20 text='Multiply the tops: 4 × 5 ='
   step1 field=pre answer=40 text='Multiply the bottoms: 5 × 8 ='
   step2 field=pre answer=1 text='That gives 20/40. Simplify by dividing top and bottom by 20. Top: 20 ÷ 20 ='
   step3 field=pre answer=2 text='Bottom: 40 ÷ 20 ='
   step4 field=pre answer=20 text='Check: turn 1/2 back up by 20. 1 × 20 ='
