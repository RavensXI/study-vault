import json
pre = json.load(open(r"_CHK_L02_pre.json", encoding="utf-8"))["pd"]
live = json.load(open(r"_CHK_L02_live.json", encoding="utf-8"))

for t in ("bronze","silver","gold"):
    a = pre["problem_bank"][t]; b = live["problem_bank"][t]
    print(f"=== {t}: pre {len(a)} live {len(b)}")
    for i,(p,q) in enumerate(zip(a,b)):
        for f in ("chart","image","ruler","options","solutions","input_type","display","id"):
            pv = p.get(f); qv = q.get(f)
            if json.dumps(pv,sort_keys=True) != json.dumps(qv,sort_keys=True):
                print(f"  {t}[{i}].{f} CHANGED")
                print("    pre :", json.dumps(pv,ensure_ascii=False)[:400])
                print("    live:", json.dumps(qv,ensure_ascii=False)[:400])
for f in ("related_videos","topic_links","worked_examples"):
    same = json.dumps(pre.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f, "same:", same)
print("pre keys", list(pre.keys()))
