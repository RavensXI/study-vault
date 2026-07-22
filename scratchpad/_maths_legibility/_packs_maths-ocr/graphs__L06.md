# maths-ocr / graphs / L06 - Trigonometric Graphs

## bronze[0] (input: single_value, main-box unit: (none))
Q: What is \(\sin 0°\)?
   - intro: sin 0° is where the sine curve begins. Read it straight off the graph.
   - ask: The sine curve rises to a maximum of  [box=1, NO label]
   - ask: At the very start, x = 0°, the curve sits on the x-axis, so its height is  [box=0, NO label]
   - ask: So sin 0° =  [box=0, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: What is \(\cos 0°\)?
   - intro: cos 0° is where the cosine curve begins.
   - ask: The lowest the cosine curve ever drops is  [box=-1, NO label]
   - ask: But at the very start, x = 0°, the cosine curve is at its highest point, which is  [box=1, NO label]
   - ask: So cos 0° =  [box=1, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: What is \(\cos 180°\)?
   - intro: The cosine curve starts at the top and falls. Track it as far as 180°.
   - ask: At x = 0° the cosine curve is at its maximum, cos 0° =  [box=1, NO label]
   - ask: By x = 180° it has fallen to its lowest point. The minimum value of cosine is  [box=-1, NO label]
   - ask: So cos 180° =  [box=-1, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: What is the period of \(\sin x\), in degrees?
   - intro: The period is how far along x you travel before the wave repeats exactly.
   - ask: The sine curve reaches its first peak at x =  [box=90, NO label]
   - ask: It returns to the same height, moving the same way, after one full turn. One full turn is  [box=360, NO label]
   - ask: So the period of sin x is  [box=360, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: What is the period of \(\tan x\), in degrees?
   - intro: The tangent curve repeats sooner than a sine wave.
   - ask: The tan curve has its first vertical asymptote at x =  [box=90, NO label]
   - ask: It then repeats after only half a turn. Half of 360° =  [box=180, NO label]
   - ask: So the period of tan x is  [box=180, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: For \(0° \le x \le 360°\), at what value of \(x\) does \(\sin x\) reach its maximum? Give your answer in degrees.
   - intro: We want WHERE the sine wave is highest, not how high it goes.
   - ask: The maximum height of the sine curve is  [box=1, NO label]
   - ask: It first reaches that height a quarter of the way through the 360° cycle. A quarter of 360° =  [box=90, NO label]
   - ask: So sin x is at its maximum when x =  [box=90, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: For \(0° \le x \le 360°\), at what value of \(x\) does \(\sin x\) reach its minimum? Give your answer in degrees.
   - intro: The sine curve bottoms out three-quarters of the way along.
   - ask: The minimum height of the sine curve is  [box=-1, NO label]
   - ask: It reaches that low point three-quarters of the way through. (3 ÷ 4) × 360° =  [box=270, NO label]
   - ask: So sin x is at its minimum when x =  [box=270, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: For \(0° \le x \le 360°\), how many times does the graph of \(\sin x\) cross the x-axis?
   - intro: Count where the sine curve cuts the x-axis between 0° and 360° inclusive.
   - ask: It starts on the axis at x = 0°, that is crossing number  [box=1, NO label]
   - ask: It comes back to the axis at x = 180°, crossing number  [box=2, NO label]
   - ask: It finishes on the axis at x = 360°, crossing number  [box=3, NO label]
   - ask: So the number of crossings is  [box=3, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: Solve \(\sin x = 0.5\) for \(0° \le x \le 360°\). Give the smaller solution.
   - intro: The calculator gives the first solution; the smaller one is asked for.
   - ask: sin⁻¹(0.5) =  [box=30, NO label]
   - ask: The second solution, by symmetry, is 180° − 30° =  [box=150, NO label]
   - ask: The smaller of 30° and 150° is  [box=30, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: Solve \(\cos x = 0.5\) for \(0° \le x \le 360°\). Give the smaller solution.
   - intro: Find the calculator value, then check which solution is smaller.
   - ask: cos⁻¹(0.5) =  [box=60, NO label]
   - ask: The second solution is 360° − 60° =  [box=300, NO label]
   - ask: The smaller of 60° and 300° is  [box=60, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: \(\sin x = 0.5\). Give the second solution for \(0° \le x \le 360°\).
   - intro: The first solution is 30°; find the second by sine symmetry.
   - ask: sin⁻¹(0.5) =  [box=30, NO label]
   - ask: Sine is also positive in the second quadrant, so the second solution is 180° − 30° =  [box=150, NO label]
   - ask: So the second solution is  [box=150, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: What is \(\tan 0°\)?
   - intro: The tangent curve starts at the origin. Build it from sine over cosine.
   - ask: tan x = sin x ÷ cos x. At 0°, sin 0° =  [box=0, NO label]
   - ask: And cos 0° =  [box=1, NO label]
   - ask: So tan 0° = 0 ÷ 1 =  [box=0, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: \(\cos x = -0.5\). Give the smaller solution for \(0° \le x \le 360°\).
   - intro: cos is negative in the second and third quadrants. Find the reference angle first.
   - ask: Ignoring the sign, cos⁻¹(0.5) =  [box=60, NO label]
   - ask: In the second quadrant the solution is 180° − 60° =  [box=120, NO label]
   - ask: The other solution is 180° + 60° = 240°, so the smaller is  [box=120, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: \(\cos x = -0.5\). Give the second (larger) solution for \(0° \le x \le 360°\).
   - intro: The first solution is 120°; find the second in the third quadrant.
   - ask: The reference angle is cos⁻¹(0.5) =  [box=60, NO label]
   - ask: In the third quadrant the solution is 180° + 60° =  [box=240, NO label]
   - ask: So the larger solution is  [box=240, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: \(\cos x = 0.5\). Give the second (larger) solution for \(0° \le x \le 360°\).
   - intro: The first solution is 60°; find the second by cosine symmetry.
   - ask: cos⁻¹(0.5) =  [box=60, NO label]
   - ask: Cosine is also positive in the fourth quadrant, so the second solution is 360° − 60° =  [box=300, NO label]
   - ask: So the larger solution is  [box=300, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: Solve \(\sin x = -0.5\) for \(0° \le x \le 360°\). Give the smaller solution.
   - intro: sin is negative in the third and fourth quadrants. Start from the reference angle.
   - ask: Ignoring the sign, sin⁻¹(0.5) =  [box=30, NO label]
   - ask: In the third quadrant the solution is 180° + 30° =  [box=210, NO label]
   - ask: The other solution is 360° − 30° = 330°, so the smaller is  [box=210, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The maximum value of \(3\sin x + 2\) is?
   - intro: 3 sin x + 2 is largest when sin x is largest.
   - ask: The maximum value of sin x is  [box=1, NO label]
   - ask: So 3 sin x is at most 3 × 1 =  [box=3, NO label]
   - ask: Adding the 2: 3 + 2 =  [box=5, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: The minimum value of \(2\cos x - 1\) is?
   - intro: 2 cos x − 1 is smallest when cos x is smallest.
   - ask: The minimum value of cos x is  [box=-1, NO label]
   - ask: So 2 cos x is at least 2 × (−1) =  [box=-2, NO label]
   - ask: Subtracting 1: −2 − 1 =  [box=-3, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: How many solutions does \(\sin x = 0.3\) have for \(0° \le x \le 720°\)?
   - intro: Count solutions across the whole range by counting periods.
   - ask: The period of sin x is 360°, so the number of full periods in 720° is 720 ÷ 360 =  [box=2, NO label]
   - ask: The line y = 0.3 cuts each period of the sine wave this many times:  [box=2, NO label]
   - ask: So the total number of solutions is 2 × 2 =  [box=4, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Solve \(\tan x = 1\) for \(0° \le x \le 360°\). Give the smaller solution.
   - intro: tan has period 180°, so the second solution is 180° on from the first.
   - ask: tan⁻¹(1) =  [box=45, NO label]
   - ask: tan repeats every 180°, so the next solution is 45° + 180° =  [box=225, NO label]
   - ask: The smaller of 45° and 225° is  [box=45, NO label]
