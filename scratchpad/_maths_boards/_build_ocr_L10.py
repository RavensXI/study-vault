# -*- coding: utf-8 -*-
import json, math

MINUS = "−"   # unicode minus for prose
SUP2  = "²"   # superscript two
TIMES = "×"

def fx(n):
    # LaTeX number (ASCII minus)
    if isinstance(n, float) and n == int(n):
        n = int(n)
    return str(n)

def pn(n):
    # prose number (unicode minus)
    if isinstance(n, float) and n == int(n):
        n = int(n)
    s = str(n)
    return s.replace("-", MINUS)

def brk(r):
    # bracket factor "x - 4" / "x + 1"  (LaTeX)
    if r >= 0:
        return "x - %s" % fx(r)
    return "x + %s" % fx(-r)

def sign_flip(quad_tex, r1, r2, tail="which do not fit the equations"):
    return ("Check the signs inside your brackets. \\(%s\\) factorises as \\((%s)(%s) = 0\\), "
            "giving \\(x = %s\\) and \\(x = %s\\). Reversing those signs gives \\(x = %s\\) and \\(x = %s\\), %s."
            % (quad_tex, brk(r1), brk(r2), fx(r1), fx(r2), fx(-r1), fx(-r2), tail))

def m_divx(N):
    return {"pattern": "divide_by_x", "expect": None,
            "message": ("When you reach \\(x^2 - %sx = 0\\), factorise as \\(x(x - %s) = 0\\) rather than dividing "
                        "both sides by x. Dividing by x throws away the solution \\(x = 0\\).") % (fx(N), fx(N))}

def m_posroot(k):
    return {"pattern": "positive_root_only", "expect": None,
            "message": ("\\(x^2 = %s\\) means \\(x = %s\\) and \\(x = %s\\). Remember the negative square root as well "
                        "as the positive one.") % (fx(k), fx(int(math.sqrt(k))), fx(-int(math.sqrt(k))))}

def m_sqbr(bracket_tex, full_tex, lost):
    return {"pattern": "square_bracket_error", "expect": None,
            "message": ("Expand \\(%s\\) in full as \\(%s\\); squaring the terms separately loses the %s."
                        % (bracket_tex, full_tex, lost))}

def m_flip(quad_tex, r1, r2, expect):
    return {"pattern": "factor_sign_flip", "expect": expect,
            "note": "sign-flipped factorisation of %s" % quad_tex,
            "message": sign_flip(quad_tex, r1, r2)}

# ---------- TYPE A: both sides y = ; set equal ----------
def steps_setequal(line_tex, curve_tex, a, b, c, d, r1, r2, line_desc):
    xc = c - a           # x coefficient after moving line across
    kc = d - b           # constant
    y1 = a*r1 + b; y2 = a*r2 + b
    assert r1*r1 + c*r1 + d == y1, (r1, y1)
    assert r2*r2 + c*r2 + d == y2, (r2, y2)
    # verify roots of x^2 + xc x + kc
    assert r1*r1 + xc*r1 + kc == 0
    assert r2*r2 + xc*r2 + kc == 0
    steps = []
    steps.append({"say": "Both equations give y, so set the two right sides equal: \\(%s = %s\\). "
                         "Bring every term to the right so \\(x^2\\) stays positive." % (line_tex, curve_tex)})
    steps.append({"pre": "The x-term becomes ", "post": "x",
                  "hint": "Take the line's x-term across the equals sign, changing its sign, then combine.",
                  "answer": xc})
    steps.append({"pre": "and the constant becomes ", "post": "",
                  "hint": "Take the line's constant across the equals sign, changing its sign.",
                  "answer": kc})
    # quadratic tex
    def term(coef, var):
        if coef == 0: return ""
        sign = " + " if coef > 0 else " " + MINUS + " "
        mag = abs(coef)
        body = ("" if (mag == 1 and var) else fx(mag)) + var
        return sign + body
    quad = "x^2" + term(xc, "x") + term(kc, "")
    quad = quad.replace(MINUS, "-")  # inside LaTeX use ascii
    if kc == 0:
        say3 = "So \\(%s = 0\\). Take out a common factor of x: \\(x(x %s %s) = 0\\)." % (
            quad, "-" if -xc>=0 else "+", fx(abs(xc)))
        # x(x - (-xc))  ; roots 0 and -xc
        steps.append({"pre": "First root, x = ", "say": say3, "post": "",
                      "hint": "Set the bracket x to zero.", "phase": "substitute", "answer": r1})
        steps.append({"pre": "Second root, x = ", "post": "",
                      "hint": "Set the other bracket to zero.", "answer": r2})
    else:
        say3 = ("So \\(%s = 0\\). Two numbers multiply to %s and add to %s: they are %s and %s, "
                "giving \\((%s)(%s) = 0\\)." % (quad, pn(kc), pn(xc), pn(-r1), pn(-r2), brk(r1), brk(r2)))
        steps.append({"pre": "First root, x = ", "say": say3, "post": "",
                      "hint": "Set %s = 0." % brk(r1), "phase": "substitute", "answer": r1})
        steps.append({"pre": "Second root, x = ", "post": "",
                      "hint": "Set %s = 0." % brk(r2), "answer": r2})
    steps.append({"pre": "At x = %s: y = " % pn(r1),
                  "say": "Now each x gets its y from the line \\(%s\\)." % line_desc,
                  "post": "", "hint": "Put x = %s into the line." % pn(r1), "answer": y1})
    steps.append({"pre": "At x = %s: y = " % pn(r2), "post": "",
                  "hint": "Put x = %s into the line." % pn(r2), "answer": y2})
    # check via curve at r1
    cterm = ""
    if c: cterm = (" + %s%s" % (fx(c), TIMES + pn(r1))) if c>0 else (" %s %s%s" % (MINUS, fx(-c), TIMES + pn(r1)))
    dterm = ""
    if d: dterm = (" + %s" % fx(d)) if d>0 else (" %s %s" % (MINUS, fx(-d)))
    curve_calc = "%s%s%s%s" % (pn(r1), SUP2, cterm, dterm)
    steps.append({"pre": "Work out %s = " % curve_calc,
                  "say": "Last check: put the first pair into the curve.",
                  "done": "It equals y = %s, so (%s, %s) is right and (%s, %s) checks the same way." % (
                      pn(y1), pn(r1), pn(y1), pn(r2), pn(y2)),
                  "post": "", "hint": "Substitute x = %s into the curve; it should give y = %s." % (pn(r1), pn(y1)),
                  "answer": y1})
    return steps, quad

# ---------- circle monic (x2coef==2, divide by 2, factorises) ----------
def steps_circle_monic(line_disp_tex, y_subj_tex, R, m, k, r1, r2, circle_lbl, mid_hint, expand_tex):
    mid = 2*m*k
    assert 1 + m*m == 2
    const = k*k - R
    xc = mid//2; kc = const//2
    assert r1*r1 + xc*r1 + kc == 0 and r2*r2 + xc*r2 + kc == 0
    y1 = m*r1 + k; y2 = m*r2 + k
    assert r1*r1 + y1*y1 == R and r2*r2 + y2*y2 == R
    quad_full = "2x^2 %s %s = 0" % ("+ %sx" % fx(mid) if mid>=0 else "- %sx" % fx(-mid),
                                    "+ %s" % fx(const) if const>=0 else "- %s" % fx(-const))
    monic = "x^2 %s %s" % ("+ %sx" % fx(xc) if xc>=0 else "- %sx" % fx(-xc),
                           "+ %s" % fx(kc) if kc>=0 else "- %s" % fx(-kc))
    steps = [
      {"pre": "The middle term, %s, is " % mid_hint[0], "post": "x",
       "say": ("Rearrange the line \\(%s\\) to \\(y = %s\\). Substitute into \\(%s\\): "
               "\\(x^2 + (%s)^2 = %s\\). Expand \\((%s)^2 = %s\\)." % (
                   line_disp_tex, y_subj_tex, circle_lbl, y_subj_tex, fx(R), y_subj_tex, expand_tex)),
       "hint": mid_hint[1], "answer": mid},
      {"pre": "Collect the two x² terms: 1 + 1 = ", "post": "x²",
       "hint": "One x² from each part.", "answer": 2},
      {"pre": "The constant, %s %s %s, becomes " % (fx(k*k), MINUS, fx(R)), "post": "",
       "hint": ("%s minus %s." % (fx(k*k), fx(R))) if const>=0 else ("%s minus %s is negative." % (fx(k*k), fx(R))),
       "answer": const},
      {"pre": "First root, x = ",
       "say": ("So \\(%s\\). Divide every term by 2 to get \\(%s = 0\\), which factorises as \\((%s)(%s) = 0\\)."
               % (quad_full, monic, brk(r1), brk(r2))),
       "post": "", "hint": "Set %s = 0." % brk(r1), "phase": "substitute", "answer": r1},
      {"pre": "Second root, x = ", "post": "", "hint": "Set %s = 0." % brk(r2), "answer": r2},
      {"pre": "At x = %s: y = " % pn(r1),
       "say": "Each x gets its y from \\(y = %s\\)." % y_subj_tex,
       "post": "", "hint": "Work out the line at x = %s." % pn(r1), "answer": y1},
      {"pre": "At x = %s: y = " % pn(r2), "post": "",
       "hint": "Work out the line at x = %s." % pn(r2), "answer": y2},
      {"pre": "Check (%s, %s) in the circle: %s%s + %s%s = " % (pn(r1), pn(y1), pn(r1), SUP2, pn(y1), SUP2),
       "done": "It equals %s, so (%s, %s) is right and (%s, %s) checks the same way." % (
           fx(R), pn(r1), pn(y1), pn(r2), pn(y2)),
       "post": "", "hint": "%s + %s." % (fx(r1*r1), fx(y1*y1)), "answer": R},
    ]
    return steps, monic, y1, y2

# ---------- SVG for circles ----------
CX, CY, S = 130.0, 105.0, 13.0
def ppx(x, y): return (CX + x*S, CY - y*S)
def build_svg(cid, R, line_fn, sols, circle_lbl, line_lbl, aria):
    r = math.sqrt(R) * S
    lx1, ly1 = ppx(-9.0, line_fn(-9.0)); lx2, ly2 = ppx(9.0, line_fn(9.0))
    dots = ""
    for x in sols:
        dx, dy = ppx(x, line_fn(x))
        dots += '<circle cx="%.1f" cy="%.1f" r="3.2" fill="#f59e0b"/>' % (dx, dy)
        ox = 7 if dx >= CX else -14
        oy = -5 if dy <= CY else 14
        dots += '<text x="%.1f" y="%.1f" font-size="12" font-family="Inter,sans-serif" fill="currentColor">?</text>' % (dx+ox, dy+oy)
    return ('<svg viewBox="0 0 260 224" role="img" aria-label="%s" style="max-width:280px">' % aria +
      '<defs><clipPath id="%s"><rect x="6" y="6" width="248" height="196"/></clipPath></defs>' % cid +
      '<g clip-path="url(#%s)">' % cid +
      '<line x1="8" y1="105" x2="252" y2="105" stroke="currentColor" stroke-width="1" opacity="0.35"/>' +
      '<line x1="130" y1="10" x2="130" y2="198" stroke="currentColor" stroke-width="1" opacity="0.35"/>' +
      '<circle cx="130" cy="105" r="%.1f" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>' % r +
      '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#f59e0b" stroke-width="1.8"/>' % (lx1, ly1, lx2, ly2) +
      '</g>' +
      '<text x="250" y="101" font-size="10" font-family="Inter,sans-serif" fill="currentColor" text-anchor="end">x</text>' +
      '<text x="134" y="18" font-size="10" font-family="Inter,sans-serif" fill="currentColor">y</text>' +
      '<text x="122" y="118" font-size="10" font-family="Inter,sans-serif" fill="currentColor">O</text>' +
      '<text x="8" y="20" font-size="10.5" font-family="Inter,sans-serif" fill="currentColor">%s</text>' % circle_lbl +
      '<text x="8" y="219" font-size="10.5" font-family="Inter,sans-serif" fill="currentColor">%s</text>' % line_lbl +
      dots + '</svg>')

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'
SET_HINT = "Set the two right-hand sides equal, rearrange to a quadratic equal to zero, then factorise."
CIR_HINT = "Rearrange the line to make y the subject, substitute into the circle, and expand the bracket in full."

def circle_disp(cid, R, line_fn, sols, clbl, llbl, aria, tail_tex):
    svg = build_svg(cid, R, line_fn, sols, clbl, llbl, aria)
    return svg + CAP + tail_tex

# ================= ASSEMBLY =================
orig = json.load(open("_pre_L10ocr.json", encoding="utf-8"))

# ---- OPENER ----
opener = {
  "label": "Before any algebra",
  "display": "I square my number and get 12 more than the number itself.",
  "steps": [
    {"pre": "One number that works is ", "post": "",
     "say": "A guess-the-number puzzle, no algebra needed. I am thinking of a number. When I square it, I get 12 more than the number I started with.",
     "hint": "Try 4: four squared is 16, and 16 is 12 more than 4.", "answer": 4},
    {"pre": "The other number is ", "post": "",
     "say": "Good. There is a second number that also works, and it is negative.",
     "hint": "Try " + MINUS + "3: negative three squared is 9, and 9 is 12 more than " + MINUS + "3.", "answer": -3},
    {"say": "You just solved \\(x^2 = x + 12\\) and found BOTH answers, \\(x = 4\\) and \\(x = -3\\). That is the whole topic: an equation with a square in it usually has TWO answers. In algebra it appears as a line \\(y = x + 12\\) crossing a curve \\(y = x^2\\); they meet at two points, so there are two x-values to find."}
  ]
}

# ---- TEACH ----
teach_bronze = {"label": "Together: your first one",
  "display": "Solve \\(y = x + 3\\) and \\(y = x^2 - 3\\)", "steps": [
    {"say": "Both equations give y, so set the two right sides equal: \\(x + 3 = x^2 - 3\\). Bring every term to the right so \\(x^2\\) stays positive."},
    {"pre": "The x-term becomes ", "post": "x", "hint": "The line's +x moves across to become " + MINUS + "x.", "answer": -1},
    {"pre": "and the constant becomes ", "post": "", "hint": "The +3 crosses to " + MINUS + "3, and " + MINUS + "3 stays, so " + MINUS + "3 " + MINUS + " 3.", "answer": -6},
    {"pre": "First root, x = ", "say": "So \\(x^2 - x - 6 = 0\\). Two numbers multiply to " + MINUS + "6 and add to " + MINUS + "1: they are " + MINUS + "3 and 2, giving \\((x - 3)(x + 2) = 0\\).", "post": "", "hint": "Set x " + MINUS + " 3 = 0.", "answer": 3},
    {"pre": "Second root, x = ", "post": "", "hint": "Set x + 2 = 0.", "answer": -2},
    {"pre": "At x = 3: y = ", "say": "Now each x gets its y from \\(y = x + 3\\).", "post": "", "hint": "3 + 3.", "answer": 6},
    {"pre": "At x = " + MINUS + "2: y = ", "post": "", "hint": "Negative 2, plus 3.", "answer": 1},
    {"pre": "Check x = 3 in the curve: 3" + SUP2 + " " + MINUS + " 3 = ", "done": "It equals y = 6, so (3, 6) is right and (" + MINUS + "2, 1) checks the same way.", "post": "", "hint": "9 " + MINUS + " 3.", "answer": 6}
  ]}

teach_silver = {"label": "Together: the silver move",
  "display": "Solve \\(y = 2x - 1\\) and \\(y = x^2 - 4x + 4\\)", "steps": [
    {"say": "Set the two right sides equal: \\(2x - 1 = x^2 - 4x + 4\\). There are x-terms and numbers on both sides, so move everything to the right with care."},
    {"pre": "Collect the x-terms, " + MINUS + "4x " + MINUS + " 2x = ", "post": "x", "hint": "Negative 4 minus 2 is negative 6.", "answer": -6},
    {"pre": "Collect the constants, 4 + 1 = ", "post": "", "hint": "The " + MINUS + "1 crosses to become +1, so 4 + 1.", "answer": 5},
    {"pre": "First root, x = ", "say": "So \\(x^2 - 6x + 5 = 0\\), which factorises as \\((x - 1)(x - 5) = 0\\).", "post": "", "hint": "Set x " + MINUS + " 1 = 0.", "answer": 1},
    {"pre": "Second root, x = ", "post": "", "hint": "Set x " + MINUS + " 5 = 0.", "answer": 5},
    {"pre": "At x = 1: y = ", "say": "Each x gets its y from \\(y = 2x - 1\\).", "post": "", "hint": "2 times 1, minus 1.", "answer": 1},
    {"pre": "At x = 5: y = ", "post": "", "hint": "2 times 5, minus 1.", "answer": 9},
    {"pre": "Check x = 5 in the curve: 5" + SUP2 + " " + MINUS + " 4" + TIMES + "5 + 4 = ", "done": "It equals y = 9, so (5, 9) is right and (1, 1) checks the same way.", "post": "", "hint": "25 " + MINUS + " 20 + 4.", "answer": 9}
  ]}

teach_gold = {"label": "Together: the gold move",
  "display": "Solve \\(x + y = 6\\) and \\(x^2 + y^2 = 20\\)", "steps": [
    {"pre": "The middle term, 2 " + TIMES + " 6 " + TIMES + " (" + MINUS + "1), is ", "post": "x", "say": "The second equation is a circle. Rearrange the line \\(x + y = 6\\) to \\(y = 6 - x\\). Substitute into \\(x^2 + y^2 = 20\\): \\(x^2 + (6 - x)^2 = 20\\). Expand \\((6 - x)^2 = 36 - 12x + x^2\\).", "hint": "2 times 6 is 12, and it is negative.", "answer": -12},
    {"pre": "Collect the two x² terms: 1 + 1 = ", "post": "x²", "say": "So \\(x^2 + 36 - 12x + x^2 = 20\\).", "hint": "One x² from each part.", "answer": 2},
    {"pre": "The constant, 36 " + MINUS + " 20, becomes ", "post": "", "say": "That gives \\(2x^2 - 12x + 36 = 20\\). Take 20 across.", "hint": "36 minus 20.", "answer": 16},
    {"pre": "First root, x = ", "say": "So \\(2x^2 - 12x + 16 = 0\\). Divide every term by 2 to get \\(x^2 - 6x + 8 = 0\\), which factorises as \\((x - 2)(x - 4) = 0\\).", "post": "", "hint": "Set x " + MINUS + " 2 = 0.", "answer": 2},
    {"pre": "Second root, x = ", "post": "", "hint": "Set x " + MINUS + " 4 = 0.", "answer": 4},
    {"pre": "At x = 2: y = ", "say": "Each x gets its y from \\(y = 6 - x\\).", "post": "", "hint": "6 " + MINUS + " 2.", "answer": 4},
    {"pre": "At x = 4: y = ", "post": "", "hint": "6 " + MINUS + " 4.", "answer": 2},
    {"pre": "Check (2, 4) in the circle: 2" + SUP2 + " + 4" + SUP2 + " = ", "done": "It equals 20, so (2, 4) is right and (4, 2) checks the same way.", "post": "", "hint": "4 + 16.", "answer": 20}
  ]}

guided = {"opener": opener, "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold}}

# ---- TIER GUIDES ----
tier_guides = {
  "bronze": {"title": "Bronze: substitute, factorise, two answers",
    "steps": [
      "Both equations are written as <strong>y = …</strong>, so set the two right-hand sides equal to each other.",
      "Move every term to one side to get a quadratic equal to zero, then factorise it.",
      "Each bracket gives one x-value. Put each x back into the linear equation to find its y."],
    "example": {"question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 1\\)", "steps": [
      {"label": "Set equal", "content": "<p>\\(x + 1 = x^2 - 1\\)</p>"},
      {"label": "Rearrange", "content": "<p>\\(x^2 - x - 2 = 0\\)</p>"},
      {"label": "Factorise", "content": "<p>\\((x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\)</p>"},
      {"label": "Find y", "content": "<p>\\(x = 2: y = 3\\). \\(x = -1: y = 0\\).</p>"},
      {"label": "Check", "content": "<p>\\(x = 2\\) in \\(y = x^2 - 1\\): \\(4 - 1 = 3\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 2, y = 3\\) and \\(x = -1, y = 0\\)</p>", "isAnswer": True, "is_answer": True}]}},
  "silver": {"title": "Silver: rearrange first, then substitute",
    "steps": [
      "The linear part may be \\(y = 2x - 1\\), \\(x + y = 5\\), or \\(xy = 10\\); rearrange it to make one letter the subject first.",
      "Substitute, expand any bracket in full, and gather x-terms and numbers from <strong>both</strong> sides.",
      "Factorise the quadratic, then find each y from the linear equation."],
    "example": {"question": "Solve \\(x + y = 5\\) and \\(x^2 + y^2 = 13\\)", "steps": [
      {"label": "Rearrange line", "content": "<p>\\(y = 5 - x\\)</p>"},
      {"label": "Substitute", "content": "<p>\\(x^2 + (5 - x)^2 = 13\\) → \\(2x^2 - 10x + 12 = 0\\)</p>"},
      {"label": "Simplify and factorise", "content": "<p>\\(x^2 - 5x + 6 = 0\\) → \\((x - 2)(x - 3) = 0\\), so \\(x = 2\\) or \\(x = 3\\)</p>"},
      {"label": "Find y", "content": "<p>\\(x = 2: y = 3\\). \\(x = 3: y = 2\\).</p>"},
      {"label": "Check", "content": "<p>\\((2, 3)\\): \\(4 + 9 = 13\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 2, y = 3\\) and \\(x = 3, y = 2\\)</p>", "isAnswer": True, "is_answer": True}]}},
  "gold": {"title": "Gold: circles and the quadratic formula",
    "steps": [
      "For a circle \\(x^2 + y^2 = r^2\\), rearrange the line to \\(y = …\\) and substitute, squaring the bracket in full.",
      "\\((a - x)^2 = a^2 - 2ax + x^2\\): never square the two terms separately.",
      "If the quadratic will not factorise, use the formula and give the two x-values as asked."],
    "example": {"question": "Solve \\(x + y = 7\\) and \\(x^2 + y^2 = 29\\)", "steps": [
      {"label": "Rearrange line", "content": "<p>\\(y = 7 - x\\)</p>"},
      {"label": "Substitute", "content": "<p>\\(x^2 + (7 - x)^2 = 29\\) → \\(2x^2 - 14x + 20 = 0\\)</p>"},
      {"label": "Simplify and factorise", "content": "<p>\\(x^2 - 7x + 10 = 0\\) → \\((x - 2)(x - 5) = 0\\), so \\(x = 2\\) or \\(x = 5\\)</p>"},
      {"label": "Find y", "content": "<p>\\(x = 2: y = 5\\). \\(x = 5: y = 2\\).</p>"},
      {"label": "Check", "content": "<p>\\((2, 5)\\): \\(4 + 25 = 29\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 2, y = 5\\) and \\(x = 5, y = 2\\)</p>", "isAnswer": True, "is_answer": True}]}}
}

# ---- METHOD CARD (slim) ----
method_card = {
  "title": "Simultaneous Equations (One Linear, One Quadratic)",
  "steps": [
    "Rearrange the linear equation to make one letter the subject.",
    "Substitute it into the quadratic, expanding any bracket in full.",
    "Rearrange to a quadratic equal to zero, then factorise or use the formula.",
    "Substitute each x back into the linear equation for its y, and give both pairs."],
  "content": "<p>When one equation is a straight line and the other is a curve (a quadratic, or a circle \\(x^2 + y^2 = r^2\\)), use <strong>substitution</strong>. The line usually crosses the curve at two points, so expect two pairs of answers.</p><p>Make a letter the subject of the line, substitute it in, and simplify to a quadratic equal to zero. Solve it, then find each matching value from the line. Always give answers as pairs.</p>",
  "example": "<p><strong>Solve</strong> \\(y = x + 1\\) and \\(y = x^2 - 1\\)</p><p>\\(x + 1 = x^2 - 1 \\Rightarrow x^2 - x - 2 = 0 \\Rightarrow (x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\). Then \\(y = 3\\) or \\(y = 0\\): the pairs are \\((2, 3)\\) and \\((-1, 0)\\).</p>"
}

def P(display, sols, gs, misc, hint, calc=False):
    return {"hint": hint, "display": display, "solutions": sols, "calculator": calc,
            "input_type": "two_solutions", "guided_steps": gs, "misconceptions": misc}

# ---- BRONZE (set-equal) ----
def setP(disp, line_tex, curve_tex, a, b, c, d, r1, r2, line_desc, misc_fn):
    gs, quad = steps_setequal(line_tex, curve_tex, a, b, c, d, r1, r2, line_desc)
    return P(disp, [r1, r2], gs, misc_fn(quad, r1, r2), SET_HINT)

bronze = [
  setP("Solve \\(y = x + 1\\) and \\(y = x^2 - 2x - 3\\). Give the two x-values.",
       "x + 1", "x^2 - 2x - 3", 1,1,-2,-3, 4,-1, "y = x + 1",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
  setP("Solve \\(y = 3x\\) and \\(y = x^2 + 2\\). Give the two x-values.",
       "3x", "x^2 + 2", 3,0,0,2, 1,2, "y = 3x",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
  setP("Solve \\(y = x + 2\\) and \\(y = x^2\\). Give the two x-values.",
       "x + 2", "x^2", 1,2,0,0, 2,-1, "y = x + 2",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
  setP("Solve \\(y = 2x\\) and \\(y = x^2 - 3\\). Give the two x-values.",
       "2x", "x^2 - 3", 2,0,0,-3, 3,-1, "y = 2x",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
  setP("Solve \\(y = x + 5\\) and \\(y = x^2 + 3x + 2\\). Give the two x-values.",
       "x + 5", "x^2 + 3x + 2", 1,5,3,2, 1,-3, "y = x + 5",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
  setP("Solve \\(y = 2x + 3\\) and \\(y = x^2 + 3\\). Give the two x-values.",
       "2x + 3", "x^2 + 3", 2,3,0,3, 0,2, "y = 2x + 3",
       lambda q,r1,r2:[m_divx(2)]),
  setP("Solve \\(y = x - 1\\) and \\(y = x^2 - 4x + 5\\). Give the two x-values.",
       "x - 1", "x^2 - 4x + 5", 1,-1,-4,5, 2,3, "y = x - 1",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
  setP("Solve \\(y = 4 - x\\) and \\(y = x^2 - 2\\). Give the two x-values.",
       "4 - x", "x^2 - 2", -1,4,0,-2, 2,-3, "y = 4 - x",
       lambda q,r1,r2:[m_flip(q,r1,r2,[-r1,-r2])]),
]

# ---- SILVER ----
def cP(disp, line_disp, y_subj, R, m, k, r1, r2, clbl, mid_hint, expand_tex, sqbr_args, flip_expect):
    gs, monic, y1, y2 = steps_circle_monic(line_disp, y_subj, R, m, k, r1, r2, clbl, mid_hint, expand_tex)
    misc = [m_flip(monic, r1, r2, flip_expect), m_sqbr(*sqbr_args)]
    return P(disp, [r1, r2], gs, misc, CIR_HINT)

# S2 manual (leading-coeff 5 circle)
s2_gs = [
  {"pre": "The middle term, 2 " + TIMES + " 2x " + TIMES + " (" + MINUS + "1), is ", "post": "x",
   "say": "Substitute \\(y = 2x - 1\\) into the circle \\(x^2 + y^2 = 10\\): \\(x^2 + (2x - 1)^2 = 10\\). Expand \\((2x - 1)^2 = 4x^2 - 4x + 1\\).",
   "hint": "2 times 2 times 1 is 4, and it is negative.", "answer": -4},
  {"pre": "Collect the x² terms: 1 + 4 = ", "post": "x²", "say": "So \\(x^2 + 4x^2 - 4x + 1 = 10\\).",
   "hint": "One x² from the first part, four from the bracket.", "answer": 5},
  {"pre": "The constant, 1 " + MINUS + " 10, becomes ", "post": "", "say": "That gives \\(5x^2 - 4x + 1 = 10\\). Take 10 across.",
   "hint": "1 minus 10 is negative 9.", "answer": -9},
  {"pre": "From x + 1 = 0, one root is x = ", "say": "So \\(5x^2 - 4x - 9 = 0\\). This factorises as \\((5x - 9)(x + 1) = 0\\).",
   "post": "", "hint": "Set x + 1 = 0.", "phase": "substitute", "answer": -1},
  {"pre": "From 5x " + MINUS + " 9 = 0, the other root is x = ", "say": "Then \\(5x = 9\\).", "post": "",
   "hint": "9 divided by 5 is 1.8.", "answer": 1.8},
  {"pre": "At x = 1.8: y = ", "say": "Each x gets its y from \\(y = 2x - 1\\).", "post": "",
   "hint": "2 times 1.8 is 3.6, minus 1.", "answer": 2.6},
  {"pre": "At x = " + MINUS + "1: y = ", "post": "", "hint": "2 times negative 1, minus 1.", "answer": -3},
  {"pre": "Check (1.8, 2.6) in the circle: 1.8" + SUP2 + " + 2.6" + SUP2 + " = ",
   "done": "It equals 10, so (1.8, 2.6) is right and (" + MINUS + "1, " + MINUS + "3) checks the same way.",
   "post": "", "hint": "3.24 + 6.76.", "answer": 10},
]
s2_misc = [
  {"pattern": "factor_sign_flip", "expect": [-1.8, 1], "note": "sign-flipped factorisation of 5x^2-4x-9",
   "message": "\\(5x^2 - 4x - 9 = 0\\) factorises as \\((5x - 9)(x + 1) = 0\\), giving \\(x = 1.8\\) and \\(x = -1\\). Reversing the signs gives \\(x = -1.8\\) and \\(x = 1\\), which do not satisfy the circle."},
  m_sqbr("(2x - 1)^2", "4x^2 - 4x + 1", "middle term 4x"),
]

# S3 manual (xy)
s3_gs = [
  {"pre": "Take 10 across so the equation is x² + 3x " + MINUS + " ", "post": " = 0",
   "say": "Substitute \\(y = x + 3\\) into \\(xy = 10\\): \\(x(x + 3) = 10\\), which expands to \\(x^2 + 3x = 10\\).",
   "hint": "Move 10 to the left so the equation equals zero.", "answer": 10},
  {"pre": "First root, x = ", "say": "So \\(x^2 + 3x - 10 = 0\\). Two numbers multiply to " + MINUS + "10 and add to 3: they are 5 and " + MINUS + "2, giving \\((x + 5)(x - 2) = 0\\).",
   "post": "", "hint": "Set x " + MINUS + " 2 = 0.", "phase": "substitute", "answer": 2},
  {"pre": "Second root, x = ", "post": "", "hint": "Set x + 5 = 0.", "answer": -5},
  {"pre": "At x = 2: y = ", "say": "Each x gets its y from \\(y = x + 3\\).", "post": "", "hint": "2 + 3.", "answer": 5},
  {"pre": "At x = " + MINUS + "5: y = ", "post": "", "hint": "Negative 5, plus 3.", "answer": -2},
  {"pre": "Check by multiplying: 2 " + TIMES + " 5 = ", "done": "It equals 10, so (2, 5) satisfies xy = 10, and (" + MINUS + "5, " + MINUS + "2) checks the same way since (" + MINUS + "5)(" + MINUS + "2) = 10.",
   "post": "", "hint": "2 times 5.", "answer": 10},
]
s3_misc = [m_flip("x^2 + 3x - 10", 2, -5, [5, -2])]

# S4 manual (x^2 + xy)
s4_gs = [
  {"pre": "Expanding x(4 " + MINUS + " 2x) gives 4x " + MINUS + " 2x². Add the x²: 1 " + MINUS + " 2 = ", "post": "x²",
   "say": "Substitute \\(y = 4 - 2x\\) into \\(x^2 + xy = 3\\): \\(x^2 + x(4 - 2x) = 3\\). Expand the bracket: \\(x^2 + 4x - 2x^2 = 3\\).",
   "hint": "One x² minus two x².", "answer": -1},
  {"pre": "Multiplying " + MINUS + "x² + 4x = 3 by " + MINUS + "1, the x-term becomes ", "post": "x",
   "say": "So \\(-x^2 + 4x = 3\\). Multiply through by " + MINUS + "1 so \\(x^2\\) is positive.",
   "hint": "4x times negative 1 is negative 4x.", "answer": -4},
  {"pre": "and moving the constant across, the equation is x² " + MINUS + " 4x + ", "post": " = 0",
   "say": "That gives \\(x^2 - 4x = -3\\).", "hint": "Take " + MINUS + "3 across to become +3.", "answer": 3},
  {"pre": "First root, x = ", "say": "\\(x^2 - 4x + 3 = 0\\) factorises as \\((x - 1)(x - 3) = 0\\).",
   "post": "", "hint": "Set x " + MINUS + " 1 = 0.", "phase": "substitute", "answer": 1},
  {"pre": "Second root, x = ", "post": "", "hint": "Set x " + MINUS + " 3 = 0.", "answer": 3},
  {"pre": "At x = 1: y = ", "say": "Each x gets its y from \\(y = 4 - 2x\\).", "post": "", "hint": "4 minus 2.", "answer": 2},
  {"pre": "At x = 3: y = ", "post": "", "hint": "4 minus 6.", "answer": -2},
  {"pre": "Check (1, 2): x² + xy = 1 + 1" + TIMES + "2 = ", "done": "It equals 3, so (1, 2) is right and (3, " + MINUS + "2) checks the same way.",
   "post": "", "hint": "1 + 2.", "answer": 3},
]
s4_misc = [m_flip("x^2 - 4x + 3", 1, 3, [-1, -3])]

# S5 set-equal (divide_by_x)
s5 = setP("Solve \\(y = x + 1\\) and \\(y = x^2 - 3x + 1\\). Give the two x-values.",
          "x + 1", "x^2 - 3x + 1", 1,1,-3,1, 0,4, "y = x + 1",
          lambda q,r1,r2:[m_divx(4)])

silver = [
  cP("Solve \\(x + y = 5\\) and \\(x^2 + y^2 = 13\\). Give the two x-values.",
     "x + y = 5", "5 - x", 13, -1, 5, 2, 3, "x^2 + y^2 = 13",
     ("2 " + TIMES + " 5 " + TIMES + " (" + MINUS + "1)", "2 times 5 is 10, and it is negative."),
     "25 - 10x + x^2", ("(5 - x)^2", "25 - 10x + x^2", "middle term 10x"), [-2, -3]),
  P(circle_disp("clS2", 10, lambda x: 2*x-1, [1.8,-1], "x²+y²=10", "y=2x" + MINUS + "1",
      "Circle x squared plus y squared equals 10 and the line y equals 2x minus 1 crossing at two points",
      "Solve \\(y = 2x - 1\\) and \\(x^2 + y^2 = 10\\). Give the two x-values."),
    [1.8, -1], s2_gs, s2_misc, CIR_HINT),
  P("Solve \\(y = x + 3\\) and \\(xy = 10\\). Give the two x-values.", [2, -5], s3_gs, s3_misc,
    "Rearrange the line, substitute into xy = 10, and solve the quadratic."),
  P("Solve \\(y = 4 - 2x\\) and \\(x^2 + xy = 3\\). Give the two x-values.", [1, 3], s4_gs, s4_misc,
    "Substitute the line into the second equation, simplify to a quadratic, and factorise."),
  s5,
  cP("Solve \\(x - y = 2\\) and \\(x^2 + y^2 = 20\\). Give the two x-values.",
     "x - y = 2", "x - 2", 20, 1, -2, 4, -2, "x^2 + y^2 = 20",
     ("2 " + TIMES + " x " + TIMES + " (" + MINUS + "2)", "2 times 2 is 4, and it is negative."),
     "x^2 - 4x + 4", ("(x - 2)^2", "x^2 - 4x + 4", "middle term 4x"), [-4, 2]),
  # S7 manual (symmetric)
  P(circle_disp("clS7", 20, lambda x: 2*x, [2,-2], "x²+y²=20", "y=2x",
      "Circle x squared plus y squared equals 20 and the line y equals 2x crossing at two points",
      "Solve \\(y = 2x\\) and \\(x^2 + y^2 = 20\\). Give the two x-values."),
    [2, -2], [
      {"pre": "Squaring 2x gives 4x². Collect x² terms: 1 + 4 = ", "post": "x²",
       "say": "Substitute \\(y = 2x\\) into \\(x^2 + y^2 = 20\\): \\(x^2 + (2x)^2 = 20\\), and \\((2x)^2 = 4x^2\\).",
       "hint": "One x² plus four x².", "answer": 5},
      {"pre": "So 5x² = 20. Then x² = ", "post": "", "say": "There is no x-term this time, so just divide by 5.",
       "hint": "20 divided by 5.", "answer": 4},
      {"pre": "Positive root, x = ", "say": "\\(x^2 = 4\\) has two roots, one positive and one negative.",
       "post": "", "hint": "The square root of 4.", "phase": "substitute", "answer": 2},
      {"pre": "Negative root, x = ", "post": "", "hint": "The negative square root of 4.", "answer": -2},
      {"pre": "At x = 2: y = ", "say": "Each x gets its y from \\(y = 2x\\).", "post": "", "hint": "2 times 2.", "answer": 4},
      {"pre": "At x = " + MINUS + "2: y = ", "post": "", "hint": "2 times negative 2.", "answer": -4},
      {"pre": "Check (2, 4) in the circle: 2" + SUP2 + " + 4" + SUP2 + " = ",
       "done": "It equals 20, so (2, 4) is right and (" + MINUS + "2, " + MINUS + "4) checks the same way.",
       "post": "", "hint": "4 + 16.", "answer": 20},
    ], [m_posroot(4)], CIR_HINT),
]

# ---- GOLD ----
# G2 manual (leading-coeff circle, divide by 2 then factor)
g2_gs = [
  {"pre": "The middle term, 2 " + TIMES + " 3x " + TIMES + " (" + MINUS + "1), is ", "post": "x",
   "say": "Substitute \\(y = 3x - 1\\) into the circle \\(x^2 + y^2 = 5\\): \\(x^2 + (3x - 1)^2 = 5\\). Expand \\((3x - 1)^2 = 9x^2 - 6x + 1\\).",
   "hint": "2 times 3 times 1 is 6, and it is negative.", "answer": -6},
  {"pre": "Collect the x² terms: 1 + 9 = ", "post": "x²", "say": "So \\(x^2 + 9x^2 - 6x + 1 = 5\\).",
   "hint": "One x² plus nine x².", "answer": 10},
  {"pre": "The constant, 1 " + MINUS + " 5, becomes ", "post": "", "say": "That gives \\(10x^2 - 6x + 1 = 5\\). Take 5 across.",
   "hint": "1 minus 5 is negative 4.", "answer": -4},
  {"pre": "First root, x = ", "say": "So \\(10x^2 - 6x - 4 = 0\\). Divide every term by 2 to get \\(5x^2 - 3x - 2 = 0\\), which factorises as \\((5x + 2)(x - 1) = 0\\).",
   "post": "", "hint": "Set x " + MINUS + " 1 = 0.", "phase": "substitute", "answer": 1},
  {"pre": "From 5x + 2 = 0, the second root is x = ", "say": "Then \\(5x = -2\\).", "post": "",
   "hint": "Negative 2 divided by 5 is negative 0.4.", "answer": -0.4},
  {"pre": "At x = 1: y = ", "say": "Each x gets its y from \\(y = 3x - 1\\).", "post": "", "hint": "3 times 1, minus 1.", "answer": 2},
  {"pre": "At x = " + MINUS + "0.4: y = ", "post": "", "hint": "3 times negative 0.4 is negative 1.2, minus 1.", "answer": -2.2},
  {"pre": "Check (1, 2) in the circle: 1" + SUP2 + " + 2" + SUP2 + " = ",
   "done": "It equals 5, so (1, 2) is right and (" + MINUS + "0.4, " + MINUS + "2.2) checks the same way.",
   "post": "", "hint": "1 + 4.", "answer": 5},
]
g2_misc = [
  {"pattern": "factor_sign_flip", "expect": [0.4, -1], "note": "sign-flipped factorisation of 5x^2-3x-2",
   "message": "\\(5x^2 - 3x - 2 = 0\\) factorises as \\((5x + 2)(x - 1) = 0\\), giving \\(x = 1\\) and \\(x = -0.4\\). Reversing the signs gives \\(x = 0.4\\) and \\(x = -1\\), which do not satisfy the circle."},
  m_sqbr("(3x - 1)^2", "9x^2 - 6x + 1", "middle term 6x"),
]

# G4 manual (xy, leading-coeff 2)
g4_gs = [
  {"pre": "Expanding x(5 " + MINUS + " 2x) gives 5x " + MINUS + " 2x². Bring 2 across so 2x² is positive: 2x² " + MINUS + " 5x + ", "post": " = 0",
   "say": "Rearrange the line \\(2x + y = 5\\) to \\(y = 5 - 2x\\). Substitute into \\(xy = 2\\): \\(x(5 - 2x) = 2\\), which expands to \\(5x - 2x^2 = 2\\).",
   "hint": "Move everything to the side where 2x² is positive; the constant is +2.", "answer": 2},
  {"pre": "First root, x = ", "say": "So \\(2x^2 - 5x + 2 = 0\\). This factorises as \\((2x - 1)(x - 2) = 0\\).",
   "post": "", "hint": "Set x " + MINUS + " 2 = 0.", "phase": "substitute", "answer": 2},
  {"pre": "From 2x " + MINUS + " 1 = 0, the second root is x = ", "say": "Then \\(2x = 1\\).", "post": "",
   "hint": "1 divided by 2.", "answer": 0.5},
  {"pre": "At x = 2: y = ", "say": "Each x gets its y from \\(y = 5 - 2x\\).", "post": "", "hint": "5 minus 4.", "answer": 1},
  {"pre": "At x = 0.5: y = ", "post": "", "hint": "5 minus 1.", "answer": 4},
  {"pre": "Check by multiplying: 2 " + TIMES + " 1 = ", "done": "It equals 2, so (2, 1) satisfies xy = 2, and (0.5, 4) checks the same way since 0.5 " + TIMES + " 4 = 2.",
   "post": "", "hint": "2 times 1.", "answer": 2},
]
g4_misc = [
  {"pattern": "factor_sign_flip", "expect": [-0.5, -2], "note": "sign-flipped factorisation of 2x^2-5x+2",
   "message": "\\(2x^2 - 5x + 2 = 0\\) factorises as \\((2x - 1)(x - 2) = 0\\), giving \\(x = 0.5\\) and \\(x = 2\\). Reversing the signs gives \\(x = -0.5\\) and \\(x = -2\\), which do not satisfy the equations."},
]

# G5 manual (x^2 + xy)
g5_gs = [
  {"pre": "Expanding x(5 " + MINUS + " 2x) gives 5x " + MINUS + " 2x². Add the x²: 1 " + MINUS + " 2 = ", "post": "x²",
   "say": "Substitute \\(y = 5 - 2x\\) into \\(x^2 + xy = 6\\): \\(x^2 + x(5 - 2x) = 6\\). Expand the bracket: \\(x^2 + 5x - 2x^2 = 6\\).",
   "hint": "One x² minus two x².", "answer": -1},
  {"pre": "Multiplying " + MINUS + "x² + 5x = 6 by " + MINUS + "1, the x-term becomes ", "post": "x",
   "say": "So \\(-x^2 + 5x = 6\\). Multiply through by " + MINUS + "1 so \\(x^2\\) is positive.",
   "hint": "5x times negative 1 is negative 5x.", "answer": -5},
  {"pre": "and moving the constant across, the equation is x² " + MINUS + " 5x + ", "post": " = 0",
   "say": "That gives \\(x^2 - 5x = -6\\).", "hint": "Take " + MINUS + "6 across to become +6.", "answer": 6},
  {"pre": "First root, x = ", "say": "\\(x^2 - 5x + 6 = 0\\) factorises as \\((x - 2)(x - 3) = 0\\).",
   "post": "", "hint": "Set x " + MINUS + " 2 = 0.", "phase": "substitute", "answer": 2},
  {"pre": "Second root, x = ", "post": "", "hint": "Set x " + MINUS + " 3 = 0.", "answer": 3},
  {"pre": "At x = 2: y = ", "say": "Each x gets its y from \\(y = 5 - 2x\\).", "post": "", "hint": "5 minus 4.", "answer": 1},
  {"pre": "At x = 3: y = ", "post": "", "hint": "5 minus 6.", "answer": -1},
  {"pre": "Check (2, 1): x² + xy = 4 + 2" + TIMES + "1 = ", "done": "It equals 6, so (2, 1) is right and (3, " + MINUS + "1) checks the same way.",
   "post": "", "hint": "4 + 2.", "answer": 6},
]
g5_misc = [m_flip("x^2 - 5x + 6", 2, 3, [-2, -3])]

gold = [
  cP("Solve \\(x + y = 1\\) and \\(x^2 + y^2 = 13\\). Give the two x-values.",
     "x + y = 1", "1 - x", 13, -1, 1, 3, -2, "x^2 + y^2 = 13",
     ("2 " + TIMES + " 1 " + TIMES + " (" + MINUS + "1)", "2 times 1 is 2, and it is negative."),
     "1 - 2x + x^2", ("(1 - x)^2", "1 - 2x + x^2", "middle term 2x"), [-3, 2]),
  P(circle_disp("clG2", 5, lambda x: 3*x-1, [1,-0.4], "x²+y²=5", "y=3x" + MINUS + "1",
      "Circle x squared plus y squared equals 5 and the line y equals 3x minus 1 crossing at two points",
      "Solve \\(y = 3x - 1\\) and \\(x^2 + y^2 = 5\\). Give the two x-values."),
    [1, -0.4], g2_gs, g2_misc, CIR_HINT),
  cP("Solve \\(x + y = 5\\) and \\(x^2 + y^2 = 17\\). Give the two x-values.",
     "x + y = 5", "5 - x", 17, -1, 5, 1, 4, "x^2 + y^2 = 17",
     ("2 " + TIMES + " 5 " + TIMES + " (" + MINUS + "1)", "2 times 5 is 10, and it is negative."),
     "25 - 10x + x^2", ("(5 - x)^2", "25 - 10x + x^2", "middle term 10x"), [-1, -4]),
  P("Solve \\(2x + y = 5\\) and \\(xy = 2\\). Give the two x-values.", [2, 0.5], g4_gs, g4_misc,
    "Rearrange the line, substitute into xy = 2, and solve the quadratic."),
  P("Solve \\(y = 5 - 2x\\) and \\(x^2 + xy = 6\\). Give the two x-values.", [2, 3], g5_gs, g5_misc,
    "Substitute the line into the second equation, simplify to a quadratic, and factorise."),
]

# add SVG to the two monic circles in silver/gold that used cP (they have no svg yet)
# cP builds display WITHOUT svg; attach here for S1,S6,G1,G3
svg_map = [
  (silver, 0, "clS1", 13, lambda x:5-x, [2,3], "x²+y²=13", "x+y=5",
   "Circle x squared plus y squared equals 13 and the line x plus y equals 5 crossing at two points"),
  (silver, 5, "clS6", 20, lambda x:x-2, [4,-2], "x²+y²=20", "x" + MINUS + "y=2",
   "Circle x squared plus y squared equals 20 and the line x minus y equals 2 crossing at two points"),
  (gold, 0, "clG1", 13, lambda x:1-x, [3,-2], "x²+y²=13", "x+y=1",
   "Circle x squared plus y squared equals 13 and the line x plus y equals 1 crossing at two points"),
  (gold, 2, "clG3", 17, lambda x:5-x, [1,4], "x²+y²=17", "x+y=5",
   "Circle x squared plus y squared equals 17 and the line x plus y equals 5 crossing at two points"),
]
for arr, idx, cid, R, fn, sols, clbl, llbl, aria in svg_map:
    p = arr[idx]
    assert "<svg" not in p["display"]
    p["display"] = build_svg(cid, R, fn, sols, clbl, llbl, aria) + CAP + p["display"]

problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Both equations are y = …; simple substitution and easy factorising",
  "silver_description": "Rearrange the line (or xy) after substituting, then factorise with care",
  "gold_description": "Circles \\(x^2 + y^2\\), or a quadratic with a leading coefficient",
}

def desanitize(o):
    if isinstance(o, dict): return {k: desanitize(v) for k, v in o.items()}
    if isinstance(o, list): return [desanitize(v) for v in o]
    if isinstance(o, str): return o.replace(" — ", ": ").replace("—", ":")
    return o

pd = {
  "guided": guided,
  "method_card": method_card,
  "tier_guides": tier_guides,
  "topic_links": orig.get("topic_links", {"prerequisites": []}),
  "problem_bank": problem_bank,
  "related_videos": orig.get("related_videos", []),
  "worked_examples": desanitize(orig.get("worked_examples", [])),
}

# ---- verification: every pair satisfies both equations ----
def verify():
    checks = {
      # tier,index : (eq1(x,y), eq2(x,y)) as booleans via lambdas, sols, line y(x)
    }
    def chk(name, sols, ly, eqs):
        for x in sols:
            y = ly(x)
            for e in eqs:
                assert abs(e(x, y)) < 1e-9, (name, x, y, e(x,y))
    # bronze
    chk("B1", [4,-1], lambda x:x+1, [lambda x,y:y-(x+1), lambda x,y:y-(x*x-2*x-3)])
    chk("B2", [1,2], lambda x:3*x, [lambda x,y:y-3*x, lambda x,y:y-(x*x+2)])
    chk("B3", [2,-1], lambda x:x+2, [lambda x,y:y-(x+2), lambda x,y:y-x*x])
    chk("B4", [3,-1], lambda x:2*x, [lambda x,y:y-2*x, lambda x,y:y-(x*x-3)])
    chk("B5", [1,-3], lambda x:x+5, [lambda x,y:y-(x+5), lambda x,y:y-(x*x+3*x+2)])
    chk("B6", [0,2], lambda x:2*x+3, [lambda x,y:y-(2*x+3), lambda x,y:y-(x*x+3)])
    chk("B7", [2,3], lambda x:x-1, [lambda x,y:y-(x-1), lambda x,y:y-(x*x-4*x+5)])
    chk("B8", [2,-3], lambda x:4-x, [lambda x,y:y-(4-x), lambda x,y:y-(x*x-2)])
    chk("S1", [2,3], lambda x:5-x, [lambda x,y:x+y-5, lambda x,y:x*x+y*y-13])
    chk("S2", [1.8,-1], lambda x:2*x-1, [lambda x,y:y-(2*x-1), lambda x,y:x*x+y*y-10])
    chk("S3", [2,-5], lambda x:x+3, [lambda x,y:y-(x+3), lambda x,y:x*y-10])
    chk("S4", [1,3], lambda x:4-2*x, [lambda x,y:y-(4-2*x), lambda x,y:x*x+x*y-3])
    chk("S5", [0,4], lambda x:x+1, [lambda x,y:y-(x+1), lambda x,y:y-(x*x-3*x+1)])
    chk("S6", [4,-2], lambda x:x-2, [lambda x,y:x-y-2, lambda x,y:x*x+y*y-20])
    chk("S7", [2,-2], lambda x:2*x, [lambda x,y:y-2*x, lambda x,y:x*x+y*y-20])
    chk("G1", [3,-2], lambda x:1-x, [lambda x,y:x+y-1, lambda x,y:x*x+y*y-13])
    chk("G2", [1,-0.4], lambda x:3*x-1, [lambda x,y:y-(3*x-1), lambda x,y:x*x+y*y-5])
    chk("G3", [1,4], lambda x:5-x, [lambda x,y:x+y-5, lambda x,y:x*x+y*y-17])
    chk("G4", [2,0.5], lambda x:5-2*x, [lambda x,y:2*x+y-5, lambda x,y:x*y-2])
    chk("G5", [2,3], lambda x:5-2*x, [lambda x,y:y-(5-2*x), lambda x,y:x*x+x*y-6])
    print("all pairs satisfy both equations")
verify()

# final root boxes land on solutions; last box before check is second root
def final_root_check():
    for tier in ("bronze","silver","gold"):
        for i,p in enumerate(problem_bank[tier]):
            gs = p["guided_steps"]
            root_boxes = [s["answer"] for s in gs if s.get("phase")=="substitute" or (isinstance(s.get("answer"),(int,float)) )]
            # locate substitute index
            sub = next(j for j,s in enumerate(gs) if s.get("phase")=="substitute")
            first = gs[sub]["answer"]
            second = gs[sub+1]["answer"]
            sset = set(p["solutions"])
            assert set([first,second])==sset, (tier,i,first,second,p["solutions"])
    print("root boxes match solutions")
final_root_check()

# em dash scan
def emscan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            emscan(v,path+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): emscan(v,path+"[%d]"%i)
    elif isinstance(o,str) and "—" in o:
        raise SystemExit("EM DASH at "+path)
emscan(pd)
print("no em dashes")

json.dump(pd, open("lesson_maths-ocr_algebra-L10.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("written lesson_maths-ocr_algebra-L10.json")
print("helpers loaded")
