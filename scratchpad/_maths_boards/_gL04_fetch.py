# -*- coding: utf-8 -*-
import json, io, os, urllib.request

LID = "fb13c12c-f5c1-4832-871b-40440d729361"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

url = BASE + "?id=eq." + LID + "&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode("utf-8"))
pd = data[0]["practice_data"]
io.open("_gL04_live.json", "w", encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("fetched. top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])), "problems")

# predump entry
pre = json.load(io.open("_pre_dump_maths-ocr.json", encoding="utf-8"))
entry = None
if isinstance(pre, dict):
    if LID in pre: entry = pre[LID]
    elif "graphs-L04" in pre: entry = pre["graphs-L04"]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==LID:
                entry=v; break
print("predump entry found:", entry is not None)
if entry is not None:
    io.open("_gL04_pre.json","w",encoding="utf-8").write(json.dumps(entry,ensure_ascii=False,indent=1))
