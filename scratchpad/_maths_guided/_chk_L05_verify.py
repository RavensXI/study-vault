import json
live=json.load(open("_CHK_L05_live.json",encoding="utf-8"))
pre=json.load(open("_CHK_L05_predump.json",encoding="utf-8"))
out=open("_CHK_L05_report.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")

# ---- Preservation ----
w("=== PRESERVATION ===")
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
    w(f, "UNCHANGED" if same else "CHANGED")
    if not same:
        w("  PRE:", json.dumps(pre.get(f),ensure_ascii=False)[:400])
        w("  NOW:", json.dumps(live.get(f),ensure_ascii=False)[:400])

# ---- Bank sizes & displays pre vs live ----
w("\n=== BANK SIZE / DISPLAYS ===")
lb=live["problem_bank"]; pb=pre["problem_bank"]
for t in ["bronze","silver","gold"]:
    w(f"{t}: pre={len(pb.get(t,[]))} live={len(lb.get(t,[]))}")
    for i,p in enumerate(lb.get(t,[])):
        w(f"  {t}[{i}] disp: {p['display']!r} sol={p['solutions']} calc={p.get('calculator')}")

# ---- em dash scan in student-facing strings ----
w("\n=== EM DASH SCAN (student-facing) ===")
import re
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            w(f"  DASH at {path}: {o!r}")
scan(live,"root")
w("(none above = clean)")
out.close()
print(open("_CHK_L05_report.txt",encoding="utf-8").read())
