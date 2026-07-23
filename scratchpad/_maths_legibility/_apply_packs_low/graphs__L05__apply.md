# apply-pack: graphs__L05.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[4] | Write it out: 5 × 5 = [25] ... First see the trap route: 5 × 2 = [10] ... type t | fix: Reorder or reword so the trap route is not labelled "First", e.g. present the trap route before the correct one, or change to "Now spot the common trap: 5 × 2 =
- [low] gold[4] step 1 (box=1) | Multiply both sides by x. The left becomes 1, so 4x² = [box=1] | fix: Split it out: 'Multiply both sides by x. The left (1/x × x) becomes 1; the right (4x × x) becomes 4x². So 1 = 4x², i.e. 4x² = [box].'
- [low] silver[2] | The equation becomes 5 = k ÷ 3. Read off the y value on the left: [box=5] | fix: Reword to 'The number on the left of the equation is [box]' and drop the reintroduced 'y value' phrasing.
- [low] silver[5] | Write it out: 5² = 5 × 5. Read the base being multiplied: [box=5] ... Check it i | fix: Change the first step to 'The number being multiplied is [box]' and spell out the final step as 'so 5 × 5 = [box]'.
- [low] bronze[0], step 3 | Count them back, 2 × 2 × 2 = [box=8, NO label] | fix: Reword to 'Now all three 2s together: 2 × 2 × 2 =' (no unit needed — it is a y-value).

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: For \(y = x^3\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text='Cubing means multiplying the number by itself three times.'
   step1 field=pre answer=4 text='First two 2s: 2 × 2 ='
   step2 field=pre answer=8 text='Now the third 2: 4 × 2 ='
   step3 field=pre answer=8 text='Count them back, 2 × 2 × 2 ='

gold[4] Q: For \(y = x^3 - 12x\), find the two values of \(x\) where \(y = 0\) (other than \(x = 0\))
   step0 field=say answer=None text='Set y = 0 and factorise: x³ − 12x = x(x² − 12) = 0. One root is x = 0; the others come fro'
   step1 field=pre answer=12 text='Rearrange x² − 12 = 0 to get x² ='
   step2 field=pre answer=3.46 text='Square-root 12 on a calculator, to 2 decimal places: √12 ='
   step3 field=pre answer=-3.46 text='There are two roots, one + and one −. The negative one is'

silver[2] Q: For \(y = \frac{-8}{x}\), find \(y\) when \(x = 4\).
   step0 field=say answer=None text='Divide, keeping the negative sign on top.'
   step1 field=pre answer=2 text='Ignore signs first: 8 ÷ 4 ='
   step2 field=pre answer=-2 text='Negative ÷ positive is negative, so y ='
   step3 field=pre answer=-8 text='Check: (−2) × 4 ='

silver[4] Q: For \(y = 5^x\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text='A power of 2 means multiply the base by itself once.'
   step1 field=pre answer=25 text='Write it out: 5 × 5 ='
   step2 field=pre answer=10 text='First see the trap route: 5 × 2 ='
   step3 field=pre answer=25 text='The power route is correct, so type the real y:'

silver[5] Q: For \(y = x^3 + 1\), find \(y\) when \(x = -2\).
   step0 field=say answer=None text='Cube the negative first, then add 1.'
   step1 field=pre answer=-8 text='Cube (−2): (−2) × (−2) × (−2) ='
   step2 field=pre answer=-7 text='Add 1: −8 + 1 ='
   step3 field=pre answer=-7 text='Confirm the sign stayed negative, so y ='

### board=maths-edexcel
bronze[0] Q: What is the value of \(y\) when \(x = 2\) on the graph \(y = x^3\)?
   step0 field=say answer=None text='Reading a value off a curve just means substituting the x into the equation. Here \\(y = x^'
   step1 field=pre answer=4 text='Square it first: 2 × 2 ='
   step2 field=pre answer=8 text='Now the third 2: 4 × 2 ='
   step3 field=pre answer=8 text='Check by counting the copies, 2 × 2 × 2 ='

gold[4] Q: The graphs \(y = \frac{1}{x}\) and \(y = 4x\) intersect in the first quadrant. Find the \(
   step0 field=say answer=None text='At an intersection both curves share the same y, so set them equal: \\(\\frac{1}{x} = 4x\\).'
   step1 field=pre answer=1 text='Multiply both sides by x. The left becomes 1, so 4x² ='
   step2 field=pre answer=0.25 text='Divide by 4: x² = 1 ÷ 4 ='
   step3 field=pre answer=0.5 text='Square root (positive, first quadrant): x = √0.25 ='
   step4 field=pre answer=2 text='Check both curves match at x = 0.5: 1 ÷ 0.5 ='

silver[2] Q: For the graph \(y = \frac{6}{x}\), find \(y\) when \(x = -2\).
   step0 field=say answer=None text='In \\(y = \\frac{6}{x}\\) divide the 6 on top by x = -2, minding the sign.'
   step1 field=pre answer=6 text='The number on top of the fraction is'
   step2 field=pre answer=-3 text='Divide by x = -2: 6 ÷ (-2) ='
   step3 field=pre answer=6 text='Check by reversing it: (-3) × (-2) ='

silver[4] Q: Which quadrants does the graph of \(y = -\frac{1}{x}\) sit in?

silver[5] Q: A substance decays according to \(y = 100 \times 0.5^x\). Find \(y\) when \(x = 3\).
   step0 field=say answer=None text='Cube the 0.5 first, then multiply by 100. A base under 1 makes the value shrink each step:'
   step1 field=pre answer=0.25 text='First pair: 0.5 × 0.5 ='
   step2 field=pre answer=0.125 text='Third one: 0.25 × 0.5 ='
   step3 field=pre answer=12.5 text='Now × 100: 0.125 × 100 ='
   step4 field=pre answer=12.5 text='Check it is decay: 100 halves to 50, to 25, to'

### board=maths-ocr
bronze[0] Q: For \(y = x^3\), find \(y\) when \(x = 3\).
   step0 field=say answer=None text='Reading a value off the curve means substituting x into the equation. Here y = x³ with x ='
   step1 field=pre answer=9 text='Square it first: 3 × 3 ='
   step2 field=pre answer=27 text='Now the third 3: 9 × 3 ='
   step3 field=pre answer=27 text='Check by counting the copies: 3 × 3 × 3 ='

gold[4] Q: For \(y = x^3 + x^2 - 6x\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text='Work out the three terms of x³ + x² − 6x at x = 2, then combine.'
   step1 field=pre answer=8 text='The cube: 2³ ='
   step2 field=pre answer=4 text='The square: 2² ='
   step3 field=pre answer=12 text='The −6x term: 6 × 2 ='
   step4 field=pre answer=0 text='Combine: 8 + 4 − 12 ='

silver[2] Q: \(y = \frac{k}{x}\) passes through \((3, 5)\). Find \(k\).
   step0 field=say answer=None text='The point (3, 5) means x = 3 gives y = 5. Put those into y = k/x.'
   step1 field=pre answer=5 text='The equation becomes 5 = k ÷ 3. Read off the y value on the left:'
   step2 field=pre answer=15 text='Multiply both sides by 3 to free k: k = 5 × 3 ='
   step3 field=pre answer=5 text='Check: k ÷ x = 15 ÷ 3 ='

silver[4] Q: Which equation matches a graph that decays toward 0 as x increases?

silver[5] Q: For \(y = 5^x\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text="y = 5ˣ means multiply 5 by itself x times, so 5² is two 5's."
   step1 field=pre answer=5 text='Write it out: 5² = 5 × 5. Read the base being multiplied:'
   step2 field=pre answer=25 text="Now multiply the two 5's: 5 × 5 ="
   step3 field=pre answer=25 text="Check it is not 5 × 2: two 5's give"

### board=maths-eduqas
bronze[0] Q: For \(y = x^3\), find \(y\) when \(x = 2\).
   step0 field=say answer=None text='Cubing means multiplying the number by itself three times.'
   step1 field=pre answer=4 text='First two 2s: 2 × 2 ='
   step2 field=pre answer=8 text='Now the third 2: 4 × 2 ='
   step3 field=pre answer=8 text='Count them back, 2 × 2 × 2 ='

gold[4] Q: The graph \(y = \frac{a}{x}\) passes through \((4, -2)\). Find \(a\).
   step0 field=say answer=None text='Substitute the point (4, −2) into y = a/x, which gives −2 = a ÷ 4.'
   step1 field=pre answer=-8 text='To undo the ÷ 4, multiply both sides by 4. Left side: −2 × 4 ='
   step2 field=pre answer=-8 text='So a ='
   step3 field=pre answer=-2 text='Check: −8 ÷ 4 ='

silver[2] Q: For \(y = 5 \times 2^x\), find \(y\) when \(x = 3\).
   step0 field=say answer=None text='Do the power first, then multiply by 5.'
   step1 field=pre answer=8 text='Work out 2³: 2 × 2 × 2 ='
   step2 field=pre answer=40 text='Multiply by 5: 5 × 8 ='
   step3 field=pre answer=40 text='So y ='

silver[4] Q: For \(y = \frac{1}{x}\), which two quadrants do the branches appear in?

silver[5] Q: Does the graph \(y = 0.7^x\) show growth or decay?
