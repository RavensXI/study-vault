# maths-aqa / probability-statistics / L02 - Venn Diagrams & Conditional Probability

## bronze[0] (input: single_value, main-box unit: (none))
Q: MathsScience14810?Total: 4040 students: 22 like maths, 18 like science, 8 like both. How many like neither?
   - intro: Fill the Venn from the middle out: the overlap first, then each single region, then what is left.
   - ask: Both maths and science (the overlap) =  [box=8, NO label]
   - ask: Maths only: 22 − 8 =  [box=14, NO label]
   - ask: Science only: 18 − 8 =  [box=10, NO label]
   - intro: Add the three filled regions.
   - ask: 14 + 8 + 10 =  [box=32, NO label]
   - ask: Neither: 40 − 32 =  [box=8, NO label]

## bronze[1] (input: fraction, main-box unit: (none))
Q: MathsScience148108Total: 40From the same data (40 students, 22 maths, 18 science, 8 both), find P(maths only) as a fraction.
   - intro: Maths only means maths but NOT the overlap. Find that count, then put it over the total.
   - ask: Maths only: 22 − 8 =  [box=14, NO label]
   - ask: Total students =  [box=40, NO label]
   - intro: So P(maths only) = 14/40. Simplify by dividing top and bottom by 2.
   - ask: 14 ÷ 2 =  [box=7, NO label]
   - ask: 40 ÷ 2 =  [box=20, NO label]

## bronze[2] (input: fraction, main-box unit: (none))
Q: CatDog22131510Total: 6060 people: 35 own a cat, 28 own a dog, 13 own both. Find P(cat or dog) as a fraction.
   - intro: Cat or dog means in either circle. Add the totals, then subtract the overlap once so it is not double counted.
   - ask: Cats plus dogs: 35 + 28 =  [box=63, NO label]
   - ask: Subtract the overlap once: 63 − 13 =  [box=50, NO label]
   - ask: Total people =  [box=60, NO label]
   - intro: So P(cat or dog) = 50/60. Simplify by dividing by 10.
   - ask: 50 ÷ 10 =  [box=5, NO label]
   - ask: 60 ÷ 10 =  [box=6, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: AB1051520Total: ?A Venn diagram has: A only = 10, B only = 15, A ∩ B = 5, neither = 20. What is the total?
   - intro: The total is every region added together, including the neither region outside the circles.
   - ask: Overlap (A and B) =  [box=5, NO label]
   - ask: In the circles: 10 + 5 + 15 =  [box=30, NO label]
   - intro: Now add the neither region to reach the total.
   - ask: 30 + 20 =  [box=50, NO label]
   - ask: Check: 10 + 5 + 15 + 20 =  [box=50, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: P(A) = 0.6, P(A ∩ B) = 0.2. Find P(A only).
   - intro: A only means the part of A that does not overlap B. Subtract the overlap from all of A.
   - ask: All of A, P(A) =  [box=0.6, NO label]
   - ask: The overlap P(A ∩ B) =  [box=0.2, NO label]
   - intro: A only is what is left after removing the overlap.
   - ask: 0.6 − 0.2 =  [box=0.4, NO label]
   - ask: Check: A only plus overlap gives all of A. 0.4 + 0.2 =  [box=0.6, NO label]

## bronze[5] (input: fraction, main-box unit: (none))
Q: EnglishHistory201010?Total: 5050 students: 30 like English, 20 like History, 10 like both. Find P(neither) as a fraction.
   - intro: Find how many like at least one subject, then the rest of the group like neither.
   - ask: English only: 30 − 10 =  [box=20, NO label]
   - ask: History only: 20 − 10 =  [box=10, NO label]
   - ask: At least one: 20 + 10 + 10 =  [box=40, NO label]
   - intro: Neither is the total minus those 40.
   - ask: 50 − 40 =  [box=10, NO label]
   - ask: So P(neither) = 10/50. Simplify by 10, top: 10 ÷ 10 =  [box=1, NO label]
   - ask: 50 ÷ 10 =  [box=5, NO label]

## bronze[6] (input: fraction, main-box unit: (none))
Q: AB205Total: 50A Venn diagram shows 25 students in set A and 5 in A ∩ B out of 50 total. Find P(A) as a fraction.
   - intro: P(A) uses everyone inside circle A: both the overlap and the A-only part.
   - ask: Number in set A =  [box=25, NO label]
   - ask: Total students =  [box=50, NO label]
   - intro: So P(A) = 25/50. Simplify by dividing by 25.
   - ask: 25 ÷ 25 =  [box=1, NO label]
   - ask: 50 ÷ 25 =  [box=2, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: AB?152035Total: 100100 people: P(A) = 0.45, P(B) = 0.35, P(A ∩ B) = 0.15. How many are in A only?
   - intro: Turn each probability into a count out of 100, then take the overlap off A.
   - ask: n(A) = 0.45 × 100 =  [box=45, NO label]
   - ask: n(A ∩ B) = 0.15 × 100 =  [box=15, NO label]
   - intro: A only removes the overlap from A.
   - ask: 45 − 15 =  [box=30, NO label]
   - ask: Check: A only plus overlap = 30 + 15 =  [box=45, NO label]

## silver[0] (input: fraction, main-box unit: (none))
Q: FootballRugby30202010Total: 8080 students: 50 like football, 40 like rugby, 20 like both. Find P(football | rugby) as a fraction.
   - intro: Given rugby, we only look inside the rugby group. P(F|R) = both, over the rugby total.
   - ask: Both football and rugby =  [box=20, NO label]
   - ask: Rugby total (the given group) =  [box=40, NO label]
   - intro: So P(F|R) = 20/40. Simplify by dividing by 20.
   - ask: 20 ÷ 20 =  [box=1, NO label]
   - ask: 40 ÷ 20 =  [box=2, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: P(A) = 0.5, P(B) = 0.4, P(A ∩ B) = 0.2. Find P(A ∪ B).
   - intro: Union is everything in either set. Add the two, then subtract the overlap so it is counted once.
   - ask: P(A) + P(B) = 0.5 + 0.4 =  [box=0.9, NO label]
   - ask: The overlap P(A ∩ B) =  [box=0.2, NO label]
   - intro: Subtract the overlap once.
   - ask: 0.9 − 0.2 =  [box=0.7, NO label]
   - ask: Check: 0.5 + 0.4 − 0.2 =  [box=0.7, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: P(A) = 0.7, P(B) = 0.5, P(A ∪ B) = 0.9. Find P(A ∩ B).
   - intro: Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union.
   - ask: P(A) + P(B) = 0.7 + 0.5 =  [box=1.2, NO label]
   - ask: The union P(A ∪ B) =  [box=0.9, NO label]
   - intro: Subtract the union from that sum.
   - ask: 1.2 − 0.9 =  [box=0.3, NO label]
   - ask: Check: 0.7 + 0.5 − 0.3 = 0.9, the union. Type the overlap again:  [box=0.3, NO label]

## silver[3] (input: fraction, main-box unit: (none))
Q: FootballCricket20151510Total: 6060 students: 35 play football, 30 play cricket, 15 play both. Find P(cricket | football) as a fraction.
   - intro: Given football, look only inside the football group. P(C|F) = both, over the football total.
   - ask: Both cricket and football =  [box=15, NO label]
   - ask: Football total (the given group) =  [box=35, NO label]
   - intro: So P(C|F) = 15/35. Simplify by dividing by 5.
   - ask: 15 ÷ 5 =  [box=3, NO label]
   - ask: 35 ÷ 5 =  [box=7, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: Are events A and B independent if P(A) = 0.3, P(B) = 0.4, P(A ∩ B) = 0.12?

## silver[5] (input: fraction, main-box unit: (none))
Q: P(B) = 0.6, P(A ∩ B) = 0.24. Find P(A | B) as a fraction.
   - intro: Conditional formula: P(A|B) = P(A ∩ B) over P(B).
   - ask: P(A ∩ B) =  [box=0.24, NO label]
   - ask: P(B) =  [box=0.6, NO label]
   - intro: Divide the overlap by P(B).
   - ask: 0.24 ÷ 0.6 =  [box=0.4, label:'(a decimal)']
   - ask: 0.4 = 4/10, simplify by 2, top: 4 ÷ 2 =  [box=2, NO label]
   - ask: 10 ÷ 2 =  [box=5, NO label]

## silver[6] (input: fraction, main-box unit: (none))
Q: GirlArt40705040Total: 200200 students: 110 girls, 120 do art, 70 girls do art. Find P(girl | does art) as a fraction.
   - intro: Given art, look only inside the art group. P(girl|art) = girls who do art, over all who do art.
   - ask: Girls who do art =  [box=70, NO label]
   - ask: Total who do art (the given group) =  [box=120, NO label]
   - intro: So P(girl|art) = 70/120. Simplify by dividing by 10.
   - ask: 70 ÷ 10 =  [box=7, NO label]
   - ask: 120 ÷ 10 =  [box=12, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: P(A) = 0.3, P(B|A) = 0.5. Find P(A ∩ B).
   - intro: Multiply rule: P(A ∩ B) = P(A) × P(B given A).
   - ask: P(A) =  [box=0.3, NO label]
   - ask: P(B given A) =  [box=0.5, NO label]
   - intro: Multiply them together.
   - ask: 0.3 × 0.5 =  [box=0.15, NO label]
   - ask: Check: an overlap is smaller than each part. Type 0.15 again:  [box=0.15, NO label]

## gold[1] (input: fraction, main-box unit: (none))
Q: TeaCoffee50302020Total: 120120 people: 80 like tea, 50 like coffee, 30 like both. A person who likes tea is chosen. Find P(also likes coffee) as a fraction.
   - intro: Given tea, look only inside the tea group. P(coffee|tea) = both, over the tea total.
   - ask: Both tea and coffee =  [box=30, NO label]
   - ask: Tea total (the given group) =  [box=80, NO label]
   - intro: So P(coffee|tea) = 30/80. Simplify by dividing by 10.
   - ask: 30 ÷ 10 =  [box=3, NO label]
   - ask: 80 ÷ 10 =  [box=8, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: P(A|B) = 0.6, P(B) = 0.5. P(A|B') = 0.2, P(B') = 0.5. Find P(A).
   - intro: A can happen through B or through not B. Total probability adds both routes.
   - ask: Route through B: 0.6 × 0.5 =  [box=0.3, NO label]
   - ask: Route through not B: 0.2 × 0.5 =  [box=0.1, NO label]
   - intro: Add the two routes.
   - ask: 0.3 + 0.1 =  [box=0.4, NO label]
   - ask: Check: the two routes cover everything, so this is P(A). Type it again:  [box=0.4, NO label]

## gold[3] (input: fraction, main-box unit: (none))
Q: P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A' ∩ B') as a fraction.
   - intro: Neither event means A' and B'. For independent events, multiply the complements.
   - ask: P(A') = 1 − 0.4 =  [box=0.6, NO label]
   - ask: P(B') = 1 − 0.5 =  [box=0.5, NO label]
   - intro: Independent, so multiply the complements.
   - ask: 0.6 × 0.5 =  [box=0.3, NO label]
   - ask: Write 0.3 as a fraction. Numerator (0.3 = 3/10) =  [box=3, NO label]
   - ask: Denominator =  [box=10, NO label]

## gold[4] (input: fraction, main-box unit: (none))
Q: P(A ∪ B) = 0.8, P(A) = 0.5, P(B) = 0.6. Find P(A | B) as a fraction.
   - intro: First find the overlap from the addition rule, then divide by P(B).
   - ask: P(A) + P(B) = 0.5 + 0.6 =  [box=1.1, NO label]
   - ask: Subtract the union: 1.1 − 0.8 =  [box=0.3, NO label]
   - intro: Now the conditional: divide the overlap by P(B).
   - ask: 0.3 ÷ 0.6 =  [box=0.5, label:'(a decimal)']
   - ask: Write 0.5 as a fraction. Numerator (0.5 = 1/2) =  [box=1, NO label]
   - ask: Denominator =  [box=2, NO label]
