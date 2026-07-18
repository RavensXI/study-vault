# -*- coding: utf-8 -*-
import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48","3848d92a-26c5-4ebf-a4d4-7f55b392e888"]
for i in IDS:
    url=f"{BASE}?id=eq.{i}&select=id,title,slug,lesson_number,practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    d=json.load(urllib.request.urlopen(req))[0]
    pd=d["practice_data"] or {}
    mc=(pd.get("method_card") or {}).get("title")
    pb=pd.get("problem_bank") or {}
    b0=(pb.get("bronze") or [{}])[0].get("display")
    print(i, "| title:", d["title"], "| slug:", d["slug"], "| L#:", d["lesson_number"])
    print("   method_card.title:", mc)
    print("   bronze[0]:", str(b0)[:80])
