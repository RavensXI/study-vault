# -*- coding: utf-8 -*-
import os, json, urllib.request, io
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48","3848d92a-26c5-4ebf-a4d4-7f55b392e888"]
def get(i):
    url=f"{BASE}?id=eq.{i}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
live0=get(IDS[0]); live1=get(IDS[1])
json.dump(live0,io.open("_LIVE_canon_L01_energy.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
s0=json.dumps(live0,sort_keys=True,ensure_ascii=False)
s1=json.dumps(live1,sort_keys=True,ensure_ascii=False)
print("PROP canonical==prop byte-identical(sorted):", s0==s1)
print("canonical method_card.title:", live0["method_card"]["title"])
print("canonical bank b/s/g:", len(live0["problem_bank"]["bronze"]),len(live0["problem_bank"]["silver"]),len(live0["problem_bank"]["gold"]))
