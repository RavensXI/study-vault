# apply-pack: probability-statistics__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[2] | Intersect: keep only A's elements that are also in B = {3,4,5,6,7}. 1 and 2 are  | fix: Split it: 'Keep only A's elements that are also in B. B = {3,4,5,6,7}, so 3, 4 and 5 count but 1 and 2 do not. How many is that?'
- [low] gold[2] | Route one, has the disease AND tests positive: 0.01 x 0.95 = ___ | fix: Add a line before the multiply: 'To get both things happening on one route, multiply along the branch: 0.01 x 0.95 = ___.'
- [low] gold[3] | Route one, B with A: 0.5 x 0.3 = ___ | fix: Add 'B happening AND A happening means multiply along the branch: 0.5 x 0.3 = ___,' or a one-line note that combined events multiply.
- [low] silver[4] | Q: Are events A and B independent if P(A) = 0.4, P(B) = 0.3, P(A ∩ B) = 0.12? | fix: Add a one-line reminder to the stem, e.g. 'Independent means P(A) × P(B) = P(A ∩ B). Work out 0.4 × 0.3 and compare it with 0.12.'
- [low] silver[2] | Check: 0.8 + 0.5 − 0.4 = 0.9, the union. Type the overlap again: [box=0.4, NO la | fix: State the number: 'Type the overlap (0.4) again:'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: CatDog22131510Total: 6060 people: 35 own a cat, 28 own a dog, 13 own both. Find P(cat or d
   step0 field=say answer=None text='Cat or dog means in either circle. Add the totals, then subtract the overlap once so it is'
   step1 field=pre answer=63 text='Cats plus dogs: 35 + 28 ='
   step2 field=pre answer=50 text='Subtract the overlap once: 63 − 13 ='
   step3 field=pre answer=60 text='Total people ='
   step4 field=pre answer=5 text='50 ÷ 10 ='
   step5 field=pre answer=6 text='60 ÷ 10 ='

gold[2] Q: P(A|B) = 0.6, P(B) = 0.5. P(A|B') = 0.2, P(B') = 0.5. Find P(A).
   step0 field=say answer=None text='A can happen through B or through not B. Total probability adds both routes.'
   step1 field=pre answer=0.3 text='Route through B: 0.6 × 0.5 ='
   step2 field=pre answer=0.1 text='Route through not B: 0.2 × 0.5 ='
   step3 field=pre answer=0.4 text='0.3 + 0.1 ='
   step4 field=pre answer=0.4 text='Check: the two routes cover everything, so this is P(A). Type it again:'

gold[3] Q: P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A' ∩ B') as a fraction.
   step0 field=say answer=None text="Neither event means A' and B'. For independent events, multiply the complements."
   step1 field=pre answer=0.6 text="P(A') = 1 − 0.4 ="
   step2 field=pre answer=0.5 text="P(B') = 1 − 0.5 ="
   step3 field=pre answer=0.3 text='0.6 × 0.5 ='
   step4 field=pre answer=3 text='Write 0.3 as a fraction. Numerator (0.3 = 3/10) ='
   step5 field=pre answer=10 text='Denominator ='

silver[2] Q: P(A) = 0.7, P(B) = 0.5, P(A ∪ B) = 0.9. Find P(A ∩ B).
   step0 field=say answer=None text='Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union.'
   step1 field=pre answer=1.2 text='P(A) + P(B) = 0.7 + 0.5 ='
   step2 field=pre answer=0.9 text='The union P(A ∪ B) ='
   step3 field=pre answer=0.3 text='1.2 − 0.9 ='
   step4 field=pre answer=0.3 text='Check: 0.7 + 0.5 − 0.3 = 0.9, the union. Type the overlap again:'

silver[4] Q: Are events A and B independent if P(A) = 0.3, P(B) = 0.4, P(A ∩ B) = 0.12?

### board=maths-edexcel
bronze[2] Q: AB1, 23, 4, 56, 7A = {1,2,3,4,5}, B = {3,4,5,6,7}. How many elements in \(A \cap B\)?
   step0 field=pre answer=5 text='How many elements does set A have in total?'
   step1 field=pre answer=3 text="Intersect: keep only A's elements that are also in B = {3,4,5,6,7}. 1 and 2 are not in B; "
   step2 field=pre answer=3 text='Check: 6 and 7 are only in B, so they do not count. Shared count ='

gold[2] Q: 0.01Disease0.95Positive0.05Negative0.99No dis.0.05Positive0.95NegativeA medical test: P(di
   step0 field=pre answer=0.0095 text='Route one, has the disease AND tests positive: 0.01 × 0.95 ='
   step1 field=pre answer=0.0495 text='Route two, no disease (that is 0.99) but a false positive: 0.99 × 0.05 ='
   step2 field=pre answer=0.059 text='A positive can come from either route, so add them: 0.0095 + 0.0495 ='
   step3 field=pre answer=590 text='Check with 10000 people: 100 diseased give 95 positives, 9900 healthy give 495; 95 + 495 ='

gold[3] Q: 0.3A0.5B0.5B'0.7A'0.2B0.8B'P(A) = 0.3, P(B|A) = 0.5, P(B|A') = 0.2. Find P(B). Give to 2 d
   step0 field=pre answer=0.15 text='Route one, B with A: 0.5 × 0.3 ='
   step1 field=pre answer=0.14 text="Route two, B without A (P(A') = 0.7): 0.2 × 0.7 ="
   step2 field=pre answer=0.29 text='B arrives by either route, so add them: 0.15 + 0.14 ='
   step3 field=pre answer=29 text='Check with 100 people: 30 in A give 15, 70 not in A give 14; 15 + 14 ='

silver[2] Q: A 0.6B 0.4?A, B independentP(A) = 0.6, P(B) = 0.4. A and B are independent. Find P(A ∩ B).
   step0 field=pre answer=0.6 text='Write the first probability: P(A) ='
   step1 field=pre answer=0.24 text='Multiply by P(B): 0.6 × 0.4 ='
   step2 field=pre answer=0.6 text='Check it behaves independently: P(A|B) = 0.24 ÷ 0.4 ='

silver[4] Q: Sport 60Music 4520n = 100P(music | sport) = ?100 students: 60 play sport, 45 play music, 2
   step0 field=pre answer=60 text='How many play sport (the condition)?'
   step1 field=pre answer=20 text='Of those, how many also play music (the overlap)?'
   step2 field=pre answer=1 text='So it is 20 out of 60. Simplify by dividing by 20. Numerator: 20 ÷ 20 ='
   step3 field=pre answer=3 text='Denominator: 60 ÷ 20 ='
   step4 field=pre answer=20 text='Check: does one third of 60 give the 20 who do both? 60 ÷ 3 ='

### board=maths-ocr
bronze[2] Q: FootballRugby?151312Total: 60Same data. How many play ONLY football?
   step0 field=say answer=None text='Only football means football but not the overlap.'
   step1 field=pre answer=35 text='Football total ='
   step2 field=pre answer=15 text='Both football and rugby ='
   step3 field=pre answer=20 text='35 − 15 ='
   step4 field=pre answer=35 text='Check: only football plus both = 20 + 15 ='

gold[2] Q: MathsPhysics50503070Total: 200200 students: 100 A-level maths, 80 A-level physics, 50 both
   step0 field=say answer=None text='Given physics, look only inside the physics group. Divide the both count by the physics to'
   step1 field=pre answer=50 text='Both maths and physics ='
   step2 field=pre answer=80 text='Physics total (the given group) ='
   step3 field=pre answer=5 text='50 ÷ 10 ='
   step4 field=pre answer=8 text='80 ÷ 10 ='

gold[3] Q: P(A) = 0.3, P(B) = 0.6, events independent. P(neither A nor B)?
   step0 field=say answer=None text='Neither means not A and not B. For independent events, multiply the complements.'
   step1 field=pre answer=0.7 text="P(A') = 1 − 0.3 ="
   step2 field=pre answer=0.4 text="P(B') = 1 − 0.6 ="
   step3 field=pre answer=0.28 text='0.7 × 0.4 ='
   step4 field=pre answer=1 text='Check the four regions cover everything: overlap 0.3×0.6=0.18, A only 0.3×0.4=0.12, B only'

silver[2] Q: TeaCoffee35152010Total: 8080 people: 50 tea, 35 coffee, 15 both. P(tea | coffee).
   step0 field=say answer=None text='Given coffee, look only inside the coffee group. Divide the overlap by the coffee total.'
   step1 field=pre answer=15 text='Both tea and coffee ='
   step2 field=pre answer=35 text='Coffee total (the given group) ='
   step3 field=pre answer=3 text='15 ÷ 5 ='
   step4 field=pre answer=7 text='35 ÷ 5 ='

silver[4] Q: AB0.30.4neither 0.3Total: 1Events A and B are mutually exclusive. P(A) = 0.3, P(B) = 0.4. 
   step0 field=say answer=None text='Mutually exclusive means the events cannot both happen, so the overlap is zero.'
   step1 field=pre answer=0 text='The overlap P(A∩B) for mutually exclusive events ='
   step2 field=pre answer=0.7 text='P(A) + P(B) = 0.3 + 0.4 ='
   step3 field=pre answer=0.7 text='0.7 − 0 ='
   step4 field=pre answer=0.7 text='Check: the two separate slices give 0.3 + 0.4 ='

### board=maths-eduqas
bronze[2] Q: CatDog30152015Total: 8080 people: 45 own a cat, 35 own a dog, 15 own both. Find P(cat or d
   step0 field=say answer=None text='Cat or dog means in either circle. Add the totals, then subtract the overlap once so it is'
   step1 field=pre answer=80 text='Cats plus dogs: 45 + 35 ='
   step2 field=pre answer=65 text='Subtract the overlap once: 80 − 15 ='
   step3 field=pre answer=80 text='Total people ='
   step4 field=pre answer=13 text='So P(cat or dog) = 65/80. Simplify by 5, top: 65 ÷ 5 ='
   step5 field=pre answer=16 text='80 ÷ 5 ='

gold[2] Q: P(A|B) = 0.7, P(B) = 0.4. P(A|B') = 0.3, P(B') = 0.6. Find P(A).
   step0 field=say answer=None text='A can happen through B or through not B. Total probability adds both routes.'
   step1 field=pre answer=0.28 text='Route through B: 0.7 × 0.4 ='
   step2 field=pre answer=0.18 text='Route through not B: 0.3 × 0.6 ='
   step3 field=pre answer=0.46 text='Add the two routes: 0.28 + 0.18 ='
   step4 field=pre answer=0.46 text='Check: the two routes cover everything, so this is P(A). Type it again:'

gold[3] Q: P(A) = 0.3, P(B) = 0.6. A and B are independent. Find P(A' ∩ B') as a simplified fraction.
   step0 field=say answer=None text="Neither event means A' and B'. For independent events, multiply the complements."
   step1 field=pre answer=0.7 text="P(A') = 1 − 0.3 ="
   step2 field=pre answer=0.4 text="P(B') = 1 − 0.6 ="
   step3 field=pre answer=0.28 text='Independent, so multiply: 0.7 × 0.4 ='
   step4 field=pre answer=7 text='0.28 = 28/100. Simplify by 4, top: 28 ÷ 4 ='
   step5 field=pre answer=25 text='100 ÷ 4 ='

silver[2] Q: P(A) = 0.8, P(B) = 0.5, P(A ∪ B) = 0.9. Find P(A ∩ B).
   step0 field=say answer=None text='Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union.'
   step1 field=pre answer=1.3 text='P(A) + P(B) = 0.8 + 0.5 ='
   step2 field=pre answer=0.9 text='The union P(A ∪ B) ='
   step3 field=pre answer=0.4 text='Subtract the union: 1.3 − 0.9 ='
   step4 field=pre answer=0.4 text='Check: 0.8 + 0.5 − 0.4 = 0.9, the union. Type the overlap again:'

silver[4] Q: Are events A and B independent if P(A) = 0.4, P(B) = 0.3, P(A ∩ B) = 0.12?
