import json, os, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def fetch(rid):
    req=urllib.request.Request(BASE+"?id=eq."+rid+"&select=practice_data",
        headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]
ids=["b76fdf39-830d-4e57-b20a-112818a6a3b2","300fd934-0f08-48bc-8082-efd556203b55"]
for rid in ids:
    pd=fetch(rid)
    with open("_live_6e66_"+rid[:8]+".json","w",encoding="utf-8") as f:
        json.dump(pd,f,ensure_ascii=False,indent=1)
    print(rid, "written")
# byte-compare
a=json.dumps(fetch(ids[0]),sort_keys=True,ensure_ascii=False)
b=json.dumps(fetch(ids[1]),sort_keys=True,ensure_ascii=False)
print("PROP_IDENTICAL:", a==b)
