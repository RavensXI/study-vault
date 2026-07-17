import json

live = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_rpL06_live.json", encoding="utf-8"))["practice_data"]
pre = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-eduqas.json", encoding="utf-8"))

# pre may be dict keyed by id/slug or list
LID = "ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
entry = None
if isinstance(pre, dict):
    if LID in pre:
        entry = pre[LID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and (v.get("id")==LID or v.get("slug")=="rates-of-change-and-iterative-processes"):
                entry = v; break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id")==LID or v.get("slug")=="rates-of-change-and-iterative-processes":
            entry = v; break
print("found pre entry:", entry is not None)
if entry is None:
    print("pre keys sample:", list(pre.keys())[:5] if isinstance(pre,dict) else type(pre))
else:
    pd = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f, "PRESERVED" if a==b else "CHANGED")
        if a!=b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])
