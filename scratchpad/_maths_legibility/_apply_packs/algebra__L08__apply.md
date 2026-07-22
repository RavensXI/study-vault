# apply-pack: algebra__L08.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[0] | so (x+3)² = 7, and comparing with −3 + √k gives k = | fix: Insert an intermediate step, e.g. 'square-root both sides: x + 3 = √7, so x = −3 + √7; matching −3 + √k gives k =' before the final box.
- [medium] gold[2] | 4ac = 4·k·k = 4k². Set 36 − 4k² = 0, so 4k² = | fix: Split into two steps and use ×: 'work out 4ac: 4 × k × k = 4k²' then 'set 36 − 4k² = 0 and rearrange, so 4k² ='.
- [medium] gold[0] | smaller root: 4 − √11 = 4 − 3.317 = | fix: Insert one intermediate step before the root asks: 'square-root both sides: x − 4 = ±√11, so x = 4 ± √11'. Then ask for each root.
- [medium] gold[4] | positive root: (−1) + √8 = (−1) + 2.828 = | fix: Add 'square-root both sides: x + 1 = ±√8, so x = −1 ± √8' before asking for the positive and other root.
- [medium] silver[0] | discriminant: 9 − (−28) = [box=37, NO label] | fix: Show b² inline like bronze[3]/[7]: 'discriminant: 3² − (−28) = 9 − (−28) ='. Do the same for silver[4] and gold[3].
- [medium] silver[3] | discriminant: 25 − 8 = [box=17, NO label] | fix: Add the b² inline: 'discriminant: (−5)² − 8 = 25 − 8 ='.
- [medium] gold[0] | so (x + 2)² = 3, and comparing −2 + √n gives n = [box=3, NO label] | fix: Insert an intermediate step: 'move the −3 across: (x + 2)² = 3, then take the root: x = −2 + √3, so n = 3.'
- [medium] bronze[1] | Enter the number of real roots: [box=2] | fix: Reword to match bronze[7]: '12 is positive, so the number of real roots is'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[1] Q: For \(2x^2 - 3x - 1 = 0\), what is the discriminant?
   step0 field=say answer=None text='The discriminant is \\(b^2 - 4ac\\). Read off a = 2, b = −3, c = −1.'
   step1 field=pre answer=9 text='b squared: (−3)² ='
   step2 field=pre answer=-8 text='4ac: 4 × 2 × −1 ='
   step3 field=pre answer=17 text='discriminant: 9 − (-8) ='

gold[0] Q: Solve \(x^2 + 6x + 2 = 0\) by completing the square. The positive root is \(-3 + \sqrt{k}\
   step0 field=say answer=None text='Solve by completing the square. Halve the 6 to get 3, giving \\((x+3)^2\\).'
   step1 field=pre answer=9 text='the correction to subtract is 3² ='
   step2 field=pre answer=-7 text='constant after completing: −9 + 2 ='
   step3 field=pre answer=7 text='so (x+3)² = 7, and comparing with −3 + √k gives k ='

gold[2] Q: \(kx^2 + 6x + k = 0\) has equal roots. Find the positive value of \(k\).
   step0 field=say answer=None text='Equal roots means the discriminant is 0. Here a = k, b = 6, c = k.'
   step1 field=pre answer=36 text='b squared: 6² ='
   step2 field=pre answer=36 text='4ac = 4·k·k = 4k². Set 36 − 4k² = 0, so 4k² ='
   step3 field=pre answer=9 text='k² = 36 ÷ 4 ='
   step4 field=pre answer=3 text='positive k = √9 ='

gold[4] Q: Find the minimum value of \(x^2 - 8x + 20\)
   step0 field=say answer=None text='The minimum of a quadratic is the constant after completing the square. Halve −8.'
   step1 field=pre answer=-4 text='half of −8 ='
   step2 field=pre answer=16 text='square it: (−4)² ='
   step3 field=pre answer=4 text='minimum value = 20 − 16 ='

silver[0] Q: Solve \(x^2 + 3x - 7 = 0\). Give the positive solution to 2 d.p.
   step0 field=say answer=None text='Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 3, c = −7.'
   step1 field=pre answer=-28 text='4ac: 4 × 1 × −7 ='
   step2 field=pre answer=37 text='discriminant: 9 − (-28) ='
   step3 field=pre answer=6.08 text='square root of 37, to 2 d.p. ='
   step4 field=pre answer=1.54 text='positive root: (-3 + 6.08) ÷ 2 ='

silver[3] Q: Write \(x^2 - 4x + 7\) in the form \((x + p)^2 + q\). Find \(p\).
   step0 field=say answer=None text='Complete the square on \\(x^2 -4 x +7\\). Halve the coefficient of x.'
   step1 field=pre answer=-2 text='half of -4 ='
   step2 field=pre answer=4 text='square it: (-2)² ='
   step3 field=pre answer=-2 text='in \\((x + p)^2 + q\\), p is that half, so p ='

### board=maths-edexcel
bronze[1] Q: Solve \(x^2 - 5x + 6 = 0\) using the quadratic formula
   step0 field=say answer=None text='Read off a = 1, b = −5, c = 6. The formula needs the discriminant b² − 4ac first.'
   step1 field=pre answer=25 text='b squared: (−5) × (−5) ='
   step2 field=pre answer=24 text='4ac: 4 × 1 × 6 ='
   step3 field=pre answer=1 text='discriminant b² − 4ac: 25 − 24 ='
   step4 field=pre answer=1 text='square root: √1 ='
   step5 field=pre answer=3 text='x = (5 + 1) ÷ 2 ='
   step6 field=pre answer=2 text='then the minus: x = (5 − 1) ÷ 2 ='
   step7 field=pre answer=0 text='check x = 3: 3² + (−5) × 3 + 6 ='

gold[0] Q: Solve \(x^2 - 8x + 5 = 0\) by completing the square. Give the smaller root to 2 d.p.
   step0 field=say answer=None text='a = 1, so complete the square. Halve b first.'
   step1 field=pre answer=-4 text='halve b: (−8) ÷ 2 ='
   step2 field=pre answer=16 text='p squared: (−4)² ='
   step3 field=pre answer=-11 text='the constant: c − p² = 5 − 16 ='
   step4 field=pre answer=11 text='(x − 4)² ='
   step5 field=pre answer=0.68 text='smaller root: 4 − √11 = 4 − 3.317 ='
   step6 field=pre answer=7.32 text='the other root: 4 + √11 ='

gold[2] Q: Solve \(2x^2 - 12x + 7 = 0\), give answers to 2 d.p.
   step0 field=say answer=None text='Read off a = 2, b = −12, c = 7. Work out the discriminant b² − 4ac first.'
   step1 field=pre answer=144 text='b squared: (−12) × (−12) ='
   step2 field=pre answer=56 text='4ac: 4 × 2 × 7 ='
   step3 field=pre answer=88 text='discriminant b² − 4ac: 144 − 56 ='
   step4 field=pre answer=5.35 text='x = (12 + 9.381) ÷ 4 ='
   step5 field=pre answer=0.65 text='then minus: x = (12 − 9.381) ÷ 4 ='
   step6 field=pre answer=6.0 text='add your two roots to check: 5.35 + 0.65 ='

gold[4] Q: Solve \(x^2 + 2x - 7 = 0\) by completing the square. Give the positive root to 2 d.p.
   step0 field=say answer=None text='a = 1, so complete the square. Halve b first.'
   step1 field=pre answer=1 text='halve b: 2 ÷ 2 ='
   step2 field=pre answer=1 text='p squared: 1² ='
   step3 field=pre answer=-8 text='the constant: c − p² = (−7) − 1 ='
   step4 field=pre answer=8 text='(x + 1)² ='
   step5 field=pre answer=1.83 text='positive root: (−1) + √8 = (−1) + 2.828 ='
   step6 field=pre answer=-3.83 text='the other root: (−1) − √8 ='

silver[0] Q: Solve \(x^2 + 4x + 1 = 0\), give answers to 2 d.p.
   step0 field=say answer=None text='Read off a = 1, b = 4, c = 1. Work out the discriminant b² − 4ac first.'
   step1 field=pre answer=16 text='b squared: 4 × 4 ='
   step2 field=pre answer=4 text='4ac: 4 × 1 × 1 ='
   step3 field=pre answer=12 text='discriminant b² − 4ac: 16 − 4 ='
   step4 field=pre answer=-0.27 text='x = (−4 + 3.464) ÷ 2 ='
   step5 field=pre answer=-3.73 text='then minus: x = (−4 − 3.464) ÷ 2 ='
   step6 field=pre answer=-4.0 text='add your two roots to check: (−0.27) + (−3.73) ='

silver[3] Q: Write \(x^2 - 4x + 1\) in the form \((x+p)^2+q\). State the value of \(q\).
   step0 field=say answer=None text='Write it as (x + p)² + q. Start by halving b.'
   step1 field=pre answer=-2 text='halve b: (−4) ÷ 2 ='
   step2 field=pre answer=4 text='p squared: (−2)² ='
   step3 field=pre answer=-3 text='q = c − p² = 1 − 4 ='
   step4 field=pre answer=1 text='check by rebuilding c: p² + q = 4 + (−3) ='

### board=maths-ocr
bronze[1] Q: Solve \(x^2 + 2x - 8 = 0\) using the formula. Enter the positive solution.
   step0 field=say answer=None text='Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 2, c = −8.'
   step1 field=pre answer=-32 text='4ac: 4 × 1 × −8 ='
   step2 field=pre answer=36 text='discriminant: 4 − (−32) ='
   step3 field=pre answer=6 text='square root: √36 ='
   step4 field=pre answer=2 text='positive root: (−2 + 6) ÷ 2 ='

gold[0] Q: Solve \(x^2 + 4x + 1 = 0\) by completing the square. Give the positive root in surd form: 
   step0 field=say answer=None text='Complete the square. Halve the 4 to get 2, giving \\((x + 2)^2\\).'
   step1 field=pre answer=4 text='the correction to subtract is 2² ='
   step2 field=pre answer=-3 text='constant after completing: −4 + 1 ='
   step3 field=pre answer=3 text='so (x + 2)² = 3, and comparing −2 + √n gives n ='

gold[2] Q: Write \(2x^2 + 12x + 5\) in the form \(a(x+p)^2 + q\). What is \(q\)?
   step0 field=say answer=None text='Factor the 2 from the first two terms: \\(2(x^2 + 6x) + 5\\).'
   step1 field=pre answer=3 text='half of the 6 inside is'
   step2 field=pre answer=18 text='the 2 outside times that square: 2 × 3² ='
   step3 field=pre answer=-13 text='q = −18 + 5 ='

gold[4] Q: The equation \(2x^2 + px + 8 = 0\) has no real roots. What is the largest integer value of
   step0 field=say answer=None text='No real roots means the discriminant is negative: \\(p^2 - 4ac < 0\\). Here a = 2, c = 8.'
   step1 field=pre answer=64 text='4ac: 4 × 2 × 8 ='
   step2 field=pre answer=8 text='so we need p² < 64; the boundary is √64 ='
   step3 field=pre answer=7 text='p must be below 8, so the largest integer p is'

silver[0] Q: Solve \(x^2 + 3x - 7 = 0\). Give the positive root to 2 d.p.
   step0 field=say answer=None text='Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 3, c = −7.'
   step1 field=pre answer=-28 text='4ac: 4 × 1 × −7 ='
   step2 field=pre answer=37 text='discriminant: 9 − (−28) ='
   step3 field=pre answer=6.08 text='square root of 37, to 2 d.p. ='
   step4 field=pre answer=1.54 text='positive root: (−3 + 6.08) ÷ 2 ='

silver[3] Q: Solve \(2x^2 - 5x + 1 = 0\). Give the larger root to 2 d.p.
   step0 field=say answer=None text='Use the formula with a = 2, b = −5, c = 1. Note 2a = 4.'
   step1 field=pre answer=8 text='4ac: 4 × 2 × 1 ='
   step2 field=pre answer=17 text='discriminant: 25 − 8 ='
   step3 field=pre answer=4.12 text='square root of 17, to 2 d.p. ='
   step4 field=pre answer=2.28 text='larger root: (5 + 4.12) ÷ 4 ='

### board=maths-eduqas
bronze[1] Q: Find the discriminant of \(x^2 + 4x + 1 = 0\).
   step0 field=say answer=None text='Read off a = 1, b = 4, c = 1.'
   step1 field=pre answer=16 text='b² = 4 × 4 ='
   step2 field=pre answer=4 text='4ac = 4 × 1 × 1 ='
   step3 field=say answer=None text='Now subtract to get the discriminant.'
   step4 field=pre answer=12 text='b² − 4ac = 16 − 4 ='
   step5 field=pre answer=2 text='Enter the number of real roots:'

gold[0] Q: Solve \(3x^2 - 5x + 1 = 0\). Give the sum of both solutions as a fraction.
   step0 field=say answer=None text='There is a shortcut: for ax² + bx + c = 0 the two roots always add to −b/a. No solving nee'
   step1 field=pre answer=3 text='a ='
   step2 field=pre answer=-5 text='b ='
   step3 field=say answer=None text='The sum is −b ÷ a. Work out −b first.'
   step4 field=pre answer=5 text='−b = −(−5) ='
   step5 field=pre answer=3 text='So the sum is 5 over a. The denominator a ='

gold[2] Q: Write \(2x^2 + 12x + 5\) in the form \(a(x+p)^2 + q\). What is \(q\)?
   step0 field=say answer=None text='Factor the 2 out of the x² and x terms only.'
   step1 field=pre answer=6 text='Inside: 12 ÷ 2 ='
   step2 field=say answer=None text='Complete the square on x² + 6x: halve the 6.'
   step3 field=pre answer=3 text='6 ÷ 2 ='
   step4 field=pre answer=9 text='Square it: 3² ='
   step5 field=say answer=None text='Inside becomes (x+3)² − 9. Multiply the −9 back by 2, then add the 5.'
   step6 field=pre answer=-18 text='2 × (−9) ='
   step7 field=pre answer=-13 text='q = −18 + 5 ='

gold[4] Q: By completing the square, find the coordinates of the turning point of \(y = x^2 - 4x + 7\
   step0 field=say answer=None text='Complete the square: the turning point pops straight out. Halve the −4.'
   step1 field=pre answer=-2 text='−4 ÷ 2 ='
   step2 field=pre answer=4 text='Square it: (−2)² ='
   step3 field=say answer=None text='The y-coordinate is c − p², and c = 7.'
   step4 field=pre answer=3 text='y = 7 − 4 ='
   step5 field=pre answer=2 text='The turning point sits at x = −p = −(−2) ='

silver[0] Q: Solve \(x^2 + 4x - 3 = 0\) using the formula. Give the positive root to 2 d.p.
   step0 field=say answer=None text='a = 1, b = 4, c = −3. Start with the discriminant.'
   step1 field=pre answer=28 text='b² − 4ac = 16 − 4 × 1 × (−3) = 16 − (−12) ='
   step2 field=pre answer=5.29 text='√28 to 2 d.p. ='
   step3 field=say answer=None text='The positive root uses +√, all over 2a = 2.'
   step4 field=pre answer=0.65 text='(−4 + √28) ÷ 2 = (2 d.p.)'
   step5 field=pre answer=-4.65 text='The other root: (−4 − √28) ÷ 2 = (2 d.p.)'

silver[3] Q: Complete the square for \(x^2 - 10x + 3\). What is the minimum value of the expression?
   step0 field=say answer=None text='Halve the −10 for p. Keep the minus.'
   step1 field=pre answer=-5 text='−10 ÷ 2 ='
   step2 field=pre answer=25 text='p² = (−5)² ='
   step3 field=say answer=None text='The least value is c − p², and c = 3.'
   step4 field=pre answer=-22 text='3 − 25 ='
   step5 field=pre answer=-22 text='Check: (x−5)² − 22 is smallest when (x−5)² = 0, giving'
