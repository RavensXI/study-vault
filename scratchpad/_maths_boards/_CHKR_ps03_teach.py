import json
pd=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
g=pd["guided"]
out=[]
out.append("===== OPENER =====")
op=g.get("opener",{})
out.append(json.dumps(op,ensure_ascii=False,indent=1))
out.append("\n===== TEACH =====")
for tier in ["bronze","silver","gold"]:
    tw=g.get("teach",{}).get(tier)
    out.append(f"\n--- teach.{tier} ---")
    out.append(json.dumps(tw,ensure_ascii=False,indent=1))
open("_CHKR_ps03_teach.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
