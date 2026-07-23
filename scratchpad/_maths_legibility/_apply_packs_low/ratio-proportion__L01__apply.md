# apply-pack: ratio-proportion__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[0] | intro: The shared letter is b. In a : b it is 4; in b : c it is 2. Scale b : c s | fix: Break it up, e.g. 'b is the shared letter. In a : b, b = 4. In b : c, b = 2. We want b to be 4 in both. What do we multiply 2 by to get 4?'
- [low] gold[2] | Real length in cm: 4.5 m = [box=450, NO label] | fix: State the factor in the intro or step, e.g. add 'There are 100 cm in 1 m' or rewrite the step as '4.5 × 100 ='.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: The ratio \(a : b = 3 : 4\) and \(b : c = 2 : 5\). Find \(a : b : c\). What is \(c\)?
   step0 field=pre answer=2 text='4 ÷ 2 ='
   step1 field=pre answer=10 text='5 × 2 ='
   step2 field=pre answer=2 text='10 ÷ 5 ='

gold[2] Q: Share £200 in the ratio \(1 : 2 : 5\). What fraction of the total does the middle share re
   step0 field=pre answer=8 text='1 + 2 + 5 ='
   step1 field=pre answer=2 text='Numerator ='
   step2 field=pre answer=1 text='2 ÷ 2 ='
   step3 field=pre answer=4 text='8 ÷ 2 ='

### board=maths-edexcel
gold[0] Q: Ali and Bob share money in the ratio \(5 : 3\). Ali gets £40 more than Bob. How much does 
   step0 field=say answer=None text='The £40 is the difference between the shares, not the total. Work in parts.'
   step1 field=pre answer=2 text='Difference in parts: 5 − 3 ='
   step2 field=pre answer=20 text='That 2-part gap is £40, so one part = 40 ÷ 2 = £'
   step3 field=pre answer=60 text='3 × 20 = £'
   step4 field=pre answer=40 text='Check the gap: Ali is 5 × 20 = £100, so 100 − 60 = £'

gold[2] Q: A model car is built to a scale of \(1 : 18\). The real car is 4.5 m long. What is the mod
   step0 field=say answer=None text='Scale 1 : 18 means the real car is 18 times the model. Work in the same units: centimetres'
   step1 field=pre answer=450 text='Real length in cm: 4.5 m ='
   step2 field=pre answer=25 text='450 ÷ 18 ='
   step3 field=pre answer=450 text='Check by scaling up: 25 × 18 ='

### board=maths-ocr
gold[0] Q: Amy and Ben share money 2 : 5. Ben gets £36 more than Amy. What is the total?
   step0 field=say answer=None text='Ben has 5 parts, Amy has 2. The gap between them is worth £36.'
   step1 field=pre answer=3 text='Gap in parts: 5 − 2 ='
   step2 field=pre answer=12 text='One part = £36 ÷ 3 = £'
   step3 field=pre answer=7 text='Total parts = 2 + 5 ='
   step4 field=pre answer=84 text='Total = 7 × £12 = £'
   step5 field=pre answer=36 text='Check: Amy 2×12 = 24, Ben 5×12 = 60, gap 60 − 24 = £'

gold[2] Q: Pack A: 750 g for £2.70. Pack B: 1.2 kg for £4.20. Which is better value? Enter A=1, B=2.
   step0 field=pre answer=1200 text='Pack B in grams: 1.2 × 1000 ='
   step1 field=pre answer=0.36 text='Pack A pence per gram. £2.70 = 270p, so 270 ÷ 750 ='
   step2 field=pre answer=0.35 text='Pack B pence per gram. £4.20 = 420p, so 420 ÷ 1200 ='
   step3 field=pre answer=2 text='0.35p is less than 0.36p, so B is cheaper per gram. Enter B as'

### board=maths-eduqas
gold[0] Q: Ali, Ben and Cal share \(\pounds360\) in the ratio \(2 : 3 : 4\). How much does Ben receiv

gold[2] Q: The ratio of cats to dogs is \(7 : 4\). There are 18 more cats than dogs. How many animals
