import json,io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
live = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
print("=== METHOD CARD ===")
mc=live.get("method_card",{})
print("title:",mc.get("title"))
steps=mc.get("steps",[])
print("n_steps:",len(steps),"content_wordcount:", sum(len(str(s).split()) for s in steps))
print(json.dumps(mc,indent=1,ensure_ascii=False)[:1200])

# preservation vs pre-dump
ID="cbc91397-a67c-472a-b0da-308aa9da1653"
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: entry=r.get("practice_data"); break
elif isinstance(pre,dict):
    entry = pre.get(ID,{}).get("practice_data") if ID in pre else None
print("\n=== PRE-DUMP found:", entry is not None)
if entry:
    for fld in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(entry.get(fld),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(fld),sort_keys=True,ensure_ascii=False)
        print(f"  {fld}: pre_present={fld in entry} live_present={fld in live} IDENTICAL={a==b}")
    print("  pre keys:", sorted(entry.keys()))
    print("  live keys:", sorted(live.keys()))
