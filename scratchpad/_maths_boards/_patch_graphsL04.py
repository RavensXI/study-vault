# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "b73c61cf-00b8-44c8-9e08-9f7f6f84c60a"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_graphs-L04.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
gurl = url + "&select=practice_data"
greq = urllib.request.Request(gurl, headers={"apikey": key, "Authorization": "Bearer " + key})
back = json.load(urllib.request.urlopen(greq))[0]["practice_data"]
checks = [
    "guided" in back,
    "tier_guides" in back,
    back["problem_bank"]["bronze"][2]["solutions"] == [24],
    len(back["problem_bank"]["gold"][0].get("chart", {})) > 0,
    back["problem_bank"]["silver"][4].get("chart") is not None,
    back["guided"]["opener"]["steps"][0]["answer"] == 6,
]
print("round-trip checks:", checks, "ALL" if all(checks) else "FAIL")
