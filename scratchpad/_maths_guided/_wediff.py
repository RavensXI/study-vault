import json
live=json.load(open("_live_L06.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="622f7959-f9e9-45aa-b2bd-8a5b6698e357"
ppd=[v for v in pre if v.get("id")==ID][0]["practice_data"]
pw=ppd["worked_examples"]; lw=live["worked_examples"]
for i,(a,b) in enumerate(zip(pw,lw)):
    if json.dumps(a,sort_keys=True)!=json.dumps(b,sort_keys=True):
        print(f"--- worked_examples[{i}] differs")
        print("PRE q:",a.get("question"),"| diff:",a.get("difficulty"))
        print("LIVE q:",b.get("question"),"| diff:",b.get("difficulty"))
        print("PRE:",json.dumps(a,ensure_ascii=False))
        print("LIVE:",json.dumps(b,ensure_ascii=False))
    else:
        print(f"worked_examples[{i}] unchanged: {b.get('question')}")
# also method_card diff
print("\n=== method_card")
print("PRE:",json.dumps(ppd["method_card"],ensure_ascii=False))
print("LIVE:",json.dumps(live["method_card"],ensure_ascii=False))
