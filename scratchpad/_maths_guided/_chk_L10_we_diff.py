import json
live = json.load(open("_CHK_L10_live.json", encoding="utf-8"))
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID="ddb5e897-f8ce-4c64-961a-7d6095d41a7c"
entry=next(e for e in pre if e.get("id")==ID)
pd=entry["practice_data"]
pw=pd["worked_examples"]; lw=live["worked_examples"]
for i,(a,b) in enumerate(zip(pw,lw)):
    sa=json.dumps(a,sort_keys=True); sb=json.dumps(b,sort_keys=True)
    if sa!=sb:
        print(f"--- we[{i}] DIFFERS")
        print("PRE :",json.dumps(a)[:600])
        print("LIVE:",json.dumps(b)[:600])
# also check method_card diff (allowed trim)
print("\n=== method_card ===")
print("PRE :",json.dumps(pd.get("method_card"))[:500])
print("LIVE:",json.dumps(live.get("method_card"))[:500])
