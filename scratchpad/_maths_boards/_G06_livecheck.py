# -*- coding: utf-8 -*-
import json, io, os, urllib.request
ID = "683b816a-4d56-4d3d-911b-58cb3bca5efd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
req = urllib.request.Request(
    "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID,
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    got = json.load(r)[0]["practice_data"]
json.dump(got, io.open("_G06_livecheck.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
mine = json.load(io.open("_G06_final.json", encoding="utf-8"))

def norm(o):
    if isinstance(o,dict): return {k:norm(v) for k,v in o.items()}
    if isinstance(o,list): return [norm(v) for v in o]
    if isinstance(o,float) and o.is_integer(): return int(o)
    return o

diffs=[]
def walk(a,b,p):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in set(a)|set(b):
            if k not in a: diffs.append(p+"."+k+" MISSING in mine")
            elif k not in b: diffs.append(p+"."+k+" MISSING in live")
            else: walk(a[k],b[k],p+"."+k)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): diffs.append(p+" len %d vs %d"%(len(a),len(b)))
        else:
            for i,(x,y) in enumerate(zip(a,b)): walk(x,y,p+"[%d]"%i)
    else:
        if a!=b: diffs.append("%s: %r vs %r"%(p,a,b))
walk(norm(mine),norm(got),"pd")
print("semantic diffs (after int/float normalisation):", len(diffs))
for d in diffs[:30]: print("  -",d)
