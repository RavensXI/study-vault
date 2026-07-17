import json

base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
ID = "47e48001-4c4f-45ab-a400-ba16648b2569"

live = json.load(open(base+"_CHK_rpL05_LIVE.json", encoding="utf-8"))
pre_all = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))

# pre_dump structure?
print("pre_dump type:", type(pre_all))
if isinstance(pre_all, dict):
    print("keys sample:", list(pre_all.keys())[:5])
    entry = pre_all.get(ID)
elif isinstance(pre_all, list):
    print("list len", len(pre_all), "sample item keys:", list(pre_all[0].keys()) if pre_all else None)
    entry = None
    for it in pre_all:
        if it.get("id")==ID or it.get("lesson_id")==ID:
            entry = it
            break
print("found entry:", entry is not None)
if entry:
    pd = entry.get("practice_data", entry)
    print("pre keys:", list(pd.keys()) if isinstance(pd,dict) else pd)
    for f in ["topic_links","related_videos","worked_examples"]:
        same = json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pd.get(f),ensure_ascii=False)[:400])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
