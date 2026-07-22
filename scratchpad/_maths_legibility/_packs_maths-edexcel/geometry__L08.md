# maths-edexcel / geometry / L08 - Vectors

## bronze[0] (input: single_value, main-box unit: (none))
Q: \(\binom{4}{1} + \binom{2}{3}\) = ? Give the top component.
   - intro: Adding column vectors means adding matching rows. Line them up and start with the bottom.
   - ask: Bottom row: 1 + 3 =  [box=4, NO label]
   - ask: Now the row the question wants, the top: 4 + 2 =  [box=6, NO label]
   - ask: So the sum is (6, 4). The top component asked for is  [box=6, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: \(\binom{5}{-2} + \binom{-3}{6}\). Give the bottom component.
   - intro: Add the matching rows, keeping every sign.
   - ask: Top row: 5 + (−3) =  [box=2, NO label]
   - ask: Bottom row: (−2) + 6 =  [box=4, NO label]
   - ask: So the sum is (2, 4). The bottom component asked for is  [box=4, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: \(3 \times \binom{3}{-1}\). Give the top component.
   - intro: A scalar multiplies every row of the vector.
   - ask: Bottom row: 3 × (−1) =  [box=-3, NO label]
   - ask: Top row: 3 × 3 =  [box=9, NO label]
   - ask: So 3 × (3, −1) = (9, −3). The top component is  [box=9, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: \(\binom{7}{3} - \binom{4}{1}\). Give the top component.
   - intro: Subtract the matching rows, top from top and bottom from bottom.
   - ask: Bottom row: 3 − 1 =  [box=2, NO label]
   - ask: Top row: 7 − 4 =  [box=3, NO label]
   - ask: So the difference is (3, 2). The top component asked for is  [box=3, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: If \(\vec{OA} = \binom{3}{5}\) and \(\vec{OB} = \binom{10}{2}\), find the top component of \(\vec{AB}\).
   - intro: \(\vec{AB}\) is the journey from A to B, which is \(\mathbf{b} - \mathbf{a}\) (end minus start).
   - ask: Bottom of AB: 2 − 5 =  [box=-3, NO label]
   - ask: Top of AB: 10 − 3 =  [box=7, NO label]
   - ask: So \(\vec{AB}\) = (7, −3). The top component is  [box=7, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: 34?Find \(|\binom{3}{4}|\) (the magnitude).Diagram not drawn accurately
   - intro: Magnitude is Pythagoras on the two components: square, add, square root.
   - ask: Square the top: 3 × 3 =  [box=9, NO label]
   - ask: Square the bottom: 4 × 4 =  [box=16, NO label]
   - ask: Add the squares: 9 + 16 =  [box=25, NO label]
   - ask: Square root the total: √25 =  [box=5, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: \(2\mathbf{a} + 6\mathbf{a} = ?\) (in terms of \(\mathbf{a}\)). What is the coefficient?
   - intro: \(2\mathbf{a}\) and \(6\mathbf{a}\) point the same way, so you just add how many a's there are.
   - ask: Count the first: 2a has this many a's:  [box=2, NO label]
   - ask: Add the counts: 2 + 6 =  [box=8, NO label]
   - ask: So \(2\mathbf{a} + 6\mathbf{a} = 8\mathbf{a}\). The coefficient (number in front) is  [box=8, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: \(\binom{-1}{4} + \binom{1}{-4}\). Give the top component.
   - intro: These two vectors point in opposite directions. Add the matching rows with their signs.
   - ask: Bottom row: 4 + (−4) =  [box=0, NO label]
   - ask: Top row: (−1) + 1 =  [box=0, NO label]
   - ask: So the sum is (0, 0). The top component is  [box=0, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: \(\vec{OA} = \binom{2}{3}\), \(\vec{OB} = \binom{8}{-1}\). Find \(|\vec{AB}|\) to 1 d.p.
   - intro: First find \(\vec{AB} = \mathbf{b} - \mathbf{a}\), then its length by Pythagoras.
   - ask: AB top: 8 − 2 =  [box=6, NO label]
   - ask: AB bottom: (−1) − 3 =  [box=-4, NO label]
   - ask: Square and add: 36 + 16 =  [box=52, NO label]
   - ask: Square root, to 1 d.p.: √52 =  [box=7.2, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: If \(\mathbf{p} = \binom{3}{6}\), write a vector parallel to \(\mathbf{p}\) with top component equal to 1. Give the bottom component.
   - intro: A parallel vector is the same vector scaled. To make the top 1, divide everything by 3.
   - ask: New top: 3 ÷ 3 =  [box=1, NO label]
   - ask: Do the same to the bottom: 6 ÷ 3 =  [box=2, NO label]
   - ask: So the parallel vector is (1, 2). Check it is parallel: 3 × 2 should give the original bottom 6, so 3 × 2 =  [box=6, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(\vec{OA} = 5\mathbf{a}\), \(\vec{OB} = 3\mathbf{b}\). Find \(\vec{BA}\) in terms of \(\mathbf{a}\) and \(\mathbf{b}\). What is the coefficient of \(\mathbf{a}\)?
   - intro: \(\vec{BA}\) is the journey from B to A: \(\vec{BA} = \vec{OA} - \vec{OB}\).
   - ask: The a terms: OA has 5a, OB has none, so 5 − 0 =  [box=5, NO label]
   - ask: The b terms: 0 − 3 =  [box=-3, NO label]
   - ask: So \(\vec{BA} = 5\mathbf{a} - 3\mathbf{b}\). The coefficient of a is  [box=5, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: If \(\binom{2k}{3}\) is parallel to \(\binom{4}{6}\), find \(k\).
   - intro: Two column vectors are parallel when their cross products are equal: top1 × bottom2 = bottom1 × top2.
   - ask: Work the right side: bottom1 × top2 = 3 × 4 =  [box=12, NO label]
   - ask: The left side is 2k × 6 = 12k, so 12k = 12. Divide: 12 ÷ 12 =  [box=1, NO label]
   - ask: Check: with k = 1 the vector is (2, 3), and doubling the bottom, 2 × 3 =  [box=6, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: 123456712345OA(1, 5)B(7, 3)MM is the midpoint of AB. \(\vec{OA} = \binom{1}{5}\), \(\vec{OB} = \binom{7}{3}\). Find the top component of \(\vec{OM}\).
   - intro: The midpoint M has \(\vec{OM} = \tfrac{1}{2}(\vec{OA} + \vec{OB})\): add the position vectors, then halve.
   - ask: Add the bottoms: 5 + 3 =  [box=8, NO label]
   - ask: Now the tops: 1 + 7 =  [box=8, NO label]
   - ask: Halve the top: 8 ÷ 2 =  [box=4, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(\vec{AB} = \binom{-3}{5}\). Find \(\vec{BA}\). Give the top component.
   - intro: \(\vec{BA}\) is the reverse of \(\vec{AB}\): \(\vec{BA} = -\vec{AB}\), so flip the sign of each component.
   - ask: Flip the bottom: −(5) =  [box=-5, NO label]
   - ask: Flip the top: −(−3) =  [box=3, NO label]
   - ask: So \(\vec{BA}\) = (3, −5). The top component is  [box=3, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: 512?Find \(|\binom{-5}{12}|\).Diagram not drawn accurately
   - intro: Magnitude is Pythagoras on the components: square, add, square root. A negative squares to a positive.
   - ask: Square the top: (−5) × (−5) =  [box=25, NO label]
   - ask: Square the bottom: 12 × 12 =  [box=144, NO label]
   - ask: Add the squares: 25 + 144 =  [box=169, NO label]
   - ask: Square root the total: √169 =  [box=13, NO label]

## gold[0] (input: fraction, main-box unit: (none))
Q: acP12OABCOABC is a parallelogram. \(\vec{OA} = \mathbf{a}\), \(\vec{OC} = \mathbf{c}\). P divides AB in ratio 1:2. Express \(\vec{OP}\) in terms of \(\mathbf{a}\) and \(\mathbf{c}\). What is the coefficient of \(\mathbf{c}\)?Diagram not drawn accurately
   - intro: In parallelogram OABC, O and B are opposite corners, so \(\vec{OB} = \mathbf{a} + \mathbf{c}\).
   - ask: Find \(\vec{AB} = \vec{OB} - \vec{OA}\). The c's: OB has 1c, OA has none, so 1 − 0 =  [box=1, NO label]
   - intro: So \(\vec{AB} = \mathbf{c}\). P divides AB in ratio 1:2.
   - ask: Turn the ratio 1:2 into a fraction: AP is 1 part out of 1 + 2 =  [box=3, NO label]
   - ask: So AP = \(\tfrac{1}{3}\mathbf{c}\) and \(\vec{OP} = \mathbf{a} + \tfrac{1}{3}\mathbf{c}\). The coefficient of c is a fraction: its numerator (top) is  [box=1, NO label]
   - ask: Its denominator (bottom), from AP being one third of AB, is  [box=3, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: \(\vec{OA} = \mathbf{a}\), \(\vec{OB} = \mathbf{b}\). X is such that \(\vec{OX} = 2\mathbf{a} - \mathbf{b}\). Y is such that \(\vec{OY} = 4\mathbf{a} - 3\mathbf{b}\). Express \(\vec{XY}\) in terms of \(\mathbf{a}\) and \(\mathbf{b}\). What is the coefficient of \(\mathbf{a}\)?
   - intro: \(\vec{XY}\) is the journey from X to Y: \(\vec{XY} = \vec{OY} - \vec{OX}\).
   - ask: The b terms: OY has −3b, OX has −b, so −3 − (−1) =  [box=-2, NO label]
   - ask: The a terms: OY has 4a, OX has 2a, so 4 − 2 =  [box=2, NO label]
   - ask: So \(\vec{XY} = 2\mathbf{a} - 2\mathbf{b}\). The coefficient of a is  [box=2, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: Vectors \(3\mathbf{a} + k\mathbf{b}\) and \(6\mathbf{a} - 4\mathbf{b}\) are parallel. Find \(k\).
   - intro: Parallel means the second vector is a scalar multiple of the first: \(6\mathbf{a} - 4\mathbf{b} = \lambda(3\mathbf{a} + k\mathbf{b})\). The a terms fix \(\lambda\).
   - ask: The a terms: 6 = λ × 3, so λ = 6 ÷ 3 =  [box=2, NO label]
   - ask: The b terms: −4 = λ × k = 2k, so k = −4 ÷ 2 =  [box=-2, NO label]
   - ask: Check: with k = −2, the b term of 2 × (3a − 2b) is 2 × (−2) =  [box=-4, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: -1123412345OA(3, 1)B(-1, 5)N\(\vec{OA} = \binom{3}{1}\), \(\vec{OB} = \binom{-1}{5}\). N divides AB in ratio 3:1. Find the top component of \(\vec{ON}\).
   - intro: First find \(\vec{AB} = \mathbf{b} - \mathbf{a}\), then N is 3/4 of the way along (3 parts out of 3 + 1).
   - ask: AB top: −1 − 3 =  [box=-4, NO label]
   - ask: AN top: \(\tfrac{3}{4}\) × (−4) =  [box=-3, NO label]
   - ask: ON top = OA top + AN top = 3 + (−3) =  [box=0, NO label]
   - ask: Check with the bottom: AB bottom = 5 − 1 = 4, AN bottom = \(\tfrac{3}{4}\)(4) = 3, so ON bottom = 1 + 3 =  [box=4, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: 24624681012OA(1, 2)B(4, 8)C(6, 12)Points A\((1,2)\), B\((4,8)\) and C\((6,12)\) are collinear. Find \(\vec{AB}\) as a column vector and give the top component.
   - intro: For points, \(\vec{AB} = B - A\): the coordinates of B minus the coordinates of A.
   - ask: AB bottom: 8 − 2 =  [box=6, NO label]
   - ask: AB top: 4 − 1 =  [box=3, NO label]
   - ask: Check collinear: \(\vec{AC} = C - A = (5, 10)\), and (5, 10) = \(\tfrac{5}{3}\)(3, 6). The top component of AB asked for is  [box=3, NO label]
