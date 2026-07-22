# apply-pack: graphs__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[0] | sin⁻¹(0.5) = [box=30, NO label] | fix: Add a bridging line before the box, e.g. 'sin⁻¹(0.5) means: the angle whose sine is 0.5 — press sin⁻¹ (or shift+sin) on the calculator.'
- [medium] silver[3] (pattern: also silver[2], silver[5], gold[0], gold[2], gold[3]) | B = sin⁻¹(0.8035) = ? (to 1 d.p.) [box=53.5, NO label] | fix: Either supply the inverse result inline, or add a one-line prompt: 'Use sin⁻¹ (shift + sin) on your calculator'
- [medium] silver[4] ask 3 | The other solution is 180° + 60° = 240°, so the smaller is [box=120] | fix: Restate both candidates in the same sentence: 'The other solution is 180° + 60° = 240°. The smaller of 120° and 240° is ___'.
- [medium] gold[0] ask 3 | The other solution is 360° − 30° = 330°, so the smaller is [box=210] | fix: Restate both candidates: 'The other solution is 360° − 30° = 330°. The smaller of 210° and 330° is ___'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: Solve \(\sin x = 0.5\) for \(0° \leq x \leq 360°\). Give the larger solution.
   step0 field=say answer=None text='Two solutions lie in the range. Find the first with the calculator, the second by symmetry'
   step1 field=pre answer=30 text='sin⁻¹(0.5) ='
   step2 field=pre answer=150 text='Sine is also positive in the second quadrant, so the other solution is 180° − 30° ='
   step3 field=pre answer=150 text='The larger of 30° and 150° is'

silver[3] Q: What is \(\sin 270°\)?
   step0 field=say answer=None text='270° is three-quarters of the way round, at the bottom of the sine wave.'
   step1 field=pre answer=270 text='Three-quarters of a full 360° cycle is (3 ÷ 4) × 360° ='
   step2 field=pre answer=-1 text='At that point the sine curve is at its lowest. The minimum value of sine is'
   step3 field=pre answer=-1 text='So sin 270° ='

silver[4] Q: Solve \(\cos x = 0\) for \(0° \leq x \leq 360°\). Give the first (smaller) value.
   step0 field=say answer=None text='cos x = 0 where the cosine curve crosses the x-axis. Find the first such angle.'
   step1 field=pre answer=1 text='The cosine curve starts at its maximum, cos 0° ='
   step2 field=pre answer=90 text='It first drops to zero a quarter of a cycle later. A quarter of 360° ='
   step3 field=pre answer=90 text='So the first solution of cos x = 0 is x ='

### board=maths-edexcel
gold[0] Q: 8 cm11 cm?Area = 30 cm²Diagram not drawn accuratelyTwo sides of a triangle are 8 cm and 11
   step0 field=say answer=None text='Work backwards from the area. Area = \\(\\tfrac{1}{2}ab\\sin C\\), so sinC = 2 × Area ÷ (a × b'
   step1 field=pre answer=88 text='a × b = 8 × 11 ='
   step2 field=pre answer=0.6818 text='sinC = (2 × 30) ÷ 88 = 60 ÷ 88 = ? (to 4 d.p.)'
   step3 field=pre answer=43.0 text='C = sin⁻¹(0.6818) = ? (to 1 d.p.)'

silver[3] Q: 12 cm15 cm?40°Diagram not drawn accuratelyUse the sine rule to find angle \(B\): \(a = 12\
   step0 field=say answer=None text='Sine rule for an angle: sinB = b × sinA ÷ a. a = 12, A = 40°, b = 15. sin40° = 0.6428 (4 d'
   step1 field=pre answer=9.642 text='b × sinA = 15 × 0.6428 = ? (to 3 d.p.)'
   step2 field=pre answer=0.8035 text='sinB = 9.642 ÷ 12 = ? (to 4 d.p.)'
   step3 field=pre answer=53.5 text='B = sin⁻¹(0.8035) = ? (to 1 d.p.)'

silver[4] Q: 11 cm13 cm52°Area = ?Diagram not drawn accuratelyFind the area of triangle with \(a = 11\)
   step0 field=say answer=None text='Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 11, b = 13, C = 52°, and sin52° = 0.7880 (4 d.p.).'
   step1 field=pre answer=143 text='The two sides: 11 × 13 ='
   step2 field=pre answer=71.5 text='Halve it: 143 ÷ 2 ='
   step3 field=pre answer=56.3 text='Multiply by sin52°: 71.5 × 0.7880 = ? (to 1 d.p.)'

### board=maths-ocr
gold[0] Q: Solve \(\sin x = -0.5\) for \(0° \le x \le 360°\). Give the smaller solution.
   step0 field=say answer=None text='sin is negative in the third and fourth quadrants. Start from the reference angle.'
   step1 field=pre answer=30 text='Ignoring the sign, sin⁻¹(0.5) ='
   step2 field=pre answer=210 text='In the third quadrant the solution is 180° + 30° ='
   step3 field=pre answer=210 text='The other solution is 360° − 30° = 330°, so the smaller is'

silver[3] Q: What is \(\tan 0°\)?
   step0 field=say answer=None text='The tangent curve starts at the origin. Build it from sine over cosine.'
   step1 field=pre answer=0 text='tan x = sin x ÷ cos x. At 0°, sin 0° ='
   step2 field=pre answer=1 text='And cos 0° ='
   step3 field=pre answer=0 text='So tan 0° = 0 ÷ 1 ='

silver[4] Q: \(\cos x = -0.5\). Give the smaller solution for \(0° \le x \le 360°\).
   step0 field=say answer=None text='cos is negative in the second and third quadrants. Find the reference angle first.'
   step1 field=pre answer=60 text='Ignoring the sign, cos⁻¹(0.5) ='
   step2 field=pre answer=120 text='In the second quadrant the solution is 180° − 60° ='
   step3 field=pre answer=120 text='The other solution is 180° + 60° = 240°, so the smaller is'

### board=maths-eduqas
gold[0] Q: Solve \(\sin x = 0.5\) for \(0° \le x \le 360°\). Give the larger solution.
   step0 field=say answer=None text='Start from the exact value: \\(\\sin 30° = 0.5\\).'
   step1 field=pre answer=30 text='The reference angle, the exact angle whose sine is 0.5, is'
   step2 field=pre answer=150 text='Sine is positive in the second quadrant too. The second solution is 180 − 30 ='
   step3 field=pre answer=150 text='The two solutions are 30° and 150°; the larger is'

silver[3] Q: What is the value of \(\sin 30°\)?

silver[4] Q: What is the value of \(\cos 120°\)?
   step0 field=say answer=None text='120° is past 90°, so on the cosine curve the height is negative here.'
   step1 field=pre answer=60 text='Find the reference angle, how far 120° is from 180°: 180 − 120 ='
   step2 field=pre answer=0.5 text='The matching first-quadrant value is cos 60° ='
   step3 field=pre answer=-0.5 text='In the second quadrant cosine is negative, so cos 120° ='
