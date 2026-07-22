# maths-aqa / algebra / L13 - Sequences & nth Term

## bronze[0] (input: single_value, main-box unit: (none))
Q: Find the 20th term of the sequence \(3, 8, 13, 18, ...\)
   - intro: A straight-line sequence, so first build its rule.
   - ask: Common difference: 8 − 3 =  [box=5, NO label]
   - ask: Zero term: 3 − 5 =  [box=-2, NO label]
   - intro: Now use the rule for n = 20.
   - ask: The dn part of the 20th term: 5 × 20 =  [box=100, NO label]
   - ask: Add the constant: 100 − 2 =  [box=98, NO label]
   - ask: Check the rule rebuilds term 1: 5 × 1 − 2 =  [box=3, NO label]

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(2, 7, 12, 17, ...\)

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(5, 9, 13, 17, ...\)

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(10, 7, 4, 1, ...\)

## bronze[4] (input: single_value, main-box unit: (none))
Q: The nth term of a sequence is \(2n + 5\). Find the 10th term.
   - intro: The rule is already given, so just feed in n = 10.
   - ask: First the 2n part: 2 × 10 =  [box=20, NO label]
   - intro: Finish the substitution:
   - ask: Now add the constant: 20 + 5 =  [box=25, NO label]
   - ask: Check with n = 1: 2 × 1 + 5 =  [box=7, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: The nth term is \(3n - 1\). Which term has value 50?
   - intro: We know the value (50) and want the position n, so solve an equation.
   - ask: Set the rule equal to 50: \(3n − 1 = 50\). Add 1 to both sides: 3n =  [box=51, NO label]
   - intro: Now undo the multiply:
   - ask: Divide by 3: n = 51 ÷ 3 =  [box=17, NO label]
   - ask: Check term 17: 3 × 17 − 1 =  [box=50, NO label]

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(1, 4, 7, 10, ...\)

## bronze[7] (input: single_value, main-box unit: (none))
Q: Write down the first 4 terms of the sequence with nth term \(n^2 + 2\). What is the 4th term?
   - intro: The rule is given. Substitute n = 4, squaring first.
   - ask: Square n: 4² = 4 × 4 =  [box=16, NO label]
   - intro: Finish it off:
   - ask: Add the constant: 16 + 2 =  [box=18, NO label]
   - ask: Check the 1st term: 1² + 2 =  [box=3, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Is \(100\) a term in the sequence \(7, 13, 19, 25, ...\)? Enter 1 for Yes, 0 for No.
   - intro: First find the rule for this sequence.
   - ask: Common difference: 13 − 7 =  [box=6, NO label]
   - ask: Zero term: 7 − 6 =  [box=1, NO label]
   - intro: Set \(6n + 1 = 100\) and solve for the position n.
   - ask: Test 100. Subtract 1: \(6n = 100 − 1\) =  [box=99, NO label]
   - ask: Divide by 6: n = 99 ÷ 6 =  [box=16.5, NO label]
   - ask: n is not whole, so 100 is skipped. Enter 0 for No:  [box=0, NO label]

## silver[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of \(-1, 3, 7, 11, ...\)

## silver[2] (input: single_value, main-box unit: (none))
Q: Two sequences have nth terms \(3n + 1\) and \(5n - 9\). Find the smallest value that appears in both.
   - intro: A shared value must appear in BOTH lists. \(3n + 1\) gives 4, 7, 10, 13, 16, ... and \(5n − 9\) gives −4, 1, 6, 11, 16, ...
   - ask: The 5th term of \(3n + 1\): 3 × 5 + 1 =  [box=16, NO label]
   - intro: Test whether 16 also belongs to the second sequence.
   - ask: Is 16 in \(5n − 9\)? Solve \(5m − 9 = 16\), so 5m = 16 + 9 =  [box=25, NO label]
   - ask: m = 25 ÷ 5 =  [box=5, NO label]
   - ask: Confirm 16 in the first: 3 × 5 + 1 =  [box=16, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: The first term of an arithmetic sequence is \(a = 3\) and the common difference is \(d = -2\). Find the 15th term.
   - intro: From term 1 to term 15 there are 14 steps, each of size d.
   - ask: Number of steps: 15 − 1 =  [box=14, NO label]
   - intro: Each step subtracts 2, so find the total change:
   - ask: Total change: 14 × (−2) =  [box=-28, NO label]
   - ask: Add to the first term: 3 + (−28) =  [box=-25, NO label]
   - ask: Sanity check the 2nd term: 3 + 1 × (−2) =  [box=1, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Find the next term in \(2, 6, 18, 54, ...\)
   - intro: The gaps grow, so test for multiplying instead of adding.
   - ask: Ratio: 6 ÷ 2 =  [box=3, NO label]
   - ask: Confirm: 18 ÷ 6 =  [box=3, NO label]
   - intro: Multiply the last term by the ratio:
   - ask: Next term: 54 × 3 =  [box=162, NO label]
   - ask: Check backwards: 162 ÷ 3 =  [box=54, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: The nth term of a geometric sequence is \(5 \times 2^{n-1}\). Find the 6th term.
   - intro: Work the power first, then multiply by the 5.
   - ask: The power: n − 1 = 6 − 1 =  [box=5, NO label]
   - intro: Raise 2 to the power you found:
   - ask: 2 to that power: 2⁵ =  [box=32, NO label]
   - ask: Multiply by 5: 5 × 32 =  [box=160, NO label]
   - ask: Check the 1st term: 5 × 2⁰ = 5 × 1 =  [box=5, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: The 5th term of an arithmetic sequence is 17 and the 8th term is 26. Find the first term.
   - intro: First find the common difference from the two known terms.
   - ask: Steps from 5th to 8th term: 8 − 5 =  [box=3, NO label]
   - ask: Total rise: 26 − 17 =  [box=9, NO label]
   - ask: So d = 9 ÷ 3 =  [box=3, NO label]
   - intro: Now step back 4 places from the 5th term:
   - ask: Step back from the 5th term to the 1st (4 steps down): 17 − 4 × 3 =  [box=5, NO label]
   - ask: Check: from first term 5, the 5th term is 5 + 4 × 3 =  [box=17, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: The sum of the first \(n\) terms of a sequence is \(S_n = n^2 + 3n\). Find the 10th term of the sequence.
   - intro: \(S_n\) is the running total. The 10th term is the jump from \(S_9\) to \(S_{10}\).
   - ask: S₁₀ = 10² + 3 × 10 = 100 + 30 =  [box=130, NO label]
   - ask: S₉ = 9² + 3 × 9 = 81 + 27 =  [box=108, NO label]
   - intro: Subtract to peel off just the 10th term:
   - ask: 10th term = S₁₀ − S₉ = 130 − 108 =  [box=22, NO label]
   - ask: Check the 1st term: S₁ = 1² + 3 × 1 =  [box=4, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: A geometric sequence has first term 4 and common ratio \(\frac{1}{2}\). Find the sum of the first 5 terms as a fraction. Give the numerator (denominator is 4).
   - intro: The terms halve each time: 4, 2, 1, 1/2, 1/4. Turn every term into quarters so they add easily.
   - ask: 4 whole = 4 × 4 quarters =  [box=16, NO label]
   - ask: 2 whole = 2 × 4 quarters =  [box=8, NO label]
   - ask: 1 whole =  [box=4, NO label]
   - intro: Add every part, counted in quarters:
   - ask: Total quarters: 28 + 2 + 1 =  [box=31, NO label]
   - ask: Check as a decimal: 31 ÷ 4 =  [box=7.75, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Prove the nth term of \(5, 8, 11, 14, ...\) is \(3n + 2\). What is the 100th term?
   - intro: First confirm the rule really is \(3n + 2\).
   - ask: Common difference: 8 − 5 =  [box=3, NO label]
   - ask: Zero term: 5 − 3 =  [box=2, NO label]
   - intro: Now use the rule for n = 100.
   - ask: The 3n part of the 100th term: 3 × 100 =  [box=300, NO label]
   - ask: Add the constant: 300 + 2 =  [box=302, NO label]
   - ask: Check the rule at n = 2: 3 × 2 + 2 =  [box=8, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: A sequence starts \(k, 8, 2k+1, ...\) and is arithmetic. Find \(k\).
   - intro: Arithmetic means the gap between terms is the same, so set the two gaps equal.
   - ask: First gap is \(8 - k\); second gap is \((2k + 1) - 8 = 2k - 7\). Set \(8 - k = 2k - 7\), add k to both sides: \(8 = 3k - 7\). Add 7: 3k =  [box=15, NO label]
   - intro: Solve for k:
   - ask: Divide by 3: k = 15 ÷ 3 =  [box=5, NO label]
   - ask: Check the gaps with k = 5: the terms are 5, 8, 11, so each gap is  [box=3, NO label]
