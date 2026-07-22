# apply-pack: algebra__L14.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[3] | Multiply both sides by 2. Left becomes 4x + 2, right becomes x − 1. Gather the x | fix: Split into two steps: first show the multiply-and-expand result ('both sides ×2 gives 4x + 2 = x − 1'), then a separate step 'Gather the x terms: 4x − x = ___'.
- [high] gold[2] step 1 | Under the quadratic-formula root, 5² + 8 = | fix: Add a step before this one that names the quadratic formula and lists a=1, b=−5, c=−2, then show the discriminant explicitly: b²−4ac = (−5)² − 4×1×(−2) = 25 + 8
- [medium] gold[2] step 3 | x = (5 + 5.74) ÷ 2, to 1 d.p. = | fix: Show the formula skeleton first: x = (−b + √(b²−4ac)) / (2a) = (5 + √33) / 2, so the 5 and the ÷2 are justified before the numbers go in.
- [medium] bronze[6] | Q: 14916Find the nth term of \(1, 4, 9, 16, 25, ...\). Which is correct? | fix: Delete the stray '14916' so the stem reads: 'Find the nth term of 1, 4, 9, 16, 25, ... Which is correct?'
- [medium] gold[4] | Subtract \(2n^2\). At n = 1: 5 - 2 x 1 squared = 5 - 2 = [box=3] ... Then n + 2  | fix: Add a bridging step turning the second difference into the coefficient ('4 divided by 2 = 2, so the quadratic part is 2n squared') and derive the linear part ex

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[6] Q: Find the nth term of \(1, 4, 9, 16, 25, ...\)

gold[2] Q: If \(f(x) = x^2 + 1\) and \(g(x) = 2x - 3\), solve \(fg(x) = 5\). Find the larger value of
   step0 field=pre answer=4 text='Subtract 1 from both sides: (2x − 3)² = 5 − 1 ='
   step1 field=pre answer=2 text='Square root both sides: √4 ='
   step2 field=pre answer=2.5 text='The + case: 2x − 3 = 2, so 2x = 5 and x ='
   step3 field=pre answer=0.5 text='The − case: 2x − 3 = −2, 2x = 1, x ='

gold[3] Q: The equation \(x^3 - 3x - 5 = 0\) has a root near \(x = 2\). Use the iteration \(x_{n+1} =
   step0 field=pre answer=11 text='Inside for x₁: 3 × 2 + 5 ='
   step1 field=pre answer=2.224 text='x₁ = cube root of 11, to 3 d.p. ='
   step2 field=pre answer=11.672 text='Inside for x₂: 3 × 2.224 + 5 ='
   step3 field=pre answer=2.268 text='x₂ = cube root of 11.672, to 3 d.p. ='

gold[4] Q: Find the nth term of \(3, 9, 19, 33, 51, ...\)

### board=maths-edexcel
bronze[6] Q: Given \(f(x) = 5x + 2\), find \(f(-1)\)
   step0 field=say answer=None text='\\(f(x) = 5x + 2\\). Find \\(f(-1)\\). Watch the sign.'
   step1 field=pre answer=-5 text='Multiply by 5: 5 × (−1) ='
   step2 field=pre answer=-3 text='Now add 2: −5 + 2 ='
   step3 field=pre answer=-3 text='Check: 5 × (−1) + 2 ='

gold[2] Q: The nth term is \(an^2 + bn + c\). Given T(1)=2, T(2)=7, T(3)=14, find \(a\).
   step0 field=say answer=None text='The nth term is \\(an^2 + bn + c\\). From T(1)=2, T(2)=7, T(3)=14, find \\(a\\). The second di'
   step1 field=pre answer=5 text='First differences: 7 − 2 ='
   step2 field=pre answer=7 text='and 14 − 7 ='
   step3 field=pre answer=2 text='Second difference: 7 − 5 ='
   step4 field=pre answer=1 text='The second difference is 2a, so a = 2 ÷ 2 ='

gold[3] Q: \(f(x) = 2x + 1\). Solve \(f(x) = f^{-1}(x)\).
   step0 field=say answer=None text='\\(f(x) = 2x + 1\\). Solve \\(f(x) = f^{-1}(x)\\). First find the inverse: write \\(y = 2x + 1\\'
   step1 field=pre answer=3 text='Multiply both sides by 2. Left becomes 4x + 2, right becomes x − 1. Gather the x terms: 4x'
   step2 field=pre answer=-3 text='Gather the numbers on the other side: −1 − 2 ='
   step3 field=pre answer=-1 text='So 3x = −3, giving x = −3 ÷ 3 ='
   step4 field=pre answer=-1 text='Check: f(−1) = 2 × (−1) + 1 ='

gold[4] Q: Use \(x_{n+1} = \sqrt[3]{8 - 2x_n}\) with \(x_0 = 1\). Find \(x_3\) to 3 d.p.
   step0 field=say answer=None text='\\(x_{n+1} = \\sqrt[3]{8 - 2x_n}\\), start \\(x_0 = 1\\). Find \\(x_3\\). Three iterations, keepi'
   step1 field=pre answer=6 text='\\(x_1\\): the inside is 8 − 2 × 1 ='
   step2 field=pre answer=1.817 text='Cube root: ∛6 = ___ (3 d.p.)'
   step3 field=pre answer=4.366 text='\\(x_2\\): the inside is 8 − 2 × (full x1) = ___ (3 d.p.)'
   step4 field=pre answer=1.634 text='Cube root: ∛4.366 = ___ (3 d.p.)'
   step5 field=pre answer=4.731 text='\\(x_3\\): the inside is 8 − 2 × (full x2) = ___ (3 d.p.)'
   step6 field=pre answer=1.679 text='Cube root: ∛4.731 = ___ (3 d.p.)'

### board=maths-ocr
bronze[6] Q: The nth term of a quadratic sequence starts \(3n^2\). What is the 2nd difference?
   step0 field=pre answer=3 text='The number in front of n² is a ='
   step1 field=pre answer=6 text='Double it: 2 × 3 ='
   step2 field=pre answer=3 text='Check by halving back: 6 ÷ 2 ='

gold[2] Q: Using \(x_{n+1} = \sqrt{5x_n + 2}\) with \(x_0 = 3\), find the value the sequence converge
   step0 field=pre answer=33 text='Under the quadratic-formula root, 5² + 8 ='
   step1 field=pre answer=5.74 text='√33 to 2 d.p. ='
   step2 field=pre answer=5.4 text='x = (5 + 5.74) ÷ 2, to 1 d.p. ='

gold[3] Q: Find the nth term of \(1, 7, 17, 31, 49, ...\)

gold[4] Q: If \(f(x) = x^2\) and \(g(x) = 2x - 1\), solve \(fg(x) = 25\).
   step0 field=pre answer=5 text='Square root of 25 ='
   step1 field=pre answer=3 text='Plus case: 2x − 1 = 5, so 2x = 6 and x = 6 ÷ 2 ='
   step2 field=pre answer=-2 text='Minus case: 2x − 1 = −5, so 2x = −4 and x = −4 ÷ 2 ='

### board=maths-eduqas
bronze[6] Q: 14916Find the nth term of \(1, 4, 9, 16, 25, ...\). Which is correct?

gold[2] Q: \(x_{n+1} = \frac{x_n^2 + 3}{5}\), \(x_0 = 1\). Find \(x_2\) to 3 d.p.
   step0 field=say answer=None text='\\(x_{n+1} = \\frac{x_n^2 + 3}{5}\\), start \\(x_0 = 1\\). Find \\(x_2\\), two iterations. Calcul'
   step1 field=pre answer=1 text='First \\(x_1\\). Square the start: 1² ='
   step2 field=pre answer=0.8 text='Add 3, then divide by 5: (1 + 3) ÷ 5 ='
   step3 field=pre answer=0.64 text='Now \\(x_2\\). Square 0.8: 0.8² ='
   step4 field=pre answer=0.728 text='Add 3, then divide by 5: (0.64 + 3) ÷ 5 ='

gold[3] Q: \(f(x) = \frac{2x+1}{x-3}\). Find \(f^{-1}(x)\). Which is correct?

gold[4] Q: A quadratic sequence begins \(5, 12, 23, 38, ...\). Find the 10th term.
   step0 field=say answer=None text='Sequence 5, 12, 23, 38. Find the nth term, then the 10th term.'
   step1 field=pre answer=7 text='First differences: 12 − 5 ='
   step2 field=pre answer=11 text='and 23 − 12 ='
   step3 field=pre answer=4 text='Second difference: 11 − 7 ='
   step4 field=pre answer=3 text='Subtract \\(2n^2\\). At n = 1: 5 − 2 × 1² = 5 − 2 ='
   step5 field=pre answer=200 text='Now the 10th term. First 2 × 10² = 2 × 100 ='
   step6 field=pre answer=12 text='Then n + 2 = 10 + 2 ='
   step7 field=pre answer=212 text='Add them: 200 + 12 ='
