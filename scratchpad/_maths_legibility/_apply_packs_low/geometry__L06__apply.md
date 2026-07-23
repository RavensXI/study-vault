# apply-pack: geometry__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] bronze[1] | Check the third angle: 180° − 35° − 25.5° = [box=119.5, NO label] | fix: Relabel to make clear this is a separate angle, not the answer, e.g. 'Angle C (a separate angle, not the one asked for): 180° − 35° − 25.5° =', or drop the 'Che
- [low] silver[2] | Q: 1086?Diagram not drawn accuratelyFind angle A when a = 10, b = 8, c = 6. | fix: Separate the side labels so they read '10, 8, 6' rather than '1086'.
- [low] silver[5] | Q: 91114?Diagram not drawn accuratelyUse the cosine rule: a = 9, b = 11, c = 14. | fix: Separate the side labels so they read '9, 11, 14' rather than '91114'.
- [low] gold[2] | Q: 567?Diagram not drawn accuratelyA triangle has sides 5, 6, and 7. | fix: Separate the side labels so they read '5, 6, 7' rather than '567'.
- [low] bronze[1] (and every diagram problem) | Q: 101230°Area = ?Diagram not drawn accurately Find the area of this triangle... | fix: Strip the run-together diagram-label text from the question stem (or space it out), leaving only the readable sentence ‘Find the area of this triangle: sides 10

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[1] Q: 12935°?ABCDiagram not drawn accurately Find angle \(B\): \(a = 12\), \(b = 9\), \(A = 35°\
   step0 field=say answer=None text='Sine rule for an angle: \\(\\frac{\\sin B}{b} = \\frac{\\sin A}{a}\\), so \\(\\sin B = \\frac{b\\sin'
   step1 field=pre answer=5.1622 text='Top line: 9 × sin 35° ='
   step2 field=pre answer=0.4302 text='Divide by 12: 5.1622 ÷ 12 ='
   step3 field=pre answer=25.5 text='Inverse sine: sin⁻¹(0.4302) ='
   step4 field=pre answer=119.5 text='Check the third angle: 180° − 35° − 25.5° ='

gold[2] Q: 1012?PQRArea = 40Diagram not drawn accurately Triangle PQR has area 40 cm², PQ = 10 cm, PR
   step0 field=say answer=None text='Area = ½ × PQ × PR × sin P, so 40 = ½ × 10 × 12 × sin P.'
   step1 field=pre answer=60 text='Half the product of the sides: ½ × 10 × 12 ='
   step2 field=pre answer=0.6667 text='Rearrange for sin P: 40 ÷ 60 ='
   step3 field=pre answer=41.8 text='Inverse sine: sin⁻¹(0.6667) ='
   step4 field=pre answer=40 text='Check: ½ × 10 × 12 × sin 41.8° rounds to'

silver[2] Q: 1114?75°ABCDiagram not drawn accurately A triangle has sides 11 cm and 14 cm and an includ
   step0 field=say answer=None text='Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\). Two sides 11 and 14 with the angl'
   step1 field=pre answer=317 text='Square and add the two sides: 11² + 14² = 121 + 196 ='
   step2 field=pre answer=79.7163 text='The subtracted part: 2 × 11 × 14 × cos 75° ='
   step3 field=pre answer=237.2837 text='So c² = 317 − (79.7163) ='
   step4 field=pre answer=15.4 text='Square root: √237.2837 ='

silver[5] Q: 1520?110°ABCDiagram not drawn accurately Find side \(a\) using cosine rule: \(b = 15\), \(
   step0 field=say answer=None text='Cosine rule for a side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\). Two sides 15 and 20 with the angl'
   step1 field=pre answer=625 text='Square and add the two sides: 15² + 20² = 225 + 400 ='
   step2 field=pre answer=-205.2121 text='The subtracted part: 2 × 15 × 20 × cos 110° ='
   step3 field=pre answer=830.2121 text='So a² = 625 − (-205.2121) ='
   step4 field=pre answer=28.8 text='Square root: √830.2121 ='

### board=maths-edexcel
bronze[1] Q: 8 cm5 cm40°Area = ?Diagram not drawn accuratelyFind the area of a triangle with sides 8 cm
   step0 field=say answer=None text='Area = \\(\\tfrac{1}{2}ab\\sin C\\), with a = 8, b = 5, C = 40°, and sin40° = 0.6428 (4 d.p.).'
   step1 field=pre answer=40 text='First the two sides: 8 × 5 ='
   step2 field=pre answer=20 text='Halve it: 40 ÷ 2 ='
   step3 field=pre answer=12.9 text='Multiply by sin40°: 20 × 0.6428 = ? (to 1 d.p.)'

gold[2] Q: 567?Diagram not drawn accuratelyA triangle has sides 5, 6, and 7. Find the largest angle t
   step0 field=say answer=None text='The largest angle sits opposite the longest side, which is 7. Call it C. \\(\\cos C = \\frac{'
   step1 field=pre answer=12 text='Top line, a² + b² − c² = 25 + 36 − 49 ='
   step2 field=pre answer=0.2 text='cosC = 12 ÷ 60 ='
   step3 field=pre answer=78.5 text='C = cos⁻¹(0.2) = ? (to 1 d.p.)'

silver[2] Q: 1086?Diagram not drawn accuratelyFind angle \(A\) when \(a = 10\), \(b = 8\), \(c = 6\). U
   step0 field=say answer=None text='Cosine rule for an angle: \\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\). Side a is opposite A. '
   step1 field=pre answer=0 text='Top line, b² + c² − a² = 64 + 36 − 100 ='
   step2 field=pre answer=0 text='cosA = 0 ÷ 96 ='
   step3 field=pre answer=90 text='A = cos⁻¹(0) = ? degrees'

silver[5] Q: 91114?Diagram not drawn accuratelyUse the cosine rule: \(a = 9\), \(b = 11\), \(c = 14\). 
   step0 field=say answer=None text='Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\). Side c is opposite C. '
   step1 field=pre answer=6 text='Top line, a² + b² − c² = 81 + 121 − 196 ='
   step2 field=pre answer=0.0303 text='cosC = 6 ÷ 198 = ? (to 4 d.p.)'
   step3 field=pre answer=88.3 text='C = cos⁻¹(0.0303) = ? (to 1 d.p.)'

### board=maths-ocr
bronze[1] Q: 101230°Area = ?Diagram not drawn accurately Find the area of this triangle: sides 10 and 1
   step0 field=say answer=None text='Area of a triangle: \\(\\frac12 ab\\sin C\\). The two sides are 10 and 12 with the included an'
   step1 field=pre answer=60.0 text='Half the product of the sides: ½ × 10 × 12 ='
   step2 field=pre answer=0.5 text='Sine of the angle: sin 30° ='
   step3 field=pre answer=30 text='Multiply: 60 × 0.5 ='
   step4 field=pre answer=30 text='Check the units: the area to 1 d.p. is'

gold[2] Q: 107100°?ABCDiagram not drawn accurately Sine rule (ambiguous case): \(a = 10\), \(b = 7\),
   step0 field=say answer=None text='Sine rule for the angle: \\(\\sin B = \\frac{b\\sin A}{a} = \\frac{7\\sin 100°}{10}\\).'
   step1 field=pre answer=6.8937 text='Top line: 7 × sin 100° ='
   step2 field=pre answer=0.6894 text='Divide by 10: 6.8937 ÷ 10 ='
   step3 field=pre answer=43.6 text='Inverse sine: sin⁻¹(0.6894) ='
   step4 field=pre answer=236.4 text='Test the other value: 100° + (180° − 43.6°) = 100° + 136.4° ='

silver[2] Q: 7912?ABCDiagram not drawn accurately Use the cosine rule to find the largest angle of a tr
   step0 field=say answer=None text='The largest angle faces the longest side (12). Call it C, with the other sides a=7 and b=9'
   step1 field=pre answer=-14 text='Top line: 7² + 9² − 12² = 49 + 81 − 144 ='
   step2 field=pre answer=126 text='Bottom line: 2 × 7 × 9 ='
   step3 field=pre answer=-0.1111 text='So cos C = −14 ÷ 126 ='
   step4 field=pre answer=96.4 text='Angle C: cos⁻¹(−0.1111) ='

silver[5] Q: 56?100°CBADiagram not drawn accurately Use the cosine rule to find side \(c\): \(a = 5\), 
   step0 field=say answer=None text='Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C = 5^2 + 6^2 - 2(5)(6)\\cos 100°\\).'
   step1 field=pre answer=61 text='Square and add: 5² + 6² = 25 + 36 ='
   step2 field=pre answer=-10.4189 text='The last term: 2 × 5 × 6 × cos 100° ='
   step3 field=pre answer=71.4189 text='So c² = 61 − (−10.4189) = 61 + 10.4189 ='
   step4 field=pre answer=8.5 text='Square root: √71.4189 ='

### board=maths-eduqas
bronze[1] Q: 10 cmb = ?65°45°Diagram not drawn accuratelySine rule: \(a = 10\), \(A = 45°\), \(B = 65°\
   step0 field=say answer=None text='b = a × sinB ÷ sinA. a = 10, A = 45°, B = 65°. sin65° = 0.9063, sin45° = 0.7071 (4 d.p.).'
   step1 field=pre answer=9.06 text='a × sinB = 10 × 0.9063 = ? (to 2 d.p.)'
   step2 field=pre answer=12.8 text='Divide by sinA: 9.06 ÷ 0.7071 = ? (to 1 d.p.)'
   step3 field=pre answer=12.8 text='Sense check: B (65°) is bigger than A (45°), so b should be bigger than a = 10. Enter b ag'

gold[2] Q: 11 cmPR = ?8 cm100°Diagram not drawn accuratelyIn triangle PQR, \(PQ = 8\) cm, \(QR = 11\)
   step0 field=say answer=None text='Angle Q is between PQ and QR, so PR is opposite it: \\(PR^2 = 8^2 + 11^2 - 2(8)(11)\\cos 100'
   step1 field=pre answer=185 text='8² + 11² = 64 + 121 ='
   step2 field=pre answer=-30.6 text='The last term, 176 × cos100° = 176 × (−0.1736) = ? (to 1 d.p.)'
   step3 field=pre answer=215.6 text='PR² = 185 − (−30.6) = 185 + 30.6 = ? (to 1 d.p.)'
   step4 field=pre answer=14.7 text='PR = √215.6 = ? (to 1 d.p.)'

silver[2] Q: 11 cm14 cm42°Area = ?Diagram not drawn accuratelyFind the area of a triangle with sides 11
   step0 field=say answer=None text='Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 11, b = 14, C = 42°, and sin42° = 0.6691 (4 d.p.).'
   step1 field=pre answer=154 text='The two sides: 11 × 14 ='
   step2 field=pre answer=77 text='Halve it: 154 ÷ 2 ='
   step3 field=pre answer=51.5 text='Multiply by sin42°: 77 × 0.6691 = ? (to 1 d.p.)'

silver[5] Q: 15 cm20 cm75°Area = ?Diagram not drawn accuratelyFind the area of a triangle with \(a = 15
   step0 field=say answer=None text='Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 15, b = 20, C = 75°, and sin75° = 0.9659 (4 d.p.).'
   step1 field=pre answer=300 text='The two sides: 15 × 20 ='
   step2 field=pre answer=150 text='Halve it: 300 ÷ 2 ='
   step3 field=pre answer=144.9 text='Multiply by sin75°: 150 × 0.9659 = ? (to 1 d.p.)'
