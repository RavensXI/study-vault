# apply-pack: geometry__L06.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[3] | The product s(s−a)(s−b)(s−c): 17 × 9 × 6 × 2 = [box=1836, NO label] | fix: Add an intermediate step showing the subtractions: s−a = 17−8 = 9, s−b = 17−11 = 6, s−c = 17−15 = 2, before forming the product.
- [medium] gold[1] | Now area = ½ × 13 × 14 × sin67.4° = 91 × 0.9231 = ? (nearest whole number) | fix: Split into two steps: 'Half of 13 × 14: ½ × 13 × 14 = 91' then 'Multiply by sin67.4°: 91 × 0.9231 = ? cm² (nearest whole number)'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[1] Q: A ship sails 8 km from A to B on bearing 040°, then 6 km from B to C on bearing 150°. Find
   step0 field=say answer=None text='First the interior angle at B. The back bearing from B to A is 040 + 180 = 220°, and the b'
   step1 field=pre answer=70 text='Interior angle at B: 220° − 150° ='
   step2 field=say answer=None text='Now the cosine rule with AB = 8, BC = 6 and that 70° between them: \\(AC^2 = 8^2 + 6^2 - 2('
   step3 field=pre answer=100 text='Square and add: 8² + 6² = 64 + 36 ='
   step4 field=pre answer=32.8339 text='The subtracted part: 2 × 8 × 6 × cos 70° ='
   step5 field=pre answer=67.1661 text='So AC² = 100 − 32.8339 ='
   step6 field=pre answer=8.2 text='Square root: √67.1661 ='

gold[3] Q: 131415ABCArea = ?Diagram not drawn accurately A triangle has sides 13 cm, 14 cm and 15 cm.
   step0 field=say answer=None text='No angle is given, so find one first. Use the cosine rule for the angle A between the side'
   step1 field=pre answer=252 text='Top line: 14² + 15² − 13² = 196 + 225 − 169 ='
   step2 field=pre answer=420 text='Bottom line: 2 × 14 × 15 ='
   step3 field=pre answer=0.6 text='So cos A = 252 ÷ 420 ='
   step4 field=pre answer=53.1 text='Angle A: cos⁻¹(0.6) ='
   step5 field=pre answer=84 text='Now the area: ½ × 14 × 15 × sin 53.1° ='

### board=maths-edexcel
gold[1] Q: 7 cm9 cmc = ?120°Diagram not drawn accuratelyIn triangle ABC, \(a = 7\), \(b = 9\), \(C = 
   step0 field=say answer=None text='Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\). a = 7, b = 9, C = 120°. cos120° ='
   step1 field=pre answer=130 text='a² + b² = 49 + 81 ='
   step2 field=pre answer=-63 text='The last term, 2ab × cosC = 126 × (−0.5) ='
   step3 field=pre answer=193 text='c² = 130 − (−63) = 130 + 63 ='
   step4 field=pre answer=13.9 text='c = √193 = ? (to 1 d.p.)'

gold[3] Q: 10 cm14 cm?30°Diagram not drawn accuratelyUse the sine rule to find the two possible value
   step0 field=say answer=None text='Sine rule for an angle: sinB = b × sinA ÷ a. a = 10, b = 14, A = 30°, and sin30° = 0.5.'
   step1 field=pre answer=7 text='b × sinA = 14 × 0.5 ='
   step2 field=pre answer=0.7 text='sinB = 7 ÷ 10 ='
   step3 field=pre answer=44.4 text='The acute answer, sin⁻¹(0.7) = ? (to 1 d.p.)'
   step4 field=pre answer=135.6 text='The question wants the OBTUSE angle: 180 − 44.4 ='

### board=maths-ocr
gold[1] Q: 8913?ABCDiagram not drawn accurately Use the cosine rule to find angle \(C\): \(a = 8\), \
   step0 field=say answer=None text='Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab} = \\frac{8^2 + 9^2 - 13^2}'
   step1 field=pre answer=-24 text='Top line: 8² + 9² − 13² = 64 + 81 − 169 ='
   step2 field=pre answer=144 text='Bottom line: 2 × 8 × 9 ='
   step3 field=pre answer=-0.1667 text='So cos C = −24 ÷ 144 ='
   step4 field=pre answer=99.6 text='Angle C: cos⁻¹(−0.1667) ='

gold[3] Q: 81115Area = ?Diagram not drawn accurately A triangle has sides 8, 11 and 15. Find its area
   step0 field=say answer=None text="Heron's formula: \\(s = \\frac{a+b+c}{2}\\), then Area \\(= \\sqrt{s(s-a)(s-b)(s-c)}\\)."
   step1 field=pre answer=17 text='Half the perimeter: (8 + 11 + 15) ÷ 2 ='
   step2 field=pre answer=1836 text='The product s(s−a)(s−b)(s−c): 17 × 9 × 6 × 2 ='
   step3 field=pre answer=42.8 text='Square root: √1836 ='
   step4 field=pre answer=42.8 text='Check the units: the area to 1 d.p. is'

### board=maths-eduqas
gold[1] Q: 131415Area = ?Diagram not drawn accuratelyA triangle has sides 13 cm, 14 cm and 15 cm. Fin
   step0 field=say answer=None text='With three sides and no angle, first find the angle between 13 and 14 (opposite 15) using '
   step1 field=pre answer=140 text='Top line, 13² + 14² − 15² = 169 + 196 − 225 ='
   step2 field=pre answer=0.3846 text='cosC = 140 ÷ 364 = ? (to 4 d.p.)'
   step3 field=pre answer=67.4 text='C = cos⁻¹(0.3846) = ? (to 1 d.p.)'
   step4 field=pre answer=84 text='Now area = ½ × 13 × 14 × sin67.4° = 91 × 0.9231 = ? (nearest whole number)'

gold[3] Q: 10 cm8 cm?Area = 30 cm²Diagram not drawn accuratelyA triangle has area 30 cm² and two side
   step0 field=say answer=None text='Work backwards from the area. Area = \\(\\tfrac{1}{2}ab\\sin C\\), so sinC = 2 × Area ÷ (a × b'
   step1 field=pre answer=80 text='a × b = 10 × 8 ='
   step2 field=pre answer=0.75 text='sinC = (2 × 30) ÷ 80 = 60 ÷ 80 ='
   step3 field=pre answer=48.6 text='C = sin⁻¹(0.75) = ? (to 1 d.p.)'
