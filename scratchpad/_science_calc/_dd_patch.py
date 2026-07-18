import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
HERE=os.path.dirname(__file__)
pd=json.load(open(os.path.join(HERE,"lesson_higher-calculations-L06@d1cc4db5ec.json"),encoding="utf-8"))
ALL=["8334cfca-5401-4f27-a3de-3c2903ebe3f2"]
body=json.dumps({"practice_data":pd}).encode("utf-8")
for rid in ALL:
    req=urllib.request.Request(BASE+"?id=eq."+rid, data=body, method="PATCH",
        headers={"apikey":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Prefer":"return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH",rid,r.status)
# verify byte-identical readback + guided present
for rid in ALL:
    req=urllib.request.Request(BASE+"?id=eq."+rid+"&select=practice_data",headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    with urllib.request.urlopen(req) as r:
        live=json.load(r)[0]["practice_data"]
    same=json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False)
    print(rid,"guided:","guided" in live,"tier_guides:","tier_guides" in live,"identical:",same)
