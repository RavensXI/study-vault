# -*- coding: utf-8 -*-
import json

live = json.load(open(r"_eq_L12_live.json", encoding="utf-8"))

# ---------- SVG generators ----------
def parabola_svg(r1, r2, region, label, aria):
    """region: 'between' (shade below-axis lens) or 'outside' (shade above-axis wings).
    Positive x^2 parabola f(x)=(x-r1)(x-r2). r1<r2."""
    assert r1 < r2
    W, xL, xR = 240, 20, 226
    yTop, yBot = 20.0, 150.0
    pad = (r2 - r1) * 0.6
    xmin, xmax = r1 - pad, r2 + pad
    def fx(x):  # data x -> pixel x
        return xL + (x - xmin) / (xmax - xmin) * (xR - xL)
    def f(x):
        return (x - r1) * (x - r2)
    ymax = max(f(xmin), f(xmax))
    ymin = f((r1 + r2) / 2.0)
    def fy(y):
        return yTop + (ymax - y) / (ymax - ymin) * (yBot - yTop)
    axisY = fy(0.0)
    N = 66
    xs = [xmin + (xmax - xmin) * i / N for i in range(N + 1)]
    curve = [(fx(x), fy(f(x))) for x in xs]
    pts = " ".join("%.2f,%.2f" % p for p in curve)
    px_r1, px_r2 = fx(r1), fx(r2)
    parts = []
    parts.append('<svg viewBox="0 0 240 172" role="img" aria-label="%s" style="max-width:240px;font-family:Inter,sans-serif">' % aria)
    parts.append('<line x1="%d" y1="%.2f" x2="%d" y2="%.2f" stroke="currentColor" stroke-width="1"/>' % (xL, axisY, xR, axisY))
    if region == "between":
        seg = [(fx(x), fy(f(x))) for x in xs if r1 <= x <= r2]
        poly = [(px_r1, axisY)] + seg + [(px_r2, axisY)]
        pp = " ".join("%.2f,%.2f" % p for p in poly)
        parts.append('<polygon points="%s" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>' % pp)
    else:  # outside
        segL = [(fx(x), fy(f(x))) for x in xs if x <= r1]
        polyL = [(fx(xmin), axisY)] + segL + [(px_r1, axisY)]
        segR = [(fx(x), fy(f(x))) for x in xs if x >= r2]
        polyR = [(px_r2, axisY)] + segR + [(fx(xmax), axisY)]
        parts.append('<polygon points="%s" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>' % " ".join("%.2f,%.2f" % p for p in polyL))
        parts.append('<polygon points="%s" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>' % " ".join("%.2f,%.2f" % p for p in polyR))
    parts.append('<polyline points="%s" fill="none" stroke="#60a5fa" stroke-width="1.8"/>' % pts)
    parts.append('<circle cx="%.2f" cy="%.2f" r="2.6" fill="currentColor"/>' % (px_r1, axisY))
    parts.append('<circle cx="%.2f" cy="%.2f" r="2.6" fill="currentColor"/>' % (px_r2, axisY))
    parts.append('<text x="%d" y="%.2f" font-size="9" fill="currentColor" text-anchor="end" opacity="0.7">x</text>' % (xR, axisY - 3))
    parts.append('<text x="120" y="12" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % label)
    parts.append('</svg>')
    return "".join(parts)

def numberline_svg(vmin, vmax, roots_open, roots_closed, dots, aria):
    """roots_open/closed: list of endpoint values. dots: filled solution integers."""
    xL, xR, yA = 20.0, 240.0, 34.0
    def fx(v):
        return xL + (v - vmin) / (vmax - vmin) * (xR - xL)
    parts = ['<svg viewBox="0 0 260 56" role="img" aria-label="%s" style="max-width:280px;width:100%%;height:auto;font-family:Inter,sans-serif">' % aria]
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>' % (xL, yA, xR, yA))
    v = vmin
    while v <= vmax + 1e-9:
        px = fx(v)
        parts.append('<line x1="%.1f" y1="30.0" x2="%.1f" y2="38.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.4"/>' % (px, px))
        parts.append('<text x="%.1f" y="50.0" font-size="10" fill="currentColor" text-anchor="middle">%d</text>' % (px, v))
        v += 1
    lo = min(roots_open + roots_closed)
    hi = max(roots_open + roots_closed)
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#f59e0b" stroke-width="4" stroke-opacity="0.55"/>' % (fx(lo), yA, fx(hi), yA))
    for r in roots_open:
        parts.append('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--sv-bg, #faf8f5)" stroke="#3b82f6" stroke-width="1.5"/>' % (fx(r), yA))
    for r in roots_closed:
        parts.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#3b82f6" stroke="#3b82f6" stroke-width="1.5"/>' % (fx(r), yA))
    for d in dots:
        parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (fx(d), yA))
    parts.append('</svg>')
    return "".join(parts)

CAP = '<span class="figure-caption">Sketch, not drawn to scale</span>'

# ---------- problem bank (preserve displays/options/solutions; add hint + expects) ----------
pb = live["problem_bank"]

def mc(prob, hint, misc):
    prob["hint"] = hint
    prob["misconceptions"] = misc
    return prob

# BRONZE
b = pb["bronze"]
mc(b[0], "The roots are the two numbers that square to give 4, so plus or minus 2. For greater than 0 take outside them.",
   [{"pattern":"wrong_region","expect":1,"message":"For \\(> 0\\) the U-shape is above the axis OUTSIDE the roots \\(\\pm 2\\): \\(x < -2\\) or \\(x > 2\\). Between the roots the curve dips below zero.","note":"inside instead of outside"}])
mc(b[1], "Find the roots (plus or minus 3), then for less than 0 take between them.",
   [{"pattern":"wrong_region","expect":1,"message":"For \\(< 0\\) the curve is below the axis BETWEEN the roots \\(\\pm 3\\): \\(-3 < x < 3\\). Outside the roots the curve is above zero.","note":"outside instead of between"}])
mc(b[2], "Rewrite as x squared minus 25, roots plus or minus 5, then for less than or equal take between them, inclusive.",
   [{"pattern":"wrong_region","expect":2,"message":"For \\(\\leq 0\\) the values sit ON or BETWEEN the roots \\(\\pm 5\\): \\(-5 \\leq x \\leq 5\\). The outside region is where \\(x^2\\) is bigger than 25.","note":"outside instead of between"}])
mc(b[3], "The roots are plus or minus 4. For greater than 0 take outside them.",
   [{"pattern":"wrong_region","expect":1,"message":"For \\(> 0\\) the values lie OUTSIDE the roots \\(\\pm 4\\): \\(x < -4\\) or \\(x > 4\\). Between the roots \\(x^2\\) is smaller than 16.","note":"inside instead of outside"}])
mc(b[4], "The roots are plus or minus 1. For less than 0 take between them.",
   [{"pattern":"wrong_region","expect":1,"message":"For \\(< 0\\) the curve is below the axis BETWEEN the roots \\(\\pm 1\\): \\(-1 < x < 1\\). Outside the roots it is above zero.","note":"outside instead of between"}])
mc(b[5], "Try the point (0, 1): is 1 bigger than 0? That point sits above the line.",
   [{"pattern":"wrong_side","expect":1,"message":"\\(y > x\\) means the \\(y\\) value beats the \\(x\\) value, which is the region ABOVE the line \\(y = x\\). Below the line is where \\(y < x\\).","note":"picked the opposite side"}])
mc(b[6], "Pick a test point below the line, like the origin, and check it makes y smaller than 2x plus 1.",
   [{"pattern":"wrong_side","expect":1,"message":"\\(y < 2x + 1\\) means \\(y\\) is smaller than the line, which is the region BELOW it. Above the line is where \\(y > 2x + 1\\).","note":"picked the opposite side"}])
mc(b[7], "The roots are plus or minus 6. For greater than or equal take outside them, inclusive.",
   [{"pattern":"wrong_region","expect":1,"message":"For \\(\\geq 0\\) the values lie ON or OUTSIDE the roots \\(\\pm 6\\): \\(x \\leq -6\\) or \\(x \\geq 6\\). Between them \\(x^2\\) is less than 36.","note":"inside instead of outside"}])

# SILVER
s = pb["silver"]
mc(s[0], "Factorise to (x minus 2)(x minus 3); for less than 0 take between the roots.",
   [{"pattern":"wrong_region","expect":1,"message":"\\((x-2)(x-3) < 0\\): for \\(< 0\\) take BETWEEN the roots, \\(2 < x < 3\\). Outside the roots both brackets share a sign, so the product is positive.","note":"outside instead of between"}])
mc(s[1], "Factorise to (x plus 3)(x minus 2); for less than or equal take between the roots, inclusive.",
   [{"pattern":"wrong_region","expect":1,"message":"\\((x+3)(x-2) \\leq 0\\): for \\(\\leq 0\\) take BETWEEN the roots, \\(-3 \\leq x \\leq 2\\). Outside the roots the product is positive.","note":"outside instead of between"},
    {"pattern":"wrong_roots","expect":2,"message":"The factors are \\((x+3)(x-2)\\), so the roots are \\(-3\\) and \\(2\\), not \\(-2\\) and \\(3\\). Match each bracket's sign carefully.","note":"sign of roots flipped"}])
mc(s[2], "Factorise to (x minus 5)(x plus 2); for greater than 0 take outside the roots.",
   [{"pattern":"wrong_region","expect":1,"message":"\\((x-5)(x+2) > 0\\): for \\(> 0\\) take OUTSIDE the roots, \\(x < -2\\) or \\(x > 5\\). Between the roots the product is negative.","note":"inside instead of outside"}])
mc(s[3], "Factorise to x(x minus 4); for less than or equal take between the roots 0 and 4.",
   [{"pattern":"wrong_region","expect":1,"message":"\\(x(x-4) \\leq 0\\): for \\(\\leq 0\\) take BETWEEN the roots, \\(0 \\leq x \\leq 4\\). Outside the roots the product is positive.","note":"outside instead of between"}])
mc(s[4], "Substitute x = 0 and y = 0 into each side and see which inequality is true.",
   [{"pattern":"wrong_test","expect":1,"message":"Substitute \\((0, 0)\\): \\(0\\) against \\(0 + 3 = 3\\). Since \\(0 < 3\\), the point satisfies \\(y < x + 3\\), not \\(y > x + 3\\).","note":"read the test backwards"}])
mc(s[5], "Factorise to (x plus 4)(x minus 2); for greater than 0 take outside the roots.",
   [{"pattern":"wrong_region","expect":1,"message":"\\((x+4)(x-2) > 0\\): for \\(> 0\\) take OUTSIDE the roots, \\(x < -4\\) or \\(x > 2\\). Between the roots the product is negative.","note":"inside instead of outside"}])
mc(s[6], "Multiply through by minus 1 and flip the sign to get x squared plus x minus 6 less than 0, then factorise.",
   [{"pattern":"sign_flip","expect":1,"message":"Multiplying by \\(-1\\) flips the sign: \\(x^2 + x - 6 < 0\\), so \\((x+3)(x-2) < 0\\) gives BETWEEN the roots, \\(-3 < x < 2\\). Forgetting to flip gives the outside region.","note":"did not flip the inequality"},
    {"pattern":"wrong_roots","expect":3,"message":"After rearranging to \\(x^2 + x - 6 < 0\\) the factors are \\((x+3)(x-2)\\), so the roots are \\(-3\\) and \\(2\\), not \\(-2\\) and \\(3\\).","note":"root signs flipped"}])

# GOLD
g = pb["gold"]
mc(g[0], "Split the middle term to factorise (2x minus 1)(x minus 3); for less than 0 take between the roots.",
   [{"pattern":"wrong_region","expect":1,"message":"\\((2x-1)(x-3) < 0\\): for \\(< 0\\) take BETWEEN the roots \\(\\tfrac{1}{2}\\) and \\(3\\), so \\(\\tfrac{1}{2} < x < 3\\). Outside the roots the product is positive.","note":"outside instead of between"},
    {"pattern":"wrong_roots","expect":3,"message":"From \\(2x - 1 = 0\\) the root is \\(\\tfrac{1}{2}\\), and from \\(x - 3 = 0\\) it is \\(3\\), not \\(\\tfrac{7}{2}\\). Solve each bracket for its own root.","note":"misread the second root"}])
mc(g[1], "Split the middle term to factorise (3x minus 1)(x plus 2); for greater than or equal take outside the roots.",
   [{"pattern":"wrong_region","expect":1,"message":"\\((3x-1)(x+2) \\geq 0\\): for \\(\\geq 0\\) take OUTSIDE the roots \\(-2\\) and \\(\\tfrac{1}{3}\\), so \\(x \\leq -2\\) or \\(x \\geq \\tfrac{1}{3}\\). Between the roots the product is negative.","note":"inside instead of outside"},
    {"pattern":"one_branch","expect":2,"message":"You need both pieces: \\(x \\leq -2\\) or \\(x \\geq \\tfrac{1}{3}\\). Keeping only \\(x \\geq \\tfrac{1}{3}\\) drops the left-hand branch.","note":"dropped one branch"}])
# g[2] single_value: how many integers x^2-5x+4<=0 -> 1<=x<=4 -> 4
g[2]["hint"] = "Factorise, find the two roots, then count every whole number from the lower root to the upper root, endpoints included."
g[2]["display"] = numberline_svg(0, 5, [], [1, 4], [2, 3],
    "Number line from 0 to 5 with closed circles at 1 and 4 and filled dots at 2 and 3, marking the integers 1 to 4") + CAP + " " + g[2]["display"]
g[2]["misconceptions"] = [
    {"pattern":"excludes_endpoints","expect":2,"message":"The sign is \\(\\leq 0\\), so the roots \\(1\\) and \\(4\\) are included. Counting only the values strictly between (\\(2, 3\\)) gives 2, but 1 and 4 belong as well, making 4.","note":"treated <= as strict"}]
g[2]["guided_steps"] = [
    {"say":"Factorise \\(x^2 - 5x + 4\\). Two numbers multiply to \\(+4\\) and add to \\(-5\\): they are \\(-1\\) and \\(-4\\), giving \\((x-1)(x-4)\\)."},
    {"pre":"From x - 1 = 0:  x = ","post":"","answer":1,"hint":"x - 1 = 0 gives x = 1."},
    {"pre":"From x - 4 = 0:  x = ","post":"","answer":4,"hint":"x - 4 = 0 gives x = 4."},
    {"say":"The sign is \\(\\leq 0\\), so the solution is between the roots, endpoints included: \\(1 \\leq x \\leq 4\\). Count every whole number from 1 to 4."},
    {"pre":"They are 1, 2, 3, 4.  How many?  ","post":"","phase":"substitute","answer":4,"hint":"Count from 1 up to 4, taking both ends."},
    {"pre":"Check the endpoint x = 1:  1² - 5(1) + 4 = ","post":"","phase":"substitute","answer":0,
     "done":"It equals 0, which satisfies \\(\\leq 0\\), so 1 IS counted. The integers 1, 2, 3, 4 give 4.","hint":"1 - 5 + 4. It should be 0."}]
# g[3] single_value: x^2 < 3x+4 -> -1<x<4 -> positive integers 1,2,3 -> 3
g[3]["hint"] = "Rearrange to one side less than 0, factorise, then count only the positive whole numbers between the roots."
g[3]["display"] = numberline_svg(-2, 5, [-1, 4], [], [1, 2, 3],
    "Number line from -2 to 5 with open circles at -1 and 4 and filled dots at 1, 2 and 3, the positive integers between the roots") + CAP + " " + g[3]["display"]
g[3]["misconceptions"] = [
    {"pattern":"includes_root","expect":4,"message":"The inequality is strict, so \\(x = 4\\) is excluded. Including it with \\(1, 2, 3\\) gives 4, but only \\(1, 2, 3\\) satisfy \\(x^2 < 3x + 4\\).","note":"counted the upper root"}]
g[3]["guided_steps"] = [
    {"say":"Rearrange \\(x^2 < 3x + 4\\) to \\(x^2 - 3x - 4 < 0\\). Factorise: two numbers multiply to \\(-4\\) and add to \\(-3\\) are \\(-4\\) and \\(+1\\), giving \\((x-4)(x+1)\\)."},
    {"pre":"From x - 4 = 0:  x = ","post":"","answer":4,"hint":"x - 4 = 0 gives x = 4."},
    {"pre":"From x + 1 = 0:  x = ","post":"","answer":-1,"hint":"x + 1 = 0 gives x = -1."},
    {"say":"For \\(< 0\\) the solution is between the roots: \\(-1 < x < 4\\). We want only the POSITIVE whole numbers inside."},
    {"pre":"The positive integers are 1, 2, 3.  How many?  ","post":"","phase":"substitute","answer":3,"hint":"Count 1, 2, 3; zero is not positive."},
    {"pre":"Check the upper root x = 4:  4² - 3(4) - 4 = ","post":"","phase":"substitute","answer":0,
     "done":"It equals 0, not below zero, so 4 is excluded. The positive integers 1, 2, 3 give 3.","hint":"16 - 12 - 4. It should be 0."}]
mc(g[4], "Solve the quadratic for x less than minus 4 or x greater than 1, then keep only the part with x less than 3.",
   [{"pattern":"dropped_branch","expect":3,"message":"\\((x+4)(x-1) > 0\\) gives \\(x < -4\\) or \\(x > 1\\). Applying \\(x < 3\\) keeps \\(1 < x < 3\\) AND the whole \\(x < -4\\) branch. Dropping \\(x < -4\\) loses part of the answer.","note":"forgot the left branch"},
    {"pattern":"wrong_region","expect":1,"message":"\\((x+4)(x-1) > 0\\) means OUTSIDE the roots, not between them. Between \\(-4\\) and \\(1\\) the quadratic is below zero, so it fails the first condition.","note":"took inside region"}])

# tier descriptions
pb["bronze_description"] = "Difference of squares and reading regions, plus which side of a line an inequality shades"
pb["silver_description"] = "Factorise three-term quadratics, strict and inclusive signs, and test-point region checks"
pb["gold_description"] = "Coefficient of x squared not 1, rearranging, integer counts and combined conditions"

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: between or outside the roots, and shading a region",
  "steps": [
   "Find the two roots. For \\(x^2 = k\\) they are \\(\\pm\\sqrt{k}\\); for a product like \\((x+2)(x-2)\\) set each bracket to zero.",
   "Sketch the U-shape crossing at the roots. For \\(< 0\\) or \\(\\leq 0\\) take BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) take OUTSIDE them.",
   "For a line \\(y > \\) or \\(y < \\), test the origin: if it fits, its side is shaded (above for greater, below for less)."
  ],
  "example": {
   "question": "Solve \\(x^2 - 16 < 0\\). Give the upper bound.",
   "steps": [
    {"label":"Find roots","content":"\\(x^2 = 16\\), so \\(x = \\pm 4\\)."},
    {"label":"Choose the region","content":"\\(< 0\\) means between the roots: \\(-4 < x < 4\\)."},
    {"label":"Check","content":"At \\(x = 0\\): \\(0 - 16 = -16\\), below zero. Correct."},
    {"label":"Answer","content":"The upper bound is \\(4\\).","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "silver": {
  "title": "Silver: below and above zero, with \\(\\leq\\), \\(\\geq\\) and test points",
  "steps": [
   "Factorise the three-term quadratic to find the two roots.",
   "For \\(< 0\\) or \\(\\leq 0\\) the curve is below the axis BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) it is above OUTSIDE them.",
   "Use \\(\\leq\\) or \\(\\geq\\) when the sign includes equals; to check a region, substitute a point and see if it fits."
  ],
  "example": {
   "question": "Solve \\(x^2 - x - 12 \\geq 0\\). Give the smaller critical value.",
   "steps": [
    {"label":"Factorise","content":"\\((x-4)(x+3) = 0\\), roots \\(-3\\) and \\(4\\)."},
    {"label":"Choose the region","content":"\\(\\geq 0\\) means outside the roots: \\(x \\leq -3\\) or \\(x \\geq 4\\)."},
    {"label":"Check","content":"At \\(x = 5\\): \\(25 - 5 - 12 = 8 \\geq 0\\). Correct."},
    {"label":"Answer","content":"The smaller critical value is \\(-3\\).","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "gold": {
  "title": "Gold: coefficient of \\(x^2\\), rearranging, counts and combined conditions",
  "steps": [
   "Rearrange so one side is 0 first; if you multiply by \\(-1\\), flip the inequality sign.",
   "When \\(x^2\\) has a coefficient, split the middle term to factorise; roots may be fractions.",
   "For an integer count list the whole numbers in the range; for a combined condition solve each part then take the overlap."
  ],
  "example": {
   "question": "Solve \\(2x^2 + 3x - 2 < 0\\). Give the upper bound as a decimal.",
   "steps": [
    {"label":"Split the middle term","content":"\\(2x^2 + 3x - 2 = (2x-1)(x+2)\\), roots \\(-2\\) and \\(\\tfrac{1}{2}\\)."},
    {"label":"Choose the region","content":"\\(< 0\\) means between the roots: \\(-2 < x < \\tfrac{1}{2}\\)."},
    {"label":"Check","content":"At \\(x = 0\\): \\(0 + 0 - 2 = -2\\), below zero. Correct."},
    {"label":"Answer","content":"The upper bound is \\(0.5\\).","isAnswer":True,"is_answer":True}
   ]
  }
 }
}

# ---------- guided (opener + teach) ----------
opener = {
 "steps": [
  {"say":"Here is a number machine. It multiplies \\((x - 2)\\) by \\((x - 6)\\). We want the values of x that make the answer come out BELOW zero (negative). Let us test a few."},
  {"pre":"Try x = 7. First bracket:  7 - 2 = ","post":"","answer":5,"hint":"7 take away 2."},
  {"say":"The second bracket is \\(7 - 6 = 1\\). Both are positive, so \\(5 \\times 1 = 5\\), above zero. Now slide x down to 4, in between 2 and 6."},
  {"pre":"First bracket:  4 - 2 = ","post":"","answer":2,"hint":"4 take away 2."},
  {"pre":"Second bracket:  4 - 6 = ","post":"","answer":-2,"hint":"4 is less than 6, so this drops below zero."},
  {"say":"One bracket is positive, the other negative, and a positive times a negative is always NEGATIVE. So the answer is below zero, and that only happens when x sits BETWEEN 2 and 6. That is the whole method for a quadratic inequality: factorise to two brackets, find the two roots, and the expression is below zero between them, above zero outside them. In algebra, \\((x-2)(x-6) < 0\\) has the solution \\(2 < x < 6\\)."}
 ]
}

teach = {
 "bronze": {
  "display": parabola_svg(-4, 4, "between",
    "y = x squared minus 16",
    "U-shaped parabola y = x squared minus 16 crossing the x-axis at minus 4 and 4, with the region below the axis between the roots shaded")
    + CAP + "Solve \\(x^2 - 16 < 0\\)",
  "steps": [
   {"say":"This is a difference of squares. \\(x^2 - 16 = 0\\) means \\(x^2 = 16\\), so the roots are \\(\\pm 4\\). Each is where the curve crosses the axis."},
   {"pre":"The positive root is x = ","post":"","answer":4,"hint":"The square root of 16."},
   {"pre":"The negative root is x = ","post":"","answer":-4,"hint":"The other square root of 16."},
   {"say":"It is a U-shape, so it dips BELOW the axis between the roots. That is where the expression is \\(< 0\\)."},
   {"pre":"The solution is written -4 < x < 4. The lower bound is  ","post":"","answer":-4,"hint":"The smaller of the two roots."},
   {"pre":"Check with x = 0, in the middle:  0² - 16 = ","post":"","answer":-16,
    "done":"Below zero, so -4 < x < 4 is right. Find the roots, take the region between them: that is the whole bronze move.","hint":"0 minus 16. It should be below zero."}
  ]
 },
 "silver": {
  "display": parabola_svg(-3, 4, "outside",
    "y = x squared minus x minus 12",
    "U-shaped parabola y = x squared minus x minus 12 crossing the x-axis at minus 3 and 4, with the regions above the axis outside the roots shaded")
    + CAP + "Solve \\(x^2 - x - 12 \\geq 0\\)",
  "steps": [
   {"say":"Factorise. Two numbers multiply to \\(-12\\) and add to \\(-1\\): they are \\(-4\\) and \\(+3\\), so \\(x^2 - x - 12 = (x-4)(x+3)\\)."},
   {"pre":"The bracket x - 4 is zero when x = ","post":"","answer":4,"hint":"x - 4 = 0."},
   {"pre":"The bracket x + 3 is zero when x = ","post":"","answer":-3,"hint":"x + 3 = 0, so x is negative."},
   {"say":"The roots are \\(-3\\) and \\(4\\). The sign is \\(\\geq 0\\), so we want where the U-shape is ON or ABOVE the axis. That is OUTSIDE the roots, not between them."},
   {"pre":"The left piece is x less than or equal to  ","post":"","answer":-3,"hint":"On or below the smaller root."},
   {"pre":"Check a value outside, x = 5:  5² - 5 - 12 = ","post":"","answer":8,
    "done":"Above zero, so the outside region is right. Taking OUTSIDE the roots for a greater-or-equal sign is the new silver move.","hint":"25 minus 5 minus 12. It should be zero or above."}
  ]
 },
 "gold": {
  "display": parabola_svg(-2, 0.5, "between",
    "y = 2x squared plus 3x minus 2",
    "U-shaped parabola y = 2x squared plus 3x minus 2 crossing the x-axis at minus 2 and one half, with the region below the axis between the roots shaded")
    + CAP + "Solve \\(2x^2 + 3x - 2 < 0\\)",
  "steps": [
   {"say":"With a 2 in front of \\(x^2\\), split the middle term. Two numbers multiply to \\((2)(-2) = -4\\) and add to \\(+3\\): they are \\(+4\\) and \\(-1\\). Grouping gives \\(2x^2 + 4x - x - 2 = 2x(x+2) - (x+2) = (2x-1)(x+2)\\)."},
   {"pre":"From 2x - 1 = 0, first 2x = ","post":"","answer":1,"hint":"Add 1 to both sides."},
   {"pre":"So x = 1 ÷ 2 = ","post":"","answer":0.5,"hint":"Divide by 2; it is a fraction."},
   {"pre":"From x + 2 = 0:  x = ","post":"","answer":-2,"hint":"x = -2."},
   {"say":"The roots are \\(-2\\) and \\(0.5\\). The sign is \\(< 0\\), so we want the U-shape BELOW the axis, which is BETWEEN the roots: \\(-2 < x < 0.5\\)."},
   {"pre":"Check x = 0 (between the roots):  2(0²) + 3(0) - 2 = ","post":"","answer":-2,
    "done":"Below zero, so -2 < x < 0.5 is right. Splitting the middle term when x squared has a coefficient is the gold move.","hint":"Everything with x vanishes, leaving the constant."}
  ]
 }
}

# ---------- method_card (slim) ----------
method_card = {
 "title": "Quadratic Inequalities & Graphical Regions",
 "steps": [
  "Rearrange so one side is 0, then factorise to find the two roots.",
  "Sketch the U-shape (positive \\(x^2\\)) crossing the x-axis at the roots.",
  "For \\(< 0\\) or \\(\\leq 0\\) take BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) take OUTSIDE them.",
  "For a region, test a point (like the origin) to see which side of the line to shade."
 ],
 "content": "<p>A <strong>quadratic inequality</strong> asks which values of \\(x\\) make a quadratic above or below zero. Find the roots, sketch the parabola, then read off the region.</p><p><strong>Below zero</strong> (\\(< 0\\), \\(\\leq 0\\)) sits between the roots; <strong>above zero</strong> (\\(> 0\\), \\(\\geq 0\\)) sits outside them. For a line, above is \\(y >\\), below is \\(y <\\).</p>",
 "example": "<p><strong>Solve</strong> \\(x^2 - 5x + 6 < 0\\).</p><p>\\((x-2)(x-3) = 0\\) gives roots \\(2\\) and \\(3\\). Below zero is between the roots, so \\(2 < x < 3\\).</p>"
}

# ---------- assemble ----------
out = {
 "guided": {"opener": opener, "teach": teach},
 "method_card": method_card,
 "tier_guides": tier_guides,
 "topic_links": live["topic_links"],
 "problem_bank": pb,
 "related_videos": live["related_videos"],
 "worked_examples": live["worked_examples"]
}

with open(r"lesson_maths-eduqas_algebra-L12.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("written. bronze",len(pb['bronze']),"silver",len(pb['silver']),"gold",len(pb['gold']))
