import os, json, urllib.request, hashlib
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def fetch(rid, sel="practice_data"):
    url=f"{BASE}?id=eq.{rid}&select={sel}"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]
# first find valid meta columns
meta=fetch("d9384cf5-c3b4-4d2d-8f46-346f2c9a8ac6", "*")
print("COLUMNS:", list(meta.keys()))
canon=meta
prop=fetch("7227fd03-247e-4573-bd70-9ef85155bc5a","*")
json.dump(canon, open("_chk05_canon.json","w"), indent=2)
json.dump(prop, open("_chk05_prop.json","w"), indent=2)
c=json.dumps(canon["practice_data"], sort_keys=True, ensure_ascii=False)
p=json.dumps(prop["practice_data"], sort_keys=True, ensure_ascii=False)
print("PROP IDENTICAL:", c==p)
print("canon md5:", hashlib.md5(c.encode()).hexdigest())
print("prop  md5:", hashlib.md5(p.encode()).hexdigest())
for r,nm in [(canon,'canon'),(prop,'prop')]:
    print(nm, "| subject:", r.get("subject_slug"), "unit:", r.get("unit_slug"), "n:", r.get("lesson_number"), "title:", r.get("title"))
