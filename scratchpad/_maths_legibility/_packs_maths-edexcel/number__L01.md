# maths-edexcel / number / L01 - Four Operations & Order of Operations

## bronze[0] (input: single_value, main-box unit: (none))
Q: \(3 + 5 \times 2\)
   - intro: There are no brackets or indices. Multiplication outranks addition, so do 5 × 2 before the add.
   - ask: 5 × 2 =  [box=10, NO label]
   - intro: The calculation is now 3 + 10. Only the add is left.
   - ask: 3 + 10 =  [box=13, NO label]
   - ask: Check by working backwards: 13 − 3 =  [box=10, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: \(12 - 4 \times 2\)
   - intro: No brackets or indices. Multiplication comes before subtraction, so do 4 × 2 first.
   - ask: 4 × 2 =  [box=8, NO label]
   - intro: Now the calculation is 12 − 8.
   - ask: 12 − 8 =  [box=4, NO label]
   - ask: Check: 4 + 8 =  [box=12, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(6 \times 3 + 2\)
   - intro: Multiplication first: 6 × 3, then the add.
   - ask: 6 × 3 =  [box=18, NO label]
   - intro: Now it is 18 + 2.
   - ask: 18 + 2 =  [box=20, NO label]
   - ask: Check: 20 − 2 =  [box=18, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(15 \div 3 + 7\)
   - intro: Division outranks addition, so do 15 ÷ 3 first.
   - ask: 15 ÷ 3 =  [box=5, NO label]
   - intro: Now it is 5 + 7.
   - ask: 5 + 7 =  [box=12, NO label]
   - ask: Check: 12 − 7 =  [box=5, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: \(4 + 8 \div 2\)
   - intro: Division comes before addition, so do 8 ÷ 2 first.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - intro: Now it is 4 + 4.
   - ask: 4 + 4 =  [box=8, NO label]
   - ask: Check: 8 − 4 =  [box=4, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: \(10 - 2 \times 3 + 1\)
   - intro: Multiplication first: 2 × 3. Then the subtraction and addition are equal priority, so go left to right.
   - ask: 2 × 3 =  [box=6, NO label]
   - intro: Now it is 10 − 6 + 1. Left to right, so subtract first.
   - ask: 10 − 6 =  [box=4, NO label]
   - ask: 4 + 1 =  [box=5, NO label]
   - ask: Check: 5 − 1 + 6 =  [box=10, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(2 \times 3 \times 4\)
   - intro: Every operation here is multiplication, equal priority, so just work left to right.
   - ask: 2 × 3 =  [box=6, NO label]
   - intro: Now multiply that result by 4.
   - ask: 6 × 4 =  [box=24, NO label]
   - ask: Check: 24 ÷ 4 =  [box=6, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(20 \div 4 + 6\)
   - intro: Division comes before addition, so do 20 ÷ 4 first.
   - ask: 20 ÷ 4 =  [box=5, NO label]
   - intro: Now it is 5 + 6.
   - ask: 5 + 6 =  [box=11, NO label]
   - ask: Check: 11 − 6 =  [box=5, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: \(3 + 2^3 \times 2\)
   - intro: Indices come before multiplication. Work out 2³ first.
   - ask: 2³ =  [box=8, NO label]
   - ask: 8 × 2 =  [box=16, NO label]
   - intro: Now just the addition: 3 + 16.
   - ask: 3 + 16 =  [box=19, NO label]
   - ask: Check: 19 − 3 =  [box=16, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: \(18 \div 6 \times 3\)
   - intro: Divide and multiply are equal priority, so work left to right. Divide first.
   - ask: 18 ÷ 6 =  [box=3, NO label]
   - intro: Now multiply: 3 × 3.
   - ask: 3 × 3 =  [box=9, NO label]
   - ask: Check: 9 ÷ 3 =  [box=3, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \((5 + 3) \times 4 - 10\)
   - intro: Brackets first: work out 5 + 3.
   - ask: 5 + 3 =  [box=8, NO label]
   - ask: 8 × 4 =  [box=32, NO label]
   - intro: Now the subtraction: 32 − 10.
   - ask: 32 − 10 =  [box=22, NO label]
   - ask: Check: 22 + 10 =  [box=32, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: \(50 - 3 \times (4 + 2^2)\)
   - intro: Brackets first, and inside the bracket indices come before adding. Work out 2² first.
   - ask: 2² =  [box=4, NO label]
   - ask: 4 + 4 =  [box=8, NO label]
   - ask: 3 × 8 =  [box=24, NO label]
   - intro: Now the subtraction: 50 − 24.
   - ask: 50 − 24 =  [box=26, NO label]
   - ask: Check: 26 + 24 =  [box=50, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(4^2 - 2 \times 5\)
   - intro: Indices first: work out 4².
   - ask: 4² =  [box=16, NO label]
   - ask: 2 × 5 =  [box=10, NO label]
   - intro: Now subtract: 16 − 10.
   - ask: 16 − 10 =  [box=6, NO label]
   - ask: Check: 6 + 10 =  [box=16, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(100 \div (2 + 3) \times 2\)
   - intro: Brackets first: work out 2 + 3.
   - ask: 2 + 3 =  [box=5, NO label]
   - ask: 100 ÷ 5 =  [box=20, NO label]
   - intro: Now multiply: 20 × 2.
   - ask: 20 × 2 =  [box=40, NO label]
   - ask: Check: 40 ÷ 2 =  [box=20, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: \(7 + 3 \times 5 - 2^2\)
   - intro: Indices first: work out 2².
   - ask: 2² =  [box=4, NO label]
   - ask: 3 × 5 =  [box=15, NO label]
   - intro: Now add and subtract left to right: 7 + 15, then take off 4.
   - ask: 7 + 15 =  [box=22, NO label]
   - ask: 22 − 4 =  [box=18, NO label]
   - ask: Check: 18 + 4 − 15 =  [box=7, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: \(\dfrac{12 + 8}{2^2} + 3 \times 5\)
   - intro: The fraction bar acts like brackets. Work out the top: 12 + 8.
   - ask: 12 + 8 =  [box=20, NO label]
   - ask: 2² =  [box=4, NO label]
   - ask: 20 ÷ 4 =  [box=5, NO label]
   - ask: 3 × 5 =  [box=15, NO label]
   - intro: Now add the two parts: 5 + 15.
   - ask: 5 + 15 =  [box=20, NO label]
   - ask: Check: 20 − 15 =  [box=5, NO label]

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
Q: \(6 \times 8 \div 4 + 5 \times (3 - 1)^2\)
   - intro: Bracket first: 3 − 1.
   - ask: 3 − 1 =  [box=2, NO label]
   - ask: 2² =  [box=4, NO label]
   - ask: 6 × 8 =  [box=48, NO label]
   - ask: 48 ÷ 4 =  [box=12, NO label]
   - ask: 5 × 4 =  [box=20, NO label]
   - intro: Now add the two parts: 12 + 20.
   - ask: 12 + 20 =  [box=32, NO label]
   - ask: Check: 32 − 20 =  [box=12, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: \(2^4 - (3 \times 2 + 1)^0 \times 10\)
   - intro: Start with the powers and the bracket. First 2⁴.
   - ask: 2⁴ =  [box=16, NO label]
   - ask: 3 × 2 + 1 =  [box=7, NO label]
   - ask: 1 × 10 =  [box=10, NO label]
   - intro: Now subtract: 16 − 10.
   - ask: 16 − 10 =  [box=6, NO label]
   - ask: Check: 6 + 10 =  [box=16, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: \(\dfrac{5^2 + \sqrt{49}}{2^3}\)
   - intro: The fraction bar groups the top. Work out 5² first.
   - ask: 5² =  [box=25, NO label]
   - ask: √49 =  [box=7, NO label]
   - ask: 25 + 7 =  [box=32, NO label]
   - ask: 2³ =  [box=8, NO label]
   - intro: Now divide top by bottom: 32 ÷ 8.
   - ask: 32 ÷ 8 =  [box=4, NO label]
   - ask: Check: 4 × 8 =  [box=32, NO label]
