import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
SID="4d1ac99e-f293-4cce-a4d3-c276c5f8f24b"
live=json.load(open("_CHK_algL08_LIVE_verify.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=None
for e in (pre if isinstance(pre,list) else pre.values()):
    if isinstance(e,dict) and e.get("id")==SID: entry=e;break
pm=entry["practice_data"]["method_card"]; lm=live["method_card"]
print("PRE method_card:"); print(json.dumps(pm,ensure_ascii=False,indent=1))
print("\nLIVE method_card:"); print(json.dumps(lm,ensure_ascii=False,indent=1))
# word count of live content
import re
c=re.sub("<[^>]+>"," ",lm.get("content",""))
print("\nLIVE content word count:",len(c.split()))
