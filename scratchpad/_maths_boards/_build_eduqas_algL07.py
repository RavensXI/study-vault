# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L07e_live.json", encoding="utf-8"))

MIN = "−"   # unicode minus
TIMES = "×"
SQ = "²"    # superscript two

def box(pre, answer, hint, post="", done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase:
        d["phase"] = "substitute"
    if done:
        d["done"] = done
    return d

def say(s):
    return {"say": s}

# ---------------- BANK ----------------
bronze = [
 { # 0  x^2+5x=0 non-zero -> -5
  "display": "Solve \\(x^2 + 5x = 0\\). Find the non-zero solution.",
  "solutions": [-5], "calculator": False, "input_type": "single_value",
  "hint": "Both terms share an x, so factorise as x(x + 5) = 0, then solve each factor.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": 5,
    "message": "x + 5 = 0 gives x = " + MIN + "5, not 5. When you move +5 to the other side it becomes negative.",
    "note": "sign-flip on the bracket root"},
   {"pattern": "gave_zero_root", "expect": 0,
    "message": "x = 0 is one root, but the question asks for the non-zero solution, which is " + MIN + "5.",
    "note": "reported the zero root"}],
  "guided_steps": [
   say("Solve \\(x^2 + 5x = 0\\). Both terms share an \\(x\\), so factorise as \\(x(x + 5) = 0\\)."),
   box("Take out x. The bracket is x + ", 5, "5x ÷ x = 5."),
   say("So \\(x(x + 5) = 0\\). Either factor can be zero."),
   box("First factor: x = ", 0, "x on its own is zero when x = 0.", phase=True),
   box("Second factor: x + 5 = 0, so x = ", -5, "Move 5 across; the sign flips.", phase=True),
   box("The non-zero solution is ", -5, "0 is one root; the other is " + MIN + "5."),
   box("Check x = " + MIN + "5: (" + MIN + "5)" + SQ + " + 5" + TIMES + "(" + MIN + "5) = ", 0,
       "25 " + MIN + " 25.", done="It gives 0, so x = " + MIN + "5 is correct.")]},
 { # 1  x^2-9=0 positive -> 3
  "display": "Solve \\(x^2 - 9 = 0\\). Find the positive solution.",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "There is no middle term, so this is a difference of two squares: (x + 3)(x - 3).",
  "misconceptions": [
   {"pattern": "gave_negative_root", "expect": -3,
    "message": MIN + "3 is also a root, but the question asks for the positive solution, which is 3.",
    "note": "picked the negative root"}],
  "guided_steps": [
   say("Solve \\(x^2 - 9 = 0\\). There is no middle term, so it is a difference of two squares, \\(x^2 - 3^2\\)."),
   box("What whole number squared gives 9? ", 3, "3 " + TIMES + " 3 = 9."),
   say("So it factorises to \\((x + 3)(x - 3) = 0\\)."),
   box("First bracket: x + 3 = 0, so x = ", -3, "Move 3 across; the sign flips.", phase=True),
   box("Second bracket: x " + MIN + " 3 = 0, so x = ", 3, "Move " + MIN + "3 across; the sign flips.", phase=True),
   box("The positive solution is ", 3, "3 is positive, " + MIN + "3 is negative."),
   box("Check x = 3: (3)" + SQ + " " + MIN + " 9 = ", 0, "9 " + MIN + " 9.",
       done="It gives 0, so x = 3 is correct.")]},
 { # 2  x^2+7x+10=0 larger -> -2
  "display": "Solve \\(x^2 + 7x + 10 = 0\\). Find the larger solution.",
  "solutions": [-2], "calculator": False, "input_type": "single_value",
  "hint": "Find two numbers that multiply to 10 and add to 7, then remember the larger of two negatives is the one closer to zero.",
  "misconceptions": [
   {"pattern": "larger_magnitude", "expect": -5,
    "message": MIN + "5 is smaller than " + MIN + "2 on the number line. The larger solution is " + MIN + "2.",
    "note": "treated bigger magnitude as larger"}],
  "guided_steps": [
   say("Solve \\(x^2 + 7x + 10 = 0\\). Two numbers multiply to 10 and add to 7: 2 and 5."),
   box("The smaller number is ", 2, "Pairs of 10: 1 and 10, 2 and 5. Which adds to 7?"),
   box("The larger number is ", 5, "7 " + MIN + " 2 = 5."),
   say("So \\((x + 2)(x + 5) = 0\\). Each bracket can be zero."),
   box("x + 2 = 0, so x = ", -2, "Move 2 across; the sign flips.", phase=True),
   box("x + 5 = 0, so x = ", -5, "Move 5 across; the sign flips.", phase=True),
   box("On the number line " + MIN + "2 is greater than " + MIN + "5, so the larger solution is ", -2,
       MIN + "2 is closer to zero than " + MIN + "5."),
   box("Check x = " + MIN + "2: (" + MIN + "2)" + SQ + " + 7" + TIMES + "(" + MIN + "2) + 10 = ", 0,
       "4 " + MIN + " 14 + 10.", done="It gives 0, so x = " + MIN + "2 is correct.")]},
 { # 3  x^2-4x=0 non-zero -> 4
  "display": "Solve \\(x^2 - 4x = 0\\). Find the non-zero solution.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Both terms share an x, so factorise as x(x - 4) = 0, then solve each factor.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": -4,
    "message": "x " + MIN + " 4 = 0 gives x = 4, not " + MIN + "4. Moving " + MIN + "4 across makes it positive.",
    "note": "sign-flip on the bracket root"},
   {"pattern": "gave_zero_root", "expect": 0,
    "message": "x = 0 is one root, but the question asks for the non-zero solution, which is 4.",
    "note": "reported the zero root"}],
  "guided_steps": [
   say("Solve \\(x^2 - 4x = 0\\). Both terms share an \\(x\\), so factorise as \\(x(x - 4) = 0\\)."),
   box("Take out x. The bracket is x " + MIN + " ", 4, "4x ÷ x = 4."),
   say("So \\(x(x - 4) = 0\\). Either factor can be zero."),
   box("First factor: x = ", 0, "x on its own is zero when x = 0.", phase=True),
   box("Second factor: x " + MIN + " 4 = 0, so x = ", 4, "Add 4 to both sides.", phase=True),
   box("The non-zero solution is ", 4, "0 is one root; the other is 4."),
   box("Check x = 4: (4)" + SQ + " " + MIN + " 4" + TIMES + "(4) = ", 0, "16 " + MIN + " 16.",
       done="It gives 0, so x = 4 is correct.")]},
 { # 4  x^2-25=0 positive -> 5  (WAS x^2-16=0 ->4, duplicate)
  "display": "Solve \\(x^2 - 25 = 0\\). Find the positive solution.",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "There is no middle term, so this is a difference of two squares: (x + 5)(x - 5).",
  "misconceptions": [
   {"pattern": "gave_negative_root", "expect": -5,
    "message": MIN + "5 is also a root, but the question asks for the positive solution, which is 5.",
    "note": "picked the negative root"}],
  "guided_steps": [
   say("Solve \\(x^2 - 25 = 0\\). No middle term, so it is a difference of two squares, \\(x^2 - 5^2\\)."),
   box("What whole number squared gives 25? ", 5, "5 " + TIMES + " 5 = 25."),
   say("So it factorises to \\((x + 5)(x - 5) = 0\\)."),
   box("First bracket: x + 5 = 0, so x = ", -5, "Move 5 across; the sign flips.", phase=True),
   box("Second bracket: x " + MIN + " 5 = 0, so x = ", 5, "Move " + MIN + "5 across; the sign flips.", phase=True),
   box("The positive solution is ", 5, "5 is positive, " + MIN + "5 is negative."),
   box("Check x = 5: (5)" + SQ + " " + MIN + " 25 = ", 0, "25 " + MIN + " 25.",
       done="It gives 0, so x = 5 is correct.")]},
 { # 5  x^2+x-6=0 positive -> 2
  "display": "Solve \\(x^2 + x - 6 = 0\\). Find the positive solution.",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Find two numbers that multiply to -6 and add to 1, watching the signs carefully.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": 3,
    "message": "Check the signs: (x + 3)(x " + MIN + " 2) = 0 gives x = " + MIN + "3 or x = 2, so the positive solution is 2, not 3.",
    "note": "flipped both signs"}],
  "guided_steps": [
   say("Solve \\(x^2 + x - 6 = 0\\). Two numbers multiply to \\(-6\\) and add to 1: that is 3 and \\(-2\\)."),
   box("The positive number is ", 3, "3 " + TIMES + " (" + MIN + "2) = " + MIN + "6 and 3 + (" + MIN + "2) = 1."),
   box("The negative number is ", -2, "The pair adds to 1, and the positive was 3."),
   say("So \\((x + 3)(x - 2) = 0\\)."),
   box("x + 3 = 0, so x = ", -3, "Move 3 across; the sign flips.", phase=True),
   box("x " + MIN + " 2 = 0, so x = ", 2, "Move " + MIN + "2 across; the sign flips.", phase=True),
   box("The positive solution is ", 2, "2 is positive, " + MIN + "3 is negative."),
   box("Check x = 2: (2)" + SQ + " + 2 " + MIN + " 6 = ", 0, "4 + 2 " + MIN + " 6.",
       done="It gives 0, so x = 2 is correct.")]},
 { # 6  x^2-6x+5=0 smaller -> 1  (WAS x^2-6x+8=0 ->2, duplicate)
  "display": "Solve \\(x^2 - 6x + 5 = 0\\). Find the smaller solution.",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "Find two numbers that multiply to 5 and add to -6; both are negative.",
  "misconceptions": [
   {"pattern": "gave_larger", "expect": 5,
    "message": "5 is the larger root; the question asks for the smaller solution, which is 1.",
    "note": "picked the larger root"}],
  "guided_steps": [
   say("Solve \\(x^2 - 6x + 5 = 0\\). Two numbers multiply to 5 and add to \\(-6\\): both negative, \\(-1\\) and \\(-5\\)."),
   box("The number closer to zero is " + MIN, 1,
       MIN + "1 " + TIMES + " (" + MIN + "5) = 5 and " + MIN + "1 + (" + MIN + "5) = " + MIN + "6.", post=""),
   say("So \\((x - 1)(x - 5) = 0\\)."),
   box("x " + MIN + " 1 = 0, so x = ", 1, "Move " + MIN + "1 across; the sign flips.", phase=True),
   box("x " + MIN + " 5 = 0, so x = ", 5, "Move " + MIN + "5 across; the sign flips.", phase=True),
   box("The smaller solution is ", 1, "1 is less than 5."),
   box("Check x = 1: (1)" + SQ + " " + MIN + " 6" + TIMES + "(1) + 5 = ", 0, "1 " + MIN + " 6 + 5.",
       done="It gives 0, so x = 1 is correct.")]},
 { # 7  x^2+2x-8=0 negative -> -4
  "display": "Solve \\(x^2 + 2x - 8 = 0\\). Find the negative solution.",
  "solutions": [-4], "calculator": False, "input_type": "single_value",
  "hint": "Find two numbers that multiply to -8 and add to 2, watching the signs carefully.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": -2,
    "message": "Watch the signs: x + 4 = 0 gives x = " + MIN + "4 and x " + MIN + " 2 = 0 gives x = 2. The negative solution is " + MIN + "4, not " + MIN + "2.",
    "note": "flipped both signs"}],
  "guided_steps": [
   say("Solve \\(x^2 + 2x - 8 = 0\\). Two numbers multiply to \\(-8\\) and add to 2: that is 4 and \\(-2\\)."),
   box("The positive number is ", 4, "4 " + TIMES + " (" + MIN + "2) = " + MIN + "8 and 4 + (" + MIN + "2) = 2."),
   box("The negative number is ", -2, "The pair adds to 2, and the positive was 4."),
   say("So \\((x + 4)(x - 2) = 0\\)."),
   box("x + 4 = 0, so x = ", -4, "Move 4 across; the sign flips.", phase=True),
   box("x " + MIN + " 2 = 0, so x = ", 2, "Move " + MIN + "2 across; the sign flips.", phase=True),
   box("The negative solution is ", -4, MIN + "4 is negative, 2 is positive."),
   box("Check x = " + MIN + "4: (" + MIN + "4)" + SQ + " + 2" + TIMES + "(" + MIN + "4) " + MIN + " 8 = ", 0,
       "16 " + MIN + " 8 " + MIN + " 8.", done="It gives 0, so x = " + MIN + "4 is correct.")]},
]

silver = [
 { # 0  x^2-5x+6=0 sum -> 5
  "display": "Solve \\(x^2 - 5x + 6 = 0\\). Find the sum of both solutions.",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Factorise, find both roots, then add them together.",
  "misconceptions": [
   {"pattern": "sign_error_factor", "expect": -5,
    "message": "The middle term is " + MIN + "5x, so both numbers are negative: (x " + MIN + " 2)(x " + MIN + " 3). The roots 2 and 3 add to 5, not " + MIN + "5.",
    "note": "factorised with wrong signs then summed"}],
  "guided_steps": [
   say("Solve \\(x^2 - 5x + 6 = 0\\). Two numbers multiply to 6 and add to \\(-5\\): both negative, \\(-2\\) and \\(-3\\)."),
   box("The number closer to zero is " + MIN, 2,
       MIN + "2 " + TIMES + " (" + MIN + "3) = 6 and " + MIN + "2 + (" + MIN + "3) = " + MIN + "5.", post=""),
   box("The other number is " + MIN, 3, "The pair adds to " + MIN + "5, and the first was " + MIN + "2.", post=""),
   say("So \\((x - 2)(x - 3) = 0\\)."),
   box("x " + MIN + " 2 = 0, so x = ", 2, "Move " + MIN + "2 across; the sign flips.", phase=True),
   box("x " + MIN + " 3 = 0, so x = ", 3, "Move " + MIN + "3 across; the sign flips.", phase=True),
   box("The sum of the two solutions is ", 5, "2 + 3."),
   box("Check x = 2: (2)" + SQ + " " + MIN + " 5" + TIMES + "(2) + 6 = ", 0, "4 " + MIN + " 10 + 6.",
       done="It gives 0, so the roots 2 and 3 are correct and sum to 5.")]},
 { # 1  x^2+3x-18=0 positive -> 3
  "display": "Solve \\(x^2 + 3x - 18 = 0\\). Find the positive solution.",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Find two numbers that multiply to -18 and add to 3.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": 6,
    "message": "The numbers are +6 and " + MIN + "3: (x + 6)(x " + MIN + " 3), giving x = " + MIN + "6 or x = 3. The positive solution is 3, not 6.",
    "note": "flipped both signs"}],
  "guided_steps": [
   say("Solve \\(x^2 + 3x - 18 = 0\\). Two numbers multiply to \\(-18\\) and add to 3: that is 6 and \\(-3\\)."),
   box("The positive number is ", 6, "6 " + TIMES + " (" + MIN + "3) = " + MIN + "18 and 6 + (" + MIN + "3) = 3."),
   box("The negative number is ", -3, "The pair adds to 3, and the positive was 6."),
   say("So \\((x + 6)(x - 3) = 0\\)."),
   box("x + 6 = 0, so x = ", -6, "Move 6 across; the sign flips.", phase=True),
   box("x " + MIN + " 3 = 0, so x = ", 3, "Move " + MIN + "3 across; the sign flips.", phase=True),
   box("The positive solution is ", 3, "3 is positive, " + MIN + "6 is negative."),
   box("Check x = 3: (3)" + SQ + " + 3" + TIMES + "(3) " + MIN + " 18 = ", 0, "9 + 9 " + MIN + " 18.",
       done="It gives 0, so x = 3 is correct.")]},
 { # 2  x^2-2x-35=0 negative -> -5
  "display": "Solve \\(x^2 - 2x - 35 = 0\\). Find the negative solution.",
  "solutions": [-5], "calculator": False, "input_type": "single_value",
  "hint": "Find two numbers that multiply to -35 and add to -2.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": -7,
    "message": "The pair is +5 and " + MIN + "7: (x + 5)(x " + MIN + " 7), giving x = " + MIN + "5 or x = 7. The negative solution is " + MIN + "5, not " + MIN + "7.",
    "note": "flipped both signs"}],
  "guided_steps": [
   say("Solve \\(x^2 - 2x - 35 = 0\\). Two numbers multiply to \\(-35\\) and add to \\(-2\\): that is 5 and \\(-7\\)."),
   box("The positive number is ", 5, "5 " + TIMES + " (" + MIN + "7) = " + MIN + "35 and 5 + (" + MIN + "7) = " + MIN + "2."),
   box("The negative number is ", -7, "The pair adds to " + MIN + "2, and the positive was 5."),
   say("So \\((x + 5)(x - 7) = 0\\)."),
   box("x + 5 = 0, so x = ", -5, "Move 5 across; the sign flips.", phase=True),
   box("x " + MIN + " 7 = 0, so x = ", 7, "Move " + MIN + "7 across; the sign flips.", phase=True),
   box("The negative solution is ", -5, MIN + "5 is negative, 7 is positive."),
   box("Check x = " + MIN + "5: (" + MIN + "5)" + SQ + " " + MIN + " 2" + TIMES + "(" + MIN + "5) " + MIN + " 35 = ", 0,
       "25 + 10 " + MIN + " 35.", done="It gives 0, so x = " + MIN + "5 is correct.")]},
 { # 3  x^2=7x-12 larger -> 4  (WAS x^2=5x-6 ->3, duplicate)
  "display": "Solve \\(x^2 = 7x - 12\\). Find the larger solution.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Rearrange to = 0 first, then factorise.",
  "misconceptions": [
   {"pattern": "gave_smaller", "expect": 3,
    "message": "3 is the smaller root; the question asks for the larger solution, which is 4.",
    "note": "picked the smaller root"}],
  "guided_steps": [
   say("First rearrange to \\(= 0\\). Move \\(7x\\) and \\(-12\\) to the left; each changes sign, giving \\(x^2 - 7x + 12 = 0\\)."),
   box("The constant on the left becomes + ", 12, MIN + "12 moves across and becomes +12."),
   say("Two numbers multiply to 12 and add to \\(-7\\): both negative, \\(-3\\) and \\(-4\\)."),
   box("The number closer to zero is " + MIN, 3, MIN + "3 and " + MIN + "4 multiply to 12 and add to " + MIN + "7.", post=""),
   say("So \\((x - 3)(x - 4) = 0\\)."),
   box("x " + MIN + " 3 = 0, so x = ", 3, "Move " + MIN + "3 across; the sign flips.", phase=True),
   box("x " + MIN + " 4 = 0, so x = ", 4, "Move " + MIN + "4 across; the sign flips.", phase=True),
   box("The larger solution is ", 4, "4 is greater than 3."),
   box("Check x = 4: (4)" + SQ + " = 16, and 7" + TIMES + "4 " + MIN + " 12 = ", 16, "28 " + MIN + " 12 = 16.",
       done="Both sides equal 16, so x = 4 is correct.")]},
 { # 4  x^2+4x=12 positive -> 2
  "display": "Solve \\(x^2 + 4x = 12\\). Find the positive solution.",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Rearrange to = 0 first, then factorise.",
  "misconceptions": [
   {"pattern": "sign_flip", "expect": 6,
    "message": "After rearranging, x" + SQ + " + 4x " + MIN + " 12 = 0 factorises to (x + 6)(x " + MIN + " 2), giving x = " + MIN + "6 or x = 2. The positive solution is 2, not 6.",
    "note": "flipped both signs after rearranging"}],
  "guided_steps": [
   say("First rearrange: move 12 to the left, giving \\(x^2 + 4x - 12 = 0\\)."),
   box("The constant on the left becomes " + MIN, 12, "12 moves across and becomes " + MIN + "12.", post=""),
   say("Two numbers multiply to \\(-12\\) and add to 4: that is 6 and \\(-2\\)."),
   box("The negative number is ", -2, "6 " + TIMES + " (" + MIN + "2) = " + MIN + "12 and 6 + (" + MIN + "2) = 4."),
   say("So \\((x + 6)(x - 2) = 0\\)."),
   box("x + 6 = 0, so x = ", -6, "Move 6 across; the sign flips.", phase=True),
   box("x " + MIN + " 2 = 0, so x = ", 2, "Move " + MIN + "2 across; the sign flips.", phase=True),
   box("The positive solution is ", 2, "2 is positive, " + MIN + "6 is negative."),
   box("Check x = 2: (2)" + SQ + " + 4" + TIMES + "(2) = 4 + 8 = ", 12, "This must equal the right side, 12.",
       done="It gives 12, matching the right side, so x = 2 is correct.")]},
 { # 5  x^2=8x-7 larger -> 7  (WAS x^2=7x-10 ->2, duplicate)
  "display": "Solve \\(x^2 = 8x - 7\\). Find the larger solution.",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Rearrange to = 0 first, then factorise.",
  "misconceptions": [
   {"pattern": "gave_smaller", "expect": 1,
    "message": "1 is the smaller root; the question asks for the larger solution, which is 7.",
    "note": "picked the smaller root"}],
  "guided_steps": [
   say("First rearrange to \\(= 0\\). Move \\(8x\\) and \\(-7\\) to the left, giving \\(x^2 - 8x + 7 = 0\\)."),
   box("The constant on the left becomes + ", 7, MIN + "7 moves across and becomes +7."),
   say("Two numbers multiply to 7 and add to \\(-8\\): both negative, \\(-1\\) and \\(-7\\)."),
   box("The number closer to zero is " + MIN, 1, MIN + "1 and " + MIN + "7 multiply to 7 and add to " + MIN + "8.", post=""),
   say("So \\((x - 1)(x - 7) = 0\\)."),
   box("x " + MIN + " 1 = 0, so x = ", 1, "Move " + MIN + "1 across; the sign flips.", phase=True),
   box("x " + MIN + " 7 = 0, so x = ", 7, "Move " + MIN + "7 across; the sign flips.", phase=True),
   box("The larger solution is ", 7, "7 is greater than 1."),
   box("Check x = 7: (7)" + SQ + " = 49, and 8" + TIMES + "7 " + MIN + " 7 = ", 49, "56 " + MIN + " 7 = 49.",
       done="Both sides equal 49, so x = 7 is correct.")]},
 { # 6  x^2-10x+25=0 how many -> 1
  "display": "Solve \\(x^2 - 10x + 25 = 0\\). How many different solutions are there?",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "Factorise; a perfect square gives one repeated root.",
  "misconceptions": [
   {"pattern": "two_always", "expect": 2,
    "message": "This is a perfect square, (x " + MIN + " 5)" + SQ + ". Both brackets give x = 5, so there is only 1 different solution, not 2.",
    "note": "assumed every quadratic has two distinct roots"}],
  "guided_steps": [
   say("Solve \\(x^2 - 10x + 25 = 0\\). Two numbers multiply to 25 and add to \\(-10\\): they are \\(-5\\) and \\(-5\\), the same number."),
   box("The repeated number is " + MIN, 5, MIN + "5 " + TIMES + " (" + MIN + "5) = 25 and " + MIN + "5 + (" + MIN + "5) = " + MIN + "10.", post=""),
   say("So \\((x - 5)(x - 5) = 0\\), which is \\((x - 5)^2 = 0\\)."),
   box("First bracket: x " + MIN + " 5 = 0, so x = ", 5, "Move " + MIN + "5 across; the sign flips.", phase=True),
   box("The second bracket is the same, so it also gives x = ", 5, "Both brackets are x " + MIN + " 5.", phase=True),
   box("Both brackets give the same value, so the number of different solutions is ", 1, "One repeated root."),
   box("Check x = 5: (5)" + SQ + " " + MIN + " 10" + TIMES + "(5) + 25 = ", 0, "25 " + MIN + " 50 + 25.",
       done="It gives 0, so x = 5 is the single repeated solution.")]},
]

gold = [
 { # 0  2x^2+5x-3=0 positive numerator -> 1
  "display": "Solve \\(2x^2 + 5x - 3 = 0\\). Find the positive solution as a fraction (give the numerator).",
  "solutions": [1], "calculator": False, "input_type": "single_value",
  "hint": "Split the middle term: two numbers multiply to a*c and add to b. The positive root is one half.",
  "misconceptions": [
   {"pattern": "gave_denominator", "expect": 2,
    "message": "The positive solution is 1/2. Its numerator (top) is 1; 2 is the denominator.",
    "note": "gave the denominator instead of the numerator"}],
  "guided_steps": [
   say("Solve \\(2x^2 + 5x - 3 = 0\\). Because \\(a = 2\\), split the middle term: two numbers multiply to \\(2 \\times (-3) = -6\\) and add to 5."),
   box("The positive number is ", 6, "6 and " + MIN + "1: 6 " + TIMES + " (" + MIN + "1) = " + MIN + "6 and 6 + (" + MIN + "1) = 5."),
   box("The negative number is " + MIN, 1, "The pair adds to 5, and the positive was 6.", post=""),
   say("Split and factor: \\(2x^2 + 6x - x - 3 = (2x - 1)(x + 3) = 0\\)."),
   box("First bracket: 2x " + MIN + " 1 = 0, so 2x = 1 and x = 1 over ", 2,
       "Divide by 2: x = 1/2.", phase=True),
   box("Second bracket: x + 3 = 0, so x = ", -3, "Move 3 across; the sign flips.", phase=True),
   box("The positive solution is 1/2. Its numerator (top number) is ", 1, "The top of 1/2 is 1."),
   box("Check x = 1/2: 2" + TIMES + "(1/2)" + SQ + " + 5" + TIMES + "(1/2) " + MIN + " 3 = 0.5 + 2.5 " + MIN + " 3 = ", 0,
       "2" + TIMES + "0.25 = 0.5.", done="It gives 0, so x = 1/2 is correct and its numerator is 1.")]},
 { # 1  3x^2-x-2=0 sum -> 1/3
  "display": "Solve \\(3x^2 - x - 2 = 0\\). Find the sum of both solutions as a fraction.",
  "solutions": [1, 3], "calculator": False, "input_type": "fraction",
  "hint": "Factorise, find both roots, then add them over a common denominator.",
  "misconceptions": [
   {"pattern": "gave_product", "expect": [-2, 3],
    "message": "That is the product of the roots. The sum of 1 and " + MIN + "2/3 is 1/3.",
    "note": "gave product -2/3 instead of the sum"}],
  "guided_steps": [
   say("Solve \\(3x^2 - x - 2 = 0\\). Split the middle term: two numbers multiply to \\(3 \\times (-2) = -6\\) and add to \\(-1\\)."),
   box("The negative number is " + MIN, 3, MIN + "3 and 2: " + MIN + "3 " + TIMES + " 2 = " + MIN + "6 and " + MIN + "3 + 2 = " + MIN + "1.", post=""),
   box("The positive number is ", 2, "The pair adds to " + MIN + "1, and the negative was " + MIN + "3."),
   say("Split and factor: \\(3x^2 - 3x + 2x - 2 = (3x + 2)(x - 1) = 0\\)."),
   box("First bracket: x " + MIN + " 1 = 0, so x = ", 1, "Move " + MIN + "1 across; the sign flips.", phase=True),
   box("Second bracket: 3x + 2 = 0, so x = " + MIN + "2 over ", 3, "Divide by 3: x = " + MIN + "2/3.", phase=True),
   box("Add the roots over 3: 3/3 + (" + MIN + "2/3) = 1/3. The numerator is ", 1, "3 " + MIN + " 2 = 1 on top."),
   box("The denominator is ", 3, "Both thirds share the denominator 3."),
   box("Check x = 1: 3" + TIMES + "(1)" + SQ + " " + MIN + " 1 " + MIN + " 2 = 3 " + MIN + " 1 " + MIN + " 2 = ", 0,
       "A root gives 0.", done="x = 1 checks out, and the two roots sum to 1/3.")]},
 { # 2  6x^2+x-2=0 negative denominator -> 3  (WAS positive numerator ->1, duplicate)
  "display": "Solve \\(6x^2 + x - 2 = 0\\). Find the negative solution as a fraction (give the denominator).",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Split the middle term: two numbers multiply to a*c and add to b. The negative root is minus two thirds.",
  "misconceptions": [
   {"pattern": "gave_numerator", "expect": 2,
    "message": "The negative solution is " + MIN + "2/3. Its denominator (bottom) is 3; 2 is the numerator.",
    "note": "gave the numerator instead of the denominator"}],
  "guided_steps": [
   say("Solve \\(6x^2 + x - 2 = 0\\). Split the middle term: two numbers multiply to \\(6 \\times (-2) = -12\\) and add to 1."),
   box("The positive number is ", 4, "4 and " + MIN + "3: 4 " + TIMES + " (" + MIN + "3) = " + MIN + "12 and 4 + (" + MIN + "3) = 1."),
   box("The negative number is " + MIN, 3, "The pair adds to 1, and the positive was 4.", post=""),
   say("Split and factor: \\(6x^2 + 4x - 3x - 2 = (2x - 1)(3x + 2) = 0\\)."),
   box("First bracket: 2x " + MIN + " 1 = 0 gives x = 1/2. Second bracket: 3x + 2 = 0, so x = " + MIN + "2 over ", 3,
       "Divide by 3: x = " + MIN + "2/3.", phase=True),
   box("The negative solution is " + MIN + "2/3. Its denominator (bottom number) is ", 3, "The bottom of " + MIN + "2/3 is 3.", phase=True),
   box("Check x = 1/2: 6" + TIMES + "(1/2)" + SQ + " + 1/2 " + MIN + " 2 = 1.5 + 0.5 " + MIN + " 2 = ", 0,
       "6" + TIMES + "0.25 = 1.5.", done="It gives 0, so the roots 1/2 and " + MIN + "2/3 are correct.")]},
 { # 3  x^2-x=2x+4 product -> -4
  "display": "Solve \\(x^2 - x = 2x + 4\\). Find the product of both solutions.",
  "solutions": [-4], "calculator": False, "input_type": "single_value",
  "hint": "Rearrange to = 0 first, then factorise and multiply the two roots.",
  "misconceptions": [
   {"pattern": "no_rearrange", "expect": 0,
    "message": "You must rearrange first: x" + SQ + " " + MIN + " x = 2x + 4 becomes x" + SQ + " " + MIN + " 3x " + MIN + " 4 = 0. The roots 4 and " + MIN + "1 have product " + MIN + "4.",
    "note": "factorised x(x-1)=0 without moving the right side, giving product 0"},
   {"pattern": "gave_sum", "expect": 3,
    "message": "That is the sum of the roots. The product of 4 and " + MIN + "1 is " + MIN + "4.",
    "note": "added the roots instead of multiplying"}],
  "guided_steps": [
   say("First rearrange to \\(= 0\\). Move \\(2x\\) and 4 to the left; each changes sign."),
   box("x" + SQ + " " + MIN + " x " + MIN + " 2x " + MIN + " 4 collects to x" + SQ + " " + MIN + " 3x " + MIN + " 4. The middle coefficient is " + MIN, 3,
       MIN + "x " + MIN + " 2x = " + MIN + "3x.", post=""),
   say("Now two numbers multiply to \\(-4\\) and add to \\(-3\\): that is \\(-4\\) and 1."),
   box("The negative number is " + MIN, 4, MIN + "4 " + TIMES + " 1 = " + MIN + "4 and " + MIN + "4 + 1 = " + MIN + "3.", post=""),
   say("So \\((x - 4)(x + 1) = 0\\)."),
   box("x " + MIN + " 4 = 0, so x = ", 4, "Move " + MIN + "4 across; the sign flips.", phase=True),
   box("x + 1 = 0, so x = ", -1, "Move 1 across; the sign flips.", phase=True),
   box("The product of the two solutions 4 and " + MIN + "1 is ", -4, "4 " + TIMES + " (" + MIN + "1) = " + MIN + "4."),
   box("Check x = 4: (4)" + SQ + " " + MIN + " 4 = 12, and 2" + TIMES + "4 + 4 = ", 12, "Both sides must match.",
       done="Both sides equal 12, so x = 4 is correct and the product is " + MIN + "4.")]},
 { # 4  4x^2=9 positive fraction -> 3/2
  "display": "Solve \\(4x^2 = 9\\). Find the positive solution as a fraction.",
  "solutions": [3, 2], "calculator": False, "input_type": "fraction",
  "hint": "Move everything to one side; it is a difference of two squares.",
  "misconceptions": [
   {"pattern": "forgot_root", "expect": [9, 4],
    "message": "Take the square root: x" + SQ + " = 9/4 gives x = 3/2, not 9/4.",
    "note": "divided but did not square-root"},
   {"pattern": "gave_negative", "expect": [-3, 2],
    "message": MIN + "3/2 is also a root, but the question asks for the positive solution, which is 3/2.",
    "note": "gave the negative root"}],
  "guided_steps": [
   say("Solve \\(4x^2 = 9\\). First move 9 across to get \\(4x^2 - 9 = 0\\), a difference of two squares."),
   box("√(4x" + SQ + ") = 2x and √9 = 3, so it factors as (2x + 3)(2x " + MIN + " ", 3,
       "Difference of two squares: (2x + 3)(2x " + MIN + " 3).", post=")"),
   say("So \\((2x + 3)(2x - 3) = 0\\)."),
   box("Second bracket: 2x " + MIN + " 3 = 0, so 2x = 3 and x = 3 over ", 2, "Divide by 2: x = 3/2.", phase=True),
   box("First bracket: 2x + 3 = 0 gives x = " + MIN + "3/2 (negative). The positive root is 3/2, whose numerator is ", 3,
       "The top of 3/2 is 3.", phase=True),
   box("The denominator of the positive solution 3/2 is ", 2, "The bottom of 3/2 is 2."),
   box("Check x = 3/2: 4" + TIMES + "(3/2)" + SQ + " = 4" + TIMES + "(9/4) = ", 9, "This must equal 9.",
       done="It gives 9, matching the right side, so x = 3/2 is correct.")]},
]

# ---------------- TIER GUIDES ----------------
tier_guides = {
 "bronze": {
  "title": "Bronze: quadratics with a = 1, then pick the solution asked for",
  "steps": [
   "Find two numbers that <strong>multiply to \\(c\\)</strong> (the last number) and <strong>add to \\(b\\)</strong> (the middle number).",
   "Write the brackets \\((x + p)(x + q) = 0\\). Set each bracket to zero: \\(x + p = 0\\) gives \\(x = -p\\), so the sign flips.",
   "For \\(x^2 + bx = 0\\) take out \\(x\\); one root is always 0. Read the question: it may want the non-zero root, the larger, or the positive one."],
  "example": {
   "question": "Solve \\(x^2 + 6x + 8 = 0\\). Find the larger solution.",
   "steps": [
    {"label": "Find the pair", "content": "<p>Multiply to \\(8\\), add to \\(6\\): that is \\(2\\) and \\(4\\).</p>"},
    {"label": "Factorise", "content": "<p>\\((x + 2)(x + 4) = 0\\), so \\(x = -2\\) or \\(x = -4\\).</p>"},
    {"label": "Check", "content": "<p>Put \\(x = -2\\): \\(4 - 12 + 8 = 0\\) ✓</p>"},
    {"label": "Answer", "content": "<p><strong>Larger solution: \\(x = -2\\)</strong></p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
  "title": "Silver: negative constants, rearranging, and repeated roots",
  "steps": [
   "When \\(c\\) is negative, one bracket number is negative. Two numbers still multiply to \\(c\\) and add to \\(b\\).",
   "If the equation is not \\(= 0\\), move every term to one side first; each term changes sign as it crosses.",
   "A perfect square like \\(x^2 - 10x + 25\\) gives one repeated root. Then answer exactly what is asked: sum, larger, or how many."],
  "example": {
   "question": "Solve \\(x^2 - 2x - 15 = 0\\). Find the sum of both solutions.",
   "steps": [
    {"label": "Find the pair", "content": "<p>Multiply to \\(-15\\), add to \\(-2\\): that is \\(3\\) and \\(-5\\).</p>"},
    {"label": "Factorise", "content": "<p>\\((x + 3)(x - 5) = 0\\), so \\(x = -3\\) or \\(x = 5\\).</p>"},
    {"label": "Check", "content": "<p>Put \\(x = 5\\): \\(25 - 10 - 15 = 0\\) ✓</p>"},
    {"label": "Answer", "content": "<p><strong>Sum: \\(-3 + 5 = 2\\)</strong></p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
  "title": "Gold: a ≠ 1 with fractional roots, rearrange first",
  "steps": [
   "When \\(a \\neq 1\\), split the middle term: two numbers multiply to \\(a \\times c\\) and add to \\(b\\), then factorise in pairs.",
   "A bracket like \\(2x - 1 = 0\\) gives \\(x = \\tfrac{1}{2}\\): the number is the numerator, the coefficient of \\(x\\) is the denominator.",
   "Rearrange to \\(= 0\\) first if needed, then read the question: numerator, denominator, sum, or product."],
  "example": {
   "question": "Solve \\(2x^2 + 5x - 3 = 0\\). Find the positive root as a fraction.",
   "steps": [
    {"label": "Split", "content": "<p>Multiply to \\(2 \\times -3 = -6\\), add to \\(5\\): \\(6\\) and \\(-1\\).</p>"},
    {"label": "Factorise", "content": "<p>\\((2x - 1)(x + 3) = 0\\), so \\(x = \\tfrac{1}{2}\\) or \\(x = -3\\).</p>"},
    {"label": "Check", "content": "<p>Put \\(x = \\tfrac{1}{2}\\): \\(0.5 + 2.5 - 3 = 0\\) ✓</p>"},
    {"label": "Answer", "content": "<p><strong>Positive root: \\(x = \\tfrac{1}{2}\\)</strong></p>", "isAnswer": True, "is_answer": True}]}},
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
 "opener": {
  "steps": [
   say("Two quick puzzles, no algebra needed. First: I am thinking of two numbers that <strong>multiply to 10</strong> and <strong>add to 7</strong>."),
   box("The smaller of my two numbers is ", 2, "Try pairs that multiply to 10: 1 and 10, 2 and 5. Which pair adds to 7?"),
   say("The pair is 2 and 5. Finding two numbers that multiply and add like that <strong>is</strong> factorising. For \\(x^2 + 7x + 10\\) you look for two numbers that multiply to 10 (the last number) and add to 7 (the middle number): 2 and 5. So it becomes \\((x + 2)(x + 5)\\)."),
   say("Now the second idea. If two numbers multiply together to give <strong>0</strong>, at least one of them must be 0. Suppose 6 times something equals 0."),
   box("6 × (something) = 0, so that something must be ", 0, "6 times what gives 0?"),
   say("That is the <strong>zero product rule</strong>. Once you have \\((x + 2)(x + 5) = 0\\), one bracket must be 0: \\(x + 2 = 0\\) gives \\(x = -2\\), and \\(x + 5 = 0\\) gives \\(x = -5\\). Finding the pair and using the zero rule are the whole method.")]},
 "teach": {
  "bronze": {
   "display": "Solve \\(x^2 + 9x + 20 = 0\\)",
   "steps": [
    say("It is already \\(= 0\\). Look for two numbers that multiply to 20 and add to 9."),
    box("The smaller number is ", 4, "Pairs of 20: 1 and 20, 2 and 10, 4 and 5. Which adds to 9?"),
    box("The larger number is ", 5, "9 " + MIN + " 4 = 5."),
    say("So \\((x + 4)(x + 5) = 0\\). Each bracket can be zero."),
    box("x + 4 = 0, so x = ", -4, "Subtract 4 from both sides; the sign flips.",
        done="The sign flips: a plus in the bracket becomes a minus in the answer. That is the whole point."),
    box("x + 5 = 0, so x = ", -5, "Subtract 5 from both sides."),
    box("Check x = " + MIN + "4: (" + MIN + "4)" + SQ + " + 9" + TIMES + "(" + MIN + "4) + 20 = ", 0, "16 " + MIN + " 36 + 20.",
        done="It gives 0, so x = " + MIN + "4 works, and x = " + MIN + "5 works the same way.")]},
  "silver": {
   "display": "Solve \\(x^2 - 2x - 15 = 0\\)",
   "steps": [
    say("The constant is negative, so one of the two numbers is negative. They multiply to \\(-15\\) and add to \\(-2\\)."),
    box("The negative number is " + MIN, 5, "Try 3 and " + MIN + "5: 3 " + TIMES + " (" + MIN + "5) = " + MIN + "15 and 3 + (" + MIN + "5) = " + MIN + "2.", post=""),
    box("The positive number is ", 3, MIN + "2 " + MIN + " (" + MIN + "5) = 3.",
        done="One negative, one positive: that is the new move when the constant is negative."),
    say("So \\((x + 3)(x - 5) = 0\\)."),
    box("x + 3 = 0, so x = ", -3, "Subtract 3 from both sides."),
    box("x " + MIN + " 5 = 0, so x = ", 5, "Add 5 to both sides."),
    box("Check x = 5: (5)" + SQ + " " + MIN + " 2" + TIMES + "(5) " + MIN + " 15 = ", 0, "25 " + MIN + " 10 " + MIN + " 15.",
        done="It gives 0, so x = 5 works, and x = " + MIN + "3 works the same way.")]},
  "gold": {
   "display": "Solve \\(x^2 = 4x + 12\\)",
   "steps": [
    say("The new move: get everything on one side first. Move \\(4x\\) and 12 to the left, each changing sign."),
    box("The middle term becomes ", -4, "+4x on the right becomes " + MIN + "4x on the left.", post="x"),
    box("The constant becomes ", -12, "+12 on the right becomes " + MIN + "12 on the left.",
        done="Everything is now on one side. That rearrangement is the whole new move."),
    say("So \\(x^2 - 4x - 12 = 0\\). Now the usual routine: two numbers multiply to \\(-12\\) and add to \\(-4\\)."),
    box("The negative number is " + MIN, 6, MIN + "6 and 2: " + MIN + "6 " + TIMES + " 2 = " + MIN + "12 and " + MIN + "6 + 2 = " + MIN + "4.", post=""),
    box("The positive number is ", 2, MIN + "4 " + MIN + " (" + MIN + "6) = 2."),
    say("So \\((x - 6)(x + 2) = 0\\)."),
    box("x " + MIN + " 6 = 0, so x = ", 6, "Add 6 to both sides."),
    box("x + 2 = 0, so x = ", -2, "Subtract 2 from both sides."),
    box("Check x = 6: (6)" + SQ + " " + MIN + " 4" + TIMES + "(6) " + MIN + " 12 = ", 0, "36 " + MIN + " 24 " + MIN + " 12.",
        done="It gives 0, so x = 6 works, and x = " + MIN + "2 works the same way.")]}}}

# ---------------- ASSEMBLE ----------------
pb = {
 "bronze_description": "Simple quadratics with a = 1: factorise, then read off the solution asked for.",
 "silver_description": "Negative constants, rearranging to = 0, and spotting a repeated root.",
 "gold_description": "Harder cases with a not equal to 1 and fractional roots; rearrange first when needed.",
 "bronze": bronze, "silver": silver, "gold": gold,
}

out = {
 "method_card": live["method_card"],
 "topic_links": live["topic_links"],
 "problem_bank": pb,
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": live.get("related_videos", []),
 "worked_examples": live["worked_examples"],
}

json.dump(out, io.open("lesson_maths-eduqas_algebra-L07.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written")
