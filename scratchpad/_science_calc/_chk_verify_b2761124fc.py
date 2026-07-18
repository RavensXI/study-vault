# -*- coding: utf-8 -*-
import json, re

pd = json.load(open("_chk_live_canonical.json", encoding="utf-8"))
pb = pd["problem_bank"]
issues = []

op = {"÷": lambda a,b: a/b, "×": lambda a,b: a*b, "−": lambda a,b: a-b, "+": lambda a,b: a+b}
pat = re.compile(r"(-?\d+(?:\.\d+)?)\s*([÷×−+])\s*(-?\d+(?:\.\d+)?)\s*=\s*$")

def check_walk(steps, path):
    for i, st in enumerate(steps):
        pre = st.get("pre","")
        ans = st.get("answer")
        if ans is None: continue
        m = pat.search(pre.strip())
        if m:
            a,o,b = float(m.group(1)), m.group(2), float(m.group(3))
            calc = op[o](a,b)
            if abs(calc - ans) > 0.005:
                issues.append(f"{path}[{i}] pre '{pre.strip()}' -> {calc} but answer={ans}")

for tier in ("bronze","silver","gold"):
    for pi, p in enumerate(pb[tier]):
        sols = p["solutions"]
        gs = p.get("guided_steps")
        if gs:
            check_walk(gs, f"{tier}[{pi}].guided_steps")
        for mi, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is not None:
                for s in sols:
                    if abs(float(e)-float(s)) < 0.011:
                        issues.append(f"{tier}[{pi}].misconceptions[{mi}] expect {e} == solution {s}")

for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], f"guided.teach.{tier}")
check_walk(pd["guided"]["opener"]["steps"], "guided.opener")

print("ISSUES:" if issues else "ALL BOX ARITHMETIC + EXPECT CHECKS CLEAN")
for x in issues: print(" -", x)
