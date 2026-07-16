import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live = json.load(open("_live_L02.json", encoding="utf-8"))

# walk all strings, track path; skip internal 'note' fields (exempt)
hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue  # internal, exempt
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:  # em dash, en dash
            hits.append((path,o))
for k,v in live.items():
    walk(v,k)
print("EM/EN DASH hits in student-facing (excl note):", len(hits))
for p,s in hits: print(" ",p,"::",s[:80])

# also check for HTML entities in plain-text guided_steps pre/post/hint, tier descriptions
import re
ent=re.compile(r"&[a-zA-Z]+;|&#\d+;")
ehits=[]
def walk2(o,path,plain=False):
    if isinstance(o,dict):
        for k,v in o.items():
            walk2(v,f"{path}.{k}", plain=k in ("pre","post","hint") or plain)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk2(v,f"{path}[{i}]",plain)
    elif isinstance(o,str) and plain:
        if ent.search(o): ehits.append((path,o))
for k,v in live.items(): walk2(v,k)
print("\nHTML entities in plain pre/post/hint:", len(ehits))
for p,s in ehits: print(" ",p,"::",s[:80])

# check every guided_step box 'answer' is numeric
bad=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                bad.append(f"{tier}[{i}].guided_steps[{j}]")
print("\nnon-numeric answers:", bad or "none")
