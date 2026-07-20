# -*- coding: utf-8 -*-
"""Independent re-solve of every L06 problem + spot-check of walk endpoints."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L06.json"), encoding="utf-8"))


def med(v):
    v = sorted(v); n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def quarts(v):
    v = sorted(v); n = len(v)
    lo, hi = (v[:n // 2], v[n // 2 + 1:]) if n % 2 else (v[:n // 2], v[n // 2:])
    return med(lo), med(v), med(hi)


checks = []
D = {
    ("bronze", 0): (med([4, 7, 10, 14, 18, 21, 23]),),
    ("bronze", 1): (quarts([0.3, 0.5, 0.8, 1.1, 1.4, 1.7, 2.0])[0],),
    ("bronze", 2): (quarts([620, 740, 850, 910, 1050])[2],),
    ("bronze", 3): (quarts([3, 8, 12, 19, 25, 34, 51])[2] - quarts([3, 8, 12, 19, 25, 34, 51])[0],),
    ("bronze", 4): (quarts([15, 28, 42, 55, 63, 78, 91, 110, 135])[0],),
    ("bronze", 5): (29 - 19,),
    ("bronze", 6): (quarts([52, 61, 67, 73, 78, 84, 91])[2],),
    ("bronze", 7): (quarts([8, 12, 15, 18, 22, 25, 31])[2] - quarts([8, 12, 15, 18, 22, 25, 31])[0],),
}
sd = [2.4, 3.1, 3.8, 4.5, 5.2, 5.9, 6.6, 7.3, 8.0, 8.7, 9.4]
gdp = [1200, 2800, 4500, 7300, 11500, 18200, 29000, 42000]
tmp = [5, 6, 8, 10, 13, 16, 18, 17, 15, 12, 8, 6]
eq = [4, 6, 7, 9, 10, 12, 13, 15, 16, 18]
D[("silver", 0)] = (round(quarts(sd)[2] - quarts(sd)[0], 10),)
D[("silver", 1)] = (quarts(gdp)[0],)
D[("silver", 2)] = (1,)
D[("silver", 3)] = (quarts(tmp)[2],)
D[("silver", 4)] = (31 - 18,)
D[("silver", 5)] = (1,)
D[("silver", 6)] = (quarts(eq)[2] - quarts(eq)[0],)
hdi = [0.35, 0.41, 0.48, 0.52, 0.58, 0.63, 0.69, 0.74, 0.80, 0.85, 0.91, 0.95]
ph = [4.2, 4.5, 4.8, 5.1, 5.3, 5.6, 5.8, 6.0, 6.3, 6.5, 6.8, 7.1, 7.4]
tour = [1.2, 2.4, 3.6, 4.8, 7.5, 9.1, 10.3, 12.7, 15.8]
mig = [-45, -20, -8, 5, 12, 25, 38, 52, 71, 95, 120]
q1t, _, q3t = quarts(tour)
q1m, m2m, q3m = quarts(mig)
D[("gold", 0)] = (round((3.6 - 1.5) - (3.2 - 2.0), 10),)
D[("gold", 1)] = (quarts(hdi)[2],)
D[("gold", 2)] = (round(quarts(ph)[2] - quarts(ph)[0], 10),)
D[("gold", 3)] = (round(q3t + 1.5 * (q3t - q1t), 10),)
D[("gold", 4)] = (round(m2m / (q3m - q1m) * 100, 1),)

bad = 0
for (tier, i), expect in D.items():
    stored = pd["problem_bank"][tier][i]["solutions"]
    ok = all(abs(float(a) - float(b)) < 1e-9 for a, b in zip(stored, expect))
    if not ok:
        bad += 1
        print("MISMATCH", tier, i, "stored", stored, "recomputed", list(expect))
print("solutions checked:", len(D), "mismatches:", bad)

# expects must never equal solutions, and must be numeric
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        for j, m in enumerate(p.get("misconceptions") or []):
            assert "check" not in m, (tier, i, j)
            assert "expect" in m and "pattern" in m and m.get("message")
            if m["expect"] is not None:
                assert float(m["expect"]) != float(p["solutions"][0]), (tier, i, j)
        # final box lands on the solution for single_value problems
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if s.get("answer") is not None]
        vals = [s["answer"] for s in boxes]
        if p.get("input_type") != "multiple_choice":
            assert any(abs(float(v) - float(p["solutions"][0])) < 1e-9 for v in vals), (tier, i, vals)
print("misconception + walk-endpoint checks OK")

# arithmetic spot checks inside walks
assert 910 + 1050 == 1960
assert 28 + 42 == 70
assert 2800 + 4500 == 7300
assert 15 + 16 == 31
assert round(0.80 + 0.85, 10) == 1.65
assert (2.4 + 3.6) / 2 == 3.0 and (10.3 + 12.7) / 2 == 11.5
assert round(11.5 + 1.5 * 8.5, 10) == 24.25
assert (4.8 + 5.1) / 2 == 4.95 and (6.5 + 6.8) / 2 == 6.65
assert 71 - (-8) == 79 and round(25 / 79 * 100, 1) == 31.6
assert (21 + 23) / 2 == 22 and (28 + 30) / 2 == 29 and 29 - 22 == 7
print("walk arithmetic OK")
