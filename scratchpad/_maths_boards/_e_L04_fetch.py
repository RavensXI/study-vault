import os, json, urllib.request
ID="83d542e3-c94b-4365-b8a9-070845b779ec"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_e_L04_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:",list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs=pb.get(t,[])
    print(t,"count:",len(probs))
