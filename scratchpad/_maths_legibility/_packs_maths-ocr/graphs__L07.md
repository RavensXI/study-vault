# maths-ocr / graphs / L07 - Graph Transformations

## bronze[0] (input: single_value, main-box unit: (none))
Q: The point \((2, 7)\) lies on \(y = f(x)\). Find the \(y\)-coordinate of its image on \(y = f(x) + 3\).
   - intro: The +3 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 2.
   - ask: The graph moves UP. How many units up?  [box=3, NO label]
   - intro: Add that to the y-coordinate.
   - ask: New y = 7 + 3 =  [box=10, NO label]
   - ask: Check how far y rose: 10 − 7 =  [box=3, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: The point \((4, 1)\) lies on \(y = f(x)\). Find the \(y\)-coordinate of its image on \(y = f(x) - 3\).
   - intro: The −3 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 4.
   - ask: The graph moves DOWN. By how many units?  [box=3, NO label]
   - intro: Take that off the y-coordinate.
   - ask: New y = 1 − 3 =  [box=-2, NO label]
   - ask: Check the drop: 1 − (−2) =  [box=3, NO label]

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: \(y = f(x) + 5\) is a translation. Which direction does the graph move?

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: \(y = f(x + 2)\) is a translation. Which direction does the graph move?

## bronze[4] (input: single_value, main-box unit: (none))
Q: The point \((5, 2)\) lies on \(y = f(x)\). Find the \(x\)-coordinate of its image on \(y = f(x + 4)\).
   - intro: The +4 is INSIDE the bracket, so it changes the x-coordinate, and inside does the OPPOSITE: it moves LEFT. y stays at 2.
   - ask: Moving left means we subtract. By how many?  [box=4, NO label]
   - intro: Take that off the x-coordinate.
   - ask: New x = 5 − 4 =  [box=1, NO label]
   - ask: Check: y is untouched, so how far did y move?  [box=0, NO label]

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: \(y = -f(x)\) is a reflection. In which axis?

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: \(y = f(-x)\) is a reflection. In which axis?

## bronze[7] (input: single_value, main-box unit: (none))
Q: The point \((3, 6)\) lies on \(y = f(x)\). Find the \(y\)-coordinate of its image on \(y = -f(x)\).
   - intro: The minus is OUTSIDE the bracket, so −f(x) reflects the graph in the x-axis: every y-value flips sign. x stays at 3.
   - ask: Before flipping, the y-coordinate is  [box=6, NO label]
   - intro: Reflecting multiplies that by −1.
   - ask: New y = 6 × (−1) =  [box=-6, NO label]
   - ask: Check the two heights cancel: 6 + (−6) =  [box=0, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: The point \((-2, 5)\) lies on \(y = f(x)\). Find the \(x\)-coordinate of its image on \(y = f(-x)\).
   - intro: The minus is INSIDE the bracket, so f(−x) reflects the graph in the y-axis: every x-value flips sign. y stays at 5.
   - ask: The x-coordinate before flipping is  [box=-2, NO label]
   - intro: Reflecting multiplies that by −1.
   - ask: New x = (−2) × (−1) =  [box=2, NO label]
   - ask: Check the two x-values cancel: (−2) + 2 =  [box=0, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: The maximum point of \(y = f(x)\) is \((4, 7)\). Find the \(y\)-coordinate of the maximum of \(y = f(x) - 4\).
   - intro: The maximum moves with the curve. The −4 is OUTSIDE, so it lowers the y-coordinate; x stays at 4.
   - ask: The graph moves DOWN by how many?  [box=4, NO label]
   - intro: Take that off the maximum's y-coordinate.
   - ask: New y = 7 − 4 =  [box=3, NO label]
   - ask: Check the drop: 7 − 3 =  [box=4, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: The minimum point of \(y = f(x)\) is \((3, -2)\). Find the \(x\)-coordinate of the minimum of \(y = f(x - 5)\).
   - intro: The minimum moves with the curve. The −5 is INSIDE, and inside does the OPPOSITE, so the graph moves RIGHT; y stays at −2.
   - ask: Moving right means we add. Add how many?  [box=5, NO label]
   - intro: Add that to the x-coordinate.
   - ask: New x = 3 + 5 =  [box=8, NO label]
   - ask: Check how far right it moved: 8 − 3 =  [box=5, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: The curve \(y = x^2\) is transformed to \(y = (x + 2)^2 + 1\) by a translation. Give the \(x\)-component of the translation vector.
   - intro: A translation vector is written as (x-shift, y-shift). Find each part from the equation.
   - ask: The +1 outside the bracket shifts the curve up. That is the y-component:  [box=1, NO label]
   - intro: Now the horizontal part, from inside the bracket.
   - ask: Inside is (x + 2). Inside does the opposite, so the curve moves LEFT, giving x-component  [box=-2, NO label]
   - ask: Check: a point at x = 0 on y = x² lands at x =  [box=-2, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: The graph \(y = f(x)\) passes through \((0, 6)\). What point does \(y = f(x + 2) - 2\) pass through? Give the \(y\)-coordinate.
   - intro: Two moves. The +2 inside changes x; the −2 outside changes y. We want the y-coordinate, which the outside part controls.
   - ask: The x-part first: +2 inside moves LEFT, so new x = 0 − 2 =  [box=-2, NO label]
   - intro: Now the y-coordinate, from the −2 outside.
   - ask: New y = 6 − 2 =  [box=4, NO label]
   - ask: Check the drop in y: 6 − 4 =  [box=2, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: The point \((5, -3)\) lies on \(y = f(x)\). It is reflected in the \(y\)-axis to give \(y = f(-x)\). Find the new \(x\)-coordinate.
   - intro: Reflecting in the y-axis flips the sign of every x-coordinate. y stays at −3.
   - ask: The x-coordinate before reflecting is  [box=5, NO label]
   - intro: Multiply that by −1.
   - ask: New x = 5 × (−1) =  [box=-5, NO label]
   - ask: Check the two x-values cancel: 5 + (−5) =  [box=0, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: The point \((-4, 7)\) lies on \(y = f(x)\). Find the \(y\)-coordinate of its image on \(y = -f(x)\).
   - intro: −f(x) reflects in the x-axis, flipping the sign of every y-coordinate. x stays at −4.
   - ask: The y-coordinate before reflecting is  [box=7, NO label]
   - intro: Multiply that by −1.
   - ask: New y = 7 × (−1) =  [box=-7, NO label]
   - ask: Check the two y-values cancel: 7 + (−7) =  [box=0, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: The curve \(y = x^2\) is transformed to \(y = (x + 1)^2 - 4\). State the coordinates of the vertex of the new curve. Give the \(y\)-coordinate.
   - intro: Start from the vertex of y = x², which sits at (0, 0). Apply the two moves to it.
   - ask: Inside is (x + 1). Inside does the opposite, so the vertex moves LEFT by 1: new x = 0 − 1 =  [box=-1, NO label]
   - intro: Now the vertical move, from the −4 outside. We want this y-coordinate.
   - ask: New y = 0 − 4 =  [box=-4, NO label]
   - ask: Check the drop: 0 − (−4) =  [box=4, NO label]

## gold[1] (input: multiple_choice, main-box unit: (none))
Q: The graph of \(y = \sin x\) is reflected in the \(x\)-axis. Write the equation of the new graph. Which of these is correct?

## gold[2] (input: single_value, main-box unit: (none))
Q: Two transformations are applied: first \(y = f(x)\) becomes \(y = -f(x)\), then that becomes \(y = -f(x) + 4\). The point \((3, 6)\) is on the original. Find the final \(y\)-coordinate.
   - intro: Two steps on the y-coordinate. First reflect, then add 4. x stays at 3.
   - ask: Reflect: −f(x) flips the sign of y, so 6 becomes  [box=-6, NO label]
   - intro: Now the +4 lifts that reflected y.
   - ask: New y = (−6) + 4 =  [box=-2, NO label]
   - ask: Check the lift: (−2) − (−6) =  [box=4, NO label]

## gold[3] (input: multiple_choice, main-box unit: (none))
Q: The point \((a, b)\) on \(y = f(x)\) maps to \((-a, -b)\). Which two transformations produce this?

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: The curve \(y = f(x)\) has a root at \(x = 6\). After the transformation \(y = f(x + 2) + 3\), does the curve still pass through the \(x\)-axis at \(x = 4\)?
