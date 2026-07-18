import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
for rid in ["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48","3848d92a-26c5-4ebf-a4d4-7f55b392e888"]:
    url=f"{BASE}?id=eq.{rid}&select=id,title,slug,lesson_number,unit_id"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        row=json.load(r)[0]
    print(row["id"],"| title:",row.get("title"),"| slug:",row.get("slug"),"| n:",row.get("lesson_number"))
# also fetch L03 circuit canonical to compare content origin
url=f"{BASE}?id=eq.b2dd6adb-eb4b-4251-a9fd-3305d8493c16&select=id,title,slug,practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    l3=json.load(r)[0]
print("L03 title:",l3.get("title"),"| slug:",l3.get("slug"),"| method_card.title:",l3.get("practice_data",{}).get("method_card",{}).get("title"))
# Is L03's practice_data identical to what's now on L01?
import io
c=json.load(open("_live_canon.json",encoding="utf-8"))
l3pd=l3.get("practice_data",{})
print("L01-live == L03-live practice_data:", json.dumps(c,sort_keys=True,ensure_ascii=False)==json.dumps(l3pd,sort_keys=True,ensure_ascii=False))
