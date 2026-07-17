import json
pd=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
out=[]
for t in ["bronze","silver","gold"]:
    out.append(f"\n############## {t} (desc: {pb.get(t+'_description')}) ##############")
    for i,p in enumerate(pb[t]):
        out.append(f"\n----- {t}[{i}] -----")
        out.append("DISPLAY: "+str(p.get("display")))
        out.append(f"SOL: {p.get('solutions')} | input_type: {p.get('input_type')}")
        if p.get("options"): out.append("OPTIONS: "+str(p.get("options")))
        if p.get("hint"): out.append("HINT: "+str(p.get("hint")))
        if p.get("chart"): out.append("CHART: "+json.dumps(p["chart"],ensure_ascii=False))
        for m in p.get("misconceptions",[]):
            out.append(f"  MISC expect={m.get('expect')} | pattern={m.get('pattern')} | msg={m.get('message')}")
open("_CHKR_ps03_dump.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
