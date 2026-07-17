import json

ID = "74d5f6d6-9036-4da3-adf3-d7e2c86fc6b4"
base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
live = json.load(open(base + r"\_CHK_psL03_LIVE.json", encoding="utf-8"))
pre_all = json.load(open(base + r"\_pre_dump_maths-aqa.json", encoding="utf-8"))

# pre_all could be list of rows or dict keyed by id
pre = None
if isinstance(pre_all, list):
    for row in pre_all:
        if row.get("id") == ID:
            pre = row.get("practice_data")
            break
elif isinstance(pre_all, dict):
    if ID in pre_all:
        pre = pre_all[ID]
        if isinstance(pre, dict) and "practice_data" in pre:
            pre = pre["practice_data"]

print("pre found:", pre is not None)
if pre:
    for f in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pre.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f, "MATCH" if a == b else "DIFF")
        if a != b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])
    print("pre keys:", list(pre.keys()))
