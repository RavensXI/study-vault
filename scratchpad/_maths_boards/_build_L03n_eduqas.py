# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L03n_live.json", encoding="utf-8"))

# ---- preserved fields (byte-for-byte) ----
method_card    = live["method_card"]
topic_links    = live["topic_links"]
related_videos = live["related_videos"]
worked_examples= live["worked_examples"]

def mis(pattern, message, expect, note, check=None):
    if check is None:
        check = "wrong" if expect is None else ("equals_%s" % expect)
    d = {"pattern": pattern, "check": check, "expect": expect, "message": message}
    if note:
        d["note"] = note
    return d

def prob(display, sol, calc, hint, steps, misc):
    return {"display": display, "solutions": [sol], "calculator": calc,
            "input_type": "single_value", "hint": hint,
            "misconceptions": misc, "guided_steps": steps}

# ================= BRONZE =================
bronze = []

# b0
bronze.append(prob(
 "Round \\(3.472\\) to 1 decimal place.", 3.5, False,
 "The digit after your last kept place decides: 5 or more rounds up.",
 [
  {"pre":"To round to 1 decimal place, keep one digit after the point. In 3.472 that kept digit is ","answer":4,"hint":"The first digit after the decimal point."},
  {"pre":"The deciding digit is the next one along: ","answer":7,"hint":"The second digit after the point."},
  {"pre":"7 is 5 or more, so round the kept 4 up. 4 + 1 = ","answer":5,"hint":"Add 1 to the kept digit.","phase":"substitute"},
  {"pre":"The whole part 3 stays. Written to 1 dp the number is 3.5, so type ","answer":3.5,"hint":"Three point five.","done":"So 3.472 rounds to 3.5 to 1 dp."},
  {"pre":"Check: the halfway value between 3.4 and 3.5 is ","answer":3.45,"hint":"Add 0.05 to 3.4.","done":"3.472 is above 3.45, so it rounds up to 3.5. Correct."},
 ],
 [mis("truncate","The deciding digit is 7, which is 5 or more, so round the 4 up. 3.472 to 1 dp is 3.5, not 3.4.",3.4,"Student truncates instead of rounding: keeps 3.4."),
  mis("wrong_places","1 decimal place means only one digit after the point. 3.47 has two, so round again to 3.5.",3.47,"Student rounds to 2 dp instead of 1 dp.")]))

# b1  rounds down
bronze.append(prob(
 "Round \\(7.849\\) to 1 decimal place.", 7.8, False,
 "Look only at the next digit after the tenths; if it is under 5, round down.",
 [
  {"pre":"Keep one digit after the point. In 7.849 the kept digit is ","answer":8,"hint":"The first digit after the point."},
  {"pre":"The deciding digit is the next one along: ","answer":4,"hint":"The second digit after the point."},
  {"pre":"4 is less than 5, so the kept 8 stays the same. The kept digit is still ","answer":8,"hint":"Under 5 means round down, leave it as it is.","phase":"substitute"},
  {"pre":"Ignore the digits after it. To 1 dp the number is 7.8, so type ","answer":7.8,"hint":"Seven point eight.","done":"So 7.849 rounds to 7.8 to 1 dp."},
  {"pre":"Check: the halfway value between 7.8 and 7.9 is ","answer":7.85,"hint":"Add 0.05 to 7.8.","done":"7.849 is below 7.85, so it rounds down to 7.8. Correct."},
 ],
 [mis("chain_round","Only the digit straight after the tenths decides. That is 4, which is under 5, so round down to 7.8. Do not round the 9 into the 4 first.",7.9,"Student rounds right to left: 9 lifts 4 to 5, then 5 lifts 8 to 9, giving 7.9.")]))

# b2
bronze.append(prob(
 "Round \\(12.365\\) to 2 decimal places.", 12.37, False,
 "The deciding digit is the third decimal, and an exact 5 rounds up.",
 [
  {"pre":"Keep two digits after the point. In 12.365 the kept digits are 3 and ","answer":6,"hint":"The second digit after the point."},
  {"pre":"The deciding digit is the next one along: ","answer":5,"hint":"The third digit after the point."},
  {"pre":"5 counts as round up, so the kept 6 goes up. 6 + 1 = ","answer":7,"hint":"Add 1 to the last kept digit.","phase":"substitute"},
  {"pre":"The other digits stay. To 2 dp the number is 12.37, so type ","answer":12.37,"hint":"Twelve point three seven.","done":"So 12.365 rounds to 12.37 to 2 dp."},
  {"pre":"Check: the halfway value between 12.36 and 12.37 is ","answer":12.365,"hint":"Add 0.005 to 12.36.","done":"12.365 is exactly halfway, and a 5 rounds up, so 12.37. Correct."},
 ],
 [mis("wrong_places","2 decimal places means two digits after the point. 12.365 to 2 dp is 12.37; 12.4 is only 1 dp.",12.4,"Student rounds to 1 dp instead of 2 dp: deciding digit 6 lifts 3 to 4, giving 12.4.")]))

# b3
bronze.append(prob(
 "Round \\(0.5482\\) to 2 decimal places.", 0.55, False,
 "Check the third decimal place to decide whether the second rounds up.",
 [
  {"pre":"Keep two digits after the point. In 0.5482 the kept digits are 5 and ","answer":4,"hint":"The second digit after the point."},
  {"pre":"The deciding digit is the next one along: ","answer":8,"hint":"The third digit after the point."},
  {"pre":"8 is 5 or more, so round the kept 4 up. 4 + 1 = ","answer":5,"hint":"Add 1 to the last kept digit.","phase":"substitute"},
  {"pre":"To 2 dp the number is 0.55, so type ","answer":0.55,"hint":"Zero point five five.","done":"So 0.5482 rounds to 0.55 to 2 dp."},
  {"pre":"Check: the halfway value between 0.54 and 0.55 is ","answer":0.545,"hint":"Add 0.005 to 0.54.","done":"0.5482 is above 0.545, so it rounds up to 0.55. Correct."},
 ],
 [mis("wrong_places","2 decimal places means two digits after the point. 0.5482 to 2 dp is 0.55; 0.5 is only 1 dp.",0.5,"Student rounds to 1 dp instead of 2 dp: deciding digit 4 is under 5, giving 0.5.")]))

# b4  add
bronze.append(prob(
 "\\(3.6 + 2.45\\)", 6.05, False,
 "Write 3.6 as 3.60, line up the points, then add.",
 [
  {"pre":"Line up the decimal points. Write 3.6 as 3.60 so both have two decimal places. Add the hundredths: 0 + 5 = ","answer":5,"hint":"Nothing in 3.60's hundredths, plus 5."},
  {"pre":"Add the tenths: 6 + 4 = ","answer":10,"hint":"6 tenths plus 4 tenths.","phase":"substitute"},
  {"pre":"That is 10 tenths: write 0, carry 1 to the units. Add the units with the carry: 3 + 2 + 1 = ","answer":6,"hint":"3 plus 2 plus the carried 1."},
  {"pre":"Put it together: 6 units, 0 tenths, 5 hundredths gives 6.05, so type ","answer":6.05,"hint":"Six point zero five.","done":"So 3.6 + 2.45 = 6.05."},
  {"pre":"Check: subtract back 6.05 − 2.45 = ","answer":3.6,"hint":"Should return the first number.","done":"6.05 − 2.45 = 3.6, so the sum is right."},
 ],
 [mis("misalign","Line up the decimal points, not the last digits. Write 3.6 as 3.60, then 3.60 + 2.45 = 6.05.",None,"Right-aligning the digit strings scrambles place value; no single determinate wrong answer.")]))

# b5  subtract
bronze.append(prob(
 "\\(5.2 - 1.87\\)", 3.33, False,
 "Write 5.2 as 5.20, line up the points, then subtract with borrowing.",
 [
  {"pre":"Line up the decimal points. Write 5.2 as 5.20. Subtract the hundredths: 0 − 7 needs a borrow, so 10 − 7 = ","answer":3,"hint":"Borrow 1 from the tenths, then 10 − 7."},
  {"pre":"The tenths dropped to 1 after lending. Subtract the tenths: 1 − 8 needs another borrow, so 11 − 8 = ","answer":3,"hint":"Borrow 1 from the units, then 11 − 8.","phase":"substitute"},
  {"pre":"The units dropped to 4 after lending. Subtract the units: 4 − 1 = ","answer":3,"hint":"5 became 4 after the borrow."},
  {"pre":"Put it together: 3 units, 3 tenths, 3 hundredths gives 3.33, so type ","answer":3.33,"hint":"Three point three three.","done":"So 5.2 − 1.87 = 3.33."},
  {"pre":"Check: add back 3.33 + 1.87 = ","answer":5.2,"hint":"Should return the first number.","done":"3.33 + 1.87 = 5.20 = 5.2, so the subtraction is right."},
 ],
 [mis("no_borrow","Line up the points and borrow. 5.20 − 1.87 = 3.33. Do not take the smaller digit from the larger in each column.",4.67,"Column-wise absolute differences: |5-1|=4, |2-8|=6, |0-7|=7 gives 4.67.")]))

# b6  multiply
bronze.append(prob(
 "\\(0.6 \\times 0.3\\)", 0.18, False,
 "Multiply 6 × 3, then put two decimal places into the answer.",
 [
  {"pre":"Ignore the decimals for now. Multiply the digits: 6 × 3 = ","answer":18,"hint":"Six times three."},
  {"pre":"Count the decimal places in the question: 0.6 has 1 and 0.3 has 1, so altogether ","answer":2,"hint":"One plus one.","phase":"substitute"},
  {"pre":"Put 2 decimal places into 18: that gives 0.18, so type ","answer":0.18,"hint":"18 becomes 0.18 with two decimal places.","done":"So 0.6 × 0.3 = 0.18."},
  {"pre":"Check: half of 0.3 is 0.15, and 0.18 sits just above it, a sensible size. Half of 0.3 = ","answer":0.15,"hint":"0.3 divided by 2.","done":"0.18 is just above 0.15, so it is right."},
 ],
 [mis("decimal_count","6 × 3 = 18, and there are two decimal places in total, so 0.6 × 0.3 = 0.18, not 1.8.",1.8,"Student uses only one decimal place: 1.8.")]))

# b7  divide
bronze.append(prob(
 "\\(4.8 \\div 0.6\\)", 8, False,
 "Multiply both numbers by 10 so you are dividing by a whole number.",
 [
  {"pre":"Scale both numbers so the divisor is a whole number. Multiply both by 10. 0.6 × 10 = ","answer":6,"hint":"Move the point one place right."},
  {"pre":"Do the same to 4.8: 4.8 × 10 = ","answer":48,"hint":"Move the point one place right.","phase":"substitute"},
  {"pre":"Now divide the whole numbers: 48 ÷ 6 = ","answer":8,"hint":"How many sixes make 48.","done":"So 4.8 ÷ 0.6 = 8."},
  {"pre":"Check: multiply back 8 × 0.6 = ","answer":4.8,"hint":"Should return the first number.","done":"8 × 0.6 = 4.8, so the answer is right."},
 ],
 [mis("divide_unscaled","Scale both up by 10: 48 ÷ 6 = 8. Dividing 4.8 by 6 instead gives 0.8, which is ten times too small.",0.8,"Student divides 4.8 by 6 without scaling the divisor.")]))

# ================= SILVER =================
silver = []

# s0
silver.append(prob(
 "Round \\(4567\\) to 2 significant figures.", 4600, False,
 "Keep the first two digits, use the third to decide, then fill with zeros.",
 [
  {"pre":"The first significant figure is the first non-zero digit. In 4567 that is ","answer":4,"hint":"The leftmost digit."},
  {"pre":"Keeping two significant figures, the second kept digit is ","answer":5,"hint":"The next digit after the 4."},
  {"pre":"The deciding digit is the next one along: ","answer":6,"hint":"The third digit, 6.","phase":"substitute"},
  {"pre":"6 is 5 or more, so round the kept 5 up. 5 + 1 = ","answer":6,"hint":"Add 1 to the last kept digit."},
  {"pre":"Replace the remaining digits with zeros to hold the size. The number is 4600, so type ","answer":4600,"hint":"Four thousand six hundred.","done":"So 4567 to 2 s.f. is 4600."},
 ],
 [mis("too_many_sf","2 significant figures means keep only the first two digits, then use the next to round: 4600, not 4570.",4570,"Student rounds to 3 s.f. (4570) instead of 2."),
  mis("drop_zeros","Keep the place value: after rounding, 46 hundreds is 4600, not 46.",46,"Student drops the place-holding zeros, writing 46.")]))

# s1  rounds down
silver.append(prob(
 "Round \\(0.003 72\\) to 2 significant figures.", 0.0037, False,
 "Ignore the leading zeros; count significant figures from the first 3.",
 [
  {"pre":"Leading zeros do not count. The first significant figure is the first non-zero digit: ","answer":3,"hint":"The 3 in 0.00372."},
  {"pre":"The second significant figure is the next digit: ","answer":7,"hint":"The digit after the 3."},
  {"pre":"The deciding digit is the next one along: ","answer":2,"hint":"The digit after the 7.","phase":"substitute"},
  {"pre":"2 is less than 5, so the kept 7 stays. The last kept digit is still ","answer":7,"hint":"Under 5 means round down, leave it."},
  {"pre":"Keeping the place value, the number is 0.0037, so type ","answer":0.0037,"hint":"Zero point zero zero three seven.","done":"So 0.00372 to 2 s.f. is 0.0037."},
 ],
 [mis("round_up_wrong","The deciding digit is 2, which is under 5, so round down: the answer is 0.0037.",None,"Student rounds up despite a deciding digit below 5; the near-value is within rounding tolerance and cannot be uniquely diagnosed.")]))

# s2
silver.append(prob(
 "Round \\(38 450\\) to 3 significant figures.", 38500, False,
 "Keep the first three digits, and an exact 5 rounds up.",
 [
  {"pre":"The first three significant figures are 3, 8 and ","answer":4,"hint":"The third digit from the left."},
  {"pre":"The deciding digit is the next one along: ","answer":5,"hint":"The fourth digit, 5.","phase":"substitute"},
  {"pre":"5 counts as round up, so the kept 4 goes up. 4 + 1 = ","answer":5,"hint":"Add 1 to the last kept digit."},
  {"pre":"Replace the remaining digits with zeros. The number is 38500, so type ","answer":38500,"hint":"Thirty-eight thousand five hundred.","done":"So 38450 to 3 s.f. is 38500."},
 ],
 [mis("round_5_down","A deciding digit of 5 rounds up, so 38450 to 3 s.f. is 38500, not 38400.",38400,"Student rounds the exact 5 down.")]))

# s3  multiply
silver.append(prob(
 "\\(0.24 \\times 0.5\\)", 0.12, False,
 "Halve 0.24, or multiply 24 × 5 and place three decimals.",
 [
  {"pre":"Ignore the decimals for now. Multiply the digits: 24 × 5 = ","answer":120,"hint":"Twenty-four times five."},
  {"pre":"Count the decimal places: 0.24 has 2 and 0.5 has 1, so altogether ","answer":3,"hint":"Two plus one.","phase":"substitute"},
  {"pre":"Put 3 decimal places into 120: that is 0.120, which is 0.12. Type ","answer":0.12,"hint":"120 with three decimal places is 0.120 = 0.12.","done":"So 0.24 × 0.5 = 0.12."},
  {"pre":"Check: 0.5 is a half, so the answer is half of 0.24. Half of 0.24 = ","answer":0.12,"hint":"0.24 divided by 2.","done":"Half of 0.24 is 0.12, matching. Correct."},
 ],
 [mis("ignore_decimal","0.5 is a half, so 0.24 × 0.5 is half of 0.24, which is 0.12, not 1.2.",1.2,"Student multiplies by 5 as if by a whole number: 1.2.")]))

# s4  divide
silver.append(prob(
 "\\(7.2 \\div 0.09\\)", 80, False,
 "Multiply both numbers by 100 so you are dividing by a whole number.",
 [
  {"pre":"Scale both numbers so the divisor is a whole number. The divisor 0.09 has two decimal places, so multiply both by 100. 0.09 × 100 = ","answer":9,"hint":"Move the point two places right."},
  {"pre":"Do the same to 7.2: 7.2 × 100 = ","answer":720,"hint":"Move the point two places right.","phase":"substitute"},
  {"pre":"Now divide the whole numbers: 720 ÷ 9 = ","answer":80,"hint":"How many nines make 720.","done":"So 7.2 ÷ 0.09 = 80."},
  {"pre":"Check: multiply back 80 × 0.09 = ","answer":7.2,"hint":"Should return the first number.","done":"80 × 0.09 = 7.2, so the answer is right."},
 ],
 [mis("divide_unscaled","Scale both up by 100: 720 ÷ 9 = 80. Dividing 7.2 by 9 gives 0.8, which is far too small.",0.8,"Student divides by 9 without scaling: 0.8.")]))

# s5  REPAIRED estimate (was duplicate answer 80)
silver.append(prob(
 "Estimate \\(6.2 \\times 4.8\\) by rounding each to 1 significant figure.", 30, False,
 "Round each number to 1 significant figure, then multiply.",
 [
  {"pre":"Round 6.2 to 1 significant figure: ","answer":6,"hint":"6.2 is nearer 6 than 7."},
  {"pre":"Round 4.8 to 1 significant figure: ","answer":5,"hint":"4.8 is nearer 5 than 4.","phase":"substitute"},
  {"pre":"Multiply the rounded values: 6 × 5 = ","answer":30,"hint":"Six times five.","done":"So 6.2 × 4.8 is about 30."},
  {"pre":"Check: the exact value 6.2 × 4.8 = 29.76. Rounded to 1 s.f. that is ","answer":30,"hint":"29.76 is nearest 30.","done":"The estimate 30 matches the rounded exact value. Correct."},
 ],
 [mis("round_down_wrong","Round 4.8 to 1 s.f.: it is nearer 5 than 4, so use 6 × 5 = 30, not 6 × 4 = 24.",24,"Student rounds 4.8 down to 4.")]))

# s6
silver.append(prob(
 "Round \\(0.06049\\) to 3 significant figures.", 0.0605, False,
 "Ignore the leading zeros; the first significant figure is the 6.",
 [
  {"pre":"Leading zeros do not count. The first significant figure is ","answer":6,"hint":"The first non-zero digit."},
  {"pre":"The next two significant figures are 0 and ","answer":4,"hint":"After the 6 comes a 0, then a 4."},
  {"pre":"The deciding digit is the next one along: ","answer":9,"hint":"The digit after the 4.","phase":"substitute"},
  {"pre":"9 is 5 or more, so round the kept 4 up. 4 + 1 = ","answer":5,"hint":"Add 1 to the last kept digit."},
  {"pre":"Keeping the place value, the number is 0.0605, so type ","answer":0.0605,"hint":"Zero point zero six zero five.","done":"So 0.06049 to 3 s.f. is 0.0605."},
 ],
 [mis("truncate","The deciding digit is 9, which is 5 or more, so round the 4 up to 5: the answer is 0.0605.",None,"Student truncates to 0.0604; the near-value is within rounding tolerance and cannot be uniquely diagnosed.")]))

# ================= GOLD =================
gold = []

# g0
gold.append(prob(
 "Estimate \\(\\dfrac{4.87 \\times 21.3}{0.52}\\) by rounding to 1 significant figure.", 200, False,
 "Round each to 1 s.f., then remember dividing by 0.5 doubles.",
 [
  {"pre":"Round each number to 1 significant figure. 4.87 rounds to ","answer":5,"hint":"4.87 is nearer 5 than 4."},
  {"pre":"21.3 rounds to ","answer":20,"hint":"21.3 is nearer 20 than 30."},
  {"pre":"0.52 rounds to 0.5. Multiply the top: 5 × 20 = ","answer":100,"hint":"Five times twenty.","phase":"substitute"},
  {"pre":"Dividing by 0.5 is the same as doubling, so 100 ÷ 0.5 = ","answer":200,"hint":"Double 100.","done":"So the estimate is 200."},
  {"pre":"Check: 200 × 0.5 = ","answer":100,"hint":"200 halved.","done":"200 × 0.5 = 100 confirms 100 ÷ 0.5 = 200. Correct."},
 ],
 [mis("divide_half","Dividing by 0.5 doubles the amount, so 100 ÷ 0.5 = 200, not 50.",50,"Student divides by 0.5 as if by 2: 50."),
  mis("round_denom_wrong","0.52 to 1 s.f. is 0.5, not 1. So 100 ÷ 0.5 = 200.",100,"Student rounds 0.52 to 1 and divides by 1, leaving 100.")]))

# g1  REPAIRED display (square-number method; strict 1sf gave sqrt(50), not 35)
gold.append(prob(
 "Estimate \\(\\dfrac{\\sqrt{48.6}}{0.21}\\). Round 48.6 to the nearest square number and 0.21 to 1 significant figure.", 35, False,
 "Round 48.6 to the nearest square, and dividing by 0.2 multiplies by 5.",
 [
  {"pre":"Round 48.6 to the nearest square number: ","answer":49,"hint":"7 × 7 = 49 is closest to 48.6."},
  {"pre":"Take the square root: √49 = ","answer":7,"hint":"What number times itself makes 49."},
  {"pre":"Round 0.21 to 1 significant figure: ","answer":0.2,"hint":"0.21 is nearer 0.2 than 0.3.","phase":"substitute"},
  {"pre":"Dividing by 0.2 is the same as multiplying by 5, so 7 ÷ 0.2 = ","answer":35,"hint":"Seven times five.","done":"So the estimate is 35."},
  {"pre":"Check: 35 × 0.2 = ","answer":7,"hint":"35 times 0.2.","done":"35 × 0.2 = 7 confirms 7 ÷ 0.2 = 35. Correct."},
 ],
 [mis("divide_decimal","Dividing by 0.2 is the same as multiplying by 5, so 7 ÷ 0.2 = 35, not 3.5.",3.5,"Student divides by 0.2 as if by 2: 3.5.")]))

# g2  exact
gold.append(prob(
 "\\(0.3^2 + 0.4^2\\)", 0.25, False,
 "Square each decimal separately, then add; watch the decimal places.",
 [
  {"pre":"Square the first: 0.3² means 0.3 × 0.3. Ignoring decimals, 3 × 3 = ","answer":9,"hint":"Three times three."},
  {"pre":"With 2 decimal places that is 0.09. Now square the second: 0.4 × 0.4, and 4 × 4 = ","answer":16,"hint":"Four times four."},
  {"pre":"With 2 decimal places that is 0.16. Add the two results: 0.09 + 0.16 = ","answer":0.25,"hint":"Add the hundredths: 9 + 16 = 25 hundredths.","phase":"substitute"},
  {"pre":"Check: 25 hundredths is a quarter. Dividing 25 by 25 gives the top of that quarter: 25 ÷ 25 = ","answer":1,"hint":"25 over 100 simplifies to 1 over 4.","done":"0.25 = 1/4, a tidy result, so it is right."},
 ],
 [mis("square_as_double","Squaring means 0.3 × 0.3 = 0.09, not 0.3 × 2. So 0.09 + 0.16 = 0.25.",1.4,"Student doubles instead of squaring: 0.6 + 0.8 = 1.4."),
  mis("wrong_dp","0.3 × 0.3 needs two decimal places: 0.09, not 0.9. So the total is 0.25.",2.5,"Student squares with one decimal place: 0.9 + 1.6 = 2.5.")]))

# g3
gold.append(prob(
 "Estimate \\(\\dfrac{6.2^2}{0.31}\\) to 1 significant figure.", 120, False,
 "Round then square 6.2, and scale the division by 0.3 up by 10.",
 [
  {"pre":"Round 6.2 to 1 significant figure: ","answer":6,"hint":"6.2 is nearer 6 than 7."},
  {"pre":"Square it: 6² = 6 × 6 = ","answer":36,"hint":"Six times six."},
  {"pre":"Round 0.31 to 1 significant figure: ","answer":0.3,"hint":"0.31 is nearer 0.3 than 0.4.","phase":"substitute"},
  {"pre":"Now 36 ÷ 0.3. Scaling both by 10 gives 360 ÷ 3 = ","answer":120,"hint":"How many threes make 360.","done":"So the estimate is 120."},
  {"pre":"Check: 120 × 0.3 = ","answer":36,"hint":"120 times 0.3.","done":"120 × 0.3 = 36 confirms 36 ÷ 0.3 = 120. Correct."},
 ],
 [mis("divide_unscaled","36 ÷ 0.3 = 120, because 0.3 goes into 36 one hundred and twenty times. Dividing by 3 gives 12, ten times too small.",12,"Student divides 36 by 3 instead of 0.3: 12."),
  mis("square_as_double","6² means 6 × 6 = 36, not 6 × 2. Then 36 ÷ 0.3 = 120.",40,"Student doubles: 6 × 2 = 12, then 12 ÷ 0.3 = 40.")]))

# g4  calculator true
gold.append(prob(
 "\\(1.2 \\times 3.5 \\div 0.07\\)", 60, True,
 "Multiply first, then scale by 100 to divide by 0.07.",
 [
  {"pre":"Work left to right. First 1.2 × 3.5 = ","answer":4.2,"hint":"12 × 35 = 420, with two decimal places: 4.20."},
  {"pre":"Now divide by 0.07. Scale both by 100 so the divisor is a whole number. 0.07 × 100 = ","answer":7,"hint":"Move the point two places right.","phase":"substitute"},
  {"pre":"Do the same to 4.2: 4.2 × 100 = ","answer":420,"hint":"Move the point two places right."},
  {"pre":"Now divide the whole numbers: 420 ÷ 7 = ","answer":60,"hint":"How many sevens make 420.","done":"So 1.2 × 3.5 ÷ 0.07 = 60."},
  {"pre":"Check: multiply back 60 × 0.07 = ","answer":4.2,"hint":"Should return the value before dividing.","done":"60 × 0.07 = 4.2, matching 1.2 × 3.5. Correct."},
 ],
 [mis("divide_unscaled","4.2 ÷ 0.07 = 60. Dividing by 7 instead gives 0.6, a hundred times too small.",0.6,"Student divides 4.2 by 7 without scaling: 0.6.")]))

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Round decimals to a number of decimal places, and add, subtract, multiply or divide simple decimals.",
 "silver_description": "Round to significant figures, tackle harder decimal calculations, and estimate by rounding to 1 s.f.",
 "gold_description": "Estimate multi-step calculations by rounding, including squares, roots and dividing by decimals below 1.",
}

# ================= tier_guides =================
tier_guides = {
 "bronze": {
  "title": "Bronze: rounding to decimal places and decimal arithmetic",
  "steps": [
   "To round to a number of <strong>decimal places</strong>, keep that many digits after the point, then look at the very next digit.",
   "If that deciding digit is <strong>5 or more, round up</strong>; if it is 4 or less, round down.",
   "To add or subtract decimals, line up the points and pad with zeros; to multiply, ignore the points, multiply, then put the decimal places back."
  ],
  "example": {
   "question": "Round \\(4.362\\) to 2 decimal places.",
   "steps": [
    {"label":"Keep two decimals","content":"Keep 4.36, then look at the next digit."},
    {"label":"Deciding digit","content":"The next digit is 2, which is under 5, so round down."},
    {"label":"Check","content":"4.362 is below the halfway value 4.365, so it rounds down."},
    {"label":"Answer","content":"\\(4.36\\)","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "silver": {
  "title": "Silver: significant figures and estimating to 1 s.f.",
  "steps": [
   "For <strong>significant figures</strong>, start counting from the first non-zero digit; leading zeros never count.",
   "Keep the figures you need, use the next digit to round, then add zeros to hold the place value.",
   "To <strong>estimate</strong>, round every number in the calculation to 1 significant figure first, then work it out."
  ],
  "example": {
   "question": "Round \\(0.04083\\) to 2 significant figures.",
   "steps": [
    {"label":"First figures","content":"Ignore the zeros: the first two significant figures are 4 and 0."},
    {"label":"Deciding digit","content":"The next digit is 8, which is 5 or more, so round the 0 up to 1."},
    {"label":"Check","content":"Keeping the place value gives 0.041."},
    {"label":"Answer","content":"\\(0.041\\)","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "gold": {
  "title": "Gold: estimating harder calculations",
  "steps": [
   "Round every value to 1 significant figure, or to a square number under a root, before you calculate.",
   "Square or root the rounded values first, then handle the division.",
   "Dividing by a decimal below 1 makes the answer <strong>bigger</strong>: by 0.5 doubles, by 0.2 multiplies by 5, by 0.1 by 10."
  ],
  "example": {
   "question": "Estimate \\(\\dfrac{5.9^2}{0.48}\\) to 1 s.f.",
   "steps": [
    {"label":"Round","content":"5.9 rounds to 6 and 0.48 rounds to 0.5."},
    {"label":"Square","content":"6² = 36, so the calculation is 36 ÷ 0.5."},
    {"label":"Divide","content":"Dividing by 0.5 doubles: 36 ÷ 0.5 = 72."},
    {"label":"Check","content":"72 × 0.5 = 36, confirming the division."},
    {"label":"Answer","content":"\\(72\\)","isAnswer":True,"is_answer":True}
   ]
  }
 }
}

# ================= guided (opener + teach) =================
numline_svg = ('<svg viewBox="0 0 246 64" role="img" aria-label="A number line from 3 to 4 with a marker at 3.7 and the halfway value 3.5 marked" '
 'style="max-width:246px;width:100%;height:auto;display:block;margin:8px 0">'
 '<line x1="20" y1="40" x2="226" y2="40" stroke="currentColor" stroke-width="1.5"/>'
 '<line x1="20" y1="34" x2="20" y2="46" stroke="currentColor" stroke-width="1.5"/>'
 '<line x1="226" y1="34" x2="226" y2="46" stroke="currentColor" stroke-width="1.5"/>'
 '<line x1="123" y1="35" x2="123" y2="45" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>'
 '<circle cx="164" cy="40" r="4" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
 '<text x="20" y="58" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">3</text>'
 '<text x="123" y="58" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">3.5</text>'
 '<text x="226" y="58" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">4</text>'
 '<text x="164" y="26" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">3.7</text>'
 '</svg>')

guided = {
 "opener": {
  "steps": [
   {"say": "Forget the rules for a second. Here is a number line from 3 to 4, with a marker sitting at 3.7.<br>" + numline_svg},
   {"pre":"Is the marker at 3.7 nearer to 3 or to 4? Type the whole number it is nearer to: ","answer":4,"hint":"It is past the halfway value 3.5."},
   {"say":"Now picture the marker slid back to 3.2 instead."},
   {"pre":"Is 3.2 nearer to 3 or to 4? Type the whole number: ","answer":3,"hint":"It has not reached the halfway value 3.5."},
   {"say":"You just <strong>rounded</strong>. Each number is nearer one end of the line, and the halfway value 3.5 is the tipping point: at or above it you round up, below it you round down. Rounding to a decimal place or a significant figure is the same idea, just zoomed in on a smaller stretch of the line."}
  ]
 },
 "teach": {
  "bronze": {
   "display": "Round \\(8.4638\\) to 2 decimal places.",
   "steps": [
    {"pre":"Keep two digits after the point. In 8.4638 the kept digits are 4 and ","answer":6,"hint":"The second digit after the point."},
    {"pre":"The deciding digit is the next one along: ","answer":3,"hint":"The third digit after the point."},
    {"pre":"3 is less than 5, so the kept 6 stays the same. The last kept digit is still ","answer":6,"hint":"Under 5 means round down."},
    {"pre":"To 2 dp the number is 8.46, so type ","answer":8.46,"hint":"Eight point four six.","done":"So 8.4638 rounds to 8.46. The whole bronze move is: find the deciding digit and let it round the last kept digit."},
    {"pre":"Check: the halfway value between 8.46 and 8.47 is ","answer":8.465,"hint":"Add 0.005 to 8.46.","done":"8.4638 is below 8.465, confirming it rounds down to 8.46."}
   ]
  },
  "silver": {
   "display": "Round \\(0.0724\\) to 2 significant figures.",
   "steps": [
    {"pre":"Leading zeros do not count. The first significant figure is ","answer":7,"hint":"The first non-zero digit."},
    {"pre":"The second significant figure is ","answer":2,"hint":"The digit after the 7."},
    {"pre":"The deciding digit is the next one along: ","answer":4,"hint":"The digit after the 2."},
    {"pre":"4 is less than 5, so the kept 2 stays. The last kept digit is still ","answer":2,"hint":"Under 5 means round down."},
    {"pre":"Keeping the place value the number is 0.072, so type ","answer":0.072,"hint":"Zero point zero seven two.","done":"So 0.0724 to 2 s.f. is 0.072. The whole silver move is: count significant figures from the first non-zero digit."}
   ]
  },
  "gold": {
   "display": "Estimate \\(\\dfrac{3.9 \\times 8.1}{0.19}\\) to 1 significant figure.",
   "steps": [
    {"pre":"Round 3.9 to 1 significant figure: ","answer":4,"hint":"3.9 is nearer 4 than 3."},
    {"pre":"Round 8.1 to 1 significant figure: ","answer":8,"hint":"8.1 is nearer 8 than 9."},
    {"pre":"Round 0.19 to 1 significant figure: ","answer":0.2,"hint":"0.19 rounds up to 0.2."},
    {"pre":"Multiply the top: 4 × 8 = ","answer":32,"hint":"Four times eight."},
    {"pre":"Dividing by 0.2 multiplies by 5, so 32 ÷ 0.2 = ","answer":160,"hint":"Thirty-two times five.","done":"So the estimate is 160. The whole gold move is: round everything to 1 s.f., then use that dividing by a decimal below 1 makes the answer bigger."}
   ]
  }
 }
}

out = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

json.dump(out, io.open("lesson_maths-eduqas_number-L03.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-eduqas_number-L03.json")
