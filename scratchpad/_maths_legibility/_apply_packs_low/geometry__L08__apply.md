# apply-pack: geometry__L08.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[2] (bottom-component step) | Bottom: (−2) ÷ 3 stays as −⅔. Multiply it back by 3 to check: (−2/3) × 3 = [box= | fix: Split into two shorter steps: state 'The bottom stays as −⅔' on its own, then a separate check line 'Multiply back by 3: (−2/3) × 3 ='; drop or simplify the 'If
- [low] silver[5] | ask: Square the x part: 6² = [box=36] | fix: Write 'Square the x part: (−6)² = [36]' (or add a one-line note that squaring a negative gives a positive).
- [low] silver[1] | ask: The y parts: 2 × 1 and −3 × (−1), combined = [box=5] | fix: Either spell it out — 'work out 2×1 = 2 and −3×(−1) = 3, then add them: [5]' — or split into two boxes as the bronze questions do.
- [low] silver[6] | Which vector is a unit vector? | fix: Add the definition to the stem: 'A unit vector has magnitude 1. Which of these is a unit vector?'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
silver[1] Q: OAB2a2bM?Diagram not drawn accurately OA = 2a, OB = 2b. M is the midpoint of AB. Find OM.
   step0 field=say answer=None text='Midpoint \\(\\overrightarrow{OM} = \\tfrac12(\\overrightarrow{OA} + \\overrightarrow{OB}) = \\tf'
   step1 field=pre answer=1 text='Coefficient of a: ½ × 2 ='
   step2 field=pre answer=1 text='Coefficient of b: ½ × 2 ='
   step3 field=pre answer=2 text='Undo the half on a to check: 1 × 2 ='

silver[2] Q: \(\overrightarrow{AB} = \binom{6}{-2}\). C is \(\frac{1}{3}\) of the way from A to B. Find
   step0 field=say answer=None text='C is one third of the way from A to B, so AC = ⅓ of AB.'
   step1 field=pre answer=2 text='Top: 6 ÷ 3 ='
   step2 field=pre answer=2 text='If you halved by mistake the top would be 3. The correct top is:'
   step3 field=pre answer=-2 text='Bottom: (−2) ÷ 3 stays as −⅔. Multiply it back by 3 to check: (−2/3) × 3 ='
   step4 field=pre answer=6 text='Top back: 2 × 3 ='

silver[5] Q: OABabP?Diagram not drawn accurately OA = a, OB = b. Point P divides AB in ratio 1:3 from A
   step0 field=say answer=None text='Ratio 1:3 from A means P is one quarter of the way along AB.'
   step1 field=pre answer=0.25 text='Fraction along AB: 1 ÷ (1 + 3) ='
   step2 field=pre answer=-1 text='AB = b − a, so the coefficient of a in AB ='
   step3 field=pre answer=0.75 text='OP = a + ¼(b − a). Coefficient of a: 1 − 0.25 ='
   step4 field=pre answer=0.25 text='Coefficient of b: 0 + 0.25 ='

silver[6] Q: 125?Diagram not drawn accurately A = (3, 2), B = (15, 7). Find |AB|.
   step0 field=say answer=None text='Find the across and up steps from A to B, then use Pythagoras.'
   step1 field=pre answer=12 text='Across: 15 − 3 ='
   step2 field=pre answer=5 text='Up: 7 − 2 ='
   step3 field=pre answer=169 text='Square and add: 12² + 5² ='
   step4 field=pre answer=13 text='√169 ='

### board=maths-edexcel
silver[1] Q: If \(\mathbf{p} = \binom{3}{6}\), write a vector parallel to \(\mathbf{p}\) with top compo
   step0 field=say answer=None text='A parallel vector is the same vector scaled. To make the top 1, divide everything by 3.'
   step1 field=pre answer=1 text='New top: 3 ÷ 3 ='
   step2 field=pre answer=2 text='Do the same to the bottom: 6 ÷ 3 ='
   step3 field=pre answer=6 text='So the parallel vector is (1, 2). Check it is parallel: 3 × 2 should give the original bot'

silver[2] Q: \(\vec{OA} = 5\mathbf{a}\), \(\vec{OB} = 3\mathbf{b}\). Find \(\vec{BA}\) in terms of \(\m
   step0 field=say answer=None text='\\(\\vec{BA}\\) is the journey from B to A: \\(\\vec{BA} = \\vec{OA} - \\vec{OB}\\).'
   step1 field=pre answer=5 text='The a terms: OA has 5a, OB has none, so 5 − 0 ='
   step2 field=pre answer=-3 text='The b terms: 0 − 3 ='
   step3 field=pre answer=5 text='So \\(\\vec{BA} = 5\\mathbf{a} - 3\\mathbf{b}\\). The coefficient of a is'

silver[5] Q: \(\vec{AB} = \binom{-3}{5}\). Find \(\vec{BA}\). Give the top component.
   step0 field=say answer=None text='\\(\\vec{BA}\\) is the reverse of \\(\\vec{AB}\\): \\(\\vec{BA} = -\\vec{AB}\\), so flip the sign of'
   step1 field=pre answer=-5 text='Flip the bottom: −(5) ='
   step2 field=pre answer=3 text='Flip the top: −(−3) ='
   step3 field=pre answer=3 text='So \\(\\vec{BA}\\) = (3, −5). The top component is'

silver[6] Q: 512?Find \(|\binom{-5}{12}|\).Diagram not drawn accurately
   step0 field=say answer=None text='Magnitude is Pythagoras on the components: square, add, square root. A negative squares to'
   step1 field=pre answer=25 text='Square the top: (−5) × (−5) ='
   step2 field=pre answer=144 text='Square the bottom: 12 × 12 ='
   step3 field=pre answer=169 text='Add the squares: 25 + 144 ='
   step4 field=pre answer=13 text='Square root the total: √169 ='

### board=maths-ocr
silver[1] Q: \(2\mathbf{a} - 3\mathbf{b}\) where \(\mathbf{a} = \binom{4}{1}\), \(\mathbf{b} = \binom{2
   step0 field=say answer=None text='Scale each vector first, then combine the matching parts.'
   step1 field=pre answer=5 text='The y parts: 2 × 1 and −3 × (−1), combined ='
   step2 field=pre answer=2 text='The x parts: 2 × 4 and −3 × 2, combined ='
   step3 field=pre answer=2 text='So the x-component ='

silver[2] Q: \(2\mathbf{a} - 3\mathbf{b}\) where \(\mathbf{a} = \binom{4}{1}\), \(\mathbf{b} = \binom{2
   step0 field=say answer=None text='Scale each vector first, then combine the matching parts.'
   step1 field=pre answer=2 text='The x parts: 2 × 4 and −3 × 2, combined ='
   step2 field=pre answer=5 text='The y parts: 2 × 1 and −3 × (−1), combined ='
   step3 field=pre answer=5 text='So the y-component ='

silver[5] Q: 68?\(|\binom{-6}{8}|\) = ? Diagram not drawn accurately
   step0 field=say answer=None text='Magnitude is the length of the arrow, found with Pythagoras on the two parts.'
   step1 field=pre answer=36 text='Square the x part: 6² ='
   step2 field=pre answer=64 text='Square the y part: 8² ='
   step3 field=pre answer=100 text='Add the squares: 36 + 64 ='
   step4 field=pre answer=10 text='Square root: √100 ='

silver[6] Q: \(\binom{6}{-8}\) is a scalar multiple of \(\binom{3}{k}\). Find \(k\).
   step0 field=say answer=None text='A scalar multiple stretches both parts by the SAME number. Find that number from the parts'
   step1 field=pre answer=2 text='The x parts go 3 to 6, so the multiplier is 6 ÷ 3 ='
   step2 field=pre answer=-4 text='Apply it to the y parts: the (3,k) becomes (6,−8), so 2 × k = −8. Then k = −8 ÷ 2 ='
   step3 field=pre answer=-4 text='So k ='

### board=maths-eduqas
silver[1] Q: 68?Diagram not drawn accuratelyMagnitude of \(\binom{-6}{8}\).

silver[2] Q: abOAB?Diagram not drawn accurately\(\overrightarrow{OA} = \mathbf{a}\), \(\overrightarrow{

silver[5] Q: PQR⅓Diagram not drawn accurately\(\overrightarrow{PQ} = \binom{6}{-2}\). R is on PQ such t

silver[6] Q: Which vector is a unit vector?
