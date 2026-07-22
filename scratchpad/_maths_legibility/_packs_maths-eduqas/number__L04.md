# maths-eduqas / number / L04 - Factors, Multiples & Primes

## bronze[0] (input: single_value, main-box unit: (none))
Q: How many factors does \(24\) have?
   - intro: Factors come in pairs that multiply to 24. Find each pair.
   - ask: 3 x ? = 24, so ? =  [box=8, NO label]
   - ask: 4 x ? = 24, so ? =  [box=6, NO label]
   - intro: Now count every different number that appears.
   - ask: The pairs are 1x24, 2x12, 3x8, 4x6. Number of different factors =  [box=8, NO label]
   - ask: Check: is 5 a factor of 24? Type 1 for yes, 0 for no:  [box=0, NO label]

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Is \(51\) prime?

## bronze[2] (input: single_value, main-box unit: (none))
Q: Find the first 4 multiples of \(7\) (give the 4th).
   - intro: Multiples are 7 times 1, 2, 3 and 4.
   - ask: 7 x 1 =  [box=7, NO label]
   - ask: 7 x 2 =  [box=14, NO label]
   - ask: 7 x 3 =  [box=21, NO label]
   - intro: The 4th multiple is 7 x 4.
   - ask: 7 x 4 =  [box=28, NO label]
   - ask: Check: 28 divided by 7 =  [box=4, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Write \(60\) as a product of prime factors. How many times does \(2\) appear?
   - intro: Split 60 into primes one step at a time.
   - ask: 60 = 2 x ? , so ? =  [box=30, NO label]
   - ask: 30 = 2 x ? , so ? =  [box=15, NO label]
   - ask: 15 = 3 x ? , so ? =  [box=5, NO label]
   - intro: The primes are 2, 2, 3 and 5.
   - ask: So 60 = 2 x 2 x 3 x 5. How many 2s?  [box=2, NO label]
   - ask: Check: 2 x 2 x 3 x 5 =  [box=60, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(12\) and \(18\).
   - intro: List the factors of each, then find the biggest number they share.
   - ask: Factors of 12: 1, 2, 3, 4, 6, 12. Is 12 a factor of 18? Type 1 or 0:  [box=0, NO label]
   - ask: Factors of 18: 1, 2, 3, 6, 9, 18. Is 9 a factor of 12? Type 1 or 0:  [box=0, NO label]
   - intro: Shared factors: 1, 2, 3, 6.
   - ask: The numbers in BOTH lists are 1, 2, 3, 6. The biggest is  [box=6, NO label]
   - ask: Check: 12 divided by 6 =  [box=2, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(4\) and \(6\).
   - intro: List the multiples of each until they meet.
   - ask: Multiples of 4: 4, 8, then next is  [box=12, NO label]
   - ask: Multiples of 6: 6, then next is  [box=12, NO label]
   - intro: 12 shows up in both lists.
   - ask: The smallest number in BOTH lists is  [box=12, NO label]
   - ask: Check: 12 divided by 4 =  [box=3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(5\) and \(8\).
   - intro: 5 and 8 share no factor except 1, so list multiples of the bigger one and test each.
   - ask: Multiples of 8: 8, 16, 24, 32, 40. Is 8 a multiple of 5? Type 1 or 0:  [box=0, NO label]
   - ask: Is 16 a multiple of 5? Type 1 or 0:  [box=0, NO label]
   - ask: Is 24 a multiple of 5? Type 1 or 0:  [box=0, NO label]
   - intro: 40 is the first multiple of 8 that 5 also divides.
   - ask: 40 is 8 x 5, so it is a multiple of both. The LCM is  [box=40, NO label]
   - ask: Check: 40 divided by 5 =  [box=8, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(20\) and \(30\).
   - intro: List the factors of each and pick the biggest shared one.
   - ask: Factors of 20: 1, 2, 4, 5, 10, 20. Is 20 a factor of 30? Type 1 or 0:  [box=0, NO label]
   - ask: Factors of 30: 1, 2, 3, 5, 6, 10, 15, 30. Is 4 a factor of 30? Type 1 or 0:  [box=0, NO label]
   - intro: Both lists contain 1, 2, 5 and 10.
   - ask: Shared factors: 1, 2, 5, 10. The biggest is  [box=10, NO label]
   - ask: Check: 20 divided by 10 =  [box=2, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(48\) and \(60\).
   - intro: Prime factorise both, then take the shared primes at their lowest powers.
   - ask: 48 = 2⁴ x 3. The power of 2 in 48 is  [box=4, NO label]
   - ask: 60 = 2² x 3 x 5. The power of 2 in 60 is  [box=2, NO label]
   - intro: 5 appears in 60 only, so it is not shared.
   - ask: Lowest power of 2 is 2² = 4. The shared 3 gives 3. HCF = 4 x 3 =  [box=12, NO label]
   - ask: Check: 48 divided by 12 =  [box=4, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(12\) and \(20\).
   - intro: Prime factorise both, then take every prime at its highest power.
   - ask: 12 = 2² x 3 and 20 = 2² x 5. The shared 2² gives  [box=4, NO label]
   - ask: The unshared primes are 3 (from 12) and 5 (from 20). 3 x 5 =  [box=15, NO label]
   - intro: That is 2² x 3 x 5.
   - ask: LCM = 4 x 15 =  [box=60, NO label]
   - ask: Check: 60 divided by 12 =  [box=5, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(36\) and \(90\).
   - intro: Prime factorise both, then take the shared primes at their lowest powers.
   - ask: 36 = 2² x 3² and 90 = 2 x 3² x 5. Lowest power of 2 is 2¹ =  [box=2, NO label]
   - ask: Lowest power of 3 is 3² =  [box=9, NO label]
   - intro: Shared primes at their lowest powers: 2¹ and 3².
   - ask: 5 is only in 90, so drop it. HCF = 2 x 9 =  [box=18, NO label]
   - ask: Check: 36 divided by 18 =  [box=2, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(9\) and \(15\).
   - intro: Prime factorise both, then take each prime at its highest power.
   - ask: 9 = 3² and 15 = 3 x 5. The highest power of 3 is 3² =  [box=9, NO label]
   - intro: Every prime at its highest power: 3² and 5.
   - ask: 5 appears only in 15, so bring it in. LCM = 9 x 5 =  [box=45, NO label]
   - ask: Check: 45 divided by 15 =  [box=3, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Write \(180\) as a product of primes in index form. What is the index of \(3\)?
   - intro: Break 180 into primes, then count the 3s.
   - ask: 180 = 2 x 90, and 90 = 2 x 45, so far two 2s. 45 = 3 x ? , so ? =  [box=15, NO label]
   - ask: 15 = 3 x ? , so ? =  [box=5, NO label]
   - intro: Two 3s appear.
   - ask: So 180 = 2² x 3 x 3 x 5. The number of 3s, the index of 3, is  [box=2, NO label]
   - ask: Check: 2² x 3² x 5 = 4 x 9 x 5 =  [box=180, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Two buses leave at 08:00. Bus A every \(12\) mins, Bus B every \(18\) mins. When do they next leave together? (mins after 08:00)
   - intro: They line up at the LCM of 12 and 18. Prime factorise each.
   - ask: 12 = 2² x 3 and 18 = 2 x 3². The highest power of 2 is 2² =  [box=4, NO label]
   - ask: The highest power of 3 is 3² =  [box=9, NO label]
   - intro: That is 2² x 3².
   - ask: LCM = 4 x 9 =  [box=36, NO label]
   - ask: Check: 36 divided by 12 =  [box=3, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Find the HCF of \(56\) and \(84\).
   - intro: Prime factorise both, then take the shared primes at their lowest powers.
   - ask: 56 = 2³ x 7 and 84 = 2² x 3 x 7. Lowest power of 2 is 2² =  [box=4, NO label]
   - intro: Shared primes: 2² and 7.
   - ask: 7 is shared too, and 3 is only in 84, so drop it. HCF = 4 x 7 =  [box=28, NO label]
   - ask: Check: 56 divided by 28 =  [box=2, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Find the LCM of \(6\), \(9\) and \(10\).
   - intro: Prime factorise all three, then take every prime at its highest power.
   - ask: 6 = 2 x 3, 9 = 3², 10 = 2 x 5. The highest power of 2 is 2¹ =  [box=2, NO label]
   - ask: The highest power of 3 is 3² =  [box=9, NO label]
   - intro: Every prime at its highest power: 2, 3² and 5.
   - ask: 5 appears once, in 10. LCM = 2 x 9 x 5 =  [box=90, NO label]
   - ask: Check: 90 divided by 9 =  [box=10, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Given \(A = 2^3 \times 3 \times 5^2\) and \(B = 2^2 \times 3^2 \times 5\), find the HCF.
   - intro: The HCF takes each shared prime at its lower power.
   - ask: Power of 2: lower of 3 and 2 is 2, so 2² =  [box=4, NO label]
   - ask: Power of 3: lower of 1 and 2 is 1, so 3¹ =  [box=3, NO label]
   - ask: Power of 5: lower of 2 and 1 is 1, so 5¹ =  [box=5, NO label]
   - intro: Multiply the lower powers together.
   - ask: HCF = 4 x 3 x 5 =  [box=60, NO label]
   - ask: Check: 60 divided by 5 =  [box=12, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Given \(A = 2^3 \times 3 \times 5^2\) and \(B = 2^2 \times 3^2 \times 5\), find the LCM.
   - intro: The LCM takes each prime at its higher power.
   - ask: Power of 2: higher of 3 and 2 is 3, so 2³ =  [box=8, NO label]
   - ask: Power of 3: higher of 1 and 2 is 2, so 3² =  [box=9, NO label]
   - ask: Power of 5: higher of 2 and 1 is 2, so 5² =  [box=25, NO label]
   - intro: Multiply the higher powers together.
   - ask: LCM = 8 x 9 x 25 =  [box=1800, NO label]
   - ask: Check: 1800 divided by 25 =  [box=72, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: The HCF of two numbers is \(6\) and their LCM is \(120\). One number is \(24\). Find the other.
   - intro: For any two numbers, HCF x LCM equals their product. Use that.
   - ask: Product of the two numbers = 6 x 120 =  [box=720, NO label]
   - intro: Divide the product by the number you already know.
   - ask: One number is 24, so the other = 720 divided by 24 =  [box=30, NO label]
   - ask: Check the HCF of 24 and 30: shared factors 1, 2, 3, 6, biggest is  [box=6, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Three lights flash every \(8\), \(12\) and \(18\) seconds. They flash together at time \(0\). After how many seconds do they next all flash together?
   - intro: They coincide at the LCM of 8, 12 and 18. Prime factorise each.
   - ask: 8 = 2³, 12 = 2² x 3, 18 = 2 x 3². The highest power of 2 is 2³ =  [box=8, NO label]
   - ask: The highest power of 3 is 3² =  [box=9, NO label]
   - intro: That is 2³ x 3².
   - ask: No other primes appear. LCM = 8 x 9 =  [box=72, NO label]
   - ask: Check: 72 divided by 18 =  [box=4, NO label]
