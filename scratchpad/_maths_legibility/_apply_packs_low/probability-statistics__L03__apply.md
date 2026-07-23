# apply-pack: probability-statistics__L03.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] | Q stem: 'Is it reliable to use the LOBF y = 3x + 10...' | fix: Expand on first use in this stem: 'line of best fit (LOBF)'.
- [low] silver[2] | ask: Check: females who failed = 22 − 12 = 10, males who failed = 28 − 18 = 10,  | fix: Split into simpler steps, or shorten to just the final sum the box needs: 'Check: total who failed = 10 + 10 = [box]'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[3] Q: Is it reliable to use the LOBF \(y = 3x + 10\) (data range \(x = 2\) to \(x = 12\)) to est

silver[2] Q: 120°80°60°?The pie chart has four sectors. Three angles are 120°, 80° and 60°. Find the an
   step0 field=say answer=None text='Every sector of a pie chart adds to 360°.'
   step1 field=pre answer=360 text='How many degrees in a full circle?'
   step2 field=pre answer=200 text='Add the two largest known angles: 120 + 80 ='
   step3 field=pre answer=260 text='Add the third: 200 + 60 ='
   step4 field=pre answer=100 text='Fourth angle = 360 − 260 ='
   step5 field=pre answer=360 text='Check: 120 + 80 + 60 + 100 ='

### board=maths-edexcel
gold[3] Q: 0123453.24.851520Frequency densityxA histogram has class 5-15 with fd = 3.2 and class 15-2
   step0 field=say answer=None text='Frequency = frequency density × class width. Use the 5 to 15 class; ignore the other one.'
   step1 field=pre answer=10 text='Class width for 5 to 15: 15 − 5 ='
   step2 field=pre answer=32 text='Frequency = density × width = 3.2 × 10 ='
   step3 field=pre answer=3.2 text='Check: density = frequency ÷ width = 32 ÷ 10 ='

silver[2] Q: The scatter graph shows maths test scores against time spent revising. Describe the correl

### board=maths-ocr
gold[3] Q: A comparative bar chart shows Year 10 scored 65% and Year 11 scored 72%. What is the perce
   step0 field=say answer=None text='Percentage point difference is simply one percentage minus the other.'
   step1 field=pre answer=72 text='Write the Year 11 percentage:'
   step2 field=pre answer=65 text='Write the Year 10 percentage:'
   step3 field=pre answer=7 text='Difference = 72 − 65 ='
   step4 field=pre answer=72 text='Check: 65 + 7 ='

silver[2] Q: Two-way table: 50 students. 28 male, 22 female. 30 pass, 20 fail. 18 males pass. How many 
   step0 field=say answer=None text='A two-way table splits by two things at once. Total passes minus male passes leaves female'
   step1 field=pre answer=30 text='Total who passed:'
   step2 field=pre answer=18 text='Males who passed:'
   step3 field=pre answer=12 text='Females who passed = 30 − 18 ='
   step4 field=pre answer=20 text='Check: females who failed = 22 − 12 = 10, males who failed = 28 − 18 = 10, total fails ='

### board=maths-eduqas
gold[3] Q: Is it reliable to use the LOBF \(y = 4x + 5\) (data range \(x = 1\) to \(x = 10\)) to esti

silver[2] Q: 100°90°70°? A pie chart has 4 sectors. Three have angles 100°, 90° and 70°. Find the angle
   step0 field=say answer=None text='All sectors of a pie add to 360°. Add the known angles, then subtract from 360.'
   step1 field=pre answer=190 text='Add the first two known angles: 100 + 90 ='
   step2 field=pre answer=260 text='Add the third: 190 + 70 ='
   step3 field=pre answer=100 text='Fourth sector = 360 − 260 ='
   step4 field=pre answer=360 text='Check: 100 + 90 + 70 + 100 ='
