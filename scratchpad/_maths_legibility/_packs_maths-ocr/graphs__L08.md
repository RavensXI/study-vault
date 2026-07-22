# maths-ocr / graphs / L08 - Gradients of Curves & Areas Under Graphs

## bronze[0] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((2, 4)\) and \((6, 12)\). Find the gradient.
   - intro: Gradient is the rise (change in y) divided by the run (change in x). Find the rise first:
   - ask: 12 − 4 =  [box=8, NO label]
   - ask: 6 − 2 =  [box=4, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 8 ÷ 4 =  [box=2, NO label]
   - intro: Check by walking from the first point. Moving 4 across should change y by 4 × 2 = 8:
   - ask: 4 + (8) =  [box=12, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((1, 5)\) and \((3, 11)\). Find the gradient.
   - intro: Gradient is the rise (change in y) divided by the run (change in x). Find the rise first:
   - ask: 11 − 5 =  [box=6, NO label]
   - ask: 3 − 1 =  [box=2, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 6 ÷ 2 =  [box=3, NO label]
   - intro: Check by walking from the first point. Moving 2 across should change y by 2 × 3 = 6:
   - ask: 5 + (6) =  [box=11, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((0, 2)\) and \((2, 10)\). Find the gradient.
   - intro: Gradient is the rise (change in y) divided by the run (change in x). Find the rise first:
   - ask: 10 − 2 =  [box=8, NO label]
   - ask: 2 − 0 =  [box=2, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - intro: Check by walking from the first point. Moving 2 across should change y by 2 × 4 = 8:
   - ask: 2 + (8) =  [box=10, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: 35Estimate the area of a rectangle: width 3, height 5.
   - intro: The area under a flat section is a rectangle: base × height. Read the base:
   - ask: base =  [box=3, NO label]
   - ask: height =  [box=5, NO label]
   - intro: Multiply base by height.
   - ask: 3 × 5 =  [box=15, NO label]
   - intro: Check by adding five lots of 3:
   - ask: 3 + 3 + 3 + 3 + 3 =  [box=15, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: 46Diagram not drawn accuratelyEstimate the area of a triangle: base 4, height 6.
   - intro: A triangle is half of the rectangle around it. Find base × height first:
   - ask: 4 × 6 =  [box=24, NO label]
   - intro: A triangle is half that rectangle.
   - ask: 24 ÷ 2 =  [box=12, NO label]
   - intro: Check the other way: halve the base first, ½ × 4 = 2, then times height:
   - ask: 2 × 6 =  [box=12, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: A tangent to a curve at \(x = 2\) has gradient 5. Is the curve increasing or decreasing here? Enter 1 for increasing, 0 for decreasing.
   - intro: A gradient is the slope of the tangent. The gradient here is 5. Is 5 greater than 0? Enter 1 for yes, 0 for no:
   - ask: answer =  [box=1, NO label]
   - intro: A positive slope goes uphill as x increases, which means the curve is increasing.
   - ask: enter 1 for increasing =  [box=1, NO label]
   - intro: Check: a line of slope 5 rises steeply from left to right, so y is going up.
   - ask: confirm increasing, enter 1 =  [box=1, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: 464Diagram not drawn accuratelyA trapezium has parallel sides 4 and 6, height 4. Find the area.
   - intro: A trapezium's area is the average of the two parallel sides, times the height. Add the parallel sides:
   - ask: 4 + 6 =  [box=10, NO label]
   - ask: average them: 10 ÷ 2 =  [box=5, NO label]
   - intro: Multiply the average by the height 4.
   - ask: 5 × 4 =  [box=20, NO label]
   - intro: Check with the full formula ½(a + b)h = ½ × 10 × 4:
   - ask: ½ × 10 × 4 =  [box=20, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: (3, 7)(5, 7)A tangent passes through \((3, 7)\) and \((5, 7)\). Find the gradient.
   - intro: Gradient is rise over run. Find the rise (change in y) first:
   - ask: 7 − 7 =  [box=0, NO label]
   - ask: run: 5 − 3 =  [box=2, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 0 ÷ 2 =  [box=0, NO label]
   - intro: A gradient of 0 means the tangent is flat. Both points sit at the same height, so the tangent is horizontal. Confirm the gradient:
   - ask: gradient =  [box=0, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 2\), y-values: 1, 6, 13. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 1 + 13 =  [box=14, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × 6 =  [box=12, NO label]
   - ask: 14 + 12 =  [box=26, NO label]
   - intro: Multiply by h ÷ 2 = 2 ÷ 2 = 1:
   - ask: 1 × 26 =  [box=26, NO label]
   - intro: Check by adding the trapezia one at a time (7 + 19):
   - ask: 7 + 19 =  [box=26, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 1\), y-values: 0, 1, 4, 9. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 0 + 9 =  [box=9, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × (1 + 4) =  [box=10, NO label]
   - ask: 9 + 10 =  [box=19, NO label]
   - intro: Multiply by h ÷ 2 = 1 ÷ 2 = 0.5:
   - ask: 0.5 × 19 =  [box=9.5, NO label]
   - intro: Check by adding the trapezia one at a time (0.5 + 2.5 + 6.5):
   - ask: 0.5 + 2.5 + 6.5 =  [box=9.5, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((-1, 6)\) and \((3, -2)\). Find the gradient.
   - intro: Gradient is the rise (change in y) divided by the run (change in x). Find the rise first:
   - ask: -2 − 6 =  [box=-8, NO label]
   - ask: 3 − -1 =  [box=4, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: -8 ÷ 4 =  [box=-2, NO label]
   - intro: Check by walking from the first point. Moving 4 across should change y by 4 × -2 = -8:
   - ask: 6 + (-8) =  [box=-2, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 0.5\), y-values: 2, 3, 5, 8, 12. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 2 + 12 =  [box=14, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × (3 + 5 + 8) =  [box=32, NO label]
   - ask: 14 + 32 =  [box=46, NO label]
   - intro: Multiply by h ÷ 2 = 0.5 ÷ 2 = 0.25:
   - ask: 0.25 × 46 =  [box=11.5, NO label]
   - intro: Check by adding the trapezia one at a time (1.25 + 2 + 3.25 + 5):
   - ask: 1.25 + 2 + 3.25 + 5 =  [box=11.5, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: gradient = 0A curve has gradient 0 at \(x = 3\). What does this tell you?

## silver[5] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 1\), y-values: 2, 4, 8. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 2 + 8 =  [box=10, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × 4 =  [box=8, NO label]
   - ask: 10 + 8 =  [box=18, NO label]
   - intro: Multiply by h ÷ 2 = 1 ÷ 2 = 0.5:
   - ask: 0.5 × 18 =  [box=9, NO label]
   - intro: Check by adding the trapezia one at a time (3 + 6):
   - ask: 3 + 6 =  [box=9, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 2\), y-values: 0, 4, 16. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 0 + 16 =  [box=16, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × 4 =  [box=8, NO label]
   - ask: 16 + 8 =  [box=24, NO label]
   - intro: Multiply by h ÷ 2 = 2 ÷ 2 = 1:
   - ask: 1 × 24 =  [box=24, NO label]
   - intro: Check by adding the trapezia one at a time (4 + 20):
   - ask: 4 + 20 =  [box=24, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 1\), y-values: 1, 2, 5, 10, 17. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 1 + 17 =  [box=18, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × (2 + 5 + 10) =  [box=34, NO label]
   - ask: 18 + 34 =  [box=52, NO label]
   - intro: Multiply by h ÷ 2 = 1 ÷ 2 = 0.5:
   - ask: 0.5 × 52 =  [box=26, NO label]
   - intro: Check by adding the trapezia one at a time (1.5 + 3.5 + 7.5 + 13.5):
   - ask: 1.5 + 3.5 + 7.5 + 13.5 =  [box=26, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The area under a speed-time graph is the distance travelled. Speeds at t = 0, 2, 4, 6 are 0, 8, 12, 20 m/s. Use the trapezium rule (h = 2) to estimate the distance.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 0 + 20 =  [box=20, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × (8 + 12) =  [box=40, NO label]
   - ask: 20 + 40 =  [box=60, NO label]
   - intro: Multiply by h ÷ 2 = 2 ÷ 2 = 1:
   - ask: 1 × 60 =  [box=60, NO label]
   - intro: Check by adding the trapezia one at a time (8 + 20 + 32):
   - ask: 8 + 20 + 32 =  [box=60, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The trapezium rule gives area 48.5. The exact area is 45. Find the percentage error to 1 d.p.
   - intro: Percentage error = (size of error ÷ true value) × 100. First the size of the error:
   - ask: 48.5 − 45 =  [box=3.5, NO label]
   - intro: Divide by the true value 45, then multiply by 100.
   - ask: 3.5 ÷ 45 × 100 =  [box=7.8, NO label]
   - intro: Check: 7.8% of 45 should give back the error. 0.078 × 45 ≈ 3.5:
   - ask: enter the error, 3.5 =  [box=3.5, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: A curve has \(y = x^3\). Estimate the gradient at \(x = 2\) using \((1.9, 6.859)\) and \((2.1, 9.261)\).
   - intro: Estimate the gradient with a chord between the two nearby points. Find the rise:
   - ask: 9.261 − 6.859 =  [box=2.402, NO label]
   - ask: run: 2.1 − 1.9 =  [box=0.2, NO label]
   - intro: Gradient = rise ÷ run.
   - ask: 2.402 ÷ 0.2 =  [box=12.01, NO label]
   - intro: Check against the exact gradient. For \(y = x^3\) it is \(3x^2\), and at x = 2 that is 3 × 4:
   - ask: 3 × 4 =  [box=12, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Trapezium rule: \(h = 0.5\), y-values: 1, 1.5, 2.5, 4, 6. Find the area.
   - intro: Trapezium rule: add the first and last heights, add double the inside heights, then multiply by h ÷ 2. Start with the two end heights:
   - ask: 1 + 6 =  [box=7, NO label]
   - intro: Now the inside heights, each counted twice:
   - ask: 2 × (1.5 + 2.5 + 4) =  [box=16.0, NO label]
   - ask: 7 + 16 =  [box=23.0, NO label]
   - intro: Multiply by h ÷ 2 = 0.5 ÷ 2 = 0.25:
   - ask: 0.25 × 23 =  [box=5.75, NO label]
   - intro: Check by adding the trapezia one at a time (0.625 + 1 + 1.625 + 2.5):
   - ask: 0.625 + 1 + 1.625 + 2.5 =  [box=5.75, NO label]
