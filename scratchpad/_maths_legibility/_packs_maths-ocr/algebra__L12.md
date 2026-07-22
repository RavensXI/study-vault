# maths-ocr / algebra / L12 - Quadratic Inequalities & Regions

## bronze[0] (input: multiple_choice, main-box unit: (none))
Q: Solve \(x^2 - 4 < 0\). What is the range?

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Solve \(x^2 - 9 > 0\). What is the range?

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Solve \((x-1)(x-5) < 0\). What is the range?

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Solve \(x^2 - 6x + 8 \leq 0\). What is the range?

## bronze[4] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 > 25\). How many integers from \(-10\) to \(10\) satisfy this?
   - intro: Find where \(x^2 = 25\) by square-rooting: the critical values are \(\pm 5\). So \(x^2 > 25\) means \(x 5\).
   - ask: The positive critical value is  [box=5, NO label]
   - ask: The negative critical value is  [box=-5, NO label]
   - intro: Now count the integers from \(-10\) to \(10\) that are below \(-5\) or above 5.
   - ask: Integers -10 to -6 (all below -5): how many?  [box=5, NO label]
   - ask: There are 5 more above 5 (6 to 10). Total =  [box=10, NO label]

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: Solve \((x+3)(x-1) > 0\). What is the range?

## bronze[6] (input: single_value, main-box unit: (none))
Q: How many integers satisfy \(x^2 - 3x - 4 \leq 0\)?
   - intro: Factorise \(x^2 - 3x - 4\). Two numbers multiply to \(-4\) and add to \(-3\): they are \(-4\) and \(+1\), giving \((x-4)(x+1)\).
   - ask: From x - 4 = 0: x =  [box=4, NO label]
   - ask: From x + 1 = 0: x =  [box=-1, NO label]
   - intro: For \(\leq 0\) the solution is between the roots, inclusive: \(-1 \leq x \leq 4\). Count every whole number from \(-1\) to 4.
   - ask: They are -1, 0, 1, 2, 3, 4. How many?  [box=6, NO label]
   - ask: Check the endpoint x = 4: 4² - 3(4) - 4 =  [box=0, NO label]

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: Solve \(x^2 + x - 6 < 0\). What is the range?

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: Solve \(x^2 - 2x - 8 \geq 0\). What is the range?

## silver[1] (input: multiple_choice, main-box unit: (none))
Q: Solve \(2x^2 - 5x - 3 < 0\). What is the range?

## silver[2] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 \leq 3x + 10\). How many integers satisfy it?
   - intro: Rearrange to \(x^2 - 3x - 10 \leq 0\). Factorise: two numbers multiply to \(-10\) and add to \(-3\), namely \(-5\) and \(+2\), giving \((x-5)(x+2)\).
   - ask: From x - 5 = 0: x =  [box=5, NO label]
   - ask: From x + 2 = 0: x =  [box=-2, NO label]
   - intro: For \(\leq 0\), take between the roots, inclusive: \(-2 \leq x \leq 5\). Count the whole numbers from \(-2\) to 5.
   - ask: They are -2, -1, 0, 1, 2, 3, 4, 5. How many?  [box=8, NO label]
   - ask: Check the endpoint x = -2: (-2)² - 3(-2) - 10 =  [box=0, NO label]

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: Solve \(-x^2 + 4x - 3 > 0\). What is the range?

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: For what values of \(x\) is \(x^2 + 6x + 5 > 0\)?

## silver[5] (input: single_value, main-box unit: (none))
Q: How many positive integers satisfy \(x^2 < 50\)?
   - intro: Find where \(x^2 = 50\). The square root is \(\sqrt{50} \approx 7.07\), so \(x^2 < 50\) means \(-7.07 < x < 7.07\).
   - ask: The largest whole number below 7.07 is  [box=7, NO label]
   - intro: We want POSITIVE integers only, so count from 1 up to that value.
   - ask: Count the positive integers 1, 2, 3, 4, 5, 6, 7. How many?  [box=7, NO label]
   - ask: Check x = 7: 7² =  [box=49, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 + 4x \geq 5\). What is the positive root?
   - intro: Rearrange to \(x^2 + 4x - 5 \geq 0\). Factorise: two numbers multiply to \(-5\) and add to \(+4\), namely \(+5\) and \(-1\), giving \((x+5)(x-1)\).
   - ask: From x + 5 = 0: x =  [box=-5, NO label]
   - ask: From x - 1 = 0: x =  [box=1, NO label]
   - ask: Of the roots -5 and 1, the positive one is  [box=1, NO label]

## gold[0] (input: multiple_choice, main-box unit: (none))
Q: Solve \(3x^2 + 2x - 1 > 0\). What is the range?

## gold[1] (input: multiple_choice, main-box unit: (none))
Q: Find the values of \(k\) for which \(x^2 + kx + 4 = 0\) has no real roots. What is the range?

## gold[2] (input: multiple_choice, main-box unit: (none))
Q: Find the set of values of \(x\) for which \(x^2 - 2x > x + 4\). What is the range?

## gold[3] (input: single_value, main-box unit: (none))
Q: How many integers satisfy both \(x^2 - 9 \leq 0\) AND \(x + 1 > 0\)?
   - intro: Solve each part. First \(x^2 - 9 \leq 0\) factorises to \((x-3)(x+3) \leq 0\), giving between the roots: \(-3 \leq x \leq 3\).
   - ask: The second condition x + 1 > 0 rearranges to x >  [box=-1, NO label]
   - intro: Overlap \(-3 \leq x \leq 3\) with \(x > -1\): since \(x\) must beat \(-1\), the overlap is \(-1 < x \leq 3\).
   - ask: The whole numbers with -1 < x ≤ 3 are 0, 1, 2, 3. How many?  [box=4, NO label]
   - ask: Check x = 3 in the first part: 3² - 9 =  [box=0, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: Solve \(6 - x - x^2 \geq 0\). What is the range?
