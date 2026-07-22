# maths-edexcel / probability-statistics / L01 - Probability Basics & Tree Diagrams

## bronze[0] (input: single_value, main-box unit: (none))
Q: 12345A spinner has sections 1-5 (equally likely). Find P(even number). Give as a decimal.
   - intro: List the outcomes: 1, 2, 3, 4, 5. The even ones are 2 and 4.
   - ask: How many outcomes are even?  [box=2, NO label]
   - ask: How many outcomes in total?  [box=5, NO label]
   - ask: P(even) as a decimal = 2 ÷ 5 =  [box=0.4, NO label]
   - ask: Check with the opposite: the three odd numbers give P(odd) = 3 ÷ 5 =  [box=0.6, label:'(a decimal)']

## bronze[1] (input: single_value, main-box unit: (none))
Q: P(rain) = 0.3. Find P(no rain).
   - intro: Rain and no rain are opposites, and opposites always add up to 1.
   - ask: Write down P(rain) =  [box=0.3, NO label]
   - ask: P(no rain) = 1 − 0.3 =  [box=0.7, NO label]
   - ask: Check the two add to 1: 0.7 + 0.3 =  [box=1, NO label]

## bronze[2] (input: fraction, main-box unit: (none))
Q: A bag has 2 red and 8 blue. Find P(red). Give as a simplified fraction (e.g. 1/5).
   - intro: P(red) is the number of red balls over the total number of balls.
   - ask: Total balls = 2 + 8 =  [box=10, NO label]
   - ask: Red balls (the top of the fraction) =  [box=2, NO label]
   - ask: So P(red) = 2/10. Simplify by 2: the top 2 ÷ 2 =  [box=1, NO label]
   - ask: and the bottom 10 ÷ 2 =  [box=5, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: A coin is tossed twice. Find P(both heads). Give as a decimal.
   - intro: Two tosses. P(heads) each time is a half, 0.5. 'Both' means AND, so multiply.
   - ask: P(heads) on one toss, as a decimal =  [box=0.5, NO label]
   - ask: Second toss is also 0.5. Multiply: 0.5 × 0.5 =  [box=0.25, NO label]
   - ask: Check by listing HH, HT, TH, TT: only HH is both heads, so 1 ÷ 4 =  [box=0.25, label:'(a decimal)']

## bronze[4] (input: fraction, main-box unit: (none))
Q: A dice is rolled. Find P(not 6). Give as a fraction.
   - intro: 'Not 6' is the opposite of rolling a 6, and opposites subtract from 1.
   - ask: A dice has 6 faces. How many are NOT a 6?  [box=5, NO label]
   - ask: So the top of the fraction is  [box=5, NO label]
   - ask: and the bottom (total faces) is  [box=6, NO label]
   - ask: Check: P(6) + P(not 6) as sixths is 1 + 5 =  [box=6, NO label]

## bronze[5] (input: fraction, main-box unit: (none))
Q: Two coins are tossed. Find P(at least one head). Give as a fraction.
   - intro: List all outcomes of two coins: HH, HT, TH, TT. That is the sample space.
   - ask: How many outcomes are there in total?  [box=4, NO label]
   - ask: How many have at least one head? (all except TT)  [box=3, NO label]
   - ask: So the bottom of the fraction is  [box=4, NO label]
   - ask: Check: only TT has no head, and that is 1 outcome, so 4 − 1 =  [box=3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: A bag has 5 red, 3 blue, 2 green. Find P(blue). Give as a decimal.
   - intro: P(blue) is the blue balls over ALL the balls, greens included.
   - ask: Total = 5 + 3 + 2 =  [box=10, NO label]
   - ask: Blue balls =  [box=3, NO label]
   - ask: P(blue) = 3 ÷ 10 =  [box=0.3, label:'(a decimal)']
   - ask: Check all three add to 1: 0.5 + 0.3 + 0.2 =  [box=1, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: A 0.45B 0.35C ?A spinner lands on A with probability 0.45 and B with probability 0.35. Find P(C) if there are only three sections.
   - intro: The three sections fill the whole spinner, so their probabilities add to 1.
   - ask: Add the two you know: 0.45 + 0.35 =  [box=0.8, NO label]
   - ask: P(C) = 1 − 0.8 =  [box=0.2, NO label]
   - ask: Check: 0.45 + 0.35 + 0.2 =  [box=1, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: 3/107/10RB3/107/103/107/10RRRBBRBBA bag has 3 red, 7 blue. Two drawn WITH replacement. Find P(both red). Give as a decimal.
   - intro: With replacement the ball goes back, so each draw is identical. P(red) = 3/10 = 0.3.
   - ask: P(red) on one draw, as a decimal =  [box=0.3, NO label]
   - ask: Second draw is the same, 0.3. Multiply: 0.3 × 0.3 =  [box=0.09, NO label]
   - ask: Check with fractions: 3/10 × 3/10 = 9/100 =  [box=0.09, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A and B). Give as a decimal.
   - intro: Independent 'A and B' means both happen, so multiply the two probabilities.
   - ask: Write P(A) =  [box=0.4, NO label]
   - ask: P(A and B) = 0.4 × 0.5 =  [box=0.2, NO label]
   - ask: Check via 4 × 5 = 20, then two decimal places gives 0.2. Type 4 × 5 =  [box=20, NO label]

## silver[2] (input: fraction, main-box unit: (none))
Q: 5/83/8RB????RRRBBRBBA bag has 5 red and 3 blue. Two drawn WITHOUT replacement. Find P(both red). Give as a fraction.
   - intro: Without replacement: after one red leaves, both the reds and the total drop by 1. Draws: 5/8 then 4/7.
   - ask: After taking one red, reds left =  [box=4, NO label]
   - ask: Total balls left =  [box=7, NO label]
   - ask: Multiply the tops: 5 × 4 =  [box=20, NO label]
   - ask: Multiply the bottoms: 8 × 7 =  [box=56, NO label]
   - ask: Simplify 20/56 by 4: the top 20 ÷ 4 =  [box=5, NO label]
   - ask: and the bottom 56 ÷ 4 =  [box=14, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: A biased coin has P(H) = 0.6. It is tossed 3 times. Find P(all heads). Give to 3 d.p.
   - intro: Three identical tosses, all heads means AND, AND: multiply 0.6 three times.
   - ask: First multiply two of them: 0.6 × 0.6 =  [box=0.36, NO label]
   - ask: Now the third toss: 0.36 × 0.6 =  [box=0.216, NO label]
   - ask: Check with whole numbers: 6 × 6 × 6 =  [box=216, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: P(rain Mon) = 0.4, P(rain Tue) = 0.3 (independent). Find P(rain on both days).
   - intro: 'Both days' is AND, and the days are independent, so multiply.
   - ask: Write P(rain Monday) =  [box=0.4, NO label]
   - ask: P(both) = 0.4 × 0.3 =  [box=0.12, NO label]
   - ask: Check via 4 × 3 = 12, then two decimal places gives 0.12. Type 4 × 3 =  [box=12, NO label]

## silver[5] (input: fraction, main-box unit: (none))
Q: 6/104/10RB????RRRBBRBBA bag has 6 red, 4 blue. Two drawn without replacement. Find P(at least one red). Give as a fraction.
   - intro: 'At least one red' is easier as 1 minus its opposite, P(both blue). Blue draws: 4/10 then 3/9.
   - ask: After one blue leaves, blues left =  [box=3, NO label]
   - ask: Total balls left =  [box=9, NO label]
   - ask: P(both blue) = (4/10)(3/9) = 12/90. Simplify by 6: top 12 ÷ 6 =  [box=2, NO label]
   - ask: and bottom 90 ÷ 6 =  [box=15, NO label]
   - ask: P(at least one red) = 1 − 2/15. As fifteenths the top is 15 − 2 =  [box=13, NO label]
   - ask: and the bottom stays  [box=15, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: A 0.5B 0.3C 0.2A spinner has P(A) = 0.5, P(B) = 0.3, P(C) = 0.2. Spun twice. Find P(same result both times). Give to 2 d.p.
   - intro: 'Same both times' means AA or BB or CC. Each is a multiply, then add the three paths.
   - ask: P(AA) = 0.5 × 0.5 =  [box=0.25, NO label]
   - ask: P(BB) = 0.3 × 0.3 =  [box=0.09, NO label]
   - ask: P(CC) = 0.2 × 0.2 =  [box=0.04, NO label]
   - ask: Add the three: 0.25 + 0.09 + 0.04 =  [box=0.38, NO label]
   - ask: Check the spinner is complete: 0.5 + 0.3 + 0.2 =  [box=1, NO label]

## gold[0] (input: fraction, main-box unit: (none))
Q: A bag has 8 red and 4 blue. Three drawn without replacement. Find P(all red). Give as a fraction.
   - intro: No replacement, three reds. The draws are 8/12, then 7/11, then 6/10 (each drops by 1).
   - ask: Multiply the tops: 8 × 7 × 6 =  [box=336, NO label]
   - ask: Multiply the bottoms: 12 × 11 × 10 =  [box=1320, NO label]
   - ask: Simplify 336/1320 by dividing both by 24: the top 336 ÷ 24 =  [box=14, NO label]
   - ask: and the bottom 1320 ÷ 24 =  [box=55, NO label]
   - ask: Check the top: 14 × 24 should give back 336, so 14 × 24 =  [box=336, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The probability of passing a driving test is 0.7. Find the probability of passing on exactly the 3rd attempt (failed first two).
   - intro: Exactly the 3rd attempt means fail, fail, then pass. P(fail) = 1 − 0.7.
   - ask: P(fail) = 1 − 0.7 =  [box=0.3, NO label]
   - ask: Multiply the three in order: 0.3 × 0.3 × 0.7 =  [box=0.063, NO label]
   - ask: Check with whole numbers: 3 × 3 × 7 =  [box=63, NO label]

## gold[2] (input: fraction, main-box unit: (none))
Q: +112233445566234567345678456789567891067891011789101112Two dice are rolled. Find the probability the total is 7. Give as a fraction.
   - intro: Two dice give 6 × 6 = 36 equally likely ordered outcomes. Count the ones totalling 7.
   - ask: List them: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1). How many?  [box=6, NO label]
   - ask: Total outcomes = 6 × 6 =  [box=36, NO label]
   - ask: P = 6/36. Simplify by 6: the top 6 ÷ 6 =  [box=1, NO label]
   - ask: and the bottom 36 ÷ 6 =  [box=6, NO label]
   - ask: Check: 7 is the most common total, and 1/6 is about 0.167. Confirm 6 × 6 =  [box=36, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: A bag has 5 red and \(n\) blue. P(two red without replacement) = \(\frac{2}{9}\). Find \(n\).
   - intro: Two reds without replacement: (5/(5+n)) × (4/(4+n)) = 2/9. The tops give 5 × 4.
   - ask: Multiply the tops: 5 × 4 =  [box=20, NO label]
   - ask: So 20 ÷ ((5+n)(4+n)) = 2/9. Cross-multiply: (5+n)(4+n) = 20 × 9 ÷ 2 =  [box=90, NO label]
   - ask: Find n so (5+n)(4+n) = 90. Try n = 5: (5+5)(4+5) = 10 × 9 =  [box=90, NO label]
   - ask: It works, so n =  [box=5, NO label]
   - ask: Check: with 5 blue, P = (5/10)(4/9) = 20/90. Simplify: 90 ÷ 45 =  [box=2, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: A biased coin has P(H) = \(p\). It is tossed twice. P(exactly one head) = 0.48. Find \(p\). Give the smaller value.
   - intro: Exactly one head in two tosses is HT or TH, so P = 2 × p × (1 − p) = 0.48.
   - ask: Divide both sides by 2: p(1 − p) = 0.48 ÷ 2 =  [box=0.24, label:'(a decimal)']
   - ask: So p² − p + 0.24 = 0. The discriminant is 1 − 4(0.24) = 1 − 0.96 =  [box=0.04, NO label]
   - ask: √0.04 =  [box=0.2, NO label]
   - ask: Smaller root: p = (1 − 0.2) ÷ 2 =  [box=0.4, label:'(a decimal)']
   - ask: Check: with p = 0.4, 2 × 0.4 × 0.6 =  [box=0.48, NO label]
