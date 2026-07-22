# apply-pack: number__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[1] | Check it is a multiple of the first number: 22680 ÷ 360 = [box=63, NO label] | fix: Add a step that establishes the first number's value before the division, e.g. 'The first number is 2^3 x 3^2 x 5 = 8 x 9 x 5 = [box=360]', then 'Check it is a 
- [medium] silver[1] | Shared power of 2, the lower of 2 and 2, is [box=2, NO label] | fix: Name the prime and the quantity wanted explicitly, separating them from the digits, e.g. 'The prime 2 is in both numbers. Take the SMALLER exponent — the lower 
- [medium] silver[2] | Lowest power of 2 is 2¹ = [box=2] | fix: Split the two meanings so 'power' is not asked to mean both. Phrase value-asks as 'Work out 2¹ = [ ]' and exponent-asks as 'The exponent (power) of 2 is [ ]', k

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[1] Q: Find the LCM of \(2^3 \times 3^2 \times 5\) and \(2^2 \times 3^4 \times 7\)
   step0 field=say answer=None text='For the LCM take every prime at its highest power: 2³, 3⁴, 5 and 7.'
   step1 field=pre answer=648 text='2³ × 3⁴ = 8 × 81 ='
   step2 field=pre answer=3240 text='now × 5: 648 × 5 ='
   step3 field=pre answer=22680 text='now × 7: 3240 × 7 ='
   step4 field=pre answer=63 text='Check it is a multiple of the first number: 22680 ÷ 360 ='

silver[1] Q: Find the LCM of \(15\) and \(20\)
   step0 field=say answer=None text='Prime-factorise both: \\(15 = 3 \\times 5\\) and \\(20 = 2^2 \\times 5\\). Take every prime at i'
   step1 field=pre answer=4 text='Highest power of 2 is 2² ='
   step2 field=pre answer=3 text='Highest power of 3 is 3¹ ='
   step3 field=pre answer=60 text='Highest power of 5 is 5¹. LCM = 4 × 3 × 5 ='
   step4 field=pre answer=3 text='Check: 60 ÷ 20 ='

silver[2] Q: Find the HCF of \(72\) and \(108\)
   step0 field=say answer=None text='Prime-factorise both: \\(72 = 2^3 \\times 3^2\\) and \\(108 = 2^2 \\times 3^3\\). Shared primes '
   step1 field=pre answer=4 text='Lowest power of 2 is 2² ='
   step2 field=pre answer=9 text='Lowest power of 3 is 3² ='
   step3 field=pre answer=36 text='HCF = 4 × 9 ='
   step4 field=pre answer=3 text='Check: 108 ÷ 36 ='

### board=maths-edexcel
gold[1] Q: The HCF of two numbers is 6 and their LCM is 120. One number is 24. Find the other.
   step0 field=say answer=None text='Use the rule HCF × LCM = the product of the two numbers.'
   step1 field=pre answer=720 text='HCF × LCM = 6 × 120 ='
   step2 field=say answer=None text='That product equals the two numbers multiplied: 24 × other = 720.'
   step3 field=pre answer=30 text='Other number = 720 ÷ 24 ='
   step4 field=pre answer=720 text='Check: 24 × 30 ='

silver[1] Q: Find the HCF of \(36\) and \(84\)
   step0 field=say answer=None text='Prime factors: \\(36 = 2^2 \\times 3^2\\) and \\(84 = 2^2 \\times 3 \\times 7\\). Shared primes: '
   step1 field=pre answer=2 text='Shared power of 2, the lower of 2 and 2, is'
   step2 field=pre answer=1 text='Shared power of 3, the lower of 2 and 1, is'
   step3 field=say answer=None text='So HCF = 2² × 3 = 4 × 3.'
   step4 field=pre answer=12 text='4 × 3 ='
   step5 field=pre answer=7 text='Check: 84 ÷ 12 ='

silver[2] Q: Find the LCM of \(15\) and \(20\)
   step0 field=say answer=None text='Primes: \\(15 = 3 \\times 5\\) and \\(20 = 2^2 \\times 5\\). Highest powers: 2² from 20, 3 from '
   step1 field=pre answer=4 text='Work out 2² ='
   step2 field=pre answer=12 text='Multiply by the 3: 4 × 3 ='
   step3 field=pre answer=60 text='Now bring in the 5: 12 × 5 ='
   step4 field=pre answer=3 text='Check: 60 ÷ 20 ='

### board=maths-ocr
gold[1] Q: Find the LCM of 24, 36 and 40
   step0 field=say answer=None text='Prime factorise all three, then take every prime at its highest power.'
   step1 field=pre answer=3 text='24 = \\(2^3\\times 3\\), so the power of 2 in 24 is'
   step2 field=pre answer=2 text='36 = \\(2^2\\times 3^2\\), so the power of 3 in 36 is'
   step3 field=say answer=None text='40 = \\(2^3\\times 5\\) adds the prime 5. Highest powers overall: \\(2^3\\), \\(3^2\\), 5.'
   step4 field=pre answer=360 text='Multiply: \\(2^3\\times 3^2\\times 5\\) = 8 × 9 × 5 ='
   step5 field=pre answer=9 text='Check all divide 360: 360 ÷ 24 = 15, 360 ÷ 36 = 10, 360 ÷ 40 ='

silver[1] Q: Find the LCM of 8 and 14
   step0 field=say answer=None text='Prime factorise both, then take every prime at its highest power.'
   step1 field=pre answer=3 text='8 = \\(2^3\\), so the power of 2 in 8 is'
   step2 field=pre answer=7 text='14 = 2 × 7. The new prime that 8 did not have is'
   step3 field=say answer=None text='Highest powers: \\(2^3\\) (from 8) and 7 (from 14).'
   step4 field=pre answer=56 text='Multiply: \\(2^3\\times 7\\) ='
   step5 field=pre answer=4 text='Check both divide 56: 56 ÷ 8 = 7 and 56 ÷ 14 ='

silver[2] Q: Find the LCM of 12 and 18
   step0 field=say answer=None text='Prime factorise both, then take each prime at its highest power.'
   step1 field=pre answer=2 text='12 = \\(2^2\\times 3\\), so the power of 2 in 12 is'
   step2 field=pre answer=2 text='18 = \\(2\\times 3^2\\), so the power of 3 in 18 is'
   step3 field=say answer=None text='Highest powers: \\(2^2\\) (from 12) and \\(3^2\\) (from 18).'
   step4 field=pre answer=36 text='Multiply: \\(2^2\\times 3^2\\) ='
   step5 field=pre answer=2 text='Check both divide 36: 36 ÷ 12 = 3 and 36 ÷ 18 ='

### board=maths-eduqas
gold[1] Q: Given \(A = 2^3 \times 3 \times 5^2\) and \(B = 2^2 \times 3^2 \times 5\), find the HCF.
   step0 field=say answer=None text='The HCF takes each shared prime at its lower power.'
   step1 field=pre answer=4 text='Power of 2: lower of 3 and 2 is 2, so 2² ='
   step2 field=pre answer=3 text='Power of 3: lower of 1 and 2 is 1, so 3¹ ='
   step3 field=pre answer=5 text='Power of 5: lower of 2 and 1 is 1, so 5¹ ='
   step4 field=pre answer=60 text='HCF = 4 x 3 x 5 ='
   step5 field=pre answer=12 text='Check: 60 divided by 5 ='

silver[1] Q: Find the LCM of \(12\) and \(20\).
   step0 field=say answer=None text='Prime factorise both, then take every prime at its highest power.'
   step1 field=pre answer=4 text='12 = 2² x 3 and 20 = 2² x 5. The shared 2² gives'
   step2 field=pre answer=15 text='The unshared primes are 3 (from 12) and 5 (from 20). 3 x 5 ='
   step3 field=pre answer=60 text='LCM = 4 x 15 ='
   step4 field=pre answer=5 text='Check: 60 divided by 12 ='

silver[2] Q: Find the HCF of \(36\) and \(90\).
   step0 field=say answer=None text='Prime factorise both, then take the shared primes at their lowest powers.'
   step1 field=pre answer=2 text='36 = 2² x 3² and 90 = 2 x 3² x 5. Lowest power of 2 is 2¹ ='
   step2 field=pre answer=9 text='Lowest power of 3 is 3² ='
   step3 field=pre answer=18 text='5 is only in 90, so drop it. HCF = 2 x 9 ='
   step4 field=pre answer=2 text='Check: 36 divided by 18 ='
