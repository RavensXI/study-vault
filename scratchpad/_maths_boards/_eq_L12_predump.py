import json
pre = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_pre_dump_maths-eduqas.json", encoding="utf-8"))
live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_eq_L12_live.json", encoding="utf-8"))
# pre may be keyed by id or key
ID = "66a1ec53-d20f-4b82-b436-1b31fc88e998"
KEY = "algebra-L12"
if isinstance(pre, dict):
    print("top keys sample:", list(pre.keys())[:5])
    ent = pre.get(ID) or pre.get(KEY)
    if ent is None:
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("id")==ID or v.get("key")==KEY):
                ent=v; print("found under",k); break
    if ent is not None:
        pd = ent.get("practice_data", ent)
        for f in ("worked_examples","topic_links","related_videos"):
            print(f, "MATCH live?" , json.dumps(pd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True))
    else:
        print("NO pre-dump entry found for this lesson")
