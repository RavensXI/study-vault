# maths-edexcel / number / L04 - Factors, Multiples & Primes

## bronze[0] (input: single_value, main-box unit: (none))
Q: Write \(36\) as a product of prime factors. Give the answer as \(2^a \times 3^b\). What is \(a + b\)?
   - intro: Build 36 from its prime building blocks. Split off the 2s first, then the 3s.
   - ask: 36 ÷ 2 =  [box=18, NO label]
   - ask: 18 ÷ 2 =  [box=9, NO label]
   - ask: 9 ÷ 3 =  [box=3, NO label]
   - intro: So 36 = 2 × 2 × 3 × 3 = \(2^2 \times 3^2\). That gives a = 2 and b = 2.
   - ask: a + b = 2 + 2 =  [box=4, NO label]
   - ask: Check the factorisation: 4 × 9 =  [box=36, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(12\) and \(18\)
   - intro: Prime factors: \(12 = 2^2 \times 3\) and \(18 = 2 \times 3^2\). HCF multiplies the shared primes at their lowest power.
   - ask: Shared power of 2, the lower of 2 and 1, is  [box=1, NO label]
   - ask: Shared power of 3, the lower of 1 and 2, is  [box=1, NO label]
   - intro: So HCF = 2 × 3.
   - ask: 2 × 3 =  [box=6, NO label]
   - ask: Check: 18 ÷ 6 =  [box=3, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(6\) and \(10\)
   - intro: Primes: \(6 = 2 \times 3\) and \(10 = 2 \times 5\). LCM uses every prime that appears, each at its highest power: here 2, 3 and 5.
   - ask: First multiply the 2 and the 3: 2 × 3 =  [box=6, NO label]
   - ask: Now bring in the 5: 6 × 5 =  [box=30, NO label]
   - ask: Check: 30 ÷ 10 =  [box=3, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(15\) and \(25\)
   - intro: Prime factors: \(15 = 3 \times 5\) and \(25 = 5^2\). The only shared prime is 5, taken at the lower power.
   - ask: How many 5s does 15 have?  [box=1, NO label]
   - intro: That is the lower count, so the HCF is one 5.
   - ask: HCF =  [box=5, NO label]
   - ask: Check: 25 ÷ 5 =  [box=5, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(4\) and \(6\)
   - intro: Primes: \(4 = 2^2\) and \(6 = 2 \times 3\). LCM takes the highest power of each prime: 2² from 4, and 3 from 6.
   - ask: Work out the highest power of 2: 2² =  [box=4, NO label]
   - ask: Multiply by the 3: 4 × 3 =  [box=12, NO label]
   - ask: Check: 12 ÷ 6 =  [box=2, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: List the prime factors of \(30\). How many different prime factors are there?
   - intro: Break 30 into primes with a factor tree.
   - ask: 30 ÷ 2 =  [box=15, NO label]
   - ask: 15 ÷ 3 =  [box=5, NO label]
   - intro: 5 is prime, so 30 = 2 × 3 × 5. Now count the DIFFERENT primes: 2, 3 and 5.
   - ask: Number of different prime factors =  [box=3, NO label]
   - ask: Check: 2 × 3 × 5 =  [box=30, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(20\) and \(30\)
   - intro: Prime factors: \(20 = 2^2 \times 5\) and \(30 = 2 \times 3 \times 5\). Shared primes: 2 and 5.
   - ask: Shared power of 2, the lower of 2 and 1, is  [box=1, NO label]
   - intro: They also share one 5 each. So HCF = 2 × 5.
   - ask: 2 × 5 =  [box=10, NO label]
   - ask: Check: 30 ÷ 10 =  [box=3, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(8\) and \(12\)
   - intro: Primes: \(8 = 2^3\) and \(12 = 2^2 \times 3\). Highest power of 2 is 2³ = 8; then bring in the 3.
   - ask: Work out 2³ =  [box=8, NO label]
   - ask: Multiply by the 3: 8 × 3 =  [box=24, NO label]
   - ask: Check: 24 ÷ 12 =  [box=2, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Write \(180\) as a product of prime factors. How many 2s appear?
   - intro: Factor 180 down to primes. Peel off 2s first.
   - ask: 180 ÷ 2 =  [box=90, NO label]
   - ask: 90 ÷ 2 =  [box=45, NO label]
   - intro: 45 is odd, so the 2s stop here. 180 = 2 × 2 × 45 = \(2^2 \times 3^2 \times 5\).
   - ask: Number of 2s =  [box=2, NO label]
   - ask: Check: 4 × 45 =  [box=180, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(36\) and \(84\)
   - intro: Prime factors: \(36 = 2^2 \times 3^2\) and \(84 = 2^2 \times 3 \times 7\). Shared primes: 2 and 3.
   - ask: Shared power of 2, the lower of 2 and 2, is  [box=2, NO label]
   - ask: Shared power of 3, the lower of 2 and 1, is  [box=1, NO label]
   - intro: So HCF = 2² × 3 = 4 × 3.
   - ask: 4 × 3 =  [box=12, NO label]
   - ask: Check: 84 ÷ 12 =  [box=7, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(15\) and \(20\)
   - intro: Primes: \(15 = 3 \times 5\) and \(20 = 2^2 \times 5\). Highest powers: 2² from 20, 3 from 15, 5 from either.
   - ask: Work out 2² =  [box=4, NO label]
   - ask: Multiply by the 3: 4 × 3 =  [box=12, NO label]
   - ask: Now bring in the 5: 12 × 5 =  [box=60, NO label]
   - ask: Check: 60 ÷ 20 =  [box=3, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(72\) and \(120\)
   - intro: Prime factors: \(72 = 2^3 \times 3^2\) and \(120 = 2^3 \times 3 \times 5\). Shared primes: 2 and 3.
   - ask: Shared power of 2, the lower of 3 and 3, is  [box=3, NO label]
   - ask: Shared power of 3, the lower of 2 and 1, is  [box=1, NO label]
   - intro: So HCF = 2³ × 3 = 8 × 3.
   - ask: 8 × 3 =  [box=24, NO label]
   - ask: Check: 120 ÷ 24 =  [box=5, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(18\) and \(24\)
   - intro: Primes: \(18 = 2 \times 3^2\) and \(24 = 2^3 \times 3\). Highest powers: 2³ from 24, 3² from 18.
   - ask: Work out 2³ =  [box=8, NO label]
   - ask: Work out 3² =  [box=9, NO label]
   - ask: Multiply them: 8 × 9 =  [box=72, NO label]
   - ask: Check: 72 ÷ 24 =  [box=3, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Write \(1080\) as a product of prime factors. What is the sum of all the index values?
   - intro: Factor 1080 into primes. Peel off 2s, then 3s, then what is left.
   - ask: 1080 ÷ 2 =  [box=540, NO label]
   - ask: 540 ÷ 2 =  [box=270, NO label]
   - ask: 270 ÷ 2 =  [box=135, NO label]
   - intro: 135 = 3 × 3 × 3 × 5, so 1080 = \(2^3 \times 3^3 \times 5^1\). The indices are 3, 3 and 1.
   - ask: Sum of the indices: 3 + 3 + 1 =  [box=7, NO label]
   - ask: Check: 8 × 27 × 5 =  [box=1080, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(9\) and \(15\)
   - intro: Primes: \(9 = 3^2\) and \(15 = 3 \times 5\). Highest powers: 3² from 9, and 5 from 15.
   - ask: Work out 3² =  [box=9, NO label]
   - ask: Multiply by the 5: 9 × 5 =  [box=45, NO label]
   - ask: Check: 45 ÷ 15 =  [box=3, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Find the HCF and LCM of \(48\) and \(180\). What is the HCF?
   - intro: Prime factors: \(48 = 2^4 \times 3\) and \(180 = 2^2 \times 3^2 \times 5\). Shared primes: 2 and 3.
   - ask: Shared power of 2, the lower of 4 and 2, is  [box=2, NO label]
   - ask: Shared power of 3, the lower of 1 and 2, is  [box=1, NO label]
   - intro: So HCF = 2² × 3 = 4 × 3.
   - ask: 4 × 3 =  [box=12, NO label]
   - ask: Check: 48 ÷ 12 =  [box=4, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The HCF of two numbers is 6 and their LCM is 120. One number is 24. Find the other.
   - intro: Use the rule HCF × LCM = the product of the two numbers.
   - ask: HCF × LCM = 6 × 120 =  [box=720, NO label]
   - intro: That product equals the two numbers multiplied: 24 × other = 720.
   - ask: Other number = 720 ÷ 24 =  [box=30, NO label]
   - ask: Check: 24 × 30 =  [box=720, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Write \(2^3 \times 3 \times 5^2\) as a whole number
   - intro: Work out each prime power first, then multiply. Remember 2³ means 2 × 2 × 2, not 2 × 3.
   - ask: 2³ = 2 × 2 × 2 =  [box=8, NO label]
   - ask: 5² = 5 × 5 =  [box=25, NO label]
   - intro: The middle term is just 3, so the product is 8 × 3 × 25.
   - ask: Multiply up: 8 × 3 × 25 =  [box=600, NO label]
   - ask: Check by dividing back: 600 ÷ 25 =  [box=24, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(12\), \(18\) and \(30\)
   - intro: Three numbers now. Factorise each: \(12 = 2^2 \times 3\), \(18 = 2 \times 3^2\), \(30 = 2 \times 3 \times 5\). LCM takes the highest power of every prime that appears: 2², 3², 5.
   - ask: Highest power of 2 is 2² =  [box=4, NO label]
   - ask: Highest power of 3 is 3² =  [box=9, NO label]
   - intro: The highest power of 5 is just 5 (only 30 has it). So LCM = 4 × 9 × 5.
   - ask: Multiply up: 4 × 9 × 5 =  [box=180, NO label]
   - ask: Check: 180 ÷ 30 =  [box=6, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Two buses leave a station at 9 am. Bus A runs every 12 minutes, Bus B every 18 minutes. How many minutes after 9 am do they next leave together?
   - intro: They leave together again after the Lowest Common Multiple of 12 and 18 minutes.
   - intro: Primes: \(12 = 2^2 \times 3\) and \(18 = 2 \times 3^2\). Highest powers: 2² and 3².
   - ask: Work out 2² =  [box=4, NO label]
   - ask: Work out 3² =  [box=9, NO label]
   - ask: LCM = 4 × 9 =  [box=36, NO label]
   - ask: Check: 36 ÷ 12 =  [box=3, NO label]
