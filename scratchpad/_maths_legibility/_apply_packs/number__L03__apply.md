# apply-pack: number__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[4] | The greatest 3 decimal place value below 3.48 is? [box=3.479] | fix: Rewrite step 3 as a full instruction, e.g. 'Any number up to but not including 3.48 truncates to 3.47. Write the largest 3-decimal-place number below 3.48.' Rew
- [medium] gold[3] | 62 sits between 49 and 64, close to 64. Using a calculator, write the root of 62 | fix: Keep one method. Either drop 'Using a calculator' and guide the estimate ('closer to 8 than 7, so try 7.9 — check 7.9×7.9'), or state up front this is a calcula
- [medium] bronze[4] | intro: The 9 rounds up, so it becomes 10 and carries into the whole number. (app | fix: Move the carry explanation to AFTER the decider box, e.g. ask for the decider (5) first, then intro 'The decider is 5, so the 9 rounds up to 10 and carries into
- [medium] silver[6] | The perfect square just below 83 is 81, which is [box=9] ... The perfect square  | fix: State the operation, e.g. '...is 81, and the square root of 81 is [9]' and '...is 100, and √100 = [10]'.
- [medium] gold[2] final check step | Check: 25 hundredths is a quarter. Dividing 25 by 25 gives the top of that quart | fix: Replace with a plain sanity check, e.g. 'Check: 0.25 is the same as one quarter. A quarter of 4 is 1, so type' [box=1] — or drop this check entirely and confirm
- [medium] gold[2] final step (box=1) | Check: 25 hundredths is a quarter. Dividing 25 by 25 gives the top of that quart | fix: Rewrite the check plainly, e.g. 'Check: 0.25 is the same as one quarter (1/4), which is a sensible size. As a fraction of 1, that quarter has 1 on top: 25 ÷ 25 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[4] Q: Round \(34.95\) to 1 decimal place
   step0 field=say answer=None text='We are rounding \\(34.95\\) to 1 decimal place.'
   step1 field=pre answer=9 text='Write the digit in the first decimal place.'
   step2 field=pre answer=5 text='Write the next digit to the right, the decider.'
   step3 field=pre answer=35 text='The 9 rounds up and carries. Write the number to 1 decimal place.'

gold[2] Q: Calculate \(0.12^2\)
   step0 field=say answer=None text='We are working out \\(0.12^2\\).'
   step1 field=pre answer=144 text='Ignore the point and multiply: 12 times 12.'
   step2 field=pre answer=4 text='0.12 has 2 decimal places. Squaring adds them: 2 plus 2. Write the number of decimal place'
   step3 field=pre answer=0.0144 text='Put 4 decimal places into 144. Write the answer.'

gold[3] Q: Estimate \(\sqrt{62}\) to 1 decimal place
   step0 field=say answer=None text='We are estimating \\(\\sqrt{62}\\) to 1 decimal place.'
   step1 field=pre answer=49 text='Which whole number squared is just below 62? Try 7: work out 7 times 7.'
   step2 field=pre answer=64 text='Now work out 8 times 8.'
   step3 field=pre answer=7.9 text='62 sits between 49 and 64, close to 64. Using a calculator, write the root of 62 to 1 deci'

gold[4] Q: A number \(x\) is truncated to 2 d.p. to give \(3.47\). What is the greatest possible valu
   step0 field=say answer=None text='A number \\(x\\) truncates to 2 decimal places to give \\(3.47\\). We want the greatest \\(x\\) '
   step1 field=pre answer=3.47 text='Truncating keeps 3.47 as long as x begins 3.47. Write the smallest such x to 2 decimal pla'
   step2 field=pre answer=3.48 text='x must stay below the next value up. Write that upper limit to 2 decimal places.'
   step3 field=pre answer=3.479 text='The greatest 3 decimal place value below 3.48 is?'

silver[6] Q: Round \(49\,750\) to 2 significant figures
   step0 field=say answer=None text='We are rounding \\(49\\,750\\) to 2 significant figures.'
   step1 field=pre answer=9 text='Write the 2nd significant figure of 49750.'
   step2 field=pre answer=7 text='Write the next digit, the decider.'
   step3 field=pre answer=50000 text='The 9 rounds up and carries. Keep place value with zeros. Write the number.'

### board=maths-edexcel
bronze[4] Q: Round \(0.562\) to 1 significant figure
   step0 field=say answer=None text='Rounding to 1 significant figure. The first significant figure is the first non-zero digit'
   step1 field=pre answer=5 text='The 1st significant figure of 0.562 is'
   step2 field=pre answer=6 text='The deciding digit after it is'
   step3 field=pre answer=6 text='5 rounds up to'
   step4 field=pre answer=0.6 text='0.562 to 1 significant figure is'
   step5 field=pre answer=0.038 text='Check: 0.6 − 0.562 ='

gold[2] Q: \(4.56 \div 0.08\)
   step0 field=say answer=None text='Dividing by a decimal: multiply BOTH numbers by the same power of 10 to make the divisor a'
   step1 field=pre answer=8 text='To turn 0.08 into a whole number, multiply both by 100. 0.08 × 100 ='
   step2 field=pre answer=456 text='And 4.56 × 100 ='
   step3 field=pre answer=57 text='456 ÷ 8 ='
   step4 field=pre answer=4.56 text='Check by multiplying back: 57 × 0.08 ='

gold[3] Q: Round \(0.009 950\) to 3 significant figures
   step0 field=say answer=None text='Rounding to 3 significant figures. Leading zeros are not significant, so start at the firs'
   step1 field=pre answer=5 text='The three significant figures of 0.009950 are 9, 9 and'
   step2 field=pre answer=0 text='The deciding digit after the last 5 is'
   step3 field=pre answer=5 text='The 5 stays as'
   step4 field=pre answer=0.00995 text='So 0.009950 to 3 significant figures is'
   step5 field=pre answer=3 text='Check: how many significant figures does 0.00995 have?'

gold[4] Q: Estimate \(\frac{\sqrt{99} + 4.1^2}{1.97}\)
   step0 field=say answer=None text='Estimating a calculation with a root and a square: round each part to something easy, then'
   step1 field=pre answer=10 text='√99 is very close to √100, which is'
   step2 field=pre answer=16 text='4.1 squared is about 4 squared, which is'
   step3 field=pre answer=2 text='1.97 to 1 significant figure is'
   step4 field=pre answer=26 text='The top first: 10 + 16 ='
   step5 field=pre answer=13 text='Now divide by 2: 26 ÷ 2 ='
   step6 field=pre answer=26 text='Check by multiplying back: 13 × 2 ='

silver[6] Q: Estimate \(\sqrt{83}\)
   step0 field=say answer=None text='Estimating a square root: find the perfect squares either side, then see which one 83 is c'
   step1 field=pre answer=9 text='The perfect square just below 83 is 81, which is'
   step2 field=pre answer=10 text='The perfect square just above 83 is 100, which is'
   step3 field=pre answer=9 text='Since 83 is very close to 81, √83 is about'
   step4 field=pre answer=81 text='Check: 9 × 9 ='

### board=maths-ocr
bronze[4] Q: Round \(347\) to 1 significant figure
   step0 field=say answer=None text='1 significant figure keeps only the first non-zero digit.'
   step1 field=pre answer=3 text='The first significant figure of 347 is:'
   step2 field=pre answer=4 text='The deciding digit, the next one along, is:'
   step3 field=pre answer=300 text='4 is less than 5, so round down and keep the 3, with zeros holding the place. Type 347 to '
   step4 field=pre answer=300 text='Confirm the answer:'

gold[2] Q: Round \(0.9955\) to 2 significant figures
   step0 field=say answer=None text='2 significant figures keeps the first two non-zero digits.'
   step1 field=pre answer=5 text='The first two significant figures of 0.9955 are 9 and 9. The deciding digit (next) is:'
   step2 field=pre answer=1 text='5 rounds up, so 99 rolls over to 100. Type 0.9955 rounded to 2 s.f.:'
   step3 field=pre answer=1 text='Check: 0.9955 is just under 1, and rounding pushes it up to 1.0. Type 1:'

gold[3] Q: Estimate \(\frac{398 \times 0.52}{19.7}\)
   step0 field=say answer=None text='Estimate every number to 1 significant figure.'
   step1 field=pre answer=400 text='398 to 1 s.f. is:'
   step2 field=pre answer=0.5 text='0.52 to 1 s.f. is:'
   step3 field=pre answer=200 text='So the top is about 400 × 0.5 ='
   step4 field=pre answer=20 text='19.7 to 1 s.f. is:'
   step5 field=pre answer=10 text='Now divide: 200 ÷ 20 ='
   step6 field=pre answer=10 text='Check: 10 × 20 = 200, matching the top. Type the estimate 10:'

gold[4] Q: Calculate \(2.56 \div 0.08\)
   step0 field=say answer=None text='Make the divisor a whole number by multiplying both numbers by 100.'
   step1 field=pre answer=256 text='2.56 × 100 ='
   step2 field=pre answer=8 text='0.08 × 100 ='
   step3 field=pre answer=32 text='Now divide whole numbers: 256 ÷ 8 ='
   step4 field=pre answer=32 text='Check: 32 × 0.08 = 2.56, matching the start. Type 32:'

silver[6] Q: Estimate \(\sqrt{53}\) to the nearest integer
   step0 field=say answer=None text='Find the two square numbers that 53 sits between.'
   step1 field=pre answer=49 text='7² ='
   step2 field=pre answer=64 text='8² ='
   step3 field=pre answer=4 text='53 lies between 49 and 64. The gap down to 49 is 53 − 49 ='
   step4 field=pre answer=11 text='The gap up to 64 is 64 − 53 ='
   step5 field=pre answer=7 text='4 is less than 11, so 53 is nearer 49. The nearest integer to √53 is:'

### board=maths-eduqas
bronze[4] Q: \(3.6 + 2.45\)
   step0 field=pre answer=5 text='Line up the decimal points. Write 3.6 as 3.60 so both have two decimal places. Add the hun'
   step1 field=pre answer=10 text='Add the tenths: 6 + 4 ='
   step2 field=pre answer=6 text='That is 10 tenths: write 0, carry 1 to the units. Add the units with the carry: 3 + 2 + 1 '
   step3 field=pre answer=6.05 text='Put it together: 6 units, 0 tenths, 5 hundredths gives 6.05, so type'
   step4 field=pre answer=3.6 text='Check: subtract back 6.05 − 2.45 ='

gold[2] Q: \(0.3^2 + 0.4^2\)
   step0 field=pre answer=9 text='Square the first: 0.3² means 0.3 × 0.3. Ignoring decimals, 3 × 3 ='
   step1 field=pre answer=16 text='With 2 decimal places that is 0.09. Now square the second: 0.4 × 0.4, and 4 × 4 ='
   step2 field=pre answer=0.25 text='With 2 decimal places that is 0.16. Add the two results: 0.09 + 0.16 ='
   step3 field=pre answer=1 text='Check: 25 hundredths is a quarter. Dividing 25 by 25 gives the top of that quarter: 25 ÷ 2'

gold[3] Q: Estimate \(\dfrac{6.2^2}{0.31}\) to 1 significant figure.
   step0 field=pre answer=6 text='Round 6.2 to 1 significant figure:'
   step1 field=pre answer=36 text='Square it: 6² = 6 × 6 ='
   step2 field=pre answer=0.3 text='Round 0.31 to 1 significant figure:'
   step3 field=pre answer=120 text='Now 36 ÷ 0.3. Scaling both by 10 gives 360 ÷ 3 ='
   step4 field=pre answer=36 text='Check: 120 × 0.3 ='

gold[4] Q: \(1.2 \times 3.5 \div 0.07\)
   step0 field=pre answer=4.2 text='Work left to right. First 1.2 × 3.5 ='
   step1 field=pre answer=7 text='Now divide by 0.07. Scale both by 100 so the divisor is a whole number. 0.07 × 100 ='
   step2 field=pre answer=420 text='Do the same to 4.2: 4.2 × 100 ='
   step3 field=pre answer=60 text='Now divide the whole numbers: 420 ÷ 7 ='
   step4 field=pre answer=4.2 text='Check: multiply back 60 × 0.07 ='

silver[6] Q: Round \(0.06049\) to 3 significant figures.
   step0 field=pre answer=6 text='Leading zeros do not count. The first significant figure is'
   step1 field=pre answer=4 text='The next two significant figures are 0 and'
   step2 field=pre answer=9 text='The deciding digit is the next one along:'
   step3 field=pre answer=5 text='9 is 5 or more, so round the kept 4 up. 4 + 1 ='
   step4 field=pre answer=0.0605 text='Keeping the place value, the number is 0.0605, so type'
