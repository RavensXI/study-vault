import os, json, urllib.request
ID="54d6fba0-9730-427b-917f-ca3487dc16e9"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_psL04_live.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t) or pd.get(t)
    if isinstance(arr,list):
        print(t, "count", len(arr))
