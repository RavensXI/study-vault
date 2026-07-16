import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_geometry-L08.json",encoding="utf-8"))
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        sol=p.get("solutions")
        for m in p.get("misconceptions",[]):
            exp=m.get("expect")
            same = (exp==sol) or (isinstance(sol,list) and len(sol)==1 and exp==sol[0])
            print(f"{tier}[{i}] sol={sol} expect={exp} pattern={m.get('pattern')}"+(" *** EQUALS CORRECT ***" if same else ""))
