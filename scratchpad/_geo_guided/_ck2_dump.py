import json, sys
p = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_ck2_L03_live.json"
d = json.load(open(p, encoding="utf-8"))
out = []
def w(s=""): out.append(str(s))

w("===== GUIDED.OPENER =====")
g = d["guided"]
w(json.dumps(g.get("opener"), ensure_ascii=False, indent=1))
w("")
w("===== GUIDED.TEACH =====")
for t in ("bronze","silver","gold"):
    w("--- teach." + t)
    w(json.dumps(g.get("teach",{}).get(t), ensure_ascii=False, indent=1))
w("")
w("===== OTHER GUIDED KEYS: " + str([k for k in g if k not in ("opener","teach")]))
w(json.dumps({k:v for k,v in g.items() if k not in ("opener","teach")}, ensure_ascii=False, indent=1))
w("")
w("===== TIER GUIDES =====")
w(json.dumps(d.get("tier_guides"), ensure_ascii=False, indent=1))
w("")
w("===== METHOD CARD =====")
w(json.dumps(d.get("method_card"), ensure_ascii=False, indent=1))
w("")
pb = d["problem_bank"]
for t in ("bronze","silver","gold"):
    w("### %s_description: %r" % (t, pb.get(t+"_description")))
for t in ("bronze","silver","gold"):
    for i, pr in enumerate(pb[t]):
        w("")
        w("="*70)
        w("%s[%d]  id=%s type=%s" % (t, i, pr.get("id"), pr.get("input_type")))
        w(json.dumps(pr, ensure_ascii=False, indent=1))
open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_ck2_L03_dump.txt","w",encoding="utf-8").write("\n".join(out))
print(len("\n".join(out)))
