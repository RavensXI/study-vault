# maths-ocr / geometry / L01 - Angle Facts & Properties

## bronze[0] (input: single_value, main-box unit: (none))
Q: 72°x°Two angles on a straight line: 72° and \(x°\). Find \(x\).
   - intro: Angles on a straight line always add up to 180°. The two angles here fill that straight line.
   - ask: The total to fill for a straight line is  [box=180, label:'°']
   - intro: Now take the angle you know from that total.
   - ask: 180 − 72 =  [box=108, label:'°']
   - ask: Check: 72 + 108 =  [box=180, label:'°']

## bronze[1] (input: single_value, main-box unit: (none))
Q: 90°120°85°x°Angles at a point: 90°, 120°, 85°, \(x°\). Find \(x\).
   - intro: The angles around a point make a full turn, which is 360°.
   - ask: The total to fill for a point is  [box=360, label:'°']
   - intro: Add the three angles you know.
   - ask: 90 + 120 + 85 =  [box=295, label:'°']
   - ask: 360 − 295 =  [box=65, label:'°']
   - ask: Check: 295 + 65 =  [box=360, label:'°']

## bronze[2] (input: single_value, main-box unit: (none))
Q: ?50°70°Diagram not drawn accuratelyA triangle has angles 50° and 70°. Find the third angle.
   - intro: The three angles inside a triangle always add up to 180°.
   - ask: The total for a triangle is  [box=180, label:'°']
   - ask: Add the two you know: 50 + 70 =  [box=120, label:'°']
   - ask: 180 − 120 =  [box=60, label:'°']
   - ask: Check: 50 + 70 + 60 =  [box=180, label:'°']

## bronze[3] (input: single_value, main-box unit: (none))
Q: 40°??Diagram not drawn accuratelyAn isosceles triangle has a top angle of 40°. Find each base angle.
   - intro: The two base angles of an isosceles triangle are equal, and all three still add to 180°.
   - ask: First take the top angle from 180: 180 − 40 =  [box=140, label:'°']
   - intro: That 140° is shared equally between the two base angles.
   - ask: 140 ÷ 2 =  [box=70, label:'°']
   - ask: Check: 40 + 70 + 70 =  [box=180, label:'°']

## bronze[4] (input: single_value, main-box unit: (none))
Q: 55°?Two vertically opposite angles: one is 55°. What is the other?
   - intro: When two straight lines cross, the angles opposite each other are equal.
   - ask: The given angle is 55°, so the vertically opposite one is also  [box=55, label:'°']
   - intro: You can check using the straight line. The angle next door fills the line with 55°.
   - ask: Neighbour on the line: 180 − 55 =  [box=125, label:'°']
   - ask: That neighbour is opposite a 125° too, and 125 + 55 =  [box=180, label:'°']

## bronze[5] (input: single_value, main-box unit: (none))
Q: 63°?Alternate angles on parallel lines: one is 63°. Find the other.
   - intro: Alternate angles lie on opposite sides of the line crossing the parallels, in a Z shape, and they are equal.
   - ask: The given alternate angle is 63°, so the other is also  [box=63, label:'°']
   - intro: Check with the co-interior angle on the same side, which should add with it to 180°.
   - ask: Co-interior partner: 180 − 63 =  [box=117, label:'°']
   - ask: And 117 + 63 =  [box=180, label:'°']

## bronze[6] (input: single_value, main-box unit: (none))
Q: 105°?Co-interior angles on parallel lines: one is 105°. Find the other.
   - intro: Co-interior angles sit on the same side of the crossing line, in a C shape, and add up to 180°.
   - ask: The total for a co-interior pair is  [box=180, label:'°']
   - ask: 180 − 105 =  [box=75, label:'°']
   - ask: Check: 105 + 75 =  [box=180, label:'°']

## bronze[7] (input: single_value, main-box unit: (none))
Q: Sum of angles in a quadrilateral?
   - intro: A quadrilateral can be split into two triangles by drawing one diagonal.
   - ask: Each triangle's angles add to  [box=180, label:'°']
   - ask: Two triangles: 2 × 180 =  [box=360, label:'°']
   - ask: Check with the formula (4 − 2) × 180 =  [box=360, label:'°']

## silver[0] (input: single_value, main-box unit: (none))
Q: Find the sum of interior angles of a hexagon.
   - intro: The interior angles of any polygon add up to (n − 2) × 180°. A hexagon has 6 sides.
   - ask: n − 2 = 6 − 2 =  [box=4, NO label]
   - ask: 4 × 180 =  [box=720, label:'°']
   - ask: Check: a hexagon splits into 4 triangles, 4 × 180 =  [box=720, label:'°']

## silver[1] (input: single_value, main-box unit: (none))
Q: Each interior angle of a regular polygon is 120°. How many sides?
   - intro: Work through the exterior angle. Interior and exterior angles on a straight line add to 180°.
   - ask: Exterior angle: 180 − 120 =  [box=60, label:'°']
   - ask: Exterior angles add to 360°, so sides = 360 ÷ 60 =  [box=6, NO label]
   - ask: Check: interior sum = (6 − 2) × 180 = 720, and 720 ÷ 6 =  [box=120, label:'°']

## silver[2] (input: single_value, main-box unit: (none))
Q: Find each exterior angle of a regular octagon.
   - intro: The exterior angles of any polygon always add up to 360°. A regular octagon has 8 equal exterior angles.
   - ask: There are 8 equal exterior angles totalling  [box=360, label:'°']
   - ask: 360 ÷ 8 =  [box=45, label:'°']
   - ask: Check: interior angle = 180 − 45 =  [box=135, label:'°']

## silver[3] (input: single_value, main-box unit: (none))
Q: Find each interior angle of a regular pentagon.
   - intro: First find the total of all the interior angles with (n − 2) × 180°, then share it equally. A pentagon has 5 sides.
   - ask: Interior sum: (5 − 2) × 180 = 3 × 180 =  [box=540, label:'°']
   - ask: Each angle: 540 ÷ 5 =  [box=108, label:'°']
   - ask: Check: exterior = 180 − 108 = 72, and 72 × 5 =  [box=360, label:'°']

## silver[4] (input: single_value, main-box unit: (none))
Q: 2x°(3x+10)°Two angles on parallel lines are co-interior. One is \(2x°\) and the other is \(3x + 10°\). Find \(x\).
   - intro: Co-interior angles add to 180°. So 2x + (3x + 10) = 180.
   - ask: Combine the x terms: 2x + 3x =  [box=5, label:'x']
   - ask: So 5x + 10 = 180. Take 10 from both sides: 180 − 10 =  [box=170, NO label]
   - ask: 5x = 170, so x = 170 ÷ 5 =  [box=34, NO label]
   - ask: Check: 2×34 + 3×34 + 10 = 68 + 102 + 10 =  [box=180, label:'°']

## silver[5] (input: single_value, main-box unit: (none))
Q: A regular polygon has exterior angles of 24°. How many sides?
   - intro: The exterior angles of a polygon add up to 360°, so the number of sides is 360 divided by one exterior angle.
   - ask: The exterior angles total  [box=360, label:'°']
   - ask: 360 ÷ 24 =  [box=15, NO label]
   - ask: Check: 15 × 24 =  [box=360, label:'°']

## silver[6] (input: single_value, main-box unit: (none))
Q: The interior angle sum of a polygon is 1440°. How many sides?
   - intro: The interior sum formula is (n − 2) × 180°. Set it equal to 1440 and solve for n.
   - ask: Divide by 180: 1440 ÷ 180 =  [box=8, NO label]
   - ask: That 8 equals n − 2, so n = 8 + 2 =  [box=10, NO label]
   - ask: Check: (10 − 2) × 180 =  [box=1440, label:'°']

## gold[0] (input: single_value, main-box unit: (none))
Q: 42°65°?Diagram not drawn accuratelyA triangle on parallel lines: angle at top = 42°, angle at bottom-left = 65°. Find the angle at bottom-right.
   - intro: The three angles of any triangle add to 180°, whatever lines it sits on.
   - ask: The total for a triangle is  [box=180, label:'°']
   - ask: Add the two known angles: 42 + 65 =  [box=107, label:'°']
   - ask: 180 − 107 =  [box=73, label:'°']
   - ask: Check: 42 + 65 + 73 =  [box=180, label:'°']

## gold[1] (input: single_value, main-box unit: (none))
Q: 90°120°?Two regular polygons share a side. One is a square, the other a regular hexagon. Find the angle between them at the shared vertex.
   - intro: The three angles meeting at the shared corner go all the way around a point, which is 360°.
   - ask: A square's interior angle is  [box=90, label:'°']
   - ask: A regular hexagon's interior angle is 720 ÷ 6 =  [box=120, label:'°']
   - ask: The gap fills the rest of the point: 360 − 90 − 120 =  [box=150, label:'°']
   - ask: Check: 90 + 120 + 150 =  [box=360, label:'°']

## gold[2] (input: single_value, main-box unit: (none))
Q: Interior angle of a regular polygon is 5× its exterior angle. Find the number of sides.
   - intro: Interior and exterior angles sit on a straight line, so they add to 180°. Here the interior is 5 times the exterior.
   - ask: Interior is 5 parts, exterior 1 part, so 6 parts make 180. One part (the exterior) = 180 ÷ 6 =  [box=30, label:'°']
   - ask: Number of sides = 360 ÷ 30 =  [box=12, NO label]
   - ask: Check: interior = 5 × 30 = 150, and 150 + 30 =  [box=180, label:'°']

## gold[3] (input: single_value, main-box unit: (none))
Q: x2x3xDiagram not drawn accuratelyAngles in a triangle are \(x\), \(2x\), and \(3x\). Find the largest angle.
   - intro: The three angles add to 180°. In parts, that is x + 2x + 3x.
   - ask: Total parts: x + 2x + 3x =  [box=6, label:'x']
   - ask: So 6x = 180, giving x = 180 ÷ 6 =  [box=30, label:'°']
   - ask: The largest is 3x = 3 × 30 =  [box=90, label:'°']
   - ask: Check: 30 + 60 + 90 =  [box=180, label:'°']

## gold[4] (input: single_value, main-box unit: (none))
Q: (3x−10)°(2x+15)°Two angles are alternate on parallel lines: \(3x - 10\) and \(2x + 15\). Find \(x\).
   - intro: Alternate angles are equal, so set the two expressions equal: 3x − 10 = 2x + 15.
   - ask: Take 2x from both sides: 3x − 2x =  [box=1, label:'x']
   - ask: So x − 10 = 15. Add 10 to both sides: 15 + 10 =  [box=25, NO label]
   - ask: Check both angles: 3×25 − 10 = 65 and 2×25 + 15 =  [box=65, label:'°']
