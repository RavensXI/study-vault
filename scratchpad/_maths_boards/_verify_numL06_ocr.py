# -*- coding: utf-8 -*-
"""Independent adversarial check of number-L06 OCR shard: fresh-solve every
problem, confirm duplicates gone, sanity-check box chains and expects."""
import json, io
from fractions import Fraction as F

pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_number-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
fails = []

# fresh solutions keyed by display (computed independently)
expected = {
    "Evaluate \\(3^4\\)": [81],
    "Evaluate \\(\\sqrt{144}\\)": [12],
    "Evaluate \\(10^3\\)": [1000],
    "Evaluate \\(\\sqrt[3]{27}\\)": [3],
    "Write \\(56\\,000\\) in standard form": [5.6, 4],
    "Write \\(0.003\\) in standard form": [3, -3],
    "Evaluate \\(5^2 + 3^2\\)": [34],
    "Write \\(8.1 \\times 10^5\\) as an ordinary number": [810000],
    "Simplify \\(2^3 \\times 2^5\\). Give your answer as a power of 2.": [8],
    "Simplify \\(5^7 \\div 5^3\\). Give your answer as a power of 5.": [4],
    "Evaluate \\(4^{-2}\\). Give your answer as a fraction.": [1, 16],
    "Calculate \\((4 \\times 10^3) \\times (3 \\times 10^5)\\)": [1.2, 9],
    "Evaluate \\(27^{1/3}\\)": [3],
    "Calculate \\((8 \\times 10^6) \\div (2 \\times 10^2)\\)": [4, 4],
    "Evaluate \\(81^{3/4}\\)": [27],
    "Calculate \\((6 \\times 10^4) \\times (5 \\times 10^{-2})\\)": [3, 3],
    "Simplify \\((3^2)^4\\). Give your answer as a power of 3.": [8],
    "Evaluate \\(125^{-2/3}\\). Give your answer as a fraction.": [1, 25],
    "Calculate \\((2 \\times 10^5) + (3.5 \\times 10^4)\\)": [2.35, 5],
    "Evaluate \\(8^{2/3} \\times 4^{-1/2}\\). Give your answer as a fraction.": [2, 1],
}

# recompute standard-form numeric value to confirm the [A,n] pair
def val(pair):
    return pair[0] * (10 ** pair[1])

# spot numeric truth-checks (independent of the stored answer)
truth = {
    "Write \\(56\\,000\\) in standard form": 56000,
    "Write \\(0.003\\) in standard form": 0.003,
    "Calculate \\((4 \\times 10^3) \\times (3 \\times 10^5)\\)": (4e3)*(3e5),
    "Calculate \\((8 \\times 10^6) \\div (2 \\times 10^2)\\)": (8e6)/(2e2),
    "Calculate \\((6 \\times 10^4) \\times (5 \\times 10^{-2})\\)": (6e4)*(5e-2),
    "Calculate \\((2 \\times 10^5) + (3.5 \\times 10^4)\\)": (2e5)+(3.5e4),
}

for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        d = p["display"]
        sol = p["solutions"]
        exp = expected.get(d)
        if exp is None:
            fails.append("%s[%d] display not in expected map: %s" % (tier, i, d)); continue
        if [float(x) for x in sol] != [float(x) for x in exp]:
            fails.append("%s[%d] solution %s != fresh %s (%s)" % (tier, i, sol, exp, d))
        if d in truth:
            if abs(val(sol) - truth[d]) > 1e-6:
                fails.append("%s[%d] standard-form pair %s = %g != true %g" % (tier, i, sol, val(sol), truth[d]))
        key = tuple(float(x) for x in sol)
        if key in seen and p.get("input_type") != "multiple_choice":
            fails.append("%s duplicate solution %s at [%d] and [%d]" % (tier, sol, seen[key], i))
        seen[key] = i
        # final live boxes should land on the solution values (order-independent multiset)
        gs = p.get("guided_steps") or []
        boxvals = [st["answer"] for st in gs if st.get("answer") is not None]
        for s in sol:
            if not any(abs(float(b) - float(s)) < 1e-6 for b in boxvals):
                fails.append("%s[%d] solution value %s never appears as a box answer" % (tier, i, s))
        # expects must differ from the correct answer
        for j, m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            if isinstance(e, list) and [float(x) for x in e] == [float(x) for x in sol]:
                fails.append("%s[%d].misc[%d] expect==solution" % (tier, i, j))
            if not isinstance(e, list) and e is not None and abs(float(e) - float(sol[0])) < 1e-9 and len(sol) == 1:
                fails.append("%s[%d].misc[%d] expect==solution" % (tier, i, j))

# opener box truths
op = [s.get("answer") for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if op != [6, 6, 8]:
    fails.append("opener box answers %s != [6,6,8]" % op)
# 1.5e8 == 150000000
if 1.5 * 10**8 != 150000000:
    fails.append("opener 1.5e8 mismatch")

print("problems checked:", sum(len(pb[t]) for t in ("bronze","silver","gold")))
if fails:
    print("FAIL", len(fails))
    for f in fails: print("  -", f)
else:
    print("ALL MATHS CHECKS PASS")
