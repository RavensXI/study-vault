# apply-pack: algebra__L09.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[3] | Replace y: 2x + (3x - 1). Collect the x terms: 2x + 3x = [box=5, label:'x'] | fix: Split into two steps: (1) 'Replace y with (3x - 1). The equation becomes 2x + (3x - 1) = 14.' then (2) 'Collect the x terms: 2x + 3x = [box, label:x]'.
- [low] bronze[1] (also bronze[3], silver[0], silver[1], gold[0]) | So x = 4. Done in one. | fix: Replace with plain wording, e.g. 'So x = 4 — the subtracting gave x straight away, with no dividing needed.'
- [low] gold[0], gold[1] | So 19x = 57. → ask: x = [box=3, NO label] (and gold[1]: So 17x = 51. → x = [box= | fix: Show the division explicitly for the awkward cases, e.g. add an ask 'ask: 57 ÷ 19 = [box=3]' or an intro 'Divide both sides by 19:' before the 'x =' box.
- [low] bronze[0] (also bronze[1,2,3,7], silver[0,1,2], gold[2]) | 7 + y = 10 → y = [3] | fix: Show the subtraction as its own box to match the harder-problem style, e.g. 'y = 10 − 7 =', and/or replace the '→' with the word 'so'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: Solve \(x + y = 10\) and \(x - y = 4\)
   step0 field=pre answer=2 text='x + x ='
   step1 field=pre answer=0 text='y + (−y) ='
   step2 field=pre answer=14 text='10 + 4 ='
   step3 field=pre answer=7 text='x ='
   step4 field=pre answer=3 text='7 + y = 10 → y ='
   step5 field=pre answer=4 text='7 − 3 ='

bronze[1] Q: Solve \(2x + y = 9\) and \(x + y = 5\)
   step0 field=pre answer=1 text='2x − x ='
   step1 field=pre answer=0 text='y − y ='
   step2 field=pre answer=4 text='9 − 5 ='
   step3 field=say answer=None text='So x = 4. Done in one.'
   step4 field=pre answer=1 text='4 + y = 5 → y ='
   step5 field=pre answer=9 text='2 × 4 + 1 ='

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

silver[3] Q: Solve \(y = 3x - 1\) and \(2x + y = 14\)
   step0 field=say answer=None text='One equation is already rearranged: \\(y = 3x - 1\\). Substitute it into \\(2x + y = 14\\) in '
   step1 field=pre answer=5 text='Replace y: 2x + (3x - 1). Collect the x terms: 2x + 3x ='
   step2 field=pre answer=15 text='So 5x - 1 = 14. Add 1 to both sides: 5x ='
   step3 field=pre answer=3 text='x ='
   step4 field=pre answer=8 text='y = 3 × 3 − 1 ='
   step5 field=pre answer=14 text='2 × 3 + 8 ='

### board=maths-edexcel
bronze[0] Q: Solve \(x + y = 8\) and \(x - y = 2\)
   step0 field=pre answer=2 text='x + x ='
   step1 field=pre answer=0 text='y + (-y) ='
   step2 field=pre answer=10 text='8 + 2 ='
   step3 field=pre answer=5 text='x ='
   step4 field=pre answer=3 text='5 + y = 8 → y ='
   step5 field=pre answer=2 text='5 − 3 ='

bronze[1] Q: Solve \(2x + y = 9\) and \(x + y = 5\)
   step0 field=pre answer=1 text='2x − x ='
   step1 field=pre answer=0 text='y − y ='
   step2 field=pre answer=4 text='9 − 5 ='
   step3 field=say answer=None text='So x = 4. Done in one.'
   step4 field=pre answer=1 text='4 + y = 5 → y ='
   step5 field=pre answer=9 text='2 × 4 + 1 ='

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

silver[3] Q: Solve \(5x - y = 5\) and \(2x + 3y = 19\)
   step0 field=pre answer=15 text='5x × 3 ='
   step1 field=pre answer=-3 text='-y × 3 ='
   step2 field=pre answer=15 text='and the right-hand side: 5 × 3 ='
   step3 field=pre answer=17 text='15x + 2x ='
   step4 field=pre answer=0 text='-3y + 3y ='
   step5 field=pre answer=34 text='15 + 19 ='
   step6 field=pre answer=2 text='x ='
   step7 field=pre answer=5 text='10 − y = 5 → y ='
   step8 field=pre answer=19 text='2 × 2 + 3 × 5 ='

### board=maths-ocr
bronze[0] Q: Solve \(x + y = 10\) and \(x - y = 4\)
   step0 field=pre answer=2 text='x + x ='
   step1 field=pre answer=0 text='y + (-y) ='
   step2 field=pre answer=14 text='10 + 4 ='
   step3 field=pre answer=7 text='x ='
   step4 field=pre answer=3 text='7 + y = 10 → y ='
   step5 field=pre answer=4 text='7 − 3 ='

bronze[1] Q: Solve \(2x + y = 9\) and \(x + y = 6\)
   step0 field=pre answer=1 text='2x − x ='
   step1 field=pre answer=0 text='y − y ='
   step2 field=pre answer=3 text='9 − 6 ='
   step3 field=say answer=None text='So x = 3. Done in one.'
   step4 field=pre answer=3 text='3 + y = 6 → y ='
   step5 field=pre answer=9 text='2 × 3 + 3 ='

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

silver[3] Q: Solve \(5x - 2y = 4\) and \(x + y = 5\)
   step0 field=pre answer=2 text='x × 2 ='
   step1 field=pre answer=2 text='y × 2 ='
   step2 field=pre answer=10 text='and the right-hand side: 5 × 2 ='
   step3 field=pre answer=7 text='5x + 2x ='
   step4 field=pre answer=0 text='-2y + 2y ='
   step5 field=pre answer=14 text='4 + 10 ='
   step6 field=pre answer=2 text='x ='
   step7 field=pre answer=3 text='2 + y = 5 → y ='
   step8 field=pre answer=4 text='5 × 2 − 2 × 3 ='

### board=maths-eduqas
bronze[0] Q: Solve \(x + y = 10\) and \(x - y = 4\)
   step0 field=pre answer=2 text='x + x ='
   step1 field=pre answer=0 text='y + (-y) ='
   step2 field=pre answer=14 text='10 + 4 ='
   step3 field=pre answer=7 text='x ='
   step4 field=pre answer=3 text='7 + y = 10 → y ='
   step5 field=pre answer=4 text='7 − 3 ='

bronze[1] Q: Solve \(2x + y = 9\) and \(x + y = 6\)
   step0 field=pre answer=1 text='2x − x ='
   step1 field=pre answer=0 text='y − y ='
   step2 field=pre answer=3 text='9 − 6 ='
   step3 field=say answer=None text='So x = 3. Done in one.'
   step4 field=pre answer=3 text='3 + y = 6 → y ='
   step5 field=pre answer=9 text='2 × 3 + 3 ='

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
   step11 field=pre answer=2 text='Now divide both sides by −2. A negative divided by a negative gives a positive, so y ='
   step12 field=pre answer=12 text='2 × 3 + 3 × 2 ='

silver[3] Q: Solve \(3x + 4y = 18\) and \(x + 2y = 8\)
   step0 field=pre answer=2 text='x × 2 ='
   step1 field=pre answer=4 text='2y × 2 ='
   step2 field=pre answer=16 text='and the right-hand side: 8 × 2 ='
   step3 field=pre answer=1 text='3x − 2x ='
   step4 field=pre answer=0 text='4y − 4y ='
   step5 field=pre answer=2 text='18 − 16 ='
   step6 field=say answer=None text='So x = 2. Done in one.'
   step7 field=pre answer=6 text='2y = 8 − 2 ='
   step8 field=pre answer=3 text='y ='
   step9 field=pre answer=18 text='3 × 2 + 4 × 3 ='
