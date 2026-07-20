import json,io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
now=json.load(open("_CHK_L05_live.json",encoding="utf-8"))
pre=json.load(open("_CHK_L05_pre.json",encoding="utf-8"))["pd"]
print("--- method_card OLD ---"); print(json.dumps(pre["method_card"],indent=1,ensure_ascii=False))
print("--- method_card NEW ---"); print(json.dumps(now["method_card"],indent=1,ensure_ascii=False))
print("--- tier_guides ---"); print(json.dumps(now["tier_guides"],indent=1,ensure_ascii=False))
# scan for check wrong / em dash / non numeric answers
s=json.dumps(now,ensure_ascii=False)
print("check_wrong occurrences:", s.count('"check"'))
print("em dash count:", s.count("—"))
for t in ("bronze","silver","gold"):
    for i,p in enumerate(now["problem_bank"][t]):
        gs=p.get("guided_steps")
        if not gs: print("NO guided_steps",t,i,p.get("guided_skip_reason"))
        else:
            boxes=[st for st in gs if "answer" in st]
            for j,st in enumerate(gs):
                if "answer" in st and not isinstance(st["answer"],(int,float)):
                    print("NON-NUMERIC",t,i,j,st["answer"])
            ph=[j for j,st in enumerate(gs) if st.get("phase")=="substitute"]
            after=sum(1 for st in gs[ph[0]:] if "answer" in st) if ph else 0
            before=sum(1 for st in gs[:ph[0]] if "answer" in st) if ph else 0
            if not ph: print("NO PHASE",t,i)
            elif before<1 or after<2: print("BOUNDARY",t,i,"before",before,"after",after)
            last=[st for st in gs if "answer" in st][-1]
            print(t,i,"lastbox",last["answer"],"sol",p.get("solutions"),"endsWithSay", "say" in gs[-1] and "answer" not in gs[-1])
        for k,m in enumerate(p.get("misconceptions",[])):
            if "check" in m: print("CHECK-WRONG",t,i,k,m)
            if "expect" not in m: print("NO EXPECT",t,i,k)
