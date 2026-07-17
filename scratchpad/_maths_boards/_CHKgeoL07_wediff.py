import json
pre=json.load(open("_pre_worked_examples.json",encoding="utf-8"))
live=json.load(open("_CHKgeoL07_live.json",encoding="utf-8"))["worked_examples"]
print("pre count:",len(pre),"live count:",len(live))
for i,(a,b) in enumerate(zip(pre,live)):
    if json.dumps(a,sort_keys=True,ensure_ascii=False)!=json.dumps(b,sort_keys=True,ensure_ascii=False):
        print(f"--- WE[{i}] DIFF ---")
        print("PRE :",json.dumps(a,ensure_ascii=False))
        print("LIVE:",json.dumps(b,ensure_ascii=False))
if len(pre)!=len(live):
    print("COUNT MISMATCH")
