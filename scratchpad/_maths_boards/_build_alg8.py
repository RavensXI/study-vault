# -*- coding: utf-8 -*-
"""Build guided-learning + figures practice_data for maths-aqa algebra-L08
   (Quadratic Formula & Completing the Square). Everything computed & asserted."""
import json, io, math

live = json.load(io.open("_live_alg8.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

# ---------------------------------------------------------------- OPENER SVG
OPENER_SVG = (
 '<svg viewBox="0 0 250 205" role="img" aria-label="A large square split into an '
 'x by x square, two strips, and a small corner square" style="max-width:250px">'
 '<rect x="45" y="12" width="120" height="120" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor"/>'
 '<rect x="165" y="12" width="40" height="120" fill="#34d399" fill-opacity="0.3" stroke="currentColor"/>'
 '<rect x="45" y="132" width="120" height="40" fill="#34d399" fill-opacity="0.3" stroke="currentColor"/>'
 '<rect x="165" y="132" width="40" height="40" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor"/>'
 '<text x="105" y="8" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">x</text>'
 '<text x="185" y="8" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">?</text>'
 '<text x="38" y="76" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">x</text>'
 '<text x="38" y="156" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">?</text>'
 '<text x="105" y="78" font-family="Inter" font-size="12" fill="currentColor" text-anchor="middle">x²</text>'
 '<text x="185" y="78" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">strip</text>'
 '<text x="105" y="156" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">strip</text>'
 '<text x="185" y="156" font-family="Inter" font-size="11" fill="currentColor" text-anchor="middle">?</text>'
 '</svg>'
)

opener = {
 "display": (OPENER_SVG +
  "You have a square tile, x by x. Someone gives you 6 thin strips, each x long, "
  "and asks you to build ONE bigger square using the tile and the strips."),
 "steps": [
   sayonly("To make a bigger square you must add the same amount along two touching "
           "sides, the right and the bottom. So share the 6 strips equally between them."),
   box("6 strips shared equally between 2 sides means each side gets ", 3,
       "Half of 6.", post=" strips"),
   sayonly("Now the big square has side (x + 3), but its bottom-right corner is still "
           "a hole. You fill it with one small square, 3 by 3."),
   box("Area of that little corner square, 3 × 3 = ", 9,
       "Three times three."),
   sayonly("So the tile plus 6 strips, that is \\(x^2 + 6x\\), makes an \\((x+3)^2\\) "
           "square with a 9 hole you had to fill in. In symbols: "
           "\\(x^2 + 6x = (x+3)^2 - 9\\). Halving the 6, then taking off the square of "
           "that half, <strong>is</strong> completing the square.")
 ]
}

# ---------------------------------------------------------------- TEACH WALKS
teach_bronze = {
 "display": "For \\(x^2 + 8x + 1 = 0\\), find the discriminant, then say how many real roots it has.",
 "steps": [
   sayonly("The discriminant is \\(b^2 - 4ac\\). Read off a = 1, b = 8, c = 1."),
   box("b squared: 8 × 8 = ", 64, "Eight times eight."),
   box("4ac: 4 × 1 × 1 = ", 4, "Multiply all three together."),
   box("discriminant: 64 − 4 = ", 60, "Subtract the second from the first."),
   box("60 is positive, so the number of real roots is ", 2,
       "Positive discriminant means two real roots.",
       done="Positive discriminant, two roots. That is the whole point.")
 ]
}
teach_silver = {
 "display": "Solve \\(x^2 + 5x + 2 = 0\\) with the quadratic formula. Give both roots to 2 d.p.",
 "steps": [
   sayonly("Here a = 1, b = 5, c = 2, so \\(x = \\frac{-5 \\pm \\sqrt{5^2 - 4(1)(2)}}{2}\\)."),
   box("4ac: 4 × 1 × 2 = ", 8, "Multiply all three."),
   box("discriminant: 25 − 8 = ", 17, "b squared minus 4ac."),
   box("square root of 17, to 2 d.p. = ", 4.12, "Use a calculator."),
   box("larger root: (−5 + 4.12) ÷ 2 = ", -0.44, "Use the plus, then divide by 2a = 2."),
   box("smaller root: (−5 − 4.12) ÷ 2 = ", -4.56, "Use the minus, then divide by 2.",
       done="Two roots from one formula. The ± did the work.")
 ]
}
teach_gold = {
 "display": "Write \\(3x^2 + 12x + 5\\) in the form \\(a(x + p)^2 + q\\).",
 "steps": [
   sayonly("The a here is 3. Factor it out of the first two terms: \\(3(x^2 + 4x) + 5\\)."),
   box("coefficient of x inside the bracket = ", 4, "It is the number in front of x once 3 is taken out."),
   box("halve it to get p: 4 ÷ 2 = ", 2, "Half of four."),
   box("the 2 outside multiplies the correction 2²: 3 × 4 = ", 12, "Three times two-squared."),
   box("q = −12 + 5 = ", -7, "Subtract the correction, then add the original constant."),
   box("check by expanding: 3 × 2² + q = 12 + (−7) = ", 5,
       "It should return the original constant, 5.",
       done="Back to +5, so 3(x+2)² − 7 is right.")
 ]
}

# ---------------------------------------------------------------- BANK WALKS
# helper builders per archetype -------------------------------------------------
def walk_discriminant(a, b, c, astr, bstr, cstr, final_is_disc=True):
    b2 = b*b
    fourac = 4*a*c
    disc = b2 - fourac
    steps = [
      sayonly("The discriminant is \\(b^2 - 4ac\\). Read off a = %s, b = %s, c = %s." % (astr, bstr, cstr)),
      box("b squared: %s = " % _sq(bstr, b), b2, "Square the number in front of x, sign and all."),
      box("4ac: 4 × %s × %s = " % (astr, cstr), fourac, "Multiply four, a and c, keeping signs.", phase="substitute"),
      box("discriminant: %d − (%d) = " % (b2, fourac) if fourac < 0 else "discriminant: %d − %d = " % (b2, fourac),
          disc, "Take 4ac away from b squared.", phase="substitute",
          done=("Positive, so two real roots." if disc>0 else ("Zero, so one repeated root." if disc==0 else "Negative, so no real roots."))),
    ]
    assert disc == b2 - fourac
    return steps, disc

def _sq(s, v):
    return "(%s)²" % s if v < 0 else "%s²" % s

def walk_nroots(a, b, c, astr, bstr, cstr, count):
    b2=b*b; fourac=4*a*c; disc=b2-fourac
    if disc>0: assert count==2
    elif disc==0: assert count==1
    else: assert count==0
    reason = ("positive, so " if disc>0 else ("zero, so " if disc==0 else "negative, so "))
    steps=[
      sayonly("Number of roots comes from the discriminant \\(b^2 - 4ac\\). Read a = %s, b = %s, c = %s." % (astr,bstr,cstr)),
      box("b squared: %s = " % _sq(bstr,b), b2, "Square the coefficient of x."),
      box("4ac: 4 × %s × %s = " % (astr,cstr), fourac, "Multiply four, a and c.", phase="substitute"),
      box(("discriminant: %d − (%d) = " % (b2,fourac)) if fourac<0 else ("discriminant: %d − %d = " % (b2,fourac)),
          disc, "b squared minus 4ac.", phase="substitute"),
      box("the discriminant is %s the number of real roots is " % reason, count,
          "Positive gives 2, zero gives 1, negative gives 0.",
          phase="substitute", done="Read straight from the sign of the discriminant."),
    ]
    return steps, count

def walk_cts_x2(bcoef, ask):   # x^2 + bcoef x  -> (x+a)^2 + b ; ask 'a' or 'b'
    half = bcoef//2
    assert half*2==bcoef
    corr = -half*half
    steps=[
      sayonly("Complete the square on \\(x^2 %+d x\\). Halve the coefficient of x." % bcoef),
      box("half of %d = " % bcoef, half, "Divide the number in front of x by 2."),
      box("square that half: %s = " % _sq(str(half), half), half*half, "Multiply the half by itself.", phase="substitute"),
    ]
    if ask=="a":
      steps.append(box("so \\(x^2 %+d x = (x %+d)^2 %+d\\); the value of a is " % (bcoef, half, corr), half,
          "a is the half you found.", phase="substitute",
          done="Expand (x%+d)² to check: it gives x² %+d x %+d, then %+d cancels back to x² %+d x." % (half, bcoef, half*half, corr, bcoef)))
      return steps, half
    else:
      steps.append(box("the constant added on is minus that square: 0 − %d = " % (half*half), corr,
          "It is negative, the square subtracted.", phase="substitute",
          done="So x²%+dx = (x%+d)² %+d." % (bcoef, half, corr)))
      return steps, corr

def walk_cts_full(bcoef, const, ask, pval, qval):  # x^2 + bcoef x + const -> (x+p)^2 + q
    half=bcoef//2; assert half*2==bcoef
    sq=half*half
    q=const-sq
    assert half==pval and q==qval
    steps=[
      sayonly("Complete the square on \\(x^2 %+d x %+d\\). Halve the coefficient of x." % (bcoef, const)),
      box("half of %d = " % bcoef, half, "Divide the coefficient of x by 2."),
      box("square it: %s = " % _sq(str(half),half), sq, "The half times itself.", phase="substitute"),
    ]
    if ask=="p":
      steps.append(box("in \\((x + p)^2 + q\\), p is that half, so p = ", half,
        "p is the half, sign included.", phase="substitute",
        done="(x%+d)² %+d rebuilds x²%+dx%+d." % (half, q, bcoef, const)))
      return steps, half
    else:
      steps.append(box("adjust the constant: %d − %d = " % (const, sq), q,
        "Original constant minus the square.", phase="substitute",
        done="So the form is (x%+d)² %+d." % (half, q)))
      return steps, q

def walk_formula(a,b,c,astr,bstr,cstr, want, target):  # 'pos' or 'larger'
    b2=b*b; fourac=4*a*c; disc=b2-fourac
    root=round(math.sqrt(disc),2)
    twoa=2*a
    val=round((-b+root)/twoa,2)
    assert abs(val-target)<0.005, (val,target)
    steps=[
      sayonly("Use \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) with a = %s, b = %s, c = %s." % (astr,bstr,cstr)),
      box("4ac: 4 × %s × %s = " % (astr,cstr), fourac, "Multiply four, a and c, keeping signs."),
      box(("discriminant: %d − (%d) = " % (b2,fourac)) if fourac<0 else ("discriminant: %d − %d = " % (b2,fourac)),
          disc, "b squared minus 4ac.", phase="substitute"),
      box("square root of %d, to 2 d.p. = " % disc, root, "Use a calculator.", phase="substitute"),
      box("%s root: (%d %s %.2f) ÷ %d = " % ("larger" if want=="larger" else "positive", -b, "+", root, twoa),
          val, "Take the + option on top, then divide by 2a = %d." % twoa, phase="substitute",
          done="Substitute back to check it satisfies the equation."),
    ]
    return steps, val

# ---- BRONZE ----
b0_steps,_ = walk_discriminant(1,5,3,"1","5","3")            # 13
b1_steps,_ = walk_discriminant(2,-3,-1,"2","−3","−1")        # 17
b2_steps,_ = walk_nroots(1,4,5,"1","4","5",0)               # 0
b3_steps,_ = walk_cts_x2(6,"a")                             # 3
b4_steps,_ = walk_cts_x2(6,"b")                             # -9
b5_steps,_ = walk_discriminant(1,4,1,"1","4","1")           # 12
b6_steps,_ = walk_nroots(1,-6,9,"1","−6","9",1)             # 1
b7_steps,_ = walk_cts_full(10,30,"q",5,5)                   # 5

# ---- SILVER ----
s0_steps,_ = walk_formula(1,3,-7,"1","3","−7","pos",1.54)   # 1.54
s1_steps,_ = walk_formula(2,-5,1,"2","−5","1","larger",2.28)# 2.28
s2_steps,_ = walk_formula(3,2,-4,"3","2","−4","pos",0.87)   # 0.87
s3_steps,_ = walk_cts_full(-4,7,"p",-2,3)                   # -2
s4_steps,_ = walk_cts_full(-4,7,"q",-2,3)                   # 3
s5_steps,_ = walk_discriminant(1,2,5,"1","2","5")           # -16
# s6 turning point of y=(x-4)^2+5
s6_steps = [
  sayonly("A turning point sits where the squared bracket is smallest, which is zero."),
  box("(x − 4)² is zero when x − 4 = 0, so x = ", 4, "What makes the bracket zero?"),
  box("check the height there: (4 − 4)² + 5 = 0 + 5 = ", 5, "Put x = 4 back in.", phase="substitute"),
  box("so the x-coordinate of the turning point is ", 4, "It is where the bracket vanished.",
      phase="substitute", done="Turning point (4, 5); its x-coordinate is 4."),
]

# ---- GOLD ----
# g0: x^2+6x+2=0 -> -3+sqrt(k), k=7
g0_steps = [
  sayonly("Solve by completing the square. Halve the 6 to get 3, giving \\((x+3)^2\\)."),
  box("the correction to subtract is 3² = ", 9, "Square the half."),
  box("constant after completing: −9 + 2 = ", -7, "Take off 9, add the original 2.", phase="substitute"),
  box("so (x+3)² = 7, and comparing with −3 + √k gives k = ", 7,
      "The number left on the right.", phase="substitute",
      done="x = −3 ± √7, so the positive root is −3 + √7 and k = 7."),
]
# g1: 2x^2+8x+3 -> a(x+p)^2+q, q=-5
g1_steps = [
  sayonly("Factor the 2 from the first two terms: \\(2(x^2 + 4x) + 3\\)."),
  box("half of the 4 inside is ", 2, "Half of four."),
  box("the 2 outside times that square: 2 × 2² = ", 8, "Two times two-squared.", phase="substitute"),
  box("q = −8 + 3 = ", -5, "Subtract the 8, add the 3.", phase="substitute",
      done="So 2(x+2)² − 5; q = −5."),
]
# g2: kx^2+6x+k=0 equal roots, positive k=3
g2_steps = [
  sayonly("Equal roots means the discriminant is 0. Here a = k, b = 6, c = k."),
  box("b squared: 6² = ", 36, "Six squared."),
  box("4ac = 4·k·k = 4k². Set 36 − 4k² = 0, so 4k² = ", 36, "Move it across.", phase="substitute"),
  box("k² = 36 ÷ 4 = ", 9, "Divide by four.", phase="substitute"),
  box("positive k = √9 = ", 3, "Square root, take the positive value.",
      phase="substitute", done="k = 3 (and −3); the positive value is 3."),
]
# g3: 5x^2-2x-1=0 positive root 0.69
g3_steps,_ = walk_formula(5,-2,-1,"5","−2","−1","pos",0.69)
# g4: min of x^2-8x+20 = 4
g4_steps = [
  sayonly("The minimum of a quadratic is the constant after completing the square. Halve −8."),
  box("half of −8 = ", -4, "Divide by two, keep the sign."),
  box("square it: (−4)² = ", 16, "Minus four squared.", phase="substitute"),
  box("minimum value = 20 − 16 = ", 4, "Original constant minus the square.",
      phase="substitute", done="(x−4)² + 4, so the least value is 4, reached at x = 4."),
]

# ---------------------------------------------------------------- MISCONCEPTIONS
def mc(pattern, message, expect):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

# ---------------------------------------------------------------- ASSEMBLE BANK
pb = live["problem_bank"]

def setp(tier, idx, **kw):
    pb[tier][idx].update(kw)

# BRONZE ------------------------------------------------------------
setp("bronze",0, hint="Read off a, b, c then work out b² − 4ac.", guided_steps=b0_steps,
  misconceptions=[mc("added_4ac","The discriminant subtracts 4ac: 25 − 12 = 13. Adding it gives 37, which counts 4ac the wrong way.",37)])
# bronze[1] REPAIR: 2x^2 - 3x + 1 (disc 1, dup) -> 2x^2 - 3x - 1 (disc 17)
setp("bronze",1, display="For \\(2x^2 - 3x - 1 = 0\\), what is the discriminant?", solutions=[17],
  hint="Here c is negative, so 4ac is negative; subtracting it adds on.", guided_steps=b1_steps,
  misconceptions=[mc("dropped_c_sign","c is −1, so 4ac = 4×2×(−1) = −8, and 9 − (−8) = 17. Treating 4ac as +8 gives 1.",1)])
setp("bronze",2, hint="Work out the discriminant; its sign tells you the count.", guided_steps=b2_steps,
  misconceptions=[mc("always_two","The discriminant is 16 − 20 = −4, negative, so there are no real solutions. A quadratic does not always have two.",2)])
setp("bronze",3, hint="Halve the coefficient of x to find a.", guided_steps=b3_steps,
  misconceptions=[mc("forgot_halve","Halve the 6 first: a = 6 ÷ 2 = 3, not 6.",6)])
setp("bronze",4, hint="After halving and squaring, the constant is subtracted.", guided_steps=b4_steps,
  misconceptions=[mc("kept_positive","The square is taken off: b = −3² = −9. Leaving it positive gives 9.",9),
                  mc("subtracted_half","Subtract the square of the half, not the half: −(3²) = −9, not −3.",-3)])
setp("bronze",5, hint="The discriminant is b² − 4ac = 16 − 4.", guided_steps=b5_steps,
  misconceptions=[mc("added_4ac","b² − 4ac = 16 − 4 = 12. Adding gives 20.",20)])
setp("bronze",6, hint="Find the discriminant; zero means a repeated root.", guided_steps=b6_steps,
  misconceptions=[mc("ignored_zero","The discriminant is 36 − 36 = 0, so there is one repeated root, not two.",2)])
setp("bronze",7, hint="Halve the 10, square it, then adjust the 30.", guided_steps=b7_steps,
  misconceptions=[mc("subtracted_half","Take off the square of the half: 30 − 5² = 30 − 25 = 5. Subtracting just 5 gives 25.",25)])

# SILVER ------------------------------------------------------------
setp("silver",0, hint="Use the formula; the positive root uses the + sign.", guided_steps=s0_steps,
  misconceptions=[mc("plus_b","Use −b on top, and here b = 3 so −b = −3: (−3 + 6.08) ÷ 2 = 1.54. Using +3 gives 4.54.",4.54)])
setp("silver",1, hint="Divide the whole top by 2a, and here 2a = 4.", guided_steps=s1_steps,
  misconceptions=[mc("divide_by_two","Divide by 2a = 4, not 2: (5 + 4.12) ÷ 4 = 2.28. Dividing by 2 gives 4.56.",4.56)])
setp("silver",2, hint="Here 2a = 6; divide the whole numerator by it.", guided_steps=s2_steps,
  misconceptions=[mc("divide_by_two","Divide by 2a = 6, not 2: (−2 + 7.21) ÷ 6 = 0.87. Dividing by 2 gives 2.61.",2.61)])
setp("silver",3, hint="p is half the coefficient of x, sign included.", guided_steps=s3_steps,
  misconceptions=[mc("dropped_sign","Half of −4 is −2, so p = −2. The minus carries through.",2)])
setp("silver",4, hint="Square the half, then subtract it from 7.", guided_steps=s4_steps,
  misconceptions=[mc("added_square","Subtract the square: 7 − 4 = 3. Adding it gives 11.",11)])
setp("silver",5, hint="The discriminant is b² − 4ac = 4 − 20.", guided_steps=s5_steps,
  misconceptions=[mc("added_4ac","4 − 20 = −16. Adding gives 24.",24)])
# silver[6] REPAIR: y=(x-3)^2+5 (x=3, dup with silver[4]=3) -> y=(x-4)^2+5 (x=4)
setp("silver",6, display="The turning point of \\(y = (x - 4)^2 + 5\\) has x-coordinate?", solutions=[4],
  hint="The bracket is zero at the turning point; solve x − 4 = 0.", guided_steps=s6_steps,
  misconceptions=[mc("sign_flip","(x − 4)² is zero at x = 4, so the turning point is at x = 4, not −4.",-4)])

# GOLD --------------------------------------------------------------
setp("gold",0, hint="Complete the square, then read off k from (x+3)² = k.", guided_steps=g0_steps,
  misconceptions=[mc("dropped_plus2","After −9 + 2 the constant is −7, so (x+3)² = 7 and k = 7. Ignoring the +2 gives 9.",9)])
setp("gold",1, hint="Factor the 2 out first, then complete the square inside.", guided_steps=g1_steps,
  misconceptions=[mc("forgot_multiply","The −4 inside is multiplied by the 2 outside: 2 × (−4) = −8, then −8 + 3 = −5. Forgetting the ×2 gives −1.",-1)])
setp("gold",2, hint="Equal roots means b² − 4ac = 0; solve for k.", guided_steps=g2_steps,
  misconceptions=[mc("forgot_sqrt","4k² = 36 gives k² = 9, so k = 3 after square-rooting. Stopping at k² = 9 leaves 9.",9)])
setp("gold",3, hint="Use the formula; here 2a = 10.", guided_steps=g3_steps,
  misconceptions=[mc("divide_by_two","Divide by 2a = 10, not 2: (2 + 4.90) ÷ 10 = 0.69. Dividing by 2 gives 3.45.",3.45)])
setp("gold",4, hint="Complete the square; the minimum is the constant left.", guided_steps=g4_steps,
  misconceptions=[mc("used_c","The minimum is 20 − 16 = 4, not the original constant 20.",20)])

# tier descriptions
pb["bronze_description"] = "Read a, b and c, work out the discriminant b² − 4ac, and complete the square on simple x² + bx."
pb["silver_description"] = "Solve with the quadratic formula to 2 d.p., complete the square with a constant, and read turning points."
pb["gold_description"] = "Complete the square when a ≠ 1, use the discriminant as a condition (equal roots), and find minimum values."

# ---------------------------------------------------------------- tier_guides
def exstep(label, content, is_ans=False):
    d={"label":label,"content":content}
    if is_ans: d["isAnswer"]=True; d["is_answer"]=True
    return d

tier_guides = {
 "bronze": {
   "title": "Bronze: a, b, c, the discriminant, and simple squares",
   "steps": [
     "Every quadratic \\(ax^2 + bx + c = 0\\) hands you three numbers: a, b and c. Read them off, keeping every minus sign.",
     "The <strong>discriminant</strong> is \\(b^2 - 4ac\\). Its sign counts the roots: positive gives 2, zero gives 1, negative gives none.",
     "To complete the square on \\(x^2 + bx\\): halve b, then subtract the square of that half. So \\(x^2 + 6x = (x+3)^2 - 9\\)."
   ],
   "example": {
     "question": "For \\(x^2 + 2x - 8 = 0\\), find the discriminant.",
     "steps": [
       exstep("Read off", "a = 1, b = 2, c = −8"),
       exstep("b squared", "\\(2^2 = 4\\)"),
       exstep("4ac", "\\(4 × 1 × (−8) = −32\\)"),
       exstep("Check the subtraction", "\\(4 − (−32) = 4 + 32\\)"),
       exstep("Answer", "Discriminant = 36 (positive, so two roots)", True)
     ]
   }
 },
 "silver": {
   "title": "Silver: the quadratic formula and completed squares",
   "steps": [
     "When a quadratic will not factorise, use \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\). Work out the discriminant, then its square root.",
     "The \\(\\pm\\) gives two answers: + for the larger root, − for the smaller. Divide the whole top by \\(2a\\), not just part of it.",
     "Completing the square \\(x^2 + bx + c = (x + p)^2 + q\\) puts the turning point at \\((-p, q)\\) with no extra work."
   ],
   "example": {
     "question": "Solve \\(x^2 + 4x + 1 = 0\\) to 2 d.p.",
     "steps": [
       exstep("Discriminant", "\\(4^2 - 4(1)(1) = 12\\)"),
       exstep("Square root", "\\(\\sqrt{12} = 3.46\\)"),
       exstep("Check both roots", "\\((-4 ± 3.46) ÷ 2\\)"),
       exstep("Answer", "x = −0.27 or x = −3.73", True)
     ]
   }
 },
 "gold": {
   "title": "Gold: harder squares and the discriminant as a condition",
   "steps": [
     "When \\(a \\neq 1\\), factor a out of the first two terms first: \\(2x^2 + 8x = 2(x^2 + 4x)\\), then complete the square inside.",
     "The discriminant is also a <strong>condition</strong>: equal roots means \\(b^2 - 4ac = 0\\). Set it to zero and solve for the unknown.",
     "The completed form \\(a(x + p)^2 + q\\) gives the minimum value \\(q\\) straight away, reached at \\(x = -p\\)."
   ],
   "example": {
     "question": "Find the minimum value of \\(x^2 - 6x + 11\\).",
     "steps": [
       exstep("Halve the −6", "half is −3, so \\((x - 3)^2\\)"),
       exstep("Adjust", "\\((x-3)^2 - 9 + 11\\)"),
       exstep("Check", "\\(-9 + 11 = 2\\)"),
       exstep("Answer", "Minimum value = 2, at x = 3", True)
     ]
   }
 }
}

# ---------------------------------------------------------------- method_card (slim)
method_card = {
 "title": "Quadratic Formula and Completing the Square",
 "steps": [
   "Read a, b, c from \\(ax^2 + bx + c = 0\\), keeping signs.",
   "Discriminant \\(b^2 - 4ac\\): positive gives 2 roots, zero gives 1, negative gives none.",
   "Formula: \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\), dividing the whole top by 2a.",
   "Completing the square: halve b, subtract its square. Form \\((x+p)^2+q\\) has turning point \\((-p, q)\\)."
 ],
 "content": "<p><strong>Two tools</strong> for quadratics that will not factorise. The <strong>discriminant</strong> \\(b^2 - 4ac\\) tells you how many real roots exist before you solve. The <strong>formula</strong> then finds them. <strong>Completing the square</strong> rewrites \\(x^2 + bx + c\\) as \\((x + p)^2 + q\\), which reveals the turning point and minimum value directly.</p>",
 "example": "<p><strong>Solve</strong> \\(2x^2 + 3x - 5 = 0\\)</p><p>\\(a = 2, b = 3, c = -5\\), so \\(x = \\frac{-3 \\pm \\sqrt{9 + 40}}{4} = \\frac{-3 \\pm 7}{4}\\)</p><p>\\(x = 1\\) or \\(x = -2.5\\)</p>"
}

# ---------------------------------------------------------------- guided block
guided = {
 "opener": opener,
 "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold}
}

# ---------------------------------------------------------------- final object
out = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": pb,
 "related_videos": live.get("related_videos", []),
 "worked_examples": live.get("worked_examples", []),
 "tier_guides": tier_guides,
 "guided": guided
}

# sanity: final boxes land on solutions --------------------------------
def last_box(steps):
    v=None
    for s in steps:
        if s.get("answer") is not None: v=s["answer"]
    return v

checks=[
 ("bronze",0,13),("bronze",1,17),("bronze",2,0),("bronze",3,3),("bronze",4,-9),
 ("bronze",5,12),("bronze",6,1),("bronze",7,5),
 ("silver",0,1.54),("silver",1,2.28),("silver",2,0.87),("silver",3,-2),("silver",4,3),
 ("silver",5,-16),("silver",6,4),
 ("gold",0,7),("gold",1,-5),("gold",2,3),("gold",3,0.69),("gold",4,4),
]
for tier,idx,sol in checks:
    p=pb[tier][idx]
    assert p["solutions"]==[sol], (tier,idx,p["solutions"],sol)
    lb=last_box(p["guided_steps"])
    assert abs(lb-sol)<0.005, ("last box mismatch", tier, idx, lb, sol)
print("all final boxes land on solutions OK")

json.dump(out, io.open("lesson_maths-aqa_algebra-L08.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_algebra-L08.json")
