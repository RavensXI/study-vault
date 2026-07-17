# -*- coding: utf-8 -*-
import json

ID = "496a8347-7f03-47a6-9543-49cb82efe3af"
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
live = json.load(open("_ADVCHK_L08_live.json", encoding="utf-8"))

# pre-dump structure: could be list or dict keyed by id
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        for k, v in pre.items():
            if isinstance(v, dict) and v.get("id") == ID:
                entry = v.get("practice_data", v)
                break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id") == ID:
            entry = v.get("practice_data", v)
            break

if entry is None:
    print("NO PRE ENTRY FOUND; pre type", type(pre))
    if isinstance(pre, dict):
        print("keys sample:", list(pre.keys())[:5])
    raise SystemExit

pd = entry.get("practice_data", entry) if isinstance(entry, dict) and "practice_data" in entry else entry

for f in ["related_videos", "topic_links", "worked_examples"]:
    a = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f, "MATCH" if a == b else "DIFF")
    if a != b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])

print("pre top keys:", sorted(pd.keys()))
# count bank problems pre vs live
for tier in ["bronze","silver","gold"]:
    pn = len(pd.get("problem_bank",{}).get(tier,[]))
    ln = len(live.get("problem_bank",{}).get(tier,[]))
    print("bank", tier, "pre", pn, "live", ln)
# compare displays and solutions per problem
for tier in ["bronze","silver","gold"]:
    pb = pd.get("problem_bank",{}).get(tier,[])
    lb = live.get("problem_bank",{}).get(tier,[])
    for i in range(min(len(pb),len(lb))):
        pd_disp = pb[i].get("display"); ld_disp = lb[i].get("display")
        ps = pb[i].get("solutions"); ls = lb[i].get("solutions")
        if pd_disp != ld_disp:
            print("DISPLAY CHANGED", tier, i)
            print("  PRE :", pd_disp)
            print("  LIVE:", ld_disp)
        if json.dumps(ps) != json.dumps(ls):
            print("SOLUTION CHANGED", tier, i, "pre", ps, "live", ls, "| disp:", ld_disp)
