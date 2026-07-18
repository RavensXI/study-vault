import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=["b2dd6adb-eb4b-4251-a9fd-3305d8493c16","ffdd38c1-b37c-4a37-83a2-12c4a58d9157"]
pd=json.load(open("lesson_physics-calculations-L03@330faf0468.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
for rid in IDS:
    req=urllib.request.Request(f"{BASE}?id=eq.{rid}",data=body,method="PATCH",
        headers={"apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req)
    print("PATCH",rid[:8],r.status)
# verify propagation: fetch back both, compare byte-identical to file
def get(rid):
    req=urllib.request.Request(f"{BASE}?id=eq.{rid}&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
live=[get(r) for r in IDS]
filecanon=json.dumps(pd,sort_keys=True,ensure_ascii=False)
a=json.dumps(live[0],sort_keys=True,ensure_ascii=False)
b=json.dumps(live[1],sort_keys=True,ensure_ascii=False)
print("live[0]==file:",a==filecanon)
print("live[1]==file:",b==filecanon)
print("live[0]==live[1] BYTE-IDENTICAL:",a==b)
json.dump(live[0],open("_live_canon_330.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
