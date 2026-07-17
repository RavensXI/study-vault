import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ID = "660796ad-070d-4a2d-af11-900e5a5af1c1"
live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L07graphs_live.json", encoding="utf-8"))
pre = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_pre_dump_maths-eduqas.json", encoding="utf-8"))
entry = None
for l in (pre if isinstance(pre,list) else pre.get("lessons",[])):
    if l.get("id")==ID: entry=l.get("practice_data"); break
if entry is None and isinstance(pre,dict) and ID in pre:
    entry = pre[ID]
    if isinstance(entry,dict) and "practice_data" in entry: entry=entry["practice_data"]

print("PRE method_card:\n", json.dumps(entry.get("method_card"), ensure_ascii=False, indent=1))
print("\n\nPRE worked_examples labels:")
for we in entry.get("worked_examples",[]):
    for s in we.get("steps",[]):
        print(" label:", repr(s.get("label")))
print("\nPRE keys:", list(entry.keys()))
print("LIVE keys:", list(live.keys()))
# check what pre had for guided/tier_guides/problem_bank presence
for k in ("guided","tier_guides"):
    print(f"pre has {k}:", k in entry)
