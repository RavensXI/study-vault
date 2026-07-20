import io,sys,json
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_L06_live.json",encoding="utf-8"))
pb=live["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs:
            print("NO GUIDED_STEPS",t,i,p.get("guided_skip_reason")); continue
        idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        boxes=[j for j,s in enumerate(gs) if "answer" in s]
        pre_boxes=[j for j in boxes if not idx or j<idx[0]]
        post=[j for j in boxes if idx and j>=idx[0]]
        last=gs[-1]
        flags=[]
        if len(idx)!=1: flags.append("phase count "+str(len(idx)))
        if idx and len(post)<2: flags.append("live boxes "+str(len(post)))
        if idx and idx[0]==0: flags.append("boundary at step0")
        if "check" not in json.dumps(last,ensure_ascii=False).lower() and "Check" not in str(last.get("pre","")) and not last.get("say"):
            flags.append("no check step at end: "+json.dumps(last,ensure_ascii=False)[:90])
        # final numeric box vs solution
        sol=p["solutions"][0]
        if p["input_type"]!="multiple_choice":
            lastbox=gs[boxes[-1]]["answer"]
            if abs(float(lastbox)-float(sol))>1e-9: flags.append(f"final box {lastbox} != sol {sol}")
        # misconception expect == solution?
        for m in p.get("misconceptions",[]):
            if m.get("expect")==sol: flags.append("expect==solution "+m.get("pattern",""))
        if flags: print(t,i,flags)
        if "hint" not in p: print(t,i,"NO HINT")
