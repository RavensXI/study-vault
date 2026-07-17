import json

ID = "6e789a76-e66f-4ed3-9031-599c6406ca45"
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
live = json.load(open(base+"_CHK_geoL07_live.json", encoding="utf-8"))
pd = live["practice_data"]

# write practice_data alone for validator
json.dump(pd, open(base+"_CHK_geoL07_pd.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)

# load pre-dump
predump = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))
# find entry
entry = None
if isinstance(predump, list):
    for e in predump:
        if e.get("id")==ID:
            entry = e; break
elif isinstance(predump, dict):
    entry = predump.get(ID)
    if entry is None:
        for k,v in predump.items():
            if isinstance(v,dict) and v.get("id")==ID:
                entry=v; break
print("pre-dump entry found:", entry is not None)
if entry:
    print("pre keys:", list(entry.keys()))
    pdp = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(pdp.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False)
        print(f"{f}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE:", a[:400])
            print("  NOW:", b[:400])
    print("pre top-level practice_data keys:", list(pdp.keys()) if isinstance(pdp,dict) else "n/a")
