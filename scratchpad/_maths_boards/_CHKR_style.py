import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]

emdash_hits=[]
badbox=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o:  # em dash
            emdash_hits.append((path,o[:80]))
walk(pd,"pd")
print("EM DASH hits:",len(emdash_hits))
for p,s in emdash_hits: print("  ",p,"::",s)

# numeric-only box answers
def chkboxes(steps,path):
    for j,s in enumerate(steps):
        if "answer" in s:
            a=s["answer"]
            if not isinstance(a,(int,float)):
                badbox.append(f"{path}[{j}] answer={a!r}")
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        chkboxes(p.get("guided_steps",[]),f"{t}[{i}].guided_steps")
for t in ["bronze","silver","gold"]:
    chkboxes(pd["guided"]["teach"][t]["steps"],f"teach.{t}")
chkboxes(pd["guided"]["opener"]["steps"],"opener")
print("\nNon-numeric boxes:",badbox)

# hint plain text (no latex/html)
print("\nHint checks:")
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        h=p.get("hint","")
        if "\(" in h or "<" in h:
            print(f"  {t}[{i}] hint has latex/html: {h!r}")
print("done")
