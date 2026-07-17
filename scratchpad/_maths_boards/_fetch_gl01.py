import os, json, urllib.request, io
KEY="112923c0-364e-4701-91d9-280e7859d6d3"
sk=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{KEY}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":sk,"Authorization":f"Bearer {sk}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
io.open("_live_gl01.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=1))
print("TOP KEYS:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    arr=pb.get(tier,[])
    print(f"--- {tier}: {len(arr)} problems ---")
    for i,p in enumerate(arr):
        print(f"[{tier}][{i}] it={p.get('input_type')} sol={p.get('solutions')} chart={'Y' if p.get('chart') else '-'}")
        print("   display:", p.get("display","")[:200])
