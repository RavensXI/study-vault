# maths-eduqas / number / L03 - Decimals & Rounding

## bronze[0] (input: single_value, main-box unit: (none))
Q: Round \(3.472\) to 1 decimal place.
   - ask: To round to 1 decimal place, keep one digit after the point. In 3.472 that kept digit is  [box=4, NO label]
   - ask: The deciding digit is the next one along:  [box=7, NO label]
   - ask: 7 is 5 or more, so round the kept 4 up. 4 + 1 =  [box=5, NO label]
   - ask: The whole part 3 stays. Written to 1 dp the number is 3.5, so type  [box=3.5, NO label]
   - ask: Check: the halfway value between 3.4 and 3.5 is  [box=3.45, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Round \(7.849\) to 1 decimal place.
   - ask: Keep one digit after the point. In 7.849 the kept digit is  [box=8, NO label]
   - ask: The deciding digit is the next one along:  [box=4, NO label]
   - ask: 4 is less than 5, so the kept 8 stays the same. The kept digit is still  [box=8, NO label]
   - ask: Ignore the digits after it. To 1 dp the number is 7.8, so type  [box=7.8, NO label]
   - ask: Check: the halfway value between 7.8 and 7.9 is  [box=7.85, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Round \(12.365\) to 2 decimal places.
   - ask: Keep two digits after the point. In 12.365 the kept digits are 3 and  [box=6, NO label]
   - ask: The deciding digit is the next one along:  [box=5, NO label]
   - ask: 5 counts as round up, so the kept 6 goes up. 6 + 1 =  [box=7, NO label]
   - ask: The other digits stay. To 2 dp the number is 12.37, so type  [box=12.37, NO label]
   - ask: Check: the halfway value between 12.36 and 12.37 is  [box=12.365, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Round \(0.5482\) to 2 decimal places.
   - ask: Keep two digits after the point. In 0.5482 the kept digits are 5 and  [box=4, NO label]
   - ask: The deciding digit is the next one along:  [box=8, NO label]
   - ask: 8 is 5 or more, so round the kept 4 up. 4 + 1 =  [box=5, NO label]
   - ask: To 2 dp the number is 0.55, so type  [box=0.55, NO label]
   - ask: Check: the halfway value between 0.54 and 0.55 is  [box=0.545, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: \(3.6 + 2.45\)
   - ask: Line up the decimal points. Write 3.6 as 3.60 so both have two decimal places. Add the hundredths: 0 + 5 =  [box=5, NO label]
   - ask: Add the tenths: 6 + 4 =  [box=10, NO label]
   - ask: That is 10 tenths: write 0, carry 1 to the units. Add the units with the carry: 3 + 2 + 1 =  [box=6, NO label]
   - ask: Put it together: 6 units, 0 tenths, 5 hundredths gives 6.05, so type  [box=6.05, NO label]
   - ask: Check: subtract back 6.05 − 2.45 =  [box=3.6, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(5.2 - 1.87\)
   - ask: Line up the decimal points. Write 5.2 as 5.20. Subtract the hundredths: 0 − 7 needs a borrow, so 10 − 7 =  [box=3, NO label]
   - ask: The tenths dropped to 1 after lending. Subtract the tenths: 1 − 8 needs another borrow, so 11 − 8 =  [box=3, NO label]
   - ask: The units dropped to 4 after lending. Subtract the units: 4 − 1 =  [box=3, NO label]
   - ask: Put it together: 3 units, 3 tenths, 3 hundredths gives 3.33, so type  [box=3.33, NO label]
   - ask: Check: add back 3.33 + 1.87 =  [box=5.2, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(0.6 \times 0.3\)
   - ask: Ignore the decimals for now. Multiply the digits: 6 × 3 =  [box=18, NO label]
   - ask: Count the decimal places in the question: 0.6 has 1 and 0.3 has 1, so altogether  [box=2, NO label]
   - ask: Put 2 decimal places into 18: that gives 0.18, so type  [box=0.18, NO label]
   - ask: Check: half of 0.3 is 0.15, and 0.18 sits just above it, a sensible size. Half of 0.3 =  [box=0.15, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(4.8 \div 0.6\)
   - ask: Scale both numbers so the divisor is a whole number. Multiply both by 10. 0.6 × 10 =  [box=6, NO label]
   - ask: Do the same to 4.8: 4.8 × 10 =  [box=48, NO label]
   - ask: Now divide the whole numbers: 48 ÷ 6 =  [box=8, NO label]
   - ask: Check: multiply back 8 × 0.6 =  [box=4.8, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Round \(4567\) to 2 significant figures.
   - ask: The first significant figure is the first non-zero digit. In 4567 that is  [box=4, NO label]
   - ask: Keeping two significant figures, the second kept digit is  [box=5, NO label]
   - ask: The deciding digit is the next one along:  [box=6, NO label]
   - ask: 6 is 5 or more, so round the kept 5 up. 5 + 1 =  [box=6, NO label]
   - ask: Replace the remaining digits with zeros to hold the size. The number is 4600, so type  [box=4600, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Round \(0.003 72\) to 2 significant figures.
   - ask: Leading zeros do not count. The first significant figure is the first non-zero digit:  [box=3, NO label]
   - ask: The second significant figure is the next digit:  [box=7, NO label]
   - ask: The deciding digit is the next one along:  [box=2, NO label]
   - ask: 2 is less than 5, so the kept 7 stays. The last kept digit is still  [box=7, NO label]
   - ask: Keeping the place value, the number is 0.0037, so type  [box=0.0037, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Round \(38 450\) to 3 significant figures.
   - ask: The first three significant figures are 3, 8 and  [box=4, NO label]
   - ask: The deciding digit is the next one along:  [box=5, NO label]
   - ask: 5 counts as round up, so the kept 4 goes up. 4 + 1 =  [box=5, NO label]
   - ask: Replace the remaining digits with zeros. The number is 38500, so type  [box=38500, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(0.24 \times 0.5\)
   - ask: Ignore the decimals for now. Multiply the digits: 24 × 5 =  [box=120, NO label]
   - ask: Count the decimal places: 0.24 has 2 and 0.5 has 1, so altogether  [box=3, NO label]
   - ask: Put 3 decimal places into 120: that is 0.120, which is 0.12. Type  [box=0.12, NO label]
   - ask: Check: 0.5 is a half, so the answer is half of 0.24. Half of 0.24 =  [box=0.12, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(7.2 \div 0.09\)
   - ask: Scale both numbers so the divisor is a whole number. The divisor 0.09 has two decimal places, so multiply both by 100. 0.09 × 100 =  [box=9, NO label]
   - ask: Do the same to 7.2: 7.2 × 100 =  [box=720, NO label]
   - ask: Now divide the whole numbers: 720 ÷ 9 =  [box=80, NO label]
   - ask: Check: multiply back 80 × 0.09 =  [box=7.2, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Estimate \(6.2 \times 4.8\) by rounding each to 1 significant figure.
   - ask: Round 6.2 to 1 significant figure:  [box=6, NO label]
   - ask: Round 4.8 to 1 significant figure:  [box=5, NO label]
   - ask: Multiply the rounded values: 6 × 5 =  [box=30, NO label]
   - ask: Check: the exact value 6.2 × 4.8 = 29.76. Rounded to 1 s.f. that is  [box=30, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Round \(0.06049\) to 3 significant figures.
   - ask: Leading zeros do not count. The first significant figure is  [box=6, NO label]
   - ask: The next two significant figures are 0 and  [box=4, NO label]
   - ask: The deciding digit is the next one along:  [box=9, NO label]
   - ask: 9 is 5 or more, so round the kept 4 up. 4 + 1 =  [box=5, NO label]
   - ask: Keeping the place value, the number is 0.0605, so type  [box=0.0605, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Estimate \(\dfrac{4.87 \times 21.3}{0.52}\) by rounding to 1 significant figure.
   - ask: Round each number to 1 significant figure. 4.87 rounds to  [box=5, NO label]
   - ask: 21.3 rounds to  [box=20, NO label]
   - ask: 0.52 rounds to 0.5. Multiply the top: 5 × 20 =  [box=100, NO label]
   - ask: Dividing by 0.5 is the same as doubling, so 100 ÷ 0.5 =  [box=200, NO label]
   - ask: Check: 200 × 0.5 =  [box=100, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Estimate \(\dfrac{\sqrt{48.6}}{0.21}\). Round 48.6 to the nearest square number and 0.21 to 1 significant figure.
   - ask: Round 48.6 to the nearest square number:  [box=49, NO label]
   - ask: Take the square root: √49 =  [box=7, NO label]
   - ask: Round 0.21 to 1 significant figure:  [box=0.2, NO label]
   - ask: Dividing by 0.2 is the same as multiplying by 5, so 7 ÷ 0.2 =  [box=35, NO label]
   - ask: Check: 35 × 0.2 =  [box=7, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(0.3^2 + 0.4^2\)
   - ask: Square the first: 0.3² means 0.3 × 0.3. Ignoring decimals, 3 × 3 =  [box=9, NO label]
   - ask: With 2 decimal places that is 0.09. Now square the second: 0.4 × 0.4, and 4 × 4 =  [box=16, NO label]
   - ask: With 2 decimal places that is 0.16. Add the two results: 0.09 + 0.16 =  [box=0.25, NO label]
   - ask: Check: 25 hundredths is a quarter. Dividing 25 by 25 gives the top of that quarter: 25 ÷ 25 =  [box=1, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Estimate \(\dfrac{6.2^2}{0.31}\) to 1 significant figure.
   - ask: Round 6.2 to 1 significant figure:  [box=6, NO label]
   - ask: Square it: 6² = 6 × 6 =  [box=36, NO label]
   - ask: Round 0.31 to 1 significant figure:  [box=0.3, NO label]
   - ask: Now 36 ÷ 0.3. Scaling both by 10 gives 360 ÷ 3 =  [box=120, NO label]
   - ask: Check: 120 × 0.3 =  [box=36, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: \(1.2 \times 3.5 \div 0.07\)
   - ask: Work left to right. First 1.2 × 3.5 =  [box=4.2, NO label]
   - ask: Now divide by 0.07. Scale both by 100 so the divisor is a whole number. 0.07 × 100 =  [box=7, NO label]
   - ask: Do the same to 4.2: 4.2 × 100 =  [box=420, NO label]
   - ask: Now divide the whole numbers: 420 ÷ 7 =  [box=60, NO label]
   - ask: Check: multiply back 60 × 0.07 =  [box=4.2, NO label]
