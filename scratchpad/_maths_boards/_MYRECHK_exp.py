import json
pd=json.load(open("_MYRECHK_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            flag=" <== EQUALS SOLUTION" if e==sol else ""
            print(f"{tier}[{i}] sol={sol} expect={e} pat={m.get('pattern')}{flag}")
