# apply-pack: algebra__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[0] | Now 4(x + 1) + 3(x − 1) = 36. Expand: 4x + 4 + 3x − 3 = 36. Combine: 7x + 1 = 36 | fix: Break into two beats: first show the expansion (4x + 4 + 3x − 3 = 36), then a separate line to combine into 7x + 1 = 36 before subtracting 1.
- [low] silver[4] | The whole left side is divided by 5. Multiply both sides by 5 to clear it. 5 × 5 | fix: Since the intro already explained it, keep the ask to the arithmetic: 'Multiply both sides by 5: 5 × 5 ='.
- [low] bronze[5] | The x term is negative, so add 3x to both sides. That gives 20 = 5 + 3x. Now sub | fix: Split into two beats: an intro/ask that lands '20 = 5 + 3x' from adding 3x, then a separate ask 'Subtract 5: 20 − 5 ='.
- [low] gold[3] | intro 'Clear the fraction: multiply both sides by 3.' → box asks only 'Right: 5  | fix: Add a sentence before 'So 2x + 1 = 15.' explaining the left side clears: 'The left, (2x + 1) ÷ 3, multiplied by 3 just leaves 2x + 1.'
- [low] gold[0] | intro: Cross-multiply to clear the fractions: 2(2x+1) = 3(x+4). | fix: Replace the jargon with the action, e.g. 'Multiply each side by the other denominator: (2x+1)×2 and (x+4)×3, giving 2(2x+1) = 3(x+4)'. Same edit in gold[3].
- [low] gold[1] | Multiply both sides by 4. On the right, 4 ÷ 2 = [box=2, NO label] → Now x + 3 =  | fix: Add a bridging line after the box: 'So the right side becomes 2 lots of (x − 1) = 2x − 2', then continue to 'Now x + 3 = 2x − 2.'
- [low] gold[3] | On the right, 2(x + 1) ÷ 2 is just x + 1. Adding the extra 1 gives x + 1 + 1 = x | fix: Split and name the reference: 'The right side simplifies to x + 1. The original equation also has a lone + 1 on the right, so add it: 1 + 1 = [box=2], giving x 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[5] Q: Solve \(20 - 3x = 5\)
   step0 field=pre answer=15 text='The x term is negative, so add 3x to both sides. That gives 20 = 5 + 3x. Now subtract 5 fr'
   step1 field=pre answer=5 text='15 ÷ 3 ='
   step2 field=pre answer=5 text='So x ='
   step3 field=pre answer=5 text='Check: 20 − 3 × 5 ='

gold[0] Q: Solve \(\frac{x+1}{3} + \frac{x-1}{4} = 3\)
   step0 field=pre answer=4 text='Clear both fractions at once. The bottoms are 3 and 4, and the number both divide into is '
   step1 field=pre answer=3 text='For the second fraction: 12 ÷ 4 ='
   step2 field=pre answer=35 text='36 − 1 ='
   step3 field=pre answer=5 text='35 ÷ 7 ='
   step4 field=pre answer=5 text='So x ='
   step5 field=pre answer=3 text='Check: (5 + 1) ÷ 3 + (5 − 1) ÷ 4 ='

gold[1] Q: Solve \(\frac{5x + 2}{3} = \frac{3x + 8}{2}\)
   step0 field=pre answer=4 text='Two single fractions equal each other, so cross multiply — each top is multiplied by the o'
   step1 field=pre answer=24 text='Right side: 3 × (3x + 8). 3 × 8 ='
   step2 field=pre answer=1 text='10x − 9x ='
   step3 field=pre answer=20 text='24 − 4 ='
   step4 field=pre answer=20 text='So x ='
   step5 field=pre answer=34 text='Check: (5 × 20 + 2) ÷ 3 ='

gold[3] Q: Solve \(3(2x + 1) = 2(4x - 3) + 3\)
   step0 field=pre answer=-6 text='Expand both sides. Left: 3(2x + 1) = 6x + 3. On the right, expand 2(4x − 3) and remember t'
   step1 field=pre answer=2 text='8x − 6x ='
   step2 field=pre answer=6 text='3 + 3 ='
   step3 field=pre answer=3 text='6 ÷ 2 ='
   step4 field=pre answer=3 text='So x ='
   step5 field=pre answer=21 text='Check: 3 × (2 × 3 + 1) ='

silver[4] Q: Solve \(\frac{2x - 3}{5} = 5\)
   step0 field=pre answer=25 text='The whole left side is divided by 5. Multiply both sides by 5 to clear it. 5 × 5 ='
   step1 field=pre answer=28 text='25 + 3 ='
   step2 field=pre answer=14 text='28 ÷ 2 ='
   step3 field=pre answer=14 text='So x ='
   step4 field=pre answer=5 text='Check: (2 × 14 − 3) ÷ 5 ='

### board=maths-edexcel
bronze[5] Q: Solve \(6x + 4 = 46\)
   step0 field=say answer=None text='Undo in reverse. The +4 was added last, so subtract 4 from both sides first.'
   step1 field=pre answer=42 text='46 − 4 ='
   step2 field=say answer=None text='So 6x = 42. Now divide both sides by 6.'
   step3 field=pre answer=7 text='42 ÷ 6 ='
   step4 field=say answer=None text='Check by putting x = 7 back in.'
   step5 field=pre answer=46 text='6 × 7 + 4 ='

gold[0] Q: Solve \(3(x + 4) = 2(x + 7)\)
   step0 field=say answer=None text='Expand both brackets first.'
   step1 field=pre answer=3 text='Left: 3 × x ='
   step2 field=pre answer=12 text='Left: 3 × 4 ='
   step3 field=pre answer=2 text='Right: 2 × x ='
   step4 field=pre answer=14 text='Right: 2 × 7 ='
   step5 field=say answer=None text='So 3x + 12 = 2x + 14. Subtract 2x from both sides.'
   step6 field=pre answer=1 text='3x − 2x ='
   step7 field=say answer=None text='Now x + 12 = 14. Subtract 12 from both sides.'
   step8 field=pre answer=2 text='14 − 12 ='
   step9 field=say answer=None text='So x = 2. Check both sides.'
   step10 field=pre answer=18 text='3 × (2 + 4) ='
   step11 field=pre answer=18 text='2 × (2 + 7) ='

gold[1] Q: Solve \(5(2x − 3) = 3(x + 2)\)
   step0 field=say answer=None text='Expand both brackets first.'
   step1 field=pre answer=10 text='Left: 5 × 2x ='
   step2 field=pre answer=-15 text='Left: 5 × (−3) ='
   step3 field=pre answer=3 text='Right: 3 × x ='
   step4 field=pre answer=6 text='Right: 3 × 2 ='
   step5 field=say answer=None text='So 10x − 15 = 3x + 6. Subtract 3x from both sides.'
   step6 field=pre answer=7 text='10x − 3x ='
   step7 field=say answer=None text='Now 7x − 15 = 6. Add 15 to both sides.'
   step8 field=pre answer=21 text='6 + 15 ='
   step9 field=say answer=None text='So 7x = 21. Now divide both sides by 7.'
   step10 field=pre answer=3 text='21 ÷ 7 ='
   step11 field=say answer=None text='Check both sides with x = 3.'
   step12 field=pre answer=15 text='5 × (2 × 3 − 3) ='
   step13 field=pre answer=15 text='3 × (3 + 2) ='

gold[3] Q: Solve \(\frac{2x + 1}{3} = 5\)
   step0 field=say answer=None text='Clear the fraction: multiply both sides by 3.'
   step1 field=pre answer=15 text='Right: 5 × 3 ='
   step2 field=say answer=None text='So 2x + 1 = 15. Subtract 1 from both sides.'
   step3 field=pre answer=14 text='15 − 1 ='
   step4 field=say answer=None text='So 2x = 14. Now divide both sides by 2.'
   step5 field=pre answer=7 text='14 ÷ 2 ='
   step6 field=say answer=None text='Check x = 7 in the original.'
   step7 field=pre answer=15 text='2 × 7 + 1 ='
   step8 field=pre answer=5 text='15 ÷ 3 ='

silver[4] Q: Solve \(8x + 1 = 5x + 25\)
   step0 field=say answer=None text='Subtract 5x from both sides to collect x.'
   step1 field=pre answer=3 text='8x − 5x ='
   step2 field=say answer=None text='Now 3x + 1 = 25. Subtract 1 from both sides.'
   step3 field=pre answer=24 text='25 − 1 ='
   step4 field=say answer=None text='So 3x = 24. Now divide both sides by 3.'
   step5 field=pre answer=8 text='24 ÷ 3 ='
   step6 field=say answer=None text='Check both sides with x = 8.'
   step7 field=pre answer=65 text='8 × 8 + 1 ='
   step8 field=pre answer=65 text='5 × 8 + 25 ='

### board=maths-ocr
bronze[5] Q: Solve \(7x - 2 = 19\)
   step0 field=say answer=None text='The 2 is subtracted, so add 2 to both sides first.'
   step1 field=pre answer=21 text='Add 2: 19 + 2 ='
   step2 field=pre answer=3 text='Now divide by 7: 21 ÷ 7 ='
   step3 field=pre answer=19 text='Check: 7 × 3 − 2 ='

gold[0] Q: Solve \(\frac{2x+1}{3} = \frac{x+4}{2}\)
   step0 field=say answer=None text='Cross-multiply to clear the fractions: \\(2(2x+1) = 3(x+4)\\).'
   step1 field=pre answer=4 text='Expand the left: 2 × 2x ='
   step2 field=pre answer=12 text='Expand the right: the x-term is 3 × x = 3x, and the number is 3 × 4 ='
   step3 field=pre answer=1 text='Collect x: 4x − 3x ='
   step4 field=say answer=None text='The left side also had 2 × 1 = 2, so now x + 2 = 12.'
   step5 field=pre answer=10 text='Take off 2: 12 − 2 ='
   step6 field=pre answer=7 text='Check the left side: (2 × 10 + 1) ÷ 3 ='

gold[1] Q: Solve \(3(2x + 1) = 5(x + 2)\)
   step0 field=say answer=None text='Expand both brackets first.'
   step1 field=pre answer=6 text='Left: 3 × 2x ='
   step2 field=pre answer=10 text='Right: 5 × 2 ='
   step3 field=pre answer=1 text='Collect x: 6x − 5x ='
   step4 field=say answer=None text='So \\(x + 3 = 10\\).'
   step5 field=pre answer=7 text='Take off 3: 10 − 3 ='
   step6 field=pre answer=45 text='Check the left side: 3 × (2 × 7 + 1) ='

gold[3] Q: Solve \(\frac{3(x-1)}{4} = \frac{2x+5}{3}\)
   step0 field=say answer=None text='Cross-multiply: \\(3 × 3(x-1) = 4(2x+5)\\).'
   step1 field=pre answer=9 text='Left coefficient: 3 × 3 ='
   step2 field=pre answer=8 text='Right: 4 × 2x ='
   step3 field=pre answer=1 text='Collect x: 9x − 8x ='
   step4 field=say answer=None text='So \\(x − 9 = 20\\).'
   step5 field=pre answer=29 text='Add 9: 20 + 9 ='
   step6 field=pre answer=21 text='Check the left side: 3 × (29 − 1) ÷ 4 ='

silver[4] Q: Solve \(\frac{x+5}{3} = 4\)
   step0 field=say answer=None text='The whole left side is divided by 3. Multiply both sides by 3 to clear it.'
   step1 field=pre answer=12 text='Multiply both sides by 3: 4 × 3 ='
   step2 field=pre answer=7 text='Take off 5: 12 − 5 ='
   step3 field=pre answer=4 text='Check: (7 + 5) ÷ 3 ='

### board=maths-eduqas
bronze[5] Q: Solve \(x + 9 = 4\)
   step0 field=pre answer=5 text='9 is larger than 4, so the answer drops below zero. First, 9 − 4 ='
   step1 field=pre answer=-5 text='So x is that far below zero: x = 4 − 9 ='
   step2 field=pre answer=4 text='Check: −5 + 9 ='

gold[0] Q: Solve \(\frac{2x + 1}{3} = 5\)
   step0 field=pre answer=15 text='Multiply both sides by 3 to clear the fraction: 5 × 3 ='
   step1 field=pre answer=14 text='Now 2x + 1 = 15. Subtract 1: 15 − 1 ='
   step2 field=pre answer=7 text='So 2x = 14. Divide by 2: 14 ÷ 2 ='
   step3 field=pre answer=5 text='Check: (2 × 7 + 1) ÷ 3 ='

gold[1] Q: Solve \(\frac{x + 3}{4} = \frac{x - 1}{2}\)
   step0 field=pre answer=2 text='Multiply both sides by 4. On the right, 4 ÷ 2 ='
   step1 field=pre answer=1 text='Now x + 3 = 2x − 2. Subtract x: 2x − x ='
   step2 field=pre answer=5 text='So x − 2 = 3. Add 2: 3 + 2 ='
   step3 field=pre answer=2 text='Check left: (5 + 3) ÷ 4 ='

gold[3] Q: Solve \(\frac{5(x-2)}{3} = \frac{2(x+1)}{2} + 1\)
   step0 field=pre answer=2 text='On the right, 2(x + 1) ÷ 2 is just x + 1. Adding the extra 1 gives x + 1 + 1 = x +'
   step1 field=pre answer=6 text='Now (5(x − 2))/3 = x + 2. Multiply both sides by 3. On the right, 3 × 2 ='
   step2 field=pre answer=2 text='So 5(x − 2) = 3x + 6, giving 5x − 10 = 3x + 6. Subtract 3x: 5x − 3x ='
   step3 field=pre answer=16 text='So 2x − 10 = 6. Add 10: 6 + 10 ='
   step4 field=pre answer=8 text='So 2x = 16. Divide by 2: 16 ÷ 2 ='
   step5 field=pre answer=10 text='Check left: 5 × (8 − 2) ÷ 3 ='

silver[4] Q: Solve \(2(3x + 1) = 5x + 9\)
   step0 field=pre answer=6 text='Expand the left. Multiply both terms by 2: 2 × 3 ='
   step1 field=pre answer=1 text='Now 6x + 2 = 5x + 9. Subtract 5x: 6x − 5x ='
   step2 field=pre answer=7 text='So x + 2 = 9. Subtract 2: 9 − 2 ='
   step3 field=pre answer=44 text='Check: 2 × (3 × 7 + 1) ='
