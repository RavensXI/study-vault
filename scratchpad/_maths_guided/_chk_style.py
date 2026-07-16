import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_algL08_LIVE_verify.json",encoding="utf-8"))
bad=[]
bank=live["problem_bank"]
for tier in ("gold","bronze","silver"):
    for i,prob in enumerate(bank[tier]):
        h=prob.get("hint","")
        if "\(" in h or "<" in h: bad.append((tier,i,"hint has latex/html",h))
        for j,s in enumerate(prob.get("guided_steps",[])):
            for f in ("pre","post"):
                if f in s and ("\(" in s[f] or "<" in s[f]): bad.append((tier,i,j,f,"latex/html",s[f]))
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                bad.append((tier,i,j,"non-numeric answer",s["answer"]))
# teach + opener boxes numeric
for w in ("bronze","silver","gold"):
    for j,s in enumerate(live["guided"]["teach"][w]["steps"]):
        if "answer" in s and not isinstance(s["answer"],(int,float)): bad.append(("teach",w,j,s["answer"]))
for j,s in enumerate(live["guided"]["opener"]["steps"]):
    if "answer" in s and not isinstance(s["answer"],(int,float)): bad.append(("opener",j,s["answer"]))
print("style issues:",bad)
