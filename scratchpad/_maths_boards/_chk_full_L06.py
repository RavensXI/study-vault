import json
pd=json.load(open("_live_number-L06.json", encoding="utf-8"))
pb=pd["problem_bank"]
issues=[]

# duplicate answers within tier
for t in ["bronze","silver","gold"]:
    seen={}
    for i,p in enumerate(pb[t]):
        k=json.dumps(p["solutions"])
        if k in seen: issues.append(f"DUP {t}: [{seen[k]}] and [{i}] both {k}")
        seen[k]=i

# em dash scan in student-facing strings
def scan(o,path):
    if isinstance(o,str):
        if "—" in o: issues.append(f"EMDASH at {path}: {o[:60]}")
    elif isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{path}[{i}]")
scan(pd,"root")

# final guided box lands on solution (numeric check where possible)
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[s for s in gs if "answer" in s]
        finals=[b["answer"] for b in boxes]
        sol=p["solutions"]
        # solution values should appear among box answers
        for sv in sol:
            if sv not in finals:
                issues.append(f"{t}[{i}] solution {sv} not among box answers {finals}")

print("ISSUES:", len(issues))
for x in issues: print(" -",x)
