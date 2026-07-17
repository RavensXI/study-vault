import os, json, urllib.request
KEY="geometry-L02"; ID="5c10e089-e2cc-4a61-b6b3-951a8994a1a0"
sk=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":sk,"Authorization":"Bearer "+sk})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
open("_live_geoL02.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, "n=", len(pb.get(t,[])))
