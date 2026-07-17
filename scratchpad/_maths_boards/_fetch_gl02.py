import os, json, urllib.request
ID="96f5aef3-e4c8-4faf-ba82-1d587dc4e10e"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_gl02.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
print("bank tiers:", list(pd.get("problem_bank",{}).keys()) if "problem_bank" in pd else "NO problem_bank")
