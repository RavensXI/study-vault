# apply-pack: ratio-proportion__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[2] (box=7908.98) | Apply for 5 years: 12000 × 0.92⁵ = [box=7908.98, NO label] | fix: Either add a short year-by-year build before this step, or show the expansion, e.g. '0.92⁵ = 0.6591 (to 4 dp)', so the power step is demonstrated rather than as
- [low] gold[3] | Cube root of 0.729 = [box=0.9, NO label] | fix: Add a one-line scaffold naming the calculator action, e.g. 'Use the cube-root button (∛) on your calculator: ∛0.729 =', or confirm with '0.9 × 0.9 × 0.9 = 0.729

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: A population decreases by 8% each year from 12000. Find the population after 5 years to th
   step0 field=say answer=None text='A fall of 8% each year means keeping 92% each year for five years.'
   step1 field=pre answer=0.92 text='Multiplier: 1 − 0.08 ='
   step2 field=pre answer=7908.98 text='Apply for 5 years: 12000 × 0.92⁵ ='
   step3 field=pre answer=7909 text='To the nearest whole number:'
   step4 field=pre answer=8596.72 text='Check by reversing one year: 7908.98 ÷ 0.92 ='

gold[3] Q: An item is increased by 10% then decreased by 10%. The final price is £495. What was the o
   step0 field=say answer=None text='A 10% rise then a 10% fall do NOT cancel. Combine the two multipliers first.'
   step1 field=pre answer=1.1 text='Rise multiplier: 1 + 0.1 ='
   step2 field=pre answer=0.9 text='Fall multiplier: 1 − 0.1 ='
   step3 field=pre answer=0.99 text='Combined: 1.1 × 0.9 ='
   step4 field=pre answer=500 text='Reverse: 495 ÷ 0.99 ='
   step5 field=pre answer=495 text='Check forwards: 500 × 0.99 ='

### board=maths-edexcel
gold[2] Q: After 2 years of 5% compound interest, an investment is worth £5,512.50. What was the orig
   step0 field=pre answer=1.05 text='Multiplier = 1 + 0.05 ='
   step1 field=pre answer=1.1025 text='1.05² ='
   step2 field=pre answer=5000 text='5512.50 ÷ 1.1025 = £'
   step3 field=pre answer=5512.5 text='5000 × 1.1025 = £'

gold[3] Q: A car was worth \(£16{,}000\). After 3 years at \(x\%\) depreciation it is worth \(£11{,}6
   step0 field=pre answer=0.729 text='11664 ÷ 16000 ='
   step1 field=pre answer=0.9 text='Cube root of 0.729 ='
   step2 field=pre answer=0.1 text='1 − 0.9 ='
   step3 field=pre answer=10 text='As a percentage: 0.1 × 100 ='
   step4 field=pre answer=11664 text='16000 × 0.9 × 0.9 × 0.9 = £'

### board=maths-ocr
gold[2] Q: After 2 years of 5% compound interest, an account has £1102.50. Find the original amount.
   step0 field=pre answer=1.05 text='Multiplier = 1 + 0.05 ='
   step1 field=pre answer=1.1025 text='1.05² ='
   step2 field=pre answer=1000 text='1102.50 ÷ 1.1025 = £'
   step3 field=pre answer=1102.5 text='Check: 1000 × 1.1025 = £'

gold[3] Q: A population of 8000 decreases by 3% per year. After how many whole years is it first belo
   step0 field=pre answer=0.97 text='Multiplier for a 3% decrease = 1 − 0.03 ='
   step1 field=pre answer=7082 text='Each year multiplies by 0.97, so after 4 years you multiply by 0.97 four times: 8000 × 0.9'
   step2 field=pre answer=6870 text='After 5 years: 8000 × 0.97⁵ ='
   step3 field=pre answer=5 text='The first whole year below 7000 is year'

### board=maths-eduqas
gold[2] Q: \(\pounds 2000\) is invested at 6% compound interest. After how many years does it exceed 

gold[3] Q: A painting increases in value by 5% each year. It is now worth \(\pounds 12\,000\). What w
