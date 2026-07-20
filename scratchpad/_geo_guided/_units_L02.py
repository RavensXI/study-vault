# -*- coding: utf-8 -*-
"""Add answer units to Geography Skills L02 (Pie Charts & Histograms)."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "_U02_live.json")
OUT = os.path.join(HERE, "lesson_L02.json")

UNITS = {
    ("bronze", 0): "%",
    ("bronze", 1): "degrees",
    ("bronze", 2): "%",
    ("bronze", 3): "tourists",
    ("bronze", 4): "degrees",
    ("bronze", 5): "%",
    ("bronze", 6): "billion litres",
    ("bronze", 7): "days",
    ("silver", 0): "people",
    ("silver", 1): "degrees",
    ("silver", 2): "dunes",
    ("silver", 3): "degrees",
    ("silver", 4): "events",
    ("silver", 5): "measurements",
    ("silver", 6): "percentage points",
    # gold 0 is multiple_choice -> never a unit
    ("gold", 1): "people",
    ("gold", 2): "degrees",
    ("gold", 3): "migrants",
    ("gold", 4): "pebbles",
}

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]
added = 0
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        u = UNITS.get((tier, i))
        if u is None:
            continue
        assert (p.get("input_type") or "single_value") != "multiple_choice", (tier, i)
        p["unit"] = u
        added += 1

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("units added:", added)
