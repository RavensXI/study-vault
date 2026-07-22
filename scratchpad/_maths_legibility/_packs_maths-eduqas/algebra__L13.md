# maths-eduqas / algebra / L13 - Sequences & nth Term

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the 10th term of the sequence \(4, 9, 14, 19, ...\)
   - intro: A straight-line sequence, so build its rule first.
   - ask: Common difference: 9 − 4 =  [box=5, NO label]
   - ask: Zero term: 4 − 5 =  [box=-1, NO label]
   - intro: Now use the rule for n = 10.
   - ask: The 5n part of the 10th term: 5 × 10 =  [box=50, NO label]
   - ask: Add the zero term: 50 − 1 =  [box=49, NO label]
   - ask: Check the rule rebuilds term 1: 5 × 1 − 1 =  [box=4, NO label]

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(5, 9, 13, 17, ...\)

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(3, 7, 11, 15, ...\)

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(2, 5, 8, 11, ...\)

## bronze[4] (input: single_value, main-box unit: (none))
Q: Find the common difference of \(8, 5, 2, -1, ...\)
   - intro: The common difference is how much you add each step. Subtract in order: the later term minus the earlier one.
   - ask: First gap: 5 − 8 =  [box=-3, NO label]
   - intro: Check the gap stays the same all the way along.
   - ask: Next gap: 2 − 5 =  [box=-3, NO label]
   - ask: And the next: −1 − 2 =  [box=-3, NO label]

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(10, 15, 20, 25, ...\)

## bronze[6] (input: single_value, main-box unit: (none))
Q: Find the 20th term of \(1, 4, 7, 10, ...\)
   - intro: Straight-line sequence: build the rule, then jump to n = 20.
   - ask: Common difference: 4 − 1 =  [box=3, NO label]
   - ask: Zero term: 1 − 3 =  [box=-2, NO label]
   - intro: Now use the rule for n = 20.
   - ask: The 3n part of the 20th term: 3 × 20 =  [box=60, NO label]
   - ask: Add the zero term: 60 − 2 =  [box=58, NO label]
   - ask: Check term 1: 3 × 1 − 2 =  [box=1, NO label]

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(6, 10, 14, 18, ...\)

## silver[0] (input: single_value, main-box unit: (none))
Q: The nth term is \(5n - 2\). Which term has value \(73\)?
   - intro: We know the value (73) and want the position n, so solve an equation.
   - ask: Set \(5n - 2 = 73\). Add 2 to both sides: 5n =  [box=75, NO label]
   - intro: Now undo the multiply.
   - ask: Divide by 5: n = 75 ÷ 5 =  [box=15, NO label]
   - ask: Check term 15: 5 × 15 − 2 =  [box=73, NO label]

## silver[1] (input: multiple_choice, main-box unit: (none))
Q: Is \(83\) in the sequence \(5, 8, 11, 14, ...\)?

## silver[2] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(20, 17, 14, 11, ...\)

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(-1, 3, 7, 11, ...\)

## silver[4] (input: single_value, main-box unit: (none))
Q: The 5th term is \(19\) and the common difference is \(4\). Find the first term.
   - intro: From the 1st term to the 5th term there are 4 steps of d.
   - ask: Number of steps: 5 − 1 =  [box=4, NO label]
   - ask: Total rise over those steps: 4 × 4 =  [box=16, NO label]
   - intro: Undo the rise to reach the first term.
   - ask: Step back from the 5th term: 19 − 16 =  [box=3, NO label]
   - ask: Check: from 3, the 5th term is 3 + 4 × 4 =  [box=19, NO label]

## silver[5] (input: multiple_choice, main-box unit: (none))
Q: Is \(50\) a term in the sequence \(3, 7, 11, 15, ...\)?

## silver[6] (input: single_value, main-box unit: (none))
Q: Find the sum of the first 5 terms of \(2, 5, 8, 11, ...\)
   - intro: Write out all 5 terms first, then add.
   - ask: The terms are 2, 5, 8, 11, then the 5th is 11 + 3 =  [box=14, NO label]
   - ask: Add the first pair: 2 + 5 =  [box=7, NO label]
   - intro: Add the terms one at a time.
   - ask: Running total with 8: 7 + 8 =  [box=15, NO label]
   - ask: Add 11: 15 + 11 =  [box=26, NO label]
   - ask: Add the last term 14: 26 + 14 =  [box=40, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Two sequences: \(3, 7, 11, 15, ...\) and \(5, 8, 11, 14, ...\). Find the smallest number that appears in both.
   - intro: A shared value must appear in BOTH lists. First list: 3, 7, 11, 15, ... Second list: 5, 8, 11, 14, ...
   - ask: The 3rd term of the first list: 4 × 3 − 1 =  [box=11, NO label]
   - intro: Test whether 11 also belongs to the second sequence.
   - ask: Is 11 in the second list? Solve \(3m + 2 = 11\), so 3m = 11 − 2 =  [box=9, NO label]
   - ask: m = 9 ÷ 3 =  [box=3, NO label]
   - ask: Check nothing smaller is shared: is 7 in the second list? 3m + 2 = 7 gives 3m =  [box=5, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The nth term is \(an + b\). The 3rd term is \(11\) and the 7th is \(23\). Find \(a\).
   - intro: Two equations: 3rd term \(3a + b = 11\), and 7th term \(7a + b = 23\). Subtract to remove b.
   - ask: Subtract the equations: (7a + b) − (3a + b) leaves 4a. The right side: 23 − 11 =  [box=12, NO label]
   - intro: The b cancels, leaving 4a. Solve for a.
   - ask: So 4a = 12. Divide by 4: a = 12 ÷ 4 =  [box=3, NO label]
   - ask: Check the step count: from the 3rd to the 7th term is 7 − 3 =  [box=4, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Find the value of \(b\) (from the previous question).
   - intro: Use a = 3 in the 3rd-term equation \(3a + b = 11\).
   - ask: Work out 3a: 3 × 3 =  [box=9, NO label]
   - intro: Substitute and solve for b.
   - ask: So 9 + b = 11. Then b = 11 − 9 =  [box=2, NO label]
   - ask: Check the 7th term: 7 × 3 + 2 =  [box=23, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: The sum of the first \(n\) terms of \(4, 7, 10, ...\) is 175. Find \(n\).
   - intro: Use the sum formula \(S_n = \frac{n}{2}(2a + (n-1)d)\) with \(a = 4\), \(d = 3\).
   - ask: The bracket 2a + (n − 1)d = 8 + 3(n − 1) = 3n + 5, so \(\frac{n}{2}(3n + 5) = 175\). Times both sides by 2: n(3n + 5) =  [box=350, NO label]
   - intro: Solve the quadratic; only a positive whole n makes sense.
   - ask: Expand to \(3n^2 + 5n - 350 = 0\), which factorises to (n − 10)(3n + 35) = 0. The positive whole solution is n =  [box=10, NO label]
   - ask: Check: the 10th term is 3 × 10 + 1 = 31, so \(S_{10} = \frac{10}{2}(4 + 31)\) = 5 × 35 =  [box=175, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: An arithmetic sequence has first term \(a = 7\) and common difference \(d = -2\). How many positive terms are in the sequence?
   - intro: Find the nth term rule, then see where it stops being positive.
   - ask: Zero term: first term minus d = 7 − (−2) =  [box=9, NO label]
   - intro: Solve the inequality for n.
   - ask: Positive means 9 − 2n > 0, so 2n < 9, giving n < 4.5. The largest whole n is  [box=4, NO label]
   - ask: Check term 4: 9 − 2 × 4 =  [box=1, NO label]
   - ask: Check term 5: 9 − 2 × 5 =  [box=-1, NO label]
