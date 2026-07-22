# apply-pack: algebra__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[1] | Two single fractions equal each other, so cross multiply: multiply the left top  | fix: Add one building sentence at first use: 'Cross multiply means each top is multiplied by the other fraction's bottom: (5x + 2) times the right bottom 2, and (3x 
- [medium] gold[2] | Cross multiply: the left top times 2, the right top times 5. Left: 2 × 2(x − 1)  | fix: Split it up. Say separately: 'The left top is 2(x − 1); multiply it by 2 to get 4(x − 1).' Then ask on its own short line: 'Expand: 4 × (−1) ='.
- [medium] silver[5] | Expand both brackets. First 5(2x + 1) = 10x + 5. Now the tricky one: −3 × (−2) = | fix: Give the first bracket in an intro, then make the ask just the question: 'Expand −3(x − 2). The tricky part is a negative times a negative: −3 × (−2) ='.
- [medium] gold[3] | Expand both sides. Left: 3(2x + 1) = 6x + 3. Right: 2 × (4x − 3) then + 3. 2 × ( | fix: Reword and separate: 'Expand 2(4x − 3) to get 8x − 6, then add the +3 that follows.' Then ask on its own line: '2 × (−3) ='.
- [medium] gold[3] | then ÷ 3 = [box=5, NO label] | fix: Rewrite the ask as the full expression: '15 ÷ 3 ='
- [medium] gold[2] | Divide by 5: 60 ÷ 5 = [box=12, NO label] | fix: Insert a combine step before dividing: 'Add the x terms: 3x + 2x = [box=5, label:'x']', then 'So 5x = 60. Divide by 5: 60 ÷ 5 ='.
- [medium] gold[4] | The second fraction: 4 × (x−1)/2 becomes __(x − 1) [box=2, NO label] | fix: Reword so the box is plainly the coefficient, e.g. 'Cancel: 4 ÷ 2 = [box=2], so 4 × (x−1)/2 = 2(x − 1)'.
- [medium] gold[4] | Take off 1: 16 − 1 = [box=15, NO label] | fix: Add a step that produces the 1, e.g. 'Constants: 3 − 2 = [box=1]', then 'So 3x + 1 = 16. Take off 1: 16 − 1 ='.
- [medium] gold[0] | Collect x: 4x − 3x = [box=1, label:'x'] … So x + 2 = 12. | fix: Box the missing terms too: add 'Expand the right x-term: 3 × x = [box=3, label:'x']' and 'Expand the left constant: 2 × 1 = [box=2]' so every number in 'Collect
- [medium] gold[4] | Cross-multiply. Left numerator times 4 gives 16x − 12. Right numerator times 5:  | fix: Before the boxed step, add a line that names and shows the move: 'Multiply the left numerator (4x − 3) by the right denominator 4: 4 × 4x = 16x and 4 × 3 = 12, 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: Solve \(\frac{x+1}{3} + \frac{x-1}{4} = 3\)
   step0 field=pre answer=4 text='Clear both fractions at once. The bottoms are 3 and 4, and the number both divide into is '
   step1 field=pre answer=3 text='For the second fraction: 12 ÷ 4 ='
   step2 field=pre answer=35 text='36 − 1 ='
   step3 field=pre answer=5 text='35 ÷ 7 ='
   step4 field=pre answer=5 text='So x ='
   step5 field=pre answer=3 text='Check: (5 + 1) ÷ 3 + (5 − 1) ÷ 4 ='

gold[1] Q: Solve \(\frac{5x + 2}{3} = \frac{3x + 8}{2}\)
   step0 field=pre answer=4 text='Two single fractions equal each other, so cross multiply: multiply the left top by 2 and t'
   step1 field=pre answer=24 text='Right side: 3 × (3x + 8). 3 × 8 ='
   step2 field=pre answer=1 text='10x − 9x ='
   step3 field=pre answer=20 text='24 − 4 ='
   step4 field=pre answer=20 text='So x ='
   step5 field=pre answer=34 text='Check: (5 × 20 + 2) ÷ 3 ='

gold[2] Q: Solve \(\frac{2(x-1)}{5} = \frac{x+3}{2}\)
   step0 field=pre answer=-4 text='Cross multiply: the left top times 2, the right top times 5. Left: 2 × 2(x − 1) = 4(x − 1)'
   step1 field=pre answer=15 text='Expand the right: 5 × 3 ='
   step2 field=pre answer=1 text='5x − 4x ='
   step3 field=pre answer=-19 text='−4 − 15 ='
   step4 field=pre answer=-19 text='So x ='
   step5 field=pre answer=-8 text='Check: 2 × (−19 − 1) ÷ 5 ='

gold[3] Q: Solve \(3(2x + 1) = 2(4x - 3) + 3\)
   step0 field=pre answer=-6 text='Expand both sides. Left: 3(2x + 1) = 6x + 3. Right: 2 × (4x − 3) then + 3. 2 × (−3) ='
   step1 field=pre answer=2 text='8x − 6x ='
   step2 field=pre answer=6 text='3 + 3 ='
   step3 field=pre answer=3 text='6 ÷ 2 ='
   step4 field=pre answer=3 text='So x ='
   step5 field=pre answer=21 text='Check: 3 × (2 × 3 + 1) ='

gold[4] Q: Solve \(\frac{7-x}{3} = \frac{x+1}{5}\)
   step0 field=pre answer=35 text='Cross multiply: left top times 5, right top times 3. Left: 5 × (7 − x). 5 × 7 ='
   step1 field=pre answer=3 text='Right: 3 × (x + 1). 3 × 1 ='
   step2 field=pre answer=32 text='35 − 3 ='
   step3 field=pre answer=4 text='32 ÷ 8 ='
   step4 field=pre answer=4 text='So x ='
   step5 field=pre answer=1 text='Check: (7 − 4) ÷ 3 ='

silver[5] Q: Solve \(5(2x + 1) - 3(x - 2) = 25\)
   step0 field=pre answer=6 text='Expand both brackets. First 5(2x + 1) = 10x + 5. Now the tricky one: −3 × (−2) ='
   step1 field=pre answer=14 text='25 − 11 ='
   step2 field=pre answer=2 text='14 ÷ 7 ='
   step3 field=pre answer=2 text='So x ='
   step4 field=pre answer=25 text='Check: 5 × (2 × 2 + 1) − 3 × (2 − 2) ='

### board=maths-edexcel
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

gold[2] Q: Solve \(4(x + 2) = 2(3x − 1)\)
   step0 field=say answer=None text='Expand both brackets first.'
   step1 field=pre answer=4 text='Left: 4 × x ='
   step2 field=pre answer=8 text='Left: 4 × 2 ='
   step3 field=pre answer=6 text='Right: 2 × 3x ='
   step4 field=pre answer=-2 text='Right: 2 × (−1) ='
   step5 field=say answer=None text='So 4x + 8 = 6x − 2. The bigger x-term is on the right, so subtract 4x from both sides.'
   step6 field=pre answer=2 text='6x − 4x ='
   step7 field=say answer=None text='Now 8 = 2x − 2. Add 2 to both sides.'
   step8 field=pre answer=10 text='8 + 2 ='
   step9 field=say answer=None text='So 2x = 10. Now divide both sides by 2.'
   step10 field=pre answer=5 text='10 ÷ 2 ='
   step11 field=say answer=None text='Check both sides with x = 5.'
   step12 field=pre answer=28 text='4 × (5 + 2) ='
   step13 field=pre answer=28 text='2 × (3 × 5 − 1) ='

gold[3] Q: Solve \(\frac{2x + 1}{3} = 5\)
   step0 field=say answer=None text='Clear the fraction: multiply both sides by 3.'
   step1 field=pre answer=15 text='Right: 5 × 3 ='
   step2 field=say answer=None text='So 2x + 1 = 15. Subtract 1 from both sides.'
   step3 field=pre answer=14 text='15 − 1 ='
   step4 field=say answer=None text='So 2x = 14. Now divide both sides by 2.'
   step5 field=pre answer=7 text='14 ÷ 2 ='
   step6 field=say answer=None text='Check x = 7 in the original.'
   step7 field=pre answer=15 text='2 × 7 + 1 ='
   step8 field=pre answer=5 text='then ÷ 3 ='

gold[4] Q: Solve \(7(x − 2) = 3(2x + 1)\)
   step0 field=say answer=None text='Expand both brackets first.'
   step1 field=pre answer=7 text='Left: 7 × x ='
   step2 field=pre answer=-14 text='Left: 7 × (−2) ='
   step3 field=pre answer=6 text='Right: 3 × 2x ='
   step4 field=pre answer=3 text='Right: 3 × 1 ='
   step5 field=say answer=None text='So 7x − 14 = 6x + 3. Subtract 6x from both sides.'
   step6 field=pre answer=1 text='7x − 6x ='
   step7 field=say answer=None text='Now x − 14 = 3. Add 14 to both sides.'
   step8 field=pre answer=17 text='3 + 14 ='
   step9 field=say answer=None text='So x = 17. Check both sides.'
   step10 field=pre answer=105 text='7 × (17 − 2) ='
   step11 field=pre answer=105 text='3 × (2 × 17 + 1) ='

silver[5] Q: Solve \(4(x − 2) = 20\)
   step0 field=say answer=None text='Expand the bracket: multiply everything inside by 4.'
   step1 field=pre answer=4 text='4 × x ='
   step2 field=pre answer=-8 text='4 × (−2) ='
   step3 field=say answer=None text='So 4x − 8 = 20. Undo the −8 by adding 8 to both sides.'
   step4 field=pre answer=28 text='20 + 8 ='
   step5 field=say answer=None text='So 4x = 28. Now divide both sides by 4.'
   step6 field=pre answer=7 text='28 ÷ 4 ='
   step7 field=say answer=None text='Check x = 7 in the original.'
   step8 field=pre answer=20 text='4 × (7 − 2) ='

### board=maths-ocr
gold[0] Q: Solve \(\frac{2x+1}{3} = \frac{x+4}{2}\)
   step0 field=say answer=None text='Cross-multiply to clear the fractions: \\(2(2x+1) = 3(x+4)\\).'
   step1 field=pre answer=4 text='Expand the left: 2 × 2x ='
   step2 field=pre answer=12 text='Expand the right: 3 × 4 ='
   step3 field=pre answer=1 text='Collect x: 4x − 3x ='
   step4 field=say answer=None text='So \\(x + 2 = 12\\).'
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

gold[2] Q: Solve \(\frac{x}{2} + \frac{x}{3} = 10\)
   step0 field=say answer=None text='The denominators are 2 and 3, so the lowest common denominator is 6. Multiply every term b'
   step1 field=pre answer=3 text='First term: 6 × x/2 ='
   step2 field=pre answer=2 text='Second term: 6 × x/3 ='
   step3 field=pre answer=60 text='Right side: 6 × 10 ='
   step4 field=pre answer=12 text='Divide by 5: 60 ÷ 5 ='
   step5 field=pre answer=10 text='Check: 12 ÷ 2 + 12 ÷ 3 ='

gold[3] Q: Solve \(\frac{3(x-1)}{4} = \frac{2x+5}{3}\)
   step0 field=say answer=None text='Cross-multiply: \\(3 × 3(x-1) = 4(2x+5)\\).'
   step1 field=pre answer=9 text='Left coefficient: 3 × 3 ='
   step2 field=pre answer=8 text='Right: 4 × 2x ='
   step3 field=pre answer=1 text='Collect x: 9x − 8x ='
   step4 field=say answer=None text='So \\(x − 9 = 20\\).'
   step5 field=pre answer=29 text='Add 9: 20 + 9 ='
   step6 field=pre answer=21 text='Check the left side: 3 × (29 − 1) ÷ 4 ='

gold[4] Q: Solve \(\frac{x+3}{4} + \frac{x-1}{2} = 4\)
   step0 field=say answer=None text='The denominators are 4 and 2, so the lowest common denominator is 4. Multiply every term b'
   step1 field=pre answer=2 text='The second fraction: 4 × (x−1)/2 becomes __(x − 1)'
   step2 field=pre answer=16 text='Right side: 4 × 4 ='
   step3 field=pre answer=3 text='Expand and collect x: x + 2x ='
   step4 field=pre answer=15 text='Take off 1: 16 − 1 ='
   step5 field=say answer=None text='So \\(3x = 15\\).'
   step6 field=pre answer=5 text='Divide by 3: 15 ÷ 3 ='
   step7 field=pre answer=4 text='Check: (5+3)÷4 + (5−1)÷2 ='

silver[5] Q: Solve \(4(x - 2) = 3(x + 1)\)
   step0 field=say answer=None text='Expand both brackets first.'
   step1 field=pre answer=-8 text='Left: 4 × (−2) ='
   step2 field=pre answer=3 text='Right: 3 × 1 ='
   step3 field=pre answer=1 text='Collect x: 4x − 3x ='
   step4 field=say answer=None text='So \\(x − 8 = 3\\).'
   step5 field=pre answer=11 text='Add 8: 3 + 8 ='
   step6 field=pre answer=36 text='Check the left side: 4 × (11 − 2) ='

### board=maths-eduqas
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

gold[2] Q: Solve \(\frac{3x}{5} + 2 = \frac{x}{2} + 4\)
   step0 field=pre answer=20 text='Multiply every term by 10. The 3x/5 becomes 6x, the x/2 becomes 5x, and 10 × 2 ='
   step1 field=pre answer=40 text='The 4 becomes 10 × 4 ='
   step2 field=pre answer=1 text='Now 6x + 20 = 5x + 40. Subtract 5x: 6x − 5x ='
   step3 field=pre answer=20 text='So x + 20 = 40. Subtract 20: 40 − 20 ='
   step4 field=pre answer=14 text='Check left: 3 × 20 ÷ 5 + 2 ='

gold[3] Q: Solve \(\frac{5(x-2)}{3} = \frac{2(x+1)}{2} + 1\)
   step0 field=pre answer=2 text='On the right, 2(x + 1) ÷ 2 is just x + 1. Adding the extra 1 gives x + 1 + 1 = x +'
   step1 field=pre answer=6 text='Now (5(x − 2))/3 = x + 2. Multiply both sides by 3. On the right, 3 × 2 ='
   step2 field=pre answer=2 text='So 5(x − 2) = 3x + 6, giving 5x − 10 = 3x + 6. Subtract 3x: 5x − 3x ='
   step3 field=pre answer=16 text='So 2x − 10 = 6. Add 10: 6 + 10 ='
   step4 field=pre answer=8 text='So 2x = 16. Divide by 2: 16 ÷ 2 ='
   step5 field=pre answer=10 text='Check left: 5 × (8 − 2) ÷ 3 ='

gold[4] Q: Solve \(\frac{4x - 3}{5} = \frac{3x + 2}{4}\)
   step0 field=pre answer=15 text='Cross-multiply. Left numerator times 4 gives 16x − 12. Right numerator times 5: 5 × 3x ='
   step1 field=pre answer=10 text='And 5 × 2 ='
   step2 field=pre answer=1 text='Now 16x − 12 = 15x + 10. Subtract 15x: 16x − 15x ='
   step3 field=pre answer=22 text='So x − 12 = 10. Add 12: 10 + 12 ='
   step4 field=pre answer=17 text='Check left: (4 × 22 − 3) ÷ 5 ='

silver[5] Q: Solve \(8 - 2x = 3x - 2\)
   step0 field=pre answer=5 text='Add 2x to both sides so no x is negative. On the right, 3x + 2x ='
   step1 field=pre answer=10 text='Now 8 = 5x − 2. Add 2: 8 + 2 ='
   step2 field=pre answer=2 text='So 5x = 10. Divide by 5: 10 ÷ 5 ='
   step3 field=pre answer=4 text='Check: 8 − 2 × 2 ='
