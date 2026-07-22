# maths-aqa / graphs / L08 - Gradients of Curves & Areas Under Graphs

## bronze[0] (input: single_value, main-box unit: (none))
Q: A tangent to a curve passes through \((1, 3)\) and \((5, 11)\). What is the gradient of the tangent?
   - intro: Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the run (the change in x).
   - ask: rise: 11 − 3 =  [box=8, NO label]
   - ask: run: 5 − 1 =  [box=4, NO label]
   - intro: Now divide the rise by the run.
   - ask: gradient: 8 ÷ 4 =  [box=2, NO label]
   - ask: check, from (1, 3) go across 4 and up gradient×run: 3 + (2)×4 =  [box=11, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((2, 10)\) and \((6, 2)\). Find the gradient.
   - intro: Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the run (the change in x).
   - ask: rise: 2 − 10 =  [box=-8, NO label]
   - ask: run: 6 − 2 =  [box=4, NO label]
   - intro: Now divide the rise by the run.
   - ask: gradient: -8 ÷ 4 =  [box=-2, NO label]
   - ask: check, from (2, 10) go across 4 and up gradient×run: 10 + (-2)×4 =  [box=2, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: base = 6height = 8Diagram not drawn accuratelyEstimate the area of a triangle with base 6 and height 8.
   - intro: Area of a triangle = ½ × base × height.
   - ask: base × height: 6 × 8 =  [box=48, NO label]
   - intro: A triangle is half of that rectangle.
   - ask: ½ × 48 =  [box=24, NO label]
   - ask: check by doubling: 2 × 24 =  [box=48, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: 104height = 3Diagram not drawn accuratelyEstimate the area of a trapezium with parallel sides 4 and 10 and height 3.
   - intro: Area of a trapezium = ½ × (sum of the parallel sides) × height.
   - ask: sum of the parallel sides: 4 + 10 =  [box=14, NO label]
   - ask: × height: 14 × 3 =  [box=42, NO label]
   - intro: Now halve it.
   - ask: ½ × 42 =  [box=21, NO label]
   - ask: check by doubling: 2 × 21 =  [box=42, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: 04812012345time (s)speed (m/s)5 s12 m/sArea under speed-time = distanceA rectangle on a speed-time graph has width 5 s and height 12 m/s. What area (distance) does it represent?
   - intro: On a speed-time graph the distance is the area of the shape. This is a rectangle: width × height.
   - ask: width in seconds: read it off =  [box=5, NO label]
   - ask: height in m/s: read it off =  [box=12, NO label]
   - intro: Multiply width by height for the area.
   - ask: area: 5 × 12 =  [box=60, label:'cm²']
   - ask: check the speed back: 60 ÷ 5 =  [box=12, NO label]

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: A tangent at a point on a distance-time graph has gradient 15. What does this represent?

## bronze[6] (input: single_value, main-box unit: (none))
Q: 051015200246810time (s)speed (m/s)10 s20 m/sArea under speed-time = distanceOn a speed-time graph, a triangular area has base 10 s and height 20 m/s. What distance does it represent?
   - intro: Distance = area under the speed-time graph. This is a triangle: ½ × base × height.
   - ask: base × height: 10 × 20 =  [box=200, NO label]
   - intro: A triangle is half of that rectangle.
   - ask: ½ × 200 =  [box=100, NO label]
   - ask: check by doubling: 2 × 100 =  [box=200, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: A tangent to a curve at \(x = 2\) passes through \((1, 2)\) and \((3, 12)\). What is the gradient at \(x = 2\)?
   - intro: Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the run (the change in x).
   - ask: rise: 12 − 2 =  [box=10, NO label]
   - ask: run: 3 − 1 =  [box=2, NO label]
   - intro: Now divide the rise by the run.
   - ask: gradient: 10 ÷ 2 =  [box=5, NO label]
   - ask: check, from (1, 2) go across 2 and up gradient×run: 2 + (5)×2 =  [box=12, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with 3 strips (\(h = 2\)) and y-values 0, 4, 12, 24 to estimate the area.
   - intro: Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].
   - ask: add the middle values: 4 + 12 =  [box=16, NO label]
   - ask: double them: 2 × 16 =  [box=32, NO label]
   - ask: first + last: 0 + 24 =  [box=24, NO label]
   - ask: bracket total: 24 + 32 =  [box=56, NO label]
   - intro: Now multiply by h ÷ 2 to finish.
   - ask: h ÷ 2 = 2 ÷ 2 =  [box=1, NO label]
   - ask: A = 1 × 56 =  [box=56, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with \(h = 1\), y-values: 1, 4, 9, 16. Estimate the area.
   - intro: Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].
   - ask: add the middle values: 4 + 9 =  [box=13, NO label]
   - ask: double them: 2 × 13 =  [box=26, NO label]
   - ask: first + last: 1 + 16 =  [box=17, NO label]
   - ask: bracket total: 17 + 26 =  [box=43, NO label]
   - intro: Now multiply by h ÷ 2 to finish.
   - ask: h ÷ 2 = 1 ÷ 2 =  [box=0.5, label:'(a decimal)']
   - ask: A = 0.5 × 43 =  [box=21.5, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: 051005101520time (s)speed (m/s)10 m/sArea = total distanceA speed-time graph shows: speed 0 at t=0, speed 10 at t=5, speed 10 at t=15, speed 0 at t=20. Estimate the total distance.
   - intro: Split the journey into a triangle, a rectangle, then a triangle, and add the areas.
   - ask: speeding up, t = 0 to 5: ½ × 5 × 10 =  [box=25, NO label]
   - ask: steady, t = 5 to 15: 10 × 10 =  [box=100, NO label]
   - ask: slowing down, t = 15 to 20: ½ × 5 × 10 =  [box=25, NO label]
   - intro: Add the three pieces for the total distance.
   - ask: total: 25 + 100 + 25 =  [box=150, NO label]
   - ask: check as one trapezium: ½ × (10 + 20) × 10 =  [box=150, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: A tangent at \(x = 2\) on \(y = x^2\) passes through \((0, -4)\) and \((3, 8)\). Find the gradient.
   - intro: Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the run (the change in x).
   - ask: rise: 8 − (-4) =  [box=12, NO label]
   - ask: run: 3 − 0 =  [box=3, NO label]
   - intro: Now divide the rise by the run.
   - ask: gradient: 12 ÷ 3 =  [box=4, NO label]
   - ask: check, from (0, -4) go across 3 and up gradient×run: -4 + (4)×3 =  [box=8, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with 4 strips (\(h = 1\)) and y-values 0, 3, 8, 15, 24. Estimate the area.
   - intro: Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].
   - ask: add the middle values: 3 + 8 + 15 =  [box=26, NO label]
   - ask: double them: 2 × 26 =  [box=52, NO label]
   - ask: first + last: 0 + 24 =  [box=24, NO label]
   - ask: bracket total: 24 + 52 =  [box=76, NO label]
   - intro: Now multiply by h ÷ 2 to finish.
   - ask: h ÷ 2 = 1 ÷ 2 =  [box=0.5, label:'(a decimal)']
   - ask: A = 0.5 × 76 =  [box=38, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Estimate the area under a curve between \(x = 0\) and \(x = 6\) using 3 strips. y-values: 0, 6, 8, 6.
   - intro: Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].
   - ask: strip width h = span ÷ strips = 6 ÷ 3 =  [box=2, NO label]
   - ask: add the middle values: 6 + 8 =  [box=14, NO label]
   - ask: double them: 2 × 14 =  [box=28, NO label]
   - ask: first + last: 0 + 6 =  [box=6, NO label]
   - ask: bracket total: 6 + 28 =  [box=34, NO label]
   - intro: Now multiply by h ÷ 2 to finish.
   - ask: h ÷ 2 = 2 ÷ 2 =  [box=1, NO label]
   - ask: A = 1 × 34 =  [box=34, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: A tangent to a distance-time curve at \(t = 5\) has gradient 12. What is the speed at \(t = 5\)?
   - intro: On a distance-time graph, the gradient at a point is the instantaneous speed there.
   - ask: read the gradient of the tangent =  [box=12, NO label]
   - intro: Speed equals that gradient.
   - ask: so the speed at t = 5 =  [box=12, NO label]
   - ask: check the units: 12 metres per second means in 1 s distance rises 12 ÷ 1 =  [box=12, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with 5 strips (\(h = 1\)) and y-values 1, 2, 5, 10, 17, 26. Estimate the area.
   - intro: Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].
   - ask: add the middle values: 2 + 5 + 10 + 17 =  [box=34, NO label]
   - ask: double them: 2 × 34 =  [box=68, NO label]
   - ask: first + last: 1 + 26 =  [box=27, NO label]
   - ask: bracket total: 27 + 68 =  [box=95, NO label]
   - intro: Now multiply by h ÷ 2 to finish.
   - ask: h ÷ 2 = 1 ÷ 2 =  [box=0.5, label:'(a decimal)']
   - ask: A = 0.5 × 95 =  [box=47.5, NO label]

## gold[1] (input: multiple_choice, main-box unit: (none))
Q: The area under a speed-time curve from \(t = 0\) to \(t = 10\) is estimated as 85 m using the trapezium rule. The exact area is 83 m. Is the trapezium rule an overestimate or underestimate?

## gold[2] (input: single_value, main-box unit: (none))
Q: On \(y = x^3\), a tangent at \(x = 2\) passes through \((1, -4)\) and \((3, 20)\). Find the gradient.
   - intro: Gradient of a straight tangent = rise ÷ run. First the rise (the change in y), then the run (the change in x).
   - ask: rise: 20 − (-4) =  [box=24, NO label]
   - ask: run: 3 − 1 =  [box=2, NO label]
   - intro: Now divide the rise by the run.
   - ask: gradient: 24 ÷ 2 =  [box=12, NO label]
   - ask: check, from (1, -4) go across 2 and up gradient×run: -4 + (12)×2 =  [box=20, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with \(h = 0.5\) and y-values 0, 0.25, 1, 2.25, 4 to estimate the area under \(y = x^2\) from 0 to 2.
   - intro: Trapezium rule: A = (h ÷ 2) × [first + last + 2 × (all the middle values)].
   - ask: add the middle values: 0.25 + 1 + 2.25 =  [box=3.5, NO label]
   - ask: double them: 2 × 3.5 =  [box=7, NO label]
   - ask: first + last: 0 + 4 =  [box=4, NO label]
   - ask: bracket total: 4 + 7 =  [box=11, NO label]
   - intro: Now multiply by h ÷ 2 to finish.
   - ask: h ÷ 2 = 0.5 ÷ 2 =  [box=0.25, label:'(a decimal)']
   - ask: A = 0.25 × 11 =  [box=2.75, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: Explain why using more strips in the trapezium rule gives a better estimate. What happens to the accuracy as the number of strips increases?
