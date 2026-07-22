# maths-edexcel / graphs / L02 - Equation of a Line

## bronze[0] (input: single_value, main-box unit: (none))
Q: A line has gradient 3 and passes through \((2, 10)\). Find \(c\).
   - intro: The gradient is given, \(m = 3\), so the line is \(y = 3x + c\). Substitute the point \((2, 10)\):
   - ask: 3 × 2 =  [box=6, NO label]
   - intro: So 10 = 6 + c.
   - ask: 10 − 6 = c, so c =  [box=4, NO label]
   - ask: Check: 3 × 2 + 4 =  [box=10, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A line has gradient 4 and passes through \((1, 6)\). Find the value of \(c\).
   - intro: The gradient is given, \(m = 4\), so the line is \(y = 4x + c\). Substitute the point \((1, 6)\):
   - ask: 4 × 1 =  [box=4, NO label]
   - intro: So 6 = 4 + c.
   - ask: 6 − 4 = c, so c =  [box=2, NO label]
   - ask: Check: 4 × 1 + 2 =  [box=6, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: A line has gradient 2 and passes through \((2, 1)\). Find the y-intercept \(c\).
   - intro: The gradient is given, \(m = 2\), so the line is \(y = 2x + c\). Substitute the point \((2, 1)\):
   - ask: 2 × 2 =  [box=4, NO label]
   - intro: So 1 = 4 + c.
   - ask: 1 − 4 = c, so c =  [box=-3, NO label]
   - ask: Check: 2 × 2 + (−3) =  [box=1, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: A line has gradient 1 and passes through \((5, 8)\). Find \(c\).
   - intro: The gradient is given, \(m = 1\), so the line is \(y = x + c\). Substitute the point \((5, 8)\):
   - ask: 1 × 5 =  [box=5, NO label]
   - intro: So 8 = 5 + c.
   - ask: 8 − 5 = c, so c =  [box=3, NO label]
   - ask: Check: 1 × 5 + 3 =  [box=8, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Find the gradient of the line with equation \(y = 7x - 2\).
   - intro: In \(y = mx + c\) the gradient sits with the x and the intercept sits alone. Line up \(y = 7x - 2\) against \(y = mx + c\).
   - ask: The number with x is the gradient. m =  [box=7, NO label]
   - ask: The number on its own is the intercept. c =  [box=-2, NO label]
   - ask: At x = 1: 7 × 1 − 2 =  [box=5, NO label]
   - ask: From x = 0 (y = −2) to x = 1 (y = 5), y climbs 5 − (−2) =  [box=7, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: A line has gradient \(-1\) and passes through \((2, 3)\). Find \(c\).
   - intro: The gradient is given, \(m = -1\), so the line is \(y = -x + c\). Substitute the point \((2, 3)\):
   - ask: −1 × 2 =  [box=-2, NO label]
   - intro: So 3 = −2 + c.
   - ask: 3 − (−2) = c, so c =  [box=5, NO label]
   - ask: Check: −1 × 2 + 5 =  [box=3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: A line has gradient \(\frac{1}{2}\) and passes through \((4, 8)\). Find \(c\).
   - intro: The gradient is given, \(m = \frac{1}{2}\), so the line is \(y = \frac{1}{2}x + c\). Substitute the point \((4, 8)\):
   - ask: ½ × 4 =  [box=2, NO label]
   - intro: So 8 = 2 + c.
   - ask: 8 − 2 = c, so c =  [box=6, NO label]
   - ask: Check: ½ × 4 + 6 =  [box=8, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: What is the y-intercept of the line \(y = -5x + 12\)?
   - intro: In \(y = mx + c\) the intercept c sits alone and the gradient m sits with x. Line up \(y = -5x + 12\) against \(y = mx + c\).
   - ask: The number with x is the gradient. m =  [box=-5, NO label]
   - ask: The number on its own is the intercept. c =  [box=12, NO label]
   - ask: The y-intercept is where x = 0. At x = 0: −5 × 0 =  [box=0, NO label]
   - ask: So y = 0 + 12 =  [box=12, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((1, 3)\) and \((3, 9)\). What is \(c\)?
   - intro: No gradient given, so find it first: rise over run, \((y_2 - y_1) \div (x_2 - x_1)\), using \((1, 3)\) and \((3, 9)\).
   - ask: top: 9 − 3 =  [box=6, NO label]
   - ask: bottom: 3 − 1 =  [box=2, NO label]
   - ask: m = 6 ÷ 2 =  [box=3, NO label]
   - intro: Now substitute \((1, 3)\) into \(y = 3x + c\):
   - ask: 3 − 3 × 1 = c, so c =  [box=0, NO label]
   - ask: Check the other point: 3 × 3 + 0 =  [box=9, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((2, 1)\) and \((5, 10)\). What is \(c\)?
   - intro: Find the gradient first from \((2, 1)\) and \((5, 10)\): rise over run.
   - ask: top: 10 − 1 =  [box=9, NO label]
   - ask: bottom: 5 − 2 =  [box=3, NO label]
   - ask: m = 9 ÷ 3 =  [box=3, NO label]
   - intro: Substitute \((2, 1)\) into \(y = 3x + c\):
   - ask: 3 × 2 =  [box=6, NO label]
   - ask: 1 − 6 = c, so c =  [box=-5, NO label]
   - ask: Check (5, 10): 3 × 5 + (−5) =  [box=10, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((2, 2)\) and \((6, 4)\). What is \(c\)?
   - intro: Find the gradient first from \((2, 2)\) and \((6, 4)\). The rise is smaller than the run, so expect a fraction: rise over run.
   - ask: top: 4 − 2 =  [box=2, NO label]
   - ask: bottom: 6 − 2 =  [box=4, NO label]
   - ask: m = 2 ÷ 4 =  [box=0.5, label:'(a decimal)']
   - intro: Substitute \((2, 2)\) into \(y = 0.5x + c\):
   - ask: 0.5 × 2 =  [box=1, NO label]
   - ask: 2 − 1 = c, so c =  [box=1, NO label]
   - ask: Check (6, 4): 0.5 × 6 + 1 =  [box=4, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Find the gradient of the line through \((0, 4)\) and \((6, -2)\).
   - intro: This one only wants the gradient: rise over run from \((0, 4)\) and \((6, -2)\).
   - ask: top: −2 − 4 =  [box=-6, NO label]
   - ask: bottom: 6 − 0 =  [box=6, NO label]
   - intro: Now divide, and mind the sign:
   - ask: −6 ÷ 6 =  [box=-1, NO label]
   - ask: Check by climbing: from (0, 4) to (6, −2), y falls 6 as x rises 6, a change of  [box=-1, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: A line passes through \((4, 3)\) and \((-2, -9)\). Find the gradient.
   - intro: Gradient only: rise over run from \((4, 3)\) and \((-2, -9)\). Keep the order the same top and bottom.
   - ask: top: −9 − 3 =  [box=-12, NO label]
   - ask: bottom: −2 − 4 =  [box=-6, NO label]
   - intro: Now divide, two negatives:
   - ask: −12 ÷ (−6) =  [box=2, NO label]
   - ask: Check: from (−2, −9) to (4, 3), y rises 12 as x rises 6, a climb of  [box=2, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: 2(1, 5)PQLine P has equation \(y = -3x + 2\). Line Q is parallel to P and passes through \((1, 5)\). What is the y-intercept of Q?
   - intro: Parallel lines share a gradient. Read P's gradient from \(y = -3x + 2\):
   - ask: m =  [box=-3, NO label]
   - intro: Q has the same gradient, so \(y = -3x + c\). Substitute \((1, 5)\):
   - ask: −3 × 1 =  [box=-3, NO label]
   - intro: So 5 = −3 + c.
   - ask: 5 − (−3) = c, so c =  [box=8, NO label]
   - ask: Check (1, 5): −3 × 1 + 8 =  [box=5, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: The equation of a line is \(3y = 9x - 6\). Find the gradient.
   - intro: The equation is not yet in \(y = mx + c\) form. Divide every term by 3 to get y alone.
   - ask: 9x ÷ 3 =  [box=3, label:'x']
   - ask: −6 ÷ 3 =  [box=-2, NO label]
   - intro: So \(y = 3x - 2\). Read off the gradient:
   - ask: the number with x is m =  [box=3, NO label]
   - ask: In y = 3x − 2, at x = 1: 3 × 1 − 2 =  [box=1, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Find the equation of the line through \((-1, 5)\) and \((3, -3)\). What is \(c\)?
   - intro: Find the gradient first from \((-1, 5)\) and \((3, -3)\). Watch the double negatives.
   - ask: top: −3 − 5 =  [box=-8, NO label]
   - ask: bottom: 3 − (−1) =  [box=4, NO label]
   - ask: m = −8 ÷ 4 =  [box=-2, NO label]
   - intro: Substitute \((-1, 5)\) into \(y = -2x + c\):
   - ask: −2 × (−1) =  [box=2, NO label]
   - ask: 5 − 2 = c, so c =  [box=3, NO label]
   - ask: Check (3, −3): −2 × 3 + 3 =  [box=-3, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: A line is perpendicular to \(y = 2x + 1\) and passes through \((4, 3)\). Find \(c\).
   - intro: The given gradient is 2. The perpendicular gradient is its negative reciprocal: flip and change sign.
   - ask: perpendicular m = −1 ÷ 2 =  [box=-0.5, NO label]
   - intro: So the line is \(y = -0.5x + c\). Substitute \((4, 3)\):
   - ask: −0.5 × 4 =  [box=-2, NO label]
   - intro: So 3 = −2 + c.
   - ask: 3 − (−2) = c, so c =  [box=5, NO label]
   - ask: Check (4, 3): −0.5 × 4 + 5 =  [box=3, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The line \(y = mx + 4\) passes through \((-2, 10)\). Find \(m\).
   - intro: Here c is known (4) and m is missing. Substitute \((-2, 10)\) into \(y = mx + 4\), so \(10 = m \times (-2) + 4\).
   - ask: Take the 4 across: 10 − 4 =  [box=6, NO label]
   - intro: So −2m = 6. Divide by −2:
   - ask: 6 ÷ (−2) = m =  [box=-3, NO label]
   - ask: Check: −3 × (−2) + 4 =  [box=10, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Find the equation of the line perpendicular to \(y = -\frac{1}{3}x + 2\) that passes through \((3, 7)\). What is \(c\)?
   - intro: The given gradient is \(-\frac{1}{3}\). The perpendicular gradient is the negative reciprocal: flip \(-\frac{1}{3}\) to −3, then change the sign to +3.
   - ask: perpendicular m =  [box=3, NO label]
   - intro: So the line is \(y = 3x + c\). Substitute \((3, 7)\):
   - ask: 3 × 3 =  [box=9, NO label]
   - intro: So 7 = 9 + c.
   - ask: 7 − 9 = c, so c =  [box=-2, NO label]
   - ask: Check (3, 7): 3 × 3 + (−2) =  [box=7, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: A(1, 2)B(5, 10)MThe midpoint of \(A(1, 2)\) and \(B(5, 10)\) lies on the line \(y = mx + c\) with gradient \(-1\). Find \(c\).
   - intro: First find the midpoint of \(A(1, 2)\) and \(B(5, 10)\): average the x's and average the y's.
   - ask: midpoint x: (1 + 5) ÷ 2 =  [box=3, NO label]
   - ask: midpoint y: (2 + 10) ÷ 2 =  [box=6, NO label]
   - intro: So the midpoint is \((3, 6)\). The gradient is given as −1, so \(y = -x + c\). Substitute \((3, 6)\):
   - ask: −1 × 3 =  [box=-3, NO label]
   - ask: 6 − (−3) = c, so c =  [box=9, NO label]
   - ask: Check: at x = 3, −1 × 3 + 9 =  [box=6, NO label]
