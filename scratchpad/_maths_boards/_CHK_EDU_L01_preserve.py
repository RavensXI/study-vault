import json
ID="89062264-f404-4e8e-8959-06c7a9fd0b7a"
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre may be list of rows
rows = pre if isinstance(pre,list) else pre.get("data",pre)
entry=None
for r in rows:
    if isinstance(r,dict) and r.get("id")==ID:
        entry=r; break
if entry is None:
    # maybe keyed by id
    if isinstance(pre,dict) and ID in pre:
        entry=pre[ID]
print("found pre entry:", entry is not None)
if entry:
    pd_pre = entry.get("practice_data", entry)
    live=json.load(open("_CHK_EDU_L01_live.json",encoding="utf-8"))["practice_data"]
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pd_pre.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "MATCH" if a==b else "DIFF")
        if a!=b:
            print("  PRE :",a[:600])
            print("  LIVE:",b[:600])
    print("pre top keys:",list(pd_pre.keys()))
