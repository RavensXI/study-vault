# maths-edexcel / ratio-proportion / L06 - Rates of Change & Iterative Processes

## bronze[0] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((2, 5)\) and \((6, 13)\). Find the gradient.
   - ask: Rise (top y minus bottom y): 13 − 5 =  [box=8, NO label]
   - ask: Run (right x minus left x): 6 − 2 =  [box=4, NO label]
   - intro: Now put the two together.
   - ask: Gradient = rise ÷ run = 8 ÷ 4 =  [box=2, NO label]
   - ask: Check: a gradient of 2 over a run of 4 should climb 2 × 4 =  [box=8, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((0, 8)\) and \((4, 0)\). Find the gradient.
   - ask: Rise (top y minus bottom y): 0 − 8 =  [box=-8, NO label]
   - ask: Run: 4 − 0 =  [box=4, NO label]
   - intro: Divide, keeping the minus sign.
   - ask: Gradient = −8 ÷ 4 =  [box=-2, NO label]
   - ask: Check: −2 × 4 =  [box=-8, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = x_n + 3\) with \(x_0 = 2\). Find \(x_3\).
   - ask: x₁ = 2 + 3 =  [box=5, NO label]
   - intro: Feed each answer back into the same rule.
   - ask: x₂ = 5 + 3 =  [box=8, NO label]
   - ask: x₃ = 8 + 3 =  [box=11, NO label]
   - ask: Check: from the start, 3 jumps of 3 is 2 + 9 =  [box=11, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = 2x_n - 1\) with \(x_0 = 3\). Find \(x_2\).
   - ask: x₁ = 2 × 3 − 1 =  [box=5, NO label]
   - intro: Now feed x₁ back into the same rule.
   - ask: x₂ = 2 × 5 − 1 =  [box=9, NO label]
   - ask: Check: reverse the rule, (9 + 1) ÷ 2 =  [box=5, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((1, 2)\) and \((5, 22)\). What is the rate of change?
   - ask: Rise: 22 − 2 =  [box=20, NO label]
   - ask: Run: 5 − 1 =  [box=4, NO label]
   - intro: Divide the rise by the run.
   - ask: Rate of change = rise ÷ run = 20 ÷ 4 =  [box=5, NO label]
   - ask: Check: 5 × 4 =  [box=20, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{x_n}{2} + 4\) with \(x_0 = 6\). Find \(x_1\).
   - ask: Halve the start value: 6 ÷ 2 =  [box=3, NO label]
   - intro: The rule says halve, then add 4.
   - ask: Then add 4: 3 + 4 =  [box=7, NO label]
   - ask: Check: 6 ÷ 2 + 4 =  [box=7, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((2, 1)\) and \((5, 10)\). Find the gradient.
   - ask: Rise: 10 − 1 =  [box=9, NO label]
   - ask: Run: 5 − 2 =  [box=3, NO label]
   - intro: Divide the rise by the run.
   - ask: Gradient = 9 ÷ 3 =  [box=3, NO label]
   - ask: Check: 3 × 3 =  [box=9, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = x_n^2 - 5\) with \(x_0 = 3\). Find \(x_1\).
   - ask: Square the start value: 3² =  [box=9, NO label]
   - intro: The rule is: square, then take away 5.
   - ask: Then subtract 5: 9 − 5 =  [box=4, NO label]
   - ask: Check: 3 × 3 − 5 =  [box=4, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \sqrt{3x_n + 7}\) with \(x_0 = 2\). Find \(x_2\) to 2 d.p.
   - ask: First iteration, inside the root: 3 × 2 + 7 =  [box=13, NO label]
   - intro: So \(x_1 = \sqrt{13} = 3.6056\). Keep this full value, do not round yet.
   - ask: Second iteration: 3 × 3.6056 + 7 gives 17.8168 under the root, so x₂ = √17.8168 to 2 d.p. =  [box=4.22, NO label]
   - ask: Check: 4.22² to 2 d.p. =  [box=17.81, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: A distance-time graph has a tangent at \(t = 4\) passing through \((2, 3)\) and \((6, 11)\). Estimate the speed at \(t = 4\).
   - ask: Rise (distance change): 11 − 3 =  [box=8, NO label]
   - ask: Run (time change): 6 − 2 =  [box=4, NO label]
   - intro: Speed is the steepness of the distance-time line.
   - ask: Speed = gradient = 8 ÷ 4 =  [box=2, NO label]
   - ask: Check: 2 × 4 =  [box=8, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{x_n^3 + 1}{4}\) with \(x_0 = 1\). Find \(x_3\) to 3 d.p.
   - ask: x₁ = (1³ + 1) ÷ 4 = 2 ÷ 4 =  [box=0.5, label:'(a decimal)']
   - intro: Feed x₁ back in to reach x₂.
   - ask: x₂ = (0.5³ + 1) ÷ 4 = (0.125 + 1) ÷ 4 =  [box=0.28125, label:'(a decimal)']
   - ask: x₃ = (0.28125³ + 1) ÷ 4, to 3 d.p. =  [box=0.256, label:'(a decimal)']

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: The gradient of a velocity-time graph at \(t = 5\) is 3. What does this represent?

## silver[4] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{10}{x_n + 1}\) with \(x_0 = 3\). Find \(x_2\) to 2 d.p.
   - ask: x₁: denominator is 3 + 1 = 4, so 10 ÷ 4 =  [box=2.5, NO label]
   - intro: Feed x₁ back in to reach x₂.
   - ask: x₂: denominator is 2.5 + 1 = 3.5, so 10 ÷ 3.5 to 2 d.p. =  [box=2.86, NO label]
   - ask: Check: 2.86 × 3.5 =  [box=10.01, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: The gradient of a curve at \(x = 2\) is found using the tangent through \((0, -1)\) and \((4, 11)\). Find the gradient.
   - ask: Rise: 11 − (−1) =  [box=12, NO label]
   - ask: Run: 4 − 0 =  [box=4, NO label]
   - intro: Divide the rise by the run.
   - ask: Gradient = 12 ÷ 4 =  [box=3, NO label]
   - ask: Check: 3 × 4 =  [box=12, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \sqrt[3]{8x_n - 3}\) with \(x_0 = 1\). Find \(x_1\) to 3 d.p.
   - ask: Inside the cube root: 8 × 1 − 3 =  [box=5, NO label]
   - intro: Now take the cube root of that.
   - ask: x₁ = ∛5, to 3 d.p. =  [box=1.71, NO label]
   - ask: Check: 1.71³ to 2 d.p. =  [box=5.0, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{2x_n^3 + 5}{3x_n^2}\) with \(x_0 = 2\) to find a root to 3 d.p. Give \(x_3\).
   - ask: x₁ numerator: 2 × 2³ + 5 = 2 × 8 + 5 =  [box=21, NO label]
   - ask: x₁ denominator: 3 × 2² = 3 × 4 =  [box=12, NO label]
   - ask: x₁ = 21 ÷ 12 =  [box=1.75, NO label]
   - intro: Feed x₁ back into the same formula for x₂.
   - ask: x₂ = (2 × 1.75³ + 5) ÷ (3 × 1.75²), to 4 d.p. =  [box=1.7109, NO label]
   - ask: x₃ = (2 × 1.7109³ + 5) ÷ (3 × 1.7109²), to 3 d.p. =  [box=1.71, NO label]
   - ask: Check: 1.71³ to 2 d.p. =  [box=5.0, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Show that \(x^3 - 5x + 1 = 0\) has a root between \(x = 2\) and \(x = 3\). What is \(f(2)\)?
   - ask: First 2³ =  [box=8, NO label]
   - ask: and 5 × 2 =  [box=10, NO label]
   - intro: Put the pieces together for f(2).
   - ask: f(2) = 8 − 10 + 1 =  [box=-1, NO label]
   - ask: Now f(3): 3³ − 5 × 3 + 1 = 27 − 15 + 1 =  [box=13, NO label]
   - ask: f(2) is negative and f(3) is positive, so a root lies between. The value asked for, f(2), is  [box=-1, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with 4 strips to estimate the area under \(y = x^2\) from \(x = 0\) to \(x = 4\). (Strip width = 1)
   - ask: Heights y = x² at x = 0, 1, 2, 3, 4. The one at x = 2 is 2² =  [box=4, NO label]
   - ask: and the one at x = 3 is 3² =  [box=9, NO label]
   - intro: Now apply the trapezium rule.
   - ask: Add the two end heights: 0 + 16 =  [box=16, NO label]
   - ask: Double the middle heights: 2 × (1 + 4 + 9) =  [box=28, NO label]
   - ask: Area = ½ × 1 × (16 + 28) =  [box=22, label:'cm²']

## gold[3] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = 5 - \frac{1}{x_n^2}\) with \(x_0 = 2\). Find \(x_3\) to 4 d.p.
   - ask: x₁ = 5 − 1 ÷ 2² = 5 − 1 ÷ 4 = 5 − 0.25 =  [box=4.75, NO label]
   - ask: For x₂, the denominator 4.75² =  [box=22.5625, NO label]
   - intro: Feed x₁ back in for x₂.
   - ask: x₂ = 5 − 1 ÷ 22.5625, to 4 d.p. =  [box=4.9557, NO label]
   - ask: x₃ = 5 − 1 ÷ 4.9557², to 4 d.p. =  [box=4.9593, NO label]
   - ask: Check: 5 − 4.9593 =  [box=0.0407, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: An iteration converges to the solution of \(x = \sqrt{2x + 15}\). What quadratic equation does this solve? Give the positive root.
   - intro: When the iteration settles, x stops changing, so \(x = \sqrt{2x + 15}\). Square both sides: \(x^2 = 2x + 15\), which rearranges to \(x^2 - 2x - 15 = 0\).
   - ask: We need two numbers that multiply to −15 and add to −2. One is −5, the other is  [box=3, NO label]
   - intro: Set each bracket to zero to find the roots.
   - ask: So (x − 5)(x + 3) = 0. The negative root is x =  [box=-3, NO label]
   - ask: The question wants the positive root, so x =  [box=5, NO label]
   - ask: Check: put x = 5 into 2x + 15: 2 × 5 + 15 =  [box=25, NO label]
