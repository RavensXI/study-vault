# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_ck14_live.json", encoding='utf-8'))
pd = d["practice_data"]
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("BANK KEYS:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    print("  ", t, len(pb.get(t,[])))

def show(o, indent=0):
    print(json.dumps(o, ensure_ascii=False, indent=1))

for k in pd:
    if k not in ("problem_bank",):
        print("\n===== %s =====" % k)
        s = json.dumps(pd[k], ensure_ascii=False, indent=1)
        print(s)

for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb.get(t,[])):
        print("\n########## %s[%d] ##########" % (t,i))
        print(json.dumps(p, ensure_ascii=False, indent=1))
    if t+"_description" in pb:
        print("\nDESC %s: %s" % (t, pb[t+"_description"]))
for k in pb:
    if k not in ("bronze","silver","gold"):
        print("\n--- pb.%s ---" % k)
        print(json.dumps(pb[k], ensure_ascii=False, indent=1))
