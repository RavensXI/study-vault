import os, json, urllib.request
SK=os.environ["SUPABASE_SERVICE_KEY"]
ID="27ec4539-cb68-4e60-ad0d-fa0828706d80"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":SK,"Authorization":f"Bearer {SK}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_live_eduqas_L10.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t,[]) if isinstance(pb.get(t),list) else pb.get(t,{})
    print(t, "->", len(probs) if isinstance(probs,list) else type(probs))
