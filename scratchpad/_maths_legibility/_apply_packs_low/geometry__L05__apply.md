# apply-pack: geometry__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[0] | sin40°, to 2 d.p. = [box=0.64, NO label] | fix: Reword to 'Use your calculator (in degrees mode): sin40°, to 2 d.p. ='.
- [low] bronze[6] | sin30° = 0.5, and the opposite is the hypotenuse times this. First write the hyp | fix: Split into two: 'sin30° = 0.5, so opposite = hypotenuse × 0.5.' then a simple 'Write down the hypotenuse:' with the box. Apply to bronze[7] too.
- [low] gold[0] | intro: The angle of depression from the top equals the angle of elevation at the | fix: Break into 2–3 short sentences, one idea each.
- [low] gold[1] | √64 = [box=8, NO label] | fix: Reword to 'Square root to get the height: √64 ='.
- [low] bronze[5] | Q: Which trig ratio uses opposite and hypotenuse? | fix: Either sequence this after a SOHCAHTOA walk, or add a one-line reminder (e.g. 'SOH: sine = opposite ÷ hypotenuse') so the ratio names are introduced before they

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[5] Q: 7 cm24 cm? cmDiagram not drawn accuratelyA right triangle has sides 7 cm and 24 cm. Find t
   step0 field=pre answer=49 text='7² ='
   step1 field=pre answer=576 text='24² ='
   step2 field=pre answer=625 text='Add the squares: 49 + 576 ='
   step3 field=pre answer=25 text='Square root to get the hypotenuse: √625 ='
   step4 field=pre answer=625 text='Check: 25² ='

bronze[6] Q: 30°?18 cmDiagram not drawn accuratelyUsing \(\sin 30° = 0.5\), find the opposite side in a
   step0 field=pre answer=18 text='sin30° = 0.5, and the opposite is the hypotenuse times this. First write the hypotenuse:'
   step1 field=pre answer=9 text='O = 18 × 0.5 ='
   step2 field=pre answer=0.5 text='Check: O ÷ H = 9 ÷ 18 ='

gold[0] Q: 35°25 m? m⛵Diagram not drawn accuratelyFrom the top of a 25 m cliff, the angle of depressi
   step0 field=say answer=None text='The angle of depression from the top equals the angle of elevation at the boat, 35°. The h'
   step1 field=pre answer=0.7 text='tan35°, to 3 d.p. ='
   step2 field=pre answer=35.7 text='d = 25 ÷ tan35° ='
   step3 field=pre answer=25 text='Check: 35.7 × tan35°, to the nearest whole number ='

gold[1] Q: 10 cm10 cm12 cm?Diagram not drawn accuratelyAn isosceles triangle has equal sides 10 cm an
   step0 field=pre answer=6 text='Half the base: 12 ÷ 2 ='
   step1 field=pre answer=100 text='The equal side is the hypotenuse: 10² ='
   step2 field=pre answer=36 text='6² ='
   step3 field=pre answer=64 text='Subtract: 100 − 36 ='
   step4 field=pre answer=8 text='√64 ='
   step5 field=pre answer=100 text='Check: 8² + 6² ='

silver[0] Q: 40°?15 cmDiagram not drawn accuratelyFind the opposite side when the hypotenuse is 15 cm a
   step0 field=pre answer=0.64 text='sin40°, to 2 d.p. ='
   step1 field=pre answer=9.6 text='O = 15 × sin40° ='
   step2 field=pre answer=0.64 text='Check: O ÷ H = 9.6 ÷ 15, to 2 d.p. ='

### board=maths-edexcel
bronze[5] Q: 30°?20 cmDiagram not drawn accurately\(\sin 30° = 0.5\). The hypotenuse is 20 cm. Find the
   step0 field=pre answer=20 text='sin30° = 0.5, and the opposite is the hypotenuse times this. First write the hypotenuse:'
   step1 field=pre answer=10 text='O = 20 × 0.5 ='
   step2 field=pre answer=0.5 text='Check: O ÷ H = 10 ÷ 20 ='

bronze[6] Q: 60°?14 cmDiagram not drawn accurately\(\cos 60° = 0.5\). The hypotenuse is 14 cm. Find the
   step0 field=pre answer=14 text='cos60° = 0.5, and the adjacent is the hypotenuse times this. First write the hypotenuse:'
   step1 field=pre answer=7 text='A = 14 × 0.5 ='
   step2 field=pre answer=0.5 text='Check: A ÷ H = 7 ÷ 14 ='

gold[0] Q: 15 km20 km? kmDiagram not drawn accuratelyA ship sails 15 km east then 20 km north. Find t
   step0 field=pre answer=225 text='East leg squared: 15² ='
   step1 field=pre answer=400 text='North leg squared: 20² ='
   step2 field=pre answer=625 text='Add: 225 + 400 ='
   step3 field=pre answer=25 text='√625 ='
   step4 field=pre answer=625 text='Check: 25² ='

gold[1] Q: θ50 m30 mDiagram not drawn accuratelyFind the angle of elevation from a point 50 m from a 
   step0 field=pre answer=0.6 text='Opposite (height) over adjacent (distance): 30 ÷ 50 ='
   step1 field=pre answer=31.0 text='θ = tan⁻¹(0.6) ='
   step2 field=pre answer=0.6 text='Check: tan31°, to 1 d.p. ='

silver[0] Q: b = 5a = ?c = 13Diagram not drawn accuratelyFind the length of side \(a\) in a right trian
   step0 field=pre answer=169 text='13² ='
   step1 field=pre answer=25 text='5² ='
   step2 field=pre answer=144 text='c is the hypotenuse, so subtract: 169 − 25 ='
   step3 field=pre answer=12 text='√144 ='
   step4 field=pre answer=169 text='Check: 12² + 5² ='

### board=maths-ocr
bronze[5] Q: Which trig ratio uses opposite and hypotenuse?

bronze[6] Q: 15 cm8 cm?Diagram not drawn accuratelyPythagoras: legs 8 and 15. Find the hypotenuse.
   step0 field=say answer=None text='Two shorter sides, no angle: Pythagoras. Square each, add, then square root.'
   step1 field=pre answer=64 text='8² ='
   step2 field=pre answer=225 text='15² ='
   step3 field=pre answer=289 text='Add the squares: 64 + 225 ='
   step4 field=pre answer=17 text='Square root to get the hypotenuse: √289 ='
   step5 field=pre answer=289 text='Check: 17² ='

gold[0] Q: 8 cm6 cm?Diagram not drawn accuratelyA rectangle is 8 cm by 6 cm. Find the diagonal length
   step0 field=say answer=None text="A rectangle's diagonal splits it into two right triangles with legs 8 and 6. The diagonal "
   step1 field=pre answer=64 text='8² ='
   step2 field=pre answer=36 text='6² ='
   step3 field=pre answer=100 text='Add: 64 + 36 ='
   step4 field=pre answer=10 text='√100 ='
   step5 field=pre answer=100 text='Check: 10² ='

gold[1] Q: 10 cm10 cm12 cm?Diagram not drawn accuratelyAn isosceles triangle has equal sides 10 cm an
   step0 field=say answer=None text='The height drops to the middle of the base, splitting it into two equal halves and making '
   step1 field=pre answer=6 text='Half the base: 12 ÷ 2 ='
   step2 field=pre answer=100 text='The equal side is the hypotenuse: 10² ='
   step3 field=pre answer=36 text='6² ='
   step4 field=pre answer=64 text='Subtract: 100 − 36 ='
   step5 field=pre answer=8 text='√64 ='
   step6 field=pre answer=100 text='Check: 8² + 6² ='

silver[0] Q: θ = ?12 cm5 cmDiagram not drawn accuratelyFind angle θ: opposite = 5, adjacent = 12. To 1 
   step0 field=say answer=None text='You have the opposite (5) and the adjacent (12). Opposite over adjacent is tan, so use inv'
   step1 field=pre answer=0.42 text='The ratio, opposite ÷ adjacent: 5 ÷ 12, to 2 d.p. ='
   step2 field=pre answer=22.6 text='θ = tan⁻¹(5 ÷ 12) ='
   step3 field=pre answer=0.42 text='Check: tan22.6°, to 2 d.p. ='

### board=maths-eduqas
bronze[5] Q: 91215Diagram not drawn accuratelyIs a triangle with sides 9, 12, 15 right-angled?

bronze[6] Q: 940xDiagram not drawn accuratelyFind \(x\): hypotenuse \(x\), shorter sides 9 and 40.
   step0 field=pre answer=81 text='9² ='
   step1 field=pre answer=1600 text='40² ='
   step2 field=pre answer=1681 text='Add the squares: 81 + 1600 ='
   step3 field=pre answer=41 text='√1681 ='
   step4 field=pre answer=1681 text='Check: 41² ='

gold[0] Q: 1.5 m? m5 mDiagram not drawn accuratelyA ladder 5 m long leans against a wall. Its foot is
   step0 field=pre answer=25 text='5² ='
   step1 field=pre answer=2.25 text='1.5² ='
   step2 field=pre answer=22.75 text='The ladder is the hypotenuse, so subtract: 25 − 2.25 ='
   step3 field=pre answer=4.8 text='√22.75, to 1 d.p. ='
   step4 field=pre answer=22.75 text='Check: 5² − 1.5² ='

gold[1] Q: 10 cm10 cm12 cm?Diagram not drawn accuratelyAn isosceles triangle has equal sides 10 cm an
   step0 field=pre answer=6 text='Half the base: 12 ÷ 2 ='
   step1 field=pre answer=100 text='The slant side is the hypotenuse: 10² ='
   step2 field=pre answer=36 text='6² ='
   step3 field=pre answer=64 text='Subtract: 100 − 36 ='
   step4 field=pre answer=8 text='√64 ='
   step5 field=pre answer=100 text='Check: 8² + 6² ='

silver[0] Q: \(\sin\theta = 0.6\). Find \(\theta\) to 1 d.p.
   step0 field=say answer=None text='sin θ = 0.6 is the ratio opposite ÷ hypotenuse. To get the angle back, use inverse sin.'
   step1 field=pre answer=36.87 text='sin⁻¹(0.6), to 2 d.p. ='
   step2 field=pre answer=36.9 text='Round to 1 d.p.: θ ='
   step3 field=pre answer=0.6 text='Check by going forward: sin36.9°, to 1 d.p. ='
