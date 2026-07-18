import json
pd=json.load(open("_RVW_canonical.json",encoding="utf-8"))
def rep(steps,label):
    sub=None; live=0; pre_boxes=0; boxes=0
    for i,st in enumerate(steps):
        b=st.get("answer") is not None
        if b: boxes+=1
        if st.get("phase")=="substitute" and sub is None: sub=i
    if sub is not None:
        pre_boxes=sum(1 for st in steps[:sub] if st.get("answer") is not None)
        live=sum(1 for st in steps[sub:] if st.get("answer") is not None)
    print(f"{label}: boxes={boxes} sub_at={sub} preworked={pre_boxes} live={live}")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("guided_steps"): rep(p["guided_steps"],f"{tier}[{i}]")
for tier in ("bronze","silver","gold"):
    rep(pd["guided"]["teach"][tier]["steps"],f"teach.{tier}")
# rounded fraction boxes
print("14/101 =",14/101,"-> box 0.139, true%",14/101*100)
print("16/18 =",16/18,"-> box 0.889, true%",16/18*100)
