import json,io,sys,statistics as st
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
now=json.load(open("_CHK_L05_live.json",encoding="utf-8"))
d=now["problem_bank"]["bronze"][5]["chart"]["data"]["datasets"][0]["data"]
from collections import Counter
print("bronze5 counter:",Counter(d).most_common(4),"sum",sum(d),"mean",sum(d)/12)
# hints / descriptions leakage vs solutions
for t in ("bronze","silver","gold"):
    for i,p in enumerate(now["problem_bank"][t]):
        sol=str(p["solutions"][0])
        h=p.get("hint","")
        if sol in h: print("HINT LEAK",t,i,h)
        for m in p.get("misconceptions",[]):
            if p["input_type"]!="multiple_choice" and sol in m["message"]: print("MSG LEAK",t,i,m)
            if m.get("expect")==p["solutions"][0]: print("EXPECT==SOLUTION",t,i,m)
print("ok")
