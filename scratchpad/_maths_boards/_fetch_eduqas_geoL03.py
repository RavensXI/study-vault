import json, os, urllib.request
ID="1e9d6465-1ec1-40a3-8138-958197366837"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_live_eduqas_geoL03.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("fetched keys:", list(pd.keys()))
pb=pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    probs=pb.get(t) or []
    print(f"--- {t}: {len(probs)} problems; desc={pb.get(t+'_description')!r}")
    for i,p in enumerate(probs):
        print(f"  [{i}] input={p.get('input_type')} calc={p.get('calculator')} sols={p.get('solutions')}")
        print(f"       display={p.get('display')!r}")
