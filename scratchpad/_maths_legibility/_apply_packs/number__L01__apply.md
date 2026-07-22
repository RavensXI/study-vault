# apply-pack: number__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [high] gold[3] | 7 to the power 0 = [box=1, NO label] | fix: Add a build to this step or the intro, e.g. 'Any number (except 0) to the power 0 equals 1, so 7 to the power 0 = 1.'
- [high] gold[3] | ask: 3 × 2 + 1 = [box=7] ... then ask: 1 × 10 = [box=10] | fix: Insert an explaining step between the bracket and the multiply: an intro 'Anything (except 0) raised to the power 0 equals 1, so 7^0 = 1' and/or an ask '7^0 = [
- [medium] gold[2] | √81 = [box=9, NO label] | fix: Scaffold the root the same way powers are scaffolded, e.g. '√81 means what number times itself makes 81, 9 × 9 = 81 so √81 =' (box stays NO label — it is a plai
- [medium] gold[3] | 4 × (−2) = [box=-8] | fix: Add the sign rule to this step, e.g. 'Now 4 × (−2): a positive times a negative gives a negative, so the answer is negative.'

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
gold[2] Q: \(5 \times 6 \div 3 + 4 \times (2 + 1)^2\)
   step0 field=say answer=None text='Bracket and power first, then handle each × and ÷ chain, then add.'
   step1 field=pre answer=3 text='bracket: 2 + 1 ='
   step2 field=pre answer=9 text='3 squared, 3 × 3 ='
   step3 field=pre answer=30 text='left chain: 5 × 6 ='
   step4 field=pre answer=10 text='30 ÷ 3 ='
   step5 field=pre answer=36 text='4 × 9 ='
   step6 field=pre answer=46 text='10 + 36 ='
   step7 field=pre answer=46 text='Read it back: 10 + 36 ='

gold[3] Q: \(2^4 - (3 \times 2 + 1)^0 \times 8\)
   step0 field=say answer=None text='Work the bracket, then the powers, then the × and −.'
   step1 field=pre answer=7 text='inside the bracket: 3 × 2 + 1 ='
   step2 field=pre answer=16 text='2 to the power 4, 2 × 2 × 2 × 2 ='
   step3 field=pre answer=1 text='7 to the power 0 ='
   step4 field=pre answer=8 text='1 × 8 ='
   step5 field=pre answer=8 text='16 − 8 ='
   step6 field=pre answer=8 text='Read it back: 16 − 8 ='

### board=maths-edexcel
gold[2] Q: \(6 \times 8 \div 4 + 5 \times (3 - 1)^2\)
   step0 field=say answer=None text='Bracket first: 3 − 1.'
   step1 field=pre answer=2 text='3 − 1 ='
   step2 field=pre answer=4 text='2² ='
   step3 field=pre answer=48 text='6 × 8 ='
   step4 field=pre answer=12 text='48 ÷ 4 ='
   step5 field=pre answer=20 text='5 × 4 ='
   step6 field=pre answer=32 text='12 + 20 ='
   step7 field=pre answer=12 text='Check: 32 − 20 ='

gold[3] Q: \(2^4 - (3 \times 2 + 1)^0 \times 10\)
   step0 field=say answer=None text='Start with the powers and the bracket. First 2⁴.'
   step1 field=pre answer=16 text='2⁴ ='
   step2 field=pre answer=7 text='3 × 2 + 1 ='
   step3 field=pre answer=10 text='1 × 10 ='
   step4 field=pre answer=6 text='16 − 10 ='
   step5 field=pre answer=16 text='Check: 6 + 10 ='

### board=maths-ocr
gold[2] Q: \(\sqrt{81} + 4 \times (2^3 - 3)\)
   step0 field=say answer=None text='Work the root, the bracket (its power first), then the multiply, then the add.'
   step1 field=pre answer=9 text='√81 ='
   step2 field=pre answer=8 text='2 cubed, 2 × 2 × 2 ='
   step3 field=pre answer=5 text='bracket: 8 − 3 ='
   step4 field=pre answer=20 text='4 × 5 ='
   step5 field=pre answer=29 text='9 + 20 ='
   step6 field=pre answer=29 text='Read it back: 9 + 20 ='

gold[3] Q: \(\frac{(3+5)^2}{4} - 2^3\)
   step0 field=say answer=None text='Finish the fraction (bracket, power, divide), work the other power, then subtract.'
   step1 field=pre answer=8 text='bracket: 3 + 5 ='
   step2 field=pre answer=64 text='8 squared, 8 × 8 ='
   step3 field=pre answer=16 text='64 ÷ 4 ='
   step4 field=pre answer=8 text='2 cubed, 2 × 2 × 2 ='
   step5 field=pre answer=8 text='16 − 8 ='
   step6 field=pre answer=8 text='Read it back: 16 − 8 ='

### board=maths-eduqas
gold[2] Q: \(\dfrac{3^3 - 7}{2 \times 5}\)
   step0 field=say answer=None text='The fraction bar groups the whole top and the whole bottom. Start with the top: 3³.'
   step1 field=pre answer=27 text='3³ ='
   step2 field=pre answer=20 text='27 − 7 ='
   step3 field=pre answer=10 text='2 × 5 ='
   step4 field=pre answer=2 text='20 ÷ 10 ='
   step5 field=pre answer=20 text='Check: 2 × 10 ='

gold[3] Q: \((-3)^2 + 4 \times (-2)\)
   step0 field=say answer=None text='Indices first. Square the bracket: (−3)², remembering a negative times a negative is posit'
   step1 field=pre answer=9 text='(−3) × (−3) ='
   step2 field=pre answer=-8 text='4 × (−2) ='
   step3 field=pre answer=1 text='9 + (−8) ='
   step4 field=pre answer=9 text='Check: 1 + 8 ='
