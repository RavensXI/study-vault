# apply-pack: ratio-proportion__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[4] | On £100: after 20% off £80, then 10% off £80 leaves £72, so 100 − 72 = | fix: Break it into short steps: 'Start with £100. 20% off leaves £80. 10% off the £80 leaves £72. The overall decrease is 100 − 72 ='.
- [medium] gold[3] | After 4 years: 8000 × 0.97⁴ = [box=7082, NO label] | fix: Replace 'Test one year at a time' with a line that builds the power, e.g. 'Each year multiplies by 0.97, so after 4 years you multiply by 0.97 four times: that 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[3] Q: An item is increased by 10% then decreased by 10%. The final price is £495. What was the o
   step0 field=say answer=None text='A 10% rise then a 10% fall do NOT cancel. Combine the two multipliers first.'
   step1 field=pre answer=1.1 text='Rise multiplier: 1 + 0.1 ='
   step2 field=pre answer=0.9 text='Fall multiplier: 1 − 0.1 ='
   step3 field=pre answer=0.99 text='Combined: 1.1 × 0.9 ='
   step4 field=pre answer=500 text='Reverse: 495 ÷ 0.99 ='
   step5 field=pre answer=495 text='Check forwards: 500 × 0.99 ='

gold[4] Q: A savings account pays 3.5% compound interest. £6000 is invested. What is the interest ear
   step0 field=say answer=None text='Grow the money by compounding, then take the £6000 back off to leave just the interest.'
   step1 field=pre answer=1.035 text='Multiplier: 1 + 0.035 ='
   step2 field=pre answer=6885.14 text='Total after 4 years: 6000 × 1.035⁴ ='
   step3 field=pre answer=885.14 text='Interest only: 6885.14 − 6000 ='
   step4 field=pre answer=6885.14 text='Check: 6000 + 885.14 ='

### board=maths-edexcel
gold[3] Q: A car was worth \(£16{,}000\). After 3 years at \(x\%\) depreciation it is worth \(£11{,}6
   step0 field=pre answer=0.729 text='11664 ÷ 16000 ='
   step1 field=pre answer=0.9 text='Cube root of 0.729 ='
   step2 field=pre answer=0.1 text='1 − 0.9 ='
   step3 field=pre answer=10 text='As a percentage: 0.1 × 100 ='
   step4 field=pre answer=11664 text='16000 × 0.9 × 0.9 × 0.9 = £'

gold[4] Q: A sale offers 20% off, then a further 10% off the sale price. What is the overall percenta
   step0 field=pre answer=0.8 text='Multiplier = 1 − 0.20 ='
   step1 field=pre answer=0.9 text='Multiplier = 1 − 0.10 ='
   step2 field=pre answer=0.72 text='0.8 × 0.9 ='
   step3 field=pre answer=0.28 text='1 − 0.72 ='
   step4 field=pre answer=28 text='As a percentage: 0.28 × 100 ='
   step5 field=pre answer=28 text='On £100: after 20% off £80, then 10% off £80 leaves £72, so 100 − 72 ='

### board=maths-ocr
gold[3] Q: A population of 8000 decreases by 3% per year. After how many whole years is it first belo
   step0 field=pre answer=0.97 text='Multiplier for a 3% decrease = 1 − 0.03 ='
   step1 field=pre answer=7082 text='After 4 years: 8000 × 0.97⁴ ='
   step2 field=pre answer=6870 text='After 5 years: 8000 × 0.97⁵ ='
   step3 field=pre answer=5 text='The first whole year below 7000 is year'

gold[4] Q: £500 earns 6% compound interest. How much interest (not total) after 2 years? To 2 d.p.
   step0 field=pre answer=1.06 text='Multiplier = 1 + 0.06 ='
   step1 field=pre answer=1.1236 text='1.06² ='
   step2 field=pre answer=561.8 text='Total: 500 × 1.1236 = £'
   step3 field=pre answer=61.8 text='Interest only: 561.80 − 500 = £'

### board=maths-eduqas
gold[3] Q: A painting increases in value by 5% each year. It is now worth \(\pounds 12\,000\). What w

gold[4] Q: A town's population decreases by 3% each year from 80 000. What is the population after 5 
