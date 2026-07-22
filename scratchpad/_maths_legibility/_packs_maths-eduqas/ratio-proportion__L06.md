# maths-eduqas / ratio-proportion / L06 - Rates of Change & Iterative Processes

## bronze[0] (input: single_value, main-box unit: (none))
Q: 804kmhoursA distance-time graph is a straight line from the origin to the point (4, 80), where distance is in km and time in hours. What is the speed?
   - ask: Distance travelled (the y-value at the end):  [box=80, NO label]
   - ask: Time taken (the x-value at the end):  [box=4, NO label]
   - intro: Speed is the steepness of the line.
   - ask: Speed = distance ÷ time = 80 ÷ 4 =  [box=20, NO label]
   - ask: Check: speed × time = 20 × 4 =  [box=80, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A straight line passes through (1, 4) and (5, 20). Find its gradient.
   - ask: Rise (top y minus bottom y): 20 − 4 =  [box=16, NO label]
   - ask: Run (right x minus left x): 5 − 1 =  [box=4, NO label]
   - intro: Now put the two together.
   - ask: Gradient = rise ÷ run = 16 ÷ 4 =  [box=4, NO label]
   - ask: Check: gradient × run = 4 × 4 =  [box=16, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = x_n + 4\) with \(x_0 = 3\). Find \(x_2\).
   - ask: x₁ = 3 + 4 =  [box=7, NO label]
   - intro: Feed each answer back into the same rule.
   - ask: x₂ = 7 + 4 =  [box=11, NO label]
   - ask: Check: from the start, two jumps of 4 is 3 + 8 =  [box=11, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = 2x_n - 1\) with \(x_0 = 4\). Find \(x_1\).
   - ask: First multiply: 2 × 4 =  [box=8, NO label]
   - intro: The rule is: double, then take away 1.
   - ask: Then subtract 1: 8 − 1 =  [box=7, NO label]
   - ask: Check: reverse it, (7 + 1) ÷ 2 =  [box=4, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: 128m/ssA speed-time graph shows a horizontal line at 12 m/s for 8 seconds. What is the acceleration?
   - ask: The speed starts at 12 and ends at 12, so the change in speed is 12 − 12 =  [box=0, NO label]
   - ask: The time taken is  [box=8, label:' seconds']
   - intro: Acceleration is how fast the speed changes.
   - ask: Acceleration = change in speed ÷ time = 0 ÷ 8 =  [box=0, NO label]
   - ask: Check: acceleration × time = 0 × 8 =  [box=0, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = x_n^2 - 4\) with \(x_0 = 3\). Find \(x_1\).
   - ask: Square the start value: 3² =  [box=9, NO label]
   - intro: The rule is: square, then take away 4.
   - ask: Then subtract 4: 9 − 4 =  [box=5, NO label]
   - ask: Check: 5 + 4 =  [box=9, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: A car speeds up from 0 to 48 m/s in 6 seconds. What is the acceleration?
   - ask: Change in speed: 48 − 0 =  [box=48, NO label]
   - ask: Time taken:  [box=6, label:' seconds']
   - intro: Divide the change in speed by the time.
   - ask: Acceleration = 48 ÷ 6 =  [box=8, NO label]
   - ask: Check: 8 × 6 =  [box=48, NO label]

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: What does the gradient of a distance-time graph represent?

## silver[0] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{10}{x_n + 1}\) with \(x_0 = 3\). Find \(x_2\) to 2 d.p.
   - ask: x₁: denominator 3 + 1 = 4, so 10 ÷ 4 =  [box=2.5, NO label]
   - intro: Feed x₁ back in for x₂.
   - ask: x₂: denominator 2.5 + 1 = 3.5, so 10 ÷ 3.5 to 2 d.p. =  [box=2.86, NO label]
   - ask: Check: 2.86 × 3.5 =  [box=10.01, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: A car decelerates from 25 m/s to 5 m/s in 4 seconds. Find the deceleration.
   - ask: Change in speed (start minus end): 25 − 5 =  [box=20, NO label]
   - intro: Divide the change in speed by the time.
   - ask: Deceleration = 20 ÷ 4 =  [box=5, NO label]
   - ask: Check: 5 × 4 =  [box=20, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{x_n^2 + 5}{2x_n}\) with \(x_0 = 3\). Find \(x_1\) to 3 d.p.
   - ask: Numerator: 3² + 5 =  [box=14, NO label]
   - ask: Denominator: 2 × 3 =  [box=6, NO label]
   - intro: Now divide the numerator by the denominator.
   - ask: x₁ = 14 ÷ 6 to 3 d.p. =  [box=2.333, NO label]
   - ask: Check: 2.333 × 6 (to the nearest whole number) =  [box=14, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(f(x) = x^3 - x - 5\). Show that a root lies between \(x = 1\) and \(x = 2\). What is \(f(2)\)?
   - ask: f(1) = 1³ − 1 − 5 = 1 − 1 − 5 =  [box=-5, NO label]
   - ask: Now 2³ =  [box=8, NO label]
   - intro: Now evaluate f at x = 2.
   - ask: f(2) = 8 − 2 − 5 =  [box=1, NO label]
   - ask: f(1) = −5 (negative) and f(2) is positive. The value asked for, f(2), is  [box=1, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: A car speeds up from 8 m/s to 20 m/s in 3 seconds. Find the acceleration.
   - ask: Change in speed: 20 − 8 =  [box=12, NO label]
   - intro: Divide the change in speed by the time.
   - ask: Acceleration = 12 ÷ 3 =  [box=4, NO label]
   - ask: Check: 4 × 3 =  [box=12, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \sqrt{3x_n + 1}\) with \(x_0 = 1\). Find \(x_2\) to 2 d.p.
   - ask: First iteration, inside the root: 3 × 1 + 1 =  [box=4, NO label]
   - ask: x₁ = √4 =  [box=2, NO label]
   - intro: Feed x₁ back in for x₂.
   - ask: Second iteration, inside the root: 3 × 2 + 1 =  [box=7, NO label]
   - ask: x₂ = √7 to 2 d.p. =  [box=2.65, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \sqrt{2x_n + 3}\) with \(x_0 = 4\). Find \(x_2\) to 3 d.p.
   - ask: First iteration, inside the root: 2 × 4 + 3 =  [box=11, NO label]
   - ask: x₁ = √11 to 4 d.p. =  [box=3.3166, NO label]
   - intro: Feed x₁ back in, keeping full precision.
   - ask: Second iteration, inside the root: 2 × 3.3166 + 3 to 4 d.p. =  [box=9.6332, NO label]
   - ask: x₂ = √9.6332 to 3 d.p. =  [box=3.104, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: A tangent to a curve at \(x = 2\) passes through the points (0, 1) and (4, 13). Find the rate of change at \(x = 2\).
   - ask: Rise (top y minus bottom y): 13 − 1 =  [box=12, NO label]
   - ask: Run (right x minus left x): 4 − 0 =  [box=4, NO label]
   - intro: The rate of change is the gradient of the tangent.
   - ask: Rate of change = rise ÷ run = 12 ÷ 4 =  [box=3, NO label]
   - ask: Check: 3 × 4 =  [box=12, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Use \(x_{n+1} = \frac{2x_n^3 + 5}{3x_n^2}\) with \(x_0 = 2\). Find \(x_2\) to 3 d.p.
   - ask: x₁ numerator: 2 × 2³ + 5 = 2 × 8 + 5 =  [box=21, NO label]
   - ask: x₁ denominator: 3 × 2² = 3 × 4 =  [box=12, NO label]
   - intro: Now feed x₁ back into the same formula for x₂.
   - ask: x₁ = 21 ÷ 12 =  [box=1.75, NO label]
   - ask: x₂ = (2 × 1.75³ + 5) ÷ (3 × 1.75²) to 3 d.p. =  [box=1.711, NO label]
   - ask: Check: 1.711³ to the nearest whole number =  [box=5, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The population \(P\) of a town is modelled by \(P = 2000 \times 1.05^t\), where \(t\) is in years. Find the average rate of change between \(t = 0\) and \(t = 10\), to the nearest whole number.
   - ask: P(0) = 2000 × 1.05⁰ =  [box=2000, NO label]
   - ask: P(10) = 2000 × 1.05¹⁰, to the nearest whole number =  [box=3258, NO label]
   - intro: The average rate of change is the total change over the time.
   - ask: Change in P = 3258 − 2000 =  [box=1258, NO label]
   - ask: Rate = 1258 ÷ 10 = 125.8, to the nearest whole number =  [box=126, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: 01234014916xUse the trapezium rule with 4 strips (each of width 1) to estimate the area under \(y = x^2\) from \(x = 0\) to \(x = 4\). The heights are 0, 1, 4, 9 and 16.Diagram not drawn accurately
   - ask: Height at x = 2: 2² =  [box=4, NO label]
   - ask: Height at x = 3: 3² =  [box=9, NO label]
   - ask: Add the two end heights: 0 + 16 =  [box=16, NO label]
   - intro: Now apply the trapezium rule.
   - ask: Double the middle heights: 2 × (1 + 4 + 9) =  [box=28, NO label]
   - ask: Area = ½ × 1 × (16 + 28) =  [box=22, label:'cm²']

## gold[4] (input: single_value, main-box unit: (none))
Q: An iteration converges to the solution of \(x = \sqrt{2x + 15}\). Find the positive value it converges to.
   - intro: When the iteration settles, x stops changing, so \(x = \sqrt{2x + 15}\). Square both sides: \(x^2 = 2x + 15\), which rearranges to \(x^2 - 2x - 15 = 0\).
   - ask: Two numbers that multiply to −15 and add to −2: one is −5, the other is  [box=3, NO label]
   - intro: Set each bracket to zero to find the roots.
   - ask: So (x − 5)(x + 3) = 0. The negative root is x =  [box=-3, NO label]
   - ask: The question wants the positive value, so x =  [box=5, NO label]
   - ask: Check: 2 × 5 + 15 =  [box=25, NO label]
