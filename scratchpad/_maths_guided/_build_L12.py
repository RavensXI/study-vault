# -*- coding: utf-8 -*-
"""Builder for algebra-L12 Quadratic Inequalities & Regions guided conversion."""
import json, io

live = json.load(io.open("_live_algebra-L12.json", encoding="utf-8"))

MIN = "-"  # hyphen-minus for plain text (em dash banned)

# ---------- helpers ----------
def say(t): return {"say": t}

def box(pre, answer, hint, post="", done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d

def root_box(r):
    if r > 0:
        return box("From x - %d = 0:  x = " % r, r, "x - %d = 0 gives x = %d." % (r, r))
    if r < 0:
        return box("From x + %d = 0:  x = " % (-r), r, "x + %d = 0 gives x = %d." % (-r, r))
    return box("The factor x on its own is zero when x = ", 0, "x = 0.")

def fac_str(r1, r2):
    def b(r):
        if r > 0: return "(x-%d)" % r
        if r < 0: return "(x+%d)" % (-r)
        return "x"
    return b(r1) + b(r2)

def std_walk(quad, prod, summ, twonums, r1, r2, sym, region, bound_which, answer,
             test_x, test_expr, test_val):
    rs, rb = sorted([r1, r2])
    fac = fac_str(r1, r2)
    s1 = say("Factorise \\(%s\\). Two numbers multiply to %s and add to %s: they are %s, giving \\(%s\\). Each bracket gives a root."
             % (quad, prod, summ, twonums, fac))
    if region == "between":
        rs_say = ("The curve is a U-shape crossing at %d and %d. For \\(%s 0\\) it dips below the x-axis BETWEEN the roots, so the solution is \\(%d %s x %s %d\\)."
                  % (rs, rb, sym, rs, sym, sym, rb))
    else:  # outside
        less = "<" if sym == ">" else "\\leq"
        rs_say = ("The curve is a U-shape crossing at %d and %d. For \\(%s 0\\) it is above the x-axis OUTSIDE the roots, so \\(x %s %d\\) or \\(x %s %d\\)."
                  % (rs, rb, sym, less, rs, sym, rb))
    s4 = say(rs_say)
    if bound_which == "lower":
        bpre, bans, bhint = "The lower bound is the smaller root:  ", rs, "The smaller of %d and %d." % (rs, rb)
    elif bound_which == "upper":
        bpre, bans, bhint = "The upper bound is the larger root:  ", rb, "The larger of %d and %d." % (rs, rb)
    elif bound_which == "larger":
        bpre, bans, bhint = "The larger root is:  ", rb, "The larger of %d and %d." % (rs, rb)
    else:  # smaller
        bpre, bans, bhint = "The smaller root is:  ", rs, "The smaller of %d and %d." % (rs, rb)
    assert bans == answer, (quad, bans, answer)
    bbox = box(bpre, bans, bhint, phase="substitute")
    donetxt = ("Below zero, so the between region is right; the answer is %d." % answer) if region == "between" \
        else ("Above zero, so the outside region is right; the answer is %d." % answer)
    cbox = box("Check with x = %s:  %s = " % (test_x, test_expr), test_val,
               "Work it out. It should land on the correct side of zero.", done=donetxt, phase="substitute")
    return [s1, root_box(r1), root_box(r2), s4, bbox, cbox]

# ---------- messages (em-dash-free) ----------
def mc_wrong_region_between(sym, rs, rb, other):
    return ("For \\(%s 0\\) the curve is below the axis BETWEEN the roots %d and %d, so the answer lies in \\(%d %s x %s %d\\). You entered %d, which is the boundary of the outside region instead."
            % (sym, rs, rb, rs, sym, sym, rb, other))

def mc_wrong_region_outside_smaller(sym, rs, rb):
    return ("For \\(%s 0\\) the curve is above the axis OUTSIDE the roots, and both roots are still the boundaries. The smaller critical value is %d; check which value the question asks for."
            % (sym, rs))

def mc_factoring(quad, fac, rs, rb):
    return ("Check your factorising. \\(%s\\) factorises to \\(%s\\), giving roots %d and %d. A sign slip on a bracket sends the roots, and the bound, to the wrong place."
            % (quad, fac, rs, rb))

# ================= PROBLEM BANK =================
bronze = []
# each: dict of fields
def P(display, solutions, input_type, hint, misc, guided):
    d = {"display": display, "solutions": solutions, "calculator": False,
         "input_type": input_type, "hint": hint, "misconceptions": misc}
    if guided is not None:
        d["guided_steps"] = guided
    return d

# --- BRONZE (all x^2 < 0, between roots) ---
# b0: x^2-4x+3<0 lower  roots 1,3
bronze.append(P(
    "Solve \\(x^2 - 4x + 3 < 0\\). Give the lower bound.", [1], "single_value",
    "Factorise, find the two roots, then take the smaller one as the lower bound.",
    [{"pattern":"wrong_region","expect":3,"message":mc_wrong_region_between("<",1,3,3),"note":"Outside-region student enters the larger root 3."},
     {"pattern":"wrong_roots","expect":-1,"message":mc_factoring("x^2 - 4x + 3","(x-1)(x-3)",1,3),"note":"Sign slip (x+1)(x-3) gives roots -1,3; lower bound -1."}],
    std_walk("x^2 - 4x + 3","+3","-4","-1 and -3",1,3,"<","between","lower",1,"2","2² - 4(2) + 3",-1)))
# b1: x^2-6x+8<0 lower roots 2,4
bronze.append(P(
    "Solve \\(x^2 - 6x + 8 < 0\\). Give the lower bound.", [2], "single_value",
    "Factorise into two brackets, then the lower bound is the smaller root.",
    [{"pattern":"wrong_region","expect":4,"message":mc_wrong_region_between("<",2,4,4),"note":"Enters larger root 4."},
     {"pattern":"wrong_roots","expect":-2,"message":mc_factoring("x^2 - 6x + 8","(x-2)(x-4)",2,4),"note":"(x+2)(x-4) sign slip gives lower bound -2."}],
    std_walk("x^2 - 6x + 8","+8","-6","-2 and -4",2,4,"<","between","lower",2,"3","3² - 6(3) + 8",-1)))
# b2: x^2-9<0 upper roots -3,3
bronze.append(P(
    "Solve \\(x^2 - 9 < 0\\). Give the upper bound.", [3], "single_value",
    "This is a difference of two squares; the upper bound is the larger root.",
    [{"pattern":"wrong_region","expect":-3,"message":mc_wrong_region_between("<",-3,3,-3),"note":"Enters smaller root -3."},
     {"pattern":"wrong_roots","expect":9,"message":"Solve \\(x^2 = 9\\) by square-rooting: \\(x = \\pm 3\\), not \\(\\pm 9\\). The roots are the numbers that square to give 9.","note":"x=9 slip (no square root)."}],
    [say("Factorise \\(x^2 - 9\\). It is a difference of two squares: \\((x-3)(x+3)\\). Each bracket gives a root."),
     root_box(3), root_box(-3),
     say("The curve is a U-shape crossing at -3 and 3. For \\(< 0\\) it dips below the x-axis BETWEEN the roots, so \\(-3 < x < 3\\)."),
     box("The upper bound is the larger root:  ", 3, "The larger of -3 and 3.", phase="substitute"),
     box("Check with x = 0:  0² - 9 = ", -9, "It should be below zero.", done="Below zero, so -3 < x < 3; the upper bound is 3.", phase="substitute")]))
# b3: x^2-x-2<0 lower roots -1,2
bronze.append(P(
    "Solve \\(x^2 - x - 2 < 0\\). Give the lower bound.", [-1], "single_value",
    "Factorise, then the lower bound is the smaller (more negative) root.",
    [{"pattern":"wrong_region","expect":2,"message":mc_wrong_region_between("<",-1,2,2),"note":"Enters larger root 2."},
     {"pattern":"wrong_roots","expect":-2,"message":mc_factoring("x^2 - x - 2","(x+1)(x-2)",-1,2),"note":"(x+2)(x-1) gives roots -2,1; lower bound -2."}],
    std_walk("x^2 - x - 2","-2","-1","+1 and -2",-1,2,"<","between","lower",-1,"0","0² - 0 - 2",-2)))
# b4 (NEW, was duplicate): x^2-10x+24<0 lower roots 4,6
bronze.append(P(
    "Solve \\(x^2 - 10x + 24 < 0\\). Give the lower bound.", [4], "single_value",
    "Factorise into two brackets; the lower bound is the smaller root.",
    [{"pattern":"wrong_region","expect":6,"message":mc_wrong_region_between("<",4,6,6),"note":"Enters larger root 6."},
     {"pattern":"wrong_roots","expect":-6,"message":mc_factoring("x^2 - 10x + 24","(x-4)(x-6)",4,6),"note":"(x+4)(x+6) sign slip gives roots -4,-6; lower bound -6."}],
    std_walk("x^2 - 10x + 24","+24","-10","-4 and -6",4,6,"<","between","lower",4,"5","5² - 10(5) + 24",-1)))
# b5 (NEW, was duplicate): x^2-4x-21<0 upper roots -3,7
bronze.append(P(
    "Solve \\(x^2 - 4x - 21 < 0\\). Give the upper bound.", [7], "single_value",
    "Factorise, then the upper bound is the larger root.",
    [{"pattern":"wrong_region","expect":-3,"message":mc_wrong_region_between("<",-3,7,-3),"note":"Enters smaller root -3."},
     {"pattern":"wrong_roots","expect":3,"message":mc_factoring("x^2 - 4x - 21","(x-7)(x+3)",-3,7),"note":"(x+7)(x-3) sign slip gives roots -7,3; upper bound 3."}],
    std_walk("x^2 - 4x - 21","-21","-4","-7 and +3",7,-3,"<","between","upper",7,"0","0² - 0 - 21",-21)))
# b6: x^2+2x-8<0 lower roots -4,2
bronze.append(P(
    "Solve \\(x^2 + 2x - 8 < 0\\). Give the lower bound.", [-4], "single_value",
    "Factorise, then take the smaller root as the lower bound.",
    [{"pattern":"wrong_region","expect":2,"message":mc_wrong_region_between("<",-4,2,2),"note":"Enters larger root 2."},
     {"pattern":"wrong_roots","expect":-2,"message":mc_factoring("x^2 + 2x - 8","(x+4)(x-2)",-4,2),"note":"(x-4)(x+2) gives roots 4,-2; lower bound -2."}],
    std_walk("x^2 + 2x - 8","-8","+2","+4 and -2",-4,2,"<","between","lower",-4,"0","0² + 0 - 8",-8)))
# b7: x^2-3x-10<0 upper roots -2,5
bronze.append(P(
    "Solve \\(x^2 - 3x - 10 < 0\\). Give the upper bound.", [5], "single_value",
    "Factorise, then the upper bound is the larger root.",
    [{"pattern":"wrong_region","expect":-2,"message":mc_wrong_region_between("<",-2,5,-2),"note":"Enters smaller root -2."},
     {"pattern":"wrong_roots","expect":2,"message":mc_factoring("x^2 - 3x - 10","(x-5)(x+2)",-2,5),"note":"(x+5)(x-2) gives roots -5,2; upper bound 2."}],
    std_walk("x^2 - 3x - 10","-10","-3","-5 and +2",5,-2,"<","between","upper",5,"0","0² - 0 - 10",-10)))

# --- SILVER ---
silver = []
# s0 (REFRAMED, region count): x^2-x-6<0 below-axis region, count integers = 4
silver.append(P(
    "The graph of \\(y = x^2 - x - 6\\) crosses the x-axis at \\(x = -2\\) and \\(x = 3\\). The solution of \\(x^2 - x - 6 < 0\\) is the region where the curve dips below the x-axis. How many integer values of x lie in that region?",
    [4], "single_value",
    "Below the x-axis means between the roots; count the whole numbers strictly between -2 and 3.",
    [{"pattern":"notation","expect":6,"message":"The inequality is strict (\\(< 0\\)), so the endpoints -2 and 3 sit ON the axis and are not below it. Counting them as well gives 6, but they must be left out.","note":"Using <= includes -2 and 3: six integers."}],
    [say("The curve crosses at -2 and 3 and is a U-shape, so below the x-axis means BETWEEN the roots: \\(-2 < x < 3\\)."),
     box("The smallest integer strictly inside -2 < x < 3 is  ", -1, "Just above -2."),
     box("The largest integer strictly inside is  ", 2, "Just below 3."),
     say("So the integers in the region are -1, 0, 1, 2."),
     box("Count them: -1, 0, 1, 2.  How many?  ", 4, "Count the list.", phase="substitute"),
     box("Check x = -2 is NOT below the axis:  (-2)² - (-2) - 6 = ", 0,
         "4 + 2 - 6. It equals 0, so -2 is on the axis, not below it.",
         done="Endpoints sit on the axis, so only -1, 0, 1, 2 count: 4 integers.", phase="substitute")]))
# s1: x^2+x-6<=0 upper roots -3,2
silver.append(P(
    "Solve \\(x^2 + x - 6 \\leq 0\\). Give the upper bound.", [2], "single_value",
    "Factorise; the upper bound is the larger root, and the sign is inclusive.",
    [{"pattern":"wrong_region","expect":-3,"message":mc_wrong_region_between("\\leq",-3,2,-3),"note":"Enters smaller root -3."},
     {"pattern":"wrong_roots","expect":3,"message":mc_factoring("x^2 + x - 6","(x+3)(x-2)",-3,2),"note":"(x-3)(x+2) gives roots 3,-2; upper bound 3."}],
    std_walk("x^2 + x - 6","-6","+1","+3 and -2",-3,2,"\\leq","between","upper",2,"0","0² + 0 - 6",-6)))
# s2: x^2-5x>=0 two critical values 0,5
silver.append(P(
    "Solve \\(x^2 - 5x \\geq 0\\). What are the two critical values?", [0,5], "two_solutions",
    "Take out a common factor of x, then set each factor to zero.",
    [],
    [say("Factorise \\(x^2 - 5x\\) by taking out x: \\(x(x-5)\\). Set each factor to zero."),
     box("The first factor is x itself, so one root is  ", 0, "x = 0."),
     box("From x - 5 = 0 the other root is  ", 5, "x - 5 = 0 gives x = 5."),
     say("The two critical values are 0 and 5. (For the full answer, \\(\\geq 0\\) means outside: \\(x \\leq 0\\) or \\(x \\geq 5\\).)"),
     box("Enter the smaller critical value:  ", 0, "The smaller of 0 and 5.", phase="substitute"),
     box("Enter the larger critical value:  ", 5, "The larger of 0 and 5.", phase="substitute"),
     box("Check x = 5:  5² - 5(5) = ", 0, "25 - 25. It equals 0, which satisfies \\(\\geq 0\\).",
         done="Both 0 and 5 make the expression 0, so they are the two critical values.", phase="substitute")]))
# s3: x^2+3x-4>0 larger root roots -4,1
silver.append(P(
    "Solve \\(x^2 + 3x - 4 > 0\\). Give the larger root.", [1], "single_value",
    "Factorise, then the larger root is the bigger of the two values.",
    [{"pattern":"wrong_roots","expect":4,"message":mc_factoring("x^2 + 3x - 4","(x+4)(x-1)",-4,1),"note":"(x-4)(x+1) gives roots 4,-1; larger root 4."}],
    std_walk("x^2 + 3x - 4","-4","+3","+4 and -1",-4,1,">","outside","larger",1,"2","2² + 3(2) - 4",6)))
# s4: how many integers satisfy x^2-9<0 => 5
silver.append(P(
    "How many integers satisfy \\(x^2 - 9 < 0\\)?", [5], "single_value",
    "Find the roots, then count the whole numbers strictly between them.",
    [{"pattern":"wrong_roots","expect":17,"message":"Solve \\(x^2 = 9\\) by square-rooting to get \\(x = \\pm 3\\), not \\(\\pm 9\\). Wrong roots give far too many integers.","note":"x=+-9 slip -> -9<x<9 -> 17 integers."},
     {"pattern":"notation","expect":7,"message":"The inequality is strict (\\(< 0\\)), so -3 and 3 are excluded. Including them (using \\(\\leq\\)) counts 7 integers, but only -2 to 2 belong.","note":"<= gives -3..3 = 7."}],
    [say("Factorise \\(x^2 - 9\\) as a difference of two squares: \\((x-3)(x+3)\\). Each bracket gives a root."),
     root_box(3), root_box(-3),
     say("For \\(< 0\\) the solution is between the roots: \\(-3 < x < 3\\). Count the whole numbers strictly between -3 and 3."),
     box("They are -2, -1, 0, 1, 2.  How many?  ", 5, "Count from -2 up to 2.", phase="substitute"),
     box("Check the endpoint x = 3:  3² - 9 = ", 0, "It equals 0, not below 0, so 3 is not counted.",
         done="Only -2 to 2 count: 5 integers.", phase="substitute")]))
# s5: x^2-8x+12<=0 upper roots 2,6
silver.append(P(
    "Solve \\(x^2 - 8x + 12 \\leq 0\\). Give the upper bound.", [6], "single_value",
    "Factorise; the upper bound is the larger root (inclusive).",
    [{"pattern":"wrong_region","expect":2,"message":mc_wrong_region_between("\\leq",2,6,2),"note":"Enters smaller root 2."},
     {"pattern":"wrong_roots","expect":-2,"message":mc_factoring("x^2 - 8x + 12","(x-2)(x-6)",2,6),"note":"(x+2)(x+6) sign slip gives roots -2,-6; upper bound -2."}],
    std_walk("x^2 - 8x + 12","+12","-8","-2 and -6",2,6,"\\leq","between","upper",6,"4","4² - 8(4) + 12",-4)))
# s6: x^2+5x+4<=0 lower roots -4,-1
silver.append(P(
    "Solve \\(x^2 + 5x + 4 \\leq 0\\). Give the lower bound.", [-4], "single_value",
    "Factorise; the lower bound is the smaller (more negative) root.",
    [{"pattern":"wrong_region","expect":-1,"message":mc_wrong_region_between("\\leq",-4,-1,-1),"note":"Enters larger root -1."},
     {"pattern":"wrong_roots","expect":1,"message":"Watch the signs: \\(x^2 + 5x + 4 = (x+4)(x+1)\\), so both roots are negative (-4 and -1). Reading the factor numbers as positive roots gives the wrong bound.","note":"Reads +4,+1 as positive roots; lower bound 1."}],
    std_walk("x^2 + 5x + 4","+4","+5","+4 and +1",-4,-1,"\\leq","between","lower",-4,"-2","(-2)² + 5(-2) + 4",-2)))

# --- GOLD ---
gold = []
# g0: 2x^2-5x-3>0 larger critical value 3  (roots -1/2, 3)
gold.append(P(
    "Solve \\(2x^2 - 5x - 3 > 0\\). Give the larger critical value.", [3], "single_value",
    "Split the middle term to factorise, then take the larger of the two roots.",
    [{"pattern":"wrong_roots","expect":1.5,"message":"Check the split. \\(2x^2 - 5x - 3 = (2x+1)(x-3)\\), with roots \\(-\\tfrac{1}{2}\\) and 3. Splitting the constant sign wrongly gives roots 1 and 1.5 and the wrong larger value.","note":"(x-1)(2x-3)=2x^2-5x+3 (wrong constant sign) -> roots 1, 1.5; larger 1.5."}],
    [say("With a 2 in front of \\(x^2\\), split the middle term. Two numbers multiply to \\((2)(-3) = -6\\) and add to -5: they are -6 and +1. Grouping gives \\(2x^2 - 6x + x - 3 = 2x(x-3) + (x-3) = (2x+1)(x-3)\\)."),
     box("From x - 3 = 0:  x = ", 3, "x = 3."),
     box("From 2x + 1 = 0, first 2x = ", -1, "Subtract 1 from both sides."),
     say("So the other root is \\(x = -1 \\div 2 = -0.5\\). The roots are -0.5 and 3. For \\(> 0\\) the U-shape is above the axis OUTSIDE the roots: \\(x < -0.5\\) or \\(x > 3\\)."),
     box("The larger critical value is  ", 3, "The larger of -0.5 and 3.", phase="substitute"),
     box("Check x = 4 (outside, to the right):  2(4²) - 5(4) - 3 = ", 9, "32 - 20 - 3. It should be above zero.",
         done="9 > 0, so the outside region is right; the larger critical value is 3.", phase="substitute")]))
# g1: 3x^2+x-2<=0 upper critical value as fraction 2/3 -> [2,3]  (roots -1, 2/3)
gold.append(P(
    "Solve \\(3x^2 + x - 2 \\leq 0\\). Give the upper critical value as a fraction.", [2,3], "fraction",
    "Split the middle term to factorise; the upper root is a fraction, so give its numerator and denominator.",
    [{"pattern":"wrong_region","expect":[-1,1],"message":"For \\(\\leq 0\\) the solution is between the roots, \\(-1 \\leq x \\leq \\tfrac{2}{3}\\), so the UPPER value is \\(\\tfrac{2}{3}\\). Entering the lower root -1 gives the wrong end of the interval.","note":"Picks lower root -1 as -1/1 = [-1,1]."}],
    [say("Split the middle term. Two numbers multiply to \\((3)(-2) = -6\\) and add to +1: they are +3 and -2. Grouping gives \\(3x^2 + 3x - 2x - 2 = 3x(x+1) - 2(x+1) = (3x-2)(x+1)\\)."),
     box("From x + 1 = 0:  x = ", -1, "x = -1."),
     box("From 3x - 2 = 0, first 3x = ", 2, "Add 2 to both sides."),
     say("So the second root is \\(x = 2 \\div 3 = \\tfrac{2}{3}\\). The roots are -1 and \\(\\tfrac{2}{3}\\). For \\(\\leq 0\\) the answer is between them: \\(-1 \\leq x \\leq \\tfrac{2}{3}\\), so the upper value is \\(\\tfrac{2}{3}\\)."),
     box("Enter the numerator of the upper value (two thirds):  ", 2, "The top of 2/3.", phase="substitute"),
     box("Enter its denominator:  ", 3, "The bottom of 2/3.", phase="substitute"),
     box("Check x = 0 (between the roots):  3(0²) + 0 - 2 = ", -2, "Only the constant is left. It should satisfy \\(\\leq 0\\).",
         done="-2 <= 0, so -1 <= x <= 2/3; the upper critical value is 2/3.", phase="substitute")]))
# g2: how many integers satisfy x^2-10x+16<0 => 5  (roots 2,8)
gold.append(P(
    "How many integers satisfy \\(x^2 - 10x + 16 < 0\\)?", [5], "single_value",
    "Factorise, then count the whole numbers strictly between the two roots.",
    [{"pattern":"wrong_roots","expect":0,"message":"\\(x^2 - 10x + 16\\) does not factorise to \\((x-4)^2\\). Its roots are 2 and 8. A perfect-square answer would wrongly give no solutions at all.","note":"(x-4)^2<0 has no solution -> counts 0."},
     {"pattern":"notation","expect":7,"message":"The inequality is strict (\\(< 0\\)), so the endpoints 2 and 8 are excluded. Including them (using \\(\\leq\\)) counts 7 integers, but only 3 to 7 belong.","note":"<= includes 2 and 8: 2..8 = 7."}],
    [say("Factorise \\(x^2 - 10x + 16\\). Two numbers multiply to +16 and add to -10: they are -2 and -8, giving \\((x-2)(x-8)\\)."),
     root_box(2), root_box(8),
     say("For \\(< 0\\) the solution is between the roots: \\(2 < x < 8\\). Count the whole numbers strictly between 2 and 8."),
     box("They are 3, 4, 5, 6, 7.  How many?  ", 5, "Count from 3 up to 7.", phase="substitute"),
     box("Check the endpoint x = 2:  2² - 10(2) + 16 = ", 0, "4 - 20 + 16. It equals 0, so 2 is not below the axis and is not counted.",
         done="Only 3 to 7 count: 5 integers.", phase="substitute")]))
# g3: MC perfect square
gold.append({
    "display": "Solve \\(x^2 + 2x + 1 > 0\\). Describe the solution.",
    "options": ["All real numbers", "All \\(x\\) except \\(x = -1\\)", "\\(x > -1\\)", "No solution"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "Try completing the square, then think about what a repeated root means for the graph.",
    "misconceptions": [
        {"pattern":"wrong_region","expect":0,"message":"A perfect square \\((x+1)^2\\) is never negative, but it does equal 0 at \\(x = -1\\). Since we need strictly \\(> 0\\), that single point is excluded, so it is not all real numbers.","note":"Confuses > with >= -> 'All real numbers'."},
        {"pattern":"forgot_sketch","expect":2,"message":"The U-shape touches the axis at \\(x = -1\\) and is above it on BOTH sides. The solution keeps every x except \\(x = -1\\), not just \\(x > -1\\).","note":"Applies outside-a-single-root rule -> x > -1 only."}]})
# g4: MC discriminant
gold.append({
    "display": "Find the range of \\(k\\) for which \\(x^2 + kx + 9 = 0\\) has no real roots.",
    "options": ["\\(-6 < k < 6\\)", "\\(k < 6\\)", "\\(-3 < k < 3\\)", "\\(k > -6\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "No real roots means the discriminant \\(b^2 - 4ac\\) is less than 0.",
    "misconceptions": [
        {"pattern":"wrong_region","expect":3,"message":"No real roots needs the discriminant \\(< 0\\), not \\(> 0\\). A positive discriminant gives two real roots. Solve \\(k^2 - 36 < 0\\) instead.","note":"Uses discriminant>0 -> k<-6 or k>6 -> picks 'k>-6'."},
        {"pattern":"wrong_roots","expect":2,"message":"The discriminant is \\(b^2 - 4ac = k^2 - 36\\). Check you used \\(4ac = 4 \\times 1 \\times 9 = 36\\), not 18.","note":"Uses 2ac=18 -> k^2<18 -> ~'-3<k<3'."},
        {"pattern":"notation","expect":1,"message":"\\(k^2 < 36\\) gives a symmetric range \\(-6 < k < 6\\). Do not drop the negative bound and write only \\(k < 6\\).","note":"Keeps only positive bound."}]})

# ================= TIER GUIDES =================
tier_guides = {
 "bronze": {
   "title": "Bronze: quadratic below zero, between the roots",
   "steps": [
     "Factorise the quadratic and set each bracket to zero to find the two roots.",
     "For \\(< 0\\), the U-shaped curve dips below the x-axis BETWEEN the roots, so the answer is \\(a < x < b\\).",
     "Read off the bound asked for: the lower bound is the smaller root, the upper bound is the larger root."],
   "example": {
     "question": "Solve \\(x^2 - 7x + 10 < 0\\). Give the lower bound.",
     "steps": [
       {"label":"Factorise","content":"\\((x-2)(x-5) = 0\\), so the roots are 2 and 5."},
       {"label":"Choose the region","content":"\\(< 0\\) means between the roots: \\(2 < x < 5\\)."},
       {"label":"Check","content":"At \\(x = 3\\): \\(9 - 21 + 10 = -2\\), which is below zero. Correct."},
       {"label":"Answer","content":"The lower bound is \\(2\\).","isAnswer":True,"is_answer":True}]}},
 "silver": {
   "title": "Silver: below and above zero, including \\(\\leq\\) and \\(\\geq\\)",
   "steps": [
     "Find the roots by factorising, exactly as in bronze.",
     "For \\(> 0\\) or \\(\\geq 0\\), the curve is above the axis OUTSIDE the roots: \\(x < a\\) or \\(x > b\\). For \\(< 0\\) or \\(\\leq 0\\) it is between them.",
     "Use \\(\\leq\\) or \\(\\geq\\) (a closed bound) when the inequality includes equals; otherwise use \\(<\\) or \\(>\\)."],
   "example": {
     "question": "Solve \\(x^2 + 2x - 15 > 0\\). Give the smaller critical value.",
     "steps": [
       {"label":"Factorise","content":"\\((x+5)(x-3) = 0\\), roots \\(-5\\) and \\(3\\)."},
       {"label":"Choose the region","content":"\\(> 0\\) means outside the roots: \\(x < -5\\) or \\(x > 3\\)."},
       {"label":"Check","content":"At \\(x = 4\\): \\(16 + 8 - 15 = 9 > 0\\). Correct."},
       {"label":"Answer","content":"The smaller critical value is \\(-5\\).","isAnswer":True,"is_answer":True}]}},
 "gold": {
   "title": "Gold: harder factorising, \\(a \\neq 1\\), reasoning about roots",
   "steps": [
     "When \\(x^2\\) has a coefficient, split the middle term to factorise; roots may be fractions.",
     "Pick the region as usual (between for \\(< 0\\), outside for \\(> 0\\)), then read off the value asked for.",
     "For a repeated root or a discriminant question, think about whether the curve touches or clears the axis."],
   "example": {
     "question": "Solve \\(2x^2 - x - 3 \\geq 0\\). Give the smaller critical value.",
     "steps": [
       {"label":"Split the middle term","content":"\\(2x^2 - x - 3 = (2x-3)(x+1)\\), roots \\(-1\\) and \\(\\tfrac{3}{2}\\)."},
       {"label":"Choose the region","content":"\\(\\geq 0\\) means outside the roots: \\(x \\leq -1\\) or \\(x \\geq \\tfrac{3}{2}\\)."},
       {"label":"Check","content":"At \\(x = 2\\): \\(8 - 2 - 3 = 3 \\geq 0\\). Correct."},
       {"label":"Answer","content":"The smaller critical value is \\(-1\\).","isAnswer":True,"is_answer":True}]}},
}

# ================= GUIDED (opener + teach) =================
opener = {
 "steps": [
   say("Here is a multiplying machine. It works out \\((x - 2) \\times (x - 3)\\). We want to know which values of x make the answer come out BELOW zero (negative). Let us test a few."),
   box("Try x = 5. First bracket:  5 - 2 = ", 3, "5 take away 2."),
   say("The second bracket is \\(5 - 3 = 2\\). Both are positive, so \\(3 \\times 2 = 6\\), above zero. Now slide x down to 2.5, in between the two numbers."),
   box("First bracket:  2.5 - 2 = ", 0.5, "2.5 take away 2."),
   box("Second bracket:  2.5 - 3 = ", -0.5, "2.5 is less than 3, so this drops below zero."),
   say("One bracket came out positive, the other negative, and a positive times a negative is always NEGATIVE. So the machine's answer is below zero, and that only happens when x sits BETWEEN 2 and 3. That is the whole method for a quadratic inequality: factorise to two brackets, find the two roots, and the expression is below zero between them, above zero outside them. In algebra, \\((x-2)(x-3) < 0\\) has the solution \\(2 < x < 3\\).")]
}

teach = {
 "bronze": {
   "display": "Solve \\(x^2 - 7x + 12 < 0\\)",
   "steps": [
     say("First factorise. We need two numbers that multiply to +12 and add to -7: they are -3 and -4, so \\(x^2 - 7x + 12 = (x-3)(x-4)\\). Each bracket gives a root."),
     box("The first bracket x - 3 is zero when x = ", 3, "x - 3 = 0."),
     box("The second bracket x - 4 is zero when x = ", 4, "x - 4 = 0."),
     say("So the curve crosses the x-axis at 3 and 4. It is a U-shape, so it dips BELOW the axis between the roots. That is where the expression is \\(< 0\\)."),
     box("The solution is 3 < x < 4. The lower bound is  ", 3, "The smaller of the two roots."),
     box("And the upper bound is  ", 4, "The larger of the two roots."),
     box("Check with x = 3.5, in the middle:  3.5² - 7(3.5) + 12 = ", -0.25, "12.25 - 24.5 + 12. It should be below zero.",
         done="Below zero, so 3 < x < 4 is right. Factorise, find the roots, take the region between them: that is the whole bronze move.")]},
 "silver": {
   "display": "Solve \\(x^2 - 2x - 15 \\geq 0\\)",
   "steps": [
     say("Factorise. Two numbers multiply to -15 and add to -2: they are -5 and +3, so \\(x^2 - 2x - 15 = (x-5)(x+3)\\)."),
     box("The bracket x - 5 is zero when x = ", 5, "x - 5 = 0."),
     box("The bracket x + 3 is zero when x = ", -3, "x + 3 = 0, so x is negative."),
     say("The roots are -3 and 5. This time the sign is \\(\\geq 0\\), so we want where the U-shape is ON or ABOVE the axis. That is OUTSIDE the roots, not between them."),
     box("The left piece is x \\(\\leq\\)  ", -3, "On or below the smaller root."),
     box("The right piece is x \\(\\geq\\)  ", 5, "On or above the larger root."),
     box("Check a value outside, x = 6:  6² - 2(6) - 15 = ", 9, "36 - 12 - 15. It should be zero or above.",
         done="Above zero, so the outside region is right. Taking OUTSIDE the roots for a \\(> 0\\) or \\(\\geq 0\\) sign is the new silver move.")]},
 "gold": {
   "display": "Solve \\(2x^2 + 5x - 3 < 0\\)",
   "steps": [
     say("With a 2 in front of \\(x^2\\), split the middle term. Two numbers multiply to \\((2)(-3) = -6\\) and add to +5: they are +6 and -1. Grouping gives \\(2x^2 + 6x - x - 3 = 2x(x+3) - (x+3) = (2x-1)(x+3)\\)."),
     box("From 2x - 1 = 0, first 2x = ", 1, "Add 1 to both sides."),
     box("So x = 1 ÷ 2 = ", 0.5, "Divide by 2; it is a fraction."),
     box("From x + 3 = 0:  x = ", -3, "x = -3."),
     say("The roots are -3 and 0.5. The sign is \\(< 0\\), so we want the U-shape BELOW the axis, which is BETWEEN the roots: \\(-3 < x < 0.5\\)."),
     box("The upper bound, as a decimal, is  ", 0.5, "The larger root, one half."),
     box("Check x = 0 (between the roots):  2(0²) + 5(0) - 3 = ", -3, "Everything with x vanishes, leaving the constant.",
         done="Below zero, so -3 < x < 0.5 is right. Splitting the middle term when \\(x^2\\) has a coefficient is the gold move.")]},
}

# ================= METHOD CARD (slim) =================
method_card = {
 "title": "Solving Quadratic Inequalities",
 "steps": [
   "Rearrange so one side is 0, then factorise the quadratic to find its two roots.",
   "Sketch the U-shape (positive \\(x^2\\)) crossing the x-axis at the roots.",
   "For \\(< 0\\) or \\(\\leq 0\\) take BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) take OUTSIDE the roots.",
   "Write the answer in inequality notation, using \\(\\leq\\) or \\(\\geq\\) when the inequality is inclusive."],
 "content": "<p>A <strong>quadratic inequality</strong> asks for which values of \\(x\\) a quadratic is above or below zero. Solve the matching equation for the roots, sketch the parabola, then read off the region.</p><p><strong>Below zero</strong> (\\(< 0\\), \\(\\leq 0\\)) sits between the roots; <strong>above zero</strong> (\\(> 0\\), \\(\\geq 0\\)) sits outside them. Use a closed bound for \\(\\leq\\) or \\(\\geq\\), an open bound for \\(<\\) or \\(>\\).</p>",
 "example": "<p><strong>Solve</strong> \\(x^2 - 3x - 4 > 0\\).</p><p>\\((x-4)(x+1) = 0\\) gives roots \\(-1\\) and \\(4\\). The U-shape is above zero outside the roots, so \\(x < -1\\) or \\(x > 4\\).</p>"
}

# ================= ASSEMBLE =================
pd = dict(live)  # preserve related_videos, topic_links, worked_examples
pd["method_card"] = method_card
pd["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Quadratic < 0 (between roots) with easy factorisation",
  "silver_description": "Both < 0 and > 0, including ≤ and ≥",
  "gold_description": "Harder factorisations, a ≠ 1, reasoning about roots",
}
pd["tier_guides"] = tier_guides
pd["guided"] = {"opener": opener, "teach": teach}

# fix em dashes in preserved worked_examples labels
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------- SELF VERIFICATION ----------
errors = []
def solve_quad(a,b,c):
    import math
    d=b*b-4*a*c
    if d<0: return []
    r=math.sqrt(d)
    return sorted(set([(-b+r)/(2*a),(-b-r)/(2*a)]))

# check each check-box arithmetic already embedded; recompute a few key ones
checks = {
 "b0":(1,-4,3,2), "b1":(1,-6,8,3), "b3":(1,-1,-2,0), "b4":(1,-10,24,5),
 "b5":(1,-4,-21,0), "b6":(1,2,-8,0), "b7":(1,-3,-10,0),
 "s1":(1,1,-6,0), "s3":(1,3,-4,2), "s5":(1,-8,12,4), "s6":(1,5,4,-2),
 "g0":(2,-5,-3,4), "g1":(3,1,-2,0), "g2":(1,-10,16,2),
}
expect_check = {"b0":-1,"b1":-1,"b3":-2,"b4":-1,"b5":-21,"b6":-8,"b7":-10,
 "s1":-6,"s3":6,"s5":-4,"s6":-2,"g0":9,"g1":-2,"g2":0}
for k,(a,b,c,x) in checks.items():
    v=a*x*x+b*x+c
    if v!=expect_check[k]: errors.append("check %s = %s expected %s"%(k,v,expect_check[k]))

# no em dash scan
def scan(o,p):
    if isinstance(o,dict):
        for kk,vv in o.items():
            if kk in ("note","guided_skip_reason"): continue
            scan(vv,p+"."+str(kk))
    elif isinstance(o,list):
        for i,vv in enumerate(o): scan(vv,p+"[%d]"%i)
    elif isinstance(o,str) and "—" in o:
        errors.append("EM DASH at %s"%p)
scan(pd,"pd")

# expect != solution and completion boundaries
pb=pd["problem_bank"]
for t in ("bronze","silver","gold"):
    seen=set()
    for i,pr in enumerate(pb[t]):
        sols=tuple(pr["solutions"])
        if sols in seen and pr.get("input_type")!="multiple_choice":
            errors.append("dup solution %s %d %s"%(t,i,sols))
        seen.add(sols)
        gs=pr.get("guided_steps")
        if gs:
            live_after=0; sub=None
            for j,st in enumerate(gs):
                if st.get("phase")=="substitute" and sub is None: sub=j
            if sub is None: errors.append("no substitute %s %d"%(t,i))
            else:
                live_after=sum(1 for st in gs[sub:] if st.get("answer") is not None)
                if live_after<2: errors.append("<2 live after boundary %s %d"%(t,i))
                before=sum(1 for st in gs[:sub] if st.get("answer") is not None)
                if before<1: errors.append("0 boxes before boundary %s %d"%(t,i))

if errors:
    print("VERIFY ERRORS:")
    for e in errors: print("  -",e)
else:
    print("SELF-VERIFY OK")

json.dump(pd, io.open("lesson_algebra-L12.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_algebra-L12.json")
