import os, json, urllib.request, hashlib
SB="https://baipckgywpnwapobwtsy.supabase.co"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
IDS=["e6963758-b327-488c-87b4-177b336f29e9","07e5d6c1-74ac-4da9-9942-7f440105e339",
"5d2257b8-5623-4832-8653-d33cbc36e417","60250fe9-465d-4667-9e15-4a601759e100",
"17bbd05b-fda5-4bde-9932-fe62b9670913","3dfe27ee-0fe0-4042-91f6-023c5d626e5b",
"ca3b27a3-d2a5-4735-bb3e-507167e7ff77"]
hashes=set()
for rid in IDS:
    url=f"{SB}/rest/v1/lessons?id=eq.{rid}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    h=hashlib.sha256(json.dumps(pd,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    hashes.add(h)
    if rid==IDS[0]:
        json.dump(pd,open("_live_canon_verify.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("distinct hashes across 7 rows:", len(hashes), "(1 = byte-identical)")
