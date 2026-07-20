import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre=json.load(open("_CHK_L05_pre.json",encoding="utf-8"))["pd"]
now=json.load(open("_CHK_L05_live.json",encoding="utf-8"))
print("PRE keys",sorted(pre.keys()))
print("NOW keys",sorted(now.keys()))
for f in ("related_videos","topic_links","worked_examples","method_card"):
    same = json.dumps(pre.get(f),sort_keys=True)==json.dumps(now.get(f),sort_keys=True)
    print(f,"identical:",same)
pb_pre=pre["problem_bank"]; pb_now=now["problem_bank"]
for t in ("bronze","silver","gold"):
    a=pb_pre[t]; b=pb_now[t]
    print(t,len(a),len(b))
    for i,(x,y) in enumerate(zip(a,b)):
        msgs=[]
        if x.get("display")!=y.get("display"): msgs.append("DISPLAY CHANGED\n  OLD:%s\n  NEW:%s"%(x.get("display"),y.get("display")))
        if x.get("solutions")!=y.get("solutions"): msgs.append("SOLUTIONS %r -> %r"%(x.get("solutions"),y.get("solutions")))
        if x.get("options")!=y.get("options"): msgs.append("OPTIONS\n  OLD:%s\n  NEW:%s"%(x.get("options"),y.get("options")))
        if x.get("input_type")!=y.get("input_type"): msgs.append("INPUT %r->%r"%(x.get("input_type"),y.get("input_type")))
        if json.dumps(x.get("chart"),sort_keys=True)!=json.dumps(y.get("chart"),sort_keys=True): msgs.append("CHART CHANGED")
        if x.get("image")!=y.get("image"): msgs.append("IMAGE %r -> %r"%(x.get("image"),y.get("image")))
        if x.get("ruler")!=y.get("ruler"): msgs.append("RULER %r -> %r"%(x.get("ruler"),y.get("ruler")))
        if x.get("calculator")!=y.get("calculator"): msgs.append("CALC %r->%r"%(x.get("calculator"),y.get("calculator")))
        if msgs:
            print(" %s[%d]:"%(t,i))
            for m in msgs: print("   ",m)
