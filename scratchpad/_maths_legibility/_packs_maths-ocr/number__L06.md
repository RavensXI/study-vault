# maths-ocr / number / L06 - Powers, Roots & Standard Form

## bronze[0] (input: single_value, main-box unit: (none))
Q: Evaluate \(3^4\)
   - intro: A power tells you how many of the base to multiply. 3⁴ is four 3s.
   - ask: 3 × 3 =  [box=9, NO label]
   - ask: Now the third 3: 9 × 3 =  [box=27, NO label]
   - ask: And the fourth: 27 × 3 =  [box=81, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: Evaluate \(\sqrt{144}\)
   - intro: A square root asks: what number times itself gives 144? Try 10.
   - ask: 10 × 10 =  [box=100, NO label]
   - intro: Too small, go higher. Try 12.
   - ask: 12 × 12 =  [box=144, NO label]
   - ask: So √144 =  [box=12, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: Evaluate \(10^3\)
   - intro: 10³ is three 10s multiplied.
   - ask: 10 × 10 =  [box=100, NO label]
   - ask: Now the third 10: 100 × 10 =  [box=1000, NO label]
   - ask: The power 3 gives this many zeros:  [box=3, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: Evaluate \(\sqrt[3]{27}\)
   - intro: A cube root asks: what number cubed gives 27? Try 2.
   - ask: 2 × 2 × 2 =  [box=8, NO label]
   - intro: Too small. Try 3.
   - ask: 3 × 3 × 3 =  [box=27, NO label]
   - ask: So ∛27 =  [box=3, NO label]

## bronze[4] (input: standard_form, main-box unit: (none))
Q: Write \(56\,000\) in standard form
   - intro: Standard form is A × 10ⁿ with A between 1 and 10. Slide the point left until one non-zero digit sits in front.
   - ask: 56000 becomes A =  [box=5.6, NO label]
   - intro: Count how many places the point moved.
   - ask: Places the point moved =  [box=4, NO label]
   - ask: Check: 5.6 × 10000 =  [box=56000, NO label]

## bronze[5] (input: standard_form, main-box unit: (none))
Q: Write \(0.003\) in standard form
   - intro: Move the point right until one non-zero digit is in front. 0.003 becomes 3.
   - ask: A =  [box=3, NO label]
   - intro: Count the places the point moved: 0.003 to 3.
   - ask: Places moved =  [box=3, NO label]
   - ask: Small number, so n is negative. n =  [box=-3, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Evaluate \(5^2 + 3^2\)
   - intro: Powers come before adding. Square each number first.
   - ask: 5 × 5 =  [box=25, NO label]
   - intro: Now the other square.
   - ask: 3 × 3 =  [box=9, NO label]
   - intro: Now add the two squares.
   - ask: 25 + 9 =  [box=34, NO label]
   - ask: The trap is adding first: (5 + 3)² = 8² = 64. Our correct total is  [box=34, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Write \(8.1 \times 10^5\) as an ordinary number
   - intro: 10⁵ moves the decimal point 5 places to the right. First move:
   - ask: 8.1 × 10 =  [box=81, NO label]
   - ask: Now 4 more places (× 10000): 81 × 10000 =  [box=810000, NO label]
   - ask: Total places the point moved for 10⁵ =  [box=5, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Simplify \(2^3 \times 2^5\). Give your answer as a power of 2.
   - intro: Same base, so combine by counting the 2s. 2³ has three 2s.
   - ask: Number of 2s in 2³ =  [box=3, NO label]
   - intro: 2⁵ has five 2s.
   - ask: Number of 2s in 2⁵ =  [box=5, NO label]
   - intro: Multiplying puts them together.
   - ask: 3 + 5 =  [box=8, NO label]
   - ask: So the answer is 2 to the power  [box=8, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Simplify \(5^7 \div 5^3\). Give your answer as a power of 5.
   - intro: Dividing cancels matching 5s. Seven on top, three underneath.
   - ask: Fives on top =  [box=7, NO label]
   - ask: Cancel the three underneath: 7 − 3 =  [box=4, NO label]
   - ask: So the answer is 5 to the power  [box=4, NO label]

## silver[2] (input: fraction, main-box unit: (none))
Q: Evaluate \(4^{-2}\). Give your answer as a fraction.
   - intro: A negative index means 'one over'. Flip it: 4⁻² = 1 over 4². First find 4².
   - ask: 4 × 4 =  [box=16, NO label]
   - ask: Put it under 1, so the numerator (top) is  [box=1, NO label]
   - ask: and the denominator (bottom) is  [box=16, NO label]

## silver[3] (input: standard_form, main-box unit: (none))
Q: Calculate \((4 \times 10^3) \times (3 \times 10^5)\)
   - intro: Multiply the numbers, add the powers. Numbers first.
   - ask: 4 × 3 =  [box=12, NO label]
   - intro: Now the powers.
   - ask: 3 + 5 =  [box=8, NO label]
   - intro: So far 12 × 10⁸, but 12 is not between 1 and 10. Rewrite 12 as 1.2 × 10.
   - ask: The new A is  [box=1.2, NO label]
   - ask: That extra 10 lifts the power: 8 + 1 =  [box=9, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: Evaluate \(27^{1/3}\)
   - intro: A power of 1/3 means the cube root. What cubed gives 27? Try 3.
   - ask: 3 × 3 × 3 =  [box=27, NO label]
   - ask: That matches, so 27^(1/3) =  [box=3, NO label]
   - ask: It is not ÷ 3 (that would give 9). The cube root is  [box=3, NO label]

## silver[5] (input: standard_form, main-box unit: (none))
Q: Calculate \((8 \times 10^6) \div (2 \times 10^2)\)
   - intro: Divide the numbers, subtract the powers. Numbers first.
   - ask: 8 ÷ 2 =  [box=4, NO label]
   - ask: Now the powers: 6 − 2 =  [box=4, NO label]
   - ask: A is 4 (between 1 and 10), so no adjusting. The power n =  [box=4, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: Evaluate \(81^{3/4}\)
   - intro: Do the root (bottom number) first. The bottom is 4, so take the 4th root of 81. What to the 4th power gives 81? Try 3.
   - ask: 3 × 3 × 3 × 3 =  [box=81, NO label]
   - intro: So the 4th root of 81 is 3. Now apply the top number, the power 3.
   - ask: 3³ = 3 × 3 × 3 =  [box=27, NO label]
   - ask: So 81^(3/4) =  [box=27, NO label]

## gold[0] (input: standard_form, main-box unit: (none))
Q: Calculate \((6 \times 10^4) \times (5 \times 10^{-2})\)
   - intro: Numbers first, then powers.
   - ask: 6 × 5 =  [box=30, NO label]
   - intro: Add the powers, keeping the sign: 4 + (−2).
   - ask: 4 + (−2) =  [box=2, NO label]
   - intro: So far 30 × 10², but 30 is not between 1 and 10. Rewrite 30 as 3 × 10.
   - ask: The new A is  [box=3, NO label]
   - ask: The extra 10 lifts the power: 2 + 1 =  [box=3, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: Simplify \((3^2)^4\). Give your answer as a power of 3.
   - intro: (3²)⁴ means 3² written four times: 3² × 3² × 3² × 3². Same base, so add those indices.
   - ask: 2 + 2 + 2 + 2 =  [box=8, NO label]
   - ask: That is the same as multiplying: 2 × 4 =  [box=8, NO label]
   - ask: So (3²)⁴ = 3 to the power  [box=8, NO label]

## gold[2] (input: fraction, main-box unit: (none))
Q: Evaluate \(125^{-2/3}\). Give your answer as a fraction.
   - intro: Take it in pieces. The bottom 3 means cube root: ∛125. What cubed gives 125? Try 5.
   - ask: 5 × 5 × 5 =  [box=125, NO label]
   - intro: So ∛125 = 5. The top 2 means square it.
   - ask: 5 × 5 =  [box=25, NO label]
   - intro: The negative sign means take the reciprocal (1 over it).
   - ask: The top of the fraction is  [box=1, NO label]
   - ask: The bottom of the fraction is  [box=25, NO label]

## gold[3] (input: standard_form, main-box unit: (none))
Q: Calculate \((2 \times 10^5) + (3.5 \times 10^4)\)
   - intro: You cannot add until the powers match. Change 2 × 10⁵ into 10⁴ form: 2 × 10⁵ = 20 × 10⁴.
   - ask: So the A becomes 2 × 10 =  [box=20, NO label]
   - intro: Now both are × 10⁴, so add the A parts.
   - ask: 20 + 3.5 =  [box=23.5, NO label]
   - intro: That gives 23.5 × 10⁴, but 23.5 is not between 1 and 10. Rewrite as 2.35 × 10.
   - ask: New A =  [box=2.35, NO label]
   - ask: The extra 10 lifts the power: 4 + 1 =  [box=5, NO label]

## gold[4] (input: fraction, main-box unit: (none))
Q: Evaluate \(8^{2/3} \times 4^{-1/2}\). Give your answer as a fraction.
   - intro: Work out each power separately. 8^(2/3): cube root first, ∛8 = 2, then square.
   - ask: 2 × 2 =  [box=4, NO label]
   - intro: Now 4^(−1/2): the 1/2 is a square root, √4 = 2, and the minus flips it to 1/2. Multiply the two results.
   - ask: 4 × 1/2 =  [box=2, NO label]
   - ask: As a fraction that is 2/1, so the numerator is  [box=2, NO label]
   - ask: and the denominator is  [box=1, NO label]
