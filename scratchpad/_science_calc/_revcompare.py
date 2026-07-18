# -*- coding: utf-8 -*-
import os, json, urllib.request, io
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48","3848d92a-26c5-4ebf-a4d4-7f55b392e888"]
authored=json.load(io.open("lesson_physics-calculations-L01@087ba4e3f7.json",encoding="utf-8"))
canon_sorted=json.dumps(authored,sort_keys=True,ensure_ascii=False)
canon_raw=json.dumps(authored,ensure_ascii=False)
for i in IDS:
    url=f"{BASE}?id=eq.{i}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    ls=json.dumps(live,sort_keys=True,ensure_ascii=False)
    lr=json.dumps(live,ensure_ascii=False)
    print(i)
    print("   sorted-identical-to-authored:", ls==canon_sorted)
    print("   raw-identical-to-authored:   ", lr==canon_raw)
    # spot-check content type
    banks=live.get("problem_bank",{})
    print("   bank sizes b/s/g:", len(banks.get("bronze",[])), len(banks.get("silver",[])), len(banks.get("gold",[])))
