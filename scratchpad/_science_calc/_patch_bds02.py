import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids=["b76fdf39-830d-4e57-b20a-112818a6a3b2","300fd934-0f08-48bc-8082-efd556203b55"]
pd=json.load(io.open("lesson_biology-data-skills-L02@6e66d8eeba.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
for rid in ids:
    req=urllib.request.Request(BASE+"?id=eq."+rid, data=body, method="PATCH",
        headers={"apikey":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req); print("PATCH",rid,r.status)
# verify byte-identical
def get(rid):
    req=urllib.request.Request(BASE+"?id=eq."+rid+"&select=practice_data",headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
canon=json.dumps(get(ids[0]),sort_keys=True,ensure_ascii=False)
want=json.dumps(pd,sort_keys=True,ensure_ascii=False)
print("canon matches file:", canon==want)
print("sibling matches canon:", json.dumps(get(ids[1]),sort_keys=True,ensure_ascii=False)==canon)
