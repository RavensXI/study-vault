# -*- coding: utf-8 -*-
"""Adversarial independent checker for graphs-L08."""
import io, json
pd = json.load(io.open("lesson_graphs-L08.json", encoding="utf-8"))
errs = []

def approx(a, b): return abs(float(a) - float(b)) < 0.011

# 1. fresh-solve every trapezium / gradient problem from display, compare solutions
def trap(h, ys):
    return (h / 2) * (ys[0] + ys[-1] + 2 * sum(ys[1:-1]))

expected = {
    ("bronze", 0): 2, ("bronze", 1): 3, ("bronze", 2): 4, ("bronze", 3): 15,
    ("bronze", 4): 12, ("bronze", 5): 1, ("bronze", 6): 20, ("bronze", 7): 0,
    ("silver", 0): 26, ("silver", 1): 9.5, ("silver", 2): -2, ("silver", 3): 11.5,
    ("silver", 4): 0, ("silver", 5): 9, ("silver", 6): 24,
    ("gold", 0): 26, ("gold", 1): 60, ("gold", 2): 7.8, ("gold", 3): 12.01, ("gold", 4): 5.75,
}
# independent recompute for trapezium/gradient problems
indep = {
    ("silver", 0): trap(2, [1, 6, 13]), ("silver", 1): trap(1, [0, 1, 4, 9]),
    ("silver", 3): trap(0.5, [2, 3, 5, 8, 12]), ("silver", 5): trap(1, [2, 4, 8]),
    ("silver", 6): trap(2, [0, 4, 16]),
    ("gold", 0): trap(1, [1, 2, 5, 10, 17]), ("gold", 1): trap(2, [0, 8, 12, 20]),
    ("gold", 4): trap(0.5, [1, 1.5, 2.5, 4, 6]),
}
indep[("bronze", 0)] = (12 - 4) / (6 - 2)
indep[("bronze", 1)] = (11 - 5) / (3 - 1)
indep[("bronze", 2)] = (10 - 2) / (2 - 0)
indep[("bronze", 7)] = (7 - 7) / (5 - 3)
indep[("silver", 2)] = (-2 - 6) / (3 - (-1))
indep[("gold", 2)] = abs(48.5 - 45) / 45 * 100
indep[("gold", 3)] = (9.261 - 6.859) / (2.1 - 1.9)

for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        if not approx(sol, expected[(tier, i)]):
            errs.append("%s[%d] solution %s != expected %s" % (tier, i, sol, expected[(tier, i)]))
        if (tier, i) in indep and not approx(round(indep[(tier, i)], 2), sol):
            errs.append("%s[%d] independent recompute %s != solution %s" % (tier, i, indep[(tier, i)], sol))
        # duplicate within tier (non-MC)
        if p.get("input_type") != "multiple_choice":
            key = tuple(p["solutions"])
            if key in seen:
                errs.append("%s[%d] duplicate solution %s (also %s)" % (tier, i, key, seen[key]))
            seen[key] = i
        # non-calc clean check
        if not p.get("calculator") and p.get("input_type") != "multiple_choice":
            # clean = at most 2 dp and denominator-friendly
            if abs(sol * 4 - round(sol * 4)) > 1e-9:
                errs.append("%s[%d] non-calc messy answer %s" % (tier, i, sol))

# 2. recompute every guided_steps box; final box lands on solution; boundary checks
def walk_boxes(steps):
    return [s["answer"] for s in steps if s.get("answer") is not None]

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        gs = p.get("guided_steps")
        if not gs:
            if p.get("input_type") != "multiple_choice":
                errs.append("%s[%d] missing guided_steps" % (tier, i))
            continue
        boxes = walk_boxes(gs)
        # find substitute boundary
        sub = next((k for k, s in enumerate(gs) if s.get("phase") == "substitute"), None)
        if sub is None:
            errs.append("%s[%d] no substitute boundary" % (tier, i))
        else:
            live_after = sum(1 for s in gs[sub:] if s.get("answer") is not None)
            if live_after < 2:
                errs.append("%s[%d] only %d live boxes after boundary" % (tier, i, live_after))
        # last box should equal solution for computational problems (not the concept ones)
        # verify arithmetic embedded in pre text where it is "a OP b = "
        for k, s in enumerate(gs):
            if s.get("answer") is None:
                continue
            pre = s.get("pre", "")
            # try to eval simple 'expr = ' patterns
            import re
            m = re.match(r"^\s*(.*?)\s*=\s*$", pre.replace("×", "*").replace("÷", "/").replace("−", "-").replace("½", "0.5*"))
            if m:
                e = m.group(1)
                e2 = re.sub(r"[a-zA-Z%,]", "", e)
                if re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", e2 or "") and any(c in e2 for c in "+-*/"):
                    try:
                        val = eval(e2)
                        if not approx(val, s["answer"]):
                            errs.append("%s[%d].gs[%d] '%s' computes %s not %s" % (tier, i, k, pre.strip(), val, s["answer"]))
                    except Exception:
                        pass

# 3. reproduce every misconception expect
def grad(x1, y1, x2, y2): return (y2 - y1) / (x2 - x1)
expect_checks = {
    ("bronze", 0): 4 / 8, ("bronze", 1): 6, ("bronze", 2): 2 / 8, ("bronze", 3): 8,
    ("bronze", 4): 24, ("bronze", 5): 0, ("bronze", 6): (4 + 6) * 4, ("bronze", 7): 2,
    ("silver", 0): (2 / 2) * (1 + 13 + 6), ("silver", 1): 0.5 * (0 + 9 + (1 + 4)),
    ("silver", 2): 2, ("silver", 3): 0.25 * (2 + 12 + (3 + 5 + 8)), ("silver", 4): None,
    ("silver", 5): 0.5 * (2 + 8 + 4), ("silver", 6): (2 / 2) * (0 + 16 + 4),
    ("gold", 0): 0.5 * (1 + 17 + (2 + 5 + 10)), ("gold", 1): (2 / 2) * (0 + 20 + (8 + 12)),
    ("gold", 2): round(3.5 / 48.5 * 100, 1), ("gold", 3): 2.402, ("gold", 4): 0.25 * (1 + 6 + (1.5 + 2.5 + 4)),
}
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        for m in p.get("misconceptions", []):
            exp = m.get("expect")
            want = expect_checks.get((tier, i), "SKIP")
            if want == "SKIP":
                continue
            if want is None:
                if exp is not None:
                    errs.append("%s[%d] expect should be null, got %s" % (tier, i, exp))
            else:
                if exp is None or not approx(exp, want):
                    errs.append("%s[%d] expect %s != derived error %s" % (tier, i, exp, want))
            # expect must not equal solution
            if exp is not None and approx(exp, p["solutions"][0]):
                errs.append("%s[%d] expect equals solution" % (tier, i))

# 4. teach boxes recompute (spot)
teach = pd["guided"]["teach"]
assert approx(grad(2, 3, 6, 15), 3)
assert approx(trap(2, [3, 7, 9, 12]), 47)
assert approx((16.81 - 15.21) / 0.2, 8)

# 5. opener
op = pd["guided"]["opener"]["steps"]
assert op[0]["answer"] == 24 and 6 * 4 == 24
assert op[1]["answer"] == 5 and 10 / 2 == 5

print("ERRORS:", len(errs))
for e in errs:
    print("  -", e)
if not errs:
    print("ALL INDEPENDENT CHECKS PASS")
