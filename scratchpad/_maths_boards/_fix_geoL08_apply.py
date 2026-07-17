# -*- coding: utf-8 -*-
import json, io

LIVE = "_chk_geoL08_live.json"
SHARD = "lesson_maths-eduqas_geometry-L08.json"

row = json.load(io.open(LIVE, encoding="utf-8"))
pd = row["practice_data"]

b5 = pd["problem_bank"]["bronze"][5]
mis0 = b5["misconceptions"][0]

# sanity: we are editing the exact defect
assert mis0["expect"] == 1, mis0
assert mis0["pattern"] == "forgot_scalar", mis0

old = dict(mis0)

# Relabel so the message honestly names the error that actually yields (5,5):
# the scalar was applied to ONLY the bottom component.
# x: 1 + 4 = 5 (top undoubled); y: 2*3 + (-1) = 5 (bottom doubled).
mis0["pattern"] = "partial_scalar"
mis0["message"] = ("The scalar doubles BOTH parts of the vector. You doubled only the bottom: "
                   "2 × (1, 3) = (2, 6), so the answer is (2+4, 6−1) = (6, 5).")
# expect stays 1 (option (5,5)) which is exactly what this error produces.

# write shard = raw practice_data
with io.open(SHARD, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

print("EDITED bronze[5].misconceptions[0]")
print("  old pattern:", old["pattern"], "| old expect:", old["expect"])
print("  old message:", old["message"])
print("  new pattern:", mis0["pattern"], "| new expect:", mis0["expect"])
print("  new message:", mis0["message"])
print("wrote", SHARD)
