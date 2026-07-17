# -*- coding: utf-8 -*-
"""Full guided conversion of OCR algebra-L14 (Quadratic nth Term, Functions & Iteration)."""
import json, io

MINUS = "−"  # −
ARROW = "→"  # →

# ---- opener SVG: three rectangles of unit squares 1x3, 2x4, 3x5 = 3, 8, 15 ----
def rect_grid(x0, y0, cols, rows, cell=11):
    out = []
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * cell
            y = y0 - r * cell  # grow upward
            out.append(
                '<rect x="%d" y="%d" width="%d" height="%d" fill="#60a5fa" '
                'fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>'
                % (x, y, cell, cell))
    return "".join(out)

# baseline y for bottom row
base = 52
cell = 11
# pattern 1: 1 row x 3 cols at x=10
p1 = rect_grid(10, base, 3, 1, cell)
# pattern 2: 2 rows x 4 cols at x=70
p2 = rect_grid(70, base, 4, 2, cell)
# pattern 3: 3 rows x 5 cols at x=140
p3 = rect_grid(140, base, 5, 3, cell)
labels = (
    '<text x="26" y="80" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle">3</text>'
    '<text x="92" y="80" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle">8</text>'
    '<text x="167" y="80" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle">15</text>'
)
opener_svg = (
    '<svg viewBox="0 0 210 90" role="img" aria-label="Three growing rectangles of squares holding 3, 8 and 15 squares">'
    + p1 + p2 + p3 + labels + "</svg>"
)

opener_display = (
    opener_svg +
    "<p>Three patterns made of squares: <strong>3</strong>, then <strong>8</strong>, "
    "then <strong>15</strong>. Just count how big each jump is.</p>"
)

practice_data = {
    "method_card": {
        "title": "Quadratic nth Term, Functions and Iteration",
        "steps": [
            "Quadratic sequence: halve the second difference for a, subtract an² to find bn + c.",
            "f(x): replace x with the input. fg(x): do g first, then f.",
            "Inverse f⁻¹: swap x and y, then make y the subject.",
            "Iteration: put xₙ into the formula to get xₙ₊₁; repeat.",
        ],
        "content": (
            "<p>A <strong>quadratic sequence</strong> has a constant second difference. "
            "Its nth term is \\(an^2 + bn + c\\), where \\(a\\) is half the second difference. "
            "Subtract \\(an^2\\) from each term, then find the nth term of the linear remainder.</p>"
            "<p><strong>Functions:</strong> \\(f(3)\\) substitutes \\(x = 3\\). Composite \\(fg(x)\\) applies "
            "\\(g\\) first, then \\(f\\). The inverse \\(f^{-1}(x)\\) reverses \\(f\\): swap \\(x\\) and \\(y\\), "
            "then rearrange.</p>"
            "<p><strong>Iteration:</strong> \\(x_{n+1} = g(x_n)\\) turns one approximation into the next; "
            "repeat until the digits settle.</p>"
        ),
        "example": (
            "<p><strong>Find the nth term of</strong> 3, 8, 15, 24, 35</p>"
            "<p>Second difference 2, so \\(a = 1\\). Subtract \\(n^2\\): 2, 4, 6, 8, 10. Remainder \\(2n\\).</p>"
            "<p><strong>Answer:</strong> \\(n^2 + 2n\\)</p>"
        ),
    },
    "topic_links": {"prerequisites": []},
    "problem_bank": {
        "bronze_description": "Put one number in: a single difference, or one substitution into a function.",
        "silver_description": "Two linked steps: composite or inverse functions, or one iteration step.",
        "gold_description": "Full quadratic nth term, solving composite equations, or iterating to a root.",
        "bronze": [
            {  # B1
                "display": "Find the 2nd difference of \\(1, 4, 9, 16, 25, ...\\)",
                "solutions": [2],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Find the differences of the differences, not just the first gaps.",
                "misconceptions": [{
                    "pattern": "first_difference", "check": "first_difference", "expect": 3,
                    "message": "3, 5, 7, 9 are the first differences and they keep changing. Take the difference of those: 5 " + MINUS + " 3 = 2. The second difference is 2.",
                    "note": "reports first first-difference"
                }],
                "guided_steps": [
                    {"say": "Second difference means the difference of the differences. First find the gaps between terms.",
                     "pre": "4 " + MINUS + " 1 = ", "post": "", "answer": 3, "hint": "Subtract the first two terms."},
                    {"pre": "9 " + MINUS + " 4 = ", "post": "", "answer": 5, "hint": "Subtract the next pair."},
                    {"phase": "substitute", "pre": "Now the difference of those gaps: 5 " + MINUS + " 3 = ", "post": "", "answer": 2, "hint": "Take the first gap from the second."},
                    {"phase": "substitute", "pre": "Check it stays constant: 16 " + MINUS + " 9 = 7, then 7 " + MINUS + " 5 = ", "post": "", "answer": 2,
                     "done": "A constant second difference of 2, so the sequence is quadratic.", "hint": "Seven minus five."},
                ],
            },
            {  # B2
                "display": "The nth term of a sequence is \\(n^2 + 3\\). Find the 5th term.",
                "solutions": [28],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Put n equals 5 in: square it first, then add 3.",
                "misconceptions": [{
                    "pattern": "squared_as_double", "check": "squared_as_double", "expect": 13,
                    "message": "\\(5^2\\) means \\(5 \\times 5 = 25\\), not \\(2 \\times 5\\). So the 5th term is \\(25 + 3 = 28\\). Using 10 for \\(5^2\\) gives 13.",
                    "note": "5^2 read as 2*5=10 -> 13"
                }],
                "guided_steps": [
                    {"say": "The 5th term means put \\(n = 5\\) into \\(n^2 + 3\\). Square first.",
                     "pre": "Square n: 5 × 5 = ", "post": "", "answer": 25, "hint": "Five times five, not five times two."},
                    {"phase": "substitute", "pre": "Now add 3: 25 + 3 = ", "post": "", "answer": 28, "hint": "Add the 3."},
                    {"phase": "substitute", "pre": "Check: 5² + 3 = 25 + 3 = ", "post": "", "answer": 28,
                     "done": "So the 5th term is 28.", "hint": "Twenty-five plus three."},
                ],
            },
            {  # B3
                "display": "If \\(f(x) = 2x + 5\\), find \\(f(3)\\).",
                "solutions": [11],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Multiply the input by 2, then add 5.",
                "misconceptions": [{
                    "pattern": "bracket_order", "check": "bracket_order", "expect": 16,
                    "message": "\\(2x + 5\\) means multiply by 2 THEN add 5: \\(2 \\times 3 + 5 = 11\\), not \\(2 \\times (3 + 5) = 16\\).",
                    "note": "does 2*(3+5)=16"
                }],
                "guided_steps": [
                    {"say": "\\(f(3)\\) means put \\(x = 3\\) into \\(2x + 5\\).",
                     "pre": "Work out 2 × 3 = ", "post": "", "answer": 6, "hint": "Multiply the input by 2."},
                    {"phase": "substitute", "pre": "Now add 5: 6 + 5 = ", "post": "", "answer": 11, "hint": "Add the 5."},
                    {"phase": "substitute", "pre": "Check: 2 × 3 + 5 = ", "post": "", "answer": 11,
                     "done": "Input 3 gives output 11, so f(3) = 11.", "hint": "Multiply then add."},
                ],
            },
            {  # B4
                "display": "If \\(f(x) = x^2 - 1\\), find \\(f(-3)\\).",
                "solutions": [8],
                "calculator": False,
                "input_type": "single_value",
                "hint": "A negative number squared is positive.",
                "misconceptions": [{
                    "pattern": "negative_square", "check": "negative_square", "expect": -10,
                    "message": "\\((-3)^2 = (-3) \\times (-3) = 9\\), positive. So \\(f(-3) = 9 - 1 = 8\\). Getting " + MINUS + "10 treats \\((-3)^2\\) as " + MINUS + "9.",
                    "note": "(-3)^2 taken as -9 -> -10"
                }],
                "guided_steps": [
                    {"say": "\\(f(-3)\\) means put \\(x = -3\\) into \\(x^2 - 1\\). A negative squared is positive.",
                     "pre": "Square it: (" + MINUS + "3) × (" + MINUS + "3) = ", "post": "", "answer": 9, "hint": "Negative times negative is positive."},
                    {"phase": "substitute", "pre": "Now subtract 1: 9 " + MINUS + " 1 = ", "post": "", "answer": 8, "hint": "Take away 1."},
                    {"phase": "substitute", "pre": "Check: (" + MINUS + "3) squared is 9, minus 1 = ", "post": "", "answer": 8,
                     "done": "So f(" + MINUS + "3) = 8.", "hint": "Nine minus one."},
                ],
            },
            {  # B5 (MC)
                "display": "Find the nth term of \\(3, 6, 11, 18, 27, ...\\)",
                "options": ["\\(n^2 + 2\\)", "\\(n^2 + 3\\)", "\\(2n^2 + 1\\)", "\\(n^2 + n + 1\\)"],
                "solutions": [0],
                "calculator": False,
                "input_type": "multiple_choice",
                "hint": "Second difference gives a; then find the constant remainder.",
                "misconceptions": [{
                    "expect": None, "pattern": "explain",
                    "message": "First differences 3, 5, 7, 9; second difference 2, so \\(a = 1\\). Subtract \\(n^2\\): 2, 2, 2, 2, 2. The nth term is \\(n^2 + 2\\).",
                }],
            },
            {  # B6
                "display": "If \\(f(x) = 4x - 3\\), solve \\(f(x) = 13\\).",
                "solutions": [4],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Undo the minus 3 by adding, then undo the times 4 by dividing.",
                "misconceptions": [{
                    "pattern": "wrong_inverse", "check": "wrong_inverse", "expect": 2.5,
                    "message": "To undo \\(-3\\) you ADD 3: \\(13 + 3 = 16\\), then \\(16 \\div 4 = 4\\). Subtracting 3 gives \\(10 \\div 4 = 2.5\\), the wrong way.",
                    "note": "subtracts 3: (13-3)/4=2.5"
                }],
                "guided_steps": [
                    {"say": "Solve \\(4x - 3 = 13\\). Undo the \\(-3\\) first by adding.",
                     "pre": "Add 3 to both sides: 13 + 3 = ", "post": "", "answer": 16, "hint": "Undo the minus 3."},
                    {"phase": "substitute", "pre": "Now undo the ×4: 16 ÷ 4 = ", "post": "", "answer": 4, "hint": "Divide by 4."},
                    {"phase": "substitute", "pre": "Check: 4 × 4 " + MINUS + " 3 = ", "post": "", "answer": 13,
                     "done": "x = 4 gives 13, so it is right.", "hint": "Sixteen minus three."},
                ],
            },
            {  # B7 (fixed: 3n^2 to remove duplicate answer 4)
                "display": "The nth term of a quadratic sequence starts \\(3n^2\\). What is the 2nd difference?",
                "solutions": [6],
                "calculator": False,
                "input_type": "single_value",
                "hint": "For an squared the second difference is twice the coefficient.",
                "misconceptions": [{
                    "pattern": "forgot_double", "check": "forgot_double", "expect": 3,
                    "message": "For \\(an^2\\) the second difference is \\(2a\\), not \\(a\\). Here \\(a = 3\\), so \\(2 \\times 3 = 6\\). Giving 3 skips the doubling.",
                    "note": "reports a not 2a"
                }],
                "guided_steps": [
                    {"say": "For a sequence \\(an^2\\), the second difference is always \\(2a\\).",
                     "pre": "The number in front of n² is a = ", "post": "", "answer": 3, "hint": "Read it from 3n²."},
                    {"phase": "substitute", "pre": "Double it: 2 × 3 = ", "post": "", "answer": 6, "hint": "Second difference is 2a."},
                    {"phase": "substitute", "pre": "Check by halving back: 6 ÷ 2 = ", "post": "", "answer": 3,
                     "done": "Halving returns a = 3, so the second difference is 6.", "hint": "Six divided by two."},
                ],
            },
            {  # B8 (fixed: x1=4 to remove duplicate answer 11)
                "display": "Using \\(x_{n+1} = x_n + 3\\) with \\(x_1 = 4\\), find \\(x_4\\).",
                "solutions": [13],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Add 3 each time, and stop at the 4th term.",
                "misconceptions": [{
                    "pattern": "stopped_early", "check": "stopped_early", "expect": 10,
                    "message": "\\(x_2 = 7, x_3 = 10, x_4 = 13\\). Stopping at \\(x_3 = 10\\) is one step short of \\(x_4\\).",
                    "note": "gives x3 not x4"
                }],
                "guided_steps": [
                    {"say": "Start at \\(x_1 = 4\\) and add 3 each step until \\(x_4\\).",
                     "pre": "x₂ = 4 + 3 = ", "post": "", "answer": 7, "hint": "Add 3 to the first term."},
                    {"phase": "substitute", "pre": "x₃ = 7 + 3 = ", "post": "", "answer": 10, "hint": "Add 3 again."},
                    {"phase": "substitute", "pre": "x₄ = 10 + 3 = ", "post": "", "answer": 13,
                     "done": "Four terms: 4, 7, 10, 13, so x₄ = 13.", "hint": "Add 3 once more."},
                ],
            },
        ],
        "silver": [
            {  # S1 (MC)
                "display": "Find the nth term of \\(0, 3, 8, 15, 24, ...\\)",
                "options": ["\\(n^2 - 1\\)", "\\(n^2 + 1\\)", "\\(n^2 - n\\)", "\\((n-1)^2\\)"],
                "solutions": [0],
                "calculator": False,
                "input_type": "multiple_choice",
                "hint": "Second difference gives a, then find the constant remainder.",
                "misconceptions": [{
                    "expect": None, "pattern": "explain",
                    "message": "First differences 3, 5, 7, 9; second difference 2, so \\(a = 1\\). Subtract \\(n^2\\): " + MINUS + "1, " + MINUS + "1, " + MINUS + "1, " + MINUS + "1, " + MINUS + "1. The nth term is \\(n^2 - 1\\).",
                }],
            },
            {  # S2
                "display": "If \\(f(x) = 3x - 1\\) and \\(g(x) = x^2\\), find \\(fg(2)\\).",
                "solutions": [11],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Do g first, then put its answer into f.",
                "misconceptions": [{
                    "pattern": "wrong_order", "check": "wrong_order", "expect": 25,
                    "message": "\\(fg(2)\\) does \\(g\\) first: \\(g(2) = 4\\), then \\(f(4) = 3 \\times 4 - 1 = 11\\). Doing \\(f\\) first gives \\(g(5) = 25\\), which is \\(gf(2)\\).",
                    "note": "computes gf(2)=25"
                }],
                "guided_steps": [
                    {"say": "\\(fg(2)\\) means \\(g\\) first, then \\(f\\). Start inside with \\(g(2)\\).",
                     "pre": "g(2) = 2 × 2 = ", "post": "", "answer": 4, "hint": "g squares the input."},
                    {"phase": "substitute", "pre": "Feed 4 into f: 3 × 4 = ", "post": "", "answer": 12, "hint": "Multiply by 3."},
                    {"phase": "substitute", "pre": "Now subtract 1: 12 " + MINUS + " 1 = ", "post": "", "answer": 11,
                     "done": "g first then f gives 11.", "hint": "Twelve minus one."},
                ],
            },
            {  # S3
                "display": "If \\(f(x) = 5x + 2\\), find \\(f^{-1}(x)\\). Then find \\(f^{-1}(17)\\).",
                "solutions": [3],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Reverse the steps: undo the plus 2, then undo the times 5.",
                "misconceptions": [{
                    "pattern": "applied_forward", "check": "applied_forward", "expect": 87,
                    "message": "\\(f^{-1}\\) reverses \\(f\\): \\(f^{-1}(x) = \\frac{x-2}{5}\\), so \\(f^{-1}(17) = 15 \\div 5 = 3\\). Putting 17 into \\(f\\) gives 87, the wrong direction.",
                    "note": "computes f(17)=87 forward"
                }],
                "guided_steps": [
                    {"say": "Reverse the function. From \\(y = 5x + 2\\), swap and rearrange: \\(f^{-1}(x) = \\frac{x - 2}{5}\\).",
                     "pre": "Undo the +2: 17 " + MINUS + " 2 = ", "post": "", "answer": 15, "hint": "Undo the plus 2 first."},
                    {"phase": "substitute", "pre": "Undo the ×5: 15 ÷ 5 = ", "post": "", "answer": 3, "hint": "Divide by 5."},
                    {"phase": "substitute", "pre": "Check with f: 5 × 3 + 2 = ", "post": "", "answer": 17,
                     "done": "f sends 3 back to 17, so f⁻¹(17) = 3.", "hint": "Put 3 into 5x + 2."},
                ],
            },
            {  # S4
                "display": "Using \\(x_{n+1} = \\frac{x_n^2 + 5}{4}\\) with \\(x_0 = 2\\), find \\(x_2\\) to 2 d.p.",
                "solutions": [2.52],
                "calculator": True,
                "input_type": "single_value",
                "hint": "Work out x1, then feed it back to get x2.",
                "misconceptions": [{
                    "pattern": "stopped_early", "check": "stopped_early", "expect": 2.25,
                    "message": "\\(x_1 = (2^2 + 5) \\div 4 = 2.25\\) is only the first step. Go again: \\(x_2 = (2.25^2 + 5) \\div 4 = 2.52\\).",
                    "note": "gives x1=2.25 not x2"
                }],
                "guided_steps": [
                    {"say": "Two iterations from \\(x_0 = 2\\). First \\(x_1\\), then feed it back for \\(x_2\\).",
                     "pre": "Top of x₁: 2² + 5 = ", "post": "", "answer": 9, "hint": "Square 2, then add 5."},
                    {"pre": "x₁ = 9 ÷ 4 = ", "post": "", "answer": 2.25, "hint": "Nine divided by four."},
                    {"phase": "substitute", "pre": "Top of x₂: 2.25² + 5 = ", "post": "", "answer": 10.0625, "hint": "Square 2.25, then add 5."},
                    {"phase": "substitute", "pre": "x₂ = 10.0625 ÷ 4, to 2 d.p. = ", "post": "", "answer": 2.52,
                     "done": "Two iterations: 2 to 2.25 to 2.52, so x₂ = 2.52.", "hint": "Divide by 4, round to 2 d.p."},
                ],
            },
            {  # S5 (MC)
                "display": "Find the nth term of \\(4, 10, 18, 28, 40, ...\\)",
                "options": ["\\(n^2 + 3n\\)", "\\(n^2 + 4\\)", "\\(2n^2 + 2n\\)", "\\(n^2 + 2n + 1\\)"],
                "solutions": [0],
                "calculator": False,
                "input_type": "multiple_choice",
                "hint": "Second difference is 2, so a is 1; then find the linear remainder.",
                "misconceptions": [{
                    "expect": None, "pattern": "explain",
                    "message": "First differences 6, 8, 10, 12; second difference 2, so \\(a = 1\\). Subtract \\(n^2\\): 3, 6, 9, 12, 15, which is \\(3n\\). The nth term is \\(n^2 + 3n\\).",
                }],
            },
            {  # S6
                "display": "If \\(f(x) = x^2 + 2\\) and \\(g(x) = 3x\\), find \\(gf(4)\\).",
                "solutions": [54],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Do f first, then put its answer into g.",
                "misconceptions": [{
                    "pattern": "wrong_order", "check": "wrong_order", "expect": 146,
                    "message": "\\(gf(4)\\) does \\(f\\) first: \\(f(4) = 18\\), then \\(g(18) = 54\\). Doing \\(g\\) first gives \\(f(12) = 146\\), which is \\(fg(4)\\).",
                    "note": "computes fg(4)=146"
                }],
                "guided_steps": [
                    {"say": "\\(gf(4)\\) means \\(f\\) first, then \\(g\\). Start inside with \\(f(4)\\).",
                     "pre": "Square 4: 4 × 4 = ", "post": "", "answer": 16, "hint": "Four squared."},
                    {"pre": "Finish f: 16 + 2 = ", "post": "", "answer": 18, "hint": "Add the 2."},
                    {"phase": "substitute", "pre": "Feed 18 into g: 3 × 18 = ", "post": "", "answer": 54, "hint": "Multiply by 3."},
                    {"phase": "substitute", "pre": "Check: g(f(4)) = 3 × 18 = ", "post": "", "answer": 54,
                     "done": "f first then g gives 54.", "hint": "Three times eighteen."},
                ],
            },
            {  # S7
                "display": "The first 3 terms of a quadratic sequence are \\(5, 12, 23\\). Find the next term.",
                "solutions": [38],
                "calculator": False,
                "input_type": "single_value",
                "hint": "The gaps grow by a constant amount; extend that pattern.",
                "misconceptions": [{
                    "pattern": "linear_assumption", "check": "linear_assumption", "expect": 34,
                    "message": "The gaps are 7 then 11, so they grow by 4 each time. The next gap is \\(11 + 4 = 15\\), giving \\(23 + 15 = 38\\). Adding 11 again gives 34, treating it as linear.",
                    "note": "adds 11 again: 23+11=34"
                }],
                "guided_steps": [
                    {"say": "In a quadratic sequence the gaps grow by a fixed amount. Find the first gaps.",
                     "pre": "12 " + MINUS + " 5 = ", "post": "", "answer": 7, "hint": "Subtract the first two terms."},
                    {"pre": "23 " + MINUS + " 12 = ", "post": "", "answer": 11, "hint": "Subtract the next pair."},
                    {"phase": "substitute", "pre": "The gaps grow by 11 " + MINUS + " 7 = ", "post": "", "answer": 4, "hint": "Difference of the gaps."},
                    {"phase": "substitute", "pre": "Next gap 11 + 4 = 15, so next term 23 + 15 = ", "post": "", "answer": 38,
                     "done": "The next term is 38.", "hint": "Twenty-three plus fifteen."},
                ],
            },
        ],
        "gold": [
            {  # G1 (MC)
                "display": "Find the nth term of \\(2, 8, 18, 32, 50, ...\\)",
                "options": ["\\(2n^2\\)", "\\(n^2 + n\\)", "\\(2n^2 + 1\\)", "\\(n^2 + 2n - 1\\)"],
                "solutions": [0],
                "calculator": False,
                "input_type": "multiple_choice",
                "hint": "Second difference is 4, so a is 2; the remainder is zero.",
                "misconceptions": [{
                    "expect": None, "pattern": "explain",
                    "message": "First differences 6, 10, 14, 18; second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): all zero. The nth term is \\(2n^2\\).",
                }],
            },
            {  # G2
                "display": "If \\(f(x) = \\frac{2x+1}{x-3}\\), find \\(f^{-1}(x)\\). Enter the numerator coefficient of x.",
                "solutions": [3],
                "calculator": False,
                "input_type": "single_value",
                "hint": "Cross-multiply, gather the x terms, then read the numerator of the inverse.",
                "misconceptions": [{
                    "pattern": "kept_original_coeff", "check": "kept_original_coeff", "expect": 2,
                    "message": "After rearranging, \\(f^{-1}(x) = \\frac{3x+1}{x-2}\\), so the numerator coefficient of x is 3. Reading 2 just copies the original numerator.",
                    "note": "copies the 2 from 2x+1"
                }],
                "guided_steps": [
                    {"say": "Let \\(y = \\frac{2x+1}{x-3}\\). Multiply out: \\(y(x-3) = 2x+1\\), so \\(xy - 3y = 2x + 1\\). Gather x on one side: \\(x(y-2) = 3y + 1\\).",
                     "pre": "In that numerator 3y + 1, the number multiplying y is ", "post": "", "answer": 3, "hint": "The coefficient of y in 3y + 1."},
                    {"phase": "substitute", "pre": "The constant added in that numerator is ", "post": "", "answer": 1, "hint": "The number after 3y."},
                    {"phase": "substitute", "pre": "Swapping letters, \\(f^{-1}(x) = \\frac{3x+1}{x-2}\\); its numerator coefficient of x is ", "post": "", "answer": 3,
                     "done": "The inverse is (3x + 1)/(x " + MINUS + " 2), so the coefficient asked for is 3.", "hint": "Read the number in front of x in 3x + 1."},
                ],
            },
            {  # G3
                "display": "Using \\(x_{n+1} = \\sqrt{5x_n + 2}\\) with \\(x_0 = 3\\), find the value the sequence converges to (1 d.p.).",
                "solutions": [5.4],
                "calculator": True,
                "input_type": "single_value",
                "hint": "At the limit x stops changing, so solve x equals the square root expression.",
                "misconceptions": [{
                    "pattern": "stopped_early", "check": "stopped_early", "expect": 4.1,
                    "message": "\\(x_1 = \\sqrt{5 \\times 3 + 2} = \\sqrt{17} = 4.1\\) is just the first step. The limit \\(L\\) satisfies \\(L = \\sqrt{5L + 2}\\), giving \\(L = 5.4\\).",
                    "note": "sqrt(17)=4.12 -> 4.1"
                }],
                "guided_steps": [
                    {"say": "At the limit the value stops changing, so \\(x = \\sqrt{5x + 2}\\). Square both sides: \\(x^2 = 5x + 2\\), i.e. \\(x^2 - 5x - 2 = 0\\).",
                     "pre": "Under the quadratic-formula root, 5² + 8 = ", "post": "", "answer": 33, "hint": "b² " + MINUS + " 4ac = 25 " + MINUS + " (" + MINUS + "8)."},
                    {"phase": "substitute", "pre": "√33 to 2 d.p. = ", "post": "", "answer": 5.74, "hint": "Square root of 33 on the calculator."},
                    {"phase": "substitute", "pre": "x = (5 + 5.74) ÷ 2, to 1 d.p. = ", "post": "", "answer": 5.4,
                     "done": "Taking the positive root, the sequence converges to 5.4.", "hint": "Add, halve, round to 1 d.p."},
                ],
            },
            {  # G4 (MC)
                "display": "Find the nth term of \\(1, 7, 17, 31, 49, ...\\)",
                "options": ["\\(2n^2 - 1\\)", "\\(2n^2 + 1\\)", "\\(n^2 + 2n - 2\\)", "\\(3n^2 - 2n\\)"],
                "solutions": [0],
                "calculator": False,
                "input_type": "multiple_choice",
                "hint": "Second difference is 4, so a is 2; then find the constant remainder.",
                "misconceptions": [{
                    "expect": None, "pattern": "explain",
                    "message": "First differences 6, 10, 14, 18; second difference 4, so \\(a = 2\\). Subtract \\(2n^2\\): " + MINUS + "1, " + MINUS + "1, " + MINUS + "1, " + MINUS + "1, " + MINUS + "1. The nth term is \\(2n^2 - 1\\).",
                }],
            },
            {  # G5 (two_solutions)
                "display": "If \\(f(x) = x^2\\) and \\(g(x) = 2x - 1\\), solve \\(fg(x) = 25\\).",
                "solutions": [3, -2],
                "calculator": False,
                "input_type": "two_solutions",
                "hint": "Build the composite, set it to 25, and take both square roots.",
                "misconceptions": [{
                    "pattern": "missed_negative_root", "check": "missed_negative_root", "expect": None,
                    "message": "\\((2x-1)^2 = 25\\) gives \\(2x - 1 = 5\\) OR \\(2x - 1 = -5\\), so \\(x = 3\\) and \\(x = -2\\). Taking only the plus root misses \\(x = -2\\).",
                    "note": "only positive root, partial pair"
                }],
                "guided_steps": [
                    {"say": "\\(fg(x)\\) does \\(g\\) first: \\(f(2x-1) = (2x-1)^2\\). Set it to 25, so \\(2x - 1 = \\pm 5\\).",
                     "pre": "Square root of 25 = ", "post": "", "answer": 5, "hint": "What squared gives 25?"},
                    {"phase": "substitute", "pre": "Plus case: 2x " + MINUS + " 1 = 5, so 2x = 6 and x = 6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Add 1, then halve."},
                    {"phase": "substitute", "pre": "Minus case: 2x " + MINUS + " 1 = " + MINUS + "5, so 2x = " + MINUS + "4 and x = " + MINUS + "4 ÷ 2 = ", "post": "", "answer": -2,
                     "done": "Both roots: x = 3 and x = " + MINUS + "2.", "hint": "Add 1, then halve."},
                ],
            },
        ],
    },
    "related_videos": [],
    "worked_examples": [
        {
            "steps": [
                {"label": "Step 1: Differences", "content": "<p>1st: 4, 6, 8, 10. 2nd: 2. So a = 1.</p>"},
                {"label": "Step 2: Subtract n squared", "content": "<p>2" + MINUS + "1, 6" + MINUS + "4, 12" + MINUS + "9, 20" + MINUS + "16 = 1, 2, 3, 4 " + ARROW + " linear part = n</p>"},
                {"label": "Answer", "content": "<p><strong>\\(n^2 + n\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
            "question": "Find the nth term of 2, 6, 12, 20, 30, ...",
            "difficulty": "Bronze",
        },
        {
            "steps": [
                {"label": "f(4)", "content": "<p>3(4) + 1 = 13</p>"},
                {"label": "Inverse", "content": "<p>y = 3x+1 " + ARROW + " x = (y" + MINUS + "1)/3 " + ARROW + " f⁻¹(x) = (x" + MINUS + "1)/3</p>"},
                {"label": "Answer", "content": "<p><strong>f(4) = 13, f⁻¹(x) = (x" + MINUS + "1)/3</strong></p>", "isAnswer": True, "is_answer": True},
            ],
            "question": "If f(x) = 3x + 1, find f(4) and f⁻¹(x)",
            "difficulty": "Silver",
        },
        {
            "steps": [
                {"label": "x1", "content": "<p>(1 + 3)/5 = 0.8</p>"},
                {"label": "x2", "content": "<p>(0.64 + 3)/5 = 0.728</p>"},
                {"label": "x3", "content": "<p>(0.529984 + 3)/5 = 0.706</p>"},
                {"label": "Answer", "content": "<p><strong>x₃ ≈ 0.706</strong></p>", "isAnswer": True, "is_answer": True},
            ],
            "question": "Using xₙ₊₁ = (xₙ² + 3)/5 with x₀ = 1, find x₃ to 3 d.p.",
            "difficulty": "Gold",
        },
    ],
    "guided": {
        "opener": {
            "label": "Before any algebra",
            "display": opener_display,
            "steps": [
                {"say": "No algebra allowed. Count the squares in each pattern: 3, 8, 15.",
                 "pre": "From pattern 1 to pattern 2, how many extra squares? 8 " + MINUS + " 3 = ", "post": "", "answer": 5, "hint": "Eight take away three."},
                {"pre": "From pattern 2 to pattern 3: 15 " + MINUS + " 8 = ", "post": "", "answer": 7, "hint": "Fifteen take away eight."},
                {"say": "The jumps were 5 then 7, so the jump itself is growing.",
                 "pre": "How much did the jump grow by? 7 " + MINUS + " 5 = ", "post": "", "answer": 2,
                 "done": "That steady growth of the jump is the second difference.", "hint": "How much bigger is the second jump than the first?"},
                {"say": "That steady growth of the jump, always 2, is the <strong>second difference</strong>. When it stays constant the sequence is <strong>quadratic</strong>: its nth term has an \\(n^2\\). Halve the second difference for the number in front of \\(n^2\\) (here \\(2 \\div 2 = 1\\)), and these really are \\(n^2 + 2n\\): 3, 8, 15, 24."},
            ],
        },
        "teach": {
            "bronze": {
                "display": "If \\(f(x) = 3x - 2\\), find \\(f(6)\\)",
                "label": "Together: your first one",
                "steps": [
                    {"say": "\\(f(6)\\) means put \\(x = 6\\) into \\(3x - 2\\). Read the input first.",
                     "pre": "The input x is ", "post": "", "answer": 6, "hint": "The number inside the brackets."},
                    {"pre": "Work out 3 × 6 = ", "post": "", "answer": 18, "hint": "Multiply the input by 3."},
                    {"pre": "Now subtract 2: 18 " + MINUS + " 2 = ", "post": "", "answer": 16, "hint": "Take away 2."},
                    {"pre": "Check: 3 × 6 " + MINUS + " 2 = ", "post": "", "answer": 16,
                     "done": "Input 6 gives output 16. That is all f(6) asks.", "hint": "Multiply then subtract."},
                ],
            },
            "silver": {
                "display": "If \\(f(x) = 2x + 3\\) and \\(g(x) = x^2\\), find \\(fg(4)\\)",
                "label": "Together: the silver move",
                "steps": [
                    {"say": "\\(fg(4)\\) does \\(g\\) first, then \\(f\\). Start inside with \\(g(4)\\).",
                     "pre": "g first: 4 × 4 = ", "post": "", "answer": 16, "hint": "g squares the input."},
                    {"pre": "Feed 16 into f: 2 × 16 = ", "post": "", "answer": 32, "hint": "Multiply by 2."},
                    {"pre": "Add 3: 32 + 3 = ", "post": "", "answer": 35, "hint": "Add the 3."},
                    {"pre": "Check: f(g(4)) = 2 × 16 + 3 = ", "post": "", "answer": 35,
                     "done": "Inside function first, every time. gf would differ.", "hint": "Multiply then add."},
                ],
            },
            "gold": {
                "display": "Find the nth term of \\(4, 13, 26, 43, 64, ...\\)",
                "label": "Together: the gold move",
                "steps": [
                    {"say": "A full quadratic nth term. First the second difference.",
                     "pre": "First gaps 9 and 13. Second difference: 13 " + MINUS + " 9 = ", "post": "", "answer": 4, "hint": "Difference of the differences."},
                    {"pre": "Halve it for the n² coefficient: 4 ÷ 2 = ", "post": "", "answer": 2, "hint": "a is the second difference divided by 2."},
                    {"say": "Now subtract \\(2n^2\\) from each term to leave a linear sequence.",
                     "pre": "Term 1: 4 " + MINUS + " 2 × 1² = 4 " + MINUS + " 2 = ", "post": "", "answer": 2, "hint": "2 times 1 squared is 2."},
                    {"pre": "Term 2: 13 " + MINUS + " 2 × 2² = 13 " + MINUS + " 8 = ", "post": "", "answer": 5, "hint": "2 times 2 squared is 8."},
                    {"say": "The remainder 2, 5, 8, ... rises by 3, giving \\(3n - 1\\). So the nth term is \\(2n^2 + 3n - 1\\).",
                     "pre": "Check term 3: 2 × 3² + 3 × 3 " + MINUS + " 1 = 18 + 9 " + MINUS + " 1 = ", "post": "", "answer": 26,
                     "done": "Matches the sequence, so the nth term is 2n² + 3n " + MINUS + " 1.", "hint": "18 + 9 minus 1."},
                ],
            },
        },
    },
    "tier_guides": {
        "bronze": {
            "title": "Bronze: put one value in",
            "steps": [
                "Function notation \\(f(x)\\) is a machine: whatever sits in the brackets replaces every \\(x\\). \\(f(3)\\) means swap \\(x\\) for 3, then work it out.",
                "For a sequence, the <strong>second difference</strong> is the difference of the first differences. A constant one means the sequence is quadratic.",
                "Take care squaring negatives: \\((-3)^2 = 9\\), never \\(-9\\) or \\(-6\\).",
            ],
            "example": {
                "question": "If f(x) = 3x + 2, find f(4)",
                "steps": [
                    {"label": "Substitute", "content": "<p>Replace \\(x\\) with 4: \\(3 \\times 4 + 2\\)</p>"},
                    {"label": "Work out", "content": "<p>\\(12 + 2 = 14\\)</p>"},
                    {"label": "Check", "content": "<p>Input 4, output 14</p>"},
                    {"label": "Answer", "content": "<p>\\(f(4) = 14\\)</p>", "isAnswer": True, "is_answer": True},
                ],
            },
        },
        "silver": {
            "title": "Silver: two linked steps",
            "steps": [
                "Composite \\(fg(x)\\) works inside out: do \\(g\\) first, then put its answer into \\(f\\). Order matters, so \\(fg\\) and \\(gf\\) usually differ.",
                "An inverse \\(f^{-1}(x)\\) undoes \\(f\\). Write \\(y = f(x)\\), swap \\(x\\) and \\(y\\), then make \\(y\\) the subject.",
                "An iteration formula feeds each answer back in: find \\(x_1\\), then reuse it to reach \\(x_2\\).",
            ],
            "example": {
                "question": "If f(x) = x + 4 and g(x) = x squared, find fg(2)",
                "steps": [
                    {"label": "Inside first", "content": "<p>\\(g(2) = 2^2 = 4\\)</p>"},
                    {"label": "Then outside", "content": "<p>\\(f(4) = 4 + 4 = 8\\)</p>"},
                    {"label": "Check", "content": "<p>g first, then f: 8</p>"},
                    {"label": "Answer", "content": "<p>\\(fg(2) = 8\\)</p>", "isAnswer": True, "is_answer": True},
                ],
            },
        },
        "gold": {
            "title": "Gold: the full method",
            "steps": [
                "For a quadratic nth term, halve the second difference to get \\(a\\), then subtract \\(an^2\\) from every term to leave a linear sequence.",
                "Find the nth term of that leftover (constant difference \\(b\\)); the result is \\(an^2 + bn + c\\).",
                "To solve \\(fg(x) = k\\), build the composite, set it equal to \\(k\\), and solve. To iterate to a root, repeat the formula until the digits settle.",
            ],
            "example": {
                "question": "Find the nth term of 4, 13, 28, 49, ...",
                "steps": [
                    {"label": "Second difference", "content": "<p>Gaps 9, 15, 21; second difference 6, so \\(a = 3\\)</p>"},
                    {"label": "Subtract 3n squared", "content": "<p>\\(4-3=1,\\ 13-12=1,\\ 28-27=1\\): remainder 1</p>"},
                    {"label": "Combine", "content": "<p>\\(3n^2 + 1\\)</p>"},
                    {"label": "Check", "content": "<p>\\(n=2:\\ 3(4)+1 = 13\\)</p>"},
                    {"label": "Answer", "content": "<p>\\(3n^2 + 1\\)</p>", "isAnswer": True, "is_answer": True},
                ],
            },
        },
    },
}

out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/lesson_maths-ocr_algebra-L14.json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(practice_data, f, indent=1, ensure_ascii=False)
print("wrote", out)
# quick self-check: no em dash anywhere student-facing
def walk(o, p):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            walk(v, p + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, p + "[%d]" % i)
    elif isinstance(o, str) and "—" in o:
        print("EMDASH", p)
walk(practice_data, "pd")
print("emdash scan done")
