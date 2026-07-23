# apply-pack: algebra__L13.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [low] silver[2] | intro: Now use \(5n - 1\) to find the 15th term. Put \(n = 15\). | fix: Add a one-line bridging step before using the formula, e.g. "So the nth term is 5n - 1 (put the difference in front of n, then add the constant)."
- [low] gold[4] | The sum of any 3 consecutive terms of the sequence 2n + 1 is always divisible by | fix: Drop the divisibility clause and ask the task plainly, e.g. 'Add the terms n, n+1 and n+2 of the sequence 2n + 1. What is the total?'
- [low] gold[4] | Positive means 9 − 2n > 0, so 2n < 9, giving n < 4.5. The largest whole n is [bo | fix: State the rule first ("the rule is 9 − 2n"), then break the inequality into its own step ending at n < 4.5, and ask for the largest whole n separately.

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
silver[2] Q: Two sequences have nth terms \(3n + 1\) and \(5n - 9\). Find the smallest value that appea
   step0 field=say answer=None text='A shared value must appear in BOTH lists. \\(3n + 1\\) gives 4, 7, 10, 13, 16, ... and \\(5n '
   step1 field=pre answer=16 text='The 5th term of \\(3n + 1\\): 3 × 5 + 1 ='
   step2 field=pre answer=25 text='Is 16 in \\(5n − 9\\)? Solve \\(5m − 9 = 16\\), so 5m = 16 + 9 ='
   step3 field=pre answer=5 text='m = 25 ÷ 5 ='
   step4 field=pre answer=16 text='Confirm 16 in the first: 3 × 5 + 1 ='

### board=maths-edexcel
gold[4] Q: Find the first term greater than 200 in the sequence 3, 8, 13, 18, ...
   step0 field=say answer=None text='Find the rule for \\(3, 8, 13, 18, \\ldots\\) first.'
   step1 field=pre answer=5 text='Common difference: 8 − 3 ='
   step2 field=pre answer=-2 text='Constant: first term − d = 3 − 5 ='
   step3 field=say answer=None text='We want the first term over 200, so solve \\(5n - 2 > 200\\). Add 2 to both sides.'
   step4 field=pre answer=202 text='200 + 2 ='
   step5 field=say answer=None text='Now find the smallest whole \\(n\\). Since \\(5 \\times 40 = 200\\) is too small, try \\(n = 41\\'
   step6 field=pre answer=205 text='5 × 41 ='
   step7 field=pre answer=203 text='The term value: 205 − 2 ='

silver[2] Q: Find the 15th term of the sequence 4, 9, 14, 19, ...
   step0 field=say answer=None text='The formula is not given, so find it first. Start with the common difference.'
   step1 field=pre answer=5 text='Common difference: 9 − 4 ='
   step2 field=pre answer=-1 text='Constant: first term − d = 4 − 5 ='
   step3 field=say answer=None text='Now use \\(5n - 1\\) to find the 15th term. Put \\(n = 15\\).'
   step4 field=pre answer=75 text='5 × 15 ='
   step5 field=pre answer=74 text='Subtract 1: 75 − 1 ='
   step6 field=pre answer=14 text='Check the rule on the 3rd term: 5 × 3 − 1 ='

### board=maths-ocr
gold[4] Q: The sum of any 3 consecutive terms of the sequence \(2n + 1\) is always divisible by 3. Wh

silver[2] Q: Find the nth term of \(6, 3, 0, -3, ...\)

### board=maths-eduqas
gold[4] Q: An arithmetic sequence has first term \(a = 7\) and common difference \(d = -2\). How many
   step0 field=say answer=None text='Find the nth term rule, then see where it stops being positive.'
   step1 field=pre answer=9 text='Zero term: first term minus d = 7 − (−2) ='
   step2 field=pre answer=4 text='Positive means 9 − 2n > 0, so 2n < 9, giving n < 4.5. The largest whole n is'
   step3 field=pre answer=1 text='Check term 4: 9 − 2 × 4 ='
   step4 field=pre answer=-1 text='Check term 5: 9 − 2 × 5 ='

silver[2] Q: Find the nth term of \(20, 17, 14, 11, ...\)
