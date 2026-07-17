import os, json, urllib.request
ID="6e4a84ec-b6c4-489b-9d86-0cc1a7fb65b0"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_L06_fetched.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
print("keys:", list(pd.keys()))
print("problem_bank tiers:", list(pd.get("problem_bank",{}).keys()) if isinstance(pd.get("problem_bank"),dict) else "n/a")
