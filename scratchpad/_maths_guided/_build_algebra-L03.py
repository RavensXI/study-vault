# -*- coding: utf-8 -*-
import json, io
from math import gcd

MINUS = "−"  # unicode minus for plain-text student-facing strings

def num(n):
    return (MINUS + str(-n)) if n < 0 else str(n)

# ---------- guided_step builders ----------
def hbox(pre, answer, hint, post="", done=None, say=None, phase=False):
    st = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: st["say"] = say
    if done is not None: st["done"] = done
    if phase: st["phase"] = "substitute"
    return st

def sbox(say):
    return {"say": say}

# ---- BRONZE walks ----
def bronze_linear_walk(p, q):
    h = gcd(abs(p), abs(q)); u = p // h; v = q // h
    inside = f"{u if u!=1 else ''}x {'+' if v>=0 else MINUS} {abs(v)}"
    return [
        hbox(f"Highest common factor of {abs(p)} and {abs(q)} = ", h,
             f"What is the biggest number that divides both {abs(p)} and {abs(q)}?",
             say=f"Take out the largest number that divides both terms of \\({p}x {'+' if q>=0 else '-'} {abs(q)}\\)."),
        hbox(f"Divide the x term: {p}x ÷ {h} = ", u, "Just divide the number in front of x.", post="x", phase=True,
             say="Now divide each term by the common factor."),
        hbox(f"Divide the number: {num(q)} ÷ {h} = ", v, "Keep the sign when you divide.", phase=True,
             done=f"So the bracket is ({inside}), giving \\({h}({u if u!=1 else ''}x {'+' if v>=0 else '-'} {abs(v)})\\)."),
        hbox(f"Check by expanding: {h} × {u} = ", p, "Multiply the factor by the first term inside.", phase=True,
             say="Expand the bracket back out to be sure."),
        hbox(f"and {h} × ({num(v)}) = ", q, "Multiply the factor by the number inside.", phase=True,
             done=f"That rebuilds \\({p}x {'+' if q>=0 else '-'} {abs(q)}\\). Correct."),
    ]

def bronze_xcommon_walk(p, q):
    h = gcd(abs(p), abs(q)); u = p // h; v = q // h
    return [
        hbox(f"Every term has an x, and the highest common factor of {abs(p)} and {abs(q)} = ", h,
             f"What is the biggest number dividing both {abs(p)} and {abs(q)}?",
             say=f"Both terms of \\({p}x^2 {'+' if q>=0 else '-'} {abs(q)}x\\) share an x. First find the biggest number they share."),
        hbox(f"So take out {h}x. Divide the first term: {p}x² ÷ {h}x = ", u, "Divide the numbers, and one x cancels.", post="x", phase=True,
             say=f"The common factor is {h}x. Divide each term by it."),
        hbox(f"Divide the second term: {num(q)}x ÷ {h}x = ", v, "Divide the numbers; the x cancels.", phase=True,
             done=f"So \\({h}x({u if u!=1 else ''}x {'+' if v>=0 else '-'} {abs(v)})\\)."),
        hbox(f"Check by expanding: {h}x × {u}x gives the x² term, coefficient {h} × {u} = ", p, "Multiply the numbers in front.", phase=True,
             say="Expand back out to check."),
        hbox(f"and {h}x × ({num(v)}) = ", q, "Multiply the factor by the number inside; keep the x.", post="x", phase=True,
             done=f"That rebuilds \\({p}x^2 {'+' if q>=0 else '-'} {abs(q)}x\\). Correct."),
    ]

# ---- SILVER walk: x^2 + b x + c -> (x+m)(x+n), m<=n ----
def silver_walk(b, c, m, n):
    assert m*n == c and m+n == b and m <= n
    def brk(r): return f"(x {'+' if r>=0 else '-'} {abs(r)})"
    return [
        hbox("The number at the end, c, is ", c, "Read off the constant term, with its sign.",
             say=f"For \\(x^2 {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)}\\), read off b and c."),
        hbox("The coefficient of x, b, is ", b, "Read off the number in front of x, with its sign."),
        hbox(f"Find two numbers that multiply to {num(c)} and add to {num(b)}. Writing the smaller first, the smaller number is ", m,
             "Try factor pairs of the constant; pick the pair that also adds to b.", phase=True,
             say="Now hunt for the pair. It must multiply to c AND add to b."),
        hbox("and the other number is ", n, "Its partner in the pair.", phase=True,
             done=f"So \\({brk(m)}{brk(n)}\\)."),
        hbox(f"Check the product: ({num(m)}) × ({num(n)}) = ", c, "Multiply your two numbers.", phase=True,
             say="Check both conditions."),
        hbox(f"and the sum: ({num(m)}) + ({num(n)}) = ", b, "Add your two numbers.", phase=True,
             done=f"Multiplies to {num(c)} and adds to {num(b)}. Correct."),
    ]

# ---- GOLD walks ----
def gold_simple_walk(k):
    return [
        sbox("This is a difference of two squares: a square, minus another square, with no middle x term. The method is to square-root each part."),
        hbox(f"\\(\\sqrt{{x^2}} = x\\), and \\(\\sqrt{{{k*k}}}\\) = ", k, f"What number times itself gives {k*k}?", phase=True,
             say="Square-root each term."),
        hbox(f"So it factorises to (x + {k})(x − {k}). The middle terms +{k}x and −{k}x add to ", 0,
             "Opposite terms of the same size cancel.", phase=True),
        hbox(f"and the constant: {k} × ({MINUS}{k}) = ", -k*k, "Multiply the two numbers, minding the sign.", phase=True,
             done=f"That rebuilds \\(x^2 - {k*k}\\). Correct."),
    ]

def gold_coeff_walk(a, bnum):
    A = a*a; B = bnum*bnum
    return [
        sbox("This is a difference of two squares: two square terms with a minus between them, and no middle x term. Square-root each part."),
        hbox(f"\\(\\sqrt{{{A}}}\\) = ", a, f"What number times itself gives {A}? This is the number in front of x.", phase=True,
             say="Square-root each term."),
        hbox(f"\\(\\sqrt{{{B}}}\\) = ", bnum, f"What number times itself gives {B}?", phase=True),
        hbox(f"So ({a}x + {bnum})({a}x − {bnum}). Check the x² term: {a} × {a} = ", A,
             "Multiply the two numbers in front of x.", phase=True, say="Expand back out to check."),
        hbox(f"and the middle terms +{a*bnum}x and −{a*bnum}x add to ", 0,
             "Opposite terms of the same size cancel.", phase=True,
             done=f"That rebuilds \\({A}x^2 - {B}\\). Correct."),
    ]

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

# ---------------- BRONZE ----------------
bronze = [
 {"display": "Factorise \\(3x + 9\\)",
  "options": ["\\(3(x + 3)\\)", "\\(9(x + 1)\\)", "\\(3(x + 9)\\)", "\\(x(3 + 9)\\)"],
  "solutions": [0], "hint": "The highest common factor of 3 and 9 is 3, so take 3 outside the bracket.",
  "walk": bronze_linear_walk(3, 9),
  "misconceptions": [
    mc("wrong_hcf", 1, "9 is not a common factor of 3x. The highest common factor of 3 and 9 is 3: take out 3 and divide each term by it."),
    mc("undivided_term", 2, "You took out 3 but did not divide the second term by it. 9 ÷ 3 = 3, so the bracket is (x + 3)."),
    mc("factored_x_only", 3, "You took out x, but the number 9 has no x in it. Take out the common number 3 instead."),
  ]},
 {"display": "Factorise \\(5x - 10\\)",
  "options": ["\\(5(x + 2)\\)", "\\(5(x - 2)\\)", "\\(10(x - 1)\\)", "\\(x(5 - 10)\\)"],
  "solutions": [1], "hint": "The highest common factor of 5 and 10 is 5; watch the minus sign on the 10.",
  "walk": bronze_linear_walk(5, -10),
  "misconceptions": [
    mc("sign_error", 0, "The sign matters: −10 ÷ 5 = −2, so the bracket is (x − 2), not (x + 2)."),
    mc("wrong_hcf", 2, "10 is not a common factor of 5x. The highest common factor of 5 and 10 is 5."),
    mc("factored_x_only", 3, "You took out x, but the number −10 has no x in it. Take out the common number 5 instead."),
  ]},
 {"display": "Factorise \\(8x + 12\\)",
  "options": ["\\(4(2x + 3)\\)", "\\(2(4x + 6)\\)", "\\(8(x + 12)\\)", "\\(4(2x + 12)\\)"],
  "solutions": [0], "hint": "The highest common factor of 8 and 12 is 4, not 2, so take out 4.",
  "walk": bronze_linear_walk(8, 12),
  "misconceptions": [
    mc("incomplete_factorisation", 1, "2(4x + 6) is correct but not finished: 4x + 6 still shares a factor of 2. The highest common factor is 4, giving 4(2x + 3)."),
    mc("wrong_hcf", 2, "8 is not a common factor of 12. The highest common factor of 8 and 12 is 4."),
    mc("undivided_term", 3, "You took out 4 but did not divide the 12 by it. 12 ÷ 4 = 3, so the bracket is (2x + 3)."),
  ]},
 {"display": "Factorise \\(6x^2 + 3x\\)",
  "options": ["\\(3(2x^2 + x)\\)", "\\(3x(2x + 1)\\)", "\\(6x(x + 3)\\)", "\\(x(6x + 3)\\)"],
  "solutions": [1], "hint": "Every term has an x and both numbers share 3, so take out 3x.",
  "walk": bronze_xcommon_walk(6, 3),
  "misconceptions": [
    mc("incomplete_factorisation", 0, "3(2x² + x) is not finished: both terms in the bracket still have an x. Take out 3x to get 3x(2x + 1)."),
    mc("wrong_hcf", 2, "6x is not a common factor here: 6 does not divide 3. The highest common factor is 3x."),
    mc("factored_x_only", 3, "x(6x + 3) is not finished: 6x + 3 still shares a factor of 3. Take out 3x to get 3x(2x + 1)."),
  ]},
 {"display": "Factorise \\(10x - 15\\)",
  "options": ["\\(5(2x - 3)\\)", "\\(5(2x + 3)\\)", "\\(10(x - 15)\\)", "\\(2(5x - 3)\\)"],
  "solutions": [0], "hint": "The highest common factor of 10 and 15 is 5; keep the minus sign.",
  "walk": bronze_linear_walk(10, -15),
  "misconceptions": [
    mc("sign_error", 1, "The sign matters: −15 ÷ 5 = −3, so the bracket is (2x − 3), not (2x + 3)."),
    mc("wrong_hcf", 2, "10 is not a common factor of 15. The highest common factor of 10 and 15 is 5."),
    mc("wrong_hcf2", 3, "2 divides 10 but not 15, so it is not a common factor of both terms. Use 5, the highest common factor."),
  ]},
 {"display": "Factorise \\(4x^2 + 8x\\)",
  "options": ["\\(4(x^2 + 2x)\\)", "\\(4x(x + 2)\\)", "\\(2x(2x + 4)\\)", "\\(x(4x + 8)\\)"],
  "solutions": [1], "hint": "Every term has an x and both numbers share 4, so take out 4x.",
  "walk": bronze_xcommon_walk(4, 8),
  "misconceptions": [
    mc("incomplete_factorisation", 0, "4(x² + 2x) is not finished: both terms in the bracket still have an x. Take out 4x to get 4x(x + 2)."),
    mc("incomplete_factorisation2", 2, "2x(2x + 4) is not finished: 2x + 4 still shares a factor of 2. The highest common factor is 4x."),
    mc("factored_x_only", 3, "x(4x + 8) is not finished: 4x + 8 still shares a factor of 4. Take out 4x to get 4x(x + 2)."),
  ]},
 {"display": "Factorise \\(15x + 10\\)",
  "options": ["\\(5(3x + 2)\\)", "\\(5(3x + 10)\\)", "\\(15(x + 10)\\)", "\\(3(5x + 2)\\)"],
  "solutions": [0], "hint": "The highest common factor of 15 and 10 is 5, so take out 5.",
  "walk": bronze_linear_walk(15, 10),
  "misconceptions": [
    mc("undivided_term", 1, "You took out 5 but did not divide the 10 by it. 10 ÷ 5 = 2, so the bracket is (3x + 2)."),
    mc("wrong_hcf", 2, "15 is not a common factor of 10. The highest common factor of 15 and 10 is 5."),
    mc("wrong_hcf2", 3, "3 divides 15 but not 10, so it is not a common factor of both terms. Use 5, the highest common factor."),
  ]},
 {"display": "Factorise \\(7x^2 - 14x\\)",
  "options": ["\\(7(x^2 - 2x)\\)", "\\(7x(x + 2)\\)", "\\(7x(x - 2)\\)", "\\(x(7x - 14)\\)"],
  "solutions": [2], "hint": "Every term has an x and both numbers share 7, so take out 7x; keep the minus.",
  "walk": bronze_xcommon_walk(7, -14),
  "misconceptions": [
    mc("incomplete_factorisation", 0, "7(x² − 2x) is not finished: both terms in the bracket still have an x. Take out 7x to get 7x(x − 2)."),
    mc("sign_error", 1, "The sign matters: −14x ÷ 7x = −2, so the bracket is (x − 2), not (x + 2)."),
    mc("factored_x_only", 3, "x(7x − 14) is not finished: 7x − 14 still shares a factor of 7. Take out 7x to get 7x(x − 2)."),
  ]},
]

# ---------------- SILVER ----------------
silver = [
 {"display": "Factorise \\(x^2 + 6x + 8\\)",
  "options": ["\\((x + 2)(x + 4)\\)", "\\((x + 1)(x + 8)\\)", "\\((x + 3)(x + 3)\\)", "\\((x - 2)(x - 4)\\)"],
  "solutions": [0], "hint": "Find two numbers that multiply to 8 and add to 6.",
  "walk": silver_walk(6, 8, 2, 4),
  "misconceptions": [
    mc("wrong_pair", 1, "1 × 8 = 8 is right, but 1 + 8 = 9, not 6. You need a pair that multiplies to 8 AND adds to 6: that is 2 and 4."),
    mc("wrong_pair2", 2, "3 + 3 = 6 is right, but 3 × 3 = 9, not 8. The pair must also multiply to 8: use 2 and 4."),
    mc("sign_error", 3, "The numbers 2 and 4 are right, but with c positive and b positive both signs are +: (x + 2)(x + 4). Two minuses would give −6x."),
  ]},
 {"display": "Factorise \\(x^2 + 9x + 14\\)",
  "options": ["\\((x + 2)(x + 7)\\)", "\\((x + 1)(x + 14)\\)", "\\((x + 3)(x + 6)\\)", "\\((x - 2)(x - 7)\\)"],
  "solutions": [0], "hint": "Find two numbers that multiply to 14 and add to 9.",
  "walk": silver_walk(9, 14, 2, 7),
  "misconceptions": [
    mc("wrong_pair", 1, "1 × 14 = 14 is right, but 1 + 14 = 15, not 9. Use 2 and 7, which multiply to 14 and add to 9."),
    mc("wrong_pair2", 2, "3 + 6 = 9 is right, but 3 × 6 = 18, not 14. The pair must multiply to 14: use 2 and 7."),
    mc("sign_error", 3, "The numbers 2 and 7 are right, but both signs should be + here: (x + 2)(x + 7)."),
  ]},
 {"display": "Factorise \\(x^2 - x - 6\\)",
  "options": ["\\((x - 2)(x + 3)\\)", "\\((x + 2)(x - 3)\\)", "\\((x + 1)(x - 6)\\)", "\\((x + 6)(x - 1)\\)"],
  "solutions": [1], "hint": "Find two numbers that multiply to −6 and add to −1.",
  "walk": silver_walk(-1, -6, -3, 2),
  "misconceptions": [
    mc("sign_error", 0, "−2 and +3 multiply to −6 but add to +1, not −1. Swap the signs: +2 and −3 give −6 and −1, so (x + 2)(x − 3)."),
    mc("wrong_pair", 2, "1 × (−6) = −6 is right, but 1 + (−6) = −5, not −1. Use +2 and −3."),
    mc("wrong_pair2", 3, "6 and −1 multiply to −6 but add to +5, not −1. Use +2 and −3."),
  ]},
 {"display": "Factorise \\(x^2 + 3x - 10\\)",
  "options": ["\\((x + 5)(x - 2)\\)", "\\((x - 5)(x + 2)\\)", "\\((x + 10)(x - 1)\\)", "\\((x + 5)(x + 2)\\)"],
  "solutions": [0], "hint": "Find two numbers that multiply to −10 and add to 3.",
  "walk": silver_walk(3, -10, -2, 5),
  "misconceptions": [
    mc("sign_error", 1, "−5 and +2 multiply to −10 but add to −3, not +3. Swap: +5 and −2 give −10 and +3, so (x + 5)(x − 2)."),
    mc("wrong_pair", 2, "10 × (−1) = −10 is right, but 10 + (−1) = 9, not 3. Use +5 and −2."),
    mc("sign_error2", 3, "5 and 2 are the right size, but c is negative, so the signs must differ: (x + 5)(x − 2). Two pluses give +10, not −10."),
  ]},
 {"display": "Factorise \\(x^2 - 5x + 6\\)",
  "options": ["\\((x + 2)(x + 3)\\)", "\\((x - 1)(x - 6)\\)", "\\((x - 2)(x - 3)\\)", "\\((x - 2)(x + 3)\\)"],
  "solutions": [2], "hint": "Find two numbers that multiply to 6 and add to −5.",
  "walk": silver_walk(-5, 6, -3, -2),
  "misconceptions": [
    mc("sign_error", 0, "2 and 3 are right, but b is negative and c positive, so both signs are −: (x − 2)(x − 3)."),
    mc("wrong_pair", 1, "1 × 6 = 6 is right, but −1 + (−6) = −7, not −5. Use −2 and −3."),
    mc("sign_error2", 3, "−2 and +3 multiply to −6, not +6. With c positive and b negative both signs are −: (x − 2)(x − 3)."),
  ]},
 {"display": "Factorise \\(x^2 + 2x - 8\\)",
  "options": ["\\((x + 4)(x - 2)\\)", "\\((x - 4)(x + 2)\\)", "\\((x + 8)(x - 1)\\)", "\\((x + 4)(x + 2)\\)"],
  "solutions": [0], "hint": "Find two numbers that multiply to −8 and add to 2.",
  "walk": silver_walk(2, -8, -2, 4),
  "misconceptions": [
    mc("sign_error", 1, "−4 and +2 multiply to −8 but add to −2, not +2. Swap: +4 and −2 give −8 and +2, so (x + 4)(x − 2)."),
    mc("wrong_pair", 2, "8 × (−1) = −8 is right, but 8 + (−1) = 7, not 2. Use +4 and −2."),
    mc("sign_error2", 3, "4 and 2 are the right size, but c is negative so the signs must differ: (x + 4)(x − 2)."),
  ]},
 {"display": "Factorise \\(x^2 - 7x + 10\\)",
  "options": ["\\((x - 2)(x - 5)\\)", "\\((x + 2)(x - 5)\\)", "\\((x - 1)(x - 10)\\)", "\\((x + 2)(x + 5)\\)"],
  "solutions": [0], "hint": "Find two numbers that multiply to 10 and add to −7.",
  "walk": silver_walk(-7, 10, -5, -2),
  "misconceptions": [
    mc("sign_error", 1, "+2 and −5 multiply to −10, not +10. With c positive and b negative both signs are −: (x − 2)(x − 5)."),
    mc("wrong_pair", 2, "1 × 10 = 10 is right, but −1 + (−10) = −11, not −7. Use −2 and −5."),
    mc("sign_error2", 3, "2 and 5 are right, but b is negative and c positive, so both signs are −: (x − 2)(x − 5)."),
  ]},
]

# ---------------- GOLD ----------------
gold = [
 {"display": "Factorise \\(x^2 - 25\\)",
  "options": ["\\((x + 5)(x - 5)\\)", "\\((x - 5)(x - 5)\\)", "\\((x + 25)(x - 1)\\)", "\\((x + 5)(x + 5)\\)"],
  "solutions": [0], "hint": "This is a difference of two squares: the square root of 25 is 5, so write one plus and one minus.",
  "walk": gold_simple_walk(5),
  "misconceptions": [
    mc("sign_error", 1, "The roots 5 and 5 are right, but a difference of two squares needs one plus and one minus: (x + 5)(x − 5). Two minuses give a middle term −10x."),
    mc("wrong_method", 2, "This has no middle term, so do not hunt for a factor pair. Square-root each part: √25 = 5, giving (x + 5)(x − 5)."),
    mc("sign_error2", 3, "Two pluses give x² + 10x + 25, not x² − 25. A difference of two squares needs one plus and one minus: (x + 5)(x − 5)."),
  ]},
 {"display": "Factorise \\(x^2 - 49\\)",
  "options": ["\\((x + 7)(x + 7)\\)", "\\((x + 7)(x - 7)\\)", "\\((x - 7)(x - 7)\\)", "\\((x + 49)(x - 1)\\)"],
  "solutions": [1], "hint": "This is a difference of two squares: the square root of 49 is 7, so write one plus and one minus.",
  "walk": gold_simple_walk(7),
  "misconceptions": [
    mc("sign_error", 0, "Two pluses give x² + 14x + 49, not x² − 49. A difference of two squares needs one plus and one minus: (x + 7)(x − 7)."),
    mc("sign_error2", 2, "The roots 7 and 7 are right, but two minuses give a middle term −14x. Use one plus and one minus: (x + 7)(x − 7)."),
    mc("wrong_method", 3, "This has no middle term, so do not hunt for a factor pair. Square-root each part: √49 = 7, giving (x + 7)(x − 7)."),
  ]},
 {"display": "Factorise \\(4x^2 - 9\\)",
  "options": ["\\((4x + 3)(x - 3)\\)", "\\((2x + 3)(2x - 3)\\)", "\\((2x - 3)(2x - 3)\\)", "\\((2x + 9)(2x - 1)\\)"],
  "solutions": [1], "hint": "A difference of two squares: the square root of 4x² is 2x and of 9 is 3.",
  "walk": gold_coeff_walk(2, 3),
  "misconceptions": [
    mc("wrong_root", 0, "You must square-root the whole first term: √(4x²) = 2x, not 4x. The factors are (2x + 3)(2x − 3)."),
    mc("sign_error", 2, "The roots 2x and 3 are right, but two minuses give a middle term −12x. Use one plus and one minus: (2x + 3)(2x − 3)."),
    mc("wrong_method", 3, "This has no middle term, so do not hunt for a factor pair. Square-root each part: √(4x²) = 2x and √9 = 3, giving (2x + 3)(2x − 3)."),
  ]},
 {"display": "Factorise \\(x^2 - 100\\)",
  "options": ["\\((x + 10)(x - 10)\\)", "\\((x + 50)(x - 2)\\)", "\\((x - 10)(x - 10)\\)", "\\((x + 100)(x - 1)\\)"],
  "solutions": [0], "hint": "This is a difference of two squares: the square root of 100 is 10, so write one plus and one minus.",
  "walk": gold_simple_walk(10),
  "misconceptions": [
    mc("wrong_method", 1, "This has no middle term, so do not hunt for a factor pair like 50 and 2. Square-root each part: √100 = 10, giving (x + 10)(x − 10)."),
    mc("sign_error", 2, "The roots 10 and 10 are right, but two minuses give a middle term −20x. Use one plus and one minus: (x + 10)(x − 10)."),
    mc("wrong_method2", 3, "100 × 1 is not the way. A difference of two squares uses the square root of each part: √100 = 10, giving (x + 10)(x − 10)."),
  ]},
 {"display": "Factorise \\(9x^2 - 16\\)",
  "options": ["\\((9x + 4)(x - 4)\\)", "\\((3x - 4)(3x - 4)\\)", "\\((3x + 4)(3x - 4)\\)", "\\((3x + 8)(3x - 2)\\)"],
  "solutions": [2], "hint": "A difference of two squares: the square root of 9x² is 3x and of 16 is 4.",
  "walk": gold_coeff_walk(3, 4),
  "misconceptions": [
    mc("wrong_root", 0, "You must square-root the whole first term: √(9x²) = 3x, not 9x. The factors are (3x + 4)(3x − 4)."),
    mc("sign_error", 1, "The roots 3x and 4 are right, but two minuses give a middle term −24x. Use one plus and one minus: (3x + 4)(3x − 4)."),
    mc("wrong_method", 3, "This has no middle term, so do not hunt for a factor pair. Square-root each part: √(9x²) = 3x and √16 = 4, giving (3x + 4)(3x − 4)."),
  ]},
]

def finalise(problem_list):
    out = []
    for p in problem_list:
        q = {
            "display": p["display"], "options": p["options"], "solutions": p["solutions"],
            "calculator": False, "input_type": "multiple_choice", "hint": p["hint"],
            "misconceptions": p["misconceptions"], "guided_steps": p["walk"],
        }
        correct = p["solutions"][0]
        expects = sorted(m["expect"] for m in p["misconceptions"])
        allbut = sorted(i for i in range(len(p["options"])) if i != correct)
        assert expects == allbut, f"{p['display']}: expects {expects} != {allbut}"
        out.append(q)
    return out

data = json.load(io.open('_fresh_algebra-L03_pd.json', encoding='utf-8'))

problem_bank = {
    "bronze": finalise(bronze), "silver": finalise(silver), "gold": finalise(gold),
    "bronze_description": "Take out common factors",
    "silver_description": "Factorise quadratics with a = 1",
    "gold_description": "Difference of two squares and mixed practice",
}

tier_guides = {
 "bronze": {
   "title": "Bronze: taking out a common factor",
   "steps": [
     "Find the <strong>highest common factor (HCF)</strong> of the numbers in every term. If every term also contains an x, that x joins the factor.",
     "Write the HCF outside a bracket, then divide each term by it to get what goes inside.",
     "Check by expanding: multiply the bracket back out and you should land on the original expression."
   ],
   "example": {"question": "Factorise \\(6x + 15\\)", "steps": [
       {"label": "Find the HCF", "content": "<p>The HCF of 6 and 15 is \\(3\\).</p>"},
       {"label": "Divide each term", "content": "<p>\\(6x \\div 3 = 2x\\) and \\(15 \\div 3 = 5\\).</p>"},
       {"label": "Check", "content": "<p>\\(3(2x + 5) = 6x + 15\\) ✔</p>"},
       {"label": "Answer", "content": "<p><strong>\\(3(2x + 5)\\)</strong></p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
   "title": "Silver: factorising \\(x^2 + bx + c\\)",
   "steps": [
     "Find two numbers that <strong>multiply to c</strong> (the number at the end) and <strong>add to b</strong> (the coefficient of x).",
     "Put them in two brackets \\((x + p)(x + q)\\). Watch the signs: if c is negative the two signs differ; if c is positive they match the sign of b.",
     "Check by multiplying out: the two numbers should multiply to c and add to b."
   ],
   "example": {"question": "Factorise \\(x^2 + 7x + 12\\)", "steps": [
       {"label": "Find the pair", "content": "<p>Two numbers that multiply to \\(12\\) and add to \\(7\\): that is \\(3\\) and \\(4\\).</p>"},
       {"label": "Write the brackets", "content": "<p>\\((x + 3)(x + 4)\\)</p>"},
       {"label": "Check", "content": "<p>\\(3 \\times 4 = 12\\) and \\(3 + 4 = 7\\) ✔</p>"},
       {"label": "Answer", "content": "<p><strong>\\((x + 3)(x + 4)\\)</strong></p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
   "title": "Gold: difference of two squares",
   "steps": [
     "Spot the pattern: <strong>one square subtract another square</strong>, with no middle x term, like \\(a^2 - b^2\\).",
     "Square-root each part. The answer is \\((a + b)(a - b)\\): the same two roots, one with a plus and one with a minus.",
     "Check by expanding: the two middle terms cancel, leaving just \\(a^2 - b^2\\)."
   ],
   "example": {"question": "Factorise \\(x^2 - 36\\)", "steps": [
       {"label": "Recognise the pattern", "content": "<p>\\(x^2 - 36 = x^2 - 6^2\\), a difference of two squares.</p>"},
       {"label": "Square-root each part", "content": "<p>\\(\\sqrt{x^2} = x\\) and \\(\\sqrt{36} = 6\\).</p>"},
       {"label": "Check", "content": "<p>\\((x + 6)(x - 6) = x^2 - 6x + 6x - 36 = x^2 - 36\\) ✔</p>"},
       {"label": "Answer", "content": "<p><strong>\\((x + 6)(x - 6)\\)</strong></p>", "isAnswer": True, "is_answer": True}]}}
}

opener = {
 "display": "A party puzzle, no algebra needed.",
 "steps": [
   {"say": "You have <strong>12 sweets</strong> and <strong>18 stickers</strong>. You want to fill party bags so that every bag is identical and nothing is left over, using as MANY bags as you can."},
   {"pre": "The largest number of identical bags you can make is ", "post": "", "answer": 6,
    "hint": "The number of bags must divide both 12 and 18 exactly. What is the biggest number that goes into both?"},
   {"say": "Six bags. You just found the <strong>highest common factor</strong> of 12 and 18. Splitting into the most equal groups is exactly what taking out a common factor does."},
   {"pre": "How many sweets go in each bag? ", "post": "", "answer": 2, "hint": "12 sweets shared equally into 6 bags."},
   {"pre": "And how many stickers in each bag? ", "post": "", "answer": 3, "hint": "18 stickers shared equally into 6 bags."},
   {"say": "So 12 and 18 split as 6 lots of (2 and 3). In algebra, \\(12x + 18\\) does the same thing: <strong>\\(6(2x + 3)\\)</strong>. Factorising just means pulling out the biggest shared amount and writing what is left inside the bracket."}
 ]
}

teach = {
 "bronze": {"display": "Factorise \\(4x + 10\\)", "steps": bronze_linear_walk(4, 10)},
 "silver": {"display": "Factorise \\(x^2 + 8x + 15\\)", "steps": silver_walk(8, 15, 3, 5)},
 "gold": {"display": "Factorise \\(4x^2 - 25\\)", "steps": gold_coeff_walk(2, 5)},
}

guided = {"opener": opener, "teach": teach}

method_card = {
 "title": "How to Factorise",
 "steps": [
   "Always check for a common factor first: take out the HCF of every term.",
   "For \\(x^2 + bx + c\\): find two numbers that multiply to c and add to b.",
   "For a difference of two squares \\(a^2 - b^2\\): write \\((a + b)(a - b)\\).",
   "Check by expanding back to the original."
 ],
 "content": "<p><strong>Factorising</strong> is the reverse of expanding: you rewrite an expression as a product of factors. Start by taking out the <strong>highest common factor</strong> of every term, for example \\(6x + 9 = 3(2x + 3)\\).</p><p>For a quadratic \\(x^2 + bx + c\\), find two numbers that multiply to \\(c\\) and add to \\(b\\); they fill the brackets \\((x + p)(x + q)\\).</p><p>A <strong>difference of two squares</strong> factorises as \\(a^2 - b^2 = (a + b)(a - b)\\), for example \\(x^2 - 16 = (x + 4)(x - 4)\\).</p>",
 "example": data["method_card"]["example"]
}

# Sanitise em dashes in preserved worked_examples labels (style rule: no em dashes student-facing)
worked_examples = data["worked_examples"]
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

out = {
 "method_card": method_card, "tier_guides": tier_guides, "guided": guided,
 "topic_links": data["topic_links"], "problem_bank": problem_bank,
 "related_videos": data["related_videos"], "worked_examples": worked_examples,
}

json.dump(out, io.open('lesson_algebra-L03.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("written lesson_algebra-L03.json")
print("bronze", len(problem_bank['bronze']), "silver", len(problem_bank['silver']), "gold", len(problem_bank['gold']))
