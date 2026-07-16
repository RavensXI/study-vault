import json, re
pd=json.load(open("_live_L03.json",encoding="utf-8"))

# 1. Em dash scan in student-facing strings (exclude internal 'note' fields)
emdash=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o:  # em dash
            emdash.append((path,o))
        if "–" in o:  # en dash
            emdash.append((path+" (EN-DASH)",o))
print("EM/EN DASH hits:", len(emdash))
for p,s in emdash: print("  ",p,"::",s[:80])

# 2. Non-numeric answer boxes
bad=[]
def checkbox(o,path):
    if isinstance(o,dict):
        if "answer" in o and "pre" not in o and "post" not in o:
            pass
        if "answer" in o:
            a=o["answer"]
            if not isinstance(a,(int,float)) or isinstance(a,bool):
                bad.append((path,a))
        for k,v in o.items(): checkbox(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): checkbox(v,f"{path}[{i}]")
checkbox(pd,"root")
print("Non-numeric answer boxes:", bad)

# 3. Check MC solutions valid indices, and option at solution
def check_mc(tier):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol=p["solutions"]
        opts=p.get("options")
        it=p.get("input_type")
        if it=="multiple_choice":
            for s in sol:
                if s<0 or s>=len(opts):
                    print(f"BAD SOL {tier}[{i}] sol={s} opts={len(opts)}")
for t in ["gold","bronze","silver"]:
    check_mc(t)
print("MC solution index check done")

# tier sizes
for t in ["gold","bronze","silver"]:
    print(t,"size",len(pd["problem_bank"][t]))
