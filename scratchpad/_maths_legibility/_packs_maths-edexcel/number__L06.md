# maths-edexcel / number / L06 - Powers, Roots & Standard Form

## bronze[0] (input: single_value, main-box unit: (none))
Q: Calculate \(3^4\)
   - intro: \(3^4\) means four 3s multiplied together: 3 × 3 × 3 × 3. Build it up one multiply at a time.
   - ask: 3 × 3 =  [box=9, NO label]
   - ask: Times another 3: 9 × 3 =  [box=27, NO label]
   - ask: One more 3: 27 × 3 =  [box=81, NO label]
   - ask: Check a different way. \(3^4 = 9^2\), so 9 × 9 =  [box=81, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Calculate \(\sqrt{196}\)
   - intro: \(\sqrt{196}\) asks what number, times itself, makes 196. It lies between \(\sqrt{100} = 10\) and \(\sqrt{225} = 15\), and 196 ends in 6, so 14 is the strong candidate.
   - ask: Test 14 by squaring. In parts: 14 × 10 =  [box=140, NO label]
   - ask: 14 × 4 =  [box=56, NO label]
   - ask: Add the parts: 140 + 56 =  [box=196, NO label]
   - ask: That is 196, the number under the root, so \(\sqrt{196}\) =  [box=14, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Calculate \(\sqrt[3]{64}\)
   - intro: \(\sqrt[3]{64}\) asks what number cubed (times itself three times) makes 64.
   - ask: Try 4. First 4 × 4 =  [box=16, NO label]
   - ask: Now × 4 again: 16 × 4 =  [box=64, NO label]
   - ask: That equals 64, so the cube root is  [box=4, NO label]

## bronze[3] (input: standard_form, main-box unit: (none))
Q: Write \(56 000\) in standard form
   - intro: Standard form is \(A \times 10^n\) with A between 1 and 10. Start with A.
   - ask: Slide the point left until one digit sits in front. A =  [box=5.6, NO label]
   - ask: Count how many places the point moved from 56 000 to 5.6:  [box=4, NO label]
   - ask: It is a large number, so n is positive. n =  [box=4, NO label]
   - ask: Check by expanding: 5.6 × 10 000 =  [box=56000, NO label]

## bronze[4] (input: standard_form, main-box unit: (none))
Q: Write \(0.0023\) in standard form
   - intro: Standard form is \(A \times 10^n\). Find A first, then the power.
   - ask: Slide the point right until one non-zero digit is in front: 0.0023 becomes  [box=2.3, NO label]
   - ask: Count the places the point moved right:  [box=3, NO label]
   - ask: It is a small number (less than 1), so n is negative. n =  [box=-3, NO label]
   - ask: Check by expanding: 2.3 × 0.001 =  [box=0.0023, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Calculate \(5^3\)
   - intro: \(5^3\) means three 5s multiplied: 5 × 5 × 5.
   - ask: First 5 × 5 =  [box=25, NO label]
   - ask: Now × 5 again: 25 × 5 =  [box=125, NO label]
   - ask: Check the count: how many 5s did we multiply?  [box=3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Calculate \(10^0\)
   - intro: Any non-zero number to the power 0 equals 1. Here is why, using a pattern of dividing by 10.
   - ask: \(10^3 = 1000\). Divide by 10 for \(10^2\): 1000 ÷ 10 =  [box=100, NO label]
   - ask: Again for \(10^1\): 100 ÷ 10 =  [box=10, NO label]
   - ask: Once more for \(10^0\): 10 ÷ 10 =  [box=1, NO label]
   - ask: Each step dropped the power by 1 and divided by 10, so \(10^0\) must be  [box=1, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Calculate \(\sqrt{225}\)
   - intro: \(\sqrt{225}\) asks what number squared makes 225. It sits between \(\sqrt{196} = 14\) and \(\sqrt{256} = 16\), and 225 ends in 5, so try 15.
   - ask: Test 15 by squaring. In parts: 15 × 10 =  [box=150, NO label]
   - ask: 15 × 5 =  [box=75, NO label]
   - ask: Add: 150 + 75 =  [box=225, NO label]
   - ask: That is 225, so \(\sqrt{225}\) =  [box=15, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Write \(7.1 \times 10^5\) as an ordinary number
   - intro: \(7.1 \times 10^5\) means 7.1 with the point moved 5 places to the right. Work out where the digits land.
   - ask: The power is positive, so we move right. How many places?  [box=5, NO label]
   - ask: Start at 7.1 and move the point 1 place right:  [box=71, NO label]
   - ask: Four more places to go, each filled with a zero. After all 5 places the number is  [box=710000, NO label]
   - ask: Check by counting the digits after the leading 7 in 710 000:  [box=5, NO label]

## silver[1] (input: standard_form, main-box unit: (none))
Q: Calculate \((4 \times 10^3) \times (3 \times 10^5)\). Give your answer in standard form.
   - intro: Multiplying in standard form: handle the front numbers and the powers separately.
   - ask: Multiply the fronts: 4 × 3 =  [box=12, NO label]
   - ask: For multiplying, ADD the powers: 3 + 5 =  [box=8, NO label]
   - intro: So far that is 12 × 10⁸, but A = 12 is not between 1 and 10. Adjust it.
   - ask: Write 12 as 1.2 × 10, so the tidy A =  [box=1.2, NO label]
   - ask: Moving one 10 into the power lifts it by 1: 8 + 1 =  [box=9, NO label]
   - intro: Check the size: \(10^3 \times 10^5 = 10^8\), and the 12 adds one more ten, giving \(10^9\). The front 1.2 is between 1 and 10, so \(1.2 \times 10^9\) is correct.

## silver[2] (input: standard_form, main-box unit: (none))
Q: Write \(0.000\,061\) in standard form
   - intro: Standard form \(A \times 10^n\): find A, then the power.
   - ask: Slide the point right to the first non-zero digit: 0.000061 becomes  [box=6.1, NO label]
   - ask: Count the places the point moved right:  [box=5, NO label]
   - ask: It is a small number, so n is negative. n =  [box=-5, NO label]
   - ask: Check by expanding: 6.1 × 0.00001 =  [box=6.1e-05, NO label]

## silver[3] (input: standard_form, main-box unit: (none))
Q: Calculate \((9 \times 10^7) \div (3 \times 10^4)\). Give your answer in standard form.
   - intro: Dividing in standard form: handle the fronts and the powers separately.
   - ask: Divide the fronts: 9 ÷ 3 =  [box=3, NO label]
   - ask: For dividing, SUBTRACT the powers: 7 − 4 =  [box=3, NO label]
   - intro: That gives 3 × 10³. A = 3 is already between 1 and 10, so no adjusting.
   - ask: Write the power: n =  [box=3, NO label]
   - ask: Check by expanding: 3 × 10³ =  [box=3000, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Calculate \(\sqrt[3]{729}\)
   - intro: \(\sqrt[3]{729}\) asks what number cubed makes 729. Nearby cubes are \(8^3 = 512\) and \(10^3 = 1000\), so try 9.
   - ask: Test 9. First 9 × 9 =  [box=81, NO label]
   - ask: Now × 9 again: 81 × 9 =  [box=729, NO label]
   - ask: That equals 729, so the cube root is  [box=9, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Which is larger: \(3 \times 10^4\) or \(9 \times 10^3\)? Enter the larger value.
   - intro: Compare by turning each into an ordinary number, then pick the bigger.
   - ask: Expand the first: 3 × 10⁴ =  [box=30000, NO label]
   - ask: Expand the second: 9 × 10³ =  [box=9000, NO label]
   - ask: Which is bigger, 30 000 or 9 000? Enter the larger value:  [box=30000, NO label]
   - ask: Check the shortcut: the bigger power wins. Of the powers 4 and 3, the larger is  [box=4, NO label]

## silver[6] (input: standard_form, main-box unit: (none))
Q: Write \(2^{10}\) in standard form
   - intro: Two jobs here: work out \(2^{10}\), then write it in standard form.
   - ask: \(2^{10}\) is a well-known power. Build from \(2^5 = 32\): 32 × 32 =  [box=1024, NO label]
   - ask: Now standard form. Slide the point left to one digit in front: 1024 becomes A =  [box=1.024, NO label]
   - ask: Count the places moved from 1024 to 1.024: n =  [box=3, NO label]
   - ask: Check by expanding: 1.024 × 1000 =  [box=1024, NO label]

## gold[0] (input: standard_form, main-box unit: (none))
Q: Calculate \((6 \times 10^4) \times (5 \times 10^{-2})\). Give your answer in standard form.
   - intro: Multiplying in standard form, with a negative power in the mix. Fronts and powers separately.
   - ask: Multiply the fronts: 6 × 5 =  [box=30, NO label]
   - ask: ADD the powers, keeping the signs: 4 + (−2) =  [box=2, NO label]
   - intro: That gives 30 × 10². A = 30 is not between 1 and 10, so adjust.
   - ask: Write 30 as 3 × 10, so the tidy A =  [box=3, NO label]
   - ask: Moving one 10 into the power lifts it by 1: 2 + 1 =  [box=3, NO label]
   - ask: Check by expanding: 3 × 10³ =  [box=3000, NO label]

## gold[1] (input: standard_form, main-box unit: (none))
Q: Calculate \((2.4 \times 10^6) + (5 \times 10^5)\). Give your answer in standard form.
   - intro: Adding in standard form: the powers must match before you add the fronts.
   - ask: Rewrite 5 × 10⁵ as a power of 10⁶. Drop the front to a tenth: 5 becomes  [box=0.5, NO label]
   - ask: Now both are × 10⁶. Add the fronts: 2.4 + 0.5 =  [box=2.9, NO label]
   - ask: A = 2.9 is in range, so the power is unchanged. n =  [box=6, NO label]
   - ask: Check by expanding: 2 400 000 + 500 000 =  [box=2900000, NO label]

## gold[2] (input: standard_form, main-box unit: (none))
Q: Light travels at \(3 \times 10^8\) m/s. How far does it travel in \(5 \times 10^2\) seconds? Give your answer in standard form.
   - intro: Distance = speed × time. Multiply the fronts and add the powers.
   - ask: Multiply the fronts: 3 × 5 =  [box=15, NO label]
   - ask: ADD the powers: 8 + 2 =  [box=10, NO label]
   - intro: That gives 15 × 10¹⁰. A = 15 is too big, so adjust.
   - ask: Write 15 as 1.5 × 10, so the tidy A =  [box=1.5, NO label]
   - ask: Lift the power by 1: 10 + 1 =  [box=11, NO label]
   - intro: Check the size: \(10^8 \times 10^2 = 10^{10}\), and the 15 adds one more ten, giving \(10^{11}\). The front 1.5 is in range, so \(1.5 \times 10^{11}\) m is correct.

## gold[3] (input: standard_form, main-box unit: (none))
Q: Write \(0.36 \times 10^5\) in correct standard form
   - intro: \(0.36 \times 10^5\) is not proper standard form because A must be between 1 and 10. Fix A, then fix the power.
   - ask: 0.36 is too small. Multiply it by 10 to get into range: 0.36 × 10 =  [box=3.6, NO label]
   - intro: We multiplied A by 10, so to keep the value the same the power part must drop by 1.
   - ask: The power falls from 5 to  [box=4, NO label]
   - ask: Check by expanding: 3.6 × 10⁴ =  [box=36000, NO label]

## gold[4] (input: standard_form, main-box unit: (none))
Q: A bacteria colony doubles every hour. Starting at \(5 \times 10^3\), how many after 4 hours? Give your answer in standard form.
   - intro: Doubling every hour for 4 hours means multiplying by 2 four times, that is × 2⁴.
   - ask: Work out 2⁴: 2 × 2 × 2 × 2 =  [box=16, NO label]
   - ask: Write the start as an ordinary number: 5 × 10³ =  [box=5000, NO label]
   - ask: Multiply: 5000 × 16 =  [box=80000, NO label]
   - ask: Standard form A: slide 80 000 to one digit in front. A =  [box=8, NO label]
   - ask: Count the places moved, giving the power n =  [box=4, NO label]
