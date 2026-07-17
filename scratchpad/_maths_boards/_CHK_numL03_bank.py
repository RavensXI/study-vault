import json
LID = "c8596747-22a3-47f0-8fe7-f0bc6c6d1101"
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
entry = pre[LID] if isinstance(pre,dict) and LID in pre else None
if entry is None and isinstance(pre,list):
    entry = next(v for v in pre if v.get("id")==LID)
prepd = entry["practice_data"] if "practice_data" in entry else entry
live = json.load(open("_CHK_numL03_live.json", encoding="utf-8"))
for tier in ["bronze","silver","gold"]:
    pb_pre = prepd["problem_bank"][tier]
    pb_live = live["problem_bank"][tier]
    print(f"\n=== {tier}: pre={len(pb_pre)} live={len(pb_live)} ===")
    for i in range(max(len(pb_pre),len(pb_live))):
        d_pre = pb_pre[i]["display"] if i<len(pb_pre) else "<none>"
        s_pre = pb_pre[i].get("solutions") if i<len(pb_pre) else None
        d_liv = pb_live[i]["display"] if i<len(pb_live) else "<none>"
        s_liv = pb_live[i].get("solutions") if i<len(pb_live) else None
        flag = "" if (d_pre==d_liv and s_pre==s_liv) else "  <-- CHANGED"
        print(f"[{i}] PRE  {s_pre} | {d_pre}")
        print(f"    LIVE {s_liv} | {d_liv}{flag}")
