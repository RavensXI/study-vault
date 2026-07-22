# apply-pack: graphs__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[1] | Check: the mean of 8 and 5.7 would be about 6.9, but total ÷ total gives ___ m/s | fix: Either add two steps that compute each leg speed first (200 ÷ 25 = 8 m/s, 200 ÷ 35 ≈ 5.7 m/s), or reword the check to use only numbers already on the page, e.g.
- [medium] bronze[5] | Q: TimeSpeedA speed-time graph rises with a positive gradient, then becomes hori | fix: Strip the axis-label artifact so the stem reads: 'A speed-time graph rises with a positive gradient, then becomes horizontal. During which section is the object
- [medium] silver[6] | Q: ABTimeDistanceOn a distance-time graph, Section A has gradient 15 and Section | fix: Strip the run-together labels so the stem reads: 'On a distance-time graph, Section A has gradient 15 and Section B has gradient 25. Which section represents fa
- [high] gold[3] | Q: v8 sarea = 80 mTime (s)Speed (m/s)A speed-time graph shows a car accelerating | fix: Strip the garbled prefix so the stem reads only: 'A speed-time graph shows a car accelerating from rest to speed v in 8 seconds. The distance travelled (the are
- [medium] gold[1] | Q: shows a car speed up from 0 to 15 m/s over the first 5 seconds, hold 15 m/s u | fix: Reword to: 'A car speeds up from 0 to 15 m/s in the first 5 seconds, stays at 15 m/s until 15 seconds, then slows to 0 by 20 seconds. Find the total distance.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[5] Q: A train covers 240 km at 80 km/h. How many hours does it take?
   step0 field=say answer=None text='Time = distance ÷ speed.'
   step1 field=pre answer=240 text='Write the distance:'
   step2 field=pre answer=3 text='Divide by the speed: 240 ÷ 80 ='
   step3 field=pre answer=240 text='Check: 80 km/h × 3 h ='

gold[1] Q: A runner completes a 400 m lap. The first 200 m takes 25 s, and the second 200 m takes 35 
   step0 field=say answer=None text='Average speed always uses the totals, never the mean of the two separate speeds.'
   step1 field=pre answer=400 text='Total distance = 200 + 200 ='
   step2 field=pre answer=60 text='Total time = 25 + 35 ='
   step3 field=pre answer=6.7 text='Average speed = 400 ÷ 60 ='
   step4 field=pre answer=6.7 text='Check: the mean of 8 and 5.7 would be about 6.9, but total ÷ total gives'

gold[3] Q: The speed-time graph shows a trapezium: speed rises from 0 to 20 m/s in 4 s, stays at 20 m
   step0 field=say answer=None text='The trapezium splits into two triangles and a rectangle.'
   step1 field=pre answer=40 text='Triangle while speeding up: ½ × 4 × 20 ='
   step2 field=pre answer=120 text='Rectangle at steady speed: 6 × 20 ='
   step3 field=pre answer=20 text='Triangle while slowing down: ½ × 2 × 20 ='
   step4 field=pre answer=180 text='Total distance = 40 + 120 + 20 ='
   step5 field=pre answer=12 text='Check: total time = 4 + 6 + 2 ='

silver[6] Q: The speed-time graph shows a car accelerating from 0 to 24 m/s in 8 seconds. Find the dist
   step0 field=say answer=None text='The line is a straight slope from 0, so the area under it is a triangle.'
   step1 field=pre answer=24 text='The base is 8 s and the height is'
   step2 field=pre answer=96 text='Area = ½ × base × height = ½ × 8 × 24 ='
   step3 field=pre answer=96 text='Check: average speed = (0 + 24) ÷ 2 = 12 m/s, so 12 × 8 ='

### board=maths-edexcel
bronze[5] Q: TimeSpeedA speed-time graph rises with a positive gradient, then becomes horizontal. Durin

gold[1] Q: A car decelerates uniformly from 30 m/s to 0 in 12 seconds. What distance does it cover wh
   step0 field=say answer=None text='Distance is the area under the graph. Slowing from 30 m/s to 0 makes a triangle.'
   step1 field=pre answer=12 text='Base of the triangle (the time) ='
   step2 field=pre answer=30 text='Height of the triangle (the start speed) ='
   step3 field=say answer=None text='Area of a triangle is ½ × base × height.'
   step4 field=pre answer=180 text='Distance = ½ × 12 × 30 ='
   step5 field=pre answer=180 text='Check: average speed while braking = 30 ÷ 2 = 15 m/s, and 15 × 12 ='

gold[3] Q: A speed-time graph shows constant acceleration from 5 m/s to 25 m/s over 8 seconds. Find t
   step0 field=say answer=None text='Acceleration is the gradient of a speed-time graph: the change in speed divided by the tim'
   step1 field=pre answer=20 text='Change in speed = 25 − 5 ='
   step2 field=pre answer=8 text='Time taken ='
   step3 field=say answer=None text='Divide the change in speed by the time.'
   step4 field=pre answer=2.5 text='Acceleration = 20 ÷ 8 ='
   step5 field=pre answer=20 text='Check: after 8 s at 2.5 m/s² the speed rises by 2.5 × 8 ='

silver[6] Q: ABTimeDistanceOn a distance-time graph, Section A has gradient 15 and Section B has gradie

### board=maths-ocr
bronze[5] Q: A conversion graph shows 5 miles ≈ 8 km. Use it to convert 15 miles to kilometres.
   step0 field=say answer=None text='Miles are bigger than kilometres, so the km number will be larger. Find the km in one mile'
   step1 field=pre answer=1.6 text='Kilometres in 1 mile: 8 ÷ 5 ='
   step2 field=pre answer=24 text='15 miles × 1.6 ='
   step3 field=pre answer=15 text='Check: 24 ÷ 1.6 ='

gold[1] Q: A car travels at 30 m/s for 10 s then decelerates at 6 m/s². How long until it stops?
   step0 field=say answer=None text='The 10 s at steady speed does not affect the stopping time. Only the deceleration does.'
   step1 field=pre answer=30 text='Speed it must lose ='
   step2 field=pre answer=5 text='Time = speed ÷ deceleration = 30 ÷ 6 ='
   step3 field=pre answer=30 text='Check: losing 6 m/s each second for 5 s loses 6 × 5 ='

gold[3] Q: v8 sarea = 80 mTime (s)Speed (m/s)A speed-time graph shows a car accelerating from rest to
   step0 field=say answer=None text='The distance is the area of the triangle: ½ × base × height. Here the height is the unknow'
   step1 field=pre answer=4 text='½ × 8 ='
   step2 field=pre answer=20 text='4 × v = 80, so v = 80 ÷ 4 ='
   step3 field=pre answer=80 text='Check: ½ × 8 × 20 ='

silver[6] Q: 8 km ≈ 5 miles. Convert 40 km to miles.
   step0 field=say answer=None text='Kilometres are smaller than miles, so the miles number will be smaller. Find the miles in '
   step1 field=pre answer=0.625 text='Miles in 1 km: 5 ÷ 8 ='
   step2 field=pre answer=25 text='40 km × 0.625 ='
   step3 field=pre answer=40 text='Check: 25 ÷ 0.625 ='

### board=maths-eduqas
bronze[5] Q: A walker covers 4 km in 1 hour. What is their speed in km per minute? Give your answer to 
   step0 field=pre answer=60 text='Minutes in one hour ='
   step1 field=say answer=None text='Speed per minute = distance ÷ number of minutes.'
   step2 field=pre answer=0.067 text='4 ÷ 60 = (3 d.p.)'
   step3 field=pre answer=4 text='Check: 0.067 × 60 ≈'

gold[1] Q: A speed-time graph shows a car speed up from 0 to 15 m/s over the first 5 seconds, hold 15
   step0 field=pre answer=37.5 text='Triangle (0 to 5 s): ½ × 5 × 15 ='
   step1 field=pre answer=150 text='Rectangle (5 to 15 s): 10 × 15 ='
   step2 field=say answer=None text='One triangle left, then total.'
   step3 field=pre answer=37.5 text='Triangle (15 to 20 s): ½ × 5 × 15 ='
   step4 field=pre answer=225 text='Total = 37.5 + 150 + 37.5 ='
   step5 field=pre answer=20 text='Time check: 5 + 10 + 5 ='

gold[3] Q: A speed-time graph shows constant acceleration from 5 m/s to 25 m/s over 8 seconds. What i
   step0 field=pre answer=20 text='Change in speed = 25 − 5 ='
   step1 field=say answer=None text='Acceleration = change in speed ÷ time.'
   step2 field=pre answer=2.5 text='20 ÷ 8 ='
   step3 field=pre answer=25 text='Check: 5 + 2.5 × 8 ='

silver[6] Q: A conversion graph shows that 1 inch = 2.54 cm. How many cm is 8 inches?
   step0 field=pre answer=2.54 text='Centimetres in one inch ='
   step1 field=say answer=None text='Multiply the number of inches by 2.54.'
   step2 field=pre answer=20.32 text='8 × 2.54 ='
   step3 field=pre answer=8 text='Check: 20.32 ÷ 2.54 ='
