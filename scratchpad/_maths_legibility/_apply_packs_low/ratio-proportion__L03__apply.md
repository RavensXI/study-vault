# apply-pack: ratio-proportion__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] | New pressure = old pressure × [box=0.5, NO label] | fix: Show the answer as ½ to match the fraction input, or label the box '(a decimal)'.
- [low] silver[0] (also silver[1], silver[4], silver[5]) | intro: Pressure = force ÷ area. Cover P in the triangle to see the divide. | fix: Drop the triangle reference (or add the triangle as a visible diagram); the explicit 'Pressure = force ÷ area' line already carries the step, e.g. 'Pressure = f
- [low] silver[2] | A journey takes 2 hours 15 minutes at 80 km/h. How far? | fix: Rewrite as 'How far does the journey go?'
- [low] bronze[7] | A cyclist travels at 12 m/s. How far in 30 seconds? | fix: Rewrite as 'How far does the cyclist travel in 30 seconds?'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[7] Q: A pressure of 50 N/m² acts on an area of 6 m². Find the force.
   step0 field=say answer=None text='Force = Pressure × Area. Pressure 50 N/m², area 6 m².'
   step1 field=pre answer=300 text='50 × 6 ='
   step2 field=pre answer=50 text='Check: 300 ÷ 6 ='
   step3 field=pre answer=500 text='The same pressure on 10 m² gives 50 × 10 ='

gold[3] Q: An object exerts 500 N on the ground. Doubling the contact area would change the pressure 
   step0 field=say answer=None text='Pressure = Force ÷ Area. The force 500 N stays the same; only the area changes.'
   step1 field=pre answer=2 text='Double the area, so the bottom of Force ÷ Area is multiplied by'
   step2 field=pre answer=0.5 text='Dividing by twice as much halves the result. New pressure = old pressure ×'
   step3 field=pre answer=250 text='Check with numbers: area 1 m² gives 500 ÷ 1 = 500; area 2 m² gives 500 ÷ 2 ='

silver[0] Q: A car travels 90 km in 1 hour 30 minutes. Find the speed in km/h.
   step0 field=say answer=None text='Speed = Distance ÷ Time, but the time must be in hours first.'
   step1 field=pre answer=1.5 text='Change the time: 1 h 30 min ='
   step2 field=pre answer=60 text='Now divide: 90 ÷ 1.5 ='
   step3 field=pre answer=90 text='Check: 60 × 1.5 ='

silver[2] Q: 5 cm5 cm5 cmNot drawn accuratelyA metal cube has sides 5 cm and mass 750 g. Find the densi
   step0 field=say answer=None text="Density = Mass ÷ Volume. First find the cube's volume."
   step1 field=pre answer=125 text='Volume = 5³ = 5 × 5 × 5 ='
   step2 field=pre answer=6 text='Density: 750 ÷ 125 ='
   step3 field=pre answer=750 text='Check: 6 × 125 ='

### board=maths-edexcel
bronze[7] Q: A pressure of 8 N/m² acts over an area of 6 m². Find the force in N.
   step0 field=say answer=None text='Rearrange Pressure = Force ÷ Area to Force = Pressure × Area. The pressure is 8 N/m², the '
   step1 field=pre answer=6 text='First, the area is'
   step2 field=pre answer=48 text='Multiply: 8 × 6 ='
   step3 field=pre answer=8 text='Check: 48 ÷ 6 ='

gold[3] Q: A cuboid block exerts a pressure of 250 N/m² on the floor. Its weight is 500 N. Find the a
   step0 field=say answer=None text='Rearrange Pressure = Force ÷ Area to Area = Force ÷ Pressure. The weight is the force (500'
   step1 field=pre answer=500 text='First, the force (the weight) is'
   step2 field=pre answer=2 text='Now divide: 500 ÷ 250 ='
   step3 field=pre answer=250 text='Check: 500 ÷ 2 ='

silver[0] Q: Convert a speed of 72 km/h to m/s.
   step0 field=say answer=None text='km/h to m/s: divide by 3.6. There are 3600 s in an hour and 1000 m in a km, and 3600 ÷ 100'
   step1 field=pre answer=72 text='First, the speed to convert is'
   step2 field=pre answer=20 text='Now divide: 72 ÷ 3.6 ='
   step3 field=pre answer=72 text='Check by converting back: 20 × 3.6 ='

silver[2] Q: A gold bar has density 19.3 g/cm³ and volume 52 cm³. Find its mass in grams (to 1 d.p.).
   step0 field=say answer=None text='Rearrange to Mass = Density × Volume. The density is 19.3 g/cm³, the volume is 52 cm³.'
   step1 field=pre answer=52 text='First, the volume is'
   step2 field=pre answer=1003.6 text='Multiply: 19.3 × 52 ='
   step3 field=pre answer=19.3 text='Check: 1003.6 ÷ 52 ='

### board=maths-ocr
bronze[7] Q: A journey of 84 miles takes 1.5 hours. What is the speed?
   step0 field=say answer=None text='Speed = distance ÷ time. The distance is 84 miles and the time is 1.5 hours.'
   step1 field=pre answer=1.5 text='Set up the division: 84 ÷'
   step2 field=pre answer=56 text='84 ÷ 1.5 ='
   step3 field=pre answer=84 text='Check: 56 × 1.5 ='

gold[3] Q: A woman of mass 55 kg stands on one heel of area 2 cm² = 0.0002 m². Find the pressure in P
   step0 field=say answer=None text='Pressure = force ÷ area. The force is her weight = mass × g.'
   step1 field=pre answer=550 text='Weight = 55 × 10 ='
   step2 field=pre answer=2750000 text='Pressure = 550 ÷ 0.0002 ='
   step3 field=pre answer=550 text='Check: 2750000 × 0.0002 ='

silver[0] Q: A force of 200 N acts on an area of 4 m². Find the pressure in N/m².
   step0 field=say answer=None text='Pressure = force ÷ area. Cover P in the triangle to see the divide. Force is 200 N, area i'
   step1 field=pre answer=4 text='Set up the division: 200 ÷'
   step2 field=pre answer=50 text='200 ÷ 4 ='
   step3 field=pre answer=200 text='Check: 50 × 4 ='

silver[2] Q: A car travels 30 km at 60 km/h then 40 km at 80 km/h. Find the total time in hours. Give a
   step0 field=say answer=None text='Total time = time for leg 1 + time for leg 2. Each time = distance ÷ speed.'
   step1 field=pre answer=0.5 text='Leg 1 time = 30 ÷ 60 ='
   step2 field=pre answer=0.5 text='Leg 2 time = 40 ÷ 80 ='
   step3 field=pre answer=1 text='Total time = 0.5 + 0.5 ='
   step4 field=pre answer=30 text='Check leg 1 distance: 60 × 0.5 ='

### board=maths-eduqas
bronze[7] Q: A cyclist travels at 12 m/s. How far in 30 seconds?

gold[3] Q: Convert 108 km/h to m/s.

silver[0] Q: A car travels 45 km in 30 minutes. What is its speed in km/h?

silver[2] Q: A journey takes 2 hours 15 minutes at 80 km/h. How far?
