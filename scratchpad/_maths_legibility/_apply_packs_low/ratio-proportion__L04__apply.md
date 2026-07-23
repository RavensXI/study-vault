# apply-pack: ratio-proportion__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[1] intro (also bronze[0]/[2]/[3]/[6], silver[2]) | intro: Direct proportion: more litre, more km. Find the value of ONE first. | fix: Pluralise: 'Direct proportion: more litres, more km.'
- [low] bronze[1] | \(y \propto x\). When \(x = 5\), \(y = 15\). Find \(y\) when \(x = 9\). | fix: Gloss the symbol on first symbolic use, e.g. 'y ∝ x (y is proportional to x)'.
- [low] silver[6] | A spring stretches 4.5 cm with a 6 N force. How much with 10 N? (Hooke's Law: ex | fix: Name the quantity: 'How much does it stretch with 10 N?'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[1] Q: 4 pens cost £6. How much do 10 pens cost?
   step0 field=pre answer=1.5 text='6 ÷ 4 ='
   step1 field=pre answer=15 text='1.5 × 10 ='
   step2 field=pre answer=1.5 text='15 ÷ 10 ='

silver[6] Q: A recipe for 8 servings needs 500 ml of milk. How much for 12 servings?
   step0 field=pre answer=62.5 text='500 ÷ 8 ='
   step1 field=pre answer=750 text='62.5 × 12 ='
   step2 field=pre answer=62.5 text='750 ÷ 12 ='

### board=maths-edexcel
bronze[1] Q: A car uses 8 litres of fuel to travel 96 km. How far can it travel on 5 litres?
   step0 field=say answer=None text='Direct proportion: more litre, more km. Find the value of ONE first.'
   step1 field=pre answer=12 text='One litre: 96 ÷ 8 ='
   step2 field=pre answer=60 text='5 litre: 12 × 5 ='
   step3 field=pre answer=12 text='Check: 60 ÷ 5 ='

silver[6] Q: 12 workers finish a job in 8 days. How many workers are needed to finish it in 6 days?
   step0 field=say answer=None text='Inverse proportion: more days, LESS workers. The total stays fixed, so find it.'
   step1 field=pre answer=96 text='Total = 12 × 8 ='
   step2 field=pre answer=16 text='6 days: 96 ÷ 6 ='
   step3 field=pre answer=96 text='Check: 6 × 16 ='

### board=maths-ocr
bronze[1] Q: \(y \propto x\). When \(x = 3\), \(y = 15\). Find \(k\).
   step0 field=say answer=None text='Direct means \\(y = kx\\), so the constant is \\(k = y \\div x\\).'
   step1 field=pre answer=5 text='k = 15 ÷ 3 ='
   step2 field=pre answer=15 text='Check: 5 × 3 ='
   step3 field=pre answer=5 text='And at x = 1: 5 × 1 ='

silver[6] Q: \(y \propto \frac{1}{x}\). When \(x = 2\), \(y = 15\). Find \(x\) when \(y = 6\).
   step0 field=say answer=None text='Inverse means \\(y = \\frac{k}{x}\\), so k is the product.'
   step1 field=pre answer=30 text='k = 2 × 15 ='
   step2 field=pre answer=5 text='x = 30 ÷ 6 ='
   step3 field=pre answer=30 text='Check: 5 × 6 ='

### board=maths-eduqas
bronze[1] Q: \(y \propto x\). When \(x = 5\), \(y = 15\). Find \(y\) when \(x = 9\).

silver[6] Q: A spring stretches 4.5 cm with a 6 N force. How much with 10 N? (Hooke's Law: extension \(
