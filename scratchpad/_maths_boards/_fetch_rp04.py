import os, json, urllib.request
ID="6f3f98f9-e772-40d9-8e54-b76a2ed3e8c7"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_rp04.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t, len(arr))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
