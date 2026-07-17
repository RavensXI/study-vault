import json
ID="fb13c12c-f5c1-4832-871b-40440d729361"
live=json.load(open("_CHKR_L04g_live.json",encoding="utf-8"))["practice_data"]
dump=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# dump structure: could be list of rows or dict keyed by id
row=None
if isinstance(dump,list):
    for r in dump:
        if r.get("id")==ID: row=r; break
elif isinstance(dump,dict):
    if ID in dump: row=dump[ID]
    else:
        # maybe {'lessons':[...]} or list under a key
        for k,v in dump.items():
            if isinstance(v,list):
                for r in v:
                    if isinstance(r,dict) and r.get("id")==ID: row=r;break
print("row found:",row is not None)
if row is None:
    print("dump type",type(dump))
    if isinstance(dump,dict): print("keys",list(dump.keys())[:10])
    if isinstance(dump,list): print("len",len(dump),"sample keys",list(dump[0].keys()) if dump else None)
else:
    pre=row.get("practice_data",row)
    for f in ["related_videos","topic_links","worked_examples","method_card"]:
        a=json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "SAME" if a==b else "CHANGED")
        if a!=b:
            print("  PRE :",a[:400])
            print("  LIVE:",b[:400])
    print("pre top keys:",list(pre.keys()))
