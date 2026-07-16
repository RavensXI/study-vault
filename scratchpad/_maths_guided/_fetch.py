import os, urllib.request, json
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.7120daae-b81f-4fc3-9ae8-e6be798f1e06&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_L07.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
