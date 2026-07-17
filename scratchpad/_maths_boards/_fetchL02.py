import os, json, urllib.request
ID="330ee5b7-1c7b-4990-861a-b9de40f4c2a9"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_fresh_L02.json","w"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t) or pd.get(t)
    if isinstance(probs,list):
        print(t, len(probs))
