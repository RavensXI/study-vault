# maths-edexcel / graphs / L04 - Real-Life Graphs

## bronze[0] (input: single_value, main-box unit: (none))
Q: The distance-time graph shows a cyclist's journey. What was the cyclist's speed during the first 20 minutes? Give your answer in km per minute.
   - intro: Speed is distance ÷ time. Read both from the graph for the first 20 minutes.
   - ask: Distance at 20 minutes (read up from 20) =  [box=5, label:'km']
   - ask: Time =  [box=20, label:'minutes']
   - intro: Now divide distance by time.
   - ask: Speed = 5 ÷ 20 =  [box=0.25, label:'km/min']
   - ask: Check: 0.25 km/min × 20 min =  [box=5, label:'km']

## bronze[1] (input: single_value, main-box unit: (none))
Q: The distance-time graph shows a walker's journey. How many minutes did the walker rest for?
   - intro: A rest is a flat (horizontal) section: the distance does not change. Find where the line goes flat.
   - ask: The flat part starts at  [box=20, label:'minutes']
   - ask: The flat part ends at  [box=35, label:'minutes']
   - intro: The rest lasts from the start of the flat part to its end.
   - ask: Rest time = 35 − 20 =  [box=15, label:'minutes']
   - ask: Check: 20 + 15 =  [box=35, label:'minutes']

## bronze[2] (input: single_value, main-box unit: (none))
Q: The distance-time graph shows a jogger's morning run. What was the total distance covered?
   - intro: The total distance is the final height of the line. Read the graph at the end, not partway.
   - ask: Distance at 25 minutes =  [box=5, label:'km']
   - ask: Distance at 30 minutes, the very end =  [box=6, label:'km']
   - intro: The journey ends at 30 minutes, so use the final value, not the 25-minute one.
   - ask: Total distance =  [box=6, label:'km']
   - ask: Check: the line rose from 5 km at 25 min to 6 km at 30 min, a rise of 6 − 5 =  [box=1, label:'km']

## bronze[3] (input: single_value, main-box unit: (none))
Q: A car travels 150 km at a constant speed of 50 km/h. How long does the journey take, in hours?
   - intro: Time is distance ÷ speed. The car covers 150 km at 50 km/h.
   - ask: Distance =  [box=150, label:'km']
   - ask: Speed =  [box=50, label:'km/h']
   - intro: Divide the distance by the speed.
   - ask: Time = 150 ÷ 50 =  [box=3, label:'hours']
   - ask: Check: 50 km/h × 3 h =  [box=150, label:'km']

## bronze[4] (input: single_value, main-box unit: (none))
Q: A distance-time graph shows a journey of 20 km taking 4 hours. What is the average speed?
   - intro: Average speed is total distance ÷ total time.
   - ask: Distance =  [box=20, label:'km']
   - ask: Time =  [box=4, label:'hours']
   - intro: Divide distance by time.
   - ask: Average speed = 20 ÷ 4 =  [box=5, label:'km/h']
   - ask: Check: 5 km/h × 4 h =  [box=20, label:'km']

## bronze[5] (input: multiple_choice, main-box unit: (none))
Q: TimeSpeedA speed-time graph rises with a positive gradient, then becomes horizontal. During which section is the object accelerating?

## bronze[6] (input: single_value, main-box unit: (none))
Q: A train travels 180 km in 2 hours. What is its speed in km/h?
   - intro: Speed is distance ÷ time.
   - ask: Distance =  [box=180, label:'km']
   - ask: Time =  [box=2, label:'hours']
   - intro: Divide distance by time.
   - ask: Speed = 180 ÷ 2 =  [box=90, label:'km/h']
   - ask: Check: 90 km/h × 2 h =  [box=180, label:'km']

## bronze[7] (input: single_value, main-box unit: (none))
Q: A cyclist travels at 12 km/h for 2.5 hours. How far do they travel?
   - intro: Distance is speed × time.
   - ask: Speed =  [box=12, label:'km/h']
   - ask: Time =  [box=2.5, label:'hours']
   - intro: Multiply speed by time.
   - ask: Distance = 12 × 2.5 =  [box=30, label:'km']
   - ask: Check: 30 ÷ 2.5 =  [box=12, label:'km/h']

## silver[0] (input: single_value, main-box unit: (none))
Q: The speed-time graph shows a car accelerating then travelling at constant speed. Calculate the total distance covered in 30 seconds. (Hint: distance = area under the graph)
   - intro: Distance is the area under the speed-time graph. Split it into a triangle and a rectangle.
   - ask: Triangle, 0 to 10 s (speed 0 to 20): ½ × 10 × 20 =  [box=100, label:'m']
   - ask: Rectangle, 10 to 30 s is 20 s at 20 m/s: 20 × 20 =  [box=400, label:'m']
   - intro: Add the two areas.
   - ask: Total distance = 100 + 400 =  [box=500, label:'m']
   - ask: Check with the trapezium: ½ × (top 20 + base 30) × 20 =  [box=500, label:'m']

## silver[1] (input: single_value, main-box unit: (none))
Q: A car accelerates from rest to 20 m/s in 10 seconds (straight line on graph). What distance is covered during acceleration?
   - intro: During acceleration the graph is a triangle. The distance is its area.
   - ask: Base of the triangle (the time) =  [box=10, label:'s']
   - ask: Height of the triangle (the top speed) =  [box=20, label:'m/s']
   - intro: Area of a triangle is ½ × base × height.
   - ask: Distance = ½ × 10 × 20 =  [box=100, label:'m']
   - ask: Check: average speed = 20 ÷ 2 = 10 m/s, and 10 × 10 =  [box=100, label:'m']

## silver[2] (input: single_value, main-box unit: (none))
Q: On a distance-time graph, a car travels 60 km in 1 hour, stops for 30 minutes, then travels 40 km in 1 hour. What is the average speed for the whole journey in km/h?
   - intro: Average speed is total distance ÷ total time. Add the moving parts AND the rest.
   - ask: Total distance = 60 + 40 =  [box=100, label:'km']
   - ask: Total time = 1 + 0.5 + 1 =  [box=2.5, label:'hours']
   - intro: Now divide the total distance by the total time.
   - ask: Average speed = 100 ÷ 2.5 =  [box=40, label:'km/h']
   - ask: Check: 40 km/h × 2.5 h =  [box=100, label:'km']

## silver[3] (input: single_value, main-box unit: (none))
Q: A speed-time graph shows constant acceleration from 0 to 30 m/s in 6 seconds. What is the acceleration?
   - intro: Acceleration is the gradient of a speed-time graph: change in speed ÷ time.
   - ask: Change in speed = 30 − 0 =  [box=30, label:'m/s']
   - ask: Time =  [box=6, label:'s']
   - intro: Divide the change in speed by the time.
   - ask: Acceleration = 30 ÷ 6 =  [box=5, label:'m/s²']
   - ask: Check: after 6 s at 5 m/s² the speed rises by 5 × 6 =  [box=30, label:'m/s']

## silver[4] (input: single_value, main-box unit: (none))
Q: The conversion graph shows miles to kilometres. Use it to convert 30 miles to km.
   - intro: A conversion graph turns one unit into another. Find how many km are in an easy number of miles, then scale up.
   - ask: From the graph, 5 miles =  [box=8, label:'km']
   - intro: So every 5 miles is 8 km, and 30 miles is several lots of 5 miles.
   - ask: Number of 5-mile steps in 30 miles: 30 ÷ 5 =  [box=6, NO label]
   - intro: Multiply the km per step by the number of steps.
   - ask: 30 miles = 6 × 8 =  [box=48, label:'km']
   - ask: Check on the graph: read up from 30 miles and across to  [box=48, label:'km']

## silver[5] (input: single_value, main-box unit: (none))
Q: A runner travels 100 m in 12.5 seconds. What is their speed in m/s?
   - intro: Speed is distance ÷ time.
   - ask: Distance =  [box=100, label:'m']
   - ask: Time =  [box=12.5, label:'s']
   - intro: Divide distance by time.
   - ask: Speed = 100 ÷ 12.5 =  [box=8, label:'m/s']
   - ask: Check: 8 m/s × 12.5 s =  [box=100, label:'m']

## silver[6] (input: multiple_choice, main-box unit: (none))
Q: ABTimeDistanceOn a distance-time graph, Section A has gradient 15 and Section B has gradient 25. Which section represents faster movement?

## gold[0] (input: single_value, main-box unit: (none))
Q: A speed-time graph shows: 0–5 s accelerating from 0 to 10 m/s, then 5–15 s at constant 10 m/s. Find the total distance.
   - intro: Distance is the area under a speed-time graph. Split it into a triangle for the speed-up and a rectangle for the steady part.
   - ask: Triangle, 0 to 5 s (speed 0 to 10): ½ × 5 × 10 =  [box=25, label:'m']
   - ask: Rectangle, 5 to 15 s is 10 s at 10 m/s: 10 × 10 =  [box=100, label:'m']
   - intro: Add the two areas to get the total distance.
   - ask: Total distance = 25 + 100 =  [box=125, label:'m']
   - ask: Check with the trapezium: ½ × (top 10 + base 15) × 10 =  [box=125, label:'m']

## gold[1] (input: single_value, main-box unit: (none))
Q: A car decelerates uniformly from 30 m/s to 0 in 12 seconds. What distance does it cover while braking?
   - intro: Distance is the area under the graph. Slowing from 30 m/s to 0 makes a triangle.
   - ask: Base of the triangle (the time) =  [box=12, label:'s']
   - ask: Height of the triangle (the start speed) =  [box=30, label:'m/s']
   - intro: Area of a triangle is ½ × base × height.
   - ask: Distance = ½ × 12 × 30 =  [box=180, label:'m']
   - ask: Check: average speed while braking = 30 ÷ 2 = 15 m/s, and 15 × 12 =  [box=180, label:'m']

## gold[2] (input: single_value, main-box unit: (none))
Q: The distance-time graph shows a delivery driver's complete journey. Calculate the average speed for the whole journey in km/h.
   - intro: Average speed is the total distance divided by the total time, rests included.
   - ask: Total distance (the final height on the graph) =  [box=60, label:'km']
   - ask: Total time (the far right of the time axis) =  [box=2.5, label:'hours']
   - intro: Now divide, and keep the rest periods in the time.
   - ask: Average speed = 60 ÷ 2.5 =  [box=24, label:'km/h']
   - ask: Check: 24 km/h × 2.5 h =  [box=60, label:'km']

## gold[3] (input: single_value, main-box unit: (none))
Q: A speed-time graph shows constant acceleration from 5 m/s to 25 m/s over 8 seconds. Find the acceleration in m/s².
   - intro: Acceleration is the gradient of a speed-time graph: the change in speed divided by the time.
   - ask: Change in speed = 25 − 5 =  [box=20, label:'m/s']
   - ask: Time taken =  [box=8, label:'s']
   - intro: Divide the change in speed by the time.
   - ask: Acceleration = 20 ÷ 8 =  [box=2.5, label:'m/s²']
   - ask: Check: after 8 s at 2.5 m/s² the speed rises by 2.5 × 8 =  [box=20, label:'m/s']

## gold[4] (input: single_value, main-box unit: (none))
Q: A speed-time graph shows: 0–4 s accelerating from 0 to 20 m/s, 4–10 s constant at 20 m/s, 10–14 s decelerating to 0. Find the total distance.
   - intro: Three parts: speed up (triangle), hold (rectangle), slow down (triangle). Find each area.
   - ask: Triangle 1, 0 to 4 s: ½ × 4 × 20 =  [box=40, label:'m']
   - ask: Rectangle, 4 to 10 s is 6 s at 20 m/s: 6 × 20 =  [box=120, label:'m']
   - ask: Triangle 2, 10 to 14 s: ½ × 4 × 20 =  [box=40, label:'m']
   - intro: Add all three areas.
   - ask: Total distance = 40 + 120 + 40 =  [box=200, label:'m']
   - ask: Check with the trapezium: ½ × (top 6 + base 14) × 20 =  [box=200, label:'m']
