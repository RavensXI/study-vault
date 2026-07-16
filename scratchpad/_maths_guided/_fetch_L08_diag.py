import os, json, urllib.request
ID="33559430-93a0-4565-971b-65b8fc2cc53d"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_diag_L08_live.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])))
