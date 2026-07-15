# -*- coding: utf-8 -*-
"""Pilot rebuild of maths-edexcel algebra L09 (Simultaneous Equations, Linear).

Everything is machine-verified before upload:
  1. Both equations of every problem are PARSED FROM THE DISPLAY STRING and
     solved exactly (fractions) - stored solutions must match. This is the
     check whose absence caused the original authoring failure.
  2. Tier structure: bronze = no scaling needed, silver = scale exactly one
     equation, gold = scale both (minimal integer multipliers over x and y).
  3. Solution pairs unique within a tier (duplicate-answer issue).
  4. Every misconception expect: simulated where mechanical (scale-LHS-only /
     RHS-wrong-op-on-subtract error models re-derive the expect from the
     equations), and always asserted != the correct solution.

Run with --push to PATCH Supabase (requires SUPABASE_SERVICE_KEY).
"""
import json, io, os, re, sys, urllib.request
from fractions import Fraction as F

sys.stdout.reconfigure(errors="replace")
PUSH = "--push" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"

# ============================== THE BANK ==============================
# (display, [x, y], hint, misconceptions)
# misconception: pattern / message / note / expect / optional _sim spec that
# re-derives expect: scale=(k1,k2), lhs_only=1|2 (that eq's RHS not scaled),
# op='sub'|'add', rhs_wrong=True (RHS added when subtracting), subst=1|2.

BRONZE = [
 (r"Solve \(x + y = 8\) and \(x - y = 2\)", [5, 3],
  "The y terms are +y and −y — opposite signs, so ADD the equations.",
  []),
 (r"Solve \(2x + y = 9\) and \(x + y = 5\)", [4, 1],
  "Both equations have +y — same sign, so subtract one from the other.",
  [dict(pattern="rhs_not_subtracted", expect=[14, -9],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="When you subtract the equations, the right-hand sides subtract too: \\(9 - 5 = 4\\), so \\(x = 4\\). Adding them instead gives 14, which is too big to fit either equation — always do the same thing to both sides.")],
 ),
 (r"Solve \(3x + y = 11\) and \(x + y = 5\)", [3, 2],
  "Both equations have +y — subtract to make the y terms vanish.",
  [dict(pattern="rhs_not_subtracted", expect=[8, -3],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtracting the left-hand sides means subtracting the right-hand sides as well: \\(11 - 5 = 6\\), so \\(2x = 6\\) and \\(x = 3\\). It looks like the right-hand sides were added instead.")],
 ),
 (r"Solve \(x + 2y = 10\) and \(x + y = 7\)", [4, 3],
  "The x terms already match — subtract to remove them.",
  [dict(pattern="rhs_not_subtracted", expect=[-10, 17],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtracting the equations removes x and leaves \\(y = 10 - 7 = 3\\). It looks like the right-hand sides were added (giving 17) instead of subtracted — both sides get the same treatment.")],
 ),
 (r"Solve \(2x + y = 10\) and \(2x - y = 6\)", [4, 2],
  "Opposite signs on y — adding the equations makes y disappear.",
  [dict(pattern="rhs_wrong_operation", expect=[1, 8],
        _sim=dict(op="sub", rhs_wrong=True, subst=1),
        message="Whichever route you take, the right-hand sides must get the same operation as the left. Adding: \\(4x = 16\\) so \\(x = 4\\). Subtracting: \\(2y = 4\\) so \\(y = 2\\). Mixing the two up leads to \\(x = 1, y = 8\\), which doesn't fit either equation.")],
 ),
 (r"Solve \(3x + y = 17\) and \(x + y = 7\)", [5, 2],
  "Both equations have +y — subtract them.",
  [dict(pattern="rhs_not_subtracted", expect=[12, -5],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtract the right-hand sides too: \\(17 - 7 = 10\\), so \\(2x = 10\\) and \\(x = 5\\). Adding them gives 24 and everything after that comes out wrong.")],
 ),
 (r"Solve \(x + 3y = 14\) and \(x + y = 6\)", [2, 4],
  "The x terms match — subtract to leave just y terms.",
  [dict(pattern="rhs_not_subtracted", expect=[-4, 10],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="After subtracting, \\(2y = 14 - 6 = 8\\), so \\(y = 4\\). It looks like the right-hand sides were added — they must be subtracted, exactly like the left-hand sides.")],
 ),
 (r"Solve \(4x + y = 13\) and \(2x + y = 7\)", [3, 1],
  "Same sign on y in both — subtract.",
  [dict(pattern="rhs_not_subtracted", expect=[10, -13],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtracting gives \\(2x = 13 - 7 = 6\\), so \\(x = 3\\). Adding the right-hand sides (20) instead of subtracting sends the whole answer off course.")],
 ),
]

SILVER = [
 (r"Solve \(3x + 2y = 19\) and \(x + y = 8\)", [3, 5],
  "Multiply the second equation by 2, then subtract.",
  [dict(pattern="scaled_lhs_only", expect=[11, -3],
        _sim=dict(scale=(1, 2), lhs_only=2, op="sub", subst=2),
        message="When you multiply an equation, multiply BOTH sides. \\(x + y = 8\\) doubled is \\(2x + 2y = 16\\) — the 8 doubles too. Leaving it as 8 makes every later step wrong."),
   dict(pattern="rhs_not_subtracted", expect=[35, -27],
        _sim=dict(scale=(1, 2), op="sub", rhs_wrong=True, subst=2),
        message="After doubling the second equation the right-hand sides are 19 and 16, and subtracting gives \\(x = 3\\). It looks like they were added (35) instead of subtracted.")],
 ),
 (r"Solve \(2x + 5y = 21\) and \(x + 2y = 8\)", [-2, 5],
  "Multiply the second equation by 2 so both have 2x. Watch out — x comes out negative.",
  [dict(pattern="scaled_lhs_only", expect=[-18, 13],
        _sim=dict(scale=(1, 2), lhs_only=2, op="sub", subst=2),
        message="Doubling \\(x + 2y = 8\\) gives \\(2x + 4y = 16\\) — the right-hand side doubles as well. Keeping it at 8 gives \\(y = 13\\), which is too big to fit either equation."),
   dict(pattern="rhs_not_subtracted", expect=[-66, 37],
        _sim=dict(scale=(1, 2), op="sub", rhs_wrong=True, subst=2),
        message="Subtract the right-hand sides: \\(21 - 16 = 5\\), so \\(y = 5\\). Adding them (37) instead of subtracting is the slip here.")],
 ),
 (r"Solve \(4x + y = 14\) and \(2x + 3y = 12\)", [3, 2],
  "Multiply the first equation by 3 so both have 3y.",
  [dict(pattern="scaled_lhs_only", expect=[0.2, 13.2],
        _sim=dict(scale=(3, 1), lhs_only=1, op="sub", subst=1),
        message="Multiplying \\(4x + y = 14\\) by 3 gives \\(12x + 3y = 42\\) — the 14 gets multiplied too. If the right-hand side stays at 14 you end up with decimals that don't fit the equations."),
   dict(pattern="rhs_not_subtracted", expect=[5.4, -7.6],
        _sim=dict(scale=(3, 1), op="sub", rhs_wrong=True, subst=1),
        message="After scaling, subtract the right-hand sides: \\(42 - 12 = 30\\), so \\(10x = 30\\) and \\(x = 3\\). Adding them (54) is the slip — both sides get subtracted.")],
 ),
 (r"Solve \(5x - y = 5\) and \(2x + 3y = 19\)", [2, 5],
  "Multiply the first equation by 3. The y terms then have opposite signs — so add.",
  [dict(pattern="substitute_sign_slip", expect=[2, -5],
        message="\\(x = 2\\) is right. Substituting into \\(5x - y = 5\\) gives \\(10 - y = 5\\), so \\(y = 5\\) — positive. Getting \\(-5\\) means the sign flipped once too often when moving terms across.",
        note="From 10 - y = 5: -y = -5 so y = 5; the slip keeps y = -5.")],
 ),
 (r"Solve \(x + 4y = 17\) and \(3x + 2y = 11\)", [1, 4],
  "Multiply the second equation by 2 so both have 4y.",
  [dict(pattern="scaled_lhs_only", expect=[-1.2, 4.55],
        _sim=dict(scale=(1, 2), lhs_only=2, op="sub", subst=1),
        message="Doubling \\(3x + 2y = 11\\) gives \\(6x + 4y = 22\\) — the 11 doubles too. Leaving it at 11 makes x come out negative when it shouldn't."),
   dict(pattern="rhs_not_subtracted", expect=[7.8, 2.3],
        _sim=dict(scale=(1, 2), op="sub", rhs_wrong=True, subst=1),
        message="Subtracting the right-hand sides gives \\(22 - 17 = 5\\), so \\(5x = 5\\) and \\(x = 1\\). Adding them (39) instead is the slip here.")],
 ),
 (r"Solve \(3x + y = 13\) and \(2x + 3y = 18\)", [3, 4],
  "Multiply the first equation by 3 so both have 3y.",
  [dict(pattern="substitute_sign_slip", expect=[3, 22],
        message="\\(x = 3\\) is right. Substituting into \\(3x + y = 13\\) gives \\(9 + y = 13\\), so \\(y = 4\\). Getting 22 means the 9 was added to 13 instead of subtracted — moving a term across the equals sign changes its sign.",
        note="Slip: y = 13 + 9 = 22 instead of 13 - 9 = 4.")],
 ),
 (r"Solve \(2x - 3y = 6\) and \(x + y = 8\)", [6, 2],
  "Multiply the second equation by 3. Opposite signs on the y terms — add.",
  [dict(pattern="scaled_lhs_only", expect=[2.8, 5.2],
        _sim=dict(scale=(1, 3), lhs_only=2, op="add", subst=2),
        message="Multiplying \\(x + y = 8\\) by 3 gives \\(3x + 3y = 24\\) — the 8 is multiplied too. Keeping it at 8 gives decimal answers, and this question has whole-number ones.")],
 ),
]

GOLD = [
 (r"Solve \(3x + 4y = 25\) and \(2x + 3y = 18\)", [3, 4],
  "No single multiplication works here — scale BOTH equations (try ×3 and ×4, or ×2 and ×3).",
  [dict(pattern="rhs_not_subtracted", expect=[147, -104],
        _sim=dict(scale=(3, 4), op="sub", rhs_wrong=True, subst=1),
        message="After scaling by 3 and 4 the right-hand sides are 75 and 72. Subtract them: \\(x = 75 - 72 = 3\\). Adding them (147) is the slip — the right-hand sides get subtracted just like the left."),
   dict(pattern="scaled_lhs_only", expect=[57, -36.5],
        _sim=dict(scale=(3, 4), lhs_only=2, op="sub", subst=1),
        message="Both equations must be multiplied on BOTH sides. Scaling \\(2x + 3y = 18\\) by 4 gives \\(8x + 12y = 72\\) — if the 18 is left unscaled, x comes out as 57, which fits neither equation.")],
 ),
 (r"Solve \(5x + 3y = 29\) and \(3x + 4y = 24\)", [4, 3],
  "Scale both equations — ×4 and ×3 makes both y terms 12y.",
  []),
 (r"Solve \(2x + 3y = 4\) and \(5x + 2y = -1\)", [-1, 2],
  "Scale both (×2 and ×3 makes both 6y). Negative numbers appear — keep signs on a tight leash.",
  []),
 (r"Solve \(7x + 2y = 27\) and \(3x + 5y = 24\)", [3, 3],
  "Scale both equations — ×5 and ×2 makes both y terms 10y.",
  [dict(pattern="substitute_sign_slip", expect=[3, 24],
        message="\\(x = 3\\) is right. Substituting into \\(7x + 2y = 27\\) gives \\(21 + 2y = 27\\), so \\(2y = 6\\) and \\(y = 3\\). Getting 24 means the 21 was added instead of subtracted when moving it across.",
        note="Slip: 2y = 27 + 21 = 48, y = 24.")],
 ),
 (r"Solve \(5x - 3y = 1\) and \(2x + 7y = 25\)", [2, 3],
  "Scale both (×7 and ×3 makes the y terms −21y and +21y) — opposite signs, so add.",
  [dict(pattern="substitute_sign_slip", expect=[2, -3],
        message="\\(x = 2\\) is right. Substituting into \\(5x - 3y = 1\\) gives \\(10 - 3y = 1\\), so \\(3y = 9\\) and \\(y = 3\\) — positive. Getting \\(-3\\) means a sign flipped once too often on the way.",
        note="From 10 - 3y = 1: -3y = -9 so y = 3; the slip keeps y = -3.")],
 ),
]

TIER_DESCRIPTIONS = {
 "bronze_description": "The numbers in front already match — add or subtract once and a letter vanishes",
 "silver_description": "Multiply one equation first to make a matching pair",
 "gold_description": "Multiply both equations — or switch to the substitution method",
}

METHOD_CARD = {
 "title": "How to Solve Simultaneous Equations (Linear)",
 "steps": [
  "Number the equations (1) and (2). You are hunting for the one pair of values — an x AND a y — that makes both equations true at the same time.",
  "Get a matching pair: the same number in front of x in both equations, or the same in front of y. If nothing matches yet, multiply one equation all the way through — every term, both sides of the equals sign. (Hardest questions: multiply both equations.)",
  "Same signs? SUBTRACT one equation from the other. Opposite signs (one +, one −)? ADD them. Either way the matched letter cancels out and you're left with an easy one-letter equation.",
  "Solve it, then put that value back into the easier original equation to find the other letter. Finally, check your pair works in BOTH original equations.",
 ],
 "content": "<p><strong>Simultaneous equations</strong> are two equations sharing the same two unknowns, usually \\(x\\) and \\(y\\). On their own, each equation has lots of possible answers — together, there is exactly <em>one</em> pair of values that fits both. Your job is to find it.</p><p><strong>The big idea:</strong> you can't solve one equation with two letters in it — so make one letter disappear. If both equations contain the same amount of \\(y\\) (say \\(3y\\) and \\(3y\\)), subtracting one equation from the other wipes the \\(y\\) out completely, leaving an ordinary one-letter equation you already know how to solve.</p><p><strong>Remember SSS — Same Signs Subtract.</strong> If the matched terms have the same sign (\\(+3y\\) and \\(+3y\\)), subtract. If the signs are opposite (\\(+3y\\) and \\(-3y\\)), add instead — adding \\(+3y\\) to \\(-3y\\) gives zero, which is exactly what you want.</p><p><strong>When nothing matches yet</strong>, make a match: multiply an equation all the way through — every term <em>and</em> the number after the equals sign. Bronze questions here need no multiplying, silver questions need one equation multiplied, and gold questions need both (for example \\(\\times 2\\) on one and \\(\\times 3\\) on the other to turn \\(3y\\) and \\(2y\\) into \\(6y\\) and \\(6y\\)).</p><p><strong>The substitution method</strong> is the alternative: rearrange one equation into \\(y = \\ldots\\) form and substitute that expression into the other equation. It shines when an equation already starts \\(y =\\) or \\(x =\\). Either method earns full marks — use whichever feels safer.</p><p>Always <strong>check</strong>: put both values back into the equation you didn't substitute into. If it balances, the answer is right — this catches nearly every slip and takes ten seconds.</p>",
 "example": "<p><strong>Solve</strong> \\(2x + y = 7\\) and \\(x + y = 4\\)</p><p><strong>Step 1:</strong> Label them: (1) \\(2x + y = 7\\), (2) \\(x + y = 4\\).</p><p><strong>Step 2:</strong> Look for a match — both equations have exactly \\(+y\\). No multiplying needed.</p><p><strong>Step 3:</strong> Same signs, so subtract: (1) − (2) gives \\(2x - x = 7 - 4\\), so \\(x = 3\\). Notice the right-hand sides were subtracted too.</p><p><strong>Step 4:</strong> Substitute \\(x = 3\\) into (2): \\(3 + y = 4\\), so \\(y = 1\\).</p><p><strong>Check</strong> in (1): \\(2(3) + 1 = 7\\) ✓</p><p><strong>Answer:</strong> \\(x = 3\\), \\(y = 1\\)</p>",
}

WORKED_EXAMPLES = [
 {"difficulty": "Bronze", "question": "Solve 3x + y = 10 and x + y = 4",
  "steps": [
   {"label": "Step 1 — Spot the match", "content": "<p>Both equations contain exactly \\(+y\\) — same sign in both. <strong>Same Signs Subtract.</strong></p>"},
   {"label": "Step 2 — Subtract the equations", "content": "<p>\\((3x + y) - (x + y) = 10 - 4\\) → \\(2x = 6\\) → \\(x = 3\\). The \\(y\\) terms cancel, and the right-hand sides are subtracted too.</p>"},
   {"label": "Step 3 — Substitute back", "content": "<p>Put \\(x = 3\\) into the simpler equation: \\(3 + y = 4\\) → \\(y = 1\\).</p>"},
   {"label": "Step 4 — Check", "content": "<p>In the other equation: \\(3(3) + 1 = 10\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 3\\), \\(y = 1\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Bronze", "question": "Solve 3x + 2y = 17 and 5x − 2y = 7",
  "steps": [
   {"label": "Step 1 — Spot the match", "content": "<p>The \\(y\\) terms are \\(+2y\\) and \\(-2y\\) — same size, <em>opposite</em> signs. Opposite signs means <strong>add</strong>: \\(+2y\\) and \\(-2y\\) make zero.</p>"},
   {"label": "Step 2 — Add the equations", "content": "<p>\\((3x + 2y) + (5x - 2y) = 17 + 7\\) → \\(8x = 24\\) → \\(x = 3\\).</p>"},
   {"label": "Step 3 — Substitute back", "content": "<p>\\(x = 3\\) into the first equation: \\(9 + 2y = 17\\) → \\(2y = 8\\) → \\(y = 4\\).</p>"},
   {"label": "Step 4 — Check", "content": "<p>\\(5(3) - 2(4) = 15 - 8 = 7\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 3\\), \\(y = 4\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Silver", "question": "Solve 2x + 3y = 12 and x + y = 5",
  "steps": [
   {"label": "Step 1 — Nothing matches yet", "content": "<p>\\(2x\\) vs \\(x\\), \\(3y\\) vs \\(y\\) — no matching pair. Multiply the <em>whole</em> second equation by 3: \\(3x + 3y = 15\\). The 5 gets multiplied too — every term, both sides.</p>"},
   {"label": "Step 2 — Subtract", "content": "<p>Now both have \\(3y\\), same sign. \\((3x + 3y) - (2x + 3y) = 15 - 12\\) → \\(x = 3\\).</p>"},
   {"label": "Step 3 — Substitute back", "content": "<p>\\(x = 3\\) into \\(x + y = 5\\): \\(y = 2\\).</p>"},
   {"label": "Step 4 — Check", "content": "<p>\\(2(3) + 3(2) = 6 + 6 = 12\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 3\\), \\(y = 2\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Gold", "question": "Solve 4x + 3y = 23 and 3x + 2y = 16",
  "steps": [
   {"label": "Step 1 — Scale BOTH equations", "content": "<p>No single multiplication makes a match, so make the \\(y\\) terms both \\(6y\\): first equation \\(\\times 2\\) → \\(8x + 6y = 46\\); second \\(\\times 3\\) → \\(9x + 6y = 48\\). Both sides of both equations get scaled.</p>"},
   {"label": "Step 2 — Subtract", "content": "<p>Same signs, so subtract: \\((9x + 6y) - (8x + 6y) = 48 - 46\\) → \\(x = 2\\).</p>"},
   {"label": "Step 3 — Substitute back", "content": "<p>\\(x = 2\\) into \\(3x + 2y = 16\\): \\(6 + 2y = 16\\) → \\(y = 5\\).</p>"},
   {"label": "Step 4 — Check", "content": "<p>\\(4(2) + 3(5) = 8 + 15 = 23\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 2\\), \\(y = 5\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Gold", "question": "Solve 2x + y = 11 and 3x + 2y = 18 (substitution method)",
  "steps": [
   {"label": "Step 1 — Make y the subject", "content": "<p>From the first equation: \\(y = 11 - 2x\\). This is the substitution method — the alternative to elimination, and worth the same marks.</p>"},
   {"label": "Step 2 — Substitute into the other equation", "content": "<p>\\(3x + 2(11 - 2x) = 18\\) → \\(3x + 22 - 4x = 18\\) → \\(-x = -4\\) → \\(x = 4\\).</p>"},
   {"label": "Step 3 — Find y", "content": "<p>\\(y = 11 - 2(4) = 3\\).</p>"},
   {"label": "Step 4 — Check", "content": "<p>\\(3(4) + 2(3) = 12 + 6 = 18\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 4\\), \\(y = 3\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
]

# ============================== VERIFICATION ==============================

def parse_eq(s):
    """'2x + 3y = 4' -> (F(2), F(3), F(4)). Handles implicit 1 and minus."""
    lhs, rhs = s.split("=")
    a = b = F(0)
    for coef, var in re.findall(r"([+-]?\s*\d*)\s*([xy])", lhs):
        coef = coef.replace(" ", "")
        val = F(coef + "1") if coef in ("", "+", "-") else F(coef)
        if var == "x": a += val
        else: b += val
    return a, b, F(rhs.replace(" ", ""))

def parse_display(d):
    eqs = re.findall(r"\\\((.*?)\\\)", d)
    assert len(eqs) == 2, "expected two equations in: " + d
    return parse_eq(eqs[0]), parse_eq(eqs[1])

def solve2(e1, e2):
    (a1, b1, c1), (a2, b2, c2) = e1, e2
    det = a1 * b2 - a2 * b1
    assert det != 0, "singular system"
    return (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det

def tier_of(e1, e2):
    """bronze: match with no scaling; silver: scale exactly one; gold: both."""
    best = None
    for pick in (0, 1):  # match on x or on y
        c1, c2 = abs(e1[pick]), abs(e2[pick])
        if c1 == 0 or c2 == 0: continue
        l = c1 * c2 / F(__import__("math").gcd(c1.numerator, c2.numerator))
        k1, k2 = l / c1, l / c2
        score = (k1 != 1) + (k2 != 1)
        best = score if best is None else min(best, score)
    return ["bronze", "silver", "gold"][best]

def simulate(e1, e2, spec):
    """Re-derive an expect from an error model. Returns (x, y) floats."""
    (a1, b1, c1), (a2, b2, c2) = e1, e2
    k1, k2 = spec.get("scale", (1, 1))
    lo = spec.get("lhs_only")
    A1, B1, C1 = a1 * k1, b1 * k1, c1 * (1 if lo == 1 else k1)
    A2, B2, C2 = a2 * k2, b2 * k2, c2 * (1 if lo == 2 else k2)
    if spec["op"] == "add":
        La, Lb, R = A1 + A2, B1 + B2, C1 + C2
    else:
        La, Lb, R = A1 - A2, B1 - B2, (C1 + C2) if spec.get("rhs_wrong") else (C1 - C2)
        if (La if Lb == 0 else Lb) < 0:  # student subtracts the way that keeps the survivor positive
            La, Lb = -La, -Lb
            R = (C1 + C2) if spec.get("rhs_wrong") else (C2 - C1)
    assert (La == 0) != (Lb == 0), "elimination must remove exactly one letter"
    if Lb == 0:
        x = R / La
        se = (a1, b1, c1) if spec["subst"] == 1 else (a2, b2, c2)
        y = (se[2] - se[0] * x) / se[1]
    else:
        y = R / Lb
        se = (a1, b1, c1) if spec["subst"] == 1 else (a2, b2, c2)
        x = (se[2] - se[1] * y) / se[0]
    return float(x), float(y)

BANK = {"bronze": BRONZE, "silver": SILVER, "gold": GOLD}
problems_out = {}
errors = 0
for tier, rows in BANK.items():
    out = []
    seen_pairs = set()
    for n, (display, sol, hint, miscs) in enumerate(rows):
        tag = "%s%d" % (tier[0].upper(), n)
        e1, e2 = parse_display(display)
        x, y = solve2(e1, e2)
        if [float(x), float(y)] != [float(s) for s in sol]:
            print("FAIL %s: display solves to (%s, %s), declared %s" % (tag, x, y, sol)); errors += 1
        t = tier_of(e1, e2)
        if t != tier:
            print("FAIL %s: structurally %s, placed in %s" % (tag, t, tier)); errors += 1
        if tuple(sol) in seen_pairs:
            print("FAIL %s: duplicate solution pair in tier %s" % (tag, sol)); errors += 1
        seen_pairs.add(tuple(sol))
        clean = []
        for m in miscs:
            exp = m["expect"]
            if "_sim" in m:
                sx, sy = simulate(e1, e2, m["_sim"])
                if abs(sx - exp[0]) > 0.011 or abs(sy - exp[1]) > 0.011:
                    print("FAIL %s %s: sim gives (%.4g, %.4g), expect %s" % (tag, m["pattern"], sx, sy, exp)); errors += 1
            if abs(exp[0] - sol[0]) < 0.011 and abs(exp[1] - sol[1]) < 0.011:
                print("FAIL %s %s: expect equals the correct answer" % (tag, m["pattern"])); errors += 1
            clean.append({"pattern": m["pattern"], "check": m["pattern"], "expect": exp,
                          "message": m["message"], "note": m.get("note", "machine-verified via error simulation")})
        out.append({"display": display, "solutions": sol, "input_type": "xy_pair",
                    "calculator": False, "hint": hint, "misconceptions": clean})
    problems_out[tier] = out

print("bank: %d bronze / %d silver / %d gold, verification %s"
      % (len(problems_out["bronze"]), len(problems_out["silver"]), len(problems_out["gold"]),
         "FAILED (%d)" % errors if errors else "CLEAN"))
if errors:
    sys.exit(1)

# ============================== ASSEMBLE + PUSH ==============================
l09_path = r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad\_l09_live.json"
pd = json.load(io.open(l09_path, encoding="utf-8"))
pd["method_card"] = METHOD_CARD
pd["worked_examples"] = WORKED_EXAMPLES
for k, v in TIER_DESCRIPTIONS.items():
    pd["problem_bank"][k] = v
for tier in ("bronze", "silver", "gold"):
    pd["problem_bank"][tier] = problems_out[tier]

outp = os.path.join(ROOT, "scratchpad", "_maths_audit", "_l09_rebuilt_practice_data.json")
io.open(outp, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("wrote", outp)

# L10 check for the report: is it also simultaneous?
dump = json.load(io.open(os.path.join(ROOT, "scratchpad", "_maths_edexcel_practice.json"), encoding="utf-8"))
for r in dump:
    if r["units"]["slug"] == "algebra" and r["lesson_number"] in (9, 10):
        print("L%02d:" % r["lesson_number"], r.get("title"))

if PUSH:
    KEY = os.environ["SUPABASE_SERVICE_KEY"]
    lid = next(r["id"] for r in dump if r["units"]["slug"] == "algebra" and r["lesson_number"] == 9)
    req = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + lid, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"},
        data=json.dumps({"practice_data": pd}).encode())
    urllib.request.urlopen(req)
    print("PATCHED live lesson", lid)
else:
    print("dry run — rerun with --push to update Supabase")
