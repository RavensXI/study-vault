import os, json, urllib.request
ID="8e823cb5-7ee7-49af-b403-2c96a246c229"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_CHK_algL11_live.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
print("keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb: print(t,"count",len(pb[t]))
