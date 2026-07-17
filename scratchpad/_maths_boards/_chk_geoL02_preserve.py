import json

ID = "09fd71ca-ab66-4ea3-bf5b-0005f5ae5b6e"
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
pre = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))
live = json.load(open(base+"_chk_geoL02_live.json", encoding="utf-8"))

# pre may be a list of rows or dict keyed by id
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id") == ID:
            entry = r.get("practice_data"); break
elif isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID].get("practice_data", pre[ID])
    else:
        # maybe keyed by lesson key
        for k,v in pre.items():
            vid = v.get("id") if isinstance(v,dict) else None
            if vid==ID:
                entry = v.get("practice_data"); break
print("found pre entry:", entry is not None)
if entry is None:
    print("pre type:", type(pre))
    if isinstance(pre, dict):
        print("sample keys:", list(pre.keys())[:5])
        first = pre[list(pre.keys())[0]]
        print("first val type/keys:", type(first), (list(first.keys())[:8] if isinstance(first,dict) else ''))
    elif isinstance(pre, list):
        print("len", len(pre), "first keys", list(pre[0].keys())[:8])
else:
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(entry.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE :", json.dumps(entry.get(f),ensure_ascii=False)[:600])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:600])
    # also list pre top keys
    print("pre keys:", list(entry.keys()))
