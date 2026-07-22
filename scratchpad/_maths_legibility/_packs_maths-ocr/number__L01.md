# maths-ocr / number / L01 - Four Operations & Order of Operations

## bronze[0] (input: single_value, main-box unit: (none))
Q: \(3 + 5 \times 2\)
   - intro: No brackets or powers. Multiplication comes before addition, so clear the × first.
   - ask: 5 × 2 =  [box=10, NO label]
   - ask: 3 + 10 =  [box=13, NO label]
   - ask: Read it back, 3 + 5 × 2 is 3 + 10 =  [box=13, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: \(20 - 4 \times 3\)
   - intro: Multiplication comes before subtraction, so do the × first.
   - ask: 4 × 3 =  [box=12, NO label]
   - ask: 20 − 12 =  [box=8, NO label]
   - ask: Read it back, 20 − 4 × 3 is 20 − 12 =  [box=8, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(6 + 12 \div 4\)
   - intro: Division comes before addition, so do the ÷ first.
   - ask: 12 ÷ 4 =  [box=3, NO label]
   - ask: 6 + 3 =  [box=9, NO label]
   - ask: Read it back, 6 + 12 ÷ 4 is 6 + 3 =  [box=9, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(8 \times 3 - 10\)
   - intro: Multiplication comes before subtraction. Clear the × first, then subtract in the order written.
   - ask: 8 × 3 =  [box=24, NO label]
   - ask: 24 − 10 =  [box=14, NO label]
   - ask: Read it back, 8 × 3 − 10 is 24 − 10 =  [box=14, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: \(15 \div 3 + 4 \times 3\)
   - intro: Two high priority operations, one ÷ and one ×. Clear BOTH before adding.
   - ask: 15 ÷ 3 =  [box=5, NO label]
   - ask: 4 × 3 =  [box=12, NO label]
   - ask: 5 + 12 =  [box=17, NO label]
   - ask: Read it back: 5 + 12 =  [box=17, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(2 \times 7 + 3 \times 4\)
   - intro: Two multiplications and one addition. Clear BOTH multiplications before adding.
   - ask: 2 × 7 =  [box=14, NO label]
   - ask: 3 × 4 =  [box=12, NO label]
   - ask: 14 + 12 =  [box=26, NO label]
   - ask: Read it back: 14 + 12 =  [box=26, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(30 - 5 \times 4 + 1\)
   - intro: One multiplication in the middle. Clear it, then work − and + left to right.
   - ask: 5 × 4 =  [box=20, NO label]
   - ask: 30 − 20 =  [box=10, NO label]
   - ask: 10 + 1 =  [box=11, NO label]
   - ask: Read it back: 30 − 20 + 1 =  [box=11, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(48 \div 6 \div 2\)
   - intro: Two divisions. They are equal priority, so work strictly left to right.
   - ask: 48 ÷ 6 =  [box=8, NO label]
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - ask: Read it back: 48 ÷ 6 ÷ 2 is 8 ÷ 2 =  [box=4, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: \((3 + 5) \times 4\)
   - intro: Brackets first, always.
   - ask: 3 + 5 =  [box=8, NO label]
   - ask: 8 × 4 =  [box=32, NO label]
   - ask: Read it back: (3 + 5) × 4 = 8 × 4 =  [box=32, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: \(5 \times (12 - 4) + 6\)
   - intro: Bracket first, then multiply, then add.
   - ask: 12 − 4 =  [box=8, NO label]
   - ask: 5 × 8 =  [box=40, NO label]
   - ask: 40 + 6 =  [box=46, NO label]
   - ask: Read it back: 40 + 6 =  [box=46, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(2^3 + 5 \times 3\)
   - intro: Do the power and the multiplication before the addition.
   - ask: 2 cubed, 2 × 2 × 2 =  [box=8, NO label]
   - ask: 5 × 3 =  [box=15, NO label]
   - ask: 8 + 15 =  [box=23, NO label]
   - ask: Read it back: 8 + 15 =  [box=23, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(100 \div (4 + 6) \times 3\)
   - intro: Bracket first, then ÷ and × left to right.
   - ask: 4 + 6 =  [box=10, NO label]
   - ask: 100 ÷ 10 =  [box=10, NO label]
   - ask: 10 × 3 =  [box=30, NO label]
   - ask: Read it back: 100 ÷ 10 × 3 =  [box=30, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(3 \times 4^2 - 20\)
   - intro: The power sits on the 4 only. Do it first, then multiply, then subtract.
   - ask: 4 squared, 4 × 4 =  [box=16, NO label]
   - ask: 3 × 16 =  [box=48, NO label]
   - ask: 48 − 20 =  [box=28, NO label]
   - ask: Read it back: 48 − 20 =  [box=28, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \((7 - 3)^2 + 8\)
   - intro: Bracket first, then square the whole bracket, then add.
   - ask: 7 − 3 =  [box=4, NO label]
   - ask: 4 squared, 4 × 4 =  [box=16, NO label]
   - ask: 16 + 8 =  [box=24, NO label]
   - ask: Read it back: 16 + 8 =  [box=24, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: \(60 - 2 \times (3^2 + 1)\)
   - intro: Work inside the bracket first (its power, then its add), then multiply, then subtract.
   - ask: 3 squared, 3 × 3 =  [box=9, NO label]
   - ask: 9 + 1 =  [box=10, NO label]
   - ask: 2 × 10 =  [box=20, NO label]
   - ask: 60 − 20 =  [box=40, NO label]
   - ask: Read it back: 60 − 20 =  [box=40, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: \(\frac{6^2 - 12}{2 \times 3}\)
   - intro: The fraction bar groups the top and the bottom. Finish each, then divide.
   - ask: top: 6 squared, 6 × 6 =  [box=36, NO label]
   - ask: top: 36 − 12 =  [box=24, NO label]
   - ask: bottom: 2 × 3 =  [box=6, NO label]
   - ask: 24 ÷ 6 =  [box=4, NO label]
   - ask: Read it back: 24 ÷ 6 =  [box=4, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: \(5 + \frac{(8-2)^2}{9}\)
   - intro: Build the fraction first (bracket, then power, then divide), then add the 5.
   - ask: bracket: 8 − 2 =  [box=6, NO label]
   - ask: 6 squared, 6 × 6 =  [box=36, NO label]
   - ask: 36 ÷ 9 =  [box=4, NO label]
   - ask: 5 + 4 =  [box=9, NO label]
   - ask: Read it back: 5 + 4 =  [box=9, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(\sqrt{81} + 4 \times (2^3 - 3)\)
   - intro: Work the root, the bracket (its power first), then the multiply, then the add.
   - ask: √81 =  [box=9, NO label]
   - ask: 2 cubed, 2 × 2 × 2 =  [box=8, NO label]
   - ask: bracket: 8 − 3 =  [box=5, NO label]
   - ask: 4 × 5 =  [box=20, NO label]
   - ask: 9 + 20 =  [box=29, NO label]
   - ask: Read it back: 9 + 20 =  [box=29, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: \(\frac{(3+5)^2}{4} - 2^3\)
   - intro: Finish the fraction (bracket, power, divide), work the other power, then subtract.
   - ask: bracket: 3 + 5 =  [box=8, NO label]
   - ask: 8 squared, 8 × 8 =  [box=64, NO label]
   - ask: 64 ÷ 4 =  [box=16, NO label]
   - ask: 2 cubed, 2 × 2 × 2 =  [box=8, NO label]
   - ask: 16 − 8 =  [box=8, NO label]
   - ask: Read it back: 16 − 8 =  [box=8, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: \(2 \times 3^2 + \frac{40}{2^3}\)
   - intro: Do both powers first, then the × and the fraction, then add.
   - ask: 3 squared, 3 × 3 =  [box=9, NO label]
   - ask: 2 × 9 =  [box=18, NO label]
   - ask: 2 cubed, 2 × 2 × 2 =  [box=8, NO label]
   - ask: 40 ÷ 8 =  [box=5, NO label]
   - ask: 18 + 5 =  [box=23, NO label]
   - ask: Read it back: 18 + 5 =  [box=23, NO label]
