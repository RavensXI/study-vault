# -*- coding: utf-8 -*-
import json, os, urllib.request
ID = "44ea1f33-8979-4e3e-83b8-d2bfd93e3ee5"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_live_ocr_algL03.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    probs = pb.get(t, [])
    print("\n===", t, "(%d)" % len(probs), "desc:", pb.get(t+"_description"))
    for i,p in enumerate(probs):
        print(" [%d]" % i, "it=", p.get("input_type"), "calc=", p.get("calculator"),
              "sol=", p.get("solutions"), "| ", p.get("display"))
        if p.get("options"): print("      opts:", p.get("options"))
