# maths-ocr / algebra / L11 - Inequalities

## bronze[0] (input: single_value, main-box unit: (none))
Q: Solve \(x + 3 > 7\). What is the smallest integer solution?
   - intro: Solve it just like an equation. Subtract 3 from both sides.
   - ask: 7 − 3 =  [box=4, NO label]
   - intro: So x > 4. The answer is every number above 4.
   - ask: x > 4 does not include 4, so the smallest whole number is  [box=5, NO label]
   - ask: Check: 5 + 3 =  [box=8, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Solve \(2x - 1 < 9\). What is the largest integer solution?
   - intro: Solve it like an equation. Add 1 to both sides.
   - ask: 9 + 1 =  [box=10, NO label]
   - intro: So 2x < 10. Divide both sides by 2.
   - ask: 10 ÷ 2 =  [box=5, NO label]
   - intro: So x < 5, every number below 5.
   - ask: x < 5 does not include 5, so the largest whole number is  [box=4, NO label]
   - ask: Check: 2 × 4 − 1 =  [box=7, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Solve \(3x \geq 9\). What is the smallest solution?
   - intro: Solve it like an equation. Divide both sides by 3.
   - ask: 9 ÷ 3 =  [box=3, NO label]
   - intro: So x ≥ 3. The ≥ sign includes 3 itself, so the smallest value x can take is 3.
   - ask: Smallest solution: x =  [box=3, NO label]
   - ask: Check by putting x = 3 in: 3 × 3 =  [box=9, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: −3−2−101234567Closed circle = included, open circle = not included How many integers satisfy \(-2 \leq x < 6\)?
   - intro: List the integers from the low end up to the high end, watching which ends are included.
   - ask: −2 has ≤ so it IS included, and 6 has < so it is NOT. The largest integer allowed is  [box=5, NO label]
   - intro: So the integers run from −2 up to 5.
   - ask: Count −2, −1, 0, 1, 2, 3, 4, 5. How many?  [box=8, NO label]
   - ask: Quick check using 5 − (−2) + 1 =  [box=8, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Solve \(5x + 4 \leq 49\). What is the largest integer solution?
   - intro: Solve it like an equation. Subtract 4 from both sides.
   - ask: 49 − 4 =  [box=45, NO label]
   - intro: So 5x ≤ 45. Divide both sides by 5.
   - ask: 45 ÷ 5 =  [box=9, NO label]
   - intro: So x ≤ 9. The ≤ sign includes 9.
   - ask: Largest integer value of x =  [box=9, NO label]
   - ask: Check: 5 × 9 + 4 =  [box=49, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Solve \(\frac{x}{2} > 3\). What is the smallest integer?
   - intro: Solve it like an equation. Multiply both sides by 2.
   - ask: 3 × 2 =  [box=6, NO label]
   - intro: So x > 6, every number above 6.
   - ask: x > 6 does not include 6, so the smallest whole number is  [box=7, NO label]
   - ask: Check: 7 ÷ 2 =  [box=3.5, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: 0123456789Open circles = ends not included How many integers satisfy \(1 < x < 8\)?
   - intro: Both ends use strict < , so neither 1 nor 8 is included. List what is left.
   - ask: The smallest integer bigger than 1 is  [box=2, NO label]
   - intro: The largest integer below 8 is 7. So the list runs 2 to 7.
   - ask: Count 2, 3, 4, 5, 6, 7. How many?  [box=6, NO label]
   - ask: Quick check using 7 − 2 + 1 =  [box=6, NO label]

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: Solve \(4x - 3 > 5\). What is \(x\)?

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: Solve \(-2x > 6\). What is \(x\)?

## silver[1] (input: single_value, main-box unit: (none))
Q: Solve \(1 \leq 2x - 3 < 9\). What is the largest integer?
   - intro: This is a three-part inequality. Do every step to all three parts. First add 3 to all three.
   - ask: On the left: 1 + 3 =  [box=4, NO label]
   - ask: On the right: 9 + 3 =  [box=12, NO label]
   - intro: So 4 ≤ 2x < 12. Now divide all three parts by 2.
   - ask: Left: 4 ÷ 2 =  [box=2, NO label]
   - ask: Right: 12 ÷ 2 =  [box=6, NO label]
   - intro: So 2 ≤ x < 6. The right end uses < , so 6 is not included.
   - ask: Largest integer value of x =  [box=5, NO label]
   - ask: Check x = 5: 2 × 5 − 3 =  [box=7, NO label]

## silver[2] (input: multiple_choice, main-box unit: (none))
Q: Solve \(3(x - 2) < x + 4\). What is \(x\)?

## silver[3] (input: single_value, main-box unit: (none))
Q: How many integers satisfy \(-3 < 2x + 1 \leq 11\)?
   - intro: Do every step to all three parts. First subtract 1 from all three.
   - ask: Left: −3 − 1 =  [box=-4, NO label]
   - ask: Right: 11 − 1 =  [box=10, NO label]
   - intro: So −4 < 2x ≤ 10. Now divide all three parts by 2.
   - ask: Left: −4 ÷ 2 =  [box=-2, NO label]
   - ask: Right: 10 ÷ 2 =  [box=5, NO label]
   - intro: So −2 < x ≤ 5. The left uses < (so −2 is out); the right uses ≤ (so 5 is in). Integers run −1 to 5.
   - ask: Count −1, 0, 1, 2, 3, 4, 5. How many?  [box=7, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: Solve \(5 - 3x \geq 14\). What is \(x\)?

## silver[5] (input: single_value, main-box unit: (none))
Q: Solve \(\frac{x+1}{3} \leq 4\). What is the largest integer?
   - intro: Solve it like an equation. Multiply both sides by 3 to clear the fraction.
   - ask: 4 × 3 =  [box=12, NO label]
   - intro: So x + 1 ≤ 12. Subtract 1 from both sides.
   - ask: 12 − 1 =  [box=11, NO label]
   - intro: So x ≤ 11. The ≤ sign includes 11.
   - ask: Largest integer value of x =  [box=11, NO label]
   - ask: Check: (11 + 1) ÷ 3 =  [box=4, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: List the integer solutions of \(-1 \leq 3x - 4 < 8\). How many are there?
   - intro: Do every step to all three parts. First add 4 to all three.
   - ask: Left: −1 + 4 =  [box=3, NO label]
   - ask: Right: 8 + 4 =  [box=12, NO label]
   - intro: So 3 ≤ 3x < 12. Now divide all three parts by 3.
   - ask: Left: 3 ÷ 3 =  [box=1, NO label]
   - ask: Right: 12 ÷ 3 =  [box=4, NO label]
   - intro: So 1 ≤ x < 4. The left ≤ includes 1; the right < excludes 4. Integers: 1, 2, 3.
   - ask: How many integers is that?  [box=3, NO label]

## gold[0] (input: multiple_choice, main-box unit: (none))
Q: Solve \(2x + 3 > x - 1\) AND \(3x - 4 < 11\). What is the range of \(x\)?

## gold[1] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 < 16\). How many integer solutions?
   - intro: For x² < 16, take the square root of 16 to find the boundary.
   - ask: √16 =  [box=4, NO label]
   - intro: So the solution is the band −4 < x < 4 (both ends strict, so 4 and −4 are out).
   - ask: The largest integer inside is  [box=3, NO label]
   - intro: By symmetry the smallest is −3. Integers run −3 to 3.
   - ask: Count −3, −2, −1, 0, 1, 2, 3. How many?  [box=7, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Solve \(\frac{2x-1}{3} \geq \frac{x+2}{2}\). What is the smallest integer?
   - intro: Clear both fractions by multiplying every term by 6, the common denominator.
   - ask: The left, (2x − 1)/3, times 6 is 2 lots of (2x − 1). The number in front of x is 2 × 2 =  [box=4, NO label]
   - ask: The right, (x + 2)/2, times 6 is 3 lots of (x + 2). The number in front of x is 3 × 1 =  [box=3, NO label]
   - intro: So 4x − 2 ≥ 3x + 6. Subtract 3x from both sides.
   - ask: 4x − 3x =  [box=1, label:'x']
   - intro: So x − 2 ≥ 6. Add 2 to both sides.
   - ask: 6 + 2 =  [box=8, NO label]
   - intro: So x ≥ 8. The ≥ includes 8, so the smallest value is 8.
   - ask: Check x = 8: left (2×8 − 1)/3 = 15/3 = 5, right (8 + 2)/2 =  [box=5, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Find the integer values of \(n\) where \(n^2 + 2n - 15 \leq 0\). How many are there?
   - intro: Factorise the quadratic. Find two numbers that multiply to −15 and add to +2.
   - ask: Those numbers are +5 and −3. The larger root comes from n − 3 = 0, giving n =  [box=3, NO label]
   - ask: The other root comes from n + 5 = 0, giving n =  [box=-5, NO label]
   - intro: The parabola opens upward, so it is ≤ 0 BETWEEN the roots: −5 ≤ n ≤ 3. Both ends use ≤, so both are included.
   - ask: The integers run from −5 to 3. Using 3 − (−5) + 1 =  [box=9, NO label]
   - ask: Check the top root n = 3: 3² + 2 × 3 − 15 = 9 + 6 − 15 =  [box=0, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Solve \(-5 < 3 - 2x \leq 7\). What is the smallest integer?
   - intro: Do every step to all three parts. First subtract 3 from all three.
   - ask: Left: −5 − 3 =  [box=-8, NO label]
   - ask: Right: 7 − 3 =  [box=4, NO label]
   - intro: So −8 flips both signs.
   - ask: Left becomes: −8 ÷ (−2) =  [box=4, NO label]
   - ask: Right becomes: 4 ÷ (−2) =  [box=-2, NO label]
   - intro: After flipping, the chain reads 4 > x ≥ −2, i.e. −2 ≤ x < 4. The ≤ end means −2 is included.
   - ask: Smallest integer value of x =  [box=-2, NO label]
