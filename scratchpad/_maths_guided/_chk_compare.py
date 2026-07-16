import json
live=json.load(open("_CHK_graphsL08_live.json",encoding="utf-8"))
pre=json.load(open("_CHK_graphsL08_predump.json",encoding="utf-8"))
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(live.get(f),sort_keys=True)==json.dumps(pre.get(f),sort_keys=True)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
# method_card present in both
print("method_card in pre:", "method_card" in pre, "in live:", "method_card" in live)
same = json.dumps(live.get("method_card"),sort_keys=True)==json.dumps(pre.get("method_card"),sort_keys=True)
print("method_card:", "UNCHANGED" if same else "CHANGED (expected, trimmed per spec 8)")
# problem_bank displays/solutions/options preservation - check displays unchanged
def bank_core(pb):
    out={}
    for tier in ["bronze","silver","gold"]:
        out[tier]=[{"display":p.get("display"),"solutions":p.get("solutions"),"options":p.get("options"),"input_type":p.get("input_type")} for p in pb.get(tier,[])]
    return out
print("bank displays/solutions:", "UNCHANGED" if json.dumps(bank_core(live["problem_bank"]),sort_keys=True)==json.dumps(bank_core(pre["problem_bank"]),sort_keys=True) else "CHANGED")
# show diffs if changed
lc=bank_core(live["problem_bank"]); pc=bank_core(pre["problem_bank"])
for tier in ["bronze","silver","gold"]:
    for i,(a,b) in enumerate(zip(lc[tier],pc[tier])):
        if json.dumps(a,sort_keys=True)!=json.dumps(b,sort_keys=True):
            print(f"  DIFF {tier}[{i}]:\n    live={a}\n    pre ={b}")
