# -*- coding: utf-8 -*-
import json
base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
live = json.load(open(base + r"\_LIVE_number-L01.json", encoding="utf-8"))
pre  = json.load(open(base + r"\_predump_number-L01.json", encoding="utf-8"))

# Preservation: related_videos, topic_links, worked_examples should be unchanged
for f in ["related_videos", "topic_links", "worked_examples"]:
    same = json.dumps(pre.get(f), sort_keys=True) == json.dumps(live.get(f), sort_keys=True)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")

# displays & solutions preserved (numbers may have been repaired-check which)
for tier in ["bronze","silver","gold"]:
    pb_pre = pre["problem_bank"][tier]
    pb_liv = live["problem_bank"][tier]
    print(f"\n{tier}: pre={len(pb_pre)} live={len(pb_liv)}")
    for i in range(max(len(pb_pre),len(pb_liv))):
        dp = pb_pre[i]["display"] if i < len(pb_pre) else "<none>"
        dl = pb_liv[i]["display"] if i < len(pb_liv) else "<none>"
        sp = pb_pre[i]["solutions"] if i < len(pb_pre) else "?"
        sl = pb_liv[i]["solutions"] if i < len(pb_liv) else "?"
        flag = "" if (dp==dl and sp==sl) else "  <<< DIFF"
        print(f"  [{i}] sol {sp}->{sl}  {flag}")
        if flag:
            print(f"        pre display: {dp}")
            print(f"        liv display: {dl}")
