# apply-pack: algebra__L11.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] gold[4] | intro: "So −8 flips both signs." | fix: Replace with: "So −8 < −2x ≤ 4. Now divide all three parts by −2. Dividing by a negative flips both inequality signs."
- [medium] gold[3] | ask: "Those numbers are +5 and −3. The larger root comes from n − 3 = 0, giving  | fix: Insert before the ask: "So it factorises to (n + 5)(n − 3) ≤ 0. Set each bracket to 0. n − 3 = 0 gives n = 3; n + 5 = 0 gives n = −5."
- [medium] gold[2] | ask: "The left, (2x − 1)/3, times 6 is 2 lots of (2x − 1). The number in front o | fix: Rewrite: "Multiplying (2x − 1)/3 by 6 gives 2(2x − 1) = 4x − 2. The number in front of x (its coefficient) is [box]." Apply the same to the right box (3(x + 2) 
- [high] gold[3] | Solve \(2x + 1 3\). How many integers satisfy both? | fix: Restore the full question so both conditions show: 'Solve 2x + 1 3. How many integers satisfy both?' — escape the (e.g. as \lt / \gt inside the LaTeX) so they d

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: Solve \(2x + 1 > 5\) and \(3x - 4 < 14\) simultaneously. Which is the solution?

gold[3] Q: If \(n\) is a positive integer and \(n^2 < 50\), find the largest possible value of \(n\).
   step0 field=say answer=None text='We need the largest whole number n with \\(n^2 < 50\\). Try n = 7.'
   step1 field=pre answer=49 text='7 × 7 ='
   step2 field=say answer=None text='49 is less than 50, so n = 7 works. Now test n = 8.'
   step3 field=pre answer=64 text='8 × 8 ='
   step4 field=pre answer=7 text='64 is more than 50, so 8 is too big. The largest possible n is'

gold[4] Q: Solve \(-3 < \frac{2x-1}{3} \le 5\). Which list of integer values of \(x\) is correct?

### board=maths-edexcel
gold[2] Q: Solve \(4(2x - 3) < 5x + 6\)

gold[3] Q: Find the largest integer \(n\) such that \(3n + 7 < 28\)
   step0 field=say answer=None text='Solve \\(3n + 7 < 28\\) like an equation. Take 7 off both sides.'
   step1 field=pre answer=21 text='28 − 7 ='
   step2 field=say answer=None text='So \\(3n < 21\\). Divide both sides by 3.'
   step3 field=pre answer=7 text='21 ÷ 3 ='
   step4 field=say answer=None text='So \\(n < 7\\). The symbol is strict, so n = 7 is NOT allowed.'
   step5 field=pre answer=6 text='The largest integer below 7 is'
   step6 field=pre answer=25 text='Check it: 3 × 6 + 7 ='

gold[4] Q: Solve \(2x + 1 > 5\) and \(3x - 4 < 11\). Express the combined solution.

### board=maths-ocr
gold[2] Q: Solve \(\frac{2x-1}{3} \geq \frac{x+2}{2}\). What is the smallest integer?
   step0 field=say answer=None text='Clear both fractions by multiplying every term by 6, the common denominator.'
   step1 field=pre answer=4 text='The left, (2x − 1)/3, times 6 is 2 lots of (2x − 1). The number in front of x is 2 × 2 ='
   step2 field=pre answer=3 text='The right, (x + 2)/2, times 6 is 3 lots of (x + 2). The number in front of x is 3 × 1 ='
   step3 field=say answer=None text='So 4x − 2 ≥ 3x + 6. Subtract 3x from both sides.'
   step4 field=pre answer=1 text='4x − 3x ='
   step5 field=say answer=None text='So x − 2 ≥ 6. Add 2 to both sides.'
   step6 field=pre answer=8 text='6 + 2 ='
   step7 field=say answer=None text='So x ≥ 8. The ≥ includes 8, so the smallest value is 8.'
   step8 field=pre answer=5 text='Check x = 8: left (2×8 − 1)/3 = 15/3 = 5, right (8 + 2)/2 ='

gold[3] Q: Find the integer values of \(n\) where \(n^2 + 2n - 15 \leq 0\). How many are there?
   step0 field=say answer=None text='Factorise the quadratic. Find two numbers that multiply to −15 and add to +2.'
   step1 field=pre answer=3 text='Those numbers are +5 and −3. The larger root comes from n − 3 = 0, giving n ='
   step2 field=pre answer=-5 text='The other root comes from n + 5 = 0, giving n ='
   step3 field=say answer=None text='The parabola opens upward, so it is ≤ 0 BETWEEN the roots: −5 ≤ n ≤ 3. Both ends use ≤, so'
   step4 field=pre answer=9 text='The integers run from −5 to 3. Using 3 − (−5) + 1 ='
   step5 field=pre answer=0 text='Check the top root n = 3: 3² + 2 × 3 − 15 = 9 + 6 − 15 ='

gold[4] Q: Solve \(-5 < 3 - 2x \leq 7\). What is the smallest integer?
   step0 field=say answer=None text='Do every step to all three parts. First subtract 3 from all three.'
   step1 field=pre answer=-8 text='Left: −5 − 3 ='
   step2 field=pre answer=4 text='Right: 7 − 3 ='
   step3 field=say answer=None text='So −8 flips both signs.'
   step4 field=pre answer=4 text='Left becomes: −8 ÷ (−2) ='
   step5 field=pre answer=-2 text='Right becomes: 4 ÷ (−2) ='
   step6 field=say answer=None text='After flipping, the chain reads 4 > x ≥ −2, i.e. −2 ≤ x < 4. The ≤ end means −2 is include'
   step7 field=pre answer=-2 text='Smallest integer value of x ='

### board=maths-eduqas
gold[2] Q: Find the integer values of \(n\) that satisfy \(n^2 \leq 16\). How many?
   step0 field=say answer=None text='\\(n^2 \\leq 16\\) asks which whole numbers, squared, stay at 16 or below.'
   step1 field=pre answer=4 text='The largest n that works: 4² = 16, which is ≤ 16, so the largest is'
   step2 field=say answer=None text='Negatives work too, because squaring cancels the minus: \\((-4)^2 = 16\\).'
   step3 field=pre answer=-4 text='The smallest (most negative) n that fits is'
   step4 field=pre answer=9 text='Count every integer from −4 to 4 inclusive:'

gold[3] Q: Solve \(2x + 1 3\). How many integers satisfy both?
   step0 field=say answer=None text='Solve each inequality on its own, then find the whole numbers that fit both.'
   step1 field=pre answer=1 text='2x + 1 < 3: subtract 1, then divide by 2 to get x <'
   step2 field=pre answer=-2 text='x + 5 > 3: subtract 5 to get x >'
   step3 field=say answer=None text='So x is between −2 and 1, and both ends are strict, so neither is included.'
   step4 field=pre answer=-1 text='The smallest integer greater than −2 is'
   step5 field=pre answer=2 text='Count the integers from −1 up to 0 (1 is excluded):'

gold[4] Q: Solve \(\frac{x}{2} + 1 > 4\). Which is the solution?
