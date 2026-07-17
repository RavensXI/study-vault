import json

ID = "014f2f50-be82-4870-a8e7-d15963b39e8f"
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
live = json.load(open("_MYCHK_L05_live.json", encoding="utf-8"))

# pre-dump may be dict keyed by id, or list of rows
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        # maybe dict of id->practice_data or list under a key
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry = v
elif isinstance(pre, list):
    for row in pre:
        if row.get("id")==ID:
            entry = row
print("type pre:", type(pre).__name__, "len/keys:", (len(pre) if hasattr(pre,'__len__') else '?'))
if entry is None:
    # show sample structure
    if isinstance(pre, list):
        print("sample row keys:", list(pre[0].keys())[:10])
        print("sample ids:", [r.get("id") for r in pre[:5]])
    else:
        print("dict keys sample:", list(pre.keys())[:5])
else:
    pd = entry.get("practice_data", entry)
    print("PRE keys:", sorted(pd.keys()))
    print("LIVE keys:", sorted(live.keys()))
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pd.get(f))[:500])
            print("  LIVE:", json.dumps(live.get(f))[:500])
    # method_card compare
    print("method_card PRE:", json.dumps(pd.get("method_card"))[:300])
    # displays comparison per tier
    prepb = pd.get("problem_bank",{})
    livepb = live.get("problem_bank",{})
    for t in ["bronze","silver","gold"]:
        pre_d = [p.get("display") for p in prepb.get(t,[])]
        live_d = [p.get("display") for p in livepb.get(t,[])]
        pre_s = [p.get("solutions") for p in prepb.get(t,[])]
        live_s = [p.get("solutions") for p in livepb.get(t,[])]
        print(f"--- {t} ---")
        for i in range(max(len(pre_d),len(live_d))):
            pd_disp = pre_d[i] if i<len(pre_d) else "MISSING"
            lv_disp = live_d[i] if i<len(live_d) else "MISSING"
            ps = pre_s[i] if i<len(pre_s) else "?"
            ls = live_s[i] if i<len(live_s) else "?"
            flag = "" if (pd_disp==lv_disp and ps==ls) else "  <-- CHANGED"
            print(f"  [{i}] sol {ps}->{ls} {'DISP-DIFF' if pd_disp!=lv_disp else ''}{flag}")
            if pd_disp!=lv_disp:
                print(f"      PRE : {pd_disp}")
                print(f"      LIVE: {lv_disp}")
