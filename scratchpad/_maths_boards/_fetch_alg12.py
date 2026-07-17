import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="971cfba0-badb-4c6b-b0f8-e9d33d450b8c"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
open("_live_alg12.json","w",encoding="utf-8").write(json.dumps(data[0], ensure_ascii=False, indent=1))
pd=data[0]["practice_data"]
print("title:", data[0].get("title"))
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t) if isinstance(pb,dict) else None
    if isinstance(probs,list):
        print(f"{t}: {len(probs)} problems")
