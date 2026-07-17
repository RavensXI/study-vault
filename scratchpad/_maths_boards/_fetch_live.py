import os, json, urllib.request
ID="89062264-f404-4e8e-8959-06c7a9fd0b7a"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_geometry-L01.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=1))
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t) or pd.get(t)
    if isinstance(arr,list):
        print(t, "count", len(arr))
