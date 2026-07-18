# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("lesson_physics-calculations-L07@003464e169.json", encoding="utf-8"))
issues = []

# 1. board neutrality
BOARDS = ["AQA", "Edexcel", "OCR", "Eduqas", "WJEC", "equation sheet", "you must memorise", "on your sheet"]
blob = json.dumps(pd, ensure_ascii=False)
for term in BOARDS:
    if term.lower() in blob.lower():
        issues.append("board/sheet term found: " + term)

# 2. em dash
if "—" in blob:
    issues.append("em dash present")

# 3. per-problem: last computational (non-check) box + solution sanity; expects outside solution
def last_numeric(steps):
    vals = [st["answer"] for st in steps if st.get("answer") is not None]
    return vals

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        gs = p.get("guided_steps", [])
        boxes = [st for st in gs if st.get("answer") is not None]
        # find the phase:substitute compute box: the first live numeric box at/after boundary that isn't the check
        # simpler: ensure the solution value appears as some box answer OR check returns a known value
        answers = [b["answer"] for b in boxes]
        if sol not in answers:
            issues.append(f"{tier}[{i}] solution {sol} not hit by any guided box; answers={answers}")
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(float(e) - float(sol)) < 0.011:
                issues.append(f"{tier}[{i}] expect {e} == solution {sol}")

# 4. recompute specific walk arithmetic
checks = {
    "bronze0": (540/60, 9), "bronze1": (25*40, 1000), "bronze2": (30/6, 5),
    "bronze3": (24/4, 6), "bronze4": (10*3, 30), "bronze5": (90/3.6, 25),
    "silver0": ((25-5)/8, 2.5), "silver1": (0.5*10*20, 100), "silver2": (20*20, 400),
    "silver3": (30/5, 6), "silver4": (0.5*10*30+20*30+0.5*5*30, 825),
    "gold0": (abs((0-400)/100), 4), "gold1": ((2*10*45)**0.5, 30),
    "gold2": (0.5*5*25+10*25+0.5*5*25, 375),
}
for k, (calc, expect) in checks.items():
    if abs(calc - expect) > 1e-9:
        issues.append(f"arithmetic {k}: {calc} != {expect}")

# 5. teach walks final answers
# bronze teach 400/50=8; silver 72/3.6=20,20/5=4; gold 2*4*18=144, sqrt=12
assert 400/50 == 8 and 72/3.6 == 20 and 20/5 == 4 and (2*4*18)**0.5 == 12

# 6. higher_only flags on v2=u2+2as gold
for i in (0, 1):
    if not pd["problem_bank"]["gold"][i].get("higher_only"):
        issues.append(f"gold[{i}] should be higher_only")

# 7. tier guide word budgets
def words(s): return len(s.replace("\\("," ").replace("\\)"," ").split())
for tier in ("bronze","silver","gold"):
    tot = sum(words(x) for x in pd["tier_guides"][tier]["steps"])
    if tot > 115: issues.append(f"tier_guide {tier} words {tot} > 115")

# 8. method_card word budget
mc = re.sub("<[^>]+>", " ", pd["method_card"]["content"])
if len(mc.split()) > 140: issues.append("method_card content > 140 words")

print("ISSUES:" if issues else "ALL CLEAN")
for x in issues:
    print("  -", x)
