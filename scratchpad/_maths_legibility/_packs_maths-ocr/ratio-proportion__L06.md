# maths-ocr / ratio-proportion / L06 - Rates of Change & Iterative Processes

## bronze[0] (input: single_value, main-box unit: (none))
Q: text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}xy(1, 3)(5, 11)run 4rise 8Diagram not drawn accurately A tangent passes through \((1, 3)\) and \((5, 11)\). Find the rate of change.
   - intro: A straight tangent's rate of change is its gradient: rise over run.
   - ask: Change in y: 11 − 3 =  [box=8, NO label]
   - ask: Change in x: 5 − 1 =  [box=4, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 8 ÷ 4 =  [box=2, NO label]
   - ask: Check from (1, 3): 3 + 4 × 2 =  [box=11, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}xy(0, 4)(2, 10)run 2rise 6Diagram not drawn accurately A tangent passes through \((0, 4)\) and \((2, 10)\). Find the rate of change.
   - ask: Change in y: 10 − 4 =  [box=6, NO label]
   - ask: Change in x: 2 − 0 =  [box=2, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 6 ÷ 2 =  [box=3, NO label]
   - ask: Check from (0, 4): 4 + 2 × 3 =  [box=10, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = x_n + 3\). \(x_0 = 1\). Find \(x_2\).
   - intro: Iteration: put the current value in, take the next one out.
   - ask: x₁ = 1 + 3 =  [box=4, NO label]
   - intro: Now feed x₁ = 4 back in.
   - ask: x₂ = 4 + 3 =  [box=7, NO label]
   - ask: Check the gap: 7 − 4 =  [box=3, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = 2x_n - 1\). \(x_0 = 3\). Find \(x_1\).
   - ask: 2 × 3 =  [box=6, NO label]
   - intro: Now subtract 1.
   - ask: 6 − 1 =  [box=5, NO label]
   - ask: Undo it: (5 + 1) ÷ 2 =  [box=3, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}xy(1, -2)(5, 14)run 4rise 16Diagram not drawn accurately A tangent at \(x = 3\) passes through \((1, -2)\) and \((5, 14)\). Find the gradient.
   - ask: Change in y: 14 − (−2) =  [box=16, NO label]
   - ask: Change in x: 5 − 1 =  [box=4, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 16 ÷ 4 =  [box=4, NO label]
   - ask: Check from (1, −2): −2 + 4 × 4 =  [box=14, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{48}{x_n}\). \(x_0 = 8\). Find \(x_1\).
   - intro: The rule divides 48 by the current value.
   - ask: Read the start value: x₀ =  [box=8, NO label]
   - intro: Apply the rule 48 ÷ x₀.
   - ask: 48 ÷ 8 =  [box=6, NO label]
   - ask: Check: 6 × 8 =  [box=48, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{48}{x_n}\). \(x_0 = 8\). Find \(x_2\).
   - ask: x₁ = 48 ÷ 8 =  [box=6, NO label]
   - intro: Now feed x₁ = 6 back in.
   - ask: x₂ = 48 ÷ 6 =  [box=8, NO label]
   - ask: Check: 8 × 6 =  [box=48, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = x_n^2 - 2\). \(x_0 = 4\). Find \(x_1\).
   - ask: Square x₀: 4² =  [box=16, NO label]
   - intro: Now subtract 2.
   - ask: 16 − 2 =  [box=14, NO label]
   - ask: Undo it: 14 + 2 =  [box=16, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{x_n^2 + 5}{2x_n}\). \(x_0 = 3\). Find \(x_1\) to 3 d.p.
   - ask: x₀²: 3² =  [box=9, NO label]
   - ask: Numerator: 9 + 5 =  [box=14, NO label]
   - intro: Denominator is 2 × x₀.
   - ask: Denominator: 2 × 3 =  [box=6, NO label]
   - ask: x₁ = 14 ÷ 6 =  [box=2.333, NO label]
   - intro: Check: this formula settles near \(\sqrt{5} ≈ 2.236\), and 2.333 is one step in, so it is sensible.

## silver[1] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \sqrt{8 + x_n}\). \(x_0 = 3\). Find \(x_1\) to 3 d.p.
   - ask: Inside the root: 8 + 3 =  [box=11, NO label]
   - intro: Now take the square root.
   - ask: √11 =  [box=3.317, NO label]
   - ask: Check: 3.317² to the nearest whole number =  [box=11, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \sqrt{8 + x_n}\). \(x_0 = 3\). Find \(x_2\) to 3 d.p.
   - ask: x₁ inside: 8 + 3 =  [box=11, NO label]
   - ask: x₁ = √11 =  [box=3.317, NO label]
   - intro: Now feed x₁ back in.
   - ask: Inside: 8 + 3.317 =  [box=11.317, NO label]
   - ask: x₂ = √11.317 =  [box=3.364, NO label]
   - intro: Check: the terms 3.317, 3.364 are creeping up towards the fixed point near 3.372, so x₂ = 3.364 is sensible.

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: A population doubles every 3 hours. At t=0, pop=100. What is the rate of change (population per hour) at t=0?

## silver[4] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{6}{x_n + 1}\). \(x_0 = 2\). Find \(x_1\).
   - ask: Denominator first: x₀ + 1 = 2 + 1 =  [box=3, NO label]
   - intro: Now divide 6 by the whole denominator.
   - ask: x₁ = 6 ÷ 3 =  [box=2, NO label]
   - ask: Check: 2 × 3 =  [box=6, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{x_n^3 + 2}{3x_n^2}\). \(x_0 = 1\). Find \(x_1\).
   - ask: x₀³: 1³ =  [box=1, NO label]
   - ask: Numerator: 1 + 2 =  [box=3, NO label]
   - intro: Denominator is 3 × x₀².
   - ask: Denominator: 3 × 1² =  [box=3, NO label]
   - ask: x₁ = 3 ÷ 3 =  [box=1, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{5}{x_n + 2}\). \(x_0 = 1\). Find \(x_1\) to 3 d.p.
   - ask: Denominator: x₀ + 2 = 1 + 2 =  [box=3, NO label]
   - intro: Now divide 5 by the whole denominator.
   - ask: x₁ = 5 ÷ 3 =  [box=1.667, NO label]
   - ask: Check: 1.667 × 3 to the nearest whole number =  [box=5, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \sqrt[3]{5x_n + 4}\). \(x_0 = 2\). Find \(x_3\) to 3 d.p.
   - intro: Cube-root iteration. Keep 4 d.p. between steps, round only at the end.
   - ask: x₁ inside: 5 × 2 + 4 =  [box=14, NO label]
   - ask: x₁ = ∛14 =  [box=2.4101, NO label]
   - intro: x₂ from x₁: 5 × 2.4101 + 4 = 16.0505, then cube root.
   - ask: x₂ = ∛16.0505 =  [box=2.5225, NO label]
   - intro: Last step, x₃ from x₂.
   - ask: 5 × 2.5225 + 4 =  [box=16.6125, NO label]
   - ask: x₃ = ∛16.6125 =  [box=2.552, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Show \(x^3 - 5x - 4 = 0\) can be rearranged to \(x = \sqrt[3]{5x+4}\). This is the iteration formula. What equation is being solved? Enter the constant term.
   - intro: Cube both sides of x = ∛(5x + 4) to get x³ = 5x + 4.
   - ask: The coefficient of x³ is  [box=1, NO label]
   - intro: Move 5x and 4 to the left.
   - ask: The coefficient of x becomes  [box=-5, NO label]
   - ask: The constant term becomes  [box=-4, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = \frac{x_n^2 + 7}{2x_n}\). \(x_0 = 3\). Find \(x_2\) to 4 d.p.
   - intro: x₀² = 9, so the numerator is 9 + 7.
   - ask: x₁ numerator: 9 + 7 =  [box=16, NO label]
   - ask: x₁ = 16 ÷ 6 =  [box=2.6667, NO label]
   - intro: Now x₂ from x₁ = 2.6667.
   - ask: x₁²: 2.6667² =  [box=7.1113, NO label]
   - ask: New numerator: 7.1113 + 7 =  [box=14.1113, NO label]
   - ask: x₂ = 14.1113 ÷ 5.3334 =  [box=2.6458, NO label]

## gold[3] (input: multiple_choice, main-box unit: (none))
Q: An iteration converges to \(x = 2.646\) to 3 d.p. This is a solution to which equation?

## gold[4] (input: single_value, main-box unit: (none))
Q: \(x_{n+1} = 3 + \frac{1}{x_n^2}\). \(x_0 = 3\). Find \(x_1\) to 3 d.p.
   - ask: x₀²: 3² =  [box=9, NO label]
   - intro: Now take one over that.
   - ask: 1 ÷ 9 =  [box=0.111, label:'(a decimal)']
   - ask: x₁ = 3 + 0.111 =  [box=3.111, NO label]
