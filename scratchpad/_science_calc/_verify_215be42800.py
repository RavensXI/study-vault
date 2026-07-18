# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_physics-calculations-L03@215be42800.json", encoding="utf-8"))
issues=[]
# expected fresh solutions
exp = {
 "bronze":[2,30,60,20,24,1.5,1,12],
 "silver":[6,8,2,4,300,1],
 "gold":[1.5,9,12,4,10,120],
}
pb=pd["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,pr in enumerate(pb[t]):
        sol=pr["solutions"]
        if pr.get("input_type")=="multiple_choice":
            # bronze index 6 -> answer index 1
            if sol!=[1]: issues.append(f"{t}[{i}] MC sol {sol}")
            continue
        want=exp[t][i]
        if abs(sol[0]-want)>1e-9: issues.append(f"{t}[{i}] sol {sol} != fresh {want}")
        # expects outside accept
        acc=pr.get("accept",0)
        for j,m in enumerate(pr.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None:
                ev=e[0] if isinstance(e,list) else e
                if abs(ev-sol[0])<=acc+1e-9:
                    issues.append(f"{t}[{i}].mc[{j}] expect {ev} inside accept of {sol[0]} (acc {acc})")
        # guided_steps final boxes land on sol; and every box has numeric answer
        gs=pr.get("guided_steps")
        if gs:
            boxes=[st for st in gs if st.get("answer") is not None]
            last=boxes[-1]["answer"]  # check box
            # ensure at least one box equals the solution value
            if not any(abs(bx["answer"]-sol[0])<1e-9 for bx in boxes):
                issues.append(f"{t}[{i}] no guided box equals solution {sol[0]}")
# recompute specific box arithmetic for a sample of walks
def approx(a,b): return abs(a-b)<1e-9
# check opener boxes
op=[st for st in pd["guided"]["opener"]["steps"] if st.get("answer") is not None]
if [b["answer"] for b in op]!=[2,3]: issues.append("opener boxes changed")
# teach walks land on their stated answers
teach_finals={"bronze":3,"silver":1000,"gold":3}
for t,fin in teach_finals.items():
    boxes=[st for st in pd["guided"]["teach"][t]["steps"] if st.get("answer") is not None]
    if not any(approx(b["answer"],fin) for b in boxes):
        issues.append(f"teach {t} missing final {fin}")
    if len(boxes)<4: issues.append(f"teach {t} <4 boxes")
# figures present on topology problems
figs=[("bronze",3),("silver",1),("silver",2),("silver",3),("gold",0),("gold",1)]
for t,i in figs:
    if "<svg" not in pb[t][i]["display"]: issues.append(f"{t}[{i}] missing svg")
# figure label sanity: gold svg must contain 24 V,10,8,24
gsvg=pb["gold"][0]["display"]
for lab in ["24 V","10 &#937;","8 &#937;","24 &#937;"]:
    if lab not in gsvg: issues.append(f"gold svg missing label {lab}")
print("ISSUES:", len(issues))
for x in issues: print("  -",x)
print("title:", pd["method_card"]["title"])
