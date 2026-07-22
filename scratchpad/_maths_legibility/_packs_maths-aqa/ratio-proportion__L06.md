# maths-aqa / ratio-proportion / L06 - Rates of Change & Iterative Processes

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the average rate of change of \(y = x^2\) between \(x = 1\) and \(x = 3\).
   - intro: Average rate of change = (change in y) ÷ (change in x).
   - ask: f(1) = 1² =  [box=1, NO label]
   - ask: f(3) = 3² =  [box=9, NO label]
   - ask: Change in y = 9 − 1 =  [box=8, NO label]
   - ask: Change in x = 3 − 1 =  [box=2, NO label]
   - ask: Rate = 8 ÷ 2 =  [box=4, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Find the average rate of change of \(y = 3x + 1\) between \(x = 0\) and \(x = 5\).
   - intro: For a straight line the average rate of change equals its gradient. Let's compute it directly.
   - ask: f(0) = 3(0) + 1 =  [box=1, NO label]
   - ask: f(5) = 3(5) + 1 =  [box=16, NO label]
   - ask: Change in y = 16 − 1 =  [box=15, NO label]
   - ask: Change in x = 5 − 0 =  [box=5, NO label]
   - ask: Rate = 15 ÷ 5 =  [box=3, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Show there is a root of \(x^2 - 7 = 0\) between \(x = 2\) and \(x = 3\). What is \(f(2)\)?
   - intro: f(x) = x² − 7. Put x = 2 in, step by step.
   - ask: First 2² =  [box=4, NO label]
   - ask: Now subtract 7: 4 − 7 =  [box=-3, NO label]
   - ask: Check by rebuilding: (−3) + 7 =  [box=4, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: For the same equation, what is \(f(3)\)?
   - intro: Same function f(x) = x² − 7. Now put x = 3 in.
   - ask: First 3² =  [box=9, NO label]
   - ask: Now subtract 7: 9 − 7 =  [box=2, NO label]
   - ask: Check by rebuilding: 2 + 7 =  [box=9, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = x_n + 3\) with \(x_0 = 2\), find \(x_1\).
   - intro: Iteration means putting the current value into the formula to get the next one. Here x_{n+1} = x_n + 3.
   - ask: The starting value is x₀ = 2. What do we add each time?  [box=3, NO label]
   - ask: x₁ = x₀ + 3 = 2 + 3 =  [box=5, NO label]
   - ask: Check: x₁ − x₀ should equal 3. Work out 5 − 2 =  [box=3, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = x_n + 3\) with \(x_0 = 2\), find \(x_2\).
   - intro: Apply the same rule again, now to x₁ = 5, to get x₂.
   - ask: The current value is x₁ =  [box=5, NO label]
   - ask: x₂ = x₁ + 3 = 5 + 3 =  [box=8, NO label]
   - ask: Check: x₂ − x₁ should be 3. Work out 8 − 5 =  [box=3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Find the average rate of change of \(y = x^2\) between \(x = 2\) and \(x = 4\).
   - intro: Average rate = (change in y) ÷ (change in x).
   - ask: f(2) = 2² =  [box=4, NO label]
   - ask: f(4) = 4² =  [box=16, NO label]
   - ask: Change in y = 16 − 4 =  [box=12, NO label]
   - ask: Change in x = 4 − 2 =  [box=2, NO label]
   - ask: Rate = 12 ÷ 2 =  [box=6, NO label]

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: What does a positive rate of change mean on a graph?

## silver[0] (input: fraction, main-box unit: (none))
Q: Using \(x_{n+1} = \frac{10}{x_n + 1}\) with \(x_0 = 2\), find \(x_1\). Give answer as a fraction.
   - intro: Iterate x_{n+1} = 10/(x_n + 1) once, from x₀ = 2.
   - ask: Work out the denominator: x₀ + 1 = 2 + 1 =  [box=3, NO label]
   - ask: So x₁ = 10 ÷ 3. The numerator is  [box=10, NO label]
   - ask: And the denominator is  [box=3, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: \(f(x) = x^3 - 4x - 1\). Find \(f(2)\).
   - intro: Substitute x = 2 into f(x) = x³ − 4x − 1, piece by piece.
   - ask: 2³ =  [box=8, NO label]
   - ask: 4 × 2 =  [box=8, NO label]
   - ask: f(2) = 8 − 8 − 1 =  [box=-1, NO label]
   - ask: Check: 8 − 8 = 0, then 0 − 1 =  [box=-1, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: For \(f(x) = x^3 - 4x - 1\), find \(f(3)\).
   - intro: Same function, now x = 3.
   - ask: 3³ =  [box=27, NO label]
   - ask: 4 × 3 =  [box=12, NO label]
   - ask: f(3) = 27 − 12 − 1 =  [box=14, NO label]
   - ask: Check: 27 − 12 = 15, then 15 − 1 =  [box=14, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = \sqrt[3]{4x_n + 1}\) with \(x_0 = 2\), find \(x_1\) to 3 d.p.
   - intro: One iteration of x_{n+1} = ∛(4x_n + 1) from x₀ = 2.
   - ask: Inside the cube root: 4 × 2 + 1 =  [box=9, NO label]
   - ask: x₁ = ∛9. To 3 d.p. this is  [box=2.08, NO label]
   - ask: Check: cube your answer. 2.08³ to the nearest whole number =  [box=9, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Find the average rate of change of \(y = x^3\) between \(x = 1\) and \(x = 2\).
   - intro: Average rate = (change in y) ÷ (change in x) for y = x³.
   - ask: f(1) = 1³ =  [box=1, NO label]
   - ask: f(2) = 2³ =  [box=8, NO label]
   - ask: Change in y = 8 − 1 =  [box=7, NO label]
   - ask: Change in x = 2 − 1 =  [box=1, NO label]
   - ask: Rate = 7 ÷ 1 =  [box=7, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Show that \(x^2 - 4x + 1 = 0\) has a root between \(x = 0\) and \(x = 1\). What is \(f(0)\)?
   - intro: f(x) = x² − 4x + 1. Substitute x = 0.
   - ask: 0² =  [box=0, NO label]
   - ask: 4 × 0 =  [box=0, NO label]
   - ask: f(0) = 0 − 0 + 1 =  [box=1, NO label]
   - ask: Check: with x = 0 only the constant term survives. That constant is  [box=1, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: For the same equation, what is \(f(1)\)?
   - intro: Same function f(x) = x² − 4x + 1, now x = 1.
   - ask: 1² =  [box=1, NO label]
   - ask: 4 × 1 =  [box=4, NO label]
   - ask: f(1) = 1 − 4 + 1 =  [box=-2, NO label]
   - ask: Check: 1 − 4 = −3, then −3 + 1 =  [box=-2, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = \sqrt[3]{5x_n + 3}\) with \(x_0 = 3\), find \(x_1\) to 3 d.p.
   - intro: One iteration of x_{n+1} = ∛(5x_n + 3) from x₀ = 3.
   - ask: Inside the cube root: 5 × 3 + 3 =  [box=18, NO label]
   - ask: x₁ = ∛18. To 3 d.p. =  [box=2.621, NO label]
   - ask: Check: cube 2.621 to the nearest whole number =  [box=18, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: \(f(x) = x^3 + 2x - 7\). Show a root lies between 1 and 2. What is \(f(1.5)\) to 3 d.p.?
   - intro: f(x) = x³ + 2x − 7. First check the interval, then find f(1.5).
   - ask: f(1) = 1 + 2 − 7 =  [box=-4, NO label]
   - ask: f(2) = 8 + 4 − 7 =  [box=5, NO label]
   - ask: Sign change between 1 and 2. Now 1.5³ =  [box=3.375, NO label]
   - ask: f(1.5) = 3.375 + 2(1.5) − 7 = 3.375 + 3 − 7 =  [box=-0.625, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The population P of a town is modelled by \(P = 5000 \times 1.03^t\). Find the average annual rate of change between \(t = 0\) and \(t = 10\). Give to the nearest whole number.
   - intro: Average rate = (P at t = 10 − P at t = 0) ÷ (10 − 0).
   - ask: P(0) = 5000 × 1.03⁰ =  [box=5000, NO label]
   - ask: P(10) = 5000 × 1.03¹⁰, to the nearest whole number =  [box=6720, NO label]
   - ask: Change in P = 6720 − 5000 =  [box=1720, NO label]
   - ask: Rate = 1720 ÷ 10 =  [box=172, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Using \(x_{n+1} = \sqrt{3x_n + 1}\) with \(x_0 = 3\), find \(x_2\) to 3 d.p.
   - intro: Two iterations of x_{n+1} = √(3x_n + 1) from x₀ = 3.
   - ask: First iteration inside the root: 3 × 3 + 1 =  [box=10, NO label]
   - ask: x₁ = √10 to 3 d.p. =  [box=3.162, NO label]
   - ask: Now use x₁ = 3.162. Inside the next root: 3 × 3.162 + 1 =  [box=10.486, NO label]
   - ask: x₂ = √10.486 to 3 d.p. =  [box=3.238, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: The equation \(x^3 - 5x - 3 = 0\) can be rearranged to \(x = \sqrt[3]{5x + 3}\). Using \(x_0 = 2\), find \(x_1\) to 3 d.p.
   - intro: The rearrangement gives x_{n+1} = ∛(5x_n + 3). Iterate once from x₀ = 2.
   - ask: Inside the cube root: 5 × 2 + 3 =  [box=13, NO label]
   - ask: x₁ = ∛13 to 3 d.p. =  [box=2.351, NO label]
   - ask: Check: cube 2.351 to the nearest whole number =  [box=13, NO label]
