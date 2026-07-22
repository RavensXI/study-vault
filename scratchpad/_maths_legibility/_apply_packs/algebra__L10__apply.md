# apply-pack: algebra__L10.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] gold[0]–gold[3] (question stem) | "xyOx²+y²=25x+y=7??Diagram not drawn accuratelySolve \(x + y = 7\) and \(x^2 + y | fix: Strip the concatenated diagram/axis text and render the diagram separately; the stem should begin "Solve x + y = 7 and x² + y² = 25."
- [high] bronze[0]–bronze[7], silver[0-3], silver[5], silver[6] ("set the two right sides equal" intro) | "set the two right sides equal: \(y = x + 3 = y = x^2 + 1\)" | fix: Drop both "y =": write "set the two right sides equal: x + 3 = x² + 1".
- [medium] bronze[0]–bronze[7], silver[0-3], silver[5], silver[6] ("each x gets its y from the line" intro) | "Now each x gets its y from the line \(y = y = x + 3\)" | fix: Remove the duplicated token: "Now each x gets its y from the line y = x + 3".
- [medium] gold[1] | "So 5x² + 4x − 9 = 0. This factorises as (5x + 9)(x − 1) = 0." | fix: Insert a bridging step for the non-monic factorisation (e.g. split the middle term 4x into 9x − 5x, then factor by grouping) instead of asserting the factors.
- [high] silver[0], silver[1], silver[5], silver[6], gold[0], gold[1], gold[2] | Q: xyOx²+y²=13x+y=5??Diagram not drawn accuratelySolve \(x + y = 5\) and \(x^2 + | fix: Strip the run-together diagram debris from the question stem. Render the sketch as a real labelled diagram (or drop it) so the stem reads only: 'Solve x + y = 5
- [medium] gold[0] | Check (3, −2) in the circle: 3² + −2² = [box=13, NO label] | fix: Bracket the negative coordinate: write '3² + (−2)² ='.
- [medium] bronze[0] (recurs across bronze[1]-[7] and every integer-root step) | "...giving (x − 4)(x + 1) = 0." → "First root, x = [box=4, NO label]" / "Second  | fix: Add a bridge line before the root boxes, e.g. 'Set each bracket to zero: x − 4 = 0 and x + 1 = 0', so the sign flip is visible.
- [medium] gold[0] (also gold[1], gold[2]) | xyOx²+y²=10y=2x+1??Diagram not drawn accuratelySolve \(y = 2x + 1\) and \(x^2 +  | fix: Strip the mashed diagram alt-text so the stem reads only 'Solve \(y = 2x + 1\) and \(x^2 + y^2 = 10\). Give the two x-values.' If a diagram is intended, render 

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: Solve \(y = x\) and \(y = x^2\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x = x^2\\). Bring every term to '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=0 text='and the constant becomes'
   step3 field=pre answer=0 text='First root, x ='
   step4 field=pre answer=1 text='Second root, x ='
   step5 field=pre answer=0 text='At x = 0: y ='
   step6 field=pre answer=1 text='At x = 1: y ='
   step7 field=pre answer=0 text='Check in the curve: 0² ='

gold[0] Q: Solve \(y = 2 - x\) and \(y = x^2 - 4\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(2 - x = x^2 - 4\\). Bring every '
   step1 field=pre answer=1 text='The x-term becomes'
   step2 field=pre answer=-6 text='and the constant becomes'
   step3 field=pre answer=-3 text='First root, x ='
   step4 field=pre answer=2 text='Second root, x ='
   step5 field=pre answer=5 text='At x = −3: y ='
   step6 field=pre answer=0 text='At x = 2: y ='
   step7 field=pre answer=5 text='Check in the curve: (−3)² − 4 ='

gold[1] Q: xyOx²+y²=25y=x−1??Diagram not drawn accuratelySolve \(y = x - 1\) and \(x^2 + y^2 = 25\). 
   step0 field=pre answer=-2 text='The middle term of (x − 1)², 2 × (−1), is'
   step1 field=pre answer=2 text='Collect the two x² terms, 1 + 1 ='
   step2 field=pre answer=-24 text='The constant, 1 − 25, becomes'
   step3 field=pre answer=-3 text='First root, x ='
   step4 field=pre answer=4 text='Second root, x ='
   step5 field=pre answer=-4 text='At x = −3: y ='
   step6 field=pre answer=3 text='At x = 4: y ='
   step7 field=pre answer=25 text='Check (−3, −4) in the circle: (−3)² + (−4)² ='

silver[0] Q: Solve \(y = x + 3\) and \(y = x^2 + 1\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x + 3 = x^2 + 1\\). Bring every '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=-2 text='and the constant becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=-1 text='Second root, x ='
   step5 field=pre answer=5 text='At x = 2: y ='
   step6 field=pre answer=2 text='At x = −1: y ='
   step7 field=pre answer=5 text='Check in the curve: 2² + 1 ='

### board=maths-edexcel
bronze[0] Q: Solve \(y = x + 3\) and \(y = x^2 + 1\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(y = x + 3 = y = x^2 + 1\\). Brin'
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=-2 text='and the constant becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=-1 text='Second root, x ='
   step5 field=pre answer=5 text='At x = 2: y ='
   step6 field=pre answer=2 text='At x = −1: y ='
   step7 field=pre answer=5 text='Work out 2² + 1 ='

gold[0] Q: xyOx²+y²=25x+y=7??Diagram not drawn accuratelySolve \(x + y = 7\) and \(x^2 + y^2 = 25\). 
   step0 field=pre answer=-14 text='The middle term, 2 × 7 × (−1), is'
   step1 field=pre answer=2 text='Collect the two x² terms: 1 + 1 ='
   step2 field=pre answer=24 text='The constant, 49 − 25, becomes'
   step3 field=pre answer=3 text='First root, x ='
   step4 field=pre answer=4 text='Second root, x ='
   step5 field=pre answer=4 text='At x = 3: y ='
   step6 field=pre answer=3 text='At x = 4: y ='
   step7 field=pre answer=25 text='Check (3, 4) in the circle: 3² + 4² ='

gold[1] Q: xyOx²+y²=10y=2x+1??Diagram not drawn accuratelySolve \(y = 2x + 1\) and \(x^2 + y^2 = 10\)
   step0 field=pre answer=4 text='The middle term, 2 × 2x × 1, is'
   step1 field=pre answer=5 text='Collect the x² terms: 1 + 4 ='
   step2 field=pre answer=-9 text='The constant, 1 − 10, becomes'
   step3 field=pre answer=1 text='From x − 1 = 0, the first root is x ='
   step4 field=pre answer=-1.8 text='So the second root is x ='
   step5 field=pre answer=3 text='At x = 1: y ='
   step6 field=pre answer=-2.6 text='At x = −1.8: y ='
   step7 field=pre answer=10 text='Check (1, 3) in the circle: 1² + 3² ='

silver[0] Q: Solve \(y = 2x + 1\) and \(y = x^2 + x - 1\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(y = 2x + 1 = y = x^2 + x - 1\\).'
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=-2 text='and the constant becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=-1 text='Second root, x ='
   step5 field=pre answer=5 text='At x = 2: y ='
   step6 field=pre answer=-1 text='At x = −1: y ='
   step7 field=pre answer=5 text='Work out 2² + 1×2 − 1 ='

### board=maths-ocr
bronze[0] Q: Solve \(y = x + 1\) and \(y = x^2 - 2x - 3\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x + 1 = x^2 - 2x - 3\\). Bring e'
   step1 field=pre answer=-3 text='The x-term becomes'
   step2 field=pre answer=-4 text='and the constant becomes'
   step3 field=pre answer=4 text='First root, x ='
   step4 field=pre answer=-1 text='Second root, x ='
   step5 field=pre answer=5 text='At x = 4: y ='
   step6 field=pre answer=0 text='At x = −1: y ='
   step7 field=pre answer=5 text='Work out 4² − 2×4 − 3 ='

gold[0] Q: xyOx²+y²=13x+y=1??Diagram not drawn accuratelySolve \(x + y = 1\) and \(x^2 + y^2 = 13\). 
   step0 field=pre answer=-2 text='The middle term, 2 × 1 × (−1), is'
   step1 field=pre answer=2 text='Collect the two x² terms: 1 + 1 ='
   step2 field=pre answer=-12 text='The constant, 1 − 13, becomes'
   step3 field=pre answer=3 text='First root, x ='
   step4 field=pre answer=-2 text='Second root, x ='
   step5 field=pre answer=-2 text='At x = 3: y ='
   step6 field=pre answer=3 text='At x = −2: y ='
   step7 field=pre answer=13 text='Check (3, −2) in the circle: 3² + −2² ='

gold[1] Q: xyOx²+y²=5y=3x−1??Diagram not drawn accuratelySolve \(y = 3x - 1\) and \(x^2 + y^2 = 5\). 
   step0 field=pre answer=-6 text='The middle term, 2 × 3x × (−1), is'
   step1 field=pre answer=10 text='Collect the x² terms: 1 + 9 ='
   step2 field=pre answer=-4 text='The constant, 1 − 5, becomes'
   step3 field=pre answer=1 text='First root, x ='
   step4 field=pre answer=-0.4 text='From 5x + 2 = 0, the second root is x ='
   step5 field=pre answer=2 text='At x = 1: y ='
   step6 field=pre answer=-2.2 text='At x = −0.4: y ='
   step7 field=pre answer=5 text='Check (1, 2) in the circle: 1² + 2² ='

silver[0] Q: xyOx²+y²=13x+y=5??Diagram not drawn accuratelySolve \(x + y = 5\) and \(x^2 + y^2 = 13\). 
   step0 field=pre answer=-10 text='The middle term, 2 × 5 × (−1), is'
   step1 field=pre answer=2 text='Collect the two x² terms: 1 + 1 ='
   step2 field=pre answer=12 text='The constant, 25 − 13, becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=3 text='Second root, x ='
   step5 field=pre answer=3 text='At x = 2: y ='
   step6 field=pre answer=2 text='At x = 3: y ='
   step7 field=pre answer=13 text='Check (2, 3) in the circle: 2² + 3² ='

### board=maths-eduqas
bronze[0] Q: Solve \(y = x\) and \(y = x^2\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x = x^2\\). Bring every term to '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=0 text='There is no constant, so factor out x. First root, x ='
   step3 field=pre answer=1 text='Second root, x ='
   step4 field=pre answer=0 text='At x = 0: y ='
   step5 field=pre answer=1 text='At x = 1: y ='
   step6 field=pre answer=1 text='Check: 1^2 ='

gold[0] Q: xyOx²+y²=10y=2x+1??Diagram not drawn accuratelySolve \(y = 2x + 1\) and \(x^2 + y^2 = 10\)
   step0 field=pre answer=4 text='The middle term, 2 × 2x × 1, is'
   step1 field=pre answer=5 text='Collect the x² terms: 1 + 4 ='
   step2 field=pre answer=-9 text='The constant, 1 − 10, becomes'
   step3 field=pre answer=1 text='From x − 1 = 0, the first root is x ='
   step4 field=pre answer=-1.8 text='So the second root is x ='
   step5 field=pre answer=3 text='At x = 1: y ='
   step6 field=pre answer=-2.6 text='At x = −1.8: y ='
   step7 field=pre answer=10 text='Check (1, 3) in the circle: 1² + 3² ='

gold[1] Q: xyOx²+y²=13x+y=5??Diagram not drawn accuratelySolve \(x + y = 5\) and \(x^2 + y^2 = 13\). 
   step0 field=pre answer=-10 text='The middle term, 2 × 5 × (−1), is'
   step1 field=pre answer=2 text='Collect the two x² terms: 1 + 1 ='
   step2 field=pre answer=12 text='The constant, 25 − 13, becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=3 text='Second root, x ='
   step5 field=pre answer=3 text='At x = 2: y ='
   step6 field=pre answer=2 text='At x = 3: y ='
   step7 field=pre answer=13 text='Check (2, 3) in the circle: 2² + 3² ='

silver[0] Q: Solve \(y = x + 3\) and \(y = x^2 + 1\). Give the two x-values.
   step0 field=say answer=None text='Both equations give y, so set the two right sides equal: \\(x + 3 = x^2 + 1\\). Bring every '
   step1 field=pre answer=-1 text='The x-term becomes'
   step2 field=pre answer=-2 text='and the constant becomes'
   step3 field=pre answer=2 text='First root, x ='
   step4 field=pre answer=-1 text='Second root, x ='
   step5 field=pre answer=5 text='At x = 2: y ='
   step6 field=pre answer=2 text='At x = -1: y ='
   step7 field=pre answer=5 text='Check: 2^2 + 1 ='
