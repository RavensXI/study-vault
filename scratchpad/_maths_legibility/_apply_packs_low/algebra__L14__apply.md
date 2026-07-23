# apply-pack: algebra__L14.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[4] | x₂: the inside is 8 − 2 × (full x1) = ___ (3 d.p.) [box=4.366, NO label] | fix: Spell it out, e.g. '8 − 2 × (the unrounded x₁ from your calculator)' or add a one-line reminder to use the un-rounded value.
- [low] gold[1] | Now solve 3x + 13 = 19. Take 13 off: 19 - 13 = [box=6] | fix: Insert a step for the variable term before solving, e.g. 'Multiply 3 by x: 3 x x = 3x, so f(x+5) = 3x + 13', then 'Now solve 3x + 13 = 19.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[1] Q: Use \(x_{n+1} = \frac{10}{x_n + 3}\) with \(x_0 = 1\). Find \(x_2\) to 2 d.p.
   step0 field=pre answer=2.5 text='x₁ = 10 ÷ (1 + 3) = 10 ÷ 4 ='
   step1 field=pre answer=5.5 text='For x₂ the new denominator is 2.5 + 3 ='
   step2 field=pre answer=1.82 text='x₂ = 10 ÷ 5.5, to 2 d.p. ='

gold[4] Q: Find the nth term of \(3, 9, 19, 33, 51, ...\)

### board=maths-edexcel
gold[1] Q: \(f(x) = \frac{1}{x-1}\). Find \(ff(3)\).
   step0 field=say answer=None text='\\(f(x) = \\frac{1}{x-1}\\). Find \\(ff(3)\\): apply \\(f\\), then apply \\(f\\) AGAIN to the resul'
   step1 field=pre answer=2 text='First f(3). The bottom is 3 − 1 ='
   step2 field=pre answer=0.5 text='So f(3) = 1 ÷ 2 ='
   step3 field=pre answer=-0.5 text='Second f. The bottom is 0.5 − 1 ='
   step4 field=pre answer=-2 text='So f(0.5) = 1 ÷ (−0.5) ='

gold[4] Q: Use \(x_{n+1} = \sqrt[3]{8 - 2x_n}\) with \(x_0 = 1\). Find \(x_3\) to 3 d.p.
   step0 field=say answer=None text='\\(x_{n+1} = \\sqrt[3]{8 - 2x_n}\\), start \\(x_0 = 1\\). Find \\(x_3\\). Three iterations, keepi'
   step1 field=pre answer=6 text='\\(x_1\\): the inside is 8 − 2 × 1 ='
   step2 field=pre answer=1.817 text='Cube root: ∛6 = ___ (3 d.p.)'
   step3 field=pre answer=4.366 text='\\(x_2\\): the inside is 8 − 2 × (full x1) = ___ (3 d.p.)'
   step4 field=pre answer=1.634 text='Cube root: ∛4.366 = ___ (3 d.p.)'
   step5 field=pre answer=4.731 text='\\(x_3\\): the inside is 8 − 2 × (full x2) = ___ (3 d.p.)'
   step6 field=pre answer=1.679 text='Cube root: ∛4.731 = ___ (3 d.p.)'

### board=maths-ocr
gold[1] Q: If \(f(x) = \frac{2x+1}{x-3}\), find \(f^{-1}(x)\). Enter the numerator coefficient of x.
   step0 field=pre answer=3 text='In that numerator 3y + 1, the number multiplying y is'
   step1 field=pre answer=1 text='The constant added in that numerator is'
   step2 field=pre answer=3 text='Swapping letters, \\(f^{-1}(x) = \\frac{3x+1}{x-2}\\); its numerator coefficient of x is'

gold[4] Q: If \(f(x) = x^2\) and \(g(x) = 2x - 1\), solve \(fg(x) = 25\).
   step0 field=pre answer=5 text='Square root of 25 ='
   step1 field=pre answer=3 text='Plus case: 2x − 1 = 5, so 2x = 6 and x = 6 ÷ 2 ='
   step2 field=pre answer=-2 text='Minus case: 2x − 1 = −5, so 2x = −4 and x = −4 ÷ 2 ='

### board=maths-eduqas
gold[1] Q: \(f(x) = 3x - 2\), \(g(x) = x + 5\). Solve \(fg(x) = 19\).
   step0 field=say answer=None text='\\(fg(x)\\) means do \\(g\\) first: \\(f(x+5) = 3(x+5) - 2\\). Multiply out and collect the numb'
   step1 field=pre answer=15 text='Multiply out the bracket: 3 × 5 ='
   step2 field=pre answer=13 text='So the constant is 15 − 2 ='
   step3 field=pre answer=6 text='Now solve 3x + 13 = 19. Take 13 off: 19 − 13 ='
   step4 field=pre answer=2 text='Divide by 3: 6 ÷ 3 ='
   step5 field=pre answer=19 text='Check: put x = 2 in: 3 × (2 + 5) − 2 ='

gold[4] Q: A quadratic sequence begins \(5, 12, 23, 38, ...\). Find the 10th term.
   step0 field=say answer=None text='Sequence 5, 12, 23, 38. Find the nth term, then the 10th term.'
   step1 field=pre answer=7 text='First differences: 12 − 5 ='
   step2 field=pre answer=11 text='and 23 − 12 ='
   step3 field=pre answer=4 text='Second difference: 11 − 7 ='
   step4 field=pre answer=3 text='The second difference is 4, and 4 ÷ 2 = 2, so the quadratic part is 2n². Subtract 2n² from'
   step5 field=pre answer=200 text='Now the 10th term. First 2 × 10² = 2 × 100 ='
   step6 field=pre answer=12 text='Then n + 2 = 10 + 2 ='
   step7 field=pre answer=212 text='Add them: 200 + 12 ='
