# apply-pack: ratio-proportion__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[0] | Express k in terms of a. Give the numerator when k = ?/a. | fix: Reword to: 'y ∝ x². When x = a, y = 5a. This gives k = 5/a. What is the number on top of the fraction (the numerator)?'
- [low] silver[4] | Check: if y really ÷ 9, then 4 × 9 = [box=36, NO label] | fix: Rewrite as: 'Check: if y really was divided by 9, then 4 × 9 = ___'.
- [low] gold[0] | x = ∛8 = [box=2, NO label] | fix: Name the operation: 'x = cube root of 8 (∛8) = ___'.
- [low] bronze[3] | Check with k: k = 18 ÷ 3² = 2, then 2 × 6² = 2 × 36 = [box=72, NO label] | fix: Split into two shorter asks, or simplify to just the final verification: 'Check: k × 6² = 2 × 36 = ___'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[3] Q: \(y = 2x^3\). Find \(y\) when \(x = 3\).
   step0 field=say answer=None text='y = 2x³, so k = 2. Put x = 3 in.'
   step1 field=pre answer=27 text='Cube x: 3³ = 3 × 3 × 3 ='
   step2 field=pre answer=54 text='y = 2 × 27 ='
   step3 field=pre answer=27 text='Check: 54 ÷ 2 ='
   step4 field=pre answer=3 text='27 is 3³; the cube root of 27 is'

gold[0] Q: \(y \propto x^2\). When \(x = a\), \(y = 5a\). Express \(k\) in terms of \(a\). Give the n
   step0 field=say answer=None text='Put x = a and y = 5a into y = kx²: 5a = k × a².'
   step1 field=pre answer=2 text='The power of a in a² is'
   step2 field=pre answer=-1 text='Remember a on its own means a to the power 1. Divide by a²: k = 5a ÷ a². Subtract the powe'
   step3 field=pre answer=5 text='So k = 5/a. The number on top (numerator) is'
   step4 field=pre answer=10 text='Check with a = 2: k = 5 ÷ 2 = 2.5, and k × a² = 2.5 × 2² = 2.5 × 4 ='

silver[4] Q: \(y \propto \frac{1}{x}\). When \(x = 4\), \(y = 9\). Find \(x\) when \(y = 12\).
   step0 field=say answer=None text='Inverse: y = k/x, so k = x × y. Find k from the first pair.'
   step1 field=pre answer=36 text='k = 4 × 9 ='
   step2 field=pre answer=3 text='Now y = 12: x = k ÷ y = 36 ÷ 12 ='
   step3 field=pre answer=36 text='Check: 3 × 12 ='
   step4 field=pre answer=36 text='First pair: 4 × 9 ='

### board=maths-edexcel
bronze[3] Q: \(y \propto \sqrt{x}\). When \(x = 16\), \(y = 20\). Find \(k\).
   step0 field=say answer=None text='Turn the proportion into an equation. \\(y \\propto \\sqrt{x}\\) means \\(y = k\\sqrt{x}\\).'
   step1 field=pre answer=4 text='Square-root the known x first: √16 ='
   step2 field=pre answer=5 text='Now 20 = k × 4, so k = 20 ÷ 4 ='
   step3 field=pre answer=20 text='Check: k × √16 = 5 × 4 ='

gold[0] Q: \(y \propto \frac{1}{x^2}\). When \(x = 3\), \(y = 4\). Find \(y\) when \(x = 6\).
   step0 field=say answer=None text='Inverse square: \\(y = \\frac{k}{x^2}\\), so k = y × x². Square the known x.'
   step1 field=pre answer=9 text='3² ='
   step2 field=pre answer=36 text='k = 4 × 9 ='
   step3 field=pre answer=36 text='6² ='
   step4 field=pre answer=1 text='y = 36 ÷ 36 ='
   step5 field=pre answer=36 text='Check: 1 × 6² = 1 × 36 ='

silver[4] Q: \(y \propto x^3\). When \(x = 2\), \(y = 40\). Find \(y\) when \(x = 3\).
   step0 field=say answer=None text='Cube proportion: \\(y = kx^3\\). Cube the known x.'
   step1 field=pre answer=8 text='2³ ='
   step2 field=pre answer=5 text='k = 40 ÷ 8 ='
   step3 field=pre answer=27 text='3³ ='
   step4 field=pre answer=135 text='y = 5 × 27 ='
   step5 field=pre answer=40 text='Check on the first pair: 5 × 2³ = 5 × 8 ='

### board=maths-ocr
bronze[3] Q: \(y \propto x^2\). When \(x\) doubles (from 3 to 6), \(y\) was 18. What is \(y\) now?
   step0 field=say answer=None text='x goes from 3 to 6. Work out how many times bigger x is.'
   step1 field=pre answer=2 text='6 ÷ 3 ='
   step2 field=pre answer=4 text='y ∝ x², so y multiplies by 2² ='
   step3 field=pre answer=72 text='New y = 18 × 4 ='
   step4 field=pre answer=72 text='Check with k: k = 18 ÷ 3² = 2, then 2 × 6² = 2 × 36 ='

gold[0] Q: \(y \propto x^3\). When \(x = 3\), \(y = 54\). Find \(x\) when \(y = 16\).
   step0 field=say answer=None text='y = k×x³. Use x = 3, y = 54 to find k first.'
   step1 field=pre answer=27 text='3³ ='
   step2 field=pre answer=2 text='k = 54 ÷ 27 ='
   step3 field=pre answer=8 text='Reverse: 16 = 2×x³, so x³ = 16 ÷ 2 ='
   step4 field=pre answer=2 text='x = ∛8 ='
   step5 field=pre answer=16 text='Check: 2 × 2³ = 2 × 8 ='

silver[4] Q: \(y \propto \frac{1}{x^2}\). When \(x\) triples, \(y\) was 36. Find the new \(y\).
   step0 field=say answer=None text='Inverse square: y = k ÷ x². See how x changes.'
   step1 field=pre answer=3 text='x triples, so the multiplier is'
   step2 field=pre answer=9 text='Inverse square, so y divides by 3² ='
   step3 field=pre answer=4 text='New y = 36 ÷ 9 ='
   step4 field=pre answer=36 text='Check: if y really ÷ 9, then 4 × 9 ='

### board=maths-eduqas
bronze[3] Q: \(y \propto x^2\). When \(x = 4\), \(y = 48\). Find \(y\) when \(x = 6\).
   step0 field=say answer=None text='y = kx². Find k from x = 4, y = 48.'
   step1 field=pre answer=16 text='4² ='
   step2 field=pre answer=3 text='k = 48 ÷ 16 ='
   step3 field=pre answer=108 text='Now x = 6: 6² = 36, y = 3 × 36 ='
   step4 field=pre answer=3 text='Check: 108 ÷ 36 ='

gold[0] Q: \(y \propto x^2\). When \(x = a\), \(y = b\). Find \(y\) in terms of \(b\) when \(x = 3a\)

silver[4] Q: \(y \propto x^2\). When \(x\) is tripled, \(y\) is multiplied by:
   step0 field=say answer=None text='y = kx². If x triples, x² is multiplied by 3².'
   step1 field=pre answer=9 text='3² ='
   step2 field=pre answer=4 text='Take k = 1 and x = 2: y = 1 × 2² ='
   step3 field=pre answer=36 text='Triple x to 6: y = 1 × 6² ='
   step4 field=pre answer=9 text='36 ÷ 4 ='
