# apply-pack: number__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[2] | Confirm the sign: the answer is positive (1/25), never −25. Type the denominator | fix: Split the guard from the ask: 'The answer stays positive: 1/25, not −25. Type the denominator: 25.'
- [low] bronze[3] | Check by taking one lot back off: 7 − 5 = | fix: Reword concretely, e.g. "Check by removing the second term's number: 7 − 5 =" so it is clear you are subtracting the 5 to get back to the original 2.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: Simplify \(5^{-2}\). Give the denominator of the fraction.
   step0 field=say answer=None text='A negative power does not make a negative number. It flips to one over the positive power:'
   step1 field=pre answer=25 text='First work out the positive power 5 squared: 5 × 5.'
   step2 field=pre answer=25 text='So \\(5^{-2} = \\frac{1}{25}\\). Write the denominator of that fraction.'
   step3 field=pre answer=25 text='Confirm the sign: the answer is positive (1/25), never −25. Type the denominator again.'

bronze[3] Q: Simplify \(\sqrt{50}\). The answer is \(a\sqrt{2}\). Find \(a\).
   step0 field=say answer=None text='To simplify a surd, split off the largest square factor.'
   step1 field=pre answer=2 text='The largest square factor of 50 is 25. Work out 50 ÷ 25.'
   step2 field=pre answer=5 text='So 50 = 25 × 2 and \\(\\sqrt{50} = \\sqrt{25} \\times \\sqrt{2}\\). Work out √25.'
   step3 field=pre answer=5 text='So \\(\\sqrt{50} = 5\\sqrt{2}\\). Write a.'

### board=maths-edexcel
bronze[2] Q: Evaluate \(3^{-2}\)
   step0 field=say answer=None text='A negative power flips it: \\(3^{-2} = \\frac{1}{3^{2}}\\).'
   step1 field=pre answer=9 text='First the bottom: 3² = 3 × 3 ='
   step2 field=pre answer=1 text='The flip puts 1 on top. Numerator ='
   step3 field=pre answer=9 text='Denominator ='

bronze[3] Q: Simplify \(\sqrt{50}\). Enter the number in front of \(\sqrt{2}\).
   step0 field=say answer=None text='Look for the biggest square number that divides 50. That is 25, and \\(25 = 5^2\\).'
   step1 field=pre answer=2 text='Split it: 50 = 25 ×'
   step2 field=pre answer=5 text='√25 ='
   step3 field=pre answer=50 text='So √50 = 5√2. Rebuild to check: 5 × 5 × 2 ='

### board=maths-ocr
bronze[2] Q: Simplify \(\sqrt{75}\)
   step0 field=pre answer=25 text='The largest square number that divides 75 is'
   step1 field=pre answer=3 text='75 ÷ 25 ='
   step2 field=say answer=None text='So \\(\\sqrt{75} = \\sqrt{25} \\times \\sqrt{3}\\).'
   step3 field=pre answer=5 text='\\(\\sqrt{25}\\) ='
   step4 field=pre answer=5 text='So \\(\\sqrt{75}\\) ='
   step5 field=pre answer=75 text='Check: 5² × 3 ='

bronze[3] Q: Simplify \(2\sqrt{3} + 5\sqrt{3}\)
   step0 field=pre answer=7 text='Both terms are lots of √3, so add the numbers in front: 2 + 5 ='
   step1 field=say answer=None text='The √3 stays the same. You never add the numbers under the root.'
   step2 field=pre answer=7 text='So the total is'
   step3 field=pre answer=2 text='Check by taking one lot back off: 7 − 5 ='

### board=maths-eduqas
bronze[2] Q: Simplify \((2^4)^2\). Give the power of 2.
   step0 field=say answer=None text='A power raised to a power MULTIPLIES the indices: \\((2^{4})^{2}=2^{4\\times2}\\).'
   step1 field=pre answer=16 text='First work out 2⁴ ='
   step2 field=pre answer=8 text='Now (2⁴)² = 16², and as a power of 2 the index is 4 × 2 ='
   step3 field=pre answer=256 text='Check: 16² = 256 and 2⁸ ='

bronze[3] Q: Evaluate \(49^{\frac{1}{2}}\).
   step0 field=say answer=None text='A power of a half means a square root, so read \\(49^{1/2}\\) as \\(\\sqrt{49}\\).'
   step1 field=pre answer=49 text='Which number squared makes 49? Try 7: 7 × 7 ='
   step2 field=pre answer=7 text='That lands on 49, so √49 ='
   step3 field=pre answer=49 text='Check by squaring: 7 × 7 ='
