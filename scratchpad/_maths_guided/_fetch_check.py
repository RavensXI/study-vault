import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="a7d027ed-f9a9-427f-aa1d-83c6459954b0"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_live_graphsL01.json","w"), indent=1)
print("keys:", list(pd.keys()))
