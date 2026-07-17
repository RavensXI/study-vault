# -*- coding: utf-8 -*-
import os, json, io, urllib.request

with io.open("_EQ_L01_live.json", encoding="utf-8") as f:
    orig = json.load(f)
with io.open("lesson_maths-eduqas_algebra-L01.json", encoding="utf-8") as f:
    new = json.load(f)

# preservation check
for k in ("worked_examples","related_videos","topic_links","method_card"):
    assert json.dumps(orig[k],ensure_ascii=False,sort_keys=True)==json.dumps(new[k],ensure_ascii=False,sort_keys=True), "CHANGED: "+k
# problem displays/options preserved except gold[4]
for tier in ("bronze","silver","gold"):
    for i,(o,nw) in enumerate(zip(orig["problem_bank"][tier], new["problem_bank"][tier])):
        if tier=="gold" and i==4:
            assert nw["solutions"]==[0] and nw["options"][0]=="\\(xy\\)"
            continue
        assert o["display"]==nw["display"], "display changed %s[%d]"%(tier,i)
        assert o["options"]==nw["options"], "options changed %s[%d]"%(tier,i)
        assert o["solutions"]==nw["solutions"], "solutions changed %s[%d]"%(tier,i)
print("PRESERVATION OK (only gold[4] answer fixed; guided/tier_guides/hints/expects added)")

LID = "7e5e6d1a-aa08-4fbf-8094-760926f7e56c"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
body = json.dumps({"practice_data": new}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# round-trip verify
req2 = urllib.request.Request(f"{url}&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
assert live["problem_bank"]["gold"][4]["solutions"]==[0]
assert live["problem_bank"]["gold"][4]["options"][0]=="\\(xy\\)"
assert "guided" in live and "tier_guides" in live
assert live["problem_bank"]["bronze"][0]["hint"]
print("ROUND-TRIP OK: gold[4]=xy, guided+tier_guides+hints live")
