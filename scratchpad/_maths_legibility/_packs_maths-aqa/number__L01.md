# maths-aqa / number / L01 - Four Operations & Order of Operations

## bronze[0] (input: single_value, main-box unit: (none))
Q: \(6 + 4 \times 3\)
   - intro: No brackets or powers. Multiplication comes before addition, so clear the × first.
   - ask: 4 × 3 =  [box=12, NO label]
   - ask: 6 + 12 =  [box=18, NO label]
   - ask: Read it back, 6 + 4 × 3 is 6 + 12 =  [box=18, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: \(20 - 8 \div 2\)
   - intro: Division comes before subtraction, so do the ÷ first.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - ask: 20 − 4 =  [box=16, NO label]
   - ask: Read it back, 20 − 8 ÷ 2 is 20 − 4 =  [box=16, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(5 \times 3 + 7 \times 2\)
   - intro: Two multiplications and one addition. Clear BOTH multiplications before adding.
   - ask: 5 × 3 =  [box=15, NO label]
   - ask: 7 × 2 =  [box=14, NO label]
   - ask: 15 + 14 =  [box=29, NO label]
   - ask: Read it back: the products are 15 and 14, total =  [box=29, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(24 \div 6 + 2 \times 5\)
   - intro: Do the ÷ and the × before the +.
   - ask: 24 ÷ 6 =  [box=4, NO label]
   - ask: 2 × 5 =  [box=10, NO label]
   - ask: 4 + 10 =  [box=14, NO label]
   - ask: Read it back: 4 plus 10 =  [box=14, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: \(3 + 5 \times 4 - 2\)
   - intro: One multiplication sits in the middle. Clear it, then work + and − left to right.
   - ask: 5 × 4 =  [box=20, NO label]
   - ask: 3 + 20 =  [box=23, NO label]
   - ask: 23 − 2 =  [box=21, NO label]
   - ask: Read it back: 3 + 20 − 2 =  [box=21, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(18 \div 2 \times 3\)
   - intro: Division and multiplication have equal priority. Work strictly left to right, so the ÷ comes first here.
   - ask: 18 ÷ 2 =  [box=9, NO label]
   - ask: 9 × 3 =  [box=27, NO label]
   - ask: Read it back: 18 ÷ 2 = 9, then × 3 =  [box=27, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(40 - 5 \times 6 + 2\)
   - intro: Clear the × first, then work − and + left to right.
   - ask: 5 × 6 =  [box=30, NO label]
   - ask: 40 − 30 =  [box=10, NO label]
   - ask: 10 + 2 =  [box=12, NO label]
   - ask: Read it back: 40 − 30 + 2 =  [box=12, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(7 + 3 \times 8 \div 4\)
   - intro: Clear the × and ÷ (left to right) before adding.
   - ask: 3 × 8 =  [box=24, NO label]
   - ask: 24 ÷ 4 =  [box=6, NO label]
   - ask: 7 + 6 =  [box=13, NO label]
   - ask: Read it back: 7 + 6 =  [box=13, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: \((3 + 5) \times 4\)
   - intro: Brackets first, always.
   - ask: 3 + 5 =  [box=8, NO label]
   - ask: 8 × 4 =  [box=32, NO label]
   - ask: Read it back: (3 + 5) × 4 = 8 × 4 =  [box=32, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: \(6 \times (9 - 4) + 3^2\)
   - intro: Do the bracket and the power before the × and +.
   - ask: 9 − 4 =  [box=5, NO label]
   - ask: 3 squared, 3 × 3 =  [box=9, NO label]
   - ask: 6 × 5 =  [box=30, NO label]
   - ask: 30 + 9 =  [box=39, NO label]
   - ask: Read it back: 30 + 9 =  [box=39, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(2^3 + 4 \times (7 - 3)\)
   - intro: Bracket and power first, then the × and +.
   - ask: 7 − 3 =  [box=4, NO label]
   - ask: 2 cubed, 2 × 2 × 2 =  [box=8, NO label]
   - ask: 4 × 4 =  [box=16, NO label]
   - ask: 8 + 16 =  [box=24, NO label]
   - ask: Read it back: 8 + 16 =  [box=24, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(50 - (2 + 3)^2\)
   - intro: Work the bracket, then square it, before subtracting.
   - ask: 2 + 3 =  [box=5, NO label]
   - ask: 5 squared, 5 × 5 =  [box=25, NO label]
   - ask: 50 − 25 =  [box=25, NO label]
   - ask: Read it back: 50 − 5² = 50 − 25 =  [box=25, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(3 \times (12 - 4) \div 6\)
   - intro: Bracket first, then × and ÷ left to right.
   - ask: 12 − 4 =  [box=8, NO label]
   - ask: 3 × 8 =  [box=24, NO label]
   - ask: 24 ÷ 6 =  [box=4, NO label]
   - ask: Read it back: 3 × 8 ÷ 6 =  [box=4, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(100 \div (4 + 6) \times 3\)
   - intro: Bracket first, then ÷ and × left to right.
   - ask: 4 + 6 =  [box=10, NO label]
   - ask: 100 ÷ 10 =  [box=10, NO label]
   - ask: 10 × 3 =  [box=30, NO label]
   - ask: Read it back: 100 ÷ 10 × 3 =  [box=30, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: \(4^2 - 3 \times (1 + 1)\)
   - intro: Bracket and power first, then × and −.
   - ask: 1 + 1 =  [box=2, NO label]
   - ask: 4 squared, 4 × 4 =  [box=16, NO label]
   - ask: 3 × 2 =  [box=6, NO label]
   - ask: 16 − 6 =  [box=10, NO label]
   - ask: Read it back: 16 − 6 =  [box=10, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: \(\dfrac{18 + 6}{2^2} + 5 \times 3\)
   - intro: The fraction bar groups the top. Work out the whole top, then the bottom, then divide.
   - ask: top: 18 + 6 =  [box=24, NO label]
   - ask: bottom: 2 squared =  [box=4, NO label]
   - ask: 24 ÷ 4 =  [box=6, NO label]
   - ask: the other term: 5 × 3 =  [box=15, NO label]
   - ask: 6 + 15 =  [box=21, NO label]
   - ask: Read it back: 6 + 15 =  [box=21, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: \((3 + 4)^2 - 5 \times (8 - 2)\)
   - intro: Two brackets, one power, one product. Clear the brackets and the power first.
   - ask: first bracket: 3 + 4 =  [box=7, NO label]
   - ask: second bracket: 8 − 2 =  [box=6, NO label]
   - ask: 7 squared, 7 × 7 =  [box=49, NO label]
   - ask: 5 × 6 =  [box=30, NO label]
   - ask: 49 − 30 =  [box=19, NO label]
   - ask: Read it back: 49 − 30 =  [box=19, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: \(5 \times 6 \div 3 + 4 \times (2 + 1)^2\)
   - intro: Bracket and power first, then handle each × and ÷ chain, then add.
   - ask: bracket: 2 + 1 =  [box=3, NO label]
   - ask: 3 squared, 3 × 3 =  [box=9, NO label]
   - ask: left chain: 5 × 6 =  [box=30, NO label]
   - ask: 30 ÷ 3 =  [box=10, NO label]
   - ask: 4 × 9 =  [box=36, NO label]
   - ask: 10 + 36 =  [box=46, NO label]
   - ask: Read it back: 10 + 36 =  [box=46, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: \(2^4 - (3 \times 2 + 1)^0 \times 8\)
   - intro: Work the bracket, then the powers, then the × and −.
   - ask: inside the bracket: 3 × 2 + 1 =  [box=7, NO label]
   - ask: 2 to the power 4, 2 × 2 × 2 × 2 =  [box=16, NO label]
   - ask: 7 to the power 0 =  [box=1, NO label]
   - ask: 1 × 8 =  [box=8, NO label]
   - ask: 16 − 8 =  [box=8, NO label]
   - ask: Read it back: 16 − 8 =  [box=8, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: \(\dfrac{(5-2)^3 + 3}{2 \times 5}\)
   - intro: The fraction bar groups top and bottom. Build the whole top, then the whole bottom, then divide.
   - ask: inside the top bracket: 5 − 2 =  [box=3, NO label]
   - ask: 3 cubed, 3 × 3 × 3 =  [box=27, NO label]
   - ask: top total: 27 + 3 =  [box=30, NO label]
   - ask: bottom: 2 × 5 =  [box=10, NO label]
   - ask: 30 ÷ 10 =  [box=3, NO label]
   - ask: Read it back: 30 ÷ 10 =  [box=3, NO label]
