# apply-pack: geometry__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] box=636.7 (check step) | Check in π units: 160 + 128/3 = 608/3, and 608π/3 rounds to [box=636.7, NO label | fix: Simplify to a decimal check, e.g. "160 + 42.7 = 202.7, then × π ≈ 636.7", or drop the fraction form entirely.
- [low] gold[3] | Check: 4 × 5² = 4 × [box=25, NO label] | fix: Complete it: 'Check: 5 × 5 = [25], then 4 × 25 = 100, giving 100π.'
- [low] silver[2] | intro: That is the whole base-times-π amount. (sits after '5 × 5 = 25', before ' | fix: Reword: 'That is r² — multiply by π next to get the base area.'
- [low] bronze[5] | Check the half first: 15 + 10 + 6 = [box=31, NO label] | fix: Reword, e.g. 'Check the inner total before doubling: 15 + 10 + 6 ='.
- [low] silver[5] | Full sphere factor: 216 × 4 ÷ 3 = [box=288, NO label] | fix: State the sphere volume formula (4/3)πr³ in the intro before asking for the 'full sphere factor'.
- [low] gold[2] | Cube root: ∛64 = [box=4, NO label] | fix: Gloss it, e.g. 'Cube root (the number whose cube is 64): ∛64 =', or introduce the symbol earlier.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[5] Q: 4 cmDiagram not drawn accurately Find the volume of a cube with side length 4 cm.
   step0 field=say answer=None text='Volume of a cube is side × side × side.'
   step1 field=pre answer=16 text='Square the side: 4 × 4 ='
   step2 field=pre answer=64 text='Multiply by the side again: 16 × 4 ='
   step3 field=pre answer=96 text='Compare: the surface area would be 6 × 16 ='

gold[2] Q: r = 5 cmDiagram not drawn accurately A sphere fits exactly inside a cylinder. The sphere h
   step0 field=say answer=None text='The sphere touches the cylinder all round, so the cylinder has radius 5 and height 10 (the'
   step1 field=pre answer=785.4 text='Cylinder volume: π × 5² × 10 = 250π ='
   step2 field=pre answer=523.6 text='Sphere volume: \\(\\frac{4}{3}\\) × π × 5³ = \\(\\frac{500\\pi}{3}\\) ='
   step3 field=pre answer=261.8 text='Subtract: 785.4 − 523.6 ='
   step4 field=pre answer=261.8 text='Check: the gap is exactly a third of the cylinder, \\(\\frac{250\\pi}{3}\\) rounds to'

gold[3] Q: r = 4 cmh = 10 cmDiagram not drawn accurately A solid is a cylinder (r=4 cm, h=10 cm) with
   step0 field=say answer=None text='Total volume = cylinder + hemisphere on top. Work each out as a decimal, then add.'
   step1 field=pre answer=502.7 text='Cylinder volume: π × 4² × 10 = 160π ='
   step2 field=pre answer=134.0 text='Hemisphere volume: ½ × \\(\\frac{4}{3}\\) × π × 4³ = \\(\\frac{128\\pi}{3}\\) ='
   step3 field=pre answer=636.7 text='Add them: 502.7 + 134.0 ='
   step4 field=pre answer=636.7 text='Check in π units: 160 + \\(\\frac{128}{3}\\) = \\(\\frac{608}{3}\\), and \\(\\frac{608\\pi}{3}\\) ro'

silver[2] Q: r = 4 cmDiagram not drawn accurately A sphere has radius 4 cm. Find the surface area to 1 
   step0 field=say answer=None text='Surface area of a sphere is \\(4\\pi r^2\\). Square the radius first.'
   step1 field=pre answer=16 text='Square the radius: 4² ='
   step2 field=pre answer=64 text='Multiply by 4: 16 × 4 ='
   step3 field=pre answer=201.1 text='Multiply by π: 64 × π ='
   step4 field=pre answer=201.1 text='Check in one go: 4 × π × 4² rounds to'

silver[5] Q: r = 9 cmDiagram not drawn accurately A hemisphere has radius 9 cm. Find its volume to 1 d.
   step0 field=say answer=None text="A hemisphere is half a sphere. Find the full sphere's volume, then halve it."
   step1 field=pre answer=729 text='Cube the radius: 9³ ='
   step2 field=pre answer=972 text='Full sphere factor: 729 × 4 ÷ 3 ='
   step3 field=pre answer=486 text='Halve it for a hemisphere: 972 ÷ 2 ='
   step4 field=pre answer=1526.8 text='Multiply by π: 486 × π ='
   step5 field=pre answer=1526.8 text='Check in one go: \\(\\frac{2}{3}\\) × π × 729 rounds to'

### board=maths-edexcel
bronze[5] Q: 8 cm2 cm3 cmDiagram not drawn accuratelyA cuboid is 8 cm × 3 cm × 2 cm. Find its surface a
   step0 field=say answer=None text='A cuboid has three different face sizes, each appearing twice. Find the three areas.'
   step1 field=pre answer=24 text='8 × 3 ='
   step2 field=pre answer=16 text='8 × 2 ='
   step3 field=pre answer=6 text='3 × 2 ='
   step4 field=pre answer=46 text='Add the three: 24 + 16 + 6 ='
   step5 field=pre answer=92 text='Each appears twice: 2 × 46 ='

gold[2] Q: 4 cm10 cmhemisphere r = 4 cmDiagram not drawn accuratelyA solid hemisphere of radius 4 cm 
   step0 field=say answer=None text='Add two volumes. Cylinder = πr²h; hemisphere = (2/3)πr³. Find each number in front of π.'
   step1 field=pre answer=160 text='Cylinder: 4 × 4 × 10 ='
   step2 field=pre answer=64 text='Hemisphere: r³ = 4 × 4 × 4 ='
   step3 field=pre answer=42.67 text='(2/3) × 64, to 2 d.p. ='
   step4 field=pre answer=202.67 text='Add the two: 160 + 42.67 ='
   step5 field=pre answer=636.7 text='202.67 × π, to 1 d.p. ='
   step6 field=say answer=None text='Check: 160π ≈ 502.7 and 42.67π ≈ 134.0; 502.7 + 134.0 ≈ 636.7 cm³.'

gold[3] Q: r = ?SA = 100π cm²Diagram not drawn accuratelyA sphere has surface area \(100\pi\) cm². Fi
   step0 field=say answer=None text='Surface area of a sphere is 4πr², and here it equals 100π. The π cancels, so 4r² = 100, gi'
   step1 field=pre answer=25 text='100 ÷ 4 ='
   step2 field=pre answer=5 text='The square root: r = √25 ='
   step3 field=pre answer=25 text='Check: 4 × 5² = 4 ×'

silver[2] Q: 5 cmh = ?V = 500 cm³Diagram not drawn accuratelyA cylinder has volume 500 cm³ and radius 5
   step0 field=say answer=None text='V = π × r² × h, so rearrange to h = V ÷ (π × r²). First find π × r².'
   step1 field=pre answer=25 text='5 × 5 ='
   step2 field=pre answer=78.54 text='π × 25, to 2 d.p. ='
   step3 field=pre answer=6.4 text='h = 500 ÷ 78.54, to 1 d.p. ='
   step4 field=say answer=None text='Check: π × 25 × 6.366 = 500 exactly; rounding the height to 6.4 explains the tiny gap, so '

silver[5] Q: 10 cm6 cmDiagram not drawn accuratelyA pyramid has square base 6 cm × 6 cm and height 10 c
   step0 field=say answer=None text='Volume of a pyramid is (1/3) × base area × height. Find the base area first.'
   step1 field=pre answer=36 text='6 × 6 ='
   step2 field=pre answer=360 text='36 × 10 ='
   step3 field=pre answer=120 text='Take a third: 360 ÷ 3 ='
   step4 field=pre answer=360 text='Check: 120 × 3 ='

### board=maths-ocr
bronze[5] Q: 5 cm2 cm3 cmDiagram not drawn accurately Find the surface area of a cuboid 5 cm × 3 cm × 2
   step0 field=say answer=None text='Surface area of a cuboid is 2(lw + lh + wh). Find the three different faces first.'
   step1 field=pre answer=15 text='Top and bottom face: 5 × 3 ='
   step2 field=pre answer=10 text='Front and back face: 5 × 2 ='
   step3 field=pre answer=6 text='Side face: 3 × 2 ='
   step4 field=pre answer=62 text='Add the three and double: 2 × (15 + 10 + 6) ='
   step5 field=pre answer=31 text='Check the half first: 15 + 10 + 6 ='

gold[2] Q: A cylinder and a cone have the same radius and height (r = 3 cm, h = 9 cm). How many times
   step0 field=say answer=None text='Volume of a cylinder is \\(\\pi r^2 h\\); volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). Use r'
   step1 field=pre answer=81 text='Cylinder in π units: 3² × 9 ='
   step2 field=pre answer=27 text='Cone in π units: ⅓ × 3² × 9 = ⅓ × 81 ='
   step3 field=pre answer=3 text='How many times bigger: 81 ÷ 27 ='
   step4 field=pre answer=3 text='Check: a cone is always ⅓ of the matching cylinder, so the cylinder is 3 × the cone, givin'

gold[3] Q: r = 6r = 3h = 126Diagram not drawn accurately A frustum is made by cutting a cone (radius 
   step0 field=say answer=None text='The frustum is the big cone with the small top cone removed. Cutting at half height also h'
   step1 field=pre answer=144 text='Big cone in π units: ⅓ × 6² × 12 = ⅓ × 432 ='
   step2 field=pre answer=18 text='Small cone in π units: ⅓ × 3² × 6 = ⅓ × 54 ='
   step3 field=pre answer=396 text='Subtract, then multiply by π: (144 − 18) × π ='
   step4 field=pre answer=396 text='Check: 126 × π rounds to'

silver[2] Q: h = 9 cmr = 4 cmDiagram not drawn accurately A cone has radius 4 cm and height 9 cm. Find 
   step0 field=say answer=None text='Volume of a cone is \\(\\frac{1}{3}\\pi r^2 h\\). Build the \\(\\pi r^2 h\\) part, then take a th'
   step1 field=pre answer=16 text='Square the radius: 4² ='
   step2 field=pre answer=144 text='Multiply by the height: 16 × 9 ='
   step3 field=pre answer=48 text='Take one third: 144 ÷ 3 ='
   step4 field=pre answer=150.8 text='Multiply by π: 48 × π ='
   step5 field=pre answer=150.8 text='Check: ⅓ × π × 16 × 9 rounds to'

silver[5] Q: 6 cmh = 10 cmDiagram not drawn accurately A pyramid has a square base of side 6 cm and hei
   step0 field=say answer=None text='Volume of a pyramid is \\(\\frac{1}{3} \\times\\) base area \\(\\times h\\). Find the base area f'
   step1 field=pre answer=36 text='Base area (square): 6 × 6 ='
   step2 field=pre answer=360 text='Multiply by the height: 36 × 10 ='
   step3 field=pre answer=120 text='Take one third: 360 ÷ 3 ='
   step4 field=pre answer=120 text='Check: ⅓ × 36 × 10 ='

### board=maths-eduqas
bronze[5] Q: 15 cm3 cm6 cmDiagram not drawn accurately A prism has a rectangular cross-section 6 cm by 
   step0 field=say answer=None text='Volume of a prism is the cross-section area times the length. The cross-section here is a '
   step1 field=pre answer=18 text='Cross-section area: 6 × 3 ='
   step2 field=pre answer=270 text='Multiply by the length: 18 × 15 ='
   step3 field=pre answer=18 text='Check: 270 ÷ 15 ='

gold[2] Q: r = ?V = (256/3)πDiagram not drawn accurately A sphere has volume \(\frac{256}{3}\pi\) cm³
   step0 field=say answer=None text='Volume of a sphere is \\(\\frac{4}{3}\\pi r^3\\). Set \\(\\frac{4}{3}r^3 = \\frac{256}{3}\\) in π '
   step1 field=pre answer=256 text='Multiply both sides by 3: \\(\\frac{256}{3}\\) × 3 gives 4r³ ='
   step2 field=pre answer=64 text='Divide by 4: 256 ÷ 4 ='
   step3 field=pre answer=4 text='Cube root: ∛64 ='
   step4 field=pre answer=85.3 text='Check: \\(\\frac{4}{3}\\) × 4³ in π units is \\(\\frac{4}{3}\\) × 64 ='

gold[3] Q: cylinderconer = 5, h = 12Diagram not drawn accurately A cone and a cylinder both have radi
   step0 field=say answer=None text='The cone is \\(\\frac{1}{3}\\) of the cylinder, so the difference is \\(\\frac{2}{3}\\) of the c'
   step1 field=pre answer=300 text='Cylinder factor: r²h = 5² × 12 ='
   step2 field=pre answer=100 text='Cone is a third: 300 ÷ 3 ='
   step3 field=pre answer=200 text='Difference: 300 − 100 ='
   step4 field=pre answer=628.3 text='Multiply by π: 200 × π ='

silver[2] Q: 6 cmh = 8 cmDiagram not drawn accurately A pyramid has a square base of side 6 cm and heig
   step0 field=say answer=None text='Volume of a pyramid is \\(\\frac{1}{3} \\times\\) base area \\(\\times h\\). Find the base area f'
   step1 field=pre answer=36 text='Base area (square): 6 × 6 ='
   step2 field=pre answer=288 text='Multiply by the height: 36 × 8 ='
   step3 field=pre answer=96 text='Take one third: 288 ÷ 3 ='
   step4 field=pre answer=96 text='Check: ⅓ × 36 × 8 ='

silver[5] Q: r = 6 cmDiagram not drawn accurately Find the volume of a hemisphere with radius 6 cm. Giv
   step0 field=say answer=None text="A hemisphere is half a sphere. Find the full sphere's volume, then halve it."
   step1 field=pre answer=216 text='Cube the radius: 6³ ='
   step2 field=pre answer=288 text='Full sphere factor: 216 × 4 ÷ 3 ='
   step3 field=pre answer=144 text='Halve it for a hemisphere: 288 ÷ 2 ='
   step4 field=pre answer=452.4 text='Multiply by π: 144 × π ='
   step5 field=pre answer=452.4 text='Check in one go: \\(\\frac{2}{3}\\) × π × 216 rounds to'
