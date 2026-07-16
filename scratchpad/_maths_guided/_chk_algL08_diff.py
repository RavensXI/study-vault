import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
SID="4d1ac99e-f293-4cce-a4d3-c276c5f8f24b"
live=json.load(open("_CHK_algL08_LIVE_verify.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=None
for e in (pre if isinstance(pre,list) else pre.values()):
    if isinstance(e,dict) and e.get("id")==SID: entry=e;break
pd=entry["practice_data"]
pw=pd["worked_examples"]; lw=live["worked_examples"]
print("PRE count",len(pw),"LIVE count",len(lw))
for i in range(max(len(pw),len(lw))):
    p=json.dumps(pw[i],sort_keys=True,ensure_ascii=False) if i<len(pw) else None
    l=json.dumps(lw[i],sort_keys=True,ensure_ascii=False) if i<len(lw) else None
    print(f"[{i}]", "SAME" if p==l else "DIFF")
    if p!=l:
        print("  PRE :",p)
        print("  LIVE:",l)
print("method_card SAME:", json.dumps(pd["method_card"],sort_keys=True,ensure_ascii=False)==json.dumps(live["method_card"],sort_keys=True,ensure_ascii=False))
