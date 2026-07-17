import os, json, urllib.request, io
ID="5ff3e1eb-2284-4096-af06-4bcb6754b0e1"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
key=os.environ["SUPABASE_SERVICE_KEY"]
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
with io.open("_CHK_L09_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("fetched OK; top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs=pb.get(t,[])
    if isinstance(probs,list):
        print(t, "n=", len(probs))
