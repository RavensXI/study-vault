import json
live=json.load(open("_live_graphs_l01.json",encoding="utf-8"))
pre=json.load(open("_pre_pd.json",encoding="utf-8"))

def cmp(name):
    a=json.dumps(pre.get(name),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(name),sort_keys=True,ensure_ascii=False)
    print(f"{name}: {'SAME' if a==b else 'CHANGED'}")

for n in ["related_videos","topic_links","worked_examples","method_card"]:
    cmp(n)

# problem displays & solutions preserved?
print("\n-- problem displays/solutions old vs new --")
for tier in ["bronze","silver","gold"]:
    op=pre["problem_bank"][tier]; np_=live["problem_bank"][tier]
    print(f"[{tier}] pre n={len(op)} live n={len(np_)}")
    for i,(o,n) in enumerate(zip(op,np_)):
        od,nd=o.get("display"),n.get("display")
        os_,ns_=o.get("solutions"),n.get("solutions")
        if od!=nd: print(f"  {tier}[{i}] DISPLAY changed:\n    OLD: {od}\n    NEW: {nd}")
        if os_!=ns_: print(f"  {tier}[{i}] SOL changed: {os_} -> {ns_}")

# descriptions
for k in ["bronze_description","silver_description","gold_description"]:
    print(k, "present" if k in live["problem_bank"] else "MISSING")
