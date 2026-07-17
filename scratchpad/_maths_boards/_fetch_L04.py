import os, json, urllib.request
ID="6e383a58-7e5b-4917-a28d-2881938a3def"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_L04_live_fetch.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=2))
pd=data[0]["practice_data"]
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
print("top keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:",list(pb.keys()))
for t in ("bronze","silver","gold"):
    arr=pb.get(t,[]) if isinstance(pb.get(t),list) else pd.get(t,[])
    print(t, "->", len(arr) if isinstance(arr,list) else arr)
