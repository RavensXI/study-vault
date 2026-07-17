import json
ID="d84411dc-60b7-4f96-8f42-35486f5d7129"
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre may be list or dict
if isinstance(pre,dict) and "practice_data" not in pre:
    # maybe keyed by id
    entry=pre.get(ID)
else:
    entry=None
if entry is None:
    # try list
    if isinstance(pre,list):
        for r in pre:
            if r.get("id")==ID:
                entry=r; break
print("type pre:", type(pre).__name__, "found entry:", entry is not None)
if entry is not None:
    pdpre = entry.get("practice_data", entry)
    print("pre keys:", list(pdpre.keys()) if isinstance(pdpre,dict) else "n/a")
    live=json.load(open("_ADVCHK_L13_live.json",encoding="utf-8"))
    for f in ["related_videos","topic_links","worked_examples"]:
        pv=pdpre.get(f); lv=live.get(f)
        same = json.dumps(pv,sort_keys=True,ensure_ascii=False)==json.dumps(lv,sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pv,ensure_ascii=False)[:400])
            print("  LIVE:", json.dumps(lv,ensure_ascii=False)[:400])
