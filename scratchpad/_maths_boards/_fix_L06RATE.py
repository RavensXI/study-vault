# -*- coding: utf-8 -*-
import json, io

SRC = "_L06RATE_live.json"
SHARD = "lesson_maths-aqa_ratio-proportion-L06.json"

live = json.load(io.open(SRC, encoding="utf-8"))
pd = live["practice_data"]

g1 = pd["problem_bank"]["gold"][1]
assert "f(1.5)" in g1["display"], g1["display"]
assert g1["solutions"] == [-0.625], g1["solutions"]

m = g1["misconceptions"][0]
assert m["pattern"] == "dropped_linear", m
old_expect = m["expect"]
old_msg = m["message"]

# Independent maths:
#   correct  f(1.5) = 1.5**3 + 2*1.5 - 7 = 3.375 + 3 - 7 = -0.625
#   dropped +2x term: 1.5**3 - 7 = 3.375 - 7 = -3.625
correct = 1.5**3 + 2*1.5 - 7
dropped = 1.5**3 - 7
assert abs(correct - (-0.625)) < 1e-9, correct
assert abs(dropped - (-3.625)) < 1e-9, dropped

MINUS = "−"  # U+2212, matches existing style
m["expect"] = -3.625
m["message"] = (
    f"{MINUS}3.625 forgets the +2x term. Put it back: "
    f"f(1.5) = 3.375 + 3 {MINUS} 7 = {MINUS}0.625."
)

# Write the shard = practice_data only (ship-gate + validator input)
with io.open(SHARD, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)

print("old expect:", old_expect, "-> new:", m["expect"])
print("old msg:", old_msg)
print("new msg:", m["message"])
print("dropped-term value recomputed:", dropped)
print("shard written:", SHARD)
