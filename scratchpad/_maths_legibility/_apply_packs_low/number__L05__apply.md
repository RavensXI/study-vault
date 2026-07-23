# apply-pack: number__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[0] | Check by building up: 10% is 8, so 20% is 16 and 5% is 4; 16 + 4 = [box=20] | fix: Trim to just the values needed for the sum, e.g. 'Another way: 20% is 16 and 5% is 4. Add them: 16 + 4 ='.
- [low] gold[2] | Check with the power: 0.85 × 0.85 = [box=0.7225, NO label] | fix: Reword to name the operation, e.g. 'Check by squaring the multiplier: 0.85 × 0.85 ='

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: Find \(25\%\) of \(360\)
   step0 field=say answer=None text='We are finding \\(25\\%\\) of \\(360\\).'
   step1 field=pre answer=36 text='Find 10% of 360 by dividing by 10.'
   step2 field=pre answer=18 text='Find 5% by halving that 10%.'
   step3 field=pre answer=90 text='25% is 10% + 10% + 5%. Add 36 + 36 + 18.'

gold[2] Q: \(\pounds5000\) is invested at \(3\%\) compound interest per year. Find the value after \(
   step0 field=say answer=None text='\\(\\pounds5000\\) grows at \\(3\\%\\) compound interest for \\(2\\) years.'
   step1 field=pre answer=5150 text='Each year multiplies by 1.03. After year 1, work out 5000 × 1.03.'
   step2 field=pre answer=5304.5 text='Apply another year: multiply 5150 by 1.03.'
   step3 field=pre answer=5304.5 text='Write the value after 2 years in pounds.'

### board=maths-edexcel
bronze[0] Q: Find 25% of 80
   step0 field=say answer=None text='25% means a quarter, which is half of a half. Set it up.'
   step1 field=pre answer=40 text='Half of 80 ='
   step2 field=pre answer=20 text='Halve again for a quarter: 40 ÷ 2 ='
   step3 field=pre answer=20 text='Check by building up: 10% is 8, so 20% is 16 and 5% is 4; 16 + 4 ='

gold[2] Q: A shop increases prices by 20% then has a 20% sale. An item now costs £48. Find the origin
   step0 field=say answer=None text='Two changes in a row: first +20% (× 1.2), then 20% off (× 0.8). Combine them.'
   step1 field=pre answer=0.96 text='Combined multiplier: 1.2 × 0.8 ='
   step2 field=pre answer=50 text='Reverse means divide: 48 ÷ 0.96 ='
   step3 field=pre answer=60 text='Check forwards: 50 × 1.2 ='
   step4 field=pre answer=48 text='Then the 20% sale: 60 × 0.8 ='

### board=maths-ocr
bronze[0] Q: Find 25% of 60
   step0 field=pre answer=0.25 text='25 ÷ 100 ='
   step1 field=pre answer=15 text='60 × 0.25 ='
   step2 field=pre answer=25 text='Check it really is 25%: 15 ÷ 60 × 100 ='

gold[2] Q: A car depreciates by 15% each year. It cost £12 000. What is its value after 2 years? (to 
   step0 field=pre answer=0.85 text='The yearly multiplier is 0.'
   step1 field=pre answer=10200 text='12000 × 0.85 ='
   step2 field=pre answer=8670 text='10200 × 0.85 ='
   step3 field=pre answer=0.7225 text='Check with the power: 0.85 × 0.85 ='

### board=maths-eduqas
bronze[0] Q: Find \(25\%\) of \(80\).
   step0 field=say answer=None text='25% is one quarter. A quarter means halve, then halve again.'
   step1 field=pre answer=40 text='Half of 80 = 80 ÷ 2 ='
   step2 field=pre answer=20 text='Half again (that is a quarter): 40 ÷ 2 ='
   step3 field=pre answer=80 text='Check: four quarters rebuild the whole, 4 × 20 ='

gold[2] Q: A car depreciates by \(20\%\) per year. It is now worth \(£12\,800\). Find its value 3 yea
   step0 field=say answer=None text='Losing 20% each year multiplies by 0.8. Over 3 years that is 0.8 × 0.8 × 0.8.'
   step1 field=pre answer=0.512 text='0.8 × 0.8 × 0.8 ='
   step2 field=pre answer=25000 text='The £12,800 is the old value × 0.512. Reverse by dividing: 12800 ÷ 0.512 = £'
   step3 field=pre answer=12800 text='Check forwards: 25000 × 0.512 = £'
