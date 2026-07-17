# -*- coding: utf-8 -*-
import json, os, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
def fetch(i):
    URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % i
    req = urllib.request.Request(URL, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

sib = fetch("4aa9afe1-7e47-4f0f-b7e6-da22be472716")
json.dump(sib, open("_G06_sib_edexcel.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("EDEXCEL SIBLING keys:", list(sib.keys()))
print("has guided:", "guided" in sib, "tier_guides:", "tier_guides" in sib)
pb=sib.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    ps=pb.get(t,[])
    print("---",t,len(ps))
    for i,p in enumerate(ps):
        print(" ",i, p.get("input_type"), "sol", p.get("solutions"), "chart" if p.get("chart") else "", "svg" if "<svg" in (p.get("display") or "") else "")
