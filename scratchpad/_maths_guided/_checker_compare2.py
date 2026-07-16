import json
ID="a43f9613-dd40-45e2-b692-00ac9c01fb92"
raw=json.load(open("_live_L04.json",encoding="utf-8"))
def unwrap(x):
    while isinstance(x,list): x=x[0]
    if isinstance(x,dict) and "practice_data" in x: return x["practice_data"]
    return x
live=unwrap(raw)
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=next((e for e in dump if e.get("id")==ID),None)
print("found:",entry is not None, "title:", entry.get("title"), "num:", entry.get("lesson_number"))
pre=entry["practice_data"]
print("pre keys:", list(pre.keys()))
# Compare preserved fields
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE:", json.dumps(pre.get(f),ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
# method_card presence
print("pre had method_card:", "method_card" in pre, "| live:", "method_card" in live)
# show pre problem_bank solutions to compare any number changes
def sols(pd):
    out={}
    for t in ["bronze","silver","gold"]:
        out[t]=[ (p.get("display","")[:45], p.get("solutions")) for p in pd.get("problem_bank",{}).get(t,[])]
    return out
import pprint
print("\n--- PRE solutions ---"); pprint.pprint(sols(pre))
print("\n--- LIVE solutions ---"); pprint.pprint(sols(live))
