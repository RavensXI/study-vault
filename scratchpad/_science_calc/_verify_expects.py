# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rowid):
    url = BASE + "?id=eq." + rowid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

pd = json.load(open("_live_canonical.json", encoding="utf-8"))

# expects outside accept
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sols = p["solutions"]; acc = p.get("accept")
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is None: continue
            ev = e if isinstance(e,list) else [e]
            if len(ev)==len(sols):
                inside = all(abs(float(a)-float(b)) <= (acc or 0) for a,b in zip(ev,sols))
                tag = "DEAD(inside accept)" if inside and acc is not None else "ok"
                if tag!="ok":
                    print(f"{tier}[{i}].misc[{j}] expect={e} sol={sols} accept={acc} -> {tag}")
print("expect scan done")

# all 7 propagation
ids = ["539110f5-5600-4dde-bee7-54fb60554f18","06772e71-a44d-47fa-967d-7ae17524126b",
"550f4c75-d1fa-4f6e-a2de-2a0f0b317bd8","d8149466-9dcb-46b2-9599-bfe559f3bd36",
"87deed73-6660-4019-bb2a-57f708b45ed8","b18f7be8-c8d8-44e6-ac6d-4246b0a7fc27",
"1cc093ed-5247-4a15-b162-fcc764763d2b"]
can = json.dumps(fetch(ids[0]), ensure_ascii=False, sort_keys=True)
for i in ids:
    s = json.dumps(fetch(i), ensure_ascii=False, sort_keys=True)
    print(i, "IDENTICAL" if s==can else "DIFFERENT")
