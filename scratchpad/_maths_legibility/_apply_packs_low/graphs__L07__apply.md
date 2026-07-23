# apply-pack: graphs__L07.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[3] | The +1 outside the bracket shifts the curve up. That is the y-component: [box=1] | fix: Reorder so the walk finds the requested x-component first, or add a lead-in such as 'We'll read off both parts; the answer we submit is the x-part' so the order
- [low] silver[4] | Q: The curve y = x^2 is translated by the vector (0, -5). Write the new equation | fix: Drop or demote the first instruction so the box has one clear target, e.g. 'The curve y = x^2 is translated by (0, -5) to give y = x^2 - 5. What is the constant

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
silver[3] Q: \(y = f(2x)\). What is the scale factor of the horizontal stretch?
   step0 field=say answer=None text='The 2 is inside f, so it changes x, and the stretch factor is the reciprocal of 2.'
   step1 field=pre answer=0.5 text='Flip the 2 into a fraction: 1 ÷ 2 ='
   step2 field=pre answer=3 text='Check with a point: x = 6 moves to 6 ÷ 2 ='
   step3 field=pre answer=0.5 text='The width halves, so as a decimal the scale factor is'

silver[4] Q: The point \((4, 3)\) is on \(y = f(x)\). What is the corresponding point on \(y = 2f(x)\)?

### board=maths-edexcel
silver[3] Q: The curve \(y = x^2\) is transformed to \(y = (x - 3)^2 + 1\) by a translation. Give the \
   step0 field=say answer=None text='A translation vector is written as (x-shift, y-shift). Find each part from the equation.'
   step1 field=pre answer=1 text='The +1 outside the bracket shifts the curve up. That is the y-component:'
   step2 field=say answer=None text='Now the horizontal part, from inside the bracket.'
   step3 field=pre answer=3 text='Inside is (x − 3). Inside does the opposite, so the curve moves RIGHT by'
   step4 field=pre answer=3 text='Check: a point at x = 0 on y = x² lands at x ='

silver[4] Q: The graph \(y = f(x)\) passes through \((0, 5)\). What point does \(y = f(x + 2) - 1\) pas
   step0 field=say answer=None text='Two moves. The +2 inside changes x; the −1 outside changes y. We want the y-coordinate, wh'
   step1 field=pre answer=-2 text='The x-part first: +2 inside moves LEFT, so new x = 0 − 2 ='
   step2 field=say answer=None text='Now the y-coordinate, from the −1 outside.'
   step3 field=pre answer=4 text='New y = 5 − 1 ='
   step4 field=pre answer=1 text='Check the drop in y: 5 − 4 ='

### board=maths-ocr
silver[3] Q: The curve \(y = x^2\) is transformed to \(y = (x + 2)^2 + 1\) by a translation. Give the \
   step0 field=say answer=None text='A translation vector is written as (x-shift, y-shift). Find each part from the equation.'
   step1 field=pre answer=1 text='The +1 outside the bracket shifts the curve up. That is the y-component:'
   step2 field=say answer=None text='Now the horizontal part, from inside the bracket.'
   step3 field=pre answer=-2 text='Inside is (x + 2). Inside does the opposite, so the curve moves LEFT, giving x-component'
   step4 field=pre answer=-2 text='Check: a point at x = 0 on y = x² lands at x ='

silver[4] Q: The graph \(y = f(x)\) passes through \((0, 6)\). What point does \(y = f(x + 2) - 2\) pas
   step0 field=say answer=None text='Two moves. The +2 inside changes x; the −2 outside changes y. We want the y-coordinate, wh'
   step1 field=pre answer=-2 text='The x-part first: +2 inside moves LEFT, so new x = 0 − 2 ='
   step2 field=say answer=None text='Now the y-coordinate, from the −2 outside.'
   step3 field=pre answer=4 text='New y = 6 − 2 ='
   step4 field=pre answer=2 text='Check the drop in y: 6 − 4 ='

### board=maths-eduqas
silver[3] Q: \(-f(x)\) is a reflection in which axis?

silver[4] Q: The curve \(y = x^2\) is translated by the vector \(\begin{pmatrix} 0 \\ -5 \end{pmatrix}\
   step0 field=say answer=None text='A translation by the vector (0, −5) shifts the curve straight down by 5. So y = x² becomes'
   step1 field=pre answer=5 text='The curve moves DOWN. By how many units?'
   step2 field=say answer=None text='That amount is subtracted from the whole function.'
   step3 field=pre answer=-5 text='The constant term of y = x² − 5 is'
   step4 field=pre answer=-5 text='Check where the vertex lands: 0 − 5 ='
