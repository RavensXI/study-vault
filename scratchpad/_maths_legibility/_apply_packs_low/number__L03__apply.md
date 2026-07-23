# apply-pack: number__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[4] | Put 3 decimal places into 360, then write it simplified. [box=0.36] | fix: Replace 'then write it simplified' with 'then remove the trailing zero', e.g. '0.360 — write it as 0.36.'
- [low] bronze[6] | Divide the denominator 10 by the common factor 2. [box=5] | fix: Flag the detour, e.g. 'First simplify the fraction. 2 divides both 4 and 10 — divide the denominator 10 by 2 (you'll give the numerator at the end).'
- [low] bronze[6] | Tenths: after lending one, 6 − 3 = [box=3] | fix: Keep one term and show the change: 'Tenths: the 7 became 6 after the borrow, so 6 − 3 = [3]'.
- [low] gold[1] step 1 (box=49) | Round 48.6 to the nearest square number: | fix: Add a reminder in the step, e.g. 'Square numbers are 1, 4, 9, 16, 25, 36, 49, 64… The nearest one to 48.6 is' [box=49].
- [low] gold[1] first step (box=49) | Round 48.6 to the nearest square number: [box=49] | fix: Add the scaffold before the box, e.g. 'The square numbers near 48.6 are 36 (6×6) and 49 (7×7). 48.6 is closer to 49, so round to [box=49].'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[6] Q: Write \(0.4\) as a fraction in its simplest form. Give the numerator.
   step0 field=say answer=None text='We are writing \\(0.4\\) as a fraction in its simplest form.'
   step1 field=pre answer=4 text='0.4 is 4 tenths, so write it as a fraction over 10. Write the top number.'
   step2 field=pre answer=5 text='Divide the denominator 10 by the common factor 2.'
   step3 field=pre answer=2 text='Divide the numerator 4 by the same factor 2. Write the simplest numerator.'

gold[1] Q: Estimate \(\dfrac{61.3 + 38.9}{0.052}\) by rounding to 1 s.f.
   step0 field=say answer=None text='We are estimating \\(\\dfrac{61.3 + 38.9}{0.052}\\) by rounding to 1 significant figure.'
   step1 field=pre answer=60 text='Round 61.3 to 1 significant figure.'
   step2 field=pre answer=40 text='Round 38.9 to 1 significant figure.'
   step3 field=pre answer=0.05 text='Round 0.052 to 1 significant figure. Type it as a decimal.'
   step4 field=pre answer=100 text='Work out the top: 60 plus 40.'
   step5 field=pre answer=2000 text='Divide by 0.05. Write the estimate.'

silver[4] Q: Calculate \(2.4 \times 0.15\)
   step0 field=say answer=None text='We are working out \\(2.4 \\times 0.15\\).'
   step1 field=pre answer=360 text='Ignore the points and multiply: 24 times 15.'
   step2 field=pre answer=3 text='Count the decimal places: 2.4 has 1 and 0.15 has 2. Write the total.'
   step3 field=pre answer=0.36 text='Put 3 decimal places into 360, then write it simplified.'

### board=maths-edexcel
bronze[6] Q: \(5.7 - 2.35\)
   step0 field=say answer=None text='Subtracting decimals: line up the points and write 5.7 as 5.70. Work right to left, borrow'
   step1 field=pre answer=5 text='Hundredths: borrow to make 10 − 5 ='
   step2 field=pre answer=3 text='Tenths: after lending one, 6 − 3 ='
   step3 field=pre answer=3 text='Units: 5 − 2 ='
   step4 field=pre answer=3.35 text='So 5.70 − 2.35 ='
   step5 field=pre answer=5.7 text='Check by adding back: 3.35 + 2.35 ='

gold[1] Q: \(0.07 \times 0.004\)
   step0 field=say answer=None text='Multiplying small decimals: multiply the non-zero digits, then count every decimal place a'
   step1 field=pre answer=28 text='Ignore the points: 7 × 4 ='
   step2 field=pre answer=5 text='Decimal places: 0.07 has 2 and 0.004 has 3, giving a total of'
   step3 field=pre answer=0.00028 text='Place the point 5 digits from the right of 28, giving'
   step4 field=pre answer=3 text='Check: how many zeros sit after the point before the 28?'

silver[4] Q: \(2.4 \times 0.3\)
   step0 field=say answer=None text='Multiplying decimals: multiply as whole numbers first, then count the total decimal places'
   step1 field=pre answer=72 text='Ignore the points: 24 × 3 ='
   step2 field=pre answer=2 text='Total decimal places: 2.4 has 1 and 0.3 has 1, giving'
   step3 field=pre answer=0.72 text='72 with 2 decimal places is'
   step4 field=pre answer=0.6 text='Check the size: 2.4 is about 2, and 2 × 0.3 ='

### board=maths-ocr
bronze[6] Q: Round \(0.0638\) to 1 significant figure
   step0 field=say answer=None text='Leading zeros are not significant. Significant figures start at the first non-zero digit.'
   step1 field=pre answer=6 text='The first significant figure of 0.0638 is:'
   step2 field=pre answer=3 text='The deciding digit, the next one along, is:'
   step3 field=pre answer=0.06 text='3 is less than 5, so round down and keep the 6. Type 0.0638 to 1 s.f.:'
   step4 field=pre answer=0.06 text='Confirm the answer:'

gold[1] Q: Calculate \(0.24 \times 0.15\)
   step0 field=say answer=None text='First multiply as whole numbers, ignoring the decimal points.'
   step1 field=pre answer=360 text='24 × 15 ='
   step2 field=pre answer=4 text='Count the decimal places: 0.24 has 2, 0.15 has 2, so the total is:'
   step3 field=pre answer=0.036 text='Put the point 4 places from the right of 360, using a leading zero. Type 0.24 × 0.15:'
   step4 field=pre answer=0.036 text='Check the size: 0.24 and 0.15 are both under 1, so the product is small. Type 0.036:'

silver[4] Q: Calculate \(4.7 \times 0.3\)
   step0 field=say answer=None text='First multiply as whole numbers, ignoring the decimal points.'
   step1 field=pre answer=141 text='47 × 3 ='
   step2 field=pre answer=2 text='Count the decimal places: 4.7 has 1, 0.3 has 1, so the total is:'
   step3 field=pre answer=1.41 text='Put the point 2 places from the right of 141. Type 4.7 × 0.3:'
   step4 field=pre answer=1.41 text='Check the size: 4.7 is near 5, and 5 × 0.3 = 1.5, close to 1.41. Type 1.41:'

### board=maths-eduqas
bronze[6] Q: \(0.6 \times 0.3\)
   step0 field=pre answer=18 text='Ignore the decimals for now. Multiply the digits: 6 × 3 ='
   step1 field=pre answer=2 text='Count the decimal places in the question: 0.6 has 1 and 0.3 has 1, so altogether'
   step2 field=pre answer=0.18 text='Put 2 decimal places into 18: that gives 0.18, so type'
   step3 field=pre answer=0.15 text='Check: half of 0.3 is 0.15, and 0.18 sits just above it, a sensible size. Half of 0.3 ='

gold[1] Q: Estimate \(\dfrac{\sqrt{48.6}}{0.21}\). Round 48.6 to the nearest square number and 0.21 t
   step0 field=pre answer=49 text='Round 48.6 to the nearest square number:'
   step1 field=pre answer=7 text='Take the square root: √49 ='
   step2 field=pre answer=0.2 text='Round 0.21 to 1 significant figure:'
   step3 field=pre answer=35 text='Dividing by 0.2 is the same as multiplying by 5, so 7 ÷ 0.2 ='
   step4 field=pre answer=7 text='Check: 35 × 0.2 ='

silver[4] Q: \(7.2 \div 0.09\)
   step0 field=pre answer=9 text='Scale both numbers so the divisor is a whole number. The divisor 0.09 has two decimal plac'
   step1 field=pre answer=720 text='Do the same to 7.2: 7.2 × 100 ='
   step2 field=pre answer=80 text='Now divide the whole numbers: 720 ÷ 9 ='
   step3 field=pre answer=7.2 text='Check: multiply back 80 × 0.09 ='
