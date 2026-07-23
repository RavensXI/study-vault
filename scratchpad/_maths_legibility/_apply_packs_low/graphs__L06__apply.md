# apply-pack: graphs__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] ask 2 | The line y = 0.3 cuts each period of the sine wave this many times: [box=2] | fix: Add a building line before this step, e.g. 'In one up-and-down cycle the curve passes the height 0.3 once on the way up and once on the way down', then keep the
- [low] bronze[6] | That full-wave length is the period. Reading the graph, sine returns to 0 rising | fix: Rephrase to separate the ideas, e.g. 'Reading the graph, the sine curve comes back to 0 while rising (going upward) at x =' so the disambiguating 'rising' stand

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[6] Q: For \(0° \leq x \leq 360°\), how many times does the graph of \(y = \sin x\) cross the x-a
   step0 field=say answer=None text='Count where the sine curve cuts the x-axis between 0° and 360° inclusive.'
   step1 field=pre answer=1 text='It starts on the axis at x = 0°, that is crossing number'
   step2 field=pre answer=2 text='It comes back to the axis at x = 180°, crossing number'
   step3 field=pre answer=3 text='It finishes on the axis at x = 360°, crossing number'
   step4 field=pre answer=3 text='So the number of crossings is'

gold[3] Q: What is \(\sin 210°\)?
   step0 field=say answer=None text='210° is in the third quadrant, where sine is negative. Use the reference angle.'
   step1 field=pre answer=30 text='The reference angle is 210° − 180° ='
   step2 field=pre answer=0.5 text='The exact value sin 30° ='
   step3 field=pre answer=-0.5 text='Sine is negative in the third quadrant, so sin 210° ='

### board=maths-edexcel
bronze[6] Q: The cosine rule gives \(a^2 = 25 + 49 - 70\cos 60°\). Find \(a^2\).
   step0 field=say answer=None text='You are given \\(a^2 = 25 + 49 - 70\\cos 60°\\). Just work it out. cos60° = 0.5.'
   step1 field=pre answer=74 text='First 25 + 49 ='
   step2 field=pre answer=35 text='The last term: 70 × cos60° = 70 × 0.5 ='
   step3 field=pre answer=39 text='Subtract: 74 − 35 ='

gold[3] Q: 10 cm14 cm?30°Diagram not drawn accuratelyUse the sine rule to find the two possible value
   step0 field=say answer=None text='Sine rule for an angle: sinB = b × sinA ÷ a. a = 10, b = 14, A = 30°, and sin30° = 0.5.'
   step1 field=pre answer=7 text='b × sinA = 14 × 0.5 ='
   step2 field=pre answer=0.7 text='sinB = 7 ÷ 10 ='
   step3 field=pre answer=44.4 text='The acute answer, sin⁻¹(0.7) = ? (to 1 d.p.)'
   step4 field=pre answer=135.6 text='The question wants the OBTUSE angle: 180 − 44.4 ='

### board=maths-ocr
bronze[6] Q: For \(0° \le x \le 360°\), at what value of \(x\) does \(\sin x\) reach its minimum? Give 
   step0 field=say answer=None text='The sine curve bottoms out three-quarters of the way along.'
   step1 field=pre answer=-1 text='The minimum height of the sine curve is'
   step2 field=pre answer=270 text='It reaches that low point three-quarters of the way through. (3 ÷ 4) × 360° ='
   step3 field=pre answer=270 text='So sin x is at its minimum when x ='

gold[3] Q: How many solutions does \(\sin x = 0.3\) have for \(0° \le x \le 720°\)?
   step0 field=say answer=None text='Count solutions across the whole range by counting periods.'
   step1 field=pre answer=2 text='The period of sin x is 360°, so the number of full periods in 720° is 720 ÷ 360 ='
   step2 field=pre answer=2 text='The line y = 0.3 cuts each period of the sine wave this many times:'
   step3 field=pre answer=4 text='So the total number of solutions is 2 × 2 ='

### board=maths-eduqas
bronze[6] Q: What is the period of the graph \(y = \sin x\)? Give your answer in degrees.
   step0 field=say answer=None text='The period is the horizontal length of one complete wave, before the pattern repeats.'
   step1 field=pre answer=90 text='A quarter of the wave, from the start up to the first peak, spans 90°. One quarter ='
   step2 field=pre answer=360 text='A full wave is 4 of those quarters: 4 × 90 ='
   step3 field=pre answer=360 text='That full-wave length is the period. Reading the graph, sine returns to 0 rising at x ='

gold[3] Q: Solve \(\tan x = 0\) for \(0° \le x \le 360°\). How many solutions are there?
   step0 field=say answer=None text='\\(\\tan x = 0\\) where the tangent curve crosses the x-axis, which is where \\(\\sin x = 0\\).'
   step1 field=pre answer=180 text='The first zero is at x = 0°. The tan graph repeats every 180°, so the next zero is at x ='
   step2 field=pre answer=360 text='The next zero after 180° is at x ='
   step3 field=pre answer=3 text='Count the zeros at 0°, 180° and 360°: that is'
