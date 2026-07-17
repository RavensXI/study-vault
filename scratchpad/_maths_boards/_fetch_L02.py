import os, json, urllib.request
KEY="number-L02"; ID="cbc91397-a67c-472a-b0da-308aa9da1653"
sk=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":sk,"Authorization":"Bearer "+sk})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
open("_live_number-L02.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, "n=", len(pb.get(t,[])))
