# maths-aqa / algebra / L14 - Quadratic nth Term, Functions & Iteration

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the nth term of \(3, 6, 11, 18, 27, ...\). The second difference is?
   - intro: Second difference means the difference of the differences. First, the gaps between terms.
   - ask: 6 − 3 =  [box=3, NO label]
   - ask: 11 − 6 =  [box=5, NO label]
   - ask: Now the difference of those gaps: 5 − 3 =  [box=2, NO label]
   - ask: Check it stays constant: 18 − 11 = 7, then 7 − 5 =  [box=2, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A quadratic sequence has second difference 6. What is the coefficient of \(n^2\)?
   - intro: The number in front of \(n^2\) is always half the second difference.
   - ask: Write the second difference:  [box=6, NO label]
   - ask: Halve it: 6 ÷ 2 =  [box=3, NO label]
   - ask: Check by doubling back: 3 × 2 =  [box=6, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 2x + 3\), find \(f(4)\)
   - intro: \(f(4)\) means put \(x = 4\) into \(2x + 3\).
   - ask: The input x is  [box=4, NO label]
   - ask: Work out 2 × 4 =  [box=8, NO label]
   - ask: Now add 3: 8 + 3 =  [box=11, NO label]
   - ask: Check: 2 × 4 + 3 =  [box=11, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: If \(f(x) = x^2 - 1\), find \(f(3)\)
   - intro: \(f(3)\) means put \(x = 3\) into \(x^2 - 1\). Here \(x^2\) means \(x \times x\).
   - ask: Square the input: 3 × 3 =  [box=9, NO label]
   - ask: Now subtract 1: 9 − 1 =  [box=8, NO label]
   - ask: Check: 3 squared is 9, minus 1 =  [box=8, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: If \(f(x) = x^2 - 1\), find \(f(-4)\)
   - intro: \(f(-4)\) means put \(x = -4\) into \(x^2 - 1\). A negative squared is positive.
   - ask: Square it: (−4) × (−4) =  [box=16, NO label]
   - ask: Now subtract 1: 16 − 1 =  [box=15, NO label]
   - ask: Check: (−4) squared is 16, minus 1 =  [box=15, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: The nth term of a quadratic sequence is \(n^2 + 2n\). Find the 5th term.
   - intro: The 5th term means put \(n = 5\) into \(n^2 + 2n\).
   - ask: Square n: 5 × 5 =  [box=25, NO label]
   - ask: The 2n part: 2 × 5 =  [box=10, NO label]
   - ask: Add them: 25 + 10 =  [box=35, NO label]
   - ask: Check: 5² + 2 × 5 = 25 + 10 =  [box=35, NO label]

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(1, 4, 9, 16, 25, ...\)

## bronze[7] (input: single_value, main-box unit: (none))
Q: If \(g(x) = 5x - 2\), find \(g(0)\)
   - intro: \(g(0)\) means put \(x = 0\) into \(5x - 2\).
   - ask: The 5x part: 5 × 0 =  [box=0, NO label]
   - ask: Now subtract 2: 0 − 2 =  [box=-2, NO label]
   - ask: Check: 5 × 0 − 2 =  [box=-2, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 3x + 1\) and \(g(x) = x^2\), find \(fg(2)\)
   - intro: \(fg(2)\) means do \(g\) first, then \(f\). Start inside with \(g(2)\).
   - ask: g(2) = 2 × 2 =  [box=4, NO label]
   - ask: Now feed 4 into f: 3 × 4 =  [box=12, NO label]
   - ask: Add 1: 12 + 1 =  [box=13, NO label]
   - ask: Check: f(g(2)) = 3 × 4 + 1 =  [box=13, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 3x + 1\) and \(g(x) = x^2\), find \(gf(2)\)
   - intro: \(gf(2)\) means do \(f\) first, then \(g\). Start inside with \(f(2)\).
   - ask: f(2) = 3 × 2 + 1 =  [box=7, NO label]
   - ask: Now feed 7 into g: 7 × 7 =  [box=49, NO label]
   - ask: Check: g(f(2)) = 7² =  [box=49, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: If \(f(x) = 2x + 5\), find \(f^{-1}(x)\). What is \(f^{-1}(11)\)?
   - intro: First reverse the function. From \(y = 2x + 5\), swap and rearrange: \(f^{-1}(x) = \frac{x - 5}{2}\).
   - ask: Undo the +5: 11 − 5 =  [box=6, NO label]
   - ask: Undo the ×2: 6 ÷ 2 =  [box=3, NO label]
   - ask: Check with f: 2 × 3 + 5 =  [box=11, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Use the iteration formula \(x_{n+1} = \sqrt{x_n + 5}\) with \(x_0 = 2\). Find \(x_1\) to 2 d.p.
   - intro: One step of the iteration: put \(x_0 = 2\) into \(\sqrt{x_n + 5}\). Add first, then square root.
   - ask: Inside first: 2 + 5 =  [box=7, NO label]
   - ask: Now square root, to 2 d.p.: √7 =  [box=2.65, NO label]
   - ask: Check: 2.65 squared is about 7, and 7 − 5 =  [box=2, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(4, 10, 20, 34, 52, ...\)

## silver[5] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(0, 5, 14, 27, 44, ...\)

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(2, 8, 18, 32, 50, ...\)

## gold[0] (input: single_value, main-box unit: (none))
Q: If \(f(x) = \frac{x+3}{2}\), find \(f^{-1}(x)\). What is \(f^{-1}(5)\)?
   - intro: Reverse the function first. From \(y = \frac{x+3}{2}\), swap and rearrange: \(f^{-1}(x) = 2x - 3\).
   - ask: Undo the ÷2 by doubling: 2 × 5 =  [box=10, NO label]
   - ask: Then subtract 3: 10 − 3 =  [box=7, NO label]
   - ask: Check with f: (7 + 3) ÷ 2 =  [box=5, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{10}{x_n + 3}\) with \(x_0 = 1\). Find \(x_2\) to 2 d.p.
   - intro: Two steps from \(x_0 = 1\). First \(x_1\), then feed it back for \(x_2\).
   - ask: x₁ = 10 ÷ (1 + 3) = 10 ÷ 4 =  [box=2.5, NO label]
   - ask: For x₂ the new denominator is 2.5 + 3 =  [box=5.5, NO label]
   - ask: x₂ = 10 ÷ 5.5, to 2 d.p. =  [box=1.82, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: If \(f(x) = x^2 + 1\) and \(g(x) = 2x - 3\), solve \(fg(x) = 5\). Find the larger value of \(x\).
   - intro: \(fg(x)\) means \(g\) first: \(f(2x-3) = (2x-3)^2 + 1\). Set it equal to 5.
   - ask: Subtract 1 from both sides: (2x − 3)² = 5 − 1 =  [box=4, NO label]
   - ask: Square root both sides: √4 =  [box=2, NO label]
   - ask: The + case: 2x − 3 = 2, so 2x = 5 and x =  [box=2.5, NO label]
   - ask: The − case: 2x − 3 = −2, 2x = 1, x =  [box=0.5, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: The equation \(x^3 - 3x - 5 = 0\) has a root near \(x = 2\). Use the iteration \(x_{n+1} = \sqrt[3]{3x_n + 5}\) with \(x_0 = 2\). Find \(x_2\) to 3 d.p.
   - intro: Two iterations from \(x_0 = 2\) using \(x_{n+1} = \sqrt[3]{3x_n + 5}\).
   - ask: Inside for x₁: 3 × 2 + 5 =  [box=11, NO label]
   - ask: x₁ = cube root of 11, to 3 d.p. =  [box=2.224, NO label]
   - ask: Inside for x₂: 3 × 2.224 + 5 =  [box=11.672, NO label]
   - ask: x₂ = cube root of 11.672, to 3 d.p. =  [box=2.268, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(3, 9, 19, 33, 51, ...\)
