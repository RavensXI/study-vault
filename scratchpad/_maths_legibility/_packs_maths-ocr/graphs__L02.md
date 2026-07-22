# maths-ocr / graphs / L02 - Equation of a Line

## bronze[0] (input: multiple_choice, main-box unit: (none))
Q: A line has gradient 5 and y-intercept 3. Write the equation.

## bronze[1] (input: single_value, main-box unit: (none))
Q: A line has equation \(y = 7x - 4\). What is the gradient?
   - intro: In \(y = mx + c\), the gradient \(m\) is the number multiplying \(x\).
   - ask: the number in front of x here is  [box=7, NO label]
   - intro: That number IS the gradient. The −4 is the y-intercept, not part of the gradient.
   - ask: so the gradient m =  [box=7, NO label]
   - ask: check: at x = 0, y = −4; at x = 1, y = 3. The rise for 1 across is 3 − (−4) =  [box=7, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: A line has equation \(y = -2x + 6\). What is the y-intercept?
   - intro: The y-intercept is \(c\), the constant added at the end of \(y = mx + c\).
   - ask: the constant at the end here is  [box=6, NO label]
   - intro: The y-intercept is where the line crosses the y-axis, at \(x = 0\).
   - ask: put x = 0: y = −2×0 + 6 =  [box=6, NO label]
   - ask: so the line crosses the y-axis at (0, 6). The y-intercept is  [box=6, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: A line passes through \((0, -2)\) with gradient 3. What is the equation? Give the value of \(c\).
   - intro: The point \((0, -2)\) is on the y-axis, because its x-value is 0.
   - ask: the y-value where x = 0 is  [box=-2, NO label]
   - intro: The y-intercept c is exactly that y-value.
   - ask: so c =  [box=-2, NO label]
   - ask: check the equation y = 3x − 2 at x = 0: y = 3×0 − 2 =  [box=-2, NO label]

## bronze[4] (input: multiple_choice, main-box unit: (none))
Q: Which line is parallel to \(y = 4x + 1\)?

## bronze[5] (input: single_value, main-box unit: (none))
Q: A line has equation \(y = -x + 5\). What is the gradient?
   - intro: \(y = -x + 5\) is the same as \(y = -1x + 5\).
   - ask: the number in front of x is  [box=-1, NO label]
   - intro: That number IS the gradient.
   - ask: so the gradient m =  [box=-1, NO label]
   - ask: check: at x = 0, y = 5; at x = 1, y = 4. The rise for 1 across is 4 − 5 =  [box=-1, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: The equation of a line is \(y = \frac{1}{2}x + 4\). What is \(y\) when \(x = 8\)?
   - intro: To find \(y\), substitute \(x = 8\) into \(y = \frac{1}{2}x + 4\).
   - ask: the x part: ½×8 =  [box=4, NO label]
   - intro: Now add the y-intercept, 4.
   - ask: y = 4 + 4 =  [box=8, NO label]
   - ask: check: ½×8 + 4 =  [box=8, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Find the gradient of the line through \((0, 1)\) and \((4, 9)\).
   - intro: Gradient is (change in y) over (change in x). Use \((0, 1)\) and \((4, 9)\).
   - ask: change in y = 9 − 1 =  [box=8, NO label]
   - ask: change in x = 4 − 0 =  [box=4, NO label]
   - intro: Now divide to get the gradient.
   - ask: m = 8 ÷ 4 =  [box=2, NO label]
   - ask: check: from (0, 1), up 2 per 1 across, at x = 4 gives y = 1 + 2×4 =  [box=9, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((1, 5)\) and \((3, 11)\). What is the y-intercept \(c\)?
   - intro: Two points and no gradient, so find \(m\) first: (change in y) over (change in x).
   - ask: change in y = 11 − 5 =  [box=6, NO label]
   - ask: change in x = 3 − 1 =  [box=2, NO label]
   - ask: m = 6 ÷ 2 =  [box=3, NO label]
   - intro: Substitute \((1, 5)\) into \(y = 3x + c\). The x part is 3×1 = 3, so \(5 = 3 + c\):
   - ask: c = 5 − 3 =  [box=2, NO label]
   - ask: check with (3, 11): 3×3 + 2 =  [box=11, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: A line has equation \(3y = 9x - 6\). What is the gradient?
   - intro: The equation is not in \(y = mx + c\) form. Divide every term by 3.
   - ask: 9x ÷ 3 gives the x coefficient: 9 ÷ 3 =  [box=3, NO label]
   - ask: −6 ÷ 3 =  [box=-2, NO label]
   - intro: So \(y = 3x - 2\). Now read the gradient.
   - ask: the number in front of x is  [box=3, NO label]
   - ask: it is 3, not the original 9. The gradient is  [box=3, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Line A: \(y = 2x + 5\). Line B is parallel to A and passes through \((0, -3)\). What is the equation of Line B? Give \(c\).
   - intro: Parallel lines share the same gradient, so Line B also has gradient 2.
   - ask: the gradient of Line B is  [box=2, NO label]
   - intro: Line B passes through \((0, -3)\), which is on the y-axis.
   - ask: the y-value where x = 0 gives c =  [box=-3, NO label]
   - ask: check the equation y = 2x − 3 at x = 0: y = 2×0 − 3 =  [box=-3, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((2, 1)\) and \((5, 13)\). What is the gradient?
   - intro: Gradient is (change in y) over (change in x). Use \((2, 1)\) and \((5, 13)\).
   - ask: change in y = 13 − 1 =  [box=12, NO label]
   - ask: change in x = 5 − 2 =  [box=3, NO label]
   - intro: Now divide to get the gradient.
   - ask: m = 12 ÷ 3 =  [box=4, NO label]
   - ask: check: from (2, 1), up 4 per 1 across, at x = 5 gives y = 1 + 4×3 =  [box=13, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: The line \(y = mx + 2\) passes through \((3, -10)\). Find \(m\).
   - intro: Substitute \((3, -10)\) into \(y = mx + 2\): \(-10 = 3m + 2\).
   - ask: take 2 off both sides: 3m = −10 − 2 =  [box=-12, NO label]
   - intro: Now divide by 3.
   - ask: m = −12 ÷ 3 =  [box=-4, NO label]
   - ask: check: 3×(−4) + 2 =  [box=-10, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: A line has equation \(4x + 2y = 10\). What is the gradient?
   - intro: Rearrange to \(y = mx + c\). Move \(4x\) across: \(2y = -4x + 10\).
   - ask: the x coefficient is now  [box=-4, NO label]
   - intro: Divide every term by 2 to make y the subject.
   - ask: −4 ÷ 2 gives the gradient:  [box=-2, NO label]
   - ask: so \(y = -2x + 5\). Check the y-intercept at x = 0: y =  [box=5, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Two lines are perpendicular. One has gradient 4. What is the gradient of the other? Give as a decimal.
   - intro: Perpendicular gradients are negative reciprocals: flip the number and change the sign.
   - ask: flip 4 (that is 1 ÷ 4) to a decimal:  [box=0.25, label:'(a decimal)']
   - intro: Now change the sign to make it negative.
   - ask: the perpendicular gradient is −(0.25) =  [box=-0.25, NO label]
   - ask: check: perpendicular gradients multiply to −1, so 4 × (−0.25) =  [box=-1, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((-1, 8)\) and \((3, -4)\). What is the value of \(c\)?
   - intro: Two points, no gradient given, so find \(m\) first: (change in y) over (change in x).
   - ask: change in y = −4 − 8 =  [box=-12, NO label]
   - ask: change in x = 3 − (−1) =  [box=4, NO label]
   - ask: m = −12 ÷ 4 =  [box=-3, NO label]
   - intro: Substitute \((-1, 8)\) into \(y = -3x + c\). The x part is −3×(−1) = 3, so \(8 = 3 + c\):
   - ask: c = 8 − 3 =  [box=5, NO label]
   - ask: check with (3, −4): −3×3 + 5 =  [box=-4, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Line P: \(y = 5x - 2\). Find the gradient of a line perpendicular to P. Give as a decimal.
   - intro: The gradient of P is 5. Perpendicular gradients are negative reciprocals: flip and change sign.
   - ask: flip 5 (that is 1 ÷ 5) to a decimal:  [box=0.2, label:'(a decimal)']
   - intro: Now change the sign to negative.
   - ask: the perpendicular gradient is −(0.2) =  [box=-0.2, NO label]
   - ask: check: 5 × (−0.2) =  [box=-1, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The line \(x + 4y = 12\) is perpendicular to \(y = mx + 1\). Find \(m\).
   - intro: First find the gradient of \(x + 4y = 12\). Make y the subject: \(4y = -x + 12\), then divide by 4.
   - ask: the x coefficient is −1 ÷ 4 =  [box=-0.25, NO label]
   - intro: So the first line has gradient −0.25 (negative one quarter). Perpendicular gradients are negative reciprocals: flip and change sign.
   - ask: flip negative one quarter to get  [box=-4, NO label]
   - intro: Now change the sign to get m.
   - ask: m = −(−4) =  [box=4, NO label]
   - ask: check: gradient −0.25 times m must equal −1, so −0.25 × 4 =  [box=-1, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Show the lines \(y = 2x + 3\) and \(y = 2x - 5\) are parallel. What is their common gradient?
   - intro: Read the gradient of each line: it is the number in front of \(x\).
   - ask: the gradient of \(y = 2x + 3\) is  [box=2, NO label]
   - intro: Now the second line.
   - ask: the gradient of \(y = 2x - 5\) is  [box=2, NO label]
   - ask: both gradients are equal, so the lines are parallel. The common gradient is  [box=2, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: (2, 0)(0, −6)xy0A line passes through \((2, 0)\) and \((0, -6)\). Find the gradient.
   - intro: Gradient is (change in y) over (change in x). Take the points in order, from \((2, 0)\) to \((0, -6)\).
   - ask: change in y = −6 − 0 =  [box=-6, NO label]
   - ask: change in x = 0 − 2 =  [box=-2, NO label]
   - intro: Now divide. A negative divided by a negative is positive.
   - ask: m = −6 ÷ (−2) =  [box=3, NO label]
   - ask: check: from (0, −6), up 3 per 1 across, at x = 2 gives y = −6 + 3×2 =  [box=0, NO label]
