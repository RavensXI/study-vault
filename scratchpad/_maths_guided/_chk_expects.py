import json, io
pd=json.load(io.open("_CHK_numL04_live.json",encoding="utf-8"))
bad=0
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol=p["solutions"][0]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and e==sol:
                print(f"EXPECT==SOL {tier}[{i}] pattern={m['pattern']} expect={e}"); bad+=1
print("expect==sol count:", bad)
# substitute step answer == solution?
print("\n=== substitute-step lands on solution ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps",[])
        subs=[s for s in gs if s.get("phase")=="substitute"]
        if subs:
            a=subs[0]["answer"]; sol=p["solutions"][0]
            if a!=sol: print(f"MISMATCH {tier}[{i}] substitute={a} sol={sol}")
print("(done)")
