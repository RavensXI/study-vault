import json

ID = "295660a5-6ee6-40a4-9c32-c6aa0de7a590"
live = json.load(open("_CHK2_graphsL05_LIVE.json", encoding="utf-8"))["practice_data"]
pre_all = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# locate pre entry
def find(obj):
    if isinstance(obj, list):
        for e in obj:
            if isinstance(e, dict) and e.get("id") == ID:
                return e
    if isinstance(obj, dict):
        if ID in obj:
            return obj[ID]
        for v in obj.values():
            r = find(v)
            if r: return r
    return None

pre = find(pre_all)
print("pre found:", pre is not None)
if pre is None:
    print("top type", type(pre_all), (list(pre_all)[:3] if isinstance(pre_all,dict) else len(pre_all)))
else:
    pd = pre.get("practice_data") if "practice_data" in pre else pre
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
    print("pre keys:", list(pd.keys()))
    # display texts preserved?
    for tier in ["bronze","silver","gold"]:
        prep = pd.get("problem_bank",{}).get(tier,[])
        livp = live.get("problem_bank",{}).get(tier,[])
        print(f"--- {tier}: pre={len(prep)} live={len(livp)}")
        for i in range(max(len(prep),len(livp))):
            pd_disp = prep[i].get("display") if i<len(prep) else "<none>"
            lv_disp = livp[i].get("display") if i<len(livp) else "<none>"
            pd_sol = prep[i].get("solutions") if i<len(prep) else None
            lv_sol = livp[i].get("solutions") if i<len(livp) else None
            mark = "" if (pd_disp==lv_disp and pd_sol==lv_sol) else "  <<CHANGED"
            print(f"  [{i}] sol pre={pd_sol} live={lv_sol}{mark}")
            if pd_disp!=lv_disp:
                print(f"      pre disp: {pd_disp}")
                print(f"      liv disp: {lv_disp}")
