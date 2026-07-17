import json

# Build revised shard from LIVE data with the single surgical SVG fix.
pd = json.load(open("_geomL05ocr_live.json", encoding="utf-8"))

d = pd["guided"]["teach"]["gold"]["display"]

assert d.count(">?</text>") == 1
assert d.count("rise unknown") == 1

# 1. Label the given rise value 2 m instead of an unknown "?"
d = d.replace(">?</text>", ">2 m</text>")
# 2. aria-label: rise is given (2 m); only the angle theta remains unknown
d = d.replace(
    "horizontal run 9 m, rise unknown, angle theta unknown",
    "horizontal run 9 m, rise 2 m, angle theta unknown",
)

assert "rise unknown" not in d
assert "rise 2 m" in d
assert d.count("2 m</text>") == 1
# the theta label must survive unchanged
assert ">θ = ?</text>" in d

pd["guided"]["teach"]["gold"]["display"] = d

json.dump(pd, open("lesson_maths-ocr_geometry-L05.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("wrote shard. new display fragment:")
import re
print(d[:260])
