# apply-pack: ratio-proportion__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] silver[2] | 5 cm5 cm5 cmNot drawn accuratelyA metal cube has sides 5 cm and mass 750 g. | fix: Separate the diagram labels from the sentence so it reads 'A metal cube has sides 5 cm and mass 750 g. Find the density.' (put '5 cm / Not drawn accurately' in 
- [high] gold[1] | 3 cm7 cmNot drawn accuratelyA cylinder has radius 3 cm, height 7 cm, and mass 59 | fix: Separate the labels from the question text (caption the '3 cm / 7 cm / Not drawn accurately').
- [high] gold[4] | 5 cm4 cm2 cmNot drawn accuratelyA 200 g block of metal measures 5 cm × 4 cm × 2  | fix: Separate the labels from the question text (caption '5 cm / 4 cm / 2 cm / Not drawn accurately').
- [medium] gold[0] | Total distance ÷ total time: 300 ÷ 5 = [box=60] | fix: Add a step to total the distances (180 + 120 = 300) and the times (2 + 3 = 5) before dividing.
- [high] gold[1] | Q: 4 cmA cube has side 4 cm and mass 384 g. Find the density.Diagram not drawn a | fix: Delete the leading stray '4 cm' and space it out: 'A cube has side 4 cm and mass 384 g. Find the density. (Diagram not drawn accurately.)'
- [high] gold[2] | Q: 3 cm10 cmA cylinder has radius 3 cm and height 10 cm and mass 848 g. Find the | fix: Delete the leading stray '3 cm10 cm' and space it out: 'A cylinder has radius 3 cm and height 10 cm and mass 848 g. Find the density to 1 d.p. (Diagram not draw

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[0] Q: A train travels 180 km at 90 km/h, then 120 km at 40 km/h. Find the average speed for the 
   step0 field=say answer=None text="Average speed = total distance ÷ total time. Find each leg's time."
   step1 field=pre answer=2 text='Leg 1 time: 180 ÷ 90 ='
   step2 field=pre answer=3 text='Leg 2 time: 120 ÷ 40 ='
   step3 field=pre answer=60 text='Total distance ÷ total time: 300 ÷ 5 ='
   step4 field=pre answer=300 text='Check: 60 × 5 ='

gold[1] Q: 3 cm7 cmNot drawn accuratelyA cylinder has radius 3 cm, height 7 cm, and mass 594 g. Find 
   step0 field=say answer=None text='Density = Mass ÷ Volume. Volume of a cylinder is πr²h.'
   step1 field=pre answer=9 text='Square the radius: 3² ='
   step2 field=pre answer=197.92 text='Volume = π × 9 × 7 = 63π ='
   step3 field=pre answer=3 text='Density: 594 ÷ 197.92 ='
   step4 field=pre answer=594 text='Check: 3 × 197.92 ≈'

gold[2] Q: A car passes point A at 12:15 and point B (60 km away) at 13:00. Find the average speed.
   step0 field=say answer=None text='Speed = Distance ÷ Time. Work out the time as a fraction of an hour.'
   step1 field=pre answer=0.75 text='From 12:15 to 13:00 is 45 minutes. In hours: 45 ÷ 60 ='
   step2 field=pre answer=80 text='Speed: 60 ÷ 0.75 ='
   step3 field=pre answer=60 text='Check: 80 × 0.75 ='

gold[4] Q: 5 cm4 cm2 cmNot drawn accuratelyA 200 g block of metal measures 5 cm × 4 cm × 2 cm. What i
   step0 field=say answer=None text='Density = Mass ÷ Volume. First multiply the three sides for the volume.'
   step1 field=pre answer=40 text='Volume = 5 × 4 × 2 ='
   step2 field=pre answer=5 text='Density: 200 ÷ 40 ='
   step3 field=pre answer=200 text='Check: 5 × 40 ='

silver[2] Q: 5 cm5 cm5 cmNot drawn accuratelyA metal cube has sides 5 cm and mass 750 g. Find the densi
   step0 field=say answer=None text="Density = Mass ÷ Volume. First find the cube's volume."
   step1 field=pre answer=125 text='Volume = 5³ = 5 × 5 × 5 ='
   step2 field=pre answer=6 text='Density: 750 ÷ 125 ='
   step3 field=pre answer=750 text='Check: 6 × 125 ='

### board=maths-edexcel
gold[0] Q: A journey has two parts: 120 km at 60 km/h and 80 km at 80 km/h. Find the overall average 
   step0 field=say answer=None text='Average speed = total distance ÷ total time. You cannot just average 60 and 80, so find ea'
   step1 field=pre answer=2 text='Leg 1 time = 120 ÷ 60 ='
   step2 field=pre answer=1 text='Leg 2 time = 80 ÷ 80 ='
   step3 field=pre answer=200 text='Total distance = 120 + 80 ='
   step4 field=pre answer=3 text='Total time = 2 + 1 ='
   step5 field=pre answer=66.7 text='Average speed = 200 ÷ 3 ='

gold[1] Q: An alloy is made from 300 cm³ of metal A (density 7.2 g/cm³) and 200 cm³ of metal B (densi
   step0 field=say answer=None text="You cannot average the densities. Find each metal's mass, add the masses, add the volumes,"
   step1 field=pre answer=2160 text='Mass of A = 300 × 7.2 ='
   step2 field=pre answer=2260 text='Mass of B = 200 × 11.3 ='
   step3 field=pre answer=4420 text='Total mass = 2160 + 2260 ='
   step4 field=pre answer=500 text='Total volume = 300 + 200 ='
   step5 field=pre answer=8.84 text='Density = 4420 ÷ 500 ='

gold[2] Q: A girl walks 2.4 km in 30 minutes. She then runs 1.6 km in 8 minutes. Find her average spe
   step0 field=say answer=None text='Average speed = total distance ÷ total time, worked in km and hours. Add the distances, ad'
   step1 field=pre answer=4 text='Total distance = 2.4 + 1.6 ='
   step2 field=pre answer=38 text='Total time = 30 + 8 ='
   step3 field=pre answer=240 text='There are 60 minutes in an hour, so scale the distance up: 4 × 60 ='
   step4 field=pre answer=6.3 text='Now divide by the total minutes: 240 ÷ 38 ='

gold[4] Q: A wooden cylinder has density 0.6 g/cm³, radius 5 cm and height 20 cm. Find its mass in gr
   step0 field=say answer=None text="Two stages: find the cylinder's volume, then Mass = Density × Volume. Volume of a cylinder"
   step1 field=pre answer=25 text='First r²: 5 × 5 ='
   step2 field=pre answer=1570 text='Volume = 3.14 × 25 × 20 ='
   step3 field=pre answer=942 text='Mass = 0.6 × 1570 ='
   step4 field=pre answer=0.6 text='Check: 942 ÷ 1570 ='

silver[2] Q: A gold bar has density 19.3 g/cm³ and volume 52 cm³. Find its mass in grams (to 1 d.p.).
   step0 field=say answer=None text='Rearrange to Mass = Density × Volume. The density is 19.3 g/cm³, the volume is 52 cm³.'
   step1 field=pre answer=52 text='First, the volume is'
   step2 field=pre answer=1003.6 text='Multiply: 19.3 × 52 ='
   step3 field=pre answer=19.3 text='Check: 1003.6 ÷ 52 ='

### board=maths-ocr
gold[0] Q: A car travels 60 km at 40 km/h, then 60 km at 60 km/h. Find the average speed for the whol
   step0 field=say answer=None text="Average speed = total distance ÷ total time. Find each leg's time first."
   step1 field=pre answer=1.5 text='Leg 1 time = 60 ÷ 40 ='
   step2 field=pre answer=1 text='Leg 2 time = 60 ÷ 60 ='
   step3 field=pre answer=120 text='Total distance = 60 + 60 ='
   step4 field=pre answer=2.5 text='Total time = 1.5 + 1 ='
   step5 field=pre answer=48 text='Average speed = 120 ÷ 2.5 ='
   step6 field=pre answer=120 text='Check: 48 × 2.5 ='

gold[1] Q: 4 cmA cube has side 4 cm and mass 384 g. Find the density.Diagram not drawn accurately
   step0 field=say answer=None text='Density = mass ÷ volume. First the volume of the cube: side × side × side.'
   step1 field=pre answer=64 text='Volume = 4 × 4 × 4 ='
   step2 field=pre answer=6 text='Density = 384 ÷ 64 ='
   step3 field=pre answer=384 text='Check: 6 × 64 ='

gold[2] Q: 3 cm10 cmA cylinder has radius 3 cm and height 10 cm and mass 848 g. Find the density to 1
   step0 field=say answer=None text='Density = mass ÷ volume. Volume of a cylinder = π × r² × h. Use π ≈ 3.142.'
   step1 field=pre answer=9 text='Square the radius: 3 × 3 ='
   step2 field=pre answer=282.7 text='Volume = π × 9 × 10 = (to 1 d.p.)'
   step3 field=pre answer=3 text='Density = 848 ÷ 282.7 = (to 1 d.p.)'
   step4 field=pre answer=282.7 text='Check: 848 ÷ 3 = (to 1 d.p.)'

gold[4] Q: Convert 15 m/s to km/h.
   step0 field=say answer=None text='m/s to km/h: multiply by 3.6 (each 1 m/s is 3.6 km/h).'
   step1 field=pre answer=15 text='Write the speed to convert:'
   step2 field=pre answer=54 text='15 × 3.6 ='
   step3 field=pre answer=15 text='Check back: 54 ÷ 3.6 ='

silver[2] Q: A car travels 30 km at 60 km/h then 40 km at 80 km/h. Find the total time in hours. Give a
   step0 field=say answer=None text='Total time = time for leg 1 + time for leg 2. Each time = distance ÷ speed.'
   step1 field=pre answer=0.5 text='Leg 1 time = 30 ÷ 60 ='
   step2 field=pre answer=0.5 text='Leg 2 time = 40 ÷ 80 ='
   step3 field=pre answer=1 text='Total time = 0.5 + 0.5 ='
   step4 field=pre answer=30 text='Check leg 1 distance: 60 × 0.5 ='

### board=maths-eduqas
gold[0] Q: A car travels 30 km at 60 km/h then 45 km at 90 km/h. What is the average speed for the wh

gold[1] Q: Two objects: A has density 3 g/cm\(^3\) (volume 100 cm\(^3\)), B has density 5 g/cm\(^3\) 

gold[2] Q: A cube has density \(2.7\text{ g/cm}^3\) and mass 729 g. What is the side length?

gold[4] Q: A stiletto heel has area 1 cm\(^2\) = \(0.0001\text{ m}^2\). A person weighs 600 N on one 

silver[2] Q: A journey takes 2 hours 15 minutes at 80 km/h. How far?
