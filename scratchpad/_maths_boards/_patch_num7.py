# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "8696e75e-f9fd-40ef-b3a4-df27f5811c73"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-aqa_number-L07.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# re-fetch and confirm live == shard
u2 = url + "&select=practice_data"
req2 = urllib.request.Request(u2, headers={"apikey": key, "Authorization": "Bearer " + key})
livenow = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live == shard:", livenow == pd)
