import json
live=json.load(open("_live_L06.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="622f7959-f9e9-45aa-b2bd-8a5b6698e357"
pe=[v for v in pre if v.get("id")==ID][0]
ppd=pe["practice_data"]
print("PRE practice_data keys:", sorted(ppd.keys()))
print("LIVE practice_data keys:", sorted(live.keys()))
for f in ("related_videos","topic_links"):
    same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
    if not same:
        print("  PRE:",json.dumps(ppd.get(f),ensure_ascii=False))
        print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False))
# worked_examples: may be trimmed. Compare.
we_same=json.dumps(ppd.get("worked_examples"),sort_keys=True)==json.dumps(live.get("worked_examples"),sort_keys=True)
print("worked_examples:", "UNCHANGED" if we_same else "CHANGED")
if not we_same:
    print("  PRE count:",len(ppd.get("worked_examples",[])),"LIVE count:",len(live.get("worked_examples",[])))
# method_card compare
print("method_card CHANGED:", json.dumps(ppd.get("method_card"),sort_keys=True)!=json.dumps(live.get("method_card"),sort_keys=True))
# what keys added
print("added keys:", set(live)-set(ppd))
print("removed keys:", set(ppd)-set(live))
# pre problem_bank displays
def disp(pb):
    d={}
    for t in ("bronze","silver","gold"):
        d[t]=[p.get("display") for p in pb.get(t,[])]
    return d
print("PRE bank displays:")
print(json.dumps(disp(ppd["problem_bank"]),ensure_ascii=False,indent=1))
print("LIVE bank displays:")
print(json.dumps(disp(live["problem_bank"]),ensure_ascii=False,indent=1))
