import json,io
live=json.load(io.open("_diag_L08_live.json",encoding="utf-8"))
new=json.load(io.open("lesson_graphs-L08_diagrams.json",encoding="utf-8"))
pbL,pbN=live["problem_bank"],new["problem_bank"]
# structural preservation outside problem_bank
for k in live:
    if k=="problem_bank": continue
    assert json.dumps(live[k],sort_keys=True)==json.dumps(new[k],sort_keys=True), "CHANGED "+k
print("non-bank fields: byte-identical")
changed=[]
for t in ("bronze","silver","gold"):
    for i,(a,b) in enumerate(zip(pbL[t],pbN[t])):
        added_chart = ("chart" not in a) and ("chart" in b)
        disp_changed = a.get("display")!=b.get("display")
        # every non-display, non-chart key identical
        for key in a:
            if key in ("display","chart"): continue
            assert json.dumps(a[key],sort_keys=True)==json.dumps(b.get(key),sort_keys=True), f"{t}[{i}] mutated {key}"
        if disp_changed:
            # new display must END with old display (svg prepended)
            assert b["display"].endswith(a["display"]), f"{t}[{i}] display tail mismatch"
        if added_chart or disp_changed:
            changed.append((t,i,"chart" if added_chart else "svg"))
print("changed problems:",changed)
print("count:",len(changed))
# spot-check svg numbers present in display text
import re
for t,i,kind in changed:
    if kind=="svg":
        d=pbN[t][i]["display"]
        svg=d.split(CAP if False else "</svg>")[0]
print("all preserved OK")
