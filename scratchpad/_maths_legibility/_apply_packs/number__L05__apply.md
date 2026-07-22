# apply-pack: number__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[4] | 1.05 to the power 14 = (2 d.p.) [box=1.98, NO label] | fix: Add a priming line, e.g. 'to the power 14 means multiply 1.05 by itself 14 times — use the x^y key on your calculator', or scaffold the computation.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[4] Q: After two successive discounts of \(10\%\) and \(20\%\), an item costs \(\pounds288\). Fin
   step0 field=say answer=None text='After discounts of \\(10\\%\\) then \\(20\\%\\), an item costs \\(\\pounds288\\). We want the origi'
   step1 field=pre answer=0.72 text='A 10% discount is ×0.9 and a 20% discount is ×0.8. Multiply them: 0.9 × 0.8.'
   step2 field=pre answer=4 text='So £288 is 72% of the original. Find 1% by dividing 288 by 72.'
   step3 field=pre answer=400 text='The original is 100%. Multiply 1% by 100.'
   step4 field=pre answer=400 text='Write the original price in pounds.'

### board=maths-edexcel
gold[4] Q: A train fare goes up by 3% to £45.26. Find the original fare to the nearest penny.
   step0 field=say answer=None text='Reverse percentage giving a decimal answer. £45.26 is after a 3% rise, so it is 103% of th'
   step1 field=pre answer=1.03 text='Multiplier for 3% up: 103 ÷ 100 ='
   step2 field=pre answer=43.94 text='Reverse means divide, to 2 d.p.: 45.26 ÷ 1.03 ='
   step3 field=pre answer=45.26 text='Check forwards, to 2 d.p.: 43.94 × 1.03 ='

### board=maths-ocr
gold[4] Q: A population grows by 5% each year. After how many whole years does it first exceed double
   step0 field=pre answer=1.98 text='1.05 to the power 14 = (2 d.p.)'
   step1 field=pre answer=2.08 text='1.05 to the power 15 = (2 d.p.)'
   step2 field=pre answer=15 text='The first whole year over double is year'

### board=maths-eduqas
gold[4] Q: \(£5000\) earns \(2.5\%\) compound interest. After how many years does it first exceed \(£
   step0 field=say answer=None text='Multiply by 1.025 each year and watch for the first time you pass £5500.'
   step1 field=pre answer=5125 text='After year 1: 5000 × 1.025 = £'
   step2 field=pre answer=5253.125 text='After year 2: 5125 × 1.025 = £'
   step3 field=pre answer=5519.06 text='Year 3 gives £5384.45 (still under 5500). After year 4: 5384.45 × 1.025 = £'
   step4 field=pre answer=4 text='5519.06 is the first value above 5500, so the number of years is'
