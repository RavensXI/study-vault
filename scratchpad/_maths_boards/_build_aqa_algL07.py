# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for maths-aqa algebra-L07
(Solving Quadratics by Factorising). Fresh-solves every problem, repairs the
two unwinnable gold problems (recurring-decimal roots under strict-equality
two_solutions matching), adds tier_guides / guided / guided_steps / hints /
honest-diagnosis misconceptions, slims the method_card."""
import json, io

M = "−"   # minus sign (U+2212)

live = json.load(io.open("_live_aqa_algL07.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

# ---------------- PROBLEM BANK ----------------
bronze = [
 # b0: x^2-7x=0  -> x(x-7)=0 ; roots 0,7
 {"display": "Solve \\(x^2 - 7x = 0\\)", "solutions": [0, 7], "calculator": False, "input_type": "two_solutions",
  "hint": "Take out the common factor x, then set each factor to zero; do not divide by x.",
  "misconceptions": [
    mc("divide_by_x", [7, 7],
       "It looks like you divided both sides by \\(x\\) and found only \\(x = 7\\). That throws away the \\(x = 0\\) solution. Factorise to \\(x(x - 7) = 0\\) instead, which keeps both.")],
  "guided_steps": [
    box("Both terms share an x. Take it out: x² − 7x = x(x − ", 7, "What times x gives 7x? Just 7.", post=")",
        say="Both terms have an x, so factorise by taking x outside a bracket."),
    box("A product is 0 only when a factor is 0. The lone x factor can be 0, giving x = ", 0, "The bare x set to 0.", phase="substitute",
        say="So \\(x(x - 7) = 0\\). One factor must be zero."),
    box("The other factor: x − 7 = 0 gives x = ", 7, "Add 7 to both sides."),
    box("Check x = 7: 7² − 7×7 = ", 0, "Work out 49 minus 49.",
        done="Gives 0, and x = 0 gives 0 too. Solutions x = 0 and x = 7.")]},
 # b1: x^2+5x=0 -> x(x+5) ; roots -5,0
 {"display": "Solve \\(x^2 + 5x = 0\\)", "solutions": [-5, 0], "calculator": False, "input_type": "two_solutions",
  "hint": "Take out the common factor x, then set each factor to zero.",
  "misconceptions": [
    mc("divide_by_x", [-5, -5],
       "It looks like you divided by \\(x\\) and kept only \\(x = -5\\). Dividing by \\(x\\) loses the \\(x = 0\\) solution. Factorise to \\(x(x + 5) = 0\\) to keep both.")],
  "guided_steps": [
    box("Both terms share an x. Take it out: x² + 5x = x(x + ", 5, "What times x gives 5x? Just 5.", post=")",
        say="Both terms have an x, so factorise by taking x outside a bracket."),
    box("A product is 0 only when a factor is 0. The lone x can be 0, giving x = ", 0, "The bare x set to 0.", phase="substitute",
        say="So \\(x(x + 5) = 0\\)."),
    box("The other factor: x + 5 = 0 gives x = ", -5, "Subtract 5 from both sides."),
    box("Check x = −5: (−5)² + 5×(−5) = ", 0, "Work out 25 minus 25.",
        done="Gives 0, and x = 0 gives 0 too. Solutions x = −5 and x = 0.")]},
 # b2: x^2-9=0 DOTS ; roots -3,3
 {"display": "Solve \\(x^2 - 9 = 0\\)", "solutions": [-3, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "This is a difference of two squares: write it as (x+3)(x−3).",
  "misconceptions": [
    mc("one_solution", [3, 3],
       "It looks like you took \\(x^2 = 9\\) and wrote only \\(x = 3\\). A square root has a positive AND a negative value, so \\(x = 3\\) or \\(x = -3\\). Factorising as \\((x + 3)(x - 3) = 0\\) shows both.")],
  "guided_steps": [
    box("9 is a square: 9 = 3². So this is a difference of two squares: x² − 9 = (x + 3)(x − ", 3, "Difference of two squares: (x+3)(x−3).", post=")",
        say="\\(x^2 - 9\\) has no middle term. It is a difference of two squares."),
    box("Set the first bracket to 0: x + 3 = 0 gives x = ", -3, "Subtract 3 from both sides.", phase="substitute",
        say="So \\((x + 3)(x - 3) = 0\\)."),
    box("Set the second bracket to 0: x − 3 = 0 gives x = ", 3, "Add 3 to both sides."),
    box("Check x = −3: (−3)² − 9 = ", 0, "Work out 9 minus 9.",
        done="Gives 0, and x = 3 gives 9 − 9 = 0 too. Solutions x = −3 and x = 3.")]},
 # b3: x^2-25=0 ; roots -5,5
 {"display": "Solve \\(x^2 - 25 = 0\\)", "solutions": [-5, 5], "calculator": False, "input_type": "two_solutions",
  "hint": "Difference of two squares: write it as (x+5)(x−5).",
  "misconceptions": [
    mc("one_solution", [5, 5],
       "It looks like you took \\(x^2 = 25\\) and wrote only \\(x = 5\\). The negative root counts too, so \\(x = 5\\) or \\(x = -5\\). Factorising as \\((x + 5)(x - 5) = 0\\) shows both.")],
  "guided_steps": [
    box("25 is a square: 25 = 5². So x² − 25 = (x + 5)(x − ", 5, "Difference of two squares: (x+5)(x−5).", post=")",
        say="\\(x^2 - 25\\) is a difference of two squares."),
    box("Set the first bracket to 0: x + 5 = 0 gives x = ", -5, "Subtract 5 from both sides.", phase="substitute",
        say="So \\((x + 5)(x - 5) = 0\\)."),
    box("Set the second bracket to 0: x − 5 = 0 gives x = ", 5, "Add 5 to both sides."),
    box("Check x = 5: 5² − 25 = ", 0, "Work out 25 minus 25.",
        done="Gives 0, and x = −5 gives 25 − 25 = 0 too. Solutions x = −5 and x = 5.")]},
 # b4: x^2+7x+10 -> (x+5)(x+2) ; roots -5,-2
 {"display": "Solve \\(x^2 + 7x + 10 = 0\\)", "solutions": [-5, -2], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to 10 and add to 7.",
  "misconceptions": [
    mc("factors_not_solutions", [5, 2],
       "It looks like you gave the numbers inside the brackets. To find \\(x\\) you set each bracket to 0, which flips the sign: \\((x + 5) = 0\\) gives \\(x = -5\\), not \\(+5\\).")],
  "guided_steps": [
    box("Find two numbers that multiply to +10 and add to +7. One is 5, the other is ", 2, "5 plus what makes 7?",
        say="Factorise: find two numbers that multiply to the last number (10) and add to the middle number (7)."),
    box("So (x + 5)(x + 2) = 0. Set the first bracket to 0: x + 5 = 0 gives x = ", -5, "Subtract 5 from both sides.", phase="substitute",
        say="5 and 2 multiply to 10 and add to 7, so \\((x + 5)(x + 2) = 0\\)."),
    box("Set the second bracket to 0: x + 2 = 0 gives x = ", -2, "Subtract 2 from both sides."),
    box("Check x = −2: (−2)² + 7×(−2) + 10 = ", 0, "Work out 4 − 14 + 10.",
        done="4 − 14 + 10 = 0, and x = −5 gives 25 − 35 + 10 = 0 too. Solutions x = −5 and x = −2.")]},
 # b5: x^2-4x+3 -> (x-1)(x-3) ; roots 1,3
 {"display": "Solve \\(x^2 - 4x + 3 = 0\\)", "solutions": [1, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to 3 and add to −4; both are negative.",
  "misconceptions": [
    mc("sign_swap", [-1, -3],
       "It looks like you kept the bracket numbers with the wrong sign. \\((x - 1)(x - 3) = 0\\) gives \\(x = +1\\) and \\(x = +3\\): a minus in the bracket becomes a plus when you solve.")],
  "guided_steps": [
    box("Find two numbers that multiply to +3 and add to −4. Both are negative: −1 and ", -3, "−1 times what gives 3? And they must add to −4.",
        say="Factorise: two numbers multiplying to +3 and adding to −4."),
    box("So (x − 1)(x − 3) = 0. Set the first bracket to 0: x − 1 = 0 gives x = ", 1, "Add 1 to both sides.", phase="substitute",
        say="−1 and −3 multiply to 3 and add to −4, so \\((x - 1)(x - 3) = 0\\)."),
    box("Set the second bracket to 0: x − 3 = 0 gives x = ", 3, "Add 3 to both sides."),
    box("Check x = 3: 3² − 4×3 + 3 = ", 0, "Work out 9 − 12 + 3.",
        done="9 − 12 + 3 = 0, and x = 1 gives 1 − 4 + 3 = 0 too. Solutions x = 1 and x = 3.")]},
 # b6: x^2+x-6 -> (x+3)(x-2) ; roots -3,2
 {"display": "Solve \\(x^2 + x - 6 = 0\\)", "solutions": [-3, 2], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to −6 and add to 1.",
  "misconceptions": [
    mc("sign_swap", [3, -2],
       "It looks like your two signs are the wrong way round. \\((x + 3)(x - 2) = 0\\) gives \\(x = -3\\) and \\(x = +2\\): each bracket flips its sign when set to 0.")],
  "guided_steps": [
    box("Find two numbers that multiply to −6 and add to +1. The positive one is ", 3, "3 × (−2) = −6 and 3 + (−2) = 1.",
        say="Factorise: two numbers multiplying to −6 and adding to +1."),
    box("So (x + 3)(x − 2) = 0. Set the first bracket to 0: x + 3 = 0 gives x = ", -3, "Subtract 3 from both sides.", phase="substitute",
        say="3 and −2 multiply to −6 and add to 1, so \\((x + 3)(x - 2) = 0\\)."),
    box("Set the second bracket to 0: x − 2 = 0 gives x = ", 2, "Add 2 to both sides."),
    box("Check x = 2: 2² + 2 − 6 = ", 0, "Work out 4 + 2 − 6.",
        done="4 + 2 − 6 = 0, and x = −3 gives 9 − 3 − 6 = 0 too. Solutions x = −3 and x = 2.")]},
 # b7: x^2-6x+8 -> (x-2)(x-4) ; roots 2,4
 {"display": "Solve \\(x^2 - 6x + 8 = 0\\)", "solutions": [2, 4], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to 8 and add to −6; both are negative.",
  "misconceptions": [
    mc("sign_swap", [-2, -4],
       "It looks like you kept the bracket numbers with the wrong sign. \\((x - 2)(x - 4) = 0\\) gives \\(x = +2\\) and \\(x = +4\\): a minus in the bracket becomes a plus when solved.")],
  "guided_steps": [
    box("Find two numbers that multiply to +8 and add to −6. Both are negative: −2 and ", -4, "−2 times what gives 8? And they add to −6.",
        say="Factorise: two numbers multiplying to +8 and adding to −6."),
    box("So (x − 2)(x − 4) = 0. Set the first bracket to 0: x − 2 = 0 gives x = ", 2, "Add 2 to both sides.", phase="substitute",
        say="−2 and −4 multiply to 8 and add to −6, so \\((x - 2)(x - 4) = 0\\)."),
    box("Set the second bracket to 0: x − 4 = 0 gives x = ", 4, "Add 4 to both sides."),
    box("Check x = 4: 4² − 6×4 + 8 = ", 0, "Work out 16 − 24 + 8.",
        done="16 − 24 + 8 = 0, and x = 2 gives 4 − 12 + 8 = 0 too. Solutions x = 2 and x = 4.")]},
]

silver = [
 # s0: x^2-3x-10 -> (x-5)(x+2) ; roots -2,5
 {"display": "Solve \\(x^2 - 3x - 10 = 0\\)", "solutions": [-2, 5], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to −10 and add to −3.",
  "misconceptions": [
    mc("sign_swap", [2, -5],
       "It looks like both signs are reversed. \\((x - 5)(x + 2) = 0\\) gives \\(x = +5\\) and \\(x = -2\\): each bracket flips its sign when set to 0.")],
  "guided_steps": [
    box("Find two numbers that multiply to −10 and add to −3. One is −5, the other is ", 2, "−5 times what gives −10? And they add to −3.",
        say="Factorise: two numbers multiplying to −10 and adding to −3."),
    box("So (x − 5)(x + 2) = 0. Set the first bracket to 0: x − 5 = 0 gives x = ", 5, "Add 5 to both sides.", phase="substitute",
        say="−5 and 2 multiply to −10 and add to −3, so \\((x - 5)(x + 2) = 0\\)."),
    box("Set the second bracket to 0: x + 2 = 0 gives x = ", -2, "Subtract 2 from both sides."),
    box("Check x = 5: 5² − 3×5 − 10 = ", 0, "Work out 25 − 15 − 10.",
        done="25 − 15 − 10 = 0, and x = −2 gives 4 + 6 − 10 = 0 too. Solutions x = −2 and x = 5.")]},
 # s1: x^2+x-12 -> (x+4)(x-3) ; roots -4,3
 {"display": "Solve \\(x^2 + x - 12 = 0\\)", "solutions": [-4, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to −12 and add to 1.",
  "misconceptions": [
    mc("sign_swap", [4, -3],
       "It looks like the two signs are swapped. \\((x + 4)(x - 3) = 0\\) gives \\(x = -4\\) and \\(x = +3\\): each bracket reverses its sign when solved.")],
  "guided_steps": [
    box("Find two numbers that multiply to −12 and add to +1. The positive one is 4, so the other is ", -3, "4 × (−3) = −12 and 4 + (−3) = 1.",
        say="Factorise: two numbers multiplying to −12 and adding to +1."),
    box("So (x + 4)(x − 3) = 0. Set the first bracket to 0: x + 4 = 0 gives x = ", -4, "Subtract 4 from both sides.", phase="substitute",
        say="4 and −3 multiply to −12 and add to 1, so \\((x + 4)(x - 3) = 0\\)."),
    box("Set the second bracket to 0: x − 3 = 0 gives x = ", 3, "Add 3 to both sides."),
    box("Check x = 3: 3² + 3 − 12 = ", 0, "Work out 9 + 3 − 12.",
        done="9 + 3 − 12 = 0, and x = −4 gives 16 − 4 − 12 = 0 too. Solutions x = −4 and x = 3.")]},
 # s2: x^2-8x+16 -> (x-4)^2 ; repeated root 4,4
 {"display": "Solve \\(x^2 - 8x + 16 = 0\\). Enter both solutions (they are equal).", "solutions": [4, 4], "calculator": False, "input_type": "two_solutions",
  "hint": "This factorises to (x−4) squared, a repeated root, so both solutions are equal.",
  "misconceptions": [
    mc("false_dots", [-4, 4],
       "It looks like you treated this as a difference of two squares. It is a perfect square: \\((x - 4)^2 = 0\\), so both solutions are \\(x = +4\\). There is no \\(x = -4\\).")],
  "guided_steps": [
    box("Find two numbers that multiply to +16 and add to −8. Both are the same: −4 and −4. So this is (x − ", 4, "−4 and −4 give the bracket (x − 4).", post=")² = 0",
        say="Two equal numbers (−4 and −4) means a perfect square."),
    box("Set the repeated bracket to 0: x − 4 = 0 gives x = ", 4, "Add 4 to both sides.", phase="substitute",
        say="So \\((x - 4)^2 = 0\\). There is just one factor, repeated."),
    box("Because the bracket is squared, the second solution is the same value: x = ", 4, "A repeated root: the same value twice."),
    box("Check x = 4: 4² − 8×4 + 16 = ", 0, "Work out 16 − 32 + 16.",
        done="16 − 32 + 16 = 0. It is a repeated root, so enter 4 twice.")]},
 # s3: x^2+2x-35 -> (x+7)(x-5) ; roots -7,5
 {"display": "Solve \\(x^2 + 2x - 35 = 0\\)", "solutions": [-7, 5], "calculator": False, "input_type": "two_solutions",
  "hint": "Find two numbers that multiply to −35 and add to 2.",
  "misconceptions": [
    mc("sign_swap", [7, -5],
       "It looks like both signs are reversed. \\((x + 7)(x - 5) = 0\\) gives \\(x = -7\\) and \\(x = +5\\): each bracket flips its sign when set to 0.")],
  "guided_steps": [
    box("Find two numbers that multiply to −35 and add to +2. The positive one is 7, so the other is ", -5, "7 × (−5) = −35 and 7 + (−5) = 2.",
        say="Factorise: two numbers multiplying to −35 and adding to +2."),
    box("So (x + 7)(x − 5) = 0. Set the first bracket to 0: x + 7 = 0 gives x = ", -7, "Subtract 7 from both sides.", phase="substitute",
        say="7 and −5 multiply to −35 and add to 2, so \\((x + 7)(x - 5) = 0\\)."),
    box("Set the second bracket to 0: x − 5 = 0 gives x = ", 5, "Add 5 to both sides."),
    box("Check x = 5: 5² + 2×5 − 35 = ", 0, "Work out 25 + 10 − 35.",
        done="25 + 10 − 35 = 0, and x = −7 gives 49 − 14 − 35 = 0 too. Solutions x = −7 and x = 5.")]},
 # s4: x^2 = 5x+14 -> rearrange -> (x-7)(x+2) ; roots -2,7
 {"display": "Solve \\(x^2 = 5x + 14\\)", "solutions": [-2, 7], "calculator": False, "input_type": "two_solutions",
  "hint": "Rearrange so one side is 0 first, then factorise.",
  "misconceptions": [
    mc("sign_swap", [2, -7],
       "It looks like you rearranged correctly but flipped both signs. \\((x - 7)(x + 2) = 0\\) gives \\(x = +7\\) and \\(x = -2\\): each bracket reverses its sign when solved.")],
  "guided_steps": [
    box("First rearrange to make one side 0. Move 5x and 14 to the left: x² − 5x − ", 14, "Subtract 5x and 14 from both sides.", post=" = 0",
        say="You cannot factorise until one side is 0. Move every term to the left."),
    box("Now factorise x² − 5x − 14. Two numbers multiply to −14 and add to −5: they are −7 and 2. So (x − 7)(x + 2) = 0. Set x − 7 = 0: x = ", 7, "Add 7 to both sides.", phase="substitute",
        say="Two numbers multiplying to −14 and adding to −5 are −7 and 2."),
    box("Set the second bracket to 0: x + 2 = 0 gives x = ", -2, "Subtract 2 from both sides."),
    box("Check x = 7: left is 7² = 49, right is 5×7 + 14 = ", 49, "Work out 35 + 14.",
        done="Both sides are 49, so x = 7 works. x = −2 gives 4 = −10 + 14 = 4 too. Solutions x = −2 and x = 7.")]},
 # s5: 2x^2-8x=0 -> 2x(x-4) ; roots 0,4
 {"display": "Solve \\(2x^2 - 8x = 0\\)", "solutions": [0, 4], "calculator": False, "input_type": "two_solutions",
  "hint": "Take out the common factor 2x, then set each factor to zero.",
  "misconceptions": [
    mc("divide_by_x", [4, 4],
       "It looks like you divided by \\(2x\\) and kept only \\(x = 4\\). That loses the \\(x = 0\\) solution. Factorise to \\(2x(x - 4) = 0\\) to keep both.")],
  "guided_steps": [
    box("Both terms share 2x. Take it out: 2x² − 8x = 2x(x − ", 4, "8x ÷ 2x = 4.", post=")",
        say="Both terms have a factor of 2x. Take it outside a bracket."),
    box("So 2x(x − 4) = 0. The 2 cannot be 0, so 2x = 0 gives x = ", 0, "0 divided by 2 is 0.", phase="substitute",
        say="A product is 0 when a factor is 0."),
    box("The other factor: x − 4 = 0 gives x = ", 4, "Add 4 to both sides."),
    box("Check x = 4: 2×4² − 8×4 = ", 0, "Work out 32 minus 32.",
        done="32 − 32 = 0, and x = 0 gives 0 too. Solutions x = 0 and x = 4.")]},
 # s6: 3x^2-12=0 -> 3(x^2-4) -> (x+2)(x-2) ; roots -2,2
 {"display": "Solve \\(3x^2 - 12 = 0\\)", "solutions": [-2, 2], "calculator": False, "input_type": "two_solutions",
  "hint": "Take out the common factor 3, then use the difference of two squares.",
  "misconceptions": [
    mc("one_solution", [2, 2],
       "It looks like you found \\(x^2 = 4\\) then wrote only \\(x = 2\\). The negative root counts too, so \\(x = 2\\) or \\(x = -2\\).")],
  "guided_steps": [
    box("Take out the common factor 3: 3x² − 12 = 3(x² − ", 4, "12 ÷ 3 = 4.", post=")",
        say="First take out the number common to both terms."),
    box("So 3(x² − 4) = 0. Divide by 3: x² − 4 = 0, a difference of two squares (x+2)(x−2) = 0. Set x + 2 = 0: x = ", -2, "Subtract 2 from both sides.", phase="substitute",
        say="\\(x^2 - 4\\) is a difference of two squares."),
    box("Set the second bracket to 0: x − 2 = 0 gives x = ", 2, "Add 2 to both sides."),
    box("Check x = 2: 3×2² − 12 = ", 0, "Work out 12 minus 12.",
        done="12 − 12 = 0, and x = −2 gives 12 − 12 = 0 too. Solutions x = −2 and x = 2.")]},
]

gold = [
 # g0: 2x^2+5x-3 -> (2x-1)(x+3) ; roots -3,0.5  (KEPT, clean)
 {"display": "Solve \\(2x^2 + 5x - 3 = 0\\)", "solutions": [-3, 0.5], "calculator": False, "input_type": "two_solutions",
  "hint": "Multiply 2 by −3, split the middle term, then factorise by grouping.",
  "misconceptions": [
    mc("forgot_divide_coeff", [-3, 1],
       "It looks like you solved \\(2x - 1 = 0\\) as \\(x = 1\\). But \\(2x = 1\\) means \\(x = \\tfrac{1}{2}\\): divide by the number in front of \\(x\\).")],
  "guided_steps": [
    box("Multiply a by c: 2 × (−3) = −6. Find two numbers that multiply to −6 and add to +5: 6 and ", -1, "6 × (−1) = −6 and 6 + (−1) = 5.",
        say="With a coefficient on \\(x^2\\), use the split-the-middle method. First multiply the ends: \\(2 \\times (-3) = -6\\)."),
    box("Split the middle: 2x² + 6x − x − 3, group to 2x(x+3) − 1(x+3) = (2x − 1)(x + 3). Set 2x − 1 = 0: 2x = 1, x = ", 0.5, "Divide 1 by 2.", phase="substitute",
        say="Grouping gives \\((2x - 1)(x + 3) = 0\\)."),
    box("Set the second bracket to 0: x + 3 = 0 gives x = ", -3, "Subtract 3 from both sides."),
    box("Check x = 0.5: 2×0.5² + 5×0.5 − 3 = ", 0, "Work out 0.5 + 2.5 − 3.",
        done="0.5 + 2.5 − 3 = 0, and x = −3 gives 18 − 15 − 3 = 0 too. Solutions x = −3 and x = 0.5.")]},
 # g1 REPLACED: 5x^2-9x-2 -> (5x+1)(x-2) ; roots -0.2,2   (was 3x^2-11x+6, root 2/3 unwinnable)
 {"display": "Solve \\(5x^2 - 9x - 2 = 0\\)", "solutions": [-0.2, 2], "calculator": False, "input_type": "two_solutions",
  "hint": "Multiply 5 by −2, split the middle term, then factorise by grouping.",
  "misconceptions": [
    mc("forgot_divide_coeff", [-1, 2],
       "It looks like you solved \\(5x + 1 = 0\\) as \\(x = -1\\). But \\(5x = -1\\) means \\(x = -\\tfrac{1}{5} = -0.2\\): divide by the number in front of \\(x\\).")],
  "guided_steps": [
    box("Multiply a by c: 5 × (−2) = −10. Find two numbers that multiply to −10 and add to −9: 1 and ", -10, "1 × (−10) = −10 and 1 + (−10) = −9.",
        say="Split-the-middle method. First multiply the ends: \\(5 \\times (-2) = -10\\)."),
    box("Split the middle: 5x² − 10x + x − 2, group to 5x(x−2) + 1(x−2) = (5x + 1)(x − 2). Set 5x + 1 = 0: 5x = −1, x = ", -0.2, "Divide −1 by 5.", phase="substitute",
        say="Grouping gives \\((5x + 1)(x - 2) = 0\\)."),
    box("Set the second bracket to 0: x − 2 = 0 gives x = ", 2, "Add 2 to both sides."),
    box("Check x = 2: 5×2² − 9×2 − 2 = ", 0, "Work out 20 − 18 − 2.",
        done="20 − 18 − 2 = 0, and x = −0.2 gives 0.2 + 1.8 − 2 = 0 too. Solutions x = −0.2 and x = 2.")]},
 # g2: 5x^2+3x-2 -> (5x-2)(x+1) ; roots -1,0.4  (KEPT, clean)
 {"display": "Solve \\(5x^2 + 3x - 2 = 0\\)", "solutions": [-1, 0.4], "calculator": False, "input_type": "two_solutions",
  "hint": "Multiply 5 by −2, split the middle term, then factorise by grouping.",
  "misconceptions": [
    mc("forgot_divide_coeff", [2, -1],
       "It looks like you solved \\(5x - 2 = 0\\) as \\(x = 2\\). But \\(5x = 2\\) means \\(x = \\tfrac{2}{5} = 0.4\\): divide by the number in front of \\(x\\).")],
  "guided_steps": [
    box("Multiply a by c: 5 × (−2) = −10. Find two numbers that multiply to −10 and add to +3: 5 and ", -2, "5 × (−2) = −10 and 5 + (−2) = 3.",
        say="Split-the-middle method. First multiply the ends: \\(5 \\times (-2) = -10\\)."),
    box("Split the middle: 5x² + 5x − 2x − 2, group to 5x(x+1) − 2(x+1) = (5x − 2)(x + 1). Set 5x − 2 = 0: 5x = 2, x = ", 0.4, "Divide 2 by 5.", phase="substitute",
        say="Grouping gives \\((5x - 2)(x + 1) = 0\\)."),
    box("Set the second bracket to 0: x + 1 = 0 gives x = ", -1, "Subtract 1 from both sides."),
    box("Check x = 0.4: 5×0.4² + 3×0.4 − 2 = ", 0, "Work out 0.8 + 1.2 − 2.",
        done="0.8 + 1.2 − 2 = 0, and x = −1 gives 5 − 3 − 2 = 0 too. Solutions x = −1 and x = 0.4.")]},
 # g3 REPLACED: 4x^2-11x-3 -> (4x+1)(x-3) ; roots -0.25,3  (was 6x^2+x-12, roots 4/3,-3/2 unwinnable)
 {"display": "Solve \\(4x^2 - 11x - 3 = 0\\)", "solutions": [-0.25, 3], "calculator": False, "input_type": "two_solutions",
  "hint": "Multiply 4 by −3, split the middle term, then factorise by grouping.",
  "misconceptions": [
    mc("forgot_divide_coeff", [-1, 3],
       "It looks like you solved \\(4x + 1 = 0\\) as \\(x = -1\\). But \\(4x = -1\\) means \\(x = -\\tfrac{1}{4} = -0.25\\): divide by the number in front of \\(x\\).")],
  "guided_steps": [
    box("Multiply a by c: 4 × (−3) = −12. Find two numbers that multiply to −12 and add to −11: 1 and ", -12, "1 × (−12) = −12 and 1 + (−12) = −11.",
        say="Split-the-middle method. First multiply the ends: \\(4 \\times (-3) = -12\\)."),
    box("Split the middle: 4x² − 12x + x − 3, group to 4x(x−3) + 1(x−3) = (4x + 1)(x − 3). Set 4x + 1 = 0: 4x = −1, x = ", -0.25, "Divide −1 by 4.", phase="substitute",
        say="Grouping gives \\((4x + 1)(x - 3) = 0\\)."),
    box("Set the second bracket to 0: x − 3 = 0 gives x = ", 3, "Add 3 to both sides."),
    box("Check x = 3: 4×3² − 11×3 − 3 = ", 0, "Work out 36 − 33 − 3.",
        done="36 − 33 − 3 = 0, and x = −0.25 gives 0.25 + 2.75 − 3 = 0 too. Solutions x = −0.25 and x = 3.")]},
 # g4: 4x^2-1=0 DOTS -> (2x+1)(2x-1) ; roots -0.5,0.5  (KEPT, clean)
 {"display": "Solve \\(4x^2 - 1 = 0\\)", "solutions": [-0.5, 0.5], "calculator": False, "input_type": "two_solutions",
  "hint": "Difference of two squares: (2x+1)(2x−1).",
  "misconceptions": [
    mc("one_solution", [0.5, 0.5],
       "It looks like you found \\(x^2 = \\tfrac{1}{4}\\) then wrote only \\(x = 0.5\\). The negative root counts too, so \\(x = 0.5\\) or \\(x = -0.5\\). Factorising as \\((2x + 1)(2x - 1) = 0\\) shows both.")],
  "guided_steps": [
    box("A difference of two squares: 4x² = (2x)² and 1 = 1². So 4x² − 1 = (2x + 1)(2x − ", 1, "(2x + 1)(2x − 1).", post=")",
        say="\\(4x^2 - 1\\) has no middle term. It is a difference of two squares."),
    box("So (2x + 1)(2x − 1) = 0. Set the first bracket to 0: 2x + 1 = 0, 2x = −1, x = ", -0.5, "Divide −1 by 2.", phase="substitute",
        say="Set each bracket to 0 in turn."),
    box("Set the second bracket to 0: 2x − 1 = 0, 2x = 1, x = ", 0.5, "Divide 1 by 2."),
    box("Check x = 0.5: 4×0.5² − 1 = ", 0, "Work out 1 minus 1.",
        done="4×0.25 − 1 = 0, and x = −0.5 gives the same. Solutions x = −0.5 and x = 0.5.")]},
]

# ---------------- TIER GUIDES ----------------
tier_guides = {
 "bronze": {
  "title": "Bronze: factorise, then set each bracket to zero",
  "steps": [
    "<strong>Get it as (bracket)(bracket) = 0.</strong> For \\(x^2 + bx + c\\), find two numbers that multiply to \\(c\\) and add to \\(b\\).",
    "A product is zero only when a factor is zero, so <strong>set each bracket to 0</strong> and solve the little equations.",
    "The sign flips: \\((x + 5) = 0\\) gives \\(x = -5\\). A quadratic has <strong>two</strong> solutions, so give both."],
  "example": {
    "question": "Solve x² + 6x + 8 = 0",
    "steps": [
      {"label": "Factorise", "content": "<p>\\((x + 2)(x + 4) = 0\\)</p>"},
      {"label": "Set each bracket to 0", "content": "<p>\\(x + 2 = 0\\) or \\(x + 4 = 0\\)</p>"},
      {"label": "Solve", "content": "<p>\\(x = -2\\) or \\(x = -4\\)</p>"},
      {"label": "Check", "content": "<p>\\((-2)^2 + 6(-2) + 8 = 0\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = -2\\) or \\(x = -4\\)</p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
  "title": "Silver: rearrange or spot a common factor first",
  "steps": [
    "<strong>Make one side 0 first</strong> if it isn't already. Move every term to the left, then factorise.",
    "Spot easy factors: \\(x^2 + bx\\) has a common \\(x\\); \\(x^2 - k^2\\) is \\((x + k)(x - k)\\).",
    "Set each bracket to 0 and solve. Watch for a <strong>repeated root</strong>, where both solutions are equal."],
  "example": {
    "question": "Solve x² − 2x − 8 = 0",
    "steps": [
      {"label": "Factorise", "content": "<p>\\((x - 4)(x + 2) = 0\\)</p>"},
      {"label": "Set each bracket to 0", "content": "<p>\\(x - 4 = 0\\) or \\(x + 2 = 0\\)</p>"},
      {"label": "Solve", "content": "<p>\\(x = 4\\) or \\(x = -2\\)</p>"},
      {"label": "Check", "content": "<p>\\(4^2 - 2(4) - 8 = 0\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 4\\) or \\(x = -2\\)</p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
  "title": "Gold: quadratics where the x squared has a coefficient",
  "steps": [
    "<strong>When \\(ax^2 + bx + c\\) has \\(a > 1\\)</strong>, multiply \\(a\\) by \\(c\\), then find two numbers multiplying to \\(ac\\) and adding to \\(b\\).",
    "<strong>Split the middle term</strong> with those two numbers, then factorise by grouping into two brackets.",
    "Set each bracket to 0. A bracket like \\(2x - 1 = 0\\) gives \\(x = \\tfrac{1}{2}\\), so divide by the number in front."],
  "example": {
    "question": "Solve 2x² + 7x + 3 = 0",
    "steps": [
      {"label": "Split the middle (2×3 = 6)", "content": "<p>\\(2x^2 + 6x + x + 3\\)</p>"},
      {"label": "Factorise by grouping", "content": "<p>\\((2x + 1)(x + 3) = 0\\)</p>"},
      {"label": "Solve each bracket", "content": "<p>\\(x = -\\tfrac{1}{2}\\) or \\(x = -3\\)</p>"},
      {"label": "Check", "content": "<p>\\(2(-3)^2 + 7(-3) + 3 = 0\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = -0.5\\) or \\(x = -3\\)</p>", "isAnswer": True, "is_answer": True}]}},
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
 "opener": {
  "label": "Before any algebra",
  "display": "Two numbers are multiplied together and the answer is <strong>0</strong>.<br>One of the numbers is <strong>6</strong>.<br><strong>What is the other number?</strong>",
  "steps": [
    {"say": "No algebra needed. Anything times 6 gives 0 only if the other number is nothing at all.",
     "pre": "The other number must be ", "post": "", "answer": 0,
     "hint": "What do you multiply 6 by to get 0?"},
    {"say": "That is the whole trick. If two things multiply to 0, at least one of them must be 0. Now try it with brackets: \\((x - 4)(x - 5) = 0\\). Suppose the first bracket is the one equal to 0.",
     "pre": "x − 4 = 0, so x = ", "post": "", "answer": 4,
     "hint": "Add 4 to both sides of x − 4 = 0."},
    {"say": "And the second bracket \\((x - 5) = 0\\) gives \\(x = 5\\). So the two solutions are \\(x = 4\\) and \\(x = 5\\). That is exactly how you solve a quadratic: factorise it into two brackets, then set each bracket to 0 in turn."}]},
 "teach": {
  "bronze": {
   "display": "Solve \\(x^2 + 5x + 6 = 0\\)",
   "label": "Together: factorise then set each to zero",
   "steps": [
     {"say": "Factorise first. Find two numbers that multiply to +6 and add to +5. One is 2.",
      "pre": "The other number is ", "post": "", "answer": 3,
      "hint": "2 plus what makes 5?"},
     {"say": "So \\((x + 2)(x + 3) = 0\\). The new move: a product is 0 only if a factor is 0. Set the first bracket to 0.",
      "pre": "x + 2 = 0, so x = ", "post": "", "answer": -2,
      "hint": "Subtract 2 from both sides."},
     {"say": "Now the second bracket.",
      "pre": "x + 3 = 0, so x = ", "post": "", "answer": -3,
      "hint": "Subtract 3 from both sides."},
     {"say": "Check x = −2 in the original.",
      "pre": "(−2)² + 5×(−2) + 6 = ", "post": "", "answer": 0,
      "done": "4 − 10 + 6 = 0, and x = −3 gives 9 − 15 + 6 = 0 too. Setting each bracket to 0 was the whole point. Solutions x = −2 and x = −3.",
      "hint": "Work out 4 − 10 + 6."}]},
  "silver": {
   "display": "Solve \\(x^2 + 4x = 12\\)",
   "label": "Together: rearrange to = 0 first",
   "steps": [
     {"say": "You cannot factorise until one side is 0. The new move: rearrange first. Move 12 to the left.",
      "pre": "x² + 4x − ", "post": " = 0", "answer": 12,
      "hint": "Subtract 12 from both sides."},
     {"say": "Now factorise x² + 4x − 12. Two numbers multiply to −12 and add to +4. One is 6.",
      "pre": "The other number is ", "post": "", "answer": -2,
      "hint": "6 × (−2) = −12 and 6 + (−2) = 4."},
     {"say": "So \\((x + 6)(x - 2) = 0\\). Set the first bracket to 0.",
      "pre": "x + 6 = 0, so x = ", "post": "", "answer": -6,
      "hint": "Subtract 6 from both sides."},
     {"say": "Now the second bracket.",
      "pre": "x − 2 = 0, so x = ", "post": "", "answer": 2,
      "hint": "Add 2 to both sides."},
     {"say": "Check x = 2 in the original: does the left equal 12?",
      "pre": "2² + 4×2 = ", "post": "", "answer": 12,
      "done": "4 + 8 = 12, matching the right side, so x = 2 works. x = −6 gives 36 − 24 = 12 too. Rearranging to = 0 unlocked it. Solutions x = −6 and x = 2.",
      "hint": "Work out 4 + 8."}]},
  "gold": {
   "display": "Solve \\(2x^2 - 3x - 2 = 0\\)",
   "label": "Together: split the middle term",
   "steps": [
     {"say": "The x² has a coefficient of 2. The new move: multiply the ends, 2 × (−2) = −4, and find two numbers multiplying to −4 and adding to −3. One is −4.",
      "pre": "The other number is ", "post": "", "answer": 1,
      "hint": "−4 × what gives −4? And they add to −3."},
     {"say": "Split the middle: \\(2x^2 - 4x + x - 2\\), then group into \\((2x + 1)(x - 2) = 0\\). Set the first bracket to 0: 2x + 1 = 0, so 2x = −1.",
      "pre": "x = ", "post": "", "answer": -0.5,
      "hint": "Divide −1 by 2."},
     {"say": "Now the second bracket.",
      "pre": "x − 2 = 0, so x = ", "post": "", "answer": 2,
      "hint": "Add 2 to both sides."},
     {"say": "Check x = 2 in the original.",
      "pre": "2×2² − 3×2 − 2 = ", "post": "", "answer": 0,
      "done": "8 − 6 − 2 = 0, and x = −0.5 gives 0.5 + 1.5 − 2 = 0 too. Splitting the middle term unlocked it. Solutions x = −0.5 and x = 2.",
      "hint": "Work out 8 − 6 − 2."}]},
 },
}

# ---------------- METHOD CARD (slim) ----------------
method_card = {
 "title": "How to Solve Quadratics by Factorising",
 "steps": [
   "Rearrange so one side equals 0",
   "Factorise into two brackets",
   "Set each bracket equal to 0",
   "Solve each to get both values of x"],
 "content": "<p>A <strong>quadratic equation</strong> has the form \\(ax^2 + bx + c = 0\\) and usually has two solutions.</p><p>Rearrange so one side is 0, then factorise. A product is 0 only when a factor is 0, so set each bracket to 0 and solve. The sign flips: \\((x + 3) = 0\\) gives \\(x = -3\\). Do not divide both sides by \\(x\\); that loses the \\(x = 0\\) solution, so factorise instead.</p>",
 "example": "<p><strong>Solve</strong> \\(x^2 - 5x + 6 = 0\\)</p><p><strong>Factorise:</strong> \\((x - 2)(x - 3) = 0\\)</p><p><strong>Set each to 0:</strong> \\(x - 2 = 0\\) or \\(x - 3 = 0\\)</p><p><strong>Solve:</strong> \\(x = 2\\) or \\(x = 3\\)</p>",
}

# ---------------- ASSEMBLE ----------------
pd = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description": "Factorise the quadratic into two brackets, then set each bracket to zero to find both solutions.",
   "silver_description": "Rearrange to equal zero, or take out a common factor or difference of two squares, before solving.",
   "gold_description": "Solve quadratics where x squared has a coefficient greater than 1, using the split the middle term method.",
 },
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": live.get("related_videos", []),
 "worked_examples": live.get("worked_examples", []),
}

json.dump(pd, io.open("lesson_maths-aqa_algebra-L07.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_algebra-L07.json")

def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
print("method_card.content words:", words(method_card["content"]))
for t in ("bronze","silver","gold"):
    print(t, "tier_guide steps words:", sum(words(s) for s in tier_guides[t]["steps"]))
