# -*- coding: utf-8 -*-
import json, io
pd=json.load(io.open("lesson_algebra-L11.json",encoding="utf-8"))
pb=pd["problem_bank"]
issues=[]

# 1. confirm final live boxes of each guided_steps land on stored solution (for value problems)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[s for s in gs if s.get("answer") is not None]
        # last box should equal solution for single_value counting? not always (check step).
        # Instead just print the box answers for manual read
        vals=[b["answer"] for b in boxes]
        print(tier,i,p["input_type"],"sol",p["solutions"],"boxes",vals)

# 2. em dash scan already done by validator. Double-check pre/hint plain (no LaTeX backslash in pre/hint)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for j,s in enumerate((p.get("guided_steps") or [])):
            for f in ("pre","post","hint"):
                if f in s and "\(" in (s.get(f) or ""):
                    issues.append(f"{tier}[{i}].gs[{j}].{f} has LaTeX")
# opener + teach boxes
for j,s in enumerate(pd["guided"]["opener"]["steps"]):
    for f in ("pre","post","hint"):
        if f in s and "\(" in (s.get(f) or ""): issues.append(f"opener[{j}].{f} LaTeX")
for t in ("bronze","silver","gold"):
    for j,s in enumerate(pd["guided"]["teach"][t]["steps"]):
        for f in ("pre","post","hint"):
            if f in s and "\(" in (s.get(f) or ""): issues.append(f"teach.{t}[{j}].{f} LaTeX")

# 3. every problem has hint
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if not p.get("hint"): issues.append(f"{tier}[{i}] no hint")

print("\nISSUES:", issues if issues else "none")
