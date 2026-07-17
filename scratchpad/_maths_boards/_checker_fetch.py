import os, json, urllib.request
ID="9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_checker_live.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t) or pd.get(t)
    if isinstance(arr,list):
        print(t, "count", len(arr))
