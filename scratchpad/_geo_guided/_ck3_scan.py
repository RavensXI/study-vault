import json,sys,re
sys.stdout.reconfigure(encoding="utf-8")
d=json.load(open("_ck3_L03_live.json",encoding="utf-8"))
issues=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+"[%d]"%i)
    elif isinstance(o,str):
        if "—" in o or "–" in o: issues.append(("EMDASH",path,o[:120]))
        if re.search(r"&[a-z]+;|&#",o): issues.append(("ENTITY",path,o[:120]))
        if "\(" in o or "$$" in o: issues.append(("LATEX",path,o[:120]))
walk(d,"")
for t in issues: print(t)
print("--- check:wrong occurrences:", json.dumps(d).count('"check"'))
pb=d["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        for j,m in enumerate(p.get("misconceptions",[])):
            if "check" in m: print("CHECKKEY",t,i,j,m)
            if "expect" not in m: print("NOEXPECT",t,i,j,m)
            if m.get("expect") is None: print("NULLEXPECT",t,i,j)
        gs=p.get("guided_steps",[])
        nb=[s for s in gs if "answer" in s]
        # numeric check
        for j,s in enumerate(gs):
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                print("NONNUMERIC",t,i,j,s["answer"])
            for f in ("pre","post","hint"):
                if f in s and re.search(r"<[a-z]",s[f] or ""): print("HTMLIN",t,i,j,f,s[f][:80])
        idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        pre_n=idx[0] if idx else None
        post_boxes=len([s for j,s in enumerate(gs) if "answer" in s and idx and j>=idx[0]])
        print("BOUNDARY %s[%d] steps=%d boxes=%d subst_at=%s pre_boxes=%s live_boxes=%d"%(t,i,len(gs),len(nb),idx,len([s for j,s in enumerate(gs) if 'answer' in s and idx and j<idx[0]]),post_boxes))
        if not idx: print("  !! NO SUBSTITUTE PHASE",t,i)
        if idx and post_boxes<2: print("  !! <2 live boxes",t,i)
        # leakage: solution appearing in hint/misc message
        sols=p.get("solutions")
        if p.get("input_type")!="multiple_choice" and sols:
            s0=str(sols[0])
            for j,m in enumerate(p.get("misconceptions",[])):
                if s0 in m.get("message",""): print("  LEAK? misc",t,i,j,m["message"])
            if s0 in (p.get("hint") or ""): print("  LEAK? hint",t,i,p["hint"])
        if p.get("input_type")=="multiple_choice" and sols:
            corr=p["options"][sols[0]]
            key=corr.split(",")[0].split(" because")[0].strip().lower()
            for j,m in enumerate(p.get("misconceptions",[])):
                if key and key in m.get("message","").lower(): print("  LEAK? misc-mc",t,i,j,key,"|",m["message"][:120])
            if key and key in (p.get("hint") or "").lower(): print("  LEAK? hint-mc",t,i,key,p["hint"])
