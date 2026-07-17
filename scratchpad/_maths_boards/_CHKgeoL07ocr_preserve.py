import json

ID = "813488f9-f52c-4d54-8b53-c95eded2df12"
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"

live = json.load(open(base+"_CHKgeoL07ocr_live.json", encoding="utf-8"))["practice_data"]
pre = json.load(open(base+"_pre_dump_maths-ocr.json", encoding="utf-8"))

# pre may be list of rows or dict keyed by id
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id") == ID:
            entry = r
            break
elif isinstance(pre, dict):
    entry = pre.get(ID)
    if entry is None and "practice_data" in pre:
        entry = pre

print("pre type:", type(pre).__name__)
if entry is None:
    # maybe dict keyed differently
    if isinstance(pre, dict):
        print("keys sample:", list(pre.keys())[:5])
    raise SystemExit("entry not found")

pd = entry.get("practice_data", entry)
print("PRE top keys:", sorted(pd.keys()))
print("LIVE top keys:", sorted(live.keys()))

for f in ["related_videos", "topic_links", "worked_examples", "method_card"]:
    same = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
    if not same:
        print("  PRE :", json.dumps(pd.get(f), ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f), ensure_ascii=False)[:400])

# problem count / solutions comparison
def sols(o):
    pb = o.get("problem_bank", {})
    return {t: [p.get("solutions") for p in pb.get(t, [])] for t in ["bronze","silver","gold"]}
print("PRE sols:", sols(pd))
print("LIVE sols:", sols(live))
