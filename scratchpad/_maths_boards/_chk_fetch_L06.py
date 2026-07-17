import os, json, urllib.request
ID="24e576f2-0e8a-43bc-bacd-5397b4da617b"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_live_number-L06.json","w"), indent=1)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t) or pd.get(t)
    if isinstance(probs,list):
        print(t, "n=", len(probs))
