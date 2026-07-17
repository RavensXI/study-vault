import json
live=json.load(open("_recheck_rp01_live.json",encoding="utf-8"))
pb=live["problem_bank"]
issues=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        opts=p.get("options",[]); sol=p.get("solutions",[])
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if not isinstance(e,int) or e<0 or e>=len(opts):
                issues.append(f"{tier}[{i}].misconceptions[{j}] expect={e} OUT OF RANGE (opts={len(opts)})")
            elif e in sol:
                issues.append(f"{tier}[{i}].misconceptions[{j}] expect={e} EQUALS SOLUTION")
        # verify solutions in range and single
        for s in sol:
            if s<0 or s>=len(opts): issues.append(f"{tier}[{i}] solution {s} out of range")
print("EXPECT/SOLUTION integrity issues:", issues if issues else "NONE")
# check duplicate option strings within a problem
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        opts=p.get("options",[])
        if len(set(opts))!=len(opts):
            print(f"DUPLICATE option in {tier}[{i}]: {opts}")
print("done")
