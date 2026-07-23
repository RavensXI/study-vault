# apply-pack: number__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[1] | 3 is already below 10, so no adjusting. Enter the power to finish 3 × 10 to the  | fix: Reword to: 'Enter the power of 10 to complete the answer 3 × 10ⁿ.'
- [low] bronze[1] | 12 lands on 144, so write \(\sqrt{144}\). [box=12, NO label] | fix: Reword to 'so √144 = [box]' or 'so the answer is [box]' (apply to all four root steps).
- [low] gold[4] | Now 4^(−1/2): the 1/2 is a square root, √4 = 2, and the minus flips it to 1/2. M | fix: Split into short sentences: 'Now do 4^(−1/2). The 1/2 means square root: √4 = 2. The minus flips it, so 4^(−1/2) = 1/2. Now multiply the two results.'
- [low] gold[1] | Same base, so add those indices. | fix: Bridge the vocabulary once: 'Same base, so add those powers (the indices): 2 + 2 + 2 + 2'.
- [low] gold[0] | 9 is already below 10, so no adjusting. Enter the power to finish 9 × 10 to the  | fix: Rewrite as: 'Enter the power n to finish 9 × 10ⁿ.'
- [low] gold[2] | 4 is already below 10, so no adjusting. Enter the power to finish 4 × 10 to the  | fix: Rewrite as: 'Enter the power n to finish 4 × 10ⁿ.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[1] Q: Calculate \(\sqrt{144}\)
   step0 field=say answer=None text='A square root reverses squaring: it asks what number times itself gives 144.'
   step1 field=pre answer=121 text='Try 11 × 11 ='
   step2 field=pre answer=144 text='Try the next one: 12 × 12 ='
   step3 field=pre answer=12 text='12 lands on 144, so write \\(\\sqrt{144}\\).'

gold[0] Q: Calculate \((6 \times 10^4) \times (5 \times 10^{-2})\). Give your answer in standard form
   step0 field=say answer=None text='Multiply the fronts, add the powers (keep the minus), then fix the front.'
   step1 field=pre answer=30 text='Multiply the fronts: 6 × 5 ='
   step2 field=pre answer=2 text='Add the powers: 4 + (−2) ='
   step3 field=pre answer=3 text='That is 30 × 10², but A must be below 10. Write 30 as 3 × 10, so the new A is:'
   step4 field=pre answer=3 text='Moving 30 down to 3 adds 1 to the power: 2 + 1 ='

gold[1] Q: Calculate \(\frac{3.6 \times 10^8}{1.2 \times 10^{-3}}\). Give your answer in standard for
   step0 field=say answer=None text='Divide the fronts and subtract the powers. Watch the second power: it is negative.'
   step1 field=pre answer=3 text='Divide the fronts: 3.6 ÷ 1.2 ='
   step2 field=pre answer=11 text='Subtract the powers. Subtracting a negative adds: 8 − (−3) = 8 + 3 ='
   step3 field=pre answer=11 text='3 is already below 10, so no adjusting. Enter the power to finish 3 × 10 to the n.'

gold[2] Q: The mass of a proton is \(1.67 \times 10^{-27}\) kg. Find the mass of \(3 \times 10^{23}\)
   step0 field=say answer=None text='Total mass is the mass of one proton times the number of protons, so multiply.'
   step1 field=pre answer=5.01 text='Multiply the fronts: 1.67 × 3 ='
   step2 field=pre answer=-4 text='Add the powers: −27 + 23 ='
   step3 field=pre answer=5.01 text='So the mass is 5.01 × 10⁻⁴ kg. The question wants the A value. Enter it.'

gold[4] Q: Light travels at \(3 \times 10^8\) m/s. How far does it travel in \(5 \times 10^2\) second
   step0 field=say answer=None text='Distance is speed × time. Multiply the fronts and add the powers, then fix the front.'
   step1 field=pre answer=15 text='Multiply the fronts: 3 × 5 ='
   step2 field=pre answer=10 text='Add the powers: 8 + 2 ='
   step3 field=pre answer=11 text='That is 15 × 10¹⁰, but 15 is not below 10. Writing 15 as 1.5 × 10 adds 1 to the power: 10 '
   step4 field=pre answer=11 text='So the distance is 1.5 × 10¹¹ m. The question wants the power. Enter it.'

### board=maths-edexcel
bronze[1] Q: Calculate \(\sqrt{196}\)
   step0 field=say answer=None text='\\(\\sqrt{196}\\) asks what number, times itself, makes 196. It lies between \\(\\sqrt{100} = 1'
   step1 field=pre answer=140 text='Test 14 by squaring. In parts: 14 × 10 ='
   step2 field=pre answer=56 text='14 × 4 ='
   step3 field=pre answer=196 text='Add the parts: 140 + 56 ='
   step4 field=pre answer=14 text='That is 196, the number under the root, so \\(\\sqrt{196}\\) ='

gold[0] Q: Calculate \((6 \times 10^4) \times (5 \times 10^{-2})\). Give your answer in standard form
   step0 field=say answer=None text='Multiplying in standard form, with a negative power in the mix. Fronts and powers separate'
   step1 field=pre answer=30 text='Multiply the fronts: 6 × 5 ='
   step2 field=pre answer=2 text='ADD the powers, keeping the signs: 4 + (−2) ='
   step3 field=say answer=None text='That gives 30 × 10². A = 30 is not between 1 and 10, so adjust.'
   step4 field=pre answer=3 text='Write 30 as 3 × 10, so the tidy A ='
   step5 field=pre answer=3 text='Moving one 10 into the power lifts it by 1: 2 + 1 ='
   step6 field=pre answer=3000 text='Check by expanding: 3 × 10³ ='

gold[1] Q: Calculate \((2.4 \times 10^6) + (5 \times 10^5)\). Give your answer in standard form.
   step0 field=say answer=None text='Adding in standard form: the powers must match before you add the fronts.'
   step1 field=pre answer=0.5 text='Rewrite 5 × 10⁵ as a power of 10⁶. Drop the front to a tenth: 5 becomes'
   step2 field=pre answer=2.9 text='Now both are × 10⁶. Add the fronts: 2.4 + 0.5 ='
   step3 field=pre answer=6 text='A = 2.9 is in range, so the power is unchanged. n ='
   step4 field=pre answer=2900000 text='Check by expanding: 2 400 000 + 500 000 ='

gold[2] Q: Light travels at \(3 \times 10^8\) m/s. How far does it travel in \(5 \times 10^2\) second
   step0 field=say answer=None text='Distance = speed × time. Multiply the fronts and add the powers.'
   step1 field=pre answer=15 text='Multiply the fronts: 3 × 5 ='
   step2 field=pre answer=10 text='ADD the powers: 8 + 2 ='
   step3 field=say answer=None text='That gives 15 × 10¹⁰. A = 15 is too big, so adjust.'
   step4 field=pre answer=1.5 text='Write 15 as 1.5 × 10, so the tidy A ='
   step5 field=pre answer=11 text='Lift the power by 1: 10 + 1 ='
   step6 field=say answer=None text='Check the size: \\(10^8 \\times 10^2 = 10^{10}\\), and the 15 adds one more ten, giving \\(10^'

gold[4] Q: A bacteria colony doubles every hour. Starting at \(5 \times 10^3\), how many after 4 hour
   step0 field=say answer=None text='Doubling every hour for 4 hours means multiplying by 2 four times, that is × 2⁴.'
   step1 field=pre answer=16 text='Work out 2⁴: 2 × 2 × 2 × 2 ='
   step2 field=pre answer=5000 text='Write the start as an ordinary number: 5 × 10³ ='
   step3 field=pre answer=80000 text='Multiply: 5000 × 16 ='
   step4 field=pre answer=8 text='Standard form A: slide 80 000 to one digit in front. A ='
   step5 field=pre answer=4 text='Count the places moved, giving the power n ='

### board=maths-ocr
bronze[1] Q: Evaluate \(\sqrt{144}\)
   step0 field=pre answer=100 text='10 × 10 ='
   step1 field=pre answer=144 text='12 × 12 ='
   step2 field=pre answer=12 text='So √144 ='

gold[0] Q: Calculate \((6 \times 10^4) \times (5 \times 10^{-2})\)
   step0 field=pre answer=30 text='6 × 5 ='
   step1 field=pre answer=2 text='4 + (−2) ='
   step2 field=pre answer=3 text='The new A is'
   step3 field=pre answer=3 text='The extra 10 lifts the power: 2 + 1 ='

gold[1] Q: Simplify \((3^2)^4\). Give your answer as a power of 3.
   step0 field=pre answer=8 text='2 + 2 + 2 + 2 ='
   step1 field=pre answer=8 text='That is the same as multiplying: 2 × 4 ='
   step2 field=pre answer=8 text='So (3²)⁴ = 3 to the power'

gold[2] Q: Evaluate \(125^{-2/3}\). Give your answer as a fraction.
   step0 field=pre answer=125 text='5 × 5 × 5 ='
   step1 field=pre answer=25 text='5 × 5 ='
   step2 field=pre answer=1 text='The top of the fraction is'
   step3 field=pre answer=25 text='The bottom of the fraction is'

gold[4] Q: Evaluate \(8^{2/3} \times 4^{-1/2}\). Give your answer as a fraction.
   step0 field=pre answer=4 text='2 × 2 ='
   step1 field=pre answer=2 text='4 × 1/2 ='
   step2 field=pre answer=2 text='As a fraction that is 2/1, so the numerator is'
   step3 field=pre answer=1 text='and the denominator is'

### board=maths-eduqas
bronze[1] Q: \(2^6\)
   step0 field=say answer=None text='\\(2^6\\) means six 2s multiplied together.'
   step1 field=pre answer=8 text='First three 2s: 2 × 2 × 2 ='
   step2 field=pre answer=16 text='That is 2³. Multiply by the fourth 2: 8 × 2 ='
   step3 field=pre answer=32 text='Multiply by the fifth 2: 16 × 2 ='
   step4 field=pre answer=64 text='Multiply by the sixth 2: 32 × 2 ='

gold[0] Q: Calculate \((3 \times 10^4)^2\). Give your answer in standard form.
   step0 field=say answer=None text='Squaring \\((3 \\times 10^4)^2\\) squares the front and multiplies the power by 2.'
   step1 field=pre answer=9 text='Square the front: 3 × 3 ='
   step2 field=pre answer=8 text='Square the power part: (10⁴)² multiplies the power by 2, so 4 × 2 ='
   step3 field=pre answer=8 text='9 is already below 10, so no adjusting. Enter the power to finish 9 × 10 to the n.'

gold[1] Q: Calculate \((2.4 \times 10^5) + (3.6 \times 10^4)\). Give your answer in standard form.
   step0 field=say answer=None text='You can only add standard-form numbers directly when the powers match. Here they differ, s'
   step1 field=pre answer=240000 text='Write the first as an ordinary number: 2.4 × 10⁵ ='
   step2 field=pre answer=36000 text='Write the second: 3.6 × 10⁴ ='
   step3 field=pre answer=276000 text='Add them: 240000 + 36000 ='
   step4 field=pre answer=2.76 text='Write 276000 in standard form. Enter A, a number below 10.'
   step5 field=pre answer=5 text='Count the places from 276000 back to 2.76 for the power.'

gold[2] Q: Calculate \(\dfrac{6 \times 10^8}{1.5 \times 10^{-2}}\). Standard form.
   step0 field=say answer=None text='Divide the fronts and subtract the powers. Watch the second power: it is negative.'
   step1 field=pre answer=4 text='Divide the fronts: 6 ÷ 1.5 ='
   step2 field=pre answer=10 text='Subtract the powers. Subtracting a negative adds: 8 − (−2) = 8 + 2 ='
   step3 field=pre answer=10 text='4 is already below 10, so no adjusting. Enter the power to finish 4 × 10 to the n.'

gold[4] Q: Simplify \(\dfrac{(2 \times 10^3)^3}{4 \times 10^5}\). Standard form.
   step0 field=say answer=None text='Cube the top bracket first: cube the front and multiply its power by 3. Then divide.'
   step1 field=pre answer=8 text='Cube the front of the top: 2 × 2 × 2 ='
   step2 field=pre answer=9 text='Cube its power: (10³)³ multiplies the power by 3, so 3 × 3 ='
   step3 field=pre answer=2 text='So the top is 8 × 10⁹. Divide the fronts: 8 ÷ 4 ='
   step4 field=pre answer=4 text='Subtract the powers: 9 − 5 ='
