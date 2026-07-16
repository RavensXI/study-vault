# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for ratio-proportion-L05 (Proportion
Equations & Powers). Every box value is computed here and asserted against the
stored solution, so the arithmetic cannot drift."""
import json, io, math

LIVE = "_live_L05.json"
OUT  = "lesson_ratio-proportion-L05.json"

live = json.load(io.open(LIVE, encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None:  d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d

def say(text):
    return {"say": text}

# ---- guided_steps generators (each returns steps + the solution it must hit) ----

def g_find_k_square(x0, y0, k):
    s = x0*x0
    assert y0 == k*s, (y0, k, s)
    return [
        say("Turn the proportion into an equation. \\(y \\propto x^2\\) means \\(y = kx^2\\), where \\(k\\) is a fixed multiplier we must find."),
        box("Square the known x first: %d² = " % x0, s, "%d times %d." % (x0, x0)),
        box("Now %d = k × %d, so k = %d ÷ %d = " % (y0, s, y0, s), k, "Divide y by the squared value.", phase="substitute",
            say="So %d = k × %d." % (y0, s)),
        box("Check: k × %d² = %d × %d = " % (x0, k, s), y0, "%d times %d." % (k, s), phase="substitute",
            done="That gives back y = %d, so k = %d is right." % (y0, k)),
    ], k

def g_find_k_root(x0, y0, k):
    r = int(round(math.isqrt(x0)))
    assert r*r == x0 and y0 == k*r, (x0, r, y0, k)
    return [
        say("Turn the proportion into an equation. \\(y \\propto \\sqrt{x}\\) means \\(y = k\\sqrt{x}\\)."),
        box("Square-root the known x first: √%d = " % x0, r, "What number squares to %d?" % x0),
        box("Now %d = k × %d, so k = %d ÷ %d = " % (y0, r, y0, r), k, "Divide y by the square root.", phase="substitute",
            say="So %d = k × %d." % (y0, r)),
        box("Check: k × √%d = %d × %d = " % (x0, k, r), y0, "%d times %d." % (k, r), phase="substitute",
            done="That returns y = %d, so k = %d is right." % (y0, k)),
    ], k

def g_sub_square(a, x1):
    s = x1*x1; res = a*s
    return [
        say("The rule is already complete: \\(y = %dx^2\\). Put x = %d in, and square the x first." % (a, x1)),
        box("%d² = " % x1, s, "%d times %d." % (x1, x1)),
        box("y = %d × %d = " % (a, s), res, "%d times %d." % (a, s), phase="substitute", say="Now multiply by %d." % a),
        box("Check by dividing back: %d ÷ %d = " % (res, s), a, "Undo the multiply to make sure.", phase="substitute",
            done="That returns the coefficient %d, so y = %d is right." % (a, res)),
    ], res

def g_sub_cube(a, x1):
    c = x1**3; res = a*c
    return [
        say("The rule is \\(y = %dx^3\\). Cube the x first: that is x × x × x." % a),
        box("%d³ = " % x1, c, "%d × %d × %d." % (x1, x1, x1)),
        box("y = %d × %d = " % (a, c), res, "%d times %d." % (a, c), phase="substitute", say="Now multiply by %d." % a),
        box("Check by dividing back: %d ÷ %d = " % (res, c), a, "Undo the multiply.", phase="substitute",
            done="That returns the coefficient %d, so y = %d is right." % (a, res)),
    ], res

def g_sub_root(a, x1):
    r = int(math.isqrt(x1)); assert r*r == x1
    res = a*r
    return [
        say("The rule is \\(y = %d\\sqrt{x}\\). Square-root the x first." % a),
        box("√%d = " % x1, r, "What number squares to %d?" % x1),
        box("y = %d × %d = " % (a, r), res, "%d times %d." % (a, r), phase="substitute", say="Now multiply by %d." % a),
        box("Check by dividing back: %d ÷ %d = " % (res, a), r, "Undo the multiply.", phase="substitute",
            done="That returns √%d = %d, so y = %d is right." % (x1, r, res)),
    ], res

def g_sub_inverse(c, x1):
    res = c // x1; assert res*x1 == c
    return [
        say("This is inverse proportion: \\(y = \\frac{%d}{x}\\). The constant %d is the product x × y and never changes." % (c, c)),
        box("Write down the fixed constant. Here it is given as k = ", c, "It is the number on top of the fraction."),
        box("y = %d ÷ %d = " % (c, x1), res, "How many %ds go into %d?" % (x1, c), phase="substitute", say="Now divide the constant by the new x."),
        box("Check the constant: %d × %d = " % (x1, res), c, "Multiply x by y.", phase="substitute",
            done="That returns k = %d, so y = %d is right." % (c, res)),
    ], res

def g_reverse_square(a, Y):
    s = Y // a; assert s*a == Y
    x = int(math.isqrt(s)); assert x*x == s
    return [
        say("The rule is \\(y = %dx^2\\) and we know y = %d. Undo the %d first." % (a, Y, a)),
        box("%d ÷ %d = " % (Y, a), s, "How many %ds go into %d?" % (a, Y)),
        box("So x² = %d. Take the square root: x = √%d = " % (s, s), x, "What number squares to %d?" % s, phase="substitute",
            say="Now undo the square by rooting."),
        box("Check: %d × %d² = %d × %d = " % (a, x, a, s), Y, "%d times %d." % (a, s), phase="substitute",
            done="That gives back y = %d, so x = %d is right." % (Y, x)),
    ], x

def g_prop_square_findy(x0, y0, x1):
    s0 = x0*x0; k = y0 // s0; assert k*s0 == y0
    s1 = x1*x1; res = k*s1
    return [
        say("First find k. \\(y \\propto x^2\\) means \\(y = kx^2\\). Square the known x."),
        box("%d² = " % x0, s0, "%d squared." % x0),
        box("k = %d ÷ %d = " % (y0, s0), k, "Divide y by the squared value.", say="So %d = k × %d." % (y0, s0)),
        box("%d² = " % x1, s1, "%d squared." % x1, phase="substitute", say="The rule is y = %dx². Now use the new x = %d, squared." % (k, x1)),
        box("y = %d × %d = " % (k, s1), res, "%d times %d." % (k, s1), phase="substitute"),
        box("Check the rule on the first pair: %d × %d² = " % (k, x0), y0, "%d times %d." % (k, s0), phase="substitute",
            done="That matches the given y = %d, so k = %d is correct and y = %d stands." % (y0, k, res)),
    ], res

def g_prop_root_findy(x0, y0, x1):
    r0 = int(math.isqrt(x0)); assert r0*r0 == x0
    k = y0 // r0; assert k*r0 == y0
    r1 = int(math.isqrt(x1)); assert r1*r1 == x1
    res = k*r1
    return [
        say("First find k. \\(y = k\\sqrt{x}\\). Square-root the known x."),
        box("√%d = " % x0, r0, "What squares to %d?" % x0),
        box("k = %d ÷ %d = " % (y0, r0), k, "Divide y by the root.", say="So %d = k × %d." % (y0, r0)),
        box("√%d = " % x1, r1, "What squares to %d?" % x1, phase="substitute", say="The rule is y = %d√x. New x = %d." % (k, x1)),
        box("y = %d × %d = " % (k, r1), res, "%d times %d." % (k, r1), phase="substitute"),
        box("Check on the first pair: %d × √%d = %d × %d = " % (k, x0, k, r0), y0, "%d times %d." % (k, r0), phase="substitute",
            done="That matches the given y = %d, so y = %d stands." % (y0, res)),
    ], res

def g_prop_inverse_findy(x0, y0, x1):
    k = x0*y0; res = k // x1; assert res*x1 == k
    return [
        say("Inverse proportion: \\(y = \\frac{k}{x}\\), so k = x × y. Find k from the known pair."),
        box("k = %d × %d = " % (x0, y0), k, "Multiply the pair together."),
        box("y = %d ÷ %d = " % (k, x1), res, "How many %ds go into %d?" % (x1, k), phase="substitute",
            say="The rule is y = %d ÷ x. New x = %d." % (k, x1)),
        box("Check the constant: %d × %d = " % (x1, res), k, "Multiply x by y.", phase="substitute",
            done="That returns k = %d, so y = %d is right." % (k, res)),
    ], res

def g_prop_cube_findy(x0, y0, x1):
    c0 = x0**3; k = y0 // c0; assert k*c0 == y0
    c1 = x1**3; res = k*c1
    return [
        say("Cube proportion: \\(y = kx^3\\). Cube the known x."),
        box("%d³ = " % x0, c0, "%d × %d × %d." % (x0, x0, x0)),
        box("k = %d ÷ %d = " % (y0, c0), k, "Divide y by the cubed value.", say="So %d = k × %d." % (y0, c0)),
        box("%d³ = " % x1, c1, "%d cubed." % x1, phase="substitute", say="The rule is y = %dx³. New x = %d, cubed." % (k, x1)),
        box("y = %d × %d = " % (k, c1), res, "%d times %d." % (k, c1), phase="substitute"),
        box("Check on the first pair: %d × %d³ = %d × %d = " % (k, x0, k, c0), y0, "%d times %d." % (k, c0), phase="substitute",
            done="That matches the given y = %d, so y = %d stands." % (y0, res)),
    ], res

def g_prop_invsquare_findy(x0, y0, x1):
    s0 = x0*x0; k = y0*s0
    s1 = x1*x1; res = k / s1
    if float(res).is_integer(): res = int(res)
    return [
        say("Inverse square: \\(y = \\frac{k}{x^2}\\), so k = y × x². Square the known x."),
        box("%d² = " % x0, s0, "%d squared." % x0),
        box("k = %d × %d = " % (y0, s0), k, "Multiply y by the squared value.", say="So the constant is k."),
        box("%d² = " % x1, s1, "%d squared." % x1, phase="substitute", say="The rule is y = %d ÷ x². New x = %d, squared." % (k, x1)),
        box("y = %d ÷ %d = " % (k, s1), res, "%d divided by %d." % (k, s1), phase="substitute"),
        box("Check: %s × %d² = %s × %d = " % (str(res), x0, str(res), s0), k, "y times x squared returns k.", phase="substitute",
            done="That returns k = %d, so y = %s is right." % (k, str(res))),
    ], res

def g_prop_invroot_findy(x0, y0, x1):
    r0 = int(math.isqrt(x0)); assert r0*r0 == x0
    k = y0*r0
    r1 = int(math.isqrt(x1)); assert r1*r1 == x1
    res = k // r1; assert res*r1 == k
    return [
        say("Inverse root: \\(y = \\frac{k}{\\sqrt{x}}\\), so k = y × √x. Square-root the known x."),
        box("√%d = " % x0, r0, "What squares to %d?" % x0),
        box("k = %d × %d = " % (y0, r0), k, "Multiply y by the root.", say="So the constant is k."),
        box("√%d = " % x1, r1, "What squares to %d?" % x1, phase="substitute", say="The rule is y = %d ÷ √x. New x = %d." % (k, x1)),
        box("y = %d ÷ %d = " % (k, r1), res, "How many %ds go into %d?" % (r1, k), phase="substitute"),
        box("Check: %d × √%d = %d × %d = " % (res, x0, res, r0), k, "y times the root returns k.", phase="substitute",
            done="That returns k = %d, so y = %d is right." % (k, res)),
    ], res

def g_prop_square_reverse(x0, y0, Y):
    s0 = x0*x0; k = y0 // s0; assert k*s0 == y0
    s = Y // k; assert s*k == Y
    x = int(math.isqrt(s)); assert x*x == s
    return [
        say("First find k. \\(y = kx^2\\). Square the known x."),
        box("%d² = " % x0, s0, "%d squared." % x0),
        box("k = %d ÷ %d = " % (y0, s0), k, "Divide y by the squared value."),
        box("%d ÷ %d = " % (Y, k), s, "How many %ds go into %d?" % (k, Y), phase="substitute",
            say="The rule is y = %dx². Now y = %d, so %d = %dx². Undo the %d." % (k, Y, Y, k, k)),
        box("So x² = %d, and x = √%d = " % (s, s), x, "What squares to %d?" % s, phase="substitute"),
        box("Check: %d × %d² = %d × %d = " % (k, x, k, s), Y, "%d times %d." % (k, s), phase="substitute",
            done="That gives back y = %d, so x = %d is right." % (Y, x)),
    ], x

def g_prop_cube_reverse(x0, y0, Y):
    c0 = x0**3; k = y0 // c0; assert k*c0 == y0
    c = Y // k; assert c*k == Y
    x = round(c ** (1/3.))
    assert x**3 == c
    return [
        say("First find k. \\(y = kx^3\\). Cube the known x."),
        box("%d³ = " % x0, c0, "%d cubed." % x0),
        box("k = %d ÷ %d = " % (y0, c0), k, "Divide y by the cubed value."),
        box("%d ÷ %d = " % (Y, k), c, "How many %ds go into %d?" % (k, Y), phase="substitute",
            say="The rule is y = %dx³. Now y = %d, so %d = %dx³. Undo the %d." % (k, Y, Y, k, k)),
        box("So x³ = %d. Take the cube root: x = " % c, x, "What cubes to %d? Try %d × %d × %d." % (c, x, x, x), phase="substitute"),
        box("Check: %d × %d³ = %d × %d = " % (k, x, k, c), Y, "%d times %d." % (k, c), phase="substitute",
            done="That gives back y = %d, so x = %d is right." % (Y, x)),
    ], x

def g_prop_root_reverse_dec(x0, y0, Y, var_y="T", var_x="L"):
    # T = k sqrt(L); k may be decimal
    r0 = int(math.isqrt(x0)); assert r0*r0 == x0
    k = y0 / r0
    root = Y / k
    x = round(root*root)
    kdisp = ("%g" % k)
    assert abs(k*math.sqrt(x) - Y) < 1e-9
    return [
        say("First find k. \\(%s = k\\sqrt{%s}\\). Square-root the known %s." % (var_y, var_x, var_x)),
        box("√%d = " % x0, r0, "What squares to %d?" % x0),
        box("k = %g ÷ %d = " % (y0, r0), k, "Divide %s by the root." % var_y),
        box("%g ÷ %s = " % (Y, kdisp), round(root), "How many %ss go into %g? Think %g ÷ %s = %d ÷ %d." % (kdisp, Y, Y, kdisp, int(Y*10), int(k*10)), phase="substitute",
            say="The rule is %s = %s√%s. Now %s = %g, so %g = %s√%s. Undo the %s." % (var_y, kdisp, var_x, var_y, Y, Y, kdisp, var_x, kdisp)),
        box("So √%s = %d. Square it: %s = %d² = " % (var_x, round(root), var_x, round(root)), x, "%d squared." % round(root), phase="substitute"),
        box("Check: %s × √%d = %s × %d = " % (kdisp, x, kdisp, round(root)), round(Y) if float(Y).is_integer() else Y, "%s times %d." % (kdisp, round(root)), phase="substitute",
            done="That gives back %s = %g, so %s = %d is right." % (var_y, Y, var_x, x)),
    ], x

# ---------------- assemble problem bank ----------------

def mis(pattern, check, expect, message, note):
    return {"pattern": pattern, "check": check, "expect": expect, "message": message, "note": note}

bank = {"bronze": [], "silver": [], "gold": []}

def add(tier, display, sol, hint, misc, gen, calc=False, it="single_value", options=None):
    prob = {"display": display, "solutions": [sol], "calculator": calc,
            "input_type": it, "hint": hint, "misconceptions": misc}
    if options is not None:
        prob["options"] = options
    if gen is not None:
        steps, landed = gen
        assert landed == sol or abs(float(landed)-float(sol)) < 1e-9, (display, landed, sol)
        prob["guided_steps"] = steps
    bank[tier].append(prob)

# --- BRONZE ---
add("bronze", "\\(y \\propto x^2\\). When \\(x = 2\\), \\(y = 12\\). Find \\(k\\).", 3,
    "Square the x value, then divide y by it to get k.",
    [mis("wrong_formula","common",6,
      "Dividing y by x gives 12 ÷ 2 = 6, but the rule is \\(y = kx^2\\), not \\(y = kx\\). Divide by x squared instead: 12 ÷ 4 = 3.",
      "Student treats as y = kx (direct, not squared): k = 12 / 2 = 6.")],
    g_find_k_square(2,12,3))

add("bronze", "\\(y = 5x^2\\). Find \\(y\\) when \\(x = 3\\).", 45,
    "Square the x first, then multiply by 5.",
    [mis("wrong_formula","common",15,
      "5 × 3 = 15 skips the square. In \\(y = 5x^2\\) you square the x first: \\(3^2 = 9\\), then 5 × 9 = 45.",
      "Student computes 5 × 3 = 15 (forgets to square x first).")],
    g_sub_square(5,3))

add("bronze", "\\(y = 2x^3\\). Find \\(y\\) when \\(x = 3\\).", 54,
    "Cube the x (x times x times x), then multiply by 2.",
    [mis("wrong_formula","common",18,
      "Squaring gives \\(3^2 = 9\\) and 2 × 9 = 18, but this is \\(x^3\\). Cube the x: \\(3^3 = 27\\), then 2 × 27 = 54.",
      "Student uses x squared instead of x cubed: 2 × 9 = 18.")],
    g_sub_cube(2,3))

add("bronze", "\\(y \\propto \\sqrt{x}\\). When \\(x = 16\\), \\(y = 20\\). Find \\(k\\).", 5,
    "Square-root the x value, then divide y by it to get k.",
    [mis("wrong_formula","common",1.25,
      "Dividing y by x gives 20 ÷ 16 = 1.25, but the rule is \\(y = k\\sqrt{x}\\). Divide by the square root instead: 20 ÷ 4 = 5.",
      "Student treats as y = kx: k = 20 / 16 = 1.25.")],
    g_find_k_root(16,20,5))

add("bronze", "\\(y = 4\\sqrt{x}\\). Find \\(y\\) when \\(x = 9\\).", 12,
    "Square-root the x first, then multiply by 4.",
    [mis("wrong_formula","common",36,
      "4 × 9 = 36 uses x itself, but the rule is \\(y = 4\\sqrt{x}\\). Root the x first: \\(\\sqrt{9} = 3\\), then 4 × 3 = 12.",
      "Student forgets the root and computes 4 × 9 = 36.")],
    g_sub_root(4,9))

add("bronze", "\\(y = \\frac{48}{x}\\). Find \\(y\\) when \\(x = 6\\).", 8,
    "Divide 48 by x.",
    [mis("wrong_formula","common",288,
      "48 × 6 = 288 multiplies when you should divide. \\(y = \\frac{48}{x}\\) means 48 ÷ 6 = 8.",
      "Student multiplies instead of divides: 48 × 6 = 288.")],
    g_sub_inverse(48,6))

add("bronze", "\\(y = 7x^2\\). Find \\(x\\) when \\(y = 112\\).", 4,
    "Divide y by 7, then square-root to get x.",
    [mis("wrong_formula","common",16,
      "\\(x^2 = 16\\) is only halfway. You still need x, so take the square root: \\(\\sqrt{16} = 4\\).",
      "Student stops at x squared = 16 and gives 16 (forgets to square root).")],
    g_reverse_square(7,112))

add("bronze", "\\(y \\propto x^2\\). When \\(x = 1\\), \\(y = 6\\). Find \\(y\\) when \\(x = 4\\).", 96,
    "Find k by dividing y by x squared, then use k with the new x squared.",
    [mis("wrong_formula","common",24,
      "The x went up 4 times, but y does not scale the same way in a square law. \\(k = 6\\), so \\(y = 6 \\times 4^2 = 6 \\times 16 = 96\\), not 6 × 4 = 24.",
      "Student scales linearly: 6 × 4 = 24 (ignores squaring).")],
    g_prop_square_findy(1,6,4))

# --- SILVER ---
add("silver", "\\(y \\propto x^2\\). When \\(x = 3\\), \\(y = 27\\). Find \\(y\\) when \\(x = 7\\).", 147,
    "Find k first, then multiply k by the new x squared.",
    [mis("wrong_formula","common",63,
      "Scaling y in the same ratio as x gives \\(27 \\times \\frac{7}{3} = 63\\), but \\(y \\propto x^2\\). Find k = 3, then \\(y = 3 \\times 7^2 = 147\\).",
      "Student scales linearly (treats as direct proportion): 27 x 7/3 = 63.")],
    g_prop_square_findy(3,27,7))

add("silver", "\\(y \\propto \\sqrt{x}\\). When \\(x = 25\\), \\(y = 15\\). Find \\(y\\) when \\(x = 64\\).", 24,
    "Find k by dividing y by the square root of x, then use the new x.",
    [mis("wrong_formula","common",38.4,
      "Treating it as \\(y \\propto x\\) gives k = 0.6 and 0.6 × 64 = 38.4. It is a square-root law: k = 15 ÷ 5 = 3, so \\(y = 3 \\times 8 = 24\\).",
      "Student treats as direct proportion: k = 15/25 = 0.6, y = 0.6 x 64 = 38.4.")],
    g_prop_root_findy(25,15,64))

add("silver", "\\(y \\propto \\frac{1}{x}\\). When \\(x = 4\\), \\(y = 10\\). Find \\(y\\) when \\(x = 8\\).", 5,
    "Multiply x and y to get k, then divide k by the new x.",
    [mis("inverse_error","common",20,
      "Direct proportion would give k = 2.5 and 2.5 × 8 = 20, but this is inverse. Use k = x × y = 40, so \\(y = 40 \\div 8 = 5\\).",
      "Student treats as direct proportion: k = 10/4 = 2.5, y = 2.5 x 8 = 20.")],
    g_prop_inverse_findy(4,10,8))

add("silver", "\\(y \\propto x^2\\). When \\(x = 4\\), \\(y = 48\\). Find \\(x\\) when \\(y = 108\\).", 6,
    "Find k, divide y by k, then square-root for x.",
    [mis("wrong_formula","common",36,
      "\\(x^2 = 36\\) is not the answer. Square-root it: \\(x = \\sqrt{36} = 6\\).",
      "Student stops at x squared = 36 and gives 36 (forgets to square root).")],
    g_prop_square_reverse(4,48,108))

add("silver", "\\(y \\propto x^3\\). When \\(x = 2\\), \\(y = 40\\). Find \\(y\\) when \\(x = 3\\).", 135,
    "Cube the x to find k, then use k with the new x cubed.",
    [mis("wrong_formula","common",90,
      "Using \\(x^2\\) gives k = 10 and 10 × 9 = 90, but the power is 3. Cube it: k = 40 ÷ 8 = 5, so \\(y = 5 \\times 27 = 135\\).",
      "Student uses x squared instead of x cubed: k = 40/4 = 10, y = 10 x 9 = 90.")],
    g_prop_cube_findy(2,40,3))

add("silver", "\\(y \\propto \\frac{1}{x^2}\\). When \\(x = 2\\), \\(y = 5\\). Find \\(y\\) when \\(x = 5\\).", 0.8,
    "Multiply y by x squared to get k, then divide k by the new x squared.",
    [mis("wrong_formula","common",2,
      "Using \\(\\frac{1}{x}\\) gives k = 10 and 10 ÷ 5 = 2. It is an inverse square: k = 5 × 4 = 20, so \\(y = 20 \\div 25 = 0.8\\).",
      "Student uses 1/x instead of 1/x squared: k = 5 x 2 = 10, y = 10/5 = 2.")],
    g_prop_invsquare_findy(2,5,5))

add("silver", "\\(y \\propto \\sqrt{x}\\). When \\(x = 4\\), \\(y = 10\\). Find \\(x\\) when \\(y = 25\\).", 25,
    "Find k, divide y by k to get the root, then square it for x.",
    [mis("wrong_formula","common",5,
      "\\(\\sqrt{x} = 5\\) is only halfway. Square both sides to get x: \\(x = 5^2 = 25\\).",
      "Student stops at root x = 5 and gives x = 5 (forgets to square).")],
    g_prop_root_reverse_dec(4,10,25,var_y="y",var_x="x"))

# --- GOLD ---
add("gold", "\\(y \\propto \\frac{1}{x^2}\\). When \\(x = 3\\), \\(y = 4\\). Find \\(y\\) when \\(x = 6\\).", 1,
    "Multiply y by x squared to get k, then divide by the new x squared.",
    [mis("wrong_formula","common",2,
      "Using \\(\\frac{1}{x}\\) gives k = 12 and 12 ÷ 6 = 2, but this is an inverse square. k = 4 × 9 = 36, so \\(y = 36 \\div 36 = 1\\).",
      "Student uses 1/x instead of 1/x squared: k = 4 x 3 = 12, y = 12/6 = 2.")],
    g_prop_invsquare_findy(3,4,6))

add("gold", "\\(y \\propto x^3\\). When \\(x = 2\\), \\(y = 24\\). Find \\(x\\) when \\(y = 192\\).", 4,
    "Cube the x to find k, divide y by k, then take the cube root.",
    [mis("wrong_formula","common",64,
      "\\(x^3 = 64\\) is not x. Take the cube root: \\(x = \\sqrt[3]{64} = 4\\).",
      "Student stops at x cubed = 64 and gives 64 (forgets the cube root).")],
    g_prop_cube_reverse(2,24,192))

add("gold", "The surface area \\(A\\) of a sphere is proportional to \\(r^2\\). When \\(r = 3\\), \\(A = 36\\pi\\). Find \\(A\\) when \\(r = 5\\).", 0,
    "Find k as a multiple of π, then multiply by the new radius squared.",
    [mis("wrong_formula","common",None,
      "Find k from the known pair: k = 36π ÷ 3² = 4π. Then \\(A = 4\\pi \\times 5^2 = 100\\pi\\). Using \\(A = \\pi r^2\\) with no constant would give 25π, which ignores the given pair.",
      "Most natural numeric error (k = 36pi/3 = 12pi, A = 60pi) matches no option, so no determinate wrong option exists.")],
    None, it="multiple_choice",
    options=["\\(100\\pi\\)","\\(50\\pi\\)","\\(25\\pi\\)","\\(125\\pi\\)"])

add("gold", "\\(T \\propto \\sqrt{L}\\). When \\(L = 4\\), \\(T = 1.2\\). Find \\(L\\) when \\(T = 3\\).", 25,
    "Square-root L to find k, divide T by k, then square the result for L.",
    [mis("wrong_formula","common",5,
      "\\(\\sqrt{L} = 5\\) is only the root of L. Square it to get L itself: \\(L = 5^2 = 25\\).",
      "Student stops at root L = 5 and gives L = 5 (forgets to square).")],
    g_prop_root_reverse_dec(4,1.2,3,var_y="T",var_x="L"))

add("gold", "\\(y \\propto \\frac{1}{\\sqrt{x}}\\). When \\(x = 9\\), \\(y = 4\\). Find \\(y\\) when \\(x = 36\\).", 2,
    "Multiply y by the square root of x to get k, then divide by the new root.",
    [mis("wrong_formula","common",1,
      "Using x instead of \\(\\sqrt{x}\\) gives k = 4 × 9 = 36 and 36 ÷ 36 = 1. Root it: k = 4 × 3 = 12, so \\(y = 12 \\div 6 = 2\\).",
      "Student uses x instead of root x: k = 4 x 9 = 36, y = 36/36 = 1.")],
    g_prop_invroot_findy(9,4,36))

# ---------------- tier guides ----------------
def ex_step(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans:
        d["isAnswer"] = True; d["is_answer"] = True
    return d

tier_guides = {
 "bronze": {
   "title": "Bronze: find k, then substitute",
   "steps": [
     "Change the proportion into an equation with a multiplier \\(k\\): \\(y \\propto x^2\\) becomes \\(y = kx^2\\), and \\(y \\propto \\sqrt{x}\\) becomes \\(y = k\\sqrt{x}\\).",
     "Put in the pair you are given and solve for \\(k\\) in one step. Square or root the \\(x\\) value first, then divide.",
     "With \\(k\\) known the equation is complete: substitute the new value to read off \\(y\\), and check it reproduces the pair you started with."
   ],
   "example": {
     "question": "y ∝ x². When x = 2, y = 12. Find k.",
     "steps": [
       ex_step("Equation", "<p>\\(y \\propto x^2\\) becomes \\(y = kx^2\\).</p>"),
       ex_step("Square x", "<p>\\(2^2 = 4\\).</p>"),
       ex_step("Find k", "<p>\\(12 = k \\times 4\\), so \\(k = 3\\).</p>"),
       ex_step("Check", "<p>\\(3 \\times 2^2 = 12\\) ✓</p>"),
       ex_step("Answer", "<p>\\(k = 3\\)</p>", ans=True),
     ]
   }
 },
 "silver": {
   "title": "Silver: roots, inverses and working backwards",
   "steps": [
     "Same start: write \\(y = kx^2\\), \\(y = k\\sqrt{x}\\), \\(y = \\frac{k}{x}\\) or \\(y = \\frac{k}{x^2}\\), then find \\(k\\) from the known pair.",
     "To find \\(y\\), substitute the new \\(x\\). To find \\(x\\), put in the known \\(y\\), divide by \\(k\\), then take the square root last.",
     "That final root is the step students forget. Always check your answer back in the original equation."
   ],
   "example": {
     "question": "y ∝ √x. When x = 25, y = 15. Find y when x = 64.",
     "steps": [
       ex_step("Find k", "<p>\\(k = 15 \\div \\sqrt{25} = 15 \\div 5 = 3\\).</p>"),
       ex_step("New value", "<p>\\(y = 3\\sqrt{64} = 3 \\times 8\\).</p>"),
       ex_step("Check", "<p>\\(3 \\times \\sqrt{25} = 15\\) ✓</p>"),
       ex_step("Answer", "<p>\\(y = 24\\)</p>", ans=True),
     ]
   }
 },
 "gold": {
   "title": "Gold: multi-step powers and real contexts",
   "steps": [
     "Gold mixes inverse squares \\(y = \\frac{k}{x^2}\\), cubes \\(y = kx^3\\) and inverse roots \\(y = \\frac{k}{\\sqrt{x}}\\), sometimes dressed as a real formula such as a surface area or a pendulum.",
     "The method never changes: find \\(k\\) from the known pair, then substitute. Working backwards needs a cube root or a square, applied last.",
     "Spot which quantity plays the part of \\(y\\) and which plays \\(x\\), follow the same three steps, and check in the original."
   ],
   "example": {
     "question": "y ∝ 1/x². When x = 3, y = 4. Find y when x = 6.",
     "steps": [
       ex_step("Find k", "<p>\\(k = y \\times x^2 = 4 \\times 9 = 36\\).</p>"),
       ex_step("New value", "<p>\\(y = 36 \\div 6^2 = 36 \\div 36\\).</p>"),
       ex_step("Check", "<p>\\(1 \\times 3^2 = 9\\) and \\(36 \\div 9 = 4\\) ✓</p>"),
       ex_step("Answer", "<p>\\(y = 1\\)</p>", ans=True),
     ]
   }
 }
}

# ---------------- guided opener + teach ----------------
guided = {
 "opener": {
   "label": "Before any algebra",
   "display": "A square lawn 3 m on each side needs 9 m² of turf.<br>You want a bigger square lawn, 6 m on each side.",
   "steps": [
     box("A 6 m square is 6 rows of 6. Turf needed = 6 × 6 = ", 36, "Six sixes.",
         say="No algebra, just picture the squares."),
     box("Check the pattern on a 5 m square: 5 × 5 = ", 25, "Five fives.",
         say="You doubled the side (3 to 6) but the turf did not double: it went from 9 to 36, four times as much. Doubling a side multiplies the area by 2 × 2 = 4. That is a <strong>square</strong> relationship."),
     say("You have been using area = side², a square proportion \\(A \\propto \\text{side}^2\\). Algebra writes it \\(y = kx^2\\): y is the area, x is the side, and k is a fixed multiplier (here k = 1). Find k from one known pair, then the equation handles every other value. The same recipe works for cubes \\(x^3\\), roots \\(\\sqrt{x}\\) and inverses \\(\\frac{1}{x^2}\\).")
   ]
 },
 "teach": {}
}

# teach.bronze: find k then find y (y prop x^2)
tb, _ = g_prop_square_findy(4,80,6)  # k=5, y=180
guided["teach"]["bronze"] = {
  "display": "\\(y \\propto x^2\\). When \\(x = 4\\), \\(y = 80\\). Find \\(y\\) when \\(x = 6\\).",
  "label": "Together: find k, then use it",
  "steps": [
    say("Bronze move: turn the proportion into \\(y = kx^2\\) and find k, then substitute."),
    box("Square the known x: 4² = ", 16, "Four squared."),
    box("Find k: 80 ÷ 16 = ", 5, "Divide y by the squared value."),
    box("Now the new x: 6² = ", 36, "Six squared.", say="The rule is y = 5x². Use x = 6."),
    box("y = 5 × 36 = ", 180, "Five times thirty-six."),
    box("Check on the first pair: 5 × 4² = 5 × 16 = ", 80, "Five sixteens.",
        done="Matches the given y = 80, so y = 180 is right."),
  ]
}

# teach.silver: reverse solve (y prop x^2), root at the end
guided["teach"]["silver"] = {
  "display": "\\(y \\propto x^2\\). When \\(x = 2\\), \\(y = 20\\). Find \\(x\\) when \\(y = 45\\).",
  "label": "Together: work backwards to x",
  "steps": [
    say("Silver move: after finding k, put in the known y and undo the square with a root at the end."),
    box("Square the known x: 2² = ", 4, "Two squared."),
    box("Find k: 20 ÷ 4 = ", 5, "Divide y by the squared value."),
    box("Now y = 45, so 45 = 5x². Undo the 5: 45 ÷ 5 = ", 9, "How many fives in 45?"),
    box("x² = 9, so x = √9 = ", 3, "What squares to 9?"),
    box("Check: 5 × 3² = 5 × 9 = ", 45, "Five nines.",
        done="Gives back y = 45, so x = 3 is right."),
  ]
}

# teach.gold: inverse square, k = y * x^2
guided["teach"]["gold"] = {
  "display": "\\(y \\propto \\frac{1}{x^2}\\). When \\(x = 2\\), \\(y = 9\\). Find \\(y\\) when \\(x = 3\\).",
  "label": "Together: the inverse-square move",
  "steps": [
    say("Gold move: for \\(y = \\frac{k}{x^2}\\) the constant is k = y × x². Find it, then divide."),
    box("Square the known x: 2² = ", 4, "Two squared."),
    box("k = y × x² = 9 × 4 = ", 36, "Multiply y by the squared value."),
    box("New x = 3, square it: 3² = ", 9, "Three squared."),
    box("y = 36 ÷ 9 = ", 4, "How many nines in 36?"),
    box("Check k: 4 × 3² = 4 × 9 = ", 36, "Four nines.",
        done="Returns k = 36, so y = 4 is right."),
  ]
}

# ---------------- method card (slim) ----------------
method_card = {
  "title": "Proportion with Powers",
  "steps": [
    "Write the proportion as an equation with a constant k, e.g. y = kx², y = k√x or y = k/x².",
    "Substitute the known pair and solve for k (square or root the x value first).",
    "Put k back for the full equation, then substitute the new value to find y.",
    "To find x from y, undo each step in turn and finish with a root. Always check."
  ],
  "content": "<p>At higher tier \\(y\\) can be proportional to a <strong>power</strong> of \\(x\\): \\(y \\propto x^2\\), \\(y \\propto x^3\\), \\(y \\propto \\sqrt{x}\\), or an inverse such as \\(y \\propto \\frac{1}{x^2}\\).</p><p>Each becomes an equation with a constant \\(k\\). Find \\(k\\) from one known pair, then the equation gives every other value. Going backwards from \\(y\\) to \\(x\\) means undoing the power last, with a root.</p>",
  "example": live["method_card"].get("example", "")
}

# ---------------- assemble final object ----------------
out = dict(live)  # preserve everything, then overwrite the sections we changed

# The em-dash rule is hard and validator-enforced, so strip em dashes from the
# preserved worked_examples labels ("Step 1 — Equation" -> "Step 1: Equation").
def strip_em(obj):
    if isinstance(obj, dict):
        return {k: strip_em(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_em(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ":")
    return obj
out["worked_examples"] = strip_em(live.get("worked_examples", []))

out["method_card"] = method_card
out["problem_bank"] = {
  "bronze": bank["bronze"],
  "silver": bank["silver"],
  "gold": bank["gold"],
  "bronze_description": "Find the constant k in one step, or substitute straight into a completed rule.",
  "silver_description": "Handle roots, cubes and inverse forms, and work backwards from y to x.",
  "gold_description": "Multi-step inverse-square, cube and root problems, including real-world formulae."
}
out["tier_guides"] = tier_guides
out["guided"] = guided
# related_videos, topic_links, worked_examples preserved from live via dict(live)

json.dump(out, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("counts: bronze=%d silver=%d gold=%d" % (len(bank["bronze"]), len(bank["silver"]), len(bank["gold"])))
print("bronze sols:", [p["solutions"] for p in bank["bronze"]])
print("silver sols:", [p["solutions"] for p in bank["silver"]])
print("gold sols:", [p["solutions"] for p in bank["gold"]])
print("wrote", OUT)
