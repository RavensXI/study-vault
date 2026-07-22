# maths-eduqas / algebra / L08 - Quadratic Formula & Completing the Square

## bronze[0] (input: single_value, main-box unit: (none))
Q: For \(x^2 + 7x - 5 = 0\), state the values of \(a\), \(b\), \(c\). What is \(b\)?
   - intro: Compare \(x^2 + 7x - 5\) with \(ax^2 + bx + c\), matching term by term.
   - ask: a, from the x² term =  [box=1, NO label]
   - ask: c, the constant with its sign =  [box=-5, NO label]
   - intro: b is the coefficient of the x term, and that is what the question wants.
   - ask: b =  [box=7, NO label]
   - ask: Check: rebuild it as 1x² + __x − 5. The blank is  [box=7, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Find the discriminant of \(x^2 + 4x + 1 = 0\).
   - intro: Read off a = 1, b = 4, c = 1.
   - ask: b² = 4 × 4 =  [box=16, NO label]
   - ask: 4ac = 4 × 1 × 1 =  [box=4, NO label]
   - intro: Now subtract to get the discriminant.
   - ask: b² − 4ac = 16 − 4 =  [box=12, NO label]
   - ask: Enter the number of real roots:  [box=2, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Find the discriminant of \(x^2 - 6x + 9 = 0\).
   - intro: Read off a = 1, b = −6, c = 9.
   - ask: b² = (−6) × (−6) =  [box=36, NO label]
   - ask: 4ac = 4 × 1 × 9 =  [box=36, NO label]
   - intro: Now subtract.
   - ask: b² − 4ac = 36 − 36 =  [box=0, NO label]
   - ask: Number of real roots when the discriminant is 0:  [box=1, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Find the discriminant of \(x^2 + 2x + 5 = 0\).
   - intro: Read off a = 1, b = 2, c = 5.
   - ask: b² = 2 × 2 =  [box=4, NO label]
   - ask: 4ac = 4 × 1 × 5 =  [box=20, NO label]
   - intro: Now subtract. The answer will be negative.
   - ask: b² − 4ac = 4 − 20 =  [box=-16, NO label]
   - ask: Number of real roots when the discriminant is negative:  [box=0, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: Complete the square: \(x^2 + 6x\). Write as \((x+p)^2 - q\). What is \(p\)?
   - intro: For \(x^2 + 6x = (x+p)^2 - q\), find p by halving the 6.
   - ask: 6 ÷ 2 =  [box=3, NO label]
   - intro: Square that to get the q you would subtract.
   - ask: 3² =  [box=9, NO label]
   - ask: Check: expand (x+3)² − 9 = x² + 6x + 9 − 9. The x coefficient is  [box=6, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Complete the square: \(x^2 + 6x\). Write as \((x+p)^2 - q\). What is \(q\)?
   - intro: For \(x^2 + 6x = (x+p)^2 - q\), halve the 6 for p.
   - ask: 6 ÷ 2 =  [box=3, NO label]
   - intro: Now q is p squared.
   - ask: 3² =  [box=9, NO label]
   - ask: Check: (x+3)² − 9 = x² + 6x + 9 − 9. The constant left is  [box=0, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Discriminant of \(2x^2 + 3x - 1 = 0\)?
   - intro: Read off a = 2, b = 3, c = −1.
   - ask: b² = 3 × 3 =  [box=9, NO label]
   - ask: 4ac = 4 × 2 × (−1) =  [box=-8, NO label]
   - intro: Now subtract 4ac from b². Watch the double negative.
   - ask: 9 − (−8) =  [box=17, NO label]
   - ask: Number of real roots when the discriminant is positive:  [box=2, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: How many real roots does \(x^2 + 5x + 2 = 0\) have?
   - intro: The number of roots comes from the sign of the discriminant. a = 1, b = 5, c = 2.
   - ask: b² = 5 × 5 =  [box=25, NO label]
   - ask: 4ac = 4 × 1 × 2 =  [box=8, NO label]
   - intro: Subtract, then read the sign.
   - ask: b² − 4ac = 25 − 8 =  [box=17, NO label]
   - ask: 17 is positive, so the number of real roots is  [box=2, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 + 4x - 3 = 0\) using the formula. Give the positive root to 2 d.p.
   - intro: a = 1, b = 4, c = −3. Start with the discriminant.
   - ask: b² − 4ac = 16 − 4 × 1 × (−3) = 16 − (−12) =  [box=28, NO label]
   - ask: √28 to 2 d.p. =  [box=5.29, NO label]
   - intro: The positive root uses +√, all over 2a = 2.
   - ask: (−4 + √28) ÷ 2 = (2 d.p.)  [box=0.65, label:'(a decimal)']
   - ask: The other root: (−4 − √28) ÷ 2 = (2 d.p.)  [box=-4.65, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 - 6x + 4 = 0\). Give the larger root to 2 d.p.
   - intro: a = 1, b = −6, c = 4. Note −b = 6.
   - ask: b² − 4ac = (−6)² − 4 × 1 × 4 = 36 − 16 =  [box=20, NO label]
   - ask: √20 to 2 d.p. =  [box=4.47, NO label]
   - intro: The larger root uses +√, all over 2a = 2, with −b = 6.
   - ask: (6 + √20) ÷ 2 = (2 d.p.)  [box=5.24, NO label]
   - ask: The smaller root: (6 − √20) ÷ 2 = (2 d.p.)  [box=0.76, label:'(a decimal)']

## silver[2] (input: single_value, main-box unit: (none))
Q: Complete the square for \(x^2 + 8x + 5\). Write as \((x+p)^2 + q\). What is \(q\)?
   - intro: Halve the 8 to get p.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - ask: p² = 4² =  [box=16, NO label]
   - intro: Now q = c − p², and c = 5 here.
   - ask: q = 5 − 16 =  [box=-11, NO label]
   - ask: Check: (x+4)² − 11 = x² + 8x + 16 − 11. The constant is 16 − 11 =  [box=5, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: Complete the square for \(x^2 - 10x + 3\). What is the minimum value of the expression?
   - intro: Halve the −10 for p. Keep the minus.
   - ask: −10 ÷ 2 =  [box=-5, NO label]
   - ask: p² = (−5)² =  [box=25, NO label]
   - intro: The least value is c − p², and c = 3.
   - ask: 3 − 25 =  [box=-22, NO label]
   - ask: Check: (x−5)² − 22 is smallest when (x−5)² = 0, giving  [box=-22, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Solve \(2x^2 + 3x - 4 = 0\). Give the positive root to 2 d.p.
   - intro: a = 2, b = 3, c = −4. The divisor is 2a = 4.
   - ask: b² − 4ac = 9 − 4 × 2 × (−4) = 9 − (−32) =  [box=41, NO label]
   - ask: √41 to 2 d.p. =  [box=6.4, NO label]
   - intro: The positive root uses +√, all over 2a = 4.
   - ask: (−3 + √41) ÷ 4 = (2 d.p.)  [box=0.85, label:'(a decimal)']
   - ask: The other root: (−3 − √41) ÷ 4 = (2 d.p.)  [box=-2.35, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: Solve \(x^2 + 5x + 2 = 0\). Give the larger root to 2 d.p.
   - intro: a = 1, b = 5, c = 2.
   - ask: b² − 4ac = 25 − 4 × 1 × 2 = 25 − 8 =  [box=17, NO label]
   - ask: √17 to 2 d.p. =  [box=4.12, NO label]
   - intro: The larger root uses +√, all over 2a = 2, with −b = −5.
   - ask: (−5 + √17) ÷ 2 = (2 d.p.)  [box=-0.44, NO label]
   - ask: The smaller root: (−5 − √17) ÷ 2 = (2 d.p.)  [box=-4.56, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Complete the square for \(x^2 + 2x - 7\). Write as \((x+p)^2 + q\). What is \(q\)?
   - intro: Halve the 2 to get p.
   - ask: 2 ÷ 2 =  [box=1, NO label]
   - ask: p² = 1² =  [box=1, NO label]
   - intro: Now q = c − p², and c = −7 here.
   - ask: q = −7 − 1 =  [box=-8, NO label]
   - ask: Check: (x+1)² − 8 = x² + 2x + 1 − 8. The constant is 1 − 8 =  [box=-7, NO label]

## gold[0] (input: fraction, main-box unit: (none))
Q: Solve \(3x^2 - 5x + 1 = 0\). Give the sum of both solutions as a fraction.
   - intro: There is a shortcut: for ax² + bx + c = 0 the two roots always add to −b/a. No solving needed.
   - ask: a =  [box=3, NO label]
   - ask: b =  [box=-5, NO label]
   - intro: The sum is −b ÷ a. Work out −b first.
   - ask: −b = −(−5) =  [box=5, NO label]
   - ask: So the sum is 5 over a. The denominator a =  [box=3, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: For what value of \(k\) does \(x^2 + 6x + k = 0\) have exactly one solution?
   - intro: One solution means the discriminant is exactly 0. Here a = 1, b = 6, c = k.
   - ask: b² = 6 × 6 =  [box=36, NO label]
   - intro: The discriminant is 36 − 4k. Set it to 0, so 4k = 36.
   - ask: 4k =  [box=36, NO label]
   - ask: k = 36 ÷ 4 =  [box=9, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Write \(2x^2 + 12x + 5\) in the form \(a(x+p)^2 + q\). What is \(q\)?
   - intro: Factor the 2 out of the x² and x terms only.
   - ask: Inside: 12 ÷ 2 =  [box=6, NO label]
   - intro: Complete the square on x² + 6x: halve the 6.
   - ask: 6 ÷ 2 =  [box=3, NO label]
   - ask: Square it: 3² =  [box=9, NO label]
   - intro: Inside becomes (x+3)² − 9. Multiply the −9 back by 2, then add the 5.
   - ask: 2 × (−9) =  [box=-18, NO label]
   - ask: q = −18 + 5 =  [box=-13, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Show that \(kx^2 + 8x + (k+6) = 0\) has no real roots when \(k = 5\). Find the discriminant.
   - intro: Put k = 5 into every k. a = k, b = 8, c = k + 6.
   - ask: a = k =  [box=5, NO label]
   - ask: c = k + 6 = 5 + 6 =  [box=11, NO label]
   - intro: Now the discriminant, b² − 4ac.
   - ask: b² = 8 × 8 =  [box=64, NO label]
   - ask: 4ac = 4 × 5 × 11 =  [box=220, NO label]
   - ask: b² − 4ac = 64 − 220 =  [box=-156, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: By completing the square, find the coordinates of the turning point of \(y = x^2 - 4x + 7\). What is the \(y\)-coordinate?
   - intro: Complete the square: the turning point pops straight out. Halve the −4.
   - ask: −4 ÷ 2 =  [box=-2, NO label]
   - ask: Square it: (−2)² =  [box=4, NO label]
   - intro: The y-coordinate is c − p², and c = 7.
   - ask: y = 7 − 4 =  [box=3, NO label]
   - ask: The turning point sits at x = −p = −(−2) =  [box=2, NO label]
