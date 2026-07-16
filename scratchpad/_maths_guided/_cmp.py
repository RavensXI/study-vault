import json
live=json.load(open("_live_L07.json",encoding="utf-8"))
pre=json.load(open("_pre_L07.json",encoding="utf-8"))["practice_data"]

def eq(a,b): return json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)

for f in ["related_videos","topic_links","worked_examples"]:
    print(f, "UNCHANGED" if eq(live.get(f),pre.get(f)) else "*** CHANGED ***")

# method_card compare
print("method_card unchanged:", eq(live.get("method_card"),pre.get("method_card")))

# problem_bank: compare display/solutions/input_type/calculator per tier
for tier in ["bronze","silver","gold"]:
    lb=live["problem_bank"][tier]; pb=pre["problem_bank"][tier]
    print(f"\n{tier}: live {len(lb)} pre {len(pb)}")
    for i,(l,p) in enumerate(zip(lb,pb)):
        for key in ["display","solutions","input_type","calculator"]:
            if json.dumps(l.get(key),ensure_ascii=False)!=json.dumps(p.get(key),ensure_ascii=False):
                print(f"  [{i}] {key}: PRE={p.get(key)!r}  LIVE={l.get(key)!r}")
