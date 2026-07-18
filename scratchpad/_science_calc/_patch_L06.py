import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
IDS=["6c88ea75-6f77-4815-aaf3-4097ee027d91"]
pd=json.load(io.open("lesson_higher-calculations-L06@f59adbb41d.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
for ID in IDS:
    url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
    req=urllib.request.Request(url,data=body,method="PATCH",headers={
        "apikey":KEY,"Authorization":f"Bearer {KEY}",
        "Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req)
    print("PATCH",ID,r.status)
# verify back
for ID in IDS:
    url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    same=json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False)
    print("verify",ID,"byte-identical to shard:",same,
          "| keys:",sorted(live.keys())==sorted(pd.keys()))
