# -*- coding: utf-8 -*-
"""Independent re-verification of every chart reading quoted in L03 walks."""
import json, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L03.json"), encoding="utf-8"))

def pts(p):
    return {d["x"]: d["y"] for d in p["chart"]["data"]["datasets"][0]["data"]}

pb = pd["problem_bank"]
checks = [
    ("bronze", 0, [(2000, 55), (50000, 82), (20000, 75)]),
    ("bronze", 2, [(32, 380), (25, 300), (30, 50), (28, 320)]),
    ("bronze", 3, [(1, 450), (15, 160), (7, 250)]),
    ("bronze", 5, [(35, 16), (45, 20)]),
    ("bronze", 7, [(22000, 76)]),
    ("silver", 0, [(10, 8), (400, 30), (100, 16)]),
    ("silver", 1, [(22, 32), (28, 45)]),
    ("silver", 3, [(0, 0.3), (25, 1.5), (12, 1.1)]),
    ("silver", 5, [(30, 20), (40, 15)]),
    ("gold", 0, [(65000, 35), (60000, 14), (2000, 1)]),
    ("gold", 2, [(40, 42), (99, 9), (70, 25)]),
    ("gold", 4, [(40, 7), (50, 10)]),
]
bad = 0
for tier, i, pairs in checks:
    d = pts(pb[tier][i])
    for x, y in pairs:
        got = d.get(x)
        if got != y:
            print("MISMATCH %s[%d] x=%s expected %s got %s" % (tier, i, x, y, got))
            bad += 1
print("chart readings checked:", sum(len(c[2]) for c in checks), "mismatches:", bad)

# counting checks
b7 = pts(pb["bronze"][7])
n_pass = sum(1 for x, y in b7.items() if x > 20000 and y > 75)
print("b7 pass count:", n_pass, "total:", len(b7), "fail:", len(b7) - n_pass)
g0 = pts(pb["gold"][0])
print("g0 points:", len(g0), "trend points:", len(g0) - 1, "max-1:", 14 - 1)
b2 = pts(pb["bronze"][2])
print("b2 points:", len(b2))

# arithmetic in walks
arith = [
    (82 - 55, 27), (15 - 3, 12), ((15 + 3) / 2, 9), (450 - 160, 290),
    (16 + 20, 36), (36 / 2, 18), (18 - 16, 2),
    (30 - 8, 22), (32 + 45, 77), (77 / 2, 38.5), (round(38.5), 39),
    (1.5 - 0.3, 1.2), (20 + 15, 35), (35 / 2, 17.5),
    (35 - 14, 21), (14 - 1, 13), (42 - 9, 33), (7 + 10, 17), (17 / 2, 8.5),
    (1200 - 800, 400), (5 + 6, 11), (11 / 2, 5.5), (5.5 - 1, 4.5), (8 - 2, 6),
    (130 + 100, 230), (230 / 2, 115), (130 - 115, 15), (12 - 7, 5),
]
for got, want in arith:
    if abs(got - want) > 1e-9:
        print("ARITH FAIL", got, want)
print("arithmetic checked:", len(arith))

# rounding convention: 38.5 -> 39 (half up), 17.5 -> 18, 8.5 -> 9
print("solutions:", {t: [p["solutions"] for p in pb[t]] for t in ("bronze", "silver", "gold")})
# no surviving check keys
n = 0
for t in ("bronze", "silver", "gold"):
    for p in pb[t]:
        for m in p.get("misconceptions", []):
            n += 1
            assert "check" not in m, (t, m)
            assert "expect" in m
print("misconceptions:", n, "all expect-matched")
