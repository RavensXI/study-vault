# maths-eduqas / graphs / L07 - Graph Transformations

## bronze[0] (input: single_value, main-box unit: (none))
Q: The point \((5, 3)\) is on \(y = f(x)\). What is the y-coordinate of the corresponding point on \(y = f(x) + 6\)?
   - intro: The +6 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 5.
   - ask: The graph moves UP. By how many units?  [box=6, NO label]
   - intro: Add that to the y-coordinate.
   - ask: New y = 3 + 6 =  [box=9, NO label]
   - ask: Check how far y rose: 9 − 3 =  [box=6, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: The point \((4, 8)\) is on \(y = f(x)\). What is the y-coordinate of the corresponding point on \(y = f(x) - 5\)?
   - intro: The −5 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 4.
   - ask: The graph moves DOWN. By how many units?  [box=5, NO label]
   - intro: Take that off the y-coordinate.
   - ask: New y = 8 − 5 =  [box=3, NO label]
   - ask: Check the drop: 8 − 3 =  [box=5, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: The point \((6, 2)\) is on \(y = f(x)\). What is the x-coordinate of the corresponding point on \(y = f(x - 5)\)?
   - intro: The −5 is INSIDE the bracket, so it changes x, and inside does the OPPOSITE: f(x − 5) moves RIGHT by 5. y stays at 2.
   - ask: Moving right means we add. Add how many?  [box=5, NO label]
   - intro: Add that to the x-coordinate.
   - ask: New x = 6 + 5 =  [box=11, NO label]
   - ask: Check: y is untouched, so how far did y move?  [box=0, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: The point \((7, 1)\) is on \(y = f(x)\). What is the x-coordinate of the corresponding point on \(y = f(x + 2)\)?
   - intro: The +2 is INSIDE the bracket, so inside does the OPPOSITE: f(x + 2) moves LEFT by 2. y stays at 1.
   - ask: Moving left means we subtract. By how many?  [box=2, NO label]
   - intro: Take that off the x-coordinate.
   - ask: New x = 7 − 2 =  [box=5, NO label]
   - ask: Check: y is untouched, so how far did y move?  [box=0, NO label]

## bronze[4] (input: multiple_choice, main-box unit: (none))
Q: \(y = f(x) + a\) shifts the graph:

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: \(y = f(x + a)\) shifts the graph:

## bronze[6] (input: single_value, main-box unit: (none))
Q: The point \((0, 5)\) is on \(y = f(x)\). What is the y-coordinate on \(y = f(x) + 10\)?
   - intro: The +10 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 0.
   - ask: The graph moves UP. By how many units?  [box=10, NO label]
   - intro: Add that to the y-coordinate.
   - ask: New y = 5 + 10 =  [box=15, NO label]
   - ask: Check how far y rose: 15 − 5 =  [box=10, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: The point \((3, -2)\) is on \(y = f(x)\). What is the x-coordinate on \(y = f(x - 7)\)?
   - intro: The −7 is INSIDE the bracket, so inside does the OPPOSITE: f(x − 7) moves RIGHT by 7. y stays at −2.
   - ask: Moving right means we add. Add how many?  [box=7, NO label]
   - intro: Add that to the x-coordinate.
   - ask: New x = 3 + 7 =  [box=10, NO label]
   - ask: Check: y is untouched, so how far did y move?  [box=0, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: The point \((2, 6)\) is on \(y = f(x)\). What is the y-coordinate on \(y = -f(x)\)?
   - intro: The minus is OUTSIDE the bracket, so −f(x) reflects the graph in the x-axis: every y-value flips sign. x stays at 2.
   - ask: The y-coordinate before flipping is  [box=6, NO label]
   - intro: Reflecting multiplies that by −1.
   - ask: New y = 6 × (−1) =  [box=-6, NO label]
   - ask: Check the two heights cancel: 6 + (−6) =  [box=0, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: The point \((-3, 4)\) is on \(y = f(x)\). What is the x-coordinate on \(y = f(-x)\)?
   - intro: The minus is INSIDE the bracket, so f(−x) reflects the graph in the y-axis: every x-value flips sign. y stays at 4.
   - ask: The x-coordinate before flipping is  [box=-3, NO label]
   - intro: Reflecting multiplies that by −1.
   - ask: New x = (−3) × (−1) =  [box=3, NO label]
   - ask: Check the two x-values cancel: (−3) + 3 =  [box=0, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: The point \((4, -1)\) is on \(y = f(x)\). Find the y-coordinate on \(y = f(x + 2) - 3\).
   - intro: Two moves. The +2 inside changes x; the −3 outside changes y. We want the y-coordinate, which the outside part controls.
   - ask: The x-part first: +2 inside moves LEFT, so new x = 4 − 2 =  [box=2, NO label]
   - intro: Now the y-coordinate, from the −3 outside.
   - ask: New y = −1 − 3 =  [box=-4, NO label]
   - ask: Check the drop in y: (−1) − (−4) =  [box=3, NO label]

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: \(-f(x)\) is a reflection in which axis?

## silver[4] (input: single_value, main-box unit: (none))
Q: The curve \(y = x^2\) is translated by the vector \(\begin{pmatrix} 0 \\ -5 \end{pmatrix}\). Write the new equation. What is the constant term?
   - intro: A translation by the vector (0, −5) shifts the curve straight down by 5. So y = x² becomes y = x² − 5.
   - ask: The curve moves DOWN. By how many units?  [box=5, NO label]
   - intro: That amount is subtracted from the whole function.
   - ask: The constant term of y = x² − 5 is  [box=-5, NO label]
   - ask: Check where the vertex lands: 0 − 5 =  [box=-5, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: The point \((1, 5)\) is on \(y = f(x)\). Find the y-coordinate on \(y = f(x - 1) + 2\).
   - intro: Two moves. The −1 inside changes x; the +2 outside changes y. We want the y-coordinate, from the outside part.
   - ask: The x-part first: −1 inside moves RIGHT, so new x = 1 + 1 =  [box=2, NO label]
   - intro: Now the y-coordinate, from the +2 outside.
   - ask: New y = 5 + 2 =  [box=7, NO label]
   - ask: Check the rise in y: 7 − 5 =  [box=2, NO label]

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: \(f(-x)\) is a reflection in which axis?

## gold[0] (input: single_value, main-box unit: (none))
Q: The point \((3, 2)\) is on \(y = f(x)\). What is the y-coordinate on \(y = 4f(x)\)?
   - intro: 4f(x) multiplies every y-coordinate by 4. This is a vertical stretch, scale factor 4. x stays at 3.
   - ask: The stretch factor is the number in front of f, which is  [box=4, NO label]
   - intro: Multiply the y-coordinate by it.
   - ask: New y = 2 × 4 =  [box=8, NO label]
   - ask: Check by dividing back: 8 ÷ 4 =  [box=2, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The point \((6, 5)\) is on \(y = f(x)\). What is the x-coordinate on \(y = f(2x)\)?
   - intro: f(2x) compresses the graph horizontally, scale factor ½: every x-coordinate is divided by 2. y stays at 5.
   - ask: We divide x by the multiplier inside the bracket, which is  [box=2, NO label]
   - intro: Divide the x-coordinate by it.
   - ask: New x = 6 ÷ 2 =  [box=3, NO label]
   - ask: Check by multiplying back: 3 × 2 =  [box=6, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The point \((4, -3)\) is on \(y = f(x)\). What is the y-coordinate on \(y = -f(x) + 1\)?
   - intro: Two moves on y. First reflect (−f(x) flips the sign), then add 1. x stays at 4.
   - ask: Reflect: −f(x) flips the sign of y, so −3 becomes  [box=3, NO label]
   - intro: Now the +1 lifts that reflected y.
   - ask: New y = 3 + 1 =  [box=4, NO label]
   - ask: Check the lift: 4 − 3 =  [box=1, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: The point \((8, 2)\) is on \(y = f(x)\). What is the x-coordinate on \(y = f(4x)\)?
   - intro: f(4x) compresses the graph horizontally, scale factor ¼: every x-coordinate is divided by 4. y stays at 2.
   - ask: We divide x by the multiplier inside the bracket, which is  [box=4, NO label]
   - intro: Divide the x-coordinate by it.
   - ask: New x = 8 ÷ 4 =  [box=2, NO label]
   - ask: Check by multiplying back: 2 × 4 =  [box=8, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: Describe the transformation that maps \(y = x^2\) to \(y = (x - 3)^2 + 5\).
