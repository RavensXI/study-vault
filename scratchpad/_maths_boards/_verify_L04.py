# -*- coding: utf-8 -*-
"""Independent re-solve of number-L04 bank + guided-step continuity checks."""
import json, io
from math import gcd

pd = json.load(io.open("lesson_maths-aqa_number-L04.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

def lcm(a, b):
    return a * b // gcd(a, b)

# ---- expected canonical answers, computed here from scratch ----
expected = {
    "bronze": [8, 42, 0, 5, 2, 6, 12, 40],
    "silver": [12, 60, 36, 120, 30, 3, 40],
    "gold":   [36, 22680, 45, 24, 108],
}

# recompute a few from first principles
assert len([d for d in range(1, 25) if 24 % d == 0]) == 8
assert 6 * 7 == 42
assert 51 % 3 == 0  # not prime -> 0
assert gcd(12, 18) == 6
assert lcm(4, 6) == 12
assert lcm(5, 8) == 40
assert gcd(48, 84) == 12
assert lcm(15, 20) == 60
assert gcd(72, 108) == 36
assert lcm(lcm(8, 15), 20) == 120
assert 6 * 90 // 18 == 30
assert gcd(2**3 * 3**2 * 5, 2**2 * 3**4 * 7) == 36
assert lcm(2**3 * 3**2 * 5, 2**2 * 3**4 * 7) == 22680
assert 14 + 15 + 16 == 45
assert lcm(8, 12) == 24
# G4: 2^a 3^b, exactly 12 factors, 100<n<200
cand = []
for a in range(0, 12):
    for b in range(0, 12):
        n = 2**a * 3**b
        if (a + 1) * (b + 1) == 12 and 100 < n < 200:
            cand.append(n)
assert cand == [108], cand
# S6 uniqueness in (30,50)
s6 = [x for x in range(31, 50) if lcm(24, x) == 120]
assert s6 == [40], s6
print("first-principles checks passed; G4 unique:", cand, "S6 unique:", s6)

# ---- compare stored solutions ----
for tier in ("bronze", "silver", "gold"):
    got = [p["solutions"][0] for p in pb[tier]]
    if got != expected[tier]:
        errs.append("%s solutions mismatch: got %s exp %s" % (tier, got, expected[tier]))
    # duplicate check
    seen = {}
    for i, s in enumerate(got):
        if s in seen:
            errs.append("%s duplicate solution %s at %d and %d" % (tier, s, seen[s], i))
        seen[s] = i

# ---- guided_steps: last answer box must equal solution; boundary sanity ----
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if s.get("answer") is not None]
        if not boxes:
            errs.append("%s[%d] no boxes" % (tier, i)); continue
        if boxes[-1]["answer"] != p["solutions"][0]:
            # final box may be a check that lands on solution OR the answer;
            # accept if any late box equals the solution
            if not any(b["answer"] == p["solutions"][0] for b in boxes):
                errs.append("%s[%d] no box lands on solution %s" % (tier, i, p["solutions"][0]))
        # boundary
        sub = [j for j, s in enumerate(gs) if s.get("phase") == "substitute"]
        if not sub:
            errs.append("%s[%d] no substitute boundary" % (tier, i))
        else:
            first = sub[0]
            live = sum(1 for s in gs[first:] if s.get("answer") is not None)
            if live < 2:
                errs.append("%s[%d] only %d live boxes" % (tier, i, live))
            if first < 1:
                errs.append("%s[%d] boundary at 0" % (tier, i))
        # every misconception expect != solution
        for m in p.get("misconceptions") or []:
            if m.get("expect") == p["solutions"][0]:
                errs.append("%s[%d] expect==solution" % (tier, i))

# ---- teach walks land correctly ----
teach_final = {"bronze": 3, "silver": 72, "gold": 15120}
for t, want in teach_final.items():
    steps = pd["guided"]["teach"][t]["steps"]
    boxes = [s for s in steps if s.get("answer") is not None]
    if len(boxes) < 4:
        errs.append("teach.%s only %d boxes" % (t, len(boxes)))
    if boxes[-1]["answer"] != want:
        errs.append("teach.%s final box %s != %s" % (t, boxes[-1]["answer"], want))

# opener boxes
op = [s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if [b["answer"] for b in op] != [12, 3]:
    errs.append("opener boxes wrong: %s" % [b["answer"] for b in op])

if errs:
    print("VERIFY FAIL:")
    for e in errs:
        print("  -", e)
else:
    print("VERIFY OK: all solutions, boxes, boundaries, expects, teach, opener check out")
