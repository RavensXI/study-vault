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
  "The y terms are +y and −y. Opposite signs, so ADD the equations.",
  []),
 (r"Solve \(2x + y = 9\) and \(x + y = 5\)", [4, 1],
  "Both equations have +y (same sign), so subtract one from the other.",
  [dict(pattern="rhs_not_subtracted", expect=[14, -9],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="When you subtract the equations, the right-hand sides subtract too: \\(9 - 5 = 4\\), so \\(x = 4\\). Adding them instead gives 14, which is too big to fit either equation. Always do the same thing to both sides.")],
 ),
 (r"Solve \(3x + y = 11\) and \(x + y = 5\)", [3, 2],
  "Both equations have +y, so subtract to make the y terms vanish.",
  [dict(pattern="rhs_not_subtracted", expect=[8, -3],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtracting the left-hand sides means subtracting the right-hand sides as well: \\(11 - 5 = 6\\), so \\(2x = 6\\) and \\(x = 3\\). It looks like the right-hand sides were added instead.")],
 ),
 (r"Solve \(x + 2y = 10\) and \(x + y = 7\)", [4, 3],
  "The x terms already match, so subtract to remove them.",
  [dict(pattern="rhs_not_subtracted", expect=[-10, 17],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtracting the equations removes x and leaves \\(y = 10 - 7 = 3\\). It looks like the right-hand sides were added (giving 17) instead of subtracted. Both sides get the same treatment.")],
 ),
 (r"Solve \(2x + y = 10\) and \(2x - y = 6\)", [4, 2],
  "Opposite signs on y, so adding the equations makes y disappear.",
  [dict(pattern="rhs_wrong_operation", expect=[1, 8],
        _sim=dict(op="sub", rhs_wrong=True, subst=1),
        message="Whichever route you take, the right-hand sides must get the same operation as the left. Adding: \\(4x = 16\\) so \\(x = 4\\). Subtracting: \\(2y = 4\\) so \\(y = 2\\). Mixing the two up leads to \\(x = 1, y = 8\\), which doesn't fit either equation.")],
 ),
 (r"Solve \(3x + y = 17\) and \(x + y = 7\)", [5, 2],
  "Both equations have +y, so subtract them.",
  [dict(pattern="rhs_not_subtracted", expect=[12, -5],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="Subtract the right-hand sides too: \\(17 - 7 = 10\\), so \\(2x = 10\\) and \\(x = 5\\). Adding them gives 24 and everything after that comes out wrong.")],
 ),
 (r"Solve \(x + 3y = 14\) and \(x + y = 6\)", [2, 4],
  "The x terms match, so subtract to leave just y terms.",
  [dict(pattern="rhs_not_subtracted", expect=[-4, 10],
        _sim=dict(op="sub", rhs_wrong=True, subst=2),
        message="After subtracting, \\(2y = 14 - 6 = 8\\), so \\(y = 4\\). It looks like the right-hand sides were added. They must be subtracted, exactly like the left-hand sides.")],
 ),
 (r"Solve \(4x + y = 13\) and \(2x + y = 7\)", [3, 1],
  "Same sign on y in both, so subtract.",
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
        message="When you multiply an equation, multiply BOTH sides. \\(x + y = 8\\) doubled is \\(2x + 2y = 16\\). The 8 doubles too. Leaving it as 8 makes every later step wrong."),
   dict(pattern="rhs_not_subtracted", expect=[35, -27],
        _sim=dict(scale=(1, 2), op="sub", rhs_wrong=True, subst=2),
        message="After doubling the second equation the right-hand sides are 19 and 16, and subtracting gives \\(x = 3\\). It looks like they were added (35) instead of subtracted.")],
 ),
 (r"Solve \(2x + 5y = 21\) and \(x + 2y = 8\)", [-2, 5],
  "Multiply the second equation by 2 so both have 2x. Watch out: x comes out negative.",
  [dict(pattern="scaled_lhs_only", expect=[-18, 13],
        _sim=dict(scale=(1, 2), lhs_only=2, op="sub", subst=2),
        message="Doubling \\(x + 2y = 8\\) gives \\(2x + 4y = 16\\). The right-hand side doubles as well. Keeping it at 8 gives \\(y = 13\\), which is too big to fit either equation."),
   dict(pattern="rhs_not_subtracted", expect=[-66, 37],
        _sim=dict(scale=(1, 2), op="sub", rhs_wrong=True, subst=2),
        message="Subtract the right-hand sides: \\(21 - 16 = 5\\), so \\(y = 5\\). Adding them (37) instead of subtracting is the slip here.")],
 ),
 (r"Solve \(4x + y = 14\) and \(2x + 3y = 12\)", [3, 2],
  "Multiply the first equation by 3 so both have 3y.",
  [dict(pattern="scaled_lhs_only", expect=[0.2, 13.2],
        _sim=dict(scale=(3, 1), lhs_only=1, op="sub", subst=1),
        message="Multiplying \\(4x + y = 14\\) by 3 gives \\(12x + 3y = 42\\). The 14 gets multiplied too. If the right-hand side stays at 14 you end up with decimals that don't fit the equations."),
   dict(pattern="rhs_not_subtracted", expect=[5.4, -7.6],
        _sim=dict(scale=(3, 1), op="sub", rhs_wrong=True, subst=1),
        message="After scaling, subtract the right-hand sides: \\(42 - 12 = 30\\), so \\(10x = 30\\) and \\(x = 3\\). Adding them (54) is the slip. Both sides get subtracted.")],
 ),
 (r"Solve \(5x - y = 5\) and \(2x + 3y = 19\)", [2, 5],
  "Multiply the first equation by 3. The y terms then have opposite signs, so add.",
  [dict(pattern="substitute_sign_slip", expect=[2, -5],
        message="\\(x = 2\\) is right. Substituting into \\(5x - y = 5\\) gives \\(10 - y = 5\\), so \\(y = 5\\), positive. Getting \\(-5\\) means the sign flipped once too often when moving terms across.",
        note="From 10 - y = 5: -y = -5 so y = 5; the slip keeps y = -5.")],
 ),
 (r"Solve \(x + 4y = 17\) and \(3x + 2y = 11\)", [1, 4],
  "Multiply the second equation by 2 so both have 4y.",
  [dict(pattern="scaled_lhs_only", expect=[-1.2, 4.55],
        _sim=dict(scale=(1, 2), lhs_only=2, op="sub", subst=1),
        message="Doubling \\(3x + 2y = 11\\) gives \\(6x + 4y = 22\\). The 11 doubles too. Leaving it at 11 makes x come out negative when it shouldn't."),
   dict(pattern="rhs_not_subtracted", expect=[7.8, 2.3],
        _sim=dict(scale=(1, 2), op="sub", rhs_wrong=True, subst=1),
        message="Subtracting the right-hand sides gives \\(22 - 17 = 5\\), so \\(5x = 5\\) and \\(x = 1\\). Adding them (39) instead is the slip here.")],
 ),
 (r"Solve \(3x + y = 13\) and \(2x + 3y = 18\)", [3, 4],
  "Multiply the first equation by 3 so both have 3y.",
  [dict(pattern="substitute_sign_slip", expect=[3, 22],
        message="\\(x = 3\\) is right. Substituting into \\(3x + y = 13\\) gives \\(9 + y = 13\\), so \\(y = 4\\). Getting 22 means the 9 was added to 13 instead of subtracted. Moving a term across the equals sign changes its sign.",
        note="Slip: y = 13 + 9 = 22 instead of 13 - 9 = 4.")],
 ),
 (r"Solve \(2x - 3y = 6\) and \(x + y = 8\)", [6, 2],
  "Multiply the second equation by 3. Opposite signs on the y terms, so add.",
  [dict(pattern="scaled_lhs_only", expect=[2.8, 5.2],
        _sim=dict(scale=(1, 3), lhs_only=2, op="add", subst=2),
        message="Multiplying \\(x + y = 8\\) by 3 gives \\(3x + 3y = 24\\). The 8 is multiplied too. Keeping it at 8 gives decimal answers, and this question has whole-number ones.")],
 ),
]

GOLD = [
 (r"Solve \(3x + 4y = 25\) and \(2x + 3y = 18\)", [3, 4],
  "No single multiplication works here, so scale BOTH equations (try ×3 and ×4, or ×2 and ×3).",
  [dict(pattern="rhs_not_subtracted", expect=[147, -104],
        _sim=dict(scale=(3, 4), op="sub", rhs_wrong=True, subst=1),
        message="After scaling by 3 and 4 the right-hand sides are 75 and 72. Subtract them: \\(x = 75 - 72 = 3\\). Adding them (147) is the slip. The right-hand sides get subtracted just like the left."),
   dict(pattern="scaled_lhs_only", expect=[57, -36.5],
        _sim=dict(scale=(3, 4), lhs_only=2, op="sub", subst=1),
        message="Both equations must be multiplied on BOTH sides. Scaling \\(2x + 3y = 18\\) by 4 gives \\(8x + 12y = 72\\). If the 18 is left unscaled, x comes out as 57, which fits neither equation.")],
 ),
 (r"Solve \(5x + 3y = 29\) and \(3x + 4y = 24\)", [4, 3],
  "Scale both equations: ×4 and ×3 makes both y terms 12y.",
  []),
 (r"Solve \(2x + 3y = 4\) and \(5x + 2y = -1\)", [-1, 2],
  "Scale both (×2 and ×3 makes both 6y). Negative numbers appear, so keep signs on a tight leash.",
  []),
 (r"Solve \(7x + 2y = 27\) and \(3x + 5y = 24\)", [3, 3],
  "Scale both equations: ×5 and ×2 makes both y terms 10y.",
  [dict(pattern="substitute_sign_slip", expect=[3, 24],
        message="\\(x = 3\\) is right. Substituting into \\(7x + 2y = 27\\) gives \\(21 + 2y = 27\\), so \\(2y = 6\\) and \\(y = 3\\). Getting 24 means the 21 was added instead of subtracted when moving it across.",
        note="Slip: 2y = 27 + 21 = 48, y = 24.")],
 ),
 (r"Solve \(5x - 3y = 1\) and \(2x + 7y = 25\)", [2, 3],
  "Scale both (×7 and ×3 makes the y terms −21y and +21y). Opposite signs, so add.",
  [dict(pattern="substitute_sign_slip", expect=[2, -3],
        message="\\(x = 2\\) is right. Substituting into \\(5x - 3y = 1\\) gives \\(10 - 3y = 1\\), so \\(3y = 9\\) and \\(y = 3\\), positive. Getting \\(-3\\) means a sign flipped once too often on the way.",
        note="From 10 - 3y = 1: -3y = -9 so y = 3; the slip keeps y = -3.")],
 ),
]

TIER_DESCRIPTIONS = {
 "bronze_description": "The numbers in front already match: add or subtract once and a letter vanishes",
 "silver_description": "Multiply one equation first to make a matching pair",
 "gold_description": "Multiply both equations, or switch to the substitution method",
}

METHOD_CARD = {
 "title": "Simultaneous Equations (Linear)",
 "steps": [
  "Find (or make) a matching pair: the same number in front of x or of y in both equations.",
  "Same signs? Subtract. Opposite signs? Add. The matched letter vanishes.",
  "Solve what's left, substitute back, and check the pair in both equations.",
 ],
 "content": "<p><strong>Simultaneous equations</strong> are two equations sharing the same two unknowns. Exactly one pair of values, an \\(x\\) and a \\(y\\), fits both, and your job is to find it by making one letter disappear.</p><p>Remember <strong>SSS: Same Signs Subtract</strong>. Opposite signs? Add instead.</p>",
 "example": "<p><strong>Solve</strong> \\(2x + y = 7\\) and \\(x + y = 4\\)</p><p>Both have \\(+y\\), the same sign, so subtract: \\(x = 3\\). Then \\(3 + y = 4\\), so \\(y = 1\\). Check in the first: \\(2(3) + 1 = 7\\) ✓</p>",
}

# Progressive teaching: one rung's method at a time. Bronze shows before Q1 on
# first visit; silver and gold appear as interstitials at their transitions.
# The left panel always shows only the current rung's card.
TIER_GUIDES = {
 "bronze": {
  "title": "Bronze: the pair already matches",
  "steps": [
   "You need the one pair of values, an \\(x\\) AND a \\(y\\), that fits both equations. In bronze, a matching pair is already there (like \\(+y\\) in both).",
   "<strong>Same Signs Subtract</strong>: subtract one equation from the other (right-hand sides too) and the matched letter vanishes. Opposite signs (\\(+y\\) and \\(-y\\))? Add instead.",
   "Solve the one-letter equation that's left, then substitute your value into the easier original equation to find the other letter.",
  ],
  "example": {
   "question": "Solve 3x + y = 10 and x + y = 4",
   "steps": [
    {"label": "Match", "content": "<p>Both equations have \\(+y\\), the same sign, so subtract.</p>"},
    {"label": "Subtract", "content": "<p>\\((3x + y) - (x + y) = 10 - 4\\) → \\(2x = 6\\) → \\(x = 3\\)</p>"},
    {"label": "Substitute", "content": "<p>\\(3 + y = 4\\) → \\(y = 1\\)</p>"},
    {"label": "Check", "content": "<p>\\(3(3) + 1 = 10\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(x = 3\\), \\(y = 1\\)</p>", "isAnswer": True, "is_answer": True},
   ]},
 },
 "silver": {
  "title": "Silver: make a match first",
  "steps": [
   "Now nothing matches yet. Multiply ONE whole equation (every term, both sides of the equals sign) until a pair matches.",
   "Then it's a bronze question: same signs subtract, opposite signs add.",
   "Substitute back and check your pair in both equations.",
  ],
  "example": {
   "question": "Solve 2x + 3y = 12 and x + y = 5",
   "steps": [
    {"label": "Multiply", "content": "<p>Second equation \\(\\times 3\\): \\(3x + 3y = 15\\). The 5 is multiplied too.</p>"},
    {"label": "Subtract", "content": "<p>\\((3x + 3y) - (2x + 3y) = 15 - 12\\) → \\(x = 3\\)</p>"},
    {"label": "Substitute", "content": "<p>\\(3 + y = 5\\) → \\(y = 2\\)</p>"},
    {"label": "Check", "content": "<p>\\(2(3) + 3(2) = 12\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(x = 3\\), \\(y = 2\\)</p>", "isAnswer": True, "is_answer": True},
   ]},
 },
 "gold": {
  "title": "Gold: multiply both equations",
  "steps": [
   "Sometimes no single multiplication works. Multiply BOTH equations to hit a common target: \\(3y\\) and \\(2y\\) both become \\(6y\\) with \\(\\times 2\\) and \\(\\times 3\\).",
   "Everything else is the same: same signs subtract, opposite signs add, substitute back, check.",
   "Prefer rearranging? <strong>Substitution</strong> also works: make \\(y\\) the subject of one equation and substitute it into the other. Either method gets full marks.",
  ],
  "example": {
   "question": "Solve 4x + 3y = 23 and 3x + 2y = 16",
   "steps": [
    {"label": "Multiply both", "content": "<p>First \\(\\times 2\\): \\(8x + 6y = 46\\). Second \\(\\times 3\\): \\(9x + 6y = 48\\).</p>"},
    {"label": "Subtract", "content": "<p>\\((9x + 6y) - (8x + 6y) = 48 - 46\\) → \\(x = 2\\)</p>"},
    {"label": "Substitute", "content": "<p>\\(6 + 2y = 16\\) → \\(y = 5\\)</p>"},
    {"label": "Check", "content": "<p>\\(4(2) + 3(5) = 23\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(x = 2\\), \\(y = 5\\)</p>", "isAnswer": True, "is_answer": True},
   ]},
 },
}

WORKED_EXAMPLES = [
 {"difficulty": "Bronze", "question": "Solve 3x + y = 10 and x + y = 4",
  "steps": [
   {"label": "Step 1: Spot the match", "content": "<p>Both equations contain exactly \\(+y\\), the same sign in both. <strong>Same Signs Subtract.</strong></p>"},
   {"label": "Step 2: Subtract the equations", "content": "<p>\\((3x + y) - (x + y) = 10 - 4\\) → \\(2x = 6\\) → \\(x = 3\\). The \\(y\\) terms cancel, and the right-hand sides are subtracted too.</p>"},
   {"label": "Step 3: Substitute back", "content": "<p>Put \\(x = 3\\) into the simpler equation: \\(3 + y = 4\\) → \\(y = 1\\).</p>"},
   {"label": "Step 4: Check", "content": "<p>In the other equation: \\(3(3) + 1 = 10\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 3\\), \\(y = 1\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Bronze", "question": "Solve 3x + 2y = 17 and 5x − 2y = 7",
  "steps": [
   {"label": "Step 1: Spot the match", "content": "<p>The \\(y\\) terms are \\(+2y\\) and \\(-2y\\): same size, <em>opposite</em> signs. Opposite signs means <strong>add</strong>: \\(+2y\\) and \\(-2y\\) make zero.</p>"},
   {"label": "Step 2: Add the equations", "content": "<p>\\((3x + 2y) + (5x - 2y) = 17 + 7\\) → \\(8x = 24\\) → \\(x = 3\\).</p>"},
   {"label": "Step 3: Substitute back", "content": "<p>\\(x = 3\\) into the first equation: \\(9 + 2y = 17\\) → \\(2y = 8\\) → \\(y = 4\\).</p>"},
   {"label": "Step 4: Check", "content": "<p>\\(5(3) - 2(4) = 15 - 8 = 7\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 3\\), \\(y = 4\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Silver", "question": "Solve 2x + 3y = 12 and x + y = 5",
  "steps": [
   {"label": "Step 1: Nothing matches yet", "content": "<p>\\(2x\\) vs \\(x\\), \\(3y\\) vs \\(y\\): no matching pair. Multiply the <em>whole</em> second equation by 3: \\(3x + 3y = 15\\). The 5 gets multiplied too (every term, both sides).</p>"},
   {"label": "Step 2: Subtract", "content": "<p>Now both have \\(3y\\), same sign. \\((3x + 3y) - (2x + 3y) = 15 - 12\\) → \\(x = 3\\).</p>"},
   {"label": "Step 3: Substitute back", "content": "<p>\\(x = 3\\) into \\(x + y = 5\\): \\(y = 2\\).</p>"},
   {"label": "Step 4: Check", "content": "<p>\\(2(3) + 3(2) = 6 + 6 = 12\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 3\\), \\(y = 2\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Gold", "question": "Solve 4x + 3y = 23 and 3x + 2y = 16",
  "steps": [
   {"label": "Step 1: Scale BOTH equations", "content": "<p>No single multiplication makes a match, so make the \\(y\\) terms both \\(6y\\): first equation \\(\\times 2\\) → \\(8x + 6y = 46\\); second \\(\\times 3\\) → \\(9x + 6y = 48\\). Both sides of both equations get scaled.</p>"},
   {"label": "Step 2: Subtract", "content": "<p>Same signs, so subtract: \\((9x + 6y) - (8x + 6y) = 48 - 46\\) → \\(x = 2\\).</p>"},
   {"label": "Step 3: Substitute back", "content": "<p>\\(x = 2\\) into \\(3x + 2y = 16\\): \\(6 + 2y = 16\\) → \\(y = 5\\).</p>"},
   {"label": "Step 4: Check", "content": "<p>\\(4(2) + 3(5) = 8 + 15 = 23\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 2\\), \\(y = 5\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
 {"difficulty": "Gold", "question": "Solve 2x + y = 11 and 3x + 2y = 18 (substitution method)",
  "steps": [
   {"label": "Step 1: Make y the subject", "content": "<p>From the first equation: \\(y = 11 - 2x\\). This is the substitution method, the alternative to elimination, and worth the same marks.</p>"},
   {"label": "Step 2: Substitute into the other equation", "content": "<p>\\(3x + 2(11 - 2x) = 18\\) → \\(3x + 22 - 4x = 18\\) → \\(-x = -4\\) → \\(x = 4\\).</p>"},
   {"label": "Step 3: Find y", "content": "<p>\\(y = 11 - 2(4) = 3\\).</p>"},
   {"label": "Step 4: Check", "content": "<p>\\(3(4) + 2(3) = 12 + 6 = 18\\) ✓</p>"},
   {"label": "Answer", "content": "<p><strong>\\(x = 4\\), \\(y = 3\\)</strong></p>", "isAnswer": True, "is_answer": True},
  ]},
]

# ============================== GUIDED STEPS ==============================
# Learning-by-doing: every problem gets machine-generated micro-steps (each a
# tiny numeric box). Same data drives the "walk me through one" teaching
# problems and the "do this one with me" rescue on wrong answers.

def _i(f):
    assert f == int(f), "non-integer in guided step: %s" % f
    return int(f)

def term(c, letter, lead=False):
    c = _i(c)
    mag = ("" if abs(c) == 1 else str(abs(c))) + letter
    if lead:
        return ("-" if c < 0 else "") + mag
    return ("- " if c < 0 else "+ ") + mag

def fmt_eq(a, b, c):
    return term(a, "x", True) + " " + term(b, "y") + " = " + str(_i(c))

def par(n):
    n = _i(n)
    return "(" + str(n) + ")" if n < 0 else str(n)

def route_of(e1, e2):
    """Cheapest elimination route: (letter_index, k1, k2). Tie prefers y."""
    import math as _m
    best = None
    for pick in (1, 0):  # try y first so ties prefer eliminating y
        c1, c2 = abs(e1[pick]), abs(e2[pick])
        if c1 == 0 or c2 == 0:
            continue
        l = c1 * c2 / F(_m.gcd(c1.numerator, c2.numerator))
        k1, k2 = _i(l / c1), _i(l / c2)
        score = (k1 != 1) + (k2 != 1)
        if best is None or score < best[0]:
            best = (score, pick, k1, k2)
    return best[1], best[2], best[3]

def gen_guided(e1, e2, sol):
    """Generate guided micro-steps for an elimination solve. Returns list of
    steps: {say?, pre?, post?, answer?, hint?, done?} — steps without answer
    are statements."""
    (a1, b1, c1), (a2, b2, c2) = e1, e2
    pick, k1, k2 = route_of(e1, e2)
    L = "xy"[pick]          # letter being eliminated
    S = "xy"[1 - pick]      # survivor
    steps = []

    def scale_steps(a, b, c, k, which):
        cs = [(a, "x"), (b, "y")]
        say = ("To make the " + L + " terms match, multiply ALL of \\(" + fmt_eq(a, b, c) +
               "\\) by " + str(k) + ": every term, both sides.")
        first = True
        for coef, let in cs:
            steps.append({
                "say": say if first else None,
                "pre": term(coef, let, True) + " × " + str(k) + " = ", "post": let,
                "answer": _i(coef * k),
                "hint": "Just multiply the number in front" + (", and keep the minus." if coef < 0 else ".")})
            first = False
        steps.append({
            "pre": "and the right-hand side: " + par(c) + " × " + str(k) + " = ", "post": "",
            "answer": _i(c * k),
            "hint": "The right-hand side gets multiplied too. That's the step everyone forgets."})

    if k1 > 1: scale_steps(a1, b1, c1, k1, 1)
    if k2 > 1: scale_steps(a2, b2, c2, k2, 2)

    A1, B1_, C1 = a1 * k1, b1 * k1, c1 * k1
    A2, B2_, C2 = a2 * k2, b2 * k2, c2 * k2
    m1, m2 = (A1, A2) if pick == 1 else (B1_, B2_)   # survivor coefficients
    e1c, e2c = (A1, B1_, C1), (A2, B2_, C2)
    lc1, lc2 = (B1_, B2_) if pick == 1 else (A1, A2)  # eliminated-letter coefficients
    same_sign = (lc1 > 0) == (lc2 > 0)

    if same_sign:
        # subtract in the direction that keeps the survivor positive
        if m1 - m2 < 0:
            e1c, e2c = e2c, e1c
        (A1, B1_, C1), (A2, B2_, C2) = e1c, e2c
        surv = (A1 - A2) if pick == 1 else (B1_ - B2_)
        assert (A1 if pick == 1 else B1_) > 0 and (A2 if pick == 1 else B2_) > 0, \
            "sub-route survivor coefficients must be positive"
        elim1, elim2 = (B1_, B2_) if pick == 1 else (A1, A2)
        steps.append({
            "say": "Both equations now have " + term(elim1, L, True) +
                   ", the same sign. <strong>Same Signs Subtract.</strong> Take \\(" +
                   fmt_eq(*e2c) + "\\) away from \\(" + fmt_eq(*e1c) + "\\), term by term:",
            "pre": term((A1 if pick == 1 else B1_), S, True) + " − " + term((A2 if pick == 1 else B2_), S, True) + " = ",
            "post": S, "answer": _i(surv),
            "hint": "Subtract the numbers in front: " + str(_i(A1 if pick == 1 else B1_)) + " − " + str(_i(A2 if pick == 1 else B2_)) + "."})
        steps.append({
            "pre": term(elim1, L, True) + " − " + term(elim2, L, True) + " = ", "post": "",
            "answer": 0, "done": "Gone. That was the whole point.",
            "hint": "They're identical, and anything minus itself is 0."})
        steps.append({
            "pre": str(_i(C1)) + " − " + par(C2) + " = ", "post": "",
            "answer": _i(C1 - C2),
            "hint": "The right-hand sides get subtracted too, exactly like the left."})
        R = C1 - C2
    else:
        surv = (A1 + A2) if pick == 1 else (B1_ + B2_)
        s1, s2 = ((A1, A2) if pick == 1 else (B1_, B2_))
        assert s1 > 0 and s2 > 0, "add-route survivor coefficients must be positive"
        elim1, elim2 = (B1_, B2_) if pick == 1 else (A1, A2)
        def wrap(coef, letter):
            t = term(coef, letter, True)
            return "(" + t + ")" if coef < 0 else t
        steps.append({
            "say": "The " + L + " terms are " + term(elim1, L, True) + " and " + term(elim2, L, True) +
                   ". Opposite signs, so <strong>ADD</strong> the equations and they cancel:",
            "pre": term(s1, S, True) + " + " + term(s2, S, True) + " = ",
            "post": S, "answer": _i(surv),
            "hint": "Add the numbers in front."})
        steps.append({
            "pre": term(elim1, L, True) + " + " + wrap(elim2, L) + " = ", "post": "",
            "answer": 0, "done": "Cancelled. Adding opposites gives zero.",
            "hint": "One is plus, one is minus, same size, so they cancel to 0."})
        steps.append({
            "pre": str(_i(C1)) + " + " + par(C2) + " = ", "post": "",
            "answer": _i(C1 + C2),
            "hint": "Add the right-hand sides too."})
        R = C1 + C2

    sv = sol[1 - pick]  # numeric value of survivor (sol is [x, y])
    if _i(surv) != 1:
        steps.append({
            "say": "So " + term(surv, S, True) + " = " + str(_i(R)) + ".",
            "pre": S + " = ", "post": "", "answer": sv,
            "hint": "Divide both sides by " + str(_i(surv)) + "."})
    else:
        steps.append({"say": "So " + S + " = " + str(_i(R)) + ". Done in one."})

    # substitute into the original equation whose unknown-letter coefficient is nicest
    unk = pick  # index of the letter still unknown (the eliminated one)
    cands = [e1, e2]
    cands.sort(key=lambda e: (abs(e[unk]) != 1, abs(_i(e[unk])), abs(_i(e[0])) + abs(_i(e[1]))))
    ea, eb, ec = cands[0]
    kco = ea if unk == 1 else eb          # coefficient of the KNOWN letter in this eq
    uco = eb if unk == 1 else ea          # coefficient of the unknown letter
    known_val = sv
    kpart = kco * known_val
    uv = sol[unk]
    say_sub = "Now find " + L + ". Put " + S + " = " + par(sv) + " into \\(" + fmt_eq(ea, eb, ec) + "\\):"
    if abs(kco) != 1:
        say_sub = say_sub[:-1] + ". The " + S + " part is " + str(_i(kco)) + " × " + par(sv) + " = " + str(_i(kpart)) + ", so:"
    if uco == 1:
        steps.append({"say": say_sub,
            "pre": str(_i(kpart)) + " + " + L + " = " + str(_i(ec)) + "  →  " + L + " = ", "post": "",
            "answer": uv, "hint": "Take " + str(_i(kpart)) + " from both sides."})
    elif uco == -1:
        steps.append({"say": say_sub,
            "pre": str(_i(kpart)) + " − " + L + " = " + str(_i(ec)) + "  →  " + L + " = ", "post": "",
            "answer": uv, "hint": str(_i(kpart)) + " minus what gives " + str(_i(ec)) + "?"})
    else:
        steps.append({"say": say_sub,
            "pre": term(uco, L, True) + " = " + str(_i(ec)) + " − " + par(kpart) + " = ", "post": "",
            "answer": _i(ec - kpart), "hint": "Whatever is left after taking the known part away."})
        steps.append({
            "pre": L + " = ", "post": "", "answer": uv,
            "hint": "Divide by " + str(_i(uco)) + "."})

    # check in the other original equation
    oa, ob, oc = cands[1]
    xv, yv = sol[0], sol[1]
    def prod(coef, val):
        return par(val) if abs(_i(coef)) == 1 else str(abs(_i(coef))) + " × " + par(val)
    steps.append({
        "say": "Last thing: check the pair in the other equation:",
        "pre": prod(oa, xv) + " " + ("+" if ob > 0 else "−") + " " + prod(ob, yv) + " = ", "post": "",
        "answer": _i(oc), "done": "It balances, so x = " + par(xv) + ", y = " + par(yv) + " is right.",
        "hint": "Work it out. If it doesn't give " + str(_i(oc)) + ", something slipped."})
    return steps

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
        gs = gen_guided(e1, e2, sol)
        for st in gs:
            if "answer" in st:
                assert isinstance(st["answer"], (int, float)), "non-numeric step answer in " + tag
        out.append({"display": display, "solutions": sol, "input_type": "xy_pair",
                    "calculator": False, "hint": hint, "misconceptions": clean,
                    "guided_steps": gs})
    problems_out[tier] = out

print("bank: %d bronze / %d silver / %d gold, verification %s"
      % (len(problems_out["bronze"]), len(problems_out["silver"]), len(problems_out["gold"]),
         "FAILED (%d)" % errors if errors else "CLEAN"))
if errors:
    sys.exit(1)

# ============================== ASSEMBLE + PUSH ==============================
l09_path = r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad\_l09_live.json"
# ---- teaching walks (one per tier) + the concrete opener ----
def teach_problem(display, label):
    e1, e2 = parse_display(display)
    x, y = solve2(e1, e2)
    return {"display": display, "label": label,
            "steps": gen_guided(e1, e2, [_i(x) if x == int(x) else float(x),
                                         _i(y) if y == int(y) else float(y)])}

GUIDED = {
 "opener": {
  "label": "Before any algebra",
  "display": "2 coffees + 1 muffin = £7<br>1 coffee + 1 muffin = £4",
  "steps": [
   {"say": "A coffee-shop puzzle. No algebra allowed, just look at the two orders.",
    "pre": "A coffee costs £", "post": "", "answer": 3,
    "hint": "Compare the orders: the ONLY difference is one extra coffee, and £3 of price."},
   {"say": "That move you just made, comparing the orders and letting the muffin cancel out, is called <strong>elimination</strong>. You subtracted two equations without noticing.",
    "pre": "And the muffin? £", "post": "", "answer": 1,
    "hint": "One coffee (£3) and a muffin cost £4 together."},
   {"say": "That second move, using the value you know to find the one you don't, is <strong>substitution</strong>. Those two moves are the entire topic. Algebra just writes coffee as \\(x\\) and muffin as \\(y\\): \\(2x + y = 7\\) and \\(x + y = 4\\)."},
  ]},
 "teach": {
  "bronze": teach_problem(r"Solve \(3x + y = 10\) and \(x + y = 4\)", "Together: your first one"),
  "silver": teach_problem(r"Solve \(2x + 3y = 12\) and \(x + y = 5\)", "Together: the silver move"),
  "gold": teach_problem(r"Solve \(4x + 3y = 23\) and \(3x + 2y = 16\)", "Together: the gold move"),
 },
}
# silver/gold teaching walks must actually demonstrate the new move
_, sk1, sk2 = route_of(*parse_display(GUIDED["teach"]["silver"]["display"]))
assert (sk1 != 1) != (sk2 != 1), "silver walk must scale exactly one equation"
_, gk1, gk2 = route_of(*parse_display(GUIDED["teach"]["gold"]["display"]))
assert gk1 != 1 and gk2 != 1, "gold walk must scale both equations"

pd = json.load(io.open(l09_path, encoding="utf-8"))
pd["method_card"] = METHOD_CARD
pd["tier_guides"] = TIER_GUIDES
pd["guided"] = GUIDED
pd["worked_examples"] = WORKED_EXAMPLES
for k, v in TIER_DESCRIPTIONS.items():
    pd["problem_bank"][k] = v
for tier in ("bronze", "silver", "gold"):
    pd["problem_bank"][tier] = problems_out[tier]

# ---- style guard: NO em dashes in student-facing text (they read as minus
# signs next to numbers — Tom, 15 Jul). "note" fields are internal-only.
def dash_scan(obj, path="pd"):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k != "note":
                hits += dash_scan(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += dash_scan(v, path + "[%d]" % i)
    elif isinstance(obj, str) and "—" in obj:
        i = obj.find("—")
        hits.append(path + ": ..." + obj[max(0, i - 35):i + 35] + "...")
    return hits

dash_hits = dash_scan(pd)
if dash_hits:
    print("EM-DASH GUARD FAILED (%d):" % len(dash_hits))
    for h in dash_hits:
        print("  ", h)
    sys.exit(1)
print("em-dash guard: CLEAN")

outp = os.path.join(ROOT, "scratchpad", "_maths_audit", "_l09_rebuilt_practice_data.json")
io.open(outp, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("wrote", outp)

# ---- human-readable transcript of every guided walk, for eyeball QA ----
def transcript(name, steps, f):
    f.write("\n### " + name + "\n")
    for st in steps:
        if st.get("say"): f.write("  [say] " + st["say"] + "\n")
        if "answer" in st:
            f.write("  [box] " + (st.get("pre") or "") + "___" + (st.get("post") or "") +
                    "   => " + str(st["answer"]) + "   (hint: " + (st.get("hint") or "") + ")\n")
            if st.get("done"): f.write("        on-correct: " + st["done"] + "\n")
tf = io.open(os.path.join(ROOT, "scratchpad", "_maths_audit", "_l09_guided_transcripts.txt"), "w", encoding="utf-8")
transcript("OPENER", GUIDED["opener"]["steps"], tf)
for t in ("bronze", "silver", "gold"):
    transcript("TEACH " + t.upper() + " — " + GUIDED["teach"][t]["display"], GUIDED["teach"][t]["steps"], tf)
for tier in ("bronze", "silver", "gold"):
    for n, p in enumerate(pd["problem_bank"][tier]):
        transcript(tier[0].upper() + str(n) + " — " + p["display"], p["guided_steps"], tf)
tf.close()
print("wrote guided transcripts (eyeball QA file)")
for show in (("bronze", 0), ("silver", 1), ("gold", 2)):
    p = pd["problem_bank"][show[0]][show[1]]
    print("\n===== SAMPLE", show[0].upper(), show[1], p["display"], "=====")
    for st in p["guided_steps"]:
        if st.get("say"): print(" say:", st["say"][:110])
        if "answer" in st: print(" box:", (st.get("pre") or "") + "___" + (st.get("post") or ""), "=>", st["answer"])

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
