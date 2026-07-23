# apply-pack: probability-statistics__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[1] | Pick 1 P(red) = 8 over [box=12, NO label] | fix: Reword to match the sibling steps, e.g. 'Pick 1: total balls = [box=12]' or 'Pick 1 P(red) = 8 out of a total of [box=12]'.
- [low] silver[1] | Check via 4 x 5 = 20, then two decimal places gives 0.2. Type 4 x 5 = [box=20] | fix: Split it: ask 'Multiply the digits: 4 x 5 = [box]' first, then give the place-value note ('shift two decimal places -> 0.2') as a following sentence.
- [low] silver[5] | and the bottom stays [box=15] | fix: Make it self-contained: 'and the bottom is still 15 (fifteenths): [box]'.
- [low] bronze[5] | Check: favourable 3 + below-3 count = [box=5, NO label] | fix: Reword to plain language: 'Check: the 3 sections we want, plus the 2 sections below 3, should total all 5. 3 + 2 ='.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[5] Q: A bag has 2 red, 3 green and 5 blue. Find P(green).
   step0 field=say answer=None text='Total everything first, then put greens over the total.'
   step1 field=pre answer=10 text='Total balls: 2 + 3 + 5 ='
   step2 field=pre answer=3 text='How many green?'
   step3 field=pre answer=3 text='Numerator ='
   step4 field=pre answer=10 text='Denominator ='

gold[1] Q: 8/127/116/10RRR14/55A bag has 8 red and 4 blue. Three are picked without replacement. Find
   step0 field=say answer=None text='Three reds without replacement: reds and total drop each pick.'
   step1 field=pre answer=12 text='Pick 1 P(red) = 8 over'
   step2 field=pre answer=11 text='Pick 2: reds now 7, total now'
   step3 field=pre answer=10 text='Pick 3: reds now 6, total now'
   step4 field=pre answer=336 text='Multiply tops: 8 × 7 × 6 ='
   step5 field=pre answer=1320 text='12 × 11 × 10 ='
   step6 field=pre answer=14 text='336 ÷ 24 ='
   step7 field=pre answer=55 text='1320 ÷ 24 ='

silver[1] Q: 6/104/10RB6/104/106/104/10RRRBBRBBA bag has 6 red and 4 blue. Two are picked with replacem
   step0 field=say answer=None text='With replacement the bag is the same each time. P(blue) = 4/10 both picks.'
   step1 field=pre answer=4 text='P(blue) numerator ='
   step2 field=pre answer=10 text='P(blue) denominator ='
   step3 field=pre answer=16 text='Multiply tops: 4 × 4 ='
   step4 field=pre answer=100 text='10 × 10 ='
   step5 field=pre answer=4 text='16 ÷ 4 ='
   step6 field=pre answer=25 text='100 ÷ 4 ='

silver[5] Q: A bag has 4 red, 3 blue, 3 green. One is picked. Find P(red or green) as a fraction.
   step0 field=say answer=None text='One pick, two acceptable colours: this is OR, so add the probabilities.'
   step1 field=pre answer=10 text='Total balls: 4 + 3 + 3 ='
   step2 field=pre answer=7 text='Reds = 4, greens = 3. Reds plus greens ='
   step3 field=pre answer=7 text='Numerator ='
   step4 field=pre answer=10 text='Denominator ='

### board=maths-edexcel
bronze[5] Q: Two coins are tossed. Find P(at least one head). Give as a fraction.
   step0 field=say answer=None text='List all outcomes of two coins: HH, HT, TH, TT. That is the sample space.'
   step1 field=pre answer=4 text='How many outcomes are there in total?'
   step2 field=pre answer=3 text='How many have at least one head? (all except TT)'
   step3 field=pre answer=4 text='So the bottom of the fraction is'
   step4 field=pre answer=3 text='Check: only TT has no head, and that is 1 outcome, so 4 − 1 ='

gold[1] Q: The probability of passing a driving test is 0.7. Find the probability of passing on exact
   step0 field=say answer=None text='Exactly the 3rd attempt means fail, fail, then pass. P(fail) = 1 − 0.7.'
   step1 field=pre answer=0.3 text='P(fail) = 1 − 0.7 ='
   step2 field=pre answer=0.063 text='Multiply the three in order: 0.3 × 0.3 × 0.7 ='
   step3 field=pre answer=63 text='Check with whole numbers: 3 × 3 × 7 ='

silver[1] Q: P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A and B). Give as a decimal.
   step0 field=say answer=None text="Independent 'A and B' means both happen, so multiply the two probabilities."
   step1 field=pre answer=0.4 text='Write P(A) ='
   step2 field=pre answer=0.2 text='P(A and B) = 0.4 × 0.5 ='
   step3 field=pre answer=20 text='Check via 4 × 5 = 20, then two decimal places gives 0.2. Type 4 × 5 ='

silver[5] Q: 6/104/10RB????RRRBBRBBA bag has 6 red, 4 blue. Two drawn without replacement. Find P(at le
   step0 field=say answer=None text="'At least one red' is easier as 1 minus its opposite, P(both blue). Blue draws: 4/10 then "
   step1 field=pre answer=3 text='After one blue leaves, blues left ='
   step2 field=pre answer=9 text='Total balls left ='
   step3 field=pre answer=2 text='P(both blue) = (4/10)(3/9) = 12/90. Simplify by 6: top 12 ÷ 6 ='
   step4 field=pre answer=15 text='and bottom 90 ÷ 6 ='
   step5 field=pre answer=13 text='P(at least one red) = 1 − 2/15. As fifteenths the top is 15 − 2 ='
   step6 field=pre answer=15 text='and the bottom stays'

### board=maths-ocr
bronze[5] Q: A fair spinner has sections 1-5. P(3 or higher).
   step0 field=pre answer=3 text='How many sections are 3, 4 or 5?'
   step1 field=pre answer=5 text='How many sections in total?'
   step2 field=pre answer=2 text='So P(3 or higher) = 3/5. Sections below 3 are 1 and 2. How many is that?'
   step3 field=pre answer=5 text='Check: favourable 3 + below-3 count ='

gold[1] Q: P(rain Mon) = 0.3, P(rain Tue) = 0.4 (independent). P(rain at least one day). Give as a de
   step0 field=pre answer=0.7 text='P(no rain Mon), 1 − 0.3 ='
   step1 field=pre answer=0.6 text='P(no rain Tue), 1 − 0.4 ='
   step2 field=pre answer=0.42 text='P(no rain either day) = 0.7 × 0.6 ='
   step3 field=pre answer=0.58 text="'At least one' is everything else. 1 − 0.42 ="
   step4 field=pre answer=1 text='Check the two opposites total 1: 0.58 + 0.42 ='

silver[1] Q: 5/83/85/83/85/83/8RRRBBRBBBag: 5 red, 3 blue. Two drawn WITH replacement. P(both red).
   step0 field=pre answer=5 text='P(red) on the first draw, top number:'
   step1 field=pre answer=5 text='P(red) on the second draw is the same, top number:'
   step2 field=pre answer=25 text='Multiply along the branches: (5/8) × (5/8). New top, 5 × 5 ='
   step3 field=pre answer=64 text='New bottom, 8 × 8 ='
   step4 field=pre answer=8 text='Check the first-draw branches cover the bag: red 5 + blue 3 ='

silver[5] Q: P(A) = 0.6. P(not A)?
   step0 field=pre answer=0.6 text='P(A) ='
   step1 field=pre answer=0.4 text='P(not A) is what is left to reach 1. 1 − 0.6 ='
   step2 field=pre answer=1 text='Check they total 1: 0.6 + 0.4 ='

### board=maths-eduqas
bronze[5] Q: P(rain) = 0.2. The event is repeated 50 times. Find the expected number of rainy days.
   step0 field=say answer=None text='Expected number = probability × number of trials.'
   step1 field=pre answer=0.2 text='The probability of rain each day ='
   step2 field=pre answer=50 text='Number of days (trials) ='
   step3 field=pre answer=10 text='0.2 × 50 ='
   step4 field=pre answer=0.2 text='Check: 10 ÷ 50 ='

gold[1] Q: 7/106/95/8RRR7/24A bag has 7 red and 3 blue. Three are picked without replacement. Find P(
   step0 field=say answer=None text='Three reds without replacement: reds and total both drop each pick.'
   step1 field=pre answer=10 text='Pick 1 P(red) = 7 over'
   step2 field=pre answer=9 text='Pick 2: reds now 6, total now'
   step3 field=pre answer=8 text='Pick 3: reds now 5, total now'
   step4 field=pre answer=210 text='Multiply tops: 7 × 6 × 5 ='
   step5 field=pre answer=7 text='210 ÷ 30 ='
   step6 field=pre answer=24 text='720 ÷ 30 ='

silver[1] Q: 6/104/10RB6/104/106/104/10RRRBBRBBA bag has 6 red and 4 blue. Two are picked with replacem
   step0 field=say answer=None text='With replacement the bag is the same each time. P(blue) = 4/10 both picks.'
   step1 field=pre answer=4 text='P(blue) numerator ='
   step2 field=pre answer=10 text='P(blue) denominator ='
   step3 field=pre answer=16 text='Multiply tops: 4 × 4 ='
   step4 field=pre answer=100 text='Multiply bottoms: 10 × 10 ='
   step5 field=pre answer=4 text='16 ÷ 4 ='
   step6 field=pre answer=25 text='100 ÷ 4 ='

silver[5] Q: 2/32/32/3LLL8/27A spinner has P(win) = 1/3. It is spun 3 times. Find P(no wins) as a simpl
   step0 field=say answer=None text='No wins in three spins means losing every spin. P(lose) = 1 − 1/3.'
   step1 field=pre answer=2 text='P(lose) numerator (1 − 1/3 = 2/3) ='
   step2 field=pre answer=3 text='P(lose) denominator ='
   step3 field=pre answer=8 text='Cube the top: 2 × 2 × 2 ='
   step4 field=pre answer=27 text='Cube the bottom: 3 × 3 × 3 ='
