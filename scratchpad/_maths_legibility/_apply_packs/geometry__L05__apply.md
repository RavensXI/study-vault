# apply-pack: geometry__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[2] | Add all three: 9 + 16 + 144 = [box=169, NO label] | fix: Add an intro like gold[0]'s: 'A cuboid's diagonal uses all three edges — d = √(l²+w²+h²) — so square all three lengths, add them, then square-root.'
- [medium] silver[2] | θ = sin⁻¹(0.7) = [box=44.4, NO label] (and silver[3] tan⁻¹) | fix: Add a line before the step: 'To find the angle, use inverse sine — the sin⁻¹ (2nd-Function sin) button.' Do the same for tan⁻¹ in silver[3].
- [medium] gold[2] | intro: So the equation is x² + (x² + 2x + 1) = x² + 4x + 4. On the left, x² + x² | fix: Insert a step before the assembly stating the setup explicitly: 'By Pythagoras: x² + (x+1)² = (x+2)²', then expand.
- [medium] silver[1] | O = 15 × sin40° = [box=9.6, NO label] | fix: Add a one-line intro deriving the rearrangement, e.g. "sin40° = opposite ÷ hypotenuse, which rearranges to opposite = hypotenuse × sin40°." Apply the same to si
- [medium] gold[4] | intro: "...At the finish, the angle between due south and the path back has tan  | fix: Split into short sentences, e.g. "To get home the ship must go 12 km west and 9 km south. That makes a right triangle. The angle measured from due south is tan⁻

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: 4 cm3 cm12 cm?Diagram not drawn accuratelyFind the diagonal of a cuboid with dimensions 3 
   step0 field=pre answer=9 text='3² ='
   step1 field=pre answer=16 text='4² ='
   step2 field=pre answer=144 text='12² ='
   step3 field=pre answer=169 text='Add all three: 9 + 16 + 144 ='
   step4 field=pre answer=13 text='√169 ='
   step5 field=pre answer=169 text='Check: 13² ='

gold[4] Q: 120 m50 mpathDiagram not drawn accuratelyA triangular field has a right angle. The two sho
   step0 field=pre answer=2500 text='50² ='
   step1 field=pre answer=14400 text='120² ='
   step2 field=pre answer=16900 text='Add the squares: 2500 + 14400 ='
   step3 field=pre answer=130 text='√16900 ='
   step4 field=pre answer=170 text='Both sides together: 50 + 120 ='
   step5 field=pre answer=40 text='How much shorter the diagonal is: 170 − 130 ='
   step6 field=pre answer=170 text='Check: 130 + 40 ='

silver[1] Q: 55°?12 cmDiagram not drawn accuratelyFind the adjacent side when the hypotenuse is 12 cm a
   step0 field=pre answer=0.57 text='cos55°, to 2 d.p. ='
   step1 field=pre answer=6.9 text='A = 12 × cos55° ='
   step2 field=pre answer=0.6 text='Check: A ÷ H = 6.9 ÷ 12, to 1 d.p. ='

silver[2] Q: θ7 cm10 cmDiagram not drawn accuratelyFind the angle when the opposite side is 7 cm and th
   step0 field=pre answer=0.7 text='Opposite over hypotenuse: 7 ÷ 10 ='
   step1 field=pre answer=44.4 text='θ = sin⁻¹(0.7) ='
   step2 field=pre answer=0.7 text='Check: sin44.4°, to 2 d.p. ='

### board=maths-edexcel
gold[2] Q: xx + 1x + 2Diagram not drawn accuratelyA right-angled triangle has shorter sides \(x\) and
   step0 field=pre answer=2 text='Expand (x + 1)² = x² + ?x + 1. The middle number (2 × 1) is'
   step1 field=pre answer=4 text='Expand (x + 2)² = x² + ?x + 4. The middle number (2 × 2) is'
   step2 field=say answer=None text='So the equation is x² + (x² + 2x + 1) = x² + 4x + 4. On the left, x² + x² = 2x²; take x² f'
   step3 field=pre answer=-2 text='The x term: left has 2x, right has 4x. 2 − 4 ='
   step4 field=pre answer=-3 text='The constant: left has 1, right has 4. 1 − 4 ='
   step5 field=pre answer=3 text='That gives x² − 2x − 3 = 0, which factorises as (x − 3)(x + 1) = 0. The positive length is'
   step6 field=pre answer=25 text='Check the sides 3, 4, 5: 3² + 4² ='

gold[4] Q: 8 cm? cm17 cmDiagram not drawn accuratelyA rectangle has diagonal 17 cm and width 8 cm. Fi
   step0 field=pre answer=289 text='The diagonal is the hypotenuse: 17² ='
   step1 field=pre answer=64 text='8² ='
   step2 field=pre answer=225 text='Subtract: 289 − 64 ='
   step3 field=pre answer=15 text='√225 ='
   step4 field=pre answer=289 text='Check: 15² + 8² ='

silver[1] Q: θ6 cm8 cmDiagram not drawn accuratelyThe opposite side is 8 cm and the adjacent side is 6 
   step0 field=pre answer=1.33 text='Opposite over adjacent: 8 ÷ 6, to 2 d.p. ='
   step1 field=pre answer=53.1 text='θ = tan⁻¹(8 ÷ 6) ='
   step2 field=pre answer=1.33 text='Check: tan53.1°, to 2 d.p. ='

silver[2] Q: 40°?12 cmDiagram not drawn accuratelyFind the adjacent side when \(\theta = 40°\) and hypo
   step0 field=pre answer=0.77 text='cos40°, to 2 d.p. ='
   step1 field=pre answer=9.2 text='A = 12 × cos40° ='
   step2 field=pre answer=0.77 text='Check: A ÷ H = 9.2 ÷ 12, to 2 d.p. ='

### board=maths-ocr
gold[2] Q: 4123?Diagram not drawn accuratelyPythagoras in 3D: cuboid 3×4×12. Find the space diagonal.
   step0 field=say answer=None text='The space diagonal of a cuboid uses all three edges: d = √(length² + width² + height²).'
   step1 field=pre answer=9 text='3² ='
   step2 field=pre answer=16 text='4² ='
   step3 field=pre answer=144 text='12² ='
   step4 field=pre answer=169 text='Add all three: 9 + 16 + 144 ='
   step5 field=pre answer=13 text='√169 ='
   step6 field=pre answer=169 text='Check: 13² ='

gold[4] Q: 32°50 m?Diagram not drawn accuratelyAngle of elevation from 50 m away to the top of a tree
   step0 field=say answer=None text='The tree height is opposite the 32° angle and the 50 m distance is adjacent. Opposite over'
   step1 field=pre answer=0.62 text='tan32°, to 2 d.p. ='
   step2 field=pre answer=31.2 text='h = 50 × tan32° ='
   step3 field=pre answer=0.62 text='Check: h ÷ 50 = 31.2 ÷ 50, to 2 d.p. ='

silver[1] Q: 40°10 cm?Diagram not drawn accuratelyFind the opposite: angle 40°, adjacent = 10 cm. To 1 
   step0 field=say answer=None text='You know the adjacent (10) and want the opposite, with the angle 40°. Opposite over adjace'
   step1 field=pre answer=0.84 text='tan40°, to 2 d.p. ='
   step2 field=pre answer=8.4 text='O = 10 × tan40° ='
   step3 field=pre answer=0.84 text='Check: O ÷ 10 = 8.4 ÷ 10 ='

silver[2] Q: 30°7 cm?Diagram not drawn accuratelyFind the hypotenuse: angle 30°, opposite = 7. To 1 d.p
   step0 field=say answer=None text='You know the opposite (7) and want the hypotenuse, with angle 30°. sin30° = opposite ÷ hyp'
   step1 field=pre answer=0.5 text='sin30° ='
   step2 field=pre answer=14 text='H = 7 ÷ 0.5 ='
   step3 field=pre answer=0.5 text='Check: opposite ÷ hypotenuse = 7 ÷ 14 ='

### board=maths-eduqas
gold[2] Q: 25°40 m? m⛵Diagram not drawn accuratelyFrom the top of a 40 m cliff, the angle of depressi
   step0 field=say answer=None text='The angle of depression from the top equals the angle of elevation at the boat, 25°. The h'
   step1 field=pre answer=0.466 text='tan25°, to 3 d.p. ='
   step2 field=pre answer=86 text='d = 40 ÷ tan25°, to the nearest metre ='
   step3 field=pre answer=40 text='Check: 86 × tan25°, to the nearest metre ='

gold[4] Q: N12 km east9 km northreturnDiagram not drawn accuratelyA ship sails 12 km east then 9 km n
   step0 field=say answer=None text='The trip out went 12 km east then 9 km north. To return, the ship heads back into the sout'
   step1 field=pre answer=1.33 text='12 ÷ 9, to 2 d.p. ='
   step2 field=pre answer=53 text='That angle, tan⁻¹(12 ÷ 9), to the nearest degree ='
   step3 field=pre answer=233 text='Bearings run clockwise from north; the south-west return is 180 + 53 ='
   step4 field=pre answer=53 text='Check: a return bearing is 180° from the outward one, so 233 − 180 ='

silver[1] Q: 40°?15 cmDiagram not drawn accuratelyFind the opposite side: angle \(40^\circ\), hypotenus
   step0 field=pre answer=0.64 text='sin40°, to 2 d.p. ='
   step1 field=pre answer=9.6 text='O = 15 × sin40° ='
   step2 field=pre answer=40 text='Check: sin⁻¹(9.6 ÷ 15), to the nearest degree ='

silver[2] Q: 55°?20 cmDiagram not drawn accuratelyFind the adjacent side: angle \(55^\circ\), hypotenus
   step0 field=pre answer=0.57 text='cos55°, to 2 d.p. ='
   step1 field=pre answer=11.5 text='A = 20 × cos55° ='
   step2 field=pre answer=55 text='Check: cos⁻¹(11.5 ÷ 20), to the nearest degree ='
