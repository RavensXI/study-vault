# -*- coding: utf-8 -*-
import json, io
pd=json.load(io.open("lesson_maths-eduqas_geometry-L03.json",encoding="utf-8"))
pb=pd["problem_bank"]
bad=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        gs=p.get("guided_steps") or []
        answers=[s["answer"] for s in gs if s.get("answer") is not None]
        # last answer box that carries a 'done' with the answer, or final live box
        landed = sol in answers
        if not landed:
            bad.append(f"{tier}[{i}] sol {sol} not among boxes {answers}")
        # expects must differ from sol
        for j,m in enumerate(p.get("misconceptions") or []):
            e=m.get("expect")
            if e is not None and abs(float(e)-float(sol))<0.011:
                bad.append(f"{tier}[{i}].mis[{j}] expect {e} == sol")
        # figure present?
        if "<svg" not in p["display"]:
            bad.append(f"{tier}[{i}] no figure")
        if "figure-caption" not in p["display"]:
            bad.append(f"{tier}[{i}] no caption")
# teach final boxes
for tier in ("bronze","silver","gold"):
    t=pd["guided"]["teach"][tier]
    nb=sum(1 for s in t["steps"] if s.get("answer") is not None)
    if nb<4: bad.append(f"teach.{tier} only {nb} boxes")
    if "<svg" not in t["display"]: bad.append(f"teach.{tier} no figure")
# opener
op=pd["guided"]["opener"]
if "<svg" not in op["display"]: bad.append("opener no figure")
print("PROBLEMS:", len(bad))
for b in bad: print("  -",b)
print("OK" if not bad else "FAIL")
