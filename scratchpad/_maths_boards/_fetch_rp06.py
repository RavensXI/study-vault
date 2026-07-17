import os, json, urllib.request
ID="e15d6925-608b-4c05-aa82-c4782d1657b3"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_rp06.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t, len(arr))
    for i,p in enumerate(arr):
        print(" ",t,i,repr(p.get("display","")[:110]), "sol=",p.get("solutions"), "calc=",p.get("calculator"), "it=",p.get("input_type"))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
print("top-level keys detail:")
for k in pd.keys():
    v=pd[k]
    print("  ",k, type(v).__name__, (len(v) if hasattr(v,'__len__') else ''))
