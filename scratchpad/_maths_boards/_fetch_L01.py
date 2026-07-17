import os, json, urllib.request
ID="e58f9467-dd87-4589-9b18-b603c1966291"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
open("_live_number-L01.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:",list(pb.keys()) if isinstance(pb,dict) else type(pb))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t) if isinstance(pb,dict) else None
    if isinstance(probs,list):
        print(f"{t}: {len(probs)} problems")
