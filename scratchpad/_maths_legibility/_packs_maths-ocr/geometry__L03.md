# maths-ocr / geometry / L03 - Volume & Surface Area

## bronze[0] (input: single_value, main-box unit: (none))
Q: 6 cm3 cm4 cmDiagram not drawn accurately Find the volume of a cuboid with length 6 cm, width 4 cm and height 3 cm.
   - intro: Volume of a cuboid is length × width × height. Multiply all three.
   - ask: Multiply length by width: 6 × 4 =  [box=24, NO label]
   - ask: Now multiply by the height: 24 × 3 =  [box=72, NO label]
   - ask: Check another order: 4 × 3 × 6 =  [box=72, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: 5 cmDiagram not drawn accurately Find the volume of a cube with side length 5 cm.
   - intro: Volume of a cube is side × side × side.
   - ask: Square the side: 5 × 5 =  [box=25, NO label]
   - ask: Multiply by the side again: 25 × 5 =  [box=125, NO label]
   - ask: Compare: the surface area would be 6 × 25 =  [box=150, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: 4 cmDiagram not drawn accurately Find the surface area of a cube with side length 4 cm.
   - intro: A cube has 6 identical square faces. Find one face, then multiply by 6.
   - ask: Area of one face: 4 × 4 =  [box=16, NO label]
   - ask: Six faces: 6 × 16 =  [box=96, NO label]
   - ask: Compare: the volume would be 4 × 4 × 4 =  [box=64, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: area 15 cm²length 8 cmDiagram not drawn accurately A prism has a cross-section area of 15 cm² and length 8 cm. Find its volume.
   - intro: Volume of any prism is the cross-section area times the length.
   - ask: Write the cross-section area:  [box=15, NO label]
   - ask: Multiply by the length: 15 × 8 =  [box=120, label:'cm']
   - ask: Check: 120 ÷ 8 =  [box=15, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: 6 cm4 cm7 cmDiagram not drawn accurately A triangular prism has a triangle base 6 cm, triangle height 4 cm and length 7 cm. Find its volume.
   - intro: A triangular prism's cross-section is the triangle. Find its area, then multiply by the length.
   - ask: Triangle area: ½ × 6 × 4 =  [box=12, NO label]
   - ask: Multiply by the length: 12 × 7 =  [box=84, label:'cm']
   - ask: Check: 84 ÷ 7 =  [box=12, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: 5 cm2 cm3 cmDiagram not drawn accurately Find the surface area of a cuboid 5 cm × 3 cm × 2 cm.
   - intro: Surface area of a cuboid is 2(lw + lh + wh). Find the three different faces first.
   - ask: Top and bottom face: 5 × 3 =  [box=15, NO label]
   - ask: Front and back face: 5 × 2 =  [box=10, NO label]
   - ask: Side face: 3 × 2 =  [box=6, NO label]
   - ask: Add the three and double: 2 × (15 + 10 + 6) =  [box=62, NO label]
   - ask: Check the half first: 15 + 10 + 6 =  [box=31, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: 10 cm?6 cmDiagram not drawn accurately A cuboid has volume 180 cm³. Its length is 10 cm and width is 6 cm. Find the height.
   - intro: Volume = length × width × height, so height = volume ÷ (length × width).
   - ask: Multiply length by width: 10 × 6 =  [box=60, NO label]
   - ask: Divide the volume by the base area: 180 ÷ 60 =  [box=3, label:'cm²']
   - ask: Check: 10 × 6 × 3 =  [box=180, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: r = 2 cmh = 5 cmDiagram not drawn accurately Find the volume of a cylinder with radius 2 cm and height 5 cm. Give your answer to the nearest whole number.
   - intro: Volume of a cylinder is \(\pi r^2 h\). Square the radius first.
   - ask: Square the radius: 2² =  [box=4, NO label]
   - ask: Multiply by the height: 4 × 5 =  [box=20, NO label]
   - ask: Multiply by π and round: 20 × π =  [box=63, NO label]
   - ask: Check: π × 2² × 5 rounds to  [box=63, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: r = 5 cmh = 12 cmDiagram not drawn accurately Find the volume of a cylinder with radius 5 cm and height 12 cm. Give your answer to 1 d.p.
   - intro: Volume of a cylinder is \(\pi r^2 h\). Square the radius first.
   - ask: Square the radius: 5² =  [box=25, NO label]
   - ask: Multiply by the height: 25 × 12 =  [box=300, NO label]
   - ask: Multiply by π: 300 × π =  [box=942.5, NO label]
   - ask: Check: π × 5² × 12 rounds to  [box=942.5, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: r = 3 cmh = 10 cmDiagram not drawn accurately Find the total surface area of a cylinder with radius 3 cm and height 10 cm. Give your answer to 1 d.p.
   - intro: Surface area of a cylinder is \(2\pi r^2 + 2\pi r h\): the two circular ends plus the curved side. Work in π units.
   - ask: The two ends, 2πr², in π units: 2 × 3² =  [box=18, NO label]
   - ask: The curved side, 2πrh, in π units: 2 × 3 × 10 =  [box=60, NO label]
   - ask: Add and multiply by π: (18 + 60) × π =  [box=245, NO label]
   - ask: Check: 78 × π rounds to  [box=245, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: h = 9 cmr = 4 cmDiagram not drawn accurately A cone has radius 4 cm and height 9 cm. Find the volume to 1 d.p.
   - intro: Volume of a cone is \(\frac{1}{3}\pi r^2 h\). Build the \(\pi r^2 h\) part, then take a third.
   - ask: Square the radius: 4² =  [box=16, NO label]
   - ask: Multiply by the height: 16 × 9 =  [box=144, NO label]
   - ask: Take one third: 144 ÷ 3 =  [box=48, NO label]
   - ask: Multiply by π: 48 × π =  [box=150.8, NO label]
   - ask: Check: ⅓ × π × 16 × 9 rounds to  [box=150.8, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: r = 3 cmDiagram not drawn accurately A sphere has radius 3 cm. Find the volume to 1 d.p.
   - intro: Volume of a sphere is \(\frac{4}{3}\pi r^3\). Cube the radius first.
   - ask: Cube the radius: 3³ =  [box=27, NO label]
   - ask: Multiply by 4: 27 × 4 =  [box=108, NO label]
   - ask: Divide by 3: 108 ÷ 3 =  [box=36, NO label]
   - ask: Multiply by π: 36 × π =  [box=113.1, NO label]
   - ask: Check: four thirds × π × 27 rounds to  [box=113.1, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: r = 5 cmDiagram not drawn accurately A hemisphere has radius 5 cm. Find the volume to 1 d.p.
   - intro: A hemisphere is half a sphere. Find the full sphere's volume, then halve it.
   - ask: Cube the radius: 5³ =  [box=125, NO label]
   - ask: Sphere volume: four thirds × π × 125 =  [box=523.6, NO label]
   - ask: Halve it for a hemisphere: 523.6 ÷ 2 =  [box=261.8, NO label]
   - ask: Check: two thirds × π × 125 rounds to  [box=261.8, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: 6 cmh = 10 cmDiagram not drawn accurately A pyramid has a square base of side 6 cm and height 10 cm. Find the volume.
   - intro: Volume of a pyramid is \(\frac{1}{3} \times\) base area \(\times h\). Find the base area first.
   - ask: Base area (square): 6 × 6 =  [box=36, NO label]
   - ask: Multiply by the height: 36 × 10 =  [box=360, NO label]
   - ask: Take one third: 360 ÷ 3 =  [box=120, NO label]
   - ask: Check: ⅓ × 36 × 10 =  [box=120, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: r = 4 cmDiagram not drawn accurately A sphere has radius 4 cm. Find the surface area to 1 d.p.
   - intro: Surface area of a sphere is \(4\pi r^2\). Square the radius first.
   - ask: Square the radius: 4² =  [box=16, NO label]
   - ask: Multiply by 4: 16 × 4 =  [box=64, NO label]
   - ask: Multiply by π: 64 × π =  [box=201.1, NO label]
   - ask: Check: 4 × π × 4² rounds to  [box=201.1, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: h = 12 cmr = ?Diagram not drawn accurately A cone has volume 150 cm³ and height 12 cm. Find the radius to 1 d.p.
   - intro: Volume of a cone is \(\frac{1}{3}\pi r^2 h\). Put the numbers in and rearrange for r.
   - ask: The ⅓ × h part: ⅓ × 12 =  [box=4, NO label]
   - ask: Divide the volume by 4π: 150 ÷ (4 × π) =  [box=11.94, NO label]
   - ask: Square root for r: √11.94 =  [box=3.5, NO label]
   - ask: Check with the exact r²: ⅓ × π × 11.94 × 12 rounds to  [box=150, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: r = ?V = 904.8Diagram not drawn accurately A sphere has volume 904.8 cm³. Find the radius to the nearest cm.
   - intro: Volume of a sphere is \(\frac{4}{3}\pi r^3\). Rearrange for r: cube root of \(\frac{3V}{4\pi}\).
   - ask: Multiply the volume by 3: 904.8 × 3 =  [box=2714.4, NO label]
   - ask: Divide by 4π: 2714.4 ÷ (4 × π) =  [box=216, NO label]
   - ask: Cube root for r: ∛216 =  [box=6, NO label]
   - ask: Check: four thirds × π × 6³ rounds to  [box=904.8, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: A cylinder and a cone have the same radius and height (r = 3 cm, h = 9 cm). How many times bigger is the cylinder's volume than the cone's volume?
   - intro: Volume of a cylinder is \(\pi r^2 h\); volume of a cone is \(\frac{1}{3}\pi r^2 h\). Use r = 3 and h = 9 in both, then divide.
   - ask: Cylinder in π units: 3² × 9 =  [box=81, NO label]
   - ask: Cone in π units: ⅓ × 3² × 9 = ⅓ × 81 =  [box=27, NO label]
   - ask: How many times bigger: 81 ÷ 27 =  [box=3, NO label]
   - ask: Check: a cone is always ⅓ of the matching cylinder, so the cylinder is 3 × the cone, giving  [box=3, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: r = 6r = 3h = 126Diagram not drawn accurately A frustum is made by cutting a cone (radius 6 cm, height 12 cm) at half its height and removing the top. Find the volume of the frustum to the nearest cm³.
   - intro: The frustum is the big cone with the small top cone removed. Cutting at half height also halves the radius, so the small cone is r = 3, h = 6.
   - ask: Big cone in π units: ⅓ × 6² × 12 = ⅓ × 432 =  [box=144, NO label]
   - ask: Small cone in π units: ⅓ × 3² × 6 = ⅓ × 54 =  [box=18, NO label]
   - ask: Subtract, then multiply by π: (144 − 18) × π =  [box=396, NO label]
   - ask: Check: 126 × π rounds to  [box=396, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: r = 5 cmDiagram not drawn accurately A sphere fits exactly inside a cylinder. The sphere has radius 5 cm. Find the volume of the empty space inside the cylinder. Give your answer to 1 d.p.
   - intro: The sphere touches the cylinder all round, so the cylinder has radius 5 and height 10 (the diameter). Empty space = cylinder − sphere.
   - ask: Cylinder volume: π × 5² × 10 = 250π =  [box=785.4, NO label]
   - ask: Sphere volume: four thirds × π × 5³ = 500π ÷ 3 =  [box=523.6, NO label]
   - ask: Subtract: 785.4 − 523.6 =  [box=261.8, NO label]
   - ask: Check: the gap is exactly a third of the cylinder, 250π ÷ 3 rounds to  [box=261.8, NO label]
