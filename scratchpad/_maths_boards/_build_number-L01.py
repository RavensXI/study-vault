# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_maths_boards/_live_number-L01.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s): return {"say": s}

def mc(pattern, expect, message, note="expect derived by committing the error"):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

# ---------------- problem bank ----------------
bronze = [
 {"display": "\\(6 + 4 \\times 3\\)", "solutions": [18], "calculator": False, "input_type": "single_value",
  "hint": "Do the multiplication before the addition.",
  "misconceptions": [mc("left_to_right", 30, "Multiplication comes first: 4 × 3 = 12, then 6 + 12 = 18. Adding 6 + 4 first gives 30, which ignores the order.")],
  "guided_steps": [
    sayonly("No brackets or powers. Multiplication comes before addition, so clear the × first."),
    box("4 × 3 = ", 12, "Just multiply 4 and 3."),
    box("6 + 12 = ", 18, "Add the 6 onto your 12.", phase="substitute"),
    box("Read it back, 6 + 4 × 3 is 6 + 12 = ", 18, "It should match your last line.", done="The × was done before the +, so 18 is right.")]},

 {"display": "\\(20 - 8 \\div 2\\)", "solutions": [16], "calculator": False, "input_type": "single_value",
  "hint": "Do the division before the subtraction.",
  "misconceptions": [mc("left_to_right", 6, "Divide first: 8 ÷ 2 = 4, then 20 − 4 = 16. Doing 20 − 8 first gives 6.")],
  "guided_steps": [
    sayonly("Division comes before subtraction, so do the ÷ first."),
    box("8 ÷ 2 = ", 4, "Halve the 8."),
    box("20 − 4 = ", 16, "Take the 4 from 20.", phase="substitute"),
    box("Read it back, 20 − 8 ÷ 2 is 20 − 4 = ", 16, "It should match.", done="The ÷ was cleared before the −.")]},

 {"display": "\\(5 \\times 3 + 7 \\times 2\\)", "solutions": [29], "calculator": False, "input_type": "single_value",
  "hint": "Work out both multiplications, then add.",
  "misconceptions": [mc("chain_left_to_right", 44, "Both multiplications come before the addition: 5 × 3 = 15 and 7 × 2 = 14, then 15 + 14 = 29. Working straight left to right gives 44.")],
  "guided_steps": [
    sayonly("Two multiplications and one addition. Clear BOTH multiplications before adding."),
    box("5 × 3 = ", 15, "Multiply 5 by 3."),
    box("7 × 2 = ", 14, "Multiply 7 by 2."),
    box("15 + 14 = ", 29, "Add your two products.", phase="substitute"),
    box("Read it back: the products are 15 and 14, total = ", 29, "It should match.", done="Both × were done before the +.")]},

 {"display": "\\(24 \\div 6 + 2 \\times 5\\)", "solutions": [14], "calculator": False, "input_type": "single_value",
  "hint": "Do the division and the multiplication, then add.",
  "misconceptions": [mc("chain_left_to_right", 30, "Do 24 ÷ 6 = 4 and 2 × 5 = 10 first, then 4 + 10 = 14. Straight left to right gives 30.")],
  "guided_steps": [
    sayonly("Do the ÷ and the × before the +."),
    box("24 ÷ 6 = ", 4, "Divide 24 by 6."),
    box("2 × 5 = ", 10, "Multiply 2 by 5."),
    box("4 + 10 = ", 14, "Add the two results.", phase="substitute"),
    box("Read it back: 4 plus 10 = ", 14, "It should match.", done="Both high priority operations were cleared first.")]},

 {"display": "\\(3 + 5 \\times 4 - 2\\)", "solutions": [21], "calculator": False, "input_type": "single_value",
  "hint": "Multiply first, then work left to right.",
  "misconceptions": [mc("left_to_right", 30, "Multiply first: 5 × 4 = 20, then 3 + 20 − 2 = 21. Adding 3 + 5 first gives 30.")],
  "guided_steps": [
    sayonly("One multiplication sits in the middle. Clear it, then work + and − left to right."),
    box("5 × 4 = ", 20, "Multiply 5 by 4."),
    box("3 + 20 = ", 23, "Add from the left first.", phase="substitute"),
    box("23 − 2 = ", 21, "Now subtract the 2."),
    box("Read it back: 3 + 20 − 2 = ", 21, "It should match.", done="The × went first, then + and − left to right.")]},

 {"display": "\\(18 \\div 2 \\times 3\\)", "solutions": [27], "calculator": False, "input_type": "single_value",
  "hint": "Divide and multiply have equal priority, so go left to right.",
  "misconceptions": [mc("multiply_first", 3, "Division and multiplication are equal priority, so go left to right: 18 ÷ 2 = 9, then 9 × 3 = 27. Doing 2 × 3 first gives 3.")],
  "guided_steps": [
    sayonly("Division and multiplication have equal priority. Work strictly left to right, so the ÷ comes first here."),
    box("18 ÷ 2 = ", 9, "Leftmost operation first: divide 18 by 2."),
    box("9 × 3 = ", 27, "Now multiply your 9 by 3.", phase="substitute"),
    box("Read it back: 18 ÷ 2 = 9, then × 3 = ", 27, "It should match.", done="Left to right, not multiply first.")]},

 {"display": "\\(40 - 5 \\times 6 + 2\\)", "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Multiply first, then subtract and add left to right.",
  "misconceptions": [mc("add_before_subtract", 8, "After 5 × 6 = 30, work left to right: 40 − 30 = 10, then + 2 = 12. Adding 30 + 2 first gives 8.")],
  "guided_steps": [
    sayonly("Clear the × first, then work − and + left to right."),
    box("5 × 6 = ", 30, "Multiply 5 by 6."),
    box("40 − 30 = ", 10, "Subtract from the left first.", phase="substitute"),
    box("10 + 2 = ", 12, "Now add the 2."),
    box("Read it back: 40 − 30 + 2 = ", 12, "It should match.", done="Left to right stops you subtracting 32 by mistake.")]},

 {"display": "\\(7 + 3 \\times 8 \\div 4\\)", "solutions": [13], "calculator": False, "input_type": "single_value",
  "hint": "Clear the multiply and divide left to right, then add.",
  "misconceptions": [mc("add_first", 20, "Clear the × and ÷ first: 3 × 8 = 24, 24 ÷ 4 = 6, then 7 + 6 = 13. Adding 7 + 3 first gives 20.")],
  "guided_steps": [
    sayonly("Clear the × and ÷ (left to right) before adding."),
    box("3 × 8 = ", 24, "Multiply 3 by 8 first, it is leftmost."),
    box("24 ÷ 4 = ", 6, "Now divide by 4."),
    box("7 + 6 = ", 13, "Add the 7.", phase="substitute"),
    box("Read it back: 7 + 6 = ", 13, "It should match.", done="× and ÷ cleared left to right, then +.")]},
]

silver = [
 {"display": "\\((3 + 5) \\times 4\\)", "solutions": [32], "calculator": False, "input_type": "single_value",
  "hint": "Work inside the brackets first.",
  "misconceptions": [mc("no_bracket", 23, "Brackets first: 3 + 5 = 8, then 8 × 4 = 32. Skipping the bracket to do 5 × 4 first gives 23.")],
  "guided_steps": [
    sayonly("Brackets first, always."),
    box("3 + 5 = ", 8, "Work inside the brackets."),
    box("8 × 4 = ", 32, "Multiply your bracket by 4.", phase="substitute"),
    box("Read it back: (3 + 5) × 4 = 8 × 4 = ", 32, "It should match.", done="The bracket was done before the ×.")]},

 {"display": "\\(6 \\times (9 - 4) + 3^2\\)", "solutions": [39], "calculator": False, "input_type": "single_value",
  "hint": "Do the bracket and the power before multiplying and adding.",
  "misconceptions": [mc("index_times_two", 36, "3² means 3 × 3 = 9, not 3 × 2 = 6. With 9 the answer is 6 × 5 + 9 = 39. Using 6 gives 36.")],
  "guided_steps": [
    sayonly("Do the bracket and the power before the × and +."),
    box("9 − 4 = ", 5, "Inside the bracket."),
    box("3 squared, 3 × 3 = ", 9, "3² means 3 × 3."),
    box("6 × 5 = ", 30, "Multiply 6 by your bracket.", phase="substitute"),
    box("30 + 9 = ", 39, "Add the 9 from the power."),
    box("Read it back: 30 + 9 = ", 39, "It should match.", done="Bracket and power first, then × then +.")]},

 {"display": "\\(2^3 + 4 \\times (7 - 3)\\)", "solutions": [24], "calculator": False, "input_type": "single_value",
  "hint": "Do the bracket and the power, then multiply and add.",
  "misconceptions": [mc("index_times", 22, "2³ means 2 × 2 × 2 = 8, not 2 × 3 = 6. With 8 the answer is 8 + 16 = 24. Using 6 gives 22.")],
  "guided_steps": [
    sayonly("Bracket and power first, then the × and +."),
    box("7 − 3 = ", 4, "Inside the bracket."),
    box("2 cubed, 2 × 2 × 2 = ", 8, "2³ means three 2s multiplied."),
    box("4 × 4 = ", 16, "Multiply 4 by your bracket.", phase="substitute"),
    box("8 + 16 = ", 24, "Add the power result."),
    box("Read it back: 8 + 16 = ", 24, "It should match.", done="Power and bracket first, then × then +.")]},

 {"display": "\\(50 - (2 + 3)^2\\)", "solutions": [25], "calculator": False, "input_type": "single_value",
  "hint": "Add inside the brackets, then square the whole bracket.",
  "misconceptions": [mc("square_each", 37, "(2 + 3)² means 5² = 25, not 2² + 3² = 13. So 50 − 25 = 25. Squaring each number gives 37.")],
  "guided_steps": [
    sayonly("Work the bracket, then square it, before subtracting."),
    box("2 + 3 = ", 5, "Inside the bracket first."),
    box("5 squared, 5 × 5 = ", 25, "Square the whole bracket, not each number."),
    box("50 − 25 = ", 25, "Subtract your squared bracket from 50.", phase="substitute"),
    box("Read it back: 50 − 5² = 50 − 25 = ", 25, "It should match.", done="The bracket was squared as a whole.")]},

 {"display": "\\(3 \\times (12 - 4) \\div 6\\)", "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Brackets first, then multiply and divide left to right.",
  "misconceptions": [mc("forgot_last_step", 24, "After the bracket, 3 × 8 = 24, but do not stop there: 24 ÷ 6 = 4. Stopping at 24 misses the final division.")],
  "guided_steps": [
    sayonly("Bracket first, then × and ÷ left to right."),
    box("12 − 4 = ", 8, "Inside the bracket."),
    box("3 × 8 = ", 24, "Leftmost of × and ÷: multiply first.", phase="substitute"),
    box("24 ÷ 6 = ", 4, "Now divide by 6."),
    box("Read it back: 3 × 8 ÷ 6 = ", 4, "It should match.", done="Bracket, then left to right.")]},

 {"display": "\\(100 \\div (4 + 6) \\times 3\\)", "solutions": [30], "calculator": False, "input_type": "single_value",
  "hint": "Brackets first, then divide and multiply left to right.",
  "misconceptions": [mc("no_bracket", 43, "Brackets first: 4 + 6 = 10, then 100 ÷ 10 = 10 and 10 × 3 = 30. Splitting it as 100 ÷ 4 + 6 × 3 gives 43.")],
  "guided_steps": [
    sayonly("Bracket first, then ÷ and × left to right."),
    box("4 + 6 = ", 10, "Inside the bracket."),
    box("100 ÷ 10 = ", 10, "Leftmost of ÷ and ×: divide first.", phase="substitute"),
    box("10 × 3 = ", 30, "Now multiply by 3."),
    box("Read it back: 100 ÷ 10 × 3 = ", 30, "It should match.", done="Divide before multiply because it is on the left.")]},

 {"display": "\\(4^2 - 3 \\times (1 + 1)\\)", "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Do the bracket and the power, then multiply and subtract.",
  "misconceptions": [mc("index_times_two", 2, "4² means 4 × 4 = 16, not 4 × 2 = 8. With 16 the answer is 16 − 6 = 10. Using 8 gives 2.")],
  "guided_steps": [
    sayonly("Bracket and power first, then × and −."),
    box("1 + 1 = ", 2, "Inside the bracket."),
    box("4 squared, 4 × 4 = ", 16, "4² means 4 × 4."),
    box("3 × 2 = ", 6, "Multiply 3 by your bracket.", phase="substitute"),
    box("16 − 6 = ", 10, "Subtract from the power result."),
    box("Read it back: 16 − 6 = ", 10, "It should match.", done="Power and bracket first, then × then −.")]},
]

gold = [
 {"display": "\\(\\dfrac{18 + 6}{2^2} + 5 \\times 3\\)", "solutions": [21], "calculator": False, "input_type": "single_value",
  "hint": "The fraction bar groups the top: add it up, then divide by 2².",
  "misconceptions": [mc("no_fraction_bracket", 27, "The bottom is 2² = 4, not 2. So (18 + 6) ÷ 4 = 6, then 6 + 15 = 21. Dividing by just 2 gives 12 + 15 = 27.")],
  "guided_steps": [
    sayonly("The fraction bar groups the top. Work out the whole top, then the bottom, then divide."),
    box("top: 18 + 6 = ", 24, "Add the whole numerator."),
    box("bottom: 2 squared = ", 4, "2² means 2 × 2."),
    box("24 ÷ 4 = ", 6, "Divide top by bottom."),
    box("the other term: 5 × 3 = ", 15, "Multiply 5 by 3."),
    box("6 + 15 = ", 21, "Add the fraction and the product.", phase="substitute"),
    box("Read it back: 6 + 15 = ", 21, "It should match.", done="Top and bottom were grouped before dividing.")]},

 {"display": "\\((3 + 4)^2 - 5 \\times (8 - 2)\\)", "solutions": [19], "calculator": False, "input_type": "single_value",
  "hint": "Clear both brackets and the power before subtracting.",
  "misconceptions": [mc("square_each", -5, "(3 + 4)² means 7² = 49, not 3² + 4² = 25. So 49 − 30 = 19. Squaring each number gives −5.")],
  "guided_steps": [
    sayonly("Two brackets, one power, one product. Clear the brackets and the power first."),
    box("first bracket: 3 + 4 = ", 7, "Add inside the first bracket."),
    box("second bracket: 8 − 2 = ", 6, "Subtract inside the second bracket."),
    box("7 squared, 7 × 7 = ", 49, "Square the first bracket."),
    box("5 × 6 = ", 30, "Multiply 5 by the second bracket."),
    box("49 − 30 = ", 19, "Subtract the product from the square.", phase="substitute"),
    box("Read it back: 49 − 30 = ", 19, "It should match.", done="Brackets and power cleared first.")]},

 {"display": "\\(5 \\times 6 \\div 3 + 4 \\times (2 + 1)^2\\)", "solutions": [46], "calculator": False, "input_type": "single_value",
  "hint": "Bracket and power first, then each multiply and divide chain, then add.",
  "misconceptions": [mc("index_dropped", 22, "Do not forget the power: (2 + 1)² = 3² = 9, not 3. With 9, 4 × 9 = 36 and 10 + 36 = 46. Using 3 gives 22.")],
  "guided_steps": [
    sayonly("Bracket and power first, then handle each × and ÷ chain, then add."),
    box("bracket: 2 + 1 = ", 3, "Inside the bracket."),
    box("3 squared, 3 × 3 = ", 9, "Square the bracket."),
    box("left chain: 5 × 6 = ", 30, "Start the left chain, leftmost first."),
    box("30 ÷ 3 = ", 10, "Now divide by 3."),
    box("4 × 9 = ", 36, "Multiply 4 by the squared bracket."),
    box("10 + 36 = ", 46, "Add your two results.", phase="substitute"),
    box("Read it back: 10 + 36 = ", 46, "It should match.", done="Each × ÷ chain done left to right, then +.")]},

 {"display": "\\(2^4 - (3 \\times 2 + 1)^0 \\times 8\\)", "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Any non-zero number to the power 0 is 1.",
  "misconceptions": [mc("zero_power", 16, "Any non-zero number to the power 0 is 1, not 0. So 7⁰ = 1 and 1 × 8 = 8, giving 16 − 8 = 8. Treating 7⁰ as 0 gives 16.")],
  "guided_steps": [
    sayonly("Work the bracket, then the powers, then the × and −."),
    box("inside the bracket: 3 × 2 + 1 = ", 7, "Multiply 3 by 2, then add 1."),
    box("2 to the power 4, 2 × 2 × 2 × 2 = ", 16, "Four 2s multiplied."),
    box("7 to the power 0 = ", 1, "Any non-zero number to the power 0 is 1."),
    box("1 × 8 = ", 8, "Multiply your power result by 8."),
    box("16 − 8 = ", 8, "Subtract from 2⁴.", phase="substitute"),
    box("Read it back: 16 − 8 = ", 8, "It should match.", done="7⁰ = 1 was the trap.")]},

 {"display": "\\(\\dfrac{(5-2)^3 + 3}{2 \\times 5}\\)", "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Finish the whole top and the whole bottom, then divide.",
  "misconceptions": [mc("no_fraction_bracket", 27.3, "The fraction bar groups the whole top: (27 + 3) = 30, then ÷ (2 × 5) = 10, giving 3. Dividing only the 3 by 10 gives 27.3.")],
  "guided_steps": [
    sayonly("The fraction bar groups top and bottom. Build the whole top, then the whole bottom, then divide."),
    box("inside the top bracket: 5 − 2 = ", 3, "Subtract inside the bracket."),
    box("3 cubed, 3 × 3 × 3 = ", 27, "Three 3s multiplied."),
    box("top total: 27 + 3 = ", 30, "Finish the numerator by adding 3."),
    box("bottom: 2 × 5 = ", 10, "Multiply the denominator."),
    box("30 ÷ 10 = ", 3, "Divide top by bottom.", phase="substitute"),
    box("Read it back: 30 ÷ 10 = ", 3, "It should match.", done="Top and bottom each finished before dividing.")]},
]

# ---------------- guided (opener + teach) ----------------
guided = {
 "opener": {
   "label": "Before any rules",
   "display": "You have a £5 note.<br>You also buy 3 chocolate bars costing £2 each.",
   "steps": [
     box("3 bars at £2 each = £", 6, "Three lots of £2."),
     box("Add your £5 note. Altogether = £", 11, "£6 of chocolate plus the £5 note."),
     sayonly("You worked out the chocolate (3 × 2 = 6) before adding the £5, without being told to. Written down, the bill is \\(5 + 3 \\times 2\\). Read blindly left to right that would be 5 + 3 = 8, then × 2 = 16, which is wrong. Your instinct to multiply first IS the rule: <strong>multiplication before addition</strong>. BIDMAS just lists the full running order: Brackets, Indices, Divide and Multiply, Add and Subtract.")]
 },
 "teach": {
   "bronze": {
     "display": "Work out \\(12 \\div 4 \\times 2 + 5\\)",
     "label": "Together: your first one",
     "steps": [
       sayonly("No brackets or powers. Do the ÷ and × first, left to right, then the +."),
       box("12 ÷ 4 = ", 3, "Leftmost operation first: divide 12 by 4."),
       box("3 × 2 = ", 6, "Now multiply your 3 by 2."),
       box("6 + 5 = ", 11, "Add the 5 last."),
       box("Read it back: 12 ÷ 4 × 2 + 5 = ", 11, "It should match.", done="÷ and × cleared left to right before the +. That was the whole point.")]
   },
   "silver": {
     "display": "Work out \\((6 + 2) \\times 3 - 4^2\\)",
     "label": "Together: the silver move",
     "steps": [
       sayonly("Now a bracket and a power appear. Both come before the × and −."),
       box("bracket: 6 + 2 = ", 8, "Work inside the bracket first."),
       box("4 squared, 4 × 4 = ", 16, "4² means 4 × 4, not 4 × 2."),
       box("8 × 3 = ", 24, "Multiply your bracket by 3."),
       box("24 − 16 = ", 8, "Subtract the squared term."),
       box("Read it back: 8 × 3 − 16 = ", 8, "It should match.", done="Bracket and power went first. Gone before any × or −.")]
   },
   "gold": {
     "display": "Work out \\(\\dfrac{(4 + 2)^2}{3} - 2 \\times 5\\)",
     "label": "Together: the gold move",
     "steps": [
       sayonly("The fraction bar groups the top. Build the whole top, then divide, then finish."),
       box("top bracket: 4 + 2 = ", 6, "Inside the bracket first."),
       box("6 squared, 6 × 6 = ", 36, "Square the whole bracket."),
       box("36 ÷ 3 = ", 12, "Divide the top by the bottom, 3."),
       box("2 × 5 = ", 10, "The other term: multiply 2 by 5."),
       box("12 − 10 = ", 2, "Subtract the product."),
       box("Read it back: 12 − 10 = ", 2, "It should match.", done="Top of the fraction grouped before dividing. That is the gold move.")]
   }
 }
}

# ---------------- tier_guides ----------------
tier_guides = {
 "bronze": {
   "title": "Bronze: multiply and divide before add and subtract",
   "steps": [
     "No brackets or powers here. Do all the × and ÷ first, then the + and −.",
     "× and ÷ share one level: when both appear, work left to right. The same goes for + and −.",
     "A common slip is going straight left to right. Always clear the × and ÷ before touching + or −."],
   "example": {
     "question": "Work out \\(9 + 12 \\div 4\\)",
     "steps": [
       {"label": "Divide", "content": "<p>\\(12 \\div 4 = 3\\), so it becomes \\(9 + 3\\).</p>"},
       {"label": "Add", "content": "<p>\\(9 + 3 = 12\\)</p>"},
       {"label": "Check", "content": "<p>The ÷ was done before the +, so 12 is right.</p>"},
       {"label": "Answer", "content": "<p>\\(12\\)</p>", "isAnswer": True, "is_answer": True}]
   }
 },
 "silver": {
   "title": "Silver: brackets and powers come first",
   "steps": [
     "Now brackets and powers appear. Work out anything inside brackets first.",
     "Then powers: remember \\(3^2\\) means 3 × 3 = 9, not 3 × 2.",
     "After brackets and powers, finish with × and ÷, then + and −, left to right."],
   "example": {
     "question": "Work out \\(50 - (2 + 3)^2\\)",
     "steps": [
       {"label": "Bracket", "content": "<p>\\(2 + 3 = 5\\)</p>"},
       {"label": "Power", "content": "<p>\\(5^2 = 25\\), the whole bracket squared.</p>"},
       {"label": "Subtract", "content": "<p>\\(50 - 25 = 25\\)</p>"},
       {"label": "Answer", "content": "<p>\\(25\\)</p>", "isAnswer": True, "is_answer": True}]
   }
 },
 "gold": {
   "title": "Gold: fraction bars group the top and bottom",
   "steps": [
     "A fraction bar acts like brackets: work out the whole top line and the whole bottom line, then divide.",
     "Inside each, follow the usual order: brackets, powers, then × and ÷, then + and −.",
     "Powers of 0 catch people out: any non-zero number to the power 0 is 1."],
   "example": {
     "question": "Work out \\(\\dfrac{18 + 6}{2^2}\\)",
     "steps": [
       {"label": "Top", "content": "<p>\\(18 + 6 = 24\\)</p>"},
       {"label": "Bottom", "content": "<p>\\(2^2 = 4\\)</p>"},
       {"label": "Divide", "content": "<p>\\(24 \\div 4 = 6\\)</p>"},
       {"label": "Answer", "content": "<p>\\(6\\)</p>", "isAnswer": True, "is_answer": True}]
   }
 }
}

# ---------------- method_card (slim) ----------------
method_card = {
 "title": "How to Use BIDMAS (Order of Operations)",
 "steps": [
   "Brackets first (innermost pair outward).",
   "Then Indices: powers and roots.",
   "Then Division and Multiplication, left to right.",
   "Then Addition and Subtraction, left to right."],
 "content": "<p><strong>BIDMAS</strong> gives the order to work in: <strong>B</strong>rackets, <strong>I</strong>ndices, <strong>D</strong>ivision and <strong>M</strong>ultiplication, <strong>A</strong>ddition and <strong>S</strong>ubtraction.</p><p>Division and multiplication share one level: do them left to right, not multiplication first. Addition and subtraction share the next level, also left to right.</p><p>A fraction bar groups its top and bottom like brackets: evaluate each fully, then divide.</p>",
 "example": "<p><strong>Calculate</strong> \\(5 + 3 \\times 2^2\\)</p><p>Indices: \\(2^2 = 4\\). Multiply: \\(3 \\times 4 = 12\\). Add: \\(5 + 12 = 17\\).</p>"
}

# ---- fix preserved em dashes (style rule enforced everywhere) ----
we = live.get("worked_examples", [])
def dedash(o):
    if isinstance(o, dict): return {k: dedash(v) for k, v in o.items()}
    if isinstance(o, list): return [dedash(v) for v in o]
    if isinstance(o, str): return o.replace(" — ", ": ").replace("—", ", ")
    return o
we = dedash(we)

# ---------------- assemble ----------------
pd = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": {
   "bronze_description": "Multiply and divide before you add and subtract; work left to right within each pair.",
   "silver_description": "Brackets and powers first, then the multiply and divide, then add and subtract, left to right.",
   "gold_description": "Multi step calculations with fraction bars, nested brackets and powers, including the power of 0.",
   "bronze": bronze, "silver": silver, "gold": gold
 },
 "related_videos": live.get("related_videos", []),
 "worked_examples": we,
 "tier_guides": tier_guides,
 "guided": guided
}

json.dump(pd, io.open("_maths_boards/lesson_number-L01.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written")
