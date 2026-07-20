import json,sys
d=json.load(open("_ck3_L03_live.json",encoding="utf-8"))
o=[]
def p(*a): o.append(" ".join(str(x) for x in a))
p("=== TOP KEYS", list(d.keys()))
g=d["guided"]
p("=== GUIDED KEYS", list(g.keys()))
p("--- OPENER"); p(json.dumps(g.get("opener"),ensure_ascii=False,indent=1))
for t in ("bronze","silver","gold"):
    p("--- TEACH",t); p(json.dumps(g["teach"][t],ensure_ascii=False,indent=1))
p("=== TIER_GUIDES"); p(json.dumps(d["tier_guides"],ensure_ascii=False,indent=1))
p("=== METHOD_CARD"); p(json.dumps(d["method_card"],ensure_ascii=False,indent=1))
pb=d["problem_bank"]
p("=== PB KEYS",list(pb.keys()))
for t in ("bronze","silver","gold"):
    for i,pr in enumerate(pb[t]):
        p("\n===== %s[%d] ====="%(t,i))
        p(json.dumps(pr,ensure_ascii=False,indent=1))
open("_ck3_dump.txt","w",encoding="utf-8").write("\n".join(o))
print(len("\n".join(o)))
