# apply-pack: number__L02.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] gold[3] | Flip and multiply the tops: 5 × 3 = [box=15] | fix: Restate the reciprocal in the intro as the sibling problems do: 'Keep, Flip, Change: \(\frac{5}{6} \div \frac{2}{3}\) becomes \(\frac{5}{6} \times \frac{3}{2}\)
- [low] gold[4] final check (line 185) | Check: 3/8 ÷ 3/4 = 0.5 and 0.5 + 0.5 = [box=1, NO label] | fix: Keep the check in fractions to match the walk, e.g. 'Check: the division gave 1/2, and 1/2 + 1/2 = [box]'. If the decimal is wanted, bridge it explicitly: '1/2 
- [low] gold[1] | Check with decimals: 2.5 × 1.6 = [box=4] | fix: Either give the working ('2.5 × 1.6: 25 × 16 = 400, so 4.0 = ___') or drop the decimal check, since the fraction answer 40 ÷ 10 = 4 was already reached.
- [low] bronze[4] | and the bottom stays [box=8] | fix: Make it self-contained: 'The bottom also shares no factor with 3, so the bottom stays ___'.
- [low] bronze[6] | Check: turn 1/3 back up by 10. 1 × 10 = [box=10] | fix: Use plainer wording, e.g. 'Check by scaling back up: multiply the top by 10, 1 × 10 = ___'.
- [low] gold[4] | Check: \frac{1}{4} + \frac{1}{4} = \frac{2}{4}, which halves to 1 over [box=2] | fix: State it explicitly: '2/4 simplifies to a half, so the bottom is ___' (or set the box to expect the full fraction 1/2).
- [low] silver[0] final box (same pattern in silver[1], silver[6], bronze[2], gold[1], gold[3]) | Check: turn 2/5 back up by 3. 2 × 3 = | fix: Use a plain instruction, e.g. 'Check by multiplying 2/5 by 3: 2 × 3 ='
- [low] bronze[0] final box (same pattern in bronze[1],[3],[4],[5],[6], silver[4],[5], gold[0],[4]) | Check: 7 and 12 share no factor, so 7/12 is simplest. Subtract back 7 − 4 = | fix: Split the check and name its purpose, e.g. 'To check the addition, undo it: 7 − 4 =' (this should return the numerator you added).
- [low] silver[2] final box (also silver[3], gold[2]) | Check: multiply back. 3/2 × 1/2, tops: 3 × 1 = | fix: Spell it out, e.g. 'To check the division, multiply your answer 3/2 by 1/2: tops 3 × 1 =' (this should rebuild the original numerator).

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: \(\frac{1}{4} + \frac{1}{3}\)
   step0 field=say answer=None text='Add and subtract fractions only when the bottoms match. First make them match.'
   step1 field=pre answer=12 text='The lowest common denominator of 4 and 3 is'
   step2 field=pre answer=3 text='Rewrite \\(\\frac{1}{4}\\) over 12. Its new top is'
   step3 field=pre answer=4 text='Rewrite \\(\\frac{1}{3}\\) over 12. Its new top is'
   step4 field=pre answer=7 text='Now add the tops over 12: 3 + 4 ='
   step5 field=pre answer=7 text='\\(\\frac{7}{12}\\) is already in lowest terms. The final top is'
   step6 field=pre answer=12 text='and the final bottom is'
   step7 field=say answer=None text='Quick check: \\(\\frac{7}{12}\\) is the answer, in lowest terms.'

bronze[4] Q: \(\frac{2}{3} \times \frac{3}{5}\)
   step0 field=say answer=None text='Multiply straight across: tops together, bottoms together.'
   step1 field=pre answer=6 text='Multiply the tops: 2 × 3 ='
   step2 field=pre answer=15 text='Multiply the bottoms: 3 × 5 ='
   step3 field=pre answer=2 text='Simplify \\(\\frac{6}{15}\\) by dividing by 3. The top becomes'
   step4 field=pre answer=5 text='and the bottom becomes'
   step5 field=say answer=None text='Check: \\(\\frac{2}{5}\\), in lowest terms.'

bronze[6] Q: \(\frac{3}{4} \div \frac{1}{2}\)
   step0 field=say answer=None text='To divide, use Keep, Flip, Change: \\(\\frac{3}{4} \\div \\frac{1}{2}\\) becomes \\(\\frac{3}{4} '
   step1 field=pre answer=6 text='Multiply the tops: 3 × 2 ='
   step2 field=pre answer=4 text='Multiply the bottoms: 4 × 1 ='
   step3 field=pre answer=3 text='Simplify \\(\\frac{6}{4}\\) by dividing by 2. Top becomes'
   step4 field=pre answer=2 text='and the bottom becomes'
   step5 field=say answer=None text='Check: \\(\\frac{3}{2}\\).'

gold[1] Q: \(2\frac{2}{3} \times 1\frac{1}{4}\)
   step0 field=say answer=None text='Change both mixed numbers to improper fractions, then multiply.'
   step1 field=pre answer=8 text='\\(2\\tfrac{2}{3}\\): top = 2 × 3 + 2 ='
   step2 field=pre answer=5 text='\\(1\\tfrac{1}{4}\\): top = 1 × 4 + 1 ='
   step3 field=pre answer=40 text='Multiply the tops: 8 × 5 ='
   step4 field=pre answer=12 text='Multiply the bottoms: 3 × 4 ='
   step5 field=pre answer=10 text='Simplify \\(\\frac{40}{12}\\) by dividing by 4: top ='
   step6 field=pre answer=3 text='bottom ='
   step7 field=say answer=None text='Check: \\(\\frac{10}{3}\\).'

gold[3] Q: \(\frac{5}{6} \div \frac{2}{3} + \frac{1}{4}\)
   step0 field=say answer=None text='Order of operations: division before addition. First do \\(\\frac{5}{6} \\div \\frac{2}{3}\\).'
   step1 field=pre answer=15 text='Flip and multiply the tops: 5 × 3 ='
   step2 field=pre answer=12 text='Multiply the bottoms: 6 × 2 ='
   step3 field=pre answer=5 text='Simplify \\(\\frac{15}{12}\\) by dividing by 3: top ='
   step4 field=pre answer=6 text='Now add \\(\\frac{1}{4}\\). Same bottom 4, so add the tops: 5 + 1 ='
   step5 field=pre answer=3 text='Simplify \\(\\frac{6}{4}\\) by dividing by 2: top ='
   step6 field=pre answer=2 text='bottom ='
   step7 field=say answer=None text='Check: \\(\\frac{3}{2}\\) is 1.5, which fits \\(\\frac{5}{4}+\\frac{1}{4}\\).'

gold[4] Q: \(\frac{3}{7} \times \frac{14}{9} \div \frac{2}{3}\)
   step0 field=say answer=None text='Work left to right. First \\(\\frac{3}{7} \\times \\frac{14}{9}\\).'
   step1 field=pre answer=42 text='Multiply the tops: 3 × 14 ='
   step2 field=pre answer=63 text='Multiply the bottoms: 7 × 9 ='
   step3 field=pre answer=2 text='Simplify \\(\\frac{42}{63}\\) by dividing by 21: top ='
   step4 field=pre answer=6 text='Now divide by \\(\\frac{2}{3}\\): flip and multiply the tops, 2 × 3 ='
   step5 field=pre answer=6 text='Multiply the bottoms: 3 × 2 ='
   step6 field=pre answer=1 text='Simplify \\(\\frac{6}{6}\\): top ='
   step7 field=pre answer=1 text='bottom ='
   step8 field=say answer=None text='Check: \\(\\frac{2}{3} \\div \\frac{2}{3} = 1\\). Correct.'

silver[0] Q: \(\frac{2}{3} + \frac{5}{8}\)
   step0 field=say answer=None text='Add and subtract fractions only when the bottoms match. First make them match.'
   step1 field=pre answer=24 text='The lowest common denominator of 3 and 8 is'
   step2 field=pre answer=16 text='Rewrite \\(\\frac{2}{3}\\) over 24. Its new top is'
   step3 field=pre answer=15 text='Rewrite \\(\\frac{5}{8}\\) over 24. Its new top is'
   step4 field=pre answer=31 text='Now add the tops over 24: 16 + 15 ='
   step5 field=pre answer=31 text='\\(\\frac{31}{24}\\) is already in lowest terms. The final top is'
   step6 field=pre answer=24 text='and the final bottom is'
   step7 field=say answer=None text='Quick check: \\(\\frac{31}{24}\\) is the answer, in lowest terms.'

silver[2] Q: \(1\frac{1}{3} + 2\frac{1}{4}\)
   step0 field=say answer=None text='Turn the mixed numbers into improper fractions first.'
   step1 field=pre answer=4 text='\\(1\\tfrac{1}{3}\\) as an improper fraction: top = 1 × 3 + 1 ='
   step2 field=pre answer=9 text='\\(2\\tfrac{1}{4}\\): top = 2 × 4 + 1 ='
   step3 field=pre answer=12 text='The LCD of 3 and 4 is'
   step4 field=pre answer=16 text='\\(\\frac{4}{3}\\) over 12: top ='
   step5 field=pre answer=27 text='\\(\\frac{9}{4}\\) over 12: top ='
   step6 field=pre answer=43 text='Add the tops over 12: 16 + 27 ='
   step7 field=pre answer=43 text='Already simplest, so the final top is'
   step8 field=pre answer=12 text='and the final bottom is'
   step9 field=say answer=None text='Check: \\(\\frac{43}{12}\\) fits the whole-number parts.'

### board=maths-edexcel
bronze[0] Q: \(\frac{1}{3} + \frac{1}{6}\)
   step0 field=pre answer=6 text='The lowest number both 3 and 6 divide into is the common denominator. It is'
   step1 field=pre answer=2 text='Convert 1/3 into sixths. 3 goes into 6 twice, so the new top is'
   step2 field=say answer=None text='The second fraction, 1/6, is already in sixths.'
   step3 field=pre answer=3 text='Now add the tops: 2 + 1 ='
   step4 field=pre answer=1 text='That gives 3/6. Simplify by dividing top and bottom by 3. Top: 3 ÷ 3 ='
   step5 field=pre answer=2 text='Bottom: 6 ÷ 3 ='
   step6 field=pre answer=3 text='Check: turn 1/2 back into sixths. 1 × 3 ='

bronze[4] Q: \(\frac{4}{5} - \frac{1}{2}\)
   step0 field=pre answer=10 text='The common denominator of 5 and 2 is'
   step1 field=pre answer=8 text='Convert 4/5 into tenths: 5 goes into 10 twice, so 4 × 2 ='
   step2 field=pre answer=5 text='Convert 1/2 into tenths: 2 goes into 10 five times, so 1 × 5 ='
   step3 field=pre answer=3 text='Subtract the tops: 8 − 5 ='
   step4 field=pre answer=10 text='The denominator stays'
   step5 field=pre answer=8 text='Check: 3 and 10 share no factor, so 3/10 is simplest. Add back 3 + 5 ='

bronze[6] Q: \(\frac{1}{3} + \frac{1}{4}\)
   step0 field=pre answer=12 text='The common denominator of 3 and 4 is'
   step1 field=pre answer=4 text='Convert 1/3 into twelfths: 3 goes into 12 four times, so 1 × 4 ='
   step2 field=pre answer=3 text='Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 ='
   step3 field=pre answer=7 text='Add the tops: 4 + 3 ='
   step4 field=pre answer=12 text='The denominator stays'
   step5 field=pre answer=4 text='Check: 7 and 12 share no factor, so 7/12 is simplest. Subtract back 7 − 3 ='

gold[1] Q: \(1\frac{2}{5} \times 2\frac{1}{2}\)
   step0 field=pre answer=7 text='Convert 1 2/5 to an improper fraction. Top: 1 × 5 + 2 ='
   step1 field=pre answer=5 text='Convert 2 1/2 to an improper fraction. Top: 2 × 2 + 1 ='
   step2 field=pre answer=35 text='Multiply the tops: 7 × 5 ='
   step3 field=pre answer=10 text='Multiply the bottoms: 5 × 2 ='
   step4 field=pre answer=7 text='That gives 35/10. Simplify by dividing top and bottom by 5. Top: 35 ÷ 5 ='
   step5 field=pre answer=2 text='Bottom: 10 ÷ 5 ='
   step6 field=pre answer=35 text='Check: turn 7/2 back up by 5. 7 × 5 ='

gold[3] Q: \(\frac{2}{3} + \frac{5}{6} - \frac{1}{4}\)
   step0 field=pre answer=12 text='The common denominator of 3, 6 and 4 is'
   step1 field=pre answer=8 text='Convert 2/3 into twelfths: 3 goes into 12 four times, so 2 × 4 ='
   step2 field=pre answer=10 text='Convert 5/6 into twelfths: 6 goes into 12 twice, so 5 × 2 ='
   step3 field=pre answer=3 text='Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 ='
   step4 field=pre answer=15 text='Combine the tops in order: 8 + 10 − 3 ='
   step5 field=pre answer=5 text='That gives 15/12. Simplify by dividing top and bottom by 3. Top: 15 ÷ 3 ='
   step6 field=pre answer=4 text='Bottom: 12 ÷ 3 ='
   step7 field=pre answer=15 text='Check: turn 5/4 back up by 3. 5 × 3 ='

gold[4] Q: \(\frac{3}{8} \div \frac{3}{4} + \frac{1}{2}\)
   step0 field=say answer=None text='BIDMAS: do the division before the addition. Work out 3/8 ÷ 3/4 first.'
   step1 field=pre answer=4 text='Flip the second fraction. The reciprocal of 3/4 is 4 over 3, so its new top is'
   step2 field=pre answer=12 text='Multiply the tops: 3 × 4 ='
   step3 field=pre answer=24 text='Multiply the bottoms: 8 × 3 ='
   step4 field=pre answer=1 text='Simplify 12/24 to a half. Its top is'
   step5 field=pre answer=2 text='Now add 1/2 + 1/2. Add the tops: 1 + 1 ='
   step6 field=pre answer=1 text='That gives 2/2, which equals'
   step7 field=pre answer=1 text='Check: 3/8 ÷ 3/4 = 0.5 and 0.5 + 0.5 ='

silver[0] Q: \(\frac{3}{4} \div \frac{1}{2}\)
   step0 field=pre answer=2 text='To divide, flip the second fraction. The reciprocal of 1/2 is 2 over 1, so its new top is'
   step1 field=say answer=None text='Now the sum is 3/4 × 2/1.'
   step2 field=pre answer=6 text='Multiply the tops: 3 × 2 ='
   step3 field=pre answer=4 text='Multiply the bottoms: 4 × 1 ='
   step4 field=pre answer=3 text='That gives 6/4. Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 ='
   step5 field=pre answer=2 text='Bottom: 4 ÷ 2 ='
   step6 field=pre answer=3 text='Check: multiply the answer back. 3/2 × 1/2, tops: 3 × 1 ='

silver[2] Q: \(\frac{7}{8} \times \frac{4}{7}\)
   step0 field=pre answer=28 text='Multiply the tops: 7 × 4 ='
   step1 field=pre answer=56 text='Multiply the bottoms: 8 × 7 ='
   step2 field=pre answer=1 text='That gives 28/56. Simplify by dividing top and bottom by 28. Top: 28 ÷ 28 ='
   step3 field=pre answer=2 text='Bottom: 56 ÷ 28 ='
   step4 field=pre answer=28 text='Check: turn 1/2 back up by 28. 1 × 28 ='

### board=maths-ocr
bronze[0] Q: \(\frac{1}{4} + \frac{1}{3}\)
   step0 field=say answer=None text='Add fractions only when the bottoms match. First make them match.'
   step1 field=pre answer=12 text='The lowest common denominator of 4 and 3 is'
   step2 field=pre answer=3 text='Rewrite \\(\\frac{1}{4}\\) over 12. Its new top is'
   step3 field=pre answer=4 text='Rewrite \\(\\frac{1}{3}\\) over 12. Its new top is'
   step4 field=pre answer=7 text='Now add the tops over 12: 3 + 4 ='
   step5 field=pre answer=12 text='\\(\\frac{7}{12}\\) is already in lowest terms, so the final bottom stays'
   step6 field=pre answer=3 text='Check by subtracting back: 7 − 4 ='

bronze[4] Q: \(\frac{1}{2} \times \frac{3}{4}\)
   step0 field=say answer=None text='Multiplying needs no common denominator. Multiply straight across.'
   step1 field=pre answer=3 text='Multiply the tops: 1 × 3 ='
   step2 field=pre answer=8 text='Multiply the bottoms: 2 × 4 ='
   step3 field=pre answer=3 text='Check for common factors: 3 and 8 share only 1, so the top stays'
   step4 field=pre answer=8 text='and the bottom stays'

bronze[6] Q: \(\frac{2}{5} \times \frac{5}{6}\)
   step0 field=say answer=None text='Multiply straight across, then simplify.'
   step1 field=pre answer=10 text='Multiply the tops: 2 × 5 ='
   step2 field=pre answer=30 text='Multiply the bottoms: 5 × 6 ='
   step3 field=pre answer=1 text='Simplify \\(\\frac{10}{30}\\) by dividing top and bottom by 10. Top: 10 ÷ 10 ='
   step4 field=pre answer=3 text='Bottom: 30 ÷ 10 ='
   step5 field=pre answer=10 text='Check: turn 1/3 back up by 10. 1 × 10 ='

gold[1] Q: \(2\frac{1}{2} \times 1\frac{3}{5}\)
   step0 field=say answer=None text='Change both mixed numbers to improper fractions, then multiply.'
   step1 field=pre answer=5 text='\\(2\\frac{1}{2}\\): top = 2 × 2 + 1 ='
   step2 field=pre answer=8 text='\\(1\\frac{3}{5}\\): top = 1 × 5 + 3 ='
   step3 field=say answer=None text='So the sum is \\(\\frac{5}{2} \\times \\frac{8}{5}\\).'
   step4 field=pre answer=40 text='Multiply the tops: 5 × 8 ='
   step5 field=pre answer=10 text='Multiply the bottoms: 2 × 5 ='
   step6 field=pre answer=4 text='Divide: 40 ÷ 10 ='
   step7 field=pre answer=4 text='Check with decimals: 2.5 × 1.6 ='

gold[3] Q: \(\frac{3}{8} \div \frac{9}{16}\)
   step0 field=say answer=None text='To divide, use Keep, Flip, Change: \\(\\frac{3}{8} \\div \\frac{9}{16}\\) becomes \\(\\frac{3}{8}'
   step1 field=pre answer=48 text='Multiply the tops: 3 × 16 ='
   step2 field=pre answer=72 text='Multiply the bottoms: 8 × 9 ='
   step3 field=pre answer=2 text='Simplify \\(\\frac{48}{72}\\) by dividing top and bottom by 24. Top: 48 ÷ 24 ='
   step4 field=pre answer=3 text='Bottom: 72 ÷ 24 ='
   step5 field=pre answer=18 text='Check: multiply back, \\(\\frac{2}{3} \\times \\frac{9}{16}\\), tops 2 × 9 ='

gold[4] Q: \(\frac{5}{6} \times \frac{3}{10} + \frac{1}{4}\)
   step0 field=say answer=None text='Order of operations: multiplication before addition. First do \\(\\frac{5}{6} \\times \\frac{3'
   step1 field=pre answer=15 text='Multiply the tops: 5 × 3 ='
   step2 field=pre answer=60 text='Multiply the bottoms: 6 × 10 ='
   step3 field=pre answer=1 text='Simplify \\(\\frac{15}{60}\\) by dividing top and bottom by 15. Top: 15 ÷ 15 ='
   step4 field=pre answer=4 text='Bottom: 60 ÷ 15 ='
   step5 field=say answer=None text='So \\(\\frac{5}{6} \\times \\frac{3}{10} = \\frac{1}{4}\\). Now add \\(\\frac{1}{4}\\).'
   step6 field=pre answer=2 text='Both are quarters, so add the tops: 1 + 1 ='
   step7 field=pre answer=1 text='That gives \\(\\frac{2}{4}\\). Simplify by dividing top and bottom by 2. Top: 2 ÷ 2 ='
   step8 field=pre answer=2 text='Bottom: 4 ÷ 2 ='
   step9 field=pre answer=2 text='Check: \\(\\frac{1}{4} + \\frac{1}{4} = \\frac{2}{4}\\), which halves to 1 over'

silver[0] Q: \(\frac{2}{3} + \frac{5}{8}\)
   step0 field=say answer=None text='Add fractions only when the bottoms match. Find the common denominator.'
   step1 field=pre answer=24 text='The lowest common denominator of 3 and 8 is'
   step2 field=pre answer=16 text='Rewrite \\(\\frac{2}{3}\\) over 24. Its new top is'
   step3 field=pre answer=15 text='Rewrite \\(\\frac{5}{8}\\) over 24. Its new top is'
   step4 field=pre answer=31 text='Add the tops over 24: 16 + 15 ='
   step5 field=pre answer=24 text='\\(\\frac{31}{24}\\) is already in lowest terms, so the final bottom stays'
   step6 field=pre answer=16 text='Check by subtracting back: 31 − 15 ='

silver[2] Q: \(\frac{3}{5} \times \frac{10}{9}\)
   step0 field=say answer=None text='Multiply straight across, then simplify.'
   step1 field=pre answer=30 text='Multiply the tops: 3 × 10 ='
   step2 field=pre answer=45 text='Multiply the bottoms: 5 × 9 ='
   step3 field=pre answer=2 text='Simplify \\(\\frac{30}{45}\\) by dividing top and bottom by 15. Top: 30 ÷ 15 ='
   step4 field=pre answer=3 text='Bottom: 45 ÷ 15 ='
   step5 field=pre answer=30 text='Check: turn 2/3 back up by 15. 2 × 15 ='

### board=maths-eduqas
bronze[0] Q: \(\frac{1}{4} + \frac{1}{3}\)
   step0 field=pre answer=12 text='The common denominator of 4 and 3 is'
   step1 field=pre answer=3 text='Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 ='
   step2 field=pre answer=4 text='Convert 1/3 into twelfths: 3 goes into 12 four times, so 1 × 4 ='
   step3 field=pre answer=7 text='Add the tops: 3 + 4 ='
   step4 field=pre answer=12 text='The denominator stays'
   step5 field=pre answer=3 text='Check: 7 and 12 share no factor, so 7/12 is simplest. Subtract back 7 − 4 ='

bronze[4] Q: \(\frac{1}{3} + \frac{2}{5}\)
   step0 field=pre answer=15 text='The common denominator of 3 and 5 is'
   step1 field=pre answer=5 text='Convert 1/3 into fifteenths: 3 goes into 15 five times, so 1 × 5 ='
   step2 field=pre answer=6 text='Convert 2/5 into fifteenths: 5 goes into 15 three times, so 2 × 3 ='
   step3 field=pre answer=11 text='Add the tops: 5 + 6 ='
   step4 field=pre answer=15 text='The denominator stays'
   step5 field=pre answer=5 text='Check: 11 and 15 share no factor, so 11/15 is simplest. Subtract back 11 − 6 ='

bronze[6] Q: \(\frac{2}{7} + \frac{3}{7}\)
   step0 field=pre answer=7 text='Both fractions are already sevenths, so the denominator stays'
   step1 field=pre answer=5 text='Add the tops: 2 + 3 ='
   step2 field=pre answer=2 text='Check: 5 and 7 share no factor, so 5/7 is simplest. Subtract back 5 − 3 ='

gold[1] Q: \(2\frac{1}{2} \times 1\frac{1}{3}\)
   step0 field=pre answer=5 text='Convert 2 1/2 to an improper fraction. Top: 2 × 2 + 1 ='
   step1 field=pre answer=4 text='Convert 1 1/3 to an improper fraction. Top: 1 × 3 + 1 ='
   step2 field=pre answer=20 text='Multiply the tops: 5 × 4 ='
   step3 field=pre answer=6 text='Multiply the bottoms: 2 × 3 ='
   step4 field=pre answer=10 text='That gives 20/6. Simplify by dividing top and bottom by 2. Top: 20 ÷ 2 ='
   step5 field=pre answer=3 text='Bottom: 6 ÷ 2 ='
   step6 field=pre answer=20 text='Check: turn 10/3 back up by 2. 10 × 2 ='

gold[3] Q: \(\frac{5}{6} + \frac{7}{8} - \frac{1}{3}\)
   step0 field=pre answer=24 text='The common denominator of 6, 8 and 3 is'
   step1 field=pre answer=20 text='Convert 5/6 into 24ths: 6 goes into 24 four times, so 5 × 4 ='
   step2 field=pre answer=21 text='Convert 7/8 into 24ths: 8 goes into 24 three times, so 7 × 3 ='
   step3 field=pre answer=8 text='Convert 1/3 into 24ths: 3 goes into 24 eight times, so 1 × 8 ='
   step4 field=pre answer=33 text='Combine the tops in order: 20 + 21 − 8 ='
   step5 field=pre answer=11 text='That gives 33/24. Simplify by dividing top and bottom by 3. Top: 33 ÷ 3 ='
   step6 field=pre answer=8 text='Bottom: 24 ÷ 3 ='
   step7 field=pre answer=33 text='Check: turn 11/8 back up by 3. 11 × 3 ='

gold[4] Q: \(2\frac{1}{5} - 1\frac{2}{3}\)
   step0 field=pre answer=11 text='Convert 2 1/5 to an improper fraction. Top: 2 × 5 + 1 ='
   step1 field=pre answer=5 text='Convert 1 2/3 to an improper fraction. Top: 1 × 3 + 2 ='
   step2 field=pre answer=15 text='The common denominator of 5 and 3 is'
   step3 field=pre answer=33 text='Convert 11/5 into fifteenths: 5 goes into 15 three times, so 11 × 3 ='
   step4 field=pre answer=25 text='Convert 5/3 into fifteenths: 3 goes into 15 five times, so 5 × 5 ='
   step5 field=pre answer=8 text='Subtract the tops: 33 − 25 ='
   step6 field=pre answer=15 text='The denominator stays'
   step7 field=pre answer=33 text='Check: 8 and 15 share no factor, so 8/15 is simplest. Add back 8 + 25 ='

silver[0] Q: \(\frac{2}{3} \times \frac{3}{5}\)
   step0 field=pre answer=6 text='Multiplying needs no common denominator. Multiply the tops: 2 × 3 ='
   step1 field=pre answer=15 text='Multiply the bottoms: 3 × 5 ='
   step2 field=pre answer=2 text='That gives 6/15. Simplify by dividing top and bottom by 3. Top: 6 ÷ 3 ='
   step3 field=pre answer=5 text='Bottom: 15 ÷ 3 ='
   step4 field=pre answer=6 text='Check: turn 2/5 back up by 3. 2 × 3 ='

silver[2] Q: \(\frac{3}{4} \div \frac{1}{2}\)
   step0 field=pre answer=2 text='To divide, flip the second fraction. The reciprocal of 1/2 is 2 over 1, so its new top is'
   step1 field=say answer=None text='Now the sum is 3/4 × 2/1.'
   step2 field=pre answer=6 text='Multiply the tops: 3 × 2 ='
   step3 field=pre answer=4 text='Multiply the bottoms: 4 × 1 ='
   step4 field=pre answer=3 text='That gives 6/4. Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 ='
   step5 field=pre answer=2 text='Bottom: 4 ÷ 2 ='
   step6 field=pre answer=3 text='Check: multiply back. 3/2 × 1/2, tops: 3 × 1 ='
