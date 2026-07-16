import json
ID = "1d34f8fe-3649-4053-8b54-1c4e843d7669"
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/"
live = json.load(open(base+"_live_L05.json", encoding="utf-8"))
pre_all = json.load(open(base+"_pre_fanout_dump.json", encoding="utf-8"))
pre=None
for e in pre_all:
    if e.get("id")==ID: pre=e["practice_data"]; break
pw = pre["worked_examples"]; lw = live["worked_examples"]
print("lens pre/live:", len(pw), len(lw))
for i in range(max(len(pw),len(lw))):
    a = pw[i] if i<len(pw) else None
    b = lw[i] if i<len(lw) else None
    print(i, "same" if a==b else "DIFF")
    if a!=b:
        print("  PRE :", json.dumps(a, ensure_ascii=False))
        print("  LIVE:", json.dumps(b, ensure_ascii=False))
