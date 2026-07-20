import json, sys
p = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_FX_L02_live.json"
d = json.load(open(p, encoding="utf-8"))
pb = d["problem_bank"]
def show(tier, i):
    pr = pb[tier][i]
    print("=== %s[%d] ===" % (tier, i))
    for k, v in pr.items():
        if k in ("guided_steps", "misconceptions"):
            print(" ", k, ":")
            for j, s in enumerate(v):
                print("   [%d] %s" % (j, json.dumps(s, ensure_ascii=False)))
        else:
            print(" ", k, "=", json.dumps(v, ensure_ascii=False)[:600])
for t, i in [("silver",5), ("bronze",7), ("gold",2)]:
    show(t, i)
g = d["guided"]
print("=== opener ===")
print(json.dumps(g["opener"], ensure_ascii=False, indent=1))
print("=== teach.bronze ===")
print(json.dumps(g["teach"]["bronze"], ensure_ascii=False, indent=1))
