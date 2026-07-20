# -*- coding: utf-8 -*-
import json, os, copy

BASE = os.path.dirname(os.path.abspath(__file__))
live = json.load(open(os.path.join(BASE, "_chk_L07_live.json"), encoding="utf-8"))
d = copy.deepcopy(live)
pb = d["problem_bank"]

changes = []

# --- FIX 1 (fail): gold[4] under-specified rounding ---
g4 = pb["gold"][4]
old = g4["display"]
assert g4["solutions"] == [20.8], g4["solutions"]
assert old.endswith("natural increase rate?")
g4["display"] = old + " Give your answer to 1 decimal place."
changes.append({"tier": "gold", "index": 4, "what": "display: added explicit rounding instruction (exact value 20.8333%, stored solution 20.8, marker tolerance 0.01)",
                "old": old, "new": g4["display"]})

# --- FIX 2 (nit): gold[2] walk hints assert unreadable precision ---
g2 = pb["gold"][2]
s2, s3 = g2["guided_steps"][2], g2["guided_steps"][3]
old2, old3 = s2["hint"], s3["hint"]
s2["hint"] = "Nigeria's 2020 bar is the blue one in her pair; hover or tap it to read its exact value in millions."
s3["hint"] = "It is the red bar beside it in the same pair; hover or tap that one to read its value."
changes.append({"tier": "gold", "index": 2, "what": "guided_steps[2].hint + [3].hint: stopped claiming the value is readable off gridlines marked every 200; point at the bar's own tooltip instead",
                "old": [old2, old3], "new": [s2["hint"], s3["hint"]]})

# --- FIX 3 (nit): silver[3] degenerate check step ---
s3p = pb["silver"][3]
oldstep = copy.deepcopy(s3p["guided_steps"][5])
s3p["guided_steps"][5] = {
    "pre": "Check: 4 × 25 ha = ",
    "post": " ha",
    "answer": 100,
    "hint": "Your percentage makes commercial a quarter of the land, so put four commercial-sized plots together.",
    "done": "Four commercial plots exactly fill the total land area, which is what a quarter means."
}
changes.append({"tier": "silver", "index": 3, "what": "guided_steps[5]: replaced a check that reproduced the percentage as its own hectare figure (0.25 × 100 ha = 25) with one that runs the quarter forward onto the 100 ha total",
                "old": oldstep, "new": s3p["guided_steps"][5]})

# --- FIX 4 (nit): silver[0] completion boundary sat after both chart readings ---
s0 = pb["silver"][0]
steps = s0["guided_steps"]
assert steps[4].pop("phase") == "substitute"
steps[2]["phase"] = "substitute"
changes.append({"tier": "silver", "index": 0, "what": "completion boundary moved from guided_steps[4] to guided_steps[2]: locating the Primary series stays pre-worked, both bar readings plus the subtraction and the check are now live (4 boxes, was 2)",
                "old": "phase:substitute on guided_steps[4]", "new": "phase:substitute on guided_steps[2]"})

out = os.path.join(BASE, "lesson_L07.json")
json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(changes, open(os.path.join(BASE, "_repair_L07_changes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# integrity: stimulus + preserved fields untouched
import hashlib
def blob(o): return json.dumps(o, sort_keys=True, ensure_ascii=False)
for f in ("related_videos", "topic_links", "worked_examples", "method_card", "tier_guides", "guided"):
    assert blob(live.get(f)) == blob(d.get(f)), f
for t in ("bronze", "silver", "gold"):
    for i, (a, b) in enumerate(zip(live["problem_bank"][t], pb[t])):
        for f in ("chart", "image", "ruler", "options", "solutions", "input_type"):
            assert blob(a.get(f)) == blob(b.get(f)), (t, i, f)
print("integrity OK; %d changes" % len(changes))
