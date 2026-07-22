# maths-edexcel / number / L03 - Decimals & Rounding

## bronze[0] (input: single_value, main-box unit: (none))
Q: Round \(4.673\) to 1 decimal place
   - intro: Rounding to 1 decimal place means keeping one digit after the point. Two digits decide it: the one you keep and the one right after.
   - ask: The 1st decimal place of 4.673 is  [box=6, NO label]
   - ask: The deciding digit, the next one along, is  [box=7, NO label]
   - intro: 7 is 5 or more, so the digit you keep rounds up.
   - ask: 6 rounds up to  [box=7, NO label]
   - ask: So 4.673 to 1 decimal place is  [box=4.7, NO label]
   - ask: Check: 4.700 − 4.673 =  [box=0.027, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Round \(12.345\) to 2 decimal places
   - intro: Rounding to 2 decimal places keeps two digits after the point. Look at the second decimal place and the digit after it.
   - ask: The 2nd decimal place of 12.345 is  [box=4, NO label]
   - ask: The deciding digit after it is  [box=5, NO label]
   - intro: The decider is exactly 5, and the rule is that 5 rounds up.
   - ask: So the 4 rounds up to  [box=5, NO label]
   - ask: 12.345 to 2 decimal places is  [box=12.35, NO label]
   - ask: Check: 12.350 − 12.345 =  [box=0.005, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Round \(8.049\) to 1 decimal place
   - intro: Rounding to 1 decimal place. Find the first decimal place and the digit right after it.
   - ask: The 1st decimal place of 8.049 is  [box=0, NO label]
   - ask: The deciding digit after it is  [box=4, NO label]
   - intro: 4 is below 5, so the kept digit does not change. The 9 further along does not matter.
   - ask: So the 0 stays as  [box=0, NO label]
   - ask: 8.049 to 1 decimal place is  [box=8, NO label]
   - ask: Check: 8.049 − 8.0 =  [box=0.049, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Round \(3 647\) to the nearest 100
   - intro: Rounding to the nearest 100. The hundreds digit is the one we keep, and the tens digit decides.
   - ask: The hundreds digit of 3647 is  [box=6, NO label]
   - ask: The deciding tens digit is  [box=4, NO label]
   - intro: 4 is below 5, so the hundreds digit stays and the digits after it become 0.
   - ask: The hundreds digit stays as  [box=6, NO label]
   - ask: So 3647 to the nearest 100 is  [box=3600, NO label]
   - ask: Check: 3647 − 3600 =  [box=47, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Round \(0.562\) to 1 significant figure
   - intro: Rounding to 1 significant figure. The first significant figure is the first non-zero digit.
   - ask: The 1st significant figure of 0.562 is  [box=5, NO label]
   - ask: The deciding digit after it is  [box=6, NO label]
   - intro: 6 is 5 or more, so the 5 rounds up.
   - ask: 5 rounds up to  [box=6, NO label]
   - ask: 0.562 to 1 significant figure is  [box=0.6, NO label]
   - ask: Check: 0.6 − 0.562 =  [box=0.038, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(3.2 + 4.58\)
   - intro: Adding decimals: line up the decimal points, then add column by column. Write 3.2 as 3.20 so both have two decimal places.
   - ask: Hundredths: 0 + 8 =  [box=8, NO label]
   - ask: Tenths: 2 + 5 =  [box=7, NO label]
   - intro: Now the units, then put it together.
   - ask: Units: 3 + 4 =  [box=7, NO label]
   - ask: So 3.20 + 4.58 =  [box=7.78, NO label]
   - ask: Check by rounding: 3.2 is about 3, 4.58 is about 5, and 3 + 5 =  [box=8, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(5.7 - 2.35\)
   - intro: Subtracting decimals: line up the points and write 5.7 as 5.70. Work right to left, borrowing when needed.
   - ask: Hundredths: borrow to make 10 − 5 =  [box=5, NO label]
   - ask: Tenths: after lending one, 6 − 3 =  [box=3, NO label]
   - intro: Now the units, then read off the answer.
   - ask: Units: 5 − 2 =  [box=3, NO label]
   - ask: So 5.70 − 2.35 =  [box=3.35, NO label]
   - ask: Check by adding back: 3.35 + 2.35 =  [box=5.7, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(0.3 \times 4\)
   - intro: Multiplying a decimal: ignore the point first, multiply as whole numbers, then put the point back by counting decimal places.
   - ask: Ignore the point: 3 × 4 =  [box=12, NO label]
   - ask: Decimal places in the question: 0.3 has  [box=1, label:' d.p.']
   - intro: So the answer needs 1 decimal place. Put the point back into 12.
   - ask: 12 with 1 decimal place is  [box=1.2, NO label]
   - ask: Check by adding: 0.3 + 0.3 + 0.3 + 0.3 =  [box=1.2, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Round \(0.003 482\) to 2 significant figures
   - intro: Rounding to 2 significant figures. Leading zeros are not significant, so start counting at the first non-zero digit.
   - ask: The 1st significant figure of 0.003482 is  [box=3, NO label]
   - ask: The 2nd significant figure is  [box=4, NO label]
   - ask: The deciding digit after the 4 is  [box=8, NO label]
   - intro: 8 is 5 or more, so the 4 rounds up. The leading zeros stay to hold the place value.
   - ask: 4 rounds up to  [box=5, NO label]
   - ask: 0.003482 to 2 significant figures is  [box=0.0035, NO label]
   - ask: Check: how many significant figures does 0.0035 have?  [box=2, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Round \(45 982\) to 3 significant figures
   - intro: Rounding 45982 to 3 significant figures: keep the first three digits, and the next digit decides. Zeros hold the place value.
   - ask: The first three significant figures are 4, 5 and  [box=9, NO label]
   - ask: The deciding digit after the 9 is  [box=8, NO label]
   - intro: 8 is 5 or more, so the 9 rounds up. That makes 459 carry to 460.
   - ask: 459 rounded up is  [box=460, NO label]
   - ask: Fill the last two places with zeros: 45982 to 3 s.f. is  [box=46000, NO label]
   - ask: Check the size: 46000 − 45982 =  [box=18, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Estimate \(31.2 \times 4.87\)
   - intro: Estimating means rounding each number to 1 significant figure first, then multiplying the simple numbers.
   - ask: 31.2 to 1 significant figure is  [box=30, NO label]
   - ask: 4.87 to 1 significant figure is  [box=5, NO label]
   - intro: Now multiply the rounded numbers.
   - ask: 30 × 5 =  [box=150, NO label]
   - ask: Check with a tighter round: 31 × 5 =  [box=155, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Estimate \(\frac{198}{0.48}\)
   - intro: Estimating a division: round each number to 1 significant figure, then divide.
   - ask: 198 to 1 significant figure is  [box=200, NO label]
   - ask: 0.48 to 1 significant figure is  [box=0.5, NO label]
   - intro: Dividing by 0.5 is the same as multiplying by 2.
   - ask: 200 ÷ 0.5 = 200 × 2 =  [box=400, NO label]
   - ask: Check by scaling: multiply both by 10, then 2000 ÷ 5 =  [box=400, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(2.4 \times 0.3\)
   - intro: Multiplying decimals: multiply as whole numbers first, then count the total decimal places and put the point back.
   - ask: Ignore the points: 24 × 3 =  [box=72, NO label]
   - ask: Total decimal places: 2.4 has 1 and 0.3 has 1, giving  [box=2, NO label]
   - intro: So the answer has 2 decimal places. Put the point back into 72.
   - ask: 72 with 2 decimal places is  [box=0.72, NO label]
   - ask: Check the size: 2.4 is about 2, and 2 × 0.3 =  [box=0.6, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(6.5 \div 0.5\)
   - intro: Dividing by a decimal: make the divisor a whole number by multiplying BOTH numbers by the same amount.
   - ask: Multiply both by 10. The divisor 0.5 becomes  [box=5, NO label]
   - ask: And 6.5 becomes  [box=65, NO label]
   - intro: Now it is a whole-number division.
   - ask: 65 ÷ 5 =  [box=13, NO label]
   - ask: Check by multiplying back: 13 × 0.5 =  [box=6.5, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Estimate \(\sqrt{83}\)
   - intro: Estimating a square root: find the perfect squares either side, then see which one 83 is closest to.
   - ask: The perfect square just below 83 is 81, which is  [box=9, NO label]
   - ask: The perfect square just above 83 is 100, which is  [box=10, NO label]
   - intro: 83 is only just above 81, so the root is just above 9.
   - ask: Since 83 is very close to 81, √83 is about  [box=9, NO label]
   - ask: Check: 9 × 9 =  [box=81, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Estimate \(\frac{6.12 \times 48.7}{0.236}\)
   - intro: Estimating a bigger calculation: round every number to 1 significant figure, then work through it.
   - ask: 6.12 to 1 significant figure is  [box=6, NO label]
   - ask: 48.7 to 1 significant figure is  [box=50, NO label]
   - ask: 0.236 to 1 significant figure is  [box=0.2, NO label]
   - intro: Now the numerator, then divide.
   - ask: The top: 6 × 50 =  [box=300, NO label]
   - intro: Dividing by 0.2 is the same as multiplying by 5.
   - ask: 300 ÷ 0.2 =  [box=1500, NO label]
   - ask: Check by scaling: 3000 ÷ 2 =  [box=1500, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: \(0.07 \times 0.004\)
   - intro: Multiplying small decimals: multiply the non-zero digits, then count every decimal place and put the point back.
   - ask: Ignore the points: 7 × 4 =  [box=28, NO label]
   - ask: Decimal places: 0.07 has 2 and 0.004 has 3, giving a total of  [box=5, NO label]
   - intro: So the answer needs 5 decimal places. Write 28 and count 5 places from the right, filling with zeros.
   - ask: Place the point 5 digits from the right of 28, giving  [box=0.00028, NO label]
   - ask: Check: how many zeros sit after the point before the 28?  [box=3, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(4.56 \div 0.08\)
   - intro: Dividing by a decimal: multiply BOTH numbers by the same power of 10 to make the divisor a whole number.
   - ask: To turn 0.08 into a whole number, multiply both by 100. 0.08 × 100 =  [box=8, NO label]
   - ask: And 4.56 × 100 =  [box=456, NO label]
   - intro: Now divide the whole numbers.
   - ask: 456 ÷ 8 =  [box=57, NO label]
   - ask: Check by multiplying back: 57 × 0.08 =  [box=4.56, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Round \(0.009 950\) to 3 significant figures
   - intro: Rounding to 3 significant figures. Leading zeros are not significant, so start at the first non-zero digit.
   - ask: The three significant figures of 0.009950 are 9, 9 and  [box=5, NO label]
   - ask: The deciding digit after the last 5 is  [box=0, NO label]
   - intro: 0 is below 5, so nothing rounds up. The digits stay as they are.
   - ask: The 5 stays as  [box=5, NO label]
   - ask: So 0.009950 to 3 significant figures is  [box=0.00995, NO label]
   - ask: Check: how many significant figures does 0.00995 have?  [box=3, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Estimate \(\frac{\sqrt{99} + 4.1^2}{1.97}\)
   - intro: Estimating a calculation with a root and a square: round each part to something easy, then work through it in order.
   - ask: √99 is very close to √100, which is  [box=10, NO label]
   - ask: 4.1 squared is about 4 squared, which is  [box=16, NO label]
   - ask: 1.97 to 1 significant figure is  [box=2, NO label]
   - intro: Work out the numerator first, then divide.
   - ask: The top first: 10 + 16 =  [box=26, NO label]
   - ask: Now divide by 2: 26 ÷ 2 =  [box=13, NO label]
   - ask: Check by multiplying back: 13 × 2 =  [box=26, NO label]
