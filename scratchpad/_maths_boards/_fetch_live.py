import os, json, urllib.request
ID="9a6f1e85-41b4-4b82-87c6-e919e48362a9"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_ratio-proportion-L01.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
print("problem_bank tiers:", list(pd.get("problem_bank",{}).keys()) if isinstance(pd.get("problem_bank"),dict) else "n/a")
