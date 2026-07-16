import json
live = json.load(open("_CHK_L10_live.json", encoding="utf-8"))

# find pre-dump entry
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID="ddb5e897-f8ce-4c64-961a-7d6095d41a7c"
entry=None
if isinstance(pre,list):
    for e in pre:
        if e.get("id")==ID: entry=e; break
elif isinstance(pre,dict):
    entry=pre.get(ID) or (pre.get("lessons") and next((x for x in pre["lessons"] if x.get("id")==ID),None))
print("pre entry found:", entry is not None)
if entry:
    pd = entry.get("practice_data") or entry
    print("pre keys:", list(pd.keys()) if isinstance(pd,dict) else type(pd))
    for k in ["related_videos","topic_links"]:
        same = json.dumps(pd.get(k),sort_keys=True)==json.dumps(live.get(k),sort_keys=True)
        print(f"{k}: preserved={same}")
        if not same:
            print("  PRE:",json.dumps(pd.get(k))[:400])
            print("  LIVE:",json.dumps(live.get(k))[:400])
    # worked_examples may be trimmed legitimately
    we_same = json.dumps(pd.get("worked_examples"),sort_keys=True)==json.dumps(live.get("worked_examples"),sort_keys=True)
    print("worked_examples: same=",we_same)
    if not we_same:
        print("  PRE we count:", len(pd.get("worked_examples") or []), "LIVE:", len(live.get("worked_examples") or []))
