import json,sys
p=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_adv14_live.json",encoding="utf-8"))["practice_data"]
out=[]
def w(s=""): out.append(s)
w("TOP KEYS: "+", ".join(sorted(p.keys())))
for k,v in p.items():
    if k not in ("problem_bank","guided","tier_guides","method_card"):
        w(f"--- {k} ---")
        w(json.dumps(v,ensure_ascii=False,indent=1)[:3000])
w("\n=== METHOD CARD ===")
w(json.dumps(p.get("method_card"),ensure_ascii=False,indent=1))
w("\n=== TIER GUIDES ===")
w(json.dumps(p.get("tier_guides"),ensure_ascii=False,indent=1))
w("\n=== GUIDED ===")
w(json.dumps(p.get("guided"),ensure_ascii=False,indent=1))
w("\n=== BANK ===")
pb=p["problem_bank"]
for k,v in pb.items():
    if not isinstance(v,list):
        w(f"[{k}] = {v!r}")
for tier in ("bronze","silver","gold"):
    probs=pb.get(tier,[])
    w(f"\n##### {tier} n={len(probs)}")
    for i,pr in enumerate(probs):
        w(f"\n----- {tier}[{i}] -----")
        w(json.dumps(pr,ensure_ascii=False,indent=1))
open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_adv14_dump.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
