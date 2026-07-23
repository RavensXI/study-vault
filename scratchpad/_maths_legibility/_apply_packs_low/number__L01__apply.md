# apply-pack: number__L01.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[2] | intro: Bracket and power first, then handle each x and ÷ chain, then add. | fix: Reword to plain language: 'Bracket and power first, then work the x and ÷ from left to right, then add.'
- [low] gold[4] | √49 = [box=7] | fix: Add a one-line prompt of what the root asks, e.g. '√49 means: what number times itself makes 49?'

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

gold[4] Q: \(\dfrac{(5-2)^3 + 3}{2 \times 5}\)
   step0 field=say answer=None text='The fraction bar groups top and bottom. Build the whole top, then the whole bottom, then d'
   step1 field=pre answer=3 text='inside the top bracket: 5 − 2 ='
   step2 field=pre answer=27 text='3 cubed, 3 × 3 × 3 ='
   step3 field=pre answer=30 text='top total: 27 + 3 ='
   step4 field=pre answer=10 text='bottom: 2 × 5 ='
   step5 field=pre answer=3 text='30 ÷ 10 ='
   step6 field=pre answer=3 text='Read it back: 30 ÷ 10 ='

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

gold[4] Q: \(\dfrac{5^2 + \sqrt{49}}{2^3}\)
   step0 field=say answer=None text='The fraction bar groups the top. Work out 5² first.'
   step1 field=pre answer=25 text='5² ='
   step2 field=pre answer=7 text='√49 ='
   step3 field=pre answer=32 text='25 + 7 ='
   step4 field=pre answer=8 text='2³ ='
   step5 field=pre answer=4 text='32 ÷ 8 ='
   step6 field=pre answer=32 text='Check: 4 × 8 ='

### board=maths-ocr
gold[2] Q: \(\sqrt{81} + 4 \times (2^3 - 3)\)
   step0 field=say answer=None text='Work the root, the bracket (its power first), then the multiply, then the add.'
   step1 field=pre answer=9 text='√81 ='
   step2 field=pre answer=8 text='2 cubed, 2 × 2 × 2 ='
   step3 field=pre answer=5 text='bracket: 8 − 3 ='
   step4 field=pre answer=20 text='4 × 5 ='
   step5 field=pre answer=29 text='9 + 20 ='
   step6 field=pre answer=29 text='Read it back: 9 + 20 ='

gold[4] Q: \(2 \times 3^2 + \frac{40}{2^3}\)
   step0 field=say answer=None text='Do both powers first, then the × and the fraction, then add.'
   step1 field=pre answer=9 text='3 squared, 3 × 3 ='
   step2 field=pre answer=18 text='2 × 9 ='
   step3 field=pre answer=8 text='2 cubed, 2 × 2 × 2 ='
   step4 field=pre answer=5 text='40 ÷ 8 ='
   step5 field=pre answer=23 text='18 + 5 ='
   step6 field=pre answer=23 text='Read it back: 18 + 5 ='

### board=maths-eduqas
gold[2] Q: \(\dfrac{3^3 - 7}{2 \times 5}\)
   step0 field=say answer=None text='The fraction bar groups the whole top and the whole bottom. Start with the top: 3³.'
   step1 field=pre answer=27 text='3³ ='
   step2 field=pre answer=20 text='27 − 7 ='
   step3 field=pre answer=10 text='2 × 5 ='
   step4 field=pre answer=2 text='20 ÷ 10 ='
   step5 field=pre answer=20 text='Check: 2 × 10 ='

gold[4] Q: \(\sqrt{49} + 2^3 \times 3 - 8\)
   step0 field=say answer=None text='Indices and roots first: √49 and 2³.'
   step1 field=pre answer=7 text='√49 ='
   step2 field=pre answer=8 text='2³ ='
   step3 field=pre answer=24 text='8 × 3 ='
   step4 field=pre answer=31 text='7 + 24 ='
   step5 field=pre answer=23 text='31 − 8 ='
   step6 field=pre answer=7 text='Check: 23 + 8 − 24 ='
