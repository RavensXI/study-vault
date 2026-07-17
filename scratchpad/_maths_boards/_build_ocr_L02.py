# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_L02_fresh.json", encoding="utf-8"))
pb = pd["problem_bank"]

MINUS = "−"  # unicode minus for plain-text pre fields

def box(pre, answer, hint, post="", done=None, say=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint, "post": post}
    if done is not None: d["done"] = done
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    return d

def say(s):
    return {"say": s}

# ---------- BRONZE ----------
pb["bronze"][5]["display"] = "\\(\\frac{7}{8} - \\frac{1}{8}\\)"
pb["bronze"][5]["solutions"] = [3, 4]
pb["bronze"][7]["display"] = "\\(\\frac{1}{2} + \\frac{1}{6}\\)"
pb["bronze"][7]["solutions"] = [2, 3]

bronze_steps = [
 [say("Add fractions only when the bottoms match. First make them match."),
  box("The lowest common denominator of 4 and 3 is ", 12, "The smallest number both 4 and 3 divide into."),
  box("Rewrite \\(\\frac{1}{4}\\) over 12. Its new top is ", 3, "1 × 3."),
  box("Rewrite \\(\\frac{1}{3}\\) over 12. Its new top is ", 4, "1 × 4."),
  box("Now add the tops over 12: 3 + 4 = ", 7, "Keep the bottom 12; only the tops change.", phase="substitute"),
  box("\\(\\frac{7}{12}\\) is already in lowest terms, so the final bottom stays ", 12, "7 and 12 share no common factor.", done="So \\(\\frac{1}{4} + \\frac{1}{3} = \\frac{7}{12}\\)."),
  box("Check by subtracting back: 7 " + MINUS + " 4 = ", 3, "Should give 3, the first fraction in twelfths.", done="3/12 = 1/4, so 7/12 is right.")],
 [say("These already share the bottom 5, so just add the tops."),
  box("The denominators are both 5, so the answer's bottom is ", 5, "Same bottoms stay the same when adding."),
  box("Add the tops: 3 + 1 = ", 4, "Add the numerators, keep the bottom 5.", phase="substitute"),
  box("\\(\\frac{4}{5}\\) is already in lowest terms, so the final bottom stays ", 5, "4 and 5 share no common factor.", done="So \\(\\frac{3}{5} + \\frac{1}{5} = \\frac{4}{5}\\)."),
  box("Check by subtracting back: 4 " + MINUS + " 1 = ", 3, "Should give 3, the first fraction's top.", done="3/5 was the first fraction, so 4/5 is right.")],
 [say("Subtract fractions only when the bottoms match. First make them match."),
  box("The lowest common denominator of 6 and 3 is ", 6, "6 is already in the 3 times table."),
  box("Rewrite \\(\\frac{1}{3}\\) over 6. Its new top is ", 2, "1 × 2."),
  say("The first fraction, 5/6, is already in sixths."),
  box("Subtract the tops: 5 " + MINUS + " 2 = ", 3, "Keep the bottom 6; only the tops change.", phase="substitute"),
  box("That gives \\(\\frac{3}{6}\\). Simplify by dividing top and bottom by 3. Top: 3 ÷ 3 = ", 1, "3 divided by 3."),
  box("Bottom: 6 ÷ 3 = ", 2, "6 divided by 3.", done="So \\(\\frac{5}{6} - \\frac{1}{3} = \\frac{1}{2}\\)."),
  box("Check: turn 1/2 back into sixths. 1 × 3 = ", 3, "If it gives 3/6, the answer matches.", done="3/6 matches, so 1/2 is correct.")],
 [say("These already share the bottom 7, so just add the tops."),
  box("The denominators are both 7, so the answer's bottom is ", 7, "Same bottoms stay the same when adding."),
  box("Add the tops: 2 + 3 = ", 5, "Add the numerators, keep the bottom 7.", phase="substitute"),
  box("\\(\\frac{5}{7}\\) is already in lowest terms, so the final bottom stays ", 7, "5 and 7 share no common factor.", done="So \\(\\frac{2}{7} + \\frac{3}{7} = \\frac{5}{7}\\)."),
  box("Check by subtracting back: 5 " + MINUS + " 3 = ", 2, "Should give 2, the first fraction's top.", done="2/7 was the first fraction, so 5/7 is right.")],
 [say("Multiplying needs no common denominator. Multiply straight across."),
  box("Multiply the tops: 1 × 3 = ", 3, "Multiply the two numerators."),
  box("Multiply the bottoms: 2 × 4 = ", 8, "Multiply the two denominators.", phase="substitute"),
  box("Check for common factors: 3 and 8 share only 1, so the top stays ", 3, "Nothing cancels."),
  box("and the bottom stays ", 8, "Already in lowest terms.", done="So \\(\\frac{1}{2} \\times \\frac{3}{4} = \\frac{3}{8}\\).")],
 [say("These already share the bottom 8, so just subtract the tops."),
  box("The denominators are both 8, so the answer's bottom starts as ", 8, "Same bottoms stay the same when subtracting."),
  box("Subtract the tops: 7 " + MINUS + " 1 = ", 6, "Keep the bottom 8; only the tops change.", phase="substitute"),
  box("That gives \\(\\frac{6}{8}\\). Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 = ", 3, "6 divided by 2."),
  box("Bottom: 8 ÷ 2 = ", 4, "8 divided by 2.", done="So \\(\\frac{7}{8} - \\frac{1}{8} = \\frac{3}{4}\\)."),
  box("Check: turn 3/4 back into eighths. 3 × 2 = ", 6, "If it gives 6/8, the answer matches.", done="6/8 matches, so 3/4 is correct.")],
 [say("Multiply straight across, then simplify."),
  box("Multiply the tops: 2 × 5 = ", 10, "Multiply the two numerators."),
  box("Multiply the bottoms: 5 × 6 = ", 30, "Multiply the two denominators."),
  box("Simplify \\(\\frac{10}{30}\\) by dividing top and bottom by 10. Top: 10 ÷ 10 = ", 1, "10 divided by 10.", phase="substitute"),
  box("Bottom: 30 ÷ 10 = ", 3, "30 divided by 10.", done="So \\(\\frac{2}{5} \\times \\frac{5}{6} = \\frac{1}{3}\\)."),
  box("Check: turn 1/3 back up by 10. 1 × 10 = ", 10, "If it gives 10/30, the answer matches.", done="10/30 matches, so 1/3 is correct.")],
 [say("Add fractions only when the bottoms match. First make them match."),
  box("The lowest common denominator of 2 and 6 is ", 6, "6 is already in the 2 times table."),
  box("Rewrite \\(\\frac{1}{2}\\) over 6. Its new top is ", 3, "1 × 3."),
  say("The second fraction, 1/6, is already in sixths."),
  box("Add the tops: 3 + 1 = ", 4, "Keep the bottom 6; only the tops change.", phase="substitute"),
  box("That gives \\(\\frac{4}{6}\\). Simplify by dividing top and bottom by 2. Top: 4 ÷ 2 = ", 2, "4 divided by 2."),
  box("Bottom: 6 ÷ 2 = ", 3, "6 divided by 2.", done="So \\(\\frac{1}{2} + \\frac{1}{6} = \\frac{2}{3}\\)."),
  box("Check: turn 2/3 back into sixths. 2 × 2 = ", 4, "If it gives 4/6, the answer matches.", done="4/6 matches, so 2/3 is correct.")],
]

bronze_hints = [
 "The LCD of 4 and 3 is 12; convert both, then add the tops.",
 "Same denominator already: just add the numerators over 5.",
 "Convert 1/3 to sixths, subtract, then simplify.",
 "Same denominator already: just add the numerators over 7.",
 "Multiply straight across: tops together, bottoms together.",
 "Same denominator: subtract the tops, then simplify.",
 "Multiply straight across, then cancel by 10.",
 "Convert 1/2 to sixths, add, then simplify.",
]

bronze_misc = [
 [{"pattern":"add_denominators","expect":[2,7],
   "message":"Do not add the bottoms. Use LCD 12: \\(\\frac{3}{12} + \\frac{4}{12} = \\frac{7}{12}\\). Adding tops and bottoms gives \\(\\frac{2}{7}\\).",
   "note":"Student adds numerators and denominators: (1+1)/(4+3) = 2/7."}],
 [{"pattern":"add_denominators","expect":[4,10],
   "message":"The bottoms already match, so keep the 5. Adding the bottoms too gives \\(\\frac{4}{10}\\); the correct answer is \\(\\frac{4}{5}\\).",
   "note":"Student adds denominators: (3+1)/(5+5) = 4/10."}],
 [{"pattern":"subtract_across","expect":[4,3],
   "message":"You cannot subtract tops and bottoms separately. Convert 1/3 to 2/6 first: \\(\\frac{5}{6} - \\frac{2}{6} = \\frac{3}{6} = \\frac{1}{2}\\).",
   "note":"Student subtracts across: (5-1)/(6-3) = 4/3."},
  {"pattern":"no_simplify","expect":[3,6],
   "message":"\\(\\frac{3}{6}\\) is correct but not simplified. Divide top and bottom by 3 to get \\(\\frac{1}{2}\\).",
   "note":"Student stops at 3/6 without simplifying."}],
 [{"pattern":"add_denominators","expect":[5,14],
   "message":"The bottoms already match, so keep the 7. Adding the bottoms too gives \\(\\frac{5}{14}\\); the correct answer is \\(\\frac{5}{7}\\).",
   "note":"Student adds denominators: (2+3)/(7+7) = 5/14."}],
 [{"pattern":"common_denominator","expect":None,
   "message":"You do not need a common denominator to multiply. Go straight across: 1 × 3 = 3 and 2 × 4 = 8, giving \\(\\frac{3}{8}\\).",
   "note":"Student wrongly hunts for an LCD before multiplying; no single determinate wrong value."}],
 [{"pattern":"subtract_denominators","expect":None,
   "message":"The bottoms are the same, so keep the 8. Just subtract the tops: 7 " + MINUS + " 1 = 6, then simplify \\(\\frac{6}{8} = \\frac{3}{4}\\).",
   "note":"Subtracting denominators too gives 6/0, undefined; no determinate wrong value."},
  {"pattern":"no_simplify","expect":[6,8],
   "message":"\\(\\frac{6}{8}\\) is correct but not simplified. Divide top and bottom by 2 to get \\(\\frac{3}{4}\\).",
   "note":"Student stops at 6/8 without simplifying."}],
 [{"pattern":"no_simplify","expect":[10,30],
   "message":"\\(\\frac{10}{30}\\) is correct but not simplified. Divide top and bottom by 10 to get \\(\\frac{1}{3}\\).",
   "note":"Student multiplies to 10/30 but stops without simplifying."}],
 [{"pattern":"add_denominators","expect":[2,8],
   "message":"Do not add the bottoms. Use LCD 6: \\(\\frac{3}{6} + \\frac{1}{6} = \\frac{4}{6} = \\frac{2}{3}\\). Adding tops and bottoms gives \\(\\frac{2}{8}\\).",
   "note":"Student adds numerators and denominators: (1+1)/(2+6) = 2/8."},
  {"pattern":"no_simplify","expect":[4,6],
   "message":"\\(\\frac{4}{6}\\) is correct but not simplified. Divide top and bottom by 2 to get \\(\\frac{2}{3}\\).",
   "note":"Student stops at 4/6 without simplifying."}],
]

# ---------- SILVER ----------
silver_steps = [
 [say("Add fractions only when the bottoms match. Find the common denominator."),
  box("The lowest common denominator of 3 and 8 is ", 24, "3 × 8, since they share no factor."),
  box("Rewrite \\(\\frac{2}{3}\\) over 24. Its new top is ", 16, "2 × 8."),
  box("Rewrite \\(\\frac{5}{8}\\) over 24. Its new top is ", 15, "5 × 3."),
  box("Add the tops over 24: 16 + 15 = ", 31, "Keep the bottom 24; only the tops change.", phase="substitute"),
  box("\\(\\frac{31}{24}\\) is already in lowest terms, so the final bottom stays ", 24, "31 is prime and shares no factor with 24.", done="So \\(\\frac{2}{3} + \\frac{5}{8} = \\frac{31}{24}\\), i.e. \\(1\\frac{7}{24}\\)."),
  box("Check by subtracting back: 31 " + MINUS + " 15 = ", 16, "Should give 16, the first fraction in 24ths.", done="16/24 = 2/3, so 31/24 is right.")],
 [say("Subtract fractions only when the bottoms match. Find the common denominator."),
  box("The lowest common denominator of 4 and 5 is ", 20, "4 × 5, since they share no factor."),
  box("Rewrite \\(\\frac{3}{4}\\) over 20. Its new top is ", 15, "3 × 5."),
  box("Rewrite \\(\\frac{2}{5}\\) over 20. Its new top is ", 8, "2 × 4."),
  box("Subtract the tops over 20: 15 " + MINUS + " 8 = ", 7, "Keep the bottom 20; only the tops change.", phase="substitute"),
  box("\\(\\frac{7}{20}\\) is already in lowest terms, so the final bottom stays ", 20, "7 and 20 share no common factor.", done="So \\(\\frac{3}{4} - \\frac{2}{5} = \\frac{7}{20}\\)."),
  box("Check by adding back: 7 + 8 = ", 15, "Should give 15, the first fraction in 20ths.", done="15/20 = 3/4, so 7/20 is right.")],
 [say("Multiply straight across, then simplify."),
  box("Multiply the tops: 3 × 10 = ", 30, "Multiply the two numerators."),
  box("Multiply the bottoms: 5 × 9 = ", 45, "Multiply the two denominators."),
  box("Simplify \\(\\frac{30}{45}\\) by dividing top and bottom by 15. Top: 30 ÷ 15 = ", 2, "30 divided by 15.", phase="substitute"),
  box("Bottom: 45 ÷ 15 = ", 3, "45 divided by 15.", done="So \\(\\frac{3}{5} \\times \\frac{10}{9} = \\frac{2}{3}\\)."),
  box("Check: turn 2/3 back up by 15. 2 × 15 = ", 30, "If it gives 30/45, the answer matches.", done="30/45 matches, so 2/3 is correct.")],
 [say("To divide, use Keep, Flip, Change: \\(\\frac{4}{5} \\div \\frac{2}{3}\\) becomes \\(\\frac{4}{5} \\times \\frac{3}{2}\\)."),
  box("Multiply the tops: 4 × 3 = ", 12, "Multiply the two numerators."),
  box("Multiply the bottoms: 5 × 2 = ", 10, "Multiply the two denominators.", phase="substitute"),
  box("Simplify \\(\\frac{12}{10}\\) by dividing top and bottom by 2. Top: 12 ÷ 2 = ", 6, "12 divided by 2."),
  box("Bottom: 10 ÷ 2 = ", 5, "10 divided by 2.", done="So \\(\\frac{4}{5} \\div \\frac{2}{3} = \\frac{6}{5}\\), i.e. \\(1\\frac{1}{5}\\)."),
  box("Check: multiply back, \\(\\frac{6}{5} \\times \\frac{2}{3}\\), tops 6 × 2 = ", 12, "If it rebuilds 4/5, the answer is right.", done="12/15 = 4/5, so 6/5 is correct.")],
 [say("Turn the mixed number into an improper fraction first."),
  box("\\(1\\frac{1}{3}\\) as an improper fraction: top = 1 × 3 + 1 = ", 4, "Whole times denominator, plus the top."),
  say("So \\(1\\frac{1}{3} = \\frac{4}{3}\\). The sum is \\(\\frac{4}{3} + \\frac{2}{5}\\)."),
  box("The lowest common denominator of 3 and 5 is ", 15, "3 × 5."),
  box("Rewrite \\(\\frac{4}{3}\\) over 15. Its new top is ", 20, "4 × 5."),
  box("Rewrite \\(\\frac{2}{5}\\) over 15. Its new top is ", 6, "2 × 3."),
  box("Add the tops over 15: 20 + 6 = ", 26, "Keep the bottom 15; only the tops change.", phase="substitute"),
  box("\\(\\frac{26}{15}\\) is already in lowest terms, so the final bottom stays ", 15, "26 and 15 share no common factor.", done="So \\(1\\frac{1}{3} + \\frac{2}{5} = \\frac{26}{15}\\), i.e. \\(1\\frac{11}{15}\\)."),
  box("Check by subtracting back: 26 " + MINUS + " 6 = ", 20, "Should give 20, which is 4/3 in fifteenths.", done="20/15 = 4/3 = 1 1/3, so 26/15 is right.")],
 [say("To divide, use Keep, Flip, Change: \\(\\frac{5}{6} \\div \\frac{5}{12}\\) becomes \\(\\frac{5}{6} \\times \\frac{12}{5}\\)."),
  box("Multiply the tops: 5 × 12 = ", 60, "Multiply the two numerators."),
  box("Multiply the bottoms: 6 × 5 = ", 30, "Multiply the two denominators.", phase="substitute"),
  box("Divide: 60 ÷ 30 = ", 2, "Top divided by bottom.", done="So \\(\\frac{5}{6} \\div \\frac{5}{12} = 2\\)."),
  box("Check: multiply back, \\(2 \\times \\frac{5}{12}\\), tops 2 × 5 = ", 10, "If it rebuilds 5/6, the answer is right.", done="10/12 = 5/6, so 2 is correct.")],
 [say("Subtract fractions only when the bottoms match. Find the common denominator."),
  box("The lowest common denominator of 10 and 4 is ", 20, "The smallest number both 10 and 4 divide into."),
  box("Rewrite \\(\\frac{7}{10}\\) over 20. Its new top is ", 14, "7 × 2."),
  box("Rewrite \\(\\frac{1}{4}\\) over 20. Its new top is ", 5, "1 × 5."),
  box("Subtract the tops over 20: 14 " + MINUS + " 5 = ", 9, "Keep the bottom 20; only the tops change.", phase="substitute"),
  box("\\(\\frac{9}{20}\\) is already in lowest terms, so the final bottom stays ", 20, "9 and 20 share no common factor.", done="So \\(\\frac{7}{10} - \\frac{1}{4} = \\frac{9}{20}\\)."),
  box("Check by adding back: 9 + 5 = ", 14, "Should give 14, the first fraction in 20ths.", done="14/20 = 7/10, so 9/20 is right.")],
]

silver_hints = [
 "The LCD of 3 and 8 is 24; convert both, then add.",
 "The LCD of 4 and 5 is 20; convert both, then subtract.",
 "Multiply straight across, then cancel by 15.",
 "Keep the first, flip 2/3 to 3/2, then multiply.",
 "Turn 1 1/3 into 4/3, then add using LCD 15.",
 "Keep, flip, multiply: 5/6 × 12/5, then cancel.",
 "The LCD of 10 and 4 is 20; convert both, then subtract.",
]

silver_misc = [
 [{"pattern":"add_denominators","expect":[7,11],
   "message":"Do not add the bottoms. Use LCD 24: \\(\\frac{16}{24} + \\frac{15}{24} = \\frac{31}{24}\\). Adding tops and bottoms gives \\(\\frac{7}{11}\\).",
   "note":"(2+5)/(3+8) = 7/11."}],
 [{"pattern":"no_scale_numerators","expect":[1,20],
   "message":"When you change the denominator to 20, scale the tops too: \\(\\frac{15}{20} - \\frac{8}{20} = \\frac{7}{20}\\). Leaving the tops as 3 and 2 gives \\(\\frac{1}{20}\\).",
   "note":"Student writes 3/20 - 2/20 = 1/20 without scaling numerators."}],
 [{"pattern":"no_simplify","expect":[30,45],
   "message":"\\(\\frac{30}{45}\\) is correct but not simplified. Divide top and bottom by 15 to get \\(\\frac{2}{3}\\).",
   "note":"Student multiplies to 30/45 but stops."}],
 [{"pattern":"no_flip","expect":[8,15],
   "message":"To divide, flip the second fraction: \\(\\frac{4}{5} \\times \\frac{3}{2} = \\frac{12}{10} = \\frac{6}{5}\\). Multiplying without flipping gives \\(\\frac{8}{15}\\).",
   "note":"4/5 x 2/3 = 8/15."}],
 [{"pattern":"ignore_whole","expect":[11,15],
   "message":"Do not drop the whole number. Convert first: \\(1\\frac{1}{3} = \\frac{4}{3}\\), so \\(\\frac{4}{3} + \\frac{2}{5} = \\frac{26}{15}\\). Using only \\(\\frac{1}{3} + \\frac{2}{5}\\) gives \\(\\frac{11}{15}\\).",
   "note":"Student ignores the whole 1: 1/3 + 2/5 = 11/15."}],
 [{"pattern":"no_flip","expect":None,
   "message":"To divide, flip the second fraction: \\(\\frac{5}{6} \\times \\frac{12}{5} = \\frac{60}{30} = 2\\). Multiplying without flipping gives \\(\\frac{25}{72}\\), not a whole number.",
   "note":"5/6 x 5/12 = 25/72; not a clean single value."}],
 [{"pattern":"no_scale_numerators","expect":[6,20],
   "message":"When you change the denominator to 20, scale the tops too: \\(\\frac{14}{20} - \\frac{5}{20} = \\frac{9}{20}\\). Leaving the tops as 7 and 1 gives \\(\\frac{6}{20}\\).",
   "note":"Student writes 7/20 - 1/20 = 6/20 without scaling numerators."}],
]

# ---------- GOLD ----------
gold_steps = [
 [say("Three fractions: put them all over one common bottom."),
  box("The lowest common denominator of 3, 4 and 6 is ", 12, "The smallest number 3, 4 and 6 all divide into."),
  box("Rewrite \\(\\frac{2}{3}\\) over 12. Its new top is ", 8, "2 × 4."),
  box("Rewrite \\(\\frac{3}{4}\\) over 12. Its new top is ", 9, "3 × 3."),
  box("Rewrite \\(\\frac{1}{6}\\) over 12. Its new top is ", 2, "1 × 2."),
  box("Combine the tops in order over 12: 8 + 9 " + MINUS + " 2 = ", 15, "Add the first two, then subtract the third.", phase="substitute"),
  box("That gives \\(\\frac{15}{12}\\). Simplify by dividing top and bottom by 3. Top: 15 ÷ 3 = ", 5, "15 divided by 3."),
  box("Bottom: 12 ÷ 3 = ", 4, "12 divided by 3.", done="So \\(\\frac{2}{3} + \\frac{3}{4} - \\frac{1}{6} = \\frac{5}{4}\\), i.e. \\(1\\frac{1}{4}\\)."),
  box("Check: turn 5/4 back up by 3. 5 × 3 = ", 15, "If it gives 15/12, the answer matches.", done="15/12 matches, so 5/4 is correct.")],
 [say("Change both mixed numbers to improper fractions, then multiply."),
  box("\\(2\\frac{1}{2}\\): top = 2 × 2 + 1 = ", 5, "Whole times denominator, plus the top."),
  box("\\(1\\frac{3}{5}\\): top = 1 × 5 + 3 = ", 8, "Whole times denominator, plus the top."),
  say("So the sum is \\(\\frac{5}{2} \\times \\frac{8}{5}\\)."),
  box("Multiply the tops: 5 × 8 = ", 40, "Multiply the two numerators."),
  box("Multiply the bottoms: 2 × 5 = ", 10, "Multiply the two denominators.", phase="substitute"),
  box("Divide: 40 ÷ 10 = ", 4, "Top divided by bottom.", done="So \\(2\\frac{1}{2} \\times 1\\frac{3}{5} = 4\\)."),
  box("Check with decimals: 2.5 × 1.6 = ", 4, "A quick decimal check of the answer.", done="2.5 × 1.6 = 4, so the answer is right.")],
 [say("Change both mixed numbers to improper fractions first."),
  box("\\(3\\frac{1}{4}\\): top = 3 × 4 + 1 = ", 13, "Whole times denominator, plus the top."),
  box("\\(1\\frac{2}{3}\\): top = 1 × 3 + 2 = ", 5, "Whole times denominator, plus the top."),
  box("The lowest common denominator of 4 and 3 is ", 12, "4 × 3, since they share no factor."),
  box("Rewrite \\(\\frac{13}{4}\\) over 12. Its new top is ", 39, "13 × 3."),
  box("Rewrite \\(\\frac{5}{3}\\) over 12. Its new top is ", 20, "5 × 4."),
  box("Subtract the tops over 12: 39 " + MINUS + " 20 = ", 19, "Keep the bottom 12; only the tops change.", phase="substitute"),
  box("\\(\\frac{19}{12}\\) is already in lowest terms, so the final bottom stays ", 12, "19 is prime and shares no factor with 12.", done="So \\(3\\frac{1}{4} - 1\\frac{2}{3} = \\frac{19}{12}\\), i.e. \\(1\\frac{7}{12}\\)."),
  box("Check by adding back: 20 + 19 = ", 39, "Should give 39, which is 13/4 in twelfths.", done="39/12 = 3 1/4, so 19/12 is right.")],
 [say("To divide, use Keep, Flip, Change: \\(\\frac{3}{8} \\div \\frac{9}{16}\\) becomes \\(\\frac{3}{8} \\times \\frac{16}{9}\\)."),
  box("Multiply the tops: 3 × 16 = ", 48, "Multiply the two numerators."),
  box("Multiply the bottoms: 8 × 9 = ", 72, "Multiply the two denominators.", phase="substitute"),
  box("Simplify \\(\\frac{48}{72}\\) by dividing top and bottom by 24. Top: 48 ÷ 24 = ", 2, "48 divided by 24."),
  box("Bottom: 72 ÷ 24 = ", 3, "72 divided by 24.", done="So \\(\\frac{3}{8} \\div \\frac{9}{16} = \\frac{2}{3}\\)."),
  box("Check: multiply back, \\(\\frac{2}{3} \\times \\frac{9}{16}\\), tops 2 × 9 = ", 18, "If it rebuilds 3/8, the answer is right.", done="18/48 = 3/8, so 2/3 is correct.")],
 [say("Order of operations: multiplication before addition. First do \\(\\frac{5}{6} \\times \\frac{3}{10}\\)."),
  box("Multiply the tops: 5 × 3 = ", 15, "Multiply the two numerators."),
  box("Multiply the bottoms: 6 × 10 = ", 60, "Multiply the two denominators."),
  box("Simplify \\(\\frac{15}{60}\\) by dividing top and bottom by 15. Top: 15 ÷ 15 = ", 1, "15 divided by 15."),
  box("Bottom: 60 ÷ 15 = ", 4, "60 divided by 15."),
  say("So \\(\\frac{5}{6} \\times \\frac{3}{10} = \\frac{1}{4}\\). Now add \\(\\frac{1}{4}\\)."),
  box("Both are quarters, so add the tops: 1 + 1 = ", 2, "Keep the bottom 4; add the numerators.", phase="substitute"),
  box("That gives \\(\\frac{2}{4}\\). Simplify by dividing top and bottom by 2. Top: 2 ÷ 2 = ", 1, "2 divided by 2."),
  box("Bottom: 4 ÷ 2 = ", 2, "4 divided by 2.", done="So \\(\\frac{5}{6} \\times \\frac{3}{10} + \\frac{1}{4} = \\frac{1}{2}\\)."),
  box("Check: \\(\\frac{1}{4} + \\frac{1}{4} = \\frac{2}{4}\\), which halves to 1 over ", 2, "Two quarters make a half.", done="1/2 is correct.")],
]

gold_hints = [
 "Convert all three to twelfths, combine the tops in order, then simplify.",
 "Convert to 5/2 and 8/5, multiply across, then cancel to a whole number.",
 "Convert to 13/4 and 5/3, use LCD 12, then subtract.",
 "Keep 3/8, flip 9/16 to 16/9, multiply, then simplify.",
 "Order of operations: multiply 5/6 × 3/10 first, then add 1/4.",
]

gold_misc = [
 [{"pattern":"combine_across","expect":[4,1],
   "message":"Use LCD 12: \\(\\frac{8}{12} + \\frac{9}{12} - \\frac{2}{12} = \\frac{15}{12} = \\frac{5}{4}\\). Combining tops and bottoms directly gives \\(\\frac{4}{1}\\).",
   "note":"(2+3-1)/(3+4-6) = 4/1."},
  {"pattern":"no_simplify","expect":[15,12],
   "message":"\\(\\frac{15}{12}\\) is correct but not simplified. Divide top and bottom by 3 to get \\(\\frac{5}{4}\\).",
   "note":"Student stops at 15/12."}],
 [{"pattern":"ignore_whole","expect":None,
   "message":"Convert both mixed numbers first: \\(\\frac{5}{2} \\times \\frac{8}{5} = 4\\). Multiplying only the whole parts, or only the fraction parts, does not give a whole number.",
   "note":"Partial products (2x1=2, or 1/2 x 3/5 = 3/10) do not form one clean value."}],
 [{"pattern":"split_no_borrow","expect":[29,12],
   "message":"You cannot subtract the parts as \\(\\frac{2}{3} - \\frac{1}{4}\\), because \\(\\frac{1}{4}\\) is smaller than \\(\\frac{2}{3}\\). Convert first: \\(\\frac{13}{4} - \\frac{5}{3} = \\frac{39}{12} - \\frac{20}{12} = \\frac{19}{12}\\).",
   "note":"Student does wholes 3-1=2 and flips the gap 2/3-1/4=5/12, giving 2 5/12 = 29/12."}],
 [{"pattern":"no_flip","expect":[27,128],
   "message":"To divide, flip the second fraction: \\(\\frac{3}{8} \\times \\frac{16}{9} = \\frac{48}{72} = \\frac{2}{3}\\). Multiplying without flipping gives \\(\\frac{27}{128}\\).",
   "note":"3/8 x 9/16 = 27/128."}],
 [{"pattern":"order_error","expect":[11,24],
   "message":"Multiplication comes before addition. Do \\(\\frac{5}{6} \\times \\frac{3}{10} = \\frac{1}{4}\\) first, then add \\(\\frac{1}{4}\\) to get \\(\\frac{1}{2}\\). Adding \\(\\frac{3}{10} + \\frac{1}{4}\\) first gives \\(\\frac{11}{24}\\).",
   "note":"5/6 x (3/10 + 1/4) = 5/6 x 11/20 = 11/24."}],
]

for i, p in enumerate(pb["bronze"]):
    p["hint"] = bronze_hints[i]; p["guided_steps"] = bronze_steps[i]; p["misconceptions"] = bronze_misc[i]
for i, p in enumerate(pb["silver"]):
    p["hint"] = silver_hints[i]; p["guided_steps"] = silver_steps[i]; p["misconceptions"] = silver_misc[i]
for i, p in enumerate(pb["gold"]):
    p["hint"] = gold_hints[i]; p["guided_steps"] = gold_steps[i]; p["misconceptions"] = gold_misc[i]

pb["bronze_description"] = "Add, subtract or multiply two simple fractions, then simplify to lowest terms."
pb["silver_description"] = "The four operations with harder numbers, now including division (KFC) and a mixed number."
pb["gold_description"] = "Multi-step problems: three fractions, mixed numbers, or an order-of-operations chain, simplifying throughout."

pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: adding, subtracting and multiplying simple fractions",
  "steps": [
   "For <strong>+</strong> or <strong>−</strong>: give both fractions the same denominator, then combine the tops only.",
   "For <strong>×</strong>: no common denominator is needed. Multiply the tops together and the bottoms together.",
   "Always simplify the final fraction by dividing top and bottom by their highest common factor."
  ],
  "example": {
   "question": "Work out \\(\\frac{3}{4} \\times \\frac{2}{3}\\)",
   "steps": [
    {"label": "Multiply across", "content": "3 × 2 = 6 and 4 × 3 = 12, giving \\(\\frac{6}{12}\\)."},
    {"label": "Simplify", "content": "Divide top and bottom by 6: \\(\\frac{6}{12} = \\frac{1}{2}\\)."},
    {"label": "Check", "content": "1 and 2 share no factor, so it is simplest."},
    {"label": "Answer", "content": "\\(\\frac{1}{2}\\)", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "silver": {
  "title": "Silver: dividing fractions and using mixed numbers",
  "steps": [
   "To <strong>divide</strong>, use KFC: Keep the first fraction, Flip the second, Change ÷ to ×, then multiply.",
   "Turn every <strong>mixed number</strong> into an improper fraction first: whole × bottom + top, over the same bottom.",
   "Multiply or add as usual, then simplify the answer."
  ],
  "example": {
   "question": "Work out \\(\\frac{3}{4} \\div \\frac{1}{2}\\)",
   "steps": [
    {"label": "Keep, Flip, Change", "content": "\\(\\frac{3}{4} \\div \\frac{1}{2} = \\frac{3}{4} \\times \\frac{2}{1}\\)."},
    {"label": "Multiply across", "content": "3 × 2 = 6 and 4 × 1 = 4, giving \\(\\frac{6}{4}\\)."},
    {"label": "Simplify", "content": "Divide top and bottom by 2: \\(\\frac{6}{4} = \\frac{3}{2}\\)."},
    {"label": "Check", "content": "\\(\\frac{3}{2} \\times \\frac{1}{2} = \\frac{3}{4}\\), rebuilding the first fraction."},
    {"label": "Answer", "content": "\\(\\frac{3}{2}\\)", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "gold": {
  "title": "Gold: three fractions, mixed numbers and order of operations",
  "steps": [
   "Convert every mixed number to an improper fraction before you start.",
   "For a chain of fractions, give them all one common denominator, then combine the tops in order.",
   "With mixed operations follow <strong>order of operations</strong>: do × and ÷ before + and −. Simplify at the end."
  ],
  "example": {
   "question": "Work out \\(\\frac{2}{3} \\div \\frac{4}{9} + \\frac{1}{2}\\)",
   "steps": [
    {"label": "Divide first", "content": "\\(\\frac{2}{3} \\div \\frac{4}{9} = \\frac{2}{3} \\times \\frac{9}{4} = \\frac{18}{12} = \\frac{3}{2}\\)."},
    {"label": "Then add", "content": "\\(\\frac{3}{2} + \\frac{1}{2} = \\frac{4}{2}\\)."},
    {"label": "Simplify", "content": "\\(\\frac{4}{2} = 2\\)."},
    {"label": "Check", "content": "Division was done before addition, as order of operations requires."},
    {"label": "Answer", "content": "\\(2\\)", "isAnswer": True, "is_answer": True}
   ]
  }
 }
}

OPENER_SVG = "<svg viewBox=\"0 0 192 148\" role=\"img\" aria-label=\"A chocolate bar of 12 equal squares: 3 squares shaded blue and 4 squares shaded orange\"><rect x=\"8\" y=\"8\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#60a5fa\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"52\" y=\"8\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#60a5fa\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"96\" y=\"8\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#60a5fa\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"140\" y=\"8\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#f59e0b\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"8\" y=\"52\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#f59e0b\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"52\" y=\"52\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#f59e0b\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"96\" y=\"52\" width=\"44\" height=\"44\" rx=\"4\" fill=\"#f59e0b\" fill-opacity=\"0.35\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"140\" y=\"52\" width=\"44\" height=\"44\" rx=\"4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"8\" y=\"96\" width=\"44\" height=\"44\" rx=\"4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"52\" y=\"96\" width=\"44\" height=\"44\" rx=\"4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"96\" y=\"96\" width=\"44\" height=\"44\" rx=\"4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"140\" y=\"96\" width=\"44\" height=\"44\" rx=\"4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><text x=\"96\" y=\"142\" text-anchor=\"middle\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"currentColor\">12 squares in the bar</text></svg><br>A chocolate bar has <strong>12 equal squares</strong>. You eat \\(\\frac{1}{4}\\) of it (the blue squares), then \\(\\frac{1}{3}\\) of it (the orange squares)."

pd["guided"] = {
 "opener": {
  "label": "Before any fraction rules",
  "display": OPENER_SVG,
  "steps": [
   {"pre": "\\(\\frac{1}{4}\\) of the 12 squares is ", "post": " squares", "answer": 3,
    "say": "No fraction rules yet, just count squares.", "hint": "12 shared into 4 equal groups."},
   {"pre": "\\(\\frac{1}{3}\\) of the 12 squares is ", "post": " squares", "answer": 4,
    "hint": "12 shared into 3 equal groups."},
   {"pre": "So altogether you ate 3 + 4 = ", "post": " squares", "answer": 7,
    "hint": "Add the two amounts of squares.", "done": "7 out of 12 squares."},
   {"say": "You just found \\(\\frac{1}{4} + \\frac{1}{3} = \\frac{7}{12}\\) by counting. Why did 12 work so neatly? Because 12 splits evenly into quarters AND thirds. That shared bottom number is the <strong>common denominator</strong>, and it is the whole trick to adding fractions."}
  ]
 },
 "teach": {
  "bronze": {
   "label": "Together: your first one",
   "display": "Work out \\(\\frac{1}{4} + \\frac{1}{12}\\)",
   "steps": [
    say("Add fractions only when the bottoms match. First make them match."),
    box("The lowest common denominator of 4 and 12 is ", 12, "12 is already in the 4 times table."),
    box("Rewrite \\(\\frac{1}{4}\\) over 12. Its new top is ", 3, "1 × 3."),
    say("The second fraction, 1/12, is already in twelfths."),
    box("Add the tops: 3 + 1 = ", 4, "Keep the bottom 12; only the tops change."),
    box("That gives \\(\\frac{4}{12}\\). Simplify by dividing top and bottom by 4. Top: 4 ÷ 4 = ", 1, "4 divided by 4."),
    box("Bottom: 12 ÷ 4 = ", 3, "12 divided by 4.", done="So 1/4 + 1/12 = 1/3. Match the bottoms, add, then simplify: that is the whole bronze move.")
   ]
  },
  "silver": {
   "label": "Together: a division",
   "display": "Work out \\(\\frac{2}{3} \\div \\frac{4}{9}\\)",
   "steps": [
    say("To divide, use Keep, Flip, Change: \\(\\frac{2}{3} \\div \\frac{4}{9}\\) becomes \\(\\frac{2}{3} \\times \\frac{9}{4}\\)."),
    box("Multiply the tops: 2 × 9 = ", 18, "Multiply the two numerators."),
    box("Multiply the bottoms: 3 × 4 = ", 12, "Multiply the two denominators."),
    box("Simplify \\(\\frac{18}{12}\\) by dividing top and bottom by 6. Top: 18 ÷ 6 = ", 3, "18 divided by 6."),
    box("Bottom: 12 ÷ 6 = ", 2, "12 divided by 6.", done="So 2/3 ÷ 4/9 = 3/2. Keep, Flip, Change: that is the whole silver move.")
   ]
  },
  "gold": {
   "label": "Together: two operations",
   "display": "Work out \\(\\frac{3}{4} \\div \\frac{1}{2} - \\frac{1}{2}\\)",
   "steps": [
    say("Two operations. Division comes before subtraction, so do \\(\\frac{3}{4} \\div \\frac{1}{2}\\) first."),
    box("Keep, Flip, Change to \\(\\frac{3}{4} \\times \\frac{2}{1}\\). Multiply the tops: 3 × 2 = ", 6, "3 times 2."),
    box("Multiply the bottoms: 4 × 1 = ", 4, "4 times 1."),
    box("Simplify \\(\\frac{6}{4}\\) by dividing by 2: the top is ", 3, "6 ÷ 2, giving three halves."),
    box("Now subtract \\(\\frac{1}{2}\\). Same bottom 2, so subtract the tops: 3 " + MINUS + " 1 = ", 2, "The division gave 3/2."),
    box("Simplify \\(\\frac{2}{2}\\): the top is ", 1, "2 ÷ 2."),
    box("and the bottom is ", 1, "2 ÷ 2.", done="\\(\\frac{2}{2} = 1\\). Order of operations settled it.")
   ]
  }
 }
}

pd["method_card"] = {
 "title": "Working with Fractions",
 "steps": [
  "Add or subtract: use a common denominator, then combine the numerators only.",
  "Multiply: tops together, bottoms together, then cancel.",
  "Divide: Keep the first, Flip the second, Change ÷ to × (KFC).",
  "Mixed numbers: change to improper fractions first, and always simplify at the end."
 ],
 "content": "<p>A <strong>fraction</strong> is a part of a whole: the top (numerator) counts the parts, the bottom (denominator) says how many equal parts make one whole.</p><p><strong>Add or subtract</strong> only when the denominators match: find the lowest common denominator, convert both, then work on the numerators. <strong>Multiply</strong> straight across, cancelling common factors first to keep the numbers small. <strong>Divide</strong> with KFC: Keep the first fraction, Flip the second, Change ÷ to ×. Turn any <strong>mixed number</strong> into an improper fraction before you start, and simplify your answer by dividing top and bottom by their highest common factor.</p>",
 "example": "<p><strong>Calculate</strong> \\(\\frac{2}{3} + \\frac{3}{4}\\)</p><p><strong>Step 1:</strong> LCD of 3 and 4 is 12</p><p><strong>Step 2:</strong> \\(\\frac{2}{3} = \\frac{8}{12}\\) and \\(\\frac{3}{4} = \\frac{9}{12}\\)</p><p><strong>Step 3:</strong> \\(\\frac{8}{12} + \\frac{9}{12} = \\frac{17}{12}\\)</p><p><strong>Step 4:</strong> \\(\\frac{17}{12} = 1\\frac{5}{12}\\) (already in simplest form)</p>"
}

# Clean em dashes in preserved worked_examples labels (ship-gate style rule)
for we in pd.get("worked_examples", []):
    for s in we.get("steps", []):
        if isinstance(s.get("label"), str):
            s["label"] = s["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, io.open("lesson_maths-ocr_number-L02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("built lesson_maths-ocr_number-L02.json; top keys:", sorted(pd.keys()))
