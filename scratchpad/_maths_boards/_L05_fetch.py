import os, json, urllib.request
ID="4fd08300-e0fe-44c5-93cd-76b6d900c72d"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_L05_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t, len(arr) if isinstance(arr,list) else arr)
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
