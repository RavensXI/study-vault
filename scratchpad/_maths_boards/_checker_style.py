import json, re
live = json.load(open("_live_L01.json", encoding="utf-8"))
s = json.dumps(live, ensure_ascii=False)
# em dash sweep (exclude internal note fields - there are none here)
print("em dash U+2014 count:", s.count("—"))
print("en dash U+2013 count:", s.count("–"))
# scan for HTML entities in plain-text pre/post/hint
issues=[]
def walk(o, path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v, f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o,str):
        pass
walk(live)
# Verify every guided box 'answer' is numeric
bad=[]
def check_boxes(steps, tag):
    for i,st in enumerate(steps):
        if "answer" in st and not isinstance(st["answer"], (int,float)):
            bad.append(f"{tag}[{i}] answer not numeric: {st['answer']!r}")
for tier in ["bronze","silver","gold"]:
    check_boxes(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
    for i,p in enumerate(live["problem_bank"][tier]):
        if "guided_steps" in p:
            check_boxes(p["guided_steps"], f"{tier}[{i}].guided_steps")
check_boxes(live["guided"]["opener"]["steps"], "opener")
print("non-numeric answer boxes:", bad or "none")
