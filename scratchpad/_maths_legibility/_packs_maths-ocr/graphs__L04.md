# maths-ocr / graphs / L04 - Real-Life Graphs

## bronze[0] (input: single_value, main-box unit: (none))
Q: The distance-time graph shows a journey. How far did the person travel in the first 2 hours?
   - intro: The distance travelled is the height of the line. Read it at the time you are asked for.
   - ask: Read the height at time = 1 hour:  [box=30, label:' km']
   - ask: Read the height at time = 2 hours:  [box=60, label:' km']
   - ask: So the distance in the first 2 hours is  [box=60, label:' km']

## bronze[1] (input: single_value, main-box unit: (none))
Q: Using the distance-time graph, for how long did the person stop?
   - intro: A stop shows up as a flat, horizontal section: the distance is not changing.
   - ask: The flat part starts at time =  [box=2, label:' hours']
   - ask: The flat part ends at time =  [box=3, label:' hours']
   - ask: Stop length = 3 − 2 =  [box=1, label:' hours']
   - ask: Check: over the flat part the distance stayed at  [box=60, label:' km']

## bronze[2] (input: single_value, main-box unit: (none))
Q: A car travels 120 km in 3 hours. What is the average speed in km/h?
   - intro: Average speed is total distance ÷ total time.
   - ask: Write the distance:  [box=120, label:' km']
   - ask: Divide by the time: 120 ÷ 3 =  [box=40, label:' km/h']
   - ask: Check: 40 km/h × 3 h =  [box=120, label:' km']

## bronze[3] (input: single_value, main-box unit: (none))
Q: A cyclist travels at 15 km/h for 2 hours. How far do they go?
   - intro: Distance = speed × time.
   - ask: Write the speed:  [box=15, label:' km/h']
   - ask: Multiply by the time: 15 × 2 =  [box=30, label:' km']
   - ask: Check: 30 km ÷ 2 h =  [box=15, label:' km/h']

## bronze[4] (input: single_value, main-box unit: (none))
Q: A bus travels 50 miles in 2.5 hours. What is the speed in mph?
   - intro: Speed = distance ÷ time.
   - ask: Write the distance:  [box=50, label:' miles']
   - ask: Divide by the time: 50 ÷ 2.5 =  [box=20, label:' mph']
   - ask: Check: 20 mph × 2.5 h =  [box=50, label:' miles']

## bronze[5] (input: single_value, main-box unit: (none))
Q: A conversion graph shows 5 miles ≈ 8 km. Use it to convert 15 miles to kilometres.
   - intro: Miles are bigger than kilometres, so the km number will be larger. Find the km in one mile first.
   - ask: Kilometres in 1 mile: 8 ÷ 5 =  [box=1.6, label:' km']
   - ask: 15 miles × 1.6 =  [box=24, label:' km']
   - ask: Check: 24 ÷ 1.6 =  [box=15, label:' miles']

## bronze[6] (input: single_value, main-box unit: (none))
Q: A runner completes 800 m in 200 seconds. What is their speed in m/s?
   - intro: Speed = distance ÷ time.
   - ask: Write the distance:  [box=800, label:' m']
   - ask: Divide by the time: 800 ÷ 200 =  [box=4, label:' m/s']
   - ask: Check: 4 m/s × 200 s =  [box=800, label:' m']

## bronze[7] (input: single_value, main-box unit: (none))
Q: A train travels at 60 mph for 1.5 hours. How far does it travel?
   - intro: Distance = speed × time.
   - ask: Write the speed:  [box=60, label:' mph']
   - ask: Multiply by the time: 60 × 1.5 =  [box=90, label:' miles']
   - ask: Check: 90 miles ÷ 1.5 h =  [box=60, label:' mph']

## silver[0] (input: single_value, main-box unit: (none))
Q: A car accelerates from 0 to 25 m/s in 5 seconds. What is the acceleration?
   - intro: Acceleration is the gradient of a speed-time graph: change in speed ÷ time.
   - ask: Change in speed = 25 − 0 =  [box=25, label:' m/s']
   - ask: Acceleration = 25 ÷ 5 =  [box=5, label:' m/s²']
   - ask: Check: 5 m/s² for 5 s gains 5 × 5 =  [box=25, label:' m/s']

## silver[1] (input: single_value, main-box unit: (none))
Q: The speed-time graph shows a car journey. Find the total distance travelled.
   - intro: Distance is the area under the line. Split it into a triangle, a rectangle, then a triangle.
   - ask: Triangle while speeding up (0 to 4 s): ½ × 4 × 20 =  [box=40, label:' m']
   - ask: Rectangle at steady speed (4 to 8 s): 4 × 20 =  [box=80, label:' m']
   - ask: Triangle while slowing down (8 to 10 s): ½ × 2 × 20 =  [box=20, label:' m']
   - ask: Total distance = 40 + 80 + 20 =  [box=140, label:' m']
   - ask: Check: total time = 4 + 4 + 2 =  [box=10, label:' s']

## silver[2] (input: single_value, main-box unit: (none))
Q: A car decelerates from 24 m/s to 0 in 3 seconds. What is the deceleration in m/s²?
   - intro: Deceleration is the size of the gradient: how fast the speed drops.
   - ask: Change in speed = 24 − 0 =  [box=24, label:' m/s']
   - ask: Deceleration = 24 ÷ 3 =  [box=8, label:' m/s²']
   - ask: Check: losing 8 m/s each second for 3 s loses 8 × 3 =  [box=24, label:' m/s']

## silver[3] (input: single_value, main-box unit: (none))
Q: A distance-time graph shows 0 km at t=0 and 90 km at t=1.5 hours. What is the speed?
   - intro: Speed on a distance-time graph is distance ÷ time.
   - ask: Distance climbed =  [box=90, label:' km']
   - ask: Speed = 90 ÷ 1.5 =  [box=60, label:' km/h']
   - ask: Check: 60 km/h × 1.5 h =  [box=90, label:' km']

## silver[4] (input: single_value, main-box unit: (none))
Q: £1 = €1.15. Convert £200 to euros.
   - intro: To go from pounds to euros, multiply by the exchange rate 1.15.
   - ask: Write the rate: £1 = €  [box=1.15, NO label]
   - ask: 200 × 1.15 =  [box=230, label:' euros']
   - ask: Check: 230 ÷ 1.15 =  [box=200, label:' pounds']

## silver[5] (input: single_value, main-box unit: (none))
Q: A speed-time graph shows constant speed of 15 m/s for 8 seconds. What is the distance?
   - intro: The line is flat, so the area under it is a rectangle.
   - ask: Write the height (speed):  [box=15, label:' m/s']
   - ask: Area = base × height = 8 × 15 =  [box=120, label:' m']
   - ask: Check: 120 m ÷ 8 s =  [box=15, label:' m/s']

## silver[6] (input: single_value, main-box unit: (none))
Q: 8 km ≈ 5 miles. Convert 40 km to miles.
   - intro: Kilometres are smaller than miles, so the miles number will be smaller. Find the miles in one km first.
   - ask: Miles in 1 km: 5 ÷ 8 =  [box=0.625, label:' miles']
   - ask: 40 km × 0.625 =  [box=25, label:' miles']
   - ask: Check: 25 ÷ 0.625 =  [box=40, label:' km']

## gold[0] (input: single_value, main-box unit: (none))
Q: A speed-time graph: 0→10 m/s in 4 s, constant 10 m/s for 6 s, then 10→0 in 5 s. Find total distance.
   - intro: Distance is the total area. Split the trapezium into two triangles and a rectangle.
   - ask: Speeding-up triangle: ½ × 4 × 10 =  [box=20, label:' m']
   - ask: Steady rectangle: 6 × 10 =  [box=60, label:' m']
   - ask: Slowing-down triangle: ½ × 5 × 10 =  [box=25, label:' m']
   - ask: Total distance = 20 + 60 + 25 =  [box=105, label:' m']
   - ask: Check: total time = 4 + 6 + 5 =  [box=15, label:' s']

## gold[1] (input: single_value, main-box unit: (none))
Q: A car travels at 30 m/s for 10 s then decelerates at 6 m/s². How long until it stops?
   - intro: The 10 s at steady speed does not affect the stopping time. Only the deceleration does.
   - ask: Speed it must lose =  [box=30, label:' m/s']
   - ask: Time = speed ÷ deceleration = 30 ÷ 6 =  [box=5, label:' s']
   - ask: Check: losing 6 m/s each second for 5 s loses 6 × 5 =  [box=30, label:' m/s']

## gold[2] (input: single_value, main-box unit: (none))
Q: A distance-time graph shows: (0,0), (2,40), (3,40), (5,100). What is the speed in the final section (km/h)?
   - intro: Speed on a distance-time graph is the gradient. Use only the final section, from t = 3 to t = 5.
   - ask: Change in distance: 100 − 40 =  [box=60, label:' km']
   - ask: Change in time: 5 − 3 =  [box=2, label:' hours']
   - ask: Speed = 60 ÷ 2 =  [box=30, label:' km/h']
   - ask: Check: 30 km/h for 2 h covers 30 × 2 =  [box=60, label:' km']

## gold[3] (input: single_value, main-box unit: (none))
Q: v8 sarea = 80 mTime (s)Speed (m/s)A speed-time graph shows a car accelerating from rest to speed v in 8 seconds. The distance travelled (the area under the graph) is 80 m. Find v.
   - intro: The distance is the area of the triangle: ½ × base × height. Here the height is the unknown speed v.
   - ask: ½ × 8 =  [box=4, NO label]
   - ask: 4 × v = 80, so v = 80 ÷ 4 =  [box=20, label:' m/s']
   - ask: Check: ½ × 8 × 20 =  [box=80, label:' m']

## gold[4] (input: single_value, main-box unit: (none))
Q: A car accelerates from rest at 4 m/s² for 10 seconds. What is the final speed?
   - intro: Final speed = start speed + acceleration × time. From rest means the start speed is 0.
   - ask: Speed gained = acceleration × time = 4 × 10 =  [box=40, label:' m/s']
   - ask: Final speed = 0 + 40 =  [box=40, label:' m/s']
   - ask: Check: gaining 4 m/s each second for 10 s gives 4 × 10 =  [box=40, label:' m/s']
