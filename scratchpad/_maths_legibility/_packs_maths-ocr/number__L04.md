# maths-ocr / number / L04 - Factors, Multiples & Primes

## bronze[0] (input: single_value, main-box unit: (none))
Q: How many factors does 12 have?
   - intro: Factors come in pairs that multiply to 12. Find every pair.
   - ask: The first pair is 1 × 12. The next pair starts with 2, and 12 ÷ 2 =  [box=6, NO label]
   - ask: The next factor to try is 3, and 12 ÷ 3 =  [box=4, NO label]
   - intro: 4 was already found (in 3 × 4), so the pairs stop: 1×12, 2×6, 3×4.
   - ask: Count all the distinct factors 1, 2, 3, 4, 6, 12. That is  [box=6, NO label]
   - ask: Check they pair up: 3 pairs, so 3 × 2 =  [box=6, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: What is the 7th multiple of 6?
   - intro: A multiple of 6 is 6 times a whole number. The 7th one uses 7.
   - ask: Write the multiplication: the 7th multiple is 6 ×  [box=7, NO label]
   - ask: Work it out: 6 × 7 =  [box=42, NO label]
   - ask: Check by counting in sixes to the 7th: 6, 12, 18, 24, 30, 36, then  [box=42, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Is 29 prime? Enter 1 for yes, 0 for no.
   - intro: A prime has exactly two factors, 1 and itself. Test 29 against small primes.
   - ask: Does 2 divide 29 exactly? Enter 1 for yes, 0 for no:  [box=0, NO label]
   - ask: Does 3 divide 29? The digit sum 2+9 = 11 is not a multiple of 3. Enter 1 or 0:  [box=0, NO label]
   - ask: Does 5 divide 29? Enter 1 or 0:  [box=0, NO label]
   - intro: We only need primes up to \(\sqrt{29}\approx 5.4\), so 2, 3 and 5 are enough.
   - ask: No prime divides it, so 29 is prime. Enter 1:  [box=1, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Find the HCF of 8 and 12
   - intro: List the factors of each number, then find the biggest they share.
   - ask: The factors of 8 are 1, 2, 4 and  [box=8, NO label]
   - ask: The factors of 12 are 1, 2, 3, 4, 6 and  [box=12, NO label]
   - intro: Shared factors are 1, 2 and 4.
   - ask: The highest shared factor is  [box=4, NO label]
   - ask: Check 4 divides both: 8 ÷ 4 = 2 and 12 ÷ 4 =  [box=3, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Find the LCM of 4 and 6
   - intro: List the multiples of each until one appears in both lists.
   - ask: The first four multiples of 4 are 4, 8, 12 and  [box=16, NO label]
   - ask: The first three multiples of 6 are 6, 12 and  [box=18, NO label]
   - ask: The smallest number in both lists is  [box=12, NO label]
   - ask: Check 12 is in both tables: 12 ÷ 4 = 3 and 12 ÷ 6 =  [box=2, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Express 36 as a product of prime factors. How many times does 2 appear?
   - intro: Break 36 down with a factor tree, splitting off primes.
   - ask: Start: 36 = 2 ×  [box=18, NO label]
   - ask: 18 = 2 ×  [box=9, NO label]
   - intro: 9 = 3 × 3, both prime, so 36 = 2 × 2 × 3 × 3 = \(2^2\times 3^2\).
   - ask: Count how many 2s are in 2 × 2 × 3 × 3:  [box=2, NO label]
   - ask: Check the product rebuilds 36: 2 × 2 × 3 × 3 =  [box=36, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Find the HCF of 15 and 20
   - intro: List factors of each and take the largest shared one.
   - ask: The factors of 15 are 1, 3, 5 and  [box=15, NO label]
   - ask: The factors of 20 are 1, 2, 4, 5, 10 and  [box=20, NO label]
   - intro: The only shared factors are 1 and 5.
   - ask: The highest shared factor is  [box=5, NO label]
   - ask: Check: 15 ÷ 5 = 3 and 20 ÷ 5 =  [box=4, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Find the LCM of 3 and 5
   - intro: 3 and 5 share no common factor, so their LCM is simply their product.
   - ask: List multiples of 3 up to 15: 3, 6, 9, 12 and  [box=15, NO label]
   - ask: List multiples of 5 up to 15: 5, 10 and  [box=15, NO label]
   - ask: The first value in both lists is  [box=15, NO label]
   - ask: Since 3 and 5 share no factors, LCM = 3 × 5 =  [box=15, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Find the HCF of 48 and 60
   - intro: Prime factorise both, then take shared primes at their lowest powers.
   - ask: 48 = \(2^4\times 3\), so the power of 2 in 48 is  [box=4, NO label]
   - ask: 60 = \(2^2\times 3\times 5\), so the power of 2 in 60 is  [box=2, NO label]
   - intro: For HCF take each shared prime at its lower power: \(2^2\) (the smaller) and 3 (in both).
   - ask: Multiply the shared primes: \(2^2\times 3\) =  [box=12, NO label]
   - ask: Check 12 divides both: 48 ÷ 12 = 4 and 60 ÷ 12 =  [box=5, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Find the LCM of 8 and 14
   - intro: Prime factorise both, then take every prime at its highest power.
   - ask: 8 = \(2^3\), so the power of 2 in 8 is  [box=3, NO label]
   - ask: 14 = 2 × 7. The new prime that 8 did not have is  [box=7, NO label]
   - intro: Highest powers: \(2^3\) (from 8) and 7 (from 14).
   - ask: Multiply: \(2^3\times 7\) =  [box=56, NO label]
   - ask: Check both divide 56: 56 ÷ 8 = 7 and 56 ÷ 14 =  [box=4, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Find the LCM of 12 and 18
   - intro: Prime factorise both, then take each prime at its highest power.
   - ask: 12 = \(2^2\times 3\), so the power of 2 in 12 is  [box=2, NO label]
   - ask: 18 = \(2\times 3^2\), so the power of 3 in 18 is  [box=2, NO label]
   - intro: Highest powers: \(2^2\) (from 12) and \(3^2\) (from 18).
   - ask: Multiply: \(2^2\times 3^2\) =  [box=36, NO label]
   - ask: Check both divide 36: 36 ÷ 12 = 3 and 36 ÷ 18 =  [box=2, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Express 180 as a product of prime factors. What is the sum of all distinct primes used?
   - intro: Prime factorise 180, then add the different primes.
   - ask: 180 ÷ 2 = 90 and 90 ÷ 2 = 45, so 180 = \(2^2\times 45\). Now 45 ÷ 9 =  [box=5, NO label]
   - intro: So 45 = \(3^2\times 5\), giving 180 = \(2^2\times 3^2\times 5\). Distinct primes: 2, 3, 5.
   - ask: Add the first two distinct primes: 2 + 3 =  [box=5, NO label]
   - ask: Add the last: 5 + 5 =  [box=10, NO label]
   - ask: Check the factorisation: \(2^2\times 3^2\times 5\) = 4 × 9 × 5 =  [box=180, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Find the HCF of 36 and 90
   - intro: Prime factorise both, then take shared primes at their lowest powers.
   - ask: 36 = \(2^2\times 3^2\), so the power of 3 in 36 is  [box=2, NO label]
   - ask: 90 = \(2\times 3^2\times 5\), so the power of 2 in 90 is  [box=1, NO label]
   - intro: Shared primes at lowest powers: \(2^1\) (lower than \(2^2\)) and \(3^2\) (in both).
   - ask: Multiply: \(2\times 3^2\) =  [box=18, NO label]
   - ask: Check 18 divides both: 36 ÷ 18 = 2 and 90 ÷ 18 =  [box=5, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Two buses leave a station together. One returns every 12 minutes, the other every 15 minutes. How many minutes until they're both at the station together?
   - intro: They meet again at the LCM of their intervals, 12 and 15.
   - ask: 12 = \(2^2\times 3\), so the power of 2 in 12 is  [box=2, NO label]
   - ask: 15 = 3 × 5. The new prime that 12 did not have is  [box=5, NO label]
   - intro: Highest powers across both: \(2^2\) (from 12), 3 (in both), 5 (from 15).
   - ask: Multiply: \(2^2\times 3\times 5\) =  [box=60, NO label]
   - ask: Check both intervals divide 60: 60 ÷ 12 = 5 and 60 ÷ 15 =  [box=4, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Find the HCF of 24, 40 and 56
   - intro: Prime factorise all three, then take primes shared by all at their lowest powers.
   - ask: 24 = \(2^3\times 3\), so the power of 2 in 24 is  [box=3, NO label]
   - ask: 40 = \(2^3\times 5\) and 56 = \(2^3\times 7\). The power of 2 shared by all three is  [box=3, NO label]
   - intro: Only 2 is common to all three (3, 5, 7 each appear once), and its lowest power is \(2^3\).
   - ask: So the HCF is \(2^3\) =  [box=8, NO label]
   - ask: Check 8 divides all: 24 ÷ 8 = 3, 40 ÷ 8 = 5, 56 ÷ 8 =  [box=7, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: The HCF of two numbers is 6 and their LCM is 180. One number is 36. What is the other?
   - intro: Use the rule HCF × LCM = the product of the two numbers.
   - ask: Multiply HCF × LCM: 6 × 180 =  [box=1080, NO label]
   - intro: This equals the two numbers multiplied: 36 × other = 1080.
   - ask: So the other number is 1080 ÷ 36 =  [box=30, NO label]
   - ask: Check the HCF of 36 and 30: both share 2 × 3 =  [box=6, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Find the LCM of 24, 36 and 40
   - intro: Prime factorise all three, then take every prime at its highest power.
   - ask: 24 = \(2^3\times 3\), so the power of 2 in 24 is  [box=3, NO label]
   - ask: 36 = \(2^2\times 3^2\), so the power of 3 in 36 is  [box=2, NO label]
   - intro: 40 = \(2^3\times 5\) adds the prime 5. Highest powers overall: \(2^3\), \(3^2\), 5.
   - ask: Multiply: \(2^3\times 3^2\times 5\) = 8 × 9 × 5 =  [box=360, NO label]
   - ask: Check all divide 360: 360 ÷ 24 = 15, 360 ÷ 36 = 10, 360 ÷ 40 =  [box=9, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Write 2520 as a product of primes in index form. What is the index of 2?
   - intro: Divide 2520 by 2 repeatedly and count how many 2s come out.
   - ask: 2520 ÷ 2 =  [box=1260, NO label]
   - ask: 1260 ÷ 2 =  [box=630, NO label]
   - ask: 630 ÷ 2 =  [box=315, NO label]
   - intro: 315 is odd, so no more 2s. We divided by 2 three times.
   - ask: The index of 2 is the number of halvings:  [box=3, NO label]
   - ask: Check: \(2^3 = 8\) and 2520 ÷ 8 = 315, which is odd, so the power of 2 is exactly  [box=3, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: The LCM of two numbers is 60. Their HCF is 4. One number is 20. What is the other?
   - intro: Use HCF × LCM = the product of the two numbers.
   - ask: Multiply HCF × LCM: 4 × 60 =  [box=240, NO label]
   - intro: This equals the two numbers multiplied: 20 × other = 240.
   - ask: So the other number is 240 ÷ 20 =  [box=12, NO label]
   - ask: Check LCM of 20 and 12: 20 = \(2^2\times 5\), 12 = \(2^2\times 3\), LCM = \(2^2\times 3\times 5\) =  [box=60, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Three lights flash at intervals of 4, 6 and 10 seconds. They all flash together. After how many seconds do they next all flash together?
   - intro: They coincide again at the LCM of 4, 6 and 10.
   - ask: 4 = \(2^2\), so the power of 2 in 4 is  [box=2, NO label]
   - ask: 6 = 2 × 3 and 10 = 2 × 5. The two new primes these add are 3 and  [box=5, NO label]
   - intro: Highest powers overall: \(2^2\) (from 4), 3 (from 6), 5 (from 10).
   - ask: Multiply: \(2^2\times 3\times 5\) =  [box=60, NO label]
   - ask: Check all divide 60: 60 ÷ 4 = 15, 60 ÷ 6 = 10, 60 ÷ 10 =  [box=6, NO label]
