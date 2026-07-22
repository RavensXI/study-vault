# apply-pack: number__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[2] | 12.4 cm5.8 cmA rectangle is 12.4 cm by 5.8 cm (both to 1 d.p.). Find the lower b | fix: Separate the fragments: keep the side labels on the diagram only, and space the note out — '...the perimeter (cm). (Diagram not drawn accurately.)'
- [medium] gold[4] | The smallest speed uses 99.5 ÷ 12.35 = 8.056, to 1 d.p. = [box=8.1, NO label] | fix: Either show the two missing bounds explicitly in the step (99.5 = 100 − 0.5, 12.35 = 12.3 + 0.05) or drop this 'for comparison' line, since the question only as

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: 12.4 cm5.8 cmA rectangle is \(12.4\) cm by \(5.8\) cm (both to 1 d.p.). Find the lower bou
   step0 field=say answer=None text='The smallest possible perimeter uses the smallest possible side lengths.'
   step1 field=pre answer=12.35 text='Lower bound of 12.4 (to 1 d.p.): 12.4 − 0.05. Work it out.'
   step2 field=pre answer=5.75 text='Lower bound of 5.8: 5.8 − 0.05. Work it out.'
   step3 field=pre answer=18.1 text='Perimeter = 2 × (length + width). Add the two lower bounds: 12.35 + 5.75.'
   step4 field=pre answer=36.2 text='Double it: 2 × 18.1.'

gold[4] Q: \(v = \frac{d}{t}\). \(d = 240\) m (2 s.f.), \(t = 8.4\) s (1 d.p.). Find the upper bound 
   step0 field=say answer=None text='Speed is largest when the distance is at its biggest and the time at its smallest.'
   step1 field=pre answer=245 text='Upper bound of d = 240 to 2 s.f. (nearest 10, so within 5): 240 + 5. Work it out.'
   step2 field=pre answer=8.35 text='Lower bound of t = 8.4 to 1 d.p. (within 0.05): 8.4 − 0.05. Work it out.'
   step3 field=pre answer=29.3 text='Maximum v = 245 ÷ 8.35, rounded to 3 s.f. Work it out.'
   step4 field=pre answer=29.3 text='Confirm the upper bound of v to 3 s.f.'

### board=maths-edexcel
gold[2] Q: A rectangle is \(8.5\) cm by \(3.2\) cm (both to 1 d.p.). Find the lower bound of the area
   step0 field=say answer=None text='Both sides are to 1 d.p., so each has a half unit of 0.05. The smallest area uses the smal'
   step1 field=pre answer=8.45 text='Lower bound of 8.5 = 8.5 − 0.05 ='
   step2 field=pre answer=3.15 text='Lower bound of 3.2 = 3.2 − 0.05 ='
   step3 field=pre answer=26.6175 text='Smallest area = 8.45 × 3.15 ='
   step4 field=pre answer=27.2 text='For comparison, the given-value area 8.5 × 3.2 ='

gold[4] Q: A speed is \(\frac{\text{distance}}{\text{time}}\). Distance = \(100\) m (nearest m), time
   step0 field=say answer=None text='Speed = distance ÷ time. For the biggest speed, use the biggest distance and the smallest '
   step1 field=pre answer=100.5 text='Biggest distance: 100 to the nearest metre, upper bound = 100 + 0.5 ='
   step2 field=pre answer=12.25 text='Smallest time: 12.3 to 1 d.p., lower bound = 12.3 − 0.05 ='
   step3 field=pre answer=8.2 text='Biggest speed = 100.5 ÷ 12.25 = 8.204..., to 1 d.p. ='
   step4 field=pre answer=8.1 text='The smallest speed uses 99.5 ÷ 12.35 = 8.056, to 1 d.p. ='

### board=maths-ocr
gold[2] Q: \(a = 6.0\) (1 d.p.), \(b = 2.0\) (1 d.p.). Find the upper bound of \(\frac{a}{b}\). (Give
   step0 field=pre answer=0.05 text='Half unit for 1 d.p. ='
   step1 field=pre answer=6.05 text='Upper bound of a = 6.0 + 0.05 ='
   step2 field=say answer=None text='For the biggest quotient, make the top as large and the bottom as small as possible.'
   step3 field=pre answer=1.95 text='Lower bound of b = 2.0 − 0.05 ='
   step4 field=pre answer=3.1 text='6.05 ÷ 1.95 = (2 d.p.)'

gold[4] Q: Simplify \(\frac{6 + \sqrt{8}}{2}\)
   step0 field=pre answer=2 text='Simplify √8: 8 = 4 × 2, so √8 = 2√2. The coefficient is'
   step1 field=say answer=None text='So the top is 6 + 2√2, all over 2.'
   step2 field=pre answer=3 text='Divide the first term: 6 ÷ 2 ='
   step3 field=pre answer=1 text='Divide the surd term: 2√2 ÷ 2 ='

### board=maths-eduqas
gold[2] Q: 8.7 cm5.3 cmArea = ?Diagram not drawn accuratelyThe sides of a rectangle are \(5.3\) cm an
   step0 field=say answer=None text='Both sides are to 1 d.p., so each has a half unit of 0.05. The smallest area uses the smal'
   step1 field=pre answer=5.25 text='Lower bound of 5.3 = 5.3 − 0.05 ='
   step2 field=pre answer=8.65 text='Lower bound of 8.7 = 8.7 − 0.05 ='
   step3 field=pre answer=45.41 text='Smallest area = 5.25 × 8.65 = 45.4125, to 4 s.f. ='
   step4 field=pre answer=46.11 text='For comparison, the rounded-value area 5.3 × 8.7 ='

gold[4] Q: Simplify \(\dfrac{16^{\frac{3}{4}}}{2^3}\).
   step0 field=say answer=None text='Work the top first: \\(16^{3/4}\\) means the fourth root of 16, then cubed.'
   step1 field=pre answer=16 text='Fourth root: which number to the power 4 gives 16? 2 × 2 × 2 × 2 ='
   step2 field=pre answer=8 text='So 16^(1/4) = 2. Now cube it: 2³ ='
   step3 field=pre answer=1 text='The bottom is 2³ = 8. Divide: 8 ÷ 8 ='
   step4 field=pre answer=8 text='Check the top as a power of 2: 16^(3/4) = 2³ = 8, and bottom 2³ ='
