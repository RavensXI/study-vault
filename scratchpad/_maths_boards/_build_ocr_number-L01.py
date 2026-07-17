# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d

def say(s):
    return {"say": s}

def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect,
            "message": message, "note": "expect derived by committing the error"}

# ---- BRONZE ----
bronze = [
 {"display": "\\(3 + 5 \\times 2\\)", "solutions": [13], "calculator": False,
  "input_type": "single_value",
  "hint": "Do the multiplication before the addition.",
  "misconceptions": [mc("left_to_right", 16,
    "Multiplication comes first: 5 × 2 = 10, then 3 + 10 = 13. Adding 3 + 5 first gives 16, which ignores the order.")],
  "guided_steps": [
    say("No brackets or powers. Multiplication comes before addition, so clear the × first."),
    box("5 × 2 = ", 10, "Multiply 5 by 2."),
    box("3 + 10 = ", 13, "Add the 3 onto your 10.", phase="substitute"),
    box("Read it back, 3 + 5 × 2 is 3 + 10 = ", 13, "It should match your last line.",
        done="The × was done before the +, so 13 is right.")]},

 {"display": "\\(20 - 4 \\times 3\\)", "solutions": [8], "calculator": False,
  "input_type": "single_value",
  "hint": "Do the multiplication before the subtraction.",
  "misconceptions": [mc("left_to_right", 48,
    "Multiply first: 4 × 3 = 12, then 20 − 12 = 8. Doing 20 − 4 first, then × 3, gives 48.")],
  "guided_steps": [
    say("Multiplication comes before subtraction, so do the × first."),
    box("4 × 3 = ", 12, "Multiply 4 by 3."),
    box("20 − 12 = ", 8, "Take 12 from 20.", phase="substitute"),
    box("Read it back, 20 − 4 × 3 is 20 − 12 = ", 8, "It should match.",
        done="The × was cleared before the −.")]},

 {"display": "\\(6 + 12 \\div 4\\)", "solutions": [9], "calculator": False,
  "input_type": "single_value",
  "hint": "Do the division before the addition.",
  "misconceptions": [mc("left_to_right", 4.5,
    "Divide first: 12 ÷ 4 = 3, then 6 + 3 = 9. Adding 6 + 12 first, then ÷ 4, gives 4.5.")],
  "guided_steps": [
    say("Division comes before addition, so do the ÷ first."),
    box("12 ÷ 4 = ", 3, "Divide 12 by 4."),
    box("6 + 3 = ", 9, "Add the 6.", phase="substitute"),
    box("Read it back, 6 + 12 ÷ 4 is 6 + 3 = ", 9, "It should match.",
        done="The ÷ was done before the +.")]},

 {"display": "\\(8 \\times 3 - 10\\)", "solutions": [14], "calculator": False,
  "input_type": "single_value",
  "hint": "Multiply first, then subtract in the order written.",
  "misconceptions": [mc("reverse_subtraction", -14,
    "Subtract in the order written: 8 × 3 = 24, then 24 − 10 = 14. Doing 10 − 24 gives −14.")],
  "guided_steps": [
    say("Multiplication comes before subtraction. Clear the × first, then subtract in the order written."),
    box("8 × 3 = ", 24, "Multiply 8 by 3."),
    box("24 − 10 = ", 14, "Take 10 from 24, in that order.", phase="substitute"),
    box("Read it back, 8 × 3 − 10 is 24 − 10 = ", 14, "It should match.",
        done="24 − 10 = 14, not 10 − 24.")]},

 {"display": "\\(15 \\div 3 + 4 \\times 3\\)", "solutions": [17], "calculator": False,
  "input_type": "single_value",
  "hint": "Do the division and the multiplication, then add.",
  "misconceptions": [mc("left_to_right", 27,
    "Do 15 ÷ 3 = 5 and 4 × 3 = 12 first, then 5 + 12 = 17. Working straight left to right gives 27.")],
  "guided_steps": [
    say("Two high priority operations, one ÷ and one ×. Clear BOTH before adding."),
    box("15 ÷ 3 = ", 5, "Divide 15 by 3."),
    box("4 × 3 = ", 12, "Multiply 4 by 3."),
    box("5 + 12 = ", 17, "Add your two results.", phase="substitute"),
    box("Read it back: 5 + 12 = ", 17, "It should match.",
        done="Both × and ÷ were done before the +.")]},

 {"display": "\\(2 \\times 7 + 3 \\times 4\\)", "solutions": [26], "calculator": False,
  "input_type": "single_value",
  "hint": "Work out both multiplications, then add.",
  "misconceptions": [mc("chain_left_to_right", 68,
    "Both multiplications come before the addition: 2 × 7 = 14 and 3 × 4 = 12, then 14 + 12 = 26. Working straight left to right gives 68.")],
  "guided_steps": [
    say("Two multiplications and one addition. Clear BOTH multiplications before adding."),
    box("2 × 7 = ", 14, "Multiply 2 by 7."),
    box("3 × 4 = ", 12, "Multiply 3 by 4."),
    box("14 + 12 = ", 26, "Add your two products.", phase="substitute"),
    box("Read it back: 14 + 12 = ", 26, "It should match.",
        done="Both × were done before the +.")]},

 {"display": "\\(30 - 5 \\times 4 + 1\\)", "solutions": [11], "calculator": False,
  "input_type": "single_value",
  "hint": "Multiply first, then subtract and add left to right.",
  "misconceptions": [mc("left_to_right", 101,
    "Clear the × first: 5 × 4 = 20, then 30 − 20 + 1 = 11. Working straight left to right gives 101.")],
  "guided_steps": [
    say("One multiplication in the middle. Clear it, then work − and + left to right."),
    box("5 × 4 = ", 20, "Multiply 5 by 4."),
    box("30 − 20 = ", 10, "Subtract from the left first.", phase="substitute"),
    box("10 + 1 = ", 11, "Now add the 1."),
    box("Read it back: 30 − 20 + 1 = ", 11, "It should match.",
        done="Left to right stops you subtracting 21 by mistake.")]},

 {"display": "\\(48 \\div 6 \\div 2\\)", "solutions": [4], "calculator": False,
  "input_type": "single_value",
  "hint": "Two divisions have equal priority, so go left to right.",
  "misconceptions": [mc("right_to_left", 16,
    "Two divisions are equal priority, so go left to right: 48 ÷ 6 = 8, then 8 ÷ 2 = 4. Doing 6 ÷ 2 first gives 48 ÷ 3 = 16.")],
  "guided_steps": [
    say("Two divisions. They are equal priority, so work strictly left to right."),
    box("48 ÷ 6 = ", 8, "Leftmost first: divide 48 by 6."),
    box("8 ÷ 2 = ", 4, "Now divide your 8 by 2.", phase="substitute"),
    box("Read it back: 48 ÷ 6 ÷ 2 is 8 ÷ 2 = ", 4, "It should match.",
        done="Left to right, not 6 ÷ 2 first.")]},
]

# ---- SILVER ----
silver = [
 {"display": "\\((3 + 5) \\times 4\\)", "solutions": [32], "calculator": False,
  "input_type": "single_value",
  "hint": "Work inside the brackets first.",
  "misconceptions": [mc("ignore_brackets", 23,
    "Brackets first: 3 + 5 = 8, then 8 × 4 = 32. Skipping the bracket to do 5 × 4 first gives 23.")],
  "guided_steps": [
    say("Brackets first, always."),
    box("3 + 5 = ", 8, "Work inside the bracket."),
    box("8 × 4 = ", 32, "Multiply your bracket by 4.", phase="substitute"),
    box("Read it back: (3 + 5) × 4 = 8 × 4 = ", 32, "It should match.",
        done="The bracket was done before the ×.")]},

 {"display": "\\(5 \\times (12 - 4) + 6\\)", "solutions": [46], "calculator": False,
  "input_type": "single_value",
  "hint": "Brackets first, then multiply, then add.",
  "misconceptions": [mc("ignore_brackets", 62,
    "Brackets first: 12 − 4 = 8, then 5 × 8 = 40, then 40 + 6 = 46. Ignoring the bracket to read 5 × 12 − 4 + 6 gives 62.")],
  "guided_steps": [
    say("Bracket first, then multiply, then add."),
    box("12 − 4 = ", 8, "Inside the bracket."),
    box("5 × 8 = ", 40, "Multiply 5 by your bracket."),
    box("40 + 6 = ", 46, "Add the 6.", phase="substitute"),
    box("Read it back: 40 + 6 = ", 46, "It should match.",
        done="Bracket, then ×, then +.")]},

 {"display": "\\(2^3 + 5 \\times 3\\)", "solutions": [23], "calculator": False,
  "input_type": "single_value",
  "hint": "Do the power and the multiplication before the addition.",
  "misconceptions": [mc("index_as_product", 21,
    "2³ means 2 × 2 × 2 = 8, not 2 × 3 = 6. With 8 the answer is 8 + 15 = 23. Using 6 gives 21.")],
  "guided_steps": [
    say("Do the power and the multiplication before the addition."),
    box("2 cubed, 2 × 2 × 2 = ", 8, "2³ means three 2s multiplied."),
    box("5 × 3 = ", 15, "Multiply 5 by 3."),
    box("8 + 15 = ", 23, "Add your two results.", phase="substitute"),
    box("Read it back: 8 + 15 = ", 23, "It should match.",
        done="Power and × first, then +.")]},

 {"display": "\\(100 \\div (4 + 6) \\times 3\\)", "solutions": [30], "calculator": False,
  "input_type": "single_value",
  "hint": "Brackets first, then divide and multiply left to right.",
  "misconceptions": [mc("ignore_brackets", 43,
    "Brackets first: 4 + 6 = 10, then 100 ÷ 10 = 10 and 10 × 3 = 30. Splitting it as 100 ÷ 4 + 6 × 3 gives 43.")],
  "guided_steps": [
    say("Bracket first, then ÷ and × left to right."),
    box("4 + 6 = ", 10, "Inside the bracket."),
    box("100 ÷ 10 = ", 10, "Leftmost of ÷ and ×: divide first.", phase="substitute"),
    box("10 × 3 = ", 30, "Now multiply by 3."),
    box("Read it back: 100 ÷ 10 × 3 = ", 30, "It should match.",
        done="Divide before multiply because it is on the left.")]},

 {"display": "\\(3 \\times 4^2 - 20\\)", "solutions": [28], "calculator": False,
  "input_type": "single_value",
  "hint": "Do the power first, then multiply, then subtract.",
  "misconceptions": [mc("square_the_product", 124,
    "The index applies only to the 4, not to 3 × 4. So 4² = 16, then 3 × 16 = 48, then 48 − 20 = 28. Squaring 3 × 4 as 12² gives 124.")],
  "guided_steps": [
    say("The power sits on the 4 only. Do it first, then multiply, then subtract."),
    box("4 squared, 4 × 4 = ", 16, "4² means 4 × 4, not 4 × 2."),
    box("3 × 16 = ", 48, "Multiply 3 by 16. The power was only on the 4."),
    box("48 − 20 = ", 28, "Take 20 from 48.", phase="substitute"),
    box("Read it back: 48 − 20 = ", 28, "It should match.",
        done="The index was on the 4 alone, then × then −.")]},

 {"display": "\\((7 - 3)^2 + 8\\)", "solutions": [24], "calculator": False,
  "input_type": "single_value",
  "hint": "Work inside the brackets, then square the whole bracket, then add.",
  "misconceptions": [mc("square_each_term", 48,
    "(7 − 3)² means 4² = 16, not 7² − 3² = 40. So the answer is 16 + 8 = 24. Squaring each number gives 40 + 8 = 48.")],
  "guided_steps": [
    say("Bracket first, then square the whole bracket, then add."),
    box("7 − 3 = ", 4, "Inside the bracket first."),
    box("4 squared, 4 × 4 = ", 16, "Square the whole bracket, not each number."),
    box("16 + 8 = ", 24, "Add the 8.", phase="substitute"),
    box("Read it back: 16 + 8 = ", 24, "It should match.",
        done="The bracket was squared as a whole, then +.")]},

 {"display": "\\(60 - 2 \\times (3^2 + 1)\\)", "solutions": [40], "calculator": False,
  "input_type": "single_value",
  "hint": "Finish the bracket (power then add), then multiply, then subtract.",
  "misconceptions": [mc("index_as_product", 46,
    "3² means 3 × 3 = 9, not 3 × 2 = 6. With 9 the bracket is 10, so 60 − 2 × 10 = 40. Using 6 gives a bracket of 7 and 60 − 14 = 46.")],
  "guided_steps": [
    say("Work inside the bracket first (its power, then its add), then multiply, then subtract."),
    box("3 squared, 3 × 3 = ", 9, "3² means 3 × 3, not 3 × 2."),
    box("9 + 1 = ", 10, "Finish the bracket by adding 1."),
    box("2 × 10 = ", 20, "Multiply 2 by your bracket."),
    box("60 − 20 = ", 40, "Take 20 from 60.", phase="substitute"),
    box("Read it back: 60 − 20 = ", 40, "It should match.",
        done="Bracket (power then add) first, then × then −.")]},
]

# ---- GOLD ----
gold = [
 {"display": "\\(\\frac{6^2 - 12}{2 \\times 3}\\)", "solutions": [4], "calculator": False,
  "input_type": "single_value",
  "hint": "The fraction bar groups the top and the bottom: finish each, then divide.",
  "misconceptions": [mc("fraction_not_grouped", 18,
    "The bar groups the top and bottom: (36 − 12) ÷ (2 × 3) = 24 ÷ 6 = 4. Reading it inline as 6² − 12 ÷ 2 × 3 gives 36 − 18 = 18.")],
  "guided_steps": [
    say("The fraction bar groups the top and the bottom. Finish each, then divide."),
    box("top: 6 squared, 6 × 6 = ", 36, "Square the 6 first."),
    box("top: 36 − 12 = ", 24, "Finish the numerator."),
    box("bottom: 2 × 3 = ", 6, "Multiply the denominator."),
    box("24 ÷ 6 = ", 4, "Divide top by bottom.", phase="substitute"),
    box("Read it back: 24 ÷ 6 = ", 4, "It should match.",
        done="Top and bottom were grouped before dividing.")]},

 {"display": "\\(5 + \\frac{(8-2)^2}{9}\\)", "solutions": [9], "calculator": False,
  "input_type": "single_value",
  "hint": "Build the fraction fully (bracket, power, divide), then add the 5.",
  "misconceptions": [mc("partial_answer", 4,
    "You found the fraction: (8 − 2)² = 36, then 36 ÷ 9 = 4. Do not stop there: add the 5 to get 5 + 4 = 9. Stopping at 4 misses the final addition.")],
  "guided_steps": [
    say("Build the fraction first (bracket, then power, then divide), then add the 5."),
    box("bracket: 8 − 2 = ", 6, "Inside the bracket."),
    box("6 squared, 6 × 6 = ", 36, "Square the bracket."),
    box("36 ÷ 9 = ", 4, "Divide by 9."),
    box("5 + 4 = ", 9, "Add the 5.", phase="substitute"),
    box("Read it back: 5 + 4 = ", 9, "It should match.",
        done="The fraction was finished before adding the 5.")]},

 {"display": "\\(\\sqrt{81} + 4 \\times (2^3 - 3)\\)", "solutions": [29], "calculator": False,
  "input_type": "single_value",
  "hint": "Work the root and the bracket (its power first), then multiply, then add.",
  "misconceptions": [mc("index_as_product", 21,
    "2³ means 2 × 2 × 2 = 8, not 2 × 3 = 6. With 8 the bracket is 5, so 9 + 4 × 5 = 29. Using 6 gives a bracket of 3 and 9 + 12 = 21.")],
  "guided_steps": [
    say("Work the root, the bracket (its power first), then the multiply, then the add."),
    box("√81 = ", 9, "What number times itself is 81?"),
    box("2 cubed, 2 × 2 × 2 = ", 8, "2³ means three 2s multiplied."),
    box("bracket: 8 − 3 = ", 5, "Finish the bracket."),
    box("4 × 5 = ", 20, "Multiply 4 by your bracket."),
    box("9 + 20 = ", 29, "Add the root.", phase="substitute"),
    box("Read it back: 9 + 20 = ", 29, "It should match.",
        done="Root, power, bracket, ×, then +.")]},

 {"display": "\\(\\frac{(3+5)^2}{4} - 2^3\\)", "solutions": [8], "calculator": False,
  "input_type": "single_value",
  "hint": "Finish the fraction (bracket, power, divide), work the other power, then subtract.",
  "misconceptions": [mc("index_as_product", 10,
    "2³ means 2 × 2 × 2 = 8, not 2 × 3 = 6. The fraction is 8² ÷ 4 = 16, so 16 − 8 = 8. Using 6 for 2³ gives 16 − 6 = 10.")],
  "guided_steps": [
    say("Finish the fraction (bracket, power, divide), work the other power, then subtract."),
    box("bracket: 3 + 5 = ", 8, "Inside the top bracket."),
    box("8 squared, 8 × 8 = ", 64, "Square the bracket."),
    box("64 ÷ 4 = ", 16, "Divide by 4."),
    box("2 cubed, 2 × 2 × 2 = ", 8, "2³ means three 2s multiplied."),
    box("16 − 8 = ", 8, "Subtract the 2³.", phase="substitute"),
    box("Read it back: 16 − 8 = ", 8, "It should match.",
        done="Fraction finished and 2³ found before subtracting.")]},

 {"display": "\\(2 \\times 3^2 + \\frac{40}{2^3}\\)", "solutions": [23], "calculator": False,
  "input_type": "single_value",
  "hint": "Do both powers first, then the multiply and the fraction, then add.",
  "misconceptions": [mc("square_the_product", 41,
    "3² means 3 × 3 = 9, not (2 × 3)² = 36. So 2 × 9 = 18, and 40 ÷ 2³ = 5, giving 18 + 5 = 23. Squaring 2 × 3 gives 36 + 5 = 41.")],
  "guided_steps": [
    say("Do both powers first, then the × and the fraction, then add."),
    box("3 squared, 3 × 3 = ", 9, "3² means 3 × 3. The 2 is separate."),
    box("2 × 9 = ", 18, "Multiply 2 by 9. The power was only on the 3."),
    box("2 cubed, 2 × 2 × 2 = ", 8, "The denominator: 2³."),
    box("40 ÷ 8 = ", 5, "Divide 40 by 8."),
    box("18 + 5 = ", 23, "Add your two parts.", phase="substitute"),
    box("Read it back: 18 + 5 = ", 23, "It should match.",
        done="Both powers first, then × and ÷, then +.")]},
]

# ---- worked_examples: preserve, fix em dash labels ----
worked_examples = [
 {"steps": [
    {"label": "Step 1: Multiplication first", "content": "<p>\\(3 \\times 2 = 6\\)</p>"},
    {"label": "Step 2: Addition", "content": "<p>\\(5 + 6 = 11\\)</p>"},
    {"label": "Answer", "content": "<p><strong>11</strong></p>", "isAnswer": True, "is_answer": True}],
  "question": "Calculate 5 + 3 × 2", "difficulty": "Bronze"},
 {"steps": [
    {"label": "Step 1: Brackets", "content": "<p>\\(8 + 4 = 12\\)</p>"},
    {"label": "Step 2: Division", "content": "<p>\\(12 \\div 3 = 4\\)</p>"},
    {"label": "Step 3: Addition", "content": "<p>\\(4 + 7 = 11\\)</p>"},
    {"label": "Answer", "content": "<p><strong>11</strong></p>", "isAnswer": True, "is_answer": True}],
  "question": "Calculate (8 + 4) ÷ 3 + 7", "difficulty": "Silver"},
 {"steps": [
    {"label": "Step 1: Brackets", "content": "<p>\\(10 - 8 = 2\\)</p>"},
    {"label": "Step 2: Indices", "content": "<p>\\(4^2 = 16\\)</p>"},
    {"label": "Step 3: Multiplication", "content": "<p>\\(3 \\times 2 = 6\\)</p>"},
    {"label": "Step 4: Subtraction", "content": "<p>\\(16 - 6 = 10\\)</p>"},
    {"label": "Answer", "content": "<p><strong>10</strong></p>", "isAnswer": True, "is_answer": True}],
  "question": "Calculate 4² − 3 × (10 − 8)", "difficulty": "Gold"},
]

tier_guides = {
 "bronze": {
  "title": "Bronze: multiply and divide before add and subtract",
  "steps": [
   "No brackets or powers here. Do all the × and ÷ first, then the + and −.",
   "× and ÷ share one level: when both appear, work left to right. The same goes for + and −.",
   "A common slip is going straight left to right. Always clear the × and ÷ before touching + or −."],
  "example": {"question": "Work out \\(9 + 20 \\div 5\\)", "steps": [
    {"label": "Divide", "content": "<p>\\(20 \\div 5 = 4\\), so it becomes \\(9 + 4\\).</p>"},
    {"label": "Add", "content": "<p>\\(9 + 4 = 13\\)</p>"},
    {"label": "Check", "content": "<p>The ÷ was done before the +, so 13 is right.</p>"},
    {"label": "Answer", "content": "<p>\\(13\\)</p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
  "title": "Silver: brackets and powers come first",
  "steps": [
   "Now brackets and powers appear. Work out anything inside brackets first.",
   "Then powers: remember \\(4^2\\) means 4 × 4 = 16, not 4 × 2.",
   "After brackets and powers, finish with × and ÷, then + and −, left to right."],
  "example": {"question": "Work out \\(40 - (2 + 4)^2\\)", "steps": [
    {"label": "Bracket", "content": "<p>\\(2 + 4 = 6\\)</p>"},
    {"label": "Power", "content": "<p>\\(6^2 = 36\\), the whole bracket squared.</p>"},
    {"label": "Subtract", "content": "<p>\\(40 - 36 = 4\\)</p>"},
    {"label": "Answer", "content": "<p>\\(4\\)</p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
  "title": "Gold: fraction bars and roots group before you divide",
  "steps": [
   "A fraction bar acts like brackets: finish the whole top and the whole bottom, then divide.",
   "Roots and powers count as indices: do them with the brackets, before × ÷ + −.",
   "Powers catch people out: \\(2^3\\) means 2 × 2 × 2 = 8, not 2 × 3."],
  "example": {"question": "Work out \\(\\dfrac{20 + 8}{2^2}\\)", "steps": [
    {"label": "Top", "content": "<p>\\(20 + 8 = 28\\)</p>"},
    {"label": "Bottom", "content": "<p>\\(2^2 = 4\\)</p>"},
    {"label": "Divide", "content": "<p>\\(28 \\div 4 = 7\\)</p>"},
    {"label": "Answer", "content": "<p>\\(7\\)</p>", "isAnswer": True, "is_answer": True}]}},
}

guided = {
 "opener": {
  "label": "Before any rules",
  "display": "A taxi charges a £3 flag fee to start, then £2 for every mile.<br>Your trip is 4 miles.",
  "steps": [
    box("4 miles at £2 each = £", 8, "Four lots of £2."),
    box("Add the £3 flag fee. Total fare = £", 11, "£8 of miles plus the £3 to start."),
    say("You worked out the miles (4 × 2 = 8) before adding the £3, without being told to. Written down, the fare is \\(3 + 2 \\times 4\\). Read blindly left to right that would be 3 + 2 = 5, then × 4 = 20, which is wrong. Your instinct to multiply first IS the rule: <strong>multiplication before addition</strong>. BIDMAS lists the full running order: Brackets, Indices, Divide and Multiply, Add and Subtract.")]},
 "teach": {
  "bronze": {
   "display": "Work out \\(20 \\div 4 \\times 2 + 3\\)",
   "label": "Together: your first one",
   "steps": [
     say("No brackets or powers. Do the ÷ and × first, left to right, then the +."),
     box("20 ÷ 4 = ", 5, "Leftmost operation first: divide 20 by 4."),
     box("5 × 2 = ", 10, "Now multiply your 5 by 2."),
     box("10 + 3 = ", 13, "Add the 3 last."),
     box("Read it back: 20 ÷ 4 × 2 + 3 = ", 13, "It should match.",
         done="÷ and × cleared left to right before the +. That was the whole point.")]},
  "silver": {
   "display": "Work out \\(3^2 + 2 \\times (10 - 6)\\)",
   "label": "Together: the silver move",
   "steps": [
     say("Now a bracket and a power appear. Both come before the × and +."),
     box("bracket: 10 − 6 = ", 4, "Work inside the bracket first."),
     box("3 squared, 3 × 3 = ", 9, "3² means 3 × 3, not 3 × 2."),
     box("2 × 4 = ", 8, "Multiply 2 by your bracket."),
     box("9 + 8 = ", 17, "Add the power result."),
     box("Read it back: 9 + 8 = ", 17, "It should match.",
         done="Bracket and power went first. Gone before any × or +.")]},
  "gold": {
   "display": "Work out \\(\\dfrac{(5 + 3)^2}{4} - 2 \\times 3\\)",
   "label": "Together: the gold move",
   "steps": [
     say("The fraction bar groups the top. Build the whole top, then divide, then finish."),
     box("top bracket: 5 + 3 = ", 8, "Inside the bracket first."),
     box("8 squared, 8 × 8 = ", 64, "Square the whole bracket."),
     box("64 ÷ 4 = ", 16, "Divide the top by the bottom, 4."),
     box("2 × 3 = ", 6, "The other term: multiply 2 by 3."),
     box("16 − 6 = ", 10, "Subtract the product."),
     box("Read it back: 16 − 6 = ", 10, "It should match.",
         done="Top of the fraction grouped before dividing. That is the gold move.")]},
 },
}

method_card = {
 "title": "How to Use BIDMAS (Order of Operations)",
 "steps": [
   "Brackets first (innermost pair outward).",
   "Then Indices: powers and roots.",
   "Then Division and Multiplication, left to right.",
   "Then Addition and Subtraction, left to right."],
 "content": "<p><strong>BIDMAS</strong> (also called BODMAS) gives the order to work in: <strong>B</strong>rackets, <strong>I</strong>ndices, <strong>D</strong>ivision and <strong>M</strong>ultiplication, <strong>A</strong>ddition and <strong>S</strong>ubtraction.</p><p>Division and multiplication share one level: do them left to right, not multiplication first. Addition and subtraction share the next level, also left to right.</p><p>A fraction bar groups its top and bottom like brackets: evaluate each fully, then divide. A root counts as an index.</p>",
 "example": "<p><strong>Calculate</strong> \\(5 + 3 \\times 2^2\\)</p><p>Indices: \\(2^2 = 4\\). Multiply: \\(3 \\times 4 = 12\\). Add: \\(5 + 12 = 17\\).</p>",
}

pd = {
 "method_card": method_card,
 "topic_links": {"prerequisites": []},
 "problem_bank": {
   "bronze_description": "Multiply and divide before you add and subtract; work left to right within each pair.",
   "silver_description": "Brackets and powers first, then multiply and divide, then add and subtract, left to right.",
   "gold_description": "Multi step calculations with fraction bars, roots, nested powers and brackets.",
   "bronze": bronze, "silver": silver, "gold": gold,
 },
 "related_videos": [],
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_number-L01.json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", out)
