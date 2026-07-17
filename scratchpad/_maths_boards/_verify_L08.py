# -*- coding: utf-8 -*-
import json, io, re

live = json.load(io.open("_live_L08.json", encoding="utf-8"))
new = json.load(io.open("lesson_maths-aqa_geometry-L08.json", encoding="utf-8"))
errs = []

# 1. preservation
for k in ["related_videos", "topic_links", "worked_examples"]:
    if json.dumps(live.get(k), sort_keys=True) != json.dumps(new.get(k), sort_keys=True):
        errs.append(f"PRESERVATION changed: {k}")

# 2. tier sizes + input types preserved
for t in ["bronze", "silver", "gold"]:
    lo, nw = live["problem_bank"][t], new["problem_bank"][t]
    if len(lo) != len(nw):
        errs.append(f"{t} size changed {len(lo)}->{len(nw)}")
    for i, (a, b) in enumerate(zip(lo, nw)):
        if a.get("input_type") != b.get("input_type"):
            errs.append(f"{t}[{i}] input_type changed")

# 3. every guided_steps walk: last box present, phase boundary, >=2 live after
def check_walk(steps, label, sol=None):
    boxes = [s for s in steps if s.get("answer") is not None]
    if not boxes:
        errs.append(f"{label}: no boxes"); return
    sub = next((i for i, s in enumerate(steps) if s.get("phase") == "substitute"), None)
    if sub is None:
        errs.append(f"{label}: no substitute")
    else:
        live_after = sum(1 for s in steps[sub:] if s.get("answer") is not None)
        if live_after < 2:
            errs.append(f"{label}: <2 live after boundary ({live_after})")
    if sol is not None:
        vals = [float(b["answer"]) for b in boxes]
        if not any(abs(v - float(sol)) < 1e-9 for v in vals):
            errs.append(f"{label}: solution {sol} never reached in boxes {vals}")

for t in ["bronze", "silver", "gold"]:
    for i, p in enumerate(new["problem_bank"][t]):
        gs = p.get("guided_steps")
        if gs:
            sol = p["solutions"][0] if p.get("input_type") != "multiple_choice" else None
            check_walk(gs, f"{t}[{i}].guided_steps", sol)
        # misconception expect present + != correct
        for j, m in enumerate(p.get("misconceptions", [])):
            if "expect" not in m:
                errs.append(f"{t}[{i}].misc[{j}] no expect")
            e = m.get("expect")
            if e is not None and p.get("input_type") != "multiple_choice":
                if abs(float(e) - float(p["solutions"][0])) < 1e-9:
                    errs.append(f"{t}[{i}].misc[{j}] expect==answer")
            if e is not None and p.get("input_type") == "multiple_choice":
                if int(e) == int(p["solutions"][0]):
                    errs.append(f"{t}[{i}].misc[{j}] expect index==correct")
                if not (0 <= int(e) < len(p.get("options", []))):
                    errs.append(f"{t}[{i}].misc[{j}] expect index out of range")

# opener + teach walks
op = new["guided"]["opener"]["steps"]
if sum(1 for s in op if s.get("answer") is not None) < 1:
    errs.append("opener <1 box")
for t in ["bronze", "silver", "gold"]:
    tw = new["guided"]["teach"][t]["steps"]
    nb = sum(1 for s in tw if s.get("answer") is not None)
    if nb < 4:
        errs.append(f"teach.{t} has {nb} boxes (<4)")

# 4. figures: extract numbers from mag_fig SVGs and cross-check
def svg_texts(disp):
    return re.findall(r'>([^<>]+)</text>', disp)

# magnitude figures: legs should be |x|,|y| from the vector in display
checks = {
    ("bronze", 2): (5, 12), ("bronze", 5): (3, 4),
    ("silver", 4): (8, 6), ("silver", 6): (12, 5),
}
for (t, i), (x, y) in checks.items():
    disp = new["problem_bank"][t][i]["display"]
    labels = svg_texts(disp)
    nums = [l for l in labels if l.strip().lstrip('-').isdigit()]
    want = {str(x), str(y)}
    if not want.issubset(set(nums)):
        errs.append(f"{t}[{i}] figure labels {nums} missing {want}")

# 5. no em dash anywhere (double-check)
def scan(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            scan(v, path + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, path + f"[{i}]")
    elif isinstance(o, str) and "—" in o:
        errs.append(f"EM DASH at {path}")
scan(new, "pd")

# 6. spot-check a few fresh solves
def mag(x, y): return (x * x + y * y) ** 0.5
assert mag(5, 12) == 13 and mag(3, 4) == 5 and mag(8, 6) == 10 and mag(12, 5) == 13

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -", e)
else:
    print("VERIFY PASS: preservation, walks, expects, figures, style all clean")
print("silver single_value answers:", [p["solutions"] for p in new["problem_bank"]["silver"] if p.get("input_type") != "multiple_choice"])
print("gold single_value answers:", [p["solutions"] for p in new["problem_bank"]["gold"] if p.get("input_type") != "multiple_choice"])
print("bronze single_value answers:", [p["solutions"] for p in new["problem_bank"]["bronze"] if p.get("input_type") != "multiple_choice"])
