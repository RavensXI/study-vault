# apply-pack: ratio-proportion__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[5] | Check: with x = 0 only the constant term survives. That constant is [box=1] | fix: Reword to: 'When x = 0 the x² and −4x parts both become 0, so only the +1 is left. That number is ___'.
- [low] gold[1] | Sign change between 1 and 2. Now 1.5³ = [box=3.375] | fix: Reword to: 'Because f(1) is negative and f(2) is positive, the sign changes, so a root lies between 1 and 2. Now work out 1.5³ = ___'.
- [low] silver[0] | Second iteration: 3 × 3.6056 + 7 gives 17.8168 under the root, so x₂ = √17.8168  | fix: Split into two shorter lines: 'Inside the root: 3 × 3.6056 + 7 = 17.8168', then 'Now x₂ = √17.8168 to 2 d.p. ='.
- [low] gold[1] | First 2³ = [box=8] ... and 5 × 2 = [box=10] | fix: Reword as full prompts, e.g. 'Work out 2³:' and 'Now work out 5 × 2:', so each stands on its own before the 'Put the pieces together' step.
- [low] silver[2] | Check: the terms 3.317, 3.364 are creeping up towards the fixed point near 3.372 | fix: Replace 'fixed point' with plain language, e.g. 'the value the sequence is settling on (about 3.372)'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[1] Q: \(f(x) = x^3 + 2x - 7\). Show a root lies between 1 and 2. What is \(f(1.5)\) to 3 d.p.?
   step0 field=say answer=None text='f(x) = x³ + 2x − 7. First check the interval, then find f(1.5).'
   step1 field=pre answer=-4 text='f(1) = 1 + 2 − 7 ='
   step2 field=pre answer=5 text='f(2) = 8 + 4 − 7 ='
   step3 field=pre answer=3.375 text='Sign change between 1 and 2. Now 1.5³ ='
   step4 field=pre answer=-0.625 text='f(1.5) = 3.375 + 2(1.5) − 7 = 3.375 + 3 − 7 ='

silver[0] Q: Using \(x_{n+1} = \frac{10}{x_n + 1}\) with \(x_0 = 2\), find \(x_1\). Give answer as a fr
   step0 field=say answer=None text='Iterate x_{n+1} = 10/(x_n + 1) once, from x₀ = 2.'
   step1 field=pre answer=3 text='Work out the denominator: x₀ + 1 = 2 + 1 ='
   step2 field=pre answer=10 text='So x₁ = 10 ÷ 3. The numerator is'
   step3 field=pre answer=3 text='And the denominator is'

silver[2] Q: For \(f(x) = x^3 - 4x - 1\), find \(f(3)\).
   step0 field=say answer=None text='Same function, now x = 3.'
   step1 field=pre answer=27 text='3³ ='
   step2 field=pre answer=12 text='4 × 3 ='
   step3 field=pre answer=14 text='f(3) = 27 − 12 − 1 ='
   step4 field=pre answer=14 text='Check: 27 − 12 = 15, then 15 − 1 ='

silver[5] Q: Show that \(x^2 - 4x + 1 = 0\) has a root between \(x = 0\) and \(x = 1\). What is \(f(0)\
   step0 field=say answer=None text='f(x) = x² − 4x + 1. Substitute x = 0.'
   step1 field=pre answer=0 text='0² ='
   step2 field=pre answer=0 text='4 × 0 ='
   step3 field=pre answer=1 text='f(0) = 0 − 0 + 1 ='
   step4 field=pre answer=1 text='Check: with x = 0 only the constant term survives. That constant is'

### board=maths-edexcel
gold[1] Q: Show that \(x^3 - 5x + 1 = 0\) has a root between \(x = 2\) and \(x = 3\). What is \(f(2)\
   step0 field=pre answer=8 text='First 2³ ='
   step1 field=pre answer=10 text='and 5 × 2 ='
   step2 field=pre answer=-1 text='f(2) = 8 − 10 + 1 ='
   step3 field=pre answer=13 text='Now f(3): 3³ − 5 × 3 + 1 = 27 − 15 + 1 ='
   step4 field=pre answer=-1 text='f(2) is negative and f(3) is positive, so a root lies between. The value asked for, f(2), '

silver[0] Q: Use \(x_{n+1} = \sqrt{3x_n + 7}\) with \(x_0 = 2\). Find \(x_2\) to 2 d.p.
   step0 field=pre answer=13 text='First iteration, inside the root: 3 × 2 + 7 ='
   step1 field=say answer=None text='So \\(x_1 = \\sqrt{13} = 3.6056\\). Keep this full value, do not round yet.'
   step2 field=pre answer=4.22 text='Second iteration: 3 × 3.6056 + 7 gives 17.8168 under the root, so x₂ = √17.8168 to 2 d.p. '
   step3 field=pre answer=17.81 text='Check: 4.22² to 2 d.p. ='

silver[2] Q: Use \(x_{n+1} = \frac{x_n^3 + 1}{4}\) with \(x_0 = 1\). Find \(x_3\) to 3 d.p.
   step0 field=pre answer=0.5 text='x₁ = (1³ + 1) ÷ 4 = 2 ÷ 4 ='
   step1 field=pre answer=0.28125 text='x₂ = (0.5³ + 1) ÷ 4 = (0.125 + 1) ÷ 4 ='
   step2 field=pre answer=0.256 text='x₃ = (0.28125³ + 1) ÷ 4, to 3 d.p. ='

silver[5] Q: The gradient of a curve at \(x = 2\) is found using the tangent through \((0, -1)\) and \(
   step0 field=pre answer=12 text='Rise: 11 − (−1) ='
   step1 field=pre answer=4 text='Run: 4 − 0 ='
   step2 field=pre answer=3 text='Gradient = 12 ÷ 4 ='
   step3 field=pre answer=12 text='Check: 3 × 4 ='

### board=maths-ocr
gold[1] Q: Show \(x^3 - 5x - 4 = 0\) can be rearranged to \(x = \sqrt[3]{5x+4}\). This is the iterati
   step0 field=say answer=None text='Cube both sides of x = ∛(5x + 4) to get x³ = 5x + 4. Move everything to one side: x³ − 5x '
   step1 field=pre answer=1 text='The coefficient of x³ is'
   step2 field=pre answer=-5 text='The coefficient of x (the number multiplying x) is'
   step3 field=pre answer=-4 text='The constant term (the number with no x) is'

silver[0] Q: \(x_{n+1} = \frac{x_n^2 + 5}{2x_n}\). \(x_0 = 3\). Find \(x_1\) to 3 d.p.
   step0 field=pre answer=9 text='x₀²: 3² ='
   step1 field=pre answer=14 text='Numerator: 9 + 5 ='
   step2 field=pre answer=6 text='Denominator: 2 × 3 ='
   step3 field=pre answer=2.333 text='x₁ = 14 ÷ 6 ='
   step4 field=say answer=None text='Check: this formula settles near \\(\\sqrt{5} ≈ 2.236\\), and 2.333 is one step in, so it is '

silver[2] Q: \(x_{n+1} = \sqrt{8 + x_n}\). \(x_0 = 3\). Find \(x_2\) to 3 d.p.
   step0 field=pre answer=11 text='x₁ inside: 8 + 3 ='
   step1 field=pre answer=3.317 text='x₁ = √11 ='
   step2 field=pre answer=11.317 text='Inside: 8 + 3.317 ='
   step3 field=pre answer=3.364 text='x₂ = √11.317 ='
   step4 field=say answer=None text='Check: the terms 3.317, 3.364 are creeping up towards the fixed point near 3.372, so x₂ = '

silver[5] Q: \(x_{n+1} = \frac{x_n^3 + 2}{3x_n^2}\). \(x_0 = 1\). Find \(x_1\).
   step0 field=pre answer=1 text='x₀³: 1³ ='
   step1 field=pre answer=3 text='Numerator: 1 + 2 ='
   step2 field=pre answer=3 text='Denominator: 3 × 1² ='
   step3 field=pre answer=1 text='x₁ = 3 ÷ 3 ='

### board=maths-eduqas
gold[1] Q: Use \(x_{n+1} = \frac{2x_n^3 + 5}{3x_n^2}\) with \(x_0 = 2\). Find \(x_2\) to 3 d.p.
   step0 field=pre answer=21 text='x₁ numerator: 2 × 2³ + 5 = 2 × 8 + 5 ='
   step1 field=pre answer=12 text='x₁ denominator: 3 × 2² = 3 × 4 ='
   step2 field=pre answer=1.75 text='x₁ = 21 ÷ 12 ='
   step3 field=pre answer=1.711 text='x₂ = (2 × 1.75³ + 5) ÷ (3 × 1.75²) to 3 d.p. ='
   step4 field=pre answer=5 text='Check: 1.711³ to the nearest whole number ='

silver[0] Q: Use \(x_{n+1} = \frac{10}{x_n + 1}\) with \(x_0 = 3\). Find \(x_2\) to 2 d.p.
   step0 field=pre answer=2.5 text='x₁: denominator 3 + 1 = 4, so 10 ÷ 4 ='
   step1 field=pre answer=2.86 text='x₂: denominator 2.5 + 1 = 3.5, so 10 ÷ 3.5 to 2 d.p. ='
   step2 field=pre answer=10.01 text='Check: 2.86 × 3.5 ='

silver[2] Q: Use \(x_{n+1} = \frac{x_n^2 + 5}{2x_n}\) with \(x_0 = 3\). Find \(x_1\) to 3 d.p.
   step0 field=pre answer=14 text='Numerator: 3² + 5 ='
   step1 field=pre answer=6 text='Denominator: 2 × 3 ='
   step2 field=pre answer=2.333 text='x₁ = 14 ÷ 6 to 3 d.p. ='
   step3 field=pre answer=14 text='Check: 2.333 × 6 (to the nearest whole number) ='

silver[5] Q: Use \(x_{n+1} = \sqrt{3x_n + 1}\) with \(x_0 = 1\). Find \(x_2\) to 2 d.p.
   step0 field=pre answer=4 text='First iteration, inside the root: 3 × 1 + 1 ='
   step1 field=pre answer=2 text='x₁ = √4 ='
   step2 field=pre answer=7 text='Second iteration, inside the root: 3 × 2 + 1 ='
   step3 field=pre answer=2.65 text='x₂ = √7 to 2 d.p. ='
