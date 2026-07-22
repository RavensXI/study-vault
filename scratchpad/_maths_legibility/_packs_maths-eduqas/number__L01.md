# maths-eduqas / number / L01 - Four Operations & Order of Operations

## bronze[0] (input: single_value, main-box unit: (none))
Q: \(6 + 4 \times 3\)
   - intro: No brackets or indices. Multiplication comes before addition, so do 4 × 3 first.
   - ask: 4 × 3 =  [box=12, NO label]
   - intro: Now it is 6 + 12.
   - ask: 6 + 12 =  [box=18, NO label]
   - ask: Check: 18 − 6 =  [box=12, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: \(20 - 8 \div 2\)
   - intro: No brackets or indices. Division comes before subtraction, so do 8 ÷ 2 first.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - intro: Now it is 20 − 4.
   - ask: 20 − 4 =  [box=16, NO label]
   - ask: Check: 16 + 4 =  [box=20, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(3 + 5 \times 2\)
   - intro: No brackets or indices. Multiply before you add, so do 5 × 2 first.
   - ask: 5 × 2 =  [box=10, NO label]
   - intro: Now it is 3 + 10.
   - ask: 3 + 10 =  [box=13, NO label]
   - ask: Check: 13 − 3 =  [box=10, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(24 \div 6 + 2\)
   - intro: Division outranks addition, so do 24 ÷ 6 first.
   - ask: 24 ÷ 6 =  [box=4, NO label]
   - intro: Now it is 4 + 2.
   - ask: 4 + 2 =  [box=6, NO label]
   - ask: Check: 6 − 2 =  [box=4, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: \(10 - 3 + 7\)
   - intro: Only subtraction and addition here, equal priority, so work left to right. Subtract first.
   - ask: 10 − 3 =  [box=7, NO label]
   - intro: Now add the 7.
   - ask: 7 + 7 =  [box=14, NO label]
   - ask: Check: 14 − 7 + 3 =  [box=10, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(2 \times 5 + 4 \times 3\)
   - intro: Two separate multiplications, both done before the add. Work out each one.
   - ask: 2 × 5 =  [box=10, NO label]
   - ask: 4 × 3 =  [box=12, NO label]
   - intro: Now add the two parts: 10 + 12.
   - ask: 10 + 12 =  [box=22, NO label]
   - ask: Check: 22 − 12 =  [box=10, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(18 \div 3 \times 2\)
   - intro: Divide and multiply are equal priority, so work left to right. Divide first.
   - ask: 18 ÷ 3 =  [box=6, NO label]
   - intro: Now multiply: 6 × 2.
   - ask: 6 × 2 =  [box=12, NO label]
   - ask: Check: 12 ÷ 2 =  [box=6, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(14 - 8 \div 2\)
   - intro: Division comes before subtraction, so do 8 ÷ 2 first.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - intro: Now it is 14 − 4.
   - ask: 14 − 4 =  [box=10, NO label]
   - ask: Check: 10 + 4 =  [box=14, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: \((3 + 5) \times 4\)
   - intro: Brackets first: work out 3 + 5.
   - ask: 3 + 5 =  [box=8, NO label]
   - intro: Now multiply the bracket result by 4.
   - ask: 8 × 4 =  [box=32, NO label]
   - ask: Check: 32 ÷ 4 =  [box=8, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: \(4^2 + 3 \times 5\)
   - intro: Indices first: work out 4².
   - ask: 4² =  [box=16, NO label]
   - ask: 3 × 5 =  [box=15, NO label]
   - intro: Now add the two parts: 16 + 15.
   - ask: 16 + 15 =  [box=31, NO label]
   - ask: Check: 31 − 15 =  [box=16, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(50 - (4 + 6)^2\)
   - intro: Brackets first, then its index. Work out 4 + 6.
   - ask: 4 + 6 =  [box=10, NO label]
   - ask: 10² =  [box=100, NO label]
   - intro: Now subtract: 50 − 100.
   - ask: 50 − 100 =  [box=-50, NO label]
   - ask: Check: −50 + 100 =  [box=50, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(36 \div (2 + 4) \times 3\)
   - intro: Brackets first: work out 2 + 4.
   - ask: 2 + 4 =  [box=6, NO label]
   - ask: 36 ÷ 6 =  [box=6, NO label]
   - intro: Now multiply: 6 × 3.
   - ask: 6 × 3 =  [box=18, NO label]
   - ask: Check: 18 ÷ 3 =  [box=6, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(2 \times (9 - 4)^2\)
   - intro: Brackets first, then its index. Work out 9 − 4.
   - ask: 9 − 4 =  [box=5, NO label]
   - ask: 5² =  [box=25, NO label]
   - intro: Now multiply: 2 × 25.
   - ask: 2 × 25 =  [box=50, NO label]
   - ask: Check: 50 ÷ 2 =  [box=25, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(100 \div (5^2)\)
   - intro: Work out the index inside the brackets first: 5².
   - ask: 5² =  [box=25, NO label]
   - intro: Now divide: 100 ÷ 25.
   - ask: 100 ÷ 25 =  [box=4, NO label]
   - ask: Check: 4 × 25 =  [box=100, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: \(7 + 2 \times (8 - 3)\)
   - intro: Brackets first: work out 8 − 3.
   - ask: 8 − 3 =  [box=5, NO label]
   - ask: 2 × 5 =  [box=10, NO label]
   - intro: Now add: 7 + 10.
   - ask: 7 + 10 =  [box=17, NO label]
   - ask: Check: 17 − 7 =  [box=10, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: \(\dfrac{18 + 6}{2^2} + 5 \times 3\)
   - intro: The fraction bar acts like brackets. Work out the top: 18 + 6.
   - ask: 18 + 6 =  [box=24, NO label]
   - ask: 2² =  [box=4, NO label]
   - ask: 24 ÷ 4 =  [box=6, NO label]
   - ask: 5 × 3 =  [box=15, NO label]
   - intro: Now add the two parts: 6 + 15.
   - ask: 6 + 15 =  [box=21, NO label]
   - ask: Check: 21 − 15 =  [box=6, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: \((2 + 3)^2 - 4 \times (7 - 5)\)
   - intro: Both brackets first: 2 + 3 and 7 − 5.
   - ask: 2 + 3 =  [box=5, NO label]
   - ask: 7 − 5 =  [box=2, NO label]
   - ask: 5² =  [box=25, NO label]
   - ask: 4 × 2 =  [box=8, NO label]
   - intro: Now subtract: 25 − 8.
   - ask: 25 − 8 =  [box=17, NO label]
   - ask: Check: 17 + 8 =  [box=25, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(\dfrac{3^3 - 7}{2 \times 5}\)
   - intro: The fraction bar groups the whole top and the whole bottom. Start with the top: 3³.
   - ask: 3³ =  [box=27, NO label]
   - ask: 27 − 7 =  [box=20, NO label]
   - ask: 2 × 5 =  [box=10, NO label]
   - intro: Now divide top by bottom: 20 ÷ 10.
   - ask: 20 ÷ 10 =  [box=2, NO label]
   - ask: Check: 2 × 10 =  [box=20, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: \((-3)^2 + 4 \times (-2)\)
   - intro: Indices first. Square the bracket: (−3)², remembering a negative times a negative is positive.
   - ask: (−3) × (−3) =  [box=9, NO label]
   - ask: 4 × (−2) =  [box=-8, NO label]
   - intro: Now add the two parts: 9 + (−8).
   - ask: 9 + (−8) =  [box=1, NO label]
   - ask: Check: 1 + 8 =  [box=9, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: \(\sqrt{49} + 2^3 \times 3 - 8\)
   - intro: Indices and roots first: √49 and 2³.
   - ask: √49 =  [box=7, NO label]
   - ask: 2³ =  [box=8, NO label]
   - ask: 8 × 3 =  [box=24, NO label]
   - intro: Now work left to right: add 7 + 24 first.
   - ask: 7 + 24 =  [box=31, NO label]
   - ask: 31 − 8 =  [box=23, NO label]
   - ask: Check: 23 + 8 − 24 =  [box=7, NO label]
