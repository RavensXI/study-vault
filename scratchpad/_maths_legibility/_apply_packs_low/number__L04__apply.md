# apply-pack: number__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[3] | Add the last: 5 + 5 = [box=10] | fix: Make the running total explicit, e.g. 'Add the last prime to the running total: 5 (so far) + 5 =' so the two 5s are clearly labelled.
- [low] bronze[2] | Does 3 divide 29? The digit sum 2+9 = 11 is not a multiple of 3. Enter 1 or 0: [ | fix: Add a short in-line reminder of the rule, e.g. '(3 divides a number only when its digits add up to a multiple of 3)'.
- [low] silver[0] | 48 = 2⁴ x 3. The power of 2 in 48 is [box=4] | fix: Add a one-line intro before the first silver ask that names the superscript, e.g. 'In 2⁴ the small 4 is the power — it tells you how many 2s multiply together. 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: Is \(51\) a prime number? Enter 1 for Yes, 0 for No.
   step0 field=say answer=None text='A prime has no factors except 1 and itself. The digits of 51 add to 5 + 1 = 6, a multiple '
   step1 field=pre answer=17 text='51 ÷ 3 ='
   step2 field=say answer=None text='17 is a whole number, so 3 and 17 both divide 51. That is an extra factor, so 51 is compos'
   step3 field=pre answer=2 text='Extra factors beyond 1 and 51: at least'
   step4 field=pre answer=0 text="So enter 0 for 'not prime':"

silver[0] Q: Find the HCF of \(48\) and \(84\)
   step0 field=say answer=None text='Prime-factorise both: \\(48 = 2^4 \\times 3\\) and \\(84 = 2^2 \\times 3 \\times 7\\). Shared pri'
   step1 field=pre answer=4 text='Lowest power of 2 is 2² ='
   step2 field=pre answer=3 text='Lowest power of 3 is 3¹ ='
   step3 field=pre answer=12 text='7 is only in 84, so ignore it. HCF = 4 × 3 ='
   step4 field=pre answer=7 text='Check: 84 ÷ 12 ='

silver[3] Q: Find the LCM of \(8\), \(15\) and \(20\)
   step0 field=say answer=None text='Prime-factorise all three: \\(8 = 2^3\\), \\(15 = 3 \\times 5\\), \\(20 = 2^2 \\times 5\\). Take e'
   step1 field=pre answer=8 text='Highest power of 2, from the 8, is 2³ ='
   step2 field=say answer=None text='Highest power of 3 is 3¹ (from 15), and highest power of 5 is 5¹.'
   step3 field=pre answer=120 text='LCM = 8 × 3 × 5 ='
   step4 field=pre answer=6 text='Check: 120 ÷ 20 ='

### board=maths-edexcel
bronze[2] Q: Find the LCM of \(6\) and \(10\)
   step0 field=say answer=None text='Primes: \\(6 = 2 \\times 3\\) and \\(10 = 2 \\times 5\\). LCM uses every prime that appears, eac'
   step1 field=pre answer=6 text='First multiply the 2 and the 3: 2 × 3 ='
   step2 field=pre answer=30 text='Now bring in the 5: 6 × 5 ='
   step3 field=pre answer=3 text='Check: 30 ÷ 10 ='

silver[0] Q: Write \(180\) as a product of prime factors. How many 2s appear?
   step0 field=say answer=None text='Factor 180 down to primes. Peel off 2s first.'
   step1 field=pre answer=90 text='180 ÷ 2 ='
   step2 field=pre answer=45 text='90 ÷ 2 ='
   step3 field=say answer=None text='45 is odd, so the 2s stop here. 180 = 2 × 2 × 45 = \\(2^2 \\times 3^2 \\times 5\\).'
   step4 field=pre answer=2 text='Number of 2s ='
   step5 field=pre answer=180 text='Check: 4 × 45 ='

silver[3] Q: Find the HCF of \(72\) and \(120\)
   step0 field=say answer=None text='Prime factors: \\(72 = 2^3 \\times 3^2\\) and \\(120 = 2^3 \\times 3 \\times 5\\). Shared primes:'
   step1 field=pre answer=3 text='Shared power of 2, the lower of 3 and 3, is'
   step2 field=pre answer=1 text='Shared power of 3, the lower of 2 and 1, is'
   step3 field=say answer=None text='So HCF = 2³ × 3 = 8 × 3.'
   step4 field=pre answer=24 text='8 × 3 ='
   step5 field=pre answer=5 text='Check: 120 ÷ 24 ='

### board=maths-ocr
bronze[2] Q: Is 29 prime? Enter 1 for yes, 0 for no.
   step0 field=say answer=None text='A prime has exactly two factors, 1 and itself. Test 29 against small primes.'
   step1 field=pre answer=0 text='Does 2 divide 29 exactly? Enter 1 for yes, 0 for no:'
   step2 field=pre answer=0 text='Does 3 divide 29? The digit sum 2+9 = 11 is not a multiple of 3. Enter 1 or 0:'
   step3 field=pre answer=0 text='Does 5 divide 29? Enter 1 or 0:'
   step4 field=say answer=None text='We only need primes up to \\(\\sqrt{29}\\approx 5.4\\), so 2, 3 and 5 are enough.'
   step5 field=pre answer=1 text='No prime divides it, so 29 is prime. Enter 1:'

silver[0] Q: Find the HCF of 48 and 60
   step0 field=say answer=None text='Prime factorise both, then take shared primes at their lowest powers.'
   step1 field=pre answer=4 text='48 = \\(2^4\\times 3\\), so the power of 2 in 48 is'
   step2 field=pre answer=2 text='60 = \\(2^2\\times 3\\times 5\\), so the power of 2 in 60 is'
   step3 field=say answer=None text='For HCF take each shared prime at its lower power: \\(2^2\\) (the smaller) and 3 (in both).'
   step4 field=pre answer=12 text='Multiply the shared primes: \\(2^2\\times 3\\) ='
   step5 field=pre answer=5 text='Check 12 divides both: 48 ÷ 12 = 4 and 60 ÷ 12 ='

silver[3] Q: Express 180 as a product of prime factors. What is the sum of all distinct primes used?
   step0 field=say answer=None text='Prime factorise 180, then add the different primes.'
   step1 field=pre answer=5 text='180 ÷ 2 = 90 and 90 ÷ 2 = 45, so 180 = \\(2^2\\times 45\\). Now 45 ÷ 9 ='
   step2 field=say answer=None text='So 45 = \\(3^2\\times 5\\), giving 180 = \\(2^2\\times 3^2\\times 5\\). Distinct primes: 2, 3, 5.'
   step3 field=pre answer=5 text='Add the first two distinct primes: 2 + 3 ='
   step4 field=pre answer=10 text='Add the last: 5 + 5 ='
   step5 field=pre answer=180 text='Check the factorisation: \\(2^2\\times 3^2\\times 5\\) = 4 × 9 × 5 ='

### board=maths-eduqas
bronze[2] Q: Find the first 4 multiples of \(7\) (give the 4th).
   step0 field=say answer=None text='Multiples are 7 times 1, 2, 3 and 4.'
   step1 field=pre answer=7 text='7 x 1 ='
   step2 field=pre answer=14 text='7 x 2 ='
   step3 field=pre answer=21 text='7 x 3 ='
   step4 field=pre answer=28 text='7 x 4 ='
   step5 field=pre answer=4 text='Check: 28 divided by 7 ='

silver[0] Q: Find the HCF of \(48\) and \(60\).
   step0 field=say answer=None text='Prime factorise both, then take the shared primes at their lowest powers.'
   step1 field=pre answer=4 text='48 = 2⁴ x 3. The power of 2 in 48 is'
   step2 field=pre answer=2 text='60 = 2² x 3 x 5. The power of 2 in 60 is'
   step3 field=pre answer=12 text='Lowest power of 2 is 2² = 4. The shared 3 gives 3. HCF = 4 x 3 ='
   step4 field=pre answer=4 text='Check: 48 divided by 12 ='

silver[3] Q: Find the LCM of \(9\) and \(15\).
   step0 field=say answer=None text='Prime factorise both, then take each prime at its highest power.'
   step1 field=pre answer=9 text='9 = 3² and 15 = 3 x 5. The highest power of 3 is 3² ='
   step2 field=pre answer=45 text='5 appears only in 15, so bring it in. LCM = 9 x 5 ='
   step3 field=pre answer=3 text='Check: 45 divided by 15 ='
