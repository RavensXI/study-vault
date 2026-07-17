import os, json, urllib.request
ID="47e48001-4c4f-45ab-a400-ba16648b2569"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_rp05.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t, len(arr))
    for i,p in enumerate(arr):
        print(" ",t,i,repr(p.get("display","")[:90]), "sol=",p.get("solutions"), "calc=",p.get("calculator"), "it=",p.get("input_type"))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
