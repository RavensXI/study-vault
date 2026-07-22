# apply-pack: algebra__L09.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[4] | -3y = 1 − 10 = [box=-9] ... then bare box y = [box=3] | fix: Insert an intermediate line before the 'y =' box, e.g. 'Divide both sides by -3. A negative divided by a negative is positive, so y = 3.'
- [medium] silver[4] | Now find y. Put x = 1 into x + 2y = 11. → ask: 2y = 11 − 1 = [box=10, NO label] | fix: Add a bridge sentence matching the gold style, e.g. intro: 'The x part is just 1, so take it off both sides:' before the '2y = 11 − 1' ask.
- [medium] gold[0], gold[1] (pattern recurs across pack) | -2y = 11 − 15 = [-4] then y = [2] | fix: Add an explicit divide step before the 'y =' box, e.g. an intro 'Now divide both sides by -2:' with a box 'y = -4 ÷ -2 =', mirroring the granular style used for

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: A café sells coffee and tea. 3 coffees and 2 teas cost £11.50. 2 coffees and 3 teas cost £
   step0 field=say answer=None text='Write a coffee as \\(x\\) and a tea as \\(y\\): \\(3x + 2y = 11.5\\) and \\(2x + 3y = 11\\). Match'
   step1 field=pre answer=9 text='3x × 3 ='
   step2 field=pre answer=6 text='2y × 3 ='
   step3 field=pre answer=34.5 text='and the right-hand side: 11.5 × 3 ='
   step4 field=pre answer=4 text='2x × 2 ='
   step5 field=pre answer=6 text='3y × 2 ='
   step6 field=pre answer=22 text='and the right-hand side: 11 × 2 ='
   step7 field=pre answer=5 text='9x − 4x ='
   step8 field=pre answer=0 text='6y − 6y ='
   step9 field=pre answer=12.5 text='34.5 − 22 ='
   step10 field=pre answer=2.5 text='x ='
   step11 field=pre answer=6 text='3y = 11 − 5 ='
   step12 field=pre answer=2 text='y ='
   step13 field=pre answer=11.5 text='3 × 2.5 + 2 × 2 ='

silver[4] Q: Solve \(4x - y = 17\) and \(2x + 3y = 19\)
   step0 field=pre answer=12 text='4x × 3 ='
   step1 field=pre answer=-3 text='−y × 3 ='
   step2 field=pre answer=51 text='and the right-hand side: 17 × 3 ='
   step3 field=pre answer=14 text='12x + 2x ='
   step4 field=pre answer=0 text='−3y + 3y ='
   step5 field=pre answer=70 text='51 + 19 ='
   step6 field=pre answer=5 text='x ='
   step7 field=pre answer=3 text='20 − y = 17 → y ='
   step8 field=pre answer=19 text='2 × 5 + 3 × 3 ='

### board=maths-edexcel
gold[0] Q: Solve \(3x + 4y = 25\) and \(2x + 3y = 18\)
   step0 field=pre answer=9 text='3x × 3 ='
   step1 field=pre answer=12 text='4y × 3 ='
   step2 field=pre answer=75 text='and the right-hand side: 25 × 3 ='
   step3 field=pre answer=8 text='2x × 4 ='
   step4 field=pre answer=12 text='3y × 4 ='
   step5 field=pre answer=72 text='and the right-hand side: 18 × 4 ='
   step6 field=pre answer=1 text='9x − 8x ='
   step7 field=pre answer=0 text='12y − 12y ='
   step8 field=pre answer=3 text='75 − 72 ='
   step9 field=say answer=None text='So x = 3. Done in one.'
   step10 field=pre answer=12 text='3y = 18 − 6 ='
   step11 field=pre answer=4 text='y ='
   step12 field=pre answer=25 text='3 × 3 + 4 × 4 ='

gold[4] Q: Solve \(5x - 3y = 1\) and \(2x + 7y = 25\)
   step0 field=pre answer=35 text='5x × 7 ='
   step1 field=pre answer=-21 text='-3y × 7 ='
   step2 field=pre answer=7 text='and the right-hand side: 1 × 7 ='
   step3 field=pre answer=6 text='2x × 3 ='
   step4 field=pre answer=21 text='7y × 3 ='
   step5 field=pre answer=75 text='and the right-hand side: 25 × 3 ='
   step6 field=pre answer=41 text='35x + 6x ='
   step7 field=pre answer=0 text='-21y + 21y ='
   step8 field=pre answer=82 text='7 + 75 ='
   step9 field=pre answer=2 text='x ='
   step10 field=pre answer=-9 text='-3y = 1 − 10 ='
   step11 field=pre answer=3 text='y ='
   step12 field=pre answer=25 text='2 × 2 + 7 × 3 ='

silver[4] Q: Solve \(x + 4y = 17\) and \(3x + 2y = 11\)
   step0 field=pre answer=6 text='3x × 2 ='
   step1 field=pre answer=4 text='2y × 2 ='
   step2 field=pre answer=22 text='and the right-hand side: 11 × 2 ='
   step3 field=pre answer=5 text='6x − x ='
   step4 field=pre answer=0 text='4y − 4y ='
   step5 field=pre answer=5 text='22 − 17 ='
   step6 field=pre answer=1 text='x ='
   step7 field=pre answer=8 text='2y = 11 − 3 ='
   step8 field=pre answer=4 text='y ='
   step9 field=pre answer=17 text='1 + 4 × 4 ='

### board=maths-ocr
gold[0] Q: Solve \(2x + 3y = 12\) and \(5x - 2y = 11\)
   step0 field=pre answer=4 text='2x × 2 ='
   step1 field=pre answer=6 text='3y × 2 ='
   step2 field=pre answer=24 text='and the right-hand side: 12 × 2 ='
   step3 field=pre answer=15 text='5x × 3 ='
   step4 field=pre answer=-6 text='-2y × 3 ='
   step5 field=pre answer=33 text='and the right-hand side: 11 × 3 ='
   step6 field=pre answer=19 text='4x + 15x ='
   step7 field=pre answer=0 text='6y + (-6y) ='
   step8 field=pre answer=57 text='24 + 33 ='
   step9 field=pre answer=3 text='x ='
   step10 field=pre answer=6 text='3y = 12 − 6 ='
   step11 field=pre answer=2 text='y ='
   step12 field=pre answer=11 text='5 × 3 − 2 × 2 ='

silver[4] Q: Solve \(3x + 4y = 23\) and \(x + 2y = 11\)
   step0 field=pre answer=2 text='x × 2 ='
   step1 field=pre answer=4 text='2y × 2 ='
   step2 field=pre answer=22 text='and the right-hand side: 11 × 2 ='
   step3 field=pre answer=1 text='3x − 2x ='
   step4 field=pre answer=0 text='4y − 4y ='
   step5 field=pre answer=1 text='23 − 22 ='
   step6 field=say answer=None text='So x = 1. Done in one.'
   step7 field=pre answer=10 text='2y = 11 − 1 ='
   step8 field=pre answer=5 text='y ='
   step9 field=pre answer=23 text='3 × 1 + 4 × 5 ='

### board=maths-eduqas
gold[0] Q: Solve \(2x + 3y = 12\) and \(5x - 2y = 11\)
   step0 field=pre answer=4 text='2x × 2 ='
   step1 field=pre answer=6 text='3y × 2 ='
   step2 field=pre answer=24 text='and the right-hand side: 12 × 2 ='
   step3 field=pre answer=15 text='5x × 3 ='
   step4 field=pre answer=-6 text='-2y × 3 ='
   step5 field=pre answer=33 text='and the right-hand side: 11 × 3 ='
   step6 field=pre answer=19 text='4x + 15x ='
   step7 field=pre answer=0 text='6y + (-6y) ='
   step8 field=pre answer=57 text='24 + 33 ='
   step9 field=pre answer=3 text='x ='
   step10 field=pre answer=-4 text='-2y = 11 − 15 ='
   step11 field=pre answer=2 text='y ='
   step12 field=pre answer=12 text='2 × 3 + 3 × 2 ='

gold[4] Q: Solve \(3x + 5y = 21\) and \(5x + 2y = 16\)
   step0 field=pre answer=15 text='3x × 5 ='
   step1 field=pre answer=25 text='5y × 5 ='
   step2 field=pre answer=105 text='and the right-hand side: 21 × 5 ='
   step3 field=pre answer=15 text='5x × 3 ='
   step4 field=pre answer=6 text='2y × 3 ='
   step5 field=pre answer=48 text='and the right-hand side: 16 × 3 ='
   step6 field=pre answer=19 text='25y − 6y ='
   step7 field=pre answer=0 text='15x − 15x ='
   step8 field=pre answer=57 text='105 − 48 ='
   step9 field=pre answer=3 text='y ='
   step10 field=pre answer=10 text='5x = 16 − 6 ='
   step11 field=pre answer=2 text='x ='
   step12 field=pre answer=21 text='3 × 2 + 5 × 3 ='

silver[4] Q: Solve \(3x + 2y = 13\) and \(x - y = 1\)
   step0 field=pre answer=2 text='x × 2 ='
   step1 field=pre answer=-2 text='-y × 2 ='
   step2 field=pre answer=2 text='and the right-hand side: 1 × 2 ='
   step3 field=pre answer=5 text='3x + 2x ='
   step4 field=pre answer=0 text='2y + (-2y) ='
   step5 field=pre answer=15 text='13 + 2 ='
   step6 field=pre answer=3 text='x ='
   step7 field=pre answer=2 text='3 − y = 1 → y ='
   step8 field=pre answer=13 text='3 × 3 + 2 × 2 ='
