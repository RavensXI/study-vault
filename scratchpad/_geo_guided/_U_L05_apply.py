# -*- coding: utf-8 -*-
import json, io

SRC = "_U_L05_live.json"
OUT = "lesson_L05.json"

UNITS = {
    ("bronze", 0): "°C",
    ("bronze", 1): "m",
    ("bronze", 3): "mm",
    ("bronze", 4): "vehicles",
    ("bronze", 5): "thousands",
    ("bronze", 7): "km/h",
    ("silver", 0): "cm",
    ("silver", 1): "°C",
    ("silver", 2): "m/s",
    ("silver", 5): "mm",
    ("gold", 0): "m",
}

CLARIFY = {
    ("bronze", 5): " Give your answer in thousands, matching the chart axis.",
}

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

added = 0
for (tier, idx), unit in UNITS.items():
    p = pb[tier][idx]
    assert p.get("input_type") != "multiple_choice", (tier, idx)
    p["unit"] = unit
    added += 1

for (tier, idx), extra in CLARIFY.items():
    p = pb[tier][idx]
    if extra.strip() not in p["display"]:
        p["display"] = p["display"].rstrip() + extra

io.open(OUT, "w", encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1)
)
total = sum(len(pb[t]) for t in ("bronze", "silver", "gold"))
print("units added:", added, "of", total, "problems")
