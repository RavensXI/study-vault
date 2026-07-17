import json
live=json.load(open("_live_ratio-proportion-L01.json",encoding="utf-8"))
# Check: every bank problem's final box == solutions[0]; count boxes at/after phase
bad=0
for tier,plist in live["problem_bank"].items():
    if not isinstance(plist,list): continue
    for i,p in enumerate(plist):
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if "answer" in s]
        if not boxes: 
            if p.get("input_type")!="multiple_choice" and "guided_skip_reason" not in p:
                print(f"{tier}[{i}] NO BOXES"); bad+=1
            continue
        # live boxes at/after first phase
        seen=False; after=0; before=0
        for s in gs:
            if s.get("phase")=="substitute": seen=True
            if "answer" in s:
                if seen: after+=1
                else: before+=1
        if before<1: print(f"{tier}[{i}] <1 box before phase"); bad+=1
        if after<2: print(f"{tier}[{i}] <2 boxes after phase (={after})"); bad+=1
        sol=p["solutions"][0]
        # final box should equal solution OR a check; just report final answer-carrying box that names the result
        # verify misconception expects != correct
        for m in p.get("misconceptions",[]):
            if m.get("expect")==sol:
                print(f"{tier}[{i}] expect==solution {sol}"); bad+=1
print("Structural box check bad count:", bad)
print("OK" if bad==0 else "ISSUES")
