# maths-edexcel / geometry / L02 - Area & Perimeter

## bronze[0] (input: single_value, main-box unit: (none))
Q: 9 cm5 cmFind the area of a rectangle with length 9 cm and width 5 cm.
   - intro: Area of a rectangle is length × width. Just multiply the two sides, nothing else.
   - ask: Write the calculation, length × width = 9 ×  [box=5, NO label]
   - ask: Now work it out: 9 × 5 =  [box=45, NO label]
   - ask: Check by dividing back: 45 ÷ 9 =  [box=5, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: 12 cm7 cmFind the perimeter of a rectangle with length 12 cm and width 7 cm.
   - intro: Perimeter is the distance all the way round. For a rectangle, add a length and a width, then double.
   - ask: First add one length and one width: 12 + 7 =  [box=19, NO label]
   - ask: Now double it, because there are two lengths and two widths: 19 × 2 =  [box=38, NO label]
   - ask: Check by adding all four sides: 12 + 7 + 12 + 7 =  [box=38, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: 10 cm6 cmDiagram not drawn accuratelyFind the area of a triangle with base 10 cm and height 6 cm.
   - intro: Area of a triangle is half of base × height.
   - ask: First multiply base × height: 10 × 6 =  [box=60, NO label]
   - ask: Now halve it, because a triangle is half a rectangle: 60 ÷ 2 =  [box=30, NO label]
   - ask: Check by doubling back: 30 × 2 =  [box=60, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: 8 cm5 cmDiagram not drawn accuratelyFind the area of a parallelogram with base 8 cm and height 5 cm.
   - intro: Area of a parallelogram is base × perpendicular height. No halving, unlike a triangle.
   - ask: Write the calculation, base × height = 8 ×  [box=5, NO label]
   - ask: Now work it out: 8 × 5 =  [box=40, NO label]
   - ask: Check by dividing back: 40 ÷ 8 =  [box=5, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: 14 cmFind the circumference of a circle with diameter 14 cm. Give your answer to 1 d.p.
   - intro: Circumference is π × diameter. The diameter is given, so there is no halving here.
   - ask: Multiply the diameter by π: 14 × π =  [box=43.98, NO label]
   - ask: Round to 1 decimal place: 43.98 rounds to  [box=44.0, NO label]
   - ask: Sense check: the circumference is a bit over 3 diameters, and 3 × 14 =  [box=42, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: 5 cmFind the area of a circle with radius 5 cm. Give your answer to 1 d.p.
   - intro: Area of a circle is π × radius². Square the radius first, then multiply by π.
   - ask: Square the radius: 5² = 5 × 5 =  [box=25, NO label]
   - ask: Now multiply by π and round to 1 d.p.: 25 × π =  [box=78.5, NO label]
   - ask: Sense check: without π it would be 25, and π is a bit over 3, so 3 × 25 =  [box=75, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: 5 cm9 cm6 cmDiagram not drawn accuratelyFind the area of a trapezium with parallel sides 5 cm and 9 cm and height 6 cm.
   - intro: Area of a trapezium is half of (the two parallel sides added) × height.
   - ask: Add the parallel sides: 5 + 9 =  [box=14, NO label]
   - ask: Multiply by the height: 14 × 6 =  [box=84, NO label]
   - ask: Now halve it: 84 ÷ 2 =  [box=42, NO label]
   - ask: Check by doubling back: 42 × 2 =  [box=84, NO label]

## bronze[7] (input: single_value, main-box unit: (none))
Q: Perimeter = 48 cmA square has perimeter 48 cm. Find its area.
   - intro: Two steps. A square has four equal sides, so first find one side, then square it for the area.
   - ask: Find one side: 48 ÷ 4 =  [box=12, NO label]
   - ask: Now the area: square the side, 12² = 12 × 12 =  [box=144, label:'cm²']
   - ask: Check the side: √144 =  [box=12, NO label]

## silver[0] (input: single_value, main-box unit: (none))
Q: 18 cmFind the area of a circle with diameter 18 cm. Give your answer to 1 d.p.
   - intro: The diameter is given, but the area formula needs the radius. Halve the diameter first.
   - ask: Halve the diameter: 18 ÷ 2 =  [box=9, NO label]
   - ask: Square the radius: 9² =  [box=81, NO label]
   - ask: Multiply by π and round to 1 d.p.: 81 × π =  [box=254.5, NO label]
   - ask: Check the radius came from the diameter: 9 × 2 =  [box=18, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: r = ?C = 31.4 cmA circle has circumference 31.4 cm. Find the radius to 1 d.p. (Use \(\pi = 3.14\))
   - intro: Circumference is 2 × π × radius. Here the circumference is known, so work backwards to the radius.
   - ask: First find 2 × π: 2 × 3.14 =  [box=6.28, NO label]
   - ask: Divide the circumference by that: 31.4 ÷ 6.28 =  [box=5, label:'cm']
   - ask: Check by working forwards: 2 × 3.14 × 5 =  [box=31.4, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: 3 m5 m8 m4 mAn L-shaped room can be split into a rectangle measuring 8 m by 4 m and another rectangle measuring 3 m by 5 m. Find the total floor area.
   - intro: Split the L into two rectangles, find each area, then add.
   - ask: First rectangle: 8 × 4 =  [box=32, NO label]
   - ask: Second rectangle: 3 × 5 =  [box=15, NO label]
   - ask: Add the two areas: 32 + 15 =  [box=47, NO label]
   - ask: Check by subtracting one back: 47 − 15 =  [box=32, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: 10 cmFind the area of a quarter circle with radius 10 cm. Give your answer to 1 d.p.
   - intro: A quarter circle is one quarter of a full circle. Take the quarter before the π so the numbers stay tidy.
   - ask: Square the radius: 10² =  [box=100, NO label]
   - ask: Take a quarter: 100 ÷ 4 =  [box=25, NO label]
   - ask: Multiply by π and round to 1 d.p.: 25 × π =  [box=78.5, NO label]
   - ask: Check by scaling back to a full circle: 78.5 × 4 =  [box=314, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: 8 cm12 cmh = ?Area = 60 cm²Diagram not drawn accuratelyA trapezium has area 60 cm², parallel sides 8 cm and 12 cm. Find the height.
   - intro: Use the trapezium formula backwards. Area = half × (sum of parallel sides) × height, and the height is missing.
   - ask: Add the parallel sides: 8 + 12 =  [box=20, NO label]
   - ask: Half of that: 20 ÷ 2 =  [box=10, NO label]
   - ask: So area = 10 × height. Divide to find the height: 60 ÷ 10 =  [box=6, label:'cm²']
   - ask: Check by working forwards: 10 × 6 =  [box=60, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: 7 cmFind the perimeter of a semicircle with radius 7 cm. Give your answer to 1 d.p.
   - intro: A semicircle's perimeter is the curved half PLUS the straight diameter across the middle. Both parts matter.
   - ask: The straight edge is the diameter: 2 × 7 =  [box=14, NO label]
   - ask: The curved edge is half the circumference: π × 7, to 1 d.p. =  [box=22.0, NO label]
   - ask: Add the two parts: 14 + 22 =  [box=36, NO label]
   - ask: Check the straight edge: half of the diameter, 14 ÷ 2 =  [box=7, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: r = ?Area = 50.3 cm²The area of a circle is 50.3 cm². Find the radius to 1 d.p.
   - intro: Area is π × radius². The area is known, so undo it: divide by π, then square-root.
   - ask: Divide the area by π: 50.3 ÷ π =  [box=16.0, NO label]
   - ask: That is the radius squared. Square-root it: √16 =  [box=4, label:'cm']
   - ask: Check by working forwards: 4² × π = 16 × π =  [box=50.3, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: 100 m60 mA running track is two straight sides of 100 m and two semicircular ends of diameter 60 m. Find the total perimeter to the nearest metre.
   - intro: The perimeter is the two straight sides plus the two curved ends. The two semicircular ends together make one full circle of diameter 60 m.
   - ask: The two straights: 2 × 100 =  [box=200, NO label]
   - ask: The two ends make one full circle, circumference π × diameter. On your calculator, π × 60 =  [box=188.5, NO label]
   - ask: Add, using the calculator's full value (not the rounded 188.5), then round the total to the nearest metre: 200 + π × 60 =  [box=388, NO label]
   - ask: Check the straights alone come to 200: 100 + 100 =  [box=200, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: 135°8 cmDiagram not drawn accuratelyA sector has radius 8 cm and angle \(135°\). Find the area to 1 d.p.
   - intro: A sector is a fraction of a whole circle. The fraction is the angle over 360.
   - ask: The fraction of the circle: 135 ÷ 360 =  [box=0.375, label:'(a decimal)']
   - ask: Square the radius: 8² =  [box=64, NO label]
   - ask: Multiply the fraction, the square and π, then round to 1 d.p.: 0.375 × 64 × π =  [box=75.4, NO label]
   - ask: Check the fraction step: 0.375 × 360 =  [box=135, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: C = ?Area = 200 cm²A circle has area \(200\) cm². Find the circumference to 1 d.p.
   - intro: Two stages: turn the area back into a radius, then use the radius to find the circumference.
   - ask: Divide the area by π: 200 ÷ π =  [box=63.66, NO label]
   - ask: That is the radius squared. Square-root it: √63.66 =  [box=7.98, NO label]
   - ask: Now the circumference: 2 × π × 7.98, to 1 d.p. =  [box=50.1, label:'cm']
   - ask: Check by squaring the radius and using π: 7.98² × π ≈  [box=200, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: θ = ?9 cmarc 12 cmDiagram not drawn accuratelyA sector has arc length 12 cm and radius 9 cm. Find the sector angle to the nearest degree.
   - intro: Arc length is a fraction of the full circumference. The fraction is the angle over 360, so work backwards to the angle.
   - ask: Full circumference = 2 × π × radius = 2 × π × 9 =  [box=56.55, NO label]
   - ask: The arc is 12 out of that whole circumference. Fraction of the circle: 12 ÷ 56.55 =  [box=0.2122, label:'(a decimal)']
   - ask: Multiply the fraction by 360 for the angle, to the nearest degree: 0.2122 × 360 =  [box=76, NO label]
   - ask: Check by working forwards: 0.2122 × 56.55 =  [box=12, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: 10 cm6 cmAn annulus (ring) has outer radius 10 cm and inner radius 6 cm. Find the area to 1 d.p.
   - intro: An annulus is a big circle with a smaller circle cut out. Find each area, then subtract. Square each radius BEFORE subtracting.
   - ask: Outer radius squared: 10² =  [box=100, NO label]
   - ask: Inner radius squared: 6² =  [box=36, NO label]
   - ask: Subtract the squares, then multiply by π, to 1 d.p.: (100 − 36) × π = 64 × π =  [box=201.1, NO label]
   - ask: Check the subtraction: 100 − 36 =  [box=64, NO label]
