import os, json, urllib.request
ID="d8937c21-f4ad-4d20-971a-03186a285b7f"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_L07_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0]["title"])
print("slug:",data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t) or pd.get(t)
    if isinstance(arr,list):
        print(t,"count",len(arr))
