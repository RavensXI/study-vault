# apply-pack: ratio-proportion__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[0] | Divide by a²: k = 5a ÷ a². Subtract powers, 1 − 2, so a is left to the power [bo | fix: Add a line before it: 'Remember a on its own means a to the power 1. Dividing means subtracting the powers: 1 − 2.'
- [medium] silver[5], gold[0], gold[4] | intro: "So the constant is k." | fix: Replace with a concrete instruction, e.g. "Now find k by multiplying y by that squared x." (silver[5]: "Multiply y (5) by 4 to get k."; gold[0]: "Multiply y (4)
- [medium] silver[4] | x triples, a multiplier of [box=3, NO label] | fix: Rephrase as a complete sentence: 'x triples, so the multiplier is ___'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: \(y \propto x^2\). When \(x = a\), \(y = 5a\). Express \(k\) in terms of \(a\). Give the n
   step0 field=say answer=None text='Put x = a and y = 5a into y = kx²: 5a = k × a².'
   step1 field=pre answer=2 text='The power of a in a² is'
   step2 field=pre answer=-1 text='Divide by a²: k = 5a ÷ a². Subtract powers, 1 − 2, so a is left to the power'
   step3 field=pre answer=5 text='So k = 5/a. The number on top (numerator) is'
   step4 field=pre answer=10 text='Check with a = 2: k = 5 ÷ 2 = 2.5, and k × a² = 2.5 × 2² = 2.5 × 4 ='

silver[4] Q: \(y \propto \frac{1}{x}\). When \(x = 4\), \(y = 9\). Find \(x\) when \(y = 12\).
   step0 field=say answer=None text='Inverse: y = k/x, so k = x × y. Find k from the first pair.'
   step1 field=pre answer=36 text='k = 4 × 9 ='
   step2 field=pre answer=3 text='Now y = 12: x = k ÷ y = 36 ÷ 12 ='
   step3 field=pre answer=36 text='Check: 3 × 12 ='
   step4 field=pre answer=36 text='First pair: 4 × 9 ='

silver[5] Q: \(y \propto x^2\). When \(x = 4\), \(y = 48\). Find \(x\) when \(y = 108\).
   step0 field=say answer=None text='Direct square: y = kx². Find k from x = 4, y = 48.'
   step1 field=pre answer=16 text='4² ='
   step2 field=pre answer=3 text='k = 48 ÷ 16 ='
   step3 field=pre answer=36 text='Now 108 = 3x², so x² = 108 ÷ 3 ='
   step4 field=pre answer=6 text='Take the square root: x = √36 ='
   step5 field=pre answer=108 text='Check: 3 × 6² = 3 × 36 ='

### board=maths-edexcel
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

silver[5] Q: \(y \propto \frac{1}{x^2}\). When \(x = 2\), \(y = 5\). Find \(y\) when \(x = 5\).
   step0 field=say answer=None text='Inverse square: \\(y = \\frac{k}{x^2}\\), so k = y × x². Square the known x.'
   step1 field=pre answer=4 text='2² ='
   step2 field=pre answer=20 text='k = 5 × 4 ='
   step3 field=pre answer=25 text='5² ='
   step4 field=pre answer=0.8 text='y = 20 ÷ 25 ='
   step5 field=pre answer=20 text='Check: 0.8 × 5² = 0.8 × 25 ='

### board=maths-ocr
gold[0] Q: \(y \propto x^3\). When \(x = 3\), \(y = 54\). Find \(x\) when \(y = 16\).
   step0 field=say answer=None text='y = k×x³. Use x = 3, y = 54 to find k first.'
   step1 field=pre answer=27 text='3³ ='
   step2 field=pre answer=2 text='k = 54 ÷ 27 ='
   step3 field=pre answer=8 text='Reverse: 16 = 2×x³, so x³ = 16 ÷ 2 ='
   step4 field=pre answer=2 text='x = ∛8 ='
   step5 field=pre answer=16 text='Check: 2 × 2³ = 2 × 8 ='

silver[4] Q: \(y \propto \frac{1}{x^2}\). When \(x\) triples, \(y\) was 36. Find the new \(y\).
   step0 field=say answer=None text='Inverse square: y = k ÷ x². See how x changes.'
   step1 field=pre answer=3 text='x triples, a multiplier of'
   step2 field=pre answer=9 text='Inverse square, so y divides by 3² ='
   step3 field=pre answer=4 text='New y = 36 ÷ 9 ='
   step4 field=pre answer=36 text='Check: if y really ÷ 9, then 4 × 9 ='

silver[5] Q: \(y \propto \sqrt{x}\). When \(x = 16\), \(y = 20\). Find \(y\) when \(x = 100\).
   step0 field=say answer=None text='y = k×√x. Use x = 16, y = 20 to find k.'
   step1 field=pre answer=4 text='√16 ='
   step2 field=pre answer=5 text='k = 20 ÷ 4 ='
   step3 field=pre answer=10 text='New x = 100. √100 ='
   step4 field=pre answer=50 text='y = 5 × 10 ='
   step5 field=pre answer=20 text='Check: k × √16 = 5 × 4 ='

### board=maths-eduqas
gold[0] Q: \(y \propto x^2\). When \(x = a\), \(y = b\). Find \(y\) in terms of \(b\) when \(x = 3a\)

silver[4] Q: \(y \propto x^2\). When \(x\) is tripled, \(y\) is multiplied by:
   step0 field=say answer=None text='y = kx². If x triples, x² is multiplied by 3².'
   step1 field=pre answer=9 text='3² ='
   step2 field=pre answer=4 text='Take k = 1 and x = 2: y = 1 × 2² ='
   step3 field=pre answer=36 text='Triple x to 6: y = 1 × 6² ='
   step4 field=pre answer=9 text='36 ÷ 4 ='

silver[5] Q: \(y \propto \frac{1}{x^2}\). When \(x = 1\), \(y = 36\). Find \(x\) when \(y = 4\).
   step0 field=say answer=None text='Inverse square: y = k/x², so k = y × x². Use x = 1, y = 36.'
   step1 field=pre answer=36 text='k = 36 × 1² ='
   step2 field=pre answer=9 text='Now 4 = 36 ÷ x², so x² = 36 ÷ 4 ='
   step3 field=pre answer=3 text='Square root: x = √9 ='
   step4 field=pre answer=4 text='Check: 36 ÷ 3² = 36 ÷ 9 ='
