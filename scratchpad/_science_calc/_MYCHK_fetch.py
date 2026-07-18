import os, json, urllib.request, hashlib, io
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def fetch(rid, sel):
    url=f"{BASE}?id=eq.{rid}&select={sel}"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]
canon="b76fdf39-830d-4e57-b20a-112818a6a3b2"
prop="300fd934-0f08-48bc-8082-efd556203b55"
c=fetch(canon,"practice_data,title,slug")
p=fetch(prop,"practice_data,title,slug")
def w(fn,obj): 
    with io.open(fn,"w",encoding="utf-8") as f: json.dump(obj,f,indent=1,ensure_ascii=False)
w("_MYCHK_canon.json",c["practice_data"])
w("_MYCHK_prop.json",p["practice_data"])
cs=json.dumps(c["practice_data"],sort_keys=True,ensure_ascii=False)
ps=json.dumps(p["practice_data"],sort_keys=True,ensure_ascii=False)
print("canon meta:", c.get("slug"), c.get("title"))
print("prop  meta:", p.get("slug"), p.get("title"))
print("pd identical:", cs==ps)
print("md5 canon:", hashlib.md5(cs.encode()).hexdigest())
print("md5 prop :", hashlib.md5(ps.encode()).hexdigest())
