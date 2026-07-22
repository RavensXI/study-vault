# apply-pack: probability-statistics__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[0] | Q: 1/21/2HT1/21/21/21/2HHHTTHTTA coin is flipped twice. Find P(two heads) as a f | fix: Ensure the tree diagram renders as a separate figure; the question stem should contain only the sentence (e.g. 'A coin is flipped twice. Find P(two heads) as a 
- [high] gold[2] | Q: +112233445566234567345678456789567891067891011789101112Two dice are rolled. F | fix: Separate the dice-total table from the question text so the stem reads cleanly: 'Two dice are rolled. Find the probability the total is 7. Give as a fraction.' 
- [medium] silver[0] | Q: 3/107/10RB3/107/103/107/10RRRBBRBBA bag has 3 red, 7 blue. | fix: Render the tree diagram separately from the stem so the question begins at 'A bag has 3 red and 7 blue balls. Two are drawn WITH replacement...'
- [medium] bronze[0] | Q: 12345A spinner has sections 1-5 (equally likely). | fix: Separate the spinner label from the stem so it reads 'A spinner has sections 1-5 (equally likely)...'; show the section values in the diagram, not inline.
- [medium] gold[4] | So p^2 - p + 0.24 = 0. The discriminant is 1 - 4(0.24) = 1 - 0.96 = [box=0.04] . | fix: Add a scaffolding line before the discriminant step, e.g. 'For p^2 - p + 0.24 = 0 use the quadratic formula p = (1 +/- sqrt(1 - 4x0.24)) / 2', so 'discriminant'
- [medium] gold[3] | Check: with 5 blue, P = (5/10)(4/9) = 20/90. Simplify: 90 / 45 = [box=2] | fix: Reword the check to match the simplification actually shown, e.g. '20/90 divides by 10: top 20 / 10 = [box=2]' so the divisor is visible and consistent.
- [medium] gold[0] | Total balls = 8 + 4 = 12. P(first red), top: [box=8, NO label] | fix: Split into two lines: first 'Total balls, 8 + 4 = [box=12]', then a separate 'How many red? [box=8]' so the box answer is the last number in its own sentence.
- [medium] silver[6] | Its bottom, 10 × 9 = [box=90, NO label] | fix: Add an intro before the bottom step: 'One ball has been taken and not replaced, so 9 balls are left. Bottom, 10 × 9 ='.
- [medium] bronze[0] | Check the two fractions are equal by cross-multiplying: 1 × 10 = [box=10, NO lab | fix: Ask both cross-products and compare, e.g. 'Top-left × bottom-right, 1 × 10 = [box=10]. Now the other way, 5 × 2 = [box=10]. Same answer, so the fractions match.
- [medium] silver[1] | Q: 5/83/85/83/85/83/8RRRBBRBBBag: 5 red, 3 blue. Two drawn WITH replacement. P(b | fix: Ensure the branch labels render as the diagram, not as text spliced into the prompt; the question should read cleanly 'Bag: 5 red, 3 blue. Two drawn with replac
- [high] silver[0], silver[1], silver[2], silver[5], silver[6], gold[0], gold[1], gold[3], gold[4] (Q stems) | e.g. silver[0]: "1/21/2HT1/21/21/21/2HHHTTHTTA coin is flipped twice. Find P(two | fix: Strip the diagram-label text out of the stem (it belongs in the tree diagram only). Each stem should start with the plain sentence, e.g. "A coin is flipped twic

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: A bag has 5 red and 3 blue balls. Find P(red) as a fraction.
   step0 field=say answer=None text='Probability is favourable outcomes over the total. Start by counting.'
   step1 field=pre answer=5 text='How many red balls?'
   step2 field=pre answer=8 text='Total number of balls: 5 + 3 ='
   step3 field=pre answer=5 text='P(red) numerator (the reds) ='
   step4 field=pre answer=8 text='P(red) denominator (the total) ='
   step5 field=pre answer=5 text='Check: 5 out of 8, and 5/8 is already simplest. Type the numerator once more:'

gold[0] Q: 7/125/12RB6/115/117/114/11RRRBBRBBA bag has 7 red and 5 blue. Two are picked without repla
   step0 field=say answer=None text='One of each can happen two ways: red then blue, or blue then red. Without replacement.'
   step1 field=pre answer=35 text='P(red-blue) top: 7 × 5 ='
   step2 field=pre answer=132 text='P(red-blue) bottom: 12 × 11 ='
   step3 field=say answer=None text='P(blue-red) works out the same, 35/132. Two paths, so add them.'
   step4 field=pre answer=70 text='35 + 35 ='
   step5 field=pre answer=35 text='Simplify 70/132 by 2, top: 70 ÷ 2 ='
   step6 field=pre answer=66 text='Bottom: 132 ÷ 2 ='

gold[2] Q: 0.60.4AA'0.50.50.20.8BB'BB'P(A) = 0.6, P(B given A) = 0.5, P(B given not A) = 0.2. Find P(
   step0 field=say answer=None text='B can be reached two ways: through A, or through not A. Total-probability rule.'
   step1 field=pre answer=0.3 text='Path through A: 0.6 × 0.5 ='
   step2 field=pre answer=0.4 text='P(not A) = 1 − 0.6 ='
   step3 field=pre answer=0.08 text='Path through not A: 0.4 × 0.2 ='
   step4 field=pre answer=19 text='38 ÷ 2 ='
   step5 field=pre answer=50 text='100 ÷ 2 ='

gold[3] Q: A coin is flipped 4 times. Find P(at least one head) as a fraction.
   step0 field=say answer=None text='At least one head is easiest as 1 − P(no heads at all).'
   step1 field=pre answer=16 text='P(no heads) bottom: 2 × 2 × 2 × 2 ='
   step2 field=pre answer=1 text='P(no heads) top: 1 × 1 × 1 × 1 ='
   step3 field=say answer=None text='So P(no heads) = 1/16, and P(at least one) = 16/16 − 1/16.'
   step4 field=pre answer=15 text='16 − 1 ='
   step5 field=pre answer=16 text='Denominator stays ='

gold[4] Q: 2/31/3HT2/31/32/31/3HHHTTHTTA biased coin has P(H) = ⅔. It is flipped twice. Find P(exactl
   step0 field=say answer=None text='Biased coin: P(H) = 2/3, so P(T) = 1/3. Exactly one head is HT or TH.'
   step1 field=pre answer=2 text='P(HT) top: 2 × 1 ='
   step2 field=pre answer=9 text='P(HT) bottom: 3 × 3 ='
   step3 field=say answer=None text='P(TH) is the same, 2/9. Two paths, so add.'
   step4 field=pre answer=4 text='2 + 2 ='
   step5 field=pre answer=9 text='Denominator stays ='

silver[0] Q: 1/21/2HT1/21/21/21/2HHHTTHTTA coin is flipped twice. Find P(two heads) as a fraction.
   step0 field=say answer=None text='Two flips: draw two branches each time. P(H) = 1/2 every flip.'
   step1 field=pre answer=1 text='P(H) on flip 1, numerator ='
   step2 field=pre answer=2 text='P(H) on flip 1, denominator ='
   step3 field=say answer=None text='Two heads needs H then H, so multiply along that branch.'
   step4 field=pre answer=1 text='1 × 1 ='
   step5 field=pre answer=4 text='Multiply the bottoms: 2 × 2 ='

silver[1] Q: 6/104/10RB6/104/106/104/10RRRBBRBBA bag has 6 red and 4 blue. Two are picked with replacem
   step0 field=say answer=None text='With replacement the bag is the same each time. P(blue) = 4/10 both picks.'
   step1 field=pre answer=4 text='P(blue) numerator ='
   step2 field=pre answer=10 text='P(blue) denominator ='
   step3 field=pre answer=16 text='Multiply tops: 4 × 4 ='
   step4 field=pre answer=100 text='10 × 10 ='
   step5 field=pre answer=4 text='16 ÷ 4 ='
   step6 field=pre answer=25 text='100 ÷ 4 ='

silver[6] Q: 3/43/43/4LLL27/64A spinner has P(win) = ¼. It is spun 3 times. Find P(no wins) as a fracti
   step0 field=say answer=None text='No wins in three spins means losing every spin. P(lose) = 1 − 1/4.'
   step1 field=pre answer=3 text='P(lose) numerator (1 − 1/4 = 3/4) ='
   step2 field=pre answer=4 text='P(lose) denominator ='
   step3 field=say answer=None text='Three losses in a row: cube the fraction.'
   step4 field=pre answer=27 text='3 × 3 × 3 ='
   step5 field=pre answer=64 text='Cube the bottom: 4 × 4 × 4 ='

### board=maths-edexcel
bronze[0] Q: 12345A spinner has sections 1-5 (equally likely). Find P(even number). Give as a decimal.
   step0 field=say answer=None text='List the outcomes: 1, 2, 3, 4, 5. The even ones are 2 and 4.'
   step1 field=pre answer=2 text='How many outcomes are even?'
   step2 field=pre answer=5 text='How many outcomes in total?'
   step3 field=pre answer=0.4 text='P(even) as a decimal = 2 ÷ 5 ='
   step4 field=pre answer=0.6 text='Check with the opposite: the three odd numbers give P(odd) = 3 ÷ 5 ='

gold[0] Q: A bag has 8 red and 4 blue. Three drawn without replacement. Find P(all red). Give as a fr
   step0 field=say answer=None text='No replacement, three reds. The draws are 8/12, then 7/11, then 6/10 (each drops by 1).'
   step1 field=pre answer=336 text='Multiply the tops: 8 × 7 × 6 ='
   step2 field=pre answer=1320 text='Multiply the bottoms: 12 × 11 × 10 ='
   step3 field=pre answer=14 text='Simplify 336/1320 by dividing both by 24: the top 336 ÷ 24 ='
   step4 field=pre answer=55 text='and the bottom 1320 ÷ 24 ='
   step5 field=pre answer=336 text='Check the top: 14 × 24 should give back 336, so 14 × 24 ='

gold[2] Q: +112233445566234567345678456789567891067891011789101112Two dice are rolled. Find the proba
   step0 field=say answer=None text='Two dice give 6 × 6 = 36 equally likely ordered outcomes. Count the ones totalling 7.'
   step1 field=pre answer=6 text='List them: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1). How many?'
   step2 field=pre answer=36 text='Total outcomes = 6 × 6 ='
   step3 field=pre answer=1 text='P = 6/36. Simplify by 6: the top 6 ÷ 6 ='
   step4 field=pre answer=6 text='and the bottom 36 ÷ 6 ='
   step5 field=pre answer=36 text='Check: 7 is the most common total, and 1/6 is about 0.167. Confirm 6 × 6 ='

gold[3] Q: A bag has 5 red and \(n\) blue. P(two red without replacement) = \(\frac{2}{9}\). Find \(n
   step0 field=say answer=None text='Two reds without replacement: (5/(5+n)) × (4/(4+n)) = 2/9. The tops give 5 × 4.'
   step1 field=pre answer=20 text='Multiply the tops: 5 × 4 ='
   step2 field=pre answer=90 text='So 20 ÷ ((5+n)(4+n)) = 2/9. Cross-multiply: (5+n)(4+n) = 20 × 9 ÷ 2 ='
   step3 field=pre answer=90 text='Find n so (5+n)(4+n) = 90. Try n = 5: (5+5)(4+5) = 10 × 9 ='
   step4 field=pre answer=5 text='It works, so n ='
   step5 field=pre answer=2 text='Check: with 5 blue, P = (5/10)(4/9) = 20/90. Simplify: 90 ÷ 45 ='

gold[4] Q: A biased coin has P(H) = \(p\). It is tossed twice. P(exactly one head) = 0.48. Find \(p\)
   step0 field=say answer=None text='Exactly one head in two tosses is HT or TH, so P = 2 × p × (1 − p) = 0.48.'
   step1 field=pre answer=0.24 text='Divide both sides by 2: p(1 − p) = 0.48 ÷ 2 ='
   step2 field=pre answer=0.04 text='So p² − p + 0.24 = 0. The discriminant is 1 − 4(0.24) = 1 − 0.96 ='
   step3 field=pre answer=0.2 text='√0.04 ='
   step4 field=pre answer=0.4 text='Smaller root: p = (1 − 0.2) ÷ 2 ='
   step5 field=pre answer=0.48 text='Check: with p = 0.4, 2 × 0.4 × 0.6 ='

silver[0] Q: 3/107/10RB3/107/103/107/10RRRBBRBBA bag has 3 red, 7 blue. Two drawn WITH replacement. Fin
   step0 field=say answer=None text='With replacement the ball goes back, so each draw is identical. P(red) = 3/10 = 0.3.'
   step1 field=pre answer=0.3 text='P(red) on one draw, as a decimal ='
   step2 field=pre answer=0.09 text='Second draw is the same, 0.3. Multiply: 0.3 × 0.3 ='
   step3 field=pre answer=0.09 text='Check with fractions: 3/10 × 3/10 = 9/100 ='

silver[1] Q: P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A and B). Give as a decimal.
   step0 field=say answer=None text="Independent 'A and B' means both happen, so multiply the two probabilities."
   step1 field=pre answer=0.4 text='Write P(A) ='
   step2 field=pre answer=0.2 text='P(A and B) = 0.4 × 0.5 ='
   step3 field=pre answer=20 text='Check via 4 × 5 = 20, then two decimal places gives 0.2. Type 4 × 5 ='

silver[6] Q: A 0.5B 0.3C 0.2A spinner has P(A) = 0.5, P(B) = 0.3, P(C) = 0.2. Spun twice. Find P(same r
   step0 field=say answer=None text="'Same both times' means AA or BB or CC. Each is a multiply, then add the three paths."
   step1 field=pre answer=0.25 text='P(AA) = 0.5 × 0.5 ='
   step2 field=pre answer=0.09 text='P(BB) = 0.3 × 0.3 ='
   step3 field=pre answer=0.04 text='P(CC) = 0.2 × 0.2 ='
   step4 field=pre answer=0.38 text='Add the three: 0.25 + 0.09 + 0.04 ='
   step5 field=pre answer=1 text='Check the spinner is complete: 0.5 + 0.3 + 0.2 ='

### board=maths-ocr
bronze[0] Q: Bag: 2 red, 8 blue. Find P(red). Give as a simplified fraction.
   step0 field=pre answer=2 text='Red balls (favourable):'
   step1 field=pre answer=10 text='Total balls, 2 + 8 ='
   step2 field=pre answer=1 text='So P(red) = 2/10. Divide top and bottom by 2. Top, 2 ÷ 2 ='
   step3 field=pre answer=5 text='Bottom, 10 ÷ 2 ='
   step4 field=pre answer=10 text='1 × 10 ='

gold[0] Q: 4/124/114/108/127/116/10RRBBBRBag: 8 red, 4 blue. Three drawn without replacement. P(all r
   step0 field=pre answer=8 text='Total balls = 8 + 4 = 12. P(first red), top:'
   step1 field=pre answer=7 text='P(second red), top (red now left):'
   step2 field=pre answer=6 text='P(third red), top (red now left):'
   step3 field=pre answer=336 text='Multiply all three tops: 8 × 7 × 6 ='
   step4 field=pre answer=1320 text='Multiply the bottoms: 12 × 11 × 10 ='
   step5 field=pre answer=14 text='Simplify 336/1320 by dividing by 24. Top, 336 ÷ 24 ='
   step6 field=pre answer=55 text='Bottom, 1320 ÷ 24 ='

gold[2] Q: Three coins flipped. P(all heads).
   step0 field=pre answer=3 text='How many tosses are there?'
   step1 field=pre answer=1 text='Multiply the tops: 1 × 1 × 1 ='
   step2 field=pre answer=8 text='Multiply the bottoms: 2 × 2 × 2 ='
   step3 field=pre answer=1 text='There are 8 equally likely outcomes and only HHH works. Favourable outcomes:'

gold[3] Q: Three coins flipped. P(exactly 2 heads).
   step0 field=pre answer=8 text='Total outcomes of three coins, 2 × 2 × 2 ='
   step1 field=pre answer=3 text='How many have exactly two heads (HHT, HTH, THH)?'
   step2 field=pre answer=3 text='So P = 3/8, and 3 and 8 share no factor. Numerator (favourable):'
   step3 field=pre answer=8 text='Check all outcomes: 1 (HHH) + 3 (two H) + 3 (one H) + 1 (no H) ='

gold[4] Q: 7/125/126/115/117/114/11RRRBBRBBBag: 7 red, 5 blue. Two without replacement. P(both blue).
   step0 field=pre answer=5 text='Total balls = 7 + 5 = 12. P(first blue), top:'
   step1 field=pre answer=4 text='P(second blue), top (blue now left):'
   step2 field=pre answer=20 text='Multiply the branches: (5/12) × (4/11). New top, 5 × 4 ='
   step3 field=pre answer=132 text='New bottom, 12 × 11 ='
   step4 field=pre answer=5 text='Simplify 20/132 by dividing by 4. Top, 20 ÷ 4 ='
   step5 field=pre answer=33 text='Bottom, 132 ÷ 4 ='

silver[0] Q: A coin is flipped twice. P(exactly one head).
   step0 field=pre answer=4 text='How many outcomes are there in total?'
   step1 field=pre answer=2 text='How many have exactly one head (HT and TH)?'
   step2 field=pre answer=1 text='So P = 2/4. Divide top and bottom by 2. Top, 2 ÷ 2 ='
   step3 field=pre answer=2 text='Bottom, 4 ÷ 2 ='
   step4 field=pre answer=4 text='1 × 4 ='

silver[1] Q: 5/83/85/83/85/83/8RRRBBRBBBag: 5 red, 3 blue. Two drawn WITH replacement. P(both red).
   step0 field=pre answer=5 text='P(red) on the first draw, top number:'
   step1 field=pre answer=5 text='P(red) on the second draw is the same, top number:'
   step2 field=pre answer=25 text='Multiply along the branches: (5/8) × (5/8). New top, 5 × 5 ='
   step3 field=pre answer=64 text='New bottom, 8 × 8 ='
   step4 field=pre answer=8 text='Check the first-draw branches cover the bag: red 5 + blue 3 ='

silver[6] Q: 6/104/105/94/96/93/9RRRBBRBBBag: 6 red, 4 blue. Two without replacement. P(one of each col
   step0 field=pre answer=24 text='Red then blue: top is 6 × 4 ='
   step1 field=pre answer=90 text='Its bottom, 10 × 9 ='
   step2 field=pre answer=24 text='Blue then red gives (4/10) × (6/9), the same 24/90. Its top, 4 × 6 ='
   step3 field=pre answer=48 text='Add the two paths: 24/90 + 24/90. Top, 24 + 24 ='
   step4 field=pre answer=8 text='Simplify 48/90 by dividing by 6. Top, 48 ÷ 6 ='
   step5 field=pre answer=15 text='Bottom, 90 ÷ 6 ='

### board=maths-eduqas
bronze[0] Q: A bag has 3 red and 5 blue balls. Find P(red) as a simplified fraction.
   step0 field=say answer=None text='Probability is favourable outcomes over the total. Start by counting.'
   step1 field=pre answer=3 text='How many red balls?'
   step2 field=pre answer=8 text='Total balls: 3 + 5 ='
   step3 field=pre answer=3 text='P(red) numerator (the reds) ='
   step4 field=pre answer=8 text='P(red) denominator (the total) ='

gold[0] Q: 6/104/10RB5/94/96/93/9RRRBBRBBA bag has 6 red and 4 blue. Two picked without replacement. 
   step0 field=say answer=None text='One of each can happen two ways: red then blue, or blue then red. Without replacement.'
   step1 field=pre answer=24 text='P(red-blue) top: 6 × 4 ='
   step2 field=pre answer=90 text='P(red-blue) bottom: 10 × 9 ='
   step3 field=pre answer=48 text='24 + 24 ='
   step4 field=pre answer=8 text='Simplify 48/90 by 6, top: 48 ÷ 6 ='
   step5 field=pre answer=15 text='Bottom: 90 ÷ 6 ='

gold[2] Q: A coin is flipped 4 times. Find P(at least one head) as a simplified fraction.
   step0 field=say answer=None text='At least one head is easiest as 1 − P(no heads at all).'
   step1 field=pre answer=16 text='P(no heads) bottom: 2 × 2 × 2 × 2 ='
   step2 field=pre answer=1 text='P(no heads) top: 1 × 1 × 1 × 1 ='
   step3 field=pre answer=15 text='16 − 1 ='
   step4 field=pre answer=16 text='Denominator stays ='

gold[3] Q: 0.60.4AA'0.50.50.250.75BB'BB'P(A) = 0.6, P(B given A) = 0.5, P(B given not A) = 0.25. Find
   step0 field=say answer=None text='B can be reached two ways: through A, or through not A. Total-probability rule.'
   step1 field=pre answer=0.3 text='Path through A: 0.6 × 0.5 ='
   step2 field=pre answer=0.4 text='P(not A) = 1 − 0.6 ='
   step3 field=pre answer=0.1 text='Path through not A: 0.4 × 0.25 ='
   step4 field=pre answer=2 text='4 ÷ 2 ='
   step5 field=pre answer=5 text='10 ÷ 2 ='

gold[4] Q: 2/31/3HT2/31/32/31/3HHHTTHTTA biased coin has P(H) = 2/3. It is flipped twice. Find P(exac
   step0 field=say answer=None text='Biased coin: P(H) = 2/3, so P(T) = 1/3. Exactly one head is HT or TH.'
   step1 field=pre answer=2 text='P(HT) top: 2 × 1 ='
   step2 field=pre answer=9 text='P(HT) bottom: 3 × 3 ='
   step3 field=pre answer=4 text='2 + 2 ='
   step4 field=pre answer=9 text='Denominator stays ='

silver[0] Q: 1/21/2HT1/21/21/21/2HHHTTHTTA coin is flipped twice. Find P(two heads) as a simplified fra
   step0 field=say answer=None text='Two flips: draw two branches each time. P(H) = 1/2 every flip.'
   step1 field=pre answer=1 text='P(H) on flip 1, numerator ='
   step2 field=pre answer=2 text='P(H) denominator ='
   step3 field=pre answer=1 text='Two heads needs H then H. Multiply tops: 1 × 1 ='
   step4 field=pre answer=4 text='Multiply bottoms: 2 × 2 ='

silver[1] Q: 6/104/10RB6/104/106/104/10RRRBBRBBA bag has 6 red and 4 blue. Two are picked with replacem
   step0 field=say answer=None text='With replacement the bag is the same each time. P(blue) = 4/10 both picks.'
   step1 field=pre answer=4 text='P(blue) numerator ='
   step2 field=pre answer=10 text='P(blue) denominator ='
   step3 field=pre answer=16 text='Multiply tops: 4 × 4 ='
   step4 field=pre answer=100 text='Multiply bottoms: 10 × 10 ='
   step5 field=pre answer=4 text='16 ÷ 4 ='
   step6 field=pre answer=25 text='100 ÷ 4 ='

silver[6] Q: 8/102/10RB7/92/98/91/9RRRBBRBBA bag has 8 red and 2 blue. Two picked without replacement. 
   step0 field=say answer=None text='One of each can happen two ways: red then blue, or blue then red. Without replacement.'
   step1 field=pre answer=16 text='P(red-blue) top: 8 × 2 ='
   step2 field=pre answer=90 text='P(red-blue) bottom: 10 × 9 ='
   step3 field=pre answer=32 text='16 + 16 ='
   step4 field=pre answer=16 text='Simplify 32/90 by 2, top: 32 ÷ 2 ='
   step5 field=pre answer=45 text='Bottom: 90 ÷ 2 ='
