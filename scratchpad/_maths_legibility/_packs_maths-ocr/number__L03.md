# maths-ocr / number / L03 - Decimals & Rounding

## bronze[0] (input: single_value, main-box unit: (none))
Q: Round \(3.847\) to 1 decimal place
   - intro: 1 decimal place means keep one digit after the point, the tenths.
   - ask: The tenths digit of 3.847 is:  [box=8, NO label]
   - ask: The deciding digit, the next one along, is:  [box=4, NO label]
   - ask: 4 is less than 5, so round down and keep the 8. Type 3.847 rounded to 1 dp:  [box=3.8, NO label]
   - intro: Check: 3.847 is 0.047 away from 3.8, less than the 0.05 half-step, so 3.8 is the nearest value.
   - ask: Confirm the answer:  [box=3.8, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Round \(12.653\) to 1 decimal place
   - intro: 1 decimal place keeps one digit after the point, the tenths.
   - ask: The tenths digit of 12.653 is:  [box=6, NO label]
   - ask: The deciding digit, the next one along, is:  [box=5, NO label]
   - ask: 5 is 5 or more, so round the 6 up to 7. Type 12.653 rounded to 1 dp:  [box=12.7, NO label]
   - intro: Check: 12.653 is 0.047 away from 12.7, less than the 0.05 half-step, so 12.7 is the nearest value.
   - ask: Confirm the answer:  [box=12.7, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Round \(0.7249\) to 2 decimal places
   - intro: 2 decimal places means keep two digits after the point.
   - ask: The 2nd decimal (last kept) digit of 0.7249 is:  [box=2, NO label]
   - ask: The deciding digit, the next one along, is:  [box=4, NO label]
   - ask: 4 is less than 5, so round down and keep the 2. Type 0.7249 rounded to 2 dp:  [box=0.72, NO label]
   - intro: Check: 0.7249 is 0.0049 away from 0.72, less than the 0.005 half-step, so 0.72 is the nearest value.
   - ask: Confirm the answer:  [box=0.72, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Round \(5.995\) to 2 decimal places
   - intro: 2 decimal places keeps two digits after the point.
   - ask: The 2nd decimal (last kept) digit of 5.995 is:  [box=9, NO label]
   - ask: The deciding digit, the next one along, is:  [box=5, NO label]
   - ask: 5 rounds up, so 5.99 rolls over. Type 5.995 rounded to 2 dp:  [box=6, NO label]
   - intro: Check: the deciding 5 rounds up, and both nines carry, so 5.99 becomes 6.00.
   - ask: Confirm the answer:  [box=6, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Round \(347\) to 1 significant figure
   - intro: 1 significant figure keeps only the first non-zero digit.
   - ask: The first significant figure of 347 is:  [box=3, NO label]
   - ask: The deciding digit, the next one along, is:  [box=4, NO label]
   - ask: 4 is less than 5, so round down and keep the 3, with zeros holding the place. Type 347 to 1 s.f.:  [box=300, NO label]
   - intro: Check: 347 is 47 away from 300, less than the 50 half-step, so 300 is the nearest value.
   - ask: Confirm the answer:  [box=300, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Round \(6.851\) to 2 significant figures
   - intro: 2 significant figures keeps the first two non-zero digits.
   - ask: The first two significant figures of 6.851 are 6 and 8. The deciding digit (next) is:  [box=5, NO label]
   - ask: 5 is 5 or more, so round the 8 up to:  [box=9, NO label]
   - ask: Type 6.851 rounded to 2 s.f.:  [box=6.9, NO label]
   - intro: Check: 6.851 is 0.049 away from 6.9, less than the 0.05 half-step, so 6.9 is the nearest value.
   - ask: Confirm the answer:  [box=6.9, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Round \(0.0638\) to 1 significant figure
   - intro: Leading zeros are not significant. Significant figures start at the first non-zero digit.
   - ask: The first significant figure of 0.0638 is:  [box=6, NO label]
   - ask: The deciding digit, the next one along, is:  [box=3, NO label]
   - ask: 3 is less than 5, so round down and keep the 6. Type 0.0638 to 1 s.f.:  [box=0.06, NO label]
   - intro: Check: 0.0638 is 0.0038 away from 0.06, less than the 0.005 half-step, so 0.06 is the nearest value.
   - ask: Confirm the answer:  [box=0.06, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Calculate \(3.4 + 2.75\)
   - intro: Line up the decimal points and pad 3.4 as 3.40 so both have two decimals.
   - ask: Hundredths column: 0 + 5 =  [box=5, NO label]
   - ask: Tenths column: 4 + 7 =  [box=11, NO label]
   - ask: Units column: 3 + 2 + the carried 1 =  [box=6, NO label]
   - intro: So far: units 6, tenths 1, hundredths 5.
   - ask: Put it together, tenths and hundredths after the point. Type 3.4 + 2.75:  [box=6.15, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Round \(45672\) to 2 significant figures
   - intro: 2 significant figures keeps the first two non-zero digits, then zeros hold the place.
   - ask: The first two significant figures of 45672 are 4 and 5. The deciding digit (next) is:  [box=6, NO label]
   - ask: 6 is 5 or more, so round 45 up to:  [box=46, NO label]
   - ask: Replace the remaining digits with zeros. Type 45672 to 2 s.f.:  [box=46000, NO label]
   - intro: Check: 45672 is 328 away from 46000, less than the 500 half-step, so 46000 is the nearest value.
   - ask: Confirm the answer:  [box=46000, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Round \(0.003457\) to 2 significant figures
   - intro: Leading zeros are not significant. Significant figures start at the first non-zero digit.
   - ask: The first significant figure of 0.003457 is:  [box=3, NO label]
   - ask: Keep 2 s.f.: 3 and 4. The deciding digit (next) is:  [box=5, NO label]
   - ask: 5 is 5 or more, so round the 4 up to 5. Type 0.003457 to 2 s.f.:  [box=0.0035, NO label]
   - intro: Check: 0.003457 is 0.000043 away from 0.0035, less than the 0.00005 half-step, so 0.0035 is the nearest value.
   - ask: Confirm the answer:  [box=0.0035, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Estimate \(4.8 \times 21.3\)
   - intro: Estimate by rounding each number to 1 significant figure.
   - ask: 4.8 to 1 s.f. is:  [box=5, NO label]
   - ask: 21.3 to 1 s.f. is:  [box=20, NO label]
   - ask: Now multiply the rounded values: 5 × 20 =  [box=100, NO label]
   - ask: Check the size: the true value is about 102, so type the estimate 100:  [box=100, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Estimate \(\frac{197}{0.48}\)
   - intro: Estimate by rounding each number to 1 significant figure.
   - ask: 197 to 1 s.f. is:  [box=200, NO label]
   - ask: 0.48 to 1 s.f. is:  [box=0.5, NO label]
   - ask: Now divide: 200 ÷ 0.5. Dividing by 0.5 doubles the number, so 200 ÷ 0.5 =  [box=400, NO label]
   - ask: Check: 400 × 0.5 = 200, matching the top. Type the estimate 400:  [box=400, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Calculate \(4.7 \times 0.3\)
   - intro: First multiply as whole numbers, ignoring the decimal points.
   - ask: 47 × 3 =  [box=141, NO label]
   - ask: Count the decimal places: 4.7 has 1, 0.3 has 1, so the total is:  [box=2, NO label]
   - ask: Put the point 2 places from the right of 141. Type 4.7 × 0.3:  [box=1.41, NO label]
   - ask: Check the size: 4.7 is near 5, and 5 × 0.3 = 1.5, close to 1.41. Type 1.41:  [box=1.41, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Calculate \(8.4 \div 0.6\)
   - intro: Make the divisor a whole number by multiplying both numbers by 10.
   - ask: 8.4 × 10 =  [box=84, NO label]
   - ask: 0.6 × 10 =  [box=6, NO label]
   - ask: Now divide whole numbers: 84 ÷ 6 =  [box=14, NO label]
   - ask: Check: 14 × 0.6 = 8.4, matching the start. Type 14:  [box=14, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Estimate \(\sqrt{53}\) to the nearest integer
   - intro: Find the two square numbers that 53 sits between.
   - ask: 7² =  [box=49, NO label]
   - ask: 8² =  [box=64, NO label]
   - ask: 53 lies between 49 and 64. The gap down to 49 is 53 − 49 =  [box=4, NO label]
   - ask: The gap up to 64 is 64 − 53 =  [box=11, NO label]
   - ask: 4 is less than 11, so 53 is nearer 49. The nearest integer to √53 is:  [box=7, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Estimate \(\frac{6.2^2 + 3.8}{0.49}\)
   - intro: Estimate every part to 1 significant figure, including the square.
   - ask: 6.2 to 1 s.f. is 6, and 6² =  [box=36, NO label]
   - ask: 3.8 to 1 s.f. is:  [box=4, NO label]
   - ask: So the top is about 36 + 4 =  [box=40, NO label]
   - ask: 0.49 to 1 s.f. is:  [box=0.5, NO label]
   - ask: Now divide: 40 ÷ 0.5. Dividing by 0.5 doubles it, so 40 ÷ 0.5 =  [box=80, NO label]
   - ask: Check: 80 × 0.5 = 40, matching the top. Type the estimate 80:  [box=80, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Calculate \(0.24 \times 0.15\)
   - intro: First multiply as whole numbers, ignoring the decimal points.
   - ask: 24 × 15 =  [box=360, NO label]
   - ask: Count the decimal places: 0.24 has 2, 0.15 has 2, so the total is:  [box=4, NO label]
   - ask: Put the point 4 places from the right of 360, using a leading zero. Type 0.24 × 0.15:  [box=0.036, NO label]
   - ask: Check the size: 0.24 and 0.15 are both under 1, so the product is small. Type 0.036:  [box=0.036, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Round \(0.9955\) to 2 significant figures
   - intro: 2 significant figures keeps the first two non-zero digits.
   - ask: The first two significant figures of 0.9955 are 9 and 9. The deciding digit (next) is:  [box=5, NO label]
   - ask: 5 rounds up, so 99 rolls over to 100. Type 0.9955 rounded to 2 s.f.:  [box=1, NO label]
   - ask: Check: 0.9955 is just under 1, and rounding pushes it up to 1.0. Type 1:  [box=1, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Estimate \(\frac{398 \times 0.52}{19.7}\)
   - intro: Estimate every number to 1 significant figure.
   - ask: 398 to 1 s.f. is:  [box=400, NO label]
   - ask: 0.52 to 1 s.f. is:  [box=0.5, NO label]
   - ask: So the top is about 400 × 0.5 =  [box=200, NO label]
   - ask: 19.7 to 1 s.f. is:  [box=20, NO label]
   - ask: Now divide: 200 ÷ 20 =  [box=10, NO label]
   - ask: Check: 10 × 20 = 200, matching the top. Type the estimate 10:  [box=10, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Calculate \(2.56 \div 0.08\)
   - intro: Make the divisor a whole number by multiplying both numbers by 100.
   - ask: 2.56 × 100 =  [box=256, NO label]
   - ask: 0.08 × 100 =  [box=8, NO label]
   - ask: Now divide whole numbers: 256 ÷ 8 =  [box=32, NO label]
   - ask: Check: 32 × 0.08 = 2.56, matching the start. Type 32:  [box=32, NO label]
