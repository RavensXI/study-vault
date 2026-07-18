import os, json, urllib.request, io
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids=["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48","3848d92a-26c5-4ebf-a4d4-7f55b392e888"]
for i,rid in enumerate(ids):
    url=f"{BASE}?id=eq.{rid}&select=id,slug,practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    data=json.load(urllib.request.urlopen(req))[0]
    fn=f"_ck01_row{i}.json"
    with io.open(fn,"w",encoding="utf-8") as f:
        json.dump(data["practice_data"],f,ensure_ascii=False,indent=1)
    print(rid, data["slug"], "->", fn)
