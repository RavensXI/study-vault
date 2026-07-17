import os, json, urllib.request
ID="d84411dc-60b7-4f96-8f42-35486f5d7129"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_eduqas_L13_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t,[])
    print(f"--- {t}: {len(probs)} problems")
    for i,p in enumerate(probs):
        print(f"  [{i}] it={p.get('input_type')} calc={p.get('calculator')} sols={p.get('solutions')}")
        print(f"       display: {p.get('display')}")
        if p.get('options'): print(f"       options: {p.get('options')}")
