# -*- coding: utf-8 -*-
import json, io, os, urllib.request

ID = "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(URL, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode("utf-8"))
pd = data[0]["practice_data"]
json.dump(pd, io.open("_numL03_live.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("LIVE top keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    ps = pb.get(t) or []
    print("---", t, "n=", len(ps), "desc=", repr(pb.get(t+"_description")))
    for i,p in enumerate(ps):
        print("  [%d]"%i, "it=", p.get("input_type"), "calc=", p.get("calculator"),
              "sols=", p.get("solutions"))
        print("      disp:", (p.get("display") or "")[:140])

# pre-dump entry
dump = json.load(io.open("_pre_dump_maths-ocr.json", encoding="utf-8"))
for row in dump:
    if row["id"] == ID:
        json.dump(row["practice_data"], io.open("_pre_numL03.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
        print("PRE-DUMP saved; title=", row["title"])
        break
