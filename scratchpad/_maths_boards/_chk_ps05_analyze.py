# -*- coding: utf-8 -*-
import json, re

live = json.load(open("_chk_ps05_live.json", encoding="utf-8"))

# 1. Em dash sweep in student-facing strings (exclude internal 'note')
EMDASH = "—"
def walk(obj, path=""):
    hits=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k == "note":  # internal exempt
                continue
            hits += walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            hits += walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EMDASH in obj:
            hits.append((path, obj[:80]))
    return hits
em = walk(live)
print("EM DASHES:", len(em))
for p,s in em: print("  ", p, repr(s))

# 2. Non-numeric guided_steps box answers
def check_boxes(steps, tag):
    probs=[]
    for i,s in enumerate(steps):
        if "answer" in s:
            a=s["answer"]
            if not isinstance(a,(int,float)):
                probs.append((f"{tag}[{i}]", a))
    return probs
allbox=[]
for tier in ["gold","bronze","silver"]:
    for j,prob in enumerate(live["problem_bank"][tier]):
        gs=prob.get("guided_steps",[])
        allbox+=check_boxes(gs, f"{tier}[{j}].guided_steps")
for tier in ["gold","bronze","silver"]:
    t=live["guided"]["teach"][tier]
    allbox+=check_boxes(t["steps"], f"teach.{tier}.steps")
allbox+=check_boxes(live["guided"]["opener"]["steps"], "opener.steps")
print("NON-NUMERIC BOXES:", allbox)

# 3. tier_guides word budget (<=115 words steps)
for tier in ["gold","bronze","silver"]:
    tg=live["tier_guides"][tier]
    words=sum(len(re.sub("<[^>]+>","",s).split()) for s in tg["steps"])
    print(f"tier_guides.{tier} steps words:", words, "OK" if words<=115 else "OVER115")

# 4. hint plain text (no LaTeX/HTML)
for tier in ["gold","bronze","silver"]:
    for j,prob in enumerate(live["problem_bank"][tier]):
        h=prob.get("hint","")
        if "\\(" in h or "<" in h:
            print("HINT markup:", f"{tier}[{j}]", h)
print("hint check done")
