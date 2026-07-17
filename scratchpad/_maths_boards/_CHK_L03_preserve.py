import json
ID="0ff5cf7c-3a9d-4854-b458-6d816b7df718"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list of rows or dict keyed by id
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID:
            entry=r; break
elif isinstance(pre,dict):
    entry=pre.get(ID)
print("found pre entry:",entry is not None)
if entry is None:
    print("keys sample:", (list(pre.keys())[:3] if isinstance(pre,dict) else [r.get("id") for r in pre[:3]]))
    raise SystemExit
prepd=entry["practice_data"] if "practice_data" in entry else entry
live=json.load(open("_CHK_L03_live.json",encoding="utf-8"))["practice_data"]
for f in ["related_videos","topic_links","worked_examples","method_card"]:
    same = json.dumps(prepd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f"{f}: preserved={same}")
    if not same:
        print("  PRE :", json.dumps(prepd.get(f),ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
# check problem displays/solutions preserved (these can change only via filed fix)
for tier in ["bronze","silver","gold"]:
    pb_pre=prepd.get("problem_bank",{}).get(tier,[])
    pb_live=live.get("problem_bank",{}).get(tier,[])
    print(f"\n== {tier}: pre={len(pb_pre)} live={len(pb_live)}")
    for i,(a,b) in enumerate(zip(pb_pre,pb_live)):
        ds = a.get("display")==b.get("display")
        sol = a.get("solutions")==b.get("solutions")
        it = a.get("input_type")==b.get("input_type")
        flag = "" if (ds and sol and it) else "  <-- CHANGED"
        print(f"  [{i}] display={ds} sol={sol}({b.get('solutions')}) input={it}{flag}")
        if not ds:
            print("     PRE :",a.get("display"))
            print("     LIVE:",b.get("display"))
