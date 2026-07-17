# -*- coding: utf-8 -*-
import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="fb13c12c-f5c1-4832-871b-40440d729361"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(pre,list):
    for e in pre:
        if e.get("id")==ID: entry=e;break
elif isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v;break
print("entry found:",entry is not None)
if entry is None:
    print("pre type",type(pre).__name__)
    if isinstance(pre,dict): print("keys sample",list(pre.keys())[:5])
    if isinstance(pre,list): print("len",len(pre),"first keys",list(pre[0].keys())[:8] if pre else None)
    sys.exit()
prepd=entry.get("practice_data") or entry
livepd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
for k in ["topic_links","related_videos","worked_examples"]:
    pv=prepd.get(k); lv=livepd.get(k)
    same=json.dumps(pv,sort_keys=True,ensure_ascii=False)==json.dumps(lv,sort_keys=True,ensure_ascii=False)
    print(f"\n{k}: preserved={same}  pre_type={type(pv).__name__} pre_len={len(pv) if isinstance(pv,(list,dict)) else pv}  live_len={len(lv) if isinstance(lv,(list,dict)) else lv}")
    if not same:
        print("  PRE:",json.dumps(pv,ensure_ascii=False)[:800])
        print("  LIVE:",json.dumps(lv,ensure_ascii=False)[:800])
# also list pre-dump top keys vs live
print("\npre top keys:",sorted(prepd.keys()))
print("live top keys:",sorted(livepd.keys()))
