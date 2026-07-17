import os, json, urllib.request
ID="39bdcd12-eb3d-45b1-b0c5-d8e2257610df"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_CHK_LIVE_fresh.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=2))
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb: print(t,"count:",len(pb[t]))
