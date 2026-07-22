# maths-ocr / probability-statistics / L02 - Venn Diagrams & Conditional Probability

## bronze[0] (input: single_value, main-box unit: (none))
Q: FootballRugby20151312Total: 6060 students: 35 play football, 28 play rugby, 15 play both. How many play at least one?
   - intro: Add both totals, then remove the overlap once so no one is counted twice.
   - ask: Football total =  [box=35, NO label]
   - ask: Rugby total =  [box=28, NO label]
   - ask: Add them: 35 + 28 =  [box=63, NO label]
   - intro: The 15 who play both were counted twice. Subtract the overlap once.
   - ask: 63 − 15 =  [box=48, NO label]
   - ask: Check by regions: football only 20, both 15, rugby only 13 add to  [box=48, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: FootballRugby201513?Total: 60Same data (60, 35, 28, 15). How many play neither?
   - intro: Neither is the whole group minus those who play at least one.
   - ask: Football only: 35 − 15 =  [box=20, NO label]
   - ask: Rugby only: 28 − 15 =  [box=13, NO label]
   - ask: At least one: 20 + 15 + 13 =  [box=48, NO label]
   - intro: Neither is the rest of the 60.
   - ask: 60 − 48 =  [box=12, NO label]
   - ask: Check: 20 + 15 + 13 + 12 =  [box=60, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: FootballRugby?151312Total: 60Same data. How many play ONLY football?
   - intro: Only football means football but not the overlap.
   - ask: Football total =  [box=35, NO label]
   - ask: Both football and rugby =  [box=15, NO label]
   - intro: Only football removes the overlap from the football total.
   - ask: 35 − 15 =  [box=20, NO label]
   - ask: Check: only football plus both = 20 + 15 =  [box=35, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: SportMusic402025?Total: 100100 students: 60 play sport, 45 play music, 20 do both. How many do neither?
   - intro: Add sport and music, subtract the overlap, then take that from 100.
   - ask: Sport plus music: 60 + 45 =  [box=105, NO label]
   - ask: Subtract the overlap once: 105 − 20 =  [box=85, NO label]
   - intro: Neither is the rest of the 100.
   - ask: 100 − 85 =  [box=15, NO label]
   - ask: Check: sport only 40, music only 25, both 20, neither 15 add to  [box=100, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: AB0.450.150.150.25Total: 1P(A) = 0.6, P(B) = 0.3, P(A∩B) = 0.15. Find P(A∪B).
   - intro: Union adds the two sets, then removes the overlap once.
   - ask: P(A) + P(B) = 0.6 + 0.3 =  [box=0.9, NO label]
   - ask: The overlap P(A∩B) =  [box=0.15, NO label]
   - intro: Subtract the overlap once.
   - ask: 0.9 − 0.15 =  [box=0.75, NO label]
   - ask: Check by regions: 0.45 + 0.15 + 0.15 =  [box=0.75, NO label]

## bronze[5] (input: fraction, main-box unit: (none))
Q: CatsDogs?10153Total: 4040 students: 22 like cats, 25 like dogs, 10 like both. P(likes cats only) out of 40.
   - intro: Cats only means cats but not the overlap. Find that count over the total.
   - ask: Cats only: 22 − 10 =  [box=12, NO label]
   - ask: Total students =  [box=40, NO label]
   - intro: So P(cats only) = 12/40. Simplify by dividing by 4.
   - ask: 12 ÷ 4 =  [box=3, NO label]
   - ask: 40 ÷ 4 =  [box=10, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: FrenchGerman108?5Total: 3030 students: 18 study French, 15 study German, 8 both. How many study only German?
   - intro: Only German means German but not the overlap.
   - ask: German total =  [box=15, NO label]
   - ask: Both French and German =  [box=8, NO label]
   - intro: Only German removes the overlap from the German total.
   - ask: 15 − 8 =  [box=7, NO label]
   - ask: Check: only German plus both = 7 + 8 =  [box=15, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: P(A) = 0.5, P(A∩B) = 0.2. Find P(A only, not B).
   - intro: A only is all of A with the overlap removed.
   - ask: All of A, P(A) =  [box=0.5, NO label]
   - ask: The overlap P(A∩B) =  [box=0.2, NO label]
   - intro: Take the overlap off P(A).
   - ask: 0.5 − 0.2 =  [box=0.3, NO label]
   - ask: Check: A only plus overlap = 0.3 + 0.2 =  [box=0.5, NO label]

## silver[0] (input: fraction, main-box unit: (none))
Q: SportMusic40202515Total: 100100 students: 60 play sport, 45 play music, 20 both. P(music | sport).
   - intro: Given sport, look only inside the sport group. Divide the overlap by the sport total.
   - ask: Both sport and music =  [box=20, NO label]
   - ask: Sport total (the given group) =  [box=60, NO label]
   - intro: So P(music|sport) = 20/60. Simplify by dividing by 20.
   - ask: 20 ÷ 20 =  [box=1, NO label]
   - ask: 60 ÷ 20 =  [box=3, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: AB0.40.30.20.1Total: 1P(A) = 0.7, P(B) = 0.5, P(A∩B) = 0.3. Find P(B|A).
   - intro: For P(B given A), divide the overlap by P(A).
   - ask: The overlap P(A∩B) =  [box=0.3, NO label]
   - ask: The given group P(A) =  [box=0.7, NO label]
   - intro: Divide the overlap by P(A). Round to 3 decimal places.
   - ask: 0.3 ÷ 0.7 =  [box=0.429, label:'(a decimal)']
   - ask: Check: 0.429 × 0.7 ≈ 0.3, the overlap. Type the answer again:  [box=0.429, NO label]

## silver[2] (input: fraction, main-box unit: (none))
Q: TeaCoffee35152010Total: 8080 people: 50 tea, 35 coffee, 15 both. P(tea | coffee).
   - intro: Given coffee, look only inside the coffee group. Divide the overlap by the coffee total.
   - ask: Both tea and coffee =  [box=15, NO label]
   - ask: Coffee total (the given group) =  [box=35, NO label]
   - intro: So P(tea|coffee) = 15/35. Simplify by dividing by 5.
   - ask: 15 ÷ 5 =  [box=3, NO label]
   - ask: 35 ÷ 5 =  [box=7, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: P(A∪B) = 0.8, P(A) = 0.5, P(B) = 0.4. Find P(A∩B).
   - intro: Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union.
   - ask: P(A) + P(B) = 0.5 + 0.4 =  [box=0.9, NO label]
   - ask: The union P(A∪B) =  [box=0.8, NO label]
   - intro: Subtract the union from that sum.
   - ask: 0.9 − 0.8 =  [box=0.1, NO label]
   - ask: Check: 0.5 + 0.4 − 0.1 = 0.8, the union. Type the overlap again:  [box=0.1, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: AB0.30.4neither 0.3Total: 1Events A and B are mutually exclusive. P(A) = 0.3, P(B) = 0.4. P(A∪B)?
   - intro: Mutually exclusive means the events cannot both happen, so the overlap is zero.
   - ask: The overlap P(A∩B) for mutually exclusive events =  [box=0, NO label]
   - ask: P(A) + P(B) = 0.3 + 0.4 =  [box=0.7, NO label]
   - intro: With no overlap to subtract, the union is just the sum.
   - ask: 0.7 − 0 =  [box=0.7, NO label]
   - ask: Check: the two separate slices give 0.3 + 0.4 =  [box=0.7, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Are A and B independent if P(A) = 0.5, P(B) = 0.4, P(A∩B) = 0.2? Enter 1 yes, 0 no.
   - intro: Independent when P(A) × P(B) equals P(A∩B).
   - ask: P(A) × P(B) = 0.5 × 0.4 =  [box=0.2, NO label]
   - ask: The given overlap P(A∩B) =  [box=0.2, NO label]
   - intro: Compare the product with the overlap.
   - ask: They are equal, so enter 1 for yes:  [box=1, NO label]
   - ask: Check: independent needs 0.5 × 0.4 = 0.2 = P(A∩B). Enter 1 again:  [box=1, NO label]

## silver[6] (input: fraction, main-box unit: (none))
Q: BusWalk50203515Total: 120120 students: 70 bus, 55 walk, 20 both. P(walk | not bus).
   - intro: Given not bus, restrict to those who do not take the bus, then find the walkers among them.
   - ask: Not bus: 120 − 70 =  [box=50, NO label]
   - ask: Walk and not bus: 55 − 20 =  [box=35, NO label]
   - intro: So P(walk|not bus) = 35/50. Simplify by dividing by 5.
   - ask: 35 ÷ 5 =  [box=7, NO label]
   - ask: 50 ÷ 5 =  [box=10, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: P(A|B) = 0.6, P(B) = 0.5. Find P(A∩B).
   - intro: Multiply rule: P(A∩B) = P(A|B) × P(B).
   - ask: P(A|B) =  [box=0.6, NO label]
   - ask: P(B) =  [box=0.5, NO label]
   - intro: Multiply them together.
   - ask: 0.6 × 0.5 =  [box=0.3, NO label]
   - ask: Check: an overlap is smaller than each part. Type 0.3 again:  [box=0.3, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: P(A) = 0.4, P(B|A) = 0.6. Find P(A∩B).
   - intro: Multiply rule: P(A∩B) = P(B|A) × P(A).
   - ask: P(B|A) =  [box=0.6, NO label]
   - ask: P(A) =  [box=0.4, NO label]
   - intro: Multiply them together.
   - ask: 0.6 × 0.4 =  [box=0.24, NO label]
   - ask: Check: the overlap is smaller than each part. Type 0.24 again:  [box=0.24, NO label]

## gold[2] (input: fraction, main-box unit: (none))
Q: MathsPhysics50503070Total: 200200 students: 100 A-level maths, 80 A-level physics, 50 both. A student who does physics is chosen. P(also does maths).
   - intro: Given physics, look only inside the physics group. Divide the both count by the physics total.
   - ask: Both maths and physics =  [box=50, NO label]
   - ask: Physics total (the given group) =  [box=80, NO label]
   - intro: So P(maths|physics) = 50/80. Simplify by dividing by 10.
   - ask: 50 ÷ 10 =  [box=5, NO label]
   - ask: 80 ÷ 10 =  [box=8, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: P(A) = 0.3, P(B) = 0.6, events independent. P(neither A nor B)?
   - intro: Neither means not A and not B. For independent events, multiply the complements.
   - ask: P(A') = 1 − 0.3 =  [box=0.7, NO label]
   - ask: P(B') = 1 − 0.6 =  [box=0.4, NO label]
   - intro: Independent, so multiply the complements.
   - ask: 0.7 × 0.4 =  [box=0.28, NO label]
   - ask: Check: overlap 0.18, A only 0.12, B only 0.42, neither 0.28 add to  [box=1, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: AB0.40.2?0.1Total: 1P(A∪B) = 0.9, P(A) = 0.6, P(A∩B) = 0.2. Find P(B).
   - intro: Rearrange the addition rule to make P(B) the subject: P(B) = P(A∪B) − P(A) + P(A∩B).
   - ask: P(A∪B) − P(A) = 0.9 − 0.6 =  [box=0.3, NO label]
   - ask: The overlap P(A∩B) =  [box=0.2, NO label]
   - intro: Add the overlap back, because subtracting P(A) also removed the shared part.
   - ask: 0.3 + 0.2 =  [box=0.5, NO label]
   - ask: Check: 0.6 + 0.5 − 0.2 = 0.9, the union. Type P(B) again:  [box=0.5, NO label]
