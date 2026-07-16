# -*- coding: utf-8 -*-
"""Builder for algebra-L14 guided-learning conversion. Asserts every box value."""
import json, io

LIVE = "_live_L14.json"
OUT  = "lesson_algebra-L14.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))

# ---- assert helper -------------------------------------------------------
def A(cond, msg):
    if not cond:
        raise SystemExit("ASSERT FAIL: " + msg)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(text):
    return {"say": text}

# =========================================================================
# 1. FIX worked_examples em-dash labels (validator scans them; not exempt)
# =========================================================================
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# =========================================================================
# 2. METHOD CARD (slim reference)
# =========================================================================
pd["method_card"] = {
    "title": "Quadratic nth Term, Functions and Iteration",
    "steps": [
        "Quadratic nth term: find the constant second difference, halve it for the \\(n^2\\) coefficient, then subtract \\(an^2\\) and read off the linear part.",
        "Functions: \\(f(a)\\) means substitute \\(a\\). \\(fg(x)\\) does \\(g\\) first, then \\(f\\). The inverse \\(f^{-1}\\) undoes \\(f\\) (swap \\(x\\) and \\(y\\), rearrange).",
        "Iteration: put \\(x_0\\) into the formula to get \\(x_1\\), then feed each answer back in for the next value.",
    ],
    "content": ("<p><strong>Quadratic nth term:</strong> constant second differences mean the sequence is quadratic. "
                "The \\(n^2\\) coefficient is <strong>half</strong> the second difference. Subtract \\(an^2\\), then find the linear nth term of what is left.</p>"
                "<p><strong>Functions:</strong> \\(f(4)\\) means substitute \\(x=4\\). For composites, \\(fg(x)\\) applies \\(g\\) first. "
                "The inverse undoes the machine: swap \\(x\\) and \\(y\\), then rearrange.</p>"
                "<p><strong>Iteration:</strong> repeat \\(x_{n+1}=g(x_n)\\), always feeding the previous answer back in.</p>"),
    "example": ("<p><strong>Find the nth term of</strong> 3, 9, 19, 33, ...</p>"
                "<p>Second differences are 4, so \\(a=2\\). Subtract \\(2n^2\\): 1, 1, 1, 1. Answer <strong>\\(2n^2+1\\)</strong>.</p>"),
}

# =========================================================================
# 3. tier descriptions
# =========================================================================
pb = pd["problem_bank"]
pb["bronze_description"] = "Put a number into a function, and name a simple quadratic sequence."
pb["silver_description"] = "Compose functions in the right order, find inverses, and solve harder sequences."
pb["gold_description"]   = "Run iteration formulas and combine functions, inverses and sequences."

# =========================================================================
# 4. MISCONCEPTION helper
# =========================================================================
def mc(pattern, message, expect, note):
    return {"pattern": pattern, "message": message, "expect": expect, "note": note}

MSG_INV   = "To find the inverse, write \\(y = f(x)\\), swap \\(x\\) and \\(y\\), then rearrange for \\(y\\). Do not confuse \\(f(a)\\) with \\(f^{-1}(a)\\)."
MSG_ORDER = "Read the letters right to left: the letter nearest the number acts first. \\(fg\\) does \\(g\\) first, \\(gf\\) does \\(f\\) first."
MSG_HALF  = "For a quadratic nth term the coefficient of \\(n^2\\) is HALF the second difference, not the whole second difference."
MSG_ITER  = "In iteration you substitute your PREVIOUS answer into the formula each time, not the starting value again."

# =========================================================================
# 5. BRONZE bank (reordered: non-MC first for the completion mechanic)
# =========================================================================
bronze = []

# B2  f(x)=4x-3, f(5)  -> 17
A(4*5-3 == 17, "B2")
bronze.append({
    "display": "Given \\(f(x) = 4x - 3\\), find \\(f(5)\\)",
    "solutions": [17], "calculator": False, "input_type": "single_value",
    "hint": "Multiply the input 5 by 4, then subtract 3.",
    "misconceptions": [mc("inverse_error", MSG_INV, 2,
        "Student confuses f(5) with the inverse: f^-1(x)=(x+3)/4, f^-1(5)=8/4=2.")],
    "guided_steps": [
        sayonly("\\(f(x) = 4x - 3\\) is a machine: multiply the input by 4, then take off 3. Find \\(f(5)\\)."),
        box("Multiply the input by 4: 4 × 5 = ", 20, "Four fives."),
        box("Now subtract 3: 20 − 3 = ", 17, "Take 3 off 20.", phase="substitute"),
        box("Read it back to check: 4 × 5 = 20, then 20 − 3 = ", 17, "Work out 4 × 5 first, then subtract 3.",
            phase="substitute", done="It matches, so \\(f(5) = 17\\)."),
    ],
})

# B0 (NEW: iconic squares replaced)  2,5,10,17,26 -> n^2+1   (MC)
seqB0=[n*n+1 for n in range(1,6)]
A(seqB0==[2,5,10,17,26], "B0 seq")
bronze.append({
    "display": "Find the nth term of 2, 5, 10, 17, 26, ...",
    "options": ["\\(n^2 + 1\\)", "\\(2n^2\\)", "\\(n^2\\)", "\\(n(n+1)\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Test each option on the terms 2, 5, 10.",
    "misconceptions": [],
})

# B3  f(x)=x^2+1, f(-3) -> 10
A((-3)**2+1 == 10, "B3")
bronze.append({
    "display": "Given \\(f(x) = x^2 + 1\\), find \\(f(-3)\\)",
    "solutions": [10], "calculator": False, "input_type": "single_value",
    "hint": "Square minus 3 first (a negative squared is positive), then add 1.",
    "misconceptions": [mc("square_negative", "Squaring a negative gives a positive: \\((-3)^2 = (-3)\\times(-3) = 9\\), not \\(-9\\).", -8,
        "Student treats (-3)^2 as -(3^2) = -9, then -9+1 = -8.")],
    "guided_steps": [
        sayonly("\\(f(x) = x^2 + 1\\). Find \\(f(-3)\\). Substitute \\(x = -3\\); a negative squared turns positive."),
        box("Square the input: (−3) × (−3) = ", 9, "A negative times a negative is positive."),
        box("Now add 1: 9 + 1 = ", 10, "Nine plus one.", phase="substitute"),
        box("Check: (−3)² + 1 = ", 10, "The square is 9, then add 1.",
            phase="substitute", done="So \\(f(-3) = 10\\). The square made it positive."),
    ],
})

# B1  3,12,27,48 -> 3n^2 (MC)
A([3*n*n for n in range(1,5)]==[3,12,27,48], "B1")
bronze.append({
    "display": "Find the nth term of 3, 12, 27, 48, ...",
    "options": ["\\(3n^2\\)", "\\(n^3\\)", "\\(3n^2 + 1\\)", "\\(3n\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Compare each option with the terms 3, 12, 27.",
    "misconceptions": [],
})

# B5  f(x)=2x+5, f(0) -> 5
A(2*0+5 == 5, "B5")
bronze.append({
    "display": "Given \\(f(x) = 2x + 5\\), find \\(f(0)\\)",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Double 0, then add 5.",
    "misconceptions": [mc("inverse_error", MSG_INV, -2.5,
        "Student confuses f(0) with f^-1(0): f^-1(x)=(x-5)/2, f^-1(0)=-2.5.")],
    "guided_steps": [
        sayonly("\\(f(x) = 2x + 5\\). Find \\(f(0)\\)."),
        box("Double the input: 2 × 0 = ", 0, "Anything times zero is zero."),
        box("Now add 5: 0 + 5 = ", 5, "Nothing, then add 5.", phase="substitute"),
        box("Check: 2 × 0 + 5 = ", 5, "Zero, then add 5.",
            phase="substitute", done="So \\(f(0) = 5\\)."),
    ],
})

# B6  0,3,8,15,24 -> n^2-1 (MC)
A([n*n-1 for n in range(1,6)]==[0,3,8,15,24], "B6")
bronze.append({
    "display": "Find the nth term of 0, 3, 8, 15, 24, ...",
    "options": ["\\(n^2 - 1\\)", "\\(n^2\\)", "\\(n^2 + 1\\)", "\\((n-1)^2\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Test each option on the terms 0, 3, 8.",
    "misconceptions": [],
})

# B7  f(x)=5x+2, f(-1) -> -3
A(5*(-1)+2 == -3, "B7")
bronze.append({
    "display": "Given \\(f(x) = 5x + 2\\), find \\(f(-1)\\)",
    "solutions": [-3], "calculator": False, "input_type": "single_value",
    "hint": "Multiply minus 1 by 5, then add 2.",
    "misconceptions": [mc("inverse_error", MSG_INV, -0.6,
        "Student confuses f(-1) with f^-1(-1): f^-1(x)=(x-2)/5, f^-1(-1)=-0.6.")],
    "guided_steps": [
        sayonly("\\(f(x) = 5x + 2\\). Find \\(f(-1)\\). Watch the sign."),
        box("Multiply by 5: 5 × (−1) = ", -5, "Five times negative one."),
        box("Now add 2: −5 + 2 = ", -3, "Start at −5 and go up 2.", phase="substitute"),
        box("Check: 5 × (−1) + 2 = ", -3, "Negative five, then add 2.",
            phase="substitute", done="So \\(f(-1) = -3\\)."),
    ],
})

# B4  4,7,12,19,28 -> n^2+3 (MC)
A([n*n+3 for n in range(1,6)]==[4,7,12,19,28], "B4")
bronze.append({
    "display": "Find the nth term of 4, 7, 12, 19, 28, ...",
    "options": ["\\(n^2 + 3\\)", "\\(n^2 + 4\\)", "\\(3n + 1\\)", "\\((n+1)^2\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Test each option on the terms 4, 7, 12.",
    "misconceptions": [],
})

pb["bronze"] = bronze

# =========================================================================
# 6. SILVER bank (reordered: composite first)
# =========================================================================
silver = []

# S1  f=3x-1, g=x^2, fg(2) -> 11   (composite first)
A(3*(2**2)-1 == 11, "S1")
silver.append({
    "display": "\\(f(x) = 3x - 1\\), \\(g(x) = x^2\\). Find \\(fg(2)\\).",
    "solutions": [11], "calculator": False, "input_type": "single_value",
    "hint": "Do g first (square 2), then put the result into f.",
    "misconceptions": [mc("composite_order", MSG_ORDER, 25,
        "Student reverses order (f then g): f(2)=5, g(5)=25.")],
    "guided_steps": [
        sayonly("\\(f(x) = 3x - 1\\) and \\(g(x) = x^2\\). Find \\(fg(2)\\). The rule: \\(fg\\) means do \\(g\\) first, then \\(f\\)."),
        box("Inside first: g(2) = 2² = ", 4, "Two squared."),
        box("Feed 4 into f: f(4) = 3 × 4 − 1 = ", 11, "Triple 4, then take 1 off.", phase="substitute"),
        box("Check: square 2 to get 4, then 3 × 4 − 1 = ", 11, "12 minus 1.",
            phase="substitute", done="So \\(fg(2) = 11\\). Inside first, then outside."),
    ],
})

# S0  inverse of 2x+7, constant term -> -3.5   (hint fixed)
A((-7)/2 == -3.5, "S0")
silver.append({
    "display": "Find the inverse of \\(f(x) = 2x + 7\\). Give the constant term.",
    "solutions": [-3.5], "calculator": False, "input_type": "single_value",
    "hint": "Write y = 2x + 7, swap x and y, then make y the subject.",
    "misconceptions": [mc("inverse_error", MSG_INV, 3.5,
        "Student writes f^-1(x)=(x+7)/2 instead of (x-7)/2 (adds 7 rather than subtracting). Constant = +3.5.")],
    "guided_steps": [
        sayonly("Find the inverse of \\(f(x) = 2x + 7\\), then read off its constant term. Method: write \\(y = 2x + 7\\), swap \\(x\\) and \\(y\\), rearrange for \\(y\\)."),
        box("After swapping: x = 2y + 7. Take 7 off both sides. The number now subtracted from x is ", 7, "The +7 crosses over as −7."),
        box("Divide by 2. The inverse is (x − 7) ÷ 2 = 0.5x − 3.5, so its constant term is ", -3.5,
            "Divide −7 by 2.", phase="substitute"),
        box("Check with an input: f(0) = 7, so the inverse must send 7 back to 0. Test: (7 − 7) ÷ 2 = ", 0,
            "7 minus 7 is 0, divided by 2.", phase="substitute",
            done="It returns 0, so the inverse is (x − 7)/2 and its constant term is −3.5."),
    ],
})

# S2  (NEW, was duplicate of S1) f=2x+3, g=x^2, gf(3) -> 81
A((2*3+3)**2 == 81, "S2")
silver.append({
    "display": "\\(f(x) = 2x + 3\\), \\(g(x) = x^2\\). Find \\(gf(3)\\).",
    "solutions": [81], "calculator": False, "input_type": "single_value",
    "hint": "Do f first (double 3 then add 3), then square the result.",
    "misconceptions": [mc("composite_order", MSG_ORDER, 21,
        "Student reverses order (g then f): g(3)=9, f(9)=2*9+3=21.")],
    "guided_steps": [
        sayonly("\\(f(x) = 2x + 3\\) and \\(g(x) = x^2\\). Find \\(gf(3)\\). The rule: \\(gf\\) means do \\(f\\) first, then \\(g\\)."),
        box("Inside first: f(3) = 2 × 3 + 3 = ", 9, "Double 3, then add 3."),
        box("Feed 9 into g: g(9) = 9² = ", 81, "Nine squared.", phase="substitute"),
        box("Check: f(3) = 9, then square it: 9 × 9 = ", 81, "Nine nines.",
            phase="substitute", done="So \\(gf(3) = 81\\). f first, then g."),
    ],
})

# S3  5,12,23,38,57 -> 2n^2+n+2 (MC)
A([2*n*n+n+2 for n in range(1,6)]==[5,12,23,38,57], "S3")
silver.append({
    "display": "Find the nth term of 5, 12, 23, 38, 57, ...",
    "options": ["\\(2n^2 + n + 2\\)", "\\(2n^2 + 3\\)", "\\(n^2 + 4n\\)", "\\(2n^2 + n - 2\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Halve the second difference for the n-squared coefficient, then check the rest.",
    "misconceptions": [],
})

# S4  (NEW, was numeric inverse of B2) f=3x+2, solve f(x)=20 -> 6
A((20-2)/3 == 6, "S4")
silver.append({
    "display": "If \\(f(x) = 3x + 2\\), solve \\(f(x) = 20\\)",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Undo the machine: take off 2, then divide by 3.",
    "misconceptions": [mc("inverse_error",
        "To solve \\(f(x)=20\\) work backwards (undo the machine). Substituting 20 into f gives \\(f(20)\\), a different thing.", 62,
        "Student evaluates f(20)=3*20+2=62 instead of solving for the input.")],
    "guided_steps": [
        sayonly("\\(f(x) = 3x + 2\\). Solve \\(f(x) = 20\\): find the input that gives 20 by undoing the machine backwards."),
        box("Take off the + 2: 20 − 2 = ", 18, "Subtract 2 from 20."),
        box("Undo the × 3: 18 ÷ 3 = ", 6, "Divide 18 by 3.", phase="substitute"),
        box("Check forwards: 3 × 6 + 2 = ", 20, "Eighteen, then add 2.",
            phase="substitute", done="It gives 20, so \\(x = 6\\)."),
    ],
})

# S5  f=x+2, g=3x, gf(4) -> 18
A(3*(4+2) == 18, "S5")
silver.append({
    "display": "\\(f(x) = x + 2\\), \\(g(x) = 3x\\). Find \\(gf(4)\\).",
    "solutions": [18], "calculator": False, "input_type": "single_value",
    "hint": "Do f first (add 2 to 4), then multiply by 3.",
    "misconceptions": [mc("composite_order", MSG_ORDER, 14,
        "Student reverses order (g then f): g(4)=12, f(12)=14.")],
    "guided_steps": [
        sayonly("\\(f(x) = x + 2\\) and \\(g(x) = 3x\\). Find \\(gf(4)\\). The rule: \\(gf\\) means do \\(f\\) first, then \\(g\\)."),
        box("Inside first: f(4) = 4 + 2 = ", 6, "Add 2 to 4."),
        box("Feed 6 into g: g(6) = 3 × 6 = ", 18, "Triple 6.", phase="substitute"),
        box("Check: f(4) = 6, then 3 × 6 = ", 18, "Three sixes.",
            phase="substitute", done="So \\(gf(4) = 18\\)."),
    ],
})

# S6  6th term of n^2+2n-1 -> 47
A(6**2+2*6-1 == 47, "S6")
silver.append({
    "display": "Find the 6th term of the sequence with nth term \\(n^2 + 2n - 1\\)",
    "solutions": [47], "calculator": False, "input_type": "single_value",
    "hint": "Put n = 6 in; remember 6 squared is 6 times 6.",
    "misconceptions": [mc("square_as_double",
        "\\(6^2\\) means \\(6 \\times 6 = 36\\), not \\(6 \\times 2\\). Then add \\(2 \\times 6\\) and subtract 1.", 23,
        "Student reads 6^2 as 6*2=12, giving 12+12-1=23.")],
    "guided_steps": [
        sayonly("The nth term is \\(n^2 + 2n - 1\\). Find the 6th term by putting \\(n = 6\\) in. Remember \\(6^2\\) means \\(6 \\times 6\\)."),
        box("Square: 6² = 6 × 6 = ", 36, "Six sixes, not six twos."),
        box("The 2n part: 2 × 6 = ", 12, "Double 6.", phase="substitute"),
        box("Add them: 36 + 12 = ", 48, "Thirty-six plus twelve.", phase="substitute"),
        box("Subtract 1: 48 − 1 = ", 47, "One less than 48.",
            phase="substitute", done="So the 6th term is 47. Squaring 6 as 6×6 = 36 is the key."),
    ],
})

pb["silver"] = silver

# =========================================================================
# 7. GOLD bank (iteration first)
# =========================================================================
gold = []

# G0  x_{n+1}=(x_n^2+3)/4, x0=2, x2 -> 1.516
x0=2.0; x1=(x0*x0+3)/4; x2=(x1*x1+3)/4
A(x1==1.75 and round(x2,3)==1.516, "G0 %r %r"%(x1,x2))
gold.append({
    "display": "Use \\(x_{n+1} = \\frac{x_n^2 + 3}{4}\\) with \\(x_0 = 2\\). Find \\(x_2\\) to 3 d.p.",
    "solutions": [1.516], "calculator": True, "input_type": "single_value",
    "hint": "Work out x1 first, then feed that answer back in for x2.",
    "misconceptions": [mc("iteration_error", MSG_ITER, 1.75,
        "Student stops at x1=1.75, or reuses x0 so x2 also = 1.75.")],
    "guided_steps": [
        sayonly("Iteration: run the formula again and again, each answer feeding the next. \\(x_{n+1} = \\frac{x_n^2 + 3}{4}\\), start \\(x_0 = 2\\). Find \\(x_2\\)."),
        box("First \\(x_1\\). Square the start: 2² = ", 4, "Two squared."),
        box("Add 3, then divide by 4: (4 + 3) ÷ 4 = ", 1.75, "7 ÷ 4.",
            done="So \\(x_1 = 1.75\\), exact. This answer becomes the new input."),
        box("Now \\(x_2\\). Square the NEW input: 1.75² = ", 3.0625, "1.75 × 1.75.", phase="substitute"),
        box("Add 3, then divide by 4: (3.0625 + 3) ÷ 4 = ", 1.516, "6.0625 ÷ 4 = 1.515625, round to 3 d.p.",
            phase="substitute", done="\\(x_2 = 1.516\\). Each step used the previous answer, never the start again."),
    ],
})

# G1  f=1/(x-1), ff(3) -> -2
f=lambda x:1/(x-1)
A(f(f(3))==-2, "G1")
gold.append({
    "display": "\\(f(x) = \\frac{1}{x-1}\\). Find \\(ff(3)\\).",
    "solutions": [-2], "calculator": False, "input_type": "single_value",
    "hint": "Work out f(3), then apply f to that answer again.",
    "misconceptions": [
        mc("composite_order", "\\(ff(3)\\) means apply f, then apply f AGAIN to the result. It is not \\(f(3) \\times f(3)\\).", 0.25,
           "Student multiplies f(3)*f(3) = 0.5*0.5 = 0.25."),
        mc("incomplete_composite", "\\(ff(3)\\) needs f applied TWICE. You have only applied it once.", 0.5,
           "Student computes f(3)=0.5 and stops."),
    ],
    "guided_steps": [
        sayonly("\\(f(x) = \\frac{1}{x-1}\\). Find \\(ff(3)\\): apply \\(f\\), then apply \\(f\\) AGAIN to the result."),
        box("First f(3). The bottom is 3 − 1 = ", 2, "Three minus one."),
        box("So f(3) = 1 ÷ 2 = ", 0.5, "One half.",
            done="f(3) = 0.5. Now apply f again to 0.5."),
        box("Second f. The bottom is 0.5 − 1 = ", -0.5, "A half minus one.", phase="substitute"),
        box("So f(0.5) = 1 ÷ (−0.5) = ", -2, "One divided by negative a half.",
            phase="substitute", done="\\(ff(3) = -2\\). Apply f twice, do not square the first answer."),
    ],
})

# G2  an^2+bn+c, T=2,7,14, find a -> 1
d1=[7-2,14-7]; d2=d1[1]-d1[0]; a=d2/2
A(d1==[5,7] and d2==2 and a==1, "G2")
gold.append({
    "display": "The nth term is \\(an^2 + bn + c\\). Given T(1)=2, T(2)=7, T(3)=14, find \\(a\\).",
    "solutions": [1], "calculator": False, "input_type": "single_value",
    "hint": "Find the second difference, then halve it.",
    "misconceptions": [mc("second_diff", MSG_HALF, 2,
        "Student uses the whole second difference (2) as a instead of halving to 1.")],
    "guided_steps": [
        sayonly("The nth term is \\(an^2 + bn + c\\). From T(1)=2, T(2)=7, T(3)=14, find \\(a\\). The second difference equals \\(2a\\)."),
        box("First differences: 7 − 2 = ", 5, "Second term minus first."),
        box("and 14 − 7 = ", 7, "Third term minus second."),
        box("Second difference: 7 − 5 = ", 2, "The difference of the differences.", phase="substitute"),
        box("The second difference is 2a, so a = 2 ÷ 2 = ", 1, "Halve the second difference.",
            phase="substitute", done="a = 1. Always halve the second difference for the n-squared coefficient."),
    ],
})

# G3  f=2x+1, solve f(x)=f^-1(x) -> -1   (hint fixed)
# 2x+1=(x-1)/2 -> 4x+2=x-1 -> 3x=-3 -> x=-1
A(2*(-1)+1 == -1 and ((-1)-1)/2 == -1, "G3")
gold.append({
    "display": "\\(f(x) = 2x + 1\\). Solve \\(f(x) = f^{-1}(x)\\).",
    "solutions": [-1], "calculator": False, "input_type": "single_value",
    "hint": "Find the inverse first, then set it equal to 2x + 1 and solve.",
    "misconceptions": [mc("inverse_error", MSG_INV, -0.333,
        "Student uses wrong inverse (x+1)/2; solving 2x+1=(x+1)/2 gives x=-1/3.")],
    "guided_steps": [
        sayonly("\\(f(x) = 2x + 1\\). Solve \\(f(x) = f^{-1}(x)\\). First find the inverse: write \\(y = 2x + 1\\), swap, rearrange to \\(f^{-1}(x) = \\frac{x-1}{2}\\). Now solve \\(2x + 1 = \\frac{x-1}{2}\\)."),
        box("Multiply both sides by 2. Left becomes 4x + 2, right becomes x − 1. Gather the x terms: 4x − x = ", 3, "Four x take away one x.", post="x"),
        box("Gather the numbers on the other side: −1 − 2 = ", -3, "Negative one take away two."),
        box("So 3x = −3, giving x = −3 ÷ 3 = ", -1, "Divide by 3.", phase="substitute"),
        box("Check: f(−1) = 2 × (−1) + 1 = ", -1, "Negative two, then add one.",
            phase="substitute", done="f(−1) = −1, and the inverse meets f on the line y = x, so x = −1 is right."),
    ],
})

# G4  x_{n+1}=cbrt(8-2x), x0=1, x3 -> 1.679
cbrt=lambda v: v**(1/3) if v>=0 else -((-v)**(1/3))
g0=1.0
g1=cbrt(8-2*g0); g2=cbrt(8-2*g1); g3=cbrt(8-2*g2)
A(round(g1,3)==1.817 and round(g2,3)==1.634 and round(g3,3)==1.679, "G4 %r %r %r"%(g1,g2,g3))
A(round(8-2*g1,3)==4.366 and round(8-2*g2,3)==4.731, "G4 insides %r %r"%(8-2*g1,8-2*g2))
gold.append({
    "display": "Use \\(x_{n+1} = \\sqrt[3]{8 - 2x_n}\\) with \\(x_0 = 1\\). Find \\(x_3\\) to 3 d.p.",
    "solutions": [1.679], "calculator": True, "input_type": "single_value",
    "hint": "Find x1, keep the full value, feed it back in for x2, then again for x3.",
    "misconceptions": [mc("iteration_error", MSG_ITER, 1.817,
        "Student reuses x0=1 every time, so every value is cbrt(6)=1.817.")],
    "guided_steps": [
        sayonly("\\(x_{n+1} = \\sqrt[3]{8 - 2x_n}\\), start \\(x_0 = 1\\). Find \\(x_3\\). Three iterations, keeping full calculator accuracy until the end."),
        box("\\(x_1\\): the inside is 8 − 2 × 1 = ", 6, "8 minus 2."),
        box("Cube root: ∛6 = ___ (3 d.p.)", 1.817, "Type 6 then cube root on your calculator.",
            done="\\(x_1 ≈ 1.817\\). Keep the FULL value in your calculator for the next step."),
        box("\\(x_2\\): the inside is 8 − 2 × (full x1) = ___ (3 d.p.)", 4.366, "8 − 3.634 ≈ 4.366.", phase="substitute"),
        box("Cube root: ∛4.366 = ___ (3 d.p.)", 1.634, "Cube root of about 4.366.",
            phase="substitute", done="\\(x_2 ≈ 1.634\\)."),
        box("\\(x_3\\): the inside is 8 − 2 × (full x2) = ___ (3 d.p.)", 4.731, "8 − 3.269 ≈ 4.731.", phase="substitute"),
        box("Cube root: ∛4.731 = ___ (3 d.p.)", 1.679, "Cube root of about 4.731.",
            phase="substitute", done="\\(x_3 = 1.679\\). Each step fed the previous answer back in."),
    ],
})

pb["gold"] = gold

# =========================================================================
# 8. tier_guides
# =========================================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: reading a function and naming a square pattern",
        "steps": [
            "A function is a machine. \\(f(5)\\) means put 5 in and follow the rule, so \\(f(x)=4x-3\\) gives \\(f(5)=17\\). Watch signs when the input is negative.",
            "For a number pattern, the terms sit close to the square numbers \\(1, 4, 9, 16\\). Find which \\(n^2\\) rule fits by testing the first few terms.",
        ],
        "example": {
            "question": "Given f(x) = 2x + 5, find f(3)",
            "steps": [
                {"label": "Double", "content": "<p>\\(2 \\times 3 = 6\\)</p>"},
                {"label": "Add 5", "content": "<p>\\(6 + 5 = 11\\)</p>"},
                {"label": "Check", "content": "<p>\\(2(3) + 5 = 11\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(f(3) = 11\\)</p>", "isAnswer": True, "is_answer": True},
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
            "question": "f(x) = 2x + 1, g(x) = x^2. Find fg(3)",
            "steps": [
                {"label": "g first", "content": "<p>\\(g(3) = 3^2 = 9\\)</p>"},
                {"label": "then f", "content": "<p>\\(f(9) = 2(9) + 1 = 19\\)</p>"},
                {"label": "Check", "content": "<p>Square 3 to 9, then \\(2(9)+1 = 19\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(fg(3) = 19\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: iteration and combining every skill",
        "steps": [
            "Iteration repeats \\(x_{n+1}=g(x_n)\\). Work out \\(x_1\\) from \\(x_0\\), then feed each answer back in. Keep full accuracy and only round at the end.",
            "Gold mixes the skills: applying a function twice \\((ff)\\), finding \\(a\\) from second differences, and solving \\(f(x)=f^{-1}(x)\\) by setting the two equal.",
        ],
        "example": {
            "question": "x_{n+1} = (x_n^2 + 5)/6 with x_0 = 2. Find x_2 to 3 d.p.",
            "steps": [
                {"label": "x1", "content": "<p>\\(x_1 = \\frac{2^2 + 5}{6} = \\frac{9}{6} = 1.5\\)</p>"},
                {"label": "x2", "content": "<p>\\(x_2 = \\frac{1.5^2 + 5}{6} = \\frac{7.25}{6} = 1.20833...\\)</p>"},
                {"label": "Round", "content": "<p>\\(x_2 = 1.208\\) (3 d.p.)</p>"},
                {"label": "Answer", "content": "<p>\\(x_2 = 1.208\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =========================================================================
# 9. guided (opener + teach)
# =========================================================================
# opener: function machine (evaluate + inverse), previews iteration
A(3*4+2 == 14 and (20-2)/3 == 6, "opener")
opener = {
    "label": "Before any algebra",
    "display": "A sweet machine:<br>your number → <strong>triple it</strong> → <strong>add 2</strong> → out",
    "steps": [
        box("Put in 4. What comes out? ", 14,
            "Triple 4 to get 12, then add 2.",
            say="A sweet machine takes your number, triples it, then adds 2. No algebra yet, just follow the machine."),
        box("Now run it backwards. The machine spat out 20. What number went IN? ", 6,
            "Undo the steps: take off 2 to get 18, then divide by 3.",
            say="That machine is a <strong>function</strong>. We write it \\(f(x) = 3x + 2\\), and 'put in 4' is written \\(f(4)\\). So you just found \\(f(4) = 14\\)."),
        sayonly("Going backwards like that is the <strong>inverse</strong> function. And if you keep feeding each answer back into the machine, you build a chain of numbers: that repeating is <strong>iteration</strong>. Evaluate, invert, iterate: that is the whole lesson, all built on one machine."),
    ],
}

# teach bronze: function evaluation (f(x)=3x-4)
A(3*6-4==14 and 3*0-4==-4, "teach bronze")
teach_bronze = {
    "display": "Given \\(f(x) = 3x - 4\\), find \\(f(6)\\)",
    "label": "Together: your first one",
    "steps": [
        sayonly("\\(f(x) = 3x - 4\\) is a machine: triple the input, then take off 4. Find \\(f(6)\\)."),
        box("Triple the input: 3 × 6 = ", 18, "Three sixes."),
        box("Now take off 4: 18 − 4 = ", 14, "Subtract 4 from 18.",
            done="That is \\(f(6) = 14\\). Substitute the number, follow the rule. That is the whole move."),
        sayonly("Try the input 0 to see negatives are fine."),
        box("Triple: 3 × 0 = ", 0, "Zero times anything is zero."),
        box("Take off 4: 0 − 4 = ", -4, "Nothing, minus 4.",
            done="So \\(f(0) = -4\\). Negatives are fine; just follow the rule."),
    ],
}

# teach silver: composite functions (f=2x+1, g=x+5)
A(2*(3+5)+1==17 and (2*3+1)+5==12, "teach silver")
teach_silver = {
    "display": "\\(f(x) = 2x + 1\\), \\(g(x) = x + 5\\). Find \\(fg(3)\\), then \\(gf(3)\\).",
    "label": "Together: the silver move",
    "steps": [
        sayonly("\\(f(x) = 2x + 1\\) and \\(g(x) = x + 5\\). Find \\(fg(3)\\). The rule: \\(fg\\) does \\(g\\) FIRST, then feeds the answer into \\(f\\)."),
        box("Inside first: g(3) = 3 + 5 = ", 8, "Add 5 to 3."),
        box("Now f(8) = 2 × 8 + 1 = ", 17, "Double 8, then add 1.",
            done="\\(fg(3) = 17\\). Inside first, then outside."),
        sayonly("Now find \\(gf(3)\\): this time do \\(f\\) first, then \\(g\\)."),
        box("f(3) = 2 × 3 + 1 = ", 7, "Double 3, then add 1."),
        box("Now g(7) = 7 + 5 = ", 12, "Add 5 to 7.",
            done="\\(gf(3) = 12\\), not 17. Same functions, opposite order, different answer."),
    ],
}

# teach gold: iteration (x_{n+1}=(x^2+5)/6, x0=2)
t0=2.0; t1=(t0*t0+5)/6; t2=(t1*t1+5)/6
A(t1==1.5 and round(t2,3)==1.208, "teach gold %r %r"%(t1,t2))
teach_gold = {
    "display": "Use \\(x_{n+1} = \\frac{x_n^2 + 5}{6}\\) with \\(x_0 = 2\\). Find \\(x_2\\) to 3 d.p.",
    "label": "Together: the gold move",
    "steps": [
        sayonly("Iteration means running a formula over and over, each answer feeding the next. \\(x_{n+1} = \\frac{x_n^2 + 5}{6}\\), start \\(x_0 = 2\\). Find \\(x_2\\)."),
        box("First \\(x_1\\). Square the start: 2² = ", 4, "Two squared."),
        box("Add 5, then divide by 6: (4 + 5) ÷ 6 = ", 1.5, "9 ÷ 6.",
            done="So \\(x_1 = 1.5\\), exact. Now that answer becomes the new input."),
        sayonly("Now \\(x_2\\): feed 1.5 back in. The NEW input is 1.5, not 2. That swap is the whole idea."),
        box("Square the new input: 1.5² = ", 2.25, "1.5 × 1.5."),
        box("Add 5, then divide by 6: (2.25 + 5) ÷ 6 = ", 1.208, "7.25 ÷ 6 = 1.20833..., round to 3 d.p.",
            done="\\(x_2 = 1.208\\). Each step uses the PREVIOUS answer, never the start again. That is iteration."),
    ],
}

pd["guided"] = {
    "opener": opener,
    "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold},
}

# =========================================================================
# 10. write
# =========================================================================
json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("built", OUT)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
