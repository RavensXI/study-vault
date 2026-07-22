# maths-eduqas / algebra / L02 - Expanding Brackets

## bronze[0] (input: multiple_choice, main-box unit: (none))
Q: Expand \(3(x + 4)\)

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Expand \(5(2y - 3)\)

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Expand \(4(a + 2)\)

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Expand \(-2(x - 5)\)

## bronze[4] (input: multiple_choice, main-box unit: (none))
Q: Expand \(x(x + 3)\)

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: Expand \(6(3 - p)\)

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: Expand \(2x(x + 4)\)

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: Expand \(-3(2a + 1)\)

## silver[0] (input: single_value, main-box unit: (none))
Q: Expand \((x + 2)(x + 5)\). What is the coefficient of \(x\)?
   - ask: Outer: x × 5 =  [box=5, label:'x']
   - ask: Inner: 2 × x =  [box=2, label:'x']
   - intro: Add the two x terms to get the coefficient.
   - ask: 5 + 2 =  [box=7, NO label]
   - ask: Full expansion x² + 7x + 10. Coefficient of x =  [box=7, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Expand \((x + 4)(x - 3)\). What is the constant term?
   - ask: Outer: x × (−3) =  [box=-3, label:'x']
   - ask: Inner: 4 × x =  [box=4, label:'x']
   - intro: The constant term is the Last pair multiplied.
   - ask: Last: 4 × (−3) =  [box=-12, NO label]
   - ask: Full expansion x² + x − 12. Constant term =  [box=-12, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Expand \((x - 1)(x - 6)\). What is the coefficient of \(x\)?
   - ask: Outer: x × (−6) =  [box=-6, label:'x']
   - ask: Inner: (−1) × x =  [box=-1, label:'x']
   - intro: Add the two x terms, keeping the signs.
   - ask: (−6) + (−1) =  [box=-7, NO label]
   - ask: Full expansion x² − 7x + 6. Coefficient of x =  [box=-7, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Expand \((x + 3)^2\). What is the coefficient of \(x\)?
   - intro: A square means two identical brackets: \((x+3)(x+3)\).
   - ask: Outer: x × 3 =  [box=3, label:'x']
   - ask: Inner: 3 × x =  [box=3, label:'x']
   - intro: Add the two x terms.
   - ask: 3 + 3 =  [box=6, NO label]
   - ask: Full expansion x² + 6x + 9. Coefficient of x =  [box=6, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Expand \((x - 4)(x + 4)\). What is the constant term?
   - ask: Outer: x × 4 =  [box=4, label:'x']
   - ask: Inner: (−4) × x =  [box=-4, label:'x']
   - intro: The x terms cancel (4x − 4x = 0). The constant is the Last pair.
   - ask: Last: (−4) × 4 =  [box=-16, NO label]
   - ask: Full expansion x² − 16. Constant term =  [box=-16, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Expand and simplify \(3(x + 2) + 4(x - 1)\). What is the constant?
   - ask: Expand the first: 3 × 2 =  [box=6, NO label]
   - ask: Expand the second: 4 × (−1) =  [box=-4, NO label]
   - intro: The constants are the number-only parts. Add them.
   - ask: 6 + (−4) =  [box=2, NO label]
   - ask: Full expansion 7x + 2. Constant term =  [box=2, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Expand \((x + 5)(x - 2)\). What is the constant term?
   - ask: Outer: x × (−2) =  [box=-2, label:'x']
   - ask: Inner: 5 × x =  [box=5, label:'x']
   - intro: The constant is the Last pair multiplied.
   - ask: Last: 5 × (−2) =  [box=-10, NO label]
   - ask: Full expansion x² + 3x − 10. Constant term =  [box=-10, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Expand \((2x + 3)(x - 4)\). What is the coefficient of \(x\)?
   - ask: Outer: 2x × (−4) =  [box=-8, label:'x']
   - ask: Inner: 3 × x =  [box=3, label:'x']
   - intro: Add the two x terms, keeping signs.
   - ask: (−8) + 3 =  [box=-5, NO label]
   - ask: Full expansion 2x² − 5x − 12. Coefficient of x =  [box=-5, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Expand \((3x - 1)^2\). What is the coefficient of \(x\)?
   - intro: A square means two identical brackets: \((3x-1)(3x-1)\).
   - ask: Outer: 3x × (−1) =  [box=-3, label:'x']
   - ask: Inner: (−1) × 3x =  [box=-3, label:'x']
   - intro: Add the two x terms.
   - ask: (−3) + (−3) =  [box=-6, NO label]
   - ask: Full expansion 9x² − 6x + 1. Coefficient of x =  [box=-6, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Expand \((2x + 1)(x + 3)(x - 2)\). What is the coefficient of \(x^2\)?
   - intro: Do two brackets first: \((2x+1)(x+3) = 2x^2 + 7x + 3\).
   - ask: The x² term of the first product: 2x × x =  [box=2, label:'x²']
   - ask: The x term of the first product: 2x × 3 + 1 × x, coefficient =  [box=7, label:'x']
   - intro: Now multiply (2x² + 7x + 3) by (x − 2). The x² term comes from two products.
   - ask: 2x² × (−2) =  [box=-4, label:'x²']
   - ask: 7x × x =  [box=7, label:'x²']
   - ask: Add them: (−4) + 7 =  [box=3, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Expand \((x + 2)^3\). What is the coefficient of \(x^2\)?
   - intro: A cube is three brackets. First square: \((x+2)(x+2) = x^2 + 4x + 4\).
   - ask: Confirm the x term of the square: 2 + 2 =  [box=4, NO label]
   - intro: Now multiply (x² + 4x + 4) by (x + 2). The x² term comes from two products.
   - ask: x² × 2 =  [box=2, label:'x²']
   - ask: 4x × x =  [box=4, label:'x²']
   - ask: Add them: 2 + 4 =  [box=6, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Show that \((x+1)(x+2)(x+3) = x^3 + 6x^2 + 11x + 6\). What is the coefficient of \(x\)?
   - intro: Do two brackets first: \((x+1)(x+2) = x^2 + 3x + 2\).
   - ask: The x term coefficient of the first product: 2x + 1x gives  [box=3, label:'x']
   - intro: Now multiply (x² + 3x + 2) by (x + 3). The x term comes from two products.
   - ask: 3x × 3 =  [box=9, label:'x']
   - ask: 2 × x =  [box=2, label:'x']
   - ask: Add them: 9 + 2 =  [box=11, NO label]
