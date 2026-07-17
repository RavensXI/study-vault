import json
live=json.load(open("_CHK_L02_live.json",encoding="utf-8"))
# key compound recomputations
print("gold3 y3:",2000*1.06**3,"y4:",2000*1.06**4)
print("gold4 rev:",12000/1.05**2)
print("gold5 pop:",80000*0.97**5)
print("silver1 comp int:",8000*1.05**3-8000)
print("silver6 comp:",6000*1.04**3)
print("mc example:",5000*1.03**4)
print("we2:",12000*0.85**3)
# integrity
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        opts=p["options"]
        if len(set(opts))!=len(opts): print("DUP OPTIONS",tier,i,opts)
        for m in p.get("misconceptions",[]):
            if m.get("expect")==0: print("EXPECT=0 collision",tier,i)
            if m.get("expect") is not None and not (0<=m["expect"]<len(opts)):
                print("BAD EXPECT INDEX",tier,i,m["expect"])
        if p["solutions"]!=[0]: print("SOL not [0]",tier,i,p["solutions"])
print("integrity scan done")
