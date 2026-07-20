# -*- coding: utf-8 -*-
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, "_L08_orig.json")
dst = os.path.join(HERE, "lesson_L08.json")

UNITS = {
    ("silver", 0): "°C",
    ("silver", 2): "mb",
    ("silver", 5): "°C",
    ("gold", 0): "mm",
    ("gold", 2): "mb per 100 km",
    ("gold", 3): "°C",
}

pd = json.load(io.open(src, encoding="utf-8"))
pb = pd["problem_bank"]
n = 0
for (tier, i), u in UNITS.items():
    p = pb[tier][i]
    assert p["input_type"] != "multiple_choice", (tier, i)
    p["unit"] = u
    n += 1
print("units added:", n)
io.open(dst, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
