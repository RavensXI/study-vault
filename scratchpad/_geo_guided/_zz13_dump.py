import json, io, sys
P=r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided"
pd=json.load(open(P+r"\_zz13_pd.json",encoding="utf-8"))
out=io.StringIO()
def w(*a): print(*a, file=out)

w("=== KEYS ===", list(pd.keys()))
w("\n=== method_card ===")
w(json.dumps(pd["method_card"], indent=1, ensure_ascii=False))
w("\n=== tier_guides ===")
w(json.dumps(pd["tier_guides"], indent=1, ensure_ascii=False))
w("\n=== guided ===")
w(json.dumps(pd["guided"], indent=1, ensure_ascii=False))
w("\n=== topic_links ===")
w(json.dumps(pd["topic_links"], indent=1, ensure_ascii=False))
w("\n=== exam_context ===")
w(json.dumps(pd["exam_context"], indent=1, ensure_ascii=False))
w("\n=== worked_examples ===")
w(json.dumps(pd["worked_examples"], indent=1, ensure_ascii=False))
b=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    w("\n\n########## %s_description: %r" % (t, b.get(t+"_description")))
    for i,p in enumerate(b[t]):
        w("\n----- %s[%d] -----" % (t,i))
        w(json.dumps(p, indent=1, ensure_ascii=False))
open(P+r"\_zz13_dump.txt","w",encoding="utf-8").write(out.getvalue())
print("ok", len(out.getvalue()))
