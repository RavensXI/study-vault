# apply-pack: probability-statistics__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] silver[1] | Q: text{font-family:Inter,system-ui,sans-serif;fill:currentColor}02460102050Freq | fix: Strip the leaked diagram markup from the stem so it reads only: 'A histogram has bars: 0-10 (fd=2), 10-20 (fd=5), 20-50 (fd=3). Find the total frequency.' (move
- [medium] bronze[3] | Q: 010203040Diagram not drawn accuratelyThe box plot shows min = 10, Q1 = 15, me | fix: Separate the mashed axis labels/caption from the sentence (move them to the diagram). Stem should read: 'The box plot shows min = 10, Q1 = 15, median = 20, Q3 =
- [medium] gold[0] | Q: 1.22.51.80102040Freq densityDiagram not drawn accuratelyThe histogram has cla | fix: Strip the mashed diagram labels. Stem should start: 'The histogram has classes 0-10 (FD 1.2), 10-20 (FD 2.5) and 20-40 (FD 1.8). Find the frequency of the 20-40
- [medium] gold[3] | Q: 426051520Freq densityDiagram not drawn accuratelyThe histogram has classes 0- | fix: Strip the mashed diagram labels. Stem should start: 'The histogram has classes 0-5 (FD 4), 5-15 (FD 2) and 15-20 (FD 6). Find the total frequency.'
- [medium] bronze[2] | The box midpoint would be (18 + 32) ÷ 2 = [box=25] | fix: Add a read step for the right edge before this line, e.g. 'Read the right edge, Q3 = [32]', then use it: '(18 + 32) ÷ 2'.
- [medium] bronze[4] | The IQR would be Q3 − Q1 = 30 − 15 = [box=15] | fix: Either drop this off-topic IQR check, or add read steps for Q1 and Q3 (e.g. 'Read Q3 = [30]', 'Read Q1 = [15]') before using them.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: The box plot shows heights of students. What is the median height?
   step0 field=say answer=None text='The median is the line drawn inside the box.'
   step1 field=pre answer=160 text='Read Q1, the left edge of the box ='
   step2 field=pre answer=175 text='Read Q3, the right edge of the box ='
   step3 field=pre answer=168 text='The median is the line inside the box, between 160 and 175. Read it ='

bronze[3] Q: The cumulative frequency curve shows waiting times for 60 patients. Find Q1.
   step0 field=say answer=None text='Q1 is the lower quartile: a quarter of the way through the data.'
   step1 field=pre answer=60 text='Total patients, n ='
   step2 field=pre answer=15 text='Q1 position = n ÷ 4 = 60 ÷ 4 ='
   step3 field=pre answer=8 text='Read across from cumulative frequency 15 to the curve, then down. Q1 ='

bronze[4] Q: The box plot shows the range of weights. What is the range?
   step0 field=say answer=None text='The range is the full spread: max − min, from whisker end to whisker end.'
   step1 field=pre answer=40 text='Read the left whisker end (minimum) ='
   step2 field=pre answer=80 text='Read the right whisker end (maximum) ='
   step3 field=pre answer=40 text='Range = 80 − 40 ='

gold[0] Q: The histogram shows ages of visitors. Estimate the number of visitors aged between 15 and 
   step0 field=say answer=None text="15 to 25 spans parts of two bars. Find each part's frequency with FD × width, then add."
   step1 field=pre answer=20 text='The 15 to 20 part sits in the 10 to 20 bar (FD 4), width 5. Frequency = 4 × 5 ='
   step2 field=pre answer=15 text='The 20 to 25 part sits in the 20 to 30 bar (FD 3), width 5. Frequency = 3 × 5 ='
   step3 field=pre answer=35 text='Total between 15 and 25 = 20 + 15 ='

gold[3] Q: A histogram: 0-20 (FD=2), 20-30 (FD=5), 30-50 (FD=3). Estimate the median class.

silver[1] Q: The two box plots compare Class A and Class B. Which class performed more consistently?

### board=maths-edexcel
bronze[2] Q: The box plot shows the distribution of heights (cm) of students in a class. What is the me
   step0 field=say answer=None text='A box plot marks five values in order: minimum, Q1, median, Q3, maximum.'
   step1 field=pre answer=160 text='Q1 is the LEFT edge of the box. Read it:'
   step2 field=pre answer=170 text='Q3 is the RIGHT edge of the box. Read it:'
   step3 field=pre answer=165 text='The median is the line INSIDE the box, between the two edges. Read it:'
   step4 field=pre answer=5 text='Check: the median must lie between Q1 and Q3. 170 − 165 ='

bronze[3] Q: The box plot shows the time (in minutes) students spent on homework. What is the interquar
   step0 field=say answer=None text='IQR = Q3 − Q1. Read the two edges of the box.'
   step1 field=pre answer=20 text='Q1 is the left edge:'
   step2 field=pre answer=40 text='Q3 is the right edge:'
   step3 field=pre answer=20 text='IQR = Q3 − Q1 = 40 − 20 ='
   step4 field=pre answer=45 text='Check: the IQR must be smaller than the full range. Range = max − min = 55 − 10 ='

bronze[4] Q: The box plot shows sprint times (seconds) for athletes. What is the range of the data?
   step0 field=say answer=None text='Range = maximum − minimum. Those are the two whisker ends, far left and far right.'
   step1 field=pre answer=10 text='The minimum is the left whisker end:'
   step2 field=pre answer=20 text='The maximum is the right whisker end:'
   step3 field=pre answer=10 text='Range = max − min = 20 − 10 ='
   step4 field=pre answer=6 text='Check: the IQR is Q3 − Q1 = 18 − 12 ='

gold[0] Q: The histogram shows ages of visitors to a museum. Estimate the number of visitors aged bet
   step0 field=say answer=None text='We want ages 15 to 25, which is not a whole bar. It is the top half of the 10 to 20 bar pl'
   step1 field=pre answer=50 text='First the 10 to 20 bar: fd 5 × width 10 ='
   step2 field=pre answer=25 text='We only want 15 to 20, half of that bar: 50 ÷ 2 ='
   step3 field=pre answer=30 text='Now the 20 to 30 bar: fd 3 × width 10 ='
   step4 field=pre answer=15 text='We only want 20 to 25, half of that bar: 30 ÷ 2 ='
   step5 field=pre answer=40 text='Total 15 to 25 = 25 + 15 ='

gold[3] Q: A histogram and a CF curve both represent the same data. The histogram bar 20-30 has fd = 
   step0 field=say answer=None text='First turn the bar into a frequency (fd × width), then express it as a percentage of the t'
   step1 field=pre answer=10 text='Class width = 30 − 20 ='
   step2 field=pre answer=45 text='Frequency = fd × width = 4.5 × 10 ='
   step3 field=pre answer=37.5 text='Percentage = frequency ÷ total × 100 = 45 ÷ 120 × 100 ='
   step4 field=pre answer=45 text='Check: 37.5% of 120 should give back 45. 120 × 0.375 ='

silver[1] Q: text{font-family:Inter,system-ui,sans-serif;fill:currentColor}02460102050Frequency density
   step0 field=say answer=None text="Each bar's frequency = frequency density × class width. Add them up. Watch the last bar's "
   step1 field=pre answer=20 text='Bar 0 to 10: fd 2 × width 10 ='
   step2 field=pre answer=50 text='Bar 10 to 20: fd 5 × width 10 ='
   step3 field=pre answer=30 text='Bar 20 to 50 is wider. Its width = 50 − 20 ='
   step4 field=pre answer=90 text='Bar 20 to 50: fd 3 × width 30 ='
   step5 field=pre answer=160 text='Total frequency = 20 + 50 + 90 ='

### board=maths-ocr
bronze[2] Q: A cumulative frequency graph has a total frequency of 60. What cumulative frequency do you
   step0 field=say answer=None text='The lower quartile Q1 sits a quarter of the way through the data: position n ÷ 4.'
   step1 field=pre answer=60 text='Total values: n ='
   step2 field=pre answer=15 text='Q1 position = n ÷ 4 = 60 ÷ 4 ='
   step3 field=pre answer=15 text='So Q1 is read across from a cumulative frequency of'

bronze[3] Q: 010203040Diagram not drawn accuratelyThe box plot shows min = 10, Q1 = 15, median = 20, Q3
   step0 field=say answer=None text='The interquartile range is the width of the box: Q3 − Q1.'
   step1 field=pre answer=28 text='Read Q3, the right side of the box: Q3 ='
   step2 field=pre answer=15 text='Read Q1, the left side of the box: Q1 ='
   step3 field=pre answer=13 text='IQR = Q3 − Q1 = 28 − 15 ='
   step4 field=pre answer=28 text='Check: 15 + 13 should return Q3, so 15 + 13 ='

bronze[4] Q: 010203040Diagram not drawn accuratelyThe box plot shows min = 10, Q1 = 15, median = 20, Q3
   step0 field=say answer=None text='The range is the full spread, from the lowest value to the highest: max − min.'
   step1 field=pre answer=35 text='Read the maximum, the right whisker end: max ='
   step2 field=pre answer=10 text='Read the minimum, the left whisker end: min ='
   step3 field=pre answer=25 text='Range = max − min = 35 − 10 ='
   step4 field=pre answer=35 text='Check: 10 + 25 should return the maximum, so 10 + 25 ='

gold[0] Q: 1.22.51.80102040Freq densityDiagram not drawn accuratelyThe histogram has classes 0-10 (FD
   step0 field=say answer=None text='Frequency is the area of the bar: frequency density × class width. Mind the wider class.'
   step1 field=pre answer=20 text='Width of the 20 to 40 class: 40 − 20 ='
   step2 field=pre answer=36 text='Frequency = density × width = 1.8 × 20 ='
   step3 field=pre answer=1.8 text='Check: 36 ÷ 20 ='

gold[3] Q: 426051520Freq densityDiagram not drawn accuratelyThe histogram has classes 0-5 (FD 4), 5-1
   step0 field=say answer=None text="Total frequency adds up every bar's area: frequency density × width for each class, then s"
   step1 field=pre answer=20 text='First class 0 to 5 (width 5): 4 × 5 ='
   step2 field=pre answer=20 text='Second class 5 to 15 (width 10): 2 × 10 ='
   step3 field=pre answer=30 text='Third class 15 to 20 (width 5): 6 × 5 ='
   step4 field=pre answer=70 text='Total frequency = 20 + 20 + 30 ='
   step5 field=pre answer=70 text='Check by adding the areas again: 20 + 20 + 30 ='

silver[1] Q: A histogram bar covers the class 0 to 5 with frequency density 3. Find the frequency.
   step0 field=say answer=None text='On a histogram the frequency is the area of the bar: frequency density × class width.'
   step1 field=pre answer=5 text='Class width: 5 − 0 ='
   step2 field=pre answer=15 text='Frequency = density × width = 3 × 5 ='
   step3 field=pre answer=3 text='Check: 15 ÷ 5 ='

### board=maths-eduqas
bronze[2] Q: The box plot shows heights of plants. What is the median height?
   step0 field=pre answer=18 text='Read the left edge, Q1 ='
   step1 field=pre answer=24 text='Read the median line ='
   step2 field=pre answer=25 text='The box midpoint would be (18 + 32) ÷ 2 ='

bronze[3] Q: The cumulative frequency curve shows waiting times for 80 patients. Find Q1 (the lower qua
   step0 field=pre answer=20 text='n ÷ 4 = 80 ÷ 4 ='
   step1 field=pre answer=10 text='Q1 is about'
   step2 field=pre answer=20 text='Check: a quarter of the 80 patients is'

bronze[4] Q: The box plot shows weights of parcels. What is the range?
   step0 field=pre answer=40 text='Read the maximum (right whisker end) ='
   step1 field=pre answer=10 text='Read the minimum (left whisker end) ='
   step2 field=pre answer=30 text='Range = max − min = 40 − 10 ='
   step3 field=pre answer=15 text='The IQR would be Q3 − Q1 = 30 − 15 ='

gold[0] Q: The histogram shows ages of visitors. Estimate the number of visitors aged between 15 and 
   step0 field=pre answer=20 text='15 to 20 is half of the 10 to 20 bar: FD 4 × width 5 ='
   step1 field=pre answer=15 text='20 to 25 is half of the 20 to 30 bar: FD 3 × width 5 ='
   step2 field=pre answer=35 text='Total aged 15 to 25 = 20 + 15 ='
   step3 field=pre answer=40 text='The whole 10 to 20 bar would be 4 × 10 ='

gold[3] Q: A histogram: 0-20 (FD=3), 20-30 (FD=5), 30-50 (FD=2). Estimate the median class.

silver[1] Q: The CF curve shows data for 120 students. Estimate the number of students who scored betwe
   step0 field=pre answer=78 text='Read the cumulative frequency at 60 ='
   step1 field=pre answer=18 text='Read the cumulative frequency at 30 ='
   step2 field=pre answer=60 text='Between 30 and 60 = 78 − 18 ='
   step3 field=pre answer=0.5 text='Check: 60 out of 120 is 60 ÷ 120 ='
