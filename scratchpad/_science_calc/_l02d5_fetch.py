# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

rid = "1fcee1e4-25c6-422a-9b32-539ba52df304"
pd = get(rid)[0]["practice_data"]
with open("_l02d5_canonical.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

# scan em dashes + non-numeric solutions
def walk(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ('note','guided_skip_reason'): continue
            walk(v,p+'.'+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,p+'[%d]'%i)
    elif isinstance(o,str) and '—' in o:
        print("EMDASH", p, '::', o[:70])
walk(pd,'pd')
pb=pd['problem_bank']
print("title:", pd['method_card']['title'])
for t in ('bronze','silver','gold'):
    for i,pr in enumerate(pb[t]):
        for s in pr['solutions']:
            if not isinstance(s,(int,float)): print("NONNUM",t,i,repr(pr['solutions']))
        if 'expect' not in str(pr.get('misconceptions')): pass
# count misconceptions missing expect
for t in ('bronze','silver','gold'):
    for i,pr in enumerate(pb[t]):
        for j,m in enumerate(pr.get('misconceptions') or []):
            if 'expect' not in m: print("NOEXPECT",t,i,j)
