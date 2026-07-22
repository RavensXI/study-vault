# maths-edexcel / probability-statistics / L05 - Cumulative Frequency, Box Plots & Histograms

## bronze[0] (input: single_value, main-box unit: (none))
Q: The cumulative frequency curve shows test scores for 80 students. Use the graph to read the median score.
   - intro: 80 students sat a test. The cumulative frequency curve is on the card. To find the median, first find its position.
   - ask: The median is at the n ÷ 2 position. n = 80, so n ÷ 2 =  [box=40, NO label]
   - intro: Now use the graph: go up the cumulative frequency axis to 40, across to the curve, then straight down to the score axis.
   - ask: On this curve, a cumulative frequency of 40 lines up with a score of  [box=40, NO label]
   - ask: Check: the lower quartile Q1 is at n ÷ 4 = 80 ÷ 4 =  [box=20, NO label]

## bronze[1] (input: single_value, main-box unit: (none))
Q: The cumulative frequency curve shows exam marks for 120 students. How many students scored less than 60 marks?
   - intro: Cumulative frequency is a running total: at each score it counts everyone up to there.
   - ask: First read the total: at the highest score (100) the curve reaches  [box=120, NO label]
   - ask: Now 'less than 60': read up from a score of 60 to the curve and across. The cumulative frequency is  [box=80, NO label]
   - ask: Check: those scoring 60 or more = total − 80 = 120 − 80 =  [box=40, NO label]

## bronze[2] (input: single_value, main-box unit: (none))
Q: The box plot shows the distribution of heights (cm) of students in a class. What is the median height?
   - intro: A box plot marks five values in order: minimum, Q1, median, Q3, maximum.
   - ask: Q1 is the LEFT edge of the box. Read it:  [box=160, label:' cm']
   - ask: Q3 is the RIGHT edge of the box. Read it:  [box=170, label:' cm']
   - ask: The median is the line INSIDE the box, between the two edges. Read it:  [box=165, label:' cm']
   - ask: Check: the median must lie between Q1 and Q3. 170 − 165 =  [box=5, NO label]

## bronze[3] (input: single_value, main-box unit: (none))
Q: The box plot shows the time (in minutes) students spent on homework. What is the interquartile range (IQR)?
   - intro: IQR = Q3 − Q1. Read the two edges of the box.
   - ask: Q1 is the left edge:  [box=20, NO label]
   - ask: Q3 is the right edge:  [box=40, NO label]
   - ask: IQR = Q3 − Q1 = 40 − 20 =  [box=20, NO label]
   - ask: Check: the IQR must be smaller than the full range. Range = max − min = 55 − 10 =  [box=45, NO label]

## bronze[4] (input: single_value, main-box unit: (none))
Q: The box plot shows sprint times (seconds) for athletes. What is the range of the data?
   - intro: Range = maximum − minimum. Those are the two whisker ends, far left and far right.
   - ask: The minimum is the left whisker end:  [box=10, label:' s']
   - ask: The maximum is the right whisker end:  [box=20, label:' s']
   - ask: Range = max − min = 20 − 10 =  [box=10, label:' s']
   - ask: Check: the IQR is Q3 − Q1 = 18 − 12 =  [box=6, NO label]

## bronze[5] (input: single_value, main-box unit: (none))
Q: Histogram: class 20-40, frequency = 30. Find the frequency density.
   - intro: Frequency density = frequency ÷ class width. Find the width first.
   - ask: Class width = 40 − 20 =  [box=20, NO label]
   - ask: Frequency density = frequency ÷ width = 30 ÷ 20 =  [box=1.5, NO label]
   - ask: Check: multiply back. fd × width = 1.5 × 20 =  [box=30, NO label]

## bronze[6] (input: single_value, main-box unit: (none))
Q: Box plot: Q1=20, median=28, Q3=36. What percentage of data is between Q1 and Q3?
   - intro: A box plot is split into four equal quarters by Q1, the median and Q3. Each quarter holds 25% of the data.
   - ask: From Q1 up to the median is one quarter, worth  [box=25, label:'%']
   - ask: From the median up to Q3 is another quarter, worth  [box=25, label:'%']
   - ask: Between Q1 and Q3 covers both quarters: 25 + 25 =  [box=50, label:'%']
   - ask: Check: the box is always the middle half of the data. Half of 100% =  [box=50, label:'%']

## bronze[7] (input: single_value, main-box unit: (none))
Q: CF graph shows median = 35 and Q3 = 48. If Q1 = 22, find the IQR.
   - intro: IQR = Q3 − Q1. The median (35) is a distractor here; it plays no part.
   - ask: The upper quartile is Q3 =  [box=48, NO label]
   - ask: The lower quartile is Q1 =  [box=22, NO label]
   - ask: IQR = Q3 − Q1 = 48 − 22 =  [box=26, NO label]
   - ask: Check: Q1 + IQR should return Q3. 22 + 26 =  [box=48, NO label]

## silver[0] (input: multiple_choice, main-box unit: (none))
Q: The box plots compare test scores for Class A and Class B. Which class had the higher median score?

## silver[1] (input: single_value, main-box unit: (none))
Q: text{font-family:Inter,system-ui,sans-serif;fill:currentColor}02460102050Frequency densityValueDiagram not drawn accuratelyA histogram has bars: 0-10 (fd=2), 10-20 (fd=5), 20-50 (fd=3). Find the total frequency.
   - intro: Each bar's frequency = frequency density × class width. Add them up. Watch the last bar's width.
   - ask: Bar 0 to 10: fd 2 × width 10 =  [box=20, NO label]
   - ask: Bar 10 to 20: fd 5 × width 10 =  [box=50, NO label]
   - ask: Bar 20 to 50 is wider. Its width = 50 − 20 =  [box=30, NO label]
   - ask: Bar 20 to 50: fd 3 × width 30 =  [box=90, NO label]
   - ask: Total frequency = 20 + 50 + 90 =  [box=160, NO label]

## silver[2] (input: single_value, main-box unit: (none))
Q: The cumulative frequency curve shows results for 100 students. Use the graph to estimate the interquartile range (IQR).
   - intro: IQR = Q3 − Q1. On a cumulative frequency graph, Q1 is at n ÷ 4 and Q3 is at 3n ÷ 4.
   - ask: Q1 position = n ÷ 4 = 100 ÷ 4 =  [box=25, NO label]
   - ask: Reading across from a cumulative frequency of 25 gives a score of  [box=40, NO label]
   - ask: Q3 position = 3n ÷ 4 = 3 × 100 ÷ 4 =  [box=75, NO label]
   - ask: Reading across from a cumulative frequency of 75 gives a score of  [box=60, NO label]
   - ask: IQR = Q3 − Q1 = 60 − 40 =  [box=20, NO label]

## silver[3] (input: single_value, main-box unit: (none))
Q: The histogram shows the distribution of waiting times at a clinic. How many patients waited between 10 and 20 minutes? (Remember: frequency = frequency density × class width)
   - intro: Frequency = frequency density × class width. Read the bar's height, then multiply by its width.
   - ask: The 10 to 20 bar has a frequency density of  [box=4, NO label]
   - ask: Its class width = 20 − 10 =  [box=10, NO label]
   - ask: Frequency = fd × width = 4 × 10 =  [box=40, NO label]
   - ask: Check: divide back. 40 ÷ 10 =  [box=4, NO label]

## silver[4] (input: single_value, main-box unit: (none))
Q: A histogram class 5-15 has frequency 24. What is the frequency density?
   - intro: Frequency density = frequency ÷ class width. Find the width first.
   - ask: Class width = 15 − 5 =  [box=10, NO label]
   - ask: Frequency density = frequency ÷ width = 24 ÷ 10 =  [box=2.4, NO label]
   - ask: Check: multiply back. 2.4 × 10 =  [box=24, NO label]

## silver[5] (input: multiple_choice, main-box unit: (none))
Q: Box plot A has range 40 and IQR 15. Box plot B has range 25 and IQR 20. Which data set has the greater overall range?

## silver[6] (input: single_value, main-box unit: (none))
Q: A cumulative frequency curve for 60 students gives Q1 = 28 and Q3 = 52. Estimate how many students scored between Q1 and Q3.
   - intro: Between Q1 and Q3 is the middle 50% of the data: Q1 cuts off the bottom 25% and Q3 the top 25%.
   - ask: The fraction of students between Q1 and Q3 =  [box=50, label:'%']
   - ask: Number of students = 50% of 60 = 60 × 0.5 =  [box=30, NO label]
   - ask: Check: 30 students is the middle half, so doubling gives the whole group: 30 × 2 =  [box=60, NO label]

## gold[0] (input: single_value, main-box unit: (none))
Q: The histogram shows ages of visitors to a museum. Estimate the number of visitors aged between 15 and 25. Assume the ages are spread evenly within each class.
   - intro: We want ages 15 to 25, which is not a whole bar. It is the top half of the 10 to 20 bar plus the bottom half of the 20 to 30 bar.
   - ask: First the 10 to 20 bar: fd 5 × width 10 =  [box=50, NO label]
   - ask: We only want 15 to 20, half of that bar: 50 ÷ 2 =  [box=25, NO label]
   - ask: Now the 20 to 30 bar: fd 3 × width 10 =  [box=30, NO label]
   - ask: We only want 20 to 25, half of that bar: 30 ÷ 2 =  [box=15, NO label]
   - ask: Total 15 to 25 = 25 + 15 =  [box=40, NO label]

## gold[1] (input: single_value, main-box unit: (none))
Q: The cumulative frequency curve shows exam results for 200 students. Estimate how many students scored more than 75 marks.
   - intro: 'More than 75' means everyone above 75. Cumulative frequency counts everyone up to 75, so subtract that from the total.
   - ask: The total number of students is  [box=200, NO label]
   - ask: Reading up from a mark of 75 to the curve gives a cumulative frequency of  [box=180, NO label]
   - ask: More than 75 = total − CF at 75 = 200 − 180 =  [box=20, NO label]
   - ask: Check: those scoring 75 or less (180) plus those above (20) =  [box=200, NO label]

## gold[2] (input: single_value, main-box unit: (none))
Q: A box plot has Q1 = 20 and Q3 = 44. An outlier is defined as more than \(1.5 \times \text{IQR}\) beyond the quartiles. Find the lower outlier boundary.
   - intro: An outlier lies more than 1.5 × IQR beyond a quartile. For the LOWER fence: Q1 − 1.5 × IQR. First the IQR.
   - ask: IQR = Q3 − Q1 = 44 − 20 =  [box=24, NO label]
   - ask: 1.5 × IQR = 1.5 × 24 =  [box=36, NO label]
   - ask: Lower fence = Q1 − 1.5 × IQR = 20 − 36 =  [box=-16, NO label]
   - ask: Check: the upper fence would be Q3 + 36 = 44 + 36 =  [box=80, NO label]

## gold[3] (input: single_value, main-box unit: (none))
Q: A histogram and a CF curve both represent the same data. The histogram bar 20-30 has fd = 4.5. Total data = 120. What percentage of data falls in this class?
   - intro: First turn the bar into a frequency (fd × width), then express it as a percentage of the total 120.
   - ask: Class width = 30 − 20 =  [box=10, NO label]
   - ask: Frequency = fd × width = 4.5 × 10 =  [box=45, NO label]
   - ask: Percentage = frequency ÷ total × 100 = 45 ÷ 120 × 100 =  [box=37.5, label:'%']
   - ask: Check: 37.5% of 120 should give back 45. 120 × 0.375 =  [box=45, NO label]

## gold[4] (input: single_value, main-box unit: (none))
Q: Two CF curves show exam results. School A (120 students): median = 58, IQR = 22. School B (80 students): median = 62, IQR = 16. How many students from School A scored above School A's Q3 (which is 69)?
   - intro: Above Q3 is always the top quarter, 25% of that school. Use School A's total of 120. School B's numbers are a distraction.
   - ask: The fraction of data above Q3 =  [box=25, label:'%']
   - ask: School A has this many students:  [box=120, NO label]
   - ask: Students above Q3 = 25% of 120 = 120 × 0.25 =  [box=30, NO label]
   - ask: Check: a quarter of 120 is 120 ÷ 4 =  [box=30, NO label]
