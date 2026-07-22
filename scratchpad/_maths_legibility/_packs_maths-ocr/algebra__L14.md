# maths-ocr / algebra / L14 - Quadratic nth Term, Functions & Iteration

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the 2nd difference of \(1, 4, 9, 16, 25, ...\)
   - intro: Second difference means the difference of the differences. First find the gaps between terms.
   - ask: 4 − 1 =  [box=3, NO label]
   - ask: 9 − 4 =  [box=5, NO label]
   - ask: Now the difference of those gaps: 5 − 3 =  [box=2, NO label]
   - ask: Check it stays constant: 16 − 9 = 7, then 7 − 5 =  [box=2, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: The nth term of a sequence is \(n^2 + 3\). Find the 5th term.
   - intro: The 5th term means put \(n = 5\) into \(n^2 + 3\). Square first.
   - ask: Square n: 5 × 5 =  [box=25, NO label]
   - ask: Now add 3: 25 + 3 =  [box=28, NO label]
   - ask: Check: 5² + 3 = 25 + 3 =  [box=28, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 2x + 5\), find \(f(3)\).
   - intro: \(f(3)\) means put \(x = 3\) into \(2x + 5\).
   - ask: Work out 2 × 3 =  [box=6, NO label]
   - ask: Now add 5: 6 + 5 =  [box=11, NO label]
   - ask: Check: 2 × 3 + 5 =  [box=11, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: If \(f(x) = x^2 - 1\), find \(f(-3)\).
   - intro: \(f(-3)\) means put \(x = -3\) into \(x^2 - 1\). A negative squared is positive.
   - ask: Square it: (−3) × (−3) =  [box=9, NO label]
   - ask: Now subtract 1: 9 − 1 =  [box=8, NO label]
   - ask: Check: (−3) squared is 9, minus 1 =  [box=8, NO label]

## bronze[4] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(3, 6, 11, 18, 27, ...\)

## bronze[5] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 4x - 3\), solve \(f(x) = 13\).
   - intro: Solve \(4x - 3 = 13\). Undo the \(-3\) first by adding.
   - ask: Add 3 to both sides: 13 + 3 =  [box=16, NO label]
   - ask: Now undo the ×4: 16 ÷ 4 =  [box=4, NO label]
   - ask: Check: 4 × 4 − 3 =  [box=13, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: The nth term of a quadratic sequence starts \(3n^2\). What is the 2nd difference?
   - intro: For a sequence \(an^2\), the second difference is always \(2a\).
   - ask: The number in front of n² is a =  [box=3, NO label]
   - ask: Double it: 2 × 3 =  [box=6, NO label]
   - ask: Check by halving back: 6 ÷ 2 =  [box=3, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = x_n + 3\) with \(x_1 = 4\), find \(x_4\).
   - intro: Start at \(x_1 = 4\) and add 3 each step until \(x_4\).
   - ask: x₂ = 4 + 3 =  [box=7, NO label]
   - ask: x₃ = 7 + 3 =  [box=10, NO label]
   - ask: x₄ = 10 + 3 =  [box=13, NO label]

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(0, 3, 8, 15, 24, ...\)

## silver[1] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 3x - 1\) and \(g(x) = x^2\), find \(fg(2)\).
   - intro: \(fg(2)\) means \(g\) first, then \(f\). Start inside with \(g(2)\).
   - ask: g(2) = 2 × 2 =  [box=4, NO label]
   - ask: Feed 4 into f: 3 × 4 =  [box=12, NO label]
   - ask: Now subtract 1: 12 − 1 =  [box=11, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 5x + 2\), find \(f^{-1}(x)\). Then find \(f^{-1}(17)\).
   - intro: Reverse the function. From \(y = 5x + 2\), swap and rearrange: \(f^{-1}(x) = \frac{x - 2}{5}\).
   - ask: Undo the +2: 17 − 2 =  [box=15, NO label]
   - ask: Undo the ×5: 15 ÷ 5 =  [box=3, NO label]
   - ask: Check with f: 5 × 3 + 2 =  [box=17, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = \frac{x_n^2 + 5}{4}\) with \(x_0 = 2\), find \(x_2\) to 2 d.p.
   - intro: Two iterations from \(x_0 = 2\). First \(x_1\), then feed it back for \(x_2\).
   - ask: Top of x₁: 2² + 5 =  [box=9, NO label]
   - ask: x₁ = 9 ÷ 4 =  [box=2.25, NO label]
   - ask: Top of x₂: 2.25² + 5 =  [box=10.0625, NO label]
   - ask: x₂ = 10.0625 ÷ 4, to 2 d.p. =  [box=2.52, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(4, 10, 18, 28, 40, ...\)

## silver[5] (input: single_value, main-box unit: (none))
Q: If \(f(x) = x^2 + 2\) and \(g(x) = 3x\), find \(gf(4)\).
   - intro: \(gf(4)\) means \(f\) first, then \(g\). Start inside with \(f(4)\).
   - ask: Square 4: 4 × 4 =  [box=16, NO label]
   - ask: Finish f: 16 + 2 =  [box=18, NO label]
   - ask: Feed 18 into g: 3 × 18 =  [box=54, NO label]
   - ask: Check: g(f(4)) = 3 × 18 =  [box=54, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: The first 3 terms of a quadratic sequence are \(5, 12, 23\). Find the next term.
   - intro: In a quadratic sequence the gaps grow by a fixed amount. Find the first gaps.
   - ask: 12 − 5 =  [box=7, NO label]
   - ask: 23 − 12 =  [box=11, NO label]
   - ask: The gaps grow by 11 − 7 =  [box=4, NO label]
   - ask: Next gap 11 + 4 = 15, so next term 23 + 15 =  [box=38, NO label]

## gold[0] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(2, 8, 18, 32, 50, ...\)

## gold[1] (input: single_value, main-box unit: (none))
Q: If \(f(x) = \frac{2x+1}{x-3}\), find \(f^{-1}(x)\). Enter the numerator coefficient of x.
   - intro: Let \(y = \frac{2x+1}{x-3}\). Multiply out: \(y(x-3) = 2x+1\), so \(xy - 3y = 2x + 1\). Gather x on one side: \(x(y-2) = 3y + 1\).
   - ask: In that numerator 3y + 1, the number multiplying y is  [box=3, NO label]
   - ask: The constant added in that numerator is  [box=1, NO label]
   - ask: Swapping letters, \(f^{-1}(x) = \frac{3x+1}{x-2}\); its numerator coefficient of x is  [box=3, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = \sqrt{5x_n + 2}\) with \(x_0 = 3\), find the value the sequence converges to (1 d.p.).
   - intro: At the limit the value stops changing, so \(x = \sqrt{5x + 2}\). Square both sides: \(x^2 = 5x + 2\), i.e. \(x^2 - 5x - 2 = 0\).
   - ask: Under the quadratic-formula root, 5² + 8 =  [box=33, NO label]
   - ask: √33 to 2 d.p. =  [box=5.74, NO label]
   - ask: x = (5 + 5.74) ÷ 2, to 1 d.p. =  [box=5.4, NO label]

## gold[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(1, 7, 17, 31, 49, ...\)

## gold[4] (input: two_solutions, main-box unit: (none))
Q: If \(f(x) = x^2\) and \(g(x) = 2x - 1\), solve \(fg(x) = 25\).
   - intro: \(fg(x)\) does \(g\) first: \(f(2x-1) = (2x-1)^2\). Set it to 25, so \(2x - 1 = \pm 5\).
   - ask: Square root of 25 =  [box=5, NO label]
   - ask: Plus case: 2x − 1 = 5, so 2x = 6 and x = 6 ÷ 2 =  [box=3, NO label]
   - ask: Minus case: 2x − 1 = −5, so 2x = −4 and x = −4 ÷ 2 =  [box=-2, NO label]
