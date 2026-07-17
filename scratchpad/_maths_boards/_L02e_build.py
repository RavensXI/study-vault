# -*- coding: utf-8 -*-
import json

live = json.load(open("_L02e_live.json", encoding="utf-8"))

SVG_BAR = ('<svg viewBox="0 0 246 50" role="img" aria-label="A chocolate bar '
           'divided into six equal squares" style="max-width:246px;width:100%;'
           'height:auto;display:block;margin:8px 0">'
           '<rect x="3" y="6" width="240" height="38" rx="3" fill="#f59e0b" '
           'fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
           '<line x1="43" y1="6" x2="43" y2="44" stroke="currentColor" stroke-width="1"/>'
           '<line x1="83" y1="6" x2="83" y2="44" stroke="currentColor" stroke-width="1"/>'
           '<line x1="123" y1="6" x2="123" y2="44" stroke="currentColor" stroke-width="1"/>'
           '<line x1="163" y1="6" x2="163" y2="44" stroke="currentColor" stroke-width="1"/>'
           '<line x1="203" y1="6" x2="203" y2="44" stroke="currentColor" stroke-width="1"/>'
           '</svg>')

def B(pre, answer, hint, **kw):
    d = {"pre": pre, "answer": answer, "hint": hint}
    d.update(kw)
    return d

def SAY(say):
    return {"say": say}

def MC(pattern, expect, message, note):
    if expect is None:
        check = "wrong"
    else:
        check = "equals_%s_%s" % (expect[0], expect[1]) if isinstance(expect, list) else "equals_%s" % expect
    return {"pattern": pattern, "check": check, "expect": expect, "message": message, "note": note}

# ---------------- BRONZE ----------------
bronze = []

bronze.append({
 "display": "\\(\\frac{1}{4} + \\frac{1}{3}\\)",
 "solutions": [7, 12], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to twelfths, then add the tops.",
 "misconceptions": [
   MC("add_denominators", [2,7],
      "Don't add the denominators. LCD of 4 and 3 is 12: 3/12 + 4/12 = 7/12.",
      "Student adds numerators AND denominators: (1+1)/(4+3) = 2/7.")],
 "guided_steps": [
   B("The common denominator of 4 and 3 is ", 12, "The smallest number in both times tables: 4 × 3."),
   B("Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 = ", 3, "Multiply the top of 1/4 by 3."),
   B("Convert 1/3 into twelfths: 3 goes into 12 four times, so 1 × 4 = ", 4, "Multiply the top of 1/3 by 4."),
   B("Add the tops: 3 + 4 = ", 7, "Add the numerators, keep the denominator 12.", phase="substitute"),
   B("The denominator stays ", 12, "Only the tops were added.", done="So 1/4 + 1/3 = 7/12."),
   B("Check: 7 and 12 share no factor, so 7/12 is simplest. Subtract back 7 − 4 = ", 3,
     "Should give 3, which is 1/4 in twelfths.", done="3/12 = 1/4, so 7/12 is right.")]})

bronze.append({
 "display": "\\(\\frac{3}{5} + \\frac{1}{10}\\)",
 "solutions": [7, 10], "calculator": False, "input_type": "fraction",
 "hint": "Turn 3/5 into tenths, then add the tops.",
 "misconceptions": [
   MC("add_denominators", [4,15],
      "Don't add the denominators. Convert 3/5 to tenths: 6/10 + 1/10 = 7/10.",
      "Student adds numerators AND denominators: (3+1)/(5+10) = 4/15.")],
 "guided_steps": [
   B("The common denominator of 5 and 10 is ", 10, "10 is already in the 5 times table."),
   B("Convert 3/5 into tenths: 5 goes into 10 twice, so 3 × 2 = ", 6, "Multiply the top of 3/5 by 2."),
   SAY("The second fraction, 1/10, is already in tenths."),
   B("Add the tops: 6 + 1 = ", 7, "Add the numerators, keep the denominator 10.", phase="substitute"),
   B("The denominator stays ", 10, "Only the tops were added.", done="So 3/5 + 1/10 = 7/10."),
   B("Check: 7 and 10 share no factor, so 7/10 is simplest. Subtract back 7 − 1 = ", 6,
     "Should give 6, which is 3/5 in tenths.", done="6/10 = 3/5, so 7/10 is right.")]})

bronze.append({
 "display": "\\(\\frac{5}{6} - \\frac{1}{3}\\)",
 "solutions": [1, 2], "calculator": False, "input_type": "fraction",
 "hint": "Convert 1/3 to sixths, subtract, then simplify.",
 "misconceptions": [
   MC("subtract_across", [4,3],
      "You can't subtract the bottoms. Convert 1/3 to sixths: 5/6 − 2/6 = 3/6 = 1/2.",
      "Student subtracts tops and bottoms: (5-1)/(6-3) = 4/3."),
   MC("no_simplify", [3,6],
      "3/6 is correct but simplify by dividing top and bottom by 3 to get 1/2.",
      "Correct subtraction to 3/6 but stops without simplifying.")],
 "guided_steps": [
   B("The common denominator of 6 and 3 is ", 6, "6 is already in the 3 times table."),
   B("Convert 1/3 into sixths: 3 goes into 6 twice, so 1 × 2 = ", 2, "Multiply the top of 1/3 by 2."),
   SAY("The first fraction, 5/6, is already in sixths."),
   B("Subtract the tops: 5 − 2 = ", 3, "Take 2 away from 5, keep the denominator 6.", phase="substitute"),
   B("That gives 3/6. Simplify by dividing top and bottom by 3. Top: 3 ÷ 3 = ", 1, "3 divided by 3."),
   B("Bottom: 6 ÷ 3 = ", 2, "6 divided by 3.", done="So 5/6 − 1/3 = 1/2."),
   B("Check: turn 1/2 back into sixths. 1 × 3 = ", 3, "If it gives 3/6, the answer matches.",
     done="3/6 matches, so 1/2 is correct.")]})

bronze.append({
 "display": "\\(\\frac{2}{3} - \\frac{1}{4}\\)",
 "solutions": [5, 12], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to twelfths, then subtract the tops.",
 "misconceptions": [
   MC("no_common_denom", None,
      "Different denominators, so find the LCD (12): 8/12 − 3/12 = 5/12.",
      "Student subtracts without converting; result varies, no single determinate answer.")],
 "guided_steps": [
   B("The common denominator of 3 and 4 is ", 12, "The smallest number in both times tables: 3 × 4."),
   B("Convert 2/3 into twelfths: 3 goes into 12 four times, so 2 × 4 = ", 8, "Multiply the top of 2/3 by 4."),
   B("Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 = ", 3, "Multiply the top of 1/4 by 3."),
   B("Subtract the tops: 8 − 3 = ", 5, "Take 3 away from 8, keep the denominator 12.", phase="substitute"),
   B("The denominator stays ", 12, "Only the tops were subtracted.", done="So 2/3 − 1/4 = 5/12."),
   B("Check: 5 and 12 share no factor, so 5/12 is simplest. Add back 5 + 3 = ", 8,
     "Should give 8, which is 2/3 in twelfths.", done="8/12 = 2/3, so 5/12 is right.")]})

# CHANGED (was 1/2 + 1/5 = 7/10, duplicate of index 1)
bronze.append({
 "display": "\\(\\frac{1}{3} + \\frac{2}{5}\\)",
 "solutions": [11, 15], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to fifteenths, then add the tops.",
 "misconceptions": [
   MC("add_denominators", [3,8],
      "Don't add the denominators. LCD of 3 and 5 is 15: 5/15 + 6/15 = 11/15.",
      "Student adds numerators AND denominators: (1+2)/(3+5) = 3/8.")],
 "guided_steps": [
   B("The common denominator of 3 and 5 is ", 15, "The smallest number in both times tables: 3 × 5."),
   B("Convert 1/3 into fifteenths: 3 goes into 15 five times, so 1 × 5 = ", 5, "Multiply the top of 1/3 by 5."),
   B("Convert 2/5 into fifteenths: 5 goes into 15 three times, so 2 × 3 = ", 6, "Multiply the top of 2/5 by 3."),
   B("Add the tops: 5 + 6 = ", 11, "Add the numerators, keep the denominator 15.", phase="substitute"),
   B("The denominator stays ", 15, "Only the tops were added.", done="So 1/3 + 2/5 = 11/15."),
   B("Check: 11 and 15 share no factor, so 11/15 is simplest. Subtract back 11 − 6 = ", 5,
     "Should give 5, which is 1/3 in fifteenths.", done="5/15 = 1/3, so 11/15 is right.")]})

bronze.append({
 "display": "\\(\\frac{3}{4} - \\frac{1}{2}\\)",
 "solutions": [1, 4], "calculator": False, "input_type": "fraction",
 "hint": "Convert 1/2 to quarters, then subtract.",
 "misconceptions": [
   MC("subtract_across", [2,2],
      "You can't subtract the bottoms. Convert 1/2 to quarters: 3/4 − 2/4 = 1/4.",
      "Student subtracts tops and bottoms: (3-1)/(4-2) = 2/2.")],
 "guided_steps": [
   B("The common denominator of 4 and 2 is ", 4, "4 is already in the 2 times table."),
   B("Convert 1/2 into quarters: 2 goes into 4 twice, so 1 × 2 = ", 2, "Multiply the top of 1/2 by 2."),
   SAY("The first fraction, 3/4, is already in quarters."),
   B("Subtract the tops: 3 − 2 = ", 1, "Take 2 away from 3, keep the denominator 4.", phase="substitute"),
   B("The denominator stays ", 4, "Only the tops were subtracted.", done="So 3/4 − 1/2 = 1/4."),
   B("Check: 1 and 4 share no factor, so 1/4 is simplest. Add back 1 + 2 = ", 3,
     "Should give 3, which is 3/4 in quarters.", done="3/4 was the first fraction, so 1/4 is right.")]})

bronze.append({
 "display": "\\(\\frac{2}{7} + \\frac{3}{7}\\)",
 "solutions": [5, 7], "calculator": False, "input_type": "fraction",
 "hint": "Same denominator already: just add the tops.",
 "misconceptions": [
   MC("add_denominators", [5,14],
      "Same denominator already, so keep the 7. Just add the tops: 2 + 3 = 5, giving 5/7.",
      "Student adds numerators AND denominators: (2+3)/(7+7) = 5/14.")],
 "guided_steps": [
   B("Both fractions are already sevenths, so the denominator stays ", 7, "Same denominators stay the same when adding."),
   B("Add the tops: 2 + 3 = ", 5, "Add the numerators, keep the denominator 7.", phase="substitute"),
   B("Check: 5 and 7 share no factor, so 5/7 is simplest. Subtract back 5 − 3 = ", 2,
     "Should give 2, the first fraction's top.", done="2/7 was the first fraction, so 5/7 is right.")]})

# CHANGED (was 7/8 - 3/8 = 1/2, duplicate of index 2)
bronze.append({
 "display": "\\(\\frac{7}{8} - \\frac{1}{8}\\)",
 "solutions": [3, 4], "calculator": False, "input_type": "fraction",
 "hint": "Same denominator: subtract the tops, then simplify.",
 "misconceptions": [
   MC("subtract_denominators", None,
      "The denominators are the same, so keep the 8. Just subtract the tops: 7 − 1 = 6, then simplify 6/8 = 3/4.",
      "Subtracting denominators gives 6/0, undefined; no single determinate wrong answer."),
   MC("no_simplify", [6,8],
      "6/8 is correct but simplify by dividing top and bottom by 2 to get 3/4.",
      "Correct subtraction to 6/8 but stops without simplifying.")],
 "guided_steps": [
   B("Both fractions are already eighths, so the denominator starts as ", 8, "Same denominators stay the same when subtracting."),
   B("Subtract the tops: 7 − 1 = ", 6, "Take 1 away from 7, keep the denominator 8.", phase="substitute"),
   B("That gives 6/8. Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 = ", 3, "6 divided by 2."),
   B("Bottom: 8 ÷ 2 = ", 4, "8 divided by 2.", done="So 7/8 − 1/8 = 3/4."),
   B("Check: turn 3/4 back into eighths. 3 × 2 = ", 6, "If it gives 6/8, the answer matches.",
     done="6/8 matches, so 3/4 is correct.")]})

# ---------------- SILVER ----------------
silver = []

silver.append({
 "display": "\\(\\frac{2}{3} \\times \\frac{3}{5}\\)",
 "solutions": [2, 5], "calculator": False, "input_type": "fraction",
 "hint": "Multiply across, then simplify the result.",
 "misconceptions": [
   MC("add_not_multiply", [5,8],
      "For multiplying, multiply straight across: 2 × 3 = 6 and 3 × 5 = 15, then simplify 6/15 = 2/5.",
      "Student adds across instead of multiplying: (2+3)/(3+5) = 5/8."),
   MC("no_simplify", [6,15],
      "6/15 is correct but simplify by dividing both by 3 to get 2/5.",
      "Multiplies correctly to 6/15 but stops without simplifying.")],
 "guided_steps": [
   B("Multiplying needs no common denominator. Multiply the tops: 2 × 3 = ", 6, "Multiply the two numerators."),
   B("Multiply the bottoms: 3 × 5 = ", 15, "Multiply the two denominators.", phase="substitute"),
   B("That gives 6/15. Simplify by dividing top and bottom by 3. Top: 6 ÷ 3 = ", 2, "6 divided by 3."),
   B("Bottom: 15 ÷ 3 = ", 5, "15 divided by 3.", done="So 2/3 × 3/5 = 2/5."),
   B("Check: turn 2/5 back up by 3. 2 × 3 = ", 6, "If it gives 6/15, the answer matches.",
     done="6/15 matches, so 2/5 is correct.")]})

silver.append({
 "display": "\\(\\frac{4}{5} \\times \\frac{5}{8}\\)",
 "solutions": [1, 2], "calculator": False, "input_type": "fraction",
 "hint": "Multiply across, then simplify fully.",
 "misconceptions": [
   MC("no_simplify", [20,40],
      "20/40 is correct but simplify: divide top and bottom by 20 to get 1/2.",
      "Multiplies to 20/40 but does not simplify.")],
 "guided_steps": [
   B("Multiply the tops: 4 × 5 = ", 20, "Multiply the two numerators."),
   B("Multiply the bottoms: 5 × 8 = ", 40, "Multiply the two denominators.", phase="substitute"),
   B("That gives 20/40. Simplify by dividing top and bottom by 20. Top: 20 ÷ 20 = ", 1, "20 divided by 20."),
   B("Bottom: 40 ÷ 20 = ", 2, "40 divided by 20.", done="So 4/5 × 5/8 = 1/2."),
   B("Check: turn 1/2 back up by 20. 1 × 20 = ", 20, "If it gives 20/40, the answer matches.",
     done="20/40 matches, so 1/2 is correct.")]})

silver.append({
 "display": "\\(\\frac{3}{4} \\div \\frac{1}{2}\\)",
 "solutions": [3, 2], "calculator": False, "input_type": "fraction",
 "hint": "Keep the first, flip the second, then multiply.",
 "misconceptions": [
   MC("no_flip", [3,8],
      "For dividing, flip the second fraction then multiply: 3/4 × 2/1 = 6/4 = 3/2.",
      "Student multiplies without flipping: 3/4 × 1/2 = 3/8."),
   MC("flip_wrong", [2,3],
      "Keep the first, flip only the second: 3/4 × 2/1.",
      "Student flips the first fraction instead: 4/3 × 1/2 = 4/6 = 2/3.")],
 "guided_steps": [
   B("To divide, flip the second fraction. The reciprocal of 1/2 is 2 over 1, so its new top is ", 2, "Swap the top and bottom of 1/2."),
   SAY("Now the sum is 3/4 × 2/1."),
   B("Multiply the tops: 3 × 2 = ", 6, "Multiply the two numerators.", phase="substitute"),
   B("Multiply the bottoms: 4 × 1 = ", 4, "Multiply the two denominators."),
   B("That gives 6/4. Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 = ", 3, "6 divided by 2."),
   B("Bottom: 4 ÷ 2 = ", 2, "4 divided by 2.", done="So 3/4 ÷ 1/2 = 3/2 = 1 1/2."),
   B("Check: multiply back. 3/2 × 1/2, tops: 3 × 1 = ", 3, "If it rebuilds 3/4, the answer is right.",
     done="3/2 × 1/2 = 3/4, so 3/2 is correct.")]})

silver.append({
 "display": "\\(\\frac{5}{6} \\div \\frac{2}{3}\\)",
 "solutions": [5, 4], "calculator": False, "input_type": "fraction",
 "hint": "Keep, flip, multiply, then simplify.",
 "misconceptions": [
   MC("no_flip", [10,18],
      "For dividing, flip the second fraction: 5/6 × 3/2 = 15/12 = 5/4.",
      "Student multiplies without flipping: 5/6 × 2/3 = 10/18."),
   MC("flip_wrong", [12,15],
      "Keep the first, flip only the second: 5/6 × 3/2.",
      "Student flips the first fraction: 6/5 × 2/3 = 12/15.")],
 "guided_steps": [
   B("To divide, flip the second fraction. The reciprocal of 2/3 is 3 over 2, so its new top is ", 3, "Swap the top and bottom of 2/3."),
   SAY("Now the sum is 5/6 × 3/2."),
   B("Multiply the tops: 5 × 3 = ", 15, "Multiply the two numerators.", phase="substitute"),
   B("Multiply the bottoms: 6 × 2 = ", 12, "Multiply the two denominators."),
   B("That gives 15/12. Simplify by dividing top and bottom by 3. Top: 15 ÷ 3 = ", 5, "15 divided by 3."),
   B("Bottom: 12 ÷ 3 = ", 4, "12 divided by 3.", done="So 5/6 ÷ 2/3 = 5/4 = 1 1/4."),
   B("Check: multiply back. 5/4 × 2/3, tops: 5 × 2 = ", 10, "If it rebuilds 5/6, the answer is right.",
     done="5/4 × 2/3 = 10/12 = 5/6, so 5/4 is correct.")]})

silver.append({
 "display": "\\(\\frac{2}{3} + \\frac{3}{4}\\)",
 "solutions": [17, 12], "calculator": False, "input_type": "fraction",
 "hint": "The LCD of 3 and 4 is 12; convert both and add.",
 "misconceptions": [
   MC("add_denominators", [5,7],
      "Don't add the denominators. LCD of 3 and 4 is 12: 8/12 + 9/12 = 17/12.",
      "Student adds numerators AND denominators: (2+3)/(3+4) = 5/7.")],
 "guided_steps": [
   B("The common denominator of 3 and 4 is ", 12, "3 × 4, since they share no factor."),
   B("Convert 2/3 into twelfths: 3 goes into 12 four times, so 2 × 4 = ", 8, "Multiply the top of 2/3 by 4."),
   B("Convert 3/4 into twelfths: 4 goes into 12 three times, so 3 × 3 = ", 9, "Multiply the top of 3/4 by 3."),
   B("Add the tops: 8 + 9 = ", 17, "Add the numerators, keep the denominator 12.", phase="substitute"),
   B("The denominator stays ", 12, "Only the tops were added.", done="So 2/3 + 3/4 = 17/12 = 1 5/12."),
   B("Check: 17 is prime, so 17/12 will not simplify. Subtract back 17 − 9 = ", 8,
     "Should give 8, which is 2/3 in twelfths.", done="8/12 = 2/3, so 17/12 is right.")]})

silver.append({
 "display": "\\(\\frac{7}{10} - \\frac{2}{5}\\)",
 "solutions": [3, 10], "calculator": False, "input_type": "fraction",
 "hint": "Convert 2/5 to tenths, then subtract.",
 "misconceptions": [
   MC("no_common_denom", [5,5],
      "Convert 2/5 to tenths: 2/5 = 4/10. Then 7/10 − 4/10 = 3/10.",
      "Student subtracts tops and bottoms separately: (7-2)/(10-5) = 5/5.")],
 "guided_steps": [
   B("The common denominator of 10 and 5 is ", 10, "10 is already in the 5 times table."),
   B("Convert 2/5 into tenths: 5 goes into 10 twice, so 2 × 2 = ", 4, "Multiply the top of 2/5 by 2."),
   SAY("The first fraction, 7/10, is already in tenths."),
   B("Subtract the tops: 7 − 4 = ", 3, "Take 4 away from 7, keep the denominator 10.", phase="substitute"),
   B("The denominator stays ", 10, "Only the tops were subtracted.", done="So 7/10 − 2/5 = 3/10."),
   B("Check: 3 and 10 share no factor, so 3/10 is simplest. Add back 3 + 4 = ", 7,
     "Should give 7, the first fraction in tenths.", done="7/10 was the first fraction, so 3/10 is right.")]})

silver.append({
 "display": "\\(\\frac{5}{9} \\times \\frac{3}{10}\\)",
 "solutions": [1, 6], "calculator": False, "input_type": "fraction",
 "hint": "Multiply across, then simplify by the HCF.",
 "misconceptions": [
   MC("add_not_multiply", [8,19],
      "For multiplying, multiply across not add: 5 × 3 = 15 and 9 × 10 = 90, then simplify 15/90 = 1/6.",
      "Student adds across: (5+3)/(9+10) = 8/19."),
   MC("no_simplify", [15,90],
      "15/90 is correct but simplify by dividing both by 15 to get 1/6.",
      "Multiplies to 15/90 but does not simplify.")],
 "guided_steps": [
   B("Multiply the tops: 5 × 3 = ", 15, "Multiply the two numerators."),
   B("Multiply the bottoms: 9 × 10 = ", 90, "Multiply the two denominators.", phase="substitute"),
   B("That gives 15/90. Simplify by dividing top and bottom by 15. Top: 15 ÷ 15 = ", 1, "15 divided by 15."),
   B("Bottom: 90 ÷ 15 = ", 6, "90 divided by 15.", done="So 5/9 × 3/10 = 1/6."),
   B("Check: turn 1/6 back up by 15. 1 × 15 = ", 15, "If it gives 15/90, the answer matches.",
     done="15/90 matches, so 1/6 is correct.")]})

# ---------------- GOLD ----------------
gold = []

gold.append({
 "display": "\\(1\\frac{2}{3} + 2\\frac{3}{4}\\)",
 "solutions": [53, 12], "calculator": False, "input_type": "fraction",
 "hint": "Convert both mixed numbers to improper fractions, then find the LCD.",
 "misconceptions": [
   MC("add_denominators", [16,7],
      "Give both a common denominator of 12 first: 20/12 + 33/12 = 53/12. Don't add the denominators.",
      "Student adds numerators and denominators of the improper fractions: (5+11)/(3+4) = 16/7."),
   MC("wrong_improper", None,
      "1 2/3 = 5/3 (1 × 3 + 2 = 5, over 3) and 2 3/4 = 11/4.",
      "Wrong improper conversions vary, no single determinate answer.")],
 "guided_steps": [
   B("Convert 1 2/3 to an improper fraction. Top: 1 × 3 + 2 = ", 5, "Whole times denominator, plus the top."),
   B("Convert 2 3/4 to an improper fraction. Top: 2 × 4 + 3 = ", 11, "Whole times denominator, plus the top."),
   B("The common denominator of 3 and 4 is ", 12, "3 × 4, since they share no factor."),
   B("Convert 5/3 into twelfths: 3 goes into 12 four times, so 5 × 4 = ", 20, "Multiply the top of 5/3 by 4."),
   B("Convert 11/4 into twelfths: 4 goes into 12 three times, so 11 × 3 = ", 33, "Multiply the top of 11/4 by 3."),
   B("Add the tops: 20 + 33 = ", 53, "Add the numerators, keep the denominator 12.", phase="substitute"),
   B("The denominator stays ", 12, "Only the tops were added.", done="So 1 2/3 + 2 3/4 = 53/12 = 4 5/12."),
   B("Check: 53 is prime, so 53/12 will not simplify. Subtract back 53 − 33 = ", 20,
     "Should give 20, which is 5/3 in twelfths.", done="20/12 = 5/3 = 1 2/3, so 53/12 is right.")]})

gold.append({
 "display": "\\(2\\frac{1}{2} \\times 1\\frac{1}{3}\\)",
 "solutions": [10, 3], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to improper fractions, then multiply across.",
 "misconceptions": [
   MC("multiply_wholes_fracs", [13,6],
      "Don't multiply the whole parts and fraction parts separately. Convert to improper fractions first: 5/2 × 4/3.",
      "Student multiplies wholes 2×1=2 and fractions 1/2×1/3=1/6, giving 2 1/6 = 13/6."),
   MC("wrong_improper", None,
      "2 1/2 = 5/2 (2 × 2 + 1 = 5) and 1 1/3 = 4/3.",
      "Wrong improper conversions vary, no single determinate answer.")],
 "guided_steps": [
   B("Convert 2 1/2 to an improper fraction. Top: 2 × 2 + 1 = ", 5, "Whole times denominator, plus the top."),
   B("Convert 1 1/3 to an improper fraction. Top: 1 × 3 + 1 = ", 4, "Whole times denominator, plus the top."),
   B("Multiply the tops: 5 × 4 = ", 20, "Multiply the two numerators.", phase="substitute"),
   B("Multiply the bottoms: 2 × 3 = ", 6, "Multiply the two denominators."),
   B("That gives 20/6. Simplify by dividing top and bottom by 2. Top: 20 ÷ 2 = ", 10, "20 divided by 2."),
   B("Bottom: 6 ÷ 2 = ", 3, "6 divided by 2.", done="So 2 1/2 × 1 1/3 = 10/3 = 3 1/3."),
   B("Check: turn 10/3 back up by 2. 10 × 2 = ", 20, "If it gives 20/6, the answer matches.",
     done="20/6 matches, so 10/3 is correct.")]})

gold.append({
 "display": "\\(3\\frac{1}{4} \\div 1\\frac{1}{2}\\)",
 "solutions": [13, 6], "calculator": False, "input_type": "fraction",
 "hint": "Convert to improper, then keep, flip, multiply.",
 "misconceptions": [
   MC("no_flip", [39,8],
      "For dividing, flip the second fraction: 13/4 × 2/3.",
      "Student multiplies without flipping: 13/4 × 3/2 = 39/8."),
   MC("wrong_improper", None,
      "3 1/4 = 13/4 (3 × 4 + 1 = 13) and 1 1/2 = 3/2.",
      "Wrong improper conversions vary, no single determinate answer.")],
 "guided_steps": [
   B("Convert 3 1/4 to an improper fraction. Top: 3 × 4 + 1 = ", 13, "Whole times denominator, plus the top."),
   B("Convert 1 1/2 to an improper fraction. Top: 1 × 2 + 1 = ", 3, "Whole times denominator, plus the top."),
   B("To divide, flip the second fraction. The reciprocal of 3/2 is 2 over 3, so its new top is ", 2, "Swap the top and bottom of 3/2."),
   SAY("Now the sum is 13/4 × 2/3."),
   B("Multiply the tops: 13 × 2 = ", 26, "Multiply the two numerators.", phase="substitute"),
   B("Multiply the bottoms: 4 × 3 = ", 12, "Multiply the two denominators."),
   B("That gives 26/12. Simplify by dividing top and bottom by 2. Top: 26 ÷ 2 = ", 13, "26 divided by 2."),
   B("Bottom: 12 ÷ 2 = ", 6, "12 divided by 2.", done="So 3 1/4 ÷ 1 1/2 = 13/6 = 2 1/6."),
   B("Check: multiply back. 13/6 × 3/2, tops: 13 × 3 = ", 39, "If it rebuilds 13/4, the answer is right.",
     done="13/6 × 3/2 = 39/12 = 13/4, so 13/6 is correct.")]})

gold.append({
 "display": "\\(\\frac{5}{6} + \\frac{7}{8} - \\frac{1}{3}\\)",
 "solutions": [11, 8], "calculator": False, "input_type": "fraction",
 "hint": "Find the common denominator of all three (6, 8 and 3), then combine.",
 "misconceptions": [
   MC("wrong_lcd", None,
      "The LCD of 6, 8 and 3 is 24. Convert: 20/24 + 21/24 − 8/24 = 33/24 = 11/8.",
      "A wrong LCD gives unpredictable results; no single determinate answer."),
   MC("partial", [41,24],
      "Combine all three: add the first two, then subtract 1/3. All need the denominator 24.",
      "Student adds 5/6 + 7/8 = 41/24 and ignores the subtraction.")],
 "guided_steps": [
   B("The common denominator of 6, 8 and 3 is ", 24, "The smallest number all three divide into."),
   B("Convert 5/6 into 24ths: 6 goes into 24 four times, so 5 × 4 = ", 20, "Multiply the top of 5/6 by 4."),
   B("Convert 7/8 into 24ths: 8 goes into 24 three times, so 7 × 3 = ", 21, "Multiply the top of 7/8 by 3."),
   B("Convert 1/3 into 24ths: 3 goes into 24 eight times, so 1 × 8 = ", 8, "Multiply the top of 1/3 by 8."),
   B("Combine the tops in order: 20 + 21 − 8 = ", 33, "Add the first two, then subtract the third.", phase="substitute"),
   B("That gives 33/24. Simplify by dividing top and bottom by 3. Top: 33 ÷ 3 = ", 11, "33 divided by 3."),
   B("Bottom: 24 ÷ 3 = ", 8, "24 divided by 3.", done="So 5/6 + 7/8 − 1/3 = 11/8 = 1 3/8."),
   B("Check: turn 11/8 back up by 3. 11 × 3 = ", 33, "If it gives 33/24, the answer matches.",
     done="33/24 matches, so 11/8 is correct.")]})

gold.append({
 "display": "\\(2\\frac{1}{5} - 1\\frac{2}{3}\\)",
 "solutions": [8, 15], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to improper fractions first, then find the LCD.",
 "misconceptions": [
   MC("subtract_wholes_fracs", [22,15],
      "You can't subtract the whole parts and fraction parts separately here, because 1/5 is smaller than 2/3. Convert to improper fractions: 11/5 and 5/3.",
      "Student does 2-1=1 and 2/3-1/5=7/15, giving 1 7/15 = 22/15."),
   MC("wrong_improper", None,
      "2 1/5 = 11/5 (2 × 5 + 1 = 11) and 1 2/3 = 5/3.",
      "Wrong improper conversions vary, no single determinate answer.")],
 "guided_steps": [
   B("Convert 2 1/5 to an improper fraction. Top: 2 × 5 + 1 = ", 11, "Whole times denominator, plus the top."),
   B("Convert 1 2/3 to an improper fraction. Top: 1 × 3 + 2 = ", 5, "Whole times denominator, plus the top."),
   B("The common denominator of 5 and 3 is ", 15, "5 × 3, since they share no factor."),
   B("Convert 11/5 into fifteenths: 5 goes into 15 three times, so 11 × 3 = ", 33, "Multiply the top of 11/5 by 3."),
   B("Convert 5/3 into fifteenths: 3 goes into 15 five times, so 5 × 5 = ", 25, "Multiply the top of 5/3 by 5."),
   B("Subtract the tops: 33 − 25 = ", 8, "Take 25 away from 33, keep the denominator 15.", phase="substitute"),
   B("The denominator stays ", 15, "Only the tops were subtracted.", done="So 2 1/5 − 1 2/3 = 8/15."),
   B("Check: 8 and 15 share no factor, so 8/15 is simplest. Add back 8 + 25 = ", 33,
     "Should give 33, which is 11/5 in fifteenths.", done="33/15 = 11/5 = 2 1/5, so 8/15 is right.")]})

# ---------------- assemble ----------------
pd = dict(live)  # preserve everything, then override
pd["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Add, subtract or multiply two simple fractions, then simplify the answer.",
  "silver_description": "Divide with keep, flip, multiply, and add or subtract fractions with unlike denominators.",
  "gold_description": "Combine mixed numbers or a three-fraction chain, converting and simplifying throughout."
}

pd["method_card"] = {
  "title": "How to Add, Subtract, Multiply and Divide Fractions",
  "steps": [
    "Convert any mixed numbers to improper fractions first.",
    "To add or subtract: find a common denominator, then combine the tops only.",
    "To multiply: multiply tops and bottoms. To divide: keep, flip, multiply.",
    "Always simplify the final fraction by its highest common factor."
  ],
  "content": ("<p><strong>Adding and subtracting</strong> need a common denominator: convert both fractions "
              "so the bottoms match, then combine the tops only.</p><p><strong>Multiplying</strong> needs no "
              "common denominator: multiply the tops together and the bottoms together.</p>"
              "<p><strong>Dividing</strong> uses keep, flip, multiply: keep the first fraction, flip the "
              "second, then multiply.</p><p><strong>Mixed numbers</strong> become improper fractions first. "
              "Simplify every answer.</p>"),
  "example": ("<p><strong>Calculate</strong> \\(\\frac{2}{3} + \\frac{3}{4}\\)</p><p>LCD of 3 and 4 is 12: "
              "\\(\\frac{8}{12} + \\frac{9}{12} = \\frac{17}{12} = 1\\frac{5}{12}\\).</p>")
}

pd["tier_guides"] = {
  "bronze": {
    "title": "Bronze: adding, subtracting and multiplying simple fractions",
    "steps": [
      "For <strong>+</strong> or <strong>−</strong>: give both fractions the same denominator, then combine the tops only.",
      "For <strong>×</strong>: no common denominator is needed. Multiply the tops together and the bottoms together.",
      "Always simplify the final fraction by dividing top and bottom by their highest common factor."
    ],
    "example": {
      "question": "Calculate \\(\\frac{1}{6} + \\frac{1}{3}\\)",
      "steps": [
        {"label": "Common denominator", "content": "The LCD of 6 and 3 is 6, so 1/3 = 2/6."},
        {"label": "Add the tops", "content": "1/6 + 2/6 = 3/6."},
        {"label": "Simplify", "content": "Divide top and bottom by 3: 3/6 = 1/2."},
        {"label": "Check", "content": "1/2 turned back into sixths is 3/6, matching the sum."},
        {"label": "Answer", "content": "\\(\\frac{1}{2}\\)", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "silver": {
    "title": "Silver: dividing fractions and unlike denominators",
    "steps": [
      "To divide, use <strong>keep, flip, multiply</strong>: keep the first fraction, flip the second, then multiply across.",
      "To add or subtract unlike fractions, convert both to a common denominator first.",
      "Multiply, add or subtract as usual, then simplify the answer."
    ],
    "example": {
      "question": "Calculate \\(\\frac{2}{3} \\div \\frac{4}{5}\\)",
      "steps": [
        {"label": "Keep, flip, multiply", "content": "2/3 ÷ 4/5 = 2/3 × 5/4."},
        {"label": "Multiply across", "content": "2 × 5 = 10 and 3 × 4 = 12, giving 10/12."},
        {"label": "Simplify", "content": "Divide top and bottom by 2: 10/12 = 5/6."},
        {"label": "Check", "content": "5/6 × 4/5 = 20/30 = 2/3, rebuilding the first fraction."},
        {"label": "Answer", "content": "\\(\\frac{5}{6}\\)", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "gold": {
    "title": "Gold: mixed numbers, three fractions and chains",
    "steps": [
      "Convert every mixed number to an improper fraction before you start.",
      "For a chain of fractions, give them all one common denominator, then combine the tops in order.",
      "Multiply, divide, add or subtract as needed, then simplify at the end."
    ],
    "example": {
      "question": "Calculate \\(1\\frac{1}{4} \\times \\frac{2}{3}\\)",
      "steps": [
        {"label": "Convert", "content": "1 1/4 = 5/4, so the sum is 5/4 × 2/3."},
        {"label": "Multiply across", "content": "5 × 2 = 10 and 4 × 3 = 12, giving 10/12."},
        {"label": "Simplify", "content": "Divide top and bottom by 2: 10/12 = 5/6."},
        {"label": "Check", "content": "5/6 ÷ 2/3 rebuilds 5/4, so the answer checks out."},
        {"label": "Answer", "content": "\\(\\frac{5}{6}\\)", "isAnswer": True, "is_answer": True}
      ]
    }
  }
}

pd["guided"] = {
  "opener": {
    "steps": [
      {"say": "Forget the rules for a second. Picture a chocolate bar split into 6 equal squares.<br>" + SVG_BAR},
      {"pre": "You break off one half of the bar to eat. How many of the 6 squares is that? ",
       "answer": 3, "hint": "Half of 6 squares."},
      {"say": "Your friend then breaks off one more single square."},
      {"pre": "Altogether, how many of the 6 squares have gone? ",
       "answer": 4, "hint": "Your 3 squares plus your friend's 1 square."},
      {"say": "You just worked out \\(\\frac{1}{2} + \\frac{1}{6} = \\frac{4}{6} = \\frac{2}{3}\\) with no rules. "
              "The trick was seeing the half as 3 squares out of 6, so both amounts were measured in the same "
              "sized pieces. That is exactly what <strong>finding a common denominator</strong> means: make the "
              "pieces the same size, then count them."}
    ]
  },
  "teach": {
    "bronze": {
      "display": "Calculate \\(\\frac{1}{2} + \\frac{1}{10}\\)",
      "steps": [
        B("The common denominator of 2 and 10 is ", 10, "10 is already in the 2 times table."),
        B("Convert 1/2 into tenths: 2 goes into 10 five times, so 1 × 5 = ", 5, "Multiply the top of 1/2 by 5."),
        SAY("The second fraction, 1/10, is already in tenths."),
        B("Add the tops: 5 + 1 = ", 6, "Add the numerators, keep the denominator 10."),
        B("That gives 6/10. Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 = ", 3, "6 divided by 2."),
        B("Bottom: 10 ÷ 2 = ", 5, "10 divided by 2.",
          done="So 1/2 + 1/10 = 3/5. That is the whole bronze move: match the denominators, add, then simplify.")]
    },
    "silver": {
      "display": "Calculate \\(\\frac{4}{5} \\div \\frac{2}{3}\\)",
      "steps": [
        B("To divide, flip the second fraction. The reciprocal of 2/3 is 3 over 2, so its new top is ", 3, "Swap the top and bottom of 2/3."),
        SAY("Now the sum is 4/5 × 3/2."),
        B("Multiply the tops: 4 × 3 = ", 12, "Multiply the two numerators."),
        B("Multiply the bottoms: 5 × 2 = ", 10, "Multiply the two denominators."),
        B("That gives 12/10. Simplify by dividing top and bottom by 2. Top: 12 ÷ 2 = ", 6, "12 divided by 2."),
        B("Bottom: 10 ÷ 2 = ", 5, "10 divided by 2.",
          done="So 4/5 ÷ 2/3 = 6/5 = 1 1/5. Keep, flip, multiply: that is the whole silver move.")]
    },
    "gold": {
      "display": "Calculate \\(3\\frac{1}{2} \\div 1\\frac{1}{4}\\)",
      "steps": [
        B("Convert 3 1/2 to an improper fraction. Top: 3 × 2 + 1 = ", 7, "Whole times denominator, plus the top."),
        B("Convert 1 1/4 to an improper fraction. Top: 1 × 4 + 1 = ", 5, "Whole times denominator, plus the top."),
        B("To divide, flip the second fraction. The reciprocal of 5/4 is 4 over 5, so its new top is ", 4, "Swap the top and bottom of 5/4."),
        SAY("Now the sum is 7/2 × 4/5."),
        B("Multiply the tops: 7 × 4 = ", 28, "Multiply the two numerators."),
        B("Multiply the bottoms: 2 × 5 = ", 10, "Multiply the two denominators."),
        B("That gives 28/10. Simplify by dividing top and bottom by 2. Top: 28 ÷ 2 = ", 14, "28 divided by 2."),
        B("Bottom: 10 ÷ 2 = ", 5, "10 divided by 2.",
          done="So 3 1/2 ÷ 1 1/4 = 14/5 = 2 4/5. Converting mixed numbers to improper fractions first is the whole gold move.")]
    }
  }
}

json.dump(pd, open("lesson_maths-eduqas_number-L02.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written; bronze/silver/gold =", len(bronze), len(silver), len(gold))
print("preserved keys:", [k for k in pd if k in ("worked_examples","related_videos","topic_links")])
