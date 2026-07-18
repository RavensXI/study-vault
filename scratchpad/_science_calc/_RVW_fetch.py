# -*- coding: utf-8 -*-
import os, json, urllib.request
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
def fetch(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data[0]["practice_data"] if data else None
canonical = "8b8d72ed-5bdb-44b2-82e8-a7272e91d854"
others = ["bac68e76-4566-4e8d-abf9-dfc663d025c9","96d403a1-e64b-4825-a7ff-65024b56a797","4e49ce91-9170-40f1-9003-4874980679ec","0cca9081-c7cf-434b-96ad-49b07dfe47b7","e9e20197-3642-4e15-8859-0254705f3b39","e6ccebe9-cd02-442f-be9c-e257fe791f66"]
cd = fetch(canonical)
with open("_RVW_canonical.json","w",encoding="utf-8") as f:
    json.dump(cd, f, ensure_ascii=False, indent=1)
cstr = json.dumps(cd, ensure_ascii=False, sort_keys=True)
print("canonical bytes:", len(cstr))
for rid in others:
    od = fetch(rid)
    ostr = json.dumps(od, ensure_ascii=False, sort_keys=True)
    print(rid, "identical:", ostr == cstr, "len:", len(ostr))
