import json, os, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_higher-calculations-L03@4def3c722e.json",encoding="utf-8"))
ids=["b4864848-f50f-4481-9af7-983e8f3d20d8"]
body=json.dumps({"practice_data":pd}).encode("utf-8")
for cid in ids:
    url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%cid
    req=urllib.request.Request(url,data=body,method="PATCH",headers={
        "apikey":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req); print("PATCH",cid,r.status)
# verify byte-identical
local=json.dumps(pd,sort_keys=True,ensure_ascii=False)
for cid in ids:
    url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%cid
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    live=json.loads(urllib.request.urlopen(req).read())[0]["practice_data"]
    print("MATCH",cid, json.dumps(live,sort_keys=True,ensure_ascii=False)==local)
