# maths-aqa / number / L04 - Factors, Multiples & Primes

## bronze[0] (input: single_value, main-box unit: (none))
Q: List all the factors of \(24\). How many factors does it have?
   - intro: Find factors in pairs that multiply to 24.
   - ask: 24 ÷ 1 =  [box=24, NO label]
   - ask: 24 ÷ 2 =  [box=12, NO label]
   - ask: 24 ÷ 3 =  [box=8, NO label]
   - ask: 24 ÷ 4 =  [box=6, NO label]
   - intro: 5 does not divide 24, and 6 is already partnered with 4, so the pairs are complete. The factors are 1, 2, 3, 4, 6, 8, 12, 24.
   - ask: How many pairs did you find?  [box=4, NO label]
   - ask: Each pair is 2 factors, so the total is 4 × 2 =  [box=8, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: What is the 7th multiple of \(6\)?
   - intro: The multiples of 6 are 6 × 1, 6 × 2, 6 × 3, and so on. The 7th multiple is 6 × 7.
   - ask: 6 × 5 =  [box=30, NO label]
   - ask: 6 × 6 =  [box=36, NO label]
   - ask: 6 × 7 =  [box=42, NO label]
   - ask: Check it is in the 6 times table: 42 ÷ 6 =  [box=7, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Is \(51\) a prime number? Enter 1 for Yes, 0 for No.
   - intro: A prime has no factors except 1 and itself. The digits of 51 add to 5 + 1 = 6, a multiple of 3, so test 3.
   - ask: 51 ÷ 3 =  [box=17, NO label]
   - intro: 17 is a whole number, so 3 and 17 both divide 51. That is an extra factor, so 51 is composite, not prime.
   - ask: Extra factors beyond 1 and 51: at least  [box=2, NO label]
   - ask: So enter 0 for 'not prime':  [box=0, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Write \(60\) as a product of prime factors. What is the largest prime factor?
   - intro: Divide 60 by the smallest prime each time.
   - ask: 60 ÷ 2 =  [box=30, NO label]
   - ask: 30 ÷ 2 =  [box=15, NO label]
   - intro: 15 is odd, so move to the next prime, 3: 15 ÷ 3 = 5, and 5 is prime. So \(60 = 2^2 \times 3 \times 5\).
   - ask: The primes used are 2, 3 and 5. The largest is  [box=5, NO label]
   - ask: Check: 2² × 3 × 5 = 4 × 15 =  [box=60, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Write \(90\) as a product of prime factors. How many times does \(3\) appear?
   - intro: Factor-tree 90 down to primes.
   - ask: 90 ÷ 2 =  [box=45, NO label]
   - intro: 45 is odd, so move to 3.
   - ask: 45 ÷ 3 =  [box=15, NO label]
   - ask: 15 ÷ 3 =  [box=5, NO label]
   - intro: 5 is prime, so stop. So \(90 = 2 \times 3 \times 3 \times 5 = 2 \times 3^2 \times 5\).
   - ask: Count the 3s in 2 × 3 × 3 × 5:  [box=2, NO label]
   - ask: Check: 2 × 3² × 5 = 2 × 9 × 5 =  [box=90, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(12\) and \(18\)
   - intro: Prime-factorise both: \(12 = 2^2 \times 3\) and \(18 = 2 \times 3^2\). Take each shared prime at its lowest power.
   - ask: Lowest power of 2 is 2¹ =  [box=2, NO label]
   - ask: Lowest power of 3 is 3¹ =  [box=3, NO label]
   - ask: HCF = 2 × 3 =  [box=6, NO label]
   - ask: Check: 12 ÷ 6 =  [box=2, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(4\) and \(6\)
   - intro: List the multiples of each number until one appears in both lists.
   - ask: Multiples of 4: 4, 8,  [box=12, NO label]
   - ask: Multiples of 6: 6,  [box=12, NO label]
   - ask: The first value in both lists is  [box=12, NO label]
   - ask: Check: 12 ÷ 6 =  [box=2, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(5\) and \(8\)
   - intro: 5 and 8 share no common factor, so list multiples until they meet.
   - ask: Multiples of 5: 5, 10, 15, 20, 25, 30, 35,  [box=40, NO label]
   - ask: Multiples of 8: 8, 16, 24, 32,  [box=40, NO label]
   - ask: First shared value:  [box=40, NO label]
   - ask: Since 5 and 8 share no factor, LCM = 5 × 8 =  [box=40, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(48\) and \(84\)
   - intro: Prime-factorise both: \(48 = 2^4 \times 3\) and \(84 = 2^2 \times 3 \times 7\). Shared primes are 2 and 3.
   - ask: Lowest power of 2 is 2² =  [box=4, NO label]
   - ask: Lowest power of 3 is 3¹ =  [box=3, NO label]
   - ask: 7 is only in 84, so ignore it. HCF = 4 × 3 =  [box=12, NO label]
   - ask: Check: 84 ÷ 12 =  [box=7, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(15\) and \(20\)
   - intro: Prime-factorise both: \(15 = 3 \times 5\) and \(20 = 2^2 \times 5\). Take every prime at its highest power.
   - ask: Highest power of 2 is 2² =  [box=4, NO label]
   - ask: Highest power of 3 is 3¹ =  [box=3, NO label]
   - ask: Highest power of 5 is 5¹. LCM = 4 × 3 × 5 =  [box=60, NO label]
   - ask: Check: 60 ÷ 20 =  [box=3, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(72\) and \(108\)
   - intro: Prime-factorise both: \(72 = 2^3 \times 3^2\) and \(108 = 2^2 \times 3^3\). Shared primes are 2 and 3.
   - ask: Lowest power of 2 is 2² =  [box=4, NO label]
   - ask: Lowest power of 3 is 3² =  [box=9, NO label]
   - ask: HCF = 4 × 9 =  [box=36, NO label]
   - ask: Check: 108 ÷ 36 =  [box=3, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(8\), \(15\) and \(20\)
   - intro: Prime-factorise all three: \(8 = 2^3\), \(15 = 3 \times 5\), \(20 = 2^2 \times 5\). Take every prime at its highest power.
   - ask: Highest power of 2, from the 8, is 2³ =  [box=8, NO label]
   - intro: Highest power of 3 is 3¹ (from 15), and highest power of 5 is 5¹.
   - ask: LCM = 8 × 3 × 5 =  [box=120, NO label]
   - ask: Check: 120 ÷ 20 =  [box=6, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Two numbers have HCF 6 and LCM 90. One number is 18. Find the other.
   - intro: For two numbers, HCF × LCM = the product of the numbers themselves.
   - ask: HCF × LCM = 6 × 90 =  [box=540, NO label]
   - ask: The two numbers multiply to 540 and one is 18, so the other = 540 ÷ 18 =  [box=30, NO label]
   - ask: Check HCF of 18 and 30: 18 = 2 × 3², 30 = 2 × 3 × 5, shared 2 × 3 =  [box=6, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Write \(180\) as a product of prime factors. How many distinct prime factors?
   - intro: Factor-tree 180 down to primes.
   - ask: 180 ÷ 2 =  [box=90, NO label]
   - ask: 90 ÷ 2 =  [box=45, NO label]
   - intro: 45 is odd: 45 ÷ 3 = 15, 15 ÷ 3 = 5, and 5 is prime. So \(180 = 2^2 \times 3^2 \times 5\).
   - ask: The different primes are 2, 3 and 5, so the count of distinct primes is  [box=3, NO label]
   - ask: Check: 2² × 3² × 5 = 4 × 9 × 5 =  [box=180, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: The LCM of two numbers is \(120\). One number is \(24\). The other is between \(30\) and \(50\). Find it.
   - intro: Here \(120 = 2^3 \times 3 \times 5\) and \(24 = 2^3 \times 3\). The other number must bring in the factor 5, and must divide 120.
   - ask: Test 40: 120 ÷ 40 =  [box=3, NO label]
   - ask: 40 = 2³ × 5. Check LCM(24, 40) = highest powers 2³ × 3 × 5 =  [box=120, NO label]
   - ask: 120 is the target and 40 lies between 30 and 50, so the other number is  [box=40, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(2^3 \times 3^2 \times 5\) and \(2^2 \times 3^4 \times 7\)
   - intro: Already in index form, so read straight off. Shared primes are 2 and 3, not 5 or 7. Take each at its lowest power.
   - ask: Lowest power of 2 is 2² =  [box=4, NO label]
   - ask: Lowest power of 3 is 3² =  [box=9, NO label]
   - ask: HCF = 4 × 9 =  [box=36, NO label]
   - ask: Confirm the value of the HCF:  [box=36, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(2^3 \times 3^2 \times 5\) and \(2^2 \times 3^4 \times 7\)
   - intro: For the LCM take every prime at its highest power: 2³, 3⁴, 5 and 7.
   - ask: 2³ × 3⁴ = 8 × 81 =  [box=648, NO label]
   - ask: now × 5: 648 × 5 =  [box=3240, NO label]
   - ask: now × 7: 3240 × 7 =  [box=22680, NO label]
   - ask: Check it is a multiple of the first number: 22680 ÷ 360 =  [box=63, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Prove that the sum of any three consecutive integers is always divisible by 3. What is the sum of three consecutive integers starting at \(14\)?
   - intro: Call the integers \(n\), \(n+1\), \(n+2\). Their sum is \(n + (n+1) + (n+2) = 3n + 3 = 3(n+1)\), which is 3 times a whole number, so always divisible by 3.
   - ask: Now use n = 14, giving 14, 15, 16. First, 14 + 15 =  [box=29, NO label]
   - ask: then + 16: 29 + 16 =  [box=45, NO label]
   - ask: Check it is divisible by 3: 45 ÷ 3 =  [box=15, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Pens come in packs of \(8\). Rulers come in packs of \(12\). What is the smallest number of each you must buy to have equal numbers of pens and rulers?
   - intro: You want the smallest total that is a multiple of both 8 and 12: the LCM. \(8 = 2^3\) and \(12 = 2^2 \times 3\).
   - ask: Highest power of 2, from the 8, is 2³ =  [box=8, NO label]
   - ask: Highest power of 3 is 3¹. LCM = 8 × 3 =  [box=24, NO label]
   - ask: Check rulers: 24 ÷ 12 =  [box=2, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: \(n = 2^a \times 3^b\). If \(n\) has exactly 12 factors and \(100 < n < 200\), find \(n\).
   - intro: The number of factors of \(2^a \times 3^b\) is \((a+1)(b+1)\). You need this to equal 12 with the value between 100 and 200.
   - ask: Try a = 2, b = 3: (2+1)(3+1) = 3 × 4 =  [box=12, NO label]
   - ask: That value is 2² × 3³ = 4 × 27 =  [box=108, NO label]
   - intro: Is 108 between 100 and 200? Yes. The other factor pairs fall outside: (a,b) = (5,1) gives 96 (too small), (3,2) gives 72 (too small), (1,5) gives 486 (too big).
   - ask: So the only value between 100 and 200 is  [box=108, NO label]
   - ask: Confirm its factor count: (2+1)(3+1) =  [box=12, NO label]
