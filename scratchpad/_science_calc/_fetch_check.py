import os, json, urllib.request
KEY=os.environ.get("SUPABASE_SERVICE_KEY")
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
cid="a28c155d-46f2-49af-9cc4-27d907de0ae2"
url=f"{BASE}?id=eq.{cid}&select=id,slug,unit_id,practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
json.dump(data, open("_live_canonical.json","w"), indent=2)
pd=data[0]["practice_data"]
print("slug:",data[0]["slug"])
print("keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in pb: print(t, len(pb[t]))
