import json
p = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_rp_L03_live.json"
d = json.load(open(p, encoding="utf-8"))
pb = d["problem_bank"]
targets = [("gold",3),("silver",1),("bronze",1),("bronze",4),("bronze",6),("silver",2),("silver",4),("silver",6),("gold",1)]
for t,i in targets:
    print("="*70)
    print(t,i)
    print(json.dumps(pb[t][i], ensure_ascii=False, indent=1))
print("="*70)
print("TEACH BRONZE")
print(json.dumps(d["guided"]["teach"]["bronze"], ensure_ascii=False, indent=1))
