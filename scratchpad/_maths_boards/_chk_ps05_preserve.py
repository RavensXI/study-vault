# -*- coding: utf-8 -*-
import json
live = json.load(open("_chk_ps05_live.json", encoding="utf-8"))
pre_all = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# find pre entry for this lesson id
ID="2e75898f-577a-42bd-b94e-f1435e89ace3"
pre=None
if isinstance(pre_all, dict):
    # could be keyed by id or key
    for k,v in pre_all.items():
        if isinstance(v,dict):
            if v.get("id")==ID or k==ID:
                pre=v.get("practice_data", v)
                break
            pd=v.get("practice_data")
            if isinstance(pd,dict):
                pass
if pre is None and isinstance(pre_all,list):
    for v in pre_all:
        if v.get("id")==ID:
            pre=v.get("practice_data"); break
print("pre found:", pre is not None)
if pre is None:
    print("top-level keys:", list(pre_all.keys())[:20] if isinstance(pre_all,dict) else type(pre_all))
else:
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE :", json.dumps(pre.get(f),ensure_ascii=False)[:400])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
    # solutions preserved per problem
    print("--- solutions pre vs live ---")
    for tier in ["gold","bronze","silver"]:
        preb=pre.get("problem_bank",{}).get(tier,[])
        liveb=live.get("problem_bank",{}).get(tier,[])
        for j in range(max(len(preb),len(liveb))):
            ps = preb[j].get("solutions") if j<len(preb) else "MISSING"
            ls = liveb[j].get("solutions") if j<len(liveb) else "MISSING"
            pd = preb[j].get("display","")[:45] if j<len(preb) else ""
            flag = "" if ps==ls else "  <-- CHANGED"
            print(f"{tier}[{j}] pre={ps} live={ls}{flag}")
