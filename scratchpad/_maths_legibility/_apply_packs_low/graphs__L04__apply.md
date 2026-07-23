# apply-pack: graphs__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[0] | Acceleration = 20 ÷ 10 = ___ m/s² | fix: Insert a step before the division: 'Change in speed = 20 − 0 = ___ m/s', matching the structure of gold[2] and silver[4].
- [low] silver[0] | Check with the trapezium: 1/2 x (top 20 + base 30) x 20 = [box=500, label:'m'] | fix: Add a one-line intro building the formula, e.g. 'A trapezium's area is 1/2 x (short side + long side) x height; here the parallel sides are 20 and 30 and the he
- [low] gold[0] | Check with the trapezium: 1/2 x (top 10 + base 15) x 10 = [box=125, label:'m'] | fix: Either add an intro stating the trapezium area rule 1/2 x (a + b) x height with the two parallel sides named, or drop the trapezium check in favour of re-adding
- [low] gold[4] | Check with the trapezium: 1/2 x (top 6 + base 14) x 20 = [box=200, label:'m'] | fix: Add a short intro defining the trapezium area formula and naming the parallel sides, or replace with a check summing the three taught areas.
- [low] silver[5], gold[3] | Check: 6 + 3 × 8 = [30] / Check: 5 + 2.5 × 8 = [25] | fix: Bracket the multiplication: 'Check: 6 + (3 × 8) =' and 'Check: 5 + (2.5 × 8) ='.
- [low] silver[5] | intro: Deceleration = change in speed ÷ time (given positive). | fix: Reword to: 'Deceleration = change in speed ÷ time (write the answer as a positive number).'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: The speed-time graph shows a car. It accelerates from 0 to 25 m/s in 10 s, then travels at
   step0 field=say answer=None text='The shape is a trapezium: two sloped triangles either side of a rectangle.'
   step1 field=pre answer=125 text='Triangle while speeding up: ½ × 10 × 25 ='
   step2 field=pre answer=500 text='Rectangle at steady speed: 20 × 25 ='
   step3 field=pre answer=62.5 text='Triangle while slowing down: ½ × 5 × 25 ='
   step4 field=pre answer=687.5 text='Total distance = 125 + 500 + 62.5 ='
   step5 field=pre answer=35 text='Check: total time = 10 + 20 + 5 ='

gold[4] Q: Two cyclists start together. Cyclist A travels at 12 km/h. Cyclist B travels at 16 km/h. A
   step0 field=say answer=None text='They travel the same way, so the gap is the difference in how far each goes.'
   step1 field=pre answer=36 text='How far cyclist A goes: 12 × 3 ='
   step2 field=pre answer=48 text='How far cyclist B goes: 16 × 3 ='
   step3 field=pre answer=12 text='Gap between them = 48 − 36 ='
   step4 field=pre answer=12 text='Check: the speed gap is 16 − 12 = 4 km/h, and over 3 h that is 4 × 3 ='

silver[0] Q: The speed-time graph shows a car's journey. What is the acceleration during the first 10 s
   step0 field=say answer=None text='Acceleration is the gradient of a speed-time graph: change in speed ÷ time.'
   step1 field=pre answer=20 text='Read the speed at time = 10 s:'
   step2 field=pre answer=2 text='Acceleration = 20 ÷ 10 ='
   step3 field=pre answer=20 text='Check: 2 m/s² for 10 s gives a speed gain of 2 × 10 ='

silver[5] Q: The speed-time graph shows a constant speed of 15 m/s for 8 seconds. What distance is cove
   step0 field=say answer=None text='The line is flat, so the area under it is a rectangle.'
   step1 field=pre answer=15 text='Write the height (speed):'
   step2 field=pre answer=120 text='Area = base × height = 8 × 15 ='
   step3 field=pre answer=15 text='Check: 120 m ÷ 8 s ='

### board=maths-edexcel
gold[0] Q: A speed-time graph shows: 0–5 s accelerating from 0 to 10 m/s, then 5–15 s at constant 10 
   step0 field=say answer=None text='Distance is the area under a speed-time graph. Split it into a triangle for the speed-up a'
   step1 field=pre answer=25 text='Triangle, 0 to 5 s (speed 0 to 10): ½ × 5 × 10 ='
   step2 field=pre answer=100 text='Rectangle, 5 to 15 s is 10 s at 10 m/s: 10 × 10 ='
   step3 field=say answer=None text='Add the two areas to get the total distance.'
   step4 field=pre answer=125 text='Total distance = 25 + 100 ='
   step5 field=pre answer=125 text='Check with the trapezium: ½ × (top 10 + base 15) × 10 ='

gold[4] Q: A speed-time graph shows: 0–4 s accelerating from 0 to 20 m/s, 4–10 s constant at 20 m/s, 
   step0 field=say answer=None text='Three parts: speed up (triangle), hold (rectangle), slow down (triangle). Find each area.'
   step1 field=pre answer=40 text='Triangle 1, 0 to 4 s: ½ × 4 × 20 ='
   step2 field=pre answer=120 text='Rectangle, 4 to 10 s is 6 s at 20 m/s: 6 × 20 ='
   step3 field=pre answer=40 text='Triangle 2, 10 to 14 s: ½ × 4 × 20 ='
   step4 field=say answer=None text='Add all three areas.'
   step5 field=pre answer=200 text='Total distance = 40 + 120 + 40 ='
   step6 field=pre answer=200 text='Check with the trapezium: ½ × (top 6 + base 14) × 20 ='

silver[0] Q: The speed-time graph shows a car accelerating then travelling at constant speed. Calculate
   step0 field=say answer=None text='Distance is the area under the speed-time graph. Split it into a triangle and a rectangle.'
   step1 field=pre answer=100 text='Triangle, 0 to 10 s (speed 0 to 20): ½ × 10 × 20 ='
   step2 field=pre answer=400 text='Rectangle, 10 to 30 s is 20 s at 20 m/s: 20 × 20 ='
   step3 field=say answer=None text='Add the two areas.'
   step4 field=pre answer=500 text='Total distance = 100 + 400 ='
   step5 field=pre answer=500 text='Check with the trapezium: ½ × (top 20 + base 30) × 20 ='

silver[5] Q: A runner travels 100 m in 12.5 seconds. What is their speed in m/s?
   step0 field=say answer=None text='Speed is distance ÷ time.'
   step1 field=pre answer=100 text='Distance ='
   step2 field=pre answer=12.5 text='Time ='
   step3 field=say answer=None text='Divide distance by time.'
   step4 field=pre answer=8 text='Speed = 100 ÷ 12.5 ='
   step5 field=pre answer=100 text='Check: 8 m/s × 12.5 s ='

### board=maths-ocr
gold[0] Q: A speed-time graph: 0→10 m/s in 4 s, constant 10 m/s for 6 s, then 10→0 in 5 s. Find total
   step0 field=say answer=None text='Distance is the total area. Split the trapezium into two triangles and a rectangle.'
   step1 field=pre answer=20 text='Speeding-up triangle: ½ × 4 × 10 ='
   step2 field=pre answer=60 text='Steady rectangle: 6 × 10 ='
   step3 field=pre answer=25 text='Slowing-down triangle: ½ × 5 × 10 ='
   step4 field=pre answer=105 text='Total distance = 20 + 60 + 25 ='
   step5 field=pre answer=15 text='Check: total time = 4 + 6 + 5 ='

gold[4] Q: A car accelerates from rest at 4 m/s² for 10 seconds. What is the final speed?
   step0 field=say answer=None text='Final speed = start speed + acceleration × time. From rest means the start speed is 0.'
   step1 field=pre answer=40 text='Speed gained = acceleration × time = 4 × 10 ='
   step2 field=pre answer=40 text='Final speed = 0 + 40 ='
   step3 field=pre answer=40 text='Check: gaining 4 m/s each second for 10 s gives 4 × 10 ='

silver[0] Q: A car accelerates from 0 to 25 m/s in 5 seconds. What is the acceleration?
   step0 field=say answer=None text='Acceleration is the gradient of a speed-time graph: change in speed ÷ time.'
   step1 field=pre answer=25 text='Change in speed = 25 − 0 ='
   step2 field=pre answer=5 text='Acceleration = 25 ÷ 5 ='
   step3 field=pre answer=25 text='Check: 5 m/s² for 5 s gains 5 × 5 ='

silver[5] Q: A speed-time graph shows constant speed of 15 m/s for 8 seconds. What is the distance?
   step0 field=say answer=None text='The line is flat, so the area under it is a rectangle.'
   step1 field=pre answer=15 text='Write the height (speed):'
   step2 field=pre answer=120 text='Area = base × height = 8 × 15 ='
   step3 field=pre answer=15 text='Check: 120 m ÷ 8 s ='

### board=maths-eduqas
gold[0] Q: Find the total distance travelled for the entire journey shown in the speed-time graph.
   step0 field=pre answer=40 text='Region 1, triangle (0 to 4 s): ½ × 4 × 20 ='
   step1 field=pre answer=160 text='Region 2, rectangle (4 to 12 s): 8 × 20 ='
   step2 field=pre answer=60 text='Region 3, trapezium (12 to 16 s): ½ × (20 + 10) × 4 ='
   step3 field=say answer=None text='One region left, then add them all.'
   step4 field=pre answer=20 text='Region 4, triangle (16 to 20 s): ½ × 4 × 10 ='
   step5 field=pre answer=280 text='Total = 40 + 160 + 60 + 20 ='
   step6 field=pre answer=20 text='Time check: 4 + 8 + 4 + 4 ='

gold[4] Q: A speed-time graph is a triangle: speed increases from 0 to 30 m/s over 12 seconds, then i
   step0 field=pre answer=360 text='The surrounding rectangle: 12 × 30 ='
   step1 field=say answer=None text='A triangle is half of that rectangle.'
   step2 field=pre answer=180 text='Area = ½ × 360 ='
   step3 field=pre answer=180 text='Or directly: ½ × 12 × 30 ='

silver[0] Q: The speed-time graph shows a car's journey. What is the acceleration during the first 10 s
   step0 field=pre answer=20 text='At 0 s the speed is 0. At 10 s the speed (m/s) ='
   step1 field=say answer=None text='Acceleration = change in speed ÷ time.'
   step2 field=pre answer=2 text='(20 − 0) ÷ 10 ='
   step3 field=pre answer=20 text='Check: 2 × 10 ='

silver[5] Q: A speed-time graph shows a car decelerating from 30 m/s to 6 m/s in 8 seconds. What is the
   step0 field=pre answer=24 text='Change in speed = 30 − 6 ='
   step1 field=say answer=None text='Deceleration = change in speed ÷ time (given positive).'
   step2 field=pre answer=3 text='24 ÷ 8 ='
   step3 field=pre answer=30 text='Check: 6 + 3 × 8 ='
