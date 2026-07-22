# maths-edexcel / graphs / L08 - Gradients of Curves & Areas Under Graphs

## bronze[0] (input: single_value, main-box unit: (none))
Q: A tangent line passes through \((2, 4)\) and \((6, 12)\). What is the gradient?
   - intro: A tangent is a straight line, so its gradient is the change in y divided by the change in x. Work out each change first, keeping both subtractions in the same order.
   - ask: change in y: 12 − 4 =  [box=8, NO label]
   - ask: change in x: 6 − 2 =  [box=4, NO label]
   - intro: Now divide to get the gradient:
   - ask: gradient = 8 ÷ 4 =  [box=2, NO label]
   - intro: Check: from x = 2 to x = 6 is a run of 4, so at gradient 2 the y-value should climb 2 × 4 = 8, from 4 up to 12.
   - ask: 4 + 2 × 4 =  [box=12, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: A tangent line passes through \((0, 5)\) and \((4, 1)\). What is the gradient?
   - intro: Gradient is the change in y over the change in x. Take both points in the same order and keep track of the minus sign.
   - ask: change in y: 1 − 5 =  [box=-4, NO label]
   - ask: change in x: 4 − 0 =  [box=4, NO label]
   - intro: Now divide, keeping the minus:
   - ask: gradient = −4 ÷ 4 =  [box=-1, NO label]
   - intro: Check: starting at y = 5, a gradient of −1 over a run of 4 drops the value by 4.
   - ask: 5 + (−1) × 4 =  [box=1, NO label]

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: To estimate the gradient of a curve at a point, which should you draw?

## bronze[3] (input: single_value, main-box unit: (none))
Q: y = 3y = 7h = 2Diagram not drawn accuratelyEstimate the area of one trapezium with parallel sides \(y = 3\) and \(y = 7\), width \(h = 2\).
   - intro: A trapezium strip is half of (side + side) times the width. Build it one step at a time. First add the two parallel sides:
   - ask: 3 + 7 =  [box=10, NO label]
   - ask: multiply by the width h = 2: 10 × 2 =  [box=20, NO label]
   - intro: Halve it for the trapezium:
   - ask: now halve it: 20 ÷ 2 =  [box=10, NO label]
   - intro: Check another way: the average of the two sides is (3 + 7) ÷ 2 = 5, and area = average height × width.
   - ask: 5 × 2 =  [box=10, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: y = 5y = 5h = 4Diagram not drawn accuratelyEstimate the area of one trapezium with parallel sides \(y = 5\) and \(y = 5\), width \(h = 4\).
   - intro: Same trapezium rule: half of (side + side) times the width. Add the sides first:
   - ask: 5 + 5 =  [box=10, NO label]
   - ask: multiply by the width h = 4: 10 × 4 =  [box=40, NO label]
   - intro: Halve it:
   - ask: now halve it: 40 ÷ 2 =  [box=20, NO label]
   - intro: Check: both sides are 5, so the strip is a 5 by 4 rectangle, area = 5 × 4.
   - ask: 5 × 4 =  [box=20, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: A tangent passes through \((-2, 1)\) and \((2, 13)\). What is the gradient?
   - intro: The tangent is a straight line. Its gradient is the change in y over the change in x. Take both points in the same order, and watch the negative coordinate.
   - ask: change in y: 13 − 1 =  [box=12, NO label]
   - ask: change in x: 2 − (−2) =  [box=4, NO label]
   - intro: Now divide:
   - ask: gradient = 12 ÷ 4 =  [box=3, NO label]
   - intro: Check: from (−2, 1), a run of 4 at gradient 3 climbs 3 × 4 = 12.
   - ask: 1 + 3 × 4 =  [box=13, NO label]

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: On a speed-time graph, what does the area under the curve represent?

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: On a distance-time graph, what does the gradient represent?

## silver[0] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with 2 strips to estimate the area under a curve: \(y_0 = 2, y_1 = 6, y_2 = 8\) at \(x = 0, 3, 6\). Give the strip width \(h\).
   - intro: The strip width h is the total x-range shared equally between the strips. Find the range first.
   - ask: total x-range: 6 − 0 =  [box=6, NO label]
   - ask: number of strips:  [box=2, NO label]
   - intro: Divide the range by the number of strips:
   - ask: strip width h = 6 ÷ 2 =  [box=3, NO label]
   - intro: Check: each gap should equal h. The first gap is from x = 0 to x = 3.
   - ask: 3 − 0 =  [box=3, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with \(h = 3\) and \(y_0 = 2, y_1 = 6, y_2 = 8\) to estimate the area under the curve.
   - intro: The trapezium rule is (h/2) × [first + last + 2 × (middle values)]. Start with the two ends.
   - ask: first + last: 2 + 8 =  [box=10, NO label]
   - ask: the middle value counts twice: 2 × 6 =  [box=12, NO label]
   - ask: bracket total: 10 + 12 =  [box=22, NO label]
   - intro: Now scale by h/2. Here h/2 = 3 ÷ 2 = 1.5:
   - ask: 1.5 × 22 =  [box=33, NO label]
   - intro: Check by strips: strip one is ½(2 + 6) × 3 = 12, strip two is ½(6 + 8) × 3 = 21.
   - ask: 12 + 21 =  [box=33, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: A tangent to the curve \(y = x^2\) at \(x = 3\) passes through \((1, -3)\) and \((5, 21)\). Estimate the gradient at \(x = 3\).
   - intro: Gradient of the tangent is the change in y over the change in x. The lower point has a negative y, so take care with the subtraction.
   - ask: change in y: 21 − (−3) =  [box=24, NO label]
   - ask: change in x: 5 − 1 =  [box=4, NO label]
   - intro: Now divide:
   - ask: gradient = 24 ÷ 4 =  [box=6, NO label]
   - intro: Check: from (1, −3), a run of 4 at gradient 6 climbs 6 × 4 = 24.
   - ask: −3 + 6 × 4 =  [box=21, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: A speed-time graph has values: \(t = 0, v = 0\); \(t = 5, v = 10\); \(t = 10, v = 10\). Use the trapezium rule to estimate the distance. Use 2 strips.
   - intro: Distance is the area under the graph. Use the trapezium rule. First find the strip width h.
   - ask: strip width h = (10 − 0) ÷ 2 =  [box=5, NO label]
   - ask: first + last speed: 0 + 10 =  [box=10, NO label]
   - ask: double the middle: 2 × 10 =  [box=20, NO label]
   - ask: bracket total: 10 + 20 =  [box=30, NO label]
   - intro: Now scale by h/2. Here h/2 = 5 ÷ 2 = 2.5:
   - ask: 2.5 × 30 =  [box=75, NO label]
   - intro: Check by strips: ½(0 + 10) × 5 = 25 and ½(10 + 10) × 5 = 50.
   - ask: 25 + 50 =  [box=75, NO label]

## silver[4] (input: multiple_choice, main-box unit: (none))
Q: The gradient of a distance-time graph at \(t = 4\) is estimated as 12. What does this tell you?

## silver[5] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule: \(y_0 = 0, y_1 = 4, y_2 = 6, y_3 = 6, y_4 = 4\). Strip width \(h = 1\). Estimate the area.
   - intro: Trapezium rule again: (h/2) × [first + last + 2 × (middle values)]. Start with the ends.
   - ask: first + last: 0 + 4 =  [box=4, NO label]
   - ask: add the middle values: 4 + 6 + 6 =  [box=16, NO label]
   - ask: double them: 2 × 16 =  [box=32, NO label]
   - ask: bracket total: 4 + 32 =  [box=36, NO label]
   - intro: Now scale by h/2. Here h/2 = 1 ÷ 2 = 0.5:
   - ask: 0.5 × 36 =  [box=18, NO label]
   - intro: Check by strips: ½(0+4), ½(4+6), ½(6+6), ½(6+4), each × 1, give 2, 5, 6, 5.
   - ask: 2 + 5 + 6 + 5 =  [box=18, NO label]

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: A curve has a negative gradient at \(x = 2\). Is the curve increasing or decreasing at this point?

## gold[0] (input: single_value, main-box unit: (none))
Q: Use the trapezium rule with 4 strips: \(y_0 = 1, y_1 = 3, y_2 = 7, y_3 = 9, y_4 = 10\) at \(x = 0, 2, 4, 6, 8\). Estimate the area.
   - intro: Here h = 2. Trapezium rule: (h/2) × [first + last + 2 × (interior values)]. Build it up.
   - ask: first + last: 1 + 10 =  [box=11, NO label]
   - ask: add the interior values: 3 + 7 + 9 =  [box=19, NO label]
   - ask: double them: 2 × 19 =  [box=38, NO label]
   - intro: Now assemble the bracket, then scale by h/2 (here h/2 = 2 ÷ 2 = 1).
   - ask: bracket total: 11 + 38 =  [box=49, NO label]
   - ask: 1 × 49 =  [box=49, NO label]
   - intro: Check by strips: ½(1+3)×2, ½(3+7)×2, ½(7+9)×2, ½(9+10)×2 give 4, 10, 16, 19.
   - ask: 4 + 10 + 16 + 19 =  [box=49, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: A velocity-time graph shows: \(t = 0, v = 0\); \(t = 2, v = 8\); \(t = 4, v = 12\); \(t = 6, v = 12\); \(t = 8, v = 8\). Use 4 strips to estimate the total distance in metres.
   - intro: Distance is the area under the velocity-time graph. Here h = 2. Use (h/2) × [first + last + 2 × (middle speeds)].
   - ask: first + last: 0 + 8 =  [box=8, NO label]
   - ask: add the middle speeds: 8 + 12 + 12 =  [box=32, NO label]
   - ask: double them: 2 × 32 =  [box=64, NO label]
   - intro: Now assemble the bracket, then scale by h/2 (here h/2 = 2 ÷ 2 = 1).
   - ask: bracket total: 8 + 64 =  [box=72, NO label]
   - ask: 1 × 72 =  [box=72, NO label]
   - intro: Check by strips: ½(0+8)×2, ½(8+12)×2, ½(12+12)×2, ½(12+8)×2 give 8, 20, 24, 20.
   - ask: 8 + 20 + 24 + 20 =  [box=72, NO label]

## gold[2] (input: multiple_choice, main-box unit: (none))
Q: (2, 18)(6, 2)x = 4Diagram not drawn accuratelyThe tangent to a curve at \(x = 4\) passes through \((2, 18)\) and \((6, 2)\). The curve represents the height (m) of a ball after \(x\) seconds. Interpret the gradient.

## gold[3] (input: multiple_choice, main-box unit: (none))
Q: estimate 42actual area 40Diagram not drawn accuratelyThe trapezium rule with 5 strips gives an area of 42. The actual area is 40. Is the trapezium rule estimate an overestimate or underestimate? (Assume the curve is concave upward, shaped like a U or bowl.)

## gold[4] (input: single_value, main-box unit: (none))
Q: 10181406t (s)Diagram not drawn accuratelyA speed-time graph is estimated using 3 trapeziums: area₁ = 10, area₂ = 18, area₃ = 14. The time interval is 0 to 6 seconds. What is the estimated total distance and the estimated average speed? Give the average speed in m/s.
   - intro: The three trapezium areas add up to the total distance (the whole area under the graph).
   - ask: total distance = 10 + 18 + 14 =  [box=42, NO label]
   - ask: total time = 6 − 0 =  [box=6, NO label]
   - intro: Average speed is total distance divided by total time:
   - ask: average speed = 42 ÷ 6 =  [box=7, NO label]
   - intro: Check: at 7 m/s for 6 s the distance would be:
   - ask: 7 × 6 =  [box=42, NO label]
