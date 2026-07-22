# maths-edexcel / probability-statistics / L02 - Venn Diagrams & Conditional Probability

## bronze[0] (input: single_value, main-box unit: (none))
Q: Tea 25Coffee 188n = 40? outside40 people: 25 like tea (T), 18 like coffee (C), 8 like both. How many like neither?
   - intro: Fill the overlap first: 8 like both. Now peel it off each circle.
   - ask: Tea only, peel off the 8 who also like coffee: 25 − 8 =  [box=17, NO label]
   - ask: Coffee only: 18 − 8 =  [box=10, NO label]
   - intro: These are everyone who likes at least one drink.
   - ask: Add the three regions inside the circles: 17 + 10 + 8 =  [box=35, NO label]
   - intro: Now finish.
   - ask: Everyone else likes neither: 40 − 35 =  [box=5, NO label]
   - ask: Check every region totals 40: 17 + 10 + 8 + 5 =  [box=40, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Tea 25Coffee 18?8n = 4040 people: 25 like tea (T), 18 like coffee (C), 8 like both. Find P(T only) as a decimal.
   - intro: Find the tea-only region first.
   - ask: How many like tea only? 25 − 8 =  [box=17, NO label]
   - intro: Now turn the count into a probability.
   - ask: Probability is that region out of 40. 17 ÷ 40 =  [box=0.425, label:'(a decimal)']
   - ask: Check: 0.425 × 40 should give the tea-only count back: 0.425 × 40 =  [box=17, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: AB1, 23, 4, 56, 7A = {1,2,3,4,5}, B = {3,4,5,6,7}. How many elements in \(A \cap B\)?
   - intro: Start with set A.
   - ask: How many elements does set A have in total?  [box=5, NO label]
   - intro: Now find the overlap.
   - ask: Intersect: keep only A's elements that are also in B = {3,4,5,6,7}. 1 and 2 are not in B; 3, 4, 5 are. How many is that?  [box=3, NO label]
   - ask: Check: 6 and 7 are only in B, so they do not count. Shared count =  [box=3, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: AB1, 23, 4, 56, 7A = {1,2,3,4,5}, B = {3,4,5,6,7}. How many elements in \(A \cup B\)?
   - intro: Start with set A.
   - ask: How many elements in A alone?  [box=5, NO label]
   - intro: Now add B's new elements.
   - ask: Union lists every element once. A already has {1,2,3,4,5}; B adds 6 and 7 (3,4,5 are already listed). How many NEW elements does B add?  [box=2, NO label]
   - ask: Total in the union: 5 + 2 =  [box=7, NO label]
   - ask: Check by listing: {1,2,3,4,5,6,7}, count =  [box=7, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: A 0.5B 0.40.2P(A ∪ B) = ?P(A) = 0.5, P(B) = 0.4, P(A ∩ B) = 0.2. Find P(A ∪ B).
   - intro: Addition rule: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).
   - ask: Add the two probabilities: 0.5 + 0.4 =  [box=0.9, NO label]
   - intro: Now finish by removing the double count.
   - ask: The 0.2 overlap was counted in both, so take it off once: 0.9 − 0.2 =  [box=0.7, NO label]
   - ask: Check with regions. A only 0.3, B only 0.2, both 0.2: 0.3 + 0.2 + 0.2 =  [box=0.7, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Maths 35Science 28?15n = 6060 students: 35 study maths (M), 28 study science (S), 15 study both. Find the number studying maths only.
   - intro: Fill the overlap first, then peel it off each circle.
   - ask: Start from the overlap of 15. Science only: 28 − 15 =  [box=13, NO label]
   - intro: Now the maths-only region.
   - ask: Maths only peels the same 15 off the 35: 35 − 15 =  [box=20, NO label]
   - ask: Check the three circle regions do not exceed 60: 20 + 13 + 15 =  [box=48, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Maths 35Science 2815n = 60? outside60 students: 35 study maths (M), 28 study science (S), 15 study both. How many study neither maths nor science?
   - intro: Peel the overlap off each subject.
   - ask: Maths only: 35 − 15 =  [box=20, NO label]
   - ask: Science only: 28 − 15 =  [box=13, NO label]
   - intro: These study at least one subject.
   - ask: Add the three regions inside the circles: 20 + 13 + 15 =  [box=48, NO label]
   - intro: Now finish.
   - ask: Everyone else studies neither: 60 − 48 =  [box=12, NO label]
   - ask: Check every region totals 60: 20 + 13 + 15 + 12 =  [box=60, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: ?AA' = 0.35total = 1If P(A') = 0.35, find P(A).
   - intro: Something must happen, so the two probabilities add to 1.
   - ask: A and not-A together must total 1. So P(A) + 0.35 must equal  [box=1, NO label]
   - intro: Now finish.
   - ask: Therefore P(A) = 1 − 0.35 =  [box=0.65, NO label]
   - ask: Check: 0.65 + 0.35 =  [box=1.0, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: A 0.7B 0.50.35P(A|B) = ?P(A) = 0.7, P(B) = 0.5, P(A ∩ B) = 0.35. Find P(A|B).
   - intro: Conditional formula: P(A|B) = P(A ∩ B) ÷ P(B). The condition B is on the bottom.
   - ask: Numerator, the overlap P(A ∩ B) =  [box=0.35, NO label]
   - intro: Now divide.
   - ask: Denominator, the condition P(B) =  [box=0.5, NO label]
   - ask: Divide: 0.35 ÷ 0.5 =  [box=0.7, label:'(a decimal)']
   - ask: Check: 0.7 × 0.5 should give the overlap back: 0.7 × 0.5 =  [box=0.35, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: French 50German 3015n = 80P(G|F) = ?80 people: 50 speak French (F), 30 speak German (G), 15 both. Find P(G|F).
   - intro: Given they speak French, shrink the world down to the 50 French speakers.
   - ask: The condition F has how many people?  [box=50, NO label]
   - intro: Now count the ones that also match.
   - ask: Of those, how many also speak German (the overlap)?  [box=15, NO label]
   - ask: P(G|F) = 15 ÷ 50 =  [box=0.3, label:'(a decimal)']
   - ask: Check: 0.3 × 50 should give the both count: 0.3 × 50 =  [box=15, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: A 0.6B 0.4?A, B independentP(A) = 0.6, P(B) = 0.4. A and B are independent. Find P(A ∩ B).
   - intro: Independent means one does not affect the other, so multiply, not add.
   - ask: Write the first probability: P(A) =  [box=0.6, label:'(a decimal)']
   - intro: Now finish the multiplication.
   - ask: Multiply by P(B): 0.6 × 0.4 =  [box=0.24, NO label]
   - ask: Check it behaves independently: P(A|B) = 0.24 ÷ 0.4 =  [box=0.6, label:'(a decimal)']

## silver[3] (input: single_value, main-box unit: (none))
Q: A 0.5B = ?0.15P(A ∪ B) = 0.75P(A) = 0.5, P(A ∩ B) = 0.15, P(A ∪ B) = 0.75. Find P(B).
   - intro: Rearrange the addition rule: P(B) = P(A ∪ B) − P(A) + P(A ∩ B).
   - ask: Start with P(A ∪ B) − P(A): 0.75 − 0.5 =  [box=0.25, NO label]
   - intro: Now finish.
   - ask: That is missing the overlap that belongs to B, so add it back: 0.25 + 0.15 =  [box=0.4, NO label]
   - ask: Check the addition rule forwards: 0.5 + 0.4 − 0.15 =  [box=0.75, NO label]

## silver[4] (input: fraction, main-box unit: (none))
Q: Sport 60Music 4520n = 100P(music | sport) = ?100 students: 60 play sport, 45 play music, 20 do both. A student who plays sport is picked at random. Find P(also plays music).
   - intro: Given they play sport, shrink the world down to the 60 sport players.
   - ask: How many play sport (the condition)?  [box=60, NO label]
   - intro: Now count the ones that also match.
   - ask: Of those, how many also play music (the overlap)?  [box=20, NO label]
   - intro: Simplify the fraction.
   - ask: So it is 20 out of 60. Simplify by dividing by 20. Numerator: 20 ÷ 20 =  [box=1, NO label]
   - ask: Denominator: 60 ÷ 20 =  [box=3, NO label]
   - ask: Check: does one third of 60 give the 20 who do both? 60 ÷ 3 =  [box=20, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: P(A|B) = 0.7 and P(B) = 0.5. Find P(A ∩ B).
   - intro: Rearrange the conditional formula: P(A ∩ B) = P(A|B) × P(B).
   - ask: Write the conditional: P(A|B) =  [box=0.7, NO label]
   - intro: Now finish.
   - ask: Multiply by P(B): 0.7 × 0.5 =  [box=0.35, NO label]
   - ask: Check with the formula forwards: P(A|B) = 0.35 ÷ 0.5 =  [box=0.7, label:'(a decimal)']

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: A 0.3B 0.40.12Independent?Are A and B independent if P(A) = 0.3, P(B) = 0.4, P(A ∩ B) = 0.12? Answer yes or no.

## gold[0] (input: single_value, main-box unit: (none))
Q: A 0.55B 0.4?neither = 0.25P(A) = 0.55, P(B) = 0.4, P(A' ∩ B') = 0.25. Find P(A ∩ B).
   - intro: Start by turning 'neither' into the union.
   - ask: 0.25 is the chance of NEITHER event. Everything else is the union. P(A ∪ B) = 1 − 0.25 =  [box=0.75, NO label]
   - intro: Now use the addition rule, P(A ∪ B) = P(A) + P(B) − P(A ∩ B), to dig out the overlap.
   - ask: First add the two singles: 0.55 + 0.4 =  [box=0.95, NO label]
   - ask: Now subtract the union: 0.95 − 0.75 =  [box=0.2, NO label]
   - ask: Check the four regions total 1. Both 0.2, A only 0.35, B only 0.2, neither 0.25: 0.2 + 0.35 + 0.2 + 0.25 =  [box=1.0, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: ABC25151020151010n = 120none = ?120 students: 70 like A, 55 like B, 45 like C. 30 like A∩B, 20 like B∩C, 25 like A∩C, 10 like all three. How many like none?
   - intro: Build the union with inclusion-exclusion. Singles first.
   - ask: Add the three single totals: 70 + 55 + 45 =  [box=170, NO label]
   - ask: Now the three pair overlaps: 30 + 20 + 25 =  [box=75, NO label]
   - intro: Inclusion-exclusion subtracts each pair once, then restores the triple.
   - ask: Singles minus pairs, then add the triple back: 170 − 75 + 10 =  [box=105, NO label]
   - intro: Now finish: everyone not in the union likes none.
   - ask: That 105 like at least one thing, so the rest like none: 120 − 105 =  [box=15, NO label]
   - ask: Check the two parts rebuild the group: 105 + 15 =  [box=120, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: 0.01Disease0.95Positive0.05Negative0.99No dis.0.05Positive0.95NegativeA medical test: P(disease) = 0.01, P(positive|disease) = 0.95, P(positive|no disease) = 0.05. Find P(positive). Give as a decimal.
   - intro: Two separate routes lead to a positive test.
   - ask: Route one, has the disease AND tests positive: 0.01 × 0.95 =  [box=0.0095, NO label]
   - intro: A healthy person can still test positive.
   - ask: Route two, no disease (that is 0.99) but a false positive: 0.99 × 0.05 =  [box=0.0495, NO label]
   - intro: Now finish by combining the routes.
   - ask: A positive can come from either route, so add them: 0.0095 + 0.0495 =  [box=0.059, NO label]
   - ask: Check with 10000 people: 100 diseased give 95 positives, 9900 healthy give 495; 95 + 495 =  [box=590, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: 0.3A0.5B0.5B'0.7A'0.2B0.8B'P(A) = 0.3, P(B|A) = 0.5, P(B|A') = 0.2. Find P(B). Give to 2 d.p.
   - intro: B can happen with A or without A. Take each route.
   - ask: Route one, B with A: 0.5 × 0.3 =  [box=0.15, NO label]
   - intro: First P(A') = 1 − 0.3 = 0.7.
   - ask: Route two, B without A (P(A') = 0.7): 0.2 × 0.7 =  [box=0.14, NO label]
   - intro: Now finish by combining the routes.
   - ask: B arrives by either route, so add them: 0.15 + 0.14 =  [box=0.29, NO label]
   - ask: Check with 100 people: 30 in A give 15, 70 not in A give 14; 15 + 14 =  [box=29, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: A 0.5B 0.6?P(A ∪ B) = 0.8Two events: P(A ∪ B) = 0.8, P(A) = 0.5, P(B) = 0.6. Are A and B mutually exclusive? Answer yes or no.
