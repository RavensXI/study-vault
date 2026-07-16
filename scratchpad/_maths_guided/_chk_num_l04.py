import json, io, re
pd=json.load(io.open("_CHK_numL04_live.json",encoding="utf-8"))

# 1. em dash scan in student-facing strings (exclude internal 'note' fields)
EMDASH="—"
hits=[]
def walk(o,path,parent_key=None):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v,f"{path}.{k}",k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]",parent_key)
    elif isinstance(o,str):
        if EMDASH in o and parent_key!="note":
            hits.append((path,o[:80]))
print("=== EM DASH HITS ===")
for h in hits: print(h)
print("total", len(hits))

# 2. check all box 'pre'/'post'/'hint' have no LaTeX (\() and answers numeric
print("\n=== BOX ANSWER TYPES ===")
def check_steps(steps,path):
    for i,s in enumerate(steps):
        if "answer" in s:
            a=s["answer"]
            if not isinstance(a,(int,float)):
                print(f"NON-NUMERIC {path}[{i}] answer={a!r}")
        for f in ("pre","post","hint"):
            if f in s and s[f] and ("\(" in s[f] or "\times" in s[f] or "$" in s[f]):
                print(f"LATEX-IN-{f} {path}[{i}]: {s[f][:60]}")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if "guided_steps" in p:
            check_steps(p["guided_steps"],f"{tier}[{i}].guided_steps")
    check_steps(pd["guided"]["teach"][tier]["steps"],f"teach.{tier}")
check_steps(pd["guided"]["opener"]["steps"],"opener")
print("(done)")
