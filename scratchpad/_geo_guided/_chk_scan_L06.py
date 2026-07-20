import io,sys,json,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_L06_live.json",encoding="utf-8"))
s=json.dumps(live,ensure_ascii=False)
print("check-wrong count:", s.count('"check"'), s.count('"wrong"'))
print("em dash count:", s.count("—"))
# figure claims
pb=live["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        d=p.get("display","")
        has=("chart" in p) or ("image" in p)
        if re.search(r"box plot|graph|map shows|the chart|diagram|shown", d, re.I) and not has:
            print("FIGURE CLAIM w/o stimulus:",t,i,d[:160])
        if not has and re.search(r"box plot|graph|chart", json.dumps(p.get("guided_steps",[]),ensure_ascii=False), re.I):
            print("walk mentions figure w/o stimulus:",t,i)
# numeric answers
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                print("NON-NUMERIC",t,i,j,st["answer"])
            for k in ("pre","post","hint"):
                if k in st and re.search(r"<|\\|\$", st[k]): print("MARKUP",t,i,j,k,st[k])
        for m in p.get("misconceptions",[]):
            if "check" in m: print("SURVIVING CHECK",t,i,m)
            if "expect" not in m: print("NO EXPECT",t,i,m)
print(json.dumps(live["tier_guides"],ensure_ascii=False,indent=1))
