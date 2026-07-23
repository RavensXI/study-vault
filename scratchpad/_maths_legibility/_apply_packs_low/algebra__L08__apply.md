# apply-pack: algebra__L08.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[4] | the constant added on is minus that square: 0 − 9 = | fix: Reword plainly, e.g. 'you subtract that square from 0: 0 − 9 ='.
- [low] bronze[0] (and every quadratic-formula walk: bronze[0]–[7], silver[0], silver[1], silver[4], gold[2]) | Now x = (−b ± √) ÷ 2a, with −b = −3 and 2a = 2. Take the plus first: | fix: Show the radicand explicitly, e.g. 'x = (−b ± √(b² − 4ac)) ÷ 2a' or 'x = (−b ± [the root you just found]) ÷ 2a'.
- [low] bronze[1] | discriminant: 4 − (−32) = [box=36, NO label] | fix: Match bronze[3]/[7] style: 'discriminant: 2² − (−32) = 4 − (−32) ='.
- [low] gold[4] | The turning point sits at x = -p = -(-2) = [box=2] | fix: Build it first: add a line 'y = (x-2)^2 + 3 is smallest when (x-2)^2 = 0, i.e. x = 2', so the x = -p step is derived rather than asserted.
- [low] silver[0] | (-4 + √28) ÷ 2 = (2 d.p.) [box=0.65] | fix: Move the instruction out of the answer slot: 'Work out (-4 + √28) ÷ 2, giving it to 2 d.p.' (leave the box after it).

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: For \(x^2 + 5x + 3 = 0\), what is the discriminant \(b^2 - 4ac\)?
   step0 field=say answer=None text='The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 5, c = 3.'
   step1 field=pre answer=25 text='b squared: 5² ='
   step2 field=pre answer=12 text='4ac: 4 × 1 × 3 ='
   step3 field=pre answer=13 text='discriminant: 25 − 12 ='

bronze[1] Q: For \(2x^2 - 3x - 1 = 0\), what is the discriminant?
   step0 field=say answer=None text='The discriminant is \\(b^2 - 4ac\\). Read off a = 2, b = −3, c = −1.'
   step1 field=pre answer=9 text='b squared: (−3)² ='
   step2 field=pre answer=-8 text='4ac: 4 × 2 × −1 ='
   step3 field=pre answer=17 text='discriminant: 9 − (-8) ='

bronze[4] Q: Write \(x^2 + 6x\) in the form \((x + a)^2 + b\). Find \(b\).
   step0 field=say answer=None text='Complete the square on \\(x^2 +6 x\\). Halve the coefficient of x.'
   step1 field=pre answer=3 text='half of 6 ='
   step2 field=pre answer=9 text='square that half: 3² ='
   step3 field=pre answer=-9 text='the constant added on is minus that square: 0 − 9 ='

gold[4] Q: Find the minimum value of \(x^2 - 8x + 20\)
   step0 field=say answer=None text='The minimum of a quadratic is the constant after completing the square. Halve −8.'
   step1 field=pre answer=-4 text='half of −8 ='
   step2 field=pre answer=16 text='square it: (−4)² ='
   step3 field=pre answer=4 text='minimum value = 20 − 16 ='

silver[0] Q: Solve \(x^2 + 3x - 7 = 0\). Give the positive solution to 2 d.p.
   step0 field=say answer=None text='Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 3, c = −7.'
   step1 field=pre answer=-28 text='4ac: 4 × 1 × −7 ='
   step2 field=pre answer=37 text='discriminant: 3² − (−28) = 9 − (−28) ='
   step3 field=pre answer=6.08 text='square root of 37, to 2 d.p. ='
   step4 field=pre answer=1.54 text='positive root: (-3 + 6.08) ÷ 2 ='

### board=maths-edexcel
bronze[0] Q: Solve \(x^2 + 3x - 10 = 0\) using the quadratic formula
   step0 field=say answer=None text='Read off a = 1, b = 3, c = −10. The formula needs the discriminant b² − 4ac first.'
   step1 field=pre answer=9 text='b squared: 3 × 3 ='
   step2 field=pre answer=-40 text='4ac: 4 × 1 × (−10) ='
   step3 field=pre answer=49 text='discriminant b² − 4ac: 9 − (−40) ='
   step4 field=pre answer=7 text='square root: √49 ='
   step5 field=pre answer=2 text='x = (−3 + 7) ÷ 2 ='
   step6 field=pre answer=-5 text='then the minus: x = (−3 − 7) ÷ 2 ='
   step7 field=pre answer=0 text='check x = 2: 2² + 3 × 2 + (−10) ='

bronze[1] Q: Solve \(x^2 - 5x + 6 = 0\) using the quadratic formula
   step0 field=say answer=None text='Read off a = 1, b = −5, c = 6. The formula needs the discriminant b² − 4ac first.'
   step1 field=pre answer=25 text='b squared: (−5) × (−5) ='
   step2 field=pre answer=24 text='4ac: 4 × 1 × 6 ='
   step3 field=pre answer=1 text='discriminant b² − 4ac: 25 − 24 ='
   step4 field=pre answer=1 text='square root: √1 ='
   step5 field=pre answer=3 text='x = (5 + 1) ÷ 2 ='
   step6 field=pre answer=2 text='then the minus: x = (5 − 1) ÷ 2 ='
   step7 field=pre answer=0 text='check x = 3: 3² + (−5) × 3 + 6 ='

bronze[4] Q: Solve \(x^2 + 5x - 6 = 0\) using the quadratic formula
   step0 field=say answer=None text='Read off a = 1, b = 5, c = −6. The formula needs the discriminant b² − 4ac first.'
   step1 field=pre answer=25 text='b squared: 5 × 5 ='
   step2 field=pre answer=-24 text='4ac: 4 × 1 × (−6) ='
   step3 field=pre answer=49 text='discriminant b² − 4ac: 25 − (−24) ='
   step4 field=pre answer=7 text='square root: √49 ='
   step5 field=pre answer=1 text='x = (−5 + 7) ÷ 2 ='
   step6 field=pre answer=-6 text='then the minus: x = (−5 − 7) ÷ 2 ='
   step7 field=pre answer=0 text='check x = 1: 1² + 5 × 1 + (−6) ='

gold[4] Q: Solve \(x^2 + 2x - 7 = 0\) by completing the square. Give the positive root to 2 d.p.
   step0 field=say answer=None text='a = 1, so complete the square. Halve b first.'
   step1 field=pre answer=1 text='halve b: 2 ÷ 2 ='
   step2 field=pre answer=1 text='p squared: 1² ='
   step3 field=pre answer=-8 text='the constant: c − p² = (−7) − 1 ='
   step4 field=pre answer=8 text='(x + 1)² ='
   step5 field=pre answer=1.83 text='square-root both sides: x + 1 = ±√8, so x = −1 ± √8. Positive root: (−1) + √8 = (−1) + 2.8'
   step6 field=pre answer=-3.83 text='the other root: (−1) − √8 ='

silver[0] Q: Solve \(x^2 + 4x + 1 = 0\), give answers to 2 d.p.
   step0 field=say answer=None text='Read off a = 1, b = 4, c = 1. Work out the discriminant b² − 4ac first.'
   step1 field=pre answer=16 text='b squared: 4 × 4 ='
   step2 field=pre answer=4 text='4ac: 4 × 1 × 1 ='
   step3 field=pre answer=12 text='discriminant b² − 4ac: 16 − 4 ='
   step4 field=pre answer=-0.27 text='x = (−4 + 3.464) ÷ 2 ='
   step5 field=pre answer=-3.73 text='then minus: x = (−4 − 3.464) ÷ 2 ='
   step6 field=pre answer=-4.0 text='add your two roots to check: (−0.27) + (−3.73) ='

### board=maths-ocr
bronze[0] Q: Find the discriminant of \(x^2 + 4x + 3 = 0\)
   step0 field=say answer=None text='The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 4, c = 3.'
   step1 field=pre answer=16 text='b squared: 4² ='
   step2 field=pre answer=12 text='4ac: 4 × 1 × 3 ='
   step3 field=pre answer=4 text='discriminant: 16 − 12 ='

bronze[1] Q: Solve \(x^2 + 2x - 8 = 0\) using the formula. Enter the positive solution.
   step0 field=say answer=None text='Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 2, c = −8.'
   step1 field=pre answer=-32 text='4ac: 4 × 1 × −8 ='
   step2 field=pre answer=36 text='discriminant: 4 − (−32) ='
   step3 field=pre answer=6 text='square root: √36 ='
   step4 field=pre answer=2 text='positive root: (−2 + 6) ÷ 2 ='

bronze[4] Q: Find the discriminant of \(x^2 + 5x + 6 = 0\)
   step0 field=say answer=None text='The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 5, c = 6.'
   step1 field=pre answer=25 text='b squared: 5² ='
   step2 field=pre answer=24 text='4ac: 4 × 1 × 6 ='
   step3 field=pre answer=1 text='discriminant: 25 − 24 ='

gold[4] Q: The equation \(2x^2 + px + 8 = 0\) has no real roots. What is the largest integer value of
   step0 field=say answer=None text='No real roots means the discriminant is negative: \\(p^2 - 4ac < 0\\). Here a = 2, c = 8.'
   step1 field=pre answer=64 text='4ac: 4 × 2 × 8 ='
   step2 field=pre answer=8 text='so we need p² < 64; the boundary is √64 ='
   step3 field=pre answer=7 text='p must be below 8, so the largest integer p is'

silver[0] Q: Solve \(x^2 + 3x - 7 = 0\). Give the positive root to 2 d.p.
   step0 field=say answer=None text='Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = 1, b = 3, c = −7.'
   step1 field=pre answer=-28 text='4ac: 4 × 1 × −7 ='
   step2 field=pre answer=37 text='discriminant: 3² − (−28) = 9 − (−28) ='
   step3 field=pre answer=6.08 text='square root of 37, to 2 d.p. ='
   step4 field=pre answer=1.54 text='positive root: (−3 + 6.08) ÷ 2 ='

### board=maths-eduqas
bronze[0] Q: For \(x^2 + 7x - 5 = 0\), state the values of \(a\), \(b\), \(c\). What is \(b\)?
   step0 field=say answer=None text='Compare \\(x^2 + 7x - 5\\) with \\(ax^2 + bx + c\\), matching term by term.'
   step1 field=pre answer=1 text='a, from the x² term ='
   step2 field=pre answer=-5 text='c, the constant with its sign ='
   step3 field=say answer=None text='b is the coefficient of the x term, and that is what the question wants.'
   step4 field=pre answer=7 text='b ='
   step5 field=pre answer=7 text='Check: rebuild it as 1x² + __x − 5. The blank is'

bronze[1] Q: Find the discriminant of \(x^2 + 4x + 1 = 0\).
   step0 field=say answer=None text='Read off a = 1, b = 4, c = 1.'
   step1 field=pre answer=16 text='b² = 4 × 4 ='
   step2 field=pre answer=4 text='4ac = 4 × 1 × 1 ='
   step3 field=say answer=None text='Now subtract to get the discriminant.'
   step4 field=pre answer=12 text='b² − 4ac = 16 − 4 ='
   step5 field=pre answer=2 text='12 is positive, so the number of real roots is'

bronze[4] Q: Complete the square: \(x^2 + 6x\). Write as \((x+p)^2 - q\). What is \(p\)?
   step0 field=say answer=None text='For \\(x^2 + 6x = (x+p)^2 - q\\), find p by halving the 6.'
   step1 field=pre answer=3 text='6 ÷ 2 ='
   step2 field=say answer=None text='Square that to get the q you would subtract.'
   step3 field=pre answer=9 text='3² ='
   step4 field=pre answer=6 text='Check: expand (x+3)² − 9 = x² + 6x + 9 − 9. The x coefficient is'

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
