# maths-ocr / algebra / L13 - Sequences & nth Term

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the 20th term of \(3, 7, 11, 15, ...\)
   - intro: A straight-line sequence, so build its rule first.
   - ask: Common difference: 7 − 3 =  [box=4, NO label]
   - ask: Zero term: 3 − 4 =  [box=-1, NO label]
   - intro: Now use the rule for n = 20.
   - ask: The dn part of the 20th term: 4 × 20 =  [box=80, NO label]
   - ask: Subtract the constant: 80 − 1 =  [box=79, NO label]
   - ask: Check the rule rebuilds term 1: 4 × 1 − 1 =  [box=3, NO label]

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(5, 9, 13, 17, ...\)

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(2, 5, 8, 11, ...\)

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(7, 12, 17, 22, ...\)

## bronze[4] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(1, 5, 9, 13, ...\)

## bronze[5] (input: single_value, main-box unit: (none))
Q: Find the common difference of \(10, 7, 4, 1, ...\)
   - intro: The common difference is any term minus the one before it.
   - ask: First difference: 7 − 10 =  [box=-3, NO label]
   - intro: Check the gap is the same each time:
   - ask: Second difference: 4 − 7 =  [box=-3, NO label]
   - ask: Third difference: 1 − 4 =  [box=-3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: What is the 5th term of the sequence with nth term \(2n + 3\)?
   - intro: The rule is given, so put n = 5 in.
   - ask: First the 2n part: 2 × 5 =  [box=10, NO label]
   - intro: Finish the substitution:
   - ask: Now add the constant: 10 + 3 =  [box=13, NO label]
   - ask: Check with n = 1: 2 × 1 + 3 =  [box=5, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Find the next term: \(3, 6, 12, 24, ...\)
   - intro: The gaps grow, so test for multiplying instead of adding.
   - ask: Ratio: 6 ÷ 3 =  [box=2, NO label]
   - ask: Confirm: 12 ÷ 6 =  [box=2, NO label]
   - intro: Multiply the last term by the ratio:
   - ask: Next term: 24 × 2 =  [box=48, NO label]
   - ask: Check backwards: 48 ÷ 2 =  [box=24, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Is \(50\) a term in the sequence \(7n + 1\)? Enter 1 for Yes, 0 for No.
   - intro: The rule is given. To test membership, set it equal to 50 and see if n is a whole number.
   - ask: Subtract the constant: 7n = 50 − 1 =  [box=49, NO label]
   - intro: Solve for the position n:
   - ask: Divide by 7: n = 49 ÷ 7 =  [box=7, NO label]
   - ask: n = 7 is a whole number, so 50 is a term. Enter 1 for Yes:  [box=1, NO label]

## silver[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(20, 17, 14, 11, ...\)

## silver[2] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(6, 3, 0, -3, ...\)

## silver[3] (input: single_value, main-box unit: (none))
Q: Find the common ratio of \(4, 12, 36, 108, ...\)
   - intro: Each term is the one before times a fixed ratio, so divide to find it.
   - ask: Ratio: 12 ÷ 4 =  [box=3, NO label]
   - intro: Check the ratio is the same all along:
   - ask: Confirm: 36 ÷ 12 =  [box=3, NO label]
   - ask: And 108 ÷ 36 =  [box=3, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Find the 8th term of the geometric sequence \(5, 10, 20, 40, ...\)
   - intro: Geometric: first term 5, ratio 2. The 8th term is 5 × 2 to a power.
   - ask: The power: n − 1 = 8 − 1 =  [box=7, NO label]
   - intro: Raise 2 to the power you found:
   - ask: 2 to that power: 2⁷ =  [box=128, NO label]
   - ask: Multiply by the first term: 5 × 128 =  [box=640, NO label]
   - ask: Check the 1st term: 5 × 2⁰ = 5 × 1 =  [box=5, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: The nth term of a sequence is \(n^2 + 1\). Find the 6th term.
   - intro: The rule is given. Substitute n = 6, squaring first.
   - ask: Square n: 6² = 6 × 6 =  [box=36, NO label]
   - intro: Finish it off:
   - ask: Add the constant: 36 + 1 =  [box=37, NO label]
   - ask: Check the 1st term: 1² + 1 =  [box=2, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Which term of the sequence \(3n - 5\) is equal to \(40\)?
   - intro: We know the value (40) and want the position n, so solve an equation.
   - ask: Set \(3n − 5 = 40\). Add 5 to both sides: 3n =  [box=45, NO label]
   - intro: Now undo the multiply:
   - ask: Divide by 3: n = 45 ÷ 3 =  [box=15, NO label]
   - ask: Check term 15: 3 × 15 − 5 =  [box=40, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: The first term of a geometric sequence is 2 and the 4th term is 54. Find the common ratio.
   - intro: Geometric: the 4th term is the first term multiplied by r three times, so \(2 × r^3 = 54\).
   - ask: Divide by the first term: r³ = 54 ÷ 2 =  [box=27, NO label]
   - intro: Undo the cube to find r:
   - ask: Cube root: r = ∛27 =  [box=3, NO label]
   - ask: Check the 4th term: 2 × 3³ = 2 × 27 =  [box=54, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The nth term of a sequence is \(2n^2 - 3\). Find the 5th term.
   - intro: The rule is given. Follow BIDMAS: square n first, then multiply, then subtract.
   - ask: Square n: 5² =  [box=25, NO label]
   - intro: Only n is squared, so multiply by 2 after squaring:
   - ask: Times 2: 2 × 25 =  [box=50, NO label]
   - ask: Subtract 3: 50 − 3 =  [box=47, NO label]
   - ask: Check the 1st term: 2 × 1² − 3 =  [box=-1, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: A geometric sequence has first term 100 and common ratio 0.5. After how many terms is the value first below 1?
   - intro: Halve from 100 and count terms until you drop below 1.
   - ask: 6th term: 100 halved five times, 100 ÷ 32 =  [box=3.125, NO label]
   - ask: 7th term: halve again, 3.125 ÷ 2 =  [box=1.5625, NO label]
   - intro: Keep halving until below 1:
   - ask: 8th term: halve again, 1.5625 ÷ 2 =  [box=0.78125, label:'(a decimal)']
   - ask: That is below 1. Which term number is it?  [box=8, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: A sequence starts \(1, 1, 2, 3, 5, 8, 13, ...\) What is the 10th term?
   - intro: Each term is the sum of the two before it. Keep adding until the 10th.
   - ask: The 7th term is 13. The 8th: 8 + 13 =  [box=21, NO label]
   - ask: 9th term: 13 + 21 =  [box=34, NO label]
   - intro: Add the last two each time to reach the 10th:
   - ask: 10th term: 21 + 34 =  [box=55, NO label]
   - ask: Count the terms 1, 1, 2, 3, 5, 8, 13, 21, 34, 55: the last is term number  [box=10, NO label]

## gold[4] (input: multiple_choice, main-box unit: (none))
Q: The sum of any 3 consecutive terms of the sequence \(2n + 1\) is always divisible by 3. What is the sum for terms \(n, n+1, n+2\)?
