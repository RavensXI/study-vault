# apply-pack: probability-statistics__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[2] | Q stem: 'ClassFrequency0-10510-201220-308Grouped data: 0-10 (f=5)...' | fix: Strip the flattened table prefix so the stem starts at the clean restatement, or render it as a real table — apply across all four grouped/frequency stems (silv
- [low] bronze[2] | The next most common values each appear how many times? [box=1, NO label] | fix: Reword to 'How many times does the next most common value appear?'
- [low] silver[0], silver[2], gold[0] | intro: 'For a frequency table, mean = Sigma fx / Sigma f' / 'Estimated mean = Si | fix: Define it in words, e.g. 'mean = (add up value x frequency for every row) / (total of the frequencies) - the sign just means "add up"', or drop the sigma symbol
- [low] bronze[7] | Careful: the median is the mean of the 4th and 5th ordered scores, 60 and 65, th | fix: Shorten and signpost the switch: 'A trap to avoid: the median is different from the mode. Median = (60 + 65) / 2 = [box=62.5]'.
- [low] silver[0] | Σfx = 6 + 21 + 24 + 20 = [box=71] | fix: Define the symbol once inline: 'Σfx (the total of the fx column) = 6 + 21 + 24 + 20 = [box]', and 'Σf (the total frequency) = ...'.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: Find the mode of 7, 2, 8, 2, 5, 2, 9.
   step0 field=pre answer=3 text='How many times does 2 appear in 7, 2, 8, 2, 5, 2, 9?'
   step1 field=pre answer=2 text='The mode is the value that appears 3 times:'
   step2 field=pre answer=4 text='How many values appear exactly once (7, 8, 5, 9)?'

bronze[7] Q: Seven students scored: 50, 60, 60, 65, 70, 75, 80. What is the mode?
   step0 field=pre answer=2 text='How many times does 60 appear?'
   step1 field=pre answer=60 text='The mode is'
   step2 field=pre answer=65 text='Careful: the median (4th of the 7 ordered scores) is a different value:'

silver[0] Q: ScoreFrequency13253844 The frequency table shows a set of scores. Find the mean.
   step0 field=pre answer=3 text='Row 1: 1 × 3 ='
   step1 field=pre answer=10 text='Row 2: 2 × 5 ='
   step2 field=pre answer=24 text='Row 3: 3 × 8 ='
   step3 field=pre answer=16 text='Row 4: 4 × 4 ='
   step4 field=pre answer=53 text='Σfx means add up all the value × frequency results: 3 + 10 + 24 + 16 ='
   step5 field=pre answer=20 text='Σf means the total frequency: 3 + 5 + 8 + 4 ='
   step6 field=pre answer=2.65 text='Mean = 53 ÷ 20 ='

silver[2] Q: The mean of 4 numbers is 15. A fifth number is added and the mean becomes 18. What is the 
   step0 field=pre answer=60 text='Original total of the 4 numbers = 4 × 15 ='
   step1 field=pre answer=90 text='New total = 5 × 18 ='
   step2 field=pre answer=30 text='Fifth number = new total − old total = 90 − 60 ='

### board=maths-edexcel
bronze[2] Q: Find the mode of: 3, 5, 5, 7, 8, 5, 9
   step0 field=say answer=None text='The mode is the value that appears most often. Tally how many times each number shows up.'
   step1 field=pre answer=3 text='How many times does 5 appear?'
   step2 field=pre answer=1 text='How many times does 3 appear?'
   step3 field=pre answer=5 text='The value that repeats most is'
   step4 field=pre answer=1 text='The next most common values each appear how many times?'

bronze[7] Q: Find the range of: −3, 5, −1, 7, 2
   step0 field=say answer=None text='Range = largest minus smallest. Take care with the negative numbers.'
   step1 field=pre answer=7 text='Largest value ='
   step2 field=pre answer=-3 text='Smallest value ='
   step3 field=pre answer=10 text='7 − (−3) = 7 + 3 ='
   step4 field=pre answer=7 text='−3 + 10 ='

silver[0] Q: xFrequency14273544Frequency table: x = 1(f=4), 2(f=7), 3(f=5), 4(f=4). Find the mean.
   step0 field=say answer=None text='Mean from a frequency table: multiply each value by its frequency, add those, then divide '
   step1 field=pre answer=4 text='1 × 4 ='
   step2 field=pre answer=14 text='2 × 7 ='
   step3 field=pre answer=15 text='3 × 5 ='
   step4 field=pre answer=16 text='4 × 4 ='
   step5 field=pre answer=49 text='Σfx = 4 + 14 + 15 + 16 ='
   step6 field=pre answer=20 text='Σf = 4 + 7 + 5 + 4 ='
   step7 field=pre answer=2.45 text='49 ÷ 20 ='
   step8 field=pre answer=49 text='2.45 × 20 ='

silver[2] Q: ClassFrequency0-10510-201220-308Grouped data: 0-10 (f=5), 10-20 (f=12), 20-30 (f=8). Estim
   step0 field=say answer=None text='Grouped data: use each class midpoint as a stand-in value, then it is just a frequency-tab'
   step1 field=pre answer=5 text='Midpoint of 0-10 = halfway between the two ends, so (0 + 10) ÷ 2 ='
   step2 field=pre answer=15 text='Midpoint of 10-20 = (10 + 20) ÷ 2 ='
   step3 field=pre answer=25 text='Midpoint of 20-30 = (20 + 30) ÷ 2 ='
   step4 field=pre answer=405 text='Σfx = 5×5 + 15×12 + 25×8 = 25 + 180 + 200 ='
   step5 field=pre answer=25 text='Σf = 5 + 12 + 8 ='
   step6 field=pre answer=16.2 text='405 ÷ 25 ='
   step7 field=pre answer=405 text='16.2 × 25 ='

### board=maths-ocr
bronze[2] Q: Mode of 2, 3, 3, 5, 7, 3, 8.
   step0 field=say answer=None text='Mode = the value that appears most often. Tally each.'
   step1 field=pre answer=3 text='How many times does 3 appear?'
   step2 field=pre answer=0 text='Does any other value appear more than twice? Enter 0 for no.'
   step3 field=pre answer=3 text='So the most frequent value, the mode, is'
   step4 field=pre answer=1 text='Check: is 3 one of the listed values? Enter 1 for yes.'

bronze[7] Q: Range of 12, 5, 8, 3, 15, 7.
   step0 field=say answer=None text='Range = largest − smallest.'
   step1 field=pre answer=15 text='Largest value:'
   step2 field=pre answer=3 text='Smallest value:'
   step3 field=pre answer=12 text='Range = 15 − 3 ='
   step4 field=pre answer=1 text='Check: is 12 less than the largest, 15? Enter 1 for yes.'

silver[0] Q: Value1234Frequency4655Find the mean.
   step0 field=say answer=None text='For a frequency table, mean = Σfx ÷ Σf. Multiply each value by its frequency first.'
   step1 field=pre answer=4 text='1 × 4 ='
   step2 field=pre answer=12 text='2 × 6 ='
   step3 field=pre answer=15 text='3 × 5 ='
   step4 field=pre answer=20 text='4 × 5 ='
   step5 field=pre answer=51 text='Add those: 4 + 12 + 15 + 20 ='
   step6 field=pre answer=20 text='Total frequency: 4 + 6 + 5 + 5 ='
   step7 field=pre answer=2.55 text='Mean = 51 ÷ 20 ='
   step8 field=pre answer=1 text='Check: is 2.55 between the smallest value 1 and largest 4? Enter 1 for yes.'

silver[2] Q: Midpoint51525Frequency8148Find the estimated mean.
   step0 field=say answer=None text='Estimated mean = Σ(midpoint × frequency) ÷ Σf.'
   step1 field=pre answer=40 text='5 × 8 ='
   step2 field=pre answer=210 text='15 × 14 ='
   step3 field=pre answer=200 text='25 × 8 ='
   step4 field=pre answer=450 text='Add those: 40 + 210 + 200 ='
   step5 field=pre answer=30 text='Total frequency: 8 + 14 + 8 ='
   step6 field=pre answer=15 text='Mean = 450 ÷ 30 ='
   step7 field=pre answer=1 text='Check: is 15 between the smallest midpoint 5 and largest 25? Enter 1 for yes.'

### board=maths-eduqas
bronze[2] Q: Find the mode of 3, 7, 3, 9, 5, 3, 8.
   step0 field=pre answer=3 text='How many times does 3 appear in 3, 7, 3, 9, 5, 3, 8?'
   step1 field=pre answer=3 text='The mode is the value that appears 3 times:'
   step2 field=pre answer=4 text='How many values appear exactly once (7, 9, 5, 8)?'

bronze[7] Q: Eight students scored: 45, 52, 52, 60, 65, 70, 75, 80. What is the mode?
   step0 field=pre answer=2 text='How many times does 52 appear?'
   step1 field=pre answer=52 text='The mode is'
   step2 field=pre answer=62.5 text='Careful: the median is the mean of the 4th and 5th ordered scores, 60 and 65, that is (60 '

silver[0] Q: ScoreFrequency23374654 The frequency table shows a set of scores. Find the mean.
   step0 field=pre answer=6 text='Row 1: 2 × 3 ='
   step1 field=pre answer=21 text='Row 2: 3 × 7 ='
   step2 field=pre answer=24 text='Row 3: 4 × 6 ='
   step3 field=pre answer=20 text='Row 4: 5 × 4 ='
   step4 field=pre answer=71 text='Σfx means add up all the value × frequency results: 6 + 21 + 24 + 20 ='
   step5 field=pre answer=20 text='Σf means the total frequency: 3 + 7 + 6 + 4 ='
   step6 field=pre answer=3.55 text='Mean = 71 ÷ 20 ='

silver[2] Q: The mean of 5 numbers is 12. A sixth number is added and the mean becomes 15. What is the 
   step0 field=pre answer=60 text='Original total of the 5 numbers = 5 × 12 ='
   step1 field=pre answer=90 text='New total = 6 × 15 ='
   step2 field=pre answer=30 text='Sixth number = new total − old total = 90 − 60 ='
