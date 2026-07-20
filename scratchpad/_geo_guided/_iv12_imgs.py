import json, os, urllib.request
d=os.path.dirname(os.path.abspath(__file__))
pd=json.load(open(os.path.join(d,"_iv12_live.json"),encoding="utf-8"))
urls={}
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        if "image" in p: urls.setdefault(p["image"],[]).append("%s[%d]"%(t,i))
for u,ps in urls.items():
    name="_m_"+u.rsplit("/",1)[-1]
    ok=os.path.exists(os.path.join(d,name))
    if not ok:
        try:
            req=urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
            data=urllib.request.urlopen(req).read()
            open(os.path.join(d,name),"wb").write(data)
            ok="downloaded %d bytes"%len(data)
        except Exception as e:
            ok="ERROR %s"%e
    print(ok, u.rsplit("/",1)[-1], ps)
