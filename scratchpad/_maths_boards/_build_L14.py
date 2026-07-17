# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L14_live.json", encoding="utf-8"))
SQ = io.open("_svg_square.txt", encoding="utf-8").read()
MACH = io.open("_svg_machine.txt", encoding="utf-8").read()

MINUS = "−"  # unicode minus


def sv(display, sols, hint, calc, guided, misc, input_type="single_value", options=None, chart=None):
    p = {"display": display, "solutions": sols, "calculator": calc,
         "input_type": input_type, "hint": hint, "misconceptions": misc}
    if options is not None:
        p["options"] = options
    if guided is not None:
        p["guided_steps"] = guided
    if chart is not None:
        p["chart"] = chart
    return p


def m(pattern, expect, message):
    return {"check": pattern, "pattern": pattern, "expect": expect, "message": message}


def say(t):
    return {"say": t}


def box(pre, answer, hint, post="", done=None, phase=None, say_t=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done is not None:
        d["done"] = done
    if phase is not None:
        d["phase"] = phase
    if say_t is not None:
        d["say"] = say_t
    return d


# ============================ BRONZE ============================
bronze = []

# B0 second difference of 1,4,9,16,25 = 2
bronze.append(sv(
    "Find the second difference of \\(1, 4, 9, 16, 25, ...\\)", [2],
    "Find the first differences, then the difference of those.", False,
    [
        say("These are the square numbers. The second difference is the gap between the gaps. First find the first differences."),
        box("4 " + MINUS + " 1 = ", 3, "Second term minus first."),
        box("9 " + MINUS + " 4 = ", 5, "Third term minus second.", done="The first differences are 3, 5, 7, 9."),
        box("Second difference: 5 " + MINUS + " 3 = ", 2, "The difference of the differences.", phase="substitute"),
        box("Check the next gap is the same: 7 " + MINUS + " 5 = ", 2, "Subtract the next pair.", done="Constant 2, so the second difference is 2.", phase="substitute"),
    ],
    [m("first_not_second", 3, "3 is the FIRST difference (4 " + MINUS + " 1). The second difference is the difference of those differences: 5 " + MINUS + " 3 = 2.")]))

# B1 second difference 6, find a = 3
bronze.append(sv(
    "The second difference of a quadratic sequence is \\(6\\). What is \\(a\\) in \\(an^2 + bn + c\\)?", [3],
    "The second difference equals 2a, so halve it.", False,
    [
        say("For a quadratic \\(an^2 + bn + c\\), the constant second difference equals \\(2a\\). Here it is 6, so find \\(a\\)."),
        box("The second difference is 2a. Halve it: 6 " + MINUS.join(["", ""]).join([""]) + "÷ 2 = ", 3, "Divide 6 by 2."),
        box("That halved value is a, so a = ", 3, "It is the number you just found.", phase="substitute"),
        box("Check by doubling: 2 × 3 = ", 6, "Two threes.", done="It gives back 6, so a = 3.", phase="substitute"),
    ],
    [m("no_halve", 6, "6 is the second difference, not a. The second difference equals 2a, so halve it: a = 3.")]))

# B2 f(x)=2x+3, f(4)=11
bronze.append(sv(
    "\\(f(x) = 2x + 3\\). Find \\(f(4)\\).", [11],
    "Double the input, then add 3.", False,
    [
        say("\\(f(x) = 2x + 3\\) is a machine: double the input, then add 3. Find \\(f(4)\\)."),
        box("Double the input: 2 × 4 = ", 8, "Two fours."),
        box("Now add 3: 8 + 3 = ", 11, "Eight plus three.", phase="substitute"),
        box("Read it back to check: 2 × 4 = 8, then 8 + 3 = ", 11, "Double first, then add 3.", done="So \\(f(4) = 11\\).", phase="substitute"),
    ],
    [m("add_before_double", 14, "Substitute into 2x first: 2 × 4 = 8, then add 3 = 11. Adding 3 to the input before doubling (2 × 7 = 14) is the slip.")]))

# B3 f(x)=x^2-1, f(3)=8
bronze.append(sv(
    "\\(f(x) = x^2 - 1\\). Find \\(f(3)\\).", [8],
    "Square the input, then take off 1.", False,
    [
        say("\\(f(x) = x^2 - 1\\). Find \\(f(3)\\): square the input, then take off 1."),
        box("Square: 3² = 3 × 3 = ", 9, "Three threes, not three twos."),
        box("Take off 1: 9 " + MINUS + " 1 = ", 8, "One less than nine.", phase="substitute"),
        box("Check: 3² " + MINUS + " 1 = ", 8, "Nine, then subtract 1.", done="So \\(f(3) = 8\\).", phase="substitute"),
    ],
    [m("square_as_double", 5, "3² means 3 × 3 = 9, not 3 × 2 = 6. Then 9 " + MINUS + " 1 = 8.")]))

# B4 f(x)=2x+3, f(-1)=1
bronze.append(sv(
    "\\(f(x) = 2x + 3\\). Find \\(f(-1)\\).", [1],
    "Double minus 1, then add 3. Keep the sign.", False,
    [
        say("\\(f(x) = 2x + 3\\). Find \\(f(-1)\\). Watch the sign."),
        box("Double: 2 × (" + MINUS + "1) = ", -2, "Two times negative one."),
        box("Add 3: " + MINUS + "2 + 3 = ", 1, "Start at negative 2 and go up 3.", phase="substitute"),
        box("Check: 2 × (" + MINUS + "1) + 3 = ", 1, "Negative two, then add 3.", done="So \\(f(-1) = 1\\).", phase="substitute"),
    ],
    [m("drop_sign", 5, "2 × (" + MINUS + "1) = " + MINUS + "2, not +2. Then " + MINUS + "2 + 3 = 1. Dropping the minus gives 2 + 3 = 5.")]))

# B5 CHANGED: x1=1, x_{n+1}=x_n+3, find x3 = 7
bronze.append(sv(
    "\\(x_{n+1} = x_n + 3\\), \\(x_1 = 1\\). Find \\(x_3\\).", [7],
    "Add 3 each time. Two steps from the start.", False,
    [
        say("\\(x_{n+1} = x_n + 3\\) means add 3 each time. Start at \\(x_1 = 1\\). Find \\(x_3\\)."),
        box("\\(x_2 = x_1 + 3\\): 1 + 3 = ", 4, "One plus three."),
        box("\\(x_3 = x_2 + 3\\): 4 + 3 = ", 7, "Four plus three.", phase="substitute"),
        box("Check the chain: 1, then 4, then ", 7, "One more step of plus 3.", done="So \\(x_3 = 7\\).", phase="substitute"),
    ],
    [m("off_by_one", 4, "4 is \\(x_2\\), only one step in. Add 3 once more for \\(x_3\\): 4 + 3 = 7.")]))

# B6 MC square numbers 1,4,9,16 with SVG
bronze.append(sv(
    SQ + "<br>Find the nth term of \\(1, 4, 9, 16, 25, ...\\). Which is correct?",
    [0],
    "Test each option on the terms 1, 4, 9.", False,
    None,
    [
        m("first_diff_only", 1, "\\(2n - 1\\) gives 1, 3, 5, 7 (the odd numbers), not 1, 4, 9, 16. These terms are perfect squares, so the nth term is \\(n^2\\)."),
        m("off_by_constant", 2, "\\(n^2 + 1\\) gives 2, 5, 10, 17, each one too big. The terms are the squares exactly, so \\(n^2\\) with no + 1."),
        m("rectangle_numbers", 3, "\\(n(n+1)\\) gives 2, 6, 12, 20 (the rectangle numbers), not the squares. \\(n^2\\) gives 1, 4, 9, 16."),
    ],
    input_type="multiple_choice",
    options=["\\(n^2\\)", "\\(2n - 1\\)", "\\(n^2 + 1\\)", "\\(n(n+1)\\)"]))

# B7 CHANGED: f(x)=5x, f(3)=15
bronze.append(sv(
    "\\(f(x) = 5x\\). Find \\(f(3)\\).", [15],
    "The 5x means 5 times the input.", False,
    [
        say("\\(f(x) = 5x\\) means five times the input. Find \\(f(3)\\)."),
        box("Five threes: 5 × 3 = ", 15, "Five times three."),
        box("So \\(f(3)\\) = ", 15, "It is the product you just found.", phase="substitute"),
        box("Check another way, add three 5s: 5 + 5 + 5 = ", 15, "Three fives.", done="Same answer, so \\(f(3) = 15\\).", phase="substitute"),
    ],
    [m("add_not_multiply", 8, "\\(f(3)\\) means 5 × 3 = 15, not 5 + 3 = 8. The 5x is a multiplication.")]))


# ============================ SILVER ============================
silver = []

# S0 MC nth term 3,8,15,24 -> n^2+2n
silver.append(sv(
    "Find the nth term of \\(3, 8, 15, 24, ...\\). Which is correct?", [0],
    "Halve the second difference for a, then find what is left after subtracting n squared.", False,
    None,
    [
        m("leftover_constant", 1, "After subtracting \\(n^2\\) the leftovers are 2, 4, 6, 8, which climb by 2, so the linear part is \\(2n\\), not a fixed + 3. That gives \\(n^2 + 2n\\)."),
        m("no_halve", 2, "The second difference is 2, and a is half of it, so a = 1, not 2. With a = 1 the answer is \\(n^2 + 2n\\)."),
        m("wrong_linear", 3, "The leftovers after \\(n^2\\) are 2, 4, 6, 8, whose nth term is \\(2n\\), giving \\(n^2 + 2n\\). \\(n^2 + n + 1\\) uses the wrong linear part."),
    ],
    input_type="multiple_choice",
    options=["\\(n^2 + 2n\\)", "\\(n^2 + 3\\)", "\\(2n^2 + 1\\)", "\\(n^2 + n + 1\\)"]))

# S1 f=3x+1,g=x^2, fg(2)=13
silver.append(sv(
    "\\(f(x) = 3x + 1\\), \\(g(x) = x^2\\). Find \\(fg(2)\\).", [13],
    "Do g first (square 2), then put the result into f.", False,
    [
        say("\\(f(x) = 3x + 1\\) and \\(g(x) = x^2\\). Find \\(fg(2)\\). The rule: \\(fg\\) means do \\(g\\) first, then \\(f\\)."),
        box("Inside first: g(2) = 2² = ", 4, "Two squared."),
        box("Feed 4 into f: f(4) = 3 × 4 + 1 = ", 13, "Triple 4, then add 1.", phase="substitute"),
        box("Check: square 2 to get 4, then 3 × 4 + 1 = ", 13, "Twelve plus one.", done="So \\(fg(2) = 13\\). Inside first, then outside.", phase="substitute"),
    ],
    [m("composite_order", 49, "\\(fg\\) does g first. Doing f first (gf) gives f(2) = 7, then 7² = 49, a different answer. For fg: square 2 to 4, then 3 × 4 + 1 = 13.")]))

# S2 f=3x+1,g=x^2, gf(2)=49
silver.append(sv(
    "\\(f(x) = 3x + 1\\), \\(g(x) = x^2\\). Find \\(gf(2)\\).", [49],
    "Do f first (triple 2, add 1), then square the result.", False,
    [
        say("Same functions, \\(f(x) = 3x + 1\\), \\(g(x) = x^2\\). Find \\(gf(2)\\): do \\(f\\) first, then \\(g\\)."),
        box("Inside first: f(2) = 3 × 2 + 1 = ", 7, "Triple 2, then add 1."),
        box("Feed 7 into g: g(7) = 7² = ", 49, "Seven squared.", phase="substitute"),
        box("Check: f(2) = 7, then square it: 7 × 7 = ", 49, "Seven sevens.", done="So \\(gf(2) = 49\\). f first, then g.", phase="substitute"),
    ],
    [m("composite_order", 13, "\\(gf\\) does f first. Doing g first (fg) gives 2² = 4, then 3 × 4 + 1 = 13. For gf: 3 × 2 + 1 = 7, then 7² = 49.")]))

# S3 MC inverse of 2x-5 -> (x+5)/2
silver.append(sv(
    "\\(f(x) = 2x - 5\\). Find \\(f^{-1}(x)\\). Which is correct?", [0],
    "Write y = 2x " + MINUS + " 5, swap x and y, then make y the subject.", False,
    None,
    [
        m("sign_slip", 1, "Swap to x = 2y " + MINUS + " 5. The " + MINUS + "5 crosses over as +5: 2y = x + 5, so y = (x + 5)/2. Keeping it as " + MINUS + "5 is the slip."),
        m("undo_one_step", 2, "Undoing must reverse BOTH steps: add 5 AND divide by 2. \\(2x + 5\\) only adds 5. The inverse is (x + 5)/2."),
        m("terms_reversed", 3, "From x = 2y " + MINUS + " 5 you add 5 then divide by 2, giving (x + 5)/2. (5 " + MINUS + " x)/2 has the x and 5 the wrong way round."),
    ],
    input_type="multiple_choice",
    options=["\\(\\frac{x + 5}{2}\\)", "\\(\\frac{x - 5}{2}\\)", "\\(2x + 5\\)", "\\(\\frac{5 - x}{2}\\)"]))

# S4 MC nth term 0,3,8,15,24 -> n^2-1
silver.append(sv(
    "Find the nth term of \\(0, 3, 8, 15, 24, ...\\). Which is correct?", [0],
    "Halve the second difference, then find the constant left after subtracting n squared.", False,
    None,
    [
        m("wrong_linear", 1, "After subtracting \\(n^2\\) the leftovers are " + MINUS + "1, " + MINUS + "1, " + MINUS + "1, a constant, so subtract 1: \\(n^2 - 1\\). \\(n^2 + n\\) would give 2, 6, 12, 20."),
        m("ignored_constant", 2, "\\(n^2\\) gives 1, 4, 9, 16, each one too big. Every term is one less, so \\(n^2 - 1\\)."),
        m("linear_not_constant", 3, "\\(n^2 - n\\) gives 0, 2, 6, 12, which fits the first term by luck but not the rest. The leftovers after \\(n^2\\) are a constant " + MINUS + "1, so \\(n^2 - 1\\)."),
    ],
    input_type="multiple_choice",
    options=["\\(n^2 - 1\\)", "\\(n^2 + n\\)", "\\(n^2\\)", "\\(n^2 - n\\)"]))

# S5 iteration x_{n+1}=(x_n+5)/2, x0=1, x2=4
silver.append(sv(
    "\\(x_{n+1} = \\frac{x_n + 5}{2}\\), \\(x_0 = 1\\). Find \\(x_2\\) to 1 d.p.", [4],
    "Work out x1 first, then feed that answer back in for x2.", False,
    [
        say("\\(x_{n+1} = \\frac{x_n + 5}{2}\\), start \\(x_0 = 1\\). Find \\(x_2\\), two iterations."),
        box("First \\(x_1\\): (1 + 5) ÷ 2 = ", 3, "Six divided by two."),
        box("Now \\(x_2\\): feed 3 back in: (3 + 5) ÷ 2 = ", 4, "Eight divided by two.", phase="substitute"),
        box("Check the chain: 1, then 3, then ", 4, "One more step.", done="So \\(x_2 = 4\\).", phase="substitute"),
    ],
    [m("off_by_one", 3, "3 is \\(x_1\\), the first iteration. Feed it back in for \\(x_2\\): (3 + 5)/2 = 4.")]))

# S6 MC inverse of (x+1)/3 -> 3x-1
silver.append(sv(
    "\\(f(x) = \\frac{x+1}{3}\\). Find \\(f^{-1}(x)\\). Which is correct?", [0],
    "Write y = (x + 1)/3, swap x and y, then make y the subject.", False,
    None,
    [
        m("reciprocal", 1, "Inverting a function is not the reciprocal. Swap to x = (y + 1)/3, so 3x = y + 1, giving y = 3x " + MINUS + " 1."),
        m("sign_slip", 2, "Swap to x = (y + 1)/3. Multiply by 3: 3x = y + 1, so y = 3x " + MINUS + " 1. The + 1 becomes " + MINUS + "1 when it crosses over."),
        m("undo_one_step", 3, "The inverse must reverse both steps: multiply by 3 AND subtract 1, giving \\(3x - 1\\). (x " + MINUS + " 1)/3 just tweaks the original."),
    ],
    input_type="multiple_choice",
    options=["\\(3x - 1\\)", "\\(\\frac{1}{3x+1}\\)", "\\(3x + 1\\)", "\\(\\frac{x-1}{3}\\)"]))


# ============================ GOLD ============================
gold = []

# G0 MC nth term 2,9,20,35,54 -> 2n^2+n-1
gold.append(sv(
    "Find the nth term of \\(2, 9, 20, 35, 54, ...\\). Which is correct?", [0],
    "Halve the second difference for a, subtract 2n squared, then find the linear part.", False,
    None,
    [
        m("constant_not_linear", 1, "First differences 7, 11, 15, 19; second difference 4, so a = 2. Subtracting \\(2n^2\\) leaves 0, 1, 2, 3, which climbs by 1, so the linear part is \\(n - 1\\), not a fixed + 1. Answer \\(2n^2 + n - 1\\)."),
        m("no_halve", 2, "The second difference is 4, and a is HALF of it, so a = 2, not 1. With a = 1 you get \\(n^2 + 2n - 1\\), but the squares grow too slowly to fit."),
        m("sign_of_n", 3, "After subtracting \\(2n^2\\) the leftovers 0, 1, 2, 3 increase, so the linear term is \\(+n\\). \\(2n^2 - n + 1\\) has the sign of n wrong."),
    ],
    input_type="multiple_choice",
    options=["\\(2n^2 + n - 1\\)", "\\(2n^2 + 1\\)", "\\(n^2 + 2n - 1\\)", "\\(2n^2 - n + 1\\)"]))

# G1 f=3x-2, g=x+5, solve fg(x)=19 -> 2
gold.append(sv(
    "\\(f(x) = 3x - 2\\), \\(g(x) = x + 5\\). Solve \\(fg(x) = 19\\).", [2],
    "Form fg(x) = 3(x + 5) " + MINUS + " 2, simplify, then solve.", False,
    [
        say("\\(fg(x)\\) means do \\(g\\) first: \\(f(x+5) = 3(x+5) - 2\\). Multiply out and collect the number part."),
        box("Multiply out the bracket: 3 × 5 = ", 15, "Three fives."),
        box("So the constant is 15 " + MINUS + " 2 = ", 13, "Fifteen take away two, giving fg(x) = 3x + 13."),
        box("Now solve 3x + 13 = 19. Take 13 off: 19 " + MINUS + " 13 = ", 6, "Nineteen minus thirteen.", phase="substitute"),
        box("Divide by 3: 6 ÷ 3 = ", 2, "Six divided by three.", phase="substitute"),
        box("Check: put x = 2 in: 3 × (2 + 5) " + MINUS + " 2 = ", 19, "Inside the bracket is 7, times 3 is 21, minus 2.", done="It gives 19, so x = 2.", phase="substitute"),
    ],
    [m("composite_order", None, "\\(fg(x)\\) does g first: \\(f(x+5) = 3(x+5) - 2 = 3x + 13\\). Solve \\(3x + 13 = 19\\) to get x = 2. Doing f first (gf) would change the equation.")]))

# G2 iteration (x_n^2+3)/5, x0=1, x2=0.728
gold.append(sv(
    "\\(x_{n+1} = \\frac{x_n^2 + 3}{5}\\), \\(x_0 = 1\\). Find \\(x_2\\) to 3 d.p.", [0.728],
    "Work out x1 first, then feed that answer back in for x2.", True,
    [
        say("\\(x_{n+1} = \\frac{x_n^2 + 3}{5}\\), start \\(x_0 = 1\\). Find \\(x_2\\), two iterations. Calculator allowed."),
        box("First \\(x_1\\). Square the start: 1² = ", 1, "One squared is one."),
        box("Add 3, then divide by 5: (1 + 3) ÷ 5 = ", 0.8, "Four divided by five.", done="\\(x_1 = 0.8\\). Feed it back in."),
        box("Now \\(x_2\\). Square 0.8: 0.8² = ", 0.64, "0.8 times 0.8.", phase="substitute"),
        box("Add 3, then divide by 5: (0.64 + 3) ÷ 5 = ", 0.728, "3.64 divided by 5.", done="\\(x_2 = 0.728\\), to 3 d.p.", phase="substitute"),
    ],
    [m("off_by_one", 0.8, "\\(x_1 = (1^2 + 3)/5 = 0.8\\) is only the FIRST iteration. Feed 0.8 back in: \\(x_2 = (0.8^2 + 3)/5 = 0.728\\).")]))

# G3 MC inverse of (2x+1)/(x-3) -> (3x+1)/(x-2)
gold.append(sv(
    "\\(f(x) = \\frac{2x+1}{x-3}\\). Find \\(f^{-1}(x)\\). Which is correct?", [0],
    "Write y = (2x + 1)/(x " + MINUS + " 3), swap x and y, then make y the subject.", False,
    None,
    [
        m("reciprocal", 1, "Flipping the fraction is not inverting the function. Swap to x = (2y + 1)/(y " + MINUS + " 3), then solve for y to get (3x + 1)/(x " + MINUS + " 2)."),
        m("signs_flipped", 2, "Just flipping the signs of the constants does not invert it. Rearranging x(y " + MINUS + " 3) = 2y + 1 properly gives (3x + 1)/(x " + MINUS + " 2)."),
        m("rearrange_sign", 3, "Careful with signs: from x(y " + MINUS + " 3) = 2y + 1 you reach y(x " + MINUS + " 2) = 3x + 1, so (3x + 1)/(x " + MINUS + " 2). (3x " + MINUS + " 1)/(x + 2) has two sign slips."),
    ],
    input_type="multiple_choice",
    options=["\\(\\frac{3x+1}{x-2}\\)", "\\(\\frac{x-3}{2x+1}\\)", "\\(\\frac{2x-1}{x+3}\\)", "\\(\\frac{3x-1}{x+2}\\)"]))

# G4 quadratic 5,12,23,38 -> 10th term 212
gold.append(sv(
    "A quadratic sequence begins \\(5, 12, 23, 38, ...\\). Find the 10th term.", [212],
    "Find the nth term (2n^2 + n + 2), then put n = 10 in.", False,
    [
        say("Sequence 5, 12, 23, 38. Find the nth term, then the 10th term."),
        box("First differences: 12 " + MINUS + " 5 = ", 7, "Second term minus first."),
        box("and 23 " + MINUS + " 12 = ", 11, "Third minus second."),
        box("Second difference: 11 " + MINUS + " 7 = ", 4, "Difference of the differences.", done="The second difference is 2a, so a = 2."),
        box("Subtract \\(2n^2\\). At n = 1: 5 " + MINUS + " 2 × 1² = 5 " + MINUS + " 2 = ", 3, "Take 2 off the first term.", done="Leftovers 3, 4, 5, 6 go up by 1, so the linear part is n + 2. nth term = 2n² + n + 2."),
        box("Now the 10th term. First 2 × 10² = 2 × 100 = ", 200, "Square 10 first, then double.", phase="substitute"),
        box("Then n + 2 = 10 + 2 = ", 12, "Ten plus two.", phase="substitute"),
        box("Add them: 200 + 12 = ", 212, "Two hundred plus twelve.", done="So the 10th term is 212.", phase="substitute"),
    ],
    [m("square_after_multiply", 412, "\\(2n^2\\) at n = 10 means 2 × (10²) = 2 × 100 = 200, not (2 × 10)² = 400. So the 10th term is 200 + 10 + 2 = 212.")]))


# Fix the B1 pre text (avoid the earlier hacky join)
bronze[1]["guided_steps"][1]["pre"] = "The second difference is 2a. Halve it: 6 ÷ 2 = "


# ============================ TIER DESCRIPTIONS ============================
descriptions = {
    "bronze_description": "Put a number into a function, and name a simple square-based sequence.",
    "silver_description": "Compose functions in the right order, find inverses, and build harder nth terms.",
    "gold_description": "Run iteration formulas, and combine quadratic sequences, composites and rational inverses.",
}


# ============================ TIER GUIDES ============================
tier_guides = {
    "bronze": {
        "title": "Bronze: reading a function and naming a square pattern",
        "steps": [
            "A function is a machine. \\(f(4)\\) means put 4 in and follow the rule, so \\(f(x)=2x+3\\) gives \\(f(4)=11\\). Watch signs when the input is negative.",
            "For a number pattern, the terms sit near the square numbers \\(1, 4, 9, 16\\). Find which \\(n^2\\) rule fits by testing the first few terms.",
        ],
        "example": {
            "question": "Given f(x) = 2x + 3, find f(4)",
            "steps": [
                {"label": "Double", "content": "<p>\\(2 \\times 4 = 8\\)</p>"},
                {"label": "Add 3", "content": "<p>\\(8 + 3 = 11\\)</p>"},
                {"label": "Check", "content": "<p>\\(2(4) + 3 = 11\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(f(4) = 11\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: composites, inverses and harder sequences",
        "steps": [
            "Composite \\(fg(x)\\) does \\(g\\) first, then \\(f\\); \\(gf(x)\\) does \\(f\\) first. The order changes the answer, so read the letters right to left.",
            "An inverse undoes the machine: write \\(y=f(x)\\), swap \\(x\\) and \\(y\\), rearrange. To solve \\(f(x)=k\\), undo the steps in reverse.",
            "For a quadratic pattern, halve the second difference to get the \\(n^2\\) coefficient, then find what is left.",
        ],
        "example": {
            "question": "f(x) = 3x + 1, g(x) = x^2. Find fg(2)",
            "steps": [
                {"label": "g first", "content": "<p>\\(g(2) = 2^2 = 4\\)</p>"},
                {"label": "then f", "content": "<p>\\(f(4) = 3(4) + 1 = 13\\)</p>"},
                {"label": "Check", "content": "<p>Square 2 to 4, then \\(3(4)+1 = 13\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(fg(2) = 13\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: iteration and combining every skill",
        "steps": [
            "Iteration repeats \\(x_{n+1}=g(x_n)\\). Work out \\(x_1\\) from \\(x_0\\), then feed each answer back in. Keep full accuracy and only round at the end.",
            "Gold mixes the skills: trickier quadratic nth terms, inverses of fractions, and iterating to 3 decimal places.",
        ],
        "example": {
            "question": "x_{n+1} = (x_n^2 + 3)/5 with x_0 = 1. Find x_2 to 3 d.p.",
            "steps": [
                {"label": "x1", "content": "<p>\\(x_1 = \\frac{1^2 + 3}{5} = \\frac{4}{5} = 0.8\\)</p>"},
                {"label": "x2", "content": "<p>\\(x_2 = \\frac{0.8^2 + 3}{5} = \\frac{3.64}{5} = 0.728\\)</p>"},
                {"label": "Round", "content": "<p>\\(x_2 = 0.728\\) (3 d.p.)</p>"},
                {"label": "Answer", "content": "<p>\\(x_2 = 0.728\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}


# ============================ GUIDED (opener + teach) ============================
guided = {
    "opener": {
        "label": "Before any algebra",
        "display": MACH + "<br>A number machine: your number, <strong>double it</strong>, then <strong>add 3</strong>.",
        "steps": [
            {"say": "The machine doubles your number, then adds 3. No algebra yet, just follow the arrows.",
             "pre": "Put in 4. What comes out? ", "post": "", "answer": 11, "hint": "Double 4 to get 8, then add 3."},
            {"say": "That machine is a <strong>function</strong>. We write it \\(f(x) = 2x + 3\\), and 'put in 4' is \\(f(4)\\). So you just found \\(f(4) = 11\\).",
             "pre": "Now run it backwards. The machine spat out 13. What number went IN? ", "post": "", "answer": 5, "hint": "Undo the steps: take off 3 to get 10, then halve it."},
            {"say": "Going backwards is the <strong>inverse</strong> function. And if you keep feeding each answer back into the machine, you build a chain of numbers: that repeating is <strong>iteration</strong>. Evaluate, invert, iterate: that is the whole lesson, all from one machine."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Given \\(f(x) = 4x + 1\\), find \\(f(2)\\), then \\(f(-1)\\)",
            "label": "Together: your first one",
            "steps": [
                {"say": "\\(f(x) = 4x + 1\\) is a machine: multiply the input by 4, then add 1. Find \\(f(2)\\)."},
                {"pre": "Multiply the input by 4: 4 × 2 = ", "post": "", "answer": 8, "hint": "Four twos."},
                {"pre": "Now add 1: 8 + 1 = ", "post": "", "answer": 9, "hint": "Eight plus one.", "done": "That is \\(f(2) = 9\\). Substitute the number, follow the rule."},
                {"say": "Now try the input −1 to see negatives are fine."},
                {"pre": "Multiply by 4: 4 × (−1) = ", "post": "", "answer": -4, "hint": "Four times negative one."},
                {"pre": "Add 1: −4 + 1 = ", "post": "", "answer": -3, "hint": "Start at negative 4, go up 1.", "done": "So \\(f(-1) = -3\\). Follow the rule, keeping the sign."},
            ],
        },
        "silver": {
            "display": "\\(f(x) = 2x + 5\\), \\(g(x) = x^2\\). Find \\(fg(3)\\), then \\(gf(3)\\).",
            "label": "Together: the silver move",
            "steps": [
                {"say": "\\(f(x) = 2x + 5\\), \\(g(x) = x^2\\). Find \\(fg(3)\\). The rule: \\(fg\\) does \\(g\\) FIRST, then feeds the answer into \\(f\\)."},
                {"pre": "Inside first: g(3) = 3² = ", "post": "", "answer": 9, "hint": "Three squared."},
                {"pre": "Now f(9) = 2 × 9 + 5 = ", "post": "", "answer": 23, "hint": "Double 9, then add 5.", "done": "\\(fg(3) = 23\\). Inside first, then outside."},
                {"say": "Now find \\(gf(3)\\): this time do \\(f\\) first, then \\(g\\)."},
                {"pre": "f(3) = 2 × 3 + 5 = ", "post": "", "answer": 11, "hint": "Double 3, then add 5."},
                {"pre": "Now g(11) = 11² = ", "post": "", "answer": 121, "hint": "Eleven squared.", "done": "\\(gf(3) = 121\\), not 23. Same functions, opposite order, different answer."},
            ],
        },
        "gold": {
            "display": "Use \\(x_{n+1} = \\frac{x_n^2 + 2}{5}\\) with \\(x_0 = 3\\). Find \\(x_2\\) to 3 d.p.",
            "label": "Together: the gold move",
            "steps": [
                {"say": "Iteration means running a formula over and over, each answer feeding the next. \\(x_{n+1} = \\frac{x_n^2 + 2}{5}\\), start \\(x_0 = 3\\). Find \\(x_2\\)."},
                {"pre": "First \\(x_1\\). Square the start: 3² = ", "post": "", "answer": 9, "hint": "Three squared."},
                {"pre": "Add 2, then divide by 5: (9 + 2) ÷ 5 = ", "post": "", "answer": 2.2, "hint": "11 ÷ 5.", "done": "So \\(x_1 = 2.2\\), exact. Now that answer becomes the new input."},
                {"say": "Now \\(x_2\\): feed 2.2 back in. The NEW input is 2.2, not 3. That swap is the whole idea."},
                {"pre": "Square the new input: 2.2² = ", "post": "", "answer": 4.84, "hint": "2.2 × 2.2."},
                {"pre": "Add 2, then divide by 5: (4.84 + 2) ÷ 5 = ", "post": "", "answer": 1.368, "hint": "6.84 ÷ 5 = 1.368.", "done": "\\(x_2 = 1.368\\). Each step uses the PREVIOUS answer, never the start again."},
            ],
        },
    },
}


# ============================ ASSEMBLE ============================
pb = {
    "gold": gold,
    "bronze": bronze,
    "silver": silver,
}
pb.update(descriptions)

out = {
    "method_card": live["method_card"],          # preserved (slim already)
    "topic_links": live["topic_links"],          # preserved
    "problem_bank": pb,
    "related_videos": live["related_videos"],    # preserved
    "worked_examples": live["worked_examples"],  # preserved
    "tier_guides": tier_guides,
    "guided": guided,
}

json.dump(out, io.open("lesson_maths-eduqas_algebra-L14.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-eduqas_algebra-L14.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
