# maths-eduqas / algebra / L14 - Quadratic nth Term, Functions & Iteration

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the second difference of \(1, 4, 9, 16, 25, ...\)
   - intro: These are the square numbers. The second difference is the gap between the gaps. First find the first differences.
   - ask: 4 − 1 =  [box=3, NO label]
   - ask: 9 − 4 =  [box=5, NO label]
   - ask: Second difference: 5 − 3 =  [box=2, NO label]
   - ask: Check the next gap is the same: 7 − 5 =  [box=2, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: The second difference of a quadratic sequence is \(6\). What is \(a\) in \(an^2 + bn + c\)?
   - intro: For a quadratic \(an^2 + bn + c\), the constant second difference equals \(2a\). Here it is 6, so find \(a\).
   - ask: The second difference is 2a. Halve it: 6 ÷ 2 =  [box=3, NO label]
   - ask: That halved value is a, so a =  [box=3, NO label]
   - ask: Check by doubling: 2 × 3 =  [box=6, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(f(x) = 2x + 3\). Find \(f(4)\).
   - intro: \(f(x) = 2x + 3\) is a machine: double the input, then add 3. Find \(f(4)\).
   - ask: Double the input: 2 × 4 =  [box=8, NO label]
   - ask: Now add 3: 8 + 3 =  [box=11, NO label]
   - ask: Read it back to check: 2 × 4 = 8, then 8 + 3 =  [box=11, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(f(x) = x^2 - 1\). Find \(f(3)\).
   - intro: \(f(x) = x^2 - 1\). Find \(f(3)\): square the input, then take off 1.
   - ask: Square: 3² = 3 × 3 =  [box=9, NO label]
   - ask: Take off 1: 9 − 1 =  [box=8, NO label]
   - ask: Check: 3² − 1 =  [box=8, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: \(f(x) = 2x + 3\). Find \(f(-1)\).
   - intro: \(f(x) = 2x + 3\). Find \(f(-1)\). Watch the sign.
   - ask: Double: 2 × (−1) =  [box=-2, NO label]
   - ask: Add 3: −2 + 3 =  [box=1, NO label]
   - ask: Check: 2 × (−1) + 3 =  [box=1, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = x_n + 3\), \(x_1 = 1\). Find \(x_3\).
   - intro: \(x_{n+1} = x_n + 3\) means add 3 each time. Start at \(x_1 = 1\). Find \(x_3\).
   - ask: \(x_2 = x_1 + 3\): 1 + 3 =  [box=4, NO label]
   - ask: \(x_3 = x_2 + 3\): 4 + 3 =  [box=7, NO label]
   - ask: Check the chain: 1, then 4, then  [box=7, NO label]

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: 14916Find the nth term of \(1, 4, 9, 16, 25, ...\). Which is correct?

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(f(x) = 5x\). Find \(f(3)\).
   - intro: \(f(x) = 5x\) means five times the input. Find \(f(3)\).
   - ask: Five threes: 5 × 3 =  [box=15, NO label]
   - ask: So \(f(3)\) =  [box=15, NO label]
   - ask: Check another way, add three 5s: 5 + 5 + 5 =  [box=15, NO label]

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(3, 8, 15, 24, ...\). Which is correct?

## silver[1] (input: single_value, main-box unit: (none))
Q: \(f(x) = 3x + 1\), \(g(x) = x^2\). Find \(fg(2)\).
   - intro: \(f(x) = 3x + 1\) and \(g(x) = x^2\). Find \(fg(2)\). The rule: \(fg\) means do \(g\) first, then \(f\).
   - ask: Inside first: g(2) = 2² =  [box=4, NO label]
   - ask: Feed 4 into f: f(4) = 3 × 4 + 1 =  [box=13, NO label]
   - ask: Check: square 2 to get 4, then 3 × 4 + 1 =  [box=13, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(f(x) = 3x + 1\), \(g(x) = x^2\). Find \(gf(2)\).
   - intro: Same functions, \(f(x) = 3x + 1\), \(g(x) = x^2\). Find \(gf(2)\): do \(f\) first, then \(g\).
   - ask: Inside first: f(2) = 3 × 2 + 1 =  [box=7, NO label]
   - ask: Feed 7 into g: g(7) = 7² =  [box=49, NO label]
   - ask: Check: f(2) = 7, then square it: 7 × 7 =  [box=49, NO label]

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: \(f(x) = 2x - 5\). Find \(f^{-1}(x)\). Which is correct?

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(0, 3, 8, 15, 24, ...\). Which is correct?

## silver[5] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{x_n + 5}{2}\), \(x_0 = 1\). Find \(x_2\) to 1 d.p.
   - intro: \(x_{n+1} = \frac{x_n + 5}{2}\), start \(x_0 = 1\). Find \(x_2\), two iterations.
   - ask: First \(x_1\): (1 + 5) ÷ 2 =  [box=3, NO label]
   - ask: Now \(x_2\): feed 3 back in: (3 + 5) ÷ 2 =  [box=4, NO label]
   - ask: Check the chain: 1, then 3, then  [box=4, NO label]

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: \(f(x) = \frac{x+1}{3}\). Find \(f^{-1}(x)\). Which is correct?

## gold[0] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(2, 9, 20, 35, 54, ...\). Which is correct?

## gold[1] (input: single_value, main-box unit: (none))
Q: \(f(x) = 3x - 2\), \(g(x) = x + 5\). Solve \(fg(x) = 19\).
   - intro: \(fg(x)\) means do \(g\) first: \(f(x+5) = 3(x+5) - 2\). Multiply out and collect the number part.
   - ask: Multiply out the bracket: 3 × 5 =  [box=15, NO label]
   - ask: So the constant is 15 − 2 =  [box=13, NO label]
   - ask: Now solve 3x + 13 = 19. Take 13 off: 19 − 13 =  [box=6, NO label]
   - ask: Divide by 3: 6 ÷ 3 =  [box=2, NO label]
   - ask: Check: put x = 2 in: 3 × (2 + 5) − 2 =  [box=19, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{x_n^2 + 3}{5}\), \(x_0 = 1\). Find \(x_2\) to 3 d.p.
   - intro: \(x_{n+1} = \frac{x_n^2 + 3}{5}\), start \(x_0 = 1\). Find \(x_2\), two iterations. Calculator allowed.
   - ask: First \(x_1\). Square the start: 1² =  [box=1, NO label]
   - ask: Add 3, then divide by 5: (1 + 3) ÷ 5 =  [box=0.8, label:'(a decimal)']
   - ask: Now \(x_2\). Square 0.8: 0.8² =  [box=0.64, NO label]
   - ask: Add 3, then divide by 5: (0.64 + 3) ÷ 5 =  [box=0.728, label:'(a decimal)']

## gold[3] (input: multiple_choice, main-box unit: (none))
Q: \(f(x) = \frac{2x+1}{x-3}\). Find \(f^{-1}(x)\). Which is correct?

## gold[4] (input: single_value, main-box unit: (none))
Q: A quadratic sequence begins \(5, 12, 23, 38, ...\). Find the 10th term.
   - intro: Sequence 5, 12, 23, 38. Find the nth term, then the 10th term.
   - ask: First differences: 12 − 5 =  [box=7, NO label]
   - ask: and 23 − 12 =  [box=11, NO label]
   - ask: Second difference: 11 − 7 =  [box=4, NO label]
   - ask: Subtract \(2n^2\). At n = 1: 5 − 2 × 1² = 5 − 2 =  [box=3, NO label]
   - ask: Now the 10th term. First 2 × 10² = 2 × 100 =  [box=200, NO label]
   - ask: Then n + 2 = 10 + 2 =  [box=12, NO label]
   - ask: Add them: 200 + 12 =  [box=212, NO label]
