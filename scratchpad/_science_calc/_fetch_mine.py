import json, urllib.request, os
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="08e03207-3ecf-4964-81dc-a8b94002b3e2"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_mine_fresh.json","w"), indent=2)
print("bronze",len(pd["problem_bank"]["bronze"]),"silver",len(pd["problem_bank"]["silver"]),"gold",len(pd["problem_bank"]["gold"]))
print("keys",list(pd.keys()))
