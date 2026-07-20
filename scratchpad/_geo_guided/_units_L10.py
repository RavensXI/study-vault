# -*- coding: utf-8 -*-
"""Add answer units to Geography Skills L10 (Fieldwork Data & Sampling)."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_UNIT_L10_live.json"), encoding="utf-8"))
pb = pd["problem_bank"]

# (tier, index, unit)  -- matched by a display fingerprint so we cannot drift
UNITS = [
    ("bronze", 2, "m/s",       "River velocity readings"),
    ("silver", 0, "people",    "How many people should be sampled from Ward B"),
    ("silver", 3, "vehicles",  "Traffic count data at a junction"),
    ("silver", 4, "households", "how many households should be surveyed"),
    ("gold",   1, "m/s",       "What is the corrected mean if this reading is removed"),
    ("gold",   2, "people",    "how many middle-aged people should be surveyed"),
    ("gold",   3, "%",         "range as a percentage of the mean"),
]

before = json.dumps(pd, sort_keys=True, ensure_ascii=False)
added = 0
for tier, idx, unit, fp in UNITS:
    p = pb[tier][idx]
    assert fp in p["display"], (tier, idx, fp)
    assert p.get("input_type", "single_value") != "multiple_choice", (tier, idx)
    p["unit"] = unit
    added += 1

# nothing else may change
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        if p.get("input_type") == "multiple_choice":
            assert "unit" not in p, (tier, i)

after = json.loads(before)
for tier, idx, unit, fp in UNITS:
    after["problem_bank"][tier][idx]["unit"] = unit
assert json.dumps(after, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False)

out = os.path.join(HERE, "lesson_L10.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("units added:", added)
print("dimensionless left:", sum(1 for t in ("bronze", "silver", "gold")
                                 for p in pb[t] if "unit" not in p))
