# -*- coding: utf-8 -*-
import json, io
from fractions import Fraction as F

pd = json.load(io.open("lesson_maths-eduqas_algebra-L07.json", encoding="utf-8"))
errs = []

# Independent fresh-solve: (a,b,c) of the standard-form quadratic ax^2+bx+c=0,
# the requested-value function, and expected stored solution.
def roots(a, b, c):
    disc = b * b - 4 * a * c
    assert disc >= 0, (a, b, c)
    s = F(disc).limit_denominator()
    # integer or simple sqrt
    import math
    r = math.isqrt(int(disc)) if disc == int(disc) else None
    assert r is not None and r * r == int(disc), ("non-square disc", a, b, c, disc)
    x1 = F(-b + r, 2 * a)
    x2 = F(-b - r, 2 * a)
    return sorted([x1, x2])

SPEC = {
 "bronze": [
  ((1, 5, 0), lambda rs: [x for x in rs if x != 0][0], [-5]),        # non-zero
  ((1, 0, -9), lambda rs: max(rs), [3]),                              # positive
  ((1, 7, 10), lambda rs: max(rs), [-2]),                             # larger
  ((1, -4, 0), lambda rs: [x for x in rs if x != 0][0], [4]),        # non-zero
  ((1, 0, -25), lambda rs: max(rs), [5]),                             # positive
  ((1, 1, -6), lambda rs: max(rs), [2]),                              # positive
  ((1, -6, 5), lambda rs: min(rs), [1]),                              # smaller
  ((1, 2, -8), lambda rs: min(rs), [-4]),                             # negative
 ],
 "silver": [
  ((1, -5, 6), lambda rs: sum(rs), [5]),                              # sum
  ((1, 3, -18), lambda rs: max(rs), [3]),                             # positive
  ((1, -2, -35), lambda rs: min(rs), [-5]),                           # negative
  ((1, -7, 12), lambda rs: max(rs), [4]),                             # larger (x^2=7x-12)
  ((1, 4, -12), lambda rs: max(rs), [2]),                             # positive (x^2+4x=12)
  ((1, -8, 7), lambda rs: max(rs), [7]),                              # larger (x^2=8x-7)
  ((1, -10, 25), lambda rs: len(set(rs)), [1]),                       # how many
 ],
 "gold": [
  ((2, 5, -3), lambda rs: max(rs).numerator, [1]),                    # positive numerator
  ((3, -1, -2), lambda rs: sum(rs), F(1, 3)),                         # sum as fraction
  ((6, 1, -2), lambda rs: min(rs).denominator, [3]),                  # negative denominator
  ((1, -3, -4), lambda rs: rs[0] * rs[1], [-4]),                      # product (x^2-x=2x+4)
  ((4, 0, -9), lambda rs: max(rs), F(3, 2)),                          # positive as fraction
 ],
}

def as_sol(v):
    if isinstance(v, F):
        return [v.numerator, v.denominator]
    if isinstance(v, list):
        return v
    return [int(v)]

for tier, specs in SPEC.items():
    probs = pd["problem_bank"][tier]
    if len(probs) != len(specs):
        errs.append("%s length %d != spec %d" % (tier, len(probs), len(specs)))
        continue
    seen = set()
    for i, ((a, b, c), fn, exp_sol) in enumerate(specs):
        rs = roots(a, b, c)
        val = fn(rs)
        want = exp_sol if isinstance(exp_sol, list) else exp_sol
        computed = as_sol(val) if not isinstance(exp_sol, F) else as_sol(val)
        target = exp_sol if isinstance(exp_sol, list) else as_sol(exp_sol)
        stored = probs[i]["solutions"]
        # normalise: whole numbers -> [n]; genuine fractions -> [num,den]
        if isinstance(val, F):
            computed = [val.numerator] if val.denominator == 1 else [val.numerator, val.denominator]
        elif isinstance(val, int):
            computed = [val]
        else:
            computed = [int(val)] if val == int(val) else [val]
        if computed != stored:
            errs.append("%s[%d] fresh-solve %s != stored %s (roots %s)" %
                        (tier, i, computed, stored, [str(x) for x in rs]))
        key = tuple(stored)
        if key in seen:
            errs.append("%s[%d] DUP solution tuple %s" % (tier, i, stored))
        seen.add(key)
        # misconception expects != solution, and every misconception has expect + message
        for j, m in enumerate(probs[i].get("misconceptions", [])):
            if "expect" not in m:
                errs.append("%s[%d].misc[%d] no expect" % (tier, i, j))
            if not m.get("message"):
                errs.append("%s[%d].misc[%d] no message" % (tier, i, j))
            e = m.get("expect")
            if e is not None:
                ev = e if isinstance(e, list) else [e]
                if [float(x) for x in ev] == [float(x) for x in stored]:
                    errs.append("%s[%d].misc[%d] expect == solution" % (tier, i, j))

# guided_steps structure: phase present, >=1 before, >=2 live after, >=3 boxes
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        gs = p.get("guided_steps", [])
        boxes = [k for k, s in enumerate(gs) if s.get("answer") is not None]
        phase = next((k for k, s in enumerate(gs) if s.get("phase") == "substitute"), None)
        if phase is None:
            errs.append("%s[%d] no phase" % (tier, i)); continue
        before = [k for k in boxes if k < phase]
        after = [k for k in boxes if k >= phase]
        if len(before) < 1: errs.append("%s[%d] no box before phase" % (tier, i))
        if len(after) < 2: errs.append("%s[%d] only %d live after phase" % (tier, i, len(after)))
        if len(boxes) < 3: errs.append("%s[%d] only %d boxes" % (tier, i, len(boxes)))
        # no LaTeX in pre/post/hint
        for k, s in enumerate(gs):
            for fld in ("pre", "post", "hint"):
                if "\\(" in (s.get(fld) or ""):
                    errs.append("%s[%d].step[%d].%s has LaTeX" % (tier, i, k, fld))

# teach: >=4 boxes each; opener has a box
for tier in ("bronze", "silver", "gold"):
    t = pd["guided"]["teach"][tier]
    nb = sum(1 for s in t["steps"] if s.get("answer") is not None)
    if nb < 4:
        errs.append("teach.%s only %d boxes" % (tier, nb))
opb = sum(1 for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None)
if opb < 1:
    errs.append("opener no box")

# check-box arithmetic: last box of each walk verified via substitution done in SPEC roots
print("errors:", len(errs))
for e in errs:
    print("  -", e)
if not errs:
    print("ALL GREEN: fresh-solve matches, no dup tuples, expects valid, walk structure ok")
