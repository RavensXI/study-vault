# apply-pack: ratio-proportion__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[1] | intro: Red is 3 parts and equals 2 litres, so one part is 2 ÷ 3 litres. Blue is  | fix: Split into short lines and isolate the ask, e.g. 'One red part = 2 ÷ 3 litres. Blue is 7 parts, so the top of the fraction is 7 × 2. Work out 7 × 2.'
- [medium] gold[1] | intro: So blue = 14/3 litres. Check the ratio: red is 2 = 6/3 and blue is 14/3,  | fix: State the action: 'Simplify 6 : 14 by dividing both parts by 2. Second part: 14 ÷ 2 =' (ideally also show 6 ÷ 2 = 3 so the check is complete).
- [medium] gold[2] | Pack A pence per gram: 270 ÷ 750 = [box=0.36, label:'(a decimal)'] | fix: Add the conversion inline, e.g. '£2.70 = 270p, so 270 ÷ 750 =' and '£4.20 = 420p, so 420 ÷ 1200 =', or insert a prior step converting each price to pence.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[1] Q: Purple paint is mixed using red and blue in the ratio \(3 : 7\). I have 2 litres of red. H
   step0 field=pre answer=14 text='7 × 2 ='
   step1 field=pre answer=3 text='The denominator is'
   step2 field=pre answer=7 text='14 ÷ 2 ='

gold[2] Q: Share £200 in the ratio \(1 : 2 : 5\). What fraction of the total does the middle share re
   step0 field=pre answer=8 text='1 + 2 + 5 ='
   step1 field=pre answer=2 text='Numerator ='
   step2 field=pre answer=1 text='2 ÷ 2 ='
   step3 field=pre answer=4 text='8 ÷ 2 ='

### board=maths-edexcel
gold[1] Q: Three friends share a prize in the ratio \(2 : 5 : 8\). The smallest share is £90. What is
   step0 field=say answer=None text='The £90 is the smallest share, worth 2 parts. Find one part first.'
   step1 field=pre answer=45 text='One part = 90 ÷ 2 = £'
   step2 field=pre answer=15 text='Total parts = 2 + 5 + 8 ='
   step3 field=pre answer=675 text='15 × 45 = £'
   step4 field=pre answer=90 text='Check the smallest share: 2 × 45 = £'

gold[2] Q: A model car is built to a scale of \(1 : 18\). The real car is 4.5 m long. What is the mod
   step0 field=say answer=None text='Scale 1 : 18 means the real car is 18 times the model. Work in the same units: centimetres'
   step1 field=pre answer=450 text='Real length in cm: 4.5 m ='
   step2 field=pre answer=25 text='450 ÷ 18 ='
   step3 field=pre answer=450 text='Check by scaling up: 25 × 18 ='

### board=maths-ocr
gold[1] Q: The ratio a : b = 2 : 3 and b : c = 4 : 5. Find a : c. Give the first number in simplest f
   step0 field=say answer=None text='Make b the same in both ratios. b is 3 in the first and 4 in the second; the common value '
   step1 field=pre answer=4 text='Scale a : b so b = 12: multiply by 12 ÷ 3 ='
   step2 field=pre answer=8 text='Then a = 2 × 4 ='
   step3 field=pre answer=3 text='Scale b : c so b = 12: multiply by 12 ÷ 4 ='
   step4 field=pre answer=15 text='Then c = 5 × 3 ='
   step5 field=pre answer=8 text='So a : c = 8 : 15. The first number is'

gold[2] Q: Pack A: 750 g for £2.70. Pack B: 1.2 kg for £4.20. Which is better value? Enter A=1, B=2.
   step0 field=pre answer=1200 text='Pack B in grams: 1.2 × 1000 ='
   step1 field=pre answer=0.36 text='Pack A pence per gram: 270 ÷ 750 ='
   step2 field=pre answer=0.35 text='Pack B pence per gram: 420 ÷ 1200 ='
   step3 field=pre answer=2 text='0.35p is less than 0.36p, so B is cheaper per gram. Enter B as'

### board=maths-eduqas
gold[1] Q: Amy and Beth share money in the ratio \(5 : 3\). Amy gets \(\pounds40\) more than Beth. Ho

gold[2] Q: The ratio of cats to dogs is \(7 : 4\). There are 18 more cats than dogs. How many animals
