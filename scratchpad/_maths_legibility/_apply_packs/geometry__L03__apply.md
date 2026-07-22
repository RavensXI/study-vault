# apply-pack: geometry__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] silver[3] box=10 | The curved part is 2πrh = 10πh, so 100 = 10h, h = 100 ÷ 10 = [box=10, NO label] | fix: Split into two steps: "Substitute r = 5, so 2πrh = 10πh" then "So 100 = 10h, meaning h = 100 ÷ 10 = ___".
- [medium] bronze[3] | intro: That is the number in front of π: 90π. (sits before '9 × 10 = [box=90]') | fix: Move this intro to after '9 × 10 = 90', or reword: 'Multiplying by the height gives 90 — that is the number in front of π (90π).'
- [medium] bronze[6] | intro: That is the number in front of π: 112π. (sits before '16 × 7 = [box=112]' | fix: Move this intro to after '16 × 7 = 112'.
- [medium] silver[3] | intro: That is the number in front of π: 36π. (sits before '4 × 9 = [box=36]') | fix: Move this intro to after '4 × 9 = 36'.
- [medium] silver[4] | intro: That is the number in front of π: 64π. (sits after '4 × 4 = 16', before ' | fix: Move this intro to after '4 × 16 = 64'.
- [medium] gold[4] | Big cone r²h: 36 × 12 = [box=432, NO label] | fix: Add the squaring steps first: '6 × 6 = 36' (big cone) and '2 × 2 = 4' (small cone) before multiplying by the height.
- [medium] gold[0] | Divide the volume by 4π: 150 ÷ (4 × π) = [box=11.94, NO label] | fix: Add a line before this step: 'Since ⅓ × h = 4, the volume equals 4 × π × r², so r² = volume ÷ (4π).'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[3] Q: r = 3 cmh = 7 cmDiagram not drawn accurately Find the volume of a cylinder with radius 3 c
   step0 field=say answer=None text='Volume of a cylinder is \\(\\pi r^2 h\\). Square the radius first.'
   step1 field=pre answer=9 text='Square the radius: 3² ='
   step2 field=pre answer=63 text='Multiply by the height: 9 × 7 ='
   step3 field=pre answer=197.9 text='Multiply by π: 63 × π ='
   step4 field=pre answer=197.9 text='Check in one go: π × 3² × 7 rounds to'

bronze[6] Q: d = 10 cmh = 6 cmDiagram not drawn accurately A cylinder has diameter 10 cm and height 6 c
   step0 field=say answer=None text='The diameter is 10 cm, so halve it to get the radius first.'
   step1 field=pre answer=5 text='Radius = 10 ÷ 2 ='
   step2 field=pre answer=25 text='Square the radius: 5² ='
   step3 field=pre answer=150 text='Multiply by the height: 25 × 6 ='
   step4 field=pre answer=471.2 text='Multiply by π: 150 × π ='
   step5 field=pre answer=471.2 text='Check in one go: π × 5² × 6 rounds to'

gold[0] Q: r = 3 cml = 5 cmDiagram not drawn accurately A cone has radius 3 cm and slant height 5 cm.
   step0 field=say answer=None text='Total surface area of a cone is the curved part \\(\\pi r l\\) plus the base \\(\\pi r^2\\). Fin'
   step1 field=pre answer=15 text='Curved part factor: r × l = 3 × 5 ='
   step2 field=pre answer=9 text='Base factor: r² = 3² ='
   step3 field=pre answer=24 text='Add them: 15 + 9 ='
   step4 field=pre answer=75.4 text='Multiply by π: 24 × π ='
   step5 field=pre answer=75.4 text='Check: 15π + 9π = 24π rounds to'

gold[4] Q: r = ?SA = 100πDiagram not drawn accurately A sphere has surface area \(100\pi\) cm². Find 
   step0 field=say answer=None text='Surface area of a sphere is \\(4\\pi r^2\\). Set it equal to 100π and the π cancels.'
   step1 field=pre answer=100 text='Divide both sides by π: 100π ÷ π ='
   step2 field=pre answer=25 text='Divide by 4: 100 ÷ 4 ='
   step3 field=pre answer=5 text='Square root: √25 ='
   step4 field=pre answer=100 text='Check: 4 × π × 5² in π units is 4 × 25 ='

silver[3] Q: r = 5 cmh = ?Diagram not drawn accurately A cylinder has surface area 150π cm². Its radius
   step0 field=say answer=None text='Surface area of a cylinder is \\(2\\pi r^2 + 2\\pi r h\\). Work in multiples of π so it stays '
   step1 field=pre answer=50 text='The two circular ends are 2πr². In π units: 2 × 5² ='
   step2 field=pre answer=100 text='Take the ends off the total: 150 − 50 ='
   step3 field=pre answer=10 text='The curved part is 2πrh = 10πh, so 100 = 10h, h = 100 ÷ 10 ='
   step4 field=pre answer=150 text='Check: 50π + 2π(5)(10) in π units is 50 + 100 ='

silver[4] Q: 6 cmh = 10 cmDiagram not drawn accurately A pyramid has a square base of side 6 cm and hei
   step0 field=say answer=None text='Volume of a pyramid is \\(\\frac{1}{3} \\times\\) base area \\(\\times h\\). Find the base area f'
   step1 field=pre answer=36 text='Base area (square): 6 × 6 ='
   step2 field=pre answer=360 text='Multiply by the height: 36 × 10 ='
   step3 field=pre answer=120 text='Take one third: 360 ÷ 3 ='
   step4 field=pre answer=120 text='Check: ⅓ × 36 × 10 ='

### board=maths-edexcel
bronze[3] Q: 3 cm10 cmDiagram not drawn accuratelyA cylinder has radius 3 cm and height 10 cm. Find its
   step0 field=say answer=None text='Volume of a cylinder is π × r² × h. Start with r².'
   step1 field=pre answer=9 text='3 × 3 ='
   step2 field=pre answer=90 text='9 × 10 ='
   step3 field=pre answer=282.7 text='90 × π, to 1 d.p. ='
   step4 field=say answer=None text='Check: the base circle has area π × 9 ≈ 28.3 cm², and over height 10 that is about 283 cm³'

bronze[6] Q: 4 cm7 cmDiagram not drawn accuratelyA cylinder has radius 4 cm and height 7 cm. Find the v
   step0 field=say answer=None text='Volume of a cylinder is π × r² × h. Start with r².'
   step1 field=pre answer=16 text='4 × 4 ='
   step2 field=pre answer=112 text='16 × 7 ='
   step3 field=pre answer=351.9 text='112 × π, to 1 d.p. ='
   step4 field=say answer=None text='Check: base area π × 16 ≈ 50.3 cm², times height 7 ≈ 352 cm³, matching 351.9 cm³.'

gold[0] Q: r = ?V = 288π cm³Diagram not drawn accuratelyA sphere has volume \(288\pi\) cm³. Find the 
   step0 field=say answer=None text='Volume of a sphere is (4/3)πr³, and here it equals 288π. The π cancels, so (4/3)r³ = 288, '
   step1 field=pre answer=864 text='288 × 3 ='
   step2 field=pre answer=216 text='864 ÷ 4 ='
   step3 field=pre answer=6 text='The cube root: r = ∛216 ='
   step4 field=say answer=None text='Check: 6³ = 216 and (4/3) × 216 = 288, so the volume is 288π. The radius is 6 cm.'

gold[4] Q: 6 cm2 cm12 cmtip 4 cmDiagram not drawn accuratelyA frustum is formed by removing a cone of
   step0 field=say answer=None text='The frustum is the big cone minus the small cone. Volume of a cone is (1/3)πr²h. Find each'
   step1 field=pre answer=432 text='Big cone r²h: 36 × 12 ='
   step2 field=pre answer=144 text='A third: 432 ÷ 3 ='
   step3 field=pre answer=16 text='Small cone r²h: 4 × 4 ='
   step4 field=pre answer=5.33 text='A third: 16 ÷ 3, to 2 d.p. ='
   step5 field=pre answer=138.67 text='Subtract: 144 − 5.33 ='
   step6 field=pre answer=435.6 text='138.67 × π, to 1 d.p. ='
   step7 field=say answer=None text='Check: big cone 144π ≈ 452.4, small cone 5.33π ≈ 16.8; 452.4 − 16.8 ≈ 435.6 cm³.'

silver[3] Q: 4 cml = 9 cmDiagram not drawn accuratelyFind the curved surface area of a cone with radius
   step0 field=say answer=None text='Curved surface area of a cone is π × r × l. Multiply r and l first.'
   step1 field=pre answer=36 text='4 × 9 ='
   step2 field=pre answer=113.1 text='36 × π, to 1 d.p. ='
   step3 field=pre answer=36 text='Check: 113.1 ÷ π, to the nearest whole number ='

silver[4] Q: 4 cmDiagram not drawn accuratelyFind the surface area of a sphere with radius 4 cm to 1 d.
   step0 field=say answer=None text='Surface area of a sphere is 4 × π × r². Start with r².'
   step1 field=pre answer=16 text='4 × 4 ='
   step2 field=pre answer=64 text='4 × 16 ='
   step3 field=pre answer=201.1 text='64 × π, to 1 d.p. ='
   step4 field=say answer=None text='Check: 201.1 ÷ π ≈ 64, which is 4 × 16, so 201.1 cm² is right.'

### board=maths-ocr
bronze[3] Q: area 15 cm²length 8 cmDiagram not drawn accurately A prism has a cross-section area of 15 
   step0 field=say answer=None text='Volume of any prism is the cross-section area times the length.'
   step1 field=pre answer=15 text='Write the cross-section area:'
   step2 field=pre answer=120 text='Multiply by the length: 15 × 8 ='
   step3 field=pre answer=15 text='Check: 120 ÷ 8 ='

bronze[6] Q: 10 cm?6 cmDiagram not drawn accurately A cuboid has volume 180 cm³. Its length is 10 cm an
   step0 field=say answer=None text='Volume = length × width × height, so height = volume ÷ (length × width).'
   step1 field=pre answer=60 text='Multiply length by width: 10 × 6 ='
   step2 field=pre answer=3 text='Divide the volume by the base area: 180 ÷ 60 ='
   step3 field=pre answer=180 text='Check: 10 × 6 × 3 ='

gold[0] Q: h = 12 cmr = ?Diagram not drawn accurately A cone has volume 150 cm³ and height 12 cm. Fin
   step0 field=say answer=None text='Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). Put the numbers in and rearrange for r.'
   step1 field=pre answer=4 text='The ⅓ × h part: ⅓ × 12 ='
   step2 field=pre answer=11.94 text='Divide the volume by 4π: 150 ÷ (4 × π) ='
   step3 field=pre answer=3.5 text='Square root for r: √11.94 ='
   step4 field=pre answer=150 text='Check with the exact r²: ⅓ × π × 11.94 × 12 rounds to'

gold[4] Q: r = 5 cmDiagram not drawn accurately A sphere fits exactly inside a cylinder. The sphere h
   step0 field=say answer=None text='The sphere touches the cylinder all round, so the cylinder has radius 5 and height 10 (the'
   step1 field=pre answer=785.4 text='Cylinder volume: π × 5² × 10 = 250π ='
   step2 field=pre answer=523.6 text='Sphere volume: four thirds × π × 5³ = 500π ÷ 3 ='
   step3 field=pre answer=261.8 text='Subtract: 785.4 − 523.6 ='
   step4 field=pre answer=261.8 text='Check: the gap is exactly a third of the cylinder, 250π ÷ 3 rounds to'

silver[3] Q: r = 3 cmDiagram not drawn accurately A sphere has radius 3 cm. Find the volume to 1 d.p.
   step0 field=say answer=None text='Volume of a sphere is \\(\\frac{4}{3}\\pi r^3\\). Cube the radius first.'
   step1 field=pre answer=27 text='Cube the radius: 3³ ='
   step2 field=pre answer=108 text='Multiply by 4: 27 × 4 ='
   step3 field=pre answer=36 text='Divide by 3: 108 ÷ 3 ='
   step4 field=pre answer=113.1 text='Multiply by π: 36 × π ='
   step5 field=pre answer=113.1 text='Check: four thirds × π × 27 rounds to'

silver[4] Q: r = 5 cmDiagram not drawn accurately A hemisphere has radius 5 cm. Find the volume to 1 d.
   step0 field=say answer=None text="A hemisphere is half a sphere. Find the full sphere's volume, then halve it."
   step1 field=pre answer=125 text='Cube the radius: 5³ ='
   step2 field=pre answer=523.6 text='Sphere volume: four thirds × π × 125 ='
   step3 field=pre answer=261.8 text='Halve it for a hemisphere: 523.6 ÷ 2 ='
   step4 field=pre answer=261.8 text='Check: two thirds × π × 125 rounds to'

### board=maths-eduqas
bronze[3] Q: 4 cmDiagram not drawn accurately Find the surface area of a cube with side length 4 cm.
   step0 field=say answer=None text='A cube has 6 identical square faces. Find one face, then multiply by 6.'
   step1 field=pre answer=16 text='Area of one face: 4 × 4 ='
   step2 field=pre answer=96 text='Six faces: 6 × 16 ='
   step3 field=pre answer=64 text='Compare: the volume would be 4 × 4 × 4 ='

bronze[6] Q: V = 27 cm³?Diagram not drawn accurately A cube has volume 27 cm³. Find the side length.
   step0 field=say answer=None text='Volume of a cube is side³, so we need the number whose cube is 27.'
   step1 field=pre answer=9 text='Try a side of 3. First 3 × 3 ='
   step2 field=pre answer=27 text='Now multiply by 3 again: 9 × 3 ='
   step3 field=pre answer=3 text='So the side length is'

gold[0] Q: r = 9 cmDiagram not drawn accurately Find the volume of a sphere with radius 9 cm. Give yo
   step0 field=say answer=None text='Volume of a sphere is \\(\\frac{4}{3}\\pi r^3\\). Cube the radius first.'
   step1 field=pre answer=729 text='Cube the radius: 9³ ='
   step2 field=pre answer=2916 text='Multiply by 4: 729 × 4 ='
   step3 field=pre answer=972 text='Divide by 3: 2916 ÷ 3 ='
   step4 field=pre answer=3054 text='Multiply by π and round: 972 × π ='
   step5 field=pre answer=3054 text='Check in one go: \\(\\frac{4}{3}\\) × π × 729 rounds to'

gold[4] Q: r = 3 cmh = 10 cmDiagram not drawn accurately A solid is a cylinder (radius 3 cm, height 1
   step0 field=say answer=None text='Total volume = cylinder + hemisphere on top. Work each in π units, then add.'
   step1 field=pre answer=90 text='Cylinder factor: r²h = 3² × 10 ='
   step2 field=pre answer=18 text='Hemisphere factor: \\(\\frac{2}{3}\\) × 3³ = \\(\\frac{2}{3}\\) × 27 ='
   step3 field=pre answer=108 text='Add them: 90 + 18 ='
   step4 field=pre answer=339.3 text='Multiply by π: 108 × π ='

silver[3] Q: r = 3 cmh = 10 cmDiagram not drawn accurately Find the total surface area of a cylinder wi
   step0 field=say answer=None text='Surface area of a cylinder is \\(2\\pi r^2 + 2\\pi r h\\). Work in multiples of π, then multip'
   step1 field=pre answer=18 text='The two ends, 2πr², in π units: 2 × 3² ='
   step2 field=pre answer=60 text='The curved part, 2πrh, in π units: 2 × 3 × 10 ='
   step3 field=pre answer=78 text='Add them: 18 + 60 ='
   step4 field=pre answer=245.0 text='Multiply by π: 78 × π ='

silver[4] Q: r = 10 cmh = ?Diagram not drawn accurately A cylinder has volume \(500\pi\) cm³ and radius
   step0 field=say answer=None text='Volume of a cylinder is \\(\\pi r^2 h\\). Work in π units so the π cancels.'
   step1 field=pre answer=100 text='Square the radius: 10² ='
   step2 field=pre answer=5 text='So 100 × h = 500 (in π units). Divide: 500 ÷ 100 ='
   step3 field=pre answer=500 text='Check: π × 10² × 5 in π units is 100 × 5 ='
