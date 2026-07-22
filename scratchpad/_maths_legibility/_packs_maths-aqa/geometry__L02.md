# maths-aqa / geometry / L02 - Area & Perimeter

## bronze[0] (input: single_value, main-box unit: (none))
Q: 12 cm5 cmFind the area of a rectangle with length 12 cm and width 5 cm.
   - intro: Area of a rectangle is length × width, so 12 × 5. Do it in two easy pieces.
   - ask: First, 10 × 5 =  [box=50, NO label]
   - ask: Now 2 × 5 =  [box=10, NO label]
   - ask: Add the pieces: 50 + 10 =  [box=60, NO label]
   - ask: Check the other way, 5 rows of 12: 5 × 12 =  [box=60, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: 9 cm4 cmFind the perimeter of a rectangle with length 9 cm and width 4 cm.
   - intro: Perimeter is the distance all the way round: 9 + 4 + 9 + 4.
   - ask: Add one length and one width: 9 + 4 =  [box=13, NO label]
   - ask: There are two of each, so double it: 13 × 2 =  [box=26, NO label]
   - ask: Check by adding all four sides: 9 + 9 + 4 + 4 =  [box=26, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: base 10 cm6 cmDiagram not drawn accuratelyFind the area of a triangle with base 10 cm and perpendicular height 6 cm.
   - intro: Area of a triangle = ½ × base × height.
   - ask: First multiply base × height: 10 × 6 =  [box=60, NO label]
   - ask: Now take half: 60 ÷ 2 =  [box=30, NO label]
   - ask: Sense check: a triangle is half its surrounding 10 by 6 rectangle, and half of 60 =  [box=30, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: base 8 cm5 cmDiagram not drawn accuratelyFind the area of a parallelogram with base 8 cm and perpendicular height 5 cm.
   - intro: Area of a parallelogram = base × perpendicular height. No halving.
   - ask: Slide the slanted end across and it becomes a rectangle 8 by 5. That area = 8 × 5 =  [box=40, label:'cm²']
   - ask: So the parallelogram equals that rectangle. Write the area:  [box=40, label:'cm²']
   - ask: Careful check: it is base × height, not ½ × base × height. Half would be 20, so the true area is 20 × 2 =  [box=40, label:'cm²']

## bronze[4] (input: single_value, main-box unit: (none))
Q: 5 cm9 cm6 cmDiagram not drawn accuratelyFind the area of a trapezium with parallel sides 5 cm and 9 cm, and height 6 cm.
   - intro: Area of a trapezium = ½ × (a + b) × height. Average the parallel sides, then × height.
   - ask: Add the parallel sides: 5 + 9 =  [box=14, NO label]
   - ask: Average them: 14 ÷ 2 =  [box=7, NO label]
   - ask: Multiply by the height: 7 × 6 =  [box=42, NO label]
   - ask: Check the other order, ½ × 14 × 6: first 14 × 6 = 84, then half: 84 ÷ 2 =  [box=42, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Perimeter = 28 cmArea = ?Diagram not drawn accuratelyA square has perimeter 28 cm. Find its area.
   - intro: Find the side first, then the area. All four sides of a square are equal.
   - ask: Side = perimeter ÷ 4 = 28 ÷ 4 =  [box=7, NO label]
   - ask: Area = side × side = 7 × 7 =  [box=49, label:'cm²']
   - ask: Check the perimeter of a side-7 square: 7 × 4 =  [box=28, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: r = 7 cmFind the circumference of a circle with radius 7 cm. Give your answer to 1 decimal place.
   - intro: Circumference = 2 × π × r. This is a calculator question.
   - ask: Double the radius first: 2 × 7 =  [box=14, NO label]
   - ask: Multiply by π, to 1 decimal place: 14 × π =  [box=44, NO label]
   - ask: Cross-check: the area would be π × 49 ≈ 153.9, a different thing. The distance round is 14 × π ≈  [box=44, label:'cm²']

## bronze[7] (input: single_value, main-box unit: (none))
Q: r = 5 cmFind the area of a circle with radius 5 cm. Give your answer to 1 decimal place.
   - intro: Area = π × r². Square the radius first.
   - ask: Square the radius: 5 × 5 =  [box=25, NO label]
   - ask: Multiply by π, to 1 decimal place: 25 × π =  [box=78.5, NO label]
   - ask: Cross-check: the circumference would be 2 × π × 5 ≈ 31.4, a length not an area. The area is π × 25 ≈  [box=78.5, label:'cm²']

## silver[0] (input: single_value, main-box unit: (none))
Q: diameter 12 cmDiagram not drawn accuratelyA semicircle has diameter 12 cm. Find its area. Give your answer to 1 decimal place.
   - intro: A semicircle is half a circle. Find the radius, then take half the circle's area.
   - ask: Radius = diameter ÷ 2 = 12 ÷ 2 =  [box=6, NO label]
   - ask: Square it: 6 × 6 =  [box=36, NO label]
   - ask: Half circle area = ½ × π × 36, to 1 decimal place =  [box=56.5, NO label]
   - ask: Check the radius fits: 2 × 6 =  [box=12, NO label]

## silver[1] (input: single_value, main-box unit: (none))
Q: r 315 cm8 cmA rectangle is 15 cm by 8 cm. A circle of radius 3 cm is cut from the middle. Find the remaining area to 1 decimal place.
   - intro: Find the rectangle, then subtract the circle that is cut out.
   - ask: Rectangle area = 15 × 8 =  [box=120, NO label]
   - ask: Square the circle's radius: 3 × 3 =  [box=9, NO label]
   - ask: Circle area = π × 9, to 2 decimal places =  [box=28.27, NO label]
   - ask: Subtract, to 1 decimal place: 120 − 28.27 =  [box=91.7, NO label]
   - ask: Sense check: the hole is small, so 120 − 91.7 =  [box=28.3, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: base 9 cmh = ?Area 36Diagram not drawn accuratelyA triangle has area 36 cm² and base 9 cm. Find the perpendicular height.
   - intro: Work the area formula backwards. Area = ½ × base × height.
   - ask: Half the base: ½ × 9 =  [box=4.5, NO label]
   - ask: So 4.5 × height = 36, meaning height = 36 ÷ 4.5 =  [box=8, NO label]
   - ask: Check forwards: ½ × 9 × 8 means 4.5 × 8 =  [box=36, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: perimeter 25.7 cmr = ?Diagram not drawn accuratelyThe perimeter of a semicircle is 25.7 cm. Find the radius to the nearest whole number.
   - intro: Perimeter of a semicircle = the curved half plus the straight diameter: π r + 2 r = r × (π + 2).
   - ask: Add the two multipliers: π + 2, to 2 decimal places =  [box=5.14, NO label]
   - ask: So 5.14 × r = 25.7, meaning r = 25.7 ÷ 5.14 =  [box=5, NO label]
   - ask: Check: 5 × (π + 2) = 5 × 5.14 =  [box=25.7, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: base 6 cm4 cmDiagram not drawn accuratelyTwo congruent triangles with base 6 cm and height 4 cm are put together to form a parallelogram. Find the area of the parallelogram.
   - intro: Two identical triangles slot together into a parallelogram, area base × height.
   - ask: Area of one triangle: first 6 × 4 =  [box=24, label:'cm²']
   - ask: Halve it for the triangle: 24 ÷ 2 =  [box=12, NO label]
   - ask: Two triangles make the parallelogram: 12 × 2 =  [box=24, NO label]
   - ask: Or straight from base × height: 6 × 4 =  [box=24, NO label]

## silver[5] (input: single_value, main-box unit: (none))
Q: C = 31.4 mA circular garden has circumference 31.4 m. Find its area to 1 decimal place.
   - intro: Get the radius from the circumference, then find the area.
   - ask: C = 2 × π × r, so first work out 2 × π, to 2 decimal places =  [box=6.28, NO label]
   - ask: Radius = 31.4 ÷ 6.28 =  [box=5, NO label]
   - ask: Area = π × r² = π × 25, to 1 decimal place =  [box=78.5, NO label]
   - ask: Check the circumference of a radius-5 circle: 2 × π × 5, to 1 dp =  [box=31.4, NO label]

## silver[6] (input: single_value, main-box unit: (none))
Q: 6 cm5 cm24Diagram not drawn accuratelyAn L-shape is formed by cutting a 2 cm × 4 cm rectangle from a corner of a 6 cm × 5 cm rectangle. Find the remaining area.
   - intro: The L-shape is the whole rectangle minus the cut-out corner.
   - ask: Whole rectangle = 6 × 5 =  [box=30, NO label]
   - ask: Cut-out corner = 2 × 4 =  [box=8, NO label]
   - ask: Subtract: 30 − 8 =  [box=22, NO label]
   - ask: Check: the L-shape is smaller than the rectangle by exactly the corner, 30 − 22 =  [box=8, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: 135°r = 8 cmDiagram not drawn accuratelyA sector has radius 8 cm and angle 135°. Find the area to 1 decimal place.
   - intro: A sector is a fraction of the whole circle: fraction = angle ÷ 360.
   - ask: Square the radius: 8 × 8 =  [box=64, NO label]
   - ask: Fraction of the circle = 135 ÷ 360 =  [box=0.375, label:'(a decimal)']
   - ask: Sector area = 0.375 × π × 64, to 1 decimal place =  [box=75.4, NO label]
   - ask: Cross-check: the whole circle is π × 64 ≈ 201.1, and 0.375 × 201.1 =  [box=75.4, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: 72°r = 10 cmDiagram not drawn accuratelyA sector has radius 10 cm and angle 72°. Find the arc length to 1 decimal place.
   - intro: Arc length is the same fraction of the whole circumference: (angle ÷ 360) × 2 π r.
   - ask: Fraction of the circle = 72 ÷ 360 =  [box=0.2, label:'(a decimal)']
   - ask: Full circumference = 2 × π × 10, to 1 decimal place =  [box=62.8, NO label]
   - ask: Arc = 0.2 × 62.8, to 1 decimal place =  [box=12.6, NO label]
   - ask: Cross-check: 360 ÷ 72 = 5, so five arcs make the full circle: 12.6 × 5 =  [box=63, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: 100 m100 md 60Diagram not drawn accuratelyA running track is two semicircles (diameter 60 m) joined by two straights of 100 m. Find the total perimeter to the nearest whole number.
   - intro: Two semicircles of diameter 60 join into one full circle. Then add the two straight sides.
   - ask: Curved part = π × diameter = π × 60, to the nearest whole =  [box=188, NO label]
   - ask: Two straights = 2 × 100 =  [box=200, NO label]
   - ask: Total perimeter = 188 + 200 =  [box=388, label:'cm']
   - ask: Check: take the straights off, 388 − 200 =  [box=188, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: Area 154A circle has area 154 cm². Find the radius to 1 decimal place.
   - intro: Work area = π r² backwards. Divide by π, then take the square root.
   - ask: Divide the area by π: 154 ÷ π, to the nearest whole =  [box=49, NO label]
   - ask: That is r². Square-root it: √49 =  [box=7, NO label]
   - ask: Check forwards: π × 7² = π × 49, to the nearest whole =  [box=154, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: R 10r 6Diagram not drawn accuratelyAn annulus (ring) has outer radius 10 cm and inner radius 6 cm. Find the area to 1 decimal place.
   - intro: An annulus is the big circle minus the small circle. Subtract the AREAS, never the radii.
   - ask: Big circle: π × 10² = π × 100, to 1 decimal place =  [box=314.2, NO label]
   - ask: Small circle: π × 6² = π × 36, to 1 decimal place =  [box=113.1, NO label]
   - ask: Subtract: 314.2 − 113.1 =  [box=201.1, NO label]
   - ask: Shortcut check: π × (100 − 36) = π × 64, to 1 decimal place =  [box=201.1, NO label]
