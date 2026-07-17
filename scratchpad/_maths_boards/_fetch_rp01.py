import os, json, urllib.request
ID="5cfec765-3128-469b-9d6a-626f042d6161"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_rp01.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t, len(arr))
