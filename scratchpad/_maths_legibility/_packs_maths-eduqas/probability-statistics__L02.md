# maths-eduqas / probability-statistics / L02 - Venn Diagrams & Conditional Probability

## bronze[0] (input: single_value, main-box unit: (none))
Q: MathsScience181012?Total: 5050 students: 28 like maths, 22 like science, 10 like both. How many like neither?
   - intro: Fill the Venn from the middle out: the overlap first, then each single region, then what is left.
   - ask: Both maths and science (the overlap) =  [box=10, NO label]
   - ask: Maths only: 28 − 10 =  [box=18, NO label]
   - ask: Science only: 22 − 10 =  [box=12, NO label]
   - intro: Add the three filled regions.
   - ask: Add the three filled regions: 18 + 10 + 12 =  [box=40, NO label]
   - ask: Neither: 50 − 40 =  [box=10, NO label]

## bronze[1] (input: fraction, main-box unit: (none))
Q: MathsScience18101210Total: 50From the same data (50 students, 28 maths, 22 science, 10 both), find P(maths only) as a simplified fraction.
   - intro: Maths only means maths but NOT the overlap. Find that count, then put it over the total.
   - ask: Maths only: 28 − 10 =  [box=18, NO label]
   - ask: Total students =  [box=50, NO label]
   - intro: Simplify by dividing top and bottom by 2.
   - ask: So P(maths only) = 18/50. Simplify by 2, top: 18 ÷ 2 =  [box=9, NO label]
   - ask: 50 ÷ 2 =  [box=25, NO label]

## bronze[2] (input: fraction, main-box unit: (none))
Q: CatDog30152015Total: 8080 people: 45 own a cat, 35 own a dog, 15 own both. Find P(cat or dog) as a simplified fraction.
   - intro: Cat or dog means in either circle. Add the totals, then subtract the overlap once so it is not double counted.
   - ask: Cats plus dogs: 45 + 35 =  [box=80, NO label]
   - ask: Subtract the overlap once: 80 − 15 =  [box=65, NO label]
   - ask: Total people =  [box=80, NO label]
   - intro: Simplify by dividing by 5.
   - ask: So P(cat or dog) = 65/80. Simplify by 5, top: 65 ÷ 5 =  [box=13, NO label]
   - ask: 80 ÷ 5 =  [box=16, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: AB1261814Total: ?A Venn diagram has: A only = 12, B only = 18, A ∩ B = 6, neither = 14. What is the total?
   - intro: The total is every region added together, including the neither region outside the circles.
   - ask: Overlap (A and B) =  [box=6, NO label]
   - ask: In the circles: 12 + 6 + 18 =  [box=36, NO label]
   - intro: Add the neither region to reach the total.
   - ask: Now add the neither region: 36 + 14 =  [box=50, NO label]
   - ask: Check: 12 + 6 + 18 + 14 =  [box=50, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: P(A) = 0.7, P(A ∩ B) = 0.3. Find P(A only) as a decimal.
   - intro: A only means the part of A that does not overlap B. Subtract the overlap from all of A.
   - ask: All of A, P(A) =  [box=0.7, NO label]
   - ask: The overlap P(A ∩ B) =  [box=0.3, NO label]
   - intro: A only is what is left after removing the overlap.
   - ask: A only: 0.7 − 0.3 =  [box=0.4, NO label]
   - ask: Check: A only plus overlap gives all of A. 0.4 + 0.3 =  [box=0.7, NO label]

## bronze[5] (input: fraction, main-box unit: (none))
Q: EnglishHistory241212?Total: 6060 students: 36 like English, 24 like History, 12 like both. Find P(neither) as a simplified fraction.
   - intro: Find how many like at least one subject, then the rest of the group like neither.
   - ask: English only: 36 − 12 =  [box=24, NO label]
   - ask: History only: 24 − 12 =  [box=12, NO label]
   - ask: At least one: 24 + 12 + 12 =  [box=48, NO label]
   - intro: Neither is the total minus those 48.
   - ask: Neither: 60 − 48 =  [box=12, NO label]
   - ask: So P(neither) = 12/60. Simplify by 12, top: 12 ÷ 12 =  [box=1, NO label]
   - ask: 60 ÷ 12 =  [box=5, NO label]

## bronze[6] (input: fraction, main-box unit: (none))
Q: AB228Total: 60A Venn diagram shows 30 students in set A and 8 in A ∩ B, out of 60 total. Find P(A) as a simplified fraction.
   - intro: P(A) uses everyone inside circle A: both the overlap and the A-only part.
   - ask: Number in set A =  [box=30, NO label]
   - ask: Total students =  [box=60, NO label]
   - intro: Simplify by dividing by 30.
   - ask: So P(A) = 30/60. Simplify by 30, top: 30 ÷ 30 =  [box=1, NO label]
   - ask: 60 ÷ 30 =  [box=2, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: AB?152025Total: 100100 people: P(A) = 0.55, P(B) = 0.35, P(A ∩ B) = 0.15. How many are in A only?
   - intro: Turn each probability into a count out of 100, then take the overlap off A.
   - ask: n(A) = 0.55 × 100 =  [box=55, NO label]
   - ask: n(A ∩ B) = 0.15 × 100 =  [box=15, NO label]
   - intro: A only removes the overlap from A.
   - ask: A only: 55 − 15 =  [box=40, NO label]
   - ask: Check: A only plus overlap = 40 + 15 =  [box=55, NO label]

## silver[0] (input: fraction, main-box unit: (none))
Q: FootballRugby35252010Total: 9090 students: 60 like football, 45 like rugby, 25 like both. Find P(football | rugby) as a simplified fraction.
   - intro: Given rugby, we only look inside the rugby group. P(F|R) = both, over the rugby total.
   - ask: Both football and rugby =  [box=25, NO label]
   - ask: Rugby total (the given group) =  [box=45, NO label]
   - intro: Simplify by dividing by 5.
   - ask: So P(F|R) = 25/45. Simplify by 5, top: 25 ÷ 5 =  [box=5, NO label]
   - ask: 45 ÷ 5 =  [box=9, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: P(A) = 0.6, P(B) = 0.5, P(A ∩ B) = 0.2. Find P(A ∪ B).
   - intro: Union is everything in either set. Add the two, then subtract the overlap so it is counted once.
   - ask: P(A) + P(B) = 0.6 + 0.5 =  [box=1.1, NO label]
   - ask: The overlap P(A ∩ B) =  [box=0.2, NO label]
   - intro: Subtract the overlap once.
   - ask: Subtract the overlap once: 1.1 − 0.2 =  [box=0.9, NO label]
   - ask: Check: 0.6 + 0.5 − 0.2 =  [box=0.9, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: P(A) = 0.8, P(B) = 0.5, P(A ∪ B) = 0.9. Find P(A ∩ B).
   - intro: Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union.
   - ask: P(A) + P(B) = 0.8 + 0.5 =  [box=1.3, NO label]
   - ask: The union P(A ∪ B) =  [box=0.9, NO label]
   - intro: Subtract the union from that sum.
   - ask: Subtract the union: 1.3 − 0.9 =  [box=0.4, NO label]
   - ask: Check: 0.8 + 0.5 − 0.4 = 0.9, the union. Type the overlap again:  [box=0.4, NO label]

## silver[3] (input: fraction, main-box unit: (none))
Q: NetballHockey20151510Total: 6060 students: 35 play netball, 30 play hockey, 15 play both. Find P(hockey | netball) as a simplified fraction.
   - intro: Given netball, look only inside the netball group. P(H|N) = both, over the netball total.
   - ask: Both hockey and netball =  [box=15, NO label]
   - ask: Netball total (the given group) =  [box=35, NO label]
   - intro: Simplify by dividing by 5.
   - ask: So P(H|N) = 15/35. Simplify by 5, top: 15 ÷ 5 =  [box=3, NO label]
   - ask: 35 ÷ 5 =  [box=7, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: Are events A and B independent if P(A) = 0.4, P(B) = 0.3, P(A ∩ B) = 0.12?

## silver[5] (input: fraction, main-box unit: (none))
Q: P(B) = 0.5, P(A ∩ B) = 0.2. Find P(A | B) as a simplified fraction.
   - intro: Conditional formula: P(A|B) = P(A ∩ B) over P(B).
   - ask: P(A ∩ B) =  [box=0.2, NO label]
   - ask: P(B) =  [box=0.5, NO label]
   - intro: Divide the overlap by P(B).
   - ask: Divide the overlap by P(B): 0.2 ÷ 0.5 =  [box=0.4, label:'(a decimal)']
   - ask: 0.4 = 4/10, simplify by 2, top: 4 ÷ 2 =  [box=2, NO label]
   - ask: 10 ÷ 2 =  [box=5, NO label]

## silver[6] (input: fraction, main-box unit: (none))
Q: GirlDrama20603040Total: 150150 students: 80 girls, 90 do drama, 60 girls do drama. Find P(girl | does drama) as a simplified fraction.
   - intro: Given drama, look only inside the drama group. P(girl|drama) = girls who do drama, over all who do drama.
   - ask: Girls who do drama =  [box=60, NO label]
   - ask: Total who do drama (the given group) =  [box=90, NO label]
   - intro: Simplify by dividing by 30.
   - ask: So P(girl|drama) = 60/90. Simplify by 30, top: 60 ÷ 30 =  [box=2, NO label]
   - ask: 90 ÷ 30 =  [box=3, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: P(A) = 0.4, P(B|A) = 0.5. Find P(A ∩ B).
   - intro: Multiply rule: P(A ∩ B) = P(A) × P(B given A).
   - ask: P(A) =  [box=0.4, NO label]
   - ask: P(B given A) =  [box=0.5, NO label]
   - intro: Multiply them together.
   - ask: Multiply them: 0.4 × 0.5 =  [box=0.2, NO label]
   - ask: Check: an overlap is smaller than each part. Type 0.2 again:  [box=0.2, NO label]

## gold[1] (input: fraction, main-box unit: (none))
Q: TeaCoffee45251515Total: 100100 people: 70 like tea, 40 like coffee, 25 like both. A person who likes tea is chosen. Find P(also likes coffee) as a simplified fraction.
   - intro: Given tea, look only inside the tea group. P(coffee|tea) = both, over the tea total.
   - ask: Both tea and coffee =  [box=25, NO label]
   - ask: Tea total (the given group) =  [box=70, NO label]
   - intro: Simplify by dividing by 5.
   - ask: So P(coffee|tea) = 25/70. Simplify by 5, top: 25 ÷ 5 =  [box=5, NO label]
   - ask: 70 ÷ 5 =  [box=14, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: P(A|B) = 0.7, P(B) = 0.4. P(A|B') = 0.3, P(B') = 0.6. Find P(A).
   - intro: A can happen through B or through not B. Total probability adds both routes.
   - ask: Route through B: 0.7 × 0.4 =  [box=0.28, NO label]
   - ask: Route through not B: 0.3 × 0.6 =  [box=0.18, NO label]
   - intro: Add the two routes.
   - ask: Add the two routes: 0.28 + 0.18 =  [box=0.46, NO label]
   - ask: Check: the two routes cover everything, so this is P(A). Type it again:  [box=0.46, NO label]

## gold[3] (input: fraction, main-box unit: (none))
Q: P(A) = 0.3, P(B) = 0.6. A and B are independent. Find P(A' ∩ B') as a simplified fraction.
   - intro: Neither event means A' and B'. For independent events, multiply the complements.
   - ask: P(A') = 1 − 0.3 =  [box=0.7, NO label]
   - ask: P(B') = 1 − 0.6 =  [box=0.4, NO label]
   - intro: Independent, so multiply the complements.
   - ask: Independent, so multiply: 0.7 × 0.4 =  [box=0.28, NO label]
   - ask: 0.28 = 28/100. Simplify by 4, top: 28 ÷ 4 =  [box=7, NO label]
   - ask: 100 ÷ 4 =  [box=25, NO label]

## gold[4] (input: fraction, main-box unit: (none))
Q: P(A ∪ B) = 0.85, P(A) = 0.6, P(B) = 0.5. Find P(A | B) as a simplified fraction.
   - intro: First find the overlap from the addition rule, then divide by P(B).
   - ask: P(A) + P(B) = 0.6 + 0.5 =  [box=1.1, NO label]
   - ask: Subtract the union: 1.1 − 0.85 =  [box=0.25, NO label]
   - intro: Divide the overlap by P(B).
   - ask: Now the conditional: 0.25 ÷ 0.5 =  [box=0.5, label:'(a decimal)']
   - ask: Write 0.5 as a fraction. Numerator (0.5 = 1/2) =  [box=1, NO label]
   - ask: Denominator =  [box=2, NO label]
