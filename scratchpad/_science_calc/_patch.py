import os,json,io,urllib.request
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_higher-calculations-L02@b3c8bb1c4f.json",encoding="utf-8"))
all_ids=["c36f2b4d-aeaa-4c83-a6b2-9a5da3abb976"]
body=json.dumps({"practice_data":pd}).encode("utf-8")
for cid in all_ids:
    url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}"
    req=urllib.request.Request(url,data=body,method="PATCH",headers={
        "apikey":key,"Authorization":f"Bearer {key}",
        "Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req)
    print(cid,"->",r.status)
# verify byte-identical readback
import hashlib
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
loc=h(pd)
for cid in all_ids:
    url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
    live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    print(cid,"match:",h(live)==loc)
