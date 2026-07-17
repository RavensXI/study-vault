# -*- coding: utf-8 -*-
"""Build the full guided-learning practice_data for maths-eduqas algebra-L03 (Factorising).
Loads the LIVE row, preserves untouched fields, adds tier_guides / guided /
guided_steps / hints / misconceptions, cleans method_card, writes shard."""
import json

MINUS = "−"  # proper minus sign for student-facing plain text
SRC = "_live_eduqas_algebra-L03.json"
OUT = "lesson_maths-eduqas_algebra-L03.json"

def fmt(n):
    return str(n) if n >= 0 else MINUS + str(-n)

def lx_sign(n):
    return "+" if n >= 0 else "-"

# ---------- guided_steps generators ----------

def cf_linear(disp, var, a, b, h):
    """a*var + b, common numeric factor h. b carries its sign."""
    q1, q2 = a // h, b // h
    inside = "%d%s %s %d" % (q1, var, "+" if q2 >= 0 else MINUS, abs(q2))
    return [
        {"say": "Take out the largest number that divides both terms of \\(%s\\)." % disp,
         "pre": "Highest common factor of %d and %d = " % (a, abs(b)), "post": "",
         "answer": h, "hint": "What is the biggest number that divides both %d and %d?" % (a, abs(b))},
        {"say": "Now divide each term by the common factor.", "phase": "substitute",
         "pre": "Divide the %s term: %d%s ÷ %d = " % (var, a, var, h), "post": var,
         "answer": q1, "hint": "Just divide the number in front of %s." % var},
        {"phase": "substitute",
         "pre": "Divide the number: %s ÷ %d = " % (fmt(b), h), "post": "",
         "answer": q2, "hint": "Keep the sign when you divide.",
         "done": "So the bracket is (%s), giving \\(%d(%d%s %s %d)\\)." % (inside, h, q1, var, lx_sign(q2), abs(q2))},
        {"say": "Expand the bracket back out to be sure.", "phase": "substitute",
         "pre": "Check by expanding: %d × %d = " % (h, q1), "post": "",
         "answer": a, "hint": "Multiply the factor by the first term inside."},
        {"phase": "substitute",
         "pre": "and %d × (%s) = " % (h, fmt(q2)), "post": "",
         "answer": b, "hint": "Multiply the factor by the number inside.",
         "done": "That rebuilds \\(%s\\). Correct." % disp},
    ]

def cf_xquad(disp, a, b, g):
    """a*x^2 + b*x, common factor g*x."""
    q1, q2 = a // g, b // g
    q1disp = "" if q1 == 1 else str(q1)
    return [
        {"say": "Both terms of \\(%s\\) share an x. First find the biggest number they share." % disp,
         "pre": "Every term has an x, and the highest common factor of %d and %d = " % (a, abs(b)), "post": "",
         "answer": g, "hint": "What is the biggest number dividing both %d and %d?" % (a, abs(b))},
        {"say": "The common factor is %dx. Divide each term by it." % g, "phase": "substitute",
         "pre": "So take out %dx. Divide the first term: %dx² ÷ %dx = " % (g, a, g), "post": "x",
         "answer": q1, "hint": "Divide the numbers, and one x cancels."},
        {"phase": "substitute",
         "pre": "Divide the second term: %sx ÷ %dx = " % (fmt(b), g), "post": "",
         "answer": q2, "hint": "Divide the numbers; the x cancels.",
         "done": "So \\(%dx(%sx %s %d)\\)." % (g, q1disp, lx_sign(q2), abs(q2))},
        {"say": "Expand back out to check.", "phase": "substitute",
         "pre": "Check by expanding: %dx × %dx gives the x² term, coefficient %d × %d = " % (g, q1, g, q1), "post": "",
         "answer": a, "hint": "Multiply the numbers in front."},
        {"phase": "substitute",
         "pre": "and %dx × (%s) = " % (g, fmt(q2)), "post": "x",
         "answer": b, "hint": "Multiply the factor by the number inside; keep the x.",
         "done": "That rebuilds \\(%s\\). Correct." % disp},
    ]

def quad(disp, b, c, p, q):
    """x^2 + b x + c = (x+p)(x+q), p the smaller signed value."""
    return [
        {"say": "For \\(%s\\), read off b and c." % disp,
         "pre": "The number at the end, c, is ", "post": "", "answer": c,
         "hint": "Read off the constant term, with its sign."},
        {"pre": "The coefficient of x, b, is ", "post": "", "answer": b,
         "hint": "Read off the number in front of x, with its sign."},
        {"say": "Now hunt for the pair. It must multiply to c AND add to b.", "phase": "substitute",
         "pre": "Find two numbers that multiply to %s and add to %s. Writing the smaller first, the smaller number is " % (fmt(c), fmt(b)),
         "post": "", "answer": p, "hint": "Try factor pairs of the constant; pick the pair that also adds to b."},
        {"phase": "substitute",
         "pre": "and the other number is ", "post": "", "answer": q, "hint": "Its partner in the pair.",
         "done": "So \\((x %s %d)(x %s %d)\\)." % (lx_sign(p), abs(p), lx_sign(q), abs(q))},
        {"say": "Check both conditions.", "phase": "substitute",
         "pre": "Check the product: (%s) × (%s) = " % (fmt(p), fmt(q)), "post": "", "answer": c,
         "hint": "Multiply your two numbers."},
        {"phase": "substitute",
         "pre": "and the sum: (%s) + (%s) = " % (fmt(p), fmt(q)), "post": "", "answer": b,
         "hint": "Add your two numbers.",
         "done": "Multiplies to %s and adds to %s. Correct." % (fmt(c), fmt(b))},
    ]

def dots_simple(disp, r):
    """x^2 - r^2 = (x+r)(x-r)."""
    return [
        {"say": "This is a difference of two squares: a square, minus another square, with no middle x term. The method is to square-root each part."},
        {"say": "Square-root each term.", "phase": "substitute",
         "pre": "\\(\\sqrt{x^2} = x\\), and \\(\\sqrt{%d}\\) = " % (r * r), "post": "",
         "answer": r, "hint": "What number times itself gives %d?" % (r * r)},
        {"phase": "substitute",
         "pre": "So it factorises to (x + %d)(x %s %d). The middle terms +%dx and %s%dx add to " % (r, MINUS, r, r, MINUS, r),
         "post": "", "answer": 0, "hint": "Opposite terms of the same size cancel."},
        {"phase": "substitute",
         "pre": "and the constant: %d × (%s%d) = " % (r, MINUS, r), "post": "",
         "answer": -(r * r), "hint": "Multiply the two numbers, minding the sign.",
         "done": "That rebuilds \\(%s\\). Correct." % disp},
    ]

# ---------- assemble bank ----------

bronze = [
    dict(display="Factorise \\(3x + 9\\)",
         options=["\\(3(x + 3)\\)", "\\(9(x + 1)\\)", "\\(3(x + 9)\\)", "\\(x(3 + 9)\\)"],
         hint="The highest common factor of 3 and 9 is 3, so take 3 outside the bracket.",
         misc=[(1, "wrong_hcf", "9 is not a common factor of 3x. The highest common factor of 3 and 9 is 3: take out 3 and divide each term by it."),
               (2, "undivided_term", "You took out 3 but did not divide the second term by it. 9 ÷ 3 = 3, so the bracket is (x + 3)."),
               (3, "factored_x_only", "You took out x, but the number 9 has no x in it. Take out the common number 3 instead.")],
         gs=cf_linear("3x + 9", "x", 3, 9, 3)),
    dict(display="Factorise \\(4a + 12\\)",
         options=["\\(4(a + 3)\\)", "\\(2(2a + 6)\\)", "\\(4(a + 12)\\)", "\\(12(a + 4)\\)"],
         hint="The highest common factor of 4 and 12 is 4, so take out 4.",
         misc=[(1, "incomplete_factorisation", "2(2a + 6) is not finished: 2a + 6 still shares a factor of 2. The highest common factor is 4, giving 4(a + 3)."),
               (2, "undivided_term", "You took out 4 but did not divide the 12 by it. 12 ÷ 4 = 3, so the bracket is (a + 3)."),
               (3, "wrong_hcf", "12 is not a common factor of 4a. The highest common factor of 4 and 12 is 4.")],
         gs=cf_linear("4a + 12", "a", 4, 12, 4)),
    dict(display="Factorise \\(5x - 10\\)",
         options=["\\(5(x - 2)\\)", "\\(5(x - 10)\\)", "\\(x(5 - 10)\\)", "\\(10(x - 5)\\)"],
         hint="The highest common factor of 5 and 10 is 5; keep the minus sign on the 10.",
         misc=[(1, "undivided_term", "You took out 5 but did not divide the second term by it. %s10 ÷ 5 = %s2, so the bracket is (x %s 2)." % (MINUS, MINUS, MINUS)),
               (2, "factored_x_only", "You took out x, but the numbers 5 and %s10 have no x in them. Take out the common number 5 instead." % MINUS),
               (3, "wrong_hcf", "10 is not a common factor of 5x. The highest common factor of 5 and 10 is 5.")],
         gs=cf_linear("5x - 10", "x", 5, -10, 5)),
    dict(display="Factorise \\(6y + 15\\)",
         options=["\\(3(2y + 5)\\)", "\\(6(y + 15)\\)", "\\(3(2y + 15)\\)", "\\(15(y + 6)\\)"],
         hint="The highest common factor of 6 and 15 is 3, not 6, so take out 3.",
         misc=[(1, "wrong_hcf", "6 is not a common factor of 15. The highest common factor of 6 and 15 is 3, giving 3(2y + 5)."),
               (2, "undivided_term", "You took out 3 but did not divide the 15 by it. 15 ÷ 3 = 5, so the bracket is (2y + 5)."),
               (3, "wrong_hcf2", "15 is not a common factor of 6y. The highest common factor of 6 and 15 is 3.")],
         gs=cf_linear("6y + 15", "y", 6, 15, 3)),
    dict(display="Factorise \\(x^2 + 4x\\)",
         options=["\\(x(x + 4)\\)", "\\(4(x^2 + x)\\)", "\\(x^2(1 + 4)\\)", "\\(2x(x + 2)\\)"],
         hint="Both terms contain an x and the coefficient of x² is 1, so the common factor is just x.",
         misc=[(1, "wrong_factor", "4 is not a factor of x². The two terms share an x, not a 4, so take out x to get x(x + 4)."),
               (2, "over_factored", "x² does not divide 4x, so it cannot come out of both terms. The common factor is a single x: x(x + 4)."),
               (3, "wrong_factor2", "2 is not a factor of x² (its coefficient is 1). The only common factor is x, giving x(x + 4).")],
         gs=[
             {"say": "Both terms of \\(x^2 + 4x\\) contain an x, and there is no number common factor, so the common factor is just x.",
              "pre": "Divide the first term: x² ÷ x = ", "post": "x", "answer": 1,
              "hint": "x² ÷ x leaves one x."},
             {"say": "Divide each term by x.", "phase": "substitute",
              "pre": "Divide the second term: 4x ÷ x = ", "post": "", "answer": 4,
              "hint": "The x cancels, leaving the number.", "done": "So \\(x(x + 4)\\)."},
             {"say": "Expand back out to check.", "phase": "substitute",
              "pre": "Check by expanding: x × x gives x², and x × 4 = ", "post": "x", "answer": 4,
              "hint": "Multiply x by 4.", "done": "That rebuilds \\(x^2 + 4x\\). Correct."},
         ]),
    dict(display="Factorise \\(8m - 12\\)",
         options=["\\(4(2m - 3)\\)", "\\(2(4m - 6)\\)", "\\(8(m - 12)\\)", "\\(4(2m - 12)\\)"],
         hint="The highest common factor of 8 and 12 is 4, not 2, so take out 4.",
         misc=[(1, "incomplete_factorisation", "2(4m %s 6) is not finished: 4m %s 6 still shares a factor of 2. The highest common factor is 4, giving 4(2m %s 3)." % (MINUS, MINUS, MINUS)),
               (2, "wrong_hcf", "8 is not a common factor of 12. The highest common factor of 8 and 12 is 4."),
               (3, "undivided_term", "You took out 4 but did not divide the 12 by it. %s12 ÷ 4 = %s3, so the bracket is (2m %s 3)." % (MINUS, MINUS, MINUS))],
         gs=cf_linear("8m - 12", "m", 8, -12, 4)),
    dict(display="Factorise \\(10p + 25\\)",
         options=["\\(5(2p + 5)\\)", "\\(10(p + 25)\\)", "\\(5(2p + 25)\\)", "\\(25(p + 10)\\)"],
         hint="The highest common factor of 10 and 25 is 5, so take out 5.",
         misc=[(1, "wrong_hcf", "10 is not a common factor of 25. The highest common factor of 10 and 25 is 5, giving 5(2p + 5)."),
               (2, "undivided_term", "You took out 5 but did not divide the 25 by it. 25 ÷ 5 = 5, so the bracket is (2p + 5)."),
               (3, "wrong_hcf2", "25 is not a common factor of 10p. The highest common factor of 10 and 25 is 5.")],
         gs=cf_linear("10p + 25", "p", 10, 25, 5)),
    dict(display="Factorise \\(3x^2 + 6x\\)",
         options=["\\(3x(x + 2)\\)", "\\(3(x^2 + 2x)\\)", "\\(x(3x + 6)\\)", "\\(6x(x + 1)\\)"],
         hint="Every term has an x and both numbers share 3, so take out 3x.",
         misc=[(1, "incomplete_factorisation", "3(x² + 2x) is not finished: both terms in the bracket still have an x. Take out 3x to get 3x(x + 2)."),
               (2, "incomplete_factorisation2", "x(3x + 6) is not finished: 3x + 6 still shares a factor of 3. Take out 3x to get 3x(x + 2)."),
               (3, "wrong_hcf", "6x is not a common factor here: 6 does not divide 3. The highest common factor is 3x.")],
         gs=cf_xquad("3x^2 + 6x", 3, 6, 3)),
]

silver = [
    dict(display="Factorise \\(x^2 + 7x + 12\\)",
         options=["\\((x + 3)(x + 4)\\)", "\\((x + 2)(x + 6)\\)", "\\((x + 1)(x + 12)\\)", "\\((x + 7)(x + 12)\\)"],
         hint="Find two numbers that multiply to 12 and add to 7.",
         misc=[(1, "wrong_pair", "2 × 6 = 12 is right, but 2 + 6 = 8, not 7. You need a pair that multiplies to 12 AND adds to 7: that is 3 and 4."),
               (2, "wrong_pair2", "1 × 12 = 12 is right, but 1 + 12 = 13, not 7. Use 3 and 4, which multiply to 12 and add to 7."),
               (3, "wrong_method", "7 and 12 are just b and c; they do not multiply to 12. Hunt for the pair: 3 and 4 multiply to 12 and add to 7.")],
         gs=quad("x^2 + 7x + 12", 7, 12, 3, 4)),
    dict(display="Factorise \\(x^2 + 5x + 6\\)",
         options=["\\((x + 2)(x + 3)\\)", "\\((x + 1)(x + 6)\\)", "\\((x + 5)(x + 1)\\)", "\\((x + 2)(x + 4)\\)"],
         hint="Find two numbers that multiply to 6 and add to 5.",
         misc=[(1, "wrong_pair", "1 × 6 = 6 is right, but 1 + 6 = 7, not 5. Use 2 and 3, which multiply to 6 and add to 5."),
               (2, "wrong_method", "5 and 1 do not multiply to 6. The pair must multiply to 6 AND add to 5: that is 2 and 3."),
               (3, "wrong_pair2", "2 + 4 = 6, but 2 × 4 = 8, not 6. The pair must multiply to 6: use 2 and 3.")],
         gs=quad("x^2 + 5x + 6", 5, 6, 2, 3)),
    dict(display="Factorise \\(x^2 - 3x - 10\\)",
         options=["\\((x - 5)(x + 2)\\)", "\\((x + 5)(x - 2)\\)", "\\((x - 5)(x - 2)\\)", "\\((x - 10)(x + 1)\\)"],
         hint="Find two numbers that multiply to −10 and add to −3.",
         misc=[(1, "sign_error", "+5 and %s2 multiply to %s10 but add to +3, not %s3. Swap the signs: %s5 and +2 give %s10 and %s3, so (x %s 5)(x + 2)." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS)),
               (2, "sign_error2", "%s5 and %s2 multiply to +10, not %s10. With c negative the two signs must differ: (x %s 5)(x + 2)." % (MINUS, MINUS, MINUS, MINUS)),
               (3, "wrong_pair", "%s10 × 1 = %s10 is right, but %s10 + 1 = %s9, not %s3. Use %s5 and +2." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS))],
         gs=quad("x^2 - 3x - 10", -3, -10, -5, 2)),
    dict(display="Factorise \\(x^2 + 2x - 15\\)",
         options=["\\((x + 5)(x - 3)\\)", "\\((x - 5)(x + 3)\\)", "\\((x + 15)(x - 1)\\)", "\\((x + 5)(x + 3)\\)"],
         hint="Find two numbers that multiply to −15 and add to 2.",
         misc=[(1, "sign_error", "%s5 and +3 multiply to %s15 but add to %s2, not +2. Swap the signs: +5 and %s3 give %s15 and +2, so (x + 5)(x %s 3)." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS)),
               (2, "wrong_pair", "15 × (%s1) = %s15 is right, but 15 + (%s1) = 14, not 2. Use +5 and %s3." % (MINUS, MINUS, MINUS, MINUS)),
               (3, "sign_error2", "+5 and +3 multiply to +15, not %s15. With c negative the signs must differ: (x + 5)(x %s 3)." % (MINUS, MINUS))],
         gs=quad("x^2 + 2x - 15", 2, -15, -3, 5)),
    dict(display="Factorise \\(x^2 - 8x + 15\\)",
         options=["\\((x - 3)(x - 5)\\)", "\\((x + 3)(x + 5)\\)", "\\((x - 3)(x + 5)\\)", "\\((x - 15)(x + 1)\\)"],
         hint="Find two numbers that multiply to 15 and add to −8.",
         misc=[(1, "sign_error", "3 and 5 are the right size, but b is negative and c positive, so both signs are %s: (x %s 3)(x %s 5)." % (MINUS, MINUS, MINUS)),
               (2, "sign_error2", "%s3 and +5 multiply to %s15, not +15. Both signs must be %s here: (x %s 3)(x %s 5)." % (MINUS, MINUS, MINUS, MINUS, MINUS)),
               (3, "wrong_pair", "%s15 × 1 = %s15, not +15, and %s15 + 1 = %s14, not %s8. Use %s3 and %s5." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS))],
         gs=quad("x^2 - 8x + 15", -8, 15, -5, -3)),
    dict(display="Factorise \\(x^2 - 25\\)",
         options=["\\((x + 5)(x - 5)\\)", "\\((x - 5)(x - 5)\\)", "\\((x + 25)(x - 1)\\)", "\\((x + 5)^2\\)"],
         hint="This is a difference of two squares: the square root of 25 is 5, so write one plus and one minus.",
         misc=[(1, "sign_error", "The roots 5 and 5 are right, but a difference of two squares needs one plus and one minus: (x + 5)(x %s 5). Two minuses give a middle term %s10x." % (MINUS, MINUS)),
               (2, "wrong_method", "This has no middle term, so do not hunt for a factor pair. Square-root each part: √25 = 5, giving (x + 5)(x %s 5)." % MINUS),
               (3, "sign_error2", "(x + 5)² = x² + 10x + 25, not x² %s 25. A difference of two squares needs one plus and one minus: (x + 5)(x %s 5)." % (MINUS, MINUS))],
         gs=dots_simple("x^2 - 25", 5)),
    dict(display="Factorise \\(x^2 - x - 12\\)",
         options=["\\((x - 4)(x + 3)\\)", "\\((x + 4)(x - 3)\\)", "\\((x - 6)(x + 2)\\)", "\\((x - 12)(x + 1)\\)"],
         hint="Find two numbers that multiply to −12 and add to −1.",
         misc=[(1, "sign_error", "+4 and %s3 multiply to %s12 but add to +1, not %s1. Swap the signs: %s4 and +3 give %s12 and %s1, so (x %s 4)(x + 3)." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS)),
               (2, "wrong_pair", "%s6 × 2 = %s12 is right, but %s6 + 2 = %s4, not %s1. Use %s4 and +3." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS)),
               (3, "wrong_pair2", "%s12 × 1 = %s12 is right, but %s12 + 1 = %s11, not %s1. Use %s4 and +3." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS))],
         gs=quad("x^2 - x - 12", -1, -12, -4, 3)),
]

# ---------- gold (bespoke walks) ----------
gold = [
    dict(display="Factorise \\(4x^2 - 9\\)",
         options=["\\((2x + 3)(2x - 3)\\)", "\\((4x + 9)(4x - 9)\\)", "\\((2x - 3)^2\\)", "\\((2x + 3)^2\\)"],
         hint="A difference of two squares: square-root 4x² to get 2x and √9 = 3.",
         misc=[(1, "no_root", "4 and 9 are not the roots. Square-root each part: √(4x²) = 2x and √9 = 3, giving (2x + 3)(2x %s 3)." % MINUS),
               (2, "sign_error", "(2x %s 3)² = 4x² %s 12x + 9, which has a middle term. A difference of two squares needs one plus and one minus: (2x + 3)(2x %s 3)." % (MINUS, MINUS, MINUS)),
               (3, "sign_error2", "(2x + 3)² = 4x² + 12x + 9, not 4x² %s 9. Use one plus and one minus: (2x + 3)(2x %s 3)." % (MINUS, MINUS))],
         gs=[
             {"say": "A difference of two squares, but now the x² term has a coefficient. Square-root each part.",
              "pre": "\\(\\sqrt{4x^2}\\) = 2x, so the number in front of x is ", "post": "", "answer": 2,
              "hint": "√4 = 2."},
             {"phase": "substitute", "pre": "\\(\\sqrt{9}\\) = ", "post": "", "answer": 3,
              "hint": "What number times itself gives 9?"},
             {"phase": "substitute", "pre": "So (2x + 3)(2x %s 3). Check the x² term: 2 × 2 = " % MINUS, "post": "",
              "answer": 4, "hint": "Multiply the two numbers in front of x.", "done": "Matches 4x²."},
             {"phase": "substitute", "pre": "and the middle terms +6x and %s6x add to " % MINUS, "post": "",
              "answer": 0, "hint": "Opposite terms of the same size cancel.",
              "done": "That rebuilds \\(4x^2 - 9\\). Correct."},
         ]),
    dict(display="Factorise \\(2x^2 + 10x + 12\\)",
         options=["\\(2(x + 2)(x + 3)\\)", "\\((2x + 6)(x + 2)\\)", "\\(2(x + 4)(x + 3)\\)", "\\((x + 2)(2x + 6)\\)"],
         hint="Take out the common factor 2 first, then factorise x² + 5x + 6.",
         misc=[(1, "incomplete_factorisation", "(2x + 6)(x + 2) multiplies back to 2x² + 10x + 12, but it is not fully factorised: 2x + 6 still shares a factor of 2. Take that 2 out: 2(x + 2)(x + 3)."),
               (2, "wrong_pair", "2(x + 4)(x + 3) = 2(x² + 7x + 12) = 2x² + 14x + 24, not 2x² + 10x + 12. After taking out 2 you need x² + 5x + 6 = (x + 2)(x + 3)."),
               (3, "incomplete_factorisation2", "(x + 2)(2x + 6) multiplies back correctly, but 2x + 6 still has a common factor of 2. Take it out: 2(x + 2)(x + 3).")],
         gs=[
             {"say": "First take out the common factor of all three terms.",
              "pre": "The highest common factor of 2, 10 and 12 = ", "post": "", "answer": 2,
              "hint": "What number divides 2, 10 and 12?"},
             {"say": "Divide through by 2, leaving x² + 5x + 6.", "phase": "substitute",
              "pre": "Two numbers that multiply to 6 and add to 5: the smaller is ", "post": "", "answer": 2,
              "hint": "Factor pairs of 6 that also add to 5."},
             {"phase": "substitute", "pre": "and the other is ", "post": "", "answer": 3,
              "hint": "Its partner in the pair.", "done": "So 2(x + 2)(x + 3)."},
             {"say": "Check the inside brackets.", "phase": "substitute",
              "pre": "Check: 2 × 3 = ", "post": "", "answer": 6, "hint": "Product of the pair."},
             {"phase": "substitute", "pre": "and 2 + 3 = ", "post": "", "answer": 5,
              "hint": "Sum of the pair.",
              "done": "Multiplies to 6, adds to 5, with the 2 taken out. Correct."},
         ]),
    dict(display="Factorise \\(x^2 - 6x + 9\\)",
         options=["\\((x - 3)^2\\)", "\\((x + 3)(x - 3)\\)", "\\((x - 9)(x + 1)\\)", "\\((x + 3)^2\\)"],
         hint="Two numbers that multiply to 9 and add to −6; they turn out to be equal.",
         misc=[(1, "wrong_method", "(x + 3)(x %s 3) = x² %s 9, which has no middle term. This expression has %s6x in the middle, so it is a perfect square: (x %s 3)²." % (MINUS, MINUS, MINUS, MINUS)),
               (2, "wrong_pair", "%s9 × 1 = %s9, not +9, and %s9 + 1 = %s8, not %s6. The pair is %s3 and %s3: (x %s 3)²." % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS)),
               (3, "sign_error", "(x + 3)² = x² + 6x + 9, but the middle term here is %s6x. Both numbers are negative: (x %s 3)²." % (MINUS, MINUS))],
         gs=[
             {"say": "Two numbers that multiply to the constant and add to the coefficient of x.",
              "pre": "The number at the end, c, is ", "post": "", "answer": 9,
              "hint": "Read off the constant term."},
             {"say": "Both signs are negative here.", "phase": "substitute",
              "pre": "Two numbers multiplying to 9 and adding to %s6 are %s3 and %s3. Each number is " % (MINUS, MINUS, MINUS),
              "post": "", "answer": -3, "hint": "√9 = 3, and both must be negative to add to %s6." % MINUS},
             {"phase": "substitute",
              "pre": "So (x %s 3)(x %s 3) = (x %s 3)². Check: (%s3) × (%s3) = " % (MINUS, MINUS, MINUS, MINUS, MINUS),
              "post": "", "answer": 9, "hint": "Multiply the pair."},
             {"phase": "substitute", "pre": "and (%s3) + (%s3) = " % (MINUS, MINUS), "post": "", "answer": -6,
              "hint": "Add the pair.", "done": "Multiplies to 9, adds to %s6. That is \\((x - 3)^2\\). Correct." % MINUS},
         ]),
    dict(display="Factorise \\(3x^2 - 27\\)",
         options=["\\(3(x + 3)(x - 3)\\)", "\\(3(x^2 - 9)\\)", "\\((3x + 9)(x - 3)\\)", "\\(3(x - 3)^2\\)"],
         hint="Take out the common factor 3 first, then factorise the difference of two squares.",
         misc=[(1, "incomplete_factorisation", "3(x² %s 9) is not finished: x² %s 9 is a difference of two squares, (x + 3)(x %s 3). The full answer is 3(x + 3)(x %s 3)." % (MINUS, MINUS, MINUS, MINUS)),
               (2, "incomplete_factorisation2", "(3x + 9)(x %s 3) multiplies back to 3x² %s 27, but 3x + 9 still shares a factor of 3. Take it out: 3(x + 3)(x %s 3)." % (MINUS, MINUS, MINUS)),
               (3, "wrong_method", "3(x %s 3)² = 3(x² %s 6x + 9) = 3x² %s 18x + 27, which has a middle term. This is a difference of two squares: 3(x + 3)(x %s 3)." % (MINUS, MINUS, MINUS, MINUS))],
         gs=[
             {"say": "Take out the common factor first.",
              "pre": "The highest common factor of 3 and 27 = ", "post": "", "answer": 3,
              "hint": "What number divides both 3 and 27?"},
             {"say": "That leaves x² %s 9, a difference of two squares." % MINUS, "phase": "substitute",
              "pre": "√9 = ", "post": "", "answer": 3, "hint": "What number times itself gives 9?"},
             {"phase": "substitute",
              "pre": "So x² %s 9 = (x + 3)(x %s 3). The middle terms +3x and %s3x add to " % (MINUS, MINUS, MINUS),
              "post": "", "answer": 0, "hint": "Opposite terms cancel."},
             {"phase": "substitute", "pre": "and 3 × (%s3) = " % MINUS, "post": "", "answer": -9,
              "hint": "Multiply the roots, minding the sign.",
              "done": "So the full answer is 3(x + 3)(x %s 3). Correct." % MINUS},
         ]),
    dict(display="Factorise completely \\(5x^3 - 20x\\)",
         options=["\\(5x(x + 2)(x - 2)\\)", "\\(5x(x^2 - 4)\\)", "\\(x(5x^2 - 20)\\)", "\\(5(x^3 - 4x)\\)"],
         hint="Take out the common factor 5x first, then factorise the difference of two squares.",
         misc=[(1, "incomplete_factorisation", "5x(x² %s 4) is not finished: x² %s 4 is a difference of two squares, (x + 2)(x %s 2). The full answer is 5x(x + 2)(x %s 2)." % (MINUS, MINUS, MINUS, MINUS)),
               (2, "incomplete_factorisation2", "x(5x² %s 20) only takes out one x. 5x² %s 20 still shares a 5, and factorises further. Take out 5x, then use the difference of two squares: 5x(x + 2)(x %s 2)." % (MINUS, MINUS, MINUS)),
               (3, "incomplete_factorisation3", "5(x³ %s 4x) only takes out the 5. x³ %s 4x still shares an x: x(x² %s 4). Take out 5x, then factorise: 5x(x + 2)(x %s 2)." % (MINUS, MINUS, MINUS, MINUS))],
         gs=[
             {"say": "Take out the common factor from both terms: the numbers 5 and 20, and the shared x.",
              "pre": "The highest common factor of 5 and 20 = ", "post": "", "answer": 5,
              "hint": "What number divides both 5 and 20?"},
             {"say": "Both terms also contain x, so the full common factor is 5x, leaving 5x(x² %s 4)." % MINUS, "phase": "substitute",
              "pre": "Now x² %s 4 is a difference of two squares. √4 = " % MINUS, "post": "", "answer": 2,
              "hint": "What number times itself gives 4?"},
             {"phase": "substitute",
              "pre": "So x² %s 4 = (x + 2)(x %s 2). The middle terms +2x and %s2x add to " % (MINUS, MINUS, MINUS),
              "post": "", "answer": 0, "hint": "Opposite terms cancel."},
             {"phase": "substitute", "pre": "and 2 × (%s2) = " % MINUS, "post": "", "answer": -4,
              "hint": "Multiply the roots.",
              "done": "So the full answer is 5x(x + 2)(x %s 2). Correct." % MINUS},
         ]),
]

def build_problems(rows):
    out = []
    for r in rows:
        p = {
            "display": r["display"],
            "options": r["options"],
            "solutions": [0],
            "calculator": False,
            "input_type": "multiple_choice",
            "hint": r["hint"],
            "misconceptions": [
                {"pattern": pat, "check": pat, "expect": idx, "message": msg}
                for (idx, pat, msg) in r["misc"]
            ],
            "guided_steps": r["gs"],
        }
        out.append(p)
    return out

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: taking out a common factor",
        "steps": [
            "Find the <strong>highest common factor (HCF)</strong> of the numbers in every term. If every term also contains a letter, that letter joins the factor.",
            "Write the HCF outside a bracket, then divide each term by it to get what goes inside.",
            "Check by expanding: multiply the bracket back out and you should land on the original expression.",
        ],
        "example": {
            "question": "Factorise \\(12x + 8\\)",
            "steps": [
                {"label": "Find the HCF", "content": "<p>The HCF of 12 and 8 is \\(4\\).</p>"},
                {"label": "Divide each term", "content": "<p>\\(12x \\div 4 = 3x\\) and \\(8 \\div 4 = 2\\).</p>"},
                {"label": "Check", "content": "<p>\\(4(3x + 2) = 12x + 8\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\(4(3x + 2)\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: factorising \\(x^2 + bx + c\\)",
        "steps": [
            "Find two numbers that <strong>multiply to c</strong> (the number at the end) and <strong>add to b</strong> (the coefficient of x).",
            "Put them in two brackets \\((x + p)(x + q)\\). Watch the signs: if c is negative the two signs differ; if c is positive they match the sign of b.",
            "Check by multiplying out: the two numbers should multiply to c and add to b.",
        ],
        "example": {
            "question": "Factorise \\(x^2 + 9x + 20\\)",
            "steps": [
                {"label": "Find the pair", "content": "<p>Two numbers that multiply to \\(20\\) and add to \\(9\\): that is \\(4\\) and \\(5\\).</p>"},
                {"label": "Write the brackets", "content": "<p>\\((x + 4)(x + 5)\\)</p>"},
                {"label": "Check", "content": "<p>\\(4 \\times 5 = 20\\) and \\(4 + 5 = 9\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\((x + 4)(x + 5)\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: difference of two squares and beyond",
        "steps": [
            "Always take out any <strong>common factor</strong> first, then look at what is left.",
            "A <strong>difference of two squares</strong> \\(a^2 - b^2\\) has no middle term: square-root each part and write \\((a + b)(a - b)\\), one plus and one minus.",
            "Check by expanding: the two middle terms cancel, leaving just \\(a^2 - b^2\\).",
        ],
        "example": {
            "question": "Factorise \\(x^2 - 36\\)",
            "steps": [
                {"label": "Recognise the pattern", "content": "<p>\\(x^2 - 36 = x^2 - 6^2\\), a difference of two squares.</p>"},
                {"label": "Square-root each part", "content": "<p>\\(\\sqrt{x^2} = x\\) and \\(\\sqrt{36} = 6\\).</p>"},
                {"label": "Check", "content": "<p>\\((x + 6)(x - 6) = x^2 - 36\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\((x + 6)(x - 6)\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided (opener + teach) ----------
guided = {
    "opener": {
        "display": "A florist's puzzle, no algebra needed.",
        "steps": [
            {"say": "You are making identical bouquets from <strong>8 red roses</strong> and <strong>12 white roses</strong>, using as MANY bouquets as you can with nothing left over."},
            {"pre": "The largest number of identical bouquets you can make is ", "post": "", "answer": 4,
             "hint": "The number of bouquets must divide both 8 and 12 exactly. What is the biggest number that goes into both?"},
            {"say": "Four bouquets. You just found the <strong>highest common factor</strong> of 8 and 12. Splitting into the most equal groups is exactly what taking out a common factor does."},
            {"pre": "How many red roses go in each bouquet? ", "post": "", "answer": 2,
             "hint": "8 roses shared equally into 4 bouquets."},
            {"pre": "And how many white roses in each bouquet? ", "post": "", "answer": 3,
             "hint": "12 roses shared equally into 4 bouquets."},
            {"say": "So 8 and 12 split as 4 lots of (2 and 3). In algebra, \\(8x + 12\\) does the same thing: <strong>\\(4(2x + 3)\\)</strong>. Factorising just means pulling out the biggest shared amount and writing what is left inside the bracket."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Factorise \\(9x + 12\\)",
            "steps": [
                {"say": "Take out the largest number that divides both terms of \\(9x + 12\\).",
                 "pre": "Highest common factor of 9 and 12 = ", "post": "", "answer": 3,
                 "hint": "What is the biggest number that divides both 9 and 12?"},
                {"say": "Now divide each term by the common factor.", "phase": "substitute",
                 "pre": "Divide the x term: 9x ÷ 3 = ", "post": "x", "answer": 3,
                 "hint": "Just divide the number in front of x."},
                {"phase": "substitute", "pre": "Divide the number: 12 ÷ 3 = ", "post": "", "answer": 4,
                 "hint": "Keep the sign when you divide.", "done": "So the bracket is (3x + 4), giving \\(3(3x + 4)\\)."},
                {"say": "Expand the bracket back out to be sure.", "phase": "substitute",
                 "pre": "Check by expanding: 3 × 3 = ", "post": "", "answer": 9,
                 "hint": "Multiply the factor by the first term inside."},
                {"phase": "substitute", "pre": "and 3 × (4) = ", "post": "", "answer": 12,
                 "hint": "Multiply the factor by the number inside.", "done": "That rebuilds \\(9x + 12\\). Correct."},
            ],
        },
        "silver": {
            "display": "Factorise \\(x^2 + 8x + 15\\)",
            "steps": [
                {"say": "For \\(x^2 + 8x + 15\\), read off b and c.",
                 "pre": "The number at the end, c, is ", "post": "", "answer": 15,
                 "hint": "Read off the constant term, with its sign."},
                {"pre": "The coefficient of x, b, is ", "post": "", "answer": 8,
                 "hint": "Read off the number in front of x, with its sign."},
                {"say": "Now hunt for the pair. It must multiply to c AND add to b.", "phase": "substitute",
                 "pre": "Find two numbers that multiply to 15 and add to 8. Writing the smaller first, the smaller number is ",
                 "post": "", "answer": 3, "hint": "Try factor pairs of the constant; pick the pair that also adds to b."},
                {"phase": "substitute", "pre": "and the other number is ", "post": "", "answer": 5,
                 "hint": "Its partner in the pair.", "done": "So \\((x + 3)(x + 5)\\)."},
                {"say": "Check both conditions.", "phase": "substitute",
                 "pre": "Check the product: (3) × (5) = ", "post": "", "answer": 15, "hint": "Multiply your two numbers."},
                {"phase": "substitute", "pre": "and the sum: (3) + (5) = ", "post": "", "answer": 8,
                 "hint": "Add your two numbers.", "done": "Multiplies to 15 and adds to 8. Correct."},
            ],
        },
        "gold": {
            "display": "Factorise \\(4x^2 - 25\\)",
            "steps": [
                {"say": "This is a difference of two squares: two square terms with a minus between them, and no middle x term. Square-root each part."},
                {"pre": "\\(\\sqrt{4}\\) = ", "post": "", "answer": 2, "phase": "substitute",
                 "hint": "What number times itself gives 4? This is the number in front of x.",
                 "say": "Square-root each term."},
                {"pre": "\\(\\sqrt{25}\\) = ", "post": "", "answer": 5, "phase": "substitute",
                 "hint": "What number times itself gives 25?"},
                {"pre": "So (2x + 5)(2x %s 5). Check the x² term: 2 × 2 = " % MINUS, "post": "", "answer": 4, "phase": "substitute",
                 "hint": "Multiply the two numbers in front of x.", "say": "Expand back out to check."},
                {"pre": "and the middle terms +10x and %s10x add to " % MINUS, "post": "", "answer": 0, "phase": "substitute",
                 "hint": "Opposite terms of the same size cancel.", "done": "That rebuilds \\(4x^2 - 25\\). Correct."},
            ],
        },
    },
}

# ---------- method_card (slim, em-dash-free) ----------
method_card = {
    "title": "How to Factorise",
    "steps": [
        "Always check for a common factor first: take out the HCF of every term.",
        "For \\(x^2 + bx + c\\): find two numbers that multiply to c and add to b.",
        "For a difference of two squares \\(a^2 - b^2\\): write \\((a + b)(a - b)\\).",
        "Check by expanding back to the original.",
    ],
    "content": "<p><strong>Factorising</strong> is the reverse of expanding: rewrite an expression as a product of factors. Start by taking out the <strong>highest common factor</strong> of every term, for example \\(6x + 9 = 3(2x + 3)\\).</p><p>For a quadratic \\(x^2 + bx + c\\), find two numbers that multiply to \\(c\\) and add to \\(b\\); they fill the brackets \\((x + p)(x + q)\\).</p><p>A <strong>difference of two squares</strong> factorises as \\(a^2 - b^2 = (a + b)(a - b)\\), for example \\(x^2 - 16 = (x + 4)(x - 4)\\).</p>",
    "example": "<p><strong>Factorise</strong> \\(x^2 + 7x + 12\\)</p><p><strong>Step 1:</strong> No common factor across all three terms.</p><p><strong>Step 2:</strong> Two numbers that multiply to \\(12\\) and add to \\(7\\): \\(3\\) and \\(4\\).</p><p><strong>Step 3:</strong> \\((x + 3)(x + 4)\\)</p><p><strong>Check:</strong> \\((x + 3)(x + 4) = x^2 + 7x + 12\\) ✔</p>",
}

# ---------- assemble ----------
pd = json.load(open(SRC, encoding="utf-8"))

pd["problem_bank"]["bronze"] = build_problems(bronze)
pd["problem_bank"]["silver"] = build_problems(silver)
pd["problem_bank"]["gold"] = build_problems(gold)
pd["problem_bank"]["bronze_description"] = "Take out the highest common factor: the biggest number, and any shared letter, that divides every term."
pd["problem_bank"]["silver_description"] = "Factorise a quadratic x² + bx + c into two brackets by finding a pair that multiplies to c and adds to b."
pd["problem_bank"]["gold_description"] = "Harder factorising: take out a common factor first, then spot a difference of two squares or a perfect square."

pd["tier_guides"] = tier_guides
pd["guided"] = guided
pd["method_card"] = method_card
# topic_links, related_videos, worked_examples preserved untouched from live.

json.dump(pd, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT)
print("bronze", len(pd["problem_bank"]["bronze"]), "silver", len(pd["problem_bank"]["silver"]), "gold", len(pd["problem_bank"]["gold"]))
