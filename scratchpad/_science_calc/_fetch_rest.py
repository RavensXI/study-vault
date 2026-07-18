import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
canon=get("cc2d2229-8dc3-496f-abf9-5e3f9b2d14ec")
cj=json.dumps(canon,sort_keys=True,ensure_ascii=False)
rest=["64873952-6334-4961-bd24-f71c463ee5ac","b4a888f7-b03f-4c51-b2e0-3146fc2e98b9","63b9f62a-e314-4e79-abe3-6f430bbe459a"]
for rid in rest:
    print(rid, "IDENTICAL" if json.dumps(get(rid),sort_keys=True,ensure_ascii=False)==cj else "DIFFERS")
