# maths-ocr / number / L07 - Indices, Surds & Bounds

## bronze[0] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(\sqrt{50}\)
   - ask: The largest square number that divides 50 is  [box=25, NO label]
   - ask: 50 ÷ 25 =  [box=2, NO label]
   - intro: So \(\sqrt{50} = \sqrt{25} \times \sqrt{2}\).
   - ask: \(\sqrt{25}\) =  [box=5, NO label]
   - ask: So \(\sqrt{50}\) =  [box=5, label:'√2']
   - ask: Check: 5² × 2 =  [box=50, NO label]

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(\sqrt{18}\)
   - ask: The largest square number that divides 18 is  [box=9, NO label]
   - ask: 18 ÷ 9 =  [box=2, NO label]
   - intro: So \(\sqrt{18} = \sqrt{9} \times \sqrt{2}\).
   - ask: \(\sqrt{9}\) =  [box=3, NO label]
   - ask: So \(\sqrt{18}\) =  [box=3, label:'√2']
   - ask: Check: 3² × 2 =  [box=18, NO label]

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(\sqrt{75}\)
   - ask: The largest square number that divides 75 is  [box=25, NO label]
   - ask: 75 ÷ 25 =  [box=3, NO label]
   - intro: So \(\sqrt{75} = \sqrt{25} \times \sqrt{3}\).
   - ask: \(\sqrt{25}\) =  [box=5, NO label]
   - ask: So \(\sqrt{75}\) =  [box=5, label:'√3']
   - ask: Check: 5² × 3 =  [box=75, NO label]

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(2\sqrt{3} + 5\sqrt{3}\)
   - ask: Both terms are lots of √3, so add the numbers in front: 2 + 5 =  [box=7, NO label]
   - intro: The √3 stays the same. You never add the numbers under the root.
   - ask: So the total is  [box=7, label:'√3']
   - ask: Check by taking one lot back off: 7 − 5 =  [box=2, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: A length is 12 cm to the nearest cm. What is the lower bound?
   - ask: Rounded to the nearest 1 cm, so the half unit is  [box=0.5, NO label]
   - intro: The lower bound is the value minus the half unit.
   - ask: 12 − 0.5 =  [box=11.5, NO label]
   - ask: The upper bound is 12 + 0.5 =  [box=12.5, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: A mass is 3.2 kg to 1 d.p. What is the upper bound?
   - ask: Rounded to 1 d.p., so the half unit is  [box=0.05, NO label]
   - intro: The upper bound is the value plus the half unit.
   - ask: 3.2 + 0.05 =  [box=3.25, NO label]
   - ask: The lower bound is 3.2 − 0.05 =  [box=3.15, NO label]

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(\sqrt{12}\)
   - ask: The largest square number that divides 12 is  [box=4, NO label]
   - ask: 12 ÷ 4 =  [box=3, NO label]
   - intro: So \(\sqrt{12} = \sqrt{4} \times \sqrt{3}\).
   - ask: \(\sqrt{4}\) =  [box=2, NO label]
   - ask: So \(\sqrt{12}\) =  [box=2, label:'√3']
   - ask: Check: 2² × 3 =  [box=12, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: A speed is 45 mph to the nearest 5 mph. What is the lower bound?
   - ask: Rounded to the nearest 5 mph, so the half unit is  [box=2.5, NO label]
   - intro: The lower bound is the value minus the half unit.
   - ask: 45 − 2.5 =  [box=42.5, NO label]
   - ask: The upper bound is 45 + 2.5 =  [box=47.5, NO label]

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: Rationalise \(\frac{6}{\sqrt{3}}\)
   - ask: Multiply top and bottom by √3. Bottom: √3 × √3 =  [box=3, NO label]
   - intro: The top becomes 6√3, so the fraction is now 6√3 over 3.
   - ask: 6 ÷ 3 =  [box=2, label:'√3']
   - ask: Check: 2√3 × √3 = 2 × 3 =  [box=6, NO label]

## silver[1] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(\sqrt{8} \times \sqrt{6}\)
   - ask: Multiply under one root: 8 × 6 =  [box=48, NO label]
   - intro: So √8 × √6 = √48. Now simplify √48.
   - ask: The largest square factor of 48 is 16, and 48 ÷ 16 =  [box=3, NO label]
   - ask: √16 =  [box=4, NO label]
   - ask: Check: 4² × 3 =  [box=48, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: Expand and simplify \((3 + \sqrt{2})(3 - \sqrt{2})\)
   - ask: This is (a + b)(a − b) = a² − b². Here a = 3, so a² =  [box=9, NO label]
   - ask: b = √2, so b² = (√2)² =  [box=2, NO label]
   - intro: Difference of two squares: a² − b².
   - ask: 9 − 2 =  [box=7, NO label]
   - ask: Check the middle terms cancel: −3√2 + 3√2 =  [box=0, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(a = 5.4\) (1 d.p.), \(b = 3.8\) (1 d.p.). Find the lower bound of \(a + b\).
   - ask: Half unit for 1 d.p. =  [box=0.05, NO label]
   - ask: Lower bound of a = 5.4 − 0.05 =  [box=5.35, NO label]
   - intro: For the smallest possible sum, use the lower bound of each value.
   - ask: Lower bound of b = 3.8 − 0.05 =  [box=3.75, NO label]
   - ask: 5.35 + 3.75 =  [box=9.1, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Simplify \(\frac{\sqrt{20}}{\sqrt{5}}\)
   - ask: Combine under one root: 20 ÷ 5 =  [box=4, NO label]
   - intro: So √20 / √5 = √4.
   - ask: √4 =  [box=2, NO label]
   - ask: Check: 2 × √5 = √20 because 2² × 5 =  [box=20, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(a = 8\) (nearest integer), \(b = 3\) (nearest integer). Find the upper bound of \(a - b\).
   - ask: Half unit for the nearest integer =  [box=0.5, NO label]
   - ask: Upper bound of a = 8 + 0.5 =  [box=8.5, NO label]
   - intro: For the biggest difference, make a as large as possible and b as small as possible.
   - ask: Lower bound of b = 3 − 0.5 =  [box=2.5, NO label]
   - ask: 8.5 − 2.5 =  [box=6, NO label]

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: Rationalise \(\frac{4}{\sqrt{2}}\)
   - ask: Multiply top and bottom by √2. Bottom: √2 × √2 =  [box=2, NO label]
   - intro: The top becomes 4√2, so the fraction is now 4√2 over 2.
   - ask: 4 ÷ 2 =  [box=2, label:'√2']
   - ask: Check: 2√2 × √2 = 2 × 2 =  [box=4, NO label]

## gold[0] (input: multiple_choice, main-box unit: (none))
Q: Rationalise \(\frac{1}{3 + \sqrt{2}}\)
   - ask: Multiply top and bottom by the conjugate 3 − √2. Bottom: 3² =  [box=9, NO label]
   - ask: (√2)² =  [box=2, NO label]
   - intro: The bottom is 3² − (√2)², a difference of two squares.
   - ask: 9 − 2 =  [box=7, NO label]
   - ask: The top is 1 × (3 − √2) = 3 − √2. Check the surds cancel: −3√2 + 3√2 =  [box=0, NO label]

## gold[1] (input: multiple_choice, main-box unit: (none))
Q: Expand and simplify \((2 + \sqrt{5})^2\)
   - ask: (2 + √5)² = 2² + 2×2×√5 + (√5)². First term 2² =  [box=4, NO label]
   - ask: Last term (√5)² =  [box=5, NO label]
   - intro: Middle term: 2 × 2 × √5 = 4√5.
   - ask: Whole-number part: 4 + 5 =  [box=9, NO label]
   - ask: Surd coefficient: 2 × 2 =  [box=4, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(a = 6.0\) (1 d.p.), \(b = 2.0\) (1 d.p.). Find the upper bound of \(\frac{a}{b}\). (Give to 2 d.p.)
   - ask: Half unit for 1 d.p. =  [box=0.05, NO label]
   - ask: Upper bound of a = 6.0 + 0.05 =  [box=6.05, NO label]
   - intro: For the biggest quotient, make the top as large and the bottom as small as possible.
   - ask: Lower bound of b = 2.0 − 0.05 =  [box=1.95, NO label]
   - ask: 6.05 ÷ 1.95 = (2 d.p.)  [box=3.1, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Show that \(\frac{\sqrt{12} + \sqrt{3}}{\sqrt{3}} = 3\). Enter the value the expression equals.
   - ask: Simplify √12: 12 = 4 × 3, so √12 = 2√3. The coefficient is  [box=2, NO label]
   - intro: The numerator is 2√3 + √3 = 3√3.
   - ask: Add the coefficients: 2 + 1 =  [box=3, label:'√3']
   - ask: Divide by √3: 3√3 ÷ √3 =  [box=3, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: Simplify \(\frac{6 + \sqrt{8}}{2}\)
   - ask: Simplify √8: 8 = 4 × 2, so √8 = 2√2. The coefficient is  [box=2, NO label]
   - intro: So the top is 6 + 2√2, all over 2.
   - ask: Divide the first term: 6 ÷ 2 =  [box=3, NO label]
   - ask: Divide the surd term: 2√2 ÷ 2 =  [box=1, label:'√2']
