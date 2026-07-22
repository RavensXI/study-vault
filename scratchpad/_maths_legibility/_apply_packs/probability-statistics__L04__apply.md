# apply-pack: probability-statistics__L04.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[4] (question stem) | ClassFrequency100-1205120-14010140-160k160-1805 The estimated mean is 140. Find  | fix: Render as a proper two-column table — Class | Frequency: 100-120 -> 5, 120-140 -> 10, 140-160 -> k, 160-180 -> 5.
- [medium] silver[1] (question stem) | ClassFrequency0-10410-201020-306 The grouped frequency table shows a set of valu | fix: Render each as a proper Class/Score | Frequency table (here: 0-10 -> 4, 10-20 -> 10, 20-30 -> 6).
- [medium] silver[0] | Sigma fx = 3 + 10 + 24 + 16 = [box=53, NO label] / Sigma f = 3 + 5 + 8 + 4 = [bo | fix: On first use write it out: 'Sigma fx (the total of the fx column) = ...' and 'Sigma f (the total frequency) = ...'.
- [medium] gold[3] | Midpoint of 10-30 = [box=20, NO label] | fix: Add a build step showing midpoint = (lower bound + upper bound) ÷ 2, e.g. '(10 + 30) ÷ 2 = 20', before (or as) this ask.
- [medium] silver[2] | Midpoint of 0-10 = [box=5, NO label] | fix: Add a one-line build: midpoint = (lower + upper) ÷ 2, i.e. (0 + 10) ÷ 2 = 5.
- [medium] gold[4] | The n terms give 25n − 24n = n; the numbers give 36 − 25 = [box=11, NO label] | fix: Split into two lines and close the loop: 'Collect n terms: 25n − 24n = n. Collect numbers: 36 − 25 = [11]. So n = 11.'
- [medium] silver[6] | Q stem: 'ValueCum. freq&lt;158&lt;2022&lt;2538&lt;3050The median of grouped data | fix: Delete the garbled table prefix and keep only the readable restatement, using real '<' signs: '<15 (8), <20 (22), <25 (38), <30 (50)'.
- [medium] silver[0], silver[2], silver[3], silver[6], gold[0] | Q lines such as 'Value1234Frequency4655Find the mean.', 'Midpoint51525Frequency8 | fix: Render as two clearly separated labelled rows, e.g. 'Values: 1, 2, 3, 4 | Frequencies: 4, 6, 5, 5' (and for grouped data 'Classes: 0-10, 10-20, 20-30 | Frequenc
- [medium] gold[1] | 'After adding, every number averages 21, which is 21 - 20 =' [1] then 'That surp | fix: Reword the middle step to 'The mean rose by 21 - 20 = [1]', then add a bridging step: 'The total extra of 10 is spread as +1 over every number, and there are n 
- [medium] bronze[1] | Check: values below 4 are 2 and 3, that is [box=2] | fix: Reword as an explicit count question: 'How many values are below 4? [box=2]'.
- [medium] gold[4] | Set the mean to 40: (700 + 50k) ÷ (20 + k) = 40. Multiply out: 700 + 50k = 40(20 | fix: Split into explicit steps: first 'Multiply both sides by (20 + k): 700 + 50k = 40 x (20 + k)', then 'Expand the bracket: 40 x (20 + k) = 800 + 40k', before coll

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[1] Q: Find the median of 3, 9, 1, 7, 5.
   step0 field=pre answer=5 text='How many values are in the list?'
   step1 field=pre answer=3 text='Middle position = (5 + 1) ÷ 2 ='
   step2 field=pre answer=5 text='The 3rd value in 1, 3, 5, 7, 9 is'
   step3 field=pre answer=2 text='Check: values below 5 are 1 and 3, that is'

gold[1] Q: The mean of a set of 10 numbers is 12. The mean of the first 6 is 10. Find the mean of the
   step0 field=pre answer=120 text='Total of all 10 numbers = 10 × 12 ='
   step1 field=pre answer=60 text='Total of the first 6 = 6 × 10 ='
   step2 field=pre answer=60 text='Total of the last 4 = 120 − 60 ='
   step3 field=pre answer=15 text='Mean of the last 4 = 60 ÷ 4 ='

gold[3] Q: A data set has mean 20 and range 15. The value 5 is added to every number. What is the new
   step0 field=pre answer=0 text='Adding 5 to every value changes the range by'
   step1 field=pre answer=25 text='New mean = old mean + 5 = 20 + 5 ='
   step2 field=pre answer=25 text='Check: sample values 15, 20, 25 (mean 20) each gain 5 to give 20, 25, 30, mean = 75 ÷ 3 ='

gold[4] Q: ClassFrequency100-1205120-14010140-160k160-1805 The estimated mean is 140. Find \(k\).
   step0 field=pre answer=2700 text='Known part of Σfx: 5×110 + 10×130 + 5×170 = 550 + 1300 + 850 ='
   step1 field=pre answer=20 text='Total known frequency: 5 + 10 + 5 ='
   step2 field=pre answer=100 text='Collect k terms: 150k − 140k = 2800 − 2700, so 10k ='
   step3 field=pre answer=10 text='k = 100 ÷ 10 ='
   step4 field=pre answer=140 text='Check: Σf = 30 and Σfx = 2700 + 1500 = 4200, so mean = 4200 ÷ 30 ='

silver[0] Q: ScoreFrequency13253844 The frequency table shows a set of scores. Find the mean.
   step0 field=pre answer=3 text='Row 1: 1 × 3 ='
   step1 field=pre answer=10 text='Row 2: 2 × 5 ='
   step2 field=pre answer=24 text='Row 3: 3 × 8 ='
   step3 field=pre answer=16 text='Row 4: 4 × 4 ='
   step4 field=pre answer=53 text='Σfx = 3 + 10 + 24 + 16 ='
   step5 field=pre answer=20 text='Σf = 3 + 5 + 8 + 4 ='
   step6 field=pre answer=2.65 text='Mean = 53 ÷ 20 ='

silver[1] Q: ClassFrequency0-10410-201020-306 The grouped frequency table shows a set of values. Estima
   step0 field=pre answer=5 text='Midpoint of 0-10 = (0+10) ÷ 2 ='
   step1 field=pre answer=15 text='Midpoint of 10-20 ='
   step2 field=pre answer=25 text='Midpoint of 20-30 ='
   step3 field=pre answer=320 text='4×5 + 10×15 + 6×25 = 20 + 150 + 150 ='
   step4 field=pre answer=20 text='Total frequency Σf = 4 + 10 + 6 ='
   step5 field=pre answer=16 text='Estimated mean = 320 ÷ 20 ='

silver[2] Q: The mean of 4 numbers is 15. A fifth number is added and the mean becomes 18. What is the 
   step0 field=pre answer=60 text='Original total of the 4 numbers = 4 × 15 ='
   step1 field=pre answer=90 text='New total = 5 × 18 ='
   step2 field=pre answer=30 text='Fifth number = new total − old total = 90 − 60 ='

silver[6] Q: Data set: 2, 5, 5, 7, 8, 12. One more value is added and the median becomes 6. What could 

### board=maths-edexcel
bronze[1] Q: Find the median of: 2, 5, 8, 11, 14
   step0 field=say answer=None text='The median is the middle value once the numbers are in order. This list is already in orde'
   step1 field=pre answer=5 text='How many numbers are in the list?'
   step2 field=pre answer=3 text='The middle position is (5 + 1) ÷ 2 ='
   step3 field=pre answer=8 text='Count along: the 3rd value is'
   step4 field=pre answer=2 text='How many numbers are below 8?'

gold[1] Q: A set of 10 numbers has mean 15. When the largest number (30) is removed, find the new mea
   step0 field=say answer=None text='Turn the mean into a total, take the removed number off, then re-average over the smaller '
   step1 field=pre answer=150 text='Original total = mean × count = 15 × 10 ='
   step2 field=pre answer=120 text='Remove the largest: 150 − 30 ='
   step3 field=pre answer=40 text='Numerator: 120 ÷ 3 ='
   step4 field=pre answer=3 text='Denominator: 9 ÷ 3 ='
   step5 field=pre answer=120 text='40 × 9 ÷ 3 ='

gold[3] Q: ClassFrequency0-10610-301430-5010A teacher needs to estimate the mean from grouped data: 0
   step0 field=say answer=None text='Grouped data: replace each class by its midpoint, then take a frequency-table mean. Watch '
   step1 field=pre answer=5 text='Midpoint of 0-10 ='
   step2 field=pre answer=20 text='Midpoint of 10-30 ='
   step3 field=pre answer=40 text='Midpoint of 30-50 ='
   step4 field=pre answer=710 text='Σfx = 6×5 + 14×20 + 10×40 = 30 + 280 + 400 ='
   step5 field=pre answer=30 text='Σf = 6 + 14 + 10 ='
   step6 field=pre answer=23.67 text='710 ÷ 30 ='
   step7 field=pre answer=710 text='30 + 280 + 400 ='

gold[4] Q: The mean of \(n\) numbers is 24. When one more number (36) is added, the mean becomes 25. 
   step0 field=say answer=None text='Set up two totals. Before, the total is 24n. After adding 36 there are n+1 numbers with me'
   step1 field=pre answer=25 text='Expand the right side: 25 × (n + 1) = 25n +'
   step2 field=pre answer=11 text='The n terms give 25n − 24n = n; the numbers give 36 − 25 ='
   step3 field=pre answer=264 text='Check with n = 11. Before: 24 × 11 ='
   step4 field=pre answer=25 text='Add 36, then share over 12 numbers: 300 ÷ 12 ='

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

silver[1] Q: The mean of 4 numbers is 10. A 5th number (20) is added. Find the new mean.
   step0 field=say answer=None text='Turn the old mean back into a total, add the new number, then re-average.'
   step1 field=pre answer=40 text='Old total = mean × count = 10 × 4 ='
   step2 field=pre answer=60 text='Add the new number: 40 + 20 ='
   step3 field=pre answer=12 text='60 ÷ 5 ='
   step4 field=pre answer=60 text='12 × 5 ='

silver[2] Q: ClassFrequency0-10510-201220-308Grouped data: 0-10 (f=5), 10-20 (f=12), 20-30 (f=8). Estim
   step0 field=say answer=None text='Grouped data: use each class midpoint as a stand-in value, then it is just a frequency-tab'
   step1 field=pre answer=5 text='Midpoint of 0-10 ='
   step2 field=pre answer=15 text='Midpoint of 10-20 ='
   step3 field=pre answer=25 text='Midpoint of 20-30 ='
   step4 field=pre answer=405 text='Σfx = 5×5 + 15×12 + 25×8 = 25 + 180 + 200 ='
   step5 field=pre answer=25 text='Σf = 5 + 12 + 8 ='
   step6 field=pre answer=16.2 text='405 ÷ 25 ='
   step7 field=pre answer=405 text='16.2 × 25 ='

silver[6] Q: ValueCum. freq&lt;158&lt;2022&lt;2538&lt;3050The median of grouped data with 50 values is 
   step0 field=say answer=None text='The median is the 25th value. Walk up the cumulative frequencies until you first pass 25.'
   step1 field=pre answer=22 text='Up to under 20, the running total is'
   step2 field=pre answer=20 text='The lower bound of the 20-25 class ='
   step3 field=pre answer=38 text='The 20-25 class covers positions 23 up to'

### board=maths-ocr
bronze[1] Q: Median of 3, 5, 7, 9, 11.
   step0 field=say answer=None text='Median = the middle value once the list is in order.'
   step1 field=pre answer=5 text='Already in order. How many values?'
   step2 field=pre answer=3 text='The middle position of 5 values is position'
   step3 field=pre answer=7 text='The value in position 3 is'
   step4 field=pre answer=2 text='Check: how many values sit above 7?'

gold[1] Q: The mean of n numbers is 20. When 30 is added, the mean becomes 21. Find n.
   step0 field=say answer=None text='Compare totals. The n originals sit exactly at the old mean, so only the new value adds su'
   step1 field=pre answer=10 text='How far is the new value 30 above the old mean of 20? 30 − 20 ='
   step2 field=pre answer=1 text='After adding, every number averages 21, which is 21 − 20 ='
   step3 field=pre answer=10 text='That surplus of 10 is shared as +1 across all the numbers, so n + 1 ='
   step4 field=pre answer=9 text='So n = 10 − 1 ='
   step5 field=pre answer=21 text='Check: (20 × 9 + 30) ÷ 10 ='

gold[3] Q: Two groups: Group A mean = 65 (20 students). Group B mean = 75 (30 students). Combined mea
   step0 field=say answer=None text='Combine by totals, never by averaging the two means. Rebuild each total first.'
   step1 field=pre answer=1300 text='Group A total = 65 × 20 ='
   step2 field=pre answer=2250 text='Group B total = 75 × 30 ='
   step3 field=pre answer=3550 text='Combined total = 1300 + 2250 ='
   step4 field=pre answer=50 text='Combined count = 20 + 30 ='
   step5 field=pre answer=71 text='Combined mean = 3550 ÷ 50 ='
   step6 field=pre answer=1 text='Check: is 71 between 65 and 75, nearer 75 (the bigger group)? Enter 1 for yes.'

gold[4] Q: A dataset has median 15, Q1 = 10, Q3 = 22. A value of 50 is added. Is 50 an outlier using 
   step0 field=say answer=None text='An outlier lies beyond a fence set 1.5 IQRs past a quartile. Build the upper fence.'
   step1 field=pre answer=12 text='IQR = Q3 − Q1 = 22 − 10 ='
   step2 field=pre answer=18 text='1.5 × IQR = 1.5 × 12 ='
   step3 field=pre answer=40 text='Upper fence = Q3 + 18 = 22 + 18 ='
   step4 field=pre answer=1 text='Is 50 beyond the fence of 40? Enter 1 for yes, 0 for no:'
   step5 field=pre answer=10 text='Check: 50 − 40 ='

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

silver[1] Q: The mean of 5 numbers is 12. A 6th number (24) is added. Find the new mean.
   step0 field=say answer=None text='Rebuild the total, add the new number, then divide by the new count.'
   step1 field=pre answer=60 text='Original total = 12 × 5 ='
   step2 field=pre answer=84 text='New total = 60 + 24 ='
   step3 field=pre answer=6 text='New count = 5 + 1 ='
   step4 field=pre answer=14 text='New mean = 84 ÷ 6 ='
   step5 field=pre answer=84 text='Check: 14 × 6 ='

silver[2] Q: Midpoint51525Frequency8148Find the estimated mean.
   step0 field=say answer=None text='Estimated mean = Σ(midpoint × frequency) ÷ Σf.'
   step1 field=pre answer=40 text='5 × 8 ='
   step2 field=pre answer=210 text='15 × 14 ='
   step3 field=pre answer=200 text='25 × 8 ='
   step4 field=pre answer=450 text='Add those: 40 + 210 + 200 ='
   step5 field=pre answer=30 text='Total frequency: 8 + 14 + 8 ='
   step6 field=pre answer=15 text='Mean = 450 ÷ 30 ='
   step7 field=pre answer=1 text='Check: is 15 between the smallest midpoint 5 and largest 25? Enter 1 for yes.'

silver[6] Q: Value01234Frequency25832Find the median.
   step0 field=say answer=None text='Total the frequencies, find the middle position, then read down the running totals.'
   step1 field=pre answer=20 text='Total frequency: 2 + 5 + 8 + 3 + 2 ='
   step2 field=pre answer=7 text='With 20 values the median averages the 10th and 11th. Running total after value 1: 2 + 5 ='
   step3 field=pre answer=15 text='Running total after value 2: 7 + 8 ='
   step4 field=pre answer=2 text='The 10th and 11th values both fall in this block, so the median value is'
   step5 field=pre answer=1 text='Check: are both the 10th and 11th between positions 8 and 15? Enter 1 for yes.'

### board=maths-eduqas
bronze[1] Q: Find the median of 7, 2, 9, 4, 3.
   step0 field=pre answer=5 text='How many values are in the list?'
   step1 field=pre answer=3 text='Middle position = (5 + 1) ÷ 2 ='
   step2 field=pre answer=4 text='The 3rd value in 2, 3, 4, 7, 9 is'
   step3 field=pre answer=2 text='Check: values below 4 are 2 and 3, that is'

gold[1] Q: The mean of a set of 8 numbers is 15. The mean of the first 5 is 12. Find the mean of the 
   step0 field=pre answer=120 text='Total of all 8 numbers = 8 × 15 ='
   step1 field=pre answer=60 text='Total of the first 5 = 5 × 12 ='
   step2 field=pre answer=60 text='Total of the last 3 = 120 − 60 ='
   step3 field=pre answer=20 text='Mean of the last 3 = 60 ÷ 3 ='

gold[3] Q: A data set has mean 25 and range 12. The value 10 is added to every number. What is the ne
   step0 field=pre answer=0 text='Adding 10 to every value changes the range by'
   step1 field=pre answer=35 text='New mean = old mean + 10 = 25 + 10 ='
   step2 field=pre answer=35 text='Check: sample values 20, 25, 30 (mean 25) each gain 10 to give 30, 35, 40, mean = 105 ÷ 3 '

gold[4] Q: ClassFrequency0-20520-401040-60k60-805 The estimated mean is 40. Find \(k\).
   step0 field=pre answer=700 text='Known part of Σfx: 5×10 + 10×30 + 5×70 = 50 + 300 + 350 ='
   step1 field=pre answer=20 text='Total known frequency: 5 + 10 + 5 ='
   step2 field=pre answer=100 text='Collect k terms: 50k − 40k = 800 − 700, so 10k ='
   step3 field=pre answer=10 text='k = 100 ÷ 10 ='
   step4 field=pre answer=40 text='Check: Σf = 30 and Σfx = 700 + 500 = 1200, so mean = 1200 ÷ 30 ='

silver[0] Q: ScoreFrequency23374654 The frequency table shows a set of scores. Find the mean.
   step0 field=pre answer=6 text='Row 1: 2 × 3 ='
   step1 field=pre answer=21 text='Row 2: 3 × 7 ='
   step2 field=pre answer=24 text='Row 3: 4 × 6 ='
   step3 field=pre answer=20 text='Row 4: 5 × 4 ='
   step4 field=pre answer=71 text='Σfx = 6 + 21 + 24 + 20 ='
   step5 field=pre answer=20 text='Σf = 3 + 7 + 6 + 4 ='
   step6 field=pre answer=3.55 text='Mean = 71 ÷ 20 ='

silver[1] Q: ClassFrequency0-10510-201520-3010 The grouped frequency table shows a set of values. Estim
   step0 field=pre answer=5 text='Midpoint of 0-10 = (0 + 10) ÷ 2 ='
   step1 field=pre answer=15 text='Midpoint of 10-20 ='
   step2 field=pre answer=25 text='Midpoint of 20-30 ='
   step3 field=pre answer=500 text='5×5 + 15×15 + 10×25 = 25 + 225 + 250 ='
   step4 field=pre answer=30 text='Total frequency Σf = 5 + 15 + 10 ='
   step5 field=pre answer=16.7 text='Estimated mean = 500 ÷ 30 = 16.66..., to 1 d.p. ='

silver[2] Q: The mean of 5 numbers is 12. A sixth number is added and the mean becomes 15. What is the 
   step0 field=pre answer=60 text='Original total of the 5 numbers = 5 × 12 ='
   step1 field=pre answer=90 text='New total = 6 × 15 ='
   step2 field=pre answer=30 text='Sixth number = new total − old total = 90 − 60 ='

silver[6] Q: Data: 4, 6, 6, 8, 10, 14. One more value is added and the median becomes 7. What could the
