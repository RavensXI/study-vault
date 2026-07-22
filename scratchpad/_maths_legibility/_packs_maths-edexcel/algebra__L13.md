# maths-edexcel / algebra / L13 - Sequences & nth Term

## bronze[0] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 2, 5, 8, 11, ...

## bronze[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 6, 10, 14, 18, ...

## bronze[2] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 1, 4, 7, 10, ...

## bronze[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 7, 12, 17, 22, ...

## bronze[4] (input: single_value, main-box unit: (none))
Q: Find the 10th term of the sequence with nth term \(2n + 3\)
   - intro: The formula \(2n + 3\) gives the value at position \(n\). For the 10th term, put \(n = 10\).
   - ask: First the 2n part: 2 × 10 =  [box=20, NO label]
   - ask: Now add the constant: 20 + 3 =  [box=23, NO label]
   - ask: Check: the 9th term is 2 × 9 + 3 = 21, and terms rise by 2, so 21 + 2 =  [box=23, NO label]

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 3, 5, 7, 9, ...

## bronze[6] (input: multiple_choice, main-box unit: (none))
Q: The nth term of a sequence is \(4n - 1\). What are the first three terms?

## bronze[7] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 10, 15, 20, 25, ...

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 20, 17, 14, 11, ...

## silver[1] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 50, 43, 36, 29, ...

## silver[2] (input: single_value, main-box unit: (none))
Q: Find the 15th term of the sequence 4, 9, 14, 19, ...
   - intro: The formula is not given, so find it first. Start with the common difference.
   - ask: Common difference: 9 − 4 =  [box=5, NO label]
   - ask: Constant: first term − d = 4 − 5 =  [box=-1, NO label]
   - intro: Now use \(5n - 1\) to find the 15th term. Put \(n = 15\).
   - ask: 5 × 15 =  [box=75, NO label]
   - ask: Subtract 1: 75 − 1 =  [box=74, NO label]
   - ask: Check the rule on the 3rd term: 5 × 3 − 1 =  [box=14, NO label]

## silver[3] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of −1, 3, 7, 11, ...

## silver[4] (input: single_value, main-box unit: (none))
Q: Is \(41\) in the sequence \(2, 5, 8, 11, \ldots\)? If so, which term?
   - intro: Find the rule for \(2, 5, 8, 11, \ldots\) first.
   - ask: Common difference: 5 − 2 =  [box=3, NO label]
   - ask: Constant: first term − d = 2 − 3 =  [box=-1, NO label]
   - intro: To test if 41 is in the sequence, solve \(3n - 1 = 41\). If \(n\) is a whole number, 41 is a term.
   - ask: Add 1 to both sides: 41 + 1 =  [box=42, NO label]
   - ask: Divide by 3: 42 ÷ 3 =  [box=14, NO label]
   - ask: Check: 3 × 14 − 1 =  [box=41, NO label]

## silver[5] (input: multiple_choice, main-box unit: (none))
Q: Find the nth term of 31, 25, 19, 13, ...

## silver[6] (input: single_value, main-box unit: (none))
Q: How many terms of the sequence 5, 8, 11, ... are less than 50?
   - intro: Find the rule for \(5, 8, 11, \ldots\) first.
   - ask: Common difference: 8 − 5 =  [box=3, NO label]
   - ask: Constant: first term − d = 5 − 3 =  [box=2, NO label]
   - intro: We want terms below 50, so solve \(3n + 2 < 50\). Take 2 from both sides first.
   - ask: 50 − 2 =  [box=48, NO label]
   - ask: 48 ÷ 3 =  [box=16, NO label]
   - intro: So \(n < 16\). As \(n\) must be a whole number, the largest is 15.
   - ask: Check the 15th term: 3 × 15 + 2 =  [box=47, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: The nth term of a sequence is \(3n + 7\). Which term has value 100?
   - intro: We want the position whose value is 100, so solve \(3n + 7 = 100\).
   - ask: Take 7 from both sides: 100 − 7 =  [box=93, NO label]
   - ask: Divide by 3: 93 ÷ 3 =  [box=31, NO label]
   - ask: Check: 3 × 31 + 7 =  [box=100, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Two sequences: \(4n + 1\) and \(3n + 5\). At what position do they first have the same value?
   - intro: The two sequences are equal when \(4n + 1 = 3n + 5\). Get the n terms on one side by subtracting \(3n\).
   - ask: 4n − 3n =  [box=1, label:'n']
   - ask: Take 1 from both sides: 5 − 1 =  [box=4, NO label]
   - ask: Check the first sequence at n = 4: 4 × 4 + 1 =  [box=17, NO label]
   - ask: Check the second at n = 4: 3 × 4 + 5 =  [box=17, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Find the sum of the first 5 terms of the sequence with nth term \(2n + 1\)
   - intro: List the first five terms of \(2n + 1\). Each is 2 more than the last.
   - ask: The 5th term: 2 × 5 + 1 =  [box=11, NO label]
   - intro: Now add the five terms together.
   - ask: 3 + 5 + 7 =  [box=15, NO label]
   - ask: 15 + 9 + 11 =  [box=35, NO label]
   - ask: Check: the middle term 7 times the 5 terms: 5 × 7 =  [box=35, NO label]

## gold[3] (input: multiple_choice, main-box unit: (none))
Q: The 3rd term of a sequence is 11 and the 7th term is 27. Find the nth term.

## gold[4] (input: single_value, main-box unit: (none))
Q: Find the first term greater than 200 in the sequence 3, 8, 13, 18, ...
   - intro: Find the rule for \(3, 8, 13, 18, \ldots\) first.
   - ask: Common difference: 8 − 3 =  [box=5, NO label]
   - ask: Constant: first term − d = 3 − 5 =  [box=-2, NO label]
   - intro: We want the first term over 200, so solve \(5n - 2 > 200\). Add 2 to both sides.
   - ask: 200 + 2 =  [box=202, NO label]
   - intro: Now find the smallest whole \(n\). Since \(5 \times 40 = 200\) is too small, try \(n = 41\).
   - ask: 5 × 41 =  [box=205, NO label]
   - ask: The term value: 205 − 2 =  [box=203, NO label]
