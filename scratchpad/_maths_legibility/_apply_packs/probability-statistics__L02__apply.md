# apply-pack: probability-statistics__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] bronze[0] Q-line (recurs in bronze[1], bronze[2], bronze[3], bronze[5], bronze[6], bronze[7], silver[0], silver[3], silver[6], gold[1]) | Q: MathsScience14810?Total: 4040 students: 22 like maths, 18 like science, 8 lik | fix: Strip the diagram-data prefix out of the question string (render it as the Venn diagram, not as text) so each question opens with its clean sentence, e.g. '40 s
- [medium] silver[4] | Q: Are events A and B independent if P(A) = 0.3, P(B) = 0.4, P(A ∩ B) = 0.12? (m | fix: Add a short walk that builds the test before the choice, e.g. ask 'P(A) × P(B) = 0.3 × 0.4 = [box=0.12]', then 'Compare with P(A ∩ B) = 0.12 — equal, so the eve
- [medium] gold[3] | Check: overlap 0.18, A only 0.12, B only 0.42, neither 0.28 add to [box=1] | fix: Show each region's working inline, e.g. 'Check: overlap 0.3x0.6=0.18, A only 0.3x0.4=0.12, B only 0.7x0.6=0.42, neither 0.28 add to 1' - or simplify the check t

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: MathsScience14810?Total: 4040 students: 22 like maths, 18 like science, 8 like both. How m
   step0 field=say answer=None text='Fill the Venn from the middle out: the overlap first, then each single region, then what i'
   step1 field=pre answer=8 text='Both maths and science (the overlap) ='
   step2 field=pre answer=14 text='Maths only: 22 − 8 ='
   step3 field=pre answer=10 text='Science only: 18 − 8 ='
   step4 field=pre answer=32 text='14 + 8 + 10 ='
   step5 field=pre answer=8 text='Neither: 40 − 32 ='

gold[3] Q: P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A' ∩ B') as a fraction.
   step0 field=say answer=None text="Neither event means A' and B'. For independent events, multiply the complements."
   step1 field=pre answer=0.6 text="P(A') = 1 − 0.4 ="
   step2 field=pre answer=0.5 text="P(B') = 1 − 0.5 ="
   step3 field=pre answer=0.3 text='0.6 × 0.5 ='
   step4 field=pre answer=3 text='Write 0.3 as a fraction. Numerator (0.3 = 3/10) ='
   step5 field=pre answer=10 text='Denominator ='

silver[4] Q: Are events A and B independent if P(A) = 0.3, P(B) = 0.4, P(A ∩ B) = 0.12?

### board=maths-edexcel
bronze[0] Q: Tea 25Coffee 188n = 40? outside40 people: 25 like tea (T), 18 like coffee (C), 8 like both
   step0 field=pre answer=17 text='Tea only, peel off the 8 who also like coffee: 25 − 8 ='
   step1 field=pre answer=10 text='Coffee only: 18 − 8 ='
   step2 field=pre answer=35 text='Add the three regions inside the circles: 17 + 10 + 8 ='
   step3 field=pre answer=5 text='Everyone else likes neither: 40 − 35 ='
   step4 field=pre answer=40 text='Check every region totals 40: 17 + 10 + 8 + 5 ='

gold[3] Q: 0.3A0.5B0.5B'0.7A'0.2B0.8B'P(A) = 0.3, P(B|A) = 0.5, P(B|A') = 0.2. Find P(B). Give to 2 d
   step0 field=pre answer=0.15 text='Route one, B with A: 0.5 × 0.3 ='
   step1 field=pre answer=0.14 text="Route two, B without A (P(A') = 0.7): 0.2 × 0.7 ="
   step2 field=pre answer=0.29 text='B arrives by either route, so add them: 0.15 + 0.14 ='
   step3 field=pre answer=29 text='Check with 100 people: 30 in A give 15, 70 not in A give 14; 15 + 14 ='

silver[4] Q: Sport 60Music 4520n = 100P(music | sport) = ?100 students: 60 play sport, 45 play music, 2
   step0 field=pre answer=60 text='How many play sport (the condition)?'
   step1 field=pre answer=20 text='Of those, how many also play music (the overlap)?'
   step2 field=pre answer=1 text='So it is 20 out of 60. Simplify by dividing by 20. Numerator: 20 ÷ 20 ='
   step3 field=pre answer=3 text='Denominator: 60 ÷ 20 ='
   step4 field=pre answer=20 text='Check: does one third of 60 give the 20 who do both? 60 ÷ 3 ='

### board=maths-ocr
bronze[0] Q: FootballRugby20151312Total: 6060 students: 35 play football, 28 play rugby, 15 play both. 
   step0 field=say answer=None text='Add both totals, then remove the overlap once so no one is counted twice.'
   step1 field=pre answer=35 text='Football total ='
   step2 field=pre answer=28 text='Rugby total ='
   step3 field=pre answer=63 text='Add them: 35 + 28 ='
   step4 field=pre answer=48 text='63 − 15 ='
   step5 field=pre answer=48 text='Check by regions: football only 20, both 15, rugby only 13 add to'

gold[3] Q: P(A) = 0.3, P(B) = 0.6, events independent. P(neither A nor B)?
   step0 field=say answer=None text='Neither means not A and not B. For independent events, multiply the complements.'
   step1 field=pre answer=0.7 text="P(A') = 1 − 0.3 ="
   step2 field=pre answer=0.4 text="P(B') = 1 − 0.6 ="
   step3 field=pre answer=0.28 text='0.7 × 0.4 ='
   step4 field=pre answer=1 text='Check: overlap 0.18, A only 0.12, B only 0.42, neither 0.28 add to'

silver[4] Q: AB0.30.4neither 0.3Total: 1Events A and B are mutually exclusive. P(A) = 0.3, P(B) = 0.4. 
   step0 field=say answer=None text='Mutually exclusive means the events cannot both happen, so the overlap is zero.'
   step1 field=pre answer=0 text='The overlap P(A∩B) for mutually exclusive events ='
   step2 field=pre answer=0.7 text='P(A) + P(B) = 0.3 + 0.4 ='
   step3 field=pre answer=0.7 text='0.7 − 0 ='
   step4 field=pre answer=0.7 text='Check: the two separate slices give 0.3 + 0.4 ='

### board=maths-eduqas
bronze[0] Q: MathsScience181012?Total: 5050 students: 28 like maths, 22 like science, 10 like both. How
   step0 field=say answer=None text='Fill the Venn from the middle out: the overlap first, then each single region, then what i'
   step1 field=pre answer=10 text='Both maths and science (the overlap) ='
   step2 field=pre answer=18 text='Maths only: 28 − 10 ='
   step3 field=pre answer=12 text='Science only: 22 − 10 ='
   step4 field=pre answer=40 text='Add the three filled regions: 18 + 10 + 12 ='
   step5 field=pre answer=10 text='Neither: 50 − 40 ='

gold[3] Q: P(A) = 0.3, P(B) = 0.6. A and B are independent. Find P(A' ∩ B') as a simplified fraction.
   step0 field=say answer=None text="Neither event means A' and B'. For independent events, multiply the complements."
   step1 field=pre answer=0.7 text="P(A') = 1 − 0.3 ="
   step2 field=pre answer=0.4 text="P(B') = 1 − 0.6 ="
   step3 field=pre answer=0.28 text='Independent, so multiply: 0.7 × 0.4 ='
   step4 field=pre answer=7 text='0.28 = 28/100. Simplify by 4, top: 28 ÷ 4 ='
   step5 field=pre answer=25 text='100 ÷ 4 ='

silver[4] Q: Are events A and B independent if P(A) = 0.4, P(B) = 0.3, P(A ∩ B) = 0.12?
