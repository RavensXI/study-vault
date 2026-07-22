# apply-pack: geometry__L08.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] bronze[2], bronze[3], silver[0], silver[1], silver[4], silver[5], silver[6], gold[0], gold[1], gold[2], gold[4] (question stems) | 512?Diagram not drawn accurately Find the magnitude of (5,12). | fix: Strip the concatenated diagram-label prefix so each stem reads cleanly, e.g. 'Find the magnitude of (5,12).' with the 'Diagram not drawn accurately' note separa
- [high] silver[4] | Q: 123456712345OA(1, 5)B(7, 3)MM is the midpoint of AB. OA=(1,5), OB=(7,3). Find | fix: Strip the leaked diagram labels and render the diagram separately; the stem should begin 'M is the midpoint of AB. OA = (1, 5), OB = (7, 3)...'
- [high] gold[0] | Q: acP12OABCOABC is a parallelogram. OA = a, OC = c. P divides AB in ratio 1:2.. | fix: Strip the leaked labels; stem should start 'OABC is a parallelogram. OA = a, OC = c...'
- [medium] bronze[5] | Q: 34?Find |(3,4)| (the magnitude).Diagram not drawn accurately | fix: Remove the leading '34?' and put the diagram note on its own line; stem should read 'Find |(3,4)| (the magnitude).'
- [medium] silver[6] | Q: 512?Find |(-5,12)|.Diagram not drawn accurately | fix: Remove '512?' and separate the diagram note; stem should read 'Find |(-5,12)|.'
- [medium] gold[3] | Q: -1123412345OA(3, 1)B(-1, 5)N OA=(3,1), OB=(-1,5). N divides AB in ratio 3:1.  | fix: Strip the leaked labels; stem should start 'OA = (3, 1), OB = (-1, 5). N divides AB in ratio 3:1...'
- [medium] gold[4] | Q: 24624681012OA(1, 2)B(4, 8)C(6, 12)Points A(1,2), B(4,8) and C(6,12) are colli | fix: Strip the leaked labels; stem should start 'Points A(1,2), B(4,8) and C(6,12) are collinear...'
- [high] silver[0] | Q: ABOA = \(\binom{1}{3}\), OB = \(\binom{5}{7}\). Find AB's x-component. | fix: Strip the leading 'AB' so it reads 'OA = (1,3), OB = (5,7). Find AB's x-component.'
- [high] silver[4] | Q: AMBM is the midpoint of AB. A = \(\binom{2}{4}\), B = \(\binom{10}{10}\). | fix: Remove the 'AMB' prefix so it reads 'M is the midpoint of AB.'
- [high] gold[0] | Q: OABMab?OA = a, OB = b. M is the midpoint of AB. | fix: Remove the 'OABMab?' prefix so it reads 'OA = a, OB = b. M is the midpoint of AB...'
- [high] gold[1] | Q: APBAP : PB = 1 : 2P divides AB in ratio 1:2. A = \(\binom{1}{3}\), B = \(\bin | fix: Delete the leading 'APBAP : PB = 1 : 2P' fragment so it starts 'P divides AB in ratio 1:2.'
- [high] gold[2] | Q: ABCShow that A(1,2), B(4,6), C(7,10) are collinear. | fix: Remove the 'ABC' prefix so it reads 'Show that A(1,2), B(4,6), C(7,10) are collinear.'
- [high] gold[3] | Q: aa10\(|\binom{a}{a}| = 10\). Find \(a\) (positive value). To 1 d.p. | fix: Remove the 'aa10' prefix so it reads '|(a, a)| = 10. Find a (positive value)...'
- [high] gold[4] | Q: APBAP : PB = 2 : 1A = \(\binom{3}{1}\), B = \(\binom{9}{5}\). | fix: Delete the 'APBAP : PB = 2 : 1' fragment; the ratio is already stated later ('AP:PB = 2:1'). Start clean with 'A = (3,1), B = (9,5).'
- [medium] bronze[4] | Q: 34?\(|\binom{3}{4}|\) = ? Diagram not drawn accurately | fix: Remove the leading '34?' so it reads '|(3,4)| = ?'
- [medium] bronze[7] | Q: 512?\(|\binom{5}{12}|\) = ? Diagram not drawn accurately | fix: Remove the leading '512?' so it reads '|(5,12)| = ?'
- [medium] silver[5] | Q: 68?\(|\binom{-6}{8}|\) = ? Diagram not drawn accurately | fix: Remove the leading '68?' so it reads '|(-6, 8)| = ?'
- [medium] silver[3] | Q: (2,6)(3,9)Are \(\binom{2}{6}\) and \(\binom{3}{9}\) parallel? Enter 1 for Yes | fix: Remove the leading '(2,6)(3,9)' so it reads 'Are (2,6) and (3,9) parallel? Enter 1 for Yes, 0 for No.'
- [medium] gold[1] | ask: First the fraction: 1 out of (1 + 2) parts, so the fraction is 1 ÷ 3 which  | fix: Split it: make this step only 'B − A in y: 9 − 3 = [6]', and move the '1 out of 3 parts = ⅓' explanation into the following 'take a third' step.
- [high] silver[3] | OABMM is the midpoint of AB. OA = (2 6), OB = (8 2). Find OM. | fix: Strip the leaked labels so it reads: 'M is the midpoint of AB. \(\overrightarrow{OA} = \binom{2}{6}\), \(\overrightarrow{OB} = \binom{8}{2}\). Find \(\overright
- [high] bronze[6] | AB(3, 4)A goes to B by vector (3 4). B goes to A by: | fix: Drop the leaked prefix: 'A goes to B by vector \(\binom{3}{4}\). B goes to A by:'
- [medium] silver[2] | abOAB?Diagram not drawn accuratelyOA = a, OB = b. Find AB. | fix: Remove 'abOAB?' and separate the caption: 'Diagram not drawn accurately. \(\overrightarrow{OA} = \mathbf{a}\), \(\overrightarrow{OB} = \mathbf{b}\). Find \(\ove
- [medium] gold[0] | abOABP21Diagram not drawn accuratelyOA = a, OB = b. P divides AB in the ratio 2: | fix: Strip 'abOABP21' and break the caption off: 'Diagram not drawn accurately. \(\overrightarrow{OA} = \mathbf{a}\), \(\overrightarrow{OB} = \mathbf{b}\). P divides
- [medium] gold[1] | abOABMDiagram not drawn accuratelyOA = 3a, OB = 6b. M is the midpoint of AB. Sho | fix: Remove 'abOABM' and separate the caption: 'Diagram not drawn accurately. \(\overrightarrow{OA} = 3\mathbf{a}\), \(\overrightarrow{OB} = 6\mathbf{b}\). M is the 
- [medium] silver[0] | 34?Diagram not drawn accuratelyMagnitude of (3 4). | fix: Strip '34?' and add a break: 'Diagram not drawn accurately. Find the magnitude of \(\binom{3}{4}\).'
- [medium] silver[1] | 68?Diagram not drawn accuratelyMagnitude of (-6 8). | fix: Strip '68?' and add a break: 'Diagram not drawn accurately. Find the magnitude of \(\binom{-6}{8}\).'
- [medium] silver[5] | PQR⅓Diagram not drawn accuratelyPQ = (6 -2). R is on PQ such that PR = ⅓ PQ. Fin | fix: Remove 'PQR⅓' and separate the caption: 'Diagram not drawn accurately. \(\overrightarrow{PQ} = \binom{6}{-2}\). R is on PQ such that PR = \(\frac{1}{3}\) PQ. Fi

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[2] Q: 512?Diagram not drawn accurately Find the magnitude of \(\binom{5}{12}\).
   step0 field=say answer=None text='Magnitude squares each number, adds them, then takes the square root.'
   step1 field=pre answer=25 text='5² ='
   step2 field=pre answer=144 text='12² ='
   step3 field=pre answer=169 text='Add: 25 + 144 ='
   step4 field=pre answer=13 text='√169 ='

bronze[4] Q: \(\mathbf{p} = \binom{4}{-3}\) and \(\mathbf{q} = \binom{-1}{2}\). Find \(\mathbf{p} - \ma
   step0 field=say answer=None text='To subtract, subtract the top numbers, then the bottom numbers.'
   step1 field=pre answer=5 text='Top: 4 − (−1) ='
   step2 field=pre answer=-5 text='Bottom: −3 − 2 ='
   step3 field=pre answer=4 text="Add q's top back to check: 5 + (−1) ="

bronze[5] Q: 34?Diagram not drawn accurately Find the magnitude of \(\binom{-3}{4}\).
   step0 field=say answer=None text='Magnitude squares each number, so the minus disappears.'
   step1 field=pre answer=9 text='(−3)² ='
   step2 field=pre answer=16 text='4² ='
   step3 field=pre answer=25 text='Add: 9 + 16 ='
   step4 field=pre answer=5 text='√25 ='

bronze[6] Q: If \(\overrightarrow{BA} = \binom{3}{-2}\), what is \(\overrightarrow{AB}\)?
   step0 field=say answer=None text='AB is the reverse of BA, so flip both signs.'
   step1 field=pre answer=-3 text='Top: −(3) ='
   step2 field=pre answer=2 text='Bottom: −(−2) ='
   step3 field=pre answer=0 text='Add the tops of AB and BA to check: −3 + 3 ='

bronze[7] Q: \(3\binom{2}{-1} = \)
   step0 field=say answer=None text='To scale, multiply both numbers by 3.'
   step1 field=pre answer=6 text='Top: 3 × 2 ='
   step2 field=pre answer=-3 text='Bottom: 3 × (−1) ='
   step3 field=pre answer=2 text='Divide the top back to check: 6 ÷ 3 ='

gold[0] Q: OABabX?Diagram not drawn accurately OA = a, OB = b. X is such that OX = 2a − b. Express BX
   step0 field=say answer=None text='Travel B to O, then O to X: \\(\\overrightarrow{BX} = \\overrightarrow{BO} + \\overrightarrow{'
   step1 field=pre answer=-1 text='OB = b, so BO reverses it. Coefficient of b in BO ='
   step2 field=pre answer=2 text='OX = 2a − b, so its coefficient of a ='
   step3 field=pre answer=2 text='Collect the a terms (0 from BO, 2 from OX):'
   step4 field=pre answer=-2 text='Collect the b terms: −1 + (−1) ='

gold[1] Q: OABabX?Diagram not drawn accurately OA = a and OB = b. A point X satisfies BX = 2a − 2b. F
   step0 field=say answer=None text='Write BA in terms of a and b, then compare it with BX.'
   step1 field=pre answer=1 text='BA = OA − OB = a − b, so the coefficient of a in BA ='
   step2 field=pre answer=2 text='BX = 2a − 2b, so the coefficient of a in BX ='
   step3 field=pre answer=2 text='How many BA fit into BX: 2 ÷ 1 ='
   step4 field=pre answer=2 text='So |BX| : |BA| = 2 : 1. Type the first number of the ratio:'

gold[2] Q: OAB3a3bPQ?Diagram not drawn accurately OA = 3a, OB = 3b. P is ⅔ along OA. Q is ⅓ along OB.
   step0 field=say answer=None text='Find OP and OQ, then \\(\\overrightarrow{PQ} = \\overrightarrow{PO} + \\overrightarrow{OQ}\\).'
   step1 field=pre answer=2 text='OP = ⅔ of 3a. Coefficient of a: (2 ÷ 3) × 3 ='
   step2 field=pre answer=1 text='OQ = ⅓ of 3b. Coefficient of b: (1 ÷ 3) × 3 ='
   step3 field=pre answer=-2 text='PO reverses OP, so the coefficient of a in PQ ='
   step4 field=pre answer=1 text='Coefficient of b in PQ, from OQ ='

gold[3] Q: Prove that the vectors \(\overrightarrow{AB} = 3\mathbf{p} + 6\mathbf{q}\) and \(\overrigh
   step0 field=say answer=None text='Parallel means one is a scalar multiple. Check both terms give the same multiplier.'
   step1 field=pre answer=3 text='From the p terms: 3 ÷ 1 ='
   step2 field=pre answer=3 text='From the q terms: 6 ÷ 2 ='
   step3 field=pre answer=3 text='Both agree, so k ='

gold[4] Q: OABabMN?Diagram not drawn accurately OA = a, OB = b. M is midpoint of OA, N is midpoint of
   step0 field=say answer=None text='M is the midpoint of OA, N of OB. Use \\(\\overrightarrow{MN} = \\overrightarrow{MO} + \\overr'
   step1 field=pre answer=-0.5 text='OM = ½a, so MO reverses it. Coefficient of a in MO ='
   step2 field=pre answer=0.5 text='ON = ½b, so the coefficient of b ='
   step3 field=pre answer=-0.5 text='Coefficient of a in MN, from MO ='
   step4 field=pre answer=0.5 text='Coefficient of b in MN, from ON ='

silver[0] Q: OABabP?Diagram not drawn accurately OA = a, OB = b. P is the midpoint of AB. Find OP in te
   step0 field=say answer=None text='For the midpoint of AB, \\(\\overrightarrow{OP} = \\tfrac12(\\mathbf{a} + \\mathbf{b})\\): halve'
   step1 field=pre answer=0.5 text='Coefficient of a: ½ × 1 ='
   step2 field=pre answer=0.5 text='Coefficient of b: ½ × 1 ='
   step3 field=pre answer=1 text='Double the a coefficient back to check: 0.5 × 2 ='

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

silver[3] Q: Vectors \(2\mathbf{a} + 3\mathbf{b}\) and \(6\mathbf{a} + k\mathbf{b}\) are parallel. Find
   step0 field=say answer=None text='Parallel vectors are scalar multiples. Find the multiplier from the a terms.'
   step1 field=pre answer=3 text='Multiplier: 6 ÷ 2 ='
   step2 field=pre answer=9 text='Apply it to the b term: k = 3 × 3 ='
   step3 field=pre answer=6 text='Check the a term: 3 × 2 ='

silver[4] Q: 86?Diagram not drawn accurately Find the magnitude of \(\binom{-8}{6}\).
   step0 field=say answer=None text='Square each number, add them, then take the square root.'
   step1 field=pre answer=64 text='(−8)² ='
   step2 field=pre answer=36 text='6² ='
   step3 field=pre answer=100 text='Add: 64 + 36 ='
   step4 field=pre answer=10 text='√100 ='

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
bronze[2] Q: \(3 \times \binom{3}{-1}\). Give the top component.
   step0 field=say answer=None text='A scalar multiplies every row of the vector.'
   step1 field=pre answer=-3 text='Bottom row: 3 × (−1) ='
   step2 field=pre answer=9 text='Top row: 3 × 3 ='
   step3 field=pre answer=9 text='So 3 × (3, −1) = (9, −3). The top component is'

bronze[4] Q: If \(\vec{OA} = \binom{3}{5}\) and \(\vec{OB} = \binom{10}{2}\), find the top component of
   step0 field=say answer=None text='\\(\\vec{AB}\\) is the journey from A to B, which is \\(\\mathbf{b} - \\mathbf{a}\\) (end minus s'
   step1 field=pre answer=-3 text='Bottom of AB: 2 − 5 ='
   step2 field=pre answer=7 text='Top of AB: 10 − 3 ='
   step3 field=pre answer=7 text='So \\(\\vec{AB}\\) = (7, −3). The top component is'

bronze[5] Q: 34?Find \(|\binom{3}{4}|\) (the magnitude).Diagram not drawn accurately
   step0 field=say answer=None text='Magnitude is Pythagoras on the two components: square, add, square root.'
   step1 field=pre answer=9 text='Square the top: 3 × 3 ='
   step2 field=pre answer=16 text='Square the bottom: 4 × 4 ='
   step3 field=pre answer=25 text='Add the squares: 9 + 16 ='
   step4 field=pre answer=5 text='Square root the total: √25 ='

bronze[6] Q: \(2\mathbf{a} + 6\mathbf{a} = ?\) (in terms of \(\mathbf{a}\)). What is the coefficient?
   step0 field=say answer=None text="\\(2\\mathbf{a}\\) and \\(6\\mathbf{a}\\) point the same way, so you just add how many a's there"
   step1 field=pre answer=2 text="Count the first: 2a has this many a's:"
   step2 field=pre answer=8 text='Add the counts: 2 + 6 ='
   step3 field=pre answer=8 text='So \\(2\\mathbf{a} + 6\\mathbf{a} = 8\\mathbf{a}\\). The coefficient (number in front) is'

bronze[7] Q: \(\binom{-1}{4} + \binom{1}{-4}\). Give the top component.
   step0 field=say answer=None text='These two vectors point in opposite directions. Add the matching rows with their signs.'
   step1 field=pre answer=0 text='Bottom row: 4 + (−4) ='
   step2 field=pre answer=0 text='Top row: (−1) + 1 ='
   step3 field=pre answer=0 text='So the sum is (0, 0). The top component is'

gold[0] Q: acP12OABCOABC is a parallelogram. \(\vec{OA} = \mathbf{a}\), \(\vec{OC} = \mathbf{c}\). P 
   step0 field=say answer=None text='In parallelogram OABC, O and B are opposite corners, so \\(\\vec{OB} = \\mathbf{a} + \\mathbf{'
   step1 field=pre answer=1 text="Find \\(\\vec{AB} = \\vec{OB} - \\vec{OA}\\). The c's: OB has 1c, OA has none, so 1 − 0 ="
   step2 field=say answer=None text='So \\(\\vec{AB} = \\mathbf{c}\\). P divides AB in ratio 1:2.'
   step3 field=pre answer=3 text='Turn the ratio 1:2 into a fraction: AP is 1 part out of 1 + 2 ='
   step4 field=pre answer=1 text='So AP = \\(\\tfrac{1}{3}\\mathbf{c}\\) and \\(\\vec{OP} = \\mathbf{a} + \\tfrac{1}{3}\\mathbf{c}\\).'
   step5 field=pre answer=3 text='Its denominator (bottom), from AP being one third of AB, is'

gold[1] Q: \(\vec{OA} = \mathbf{a}\), \(\vec{OB} = \mathbf{b}\). X is such that \(\vec{OX} = 2\mathbf
   step0 field=say answer=None text='\\(\\vec{XY}\\) is the journey from X to Y: \\(\\vec{XY} = \\vec{OY} - \\vec{OX}\\).'
   step1 field=pre answer=-2 text='The b terms: OY has −3b, OX has −b, so −3 − (−1) ='
   step2 field=pre answer=2 text='The a terms: OY has 4a, OX has 2a, so 4 − 2 ='
   step3 field=pre answer=2 text='So \\(\\vec{XY} = 2\\mathbf{a} - 2\\mathbf{b}\\). The coefficient of a is'

gold[2] Q: Vectors \(3\mathbf{a} + k\mathbf{b}\) and \(6\mathbf{a} - 4\mathbf{b}\) are parallel. Find
   step0 field=say answer=None text='Parallel means the second vector is a scalar multiple of the first: \\(6\\mathbf{a} - 4\\math'
   step1 field=pre answer=2 text='The a terms: 6 = λ × 3, so λ = 6 ÷ 3 ='
   step2 field=pre answer=-2 text='The b terms: −4 = λ × k = 2k, so k = −4 ÷ 2 ='
   step3 field=pre answer=-4 text='Check: with k = −2, the b term of 2 × (3a − 2b) is 2 × (−2) ='

gold[3] Q: -1123412345OA(3, 1)B(-1, 5)N\(\vec{OA} = \binom{3}{1}\), \(\vec{OB} = \binom{-1}{5}\). N d
   step0 field=say answer=None text='First find \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\), then N is 3/4 of the way along (3 parts'
   step1 field=pre answer=-4 text='AB top: −1 − 3 ='
   step2 field=pre answer=-3 text='AN top: \\(\\tfrac{3}{4}\\) × (−4) ='
   step3 field=pre answer=0 text='ON top = OA top + AN top = 3 + (−3) ='
   step4 field=pre answer=4 text='Check with the bottom: AB bottom = 5 − 1 = 4, AN bottom = \\(\\tfrac{3}{4}\\)(4) = 3, so ON b'

gold[4] Q: 24624681012OA(1, 2)B(4, 8)C(6, 12)Points A\((1,2)\), B\((4,8)\) and C\((6,12)\) are collin
   step0 field=say answer=None text='For points, \\(\\vec{AB} = B - A\\): the coordinates of B minus the coordinates of A.'
   step1 field=pre answer=6 text='AB bottom: 8 − 2 ='
   step2 field=pre answer=3 text='AB top: 4 − 1 ='
   step3 field=pre answer=3 text='Check collinear: \\(\\vec{AC} = C - A = (5, 10)\\), and (5, 10) = \\(\\tfrac{5}{3}\\)(3, 6). The'

silver[0] Q: \(\vec{OA} = \binom{2}{3}\), \(\vec{OB} = \binom{8}{-1}\). Find \(|\vec{AB}|\) to 1 d.p.
   step0 field=say answer=None text='First find \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\), then its length by Pythagoras.'
   step1 field=pre answer=6 text='AB top: 8 − 2 ='
   step2 field=pre answer=-4 text='AB bottom: (−1) − 3 ='
   step3 field=pre answer=52 text='Square and add: 36 + 16 ='
   step4 field=pre answer=7.2 text='Square root, to 1 d.p.: √52 ='

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

silver[3] Q: If \(\binom{2k}{3}\) is parallel to \(\binom{4}{6}\), find \(k\).
   step0 field=say answer=None text='Two column vectors are parallel when their cross products are equal: top1 × bottom2 = bott'
   step1 field=pre answer=12 text='Work the right side: bottom1 × top2 = 3 × 4 ='
   step2 field=pre answer=1 text='The left side is 2k × 6 = 12k, so 12k = 12. Divide: 12 ÷ 12 ='
   step3 field=pre answer=6 text='Check: with k = 1 the vector is (2, 3), and doubling the bottom, 2 × 3 ='

silver[4] Q: 123456712345OA(1, 5)B(7, 3)MM is the midpoint of AB. \(\vec{OA} = \binom{1}{5}\), \(\vec{O
   step0 field=say answer=None text='The midpoint M has \\(\\vec{OM} = \\tfrac{1}{2}(\\vec{OA} + \\vec{OB})\\): add the position vect'
   step1 field=pre answer=8 text='Add the bottoms: 5 + 3 ='
   step2 field=pre answer=8 text='Now the tops: 1 + 7 ='
   step3 field=pre answer=4 text='Halve the top: 8 ÷ 2 ='

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
bronze[2] Q: \(3 \times \binom{2}{-1}\). Give the x-component.
   step0 field=say answer=None text='Scalar multiply means multiply BOTH parts by 3.'
   step1 field=pre answer=-3 text='The y part: 3 × (−1) ='
   step2 field=pre answer=6 text='The x part, the one asked for: 3 × 2 ='
   step3 field=pre answer=6 text='So the x-component ='

bronze[4] Q: 34?\(|\binom{3}{4}|\) = ? Diagram not drawn accurately
   step0 field=say answer=None text='Magnitude is the length of the arrow, found with Pythagoras on the two parts.'
   step1 field=pre answer=9 text='Square the x part: 3² ='
   step2 field=pre answer=16 text='Square the y part: 4² ='
   step3 field=pre answer=25 text='Add the squares: 9 + 16 ='
   step4 field=pre answer=5 text='Square root: √25 ='

bronze[5] Q: \(-2 \times \binom{3}{-4}\). Give the y-component.
   step0 field=say answer=None text='Scalar multiply means multiply BOTH parts by −2.'
   step1 field=pre answer=-6 text='The x part: −2 × 3 ='
   step2 field=pre answer=8 text='The y part, the one asked for: −2 × (−4) ='
   step3 field=pre answer=8 text='So the y-component ='

bronze[6] Q: \(\binom{1}{2} + \binom{-1}{-2}\). Give the x-component.
   step0 field=say answer=None text='Add column vectors by working down the columns: the two x parts together, the two y parts '
   step1 field=pre answer=0 text='First the y parts, 2 + (−2) ='
   step2 field=pre answer=0 text='Now the x parts, the one asked for, 1 + (−1) ='
   step3 field=pre answer=0 text='So the full answer is a column vector. Its x-component ='

bronze[7] Q: 512?\(|\binom{5}{12}|\) = ? Diagram not drawn accurately
   step0 field=say answer=None text='Magnitude is the length of the arrow, found with Pythagoras on the two parts.'
   step1 field=pre answer=25 text='Square the x part: 5² ='
   step2 field=pre answer=144 text='Square the y part: 12² ='
   step3 field=pre answer=169 text='Add the squares: 25 + 144 ='
   step4 field=pre answer=13 text='Square root: √169 ='

gold[0] Q: OABMab?OA = a, OB = b. M is the midpoint of AB. Find OM in terms of a and b, then with a =
   step0 field=say answer=None text='To reach M, go to A then half of AB: \\(OM = a + \\tfrac{1}{2}(b - a) = \\tfrac{1}{2}(a + b)\\'
   step1 field=pre answer=8 text='Add the y parts of a and b: 6 + 2 ='
   step2 field=pre answer=4 text="Halve it for OM's y part: 8 ÷ 2 ="
   step3 field=pre answer=12 text='Now the x parts, the one asked for: add 2 + 10 ='
   step4 field=pre answer=6 text='Halve it: 12 ÷ 2 ='

gold[1] Q: APBAP : PB = 1 : 2P divides AB in ratio 1:2. A = \(\binom{1}{3}\), B = \(\binom{7}{9}\). F
   step0 field=say answer=None text='Ratio 1:2 splits AB into 3 equal parts, and P is 1 part along, so P = A + \\(\\tfrac{1}{3}\\)'
   step1 field=pre answer=6 text='First the fraction: 1 out of (1 + 2) parts, so the fraction is 1 ÷ 3 which we use as ⅓. Th'
   step2 field=pre answer=2 text='Take a third of that: 6 ÷ 3 ='
   step3 field=pre answer=5 text="Add it onto A's y: 3 + 2 ="

gold[2] Q: ABCShow that A(1,2), B(4,6), C(7,10) are collinear. AB has what x-component? Diagram not d
   step0 field=say answer=None text='Collinear means the points lie on one straight line: AB and BC must be parallel and share '
   step1 field=pre answer=4 text='AB in y: 6 − 2 ='
   step2 field=pre answer=3 text='AB in x, the one asked for: 4 − 1 ='
   step3 field=pre answer=3 text='Check BC in x: 7 − 4 ='

gold[3] Q: aa10\(|\binom{a}{a}| = 10\). Find \(a\) (positive value). To 1 d.p. Diagram not drawn accu
   step0 field=say answer=None text='Magnitude squared: \\(a^2 + a^2 = 10^2\\). Both parts are a, so there are two a² terms.'
   step1 field=pre answer=100 text='Square the length: 10² ='
   step2 field=pre answer=2 text='Combine the two a² terms: a² + a² ='
   step3 field=pre answer=50 text='So 2a² = 100, giving a² = 100 ÷ 2 ='
   step4 field=pre answer=7.1 text='Square root for a: √50 ='

gold[4] Q: APBAP : PB = 2 : 1A = \(\binom{3}{1}\), B = \(\binom{9}{5}\). Point P is on AB such that A
   step0 field=say answer=None text='Ratio 2:1 splits AB into 3 equal parts, and P is 2 parts along, so P = A + \\(\\tfrac{2}{3}\\'
   step1 field=pre answer=6 text='The step B − A in x: 9 − 3 ='
   step2 field=pre answer=4 text='Take two thirds of it: 6 × 2 ÷ 3 ='
   step3 field=pre answer=7 text="Add it onto A's x: 3 + 4 ="

silver[0] Q: ABOA = \(\binom{1}{3}\), OB = \(\binom{5}{7}\). Find AB's x-component. Diagram not drawn a
   step0 field=say answer=None text='To travel A to B, subtract the start from the end: \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\).'
   step1 field=pre answer=4 text='The y part: 7 − 3 ='
   step2 field=pre answer=4 text='The x part, the one asked for: 5 − 1 ='
   step3 field=pre answer=4 text='So the x-component of AB ='

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

silver[3] Q: (2,6)(3,9)Are \(\binom{2}{6}\) and \(\binom{3}{9}\) parallel? Enter 1 for Yes, 0 for No.
   step0 field=say answer=None text='Parallel means one vector is a scalar multiple of the other: the same number times BOTH pa'
   step1 field=pre answer=1.5 text='Compare the x parts: 3 ÷ 2 ='
   step2 field=pre answer=1.5 text='Compare the y parts: 9 ÷ 6 ='
   step3 field=pre answer=1 text='Same multiplier both times means parallel. Enter 1 for Yes:'

silver[4] Q: AMBM is the midpoint of AB. A = \(\binom{2}{4}\), B = \(\binom{10}{10}\). Find M's x-compo
   step0 field=say answer=None text='The midpoint is the average of the two ends: add the coordinates and halve.'
   step1 field=pre answer=7 text='The y coordinate: (4 + 10) ÷ 2 ='
   step2 field=pre answer=6 text='The x coordinate, the one asked for: (2 + 10) ÷ 2 ='
   step3 field=pre answer=6 text="So M's x-component ="

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
bronze[2] Q: \(3 \times \binom{2}{-4}\) =

bronze[4] Q: \(\binom{0}{7} + \binom{-3}{0}\) =

bronze[5] Q: \(2\binom{1}{3} + \binom{4}{-1}\) =

bronze[6] Q: AB(3, 4)A goes to B by vector \(\binom{3}{4}\). B goes to A by:

bronze[7] Q: \(\binom{-1}{6} + \binom{1}{-6}\) =

gold[0] Q: abOABP21Diagram not drawn accurately\(\overrightarrow{OA} = \mathbf{a}\), \(\overrightarro

gold[1] Q: abOABMDiagram not drawn accurately\(\overrightarrow{OA} = 3\mathbf{a}\), \(\overrightarrow

gold[2] Q: If \(\overrightarrow{AB} = k \overrightarrow{CD}\), what can you conclude?

gold[3] Q: \(\overrightarrow{OA} = \mathbf{a}\), \(\overrightarrow{OB} = \mathbf{b}\), \(\overrightar

gold[4] Q: \(\mathbf{a} = \binom{1}{2}\), \(\mathbf{b} = \binom{3}{-1}\). Find \(|2\mathbf{a} - \math

silver[0] Q: 34?Diagram not drawn accuratelyMagnitude of \(\binom{3}{4}\).

silver[1] Q: 68?Diagram not drawn accuratelyMagnitude of \(\binom{-6}{8}\).

silver[2] Q: abOAB?Diagram not drawn accurately\(\overrightarrow{OA} = \mathbf{a}\), \(\overrightarrow{

silver[3] Q: OABMM is the midpoint of AB. \(\overrightarrow{OA} = \binom{2}{6}\), \(\overrightarrow{OB}

silver[4] Q: Vectors \(\mathbf{p}\) and \(\mathbf{q}\) are parallel. \(\mathbf{p} = \binom{4}{6}\). Whi

silver[5] Q: PQR⅓Diagram not drawn accurately\(\overrightarrow{PQ} = \binom{6}{-2}\). R is on PQ such t

silver[6] Q: Which vector is a unit vector?
