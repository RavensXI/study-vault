# -*- coding: utf-8 -*-
import json, os, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
def fetch(i):
    URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % i
    req = urllib.request.Request(URL, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]
g1 = fetch("112923c0-364e-4701-91d9-280e7859d6d3")  # graphs-L01 eduqas
found=False
for t in ("bronze","silver","gold"):
    for i,p in enumerate((g1.get("problem_bank") or {}).get(t,[])):
        if p.get("chart"):
            print("=== %s[%d] chart ===" % (t,i))
            print(json.dumps(p["chart"], ensure_ascii=False)[:1800])
            found=True
            break
    if found: break
if not found:
    print("no chart in graphs-L01; checking guided/openers")
    print("keys", list(g1.keys()))
