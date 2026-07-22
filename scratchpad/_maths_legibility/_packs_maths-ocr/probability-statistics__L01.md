# maths-ocr / probability-statistics / L01 - Probability Basics & Tree Diagrams

## bronze[0] (input: fraction, main-box unit: (none))
Q: Bag: 2 red, 8 blue. Find P(red). Give as a simplified fraction.
   - intro: Probability is what you want ÷ everything there is. Count the red first.
   - ask: Red balls (favourable):  [box=2, NO label]
   - ask: Total balls, 2 + 8 =  [box=10, NO label]
   - intro: Now simplify.
   - ask: So P(red) = 2/10. Divide top and bottom by 2. Top, 2 ÷ 2 =  [box=1, NO label]
   - ask: Bottom, 10 ÷ 2 =  [box=5, NO label]
   - intro: Check the two fractions are equal by cross-multiplying:
   - ask: 1 × 10 =  [box=10, NO label]

## bronze[1] (input: fraction, main-box unit: (none))
Q: A fair die is rolled. P(even number).
   - intro: List the even faces on a fair die.
   - ask: How many faces are even (2, 4, 6)?  [box=3, NO label]
   - ask: How many faces in total?  [box=6, NO label]
   - intro: Now simplify.
   - ask: So P(even) = 3/6. Divide top and bottom by 3. Top, 3 ÷ 3 =  [box=1, NO label]
   - ask: Bottom, 6 ÷ 3 =  [box=2, NO label]
   - intro: Check the two fractions are equal by cross-multiplying:
   - ask: 1 × 6 =  [box=6, NO label]

## bronze[2] (input: fraction, main-box unit: (none))
Q: A card is picked from a standard deck. P(heart).
   - intro: A standard deck has four suits of 13 cards each.
   - ask: How many hearts are in the deck?  [box=13, NO label]
   - ask: How many cards in total?  [box=52, NO label]
   - intro: Now simplify.
   - ask: So P(heart) = 13/52. Divide top and bottom by 13. Top, 13 ÷ 13 =  [box=1, NO label]
   - ask: Bottom, 52 ÷ 13 =  [box=4, NO label]
   - intro: Check the two fractions are equal by cross-multiplying:
   - ask: 1 × 52 =  [box=52, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: P(not rain) if P(rain) = 0.3. Give as a decimal.
   - intro: Rain or no rain covers everything, so the two add up to 1.
   - ask: P(rain) =  [box=0.3, NO label]
   - ask: P(no rain) is what is left to reach 1. 1 − 0.3 =  [box=0.7, NO label]
   - intro: Check:
   - ask: Check the two total 1: 0.3 + 0.7 =  [box=1, NO label]

## bronze[4] (input: fraction, main-box unit: (none))
Q: Bag: 5 red, 3 blue. Find P(blue). Give as a fraction.
   - intro: Count the blue balls, then the total.
   - ask: Blue balls (favourable):  [box=3, NO label]
   - ask: Total balls, 5 + 3 =  [box=8, NO label]
   - intro: 3 and 8 share no common factor, so 3/8 is already simplest.
   - ask: P(blue) = 3/8. The red balls are the rest. Red balls:  [box=5, NO label]
   - ask: Check both colours cover everything: blue top 3 + red 5 =  [box=8, NO label]

## bronze[5] (input: fraction, main-box unit: (none))
Q: A fair spinner has sections 1-5. P(3 or higher).
   - intro: '3 or higher' includes the 3 itself.
   - ask: How many sections are 3, 4 or 5?  [box=3, NO label]
   - ask: How many sections in total?  [box=5, NO label]
   - intro: 3 and 5 share no factor, so 3/5 is already simplest.
   - ask: So P(3 or higher) = 3/5. Sections below 3 are 1 and 2. How many is that?  [box=2, NO label]
   - ask: Check: favourable 3 + below-3 count =  [box=5, NO label]

## bronze[6] (input: fraction, main-box unit: (none))
Q: Bag: 4 red, 4 blue, 2 green. P(not green).
   - intro: 'Not green' means everything except green. Find the total first.
   - ask: Total balls, 4 + 4 + 2 =  [box=10, NO label]
   - ask: Green balls:  [box=2, NO label]
   - ask: Not green = total − green. 10 − 2 =  [box=8, NO label]
   - ask: So P(not green) = 8/10. Divide top and bottom by 2. Top, 8 ÷ 2 =  [box=4, NO label]
   - ask: Bottom, 10 ÷ 2 =  [box=5, NO label]

## bronze[7] (input: fraction, main-box unit: (none))
Q: A die is rolled. P(less than 3).
   - intro: 'Less than 3' means below 3, so 3 is not included.
   - ask: How many faces are less than 3 (just 1 and 2)?  [box=2, NO label]
   - ask: How many faces in total?  [box=6, NO label]
   - intro: Now simplify.
   - ask: So P(less than 3) = 2/6. Divide top and bottom by 2. Top, 2 ÷ 2 =  [box=1, NO label]
   - ask: Bottom, 6 ÷ 2 =  [box=3, NO label]
   - intro: Check the two fractions are equal by cross-multiplying:
   - ask: 1 × 6 =  [box=6, NO label]

## silver[0] (input: fraction, main-box unit: (none))
Q: A coin is flipped twice. P(exactly one head).
   - intro: Two tosses give four equally likely outcomes: HH, HT, TH, TT.
   - ask: How many outcomes are there in total?  [box=4, NO label]
   - intro: 'Exactly one head' means one H and one T, in either order.
   - ask: How many have exactly one head (HT and TH)?  [box=2, NO label]
   - intro: Now simplify.
   - ask: So P = 2/4. Divide top and bottom by 2. Top, 2 ÷ 2 =  [box=1, NO label]
   - ask: Bottom, 4 ÷ 2 =  [box=2, NO label]
   - intro: Check the two fractions are equal by cross-multiplying:
   - ask: 1 × 4 =  [box=4, NO label]

## silver[1] (input: fraction, main-box unit: (none))
Q: 5/83/85/83/85/83/8RRRBBRBBBag: 5 red, 3 blue. Two drawn WITH replacement. P(both red).
   - intro: With replacement the ball goes back, so both draws face the same 8 balls.
   - ask: P(red) on the first draw, top number:  [box=5, NO label]
   - ask: P(red) on the second draw is the same, top number:  [box=5, NO label]
   - intro: Tops multiply, bottoms multiply.
   - ask: Multiply along the branches: (5/8) × (5/8). New top, 5 × 5 =  [box=25, NO label]
   - ask: New bottom, 8 × 8 =  [box=64, NO label]
   - intro: Check:
   - ask: Check the first-draw branches cover the bag: red 5 + blue 3 =  [box=8, NO label]

## silver[2] (input: fraction, main-box unit: (none))
Q: 5/83/84/73/75/72/7RRRBBRBBBag: 5 red, 3 blue. Two drawn WITHOUT replacement. P(both red).
   - intro: First draw: 5 red out of 8.
   - ask: P(first red), top number:  [box=5, NO label]
   - intro: One red is gone and kept out, so 4 red remain and 7 balls in total.
   - ask: P(second red), top number (red now left):  [box=4, NO label]
   - ask: Multiply the branches: (5/8) × (4/7). New top, 5 × 4 =  [box=20, NO label]
   - ask: New bottom, 8 × 7 =  [box=56, NO label]
   - intro: Now simplify.
   - ask: Simplify 20/56 by dividing by 4. Top, 20 ÷ 4 =  [box=5, NO label]
   - ask: Bottom, 56 ÷ 4 =  [box=14, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: P(A) = 0.4, P(B) = 0.3. A and B are independent. P(A and B)?
   - intro: Independent events do not affect each other, so 'A and B' multiplies.
   - ask: P(A) =  [box=0.4, NO label]
   - ask: P(B) =  [box=0.3, NO label]
   - ask: Multiply them. 0.4 × 0.3 =  [box=0.12, NO label]
   - intro: Check:
   - ask: Check the other way (it must match): 0.3 × 0.4 =  [box=0.12, NO label]

## silver[4] (input: fraction, main-box unit: (none))
Q: 112233445566Die 2Die 1A die is rolled twice. P(total = 7).
   - intro: Two dice give 6 × 6 outcomes. The grid shows them all.
   - ask: Total number of outcomes, 6 × 6 =  [box=36, NO label]
   - intro: Now count the pairs that add to 7.
   - ask: How many pairs total 7 (the highlighted diagonal)?  [box=6, NO label]
   - intro: Now simplify.
   - ask: So P = 6/36. Divide top and bottom by 6. Top, 6 ÷ 6 =  [box=1, NO label]
   - ask: Bottom, 36 ÷ 6 =  [box=6, NO label]
   - intro: Check the two fractions are equal by cross-multiplying:
   - ask: 1 × 36 =  [box=36, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: P(A) = 0.6. P(not A)?
   - intro: An event and its opposite always add to 1.
   - ask: P(A) =  [box=0.6, NO label]
   - ask: P(not A) is what is left to reach 1. 1 − 0.6 =  [box=0.4, NO label]
   - intro: Check:
   - ask: Check they total 1: 0.6 + 0.4 =  [box=1, NO label]

## silver[6] (input: fraction, main-box unit: (none))
Q: 6/104/105/94/96/93/9RRRBBRBBBag: 6 red, 4 blue. Two without replacement. P(one of each colour).
   - intro: 'One of each' has two paths: red then blue, or blue then red. Total balls = 10.
   - ask: Red then blue: top is 6 × 4 =  [box=24, NO label]
   - ask: Its bottom, 10 × 9 =  [box=90, NO label]
   - ask: Blue then red gives (4/10) × (6/9), the same 24/90. Its top, 4 × 6 =  [box=24, NO label]
   - intro: Now add both orders.
   - ask: Add the two paths: 24/90 + 24/90. Top, 24 + 24 =  [box=48, NO label]
   - ask: Simplify 48/90 by dividing by 6. Top, 48 ÷ 6 =  [box=8, NO label]
   - ask: Bottom, 90 ÷ 6 =  [box=15, NO label]

## gold[0] (input: fraction, main-box unit: (none))
Q: 4/124/114/108/127/116/10RRBBBRBag: 8 red, 4 blue. Three drawn without replacement. P(all red).
   - intro: First draw: 8 red out of 12.
   - ask: Total balls = 8 + 4 = 12. P(first red), top:  [box=8, NO label]
   - intro: One red gone: 7 red left, 11 balls.
   - ask: P(second red), top (red now left):  [box=7, NO label]
   - intro: Another red gone: 6 red left, 10 balls.
   - ask: P(third red), top (red now left):  [box=6, NO label]
   - intro: Multiply the three tops and the three bottoms.
   - ask: Multiply all three tops: 8 × 7 × 6 =  [box=336, NO label]
   - ask: Multiply the bottoms: 12 × 11 × 10 =  [box=1320, NO label]
   - ask: Simplify 336/1320 by dividing by 24. Top, 336 ÷ 24 =  [box=14, NO label]
   - ask: Bottom, 1320 ÷ 24 =  [box=55, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: P(rain Mon) = 0.3, P(rain Tue) = 0.4 (independent). P(rain at least one day). Give as a decimal.
   - intro: 'At least one' is the opposite of 'none'. Find P(no rain) each day first.
   - ask: P(no rain Mon), 1 − 0.3 =  [box=0.7, NO label]
   - ask: P(no rain Tue), 1 − 0.4 =  [box=0.6, NO label]
   - ask: P(no rain either day) = 0.7 × 0.6 =  [box=0.42, NO label]
   - ask: 'At least one' is everything else. 1 − 0.42 =  [box=0.58, NO label]
   - intro: Check:
   - ask: Check the two opposites total 1: 0.58 + 0.42 =  [box=1, NO label]

## gold[2] (input: fraction, main-box unit: (none))
Q: Three coins flipped. P(all heads).
   - intro: Each toss is independent with P(head) = 1/2. Three heads multiply.
   - ask: How many tosses are there?  [box=3, NO label]
   - ask: Multiply the tops: 1 × 1 × 1 =  [box=1, NO label]
   - intro: The denominator is the total number of outcomes.
   - ask: Multiply the bottoms: 2 × 2 × 2 =  [box=8, NO label]
   - ask: There are 8 equally likely outcomes and only HHH works. Favourable outcomes:  [box=1, NO label]

## gold[3] (input: fraction, main-box unit: (none))
Q: Three coins flipped. P(exactly 2 heads).
   - intro: Three coins give 8 equally likely outcomes.
   - ask: Total outcomes of three coins, 2 × 2 × 2 =  [box=8, NO label]
   - intro: List those with exactly two heads.
   - ask: How many have exactly two heads (HHT, HTH, THH)?  [box=3, NO label]
   - intro: Already in lowest terms.
   - ask: So P = 3/8, and 3 and 8 share no factor. Numerator (favourable):  [box=3, NO label]
   - ask: Check all outcomes: 1 (HHH) + 3 (two H) + 3 (one H) + 1 (no H) =  [box=8, NO label]

## gold[4] (input: fraction, main-box unit: (none))
Q: 7/125/126/115/117/114/11RRRBBRBBBag: 7 red, 5 blue. Two without replacement. P(both blue).
   - intro: First draw: 5 blue out of 12.
   - ask: Total balls = 7 + 5 = 12. P(first blue), top:  [box=5, NO label]
   - intro: One blue gone and kept out: 4 blue left, 11 balls.
   - ask: P(second blue), top (blue now left):  [box=4, NO label]
   - ask: Multiply the branches: (5/12) × (4/11). New top, 5 × 4 =  [box=20, NO label]
   - ask: New bottom, 12 × 11 =  [box=132, NO label]
   - intro: Now simplify.
   - ask: Simplify 20/132 by dividing by 4. Top, 20 ÷ 4 =  [box=5, NO label]
   - ask: Bottom, 132 ÷ 4 =  [box=33, NO label]
