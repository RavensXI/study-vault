import json
pd=json.load(open("_live_6e66_b76fdf39.json",encoding="utf-8"))
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    sols=[]
    for i,p in enumerate(pb[tier]):
        s=p["solutions"]
        sols.append(tuple(s))
        # final guided box must equal solution? not always (check box). Just report last non-check
        gs=p.get("guided_steps",[])
        boxes=[st["answer"] for st in gs if st.get("answer") is not None]
        acc=p.get("accept")
        # expects
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None:
                sv=s[0]
                tol=acc if acc else 0.011
                if abs(float(e)-float(sv))<=tol:
                    print("!! DEAD EXPECT",tier,i,"expect",e,"sol",sv,"tol",tol)
        print(tier,i,"sol",s,"boxes",boxes,"accept",acc,"unit",repr(p.get("unit")),"HT",p.get("higher_only"))
    dups=[x for x in set(sols) if sols.count(x)>1]
    if dups: print("!! DUP in",tier,dups)
