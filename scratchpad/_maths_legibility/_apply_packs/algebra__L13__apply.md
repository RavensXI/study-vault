# apply-pack: algebra__L13.md

Return prose-only edits. NEVER change an answer, NEVER add or remove a step.
Only reword an existing step's pre/say/done text to be clearer to a struggling 15-year-old.

## FINDINGS to address (from readers):
- [medium] gold[1] | Total quarters: 28 + 2 + 1 = [box=31] | fix: Add explicit conversion asks for the fractional terms and name the subtotal, e.g. 'Half in quarters: 1/2 = [box=2]', 'Quarter in quarters: 1/4 = [box=1]', then 
- [medium] gold[3] | First gap is 8 - k; second gap is (2k + 1) - 8 = 2k - 7. Set 8 - k = 2k - 7, add | fix: Break it into staged asks with their own boxes: 'Second gap: (2k + 1) - 8 = 2k - [box=7]', then 'Set the gaps equal: 8 - k = 2k - 7. Add k to both sides: 8 = 3k
- [medium] gold[2] | Check: the middle term 7 times the 5 terms: 5 × 7 = [box=35] | fix: Rewrite as: "Check: the middle term (7) times the number of terms (5): 7 × 5 ="
- [medium] gold[2] | 6th term: 100 halved five times, 100 ÷ 32 = [box=3.125] | fix: Either show the halving chain (100 → 50 → 25 → 12.5 → 6.25 → 3.125) to match the later steps, or insert 'halving five times = ÷2⁵ = ÷32' before the division.
- [medium] bronze[0] | Zero term: 4 − 5 = [box=-1, NO label] | fix: Introduce it in plain words the first time, e.g. "The term that would sit before the 1st one (the 0th term): first term − common difference = 4 − 5 =". Then "Ad
- [medium] bronze[0] | The 5n part of the 10th term: 5 × 10 = [box=50, NO label] | fix: Add a stating line before the jump: "So the rule is 5n − 1. Now, for n = 10, the 5n part is 5 × 10 =".
- [medium] gold[0] | Check nothing smaller is shared: is 7 in the second list? 3m + 2 = 7 gives 3m =  | fix: Finish the reasoning: "3m = 5, but 5 ÷ 3 is not a whole number, so 7 is not in the second list — 11 really is the smallest shared value."
- [medium] gold[3] | The bracket 2a + (n − 1)d = 8 + 3(n − 1) = 3n + 5, so \frac{n}{2}(3n + 5) = 175. | fix: Split it: first ask "Simplify the bracket: 8 + 3(n − 1) = 3n + 5" as its own step, then a separate step "Multiply both sides by 2: n(3n + 5) = 350".

## REAL walk data per board (edit against THIS text):
### board=maths-aqa
bronze[0] Q: Find the 20th term of the sequence \(3, 8, 13, 18, ...\)
   step0 field=say answer=None text='A straight-line sequence, so first build its rule.'
   step1 field=pre answer=5 text='Common difference: 8 − 3 ='
   step2 field=pre answer=-2 text='Zero term: 3 − 5 ='
   step3 field=pre answer=100 text='The dn part of the 20th term: 5 × 20 ='
   step4 field=pre answer=98 text='Add the constant: 100 − 2 ='
   step5 field=pre answer=3 text='Check the rule rebuilds term 1: 5 × 1 − 2 ='

gold[0] Q: The sum of the first \(n\) terms of a sequence is \(S_n = n^2 + 3n\). Find the 10th term o
   step0 field=say answer=None text='\\(S_n\\) is the running total. The 10th term is the jump from \\(S_9\\) to \\(S_{10}\\).'
   step1 field=pre answer=130 text='S₁₀ = 10² + 3 × 10 = 100 + 30 ='
   step2 field=pre answer=108 text='S₉ = 9² + 3 × 9 = 81 + 27 ='
   step3 field=pre answer=22 text='10th term = S₁₀ − S₉ = 130 − 108 ='
   step4 field=pre answer=4 text='Check the 1st term: S₁ = 1² + 3 × 1 ='

gold[1] Q: A geometric sequence has first term 4 and common ratio \(\frac{1}{2}\). Find the sum of th
   step0 field=say answer=None text='The terms halve each time: 4, 2, 1, 1/2, 1/4. Turn every term into quarters so they add ea'
   step1 field=pre answer=16 text='4 whole = 4 × 4 quarters ='
   step2 field=pre answer=8 text='2 whole = 2 × 4 quarters ='
   step3 field=pre answer=4 text='1 whole ='
   step4 field=pre answer=31 text='Total quarters: 28 + 2 + 1 ='
   step5 field=pre answer=7.75 text='Check as a decimal: 31 ÷ 4 ='

gold[2] Q: Prove the nth term of \(5, 8, 11, 14, ...\) is \(3n + 2\). What is the 100th term?
   step0 field=say answer=None text='First confirm the rule really is \\(3n + 2\\).'
   step1 field=pre answer=3 text='Common difference: 8 − 5 ='
   step2 field=pre answer=2 text='Zero term: 5 − 3 ='
   step3 field=pre answer=300 text='The 3n part of the 100th term: 3 × 100 ='
   step4 field=pre answer=302 text='Add the constant: 300 + 2 ='
   step5 field=pre answer=8 text='Check the rule at n = 2: 3 × 2 + 2 ='

gold[3] Q: A sequence starts \(k, 8, 2k+1, ...\) and is arithmetic. Find \(k\).
   step0 field=say answer=None text='Arithmetic means the gap between terms is the same, so set the two gaps equal.'
   step1 field=pre answer=15 text='First gap is \\(8 - k\\); second gap is \\((2k + 1) - 8 = 2k - 7\\). Set \\(8 - k = 2k - 7\\), a'
   step2 field=pre answer=5 text='Divide by 3: k = 15 ÷ 3 ='
   step3 field=pre answer=3 text='Check the gaps with k = 5: the terms are 5, 8, 11, so each gap is'

### board=maths-edexcel
bronze[0] Q: Find the nth term of 2, 5, 8, 11, ...

gold[0] Q: The nth term of a sequence is \(3n + 7\). Which term has value 100?
   step0 field=say answer=None text='We want the position whose value is 100, so solve \\(3n + 7 = 100\\).'
   step1 field=pre answer=93 text='Take 7 from both sides: 100 − 7 ='
   step2 field=pre answer=31 text='Divide by 3: 93 ÷ 3 ='
   step3 field=pre answer=100 text='Check: 3 × 31 + 7 ='

gold[1] Q: Two sequences: \(4n + 1\) and \(3n + 5\). At what position do they first have the same val
   step0 field=say answer=None text='The two sequences are equal when \\(4n + 1 = 3n + 5\\). Get the n terms on one side by subtr'
   step1 field=pre answer=1 text='4n − 3n ='
   step2 field=pre answer=4 text='Take 1 from both sides: 5 − 1 ='
   step3 field=pre answer=17 text='Check the first sequence at n = 4: 4 × 4 + 1 ='
   step4 field=pre answer=17 text='Check the second at n = 4: 3 × 4 + 5 ='

gold[2] Q: Find the sum of the first 5 terms of the sequence with nth term \(2n + 1\)
   step0 field=say answer=None text='List the first five terms of \\(2n + 1\\). Each is 2 more than the last.'
   step1 field=pre answer=11 text='The 5th term: 2 × 5 + 1 ='
   step2 field=say answer=None text='Now add the five terms together.'
   step3 field=pre answer=15 text='3 + 5 + 7 ='
   step4 field=pre answer=35 text='15 + 9 + 11 ='
   step5 field=pre answer=35 text='Check: the middle term 7 times the 5 terms: 5 × 7 ='

gold[3] Q: The 3rd term of a sequence is 11 and the 7th term is 27. Find the nth term.

### board=maths-ocr
bronze[0] Q: Find the 20th term of \(3, 7, 11, 15, ...\)
   step0 field=say answer=None text='A straight-line sequence, so build its rule first.'
   step1 field=pre answer=4 text='Common difference: 7 − 3 ='
   step2 field=pre answer=-1 text='Zero term: 3 − 4 ='
   step3 field=pre answer=80 text='The dn part of the 20th term: 4 × 20 ='
   step4 field=pre answer=79 text='Subtract the constant: 80 − 1 ='
   step5 field=pre answer=3 text='Check the rule rebuilds term 1: 4 × 1 − 1 ='

gold[0] Q: The first term of a geometric sequence is 2 and the 4th term is 54. Find the common ratio.
   step0 field=say answer=None text='Geometric: the 4th term is the first term multiplied by r three times, so \\(2 × r^3 = 54\\)'
   step1 field=pre answer=27 text='Divide by the first term: r³ = 54 ÷ 2 ='
   step2 field=pre answer=3 text='Cube root: r = ∛27 ='
   step3 field=pre answer=54 text='Check the 4th term: 2 × 3³ = 2 × 27 ='

gold[1] Q: The nth term of a sequence is \(2n^2 - 3\). Find the 5th term.
   step0 field=say answer=None text='The rule is given. Follow BIDMAS: square n first, then multiply, then subtract.'
   step1 field=pre answer=25 text='Square n: 5² ='
   step2 field=pre answer=50 text='Times 2: 2 × 25 ='
   step3 field=pre answer=47 text='Subtract 3: 50 − 3 ='
   step4 field=pre answer=-1 text='Check the 1st term: 2 × 1² − 3 ='

gold[2] Q: A geometric sequence has first term 100 and common ratio 0.5. After how many terms is the 
   step0 field=say answer=None text='Halve from 100 and count terms until you drop below 1.'
   step1 field=pre answer=3.125 text='6th term: 100 halved five times, 100 ÷ 32 ='
   step2 field=pre answer=1.5625 text='7th term: halve again, 3.125 ÷ 2 ='
   step3 field=pre answer=0.78125 text='8th term: halve again, 1.5625 ÷ 2 ='
   step4 field=pre answer=8 text='That is below 1. Which term number is it?'

gold[3] Q: A sequence starts \(1, 1, 2, 3, 5, 8, 13, ...\) What is the 10th term?
   step0 field=say answer=None text='Each term is the sum of the two before it. Keep adding until the 10th.'
   step1 field=pre answer=21 text='The 7th term is 13. The 8th: 8 + 13 ='
   step2 field=pre answer=34 text='9th term: 13 + 21 ='
   step3 field=pre answer=55 text='10th term: 21 + 34 ='
   step4 field=pre answer=10 text='Count the terms 1, 1, 2, 3, 5, 8, 13, 21, 34, 55: the last is term number'

### board=maths-eduqas
bronze[0] Q: Find the 10th term of the sequence \(4, 9, 14, 19, ...\)
   step0 field=say answer=None text='A straight-line sequence, so build its rule first.'
   step1 field=pre answer=5 text='Common difference: 9 − 4 ='
   step2 field=pre answer=-1 text='Zero term: 4 − 5 ='
   step3 field=pre answer=50 text='The 5n part of the 10th term: 5 × 10 ='
   step4 field=pre answer=49 text='Add the zero term: 50 − 1 ='
   step5 field=pre answer=4 text='Check the rule rebuilds term 1: 5 × 1 − 1 ='

gold[0] Q: Two sequences: \(3, 7, 11, 15, ...\) and \(5, 8, 11, 14, ...\). Find the smallest number t
   step0 field=say answer=None text='A shared value must appear in BOTH lists. First list: 3, 7, 11, 15, ... Second list: 5, 8,'
   step1 field=pre answer=11 text='The 3rd term of the first list: 4 × 3 − 1 ='
   step2 field=pre answer=9 text='Is 11 in the second list? Solve \\(3m + 2 = 11\\), so 3m = 11 − 2 ='
   step3 field=pre answer=3 text='m = 9 ÷ 3 ='
   step4 field=pre answer=5 text='Check nothing smaller is shared: is 7 in the second list? 3m + 2 = 7 gives 3m ='

gold[1] Q: The nth term is \(an + b\). The 3rd term is \(11\) and the 7th is \(23\). Find \(a\).
   step0 field=say answer=None text='Two equations: 3rd term \\(3a + b = 11\\), and 7th term \\(7a + b = 23\\). Subtract to remove '
   step1 field=pre answer=12 text='Subtract the equations: (7a + b) − (3a + b) leaves 4a. The right side: 23 − 11 ='
   step2 field=pre answer=3 text='So 4a = 12. Divide by 4: a = 12 ÷ 4 ='
   step3 field=pre answer=4 text='Check the step count: from the 3rd to the 7th term is 7 − 3 ='

gold[2] Q: Find the value of \(b\) (from the previous question).
   step0 field=say answer=None text='Use a = 3 in the 3rd-term equation \\(3a + b = 11\\).'
   step1 field=pre answer=9 text='Work out 3a: 3 × 3 ='
   step2 field=pre answer=2 text='So 9 + b = 11. Then b = 11 − 9 ='
   step3 field=pre answer=23 text='Check the 7th term: 7 × 3 + 2 ='

gold[3] Q: The sum of the first \(n\) terms of \(4, 7, 10, ...\) is 175. Find \(n\).
   step0 field=say answer=None text='Use the sum formula \\(S_n = \\frac{n}{2}(2a + (n-1)d)\\) with \\(a = 4\\), \\(d = 3\\).'
   step1 field=pre answer=350 text='The bracket 2a + (n − 1)d = 8 + 3(n − 1) = 3n + 5, so \\(\\frac{n}{2}(3n + 5) = 175\\). Times'
   step2 field=pre answer=10 text='Expand to \\(3n^2 + 5n - 350 = 0\\), which factorises to (n − 10)(3n + 35) = 0. The positive'
   step3 field=pre answer=175 text='Check: the 10th term is 3 × 10 + 1 = 31, so \\(S_{10} = \\frac{10}{2}(4 + 31)\\) = 5 × 35 ='
