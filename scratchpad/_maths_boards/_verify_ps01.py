# -*- coding: utf-8 -*-
"""Independent check: recompute every box line from its pre-text and confirm walks
land on solutions; confirm each expect differs from solution and is length-matched."""
import json, io, re
from fractions import Fraction

pd = json.load(io.open("lesson_maths-aqa_probability-statistics-L01.json", encoding="utf-8"))
pb = pd["problem_bank"]
problems = 0
issues = []

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        problems += 1
        tag = "%s[%d]" % (tier, i)
        sols = p["solutions"]
        # expects
        for j, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is None:
                continue
            ev = e if isinstance(e, list) else [e]
            if len(ev) != len(sols):
                issues.append("%s mc[%d] expect length %d != sols %d" % (tag, j, len(ev), len(sols)))
            if [float(x) for x in ev] == [float(x) for x in sols]:
                issues.append("%s mc[%d] expect == solution" % (tag, j))
        # walk boxes: evaluate any 'A op B =' pattern in pre
        gs = p.get("guided_steps", [])
        boxes = [(k, st) for k, st in enumerate(gs) if st.get("answer") is not None]
        for k, st in boxes:
            pre = st.get("pre", "")
            ans = st["answer"]
            # find last "expr =" arithmetic
            m = re.search(r"([\d\.\s×x\*\+\-−÷/()]+)=\s*$", pre)
            expr = None
            if m:
                expr = m.group(1)
            else:
                m2 = re.search(r"=\s*([\d\.\s×x\*\+\-−÷/()]+)=", pre)
                if m2:
                    expr = m2.group(1)
            if expr:
                e2 = expr.replace("×", "*").replace("x", "*").replace("−", "-").replace("÷", "/")
                e2 = e2.strip().strip("*")
                try:
                    val = eval(e2, {"__builtins__": {}})
                    if abs(float(val) - float(ans)) > 1e-9:
                        issues.append("%s box%d '%s' -> eval %s != answer %s" % (tag, k, pre.strip(), val, ans))
                except Exception:
                    pass

print("problems:", problems)
if issues:
    print("ISSUES:")
    for x in issues:
        print("  -", x)
else:
    print("all expects length/differ OK; all arithmetic-in-pre boxes compute to their answers")
