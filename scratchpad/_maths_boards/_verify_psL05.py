# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("lesson_maths-ocr_probability-statistics-L05.json", encoding="utf-8"))
bad = []

# normalise unicode operators to python
def ev(expr):
    e = expr.replace("−", "-").replace("×", "*").replace("÷", "/").replace("½", "0.5").replace("¼", "0.25").replace("¾", "0.75")
    return eval(e, {"__builtins__": {}})

# 1. check every box: last "<arith> = " chunk in pre must equal answer
def check_box(path, st):
    if st.get("answer") is None:
        return
    pre = st.get("pre", "")
    # find arithmetic just before final "= "
    m = re.search(r'([0-9.+\-*/×÷−()\s]+?)\s*=\s*$', pre)
    if m:
        chunk = m.group(1).strip()
        # strip leading words: keep only trailing pure-arithmetic
        m2 = re.search(r'([0-9.][0-9.+\-*/×÷−()\s]*)$', chunk)
        if m2:
            expr = m2.group(1).strip()
            try:
                val = ev(expr)
                if abs(val - st["answer"]) > 1e-9:
                    bad.append("%s: '%s' = %s but answer=%s" % (path, expr, val, st["answer"]))
            except Exception as e:
                pass  # non-arithmetic pre (e.g. 'n = ')

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        path = "%s[%d]" % (tier, i)
        sols = tuple(p["solutions"])
        if p.get("input_type") != "multiple_choice":
            if sols in seen:
                bad.append("%s duplicate solution %s (also %s)" % (path, sols, seen[sols]))
            seen[sols] = path
        for j, st in enumerate(p.get("guided_steps", [])):
            check_box(path + ".gs[%d]" % j, st)
        # last numeric box in guided_steps should be checkable; ensure a box hits the solution
        boxes = [st["answer"] for st in p.get("guided_steps", []) if st.get("answer") is not None]
        if boxes and p.get("input_type") != "multiple_choice":
            if not any(abs(b - p["solutions"][0]) < 1e-9 for b in boxes):
                bad.append("%s: no guided box lands on solution %s (boxes=%s)" % (path, p["solutions"], boxes))
        # expect must not equal solution; and be a plausible number/null
        for k, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is not None and abs(float(e) - float(p["solutions"][0])) < 1e-9:
                bad.append("%s.mc[%d] expect==solution" % (path, k))

# teach + opener boxes
for st in pd["guided"]["opener"]["steps"]:
    check_box("opener", st)
for tier in ("bronze", "silver", "gold"):
    for j, st in enumerate(pd["guided"]["teach"][tier]["steps"]):
        check_box("teach.%s[%d]" % (tier, j), st)

print("PROBLEMS FOUND:" if bad else "ALL BOX ARITHMETIC + SOLUTIONS + EXPECTS CLEAN")
for b in bad:
    print("  -", b)
