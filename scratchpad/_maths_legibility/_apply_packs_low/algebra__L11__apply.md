# apply-pack: algebra__L11.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[2] intro | Subtract 3 from all three parts of 1 < x + 3 ≤ 6, the same step done to each par | fix: Drop the redundant clause: 'Subtract 3 from all three parts of 1 < x + 3 ≤ 6.' (or 'Subtract 3 from all three parts. Do the same to each part.')
- [low] bronze[3] (Q line) | Q: "−3−2−101234567Closed circle = included, open circle = not included How many  | fix: Put the legend and question on their own line with a break/full stop: "...open circle = not included. How many integers satisfy −2 ≤ x < 6?"
- [low] bronze[6] (Q line) | Q: "0123456789Open circles = ends not included How many integers satisfy 1 < x < | fix: Separate onto its own line: "...ends not included. How many integers satisfy 1 < x < 8?"

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[3] Q: Solve \(5x + 2 \ge 17\). Which is the solution?

bronze[6] Q: Solve \(10 - x < 4\). Which is the solution?

silver[2] Q: Solve \(7 - 3x \ge 1\). Which is the solution?

### board=maths-edexcel
bronze[3] Q: Solve \(4x + 2 \leq 18\)

bronze[6] Q: Solve \(7x + 1 \leq 22\)

silver[2] Q: Solve \(1 < x + 3 \leq 6\). How many integers satisfy this?
   step0 field=say answer=None text='Subtract 3 from all three parts of \\(1 < x + 3 \\leq 6\\), the same step done to each part.'
   step1 field=pre answer=-2 text='Left part: 1 − 3 ='
   step2 field=pre answer=3 text='Right part: 6 − 3 ='
   step3 field=say answer=None text='So the range is \\(-2 < x \\leq 3\\). The left is strict, so −2 is left out; the right includ'
   step4 field=pre answer=-1 text='−2 is excluded, so the smallest integer allowed is'
   step5 field=pre answer=5 text='Count the integers from −1 up to 3 inclusive:'

### board=maths-ocr
bronze[3] Q: −3−2−101234567Closed circle = included, open circle = not included How many integers satis
   step0 field=say answer=None text='List the integers from the low end up to the high end, watching which ends are included.'
   step1 field=pre answer=5 text='−2 has ≤ so it IS included, and 6 has < so it is NOT. The largest integer allowed is'
   step2 field=say answer=None text='So the integers run from −2 up to 5.'
   step3 field=pre answer=8 text='Count −2, −1, 0, 1, 2, 3, 4, 5. How many?'
   step4 field=pre answer=8 text='Quick check using 5 − (−2) + 1 ='

bronze[6] Q: 0123456789Open circles = ends not included How many integers satisfy \(1 < x < 8\)?
   step0 field=say answer=None text='Both ends use strict < , so neither 1 nor 8 is included. List what is left.'
   step1 field=pre answer=2 text='The smallest integer bigger than 1 is'
   step2 field=say answer=None text='The largest integer below 8 is 7. So the list runs 2 to 7.'
   step3 field=pre answer=6 text='Count 2, 3, 4, 5, 6, 7. How many?'
   step4 field=pre answer=6 text='Quick check using 7 − 2 + 1 ='

silver[2] Q: Solve \(3(x - 2) < x + 4\). What is \(x\)?

### board=maths-eduqas
bronze[3] Q: Solve \(3x + 1 > 16\). Which is the solution?

bronze[6] Q: How many integer values of \(n\) satisfy \(2 < n \leq 6\)?
   step0 field=say answer=None text='You want every whole number bigger than 2 but no bigger than 6.'
   step1 field=say answer=None text='2 < n is strict, so 2 itself is left out. Start just above it.'
   step2 field=pre answer=3 text='The smallest integer bigger than 2 is'
   step3 field=pre answer=6 text='n ≤ 6 includes 6, so the largest integer is'
   step4 field=pre answer=4 text='Count the integers from 3 up to 6:'

silver[2] Q: Solve \(2(x + 3) > 10\). Which is the solution?
