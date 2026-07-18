import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=[
 "2dc58e27-b4f5-42e5-9d45-0e632c9a2371",
 "a6d04da2-b3f8-439b-bd35-1fe691f4d37d",
 "6b4930c0-ab0c-42b9-a107-f71ada9b89b4",
 "98056365-9b88-4bb1-9cdc-9383ad899a3b",
 "3a52b887-a361-4c21-b41c-0f29dac86d7c",
 "0b703489-9aa1-4f45-a17a-3e372482390a",
 "eac3d993-5c56-4ed3-834e-0ebd6ce733b2",
]
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
def patch(rid, pd):
    url=f"{BASE}?id=eq.{rid}"
    body=json.dumps({"practice_data":pd}).encode("utf-8")
    req=urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey":KEY,"Authorization":f"Bearer {KEY}",
        "Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req); return r.status

import io
pre=json.load(io.open("_canon_215be42800.json",encoding="utf-8"))
new=json.load(io.open("lesson_physics-calculations-L03@215be42800.json",encoding="utf-8"))
prekey=json.dumps(pre,sort_keys=True,ensure_ascii=False)

# 1. pre-check every row currently matches the pre-edit canonical
for rid in IDS:
    cur=get(rid)
    same = json.dumps(cur,sort_keys=True,ensure_ascii=False)==prekey
    print("PRECHECK", rid, "identical-to-canon:", same,
          "| title:", cur.get("method_card",{}).get("title"))

# 2. patch all
newblob=json.dumps(new,sort_keys=True,ensure_ascii=False)
for rid in IDS:
    st=patch(rid,new)
    print("PATCH", rid, st)

# 3. verify all 7 now byte-identical to new
allok=True
for rid in IDS:
    cur=get(rid)
    same=json.dumps(cur,sort_keys=True,ensure_ascii=False)==newblob
    if not same: allok=False
    print("VERIFY", rid, "identical-to-new:", same)
print("ALL_OK", allok)
