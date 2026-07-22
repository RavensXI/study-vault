# apply-pack: ratio-proportion__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[2] | P(0) = 5000 × 1.03⁰ = [box=5000] | fix: Add a line first: 'Anything to the power 0 equals 1, so 1.03⁰ = 1' before asking for P(0).
- [medium] gold[2] | Add the two end heights: 0 + 16 = [box=16] ... Double the middle heights: 2 × (1 | fix: Add explicit ask steps for the missing heights first (y at x=0 is 0², y at x=1 is 1², y at x=4 is 4² = 16), then state the trapezium rule in words before the '½
- [high] bronze[0], bronze[1], bronze[4] | text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}xy( | fix: Strip the leaked SVG/CSS and render the graph as an actual image/SVG. Start the stem cleanly at 'A tangent passes through (1, 3) and (5, 11). Find the rate of c
- [medium] gold[2] | x2 = 14.1113 ÷ 5.3334 = [box=2.6458, NO label] | fix: Add an explicit denominator step before the division, e.g. 'Denominator: 2 × 2.6667 = [box=5.3334]', matching how the x1 step should also show its denominator.
- [medium] gold[1] | Show x^3 - 5x - 4 = 0 can be rearranged to x = cbrt(5x+4). This is the iteration | fix: Reduce to a single clear instruction, e.g. 'The equation being solved is x^3 - 5x - 4 = 0. The constant term is the number with no x. Enter it.' and add a one-l
- [medium] bronze[0] | Q: 804kmhoursA distance-time graph is a straight line from the origin to the poi | fix: Delete the leading "804kmhours" so the stem starts "A distance-time graph is a straight line from the origin to the point (4, 80)..."
- [medium] bronze[4] | Q: 128m/ssA speed-time graph shows a horizontal line at 12 m/s for 8 seconds... | fix: Delete the leading "128m/ss" so the stem starts "A speed-time graph shows a horizontal line at 12 m/s for 8 seconds..."
- [medium] gold[3] | Q: 01234014916xUse the trapezium rule with 4 strips (each of width 1)... The hei | fix: Delete the leading "01234014916x" so it starts "Use the trapezium rule...", and put a space/line break before "Diagram not drawn accurately"

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: Find the average rate of change of \(y = x^2\) between \(x = 1\) and \(x = 3\).
   step0 field=say answer=None text='Average rate of change = (change in y) ÷ (change in x).'
   step1 field=pre answer=1 text='f(1) = 1² ='
   step2 field=pre answer=9 text='f(3) = 3² ='
   step3 field=pre answer=8 text='Change in y = 9 − 1 ='
   step4 field=pre answer=2 text='Change in x = 3 − 1 ='
   step5 field=pre answer=4 text='Rate = 8 ÷ 2 ='

bronze[4] Q: Using \(x_{n+1} = x_n + 3\) with \(x_0 = 2\), find \(x_1\).
   step0 field=say answer=None text='Iteration means putting the current value into the formula to get the next one. Here x_{n+'
   step1 field=pre answer=3 text='The starting value is x₀ = 2. What do we add each time?'
   step2 field=pre answer=5 text='x₁ = x₀ + 3 = 2 + 3 ='
   step3 field=pre answer=3 text='Check: x₁ − x₀ should equal 3. Work out 5 − 2 ='

gold[1] Q: \(f(x) = x^3 + 2x - 7\). Show a root lies between 1 and 2. What is \(f(1.5)\) to 3 d.p.?
   step0 field=say answer=None text='f(x) = x³ + 2x − 7. First check the interval, then find f(1.5).'
   step1 field=pre answer=-4 text='f(1) = 1 + 2 − 7 ='
   step2 field=pre answer=5 text='f(2) = 8 + 4 − 7 ='
   step3 field=pre answer=3.375 text='Sign change between 1 and 2. Now 1.5³ ='
   step4 field=pre answer=-0.625 text='f(1.5) = 3.375 + 2(1.5) − 7 = 3.375 + 3 − 7 ='

gold[2] Q: The population P of a town is modelled by \(P = 5000 \times 1.03^t\). Find the average ann
   step0 field=say answer=None text='Average rate = (P at t = 10 − P at t = 0) ÷ (10 − 0).'
   step1 field=pre answer=5000 text='P(0) = 5000 × 1.03⁰ ='
   step2 field=pre answer=6720 text='P(10) = 5000 × 1.03¹⁰, to the nearest whole number ='
   step3 field=pre answer=1720 text='Change in P = 6720 − 5000 ='
   step4 field=pre answer=172 text='Rate = 1720 ÷ 10 ='

gold[3] Q: Using \(x_{n+1} = \sqrt{3x_n + 1}\) with \(x_0 = 3\), find \(x_2\) to 3 d.p.
   step0 field=say answer=None text='Two iterations of x_{n+1} = √(3x_n + 1) from x₀ = 3.'
   step1 field=pre answer=10 text='First iteration inside the root: 3 × 3 + 1 ='
   step2 field=pre answer=3.162 text='x₁ = √10 to 3 d.p. ='
   step3 field=pre answer=10.486 text='Now use x₁ = 3.162. Inside the next root: 3 × 3.162 + 1 ='
   step4 field=pre answer=3.238 text='x₂ = √10.486 to 3 d.p. ='

### board=maths-edexcel
bronze[0] Q: A tangent passes through \((2, 5)\) and \((6, 13)\). Find the gradient.
   step0 field=pre answer=8 text='Rise (top y minus bottom y): 13 − 5 ='
   step1 field=pre answer=4 text='Run (right x minus left x): 6 − 2 ='
   step2 field=pre answer=2 text='Gradient = rise ÷ run = 8 ÷ 4 ='
   step3 field=pre answer=8 text='Check: a gradient of 2 over a run of 4 should climb 2 × 4 ='

bronze[4] Q: A tangent passes through \((1, 2)\) and \((5, 22)\). What is the rate of change?
   step0 field=pre answer=20 text='Rise: 22 − 2 ='
   step1 field=pre answer=4 text='Run: 5 − 1 ='
   step2 field=pre answer=5 text='Rate of change = rise ÷ run = 20 ÷ 4 ='
   step3 field=pre answer=20 text='Check: 5 × 4 ='

gold[1] Q: Show that \(x^3 - 5x + 1 = 0\) has a root between \(x = 2\) and \(x = 3\). What is \(f(2)\
   step0 field=pre answer=8 text='First 2³ ='
   step1 field=pre answer=10 text='and 5 × 2 ='
   step2 field=pre answer=-1 text='f(2) = 8 − 10 + 1 ='
   step3 field=pre answer=13 text='Now f(3): 3³ − 5 × 3 + 1 = 27 − 15 + 1 ='
   step4 field=pre answer=-1 text='f(2) is negative and f(3) is positive, so a root lies between. The value asked for, f(2), '

gold[2] Q: Use the trapezium rule with 4 strips to estimate the area under \(y = x^2\) from \(x = 0\)
   step0 field=pre answer=4 text='Heights y = x² at x = 0, 1, 2, 3, 4. The one at x = 2 is 2² ='
   step1 field=pre answer=9 text='and the one at x = 3 is 3² ='
   step2 field=pre answer=16 text='Add the two end heights: 0 + 16 ='
   step3 field=pre answer=28 text='Double the middle heights: 2 × (1 + 4 + 9) ='
   step4 field=pre answer=22 text='Area = ½ × 1 × (16 + 28) ='

gold[3] Q: Use \(x_{n+1} = 5 - \frac{1}{x_n^2}\) with \(x_0 = 2\). Find \(x_3\) to 4 d.p.
   step0 field=pre answer=4.75 text='x₁ = 5 − 1 ÷ 2² = 5 − 1 ÷ 4 = 5 − 0.25 ='
   step1 field=pre answer=22.5625 text='For x₂, the denominator 4.75² ='
   step2 field=pre answer=4.9557 text='x₂ = 5 − 1 ÷ 22.5625, to 4 d.p. ='
   step3 field=pre answer=4.9593 text='x₃ = 5 − 1 ÷ 4.9557², to 4 d.p. ='
   step4 field=pre answer=0.0407 text='Check: 5 − 4.9593 ='

### board=maths-ocr
bronze[0] Q: text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}xy(1, 3)(5, 1
   step0 field=say answer=None text="A straight tangent's rate of change is its gradient: rise over run."
   step1 field=pre answer=8 text='Change in y: 11 − 3 ='
   step2 field=pre answer=4 text='Change in x: 5 − 1 ='
   step3 field=pre answer=2 text='8 ÷ 4 ='
   step4 field=pre answer=11 text='Check from (1, 3): 3 + 4 × 2 ='

bronze[4] Q: text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}xy(1, -2)(5, 
   step0 field=pre answer=16 text='Change in y: 14 − (−2) ='
   step1 field=pre answer=4 text='Change in x: 5 − 1 ='
   step2 field=pre answer=4 text='16 ÷ 4 ='
   step3 field=pre answer=14 text='Check from (1, −2): −2 + 4 × 4 ='

gold[1] Q: Show \(x^3 - 5x - 4 = 0\) can be rearranged to \(x = \sqrt[3]{5x+4}\). This is the iterati
   step0 field=say answer=None text='Cube both sides of x = ∛(5x + 4) to get x³ = 5x + 4.'
   step1 field=pre answer=1 text='The coefficient of x³ is'
   step2 field=pre answer=-5 text='The coefficient of x becomes'
   step3 field=pre answer=-4 text='The constant term becomes'

gold[2] Q: \(x_{n+1} = \frac{x_n^2 + 7}{2x_n}\). \(x_0 = 3\). Find \(x_2\) to 4 d.p.
   step0 field=say answer=None text='x₀² = 9, so the numerator is 9 + 7.'
   step1 field=pre answer=16 text='x₁ numerator: 9 + 7 ='
   step2 field=pre answer=2.6667 text='x₁ = 16 ÷ 6 ='
   step3 field=pre answer=7.1113 text='x₁²: 2.6667² ='
   step4 field=pre answer=14.1113 text='New numerator: 7.1113 + 7 ='
   step5 field=pre answer=2.6458 text='x₂ = 14.1113 ÷ 5.3334 ='

gold[3] Q: An iteration converges to \(x = 2.646\) to 3 d.p. This is a solution to which equation?

### board=maths-eduqas
bronze[0] Q: 804kmhoursA distance-time graph is a straight line from the origin to the point (4, 80), w
   step0 field=pre answer=80 text='Distance travelled (the y-value at the end):'
   step1 field=pre answer=4 text='Time taken (the x-value at the end):'
   step2 field=pre answer=20 text='Speed = distance ÷ time = 80 ÷ 4 ='
   step3 field=pre answer=80 text='Check: speed × time = 20 × 4 ='

bronze[4] Q: 128m/ssA speed-time graph shows a horizontal line at 12 m/s for 8 seconds. What is the acc
   step0 field=pre answer=0 text='The speed starts at 12 and ends at 12, so the change in speed is 12 − 12 ='
   step1 field=pre answer=8 text='The time taken is'
   step2 field=pre answer=0 text='Acceleration = change in speed ÷ time = 0 ÷ 8 ='
   step3 field=pre answer=0 text='Check: acceleration × time = 0 × 8 ='

gold[1] Q: Use \(x_{n+1} = \frac{2x_n^3 + 5}{3x_n^2}\) with \(x_0 = 2\). Find \(x_2\) to 3 d.p.
   step0 field=pre answer=21 text='x₁ numerator: 2 × 2³ + 5 = 2 × 8 + 5 ='
   step1 field=pre answer=12 text='x₁ denominator: 3 × 2² = 3 × 4 ='
   step2 field=pre answer=1.75 text='x₁ = 21 ÷ 12 ='
   step3 field=pre answer=1.711 text='x₂ = (2 × 1.75³ + 5) ÷ (3 × 1.75²) to 3 d.p. ='
   step4 field=pre answer=5 text='Check: 1.711³ to the nearest whole number ='

gold[2] Q: The population \(P\) of a town is modelled by \(P = 2000 \times 1.05^t\), where \(t\) is i
   step0 field=pre answer=2000 text='P(0) = 2000 × 1.05⁰ ='
   step1 field=pre answer=3258 text='P(10) = 2000 × 1.05¹⁰, to the nearest whole number ='
   step2 field=pre answer=1258 text='Change in P = 3258 − 2000 ='
   step3 field=pre answer=126 text='Rate = 1258 ÷ 10 = 125.8, to the nearest whole number ='

gold[3] Q: 01234014916xUse the trapezium rule with 4 strips (each of width 1) to estimate the area un
   step0 field=pre answer=4 text='Height at x = 2: 2² ='
   step1 field=pre answer=9 text='Height at x = 3: 3² ='
   step2 field=pre answer=16 text='Add the two end heights: 0 + 16 ='
   step3 field=pre answer=28 text='Double the middle heights: 2 × (1 + 4 + 9) ='
   step4 field=pre answer=22 text='Area = ½ × 1 × (16 + 28) ='
